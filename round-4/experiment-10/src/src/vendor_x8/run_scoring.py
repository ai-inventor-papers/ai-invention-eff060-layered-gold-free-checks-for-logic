#!/usr/bin/env python3
"""Label-free scoring driver for the pair engine (src/pairs.py). Never opens a label view.

usage: run_scoring.py screen [--stage mini|all]
       run_scoring.py E      [--stage mini|100|all]     (E sentences; the 200 PERTURB E-base sentences carry their
                                                       PERTURB mutants/controls/base as extra non-peer candidates)
Outputs (append-only, resumable by sentence_id):
  results/scores_{screen,E}.jsonl   one line per sentence: rows (c/g for align, nf, hyb; medoids), stats
  results/pairs_{screen,E}.jsonl    one line per (candidate row, peer row): align_eq, nf_eq, hyb_eq, nf_cost
  cache/pair_cache.sqlite           pair records (single writer = this process)
  results/stage_<pass>_<stage>.json timing per stratum + projection
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))
os.environ.setdefault("NLTK_DATA", str(ROOT / "data" / "nltk_data"))
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):  # spawned workers inherit: no BLAS thread pools
    os.environ[_v] = "1"
import pairs as PR  # noqa: E402
import peer_text as PT  # noqa: E402
import tasks as TK  # noqa: E402

RES = ROOT / "results"
PARAMS = {"k": 5, "tau": {"NF-anchored": 0.5, "ALIGN": None}, "timeout_ms": 2000, "pair_cap_s": 30, "codes": False,
          "medoid": True, "emit_pairs": True, "use_cache": True}


def n_workers() -> int:
    try:
        q = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_quota_us").read_text())
        p = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_period_us").read_text())
        n = max(1, int(q / p)) if q > 0 else len(os.sched_getaffinity(0))
    except (FileNotFoundError, ValueError):
        n = len(os.sched_getaffinity(0))
    return max(1, n - 1)


logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "run_scoring.log", rotation="30 MB", level="DEBUG")


def build(pass_: str) -> list[dict]:
    if pass_ == "screen":
        return TK.screen_tasks()
    extra = TK.perturb_extra()
    base = TK.E_tasks()
    ext = {t["sentence_id"]: t for t in TK.E_tasks(extra=extra)}
    out = [ext.get(t["sentence_id"], t) for t in base]
    for t in out:
        t["has_perturb"] = t["sentence_id"] in ext
    return out


def select(T: list[dict], stage: str, pass_: str) -> list[dict]:
    if stage == "all":
        return T
    if pass_ == "screen":
        return T[:20]
    per = 5 if stage == "mini" else 25
    sel = []
    for s in TK.STRATA:
        sel += [x for x in T if x["stratum"] == s][:per]
    return sel


@logger.catch(reraise=True)
def run(pass_: str, stage: str, workers: int):
    T = build(pass_)
    outp, pairp = RES / f"scores_{pass_}.jsonl", RES / f"pairs_{pass_}.jsonl"
    done = {r["sentence_id"] for r in TK.jl(outp)}
    sel = select(T, stage, pass_)
    todo = [t for t in sel if t["sentence_id"] not in done]
    con = PR.open_db()
    for t in todo:  # preload cached peer-peer pairs (reuse across passes / restarts)
        pool = sorted({PT.canon(e) for e in (PT.parse_fol(r["fol"]) for r in t["rows"] if r.get("is_peer")) if e is not None})
        t["preload"] = PR.load_pairs(con, PR.preload_keys(t["text"], pool))
    logger.info(f"{pass_} stage {stage}: {len(sel)} selected, {len(todo)} to score, rows {sum(len(t['rows']) for t in todo)}, "
                f"workers {workers}")
    t0 = time.time()
    secs_by, rows_by = defaultdict(list), defaultdict(int)
    todo.sort(key=lambda t: -len(t["rows"]))
    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn"), initializer=PR.init_worker,
                             initargs=(5.0,)) as ex, outp.open("a") as fh, pairp.open("a") as fp:
        futs = {ex.submit(PR.score_sentence, t, PARAMS): t for t in todo}
        for i, fu in enumerate(as_completed(futs)):
            t = futs[fu]
            try:
                res = fu.result()
            except Exception as e:  # noqa: BLE001 - a sentence failure is logged and its rows marked, never dropped
                logger.error(f"sentence {t['sentence_id']} failed: {e!r}")
                res = {"sentence_id": t["sentence_id"], "rows": [{"key": r["key"], "coverage_status": "WORKER_FAIL"} for r in t["rows"]],
                       "pairs": [], "stats": {"error": repr(e)[:300]}, "new_cache": {}}
            PR.store_pairs(con, res.pop("new_cache", {}))
            for p in res.pop("pairs"):
                fp.write(json.dumps({"sentence_id": t["sentence_id"], **p}) + "\n")
            res["stratum"] = t["stratum"]
            res["has_perturb"] = t.get("has_perturb", False)
            fh.write(json.dumps(res, ensure_ascii=False) + "\n")
            fh.flush()
            fp.flush()
            secs_by[t["stratum"]].append(res["stats"].get("secs_total", 0))
            rows_by[t["stratum"]] += len(t["rows"])
            if (i + 1) % 10 == 0:
                logger.info(f"{pass_} {i + 1}/{len(todo)} sentences, {time.time() - t0:.0f}s wall")
    wall = time.time() - t0
    per = {s: (sum(v) / len(v), len(v)) for s, v in secs_by.items() if v}
    done2 = {r["sentence_id"] for r in TK.jl(outp)}
    remaining = [t for t in T if t["sentence_id"] not in done2]
    tot_cpu = sum(sum(v) for v in secs_by.values())
    tot_rows = sum(rows_by.values())
    proj = (tot_cpu / max(1, tot_rows)) * sum(len(t["rows"]) for t in remaining) / workers
    st = {"wall_s": round(wall, 1), "per_stratum_mean_cpu_s": per, "cpu_s_per_row": tot_cpu / max(1, tot_rows),
          "remaining_sentences": len(remaining), "projection_min_remaining": round(proj / 60, 1), "workers": workers}
    logger.info(f"{pass_} stage {stage} done: {json.dumps(st)}")
    (RES / f"stage_{pass_}_{stage}.json").write_text(json.dumps(st, indent=1))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("pass_", choices=["screen", "E"])
    ap.add_argument("--stage", default="mini", choices=["mini", "100", "all"])
    ap.add_argument("--workers", type=int, default=0)
    a = ap.parse_args()
    RES.mkdir(exist_ok=True)
    run(a.pass_, a.stage, a.workers or n_workers())
