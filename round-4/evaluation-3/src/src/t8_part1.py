#!/usr/bin/env python3
"""PART 1: gates G0-G2, per-peer-pair vocabulary classes, counting rules, the pre-registered CSC d prediction (3-pool
PRIMARY, 9-family secondary), cuts, GEE slopes, specificity placebo, c_vres. Writes results/part1.json,
results/part1_rows.pkl, results/part1_pairs.pkl and tables/p1_*.csv. Reads prereg_d_split.json (must exist)."""
from __future__ import annotations

import hashlib
import json
import multiprocessing as mp
import os
import sys
import time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

os.environ["PYTHONHASHSEED"] = "0"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from loguru import logger  # noqa: E402

from t8_paths import E8, EV2, RESD, ROOT, jdump, jl, write_csv  # noqa: E402
import consensus_mx as CS  # noqa: E402
import mechanism as MC  # noqa: E402
from frame import build_frame  # noqa: E402
from stats import SentBoot, WAuc, WStratAuc, auc, ci, strat_auc  # noqa: E402
import t8_classes as TC  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "part1.log", rotation="30 MB", level="DEBUG")

POOL3 = ("deepseek", "microsoft", "openai")
N_MC = 500
B = 2000
TARGET = {"e": 0.124, "d": 0.537, "auroc_c_exact": 0.748, "auroc_c_align": 0.784}
RULES_DET = ["R_exact", "R_align", "R_name", "R_liberal", "R_oracle", "R_oracle_labdenom"]
RULES_MC = ["R_point_MC", "R_point_label"]
RULES = RULES_DET + RULES_MC


def op_class(ops) -> str:
    from common import op_class as oc
    return oc(list(ops) if ops is not None and not isinstance(ops, float) else [])


# ============================================================================================ data
def load() -> tuple[pd.DataFrame, dict, dict]:
    df, info = build_frame()
    mats = {r["sentence_id"]: r for r in jl(EV2 / "pairwise_classes_E.jsonl")}
    sms = {s: CS.SentenceMatrix(r) for s, r in mats.items()}
    return df, sms, info


def gate_g0(P: pd.DataFrame) -> dict:
    y = P.y_AB.values.astype(int)
    ed = MC.ed_decomposition(y, P.end_maj_mx.values.astype(int))
    g = {"n_scorable": len(P), "n_err": ed["n_err"], "n_cor": ed["n_cor"], "n_sent": int(P.sentence_id.nunique()),
         "e_END_MAJ_matrix": ed["e"], "d_END_MAJ_matrix": ed["d"],
         "e_END_MAJ_frozen": float(P.end_maj_frozen[y == 1].mean()), "d_END_MAJ_frozen": float(1 - P.end_maj_frozen[y == 0].mean()),
         "auroc_c_exact": auc(y, P.c_exact.values), "auroc_c_align_frozen": auc(y, P.c_frozen.values),
         "auroc_c_align_matrix": auc(y, P.c_re.values), "targets": TARGET, "tolerance": 0.002}
    g["pass"] = (abs(g["e_END_MAJ_matrix"] - TARGET["e"]) <= 0.002 and abs(g["d_END_MAJ_matrix"] - TARGET["d"]) <= 0.002
                 and abs(g["auroc_c_exact"] - TARGET["auroc_c_exact"]) <= 0.002
                 and abs(g["auroc_c_align_frozen"] - TARGET["auroc_c_align"]) <= 0.002)
    g["n_rows_end_maj_matrix_ne_frozen"] = int((P.end_maj_mx != P.end_maj_frozen).sum())
    return g


