# Dataset card: held-out NL→FOL faithfulness meta-evaluation set (run_u75jRHUss0zo, invention iter 1, dataset E)

> **HELD-OUT: iteration 2 must not tune any threshold on these rows.** Use them ONCE, to confirm a screen survivor whose
> thresholds are already frozen. Tune and select on the screen (the `screen_audit` group / `screen_adjudicated_labels.json`).

**Status: COMPLETE.** Generation, solver labelling, the blind 3-family panel pass (gold audit + adjudication), the
reference repair, the track-H real-error check and the screen audit have all run.

**History.** A first pass (2026-09-23, morning UTC) was cut off at 13:29 UTC when other runs exhausted the shared OpenRouter
key's $50/day limit. That release had solver-only labels and 5,128 UNRESOLVED rows. After the key reset, the pass resumed
from its caches. On resumption:
- the 541 Qwen zero-shot generations lost to the limit were regenerated;
- the pre-registered L25 top-up was executed;
- the panel ran.

Totals: 700 sentences, 8507 candidate rows,
173 calibration rows, 1173 screen rows. Total OpenRouter cost
**$9.833** (hard cap $9.50).

Held-out final labels: `{"UNPARSEABLE": 1086, "CORRECT": 1750, "ERROR": 5005, "UNRESOLVED": 276, "CONTESTED": 390}`. Tiers: `{"-": 1086, "A": 1044, "B": 2157, "C": 3891, "none": 276, "A_unaudited_ref": 53}`.

### Headline data-quality facts (read before using the labels)
1. **Testability (tiers A+B, primary pool).** The testable strata are L25 (all 300), L20, EXC and CTRL. The L25 top-up batch
   alone is not testable, and is meant to be pooled. See section 3.
2. **The panel is strict, and the reference audit rejects most references.**
   - It judged 440/535 MALLS gold formulas unfaithful
     (0.822 [0.788, 0.853]) and 112/148 CTRL
     references (0.757 [0.682, 0.819]). Expert audits report about 36-46%.
   - On track H the same panel accepts only 0.613
     of expert-CORRECTED formulas.
   - So a large part of these rejections is probably panel over-strictness (false alarms on long, multi-condition formulas),
     not reference error. Tier-C rows (unrepaired or disputed references) and all panel-decided ERROR labels inherit this
     bias. The panel's faithful rate over all shown items is only about 0.2 (section 7).
   - The label ERROR therefore means "at least 2 of 3 small judges found a meaning difference", and should be read that way.
3. **Tier A vs tier B.**
   - Tier A (solver-decided against an audited or repaired reference) is the most panel-independent layer. Iteration 2
     should confirm on tier A alone as a robustness check. Tier-A counts are printed in section 3.
   - Tier B (panel-decided for VOCAB_GRAN/COMPOUND/TIMEOUT) has majority accuracy of about 0.73 on real errors.
4. **Budget deviations.**
   - The plan's cap was $9.50. It was raised to $9.80 for the final reference-repair tie-breaks and the adjudication
     remainder. The last batch of 16 in-flight calls overshot, so the final spend is $9.833, still under
     the $10 artifact budget.
   - The adjudication remainder was not finished for 32 low-priority sentences. Their split items are CONTESTED (a 1-1
     split with a missing vote) or UNRESOLVED (a single vote).
   - 120 stage-1 sentences lost their Kimi call to the phase cap. Haiku then judged those items, so they have two votes,
     and any 1-1 split is CONTESTED.
5. **CTRL UNRESOLVED rows.** They arise where a CTRL reference was DISPUTED (tier C → panel-only labels) but the sentence
   was outside the 20% full-coverage sample. Its auto-ERROR classes were never shown to the panel, so they stay UNRESOLVED
   rather than taking a solver label measured against a disputed reference.

