# Reproducibility: T6-E Candidate-Signature Consensus on dataset E

These are the steps that were actually run on 2026-09-24 (UTC). The machine was a Docker container on Debian 12, which runs unchanged on Ubuntu 22.04/24.04. It had 4 CPUs (AMD EPYC 9655P), a 29 GB RAM cgroup limit and **no GPU**.

## 1. Copy the artifact

```bash
cp -r /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9 ~/csc_e && cd ~/csc_e
```

Some inputs are read in place from absolute paths under `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/` (read-only, with sha256 in `inputs_manifest.json`):

- dataset E `full_data_out.json`;
- `per_item_T1.jsonl`;
- `pairwise_classes_E.jsonl`;
- `pairs_E.jsonl`;
- `E_baseline_features.jsonl`;
- `folds_E.json`;
- `s4_full_coefs.json`;
- exp 5 `prereg.json`;
- the exp 8 `data/nltk_data` directory (WordNet, used for RENAME_SYN);
- the sibling `iter_4/gen_art/gen_art_evaluation_3/results/part1.json`, which is read only after d is written.

Keep those paths, or edit `src/prep.py:INPUTS`, `src/score.py:EV2_PAIRWISE`, `src/analyse.py:RUN` and `src/csc.py` (the NLTK_DATA default).

Small inputs are also copied in `inputs/`. `data/` already holds the derived frame, so the $0 stages do not need dataset E itself.

## 2. Environment

- **System packages:** none beyond `uv` (0.x) and Python 3.12. The actual version was 3.12.14.
- **Environment:**

  ```bash
  uv venv .venv --python=3.12
  uv pip install --python .venv/bin/python -r <(python3 -c "import tomllib;print('\n'.join(tomllib.load(open('pyproject.toml','rb'))['project']['dependencies']))")
  ```

- **Pinned versions:** every package is pinned in `pyproject.toml` (also in `logs/pip_freeze.txt`). The key ones are numpy 2.5.3, pandas 3.0.6, scipy 1.18.1, scikit-learn 1.9.1, statsmodels 0.15.0, z3-solver 5.1.0.0, nltk 3.10.3, aiohttp 3.14.3 and loguru 0.7.3.
- **`PYTHONHASHSEED=0` is required.** The vendored `repair_census.fp` uses `hash()`, and `method.py` sets it for every stage.

## 3. Data, models, keys

- **Environment variables for API stages only:** `OPENROUTER_BASE_URL` and `OPENROUTER_API_KEY`. Never commit their values.
- **Peer models, via OpenRouter:** `deepseek/deepseek-v3.2` (`reasoning.enabled=false`), `microsoft/phi-4`, `openai/gpt-4.1-mini` and `qwen/qwen3-235b-a22b-2507`. All ran at temperature 0 with max_tokens 600.
- **No model downloads.** No local model is used.
- **API calls are optional for reproduction.** All 599 successful peer generations are cached in `results/llm_cache.jsonl` and are replayed by key. Re-running the API stages with this cache in place makes 0 calls for them.

## 4. Commands actually run, in order

| # | command | what it did | time | cost |
|---|---|---|---|---|
| 1 | `PYTHONHASHSEED=0 .venv/bin/python src/prep.py` | inputs sha256, prompt sha check, label sha1 check (pass), label-blind frame | ~1 min | |
| 2 | 1-token curl probe of the 4 peer models (all 200 OK) | probe | | $1.4e-5 (ledger row "probe") |
| 3 | `PYTHONHASHSEED=0 .venv/bin/python src/pilot.py` | 30-row pilot → `results/pilot.json` | ~1 min | $0.017 |
| 4 | `PYTHONHASHSEED=0 .venv/bin/python src/gen.py prereg` | `prereg_csc_E.json`, sha256 `d1f51857…` | | |
| 5 | `PYTHONHASHSEED=0 .venv/bin/python src/gen.py mini` | 1,015 calls attempted | ~2 min | $0.091 |
| 6 | `PYTHONHASHSEED=0 .venv/bin/python src/repro.py` | $0 reproduction → `results/repro_checks.json` (pass) | | |
| 7 | `PYTHONHASHSEED=0 .venv/bin/python -m pytest -q -c pytest.ini tests` | unit tests (27 pass) | | |
| 8 | inline script (recorded in the addendum) | `prereg_csc_E_addendum1.json` (+`.sha256`), `results/salvage_rows.json` | | |
| 9 | `PYTHONHASHSEED=0 .venv/bin/python src/score.py` | label-blind scoring (4 processes), sha256 → `prereg_csc_E_addendum.json` | ~1 min | |
| 10 | `PYTHONHASHSEED=0 .venv/bin/python src/analyse.py` | B = 2000, seed 0 → `results/analysis.json` | ~5 min | |
| 11 | `PYTHONHASHSEED=0 .venv/bin/python src/posthoc_contam.py` | post-hoc phi-4 leakage sensitivity | | |
| 12 | `PYTHONHASHSEED=0 .venv/bin/python src/report.py` | `tables.md`, `csc_gate_E.json`, `results/per_item_csc_E.jsonl`, `method_out.json`, `deviations.json`, `api_cost_ledger.json` | | |
| 13 | aii-json `aii_json_format_mini_preview.py --input method_out.json` | full/mini/preview variants (validated as exp_gen_sol_out) | | |
| 14 | `PYTHONHASHSEED=0 .venv/bin/python src/audit_rederive.py` then `src/audit_rederive.py extra` | independent re-derivation → `results/audit_rederive.json` | ~1 min | |

