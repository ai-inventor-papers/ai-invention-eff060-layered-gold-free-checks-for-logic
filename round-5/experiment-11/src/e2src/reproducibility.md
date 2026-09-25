# Reproducing E2 (gen_art_dataset_4): fresh NL→FOL faithfulness confirmation set

This file records what was **actually run** (2026-09-24, 07:10–07:45 UTC), in order, and how to finish it.
E2 is **partial**. The run-level OpenRouter budget for the "Test idea" phase ($7.00, shared by all concurrent
artifacts) was exhausted at 07:26 UTC, after this artifact had spent $0.24. Every later paid call was refused with
`HTTP 403 aii_run_budget_exhausted`. All API stages are resumable and cached (`raw/generations.jsonl`,
`work/panel_cache.jsonl`, `raw/reference_repair.jsonl`), so a reproduction that keeps `raw/` and `work/` re-bills
nothing and gets identical rows. A reproduction from scratch re-calls the models at temperature 0; provider-side
non-determinism can then change individual outputs.

## 1. Copy the artifact

```bash
cp -r ../../../../round-4/dataset-4/src ~/e2
cd ~/e2
```
Every script derives its paths from its own file location (`ROOT = Path(__file__).resolve().parents[1]`). Four
read-only inputs are referenced by absolute path and must stay reachable:
- dataset E: `../../../../round-1/dataset-1/src`
  (its 700 sentences, calibration items, panel cache and track-H rows for exclusion and the drift check);
- the screen: `.../round-1/experiment-1/src/screen_items.json`;
- dataset 3: `.../round-2/dataset-3/src`, whose code is already copied into `src_d3/`.

## 2. System, Python and libraries

- Linux (Debian 12 container, kernel 6.17), **Python 3.12.14**, **uv 0.6.14** (`pip` is not used).
- Hardware used: 4 CPU cores (AMD EPYC 9655P, cgroup quota), 29 GB RAM, no GPU. Everything is CPU-only.
- Environment: pins are exactly `pyproject.toml`, identical to `uv pip freeze` of the venv that ran
  (`logs/pip_freeze.txt`) and to dataset E's pins. Key pins: z3-solver 5.1.0.0, nltk 3.10.3, aiohttp 3.14.3,
  loguru 0.7.3, huggingface-hub 1.32.0, numpy 2.5.3, pandas 3.0.6.
  ```bash
  bash restore.sh     # .venv from pyproject.toml, NLTK wordnet + omw-1.4, HF sources, parser regression test
  ```

## 3. Data, models, environment variables

