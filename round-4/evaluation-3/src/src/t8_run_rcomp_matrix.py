#!/usr/bin/env python3
"""PART 2 driver: eval-2's UNCHANGED pairwise.work (label-free eqmv matrix, eqmv_ms 3000, pair cap 30 s) on every
R_COMP (sentence_id, condition) task -> results/pair_matrix_RCOMP.jsonl (append-only, resumable).

usage: t8_run_rcomp_matrix.py --stage mini|s50|all [--workers 4]
Rows = parse_ok candidates of the task (fol = candidate_fol, family = rcomp vendor family, slot). Peers follow exp 7's
scorer: few-shot rows (SIG sig_v1, FREE fewshot_v1) are system_class 'llm' (is_peer); FREE zero-shot rows are nodes but
not peers (system_class 'llm_zeroshot'). No label is read here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import multiprocessing as mp
import os
import sys
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

os.environ["PYTHONHASHSEED"] = "0"  # inherited by spawned workers (must be set before interpreter start of children)
sys.path.insert(0, str(Path(__file__).resolve().parent))
from loguru import logger  # noqa: E402

from t8_paths import E7, RESD, ROOT, jl  # noqa: E402
import pairwise as PW  # noqa: E402  (eval-2 src, unchanged)

OUT = RESD / "pair_matrix_RCOMP.jsonl"
PEER_VARIANT = {"SIG": "sig_v1", "FREE": "fewshot_v1"}

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "rcomp_matrix.log", rotation="30 MB", level="DEBUG")


def build_tasks() -> list[dict]:
    by = defaultdict(list)
    for r in jl(E7 / "results" / "rcomp_candidates.jsonl"):
        by[(r["sentence_id"], r["condition"])].append(r)
    tasks = []
    for (sid, cond), rs in by.items():
        st = rs[0]["strata"]
        rows = [{"row_key": r["row_key"], "fol": r["candidate_fol"], "slot": r["slot"], "family": r["family"],
                 "family_field": r["family"],
                 "system_class": "llm" if r["prompt_variant"] == PEER_VARIANT[cond] else "llm_zeroshot"}
                for r in rs if r["parse_ok"] and r["candidate_fol"]]
        tasks.append({"sentence_id": sid, "condition": cond, "source_stratum": f"RCOMP_{st['template_id']}",
                      "words": st["words"], "n_conditions": st["nconds_weak"], "rows": rows})
    tasks.sort(key=lambda t: (hashlib.sha1(t["sentence_id"].encode()).hexdigest(), t["condition"]))
    return tasks


def work(task: dict) -> dict:
    res = PW.work(task)
    res["condition"] = task["condition"]
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["mini", "s50", "all"], required=True)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    tasks = build_tasks()
    sids = sorted({t["sentence_id"] for t in tasks}, key=lambda s: hashlib.sha1(s.encode()).hexdigest())
    lim = {"mini": 5, "s50": 50, "all": len(sids)}[a.stage]
    keep = set(sids[:lim])
    done = {(r["sentence_id"], r["condition"]) for r in jl(OUT)}
    todo = [t for t in tasks if t["sentence_id"] in keep and (t["sentence_id"], t["condition"]) not in done]
    logger.info(f"stage {a.stage}: {len(keep)} sentences, {len(todo)} tasks to compute, code_sha {PW.code_sha()}")
    import z3
    zver = z3.get_version_string()
    t0 = time.time()
    n = 0
    with ProcessPoolExecutor(max_workers=a.workers, mp_context=mp.get_context("spawn"), initializer=PW.init_worker,
                             initargs=(3.5,)) as ex, OUT.open("a") as fh:
        futs = {ex.submit(work, t): t for t in todo}
        for fu in as_completed(futs):
            t = futs[fu]
            try:
                res = fu.result()
            except Exception as e:  # noqa: BLE001 - recorded, never silently dropped
                logger.error(f"task {t['sentence_id']}/{t['condition']} failed: {e}")
                res = {"sentence_id": t["sentence_id"], "condition": t["condition"], "error": str(e)[:300],
                       "nodes": [], "pairs": [], "unparseable": []}
            res["z3_version"] = zver
            res["code_sha"] = PW.code_sha()
            fh.write(json.dumps(res, ensure_ascii=False) + "\n")
            fh.flush()
            n += 1
            if n % 20 == 0 or n == len(todo):
                el = time.time() - t0
                logger.info(f"{n}/{len(todo)} tasks, {el:.0f}s, {el / n:.2f} s/task, ETA {el / n * (len(todo) - n) / 60:.1f} min")
    el = time.time() - t0
    (RESD / f"rcomp_matrix_stage_{a.stage}.json").write_text(json.dumps(
        {"stage": a.stage, "n_sentences": len(keep), "n_tasks_computed": n, "wall_s": el,
         "s_per_sentence": el / max(1, n / 2), "workers": a.workers, "z3": zver}))
    logger.info(f"stage {a.stage} done: {n} tasks in {el:.0f}s")


if __name__ == "__main__":
    main()
