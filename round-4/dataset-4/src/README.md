# E2: fresh, untouched NL→FOL faithfulness confirmation set

run_u75jRHUss0zo · invention iteration 4 · artifact `gen_art_dataset_4` (plan `gen_plan_dataset_1_idx3`).
Workspace (absolute): `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4`

E2 is the first NL→FOL confirmation set that no earlier decision in this run has touched. It is disjoint from dataset
E's 700 sentences, the screen, FOLIO, the calibration items and the few-shot exemplars, and from any sentence sharing a
12-gram with an E sentence. It concentrates on the strata where iteration 3 was null: long, heavily conditioned sentences
(L25) and exception sentences (EXC). It adds a domain-transfer slice (DT) from ProverQA, whose gold FOL is built with a
prover. It is labelled by EXACTLY dataset E's protocol: E's code is copied byte-identical and hash-frozen
(`code_freeze.json`). The only code change is the transport-only base-URL fix (D0).

**No metric is computed here. Iteration-4 experiments must not read E2.** Read `dataset_card.md` first.

## Status

**PARTIAL.** The run-level OpenRouter budget for the "Test idea" phase ($7.00, shared by all concurrent artifacts)
was exhausted at 07:26 UTC, after this artifact had spent $0.24. The proxy refuses every paid call, the budget does not
reset during the run, and only the user can raise it (Configure). Details are in `dataset_card.md` §0.

Done ($0 steps and the pilot):
- The complete frozen design:
  - 550 active sentences (L25 350, EXC 100, DT 100), plus the ranked L25 surplus order (98) and the DT reserve (10);
  - pre-registration `prereg_E2.json` (sha256 in `prereg_E2.sha256`, frozen before any generation);
  - `census_E2.json` and `exclusion_log_E2.json`.
- The 30-sentence pilot:
  - 300 real candidates from E's 10 few-shot generator slots, plus 30 gold-as-system rows;
  - solver-labelled by E's frozen labeller: equivalence classes, z3 equivalence modulo vocabulary, minimal typed repair;
  - VEX flags, the seal, and a verified `full_data_out.json`.
