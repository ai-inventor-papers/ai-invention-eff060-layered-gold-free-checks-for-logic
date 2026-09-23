#!/usr/bin/env python3
"""STEP 7b: render dataset_card.md from work/label_report.json (data-quality statistics only, NO metric results)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = json.loads((ROOT / "work" / "label_report.json").read_text())


def tbl(head, rows):
    out = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def ci(w):
    return "n/a" if not w else f"{w[0]:.3f} [{w[1]:.3f}, {w[2]:.3f}]"


def rs(d):
    return f"{d['rows']} ({d['sents']})"


def gate_rows(g):
    return [[m, v["model"], v["n_scored"], v["balanced_accuracy"], v["recall_faithful"], v["recall_unfaithful"],
             v["recall_unfaithful_DOWN"], v["recall_unfaithful_UP"], v["recall_STRICT"], v["recall_RENAME"],
             v["reference_accepted"], "PASS" if v["passes_gate"] else "fail"] for m, v in (g or {}).items()]


def main():
    P = R["testability_primary"]
    GA = R["gold_audit"]
    TH = R.get("trackH_real_error_accuracy") or {}
    PR = R["panel_reliability"]
    LB = R["labeller_vs_panel_binary"]
    ex = R["exclusion_log"]
    sm = R["screen_meta"] or {}
    names = {"L25": "L25 (all 300)", "L25_orig200": "  L25 original 200", "L25_topup100": "  L25 top-up 100", "L20": "L20", "EXC": "EXC", "CTRL": "CTRL"}
    test_rows = [[names[k], v["sentences"], v["rows"], rs(v["tierAB_primary"]["CORRECT"]), rs(v["tierAB_primary"]["ERROR"]),
                  "**YES**" if v["tierAB_primary"]["testable"] else "no", rs(v["tierA_only"]["CORRECT"]), rs(v["tierA_only"]["ERROR"]),
                  "yes" if v["tierA_only"]["testable"] else "no", v["CONTESTED_rows"], v["reading_choice_rows"], v["tierC_rows"], v["UNRESOLVED_rows"]]
                 for k, v in P.items()]
    ga_rows = [[names.get(k, k), v["sentences"], v["audited"], v["judged_wrong"], ci(v["gold_error_rate_wilson95"]),
                json.dumps(v["reference_status"]), v["reading_choice_sentences"]] for k, v in GA.items()]
    cne = R["correct_not_equivalent"]
    cne_st = [[k, v["non_EQ_decided_rows"], ci(v["final_CORRECT_among_non_EQ"]), ci(v["share_of_final_CORRECT_that_is_not_EQ"])]
              for k, v in cne["by_stratum"].items()]
    cne_sys = [[k, v["non_EQ_decided_rows"], ci(v["final_CORRECT_among_non_EQ"]), ci(v["share_of_final_CORRECT_that_is_not_EQ"])]
               for k, v in cne["by_system"].items()]
    conf = R["labeller_vs_panel_confusion"]
    conf_rows = [[a, v.get("FAITHFUL", 0), v.get("UNFAITHFUL", 0), v.get("no_majority_or_not_covered", 0)] for a, v in sorted(conf.items())]
    sys_rows = [[k, v["n"], v["parse_rate"], v.get("CORRECT", 0), v.get("VOCAB_GRAN", 0), v.get("ERROR", 0), v.get("COMPOUND", 0),
                 v.get("TIMEOUT_UNKNOWN", 0)] for k, v in R["per_system"].items()]
    th_rows = []
    for who, v in (TH.get("per_model") or {}).items():
        th_rows.append([who, v["unambiguous"]["n_judgements"], v["unambiguous"]["accuracy"], v["orig_flagged_rate_unamb"],
                        v["corr_accepted_rate_unamb"], v["ambiguous_READING_CHOICE"]["accuracy"]])
    th_cls = [[k, v["n"], v["majority"]["accuracy"]] for k, v in (TH.get("by_census_class") or {}).items()]
    kap = [[k, v["items"], v["agreement"], v["cohen_kappa_P3_R1"], v["faithful_rate_P3"], v["faithful_rate_R1"]]
           for k, v in PR["pairwise_P3_R1_by_stratum"].items()]
    pil = PR["pilot_3rater"]
    adj = PR["adjudication"]
    cont = [[k, ci(v)] for k, v in R["contested_rate"].items()]
    cost_rows = [[k, v["calls"], v["usd"]] for k, v in R["cost_by_phase"].items()]
    fin = R["heldout_final_label"]
    tiers = R["heldout_tier"]
    addrop = R["addrop"]
    ctrl_types = R["ctrl_agreement_type"]
    top = R["l25_topup_rule"].get("execution") or {}
    md = f"""# Dataset card: held-out NL→FOL faithfulness meta-evaluation set (run_u75jRHUss0zo, invention iter 1, dataset E)

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

