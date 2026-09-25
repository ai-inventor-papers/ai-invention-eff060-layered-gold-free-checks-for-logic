"""Independent re-derivation of the headline numbers (T4c) + shuffled-label placebos (T4b).

Separate code path from src/analysis.py / src/analysis_E.py: labels are read straight from dataset E's JSON, scores
straight from results/scores/*.jsonl and E_baseline_features.jsonl, AUROC is the explicit Mann-Whitney statistic
(pairwise with ties = 0.5, via ranks), CIs use a python-`random` sentence-cluster bootstrap (1,000 resamples, seed 1).
Usage: PYTHONHASHSEED=0 .venv/bin/python tests/audit_E.py  -> results/audit_E.json
"""
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import rankdata

ROOT = Path(__file__).resolve().parent.parent
E = Path(__file__).resolve().parents[4] / "round-1/dataset-1/src/full_data_out.json"


def mw_auc(y, s):
    y, s = np.asarray(y), np.asarray(s, dtype=float)
    ok = ~np.isnan(s)
    y, s = y[ok], s[ok]
    n1, n0 = int(y.sum()), int(len(y) - y.sum())
    if n1 == 0 or n0 == 0:
        return float("nan")
    r = rankdata(s)
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def cluster_boot(keys, clusters, fn, B=1000, seed=1):
    rnd = random.Random(seed)
    by = defaultdict(list)
    for i, k in enumerate(keys):
        by[clusters[k]].append(i)
    cl = sorted(by)
    out = []
    for _ in range(B):
        idx = [i for c in (rnd.choice(cl) for _ in cl) for i in by[c]]
        out.append(fn(idx))
    a = np.array([x for x in out if x == x])
    return [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]


