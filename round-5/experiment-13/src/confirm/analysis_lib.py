"""Statistics used by join_and_test.py: within-template AUROC with shared template-stratified sentence-bootstrap
weights, paired deltas, cross-fitted nesting, operating points and Holm. Orientation: higher score = more likely ERROR;
y = 1 means ERROR. Pure numpy / sklearn; no file I/O."""
from __future__ import annotations

import numpy as np
from sklearn.linear_model import LogisticRegression

from auc_tools import StratAUC, boot_weights


class Boot:
    """One set of bootstrap weights over ALL sentences (clusters), resampled within template; shared by every metric,
    population and delta, so that paired comparisons use the SAME resamples."""

    def __init__(self, sentence_ids: list[str], sentence_template: dict, B: int, seed: int):
        self.sids = sorted(sentence_ids)
        self.ix = {s: i for i, s in enumerate(self.sids)}
        cs = np.array([sentence_template[s] for s in self.sids])
        self.W = boot_weights(cs, B, seed)
        self.B = B

    def cl(self, sids) -> np.ndarray:
        return np.array([self.ix[s] for s in sids], dtype=np.int64)


def _arr(df, col):
    return df[col].to_numpy(dtype=float)


def auc_block(df, score: str, boot: Boot, ycol: str = "y", stratum: str = "template_id", with_boot: bool = True) -> dict:
    d = df[df[score].notna() & df[ycol].notna()]
    y = d[ycol].to_numpy().astype(bool)
    out = {"n": int(len(d)), "n_err": int(y.sum()), "n_cor": int((~y).sum()), "n_sent": int(d.sentence_id.nunique()),
           "n_sent_err": int(d[y].sentence_id.nunique()), "n_sent_cor": int(d[~y].sentence_id.nunique())}
    if y.all() or (~y).all() or len(d) == 0:
        out.update(est=None, ci=[None, None], se=None)
        return out
    st = d[stratum].to_numpy() if stratum != "pooled" else np.zeros(len(d))
    A = StratAUC(_arr(d, score), y, st, boot.cl(d.sentence_id))
    out["est"] = A.value()
    if with_boot:
        bs = np.array([A.value(boot.W[b]) for b in range(boot.B)])
        bs = bs[~np.isnan(bs)]
        out["ci"] = [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))]
        out["se"] = float(np.std(bs, ddof=1))
    return out


def paired_delta(df, a: str, b: str, boot: Boot, ycol: str = "y", stratum: str = "template_id") -> dict:
    """AUROC_within(a) - AUROC_within(b) on rows where both are scored, same bootstrap weights."""
    d = df[df[a].notna() & df[b].notna() & df[ycol].notna()]
    y = d[ycol].to_numpy().astype(bool)
    out = {"a": a, "b": b, "n": int(len(d)), "n_err": int(y.sum()), "n_cor": int((~y).sum()), "n_sent": int(d.sentence_id.nunique())}
    if len(d) == 0 or y.all() or (~y).all():
        out.update(delta=None, ci=[None, None], p_two_sided=None, auroc_a=None, auroc_b=None)
        return out
    st = d[stratum].to_numpy() if stratum != "pooled" else np.zeros(len(d))
    cl = boot.cl(d.sentence_id)
    A = StratAUC(_arr(d, a), y, st, cl)
    Bm = StratAUC(_arr(d, b), y, st, cl)
    ea, eb = A.value(), Bm.value()
    ba = np.array([A.value(boot.W[i]) for i in range(boot.B)])
    bb = np.array([Bm.value(boot.W[i]) for i in range(boot.B)])
    dd = ba - bb
    ok = ~np.isnan(dd)
    dd, ba, bb = dd[ok], ba[ok], bb[ok]
    out.update(auroc_a=ea, auroc_b=eb, auroc_a_ci=[float(np.percentile(ba, 2.5)), float(np.percentile(ba, 97.5))],
               auroc_b_ci=[float(np.percentile(bb, 2.5)), float(np.percentile(bb, 97.5))], delta=ea - eb,
               ci=[float(np.percentile(dd, 2.5)), float(np.percentile(dd, 97.5))], se=float(np.std(dd, ddof=1)),
               p_two_sided=float(min(1.0, 2 * min((dd <= 0).mean(), (dd >= 0).mean()))), ci_lower_gt_0=bool(np.percentile(dd, 2.5) > 0),
               ratio=(ea / eb) if eb else None, ratio_ci=[float(np.percentile(ba / bb, 2.5)), float(np.percentile(ba / bb, 97.5))])
    return out


def delta_boot_vector(df, a: str, b: str, boot: Boot, ycol: str = "y") -> tuple[float, np.ndarray]:
    d = df[df[a].notna() & df[b].notna() & df[ycol].notna()]
    y = d[ycol].to_numpy().astype(bool)
    st = d.template_id.to_numpy()
    cl = boot.cl(d.sentence_id)
    A, Bm = StratAUC(_arr(d, a), y, st, cl), StratAUC(_arr(d, b), y, st, cl)
    return A.value() - Bm.value(), np.array([A.value(boot.W[i]) - Bm.value(boot.W[i]) for i in range(boot.B)])


