#!/usr/bin/env python3
"""E2-A label-free consensus scoring with the FROZEN iteration-2 exp-5 code (frozen/exp5/src, byte-identical copies).

  l3        L3 role questionnaire (exp-A role_questionnaire, flash-lite, TEXT ONLY) for every E2 sentence -> cache/E2_l3_q.jsonl
  score     exp-5 pool_scoring.score_sentence per sentence (peers = the other LLM slots of the same sentence, leave-own-
            vendor-family-out, frozen family_map_vendor) -> cache/consensus_sentences.jsonl
              c_score_align = 1 - share of family-disjoint parseable peers eqmv-equivalent to the candidate (V0, PRIMARY)
              ALIGN:g_score (graded consensus), l2_bow, l3_z3 (TEXT side) -> p_peer_text (frozen fusion), n_peers_used
  pairwise  eval-2 pairwise_matrix per sentence (all eqmv pairs among parseable outputs; H-MECH and variants V1-V5)
            -> cache/pairwise_E2.jsonl
  exact     c_exact: the same consensus with z3 equivalence on IDENTICAL symbol names (no aligner) -> cache/exact_E2.jsonl

Parameters: exp-5 prereg scoring_params, except variants = ['ALIGN'] (NF-anchored is a closed strand), k6_seeds = 0,
famfield = False, medoid_budget_s = 0. These switch off auxiliary readouts only; c_score_align, ALIGN:g_score, l2_bow and
l3_z3 are computed by the unchanged code path (checked by scoring/tests: reproduction of E rows).
Usage: env/.venv/bin/python scoring/score_consensus.py --stage l3|score|pairwise|exact [--workers 44]
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import scoring.guard  # noqa: E402,F401
from scoring.common import CACHE, FROZEN, append_jsonl, by_sentence, candidates, jl, setup_log  # noqa: E402

import argparse  # noqa: E402
import asyncio  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import multiprocessing as mp  # noqa: E402
import os  # noqa: E402
import time  # noqa: E402
from concurrent.futures import ProcessPoolExecutor, as_completed  # noqa: E402

from loguru import logger  # noqa: E402

EXP5 = FROZEN / "exp5" / "src"
os.environ.setdefault("NLTK_DATA", str(FROZEN / "nltk_data"))
PRE5 = json.loads((FROZEN / "exp5" / "results" / "prereg.json").read_text())
FAM = PRE5["family_map_vendor"]
L3P = CACHE / "E2_l3_q.jsonl"
JUDGE_MODEL = "google/gemini-2.5-flash-lite"


def params() -> dict:
    P = dict(PRE5["scoring_params"])
    P.update(variants=["ALIGN"], k6_seeds=0, famfield=False, medoid_budget_s=0)
    return P


def sentence_tasks() -> list[dict]:
    q = {r["text"]: r["q"] for r in jl(L3P) if r.get("coverage_status") == "OK"}
    out = []
    for sid, rs in by_sentence(candidates()).items():
        text = rs[0]["text"]
        out.append({"sentence_id": sid, "text": text, "q": q.get(text), "stratum": rs[0]["stratum"],
                    "rows": [{"key": r["row_key"], "fol": r["candidate_fol"], "family": FAM[r["slot"]],
                              "family_field": r.get("family_field") or FAM[r["slot"]], "system": r["system"], "is_peer": True}
                             for r in rs]})
    out.sort(key=lambda t: hashlib.sha1(("E2_v1|" + t["sentence_id"]).encode()).hexdigest())
    return out


# ------------------------------------------------------------------------------------------------------------ L3
async def _l3(texts: list[str]) -> None:
    sys.path.insert(0, str(EXP5))
    sys.path.insert(0, str(EXP5 / "vendor_a"))
    import peer_text  # noqa: F401  (binds the dataset-E parser as `fol` for the vendored modules)
    import llm as LA
    import fol_triage as FT
    LA.URL = os.environ["OPENROUTER_BASE_URL"].rstrip("/") + "/chat/completions"  # transport-only (as dataset-4 D0)
    LA.CACHE_P = CACHE / "l3_llm_cache.jsonl"
    LA.LEDGER_P = CACHE / "l3_cost_ledger.jsonl"
    LA.HARD_STOP_USD = 0.5
    have = {r["text"] for r in jl(L3P) if r.get("coverage_status") == "OK"}
    todo = [t for t in dict.fromkeys(texts) if t not in have]
    logger.info(f"L3: {len(todo)} texts to answer")
    async with LA.LLM(concurrency=24) as llm:
        async def one(t):
            try:
                r = await FT.role_questionnaire(t, llm, JUDGE_MODEL, tag="L3")
            except LA.StopBudget as ex:
                r = {"q": None, "coverage_status": "BUDGET_STOP", "cost_usd": 0.0, "secs": 0.0, "err": str(ex)}
            except RuntimeError as ex:
                r = {"q": None, "coverage_status": "L3_FAIL", "cost_usd": 0.0, "secs": 0.0, "err": str(ex)[:200]}
            return {"text": t, "cond": "orig", **r}
        res = await asyncio.gather(*[one(t) for t in todo])
    append_jsonl(L3P, res)
    logger.info(f"L3: ok {sum(r['coverage_status'] == 'OK' for r in res)}/{len(res)}; spent ${llm.spent:.4f}")


# --------------------------------------------------------------------------------------------------------- score
def _init(mem_gb: float = 4.0):
    sys.path.insert(0, str(EXP5))
    import scoring.guard  # noqa: F401
    import pool_scoring as PS
    PS.init_worker(mem_gb)


def _score_one(t: dict, P: dict) -> dict:
    import pool_scoring as PS
    return PS.score_sentence(t, P)


def stage_score(workers: int) -> None:
    outp = CACHE / "consensus_sentences.jsonl"
    done = {r["sentence_id"] for r in jl(outp)}
    T = [t for t in sentence_tasks() if t["sentence_id"] not in done]
    P = params()
    logger.info(f"score: {len(T)} sentences; params {P}; q present {sum(t['q'] is not None for t in T)}")
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn"), initializer=_init) as ex, \
            outp.open("a") as fh:
        futs = {ex.submit(_score_one, t, P): t for t in T}
        for i, fu in enumerate(as_completed(futs)):
            t = futs[fu]
            try:
                res = fu.result()
            except Exception as e:  # noqa: BLE001 - counted as coverage failure of every row of the sentence
                logger.error(f"sentence {t['sentence_id']} failed: {e}")
                res = {"sentence_id": t["sentence_id"], "rows": [{"key": r["key"], "coverage_status": "WORKER_FAIL"} for r in t["rows"]],
                       "stats": {"error": str(e)[:300]}}
            res["stratum"] = t["stratum"]
            fh.write(json.dumps(res, ensure_ascii=False) + "\n")
            fh.flush()
            if (i + 1) % 25 == 0:
                logger.info(f"score {i + 1}/{len(T)} {time.time() - t0:.0f}s")
    logger.info(f"score done in {time.time() - t0:.0f}s")


# ------------------------------------------------------------------------------------------------------ pairwise
def _init_pw():
    sys.path.insert(0, str(FROZEN / "eval2" / "src"))
    import scoring.guard  # noqa: F401
    import pairwise
    pairwise.init_worker(4.0)


def _pw_one(t: dict) -> dict:
    import pairwise
    t0 = time.time()
    rows = [{"row_key": r["key"], "fol": r["fol"], "slot": r["slot"], "family": r["family"], "family_field": r["family_field"],
             "system_class": "llm"} for r in t["rows"]]
    m = pairwise.pairwise_matrix(rows)
    m["sentence_id"] = t["sentence_id"]
    m["secs"] = round(time.time() - t0, 2)
    return m


def stage_pairwise(workers: int) -> None:
    outp = CACHE / "pairwise_E2.jsonl"
    done = {r["sentence_id"] for r in jl(outp)}
    cand = by_sentence(candidates())
    T = []
    for t in sentence_tasks():
        if t["sentence_id"] in done:
            continue
        slot_of = {r["row_key"]: r["slot"] for r in cand[t["sentence_id"]]}
        for r in t["rows"]:
            r["slot"] = slot_of[r["key"]]
        T.append(t)
    logger.info(f"pairwise: {len(T)} sentences")
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn"), initializer=_init_pw) as ex, \
            outp.open("a") as fh:
        futs = {ex.submit(_pw_one, t): t for t in T}
        for i, fu in enumerate(as_completed(futs)):
            try:
                res = fu.result()
            except Exception as e:  # noqa: BLE001
                res = {"sentence_id": futs[fu]["sentence_id"], "error": str(e)[:300]}
            fh.write(json.dumps(res, ensure_ascii=False) + "\n")
            fh.flush()
            if (i + 1) % 50 == 0:
                logger.info(f"pairwise {i + 1}/{len(T)} {time.time() - t0:.0f}s")


# --------------------------------------------------------------------------------------------------------- exact
def _init_ex():
    sys.path.insert(0, str(EXP5))
    import scoring.guard  # noqa: F401
    import pool_scoring as PS
    PS.init_worker(4.0)


def _exact_one(t: dict) -> dict:
    """c_exact: z3 equivalence (both entailment directions, 2 s each, frozen PT.z3_entails) with symbols identified by
    their exact name; UNKNOWN = not equivalent (counted)."""
    import peer_text as PT
    import pool_scoring as PS
    parsed = {}
    for r in t["rows"]:
        e = PT.parse_fol(r["fol"])
        parsed[r["key"]] = (PT.canon(e), e) if e is not None else (None, None)
    cache: dict = {}
    n_unknown = 0

    def eq(a: str, b: str):
        nonlocal n_unknown
        if a == b:
            return True
        k = (a, b) if a < b else (b, a)
        if k not in cache:
            ea, eb = PT.parse_fol(k[0]), PT.parse_fol(k[1])
            r1, to1 = PS._with_alarm(10, PT.z3_entails, ea, eb, 2000)
            r2, to2 = (None, True) if (to1 or r1 is not True) else PS._with_alarm(10, PT.z3_entails, eb, ea, 2000)
            if r1 is False or r2 is False:
                cache[k] = False
            elif r1 is True and r2 is True:
                cache[k] = True
            else:
                cache[k] = None
                n_unknown += 1
        return cache[k]
    out = []
    for r in t["rows"]:
        cs = parsed[r["key"]][0]
        if cs is None:
            out.append({"key": r["key"], "c_exact": None, "n_peers_exact": 0})
            continue
        P_c = [parsed[p["key"]][0] for p in t["rows"] if p["family"] != r["family"] and parsed[p["key"]][0] is not None]
        if len(P_c) < 2:
            out.append({"key": r["key"], "c_exact": None, "n_peers_exact": len(P_c)})
            continue
        eqs = [eq(cs, p) for p in P_c]
        out.append({"key": r["key"], "c_exact": 1 - sum(e is True for e in eqs) / len(P_c), "n_peers_exact": len(P_c),
                    "n_unknown_exact": sum(e is None for e in eqs)})
    return {"sentence_id": t["sentence_id"], "rows": out, "n_unknown_pairs": n_unknown}


def stage_exact(workers: int) -> None:
    outp = CACHE / "exact_E2.jsonl"
    done = {r["sentence_id"] for r in jl(outp)}
    T = [t for t in sentence_tasks() if t["sentence_id"] not in done]
    logger.info(f"exact: {len(T)} sentences")
    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn"), initializer=_init_ex) as ex, \
            outp.open("a") as fh:
        futs = {ex.submit(_exact_one, t): t for t in T}
        for fu in as_completed(futs):
            try:
                res = fu.result()
            except Exception as e:  # noqa: BLE001
                res = {"sentence_id": futs[fu]["sentence_id"], "rows": [], "error": str(e)[:300]}
            fh.write(json.dumps(res, ensure_ascii=False) + "\n")
            fh.flush()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", required=True)
    ap.add_argument("--workers", type=int, default=44)
    a = ap.parse_args()
    setup_log(f"consensus_{a.stage}")
    if a.stage == "l3":
        asyncio.run(_l3([t["text"] for t in sentence_tasks()]))
    elif a.stage == "score":
        stage_score(a.workers)
    elif a.stage == "pairwise":
        stage_pairwise(a.workers)
    elif a.stage == "exact":
        stage_exact(a.workers)


if __name__ == "__main__":
    main()
