# Reproducing R_COMP: model agreement vs LLM judges (gen_art_experiment_7)

This file records what was **actually run** (2026-09-24, 01:35–04:35 UTC), in order. All API stages are resumable,
and their responses are cached (`results/llm_cache.jsonl`, `results/local_cache.jsonl`, `rcomp/raw/*.jsonl`). A
reproduction that keeps `results/` and `rcomp/raw/` therefore re-bills nothing and gets identical numbers. A reproduction
from scratch re-calls the LLMs at temperature 0; provider-side non-determinism can then change individual outputs.

## 1. Copy the artifact

```bash
cp -r /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_7 ~/rcomp_exp7
cd ~/rcomp_exp7
```

`env.sh` hard-codes `ART_ROOT` to the original workspace path. After copying, edit `ART_ROOT` (and `NLTK_DATA`, which
derives from it) to the new location. Every script otherwise derives its paths from its own file location.

## 2. System, Python and libraries

- Ubuntu (Linux 6.8), **Python 3.12.14**, `uv` (package manager; `pip` is not used), `git`, `curl`, `unzip`.
- Hardware used: **AMD EPYC 7352 (48 threads), 251 GB RAM, one NVIDIA RTX 4000 Ada Generation (20 GB VRAM)**.
  The GPU is needed only for the local Qwen3-8B judge.
- Main env (CPU, API clients, z3, analysis). Its pins are exactly `pyproject.toml`, identical to `uv pip freeze` of the
  venv that ran; key pins are z3-solver 5.1.0.0, numpy 2.5.3, scipy 1.18.1, scikit-learn 1.9.1, statsmodels 0.15.0,
  pandas 3.0.6, nltk 3.10.3, aiohttp 3.14.3, loguru 0.7.3, spacy 3.8.16 + en_core_web_sm 3.8.0:
  ```bash
  uv venv .venv --python=3.12
  uv pip install --python .venv/bin/python -r pyproject.toml
  ln -s ../.venv rcomp/.venv          # rcomp/ (dataset 3 code) runs on the same venv
  ```
- GPU env (local judge only). Its pins are exactly `requirements_gpu.txt`: torch 2.14.0, transformers 5.17.0,
  accelerate 1.15.0, huggingface-hub 1.32.0, z3-solver 5.1.0.0, loguru 0.7.3:
  ```bash
  uv venv .venv_gpu --python=3.12
  uv pip install --python .venv_gpu/bin/python -r requirements_gpu.txt
  ```
- NLTK corpora (`wordnet`, `omw-1.4`, `words`) in `data/nltk_data/corpora/` (committed; `./restore.sh` re-downloads them).

## 3. Data, models, environment variables

- Inputs are already inside the folder: `rcomp/` is a copy of dataset 3 (`art_zcwCQgTqk6DN`), and the dataset-E panel code
  and exp-5/exp-D code are vendored in `src/vendor_e_panel/` and `src/vendor_x5/`. Their hashes and patches are in
  `results/VENDOR_SHA256.json`.
- Read-only references by absolute path (tests only): exp 5
  `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/`, used for the T3
  and T4 regressions.
- Model download (GPU judge): `Qwen/Qwen3-8B` from Hugging Face (about 16 GB). `.venv_gpu/bin/python -c "from huggingface_hub import snapshot_download; snapshot_download('Qwen/Qwen3-8B')"`.
- Environment variables (names only): `OPENROUTER_API_KEY`, `OPENROUTER_BASE_URL` (all LLM calls go through
  OpenRouter at that base URL), `HF_HOME` / `HF_HUB_CACHE` (the model cache), and optionally `HF_TOKEN`. `env.sh` sets
  `ART_ROOT`, `NLTK_DATA`, `PYTHONHASHSEED=0` and single-threaded BLAS (`OPENBLAS_NUM_THREADS=1` and so on).
- API models: 10 generator slots (`results/prereg_sig.json` → `slots`), google/gemini-2.5-flash-lite (cheap judge),
  google/gemini-3.1-pro-preview (frontier judge, reasoning effort low, max_tokens 4000), and anthropic/claude-haiku-4.5
  (fluency).

