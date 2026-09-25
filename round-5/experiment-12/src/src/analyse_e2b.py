#!/usr/bin/env python3
"""E2-B Steps 4-5: label join (only after BOTH seals verify) and every pre-registered E2-B analysis.

Statistics core = exp 6 src/api_bar.py (copied byte-identical to exp6src/, sha recorded): Mann-Whitney AUROC with ties
= 1/2, stratified AUROC, sentence-cluster bootstrap (B = 2000, seed 0, identical resamples for every metric = paired
deltas), IPW AUROC; S4 stack = exp 6 src/s4.fit_s4_oof (cross-fitted L2 logistic, missing indicators, FAIL -> worst).
Orientation everywhere: HIGHER score = MORE LIKELY ERROR.

Outputs: analysis/per_item_E2B.jsonl, analysis/analysis_E2B.json, analysis/confirm_verdict_E2B.json,
e2b/E2B_FINAL_READY.json (marker M3 for E2-B).  Usage: analyse_e2b.py [--B 2000] [--placebo-n 300]"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import subprocess
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

WS = Path(__file__).resolve().parents[1]
E2S = WS / "e2bsrc"
SC, AN, E2B = WS / "scores", WS / "analysis", WS / "e2b"
AN.mkdir(exist_ok=True)
sys.path.insert(0, str(WS / "exp6src"))
from src import api_bar as AB  # noqa: E402
from src.s4 import fit_s4_oof  # noqa: E402

from loguru import logger  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(WS / "logs" / "analyse_e2b.log", rotation="30 MB", level="DEBUG")

PRIMARY = "V0"
COMPARATORS = ["flashlite_disg", "flashlite_orig", "nano_orig", "nano_disg", "costmatched_disg", "costmatched_orig"]
METRICS = ["V0", "p_peer_text", "c_exact", "V1", "V2", "V3", "V4", "V5", "flashlite_disg", "flashlite_orig", "nano_orig", "nano_disg",
           "costmatched_disg", "costmatched_orig", "frontier_orig", "S4_E2B", "S4_E2B_plus_V0", "l2_bow", "l3_z3", "pilot_joint_conflict"]
S4_FEATS = ["parse_fail", "pilot_joint_conflict", "pilot_arity_incons", "l2_bow", "l3_z3", "flashlite_disg", "flashlite_orig", "nano_orig", "nano_disg"]
S4_SUBSTITUTED = {
    "judge_local_qwen8b_disg/orig, judge_local_llama8b_disg/orig": "dropped: no GPU on this machine (4 CPUs, no CUDA); exp-6 rule",
    "rt_nli_* / rt_embed_cos (API and local round trip)": "dropped: NLI/embedding models need a GPU; no local counterpart available",
    "sc5_* (API and local self-consistency)": "dropped: needs 5 extra samples per sentence + a local model; not in the E2-B budget",
    "pilot_dangling / pilot_rerun_jacc / pilot_undeclared": "not applicable: a MALLS sentence has no story/document; E2 has no zero-shot rerun",
    "nano_disg": "ADDED (cheap API judge, disguised view) so the stack holds both views of both cheap judges"}
OWN_FAMILY = {"flashlite_disg": "G8", "flashlite_orig": "G8", "frontier_orig": "G8", "nano_orig": "G7", "nano_disg": "G7",
              "costmatched_disg": "G4", "costmatched_orig": "G4"}


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def fold_e2(sid: str) -> int:
    return int(hashlib.sha1(("E2_folds_v1|" + sid).encode()).hexdigest(), 16) % 5


def fnum(x):
    return None if x is None or (isinstance(x, float) and math.isnan(x)) else float(x)


def wilson(k: int, n: int, z: float = 1.96) -> list:
    if n == 0:
        return [None, None]
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return [c - h, c + h]


# ================================================================================================= join
def verify_seals() -> dict:
    r1 = subprocess.run([str(E2S / ".venv/bin/python"), str(E2S / "src_e2/verify_seal.py")], capture_output=True, text=True, cwd=str(E2S))
    r2 = subprocess.run([sys.executable, str(WS / "src/seal_scores.py"), "verify"], capture_output=True, text=True)
    out = {"label_seal_verify": r1.stdout.strip().splitlines()[-1] if r1.stdout.strip() else r1.stderr[-300:], "label_seal_rc": r1.returncode,
           "score_seal_verify": r2.stdout.strip().splitlines()[-1] if r2.stdout.strip() else r2.stderr[-300:], "score_seal_rc": r2.returncode}
    if r1.returncode != 0 or r2.returncode != 0:
        raise SystemExit(f"REFUSED: seal verification failed {out}")
    return out


def join() -> list[dict]:
    labels = {r["row_key"]: r for r in jl(E2S / "sealed" / "labels_E2.jsonl")}
    nol = jl(E2S / "candidates_E2_nolabels.jsonl")
    scores = {r["row_key"]: r for r in jl(SC / "scores_E2B.jsonl")}
    sel = json.loads((WS / "freeze_copy" / "selection.json").read_text())
    coefs = sel["V4_coefficients_frozen"]
    sents = {s["sentence_id"]: s for s in json.loads((E2B / "sentences_E2B.json").read_text())}
    dec = json.loads((E2B / "drift_decision.json").read_text())
    regime = "PASS" if str(dec.get("decision")).upper() == "PASS" else "DRIFTED"
    rows = []
    for n in nol:
        k = f"{n['sentence_id']}|{n['slot']}"
        s = scores.get(k)
        lab = labels.get(n["row_key"])
        if s is None or lab is None:
            logger.warning(f"join: missing {'scores' if s is None else 'label'} for {k}")
            continue
        st = sents[n["sentence_id"]]
        r = {"row_key": k, "e2_row_key": n["row_key"], "sentence_id": n["sentence_id"], "sample": "E2B", "stratum": "L25_E2B",
             "word_bin": st["word_bin"], "words": st["words"], "n_conditions": st["n_conditions"], "n_quant": st["n_quant"], "depth": st["depth"],
             "e2b_batch": st["e2b_batch"], "e2b_origin": st["e2b_origin"], "slot": n["slot"], "system": n["system"], "family_field": n["family"],
             "family": s["family_vendor"], "fold_E2": fold_e2(n["sentence_id"]), "label": lab["label"], "tier": lab["label_tier"],
             "reading_choice": bool(lab["reading_choice"]), "contested": lab["label"] == "CONTESTED", "auto_label": lab["auto_label"],
             "error_ops": lab["error_ops"], "correct_not_equivalent": lab["correct_not_equivalent"], "reference_status": lab["reference_status"],
             "vex": lab.get("vex"), "label_regime": regime, "coverage_status": s["coverage_status"], "parse_ok": s["parse_ok"]}
        for c in ("V0", "p_peer_text", "p_text", "c_exact", "V1", "V2", "V3", "V5", "V0_matrix", "l2_bow", "l3_z3", "parse_fail",
                  "pilot_joint_conflict", "pilot_arity_incons", "pilot_shape_incons", "n_peers_used", "g_score",
                  "flashlite_disg", "flashlite_orig", "nano_orig", "nano_disg", "costmatched_disg", "costmatched_orig", "frontier_orig",
                  "in_frontier_subsample", "frontier_inclusion_prob", "secs_align_sentence", "gen_cost_usd",
                  "flashlite_disg_cost", "flashlite_orig_cost", "nano_orig_cost", "nano_disg_cost", "costmatched_disg_cost",
                  "costmatched_orig_cost", "frontier_orig_cost", "flashlite_disg_seconds", "costmatched_disg_seconds", "frontier_orig_seconds",
                  "flashlite_disg_status", "flashlite_orig_status", "nano_orig_status", "costmatched_disg_status", "costmatched_orig_status",
                  "frontier_orig_status", "flashlite_disg_vfb", "flashlite_orig_vfb", "costmatched_disg_vfb", "costmatched_orig_vfb",
                  "frontier_orig_vfb", "nano_orig_status", "nano_disg_status"):
            r[c] = s.get(c)
        if s["coverage_status"] == "UNPARSEABLE":
            r["V4"] = 1.0
        elif r["c_exact"] is not None and r["V0"] is not None:
            z = coefs["intercept"] + coefs["c_exact"] * r["c_exact"] + coefs["c_align"] * r["V0"]
            r["V4"] = 1 / (1 + math.exp(-z))
        else:
            r["V4"] = None
        r["y_AB"] = 1 if r["label"] == "ERROR" else (0 if r["label"] == "CORRECT" else None)
        r["in_R_AB"] = r["label"] in ("CORRECT", "ERROR") and r["tier"] in ("A", "B") and not r["reading_choice"]
        r["in_R_A"] = r["label"] in ("CORRECT", "ERROR") and r["tier"] == "A" and not r["reading_choice"]
        r["in_R_AB_cont"] = r["label"] in ("CORRECT", "ERROR", "CONTESTED") and r["tier"] in ("A", "B") and not r["reading_choice"]
        # E2's pre-registered no-panel regime (testability_E2 'R_A_UNAUDITED'; drift stop rule 'tier-A-only confirmation'):
        # solver labels against the UNAUDITED MALLS gold, every non-equivalent auto class UNRESOLVED
        r["in_R_AU"] = r["label"] in ("CORRECT", "ERROR") and r["tier"] == "A_unaudited_ref" and not r["reading_choice"]
        rows.append(r)
    if rows and not any(r["tier"] in ("A", "B") for r in rows):
        # the drift decision (M2) passed, but no batch completed the panel: the labels are E's final rule WITHOUT votes
        for r in rows:
            r["label_regime"] = "NO_PANEL_TIER_A_UNAUDITED"
    return rows


def add_s4(rows: list[dict]) -> dict:
    """S4_E2B and S4_E2B + V0, cross-fitted over E2-B sentence folds (E2_folds_v1), trained on R_AB labels only."""
    lab = {r["row_key"]: r["y_AB"] for r in rows if r["in_POP"]}
    folds = {r["row_key"]: r["fold_E2"] for r in rows}
    tab = []
    for r in rows:
        t = {"row_key": r["row_key"]}
        for f in S4_FEATS + ["V0"]:
            v = r.get(f)
            st = r.get(f + "_status")
            t[f] = None if v is None else float(v)
            t[f + "__status"] = "fail" if (st and str(st).startswith("fail")) else ("ok" if v is not None else "na")
        tab.append(t)
    ff = {f: 1.0 for f in S4_FEATS + ["V0"]}
    ff.update({"pilot_arity_incons": max([r.get("pilot_arity_incons") or 0 for r in rows] + [1])})
    info = {}
    for nm, feats in (("S4_E2B", S4_FEATS), ("S4_E2B_plus_V0", S4_FEATS + ["V0"])):
        oof, inf = fit_s4_oof(tab, lab, folds, feats, C=1.0, fail_fill=ff)
        for r in rows:
            r[nm] = oof.get(r["row_key"])
        info[nm] = {"features_used": inf["features_used"], "feature_names": inf["feature_names"], "n_train_per_fold": inf["n_train_per_fold"],
                    "mean_coef": {k: float(np.mean([c["coef"].get(k, 0.0) for c in inf["coefs"]])) for k in inf["feature_names"]}}
    info["substituted"] = S4_SUBSTITUTED
    return info


def testable(rows: list[dict], flag: str) -> dict:
    R = [r for r in rows if r[flag]]
    ce = [r for r in R if r["label"] == "ERROR"]
    cc = [r for r in R if r["label"] == "CORRECT"]
    se, sc = {r["sentence_id"] for r in ce}, {r["sentence_id"] for r in cc}
    return {"ERROR_rows": len(ce), "CORRECT_rows": len(cc), "ERROR_sentences": len(se), "CORRECT_sentences": len(sc),
            "sentences_with_both": len(se & sc), "testable": len(ce) >= 50 and len(cc) >= 50 and len(se) >= 25 and len(sc) >= 25}


def choose_population(rows: list[dict]) -> dict:
    """PRIMARY = R_AB (panel regime). If R_AB is not testable (E's rule) the analysis population falls back to E2's
    pre-registered no-panel regime R_A_UNAUDITED, and every number is SECONDARY (label = solver vs UNAUDITED MALLS gold)."""
    t_ab, t_au = testable(rows, "in_R_AB"), testable(rows, "in_R_AU")
    if t_ab["testable"]:
        return {"population": "R_AB", "status": "PRIMARY", "R_AB": t_ab, "R_A_UNAUDITED": t_au}
    return {"population": "R_A_UNAUDITED", "status": ("SECONDARY: R_AB not testable (no panel regime); E2's pre-registered no-panel regime "
                                                      "'tier-A-only' (solver vs UNAUDITED MALLS gold; E's panel judged most MALLS gold wrong, so ERROR "
                                                      "means 'not equivalent to the gold' and CORRECT means 'z3-equivalent to the gold')"),
            "testable": t_au["testable"], "R_AB": t_ab, "R_A_UNAUDITED": t_au}


# ================================================================================================= stats helpers
class Cell:
    def __init__(self, rows: list[dict], name: str, B: int, ycol: str = "y_AB"):
        self.rows, self.name = rows, name
        self.y = np.array([r[ycol] for r in rows], int)
        self.cl = [r["sentence_id"] for r in rows]
        self.h = np.array([r["word_bin"] for r in rows])
        self.B = B
        self._cb = {}

    def vec(self, m: str) -> np.ndarray:
        return np.array([np.nan if r.get(m) is None else float(r[m]) for r in self.rows], float)

    def cb(self, mask: np.ndarray):
        k = hashlib.sha1(mask.tobytes()).hexdigest()
        if k not in self._cb:
            self._cb[k] = AB.ClusterBoot([c for c, m in zip(self.cl, mask) if m], b=self.B, seed=0)
        return self._cb[k]

    def counts(self, mask) -> dict:
        y = self.y[mask]
        sid = np.array(self.cl)[mask]
        both = len(set(sid[y == 1]) & set(sid[y == 0]))
        return {"n": int(mask.sum()), "n_error": int(y.sum()), "n_correct": int(len(y) - y.sum()), "n_sentences": len(set(sid)),
                "sentences_with_both_classes": both}

    def metric(self, m: str) -> dict:
        s = self.vec(m)
        mask = ~np.isnan(s)
        if mask.sum() < 10 or len(set(self.y[mask])) < 2:
            return {"n": int(mask.sum()), "auroc": None}
        cb = self.cb(mask)
        y, ss, h = self.y[mask], s[mask], self.h[mask]
        st = AB.boot_stat(y, ss, cb, "strat", h)
        po = AB.boot_stat(y, ss, cb, "pooled")
        from sklearn.metrics import average_precision_score
        return {"strat_auroc": st["auroc"], "strat_ci": st["ci"], "pooled_auroc": po["auroc"], "pooled_ci": po["ci"],
                "auprc": float(average_precision_score(y, ss)), "error_base_rate": float(y.mean()), "tie_rate": AB.tie_rate(y, ss),
                "coverage_in_cell": float(mask.mean()), **self.counts(mask)}

    def delta(self, a: str, b: str, extra_mask: np.ndarray | None = None) -> dict:
        sa, sb = self.vec(a), self.vec(b)
        mask = ~np.isnan(sa) & ~np.isnan(sb)
        if extra_mask is not None:
            mask &= extra_mask
        if mask.sum() < 10 or len(set(self.y[mask])) < 2:
            return {"n": int(mask.sum()), "delta": None}
        cb = self.cb(mask)
        d = AB.paired_boot(self.y[mask], sa[mask], sb[mask], cb, "strat", self.h[mask])
        dp = AB.paired_boot(self.y[mask], sa[mask], sb[mask], cb, "pooled")
        return {"a": a, "b": b, "strat_a": d["a"], "strat_b": d["b"], "strat_delta": d["delta"], "strat_ci": d["ci"], "strat_se": d["se"],
                "p_one_sided_le0": d["p_one_sided_le0"], "pooled_delta": dp["delta"], "pooled_ci": dp["ci"],
                "ci_gt_0": bool(d["ci"][0] is not None and d["ci"][0] > 0), **self.counts(mask)}


# ================================================================================================= analyses
def frontier_block(rows: list[dict], B: int) -> dict:
    from sklearn.linear_model import LogisticRegression
    sub = [r for r in rows if r["in_POP"] and r.get("in_frontier_subsample") and r.get("frontier_orig") is not None and r.get("V0") is not None]
    out = {"n_subsample_rows_scored": sum(1 for r in rows if r.get("in_frontier_subsample") and r.get("frontier_orig") is not None),
           "n_in_R_AB_complete": len(sub)}
    if len(sub) < 20 or len({r["y_AB"] for r in sub}) < 2:
        out["status"] = "NOT_TESTABLE"
        return out
    y = np.array([r["y_AB"] for r in sub])
    w = np.array([1.0 / r["frontier_inclusion_prob"] for r in sub])
    fr = np.array([r["frontier_orig"] for r in sub])
    v0 = np.array([r["V0"] for r in sub])
    s4 = np.array([np.nan if r.get("S4_E2B") is None else r["S4_E2B"] for r in sub])
    fl = np.array([np.nan if r.get("flashlite_disg") is None else r["flashlite_disg"] for r in sub])
    cm = np.array([np.nan if r.get("costmatched_disg") is None else r["costmatched_disg"] for r in sub])
    # nested [frontier + V0] - frontier, cross-fitted over sentence folds within the subsample
    X1, X2 = fr[:, None], np.column_stack([fr, v0])
    fo = np.array([r["fold_E2"] for r in sub])
    o1, o2 = np.full(len(sub), np.nan), np.full(len(sub), np.nan)
    for k in range(5):
        tr, te = fo != k, fo == k
        if te.sum() == 0 or len(set(y[tr])) < 2:
            continue
        for X, o in ((X1, o1), (X2, o2)):
            mu, sd = X[tr].mean(0), X[tr].std(0) + 1e-12
            m = LogisticRegression(C=1.0, max_iter=2000).fit((X[tr] - mu) / sd, y[tr], sample_weight=w[tr])
            o[te] = m.predict_proba((X[te] - mu) / sd)[:, 1]
    cb = AB.ClusterBoot([r["sentence_id"] for r in sub], b=B, seed=0)

    def ipw_ci(s):
        ok = ~np.isnan(s)
        pt = AB.ipw_auroc(y[ok], s[ok], w[ok])
        bs = []
        for ix in cb.idx:
            ix2 = ix[ok[ix]]
            bs.append(AB.ipw_auroc(y[ix2], s[ix2], w[ix2]))
        return pt, AB.boot_ci(bs), np.array(bs)
    res = {}
    for nm, s in (("frontier_orig", fr), ("V0", v0), ("S4_E2B", s4), ("flashlite_disg", fl), ("costmatched_disg", cm),
                  ("nested_frontier", o1), ("nested_frontier_plus_V0", o2)):
        pt, ci, bs = ipw_ci(s)
        res[nm] = {"ipw_auroc": pt, "ci": ci}
        res[nm]["_bs"] = bs
    ratio = res["V0"]["ipw_auroc"] / res["frontier_orig"]["ipw_auroc"]
    rb = res["V0"]["_bs"] / res["frontier_orig"]["_bs"]
    nd = res["nested_frontier_plus_V0"]["_bs"] - res["nested_frontier"]["_bs"]
    dv = res["V0"]["_bs"] - res["frontier_orig"]["_bs"]
    for v in res.values():
        v.pop("_bs")
    out.update({"status": "OK", "ipw": res, "ratio_V0_over_frontier": {"ratio": ratio, "ci": AB.boot_ci(rb[np.isfinite(rb)])},
                "delta_V0_minus_frontier": {"delta": res["V0"]["ipw_auroc"] - res["frontier_orig"]["ipw_auroc"], "ci": AB.boot_ci(dv)},
                "nested_frontier_plus_V0_minus_frontier": {"delta": res["nested_frontier_plus_V0"]["ipw_auroc"] - res["nested_frontier"]["ipw_auroc"],
                                                           "ci": AB.boot_ci(nd)},
                "n_error": int(y.sum()), "n_correct": int(len(y) - y.sum()), "n_sentences": len({r["sentence_id"] for r in sub}),
                "note": "IPW = 1/inclusion probability of the words-tercile x family cell; nested fits are cross-fitted (5 sentence folds) and weighted"})
    return out


def hmech(rows: list[dict], B: int) -> dict:
    import importlib.util
    spec = importlib.util.spec_from_file_location("cv", WS / "freeze_copy" / "consensus_variants.py")
    cv = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cv)
    idx = {r["sentence_id"]: cv.build_index(r) for r in jl(SC / "pairwise_classes_E2B.jsonl")}
    lab = {r["row_key"]: r for r in rows if r["in_POP"]}
    rng_sids = sorted({r["sentence_id"] for r in lab.values()})
    out = {}
    # (i) share of NON-agreeing peers (of a CORRECT candidate) whose own label is ERROR
    per_sent = defaultdict(lambda: [0, 0])
    for k, r in lab.items():
        if r["y_AB"] != 0 or r["sentence_id"] not in idx:
            continue
        ix = idx[r["sentence_id"]]
        if k not in ix["node_of"]:
            continue
        c = ix["node_of"][k]
        for p in cv.peers_lofo(ix, k):
            if cv.agree(ix, c, ix["node_of"][p]) or p not in lab:
                continue
            per_sent[r["sentence_id"]][0] += lab[p]["y_AB"]
            per_sent[r["sentence_id"]][1] += 1
    out["i_share_nonagreeing_peers_ERROR"] = _ratio_boot(per_sent, B, threshold=0.50, name="share")
    # (ii) SCATTER: SI_cor / SI_err over cross-family pairs of labelled rows, per sentence, same-sentence ratio of means
    si = {}
    for sid, ix in idx.items():
        rs = [(k, ix["node_of"][k], lab[k]["family"], lab[k]["y_AB"]) for k in lab if lab[k]["sentence_id"] == sid and k in ix["node_of"]]
        ee, cc = [], []
        for i in range(len(rs)):
            for j in range(i + 1, len(rs)):
                a, b = rs[i], rs[j]
                if a[2] == b[2]:
                    continue
                e = int(cv.agree(ix, a[1], b[1]))
                if a[3] + b[3] == 2:
                    ee.append(e)
                elif a[3] + b[3] == 0:
                    cc.append(e)
        if ee and cc:
            si[sid] = (np.mean(cc), np.mean(ee))
    if si:
        ks = sorted(si)
        C = np.array([si[k][0] for k in ks])
        E = np.array([si[k][1] for k in ks])
        rng = np.random.default_rng(0)
        rb = []
        for _ in range(B):
            ix_ = rng.integers(0, len(ks), len(ks))
            e_ = E[ix_].mean()
            rb.append(C[ix_].mean() / e_ if e_ > 0 else np.inf)
        rb = np.array(rb)
        ratio = C.mean() / E.mean() if E.mean() > 0 else float("inf")
        out["ii_scatter_ratio_SI_cor_over_SI_err"] = {"SI_cor": float(C.mean()), "SI_err": float(E.mean()), "ratio": float(ratio),
                                                       "ci": AB.boot_ci(rb[np.isfinite(rb)]), "n_sentences": len(ks), "threshold": 2.0,
                                                       "verdict": "CONFIRMED" if ratio >= 2 else "REFUTED"}
    else:
        out["ii_scatter_ratio_SI_cor_over_SI_err"] = {"verdict": "NOT_TESTABLE", "n_sentences": 0}
    # (iii) NET: Delta(e+d) top vs bottom words tercile, endorsement = V0 <= 0.5
    R = [r for r in lab.values() if r.get("V0") is not None]
    sent_words = {r["sentence_id"]: r["words"] for r in R}
    cuts = [float(x) for x in np.quantile(list(sent_words.values()), [1 / 3, 2 / 3])]

    def terc(w):
        return "T1" if w <= cuts[0] else ("T2" if w <= cuts[1] else "T3")

    def ed(rs):
        err = [r for r in rs if r["y_AB"] == 1]
        cor = [r for r in rs if r["y_AB"] == 0]
        e = np.mean([r["V0"] <= 0.5 for r in err]) if err else np.nan
        d = np.mean([r["V0"] > 0.5 for r in cor]) if cor else np.nan
        return e, d, len(err), len(cor)
    by_s = defaultdict(list)
    for r in R:
        by_s[r["sentence_id"]].append(r)
    sids = sorted(by_s)
    lo = [r for r in R if terc(r["words"]) == "T1"]
    hi = [r for r in R if terc(r["words"]) == "T3"]
    e1, d1, ne1, nc1 = ed(lo)
    e3, d3, ne3, nc3 = ed(hi)
    rng = np.random.default_rng(0)
    bs = []
    for _ in range(B):
        pick = [sids[i] for i in rng.integers(0, len(sids), len(sids))]
        rr = [r for s in pick for r in by_s[s]]
        a1 = ed([r for r in rr if terc(r["words"]) == "T1"])
        a3 = ed([r for r in rr if terc(r["words"]) == "T3"])
        bs.append((a3[0] + a3[1]) - (a1[0] + a1[1]))
    bs = np.array([b for b in bs if not np.isnan(b)])
    dnet = (e3 + d3) - (e1 + d1)
    out["iii_NET_delta_e_plus_d_words_T3_minus_T1"] = {"delta": float(dnet), "ci": AB.boot_ci(bs), "e_T1": float(e1), "d_T1": float(d1),
                                                        "e_T3": float(e3), "d_T3": float(d3), "n_err_T1": ne1, "n_cor_T1": nc1, "n_err_T3": ne3,
                                                        "n_cor_T3": nc3, "tercile_cuts_words": cuts,
                                                        "range_restriction_flag": f"E2-B words range {min(r['words'] for r in R)}-{max(r['words'] for r in R)}: narrow terciles",
                                                        "verdict": "CONFIRMED" if dnet > 0 else "REFUTED"}
    # (iv) exact vs ALIGN e/d per class
    Rx = [r for r in R if r.get("c_exact") is not None]

    def cls(r):
        ops = set(r.get("error_ops") or [])
        return {"MEANING_RENAME": "MEANING_RENAME" in ops, "ADD_DROP": bool(ops & {"ADD", "DROP"})}
    res4 = {}
    cor = [r for r in Rx if r["y_AB"] == 0]
    res4["d_ALIGN"] = float(np.mean([r["V0"] > 0.5 for r in cor])) if cor else None
    res4["d_exact"] = float(np.mean([r["c_exact"] > 0.5 for r in cor])) if cor else None
    res4["n_correct"] = len(cor)
    ok = [res4["d_ALIGN"] is not None and res4["d_ALIGN"] < res4["d_exact"]]
    for c in ("MEANING_RENAME", "ADD_DROP"):
        err = [r for r in Rx if r["y_AB"] == 1 and cls(r)[c]]
        ea = float(np.mean([r["V0"] <= 0.5 for r in err])) if err else None
        ex = float(np.mean([r["c_exact"] <= 0.5 for r in err])) if err else None
        res4[f"e_ALIGN_{c}"], res4[f"e_exact_{c}"], res4[f"n_error_{c}"] = ea, ex, len(err)
        ok.append(ea is not None and ea > ex)
    # bootstrap CIs of the three differences
    by_s2 = defaultdict(list)
    for r in Rx:
        by_s2[r["sentence_id"]].append(r)
    s2 = sorted(by_s2)
    rng = np.random.default_rng(1)
    diffs = defaultdict(list)
    for _ in range(min(B, 1000)):
        rr = [r for i in rng.integers(0, len(s2), len(s2)) for r in by_s2[s2[i]]]
        cr = [r for r in rr if r["y_AB"] == 0]
        if cr:
            diffs["d_exact_minus_d_ALIGN"].append(np.mean([r["c_exact"] > 0.5 for r in cr]) - np.mean([r["V0"] > 0.5 for r in cr]))
        for c in ("MEANING_RENAME", "ADD_DROP"):
            er = [r for r in rr if r["y_AB"] == 1 and cls(r)[c]]
            if er:
                diffs[f"e_ALIGN_minus_e_exact_{c}"].append(np.mean([r["V0"] <= 0.5 for r in er]) - np.mean([r["c_exact"] <= 0.5 for r in er]))
    res4["ci"] = {k: AB.boot_ci(v) for k, v in diffs.items()}
    res4["prediction"] = "ALIGN d lower than exact's; ALIGN e higher than exact's on MEANING_RENAME-type and on ADD/DROP errors"
    comp = {"d_lower": ok[0], "e_higher_MEANING_RENAME": ok[1] if res4["n_error_MEANING_RENAME"] else None,
            "e_higher_ADD_DROP": ok[2] if res4["n_error_ADD_DROP"] else None}
    tested = [v for v in comp.values() if v is not None]
    res4["verdict"] = ("CONFIRMED" if all(tested) and len(tested) == 3 else
                       ("PARTIAL: tested components hold, MEANING_RENAME component NOT_TESTABLE (no MEANING_RENAME labels without the panel)"
                        if all(tested) else "REFUTED"))
    res4["components_hold"] = comp
    out["iv_exact_vs_ALIGN_e_d"] = res4
    if any(r.get("tier") == "A_unaudited_ref" for r in lab.values()):
        note = ("UNINFORMATIVE in the no-panel regime: CORRECT = z3-equivalent to the (unaudited) gold, so two CORRECT rows are "
                "always mutually equivalent and a CORRECT candidate can only disagree with non-CORRECT peers (tautological)")
        for k in ("i_share_nonagreeing_peers_ERROR", "ii_scatter_ratio_SI_cor_over_SI_err"):
            if isinstance(out.get(k), dict):
                out[k]["verdict_as_computed"] = out[k].get("verdict")
                out[k]["verdict"] = "UNINFORMATIVE (tautological under gold-equivalence labels)"
                out[k]["regime_note"] = note
    out["definitions"] = {"endorsement": "peers endorse a candidate iff its score <= 0.5; e = P(endorsed | ERROR), d = P(flagged | CORRECT) (exp 9 analyse.py)",
                          "pairs": "cross-family = different vendor family; agreement = eqmv (eval-2 pairwise matrix, UNKNOWN = not agreeing)",
                          "population": "L25_E2B analysis-population rows (in_POP: R_AB if testable, else R_A_UNAUDITED)"}
    return out


def _ratio_boot(per_sent: dict, B: int, threshold: float, name: str) -> dict:
    ks = sorted(per_sent)
    if not ks:
        return {"verdict": "NOT_TESTABLE", "n_pairs": 0}
    num = np.array([per_sent[k][0] for k in ks], float)
    den = np.array([per_sent[k][1] for k in ks], float)
    pt = num.sum() / den.sum()
    rng = np.random.default_rng(0)
    bs = []
    for _ in range(B):
        ix = rng.integers(0, len(ks), len(ks))
        bs.append(num[ix].sum() / max(1.0, den[ix].sum()))
    ci = AB.boot_ci(bs)
    return {name: float(pt), "ci": ci, "n_pairs": int(den.sum()), "n_sentences": len(ks), "threshold": threshold,
            "verdict": "CONFIRMED" if pt >= threshold else "REFUTED", "ci_excludes_threshold": bool(ci[0] is not None and (ci[0] > threshold or ci[1] < threshold))}


def coupling_block(rows: list[dict], B: int) -> dict:
    """Label-coupling diagnostic (label-USING, diagnostic only, never a metric): under gold-equivalence labels every CORRECT
    row agrees with every other CORRECT row, which mechanically lowers V0 on CORRECT rows. V0_decoupled recomputes V0 from
    the eval-2 matrix with every peer labelled CORRECT removed from the peer pool (>= 2 peers left). If V0's separation
    survives, it is not only CORRECT-CORRECT agreement."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("cv", WS / "freeze_copy" / "consensus_variants.py")
    cv = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cv)
    idx = {r["sentence_id"]: cv.build_index(r) for r in jl(SC / "pairwise_classes_E2B.jsonl")}
    lab_all = {r["row_key"]: r["label"] for r in rows}
    R = [dict(r) for r in rows if r["in_POP"]]
    for r in R:
        ix = idx.get(r["sentence_id"])
        r["V0_decoupled"] = None
        if ix is None or r["row_key"] not in ix["node_of"]:
            continue
        P = [p for p in cv.peers_lofo(ix, r["row_key"]) if lab_all.get(p) != "CORRECT"]
        if len(P) >= 2:
            c = ix["node_of"][r["row_key"]]
            r["V0_decoupled"] = 1 - sum(cv.agree(ix, c, ix["node_of"][p]) for p in P) / len(P)
    C = Cell(R, "coupling", B)
    return {"definition": coupling_block.__doc__.split("\n")[0], "V0_decoupled": C.metric("V0_decoupled"), "V0_same_rows": C.metric("V0"),
            "V0_decoupled - flashlite_disg": C.delta("V0_decoupled", "flashlite_disg"), "V0_decoupled - V0": C.delta("V0_decoupled", "V0"),
            "n_rows_with_decoupled": sum(r["V0_decoupled"] is not None for r in R)}


