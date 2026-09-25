"""Budget-guarded async OpenRouter client. EVERY LLM call of this artifact goes through Budget.call().

* Before a call: estimated cost = prompt_tokens_est * price_in + max_tokens * price_out; the call is REFUSED if
  spent + estimate would exceed the component cap or the total cap.
* After a call: actual cost from usage.cost (OpenRouter usage accounting) or tokens x catalogue price.
  Appended to results/costs.jsonl and to the run's AII_COST_LEDGER; spent state persisted to results/budget_state.json.
* Retries: 3 with exponential backoff on 429/5xx/network errors; the caller handles JSON-parse retries.
"""
from __future__ import annotations

import asyncio
import json
import os
import time
from pathlib import Path

import aiohttp
from loguru import logger

ROOT = Path(__file__).resolve().parent.parent

RES = ROOT / "results"
# iteration 3 (T1 API bar): the run key works ONLY at OPENROUTER_BASE_URL -> never hard-code OpenRouter's own host
BASE = os.environ.get("OPENROUTER_BASE_URL", "").rstrip("/")
URL = BASE + "/chat/completions"
MODELS_URL = BASE + "/models"
KEY_URL = BASE + "/key"

# T1 caps (sum 4.60 = hard total) are loaded from prereg_T1.json['budget'] once it exists; the defaults below are the
# same numbers (used only by the label-blind pilots, which run before the freeze and count against the same caps)
CAP_TOTAL = 4.60
CAPS = {"judge_cheap": 0.75, "judge_cheap2": 0.45, "strong": 2.50, "roundtrip": 0.35, "sc5": 0.50, "retest": 0.05}
_PT1 = ROOT / "prereg_T1.json"
if _PT1.exists():
    _b = json.loads(_PT1.read_text()).get("budget", {})
    CAP_TOTAL = float(_b.get("cap_total", CAP_TOTAL))
    CAPS = {k: float(v) for k, v in _b.get("caps", CAPS).items()}
DEAD_MARKERS = ("402", "insufficient", "limit exceeded", "Key limit", "credits")


class BudgetExceeded(RuntimeError):
    pass


