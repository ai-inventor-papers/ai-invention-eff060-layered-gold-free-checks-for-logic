# Reproducibility: R_COMP + PERTURB dataset (`gen_art_dataset_3`)

This file was written after the fact from the workspace contents. Nothing was re-run to write it. Where the workspace does not record something, it says so.

## What is reproducible, and what is not

- **PERTURB** (group `perturb_suite`: 4,234 mutants and 868 controls) is complete. It is deterministic and needs no API key, only z3.
- **R_COMP** (group `rcomp_sentences`: 250 main and 100 reserve sentences) is built with no API calls after the Haiku lexicon extraction. Every LLM-dependent field is `PENDING`: the Sonnet lexicon audit, fluency, the reference audit, generator candidates (`rcomp_candidates`), solver labels, adjudication, and the testability declaration.
- **Cause.** The shared OpenRouter key hit its daily limit about 5 minutes into the module, and a replacement key was already exhausted (README, `dataset_card.md`).
- **LLM step that cannot be re-run.** The Haiku extraction output is stored in `raw/lexicon_extract.jsonl`. It is the only recorded output of the paid step, so keep it and do not re-bill it.
- **Cost.** `cost_ledger.jsonl` has 67 calls totalling $0.414154, all phase `lexicon_extraction` with model `anthropic/claude-haiku-4.5`.
- **R_COMP is not yet usable for metric claims.** Run `./run_all.sh` to complete it.

## 1. Get the artifact

```bash
git clone <URL-of-the-public-repository>   # the URL is not recorded in the workspace
cd <repository>/<folder-of-gen_art_dataset_3>
```

The workspace is one folder of that repository. Every path below is relative to it.

### Sibling input: dataset E (`gen_art_dataset_1`)

The pipeline reads the iteration-1 artifact `gen_art_dataset_1` (dataset E). Specifically it reads its `full_data_out.json`, which holds the `heldout_sentences` group with `TRUSTED_AGREED`, `GOLD_PANEL_OK` and `PANEL_REPAIRED` references. In the repository it is a sibling folder.

**Known portability defect.** The code hard-codes the original server path in `src/common.py` line 10:

```python
E_DIR = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_dataset_1")
```

`E_DIR` is imported by `src/source_pool.py`, `src/perturb.py` and `src/assemble.py`. In addition, `temp/datasets/E_heldout_dataset1_full_data_out.json` is a symlink to the same absolute path.

Before running the pipeline elsewhere, do both of these:

1. Edit `src/common.py` so that `E_DIR = ROOT.parent / "gen_art_dataset_1"`, or wherever the sibling folder is.
2. Re-point the symlink:
   ```bash
   ln -sfn ../../../gen_art_dataset_1/full_data_out.json temp/datasets/E_heldout_dataset1_full_data_out.json
   ```

This is not needed if you only read the shipped `full_data_out.json`. The workspace does not record whether these edits were made in the published copy.

## 2. Environment

- OS: Ubuntu (kernel 6.8, per the session environment). The workspace records no system packages beyond a working `curl`, `python3` and `uv`. The `run_all.sh` key check uses `curl` and `python3`.
- Python 3.12 (`requires-python = ">=3.12"`; the README uses `--python=3.12`).
- Tool: `uv`.

```bash
uv venv .venv --python=3.12
uv pip install --python=.venv/bin/python -r pyproject.toml
```

`pyproject.toml` pins every package to the exact installed version. `work/venv_freeze.txt` is the same list. Key pins:

| Package | Version |
|---|---|
| z3-solver | 5.1.0.0 |
| spacy | 3.8.16 |
| en-core-web-sm | 3.8.0, installed from a wheel URL |
| nltk | 3.10.3 |
| numpy | 2.5.3 |
| pandas | 3.0.6 |
| scipy | 1.18.1 |
| aiohttp | 3.14.3 |
| httpx | 0.28.1 |
| huggingface-hub | 1.32.0 |
| pyarrow | 25.0.1 |
| loguru | 0.7.3 |
| pytest | 9.1.1 |

Two setup notes:

- `pyproject.toml` lists only `dependencies`, with no build-system table. Install with `-r pyproject.toml` as the README does.
- `data.py` is a `uv` inline script that needs only `loguru`.

