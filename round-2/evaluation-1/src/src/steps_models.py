"""Steps 6-7: SCREEN-ONLY PEER+TEXT preview (cross-fitted, exp D's model spec) and P1/P2 mechanism pre-tests."""
from __future__ import annotations

import numpy as np
import pandas as pd
from loguru import logger
from sklearn.linear_model import LogisticRegression

import stats_utils as su

PT = ["c_score", "bow_uncarried", "l3_score"]
PT_TEXT = ["bow_uncarried", "l3_score"]
PTJ = PT + ["judge_cheap_disg"]
PTG = PT + ["medoid_depth", "cluster_entropy"]
# exp D prereg.json combination_feature_sets: S4 = S1 u S2 u S3 u {judge_cheap_orig, judge_cheap2_orig}
S1 = ["parse_fail", "pilot_joint_conflict", "pilot_arity_incons", "pilot_shape_incons", "pilot_dangling", "pilot_undeclared", "pilot_rerun_jacc"]
S2 = ["rt_nli_min", "rt_nli_fwd", "rt_nli_bwd", "rt_nli_contra", "rt_embed_cos", "rt_reformalise_eq"]
S3 = ["judge_cheap_disg", "judge_cheap2_disg"]
S4 = S1 + S2 + S3 + ["judge_cheap_orig", "judge_cheap2_orig"]
MODELS = {"PT_oof": PT, "PTJ_oof": PTJ, "PTg_oof": PTG, "S4_refit_oof": S4, "S4PT_oof": S4 + PT, "PTtext_oof": PT_TEXT}
FINE = ["NEG", "REV", "QUANT", "SWAP", "SCOPE", "BIND", "RESTR", "CONN", "MOVE", "DROP", "ADD", "UNGLUE"]
P1_STRUCT = ["QUANT", "SCOPE", "BIND", "SWAP", "NEG"]
NOTE = "SCREEN_PREVIEW_NOT_CONFIRMATION; coefficients are descriptive, not for use as prereg weights; iteration-2 EXP1 fits its own"


# ------------------------------------------------------------------------------------------------ design + folds
def design(sub: pd.DataFrame, feats: list[str]) -> tuple[np.ndarray, list[str]]:
    """Exp D combo_oof design: raw oriented feature (NaN kept for standardisation), plus a missing indicator column
    for every feature that has any missing value; NaN -> 0 after standardisation."""
    X, cols = [], []
    for f in feats:
        v = sub[f].values.astype(float)
        X.append(v)
        cols.append(f)
        miss = np.isnan(v)
        if miss.any():
            X.append(miss.astype(float))
            cols.append(f + "__missing")
    return np.vstack(X).T, cols


def assign_folds(sub: pd.DataFrame, d_folds: dict, seed: int) -> tuple[np.ndarray, int]:
    """seed 0: exp D's data/folds.json ids; items without a D fold inherit their sentence's D fold, else a seeded
    cluster-level assignment. seeds 1-4: every sentence cluster shuffled with default_rng(seed), fold = rank % 5."""
    clusters = sub.cluster.values
    uc = sorted(set(clusters))
    rng = np.random.default_rng(seed)
    perm = rng.permutation(len(uc))
    own = {c: int(perm[i] % 5) for i, c in enumerate(uc)}
    if seed != 0:
        return np.array([own[c] for c in clusters]), len(sub)
    cl_fold = {}
    for k, c in zip(sub.index, clusters):
        if k in d_folds:
            cl_fold.setdefault(c, int(d_folds[k]))
    fold, n_new = [], 0
    for k, c in zip(sub.index, clusters):
        if k in d_folds:
            fold.append(int(d_folds[k]))
        elif c in cl_fold:
            fold.append(cl_fold[c])
        else:
            fold.append(own[c])
            n_new += 1
    return np.array(fold), n_new


def fit_predict(Xtr, ytr, Xte):
    mu = np.nanmean(Xtr, 0)
    mu = np.where(np.isnan(mu), 0, mu)
    sd = np.nanstd(Xtr, 0)
    sd = np.where((sd == 0) | np.isnan(sd), 1, sd)
    A = np.nan_to_num((Xtr - mu) / sd)
    Bm = np.nan_to_num((Xte - mu) / sd)
    clf = LogisticRegression(C=1.0, max_iter=2000)
    clf.fit(A, ytr)
    return clf.predict_proba(Bm)[:, 1], clf.coef_[0]


