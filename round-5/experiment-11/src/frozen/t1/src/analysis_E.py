"""Meta-evaluation of every baseline on held-out dataset E (analyses (a)-(k) of prereg_baselines.json).

This is the ONLY module that joins scores to labels; it is called by method.py --stage analysis after the prereg check
(load_E(blind=False) refuses to load labels otherwise). All scores are oriented: higher = more likely UNFAITHFUL.
Bootstrap: 2,000 sentence-cluster resamples, seed 0, SAME resamples for every metric inside a set (paired deltas).
"""
from __future__ import annotations

import math
from collections import Counter, defaultdict

import numpy as np
from loguru import logger
from scipy import stats
from sklearn.metrics import roc_auc_score

from .analysis import ClusterBoot, auc_w, boot_auc, ci, delong, evaluate_set, fill, tie_rate

NA, FAIL = "NA", "FAIL"
STRATA = ["L25", "L20", "EXC", "CTRL"]


# ------------------------------------------------------------------ table helpers
def make_table(rows, cols, status, fail_fill, clusters):
    """rows: list of unit dicts (row_key, item_id); cols {m: {item_id: v}}; status {m: {item_id: ok|fail|na}}."""
    T = {"_cluster": {}, "_max": dict(fail_fill)}
    for m in cols:
        T[m] = {}
    for r in rows:
        k = r["row_key"]
        T["_cluster"][k] = clusters[k]
        for m in cols:
            st = status[m].get(r["item_id"], "na")
            v = cols[m].get(r["item_id"])
            if st == "fail":
                T[m][k] = FAIL
            elif st == "na" or v is None:
                T[m][k] = NA
            else:
                T[m][k] = float(v)
    return T


def arr(T, m, keys):
    s, app, fl = fill([T[m][k] for k in keys], T["_max"][m])
    return np.where(app, s, np.nan), app, fl


def _r(x, n=4):
    return None if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))) else round(float(x), n)


# ------------------------------------------------------------------ (a) + (b)
def eval_block(name, keys, y, T, thr, metrics, bar, compute_delta=True):
    """AUROC/AUPRC/threshold stats for every metric + paired Δ vs the bar (bootstrap CI + DeLong)."""
    res, cb, boots = evaluate_set(name, keys, y, T, thr, metrics)
    out = {"n": len(keys), "n_pos": int(y.sum()), "n_neg": int(len(y) - y.sum()), "n_sentences": len(set(T["_cluster"][k] for k in keys)),
           "metrics": {m: {kk: (_r(vv) if isinstance(vv, float) else vv) for kk, vv in r.items()} for m, r in res.items()}}
    pos_s = {T["_cluster"][k] for k, yy in zip(keys, y) if yy == 1}
    neg_s = {T["_cluster"][k] for k, yy in zip(keys, y) if yy == 0}
    out["testable"] = bool(out["n_pos"] >= 50 and out["n_neg"] >= 50 and len(pos_s) >= 25 and len(neg_s) >= 25)
    if compute_delta and bar in boots:
        sb, _, _ = arr(T, bar, keys)
        d = {}
        for m, bm in boots.items():
            if m == bar or res[m].get("auroc") is None:
                continue
            sm, _, _ = arr(T, m, keys)
            ok = ~np.isnan(sm) & ~np.isnan(sb)
            if ok.sum() < len(keys) * 0.9:  # subset metrics are compared on their own subset elsewhere
                continue
            diff = bm - boots[bar]
            dl = delong(y, sm, sb)
            d[m] = {"delta": _r(res[m]["auroc"] - res[bar]["auroc"]), "ci": [_r(x) for x in ci(diff)],
                    "delong_p": _r(dl[3], 6) if dl else None, "p_boot_le0": _r(float(np.mean(diff[~np.isnan(diff)] <= 0)))}
        out["paired_vs_bar"] = {"bar": bar, "deltas": d}
    return out, cb, boots


# ------------------------------------------------------------------ (c) frontier / larger judge on the frame
def ipw_auc_boot(y, s, w_ipw, cb):
    ok = ~np.isnan(s)
    pt = roc_auc_score(y[ok], s[ok], sample_weight=w_ipw[ok]) if len(np.unique(y[ok])) == 2 else np.nan
    bs = []
    for b in range(cb.B):
        w = cb.item_weights(b) * w_ipw
        m = ok & (w > 0)
        if len(np.unique(y[m])) < 2:
            bs.append(np.nan)
            continue
        bs.append(roc_auc_score(y[m], s[m], sample_weight=w[m]))
    return float(pt), np.array(bs)


