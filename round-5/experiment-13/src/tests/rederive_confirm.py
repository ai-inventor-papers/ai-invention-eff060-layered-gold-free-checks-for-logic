#!/usr/bin/env python3
"""Independent re-derivation (testing plan item 13), written WITHOUT auc_tools / analysis_lib: recompute from
results/per_item_rcomp_free.jsonl the headline within-template AUROCs of c_score_align, judge_cheap_disg and
judge_cheap_orig (PROVISIONAL view: untouched, ERROR_CERT vs MAPPED, per-view scored rows) and both deltas by
brute-force pair counting; they must match results/analysis_rcomp.json to 1e-9. Also re-checks the confirmatory count
(0 CORRECT). Writes results/rederive_check.json."""
import json
from collections import defaultdict
from pathlib import Path

WS = Path(__file__).resolve().parents[1]


def within_template_auc(rows, key):
    by = defaultdict(lambda: ([], []))
    for r in rows:
        (by[r["template_id"]][0] if r["y"] == 1 else by[r["template_id"]][1]).append(r[key])
    U = P = 0.0
    for pos, neg in by.values():
        if not pos or not neg:
            continue
        for p in pos:
            for q in neg:
                U += 1.0 if p > q else (0.5 if p == q else 0.0)
        P += len(pos) * len(neg)
    return U / P


def main():
    items = [json.loads(l) for l in (WS / "results/per_item_rcomp_free.jsonl").read_text().splitlines() if l.strip()]
    A = json.loads((WS / "results/analysis_rcomp.json").read_text())
    out = {}
    for view, j in (("disg", "judge_cheap_disg"), ("orig", "judge_cheap_orig")):
        rows = [r for r in items if r["untouched"] and r["y"] is not None and r["c_score_align"] is not None and r[j] is not None]
        a, b = within_template_auc(rows, "c_score_align"), within_template_auc(rows, j)
        h = A["provisional_headline"][view]
        out[view] = {"n": len(rows), "auroc_c_align": a, "auroc_judge": b, "delta": a - b,
                     "match_1e-9": abs(a - h["auroc_a"]) < 1e-9 and abs(b - h["auroc_b"]) < 1e-9 and abs((a - b) - h["delta"]) < 1e-9 and len(rows) == h["n"]}
    n_cor = sum(1 for r in items if r["untouched"] and r["label_binary"] == "CORRECT")
    out["confirmatory_n_CORRECT_untouched"] = n_cor
    out["PASS"] = bool(out["disg"]["match_1e-9"] and out["orig"]["match_1e-9"] and n_cor == A["confirmatory"]["disg"]["n_CORRECT"])
    (WS / "results/rederive_check.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))
    assert out["PASS"]


if __name__ == "__main__":
    main()