def build_pairs(df: pd.DataFrame, sms: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    """P = consensus-scorable R_AB rows; Q = one record per (candidate, family-disjoint peer)."""
    lab = df.set_index("row_key")
    yab = lab.y_AB.to_dict()
    opc = {rk: op_class(o) for rk, o in lab.error_ops.items()}
    rc = []
    pr = []
    for r in df[df.y_AB.notna() & df.parseable].itertuples():
        sm_ = sms.get(r.sentence_id)
        if sm_ is None or r.row_key not in sm_.row_node:
            continue
        x = CS.row_consensus(sm_, r.row_key)
        if x["npc"] < 2:
            continue
        rc.append({"row_key": r.row_key, "npc": x["npc"], "n_eq_mx": x["n_eq"], "c_re": x["c_re"], "c_exact": x["c_exact"],
                   "end_maj_mx": int(x["end_maj"])})
        ci_ = sm_.row_node[r.row_key]
        fam = sm_.row_meta[r.row_key]["family"]
        for rk, m in sm_.row_meta.items():
            if not m["is_peer"] or m["family"] == fam or rk == r.row_key:
                continue
            pj = sm_.row_node[rk]
            pr.append({"sentence_id": r.sentence_id, "cand": r.row_key, "peer": rk, "cn": ci_, "pn": pj,
                       "peer_family": m["family"], "f_exact": sm_.is_exact(ci_, pj), "f_align": sm_.is_eq(ci_, pj),
                       "mx_reason": "same_node" if ci_ == pj else sm_.reason.get((ci_, pj)),
                       "mx_eq": True if ci_ == pj else sm_.eq.get((ci_, pj)),
                       "c_fol": sm_.nodes[ci_]["canon_fol"], "p_fol": sm_.nodes[pj]["canon_fol"],
                       "peer_y": yab.get(rk), "peer_opc": opc.get(rk), "cand_opc": opc.get(r.row_key)})
    P = df.merge(pd.DataFrame(rc), on="row_key", how="inner").reset_index(drop=True)
    Q = pd.DataFrame(pr)
    return P, Q


def add_name_only(Q: pd.DataFrame, workers: int = 4) -> dict:
    need = Q[~Q.f_exact][["c_fol", "p_fol"]].drop_duplicates()
    uniq = sorted({(min(a, b), max(a, b)) for a, b in zip(need.c_fol, need.p_fol)})
    pre = {u: TC.name_only_prefilter(*u) for u in uniq}
    z3_todo = [u for u, v in pre.items() if v == "z3"]
    logger.info(f"NAME_ONLY: {len(uniq)} unique non-exact node pairs, {len(z3_todo)} need z3")
    res = {u: (False, v) for u, v in pre.items() if v != "z3"}
    import pairwise as PW
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn"), initializer=PW.init_worker,
                             initargs=(3.5,)) as ex:
        for a, b, r, why in ex.map(TC.work_name_only, z3_todo, chunksize=8):
            res[(a, b)] = (r, why)
    key = [(min(a, b), max(a, b)) for a, b in zip(Q.c_fol, Q.p_fol)]
    Q["f_name"] = [(not fe) and (res[k][0] is True) for k, fe in zip(key, Q.f_exact)]
    Q["name_reason"] = [("exact" if fe else res[k][1]) for k, fe in zip(key, Q.f_exact)]
    from collections import Counter
    return {"n_unique_nonexact_node_pairs": len(uniq), "n_z3_calls": len(z3_todo), "secs": round(time.time() - t0, 1),
            "prefilter_reasons": dict(Counter(pre.values())), "n_unknown": int(sum(v[0] is None for v in res.values())),
            "n_name_only_node_pairs": int(sum(v[0] is True for v in res.values()))}


def add_pairs_E(Q: pd.DataFrame) -> dict:
    pe = {}
    for r in jl(E8 / "results" / "pairs_E.jsonl"):
        pe[(r["cand"], r["peer"])] = r
    hit = [pe.get((c, p)) for c, p in zip(Q.cand, Q.peer)]
    rev = [pe.get((p, c)) for c, p in zip(Q.cand, Q.peer)]
    Q["pe_join"] = [h is not None for h in hit]
    Q["pe_rev_only"] = [h is None and r_ is not None for h, r_ in zip(hit, rev)]
    Q["align_eq8"] = [h["align_eq"] if h else None for h in hit]
    Q["f_vocab_raw"] = [bool(h and (h["nf_eq"] is True or h["hyb_eq"] is True)) for h in hit]
    return {"n_pairs_E_records": len(pe)}


def classify(Q: pd.DataFrame) -> None:
    Q["cls"] = np.select([Q.f_exact, Q.f_name, Q.f_align, Q.f_vocab_raw],
                         ["EXACT", "NAME_ONLY", "ALIGN_ONLY", "VOCAB"], "IRREDUCIBLE")
    Q["f_vocab_extra"] = Q.cls == "VOCAB"
    Q["in_pool3"] = Q.peer_family.isin(POOL3)


