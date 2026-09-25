#!/usr/bin/env python3
"""method_out.json (aii exp_gen_sol_out) from analysis/per_item_E2B.jsonl + scores/controls_scores_E2B.jsonl.

dataset 'E2B_L25_candidates': one example per E2-B LLM candidate row. input = JSON{text, candidate_fol, system};
output = the final label (CORRECT / ERROR / CONTESTED / UNRESOLVED / UNPARSEABLE). predict_<metric> = the oriented score
as a string (higher = more likely unfaithful; '' when the metric is missing): V0 (PRIMARY c_score_align), p_peer_text,
V1-V5, c_exact, the judges (flash-lite disguised/original, nano, cost-matched deepseek-v3.2 disguised/original, frontier
gemini-3.1-pro-preview original on the subsample) and the S4 stacks. metadata_* = stratum, word bin, words, n_conditions,
tier, R_AB flag, sample, slot, family, fold, frontier inclusion probability.
dataset 'E2B_rename_controls': one example per RENAME_SYN / RENAME_NONCE control (output CORRECT by construction),
predict_V0_control and predict_V0_parent."""
from __future__ import annotations

import json
from pathlib import Path

WS = Path(__file__).resolve().parents[1]
PRED = ["V0", "p_peer_text", "V1", "V2", "V3", "V4", "V5", "c_exact", "flashlite_disg", "flashlite_orig", "nano_orig", "nano_disg",
        "costmatched_disg", "costmatched_orig", "frontier_orig", "S4_E2B", "S4_E2B_plus_V0"]
META = ["row_key", "e2_row_key", "sentence_id", "sample", "stratum", "word_bin", "words", "n_conditions", "n_quant", "depth", "e2b_batch",
        "e2b_origin", "slot", "family", "fold_E2", "tier", "reading_choice", "in_R_AB", "in_R_A", "auto_label", "error_ops",
        "correct_not_equivalent", "label_regime", "coverage_status", "in_frontier_subsample", "frontier_inclusion_prob"]


def s(v) -> str:
    return "" if v is None else (f"{v:.6g}" if isinstance(v, float) else str(v))


def main():
    rows = [json.loads(l) for l in (WS / "analysis" / "per_item_E2B.jsonl").read_text().splitlines() if l.strip()]
    srows = {json.loads(l)["row_key"]: json.loads(l) for l in (WS / "scores" / "rows_E2B.jsonl").read_text().splitlines() if l.strip()}
    ex = []
    for r in rows:
        sr = srows[r["row_key"]]
        e = {"input": json.dumps({"text": sr["text"], "candidate_fol": sr["candidate_fol"], "system": r["system"]}, ensure_ascii=False),
             "output": r["label"]}
        for p in PRED:
            if r.get(p) is not None:  # a metric that was not run on this row (API refused) is omitted, never an empty string
                e[f"predict_{p}"] = s(r.get(p))
        for m in META:
            v = r.get(m)
            e[f"metadata_{m}"] = v if isinstance(v, (str, int, float, bool)) or v is None else json.dumps(v)
        ex.append(e)
    ctrl = []
    cp = WS / "scores" / "controls_scores_E2B.jsonl"
    v0 = {r["row_key"]: r.get("V0") for r in rows}
    if cp.exists():
        for c in (json.loads(l) for l in cp.read_text().splitlines() if l.strip()):
            sr = srows.get(c["parent_row_key"])
            if sr is None:
                continue
            ctrl.append({"input": json.dumps({"text": sr["text"], "candidate_fol": c["candidate_fol"], "system": sr["system"]}, ensure_ascii=False),
                         "output": "CORRECT", "predict_V0_control": s(c["V0_control"]), "predict_V0_parent": s(v0.get(c["parent_row_key"])),
                         "metadata_control_type": c["control_type"], "metadata_parent_row_key": c["parent_row_key"],
                         "metadata_sentence_id": c["sentence_id"], "metadata_n_peers": c["n_peers"]})
    ds = [{"dataset": "E2B_L25_candidates", "examples": ex}]
    if ctrl:
        ds.append({"dataset": "E2B_rename_controls", "examples": ctrl})
    out = {"metadata": {"method_name": "Frozen cross-family consensus c_score_align (V0) on E2-B, a second untouched L25 sample",
                        "description": "E2-B: 400 untouched MALLS-train sentences (>=25 words, >=3 conditions) drawn by E2's frozen rule; 10 generator slots; "
                                       "labels by E2's byte-identical solver + blind panel; scores sealed before labels. Orientation: higher = more likely unfaithful.",
                        "primary": "predict_V0", "baselines": ["predict_flashlite_disg (primary comparator)", "predict_flashlite_orig", "predict_nano_orig",
                                                              "predict_costmatched_disg (cost-matched deepseek-v3.2)", "predict_frontier_orig (gemini-3.1-pro-preview, 300-row subsample)",
                                                              "predict_S4_E2B (stack of cheap baselines)"],
                        "analysis": "analysis/analysis_E2B.json, analysis/confirm_verdict_E2B.json, analysis/union_longpool.json, analysis/tables.md"},
           "datasets": ds}
    (WS / "method_out.json").write_text(json.dumps(out, ensure_ascii=False))
    print(f"method_out.json: {len(ex)} candidate examples, {len(ctrl)} control examples")


if __name__ == "__main__":
    main()
