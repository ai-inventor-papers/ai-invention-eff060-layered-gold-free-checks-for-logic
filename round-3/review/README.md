# REVIEW_REPORT: iteration 3 (run_u75jRHUss0zo, NL→FOL gold-free faithfulness metrics)

This is an adversarial audit of the iteration-3 internal research report. The review is **blocking**: soundness 1, score 3/10, coverage partial. results_reported is true because the headline numbers were recomputed from the raw files and match.

## Layout
- `.terminal_claude_agent_struct_out.json`: the review (ReviewerFeedback schema, 12 critiques).
- `audit/recompute_headlines.py` / `.json`: recomputes the report's headline numbers from raw per-item files.
  - T1 (`gen_art_experiment_6/results/per_item_T1.jsonl`): c_score_align strat 0.7415 vs flash-lite disguised 0.6425, Δ 0.099 [0.050, 0.145]. L25 pooled Δ is +0.069 [−0.020, 0.146], not significant, and the report omits it.
  - R_COMP SIG (`gen_art_experiment_7/results/analysis_rows_SIG.jsonl`): within-template 0.954 vs 0.587, e = 0, d = 0.260.
- `audit/perturb_c_align_constant.py` / `.json`: checks the PERTURB consensus scores. 94–100% of mutants of every operator score c_align = 1. The within-base AUROC is therefore fixed by the base-endorsement rate: 0.866 predicted vs 0.866 reported. The per-operator ranking carries no information.
- `audit/write_review.py`: generates the review JSON.

## How to run
`python3 audit/recompute_headlines.py` needs numpy and scipy and takes about 1 minute; its bootstrap uses B=1000. `python3 audit/perturb_c_align_constant.py` runs in seconds. Both read the iteration-3 artifacts read-only.

## Restoring removed files
Nothing is marked `delete`, so there is nothing to restore.
