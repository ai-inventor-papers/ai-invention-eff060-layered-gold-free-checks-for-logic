# R_COMP + PERTURB: long composed sentences with trusted answers (run_u75jRHUss0zo, invention iter 2, dataset_3)

Workspace (absolute): `.`

This repository builds two held-out tables for evaluating gold-free NL→FOL faithfulness metrics. It deepens dataset E
(`round-1/dataset-1/src`). E's code is copied into `labeller/` and `src_e/`; E itself is never written to.

1. **R_COMP.** 250 main + 100 reserve composed sentences. Each has at least 25 words, at least 3 conditions and exactly
   one unless / except / provided-that / as-long-as / only-if clause.
   - Every sentence is filled from an atom lexicon: atom ⇄ English verb phrase pairs mined from screen-disjoint,
     already-verified short references.
   - The sentence is built with one of 9 templates. Each template derives a **weak** and a **strong** exception
     reading (T8 also stores the not-accepted only-if converse) from the same slots that fill the text. The
     references are therefore trusted **by construction**; unit tests and z3 checks verify this.
   - The real candidates come from E's 13 generator × prompt rows and are labelled by E's solver labeller against
     both readings, plus the shared Sonnet adjudicator.
2. **PERTURB.** 4,234 z3-verified typed mutants over 300 bases (200 E references + 100 R_COMP references).
   - 13 operator families at matched DOWN/UP positions (1,354 complete matched pairs).
   - 868 z3-verified meaning-preserving controls (RENAME_SYN / RENAME_NONCE, REORDER, CONTRAPOSITIVE / DEMORGAN).

**Status (read `dataset_card.md` §0).** The shared OpenRouter key hit its $50/day limit about 5 minutes into this module.
- Complete: every $0 phase, including the full PERTURB suite and the pre-registration.
- Pending: every paid phase after the Haiku lexicon extraction:
  - Sonnet lexicon audit, fluency rating, Sonnet reference audit;
  - candidate generation (~3.1k calls), solver labels and adjudication;
  - the known-label check verdicts and the testability declaration.
- `./run_all.sh` completes all of it in the pre-registered order, resumably. `./watch_and_run.sh` waits for key budget
  first.
- A replacement key (21:38 UTC) was also already exhausted ($50.06/$50 used); it stayed at 0 until the final poll at
  22:07 UTC. To run with it:
  `OPENROUTER_API_KEY="$(cat /ai-inventor/aii_data/.secrets/openrouter_key.private)" ./run_all.sh`.
- Spend so far: $0.414 of the $10 budget.

## The two datasets (TODO 3 decision)
The plan targets two datasets, and both are delivered:
1. **R_COMP**: group `rcomp_sentences`, plus `rcomp_candidates` once generated.
2. **PERTURB**: group `perturb_suite`, with folds PERTURB and PERTURB_CONTROL.

`adjudicator_check` is kept as an auxiliary label-quality table in `adjudicator_check_out.json`, because the plan
requires it: its 60 known-label rows measure the adjudicator on R_COMP bases.

Source datasets, all in `temp/datasets/`:
- FOLIO-v2 (tasksource) and folio-refined: agreement premises, which give lexicon atoms and the TRUSTED_AGREED bases.
- MALLS-v0.1: E's GOLD_PANEL_OK and PANEL_REPAIRED references.
- Dataset E's `full_data_out.json`: the trusted and repaired reference status.
- DSAVlab curated sets, Logic-LM outputs and the validation/test splits: used only for screen exclusion hashes.

`temp/search/selection.json` records the 16 searches, the 8 previews, and why the other candidates (ProverQA,
LogicBench, ProofWriter, yale-nlp/FOLIO) were discarded.

