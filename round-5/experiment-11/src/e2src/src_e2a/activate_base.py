#!/usr/bin/env python3
"""E2-A copy of src_e2/activate_full.py with the L25 SURPLUS NOT activated (deviation D-SURPLUS: sibling E2-B claims
the 98 surplus sentences). Base 350/100/100 exactly as frozen; pilot sentences keep pilot=True. Idempotent."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W = ROOT / "work"
pool = json.loads((W / "pool_E2.json").read_text())
pilot = {s["sentence_id"] for s in json.loads((W / "sentences_pilot.json").read_text())}
l25 = [r for r in pool["L25"] if r["l25_tier"] == "base"]
dt = [r for r in pool["DT"] if r["dt_tier"] == "base"]
act = pool["EXC"] + l25 + dt
for r in act:
    r["pilot"] = r["sentence_id"] in pilot
(W / "sentences_E2_active.json").write_text(json.dumps(act, ensure_ascii=False, indent=1))
(W / "sentences.json").write_text(json.dumps(act, ensure_ascii=False, indent=1))
print(f"active: EXC {len(pool['EXC'])} L25 {len(l25)} (surplus not activated), DT {len(dt)}; pilot {sum(r['pilot'] for r in act)}")
