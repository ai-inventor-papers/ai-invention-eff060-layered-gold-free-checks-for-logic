#!/usr/bin/env python3
"""STEP B: write prereg_freelab.json + prereg_freelab.sha256 (frozen before the first FREE labelling run)."""
from __future__ import annotations

import json
import time

from common import ROOT, RES, dump, sha256_bytes, sha256_file

import freelab as FL


def main() -> None:
    census = json.loads((RES / "shape_census.json").read_text())
    prompt = json.loads((ROOT / "prompts/gloss_v1.json").read_text())
    pr = {
        "id": "prereg_freelab_v1",
        "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "scope": "FREE condition of R_COMP (exp 7 rcomp/raw/generations.jsonl, last record per (sentence, slot, prompt_variant)); "
                 "SIG rows (exp 7 results/sig_labels.jsonl) only for the gate and soundness audit (i)",
        "a_map_family": {
            "units": "a candidate predicate is a UNIT if in every occurrence all argument positions except one subject "
                     "position hold the same constants and those constants occur nowhere else in the formula (constant "
                     "absorption; unary predicates are units). Template units = atom instances over the single variable x.",
            "unit_map": "candidate unit -> exactly one template unit (plain rename; B1 reification P(x):=R(x,c); B2 "
                        "de-reification P(x,k[,k2..]):=U(x) (generalised from binary to n-ary constant absorption); "
                        "P(x,k):=R(x,c)); the subject argument keeps its term",
            "relation_map": "a relevant non-unit binary candidate predicate -> a template binary predicate, either argument "
                            "order; its non-absorbed relevant constants -> template constants injectively, or free (fresh)",
            "injective": "each template unit / template predicate is the target of at most one candidate symbol (B4 excepted)",
            "unmapped": "an unmapped candidate symbol stays a fresh uninterpreted symbol (only relevance-UNKNOWN symbols may "
                        "stay unmapped; a relevant unmapped symbol makes the map non-equivalent, certificate 'coverage')",
            "other_arity": "a relevant candidate symbol of arity 0, or arity >= 3 that is not a unit, has no target "
                           "(certificate 'unmappable_symbol')",
        },
        "b_bridges": {
            "B1": "reification: candidate unary P(x) := template R(x,c)",
            "B2": "de-reification: candidate P(x,k..) with constants k only in those slots := template unary U(x)",
            "B3": "merge: candidate unit := u1 ∧ u2 for two template units that are direct sibling conjuncts of one ∧-chain "
                  "of the reading",
            "B4": "conjunctive split: two candidate units both := one template unit; only if both occur ONLY as positive "
                  "direct sibling conjuncts with the same subject term (checked syntactically on every occurrence)",
            "B5": "lexical negation: candidate unit := ¬u; only if the first CamelCase/underscore token matches "
                  "^(not|non|no|un|in|im|il|ir|dis|never|lacks?|without)$ (case-insensitive) or the name matches ^(Un|Non|In|Im|Dis)[A-Z]",
            "B6": "NOT declared: label-free shape census found the ∃-for-constant form in "
                  f"{census['exists_for_constant_share']:.0%} of 100 sampled rows (< 5% bar); it is a known out-of-family form "
                  "quantified by audit (ii)",
            "cap": f"structural bridge uses (B3 + B4) <= {FL.MAX_STRUCT} per map; B1/B2/B5 are 1:1 unit forms and are NOT "
                   "capped (deviation D2 from the plan's 'at most 2 bridge uses', decided from the label-free shape census: "
                   f"{census['counts']['unary_count_gt_template']}% of sampled rows have more unary predicates than the template "
                   "and 37% fewer binary ones, i.e. >=3 reification uses per row are common)",
        },
        "c_sound_prunes": {
            "relevance": "symbol s is inert iff F ≡ F[s := fresh] (z3: VACUOUS in fol.profile for predicates; "
                         "F ≡ F[c := c'] for constants); inert symbols are recorded and dropped (kept fresh in the image)",
            "coverage_count": "every relevant template unit must be covered by the image (a relevant template predicate "
                              "absent from the image makes equivalence impossible); subtree prune when the remaining symbols "
                              "cannot cover the remaining units",
            "polarity": "z3-exact per-predicate monotonicity (UP / DOWN / NONMONO) of the candidate must equal that of the "
                        "target unit (flipped under B5); for B3/B4 required only when the candidate side is UP or DOWN; "
                        "UNKNOWN = no prune (and an UNKNOWN-relevance symbol may stay unmapped)",
            "fingerprint": f"evaluate image and reading on {FL.N_FP} finite interpretations (domain 2/3, predicate densities "
                           "50/75/90/25%, crc32-seeded, fixed); a mismatch is a certified finite countermodel",
            "z3": f"maps that agree on all {FL.N_FP} go to z3 equivalence, {FL.Z3_MS} ms, one retry at {FL.Z3_MS_RETRY} ms if unknown",
        },
        "d_caps": {"max_maps_per_candidate_reading": FL.MAX_MAPS, "max_secs_per_candidate_reading": FL.MAX_SECS,
                   "cap_hit": "UNRESOLVED_SEARCH_CAP", "second_pass": "a single second pass at 4x both caps for capped classes only",
                   "z3_unknown": "any z3 UNKNOWN on a fingerprint-passing map (or UNKNOWN relevance) with no equivalent map "
                                 "-> UNRESOLVED_Z3_UNKNOWN"},
        "e_label_rules": {
            "unit_of_search": "unique (sentence_id, whitespace-normalised candidate_fol) class",
            "ERROR_CERT": "no map equivalent to weak or strong (and on T8 none to the converse); every rejected map carries a "
                          "certificate (countermodel / z3_sat / polarity / coverage / unmappable)",
            "READING_CHOICE": "maps equivalent only to the T8 converse",
            "MAPPED": "maps equivalent to weak or strong -> gloss rule (f); matched_reading weak / strong / both",
            "NO_OUTPUT": "raw_output None", "UNPARSEABLE": "exp 7 parse_ok False or our parser fails",
            "binary": "ERROR = ERROR_CERT or ERROR_GLOSS; CORRECT = CORRECT; EXCLUDED otherwise",
        },
        "f_gloss_rule": "union of (symbol use, meaning) pairs over ALL z3-equivalent maps; each checker rates every pair "
                        "independently; CORRECT iff some equivalent map has all pairs YES from BOTH checkers; ERROR_GLOSS iff "
                        "every equivalent map contains a pair that is NO from BOTH; otherwise UNRESOLVED_GLOSS. Unparseable "
                        "checker JSON: one re-ask, then NO_VERDICT (-> UNRESOLVED). Cache key (sentence_id, use, meaning).",
        "g_gloss_prompt": prompt,
        "g_gloss_prompt_sha256": sha256_file(ROOT / "prompts/gloss_v1.json"),
        "checkers": {"A": "anthropic/claude-haiku-4.5", "B": "qwen/qwen3-235b-a22b-2507",
                     "family_disjointness": "CSC peers are DeepSeek/Microsoft/OpenAI, the LLM evaluators under test Google/OpenAI; checkers are "
                                            "Anthropic and Alibaba"},
        "h_gate": {
            "classes": {"YES_IDENT": "template name, _k suffix stripped", "YES_SYN": "WordNet mutual first-sense synonym of one "
                        "name token (dataset 3 first_sense_synonyms)", "YES_FORM": "reified (R+Const as unary), de-reified "
                        "(Head(x, rest)), lexical-negation name for the negated gloss, or merged name for a conjunction of two sibling glosses",
                        "NO_NONCE": "nonce CVCVC name", "NO_DONOR": "another lexicon entry's predicate of the same sort "
                        "group whose tokens are not WordNet synonyms", "NO_ROLE": "argument swap of a directional binary unit, "
                        "or the positive name offered for the negated gloss", "NO_MERGE": "(added, D3) one unit's name offered "
                        "for the conjunction of its gloss and a sibling's gloss (the DROP-rescue case of B3)"},
            "n_per_class": ">= 100 (target 120), stratified over templates and sort groups, halves A/B by sha1(sentence_id) parity",
            "pass": "balanced accuracy >= 0.90 for Haiku, for Qwen AND for the both-YES conjunction, AND recall >= 0.85 for "
                    "each of the YES and NO super-classes (conjunction), on half A",
            "fail": "one revision gloss_v2, re-frozen with a hash, evaluated on half B only; a second failure -> no gloss "
                    "step: every MAPPED row becomes UNRESOLVED_GLOSS_GATE_FAILED",
        },
        "i_testability": {"rule": "TESTABLE iff >= 50 ERROR and >= 50 CORRECT rows spread over >= 25 sentences each "
                                  "(a sentence counts toward a class if it has >= 1 row of that class)",
                          "populations": ["all FREE rows", "untouched subset (not tier-A labelled in iteration 3) = PRIMARY"],
                          "descriptive": "30/30 reportability per stratum (template, clause_type, word tercile 30/35, prompt_variant)",
                          "mde_note": "AUROC SE ~0.05 and MDE ~0.10 at 50/50"},
        "j_audits": {
            "i_sig_replay": "all SIG CORRECT/ERROR/READING_CHOICE rows with an on-signature candidate, every symbol consistently "
                            "renamed (a) to nonce tokens, (b) to WordNet synonyms where one exists; map search vs references; "
                            "report ERROR_CERT false-error rate on SIG-CORRECT (bar <= 0.02) and the non-identity rescue rate "
                            "on SIG-ERROR; on a stratified 300 (150 CORRECT / 150 ERROR by template) of the synonym renames "
                            "run the full pipeline incl. gloss: false-CORRECT on known ERROR (bar <= 0.05), CORRECT recall, UNRESOLVED share",
            "ii_stronger_model": "anthropic/claude-sonnet-5 (newest Sonnet in the catalogue), 60 ERROR_CERT (stratified by "
                                 "template) + 60 CORRECT FREE rows; prompt shows sentence, candidate, English meaning of each "
                                 "template atom; FAITHFUL / FAITHFUL_DIFFERENT_DECOMPOSITION / UNFAITHFUL / UNSURE + reason; "
                                 "Wilson 95% CIs; never changes a label",
            "iii_old_labels": "post-seal join of exp 7 tier-A FREE labels via a whitelist loader (row_key, label, label_tier, "
                              "label_source); kappa + 20 hand-classified disagreements",
        },
        "budget": {"plan_estimate_usd": "2.5-3.2", "plan_hard_stop_usd": 3.8,
                   "rule": "if the FREE gloss sweep estimate exceeds $2.2, untouched-subset rows are processed first; the "
                           "artifact hard stop is $6.0 (artifact budget $10), logged as deviation D4 if the $3.8 plan stop is passed"},
        "code_sha256": {"src/freelab.py": sha256_file(ROOT / "src/freelab.py")},
        "vendor_sha256": json.loads((ROOT / "VENDOR_SHA256.json").read_text())["vendor"],
        "pre_freeze_disclosures": [
            "D1: a 12-row FREE dev trial of the search code (random seed 3; printed maps, no labels, no scores) was run before "
            "this freeze; it confirmed the reification forms also seen in the label-free census",
            "D2: B1/B2/B5 uncapped; only B3+B4 <= 2 (see b_bridges.cap)",
            "D3: gate class NO_MERGE added; B2 generalised to n-ary constant absorption",
            "D5: the plan's '1,904 SIG rows' is the subset with both exp-7 scores; audit (i) uses every SIG row labelled "
            "CORRECT / ERROR / READING_CHOICE (2,140) - a superset, chosen before any replay output",
        ],
    }
    b = json.dumps(pr, indent=1, ensure_ascii=False).encode()
    (ROOT / "prereg_freelab.json").write_bytes(b)
    (ROOT / "prereg_freelab.sha256").write_text(sha256_bytes(b) + "  prereg_freelab.json\n")
    print(sha256_bytes(b))


if __name__ == "__main__":
    main()