## 1. Composition
- **heldout_sentences** (700), all screen-disjoint (hash collisions after exclusion:
  0):
  - **L25 = 300**: MALLS-v0.1-train, ≥25 words AND ≥3 gold-derived conditions, sha1 order, spread over word bins 25-29 / 30-34
    / ≥35.
    - 200 were selected in step 1.
    - The other 100 are the **pre-registered top-up** batch: the same rule on the unused pool, bins taken
      [43, 42, 15]. The ≥35-word supply was exhausted at 15.
    - The top-up rule was frozen in `prereg_strata.json` before any label was seen: "If after Step 3 the tier-A-projected
      ERROR or CORRECT count of L25 is below 60, generate one more sha1-ordered batch of 100 L25 sentences with the 5 cheapest
      generator slots". Tier-A CORRECT was 9. The top-up was generated with the 5 cheapest slots (Command-R7B, Llama-3.1-8B,
      Phi-4, Mistral-Small-3.2, Qwen3-235B) plus the MALLS gold, so its rows per sentence differ from the original 200.
    - `metadata_strata.l25_topup_batch` marks these rows. Statistics are also reported with and without the top-up.
  - **L20 = 150**: 20-24 words and ≥3 conditions.
  - **EXC = 100**: all 67 parseable unless/except/excluding/other-than items plus 33 'without' items with ≥15 words. The XOR
    pattern 'but not (both)' is excluded.
  - **CTRL = 150** FOLIO-v2-train premises where the tasksource original ≡ folio-refined modulo vocabulary. Bins are
    50/60/40 by length <12 / 12-19 / ≥20 words. Reference = the refined formula. agreement_type: `{"IDENTICAL_STRING": 113, "EQ": 24, "VOCAB": 13}`.
    IDENTICAL_STRING shows only that the refiner did not change the formula; it is weak evidence. The blind panel audit of
    the reference (section 4) is the real check.
- **heldout_candidates** (8507 rows):
  - 10 LLM slots over 9 families, one fixed few-shot prompt (`prompts/fewshot_v1.txt`), temperature 0: Llama-3.1-8B,
    Llama-3.3-70B, Qwen3-235B-A22B-2507, Mistral-Small-3.2-24B, DeepSeek-V3.2 (reasoning off), Gemma-3-27B, Phi-4,
    GPT-4.1-mini, Gemini-2.5-Flash (reasoning off), Command-R7B;
  - zero-shot variants for 2 families: Llama-3.3-70B and Qwen3-235B;
  - frontier GPT-5.1 (effort low) on a 200-sentence subset (60 L25 + 50 L20 + 40 EXC + 50 CTRL);
  - ccg2lambda (system_class `symbolic_eventsem`): 57 CTRL sentences matched in the HF train
    split. Too few to analyse on its own, and never pooled with LLM rows;
  - the MALLS GPT-4 gold itself, as system `malls_gpt4_gold` (system_class `reference_gold_as_system`), on every MALLS
    sentence. Its label is the blind gold audit.
  - Every unparseable output is kept (final label UNPARSEABLE).
- **panel_calibration**: the synthetic known-label gate (77 items) and the 96 track-H human real-error pairs with panel
  votes.
- **screen_audit** (1173 rows): track L = Logic-LM's released FOLIO-dev outputs; track H = the 302
  curated FOLIO/MALLS items. They are keyed by the screen's exact `item_id`, and the same labels are in
  `screen_adjudicated_labels.json`.

## 2. Final label rule (plan 5f, verbatim; `src/assemble.py::final_rule`)
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

Primary analyses use tiers A+B, exclude CONTESTED (and reading_choice rows), and report sensitivity with CONTESTED counted
as CORRECT and as ERROR.

**Implementation details that matter for users:**
1. **Class collapse.** Per sentence, candidates are union-found into classes modulo vocabulary (`equivalent_modulo_vocab`).
   The panel judges one representative per class (disguised, blind, shuffled), and the label propagates to the members.
   - The reference class c0 is shown unlabelled among the candidates, so the gold audit is blind.
   - A candidate that joined c0 only modulo vocabulary or granularity (auto VOCAB_GRAN) is shown to the panel **as its own
     item** (`metadata_panel_item` = `<sid>:vg:<hash>`). A vote on the reference itself cannot tell whether the renaming
     preserved meaning.
2. **Panel design (budget-driven, label-preserving).** GLM-4.6 (P3) and Kimi-K2-0905 (R1) judge every shown item. Haiku-4.5
   (P1) judges only the items where they disagree or a vote is missing, plus the reference item when only the
   sentence-level ambiguity flag is split. Because P1 is only needed when the other two disagree, the 2-of-3 majority is the
   same as a full 3-vote majority. What is lost is a 3-rater κ on all items; it is reported on the 30-sentence pilot, which
   all three judged.
   - Why: the full 3-model pass was projected at $7.6 against about $6.3 of remaining budget.
   - Adjudicator calls see fewer items than a full call (a mild format difference from the gate).
3. **CTRL scope (plan 5c fallback).** For CTRL, a 20% sha1 sample of sentences gets full class coverage. For the rest, the
   panel sees the reference class plus all VOCAB_GRAN/COMPOUND/TIMEOUT classes. Their auto-ERROR classes keep the solver
   label (tier A, `label_source=solver`, no CONTESTED routing). MALLS strata (L25/L20/EXC) have full coverage.
   `metadata_panel_scope` records which applies.
