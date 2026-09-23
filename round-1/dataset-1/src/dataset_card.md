# Dataset card — held-out NL→FOL faithfulness meta-evaluation set (run_u75jRHUss0zo, invention iter 1, dataset E)

> **HELD-OUT: iteration 2 must not tune any threshold on these rows.** Use them once, to confirm a screen survivor
> whose thresholds are already frozen.

> **STATUS: PARTIAL. The LLM panel stage was BLOCKED.** The OpenRouter key is shared by every concurrent run and has a
> **$50/day limit**. Other runs used it up at about 13:29 UTC on 2026-09-23 (`GET /api/v1/key` → `limit_remaining = 0`,
> `usage_daily ≈ $50.06`). This run had spent $1.3927 by then. Everything that needs no LLM is complete:
> - all 600 sentences and all candidate generations (generation finished before the cut-off);
> - solver labels for every row;
> - the screen rebuild and its solver labels;
> - the synthetic panel gate.
>
> The following did not happen and are **pending**:
> - the blind panel pass (gold audit + tier-B adjudication);
> - the reference repair;
> - the track-H real-error accuracy (4c);
> - the screen panel audit.
>
> Consequences:
> - Every row the solver cannot settle (VOCAB_GRAN / COMPOUND / TIMEOUT) has `final_label = UNRESOLVED` (tier `none`).
> - Every CORRECT/ERROR label is solver-only and measured against an **UNAUDITED** reference: tier `A_unaudited_ref`. The
>   sibling run found ≈46% of MALLS gold wrong.
> - `src/resume_panel.sh` finishes all pending steps when the key has credit again. All steps are resumable and cached, and
>   the gated panel is already fixed. Re-running `assemble.py → stats.py → card.py → finalize.py` then upgrades labels in place.

## 1. Composition
- **heldout_sentences**: 600 screen-disjoint sentences.
  - MALLS-v0.1-train (GPT-4 gold): L25 = 200 (≥25 words and ≥3 gold conditions, spread evenly over 25-29 / 30-34 / ≥35
    words); L20 = 150 (20-24 words); EXC = 100 (all 67 parseable unless/except/excluding items, plus 33 'without' items
    with ≥15 words; XOR 'but not' excluded).
  - CTRL = 150 FOLIO-v2-train premises whose tasksource original ≡ folio-refined (bins 50 / 60 / 40 by length <12 / 12-19 /
    ≥20 words). agreement_type in CTRL: {'EQ': 24, 'VOCAB': 13, 'IDENTICAL_STRING': 113}. Identical strings are weak evidence: they show only
    that the refiner did not change the formula.
- **heldout_candidates**: 7307 rows. They come from:
  - 10 LLM slots over 9 families, few-shot, temperature 0: Llama-3.1-8B, Llama-3.3-70B, Qwen3-235B-A22B-2507,
    Mistral-Small-3.2, DeepSeek-V3.2 (reasoning off), Gemma-3-27B, Phi-4, GPT-4.1-mini, Gemini-2.5-Flash (reasoning off),
    Command-R7B;
  - the zero-shot Llama-3.3-70B variant;
  - the frontier model GPT-5.1 (effort low) on a 200-sentence subset;
  - ccg2lambda: 57 CTRL sentences matched in the train split, 17
    NLTK→FOL conversion failures and 7 parse failures, all kept as UNPARSEABLE. With fewer
    than about 60 rows, this system is not analysable on its own;
  - the MALLS GPT-4 gold itself, as system `malls_gpt4_gold` on the 450 MALLS sentences. Its label can only come from the
    blind gold audit, so it is UNRESOLVED while the panel is pending.
- **panel_calibration**:
  - the synthetic known-label gate: 77 items on 20 disjoint TRUSTED_AGREED CTRL-pool sentences (40 FAITHFUL = 20 strict
    z3-verified rewrites + 20 renames; 37 UNFAITHFUL z3-verified perturbations, 20 at DOWN sites and 17 at UP sites). Three
    sentences are single ground atoms and admit only one perturbation, so there are 77 items, not 80;
  - the 96 track-H human real-error pairs. With the ⊕ fix there are 96 non-equivalent pairs, not 99.