def cross_fit(X, y, fold):
    oof = np.zeros(len(y))
    coefs = []
    for i in sorted(set(fold)):
        tr, te = fold != i, fold == i
        if len(np.unique(y[tr])) < 2 or te.sum() == 0:
            oof[te] = np.mean(y[tr])
            continue
        p, c = fit_predict(X[tr], y[tr], X[te])
        oof[te] = p
        coefs.append(c)
    return oof, np.mean(coefs, 0) if coefs else None


# ------------------------------------------------------------------------------------------------ step 6
def step6_regime(sub: pd.DataFrame, y: np.ndarray, d_folds: dict, n_seeds: int = 5) -> dict:
    """Cross-fitted PEER+TEXT variants + refitted S4 on one regime's common items. Adds *_oof columns to sub."""
    res = {"note": NOTE, "models": {}}
    folds = {}
    for seed in range(n_seeds):
        folds[seed], n_new = assign_folds(sub, d_folds, seed)
        if seed == 0:
            res["n_items_without_D_fold_assigned_by_own_split"] = int(n_new)
            res["n_items_with_D_fold"] = int(sum(k in d_folds for k in sub.index))
    for name, feats in MODELS.items():
        X, cols = design(sub, feats)
        per_seed = []
        coef0 = None
        for seed in range(n_seeds):
            oof, coef = cross_fit(X, y, folds[seed])
            if seed == 0:
                sub[name] = oof
                coef0 = coef
            per_seed.append(su.auroc(y, oof))
        res["models"][name] = {"features": feats, "oof_auroc_seed0_Dfolds": per_seed[0], "oof_auroc_mean_5seeds": float(np.mean(per_seed)),
                               "oof_auroc_sd_5seeds": float(np.std(per_seed, ddof=1)) if n_seeds > 1 else None,
                               "oof_auroc_per_seed": per_seed,
                               "std_coefficients_mean_over_folds_seed0": dict(zip(cols, [float(c) for c in coef0])) if coef0 is not None else None}
    # paired deltas over OOF predictions (seed 0) -- bootstrap does NOT refit (understates model-selection variance)
    cb = su.ClusterBoot(list(sub.cluster.values), B=2000)
    W = cb.item_W()
    pairs = [("PT_oof", "judge_cheap_disg"), ("PTJ_oof", "judge_cheap_disg"), ("S4PT_oof", "S4_refit_oof"), ("PTg_oof", "PT_oof"),
             ("PT_oof", "c_score"), ("PT_oof", "bow_uncarried"), ("PT_oof", "l3_score"), ("S4_refit_oof", "judge_cheap_disg"),
             ("PT_oof", "best_baseline_oof")]
    for a, b in pairs:
        if a not in sub.columns or b not in sub.columns or sub[a].isna().any() or sub[b].isna().any():
            continue
        d = su.boot_auc_w(y, sub[a].values, W) - su.boot_auc_w(y, sub[b].values, W)
        ci = su.ci95(d)
        # spread of the point Delta across fold seeds for model-vs-model pairs
        res[f"delta_{a}_vs_{b}"] = {"delta": su.auroc(y, sub[a].values) - su.auroc(y, sub[b].values), "ci": ci,
                                    "p_boot": su.boot_p_two_sided(d), "delong_p": su.delong_paired(y, sub[a].values, sub[b].values)["p"]}
    for a, b in [("PT_oof", "judge_cheap_disg"), ("PTJ_oof", "judge_cheap_disg"), ("S4PT_oof", "S4_refit_oof")]:
        ds = []
        if f"delta_{a}_vs_{b}" not in res:
            continue
        for seed in range(n_seeds):
            Xa, _ = design(sub, MODELS[a])
            oa, _ = cross_fit(Xa, y, folds[seed])
            if b in MODELS:
                Xb, _ = design(sub, MODELS[b])
                ob, _ = cross_fit(Xb, y, folds[seed])
            else:
                ob = sub[b].values
            ds.append(su.auroc(y, oa) - su.auroc(y, ob))
        res[f"delta_{a}_vs_{b}"]["delta_mean_5seeds"] = float(np.mean(ds))
        res[f"delta_{a}_vs_{b}"]["delta_sd_5seeds"] = float(np.std(ds, ddof=1))
    return res


