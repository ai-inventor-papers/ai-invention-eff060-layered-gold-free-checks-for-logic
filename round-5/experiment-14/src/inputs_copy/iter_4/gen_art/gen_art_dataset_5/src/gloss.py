"""Gloss checker client: two family-disjoint checkers rate (symbol use, proposed meaning) pairs, <= 12 per call, one
sentence per call, temperature 0, prompt gloss_v1 (hashed in the prereg). Every call is written to cost_ledger.jsonl
and every verdict to results/gloss_cache.jsonl (keyed by checker|prompt_version|sentence_id|use|meaning), so re-runs
never re-bill. Budget guard: stops before a call when the artifact total would pass HARD_STOP_USD.
The checker never sees a whole candidate formula, a reading, a label, or which map was z3-equivalent.
"""
from __future__ import annotations

import asyncio
import json
import os
import random
import re
import time
from pathlib import Path

import httpx

from common import RES, ROOT, sha1

CHECKERS = {"haiku": "anthropic/claude-haiku-4.5", "qwen": "qwen/qwen3-235b-a22b-2507"}
AUDITOR = "anthropic/claude-sonnet-5"
HARD_STOP_USD = 6.0
LEDGER = ROOT / "cost_ledger.jsonl"
CACHE = RES / "gloss_cache.jsonl"
_lock = asyncio.Lock()


class BudgetExceeded(RuntimeError):
    pass


class QuotaError(RuntimeError):
    pass


def spent() -> float:
    if not LEDGER.exists():
        return 0.0
    return sum(json.loads(l).get("usd", 0.0) for l in LEDGER.read_text().splitlines() if l.strip())


def load_prompt(version: str = "gloss_v1") -> dict:
    return json.loads((ROOT / "prompts" / f"{version}.json").read_text())


def cache_key(checker: str, version: str, sid: str, use: str, meaning: str) -> str:
    return sha1(f"{checker}|{version}|{sid}|{use}|{meaning}")


def load_cache() -> dict:
    out = {}
    if CACHE.exists():
        for l in CACHE.read_text().splitlines():
            if l.strip():
                r = json.loads(l)
                out[r["key"]] = r["verdict"]
    return out


class Client:
    def __init__(self, phase: str, concurrency: int = 8):
        self.phase = phase
        self.sem = asyncio.Semaphore(concurrency)
        self.base = os.environ["OPENROUTER_BASE_URL"].rstrip("/")
        self.key = os.environ["OPENROUTER_API_KEY"]
        self.http = httpx.AsyncClient(timeout=120)
        self.total = spent()
        self.stop = False

    async def close(self):
        await self.http.aclose()

    async def chat(self, model: str, messages: list[dict], max_tokens: int, logger=None) -> tuple[str | None, float]:
        """One chat completion with 3 retries (exponential backoff); no retry on 402 / quota errors."""
        if self.stop:
            raise QuotaError("stopped")
        if self.total >= HARD_STOP_USD:
            raise BudgetExceeded(f"artifact spend {self.total:.3f} >= {HARD_STOP_USD}")
        body = {"model": model, "messages": messages, "temperature": 0, "max_tokens": max_tokens,
                "usage": {"include": True}}
        async with self.sem:
            for attempt in range(4):
                try:
                    r = await self.http.post(f"{self.base}/chat/completions", json=body,
                                             headers={"Authorization": f"Bearer {self.key}"})
                except httpx.HTTPError as e:
                    if logger:
                        logger.warning(f"{model} http error {type(e).__name__} attempt {attempt}")
                    await asyncio.sleep(2 ** attempt)
                    continue
                if r.status_code == 402 or (r.status_code == 403 and "limit" in r.text.lower()):
                    self.stop = True
                    raise QuotaError(f"{r.status_code}: {r.text[:200]}")
                if r.status_code != 200:
                    if logger:
                        logger.warning(f"{model} status {r.status_code}: {r.text[:200]} attempt {attempt}")
                    await asyncio.sleep(2 ** attempt)
                    continue
                d = r.json()
                if "error" in d:
                    if logger:
                        logger.warning(f"{model} error body {str(d['error'])[:200]}")
                    await asyncio.sleep(2 ** attempt)
                    continue
                usage = d.get("usage") or {}
                usd = float(usage.get("cost") or 0.0)
                async with _lock:
                    self.total += usd
                    with LEDGER.open("a") as fh:
                        fh.write(json.dumps({"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "phase": self.phase,
                                             "model": model, "usd": usd, "prompt_tokens": usage.get("prompt_tokens"),
                                             "completion_tokens": usage.get("completion_tokens"),
                                             "cum_usd": round(self.total, 6)}) + "\n")
                txt = (d.get("choices") or [{}])[0].get("message", {}).get("content")
                if logger:
                    logger.debug(f"{model} -> {str(txt)[:300]}")
                return txt, usd
        return None, 0.0


