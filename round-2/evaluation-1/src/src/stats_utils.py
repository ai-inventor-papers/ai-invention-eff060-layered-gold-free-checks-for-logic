"""Statistics primitives for the iteration-1 re-analysis.

Every score is oriented so that HIGHER = MORE LIKELY UNFAITHFUL (ERROR). Labels y: 1 = ERROR, 0 = CORRECT.
AUROC is the Mann-Whitney statistic with ties counted 0.5 (identical to sklearn.roc_auc_score).
The cluster bootstrap resamples sentences (cluster = norm(text)) with replacement; an item's weight in a resample is
its sentence's multiplicity (the same convention as exp D's ClusterBoot, seed 0, 2000 resamples, percentile CI).
"""
from __future__ import annotations

import math
import re
from collections import Counter

import numpy as np
from scipy import stats
from sklearn.metrics import average_precision_score, roc_auc_score

B_RESAMPLES = 2000
SEED = 0

# exp D src/common.py::norm (gen_art_experiment_4/src/common.py lines 23-29), copied verbatim
_QUOTES = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", "—": "-", "−": "-"})


def norm(s: str) -> str:
    """Exp D's GroupKFold / bootstrap cluster key: lower-case, quotes unified, punctuation -> space, spaces collapsed."""
    s = (s or "").translate(_QUOTES).lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


# exp C src/common.py line 23 (COARSE) and lines 48-52 (op_class), copied verbatim
COARSE = {"ADD": "COVERAGE", "DROP": "COVERAGE", "NEG": "POLARITY", "REV": "POLARITY", "QUANT": "POLARITY"}


def op_class(ops: list[str]) -> str:
    """Exp C's coarse operator class of a repair set: POLARITY / COVERAGE / STRUCT / MIXED (NONE if empty)."""
    if not ops:
        return "NONE"
    cs = {COARSE.get(o, "STRUCT") for o in ops}
    return cs.pop() if len(cs) == 1 else "MIXED"


# ----------------------------------------------------------------------------------------------- point statistics
def auroc(y: np.ndarray, s: np.ndarray) -> float:
    y = np.asarray(y)
    if len(np.unique(y)) < 2:
        return float("nan")
    return float(roc_auc_score(y, s))


def auprc(y: np.ndarray, s: np.ndarray) -> float:
    if len(np.unique(y)) < 2:
        return float("nan")
    return float(average_precision_score(y, s))


def tie_fraction(y: np.ndarray, s: np.ndarray) -> float:
    """Share of (ERROR, CORRECT) pairs whose scores are tied (Deutsch et al. 2023 'Ties Matter')."""
    pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    cp, cn = Counter(np.round(pos, 9).tolist()), Counter(np.round(neg, 9).tolist())
    return sum(cp[v] * cn.get(v, 0) for v in cp) / (len(pos) * len(neg))


def ppv_at_prevalence(tpr: float | None, fpr: float | None, pi: float) -> float | None:
    """PPV = TPR*pi / (TPR*pi + FPR*(1-pi))."""
    if tpr is None or fpr is None:
        return None
    den = tpr * pi + fpr * (1 - pi)
    return None if den == 0 else tpr * pi / den


def at_flag(y: np.ndarray, flag: np.ndarray) -> dict:
    f = flag.astype(bool)
    P, N = int((y == 1).sum()), int((y == 0).sum())
    tp, fp = int((f & (y == 1)).sum()), int((f & (y == 0)).sum())
    rec = tp / P if P else None
    fa = fp / N if N else None
    return {"precision": (tp / (tp + fp)) if (tp + fp) else None, "recall": rec, "fa": fa,
            "prec_at_prev10": ppv_at_prevalence(rec, fa, 0.10), "prec_at_prev25": ppv_at_prevalence(rec, fa, 0.25),
            "n_flagged": int(f.sum())}


def wilson(k: float, n: float, z: float = 1.959964) -> tuple[float, float]:
    if n <= 0:
        return (float("nan"), float("nan"))
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, c - h), min(1.0, c + h))


