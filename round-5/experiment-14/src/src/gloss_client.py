"""Async OpenRouter gloss client (pattern of dataset-5 src/gloss.py): Semaphore(8), temperature 0, reasoning disabled,
one re-ask on unparseable JSON (then every item of the call = NO, counted as unparseable), exponential-backoff retries on
transport / 429 / 5xx, no retry on 402/403 quota errors. Every call -> cost_ledger.jsonl (ts, model, prompt_tok,
completion_tok, reasoning_tok, usd = usage.cost, cumulative_usd); every verdict -> results/gloss_cache.jsonl keyed by
checker|prompt_sha|sentence_id|item key, so re-runs never re-bill. HARD STOP: no call starts once the artifact total
reaches the cap (default $2.00; sweeps pass stop_at = cap - 10% reserve)."""
from __future__ import annotations

import asyncio
import json
import os
import time
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "cost_ledger.jsonl"
CACHE = ROOT / "results" / "gloss_cache.jsonl"
HARD_CAP = 2.00
MODEL_EXTRA = {"google/gemini-2.5-flash": {"reasoning": {"max_tokens": 0}}, "openai/gpt-4.1-mini": {},
               "mistralai/mistral-small-3.2-24b-instruct": {}}


class QuotaError(RuntimeError):
    pass


class BudgetStop(RuntimeError):
    pass


def spent() -> float:
    if not LEDGER.exists():
        return 0.0
    return sum(float(json.loads(l).get("usd") or 0.0) for l in LEDGER.read_text().splitlines() if l.strip())


def load_cache() -> dict:
    out = {}
    if CACHE.exists():
        for l in CACHE.read_text().splitlines():
            if l.strip():
                r = json.loads(l)
                out[r["key"]] = r["verdict"]
    return out


def ckey(checker: str, psha: str, sid: str, item_key) -> str:
    return f"{checker}|{psha[:16]}|{sid}|{json.dumps(item_key, ensure_ascii=False)}"


class Client:
    def __init__(self, model: str, phase: str, stop_at: float = HARD_CAP, concurrency: int = 8, logger=None):
        self.model, self.phase, self.stop_at, self.log = model, phase, min(stop_at, HARD_CAP), logger
        self.sem = asyncio.Semaphore(concurrency)
        self.lock = asyncio.Lock()
        self.base = os.environ["OPENROUTER_BASE_URL"].rstrip("/")
        self.key = os.environ["OPENROUTER_API_KEY"]
        self.total = spent()
        self.stop = False
        self.stats = {"calls": 0, "unparseable_calls": 0, "reasoning_tokens": 0, "prompt_tokens": 0, "completion_tokens": 0,
                      "usd": 0.0, "secs": 0.0}

    async def chat(self, http: httpx.AsyncClient, messages: list[dict], max_tokens: int) -> str | None:
        if self.stop:
            raise QuotaError("stopped")
        if self.total >= self.stop_at:
            raise BudgetStop(f"spend {self.total:.4f} >= stop {self.stop_at}")
        body = {"model": self.model, "messages": messages, "temperature": 0, "max_tokens": max_tokens,
                "usage": {"include": True}, **MODEL_EXTRA.get(self.model, {})}
        async with self.sem:
            for attempt in range(5):
                t0 = time.time()
                try:
                    r = await http.post(f"{self.base}/chat/completions", json=body, headers={"Authorization": f"Bearer {self.key}"})
                except httpx.HTTPError as e:
                    if self.log:
                        self.log.warning(f"http error {type(e).__name__} attempt {attempt}")
                    await asyncio.sleep(2 ** attempt)
                    continue
                if r.status_code in (402, 403):
                    self.stop = True
                    raise QuotaError(f"{r.status_code}: {r.text[:200]}")
                if r.status_code != 200:
                    if self.log:
                        self.log.warning(f"status {r.status_code}: {r.text[:200]} attempt {attempt}")
                    await asyncio.sleep(2 ** attempt)
                    continue
                d = r.json()
                if "error" in d or not d.get("choices"):
                    if self.log:
                        self.log.warning(f"error body {str(d.get('error'))[:200]} attempt {attempt}")
                    await asyncio.sleep(2 ** attempt)
                    continue
                u = d.get("usage") or {}
                usd = float(u.get("cost") or 0.0)
                rt = (u.get("completion_tokens_details") or {}).get("reasoning_tokens") or 0
                async with self.lock:
                    self.total += usd
                    self.stats["calls"] += 1
                    self.stats["usd"] += usd
                    self.stats["reasoning_tokens"] += rt
                    self.stats["prompt_tokens"] += u.get("prompt_tokens") or 0
                    self.stats["completion_tokens"] += u.get("completion_tokens") or 0
                    self.stats["secs"] += time.time() - t0
                    with LEDGER.open("a") as fh:
                        fh.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "phase": self.phase,
                                             "model": self.model, "provider": d.get("provider"), "prompt_tok": u.get("prompt_tokens"),
                                             "completion_tok": u.get("completion_tokens"), "reasoning_tok": rt, "usd": usd,
                                             "cumulative_usd": round(self.total, 6)}) + "\n")
                txt = d["choices"][0].get("message", {}).get("content")
                if self.log:
                    self.log.debug(f"{self.model} <- {messages[-1]['content'][:300]!r} -> {str(txt)[:300]!r}")
                return txt
        return None


async def run_calls(client: Client, calls: list[dict], parse, psha: str, max_tokens: int = 200) -> dict:
    """calls: [{'sid', 'messages', 'keys': [item_key, ...]}]. parse(txt, n) -> {i: 'YES'|'NO'} | None.
    Returns {cache_key: verdict} with verdict YES / NO / NO_UNPARSEABLE / NOT_RUN(<reason>)."""
    cache = load_cache()
    out = {}
    todo = []
    for c in calls:
        ks = [ckey(client.model, psha, c["sid"], k) for k in c["keys"]]
        if all(k in cache for k in ks):
            out.update({k: cache[k] for k in ks})
        else:
            todo.append((c, ks))

    async def one(http, c, ks):
        v = None
        try:
            for _ask in range(2):
                txt = await client.chat(http, c["messages"], max_tokens)
                v = parse(txt, len(ks))
                if v is not None:
                    break
        except (QuotaError, BudgetStop) as e:
            for k in ks:
                out[k] = f"NOT_RUN({type(e).__name__})"
            return
        if v is None:
            client.stats["unparseable_calls"] += 1
        rec = []
        for i, k in enumerate(ks):
            verdict = v[i + 1] if v else "NO_UNPARSEABLE"
            out[k] = verdict
            rec.append({"key": k, "verdict": verdict, "model": client.model, "phase": client.phase})
        async with client.lock:
            with CACHE.open("a") as fh:
                for r in rec:
                    fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    async with httpx.AsyncClient(timeout=120) as http:
        res = await asyncio.gather(*[one(http, c, ks) for c, ks in todo], return_exceptions=True)
    errs = [r for r in res if isinstance(r, Exception)]
    if errs and client.log:
        client.log.error(f"{len(errs)} calls raised; first {type(errs[0]).__name__}: {errs[0]}")
    return out
