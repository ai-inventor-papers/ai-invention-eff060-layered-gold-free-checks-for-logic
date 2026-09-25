# Review of the iteration-4 research report (run_u75jRHUss0zo)

This directory holds an adversarial audit of the internal research report after iteration 4. The review itself is in `.terminal_claude_agent_struct_out.json`: score 3, blocking, coverage partial.

## Layout
- `.terminal_claude_agent_struct_out.json`: the structured review (ReviewerFeedback schema).
- `audit/recompute_csc.py` → `audit/recompute_csc.json`: independent recompute of exp-9 CSC headline numbers (strat AUROC, e, d, PRIMARY composition) from `round-4/experiment-9/src/results/per_item_csc_E.jsonl`.
- `audit/recompute_perturb_csc.py` → `audit/recompute_perturb_csc.json`: base false-alarm rate vs mutant recall for each consensus arm, and LOCAL2 tie share, from `round-4/experiment-10/src/results/perturb_csc_scores.jsonl`.
- `audit/write_review.py`: writes the review JSON.

## How to run
```
python3 audit/recompute_csc.py
python3 audit/recompute_perturb_csc.py
python3 audit/write_review.py
```
The scripts use the standard library only, and they read the sibling artifacts read-only.

## Restoring removed files
Nothing is marked for deletion (`.aii/manifest.yaml` has no entries). All files here are small text files.