# ============================================================================================ rules
def endorse_det(Q: pd.DataFrame, P: pd.DataFrame, pool: str) -> tuple[dict, np.ndarray]:
    """Deterministic endorsement per rule for every P row (NaN when the pool has no rows)."""
    q = Q if pool == "9fam" else Q[Q.in_pool3]
    idx = {rk: i for i, rk in enumerate(P.row_key)}
    ci_ = q.cand.map(idx).values
    n = np.bincount(ci_, minlength=len(P)).astype(float)
    y = P.y_AB.values.astype(int)
    cand_opc = P.row_key.map(dict(zip(Q.cand, Q.cand_opc))).values
    agree = {
        "R_exact": q.f_exact.values, "R_align": q.f_align.values, "R_name": (q.f_align | q.f_name).values,
        "R_liberal": (q.f_align | q.f_name | q.f_vocab_raw).values}
    peer_y = q.peer_y.values
    cy = y[ci_]
    lab_agree = np.where(cy == 0, peer_y == 0, (peer_y == 1) & (q.peer_opc.values == cand_opc[ci_]))
    agree["R_oracle"] = lab_agree
    labelled = np.array([v in (0, 1) for v in peer_y])
    out = {}
    with np.errstate(invalid="ignore", divide="ignore"):
        for r, a in agree.items():
            k = np.bincount(ci_, weights=a.astype(float), minlength=len(P))
            out[r] = np.where(n > 0, (k > n / 2).astype(float), np.nan)
        k = np.bincount(ci_, weights=lab_agree.astype(float), minlength=len(P))
        nl = np.bincount(ci_, weights=labelled.astype(float), minlength=len(P))
        out["R_oracle_labdenom"] = np.where(nl > 0, (k > nl / 2).astype(float), np.nan)
        out["_n"] = n
        out["_agree_liberal"] = np.bincount(ci_, weights=agree["R_liberal"].astype(float), minlength=len(P))
        out["_agree_align"] = np.bincount(ci_, weights=agree["R_align"].astype(float), minlength=len(P))
    return out, ci_


def endorse_mc(Q: pd.DataFrame, P: pd.DataFrame, pool: str, p_acc: float, seed: int = 0) -> dict:
    """(N_MC, n_rows) endorsement draws for R_point_MC and R_point_label."""
    q = Q if pool == "9fam" else Q[Q.in_pool3]
    idx = {rk: i for i, rk in enumerate(P.row_key)}
    ci_ = q.cand.map(idx).values
    n = np.bincount(ci_, minlength=len(P)).astype(float)
    base = np.bincount(ci_, weights=(q.f_align | q.f_name).values.astype(float), minlength=len(P))
    vx = q.f_vocab_extra.values
    y = P.y_AB.values.astype(int)
    cy = y[ci_]
    peer_y = q.peer_y.values
    cand_opc = P.row_key.map(dict(zip(Q.cand, Q.cand_opc))).values[ci_]
    unl = np.array([v not in (0, 1) for v in peer_y])
    acc_lab = np.where(cy == 0, peer_y == 0, (peer_y == 1) & (q.peer_opc.values == cand_opc))
    p_label = np.where(unl, p_acc, acc_lab.astype(float))
    rng = np.random.default_rng(seed)
    vi = np.where(vx)[0]
    U = rng.random((N_MC, len(vi)))
    out = {}
    for name, prob in (("R_point_MC", np.full(len(vi), p_acc)), ("R_point_label", p_label[vi])):
        acc = (U < prob[None, :]).astype(float)
        K = np.zeros((N_MC, len(P)))
        np.add.at(K.T, ci_[vi], acc.T)
        with np.errstate(invalid="ignore"):
            out[name] = np.where(n[None, :] > 0, ((base[None, :] + K) > n[None, :] / 2).astype(float), np.nan)
    return out


