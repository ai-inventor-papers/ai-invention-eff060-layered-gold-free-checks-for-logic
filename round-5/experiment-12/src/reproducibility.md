> NOTE (published copy): this file names server paths this repository
> does not publish (a stage it does not ship, or another run's workspace),
> so the steps that read them will not run from a clone as written:
>   /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4

# Reproducing E2-B (gen_art_experiment_12)

This file records what was **actually run** on 2026-09-24, 11:08-14:55 UTC, in order.

E2-B is **PARTIAL**. At 11:39 UTC the run-level OpenRouter budget for the phase ($12, shared by every concurrent artifact of the
run) was exhausted, and every later paid call returned `HTTP 403 aii_run_budget_exhausted`. This artifact had spent $0.83. The
blind panel therefore completed no batch. The labels are E's final rule without panel votes: tier A against the *unaudited* MALLS
gold. Every paid stage is cached and resumable, so a reproduction that keeps `e2bsrc/raw/`, `e2bsrc/work/`, `exp5src/results/`,
`exp5src/cache/` and `scores/` re-bills nothing and reproduces every number exactly. A reproduction from scratch re-calls the
models at temperature 0, where provider-side non-determinism can change individual generations.

## 1. Copy the artifact
```bash
cp -r . ~/e2b && cd ~/e2b
```
Scripts derive paths from their own location. The following inputs are referenced by absolute path and must stay reachable
(all read-only):
- `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4` (E2; also the source of
  `e2bsrc/data_local`);
- `.../iter_1/gen_art/gen_art_dataset_1` (dataset E: its 700 sentences, calibration and few-shot items, the exclusion set);
- `.../iter_1/gen_art/gen_art_experiment_1/screen_items.json` (screen texts, exclusion);
- `.../iter_2/gen_art/gen_art_experiment_5` (stored per_item_E.jsonl, used only by the reproduction check);
- `.../iter_3/gen_art/gen_art_experiment_6/results/per_item_T1.jsonl` (used only by the T1 check).

## 2. System, Python, libraries
- Ubuntu/Debian 12 container, kernel 6.17, **Python 3.12.14**, **uv 0.6.14** (pip is not installed; `uv pip` is used everywhere).
- Hardware: **4 CPUs** (affinity-limited; `nproc` = 4), 32 GB RAM (cgroup), **no GPU**. Everything runs on CPU.
- Two virtual environments, each pinned:
  - `e2bsrc/.venv`: E2's frozen labelling pipeline. Pins are `e2bsrc/pyproject.toml` (E's pins, e.g. z3-solver 5.1.0.0,
    nltk 3.10.3, numpy 2.5.3), plus scikit-learn 1.9.1. The exact freeze is `logs/pip_freeze_e2bsrc.txt`.
  - `exp5src/.venv`: the scoring and analysis environment (exp 5's pins, incl. spaCy en_core_web_sm 3.8.0, scipy 1.18.1,
    scikit-learn 1.9.1, z3-solver 5.1.0.0). Its exact freeze = the root `pyproject.toml` = `logs/pip_freeze_exp5src.txt`.
```bash
bash restore.sh     # both venvs, NLTK wordnet/omw-1.4/words, HF sources (ProverQA, FOLIO v2 at pinned revisions), E2 data_local, parser test
```