def rename_block(rows: list[dict]) -> dict:
    cs = jl(SC / "controls_scores_E2B.jsonl")
    if not cs:
        return {"status": "NOT_RUN (no controls)"}
    V0 = {r["row_key"]: r.get("V0") for r in rows}
    out = {}
    for t in ("RENAME_SYN", "RENAME_NONCE"):
        cc = [c for c in cs if c["control_type"] == t and c["V0_control"] is not None and V0.get(c["parent_row_key"]) is not None]
        n = len(cc)
        fa = sum(c["V0_control"] > 0.5 for c in cc)
        base = sum(V0[c["parent_row_key"]] > 0.5 for c in cc)
        flip = sum(c["V0_control"] > 0.5 and not V0[c["parent_row_key"]] > 0.5 for c in cc)
        rev = sum(not c["V0_control"] > 0.5 and V0[c["parent_row_key"]] > 0.5 for c in cc)
        repro = sum(c["V0_parent_recomputed"] is not None and abs(c["V0_parent_recomputed"] - V0[c["parent_row_key"]]) < 1e-9 for c in cc)
        out[t] = {"n_pairs": n, "FA_control": fa / n if n else None, "FA_control_ci": wilson(fa, n), "base_FA_parent": base / n if n else None,
                  "base_FA_ci": wilson(base, n), "paired_flip": flip / n if n else None, "paired_flip_ci": wilson(flip, n),
                  "reverse_flip": rev / n if n else None, "mean_delta_V0_control_minus_parent": float(np.mean([c["V0_control"] - V0[c["parent_row_key"]] for c in cc])) if n else None,
                  "parent_V0_recomputed_matches": repro, "n_controls_total": sum(1 for c in cs if c["control_type"] == t),
                  "n_unscorable": sum(1 for c in cs if c["control_type"] == t and c["V0_control"] is None)}
    out["definition"] = "FA at c > 0.5 on meaning-preserving renames of final-CORRECT parents; paired flip = control flagged while its parent is not; base FA = parent flagged"
    return out


