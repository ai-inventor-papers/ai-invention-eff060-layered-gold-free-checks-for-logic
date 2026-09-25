#!/usr/bin/env python3
"""POST-HOC AUDIT: re-derive headline numbers through a minimal independent sklearn/numpy path and compare (1e-9):
  (1) E R_AB pooled stratified AUROC of c_hyb and c_align and their difference (analysis_hyb.json);
  (2) three PERTURB recall cells (perturb_sensitivity.csv, subset E_bases, polarity ALL) from perturb_scores.jsonl;
  (3) every paired comparison used identical n. Writes results/audit_rederive.json."""
import csv
import json
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parent.parent
R = ROOT / "results"
out = {}
A = json.loads((R / "analysis_hyb.json").read_text())
rows = [json.loads(l) for l in (R / "per_item_hyb_E.jsonl").read_text().splitlines()]
rows = [r for r in rows if r["y_AB"] is not None]


def strat(m):
    num = den = 0.0
    for s in sorted({r["stratum"] for r in rows}):
        rr = [r for r in rows if r["stratum"] == s]
        y = np.array([r["y_AB"] for r in rr])
        n1, n0 = y.sum(), len(y) - y.sum()
        num += roc_auc_score(y, [r[m] for r in rr]) * n1 * n0
        den += n1 * n0
    return num / den


ev = A["E"]["R_AB pooled"]
d = strat("c_hyb") - strat("c_align")
out["E_strat_delta_hyb_minus_align"] = {"rederived": d, "reported": ev["paired"]["c_hyb - c_align"]["delta_strat_auroc"],
                                        "match_1e-9": abs(d - ev["paired"]["c_hyb - c_align"]["delta_strat_auroc"]) < 1e-9,
                                        "n_rederived": len(rows), "n_reported": ev["n"], "same_n": len(rows) == ev["n"]}
pp = json.loads((R / "prereg_perturb.json").read_text())["thresholds_primary"]
PS = [json.loads(l) for l in (R / "perturb_scores.jsonl").read_text().splitlines()]
sens = list(csv.DictReader((R / "perturb_sensitivity.csv").open()))
cells = []
for m, op in (("c_hyb", "NEG"), ("l2_bow", "MEANING_RENAME"), ("judge_cheap_disg", "SWAP")):
    t, lam = pp[m]["t"], pp[m]["lambda"]
    v = np.array([u[m] for u in PS if u["y"] == 1 and u["operator"] == op and not u["is_rcomp"] and u.get(m) is not None], float)
    rec = float(np.mean(np.where(v > t, 1.0, np.where(v == t, lam, 0.0))))
    rep = next(float(r["recall_primary"]) for r in sens if r["metric"] == m and r["operator"] == op and r["polarity"] == "ALL" and r["subset"] == "E_bases")
    nrep = next(int(r["n"]) for r in sens if r["metric"] == m and r["operator"] == op and r["polarity"] == "ALL" and r["subset"] == "E_bases")
    cells.append({"metric": m, "operator": op, "rederived": rec, "reported": rep, "match_1e-9": abs(rec - rep) < 1e-9, "n": len(v), "same_n": len(v) == nrep})
out["perturb_recall_cells"] = cells
same_n = all(p["n"] == ev["n"] for p in ev["paired"].values())
out["E_paired_same_n"] = same_n
out["all_pass"] = out["E_strat_delta_hyb_minus_align"]["match_1e-9"] and all(c["match_1e-9"] and c["same_n"] for c in cells) and same_n
(R / "audit_rederive.json").write_text(json.dumps(out, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
print(json.dumps(out, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o)))
