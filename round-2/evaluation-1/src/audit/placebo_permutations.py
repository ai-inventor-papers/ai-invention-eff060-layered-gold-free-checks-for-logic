#!/usr/bin/env python3
"""Placebo characterisation for the cross-fitted PT: 20 label permutations per regime (same items, same sentence groups).
Reports the null distribution of AUROC(PT_oof), AUROC(judge) and their difference, so the observed PT-judge Delta can be read
against its permutation null (a cross-fitted model on permuted labels is biased BELOW 0.5 by fold-prevalence anti-learning)."""
import json, runpy, sys
from pathlib import Path
import numpy as np
sys.argv = ["x"]
WS = Path(__file__).resolve().parent.parent
g = runpy.run_path(str(WS / "audit/rederive_headlines.py"), run_name="lib")
out = {}
for rn in ("R_SOLVER_CONS", "R_ADJ_AB"):
    R = g["regime"](rn); keys = sorted(R)
    y = np.array([R[k]["y"] for k in keys]); glab = np.array([R[k]["cluster"] for k in keys])
    X = np.column_stack([[R[k][m] for k in keys] for m in ("c_score", "bow_uncarried", "l3_score")])
    j = np.array([R[k]["judge_cheap_disg"] for k in keys])
    rng = np.random.default_rng(7); pa, pj, dd = [], [], []
    for _ in range(20):
        yp = rng.permutation(y); o = g["pt_oof"](X, yp, glab)
        pa.append(g["mw_auc"](yp, o)); pj.append(g["mw_auc"](yp, j)); dd.append(pa[-1] - pj[-1])
    obs = g["mw_auc"](y, g["pt_oof"](X, y, glab)) - g["mw_auc"](y, j)
    out[rn] = {"null_auroc_PT_mean": float(np.mean(pa)), "null_auroc_PT_sd": float(np.std(pa)), "null_auroc_judge_mean": float(np.mean(pj)),
               "null_delta_mean": float(np.mean(dd)), "null_delta_max": float(np.max(dd)), "observed_delta": float(obs),
               "observed_exceeds_all_20_null_deltas": bool(obs > np.max(dd))}
(WS / "audit/placebo_permutations.json").write_text(json.dumps(out, indent=1)); print(json.dumps(out, indent=1))
