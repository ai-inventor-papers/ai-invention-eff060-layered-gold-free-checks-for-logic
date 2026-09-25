"""Meta-evaluation of every baseline on the shared frozen screen. All scores oriented: higher = more likely UNFAITHFUL.

Item-level AUROC (ties = 0.5) / AUPRC with prevalence; tie rate; thresholded precision/recall/FA/balanced accuracy and
precision re-weighted to 10%/25% prevalence; sentence-clustered bootstrap CIs (2,000 resamples, seed 0) with the SAME
resamples for every metric (paired deltas) + DeLong check; contamination (disguise delta, DiD, score shift, recall probe);
cross-fitted best-baseline combination (GroupKFold by sentence); per-census-type sensitivity; invariance; complexity
strata; system level; coverage; cost.
"""
from __future__ import annotations

import math
from collections import Counter, defaultdict

import numpy as np
from loguru import logger
from scipy import stats
from sklearn.metrics import average_precision_score, roc_auc_score

from .common import norm

B_RESAMPLES = 2000
SEED = 0

# name -> (source description, kind) ; kind: prob (judge, thr 0.5) | cont (percentile thr) | bin (>0.5) | count (>0)
METRICS = {
    "parse_fail": ("1 - parses under the shared FOL grammar + z3", "bin"),
    "pilot_joint_conflict": ("story ∪ {cand} UNSAT (z3)", "bin"),
    "pilot_arity_incons": ("#arity clashes with story / within cand", "count"),
    "pilot_shape_incons": ("#arg-kind shape clashes with story", "count"),
    "pilot_dangling": ("fraction of cand symbols absent from story", "cont"),
    "pilot_undeclared": ("fraction of cand predicates not declared (Logic-LM)", "count"),
    "pilot_rerun_jacc": ("1 - cross-system predicate Jaccard (rerun proxy)", "cont_L"),
    "rt_nli_min": ("1 - min(P_entail fwd, bwd)", "cont"),
    "rt_nli_fwd": ("1 - P_entail(text => verbalisation)", "cont"),
    "rt_nli_bwd": ("1 - P_entail(verbalisation => text)", "cont"),
    "rt_nli_contra": ("max P_contradiction", "cont"),
    "rt_nli_min_alt": ("1 - min entail, alt NLI checkpoint", "cont"),
    "rt_embed_cos": ("1 - mpnet cosine(text, verbalisation)", "cont"),
    "rt_reformalise_eq": ("1 - [re-formalised verbalisation ≡ cand modulo vocab]", "bin"),
    "judge_cheap_orig": ("1 - P(faithful), primary cheap judge, original", "prob"),
    "judge_cheap_disg": ("1 - P(faithful), primary cheap judge, DISGUISED (pre-registered bar)", "prob"),
    "judge_cheap2_orig": ("1 - P(YES), secondary judge logprobs, original", "prob"),
    "judge_cheap2_disg": ("1 - P(YES), secondary judge logprobs, disguised", "prob"),
    "judge_strong_orig": ("1 - P(faithful), strong (frontier) judge, original (subset)", "prob"),
    "judge_strong_disg": ("1 - P(faithful), strong (frontier) judge, disguised (subset)", "prob"),
    # secondary: open-weight local judges / local verbaliser (run while the API key was exhausted)
    "judge_local_qwen8b_orig": ("1 - P(faithful), local Qwen3-8B JSON judge, original", "prob"),
    "judge_local_qwen8b_disg": ("1 - P(faithful), local Qwen3-8B JSON judge, disguised", "prob"),
    "judge_local_llama8b_orig": ("1 - P(YES), local Llama-3.1-8B logprob judge, original", "prob"),
    "judge_local_llama8b_disg": ("1 - P(YES), local Llama-3.1-8B logprob judge, disguised", "prob"),
    "judge_local_qwen14b_orig": ("1 - P(faithful), local Qwen3-14B-nf4 judge, original (subset)", "prob"),
    "judge_local_qwen14b_disg": ("1 - P(faithful), local Qwen3-14B-nf4 judge, disguised (subset)", "prob"),
    "rt_nli_min_localverb": ("1 - min NLI entail, local Qwen3-8B verbaliser", "cont"),
    "rt_reformalise_eq_localverb": ("1 - re-formalisation equivalence, local Qwen3-8B verbaliser", "bin"),
}
SUBSET_METRICS = {"judge_strong_orig", "judge_strong_disg", "judge_local_qwen14b_orig", "judge_local_qwen14b_disg"}
NA = "NA"      # not applicable by design (excluded from that metric's evaluation)
FAIL = "FAIL"  # metric failure: scored as the maximum (flagged) and counted against coverage


