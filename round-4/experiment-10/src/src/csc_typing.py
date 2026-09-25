"""STAGE 7 PART 3 (search part): same-vocabulary typed repair of every PERTURB mutant towards several targets.

Targets per mutant (label-blind search; the operator is joined only in csc_analysis.py):
  oracle        the true base reference (same-code ceiling; ORACLE_samevocab)
  csc           CSC K3 peer-majority formula (if CSC peers exist; NO_MAJORITY recorded)
  proxy         SIGPROXY K3 peer-majority formula (exp-7 SIG outputs of the same families; R_COMP bases only)
  free3         FREE3 (uncued, same families) peer-majority formula (lower-cased; vocabulary usually differs)
Sound shortcut MISSING_PREDS: each typed edit introduces at most ONE predicate symbol absent from the mutant
(ADD / SUBST; ADD_ANY re-uses present ones), so a target with > 2 predicate symbols missing from the mutant has no
depth-2 repair; recorded as cls 'VOCAB_GAP' without search.
Output: results/typing_search_rows.jsonl (append; resumable by (key, which)).
"""
from __future__ import annotations

import json
import multiprocessing as mp
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from loguru import logger

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
DATA = ROOT / "data"
RES = ROOT / "results"
OUT = RES / "typing_search_rows.jsonl"
BUDGET_S = 6.0


def jl(p: Path) -> list[dict]:
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()] if p.exists() else []


def _init():
    for v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ[v] = "1"
    sys.path.insert(0, str(SRC))
    sys.setrecursionlimit(20000)
    import csc_lib  # noqa: F401


def missing_preds(L, mutant: str, target: str) -> int | None:
    a, b = L.parse(mutant), L.parse(target)
    if a is None or b is None:
        return None
    pa = {(n.lower(), k) for n, k in L.RC.symbols(a)[0]}
    pb = {(n.lower(), k) for n, k in L.RC.symbols(b)[0]}
    return len(pb - pa)


def job(args):
    key, which, mutant, target = args
    import csc_lib as L
    t0 = time.time()
    mp_ = missing_preds(L, mutant, target)
    if mp_ is None:
        return {"key": key, "which": which, "cls": "PARSE_FAIL", "ops": [], "secs": 0.0}
    if mp_ > 2:
        return {"key": key, "which": which, "cls": "VOCAB_GAP", "ops": [], "missing_preds": mp_, "secs": round(time.time() - t0, 3)}
    r = L.typed_repair_same_vocab(mutant, target, budget_s=BUDGET_S)
    return {"key": key, "which": which, **r, "missing_preds": mp_}


def build_jobs(which_set: set[str]) -> list[tuple]:
    view = {r["key"]: r for r in jl(DATA / "perturb_view.jsonl")}
    sc = {r["key"]: r for r in jl(RES / "scores_raw.jsonl")}
    jobs = []
    for k, r in view.items():
        if r["fold"] != "PERTURB":
            continue
        s = sc.get(k, {})
        tg = {"oracle": r["reference_fol"], "csc": s.get("csc_majority"), "proxy": s.get("proxy_majority"),
              "free3": s.get("free3_majority")}
        for w, t in tg.items():
            if w in which_set and t:
                jobs.append((k, w, r["candidate_fol"], t))
    return jobs


def main(argv: list[str]) -> None:
    which = set((argv[argv.index("--which") + 1]).split(",")) if "--which" in argv else {"oracle", "csc", "proxy", "free3"}
    mini = int(argv[argv.index("--mini") + 1]) if "--mini" in argv else None
    out_p = RES / ("typing_search_rows_mini.jsonl" if mini else "typing_search_rows.jsonl")
    jobs = build_jobs(which)
    if mini:
        import random
        jobs = random.Random(0).sample(jobs, min(mini, len(jobs)))
        if out_p.exists():
            out_p.unlink()
    done = {(x["key"], x["which"]) for x in jl(out_p)}
    todo = [j for j in jobs if (j[0], j[1]) not in done]
    nw = max(1, len(os.sched_getaffinity(0)) - 1)
    logger.info(f"typing: {len(jobs)} jobs ({sorted(which)}), {len(todo)} to do, {nw} workers")
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=nw, mp_context=mp.get_context("spawn"), initializer=_init) as ex, out_p.open("a") as fh:
        futs = {ex.submit(job, j): j for j in todo}
        for i, f in enumerate(as_completed(futs)):
            j = futs[f]
            try:
                res = f.result()
            except Exception as e:  # noqa: BLE001
                res = {"key": j[0], "which": j[1], "cls": "ERROR", "ops": [], "err": f"{type(e).__name__}: {str(e)[:120]}"}
            fh.write(json.dumps(res) + "\n")
            if (i + 1) % 250 == 0:
                fh.flush()
                el = time.time() - t0
                logger.info(f"typing {i + 1}/{len(todo)} {el:.0f}s (eta {(len(todo) - i - 1) * el / (i + 1) / 60:.1f} min)")
    logger.info(f"typing done {time.time() - t0:.0f}s")


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(ROOT / "logs" / "csc_typing.log", rotation="30 MB", level="DEBUG")
    main(sys.argv)