## 4. Commands, in the order they were run

Every command is run from the workspace root after `source env.sh`, unless it says `cd rcomp`. Times are wall-clock
times on the hardware above.

| # | stage | command | time / cost |
|---|---|---|---|
| 0 | tests (T0) | `(cd rcomp && .venv/bin/python -m pytest tests -q)`; `.venv/bin/python -m pytest tests/test_peer_text_x5.py tests/test_label_sig.py -q` | 1 min |
| 1 | S1 fluency (Sonnet audits NOT run, D1) | `cd rcomp; .venv/bin/python src/llm_phases.py fluency --cap 0.1` | 1 min, $0.056 |
| 2 | S1 final selection + freeze | `cd rcomp; cp work/rcomp_sentences.json work/rcomp_sentences_preliminary_iter2.json; .venv/bin/python src/select_rcomp.py final`, then the freeze one-liner that writes `work/rcomp_freeze.json` (sha256 of the sorted sentence ids) → 221 main + 93 reserve | <1 min |
| 3 | S2 pre-registration | the one-off script that writes `results/prereg_sig.json` (signature blocks from `src/sig_prompt.py`), `sha256sum results/prereg_sig.json > results/prereg_sig.sha256`, git commit `3e80c9b` | — |
| 4 | S3 SIG pilot + full | `.venv/bin/python src/gen_sig.py pilot --cap 1.5` (projection in `results/sig_pilot_projection.json`); `.venv/bin/python src/gen_sig.py full --cap 1.5` | 8 min, $0.257 |
| 5 | S4 FREE generation (F dropped: `work/generation_plan.json` F_sentences = 0) | `cd rcomp; .venv/bin/python src_e/generate.py --slots G1,G1b,G2,G3,G4,G5,G6,G7,G8,G9 --variants fewshot_v1,zeroshot_v1 --sentences work/rcomp_gen_main.json --cap 1.5 --concurrency 16`, then a retry of the zero-shot G1b/G2 failures | 8 min, $0.223 |
| 6 | S5 SIG labels (+ T6 sanity) | `.venv/bin/python src/label_sig.py label --workers 24`; `.venv/bin/python src/label_sig.py repair --workers 5` | 2 min + 3 min |
| 7 | S6 SIG testability | `.venv/bin/python src/testability.py SIG`, git commit `59ad739` (before any SIG score) | — |
| 8 | T4 judge regression | `.venv/bin/python src/run_judges.py regress` → `results/judge_regression_T4.json` (10/10 cache keys, 5/5 disguises) | $0 |
| 9 | S7a SIG consensus | `.venv/bin/python src/score_consensus.py run --cond SIG --stage all --workers 20` | 70 s |
| 10 | S7b SIG cheap judge | `.venv/bin/python src/run_judges.py cheap --cond SIG --cap 0.7` (run twice: the 2nd pass filled proxy-5xx failures) | 10 min, $0.163 |
| 11 | S7c frontier | `.venv/bin/python src/run_judges.py frontier --pilot --cap 1.0`; `.venv/bin/python src/run_judges.py frontier --n-rows 60 --cap 0.75` | 5 min, $0.714 |
| 12 | S8 FREE solver labels | `cd rcomp; RCOMP_LABEL_WORKERS=16 .venv/bin/python src/label_rcomp.py` | 25 min |
| 13 | S9 FREE cheap judge (label-blind, before the FREE declaration) | `FREE_PREJOIN=1 .venv/bin/python src/run_judges.py cheap --cond FREE --cap 0.6` (the orig pass stopped at 916 rows, D7) | $0.168 |
| 14 | S9 FREE consensus | `FREE_PREJOIN=1 .venv/bin/python src/score_consensus.py run --cond FREE --stage mini --workers 5`, then `--stage all --workers 12` | 3.5 min |
| 15 | S10.8 rename pass | `.venv/bin/python src/score_consensus.py rename --workers 16` | 1.5 min |
| 16 | S7d local judge (SIG, disg + orig) | `.venv_gpu/bin/python src/local_judge_rcomp.py --cond SIG --limit 20 --orig` (mini), then `... --cond SIG --orig --bs 12` | 31 min GPU |
| 17 | F1 key poll (panel prerequisite) | `.venv/bin/python src/key_poll.py 2.0` (7 polls, 60 min; the key stayed at $0.31, so the panel was not run: D9) | 60 min |
| 18 | local judge (FREE, disg) | `FREE_PREJOIN=1 .venv_gpu/bin/python src/local_judge_rcomp.py --cond FREE --bs 12` | 23 min GPU |
| 19 | S8 FREE labels + declaration | `.venv/bin/python src/panel_rcomp.py assemble`; `.venv/bin/python src/testability.py FREE`, git commit `6fbba53` (before the first join) | — |
| 20 | S10 + S11 | `.venv/bin/python method.py analyse --B 2000` (= `src/analyse.py --B 2000`, `tests/audit_rederive.py`, `src/write_records.py`, then build `method_out.json`) | 3 min |
| 21 | output variants | `$SKILL/../.ability_client_venv/bin/python $SKILL/scripts/aii_json_format_mini_preview.py --input method_out.json` (aii-json skill), then validate with `aii_json_validate_schema.py --format exp_gen_sol_out` | — |
| 22 | tests + independent audit | `.venv/bin/python -m pytest tests/test_consensus_rcomp.py -q` (T3, 6 passed); `.venv/bin/python tests/rederive_raw.py --B 400` | 5 min |

