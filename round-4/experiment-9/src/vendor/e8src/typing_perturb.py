#!/usr/bin/env python3
"""STEP 6 PART C: gold-free error-type identification on PERTURB mutants of E bases (the only ones with peers).

For each mutant M:
  PEER typing   : minimal typed repair (exp C repair_census: align vocabulary -> VOCAB/GRAN bridge -> BFS depth <= 2 over
                  typed edits, z3-verified, 10 s budget) of M towards the peer MEDOID. No variant was frozen by the
                  selection rule (neither eligible), so per the prereg the medoid is the ALIGN (eqmv) medoid of the full peer
                  pool (secondary: the HYB medoid).
  ORACLE typing : the same search towards the TRUE base reference (separates 'weak typer' from 'wrong medoid').
  JUDGE typing  : flash-lite error_type (rubric A JSON, disguised) and local Qwen3-8B type (nf4, disguised), if present.
Predicted PERTURB operator = mapped repair op (prereg typing_operator_map: a repair maps the MUTANT back, so DROP->ADD,
ADD->DROP, others identity); strict = the single op of a depth-1 repair; lenient = true op among the mapped ops of the repair.
Baselines: majority class and marginal-draw chance. Outputs: results/typing.csv, results/typing_confusion.csv,
results/typing_rows.jsonl, results/analysis_typing.json.
"""
from __future__ import annotations

import csv
import json
import multiprocessing as mp
import os
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
from loguru import logger

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"
RES = ROOT / "results"
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "typing_perturb.log", rotation="30 MB", level="DEBUG")

BUDGET_S = 10.0


def typed_repair(args):
    """(key, which, mutant_str, target_str) -> repair record (exp C repair_census.work logic, 10 s budget)."""
    key, which, m, t = args
    sys.path.insert(0, str(SRC / "vendor_c"))
    sys.setrecursionlimit(10000)
    import repair_census as RC
    from fol import equivalent, parse
    t0 = time.time()
    try:
        me, te = parse(m), parse(t)
    except Exception as e:  # noqa: BLE001 - unparseable by the census parser -> recorded
        return {"key": key, "which": which, "cls": "PARSE_FAIL", "err": str(e)[:80], "secs": 0.0}
    try:
        if equivalent(me, te, ms=2000) is True:
            return {"key": key, "which": which, "cls": "EQUIV", "ops": [], "secs": round(time.time() - t0, 2)}
        ao, pmap, cmap = RC.align(me, te)
        if equivalent(ao, te, ms=2000) is True:
            return {"key": key, "which": which, "cls": "VOCAB", "ops": ["RENAME"] if pmap else [], "secs": round(time.time() - t0, 2)}
        gb = RC.gran_bridge(ao, te)
        if gb and equivalent(gb[0], gb[1], ms=2000) is True:
            return {"key": key, "which": which, "cls": "GRAN", "ops": [], "secs": round(time.time() - t0, 2)}
        base, tgt = (gb if gb else (ao, te))
        ops, dt = RC.search(base, tgt, budget_s=BUDGET_S)
        return {"key": key, "which": which, "cls": "+".join(ops) if ops else ("TIMEOUT_OR_COMPOUND"),
                "ops": ops or [], "secs": round(time.time() - t0, 2), "renamed": bool(pmap)}
    except Exception as e:  # noqa: BLE001
        return {"key": key, "which": which, "cls": "ERROR", "err": str(e)[:80], "ops": [], "secs": round(time.time() - t0, 2)}


