#!/usr/bin/env python3
"""Append one line per completed batch to <WS>/e2b/progress.jsonl: sentences completed (solver labels + panel stage 1
record) per word bin, generation rows / parse rate, spend per sentence by phase vs the $0.01182 projection.
Reads NO label value (only whether a sentence has a labels/panel record)."""
import argparse
import json
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WS = ROOT.parent


def jl(p):
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=int, required=True)
    a = ap.parse_args()
    sents = [s for s in json.loads((WS / "e2b" / "sentences_E2B.json").read_text()) if s["e2b_batch"] <= a.batch]
    ids = {s["sentence_id"] for s in sents}
    lab_ids = {r["sentence_id"] for r in jl(ROOT / "work" / "labels_heldout.jsonl")}
    pan_ids = {r["sentence_id"] for r in jl(ROOT / "work" / "panel_heldout.jsonl")}
    comp = [s for s in sents if s["sentence_id"] in lab_ids and s["sentence_id"] in pan_ids]
    gens = [g for g in jl(ROOT / "raw" / "generations.jsonl") if g["sentence_id"] in ids]
    by_phase = Counter()
    for r in jl(ROOT / "cost_ledger.jsonl"):
        by_phase[r.get("phase")] += r.get("cost_usd", 0.0)
    lab_spend = sum(v for k, v in by_phase.items() if k in ("generation", "panel_heldout", "panel_heldout_adj", "reference_repair"))
    rec = {"ts_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "batch": a.batch, "n_sentences_active": len(sents),
           "n_sentences_completed": len(comp), "completed_per_word_bin": dict(Counter(s["word_bin"] for s in comp)),
           "generation_rows": len(gens), "generation_parse_rate": round(sum(g["parse_ok"] for g in gens) / max(1, len(gens)), 4),
           "generation_final_failures": sum(g["raw_output"] is None for g in gens),
           "spend_by_phase": {k: round(v, 5) for k, v in by_phase.items()},
           "label_pipeline_spend_per_completed_sentence": round(lab_spend / max(1, len(comp)), 5), "projection_per_sentence": 0.01182}
    with open(WS / "e2b" / "progress.jsonl", "a") as f:
        f.write(json.dumps(rec) + "\n")
    print(json.dumps(rec))
