#!/usr/bin/env python3
"""Fallback (10) of the plan: the 10 s typed-repair search timed out on > 30% of mutants for the peer medoid (52%), so the
search is re-run with a 20 s budget on a 500-mutant sha1-ordered sample (medoid_align + oracle); typing accuracy is reported
on that sample (results/typing_s20.json) next to the 10 s numbers on the same sample."""
import hashlib
import json
import multiprocessing as mp
import os
import sys
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import typing_perturb as TP  # noqa: E402


def job(a):
    TP.BUDGET_S = 20.0
    return TP.typed_repair(a)


def main():
    import an_common as C
    import stats as ST
    pp = C.guard("prereg_perturb")
    MAP = pp["typing_operator_map"]["repair ops -> PERTURB operator"]
    cons = C.load_scores("E")
    rows = [r for r in C.jl(C.DATA / "perturb_rows.jsonl") if r["fold"] == "PERTURB" and r["base_source"] != "RCOMP"
            and cons.get("PT:" + r["item_id"], {}).get("medoid_align")]
    rows = sorted(rows, key=lambda r: hashlib.sha1(r["item_id"].encode()).hexdigest())[:500]
    outp = C.RES / "typing_rows_s20.jsonl"
    done = {(x["key"], x["which"]) for x in C.jl(outp)}
    jobs = [(k, w, r["candidate_fol"], t) for r in rows for k in ["PT:" + r["item_id"]]
            for w, t in (("medoid_align", cons[k]["medoid_align"]), ("oracle", r["reference_fol"])) if (k, w) not in done]
    with ProcessPoolExecutor(max_workers=max(1, len(os.sched_getaffinity(0)) - 2), mp_context=mp.get_context("spawn")) as ex, outp.open("a") as fh:
        for res in ex.map(job, jobs, chunksize=2):
            fh.write(json.dumps(res) + "\n")
    R20 = {(x["key"], x["which"]): x for x in C.jl(outp)}
    R10 = {(x["key"], x["which"]): x for x in C.jl(C.RES / "typing_rows.jsonl")}

    def pred(x):
        mapped = [MAP.get(o, o) for o in (x or {}).get("ops", [])]
        return mapped[0] if len(mapped) == 1 else ("+".join(sorted(mapped)) if mapped else "NONE")
    out = {"n": len(rows)}
    for tag, RR in (("budget10", R10), ("budget20", R20)):
        for w in ("medoid_align", "oracle"):
            acc = np.array([pred(RR.get(("PT:" + r["item_id"], w))) == r["operator"] for r in rows], float)
            to = np.mean([(RR.get(("PT:" + r["item_id"], w)) or {}).get("cls") == "TIMEOUT_OR_COMPOUND" for r in rows])
            m, ci = ST.cluster_boot_mean(acc, [r["base_item_id"] for r in rows])
            out[f"{tag}_{w}"] = {"acc": m, "ci": ci, "timeout_or_compound_share": float(to)}
    maj = Counter(r["operator"] for r in rows).most_common(1)[0]
    out["majority"] = {"class": maj[0], "acc": maj[1] / len(rows)}
    (C.RES / "typing_s20.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
