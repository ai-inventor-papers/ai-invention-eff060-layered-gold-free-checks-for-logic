#!/usr/bin/env python3
"""STEP I: full_data_out.json (exp_sel_data_out) with three groups:
  rcomp_free_labels     one row per FREE generation record (2,652), label = name-free label (search-only now, D9)
  gloss_gate_items      840 known-answer (symbol use, meaning) items, 7 classes, halves A/B
  sig_soundness_replay  4,280 rows = 2,140 SIG rows x {nonce, synonym} renames, output = known pure-z3 SIG label
"""
from __future__ import annotations

import json

from common import RES, ROOT, WORK, load_jsonl, setup_logger

logger = setup_logger("build_output")


def md(d: dict) -> dict:
    return {f"metadata_{k}": v for k, v in d.items()}


def free_group() -> dict:
    rows = load_jsonl(RES / "free_labels_v2.jsonl")
    ex = []
    for r in rows:
        inp = {"text": r["text"], "candidate_fol": r["candidate_fol"], "system": r["system"], "family": r["family"],
               "slot": r["slot"], "prompt_variant": r["prompt_variant"], "condition": "FREE", "template_id": r["template_id"]}
        search_bin = {"ERROR_CERT": "ERROR", "UNRESOLVED_GLOSS_NOT_RUN": "MAPPED"}.get(r["label"], "EXCLUDED")
        meta = {
            "row_key": r["row_key"], "item_id": r["item_id"], "sentence_id": r["sentence_id"], "template_id": r["template_id"],
            "clause_type": r["clause_type"], "words": r["words"], "word_tercile": r["word_tercile"],
            "nconds_weak": r["nconds_weak"], "negated_condition": r["negated_condition"], "nested": r["nested"],
            "label_binary": r["label_binary"], "label_binary_search_provisional": search_bin,
            "label_source": r["label_source"], "search_status": r.get("search_status"),
            "matched_reading": r.get("matched_reading") or r.get("matched_reading_search"),
            "map_certificate": r.get("map_certificate"),
            "n_maps_enumerated": r.get("n_maps_enumerated"), "n_maps_fingerprint_pass": r.get("n_maps_fingerprint_pass"),
            "n_equiv_maps": r.get("n_equiv_maps"), "n_equiv_map_orbits": r.get("n_equiv_map_orbits"),
            "nonequiv_certificate_type_counts": r.get("nonequiv_certificate_type_counts"),
            "gloss_pairs": r.get("gloss_pairs"), "gloss_decision": r.get("gloss_decision"),
            "unresolved_reason": r.get("unresolved_reason"), "irrelevant_symbols": r.get("irrelevant_symbols"),
            "search_secs": r.get("search_secs"), "seen_iter3": r.get("seen_iter3"),
            "old_label_iter3": r.get("old_label_iter3"), "fold": "RCOMP_FREE"}
        ex.append({"input": json.dumps(inp, ensure_ascii=False), "output": r["label"], **md(meta)})
    return {"dataset": "rcomp_free_labels", "examples": ex}


def gate_group() -> dict:
    items = json.loads((RES / "gate_items.json").read_text())
    ex = []
    for i in items:
        inp = {"sentence": i["sentence"], "candidate_atom": i["candidate_atom"], "proposed_meaning": i["proposed_meaning"]}
        meta = {"item_id": i["item_id"], "class": i["class"], "half": i["half"], "sentence_id": i["sentence_id"],
                "template_id": i["template_id"], "note": i["note"], "prompt_version": "gloss_v1",
                "haiku_verdict": i.get("haiku_gloss_v1"), "qwen_verdict": i.get("qwen_gloss_v1"), "fold": "GLOSS_GATE"}
        ex.append({"input": json.dumps(inp, ensure_ascii=False), "output": i["gold"], **md(meta)})
    return {"dataset": "gloss_gate_items", "examples": ex}


def sig_group() -> dict:
    sents = json.loads((WORK / "sentences.json").read_text())
    rows = load_jsonl(RES / "sig_replay_rows.jsonl")
    ex = []
    for r in rows:
        inp = {"text": sents[r["sentence_id"]]["text"], "candidate_fol": r["renamed_fol"], "rename": r["rename"],
               "template_id": r["template_id"]}
        meta = {k: r[k] for k in ("row_key", "sentence_id", "slot", "template_id", "sig_matched_reading", "canon_fol",
                                  "search_status", "identity_map_found", "non_identity_map_found", "n_equiv_maps",
                                  "n_equiv_map_orbits", "n_maps_enumerated", "nonequiv_certificate_type_counts",
                                  "oracle_end_to_end_label", "in_e2e_gloss_subsample_300", "e2e_gloss_label")}
        meta["map_equiv_found"] = r["search_status"] in ("MAPPED", "READING_CHOICE")
        meta["fold"] = f"SIG_REPLAY_{r['rename'].upper()}"
        ex.append({"input": json.dumps(inp, ensure_ascii=False), "output": r["sig_label"], **md(meta)})
    return {"dataset": "sig_soundness_replay", "examples": ex}


def main() -> None:
    seal = json.loads((RES / "seal.json").read_text())["seals"]
    t = json.loads((RES / "testability_FREE_v2.json").read_text())
    out = {"metadata": {
        "artifact": "T7b name-free labels for free-vocabulary rule translations (run_u75jRHUss0zo, iter 4, gen_art_dataset_5)",
        "workspace": str(ROOT),
        "label_mode": seal[-1]["mode"],
        "status_note": ("SEARCH-ONLY labels: the paid gloss step could not run (deviation D9: run OpenRouter budget "
                        "exhausted before this artifact's first call). ERROR_CERT is final and certificate-backed; MAPPED rows "
                        "are UNRESOLVED_GLOSS_NOT_RUN until src/resume_gloss.py runs. metadata_label_binary_search_provisional "
                        "(ERROR vs MAPPED) is a provisional view with audited contamination (see results/soundness_audit.json)."),
        "seal_all_rows_sha256": seal[-1]["label_vector_sha256_all_rows"],
        "seal_untouched_sha256": seal[-1].get("label_vector_sha256_untouched"),
        "prereg_sha256": seal[-1]["prereg_sha256"],
        "testability_all_rows": {k: t["all_rows"][k] for k in ("n_ERROR", "n_CORRECT", "TESTABLE", "label_counts")},
        "testability_untouched": {k: t["untouched_subset"][k] for k in ("n_ERROR", "n_CORRECT", "TESTABLE", "label_counts")}
        if isinstance(t.get("untouched_subset"), dict) else None,
    }, "datasets": [free_group(), gate_group(), sig_group()]}
    (ROOT / "full_data_out.json").write_text(json.dumps(out, ensure_ascii=False))
    logger.info(f"full_data_out.json: {[(d['dataset'], len(d['examples'])) for d in out['datasets']]}")


if __name__ == "__main__":
    main()
