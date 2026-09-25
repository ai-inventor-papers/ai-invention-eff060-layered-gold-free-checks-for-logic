#!/usr/bin/env python3
"""T8: independent re-derivation of the primary within-template AUROCs and delta (sklearn roc_auc_score per template,
weighted by the number of ERROR x CORRECT pairs), compared with results/analysis.json to 1e-9. Also re-checks the
label-shuffle and within-sentence score-shuffle placebos with independent code. Writes results/audit_rederive.json.
usage: .venv/bin/python tests/audit_rederive.py"""
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"


def within(rows, key):
    by = defaultdict(list)
    for r in rows:
        by[r["template_id"]].append(r)
    num = den = 0.0
    for t, rs in by.items():
        y = np.array([r["label"] == "ERROR" for r in rs])
        if y.all() or (~y).all():
            continue
        pairs = y.sum() * (~y).sum()
        num += roc_auc_score(y, [r[key] for r in rs]) * pairs
        den += pairs
    return num / den


def main():
    A = json.loads((RES / "analysis.json").read_text())["SIG"]
    rows = [json.loads(l) for l in (RES / "analysis_rows_SIG.jsonl").read_text().splitlines() if l.strip()]
    pool = [r for r in rows if r["label"] in ("CORRECT", "ERROR") and r["c_score_sig"] is not None and r["judge_cheap_disg"] is not None]
    a1, a2 = within(pool, "c_score_sig"), within(pool, "judge_cheap_disg")
    p = A["primary"]
    out = {"n": len(pool), "auroc_c_score_sig": a1, "auroc_judge_cheap_disg": a2, "delta": a1 - a2,
           "analysis_auroc_c_score_sig": p["auroc_metric"], "analysis_auroc_judge": p["auroc_comparator"], "analysis_delta": p["delta"],
           "n_match": len(pool) == p["n"]}
    out["match_1e-9"] = bool(abs(a1 - p["auroc_metric"]) < 1e-9 and abs(a2 - p["auroc_comparator"]) < 1e-9 and out["n_match"])
    rng = np.random.default_rng(7)
    lab = [r["label"] for r in pool]
    shuf = [dict(r, label=l) for r, l in zip(pool, rng.permutation(lab))]
    out["label_shuffle_auroc_c_score_sig"] = within(shuf, "c_score_sig")
    by = defaultdict(list)
    for i, r in enumerate(pool):
        by[r["sentence_id"]].append(i)
    s1 = [dict(r) for r in pool]
    for idx in by.values():
        perm = rng.permutation(idx)
        for i, j in zip(idx, perm):
            s1[i]["c_score_sig"] = pool[j]["c_score_sig"]
            s1[i]["judge_cheap_disg"] = pool[int(rng.choice(idx))]["judge_cheap_disg"]
    num = den = 0.0
    for idx in by.values():
        y = np.array([s1[i]["label"] == "ERROR" for i in idx])
        if y.all() or (~y).all():
            continue
        pairs = y.sum() * (~y).sum()
        num += (roc_auc_score(y, [s1[i]["c_score_sig"] for i in idx]) - roc_auc_score(y, [s1[i]["judge_cheap_disg"] for i in idx])) * pairs
        den += pairs
    out["within_sentence_score_shuffle_delta"] = num / den
    (RES / "audit_rederive.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))
    return 0 if out["match_1e-9"] else 1


if __name__ == "__main__":
    sys.exit(main())