NLTK data (WordNet is used by the `MEANING_RENAME` operator and the lexicon checks; `nltk_data/` is not shipped):

```bash
.venv/bin/python -c "import nltk; [nltk.download(p, download_dir='nltk_data') for p in ('wordnet','omw-1.4')]"
```

## 3. Data downloads and keys

**FOLIO v2** (`tasksource/folio`), redownloadable from the Hugging Face Hub. Files are placed in `raw/hf/tasksource__folio`, which `temp/datasets/tasksource__folio` points to:

```bash
.venv/bin/python -c "from huggingface_hub import hf_hub_download as d; [d('tasksource/folio', f, repo_type='dataset', local_dir='raw/hf/tasksource__folio') for f in ('folio_v2_train.jsonl','folio_v2_validation.jsonl')]"
```

Already in the workspace:

- `data_local/`: MALLS-v0.1 train and test, folio-refined train and validation, and the DSAVlab curated sets. The DSAVlab sets and MALLS test are used only for screen-exclusion hashes. ProverQA dev is also there.
- `raw/logiclm/`: Logic-LM FOLIO dev outputs, used only for screen exclusion.
- `prompts/`: E's frozen prompts.
- `temp/datasets/`: symlinks into `data_local/`, `raw/` and E. The exact links are listed in `data.py`'s docstring.
- `temp/search/`: holds the HF search results and previews (`hf_search_results.txt`, `hf_previews.json`, `hf_previews.txt`) and the keep/discard record (`selection.json`, per the README).

**Environment variables (names only):**

- `OPENROUTER_API_KEY`: needed only for the paid phases (`run_all.sh`, `watch_and_run.sh`, `src/key_poll.sh`).
- `AII_HARD_CAP`: cumulative spend stop in USD; default 9.5 in `run_all.sh`.
- `AII_COST_LEDGER`: optional ledger path read in `src_e/or_client.py`.
- `LEX_MAX_RULES`: default 320; read in `src/lexicon.py`.

Models named in the workspace:

- Extraction: `anthropic/claude-haiku-4.5`.
- Adjudicator and audit: `anthropic/claude-sonnet-5`, temperature 0.0, max_tokens 300, reasoning disabled, fallback `anthropic/claude-sonnet-4.6` (`work/adjudicator_model.json`).

No GPU or model checkpoint is used.

## 4. Commands, in the order the README records

Run from the workspace root.

```bash
.venv/bin/python -m pytest -q -c pytest.ini tests/          # 17 tests, per README
# $0 deterministic phases
.venv/bin/python src/source_pool.py && .venv/bin/python src/lexicon.py check && .venv/bin/python src/lexicon.py build
.venv/bin/python src/compose.py && .venv/bin/python src/select_rcomp.py preselect && .venv/bin/python src/select_rcomp.py final
.venv/bin/python src/perturb.py && .venv/bin/python src/adjudicate.py select && .venv/bin/python src/assemble.py
uv run data.py && .venv/bin/python src/verify.py && .venv/bin/python src/card.py
```

Notes on these commands:

- `src/lexicon.py extract` (Haiku) was run first and is closed. It stopped at its $0.4 cap with 57 of 64 jobs done, and 7 jobs were left unextracted (`job_missing: 7` in `work/lexicon_check_log.json`). Its output is `raw/lexicon_extract.jsonl`.
- `uv run data.py` writes `full_data_out.json` and `adjudicator_check_out.json`.
- `mini_data_out.json` and `preview_data_out.json` come from the aii-json skill script `aii_json_format_mini_preview.py --input full_data_out.json --format exp_sel_data_out`, with outputs renamed from `*_full_data_out.json`. That script lives in the server-side skill directory `/ai-inventor/.claude/skills/aii-json` and is not in this repository. Schema validation used `aii_json_validate_schema.py --format exp_sel_data_out`.

**Paid phases** (needs `OPENROUTER_API_KEY`; resumable and cached per call; exit code 3 means key limit or cap reached):

```bash
export OPENROUTER_API_KEY=...          # supply your own; never commit it
./run_all.sh                            # or: nohup ./watch_and_run.sh 86400 > logs/watch.log 2>&1 &
```

