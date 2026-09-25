"""Async OpenRouter client with a persistent JSON response cache and a cumulative cost ledger.

Every call is cached in cache/llm_cache.jsonl keyed by sha1(model|system|user|temperature|tag) so re-runs cost $0.
Cost is taken from the response usage.cost (OpenRouter usage accounting) or, failing that, tokens x catalog price.
StopBudget is raised once the cumulative ledger (cache/cost_ledger.jsonl) exceeds HARD_STOP_USD.
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

ROOT = Path(__file__).resolve().parent.parent
CACHE_P = ROOT / "cache" / "llm_cache.jsonl"
LEDGER_P = ROOT / "cache" / "cost_ledger.jsonl"
HARD_STOP_USD = 8.0
PRICES = {  # $/M tokens (in, out), OpenRouter catalog 2026-09-23
    "google/gemini-2.5-flash-lite": (0.10, 0.40),
    "qwen/qwen3-30b-a3b-instruct-2507": (0.0481, 0.193),
    "meta-llama/llama-3.3-70b-instruct": (0.10, 0.32),
}
URL = "https://openrouter.ai/api/v1/chat/completions"


class StopBudget(Exception):
    pass


class LLM:
    def __init__(self, concurrency: int = 16):
        self.sem = asyncio.Semaphore(concurrency)
        self.cache: dict[str, dict] = {}
        CACHE_P.parent.mkdir(exist_ok=True)
        if CACHE_P.exists():
            for l in CACHE_P.read_text().splitlines():
                if l.strip():
                    r = json.loads(l)
                    self.cache[r["key"]] = r
        self.spent = 0.0
        if LEDGER_P.exists():
            for l in LEDGER_P.read_text().splitlines():
                if l.strip():
                    self.spent += json.loads(l)["cost_usd"]
        self.key = os.environ["OPENROUTER_API_KEY"]
        self.session: aiohttp.ClientSession | None = None
        self.n_calls = 0
        logger.info(f"LLM: {len(self.cache)} cached responses, ledger spent so far ${self.spent:.4f}")

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=120))
        return self

    async def __aexit__(self, *a):
        await self.session.close()

    @staticmethod
    def ckey(model, system, user, temperature, tag):
        return hashlib.sha1(f"{model}|{system}|{user}|{temperature}|{tag}".encode()).hexdigest()

    def cached(self, model, system, user, temperature=0.0, tag=""):
        return self.cache.get(self.ckey(model, system, user, temperature, tag))

    async def chat_json(self, model: str, system: str, user: str, *, temperature: float = 0.0, max_tokens: int = 700,
                        tag: str = "", schema: dict | None = None) -> dict:
        """-> {'text', 'cost_usd', 'secs', 'in_tok', 'out_tok', 'cached'}; raises StopBudget / RuntimeError."""
        k = self.ckey(model, system, user, temperature, tag)
        if k in self.cache:
            r = dict(self.cache[k]); r["cached"] = True
            return r
        if self.spent > HARD_STOP_USD:
            raise StopBudget(f"spent ${self.spent:.3f} > ${HARD_STOP_USD}")
        body = {"model": model, "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
                "temperature": temperature, "max_tokens": max_tokens, "response_format": {"type": "json_object"},
                "usage": {"include": True}}
        if model.startswith("google/"):
            body["reasoning"] = {"max_tokens": 0}  # no hidden thinking on flash-lite
        hdr = {"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"}
        last = None
        for attempt in range(5):
            async with self.sem:
                t0 = time.time()
                try:
                    async with self.session.post(URL, json=body, headers=hdr) as resp:
                        js = await resp.json(content_type=None)
                        if resp.status != 200 or "choices" not in js:
                            raise RuntimeError(f"HTTP {resp.status}: {str(js)[:300]}")
                except (aiohttp.ClientError, asyncio.TimeoutError, RuntimeError, json.JSONDecodeError) as ex:
                    last = ex
                    logger.warning(f"LLM attempt {attempt} failed ({model}): {str(ex)[:200]}")
                    await asyncio.sleep(2 ** attempt)
                    continue
            dt = time.time() - t0
            u = js.get("usage", {}) or {}
            pin, pout = PRICES.get(model, (1.0, 5.0))
            cost = u.get("cost")
            if cost is None:
                cost = (u.get("prompt_tokens", 0) * pin + u.get("completion_tokens", 0) * pout) / 1e6
            text = js["choices"][0]["message"].get("content") or ""
            rec = {"key": k, "model": model, "tag": tag, "text": text, "cost_usd": float(cost), "secs": round(dt, 2),
                   "in_tok": u.get("prompt_tokens", 0), "out_tok": u.get("completion_tokens", 0)}
            self.cache[k] = rec
            self.spent += float(cost)
            self.n_calls += 1
            with CACHE_P.open("a") as fh:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            with LEDGER_P.open("a") as fh:
                fh.write(json.dumps({"ts": time.time(), "model": model, "tag": tag, "cost_usd": float(cost)}) + "\n")
            led = os.environ.get("AII_COST_LEDGER")
            if led:
                try:
                    with open(led, "a") as fh:
                        fh.write(json.dumps({"ts": time.time(), "tool": "openrouter_fol_triage", "cost_usd": float(cost),
                                             "model": model}) + "\n")
                except OSError:
                    pass
            logger.debug(f"LLM {model} tag={tag} ${cost:.5f} {dt:.1f}s in={rec['in_tok']} out={rec['out_tok']} "
                         f"| {user[:120]!r} -> {text[:200]!r}")
            r = dict(rec); r["cached"] = False
            return r
        raise RuntimeError(f"LLM failed after retries: {last}")


# ================================================================================================ local fallback
LOCAL_MODELS = {
    "local/qwen2.5-1.5b-instruct-q4_k_m": ("Qwen/Qwen2.5-1.5B-Instruct-GGUF", "qwen2.5-1.5b-instruct-q4_k_m.gguf"),
    "local/qwen2.5-3b-instruct-q4_k_m": ("Qwen/Qwen2.5-3B-Instruct-GGUF", "qwen2.5-3b-instruct-q4_k_m.gguf"),
}


class CacheMiss(Exception):
    pass


class CachedLLM:
    """Read-only view of the response cache (used by method.py once OpenRouter is unavailable / local runs finished).
    Same chat_json interface; a miss raises CacheMiss (the caller records a coverage failure)."""

    def __init__(self):
        self.cache = {}
        if CACHE_P.exists():
            for l in CACHE_P.read_text().splitlines():
                if l.strip():
                    try:
                        r = json.loads(l)
                    except json.JSONDecodeError:
                        continue  # a partially written last line from a concurrent writer
                    self.cache[r["key"]] = r
        self.spent = sum(json.loads(l)["cost_usd"] for l in LEDGER_P.read_text().splitlines() if l.strip()) \
            if LEDGER_P.exists() else 0.0
        self.n_calls = 0

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return None

    async def chat_json(self, model, system, user, *, temperature=0.0, max_tokens=700, tag="", schema=None):
        k = LLM.ckey(model, system, user, temperature, tag)
        if k not in self.cache:
            raise CacheMiss(f"{model} {tag}")
        r = dict(self.cache[k]); r["cached"] = True
        return r


class LocalLLM:
    """llama.cpp CPU fallback (OpenRouter key hit its daily limit). Deterministic at temperature 0; JSON-schema grammar
    constrains the output to the frozen schema. Retries (tag '#1', '#2') sample at temperature 0.3 with a fixed seed."""

    def __init__(self, model: str, n_threads: int = 4):
        from huggingface_hub import hf_hub_download
        from llama_cpp import Llama, LlamaRAMCache
        self.model = model
        self.llm = Llama(model_path=hf_hub_download(*LOCAL_MODELS[model]), n_ctx=4096, n_threads=n_threads,
                         verbose=False, seed=0)
        self.llm.set_cache(LlamaRAMCache(capacity_bytes=2 << 30))
        self.cache = {}
        if CACHE_P.exists():
            for l in CACHE_P.read_text().splitlines():
                if l.strip():
                    try:
                        r = json.loads(l); self.cache[r["key"]] = r
                    except json.JSONDecodeError:
                        continue
        self.n_calls = 0
        self.spent = 0.0

    def chat_json_sync(self, system, user, *, temperature=0.0, max_tokens=700, tag="", schema=None):
        k = LLM.ckey(self.model, system, user, temperature, tag)
        if k in self.cache:
            r = dict(self.cache[k]); r["cached"] = True
            return r
        temp = temperature if not tag.endswith(("#1", "#2")) else 0.3
        t0 = time.time()
        rf = {"type": "json_object", "schema": schema} if schema else {"type": "json_object"}
        out = self.llm.create_chat_completion(messages=[{"role": "system", "content": system},
                                                        {"role": "user", "content": user}],
                                              temperature=temp, max_tokens=max_tokens, response_format=rf,
                                              seed=int(tag[-1]) if tag[-1:].isdigit() else 0)
        u = out.get("usage", {})
        rec = {"key": k, "model": self.model, "tag": tag, "text": out["choices"][0]["message"]["content"] or "",
               "cost_usd": 0.0, "secs": round(time.time() - t0, 2), "in_tok": u.get("prompt_tokens", 0),
               "out_tok": u.get("completion_tokens", 0)}
        self.cache[k] = rec
        self.n_calls += 1
        with CACHE_P.open("a") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        r = dict(rec); r["cached"] = False
        return r

    async def __aenter__(self):
        return self

    async def __aexit__(self, *a):
        return None

    async def chat_json(self, model, system, user, *, temperature=0.0, max_tokens=700, tag="", schema=None):
        return self.chat_json_sync(system, user, temperature=temperature, max_tokens=max_tokens, tag=tag, schema=schema)