def frame_analysis(frame_rows, labels, T, pairs, clusters):
    keys = [r["row_key"] for r in frame_rows if r["row_key"] in labels]
    y = np.array([labels[k] for k in keys])
    ipw = np.array([1.0 / r["incl_prob"] for r in frame_rows if r["row_key"] in labels])
    cb = ClusterBoot([clusters[k] for k in keys])
    out = {"n": len(keys), "n_pos": int(y.sum()), "n_neg": int(len(y) - y.sum()), "contrasts": {}, "aurocs": {}}
    cache = {}
    for a, b in pairs:
        for m in (a, b):
            if m in cache or m not in T:
                continue
            s, _, fl = arr(T, m, keys)
            if np.isnan(s).all():
                continue
            ua = auc_w(y, s)
            ub = boot_auc(y, s, cb)
            wa, wb = ipw_auc_boot(y, s, ipw, cb)
            cache[m] = (s, ua, ub, wa, wb)
            out["aurocs"][m] = {"auroc": _r(ua), "ci": [_r(x) for x in ci(ub)], "auroc_ipw": _r(wa), "ci_ipw": [_r(x) for x in ci(wb)],
                                "n_fail": int(fl.sum())}
        if a in cache and b in cache:
            sa, ua, ba, wa, wba = cache[a]
            sb, ub_, bb, wb_, wbb = cache[b]
            dl = delong(y, sa, sb)
            out["contrasts"][f"{a} - {b}"] = {"delta": _r(ua - ub_), "ci": [_r(x) for x in ci(ba - bb)], "delong_p": _r(dl[3], 6) if dl else None,
                                              "delta_ipw": _r(wa - wb_), "ci_ipw": [_r(x) for x in ci(wba - wbb)]}
    return out


# ------------------------------------------------------------------ (d) contamination
def contamination(comp_pairs, keys_E, keys_G, lab, T, clusters):
    """DiD = Δ_disg(GOLDSYS) − Δ_disg(E_POOL), Δ_disg = AUROC_orig − AUROC_disg (same joint sentence bootstrap);
    gold-recognition probe: P(say faithful | ERROR) orig − disg on GOLDSYS minus the same on E_POOL ERROR rows."""
    keys = keys_E + keys_G
    y = np.array([lab[k] for k in keys])
    inE = np.array([True] * len(keys_E) + [False] * len(keys_G))
    cb = ClusterBoot([clusters[k] for k in keys])
    out = {}
    for name, (mo, md) in comp_pairs.items():
        if mo not in T or md not in T:
            continue
        so, _, _ = arr(T, mo, keys)
        sd, _, _ = arr(T, md, keys)
        if np.isnan(so[inE]).all() or np.isnan(so[~inE]).all():
            out[name] = {"note": "no rows in one arm"}
            continue
        r = {}
        bo = {}
        for arm, msk in (("E_POOL", inE), ("GOLDSYS", ~inE)):
            so_a = np.where(msk, so, np.nan)
            sd_a = np.where(msk, sd, np.nan)
            ao, ad = auc_w(y, so_a), auc_w(y, sd_a)
            bo_, bd_ = boot_auc(y, so_a, cb), boot_auc(y, sd_a, cb)
            bo[arm] = bo_ - bd_
            r[arm] = {"auroc_orig": _r(ao), "auroc_disg": _r(ad), "delta_disg": _r(ao - ad), "ci": [_r(x) for x in ci(bo_ - bd_)],
                      "n": int(msk.sum()), "n_pos": int(y[msk].sum())}
        did = bo["GOLDSYS"] - bo["E_POOL"]
        se = float(np.nanstd(did))
        r["DiD"] = {"point": _r(r["GOLDSYS"]["delta_disg"] - r["E_POOL"]["delta_disg"]), "ci": [_r(x) for x in ci(did)],
                    "boot_se": _r(se), "MDE_2.8SE": _r(2.8 * se)}
        # gold-recognition probe (ERROR rows only; 'says faithful' = oriented score < 0.5)
        W = cb.W[:, cb.cid].astype(float)
        err = y == 1
        fo = (so < 0.5).astype(float)
        fd = (sd < 0.5).astype(float)
        probe = {}
        pb = {}
        for arm, msk in (("E_POOL", inE), ("GOLDSYS", ~inE)):
            m2 = msk & err & ~np.isnan(so) & ~np.isnan(sd)
            if m2.sum() == 0:
                continue
            d_pt = float(fo[m2].mean() - fd[m2].mean())
            wm = W[:, m2]
            with np.errstate(invalid="ignore", divide="ignore"):
                d_b = (wm @ fo[m2] - wm @ fd[m2]) / wm.sum(1)
            pb[arm] = d_b
            probe[arm] = {"p_faithful_orig": _r(float(fo[m2].mean())), "p_faithful_disg": _r(float(fd[m2].mean())), "delta": _r(d_pt),
                          "ci": [_r(x) for x in ci(d_b)], "n_error_rows": int(m2.sum())}
        if len(pb) == 2:
            dd = pb["GOLDSYS"] - pb["E_POOL"]
            se2 = float(np.nanstd(dd))
            probe["DiD"] = {"point": _r(probe["GOLDSYS"]["delta"] - probe["E_POOL"]["delta"]), "ci": [_r(x) for x in ci(dd)],
                            "MDE_2.8SE": _r(2.8 * se2)}
        r["gold_recognition_probe"] = probe
        out[name] = r
    return out