def complexity_block(rows: list[dict], B: int) -> dict:
    R = [r for r in rows if r["in_POP"]]
    sents = json.loads((E2B / "sentences_E2B.json").read_text())
    out = {}
    for var in ("words", "n_conditions", "n_quant", "depth"):
        vals = [s[var] for s in sents]
        qs = list(np.unique(np.quantile(vals, [0.25, 0.5, 0.75])))

        def binof(v):
            for i, q in enumerate(qs):
                if v <= q:
                    return f"Q{i + 1}(<= {q:g})"
            return f"Q{len(qs) + 1}(> {qs[-1]:g})"
        by = defaultdict(list)
        for r in R:
            by[binof(r[var])].append(r)
        res = {}
        for b, rs in sorted(by.items()):
            y = np.array([r["y_AB"] for r in rs])
            ent = {"n": len(rs), "n_error": int(y.sum()), "n_correct": int(len(y) - y.sum()), "n_sentences": len({r["sentence_id"] for r in rs})}
            for m in ("V0", "flashlite_disg", "costmatched_disg", "nano_orig", "p_peer_text"):
                s = np.array([np.nan if r.get(m) is None else r[m] for r in rs], float)
                ok = ~np.isnan(s)
                ent[m] = {"auroc": AB.auroc(y[ok], s[ok]) if ok.sum() > 5 and len(set(y[ok])) == 2 else None,
                          "FA_at_0.5": float(np.mean(s[ok & (y == 0)] > 0.5)) if (ok & (y == 0)).sum() else None,
                          "recall_at_0.5": float(np.mean(s[ok & (y == 1)] > 0.5)) if (ok & (y == 1)).sum() else None}
            res[b] = ent
        out[var] = {"quartile_cuts_on_E2B_sentences": qs, "bins": res}
    return out


