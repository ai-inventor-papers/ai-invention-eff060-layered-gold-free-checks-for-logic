#!/usr/bin/env python3
"""Independent re-derivation of the headline numbers of eval.py, through a DIFFERENT code path.

Reads the raw iteration-1 per-item files directly (not eval_out.json, not src/*):
  - AUROC via scipy Mann-Whitney U (not sklearn roc_auc_score);
  - bootstrap via explicit index resampling with python `random` over sentence groups (not the weight-matrix bootstrap);
  - PT via sklearn Pipeline(StandardScaler, LogisticRegression) with sklearn GroupKFold by sentence (not exp D's fold ids);
  - matched-FA recall via sklearn roc_curve + np.interp (not the randomised-threshold rule).
Placebos: permuted labels (within the same items) must give AUROC ~0.5 and a PT-judge CI that includes 0.
Writes audit/rederive_headlines.json and compares with eval_out.json metrics_agg.
"""
from __future__ import annotations

import json
import random
import re
from pathlib import Path

import numpy as np
from scipy.stats import mannwhitneyu
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_curve
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

WS = Path(__file__).resolve().parent.parent
GA = Path(__file__).resolve().parents[4] / "round-1"
BIN = ("CORRECT", "ERROR")


def rj(p):
    return [json.loads(l) for l in open(p) if l.strip()]


def fl(v):
    try:
        return float(v) if v is not None else None
    except (TypeError, ValueError):
        return None


def clus(t):  # same key definition as exp D, re-typed
    t = (t or "").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("–", "-").replace("—", "-").replace("−", "-").lower()
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", t)).strip()


def mw_auc(y, s):
    y, s = np.asarray(y), np.asarray(s, float)
    u = mannwhitneyu(s[y == 1], s[y == 0], alternative="two-sided").statistic
    return u / ((y == 1).sum() * (y == 0).sum())


# ---------------------------------------------------------------- raw load
A = {r["item_id"]: r for r in rj(GA / "experiment-1/src/results/per_item.jsonl") if r["track"] == "L"}
labA = {r["item_id"]: r["label"] for r in json.load(open(GA / "experiment-1/src/screen_items.json"))}
C = {r["item_id"]: r for r in rj(GA / "experiment-3/src/results/analysis_table.jsonl") if r["track"] == "L"}
D = {r["item_id"]: r for r in rj(GA / "experiment-4/src/results/per_item_scores.jsonl") if r["track"] == "L"}
E = json.load(open(GA / "dataset-1/src/screen_adjudicated_labels.json"))

A_M = ["p_fused_H", "bow_uncarried", "l3_score", "n_smells", "role_count"]
C_M = ["c_score", "c_score_peers6", "medoid_depth", "cluster_entropy", "sc5_cheap"]
D_M = ["judge_cheap_disg", "judge_cheap_orig", "judge_cheap2_disg", "judge_cheap2_orig", "rt_nli_min", "rt_nli_min_localverb",
       "rt_embed_cos", "parse_fail", "pilot_rerun_jacc", "pilot_joint_conflict"]


def row(k):
    a, c, d = A.get(k), C.get(k), D.get(k)
    if not (a and c and d):
        return None
    r = {m: fl(a.get(m)) for m in A_M}
    ok = str(a.get("parse_ok")) == "True" and a.get("cpu_status") == "OK"
    r["l2_bow_Adef"] = ((fl(a.get("bow_n_unanch")) or 0.0) + (fl(a.get("bow_uncarried")) or 0.0)) if ok else None
    r.update({m: fl(c.get(m)) for m in C_M})
    r.update({m: fl(d["oriented_scores"].get(m)) for m in D_M})
    if any(v is None for v in r.values()):
        return None
    r["cluster"] = clus(a["text"])
    return r


def regime(name):
    out = {}
    for k in set(A) | set(C) | set(D) | set(E):
        if name == "R_SOLVER_CONS":
            la, lc, ld = labA.get(k), (C.get(k) or {}).get("label"), (D.get(k) or {}).get("label")
            if not (k in A and k in C and k in D and la == lc == ld and la in BIN):
                continue
            y = int(la == "ERROR")
        else:  # R_ADJ_AB
            e = E.get(k)
            if not e or e["track"] != "L" or e["label_tier"] not in ("A", "B") or e["final_label"] not in BIN or e.get("reading_choice"):
                continue
            y = int(e["final_label"] == "ERROR")
        r = row(k)
        if r is not None:
            r["y"] = y
            out[k] = r
    return out


def boot_groups(keys, R):
    g = {}
    for i, k in enumerate(keys):
        g.setdefault(R[k]["cluster"], []).append(i)
    return list(g.values())


def boot_delta(y, s1, s2, groups, B=2000, seed=11):
    rng = random.Random(seed)
    d = []
    for _ in range(B):
        ii = [i for gi in rng.choices(groups, k=len(groups)) for i in gi]
        yy = y[ii]
        if yy.min() == yy.max():
            continue
        d.append(mw_auc(yy, s1[ii]) - mw_auc(yy, s2[ii]))
    return float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))


