"""PART 2 + STEP 4: exact decomposition AUROC_b = 1 - (e + d)/2 of binary cross-family consensus, its cuts, the graded
trace, the VOCAB_EXACT aligner-free control, and the mechanism tests M1 / M2 / NET / SCATTER / M3-local.

ed_decomposition(y, endorsed) is the reusable function (iteration 4 applies it unchanged to R_COMP)."""
from __future__ import annotations

import re
import warnings
from collections import Counter, defaultdict

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from loguru import logger
from sklearn.linear_model import LogisticRegression
from statsmodels.stats.outliers_influence import variance_inflation_factor

from stats import SentBoot, WAuc, WStratAuc, auc, ci, strat_auc

RULES = ["MAJ", "PLUR", "FAM2", "FAMMAJ", "MAJ_EXACT"]
MIN_ROWS, MIN_SENT = 30, 10


# =================================================================================================== identity
def ed_decomposition(y, endorsed) -> dict:
    """y: 1 = ERROR, 0 = CORRECT; endorsed: 1 = the cross-family peer rule endorses the candidate.
    Returns e = P(endorsed | ERROR) (error-endorsement), d = P(not endorsed | CORRECT) (correct-divergence) and
    AUROC_b of b = 1 - endorsed, asserting the bookkeeping identity AUROC_b = 1 - (e + d)/2 (balanced accuracy)."""
    y = np.asarray(y, int)
    en = np.asarray(endorsed, int)
    e = float(en[y == 1].mean())
    d = float((1 - en[y == 0]).mean())
    a = auc(y, 1 - en)
    assert abs(a - (1 - (e + d) / 2)) < 1e-12, (a, e, d)
    return {"n_err": int((y == 1).sum()), "n_cor": int((y == 0).sum()), "e": e, "d": d, "auroc_b": a}