def coverage_block(rows: list[dict]) -> dict:
    by = defaultdict(list)
    for r in rows:
        by[r["slot"]].append(r)
    out = {}
    for s, rs in sorted(by.items()):
        n = len(rs)
        out[s] = {"system": rs[0]["system"], "n_rows": n, "parse_rate": sum(r["parse_ok"] for r in rs) / n,
                  "V0_scorable_rate_(>=2_peers)": sum(r["V0"] is not None and r["parse_ok"] for r in rs) / n,
                  "flashlite_disg_ok": sum(r.get("flashlite_disg_status") == "ok" for r in rs) / n,
                  "costmatched_disg_ok": sum(r.get("costmatched_disg_status") == "ok" for r in rs) / n,
                  "labels": dict(Counter(r["label"] for r in rs))}
    allr = len(rows)
    out["ALL"] = {"n_rows": allr, "parse_rate": sum(r["parse_ok"] for r in rows) / allr,
                  "V0_scorable_rate": sum(r["V0"] is not None and r["parse_ok"] for r in rows) / allr,
                  "unparseable_rows_scored_1.0": sum(not r["parse_ok"] for r in rows), "labels": dict(Counter(r["label"] for r in rows))}
    return out


def cost_block(rows: list[dict], cells: dict) -> dict:
    by_s = defaultdict(list)
    for r in rows:
        by_s[r["sentence_id"]].append(r)
    gen_sent = [sum((r.get("gen_cost_usd") or 0.0) for r in rs) for rs in by_s.values()]
    full_peer = []
    for rs in by_s.values():
        tot = sum((r.get("gen_cost_usd") or 0.0) for r in rs)
        for r in rs:
            full_peer.append(tot - (r.get("gen_cost_usd") or 0.0))
    z3s = [rs[0].get("secs_align_sentence") / len(rs) for rs in by_s.values() if rs[0].get("secs_align_sentence") is not None]
    l3 = jl(WS / "exp5src" / "cache" / "l3_cost_ledger.jsonl")
    l3_per_sent = sum(x["cost_usd"] for x in l3) / max(1, len(by_s))
    out = {"V0_c_score_align": {"FULL_usd_per_candidate_(its_9_peer_generations)": float(np.mean(full_peer)),
                                "FULL_usd_per_candidate_amortised_(sentence_generations/10)": float(np.mean(gen_sent)) / 10,
                                "MARGINAL_usd_per_candidate": 0.0, "z3_seconds_per_candidate_(align_readout)": float(np.mean(z3s)) if z3s else None,
                                "note": "peers are the other systems' outputs: in a multi-system evaluation they already exist (MARGINAL = CPU only)"},
           "p_peer_text": {"extra_usd_per_candidate_(L3_questionnaire_per_sentence/10)": l3_per_sent / 10}}
    for m in ("flashlite_disg", "flashlite_orig", "nano_orig", "nano_disg", "costmatched_disg", "costmatched_orig", "frontier_orig"):
        c = [r.get(m + "_cost") for r in rows if r.get(m + "_cost")]
        sec = [r.get(m + "_seconds") for r in rows if r.get(m + "_seconds")]
        out[m] = {"usd_per_call": float(np.mean(c)) if c else None, "n_calls_with_cost": len(c), "seconds_per_call": float(np.mean(sec)) if sec else None}
    L = cells.get("L25_E2B_R_AB", {}).get("metrics", {})
    fl = out["flashlite_disg"]["usd_per_call"]
    for m in ("costmatched_disg", "costmatched_orig", "V0"):
        a = (L.get(m) or {}).get("strat_auroc")
        base = (L.get("flashlite_disg") or {}).get("strat_auroc")
        cm = out.get(m, {}).get("usd_per_call") if m != "V0" else 0.0
        if a is not None and base is not None and cm is not None and fl:
            out.setdefault("auroc_gain_per_extra_usd_vs_flashlite_disg", {})[m] = {"delta_auroc": a - base, "extra_usd_per_candidate": cm - fl,
                                                                                  "gain_per_usd": (a - base) / (cm - fl) if abs(cm - fl) > 1e-12 else None}
    return out


