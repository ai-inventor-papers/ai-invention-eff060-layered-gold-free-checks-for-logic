# Reproducibility: R_COMP FREE confirmation (iteration 5, gen_art_experiment_13)

This file describes what was ACTUALLY run on 2026-09-24, between 11:06 and 11:50 UTC.

## 1. Copy the folder

```bash
cp -r . ~/rcomp_confirm && cd ~/rcomp_confirm
```

Read-only absolute inputs, under `../../../`:

| input | path |
|---|---|
| exp 7: scores (whitelist loader), judges, generations, sentences, NLTK data | `round-3/experiment-7/src/...` |
| eval 3: matrix records | `round-4/evaluation-3/src/pairwise_classes_RCOMP.jsonl` |
| eval 2: `consensus_mx.py`, `mechanism.py`, `stats.py`, imported unchanged | `round-3/evaluation-2/src/src/` |
| dataset 3: lexicon | `round-2/dataset-3/src/lexicon.json` |

These paths must exist, or the constants in `confirm/cc.py` and `labeller/src/common.py` must be edited.

## 2. Environment

**Machine:**
- Ubuntu (Linux 6.8);
- 8 CPUs;
- no GPU used;
- Python 3.12.14;
- `uv` only (no pip).

**Install:**

```bash
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r pyproject.toml   # 48 pinned packages, e.g.:
# z3-solver==5.1.0.0, numpy==2.5.3, pandas==3.0.6, scikit-learn==1.9.1, statsmodels==0.15.0, httpx==0.28.1, loguru==0.7.3, nltk==3.10.3
```

**Environment variables (names only):**
- `OPENROUTER_BASE_URL` and `OPENROUTER_API_KEY`: needed only for the paid steps.

**Downloads:** none. The model catalogue snapshot was saved to `results/models_snapshot_iter5.json`.

## 3. Commands, in the order they ran

Seeds:
- bootstrap seed 20260924 (B = 2000);
- sentence folds `sha1('rcomp_folds_v1|'+sid) % 5`;
- audit and frontier samples `random.Random(20260924)`;
- placebo permutations `numpy default_rng(20260924)`.

| # | command | cost | time |
|---|---|---|---|
| 1 | copy `labeller/` from dataset 5; rename `results/gate_report.json` → `gate_report_D9_notrun.json` (D10); set `HARD_STOP_USD = 3.6` in `labeller/src/gloss.py` (D11) | $0 | – |
| 2 | `cd labeller && ../.venv/bin/python -m pytest -q` | $0 | 10 s |
| 3 | R0: `src/assemble_labels.py --mode search_only` in a scratch copy → hash 9609ebbb… (match) | $0 | 2 s |
| 4 | `cd confirm && ../.venv/bin/python g0_repro.py` (SIG: 0.9543 / 0.5872, n 1,904, exact) | $0 | 5 s |
| 5 | `judge_orig_complete.py --regress-only`, then `--limit 10`, then full (1,289 rows) | $0.062 | 1 min |
| 6 | `scores.py` (score seal), `prereg.py`, `git commit` at 11:18:46Z | $0 | 1 s |
| 7 | `gloss_pilot.py` (projection $1.87 ≤ $3.24) | $0.003 | 5 s |
| 8 | `cd labeller && ../.venv/bin/python src/resume_gloss.py gate` → gloss_v1 half A FAIL | $0.067 | 40 s |
| 9 | write `prompts/gloss_v2.json`, `git commit`, `src/gate.py run --half B --version gloss_v2` → FAIL | $0.173 | 1 min |
| 10 | `confirm/gate_diagnostics.py`; `labeller/src/resume_gloss.py finalize --version gloss_v2` (FALLBACK B seal b7916aea…) | $0 | 3 s |
| 11 | commit `prereg_addendum_fallbackB.json` | $0 | – |
| 12 | `audit_blind.py --pilot 3`, then full (Sonnet-5 reasoning off, D19), then `--retry-missing` (refused, D25) | ~$1.0 | 13 min |
| 13 | `frontier_judge.py` (5-row pilot, then 145 rows) | $0.715 | 1 min |
| 14 | `join_and_test.py --quick` (debug, D21), then `join_and_test.py` (B = 2000) twice (D26: V4 + placebo supplement added) | $0 | 2 min |
| 15 | `report.py`, `write_deviations.py`, `../tests/rederive_confirm.py`, `final_checks.py`, `../tests/rederive_raw.py` | $0 | 2 min |
| 16 | aii-json validate + mini/preview of `method_out.json` | $0 | – |

**Re-running:**
- `uv run method.py` repeats steps 14–15.
- `--steps` selects others. Paid steps reuse caches (`labeller/results/gloss_cache.jsonl`, appended jsonl files) and do not
  re-bill finished rows.

## 4. Expected outputs and numbers

**Seals:**
- labels (all rows): b7916aeae77ecfe2556e0f545bb5813843a36d12ba73043dfc1320c13c45cd5e;
- labels (untouched rows): 79eb623a1a75279c1db96c8d31311b59e16bcc7b911064f04c9909fb4d6afcbb;
- scores: `results/score_seal_rcomp.json`.

**Main results:**
- `results/confirm_verdict_rcomp.json`: VERDICT NOT_TESTABLE (0 CORRECT).
- `results/tables.md` / `analysis_rcomp.json`: PROVISIONAL deltas +0.217 [0.175, 0.260] (disguised) and +0.171 [0.135, 0.206]
  (original).
- Audit-labelled view: +0.377 (disguised).
- Frontier: −0.051 [−0.153, 0.044].
- `results/gate_diagnostics.json`: the gate table.

**Where these go in the paper:** the R_COMP FREE confirmation section. Report it as "not testable: the label gate failed", and
the provisional numbers only as non-confirmatory evidence, always marked as templated text.