# ============================================================================================ summaries
def ed_ci(y, en, W) -> dict:
    """e, d, AUROC_b with sentence-cluster CIs. en: (n,) binary or (N_MC, n) draws (combined band: replicate b uses
    draw b % N_MC)."""
    y = np.asarray(y, int)
    if en.ndim == 1:
        e = float(en[y == 1].mean()) if (y == 1).any() else np.nan
        d = float(1 - en[y == 0].mean()) if (y == 0).any() else np.nan
        with np.errstate(invalid="ignore", divide="ignore"):
            eb = (W @ (en * y)) / (W @ y)
            db = (W @ ((1 - en) * (1 - y))) / (W @ (1 - y))
        rec = {"e": e, "d": d}
    else:
        e = float(np.nanmean(en[:, y == 1].mean(1))) if (y == 1).any() else np.nan
        d = float(np.nanmean(1 - en[:, y == 0].mean(1))) if (y == 0).any() else np.nan
        M = en[np.arange(W.shape[0]) % en.shape[0]]
        with np.errstate(invalid="ignore", divide="ignore"):
            eb = (W * M * y).sum(1) / (W @ y)
            db = (W * (1 - M) * (1 - y)).sum(1) / (W @ (1 - y))
        rec = {"e": e, "d": d, "mc_band_e": [float(np.percentile(en[:, y == 1].mean(1), 2.5)), float(np.percentile(en[:, y == 1].mean(1), 97.5))] if (y == 1).any() else [None, None],
               "mc_band_d": [float(np.percentile(1 - en[:, y == 0].mean(1), 2.5)), float(np.percentile(1 - en[:, y == 0].mean(1), 97.5))] if (y == 0).any() else [None, None]}
    rec.update({"auroc_b": 1 - (e + d) / 2, "e_ci": ci(eb), "d_ci": ci(db), "auroc_b_ci": ci(1 - (eb + db) / 2),
                "n_err": int((y == 1).sum()), "n_cor": int((y == 0).sum())})
    return rec


def cut_labels(P: pd.DataFrame) -> dict:
    return {"ALL": np.array(["ALL"] * len(P), object), "words_tercile": P.words_t.values, "ncond_bin": P.ncond_bin.values,
            "stratum": P.stratum.values, "long_pool": np.where(P.long.values, "L25+L20+EXC", None)}


def rule_tables(P: pd.DataFrame, EN: dict, boot: SentBoot, pool: str) -> tuple[pd.DataFrame, dict]:
    """e/d per rule and cut. EN: rule -> (n,) or (N_MC, n) with NaN = not scorable in this pool."""
    Wf = boot.W()
    y_all = P.y_AB.values.astype(int)
    rows = []
    heads = {}
    for rule in RULES:
        en_all = EN[rule]
        ok = ~np.isnan(en_all if en_all.ndim == 1 else en_all[0])
        for dim, lab in cut_labels(P).items():
            for val in sorted({v for v in lab if v is not None}):
                m = ok & (lab == val)
                if m.sum() == 0:
                    continue
                y = y_all[m]
                en = en_all[m] if en_all.ndim == 1 else en_all[:, m]
                rec = ed_ci(y, en, Wf[:, m])
                ns = int(P.sentence_id.values[m].size and len(set(P.sentence_id.values[m])))
                rec.update({"pool": pool, "rule": rule, "dim": dim, "cell": val, "n_sent": ns,
                            "testable_d": bool(rec["n_cor"] >= MC.MIN_ROWS and ns >= MC.MIN_SENT),
                            "testable_e": bool(rec["n_err"] >= MC.MIN_ROWS and ns >= MC.MIN_SENT)})
                if en.ndim == 1:
                    ed = MC.ed_decomposition(y, en.astype(int)) if (y == 1).any() and (y == 0).any() else None
                    rec["identity_ok"] = ed is not None
                rows.append(rec)
                if dim == "ALL":
                    heads[rule] = rec
    T = pd.DataFrame(rows)
    return T, heads