Totals: {R['counts']['heldout_sentences']} sentences, {R['counts']['heldout_candidates']} candidate rows,
{R['counts']['panel_calibration']} calibration rows, {R['counts']['screen_audit']} screen rows. Total OpenRouter cost
**${R['cost_total_usd']}** (hard cap $9.50).

Held-out final labels: `{json.dumps(fin)}`. Tiers: `{json.dumps(tiers)}`.

### Headline data-quality facts (read before using the labels)
1. **Testability (tiers A+B, primary pool).** The testable strata are L25 (all 300), L20, EXC and CTRL. The L25 top-up batch
   alone is not testable, and is meant to be pooled. See section 3.
2. **The panel is strict, and the reference audit rejects most references.**
   - It judged {GA['MALLS_all']['judged_wrong']}/{GA['MALLS_all']['audited']} MALLS gold formulas unfaithful
     ({ci(GA['MALLS_all']['gold_error_rate_wilson95'])}) and {GA['CTRL']['judged_wrong']}/{GA['CTRL']['audited']} CTRL
     references ({ci(GA['CTRL']['gold_error_rate_wilson95'])}). Expert audits report about 36-46%.
   - On track H the same panel accepts only {(TH.get('per_model') or {}).get('majority', {}).get('corr_accepted_rate_unamb')}
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
     remainder. The last batch of 16 in-flight calls overshot, so the final spend is ${R['cost_total_usd']}, still under
     the $10 artifact budget.
   - The adjudication remainder was not finished for 32 low-priority sentences. Their split items are CONTESTED (a 1-1
     split with a missing vote) or UNRESOLVED (a single vote).
   - 120 stage-1 sentences lost their Kimi call to the phase cap. Haiku then judged those items, so they have two votes,
     and any 1-1 split is CONTESTED.
5. **CTRL UNRESOLVED rows.** They arise where a CTRL reference was DISPUTED (tier C → panel-only labels) but the sentence
   was outside the 20% full-coverage sample. Its auto-ERROR classes were never shown to the panel, so they stay UNRESOLVED
   rather than taking a solver label measured against a disputed reference.

## 1. Composition
- **heldout_sentences** ({R['counts']['heldout_sentences']}), all screen-disjoint (hash collisions after exclusion:
  {ex['hash_collisions_with_screen_after_exclusion']}):
  - **L25 = 300**: MALLS-v0.1-train, ≥25 words AND ≥3 gold-derived conditions, sha1 order, spread over word bins 25-29 / 30-34
    / ≥35.
    - 200 were selected in step 1.
    - The other 100 are the **pre-registered top-up** batch: the same rule on the unused pool, bins taken
      {top.get('bin_log', {}).get('bin_taken')}. The ≥35-word supply was exhausted at {top.get('bin_log', {}).get('bin_supply', [0, 0, 0])[2]}.
    - The top-up rule was frozen in `prereg_strata.json` before any label was seen: "If after Step 3 the tier-A-projected
      ERROR or CORRECT count of L25 is below 60, generate one more sha1-ordered batch of 100 L25 sentences with the 5 cheapest
      generator slots". Tier-A CORRECT was 9. The top-up was generated with the 5 cheapest slots (Command-R7B, Llama-3.1-8B,
      Phi-4, Mistral-Small-3.2, Qwen3-235B) plus the MALLS gold, so its rows per sentence differ from the original 200.
    - `metadata_strata.l25_topup_batch` marks these rows. Statistics are also reported with and without the top-up.
  - **L20 = 150**: 20-24 words and ≥3 conditions.
  - **EXC = 100**: all 67 parseable unless/except/excluding/other-than items plus 33 'without' items with ≥15 words. The XOR
    pattern 'but not (both)' is excluded.
  - **CTRL = 150** FOLIO-v2-train premises where the tasksource original ≡ folio-refined modulo vocabulary. Bins are
    50/60/40 by length <12 / 12-19 / ≥20 words. Reference = the refined formula. agreement_type: `{json.dumps(ctrl_types)}`.
    IDENTICAL_STRING shows only that the refiner did not change the formula; it is weak evidence. The blind panel audit of
    the reference (section 4) is the real check.
