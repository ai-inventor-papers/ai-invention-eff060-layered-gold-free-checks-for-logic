#!/usr/bin/env python3
"""STEP 7 + 8: meta-evaluation of candidate C (cross-system z3 consensus) against the sampling
self-consistency baselines and cheap structural baselines on the frozen screen; writes
results/summary.json and method_out.json (exp_gen_sol_out schema).

usage: analysis.py [--mini N] [--boot 2000]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger
from scipy.stats import rankdata, spearmanr
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import GroupKFold

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from common import COARSE, LLM_SYSTEMS, op_class, safe_parse  # noqa: E402
from repair_census import symbols  # noqa: E402

RES = ROOT / "results"
logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "analysis.log", rotation="30 MB", level="DEBUG")

SCORES = {  # name -> description (higher = more likely an error)
    "c_score": "1 - eq_frac over the full leave-one-system-out LLM pool (candidate C, PRIMARY)",
    "medoid_depth": "typed-repair distance to the pool medoid, 0-3 (candidate C)",
    "cluster_entropy": "semantic entropy of z3-eqmv classes of pool ∪ {c} (candidate C variant)",
    "c_score_peers6": "1 - eq_frac over the six fresh peers only",
    "c_score_nonoai": "1 - eq_frac over the five non-OpenAI peers",
    "c_score_llm2": "1 - eq_frac over the other Logic-LM systems only",
    "sc5_cheap": "1 - share of K=5 gpt-4.1-nano T=0.7 samples eqmv to c (single-other-model agreement baseline)",
    "sc5_entropy_cheap": "semantic entropy of c + the 5 gpt-4.1-nano samples",
    "sc5_same": "1 - share of K=5 gpt-3.5-turbo T=0.7 samples eqmv to c (true same-model SC; gpt-3.5 candidates)",
    "predset_instab_sc": "1 - mean Jaccard of predicate names, c vs SC samples (user's rerun predicate-set similarity baseline)",
    "predset_instab_pool": "1 - mean Jaccard of predicate names, c vs pool members (string-level consensus baseline)",
    "fol_length": "number of atoms in the candidate (trivial complexity baseline)",
    "misalign": "1 - alignable_frac (candidate predicates alignable to the REFERENCE; uses gold, confound probe only)",
}


# ------------------------------------------------------------------ statistics
def auc_fast(y: np.ndarray, s: np.ndarray) -> float:
    n1 = int(y.sum()); n0 = len(y) - n1
    if n1 == 0 or n0 == 0:
        return float("nan")
    r = rankdata(s)
    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)


def cluster_boot_idx(groups: np.ndarray, B: int, seed: int = 0) -> list[np.ndarray]:
    rng = np.random.default_rng(seed)
    uniq, inv = np.unique(groups, return_inverse=True)
    members = [np.where(inv == g)[0] for g in range(len(uniq))]
    out = []
    for _ in range(B):
        pick = rng.integers(0, len(uniq), len(uniq))
        out.append(np.concatenate([members[g] for g in pick]))
    return out


def ci(vals) -> list:
    v = np.array([x for x in vals if not np.isnan(x)])
    return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))] if len(v) else [None, None]


def wilson(k: int, n: int, z: float = 1.96) -> list:
    if n == 0:
        return [None, None]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - h, 4), round(c + h, 4)]


def tie_acc(y: np.ndarray, s: np.ndarray, eps: float) -> float:
    """Deutsch, Foster & Freitag (2023) acc_eq over all item pairs, metric ties within eps."""
    g = np.sign(y[:, None] - y[None, :])
    m = s[:, None] - s[None, :]
    tie = np.abs(m) <= eps
    ok = np.where(g == 0, tie, (~tie) & (np.sign(m) == g))
    iu = np.triu_indices(len(y), 1)
    return float(ok[iu].mean())


def tie_calibrated(y, s) -> dict:
    diffs = np.unique(np.abs(s[:, None] - s[None, :]))
    cands = np.unique(np.concatenate([[0.0], diffs[: min(len(diffs), 60)] + 1e-9]))
    best = max(((tie_acc(y, s, e), e) for e in cands), key=lambda t: t[0])
    return {"acc_eq_eps0": round(tie_acc(y, s, 1e-12), 4), "acc_eq_best": round(best[0], 4), "eps_best": float(best[1])}


def evaluate(df: pd.DataFrame, score: str, B: int, boots=None, thr_flag: str | None = None) -> dict:
    d = df[df[score].notna()]
    y = d["y"].to_numpy().astype(int)
    s = d[score].to_numpy().astype(float)
    n1, n0 = int(y.sum()), int(len(y) - y.sum())
    out = {"n": len(d), "n_err": n1, "n_cor": n0, "prevalence": round(n1 / max(1, len(d)), 4)}
    if n1 == 0 or n0 == 0:
        return out
    out["auroc"] = round(auc_fast(y, s), 4)
    out["auprc"] = round(float(average_precision_score(y, s)), 4)
    groups = d["sentence_key"].to_numpy()
    bi = cluster_boot_idx(groups, B) if boots is None else boots
    out["auroc_ci95"] = [round(x, 4) if x is not None else None for x in ci([auc_fast(y[i], s[i]) for i in bi])]
    if len(d) <= 1500:
        out.update(tie_calibrated(y, s))
    out["testable"] = n1 >= 50 and n0 >= 50
    if thr_flag:
        f = d[thr_flag].to_numpy().astype(bool)
        tp, fp = int((f & (y == 1)).sum()), int((f & (y == 0)).sum())
        tpr, fpr = tp / n1, fp / n0
        out["threshold"] = {"flag": thr_flag, "recall": round(tpr, 4), "recall_ci95": wilson(tp, n1), "false_alarm": round(fpr, 4),
                            "false_alarm_ci95": wilson(fp, n0), "precision": round(tp / max(1, tp + fp), 4)}
        for pi in (0.10, 0.25):
            out["threshold"][f"precision_at_prev_{int(pi * 100)}"] = round(tpr * pi / max(1e-12, tpr * pi + fpr * (1 - pi)), 4)
    return out


def paired_delta(df: pd.DataFrame, a: str, b: str, B: int) -> dict:
    d = df[df[a].notna() & df[b].notna()]
    y = d["y"].to_numpy().astype(int)
    if y.sum() == 0 or y.sum() == len(y):
        return {"n": len(d)}
    sa, sb = d[a].to_numpy().astype(float), d[b].to_numpy().astype(float)
    bi = cluster_boot_idx(d["sentence_key"].to_numpy(), B)
    deltas = [auc_fast(y[i], sa[i]) - auc_fast(y[i], sb[i]) for i in bi]
    dv = np.array([x for x in deltas if not np.isnan(x)])
    return {"n": len(d), "n_err": int(y.sum()), "auroc_a": round(auc_fast(y, sa), 4), "auroc_b": round(auc_fast(y, sb), 4),
            "delta": round(auc_fast(y, sa) - auc_fast(y, sb), 4), "delta_ci95": [round(x, 4) for x in ci(deltas)],
            "p_delta_le_0": round(float((dv <= 0).mean()), 4)}


def crossfit(df: pd.DataFrame, feats: list[str], base: list[str], B: int) -> dict:
    d = df.dropna(subset=list(set(feats + base))).copy()
    y = d["y"].to_numpy().astype(int)
    if y.sum() < 10 or (len(y) - y.sum()) < 10:
        return {"n": len(d)}
    g = d["sentence_key"].to_numpy()
    gkf = GroupKFold(n_splits=5)
    oof = {}
    for name, fs in (("full", feats), ("base", base)):
        p = np.zeros(len(d))
        X = d[fs].to_numpy().astype(float)
        for tr, te in gkf.split(X, y, g):
            m = LogisticRegression(max_iter=1000).fit(X[tr], y[tr])
            p[te] = m.predict_proba(X[te])[:, 1]
        oof[name] = p
    d["_full"], d["_base"] = oof["full"], oof["base"]
    r = paired_delta(d, "_full", "_base", B)
    r.update(features=feats, base=base)
    return r


def partial_spearman(y, s, z) -> float:
    ry, rs, rz = rankdata(y), rankdata(s), rankdata(z)
    def res(a, b):
        b1 = np.c_[np.ones(len(b)), b]
        coef, *_ = np.linalg.lstsq(b1, a, rcond=None)
        return a - b1 @ coef
    return float(np.corrcoef(res(ry, rz), res(rs, rz))[0, 1])


def jacc(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if (a | b) else 1.0


def pred_names(f: str | None) -> set | None:
    e = safe_parse(f) if f else None
    if e is None:
        return None
    return {p[0].lower() for p in symbols(e)[0]}


def n_atoms(f: str | None) -> float | None:
    e = safe_parse(f) if f else None
    if e is None:
        return None
    from repair_census import atoms
    return float(len(atoms(e)))


def bins(df: pd.DataFrame) -> pd.DataFrame:
    st = df["strata"]
    df = df.copy()
    df["len_bin"] = [s["len_bin"] for s in st]
    df["words"] = [s["words"] for s in st]
    df["nq_bin"] = [None if s["n_quant"] is None else ("<=1" if s["n_quant"] <= 1 else ("2" if s["n_quant"] == 2 else ">=3")) for s in st]
    df["depth_bin"] = [None if s["depth"] is None else ("<=3" if s["depth"] <= 3 else ("4-5" if s["depth"] <= 5 else ">=6")) for s in st]
    df["ncond_bin"] = [None if s["n_cond"] is None else ("0" if s["n_cond"] == 0 else ("1-2" if s["n_cond"] <= 2 else ">=3")) for s in st]
    df["exception"] = [bool(s["exception"]) for s in st]
    return df


@logger.catch(reraise=True)
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mini", type=int, default=0)
    ap.add_argument("--boot", type=int, default=2000)
    a = ap.parse_args()
    B = a.boot
    suffix = f"_mini{a.mini}" if a.mini else ""
    items = json.loads((RES / "screen_items.json").read_text())
    cons = json.loads((RES / f"consensus{suffix}.json").read_text())
    peer_lab = json.loads((RES / f"peer_outputs_labelled{suffix}.json").read_text())
    prereg = json.loads((RES / "prereg.json").read_text())
    h = (RES / "screen_label_hash.txt").read_text().strip()
    assert prereg["screen_label_hash"] == h, "label hash changed after pre-registration"
    rec = {r["item_id"]: r for r in cons["records"]}
    items = [x for x in items if x["item_id"] in rec]
    sents = cons["sentences"]
    sc_rows = [json.loads(l) for l in (RES / "sc_samples.jsonl").read_text().splitlines() if l.strip()]
    uj = json.loads((RES / "units.json").read_text())

    rows = []
    for x in items:
        r = rec[x["item_id"]]
        S = sents[x["sentence_key"]]
        row = {k: x[k] for k in ("item_id", "track", "kind", "system", "text", "candidate_fol", "reference_fol", "label",
                                 "auto_class", "repair_ops", "vocab_strict", "sentence_key", "strata")}
        row.update({k: r.get(k) for k in ("eq_frac_full", "eq_frac_peers6", "eq_frac_nonoai", "eq_frac_llm2", "medoid", "medoid_fol",
                                           "medoid_support", "medoid_depth", "medoid_ops", "cluster_entropy", "n_classes",
                                           "n_peers_parsed", "n_peers_total", "coverage_status", "c_score", "sc5_eq_frac_cheap",
                                           "sc5_eq_frac_same", "sc5_entropy_cheap", "sc5_entropy_same", "alignable_frac",
                                           "medoid_label", "medoid_ref_ops", "pool_eq", "pool_ids", "seconds_z3", "n_timeouts")})
        ok = r["coverage_status"] == "ok"
        for nm, col in (("c_score_peers6", "eq_frac_peers6"), ("c_score_nonoai", "eq_frac_nonoai"), ("c_score_llm2", "eq_frac_llm2")):
            v = r.get(col)
            row[nm] = (1 - v) if (ok and v is not None) else 1.0
        row["sc5_cheap"] = 1 - r["sc5_eq_frac_cheap"] if r.get("sc5_eq_frac_cheap") is not None else None
        row["sc5_same"] = (1 - r["sc5_eq_frac_same"]) if (r.get("sc5_eq_frac_same") is not None and x["system"] == "gpt-3.5-turbo") else None
        row["flag_medoid"] = (r["medoid_depth"] or 0) >= 1
        cp = pred_names(x["candidate_fol"])
        scs = [f for f in [None] * 0]
        u = S["unit"]
        smp = [s["fol"] for s in sc_rows if s["arm"] == "sc_cheap" and s["unit_id"] == u and s.get("sentence_norm") == x["sentence_key"]]
        if cp is not None:
            js = [jacc(cp, pred_names(f)) for f in smp if pred_names(f) is not None]
            row["predset_instab_sc"] = 1 - (sum(js) / 5 if js else 0.0)
            pm = [S["members"][m] for m in (r.get("pool_ids") or [])]
            jp = [jacc(cp, pred_names(f)) for f in pm if f]
            row["predset_instab_pool"] = 1 - (sum(jp) / len(jp)) if jp else 1.0
        else:
            row["predset_instab_sc"] = row["predset_instab_pool"] = None
        row["fol_length"] = n_atoms(x["candidate_fol"])
        row["misalign"] = (1 - r["alignable_frac"]) if r.get("alignable_frac") is not None else None
        rows.append(row)
    df = bins(pd.DataFrame(rows))
    S_ = {}

    # ------------------------------------------------------------------ contrasts
    def contrast(name):
        L = df[df["track"] == "L"]
        if name == "primary":
            d = L[L["label"].isin(["CORRECT", "ERROR"])]
        elif name == "lenient":
            d = L[L["label"].isin(["CORRECT", "ERROR", "UNCERTAIN_COMPOUND"])]
        elif name == "vocab_strict":
            d = L[(L["label"] == "ERROR") | ((L["label"] == "CORRECT") & (L["vocab_strict"] == True))]  # noqa: E712
        elif name == "trackH":
            H = df[df["track"] == "H"]
            d = H[H["label"].isin(["CORRECT", "ERROR"])]
        elif name == "vocab_clean":
            d = L[L["label"].isin(["CORRECT", "ERROR"]) & (L["alignable_frac"] == 1.0)]
        else:
            raise ValueError(name)
        d = d.copy()
        d["y"] = (d["label"] != "CORRECT").astype(int)
        return d
    CONTR = ["primary", "lenient", "vocab_strict", "trackH", "vocab_clean"]
    res = {}
    for cn in CONTR:
        d = contrast(cn)
        res[cn] = {}
        for sc in SCORES:
            res[cn][sc] = evaluate(d, sc, B, thr_flag="flag_medoid" if sc == "c_score" else None)
        logger.info(f"[{cn}] n={len(d)} err={int(d['y'].sum())}  " +
                    "  ".join(f"{sc}={res[cn][sc].get('auroc')}" for sc in ("c_score", "medoid_depth", "cluster_entropy", "sc5_cheap", "sc5_same", "misalign")))
    S_["auroc"] = res
    P = contrast("primary")
    # ------------------------------------------------------------------ paired deltas
    deltas = {}
    for cn in ("primary", "lenient", "trackH", "vocab_clean"):
        d = contrast(cn)
        deltas[cn] = {"c_score-sc5_cheap": paired_delta(d, "c_score", "sc5_cheap", B),
                      "c_score-cluster_entropy": paired_delta(d, "c_score", "cluster_entropy", B),
                      "c_score-c_score_peers6": paired_delta(d, "c_score", "c_score_peers6", B),
                      "c_score_peers6-sc5_cheap": paired_delta(d, "c_score_peers6", "sc5_cheap", B),
                      "c_score-predset_instab_pool": paired_delta(d, "c_score", "predset_instab_pool", B),
                      "c_score-misalign": paired_delta(d, "c_score", "misalign", B)}
        d35 = d[d["system"] == "gpt-3.5-turbo"]
        deltas[cn]["c_score-sc5_same(gpt-3.5 subset)"] = paired_delta(d35, "c_score", "sc5_same", B)
        deltas[cn]["sc5_cheap-sc5_same(gpt-3.5 subset)"] = paired_delta(d35, "sc5_cheap", "sc5_same", B)
    S_["paired_delta_auroc"] = deltas
    S_["crossfit_logistic"] = {"primary: [c_score, sc5_cheap] vs [sc5_cheap]": crossfit(P, ["c_score", "sc5_cheap"], ["sc5_cheap"], B),
                               "primary: [c_score, medoid_depth, cluster_entropy, sc5_cheap] vs [sc5_cheap]":
                                   crossfit(P, ["c_score", "medoid_depth", "cluster_entropy", "sc5_cheap"], ["sc5_cheap"], B),
                               "primary: [c_score, misalign] vs [misalign]": crossfit(P, ["c_score", "misalign"], ["misalign"], B),
                               "primary: [c_score, fol_length] vs [fol_length]": crossfit(P, ["c_score", "fol_length"], ["fol_length"], B)}
    # ------------------------------------------------------------------ per system
    S_["per_system"] = {s: {sc: evaluate(P[P["system"] == s], sc, B // 4) for sc in ("c_score", "medoid_depth", "sc5_cheap", "sc5_same")}
                        for s in LLM_SYSTEMS}
    # ------------------------------------------------------------------ per type sensitivity at the pre-registered threshold
    L = df[df["track"] == "L"].copy()
    L["op_class"] = [op_class(o) if lab == "ERROR" else lab for o, lab in zip(L["repair_ops"], L["label"])]
    pts = {}
    for cls, g in L[L["label"].isin(["ERROR", "UNCERTAIN_COMPOUND"])].groupby("op_class"):
        k, n = int(g["flag_medoid"].sum()), len(g)
        pts[cls] = {"n": n, "recall_at_threshold": round(k / n, 4), "ci95": wilson(k, n), "mean_c_score": round(float(g["c_score"].mean()), 4),
                    "sc5_cheap_mean": round(float(g["sc5_cheap"].mean()), 4) if g["sc5_cheap"].notna().any() else None}
    cor = L[L["label"] == "CORRECT"]
    pts["CORRECT(false-alarm)"] = {"n": len(cor), "rate": round(float(cor["flag_medoid"].mean()), 4), "ci95": wilson(int(cor["flag_medoid"].sum()), len(cor))}
    by_op = {}
    for ops, lab, fl in zip(L["repair_ops"], L["label"], L["flag_medoid"]):
        if lab != "ERROR":
            continue
        for o in set(ops):
            by_op.setdefault(o, [0, 0]); by_op[o][0] += int(fl); by_op[o][1] += 1
    pts["by_operator"] = {o: {"n": n, "recall": round(k / n, 4), "ci95": wilson(k, n)} for o, (k, n) in sorted(by_op.items())}
    H = df[df["track"] == "H"].copy()
    H["op_class"] = [op_class(o) if lab == "ERROR" else lab for o, lab in zip(H["repair_ops"], H["label"])]
    pts_h = {}
    for cls, g in H[H["label"].isin(["ERROR", "UNCERTAIN_COMPOUND", "READING_CHOICE"])].groupby("op_class"):
        k, n = int(g["flag_medoid"].sum()), len(g)
        pts_h[cls] = {"n": n, "recall_at_threshold": round(k / n, 4), "ci95": wilson(k, n)}
        corh = H[H["label"] == "CORRECT"]
    pts_h["CORRECT(false-alarm)"] = {"n": len(corh), "rate": round(float(corh["flag_medoid"].mean()), 4)}
    S_["per_type_sensitivity"] = {"trackL": pts, "trackH": pts_h}
    # ------------------------------------------------------------------ pool-size curve
    curve = {}
    Pp = P[P["coverage_status"] != "candidate_unparseable"]
    for k in (1, 2, 3, 4, 6, 8):
        aucs = []
        for seed in range(20):
            rnd = random.Random(seed)
            sc = []
            for pe in Pp["pool_eq"]:
                ids = sorted(pe or {})
                sub = rnd.sample(ids, min(k, len(ids))) if ids else []
                sc.append(1 - (sum(pe[m] is True for m in sub) / len(sub)) if sub else 1.0)
            aucs.append(auc_fast(Pp["y"].to_numpy(), np.array(sc)))
        curve[k] = {"mean_auroc": round(float(np.mean(aucs)), 4), "sd": round(float(np.std(aucs)), 4),
                    "mean_pool_used": round(float(np.mean([min(k, len(pe or {})) for pe in Pp["pool_eq"]])), 2)}
    S_["pool_size_curve"] = curve
    # pool composition (peers-only / non-OpenAI / Logic-LM-only) is in auroc[*][c_score_peers6|nonoai|llm2]
    # ------------------------------------------------------------------ shared-aligner confound
    Pa = P[P["alignable_frac"].notna()]
    conf = {"auroc_misalign_alone": res["primary"]["misalign"].get("auroc"),
            "auroc_c_score": res["primary"]["c_score"].get("auroc"),
            "vocab_clean_subset": {sc: res["vocab_clean"][sc] for sc in ("c_score", "medoid_depth", "cluster_entropy", "sc5_cheap")},
            "partial_spearman_c_score_label_given_alignable": round(partial_spearman(Pa["y"].to_numpy(), Pa["c_score"].to_numpy(), Pa["alignable_frac"].to_numpy()), 4),
            "spearman_c_score_label": round(float(spearmanr(Pa["y"], Pa["c_score"]).correlation), 4),
            "spearman_c_score_alignable": round(float(spearmanr(Pa["alignable_frac"], Pa["c_score"]).correlation), 4),
            "share_alignable_1": {"CORRECT": round(float((Pa[Pa["y"] == 0]["alignable_frac"] == 1).mean()), 4),
                                  "ERROR": round(float((Pa[Pa["y"] == 1]["alignable_frac"] == 1).mean()), 4)}}
    conf["misalign_ge_c_score"] = (conf["auroc_misalign_alone"] or 0) >= (conf["auroc_c_score"] or 0)
    S_["shared_aligner_confound"] = conf
    # ------------------------------------------------------------------ blind spots
    E = L[L["label"] == "ERROR"].copy()
    E["blind_strict"] = E["medoid_depth"] == 0
    E["medoid_correct"] = E["medoid_label"] == "CORRECT"
    E["blind_same_ops"] = [(ml == "ERROR") and sorted(mo or []) == sorted(ro or []) for ml, mo, ro in zip(E["medoid_label"], E["medoid_ref_ops"], E["repair_ops"])]
    E["majority_endorses"] = E["eq_frac_full"].fillna(0) >= 0.5

    def rates(g):
        n = len(g)
        o = {"n": n}
        for c in ("blind_strict", "blind_same_ops", "majority_endorses", "medoid_correct"):
            k = int(g[c].sum())
            o[c] = round(k / n, 4) if n else None
            o[c + "_ci95"] = wilson(k, n)
        return o
    E["op_class"] = [op_class(o) for o in E["repair_ops"]]
    bs = {"overall": rates(E), "ceiling_max_recall_at_medoid_threshold": round(1 - float(E["blind_strict"].mean()), 4) if len(E) else None,
          "per_system": {s: rates(g) for s, g in E.groupby("system")}, "per_len_bin": {s: rates(g) for s, g in E.groupby("len_bin")},
          "per_op_class": {s: rates(g) for s, g in E.groupby("op_class")}}
    Lc = L[L["label"] == "CORRECT"]
    bs["medoid_correct_on_CORRECT_items"] = round(float((Lc["medoid_label"] == "CORRECT").mean()), 4) if len(Lc) else None
    bs["medoid_correct_by_len_bin_all_trackL"] = {s: round(float((g["medoid_label"] == "CORRECT").mean()), 4) for s, g in L[L["label"].isin(["CORRECT", "ERROR"])].groupby("len_bin")}
    S_["blind_spots"] = bs
    # ------------------------------------------------------------------ operator agreement
    D = E[E["repair_ops"].map(len).between(1, 2) & E["medoid_depth"].isin([1, 2])]
    if len(D):
        ex = [sorted(m) == sorted(r) for m, r in zip(D["medoid_ops"], D["repair_ops"])]
        ov = [bool(set(m) & set(r)) for m, r in zip(D["medoid_ops"], D["repair_ops"])]
        cc = [op_class(m) == op_class(r) for m, r in zip(D["medoid_ops"], D["repair_ops"])]
        maj = Counter(op_class(r) for r in D["repair_ops"]).most_common(1)[0]
        maj_ops = Counter(tuple(sorted(r)) for r in D["repair_ops"]).most_common(1)[0]
        S_["operator_agreement"] = {"n": len(D), "exact_multiset": round(float(np.mean(ex)), 4), "exact_ci95": wilson(sum(ex), len(D)),
                                    "any_overlap": round(float(np.mean(ov)), 4), "coarse_class": round(float(np.mean(cc)), 4),
                                    "coarse_ci95": wilson(sum(cc), len(D)),
                                    "chance_majority_coarse": {"class": maj[0], "freq": round(maj[1] / len(D), 4)},
                                    "chance_majority_exact": {"ops": list(maj_ops[0]), "freq": round(maj_ops[1] / len(D), 4)}}
    else:
        S_["operator_agreement"] = {"n": 0}
    # ------------------------------------------------------------------ complexity strata
    cx = {}
    for col in ("len_bin", "nq_bin", "depth_bin", "ncond_bin", "exception"):
        cx[col] = {}
        for v, g in P.groupby(col):
            e = {sc: evaluate(g, sc, B // 4) for sc in ("c_score", "medoid_depth", "sc5_cheap")}
            gc = g[g["y"] == 0]
            cx[col][str(v)] = {"n_err": int(g["y"].sum()), "n_cor": int((g["y"] == 0).sum()),
                               "testable": bool(g["y"].sum() >= 50 and (g["y"] == 0).sum() >= 50),
                               "auroc": {sc: e[sc].get("auroc") for sc in e}, "auroc_ci95": {sc: e[sc].get("auroc_ci95") for sc in e},
                               "false_alarm_at_threshold": round(float(gc["flag_medoid"].mean()), 4) if len(gc) else None,
                               "recall_at_threshold": round(float(g[g["y"] == 1]["flag_medoid"].mean()), 4) if g["y"].sum() else None}
    inter = {}
    for sc in ("c_score", "sc5_cheap"):
        d = P.dropna(subset=[sc])
        w = (d["words"] - d["words"].mean()) / d["words"].std()
        X = np.c_[d[sc], w, d[sc] * w]
        m = LogisticRegression(max_iter=1000, C=1e6).fit(X, d["y"])
        inter[sc] = {"coef_score": round(float(m.coef_[0][0]), 4), "coef_words_z": round(float(m.coef_[0][1]), 4),
                     "coef_score_x_words": round(float(m.coef_[0][2]), 4), "note": "descriptive only"}
    cx["logistic_score_x_words"] = inter
    long_ = P[(P["words"] >= 20) | (P["ncond_bin"] == ">=3") | P["exception"]]
    cx["long_or_conditioned_or_exception_stratum"] = {"n_err": int(long_["y"].sum()), "n_cor": int((long_["y"] == 0).sum()),
                                                      "auroc": {sc: evaluate(long_, sc, B // 4).get("auroc") for sc in ("c_score", "sc5_cheap")},
                                                      "descriptive_only": True}
    S_["complexity"] = cx
    # ------------------------------------------------------------------ coverage
    pb = json.loads((RES / "peer_build_stats.json").read_text()) if (RES / "peer_build_stats.json").exists() else {}
    cov = {"coverage_status_counts": {f"{t}|{s}": int(v) for (t, s), v in Counter(zip(df["track"], df["coverage_status"])).items()},
           "screen_label_counts": {f"{t}|{s}|{l}": int(v) for (t, s, l), v in Counter(zip(df["track"], df["system"], df["label"])).items()},
           "logiclm_parse_rate": {s: round(float((df[(df["track"] == "L") & (df["system"] == s)]["label"] != "UNPARSEABLE").mean()), 4) for s in LLM_SYSTEMS},
           "peer_build_stats": pb,
           "mean_pool_size_primary": round(float(P["n_peers_parsed"].mean()), 3),
           "z3_timeouts_in_pools": int(df["n_timeouts"].fillna(0).sum())}
    pr = defaultdict(lambda: [0, 0])
    for r in peer_lab:
        pr[r["peer"]][1] += 1
        pr[r["peer"]][0] += r["label"] not in ("UNPARSEABLE", "PEER_MISSING")
    cov["peer_parse_rate_on_screen_sentences"] = {p: round(k / n, 4) for p, (k, n) in sorted(pr.items())}
    S_["coverage"] = cov
    # ------------------------------------------------------------------ cost
    cl = [json.loads(l) for l in (ROOT / "logs" / "cost_log.jsonl").read_text().splitlines() if l.strip()]
    tot = sum(r["cost_usd"] for r in cl)
    by_model = defaultdict(float)
    by_mt = defaultdict(lambda: [0.0, set()])
    lat = defaultdict(list)
    for r in cl:
        by_model[r["model"]] += r["cost_usd"]
        ut = r["unit_id"].split(":")[0]
        by_mt[(r["model"], ut)][0] += r["cost_usd"]
        by_mt[(r["model"], ut)][1].add((r["unit_id"], r.get("sample")))
    from peers import PEERS, SC_CHEAP, SC_SAME
    peer_models = [m for _, m, _ in PEERS]
    n_sent_cov = len({x["sentence_key"] for x in items})
    peer_cost = sum(by_model[m] for m in peer_models)
    story_units = {k: v for k, v in by_mt.items() if k[1] in ("F", "P") and k[0] in peer_models}
    malls = {k: v for k, v in by_mt.items() if k[1] == "M" and k[0] in peer_models}
    cost = {"total_usd": round(tot, 4), "by_model_usd": {m: round(v, 4) for m, v in sorted(by_model.items())},
            "per_unit_usd": {f"{m}|{t}": round(v[0] / max(1, len(v[1])), 6) for (m, t), v in sorted(by_mt.items())},
            "C_peer_cost_total_usd": round(peer_cost, 4),
            "C_story_amortised_per_sentence_usd": round(sum(v[0] for v in story_units.values()) /
                                                        max(1, len({x['sentence_key'] for x in items if x['kind'] != 'malls'})), 6),
            "C_single_sentence_MALLS_per_sentence_usd": round(sum(v[0] for v in malls.values()) / 100, 6),
            "C_all_sentences_per_sentence_usd": round(peer_cost / max(1, n_sent_cov), 6),
            "gate_usd_per_item": 0.002,
            "sc_cheap_total_usd": round(by_model[SC_CHEAP[1]], 4), "sc_same_total_usd": round(by_model[SC_SAME[1]], 4),
            "sc_cheap_per_unit_K5_usd": round(by_model[SC_CHEAP[1]] / max(1, len({r["unit_id"] for r in cl if r["model"] == SC_CHEAP[1]})), 6),
            "z3_seconds_per_candidate_mean": round(float(df["seconds_z3"].fillna(0).mean()), 4),
            "z3_timing": cons["timing"]}
    lat_rows = [json.loads(l) for l in (RES / "peer_outputs.jsonl").read_text().splitlines() if l.strip()]
    lat_m = defaultdict(list)
    for r in lat_rows:
        if r.get("latency_s") is not None:
            lat_m[r["model"]].append(r["latency_s"])
    cost["api_latency_s_mean_per_call"] = {m: round(float(np.mean(v)), 2) for m, v in lat_m.items()}
    cost["C_gate_pass_story_amortised"] = cost["C_story_amortised_per_sentence_usd"] <= 0.002
    cost["C_gate_pass_single_sentence"] = cost["C_single_sentence_MALLS_per_sentence_usd"] <= 0.002
    S_["cost"] = cost
    # ------------------------------------------------------------------ secondary: peers as candidates
    pdf = pd.DataFrame(peer_lab)
    sec = {}
    if len(pdf):
        pdf["y"] = (pdf["label"] != "CORRECT").astype(int)
        pd2 = pdf[pdf["label"].isin(["CORRECT", "ERROR"])].copy()
        pd2["misalign"] = 1 - pd2["alignable_frac"]
        pd2["flag_medoid"] = pd2["medoid_flag"]
        pd2["sc5_cheap"] = [1 - v if v is not None and not (isinstance(v, float) and np.isnan(v)) else None for v in pd2.get("sc5_eq_frac_cheap", [None] * len(pd2))]
        sec["all_sentences"] = {sc: evaluate(pd2, sc, B // 2, thr_flag="flag_medoid" if sc == "c_score" else None)
                                for sc in ("c_score", "cluster_entropy", "sc5_cheap", "misalign")}
        tl = pd2[pd2["sentence_tracks"].map(lambda t: "L" in t)]
        sec["trackL_sentences"] = {sc: evaluate(tl, sc, B // 2) for sc in ("c_score", "sc5_cheap", "misalign")}
        va = pd2[pd2["alignable_frac"] == 1.0]
        sec["vocab_clean"] = {sc: evaluate(va, sc, B // 2) for sc in ("c_score", "sc5_cheap")}
        sec["paired_c_score-sc5_cheap"] = paired_delta(pd2, "c_score", "sc5_cheap", B // 2)
        sec["per_family"] = {f: {"n": len(g), "n_err": int(g["y"].sum()), "auroc_c_score": evaluate(g, "c_score", 200).get("auroc")}
                             for f, g in pd2.groupby("family")}
        sec["label_counts_per_family"] = {f: dict(Counter(g["label"])) for f, g in pdf.groupby("family")}
        mix = {}
        for f, g in pdf[pdf["label"] == "ERROR"].groupby("family"):
            mix[f] = dict(Counter(op_class(o) for o in g["repair_ops"]))
        sec["error_op_class_mix_per_family"] = mix
        sec["compound_share_per_family"] = {f: round(float((g["label"] == "UNCERTAIN_COMPOUND").mean()), 4) for f, g in pdf.groupby("family")}
    S_["secondary_peer_as_candidate"] = sec
    # system level (descriptive): 3 Logic-LM + 6 peer systems on the same primary sentences
    sys_rows = []
    for s, g in P.groupby("system"):
        sys_rows.append((s, float(g["y"].mean()), float(g["c_score"].mean()), float(g["sc5_cheap"].mean())))
    if len(pdf):
        for f, g in pd2.groupby("model"):
            sys_rows.append((f, float(g["y"].mean()), float(g["c_score"].mean()), float(pd.Series(g["sc5_cheap"]).astype(float).mean())))
    if len(sys_rows) >= 3:
        er = [r[1] for r in sys_rows]
        S_["system_level"] = {"systems": [{"system": r[0], "error_rate": round(r[1], 4), "mean_c_score": round(r[2], 4), "mean_sc5_cheap": round(r[3], 4)} for r in sys_rows],
                              "spearman_error_rate_vs_mean_c_score": round(float(spearmanr(er, [r[2] for r in sys_rows]).correlation), 4),
                              "spearman_error_rate_vs_mean_sc5_cheap": round(float(spearmanr(er, [r[3] for r in sys_rows]).correlation), 4),
                              "note": "descriptive only; systems are few and labelled on different sentence sets for peers vs Logic-LM"}
    # ------------------------------------------------------------------ sanity checks T5
    gold = pd.DataFrame(cons["gold_as_candidate"])
    gL = gold[gold["is_trackL"]] if len(gold) else gold
    S_["sanity"] = {"gold_as_candidate_mean_eq_frac_trackL": round(float(gL["eq_frac_full"].dropna().mean()), 4) if len(gL) else None,
                    "trackL_ERROR_mean_eq_frac": round(float(P[P["y"] == 1]["eq_frac_full"].dropna().mean()), 4),
                    "trackL_CORRECT_mean_eq_frac": round(float(P[P["y"] == 0]["eq_frac_full"].dropna().mean()), 4)}
    S_["sanity"]["gold_exceeds_error"] = (S_["sanity"]["gold_as_candidate_mean_eq_frac_trackL"] or 0) > S_["sanity"]["trackL_ERROR_mean_eq_frac"]
    pl = cons["planted"]
    if pl:
        room = [p for p in pl if p["base_c_score"] < 1.0]
        S_["sanity"]["planted"] = {"n": len(pl), "ops": dict(Counter(p["op"] for p in pl)),
                                   "rises_strict": round(sum(p["rises"] for p in pl) / len(pl), 4),
                                   "rises_among_items_with_room": round(sum(p["rises"] for p in room) / max(1, len(room)), 4), "n_with_room": len(room),
                                   "pass_70pct": (sum(p["rises"] for p in room) / max(1, len(room))) >= 0.7,
                                   "note": "pipeline check only; never reported as validation"}
    # ------------------------------------------------------------------ rewrite invariance
    rw = pd.DataFrame([r for r in cons["rewrites"] if r.get("applicable")])
    inv = {}
    if len(rw):
        for fam, g in rw.groupby("family"):
            g2 = g[g["reparse_ok"] == True]  # noqa: E712
            g2 = g2[g2["eq_frac_full"].notna()] if "eq_frac_full" in g2 else g2
            inv[fam] = {"n_applicable": len(g), "n_scored": len(g2),
                        "n_proved_equivalent": int((g["equivalent_to_original"] == True).sum()),  # noqa: E712
                        "false_alarm_rate": round(float(g2["flag"].mean()), 4) if len(g2) else None,
                        "false_alarm_ci95": wilson(int(g2["flag"].sum()), len(g2)) if len(g2) else None,
                        "base_false_alarm_rate": round(float(g2["base_flag"].mean()), 4) if len(g2) else None,
                        "flip_rate": round(float((g2["flag"] != g2["base_flag"]).mean()), 4) if len(g2) else None,
                        "mean_abs_delta_eq_frac": round(float((g2["eq_frac_full"] - g2["base_eq_frac_full"]).abs().mean()), 4) if len(g2) else None}
        inv["note"] = ("z3-equivalent families (REORDER, DEMORGAN, PRENEX, CONTRAPOSITIVE) are invariant BY CONSTRUCTION of eqmv; "
                       "RENAME (WordNet synonym heads + hashed constants) is the real test of the aligner")
    S_["rewrite_invariance"] = inv
    # ------------------------------------------------------------------ label-noise context
    Hh = df[df["track"] == "H"]
    S_["label_noise_context"] = {
        "trackH_original_gold_not_CORRECT_share": round(float((Hh["label"] != "CORRECT").mean()), 4),
        "trackH_label_counts": dict(Counter(Hh["label"])),
        "trackL_CORRECT_via_VOCAB_share": round(float((P[P["y"] == 0]["auto_class"] == "VOCAB").mean()), 4),
        "trackL_CORRECT_VOCAB_nonstrict_share": round(float(((P["y"] == 0) & (P["auto_class"] == "VOCAB") & (P["vocab_strict"] == False)).sum() / max(1, (P["y"] == 0).sum())), 4),  # noqa: E712
        "trackL_uncertain_compound_share": round(float((df[df["track"] == "L"]["label"] == "UNCERTAIN_COMPOUND").mean()), 4)}
    S_["prereg"] = {"hash_check": "screen_label_hash matches prereg.json", "screen_label_hash": h, "written_utc": prereg["written_utc"]}
    S_["score_definitions"] = SCORES
    S_["n"] = {"screen_items": len(df), "primary_n": len(P), "primary_err": int(P["y"].sum()), "primary_cor": int((P["y"] == 0).sum())}
    (RES / f"summary{suffix}.json").write_text(json.dumps(S_, ensure_ascii=False, indent=1, default=str))
    df.drop(columns=["strata"]).to_json(RES / f"analysis_table{suffix}.jsonl", orient="records", lines=True, force_ascii=False)
    write_method_out(df, S_, suffix)
    logger.info(f"summary written: {RES / f'summary{suffix}.json'}")


def write_method_out(df: pd.DataFrame, S_: dict, suffix: str):
    def s(v):
        if v is None or (isinstance(v, float) and np.isnan(v)):
            return "NA"
        return str(round(v, 6)) if isinstance(v, float) else str(v)
    ds = defaultdict(list)
    for _, r in df.iterrows():
        name = f"logiclm_folio_dev_trackL" if r["track"] == "L" else ("malls_test_curated_trackH" if r["kind"] == "malls" else "folio_val_curated_trackH")
        ex = {"input": f"TEXT: {r['text']}\nCANDIDATE FOL: {r['candidate_fol']}", "output": str(r["label"]),
              "predict_c_score": s(r["c_score"]), "predict_medoid_depth": s(r["medoid_depth"]),
              "predict_cluster_entropy": s(r["cluster_entropy"]), "predict_sc5_cheap": s(r["sc5_cheap"]),
              "predict_sc5_same": s(r["sc5_same"]), "predict_flag_medoid": s(bool(r["flag_medoid"])),
              "predict_c_score_peers6": s(r["c_score_peers6"]),
              "metadata_item_id": r["item_id"], "metadata_track": r["track"], "metadata_system": r["system"], "metadata_kind": r["kind"],
              "metadata_reference_fol": r["reference_fol"], "metadata_auto_class": r["auto_class"], "metadata_repair_ops": list(r["repair_ops"] or []),
              "metadata_strata": {k: r[k] for k in ("len_bin", "words", "nq_bin", "depth_bin", "ncond_bin", "exception")},
              "metadata_eq_frac_full": r["eq_frac_full"], "metadata_eq_frac_peers6": r["eq_frac_peers6"],
              "metadata_eq_frac_nonoai": r["eq_frac_nonoai"], "metadata_eq_frac_llm2": r["eq_frac_llm2"],
              "metadata_medoid": r["medoid"], "metadata_medoid_fol": r["medoid_fol"], "metadata_medoid_ops": list(r["medoid_ops"] or []),
              "metadata_medoid_support": r["medoid_support"], "metadata_medoid_label": r["medoid_label"],
              "metadata_n_peers_parsed": int(r["n_peers_parsed"]), "metadata_n_peers_total": int(r["n_peers_total"]),
              "metadata_coverage_status": r["coverage_status"], "metadata_alignable_frac": r["alignable_frac"],
              "metadata_sc5_eq_frac_cheap": r["sc5_eq_frac_cheap"], "metadata_sc5_eq_frac_same": r["sc5_eq_frac_same"],
              "metadata_seconds_z3": r["seconds_z3"], "metadata_sentence_key": r["sentence_key"]}
        ex = {k: (None if isinstance(v, float) and np.isnan(v) else v) for k, v in ex.items()}
        ds[name].append(ex)
    P = S_["auroc"]["primary"]
    meta = {"method_name": "Candidate C: cross-system z3 consensus (eq_frac / medoid repair / semantic entropy) vs K=5 self-consistency",
            "primary_contrast": "track L CORRECT vs ERROR",
            "headline": {sc: {k: P[sc].get(k) for k in ("n", "n_err", "auroc", "auroc_ci95", "auprc", "prevalence")} for sc in P},
            "summary_file": "results/summary.json", "prereg_file": "results/prereg.json", "label_hash": S_["prereg"]["screen_label_hash"],
            "cost_total_usd": S_["cost"]["total_usd"]}
    out = {"metadata": meta, "datasets": [{"dataset": k, "examples": v} for k, v in sorted(ds.items())]}
    (ROOT / f"method_out{suffix}.json").write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str))


if __name__ == "__main__":
    main()