- **screen_audit**: 1173 rows (track L = Logic-LM released FOLIO-dev outputs; track H = the 302
  curated items), keyed by the screen's exact `item_id`. The same labels are in `screen_adjudicated_labels.json`.

## 2. Final label rule (plan 5f, verbatim; implemented in `src/assemble.py::final_rule`)
- auto CORRECT (plain z3 EQ to the reference) → final CORRECT, tier A. Panel dissent is logged as panel false-alarm evidence.
- auto ERROR(ops) → final ERROR(ops), tier A, unless ≥2/3 panel models say faithful → CONTESTED (a likely convention,
  aligner or reference issue; convention_flags are recorded).
- auto VOCAB_GRAN → panel majority: faithful → CORRECT (correct_not_equivalent=true, tier B); unfaithful →
  ERROR('MEANING_RENAME' + panel ops, tier B).
- auto COMPOUND or TIMEOUT_UNKNOWN → panel majority: unfaithful → ERROR('COMPOUND', panel ops, tier B); faithful → CORRECT
  (correct_not_equivalent=true, tier B).
- If the panel majority flags the sentence AMBIGUOUS, add reading_choice=true and keep it out of primary pooling, as a
  separate class.
- A missing vote (a model failed) with a 1-1 split → CONTESTED.
- UNPARSEABLE → final UNPARSEABLE, kept in the denominator.
- NO_TRUSTED_REFERENCE or DISPUTED_REFERENCE → final = panel majority, tier C (secondary only).

Primary analyses use tiers A+B, exclude CONTESTED, and report sensitivity with CONTESTED counted as CORRECT and as ERROR.

**Applied in this release (no panel votes):**
- tier A becomes `A_unaudited_ref`, because the reference audit is pending;
- VOCAB_GRAN / COMPOUND / TIMEOUT → `UNRESOLVED` (tier `none`);
- `malls_gpt4_gold` rows → `UNRESOLVED`.

`metadata_solver_lenient_label` (VOCAB_GRAN counted as CORRECT) is provided for SENSITIVITY ANALYSIS ONLY. The iter-3
review showed the aligner accepts meaning-changing renames (Sugar→MadeFromSugar), so it is not a label.

## 3. Label counts per stratum (LLM rows; each cell is rows (distinct sentences))
| stratum | sentences | rows | CORRECT A_unaudited | ERROR A_unaudited | UNRESOLVED | UNPARSEABLE |
|---|---|---|---|---|---|---|
| L25 | 200 | 2260 | 9 (6) | 131 (63) | 1833 | 287 |
| L20 | 150 | 1700 | 33 (20) | 227 (81) | 1268 | 172 |
| EXC | 100 | 1140 | 76 (25) | 218 (64) | 731 | 115 |
| CTRL | 150 | 1700 | 193 (28) | 433 (84) | 813 | 261 |

Solver auto-label distribution (LLM rows):
| stratum | CORRECT(EQ) | VOCAB_GRAN | ERROR | COMPOUND | TIMEOUT_UNKNOWN | UNPARSEABLE |
|---|---|---|---|---|---|---|
| L25 | 9 | 56 | 131 | 1777 | 0 | 287 |
| L20 | 33 | 94 | 227 | 1174 | 0 | 172 |
| EXC | 76 | 77 | 218 | 654 | 0 | 115 |
| CTRL | 193 | 231 | 433 | 582 | 0 | 261 |

Why the MALLS strata have almost no tier-A CORRECT: plain z3 EQ needs the SAME predicate names as the reference. LLMs choose
their own vocabulary, so a correct MALLS candidate is at best VOCAB_GRAN and needs the panel. CTRL gets CORRECT rows because
the FOLIO-style few-shot exemplars lead models to reuse FOLIO naming on short premises.