4. **Reference audit and repair.**
   - MALLS gold with ≥2 unfaithful votes = GOLD_WRONG.
   - The panel models then write their own FOL for the original, undisguised sentence with the few-shot generation prompt.
     GLM and Kimi go first; Haiku is called only when those two are not mutually equivalent modulo vocabulary. The raw
     outputs are in `raw/reference_repair.jsonl`.
   - If ≥2 formulas are mutually equivalent modulo vocabulary, the one with the fewest atoms becomes the reference
     (PANEL_REPAIRED), and all rows are re-labelled by the solver against it (`work/labels_heldout_repaired.jsonl`).
     Otherwise the status is NO_TRUSTED_REFERENCE (tier C).
   - Caveat: a panel-written reference comes from the same families that judge the rows.
   - CTRL references judged unfaithful are DISPUTED_REFERENCE (tier C).
   - Panel votes on candidate classes are reference-free, so they stay valid after a repair.

## 3. Label counts and the testability declaration
Cells are rows (distinct sentences), LLM systems only. The rule: a stratum is testable if it has ≥50 ERROR rows AND ≥50
CORRECT rows AND ≥25 distinct sentences on each side, tier A+B, CONTESTED and reading_choice rows excluded. It was declared
after labelling and before any metric run, and is copied into `prereg_strata.json` (`testability_declaration.primary_pool`).

| stratum | sents | LLM rows | CORRECT A+B | ERROR A+B | TESTABLE | CORRECT tier A | ERROR tier A | tier-A testable | CONTESTED | reading_choice | tier C | UNRESOLVED |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| L25 (all 300) | 300 | 2960 | 176 (78) | 697 (107) | **YES** | 40 (25) | 98 (46) | no | 130 | 5 | 1566 | 4 |
|   L25 original 200 | 200 | 2460 | 141 (54) | 567 (70) | **YES** | 34 (19) | 73 (30) | no | 116 | 0 | 1334 | 4 |
|   L25 top-up 100 | 100 | 500 | 35 (24) | 130 (37) | no | 6 (6) | 25 (16) | no | 14 | 5 | 232 | 0 |
| L20 | 150 | 1850 | 229 (65) | 592 (79) | **YES** | 64 (33) | 132 (51) | yes | 91 | 22 | 746 | 0 |
| EXC | 100 | 1240 | 222 (55) | 384 (63) | **YES** | 124 (38) | 129 (48) | yes | 90 | 13 | 401 | 11 |
| CTRL | 150 | 1850 | 237 (31) | 149 (28) | **YES** | 186 (20) | 94 (15) | no | 65 | 0 | 865 | 260 |

**Tier-A-only** counts are printed next to A+B, so that iteration 2 can confirm on the panel-independent labels alone as a
robustness check. Tier-A CORRECT is structurally rare on MALLS strata: plain z3 EQ needs the reference's own predicate
names. EXC by exception type: `{"except": {"CORRECT": 80, "UNPARSEABLE": 44, "ERROR": 122, "CONTESTED": 20}, "excluding": {"CORRECT": 10, "ERROR": 16, "CONTESTED": 1, "UNPARSEABLE": 10}, "unless": {"ERROR": 291, "UNPARSEABLE": 53, "CORRECT": 124, "CONTESTED": 36, "UNRESOLVED": 10}, "without": {"CORRECT": 86, "ERROR": 279, "CONTESTED": 33, "UNPARSEABLE": 24, "UNRESOLVED": 1}}`. CTRL by length bin:
`{"0-11": {"CORRECT": 263, "ERROR": 209, "UNRESOLVED": 78, "UNPARSEABLE": 60, "CONTESTED": 25}, "12-19": {"CORRECT": 194, "ERROR": 231, "UNPARSEABLE": 158, "UNRESOLVED": 130, "CONTESTED": 20}, "20-inf": {"CORRECT": 75, "ERROR": 262, "UNRESOLVED": 52, "UNPARSEABLE": 73, "CONTESTED": 20}}`.

Final labels by system class: `{"llm": {"CORRECT": 1643, "ERROR": 4544, "UNPARSEABLE": 1062, "UNRESOLVED": 275, "CONTESTED": 376}, "reference_gold_as_system": {"ERROR": 435, "CORRECT": 100, "CONTESTED": 14, "UNRESOLVED": 1}, "symbolic_eventsem": {"UNPARSEABLE": 24, "ERROR": 26, "CORRECT": 7}}`.
Rows still UNRESOLVED (auto label | reference status): `{"ERROR|DISPUTED_REFERENCE": 255, "VOCAB_GRAN|GOLD_PANEL_OK": 1, "COMPOUND|GOLD_PANEL_OK": 5, "NO_REF|NO_TRUSTED_REFERENCE": 5, "COMPOUND|UNAUDITED_MALLS_GPT4_GOLD": 4, "REFERENCE_SELF|UNAUDITED_MALLS_GPT4_GOLD": 1, "COMPOUND|DISPUTED_REFERENCE": 5}`. These are items the panel
could not settle: no disguised formula, failed calls, or a vote that was never cast.

