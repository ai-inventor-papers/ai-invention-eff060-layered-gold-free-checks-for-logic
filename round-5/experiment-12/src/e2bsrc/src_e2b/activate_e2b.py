#!/usr/bin/env python3
"""Point E2's frozen scripts at E2-B: writes work/batch_<b>.json for every batch and work/sentences.json +
work/sentences_E2_active.json = the CUMULATIVE set of batches 1..B (the file E's frozen scripts read).
Usage: activate_e2b.py --upto B"""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WS = ROOT.parent
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--upto", type=int, required=True)
    a = ap.parse_args()
    sents = json.loads((WS / "e2b" / "sentences_E2B.json").read_text())
    for b in range(1, 9):
        (ROOT / "work" / f"batch_{b}.json").write_text(json.dumps([s for s in sents if s["e2b_batch"] == b], ensure_ascii=False, indent=1))
    act = [s for s in sents if s["e2b_batch"] <= a.upto]
    for s in act:
        s["pilot"] = False
        if s.get("e2_rank") is None:  # continuation rows: their rank in E2's continued L25 order (surplus = 350..447)
            s["e2_rank"] = 448 + (s["e2b_rank"] - 98)
    for n in ("sentences.json", "sentences_E2_active.json"):
        (ROOT / "work" / n).write_text(json.dumps(act, ensure_ascii=False, indent=1))
    print(f"active E2-B batches 1..{a.upto}: {len(act)} sentences")