Notes on individual steps:

- **Step 5 (mini).** 506 of the 1,015 calls were refused by the platform with `HTTP 403 aii_run_budget_exhausted`. The shared phase budget was spent; see deviations D1. The `:free` tier was also exhausted (`429`). The paid sweep (`gen.py full`) was therefore never run.
- **Step 8 (salvage addendum).** It fixes the PRIMARY (354 rows), GE2 and MINI200 populations before any score exists.

One-line $0 replay of steps 6 and 9–12: `PYTHONHASHSEED=0 .venv/bin/python method.py` (stages repro, score, analyse, posthoc, report; about 7 min on 4 CPUs). Audits: `method.py audit audit_extra`. Seeds:

- bootstrap `numpy.default_rng(0)`, B = 2000;
- audit bootstrap seed 1, B = 1000, and placebo permutation seed 7;
- row selection by `sha1(tag|row_key)`;
- symbol order by `random.Random(int(sha1(text|signature),16))`.

Total API spend was **$0.1082**, from `api_cost_ledger.json` (sum of `usage.cost` per call).

## 5. Expected outputs and numbers

All numbers are DEVELOPMENT E. Everything is in `tables.md`, with the table ID and source file given for each.

**Integrity (`results/repro_checks.json`):**

| check | value | target |
|---|---|---|
| eval-2 3-pool strat AUROC | 0.7428 | 0.7427 |
| T1 c_score_align strat AUROC | 0.741 | 0.741 |
| label sha1 | `1bfcb306…` | matches |

**CSC vs baselines on PRIMARY** (354 rows, 196 ERROR / 158 CORRECT):

| metric | CSC | same free peers, exact names | T1 comparators |
|---|---|---|---|
| e (T1) | 0.459 | 0.173 | |
| d (T1) | 0.139 | 0.323 | |
| strat AUROC (T4) | 0.614 | 0.770 | c_score_align 0.774; flash-lite 0.664 |

**Other results:**

| result | value | source |
|---|---|---|
| Δ CSC − FREE exact | −0.156 [−0.290, −0.031] | T5 |
| MEANING_RENAME-type e | 0.82 vs 0.04 | T9 |
| d-vs-words GEE slope | +1.25 [+0.41, +2.09] | T3 |
| nesting over S4_full | +0.006 [−0.013, +0.025] | T7 |
| FULL free peers, exact vs ALIGN d | 0.583 vs 0.328 | T2 |
| c_score_align rename FA | 0.595 → 0.868 | T15 |
| cost per candidate (G5) | $5.25e-4 | T11 |

**Gates:** `csc_gate_E.json` is PROVISIONAL.

| gate | result |
|---|---|
| G1 | FAIL |
| G2 | FAIL on R_AB; L25 NOT_READ |
| G3-E | NOT_RUN |
| G5 | PASS |

A re-run of the $0 stages reproduces these numbers exactly: the same seeds, and z3 5.1.0.0 is deterministic at these timeouts, with 0 UNKNOWN pairs on PRIMARY. In a paper, these results belong in the section on candidate-signature consensus (negative result: anchoring), and the FULL-population rows in the mechanism section (vocabulary vs structural divergence).
