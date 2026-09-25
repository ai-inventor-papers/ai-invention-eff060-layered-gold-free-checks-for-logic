#!/usr/bin/env python3
"""results/deviations.json = dataset-5 D1-D9 (copied) + this artifact's D10+ (iteration 5)."""
from __future__ import annotations

import json

from cc import LAB, LOGS, RES, dump

NEW = [
    {"id": "D10", "utc": "2026-09-24T11:12:40Z", "step": "S-1", "what": "labeller/results/gate_report.json held {'status': 'NOT_RUN', ...} "
     "(dataset-5 D9); assemble_labels.py final mode iterates gr.values() with .get() and would crash on the strings; renamed to "
     "gate_report_D9_notrun.json before the gate", "cost": "none"},
    {"id": "D11", "utc": "2026-09-24T11:13:30Z", "step": "S-1", "what": "labeller/src/gloss.py: HARD_STOP_USD 6.0 -> 3.6 ($4 cap - 10%); Client.chat "
     "gained two OPTIONAL keyword args (extra body params, usage_out) used only by the iter-5 judge completion / auditors / frontier; "
     "verdict logic unchanged; sha before bd2a81a5..., after 61cd3fa8... (logs/gloss_sha_before.txt); gloss.py is not in the sealed code hash",
     "cost": "none"},
    {"id": "D12", "utc": "2026-09-24T11:20:50Z", "step": "STEP 1 gate", "what": "gloss_v1 FAILED on half A (haiku BA 0.776, qwen 0.855, both_yes 0.817). "
     "ONE revision prompts/gloss_v2.json (sha 329231d0...), written only from the half-A per-class error pattern (in-name negation rejected, "
     "non-word tokens accepted, argument-role reversals missed, reification / merges / rare synonyms rejected): explicit reading conventions. "
     "Committed to git before half B. gloss_v2 FAILED on half B (haiku BA 0.561 with 141/398 NO_VERDICT: analysis text before the JSON, "
     "truncated at max_tokens 300; 0.861 on verdicted items; qwen BA 0.883 with 0 NO_VERDICT)", "cost": "the gate cannot pass -> FALLBACK B"},
    {"id": "D13", "step": "STEP 2", "what": "the pre-declared FREE-gloss batching/order change was NOT used: the FREE gloss never ran (gate failed twice)",
     "cost": "none"},
    {"id": "D14", "utc": "2026-09-24T11:25:00Z", "step": "STEP 2 audit", "what": "audit re-targeted under FALLBACK B (addendum prereg): no CORRECT or "
     "ERROR_GLOSS rows exist, so the blind audit samples 100 ERROR_CERT + 100 MAPPED untouched rows; both auditors (Sonnet-5 + GLM-4.6, "
     "family-disjoint from checkers, peers and judges) rate every row; auditor-auditor kappa", "cost": "~$0.85"},
    {"id": "D15", "utc": "2026-09-24T11:17:00Z", "step": "STEP 0", "what": "exp-7 c_score_sig is NULL on every FREE row (it is the SIG-only exact "
     "consensus), so c_exact on FREE is recomputed from the eval-3 pair matrix with eval-2 consensus_mx.row_consensus (unchanged) = "
     "1 - share of other-family fewshot peers z3-equivalent with identical symbols; cross-checks: recomputed c_align == exp-7 c_score_align "
     "on 2,254/2,254 rows; c_exact == the sibling variants-file c_exact on 2,254/2,254", "cost": "none"},
    {"id": "D16", "utc": "2026-09-24T11:16:00Z", "step": "STEP 0 (pre-seal, label-blind)", "what": "exp 7's ORIGINAL-view flash-lite judge covered "
     "only 916/2,265 parseable FREE rows (budget stop + 224 network 502s). Completed on 1,289 rows with the byte-identical prompt/params "
     "(40/40 exp-7 cache-key regression hits); 1,232 scored, 57 json_parse failures kept as coverage failures (as the 60 exp-7 json_parse "
     "rows). Column judge_cheap_orig = exp-7 where present else iter-5; s9 restricts to exp-7 rows", "cost": "$0.062"},
    {"id": "D17", "step": "S-1", "what": "the prereg_freelab.json code_sha256 for src/freelab.py (05a5151e...) is the pre-D8 file; the running file "
     "(06e14f58...) equals the dataset-5 seal's code_sha256 (edited at 07:32:19 for D8, recorded in the seal); vendor files match "
     "VENDOR_SHA256.json; R0 reproduces the search-only label hash 9609ebbb... exactly", "cost": "none"},
    {"id": "D18", "utc": "2026-09-24T11:23:52Z", "step": "FALLBACK B", "what": "gate failed twice and neither checker passes alone (fallback C "
     "unavailable): assemble_labels --mode final -> every MAPPED row UNRESOLVED_GLOSS_GATE_FAILED; final seal b7916aea... (all), 79eb623a... "
     "(untouched); criterion (c) NOT_TESTABLE. The SIG end-to-end gloss check (300 rows) was not run: no gloss labels exist to validate",
     "cost": "(c) not testable in this iteration"},
    {"id": "D19", "utc": "2026-09-24T11:27:00Z", "step": "audit", "what": "anthropic/claude-sonnet-5 returned empty content on 2/6 pilot calls at max_tokens 400 "
     "(hidden reasoning consumed the budget); rerun with reasoning disabled (75 completion tokens); the 6 pilot rows are archived in "
     "results/audit_rows_pilot_sonnet_reasoning_default.jsonl and every reported Sonnet verdict comes from the reasoning-off config",
     "cost": "~$0.02"},
    {"id": "D20", "step": "STEP 0 / 20", "what": "V1/V2/V3/V5 computed at score-seal time from the sibling experiment_14 freeze DRAFT "
     "(freeze/consensus_variants.py, sha 6730a63b..., copied to freeze_copy_prelim/ before any label); the CONSENSUS_FREEZE_READY marker (M1) "
     "was absent at that time; V4 = NOT_COMPUTED unless M1 appears with frozen coefficients (logs/poll_M1.log)", "cost": "exploratory rows only"},
    {"id": "D21", "step": "STEP 3", "what": "one debug run of join_and_test.py with B=200 (results/analysis_rcomp_quick.json) before the final B=2000 run; "
     "fixes after it: FA=0.10 operating point replaced by the two achievable thresholds bracketing it (heavy ties at the maximum score made "
     "FA<=0.10 flag nothing), empty certificate-type cell skipped, net_test fallback for MAJ_EXACT (it endorses no ERROR, so AME is undefined). "
     "No population, estimand or parameter changed; the confirmatory verdict is fixed by the frozen rule", "cost": "none"},
    {"id": "D22", "step": "STEP 3", "what": "exp-5 has no frozen c_score_align-only threshold (its thresholds belong to fused models): the operating "
     "point is the label-free majority rule c_align > 0.5, plus the FA=0.10 bracket (descriptive)", "cost": "none"},
    {"id": "D23", "step": "STEP 3", "what": "H-MECH (ii) SCATTER and (iii) NET use all FREE rows with provisional labels (pair statistics need every labelled "
     "row of a sentence); (i) and (iv) use untouched rows. The system-level bootstrap uses 500 of the 2,000 shared replicates", "cost": "none"},
    {"id": "D24", "step": "STEP F", "what": "the frontier judge ran on the PROVISIONAL orig-view population (addendum prereg), not on a gated P0",
     "cost": "$0.68"},
    {"id": "D25", "utc": "2026-09-24T11:39:30Z", "step": "audit retry", "what": "after the main audit pass, 19 (row, auditor) calls had no verdict "
     "(GLM-4.6 exhausted 3,000 reasoning tokens; Sonnet-5 wrote analysis past 400 tokens). A regex recovered 1 truncated verdict; the "
     "retry with larger budgets was REFUSED (HTTP 403 aii_run_budget_exhausted: the run-level Test-idea budget, $12.08 of $12.00, was "
     "spent by the run's parallel artifacts; this artifact had spent $1.97 of its own $4 cap). Those 18 rows stay without a verdict "
     "(reported as n_verdict < 100); no further paid call was possible", "cost": "audit n 93-97 per auditor-class instead of 100"},
    {"id": "D26", "utc": "2026-09-24T11:45:00Z", "step": "STEP 3 (after the first final run)", "what": "the M1 marker (experiment_14 freeze, token ok, "
     "written 11:20:44Z) appeared after the first B=2000 run: its consensus_variants.py is byte-identical to the pre-label copy (V1/V2/V3/V5 "
     "unchanged); V4 (frozen coefficients applied to the sealed c_exact / c_align columns) added as an exploratory row flagged 'scored after "
     "label seal, code frozen externally' (results/score_seal_rcomp_v.json). Re-run with identical seeds: every pre-existing number is unchanged. "
     "Also added after seeing the first run: a validity flag on the noise correction (corrected AUROC outside [0,1] => non-differential "
     "assumption fails) and a 100-shuffle placebo supplement (the pre-set 20-shuffle placebo gave 17/20 vs the 18/20 bar; supplement 95/100)",
     "cost": "none"},
]


def main() -> None:
    old = json.loads((LAB / "deviations.json").read_text())["deviations"]
    dump(RES / "deviations.json", {"deviations": old + NEW, "note": "D1-D9 from dataset 5 (iteration 4); D10+ from this artifact (iteration 5)"})
    print(len(old), len(NEW))


if __name__ == "__main__":
    main()
