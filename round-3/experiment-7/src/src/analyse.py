#!/usr/bin/env python3
"""S10: pre-registered analysis of R_COMP-SIG (primary) and R_COMP-FREE (sign readout). CPU only, $0.

Every metric is oriented so that HIGHER = MORE LIKELY ERROR:
  c_score_sig, c_score_align, c_score_nf (NF-anchored), c_score_hyb   (share of family-disjoint peers NOT agreeing)
  g_align = ALIGN:g_score, g_nf = NF-anchored:g_score                  (graded consensus, exp 5; g = 1 - F1(support,
                                                                        coverage) is ALREADY error-oriented, peer_text.py
                                                                        l.812, so the plan's "1 - g" would invert it)
  judge_* = 1 - P(faithful)                                             (flash-lite cheap, gemini-3.1-pro frontier, local Qwen3-8B)
Primary (prereg_sig.json): delta_strat = AUROC_within_template(c_score_sig) - AUROC_within_template(judge_cheap_disg) on the
SIG primary pool (10 few-shot slots, labels CORRECT/ERROR) restricted to rows where both scores exist; sentence-clustered
bootstrap stratified by template, B=2000, seed 20260924; PASS iff the 95% CI lower bound > 0.

Guards (T7): testability_<COND>.json must exist, predate this run and every SIG score file, and its label-vector sha256 must
equal the one recomputed from the label file. The analysis refuses to run otherwise.

Outputs: results/analysis.json, results/tables.md, results/rcomp_candidates.jsonl, results/analysis_rows_{SIG,FREE}.jsonl.
usage: analyse.py [--B 2000] [--no-free]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
import warnings
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RES = ROOT / "results"
RC = ROOT / "rcomp"
sys.path.insert(0, str(ROOT / "src"))
from loguru import logger  # noqa: E402

from auc_tools import StratAUC, boot_weights, summarize  # noqa: E402

SEED = 20260924
FEW = ["G1", "G1b", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9"]
FAM = {"G1": "meta", "G1b": "meta", "G2": "qwen", "G3": "mistral", "G4": "deepseek", "G5": "google", "G8": "google",
       "G6": "microsoft", "G7": "openai", "F": "openai", "G9": "cohere"}  # exp-5 family_map_vendor
CONS = ["c_score_sig", "c_score_align", "c_score_nf", "c_score_hyb", "g_align", "g_nf"]
JUDGES = ["judge_cheap_disg", "judge_cheap_orig", "judge_frontier_orig", "judge_frontier_disg", "judge_local_disg",
          "judge_local_orig"]
METRICS = CONS + JUDGES
PRIMARY_BAR = "judge_cheap_disg"


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest()


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating, float)):
        return None if (o is None or math.isnan(o) or math.isinf(o)) else float(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.bool_):
        return bool(o)
    return o


# ---------------------------------------------------------------------------------------------------------------- load
def load_judges(p: Path) -> dict:
    d = {}
    for r in jl(p):
        if r.get("p") is not None:
            d[(r["row_key"], r["cond"])] = float(r["p"])
    return d


def load_judge_cost(p: Path) -> list[float]:
    return [float(r["cost"]) for r in jl(p) if r.get("p") is not None and r.get("cost")]


def load_scores(p: Path) -> tuple[dict, dict]:
    rows, stats = {}, {}
    for r in jl(p):
        stats[r["sentence_id"]] = r.get("stats", {})
        for k, v in r["rows"].items():
            rows[k] = v
    return rows, stats


def oriented(sc: dict) -> dict:
    g = lambda k: sc.get(k)  # noqa: E731
    return {"c_score_sig": g("c_score_sig"), "c_score_align": g("c_score_align"), "c_score_nf": g("NF-anchored:c_score_nf"),
            "c_score_hyb": g("c_score_hyb"), "g_align": g("ALIGN:g_score"), "g_nf": g("NF-anchored:g_score")}


def sentences() -> dict:
    return {s["sentence_id"]: s for s in json.loads((RC / "work" / "rcomp_sentences.json").read_text())}


def strata_of(s: dict, cuts: dict) -> dict:
    w = s["words"]
    return {"words": w, "word_tercile": "W1" if w < cuts["cut_1"] else ("W2" if w < cuts["cut_2"] else "W3"),
            "nconds_weak": s["nconds_weak"], "nconds_bin": str(min(s["nconds_weak"], 6)) if s["nconds_weak"] < 6 else ">=6",
            "depth_weak": s["depth_weak"], "nquant": s["nquant"], "nested": bool(s["nested"]),
            "negated_condition": s.get("negated_condition") is not None, "clause_type": s["clause_type"],
            "template_id": s["template_id"]}


def build_sig(S: dict, cuts: dict) -> list[dict]:
    labs = jl(RES / "sig_labels.jsonl")
    sc, _ = load_scores(RES / "scores_SIG.jsonl")
    jc = load_judges(RES / "judge_SIG.jsonl")
    jf = load_judges(RES / "judge_frontier_SIG.jsonl")
    jlo = load_judges(RES / "judge_local_SIG.jsonl")
    rep = {r["class_id"]: r for r in jl(RES / "sig_repairs.jsonl")}
    out = []
    for r in labs:
        s = S[r["sentence_id"]]
        k = r["row_key"]
        x = sc.get(k, {})
        m = oriented(x)
        for name, d, c in (("judge_cheap_disg", jc, "disg"), ("judge_cheap_orig", jc, "orig"), ("judge_frontier_orig", jf, "orig"),
                           ("judge_frontier_disg", jf, "disg"), ("judge_local_disg", jlo, "disg"), ("judge_local_orig", jlo, "orig")):
            p = d.get((k, c))
            m[name] = None if p is None else 1.0 - p
        rp = rep.get(r.get("sig_class_id") or "", {})
        out.append({"row_key": k, "item_id": r["item_id"], "sentence_id": r["sentence_id"], "condition": "SIG", "slot": r["slot"],
                    "system": r["system"], "family": FAM.get(r["slot"], r["family"]), "prompt_variant": r["prompt_variant"],
                    "text": s["text"], "candidate_fol": r["candidate_fol"], "parse_ok": r["parse_ok"], "label": r["label"],
                    "label_source": r["label_source"], "label_tier": r.get("label_tier"), "matched_reading": r.get("matched_reading"),
                    "off_signature": r.get("off_signature"), "sig_status": r.get("sig_status"), "label_loose": r.get("label_loose"),
                    "sig_class_id": r.get("sig_class_id"), "repair_status": rp.get("repair_status"),
                    "repair_ops": rp.get("repair_ops"), "cost_usd": r.get("cost_usd"),
                    "n_peers_sig": x.get("n_peers_sig"), "n_peers_equal_sig": x.get("n_peers_equal_sig"),
                    "n_unknown_sig": x.get("n_unknown_sig"), "peer_equal_sig": x.get("peer_equal_sig"),
                    "peer_equal_align": x.get("peer_equal_align"), "peer_equal_nf": x.get("peer_equal_nf"),
                    "secs_sig": x.get("secs_sig"), "coverage_status": x.get("coverage_status"),
                    "strata": strata_of(s, cuts), "template_id": s["template_id"], **m})
    return out


def build_free(S: dict, cuts: dict) -> list[dict]:
    labs = jl(RES / "free_labels.jsonl")
    sc, _ = load_scores(RES / "scores_FREE.jsonl")
    jc = load_judges(RES / "judge_FREE.jsonl")
    jlo = load_judges(RES / "judge_local_FREE.jsonl")
    out = []
    for r in labs:
        s = S[r["sentence_id"]]
        k = r["row_key"]
        x = sc.get(k, {})
        m = oriented(x)
        m["c_score_sig"] = None
        for name, c in (("judge_cheap_disg", "disg"), ("judge_cheap_orig", "orig")):
            p = jc.get((k, c))
            m[name] = None if p is None else 1.0 - p
        for name in ("judge_frontier_orig", "judge_frontier_disg", "judge_local_orig"):
            m[name] = None
        p = jlo.get((k, "disg"))
        m["judge_local_disg"] = None if p is None else 1.0 - p
        out.append({"row_key": k, "item_id": r["item_id"], "sentence_id": r["sentence_id"], "condition": "FREE", "slot": r["slot"],
                    "system": r["system"], "family": FAM.get(r["slot"], r["family"]), "prompt_variant": r["prompt_variant"],
                    "text": s["text"], "candidate_fol": r["candidate_fol"], "parse_ok": r["parse_ok"], "label": r["label"],
                    "label_source": r["label_source"], "label_tier": r["label_tier"], "matched_reading": r.get("matched_reading"),
                    "solver_label": r["solver_label"], "repair_ops": r.get("solver_repair_ops") or r.get("panel_ops"),
                    "correct_not_equivalent": r.get("correct_not_equivalent"), "ref_flagged": r.get("ref_flagged"),
                    "tier_B_provisional": r.get("tier_B_provisional"), "free_solver_class_id": r.get("free_solver_class_id"),
                    "panel_votes": r.get("panel_votes"), "route_priority": r.get("route_priority"),
                    "n_peers_hyb": x.get("n_peers_hyb"), "peer_equal_align": x.get("peer_equal_align"),
                    "peer_equal_nf": x.get("peer_equal_nf"), "coverage_status": x.get("coverage_status"),
                    "strata": strata_of(s, cuts), "template_id": s["template_id"], **m})
    return out


# ------------------------------------------------------------------------------------------------------ AUROC blocks
class Ctx:
    """Per condition: sentence index + ONE set of bootstrap weights (paired across every metric and comparison)."""

    def __init__(self, rows: list[dict], B: int):
        sids = sorted({r["sentence_id"] for r in rows})
        self.sidx = {s: i for i, s in enumerate(sids)}
        tm = {r["sentence_id"]: r["template_id"] for r in rows}
        self.W = boot_weights(np.array([tm[s] for s in sids]), B, SEED)
        self.B = B


def _arrays(ctx: Ctx, rows: list[dict], key: str, stratum: str):
    s = np.array([r[key] for r in rows], dtype=float)
    y = np.array([r["label"] == "ERROR" for r in rows])
    cl = np.array([ctx.sidx[r["sentence_id"]] for r in rows])
    if stratum == "template":
        st = np.array([r["template_id"] for r in rows])
    elif stratum == "sentence":
        st = cl.copy()
    elif stratum == "pooled":
        st = np.zeros(len(rows), dtype=int)
    else:
        st = np.array([r["strata"][stratum] for r in rows])
    return s, y, st, cl


def auc_obj(ctx: Ctx, rows: list[dict], key: str, stratum: str) -> StratAUC:
    s, y, st, cl = _arrays(ctx, rows, key, stratum)
    return StratAUC(s, y, st, cl, stratum_is_cluster=(stratum == "sentence"))


def counts(rows: list[dict]) -> dict:
    return {"n": len(rows), "n_error": sum(r["label"] == "ERROR" for r in rows), "n_correct": sum(r["label"] == "CORRECT" for r in rows),
            "n_sentences": len({r["sentence_id"] for r in rows})}


def auc_block(ctx: Ctx, rows: list[dict], key: str, stratum: str = "template", boot: bool = True) -> dict:
    rows = [r for r in rows if r.get(key) is not None]
    c = counts(rows)
    if c["n_error"] == 0 or c["n_correct"] == 0:
        return {**c, "auroc": None, "untestable": True}
    a = auc_obj(ctx, rows, key, stratum)
    pt = a.value()
    out = {**c, "auroc": pt, "n_pairs": a.n_pairs()}
    if boot:
        bs = np.array([a.value(ctx.W[b]) for b in range(ctx.B)])
        sm = summarize(pt, bs)
        out.update({"ci": sm["ci"], "se": sm["se"]})
    if stratum == "pooled":
        from sklearn.metrics import average_precision_score
        y = np.array([r["label"] == "ERROR" for r in rows])
        out["auprc"] = float(average_precision_score(y, np.array([r[key] for r in rows], dtype=float)))
        out["prevalence"] = float(y.mean())
    return out


def delta_block(ctx: Ctx, rows: list[dict], k1: str, k2: str, stratum: str = "template") -> dict:
    rows = [r for r in rows if r.get(k1) is not None and r.get(k2) is not None]
    c = counts(rows)
    if c["n_error"] == 0 or c["n_correct"] == 0:
        return {**c, "untestable": True}
    a1, a2 = auc_obj(ctx, rows, k1, stratum), auc_obj(ctx, rows, k2, stratum)
    p1, p2 = a1.value(), a2.value()
    b1 = np.array([a1.value(ctx.W[b]) for b in range(ctx.B)])
    b2 = np.array([a2.value(ctx.W[b]) for b in range(ctx.B)])
    d = b1 - b2
    ok = ~np.isnan(d)
    sm = summarize(p1 - p2, d)
    return {**c, "metric": k1, "comparator": k2, "stratum": stratum, "auroc_metric": p1, "auroc_comparator": p2,
            "auroc_metric_ci": summarize(p1, b1)["ci"], "auroc_comparator_ci": summarize(p2, b2)["ci"],
            "delta": p1 - p2, "ci": sm["ci"], "se": sm["se"], "p_one_sided": float(np.mean(d[ok] <= 0)) if ok.any() else None,
            "ci_lower_gt_0": bool(sm["ci"][0] is not None and sm["ci"][0] > 0)}


# ------------------------------------------------------------------------------------------------------ pieces of S10
def op_point(rows: list[dict], key: str) -> dict:
    rows = [r for r in rows if r.get(key) is not None]
    if not rows:
        return {"n": 0}
    judge = key.startswith("judge")
    flag = np.array([(r[key] > 0.5) if judge else (r[key] >= 0.5) for r in rows])
    y = np.array([r["label"] == "ERROR" for r in rows])
    tp, fp = int((flag & y).sum()), int((flag & ~y).sum())
    from sklearn.metrics import average_precision_score
    return {"n": len(rows), "threshold": "P(faithful) < 0.5 (verdict)" if judge else "score >= 0.5",
            "precision": tp / max(1, tp + fp), "recall": tp / max(1, int(y.sum())), "fa_rate": fp / max(1, int((~y).sum())),
            "flag_rate": float(flag.mean()), "prevalence": float(y.mean()),
            "auprc": float(average_precision_score(y, [r[key] for r in rows])) if 0 < y.sum() < len(y) else None}


def nested(ctx: Ctx, rows: list[dict], base: list[str], add: list[str], tag: str) -> dict:
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler
    feats = base + add
    rows = [dict(r) for r in rows if all(r.get(f) is not None for f in feats)]
    c = counts(rows)
    if c["n_error"] < 5 or c["n_correct"] < 5:
        return {**c, "untestable": True}
    y = np.array([r["label"] == "ERROR" for r in rows]).astype(int)
    fold = np.array([int(sha1("RCOMP_folds_v1|" + r["sentence_id"]), 16) % 5 for r in rows])
    for name, fs in (("oof_base", base), ("oof_full", feats)):
        X = np.array([[r[f] for f in fs] for r in rows], dtype=float)
        oof = np.full(len(rows), np.nan)
        for k in range(5):
            tr, te = fold != k, fold == k
            if te.sum() == 0 or len(set(y[tr])) < 2:
                continue
            scl = StandardScaler().fit(X[tr])
            lr = LogisticRegression(C=1.0, max_iter=2000).fit(scl.transform(X[tr]), y[tr])
            oof[te] = lr.predict_proba(scl.transform(X[te]))[:, 1]
        for r, v in zip(rows, oof):
            r[name] = None if np.isnan(v) else float(v)
    return {"model": tag, "base": base, "added": add,
            "within_template": delta_block(ctx, rows, "oof_full", "oof_base", "template"),
            "pooled": delta_block(ctx, rows, "oof_full", "oof_base", "pooled")}


def gee_block(rows: list[dict], metrics: list[str], var: str) -> dict:
    """decision correctness at the frozen threshold ~ z(var), binomial GEE, exchangeable, groups = sentence_id."""
    import pandas as pd
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    out = {}
    recs = []
    for m in metrics:
        judge = m.startswith("judge")
        for r in rows:
            if r.get(m) is None:
                continue
            flag = (r[m] > 0.5) if judge else (r[m] >= 0.5)
            recs.append({"metric": m, "correct": int(flag == (r["label"] == "ERROR")), "x": float(r["strata"][var]),
                         "sid": r["sentence_id"]})
    df = pd.DataFrame(recs)
    if df.empty:
        return {"untestable": True}
    mu, sd = df["x"].mean(), df["x"].std(ddof=0) or 1.0
    df["z"] = (df["x"] - mu) / sd
    for m in metrics:
        d = df[df.metric == m]
        if d["correct"].nunique() < 2:
            out[m] = {"n": len(d), "untestable": True}
            continue
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                f = smf.gee("correct ~ z", "sid", d, family=sm.families.Binomial(), cov_struct=sm.cov_struct.Exchangeable()).fit()
            ci = f.conf_int().loc["z"].tolist()
            out[m] = {"n": len(d), "accuracy": float(d["correct"].mean()), "slope_logodds_per_sd": float(f.params["z"]),
                      "ci": ci, "p": float(f.pvalues["z"])}
        except Exception as e:  # noqa: BLE001 - a failed fit is reported, not hidden
            out[m] = {"n": len(d), "error": str(e)[:200]}
    # stacked interaction: each consensus metric vs the pre-registered bar
    for m in metrics:
        if m == PRIMARY_BAR or m.startswith("judge"):
            continue
        d = df[df.metric.isin([m, PRIMARY_BAR])].copy()
        common = set(d[d.metric == m].index.map(lambda i: None))  # placeholder to keep flake quiet
        del common
        d["is_cons"] = (d.metric == m).astype(int)
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                f = smf.gee("correct ~ is_cons * z", "sid", d, family=sm.families.Binomial(),
                            cov_struct=sm.cov_struct.Exchangeable()).fit()
            out[f"interaction_{m}_minus_{PRIMARY_BAR}"] = {"n": len(d), "coef": float(f.params["is_cons:z"]),
                                                           "ci": f.conf_int().loc["is_cons:z"].tolist(),
                                                           "p": float(f.pvalues["is_cons:z"])}
        except Exception as e:  # noqa: BLE001
            out[f"interaction_{m}_minus_{PRIMARY_BAR}"] = {"error": str(e)[:200]}
    out["variable"] = var
    out["z_mean_sd"] = [float(mu), float(sd)]
    return out


def permutation_placebo(rows: list[dict], k1: str, k2: str, n_perm: int = 200) -> dict:
    rows = [r for r in rows if r.get(k1) is not None and r.get(k2) is not None]
    rng = np.random.default_rng(SEED + 1)
    tmpl = np.array([r["template_id"] for r in rows])
    cl = np.array([r["sentence_id"] for r in rows])
    s1 = np.array([r[k1] for r in rows], dtype=float)
    s2 = np.array([r[k2] for r in rows], dtype=float)
    y = np.array([r["label"] == "ERROR" for r in rows])
    obs = StratAUC(s1, y, tmpl, cl).value() - StratAUC(s2, y, tmpl, cl).value()
    groups = defaultdict(list)
    for i, s in enumerate(cl):
        groups[s].append(i)
    ds = []
    for _ in range(n_perm):
        yp = y.copy()
        for idx in groups.values():
            idx = np.array(idx)
            yp[idx] = y[rng.permutation(idx)]
        ds.append(StratAUC(s1, yp, tmpl, cl).value() - StratAUC(s2, yp, tmpl, cl).value())
    ds = np.array(ds)
    return {"observed_delta": obs, "perm_mean": float(np.nanmean(ds)), "perm_p95": float(np.nanpercentile(ds, 95)),
            "perm_p_one_sided": float((np.sum(ds >= obs) + 1) / (len(ds) + 1)), "n_perm": n_perm,
            "observed_exceeds_p95": bool(obs > np.nanpercentile(ds, 95))}


def shuffle_placebos(rows: list[dict], k1: str, k2: str) -> dict:
    rows = [r for r in rows if r.get(k1) is not None and r.get(k2) is not None]
    rng = np.random.default_rng(SEED + 2)
    tmpl = np.array([r["template_id"] for r in rows])
    cl = np.array([r["sentence_id"] for r in rows])
    s1 = np.array([r[k1] for r in rows], dtype=float)
    s2 = np.array([r[k2] for r in rows], dtype=float)
    y = np.array([r["label"] == "ERROR" for r in rows])
    ysh = rng.permutation(y)
    s1s, s2s = s1.copy(), s2.copy()
    for s in np.unique(cl):
        idx = np.flatnonzero(cl == s)
        s1s[idx] = s1[rng.permutation(idx)]
        s2s[idx] = s2[rng.permutation(idx)]
    return {"global_label_shuffle_auroc_template_" + k1: StratAUC(s1, ysh, tmpl, cl).value(),
            "within_sentence_score_shuffle_auroc_sentence_" + k1: StratAUC(s1s, y, cl, cl, True).value(),
            "within_sentence_score_shuffle_delta_sentence": StratAUC(s1s, y, cl, cl, True).value() - StratAUC(s2s, y, cl, cl, True).value()}


def per_group_table(rows_all: list[dict], key) -> dict:
    d = defaultdict(Counter)
    for r in rows_all:
        d[key(r)][r["label"]] += 1
    return {k: dict(v) for k, v in sorted(d.items())}


def mechanism(rows_all: list[dict], pool: list[dict], cls_key: str, score_key: str) -> dict:
    """class sizes / peer majority per row + e (error endorsement) and d (correct divergence) by stratum."""
    by_s = defaultdict(list)
    for r in rows_all:
        by_s[r["sentence_id"]].append(r)
    for s, rs in by_s.items():
        peers = [r for r in rs if r["slot"] in FEW and r["prompt_variant"] in ("sig_v1", "fewshot_v1") and r["parse_ok"]]
        size = Counter(r.get(cls_key) for r in rs if r.get(cls_key))
        for r in rs:
            c = r.get(cls_key)
            P = [p for p in peers if p["family"] != r["family"] and p["row_key"] != r["row_key"]]
            pc = Counter(p.get(cls_key) or ("NOCLASS:" + p["row_key"]) for p in P)
            maj = pc.most_common(1)[0][0] if pc else None
            r[f"{cls_key}_size"] = size.get(c, 0) if c else 0
            r[f"{cls_key}_n_peers"] = len(P)
            r[f"{cls_key}_n_peers_same_class"] = sum(1 for p in P if c and p.get(cls_key) == c)
            r[f"{cls_key}_peer_majority_class"] = maj
            r[f"{cls_key}_is_peer_majority"] = bool(c and maj == c)
    pool = [r for r in pool if r.get(score_key) is not None]

    def ed(rs):
        er = [r for r in rs if r["label"] == "ERROR"]
        co = [r for r in rs if r["label"] == "CORRECT"]
        return {"n_error": len(er), "n_correct": len(co),
                "e_error_endorsement": (sum(r[score_key] < 0.5 for r in er) / len(er)) if er else None,
                "d_correct_divergence": (sum(r[score_key] >= 0.5 for r in co) / len(co)) if co else None}
    out = {"overall": ed(pool)}
    for strat in ("word_tercile", "nconds_bin", "template_id", "clause_type"):
        g = defaultdict(list)
        for r in pool:
            g[r["strata"][strat]].append(r)
        out[strat] = {k: ed(v) for k, v in sorted(g.items())}
    # distinct classes among ERROR vs CORRECT rows per sentence
    dc = {"ERROR": [], "CORRECT": []}
    for s, rs in by_s.items():
        for lab in dc:
            cs = {r.get(cls_key) for r in rs if r["label"] == lab and r.get(cls_key)}
            if cs:
                dc[lab].append(len(cs))
    out["distinct_classes_per_sentence"] = {k: {"mean": float(np.mean(v)) if v else None, "n_sentences": len(v)} for k, v in dc.items()}
    return out


def greedy_classes(rows_all: list[dict], hyb: bool) -> None:
    """free_align_class_id / free_hyb_class_id: greedy representative clustering in sha1(row_key) order; a row joins the
    first class whose representative it matches (pair known from either side's family-disjoint peer map). Pairs never
    compared (same family, or two zero-shot rows) count as not matching: non-transitive and order-dependent by design."""
    name = "free_hyb_class_id" if hyb else "free_align_class_id"
    by_s = defaultdict(list)
    for r in rows_all:
        by_s[r["sentence_id"]].append(r)

    def eq(a, b):
        for x, y in ((a, b), (b, a)):
            pa = x.get("peer_equal_align") or {}
            pn = x.get("peer_equal_nf") or {}
            if isinstance(pa, dict) and y["row_key"] in pa:
                return bool(pa[y["row_key"]] or (hyb and pn.get(y["row_key"])))
        return False
    for s, rs in by_s.items():
        reps = []
        for r in sorted(rs, key=lambda r: sha1(r["row_key"])):
            if not r["parse_ok"]:
                r[name] = None
                continue
            for i, rep in enumerate(reps):
                if eq(r, rep):
                    r[name] = f"{s}:{'h' if hyb else 'a'}{i}"
                    break
            else:
                reps.append(r)
                r[name] = f"{s}:{'h' if hyb else 'a'}{len(reps) - 1}"


def rename_block(sig_rows: list[dict]) -> dict:
    ren = {}
    for rec in jl(RES / "scores_rename_SIG.jsonl"):
        ren.update(rec["rows"])
    base = {r["row_key"]: r for r in sig_rows}
    out = {}
    for kind in ("RENAME_NONCE", "RENAME_SYN"):
        rs = [(k, v) for k, v in ren.items() if k.startswith(f"REN|{kind}|")]
        d = {"n_copies": len(rs)}
        for m in ("c_score_sig", "c_score_align", "c_score_nf", "c_score_hyb", "g_align", "g_nf"):
            vals, flips = [], []
            for k, v in rs:
                o = oriented(v)[m]
                if m == "c_score_sig" and o is None and v.get("sig_status_scorer") not in (None, "UNPARSEABLE"):
                    o = 1.0  # off-signature under exact names: no peer can match -> maximal suspicion (by design)
                if o is None:
                    continue
                vals.append(o)
                b = base.get(k.split("|", 2)[2], {}).get(m)
                if b is not None:
                    flips.append(int((o >= 0.5) and (b < 0.5)))
            d[m] = {"n": len(vals), "fa_rate_c_ge_0.5": (sum(v >= 0.5 for v in vals) / len(vals)) if vals else None,
                    "mean_score": float(np.mean(vals)) if vals else None,
                    "flip_rate_vs_original": (sum(flips) / len(flips)) if flips else None}
        out[kind] = d
    base_fa = {}
    cor = [r for r in sig_rows if r["label"] == "CORRECT"]
    for m in ("c_score_sig", "c_score_align", "c_score_nf", "c_score_hyb", "g_align", "g_nf"):
        v = [r[m] for r in cor if r.get(m) is not None]
        base_fa[m] = (sum(x >= 0.5 for x in v) / len(v)) if v else None
    out["reference_unrenamed_correct_fa"] = base_fa
    out["note"] = ("renamed copies of SIG CORRECT rows scored as extra candidates against the UNCHANGED peer pool; FA = share "
                   "flagged (c >= 0.5); c_score_sig of an off-signature copy is set to 1.0 (exact names cannot match), which "
                   "is expected by design: SIG-exact is a labelling-regime metric, not a deployable one")
    return out


def cost_block(sig_rows: list[dict]) -> dict:
    gen = defaultdict(lambda: defaultdict(float))
    for r in jl(RC / "raw" / "generations_sig.jsonl"):
        if r.get("raw_output") is not None:
            gen[r["sentence_id"]][r["slot"]] += float(r.get("cost_usd") or 0.0)
    per_slot = defaultdict(list)
    for s, d in gen.items():
        for k, v in d.items():
            per_slot[k].append(v)
    cons_cost = []
    for r in sig_rows:
        d = gen.get(r["sentence_id"], {})
        cons_cost.append(sum(v for k, v in d.items() if FAM.get(k) != r["family"]))
    _, st = load_scores(RES / "scores_SIG.jsonl")
    cpu = [(v.get("secs_total", 0) / max(1, v.get("n_rows", 1))) for v in st.values() if v.get("secs_total") is not None]
    cpu_sig = [(v.get("secs_sig", 0) / max(1, v.get("n_rows", 1))) for v in st.values() if v.get("secs_sig") is not None]
    cheap = load_judge_cost(RES / "judge_SIG.jsonl") + load_judge_cost(RES / "judge_FREE.jsonl")
    fr = load_judge_cost(RES / "judge_frontier_SIG.jsonl")
    loc = [r["seconds"] for r in jl(RES / "judge_local_SIG.jsonl") if r.get("seconds")]
    led = defaultdict(float)
    for r in jl(ROOT / "cost_ledger.jsonl"):
        led[r.get("phase", "?")] += float(r.get("usd") or 0)
    return {"generation_usd_per_sentence_per_slot": {k: float(np.mean(v)) for k, v in sorted(per_slot.items())},
            "consensus_peer_generation_usd_per_candidate_mean": float(np.mean(cons_cost)) if cons_cost else None,
            "consensus_cpu_s_per_row_all_variants_mean": float(np.mean(cpu)) if cpu else None,
            "consensus_sig_exact_cpu_s_per_row_mean": float(np.mean(cpu_sig)) if cpu_sig else None,
            "judge_cheap_usd_per_call_mean": float(np.mean(cheap)) if cheap else None,
            "judge_frontier_usd_per_call_mean": float(np.mean(fr)) if fr else None,
            "judge_local_gpu_s_per_call_mean": float(np.mean(loc)) if loc else None,
            "frontier_over_consensus_cost_ratio": (float(np.mean(fr)) / float(np.mean(cons_cost))) if fr and cons_cost and np.mean(cons_cost) > 0 else None,
            "artifact_ledger_usd_by_phase": dict(led), "artifact_ledger_usd_total": float(sum(led.values()))}


def system_level(pool: list[dict], metrics: list[str]) -> dict:
    from scipy.stats import pearsonr, spearmanr
    by = defaultdict(list)
    for r in pool:
        by[r["slot"]].append(r)
    err = {k: sum(r["label"] == "ERROR" for r in v) / len(v) for k, v in by.items()}
    out = {"error_rate_by_slot": err}
    for m in metrics:
        pairs = [(err[k], float(np.mean([r[m] for r in v if r.get(m) is not None]))) for k, v in by.items()
                 if any(r.get(m) is not None for r in v)]
        if len(pairs) >= 4:
            a, b = zip(*pairs)
            out[m] = {"n_systems": len(pairs), "spearman": float(spearmanr(a, b)[0]), "pearson": float(pearsonr(a, b)[0])}
    return out


def error_type_block(ctx: Ctx, pool: list[dict], metrics: list[str]) -> dict:
    ops = Counter(o for r in pool if r["label"] == "ERROR" for o in (r.get("repair_ops") or ["COMPOUND"]))
    out = {"op_counts_error_rows": dict(ops)}
    cor = [r for r in pool if r["label"] == "CORRECT"]
    for op, n in ops.most_common():
        if n < 10:
            continue
        er = [r for r in pool if r["label"] == "ERROR" and op in (r.get("repair_ops") or ["COMPOUND"])]
        d = {"n_error_rows": n}
        for m in metrics:
            sub = [r for r in er + cor if r.get(m) is not None]
            a = auc_block(ctx, sub, m, "template", boot=False)
            erm = [r for r in er if r.get(m) is not None]
            judge = m.startswith("judge")
            d[m] = {"auroc_within_template_vs_all_correct": a.get("auroc"),
                    "recall_at_frozen_threshold": (sum((r[m] > 0.5) if judge else (r[m] >= 0.5) for r in erm) / len(erm)) if erm else None}
        out[op] = d
    return out


# --------------------------------------------------------------------------------------------------------- guards
def label_sha(pool: list[dict]) -> str:
    return hashlib.sha256(json.dumps(sorted((r["row_key"], r["label"]) for r in pool)).encode()).hexdigest()


def guard(cond: str, t_start: float, score_files: list[Path]) -> dict:
    p = RES / f"testability_{cond}.json"
    if not p.exists():
        raise SystemExit(f"{p.name} missing: analysis refuses to run")
    t = json.loads(p.read_text())
    mt = p.stat().st_mtime
    if mt >= t_start:
        raise SystemExit(f"{p.name} is newer than the analysis start")
    before = {f.name: (f.stat().st_mtime > mt) for f in score_files if f.exists()}
    return {"file": p.name, "mtime_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(mt)), "verdict": t["verdict"],
            "sha256_declared": t["sha256_label_vector"], "score_files_newer_than_declaration": before}


# ----------------------------------------------------------------------------------------------------------- SIG
def analyse_sig(B: int) -> tuple[dict, list[dict]]:
    t_start = time.time()
    S = sentences()
    tsig = json.loads((RES / "testability_SIG.json").read_text())
    cuts = tsig["word_terciles"]
    g = guard("SIG", t_start, [RES / "scores_SIG.jsonl", RES / "judge_SIG.jsonl", RES / "judge_frontier_SIG.jsonl",
                               RES / "judge_local_SIG.jsonl", RES / "scores_rename_SIG.jsonl"])
    if not all(g["score_files_newer_than_declaration"].values()):
        raise SystemExit(f"a SIG score file predates the testability declaration: {g}")
    rows = build_sig(S, cuts)
    pool = [r for r in rows if r["slot"] in FEW and r["label"] in ("CORRECT", "ERROR")
            and S[r["sentence_id"]]["batch"] == "main"]
    sha = label_sha(pool)
    if sha != tsig["sha256_label_vector"]:
        raise SystemExit(f"SIG label sha mismatch: {sha} != {tsig['sha256_label_vector']}")
    g["sha256_recomputed"] = sha
    g["sha_match"] = True
    ctx = Ctx(rows, B)
    A = {"guard": g, "counts": counts(pool)}
    logger.info(f"[SIG] pool {A['counts']}")

    # (1) criterion (c)
    prim = delta_block(ctx, pool, "c_score_sig", PRIMARY_BAR, "template")
    prim["PASS"] = prim.get("ci_lower_gt_0", False)
    n_both_missing_judge = sum(1 for r in pool if r.get("c_score_sig") is not None and r.get(PRIMARY_BAR) is None)
    prim["n_excluded_judge_missing"] = n_both_missing_judge
    prim["n_excluded_consensus_missing"] = sum(1 for r in pool if r.get("c_score_sig") is None)
    A["primary"] = prim
    logger.info(f"[SIG] PRIMARY delta {prim['delta']:.4f} CI {prim['ci']} PASS={prim['PASS']}")
    sec = {"pooled": delta_block(ctx, pool, "c_score_sig", PRIMARY_BAR, "pooled"),
           "within_sentence": delta_block(ctx, pool, "c_score_sig", PRIMARY_BAR, "sentence"),
           "vs_judge_cheap_orig": delta_block(ctx, pool, "c_score_sig", "judge_cheap_orig", "template"),
           "vs_judge_local_disg": delta_block(ctx, pool, "c_score_sig", "judge_local_disg", "template")}
    for m in ("c_score_hyb", "c_score_align", "c_score_nf", "g_align", "g_nf"):
        sec[f"{m}_vs_{PRIMARY_BAR}"] = delta_block(ctx, pool, m, PRIMARY_BAR, "template")
    sec["c_score_sig_vs_c_score_align"] = delta_block(ctx, pool, "c_score_sig", "c_score_align", "template")
    sec["c_score_sig_vs_c_score_hyb"] = delta_block(ctx, pool, "c_score_sig", "c_score_hyb", "template")
    A["secondary"] = sec
    A["auroc_table"] = {m: {st: auc_block(ctx, pool, m, st) for st in ("template", "pooled", "sentence")} for m in METRICS}

    # (2) nested adds-signal
    A["nested"] = {"cheap_disg_plus_c_sig": nested(ctx, pool, [PRIMARY_BAR], ["c_score_sig"], "logit"),
                   "cheap_disg_plus_c_hyb": nested(ctx, pool, [PRIMARY_BAR], ["c_score_hyb"], "logit"),
                   "c_sig_plus_cheap_disg": nested(ctx, pool, ["c_score_sig"], [PRIMARY_BAR], "logit")}

    # (3) frontier (d)-analogue on the subsample
    sub = [r for r in pool if r.get("judge_frontier_orig") is not None]
    cst = cost_block(rows)
    fr = {"counts": counts(sub)}
    for m in ("c_score_sig", "judge_frontier_orig", "judge_frontier_disg", PRIMARY_BAR, "c_score_hyb"):
        fr[m] = {"pooled": auc_block(ctx, sub, m, "pooled"), "template": auc_block(ctx, sub, m, "template")}
    for comp in ("judge_frontier_orig", "judge_frontier_disg"):
        d = delta_block(ctx, sub, "c_score_sig", comp, "pooled")
        fr[f"c_score_sig_vs_{comp}_pooled"] = d
        if d.get("auroc_comparator"):
            fr[f"auroc_ratio_c_sig_over_{comp}"] = d["auroc_metric"] / d["auroc_comparator"]
    fr["nested_frontier_plus_c_sig"] = nested(ctx, sub, ["judge_frontier_orig"], ["c_score_sig"], "logit")
    fr["cost_ratio_frontier_call_over_consensus_peer_generation"] = cst["frontier_over_consensus_cost_ratio"]
    fr["note"] = "descriptive (n ~ 60 rows after the shared-key cut): CIs are wide"
    A["frontier"] = fr

    # (4) operating points
    A["operating_points"] = {m: op_point(pool, m) for m in METRICS}
    # (5) per template / clause / slot
    A["per_template_labels"] = per_group_table(rows, lambda r: r["template_id"])
    A["per_clause_labels"] = per_group_table(rows, lambda r: r["strata"]["clause_type"])
    A["per_slot_labels"] = per_group_table(rows, lambda r: r["slot"])
    cor = [r for r in rows if r["label"] == "CORRECT"]
    A["matched_reading_by_template"] = {t: dict(Counter(r["matched_reading"] for r in cor if r["template_id"] == t))
                                        for t in sorted({r["template_id"] for r in rows})}
    t8 = [r for r in rows if r["template_id"] == "T8" and r["parse_ok"]]
    A["T8_reading_choice_rate"] = (sum(r["label"] == "READING_CHOICE" for r in t8) / len(t8)) if t8 else None
    A["off_signature_rate_by_slot"] = {s: sum(bool(r["off_signature"]) for r in rows if r["slot"] == s and r["parse_ok"]) /
                                       max(1, sum(1 for r in rows if r["slot"] == s and r["parse_ok"])) for s in FEW}
    A["unparseable_rate_by_slot"] = {s: sum(not r["parse_ok"] for r in rows if r["slot"] == s) /
                                     max(1, sum(1 for r in rows if r["slot"] == s)) for s in FEW}
    A["error_rate_by_slot"] = {s: sum(r["label"] == "ERROR" for r in pool if r["slot"] == s) /
                               max(1, sum(1 for r in pool if r["slot"] == s)) for s in FEW}
    per_t = {}
    for t in sorted({r["template_id"] for r in pool}):
        pt = [r for r in pool if r["template_id"] == t]
        c = counts(pt)
        per_t[t] = {**c, "reportable_30_30": c["n_error"] >= 30 and c["n_correct"] >= 30}
        if per_t[t]["reportable_30_30"]:
            for m in ("c_score_sig", "c_score_hyb", "c_score_align", PRIMARY_BAR, "judge_cheap_orig", "judge_local_disg"):
                per_t[t][m] = auc_block(ctx, pt, m, "pooled")
    A["per_template_auroc"] = per_t
    per_c = {}
    for c_ in sorted({r["strata"]["clause_type"] for r in pool}):
        pc = [r for r in pool if r["strata"]["clause_type"] == c_]
        c = counts(pc)
        per_c[c_] = {**c, "reportable_30_30": c["n_error"] >= 30 and c["n_correct"] >= 30}
        if per_c[c_]["reportable_30_30"]:
            per_c[c_]["delta_c_sig_vs_bar"] = delta_block(ctx, pc, "c_score_sig", PRIMARY_BAR, "template")
    A["per_clause_type_auroc"] = per_c

    # (6) complexity
    cx = {}
    for strat in ("word_tercile", "nconds_bin"):
        d = {}
        for k in sorted({r["strata"][strat] for r in pool}):
            pk = [r for r in pool if r["strata"][strat] == k]
            c = counts(pk)
            d[k] = {**c, "reportable_30_30": c["n_error"] >= 30 and c["n_correct"] >= 30}
            for m in ("c_score_sig", "c_score_hyb", PRIMARY_BAR, "judge_cheap_orig", "judge_local_disg"):
                d[k][m] = auc_block(ctx, pk, m, "template")
            d[k]["delta_c_sig_vs_bar"] = delta_block(ctx, pk, "c_score_sig", PRIMARY_BAR, "template")
        cx[strat] = d
    gm = ["c_score_sig", "c_score_hyb", "c_score_align", PRIMARY_BAR, "judge_cheap_orig"]
    cx["gee_words"] = gee_block(pool, gm, "words")
    cx["gee_nconds"] = gee_block(pool, gm, "nconds_weak")
    cx["gee_depth"] = gee_block(pool, gm, "depth_weak")
    A["complexity"] = cx

    # (7) mechanism inputs
    A["mechanism_sig"] = mechanism(rows, pool, "sig_class_id", "c_score_sig")
    A["mechanism_sig"]["note"] = "M1/M2 GEE tests of e/d belong to the T4 evaluation; values here are descriptive"
    dm = {}
    for mr in ("weak", "strong", "both"):
        co = [r for r in pool if r["label"] == "CORRECT" and r["matched_reading"] == mr and r.get("c_score_sig") is not None]
        dm[mr] = {"n_correct": len(co), "d_correct_divergence": (sum(r["c_score_sig"] >= 0.5 for r in co) / len(co)) if co else None,
                  "share_of_correct": len(co) / max(1, sum(r["label"] == "CORRECT" for r in pool))}
    A["mechanism_sig"]["d_by_matched_reading"] = dm
    rc = [r for r in rows if r["label"] == "READING_CHOICE" and r.get("c_score_sig") is not None]
    A["mechanism_sig"]["reading_choice_rows_T8"] = {"n": len(rc), "share_flagged_c_ge_0.5": (sum(r["c_score_sig"] >= 0.5 for r in rc) / len(rc)) if rc else None}
    # (8) rename invariance
    A["rename_invariance"] = rename_block(rows)
    # (9) coverage view
    cov = [dict(r) for r in rows if r["slot"] in FEW and r["label"] in ("CORRECT", "ERROR", "UNPARSEABLE")]
    for r in cov:
        if r["label"] == "UNPARSEABLE":
            r["label"] = "ERROR"
            for m in METRICS:
                r[m] = 1.0
    A["coverage_view"] = {"counts": counts(cov), "n_unparseable": sum(1 for r in rows if r["label"] == "UNPARSEABLE"),
                          "n_off_signature": sum(1 for r in rows if r["label"] == "OFF_SIGNATURE"),
                          "primary_delta_unparseable_as_error": delta_block(ctx, cov, "c_score_sig", PRIMARY_BAR, "template"),
                          "auroc_template": {m: auc_block(ctx, cov, m, "template", boot=False).get("auroc") for m in METRICS}}
    offs = [r for r in rows if r["label"] == "OFF_SIGNATURE"]
    A["off_signature_rows"] = {"n": len(offs), "by_slot": dict(Counter(r["slot"] for r in offs)),
                               "judge_cheap_disg_mean": float(np.mean([r[PRIMARY_BAR] for r in offs if r.get(PRIMARY_BAR) is not None]))
                               if any(r.get(PRIMARY_BAR) is not None for r in offs) else None,
                               "loose_view_labels": dict(Counter(r["label_loose"] for r in offs))}
    # (10) contamination (templated sentences: a natural negative control)
    con = {}
    for j in ("judge_cheap", "judge_local"):
        d = delta_block(ctx, pool, f"{j}_orig", f"{j}_disg", "template")
        dp = delta_block(ctx, pool, f"{j}_orig", f"{j}_disg", "pooled")
        if not d.get("untestable"):
            d["MDE_2.8SE"] = 2.8 * d["se"] if d.get("se") else None
        con[j] = {"orig_minus_disg_within_template": d, "orig_minus_disg_pooled": dp}
    con["E_reference"] = {"judge_local_qwen8b_orig_minus_disg_pooled_E": -0.06397661554254586,
                          "ci": [-0.09822851070892955, -0.032207955124332124], "source": "iter2 exp5 results/analysis.json i_contamination"}
    A["contamination"] = con
    # (11) placebos
    words_rows = [dict(r, words_score=float(r["strata"]["words"])) for r in pool]
    A["placebos"] = {"composition_words_within_template": auc_block(ctx, words_rows, "words_score", "template"),
                     "composition_words_pooled": auc_block(ctx, words_rows, "words_score", "pooled"),
                     "permutation_primary": permutation_placebo(pool, "c_score_sig", PRIMARY_BAR, 200),
                     **shuffle_placebos(pool, "c_score_sig", PRIMARY_BAR)}
    # (12) cost + system level + error types
    A["cost"] = cst
    A["system_level"] = system_level(pool, METRICS)
    A["error_types"] = error_type_block(ctx, pool, ["c_score_sig", "c_score_hyb", PRIMARY_BAR, "judge_cheap_orig"])
    A["judge_coverage"] = {m: {"n_pool_scored": sum(r.get(m) is not None for r in pool), "n_pool": len(pool)} for m in JUDGES}
    A["disguise_failures"] = sum(1 for r in jl(RES / "disguise_map_SIG.jsonl") if not r.get("text_d") or not r.get("fol_d"))
    return A, rows


# ---------------------------------------------------------------------------------------------------------- FREE
def analyse_free(B: int, sig_rows: list[dict]) -> tuple[dict, list[dict]]:
    t_start = time.time()
    S = sentences()
    tf = json.loads((RES / "testability_FREE.json").read_text())
    cuts = tf["word_terciles"]
    g = guard("FREE", t_start, [RES / "scores_FREE.jsonl", RES / "judge_FREE.jsonl", RES / "judge_local_FREE.jsonl"])
    g["note"] = ("FREE scores were computed label-blind BEFORE the FREE declaration (FREE_PREJOIN; prereg S8 requires the "
                 "declaration before any FREE score is JOINED); this analysis is the first join")
    rows = build_free(S, cuts)
    ok = lambda r: (r["label"] in ("CORRECT", "ERROR") and r["label_tier"] in ("A", "B") and not r.get("ref_flagged"))  # noqa: E731
    pool = [r for r in rows if ok(r)]
    sha = label_sha(pool)
    g["sha256_recomputed"], g["sha_match"] = sha, sha == tf["sha256_label_vector"]
    if not g["sha_match"]:
        raise SystemExit(f"FREE label sha mismatch {sha} != {tf['sha256_label_vector']}")
    ctx = Ctx(rows, B)
    A = {"guard": g, "verdict": tf["verdict"], "counts": counts(pool)}
    views = {"tier_AB": pool, "tier_A": [r for r in pool if r["label_tier"] == "A"],
             "tier_B_only_errors_or_corrects": [r for r in pool if r["label_tier"] == "B"],
             "few_shot_AB": [r for r in pool if r["prompt_variant"] == "fewshot_v1"]}
    fm = [m for m in METRICS if m not in ("c_score_sig", "judge_local_orig") and not m.startswith("judge_frontier")]
    for vn, vp in views.items():
        v = {"counts": counts(vp)}
        for m in ("c_score_align", "c_score_hyb", "c_score_nf", "g_align", "g_nf"):
            v[f"{m}_vs_{PRIMARY_BAR}"] = delta_block(ctx, vp, m, PRIMARY_BAR, "template")
            v[f"{m}_vs_{PRIMARY_BAR}"]["sign_positive"] = (v[f"{m}_vs_{PRIMARY_BAR}"].get("delta") or 0) > 0
        v["auroc_template"] = {m: auc_block(ctx, vp, m, "template") for m in fm}
        v["auroc_pooled"] = {m: auc_block(ctx, vp, m, "pooled") for m in fm}
        A[vn] = v
    A["nested_cheap_disg_plus_c_hyb"] = nested(ctx, pool, [PRIMARY_BAR], ["c_score_hyb"], "logit")
    A["operating_points"] = {m: op_point(pool, m) for m in fm}
    A["per_slot_labels"] = per_group_table(rows, lambda r: f"{r['slot']}|{r['prompt_variant']}")
    A["label_tiers"] = dict(Counter(f"{r['label']}:{r['label_tier']}" for r in rows))
    greedy_classes(rows, False)
    greedy_classes(rows, True)
    A["mechanism_free_align"] = mechanism(rows, pool, "free_align_class_id", "c_score_align")
    A["mechanism_free_hyb"] = mechanism(rows, pool, "free_hyb_class_id", "c_score_hyb")
    A["complexity"] = {"gee_words": gee_block(pool, ["c_score_align", "c_score_hyb", PRIMARY_BAR], "words"),
                       "word_tercile": {k: {m: auc_block(ctx, [r for r in pool if r["strata"]["word_tercile"] == k], m, "template", boot=False).get("auroc")
                                            for m in ("c_score_align", "c_score_hyb", PRIMARY_BAR)} | counts([r for r in pool if r["strata"]["word_tercile"] == k])
                                        for k in ("W1", "W2", "W3")}}
    A["system_level"] = system_level([r for r in pool if r["prompt_variant"] == "fewshot_v1"], fm)
    A["contamination_judge_cheap"] = delta_block(ctx, pool, "judge_cheap_orig", PRIMARY_BAR, "template")
    cov = [dict(r) for r in rows if r["label"] in ("CORRECT", "ERROR", "UNPARSEABLE") and (r["label"] == "UNPARSEABLE" or ok(r))]
    for r in cov:
        if r["label"] == "UNPARSEABLE":
            r["label"] = "ERROR"
            for m in METRICS:
                r[m] = 1.0
    A["coverage_view"] = {"counts": counts(cov), "unparseable_by_slot": dict(Counter(f"{r['slot']}|{r['prompt_variant']}" for r in rows if r["label"] == "UNPARSEABLE")),
                          "c_hyb_vs_bar": delta_block(ctx, cov, "c_score_hyb", PRIMARY_BAR, "template")}
    # SIG vs FREE: vocabulary-divergence cost of consensus (same sentences, same slots)
    sig_pool = [r for r in sig_rows if r["slot"] in FEW and r["label"] in ("CORRECT", "ERROR")]
    fa = lambda rs, m: (sum(r[m] >= 0.5 for r in rs if r["label"] == "CORRECT" and r.get(m) is not None) /  # noqa: E731
                        max(1, sum(1 for r in rs if r["label"] == "CORRECT" and r.get(m) is not None)))
    A["sig_vs_free"] = {m: {"SIG_auroc_template": auc_block(Ctx(sig_rows, 1), sig_pool, m, "template", boot=False).get("auroc"),
                            "FREE_tierA_auroc_template": auc_block(ctx, views["tier_A"], m, "template", boot=False).get("auroc"),
                            "SIG_correct_divergence_d": fa(sig_pool, m) if not m.startswith("judge") else None,
                            "FREE_tierA_correct_divergence_d": fa(views["tier_A"], m) if not m.startswith("judge") else None}
                        for m in ("c_score_align", "c_score_hyb", "c_score_nf", PRIMARY_BAR, "judge_cheap_orig")}
    A["panel_check"] = json.loads((RES / "panel_check.json").read_text()) if (RES / "panel_check.json").exists() else {"not_run": True}
    if isinstance(A["panel_check"], dict):
        A["panel_check"].pop("rows", None)
    return A, rows


# ---------------------------------------------------------------------------------------------------------- tables
def fmt(x, nd=3):
    return "-" if x is None else (f"{x:.{nd}f}" if isinstance(x, float) else str(x))


def fci(d):
    if not d or d.get("untestable"):
        return "untestable"
    ci = d.get("ci") or [None, None]
    a = d.get("auroc", d.get("delta"))
    return f"{fmt(a)} [{fmt(ci[0])}, {fmt(ci[1])}]"


def tables_md(A: dict) -> str:
    L = ["# R_COMP results tables (auto-generated by src/analyse.py)", ""]
    s = A.get("SIG")
    if s:
        p = s["primary"]
        L += ["## SIG: primary test, criterion (c)", "",
              f"Pool: {s['counts']}. Rows where both scores exist: n={p['n']} ({p['n_error']} ERROR / {p['n_correct']} CORRECT, "
              f"{p['n_sentences']} sentences); judge-missing rows excluded: {p['n_excluded_judge_missing']}.", "",
              "| statistic | c_score_sig | judge_cheap_disg | delta [95% CI] | one-sided p | PASS |", "|---|---|---|---|---|---|",
              f"| within-template AUROC | {fmt(p['auroc_metric'])} | {fmt(p['auroc_comparator'])} | {fci(p)} | {fmt(p['p_one_sided'])} | {p['PASS']} |", ""]
        L += ["## SIG: secondary deltas", "", "| comparison | stratum | n | AUROC metric | AUROC comparator | delta [95% CI] | p |", "|---|---|---|---|---|---|---|"]
        for k, d in s["secondary"].items():
            if d.get("untestable"):
                L.append(f"| {k} | - | {d['n']} | untestable | | | |")
                continue
            L.append(f"| {k} | {d['stratum']} | {d['n']} | {fmt(d['auroc_metric'])} | {fmt(d['auroc_comparator'])} | {fci(d)} | {fmt(d['p_one_sided'])} |")
        L += ["", "## SIG: AUROC per metric (within-template / pooled / within-sentence), 95% CI, n", "",
              "| metric | n | within-template | pooled | within-sentence | AUPRC (prevalence) |", "|---|---|---|---|---|---|"]
        for m, d in s["auroc_table"].items():
            L.append(f"| {m} | {d['template'].get('n')} | {fci(d['template'])} | {fci(d['pooled'])} | {fci(d['sentence'])} | "
                     f"{fmt(d['pooled'].get('auprc'))} ({fmt(d['pooled'].get('prevalence'))}) |")
        L += ["", "## SIG: nested adds-signal (5-fold cross-fitted logistic; OOF AUROC delta)", "", "| model | n | within-template delta [CI] | pooled delta [CI] |", "|---|---|---|---|"]
        for k, d in s["nested"].items():
            if d.get("untestable"):
                continue
            L.append(f"| {k} | {d['within_template']['n']} | {fci(d['within_template'])} | {fci(d['pooled'])} |")
        fr = s["frontier"]
        L += ["", f"## SIG: frontier subsample (descriptive), {fr['counts']}", "", "| metric | pooled AUROC [CI] | within-template AUROC |", "|---|---|---|"]
        for m in ("c_score_sig", "judge_frontier_orig", "judge_frontier_disg", PRIMARY_BAR, "c_score_hyb"):
            L.append(f"| {m} | {fci(fr[m]['pooled'])} | {fmt(fr[m]['template'].get('auroc'))} |")
        L.append(f"\nCost ratio (frontier $/call over consensus peer-generation $/candidate): {fmt(fr.get('cost_ratio_frontier_call_over_consensus_peer_generation'), 2)}")
        L += ["", "## SIG: operating points at the frozen thresholds", "", "| metric | n | precision | recall | FA rate | flag rate | AUPRC | prevalence |", "|---|---|---|---|---|---|---|---|"]
        for m, d in s["operating_points"].items():
            if d.get("n"):
                L.append(f"| {m} | {d['n']} | {fmt(d['precision'])} | {fmt(d['recall'])} | {fmt(d['fa_rate'])} | {fmt(d['flag_rate'])} | {fmt(d['auprc'])} | {fmt(d['prevalence'])} |")
        L += ["", "## SIG: complexity (within-template AUROC by stratum)", ""]
        for strat in ("word_tercile", "nconds_bin"):
            L += [f"### {strat}", "", "| stratum | n | ERR/COR | c_score_sig | c_score_hyb | judge_cheap_disg | judge_cheap_orig | delta c_sig - bar [CI] |", "|---|---|---|---|---|---|---|---|"]
            for k, d in s["complexity"][strat].items():
                L.append(f"| {k} | {d['n']} | {d['n_error']}/{d['n_correct']} | {fmt(d['c_score_sig'].get('auroc'))} | {fmt(d['c_score_hyb'].get('auroc'))} | "
                         f"{fmt(d[PRIMARY_BAR].get('auroc'))} | {fmt(d['judge_cheap_orig'].get('auroc'))} | {fci(d['delta_c_sig_vs_bar'])} |")
            L.append("")
        L += ["### GEE: decision correctness ~ z(words), binomial, exchangeable, groups = sentence", "", "| metric | n | accuracy | slope per SD [CI] | p |", "|---|---|---|---|---|"]
        for m, d in s["complexity"]["gee_words"].items():
            if isinstance(d, dict) and "slope_logodds_per_sd" in d:
                L.append(f"| {m} | {d['n']} | {fmt(d['accuracy'])} | {fmt(d['slope_logodds_per_sd'])} [{fmt(d['ci'][0])}, {fmt(d['ci'][1])}] | {fmt(d['p'])} |")
            elif isinstance(d, dict) and "coef" in d:
                L.append(f"| {m} (interaction) | {d['n']} | | {fmt(d['coef'])} [{fmt(d['ci'][0])}, {fmt(d['ci'][1])}] | {fmt(d['p'])} |")
        L += ["", "## SIG: mechanism inputs (descriptive)", "", f"overall: {json.dumps(clean(s['mechanism_sig']['overall']))}",
              f"distinct classes per sentence: {json.dumps(clean(s['mechanism_sig']['distinct_classes_per_sentence']))}", ""]
        L += [f"d by matched reading (CORRECT rows): {json.dumps(clean(s['mechanism_sig']['d_by_matched_reading']))}",
              f"T8 READING_CHOICE rows (converse reading, excluded from the pool): {json.dumps(clean(s['mechanism_sig']['reading_choice_rows_T8']))}", ""]
        L += ["| word tercile | e (ERROR endorsed, c<0.5) | d (CORRECT diverges, c>=0.5) |", "|---|---|---|"]
        for k, d in s["mechanism_sig"]["word_tercile"].items():
            L.append(f"| {k} | {fmt(d['e_error_endorsement'])} (n={d['n_error']}) | {fmt(d['d_correct_divergence'])} (n={d['n_correct']}) |")
        ri = s["rename_invariance"]
        L += ["", "## SIG: rename invariance (FA = renamed CORRECT copies flagged, c >= 0.5)", "", "| metric | unrenamed CORRECT FA | RENAME_NONCE FA | RENAME_SYN FA |", "|---|---|---|---|"]
        for m in ("c_score_sig", "c_score_align", "c_score_nf", "c_score_hyb", "g_align", "g_nf"):
            L.append(f"| {m} | {fmt(ri['reference_unrenamed_correct_fa'].get(m))} | {fmt(ri['RENAME_NONCE'].get(m, {}).get('fa_rate_c_ge_0.5'))} "
                     f"(n={ri['RENAME_NONCE'].get(m, {}).get('n')}) | {fmt(ri['RENAME_SYN'].get(m, {}).get('fa_rate_c_ge_0.5'))} (n={ri['RENAME_SYN'].get(m, {}).get('n')}) |")
        cv = s["coverage_view"]
        L += ["", f"## SIG: coverage view (UNPARSEABLE = ERROR, max suspicion): {cv['counts']}; primary delta {fci(cv['primary_delta_unparseable_as_error'])}", ""]
        c = s["contamination"]
        L += ["## SIG: contamination negative control (orig - disg)", "", "| judge | within-template delta [CI] | MDE (2.8 SE) | pooled delta [CI] |", "|---|---|---|---|"]
        for j in ("judge_cheap", "judge_local"):
            d = c[j]["orig_minus_disg_within_template"]
            L.append(f"| {j} | {fci(d)} | {fmt(d.get('MDE_2.8SE'))} | {fci(c[j]['orig_minus_disg_pooled'])} |")
        pl = s["placebos"]
        L += ["", "## SIG: placebos", "", f"- composition (words) within-template AUROC: {fci(pl['composition_words_within_template'])}; pooled {fci(pl['composition_words_pooled'])}",
              f"- permutation (200 within-sentence label permutations): observed {fmt(pl['permutation_primary']['observed_delta'])}, "
              f"perm 95th pct {fmt(pl['permutation_primary']['perm_p95'])}, exceeds={pl['permutation_primary']['observed_exceeds_p95']}, p={fmt(pl['permutation_primary']['perm_p_one_sided'])}"]
        for k, v in pl.items():
            if k.startswith(("global", "within")):
                L.append(f"- {k}: {fmt(v)}")
        L += ["", "## SIG: labels per slot", "", "| slot | " + " | ".join(["CORRECT", "ERROR", "READING_CHOICE", "OFF_SIGNATURE", "UNPARSEABLE"]) + " | error rate |", "|---|---|---|---|---|---|---|"]
        for sl, d in s["per_slot_labels"].items():
            L.append(f"| {sl} | " + " | ".join(str(d.get(k, 0)) for k in ["CORRECT", "ERROR", "READING_CHOICE", "OFF_SIGNATURE", "UNPARSEABLE"]) + f" | {fmt(s['error_rate_by_slot'].get(sl))} |")
        L += ["", "## SIG: labels per template", "", "| template | CORRECT | ERROR | READING_CHOICE | OFF_SIGNATURE | UNPARSEABLE | matched reading (CORRECT) |", "|---|---|---|---|---|---|---|"]
        for t, d in s["per_template_labels"].items():
            L.append(f"| {t} | " + " | ".join(str(d.get(k, 0)) for k in ["CORRECT", "ERROR", "READING_CHOICE", "OFF_SIGNATURE", "UNPARSEABLE"]) + f" | {s['matched_reading_by_template'].get(t)} |")
        L += ["", "## SIG: error types (repair ops of ERROR classes; within-template AUROC vs all CORRECT / recall at frozen threshold)", "",
              "| op | n ERROR rows | c_score_sig | c_score_hyb | judge_cheap_disg | judge_cheap_orig |", "|---|---|---|---|---|---|"]
        for op, d in s["error_types"].items():
            if op == "op_counts_error_rows":
                continue
            cells = [f"{fmt(d[m]['auroc_within_template_vs_all_correct'])} / {fmt(d[m]['recall_at_frozen_threshold'])}" for m in ("c_score_sig", "c_score_hyb", PRIMARY_BAR, "judge_cheap_orig")]
            L.append(f"| {op} | {d['n_error_rows']} | " + " | ".join(cells) + " |")
        L += ["", "## SIG: system level (10 slots): Spearman of slot error rate vs mean score", ""]
        for m, d in s["system_level"].items():
            if m != "error_rate_by_slot":
                L.append(f"- {m}: spearman {fmt(d['spearman'])}, pearson {fmt(d['pearson'])} (n={d['n_systems']})")
        L += ["", "## Cost", "", "```", json.dumps(clean(s["cost"]), indent=1), "```"]
    f = A.get("FREE")
    if f:
        L += ["", "## FREE (sign readout; tier-B labels provisional if the panel check BA < 0.80)", "", f"verdict {f['verdict']}; label tiers {f['label_tiers']}", "",
              "| view | n (ERR/COR) | c_align - bar [CI] | c_hyb - bar [CI] | c_nf - bar [CI] | AUROC bar (template) |", "|---|---|---|---|---|---|"]
        for vn in ("tier_AB", "tier_A", "tier_B_only_errors_or_corrects", "few_shot_AB"):
            v = f[vn]
            L.append(f"| {vn} | {v['counts']['n']} ({v['counts']['n_error']}/{v['counts']['n_correct']}) | {fci(v['c_score_align_vs_' + PRIMARY_BAR])} | "
                     f"{fci(v['c_score_hyb_vs_' + PRIMARY_BAR])} | {fci(v['c_score_nf_vs_' + PRIMARY_BAR])} | {fmt(v['auroc_template'][PRIMARY_BAR].get('auroc'))} |")
        L += ["", "### SIG vs FREE (vocabulary-divergence cost of consensus)", "", "| metric | SIG AUROC | FREE tier-A AUROC | SIG d | FREE tier-A d |", "|---|---|---|---|---|"]
        for m, d in f["sig_vs_free"].items():
            L.append(f"| {m} | {fmt(d['SIG_auroc_template'])} | {fmt(d['FREE_tierA_auroc_template'])} | {fmt(d['SIG_correct_divergence_d'])} | {fmt(d['FREE_tierA_correct_divergence_d'])} |")
        pc = f.get("panel_check", {})
        L += ["", f"Panel known-label check: {json.dumps(clean({k: pc.get(k) for k in ('n_items', 'n_answered', 'balanced_accuracy', 'recall_error', 'recall_correct', 'tier_B_provisional', 'not_run')}))}"]
    return "\n".join(L) + "\n"


def write_candidates(rows: list[dict]) -> None:
    keep = ["row_key", "item_id", "sentence_id", "condition", "template_id", "slot", "system", "family", "prompt_variant",
            "candidate_fol", "parse_ok", "label", "label_source", "label_tier", "matched_reading", "off_signature", "sig_status",
            "repair_ops", "repair_status", "strata", "sig_class_id", "sig_class_id_size", "sig_class_id_n_peers",
            "sig_class_id_n_peers_same_class", "sig_class_id_peer_majority_class", "sig_class_id_is_peer_majority",
            "free_solver_class_id", "free_align_class_id", "free_hyb_class_id", "free_align_class_id_size",
            "free_align_class_id_is_peer_majority", "free_hyb_class_id_size", "free_hyb_class_id_is_peer_majority",
            "n_peers_sig", "n_peers_equal_sig", "n_unknown_sig", "n_peers_hyb", "correct_not_equivalent", "ref_flagged",
            "tier_B_provisional", "panel_votes", "cost_usd", "secs_sig", "coverage_status"] + METRICS
    with (RES / "rcomp_candidates.jsonl").open("w") as fh:
        for r in rows:
            fh.write(json.dumps(clean({k: r.get(k) for k in keep}), ensure_ascii=False) + "\n")


@logger.catch(reraise=True)
def main() -> None:
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(ROOT / "logs" / "analyse.log", rotation="30 MB", level="DEBUG")
    ap = argparse.ArgumentParser()
    ap.add_argument("--B", type=int, default=2000)
    ap.add_argument("--no-free", action="store_true")
    a = ap.parse_args()
    t0 = time.time()
    A = {"generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "B": a.B, "seed": SEED,
         "orientation": "every metric higher = more likely ERROR"}
    A["SIG"], sig_rows = analyse_sig(a.B)
    all_rows = list(sig_rows)
    with (RES / "analysis_rows_SIG.jsonl").open("w") as fh:
        for r in sig_rows:
            fh.write(json.dumps(clean({k: r.get(k) for k in ["row_key", "sentence_id", "template_id", "slot", "label"] + METRICS}), ensure_ascii=False) + "\n")
    if not a.no_free and (RES / "testability_FREE.json").exists():
        A["FREE"], free_rows = analyse_free(a.B, sig_rows)
        all_rows += free_rows
    else:
        A["FREE"] = None
    write_candidates(all_rows)
    A["runtime_s"] = time.time() - t0
    (RES / "analysis.json").write_text(json.dumps(clean(A), indent=1))
    (RES / "tables.md").write_text(tables_md(clean(A)))
    logger.info(f"analysis written in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