- **heldout_candidates** ({R['counts']['heldout_candidates']} rows):
  - 10 LLM slots over 9 families, one fixed few-shot prompt (`prompts/fewshot_v1.txt`), temperature 0: Llama-3.1-8B,
    Llama-3.3-70B, Qwen3-235B-A22B-2507, Mistral-Small-3.2-24B, DeepSeek-V3.2 (reasoning off), Gemma-3-27B, Phi-4,
    GPT-4.1-mini, Gemini-2.5-Flash (reasoning off), Command-R7B;
  - zero-shot variants for 2 families: Llama-3.3-70B and Qwen3-235B;
  - frontier GPT-5.1 (effort low) on a 200-sentence subset (60 L25 + 50 L20 + 40 EXC + 50 CTRL);
  - ccg2lambda (system_class `symbolic_eventsem`): {R['ccg2lambda']['matched']} CTRL sentences matched in the HF train
    split. Too few to analyse on its own, and never pooled with LLM rows;
  - the MALLS GPT-4 gold itself, as system `malls_gpt4_gold` (system_class `reference_gold_as_system`), on every MALLS
    sentence. Its label is the blind gold audit.
  - Every unparseable output is kept (final label UNPARSEABLE).
- **panel_calibration**: the synthetic known-label gate (77 items) and the 96 track-H human real-error pairs with panel
  votes.
- **screen_audit** ({R['counts']['screen_audit']} rows): track L = Logic-LM's released FOLIO-dev outputs; track H = the 302
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

{tbl(['stratum', 'sents', 'LLM rows', 'CORRECT A+B', 'ERROR A+B', 'TESTABLE', 'CORRECT tier A', 'ERROR tier A', 'tier-A testable', 'CONTESTED', 'reading_choice', 'tier C', 'UNRESOLVED'], test_rows)}

**Tier-A-only** counts are printed next to A+B, so that iteration 2 can confirm on the panel-independent labels alone as a
robustness check. Tier-A CORRECT is structurally rare on MALLS strata: plain z3 EQ needs the reference's own predicate
names. EXC by exception type: `{json.dumps(R['strata']['EXC'].get('by_exception_type'))}`. CTRL by length bin:
`{json.dumps(R['strata']['CTRL'].get('by_len_bin'))}`.

Final labels by system class: `{json.dumps(R['final_by_system_class'])}`.
Rows still UNRESOLVED (auto label | reference status): `{json.dumps(R['unresolved_reasons'])}`. These are items the panel
could not settle: no disguised formula, failed calls, or a vote that was never cast.

## 4. Gold audit: how often is the reference wrong? (blind, reference hidden among candidates)
{tbl(['stratum', 'sentences', 'audited (≥2 votes, majority)', 'judged wrong', 'gold-error rate [Wilson 95%]', 'reference status', 'ambiguous sentences'], ga_rows)}

For comparison, the sibling run's panel judged 45.6% of MALLS gold wrong. 2606.02837 (human experts) found about 36-39% on
FOLIO/MALLS. The panel's accuracy on REAL errors (section 7) is only about 0.73, so each rate carries panel noise in both
directions.

## 5. Correct-but-not-equivalent (a correct candidate the solver cannot prove equivalent to the reference)
"final CORRECT among non-EQ" = the share of decided (tier A+B) rows NOT plain-z3-equivalent to the reference that are final
CORRECT. "share of CORRECT not EQ" = the share of all final-CORRECT rows that came from VOCAB_GRAN/COMPOUND/TIMEOUT via the
panel.

{tbl(['stratum', 'non-EQ decided rows', 'final CORRECT among non-EQ', 'share of CORRECT that is not EQ'], cne_st)}

Per system × prompt variant:
{tbl(['system|variant', 'non-EQ decided rows', 'final CORRECT among non-EQ', 'share of CORRECT not EQ'], cne_sys)}

This is the bias of "prover-checked equivalence to gold" as a label. Without the panel, every row counted in the first
column would be an ERROR or UNRESOLVED.

