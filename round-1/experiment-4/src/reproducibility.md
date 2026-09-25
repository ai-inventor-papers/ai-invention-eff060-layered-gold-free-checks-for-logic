# Reproducibility: Experiment D (disguised cheap judge + baselines on the NL→FOL screen)

Derived from `README.md`, `method.py`, `restore.sh`, `requirements.txt`, `prereg*.json` and `logs/`.
Paths are relative to this directory.

## 1. Environment
- Python 3.12, uv only (no pip). GPU used for local judges: RTX 4000 Ada (CPU-only works for API stages).
- Restore everything deleted from the workspace: `bash restore.sh all`
  (or `venv | nltk | pilot | models`). It creates `.venv`, installs pinned `requirements.txt`
  (z3-solver 5.1.0.0, torch 2.14.0, transformers 5.17.0, spacy 3.8.16 + en_core_web_sm 3.8.0, ...),
  downloads NLTK words/wordnet/omw-1.4 into `data/nltk_data`, unpacks the pilot study
  (`user_uploads/dpv_pilot_study.zip` -> `pilot_ref/`), and fetches model weights into the shared `HF_HOME` cache:
  Qwen3-8B, Llama-3.1-8B-Instruct, Qwen3-14B, DeBERTa-v3-large NLI (MoritzLaurer), cross-encoder/nli-deberta-v3-large, all-mpnet-base-v2.
- Environment variables: `PYTHONHASHSEED=0` (mandatory: the labeller fingerprint uses `hash()`),
  `NLTK_DATA=data/nltk_data`, `OPENROUTER_API_KEY` (API stages only; never store or print it),
  optional `AII_COST_LEDGER`. `HF_HOME` is the run's shared cache.

## 2. Inputs
- `data/screen_items.json` (1,090 items: track L 796, track H 294), `data/label_vector.sha1`, `data/folds.json`,
  `data/invariance_items.json`, `data/iter3_repair_census.rows.json`, `data/logiclm/`, dataset from `../../dataset-1/src`.
- Labels are shared with experiments A, B, C via `item_id`; verify with `data/label_vector.sha1`.

## 3. Running
`PYTHONHASHSEED=0 NLTK_DATA=data/nltk_data .venv/bin/python method.py --stage NAME [--limit N] [--variant api|local]`

Stage order: `labeller` -> `screen` -> `prep` -> `promptdev` -> `prereg` -> `judges` -> `strong` -> `roundtrip` -> `pilot` -> `recall` -> `analysis`.
Local-model stage names: `promptdev_local`, `llm_local`, `rt_llm_local`. Stages persist outputs and are resumable.
`--stage analysis` (default) rebuilds all tables and `method_out.json` / `full_method_out.json` / `mini_` / `preview_` from cached scores
in `results/scores/*.jsonl`, `results/llm_cache.jsonl`, `results/local_cache.jsonl`, so the headline numbers reproduce with no API spend.
Non-GPU stages run under a 40 GB RLIMIT_AS.

## 4. Models and settings
- API judges (OpenRouter, T=0): `judge_cheap` = gemini-2.5-flash-lite, rubric A; `judge_cheap2` = gpt-4.1-nano (P(YES));
  `judge_strong` = gemini-3.1-pro-preview on the pre-registered 200 L + 96 H subset (same subsample as `prereg_local.json`).
- Local judges: Qwen3-8B (JSON), Llama-3.1-8B (P(YES)), Qwen3-14B nf4; local verbaliser Qwen3-8B.
- Pre-registration: `prereg_local.json` (sha1 in `prereg_local.sha1`, frozen 13:49 UTC) and `prereg.json` (`prereg.sha1`, frozen 15:13 UTC),
  both frozen before scores were joined to track-L labels.
- Statistics: sentence-clustered bootstrap, 2,000 resamples; DeLong for paired AUROC; cross-fitted combination uses `data/folds.json`.
- Budget: total API spend $2.02 (cap $9.5), ledger in `results/costs.jsonl` and `.aii_cost_ledger.jsonl`.

## 5. Expected outputs and check
- `results/analysis.json` (all numbers), `results/summary.md`, `method_out.json` (exp_gen_sol_out schema), `results/judge_label_disagreements.csv`.
- Headline numbers: judge_cheap_disg AUROC 0.777 [0.720, 0.827]; judge_strong_orig 0.802; rt_nli_min 0.710; pilot_rerun_jacc 0.720; OOF combination 0.817.
- Independent check: `.venv/bin/python tests/audit_headlines.py` -> `results/audit_headlines.json`; unit tests `tests/test_labeller.py`.

## 6. Known non-determinism / caveats
- LLM outputs vary across providers/model revisions; use the caches for exact reproduction. gemini-3-pro-preview is no longer listed.
- The labeller uses a deterministic candidate budget (60k), not wall-clock (`src/labeller/labeller.py:search_det`).
- Budget guard reservation bug (fixed in `src/budget.py`) and a `budget_state.json` race were reconciled from `costs.jsonl`.
- 11 judge JSON failures are flagged (not dropped); dropping them gives 0.785 instead of 0.777.

## 7. Not recorded in the workspace
Exact wall-clock per stage beyond `logs/stage_*.log`, the container image, and the exact OpenRouter model revision hashes were not recorded.
