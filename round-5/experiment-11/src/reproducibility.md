# Reproducing E2-A (iteration 5, gen_art_experiment_11)

This file records what was **actually run** on 2026-09-24, 11:09–15:35 UTC, in order. The run was **partial**. The run-level
OpenRouter "Test idea" budget ($12, shared by every concurrent artifact) ran out at about 11:40 UTC, after this artifact had
spent $2.05. All paid stages are cached and resumable, so a copy that keeps `e2src/raw`, `e2src/work` and `cache/` re-bills
nothing and gets identical rows.

## 1. Copy the artifact

```bash
cp -r . ~/e2a && cd ~/e2a
```

Read-only inputs are referenced by absolute path:
- dataset E (`round-1/dataset-1/src`): drift replay and E's panel votes;
- exp-5 (`iter_2/.../gen_art_experiment_5`): the V0 reproduction test only;
- the sibling markers: `iter_5/gen_art/gen_art_experiment_{12,13,14}`.

Everything else is copied inside. `inputs_manifest.json` lists 131 copied files, all byte-identical to their originals.

## 2. System, Python, libraries

**Hardware used:** Ubuntu container, 48 vCPU, 503 GB RAM, 1× NVIDIA L4 (23 GB VRAM). Python 3.12.14, uv (no pip).

