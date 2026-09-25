> NOTE (published copy): this file names server paths this repository
> does not publish (a stage it does not ship, or another run's workspace),
> so the steps that read them will not run from a clone as written:
>   /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3

# Dataset card: R_COMP (long composed sentences with trusted references) + PERTURB (typed perturbation suite)

Generated 2026-09-23 22:07 UTC by `src/card.py`. Run `run_u75jRHUss0zo`, invention iteration 2, `gen_art_dataset_3` (plan `gen_plan_dataset_2_idx4`). It builds on dataset E (`iter_1/gen_art/gen_art_dataset_1`) and never writes to it. Absolute workspace: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_dataset_3`.

## 0. Status: read this first
**The R_COMP candidate generation, labelling and adjudication have NOT run yet.** The shared OpenRouter key (a $50/day limit shared by every run on the machine) hit its daily limit at about 18:00 UTC on 2026-09-23, roughly five minutes into this module, after 67 lexicon-extraction calls ($0.414). The limit resets daily at 00:00 UTC, after this module's deadline (23:49 UTC). Every later poll (`logs/key_status.log`, every 5 min) showed `limit_remaining = 0`; the last line is `2026-09-23T21:48:40Z 0 (replacement key, usage_daily 50.06 at 21:39 UTC)`.

A replacement key arrived at about 21:38 UTC. It had already used its $50 daily limit before this module's first call ($50.06 used; a test call returned 403 'Key limit exceeded'). It stayed at 0 through the last poll at 22:07 UTC. To use it, prefix `./run_all.sh` with `OPENROUTER_API_KEY="$(cat /ai-inventor/aii_data/.secrets/openrouter_key.private)"`.

What IS complete ($0 phases, all deterministic and re-runnable):
- Source atom pool (STEP 1).
- Haiku lexicon extraction (STEP 2a): 57 of 64 jobs; the $0.4 cap stopped the rest.
- Deterministic lexicon checks (STEP 2b).
- Nine templates with unit tests (STEP 3).
- Composition and all z3 filters.
- Stratified selection of 250 main + 100 reserve sentences.
- Pre-registration (STEP 5).
- The FULL typed-perturbation suite with controls (STEP 9).
- Known-label check item selection (8a).
- Disguise with its guard (STEP 10).
- Assembly and validation (STEP 11).

What is PENDING (needs OpenRouter):
- 2c Sonnet lexicon audit.
- 4a fluency rating.
- 4b Sonnet reference audit.
- 6 generation: about 3.1k calls.
- 7 solver labels: CPU only, but they need the candidates.
- 8 known-label check and adjudication.
- The top-up (if it fires) and the testability declaration.

**To finish:** run `./run_all.sh`, or `nohup ./watch_and_run.sh &`, which waits for key budget. It runs every pending phase in the pre-registered order. Every call is cached, so re-running never re-bills. It then re-assembles `full_data_out.json`, adding the `rcomp_candidates` group, `rcomp_peers.json` and this card.

Consequences for anyone reading the data NOW:
1. `rcomp_sentences` references are correct by construction, but their atom lexicon and reference audits are PENDING (`metadata_audit_status`). The final 250 may still change slightly: the post-audit selection drops flagged sentences and fills from the pre-audited spare set.
2. `perturb_suite` is final for the 200 E bases. The 100 R_COMP bases follow the R_COMP selection, so they are rebuilt deterministically by `run_all.sh`.
3. `adjudicator_check` rows carry their known labels; the adjudicator verdicts are PENDING.
4. `rcomp_candidates` is absent, because the aii schema forbids empty groups.

## 1. Contents
| file | what |
|---|---|
| `full_data_out.json` | aii `exp_sel_data_out`; groups `rcomp_sentences` (350), `perturb_suite` (5102), `adjudicator_check` (60) |
| `mini_data_out.json` / `preview_data_out.json` | first 3 rows per group (preview: strings cut to 200 chars) |
| `lexicon.json` | 652 atom-lexicon entries (atom ⇄ 3sg verb phrase) with provenance and audit status |
| `prereg_rcomp.json` | pre-registration, frozen before generation (sha256 in §5) |
| `adjudication_prompt.txt` | shared ADJ-PROMPT, the verbatim sibling R_ADJ V1 (sha256 `32bcc0f9a0cd35db…`) |
| `rcomp_peers.json` | every generator output per sentence (written once generation has run) |
| `cost_ledger.jsonl` | one line per OpenRouter call |
| `work/` | intermediates: source_rules, lexicon_checked, rcomp_pool (5,109 filtered compositions), rcomp_preselect, rcomp_sentences, perturb_* and all logs/statistics (`stats.json`) |

Row format (all groups):
- `input` is a JSON string `{text, candidate_fol, reference_fol (= weak reading, E-compatible), reference_fol_weak, reference_fol_strong, system, prompt_variant}`. Sentence rows have no candidate.
- `output` is the label:
  - candidates: CORRECT / ERROR / CONTESTED / UNRESOLVED / UNPARSEABLE;
  - PERTURB: ERROR; PERTURB_CONTROL: CORRECT;
  - adjudicator_check: the known label;
  - sentences: the reference status.
- `item_id` = sha1(system|norm(text)|raw_output)[:16], dataset E's recipe. For perturbation rows `raw_output` is the mutant string and `system` is `PERTURB:<op>:<polarity>` or `CONTROL:<type>`.

## 2. Provenance: sources, atom pool and lexicon
Source atom pool (STEP 1, `src/source_pool.py`; screen exclusion is E's `build_exclusion()`):
- Exclusion hashes: 2054.
- Rows read: (a) 131 E heldout TRUSTED_AGREED/GOLD_PANEL_OK rows; (b) 1507 FOLIO-v2-train premises agreeing with folio-refined (IDENTICAL_STRING/EQ/VOCAB).
- Removed: 6 of E's few-shot exemplars; 0 screen collisions.
- Kept: 874 universal rules with at least one atom over the rule's variable (580 of them shaped ∀x(L1[∧L2[∧L3]]→L)); 2306 atoms.
- By source: `{"E_heldout_TRUSTED_AGREED": 15, "E_heldout_GOLD_PANEL_OK": 88, "FOLIO-v2-train_agreed": 771}`.
- The MALLS fallback was not needed.

Lexicon extraction and checks (STEP 2):
- **2a extraction.** `anthropic/claude-haiku-4.5`, 5 rules per call, temperature 0. Selection was greedy by atom novelty, capped at 320 rules. The $0.4 cap was reached after 67 calls and 57/64 jobs. 10 answers were truncated at 1,500 tokens; their complete objects were salvaged at $0.
- **2b deterministic checks.** 801 entries checked; 762 pass; 6 SKIPped by the extractor. Failures: `{"fail_DANGLING_PRONOUN": 8, "fail_CONST_MISSING": 5, "fail_NOT_VBZ": 11, "fail_STEM": 16, "fail_BAD_NOUN": 1}`.
  - STEM: every content word of the phrase is a Porter stem of a source-sentence word, or a WordNet synonym/derivation of one.
  - NOT_VBZ: spaCy VBZ/MD first token.
  - NO_NEG: negation marker.
  - CONST_MISSING: a binary atom's constant must appear in the phrase.
  - DANGLING_PRONOUN: added here. It rejects antecedent-less them/it/this…; see §12.
  - Sortal = the phrase is 'is a/an N'. The noun keeps the phrase's own casing.
- **2c Sonnet audit.** Audit status counts: `{"PENDING": 652}`. The WRONG rate (Wilson 95% CI) is PENDING. An audited-WRONG entry is never used: compose.py rejects any sentence that draws one. That rejection, rather than removal, keeps all other sentences identical across the audit.
- **Executor spot audit (NOT the pre-registered 2c audit).** 40 sha1-sampled entries used in the main sentences were checked by hand against source sentence + formula: 0 wrong, 1 minor grammar ('is archaea'). Wrong rate 0/40, Wilson 95% upper bound 0.0876. File: `work/executor_lexicon_spotcheck.json`.
- **2e name collisions.** 6 entries renamed Name_k. 110 duplicate (atom, phrase) pairs merged.
- **2f sort groups** (a group is usable with at least 12 non-sortal entries from at least 4 rules and at least 1 sortal noun):

| group | sortal nouns | non-sortal entries | source rules | usable |
|---|---|---|---|---|
| event | 8 | 14 | 6 | True |
| person | 57 | 123 | 79 | True |
| object | 125 | 225 | 97 | True |
| animal | 24 | 21 | 13 | True |
| other | 13 | 18 | 11 | True |
| organisation | 4 | 7 | 3 | False |
| place | 7 | 6 | 3 | False |

## 3. Templates, readings, composition and selection
The weak and strong readings are derived from the SAME slots that fill the text (`src/templates.py`).
- `tests/test_templates.py` (9 tests, all pass) checks, on hand-written instances:
  - the exact text and FOL;
  - strong ⊨ weak and weak ⊭ strong for every exception template;
  - T8 strong ≡ weak ∧ converse, with the converse non-equivalent to both accepted readings;
  - T9's strong reading ≡ ∀x(…→(Q↔E));
  - no VACUOUS atom, and non-triviality.
- `tests/test_fol.py` (E's parser tests) passes unchanged.
- `tests/test_perturb.py` checks that the path-tracked edit generator reproduces `repair_census.edits` exactly.

| id | template | weak | strong |
|---|---|---|---|
| T1 | Every N who C1, who C2, and who C3 Q, unless the N E. | ∀x (S ∧ A1 ∧ A2 ∧ A3 ∧ ¬E → Q) | ∀x (S ∧ A1 ∧ A2 ∧ A3 → (Q ↔ ¬E)) |
| T2 | If a N C1 and C2, and the N also C3, then the N Q, except when the N E. | as T1 | as T1 |
| T3 | Any N that C1 and that C2 Q, provided that the N P and C3. | ∀x (S ∧ A1 ∧ A2 ∧ P ∧ A3 → Q) | ∀x (S ∧ A1 ∧ A2 → (Q ↔ (P ∧ A3))) |
| T4 | A N who C1 and who C2 Q as long as the N C3, unless the N E. | as T1 | as T1 |
| T5 | Every N who C1 and who C2 Q, provided that the N C3, unless the N E. | as T1 | as T1 |
| T6 | Except when the N E, every N who C1 and who C2 Q, provided that the N C3. | as T1 | as T1 |
| T7 | Anyone who C1, C2, and C3 Q unless they E. | ∀x (A1 ∧ A2 ∧ A3 ∧ ¬E → Q) | ∀x (A1 ∧ A2 ∧ A3 → (Q ↔ ¬E)) |
| T8 | If a N C1, C2, and C3, then the N Q, but only if the N P. | ∀x (S ∧ A1 ∧ A2 ∧ A3 ∧ Q → P) | ∀x (S ∧ A1 ∧ A2 ∧ A3 → (Q ↔ P)) |
| T9 | No N who C1, who C2, and who C3 Q, unless the N E. | ∀x (S ∧ A1 ∧ A2 ∧ A3 ∧ ¬E → ¬Q) | ∀x (S ∧ A1 ∧ A2 ∧ A3 → (¬Q ↔ ¬E)) |

**Executor read-through (10 filled instances per template): PASS, with notes.**
- All nine templates render grammatical English whose structure matches both readings.
- Content is often semantically odd, e.g. 'a sport orbits around a star'. The generic 'object' group mixes unrelated sources. This is expected of templated composition, and fluency is rated on grammar only.
- Issues found and FIXED before selection:
  - lower-cased proper nouns ('prc national' → the noun now keeps the phrase casing);
  - antecedent-less pronouns ('processes them for…' → the DANGLING_PRONOUN check);
  - near-duplicate atoms in one sentence ('attends the conference remotely … unless they attend the conference' → content-stem overlap guard).

Composition (sha1-seeded, 600 draws per template) and the pre-registered filters, in order:
- Composed: 5318. Rejected compositions: `{"compose_QX_same_rule": 80, "compose_conds_one_rule": 2}`.
- words ≥ 25: 5109.
- nconds(weak) ≥ 3: 5109.
- ≥ 2 non-sortal restrictor atoms: 5109.
- z3 non-trivial (not valid, not unsat, weak ≢ strong, no VACUOUS atom): 5109.
- No screen hash collision: 5109.
- No string or combination duplicate: 5109.

Selection (`src/select_rcomp.py`):
- Preselect for fluency/audit: 276 main candidates at usage cap 4 (the pool's cap-4 capacity), plus 130 reserve.
- Final main set: 250. Per template: `{"T1": 29, "T2": 28, "T3": 28, "T4": 28, "T5": 28, "T6": 28, "T7": 28, "T8": 25, "T9": 28}`. Per word bin: `{"25-29": 77, "30-34": 87, ">=35": 86}` (mean 32.98 words).
- Sort groups: `{"person": 78, "animal": 14, "object": 136, "other": 12, "event": 10}`.
- Maximum lexicon-entry usage: 4.
- Sentences with one negated condition: 0.396.
- E's `exception_type()` on the main set: `{"except": 89, "None": 52, "unless": 108, "without": 1}`. T3/T8 carry proviso/only-if markers that E's function does not know; use `metadata_clause_type`.
- TOP-UP RESERVE: 100 sentences (T1/T2/T7; 3 conditions; not nested).
- Fluency: PENDING.
- Reference audit REF_FLAGGED rate (Wilson 95% CI): preselect PENDING; selected PENDING.

## 4. Adjudicator
- Model: `anthropic/claude-sonnet-5`. Params: `{"temperature": 0.0, "max_tokens": 300, "reasoning": {"enabled": false}}`. Fallback: `anthropic/claude-sonnet-4.6`.
- Source: sibling R_ADJ workspace iter_2/gen_art/gen_art_dataset_2: work/pilot_results.json (sonnet5_off, mean $0.00276/call, 0 reasoning tokens) and prereg_radj.json.
- System prompt: `adjudication_prompt.txt`, the sibling's V1 verbatim (sha256 `32bcc0f9a0cd35dbd3ec6a4f7726f8094bca3a7785f2e9f0fbe509df7cbb3011`).
- The only R_COMP addition is in the user message:
  - both readings, tagged 'REFERENCE FOL (VERIFIED), reading 1 (weak exception)' and 'reading 2 (strong exception)'. T3 uses 'weak/strong proviso'; T8 uses 'literal only-if' / 'biconditional'.
  - the line 'A translation equivalent in meaning to either reading is faithful.'
- Sibling gate status at assembly: **VOID_KEY_OUTAGE**. VOID (OpenRouter key limit hit mid-gate, work/gate_report_VOID_key_outage.json); sibling dev-half balanced accuracy 0.730 for V1 and V2 (V1 kept by its tie rule) -> gate likely FAIL -> per plan every tier-B R_COMP label is PROVISIONAL unless the sibling gate is later PASSED
- In-stratum known-label check (8a; 30 PERTURB + 30 PERTURB_CONTROL on R_COMP bases, identical prompt): PENDING.
- Lexicon extraction (Haiku), audit and adjudication (Sonnet) are all Anthropic models. That family is disjoint from every generator and every metric judge (Gemini/OpenAI/Qwen).

## 5. Pre-registration and testability
- `prereg_rcomp.json` sha256 **`44445b3202e00f191fbc14c4e5338e2749d3cc8be1deed78c2a1e894973a3c75`**, frozen 2026-09-23T18:28:06Z, before any generation.
- Testability rule: R_COMP is TESTABLE iff tiers A+B hold >= 50 CORRECT and >= 50 ERROR LLM rows, each spread over >= 25 distinct sentences, excluding CONTESTED, reading_choice and REF_FLAGGED rows; declared (A+B and A-only) after labelling and BEFORE any metric runs.
- Top-up rule: after STEP 8, if tiers A+B hold < 50 CORRECT LLM rows or < 25 CORRECT sentences (likewise ERROR), generate, label and adjudicate the 100-sentence reserve with the full slot set (cap $1.3); flagged topup_batch; results reported with and without the top-up.

**TESTABILITY DECLARATION** (made after labelling and before any metric; copied into `prereg_rcomp.json`):
PENDING: no R_COMP candidates exist yet (§0). R_COMP must not be used for any metric claim until this is filled.

## 6. R_COMP candidate labels
Label rule (verbatim in `prereg_rcomp.json`):
- **Solver (E's labeller, against BOTH readings).**
  - EQ with either reading → CORRECT, tier A.
  - VOCAB/GRAN → routed P1. It is never auto-CORRECT: in E, 58 of 59 solver-to-panel transitions went CORRECT→ERROR.
  - TIMEOUT or COMPOUND → routed P2.
  - Minimal typed repair → ERROR(ops), tier A. ADD/DROP-only repairs, convention flags and T8 converse matches → routed P3.
  - A 20% sha1 sample of the other ERRORs → P4.
- **Adjudicator.**
  - Routed + FAITHFUL → CORRECT, tier B, correct_not_equivalent.
  - Routed + UNFAITHFUL → ERROR, tier B.
  - Solver ERROR + FAITHFUL → CONTESTED.
  - Solver ERROR + UNFAITHFUL → ERROR, tier A (confirmed).
  - AMBIGUOUS_READING → reading_choice; routed rows become CONTESTED.
  - Not reached before the cap: P1/P2 → UNRESOLVED; P3/P4 → the solver ERROR stays, with adj_pending.
  - A sentence with at least 2 reference_wrong adjudications → tier C (REF_FLAGGED).
  - If the sibling gate is not PASS, or the known-label BA is below 0.80, tier-B rows are `tier_b_provisional`.

Statistics PENDING (§0).

E's L25 per-system error rates (tiers A+B), the comparison baseline for 'is R_COMP easier?':

| system | E L25 error rate | n |
|---|---|---|
| F:fewshot_v1 | 0.522 | 23 |
| G1:fewshot_v1 | 0.963 | 80 |
| G1b:fewshot_v1 | 0.862 | 58 |
| G1b:zeroshot_v1 | 0.954 | 65 |
| G2:fewshot_v1 | 0.7 | 90 |
| G2:zeroshot_v1 | 0.829 | 41 |
| G3:fewshot_v1 | 0.794 | 97 |
| G4:fewshot_v1 | 0.492 | 59 |
| G5:fewshot_v1 | 0.937 | 63 |
| G6:fewshot_v1 | 0.747 | 95 |
| G7:fewshot_v1 | 0.635 | 52 |
| G8:fewshot_v1 | 0.764 | 55 |
| G9:fewshot_v1 | 0.926 | 95 |

## 7. PERTURB suite (metadata_fold PERTURB / PERTURB_CONTROL)
**Bases** (300, sha1 order): 36 TRUSTED_AGREED + 95 GOLD_PANEL_OK E references, 69 PANEL_REPAIRED (`base_trust=panel_repaired`), and the first 100 R_COMP main sentences (weak reading; mutants also non-equivalent to strong and, for T8, the converse).

**Mutants.**
- Generator: E's `repair_census.edits(base, donor)` used FORWARD, through a path-tracked mirror that tests prove identical, plus own ADD_INTERNAL and MEANING_RENAME operators. The donor is a sha1-chosen base from a different source with no shared predicate.
- Validity checks:
  - emit→parse round-trip, with a minimal-parenthesis printer;
  - no free variables (418 root-level ADD_FOREIGN mutants with an unbound x were rejected);
  - z3 non-equivalent at 3 s to the base and every accepted reading (UNKNOWN discarded);
  - non-trivial if the base is;
  - no duplicates.
- Tested 12225; rejected 5249 equivalent, 2324 trivial, 418 free-variable.
- Positions skipped for polarity: 1506 NONMONO, 20 VACUOUS.
- **4234 mutants, 868 controls**; 1354 complete DOWN/UP matched pairs.

| operator:polarity | rows |
|---|---|
| ADD:DOWN | 280 |
| ADD:UP | 281 |
| ADD_INTERNAL:DOWN | 60 |
| ADD_INTERNAL:UP | 140 |
| BIND:DOWN | 250 |
| BIND:UP | 231 |
| CONN:DOWN | 241 |
| CONN:UP | 289 |
| DROP:DOWN | 241 |
| DROP:UP | 51 |
| MEANING_RENAME:DOWN | 264 |
| MEANING_RENAME:UP | 234 |
| MOVE:UP | 6 |
| NEG:DOWN | 283 |
| NEG:UP | 300 |
| QUANT:UP | 281 |
| RESTR:UP | 279 |
| REV:UP | 281 |
| SWAP:DOWN | 134 |
| SWAP:UP | 108 |

| operator | rows in complete DOWN/UP pairs | unpaired rows |
|---|---|---|
| ADD | 560 | 1 |
| ADD_INTERNAL | 70 | 130 |
| BIND | 420 | 61 |
| CONN | 482 | 48 |
| DROP | 46 | 246 |
| MEANING_RENAME | 434 | 64 |
| MOVE | 0 | 6 |
| NEG | 566 | 17 |
| QUANT | 0 | 281 |
| RESTR | 0 | 279 |
| REV | 0 | 281 |
| SWAP | 130 | 112 |

Coverage notes:
- QUANT, REV and RESTR edit the top quantifier or the top implication. Their syntactic position is always UP, so they have no DOWN twin.
- MOVE (exportation) is almost always logically EQUIVALENT, so it is rejected (6 rows).
- SCOPE and UNGLUE need nested or glued quantifier blocks, which these bases lack, so they have 0 rows.
- ADD rows use foreign-vocabulary atoms (ADD_FOREIGN, easy for lexical metrics) or existing atoms (subtype ADD_INTERNAL).
- MEANING_RENAME swaps a whole predicate for a non-synonymous donor predicate.
- Polarity:
  - atom-level ops (SWAP/BIND/MEANING_RENAME) use `fol.profile` (`polarity_method=semantic_profile`);
  - structural ops use the syntactic path polarity (`syntactic_path`);
  - NONMONO positions are excluded from the matched design.

**Controls** (each z3-verified equivalent): `{"RENAME_NONCE": 159, "CONTRAPOSITIVE": 281, "REORDER_COMMUTE": 258, "RENAME_SYN": 141, "DEMORGAN": 8, "REORDER_QUANT": 21}`.
- RENAME_SYN uses a mutual-first-sense, noun-only WordNet synonym; otherwise RENAME_NONCE is used.
- Iteration 3 should analyse RENAME_SYN and RENAME_NONCE separately. A nonce rename breaks the text-to-vocabulary link, which a text-grounded metric may legitimately penalise.
- Some synonyms are archaic (China→Cathay).
- The solver labels most RENAME_SYN rows ERROR(ADD+DROP) (dry run: 5/10). That is why ADD/DROP-only solver ERRORs are routed to adjudication.

## 8. Disguise
E's `disguise.py` is applied per sentence. The bijection is built over the text and ALL formulas of that sentence (both readings, the converse, candidates, mutants and controls).
- Guard: plain-z3 equivalence of formula pairs before vs after disguise, on 30 sentences / 125 pairs: **0 mismatches**.

### Independent re-verification (`src/verify.py`)
Every row is re-checked from `full_data_out.json`, without reusing the generator's verdicts:
- PERTURB mutants: z3 (8 s) proves each NOT equivalent to the base and to every accepted reading.
- Controls: z3 proves each EQUIVALENT to the base (RENAME after the inverse map).
- R_COMP sentences: weak ≢ strong; every lexicon phrase occurs in the text and every atom in the weak reading; the sentence_id and item_id recipes hold.
- IDs are unique within each group.
- Result: `{"rcomp_sentences_rows": 350, "rcomp_sentences_dup_ids": 0, "perturb_suite_rows": 5102, "perturb_suite_dup_ids": 0, "perturb_rows_verified": 5102, "rcomp_sentences_verified": 350}`; **0 failures**.

## 9. Costs
| phase | USD | calls |
|---|---|---|
| lexicon_extraction | 0.4142 | 67 |

Total $0.4142. Plan caps: `{"lexicon_extraction": 0.4, "lexicon_audit": 0.4, "fluency": 0.1, "reference_audit": 0.5, "generation": 1.5, "known_label_check": 0.2, "adjudication": 2.5, "topup": 1.3, "reserve": 2.6, "hard_stop": 9.5}`.

## 10. Licences
- FOLIO (tasksource/folio v2): CC-BY-SA-4.0.
- folio-refined (yfxiao): MIT.
- MALLS-v0.1 (yuan-yang): CC-BY-NC-4.0. The E GOLD_PANEL_OK / PANEL_REPAIRED bases and the lexicon entries mined from them inherit it: non-commercial.
- DSAVlab-UNIUD curated FOLIO/MALLS (exclusion only): per their cards.
- Generator outputs follow each provider's terms.
- The composed sentences are new text built from those sources.

## 11. Known biases and limitations
- **Templated English.** It is cleaner and more regular than natural text, with a fixed set of 9 templates × 2 surface variants. R_COMP is evidence for a 'reference-trusted long stratum', NOT for natural text, and must never be pooled with E. §6 compares per-system error rates with E's L25.
- **Semantic incoherence.** Conditions are drawn across unrelated source rules inside a sort group, so many sentences are odd. The 'object' group (136/250) is the worst. Generators may treat absurd content differently from natural content.
- **Anthropic family throughout.** Haiku extracts the lexicon; Sonnet audits and adjudicates. The audit filter can favour Sonnet-legible sentences.
- **R_COMP and R_ADJ are not independent.** They share the adjudicator for CORRECT rows, and tier-A CORRECT is scarce (plain EQ needs the reference's own predicate names).
- **Unaudited lexicon (current state).** Until 2c runs, trust rests on the deterministic checks plus the source formulas, not on an audit.
- **Lexicon inherits source errors.** An atom's phrase is only as right as the source formula's atom. E's GOLD_PANEL_OK references passed a strict panel; FOLIO premises passed the tasksource/folio-refined agreement filter.
- **PERTURB is a synthetic diagnostic.** It must never be pooled with real errors. Its error distribution is not the real one, and ADD_FOREIGN / MEANING_RENAME use foreign vocabulary.
- **Descriptive system rankings only.** There is one prompt per generator at temperature 0.

## 12. Deviations from the plan (all logged)
1. **OpenRouter key exhausted.** Every paid phase after 2a is pending (§0). Nothing was substituted: no generator family, adjudicator or local model stands in.
2. **2a truncation.** The extraction cap stopped 7 of 64 jobs (35 rules). 10 truncated answers were salvaged object by object; one wasted retry each (≈$0.06).
3. **2b additions.** DANGLING_PRONOUN check; the sortal requires 'is a/an N'; 'cannot' counts as negation; the STEM exemption list covers function words and prepositions, not only auxiliaries and articles.
4. **Lexicon audit handling.** Audited-WRONG entries are kept in `lexicon.json` with their status and rejected at composition, not removed. This keeps the sha1-seeded composition stable.
5. **Usage cap.** Each lexicon entry is used in at most 4 main sentences, and separately at most 4 reserve sentences. The lexicon's non-sortal capacity (~1,636 slots) is below 350 × 5.
6. **Preselect size.** Fluency and the reference audit are planned on 406 preselected sentences (276 main + 130 reserve), not ~450.
7. **Composition guard.** Added a content-stem overlap guard between the atoms of one sentence.
8. **Adjudicator settings.** `max_tokens` is 300, not 200, to match the sibling R_ADJ exactly (join).
9. **AMBIGUOUS_READING on routed rows.** These become CONTESTED with reading_choice (the plan does not fix the output).
11. **Audit caps raised.** Lexicon audit $0.4→$0.5 and reference audit $0.5→$0.7, both from the plan's $2.6 reserve. The projection from the observed per-call token use (compact JSON) is ≈$0.43 and ≈$0.54. A phase-cap stop is a planned truncation (exit 0); only the OpenRouter key limit stops `run_all.sh` (exit 3).
10. **Exclusion data restored.** `raw/hf/tasksource__folio` (deleted in E as redownloadable) was re-downloaded, as E's README describes, for `build_exclusion()` and `ctrl_pool()`.

## 13. How iteration 3 should use this
- **Primary pool (R_COMP).** Tiers A+B; exclude CONTESTED, reading_choice and REF_FLAGGED; bootstrap by `sentence_id`.
- **Robustness.** Tier A only; report with and without `topup_batch`; flag `tier_b_provisional`.
- **PERTURB.** Per-operator sensitivity within `matched_pair_id` (DOWN vs UP), and invariance on PERTURB_CONTROL split by `metadata_subtype`.
- **Join keys.** `item_id` (E recipe); `rcomp_peers.json` for graded consensus without new calls.