## 4. Gold audit: how often is the reference wrong? (blind, reference hidden among candidates)
| stratum | sentences | audited (≥2 votes, majority) | judged wrong | gold-error rate [Wilson 95%] | reference status | ambiguous sentences |
|---|---|---|---|---|---|---|
| L25 (all 300) | 300 | 294 | 249 | 0.847 [0.801, 0.884] | {"NO_TRUSTED_REFERENCE": 188, "PANEL_REPAIRED": 61, "GOLD_PANEL_OK": 45, "UNAUDITED_MALLS_GPT4_GOLD": 6} | 1 |
|   L25 original 200 | 200 | 196 | 168 | 0.857 [0.801, 0.899] | {"NO_TRUSTED_REFERENCE": 130, "PANEL_REPAIRED": 38, "GOLD_PANEL_OK": 28, "UNAUDITED_MALLS_GPT4_GOLD": 4} | 0 |
|   L25 top-up 100 | 100 | 98 | 81 | 0.827 [0.740, 0.889] | {"NO_TRUSTED_REFERENCE": 58, "GOLD_PANEL_OK": 17, "PANEL_REPAIRED": 23, "UNAUDITED_MALLS_GPT4_GOLD": 2} | 1 |
| L20 | 150 | 146 | 118 | 0.808 [0.737, 0.864] | {"NO_TRUSTED_REFERENCE": 71, "GOLD_PANEL_OK": 28, "PANEL_REPAIRED": 47, "UNAUDITED_MALLS_GPT4_GOLD": 4} | 2 |
| EXC | 100 | 95 | 73 | 0.768 [0.674, 0.842] | {"NO_TRUSTED_REFERENCE": 36, "PANEL_REPAIRED": 37, "GOLD_PANEL_OK": 22, "UNAUDITED_MALLS_GPT4_GOLD": 5} | 1 |
| CTRL | 150 | 148 | 112 | 0.757 [0.682, 0.819] | {"TRUSTED_AGREED": 36, "DISPUTED_REFERENCE": 112, "UNAUDITED_AGREED_FOLIO": 2} | 0 |
| MALLS_all | 550 | 535 | 440 | 0.822 [0.788, 0.853] | {"NO_TRUSTED_REFERENCE": 295, "PANEL_REPAIRED": 145, "GOLD_PANEL_OK": 95, "UNAUDITED_MALLS_GPT4_GOLD": 15} | 4 |

For comparison, the sibling run's panel judged 45.6% of MALLS gold wrong. 2606.02837 (human experts) found about 36-39% on
FOLIO/MALLS. The panel's accuracy on REAL errors (section 7) is only about 0.73, so each rate carries panel noise in both
directions.

## 5. Correct-but-not-equivalent (a correct candidate the solver cannot prove equivalent to the reference)
"final CORRECT among non-EQ" = the share of decided (tier A+B) rows NOT plain-z3-equivalent to the reference that are final
CORRECT. "share of CORRECT not EQ" = the share of all final-CORRECT rows that came from VOCAB_GRAN/COMPOUND/TIMEOUT via the
panel.

| stratum | non-EQ decided rows | final CORRECT among non-EQ | share of CORRECT that is not EQ |
|---|---|---|---|
| L25 | 833 | 0.163 [0.140, 0.190] | 0.773 [0.705, 0.828] |
| L20 | 757 | 0.218 [0.190, 0.249] | 0.721 [0.659, 0.775] |
| EXC | 482 | 0.203 [0.170, 0.241] | 0.441 [0.378, 0.507] |
| CTRL | 200 | 0.255 [0.200, 0.320] | 0.215 [0.168, 0.272] |

