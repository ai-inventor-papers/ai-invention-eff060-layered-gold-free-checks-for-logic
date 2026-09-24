# Held-out NL→FOL faithfulness meta-evaluation set (run_u75jRHUss0zo, invention iter 1, dataset E)

Workspace (absolute): `.`

This is the one-shot **confirmation** population for gold-free NL→FOL faithfulness metrics. **Iteration 2 must not tune any
threshold on it.**
- 700 screen-disjoint sentences:
  - MALLS-train L25 (300, including a pre-registered 100-sentence top-up), L20 (150) and EXC (100);
  - FOLIO-train CTRL (150).
- 8,507 real candidate rows. They come from 9 LLM families (10 few-shot slots), 2 zero-shot variants, the frontier model
  GPT-5.1 on 200 sentences, ccg2lambda, and the MALLS GPT-4 gold treated as a system.
- Each row is labelled by the shared solver labeller (`labeller/`, the ⊕-precedence-fixed iter-3 code) and by a blind,
  disguised, family-disjoint LLM panel: Haiku-4.5 / GLM-4.6 / Kimi-K2. The panel passed a known-label gate, and its
  accuracy on real errors is measured against expert corrections.
- The panel also audits every reference, and wrong MALLS references were repaired by panel agreement where possible.
- The rebuilt shared screen (Logic-LM track L + curated track H) is included, keyed by the screen's exact `item_id`.

**Read `dataset_card.md` first.** It holds every data-quality statistic, the label rule verbatim, the panel calibration and
the known biases.

## Headline numbers
- Final labels (held-out rows): `{"UNPARSEABLE": 1086, "CORRECT": 1750, "ERROR": 5005, "UNRESOLVED": 276, "CONTESTED": 390}`. Tiers: `{"-": 1086, "A": 1044, "B": 2157, "C": 3891, "none": 276, "A_unaudited_ref": 53}`.
- Testability (LLM rows, tiers A+B, CONTESTED and reading_choice excluded; each cell is rows (distinct sentences)):

| stratum | CORRECT A+B | ERROR A+B | testable | CORRECT tier A | ERROR tier A |
|---|---|---|---|---|---|
| L25 | 176 (78) | 697 (107) | yes | 40 (25) | 98 (46) |
| L25_orig200 | 141 (54) | 567 (70) | yes | 34 (19) | 73 (30) |
| L25_topup100 | 35 (24) | 130 (37) | no | 6 (6) | 25 (16) |
| L20 | 229 (65) | 592 (79) | yes | 64 (33) | 132 (51) |
| EXC | 222 (55) | 384 (63) | yes | 124 (38) | 129 (48) |
| CTRL | 237 (31) | 149 (28) | yes | 186 (20) | 94 (15) |

- Panel: its majority accuracy on the 75 unambiguous expert-corrected real-error pairs is 0.727. It
  accepts only 0.613 of the expert-corrected formulas, so it is STRICT.
  - The reference audit rejects 440/535 MALLS golds and
    112/148 CTRL references. Part of this is likely panel over-strictness
    (card §0 and §7).
  - Cohen κ between GLM and Kimi is 0.5133; the
    3-rater Fleiss κ on the pilot is 0.5391.
- Solver labeller vs panel majority: error precision 0.7879, error recall
  0.8363.
- OpenRouter spend: $9.833, still under the $10 artifact budget. The plan cap was $9.50; it was raised to
  $9.80 for the last repair and adjudication calls, and one batch overshot. See card §0.