Seeds and configuration: bootstrap B = 2000 with seed 20260924 (sentences resampled within template); permutation
placebo seed 20260925; cross-fitted folds `sha1('RCOMP_folds_v1|'+sentence_id) % 5`; generators and judges at
temperature 0. Consensus parameters are frozen from exp 5 (`src/vendor_x5/prereg_exp5.json`: variants ALIGN and
NF-anchored, k = 5, tau 0.5, timeout 2000 ms, pair cap 30 s). The total API spend of this artifact was **$1.58**
(`cost_ledger.jsonl`), against a $9.5 cap.

## 5. What you should get

| number | value | where |
|---|---|---|
| SIG pool | 2,024 rows (429 ERROR / 1,595 CORRECT, 221 sentences); label sha256 `396aed1f…` | `results/testability_SIG.json` |
| Primary delta (within-template AUROC c_score_sig − judge_cheap_disg, n = 1,904) | 0.954 − 0.587 = **+0.367 [0.328, 0.404]**, PASS | `results/analysis.json` → SIG.primary; `results/tables.md` first table; paper: main result table |
| vs judge_cheap_orig | +0.278 [0.239, 0.319] | SIG.secondary.vs_judge_cheap_orig |
| Pooled / within-sentence delta | +0.388 / +0.369 | SIG.secondary |
| Nested [judge + c_sig] over [judge] | +0.377 [0.338, 0.416] | SIG.nested |
| Frontier subsample (n = 60) | c_sig 0.956, frontier orig 0.932, frontier disg 0.735 | SIG.frontier |
| Disguise cost (orig − disg) | cheap +0.085, local +0.175 | SIG.contamination |
| Rename FA (nonce) | c_nf / c_hyb 0.261, c_align 1.00, c_sig 1.00 | SIG.rename_invariance |
| d by reading | strong 0.965, weak 0.143; e = 0 | SIG.mechanism_sig |
| FREE (tier A, NOT_TESTABLE) | c_align − disg +0.214, c_hyb − disg +0.191 (CIs include 0) | FREE.tier_AB |
| Independent re-derivation | all 14 compared numbers match to 1e-9; placebos fail as required | `results/rederive_raw.json`, `results/audit_rederive.json` |

The paper should cite these by the file paths above; the per-row data is `results/rcomp_candidates.jsonl`
and `method_out.json` (datasets R_COMP_SIG, R_COMP_FREE).