**Three environments** (pins are listed in `pyproject.toml`; `e2src/pyproject.toml` has dataset 4's pins):
- `e2src/.venv`: dataset 4's frozen E protocol (z3-solver 5.1.0.0, aiohttp 3.14.3, nltk 3.10.3):
  `cd e2src && uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r pyproject.toml`
- `env` → `/root/e2a_env`: the CPU scoring env. It is exp-6's pins without torch, CUDA or transformers, plus pytest 9.1.1:
  numpy 2.5.3, scipy 1.18.1, scikit-learn 1.9.1, spacy 3.8.16 + en_core_web_sm 3.8.0, z3-solver 5.1.0.0.
- `/root/e2a_gpu/.venv`: the full exp-6 pins, including torch 2.11.0+cu128 and transformers 5.17.0. Install with
  `uv pip install -r frozen/t1/pyproject.toml --index-strategy unsafe-best-match --extra-index-url https://download.pytorch.org/whl/cu128`.

**NLTK data:** wordnet, omw-1.4, words and stopwords go into `e2src/nltk_data` and `frozen/nltk_data`. Download them to a
private directory first, then copy them in: NLTK refuses world-writable download directories.

## 3. Data, models, environment variables

- Environment variables: `OPENROUTER_API_KEY`, `OPENROUTER_BASE_URL`, `HF_HOME` (names only). Optionally `AII_HARD_CAP`
  (9.5) and `AII_PROVIDER_PIN` (read from `e2src/src_e2a/pin.json`).
- Model: `Qwen/Qwen3-8B` from the Hugging Face Hub (bf16, about 16 GB) for the local judge.
- API models:
  - generators G1–G9 (dataset-4 frozen);
  - panel: Haiku-4.5 on Amazon Bedrock, GLM-4.6 on Venice then Novita, Kimi-K2-0905 on Novita (pinned, D-PIN);
  - judges: google/gemini-2.5-flash-lite and openai/gpt-4.1-nano; L3 questionnaire: flash-lite.

## 4. Commands, in the order run

Set `T0` to 11:09 UTC.

```bash
cd e2src && .venv/bin/python -m pytest -q -c pytest.ini tests/test_fol.py            # 5 passed
.venv/bin/python src_e2/probe.py && .venv/bin/python src_e2a/pin_probe.py              # key + pinned providers OK
# prereg_iter5_E2A.json + sha256 written before any further paid call
.venv/bin/python src_e2a/activate_base.py                                               # 550 base sentences (surplus not activated)
bash src_e2a/run_drift.sh      # gate synthetic + trackh, drift_report -> PASS 0.9554 (~5 min, $0.62)
bash src_e2a/run_gen.sh        # 5,200 generations + retries (~6 min, $0.49)
.venv/bin/python src_e2a/order.py 0 && .venv/bin/python src_e2/e.py run_label.py --kind heldout --budget 8 --workers 40   # ~10 min
bash src_e2a/run_panel.sh      # prefix 110 completed; budget 403 at ~11:40 during prefix 220 (stopped)
.venv/bin/python src_e2a/build_candidates.py                                            # ../e2/candidates_E2_nolabels.jsonl
cd ..
python method.py --from l3     # label-free stages, then seals/join/analyses; equivalently, stage by stage:
#   scoring/score_consensus.py --stage l3|score|pairwise|exact   (~5 min on 30-36 workers; L3 $0.13)
#   scoring/api_judges.py --stage prep|judges                    (judges mostly refused: 403)
#   /root/e2a_gpu/.venv/bin/python scoring/local_judge.py        (L4, bs 64 -> 32 after OOM; 38 + 33 min)
#   scoring/pilot_metrics_E2.py ; scoring/assemble_scores.py      (score_seal.json 13:01 UTC)
#   e2src/src_e2/{assemble_e2,controls_e2,testability_e2,seal_e2,verify_seal}.py (15:12 UTC; panel records outside prefix 110 moved aside first)
#   analysis/analyse_E2A.py --stage join  (15:30 UTC) ; --stage analyse --prefix 110  (B = 2000, seed 0; ~2 min)
#   analysis/rename_V0.py ; analysis/union_E2B.py --once ; analysis/make_outputs.py
bash e2src/src_e2a/key_poll_resume.sh   # (background) polled the key every 15 min 11:43-15:30; never recovered
env/.venv/bin/python audit/rederive.py  # independent re-derivation + shuffled-label placebo
```

Tests:
- `pytest -c pytest.ini scoring/tests/test_guard.py`: 16 passed; run it in its own process, because the guard stays installed.
- `scoring/tests/test_{variants,v0_repro}.py`, `analysis/tests/test_stats.py` and `lib/tests/test_lib.py`: 7 passed.

Seeds: `PYTHONHASHSEED=0`. Bootstrap `numpy default_rng(0)`, B = 2000. Generators and judges at temperature 0.

## 5. What you should get

The numbers are in `tables.md` and `results/*.json`, and are summarized in `README.md`.
- `e2/E2_DRIFT_DECISION.json`: PASS. Majority agreement 0.9554 on 269 items; track-H flag rate 0.827, inside E's Wilson
  CI [0.773, 0.890].
- `results/confirm_verdict_E2A.json`: overall **NOT_TESTABLE**. The R_AB long pool has 94 rows, 76 ERROR / 18 CORRECT.
- `results/auroc_cells.json`, R_AB DT (179 rows): V0 0.916 [0.858, 0.970]; local Qwen3-8B judge (disguised view) 0.913;
  Δ +0.003 [−0.042, +0.052].
- R_AB ALL (273 rows): V0 0.890; S4_E2 stack 0.931; [S4 + V0] − S4 = −0.009 [−0.034, +0.014].
- The user's pilot metrics on ALL: joint conflict 0.500, arity 0.507, shape 0.510, dangling 0.413, 1 − rerun-Jaccard 0.713.
- `results/rename_V0.json`: RENAME_NONCE false-alarm rate 1.000 (n = 145, base 0.262); RENAME_SYN 0.944 (n = 36, base 0.361).
- `results/hmech_E2.json`: (i) 0.909 [0.842, 0.977]; (iv) CONFIRMED; (ii) NOT_READ; (iii) point +0.347, CI includes 0.
- `audit/rederive_out.json`: all headline AUROCs re-derived with sklearn from the raw files (absolute difference 0 to
  1e-16). Shuffled labels give V0 0.497 (97.5th percentile 0.578).
- Spend: $2.045 (`results/cost_E2A.json`; ledgers `e2src/cost_ledger.jsonl`, `cache/l3_cost_ledger.jsonl`,
  `cache/t1_results/costs.jsonl`).

To finish the pre-registered test once the run budget is raised:
1. `bash e2src/src_e2a/run_panel.sh` (restore `e2src/work/panel_heldout*_ALL_before_prefix_cut.jsonl` first, or let the
   cache regenerate them).
2. `scoring/api_judges.py --stage judges`.
3. `python method.py --from assemble --prefix 0`.
