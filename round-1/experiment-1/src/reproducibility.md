# Reproducibility: FOL-Triage wide screen (iter-1 experiment A)

Everything below is taken from the files in this folder (README.md, pyproject.toml, method.py, src/*.py, logs/, results/, cache/).
Nothing was re-run when writing this document.

## 1. Get the artifact

This folder is one folder of a public GitHub repository. Clone the repository and `cd` into this folder
(`round-1/experiment-1/src` in the original run layout; the repository URL is not recorded in the workspace):

```bash
git clone <repository-url>
cd <repository>/<path-to>/gen_art_experiment_1
```

All paths in the code are anchored on `Path(__file__)` and are relative to this folder. No other artifact is read:
the inputs are in `data/`. `data/` was copied from the same run's earlier iteration-3 hypothesis step (`iter_3/gen_hypo`, sibling id not recorded in the workspace),
plus `data/logiclm/` (fetched from GitHub, see 3). Nothing user-uploaded is used.

## 2. System, Python, environment

* Ubuntu (run on Linux 6.8.0-101-generic). Python 3.12 (`requires-python = ">=3.12"`; README uses `--python=3.12`).
* `uv` for the venv. No apt packages are named anywhere in the workspace. `llama-cpp-python` is installed from a prebuilt CPU wheel
  (`--only-binary`), so no compiler is needed for that path.
* All versions are pinned in `pyproject.toml` (e.g. z3-solver==5.1.0.0, spacy==3.8.16, nltk==3.10.3, numpy==2.5.3, scipy==1.18.1, scikit-learn==1.9.1,
  pandas==3.0.6, aiohttp==3.14.3, llama-cpp-python==0.3.35, huggingface-hub==1.32.0, loguru==0.7.3, and the spaCy model en-core-web-sm 3.8.0 by URL).

```bash
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r pyproject.toml --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
.venv/bin/python -m spacy download en_core_web_sm      # only if the wheel URL in pyproject was not resolved
.venv/bin/python -c "import nltk; nltk.download('wordnet', download_dir='nltk_data'); nltk.download('omw-1.4', download_dir='nltk_data')"
```

(The README's original ad-hoc install listed unpinned package names; the pinned `pyproject.toml` is the record of what was installed.)
WordNet in `nltk_data/` is needed by `src/rewrites.py` (RENAME rewrites) only when the invariance set is rebuilt.

## 3. Downloads, keys, env vars

* Logic-LM outputs: `src/screen.py` reads `data/logiclm/FOLIO_dev_{gpt-3.5-turbo,gpt-4,text-davinci-003}.json` (already in this folder). If absent it
  downloads from `https://raw.githubusercontent.com/teacherpeterpan/Logic-LLM/main/outputs/logic_programs/FOLIO_dev_<system>.json`.
* Other data already present in `data/`: DSAVlab-UNIUD FOLIO/MALLS curated JSONL, `folio_refined_validation.csv`, `iter3_repair_census.rows.json`, MALLS test json.
* Env vars (names only): `OPENROUTER_API_KEY` (required only for live LLM calls; `src/llm.py` reads it), `LLM_LIVE=0` (force cache-only, no network),
  `AII_COST_LEDGER` (optional extra ledger path), `DRY=1` (small dry run into `results_dry/`). `PYTHONHASHSEED=0` is set inside the code.
* Models: primary L3 `google/gemini-2.5-flash-lite`; robustness row `qwen/qwen3-30b-a3b-instruct-2507` (both via OpenRouter, temperature 0);
  outage-fallback local `Qwen/Qwen2.5-1.5B-Instruct-GGUF` file `qwen2.5-1.5b-instruct-q4_k_m.gguf` (llama.cpp, CPU, downloaded by `huggingface_hub`).

## 4. Commands, in the order run

Seeds: bootstrap seed 0 (B=2000, sentence-clustered; seed 1 for the secondary-set bootstraps in `src/analysis.py`), fusion `seed=0`, rewrites deterministic seed 0,
`PYTHONHASHSEED=0`, llama.cpp `seed=0` (retries `#n` sample at temperature 0.3 with seed n).
Hardware: not recorded (CPU only; no GPU used; core count and RAM not recorded; `method.py` sets an RLIMIT_AS of 20 GiB).

```bash
cd src
../.venv/bin/python run_screen.py        # builds screen_items.json, href_items.json, invariance_set.json, screen_meta.json, results/premise_agreement.json (labels cached in cache/labels.jsonl; ~1.5 min in logs/run_screen.out)
../.venv/bin/python run_cpu.py           # L1/L2/z3 layers -> cache/cpu_layers.jsonl (1182 pairs, ~41 s per logs/run_cpu.out)
../.venv/bin/python run_local_llm.py $(( $(date +%s) + 7200 )) q   # OPTIONAL local-model robustness row; phases q / j / d (logs/run_llm_chain.sh used deadline 1790182372); the q phase took ~81 min on CPU
cd ..
OPENROUTER_API_KEY=... .venv/bin/python method.py   # prereg (if absent) -> calibration on H+HREF -> scoring (labels hidden) -> analysis -> method_out.json
```

Live `method.py` (stage 6) took ~184 s and cost $0.2919 total across all stages (ledger; $0.29). Also available: `src/rerun_analysis.py` (stage 7 only),
`src/make_report.py` (regenerates `results/RESULTS.md`), `src/audit_rederive.py` (independent re-derivation), `src/test_units.py`, `src/check_t0_t1.py`, `src/check_role_href.py`.

**Cheapest exact reproduction:** `cache/` (llm_cache.jsonl, cpu_layers.jsonl, labels.jsonl, profiles_extra.jsonl, cost_ledger.jsonl) holds every LLM answer, so
`LLM_LIVE=0 .venv/bin/python method.py` reproduces every number with no API key and no spend. Local-model answers are always read from the cache.
If `cache/` is missing from your clone, live re-running needs the key and will not return byte-identical LLM answers (hosted model versions may drift); the
key was shared and rate-limited in the original run (an outage 13:30 to ~15:00 UTC on 2026-09-23 forced the local fallback, see README).
`prereg.json` is already present and frozen; code hashes are in `results/code_freeze_after_fullsize_dryrun.json`.

## 5. Outputs and expected numbers

Files: `method_out.json` (exp_gen_sol_out format; also `full_/mini_/preview_method_out.json`), `results/metrics.json`, `results/per_item.jsonl`, `results/RESULTS.md`,
`results/calibration.json`, `results/ablations.json`, `results/invariance_scores.json`, `results/audit_rederive.json`, `results/not_run.json`, `prereg.json`, `results/fusion_H_noleak.pkl`.
The README's Results section holds all tables. The paper is not in this folder, so paper locations are not recorded; README section names are given instead.

Primary set (track L, ERROR vs CORRECT, n=477, 199 positives), item-level AUROC (sentence-clustered bootstrap 95% CI):
fused (`p_fused_H`) 0.759 [0.695, 0.825]; L2-bow 0.737; L3 0.756; L2-role 0.557; L1 0.508 (0.655 on track H); fused minus L2-bow +0.022 [-0.019, 0.061];
decomposed-judge L3 0.697 (paired delta -0.059 [-0.094, -0.022]); local Qwen2.5-1.5B L3 0.708; nonce-disguise 0.770 vs 0.765 original.
Labels on track L: CORRECT 278, ERROR 199, UNCERTAIN 204, UNPARSEABLE 60 (plus 12 REF_UNPARSEABLE). Parse/coverage rate 0.9203.
Gates: AUROC 0.7589 pass; coverage 0.92 pass; cost $0.0002/item pass; rewrite false-alarm fails (worst family 0.275, flip rate <= 0.0606).
Fused operating point FA 0.194 / TPR 0.568. `results/audit_rederive.json` re-derives the four headline AUROCs (0.7589, 0.7367, 0.7563, 0.5083),
with permuted-label placebos about 0.50. Bootstrap CIs, strata, invariance and ablations were not independently re-derived.
Long/heavily conditioned strata are UNTESTABLE on this screen (fewer than 50 errors or correct items per bin).
Judge, round-trip and self-consistency baselines are not part of this artifact (sibling experiments C/D; join on `item_id`).