## Deliverables
| Path | What |
|---|---|
| `full_data_out.json` | **THE DATASET** (aii-json `exp_sel_data_out`, validated; 27.7 MB, one file). Groups: `heldout_candidates` (8,507), `heldout_sentences` (700), `panel_calibration` (173), `screen_audit` (1,173). Absolute path: `./full_data_out.json` |
| `mini_data_out.json`, `preview_data_out.json` | First 3 rows per group; the preview truncates strings to 200 chars |
| `screen_adjudicated_labels.json` | `{item_id: {track, system, auto_label, repair_ops, panel_votes, final_label, label_tier, reading_choice, join_keys, ...}}` for the screen. Absolute path: `./screen_adjudicated_labels.json` |
| `prereg_strata.json` | Strata definitions and exclusion counts (frozen at selection), the L25 top-up execution record, and the testability declaration (`testability_declaration.primary_pool`, made before any metric run) |
| `dataset_card.md` | Data-quality statistics, the label rule, gate and real-error tables, deviations, licences |
| `work/label_report.json` | Every statistic in the card, machine-readable |
| `cost_ledger.jsonl` | One line per OpenRouter call: phase, model, tokens, usage.cost |
| `data.py` | `uv run data.py` builds `full_data_out.json` from `work/assembled.json` and re-verifies EVERY row against the sources in `temp/datasets/`. Result: `metadata_source_verified` is true for 10,553/10,553 rows |

Row format:
- `input` is a JSON string `{text, candidate_fol, reference_fol, system, prompt_variant}`.
- `output` is the final label: `CORRECT` / `ERROR` / `CONTESTED` / `UNRESOLVED` / `UNPARSEABLE`. Sentence rows carry the
  reference status instead.

Key `metadata_*` fields:
- identity: `item_id` (sha1(system|norm(text)|raw_output)[:16], the screen recipe), `sentence_id`, `system`, `slot`,
  `family`, `system_class`, `prompt_variant`, `raw_output`, `normalisation_applied`;
- solver: `auto_label`, `equiv_status`, `repair_ops`, `repair_status`, `convention_flags`;
- panel: `panel_votes` (per model: faithful, ops, conf), `panel_item`, `panel_ambiguous`, `panel_scope`;
- final label: `error_ops`, `label_tier` (A / B / C / A_unaudited_ref / none / -), `label_source`, `correct_not_equivalent`,
  `reading_choice`, `addrop_only_suspect`;
- reference: `gold_audit_flag`, `reference_status`;
- `strata` {words, n_quant, depth, n_conditions, text_conditions, exception_type, source_stratum, ctrl_len_bin,
  l25_topup_batch};
- `disguised_text`, `disguised_fol`, `class_id`, `class_size`, `cost_usd`.

**Primary analysis**: tiers A+B, excluding CONTESTED and reading_choice rows. Bootstraps must resample by `sentence_id`.
**Robustness**: tier A only. **Secondary**: tier C (panel-only labels for sentences without a trusted reference).

## Layout
- `labeller/`: the shared labeller.
  - `fol.py`: the iter-3 parser with the ⊕-precedence and `<->` fixes.
  - `repair_census.py`.
  - `label_lib.py`: `equivalent_modulo_vocab`, `minimal_typed_repair`, `convention_flags`, `auto_label`.
  - `disguise.py`: the nonce disguise.
  - `complexity_counts.py`, `lint_smells.py`: reference copies; L1 lint is NOT run.
- `src/`: pipeline scripts.
  - `select_sentences.py`, `select_topup.py`: sentence selection and the L25 top-up.
  - `generate.py`, `ccg2lambda_candidates.py`, `normalise.py`: candidate generation and normalisation.
  - `screen.py`: the screen rebuild.
  - `run_label.py`, `label_worker.py`, `extend_labels.py`: solver labelling; `extend_labels.py` adds new rows without
    renumbering classes.
  - `calibration.py`, `gate.py`: the gate and track H.
  - `panel.py`, `panel_run.py`: the panel, including the `--adjudicate`, `--ctrl-reduced` and `--vg-only` modes.
  - `screen_scope.py`, `repair_refs.py`.
  - `assemble.py`, `stats.py`, `card.py`: the final label rule, the statistics and the card.
  - `or_client.py`: an async OpenRouter client with a cost ledger and budget stops.
  - `resume_panel.sh`: the LLM steps in the order they were executed.
