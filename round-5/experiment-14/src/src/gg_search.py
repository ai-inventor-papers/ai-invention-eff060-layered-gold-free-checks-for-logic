#!/usr/bin/env python3
"""B4: CPU map search (freeze/gg.py gg_map_search) for
  * E: every node pair with kind != 'exact' in the sentences that contain >= 1 Z row (label-free: Z membership is used
    only to choose sentences, as in the plan), direction i -> j (bijections: one direction suffices);
  * PERTURB E-base items (MEANING_RENAME mutants, RENAME_SYN / RENAME_NONCE controls, BASE references) vs every peer node
    (node with >= 1 is_peer row) of their E sentence (exp-8 pool_rule 'all').
Parallel: ProcessPoolExecutor (spawn), one task = one sentence (formula analysis cached per worker). Resumable: appends
to results/gg_search.jsonl and skips done task ids. Usage: gg_search.py pilot | all"""
from __future__ import annotations

import json
import multiprocessing as mp
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from common import FREEZE, MATRIX, PERTURB_SCORES, RES, jl, sha1, setup_logger

logger = setup_logger("gg_search")
OUT = RES / "gg_search.jsonl"
PERTURB_KINDS = {"MEANING_RENAME", "RENAME_SYN", "RENAME_NONCE", "BASE"}


def z_sentences() -> set:
    """Sentences with >= 1 Z row (reads the sealed scores + the R_AB flag only)."""
    from labels import frame
    df = frame()
    return set(df[df.Z].sentence_id)


def perturb_items() -> list[dict]:
    out = []
    for r in jl(PERTURB_SCORES):
        if r["is_rcomp"]:
            continue
        kind = r["operator"] if r["operator"] else r["control_type"]
        if kind not in PERTURB_KINDS:
            continue
        out.append({"key": r["key"], "sentence_id": r["sentence_id"], "fol": r["fol"], "kind": kind})
    return out


def build_tasks(zs: set) -> list[dict]:
    recs = {r["sentence_id"]: r for r in jl(MATRIX)}
    pt = {}
    for it in perturb_items():
        pt.setdefault(it["sentence_id"], []).append(it)
    tasks = []
    for sid in sorted(set(zs) | set(pt), key=lambda s: sha1("GG|" + s)):
        r = recs[sid]
        fol = {nd["node_id"]: nd["canon_fol"] for nd in r["nodes"]}
        jobs = []
        if sid in zs:
            for i, j, eq, kind, _s in r["pairs"]:
                if kind != "exact":
                    jobs.append({"id": f"E|{sid}|{i}|{j}", "a": fol[i], "b": fol[j]})
        peer_nodes = [nd["node_id"] for nd in r["nodes"] if any(x["is_peer"] for x in nd["rows"])]
        for it in pt.get(sid, []):
            for n in peer_nodes:
                jobs.append({"id": f"P|{it['key']}|{n}", "a": it["fol"], "b": fol[n]})
        if jobs:
            tasks.append({"sid": sid, "stratum": r["source_stratum"], "jobs": jobs})
    return tasks


def work(task: dict) -> list[dict]:
    import resource
    resource.setrlimit(resource.RLIMIT_AS, (3 * 1024 ** 3, 3 * 1024 ** 3))
    sys.path.insert(0, str(FREEZE))
    sys.setrecursionlimit(20000)
    import gg
    out = []
    for j in task["jobs"]:
        t0 = time.time()
        try:
            s = gg.gg_map_search(j["a"], j["b"])
        except (MemoryError, RecursionError, ValueError, KeyError) as ex:
            s = {"status": "ERROR:" + type(ex).__name__, "maps": [], "n_maps": 0, "secs": round(time.time() - t0, 3)}
        out.append({"id": j["id"], "sid": task["sid"], "status": s["status"], "n_maps": s.get("n_maps", 0),
                    "n_fp_pass": s.get("n_fp_pass", 0), "n_z3_unknown": s.get("n_z3_unknown", 0), "anchored": s.get("anchored", False),
                    "capped": s.get("capped", False), "secs": s.get("secs"),
                    "maps": [{"nonidentity": m["nonidentity"], "pred": m["pred"], "const": m["const"]} for m in s.get("maps", [])]})
    return out


@logger.catch(reraise=True)
def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "pilot"
    os.environ["PYTHONHASHSEED"] = "0"
    tasks = build_tasks(z_sentences())
    n_jobs = sum(len(t["jobs"]) for t in tasks)
    logger.info(f"{len(tasks)} sentence tasks, {n_jobs} pairs "
                f"(E {sum(j['id'].startswith('E|') for t in tasks for j in t['jobs'])}, PERTURB {sum(j['id'].startswith('P|') for t in tasks for j in t['jobs'])})")
    out = OUT if mode == "all" else RES / "gg_search_pilot.jsonl"
    if mode == "pilot":
        flat = sorted([(t["sid"], t["stratum"], j) for t in tasks for j in t["jobs"]], key=lambda x: sha1("pilot|" + x[2]["id"]))[:200]
        by = {}
        for sid, stt, j in flat:
            by.setdefault(sid, {"sid": sid, "stratum": stt, "jobs": []})["jobs"].append(j)
        tasks = list(by.values())
        if out.exists():
            out.unlink()
    done = {r["id"] for r in jl(out)} if out.exists() else set()
    tasks = [{**t, "jobs": [j for j in t["jobs"] if j["id"] not in done]} for t in tasks]
    tasks = [t for t in tasks if t["jobs"]]
    workers = int(os.environ.get("GG_WORKERS", "6"))
    t0 = time.time()
    n = 0
    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn")) as ex, out.open("a") as fh:
        futs = {ex.submit(work, t): t["sid"] for t in tasks}
        for k, f in enumerate(as_completed(futs)):
            try:
                res = f.result()
            except Exception as e:  # noqa: BLE001 - a crashed worker task is logged and skipped (resumable)
                logger.error(f"task {futs[f]} failed: {type(e).__name__}: {str(e)[:200]}")
                continue
            for r in res:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            fh.flush()
            n += len(res)
            if (k + 1) % 20 == 0:
                logger.info(f"{k + 1}/{len(tasks)} sentences, {n} pairs, {time.time() - t0:.0f}s")
    logger.info(f"done {n} pairs in {time.time() - t0:.0f}s ({workers} workers)")


if __name__ == "__main__":
    main()
