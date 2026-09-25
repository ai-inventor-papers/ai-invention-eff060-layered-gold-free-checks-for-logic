#!/usr/bin/env python3
"""STEP 11: dataset_card.md from work/stats.json, prereg_rcomp.json and the phase logs (re-run after every phase)."""
from __future__ import annotations

import hashlib
import json
import time

from common import ROOT, W, load_jsonl

S = json.loads((W / "stats.json").read_text())
PRE = ROOT / "prereg_rcomp.json"
PR = json.loads(PRE.read_text())
ADJ = json.loads((W / "adjudicator_model.json").read_text())
KEYLOG = (ROOT / "logs" / "key_status.log").read_text().strip().splitlines() if (ROOT / "logs" / "key_status.log").exists() else []


def j(x) -> str:
    return "`" + json.dumps(x, ensure_ascii=False) + "`"


def table(rows: list[list], head: list[str]) -> str:
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def main():
    has_c = "candidates" in S
    C = S.get("candidates", {})
    T = S.get("testability")
    L = []
    a = L.append
    a("# Dataset card: R_COMP (long composed sentences with trusted references) + PERTURB (typed perturbation suite)")
    a("")
    a(f"Generated {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())} by `src/card.py`. Run `run_u75jRHUss0zo`, invention iteration 2, "
      f"`gen_art_dataset_3` (plan `gen_plan_dataset_2_idx4`). It builds on dataset E (`iter_1/gen_art/gen_art_dataset_1`) and never writes to it. "
      f"Absolute workspace: `{ROOT}`.")
    a("")
    a("## 0. Status: read this first")
    if has_c:
        a("All phases have run. See §6 for the labels and §5 for the testability declaration.")
    else:
        a("**The R_COMP candidate generation, labelling and adjudication have NOT run yet.** The shared OpenRouter key (a $50/day "
          "limit shared by every run on the machine) hit its daily limit at about 18:00 UTC on 2026-09-23, "
          "roughly five minutes into this module, after 67 lexicon-extraction calls ($0.414). The limit resets daily "
          "at 00:00 UTC, after this module's deadline (23:49 UTC). Every later poll (`logs/key_status.log`, every 5 min) "
          f"showed `limit_remaining = 0`; the last line is `{KEYLOG[-1] if KEYLOG else 'n/a'}`.")
        a("")
        a("A replacement key arrived at about 21:38 UTC. It had already used its $50 daily limit before this module's first "
          "call ($50.06 used; a test call returned 403 'Key limit exceeded'). It stayed at 0 through the last poll at "
          "22:07 UTC. To use it, prefix `./run_all.sh` with "
          "`OPENROUTER_API_KEY=\"$(cat /ai-inventor/aii_data/.secrets/openrouter_key.private)\"`.")
        a("")
        a("What IS complete ($0 phases, all deterministic and re-runnable):")
        a("- Source atom pool (STEP 1).")
        a("- Haiku lexicon extraction (STEP 2a): 57 of 64 jobs; the $0.4 cap stopped the rest.")
        a("- Deterministic lexicon checks (STEP 2b).")
        a("- Nine templates with unit tests (STEP 3).")
        a("- Composition and all z3 filters.")
        a("- Stratified selection of 250 main + 100 reserve sentences.")
        a("- Pre-registration (STEP 5).")
        a("- The FULL typed-perturbation suite with controls (STEP 9).")
        a("- Known-label check item selection (8a).")
        a("- Disguise with its guard (STEP 10).")
        a("- Assembly and validation (STEP 11).")
        a("")
        a("What is PENDING (needs OpenRouter):")
        a("- 2c Sonnet lexicon audit.")
        a("- 4a fluency rating.")
        a("- 4b Sonnet reference audit.")
        a("- 6 generation: about 3.1k calls.")
        a("- 7 solver labels: CPU only, but they need the candidates.")
        a("- 8 known-label check and adjudication.")
        a("- The top-up (if it fires) and the testability declaration.")
        a("")
        a("**To finish:** run `./run_all.sh`, or `nohup ./watch_and_run.sh &`, which waits for key budget. It runs every pending phase in the "
          "pre-registered order. Every call is cached, so re-running never re-bills. It then re-assembles `full_data_out.json`, adding the "
          "`rcomp_candidates` group, `rcomp_peers.json` and this card.")
        a("")
        a("Consequences for anyone reading the data NOW:")
        a("1. `rcomp_sentences` references are correct by construction, but their atom lexicon and reference audits are "
          "PENDING (`metadata_audit_status`). The final 250 may still change slightly: the post-audit selection drops "
          "flagged sentences and fills from the pre-audited spare set.")
        a("2. `perturb_suite` is final for the 200 E bases. The 100 R_COMP bases follow the R_COMP selection, so they are "
          "rebuilt deterministically by `run_all.sh`.")
        a("3. `adjudicator_check` rows carry their known labels; the adjudicator verdicts are PENDING.")
        a("4. `rcomp_candidates` is absent, because the aii schema forbids empty groups.")
    a("")
    a("## 1. Contents")
    rows = [["`full_data_out.json`", "aii `exp_sel_data_out`; groups " + ", ".join(f"`{k}` ({v})" for k, v in S["groups"].items())],
            ["`mini_data_out.json` / `preview_data_out.json`", "first 3 rows per group (preview: strings cut to 200 chars)"],
            ["`lexicon.json`", f"{S['lexicon']['n_entries']} atom-lexicon entries (atom ⇄ 3sg verb phrase) with provenance and audit status"],
            ["`prereg_rcomp.json`", "pre-registration, frozen before generation (sha256 in §5)"],
            ["`adjudication_prompt.txt`", f"shared ADJ-PROMPT, the verbatim sibling R_ADJ V1 (sha256 `{ADJ['system_prompt_sha256'][:16]}…`)"],
            ["`rcomp_peers.json`", "every generator output per sentence" + ("" if has_c else " (written once generation has run)")],
            ["`cost_ledger.jsonl`", "one line per OpenRouter call"],
            ["`work/`", "intermediates: source_rules, lexicon_checked, rcomp_pool (5,109 filtered compositions), rcomp_preselect, "
                        "rcomp_sentences, perturb_* and all logs/statistics (`stats.json`)"]]
    a(table(rows, ["file", "what"]))
    a("")
    a("Row format (all groups):")
    a("- `input` is a JSON string `{text, candidate_fol, reference_fol (= weak reading, E-compatible), reference_fol_weak, "
      "reference_fol_strong, system, prompt_variant}`. Sentence rows have no candidate.")
    a("- `output` is the label:")
    a("  - candidates: CORRECT / ERROR / CONTESTED / UNRESOLVED / UNPARSEABLE;")
    a("  - PERTURB: ERROR; PERTURB_CONTROL: CORRECT;")
    a("  - adjudicator_check: the known label;")
    a("  - sentences: the reference status.")
    a("- `item_id` = sha1(system|norm(text)|raw_output)[:16], dataset E's recipe. For perturbation rows `raw_output` is the "
      "mutant string and `system` is `PERTURB:<op>:<polarity>` or `CONTROL:<type>`.")
    a("")
    a("## 2. Provenance: sources, atom pool and lexicon")
    sp = S["source_pool_log"]
    a("Source atom pool (STEP 1, `src/source_pool.py`; screen exclusion is E's `build_exclusion()`):")
    a(f"- Exclusion hashes: {sp['exclusion_hash_count']}.")
    a(f"- Rows read: (a) {sp['a_rows']} E heldout TRUSTED_AGREED/GOLD_PANEL_OK rows; (b) {sp['b_rows']} FOLIO-v2-train premises "
      "agreeing with folio-refined (IDENTICAL_STRING/EQ/VOCAB).")
    a(f"- Removed: {sp['fewshot_excluded']} of E's few-shot exemplars; {sp['screen_collisions']} screen collisions.")
    a(f"- Kept: {sp['rules']} universal rules with at least one atom over the rule's variable ({sp['shaped']} of them shaped "
      f"∀x(L1[∧L2[∧L3]]→L)); {sp['atoms_total']} atoms.")
    a(f"- By source: {j(sp['by_source'])}.")
    a("- The MALLS fallback was not needed.")
    a("")
    lc = S["lexicon_check_log"]
    a("Lexicon extraction and checks (STEP 2):")
    a("- **2a extraction.** `anthropic/claude-haiku-4.5`, 5 rules per call, temperature 0. Selection was greedy by atom "
      "novelty, capped at 320 rules. The $0.4 cap was reached after 67 calls and 57/64 jobs. 10 answers were truncated at "
      "1,500 tokens; their complete objects were salvaged at $0.")
    a(f"- **2b deterministic checks.** {lc.get('checked')} entries checked; {lc.get('pass')} pass; {lc.get('skip', 0)} "
      f"SKIPped by the extractor. Failures: {j({k: v for k, v in lc.items() if k.startswith('fail_')})}.")
    a("  - STEM: every content word of the phrase is a Porter stem of a source-sentence word, or a WordNet "
      "synonym/derivation of one.")
    a("  - NOT_VBZ: spaCy VBZ/MD first token.")
    a("  - NO_NEG: negation marker.")
    a("  - CONST_MISSING: a binary atom's constant must appear in the phrase.")
    a("  - DANGLING_PRONOUN: added here. It rejects antecedent-less them/it/this…; see §12.")
    a("  - Sortal = the phrase is 'is a/an N'. The noun keeps the phrase's own casing.")
    a(f"- **2c Sonnet audit.** Audit status counts: {j(S['lexicon']['audit_counts'])}. The WRONG rate (Wilson 95% CI) is "
      f"{S['lexicon_audit_wrong_rate'] or 'PENDING'}. An audited-WRONG entry is never used: compose.py rejects any "
      "sentence that draws one. That rejection, rather than removal, keeps all other sentences identical across the audit.")
    sc = json.loads((W / "executor_lexicon_spotcheck.json").read_text()) if (W / "executor_lexicon_spotcheck.json").exists() else None
    if sc:
        a(f"- **Executor spot audit (NOT the pre-registered 2c audit).** {sc['n']} sha1-sampled entries used in the main "
          f"sentences were checked by hand against source sentence + formula: {sc['wrong']} wrong, {sc['minor_grammar']} "
          f"minor grammar ('is archaea'). Wrong rate {sc['wrong']}/{sc['n']}, Wilson 95% upper bound {sc['wrong_rate_wilson95'][2]}. "
          "File: `work/executor_lexicon_spotcheck.json`.")
    a(f"- **2e name collisions.** {S['lexicon']['log'].get('renamed', 0)} entries renamed Name_k. "
      f"{S['lexicon']['log'].get('dup_atom_vp', 0)} duplicate (atom, phrase) pairs merged.")
    a("- **2f sort groups** (a group is usable with at least 12 non-sortal entries from at least 4 rules and at least 1 sortal noun):")
    a("")
    a(table([[g, v["n_sortal"], v["n_nonsortal"], v["n_rules_nonsortal"], v["usable"]] for g, v in S["lexicon"]["groups"].items()],
            ["group", "sortal nouns", "non-sortal entries", "source rules", "usable"]))
    a("")
    a("## 3. Templates, readings, composition and selection")
    a("The weak and strong readings are derived from the SAME slots that fill the text (`src/templates.py`).")
    a("- `tests/test_templates.py` (9 tests, all pass) checks, on hand-written instances:")
    a("  - the exact text and FOL;")
    a("  - strong ⊨ weak and weak ⊭ strong for every exception template;")
    a("  - T8 strong ≡ weak ∧ converse, with the converse non-equivalent to both accepted readings;")
    a("  - T9's strong reading ≡ ∀x(…→(Q↔E));")
    a("  - no VACUOUS atom, and non-triviality.")
    a("- `tests/test_fol.py` (E's parser tests) passes unchanged.")
    a("- `tests/test_perturb.py` checks that the path-tracked edit generator reproduces `repair_census.edits` exactly.")
    a("")
    a(table([[t, v["text"], v["weak"], v["strong"]] for t, v in PR["templates_and_readings"].items()], ["id", "template", "weak", "strong"]))
    a("")
    a("**Executor read-through (10 filled instances per template): PASS, with notes.**")
    a("- All nine templates render grammatical English whose structure matches both readings.")
    a("- Content is often semantically odd, e.g. 'a sport orbits around a star'. The generic 'object' group mixes unrelated "
      "sources. This is expected of templated composition, and fluency is rated on grammar only.")
    a("- Issues found and FIXED before selection:")
    a("  - lower-cased proper nouns ('prc national' → the noun now keeps the phrase casing);")
    a("  - antecedent-less pronouns ('processes them for…' → the DANGLING_PRONOUN check);")
    a("  - near-duplicate atoms in one sentence ('attends the conference remotely … unless they attend the conference' → "
      "content-stem overlap guard).")
    a("")
    cl = S["compose_log"]
    a("Composition (sha1-seeded, 600 draws per template) and the pre-registered filters, in order:")
    a(f"- Composed: {cl['composed']}. Rejected compositions: "
      f"{j({k: v for k, v in cl.items() if k.startswith('compose_') and k != 'compose_ok'})}.")
    a(f"- words ≥ 25: {cl['f1_words_ge25']}.")
    a(f"- nconds(weak) ≥ 3: {cl['f2_nconds_ge3']}.")
    a(f"- ≥ 2 non-sortal restrictor atoms: {cl['f3_restrictor_nonsortal_ge2']}.")
    a(f"- z3 non-trivial (not valid, not unsat, weak ≢ strong, no VACUOUS atom): {cl['f4_z3_nontrivial']}.")
    a(f"- No screen hash collision: {cl['f5_no_screen_collision']}.")
    a(f"- No string or combination duplicate: {cl['f6_no_dup']}.")
    a("")
    sl = S["select_log"]
    a("Selection (`src/select_rcomp.py`):")
    a("- Preselect for fluency/audit: 276 main candidates at usage cap 4 (the pool's cap-4 capacity), plus 130 reserve.")
    a(f"- Final main set: {sl['main']}. Per template: {j(sl['main_per_template'])}. Per word bin: "
      f"{j(sl['main_per_bin'])} (mean {S['words_mean_main']} words).")
    a(f"- Sort groups: {j(sl['main_per_group'])}.")
    a(f"- Maximum lexicon-entry usage: {sl['max_usage_main']}.")
    a(f"- Sentences with one negated condition: {S['negated_condition_share_main']}.")
    a(f"- E's `exception_type()` on the main set: {j(S['exception_type'])}. T3/T8 carry proviso/only-if markers that E's "
      "function does not know; use `metadata_clause_type`.")
    a(f"- TOP-UP RESERVE: {sl['reserve']} sentences (T1/T2/T7; 3 conditions; not nested).")
    a(f"- Fluency: {S['fluency_distribution']}.")
    a(f"- Reference audit REF_FLAGGED rate (Wilson 95% CI): preselect {S['reference_audit_flag_rate_preselect']}; "
      f"selected {S['reference_audit_flag_rate_selected']}.")
    a("")
    a("## 4. Adjudicator")
    a(f"- Model: `{ADJ['model']}`. Params: {j(ADJ['params'])}. Fallback: `{ADJ['fallback']}`.")
    a(f"- Source: {ADJ['source']}.")
    a(f"- System prompt: `adjudication_prompt.txt`, the sibling's V1 verbatim (sha256 `{ADJ['system_prompt_sha256']}`).")
    a("- The only R_COMP addition is in the user message:")
    a("  - both readings, tagged 'REFERENCE FOL (VERIFIED), reading 1 (weak exception)' and 'reading 2 (strong exception)'. "
      "T3 uses 'weak/strong proviso'; T8 uses 'literal only-if' / 'biconditional'.")
    a("  - the line 'A translation equivalent in meaning to either reading is faithful.'")
    a(f"- Sibling gate status at assembly: **{S['sibling_gate_status']}**. {ADJ['sibling_gate_status_at_copy']}")
    a(f"- In-stratum known-label check (8a; 30 PERTURB + 30 PERTURB_CONTROL on R_COMP bases, identical prompt): {S['adjudicator_check']}.")
    a("- Lexicon extraction (Haiku), audit and adjudication (Sonnet) are all Anthropic models. That family is disjoint from "
      "every generator and every metric judge (Gemini/OpenAI/Qwen).")
    a("")
    a("## 5. Pre-registration and testability")
    a(f"- `prereg_rcomp.json` sha256 **`{hashlib.sha256(PRE.read_bytes()).hexdigest()}`**, frozen {PR['frozen_at_utc']}, "
      "before any generation.")
    a(f"- Testability rule: {PR['testability_rule']}.")
    a(f"- Top-up rule: {PR['topup_rule']}.")
    decl = PR.get("testability_declaration")
    a("")
    a("**TESTABILITY DECLARATION** (made after labelling and before any metric; copied into `prereg_rcomp.json`):")
    if decl:
        a("")
        a(table([[k, v["correct_rows"], v["correct_sentences"], v["error_rows"], v["error_sentences"], v["testable"]]
                 for k, v in decl.items() if isinstance(v, dict) and "testable" in v],
                ["pool", "CORRECT rows", "CORRECT sentences", "ERROR rows", "ERROR sentences", "testable"]))
        a(f"\nVerdict: **{decl['verdict']}** (declared {decl.get('declared_at_utc')}).")
    elif T:
        a(f"computed but not yet declared: {j(T)}")
    else:
        a("PENDING: no R_COMP candidates exist yet (§0). R_COMP must not be used for any metric claim until this is filled.")
    a("")
    a("## 6. R_COMP candidate labels")
    a("Label rule (verbatim in `prereg_rcomp.json`):")
    a("- **Solver (E's labeller, against BOTH readings).**")
    a("  - EQ with either reading → CORRECT, tier A.")
    a("  - VOCAB/GRAN → routed P1. It is never auto-CORRECT: in E, 58 of 59 solver-to-panel transitions went CORRECT→ERROR.")
    a("  - TIMEOUT or COMPOUND → routed P2.")
    a("  - Minimal typed repair → ERROR(ops), tier A. ADD/DROP-only repairs, convention flags and T8 converse matches → routed P3.")
    a("  - A 20% sha1 sample of the other ERRORs → P4.")
    a("- **Adjudicator.**")
    a("  - Routed + FAITHFUL → CORRECT, tier B, correct_not_equivalent.")
    a("  - Routed + UNFAITHFUL → ERROR, tier B.")
    a("  - Solver ERROR + FAITHFUL → CONTESTED.")
    a("  - Solver ERROR + UNFAITHFUL → ERROR, tier A (confirmed).")
    a("  - AMBIGUOUS_READING → reading_choice; routed rows become CONTESTED.")
    a("  - Not reached before the cap: P1/P2 → UNRESOLVED; P3/P4 → the solver ERROR stays, with adj_pending.")
    a("  - A sentence with at least 2 reference_wrong adjudications → tier C (REF_FLAGGED).")
    a("  - If the sibling gate is not PASS, or the known-label BA is below 0.80, tier-B rows are `tier_b_provisional`.")
    if has_c:
        a("")
        a(f"- Final labels: {j(C['final_label'])}; tiers {j(C['tier'])}; solver labels {j(C['solver_label'])}.")
        a(f"- UNRESOLVED: {C['unresolved']}; adj_pending: {C['adj_pending']}.")
        a(f"- Weak-vs-strong acceptance: tier-A CORRECT {j(C['weak_vs_strong_tierA'])}; tier-B CORRECT (reading matched modulo "
          f"vocabulary) {j(C['weak_vs_strong_tierB_modulo_vocab'])}.")
        a(f"- ONLY_IF_CONVERSE rate among parseable T8 rows (Wilson): {C['only_if_converse_rate_T8']}.")
        a(f"- Solver × adjudicator confusion: {j(C['solver_vs_adjudicator'])}.")
        a(f"- Solver-ERROR precision from P4 (Wilson): {C['solver_error_precision_P4']}. E's value was 0.705.")
        a(f"- lex_anchored_vocab (DIAGNOSTIC; shares an instrument with L2-bow) × adjudicator on VOCAB_GRAN: "
          f"{j(C['lex_anchored_vs_adjudicator'])}.")
        a("")
        a("Label counts per template | exception type | tier:")
        a("")
        a(table([[k, j(v)] for k, v in C["template_x_exception_x_tier"].items()], ["template|exception|tier", "labels"]))
        a("")
        a("Error rate per system, R_COMP (tiers A+B) vs E's L25 (tiers A+B). Is R_COMP easier?")
        a("")
        keys = sorted(set(C["error_rate_per_system"]) | set(S["e_l25_error_rates"]))
        a(table([[k, (C["error_rate_per_system"].get(k) or {}).get("error_rate"), (C["error_rate_per_system"].get(k) or {}).get("n"),
                  (S["e_l25_error_rates"].get(k) or {}).get("error_rate"), (S["e_l25_error_rates"].get(k) or {}).get("n")] for k in keys],
                ["system", "R_COMP err", "n", "E L25 err", "n"]))
        a(f"\nUNPARSEABLE per system (kept, never dropped): {j(C['unparseable_per_system'])}")
    else:
        a("")
        a("Statistics PENDING (§0).")
        a("")
        a("E's L25 per-system error rates (tiers A+B), the comparison baseline for 'is R_COMP easier?':")
        a("")
        a(table([[k, v["error_rate"], v["n"]] for k, v in S["e_l25_error_rates"].items()], ["system", "E L25 error rate", "n"]))
    a("")
    a("## 7. PERTURB suite (metadata_fold PERTURB / PERTURB_CONTROL)")
    pl = S["perturb_log"]
    a("**Bases** (300, sha1 order): 36 TRUSTED_AGREED + 95 GOLD_PANEL_OK E references, 69 PANEL_REPAIRED (`base_trust="
      "panel_repaired`), and the first 100 R_COMP main sentences (weak reading; mutants also non-equivalent to strong and, "
      "for T8, the converse).")
    a("")
    a("**Mutants.**")
    a("- Generator: E's `repair_census.edits(base, donor)` used FORWARD, through a path-tracked mirror that tests prove "
      "identical, plus own ADD_INTERNAL and MEANING_RENAME operators. The donor is a sha1-chosen base from a different "
      "source with no shared predicate.")
    a("- Validity checks:")
    a("  - emit→parse round-trip, with a minimal-parenthesis printer;")
    a("  - no free variables (418 root-level ADD_FOREIGN mutants with an unbound x were rejected);")
    a("  - z3 non-equivalent at 3 s to the base and every accepted reading (UNKNOWN discarded);")
    a("  - non-trivial if the base is;")
    a("  - no duplicates.")
    a(f"- Tested {pl.get('tested')}; rejected {pl.get('equivalent')} equivalent, {pl.get('trivial')} trivial, "
      f"{pl.get('free_variable', 0)} free-variable.")
    a(f"- Positions skipped for polarity: {pl.get('skip_polarity_NONMONO')} NONMONO, {pl.get('skip_polarity_VACUOUS', 0)} VACUOUS.")
    a(f"- **{pl['mutants']} mutants, {pl['controls']} controls**; {S['matched_pairs']['complete']} complete DOWN/UP matched "
      "pairs.")
    a("")
    a(table([[k, v] for k, v in S["perturb_op_pol"].items()], ["operator:polarity", "rows"]))
    a("")
    a(table([[k, v["rows_in_complete_pairs"], v["rows_unpaired"]] for k, v in S["matched_pair_coverage_by_op"].items()],
            ["operator", "rows in complete DOWN/UP pairs", "unpaired rows"]))
    a("")
    a("Coverage notes:")
    a("- QUANT, REV and RESTR edit the top quantifier or the top implication. Their syntactic position is always UP, so "
      "they have no DOWN twin.")
    a("- MOVE (exportation) is almost always logically EQUIVALENT, so it is rejected (6 rows).")
    a("- SCOPE and UNGLUE need nested or glued quantifier blocks, which these bases lack, so they have 0 rows.")
    a("- ADD rows use foreign-vocabulary atoms (ADD_FOREIGN, easy for lexical metrics) or existing atoms (subtype ADD_INTERNAL).")
    a("- MEANING_RENAME swaps a whole predicate for a non-synonymous donor predicate.")
    a("- Polarity:")
    a("  - atom-level ops (SWAP/BIND/MEANING_RENAME) use `fol.profile` (`polarity_method=semantic_profile`);")
    a("  - structural ops use the syntactic path polarity (`syntactic_path`);")
    a("  - NONMONO positions are excluded from the matched design.")
    a("")
    a(f"**Controls** (each z3-verified equivalent): {j(S['controls_by_type'])}.")
    a("- RENAME_SYN uses a mutual-first-sense, noun-only WordNet synonym; otherwise RENAME_NONCE is used.")
    a("- Iteration 3 should analyse RENAME_SYN and RENAME_NONCE separately. A nonce rename breaks the text-to-vocabulary "
      "link, which a text-grounded metric may legitimately penalise.")
    a("- Some synonyms are archaic (China→Cathay).")
    a("- The solver labels most RENAME_SYN rows ERROR(ADD+DROP) (dry run: 5/10). That is why ADD/DROP-only solver ERRORs are "
      "routed to adjudication.")
    a("")
    a("## 8. Disguise")
    g = S["disguise_guard"]
    a("E's `disguise.py` is applied per sentence. The bijection is built over the text and ALL formulas of that sentence "
      "(both readings, the converse, candidates, mutants and controls).")
    a(f"- Guard: plain-z3 equivalence of formula pairs before vs after disguise, on {g['sentences_checked']} sentences / "
      f"{g['pairs_checked']} pairs: **{g['mismatches']} mismatches**.")
    a("")
    vr = json.loads((W / "verify_report.json").read_text()) if (W / "verify_report.json").exists() else None
    a("### Independent re-verification (`src/verify.py`)")
    a("Every row is re-checked from `full_data_out.json`, without reusing the generator's verdicts:")
    a("- PERTURB mutants: z3 (8 s) proves each NOT equivalent to the base and to every accepted reading.")
    a("- Controls: z3 proves each EQUIVALENT to the base (RENAME after the inverse map).")
    a("- R_COMP sentences: weak ≢ strong; every lexicon phrase occurs in the text and every atom in the weak reading; "
      "the sentence_id and item_id recipes hold.")
    a("- IDs are unique within each group.")
    a(f"- Result: {j(vr['counts']) if vr else 'not run'}; **{len(vr['failures']) if vr else 'n/a'} failures**.")
    a("")
    a("## 9. Costs")
    a(table([[k, v["usd"], v["calls"]] for k, v in S["cost_by_phase"].items()], ["phase", "USD", "calls"]))
    a(f"\nTotal ${S['cost_total_usd']}. Plan caps: {j(PR['caps_usd'])}.")
    a("")
    a("## 10. Licences")
    a("- FOLIO (tasksource/folio v2): CC-BY-SA-4.0.")
    a("- folio-refined (yfxiao): MIT.")
    a("- MALLS-v0.1 (yuan-yang): CC-BY-NC-4.0. The E GOLD_PANEL_OK / PANEL_REPAIRED bases and the lexicon entries mined from them "
      "inherit it: non-commercial.")
    a("- DSAVlab-UNIUD curated FOLIO/MALLS (exclusion only): per their cards.")
    a("- Generator outputs follow each provider's terms.")
    a("- The composed sentences are new text built from those sources.")
    a("")
    a("## 11. Known biases and limitations")
    a("- **Templated English.** It is cleaner and more regular than natural text, with a fixed set of 9 templates × 2 "
      "surface variants. R_COMP is evidence for a 'reference-trusted long stratum', NOT for natural text, and must never "
      "be pooled with E. §6 compares per-system error rates with E's L25.")
    a("- **Semantic incoherence.** Conditions are drawn across unrelated source rules inside a sort group, so many sentences "
      "are odd. The 'object' group (136/250) is the worst. Generators may treat absurd content differently from natural "
      "content.")
    a("- **Anthropic family throughout.** Haiku extracts the lexicon; Sonnet audits and adjudicates. The audit filter can "
      "favour Sonnet-legible sentences.")
    a("- **R_COMP and R_ADJ are not independent.** They share the adjudicator for CORRECT rows, and tier-A CORRECT is "
      "scarce (plain EQ needs the reference's own predicate names).")
    a("- **Unaudited lexicon (current state).** Until 2c runs, trust rests on the deterministic checks plus the source "
      "formulas, not on an audit.")
    a("- **Lexicon inherits source errors.** An atom's phrase is only as right as the source formula's atom. E's "
      "GOLD_PANEL_OK references passed a strict panel; FOLIO premises passed the tasksource/folio-refined agreement filter.")
    a("- **PERTURB is a synthetic diagnostic.** It must never be pooled with real errors. Its error distribution is not "
      "the real one, and ADD_FOREIGN / MEANING_RENAME use foreign vocabulary.")
    a("- **Descriptive system rankings only.** There is one prompt per generator at temperature 0.")
    a("")
    a("## 12. Deviations from the plan (all logged)")
    a("1. **OpenRouter key exhausted.** Every paid phase after 2a is pending (§0). Nothing was substituted: no generator "
      "family, adjudicator or local model stands in.")
    a("2. **2a truncation.** The extraction cap stopped 7 of 64 jobs (35 rules). 10 truncated answers were salvaged "
      "object by object; one wasted retry each (≈$0.06).")
    a("3. **2b additions.** DANGLING_PRONOUN check; the sortal requires 'is a/an N'; 'cannot' counts as negation; the STEM "
      "exemption list covers function words and prepositions, not only auxiliaries and articles.")
    a("4. **Lexicon audit handling.** Audited-WRONG entries are kept in `lexicon.json` with their status and rejected at "
      "composition, not removed. This keeps the sha1-seeded composition stable.")
    a("5. **Usage cap.** Each lexicon entry is used in at most 4 main sentences, and separately at most 4 reserve sentences. "
      "The lexicon's non-sortal capacity (~1,636 slots) is below 350 × 5.")
    a("6. **Preselect size.** Fluency and the reference audit are planned on 406 preselected sentences (276 main + 130 "
      "reserve), not ~450.")
    a("7. **Composition guard.** Added a content-stem overlap guard between the atoms of one sentence.")
    a("8. **Adjudicator settings.** `max_tokens` is 300, not 200, to match the sibling R_ADJ exactly (join).")
    a("9. **AMBIGUOUS_READING on routed rows.** These become CONTESTED with reading_choice (the plan does not fix the output).")
    a("11. **Audit caps raised.** Lexicon audit $0.4→$0.5 and reference audit $0.5→$0.7, both from the plan's $2.6 reserve. "
      "The projection from the observed per-call token use (compact JSON) is ≈$0.43 and ≈$0.54. A phase-cap stop is a "
      "planned truncation (exit 0); only the OpenRouter key limit stops `run_all.sh` (exit 3).")
    a("10. **Exclusion data restored.** `raw/hf/tasksource__folio` (deleted in E as redownloadable) was re-downloaded, as "
      "E's README describes, for `build_exclusion()` and `ctrl_pool()`.")
    a("")
    a("## 13. How iteration 3 should use this")
    a("- **Primary pool (R_COMP).** Tiers A+B; exclude CONTESTED, reading_choice and REF_FLAGGED; bootstrap by `sentence_id`.")
    a("- **Robustness.** Tier A only; report with and without `topup_batch`; flag `tier_b_provisional`.")
    a("- **PERTURB.** Per-operator sensitivity within `matched_pair_id` (DOWN vs UP), and invariance on PERTURB_CONTROL "
      "split by `metadata_subtype`.")
    a("- **Join keys.** `item_id` (E recipe); `rcomp_peers.json` for graded consensus without new calls.")
    (ROOT / "dataset_card.md").write_text("\n".join(L) + "\n")
    print("card written", len(L), "lines")


if __name__ == "__main__":
    main()
