#!/usr/bin/env python3
"""Testing plan 8: the copied exp-6 statistics core (exp6src/src/api_bar.py) reproduces iteration-3 T1's L25 delta
(c_score_align - flash-lite disguised, strat AUROC, R_AB, E_POOL; power_E2.json observed_delta 0.06942) from
exp 6's per_item_T1.jsonl. -> e2b/T1_repro_check.json"""
import json
import sys
from pathlib import Path

import numpy as np

WS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WS / "exp6src"))
from src import api_bar as AB  # noqa: E402

T1 = Path("../../../../round-3/experiment-6/src/results/per_item_T1.jsonl")
rows = [json.loads(l) for l in T1.read_text().splitlines() if l.strip()]
out = {}
for cell, strata in (("L25", ("L25",)), ("long", ("L25", "L20", "EXC"))):
    R = [r for r in rows if r["in_R_AB"] and r["pool"] == "E_POOL" and r["source_stratum"] in strata
         and r.get("c_score_align") is not None and r.get("judge_cheap_disg") is not None]
    y = np.array([r["y_R_AB"] for r in R])
    a = np.array([r["c_score_align"] for r in R], float)
    b = np.array([r["judge_cheap_disg"] for r in R], float)
    h = np.array([r["source_stratum"] for r in R])
    cb = AB.ClusterBoot([r["sentence_id"] for r in R], b=1000, seed=0)
    d = AB.paired_boot(y, a, b, cb, "strat", h)
    out[cell] = {"n": len(R), "delta": d["delta"], "ci": d["ci"], "se": d["se"],
                 "judge_fail_status_rows": sum(r.get("judge_cheap_disg__status") == "fail" for r in R)}
out["expected"] = {"L25": 0.06942089474370672, "long": 0.11625879215576673, "source": "iter_4 evaluation_3 power_E2.json observed_delta"}
out["L25_reproduced"] = abs(out["L25"]["delta"] - 0.06942089474370672) < 1e-6
out["long_reproduced"] = abs(out["long"]["delta"] - 0.11625879215576673) < 1e-6
(WS / "e2b" / "T1_repro_check.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out))
