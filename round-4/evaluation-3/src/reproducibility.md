# Reproducing T8 (vocabulary-fix prediction, R_COMP second population, iteration-5 power, verified record)

This artifact is CPU only. It makes **no LLM or API calls, needs no API keys and spent $0**. The steps below are exactly what was run on 2026-09-24.

## 1. Copy the artifact

```bash
cp -r gen_art_evaluation_3 ~/t8 && cd ~/t8
```

The scripts read their inputs **read-only** from absolute paths in `src/t8_paths.py` (`RUN = /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop`).
If you are on another machine, edit `RUN` there, and the three hard-coded `RUN`/`E6T1`/`E7`/`E8` paths at the top of `audit/rederive.py`. The input workspaces are:

- `iter_3/gen_art/gen_art_evaluation_2`: eval 2. Its `src/` and `vendor_exp5/` are **imported unchanged via sys.path** (code sha `dd73975642f428cc`).
- `iter_3/gen_art/gen_art_experiment_{6,7,8}`
- `iter_1/gen_art/gen_art_dataset_1`
- `iter_2/gen_art/gen_art_experiment_5`, used by eval 2's `frame.build_frame`
- `iter_3/review_report/review_report/audit`, `iter_3/gen_art/gen_art_research_1`, and `iter_3/upd_hypo/upd_hypo` (the iteration-4 hypothesis text)

`tables/source_hashes.csv` lists the sha256 of every input read.

## 2. Environment

- Ubuntu with Linux 6.8. No system packages beyond `uv` are needed.
- Python **3.12.14**.

```bash
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r pyproject.toml   # exact pins below
```

Pinned versions are in `pyproject.toml` and equal `uv pip freeze` of the venv that produced the results. The key ones:
`z3-solver==5.1.0.0` (z3 5.1.0), `numpy==2.5.3`, `pandas==3.0.6`, `scipy==1.18.1`, `statsmodels==0.15.0`, `scikit-learn==1.9.1`,
`matplotlib==3.11.2`, `loguru==0.7.3`.

## 3. Data, models, environment variables

- No downloads, models or checkpoints are needed.
- Set `PYTHONHASHSEED=0` and `PYTHONDONTWRITEBYTECODE=1`. `eval.py` and `run_all.sh` set both. PYTHONHASHSEED matters because eqmv's aligner iterates over hash-ordered sets. PYTHONDONTWRITEBYTECODE keeps eval 2's read-only workspace free of new `.pyc` files.

## 4. Commands, in the order they were run

The whole pipeline runs with `.venv/bin/python eval.py`, or equivalently `./run_all.sh`. To reuse the stored R_COMP matrix, add `--skip-matrix`. To resume from a step, use `--from <step>`.

| # | Command | What it does | Runtime (4-CPU cgroup, no GPU, shared host at load ~180) |
|---|---|---|---|
| 1 | `src/t8_prereg.py` | Writes `prereg_d_split.json` and its sha256 **before** any Part-1 number. It reads the 0.388 discount from exp 8 and the cuts from eval 2 | <1 s |
| 2 | `src/t8_run_rcomp_matrix.py --stage mini`, then `s50`, then `all` | eval-2 `pairwise.work` on 442 (sentence, condition) tasks; spawn pool with 4 workers, eqmv 3000 ms, pair cap 30 s → `results/pair_matrix_RCOMP.jsonl` | 19 s + 12 s + 18 s |
| 3 | `src/t8_part1.py` | Gates G0-G2, pair classes (NAME_ONLY z3 on 4 workers), the counting rules, 500 MC draws (seed 0), SentBoot B = 2000 (seed 0), GEE, the placebo (200 draws, seed 0) and c_vres | ~65 s |
| 4 | `src/t8_part1_net.py` | NET per rule and pool. Δ(e+d) at B = 2000; unchanged `net_test` at B = 200 | ~20 min (contended host) |
| 5 | `src/t8_part3.py` | Power: B = 1000 sentence subsamples per cell and n (seed 1000+n); R_COMP FREE scenarios (300 resamples, seed 7) → `power_E2.json` | ~11 min |
| 6 | `src/t8_part2.py` | G3, SIG e/d/scatter/NET/GEE, the SIG-FREE paired drop, FREE classes, out-of-sample validation (500 MC, seed 0) → `pairwise_classes_RCOMP.jsonl` | ~4 min |
| 7 | `src/t8_part4.py` | Record tables (a)-(m), `record_claims.csv`, `record_mismatches.csv` | ~25 s |
| 8 | `src/t8_figs.py` | 2 figures (PDF, PNG, JSON spec) | ~17 s |
| 9 | `audit/rederive.py` | Independent re-derivation and placebos → `audit/rederive.json` | ~27 s |
| 10 | `src/t8_eval_out.py` | `eval_out.json` (exp_eval_sol_out) | ~6 s |
| 11 | `src/t8_record_md.py` | `record.md`, `tables/source_hashes.csv` | ~7 s |

After these, the aii-json `aii_json_format_mini_preview.py --input eval_out.json` produced `full_/mini_/preview_eval_out.json`, and `aii_json_validate_schema.py --format exp_eval_sol_out` passed.

## 5. Expected outputs and numbers

- **Gates** (`results/part1.json`, `results/part2.json`):
  - G0: END_MAJ e 0.1249 / d 0.5371; AUROC c_exact 0.7477 and c_align 0.7837.
  - G1: pairs_E coverage 1.000.
  - G2: concordance 0.9997.
  - G3: match rate 1.000 on all three score columns.
- **Part 1, 3-pool** (`results/part1.json` pools.3pool; `tables/p1_rule_cuts.csv`): d under R_align 0.415, R_point_label 0.402 [0.336, 0.471], R_liberal 0.396, R_oracle 0.385; e_ceiling 0.162.
- **Part 1, 9-family:** d 0.537 / 0.532 / 0.522 / 0.586 for the same four rules.
- **Part 2** (`results/part2.json`):
  - SIG e 0.000, d 0.2596, weak/strong d 0.143/0.965.
  - SIG-FREE exact-agreement drop +0.479 [0.447, 0.513]; ALIGN∪NF recovers 0.455.
  - Validation calibration error −0.372 [−0.423, −0.323], so NOT validated.
- **Part 3** (`power_E2.json`):
  - L25 yield 0.37.
  - MDE80 at L25 250/300/350/400 = 0.130/0.119/0.110/0.103.
  - Detecting 0.069 on L25 needs 326 usable ≈ 882 planned sentences.
- **Part 4** (`record.md`): 64 claims, 60 match, 1 mismatch.
- **Audit** (`audit/rederive.json`): 11/11 checks pass. Placebos:
  - condition permutation 0.000 [−0.014, 0.015];
  - VOCAB-share label shuffle inside its null band.
- **Where they appear:** `README.md` has the headline table. The figures are `figures/fig_d_floor_vs_words.*` and `figures/fig_sig_vs_free_agreement.*`.

The stochastic parts (MC, bootstraps, placebos) use fixed numpy `default_rng` seeds, so reruns give identical numbers. The one exception is eqmv timeouts, and none occurred: 0 UNKNOWN pairs.
