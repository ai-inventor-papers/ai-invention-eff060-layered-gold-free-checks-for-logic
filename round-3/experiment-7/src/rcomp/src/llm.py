"""Resumable batched LLM calls on top of dataset E's or_client (cost ledger + phase caps + hard cap).

run_jobs(phase, cap, model, jobs, cache_path, ...) sends every job whose key is not yet in cache_path, in the given
(priority) order, appending {key, model, text, parsed, cost_usd, error} per call. Key-limit failures are not cached,
so a re-run retries them. Jobs are processed in waves of `concurrency` so the order is preserved under a cap cut.
"""
from __future__ import annotations

import asyncio
import json
import re

from common import append_jsonl, load_jsonl
from or_client import BudgetExceeded, Client  # E's client (src_e/or_client.py)

ANTHROPIC_NO_THINK = {"reasoning": {"enabled": False}}


def parse_json(text: str | None):
    if not text:
        return None
    t = text.strip()
    m = re.search(r"```(?:json)?\s*(.*?)```", t, re.S)
    if m:
        t = m.group(1).strip()
    for opener, closer in (("{", "}"), ("[", "]")):
        i, j = t.find(opener), t.rfind(closer)
        if i != -1 and j > i:
            try:
                return json.loads(t[i:j + 1])
            except json.JSONDecodeError:
                continue
    return None


def salvage_objects(text: str | None, list_key: str):
    """Recover the complete flat objects of a truncated {list_key: [ {...}, ... ]} JSON answer."""
    if not text:
        return None
    objs = []
    for m in re.finditer(r"\{[^{}]*\}", text):
        try:
            objs.append(json.loads(m.group(0)))
        except json.JSONDecodeError:
            continue
    return {list_key: objs, "salvaged": True} if objs else None


def cached(cache_path) -> dict:
    out = {}
    for r in load_jsonl(cache_path):
        if r.get("parsed") is not None:
            out[r["key"]] = r
    return out


async def _run(phase, cap, model, jobs, cache_path, concurrency, params, validate, logger, salvage_key=None):
    done = cached(cache_path)
    todo = [j for j in jobs if j["key"] not in done]
    logger.info(f"[{phase}] {len(jobs)} jobs, {len(todo)} to run, model {model}")
    stop = False
    async with Client(phase, phase_cap=cap, concurrency=concurrency, timeout=240) as client:
        async def one(j, attempt=0):
            r = await client.chat(model, j["messages"], tag=f"{phase}:{j['key']}", retries=3, **params)
            parsed = parse_json(r["text"])
            if parsed is None and salvage_key and r.get("finish_reason") == "length":
                parsed = salvage_objects(r["text"], salvage_key)  # truncated: keep complete objects, no retry
            if parsed is not None and validate is not None and not validate(j, parsed):
                parsed = None
            if parsed is None and r["text"] is not None and attempt == 0:
                rec0 = {"key": j["key"], "model": model, "text": r["text"], "parsed": None, "cost_usd": r["cost_usd"],
                        "error": "parse_fail_retry", "attempt": 0}
                append_jsonl(cache_path, rec0)
                return await one(j, 1)
            rec = {"key": j["key"], "model": model, "text": r["text"], "parsed": parsed, "cost_usd": r["cost_usd"],
                   "error": r["error"], "attempt": attempt, "usage": r["usage"]}
            if r["text"] is None and "Key limit exceeded" in (r["error"] or ""):
                logger.error(f"KEY LIMIT: {r['error'][:200]}")
                return "KEYLIMIT"
            append_jsonl(cache_path, rec)
            return rec
        for i in range(0, len(todo), concurrency):
            wave = todo[i:i + concurrency]
            res = await asyncio.gather(*[one(j) for j in wave], return_exceptions=True)
            for x in res:
                if isinstance(x, BudgetExceeded):
                    logger.error(f"[{phase}] budget stop: {x}"); stop = stop or "CAP"
                elif isinstance(x, Exception):
                    logger.error(f"[{phase}] job error {type(x).__name__}: {x}")
                elif x == "KEYLIMIT":
                    stop = "KEYLIMIT"
            if stop:
                break
            logger.info(f"[{phase}] {min(i + concurrency, len(todo))}/{len(todo)} phase ${client.spent_phase:.4f} "
                        f"total ${client.spent_total:.4f}")
    return cached(cache_path), stop


def run_jobs(phase, cap, model, jobs, cache_path, logger, concurrency=8, params=None, validate=None, salvage_key=None):
    return asyncio.run(_run(phase, cap, model, jobs, cache_path, concurrency, params or {}, validate, logger, salvage_key))