def gee_slopes(P: pd.DataFrame, EN: dict, boot: SentBoot, pool: str) -> dict:
    from sklearn.linear_model import LogisticRegression
    out = {}
    cor = (P.y_AB.values == 0)
    for rule in ("R_exact", "R_align", "R_name", "R_liberal", "R_oracle", "R_point_label"):
        en = EN[rule] if EN[rule].ndim == 1 else EN[rule][0]
        m = cor & ~np.isnan(en)
        d = P[m].copy()
        d["not_endorsed"] = (1 - en[m]).astype(int)
        d = MC.zcols(d)
        g = MC.gee_fit(d, "not_endorsed ~ zw + C(stratum)")
        out[rule] = {"b_zw": (g["coef"] or {}).get("zw"), "n": g["n"], "n_clusters": g["n_clusters"],
                     "cov_struct": g.get("cov_struct"), "rate": float(d.not_endorsed.mean())}
    # slope difference R_align - R_point_label (draw 0) with a sentence-cluster bootstrap of plain logistic fits
    en_a = EN["R_align"]
    en_p = EN["R_point_label"]
    m = cor & ~np.isnan(en_a)
    d = MC.zcols(P[m].copy())
    X = np.column_stack([d.zw.values, pd.get_dummies(d.stratum, drop_first=True).values.astype(float)])
    ya = (1 - en_a[m]).astype(int)
    W = boot.W(m)

    def sl(yv, w):
        return LogisticRegression(C=1e6, max_iter=500).fit(X, yv, sample_weight=w).coef_[0][0]
    pt = sl(ya, np.ones(m.sum())) - sl((1 - en_p[0][m]).astype(int), np.ones(m.sum()))
    diffs = []
    for b in range(W.shape[0]):
        yp = (1 - en_p[b % N_MC][m]).astype(int)
        try:
            diffs.append(sl(ya, W[b] + 1e-12) - sl(yp, W[b] + 1e-12))
        except ValueError:
            continue
    out["slope_diff_R_align_minus_R_point_label"] = {"point": float(pt), "ci": ci(diffs), "n_boot": len(diffs),
                                                     "method": "plain logistic not_endorsed ~ zw + stratum dummies, CORRECT rows; replicate b uses MC draw b%500"}
    return out


def placebo(P: pd.DataFrame, Q: pd.DataFrame, EN: dict, pool: str, boot: SentBoot, n_draw: int = 200) -> dict:
    """Random IRREDUCIBLE pairs (same count per sentence as VOCAB pairs) counted as agreements on top of R_name."""
    q = Q if pool == "9fam" else Q[Q.in_pool3]
    idx = {rk: i for i, rk in enumerate(P.row_key)}
    ci_ = q.cand.map(idx).values
    n = np.bincount(ci_, minlength=len(P)).astype(float)
    base = np.bincount(ci_, weights=(q.f_align | q.f_name).values.astype(float), minlength=len(P))
    y = P.y_AB.values.astype(int)
    en_name = EN["R_name"]
    en_lib = EN["R_liberal"]
    ok = ~np.isnan(en_name)
    sid = q.sentence_id.values
    irr = np.where((q.cls == "IRREDUCIBLE").values)[0]
    by_irr = defaultdict(list)
    for i in irr:
        by_irr[sid[i]].append(i)
    kv = defaultdict(int)
    for s in sid[q.f_vocab_extra.values]:
        kv[s] += 1
    rng = np.random.default_rng(0)
    draws = []
    n_capped = 0
    for _ in range(n_draw):
        extra = np.zeros(len(P))
        for s, k in kv.items():
            pool_i = by_irr.get(s, [])
            if len(pool_i) < k:
                n_capped += 1
            pick = rng.choice(pool_i, size=min(k, len(pool_i)), replace=False) if pool_i else []
            np.add.at(extra, ci_[pick], 1.0)
        with np.errstate(invalid="ignore"):
            draws.append(np.where(n > 0, ((base + extra) > n / 2).astype(float), np.nan))
    R = np.array(draws)
    W = boot.W()[:, ok]
    yk = y[ok]

    def dd(en):  # d, e for binary vector or rows
        return (1 - en[..., yk == 0]).mean(-1), en[..., yk == 1].mean(-1)
    d_n, e_n = dd(en_name[ok])
    d_l, e_l = dd(en_lib[ok])
    d_r, e_r = dd(R[:, ok])
    dV, eV = d_n - d_l, e_l - e_n
    dR, eR = d_n - d_r, e_r - e_n
    with np.errstate(invalid="ignore", divide="ignore"):
        ratio = (dV / eV) / (np.mean(dR) / np.mean(eR))
    # bootstrap: replicate b uses placebo draw b % n_draw
    rb = []
    Rk = R[:, ok]
    for b in range(W.shape[0]):
        w = W[b]
        w0, w1 = w * (yk == 0), w * (yk == 1)
        if w0.sum() == 0 or w1.sum() == 0:
            continue

        def de(en):
            return (w0 @ (1 - en)) / w0.sum(), (w1 @ en) / w1.sum()
        dn, en_ = de(en_name[ok])
        dl, el = de(en_lib[ok])
        dr, er = de(Rk[b % n_draw])
        with np.errstate(invalid="ignore", divide="ignore"):
            rb.append(((dn - dl) / (el - en_)) / ((dn - dr) / (er - en_)))
    rb = np.array(rb)
    return {"pool": pool, "n_vocab_pairs": int(sum(kv.values())), "n_sentences_with_vocab": len(kv),
            "n_sentence_draws_capped": n_capped, "delta_d_vocab": float(dV), "delta_e_vocab": float(eV),
            "delta_d_random_mean": float(np.mean(dR)), "delta_e_random_mean": float(np.mean(eR)),
            "delta_d_random_band": [float(np.percentile(dR, 2.5)), float(np.percentile(dR, 97.5))],
            "delta_e_random_band": [float(np.percentile(eR, 2.5)), float(np.percentile(eR, 97.5))],
            "specificity_ratio": float(ratio), "specificity_ratio_ci": ci(rb[np.isfinite(rb)]),
            "n_boot_finite": int(np.isfinite(rb).sum()),
            "reading": "ratio well above 1 = VOCAB agreements concentrated among CORRECT candidates; ~1 = indiscriminate"}