- A partial panel drift check: all 77 synthetic gate items replayed (majority agreement with E's stored votes 0.974);
  the 96 track-H pairs were cut off by the budget.

Pending (needs budget): the remaining 5,200 generations, the whole blind panel (reference audit, adjudication, tier B),
reference repair, the rest of the drift check, and rename controls (they need final-CORRECT rows).
**Resume with `bash src_e2/run_all.sh`.** Every step is resumable, and paid work is never re-billed. The projected
total is $6.8, about 2.5 h of wall time.

In the current state no confirmation cell is testable (`testability_E2.json`). Without panel votes, E's final rule
leaves every non-equivalent auto class UNRESOLVED. On MALLS, as in E, plain z3 equivalence to the gold almost never
holds, which is why the panel is needed.

## Layout
| Path | What |
|---|---|
| `full_data_out.json` | **THE DATASET** (aii-json `exp_sel_data_out`, validated). Groups: `e2_candidates` (LLM rows), `e2_gold_as_system`, `e2_controls` (omitted while empty), `e2_sentences` (all 550 active sentences with references and status), `e2_panel_drift` (replayed items, E's stored votes vs today's). Every row carries `metadata_source_verified`. |
| `mini_data_out.json`, `preview_data_out.json` | 3 rows per group; the preview truncates strings to 200 chars |
| `candidates_E2_nolabels.jsonl`, `controls_E2_nolabels.jsonl` | **What iteration 5 scores**: no label, no reference, no label-derived field, no gold-as-system row |
| `sealed/labels_E2.jsonl`, `sealed/references_E2.jsonl`, `seal.json` | Sealed labels and references, and the sha256 of every sealed file. Verify with `src_e2/verify_seal.py`. |
| `prereg_E2.json` (+ `.sha256`) | Pre-registration: sources and revisions, strata and ladders, targets, seed, slots, panel, E's tier and testability rules verbatim, drift stop rule, budget caps, shrink and surplus rules, deviations D0-D3 |
| `code_freeze.json` | sha256 of every copied E / dataset-3 file next to its original (all identical), plus the D0 diff |
| `census_E2.json`, `exclusion_log_E2.json` | Supply per pool and ladder rung, exclusion sources, 12-gram drops, the E cross-check |
| `panel_drift_E2.json` | Drift check (status INCOMPLETE; replayed-item agreement) |
| `pilot_projection.json` | Cost-only projection and the surplus decision |
| `testability_E2.json` | Per stratum × regime (R_AB, R_A, R_VEX, R_A_UNAUDITED) counts, testability and MDE80 |
| `reproducibility.md` | What was actually run, in order, with versions, hashes and the resume command |
| `dataset_card.md` | Datasheet: status, composition, exclusion, label counts, testability, drift, parse rates, DT source, cost, corrected power statement, seal, deviations, licences |
| `data.py` | Builds `full_data_out.json` / mini / preview from `work/assembled_E2.json` and re-verifies every row against `temp/datasets/` |
| `src/`, `labeller/`, `prompts/`, `tests/` | Dataset E's frozen code, byte-identical (D2: copied to `./src` because its ROOT-relative paths need that layout); `src/or_client.py` has the D0 fix |
| `src_d3/` | Dataset 3's `perturb.py` / `common.py` (rename controls), byte-identical |
| `src_e2/` | E2 code: `select_e2.py` (step 1), `prereg_e2.py` (2), `drift_report.py` (3), `gen_retry.py` (D4), `pilot_projection.py` + `activate_full.py` (4), `vex.py` (6), `repair.py` (7b), `assemble_e2.py` (7d), `controls_e2.py` (8), `testability_e2.py` (9), `seal_e2.py` + `verify_seal.py` (10), `card_e2.py` (12), `compat.py` + `e.py` (D1 shim and runner), `run_all.sh` (resume), `probe.py`, `key_poll.sh` |
| `E_ref/` | Read-only copies of E's reference files (prereg_strata, gate results, track-H rows, E's sentences, lock files) |
| `raw/generations.jsonl` | Every generator response (append-only; the later record of a duplicate key wins) |
| `cost_ledger.jsonl` | One line per OpenRouter call |
| `work/` | `pool_E2.json` (ranked pools), `sentences_E2_active.json` (active set), `sentences_pilot.json`, `sentences.json` (the file E's scripts read), `labels_heldout.jsonl`, `panel_cache.jsonl`, `gate_results.json`, `trackh_panel_rows.json`, `assembled_E2.json`, `controls_E2.json`, `models_snapshot_E2.json` |
| `data_local/` | Byte-identical copies of E's MALLS-v0.1 train/test, DSAVlab curated sets, folio-refined |
| `temp/datasets/` | Symlinks to the sources `data.py` verifies against |
| `logs/` | Run logs, the key-status poll log, D0 diff, pip freeze |

## How to run
```
bash restore.sh                                   # venv (E's pins), WordNet, HF sources, parser regression test
.venv/bin/python src_e2/select_e2.py              # step 1 (already frozen: DO NOT rerun after prereg)
.venv/bin/python src_e2/prereg_e2.py              # step 2 (refuses to overwrite)
bash src_e2/run_all.sh                            # steps 3-12, resumable; needs OPENROUTER_API_KEY / OPENROUTER_BASE_URL
```
`AII_HARD_CAP` (default 9.5) is the cumulative spend stop. Phase caps are in `prereg_E2.json`.

## Restoring removed files
Everything marked `delete` in `.aii/manifest.yaml` is restored by `bash restore.sh`:
- `.venv/` (regenerable): `uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r pyproject.toml`
- `nltk_data/` (redownloadable): `.venv/bin/python -c "import nltk; [nltk.download(p, download_dir='nltk_data') for p in ('wordnet','omw-1.4')]"`
- `raw/hf/` (redownloadable): ProverQA dev/train at revision `e2561beed450272690da658d21ae667570dbbafc`, and
  tasksource/folio v2 train/validation at revision `295b95fb4fe9be4ff3f933b73142d142cf6b2c97` (the commands are in `restore.sh`).
  `temp/datasets/` symlinks point into it.
- `src/__pycache__/`, `src_e2/__pycache__/`, `src_d3/__pycache__/`, `labeller/__pycache__/`, `tests/__pycache__/` (regenerable):
  Python bytecode, recreated on import.
- `.pytest_cache/` (regenerable): `.venv/bin/python -m pytest -q -c pytest.ini tests/test_fol.py`

## Licences
MALLS-v0.1: CC-BY-NC-4.0. ProverQA: no licence field on its HF card (see the ProverGen repository). Generator outputs are
under their providers' terms.