# ------------------------------------------------------------------ assemble per-key oriented scores
def assemble(keys, pilot, rt_llm, rt_nli, rt_eq, j1, j2, j3, track_of, sub_of, local=None):
    """Return {key: {metric: float | NA | FAIL}} + raw fields."""
    out = {}
    for k in keys:
        p = pilot.get(k, {})
        tr, sub = track_of(k), sub_of(k)
        row = {}
        row["parse_fail"] = 0.0 if p.get("parse_ok") else 1.0
        unp = p.get("parse_fail") == 1
        def pil(name, val, applicable=True):
            if not applicable:
                return NA
            if unp:
                return FAIL
            return FAIL if val is None else float(val)
        row["pilot_joint_conflict"] = pil("jc", p.get("pilot_joint_conflict"))
        row["pilot_arity_incons"] = pil("ar", p.get("pilot_arity_incons"))
        row["pilot_shape_incons"] = pil("sh", p.get("pilot_shape_incons"))
        row["pilot_dangling"] = pil("dg", p.get("pilot_dangling"), applicable=(sub != "MALLS"))
        row["pilot_undeclared"] = pil("ud", p.get("pilot_undeclared"), applicable=(tr == "L"))
        rj = p.get("pilot_rerun_jacc")
        row["pilot_rerun_jacc"] = NA if tr != "L" else (FAIL if unp else (NA if rj is None else 1.0 - rj))
        n = rt_nli.get(k)
        for m in ("rt_nli_min", "rt_nli_fwd", "rt_nli_bwd", "rt_nli_min_alt"):
            row[m] = FAIL if (n is None or n.get(m) is None) else 1.0 - n[m]
        row["rt_nli_contra"] = FAIL if (n is None or n.get("rt_nli_contra") is None) else n["rt_nli_contra"]
        row["rt_embed_cos"] = FAIL if (n is None or n.get("rt_embed_cos") is None) else 1.0 - n["rt_embed_cos"]
        e = rt_eq.get(k)
        row["rt_reformalise_eq"] = FAIL if (e is None or e.get("rt_reformalise_eq") is None) else 1.0 - e["rt_reformalise_eq"]
        for name, src in (("judge_cheap", j1), ("judge_cheap2", j2), ("judge_strong", j3)):
            for cond in ("orig", "disg"):
                r = src.get(f"{k}|{cond}")
                if r is None:
                    row[f"{name}_{cond}"] = NA if name == "judge_strong" else FAIL
                else:
                    row[f"{name}_{cond}"] = FAIL if r.get("p") is None else 1.0 - float(r["p"])
        local = local or {}
        for name in ("judge_local_qwen8b", "judge_local_llama8b", "judge_local_qwen14b"):
            src = local.get(name, {})
            for cond in ("orig", "disg"):
                r = src.get(f"{k}|{cond}")
                if r is None:
                    row[f"{name}_{cond}"] = NA if name == "judge_local_qwen14b" else FAIL
                else:
                    row[f"{name}_{cond}"] = FAIL if r.get("p") is None else 1.0 - float(r["p"])
        nl = local.get("rt_nli_local", {}).get(k)
        row["rt_nli_min_localverb"] = FAIL if (nl is None or nl.get("rt_nli_min") is None) else 1.0 - nl["rt_nli_min"]
        el = local.get("rt_eq_local", {}).get(k)
        row["rt_reformalise_eq_localverb"] = FAIL if (el is None or el.get("rt_reformalise_eq") is None) else 1.0 - el["rt_reformalise_eq"]
        out[k] = row
    return out