def pt_oof(X, y, groups_lab, seed=0):
    oof = np.zeros(len(y))
    for tr, te in GroupKFold(n_splits=5).split(X, y, groups_lab):
        m = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=5000)).fit(X[tr], y[tr])
        oof[te] = m.predict_proba(X[te])[:, 1]
    return oof


res = {}
agg = json.load(open(WS / "eval_out.json"))["metrics_agg"]
for rn in ("R_SOLVER_CONS", "R_ADJ_AB"):
    R = regime(rn)
    keys = sorted(R)
    y = np.array([R[k]["y"] for k in keys])
    S = lambda m: np.array([R[k][m] for k in keys])  # noqa: E731
    groups = boot_groups(keys, R)
    glab = np.array([R[k]["cluster"] for k in keys])
    out = {"n": len(keys), "n_err": int(y.sum()), "n_sent": len(groups)}
    for m in ("judge_cheap_disg", "c_score", "p_fused_H", "bow_uncarried", "l3_score"):
        out[f"auroc_{m}"] = mw_auc(y, S(m))
    X = np.column_stack([S("c_score"), S("bow_uncarried"), S("l3_score")])
    pt = pt_oof(X, y, glab)
    out["auroc_PT_groupkfold"] = mw_auc(y, pt)
    out["delta_PT_minus_judge"] = out["auroc_PT_groupkfold"] - out["auroc_judge_cheap_disg"]
    out["delta_PT_minus_judge_ci"] = boot_delta(y, pt, S("judge_cheap_disg"), groups)
    out["delta_fusedH_minus_judge"] = out["auroc_p_fused_H"] - out["auroc_judge_cheap_disg"]
    out["delta_fusedH_minus_judge_ci"] = boot_delta(y, S("p_fused_H"), S("judge_cheap_disg"), groups)
    # matched-FA 0.10 recall orig vs disg (roc_curve interpolation)
    for j in ("judge_cheap_orig", "judge_cheap_disg"):
        fpr, tpr, _ = roc_curve(y, S(j))
        out[f"recall_FA010_{j}"] = float(np.interp(0.10, fpr, tpr))
    # placebo: permuted labels (same items, same groups)
    rng = np.random.default_rng(123)
    yp = rng.permutation(y)
    ptp = pt_oof(X, yp, glab)
    out["placebo_auroc_PT"] = mw_auc(yp, ptp)
    out["placebo_auroc_judge"] = mw_auc(yp, S("judge_cheap_disg"))
    out["placebo_delta_PT_minus_judge_ci"] = boot_delta(yp, ptp, S("judge_cheap_disg"), groups, B=1000)
    out["placebo_passes_(CI_includes_0)"] = bool(out["placebo_delta_PT_minus_judge_ci"][0] <= 0 <= out["placebo_delta_PT_minus_judge_ci"][1])
    # comparison with eval.py
    out["eval_py"] = {"n": agg.get(f"regime_{rn}_n"), "auroc_judge": agg.get(f"common_{rn}_auroc_judge_cheap_disg"),
                      "auroc_c_score": agg.get(f"common_{rn}_auroc_c_score"), "auroc_fused_H": agg.get(f"common_{rn}_auroc_p_fused_H"),
                      "auroc_PT_Dfolds": agg.get(f"common_{rn}_auroc_PT_oof"),
                      "delta_PT": agg.get(f"common_{rn}_delta_vs_judge_PT_oof"),
                      "delta_PT_ci": [agg.get(f"common_{rn}_delta_ci_lo_PT_oof"), agg.get(f"common_{rn}_delta_ci_hi_PT_oof")],
                      "delta_fusedH_ci": [agg.get(f"common_{rn}_delta_ci_lo_p_fused_H"), agg.get(f"common_{rn}_delta_ci_hi_p_fused_H")]}
    res[rn] = out
    res[rn + "_R"] = R

# label-only shift on shared items (solver -> A+B)
Rs, Ra = res.pop("R_SOLVER_CONS_R"), res.pop("R_ADJ_AB_R")
shared = sorted(set(Rs) & set(Ra))
ys = np.array([Rs[k]["y"] for k in shared])
ya = np.array([Ra[k]["y"] for k in shared])
lo = {"n_shared": len(shared), "n_label_changes": int((ys != ya).sum())}
for m in ("bow_uncarried", "c_score", "p_fused_H"):
    s = np.array([Rs[k][m] for k in shared])
    lo[m] = mw_auc(ya, s) - mw_auc(ys, s)
    lo[m + "_eval_py"] = agg.get(f"labelshift_R_ADJ_AB_{ {'bow_uncarried': 'L2_bow', 'c_score': 'c_score', 'p_fused_H': 'fused_H'}[m]}")
res["label_only_shift_solver_to_ADJ_AB"] = lo
(WS / "audit" / "rederive_headlines.json").write_text(json.dumps(res, indent=1, default=float))
print(json.dumps(res, indent=1, default=float))
