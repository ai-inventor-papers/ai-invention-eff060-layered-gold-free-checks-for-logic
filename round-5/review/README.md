# Iteration-5 review of the internal research report (REVIEW_REPORT step)

This folder holds the adversarial audit of the run's internal research report after iteration 5.
The review checks completeness, traceability, recorded reasoning and honesty. Each headline
number was recomputed from the artifacts' raw per-item files.

## Layout
- `.terminal_claude_agent_struct_out.json`: the structured review (scores, 11 critiques, blocking flag).
- `audit/recompute_e2a.py` / `.json`: recomputes E2-A (exp 11) AUROCs per cell from `per_item_E2A.jsonl`, and counts the flash-lite-scored R_AB rows.
- `audit/recompute_e2b.py` / `.json`: recomputes E2-B (exp 12) V0 and flash-lite AUROCs and V0's flag rate on CORRECT rows.
- `audit/recompute_rcomp_free.py` / `.json`: recomputes R_COMP FREE (exp 13) within-template AUROCs (c_align, c_exact, hyb, nf, judges) and the MAPPED flag rate.
- `audit/write_review.py`: writes the review JSON.

## How to run
```
python3 audit/recompute_e2a.py
python3 audit/recompute_e2b.py
python3 audit/recompute_rcomp_free.py
python3 audit/write_review.py
```
Requires Python 3 with scikit-learn. The scripts read the sibling artifact workspaces of this run read-only.

## Restoring removed files
Nothing is marked for deletion. Every file here is small text or code (see `.aii/manifest.yaml`).
