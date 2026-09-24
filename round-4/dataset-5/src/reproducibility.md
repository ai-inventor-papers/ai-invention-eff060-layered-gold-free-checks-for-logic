# Reproducibility: T7b name-free FREE labels (gen_art_dataset_5)

This file describes exactly what was run on 2026-09-24 (UTC 07:07–07:52) to produce the released outputs.

**The released labels are SEARCH-ONLY (deviation D9).** Every paid OpenRouter call was refused with HTTP 403
`aii_run_budget_exhausted`, so this artifact spent $0. The CPU-only steps below reproduce every released file
bit-for-bit, except for the UTC timestamps in `seal.json`, `deviations.json` and the testability file. Step 7 lists the
paid steps that were written and tested but not run.

## 1. Get the folder

```bash
cp -r /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5 ~/t7b && cd ~/t7b
```

The code reads these other run artifacts **read-only**, by absolute path (`src/common.py`). A copy elsewhere needs these
paths to exist, or the constants in `src/common.py` must be edited:

| input | path under `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/` |
|---|---|
| FREE generations (no scores) | `iter_3/gen_art/gen_art_experiment_7/rcomp/raw/generations.jsonl` |
| sentences and references | `iter_3/gen_art/gen_art_experiment_7/rcomp/work/rcomp_sentences.json` |
| SIG pure-z3 labels | `iter_3/gen_art/gen_art_experiment_7/results/sig_labels.jsonl` |
| old labels (post-seal join only, whitelist loader) | `iter_3/gen_art/gen_art_experiment_7/results/rcomp_candidates.jsonl` |
| WordNet data (`NLTK_DATA`) | `iter_3/gen_art/gen_art_experiment_7/data/nltk_data` |
| lexicon | `iter_2/gen_art/gen_art_dataset_3/lexicon.json` |
| cross-check | `iter_2/gen_art/gen_art_dataset_3/full_data_out.json` |
| vendored code sources (hashes in `VENDOR_SHA256.json`) | dataset 3 `labeller/fol.py`, `labeller/repair_census.py`, `src/templates.py`, `src/perturb.py`; exp 5 `src/vendor_a/fol_triage.py`; exp 7 `src/sig_prompt.py`, `src/label_sig.py` |

## 2. Environment

**Machine:**
- Ubuntu (Linux 6.17);
- 4 vCPUs (CPU affinity) on an AMD EPYC 9655P;
- 32 GB cgroup RAM limit;
- **no GPU**.

**Software:**
- Python 3.12.14;
- `uv` for all package management (no pip);
- no system packages beyond Python and uv.

```bash
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r pyproject.toml   # 24 pinned packages, e.g. z3-solver==5.1.0.0, nltk==3.10.3,
                                                              # loguru==0.7.3, numpy==2.5.3, httpx==0.28.1, pytest==9.1.1
```

`data.py` is a uv inline script; `uv run data.py` builds its own environment (`loguru==0.7.3`).

**Environment variables (names only):**

| variable | needed for |
|---|---|
| `OPENROUTER_BASE_URL`, `OPENROUTER_API_KEY` | only the paid steps in 7 and the model-catalogue snapshot |
| `HF_TOKEN` | optional, for the dataset survey |

Neither the CPU steps nor any model download needs them.

## 3. Downloads

- **Models:** none.
- **External data:** only for the context survey (`src/hf_survey.py`, via the HuggingFace Datasets Server API). It goes
  into `temp/datasets/` and is **not** used for any label.
- **Catalogue snapshot:** the OpenRouter price snapshot `work/models_snapshot.json` was fetched once with a GET on
  `$OPENROUTER_BASE_URL/models`.

## 4. Commands, in the order they ran

Wall times are on the 4-vCPU machine. All seeds are fixed in code:
- shape census `random.Random(0)`;
- evaluator test `Random(7)`;
- audit samples `Random(20260924)` / `Random(20260925)`;
- fingerprint interpretations crc32-seeded (`src/freelab.py`, 128 interpretations, domain 2/3);
- SIG renames `sha1(sentence_id + mode)`.