Sensitivity only, `solver_lenient_label`:
| stratum | CORRECT | CORRECT sents | ERROR | ERROR sents | UNRESOLVED | UNPARSEABLE |
|---|---|---|---|---|---|---|
| L25 | 65 | 30 | 131 | 63 | 1777 | 287 |
| L20 | 127 | 57 | 227 | 81 | 1174 | 172 |
| EXC | 153 | 44 | 218 | 64 | 654 | 115 |
| CTRL | 424 | 69 | 433 | 84 | 582 | 261 |

EXC by exception type: `{"except": {"CORRECT": 49, "UNRESOLVED": 93, "UNPARSEABLE": 41, "ERROR": 61}, "excluding": {"UNRESOLVED": 24, "ERROR": 1, "UNPARSEABLE": 9}, "unless": {"UNRESOLVED": 296, "UNPARSEABLE": 45, "CORRECT": 25, "ERROR": 106}, "without": {"UNRESOLVED": 318, "UNPARSEABLE": 20, "ERROR": 50, "CORRECT": 2}}`
CTRL by length bin: `{"0-11": {"CORRECT": 159, "UNRESOLVED": 200, "ERROR": 171, "UNPARSEABLE": 55}, "12-19": {"UNRESOLVED": 319, "UNPARSEABLE": 143, "CORRECT": 26, "ERROR": 185}, "20-inf": {"UNRESOLVED": 294, "ERROR": 77, "UNPARSEABLE": 63, "CORRECT": 8}}`

## 4. Testability declaration (frozen in prereg_strata.json before any metric run)
Rule: ≥50 ERROR rows AND ≥50 CORRECT rows AND ≥25 distinct sentences on each side, tier A+B only.
| stratum | OFFICIAL testable (A+B) | prov. ERROR rows/sents | prov. CORRECT rows/sents | prov. testable | prov. ERROR excl. ADD/DROP-only | prov.-strict testable |
|---|---|---|---|---|---|---|
| L25 | False | 131/63 | 9/6 | False | 39/18 | False |
| L20 | False | 227/81 | 33/20 | False | 78/35 | False |
| EXC | False | 218/64 | 76/25 | True | 115/46 | True |
| CTRL | False | 433/84 | 193/28 | True | 113/33 | True |

OFFICIAL: no stratum is testable, because tier A+B requires the panel. PROVISIONAL counts use tier A against unaudited
references. L25 top-up rule (frozen before labels): triggered = True, executed = False.
OpenRouter key daily limit exhausted (limit_remaining=0) — no generation possible.

## 5. Automatic labeller facts
- Repair status: `{"None": 2078, "COMPOUND_EXHAUSTED": 3183, "FOUND": 1009, "COMPOUND_TIMEOUT": 1004, "SKIPPED_EVENTSEM": 33}`. The 8 s budget (vs 25 s in iter 3) turns some COMPOUND results
  into timeouts; they are split into COMPOUND_TIMEOUT vs COMPOUND_EXHAUSTED.
- Equivalence status: `{"None": 859, "EQ": 761, "NONEQ": 5229, "VOCAB": 415, "GRAN": 43}`
- **Caveat for tier-A ERROR: ADD/DROP-only repairs.** 664 of 1009 solver ERROR
  rows (LLM systems) are repaired ONLY by ADD/DROP operators (ADD+DROP = 436). A depth-2 ADD+DROP
  "repair" replaces an unmatched candidate atom with the reference atom. That is exactly what a vocabulary or arity mismatch
  the iter-3 aligner cannot bridge looks like (e.g. Lunch(james) vs HasLunch(james, company)). The iter-3 review and the
  sibling screen executor flagged these as label artefacts, and the plan routes them to the panel for CONTESTED. Such rows
  carry `metadata_addrop_only_suspect = true`; the stricter provisional count in section 4 excludes them.