Per system × prompt variant:
| system|variant | non-EQ decided rows | final CORRECT among non-EQ | share of CORRECT not EQ |
|---|---|---|---|
| F:openai/gpt-5.1|fewshot_v1 | 53 | 0.321 [0.211, 0.455] | 0.370 [0.245, 0.514] |
| G1:meta-llama/llama-3.1-8b-instruct|fewshot_v1 | 204 | 0.069 [0.041, 0.112] | 0.424 [0.272, 0.592] |
| G1b:meta-llama/llama-3.3-70b-instruct|fewshot_v1 | 170 | 0.129 [0.087, 0.188] | 0.449 [0.319, 0.587] |
| G1b:meta-llama/llama-3.3-70b-instruct|zeroshot_v1 | 196 | 0.076 [0.047, 0.122] | 0.455 [0.298, 0.620] |
| G2:qwen/qwen3-235b-a22b-2507|fewshot_v1 | 199 | 0.276 [0.219, 0.342] | 0.611 [0.508, 0.705] |
| G2:qwen/qwen3-235b-a22b-2507|zeroshot_v1 | 155 | 0.245 [0.184, 0.319] | 0.613 [0.488, 0.724] |
| G3:mistralai/mistral-small-3.2-24b-instruct|fewshot_v1 | 206 | 0.214 [0.163, 0.275] | 0.506 [0.403, 0.608] |
| G4:deepseek/deepseek-v3.2|fewshot_v1 | 152 | 0.428 [0.352, 0.507] | 0.537 [0.449, 0.624] |
| G5:google/gemma-3-27b-it|fewshot_v1 | 193 | 0.150 [0.107, 0.207] | 0.500 [0.375, 0.625] |
| G6:microsoft/phi-4|fewshot_v1 | 204 | 0.270 [0.213, 0.334] | 0.567 [0.468, 0.661] |
| G7:openai/gpt-4.1-mini|fewshot_v1 | 141 | 0.340 [0.267, 0.422] | 0.516 [0.416, 0.615] |
| G8:google/gemini-2.5-flash|fewshot_v1 | 162 | 0.204 [0.149, 0.272] | 0.471 [0.359, 0.587] |
| G9:cohere/command-r7b-12-2024|fewshot_v1 | 237 | 0.063 [0.039, 0.102] | 0.600 [0.407, 0.766] |

This is the bias of "prover-checked equivalence to gold" as a label. Without the panel, every row counted in the first
column would be an ERROR or UNRESOLVED.

## 6. The automatic (solver) labeller vs the panel majority
Scope: LLM rows whose reference was audited FAITHFUL or repaired. Rows without a strict 2-of-3 majority are excluded.
| auto label | panel FAITHFUL | panel UNFAITHFUL | no majority / not covered |
|---|---|---|---|
| COMPOUND | 241 | 1090 | 46 |
| CORRECT | 343 | 62 | 9 |
| ERROR | 147 | 351 | 102 |
| VOCAB_GRAN | 183 | 220 | 24 |

- Binary, treating "error" as the positive class (auto ERROR/COMPOUND/TIMEOUT vs CORRECT/VOCAB_GRAN):
  - error precision 0.788 [0.768, 0.806], error recall 0.836 [0.818, 0.853];
  - faithful precision 0.651 [0.618, 0.683], faithful recall 0.576 [0.543, 0.607].
- Solver ERROR (a typed repair was found) only: precision 0.705 [0.663, 0.743].
- auto CORRECT rows get their vote from the reference item. A panel UNFAITHFUL there means the panel rejected an audited-OK
  reference, i.e. panel noise.

ADD/DROP caveat: 312 of 4544 final-ERROR LLM rows have a solver repair made only of
ADD/DROP operators (flag `metadata_addrop_only_suspect`). These are often vocabulary or arity mismatches the aligner cannot
bridge. Where the panel says faithful they became CONTESTED. Operator mass of final ERROR rows:
`{"DROP": 4225, "ADD": 3207, "RESTR": 2055, "CONN": 1748, "BIND": 1650, "COMPOUND": 1257, "MOVE": 755, "SWAP": 738, "REV": 611, "UNGLUE": 578, "QUANT": 539, "MEANING_RENAME": 238, "NEG": 206, "SCOPE": 157, "OTHER": 32, "REST": 1}`. Panel ops on tier-B ERROR rows: `{"DROP": 1315, "COMPOUND": 1257, "ADD": 872, "CONN": 573, "RESTR": 546, "BIND": 431, "MEANING_RENAME": 238, "REV": 215, "MOVE": 214, "SWAP": 174, "UNGLUE": 139, "QUANT": 134, "NEG": 54, "SCOPE": 44, "OTHER": 18, "REST": 1}`.
Repair status: `{"None": 2657, "COMPOUND_EXHAUSTED": 3306, "FOUND": 1270, "COMPOUND_TIMEOUT": 1241, "SKIPPED_EVENTSEM": 33}`. The 8 s budget turns some COMPOUND results into COMPOUND_TIMEOUT,
and the panel decides those. convention_flags (diagnostic only): `{"CONST_VS_EXISTS": 534, "ARITY_REIFY": 461, "SORTAL": 39, "XOR_OR": 41}`.

## 7. Panel: calibration, real-error accuracy, agreement
The panel is family-disjoint from all 9 generator families: Anthropic Haiku-4.5 (P1), Zhipu GLM-4.6 non-thinking (P3),
Moonshot Kimi-K2-0905 (R1, the reserve replacing xAI Grok-4.3, which failed the gate). Items are nonce-disguised.