def taub_block(rows: list[dict], B: int) -> dict:
    from scipy.stats import kendalltau
    R = [r for r in rows if r["in_POP"]]
    slots = sorted({r["slot"] for r in R})
    by_s = defaultdict(list)
    for r in R:
        by_s[r["sentence_id"]].append(r)
    sids = sorted(by_s)

    def tau(rs, m):
        acc, mu = [], []
        for s in slots:
            xs = [r for r in rs if r["slot"] == s and r.get(m) is not None]
            if len(xs) < 3:
                continue
            acc.append(np.mean([r["y_AB"] == 0 for r in xs]))
            mu.append(-np.mean([r[m] for r in xs]))
        if len(acc) < 4:
            return np.nan, len(acc)
        return kendalltau(mu, acc, variant="b").statistic, len(acc)
    out = {}
    rng = np.random.default_rng(0)
    picks = [[sids[i] for i in rng.integers(0, len(sids), len(sids))] for _ in range(min(B, 500))]
    for m in ("V0", "p_peer_text", "flashlite_disg", "flashlite_orig", "nano_orig", "costmatched_disg", "costmatched_orig", "S4_E2B"):
        t, n = tau(R, m)
        bs = [tau([r for s in p for r in by_s[s]], m)[0] for p in picks]
        bs = [b for b in bs if not np.isnan(b)]
        out[m] = {"tau_b": fnum(t), "ci": AB.boot_ci(bs), "n_systems": n}
    out["note"] = "system = generator slot (10 slots, 9 families); system mean of (-score) vs system accuracy on R_AB; DESCRIPTIVE only (far fewer systems than WMT)"
    return out


