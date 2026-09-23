# Held-out NL→FOL faithfulness meta-evaluation set (run_u75jRHUss0zo, invention iter 1, dataset E)

Workspace (absolute): `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_dataset_1`

This is the one-shot **confirmation** population for gold-free NL→FOL faithfulness metrics. Iteration 2 must not tune
thresholds on it. It has 600 screen-disjoint sentences (MALLS-train L25/L20/EXC plus FOLIO-train CTRL). Each sentence has
real candidates from 9 LLM families, a zero-shot variant, a frontier model, ccg2lambda and the MALLS GPT-4 gold, labelled by
the shared solver labeller.

It also contains the rebuilt shared screen (Logic-LM track L + curated track H), keyed by the screen's exact `item_id`, and
the panel calibration material.

**Read `dataset_card.md` first.**

The LLM panel stage (gold audit + tier-B adjudication + track-H real-error check + screen audit) was **blocked**: the OpenRouter
key is shared across runs and has a $50/day limit, which other runs exhausted at 13:29 UTC. In this release:
- CORRECT/ERROR labels are solver-only, against an unaudited reference (tier `A_unaudited_ref`);
- every row the solver cannot settle is `UNRESOLVED`.

`src/resume_panel.sh` completes those steps (they are resumable and cached) once the key has credit again.

