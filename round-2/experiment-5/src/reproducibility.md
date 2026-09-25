# Reproducibility: PEER+TEXT held-out test on dataset E

Everything below comes from the files in this folder (README.md, method.py, pyproject.toml, restore.sh, src/, tests/,
logs/, results/). Nothing was re-run when writing this file. Where the workspace does not record a point, it says so.

## 1. Get the artifact

```bash
git clone <URL of the public repository that holds this folder>   # the URL is not recorded in the workspace
cd <repository>/<folder of this artifact>                          # the run's id for this folder: gen_art_experiment_5 (iteration 2)
```

All paths below are relative to this folder.

**Inputs from other artifacts and known portability gaps.**
- Dataset E comes from the iteration-1 artifact `gen_art_dataset_1`, a sibling folder in the repository. Its blind and label
  views are already copied here: `data/E_blind.jsonl` (sha256 in `data/E_blind.sha256`) and `data/E_labels.jsonl`. The
  screen inputs from iteration 1 are copied under `data/screen/`, and the exp A/D prereg files are `data/expA_prereg.json`
  and `data/expD_prereg.json`.
- These are the only inputs needed to score and analyse. Several source files still contain absolute paths of the original
  server: `src/data_views.py:24` (`E_DIR`, points at `gen_art_dataset_1`), `src/screen_fit.py:534` (reads the dataset card),
  `src/vendor_d/common.py:17` (`SRC_DATA`), `src/vendor_c/peers.py:34` and `src/vendor_c/repair_census.py:34` (MALLS and other
  iteration-3 data), and `src/key_monitor.sh:6` (a private key file).
- These paths are only used by the `views` stage (rebuilding `data/E_*.jsonl` from the dataset artifact) and by the screen
  stage (`screen_fit.py`, the one-time freeze). Neither is needed to reproduce the reported numbers, because the frozen
  `results/prereg.json` and the copied views are shipped. To rerun `views` or `screen` from scratch, point those constants at
  the sibling folder `../gen_art_dataset_1` (and at your own copy of the MALLS/FOLIO source data used by the vendored
  iteration-1 code).
- The shared OpenRouter key and the key file are private and not published.

## 2. System, Python and libraries

- Ubuntu (the run was on Linux 6.8); `uv`, `curl`, `unzip`, `git`.
- Python 3.12 (`requires-python >= 3.12`; `restore.sh` uses `--python=3.12`).
- Main env `.venv`: exact pins are in `pyproject.toml` (frozen with `uv pip freeze`, 2026-09-23). Key ones: z3-solver==5.1.0.0,
  numpy==2.5.3, scipy==1.18.1, scikit-learn==1.9.1, pandas==3.0.6, statsmodels==0.15.0, nltk==3.10.3, spacy==3.8.16 (+
  en_core_web_sm 3.8.0 wheel), aiohttp==3.14.3, requests==2.34.2, loguru==0.7.3, pytest==9.1.1.
- GPU env `.venv_gpu` (only for the local Qwen3-8B judge): `torch transformers accelerate loguru huggingface_hub aiohttp
  requests z3-solver`, **not pinned**; versions were not recorded.
- Setup, as run by `restore.sh`:

```bash
bash restore.sh        # creates .venv from pyproject.toml, .venv_gpu, and downloads NLTK wordnet, omw-1.4, words into data/nltk_data
export NLTK_DATA=$PWD/data/nltk_data
```

## 3. Downloads, keys, environment variables

- NLTK corpora (`wordnet`, `omw-1.4`, `words`) from `raw.githubusercontent.com/nltk/nltk_data`, fetched by `restore.sh`.
- Local judge model `Qwen/Qwen3-8B` from the Hugging Face hub (`snapshot_download('Qwen/Qwen3-8B')`; bf16, no quantisation;
  the code loads it through `src/vendor_d/local_llm.py`). Loading took 52 s and about 16.4 GB VRAM (`logs/local_judge_E.out`).
