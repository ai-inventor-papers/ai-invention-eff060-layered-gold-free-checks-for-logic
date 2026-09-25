#!/usr/bin/env python3
"""STEP 7b: render dataset_card.md from work/label_report.json (data-quality statistics only, no metric results)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = json.loads((ROOT / "work" / "label_report.json").read_text())


def tbl(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def gate_rows(g):
    rows = []
    for m, v in (g or {}).items():
        rows.append([m, v["model"], v["n_scored"], v["balanced_accuracy"], v["recall_faithful"], v["recall_unfaithful"],
                     v["recall_unfaithful_DOWN"], v["recall_unfaithful_UP"], v["recall_STRICT"], v["recall_RENAME"],
                     v["reference_accepted"], "PASS" if v["passes_gate"] else "fail"])
    return rows


def main():
    st = R["strata"]
    strat_rows = []
    for k, d in st.items():
        g = lambda key: d.get(key, {}).get("rows", 0)
        gs = lambda key: d.get(key, {}).get("sentences", 0)
        strat_rows.append([k, d["sentences"], d["rows"], f"{g('A_unaudited_ref:CORRECT')} ({gs('A_unaudited_ref:CORRECT')})",
                           f"{g('A_unaudited_ref:ERROR')} ({gs('A_unaudited_ref:ERROR')})", d["UNRESOLVED"], d["UNPARSEABLE"]])
    len_rows = [[k, v.get("CORRECT", 0), v.get("CORRECT_sents", 0), v.get("ERROR", 0), v.get("ERROR_sents", 0), v.get("UNRESOLVED", 0), v.get("UNPARSEABLE", 0)]
                for k, v in R["solver_lenient_by_stratum"].items()]
    auto_rows = [[k] + [v.get(x, 0) for x in ("CORRECT", "VOCAB_GRAN", "ERROR", "COMPOUND", "TIMEOUT_UNKNOWN", "UNPARSEABLE")]
                 for k, v in R["auto_by_stratum"].items()]
    sys_rows = [[k, v["n"], v["parse_rate"], v.get("CORRECT", 0), v.get("VOCAB_GRAN", 0), v.get("ERROR", 0), v.get("COMPOUND", 0),
                 v.get("TIMEOUT_UNKNOWN", 0)] for k, v in R["per_system"].items()]
    test_rows = [[k, v["official_tierAB"]["testable"], f"{v['provisional_incl_unaudited_ref']['ERROR_rows']}/{v['provisional_incl_unaudited_ref']['ERROR_sents']}",
                  f"{v['provisional_incl_unaudited_ref']['CORRECT_rows']}/{v['provisional_incl_unaudited_ref']['CORRECT_sents']}",
                  v["provisional_incl_unaudited_ref"]["testable"],
                  f"{v['provisional_strict_excl_addrop']['ERROR_rows']}/{v['provisional_strict_excl_addrop']['ERROR_sents']}",
                  v["provisional_strict_excl_addrop"]["testable"]] for k, v in R["testability"].items()]
    cost_rows = [[k, v["calls"], v["usd"]] for k, v in R["cost_by_phase"].items()]
    ex = R["exclusion_log"]
    sm = R["screen_meta"] or {}
    md = f"""# Dataset card — held-out NL→FOL faithfulness meta-evaluation set (run_u75jRHUss0zo, invention iter 1, dataset E)

> **HELD-OUT: iteration 2 must not tune any threshold on these rows.** Use them once, to confirm a screen survivor
> whose thresholds are already frozen.

