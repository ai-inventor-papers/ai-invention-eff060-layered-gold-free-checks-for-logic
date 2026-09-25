#!/usr/bin/env python3
"""STEP 3 (and 6b): per-sentence auto-labelling with EQUIVALENCE-CLASS collapse.

Job = {sentence_id, reference, cands: [{key, fol, no_repair}]}.
1. Union-find: each parseable candidate is compared with the existing class representatives (reference class
   first) using label_lib.equivalent_modulo_vocab(cand, rep); EQ/VOCAB/GRAN joins; UNKNOWN/NONEQ against every
   rep opens a new class. Identical strings join without a solver call.
2. Reference-class members: EQ -> CORRECT, VOCAB/GRAN -> VOCAB_GRAN (status measured against the reference).
3. Every other class: label_lib.auto_label(rep, reference, budget_s) -> ERROR(ops) / COMPOUND / TIMEOUT_UNKNOWN;
   the label propagates from the representative to all member rows.
Usage: run_label.py --kind heldout|screen [--limit N] [--budget 8] [--workers 4]
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _init():
    sys.path.insert(0, str(ROOT / "labeller"))
    sys.setrecursionlimit(10000)


def label_sentence(job: dict, budget_s: float) -> dict:
    _init()
    from fol import parse
    from label_lib import equivalent_modulo_vocab, auto_label, convention_flags
    t0 = time.time()
    ref_str = job["reference"]
    ref = parse(ref_str)
    classes = [{"rep_str": ref_str, "rep": ref, "members": [], "is_ref": True, "no_repair": False}]
    rows = {}
    n_checks = 0
    for c in job["cands"]:
        key, fol = c["key"], c["fol"]
        if not (fol or "").strip():  # fol.parse('') returns ('atom', None, ()) -> must be UNPARSEABLE
            rows[key] = {"auto_label": "UNPARSEABLE", "class_idx": None, "parse_error": "empty"}
            continue
        try:
            e = parse(fol)
        except Exception as ex:  # noqa: BLE001 - parser raises assorted errors on junk
            rows[key] = {"auto_label": "UNPARSEABLE", "class_idx": None, "parse_error": str(ex)[:100]}
            continue
        joined = None
        for ci, cl in enumerate(classes):
            if fol.strip() == cl["rep_str"].strip():
                st = "EQ"
            else:
                try:
                    st = equivalent_modulo_vocab(e, cl["rep"])
                except (RecursionError, Exception):  # noqa: BLE001 - z3/aligner failure = no join
                    st = "UNKNOWN"
                n_checks += 1
            if st in ("EQ", "VOCAB", "GRAN"):
                joined = ci
                cl["members"].append(key)
                if cl["is_ref"]:
                    rows[key] = {"auto_label": "CORRECT" if st == "EQ" else "VOCAB_GRAN", "equiv_status": st,
                                 "class_idx": ci, "join_status": st}
                else:
                    rows[key] = {"class_idx": ci, "join_status": st}
                break
        if joined is None:
            classes.append({"rep_str": fol, "rep": e, "members": [key], "is_ref": False, "no_repair": bool(c.get("no_repair"))})
            rows[key] = {"class_idx": len(classes) - 1, "join_status": "REP"}
    # label non-reference classes from their representative
    cls_out = []
    for ci, cl in enumerate(classes):
        info = {"class_idx": ci, "is_ref": cl["is_ref"], "rep_fol": cl["rep_str"], "size": len(cl["members"]) + (1 if cl["is_ref"] else 0),
                "members": cl["members"]}
        if not cl["is_ref"]:
            try:
                lab = auto_label(cl["rep_str"], ref_str, budget_s=budget_s, repair=not cl["no_repair"])
            except (RecursionError, Exception) as ex:  # noqa: BLE001
                lab = {"auto_label": "TIMEOUT_UNKNOWN", "equiv_status": "ERROR", "error": str(ex)[:100]}
            if lab.get("auto_label") == "NONEQ_UNREPAIRED":
                lab["auto_label"], lab["repair_status"] = "COMPOUND", "SKIPPED_EVENTSEM"
            info.update(lab)
            for k in cl["members"]:
                rows[k].update({kk: lab.get(kk) for kk in ("auto_label", "equiv_status", "repair_ops", "repair_status", "convention_flags")})
        else:
            info["auto_label"] = "REFERENCE"
            for k in cl["members"]:
                if rows[k]["auto_label"] != "CORRECT":
                    try:
                        rows[k]["convention_flags"] = convention_flags(parse(next(c["fol"] for c in job["cands"] if c["key"] == k)), ref)
                    except (RecursionError, Exception):  # noqa: BLE001
                        rows[k]["convention_flags"] = ["FLAG_ERROR"]
        cls_out.append(info)
    return {"sentence_id": job["sentence_id"], "reference": ref_str, "rows": rows, "classes": cls_out,
            "n_checks": n_checks, "secs": round(time.time() - t0, 2), "budget_s": budget_s}


def run(jobs: list[dict], out_path: Path, budget_s: float, workers: int, log=print) -> None:
    done = set()
    if out_path.exists():
        for line in out_path.read_text().splitlines():
            if line.strip():
                done.add(json.loads(line)["sentence_id"])
    todo = [j for j in jobs if j["sentence_id"] not in done]
    log(f"label jobs: {len(todo)} (done {len(done)})")
    t0 = time.time()
    ctx = mp.get_context("spawn")
    with ProcessPoolExecutor(max_workers=workers, mp_context=ctx) as ex, open(out_path, "a", encoding="utf-8") as f:
        futs = {ex.submit(label_sentence, j, budget_s): j["sentence_id"] for j in todo}
        n = 0
        for fut in as_completed(futs):
            try:
                r = fut.result()
            except Exception as e:  # noqa: BLE001 - keep the sweep alive; record the failure
                r = {"sentence_id": futs[fut], "error": f"{type(e).__name__}: {str(e)[:200]}", "rows": {}, "classes": []}
            f.write(json.dumps(r, ensure_ascii=False) + "\n"); f.flush()
            n += 1
            if n % 20 == 0 or n == len(todo):
                el = time.time() - t0
                log(f"labelled {n}/{len(todo)} in {el:.0f}s; projected total {el / n * len(todo):.0f}s")
