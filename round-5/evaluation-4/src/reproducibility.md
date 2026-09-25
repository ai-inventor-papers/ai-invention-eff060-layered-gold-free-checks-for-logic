# Reproducibility — corrected record (iteration 5, evaluation 4)

This is what was actually run, on Ubuntu (Linux 6.17). It used 4 CPU cores and no GPU, made no network or LLM calls, and cost $0.

## 1. Get the folder

```bash
cp -r . ~/record_eval4
cd ~/record_eval4
```

Inputs are read in place, read-only, from absolute paths under
`../../../` (iterations 1–5: the iteration-4 paper draft and review; eval 2/3; exp 6/7/8/9/10; datasets 4/5; the iter-3/iter-4 hypothesis and strategy JSONs; the iter-5 strategy and sibling workspaces). The run tree must be mounted at that path. Nothing is downloaded. A missing input produces NOT_FOUND rows, not a crash.

## 2. Environment

- Python 3.12.14 (via `uv`); no system packages beyond `uv`.
- Exact versions (also pinned in `pyproject.toml`): contourpy 1.4.0, cycler 0.12.1, fonttools 4.66.0, kiwisolver 1.5.1, loguru 0.7.3, matplotlib 3.11.2, numpy 2.5.3, packaging 26.3, pandas 3.0.6, pillow 12.3.0, pyparsing 3.3.3, python-dateutil 2.9.0.post0, pyyaml 6.0.3, scipy 1.18.1, six 1.17.0.
- The figures import the house-style helpers from `/ai-inventor/.claude/skills/aii-data-fig-gen/scripts/chart_style.py` (read-only).

```bash
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r pyproject.toml
```

## 3. Data, models, keys

None. No API keys are needed: `eval.py` asserts that `openai` and `requests` are never imported.

## 4. Commands (in order), with seeds and runtime

```bash
./run_all.sh            # = .venv/bin/python eval.py ; ~20–30 s wall clock on 4 CPUs
```

`eval.py` does the following, in order:
1. It exports `claims_spec.yaml`.
2. It checks 244 claims and 258 transcription rows via `src/checker.py`, writing `numbers.csv` and `mismatches.csv`.
3. It scans the spend ledgers (`results/spend_iter4.json`).
4. It builds `record_final.md` and runs the 8 lints (`lint_report.json`); the run fails on any lint.
5. It writes `claims_ledger.csv`, `reviewer_checklist.csv`, `skeleton_iter5.md` and `skeleton_resolution.json`.
6. It draws the figures `figures/F1–F4` (`.pdf`, `.png`, `.json`).
7. It runs the independent audit `audit/rederive.py` in a separate process, with its own code path: sentence-cluster bootstrap B = 2000, seed 0; label placebo permuted within stratum, seed 7; placebo CI B = 500, seed 1.
8. It runs the checker mutation test `audit/checker_mutation.json`.
9. It writes `tables/source_hashes.csv` and `eval_out.json`.

After it, run:

```bash
python /ai-inventor/.claude/skills/aii-json/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file $PWD/eval_out.json   # PASSED
python /ai-inventor/.claude/skills/aii-json/scripts/aii_json_format_mini_preview.py --input $PWD/eval_out.json   # full_/mini_/preview_
```

## 5. What you should get

- `numbers.csv`: 554 rows. The 244 claims are all MATCH (0 MISMATCH / NOT_FOUND / AMBIGUOUS). Paper vs file: 153 MATCH, **15 MISMATCH** (listed in `record_final.md` §0), 76 not in the paper.
- `lint_report.json`: 0 failures. 43 correction markers; 42 have the original sentence found in the paper.
- `audit/rederive.json`: **17/17 pass** (c_csc 0.614, FREE_exact 0.770, c_score_align 0.774, e 0.459/0.173, d 0.139/0.323, CTRL share 0.274, base FA 0.712/0.803/0.986/0.757, E2 and R_COMP FREE label counts, 77%/61%, iter-4 spend 0.35). Shuffled-label placebo AUROC ≈ 0.458 with a CI covering 0.5. Our c_csc CI ≈ [0.487, 0.734] vs T4 [0.493, 0.736] (T4 is transcribed).
- `audit/checker_mutation.json`: 10/10 mutations caught, 10/10 untouched claims MATCH.
- `results/spend_iter4.json`: iteration-4 artifacts $0.349; all artifacts with records in the window $4.687; unaccounted $2.313 of the $7.00 phase budget. The ledger count can grow while the iteration-5 siblings run; this changes only the file count, not the window sums.
- `reviewer_checklist.csv`: 9 CLOSED, 2 PARTIAL (critiques 7 and 8).
- `skeleton_resolution.json`: depends on when you run it. At our run, 9 named sibling files existed.
- Where these appear in the paper: `record_final.md` sections 1–17 replace or extend paper §3.3–§3.7, §4.1–§4.7 and "What we have learned" (each section names the lines it replaces). F1–F4 support §3.2/§4.2 (F1, F2), §4.6 (F3) and §3.5 (F4).
