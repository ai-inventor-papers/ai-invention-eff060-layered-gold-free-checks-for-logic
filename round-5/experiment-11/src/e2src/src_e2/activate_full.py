#!/usr/bin/env python3
"""After the pilot: write the FULL active E2 set (base 350/100/100 + the pre-registered L25 surplus if
pilot_projection.json says so; DT reserve only if the DT failure rate > 10%) to work/sentences_E2_active.json and
work/sentences.json (the file E's frozen scripts read). Pilot sentences keep pilot=True. Idempotent."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W = ROOT / "work"
pool = json.loads((W / "pool_E2.json").read_text())
proj = json.loads((ROOT / "pilot_projection.json").read_text())
pilot = {s["sentence_id"] for s in json.loads((W / "sentences_pilot.json").read_text())}
l25 = [r for r in pool["L25"] if r["l25_tier"] == "base"]
sur = [r for r in pool["L25"] if r["l25_tier"] == "surplus"][: proj.get("add_l25", 0)]
dt = [r for r in pool["DT"] if r["dt_tier"] == "base"]
act = pool["EXC"] + l25 + sur + dt
for r in act:
    r["pilot"] = r["sentence_id"] in pilot
(W / "sentences_E2_active.json").write_text(json.dumps(act, ensure_ascii=False, indent=1))
(W / "sentences.json").write_text(json.dumps(act, ensure_ascii=False, indent=1))
print(f"active: EXC {len(pool['EXC'])} L25 {len(l25)}+{len(sur)} surplus, DT {len(dt)}; pilot {sum(r['pilot'] for r in act)}")
