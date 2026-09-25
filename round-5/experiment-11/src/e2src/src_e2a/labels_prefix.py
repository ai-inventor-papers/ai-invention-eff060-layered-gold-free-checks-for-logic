#!/usr/bin/env python3
"""Write work/labels_heldout_prefix.jsonl = the solver-label records of the first N sentences of the frozen sha1 order
(work/e2a_order.json from order.py). panel_run.py --labels reads it, so the panel runs in completed sha1 prefixes while
work/sentences.json keeps all 550 active sentences. Reads no label VALUE: records are copied verbatim by sentence_id."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
W = ROOT / "work"
order = json.loads((W / "e2a_order.json").read_text())
n = int(sys.argv[1])
keep = set(order[:n])
lines = [l for l in (W / "labels_heldout.jsonl").read_text().splitlines() if l.strip() and json.loads(l)["sentence_id"] in keep]
(W / "labels_heldout_prefix.jsonl").write_text("\n".join(lines) + "\n")
print(f"labels prefix: {len(lines)} records for {len(keep)} sentences")