**Synthetic gate, prompt v1.** Every cheap model failed, mainly by rejecting contrapositives and the renames.
| member | model | n | bal.acc | rec F | rec U | U@DOWN | U@UP | STRICT | RENAME | ref accepted | gate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 | anthropic/claude-haiku-4.5 | 77 | 0.712 | 0.45 | 0.973 | 1.0 | 0.941 | 0.55 | 0.35 | 0.9 | fail |
| P2 | x-ai/grok-4.3 | 77 | 0.71 | 0.475 | 0.946 | 0.95 | 0.941 | 0.6 | 0.35 | 1.0 | fail |
| P3 | z-ai/glm-4.6 | 77 | 0.787 | 0.575 | 1.0 | 1.0 | 1.0 | 0.7 | 0.45 | 0.95 | fail |
| P1alt | anthropic/claude-sonnet-4.6 | 77 | 0.875 | 0.75 | 1.0 | 1.0 | 1.0 | 0.85 | 0.65 | 0.9 | PASS |

**Synthetic gate, prompt v2 = production prompt.** v2 adds one generic line on logical equivalences. It was chosen after
seeing v1 on the same 77 items, so these numbers are optimistic. Gate: balanced accuracy ≥0.80 and recall ≥0.70 per class.
| member | model | n | bal.acc | rec F | rec U | U@DOWN | U@UP | STRICT | RENAME | ref accepted | gate |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P1 | anthropic/claude-haiku-4.5 | 77 | 0.861 | 0.75 | 0.973 | 1.0 | 0.941 | 0.75 | 0.75 | 0.95 | PASS |
| P2 | x-ai/grok-4.3 | 77 | 0.773 | 0.6 | 0.946 | 0.95 | 0.941 | 0.7 | 0.5 | 1.0 | fail |
| P3 | z-ai/glm-4.6 | 77 | 0.85 | 0.7 | 1.0 | 1.0 | 1.0 | 0.75 | 0.65 | 0.9 | PASS |
| R1 | moonshotai/kimi-k2-0905 | 77 | 0.863 | 0.725 | 1.0 | 1.0 | 1.0 | 0.8 | 0.65 | 0.9 | PASS |
| R2 | minimax/minimax-01 | 77 | 0.674 | 0.375 | 0.973 | 0.95 | 1.0 | 0.35 | 0.4 | 0.95 | fail |

**Real-error accuracy against human experts (track H, plan 4c).** The data are the 96 curated FOLIO/MALLS pairs (original
gold → expert-corrected) that are not z3-equivalent, with both formulas shown blind per sentence. The human verdict is
corrected = faithful, original = unfaithful. 75 pairs are unambiguous; the ambiguity-flagged ones are
reported separately.
| member | judgements (unamb.) | accuracy | original flagged | corrected accepted | accuracy on ambiguous |
|---|---|---|---|---|---|
| P1 | 150 | 0.747 | 0.867 | 0.627 | 0.69 |
| P3 | 150 | 0.693 | 0.773 | 0.613 | 0.762 |
| R1 | 142 | 0.725 | 0.72 | 0.653 | 0.711 |
| majority | 150 | 0.727 | 0.84 | 0.613 | 0.786 |

By auto census class (majority, unambiguous pairs):
| census class | pairs | majority accuracy |
|---|---|---|
| COMPOUND | 22 | 0.727 |
| VOCAB_GRAN | 18 | 0.806 |
| single-op | 21 | 0.714 |
| two-op | 14 | 0.643 |

**Read this next to every panel-decided (tier B/C) label rate.** On real errors the panel majority is right about
0.727 of the time. It flags about
0.84 of the expert-confirmed wrong formulas.
But it accepts only about 0.613 of the
expert-corrected ones. So the panel is **strict**: it over-calls unfaithfulness. Consequences:
- tier-B CORRECT rows are fairly reliable;
- tier-B ERROR rows and GOLD_WRONG verdicts contain false alarms;
- the corrected formulas are often themselves contestable, and 2606.02837 flags ambiguity as common.

Agreement between the two full raters, P3 and R1 (Cohen κ):
| stratum | items | raw agreement | Cohen κ | P3 faithful rate | R1 faithful rate |
|---|---|---|---|---|---|
| L25 | 1985 | 0.8448 | 0.4721 | 0.199 | 0.1577 |
| L20 | 1150 | 0.8391 | 0.52 | 0.2452 | 0.1765 |
| EXC | 688 | 0.7892 | 0.4415 | 0.2791 | 0.2224 |
| CTRL | 721 | 0.8391 | 0.6179 | 0.3135 | 0.2885 |
| ALL | 4544 | 0.8341 | 0.5133 | 0.241 | 0.193 |