def f3_preview(df: pd.DataFrame, regimes: dict, commons: dict, d_folds: dict) -> dict:
    """Fit PT on track-L items whose solver-consistent label agrees with E's adjudicated label; score the disagreeing
    (flipped) items out of sample; threshold at FA=0.10 on the agreeing CORRECT items (all LLM-system outputs)."""
    L = df[df.track == "L"]
    ycons = regimes["R_SOLVER_CONS"]["y"]
    base = L.loc[ycons.index]
    base = base[base.E_final_label.isin(["CORRECT", "ERROR"]) & base[PT].notna().all(axis=1)]
    yc = ycons.loc[base.index].values
    ye = (base.E_final_label == "ERROR").astype(int).values
    agree = yc == ye
    ag, dis = base[agree].copy(), base[~agree].copy()
    yag = yc[agree]
    X, cols = design(ag, PT)
    fold, _ = assign_folds(ag, d_folds, 0)
    oof, coef = cross_fit(X, yag, fold)
    Xd, _ = design(dis, PT)
    pd_, coef_full = fit_predict(X, yag, Xd) if len(dis) else (np.array([]), None)
    rule = su.matched_fa_rule(oof[yag == 0], 0.10)
    res = {"note": NOTE, "n_agreeing": int(agree.sum()), "n_agreeing_err": int(yag.sum()), "n_disagreeing": int((~agree).sum()),
           "oof_auroc_on_agreeing": su.auroc(yag, oof), "threshold_rule_FA0.10": {"v": rule[0], "q": rule[1], "achieved_fa_agreeing": rule[2]},
           "std_coefficients_full_fit": dict(zip(cols, [float(c) for c in coef_full])) if coef_full is not None else None}
    ydis_E = (dis.E_final_label == "ERROR").astype(int).values
    fp = su.flag_prob(pd_, rule)
    res["flipped_CORRECT_to_ERROR_n"] = int(ydis_E.sum())
    res["recall_on_flipped_CORRECT_to_ERROR_at_FA0.10"] = float(fp[ydis_E == 1].mean()) if ydis_E.sum() else None
    res["flag_rate_on_flipped_ERROR_to_CORRECT"] = float(fp[ydis_E == 0].mean()) if (ydis_E == 0).sum() else None
    # F3 score for every scorable L item: OOF on agreeing items, out-of-sample full fit elsewhere
    allL = L[L[PT].notna().all(axis=1)].copy()
    Xall, _ = design(allL, PT)
    p_all, _ = fit_predict(X, yag, Xall)
    s = pd.Series(p_all, index=allL.index)
    s.loc[ag.index] = oof
    per_reg = {}
    for rn, reg in regimes.items():
        if reg["track"] != "L":
            continue
        sub, y = commons[rn]
        sc = s.reindex(sub.index)
        ok = sc.notna().values
        f = su.flag_prob(sc.values[ok], rule)
        yy = y[ok]
        fa = float(f[yy == 0].mean()) if (yy == 0).sum() else None
        rec = float(f[yy == 1].mean()) if (yy == 1).sum() else None
        fused_fa = float((sub.fused_flag.values[ok][yy == 0] > 0.5).mean()) if (yy == 0).sum() else None
        per_reg[rn] = {"n": int(ok.sum()), "achieved_FA_on_CORRECT": fa, "recall": rec, "target_FA": 0.10,
                       "fused_H_shipped_flag_FA_same_items": fused_fa, "auroc_F3_score": su.auroc(yy, sc.values[ok])}
    res["per_regime"] = per_reg
    return res


# ------------------------------------------------------------------------------------------------ step 7
def type_columns(sub: pd.DataFrame, y: np.ndarray, adjudicated: bool) -> pd.DataFrame:
    T = pd.DataFrame(index=sub.index)
    ops_col = "E_repair_ops" if adjudicated else "ops_C"
    ops = []
    for k, r in sub.iterrows():
        o = r[ops_col]
        if not isinstance(o, list):
            o = r["ops_C"] if isinstance(r["ops_C"], list) else (r["ops_D"] if isinstance(r["ops_D"], list) else [])
        ops.append([x for x in o if isinstance(x, str)])
    T["ops"] = ops
    T["coarse"] = [("COMPOUND" if not o else su.op_class(o)) for o in ops]
    for f in FINE:
        T[f"op_{f}"] = [f in o for o in ops]
    T["meaning_rename"] = (sub.E_label_tier == "B") & (sub.E_auto_label == "VOCAB_GRAN") if adjudicated else False
    T["endorsed"] = sub.medoid_depth == 0
    T["y"] = y
    return T