def placebo_block(rows: list[dict], n: int) -> dict:
    """V0 with SHUFFLED sentence peers: each candidate is scored against the other-family peers of a different,
    seeded-random E2-B sentence (exp-5 eqmv, same pair cap). Expected AUROC ~0.5 if the signal needs same-sentence peers."""
    sys.path.insert(0, str(WS / "exp5src" / "src"))
    sys.path.insert(0, str(WS / "exp5src" / "src" / "vendor_a"))
    import peer_text as PT
    import pool_scoring as PS
    from common import eqmv
    PS.init_worker(4.0)
    R = sorted([r for r in rows if r["in_POP"] and r["parse_ok"]], key=lambda r: hashlib.sha1(("placebo|" + r["row_key"]).encode()).hexdigest())[:n]
    rows_all = {r["row_key"]: r for r in jl(SC / "rows_E2B.jsonl")}
    by_s = defaultdict(list)
    for r in rows_all.values():
        if r["parse_ok"]:
            by_s[r["sentence_id"]].append(r)
    sids = sorted(by_s)
    rng = np.random.default_rng(7)
    R = [r for r in R if r.get("V0") is not None]
    ys, vs, v0 = [], [], []
    t0 = time.time()
    for r in R:
        other = r["sentence_id"]
        while other == r["sentence_id"]:
            other = sids[rng.integers(0, len(sids))]
        cs = PT.canon(PT.parse_fol(rows_all[r["row_key"]]["candidate_fol"]))
        P = [PT.canon(PT.parse_fol(p["candidate_fol"])) for p in by_s[other] if p["family_vendor"] != r["family"]]
        if len(P) < 2:
            continue
        eqs = []
        for q in P:
            res, to = PS._with_alarm(5, eqmv, PT.parse_fol(cs), PT.parse_fol(q))
            eqs.append(False if (to or res is None) else res[0] is True)
        ys.append(r["y_AB"])
        vs.append(1 - sum(eqs) / len(P))
        v0.append(r["V0"])
    ys, vs = np.array(ys), np.array(vs)
    return {"n": len(ys), "auroc_V0_shuffled_peers": AB.auroc(ys, vs) if len(set(ys)) == 2 else None,
            "auroc_V0_same_rows": AB.auroc(ys, np.array([np.nan if v is None else v for v in v0], float)) if len(set(ys)) == 2 else None,
            "share_shuffled_score_1.0": float(np.mean(vs == 1.0)) if len(vs) else None, "secs": round(time.time() - t0, 1)}


