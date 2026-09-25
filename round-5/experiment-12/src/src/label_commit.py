#!/usr/bin/env python3
"""$ still committed to the E2-B label batches (labels are LAST in the shrink order, so judge sweeps keep this out of
their budget): (8 - completed batches) x next-batch estimate (actuals when available). Prints a float."""
import json
import subprocess
from pathlib import Path

WS = Path(__file__).resolve().parents[1]
prog = WS / "e2b" / "progress.jsonl"
done = len([l for l in prog.read_text().splitlines() if l.strip()]) if prog.exists() else 0
est = float(subprocess.run([str(WS / "e2bsrc/.venv/bin/python"), str(WS / "e2bsrc/src_e2b/batch_estimate.py")], capture_output=True, text=True).stdout.strip())
print(round(max(0, 8 - done) * est, 4))
