# Reproducibility: held-out NL→FOL faithfulness meta-evaluation set

This folder (`gen_art_dataset_1`) is a dataset artifact. Its result is `full_data_out.json`. It was built by an LLM-calling pipeline (OpenRouter) plus a local z3-based solver labeller. The build is **not bit-for-bit reproducible from scratch**: the LLM outputs are stored API responses, and the panel and generator calls are non-deterministic across providers. The stored raw outputs in `raw/` and `work/` are what make the dataset rebuildable. Everything below is taken from the files in this folder; where the files are silent, that is stated.

## 1. Get the artifact
```bash
git clone <URL of the public repository that publishes this workspace>   # URL not recorded in the workspace
cd <repo>/<folder containing this file>                                   # the gen_art_dataset_1 folder
```
All paths below are relative to this folder. Scripts anchor on `Path(__file__)`. `README.md` and `dataset_card.md` still quote the original absolute workspace path as documentation only; no code uses it.

## 2. System, Python, environment
- Ubuntu (built on Linux 6.8). No system packages beyond a Python 3.12 toolchain and `uv` are recorded as needed. The `bash` steps and `curl` (only in `src/key_monitor.sh`) are standard.
- Python `>=3.12` (`pyproject.toml`); the README uses `--python=3.12`.
- Pinned libraries in `pyproject.toml` (`uv.lock` is also included), including: aiohttp==3.14.3, huggingface-hub==1.32.0, loguru==0.7.3, nltk==3.10.3, numpy==2.5.3, pandas==3.0.6, pyarrow==25.0.1, pytest==9.1.1, scipy==1.18.1, z3-solver==5.1.0.0, requests==2.34.2, httpx==0.28.1, pyyaml==6.0.3, regex==2026.9.10 (plus the transitive pins).
```bash
uv venv .venv --python=3.12
uv pip install --python=.venv/bin/python -r pyproject.toml
```
- NLTK data (WordNet is used by the nonce disguise, `labeller/disguise.py`, and by `src/calibration.py`), downloaded into `nltk_data/`:
```bash
.venv/bin/python -c "import nltk; [nltk.download(p, download_dir='nltk_data') for p in ('wordnet','omw-1.4')]"
```

## 3. Data, models, credentials
- Environment variables (names only): `OPENROUTER_API_KEY` (required for any LLM step; `src/or_client.py`), `AII_HARD_CAP` (cumulative spend stop in USD, default 9.50), and optionally `AII_COST_LEDGER`. The key was a shared OpenRouter key; never put its value in a file.
- Bundled, read-only sources in `data_local/` (already in this folder): MALLS-v0.1 train/test JSON, `yfxiao__folio-refined__train.csv`, `folio_refined_validation.csv`, the DSAVlab-UNIUD curated FOLIO and MALLS jsonl files, and ProverQA dev_hard.
- `raw/logiclm/` (Logic-LM FOLIO dev outputs for gpt-3.5-turbo, gpt-4, text-davinci-003) is bundled.
- `raw/hf/` is NOT in the folder (removed as regenerable). Restore it with this command from `README.md`:
```bash
.venv/bin/python -c "from huggingface_hub import hf_hub_download as d; [d('tasksource/folio', f, repo_type='dataset', local_dir='raw/hf/tasksource__folio') for f in ('folio_v2_train.jsonl','folio_v2_validation.jsonl')]; [d('kenken6696/folio_by_ccg2lambda', f, repo_type='dataset', local_dir='raw/hf/kenken6696__folio_by_ccg2lambda') for f in ('data/train-00000-of-00001.parquet','data/valid-00000-of-00001.parquet')]"
```
- `temp/datasets/` is a set of relative symlinks used by `data.py`: `local_sources -> ../../data_local`, `generated_candidates -> ../../raw`, `logiclm_FOLIO_dev_outputs -> ../../raw/logiclm`, `tasksource__folio` and `kenken6696__folio_by_ccg2lambda -> ../../raw/hf/...`. It is not among the published files listed, so recreate it if missing (`mkdir -p temp/datasets` and `ln -s` these targets).
- Generator models (`work/generation_manifest.json`, via OpenRouter, temperature 0, `max_tokens` 600 unless noted): G1 meta-llama/llama-3.1-8b-instruct, G1b meta-llama/llama-3.3-70b-instruct, G2 qwen/qwen3-235b-a22b-2507, G3 mistralai/mistral-small-3.2-24b-instruct, G4 deepseek/deepseek-v3.2, G5 google/gemma-3-27b-it, G6 microsoft/phi-4, G7 openai/gpt-4.1-mini, G8 google/gemini-2.5-flash, G9 cohere/command-r7b-12-2024, F openai/gpt-5.1 (200 sentences). Prompts: `prompts/fewshot_v1.txt`, `prompts/zeroshot_v1.txt`; few-shot exemplars: `work/fewshot_exemplars.json`. The full provider/model snapshot is `work/models_snapshot.json`.
- Panel models (`src/panel.py`, temperature 0, `max_tokens` 1500): P1 anthropic/claude-haiku-4.5, P3 z-ai/glm-4.6, R1 moonshotai/kimi-k2-0905. Also defined but not used in the final panel: P2 x-ai/grok-4.3, P1alt anthropic/claude-sonnet-4.6, R2 minimax/minimax-01.
- Non-LLM system: ccg2lambda candidates (from the kenken6696/folio_by_ccg2lambda train split), and the MALLS GPT-4 gold treated as a system.