- MALLS-v0.1 train/test: `data_local/` (byte-identical copies of dataset E's files; sha256 in `code_freeze.json`).
- ProverQA: `opendatalab/ProverQA` revision `e2561beed450272690da658d21ae667570dbbafc`, `dev/{easy,medium,hard}.json`.
- FOLIO v2 (exclusion only): `tasksource/folio` revision `295b95fb4fe9be4ff3f933b73142d142cf6b2c97`.
- Generator slots (temperature 0, max_tokens 600, `prompts/fewshot_v1.txt`, sha1 a1c7ae39…): G1 llama-3.1-8b-instruct,
  G1b llama-3.3-70b-instruct, G2 qwen3-235b-a22b-2507, G3 mistral-small-3.2-24b-instruct, G4 deepseek-v3.2 (reasoning
  off), G5 gemma-3-27b-it, G6 phi-4, G7 gpt-4.1-mini, G8 gemini-2.5-flash (reasoning max_tokens 0), G9 command-r7b-12-2024.
- Panel: P1 anthropic/claude-haiku-4.5, P3 z-ai/glm-4.6 (reasoning off), R1 moonshotai/kimi-k2-0905; E's prompt v2.
- Environment variables: `OPENROUTER_API_KEY`, `OPENROUTER_BASE_URL` (all calls go through the base URL; deviation D0),
  optional `AII_HARD_CAP` (default 9.5, the cumulative-spend stop in `src/or_client.py`).

## 4. Commands, in the order they were run

```bash
# step 0: copy E's code byte-identical, record hashes, apply D0 (base-URL fix), parser tests  -> code_freeze.json
.venv/bin/python -m pytest -q -c pytest.ini tests/test_fol.py                       # 5 passed
.venv/bin/python src_e2/probe.py                                                     # 1-token key probe: OK
# step 1-2 ($0): selection, census, pre-registration (frozen 07:24 UTC, BEFORE any generation)
.venv/bin/python src_e2/select_e2.py        # -> work/pool_E2.json, work/sentences.json, census_E2.json, exclusion_log_E2.json
.venv/bin/python src_e2/prereg_e2.py        # -> prereg_E2.json + prereg_E2.sha256
# step 3 (drift) and step 4 (pilot), concurrently
.venv/bin/python src_e2/e.py gate.py --mode synthetic --members P1,P3,R1 --cap 0.30     # 77/77 items replayed
.venv/bin/python src_e2/e.py gate.py --mode trackh --members P1,P3,R1 --cap 0.50        # cut off by the budget stop
.venv/bin/python src_e2/drift_report.py                                                  # -> panel_drift_E2.json (INCOMPLETE)
.venv/bin/python src_e2/e.py generate.py --slots G1,G1b,G2,G3,G4,G5,G6,G7,G8,G9 --variants fewshot_v1 \
      --sentences work/sentences_pilot.json --cap 1.3                                    # 300 calls, $0.027
.venv/bin/python src_e2/gen_retry.py --sentences work/sentences_pilot.json --concurrency 3   # 11 phi-4 HTTP-429 retries (D4)
.venv/bin/python src_e2/e.py run_label.py --kind heldout --budget 8 --workers 4          # 30 sentences, 182 s
# --- budget stop at 07:26 UTC: the pilot panel, reference repair and full generation could not run ---
.venv/bin/python src_e2/assemble_e2.py      # E's final_rule without votes -> work/assembled_E2.json
.venv/bin/python src_e2/controls_e2.py      # 0 controls (no final-CORRECT rows without the panel)
.venv/bin/python src_e2/testability_e2.py   # -> testability_E2.json (no cell testable)
.venv/bin/python src_e2/seal_e2.py && .venv/bin/python src_e2/verify_seal.py   # seal_intact: true
.venv/bin/python src_e2/pilot_projection.py # cost-only projection: $6.79 -> surplus rule adds the 98 L25 surplus sentences
uv run data.py                              # -> full_data_out.json, mini_data_out.json, preview_data_out.json (schema PASSED)
.venv/bin/python src_e2/card_e2.py          # -> dataset_card.md
```

To **finish E2** once the budget is raised (resumable; projected ≈ $6.8 total and ≈ 2.5 h wall time):
```bash
bash src_e2/run_all.sh
```

## 5. What you should get (current, partial state)

| file | sha256 (prefix) | content |
|---|---|---|
| `prereg_E2.json` | 36957fcb5b468122 | frozen before any generation |
| `code_freeze.json` | 986334dc05d1c2be | 54 copied files identical to their originals + the D0 diff |
| `work/pool_E2.json` | 98cdccffa55226db | ranked pools: EXC 100, L25 350 base + 98 surplus, DT 100 + 10 reserve |
| `candidates_E2_nolabels.jsonl` | a220238626e2fbe2 | 300 pilot candidate rows, no labels |
| `sealed/labels_E2.jsonl` | 00c2592c8c648c17 | 330 sealed labels (300 LLM + 30 gold-as-system) |
| `full_data_out.json` | fbfaedcfb7e61850 | e2_candidates 300, e2_gold_as_system 30, e2_sentences 550, e2_panel_drift 173 |

- Pilot labels (no panel): ERROR 36 (tier A_unaudited_ref), UNRESOLVED 244, UNPARSEABLE 20, CORRECT 0.
- Drift check: synthetic-gate majority agreement with E's stored votes 0.974 (77 items); track H incomplete.
- No testable cell (`testability_E2.json`). Projected MDE80 after completion: L25 350 → 0.112, 450 → 0.099.
