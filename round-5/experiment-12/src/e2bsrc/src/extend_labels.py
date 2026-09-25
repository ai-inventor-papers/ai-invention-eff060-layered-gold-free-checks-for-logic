#!/usr/bin/env python3
"""Incremental auto-labelling: add candidate rows that are missing from an existing labels file WITHOUT renumbering
the classes that are already there (so panel votes keyed by class id stay valid).

Same algorithm as label_worker.label_sentence: each new parseable candidate is compared with the existing class
representatives in class order (reference class first) via equivalent_modulo_vocab; EQ/VOCAB/GRAN joins (label
propagates from the class), otherwise it founds a new class appended at the end, labelled by auto_label(rep, ref).
Used for the G2 zero-shot rows regenerated after the key's daily limit reset.
Usage: extend_labels.py [--labels labels_heldout.jsonl] [--budget 8] [--workers 4]
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import shutil
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))


def extend(lab: dict, new: list[dict], budget_s: float) -> dict:
    sys.path.insert(0, str(ROOT / "labeller"))
    sys.setrecursionlimit(10000)
    from fol import parse
    from label_lib import equivalent_modulo_vocab, auto_label, convention_flags
    t0 = time.time()
    ref_str = lab["reference"]
    ref = parse(ref_str)
    classes = lab["classes"]
    reps = []
    for c in classes:
        try:
            reps.append(parse(c["rep_fol"]) if c["rep_fol"].strip() else None)
        except Exception:  # noqa: BLE001
            reps.append(None)
    n_checks = 0
    for c in new:
        key, fol = c["key"], c["fol"]
        if not (fol or "").strip():
            lab["rows"][key] = {"auto_label": "UNPARSEABLE", "class_idx": None, "parse_error": "empty", "added_incrementally": True}
            continue
        try:
            e = parse(fol)
        except Exception as ex:  # noqa: BLE001
            lab["rows"][key] = {"auto_label": "UNPARSEABLE", "class_idx": None, "parse_error": str(ex)[:100], "added_incrementally": True}
            continue
        joined = None
        for ci, cl in enumerate(classes):
            if reps[ci] is None:
                continue
            if fol.strip() == cl["rep_fol"].strip():
                st = "EQ"
            else:
                try:
                    st = equivalent_modulo_vocab(e, reps[ci])
                except (RecursionError, Exception):  # noqa: BLE001
                    st = "UNKNOWN"
                n_checks += 1
            if st in ("EQ", "VOCAB", "GRAN"):
                joined = ci
                cl["members"].append(key); cl["size"] += 1
                if cl["is_ref"]:
                    row = {"auto_label": "CORRECT" if st == "EQ" else "VOCAB_GRAN", "equiv_status": st, "class_idx": ci, "join_status": st}
                    if st != "EQ":
                        try:
                            row["convention_flags"] = convention_flags(e, ref)
                        except (RecursionError, Exception):  # noqa: BLE001
                            row["convention_flags"] = ["FLAG_ERROR"]
                else:
                    row = {"class_idx": ci, "join_status": st, **{k: cl.get(k) for k in ("auto_label", "equiv_status", "repair_ops", "repair_status", "convention_flags")}}
                row["added_incrementally"] = True
                lab["rows"][key] = row
                break
        if joined is None:
            try:
                lb = auto_label(fol, ref_str, budget_s=budget_s, repair=not c.get("no_repair"))
            except (RecursionError, Exception) as ex:  # noqa: BLE001
                lb = {"auto_label": "TIMEOUT_UNKNOWN", "equiv_status": "ERROR", "error": str(ex)[:100]}
            ci = len(classes)
            classes.append({"class_idx": ci, "is_ref": False, "rep_fol": fol, "size": 1, "members": [key], **lb})
            reps.append(e)
            lab["rows"][key] = {"class_idx": ci, "join_status": "REP", "added_incrementally": True,
                                **{k: lb.get(k) for k in ("auto_label", "equiv_status", "repair_ops", "repair_status", "convention_flags")}}
    lab["n_checks_incremental"] = lab.get("n_checks_incremental", 0) + n_checks
    lab["secs_incremental"] = round(lab.get("secs_incremental", 0) + time.time() - t0, 2)
    return lab


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--labels", default="labels_heldout.jsonl")
    ap.add_argument("--budget", type=float, default=8.0)
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args()
    from run_label import heldout_jobs
    path = ROOT / "work" / a.labels
    labs = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    jobs = {j["sentence_id"]: j for j in heldout_jobs()}
    todo = []
    for lab in labs:
        j = jobs.get(lab["sentence_id"])
        if j is None or "error" in lab:
            continue
        new = [c for c in j["cands"] if c["key"] not in lab["rows"]]
        if new:
            todo.append((lab, new))
    print(f"sentences with new rows: {len(todo)}; new rows: {sum(len(n) for _, n in todo)}", flush=True)
    if not todo:
        return
    shutil.copy(path, path.with_suffix(".jsonl.bak_before_extend"))
    out = {}
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=a.workers, mp_context=mp.get_context("spawn")) as ex:
        futs = {ex.submit(extend, lab, new, a.budget): lab["sentence_id"] for lab, new in todo}
        for i, f in enumerate(as_completed(futs), 1):
            out[futs[f]] = f.result()
            if i % 50 == 0:
                print(f"{i}/{len(todo)} {time.time() - t0:.0f}s", flush=True)
    tmp = path.with_suffix(".jsonl.tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        for lab in labs:
            f.write(json.dumps(out.get(lab["sentence_id"], lab), ensure_ascii=False) + "\n")
    tmp.replace(path)
    print(f"extended {len(out)} sentences in {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