`run_all.sh` runs these steps in order:

1. `src/lexicon.py audit --cap 0.5`
2. `src/lexicon.py build`
3. `src/compose.py`
4. `src/select_rcomp.py preselect`
5. `src/llm_phases.py fluency --cap 0.1`
6. `src/llm_phases.py audit --cap 0.7`
7. `src/select_rcomp.py final`
8. `src/perturb.py`
9. `src/adjudicate.py select`
10. `src/gen_rcomp.py pilot --cap 1.5`, then `full --cap 1.5`
11. `src/label_rcomp.py`
12. `src/adjudicate.py check --cap 0.2`
13. `src/adjudicate.py queue`
14. `src/adjudicate.py run --cap 2.5`
15. `src/assemble.py`
16. `uv run data.py`
17. An optional top-up (`gen_rcomp.py topup --cap 2.1`, then labelling and adjudication again).
18. `src/prereg.py declare`, `src/verify.py`, `src/card.py`, then schema validation and mini/preview generation.

The script ends with the two aii-json commands, which need the server-side skill directory noted above.

`run_all.sh` under the pre-registered rules in `prereg_rcomp.json` will change `full_data_out.json`, adding `rcomp_candidates` and filled label fields.

**Seeds.** There is no global random seed.

- Composition is seeded per sentence: `random.Random(int(sha1(f"rcomp|{t}|{i}"),16))` in `src/compose.py`.
- Perturbation and control choices are sha1-ordered (`src/perturb.py`), so the run is deterministic.
- The seeds themselves are stored per row as `metadata_sentence_seed`.

**Hardware and runtime** are not recorded. The machine had 2 CPU cores (`nproc`, checked at the time this file was written, not at build time). The only timing evidence is `logs/perturb_run.out`: PERTURB over 300 bases ran from about 18:16:57 to 18:17:30, roughly 33 s. z3 timeouts in the code are 3 s per mutant check and 8 s in `src/verify.py`.

## 5. Expected outputs and numbers

Where these appear in a paper is not recorded, because this artifact has no paper text. Numbers below come from `full_data_out.json` metadata, `work/stats.json`, `work/perturb_log.json`, `work/select_log.json` and `work/verify_report.json`.

**`full_data_out.json`** (about 16 MB) has two groups:

- `rcomp_sentences`: 350 rows (250 main and 100 reserve).
- `perturb_suite`: 5,102 rows.
  - 4,234 PERTURB mutants (output ERROR) and 868 PERTURB_CONTROL rows (output CORRECT).
  - 300 bases: 36 TRUSTED_AGREED, 95 GOLD_PANEL_OK, 69 PANEL_REPAIRED and 100 R_COMP.
  - 1,354 complete DOWN/UP matched pairs.
  - Controls: RENAME_SYN 141, RENAME_NONCE 159, REORDER_COMMUTE 258, REORDER_QUANT 21, CONTRAPOSITIVE 281, DEMORGAN 8.
  - Mutant counts per operator and polarity (for example NEG 283 DOWN and 300 UP, QUANT 281 UP) are in `work/perturb_log.json`.

**Verification** (`data.py` source verification and `work/verify_report.json`):

- 350/350 sentences, 5,102/5,102 PERTURB rows and 60/60 check rows verified.
- `failures` is empty.
- The independent z3 re-verification (`src/verify.py`) reports `ok: true`.

**Other outputs:**

- `adjudicator_check_out.json`: 60 known-label QA rows, verdicts pending.
- `mini_data_out.json` and `preview_data_out.json`.
- `dataset_card.md`, the datasheet with the counts above.
- `prereg_rcomp.json`.
- `lexicon.json`: 652 entries, audit `PENDING`.

**R_COMP selection** (`work/select_log.json`):

- 250 main sentences, split by length bin 77 / 87 / 86 (25-29, 30-34 and ≥35 words).
- Template counts are T1 29, T2 28, T3 28, T4 28, T5 28, T6 28, T7 28, T8 25 and T9 28.
- The pool before selection has 5,109 filtered compositions.

**Disguise guard:** 0 mismatches over 125 pairs.