def main():
    d = json.loads(E.read_text())
    rows = next(g for g in d["datasets"] if g["dataset"] == "heldout_candidates")["examples"]
    cnt = defaultdict(int)
    for r in rows:
        cnt[r["metadata_item_id"]] += 1
    lab, pool, clusters, strat = {}, {}, {}, {}
    for r in rows:
        rk = r["metadata_item_id"] if cnt[r["metadata_item_id"]] == 1 else f"{r['metadata_item_id']}~{r['metadata_prompt_variant']}"
        clusters[rk] = r["metadata_sentence_id"]
        pool[rk] = r["metadata_system_class"]
        strat[rk] = r["metadata_strata"]["source_stratum"]
        if r["metadata_label_tier"] in ("A", "B") and r["metadata_final_label"] in ("CORRECT", "ERROR") and not r.get("metadata_reading_choice"):
            lab[rk] = 1 if r["metadata_final_label"] == "ERROR" else 0
    feats = [json.loads(l) for l in (ROOT / "E_baseline_features.jsonl").read_text().splitlines()]
    F = {f["row_key"]: f for f in feats}
    A = json.loads((ROOT / "results" / "analysis_E.json").read_text())
    bar = A["bar"]
    keys = sorted(k for k in lab if pool[k] == "llm" and F[k]["parse_ok"])
    y = np.array([lab[k] for k in keys])

    def col(c):
        out = []
        for k in keys:
            f = F[k]
            if f.get(c + "__status") == "fail":
                out.append(A["fail_fill"].get(c, 1.0))
            else:
                out.append(np.nan if f.get(c) is None else f[c])
        return np.array(out, dtype=float)
    res = {"bar": bar, "n": len(keys)}
    sb = col(bar)
    res["bar_auroc"] = mw_auc(y, sb)
    res["bar_auroc_ci"] = cluster_boot(keys, clusters, lambda idx: mw_auc(y[idx], sb[idx]))
    res["bar_auroc_original"] = A["sets"]["R_AB|pooled"]["metrics"][bar]["auroc"]
    # S4 - bar: S4 OOF is read from method_out.json predictions (the refit lives in src/s4.py)
    mo = json.loads((ROOT / "method_out.json").read_text())
    ex = {e["metadata_row_key"]: e for e in mo["datasets"][0]["examples"]}
    s4name = "S4_oof_RAB" if f"predict_S4_oof_RAB" in next(iter(ex.values())) else "S4_local_oof_RAB"
    s4 = np.array([float(ex[k][f"predict_{s4name}"]) if ex[k][f"predict_{s4name}"] not in ("NA", "FAIL") else np.nan for k in keys])
    res["S4_name"] = s4name
    res["S4_minus_bar"] = mw_auc(y, s4) - mw_auc(y, sb)
    res["S4_minus_bar_ci"] = cluster_boot(keys, clusters, lambda idx: mw_auc(y[idx], s4[idx]) - mw_auc(y[idx], sb[idx]))
    res["S4_minus_bar_original"] = A["sets"]["R_AB|pooled"].get("paired_vs_bar", {}).get("deltas", {}).get(s4name, {}).get("delta")
    # independent S4 refit with its own sklearn pipeline (same folds, same features)
    from sklearn.impute import SimpleImputer
    from sklearn.linear_model import LogisticRegression
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler
    feats_used = json.loads((ROOT / "results" / "s4_coefs.json").read_text())[s4name]["features_used"]
    allk = sorted(k for k in F if pool[k] == "llm")
    X = np.array([[A["fail_fill"].get(c, 1.0) if F[k].get(c + "__status") == "fail" else (np.nan if F[k].get(c) is None else F[k][c])
                   for c in feats_used] for k in allk], dtype=float)
    M = np.isnan(X).astype(float)
    X = np.hstack([X, M[:, M.any(0)]])
    fold = np.array([F[k]["metadata_fold_E"] for k in allk])
    yy = np.array([lab.get(k, -1) for k in allk])
    oof = np.full(len(allk), np.nan)
    for kf in range(5):
        tr, te = (fold != kf) & (yy >= 0), fold == kf
        pipe = make_pipeline(SimpleImputer(strategy="mean"), StandardScaler(), LogisticRegression(C=1.0, max_iter=3000))
        pipe.fit(X[tr], yy[tr])
        oof[te] = pipe.predict_proba(X[te])[:, 1]
    o = dict(zip(allk, oof))
    s4b = np.array([o[k] for k in keys])
    res["S4_refit_auroc"] = mw_auc(y, s4b)
    res["S4_original_auroc"] = mw_auc(y, s4)
    # larger judge - cheap judge on the frame
    fr = json.loads((ROOT / "data" / "frontier_frame.json").read_text())["rows"]
    fk = [r["item_id"] for r in fr if r["item_id"] in lab]
    yf = np.array([lab[k] for k in fk])
    big, small = ("judge_strong_orig", "judge_cheap_orig") if F[fk[0]].get("judge_strong_orig__status") == "ok" else \
        ("judge_local_qwen14b_orig", "judge_local_qwen8b_orig")

    def fcol(c):
        return np.array([np.nan if F[k].get(c) is None else F[k][c] for k in fk], dtype=float)
    sB, sS = fcol(big), fcol(small)
    res["frame_contrast"] = f"{big} - {small}"
    res["frame_delta"] = mw_auc(yf, sB) - mw_auc(yf, sS)
    res["frame_delta_ci"] = cluster_boot(fk, clusters, lambda idx: mw_auc(yf[idx], sB[idx]) - mw_auc(yf[idx], sS[idx]))
    res["frame_delta_original"] = A["frontier_frame"]["contrasts"].get(f"{big} - {small}", {}).get("delta")
    # one DiD (bar component)
    comp = bar.rsplit("_", 1)[0]
    gk = sorted(k for k in lab if pool[k] == "reference_gold_as_system" and F[k]["parse_ok"])
    yg = np.array([lab[k] for k in gk])

    def c2(c, ks):
        return np.array([np.nan if F[k].get(c) is None else F[k][c] for k in ks], dtype=float)
    dE = mw_auc(y, c2(comp + "_orig", keys)) - mw_auc(y, c2(comp + "_disg", keys))
    dG = mw_auc(yg, c2(comp + "_orig", gk)) - mw_auc(yg, c2(comp + "_disg", gk))
    res["DiD"] = dG - dE
    res["DiD_original"] = A["contamination"].get(comp, {}).get("DiD", {}).get("point")
    # B2
    if "b2_score" in F[keys[0]]:
        s2 = col("b2_score")
        res["b2_auroc"] = mw_auc(y, s2)
        res["b2_auroc_ci"] = cluster_boot(keys, clusters, lambda idx: mw_auc(y[idx], s2[idx]))
        res["b2_auroc_original"] = A["sets"]["R_AB|pooled"]["metrics"].get("b2_score", {}).get("auroc")
    # placebos: shuffled labels
    rng = np.random.default_rng(7)
    pl = {}
    for name, s in (("bar", sb), ("S4", s4), ("b2", col("b2_score") if "b2_score" in F[keys[0]] else None)):
        if s is None:
            continue
        pl[name] = float(np.mean([mw_auc(rng.permutation(y), s) for _ in range(50)]))
    yp = rng.permutation(y)
    pl["S4_minus_bar_shuffled"] = mw_auc(yp, s4) - mw_auc(yp, sb)
    pl["S4_minus_bar_shuffled_ci"] = cluster_boot(keys, clusters, lambda idx: mw_auc(yp[idx], s4[idx]) - mw_auc(yp[idx], sb[idx]), B=300)
    ypf = rng.permutation(yf)
    pl["frame_delta_shuffled"] = mw_auc(ypf, sB) - mw_auc(ypf, sS)
    res["placebos"] = pl
    res["agree_3dp"] = {
        "bar_auroc": round(res["bar_auroc"], 3) == round(res["bar_auroc_original"], 3),
        "S4_minus_bar": res["S4_minus_bar_original"] is not None and round(res["S4_minus_bar"], 3) == round(res["S4_minus_bar_original"], 3),
        "frame_delta": res["frame_delta_original"] is not None and round(res["frame_delta"], 3) == round(res["frame_delta_original"], 3),
        "DiD": res["DiD_original"] is not None and round(res["DiD"], 3) == round(res["DiD_original"], 3),
        "b2_auroc": res.get("b2_auroc_original") is not None and round(res["b2_auroc"], 3) == round(res["b2_auroc_original"], 3)}
    (ROOT / "results" / "audit_E.json").write_text(json.dumps(res, indent=1))
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    sys.exit(main())