## 6. The automatic (solver) labeller vs the panel majority
Scope: LLM rows whose reference was audited FAITHFUL or repaired. Rows without a strict 2-of-3 majority are excluded.
{tbl(['auto label', 'panel FAITHFUL', 'panel UNFAITHFUL', 'no majority / not covered'], conf_rows)}

- Binary, treating "error" as the positive class (auto ERROR/COMPOUND/TIMEOUT vs CORRECT/VOCAB_GRAN):
  - error precision {ci(LB['error_precision'])}, error recall {ci(LB['error_recall'])};
  - faithful precision {ci(LB['faithful_precision'])}, faithful recall {ci(LB['faithful_recall'])}.
- Solver ERROR (a typed repair was found) only: precision {ci(LB['ERROR_only_precision'])}.
- auto CORRECT rows get their vote from the reference item. A panel UNFAITHFUL there means the panel rejected an audited-OK
  reference, i.e. panel noise.

ADD/DROP caveat: {addrop['n_addrop_only']} of {addrop['n_error_llm']} final-ERROR LLM rows have a solver repair made only of
ADD/DROP operators (flag `metadata_addrop_only_suspect`). These are often vocabulary or arity mismatches the aligner cannot
bridge. Where the panel says faithful they became CONTESTED. Operator mass of final ERROR rows:
`{json.dumps(R['heldout_error_ops_mass'])}`. Panel ops on tier-B ERROR rows: `{json.dumps(R['error_ops_tierB_panel'])}`.
Repair status: `{json.dumps(R['heldout_repair_status'])}`. The 8 s budget turns some COMPOUND results into COMPOUND_TIMEOUT,
and the panel decides those. convention_flags (diagnostic only): `{json.dumps(R['convention_flags'])}`.

## 7. Panel: calibration, real-error accuracy, agreement
The panel is family-disjoint from all 9 generator families: Anthropic Haiku-4.5 (P1), Zhipu GLM-4.6 non-thinking (P3),
Moonshot Kimi-K2-0905 (R1, the reserve replacing xAI Grok-4.3, which failed the gate). Items are nonce-disguised.

**Synthetic gate, prompt v1.** Every cheap model failed, mainly by rejecting contrapositives and the renames.
{tbl(['member', 'model', 'n', 'bal.acc', 'rec F', 'rec U', 'U@DOWN', 'U@UP', 'STRICT', 'RENAME', 'ref accepted', 'gate'], gate_rows(R.get('gate_prompt_v1')))}

**Synthetic gate, prompt v2 = production prompt.** v2 adds one generic line on logical equivalences. It was chosen after
seeing v1 on the same 77 items, so these numbers are optimistic. Gate: balanced accuracy ≥0.80 and recall ≥0.70 per class.
{tbl(['member', 'model', 'n', 'bal.acc', 'rec F', 'rec U', 'U@DOWN', 'U@UP', 'STRICT', 'RENAME', 'ref accepted', 'gate'], gate_rows(R.get('gate_prompt_v2')))}

**Real-error accuracy against human experts (track H, plan 4c).** The data are the 96 curated FOLIO/MALLS pairs (original
gold → expert-corrected) that are not z3-equivalent, with both formulas shown blind per sentence. The human verdict is
corrected = faithful, original = unfaithful. {TH.get('n_unambiguous')} pairs are unambiguous; the ambiguity-flagged ones are
reported separately.
{tbl(['member', 'judgements (unamb.)', 'accuracy', 'original flagged', 'corrected accepted', 'accuracy on ambiguous'], th_rows)}

By auto census class (majority, unambiguous pairs):
{tbl(['census class', 'pairs', 'majority accuracy'], th_cls)}

**Read this next to every panel-decided (tier B/C) label rate.** On real errors the panel majority is right about
{(TH.get('per_model') or {}).get('majority', {}).get('unambiguous', {}).get('accuracy')} of the time. It flags about
{(TH.get('per_model') or {}).get('majority', {}).get('orig_flagged_rate_unamb')} of the expert-confirmed wrong formulas.
But it accepts only about {(TH.get('per_model') or {}).get('majority', {}).get('corr_accepted_rate_unamb')} of the
expert-corrected ones. So the panel is **strict**: it over-calls unfaithfulness. Consequences:
- tier-B CORRECT rows are fairly reliable;
- tier-B ERROR rows and GOLD_WRONG verdicts contain false alarms;
- the corrected formulas are often themselves contestable, and 2606.02837 flags ambiguity as common.