def class_shares(P: pd.DataFrame, Q: pd.DataFrame, pool: str) -> pd.DataFrame:
    q = Q if pool == "9fam" else Q[Q.in_pool3]
    ymap = dict(zip(P.row_key, P.y_AB.astype(int)))
    q = q.assign(cand_y=q.cand.map(ymap), peer_lab=q.peer_y.map({0: "CORRECT", 1: "ERROR"}).fillna("unlabelled"))
    sets = {"all_pairs": q, "CORRECT_cand_pairs": q[q.cand_y == 0], "ERROR_cand_pairs": q[q.cand_y == 1],
            "disagreeing_CORRECT_cand_pairs": q[(q.cand_y == 0) & ~q.f_align]}
    rows = []
    for nm, s in sets.items():
        for pl in ("ALL", "CORRECT", "ERROR", "unlabelled"):
            ss = s if pl == "ALL" else s[s.peer_lab == pl]
            if len(ss) == 0:
                continue
            vc = ss.cls.value_counts()
            rows.append({"pool": pool, "pair_set": nm, "peer_label": pl, "n_pairs": len(ss), "n_sent": ss.sentence_id.nunique(),
                         **{f"share_{c}": float(vc.get(c, 0) / len(ss)) for c in ("EXACT", "NAME_ONLY", "ALIGN_ONLY", "VOCAB", "IRREDUCIBLE")}})
    return pd.DataFrame(rows)


def cvres(P: pd.DataFrame, D: dict, boot: SentBoot, pool: str) -> dict:
    n = D["_n"]
    ok = n > 0
    c_v = np.where(ok, 1 - D["_agree_liberal"] / np.where(ok, n, 1), np.nan)
    c_a = np.where(ok, 1 - D["_agree_align"] / np.where(ok, n, 1), np.nan)
    P[f"c_vres_{pool}"] = c_v
    P[f"c_align_{pool}"] = c_a
    out = {}
    for cell, m0 in (("R_AB", np.ones(len(P), bool)), ("L25", P.stratum.values == "L25"), ("long", P.long.values)):
        m = m0 & ok
        y = P.y_AB.values[m].astype(int)
        st = P.stratum.values[m]
        W = boot.W(m)
        rec = {"n": int(m.sum()), "n_err": int(y.sum()), "n_cor": int((1 - y).sum())}
        for nm, s in (("c_vres", c_v[m]), ("c_align_pool", c_a[m]), ("c_score_align_frozen", P.c_frozen.values[m])):
            rec[f"auroc_{nm}"] = auc(y, s)
            rec[f"strat_auroc_{nm}"] = strat_auc(y, s, st)
        wv, wa = WAuc(y, c_v[m]), WAuc(y, P.c_frozen.values[m])
        sv, sa = WStratAuc(y, c_v[m], st), WStratAuc(y, P.c_frozen.values[m], st)
        rec["delta_auroc_vres_minus_frozen_ci"] = ci([wv(W[b]) - wa(W[b]) for b in range(W.shape[0])])
        rec["delta_strat_auroc_vres_minus_frozen_ci"] = ci([sv(W[b]) - sa(W[b]) for b in range(W.shape[0])])
        rec["delta_auroc_vres_minus_frozen"] = rec["auroc_c_vres"] - rec["auroc_c_score_align_frozen"]
        rec["delta_strat_auroc_vres_minus_frozen"] = rec["strat_auroc_c_vres"] - rec["strat_auroc_c_score_align_frozen"]
        out[cell] = rec
    return out