- Operator mass of solver ERROR rows: `{"ADD": 627, "DROP": 579, "CONN": 226, "NEG": 112, "BIND": 54, "REV": 17, "MOVE": 17, "SWAP": 15, "RESTR": 11, "QUANT": 9}`, depth `{"1": 351, "2": 658}`
- convention_flags (diagnostic only; they never change a label): `{"CONST_VS_EXISTS": 439, "ARITY_REIFY": 404, "SORTAL": 33, "XOR_OR": 32}`
- ⊕ precedence fix regression: re-running the 99-pair census makes 3 pairs equivalent (99→96 non-equivalent), and COMPOUND
  falls 36→33. This matches the review's 3 pure ⊕/→ bracketing items.
- Parser note: `fol.parse('')` returns an atom named None. Empty outputs are forced to UNPARSEABLE in the worker and in the
  assembler.
- The labeller's precision/recall against the panel majority, and the correct-but-not-equivalent rate, are **PENDING (panel)**.

## 6. Parse rate and auto labels per system × prompt variant
| system|variant | n | parse rate | CORRECT | VOCAB_GRAN | ERROR | COMPOUND | TIMEOUT |
|---|---|---|---|---|---|---|---|
| F:openai/gpt-5.1|fewshot_v1 | 200 | 0.965 | 24 | 27 | 40 | 102 | 0 |
| G1:meta-llama/llama-3.1-8b-instruct|fewshot_v1 | 600 | 0.7967 | 20 | 32 | 80 | 346 | 0 |
| G1b:meta-llama/llama-3.3-70b-instruct|fewshot_v1 | 600 | 0.8783 | 26 | 38 | 98 | 365 | 0 |
| G1b:meta-llama/llama-3.3-70b-instruct|zeroshot_v1 | 600 | 0.8833 | 21 | 41 | 106 | 362 | 0 |
| G2:qwen/qwen3-235b-a22b-2507|fewshot_v1 | 600 | 0.8167 | 27 | 47 | 102 | 314 | 0 |
| G3:mistralai/mistral-small-3.2-24b-instruct|fewshot_v1 | 600 | 0.9183 | 36 | 44 | 72 | 399 | 0 |
| G4:deepseek/deepseek-v3.2|fewshot_v1 | 600 | 0.9017 | 25 | 34 | 76 | 406 | 0 |
| G5:google/gemma-3-27b-it|fewshot_v1 | 600 | 0.9067 | 23 | 28 | 79 | 414 | 0 |
| G6:microsoft/phi-4|fewshot_v1 | 600 | 0.8867 | 32 | 60 | 90 | 350 | 0 |
| G7:openai/gpt-4.1-mini|fewshot_v1 | 600 | 0.8517 | 31 | 51 | 98 | 331 | 0 |
| G8:google/gemini-2.5-flash|fewshot_v1 | 600 | 0.9267 | 36 | 31 | 92 | 397 | 0 |
| G9:cohere/command-r7b-12-2024|fewshot_v1 | 600 | 0.8533 | 10 | 25 | 76 | 401 | 0 |
| ccg2lambda|none | 57 | 0.5789 | 0 | 0 | 0 | 33 | 0 |
| malls_gpt4_gold|none | 450 | 1.0 | 0 | 0 | 0 | 0 | 0 |

## 7. Panel calibration
Panel: Anthropic Haiku-4.5 (P1), Zhipu GLM-4.6 non-thinking (P3), Moonshot Kimi-K2-0905 (R1, the reserve replacing xAI
Grok-4.3). The panel is family-disjoint from all 9 generator families.

Gate: balanced accuracy ≥0.80, and recall ≥0.70 on each class. It is run in the exact production format (disguised,
batched per sentence, the reference shown among the variants).