- API: `OPENROUTER_API_KEY` (name only). Used for the L3 text-only questionnaire and the pre-registered flash-lite judge
  (`google/gemini-2.5-flash-lite`). The code caps spend at $3 (`VB.CAP_TOTAL = 3.0` in `src/run_api_E.py`).
  Optional: `AII_COST_LEDGER` (cost ledger path, read in `src/vendor_d/budget.py`), `NLTK_DATA` (defaults to `data/nltk_data`).
- All LLM calls are cached (`results/llm_cache.jsonl`, `results/local_cache.jsonl`) and the L3 outputs are stored in
  `results/E_l3_q.jsonl`, so the analysis can be rerun without a key.
- **The pre-registered flash-lite judge bar could not be run.** The shared key hit its daily limit at about 18:00 UTC and the
  replacement key was also exhausted (polled 19:10 to 22:13 UTC with `src/key_monitor.sh`). Only 20 judge rows exist in
  `results/E_judge.jsonl`. A rerun with a funded key would fill this bar; the `disg`, `orig`, `l3disg`, `rest` phases of
  `src/run_api_E.py` are resumable.

## 4. Commands, in the order the pipeline runs them

`method.py` is the driver (`views`, `api`, `local`, `screen`, `score`, `analyse`, `outputs`, `all`). Each stage is resumable
and cached. The `screen` stage is skipped if `results/prereg.json` exists (it is never re-frozen).

```bash
.venv/bin/python -m pytest -c pytest.ini tests/test_peer_text.py tests/test_isolation.py   # 12 unit tests + isolation checks
.venv/bin/python method.py all
```

`method.py all` runs, in this order:
1. `.venv/bin/python src/data_views.py` (E blind view with an allowlist, label view, API row order; needs `gen_art_dataset_1`, see section 1)
2. `.venv/bin/python src/run_api_E.py` (defaults `--phases l3,disg,orig,l3disg,rest`, optional `--limit N`; needs `OPENROUTER_API_KEY`)
3. `.venv_gpu/bin/python src/local_judge_E.py` (only if `.venv_gpu` exists)
4. `src/screen_fit.py compute`, `fit`, `freeze` (only if no `results/prereg.json`; freeze wrote `results/prereg.json`, sha256 `b9f28b1b…` in `results/prereg.sha256`, git commit `a6896ce`)
5. `src/score_E.py run --stage mini`, `--stage 100`, `--stage all`, then `src/score_E.py assemble` (writes `results/per_item_E.jsonl`)
6. `src/analyse_E.py` (the only step that joins labels; refuses a missing, mismatched or newer prereg)
7. `build_outputs()` in `method.py`, which writes `method_out.json` (the `full_`, `mini_` and `preview_` variants are also in the folder)

Extra steps that the logs and README show were run separately: `src/posthoc_nf_fusion.py` (labelled post-hoc NF fusion,
`results/posthoc_nf_fusion.json`), `src/write_deviations.py` (`results/deviations.json`), and the audits:

```bash
.venv/bin/python tests/audit_rederive.py       # re-derives pooled AUROCs and the headline delta, asserts a match to 1e-9
.venv/bin/python tests/placebo_headline.py     # shuffled-label placebo -> results/placebo_headline.json
.venv/bin/python tests/prefilter_audit.py      # finite-model refuter vs z3, 500 screen pairs -> results/prefilter_audit.json
.venv/bin/python tests/judge_cache_regression.py   # 30 screen items hit exp D's judge cache (30/30)
```

The arguments of the last three audits and the post-hoc script are not passed on a command line in the code shown; they take
no arguments as far as the scripts show. The exact invocation used for `posthoc_nf_fusion.py` was not recorded beyond its log
`logs/posthoc.out`.

