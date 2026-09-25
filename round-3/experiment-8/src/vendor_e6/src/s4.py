"""S4: the cross-fitted logistic stack of all cheap baselines on dataset E, and the per-item feature table it is fitted on.

build_feature_table(units, scores) -> list[dict]   one row per E row (all 8,507, all systems), every ORIENTED baseline
                                                   column (higher = more likely unfaithful), a status per column
                                                   ('ok' | 'fail' | 'na'), metadata_fold_E, pool, parse flag.
fit_s4_oof(table, labels, folds, feats, C=1.0)   -> ({row_key: oof_p}, {"coefs": per-fold, "thr": per-fold nested threshold})
    For fold k: fit on the rows of the OTHER folds that carry a label in `labels`; predict ALL rows of fold k (labelled or
    not). Missing / failed values -> 0 after standardisation + a missing-indicator column (exp D combo_oof convention);
    standardisation statistics come from the training folds only. The nested flag threshold of fold k is the training-fit
    score quantile that gives FA = 0.10 on the training CORRECT rows.
Iteration 3 imports fit_s4_oof with R_ADJ labels and nests [S4 + PEER+TEXT] on the identical folds (folds_E.json).
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

FAIL_VALUE = {"count": None}  # counts: FAIL -> max observed (set in build); bounded metrics: FAIL -> 1.0


def _orient(name: str, raw) -> float | None:
    return None if raw is None else float(raw)


def build_feature_table(units: list[dict], cols: dict[str, dict[str, float | None]], status: dict[str, dict[str, str]]) -> list[dict]:
    """cols: {column: {item_id: oriented value or None}}; status: {column: {item_id: 'ok'|'fail'|'na'}} (missing -> 'na')."""
    rows = []
    for u in units:
        r = {"row_key": u["row_key"], "item_id": u["item_id"], "sentence_id": u["sentence_id"], "metadata_fold_E": u["fold_E"],
             "pool": u["pool"], "sysvar": u["sysvar"], "parse_ok": u["parse_ok"], "source_stratum": u["strata"]["source_stratum"]}
        for c, vals in cols.items():
            st = status.get(c, {}).get(u["item_id"], "na")
            v = vals.get(u["item_id"])
            r[c] = None if v is None or (isinstance(v, float) and math.isnan(v)) else float(v)
            r[c + "__status"] = st
        rows.append(r)
    return rows


def _matrix(table: list[dict], feats: list[str], fail_fill: dict[str, float]) -> tuple[np.ndarray, list[str]]:
    X, names = [], []
    for f in feats:
        v = np.array([(fail_fill.get(f, 1.0) if r.get(f + "__status") == "fail" else
                       (np.nan if r.get(f) is None else r[f])) for r in table], dtype=float)
        miss = np.isnan(v)
        X.append(v)
        names.append(f)
        if miss.any():
            X.append(miss.astype(float))
            names.append(f + "__missing")
    return np.vstack(X).T, names


def fit_s4_oof(table: list[dict], labels: dict[str, int], folds: dict[str, int], feats: list[str], C: float = 1.0,
               fail_fill: dict[str, float] | None = None, n_folds: int = 5, fa_target: float = 0.10):
    """-> (oof {row_key: p}, info {coefs, thresholds, flags {row_key: 0/1}, feature_names, n_train})."""
    from sklearn.linear_model import LogisticRegression
    feats = [f for f in feats if any(r.get(f) is not None or r.get(f + "__status") == "fail" for r in table)]
    X, names = _matrix(table, feats, fail_fill or {})
    keys = [r["row_key"] for r in table]
    fold = np.array([folds[k] for k in keys])
    y = np.array([labels.get(k, -1) for k in keys])
    oof = np.full(len(keys), np.nan)
    flags = np.zeros(len(keys), dtype=int)
    coefs, thrs, ntr = [], [], []
    for k in range(n_folds):
        tr = (fold != k) & (y >= 0)
        te = fold == k
        Xtr, Xte = X[tr].copy(), X[te].copy()
        mu = np.nanmean(Xtr, 0)
        mu = np.where(np.isnan(mu), 0, mu)
        sd = np.nanstd(Xtr, 0)
        sd = np.where((sd == 0) | np.isnan(sd), 1, sd)
        Xtr = np.nan_to_num((Xtr - mu) / sd)
        Xte = np.nan_to_num((Xte - mu) / sd)
        if len(np.unique(y[tr])) < 2:
            continue
        clf = LogisticRegression(C=C, max_iter=3000)
        clf.fit(Xtr, y[tr])
        oof[te] = clf.predict_proba(Xte)[:, 1]
        ptr = clf.predict_proba(Xtr)[:, 1]
        thr = float(np.quantile(ptr[y[tr] == 0], 1 - fa_target))
        flags[te] = (oof[te] > thr).astype(int)
        coefs.append({"fold": k, "intercept": float(clf.intercept_[0]), "coef": dict(zip(names, map(float, clf.coef_[0])))})
        thrs.append(thr)
        ntr.append(int(tr.sum()))
    info = {"coefs": coefs, "thresholds": thrs, "flags": dict(zip(keys, flags.tolist())), "feature_names": names,
            "features_used": feats, "n_train_per_fold": ntr, "C": C}
    return {k: (None if np.isnan(p) else float(p)) for k, p in zip(keys, oof)}, info


def write_table(table: list[dict], p: Path) -> None:
    with p.open("w") as f:
        for r in table:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def read_table(p: Path) -> list[dict]:
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]