```bash
.venv/bin/python src/vendor_copy.py                  # A1 vendor + VENDOR_SHA256.json (<1 s)
.venv/bin/python src/inputs.py                       # A2-A6: work/sentences.json, work/free_rows.jsonl, work/sig_rows.jsonl,
                                                     #   results/input_counts.json, results/shape_census.json (~2 s)
.venv/bin/python -m pytest -q                        # 13 tests incl. evaluator-vs-z3 on 200 random pairs, firewall (~10 s)
.venv/bin/python src/prereg.py                       # B: prereg v1 (the committed file is v1.1; see below)
.venv/bin/python src/run_search.py free --limit 10   # C staging: 10 classes (2 s)
.venv/bin/python src/run_search.py free --limit 100  # 100 classes (10 s)
.venv/bin/python src/run_search.py free              # all 2,163 unique classes, 4 spawn workers (~3.5 min) -> results/map_search.jsonl
.venv/bin/python src/gate.py build                   # D1: results/gate_items.json (840 items)
.venv/bin/python src/gate.py run --half A            # D2: all 190 calls refused (403) -> gate NOT_RUN (results/gate_report.json)
.venv/bin/python src/sig_rename.py                   # F(i) inputs: work/sig_renamed_{nonce,syn}.jsonl (~15 s)
.venv/bin/python src/run_search.py sig --rename nonce   # ~1.5 min -> results/sig_replay_nonce.jsonl
.venv/bin/python src/run_search.py sig --rename syn     # ~1.5 min -> results/sig_replay_syn.jsonl
.venv/bin/python src/assemble_labels.py --mode search_only   # G: results/free_labels_v2.jsonl, testability, seal (~2 s)
.venv/bin/python src/post_seal_join.py               # H: whitelist join, untouched subset, results/old_label_agreement.json
.venv/bin/python src/soundness.py                    # F: results/soundness_audit.json, results/sig_replay_rows.jsonl
.venv/bin/python src/provisional_view.py             # provisional ERROR_CERT vs MAPPED testability
uv run data.py                                       # I: full_data_out.json (3 groups)
# aii-json skill: validate (exp_sel_data_out) and make mini/preview; renamed to mini_data_out.json / preview_data_out.json
```

**How the pre-registration evolved:**
- The v1 prereg (`prereg_freelab_v1.json`, sha256 `1d6875a9…`) was frozen before any FREE labelling.
- After the 10-class staging run it was amended to v1.1 (D6: no B3+B4 in one map). This is `prereg_freelab.json`,
  sha256 `b081c399…`. The v1.1 file was produced by a one-off inline script (recorded in `deviations.json`) that loads v1
  and adds the `amendments` block.
- The first full FREE search was then re-run after D8 (storing T8 converse maps). Only the second run's output is kept.

**Hand-made inputs:**
- `work/executor_audit_verdicts.json` holds the executor's (non-blind) audit verdicts on 60 + 60 rows and the 20 old/new
  disagreements.
- They were written by reading `work/audit_mapped_view.txt` and the equivalent ERROR_CERT listing; the sampled row keys
  are in `work/audit_*_keys.json`.

## 5. Expected outputs and numbers

**Label and dataset files:**

| file | content |
|---|---|
| `full_data_out.json` | `rcomp_free_labels` 2,652, `gloss_gate_items` 840, `sig_soundness_replay` 4,280 examples |
| `results/free_labels_v2.jsonl` labels | ERROR_CERT 759 · UNRESOLVED_GLOSS_NOT_RUN 1,506 · UNPARSEABLE 188 · NO_OUTPUT 199 |
| `results/seal.json` | all-row label-vector sha256 `9609ebbb725832c467389e9d04b6334ca906ba10d400e7a7dccd976d39ebe3dd`; untouched `b364a49a8e21835de660689097b462212f3f72b96ef66b437a14cc60e039f500` |

**Map search** (`results/map_search.jsonl`):
- 2,163 classes: 1,413 MAPPED, 750 ERROR_CERT;
- 0 capped, 0 z3 unknown;
- 11,530 unique gloss pairs.

**Audits** (`results/soundness_audit.json`):
- SIG replay, nonce and synonym:
  - false ERROR_CERT on SIG-CORRECT: 0/1,595;
  - identity recovery: 1.00;
  - rescue on SIG-ERROR: 0.091 (nonce), 0.105 (synonym);
  - oracle ceiling: recall 1.00, false CORRECT 0.00.
- Executor audit: ERROR_CERT precision 0.867 [0.758, 0.931]; MAPPED faithful 0.867 [0.758, 0.931].

**Old-label agreement** (`results/old_label_agreement.json`):
- old CORRECT → MAPPED: 34/34;
- old ERROR → ERROR_CERT: 123;
- old ERROR → MAPPED: 297;
- κ = 0.058;
- 0 missing row keys.

**Testability** (`results/testability_FREE_v2.json`):
- search-only labels: NOT_TESTABLE (0 CORRECT);
- provisional view: TESTABLE on all rows (759 / 1,506) and on the untouched subset (636 / 1,175).

In the paper, these numbers belong in the R_COMP-FREE labelling / meta-evaluation-set section (label construction and
soundness), and in the caveat that FREE AUROC awaits the gloss step.

## 6. Tests

```bash
.venv/bin/python -m pytest -q   # 13 passed
```

## 7. Paid steps not yet run (D9)

These need `OPENROUTER_BASE_URL` / `OPENROUTER_API_KEY` with budget. Estimated ≈$1.8 at the catalogue prices in
`work/models_snapshot.json`:

```bash
.venv/bin/python src/resume_gloss.py all
# gate (Haiku 4.5 + Qwen3-235B-2507, gloss_v1, half A) -> FREE gloss (11.5k pairs) -> final labels + new seal + z3
# re-verification of CORRECT certificates -> post-seal join -> SIG end-to-end 300 -> Sonnet-5 audit (ii) -> package
uv run data.py
```

Every call goes through `src/gloss.py`, which provides a cache, writes the cost ledger (`cost_ledger.jsonl`) and stops
hard at $6.