# ================================================================================================= main
@logger.catch(reraise=True)
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--B", type=int, default=2000)
    ap.add_argument("--placebo-n", dest="placebo_n", type=int, default=300)
    a = ap.parse_args()
    t0 = time.time()
    seals = verify_seals()
    rows = join()
    pop = choose_population(rows)
    for r in rows:
        r["in_POP"] = r["in_R_AB"] if pop["population"] == "R_AB" else r["in_R_AU"]
    s4info = add_s4(rows)
    (AN / "per_item_E2B.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    logger.info(f"joined {len(rows)} rows; labels {Counter(r['label'] for r in rows)}; R_AB {sum(r['in_R_AB'] for r in rows)}")
    A = {"seals": seals, "n_rows": len(rows), "label_counts": dict(Counter(r["label"] for r in rows)),
         "tier_counts": dict(Counter(r["tier"] for r in rows)), "label_regime": rows[0]["label_regime"] if rows else None,
         "s4": s4info, "B": a.B, "analysis_population": pop}
    # ---------------- populations x cells
    pops = {"R_AB": lambda r: r["in_R_AB"], "R_A": lambda r: r["in_R_A"],
            "CONTESTED_as_CORRECT": lambda r: r["in_R_AB_cont"], "CONTESTED_as_ERROR": lambda r: r["in_R_AB_cont"],
            "R_A_UNAUDITED": lambda r: r["in_R_AU"]}
    cells = {}
    for pn, pf in pops.items():
        R = [dict(r) for r in rows if pf(r)]
        if pn == "CONTESTED_as_CORRECT":
            for r in R:
                r["y_AB"] = 1 if r["label"] == "ERROR" else 0
        if pn == "CONTESTED_as_ERROR":
            for r in R:
                r["y_AB"] = 0 if r["label"] == "CORRECT" else 1
        subcells = {"L25_E2B": R}
        if pn == pop["population"]:
            for b in ("25-29", "30-34"):
                subcells[f"L25_E2B_bin_{b}"] = [r for r in R if r["word_bin"] == b]
        for cn, rr in subcells.items():
            if len(rr) < 20 or len({r["y_AB"] for r in rr}) < 2:
                cells[f"{cn}_{pn}"] = {"status": "NOT_TESTABLE", "n": len(rr)}
                continue
            C = Cell(rr, cn, a.B)
            full = pn == pop["population"] and cn == "L25_E2B"
            ms = METRICS if full else ["V0", "flashlite_disg", "flashlite_orig", "nano_orig", "costmatched_disg", "costmatched_orig", "p_peer_text"]
            ent = {"counts": C.counts(np.ones(len(rr), bool)), "metrics": {m: C.metric(m) for m in ms}}
            ent["deltas"] = {f"V0 - {c}": C.delta("V0", c) for c in COMPARATORS}
            if full:
                ent["deltas"]["V0 - frontier_orig (unweighted, subsample rows)"] = C.delta("V0", "frontier_orig")
                ent["deltas"]["p_peer_text - flashlite_disg"] = C.delta("p_peer_text", "flashlite_disg")
                ent["deltas"]["S4_E2B_plus_V0 - S4_E2B (nested, B2)"] = C.delta("S4_E2B_plus_V0", "S4_E2B")
                ent["deltas"]["V0 - S4_E2B"] = C.delta("V0", "S4_E2B")
                for v in ("V1", "V2", "V3", "V4", "V5", "c_exact"):
                    ent["deltas"][f"{v} - V0 (development-only)"] = C.delta(v, "V0")
                ent["deltas"]["costmatched_disg - flashlite_disg"] = C.delta("costmatched_disg", "flashlite_disg")
                ent["deltas"]["V0 - flashlite_disg_vfb (T1 sensitivity: verdict-median fill)"] = C.delta("V0", "flashlite_disg_vfb")
                ent["deltas"]["V0 - costmatched_disg_vfb (T1 sensitivity: verdict-median fill)"] = C.delta("V0", "costmatched_disg_vfb")
                okm = np.array([r.get("flashlite_disg_status") == "ok" for r in rr])
                ent["deltas"]["V0 - flashlite_disg (judge-ok rows only)"] = C.delta("V0", "flashlite_disg", extra_mask=okm)
                ent["judge_status_counts"] = {j: dict(Counter(r.get(j + "_status") for r in rr)) for j in
                                              ("flashlite_disg", "flashlite_orig", "nano_orig", "nano_disg", "costmatched_disg", "costmatched_orig", "frontier_orig")}
                # own-family exclusion (judge self-preference control)
                ofe = {}
                slots = np.array([r["slot"] for r in rr])
                for j, fam_slot in OWN_FAMILY.items():
                    ofe[j] = {"excluded_slot": fam_slot, "with_all_rows": C.delta("V0", j), "excluding_own_family": C.delta("V0", j, extra_mask=slots != fam_slot)}
                ent["own_family_exclusion"] = ofe
            cells[f"{cn}_{pn}"] = ent
            logger.info(f"cell {cn}_{pn}: {ent['counts']} V0-flashlite_disg {ent['deltas']['V0 - flashlite_disg'].get('strat_delta')}")
    A["cells"] = cells
    A["frontier_B4"] = frontier_block(rows, a.B)
    try:
        A["H_MECH"] = hmech(rows, a.B)
    except Exception as e:  # noqa: BLE001 - reported, never silent
        logger.error(f"H-MECH failed: {e}")
        A["H_MECH"] = {"status": f"FAILED: {e}"}
    A["rename"] = rename_block(rows)
    try:
        A["label_coupling_diagnostic"] = coupling_block(rows, a.B)
    except Exception as e:  # noqa: BLE001
        logger.error(f"coupling diagnostic failed: {e}")
        A["label_coupling_diagnostic"] = {"status": f"FAILED: {e}"}
    A["complexity"] = complexity_block(rows, a.B)
    A["coverage"] = coverage_block(rows)
    A["cost"] = cost_block(rows, cells)
    A["system_tau_b"] = taub_block(rows, a.B)
    try:
        A["placebo_shuffled_peers"] = placebo_block(rows, a.placebo_n) if a.placebo_n else {"status": "skipped"}
    except Exception as e:  # noqa: BLE001
        logger.error(f"placebo failed: {e}")
        A["placebo_shuffled_peers"] = {"status": f"FAILED: {e}"}
    A["secs"] = round(time.time() - t0, 1)
    A["code_sha256"] = {"analyse_e2b.py": sha(Path(__file__)), "exp6src/src/api_bar.py": sha(WS / "exp6src/src/api_bar.py"),
                        "exp6src/src/s4.py": sha(WS / "exp6src/src/s4.py")}
    (AN / "analysis_E2B.json").write_text(json.dumps(A, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
    verdict(A, rows)
    logger.info(f"analysis done in {A['secs']}s")


def _panel_fraction(sents: list[dict]) -> dict:
    prog = jl(E2B / "progress.jsonl")
    last = max([p["batch"] for p in prog], default=0)
    tot = Counter(s["word_bin"] for s in sents)
    done = Counter(s["word_bin"] for s in sents if s["e2b_batch"] <= last)
    return {b: f"{done[b]}/{tot[b]}" for b in tot}


def verdict(A: dict, rows: list[dict]) -> None:
    popn = A["analysis_population"]["population"]
    L = A["cells"].get(f"L25_E2B_{popn}", {})
    d = (L.get("deltas") or {})
    b1 = d.get("V0 - flashlite_disg", {})
    b2 = d.get("S4_E2B_plus_V0 - S4_E2B (nested, B2)", {})
    b3 = d.get("V0 - costmatched_disg", {})
    se = b1.get("strat_se")
    tst = A["analysis_population"].get("testable", True) if popn != "R_AB" else True
    tst_txt = ("" if tst else "NOT TESTABLE by E's pre-registered rule in any regime (no panel: R_AB has no CORRECT class; "
               f"R_A_UNAUDITED has {A['analysis_population']['R_A_UNAUDITED']['CORRECT_rows']} CORRECT rows < 50); the numbers below are "
               "EXPLORATORY estimates in a gold-equivalence label regime that structurally favours agreement-based metrics. ")
    V = {"label_regime": A["label_regime"], "analysis_population": A["analysis_population"],
         "population": (f"L25_E2B {popn}" + (" (LLM systems, tiers A+B, excluding CONTESTED and reading_choice)" if popn == "R_AB" else
                                              " (LLM systems, tier A_unaudited_ref: solver vs unaudited MALLS gold; SECONDARY)")),
         "testable_under_E_rule": tst, "testability_note": tst_txt or "testable",
         "B1_V0_minus_flashlite_disg": {"delta": b1.get("strat_delta"), "ci": b1.get("strat_ci"), "n": b1.get("n"),
                                        "sentences_with_both_classes": b1.get("sentences_with_both_classes"),
                                        "verdict": (("NOT TESTABLE (E's rule); exploratory CI " + ("> 0" if b1.get("ci_gt_0") else "includes 0 or < 0")) if not tst else
                                                    "CONFIRMED (CI > 0)" if b1.get("ci_gt_0") else
                                                    ("POSITIVE, CI includes 0 (underpowered alone: pre-registered MDE80 0.103)" if (b1.get("strat_delta") or 0) > 0 else
                                                     "NOT CONFIRMED (point <= 0)")),
                                        "observed_MDE80_from_bootstrap_SE": 2.8 * se if se else None,
                                        "also_vs": {k: {"delta": v.get("strat_delta"), "ci": v.get("strat_ci")} for k, v in d.items()
                                                    if k.startswith("V0 - ") and k != "V0 - flashlite_disg"}},
         "B2_nested_S4_plus_V0_minus_S4": {"delta": b2.get("strat_delta"), "ci": b2.get("strat_ci"),
                                           "verdict": (("NOT TESTABLE (E's rule); exploratory CI " + ("> 0" if b2.get("ci_gt_0") else "includes 0 or < 0")) if not tst else
                                                       "CONFIRMED (CI > 0)" if b2.get("ci_gt_0") else "NOT CONFIRMED"), "substituted": A["s4"]["substituted"]},
         "label_coupling_diagnostic": {k: (v.get("strat_delta") if isinstance(v, dict) and "strat_delta" in v else
                                           (v.get("strat_auroc") if isinstance(v, dict) and "strat_auroc" in v else v))
                                       for k, v in (A.get("label_coupling_diagnostic") or {}).items() if k != "definition"},
         "B3_V0_minus_costmatched_disg": {"delta": b3.get("strat_delta"), "ci": b3.get("strat_ci"), "directional_prediction": "none (pre-registered)",
                                          "reading": ("NOT RUN: every cost-matched call was refused (HTTP 403 run budget exhausted)" if b3.get("strat_delta") is None else
                                                      "V0 above the cost-matched judge (CI > 0)" if b3.get("ci_gt_0") else
                                                      ("cost-matched judge above V0 (CI < 0)" if (b3.get("strat_ci") or [0, 0])[1] is not None and (b3.get("strat_ci") or [0, 0])[1] < 0 else
                                                       "no significant difference"))},
         "B4_frontier": {k: A["frontier_B4"].get(k) for k in ("status", "ratio_V0_over_frontier", "delta_V0_minus_frontier",
                                                                "nested_frontier_plus_V0_minus_frontier", "n_in_R_AB_complete")},
         "H_IMPROVE": "no carried variant: M1 selection.json winner = 'NONE: V0 stands'; V1-V5 reported as development-only rows",
         "H_MECH": {k: (v.get("verdict") if isinstance(v, dict) else v) for k, v in (A.get("H_MECH") or {}).items() if k != "definitions"},
         "sensitivity_B1": {pn: (A["cells"].get(f"L25_E2B_{pn}", {}).get("deltas", {}).get("V0 - flashlite_disg", {}) or {}).get("strat_delta")
                            for pn in ("R_A", "CONTESTED_as_CORRECT", "CONTESTED_as_ERROR")},
         "secondary_note": (("NO PANEL: the run-level OpenRouter budget was exhausted before any batch completed the panel; labels are E's final "
                             "rule without votes (tier A against the unaudited MALLS gold). Nothing is confirmatory; every number is exploratory")
                            if str(A["label_regime"]).startswith("NO_PANEL") else
                            "label regime DRIFTED: every E2-B result is SECONDARY" if A["label_regime"] != "PASS" else
                            "label regime PASS (M2 from E2-A, pinned providers); E2-B-alone numbers are secondary to the union by design")}
    (AN / "confirm_verdict_E2B.json").write_text(json.dumps(V, indent=1, default=str))
    per = AN / "per_item_E2B.jsonl"
    sents = json.loads((E2B / "sentences_E2B.json").read_text())
    have = {r["sentence_id"] for r in rows}
    comp = Counter(s["word_bin"] for s in sents if s["sentence_id"] in have)
    tot = Counter(s["word_bin"] for s in sents)
    marker = {"token": "aii_iter5_e2b_final_v1", "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "per_row_file": str(per), "sha256": sha(per), "n_rows": len(rows), "label_regime": A["label_regime"],
              "solver_labelled_fraction_per_word_bin": {b: f"{comp[b]}/{tot[b]}" for b in tot},
              "panel_completed_fraction_per_word_bin": _panel_fraction(sents),
              "analysis_population": A["analysis_population"]["population"], "testable_under_E_rule": A["analysis_population"].get("testable", True),
              "drift_decision_M2": json.loads((E2B / "drift_decision.json").read_text()).get("decision"),
              "columns": {"row_key": "sentence_id|slot", "e2_row_key": "E2 recipe item_id|prompt_variant", "stratum": "L25_E2B",
                          "label": "CORRECT/ERROR/CONTESTED/UNRESOLVED/UNPARSEABLE", "tier": "A/B/C/-", "in_R_AB": "primary population flag",
                          "y_AB": "1 ERROR / 0 CORRECT", "V0": "c_score_align (exp-5 byte-identical, leave-own-family-out), unparseable -> 1.0",
                          "flashlite_disg/flashlite_orig/nano_orig/nano_disg/costmatched_disg/costmatched_orig/frontier_orig": "1 - P(faithful) judges, unparseable -> 1.0",
                          "p_peer_text": "PT frozen exp-5 fusion", "V1..V5/c_exact": "M1 variants (development-only)", "word_bin": "25-29 / 30-34"},
              "confirm_verdict": str(AN / "confirm_verdict_E2B.json")}
    (E2B / "E2B_FINAL_READY.json").write_text(json.dumps(marker, indent=1))


if __name__ == "__main__":
    main()
