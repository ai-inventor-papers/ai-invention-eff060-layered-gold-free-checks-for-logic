#!/usr/bin/env python3
# NOTE (published copy): this file names server paths this repository
# does not publish (a stage it does not ship, or another run's workspace),
# so the steps that read them will not run from a clone as written:
#   /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_6
"""S4_local for PERTURB (labelled DEVIATION D-S4FULL): exp 6's S4 local feature stack refitted ONCE on all E R_AB rows
(no OOF folds exist for PERTURB rows), written to results/s4_perturb_coefs.json BEFORE any PERTURB label is read.

Feature set = exp 6 S4_local minus (a) pilot_rerun_jacc (no rerun analogue for PERTURB rows) and (b) the *_orig judge
columns (the PERTURB judge arm is disguised-only, per the plan). Convention (exp 6 s4.py): status 'fail' -> fail_fill value,
missing -> NaN -> 0 after standardisation + a missing-indicator column; LogisticRegression(C=1.0).
Threshold: matched FA 0.10 (fractional ties) on the in-sample E R_AB CORRECT scores.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from sklearn.linear_model import LogisticRegression

sys.path.insert(0, str(Path(__file__).resolve().parent))
import an_common as C  # noqa: E402
import stats as ST  # noqa: E402

E6 = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_6")
FEATS = ["parse_fail", "pilot_joint_conflict", "pilot_arity_incons", "pilot_shape_incons", "pilot_dangling",
         "rt_nli_min_local", "rt_nli_fwd_local", "rt_nli_bwd_local", "rt_nli_contra_local", "rt_embed_cos_local",
         "judge_local_qwen8b_disg", "judge_local_llama8b_disg", "sc5_local_eq_frac", "sc5_local_entropy"]


def e6_features() -> dict:
    """exp 6 E_baseline_features keyed by dataset-E row_key (item_id|prompt_variant; exp 6's own row_key differs)."""
    return {r["item_id"] + "|" + r["sysvar"].split("|")[-1]: r for r in C.jl(E6 / "E_baseline_features.jsonl")}


def matrix(rows: list[dict], feats: list[str], fail_fill: dict, names_fixed: list[str] | None = None):
    X, names = [], []
    for f in feats:
        v = np.array([(fail_fill.get(f, 1.0) if r.get(f + "__status") == "fail" else
                       (np.nan if r.get(f) is None else r[f])) for r in rows], dtype=float)
        X.append(v)
        names.append(f)
        miss = np.isnan(v)
        if (names_fixed is None and miss.any()) or (names_fixed is not None and f + "__missing" in names_fixed):
            X.append(miss.astype(float))
            names.append(f + "__missing")
    return np.vstack(X).T, names


def apply(model: dict, rows: list[dict]) -> np.ndarray:
    X, names = matrix(rows, model["features"], model["fail_fill"], names_fixed=model["names"])
    assert names == model["names"], (names, model["names"])
    Z = np.nan_to_num((X - np.array(model["mu"])) / np.array(model["sd"]))
    s = Z @ np.array(model["coef"]) + model["intercept"]
    return 1 / (1 + np.exp(-s))


def main():
    C.guard()
    meta = json.loads((E6 / "results" / "feature_meta.json").read_text())
    ff = meta["fail_fill"]
    feat = e6_features()
    lab = {r["row_key"]: r for r in C.jl(C.DATA / "exp5" / "E_labels.jsonl")}
    rows, y = [], []
    for k, r in feat.items():
        yy = C.E_regime(lab[k], "R_AB")
        if yy is not None:
            rows.append(r)
            y.append(yy)
    y = np.array(y)
    X, names = matrix(rows, FEATS, ff)
    mu = np.nanmean(X, 0)
    mu = np.where(np.isnan(mu), 0, mu)
    sd = np.nanstd(X, 0)
    sd = np.where((sd == 0) | np.isnan(sd), 1, sd)
    Z = np.nan_to_num((X - mu) / sd)
    clf = LogisticRegression(C=1.0, max_iter=5000).fit(Z, y)
    p = clf.predict_proba(Z)[:, 1]
    thr = ST.matched_fa(p[y == 0], 0.10)
    model = {"features": FEATS, "names": names, "fail_fill": {f: ff.get(f, 1.0) for f in FEATS}, "mu": mu.tolist(),
             "sd": sd.tolist(), "coef": clf.coef_[0].tolist(), "intercept": float(clf.intercept_[0]), "C": 1.0,
             "n_train": int(len(y)), "n_error": int(y.sum()), "in_sample_auroc": ST.auc_fast(y, p),
             "threshold_FA0.10_E_RAB_correct": {"t": thr[0], "lambda": thr[1]},
             "note": "DEVIATION D-S4FULL: one full-E fit (no OOF for PERTURB); judge/round-trip inputs on PERTURB are nf4 "
                     "(D-GPU16) while this fit used exp 6's bf16 E features; secondary threshold on PERTURB controls reported."}
    assert np.allclose(apply(model, rows), p)
    (C.RES / "s4_perturb_coefs.json").write_text(json.dumps(model, indent=1))
    print(json.dumps({k: v for k, v in model.items() if k in ("n_train", "n_error", "in_sample_auroc", "threshold_FA0.10_E_RAB_correct")}))


if __name__ == "__main__":
    main()