# ------------------------------------------------------------------ (e) recall per error type at matched FA
# tier-A repair ops transform the CANDIDATE into the reference: repair ADD = the candidate is MISSING content (error code DROP),
# repair DROP = the candidate has EXTRA content (error code ADD); all other operators name the same error.
REPAIR2ERR = {"ADD": "DROP", "DROP": "ADD"}


def error_type_of(r):
    """Error type (census error codes) of an E ERROR row: tier A -> the single repair op mapped to its error code
    ('A:NEG', 'A:DROP' = missing content, ...), 'A:TWO_OP'; tier B -> COMPOUND / COMPOUND_ADD_DROP / MEANING_RENAME / OTHER
    from the panel's error_ops."""
    tier = r["metadata_label_tier"]
    if tier == "A":
        ops = r.get("metadata_repair_ops") or r.get("metadata_error_ops") or []
        ops = [o for o in ops if o]
        if len(ops) == 1:
            return "A:" + REPAIR2ERR.get(ops[0], ops[0])
        if len(ops) == 2:
            return "A:TWO_OP"
        return "A:OTHER"
    ops = set(r.get("metadata_error_ops") or [])
    if "MEANING_RENAME" in ops:
        return "B:MEANING_RENAME"
    if "COMPOUND" in ops:
        if ops <= {"COMPOUND", "ADD", "DROP"} and ops & {"ADD", "DROP"}:
            return "B:COMPOUND_ADD_DROP"
        return "B:COMPOUND"
    return "B:OTHER"


def dropped_condition(r) -> bool:
    """Candidate is missing content: tier-A repair ops contain ADD, or the tier-B panel error_ops contain DROP."""
    if r["metadata_label_tier"] == "A":
        return "ADD" in (r.get("metadata_repair_ops") or [])
    return "DROP" in (r.get("metadata_error_ops") or [])


def recall_by_type(keys, y, types, T, judges, cb, fas=(0.10, 0.20)):
    out = {}
    W = cb.W[:, cb.cid].astype(float)
    for m in judges:
        if m not in T:
            continue
        s, _, _ = arr(T, m, keys)
        if np.isnan(s).all():
            continue
        neg = s[(y == 0) & ~np.isnan(s)]
        r = {}
        for fa in fas:
            t = float(np.quantile(neg, 1 - fa))
            flag = (s > t).astype(float)
            per = {}
            for ty in sorted(set(types[i] for i in range(len(keys)) if y[i] == 1)):
                msk = np.array([y[i] == 1 and types[i] == ty for i in range(len(keys))]) & ~np.isnan(s)
                if msk.sum() < 5:
                    continue
                wm = W[:, msk]
                with np.errstate(invalid="ignore", divide="ignore"):
                    rb = (wm @ flag[msk]) / wm.sum(1)
                per[ty] = {"n": int(msk.sum()), "recall": _r(float(flag[msk].mean())), "ci": [_r(x) for x in ci(rb)]}
            r[f"FA={fa}"] = {"threshold": _r(t), "realised_fa": _r(float(flag[(y == 0) & ~np.isnan(s)].mean())), "per_type": per}
        out[m] = r
    return out