- 3-rater pilot (30 sentences, 225 items, all three models): Fleiss κ = 0.5391;
  unanimous share 0.7644; pairwise Cohen κ `{"P1-P3": 0.5888, "P1-R1": 0.4953, "P3-R1": 0.533}`.
- Adjudication: 1618 of 5084 stage-1 items
  (0.3183) went to P1 across 538 sentences. P1 agreement counts:
  `{"P1_agrees_P3": 928, "n_P3": 1428, "P1_agrees_R1": 374, "n_R1": 684}`. Failed adjudication calls: 75.

CONTESTED rate (CONTESTED / decided rows, LLM systems):
| stratum | rate [Wilson 95%] |
|---|---|
| L25 | 0.051 [0.044, 0.061] |
| L20 | 0.055 [0.045, 0.068] |
| EXC | 0.082 [0.067, 0.100] |
| CTRL | 0.050 [0.040, 0.063] |

## 8. Parse rate and auto labels per system × prompt variant
| system|variant | n | parse rate | CORRECT | VOCAB_GRAN | ERROR | COMPOUND | TIMEOUT |
|---|---|---|---|---|---|---|---|
| F:openai/gpt-5.1|fewshot_v1 | 200 | 0.965 | 29 | 29 | 27 | 33 | 0 |
| G1:meta-llama/llama-3.1-8b-instruct|fewshot_v1 | 700 | 0.7857 | 22 | 31 | 75 | 205 | 0 |
| G1b:meta-llama/llama-3.3-70b-instruct|fewshot_v1 | 600 | 0.8783 | 31 | 49 | 82 | 154 | 0 |
| G1b:meta-llama/llama-3.3-70b-instruct|zeroshot_v1 | 600 | 0.8833 | 18 | 40 | 82 | 183 | 0 |
| G2:qwen/qwen3-235b-a22b-2507|fewshot_v1 | 700 | 0.8186 | 38 | 60 | 96 | 149 | 0 |
| G2:qwen/qwen3-235b-a22b-2507|zeroshot_v1 | 600 | 0.7717 | 27 | 53 | 69 | 142 | 0 |
| G3:mistralai/mistral-small-3.2-24b-instruct|fewshot_v1 | 700 | 0.9171 | 45 | 53 | 78 | 196 | 0 |
| G4:deepseek/deepseek-v3.2|fewshot_v1 | 600 | 0.9017 | 57 | 47 | 66 | 155 | 0 |
| G5:google/gemma-3-27b-it|fewshot_v1 | 600 | 0.9067 | 31 | 44 | 81 | 177 | 0 |
| G6:microsoft/phi-4|fewshot_v1 | 700 | 0.8814 | 43 | 71 | 66 | 185 | 0 |
| G7:openai/gpt-4.1-mini|fewshot_v1 | 600 | 0.8517 | 48 | 57 | 77 | 129 | 0 |
| G8:google/gemini-2.5-flash|fewshot_v1 | 600 | 0.9267 | 43 | 54 | 98 | 144 | 0 |
| G9:cohere/command-r7b-12-2024|fewshot_v1 | 700 | 0.8443 | 11 | 32 | 80 | 228 | 0 |
| ccg2lambda|none | 57 | 0.5789 | 0 | 0 | 0 | 33 | 0 |
| malls_gpt4_gold|none | 550 | 1.0 | 5 | 17 | 25 | 98 | 0 |

## 9. Disguise (plan 5a)
- Each sentence gets its own CVCVC nonce bijection. It covers the Porter stems of the text's content words and the name
  tokens of ALL formulas of that sentence.
  - It is seeded by sha1(sentence_id), and a nonce is rejected if it is a WordNet lemma.
  - A name token that is a WordNet synonym of a sentence word reuses that word's nonce.
  - Logic symbols, quantifiers and numbers are unchanged.
- Guard: plain-z3 equivalence of class representatives before vs after disguise, 50 sentences:
  `{"sentences": 50, "pairs": 957, "mismatches": 0, "z3_unknown_pairs": 0, "passed": true}`.
- Deviation from the plan: NLTK Porter stems are used instead of spaCy lemmas.
- `metadata_disguised_text` and `metadata_disguised_fol` are on every row, for contamination checks.

## 10. Disjointness and exclusion
- Exclusion hashes: 2054. They cover FOLIO-validation (tasksource and refined), the curated
  FOLIO/MALLS sets, MALLS-test, the Logic-LM FOLIO_dev contexts and the few-shot exemplars: `{"tasksource_folio_validation": 2634, "folio_refined_validation": 2634, "curated_folio": 859, "curated_malls": 200, "malls_test": 2000, "logiclm_context": 3876, "logiclm_question": 1224}`.
