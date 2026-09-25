"""Shared statistics (exp 5 analyse_E.py implementations reused verbatim where noted).

auc_fast / matched_fa / flagp / Boot / ci          : exp 5 analyse_E.py verbatim.
strat_auc                                         : exp 5 analyse_E.py strat_auc (within-stratum pairs, weights n1*n0).
fa_recall(neg, pos, t, lam)                       : tie-aware (expected-value) FA / recall at a fractional threshold.
cluster_boot_mean(values, clusters)               : percentile CI of a mean, resampling clusters (sentence or base).
"""
from __future__ import annotations

import math
from collections import defaultdict

import numpy as np
from scipy.stats import rankdata

B = 2000
SEED = 0


def auc_fast(y: np.ndarray, s: np.ndarray) -> float:
    y = np.asarray(y)
    s = np.asarray(s, float)
    n1 = int(y.sum())
    n0 = len(y) - n1
    if n1 == 0 or n0 == 0:
        return float("nan")
    r = rankdata(s)
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def auprc(y, s):
    from sklearn.metrics import average_precision_score
    y = np.asarray(y)
    return float(average_precision_score(y, s)) if 0 < y.sum() < len(y) else float("nan")


def matched_fa(neg_vals, fa: float = 0.10):
    """(t, lam) such that flagging s > t fully and s == t with weight lam gives EXACTLY the target FA on the negatives
    (fractional tie-breaking = expectation of randomized tie-breaking; needed when many CORRECT rows tie at the max)."""
    v = np.asarray(neg_vals, float)
    for t in sorted(set(v.tolist()), reverse=True):
        gt, ge = float(np.mean(v > t)), float(np.mean(v >= t))
        if gt <= fa <= ge:
            return float(t), ((fa - gt) / (ge - gt) if ge > gt else 0.0)
    return float(v.min()), 1.0


def flagp(x: float, t: float, lam: float) -> float:
    return 1.0 if x > t else (lam if x == t else 0.0)


def flag_vec(v, t: float, lam: float) -> np.ndarray:
    v = np.asarray(v, float)
    return np.where(v > t, 1.0, np.where(v == t, lam, 0.0))


def tie_share_at(neg_vals, t: float) -> float:
    v = np.asarray(neg_vals, float)
    return float(np.mean(v == t)) if len(v) else float("nan")


class Boot:
    """Cluster bootstrap index sets (fixed seed; identical resamples for every metric on a subset)."""

    def __init__(self, sids: list[str], b: int = B, seed: int = SEED):
        self.by = defaultdict(list)
        for i, s in enumerate(sids):
            self.by[s].append(i)
        keys = sorted(self.by)
        rng = np.random.default_rng(seed)
        arr = [np.array(self.by[k]) for k in keys]
        self.idx = []
        for _ in range(b):
            pick = rng.integers(0, len(keys), len(keys))
            self.idx.append(np.concatenate([arr[j] for j in pick]) if len(keys) else np.array([], int))


def ci(vals):
    v = np.asarray([x for x in vals if x is not None and not (isinstance(x, float) and math.isnan(x))])
    if len(v) == 0:
        return [None, None]
    return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]


def strat_auc(y, s, strata) -> float:
    y, s, strata = np.asarray(y), np.asarray(s, float), np.asarray(strata)
    num = den = 0.0
    for st in sorted(set(strata.tolist())):
        m = strata == st
        yv = y[m]
        n1, n0 = int(yv.sum()), int(len(yv) - yv.sum())
        if n1 and n0:
            num += auc_fast(yv, s[m]) * n1 * n0
            den += n1 * n0
    return num / den if den else float("nan")


def cluster_boot_mean(values, clusters, b: int = B, seed: int = SEED):
    """Mean of `values` and its percentile CI from a cluster bootstrap (resample clusters with replacement, B times).
    Vectorised: per-cluster sums/counts, one (B x K) index draw from default_rng(seed)."""
    values = np.asarray(values, float)
    if len(values) == 0:
        return float("nan"), [None, None]
    keys = sorted(set(clusters))
    pos = {k: i for i, k in enumerate(keys)}
    ci_ = np.array([pos[c] for c in clusters])
    sums = np.bincount(ci_, weights=values, minlength=len(keys))
    cnts = np.bincount(ci_, minlength=len(keys)).astype(float)
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(keys), (b, len(keys)))
    bs = sums[idx].sum(1) / np.maximum(cnts[idx].sum(1), 1e-12)
    return float(values.mean()), [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