## 4. Commands (in the order they were run; from `README.md` and `src/resume_panel.sh`)
Seeds: there is no global random seed. Generation and the panel use temperature 0. Panel item order is shuffled with a seed from `sha1(sentence_id)` (`src/panel.py`); the disguise nonces and the calibration items are also seeded by `sha1(sentence_id)`. `labeller/repair_census.py` uses `SEEDS = list(range(24))` for its model-evaluation equivalence test. The 6 few-shot exemplars were hand-picked (card §10).
```bash
.venv/bin/python -m pytest -q -c pytest.ini tests/test_fol.py                    # parser regression tests
.venv/bin/python src/select_sentences.py                                         # step 1: 600 screen-disjoint sentences
.venv/bin/python src/generate.py --limit 12 && .venv/bin/python src/generate.py --cap 3.5
.venv/bin/python src/ccg2lambda_candidates.py && .venv/bin/python src/screen.py
.venv/bin/python src/run_label.py --kind heldout --budget 8 && .venv/bin/python src/run_label.py --kind screen --budget 8
.venv/bin/python src/calibration.py && .venv/bin/python src/gate.py --mode synthetic --members P1,P2,P3,R1 --cap 0.45
bash src/resume_panel.sh
```
`src/resume_panel.sh` runs, in order: `gate.py --mode trackh`, `select_topup.py` (the 100-sentence L25 top-up), the top-up generation calls, `extend_labels.py`, `run_label.py`, `screen_scope.py`, `panel_run.py` (screen; pilot with 3 raters; stage 1 with GLM and Kimi; `--adjudicate P1` for Haiku on disagreements), `repair_refs.py`, relabelling with `work/reference_overrides.json`, and finally `assemble.py && stats.py && card.py && data.py`. The `--cap` values are USD budgets per step.

To rebuild only the final files from the stored labelled data (no API key needed): with `work/assembled.json` and the restored `raw/hf/` present, run `uv run data.py` (or `.venv/bin/python data.py`). It writes `full_data_out.json`, `mini_data_out.json` and `preview_data_out.json`, and re-verifies every row against the source datasets. Note that `data.py` reads `work/assembled.json`, which `src/assemble.py` produces.

Hardware and runtime: not recorded. No GPU is used; the solver is z3 on CPU, and the LLMs are remote. Total OpenRouter spend was $9.833 (`cost_ledger.jsonl`, `README.md`).

## 5. Expected outputs and numbers
Values below are from `README.md`, `logs/stats.out`, `work/source_verification.json` and `work/label_report.json`. A rerun of the LLM steps will not exactly reproduce them, because the API responses differ; re-deriving from the stored `raw/` and `work/` files should.
- `full_data_out.json` (27.7 MB): groups `heldout_candidates` 8,507 rows, `heldout_sentences` 700, `panel_calibration` 173, `screen_audit` 1,173. `data.py` marks `metadata_source_verified` true for all 10,553 held-out and calibration rows (8,507 + 700 + 173 + 1,173 rows are all verified; `work/source_verification.json` shows 0 unverified).
- Held-out final labels: UNPARSEABLE 1,086, CORRECT 1,750, ERROR 5,005, UNRESOLVED 276, CONTESTED 390. Label tiers: A 1,044, B 2,157, C 3,891, none 276, `-` 1,086, A_unaudited_ref 53.
- Testable primary pool (tiers A+B, CONTESTED and `reading_choice` excluded): L25 176 CORRECT / 697 ERROR; L20 229/592; EXC 222/384; CTRL 237/149 (`README.md` table).
- Reference statuses (`heldout_sentences`): GOLD_PANEL_OK 95, PANEL_REPAIRED 145, NO_TRUSTED_REFERENCE 295, TRUSTED_AGREED 36, DISPUTED 112, plus 15 UNAUDITED_MALLS_GPT4_GOLD and 2 UNAUDITED_AGREED_FOLIO.
- Panel: majority accuracy on 75 unambiguous expert-corrected real-error pairs 0.727; accepts 0.613 of expert-corrected formulas; Cohen κ (GLM vs Kimi) 0.5133; pilot Fleiss κ 0.5391; solver-vs-panel error precision 0.7879, recall 0.8363.
- Related files: `screen_adjudicated_labels.json`, `prereg_strata.json`, `dataset_card.md` (all statistics), `work/label_report.json` (machine-readable), `cost_ledger.jsonl`.
- Where they appear in the paper: the paper text is not part of this workspace, so the mapping to paper sections or tables is not recorded. The dataset card sections referenced by the README are §0, §7 and §10.

## 6. Not recorded
Hardware, wall-clock runtime, the public repository URL, the exact HF download revisions, and the paper table mapping. The shared-key OpenRouter API responses cannot be regenerated identically. `src/key_monitor.sh` is a helper that polls key quota and is not needed for the build.