def step7_regime(sub: pd.DataFrame, y: np.ndarray, adjudicated: bool, metrics: list[str], B: int = 2000) -> dict:
    T = type_columns(sub, y, adjudicated)
    cb = su.ClusterBoot(list(sub.cluster.values), B=B)
    W = cb.item_W()
    err = y == 1
    cells = {"ALL": err}
    for c in ["POLARITY", "COVERAGE", "STRUCT", "MIXED", "COMPOUND"]:
        cells[f"coarse:{c}"] = err & (T.coarse.values == c)
    for f in FINE:
        cells[f"op:{f}"] = err & T[f"op_{f}"].values
    if adjudicated:
        cells["MEANING_RENAME"] = err & T.meaning_rename.values.astype(bool)
    cells["PEER_ENDORSED"] = err & T.endorsed.values
    cells["NON_ENDORSED"] = err & ~T.endorsed.values
    rows = []
    fps = {}
    for f in (0.10, 0.20):
        for m in metrics:
            s = sub[m].values.astype(float)
            rule = su.matched_fa_rule(s[~err], f)
            fps[(m, f)] = su.flag_prob(s, rule)
            for cname, mask in cells.items():
                n = int(mask.sum())
                k = float(fps[(m, f)][mask].sum())
                lo, hi = su.wilson(k, n) if n else (None, None)
                rows.append({"fa_target": f, "achieved_fa": rule[2], "metric": m, "cell": cname, "n_err": n,
                             "recall": k / n if n else None, "wilson_lo": lo, "wilson_hi": hi, "informative": n >= 15})
    tab = pd.DataFrame(rows)
    # recall differences c_score - text with cluster bootstrap (thresholds fixed at full-sample values)
    drows = []
    for f in (0.10, 0.20):
        for text in ("bow_uncarried", "l3_score"):
            for cname, mask in cells.items():
                n = int(mask.sum())
                if n == 0:
                    continue
                a, b = fps[("c_score", f)], fps[(text, f)]
                Wm = W[:, mask]
                den = Wm.sum(1)
                with np.errstate(invalid="ignore", divide="ignore"):
                    d = (Wm @ a[mask] - Wm @ b[mask]) / den
                ci = su.ci95(d)
                drows.append({"fa_target": f, "text_metric": text, "cell": cname, "n_err": n, "informative": n >= 15,
                              "diff_cscore_minus_text": float(a[mask].mean() - b[mask].mean()), "ci_lo": ci[0], "ci_hi": ci[1]})
    dtab = pd.DataFrame(drows)
    verdicts = {}
    for f in (0.10, 0.20):
        for text in ("bow_uncarried", "l3_score"):
            dd = dtab[(dtab.fa_target == f) & (dtab.text_metric == text)].set_index("cell")
            inf = [c for c in [f"op:{o}" for o in P1_STRUCT] if c in dd.index and dd.loc[c, "informative"]]
            pos = [c for c in inf if dd.loc[c, "diff_cscore_minus_text"] > 0]
            ci_pos = [c for c in inf if dd.loc[c, "ci_lo"] is not None and dd.loc[c, "ci_lo"] > 0]
            if not inf:
                cond1 = None
            else:
                cond1 = bool((len(ci_pos) >= 1 and len(pos) == len(inf)) or len(pos) >= 4)
            e = dd.loc["PEER_ENDORSED"] if "PEER_ENDORSED" in dd.index else None
            cond2 = bool(e is not None and e["ci_hi"] is not None and e["ci_hi"] < 0)
            if cond1 is None:
                v = "PARTIAL_STRUCT_UNTESTABLE" if cond2 else "UNTESTABLE_STRUCT_AND_ENDORSED_NS"
            elif cond1 and cond2:
                v = "CONFIRMED"
            elif cond1 or cond2:
                v = "PARTIAL"
            else:
                v = "REFUTED"
            supp = {c: [dd.loc[c, "n_err"], dd.loc[c, "diff_cscore_minus_text"], dd.loc[c, "ci_lo"], dd.loc[c, "ci_hi"]]
                    for c in ("coarse:COMPOUND", "coarse:COVERAGE", "coarse:POLARITY", "coarse:STRUCT", "MEANING_RENAME", "NON_ENDORSED", "PEER_ENDORSED", "ALL")
                    if c in dd.index}
            verdicts[f"FA{f:.2f}_{text}"] = {"verdict": v, "code": {"CONFIRMED": 1.0, "PARTIAL": 0.5, "PARTIAL_STRUCT_UNTESTABLE": 0.5}.get(v, 0.0),
                                             "informative_struct_cells": inf, "cells_peers_gt_text_point": pos,
                                             "cells_peers_gt_text_CI": ci_pos, "cond1_peers_beat_text_on_struct": cond1,
                                             "cond2_text_beats_peers_on_endorsed_CI": cond2,
                                             "endorsed_diff": None if e is None else [e["diff_cscore_minus_text"], e["ci_lo"], e["ci_hi"]],
                                             "supplementary_cells_[n_err,diff,ci_lo,ci_hi]": supp,
                                             "note": ("fine structural operator cells (QUANT/SCOPE/BIND/SWAP/NEG) all have <15 errors on the screen "
                                                      "(most errors are COMPOUND = no repair found, or ADD/DROP), so the structural clause is UNTESTABLE here; "
                                                      "coarse/COMPOUND cells are reported as a supplementary, non-prereg view") if not inf else ""}
    # ---------------- P2: disjointness + exact placement-value gain decomposition
    p2 = {}
    idx_res = [su.resample_indices(cb.cid, cb.W, b) for b in range(B)]
    for grp, gm in [("errors", err), ("correct", ~err)]:
        for other in ("bow_uncarried", "l3_score", "PTtext_oof"):
            a, b = sub.c_score.values[gm], sub[other].values[gm]
            pt = su.spearman(a, b)
            gidx = np.where(gm)[0]
            pos_in = -np.ones(len(sub), dtype=int)
            pos_in[gidx] = np.arange(len(gidx))
            bs = []
            for ii in idx_res[:1000]:
                jj = pos_in[ii]
                jj = jj[jj >= 0]
                bs.append(su.spearman(a[jj], b[jj]))
            ci = su.ci95(np.array(bs))
            p2[f"spearman_c_score_vs_{other}_{grp}"] = {"rho": pt, "ci": ci, "n": int(gm.sum())}
    e_main = p2["spearman_c_score_vs_PTtext_oof_errors"]
    p2["P2a_verdict"] = "CONFIRMED" if (e_main["ci"][1] is not None and e_main["ci"][1] < 0.4) else ("PARTIAL" if e_main["rho"] < 0.4 else "REFUTED")
    singles = {m: su.auroc(y, sub[m].values) for m in ("c_score", "bow_uncarried", "l3_score")}
    best = max(singles, key=singles.get)
    endorsed = T.endorsed.values
    dec = {}
    for comp_name, comp in [("PT_vs_best_single", best), ("PT_vs_judge", "judge_cheap_disg"), ("PT_vs_c_score", "c_score"),
                             ("PT_vs_bow_uncarried", "bow_uncarried"), ("PT_vs_l3_score", "l3_score")]:
        dec[comp_name] = decompose(y, sub.PT_oof.values, sub[comp].values, endorsed, W)
        dec[comp_name]["comparator"] = comp
    p2["decomposition"] = dec
    p2["best_single"] = best
    p2["single_aurocs"] = singles
    sh = dec["PT_vs_best_single"]
    if sh["delta"] <= 0:
        p2["P2b_verdict"] = "UNDEFINED_DELTA_LE_0"
    elif sh["endorsed_share"] >= 0.5:
        p2["P2b_verdict"] = "CONFIRMED" if (sh["delta_ci"][0] is not None and sh["delta_ci"][0] > 0) else "CONFIRMED_POINT_ONLY_DELTA_CI_INCLUDES_0"
    else:
        p2["P2b_verdict"] = "REFUTED"
    p2["P2b_note"] = ("The endorsed share depends on WHICH single component is the comparator: vs c_score the text features must add on "
                      "peer-endorsed errors (consensus blind spot); vs a text feature the peers add on non-endorsed errors. See decomposition.PT_vs_*.")
    p2["peer_endorsed_share_of_errors"] = float(endorsed[err].mean())
    return {"recall_table": tab, "diff_table": dtab, "P1": verdicts, "P2": p2}


