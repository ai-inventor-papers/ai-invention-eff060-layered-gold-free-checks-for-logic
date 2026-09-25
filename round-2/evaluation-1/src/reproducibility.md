# Reproducibility: re-checking iteration-1 logic-metric results across label sets

This artifact is a CPU-only re-analysis of four iteration-1 artifacts. It makes **no LLM calls and no API calls, and it needs no API keys**. Everything below comes from `README.md`, `eval.py`, `src/`, `audit/`, `pyproject.toml`, `requirements.txt` and `logs/full_run.out`.

## 1. Get the artifact
Clone the public repository that contains this folder, then `cd` into the folder `gen_art_evaluation_1` (the exact repository URL was not recorded in the workspace).

## 2. Environment
- Ubuntu (Linux 6.8 kernel). No system packages beyond Python and `uv` are recorded.
- Python 3.12 (`pyproject.toml`: `requires-python = ">=3.12"`; the README uses `--python=3.12`).
- Create the venv and install the pins with `uv`, as the README says:
```bash
uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r requirements.txt
```
- Pinned versions (`requirements.txt`, identical to `pyproject.toml`): cloudpickle 3.1.2, contourpy 1.4.0, cycler 0.12.1, fonttools 4.65.0, formulaic 1.2.2, ijson 3.5.1, interface-meta 2.0.1, joblib 1.6.0, kiwisolver 1.5.1, loguru 0.7.3, matplotlib 3.11.2, narwhals 2.26.0, numpy 2.5.3, packaging 26.3, pandas 3.0.6, patsy 1.0.3, pillow 12.3.0, pyparsing 3.3.3, python-dateutil 2.9.0.post0, pyyaml 6.0.3, scikit-learn 1.9.1, scipy 1.18.1, six 1.17.0, statsmodels 0.15.0, threadpoolctl 3.7.0, typing-extensions 4.16.0, wrapt 2.4.1.

## 3. Inputs, downloads, keys
- No downloads, no models or checkpoints, no environment variables and no API keys. Recorded OpenRouter spend is 0.0 USD (`eval.py`, firewall block).
- The inputs are the iteration-1 artifacts of the same run, read read-only: `gen_art_experiment_1` (exp A, FOL-Triage), `gen_art_experiment_3` (exp C, consensus c_score), `gen_art_experiment_4` (exp D, judges/baselines) and `gen_art_dataset_1` (dataset E, screen adjudication). Their files (49 in total; list in `src/load.py`, `INPUT_FILES`) include `results/metrics.json`, `results/summary.json`, `results/analysis.json`, per-item JSONL files, `screen_adjudicated_labels.json`, `dataset_card.md` and `full_data_out.json`. Their sha256 hashes are stored in `eval_out.json -> metadata.provenance`.
- **Path caveat (not recorded as portable):** `src/load.py` line 18 hard-codes `IT1 = Path("../../../round-1")`, and `EXP_A/EXP_C/EXP_D/DS_E` are derived from it (under `gen_art/`). `audit/rederive_headlines.py` line 28 hard-codes the same `GA` path. `src/outputs.py` line 16 points `FIG_SKILL` at `../../../tools/aii-data-fig-gen/scripts`, a helper for figure rendering that is not part of this folder. A reader outside the original server must edit `IT1`/`GA` to point at the sibling folders of the published repository (the four artifacts above). The figure-skill path must be pointed at an equivalent figure helper, or figure regeneration will fail. This was not changed here, because the code was not to be modified.
- `data/panel_calibration.json` (already shipped) is the only group extracted from dataset E's `full_data_out.json`. `eval.py` re-extracts it only if the file is missing. The held-out rows of dataset E are never loaded.
- If the iteration-1 artifacts are unavailable, the shipped `eval_out.json`, `tables/`, `figures/` and `audit/*.json` remain as recorded outputs.