## Deliverables
| Path | What |
|---|---|
| `data.py` | `uv run data.py`: builds the dataset from `work/assembled.json`, re-verifies EVERY row against the sources symlinked in `temp/datasets/` (`metadata_source_verified`: 9,253/9,253 true), writes the files below |
| `full_data_out.json` | **THE DATASET** (aii-json `exp_sel_data_out`, single file, 26.6 MB, under the 100 MB limit). Groups: `heldout_candidates` (7,307), `heldout_sentences` (600), `panel_calibration` (173), `screen_audit` (1,173). Absolute path: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json` |
| `mini_data_out.json`, `preview_data_out.json` | First 3 rows per group; preview truncates strings to 200 chars |
| `screen_adjudicated_labels.json` | `{item_id: {track, system, auto_label, repair_ops, panel_votes, final_label, label_tier, reading_choice, join_keys, ...}}` for the screen (absolute path: workspace + `/screen_adjudicated_labels.json`) |
| `prereg_strata.json` | Strata definitions, counts and exclusion counts (frozen at selection, before any generation). The testability declaration was added after labelling, before any metric run |
| `dataset_card.md` | Data-quality statistics, label rule, gate tables, deviations, licences |
| `work/label_report.json` | Every statistic in the card, machine-readable |
| `cost_ledger.jsonl` | One line per OpenRouter call (phase, model, tokens, usage.cost) |

Row format: `input` = JSON string `{text, candidate_fol, reference_fol, system, prompt_variant}`; `output` = final label
(`CORRECT` / `ERROR` / `CONTESTED` / `UNRESOLVED` / `UNPARSEABLE`).

Key `metadata_*` fields:
- `item_id`, `sentence_id`, `system`, `slot`, `family`, `system_class`, `raw_output`, `normalisation_applied`;
- `auto_label`, `equiv_status`, `repair_ops`, `repair_status`, `convention_flags`;
- `panel_votes`, `error_ops`, `label_tier`, `label_source`, `solver_lenient_label` (sensitivity only);
- `correct_not_equivalent`, `reading_choice`, `gold_audit_flag`, `reference_status`;
- `strata` {words, n_quant, depth, n_conditions, text_conditions, exception_type, source_stratum, ctrl_len_bin};
- `disguised_text`, `disguised_fol`, `class_id`, `class_size`, `cost_usd`.

The held-out `item_id` = sha1(system|norm(text)|raw_output.strip())[:16], using the screen's norm.

## Layout
- `labeller/`: the shared labeller.
  - `fol.py`: the iter-3 parser with the ⊕ precedence fix and the `<->` tokenisation fix.
  - `repair_census.py`: verbatim, with the data path repointed.
  - `label_lib.py`: `equivalent_modulo_vocab`, `minimal_typed_repair`, `convention_flags`, `auto_label`.
  - `disguise.py`: the nonce disguise.
  - `complexity_counts.py`, `lint_smells.py`: copied for reference; L1 lint is NOT run here.
- `src/`: pipeline scripts (below). `tests/test_fol.py`: parser regression tests.
- `prompts/`:
  - `fewshot_v1.txt` (sha1 a1c7ae39…): the frozen generation prompt;
  - `zeroshot_v1.txt`: the same prompt without exemplars.
- `raw/`:
  - `generations.jsonl`: all generator API outputs, irreproducible;
  - `ccg2lambda_candidates.jsonl`;
  - `logiclm/`: Logic-LM FOLIO_dev outputs;
  - `hf/`: HF downloads.
- `work/`:
  - `sentences.json`, `calib_sentences.json`, `fewshot_exemplars.json`, `exclusion_log.json`;
  - `labels_heldout.jsonl` and `labels_screen.jsonl`: per-sentence class collapse and labels;
  - `screen_items.json`, `screen_meta.json`, `calibration_items.json`;
  - `gate_results*.json`, `panel_cache.jsonl` (every panel response), `trackh_panel_rows.json`;
  - `models_snapshot.json`, `generation_manifest.json`, `assembled.json`, `label_report.json`.
- `data_local/`: read-only copies of the iter-3 source files (MALLS-v0.1, folio-refined, DSAVlab curated).

## How to rerun (each step is resumable from its jsonl)
```
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python z3-solver nltk aiohttp loguru huggingface_hub numpy scipy requests pytest pandas pyarrow
.venv/bin/python -m pytest -q -c pytest.ini tests/test_fol.py     # step 0b regression
.venv/bin/python src/select_sentences.py                          # step 1 (deterministic; the 6 exemplars were then hand-picked, see card §9)
.venv/bin/python src/generate.py --limit 12 && .venv/bin/python src/generate.py --cap 3.5   # step 2 pilot + sweep
.venv/bin/python src/ccg2lambda_candidates.py                     # step 2d
.venv/bin/python src/screen.py                                    # step 6a
.venv/bin/python src/run_label.py --kind heldout --budget 8       # step 3 (~50 min on 4 CPUs)
.venv/bin/python src/run_label.py --kind screen --budget 8        # step 6b auto labels
.venv/bin/python src/calibration.py && .venv/bin/python src/gate.py --mode synthetic --members P1,P2,P3,R1 --cap 0.45   # step 4a/4b
bash src/resume_panel.sh                                          # steps 4c, 5b-5e, 6b panel (pending: needs key credit)
.venv/bin/python src/assemble.py && .venv/bin/python src/stats.py && .venv/bin/python src/card.py && uv run data.py   # step 7
```

## Restoring removed files
- `.venv/`: regenerable. `uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r pyproject.toml`
- `nltk_data/`: redownloadable. `.venv/bin/python -c "import nltk; [nltk.download(p, download_dir='nltk_data') for p in ('wordnet','omw-1.4')]"`
- `raw/hf/`: redownloadable. `.venv/bin/python -c "from huggingface_hub import hf_hub_download as d; [d('tasksource/folio', f, repo_type='dataset', local_dir='raw/hf/tasksource__folio') for f in ('folio_v2_train.jsonl','folio_v2_validation.jsonl')]; [d('kenken6696/folio_by_ccg2lambda', f, repo_type='dataset', local_dir='raw/hf/kenken6696__folio_by_ccg2lambda') for f in ('data/train-00000-of-00001.parquet','data/valid-00000-of-00001.parquet')]"`
  (`temp/datasets/` symlinks point into it.)
- `__pycache__/`, `src/__pycache__/`, `tests/__pycache__/`, `labeller/__pycache__/`: regenerable Python bytecode, recreated on import.
- `.pytest_cache/`: regenerable. `.venv/bin/python -m pytest -q -c pytest.ini tests/test_fol.py`
