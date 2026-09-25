#!/usr/bin/env python3
"""Estimate the $ cost of the next 50-sentence batch from actuals (label-pipeline spend per completed sentence x 50 x 1.2);
before any batch completes: the E-measured projection 50 x $0.01182 (pilot_projection.json). Prints a float."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WS = ROOT.parent
PHASES = ("generation", "panel_heldout", "panel_heldout_adj", "reference_repair")
prog = WS / "e2b" / "progress.jsonl"
done = [json.loads(l) for l in prog.read_text().splitlines() if l.strip()] if prog.exists() else []
if not done:
    print(round(50 * 0.01182, 4))
else:
    spent = 0.0
    for line in (ROOT / "cost_ledger.jsonl").read_text().splitlines():
        if line.strip():
            r = json.loads(line)
            if r.get("phase") in PHASES:
                spent += r.get("cost_usd", 0.0)
    n = done[-1]["n_sentences_completed"]
    print(round(spent / max(1, n) * 50 * 1.2, 4))
