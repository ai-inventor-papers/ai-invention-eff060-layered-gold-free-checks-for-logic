> NOTE (published copy): this file names server paths this repository
> does not publish (a stage it does not ship, or another run's workspace),
> so the steps that read them will not run from a clone as written:
>   /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json

# Reproducing T1 (consensus vs paid LLM judges on held-out dataset E)

This file records what was **actually run** on 2026-09-24, from 01:35 to 03:56 UTC. That run was interrupted twice by
platform restarts. Every stage is cached and idempotent, so re-runs resumed where they stopped; see
`results/deviations.json` D1 and D2.

## 1. Copy the artifact

```bash
cp -r . ~/t1
cd ~/t1
```

The workspace is self-contained. `data/` holds every frozen input, copied from earlier artifacts:
- the label-free units `data/E_units.json`;
- exp 5's frozen consensus scores `data/exp5/per_item_E.jsonl`;
- exp 6's local baselines `data/exp6_*`;
- `data/folds_E.json` and `data/frontier_frame.json`.

The labels come from dataset E. The code reads it from its original path, shown below; to use it elsewhere, copy the
file and edit `src/e_pool.py`'s path and the `E_FULL` constant in `tests/audit_raw_T1.py`:
`/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json`

## 2. System, Python, environment

These are the versions actually used:
- Ubuntu (container);
- Python 3.12.14;
- uv 0.6.14;
- NVIDIA driver 580.159.04.

```bash
bash restore.sh venv    # = uv venv .venv --python=3.12 ; uv pip install -r requirements.txt ;
                        #   uv pip install torch==2.11.0 --index-url https://download.pytorch.org/whl/cu128 --reinstall-package torch
uv pip install --python .venv/bin/python matplotlib==3.11.2   # figures (now also listed in requirements.txt)
bash restore.sh nltk    # WordNet / omw-1.4 / words into data/nltk_data (disguise + VEX lemmatisation)
```

`pyproject.toml` pins all 132 packages at the exact versions in `.venv` (from `uv pip freeze`, also saved as
`logs/pip_freeze.txt`). Key versions:

| package | version |
|---|---|
| torch | 2.11.0+cu128 |
| numpy | 2.5.3 |
| scikit-learn | 1.9.1 |
| scipy | 1.18.1 |
| statsmodels | 0.15.0 |
| transformers | 5.17.0 |
| sentence-transformers | 6.1.0 |
| z3-solver | 5.1.0.0 |
| aiohttp | 3.14.3 |
| matplotlib | 3.11.2 |

Alternatively, `uv sync` uses the pyproject, with the cu128 index already declared.

## 3. Models, data and environment variables (names only)

- **Environment variables:**
  - `OPENROUTER_BASE_URL` and `OPENROUTER_API_KEY`: every LLM call goes through `src/budget.py` to that base URL.
  - `PYTHONHASHSEED=0`.
  - `HF_HOME` / `HF_HUB_CACHE`: the run's shared cache.
- **Local weights**, downloaded by `scripts_download.py` into the HF cache:
  - `MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli`
  - `cross-encoder/nli-deberta-v3-large`
  - `sentence-transformers/all-mpnet-base-v2`
- **API models** (OpenRouter):
  - `google/gemini-2.5-flash-lite`: cheap judge and verbaliser;
  - `openai/gpt-4.1-nano`: P(YES) judge and SC-5 sampler;
  - `google/gemini-3.1-pro-preview`: frontier judge, reasoning effort low, max_tokens 4000.
- **Prompts** are frozen by sha1 in `prereg_T1.json`: RUBRIC_A `06686913…`, USER_JSON_A `5b3ccfb9…`, USER_YESNO
  `b36e93cb…`, VERBALISE `584f33d0…`, SC few-shot `6c4db3c3…`.
- **API cost cache.** `results/llm_cache.jsonl` holds every API response. With it, re-running any API stage costs
  **$0** and returns identical scores. Without it, a fresh run costs about $2.40 (see `results/api_cost_ledger.json`);
  temperature-0 outputs are near-deterministic, with retest exact-match 0.984.

## 4. Commands, in the order actually run

All commands run from the workspace root with `export PYTHONHASHSEED=0`.

**Hardware:**
- setup and pilots (steps 1–3): an earlier container (GPU model not recorded in the logs; these steps are CPU/API only);
- sweeps and analysis: NVIDIA RTX 2000 Ada (16 GB VRAM), 6 CPUs (cgroup), 251 GB RAM.

**Seeds:**
- bootstrap seed 0 (B = 2000);
- GEE bootstrap seed 0 (B = 1000; n_conditions B = 500);
- permutation null seed 0 (100 reps);
- placebos seed 0.

| # | command | what it does | runtime |
|---|---|---|---|
| 1 | `.venv/bin/python method.py --stage t1_prep` | key bijection, label-vector hashes, reproduction gates, VEX declaration → `results/repro_gates.json`, `results/vex_declaration.json` | 86 s |
| 2 | `.venv/bin/python method.py --stage t1_pilot` | label-blind 20-row pilots → `results/pilot/` | 30 s |
| 3 | `.venv/bin/python method.py --stage t1_freeze` | writes `prereg_T1.json` + `prereg_T1.sha256` (sha256 `c2a6cf84…`, 01:54:08Z). **Do not re-run:** the analysis refuses a changed prereg. | <1 s |
| 4 | `bash t1_api_chain.sh` | judges `cheap_disg,cheap_orig`; judges `cheap2_disg,cheap2_orig`; `strong --which orig`; `verbalise`; `sc_gen`; `retest`; `strong --which disg` (the last is stopped by the pre-registered reserve rule) | ~10 min per cheap arm, 80 s frontier, ~9 min verbaliser, ~5 min SC-5 |
| 5 | `method.py --stage verbalise` ; `--stage sc_gen` ; `--stage retest` | re-issue calls that failed during relay outages (cached, idempotent) | <1 min |
| 6 | `.venv/bin/python method.py --stage nli --which api` | GPU: DeBERTa NLI in both directions (2 checkpoints) plus mpnet cosine on 6,228 (text, verbalisation) pairs | 5.4 min |
| 7 | `.venv/bin/python method.py --stage sc_score --which sc5_samples` | CPU z3 equivalence modulo vocabulary, 25,429 pairs | 50 s |
| 8 | `.venv/bin/python method.py --stage t1_analysis` | join, all analyses (a)–(j), verdict, tables, figures, method_out | 8.5 min |
| 9 | `.venv/bin/python tests/audit_T1.py` | independent re-derivation from the joined per-row table | ~1 min |
| 10 | `.venv/bin/python tests/audit_raw_T1.py` | re-derivation from RAW files (dataset E labels, exp 5 scores, raw API score files), plus placebo tests | ~1 min |
| 11 | `aii_json_format_mini_preview.py --input method_out.json` (aii-json skill) | full / mini / preview outputs, validated as `exp_gen_sol_out` | seconds |

The figures were re-rendered after `t1_analysis`, from `results/analysis_T1.json`, via `src/report_T1.figures`, once
two legend and import fixes were in (D6). No number changed.

## 5. What you should get

These are the headline results (`results/verdict_T1.json`, `results/tables_T1.md`); the paper's T1 results section and
forest figure use them. All figures are on the R_AB E_POOL PRIMARY population: n = 2,686 (1,822 ERROR / 864 CORRECT),
292 sentences. "Strat" means stratified AUROC.

| quantity | value |
|---|---|
| strat AUROC, `c_score_align` / flash-lite disguised | 0.741 / 0.642 |
| pooled AUROC, `c_score_align` / flash-lite disguised | 0.782 / 0.696 |
| **(a)** confirmatory strat Δ | **+0.099 [0.049, 0.146]** |
| (a) long pool | +0.116 [0.070, 0.163] |
| (a) R_A L20+EXC | +0.299 |
| **(b)** nested [S4_full + c] − S4_full, strat | **+0.039 [0.021, 0.057]** (null p95 0.009) |
| (d) frame ratio vs gemini-3.1-pro-preview | 0.957 [0.887, 1.034] |
| (d) nested frame gain | +0.037 [0.008, 0.066] |
| (d) cost per item, consensus / frontier | $1.2e-4 / $3.65e-3 |
| VEX Δ | +0.306 [0.232, 0.376] |
| M3 (words) | +0.146 [−0.051, +0.361] → **DISCONFIRMED** |
| overall | **CONFIRMED** |
| API spend | $2.395 |

Other outputs:
- `figures/forest_T1.png`: all cell deltas.
- `figures/complexity_curves.png`: AUROC by length and by number of conditions.
- `full_method_out.json`: per-row oriented scores of every metric.

### Independent checks

- `tests/audit_T1.py`: 5 headline numbers match to 1e-3.
- `tests/audit_raw_T1.py`: re-derives the population, the pooled and stratified AUROCs, the confirmatory and long-pool
  Δ, and the frame ratio exactly from the raw files. The same bootstrap test **fails**, as it should, on
  within-stratum permuted labels (Δ +0.021 [−0.008, +0.049]) and on a random-score challenger (Δ −0.152).
- The nested (b) gain and M3 were re-derived by `audit_T1.py` (per-row table, statsmodels refit), not from the raw
  files. The (b) gain is additionally checked against a 100-rep label-permutation null, where it sits at percentile 1.00.