## 4. Commands
```bash
.venv/bin/python eval.py            # full run; steps 0-13, writes everything below
.venv/bin/python eval.py --quick    # smoke test: B=200 bootstrap, 1 fold seed
.venv/bin/python audit/rederive_headlines.py   # independent re-derivation -> audit/rederive_headlines.json
.venv/bin/python audit/placebo_permutations.py # 20 label permutations -> audit/placebo_permutations.json
```
(The audit scripts' exact invocation was not logged; the two commands above follow the files' names and are assumed to be run from the workspace root. `placebo_permutations.py` sets `sys.argv = ["x"]` internally.)

- Seeds and config (from `eval.py`/README): the bootstrap is a sentence-cluster bootstrap with 2000 resamples, seed 0, 95% percentile CIs (`B=200` with `--quick`). The PT preview uses 5 fold seeds (1 with `--quick`) and exp D's own folds. The Kendall tau bootstrap uses 500 resamples (100 with `--quick`). `audit/rederive_headlines.py` uses `boot_delta(..., B=2000, seed=11)` and `pt_oof(..., seed=0)`. The placebo uses 20 permutations.
- Hardware and runtime: CPU only, no GPU. The README says about 1-3 min on 4 CPUs; the `eval.py` docstring says 10-20 min. The one recorded run (`logs/full_run.out`) reports `DONE in 139s`. The CPU model and RAM were not recorded.
- Run order in `eval.py`: step 0 (hash inputs), 1 (bookkeeping), 2 (re-derivation gate, aborts if it fails), 3 (regimes, written to `regimes.json`), 6 (PT preview), 4 (common-item tables), 5 (regime shift, tau, flipped items), 7 (P1/P2), then `src/steps_audit.py` (8-13) and `src/outputs.py` (writes `eval_out.json`, figures, VERDICT).

## 5. Outputs and expected numbers
Outputs: `eval_out.json` (exp_eval_sol_out, 5,930 `metrics_agg` keys, 1,380 examples; `full_/mini_/preview_` variants), `regimes.json`, `tables/*.csv` (first line `# source:`), `figures/fig_regime_shift.*` and `figures/fig_forest_common.*` (json/png/pdf), `audit/*.json`, `logs/`. Paper locations were not recorded; the numbers appear in the README headline sections. Values below are from `logs/full_run.out` and the README:
- Step 2 gate: 57/57 MATCH (`tables/rederivation.csv`). n=389, 160 errors, 151 sentences; c_score 0.8416, fused 0.767, judge 0.785; tier A+B n=304: fused .872, L2-bow .817, c_score .776, judge .771.
- Master frame: 1,380 rows (L 1037, H 343). Step 1: 588 common L ids, 398 consistent.
- Regimes (n / errors): R_SOLVER_CONS 373/155, R_ADJ_AB 298/165, R_ADJ_ALL 498/271, L_UNPARSEABLE_AS_ERROR 413/195. R_ADJ_A (75/36) and the H_* regimes (H_SOLVER 150/17, H_ADJ_AB 51/46, H_CURATOR 166/33) are untestable, so sign-only.
- PT − judge_cheap_disg: +0.089 (solver-consistent), +0.104 (A+B), +0.090 (all tiers), +0.118 (unparseable as error).
- Iteration-1 rule: fused_H and c_score fail in every regime. fused_H − judge is −0.013 under solver labels and +0.096 [0.020, 0.171] under A+B.
- Label-only shift, solver to A+B: bow +0.102, fused +0.080, c_score −0.106. Kendall tau 0.60.
- Step 8 MUST-FIX rows: 1507 (790 MATCH, 627 TRANSCRIBED_ONLY, 60 RECOMPUTED_ONLY, 30 MISMATCH).
- Audit: PT − judge re-derived +0.086 (solver) and +0.103 (A+B). Placebo null maxima are 0.047 (solver) and 0.087 (A+B); all 20 null deltas fall below the observed ones.
- Small differences can arise from the fold assignment (audit uses sklearn `GroupKFold`) and are expected there, not in `eval.py`.