Agreement between the two full raters, P3 and R1 (Cohen κ):
{tbl(['stratum', 'items', 'raw agreement', 'Cohen κ', 'P3 faithful rate', 'R1 faithful rate'], kap)}

- 3-rater pilot ({pil['sentences']} sentences, {pil['items']} items, all three models): Fleiss κ = {pil['fleiss_kappa']};
  unanimous share {pil['unanimous_share']}; pairwise Cohen κ `{json.dumps(pil['cohen'])}`.
- Adjudication: {adj['items_sent_to_P1']} of {adj['stage1_items']} stage-1 items
  ({adj['share_items_adjudicated']}) went to P1 across {adj['sentences']} sentences. P1 agreement counts:
  `{json.dumps(adj['P1_agreement_counts'])}`. Failed adjudication calls: {adj['failed_calls']}.

CONTESTED rate (CONTESTED / decided rows, LLM systems):
{tbl(['stratum', 'rate [Wilson 95%]'], cont)}

## 8. Parse rate and auto labels per system × prompt variant
{tbl(['system|variant', 'n', 'parse rate', 'CORRECT', 'VOCAB_GRAN', 'ERROR', 'COMPOUND', 'TIMEOUT'], sys_rows)}

## 9. Disguise (plan 5a)
- Each sentence gets its own CVCVC nonce bijection. It covers the Porter stems of the text's content words and the name
  tokens of ALL formulas of that sentence.
  - It is seeded by sha1(sentence_id), and a nonce is rejected if it is a WordNet lemma.
  - A name token that is a WordNet synonym of a sentence word reuses that word's nonce.
  - Logic symbols, quantifiers and numbers are unchanged.
- Guard: plain-z3 equivalence of class representatives before vs after disguise, 50 sentences:
  `{json.dumps(R['disguise_check'])}`.
- Deviation from the plan: NLTK Porter stems are used instead of spaCy lemmas.
- `metadata_disguised_text` and `metadata_disguised_fol` are on every row, for contamination checks.

## 10. Disjointness and exclusion
- Exclusion hashes: {ex['exclusion_hash_count']}. They cover FOLIO-validation (tasksource and refined), the curated
  FOLIO/MALLS sets, MALLS-test, the Logic-LM FOLIO_dev contexts and the few-shot exemplars: `{json.dumps(ex['exclusion_sources'])}`.
- Collisions after exclusion: **{ex['hash_collisions_with_screen_after_exclusion']}**; top-up collisions: {top.get('hash_collisions_with_screen')}.
- MALLS pool log: `{json.dumps(ex['malls_pool'])}`. CTRL pool log: `{json.dumps(ex['ctrl_pool'])}`.
- The 6 few-shot exemplars were hand-picked from the sha1-ordered eligible CTRL pool, because the auto-pick contained wrong
  golds. They are excluded from CTRL and calibration.

## 11. Screen audit (secondary deliverable)
- Logic-LM records per file: {sm.get('logiclm_records_per_file')}. Curated conclusions matched:
  {sm.get('distinct_conclusions_matched')}/{sm.get('curated_conclusions')} ({sm.get('conclusion_match_rate')}).
  Items per track: {sm.get('items_per_track')}.
- Panel scope (plan 6b): every track-L sentence with a VOCAB_GRAN/COMPOUND/TIMEOUT class, plus a 20% sha1 sample of the rest,
  plus a supplementary pass over the VOCAB_GRAN strings themselves. Track-H rows take their votes from the 4c real-error
  check, where the original formula is the candidate. Rows not covered have `label_tier = auto_only`.
- Final labels per track: `{json.dumps(R['screen_final_label'])}`. Tiers: `{json.dumps(R['screen_panel']['tier_by_track'])}`.
- Track-L auto label vs panel majority: `{json.dumps(R['screen_panel']['trackL_auto_vs_panel_majority'])}`.
- item_id = sha1(system + '|' + norm(text) + '|' + raw_fol)[:16]. The raw join keys are stored in every row.

## 12. Cost (OpenRouter, from per-call usage.cost; `cost_ledger.jsonl`)
{tbl(['phase', 'calls', 'USD'], cost_rows)}
Total **${R['cost_total_usd']}** of the $9.50 hard cap.

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
"""
    (ROOT / "dataset_card.md").write_text(md)
    print("dataset_card.md written", len(md))


if __name__ == "__main__":
    main()
