"""Async OpenRouter client with a disk cache (results/llm_cache.jsonl), a per-call cost ledger (results/api_cost_ledger.jsonl)
and a hard cumulative spend stop. Keys/URLs come only from os.environ (never printed or saved)."""
from __future__ import annotations

import asyncio
import json
import os
import time
from pathlib import Path

import aiohttp
from loguru import logger

from csc import parse_response, prompt_key

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
CACHE_P = RES / "llm_cache.jsonl"
LEDGER_P = RES / "api_cost_ledger.jsonl"
HARD_STOP = 9.5
REASK = "Return only the JSON object."


class BudgetExceeded(Exception):
    pass


class DailyLimit(Exception):
    pass


def load_cache() -> dict:
    out = {}
    if CACHE_P.exists():
        for line in CACHE_P.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                out[r["key"]] = r
    return out


def ledger_total() -> float:
    if not LEDGER_P.exists():
        return 0.0
    return sum(json.loads(l).get("usd", 0.0) for l in LEDGER_P.read_text().splitlines() if l.strip())


class Client:
    def __init__(self, concurrency: int = 24, hard_stop: float = HARD_STOP, stop_at: float | None = None):
        RES.mkdir(exist_ok=True)
        self.cache = load_cache()
        self.spent = ledger_total()
        self.hard_stop = hard_stop
        self.stop_at = min(stop_at or hard_stop, hard_stop)
        self.sem = asyncio.Semaphore(concurrency)
        self.base = os.environ["OPENROUTER_BASE_URL"].rstrip("/")
        self.key = os.environ["OPENROUTER_API_KEY"]
        self.n_calls = 0
        self.n_fail = 0
        self.stopped = False
        self.daily_limit = False

    def _append(self, p: Path, rec: dict) -> None:
        with open(p, "a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

    async def _post(self, session, model: str, messages: list[dict], extra: dict) -> tuple[dict | None, str | None]:
        body = {"model": model, "messages": messages, "temperature": 0.0, "max_tokens": 600, "usage": {"include": True}, **extra}
        for attempt in range(3):  # transient HTTP errors only (5xx / network); no content retry loops
            try:
                async with session.post(self.base + "/chat/completions", json=body,
                                        headers={"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"},
                                        timeout=aiohttp.ClientTimeout(total=180)) as r:
                    txt = await r.text()
                    if r.status in (402, 429) and ("limit" in txt.lower() or "credit" in txt.lower()):
                        if r.status == 402 or "daily" in txt.lower() or "key limit" in txt.lower():
                            raise DailyLimit(txt[:200])
                        await asyncio.sleep(5 * (attempt + 1))
                        continue
                    if r.status >= 500:
                        await asyncio.sleep(3 * (attempt + 1))
                        continue
                    d = json.loads(txt)
                    if "choices" not in d:
                        return None, f"http{r.status}:{txt[:200]}"
                    return d, None
            except (aiohttp.ClientError, asyncio.TimeoutError, json.JSONDecodeError) as e:
                err = f"{type(e).__name__}:{str(e)[:100]}"
                await asyncio.sleep(3 * (attempt + 1))
        return None, "transient_exhausted"

    async def call(self, session, key: str, model: str, extra: dict, messages: list[dict], tag: str) -> dict:
        if key in self.cache:
            return self.cache[key]
        async with self.sem:
            if self.spent >= self.stop_at or self.stopped:
                self.stopped = True
                raise BudgetExceeded(f"spent {self.spent:.4f} >= stop_at {self.stop_at}")
            t0 = time.time()
            d, err = await self._post(session, model, messages, extra)
            recs = []
            raw = None
            usage = {}
            provider = None
            if d is not None:
                raw = d["choices"][0]["message"].get("content") or ""
                usage = d.get("usage") or {}
                provider = d.get("provider")
                recs.append(usage)
            parsed = parse_response(raw)
            reask = False
            if d is not None and parsed["route"] not in ("json", "json_fenced", "json_regex"):
                # ONE re-ask with the raw answer in context; still failing -> fol from the fallback route or None (counted)
                reask = True
                d2, err2 = await self._post(session, model, messages + [{"role": "assistant", "content": raw},
                                                                       {"role": "user", "content": REASK}], extra)
                if d2 is not None:
                    raw2 = d2["choices"][0]["message"].get("content") or ""
                    recs.append(d2.get("usage") or {})
                    p2 = parse_response(raw2)
                    if p2["route"] in ("json", "json_fenced", "json_regex"):
                        parsed = {**p2, "route": "reask_" + p2["route"]}
                        raw = raw + "\n<<REASK>>\n" + raw2
            usd = float(sum(float(u.get("cost") or 0.0) for u in recs))
            secs = time.time() - t0
            self.spent += usd
            self.n_calls += 1
            rec = {"key": key, "model": model, "tag": tag, "raw": raw, "fol": parsed["fol"], "alt_fol": parsed["alt_fol"],
                   "route": parsed["route"], "reask": reask, "error": err, "usd": usd, "secs": round(secs, 2),
                   "in_tok": sum(int(u.get("prompt_tokens") or 0) for u in recs),
                   "out_tok": sum(int(u.get("completion_tokens") or 0) for u in recs), "provider": provider, "ts": time.time()}
            self._append(LEDGER_P, {k: rec[k] for k in ("key", "model", "tag", "usd", "secs", "in_tok", "out_tok", "provider", "ts", "reask")})
            if d is None:
                self.n_fail += 1
                logger.warning(f"call failed {model} {tag}: {err}")
                return rec  # failures are not cached (a later run may retry them once)
            self.cache[key] = rec
            self._append(CACHE_P, rec)
            logger.debug(f"[{tag}] {model} ${usd:.6f} {secs:.1f}s route={parsed['route']} fol={str(parsed['fol'])[:120]}")
            return rec


async def run_jobs(jobs: list[dict], concurrency: int = 24, stop_at: float | None = None, log_every: int = 200) -> dict:
    """jobs: [{'key','model','extra','messages','tag'}] (deduplicated by key). Returns {key: record}."""
    cl = Client(concurrency=concurrency, stop_at=stop_at)
    todo = [j for j in jobs if j["key"] not in cl.cache]
    logger.info(f"run_jobs: {len(jobs)} jobs, {len(jobs) - len(todo)} cached, {len(todo)} to call; spent so far ${cl.spent:.4f}; stop_at ${cl.stop_at}")
    out = {j["key"]: cl.cache[j["key"]] for j in jobs if j["key"] in cl.cache}
    t0 = time.time()
    done = 0
    async with aiohttp.ClientSession(headers={"User-Agent": "aii-csc/1.0"}) as session:
        async def one(j):
            nonlocal done
            try:
                r = await cl.call(session, j["key"], j["model"], j["extra"], j["messages"], j["tag"])
                out[j["key"]] = r
            except BudgetExceeded:
                pass
            except DailyLimit as e:
                cl.daily_limit = True
                cl.stopped = True
                logger.error(f"daily limit hit: {str(e)[:120]}")
            done += 1
            if done % log_every == 0:
                el = time.time() - t0
                logger.info(f"  {done}/{len(todo)} calls, ${cl.spent:.4f} total, {el:.0f}s elapsed, fails {cl.n_fail}")
        await asyncio.gather(*[one(j) for j in todo], return_exceptions=False)
    logger.info(f"run_jobs done: calls {cl.n_calls}, fails {cl.n_fail}, spent ${cl.spent:.4f}, stopped={cl.stopped}, daily_limit={cl.daily_limit}, {time.time()-t0:.0f}s")
    return {"records": out, "spent": cl.spent, "stopped": cl.stopped, "daily_limit": cl.daily_limit, "n_calls": cl.n_calls, "n_fail": cl.n_fail}