def error_type_accuracy(keys, types, judge_types: dict, y):
    """Judge error_type field vs single-op tier-A repair op; chance = majority-class share."""
    out = {}
    gold = {k: t[2:] for k, t, yy in zip(keys, types, y) if yy == 1 and t.startswith("A:") and t not in ("A:TWO_OP", "A:OTHER")}
    if not gold:
        return {"note": "no single-op tier-A errors"}
    maj = Counter(gold.values()).most_common(1)[0]
    out["n_single_op"] = len(gold)
    out["majority_class"] = maj[0]
    out["chance_majority"] = _r(maj[1] / len(gold))
    out["gold_dist"] = dict(Counter(gold.values()))
    for m, jt in judge_types.items():
        hits = [jt.get(k) == g for k, g in gold.items() if jt.get(k) is not None]
        named = [(jt.get(k), g) for k, g in gold.items() if jt.get(k) not in (None, "NONE")]
        out[m] = {"n": len(hits), "accuracy": _r(sum(hits) / len(hits)) if hits else None,
                  "n_code_named": len(named), "accuracy_when_code_named": _r(sum(a == g for a, g in named) / len(named)) if named else None,
                  "named_code_dist": dict(Counter(a for a, _ in named))}
    return out


# ------------------------------------------------------------------ (f) complexity
def bin_of(kind, st):
    if kind == "words":
        w = st.get("words") or 0
        return "<12" if w < 12 else "12-19" if w < 20 else "20-24" if w < 25 else "25-29" if w < 30 else "30-34" if w < 35 else ">=35"
    if kind == "n_quant":
        q = st.get("n_quant") or 0
        return str(q) if q < 3 else "3+"
    if kind == "depth":
        d = st.get("depth") or 0
        return "<=3" if d <= 3 else "4-5" if d <= 5 else "6-7" if d <= 7 else "8+"
    if kind == "n_conditions":
        c = st.get("n_conditions") or 0
        return "<=1" if c <= 1 else str(c) if c < 4 else "4+"
    if kind == "exception_type":
        return st.get("exception_type") or "none"
    raise ValueError(kind)


def complexity(keys, y, strata, T, metrics):
    out = {}
    for kind in ("words", "n_quant", "depth", "n_conditions", "exception_type"):
        bins = [bin_of(kind, strata[k]) for k in keys]
        tab = {}
        for b in sorted(set(bins)):
            msk = np.array([x == b for x in bins])
            yy = y[msk]
            cell = {"n_pos": int(yy.sum()), "n_neg": int(len(yy) - yy.sum())}
            cell["descriptive_only"] = not (cell["n_pos"] >= 50 and cell["n_neg"] >= 50)
            for m in metrics:
                if m not in T:
                    continue
                s, _, _ = arr(T, m, [k for k, mm in zip(keys, msk) if mm])
                cell[m] = _r(auc_w(yy, s)) if len(np.unique(yy)) == 2 else None
            tab[b] = cell
        out[kind] = tab
    return out


def gee_slopes(keys, y, strata, clusters, T, thr, metrics):
    import pandas as pd
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    out = {}
    base = pd.DataFrame({"y": y, "sid": [clusters[k] for k in keys], "words": [strata[k].get("words") or 0 for k in keys],
                         "ncond": [strata[k].get("n_conditions") or 0 for k in keys],
                         "stratum": [strata[k].get("source_stratum") for k in keys]})
    base["zw"] = (base.words - base.words.mean()) / base.words.std()
    base["zc"] = (base.ncond - base.ncond.mean()) / base.ncond.std()
    for m in metrics:
        if m not in T:
            continue
        s, _, _ = arr(T, m, keys)
        if np.isnan(s).any():
            continue
        t = thr.get(m, 0.5)
        df = base.copy()
        df["correct"] = ((s > t).astype(int) == y).astype(int)
        r = {"threshold": _r(t), "accuracy": _r(float(df.correct.mean()))}
        for term, f in (("words", "correct ~ zw + C(stratum)"), ("n_conditions", "correct ~ zc + C(stratum)")):
            try:
                g = smf.gee(f, "sid", df, family=sm.families.Binomial(), cov_struct=sm.cov_struct.Exchangeable()).fit()
                v = "zw" if term == "words" else "zc"
                r[term] = {"slope_per_sd": _r(g.params[v]), "se": _r(g.bse[v]), "p": _r(g.pvalues[v], 6),
                           "ci": [_r(g.conf_int().loc[v, 0]), _r(g.conf_int().loc[v, 1])]}
            except Exception as e:  # noqa: BLE001 - GEE non-convergence is reported, not hidden
                r[term] = {"error": str(e)[:120]}
        out[m] = r
    return out


# ------------------------------------------------------------------ (h) label-quality rates
def wilson(k, n, z=1.96):
    if n == 0:
        return [None, None]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [_r(c - h), _r(c + h)]