def normalise_name(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


# =================================================================================================== bins
def make_bins(df: pd.DataFrame, cut: dict) -> pd.DataFrame:
    q1, q2 = cut["words_tercile_cuts"]
    df = df.copy()
    df["words_t"] = np.where(df.words <= q1, "T1", np.where(df.words <= q2, "T2", "T3"))
    nc = df.n_conditions.fillna(-1).astype(int)
    df["ncond_bin"] = np.where(nc <= 1, "0-1", np.where(nc == 2, "2", np.where(nc == 3, "3", "4+")))
    et = df.exception_type.fillna("none").astype(str)
    keep = set(cut["exception_types_kept"])
    df["exc_bin"] = np.where(et == "none", "none", np.where(et.isin(keep), et, "other_exc"))
    df["long"] = df.stratum.isin(["L25", "L20", "EXC"])
    return df


def prereg_cuts(rab: pd.DataFrame) -> dict:
    sent = rab.drop_duplicates("sentence_id")
    q1, q2 = np.quantile(sent.words.values, [1 / 3, 2 / 3])
    et = rab.exception_type.fillna("none").astype(str)
    cnt = Counter(et[et != "none"])
    return {"words_tercile_cuts": [float(q1), float(q2)], "words_tercile_rule": "T1: words<=q1, T2: q1<words<=q2, T3: >q2; "
            "cut points = 1/3, 2/3 quantiles of R_AB SENTENCE words (np.quantile, linear)",
            "n_conditions_bins": ["0-1", "2", "3", "4+"], "exception_types_kept": sorted(k for k, v in cnt.items() if v >= 30),
            "exception_type_counts_R_AB_rows": dict(cnt)}


# =================================================================================================== cuts
def cell_stats(sub: pd.DataFrame, ycol: str, rule_cols: dict, boot: SentBoot, W_all: np.ndarray, pos: np.ndarray,
               score_col: str = "c_frozen") -> list[dict]:
    """e, d, AUROC_b per rule and AUROC(score) for one cell, with sentence-cluster bootstrap CIs."""
    y = sub[ycol].values.astype(int)
    n1, n0 = int(y.sum()), int((1 - y).sum())
    nsent = sub.sentence_id.nunique()
    W = W_all[:, pos]
    ok_e = n1 >= MIN_ROWS and nsent >= MIN_SENT
    ok_d = n0 >= MIN_ROWS and nsent >= MIN_SENT
    out = []
    a_c = auc(y, sub[score_col].values) if n1 and n0 else float("nan")
    a_c_ci = [None, None]
    if ok_e and ok_d:
        wa = WAuc(y, sub[score_col].values)
        a_c_ci = ci([wa(W[b]) for b in range(W.shape[0])])
    for rule, col in rule_cols.items():
        en = sub[col].values.astype(float)
        if np.isnan(en).any():
            m = ~np.isnan(en)
            logger.warning(f"rule {rule}: {int((~m).sum())} rows without a value dropped in cell")
        e = float(en[y == 1].mean()) if n1 else float("nan")
        d = float((1 - en[y == 0]).mean()) if n0 else float("nan")
        ab = 1 - (e + d) / 2 if n1 and n0 else float("nan")
        if n1 and n0:
            assert abs(ab - auc(y, 1 - en)) < 1e-12
        rec = {"rule": rule, "n_err": n1, "n_cor": n0, "n_sent": nsent, "e": e, "d": d, "auroc_b": ab, "auroc_c": a_c,
               "auroc_c_ci": a_c_ci, "inference": "tested" if (ok_e and ok_d) else ("partial" if (ok_e or ok_d) else "descriptive")}
        with np.errstate(invalid="ignore", divide="ignore"):
            eb = (W @ (en * y)) / (W @ y) if ok_e else None
            db = (W @ ((1 - en) * (1 - y))) / (W @ (1 - y)) if ok_d else None
        rec["e_ci"] = ci(eb) if eb is not None else [None, None]
        rec["d_ci"] = ci(db) if db is not None else [None, None]
        rec["auroc_b_ci"] = ci(1 - (eb + db) / 2) if (eb is not None and db is not None) else [None, None]
        out.append(rec)
    return out


def run_cuts(P: pd.DataFrame, boot: SentBoot, regimes: dict, rule_cols: dict) -> pd.DataFrame:
    """P = consensus-scorable population frame (aligned with boot rows). regimes = {name: (mask, ycol)}."""
    W_all = boot.W()
    rows = []
    dims = {"ALL": lambda d: pd.Series("ALL", index=d.index), "stratum": lambda d: d.stratum,
            "long_pool": lambda d: pd.Series(np.where(d.long, "L25+L20+EXC", None), index=d.index),
            "words_tercile": lambda d: d.words_t, "ncond_bin": lambda d: d.ncond_bin, "exception_type": lambda d: d.exc_bin,
            "label_tier": lambda d: d.label_tier}
    for rname, (mask, ycol) in regimes.items():
        sub0 = P[mask]
        pos0 = np.where(mask)[0]
        for dim, fn in dims.items():
            lab = fn(sub0)
            for val in sorted(v for v in lab.dropna().unique()):
                m = (lab == val).values
                for rec in cell_stats(sub0[m], ycol, rule_cols, boot, W_all, pos0[m]):
                    rows.append({"regime": rname, "dim": dim, "cell": val, **rec})
    return pd.DataFrame(rows)


# =================================================================================================== graded trace
def graded_trace(y, c) -> dict:
    """(e_t, d_t) at every distinct threshold t of the graded score (flag = c >= t); the ROC = (d_t, 1 - e_t).
    Asserts the trapezoid area equals the tie-aware AUROC to 1e-9."""
    y = np.asarray(y, int)
    c = np.asarray(c, float)
    ts = np.unique(c)
    pts = [(0.0, 0.0)]
    tr = []
    for t in ts[::-1]:
        fl = c >= t
        tpr = fl[y == 1].mean()
        fpr = fl[y == 0].mean()
        tr.append({"t": float(t), "e_t": float(1 - tpr), "d_t": float(fpr)})
        pts.append((fpr, tpr))
    pts.append((1.0, 1.0))
    xs, ys = zip(*pts)
    area = float(np.trapezoid(ys, xs))
    a = auc(y, c)
    assert abs(area - a) < 1e-9, (area, a)
    named = {}
    for nm, en in (("any_peer_agrees (c<1)", c < 1), ("majority END_MAJ (c<0.5)", c < 0.5), ("all_peers_agree (c==0)", c == 0)):
        named[nm] = {"e": float(en[y == 1].mean()), "d": float((~en)[y == 0].mean()),
                     "auroc_b": float(1 - (en[y == 1].mean() + (~en)[y == 0].mean()) / 2)}
    return {"trace": tr, "trapezoid_area": area, "auroc": a, "named_points": named}


# =================================================================================================== GEE
def gee_fit(data: pd.DataFrame, formula: str, groups: str = "sentence_id") -> dict:
    """Binomial-logit GEE, exchangeable working correlation, robust SE; falls back to Independence."""
    out = {"formula": formula, "n": len(data), "n_clusters": int(data[groups].nunique())}
    for cs_name, cs in (("Exchangeable", sm.cov_struct.Exchangeable()), ("Independence", sm.cov_struct.Independence())):
        try:
            with warnings.catch_warnings(record=True) as wl:
                warnings.simplefilter("always")
                m = smf.gee(formula, groups, data=data, family=sm.families.Binomial(), cov_struct=cs)
                r = m.fit(maxiter=200)
            conv_warn = [str(w.message)[:120] for w in wl if "converge" in str(w.message).lower() or "singular" in str(w.message).lower()]
            ciq = r.conf_int()
            if not np.all(np.isfinite(r.bse.values)):
                raise np.linalg.LinAlgError("non-finite SE")
            if conv_warn and cs_name == "Exchangeable":
                raise RuntimeError("; ".join(conv_warn))
            out.update({"cov_struct": cs_name, "warnings": conv_warn,
                        "coef": {k: {"b": float(r.params[k]), "se": float(r.bse[k]), "ci": [float(ciq.loc[k, 0]), float(ciq.loc[k, 1])],
                                     "p": float(r.pvalues[k])} for k in r.params.index}})
            return out
        except (np.linalg.LinAlgError, ValueError, RuntimeError, ZeroDivisionError) as e:  # noqa: PERF203
            logger.warning(f"GEE {cs_name} failed for {formula}: {str(e)[:150]}")
            out[f"fail_{cs_name}"] = str(e)[:200]
    out["coef"] = None
    return out


def vif_table(data: pd.DataFrame, cols: list[str], strat: bool = True) -> dict:
    X = data[cols].astype(float)
    if strat:
        X = pd.concat([X, pd.get_dummies(data.stratum, prefix="st", drop_first=True).astype(float)], axis=1)
    X = sm.add_constant(X)
    return {c: float(variance_inflation_factor(X.values, i)) for i, c in enumerate(X.columns) if c != "const"}


def verdict_slope(coef: dict | None, key: str, want: str) -> str:
    if not coef or key not in coef:
        return "UNTESTABLE"
    lo, hi = coef[key]["ci"]
    if want == "neg":
        return "CONFIRMED" if hi < 0 else ("REFUTED" if lo > 0 else "INCONCLUSIVE")
    return "CONFIRMED" if lo > 0 else ("REFUTED" if hi < 0 else "INCONCLUSIVE")


def zcols(d: pd.DataFrame) -> pd.DataFrame:
    d = d.copy()
    d["zn"] = (d.n_conditions - d.n_conditions.mean()) / d.n_conditions.std()
    d["zw"] = (d.words - d.words.mean()) / d.words.std()
    return d


def mechanism_M1_M2(P: pd.DataFrame, rule_cols: dict) -> dict:
    """M1: endorsed ~ z(n_conditions) + z(words) + C(stratum) among R_AB ERROR rows (prediction: n_conditions < 0).
    M2: divergent ~ z(words) + z(n_conditions) + C(stratum) among R_AB CORRECT rows (prediction: words > 0)."""
    res = {"M1": {}, "M2": {}}
    ab = P[P.in_RAB]
    for rule, col in rule_cols.items():
        for side, yv, dep, key, want in (("M1", 1, "endorsed", "zn", "neg"), ("M2", 0, "divergent", "zw", "pos")):
            base = ab[ab.y_AB == yv].copy()
            base["endorsed"] = base[col].astype(int)
            base["divergent"] = 1 - base["endorsed"]
            variants = {"primary": (zcols(base), f"{dep} ~ zn + zw + C(stratum)")}
            if rule == "MAJ":
                variants["long_pool_only"] = (zcols(base[base.long]), f"{dep} ~ zn + zw + C(stratum)")
                variants["plus_vendor_family"] = (zcols(base), f"{dep} ~ zn + zw + C(stratum) + C(family_vendor)")
                variants["no_stratum_dummies"] = (zcols(base), f"{dep} ~ zn + zw")
                variants["EXPLORATORY_ncond_only"] = (zcols(base), f"{dep} ~ zn")
                variants["EXPLORATORY_words_only"] = (zcols(base), f"{dep} ~ zw")
                ra = base[base.label_tier == "A"]
                variants["R_A_only"] = (zcols(ra), f"{dep} ~ zn + zw + C(stratum)")
                if side == "M2":
                    for cne in (True, False):
                        sub = base[base.correct_not_equivalent == cne]
                        variants[f"CNE={cne}"] = (zcols(sub), f"{dep} ~ zn + zw + C(stratum)")
            for vn, (d, f) in variants.items():
                g = gee_fit(d, f)
                kk = key if key in (g["coef"] or {}) else ("zw" if key == "zn" else "zn")  # EXPLORATORY single-predictor fits
                g["verdict"] = verdict_slope(g["coef"], kk, want)
                g["verdict_on"] = kk
                g["rate"] = float(d[dep].mean())
                res[side][f"{rule}|{vn}"] = g
    base = zcols(ab)
    res["VIF"] = vif_table(base, ["zn", "zw"])
    res["corr_words_ncond_rows"] = float(np.corrcoef(ab.words, ab.n_conditions)[0, 1])
    # d split by correct_not_equivalent (the hypothesis puts d in the CNE rows)
    cor = ab[ab.y_AB == 0]
    res["M2_d_by_CNE"] = {str(k): {"n": int(len(g)), "d_MAJ": float(1 - g["end_MAJ"].mean())} for k, g in cor.groupby("correct_not_equivalent")}
    return res


# =================================================================================================== NET
def _ame(X: np.ndarray, yv: np.ndarray, w: np.ndarray, j: int) -> float:
    m = LogisticRegression(C=1e6, max_iter=500).fit(X, yv, sample_weight=w)
    p = m.predict_proba(X)[:, 1]
    return float(np.average(m.coef_[0][j] * p * (1 - p), weights=w))


def net_test(P: pd.DataFrame, boot: SentBoot, col: str = "end_MAJ", long_only: bool = False) -> dict:
    """Delta(e+d) top vs bottom words tercile (and n_conditions 4+ vs 0-1) with cluster-bootstrap CIs, plus the summed
    average marginal effect per SD (AME_e + AME_d) from plain logistic refits in every replicate."""
    mask = P.in_RAB.values & (P.long.values if long_only else True)
    W = boot.W(mask)
    d = P[mask]
    y = d.y_AB.values.astype(int)
    en = d[col].values.astype(float)
    out = {}
    for nm, lo_m, hi_m in (("words_T3_minus_T1", d.words_t.values == "T1", d.words_t.values == "T3"),
                           ("ncond_4p_minus_01", d.ncond_bin.values == "0-1", d.ncond_bin.values == "4+")):
        def ed(Wm, m):
            with np.errstate(invalid="ignore", divide="ignore"):
                e = (Wm[..., m] @ (en[m] * y[m])) / (Wm[..., m] @ y[m])
                dd = (Wm[..., m] @ ((1 - en[m]) * (1 - y[m]))) / (Wm[..., m] @ (1 - y[m]))
            return e, dd
        one = np.ones(len(d))
        e_lo, d_lo = ed(one, lo_m)
        e_hi, d_hi = ed(one, hi_m)
        eb_lo, db_lo = ed(W, lo_m)
        eb_hi, db_hi = ed(W, hi_m)
        delta = (e_hi + d_hi) - (e_lo + d_lo)
        dB = (eb_hi + db_hi) - (eb_lo + db_lo)
        c = ci(dB)
        verdict = ("IMPROVES_WITH_COMPLEXITY (scatter dominates)" if c[1] is not None and c[1] < 0 else
                   "DEGRADES_WITH_COMPLEXITY (legitimate divergence dominates)" if c[0] is not None and c[0] > 0 else
                   "BALANCED_OR_UNDETERMINED")
        out[nm] = {"delta_e_plus_d": float(delta), "ci": c, "delta_e": float(e_hi - e_lo), "delta_e_ci": ci(eb_hi - eb_lo),
                   "delta_d": float(d_hi - d_lo), "delta_d_ci": ci(db_hi - db_lo), "e_lo": float(e_lo), "d_lo": float(d_lo),
                   "e_hi": float(e_hi), "d_hi": float(d_hi), "n_lo": int(lo_m.sum()), "n_hi": int(hi_m.sum()),
                   "delta_auroc_b": float(-delta / 2), "verdict": verdict,
                   "driver": "e" if abs(e_hi - e_lo) > abs(d_hi - d_lo) else "d"}
    # AME per SD (words and n_conditions), plain logistic with stratum dummies (dropped within the long pool? kept)
    dz = zcols(d)
    X = np.column_stack([dz.zw.values, dz.zn.values, pd.get_dummies(d.stratum, drop_first=True).values.astype(float)])
    err, cor = y == 1, y == 0
    for j, nm in ((0, "words"), (1, "n_conditions")):
        ame_e = _ame(X[err], en[err], np.ones(err.sum()), j)
        ame_d = _ame(X[cor], 1 - en[cor], np.ones(cor.sum()), j)
        bs = []
        for b in range(W.shape[0]):
            w = W[b]
            try:
                bs.append(_ame(X[err], en[err], w[err] + 1e-12, j) + _ame(X[cor], 1 - en[cor], w[cor] + 1e-12, j))
            except ValueError:
                continue
        out[f"AME_sum_per_SD_{nm}"] = {"ame_e": ame_e, "ame_d": ame_d, "sum": ame_e + ame_d, "ci": ci(bs), "n_boot": len(bs)}
    return out


# =================================================================================================== SCATTER
def scatter_index(P_lab: pd.DataFrame, sms: dict, cut: dict, boot_seed: int = 0, B: int = 2000) -> dict:
    """Anna-Karenina quantities over CROSS-FAMILY pairs of labelled LLM rows per sentence.
    SI_err = share of ERROR-ERROR pairs that are eqmv-equivalent (wrong the SAME way), SI_cor for CORRECT-CORRECT,
    SI_mix for ERROR-CORRECT; joint = share of cross-family pairs that are both ERROR (both wrong);
    classes_per_output = #distinct components among ERROR (CORRECT) rows / #rows."""
    sent_rows = []
    pair_rows = []
    for sid, g in P_lab.groupby("sentence_id"):
        sm_ = sms[sid]
        rs = [(r.row_key, sm_.row_node[r.row_key], r.family_vendor, int(r.y_AB)) for r in g.itertuples() if r.row_key in sm_.row_node]
        cnt = defaultdict(list)
        for i in range(len(rs)):
            for j in range(i + 1, len(rs)):
                a, b = rs[i], rs[j]
                if a[2] == b[2]:
                    continue
                t = "EE" if a[3] + b[3] == 2 else ("CC" if a[3] + b[3] == 0 else "EC")
                e = int(sm_.is_eq(a[1], b[1]))
                cnt[t].append(e)
                pair_rows.append({"sentence_id": sid, "pair_type": t, "eq": e})
        errs = [r for r in rs if r[3] == 1]
        cors = [r for r in rs if r[3] == 0]
        n_pairs = sum(len(v) for v in cnt.values())
        st = g.iloc[0]
        sent_rows.append({"sentence_id": sid, "words": st.words, "n_conditions": st.n_conditions, "stratum": st.stratum,
                          "SI_err": np.mean(cnt["EE"]) if cnt["EE"] else np.nan,
                          "SI_cor": np.mean(cnt["CC"]) if cnt["CC"] else np.nan,
                          "SI_mix": np.mean(cnt["EC"]) if cnt["EC"] else np.nan,
                          "joint_fail": len(cnt["EE"]) / n_pairs if n_pairs else np.nan,
                          "same_wrong_any_pair": (sum(cnt["EE"]) / n_pairs) if n_pairs else np.nan,
                          "cpo_err": len({sm_.comp[r[1]] for r in errs}) / len(errs) if len(errs) >= 2 else np.nan,
                          "cpo_cor": len({sm_.comp[r[1]] for r in cors}) / len(cors) if len(cors) >= 2 else np.nan,
                          "n_err_rows": len(errs), "n_cor_rows": len(cors)})
    S = pd.DataFrame(sent_rows)
    q1, q2 = cut["words_tercile_cuts"]
    S["words_t"] = np.where(S.words <= q1, "T1", np.where(S.words <= q2, "T2", "T3"))
    nc = S.n_conditions.fillna(-1).astype(int)
    S["ncond_bin"] = np.where(nc <= 1, "0-1", np.where(nc == 2, "2", np.where(nc == 3, "3", "4+")))
    rng = np.random.default_rng(boot_seed)
    n = len(S)
    Cb = np.stack([np.bincount(rng.integers(0, n, n), minlength=n) for _ in range(B)]).astype(float)
    qty = ["SI_err", "SI_cor", "SI_mix", "joint_fail", "same_wrong_any_pair", "cpo_err", "cpo_cor"]

    def summarise(mask) -> dict:
        o = {}
        for q in qty:
            v = S[q].values
            m = mask & ~np.isnan(v)
            if m.sum() == 0:
                o[q] = {"mean": None, "ci": [None, None], "n_sent": 0}
                continue
            vb = (Cb[:, m] @ v[m]) / Cb[:, m].sum(1)
            o[q] = {"mean": float(v[m].mean()), "ci": ci(vb) if m.sum() >= MIN_SENT else [None, None], "n_sent": int(m.sum())}
        m = mask & ~np.isnan(S.SI_err.values) & ~np.isnan(S.SI_cor.values)
        if m.sum():
            e_b = (Cb[:, m] @ S.SI_err.values[m]) / Cb[:, m].sum(1)
            c_b = (Cb[:, m] @ S.SI_cor.values[m]) / Cb[:, m].sum(1)
            with np.errstate(divide="ignore", invalid="ignore"):
                r_b = c_b / e_b
            r = S.SI_cor.values[m].mean() / S.SI_err.values[m].mean() if S.SI_err.values[m].mean() > 0 else float("inf")
            o["ratio_SI_cor_over_SI_err_same_sentences"] = {"ratio": float(r), "ci": ci(r_b[np.isfinite(r_b)]), "n_sent": int(m.sum())}
            o["diff_SI_cor_minus_SI_err_same_sentences"] = {"diff": float(S.SI_cor.values[m].mean() - S.SI_err.values[m].mean()),
                                                            "ci": ci(c_b - e_b)}
        return o
    out = {"overall": summarise(np.ones(n, bool)), "by_ncond_bin": {}, "by_words_tercile": {}, "by_stratum": {}}
    for b in ["0-1", "2", "3", "4+"]:
        out["by_ncond_bin"][b] = summarise(S.ncond_bin.values == b)
    for b in ["T1", "T2", "T3"]:
        out["by_words_tercile"][b] = summarise(S.words_t.values == b)
    for b in ["L25", "L20", "EXC", "CTRL"]:
        out["by_stratum"][b] = summarise(S.stratum.values == b)
    # pair-level GEE eq ~ C(pair_type) * z(n_conditions)
    PR = pd.DataFrame(pair_rows).merge(S[["sentence_id", "n_conditions", "words"]], on="sentence_id")
    PR["zn"] = (PR.n_conditions - PR.n_conditions.mean()) / PR.n_conditions.std()
    PR["pair_type"] = pd.Categorical(PR.pair_type, categories=["EE", "CC", "EC"])
    out["pair_gee"] = gee_fit(PR, "eq ~ C(pair_type) * zn")
    out["n_pairs"] = {k: int(v) for k, v in PR.pair_type.value_counts().items()}
    # prediction check: SI_err low and falling with n_conditions; SI_cor high
    co = out["pair_gee"]["coef"] or {}
    out["prediction"] = {"SI_err_falls_with_ncond": verdict_slope(co, "zn", "neg"),
                         "SI_cor_gt_SI_err": ("CONFIRMED" if (out["overall"].get("diff_SI_cor_minus_SI_err_same_sentences", {}).get("ci", [None])[0] or -1) > 0
                                              else "NOT_CONFIRMED")}
    return {"summary": out, "sentence_table": S}


# =================================================================================================== M3-local
def m3_local(P: pd.DataFrame, boot: SentBoot, exp6_judge_slope) -> dict:
    """Row-level correctness of the binary decision ~ z(words) on R_AB: consensus END_MAJ vs the local judge thresholded
    at the flag rate of END_MAJ (no frozen judge threshold exists in exp 5)."""
    mask = P.in_RAB.values & P.judge_local.notna().values
    d = zcols(P[mask])
    y = d.y_AB.values.astype(int)
    b_c = 1 - d.end_MAJ.values.astype(int)
    rate = b_c.mean()
    js = d.judge_local.values.astype(float)
    # The judge score is discrete (0, .05, .10, ...), so no plain threshold reproduces END_MAJ's flag rate.
    # PRIMARY: exact flag-rate match = flag the top round(rate*n) rows by (judge score, deterministic tie-break
    # sha1(row_key)), i.e. a random split of the boundary tie group. SENSITIVITY: the nearest plain threshold.
    import hashlib
    cands = np.unique(js)
    t = float(min(cands, key=lambda v: (abs(np.mean(js >= v) - rate), v)))
    b_thr = (js >= t).astype(int)
    tb = np.array([int(hashlib.sha1(f"M3|{rk}".encode()).hexdigest()[:12], 16) / 16 ** 12 for rk in d.row_key])
    order = np.lexsort((tb, js))[::-1]  # descending by score, then tie-break
    n_flag = int(round(rate * len(js)))
    b_j = np.zeros(len(js), int)
    b_j[order[:n_flag]] = 1
    d["correct_c"] = (b_c == y).astype(int)
    d["correct_j"] = (b_j == y).astype(int)
    d["correct_j_thr"] = (b_thr == y).astype(int)
    gc = gee_fit(d, "correct_c ~ zw")
    gj = gee_fit(d, "correct_j ~ zw")
    gjt = gee_fit(d, "correct_j_thr ~ zw")
    W = boot.W(mask)
    X = d[["zw"]].values

    def slope(yv, w):
        return LogisticRegression(C=1e6, max_iter=500).fit(X, yv, sample_weight=w).coef_[0][0]
    diffs, diffs_t = [], []
    for b in range(W.shape[0]):
        try:
            s_c = slope(d.correct_c.values, W[b] + 1e-12)
            diffs.append(s_c - slope(d.correct_j.values, W[b] + 1e-12))
            diffs_t.append(s_c - slope(d.correct_j_thr.values, W[b] + 1e-12))
        except ValueError:
            continue
    sc = gc["coef"]["zw"]["b"] if gc["coef"] else None
    sj = gj["coef"]["zw"]["b"] if gj["coef"] else None
    sjt = gjt["coef"]["zw"]["b"] if gjt["coef"] else None
    return {"n": int(mask.sum()), "flag_rate_END_MAJ": float(rate),
            "judge_matching": "exact flag-rate match: top round(rate*n) rows by judge score, boundary ties split by sha1('M3|'+row_key)",
            "judge_flag_rate": float(b_j.mean()), "gee_consensus": gc, "gee_judge": gj,
            "slope_consensus_minus_judge": (sc - sj) if (sc is not None and sj is not None) else None,
            "slope_diff_ci": ci(diffs), "n_boot": len(diffs),
            "sensitivity_nearest_threshold": {"threshold": t, "judge_flag_rate": float(b_thr.mean()), "gee_judge": gjt,
                                              "slope_consensus_minus_judge": (sc - sjt) if (sc is not None and sjt is not None) else None,
                                              "slope_diff_ci": ci(diffs_t), "acc_judge": float(d.correct_j_thr.mean())},
            "exp6_published_judge_slope_per_SD": exp6_judge_slope,
            "note_on_comparability": "exp 6's slope is a GEE of judge-correctness at ITS OWN operating point; the rows here are the same R_AB rows but the judge is binarised at END_MAJ's flag rate",
            "acc_consensus": float(d.correct_c.mean()), "acc_judge": float(d.correct_j.mean()),
            "label": "SECONDARY (the pre-registered M3 vs the API judge belongs to the T1 experiment)"}
