"""Independent re-derivation of the headline numbers (TODO 4). Different code path from analysis.py:
labels read directly from screen_items.json; scores recomputed from raw per-item fields; AUROC via a hand-written
Mann-Whitney rank formula (no sklearn); fused p re-predicted from the pickled no-leak model and raw feature fields;
placebo: the same AUROC / paired delta on permuted labels must collapse to ~0.5 / ~0."""
import json
import pickle
import random
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
labels = {x["item_id"]: x for x in json.loads((ROOT / "screen_items.json").read_text())}
rows = [json.loads(l) for l in (ROOT / "results" / "scores_unlabelled.jsonl").read_text().splitlines() if l.strip()]
L = [r for r in rows if r["track"] == "L"]


def rank_auc(pos, neg):
    """P(score_pos > score_neg) + 0.5 P(tie), computed with average ranks."""
    allv = np.array(list(pos) + list(neg), float)
    order = allv.argsort(kind="mergesort")
    ranks = np.empty(len(allv))
    sv = allv[order]
    i = 0
    while i < len(sv):
        j = i
        while j + 1 < len(sv) and sv[j + 1] == sv[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2 + 1
        i = j + 1
    rp = ranks[:len(pos)].sum()
    return (rp - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg))


prim = [r for r in L if labels[r["item_id"]]["label"] in ("CORRECT", "ERROR") and r.get("parse_ok") and r.get("cpu_status") == "OK"]
y = np.array([labels[r["item_id"]]["label"] == "ERROR" for r in prim])
model = pickle.load(open(ROOT / "results" / "fusion_H_noleak.pkl", "rb"))
feats = json.loads((ROOT / "prereg.json").read_text())["fusion_features"]
X = np.array([[float(r.get(f) or 0.0) for f in feats] for r in prim])
p_re = model.predict_proba(X)[:, 1]
stored = np.array([r["p_fused_H"] for r in prim])
out = {"n_primary": len(prim), "n_error": int(y.sum()), "n_correct": int((~y).sum()),
       "max_abs_diff_repredicted_vs_stored_p_fused": float(np.abs(p_re - stored).max())}
scores = {
    "p_fused_H(re-predicted)": p_re,
    "l2_bow(raw fields)": np.array([(r.get("bow_n_unanch") or 0) + (r.get("bow_uncarried") or 0) for r in prim]),
    "l3_score": np.array([r["l3_score"] for r in prim]),
    "l1_any": np.array([r["l1_any"] for r in prim]),
}
for k, s in scores.items():
    out[f"AUROC {k}"] = round(rank_auc(s[y], s[~y]), 4)
rng = np.random.default_rng(123)
plac = {k: [] for k in scores}
pdelta = []
for _ in range(200):
    yp = rng.permutation(y)
    for k, s in scores.items():
        plac[k].append(rank_auc(s[yp], s[~yp]))
    pdelta.append(rank_auc(scores["p_fused_H(re-predicted)"][yp], scores["p_fused_H(re-predicted)"][~yp])
                  - rank_auc(scores["l2_bow(raw fields)"][yp], scores["l2_bow(raw fields)"][~yp]))
for k in scores:
    a = np.array(plac[k])
    out[f"PLACEBO permuted-label AUROC {k}: mean / 95% range"] = [round(a.mean(), 4), round(np.quantile(a, .025), 4), round(np.quantile(a, .975), 4)]
    out[f"PLACEBO p-value (observed vs permutation) {k}"] = float((a >= out[f"AUROC {k}"]).mean())
out["observed delta fused - l2_bow"] = round(out["AUROC p_fused_H(re-predicted)"] - out["AUROC l2_bow(raw fields)"], 4)
out["PLACEBO delta fused - l2_bow (permuted): mean / 95% range"] = [round(float(np.mean(pdelta)), 4), round(float(np.quantile(pdelta, .025)), 4), round(float(np.quantile(pdelta, .975)), 4)]
# coverage / parse rate from raw rows
out["track_L_parse_rate(raw)"] = round(sum(1 for r in L if r.get("parse_ok")) / len(L), 4)
out["track_L_UNPARSEABLE_labels(raw)"] = sum(1 for r in L if labels[r["item_id"]]["label"] == "UNPARSEABLE")
# fused FA on track-L CORRECT at the frozen no-leak threshold (from prereg)
thr = json.loads((ROOT / "prereg.json").read_text())["calibration"]["fused_threshold_noleak_OOF_10pctFA"]
out["fused FA on L CORRECT @prereg thr (re-predicted)"] = round(float((p_re[~y] > thr).mean()), 4)
out["fused TPR on L ERROR @prereg thr (re-predicted)"] = round(float((p_re[y] > thr).mean()), 4)
# spend from ledger
out["spend_usd(ledger sum)"] = round(sum(json.loads(l)["cost_usd"] for l in (ROOT / "cache" / "cost_ledger.jsonl").read_text().splitlines() if l.strip()), 4)
(ROOT / "results" / "audit_rederive.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
