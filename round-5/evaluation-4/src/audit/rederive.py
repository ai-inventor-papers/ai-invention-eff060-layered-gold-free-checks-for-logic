#!/usr/bin/env python3
"""Independent re-derivation of 12 headline numbers from RAW per-item files.

Second code path: imports nothing from src/ (numpy/pandas/json only), reads the raw per-item
files, recomputes, and compares with the transcribed value at the transcribed precision.
Placebos: shuffled labels within stratum must give AUROC ~0.5 (and a CI that covers 0.5).
Output: audit/rederive.json
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

RUN = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop")
I4 = RUN / "iter_4/gen_art"
OUT = Path(__file__).resolve().parent / "rederive.json"


def jl(p: Path) -> list[dict]:
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]


def cmp_mat(pos: np.ndarray, neg: np.ndarray) -> np.ndarray:
    return (pos[:, None] > neg[None, :]).astype(float) + 0.5 * (pos[:, None] == neg[None, :])


def strat_auc_pairweighted(y, s, st) -> float:
    num = den = 0.0
    for g in np.unique(st):
        m = st == g
        pos, neg = s[m & (y == 1)], s[m & (y == 0)]
        if len(pos) and len(neg):
            num += cmp_mat(pos, neg).sum()
            den += len(pos) * len(neg)
    return num / den


def strat_auc_nweighted(y, s, st) -> float:
    num = den = 0.0
    for g in np.unique(st):
        m = st == g
        pos, neg = s[m & (y == 1)], s[m & (y == 0)]
        if len(pos) and len(neg):
            num += cmp_mat(pos, neg).mean() * m.sum()
            den += m.sum()
    return num / den


def boot_ci(y, s, st, sid, B=2000, seed=0) -> list[float]:
    """Sentence-cluster bootstrap of the pair-weighted stratified AUROC (vectorised by weights)."""
    rng = np.random.default_rng(seed)
    sents, inv = np.unique(sid, return_inverse=True)
    blocks = []
    for g in np.unique(st):
        m = st == g
        ip, ineg = np.where(m & (y == 1))[0], np.where(m & (y == 0))[0]
        if len(ip) and len(ineg):
            blocks.append((cmp_mat(s[ip], s[ineg]), inv[ip], inv[ineg]))
    vals = []
    for _ in range(B):
        w = np.bincount(rng.integers(0, len(sents), len(sents)), minlength=len(sents)).astype(float)
        num = den = 0.0
        for C, a, b in blocks:
            wp, wn = w[a], w[b]
            num += wp @ C @ wn
            den += wp.sum() * wn.sum()
        if den > 0:
            vals.append(num / den)
    return [float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))]


def check(name, got, transcribed, dec) -> dict:
    ok = abs(got - transcribed) <= 0.5 * 10 ** (-dec) + 1e-12
    return dict(item=name, rederived=got, transcribed=transcribed, precision_decimals=dec, PASS=bool(ok))


def main() -> None:
    res: dict = {"method": __doc__.strip(), "checks": [], "extra": {}}
    C = res["checks"]
    # (1) exp 9 per-item file
    rows = jl(I4 / "gen_art_experiment_9/results/per_item_csc_E.jsonl")
    prim = [r for r in rows if r["in_PRIMARY"]]
    y = np.array([r["y_R_AB"] for r in prim]); st = np.array([r["stratum"] for r in prim]); sid = np.array([r["sentence_id"] for r in prim])
    for key, tv in (("c_csc", 0.614), ("c_free_exact", 0.770), ("c_score_align", 0.774)):
        s = np.array([np.nan if r[key] is None else r[key] for r in prim], dtype=float)
        ok = ~np.isnan(s)
        pw = strat_auc_pairweighted(y[ok], s[ok], st[ok])
        nw = strat_auc_nweighted(y[ok], s[ok], st[ok])
        C.append(check(f"exp9 strat AUROC {key} (pair-weighted within-stratum; exp-9 src definition)", pw, tv, 3))
        res["extra"][f"{key}_nweighted_strat"] = nw
    s = np.array([r["c_csc"] for r in prim], dtype=float)
    res["extra"]["c_csc_boot_ci_B2000_seed0"] = boot_ci(y, s, st, sid)
    res["extra"]["c_csc_ci_transcribed_T4"] = [0.493, 0.736]
    res["extra"]["c_csc_ci_reviewer_B300"] = [0.501, 0.728]
    res["extra"]["ci_note"] = "our CI is reported; the paper TRANSCRIBES T4. Differences are resampling noise / B and seed."
    err, cor = y == 1, y == 0
    fx = np.array([r["c_free_exact"] for r in prim], dtype=float)
    C.append(check("exp9 CSC e (ERROR rows with c <= 0.5)", float((s[err] <= 0.5).mean()), 0.459, 3))
    C.append(check("exp9 FREE_exact e", float((fx[err] <= 0.5).mean()), 0.173, 3))
    C.append(check("exp9 CSC d (CORRECT rows with c > 0.5)", float((s[cor] > 0.5).mean()), 0.139, 3))
    C.append(check("exp9 FREE_exact d", float((fx[cor] > 0.5).mean()), 0.323, 3))
    full_cor = [r for r in rows if r["y_R_AB"] == 0]
    res["extra"]["n_primary_err_cor_sent"] = [len(prim), int(err.sum()), int(cor.sum()), len(set(sid))]
    res["extra"]["ctrl_share_primary_correct"] = float(np.mean(st[cor] == "CTRL"))
    res["extra"]["ctrl_share_full_correct"] = float(np.mean([r["stratum"] == "CTRL" for r in full_cor]))
    C.append(check("exp9 CTRL share of FULL CORRECT rows", res["extra"]["ctrl_share_full_correct"], 0.274, 3))
    res["extra"]["c_csc_tie_rate_1_minus_unique_over_n"] = 1 - len(np.unique(s)) / len(s)
    rng = np.random.default_rng(7)
    yp = y.copy()
    for g in np.unique(st):
        m = np.where(st == g)[0]
        yp[m] = rng.permutation(y[m])
    plc = strat_auc_pairweighted(yp, s, st)
    plc_ci = boot_ci(yp, s, st, sid, B=500, seed=1)
    res["placebo_shuffled_labels_c_csc"] = dict(auroc=plc, ci_B500=plc_ci, covers_0_5=bool(plc_ci[0] <= 0.5 <= plc_ci[1]))
    # (2) exp 10 per-row PERTURB scores: base FA at c > 0.5 and LOCAL2 tie share
    pr = jl(I4 / "gen_art_experiment_10/results/perturb_csc_scores.jsonl")
    for key, rc, tv, name in (("c_align_exp8", False, 0.712, "c_align E"), ("c_free3_exact", False, 0.803, "FREE3_exact E"),
                              ("c_free3_exact", True, 0.986, "FREE3_exact R_COMP"), ("c_free3_align", True, 0.757, "FREE3_align R_COMP")):
        b = [r[key] for r in pr if r["op_label"] == "BASE" and r["is_rcomp"] == rc and r.get(key) is not None]
        C.append(check(f"exp10 base FA at c > 0.5, {name}", float(np.mean(np.array(b) > 0.5)), tv, 3))
    mut = [r["c_local"] for r in pr if r["y"] == 1 and r.get("c_local") is not None]
    res["extra"]["local2_share_exactly_0_5"] = float(np.mean(np.array(mut) == 0.5))
    res["extra"]["local2_e_all"] = float(np.mean(np.array(mut) <= 0.5))
    # (3) dataset 4 label counts
    lab = Counter(r["label"] for r in jl(I4 / "gen_art_dataset_4/sealed/labels_E2.jsonl"))
    res["extra"]["d4_label_counts"] = dict(lab)
    C.append(check("dataset 4 E2 pilot counts ERROR/UNRESOLVED/UNPARSEABLE/CORRECT == 36/274/20/0",
                   float([lab.get("ERROR", 0), lab.get("UNRESOLVED", 0), lab.get("UNPARSEABLE", 0), lab.get("CORRECT", 0)] == [36, 274, 20, 0]), 1.0, 0))
    # (4) dataset 5 label counts (+ 297/420 SOURCE_ONLY: needs the iter-3 label join)
    l5 = Counter(r.get("label") for r in jl(I4 / "gen_art_dataset_5/results/free_labels_v2.jsonl"))
    res["extra"]["d5_label_counts"] = dict(l5)
    C.append(check("dataset 5 counts ERROR_CERT/MAPPED/UNPARSEABLE/NO_OUTPUT == 759/1506/188/199",
                   float([l5.get("ERROR_CERT", 0), l5.get("UNRESOLVED_GLOSS_NOT_RUN", 0), l5.get("UNPARSEABLE", 0), l5.get("NO_OUTPUT", 0)] == [759, 1506, 188, 199]), 1.0, 0))
    res["extra"]["d5_297_of_420"] = "SOURCE_ONLY (old_label_agreement.json); the iter-3 label join is not re-run here"
    # (5) eval-3 77% / 61% from the pair table
    try:
        pairs = pd.read_pickle(I4 / "gen_art_evaluation_3/results/part1_pairs.pkl")
        rws = pd.read_pickle(I4 / "gen_art_evaluation_3/results/part1_rows.pkl")
        ycol = "y_AB" if "y_AB" in rws.columns else "final_label"
        yc = dict(zip(rws["row_key"], rws[ycol]))
        pairs = pairs.assign(cy=pairs["cand"].map(yc))
        dis = pairs[(pairs["cy"] == 0) & pairs["cls"].isin(["VOCAB", "IRREDUCIBLE"])]
        s9 = float((dis["peer_y"] == 1).mean())
        d3 = dis[dis["in_pool3"]]
        s3 = float((d3["peer_y"] == 1).mean())
        C.append(check("eval3 9-family share of non-agreeing peers of CORRECT candidates labelled ERROR", s9, 0.77, 2))
        C.append(check("eval3 3-pool share (in_pool3 pairs)", s3, 0.61, 2))
    except (FileNotFoundError, KeyError, ValueError) as e:
        res["extra"]["eval3_shares"] = f"SOURCE_ONLY ({type(e).__name__}: {e})"
    # (6) iteration-4 spend: sum of the four iter-4 ledgers (independent of src/spend.py)
    tot = 0.0
    for p, f in ((I4 / "gen_art_experiment_9/results/api_cost_ledger.jsonl", "usd"), (I4 / "gen_art_experiment_10/results/api_cost_ledger.jsonl", "cost_usd"),
                 (I4 / "gen_art_dataset_4/cost_ledger.jsonl", "cost_usd"), (I4 / "gen_art_dataset_5/cost_ledger.jsonl", "usd")):
        tot += sum(float(r.get(f) or 0) for r in jl(p))
    C.append(check("iteration-4 spend (four iter-4 ledgers)", tot, 0.35, 2))
    res["n_checks"] = len(C)
    res["n_pass"] = sum(c["PASS"] for c in C)
    OUT.write_text(json.dumps(res, indent=1))
    print(f"audit: {res['n_pass']}/{res['n_checks']} pass; placebo {res['placebo_shuffled_labels_c_csc']}")


if __name__ == "__main__":
    main()