> **STATUS: PARTIAL. The LLM panel stage was BLOCKED.** The OpenRouter key is shared by every concurrent run and has a
> **$50/day limit**. Other runs used it up at about 13:29 UTC on 2026-09-23 (`GET /api/v1/key` → `limit_remaining = 0`,
> `usage_daily ≈ $50.06`). This run had spent ${R['cost_total_usd']} by then. Everything that needs no LLM is complete:
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
- **heldout_sentences**: {R['counts']['heldout_sentences']} screen-disjoint sentences.
  - MALLS-v0.1-train (GPT-4 gold): L25 = 200 (≥25 words and ≥3 gold conditions, spread evenly over 25-29 / 30-34 / ≥35
    words); L20 = 150 (20-24 words); EXC = 100 (all 67 parseable unless/except/excluding items, plus 33 'without' items
    with ≥15 words; XOR 'but not' excluded).
  - CTRL = 150 FOLIO-v2-train premises whose tasksource original ≡ folio-refined (bins 50 / 60 / 40 by length <12 / 12-19 /
    ≥20 words). agreement_type in CTRL: {ex['ctrl_agreement_counts']}. Identical strings are weak evidence: they show only
    that the refiner did not change the formula.
- **heldout_candidates**: {R['counts']['heldout_candidates']} rows. They come from:
  - 10 LLM slots over 9 families, few-shot, temperature 0: Llama-3.1-8B, Llama-3.3-70B, Qwen3-235B-A22B-2507,
    Mistral-Small-3.2, DeepSeek-V3.2 (reasoning off), Gemma-3-27B, Phi-4, GPT-4.1-mini, Gemini-2.5-Flash (reasoning off),
    Command-R7B;
  - the zero-shot Llama-3.3-70B variant;
  - the frontier model GPT-5.1 (effort low) on a 200-sentence subset;
  - ccg2lambda: {R['ccg2lambda']['matched']} CTRL sentences matched in the train split, {R['ccg2lambda']['convert_fail']}
    NLTK→FOL conversion failures and {R['ccg2lambda']['parse_fail']} parse failures, all kept as UNPARSEABLE. With fewer
    than about 60 rows, this system is not analysable on its own;
  - the MALLS GPT-4 gold itself, as system `malls_gpt4_gold` on the 450 MALLS sentences. Its label can only come from the
    blind gold audit, so it is UNRESOLVED while the panel is pending.
- **panel_calibration**:
  - the synthetic known-label gate: 77 items on 20 disjoint TRUSTED_AGREED CTRL-pool sentences (40 FAITHFUL = 20 strict
    z3-verified rewrites + 20 renames; 37 UNFAITHFUL z3-verified perturbations, 20 at DOWN sites and 17 at UP sites). Three
    sentences are single ground atoms and admit only one perturbation, so there are 77 items, not 80;
  - the 96 track-H human real-error pairs. With the ⊕ fix there are 96 non-equivalent pairs, not 99.
