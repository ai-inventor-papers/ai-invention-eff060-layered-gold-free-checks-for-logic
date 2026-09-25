# REVIEW_REPORT — run_u75jRHUss0zo, invention iteration 1

Adversarial audit of the iteration-1 internal research report (gold-free NL→FOL faithfulness metrics) against the four
executed artifacts (exp A FOL-Triage `gen_art_experiment_1`, exp C consensus `gen_art_experiment_3`, exp D judge+baselines
`gen_art_experiment_4`, dataset E `gen_art_dataset_1`). `gen_art_experiment_2` (planned candidate B: template-NLI B1 +
z3-distinguishing-worlds B2) is empty — it never ran.

## Layout
- `.terminal_claude_agent_struct_out.json` — the structured review (scores, critiques, flags).
- `audit/join_audit.py` → `audit/join_audit.json` — joins A/C/D per-item scores on `item_id`; label-set disagreement across
  experiments; own-label AUROC recomputation (c_score 0.8655, fused 0.7589, judge_disg 0.7846 excl. 11 JSON failures).
- `audit/paired_boot.py` → `audit/paired_boot.json` — paired sentence-clustered bootstrap (B=2000) on the 389 common,
  label-consistent track-L items: c_score − judge_cheap_disg = +0.057 [−0.022, 0.137]; fused − judge = −0.020 [−0.111, 0.074].
- `audit/rescore_adjudicated.py` → `audit/rescore_adjudicated.json` — re-scores iteration-1 metrics under dataset E's
  `screen_adjudicated_labels.json`: ranking reverses (tier A+B, n=304: fused 0.872, l2_bow 0.817, c_score 0.776, judge 0.771).

## How to run
`python3 audit/join_audit.py && python3 audit/paired_boot.py && python3 audit/rescore_adjudicated.py`
(needs numpy + scikit-learn; reads the sibling artifact directories read-only).

## Restoring removed files
Nothing is marked `delete`; the workspace holds only text and small JSON.