# ============================================================================================ main
@logger.catch(reraise=True)
def main() -> None:
    pre_p = ROOT / "prereg_d_split.json"
    h = hashlib.sha256(pre_p.read_bytes()).hexdigest()
    assert (ROOT / "prereg_d_split.sha256").read_text().split()[0] == h, "prereg hash mismatch"
    pre = json.loads(pre_p.read_text())
    p_acc = float(pre["vocab_discount"]["accept_prob"])
    A = {"prereg_sha256": h, "p_accept_vocab": p_acc}
    t0 = time.time()
    df, sms, info = load()
    cut = {"words_tercile_cuts": pre["cuts"]["words_tercile_cuts"], "exception_types_kept": json.loads(
        (EV2 / "prereg_mech.json").read_text())["cuts"]["exception_types_kept"]}
    df = MC.make_bins(df, cut)
    P, Q = build_pairs(df, sms)
    P["in_RAB"] = True
    P["end_maj_frozen"] = (P.c_frozen_raw < 0.5).astype(int)
    logger.info(f"P {len(P)} rows, Q {len(Q)} pairs ({time.time() - t0:.0f}s)")
    A["G0"] = gate_g0(P)
    logger.info(f"G0 {A['G0']}")
    if not A["G0"]["pass"]:
        jdump(RESD / "part1.json", A)
        raise SystemExit("G0 failed")
    A["pairs_E"] = add_pairs_E(Q)
    # G1 coverage
    cov = {"overall": float(Q.pe_join.mean()), "n_pairs": len(Q), "n_joined": int(Q.pe_join.sum()),
           "n_reverse_only": int(Q.pe_rev_only.sum())}
    st_map = dict(zip(P.row_key, P.stratum))
    Q["stratum"] = Q.cand.map(st_map)
    cov["by_stratum"] = {s: float(g.pe_join.mean()) for s, g in Q.groupby("stratum")}
    rowcov = Q.groupby("cand").pe_join.mean()
    cov["rows_full_coverage"] = int((rowcov == 1).sum())
    cov["pass"] = cov["overall"] >= 0.95
    A["G1"] = cov
    # G2 concordance
    j = Q[Q.pe_join]
    ct = pd.crosstab(j.f_align, j.align_eq8.astype(bool))
    A["G2"] = {"crosstab_matrix_eq_vs_exp8_align_eq": {f"mx={a}|e8={b}": int(ct.loc[a, b]) if (a in ct.index and b in ct.columns) else 0
                                                        for a in (True, False) for b in (True, False)},
               "agreement": float((j.f_align == j.align_eq8.astype(bool)).mean()), "winner": "eval-2 matrix (END_MAJ uses it)"}
    logger.info(f"G1 {cov['overall']:.4f} G2 {A['G2']}")
    A["name_only"] = add_name_only(Q)
    logger.info(f"NAME_ONLY {A['name_only']}")
    classify(Q)
    if not cov["pass"]:
        full = set(rowcov[rowcov == 1].index)
        A["G1"]["primary_restricted_to_full_coverage_rows"] = len(full)
    boot = SentBoot(P.sentence_id.values, b=B, seed=0)
    A["pools"] = {}
    ENs = {}
    tabs = []
    shares = []
    for pool in ("3pool", "9fam"):
        D, _ = endorse_det(Q, P, pool)
        EN = {r: D[r] for r in RULES_DET}
        EN.update(endorse_mc(Q, P, pool, p_acc))
        ENs[pool] = EN
        T, heads = rule_tables(P, EN, boot, pool)
        tabs.append(T)
        shares.append(class_shares(P, Q, pool))
        d0, e0 = heads["R_align"]["d"], heads["R_align"]["e"]
        pr = {"n_rows_scorable": int((D["_n"] > 0).sum()), "n_rows_excluded_no_pool_rows": int((D["_n"] == 0).sum()),
              "heads": heads,
              "d_floor_pred": heads["R_point_label"]["d"], "d_floor_pred_ci": heads["R_point_label"]["d_ci"],
              "d_bracket": [heads["R_liberal"]["d"], heads["R_name"]["d"]],
              "d_R_exact": heads["R_exact"]["d"], "d_R_oracle": heads["R_oracle"]["d"], "d_R_oracle_labdenom": heads["R_oracle_labdenom"]["d"],
              "d_R_point_MC": heads["R_point_MC"]["d"],
              "e_ceiling_pred": heads["R_point_label"]["e"], "e_ceiling_pred_ci": heads["R_point_label"]["e_ci"],
              "e_bracket": [heads["R_name"]["e"], heads["R_liberal"]["e"]],
              "d_END_MAJ_this_pool": d0, "e_END_MAJ_this_pool": e0,
              "Delta_d_vs_0537": {r: 0.537 - heads[r]["d"] for r in RULES}, "Delta_e_vs_0124": {r: heads[r]["e"] - 0.124 for r in RULES},
              "Delta_d_vs_pool_END_MAJ": {r: d0 - heads[r]["d"] for r in RULES}, "Delta_e_vs_pool_END_MAJ": {r: heads[r]["e"] - e0 for r in RULES}}
        dfl = pr["d_floor_pred"]
        pr["decision_rule"] = {"d_matched": d0, "d_floor_pred_matched": dfl,
                               "d_CSC_for_gap_0.67": d0 - 0.67 * (d0 - dfl), "d_CSC_for_gap_0.33": d0 - 0.33 * (d0 - dfl),
                               "anchoring_floor_d_R_oracle": heads["R_oracle"]["d"],
                               "verbatim": pre["decision_rule_verbatim"]}
        logger.info(f"[{pool}] d: align {d0:.3f} exact {pr['d_R_exact']:.3f} name {heads['R_name']['d']:.3f} "
                    f"point_label {dfl:.3f} liberal {heads['R_liberal']['d']:.3f} oracle {pr['d_R_oracle']:.3f}; "
                    f"e: align {e0:.3f} point_label {pr['e_ceiling_pred']:.3f} liberal {heads['R_liberal']['e']:.3f}")
        pr["gee"] = gee_slopes(P, EN, boot, pool)
        pr["placebo"] = placebo(P, Q, EN, pool, boot)
        logger.info(f"[{pool}] placebo {pr['placebo']['specificity_ratio']:.3f} {pr['placebo']['specificity_ratio_ci']}")
        pr["c_vres"] = cvres(P, D, boot, pool)
        A["pools"][pool] = pr
        for r in RULES:
            en = EN[r]
            P[f"en_{pool}_{r}"] = en if en.ndim == 1 else en.mean(0)
        P[f"en_{pool}_R_point_label_draw0"] = EN["R_point_label"][0]
    T = pd.concat(tabs, ignore_index=True)
    for c in ("e_ci", "d_ci", "auroc_b_ci"):
        T[c + "_lo"] = T[c].apply(lambda v: v[0])
        T[c + "_hi"] = T[c].apply(lambda v: v[1])
    T = T.drop(columns=["e_ci", "d_ci", "auroc_b_ci"])
    srcs = [f"{EV2}/pairwise_classes_E.jsonl :: nodes/pairs (eval-2 eqmv matrix)", f"{E8}/results/pairs_E.jsonl :: nf_eq, hyb_eq",
            f"{ROOT}/prereg_d_split.json :: rules, cuts, discount"]
    write_csv(T, "p1_rule_cuts.csv", srcs)
    write_csv(pd.concat(shares, ignore_index=True), "p1_class_shares.csv", srcs)
    # per-row class counts
    cnt = Q.pivot_table(index="cand", columns="cls", values="peer", aggfunc="count", fill_value=0)
    cnt3 = Q[Q.in_pool3].pivot_table(index="cand", columns="cls", values="peer", aggfunc="count", fill_value=0).add_suffix("_3pool")
    P = P.merge(cnt, left_on="row_key", right_index=True, how="left").merge(cnt3, left_on="row_key", right_index=True, how="left")
    keep = [c for c in P.columns if c not in ("text", "reference_fol", "e6_output")]
    P[keep].to_pickle(RESD / "part1_rows.pkl")
    Q.drop(columns=["c_fol", "p_fol"]).to_pickle(RESD / "part1_pairs.pkl")
    A["n_pairs_by_class"] = {k: int(v) for k, v in Q.cls.value_counts().items()}
    A["n_pairs_by_class_3pool"] = {k: int(v) for k, v in Q[Q.in_pool3].cls.value_counts().items()}
    A["wall_s"] = round(time.time() - t0, 1)
    jdump(RESD / "part1.json", A)
    logger.info(f"PART 1 done in {A['wall_s']}s")


if __name__ == "__main__":
    main()