def main():
    sys.path.insert(0, str(SRC))
    import an_common as C
    pp = C.guard("prereg_perturb")
    MAP = pp["typing_operator_map"]["repair ops -> PERTURB operator"]
    cons = C.load_scores("E")
    rows = [r for r in C.jl(C.DATA / "perturb_rows.jsonl") if r["fold"] == "PERTURB" and r["base_source"] != "RCOMP"]
    jc = {r["key"]: r for r in C.jl(RES / "perturb_scores" / "judge_cheap_disg.jsonl")}
    jq = {r["key"].rsplit("|", 1)[0]: r for r in C.jl(RES / "perturb_scores" / "judge_local_qwen8b_nf4.jsonl") if r["key"].endswith("|disg")}
    outp = RES / "typing_rows.jsonl"
    done = {(r["key"], r["which"]) for r in C.jl(outp)}
    jobs = []
    for r in rows:
        k = "PT:" + r["item_id"]
        c = cons.get(k, {})
        for which, tgt in (("oracle", r["reference_fol"]), ("medoid_align", c.get("medoid_align")), ("medoid_hyb", c.get("medoid_hyb"))):
            if tgt and (k, which) not in done:
                jobs.append((k, which, r["candidate_fol"], tgt))
    if len(sys.argv) > 1 and sys.argv[1] == "--mini":
        jobs = jobs[:60]
    logger.info(f"typing jobs: {len(jobs)} (rows {len(rows)})")
    t0 = time.time()
    nw = max(1, len(os.sched_getaffinity(0)) - 2)
    with ProcessPoolExecutor(max_workers=nw, mp_context=mp.get_context("spawn")) as ex, outp.open("a") as fh:
        for i, res in enumerate(ex.map(typed_repair, jobs, chunksize=4)):
            fh.write(json.dumps(res) + "\n")
            if (i + 1) % 500 == 0:
                fh.flush()
                logger.info(f"typing {i + 1}/{len(jobs)} {time.time() - t0:.0f}s")
    if len(sys.argv) > 1 and sys.argv[1] == "--mini":
        return
    # ------------------------------------------------ scoring
    R = defaultdict(dict)
    for x in C.jl(outp):
        R[x["key"]][x["which"]] = x
    ops_true = Counter(r["operator"] for r in rows)
    maj = ops_true.most_common(1)[0][0]
    chance = sum((v / len(rows)) ** 2 for v in ops_true.values())
    out, conf = [], Counter()
    per = []
    for r in rows:
        k = "PT:" + r["item_id"]
        true = r["operator"]
        rec = {"key": k, "true": true, "true_fine": r["op_fine"], "polarity": r["polarity"], "base": r["base_item_id"]}
        for which in ("medoid_align", "medoid_hyb", "oracle"):
            x = R[k].get(which)
            if x is None:
                rec[f"{which}_pred"] = "NO_MEDOID"
                rec[f"{which}_lenient"] = False
                continue
            mapped = [MAP.get(o, o) for o in x.get("ops", [])]
            if x["cls"] in ("EQUIV",):
                pred = "NONE(equivalent)"
            elif x["cls"] == "VOCAB":
                pred = "MEANING_RENAME" if x.get("ops") else "NONE(vocab)"
            elif not mapped:
                pred = "UNREPAIRABLE" if x["cls"] not in ("PARSE_FAIL", "ERROR") else x["cls"]
            else:
                pred = mapped[0] if len(mapped) == 1 else "+".join(sorted(mapped))
            rec[f"{which}_pred"] = pred
            rec[f"{which}_strict"] = pred == true
            rec[f"{which}_lenient"] = true in (mapped or ([pred] if pred == "MEANING_RENAME" else []))
            rec[f"{which}_found"] = bool(mapped) or x["cls"] == "VOCAB"
            rec[f"{which}_secs"] = x.get("secs")
            conf[(which, true, pred)] += 1
        j = jc.get(k) or {}
        rec["judge_cheap_pred"] = j.get("type")
        rec["judge_cheap_strict"] = (j.get("type") == true) or (true == "MEANING_RENAME" and False)
        q = jq.get(k) or {}
        rec["judge_local_pred"] = q.get("type")
        rec["judge_local_strict"] = q.get("type") == true
        per.append(rec)
    import an_common as C2  # noqa: F401
    import stats as ST
    tab = []
    for op in sorted(ops_true) + ["ALL"]:
        rs = [p for p in per if op == "ALL" or p["true"] == op]
        row = {"operator": op, "n": len(rs), "majority_baseline": float(np.mean([p["true"] == maj for p in rs])), "majority_class": maj,
               "marginal_chance_overall": chance}
        for which in ("medoid_align", "medoid_hyb", "oracle"):
            for kind in ("strict", "lenient"):
                v = np.array([bool(p.get(f"{which}_{kind}")) for p in rs], float)
                m, ci = ST.cluster_boot_mean(v, [p["base"] for p in rs], b=1000)
                row[f"{which}_{kind}_acc"] = m
                row[f"{which}_{kind}_ci"] = ci
            row[f"{which}_repair_found_rate"] = float(np.mean([bool(p.get(f"{which}_found")) for p in rs]))
        for jn in ("judge_cheap", "judge_local"):
            have = [p for p in rs if p.get(f"{jn}_pred")]
            row[f"{jn}_n"] = len(have)
            if have:
                v = np.array([bool(p[f"{jn}_strict"]) for p in have], float)
                m, ci = ST.cluster_boot_mean(v, [p["base"] for p in have], b=1000)
                row[f"{jn}_acc"], row[f"{jn}_ci"] = m, ci
        tab.append(row)
    allrow = tab[-1]
    verdict = {}
    for which in ("medoid_align", "medoid_hyb", "judge_cheap", "judge_local"):
        ci = allrow.get(f"{which}_strict_ci") or allrow.get(f"{which}_ci")
        verdict[which] = {"acc": allrow.get(f"{which}_strict_acc", allrow.get(f"{which}_acc")), "ci": ci,
                          "above_majority": bool(ci and ci[0] is not None and ci[0] > allrow["majority_baseline"]),
                          "above_chance": bool(ci and ci[0] is not None and ci[0] > chance)}
    neg = not any(v["above_majority"] for k, v in verdict.items() if k.startswith("medoid"))
    A = {"n_mutants": len(per), "majority_class": maj, "majority_acc": allrow["majority_baseline"], "marginal_chance": chance,
         "verdict": verdict, "oracle_strict_acc": allrow["oracle_strict_acc"], "oracle_lenient_acc": allrow["oracle_lenient_acc"],
         "negative_statement": ("no gold-free metric here identifies error type (peer-medoid typing CI overlaps the majority baseline); "
                                "the oracle row shows the typer's ceiling") if neg else "peer-medoid typing beats the majority baseline",
         "timeouts": dict(Counter(x["cls"] for v in R.values() for x in v.values() if x["cls"] in ("TIMEOUT_OR_COMPOUND", "PARSE_FAIL", "ERROR")))}
    (RES / "analysis_typing.json").write_text(json.dumps(A, indent=1))
    with (RES / "typing.csv").open("w", newline="") as fh:
        keys = list(tab[0].keys())
        for t in tab:
            for k in t:
                if k not in keys:
                    keys.append(k)
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        for t in tab:
            w.writerow(t)
    with (RES / "typing_confusion.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["typer", "true_operator", "predicted", "n"])
        for (which, t, p), n in sorted(conf.items()):
            w.writerow([which, t, p, n])
    with (RES / "typing_per_row.jsonl").open("w") as fh:
        for p in per:
            fh.write(json.dumps(p) + "\n")
    logger.info(f"typing verdict: {json.dumps(A)[:800]}")


if __name__ == "__main__":
    main()