def parse_verdicts(txt: str | None, n: int) -> dict | None:
    if not txt:
        return None
    m = re.search(r"\{.*\}", txt, re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    out = {}
    for i in range(1, n + 1):
        v = str(d.get(str(i), "")).strip().upper()
        if v not in ("YES", "NO"):
            return None
        out[i] = v
    return out


def build_messages(prompt: dict, sentence: str, pairs: list[tuple[str, str]]) -> list[dict]:
    items = "\n".join(prompt["item_template"].format(n=i + 1, use=u, meaning=m) for i, (u, m) in enumerate(pairs))
    return [{"role": "system", "content": prompt["system"]},
            {"role": "user", "content": prompt["user_template"].format(sentence=sentence, items=items)}]


async def rate_pairs(client: Client, jobs: list[dict], version: str = "gloss_v1", logger=None) -> dict:
    """jobs: [{'sentence_id', 'sentence', 'pairs': [(use, meaning), ...]}]. Returns {(checker, sid, use, meaning): verdict}
    with verdict YES / NO / NO_VERDICT, using and extending the cache."""
    prompt = load_prompt(version)
    cache = load_cache()
    out = {}
    calls = []
    for j in jobs:
        for ck in CHECKERS:
            todo = []
            for (u, m) in j["pairs"]:
                k = cache_key(ck, version, j["sentence_id"], u, m)
                if k in cache:
                    out[(ck, j["sentence_id"], u, m)] = cache[k]
                else:
                    todo.append((u, m))
            todo = sorted(set(todo))
            random.Random(sha1(j["sentence_id"] + ck)).shuffle(todo)
            for i in range(0, len(todo), prompt["max_items_per_call"]):
                calls.append((ck, j, todo[i:i + prompt["max_items_per_call"]]))

    async def one(ck, j, chunk):
        msgs = build_messages(prompt, j["sentence"], chunk)
        v = None
        for _ask in range(2):  # one re-ask on unparseable JSON
            txt, _ = await client.chat(CHECKERS[ck], msgs, prompt["max_tokens"], logger)
            v = parse_verdicts(txt, len(chunk))
            if v is not None:
                break
        rec = []
        for i, (u, m) in enumerate(chunk):
            verdict = v[i + 1] if v else "NO_VERDICT"
            out[(ck, j["sentence_id"], u, m)] = verdict
            rec.append({"key": cache_key(ck, version, j["sentence_id"], u, m), "checker": ck, "version": version,
                        "sentence_id": j["sentence_id"], "use": u, "meaning": m, "verdict": verdict})
        async with _lock:
            with CACHE.open("a") as fh:
                for r in rec:
                    fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    if logger:
        logger.info(f"rate_pairs: {len(calls)} calls needed ({sum(len(c[2]) for c in calls)} pair-verdicts), "
                    f"artifact spend so far ${client.total:.3f}")
    res = await asyncio.gather(*[one(*c) for c in calls], return_exceptions=True)
    errs = [r for r in res if isinstance(r, Exception)]
    if errs and logger:
        logger.error(f"{len(errs)} calls failed; first: {type(errs[0]).__name__}: {errs[0]}")
    return out


def estimate_cost(n_pairs: int, prices: dict, per_call_in: int = 520, per_call_out: int = 75, per_call: int = 12) -> float:
    calls = -(-n_pairs // per_call)
    return sum(calls * (per_call_in * p["prompt"] + per_call_out * p["completion"]) for p in prices.values())


def live_prices() -> dict:
    snap = json.loads((ROOT / "work/models_snapshot.json").read_text())
    by = {m["id"]: m["pricing"] for m in snap}
    return {ck: {"prompt": float(by[m]["prompt"]), "completion": float(by[m]["completion"])} for ck, m in CHECKERS.items()}