- `tests/test_fol.py`: parser regression tests.
- `prompts/`: `fewshot_v1.txt` (the frozen generation prompt) and `zeroshot_v1.txt`.
- `raw/` (irreproducible API outputs, keep):
  - `generations.jsonl`: all generator outputs; the later of duplicate keys wins;
  - `reference_repair.jsonl`: the panel-written references;
  - `ccg2lambda_candidates.jsonl`;
  - `logiclm/`;
  - `hf/`: HF downloads.
- `work/`:
  - `sentences.json` (700 rows), `sentences_topup.json`, `sentences_600_before_topup.json`;
  - `labels_heldout.jsonl`, `labels_heldout_repaired.jsonl`, `labels_screen.jsonl`: per-sentence classes and labels;
  - `panel_cache.jsonl`: every panel response;
  - `panel_heldout.jsonl` and `panel_heldout_adj.jsonl`: stage 1, and the Haiku adjudication;
  - `panel_screen.jsonl`, `panel_screen_vg.jsonl`;
  - `reference_overrides.json`, `no_trusted_reference.json`;
  - `gate_results.json` (synthetic gate + track H), `trackh_panel_rows.json`;
  - `assembled.json`, `label_report.json`;
  - backups of the pre-panel versions: `*_v1_blocked.py.txt`, `labels_heldout.jsonl.bak_before_extend`.
- `data_local/`: read-only copies of the iter-3 source files (MALLS-v0.1, folio-refined, DSAVlab curated).
- `temp/datasets/`: symlinks to every source used by `data.py`. No external dataset search was needed: the plan fixes all
  sources.

## How to rerun (each step is resumable; the panel cache never re-bills)
```
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r pyproject.toml
.venv/bin/python -m pytest -q -c pytest.ini tests/test_fol.py                   # step 0b regression
.venv/bin/python src/select_sentences.py                                        # step 1 (the 6 exemplars were hand-picked, card §10)
.venv/bin/python src/generate.py --limit 12 && .venv/bin/python src/generate.py --cap 3.5   # step 2
.venv/bin/python src/ccg2lambda_candidates.py && .venv/bin/python src/screen.py             # step 2d, 6a
.venv/bin/python src/run_label.py --kind heldout --budget 8 && .venv/bin/python src/run_label.py --kind screen --budget 8   # step 3
.venv/bin/python src/calibration.py && .venv/bin/python src/gate.py --mode synthetic --members P1,P2,P3,R1 --cap 0.45       # step 4a/4b
bash src/resume_panel.sh    # 4c, top-up, 5b-5e, 6b, then assemble -> stats -> card -> data.py
```
OpenRouter needs `OPENROUTER_API_KEY`. `AII_HARD_CAP` (default 9.50) is the cumulative-spend stop.

## Restoring removed files
- `.venv/` (regenerable): `uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r pyproject.toml`
- `nltk_data/` (redownloadable):
  `.venv/bin/python -c "import nltk; [nltk.download(p, download_dir='nltk_data') for p in ('wordnet','omw-1.4')]"`
- `raw/hf/` (redownloadable):
  `.venv/bin/python -c "from huggingface_hub import hf_hub_download as d; [d('tasksource/folio', f, repo_type='dataset', local_dir='raw/hf/tasksource__folio') for f in ('folio_v2_train.jsonl','folio_v2_validation.jsonl')]; [d('kenken6696/folio_by_ccg2lambda', f, repo_type='dataset', local_dir='raw/hf/kenken6696__folio_by_ccg2lambda') for f in ('data/train-00000-of-00001.parquet','data/valid-00000-of-00001.parquet')]"`.
  The `temp/datasets/` symlinks point into it.
- `__pycache__/`, `src/__pycache__/`, `tests/__pycache__/`, `labeller/__pycache__/` (regenerable): Python bytecode,
  recreated on import.
- `.pytest_cache/` (regenerable): `.venv/bin/python -m pytest -q -c pytest.ini tests/test_fol.py`
