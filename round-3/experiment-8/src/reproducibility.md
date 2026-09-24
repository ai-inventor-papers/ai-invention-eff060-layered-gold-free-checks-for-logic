# Reproducing this artifact (what was actually run)

Artifact: rename-invariant cross-family consensus (PEER_HYB) and per-error-type PERTURB sensitivity (iteration 3, T3+T5).
Original workspace: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8`.

## 1. Copy the artifact

```bash
cp -r gen_art_experiment_8 ~/work/hyb && cd ~/work/hyb
```
All inputs the code reads are already copied into `data/`: the exp 5 frozen files, the screen files, dataset 3's
`perturb_rows.jsonl`, the E calibration units and the fewshot prompt. A few scripts also read read-only files by
absolute path from sibling artifacts of the same run:
* `src/prep_data.py`: dataset 3 / dataset E `full_data_out.json` and exp 6 `prereg_baselines.json`.
* `src/prep_calib.py`, `src/fit_s4_perturb.py`, `src/freeze_prereg_perturb.py`, `src/perturb_cpu.py`: exp 6 `data/E_units.json`,
  `E_baseline_features.jsonl`, `results/feature_meta.json`, `results/scores/sc5_local_samples.jsonl` and
  `results/sc_pair_cache_sc5_local_samples.jsonl`.
* `src/perturb_gpu.py`: exp D `prereg_local.json`.

Outside that run, point those paths (constants at the top of each script) at copies of the same files.

## 2. System, Python, environment

* Ubuntu (container), Python 3.12.14, `uv` for every package operation (no pip).
* GPU: **NVIDIA RTX 2000 Ada, 16 GB**, driver 580.159.04 (CUDA 13.0). 48 vCPUs, 251 GB RAM.
  (The Part A scoring ran before a machine migration on a 21 GB GPU host; Part A is CPU-only, so this does not matter.)
* Environment:
```bash
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r requirements.txt     # = `uv pip freeze` of the venv used; same pins as pyproject.toml
```
  Key pins: torch 2.14.0 (default PyPI CUDA-13 wheel), transformers 5.17.0, bitsandbytes 0.50.2, accelerate 1.15.0,
  sentence-transformers 6.1.0, z3-solver 5.1.0.0, numpy 2.5.3, scipy 1.18.1, scikit-learn 1.9.1, nltk 3.10.3,
  matplotlib 3.10.9, pytest 9.1.1, loguru 0.7.3, aiohttp 3.14.3.
* Optional speed patch (used here): transformers' import-time `rglob` took more than 10 min on the network filesystem.
  `restore.sh` writes `_aii_image_processing_files.txt` and patches `transformers/__init__.py` to read it. Results do
  not depend on the patch.
* NLTK data (WordNet, OMW-1.4, words) in `data/nltk_data/`: `NLTK_DATA` is set by the code; restore with `restore.sh`.

## 3. Downloads, environment variables, keys

* Models (HF hub, into `HF_HOME`): `Qwen/Qwen3-8B`, `meta-llama/Llama-3.1-8B-Instruct` (gated: needs `HF_TOKEN`),
  `MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli`, `cross-encoder/nli-deberta-v3-large`,
  `sentence-transformers/all-mpnet-base-v2`. Command: `scripts/download_models.sh`.
* Env vars (names only): `OPENROUTER_BASE_URL`, `OPENROUTER_API_KEY` (flash-lite judge, `peer_pool` live test),
  `HF_TOKEN`, `HF_HOME` / `HF_HUB_CACHE`, `AII_COST_LEDGER` (optional). The OpenRouter proxy rejected the default
  Python User-Agent with a 403, so the scripts send an explicit User-Agent.

## 4. Commands in the order they were run (UTC, 2026-09-24)

| step | command | notes / runtime |
|---|---|---|
| prep | `.venv/bin/python src/prep_data.py` | flattens perturb_suite; label-vector sha1 check vs exp 6 (R_AB 2941, R_A 897: match) |
| scoring | `.venv/bin/python src/run_scoring.py E --stage mini`, `--stage 100`, `--stage all`, then `src/run_scoring.py screen --stage all` | pair engine, 6 workers on the old host: E+PERTURB-E-bases 4.7 min, screen 1 min; params k=5, tau=0.5, 2000 ms z3, 30 s pair cap |
| gate | `.venv/bin/python src/gate_check.py` | c_align 99.81%, c_nf 99.91% match (pass) |
| freeze A | `.venv/bin/python src/freeze_prereg_hyb.py` | 02:59 UTC, sha256 47d10ac6... |
| Part A | `.venv/bin/python src/analyse_hyb.py` | ~2.5 min; bootstrap B=2000, seed 0 |
| calib | `.venv/bin/python src/prep_calib.py` | 864 CORRECT + 400 ERROR E rows |
| API | `python3 src/run_api_perturb.py --limit 20`, then `python3 src/run_api_perturb.py` | flash-lite, 6,666 calls, $0.351, ~4 min |
| CPU B | `.venv/bin/python src/perturb_cpu.py` | ~4 min on 46 workers |
| S4 | `.venv/bin/python src/fit_s4_perturb.py` | full-E fit |
| freeze B | `.venv/bin/python src/freeze_prereg_perturb.py` | 03:18 UTC, sha256 773d73a6... |
| GPU B | `.venv/bin/python src/perturb_gpu.py --limit 40 --which judges_disg` (pilot), then `.venv/bin/python src/perturb_gpu.py --which judges_disg,verb,nli` | nf4; Qwen judge 66 min, Llama 20 min, verbaliser 37 min, NLI 3 min |
| Part C | `.venv/bin/python src/typing_perturb.py`, then `src/typing_fallback20.py` | 7,944 searches ~15 min; 20 s fallback on 500 mutants |
| Part B | `.venv/bin/python src/analyse_perturb.py` | ~1 min |
| extras | `src/quant_shift.py`, `python3 src/sanity_checks.py`, `src/make_figures.py`, `src/write_tables.py`, `src/write_deviations_iter3.py` | seconds |
| tests | `.venv/bin/python -m pytest -c pytest.ini tests` (+ `AII_LIVE=1` once) | 31 passed, 1 live test passed when enabled (< $0.002) |
| audits | `.venv/bin/python tests/audit_rederive.py`, `.venv/bin/python tests/audit_raw.py` | all_pass; raw re-derivation matches, placebos fail |
| output | `.venv/bin/python method.py output`, then aii-json `aii_json_format_mini_preview.py --input method_out.json` | 15,770 examples, schema exp_gen_sol_out valid |

`method.py run` executes the same stages in order and skips frozen files.

## 5. Expected outputs and numbers

* `results/selection.json`: frozen_variant **null** (neither eligible). Rename FA: HYB (i) 0.050, (ii) 0.841, (iii) 0.700;
  NF 0.030, 0.686, 0.485.
* `results/analysis_hyb.json` → E R_AB stratified AUROC: c_hyb **0.738**, c_align **0.741**, c_nf **0.686**. HYB−ALIGN
  **−0.004 [−0.011, 0.004]**. Placebo ≈ 0.515.
* The over-alignment audit: discordance for new HYB agreements **0.388** vs ALIGN agreements **0.127**.
* `results/sanity_checks.json`: NF keeps 100% of endorsers under renames, HYB 74–75%, ALIGN 0–33%.
* `results/perturb_sensitivity.csv`, `tradeoff.csv`, `perturb_downup.csv`, `results/tables.md` (T1–T12),
  `results/figures/*.png`. Within-base AUROC over all E-base mutants: c_align 0.866, c_hyb 0.847, c_nf 0.785,
  p_peer_text 0.948. DOWN−UP: consensus |diff| < 0.01; local judges −0.15.
* `results/typing.csv`: peer-medoid strict accuracy **0.328** [0.277, 0.387] vs majority 0.177; oracle 0.802.
* `results/quant_shift.json`: nf4 vs bf16 judge AUROC shift −0.015 to −0.035.
* In a paper these map to the results tables on consensus selection and rename invariance (T1, T7), E discrimination
  (T2/T3), over-alignment (T4/T5), per-operator sensitivity (T8/T9, heatmap figure), polarity (T10) and typing (T12).

Randomness: all bootstraps use `numpy.random.default_rng(0)` (B=2000). Generation is greedy (T=0) for every LLM. Local
model outputs are cached in `results/local_cache.jsonl` and API outputs in `results/llm_cache.jsonl`, so re-runs are
deterministic and cost $0.