def label_quality(full_rows, sentences):
    out = {"gold_error": {}, "correct_not_equivalent": {}, "per_sysvar": {}}
    for st in STRATA + ["MALLS_all"]:
        ss = [s for s in sentences if (s["metadata_strata"]["source_stratum"] == st or (st == "MALLS_all" and s["metadata_strata"]["source_stratum"] != "CTRL"))]
        aud = [s for s in ss if s.get("metadata_gold_audit_flag") in ("FAITHFUL", "UNFAITHFUL")]
        k = sum(1 for s in aud if s["metadata_gold_audit_flag"] == "UNFAITHFUL")
        out["gold_error"][st] = {"sentences": len(ss), "audited": len(aud), "judged_wrong": k,
                                 "rate": _r(k / len(aud)) if aud else None, "wilson": wilson(k, len(aud))}

    def cne(rows):
        dec = [r for r in rows if r["metadata_label_tier"] in ("A", "B") and r["metadata_final_label"] in ("CORRECT", "ERROR")
               and r.get("metadata_equiv_status") != "EQ"]
        cor = [r for r in rows if r["metadata_label_tier"] in ("A", "B") and r["metadata_final_label"] == "CORRECT"]
        k1 = sum(1 for r in dec if r["metadata_final_label"] == "CORRECT")
        k2 = sum(1 for r in cor if r.get("metadata_correct_not_equivalent"))
        return {"non_eq_decided": len(dec), "final_correct_among_non_eq": _r(k1 / len(dec)) if dec else None, "wilson1": wilson(k1, len(dec)),
                "n_correct": len(cor), "share_correct_not_eq": _r(k2 / len(cor)) if cor else None, "wilson2": wilson(k2, len(cor))}
    llm = [r for r in full_rows if r["metadata_system_class"] == "llm"]
    for st in STRATA:
        out["correct_not_equivalent"][st] = cne([r for r in llm if r["metadata_strata"]["source_stratum"] == st])
    by = defaultdict(list)
    for r in llm:
        by[f"{r['metadata_system']}|{r['metadata_prompt_variant']}"].append(r)
    for k, rows in sorted(by.items()):
        out["per_sysvar"][k] = cne(rows)
    return out


# ------------------------------------------------------------------ (i) system level
def system_level(keys, y, sysv, clusters, T, metrics, B=2000, seed=0):
    rng = np.random.default_rng(seed)
    systems = sorted(set(sysv))
    sents = sorted(set(clusters[k] for k in keys))
    sidx = {s: i for i, s in enumerate(sents)}
    cid = np.array([sidx[clusters[k]] for k in keys])
    sy = np.array([systems.index(s) for s in sysv])
    fam = [s.split("|")[0] for s in systems]
    famu = sorted(set(fam))
    draws = rng.integers(0, len(sents), size=(B, len(sents)))
    Wb = np.zeros((B, len(sents)))
    for b in range(B):
        np.add.at(Wb[b], draws[b], 1)
    out = {"n_systems": len(systems), "systems": systems, "note": "descriptive only (13 rows; CI ~ ±0.4)"}

    def per_sys(vals, w):
        num = np.bincount(sy, weights=vals * w, minlength=len(systems))
        den = np.bincount(sy, weights=w, minlength=len(systems))
        with np.errstate(invalid="ignore", divide="ignore"):
            return num / den, den

    def fam_avg(v):
        return np.array([np.nanmean([v[i] for i, f in enumerate(fam) if f == fu]) for fu in famu])
    er_pt, _ = per_sys(y.astype(float), np.ones(len(y)))
    out["error_rate"] = dict(zip(systems, map(_r, er_pt)))
    for m in metrics:
        if m not in T:
            continue
        s, _, _ = arr(T, m, keys)
        if np.isnan(s).any():
            continue
        ms_pt, _ = per_sys(s, np.ones(len(s)))
        tau = stats.kendalltau(ms_pt, er_pt).statistic
        tauf = stats.kendalltau(fam_avg(ms_pt), fam_avg(er_pt)).statistic
        tb, tbf = [], []
        for b in range(B):
            w = Wb[b][cid]
            a1, _ = per_sys(s, w)
            a2, _ = per_sys(y.astype(float), w)
            ok = ~np.isnan(a1) & ~np.isnan(a2)
            tb.append(stats.kendalltau(a1[ok], a2[ok]).statistic)
            tbf.append(stats.kendalltau(fam_avg(a1), fam_avg(a2)).statistic)
        out[m] = {"tau_b_13": _r(tau), "ci": [_r(x) for x in ci(np.array(tb, dtype=float))],
                  "tau_b_11fam": _r(tauf), "ci_11fam": [_r(x) for x in ci(np.array(tbf, dtype=float))],
                  "mean_score": dict(zip(systems, map(_r, ms_pt)))}
    return out
