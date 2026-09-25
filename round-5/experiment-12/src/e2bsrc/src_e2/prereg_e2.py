#!/usr/bin/env python3
"""E2 STEP 2: write prereg_E2.json and prereg_E2.sha256 BEFORE any generation (refuses to overwrite a frozen prereg)."""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from generate import SLOTS  # noqa: E402  (E's frozen slot table)
from panel import MEMBERS, PROMPT_SHA1  # noqa: E402

E_CARD = Path(__file__).resolve().parents[5] / "round-1/dataset-1/src/dataset_card.md"
FEWSHOT_SLOTS = ["G1", "G1b", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9"]


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    out = ROOT / "prereg_E2.json"
    if out.exists():
        print("prereg_E2.json already frozen; refusing to overwrite"); return
    e_prereg = json.loads((ROOT / "E_ref" / "prereg_strata.json").read_text())
    census = json.loads((ROOT / "census_E2.json").read_text())
    pool = json.loads((ROOT / "work" / "pool_E2.json").read_text())
    card = E_CARD.read_text()
    tier_rules = card[card.index("## 2. Final label rule"):card.index("## 3. Label counts")]
    cf = json.loads((ROOT / "code_freeze.json").read_text())
    fs_txt = (ROOT / "prompts" / "fewshot_v1.txt").read_text()
    pre = {
        "artifact": "E2 - fresh untouched NL->FOL confirmation set (run_u75jRHUss0zo, iteration 4, gen_art_dataset_4, plan gen_plan_dataset_1_idx3)",
        "frozen_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "frozen_before": "any E2 candidate generation, any E2 label, any metric. NO METRIC IS COMPUTED IN THIS ARTIFACT; iteration-4 experiments must not read E2.",
        "sources": {
            "MALLS": {"hf_repo": "yuan-yang/MALLS-v0", "files": ["MALLS-v0.1-train.json", "MALLS-v0.1-test.json"],
                      "local_copy": "data_local/ (byte-identical copies of dataset E's data_local, sha256 in code_freeze.json)", "licence": "CC-BY-NC-4.0"},
            "ProverQA": {"hf_repo": "opendatalab/ProverQA", "revision": census["dt"]["hf_revision"], "files": ["dev/easy.json", "dev/medium.json", "dev/hard.json"]},
            "FOLIO (exclusion only)": {"hf_repo": "tasksource/folio", "revision": "295b95fb4fe9be4ff3f933b73142d142cf6b2c97"}},
        "strata": {
            "E_strata_verbatim": e_prereg["strata"],
            "L25_E2": "MALLS-v0.1-train, >=25 words AND gold n_conditions>=3 (E's rule and E's functions); bins 25-29 and >=30 (30-34; >=35 is exhausted): the >=30 bin gets min(supply, 45% of target), the rest from 25-29; sha1('E2_v1|'+sentence_id) order within bin",
            "EXC_E2": "exception_type() of E EXCLUDING the XOR 'but not (both)' pattern, filled to target in pre-registered order (a) MALLS-train core unless/except/excluding/other-than not used by E, (b) MALLS-v0.1-test non-curated core-marker items >=15 words with parseable gold, (c) MALLS-train 'without' >=15 words, (d) non-XOR 'but not' >=15 words (train then test)",
            "DT_E2": "ProverQA dev (easy/medium/hard): every nl2fol (sentence->FOL) unit plus question statement->conclusion_fol; gold must parse and round-trip (parse->emit->parse, z3 self-equivalence); dedup by normalised text and by entity-abstracted skeleton (constants -> ENT), 1 per skeleton; inclusion ladder (>=15w,>=2c) -> (>=12w,>=2c) -> (>=15w,>=1c); XOR/OR convention flag carried"},
        "targets": {"L25": 350, "EXC": 100, "DT": 100, "DT_reserve": 10,
                    "DT_reserve_rule": "used only if the DT gold-parse or generation failure rate exceeds 10%"},
        "seed_string": "E2_v1|", "order": "sha1('E2_v1|' + sentence_id), sentence_id = E's sid(): sha1('heldout|'+norm(text))[:12]",
        "exclusion_rules": {
            "hash_exclusion": "E's build_exclusion() (FOLIO validation tasksource + refined, curated FOLIO/MALLS, MALLS-test, Logic-LM contexts/questions) + E's 700 sentences + E's 20 calibration sentences + E's 6 few-shot exemplars + every screen text + FOLIO-v2-train premises/conclusions (MALLS-test suppressed only for EXC pool b)",
            "twelve_gram": "lowercase word-token 12-grams (E's norm()); drop any candidate sharing a 12-gram with any E sentence; within E2 keep only the first (E2 build order EXC -> L25 -> DT, sha1 order within) of two sentences sharing a 12-gram"},
        "selection_census": census,
        "selection_hashes": {"work/pool_E2.json": sha256(ROOT / "work" / "pool_E2.json"),
                             "work/sentences.json (active base set)": sha256(ROOT / "work" / "sentences.json")},
        "pool_order": {k: [r["sentence_id"] for r in v] for k, v in pool.items()},
        "generator_slots": {s: {"model": SLOTS[s][0], "family": SLOTS[s][1], "params": SLOTS[s][2]} for s in FEWSHOT_SLOTS},
        "generation": {"prompt": "prompts/fewshot_v1.txt (verbatim, E)", "prompt_sha1": hashlib.sha1(fs_txt.encode()).hexdigest(),
                       "temperature": 0.0, "max_tokens": 600, "variants": ["fewshot_v1"],
                       "excluded": "no zero-shot rows, no GPT-5.1 frontier slot, no ccg2lambda"},
        "slot_unavailability_rule": "a model id no longer served is replaced by the same family's nearest current instruct model, logged and flagged slot_substituted=true; a family is never swapped. At freeze time all 10 slot ids and all 3 panel ids are served (work/models_snapshot_E2.json).",
        "labeller_sha256": {r["copy"]: r["sha256_copy"] for r in cf["files"] if r["copy"].startswith(("labeller/", "src/"))},
        "code_freeze_sha256": sha256(ROOT / "code_freeze.json"),
        "panel": {"P1": MEMBERS["P1"], "P3": MEMBERS["P3"], "R1": MEMBERS["R1"], "production_prompt_sha1": PROMPT_SHA1,
                  "design": "disguised (labeller/disguise.py), blind, shuffled, <=8 formulas per call; stage 1 = P3+R1 on every class of every sentence (full class coverage on all E2 strata, as E did for its MALLS strata); stage 2 = P1 only where P3/R1 disagree or a vote is missing; pilot = all three raters (as E's 5c pilot)",
                  "cache": "fresh work/panel_cache.jsonl in this workspace (no reply cached for E can be served; E's cache file is never read by the panel code)"},
        "tier_rules_verbatim_from_E_card_section_2": tier_rules,
        "testability_rule_verbatim_from_E": e_prereg["testability_rule"],
        "testability_application_E2": "LLM systems only (gold-as-system rows excluded), tiers A+B, CONTESTED and reading_choice excluded; applied to regimes R_AB (primary), R_A (tier A only) and R_VEX (tier A+B rows whose candidate (name, arity) symbol set is a subset of the reference's; no rename step)",
        "drift_check_stop_rule": "replay E's 77 synthetic gate items and the 96 track-H expert pairs with today's P1/P3/R1, the v2 prompt and the fresh cache. If majority agreement with E's STORED votes is < 0.85, or a panel model id is no longer served, the panel is NOT used for E2: tier A against UNAUDITED gold only (reference_status UNAUDITED_GOLD_DRIFT_STOP), every non-EQ auto class stays UNRESOLVED, and the card marks E2 'tier-A-only confirmation'.",
        "budget": {"hard_cap_usd": 9.5, "phase_caps_usd": {"drift (gate + gate_trackh)": 0.8, "pilot": 0.6, "generation": 1.3,
                                                          "panel stage 1 (panel_heldout)": 4.6, "adjudication (panel_heldout_adj)": 1.9, "reference repair": 1.0},
                   "note": "pilot calls are booked under the production phase names (generation / panel_heldout / panel_heldout_adj / reference_repair) because the frozen scripts are used; pilot spend is reported separately by sentence id"},
        "shrink_order": "EXC -> 75, then L25 -> 300 (floor); DT never below 100",
        "surplus_rule": "if the pilot projection is <= $8.0, add L25 sentences from the pre-registered surplus order (pool_order.L25 after the first 350) until projected spend = $8.6, up to L25 = 450. Pilot data inform COST only.",
        "vex_flag": "new additive helper src_e2/vex.py: set(normalised (name, arity) of candidate predicates+constants) subset-of set(reference's), no rename step; vex_eq = plain z3 equivalence (no alignment). Changes no label.",
        "controls": "up to 300 final-CORRECT LLM rows (tier A first, then tier B), spread over strata, sha1 order; RENAME_SYN and RENAME_NONCE via dataset 3's perturb.control_rename; z3-verified under the inverse map; separate fold, never in R_AB pools",
        "seal": "sealed/labels_E2.jsonl + sealed/references_E2.jsonl separated from candidates_E2_nolabels.jsonl (no label, no reference, no gold-as-system row) and controls_E2_nolabels.jsonl; seal.json with sha256s; verify_seal.py scans for forbidden keys and reference strings",
        "deviations_known_at_freeze": [
            {"id": "D0", "what": "or_client.py base-URL transport fix", "effect": "none on labels"},
            {"id": "D1", "what": "src_e2/compat.py makes E's MALLS-only branches (gold row as a system, blind gold audit counted as GOLD_WRONG, reference repair) apply to the ProverQA DT gold, as the plan requires ('MALLS gold and ProverQA gold get the same audit'). E's code is unmodified; the shim wraps the source string.", "effect": "DT sentences get the MALLS treatment instead of E's CTRL treatment (DISPUTED_REFERENCE)"},
            {"id": "D2", "what": "E's code is copied to ./src and ./labeller (not ./src_E) because its ROOT-relative paths require that layout; E2 wrappers live in ./src_e2", "effect": "none"},
            {"id": "D3", "what": "EXC core-marker supply is exhausted: pools (a) and (b) are empty (E took all 67 MALLS-train core items; MALLS-test has only 3 core-marker items, all excluded). EXC = 'without' + non-XOR 'but not' items; core-marker share 0.0. Fallback (iv): keep EXC, never borrow E sentences.", "effect": "EXC on E2 is about weaker exception constructions; the EXC-core testability row is empty by construction"}],
        "power_statement_corrected": "From E's L25 numbers the stratified dAUROC CI half-width was 0.085 at 300 sentences (SE ~0.043, SE ~ 1/sqrt(sentences with both classes)). Detecting d=0.08 at 80% power needs SE <= 0.0286, about 690 L25 sentences at E's yield. 350 L25 sentences give MDE80 ~0.11; 450 give ~0.10. The direction's claim that ~400 L25 sentences detect +0.08 is wrong.",
        "success_criterion_DT": "positive sign only (transfer check on a different, templated register)",
    }
    out.write_text(json.dumps(pre, ensure_ascii=False, indent=1))
    (ROOT / "prereg_E2.sha256").write_text(sha256(out) + "  prereg_E2.json\n")
    print("frozen", sha256(out))


if __name__ == "__main__":
    main()