def decompose(y, s_new, s_old, endorsed, W) -> dict:
    """AUROC = mean over errors of V(e) (share of CORRECT scored below e, ties 0.5). Delta = mean_e[V_new - V_old],
    split exactly into endorsed-error and non-endorsed-error parts; plus the CORRECT-side view V(c) = share of errors
    above c, split by whether the CORRECT item is peer-endorsed."""
    err, cor = y == 1, y == 0

    def pv(s):
        se, sc = s[err], s[cor]
        M = (se[:, None] > sc[None, :]).astype(float) + 0.5 * (se[:, None] == sc[None, :])
        return M  # n_err x n_cor

    Mn, Mo = pv(s_new), pv(s_old)
    Vn, Vo = Mn.mean(1), Mo.mean(1)
    dV = Vn - Vo
    ne = err.sum()
    end_e = endorsed[err]
    delta = float(dV.mean())
    part_end = float(dV[end_e].sum() / ne)
    part_non = float(dV[~end_e].sum() / ne)
    # bootstrap with weights (errors and corrects re-weighted by cluster multiplicity)
    We, Wc = W[:, err], W[:, cor]
    with np.errstate(invalid="ignore", divide="ignore"):
        Vn_b = (Wc @ Mn.T) / Wc.sum(1, keepdims=True)  # B x n_err
        Vo_b = (Wc @ Mo.T) / Wc.sum(1, keepdims=True)
        dVb = Vn_b - Vo_b
        tot = We.sum(1)
        d_b = (We * dVb).sum(1) / tot
        pe_b = (We[:, end_e] * dVb[:, end_e]).sum(1) / tot
        pn_b = (We[:, ~end_e] * dVb[:, ~end_e]).sum(1) / tot
        share_b = np.where(d_b > 0, pe_b / d_b, np.nan)
    # CORRECT side
    Uc_n, Uc_o = Mn.mean(0), Mo.mean(0)
    end_c = endorsed[cor]
    nc = cor.sum()
    out = {"delta": delta, "delta_ci": su.ci95(d_b), "endorsed_part_auroc_units": part_end, "endorsed_part_ci": su.ci95(pe_b),
           "nonendorsed_part_auroc_units": part_non, "nonendorsed_part_ci": su.ci95(pn_b),
           "endorsed_share": (part_end / delta) if delta > 0 else None, "endorsed_share_ci": su.ci95(share_b) if delta > 0 else [None, None],
           "n_err_endorsed": int(end_e.sum()), "n_err_nonendorsed": int((~end_e).sum()),
           "identity_check_abs_err": float(abs(delta - (part_end + part_non))),
           "correct_side_delta_endorsed_correct": float((Uc_n - Uc_o)[end_c].sum() / nc),
           "correct_side_delta_nonendorsed_correct": float((Uc_n - Uc_o)[~end_c].sum() / nc)}
    return out


def reproduce_c_endorsement(df: pd.DataFrame) -> dict:
    """Reproduce exp C's blind-spot numbers (38% endorsed; POLARITY 5%, COVERAGE 41%, STRUCT 57%) on C's own labels."""
    L = df[(df.track == "L") & (df.lab_C == "ERROR") & df.c_score.notna()]
    end = L.medoid_depth == 0
    cls = L.ops_C.apply(lambda o: "COMPOUND" if not isinstance(o, list) or not o else su.op_class(o))
    out = {"n": len(L), "endorsed_share": float(end.mean())}
    for c in ["POLARITY", "COVERAGE", "STRUCT", "MIXED", "COMPOUND"]:
        m = cls == c
        out[f"endorsed_share_{c}"] = float(end[m].mean()) if m.sum() else None
        out[f"n_{c}"] = int(m.sum())
    out["expected"] = "0.3815 overall; POLARITY 0.05, COVERAGE 0.41, STRUCT 0.57 (exp C summary)"
    return out
