#!/usr/bin/env python3
"""STEP 5: write prereg_rcomp.json BEFORE any candidate generation (refuses to overwrite once generation started).

`declare` (after STEP 7/8 labels exist, BEFORE any metric runs) fills `testability_declaration` exactly once.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import time

from common import RAW, ROOT, W, dump, load_jsonl, setup_logger

logger = setup_logger("prereg")
P = ROOT / "prereg_rcomp.json"

TEMPLATES = {
    "T1": {"text": "Every N who C1, who C2, and who C3 Q, unless the N E.", "variant_1": "Each ... , except if the N E.",
           "weak": "∀x (S ∧ A1 ∧ A2 ∧ A3 ∧ ¬E → Q)", "strong": "∀x (S ∧ A1 ∧ A2 ∧ A3 → (Q ↔ ¬E))"},
    "T2": {"text": "If a N C1 and C2, and the N also C3, then the N Q, except when the N E.",
           "variant_1": "When a N C1 and C2, and the N also C3, the N Q, except when the N E.", "weak": "as T1", "strong": "as T1"},
    "T3": {"text": "Any N that C1 and that C2 Q, provided that the N P and C3.", "variant_1": "Every ... providing that ...",
           "weak": "∀x (S ∧ A1 ∧ A2 ∧ P ∧ A3 → Q)", "strong": "∀x (S ∧ A1 ∧ A2 → (Q ↔ (P ∧ A3)))"},
    "T4": {"text": "A N who C1 and who C2 Q as long as the N C3, unless the N E.", "variant_1": "... so long as ...",
           "weak": "as T1", "strong": "as T1", "note": "A3 stays a plain condition: single-exception reading"},
    "T5": {"text": "Every N who C1 and who C2 Q, provided that the N C3, unless the N E.", "variant_1": "Each ... except if ...",
           "weak": "as T1", "strong": "as T1", "nested": True},
    "T6": {"text": "Except when the N E, every N who C1 and who C2 Q, provided that the N C3.",
           "variant_1": "Except if the N E, each N ...", "weak": "as T1", "strong": "as T1"},
    "T7": {"text": "Anyone who C1, C2, and C3 Q unless they E.", "variant_1": "Anybody ...",
           "weak": "∀x (A1 ∧ A2 ∧ A3 ∧ ¬E → Q)", "strong": "∀x (A1 ∧ A2 ∧ A3 → (Q ↔ ¬E))",
           "note": "person group only; no sortal atom; E re-inflected for 'they' (is->are, has->have, does->do, -s stripping)"},
    "T8": {"text": "If a N C1, C2, and C3, then the N Q, but only if the N P.", "variant_1": "When a N C1, C2, and C3, the N Q, but only if the N P.",
           "weak": "∀x (S ∧ A1 ∧ A2 ∧ A3 ∧ Q → P)", "strong": "∀x (S ∧ A1 ∧ A2 ∧ A3 → (Q ↔ P))",
           "converse_NOT_accepted": "∀x (S ∧ A1 ∧ A2 ∧ A3 ∧ P → Q) -> flag ONLY_IF_CONVERSE, routed to adjudication"},
    "T9": {"text": "No N who C1, who C2, and who C3 Q, unless the N E.", "variant_1": "No N that ..., except when the N E.",
           "weak": "∀x (S ∧ A1 ∧ A2 ∧ A3 ∧ ¬E → ¬Q)", "strong": "∀x (S ∧ A1 ∧ A2 ∧ A3 → (¬Q ↔ ¬E))"},
}


def sha256(p) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def write():
    if P.exists() and (RAW / "generations.jsonl").exists():
        raise SystemExit("prereg_rcomp.json is frozen: candidate generation has started")
    d = {
        "frozen_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "frozen_before": "any R_COMP candidate generation, solver labelling, adjudication or metric run",
        "templates_and_readings": TEMPLATES,
        "slots": "N noun of a sortal lexicon entry (S its atom); C1..C3 condition phrases (vp_sg_pos, or vp_sg_neg for one "
                 "condition in ~45% of sentences = ~15% of conditions); Q consequent; E exception; P proviso",
        "composition_constraints": ["conditions from >= 2 distinct source rules", "Q and E/P from different source rules",
                                    "no predicate twice in a sentence", "no two entries whose content-word stems overlap "
                                    "(subset or Jaccard >= 0.5)", "unique (sorted conditions, Q, E/P)",
                                    "each lexicon entry in <= 4 main sentences (and separately <= 4 reserve sentences)",
                                    "any sentence drawing an audited-WRONG lexicon entry is rejected"],
        "filters_in_order": ["words >= 25", "nconds(weak) >= 3 (E complexity_counts.nconds)", ">= 2 non-sortal restrictor atoms",
                             "z3: weak neither valid nor unsat; weak not equivalent to strong; no VACUOUS/UNKNOWN atom in "
                             "fol.profile(weak) and no VACUOUS atom in profile(strong)", "no screen hash collision (E build_exclusion)",
                             "no string / combination duplicate", "fluency >= 3 (Haiku-4.5)", "not REF_FLAGGED by the Sonnet reference audit",
                             "no lexicon entry implicated in >= 2 flags"],
        "selection": "sha1 order; main 250 = T8 25 (<= 10%), T1 29, every other template 28; round-robin over word bins "
                     "25-29 / 30-34 / >=35; TOP-UP RESERVE 100 = next-best T1/T2/T7 (3 conditions, not nested), audited now",
        "label_rule_step7": {
            "CORRECT": "auto_label(c, weak) or auto_label(c, strong) == CORRECT (plain z3 EQ) -> tier A, matched_reading",
            "VOCAB_GRAN": "either reading VOCAB/GRAN -> routed P1 (NEVER auto-CORRECT; E: 58/59 solver->panel transitions CORRECT->ERROR)",
            "TIMEOUT_UNKNOWN": "routed P2",
            "ERROR": "minimal_typed_repair vs weak AND strong (8 s each), fewest ops (tie -> weak) -> ERROR(ops) tier A",
            "COMPOUND": "no repair found vs either reading -> routed P2",
            "UNPARSEABLE": "kept, never dropped",
            "ONLY_IF_CONVERSE": "T8 candidate equivalent (modulo vocabulary) to the converse -> flag, routed P3",
            "classes": "per sentence by identical normalised string or plain z3 EQ with identical symbols only",
            "lex_anchored_vocab": "diagnostic column only, never a label (shares an instrument with L2-bow)"},
        "routing_step8": {"order": "strict P1 > P2 > P3 > P4; within a priority sentences in sha1(sentence_id) order; SENTENCE-COMPLETE",
                          "P1": "VOCAB_GRAN", "P2": "COMPOUND, TIMEOUT_UNKNOWN",
                          "P3": "ERROR with addrop_only_suspect, SORTAL/ARITY_REIFY/XOR_OR flag, or ONLY_IF_CONVERSE",
                          "P4": "20% sha1 sample of other solver ERRORs (solver-ERROR precision)"},
        "final_label_rule": {
            "routed(VG/COMPOUND/TIMEOUT) + FAITHFUL": "CORRECT, tier B, correct_not_equivalent = true",
            "routed + UNFAITHFUL": "ERROR, tier B, adjudicator ops (+ MEANING_RENAME for VOCAB_GRAN)",
            "solver ERROR + FAITHFUL": "CONTESTED", "solver ERROR + UNFAITHFUL": "ERROR, tier A (confirmed)",
            "AMBIGUOUS_READING": "reading_choice = true",
            "not reached before cap": "P1/P2 -> UNRESOLVED; P3/P4 -> solver ERROR kept with adj_pending = true",
            "REF_FLAGGED sentence": ">= 2 adjudications with reference_wrong = true -> all its rows tier C, out of the primary pool",
            "adjudicator gate": "if the sibling R_ADJ gate FAILED (or is void) or the in-stratum known-label check BA < 0.80, "
                                "every tier-B R_COMP label is marked provisional"},
        "caps_usd": {"lexicon_extraction": 0.4, "lexicon_audit": 0.4, "fluency": 0.1, "reference_audit": 0.5, "generation": 1.5,
                     "known_label_check": 0.2, "adjudication": 2.5, "topup": 1.3, "reserve": 2.6, "hard_stop": 9.5},
        "testability_rule": "R_COMP is TESTABLE iff tiers A+B hold >= 50 CORRECT and >= 50 ERROR LLM rows, each spread over >= 25 "
                            "distinct sentences, excluding CONTESTED, reading_choice and REF_FLAGGED rows; declared (A+B and A-only) "
                            "after labelling and BEFORE any metric runs",
        "topup_rule": "after STEP 8, if tiers A+B hold < 50 CORRECT LLM rows or < 25 CORRECT sentences (likewise ERROR), generate, "
                      "label and adjudicate the 100-sentence reserve with the full slot set (cap $1.3); flagged topup_batch; "
                      "results reported with and without the top-up",
        "generation": "E's generate.py unchanged: 10 few-shot slots + zero-shot G1b/G2 on all 250; F gpt-5.1 (effort low, 4000 tokens) "
                      "on the sha1-first 80 (40 if the 12-sentence pilot projects > $1.5); temperature 0; prompts/fewshot_v1.txt "
                      "sha1 a1c7ae39f13979a96e6b360f8d3164735c334d80, zeroshot_v1.txt sha1 9e8b244214f84e8ba46041eb0be4cef6cb7cc196",
        "adjudicator": json.loads((W / "adjudicator_model.json").read_text()),
        "adjudication_user_message": "SENTENCE / CANDIDATE FOL / REFERENCE FOL (VERIFIED), reading 1 (<weak label>) / reading 2 "
                                     "(<strong label>) / 'A translation equivalent in meaning to either reading is faithful.' "
                                     "(the only addition to the sibling's user template)",
        "known_label_check": "30 PERTURB + 30 PERTURB_CONTROL rows on R_COMP bases through the identical prompt; BA < 0.80 -> tier B provisional",
        "perturbation_spec": {"bases": "E GOLD_PANEL_OK + TRUSTED_AGREED (131), PANEL_REPAIRED to 200, first 100 R_COMP main (weak)",
                              "operators": ["NEG", "REV", "QUANT", "RESTR", "CONN", "MOVE", "DROP", "ADD (ADD_FOREIGN, ADD_INTERNAL)",
                                            "SWAP", "BIND", "SCOPE", "UNGLUE", "MEANING_RENAME"],
                              "polarity": "atom-level (SWAP/BIND/MEANING_RENAME) fol.profile; structural: syntactic path polarity",
                              "selection": "first valid mutant per (base, op, DOWN/UP) in sha1(string) order; z3 non-equivalent (3 s) to "
                                           "base and every accepted reading (+ T8 converse); UNKNOWN discarded; non-trivial if base is; "
                                           "no free variables; cap 6000",
                              "controls": "RENAME (RENAME_SYN mutual-first-sense noun synonym / RENAME_NONCE), REORDER, "
                                          "CONTRAPOSITIVE (DEMORGAN without implication), each z3-verified equivalent"},
        "file_hashes_at_freeze": {"adjudication_prompt.txt": sha256(ROOT / "adjudication_prompt.txt"),
                                  "prompts/fewshot_v1.txt": sha256(ROOT / "prompts/fewshot_v1.txt"),
                                  "prompts/zeroshot_v1.txt": sha256(ROOT / "prompts/zeroshot_v1.txt"),
                                  "src/templates.py": sha256(ROOT / "src/templates.py")},
        "testability_declaration": None,
    }
    dump(P, d)
    logger.info(f"prereg written, sha256 {sha256(P)}")


def declare():
    d = json.loads(P.read_text())
    if d.get("testability_declaration"):
        raise SystemExit("testability already declared")
    decl = json.loads((W / "testability.json").read_text())
    decl["declared_at_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    decl["declared_before"] = "any metric run on R_COMP"
    d["testability_declaration"] = decl
    dump(P, d)
    logger.info(f"testability declared: {decl.get('verdict')}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["write", "declare"])
    a = ap.parse_args()
    write() if a.cmd == "write" else declare()
