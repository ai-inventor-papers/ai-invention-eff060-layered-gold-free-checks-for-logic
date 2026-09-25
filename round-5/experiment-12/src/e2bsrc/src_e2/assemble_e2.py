#!/usr/bin/env python3
"""E2 STEP 7d (+VEX): final labels via E's frozen assemble.heldout() (final_rule, tiers, CONTESTED, reading_choice,
correct_not_equivalent, disguise) under the D1 shim, then E2 post-processing that changes no label:
  * per-row fields required by the E2 plan (row_key, strata incl. source_dataset/word_bin, fold, vex, vex_eq, pilot);
  * DT gold rows renamed from E's MALLS naming to 'proverqa_gold' (system/family/model) and E's
    'UNAUDITED_MALLS_GPT4_GOLD' reference status renamed 'UNAUDITED_PROVERQA_GOLD' for DT;
  * every ACTIVE E2 sentence (work/sentences_E2_active.json) gets a sentence row, including sentences with no
    candidates yet (reference_status PENDING_GENERATION_BUDGET_STOP) so nothing is silently dropped.
Output: work/assembled_E2.json with groups e2_candidates, e2_gold_as_system, e2_sentences.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src_e2"))
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "labeller"))
from compat import install  # noqa: E402

install()
import assemble  # noqa: E402
from vex import vex  # noqa: E402
from loguru import logger  # noqa: E402

W = ROOT / "work"
FOLD = {"L25": "E2_L25", "EXC": "E2_EXC", "DT": "E2_DT"}


def main():
    active = json.loads((W / "sentences_E2_active.json").read_text())
    by_sid = {s["sentence_id"]: s for s in active}
    rows, sent_rows = assemble.heldout()
    cands, golds = [], []
    for r in rows:
        s = by_sid[r["metadata_sentence_id"]]
        inp = json.loads(r["input"])
        is_dt = s["source_stratum"] == "DT"
        st = dict(r["metadata_strata"])
        st.update({"source_dataset": s["source_dataset"], "word_bin": s.get("word_bin"), "exc_pool": s.get("exc_pool"),
                   "dt_rung": s.get("dt_rung"), "proverqa_difficulty": s["source"].rsplit("-", 1)[-1] if is_dt else None})
        r["metadata_strata"] = st
        r["metadata_fold"] = FOLD[s["source_stratum"]]
        r["metadata_row_key"] = f"{r['metadata_item_id']}|{r['metadata_prompt_variant']}"
        r["metadata_pilot"] = bool(s.get("pilot"))
        r["metadata_convention_flag_source"] = s.get("convention_flag")
        r["metadata_control_type"] = None
        if is_dt and r["metadata_reference_status"] == "UNAUDITED_MALLS_GPT4_GOLD":
            r["metadata_reference_status"] = "UNAUDITED_PROVERQA_GOLD"
        if r["metadata_system_class"] == "reference_gold_as_system":
            if is_dt:
                r["metadata_system"] = "proverqa_gold"
                r["metadata_family"] = "prover-built-proverqa"
                r["metadata_generator_model_id"] = "ProverQA gold (ProverGen, Prover9-validated)"
                inp["system"] = "proverqa_gold"
                r["input"] = json.dumps(inp, ensure_ascii=False)
            golds.append(r)
            continue
        v = vex(inp["candidate_fol"], inp["reference_fol"]) if r["output"] != "UNPARSEABLE" else {"vex": None, "vex_eq": None}
        r["metadata_vex"], r["metadata_vex_eq"] = v["vex"], v["vex_eq"]
        cands.append(r)
    have = set()
    for sr in sent_rows:
        s = by_sid[sr["metadata_sentence_id"]]
        have.add(s["sentence_id"])
        if s["source_stratum"] == "DT" and sr["output"] == "UNAUDITED_MALLS_GPT4_GOLD":
            sr["output"] = "UNAUDITED_PROVERQA_GOLD"
    for s in active:
        if s["sentence_id"] in have:
            continue
        sent_rows.append({"input": json.dumps({"text": s["text"], "reference_fol": s["reference_fol"]}, ensure_ascii=False),
                          "output": "PENDING_GENERATION_BUDGET_STOP", "metadata_fold": "heldout",
                          "metadata_sentence_id": s["sentence_id"], "metadata_source": s["source"],
                          "metadata_original_reference_fol": s["reference_fol"], "metadata_n_candidates": 0})
    for sr in sent_rows:
        s = by_sid[sr["metadata_sentence_id"]]
        sr["metadata_fold"] = FOLD[s["source_stratum"]]
        sr["metadata_source_dataset"] = s["source_dataset"]
        sr["metadata_strata"] = {k: s.get(k) for k in ("words", "n_quant", "depth", "n_conditions", "text_conditions", "exception_type",
                                                          "source_stratum", "word_bin", "exc_pool", "dt_rung")}
        sr["metadata_exception_type"] = s.get("exception_type")
        sr["metadata_skeleton"] = s.get("skeleton")
        sr["metadata_proverqa_problem_id"] = s.get("proverqa_problem_id")
        sr["metadata_proverqa_role"] = s.get("proverqa_role")
        sr["metadata_convention_flag_source"] = s.get("convention_flag")
        sr["metadata_e2_rank"] = s.get("e2_rank")
        sr["metadata_e2_key"] = s.get("e2_key")
        sr["metadata_pilot"] = bool(s.get("pilot"))
        sr["metadata_l25_tier"] = s.get("l25_tier")
    sent_rows.sort(key=lambda x: (x["metadata_fold"], x["metadata_e2_rank"]))
    out = {"metadata": {"description": "E2 NL->FOL faithfulness confirmation set (run_u75jRHUss0zo iteration 4). NO METRIC IS COMPUTED HERE; "
                                       "iteration-4 experiments must not read E2.", "panel_members": assemble.MEMBER_MODEL},
           "datasets": [{"dataset": "e2_candidates", "examples": cands}, {"dataset": "e2_gold_as_system", "examples": golds},
                        {"dataset": "e2_sentences", "examples": sent_rows}]}
    (W / "assembled_E2.json").write_text(json.dumps(out, ensure_ascii=False))
    logger.info(f"E2 assembled: candidates {len(cands)} {dict(Counter(r['output'] for r in cands))}; tiers {dict(Counter(r['metadata_label_tier'] for r in cands))}; "
                f"gold rows {len(golds)}; sentences {len(sent_rows)} {dict(Counter(r['output'] for r in sent_rows))}")


if __name__ == "__main__":
    main()