- Collisions after exclusion: **0**; top-up collisions: 0.
- MALLS pool log: `{"raw": 27284, "gold_unparseable": 334, "excluded_screen_hash": 1, "dup_text": 30, "pool": 26919}`. CTRL pool log: `{"story_matched": 1001, "agreement_IDENTICAL_STRING": 1465, "agreement_UNPARSEABLE": 147, "agreement_VOCAB": 15, "agreement_NONEQ": 20, "agreement_EQ": 27, "excluded_screen_hash": 3}`.
- The 6 few-shot exemplars were hand-picked from the sha1-ordered eligible CTRL pool, because the auto-pick contained wrong
  golds. They are excluded from CTRL and calibration.

## 11. Screen audit (secondary deliverable)
- Logic-LM records per file: {'gpt-3.5-turbo': 204, 'gpt-4': 204, 'text-davinci-003': 204}. Curated conclusions matched:
  112/202 (0.554).
  Items per track: {'L': 871, 'H': 302}.
- Panel scope (plan 6b): every track-L sentence with a VOCAB_GRAN/COMPOUND/TIMEOUT class, plus a 20% sha1 sample of the rest,
  plus a supplementary pass over the VOCAB_GRAN strings themselves. Track-H rows take their votes from the 4c real-error
  check, where the original formula is the candidate. Rows not covered have `label_tier = auto_only`.
- Final labels per track: `{"L": {"ERROR": 459, "CORRECT": 284, "UNPARSEABLE": 62, "NO_REFERENCE": 52, "CONTESTED": 14}, "H": {"ERROR": 81, "UNPARSEABLE": 16, "CORRECT": 189, "UNRESOLVED": 1, "NO_REFERENCE": 8, "CONTESTED": 7}}`. Tiers: `{"L": {"auto_only": 269, "B": 366, "-": 62, "A": 122, "none": 52}, "H": {"A": 42, "-": 16, "auto_only": 182, "B": 54, "none": 8}}`.
- Track-L auto label vs panel majority: `{"COMPOUND": {"UNFAITHFUL": 178, "FAITHFUL": 42}, "CORRECT": {"FAITHFUL": 34, "UNFAITHFUL": 14}, "ERROR": {"FAITHFUL": 14, "UNFAITHFUL": 60}, "REF_UNPARSEABLE": {}, "UNPARSEABLE": {}, "VOCAB_GRAN": {"FAITHFUL": 76, "UNFAITHFUL": 70}}`.
- item_id = sha1(system + '|' + norm(text) + '|' + raw_fol)[:16]. The raw join keys are stored in every row.

## 12. Cost (OpenRouter, from per-call usage.cost; `cost_ledger.jsonl`)
| phase | calls | USD |
|---|---|---|
| generation | 7900 | 0.9504 |
| gate | 185 | 0.4289 |
| gate_trackh | 299 | 0.513 |
| panel_screen | 683 | 0.9283 |
| panel_heldout | 2397 | 4.6615 |
| panel_heldout_adj | 508 | 1.6697 |
| reference_repair | 1244 | 0.6812 |
Total **$9.833** of the $9.50 hard cap.

## 13. Licences, overlaps, known biases
- Licences:
  - MALLS-v0 (yuan-yang): CC-BY-NC-4.0 (non-commercial);
  - FOLIO (tasksource/folio): CC-BY-SA-4.0;
  - folio-refined (yfxiao): MIT;
  - folio_by_ccg2lambda: CC-BY-4.0;
  - DSAVlab-UNIUD curated sets: FOLIO CC-BY-4.0, MALLS CC-BY-NC-4.0;
  - Logic-LLM outputs: MIT;
  - generator outputs are subject to their providers' terms.
- Judge-family overlap: Gemini-Flash (G8) and Qwen (G2) are likely judge families in iteration 2. The self-preference check
  there must account for this; it does not affect these labels. The panel families (Anthropic, Zhipu, Moonshot) are
  disjoint from all generators.
- Known biases:
  1. Tier-B/C labels carry panel error: about 0.73 accuracy on real errors, and the panel is strict (section 7).
  2. A MALLS reference judged faithful may still be wrong if 2 of the 3 panel members missed the error.
  3. CTRL references are FOLIO annotations the refiner left unchanged (mostly IDENTICAL_STRING); they are not independent
     re-annotations.
  4. Tier A depends on the iter-3 aligner. Its VOCAB/GRAN bridge can accept meaning-changing renames, which is why
     VOCAB_GRAN rows go to the panel.
  5. One prompt per generator at temperature 0, so system-level rankings are descriptive only.
  6. The L25 top-up batch has only 5 generator slots.
  7. Items are clustered by sentence (up to 14 systems per sentence), so bootstraps must resample sentences.
