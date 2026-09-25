#!/usr/bin/env python3
"""STEP 2c REGRESSION GATE: re-derived c_align / c_nf (and g_align / g_nf, ALIGN-map c) vs exp 5 frozen per_item_E columns.
Label-free (reads only exp 5 score columns). Writes results/regression_gate.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import tasks as TK  # noqa: E402

PAIRS = [("c_align", "c_score_align"), ("c_nf", "nf_c_score"), ("g_align", "g_score"), ("g_nf", "nf_g_score"),
         ("c_align_graded_map", "c_score_nf")]


def main(write: bool = True) -> dict:
    fz = {r["row_key"]: r for r in TK.jl(ROOT / "data/exp5/per_item_E.jsonl")}
    ours = {}
    for s in TK.jl(ROOT / "results/scores_E.jsonl"):
        for r in s["rows"]:
            if r["key"] in fz:
                ours[r["key"]] = r
    out = {"n_rows_compared": len(ours)}
    for a, b in PAIRS:
        n = m = 0
        bad = []
        for k, r in ours.items():
            x, y = r.get(a), fz[k].get(b)
            if x is None and y is None:
                n += 1
                continue
            n += 1
            if x is None or y is None or abs(x - y) > 1e-9:
                m += 1
                if len(bad) < 40:
                    bad.append({"row_key": k, "ours": x, "frozen": y, "n_unknown_align": r.get("n_unknown_align"),
                                "n_unknown_nf": r.get("n_unknown_nf")})
        out[f"{a}_vs_{b}"] = {"n": n, "mismatch": m, "match_rate": 1 - m / max(1, n), "examples": bad}
    out["gate_pass"] = all(out[f"{a}_vs_{b}"]["match_rate"] >= 0.99 for a, b in PAIRS[:2])
    if write:
        (ROOT / "results/regression_gate.json").write_text(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    o = main()
    print(json.dumps({k: (v if not isinstance(v, dict) else {kk: vv for kk, vv in v.items() if kk != "examples"}) for k, v in o.items()}, indent=1))
