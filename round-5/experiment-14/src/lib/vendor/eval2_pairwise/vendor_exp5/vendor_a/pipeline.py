"""Scoring pipeline (STAGES 3-6). Scoring code NEVER reads track-L labels: it consumes `scoring_view()` items only.

cpu_layers(text, fol)  -> L1 lint, L2-bow, L2-role, exact z3 formula profile (+ seconds per layer); cached per (text, fol)
LLM stages             -> L3 questionnaire (primary, retest, 2nd model), decomposed judge, disguised questionnaire
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import math
import multiprocessing as mp
import os
import signal
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from loguru import logger

sys.setrecursionlimit(10000)
SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
CACHE = ROOT / "cache"
LABEL_KEYS = ("label", "auto_class", "repair_ops")


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()


def scoring_view(items: list[dict]) -> list[dict]:
    """Items stripped of every label field; asserts the keys are absent (scoring code can only see this view)."""
    out = [{k: v for k, v in x.items() if k not in LABEL_KEYS} for x in items]
    for x in out:
        assert not any(k in x for k in LABEL_KEYS)
    return out


# ------------------------------------------------------------------------------------------------ CPU layers
class _TO(Exception):
    pass


def _alarm(signum, frame):  # noqa: ARG001
    raise _TO()


def prof_to_json(p: dict) -> dict:
    return {k: {**v, "slots": [list(s) for s in v["slots"]]} for k, v in p.items()}


def prof_from_json(p: dict | None) -> dict | None:
    if p is None:
        return None
    return {k: {**v, "slots": [tuple(s) for s in v["slots"]]} for k, v in p.items()}


def cpu_layers_job(args: tuple) -> dict:
    key, text, fol, hard_s = args
    sys.path.insert(0, str(SRC))
    from fol import parse
    from fol_triage import fol_lint, content_accounting, role_accounting, formula_role_profile
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(hard_s)
    out = {"key": key, "parse_ok": True, "status": "OK", "secs": {}}
    try:
        try:
            e = parse(fol)
        except Exception as ex:  # noqa: BLE001
            out.update(parse_ok=False, status="UNPARSEABLE", err=str(ex)[:120])
            return out
        t = time.time(); out["l1"] = fol_lint(e); out["secs"]["l1"] = round(time.time() - t, 3)
        t = time.time()
        try:
            out["bow"] = content_accounting(text, e)
        except Exception as ex:  # noqa: BLE001
            out["bow"] = None; out["bow_err"] = str(ex)[:120]
        out["secs"]["bow"] = round(time.time() - t, 3)
        t = time.time(); prof = formula_role_profile(e); out["profile"] = prof_to_json(prof)
        out["secs"]["profile"] = round(time.time() - t, 3)
        t = time.time()
        try:
            ra = role_accounting(text, e, prof)
            out["role"] = {k: v for k, v in ra.items()}
        except Exception as ex:  # noqa: BLE001
            out["role"] = None; out["role_err"] = str(ex)[:120]
        out["secs"]["role"] = round(time.time() - t, 3)
    except _TO:
        out["status"] = "CPU_TIMEOUT"
    except RecursionError:
        out["status"] = "CPU_RECURSION"
    finally:
        signal.alarm(0)
    return out


def _init_worker():
    os.environ["PYTHONHASHSEED"] = "0"


def run_cpu_layers(pairs: list[tuple[str, str]], workers: int = 4, hard_s: int = 120) -> dict:
    """pairs [(text, fol)] -> {sha1(text|fol): result}. Cached in cache/cpu_layers.jsonl."""
    cp = CACHE / "cpu_layers.jsonl"
    cache = {}
    if cp.exists():
        for l in cp.read_text().splitlines():
            if l.strip():
                r = json.loads(l); cache[r["key"]] = r
    todo = {}
    for t, f in pairs:
        k = sha1(f"{t}|{f}")
        if k not in cache and k not in todo:
            todo[k] = (k, t, f, hard_s)
    logger.info(f"cpu_layers: {len(set(pairs))} unique pairs, {len(todo)} uncached")
    if todo:
        t0 = time.time()
        with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn"),
                                 initializer=_init_worker) as pool, cp.open("a") as fh:
            futs = [pool.submit(cpu_layers_job, a) for a in todo.values()]
            for i, fu in enumerate(as_completed(futs)):
                r = fu.result()
                cache[r["key"]] = r
                fh.write(json.dumps(r, ensure_ascii=False) + "\n"); fh.flush()
                if (i + 1) % 100 == 0:
                    logger.info(f"  cpu_layers {i + 1}/{len(todo)} ({time.time() - t0:.0f}s)")
    return {sha1(f"{t}|{f}"): cache[sha1(f"{t}|{f}")] for t, f in pairs}


def profile_job(args):
    key, fol = args
    sys.path.insert(0, str(SRC))
    from fol_triage import formula_role_profile
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(90)
    try:
        return {"key": key, "profile": prof_to_json(formula_role_profile(fol))}
    except Exception as ex:  # noqa: BLE001
        return {"key": key, "profile": None, "err": str(ex)[:100]}
    finally:
        signal.alarm(0)


def run_profiles(fols: list[str], workers: int = 4) -> dict:
    cp = CACHE / "profiles_extra.jsonl"
    cache = {}
    if cp.exists():
        for l in cp.read_text().splitlines():
            if l.strip():
                r = json.loads(l); cache[r["key"]] = r
    todo = {sha1(f): (sha1(f), f) for f in fols if sha1(f) not in cache}
    if todo:
        with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn"),
                                 initializer=_init_worker) as pool, cp.open("a") as fh:
            for fu in as_completed([pool.submit(profile_job, a) for a in todo.values()]):
                r = fu.result(); cache[r["key"]] = r
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    return {f: prof_from_json(cache[sha1(f)]["profile"]) for f in fols}


# ------------------------------------------------------------------------------------------------ LLM stages
def _client(model: str = ""):
    """Live OpenRouter client unless LLM_LIVE=0 or the model is local (local answers are read from the cache only)."""
    from llm import LLM, CachedLLM
    if model.startswith("local/") or os.environ.get("LLM_LIVE", "1") == "0":
        return CachedLLM()
    return LLM()


async def run_questionnaires(texts: list[str], model: str, tag: str = "L3", system: str | None = None) -> dict:
    from llm import StopBudget, CacheMiss
    from fol_triage import role_questionnaire
    out = {}
    async with _client(model) as llm:
        async def one(t):
            try:
                out[t] = await role_questionnaire(t, llm, model, tag=tag, system=system)
            except CacheMiss as ex:
                out[t] = {"q": None, "coverage_status": "L3_MISSING", "cost_usd": 0.0, "secs": 0.0, "err": str(ex)}
            except StopBudget as ex:
                out[t] = {"q": None, "coverage_status": "BUDGET_STOP", "cost_usd": 0.0, "secs": 0.0, "err": str(ex)}
            except RuntimeError as ex:
                out[t] = {"q": None, "coverage_status": "L3_FAIL", "cost_usd": 0.0, "secs": 0.0, "err": str(ex)[:200]}
        await asyncio.gather(*[one(t) for t in dict.fromkeys(texts)])
        logger.info(f"questionnaires[{model} {tag}]: {len(out)} texts, new calls {llm.n_calls}, ledger ${llm.spent:.4f}")
    return out


async def run_decomposed(pairs: list[tuple[str, str]], model: str) -> dict:
    from llm import StopBudget, CacheMiss
    from fol_triage import decomposed_profile
    out = {}
    async with _client(model) as llm:
        async def one(t, f):
            try:
                out[(t, f)] = await decomposed_profile(t, f, llm, model)
            except CacheMiss as ex:
                out[(t, f)] = {"profile": None, "status": "DJ_MISSING", "cost_usd": 0.0, "err": str(ex)}
            except StopBudget as ex:
                out[(t, f)] = {"profile": None, "status": "BUDGET_STOP", "cost_usd": 0.0, "err": str(ex)}
            except Exception as ex:  # noqa: BLE001
                out[(t, f)] = {"profile": None, "status": "DJ_FAIL", "cost_usd": 0.0, "err": str(ex)[:200]}
        await asyncio.gather(*[one(t, f) for t, f in dict.fromkeys(pairs)])
        logger.info(f"decomposed[{model}]: {len(out)} pairs, new calls {llm.n_calls}, ledger ${llm.spent:.4f}")
    return out


def ledger_total() -> float:
    p = CACHE / "cost_ledger.jsonl"
    if not p.exists():
        return 0.0
    return sum(json.loads(l)["cost_usd"] for l in p.read_text().splitlines() if l.strip())


def safe_log_words(text: str) -> float:
    return math.log(max(1, len(text.split())))
