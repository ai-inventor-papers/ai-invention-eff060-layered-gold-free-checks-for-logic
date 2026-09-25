#!/usr/bin/env python3
"""V4 (label-using by construction): cross-fitted two-channel logistic on (c_exact, c_align = V0 frozen) over Z rows.
Fold k is predicted by a model fit on Z rows of the OTHER folds (asserted); rows outside Z get the full-Z fit; the full-Z
refit gives the frozen coefficients. Writes results/scores_E_V4.jsonl, results/v4_coefs.json, prereg_improve_addendum_v4.json."""
from __future__ import annotations

import json

import numpy as np
from sklearn.linear_model import LogisticRegression

from common import RES, ROOT, jdump, sha256_file, setup_logger, utc
from labels import frame

logger = setup_logger("fit_v4")


def fit(X, y):
    m = LogisticRegression(C=1e6, max_iter=2000).fit(X, y)
    return {"intercept": float(m.intercept_[0]), "c_exact": float(m.coef_[0][0]), "c_align": float(m.coef_[0][1])}


def predict(c, X):
    z = c["intercept"] + c["c_exact"] * X[:, 0] + c["c_align"] * X[:, 1]
    return 1 / (1 + np.exp(-z))


@logger.catch(reraise=True)
def main():
    df = frame()
    df["V0_f"] = df.V0_frozen.astype(float)
    X = df[["c_exact", "V0_f"]].astype(float).values
    Z = df.Z.values
    y = df.y.values
    full = fit(X[Z], y[Z].astype(int))
    pred = predict(full, X)
    folds = {}
    for k in range(5):
        tr = Z & (df.fold.values != k)
        te = Z & (df.fold.values == k)
        assert not (tr & te).any() and set(df.fold.values[tr]) == set(range(5)) - {k}
        c = fit(X[tr], y[tr].astype(int))
        pred[te] = predict(c, X[te])
        folds[k] = {**c, "n_train": int(tr.sum()), "n_test": int(te.sum())}
    out = RES / "scores_E_V4.jsonl"
    with out.open("w") as fh:
        for rk, v, z in zip(df.row_key, pred, Z):
            fh.write(json.dumps({"row_key": rk, "V4": float(v), "V4_oof": bool(z)}) + "\n")
    jdump({"frozen_coefficients_full_Z": full, "per_fold": folds, "features": ["c_exact", "c_align (V0 frozen)"],
           "model": "sklearn LogisticRegression(C=1e6, intercept, lbfgs)", "n_Z": int(Z.sum())}, RES / "v4_coefs.json")
    jdump({"written_utc": utc(), "v4_file": "results/scores_E_V4.jsonl", "v4_sha256": sha256_file(out)}, ROOT / "prereg_improve_addendum_v4.json")
    logger.info(f"V4 frozen coefs {full}; folds {json.dumps(folds)}")


if __name__ == "__main__":
    main()