**Prompt v1** (first attempt). It FAILED for every cheap model: faithful recall was 0.45-0.58, driven by contrapositive
rejection and by rename items. The v1 renames also came from WordNet first senses and turned out to change meaning
(In→Inch, At→Astatine, Band→Set). They were replaced with naming-convention renames (Is/Has prefix).
| member | model | n | bal.acc | rec F | rec U | U@DOWN | U@UP | STRICT | RENAME | ref accepted | gate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 | anthropic/claude-haiku-4.5 | 77 | 0.712 | 0.45 | 0.973 | 1.0 | 0.941 | 0.55 | 0.35 | 0.9 | fail |
| P2 | x-ai/grok-4.3 | 77 | 0.71 | 0.475 | 0.946 | 0.95 | 0.941 | 0.6 | 0.35 | 1.0 | fail |
| P3 | z-ai/glm-4.6 | 77 | 0.787 | 0.575 | 1.0 | 1.0 | 1.0 | 0.7 | 0.45 | 0.95 | fail |
| P1alt | anthropic/claude-sonnet-4.6 | 77 | 0.875 | 0.75 | 1.0 | 1.0 | 1.0 | 0.85 | 0.65 | 0.9 | PASS |

**Prompt v2** (adds one generic sentence: contrapositive / De Morgan / ¬¬ / nested quantifiers are equivalent). This is the
production prompt. Caveat: v2 was chosen after seeing the v1 gate on the same 77 items, so these gate numbers are optimistic.
The track-H real-error check (4c) is the independent accuracy estimate, and it is pending.
| member | model | n | bal.acc | rec F | rec U | U@DOWN | U@UP | STRICT | RENAME | ref accepted | gate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 | anthropic/claude-haiku-4.5 | 77 | 0.861 | 0.75 | 0.973 | 1.0 | 0.941 | 0.75 | 0.75 | 0.95 | PASS |
| P2 | x-ai/grok-4.3 | 77 | 0.773 | 0.6 | 0.946 | 0.95 | 0.941 | 0.7 | 0.5 | 1.0 | fail |
| P3 | z-ai/glm-4.6 | 77 | 0.85 | 0.7 | 1.0 | 1.0 | 1.0 | 0.75 | 0.65 | 0.9 | PASS |
| R1 | moonshotai/kimi-k2-0905 | 77 | 0.863 | 0.725 | 1.0 | 1.0 | 1.0 | 0.8 | 0.65 | 0.9 | PASS |
| R2 | minimax/minimax-01 | 77 | 0.674 | 0.375 | 0.973 | 0.95 | 1.0 | 0.35 | 0.4 | 0.95 | fail |

All three members pass: P1 Haiku, P3 GLM and R1 Kimi. P2 Grok-4.3 fails (faithful recall 0.60), so the reserve Kimi-K2
replaces it per plan 4b. MiniMax-01 also fails. Sonnet-4.6 passed only under v1 (0.875) but cost ≈4.6× Haiku in the gate ($0.196 vs $0.043 for 20 calls), so it is
not used.

Track-H real-error check (4c): {"pairs": 96, "votes_per_pair": {"3": 9, "2": 1, "1": 1, "0": 85}, "note": "4c was cut off by the key's daily limit after a few calls; accuracy is NOT reported (too few judgements)"}

Fleiss κ and the CONTESTED rate: PENDING (panel).

## 8. Disguise (plan 5a)
- Nonce CVCVC bijection per sentence over Porter stems of text words plus name tokens of ALL formulas of the sentence,
  seeded by sha1(sentence_id) and rejected if the nonce is a WordNet lemma. Name tokens that are WordNet synonyms of a
  sentence word reuse that word's nonce, so paraphrased names stay linked to the text.
- Guard (50 sentences): pairwise plain-z3 equivalence of class representatives before vs after disguise: `{"sentences": 50, "pairs": 932, "mismatches": 0, "z3_unknown_pairs": 0, "passed": true}`.
- Deviation: NLTK Porter stems are used instead of spaCy lemmas.

