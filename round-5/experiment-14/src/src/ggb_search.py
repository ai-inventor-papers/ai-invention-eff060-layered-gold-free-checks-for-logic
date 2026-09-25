#!/usr/bin/env python3
"""GG_B (SECONDARY, prereg_gg map_family 'SECONDARY GG_B'): dataset-5 freelab full map family (units incl. B1 reification /
B2 de-reification, B3 merge, B4 split, B5 lexical negation, binary relations either argument order, constants) on every
E non-exact node pair that PRIMARY GG does NOT accept (PRIMARY-accepted pairs stay accepted). Direction i -> j first,
then j -> i; up to 5 equivalence maps kept; caps 2e4 maps / 10 s per direction (cap = not agreeing, counted).
Non-identity map entries are then glossed with the same checker + prompt gloss_gg_v2 (item: A = candidate symbol use,
B = its image under the map). Writes results/ggb_search.jsonl. Usage: ggb_search.py pilot | all"""
from __future__ import annotations

import json
import multiprocessing as mp
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

from common import MATRIX, RES, ROOT, jl, sha1, setup_logger

logger = setup_logger("ggb_search")
OUT = RES / "ggb_search.jsonl"
FL_PATHS = [ROOT / "lib" / "vendor" / "dataset5_freelab" / "src", ROOT / "lib" / "vendor" / "dataset5_freelab" / "vendor"]
MAX_MAPS, MAX_SECS, KEEP = 20_000, 10.0, 5


def build_tasks() -> list[dict]:
    import gg_score as GS
    from labels import frame
    df = frame()
    searched = set(df[df.Z].sentence_id)
    S = GS.load_search()
    verdicts = json.loads((RES / "gg_verdicts.json").read_text())
    tasks = []
    for r in jl(MATRIX):
        sid = r["sentence_id"]
        if sid not in searched:
            continue
        fol = {nd["node_id"]: nd["canon_fol"] for nd in r["nodes"]}
        jobs = []
        for i, j, eq, kind, _s in r["pairs"]:
            if kind == "exact":
                continue
            ok, _, _, _ = GS.decide(S.get(f"E|{sid}|{i}|{j}"), sid, verdicts)
            if not ok:
                jobs.append({"id": f"E|{sid}|{i}|{j}", "a": fol[i], "b": fol[j]})
        if jobs:
            tasks.append({"sid": sid, "jobs": jobs})
    return sorted(tasks, key=lambda t: sha1("GGB|" + t["sid"]))


def _entries(m, cand, rd, FL) -> list[list]:
    """Non-identity entries of one freelab map as (kind, a_display, b_display)."""
    out = []
    for a, b in FL.map_to_json(m["assign"], m["cmap"], cand, rd).items():
        if b in ("<fresh>", "<free>"):
            continue
        if a.startswith("const:"):
            c = a[6:]
            if c.lower() != b.lower():
                out.append(["const", c, b])
            continue
        if "/" in a and "(" not in a:  # relation key 'Name/2' -> target 'Rel(x, y)' or 'Rel(y, x)'
            nm = a.split("/")[0]
            if not (b.lower() == f"{nm.lower()}(x, y)"):
                out.append(["rel", f"{nm}(x, y)", b])
            continue
        if a.lower() != b.lower():
            out.append(["unit", a, b])
    return out


def work(task: dict) -> list[dict]:
    import resource
    resource.setrlimit(resource.RLIMIT_AS, (3 * 1024 ** 3, 3 * 1024 ** 3))
    for p in FL_PATHS:
        sys.path.insert(0, str(p))
    sys.setrecursionlimit(20000)
    import freelab as FL
    cands, rds = {}, {}

    def get(cache, cls, s):
        if s not in cache:
            try:
                cache[s] = cls(s)
            except (ValueError, IndexError, TypeError, KeyError, RecursionError) as ex:
                cache[s] = ex
        return cache[s]
    out = []
    for j in task["jobs"]:
        t0 = time.time()
        rec = {"id": j["id"], "sid": task["sid"], "status": "NO_MAP", "maps": [], "n_maps": 0, "capped": False, "z3_unknown": 0}
        for direction, (x, y) in (("a->b", (j["a"], j["b"])), ("b->a", (j["b"], j["a"]))):
            cand, rd = get(cands, FL.Candidate, x), get(rds, FL.Reading, y)
            if isinstance(cand, Exception) or isinstance(rd, Exception):
                rec["status"] = "ERROR:" + type(cand if isinstance(cand, Exception) else rd).__name__
                break
            try:
                r = FL.search(cand, rd, max_maps=MAX_MAPS, max_secs=MAX_SECS, keep_equiv=KEEP)
            except (MemoryError, RecursionError, ValueError, KeyError, IndexError) as ex:
                rec["status"] = "ERROR:" + type(ex).__name__
                break
            rec["n_maps"] += r["n_maps_enumerated"]
            rec["capped"] |= r["capped"]
            rec["z3_unknown"] += r["z3_unknown"]
            if r["n_equiv"] > 0:
                rec["status"] = "MAPPED"
                rec["direction"] = direction
                rec["maps"] = [{"entries": _entries(m, cand, rd, FL), "bridges": FL.bridges_of(m["assign"], cand, rd), "image": m["image"]}
                               for m in r["equiv_maps"][:KEEP]]
                break
        if rec["status"] == "NO_MAP" and rec["capped"]:
            rec["status"] = "CAPPED"
        rec["secs"] = round(time.time() - t0, 3)
        out.append(rec)
    return out


@logger.catch(reraise=True)
def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "pilot"
    tasks = build_tasks()
    logger.info(f"{len(tasks)} sentences, {sum(len(t['jobs']) for t in tasks)} pairs not accepted by PRIMARY GG")
    out = OUT if mode == "all" else RES / "ggb_search_pilot.jsonl"
    if mode == "pilot":
        flat = sorted([(t["sid"], j) for t in tasks for j in t["jobs"]], key=lambda x: sha1("pilot|" + x[1]["id"]))[:200]
        by = {}
        for sid, j in flat:
            by.setdefault(sid, {"sid": sid, "jobs": []})["jobs"].append(j)
        tasks = list(by.values())
        if out.exists():
            out.unlink()
    done = {r["id"] for r in jl(out)} if out.exists() else set()
    tasks = [t for t in ({**t, "jobs": [j for j in t["jobs"] if j["id"] not in done]} for t in tasks) if t["jobs"]]
    workers = int(os.environ.get("GG_WORKERS", "6"))
    t0 = time.time()
    n = 0
    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn")) as ex, out.open("a") as fh:
        futs = {ex.submit(work, t): t["sid"] for t in tasks}
        for k, f in enumerate(as_completed(futs)):
            try:
                res = f.result()
            except Exception as e:  # noqa: BLE001 - crashed task logged, resumable
                logger.error(f"task {futs[f]} failed: {type(e).__name__}: {str(e)[:200]}")
                continue
            for r in res:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
            fh.flush()
            n += len(res)
            if (k + 1) % 20 == 0:
                logger.info(f"{k + 1}/{len(tasks)} sentences, {n} pairs, {time.time() - t0:.0f}s")
    logger.info(f"done {n} pairs in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
