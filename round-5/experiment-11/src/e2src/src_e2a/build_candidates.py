#!/usr/bin/env python3
"""E2-A: LABEL-FREE candidate rows for scoring -> ../e2/candidates_E2_nolabels.jsonl

Reads ONLY raw/generations.jsonl (generator outputs; the later record of a duplicate key wins, as in E's assemble) and
work/sentences_E2_active.json (sentence text + text-level strata). Writes no label, no reference formula, no
gold-derived feature (n_conditions / n_quant / depth are joined at analysis time from the sentence file), and no
gold-as-system row. item_id is E's frozen formula sha1(system|norm_screen(text)|raw_output)[:16]; row_key =
item_id|prompt_variant, the key of sealed/labels_E2.jsonl.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WS = ROOT.parent
FAM = {"G1": "meta", "G1b": "meta", "G2": "qwen", "G3": "mistral", "G4": "deepseek", "G5": "google", "G8": "google",
       "G6": "microsoft", "G7": "openai", "G9": "cohere"}  # exp-5 prereg family_map_vendor (frozen)
SLOTS = ["G1", "G1b", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9"]


def norm_screen(t: str) -> str:  # byte-identical to src/screen.py
    t = t.lower().replace("’", "").replace("'", "").replace("‘", "")
    t = re.sub(r"[^\w\s]", "", t)
    return re.sub(r"\s+", " ", t).strip()


def main() -> None:
    act = json.loads((ROOT / "work" / "sentences_E2_active.json").read_text())
    by_sid = {s["sentence_id"]: s for s in act}
    gens = {}
    for line in (ROOT / "raw" / "generations.jsonl").read_text().splitlines():
        if not line.strip():
            continue
        g = json.loads(line)
        if g.get("sentence_id") in by_sid and g.get("prompt_variant") == "fewshot_v1":
            gens[(g["sentence_id"], g["slot"])] = g
    rows, missing = [], []
    for s in act:
        for slot in SLOTS:
            g = gens.get((s["sentence_id"], slot))
            if g is None:
                missing.append((s["sentence_id"], slot))
                continue
            raw = (g.get("raw_output") or "").strip()  # E assemble.py:200 strips raw before item_id
            iid = hashlib.sha1((g["system"] + "|" + norm_screen(s["text"]) + "|" + raw).encode()).hexdigest()[:16]
            rows.append({
                "row_key": f"{iid}|fewshot_v1", "item_id": iid, "sentence_id": s["sentence_id"], "text": s["text"],
                "slot": slot, "system": g["system"], "model": g["model"], "family": FAM[slot],
                "family_field": g.get("family"), "prompt_variant": "fewshot_v1", "candidate_fol": g.get("candidate_fol") or "",
                "raw_output": raw, "parse_ok_gen": g.get("parse_ok"), "gen_cost_usd": g.get("cost_usd") or 0.0,
                "stratum": s["source_stratum"], "words": s["words"], "text_conditions": s.get("text_conditions"),
                "exception_type": s.get("exception_type"), "word_bin": s.get("word_bin"), "pilot": bool(s.get("pilot")),
                "source_dataset": s["source_dataset"]})
    out = WS / "e2" / "candidates_E2_nolabels.jsonl"
    out.parent.mkdir(exist_ok=True)
    out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    assert len({r["row_key"] for r in rows}) == len(rows), "duplicate row_key"
    print(json.dumps({"rows": len(rows), "sentences": len({r['sentence_id'] for r in rows}), "missing_slots": len(missing),
                      "missing_examples": missing[:5]}))


if __name__ == "__main__":
    main()
