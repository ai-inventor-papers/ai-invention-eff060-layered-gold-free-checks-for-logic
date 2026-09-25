#!/usr/bin/env python3
"""STEP 2 driver: stream the label-free pairwise eqmv matrix per E sentence to results/pair_matrix_E.jsonl.

usage: run_matrix.py --stage mini|rab|rest [--workers N] [--max-minutes M]
  mini = 12 sentences (3 per stratum); rab = every sentence with >=1 R_AB row (L25, L20, EXC, CTRL order);
  rest = the remaining E sentences. Append-only and resumable (sentences already in the file are skipped).
Labels are read ONLY to choose the R_AB-first ORDER; the matrix itself never sees a label.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import multiprocessing as mp
import os
import sys
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

os.environ["PYTHONHASHSEED"] = "0"  # inherited by spawned workers
from loguru import logger

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import pairwise as PW  # noqa: E402
from paths import E5, jl  # noqa: E402

OUT = ROOT / "results" / "pair_matrix_E.jsonl"
STRATA = ["L25", "L20", "EXC", "CTRL"]

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "run_matrix.log", rotation="30 MB", level="DEBUG")


def detect_cpus() -> int:
    try:
        parts = Path("/sys/fs/cgroup/cpu.max").read_text().split()
        if parts[0] != "max":
            return math.ceil(int(parts[0]) / int(parts[1]))
    except (FileNotFoundError, ValueError):
        pass
    try:
        return len(os.sched_getaffinity(0))
    except (AttributeError, OSError):
        return os.cpu_count() or 1


def in_rab(L: dict) -> bool:
    """analyse_E.regime(r, 'R_AB') with default args."""
    return (L["system_class"] == "llm" and not L.get("reading_choice") and L["final_label"] in ("CORRECT", "ERROR")
            and L["label_tier"] in ("A", "B"))


def build_tasks() -> tuple[list[dict], set]:
    pre = json.loads((E5 / "results" / "prereg.json").read_text())
    fam_v = pre["family_map_vendor"]
    by = defaultdict(list)
    for r in jl(E5 / "data" / "E_blind.jsonl"):
        by[r["sentence_id"]].append(r)
    rab_sids = {L["sentence_id"] for L in jl(E5 / "data" / "E_labels.jsonl") if in_rab(L)}
    tasks = []
    for sid, rs in by.items():
        st = rs[0]["strata"]
        tasks.append({"sentence_id": sid, "source_stratum": st["source_stratum"], "words": st["words"],
                      "n_conditions": st["n_conditions"],
                      "rows": [{"row_key": r["row_key"], "fol": r["candidate_fol"], "slot": r["slot"], "family": fam_v[r["slot"]],
                                "family_field": r["family"], "system_class": r["system_class"]} for r in rs]})
    tasks.sort(key=lambda t: (STRATA.index(t["source_stratum"]), hashlib.sha1(t["sentence_id"].encode()).hexdigest()))
    return tasks, rab_sids


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=["mini", "rab", "rest"], required=True)
    ap.add_argument("--workers", type=int, default=0)
    ap.add_argument("--max-minutes", type=float, default=70.0)
    a = ap.parse_args()
    tasks, rab = build_tasks()
    done = {r["sentence_id"] for r in jl(OUT)}
    if a.stage == "mini":
        sel = [t for s in STRATA for t in [x for x in tasks if x["source_stratum"] == s and x["sentence_id"] in rab][:3]]
    elif a.stage == "rab":
        sel = [t for t in tasks if t["sentence_id"] in rab]
    else:
        sel = [t for t in tasks if t["sentence_id"] not in rab]
    todo = [t for t in sel if t["sentence_id"] not in done]
    nw = a.workers or detect_cpus()
    logger.info(f"stage {a.stage}: {len(sel)} selected, {len(todo)} to compute, {nw} workers, code_sha {PW.code_sha()}")
    t0 = time.time()
    deadline = t0 + a.max_minutes * 60
    import z3
    zver = z3.get_version_string()
    n_ok = 0
    with ProcessPoolExecutor(max_workers=nw, mp_context=mp.get_context("spawn"), initializer=PW.init_worker,
                             initargs=(3.5,)) as ex, OUT.open("a") as fh:
        futs = {ex.submit(PW.work, t): t for t in todo}
        for fu in as_completed(futs):
            t = futs[fu]
            try:
                res = fu.result()
            except Exception as e:  # noqa: BLE001 - recorded, never silently dropped
                logger.error(f"sentence {t['sentence_id']} failed: {e}")
                res = {"sentence_id": t["sentence_id"], "source_stratum": t["source_stratum"], "error": str(e)[:300],
                       "nodes": [], "pairs": [], "unparseable": []}
            res["z3_version"] = zver
            res["code_sha"] = PW.code_sha()
            fh.write(json.dumps(res, ensure_ascii=False) + "\n")
            fh.flush()
            n_ok += 1
            if n_ok % 10 == 0 or n_ok == len(todo):
                el = time.time() - t0
                logger.info(f"{n_ok}/{len(todo)} sentences, {el:.0f}s wall, ETA {el / n_ok * (len(todo) - n_ok) / 60:.1f} min")
            if time.time() > deadline:
                logger.warning("max-minutes reached: cancelling remaining sentences (resumable)")
                for f in futs:
                    f.cancel()
                break
    el = time.time() - t0
    (ROOT / "results" / f"matrix_stage_{a.stage}.json").write_text(json.dumps(
        {"stage": a.stage, "n_selected": len(sel), "n_computed": n_ok, "wall_s": el, "workers": nw, "z3": zver}))
    logger.info(f"stage {a.stage} done: {n_ok} sentences in {el:.0f}s")


if __name__ == "__main__":
    main()