## 3. Data, models, environment variables
- MALLS-v0.1 train/test: `e2bsrc/data_local/` (byte-identical to E's; sha256 in `e2bsrc/code_freeze.json`).
- `opendatalab/ProverQA` dev at revision `e2561beed450272690da658d21ae667570dbbafc`, and `tasksource/folio` v2 at revision
  `295b95fb4fe9be4ff3f933b73142d142cf6b2c97`. Both are needed only to re-run E2's selection reproduction.
- Environment variables (names only): `OPENROUTER_API_KEY`, `OPENROUTER_BASE_URL`. Every call goes through the base URL; the
  vendored clients' hard-coded URLs are replaced at runtime.
- Models:
  - generators G1-G9 and G1b (see `prereg_iter5_E2B.json` / `e2bsrc/prereg_E2.json`);
  - panel P1 claude-haiku-4.5, P3 glm-4.6, R1 kimi-k2-0905, pinned providers from E2-A's M2;
  - judges gemini-2.5-flash-lite, gpt-4.1-nano, deepseek-v3.2 (cost-matched), gemini-3.1-pro-preview (frontier);
  - L3 questionnaire: flash-lite.

## 4. Commands, in the order they were run
```bash
# T+0 (11:08 UTC)  setup + $0 checks
cd e2bsrc && .venv/bin/python src_e2b/code_freeze_check.py          # 78 files, 0 mismatches -> code_freeze_check_E2B.json
.venv/bin/python -m pytest -q -c pytest.ini tests/test_fol.py       # 5 passed
.venv/bin/python src_e2b/probe_e2b.py                               # 1-token probe OK; all 17 model ids served
.venv/bin/python src_e2b/select_e2b.py && cd ..                     # reproduces E2 pool sha 98cdccff...; E2-B 400 + reserve 150
python3 src/prereg_e2b.py                                           # prereg_iter5_E2B.json (sha dc4844dd...) + surplus claim, BEFORE generation
nohup python3 src/poll_markers.py &                                 # M1/M2/M3 poller (M2 PASS found 11:20, M1 11:25, M3 never)
# generation (11:17-11:28): 8 batches x 50 sentences x 10 slots = 4,000 calls, $0.382
bash e2bsrc/src_e2b/gen_all.sh
# label-free scoring (11:29-12:10) under the open() guard
bash src/scoring_pipeline.sh     # build rows, disguise (vendor_d), L3 questionnaires (400/400, $0.092), judges...
bash src/judge_chain.sh          # flash-lite: 2,735 disguised units answered before the 403 stop; nano/deepseek refused
exp5src/.venv/bin/python src/score_e2b.py frontier_sample --n 300 && exp5src/.venv/bin/python src/score_e2b.py judges --which frontier_pilot
bash src/cpu_chain.sh            # exp-5 pool scoring (2 workers, 35 min), local features, eval-2 matrix (132 s), M1 variants
# labels (11:28-12:38): batch-1 panel started, 403 at 11:39 -> driver stopped, incomplete records quarantined,
# solver labels for all 400 sentences on CPU (3 workers, 57 min)
cd e2bsrc && .venv/bin/python src_e2/e.py run_label.py --kind heldout --budget 8 --workers 3 && cd ..
nohup python3 src/budget_poller.py &                                # 15-min probes 11:41-14:41, all 403; stopped 14:47
cd e2bsrc && .venv/bin/python src_e2b/controls_lf.py 300 && cd .. && exp5src/.venv/bin/python src/score_e2b.py controls --which lf
# checks
exp5src/.venv/bin/python src/verify_exp5_copy.py [--reduced]        # 50/50 E rows: c_score_align and p_peer_text exact
exp5src/.venv/bin/python src/check_T1_repro.py                      # T1 L25 delta 0.06942, long 0.11626 reproduced exactly
exp5src/.venv/bin/python tests/test_union_synthetic.py; exp5src/.venv/bin/python tests/test_analysis_synthetic.py
# finalisation (12:38-14:07): score seal -> incomplete batch excluded -> E2 assemble/controls/testability/seal/verify
#   -> labelled controls -> score seal refreshed -> join + analyses (B=2000, seed 0) -> union placeholder -> outputs
bash src/finalize.sh
python3 src/write_deviations.py
exp5src/.venv/bin/python src/rederive_headline.py                   # independent re-derivation + placebos
# equivalently: python3 method.py --stage all
```
Seeds: bootstrap seed 0 (exp-6 ClusterBoot, B=2000); the re-derivation uses seed 12345. Every ordering is a sha1 hash
(`E2_v1|`, `E2B_batch_v1|`, `E2B_frontier_v1|`, `E2B_lfctrl|`, `E2_folds_v1|`). The run took about 3.8 h of wall time, dominated by
CPU (z3) work on 4 cores.

## 5. What you should get
| file | content |
|---|---|
| `e2b/census_E2B.json` | E2 pool reproduced; 400 sentences (98 surplus + 302 continuation), 93.5% 25-29 words; 0 collisions |
| `e2b/testability_E2B.json` | no cell testable; R_A_UNAUDITED L25 48 CORRECT / 334 ERROR |
| `analysis/analysis_E2B.json`, `analysis/tables.md` | exploratory R_A_UNAUDITED cell: V0 strat AUROC 0.737 [0.645, 0.827]; flash-lite disguised 0.496; V0 − flash-lite +0.208 [0.066, 0.363] (276 paired rows, 31 CORRECT); nested [S4+V0]−S4 +0.120; V0 with gold-equivalent peers removed 0.611 |
| `analysis/descriptive_nolabels_E2B.json` | parse rate 0.883; cross-family agreement 13.4%; Spearman(V0, flash-lite) 0.296; rename paired flips 0.088 (SYN) / 0.107 (NONCE), reverse flips 0 |
| `analysis/rederive_headline.json` | the same numbers re-derived through sklearn and an independent bootstrap; placebo permutation null mean 0.001 (p = 0.005 for the observed Δ); the permuted-label and random-score CIs include 0 |
| `method_out.json` | exp_gen_sol_out; 4,000 candidate rows + 79 rename-control rows |

In the paper these numbers belong in the E2-B / replication section as a PARTIAL, EXPLORATORY result. They are not a
confirmation: without the panel, CORRECT means z3-equivalent to an unaudited gold, which structurally favours agreement-based
metrics (see the label-coupling diagnostic).