def load_prices(refresh: bool = False) -> dict:
    p = RES / "prices.json"
    if p.exists() and not refresh:
        return json.loads(p.read_text())
    import requests
    d = requests.get(MODELS_URL, timeout=60, headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"}).json()["data"]
    prices = {m["id"]: {"in": float(m["pricing"]["prompt"]), "out": float(m["pricing"]["completion"]),
                        "params": m.get("supported_parameters", [])} for m in d}
    p.write_text(json.dumps(prices, indent=0))
    return prices


def est_tokens(text: str) -> int:
    return int(len(text) / 3.2) + 8


class Budget:
    def __init__(self, concurrency: int = 16):
        RES.mkdir(exist_ok=True)
        self.state_p = RES / "budget_state.json"
        self.cost_p = RES / "costs.jsonl"
        # spend is re-derived from the append-only costs.jsonl (shared by concurrent stage processes; each process
        # spends only its own components, and the component caps sum to CAP_TOTAL, so caps hold across processes)
        self.by_comp = self._ledger_by_component()
        self.spent = sum(self.by_comp.values())
        self.pending = 0.0  # reserved estimates of in-flight calls
        self.pending_comp: dict[str, float] = {}
        self.prices = load_prices()
        self.sem = asyncio.Semaphore(concurrency)
        self.session: aiohttp.ClientSession | None = None
        self.key = os.environ["OPENROUTER_API_KEY"]
        self.ledger = os.environ.get("AII_COST_LEDGER")
        self.n_calls = 0
        self.dead = False  # set when the shared key returns 402 / daily-limit errors: every later call is refused fast

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=240))
        return self

    async def __aexit__(self, *a):
        await self.session.close()
        self._persist()

    def _ledger_by_component(self) -> dict[str, float]:
        out: dict[str, float] = {}
        if self.cost_p.exists():
            for l in self.cost_p.read_text().splitlines():
                try:
                    r = json.loads(l)
                except json.JSONDecodeError:
                    continue
                out[r["component"]] = out.get(r["component"], 0.0) + float(r.get("cost") or 0.0)
        return out

    def _persist(self):
        by = self._ledger_by_component()  # all processes' spend (the file is the single source of truth)
        self.state_p.write_text(json.dumps({"spent": round(sum(by.values()), 6), "by_component": by,
                                            "this_process": {"spent": round(self.spent, 6), "by_component": self.by_comp},
                                            "cap_total": CAP_TOTAL, "caps": CAPS, "ts": time.time()}, indent=1))

    def remaining(self, component: str) -> float:
        return min(CAP_TOTAL - self.spent - self.pending,
                   CAPS[component] - self.by_comp.get(component, 0.0) - self.pending_comp.get(component, 0.0))

    async def call(self, *, component: str, model: str, messages: list[dict], max_tokens: int, item_id: str = "",
                   temperature: float = 0.0, extra: dict | None = None) -> dict:
        """Returns {'text', 'logprobs', 'cost', 'in_tok', 'out_tok', 'seconds', 'raw_usage'}; raises BudgetExceeded."""
        pr = self.prices.get(model)
        if pr is None:
            raise ValueError(f"model {model} not in catalogue")
        prompt_chars = sum(len(m["content"]) for m in messages)
        # reservation: prompt + min(max_tokens, 600) output tokens (+800 reasoning tokens); real cost booked afterwards
        est = est_tokens("x" * prompt_chars) * pr["in"] + min(max_tokens, 600) * pr["out"]
        if (extra or {}).get("reasoning"):
            est += 800 * pr["out"]
        body = {"model": model, "messages": messages, "max_tokens": max_tokens, "temperature": temperature,
                "usage": {"include": True}}
        if extra:
            body.update(extra)
        if self.dead:
            raise BudgetExceeded("key_dead: shared OpenRouter key exhausted (402/limit)")
        async with self.sem:  # reserve only for in-flight calls (queued coroutines must not pre-reserve the budget)
            if est > self.remaining(component):
                raise BudgetExceeded(f"{component}: est {est:.5f} > remaining {self.remaining(component):.5f}")
            self.pending += est
            self.pending_comp[component] = self.pending_comp.get(component, 0.0) + est
            try:
                t0 = time.time()
                data = None
                for attempt in range(4):
                    try:
                        async with self.session.post(URL, json=body, headers={"Authorization": f"Bearer {self.key}"}) as r:
                            txt = await r.text()
                            if r.status in (402, 403) and any(m.lower() in txt.lower() for m in DEAD_MARKERS + ("403",)):
                                self.dead = True
                                raise BudgetExceeded(f"key_dead: HTTP 402 {txt[:200]}")
                            if r.status == 429 or r.status >= 500:
                                raise aiohttp.ClientResponseError(r.request_info, (), status=r.status, message=txt[:200])
                            data = json.loads(txt)
                            if "error" in data and not data.get("choices"):
                                code = data["error"].get("code", 0)
                                if isinstance(code, int) and (code == 429 or code >= 500) and attempt < 3:
                                    raise aiohttp.ClientResponseError(r.request_info, (), status=code, message=str(data["error"])[:200])
                                if code == 402 or any(m.lower() in str(data["error"]).lower() for m in DEAD_MARKERS):
                                    self.dead = True
                                    raise BudgetExceeded(f"key_dead: {str(data['error'])[:200]}")
                                raise RuntimeError(f"OpenRouter error: {str(data['error'])[:300]}")
                            break
                    except (aiohttp.ClientError, asyncio.TimeoutError, json.JSONDecodeError) as e:
                        if attempt == 3:
                            raise RuntimeError(f"network/5xx after retries: {str(e)[:200]}") from e
                        await asyncio.sleep(2 ** attempt + 0.5)
                secs = time.time() - t0
            finally:
                self.pending -= est
                self.pending_comp[component] -= est
        usage = data.get("usage") or {}
        in_tok, out_tok = int(usage.get("prompt_tokens", 0)), int(usage.get("completion_tokens", 0))
        cost = usage.get("cost")
        cost = float(cost) if cost is not None else in_tok * pr["in"] + out_tok * pr["out"]
        self.spent += cost
        self.by_comp[component] = self.by_comp.get(component, 0.0) + cost
        self.n_calls += 1
        rec = {"ts": time.time(), "component": component, "model": model, "item_id": item_id, "in_tok": in_tok,
               "out_tok": out_tok, "cost": cost, "seconds": round(secs, 3)}
        with self.cost_p.open("a") as f:
            f.write(json.dumps(rec) + "\n")
        if self.ledger:
            try:
                with open(self.ledger, "a") as f:
                    f.write(json.dumps({"ts": rec["ts"], "tool": "openrouter", "cost_usd": cost, "model": model,
                                        "component": component}) + "\n")
            except OSError:
                pass
        if self.n_calls % 10 == 0:  # costs.jsonl (written on EVERY call, above) is the per-call record
            self._persist()
        ch = (data.get("choices") or [{}])[0]
        msg = ch.get("message") or {}
        text = msg.get("content") or ""
        logger.debug(f"[{component}] {model} {item_id} in={in_tok} out={out_tok} ${cost:.6f} -> {text[:160]!r}")
        return {"text": text, "logprobs": ch.get("logprobs"), "cost": cost, "in_tok": in_tok, "out_tok": out_tok,
                "seconds": secs, "finish": ch.get("finish_reason")}
