#!/usr/bin/env python3
"""E2 STEP 10: label seal.

  sealed/labels_E2.jsonl        row_key -> {label, label_tier, reference_status, correct_not_equivalent, reading_choice,
                                 vex, vex_eq, auto_label, repair_ops, error_ops, panel_votes, system_class}
                                 (LLM rows AND gold-as-system rows; the gold rows are sealed too)
  sealed/references_E2.jsonl    sentence_id -> {reference_fol, reference_status, gold_fol}
  candidates_E2_nolabels.jsonl  every LLM candidate row: text, candidate_fol, system, slot, family, prompt_variant,
                                 strata, disguised text/fol, parse status (parser only), cost, provider. NO label, NO
                                 reference, NO label-derived field (class ids, equivalence status, repair ops,
                                 convention flags, panel fields), NO gold-as-system row.
  controls_E2_nolabels.jsonl    control rows without output / label fields.
  seal.json                     sha256 of each file + prereg sha + code_freeze sha + UTC time.
Iteration 5 freezes and hashes its metric scores on candidates_E2_nolabels.jsonl BEFORE joining sealed/labels_E2.jsonl.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W = ROOT / "work"
SEALED = ROOT / "sealed"
NOLABEL_KEYS = ["row_key", "item_id", "sentence_id", "text", "candidate_fol", "raw_output", "system", "slot", "family", "model",
                "model_returned_provider", "prompt_variant", "fold", "strata", "disguised_text", "disguised_fol", "parse_ok",
                "cost_usd", "finish_reason", "pilot"]
FORBIDDEN = ["label", "final_label", "output", "label_tier", "reference_fol", "reference", "gold_fol", "reference_status", "auto_label",
             "equiv_status", "repair_ops", "repair_status", "error_ops", "panel_votes", "panel_item", "panel_ambiguous", "class_id",
             "class_size", "convention_flags", "correct_not_equivalent", "reading_choice", "vex", "vex_eq", "gold_audit_flag",
             "label_source", "addrop_only_suspect", "solver_lenient_label", "control_type_label"]


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write_jsonl(p: Path, rows: list[dict]) -> None:
    with open(p, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")


def main():
    SEALED.mkdir(exist_ok=True)
    d = json.loads((W / "assembled_E2.json").read_text())
    g = {x["dataset"]: x["examples"] for x in d["datasets"]}
    labels, nolab = [], []
    for r in g["e2_candidates"] + g["e2_gold_as_system"]:
        labels.append({"row_key": r["metadata_row_key"], "system_class": r["metadata_system_class"], "label": r["output"],
                       "label_tier": r["metadata_label_tier"], "reference_status": r["metadata_reference_status"],
                       "correct_not_equivalent": r["metadata_correct_not_equivalent"], "reading_choice": r["metadata_reading_choice"],
                       "vex": r.get("metadata_vex"), "vex_eq": r.get("metadata_vex_eq"), "auto_label": r["metadata_auto_label"],
                       "repair_ops": r["metadata_repair_ops"], "error_ops": r["metadata_error_ops"], "panel_votes": r["metadata_panel_votes"]})
    for r in g["e2_candidates"]:
        inp = json.loads(r["input"])
        nolab.append({"row_key": r["metadata_row_key"], "item_id": r["metadata_item_id"], "sentence_id": r["metadata_sentence_id"],
                      "text": inp["text"], "candidate_fol": inp["candidate_fol"], "raw_output": r["metadata_raw_output"],
                      "system": r["metadata_system"], "slot": r["metadata_slot"], "family": r["metadata_family"],
                      "model": r["metadata_generator_model_id"], "model_returned_provider": r["metadata_provider"],
                      "prompt_variant": r["metadata_prompt_variant"], "fold": r["metadata_fold"],
                      "strata": {k: v for k, v in r["metadata_strata"].items()}, "disguised_text": r["metadata_disguised_text"],
                      "disguised_fol": r["metadata_disguised_fol"], "parse_ok": r["output"] != "UNPARSEABLE",
                      "cost_usd": r["metadata_cost_usd"], "finish_reason": r["metadata_finish_reason"], "pilot": r["metadata_pilot"]})
    refs = []
    for s in g["e2_sentences"]:
        inp = json.loads(s["input"])
        refs.append({"sentence_id": s["metadata_sentence_id"], "reference_fol": inp["reference_fol"], "reference_status": s["output"],
                     "gold_fol": s["metadata_original_reference_fol"]})
    ctrl = json.loads((W / "controls_E2.json").read_text())["rows"] if (W / "controls_E2.json").exists() else []
    ctrl_nolab = [{"row_key": c["metadata_row_key"], "sentence_id": c["metadata_sentence_id"], "text": json.loads(c["input"])["text"],
                   "candidate_fol": json.loads(c["input"])["candidate_fol"], "system": c["metadata_system"], "family": c["metadata_family"],
                   "fold": "E2_CONTROL", "control_parent_row_key": c["metadata_control_parent_row_key"], "strata": c["metadata_strata"]}
                  for c in ctrl]
    files = {"sealed/labels_E2.jsonl": labels, "sealed/references_E2.jsonl": refs,
             "candidates_E2_nolabels.jsonl": nolab, "controls_E2_nolabels.jsonl": ctrl_nolab}
    for rel, rows in files.items():
        write_jsonl(ROOT / rel, rows)
    seal = {"sealed_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "files": {rel: {"sha256": sha256(ROOT / rel), "n_rows": len(rows)} for rel, rows in files.items()},
            "prereg_E2.json_sha256": sha256(ROOT / "prereg_E2.json"), "code_freeze.json_sha256": sha256(ROOT / "code_freeze.json"),
            "forbidden_keys_in_nolabel_files": FORBIDDEN,
            "protocol": "iteration 5 freezes and hashes its metric scores on candidates_E2_nolabels.jsonl (and controls_E2_nolabels.jsonl) BEFORE joining sealed/labels_E2.jsonl by row_key; verify with `.venv/bin/python src_e2/verify_seal.py`"}
    (ROOT / "seal.json").write_text(json.dumps(seal, indent=1))
    print(json.dumps(seal["files"]))


if __name__ == "__main__":
    main()