## 9. Disjointness and exclusion
- Exclusion hashes: 2054. Sources: `{"tasksource_folio_validation": 2634, "folio_refined_validation": 2634, "curated_folio": 859, "curated_malls": 200, "malls_test": 2000, "logiclm_context": 3876, "logiclm_question": 1224}`.
- Collisions after exclusion: **0**.
- MALLS pool: `{"raw": 27284, "gold_unparseable": 334, "excluded_screen_hash": 1, "dup_text": 30, "pool": 26919}`. CTRL pool: `{"story_matched": 1001, "agreement_IDENTICAL_STRING": 1465, "agreement_UNPARSEABLE": 147, "agreement_VOCAB": 15, "agreement_NONEQ": 20, "agreement_EQ": 27, "excluded_screen_hash": 3}`.
- Few-shot exemplars: 6, hand-picked from the sha1-ordered eligible CTRL pool and excluded from CTRL and calibration. The
  auto-pick contained wrong golds (e.g. Age(james, y) for 'the customers'); it is kept in work/fewshot_exemplars_autopick_rejected.json.

## 10. Screen rebuild
- Logic-LM records per file: {'gpt-3.5-turbo': 204, 'gpt-4': 204, 'text-davinci-003': 204}.
- Conclusion match rate: 112/202 = 0.554.
- Agreed-premise pool: 341. Items per track: {'L': 871, 'H': 302}. Track-L reference sources: `{"curated_corrected_conclusion": 307, "agreed_premise_IDENTICAL_STRING": 550, "agreed_premise_EQ": 7, "agreed_premise_VOCAB": 7}`.
- Screen auto labels per track: `{"L": {"ERROR": 225, "COMPOUND": 220, "VOCAB_GRAN": 146, "CORRECT": 166, "UNPARSEABLE": 62, "REF_UNPARSEABLE": 52}, "H": {"ERROR": 42, "UNPARSEABLE": 16, "CORRECT": 181, "COMPOUND": 34, "VOCAB_GRAN": 21, "REF_UNPARSEABLE": 8}}`
- Screen final labels (auto_only; panel pending): `{"L": {"ERROR": 225, "UNRESOLVED": 366, "CORRECT": 166, "UNPARSEABLE": 62, "NO_REFERENCE": 52}, "H": {"ERROR": 43, "UNPARSEABLE": 16, "CORRECT": 181, "UNRESOLVED": 52, "NO_REFERENCE": 8, "CONTESTED": 2}}`
- item_id = sha1(system + '|' + norm(text) + '|' + raw_fol)[:16], where norm = lowercase, apostrophes removed, punctuation
  stripped, whitespace collapsed. Raw join keys are stored in every row.

## 11. Cost (OpenRouter, from per-call usage.cost)
| phase | calls | USD |
|---|---|---|
| generation | 6859 | 0.903 |
| gate | 185 | 0.4289 |
| gate_trackh | 31 | 0.0609 |
Total $1.3927 of the $9.5 hard cap.

## 12. Licences, overlap and caveats
- MALLS-v0 (yuan-yang): CC-BY-NC-4.0 (non-commercial).
- FOLIO (tasksource/folio): CC (the FOLIO release is CC-BY-SA-4.0).
- folio-refined (yfxiao): MIT.
- folio_by_ccg2lambda: CC-BY-4.0.
- DSAVlab-UNIUD curated sets: FOLIO CC-BY-4.0, MALLS CC-BY-NC-4.0.
- Logic-LLM outputs: MIT.
- Generator outputs are subject to their providers' terms.
- Family overlap with the screen's judges: the Gemini-Flash family (G8) and Qwen (G2) are likely judge families in iteration
  2's experiments. Iteration 2's self-preference check must account for this; it does not change the labels.
- Single prompt per generator at temperature 0, so system-level rankings are descriptive only.
- ccg2lambda event-semantics rows are a separate system class and are never pooled with the LLM rows.
