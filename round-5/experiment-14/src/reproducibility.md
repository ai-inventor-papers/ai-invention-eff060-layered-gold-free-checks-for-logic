# Reproducibility

## Environment

| item | value |
|---|---|
| Python | 3.12.14 (uv venv) |
| key packages | z3-solver 5.1.0.0 (= eval-2 matrix, `z3_version` 5.1.0), numpy 2.5.3, pandas 3.0.6, scikit-learn 1.9.1, scipy 1.18.1, loguru 0.7.3, httpx, nltk |
| hardware | CPU only; 8 vCPU container (cgroup), 29 GB RAM limit; map searches used 6 spawn workers with RLIMIT_AS 3 GB each |
| hash seed | every script runs with `PYTHONHASHSEED=0` (`method.py` sets it) |
| bootstrap | sentence-cluster percentile, B = 2000, seed 20260924 (eval-2 `SentBoot` weights = exp-6 `ClusterBoot` draws for the same seed); gate G0 uses exp-6's own estimator with seed 0 |
| stability / null | seeds 20260925 (500 within-stratum resamples) / 20260926 (200 within-stratum label permutations) |
| folds | `int(sha1('E_folds_v1|' + sentence_id), 16) % 5` (asserted == `fold_E`) |
| LLM | `google/gemini-2.5-flash` via OpenRouter, temperature 0, `reasoning.max_tokens = 0` (0 reasoning tokens on every call), <= 12 symbol pairs per call |

## Commands

```bash
uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml
.venv/bin/python method.py                 # all stages; idempotent (skips steps whose outputs exist)
.venv/bin/python method.py --stage TEST    # pytest (14 tests) + audit_rederive + smoke_lib
```

Stage order (`method.py` STEPS):

1. **A**: copy_inputs → step0_gates (G0) → prereg_improve → make_row_index → score_variants (label-free, sealed) →
   fit_v4 → screen → select_rule → freeze_part_a (M1).
2. **B**: probe → prereg_gg → gg_search → gg_gates dev v1 / confirm v2 → gg_gloss → gg_score → freeze_part_b.
3. **GGB**: ggb_search → ggb_score.
4. **C**: vendor_lib.
5. **OUT**: make_outputs → make_tables.
6. **TEST**: the three test/check scripts.

The frozen writers (`prereg_improve.py`, `prereg_gg.py`, `freeze_part_a.py`) refuse to overwrite.

## Runtimes (this run, host under heavy shared load)

| step | wall time |
|---|---|
| G0 | 10 s |
| score_variants | 2 s |
| screen | 17 s |
| select_rule (500 + 200 replicates) | 35 s |
| gg_search (17,913 pairs, 6 workers) | 31 s |
| each checker gate stage | ~15 s |
| gloss sweep (415 calls, concurrency 8) | 42 s |
| gg_score | 11 s |
| ggb_search (11,202 pairs) | ~9.5 min, then 20 min on the last sentence until the wall deadline (53 pairs recorded CAPPED, D12) |
| smoke_lib | 27–40 s |

## Spend

`cost_ledger.jsonl`, $0.219 in total:

| phase | calls | $ |
|---|---|---|
| probe | 1 | 0.0000046 |
| gate_dev_v1 | 147 | 0.0266 |
| gate_confirm_v2 | 128 | 0.0294 |
| gg_sweep (first 50 + rest) | 415 | 0.1630 |

The GG_B gloss made 0 billed calls: the run-level budget was exhausted (HTTP 403, D13). All verdicts are cached in
`results/gloss_cache.jsonl`, so a re-run costs $0.

## Expected numbers (a re-run must reproduce them)

| quantity | expected value |
|---|---|
| G0 (V0 strat on R_AB) | 0.741462, Δ vs judge_cheap_disg +0.098975 [0.049345, 0.145991] |
| G1 mismatches | 24 / 8,469 |
| c_exact pooled on Z | 0.74768 |
| 3-pool plain c | 0.784520 |
| oracle d, 3-pool ALL / L25 | 0.38543 / 0.54217 |
| LONG-strat AUROC: V0 / V1 / V2 / V3 / V4 / V5 | 0.74259 / 0.73914 / 0.75014 / 0.74999 / 0.75139 / 0.74562 |
| selection | winner "NONE: V0 stands" |
| GG g3 (ALL-strat): GG vs V0 | 0.69644 vs 0.74217 |
| GG g1 flip | 0.03409 |
| GG g2 recall | 1.0 |
| G-A confirm (v2) | 0.907 |
| GG_B all-yes ALL-strat | 0.65250 |

`tests/audit_rederive.py` re-derives the decision, the best LONG Δ (to 1e-9) and the GG gate numbers with independent code.
`tests/smoke_lib.py` recomputes V0/c_exact/V1–V5 from raw candidate strings through `lib/api.py`, to 1e-9.

The gloss checker is an API model: exact verdicts can drift if the provider changes the model behind the id. The cache
freezes the verdicts used here.
