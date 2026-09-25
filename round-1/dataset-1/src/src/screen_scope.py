#!/usr/bin/env python3
"""STEP 6b panel scope: screen sentences having any VOCAB_GRAN/COMPOUND/TIMEOUT_UNKNOWN class, plus a 20% sha1 sample
of the remaining sentences (track L only; track H pairs are covered by the 4c real-error check). -> work/screen_panel_scope.json"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
labs = [json.loads(l) for l in open(ROOT / "work" / "labels_screen.jsonl") if l.strip()]
items = json.loads((ROOT / "work" / "screen_items.json").read_text())
track = {i["screen_sentence_id"]: i["track"] for i in items}
unc, rest = [], []
for r in labs:
    if track.get(r["sentence_id"]) != "L":
        continue
    if any(c.get("auto_label") in ("VOCAB_GRAN", "COMPOUND", "TIMEOUT_UNKNOWN") for c in r["classes"]):
        unc.append(r["sentence_id"])
    else:
        rest.append(r["sentence_id"])
samp = [s for s in rest if int(hashlib.sha1(("scope|" + s).encode()).hexdigest()[:8], 16) % 5 == 0]
(ROOT / "work" / "screen_panel_scope.json").write_text(json.dumps(sorted(unc + samp)))
print(f"uncertain {len(unc)} + sample {len(samp)}/{len(rest)}")