- **screen_audit**: {R['counts'].get('screen_audit')} rows (track L = Logic-LM released FOLIO-dev outputs; track H = the 302
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
{tbl(['stratum', 'sentences', 'rows', 'CORRECT A_unaudited', 'ERROR A_unaudited', 'UNRESOLVED', 'UNPARSEABLE'], strat_rows)}

Solver auto-label distribution (LLM rows):
{tbl(['stratum', 'CORRECT(EQ)', 'VOCAB_GRAN', 'ERROR', 'COMPOUND', 'TIMEOUT_UNKNOWN', 'UNPARSEABLE'], auto_rows)}

Why the MALLS strata have almost no tier-A CORRECT: plain z3 EQ needs the SAME predicate names as the reference. LLMs choose
their own vocabulary, so a correct MALLS candidate is at best VOCAB_GRAN and needs the panel. CTRL gets CORRECT rows because
the FOLIO-style few-shot exemplars lead models to reuse FOLIO naming on short premises.

Sensitivity only, `solver_lenient_label`:
{tbl(['stratum', 'CORRECT', 'CORRECT sents', 'ERROR', 'ERROR sents', 'UNRESOLVED', 'UNPARSEABLE'], len_rows)}

EXC by exception type: `{json.dumps(st['EXC'].get('by_exception_type'))}`
CTRL by length bin: `{json.dumps(st['CTRL'].get('by_len_bin'))}`

## 4. Testability declaration (frozen in prereg_strata.json before any metric run)
Rule: ≥50 ERROR rows AND ≥50 CORRECT rows AND ≥25 distinct sentences on each side, tier A+B only.
{tbl(['stratum', 'OFFICIAL testable (A+B)', 'prov. ERROR rows/sents', 'prov. CORRECT rows/sents', 'prov. testable', 'prov. ERROR excl. ADD/DROP-only', 'prov.-strict testable'], test_rows)}

OFFICIAL: no stratum is testable, because tier A+B requires the panel. PROVISIONAL counts use tier A against unaudited
references. L25 top-up rule (frozen before labels): triggered = {R['l25_topup_rule']['triggered']}, executed = False.
{R['l25_topup_rule']['reason_not_executed']}.

## 5. Automatic labeller facts
- Repair status: `{json.dumps(R['heldout_repair_status'])}`. The 8 s budget (vs 25 s in iter 3) turns some COMPOUND results
  into timeouts; they are split into COMPOUND_TIMEOUT vs COMPOUND_EXHAUSTED.
- Equivalence status: `{json.dumps(R['heldout_equiv_status'])}`
- **Caveat for tier-A ERROR: ADD/DROP-only repairs.** {R['addrop']['n_addrop_only']} of {R['addrop']['n_error_llm']} solver ERROR
  rows (LLM systems) are repaired ONLY by ADD/DROP operators (ADD+DROP = {R['addrop']['n_add_plus_drop']}). A depth-2 ADD+DROP
  "repair" replaces an unmatched candidate atom with the reference atom. That is exactly what a vocabulary or arity mismatch
  the iter-3 aligner cannot bridge looks like (e.g. Lunch(james) vs HasLunch(james, company)). The iter-3 review and the
  sibling screen executor flagged these as label artefacts, and the plan routes them to the panel for CONTESTED. Such rows
  carry `metadata_addrop_only_suspect = true`; the stricter provisional count in section 4 excludes them.
- Operator mass of solver ERROR rows: `{json.dumps(R['heldout_error_ops_mass'])}`, depth `{json.dumps(R['heldout_error_depth'])}`
- convention_flags (diagnostic only; they never change a label): `{json.dumps(R['convention_flags'])}`
- ⊕ precedence fix regression: re-running the 99-pair census makes 3 pairs equivalent (99→96 non-equivalent), and COMPOUND
  falls 36→33. This matches the review's 3 pure ⊕/→ bracketing items.
- Parser note: `fol.parse('')` returns an atom named None. Empty outputs are forced to UNPARSEABLE in the worker and in the
  assembler.
- The labeller's precision/recall against the panel majority, and the correct-but-not-equivalent rate, are **PENDING (panel)**.

## 6. Parse rate and auto labels per system × prompt variant
{tbl(['system|variant', 'n', 'parse rate', 'CORRECT', 'VOCAB_GRAN', 'ERROR', 'COMPOUND', 'TIMEOUT'], sys_rows)}

## 7. Panel calibration
Panel: Anthropic Haiku-4.5 (P1), Zhipu GLM-4.6 non-thinking (P3), Moonshot Kimi-K2-0905 (R1, the reserve replacing xAI
Grok-4.3). The panel is family-disjoint from all 9 generator families.

Gate: balanced accuracy ≥0.80, and recall ≥0.70 on each class. It is run in the exact production format (disguised,
batched per sentence, the reference shown among the variants).

**Prompt v1** (first attempt). It FAILED for every cheap model: faithful recall was 0.45-0.58, driven by contrapositive
rejection and by rename items. The v1 renames also came from WordNet first senses and turned out to change meaning
(In→Inch, At→Astatine, Band→Set). They were replaced with naming-convention renames (Is/Has prefix).
{tbl(['member', 'model', 'n', 'bal.acc', 'rec F', 'rec U', 'U@DOWN', 'U@UP', 'STRICT', 'RENAME', 'ref accepted', 'gate'], gate_rows(R.get('gate_prompt_v1')))}

**Prompt v2** (adds one generic sentence: contrapositive / De Morgan / ¬¬ / nested quantifiers are equivalent). This is the
production prompt. Caveat: v2 was chosen after seeing the v1 gate on the same 77 items, so these gate numbers are optimistic.
The track-H real-error check (4c) is the independent accuracy estimate, and it is pending.
{tbl(['member', 'model', 'n', 'bal.acc', 'rec F', 'rec U', 'U@DOWN', 'U@UP', 'STRICT', 'RENAME', 'ref accepted', 'gate'], gate_rows(R.get('gate_prompt_v2')))}

All three members pass: P1 Haiku, P3 GLM and R1 Kimi. P2 Grok-4.3 fails (faithful recall 0.60), so the reserve Kimi-K2
replaces it per plan 4b. MiniMax-01 also fails. Sonnet-4.6 passed only under v1 (0.875) but cost ≈4.6× Haiku in the gate ($0.196 vs $0.043 for 20 calls), so it is
not used.

Track-H real-error check (4c): {json.dumps(R['trackH_panel_coverage'])}

Fleiss κ and the CONTESTED rate: PENDING (panel).

## 8. Disguise (plan 5a)
- Nonce CVCVC bijection per sentence over Porter stems of text words plus name tokens of ALL formulas of the sentence,
  seeded by sha1(sentence_id) and rejected if the nonce is a WordNet lemma. Name tokens that are WordNet synonyms of a
  sentence word reuse that word's nonce, so paraphrased names stay linked to the text.
- Guard (50 sentences): pairwise plain-z3 equivalence of class representatives before vs after disguise: `{json.dumps(R['disguise_check'])}`.
- Deviation: NLTK Porter stems are used instead of spaCy lemmas.

## 9. Disjointness and exclusion
- Exclusion hashes: {ex['exclusion_hash_count']}. Sources: `{json.dumps(ex['exclusion_sources'])}`.
- Collisions after exclusion: **{ex['hash_collisions_with_screen_after_exclusion']}**.
- MALLS pool: `{json.dumps(ex['malls_pool'])}`. CTRL pool: `{json.dumps(ex['ctrl_pool'])}`.
- Few-shot exemplars: 6, hand-picked from the sha1-ordered eligible CTRL pool and excluded from CTRL and calibration. The
  auto-pick contained wrong golds (e.g. Age(james, y) for 'the customers'); it is kept in work/fewshot_exemplars_autopick_rejected.json.

## 10. Screen rebuild
- Logic-LM records per file: {sm.get('logiclm_records_per_file')}.
- Conclusion match rate: {sm.get('distinct_conclusions_matched')}/{sm.get('curated_conclusions')} = {sm.get('conclusion_match_rate')}.
- Agreed-premise pool: {sm.get('agreed_premise_pool')}. Items per track: {sm.get('items_per_track')}. Track-L reference sources: `{json.dumps(sm.get('track_L_reference_source'))}`.
- Screen auto labels per track: `{json.dumps(R['screen_auto_label'])}`
- Screen final labels (auto_only; panel pending): `{json.dumps(R['screen_final_label'])}`
- item_id = sha1(system + '|' + norm(text) + '|' + raw_fol)[:16], where norm = lowercase, apostrophes removed, punctuation
  stripped, whitespace collapsed. Raw join keys are stored in every row.

## 11. Cost (OpenRouter, from per-call usage.cost)
{tbl(['phase', 'calls', 'USD'], cost_rows)}
Total ${R['cost_total_usd']} of the $9.5 hard cap.

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
"""
    (ROOT / "dataset_card.md").write_text(md)
    print("dataset_card.md written", len(md))


if __name__ == "__main__":
    main()