def fill(values: list, maxval: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """-> scores (FAIL -> maxval), applicable mask, fail mask."""
    s = np.array([maxval if v == FAIL else (np.nan if v == NA else v) for v in values], dtype=float)
    app = np.array([v != NA for v in values])
    fl = np.array([v == FAIL for v in values])
    return s, app, fl


# ------------------------------------------------------------------ bootstrap machinery
class ClusterBoot:
    """Cluster bootstrap weights: each resample draws clusters with replacement; item weight = cluster multiplicity."""

    def __init__(self, clusters: list[str], B: int = B_RESAMPLES, seed: int = SEED):
        self.uc = sorted(set(clusters))
        idx = {c: i for i, c in enumerate(self.uc)}
        self.cid = np.array([idx[c] for c in clusters])
        rng = np.random.default_rng(seed)
        draws = rng.integers(0, len(self.uc), size=(B, len(self.uc)))
        self.W = np.zeros((B, len(self.uc)), dtype=np.int32)
        for b in range(B):
            np.add.at(self.W[b], draws[b], 1)
        self.B = B

    def item_weights(self, b: int) -> np.ndarray:
        return self.W[b][self.cid]


def auc_w(y, s, w=None):
    ok = ~np.isnan(s)
    y, s = y[ok], s[ok]
    w = None if w is None else w[ok]
    if w is not None:
        keep = w > 0
        y, s, w = y[keep], s[keep], w[keep]
    if len(np.unique(y)) < 2:
        return np.nan
    return roc_auc_score(y, s, sample_weight=w)


def boot_auc(y, s, cb: ClusterBoot):
    """Vectorised weighted AUROC (ties = 0.5) for all B cluster-bootstrap resamples at once."""
    ok = ~np.isnan(s)
    if ok.sum() == 0 or len(np.unique(y[ok])) < 2:
        return np.full(cb.B, np.nan)
    s_, y_, cid = s[ok], y[ok], cb.cid[ok]
    Wi = cb.W[:, cid].astype(np.float64)                      # B x n item weights
    u, inv = np.unique(s_, return_inverse=True)                # ascending unique scores
    K = len(u)
    onehot = np.zeros((len(s_), K))
    onehot[np.arange(len(s_)), inv] = 1.0
    P = Wi[:, y_ == 1] @ onehot[y_ == 1]                       # B x K positive weight per unique score
    N = Wi[:, y_ == 0] @ onehot[y_ == 0]
    cumN_before = np.cumsum(N, axis=1) - N
    num = (P * (cumN_before + 0.5 * N)).sum(1)
    den = P.sum(1) * N.sum(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        out = np.where(den > 0, num / den, np.nan)
    return out


def ci(a):
    a = a[~np.isnan(a)]
    if len(a) == 0:
        return [None, None]
    return [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]


def tie_rate(y, s):
    ok = ~np.isnan(s)
    pos, neg = s[ok & (y == 1)], s[ok & (y == 0)]
    if len(pos) == 0 or len(neg) == 0:
        return None
    # count tied (pos, neg) pairs via value counts
    cp, cn = Counter(pos.round(9).tolist()), Counter(neg.round(9).tolist())
    ties = sum(cp[v] * cn.get(v, 0) for v in cp)
    return ties / (len(pos) * len(neg))


def delong(y, s1, s2):
    """Paired DeLong test for two correlated AUCs (Sun & Xu 2014 fast version). Returns (auc1, auc2, z, p)."""
    ok = ~np.isnan(s1) & ~np.isnan(s2)
    y, s1, s2 = y[ok], s1[ok], s2[ok]
    pos, neg = y == 1, y == 0
    m, n = pos.sum(), neg.sum()
    if m < 2 or n < 2:
        return None

    def comps(s):
        x, yv = s[pos], s[neg]
        v10 = np.array([(np.sum(xi > yv) + 0.5 * np.sum(xi == yv)) / n for xi in x])
        v01 = np.array([(np.sum(x > yj) + 0.5 * np.sum(x == yj)) / m for yj in yv])
        return v10.mean(), v10, v01
    a1, v10a, v01a = comps(s1)
    a2, v10b, v01b = comps(s2)
    s10 = np.cov(np.vstack([v10a, v10b]))
    s01 = np.cov(np.vstack([v01a, v01b]))
    S = s10 / m + s01 / n
    var = S[0, 0] + S[1, 1] - 2 * S[0, 1]
    if var <= 0:
        return float(a1), float(a2), 0.0, 1.0
    z = (a1 - a2) / math.sqrt(var)
    return float(a1), float(a2), float(z), float(2 * (1 - stats.norm.cdf(abs(z))))


# ------------------------------------------------------------------ thresholds
def thresholds(scores_by_metric: dict, ref_mask_by_metric: dict) -> dict:
    """judges 0.5 on oriented scale; continuous -> 90th pct of oriented score on the reference (track-H CORRECT, dev
    excluded); binary -> 0.5; counts -> 0 (flag if >0); L-only continuous (rerun jacc) -> 0.5 (Jaccard < 0.5)."""
    thr = {}
    for m, (_, kind) in METRICS.items():
        if kind == "prob" or kind == "bin":
            thr[m] = 0.5
        elif kind == "count":
            thr[m] = 0.0
        elif kind == "cont_L":
            thr[m] = 0.5
        else:
            s = scores_by_metric[m]
            ref = s[ref_mask_by_metric[m] & ~np.isnan(s)]
            thr[m] = float(np.percentile(ref, 90)) if len(ref) else 0.5
    return thr


def at_threshold(y, s, t):
    ok = ~np.isnan(s)
    y, s = y[ok], s[ok]
    f = s > t
    tp, fp = int(np.sum(f & (y == 1))), int(np.sum(f & (y == 0)))
    P, N = int(np.sum(y == 1)), int(np.sum(y == 0))
    rec = tp / P if P else None
    fa = fp / N if N else None
    prec = tp / (tp + fp) if (tp + fp) else None

    def rw(pi):
        if rec is None or fa is None or (rec * pi + fa * (1 - pi)) == 0:
            return None
        return rec * pi / (rec * pi + fa * (1 - pi))
    return {"precision": prec, "recall": rec, "fa": fa, "bal_acc": None if rec is None or fa is None else (rec + 1 - fa) / 2,
            "prec_at_10pct": rw(0.10), "prec_at_25pct": rw(0.25), "n_flagged": int(f.sum())}


def evaluate_set(name, keys, y, table, thr, metrics, cb=None, compute_ci=True):
    """-> ({metric: result}, cb, {metric: boot array})."""
    clusters = [table["_cluster"][k] for k in keys]
    if cb is None and compute_ci:
        cb = ClusterBoot(clusters)
    res, boots = {}, {}
    for m in metrics:
        vals = [table[m][k] for k in keys]
        mx = table["_max"][m]
        s, app, fl = fill(vals, mx)
        s_app = np.where(app, s, np.nan)
        n_app = int(app.sum())
        if n_app == 0 or len(np.unique(y[app])) < 2:
            res[m] = {"n_applicable": n_app, "auroc": None, "note": "not applicable / single class"}
            continue
        a = auc_w(y, s_app)
        r = {"n_applicable": n_app, "n_pos": int(np.sum(y[app] == 1)), "n_neg": int(np.sum(y[app] == 0)),
             "prevalence": float(np.mean(y[app])), "auroc": float(a),
             "auprc": float(average_precision_score(y[app], s[app])), "tie_rate": tie_rate(y, s_app),
             "coverage": float(1 - fl[app].mean()), "n_fail": int(fl[app].sum()), "threshold": thr[m],
             **at_threshold(y, s_app, thr[m])}
        r["testable"] = bool(r["n_pos"] >= 50 and r["n_neg"] >= 50)
        if compute_ci:
            ba = boot_auc(y, s_app, cb)
            boots[m] = ba
            r["auroc_ci"] = ci(ba)
        res[m] = r
    return res, cb, boots


# ------------------------------------------------------------------ combination
def combo_oof(keys, y, groups, table, feats, n_splits=5, C=1.0, fold_of=None):
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    from sklearn.preprocessing import StandardScaler
    X, cols = [], []
    for f in feats:
        v = [table[f][k] for k in keys]
        s, app, fl = fill(v, table["_max"][f])
        miss = np.isnan(s)
        X.append(np.where(miss, np.nan, s))
        cols.append(f)
        if miss.any():
            X.append(miss.astype(float))
            cols.append(f + "__missing")
    X = np.vstack(X).T
    if fold_of is None:
        gkf = GroupKFold(n_splits=n_splits)
        fold = np.zeros(len(keys), dtype=int)
        for i, (_, te) in enumerate(gkf.split(X, y, groups)):
            fold[te] = i
    else:
        fold = np.array([fold_of[k] for k in keys])
    oof = np.zeros(len(keys))
    for i in range(n_splits):
        tr, te = fold != i, fold == i
        Xtr, Xte = X[tr].copy(), X[te].copy()
        mu = np.nanmean(Xtr, 0)
        mu = np.where(np.isnan(mu), 0, mu)
        sd = np.nanstd(Xtr, 0)
        sd = np.where((sd == 0) | np.isnan(sd), 1, sd)
        Xtr = np.nan_to_num((Xtr - mu) / sd)
        Xte = np.nan_to_num((Xte - mu) / sd)
        clf = LogisticRegression(C=C, max_iter=2000)
        clf.fit(Xtr, y[tr])
        oof[te] = clf.predict_proba(Xte)[:, 1]
    return oof, fold, cols