def holm(pvals: dict) -> dict:
    items = sorted(pvals.items(), key=lambda kv: kv[1])
    m = len(items)
    adj, run = {}, 0.0
    for i, (k, p) in enumerate(items):
        run = max(run, min(1.0, (m - i) * p))
        adj[k] = run
    return adj


# ------------------------------------------------------------------------------------------ nesting
def _ecdf_map(train: np.ndarray, x: np.ndarray) -> np.ndarray:
    s = np.sort(train)
    lo = np.searchsorted(s, x, side="left")
    hi = np.searchsorted(s, x, side="right")
    return (lo + hi) / (2.0 * len(s))


def crossfit_oof(d, features: list[str], ycol: str = "y", C: float = 1.0) -> np.ndarray:
    """5 sentence folds (d.fold); features rank-normalised by the TRAIN fold's ECDF; logistic OOF probabilities."""
    y = d[ycol].to_numpy().astype(int)
    out = np.full(len(d), np.nan)
    folds = d.fold.to_numpy()
    X = d[features].to_numpy(dtype=float)
    for f in range(5):
        te, tr = folds == f, folds != f
        if te.sum() == 0 or len(set(y[tr])) < 2:
            continue
        Xtr = np.column_stack([_ecdf_map(X[tr, j], X[tr, j]) for j in range(X.shape[1])])
        Xte = np.column_stack([_ecdf_map(X[tr, j], X[te, j]) for j in range(X.shape[1])])
        m = LogisticRegression(C=C, max_iter=1000).fit(Xtr, y[tr])
        out[te] = m.predict_proba(Xte)[:, 1]
    return out


def nested_block(df, base: list[str], add: list[str], boot: Boot, ycol: str = "y", n_perm: int = 50, seed: int = 20260924) -> dict:
    """[base+add] - [base] within-template AUROC of cross-fitted OOF predictions, bootstrap over sentences on the fixed
    OOF predictions (no refit per replicate), plus a within-template label-permutation null with refits."""
    cols = base + add
    d = df[df[cols].notna().all(axis=1) & df[ycol].notna()].copy()
    d["_p_base"] = crossfit_oof(d, base, ycol)
    d["_p_full"] = crossfit_oof(d, cols, ycol)
    r = paired_delta(d, "_p_full", "_p_base", boot, ycol)
    rng = np.random.default_rng(seed)
    null = []
    for _ in range(n_perm):
        dp = d.copy()
        yp = dp[ycol].to_numpy().copy()
        for t in np.unique(dp.template_id):
            m = dp.template_id.to_numpy() == t
            yp[m] = rng.permutation(yp[m])
        dp["_yp"] = yp
        dp["_pb"] = crossfit_oof(dp, base, "_yp")
        dp["_pf"] = crossfit_oof(dp, cols, "_yp")
        yb = dp._yp.to_numpy().astype(bool)
        st, cl = dp.template_id.to_numpy(), boot.cl(dp.sentence_id)
        null.append(StratAUC(dp._pf.to_numpy(), yb, st, cl).value() - StratAUC(dp._pb.to_numpy(), yb, st, cl).value())
    null = np.array(null)
    return {"model_base": base, "model_full": cols, "n": int(len(d)), "auroc_full": r.get("auroc_a"), "auroc_base": r.get("auroc_b"),
            "delta": r.get("delta"), "ci": r.get("ci"), "p_two_sided": r.get("p_two_sided"),
            "perm_null_p95": float(np.percentile(null, 95)), "perm_null_mean": float(null.mean()), "n_perm": n_perm,
            "delta_gt_null_p95": bool(r.get("delta") is not None and r["delta"] > np.percentile(null, 95)),
            "note": "bootstrap over sentences on fixed OOF predictions (no refit per replicate); permutation null refits"}


# ------------------------------------------------------------------------------------------ operating points
def op_point(df, score: str, thr: float, ycol: str = "y") -> dict:
    from cc import wilson
    d = df[df[score].notna() & df[ycol].notna()]
    y = d[ycol].to_numpy().astype(bool)
    f = d[score].to_numpy() > thr
    tp, fp = int((f & y).sum()), int((f & ~y).sum())
    return {"threshold_gt": thr, "n_err": int(y.sum()), "n_cor": int((~y).sum()), "recall": tp / max(y.sum(), 1),
            "recall_ci": wilson(tp, int(y.sum())), "FA": fp / max((~y).sum(), 1), "FA_ci": wilson(fp, int((~y).sum())),
            "precision": tp / max(tp + fp, 1), "precision_ci": wilson(tp, tp + fp), "n_flagged": int(f.sum())}


def thr_at_fa(df, score: str, fa: float = 0.10, ycol: str = "y") -> dict:
    """Coarse scores tie heavily, so FA = 0.10 is rarely achievable exactly: return the two achievable thresholds that
    bracket it (rule 'score > t'): t_le = smallest t with FA <= fa, t_gt = largest t with FA > fa."""
    d = df[df[score].notna() & df[ycol].notna()]
    neg = d[~d[ycol].astype(bool)][score].to_numpy()
    cands = np.unique(np.concatenate([neg, [neg.min() - 1e-9]]))
    fas = np.array([(neg > t).mean() for t in cands])
    le = cands[fas <= fa]
    gt = cands[fas > fa]
    return {"t_le": float(le.min()) if len(le) else None, "t_gt": float(gt.max()) if len(gt) else None}