## Deliverables
| Path | What |
|---|---|
| `full_data_out.json` | **THE DATASET**: the 2 chosen datasets (aii `exp_sel_data_out`, validated, 16 MB, under the 100 MB limit; built by `uv run data.py`, then formatted by the aii-json format script). Groups: `rcomp_sentences` (350), `perturb_suite` (5,102 = 4,234 PERTURB + 868 PERTURB_CONTROL). `rcomp_candidates` is added by `run_all.sh` once generation runs; the schema forbids an empty group. |
| `adjudicator_check_out.json` | auxiliary: the 60 known-label adjudicator QA rows (STEP 8a), same row format, validated; verdicts pending |
| `data.py` | `uv run data.py` (uv inline script): builds `full_data_out.json` + mini/preview from `work/assembled.json` (written by `src/assemble.py`) and re-verifies EVERY row against the sources in `temp/datasets/` (`metadata_source_verified`, `metadata_source_file`, `metadata_verify_notes`; current result: 350/350 sentences, 5,102/5,102 PERTURB rows, 60/60 check rows verified; all 652 lexicon entries trace to their source sentence + formula) |
| `mini_data_out.json`, `preview_data_out.json` | first 3 rows per group, from `aii_json_format_mini_preview.py --input full_data_out.json --format exp_sel_data_out` (outputs renamed from `*_full_data_out.json`); the preview truncates strings |
| `dataset_card.md` | datasheet: status, provenance, lexicon and composition statistics, filter counts, PERTURB counts per op × polarity with matched-pair coverage, disguise guard, costs, licences, biases, deviations |
| `prereg_rcomp.json` | pre-registration frozen before generation: templates and readings, filters, label rule, routing, caps, testability and top-up rules, perturbation spec. `testability_declaration` is filled once, after labelling and before any metric (`src/prereg.py declare`). |
| `lexicon.json` | 652 atom-lexicon entries: atom, phrase, noun/sortal, sort group, source rule, sentence and formula, audit status |
| `adjudication_prompt.txt` | shared ADJ-PROMPT, the verbatim sibling R_ADJ V1 (sha256 32bcc0f9…); model and params in `work/adjudicator_model.json` |
| `rcomp_peers.json` | `{sentence_id: {text, readings, template_id, candidates: [...]}}`; written after generation |
| `cost_ledger.jsonl` | one line per OpenRouter call (phase, model, tokens, usage.cost) |

Key row fields (see the card §1):
- `input` = JSON `{text, candidate_fol, reference_fol (= weak), reference_fol_weak, reference_fol_strong, system, prompt_variant}`.
- `output` = label.
- `metadata_item_id` = sha1(system|norm(text)|raw_output)[:16], E's recipe.
- R_COMP sentences: `metadata_template_id`, `surface_variant`, `sentence_seed`, `source_rule_ids`, `lexicon_ids`,
  `strata`, `audit_status`, `fluency`.
- PERTURB rows: `metadata_operator`, `subtype`, `position_polarity`, `polarity_method`, `matched_pair_id`,
  `base_item_id`, `base_trust`, `donor_item_id`.
- All rows: `metadata_disguised_text` / `metadata_disguised_fol` (E's disguise, per-sentence bijection; guard 0/125 mismatches).

## Layout
- `src/` (this module):
  - `common.py`: paths and imports of E's code.
  - `source_pool.py`: STEP 1, atom pool.
  - `lexicon.py`: 2a Haiku extraction, 2b deterministic checks, 2c Sonnet audit, 2d-2f build.
  - `templates.py`: the 9 templates with compositional readings.
  - `compose.py`: STEP 3, sha1-seeded composition and filters.
  - `select_rcomp.py`: preselect and final stratified selection.
  - `llm_phases.py`: 4a fluency, 4b reference audit.
  - `prereg.py`: STEP 5, plus the testability declaration.
  - `gen_rcomp.py`: STEP 6, wrapping E's `generate.py` unchanged; pilot then full then top-up.
  - `label_rcomp.py`: STEP 7, solver labels vs both readings (`--dry-run` tests the code path on PERTURB rows).
  - `adjudicate.py`: STEP 8, known-label check and the sentence-complete priority queue.
  - `perturb.py`: STEP 9, typed perturbations and controls.
  - `assemble.py`: final label rule, testability, disguise, `work/assembled.json`, statistics (then `data.py` writes `full_data_out.json`).
  - `card.py`, `verify.py` (independent z3 re-verification), `make_variants.py` (superseded by `data.py`).
  - `llm.py`: resumable batched calls on E's `or_client`.
  - `hf_preview.py`: dataset-search previews.
  - `key_poll.sh`.
- `src_e/`: E's `select_sentences.py`, `normalise.py`, `or_client.py`, `generate.py`, verbatim.
- `labeller/`: E's shared labeller, verbatim: `fol.py`, `label_lib.py`, `repair_census.py`, `disguise.py`, `complexity_counts.py`.
- `tests/`:
  - `test_fol.py`: E's tests, unchanged.
  - `test_templates.py`: readings and z3 relations per template.
  - `test_perturb.py`: the edit mirror is identical to `repair_census.edits`; polarity; controls.
  - All 17 tests pass.
- `prompts/`: E's frozen `fewshot_v1.txt` (sha1 a1c7ae39…, equal to E's `prompt_sha1`) and `zeroshot_v1.txt`.
- `raw/` (API outputs, irreproducible, keep):
  - `lexicon_extract.jsonl`: Haiku; truncated answers were salvaged.
  - Written by `run_all.sh`: `lexicon_audit.jsonl`, `fluency*.jsonl`, `ref_audit*.jsonl`, `generations.jsonl`, `adjudication.jsonl`.
  - `logiclm/`: E's copy, used for the screen exclusion.
  - `hf/tasksource__folio/`: FOLIO v2, redownloadable.
