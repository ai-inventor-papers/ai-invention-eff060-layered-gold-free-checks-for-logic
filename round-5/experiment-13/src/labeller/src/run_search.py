#!/usr/bin/env python3
"""STEP C (and audit (i) search): exhaustive map search per unique (sentence, candidate) class, CPU only.

usage: run_search.py free [--limit N]          -> results/map_search.jsonl       (FREE classes)
       run_search.py sig --rename nonce|syn    -> results/sig_replay_{nonce,syn}.jsonl (renamed SIG classes)
Resumable (skips class keys already written). ProcessPoolExecutor(spawn), one task per sentence.
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import re
import resource
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed

from common import RES, WORK, load_jsonl, setup_logger, sha1

NUM_WORKERS = 4


def class_key(sid: str, fol: str) -> str:
    return sha1(sid + "|" + re.sub(r"\s+", "", fol))[:16]


def work_sentence(job: dict) -> list[dict]:
    import sys
    sys.setrecursionlimit(10000)
    import common  # noqa: F401  (paths)
    import freelab as FL
    s = job["sent"]
    rdfs = {"weak": s["reference_fol_weak"], "strong": s["reference_fol_strong"]}
    if s.get("reading_converse"):
        rdfs["converse"] = s["reading_converse"]
    rds = {k: FL.Reading(v, s["units"]) for k, v in rdfs.items()}
    out = []
    for ck, fol in job["classes"]:
        t0 = time.time()
        try:
            cand = FL.Candidate(fol)
        except (ValueError, IndexError, TypeError, KeyError, RecursionError) as ex:
            out.append({"class_key": ck, "sentence_id": s["sentence_id"], "candidate_fol": fol, "status": "UNPARSEABLE",
                        "error": str(ex)[:160]})
            continue
        try:
            r = FL.label_with(cand, rds, FL.MAX_MAPS * job.get("cap_mult", 1), FL.MAX_SECS * job.get("cap_mult", 1), t0)
        except Exception as ex:  # noqa: BLE001 - one class must not kill the sentence
            out.append({"class_key": ck, "sentence_id": s["sentence_id"], "candidate_fol": fol,
                        "status": "UNRESOLVED_Z3_UNKNOWN", "error": f"{type(ex).__name__}: {str(ex)[:160]}"})
            continue
        out.append({"class_key": ck, "sentence_id": s["sentence_id"], "candidate_fol": fol, **r})
    return out


def run(classes_by_sid: dict, sents: dict, outp, logger, limit: int | None, cap_mult: int = 1) -> None:
    done = set()
    if outp.exists():
        done = {json.loads(l)["class_key"] for l in outp.read_text().splitlines() if l.strip()}
    jobs, n = [], 0
    for sid in sorted(classes_by_sid):
        cl = [(ck, f) for ck, f in classes_by_sid[sid] if ck not in done]
        if not cl:
            continue
        if limit is not None and n >= limit:
            break
        if limit is not None:
            cl = cl[: max(0, limit - n)]
        n += len(cl)
        jobs.append({"sent": sents[sid], "classes": cl, "cap_mult": cap_mult})
    logger.info(f"{outp.name}: {n} classes to search over {len(jobs)} sentences ({len(done)} already done), {NUM_WORKERS} workers")
    t0 = time.time()
    k = 0
    with ProcessPoolExecutor(max_workers=NUM_WORKERS, mp_context=mp.get_context("spawn")) as ex, outp.open("a") as fh:
        futs = {ex.submit(work_sentence, j): j["sent"]["sentence_id"] for j in jobs}
        for f in as_completed(futs):
            try:
                res = f.result()
            except Exception as e:  # noqa: BLE001 - worker crash: the sentence is retried on the next resume
                logger.error(f"sentence {futs[f]} failed: {type(e).__name__}: {e}")
                continue
            for r in res:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
                k += 1
            fh.flush()
            logger.info(f"{k}/{n} classes, {time.time() - t0:.0f}s elapsed, {(time.time() - t0) / max(k, 1):.2f}s/class")
    logger.info(f"done {k} classes in {time.time() - t0:.0f}s")


def main() -> None:
    resource.setrlimit(resource.RLIMIT_AS, (60 * 1024**3, 60 * 1024**3))
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["free", "sig"])
    ap.add_argument("--rename", choices=["nonce", "syn"])
    ap.add_argument("--limit", type=int)
    ap.add_argument("--cap-mult", type=int, default=1)
    ap.add_argument("--out")
    a = ap.parse_args()
    logger = setup_logger(f"search_{a.mode}{'_' + a.rename if a.rename else ''}")
    sents = json.loads((WORK / "sentences.json").read_text())
    by = defaultdict(dict)
    if a.mode == "free":
        for r in load_jsonl(WORK / "free_rows.jsonl"):
            if r["input_status"] == "PARSED":
                by[r["sentence_id"]][class_key(r["sentence_id"], r["candidate_fol"])] = r["candidate_fol"]
        outp = RES / (a.out or "map_search.jsonl")
    else:
        for r in load_jsonl(WORK / f"sig_renamed_{a.rename}.jsonl"):
            by[r["sentence_id"]][class_key(r["sentence_id"], r["renamed_fol"])] = r["renamed_fol"]
        outp = RES / (a.out or f"sig_replay_{a.rename}.jsonl")
    classes = {sid: sorted(d.items()) for sid, d in by.items()}
    run(classes, sents, outp, logger, a.limit, a.cap_mult)


if __name__ == "__main__":
    main()