**Seeds and configs (from the code).**
- Bootstrap: sentence-cluster, B=2000, seed 20260923 (`results/prereg.json`; `SEED` in `src/analyse_E.py`, `default_rng`).
- `src/screen_fit.py`: `np.random.default_rng(20260923)`; `random.Random(0)` for the `--mini` subsample.
- `src/pool_scoring.py`: `PYTHONHASHSEED=0`; k=6 peer subsamples use `random.Random(f"k6|{sentence_id}|{key}|{sd}")` with `k6_seeds=5`.
- `src/peer_text.py`: finite-model refuter uses seeds derived by `_seed(...)` from the predicate name, arity, domain size and model index (64 random interpretations, domains 1 to 3).
- z3 timeout 2000 ms per entailment, pair cap 30 s, medoid repair budget 2 s at the freeze (0 in the screen compute).
- Folds: `fold_E = sha1('E_folds_v1|' + sentence_id) % 5`.
- Local judge: Qwen3-8B, greedy decoding.

**Hardware and runtime.**
- CPU scoring of E (`logs/score_E_all.out`): 600 sentences in 928 s wall (the earlier 100-sentence stage covered the rest of the 700
  sentences). Mean cpu-s per sentence by stratum: CTRL 6.1, EXC 9.9, L20 16.6, L25 25.1. Screen compute: 41 s.
  The CPU model and core count were not recorded.
- Local judge: about 0.13 to 0.15 s per item, roughly 16.4 GB VRAM. The GPU model was not recorded (`nvidia-smi` is not
  available in the current shell, and no log names the card). It hit one OOM and dropped to batch size 24.
- The whole scoring was run 2026-09-23, the freeze at 18:23:50 UTC. Total OpenRouter spend: $0.155.

## 5. Expected outputs and numbers

| file | contents |
|---|---|
| `results/per_item_E.jsonl` | one line per E row (8,507), `row_key = item_id\|prompt_variant`, every score, join input for iteration 3 |
| `results/analysis.json`, `results/tables.md` | all AUROC tables, CIs, sensitivities |
| `results/p_tests.json` | P1 to P4 verdicts |
| `results/deviations.json` | deviations D1 to D11 |
| `results/audit_rederive.json`, `placebo_headline.json`, `prefilter_audit.json`, `judge_cache_regression.json` | audits |
| `method_out.json` | exp_gen_sol_out format, `predict_*` for each metric (higher = more likely an error) |

Headline numbers (dataset E, label regime R_AB: tiers A+B, 2,686 rows = 1,822 ERROR + 864 CORRECT, 700 sentences; 95%
sentence-cluster bootstrap CIs):
- PEER+TEXT pooled AUROC 0.790 [0.75, 0.82]; stratified 0.753; long pool 0.768; tier A L20+EXC 0.818.
- c_score_align 0.782 (stratified 0.741; tier A 0.860); NF-anchored c_score 0.743; TEXT alone 0.693; local Qwen3-8B disguised judge 0.712.
- Delta PEER+TEXT minus local judge: +0.078 [0.043, 0.112] pooled; +0.115 [0.075, 0.157] long pool; +0.075 stratified.
  CTRL stratum: -0.031, not significant.
- Fusion vs c_score_align alone, stratified: +0.011 [-0.012, 0.038], not significant.
- P1 inconclusive, P2 refuted, P3 inconclusive, P4 refuted (fused RENAME false alarm 0.385).
- Unit-code typing 0.37 vs 0.38 chance. Post-hoc NF fusion 0.759 pooled.
- Placebo: `results/placebo_headline.json` gives real delta 0.0783, shuffled-label mean delta 0.0037.
- Flash-lite pre-registered bar: untestable (20 rows).
- Coverage: 1,086 UNPARSEABLE rows are counted in every metric (scored 1.0).

A reader who reruns `method.py analyse` and `tests/audit_rederive.py` from the shipped `results/per_item_E.jsonl` and
`results/prereg.json` should reproduce these figures. Reruns of scoring itself should match up to z3 timeout effects (UNKNOWN on
2.3% of rows had at least one timed-out unit). The local judge outputs and L3 questionnaires are cached in `results/`, so
those LLM-dependent parts are reproduced from cache, not regenerated.

**Where in the paper.** The workspace does not contain the paper or its section and table numbering, so the mapping to paper
tables was not recorded. `results/tables.md` holds the tables in the order the analysis produced them.
