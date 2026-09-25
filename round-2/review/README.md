# REVIEW_REPORT — iteration 2 (run_u75jRHUss0zo, NL→FOL gold-free faithfulness metrics)

This is an adversarial audit of the iteration-2 internal research report. The verdict is **blocking**: soundness 1, score 3/10, coverage partial.

## Layout
- `.terminal_claude_agent_struct_out.json`: the review (ReviewerFeedback schema).
- `audit/pt_vs_s4.py` / `audit/pt_vs_s4.json`: a reviewer recomputation that joins exp 5's `results/per_item_E.jsonl` with exp 6's `full_method_out.json` on dataset-E R_AB rows (n=2,672).
  - It re-derives these AUROCs: PT 0.790, local judge 0.710, S4_local 0.748.
  - It computes the paired deltas no artifact reported: PT − S4_local +0.042 [0.014, 0.070], and nested [S4, PT] over S4 +0.055 [0.036, 0.074].
- `audit/report_iter_1.md`, `audit/report_iter_2.md`: copies of the two report versions, used to diff the iteration-1 section. Only formatting changed, plus one SAC3 sentence.

## How to run
`python3 audit/pt_vs_s4.py` needs numpy and scikit-learn and takes about 1 minute. It reads the iteration-2 artifacts read-only.

## Restoring removed files
Nothing is marked `delete`, so there is nothing to restore.