- `work/`: every intermediate and log:
  - pipeline: `source_rules.json`, `lexicon_checked.json`, `rcomp_pool.json` (5,109 filtered compositions),
    `rcomp_preselect.json`, `rcomp_sentences.json`;
  - PERTURB: `perturb_suite.json`, `perturb_controls.json`, `perturb_bases.json`;
  - adjudication: `adjudicator_check_items.json`, `adjudicator_model.json`;
  - statistics and logs: `stats.json`, `*_log.json`, `disguise_guard.json`;
  - dry run: `rcomp_labels_dryrun.json`, the solver dry run on 90 synthetic candidates.
- `data_local/`: read-only copies of E's local sources: MALLS-v0.1, folio-refined, DSAVlab curated, ProverQA dev.
- `temp/datasets/`: symlinks to the 4 kept sources. `temp/search/`: the 16 HF searches, 8 previews, web provenance and
  the keep/discard decision (`selection.json`).
- `logs/`: per-script logs; `key_status.log` holds the key polls.
- `run_all.sh`, `watch_and_run.sh`.

## How to run
```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r pyproject.toml
.venv/bin/python -m spacy download en_core_web_sm
.venv/bin/python -c "import nltk; [nltk.download(p, download_dir='nltk_data') for p in ('wordnet','omw-1.4')]"
.venv/bin/python -c "from huggingface_hub import hf_hub_download as d; [d('tasksource/folio', f, repo_type='dataset', local_dir='raw/hf/tasksource__folio') for f in ('folio_v2_train.jsonl','folio_v2_validation.jsonl')]"
.venv/bin/python -m pytest -q -c pytest.ini tests/                   # 17 tests
# $0 phases (deterministic; already run):
.venv/bin/python src/source_pool.py && .venv/bin/python src/lexicon.py check && .venv/bin/python src/lexicon.py build
.venv/bin/python src/compose.py && .venv/bin/python src/select_rcomp.py preselect && .venv/bin/python src/select_rcomp.py final
.venv/bin/python src/perturb.py && .venv/bin/python src/adjudicate.py select && .venv/bin/python src/assemble.py
uv run data.py && .venv/bin/python src/verify.py && .venv/bin/python src/card.py
# every paid phase, in pre-registered order (resumable; OPENROUTER_API_KEY needed; hard stop AII_HARD_CAP=9.5):
./run_all.sh            # or: nohup ./watch_and_run.sh 86400 > logs/watch.log 2>&1 &
```

## Restoring removed files
- `.venv/` (regenerable, about 2 GB):
  `uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r pyproject.toml` (every package is pinned to the exact installed version, including the spaCy model wheel URL).
  This also restores the spaCy model `en_core_web_sm` inside `.venv`.
- `nltk_data/` (redownloadable):
  `.venv/bin/python -c "import nltk; [nltk.download(p, download_dir='nltk_data') for p in ('wordnet','omw-1.4')]"`
- `raw/hf/` (redownloadable; the `temp/datasets/tasksource__folio` symlink points into it):
  `.venv/bin/python -c "from huggingface_hub import hf_hub_download as d; [d('tasksource/folio', f, repo_type='dataset', local_dir='raw/hf/tasksource__folio') for f in ('folio_v2_train.jsonl','folio_v2_validation.jsonl')]"`
- `__pycache__/` in `src/`, `src_e/`, `labeller/`, `tests/` (regenerable): Python bytecode, recreated on import.
- `.pytest_cache/` (regenerable): `.venv/bin/python -m pytest -q -c pytest.ini tests/`
