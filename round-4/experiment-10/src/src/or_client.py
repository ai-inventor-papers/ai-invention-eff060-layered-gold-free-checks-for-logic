"""Async OpenRouter client with a content-addressed JSONL cache and the budget ledger.

Cache: data/csc_llm_cache.jsonl, key = sha1(namespace | model | json(messages) | json(params)); a hit costs $0.
Calls: POST {OPENROUTER_BASE_URL}/chat/completions with {model, messages, temperature 0, max_tokens 400,
usage: {include: true}, **extra}. At most 3 retries with exponential backoff on 429 / 5xx / timeouts / network
errors; a call that still fails is recorded as status 'API_FAIL' (content None) and never retried in a loop.
A 402 / 'limit' answer raises KeyLimit so the caller can stop cleanly (the pre-declared outage fallback).
The key is read from the environment and never printed or stored.
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
import time
from pathlib import Path

import aiohttp
from loguru import logger

import csc_budget as budget

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "csc_llm_cache.jsonl"
PER_MODEL_CONCURRENCY = 12
MAX_RETRIES = 3


class KeyLimit(RuntimeError):
    pass


def cache_key(model: str, messages: list[dict], params: dict, namespace: str = "") -> str:
    blob = namespace + "|" + model + "|" + json.dumps(messages, ensure_ascii=False, sort_keys=True) + "|" + \
        json.dumps(params, sort_keys=True)
    return hashlib.sha1(blob.encode()).hexdigest()


class Cache:
    """In-memory view of the append-only JSONL cache (last record per key wins; API_FAIL records are not hits)."""

    def __init__(self, path: Path = CACHE):
        self.path = path
        self.d: dict[str, dict] = {}
        if path.exists():
            for line in path.read_text().splitlines():
                if not line.strip():
                    continue
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                self.d[r["key"]] = r

    def get(self, k: str) -> dict | None:
        r = self.d.get(k)
        return r if (r is not None and r.get("status") == "ok") else None

    def put(self, rec: dict) -> None:
        self.d[rec["key"]] = rec
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


class Client:
    def __init__(self, stage: str, cache: Cache | None = None, max_tokens: int = 400, timeout_s: int = 90):
        self.stage = stage
        self.cache = cache or Cache()
        self.max_tokens = max_tokens
        self.timeout = aiohttp.ClientTimeout(total=timeout_s)
        self.sems: dict[str, asyncio.Semaphore] = {}
        self.base = os.environ["OPENROUTER_BASE_URL"].rstrip("/")
        self.key_dead = False
        self.n_calls = 0
        self.n_hits = 0

    def _sem(self, model: str) -> asyncio.Semaphore:
        if model not in self.sems:
            self.sems[model] = asyncio.Semaphore(PER_MODEL_CONCURRENCY)
        return self.sems[model]

    async def chat(self, session: aiohttp.ClientSession, model: str, messages: list[dict], extra: dict | None = None,
                   namespace: str = "", meta: dict | None = None) -> dict:
        """-> cache record {key, model, namespace, content, cost_usd, prompt_tokens, completion_tokens, latency_s, status}."""
        params = {"temperature": 0.0, "max_tokens": self.max_tokens, **(extra or {})}
        k = cache_key(model, messages, params, namespace)
        hit = self.cache.get(k)
        if hit is not None:
            self.n_hits += 1
            return {**hit, "cache_hit": True}
        if self.key_dead:
            return {"key": k, "model": model, "status": "API_FAIL", "content": None, "cost_usd": 0.0, "err": "key_dead"}
        async with self._sem(model):
            hit = self.cache.get(k)
            if hit is not None:
                self.n_hits += 1
                return {**hit, "cache_hit": True}
            budget.check(0.003)
            body = {"model": model, "messages": messages, "usage": {"include": True}, **params}
            headers = {"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}", "Content-Type": "application/json"}
            err = None
            for attempt in range(MAX_RETRIES + 1):
                t0 = time.time()
                try:
                    async with session.post(self.base + "/chat/completions", json=body, headers=headers,
                                            timeout=self.timeout) as r:
                        status = r.status
                        txt = await r.text()
                    lat = time.time() - t0
                    if status == 402 or (status == 429 and "limit" in txt.lower() and "rate" not in txt.lower()):
                        self.key_dead = True
                        budget.record(stage=self.stage, model=model, prompt_tokens=None, completion_tokens=None,
                                      cost_usd=0.0, latency_s=lat, status=f"KEY_LIMIT_{status}")
                        raise KeyLimit(f"{status}: {txt[:160]}")
                    if status == 429 or status >= 500:
                        err = f"http {status}: {txt[:120]}"
                        await asyncio.sleep(2 ** attempt + 0.5)
                        continue
                    d = json.loads(txt)
                    if "choices" not in d:
                        err = f"no choices: {txt[:160]}"
                        if "limit" in txt.lower() and ("key" in txt.lower() or "credit" in txt.lower()):
                            self.key_dead = True
                            raise KeyLimit(err)
                        await asyncio.sleep(2 ** attempt + 0.5)
                        continue
                    u = d.get("usage") or {}
                    cost = float(u.get("cost") or 0.0)
                    content = (d["choices"][0].get("message") or {}).get("content") or ""
                    budget.record(stage=self.stage, model=model, prompt_tokens=u.get("prompt_tokens"),
                                  completion_tokens=u.get("completion_tokens"), cost_usd=cost, latency_s=lat)
                    rec = {"key": k, "model": model, "namespace": namespace, "content": content, "cost_usd": cost,
                           "prompt_tokens": u.get("prompt_tokens"), "completion_tokens": u.get("completion_tokens"),
                           "latency_s": round(lat, 3), "status": "ok", "ts": round(time.time(), 1),
                           "provider": d.get("provider"), "meta": meta or {}}
                    self.cache.put(rec)
                    self.n_calls += 1
                    logger.debug(f"[{self.stage}] {model} ${cost:.6f} {lat:.1f}s -> {content[:160]!r}")
                    return {**rec, "cache_hit": False}
                except (aiohttp.ClientError, asyncio.TimeoutError, json.JSONDecodeError) as ex:
                    err = f"{type(ex).__name__}: {str(ex)[:120]}"
                    await asyncio.sleep(2 ** attempt + 0.5)
            logger.warning(f"[{self.stage}] API_FAIL {model}: {err}")
            budget.record(stage=self.stage, model=model, prompt_tokens=None, completion_tokens=None, cost_usd=0.0,
                          latency_s=0.0, status="API_FAIL")
            return {"key": k, "model": model, "status": "API_FAIL", "content": None, "cost_usd": 0.0, "err": err}


async def probe(model: str = "openai/gpt-4.1-mini") -> tuple[bool, str]:
    """1-token probe; returns (ok, message). Not cached."""
    base = os.environ["OPENROUTER_BASE_URL"].rstrip("/")
    headers = {"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"}
    body = {"model": model, "messages": [{"role": "user", "content": "Say OK."}], "max_tokens": 1, "temperature": 0,
            "usage": {"include": True}}
    t0 = time.time()
    async with aiohttp.ClientSession() as s:
        async with s.post(base + "/chat/completions", json=body, headers=headers,
                          timeout=aiohttp.ClientTimeout(total=60)) as r:
            txt = await r.text()
            st = r.status
    ok = st == 200 and "choices" in txt
    cost = 0.0
    if ok:
        cost = float((json.loads(txt).get("usage") or {}).get("cost") or 0.0)
    budget.record(stage="probe", model=model, prompt_tokens=None, completion_tokens=None, cost_usd=cost,
                  latency_s=time.time() - t0, status="ok" if ok else f"http_{st}")
    return ok, f"http {st} {'ok' if ok else txt[:200]}"
