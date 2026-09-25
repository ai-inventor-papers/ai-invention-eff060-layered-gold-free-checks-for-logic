# Reproducing this artifact (consensus-mechanism audit, T4 on dataset E, plus the verified record)

These are the steps that were actually run to produce the files in this folder (2026-09-24). It is CPU only. **No API keys are needed and no LLM calls are made.**

## 1. Get the folder

```bash
cp -r . ~/work/consensus_audit
cd ~/work/consensus_audit
```

The code reads its **inputs by absolute path** (`src/paths.py`: `RUN = ../../..`). The inputs are:
- exp 5 (`round-2/experiment-5/src`)
- exp 6 (`iter_2/gen_art/gen_art_experiment_6`)
- dataset E (`round-1/dataset-1/src`, whose 27.7 MB `full_data_out.json` and `raw/generations.jsonl` are not copied)
- datasets 2 and 3 and evaluation 1 (`iter_2/gen_art/...`)
- the reviewer audit (`iter_2/review_report/review_report/audit/`)
- iteration-1 exp 1, 3 and 4

Every input smaller than 10 MB is mirrored under `inputs_copy/3_invention_loop/...`, with its sha256 in `tables/source_hashes.csv`. On another machine, either recreate that directory tree at the same absolute path, or edit `RUN` in `src/paths.py`. The vendored exp-5 scoring code is in `vendor_exp5/`, and its hashes are checked identical to the source.

## 2. Environment (as used)

- OS: Debian 12 container (Ubuntu works the same), Linux 6.8, **4 vCPU (AMD EPYC 9655P), 29 GB RAM cgroup limit, no GPU**.
- Python **3.12.14**, installed with `uv` (no system packages beyond `uv`).

```bash
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r pyproject.toml
```

`pyproject.toml` pins all 32 packages to the versions installed (from `uv pip freeze`). The key ones:
- `z3-solver==5.1.0.0` (identical to exp 5; a different z3 can flip eqmv outcomes and break gate G2)
- `numpy==2.5.3`, `pandas==3.0.6`, `scipy==1.18.1`, `scikit-learn==1.9.1`, `statsmodels==0.15.0`, `loguru==0.7.3`
- `matplotlib`, `pyyaml`, `psutil` and `pytest` are pinned as well

No data, model or checkpoint downloads. No environment variables are required. `eval.py` sets `PYTHONHASHSEED=0` itself by re-executing, because eqmv's aligner iterates hashed sets.

## 3. Commands that were run, in order

```bash
uv run pytest -q tests                            # 23 passed (~25 s)
.venv/bin/python eval.py --stage all              # ~5 min wall on 4 vCPU:
#   src/copy_inputs.py      -> inputs_copy/, tables/source_hashes.csv
#   src/run_matrix.py rab   -> 292 R_AB sentences, 4 spawn workers, ~30 s
#   src/run_matrix.py rest  -> remaining 408 sentences, ~70 s       => results/pair_matrix_E.jsonl (700 sentences, 29,107 pairs)
#   PART A (src/part_a.py)  -> gates G0/G1/G2, prereg_mech.json(+sha256), pairwise_classes_E.jsonl, cuts, M1/M2/NET/SCATTER/M3/M4 (~4.5 min)
#   PART B (src/record.py)  -> verified-record tables (~10 s)
#   audit/rederive.py, audit/m2_specificity.py -> audit/*.json (~1.5 min)
#   figures + eval_out.json
.venv/bin/python eval.py --stage all --skip-matrix   # the final run: reuses the matrix, re-runs every analysis + audits
python /ai-inventor/.claude/skills/aii-json/scripts/aii_json_format_mini_preview.py --input eval_out.json   # full_/mini_/preview_
python /ai-inventor/.claude/skills/aii-json/scripts/aii_json_validate_schema.py --format exp_eval_sol_out --file $PWD/eval_out.json
```

Seeds are fixed throughout:
- the sentence-cluster bootstrap uses `numpy.random.default_rng(0)` with B = 2000;
- the M4 draws use `sha1('M4|'+row_key+'|'+k+'|'+j)` with 50 draws per k;
- the M3 tie-break uses `sha1('M3|'+row_key)`;
- the audits use `default_rng(7/11/123)`.

The matrix is deterministic: three independent computations gave 0 differing pairs out of 29,107 (`results/matrix_determinism_check.json`). The matrix stage is resumable. It skips sentences already in `results/pair_matrix_E.jsonl`, so move that file away to recompute it.

## 4. What you should get

Everything below is in `eval_out.json` → `metrics_agg` / `metadata.verdicts`, `results/part_a.json`, and `tables/*.csv`.

- **Gates:**
  - G0: R_AB n = 2686 (1822 ERROR / 864 CORRECT, 292 sentences); R_A L20+EXC = 449 (261/188).
  - G1: frozen c_score_align AUROC 0.7824 (R_AB) and 0.8599 (R_A L20+EXC).
  - G2: mismatch rate 0.00325 (24 of 7,383 rows).
- **Decomposition, R_AB (2,672 scorable rows):**
  - END_MAJ: e = 0.124, d = 0.537, AUROC_b = 0.669.
  - Graded c_score_align: 0.784; Δ = +0.114 [0.091, 0.140].
  - c_score_exact: 0.748.
  - `tables/ed_decomposition_cuts.csv` and `figures/fig1_e_d_by_complexity.*` hold the cuts.
- **Verdicts:**
  - M1 INCONCLUSIVE (n_conditions partial slope −0.04 [−0.53, 0.45]).
  - M2 CONFIRMED (+1.95 [1.12, 2.77]) but **non-specific**: the shuffled-label placebo also gives a positive slope, and the label×words interaction is −0.29 [−0.77, 0.20]. See `audit/m2_specificity.json`.
  - NET: DEGRADES with length, Δ(e+d) = +0.356 [0.198, 0.493], driven by d. Its placebo gives −0.034 [−0.108, 0.034].
  - SCATTER: SI_err 0.159 vs SI_cor 0.760, ratio 4.45 (`figures/fig3_scatter_index.*`).
  - M4: CONFIRMED, k95 = 3; AUROC(k) 0.685 … 0.784 (`figures/fig2_auroc_k.*`, `tables/m4_auroc_k_cost.csv`).
  - Best cross-fitted 3-pool deepseek+microsoft+openai: out-of-fold AUROC 0.785.
  - LOFO minimum Δ = −0.011.
- **Verified record:** `tables/hypothesis_verdicts.csv` has 48 VERIFIED_MATCH and 0 DISCREPANT or NOT_IN_FILES rows. `tables/pt_vs_s4_rerun.csv` reproduces every reviewer point to 1e-4 and every CI to 0.01.
- **Audit:** `audit/rederive.json` re-derives 13 headline numbers from raw files through separate code, and all match to 1e-9. The AUROC permutation test gives p = 0.001 (null max 0.539).

In the paper, these numbers belong in the "mechanism of cross-family consensus" section and its complexity figure (fig1/fig3), the peer-count/cost figure (fig2), and the corrected-record appendix (PART B tables).