# ----------------------------------------------------------------------------------------------- cluster bootstrap
class ClusterBoot:
    """Sentence-cluster bootstrap weights: W[b, c] = multiplicity of cluster c in resample b (exp D convention)."""

    def __init__(self, clusters: list[str], B: int = B_RESAMPLES, seed: int = SEED):
        self.uc = sorted(set(clusters))
        idx = {c: i for i, c in enumerate(self.uc)}
        self.cid = np.array([idx[c] for c in clusters])
        rng = np.random.default_rng(seed)
        draws = rng.integers(0, len(self.uc), size=(B, len(self.uc)))
        self.W = np.zeros((B, len(self.uc)), dtype=np.float64)
        for b in range(B):
            np.add.at(self.W[b], draws[b], 1)
        self.B = B

    def item_W(self, mask: np.ndarray | None = None) -> np.ndarray:
        """B x n item weight matrix (optionally restricted to items in mask)."""
        cid = self.cid if mask is None else self.cid[mask]
        return self.W[:, cid]


def boot_auc_w(y: np.ndarray, s: np.ndarray, Wi: np.ndarray) -> np.ndarray:
    """Vectorised weighted AUROC (ties 0.5) for every row of the B x n weight matrix Wi. NaN where a class is empty."""
    u, inv = np.unique(s, return_inverse=True)
    K = len(u)
    onehot = np.zeros((len(s), K))
    onehot[np.arange(len(s)), inv] = 1.0
    P = Wi[:, y == 1] @ onehot[y == 1]
    N = Wi[:, y == 0] @ onehot[y == 0]
    cumN_before = np.cumsum(N, axis=1) - N
    num = (P * (cumN_before + 0.5 * N)).sum(1)
    den = P.sum(1) * N.sum(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(den > 0, num / den, np.nan)


def ci95(a: np.ndarray) -> list:
    a = np.asarray(a, dtype=float)
    a = a[~np.isnan(a)]
    if len(a) == 0:
        return [None, None]
    return [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]


def boot_p_two_sided(d: np.ndarray) -> float:
    """Two-sided bootstrap p = 2 x min(share of Delta <= 0, share of Delta >= 0), capped at 1."""
    d = d[~np.isnan(d)]
    if len(d) == 0:
        return float("nan")
    return float(min(1.0, 2 * min(np.mean(d <= 0), np.mean(d >= 0))))


# ----------------------------------------------------------------------------------------------- DeLong
def _midrank(x: np.ndarray) -> np.ndarray:
    J = np.argsort(x, kind="mergesort")
    Z = x[J]
    N = len(x)
    T = np.zeros(N)
    i = 0
    while i < N:
        j = i
        while j < N and Z[j] == Z[i]:
            j += 1
        T[i:j] = 0.5 * (i + j - 1) + 1
        i = j
    out = np.empty(N)
    out[J] = T
    return out


def placements(y: np.ndarray, s: np.ndarray) -> tuple[float, np.ndarray, np.ndarray]:
    """Fast DeLong (Sun & Xu 2014) placement values: V10 per ERROR item (share of CORRECT below, ties 0.5) and
    V01 per CORRECT item (share of ERROR above, ties 0.5). AUROC = mean(V10) = mean(V01)."""
    pos, neg = s[y == 1], s[y == 0]
    m, n = len(pos), len(neg)
    tx, ty, tz = _midrank(pos), _midrank(neg), _midrank(np.concatenate([pos, neg]))
    v10 = (tz[:m] - tx) / n
    v01 = 1.0 - (tz[m:] - ty) / m
    return float(v10.mean()), v10, v01


def delong_paired(y: np.ndarray, s1: np.ndarray, s2: np.ndarray) -> dict:
    a1, v10a, v01a = placements(y, s1)
    a2, v10b, v01b = placements(y, s2)
    m, n = len(v10a), len(v01a)
    s10 = np.cov(np.vstack([v10a, v10b]))
    s01 = np.cov(np.vstack([v01a, v01b]))
    S = s10 / m + s01 / n
    var = S[0, 0] + S[1, 1] - 2 * S[0, 1]
    if var <= 0:
        return {"auc1": a1, "auc2": a2, "z": 0.0, "p": 1.0}
    z = (a1 - a2) / math.sqrt(var)
    return {"auc1": a1, "auc2": a2, "z": float(z), "p": float(2 * stats.norm.sf(abs(z)))}


def delong_clustered_paired(y: np.ndarray, s1: np.ndarray, s2: np.ndarray, clusters: np.ndarray) -> dict:
    """Obuchowski (1997) clustered-ROC variance for the paired AUROC difference: placement values are summed within
    sentence clusters and the variance is estimated from between-cluster variation of those sums."""
    a1, v10a, v01a = placements(y, s1)
    a2, v10b, v01b = placements(y, s2)
    d10, d01 = v10a - v10b, v01a - v01b
    ad = a1 - a2
    cp, cn = clusters[y == 1], clusters[y == 0]
    uc = sorted(set(clusters.tolist()))
    K = len(uc)
    M, N = len(d10), len(d01)
    idx = {c: i for i, c in enumerate(uc)}
    X, Y, mi, ni = np.zeros(K), np.zeros(K), np.zeros(K), np.zeros(K)
    np.add.at(X, [idx[c] for c in cp], d10)
    np.add.at(mi, [idx[c] for c in cp], 1)
    np.add.at(Y, [idx[c] for c in cn], d01)
    np.add.at(ni, [idx[c] for c in cn], 1)
    f = K / (K - 1)
    S10 = f / M * np.sum((X - mi * ad) ** 2)
    S01 = f / N * np.sum((Y - ni * ad) ** 2)
    S11 = f * np.sum((X - mi * ad) * (Y - ni * ad))
    var = S10 / M + S01 / N + 2 * S11 / (M * N)
    if var <= 0:
        return {"z": 0.0, "p": 1.0, "se": 0.0}
    z = ad / math.sqrt(var)
    return {"z": float(z), "p": float(2 * stats.norm.sf(abs(z))), "se": float(math.sqrt(var))}


def holm(pvals: dict) -> dict:
    items = [(k, v) for k, v in pvals.items() if v is not None and not (isinstance(v, float) and math.isnan(v))]
    items.sort(key=lambda kv: kv[1])
    m = len(items)
    out, run = {}, 0.0
    for i, (k, p) in enumerate(items):
        run = max(run, min(1.0, (m - i) * p))
        out[k] = run
    return out


# ----------------------------------------------------------------------------------------------- matched-FA operating point
def matched_fa_rule(s_correct: np.ndarray, f: float) -> tuple[float, float, float]:
    """Randomised threshold achieving FA exactly f on the CORRECT scores (= linear interpolation between adjacent ROC
    vertices). Returns (v, q, achieved_fa): an item is flagged with prob 1 if s > v, prob q if s == v, else 0."""
    sc = np.sort(s_correct)
    n = len(sc)
    levels = np.unique(sc)[::-1]  # descending
    fa_above = 0.0
    for v in levels:
        at = np.sum(sc == v) / n
        if fa_above + at >= f - 1e-12:
            q = (f - fa_above) / at if at > 0 else 0.0
            return float(v), float(min(max(q, 0.0), 1.0)), float(fa_above + q * at)
        fa_above += at
    return float(levels[-1]), 1.0, 1.0


def flag_prob(s: np.ndarray, rule: tuple[float, float, float]) -> np.ndarray:
    v, q, _ = rule
    return np.where(s > v + 1e-12, 1.0, np.where(np.abs(s - v) <= 1e-12, q, 0.0))


def interp_recall_at_fa(y: np.ndarray, s: np.ndarray, f: float) -> tuple[float, float]:
    rule = matched_fa_rule(s[y == 0], f)
    return float(flag_prob(s[y == 1], rule).mean()), rule[2]


# ----------------------------------------------------------------------------------------------- misc
def spearman(a: np.ndarray, b: np.ndarray) -> float:
    if len(a) < 3 or np.std(a) == 0 or np.std(b) == 0:
        return float("nan")
    return float(stats.spearmanr(a, b).correlation)


def resample_indices(cb_items_cid: np.ndarray, W: np.ndarray, b: int) -> np.ndarray:
    """Materialise item indices for resample b from cluster multiplicities."""
    w = W[b][cb_items_cid].astype(int)
    return np.repeat(np.arange(len(w)), w)
