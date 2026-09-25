# Reproducibility: CSC on PERTURB and R_COMP (iteration 4, gen_art_experiment_10)

This describes what was **actually run** on 2026-09-24 (UTC), including the parts that could not run.

## 0. Important context: what could not run

Every OpenRouter call returned `403 aii_run_budget_exhausted`, because the run-wide "Test idea" budget was exhausted by
other artifacts. `:free` models returned `429` (daily limit). The pre-registered CSC peer sweep (pilot plus
17,075 calls, projected $3.07) therefore **did not run**. This artifact spent $0.0000088 in total, on one 1-token probe
(`results/api_cost_ledger.jsonl`). Every number below comes from $0 arms: SIGPROXY, FREE3, exp-8 free consensus, typing
and LOCAL2. To run the missing part, raise the budget and follow step 5b.

## 1. Copy the artifact

```bash
cp -r . ~/csc && cd ~/csc
```
The code reads these inputs **read-only by absolute path**. To reproduce elsewhere, place them at the same paths:
* `iter_3/gen_art/gen_art_experiment_8/{data/perturb_rows.jsonl, results/perturb_scores.jsonl, results/invariance_table.csv, results/analysis_typing.json, src/, tests/, data/nltk_data/}`
* `iter_3/gen_art/gen_art_experiment_7/{results/rcomp_candidates.jsonl, results/analysis_rows_SIG.jsonl, rcomp/work/rcomp_sentences.json, src/auc_tools.py, src/consensus_rcomp.py}`
* `iter_2/gen_art/gen_art_dataset_3/full_data_out.json` (perturb_suite, rcomp_sentences)
* `iter_1/gen_art/gen_art_dataset_1/{full_data_out.json, prompts/fewshot_v1.txt}`
* `iter_4/gen_art/gen_art_experiment_9/results/pilot.json`, used only for the cost projection

All paths are under `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/`. Exp 7's `results/free_labels.jsonl`
is **never** opened (firewall).

## 2. System, Python, environment

* **Hardware:** Debian 12 container; 4 vCPU (AMD EPYC 9655P, cpuset); 29 GB RAM cgroup limit; **no GPU**. The host was
  heavily loaded (load average about 300–350), which slowed the llama.cpp step considerably.
* **Software:** Python 3.12.14 and uv. No other system packages.

```bash
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r requirements.txt          # = pyproject.toml pins, minus llama-cpp-python
uv pip install --python .venv/bin/python "llama-cpp-python==0.3.35" --only-binary llama-cpp-python \
    --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
```
Key pins (all 50 are in `pyproject.toml`): z3-solver 5.1.0.0, numpy 2.5.3, pandas 3.0.6, scikit-learn, scipy, loguru,
aiohttp, nltk, pytest, huggingface_hub, llama-cpp-python 0.3.35.

## 3. Downloads, environment variables, keys (names only)

* **Environment variables:** `OPENROUTER_API_KEY`, `OPENROUTER_BASE_URL` (all API calls; never hard-code the URL), and
  `HF_HOME` (shared cache; leave as provided).
* **Local GGUF models** (LOCAL2 arm only). They are not stored in this folder (each exceeds 100 MB); `src/local_peers.py` downloads a missing one on demand (`ensure_model`) into `models/`, and so does `./restore.sh`. Note: a later test of that download also cached 43 more gemma calls in `data/local_llm_cache.jsonl`. The reported LOCAL2 numbers use the 27-base `data/peers_local2.jsonl` and `data/local2_bases.json`; rerunning `--finalize` now yields 32 bases and slightly different LOCAL2 numbers.
  * `Qwen/Qwen2.5-1.5B-Instruct-GGUF/qwen2.5-1.5b-instruct-q4_k_m.gguf`
  * `bartowski/gemma-2-2b-it-GGUF/gemma-2-2b-it-Q4_K_M.gguf`
  * `bartowski/Llama-3.2-1B-Instruct-GGUF/Llama-3.2-1B-Instruct-Q4_K_M.gguf`, which was used only in a 3-prompt smoke
    test and then dropped
* **NLTK data** for the vendored NF aligner (vendored exp-8 tests only): copy exp 8's `data/nltk_data` to
  `src/data/nltk_data/`.
* `./restore.sh` performs steps 2 and 3.

## 4. Commands actually run, in order (times are wall-clock on the hardware above)

| # | command | what | time |
|---|---|---|---|
| 1 | `.venv/bin/python src/views.py` | data views; asserts 4,234 / 868 / 300 (200 E + 100 R_COMP); `sig_sharing.csv`; firewalled FREE view; FREE3 peers | ~1 min |
| 2 | `.venv/bin/python -m pytest -q tests/test_csc_lib.py` | 45 unit tests (all pass) | ~80 s |
| 3 | `.venv/bin/python src/peers_run.py pilot` | pilot: **all 120 calls returned 403** (outputs moved to `logs/peers_pilot_all_failed.jsonl`) | seconds |
| 4 | `.venv/bin/python src/csc_prereg.py` | freeze `results/prereg_csc_P.json`, sha256 `7cb4e5d6…43a8` | seconds |
| 5 | `.venv/bin/python src/csc_score.py --mini 12`, then `.venv/bin/python src/csc_score.py` | SIGPROXY / FREE3 scores for 7,612 rows (3 spawn workers, z3 2 s timeout) | 2 min |
| 6 | `.venv/bin/python src/csc_typing.py --mini 120 --which oracle,proxy,free3`, then `--which oracle,proxy,free3` | 6,272 same-vocabulary repair searches (6 s budget each) | 14 min |
| 7 | `.venv/bin/python src/csc_manifest.py` | iteration-5 job list (`data/csc_jobs.jsonl`) + `firewall.json` | 1 min |
| 8 | `.venv/bin/python src/local_peers.py --limit 6`, then `.venv/bin/python src/local_peers.py` (under `timeout 6000`), then `.venv/bin/python src/local_peers.py --finalize` | LOCAL2 peers at temperature 0 (n_ctx 4096, 4 threads, max 300 tokens) for 40 seeded bases. The run hit its 6,000 s timeout; finalize kept the **27 complete bases** (209 signatures) | ~1 h 50 min |
| 9 | `.venv/bin/python src/csc_score.py --local` | LOCAL2 scores (486 rows) | 15 s |
| 10 | `.venv/bin/python src/csc_analysis.py && .venv/bin/python src/csc_tables.py` | all tables (verifies the prereg sha256 first), bootstrap B = 2000, seed 0 | ~1 min on an idle CPU |
| 11 | `.venv/bin/python src/csc_output.py` | `perturb_csc_scores.jsonl`, `csc_rcomp_sig_scores.jsonl`, `method_out.json` | 30 s |
| 12 | `.venv/bin/python tests/rederive.py` | independent re-derivation: 429 checks, 0 mismatches | 20 s |
| 13 | `.venv/bin/python tests/rederive_headline.py` | headline numbers from raw files, with placebos | ~1 min |
| 14 | `.venv/bin/python -m pytest -q tests/` | 73 passed, 1 skipped (live API test). Run on an idle CPU: under load, z3's 2 s timeouts produce UNKNOWN verdicts in exp 8's NF tests | ~100 s |
| 15 | aii-json `aii_json_validate_schema.py --format exp_gen_sol_out` and `aii_json_format_mini_preview.py --input method_out.json` | schema PASSED; full / mini / preview files written | seconds |

`method.py` wraps these stages: `.venv/bin/python method.py --stage all` runs every $0 stage and skips the API stages
when the key probe fails.

**5b. When the budget exists:**
```bash
.venv/bin/python method.py --stage pilot,peers,score,typing,manifest,analysis,output,rederive
```
The run is cached and resumable, with a hard stop at $9.5.

Seeds and determinism:
* Bootstrap seed 0 (B = 2000); LOCAL2 base draw `random.Random(0)`; llama.cpp `seed=0`, temperature 0.
* The symbol-list shuffle is seeded by `sha1(text | signature)`, so the same prompt bytes are produced across processes
  (tested).
* The fingerprint uses Python's `hash`, only within a process, so it is independent of PYTHONHASHSEED.

## 5. What a reader should get (`results/tables.md`; T-numbers refer to it)

* **T1** `sig_sharing.csv`:
  * signature-preserving (100% share the base signature): ADD_INTERNAL, CONN, NEG, QUANT, RESTR, REV, SWAP, MOVE and the
    equivalence controls;
  * always new: ADD_FOREIGN, MEANING_RENAME, RENAME_*;
  * BIND is 6% shared and DROP 2%;
  * 2,254 unique signatures.
* **T2/T3:** SIGPROXY on 1,196 R_COMP mutants: e = 0.000, recall 1.000; recall given base endorsed = 1.000 (n = 1,030).
  Exp 8 `c_align` e on E = 0.001.
* **T4/T4b:** on the same 74 R_COMP bases, d is 0.149 for SIGPROXY K3 and 0.757 for FREE3-ALIGN, a difference of −0.608
  [−0.716, −0.500]. `c_align` d by E word tercile is 0.47 / 0.80 / 0.91.
* **T5:** SIGPROXY rename FA = 1.000 (base-signature cue); equivalence rewrites have flip rate 0.
* **T6 typing strict:**
  * ORACLE_samevocab E 0.928 [0.919, 0.937];
  * SIGPROXY majority, R_COMP: 0.784 [0.711, 0.849];
  * FREE3 majority, E: 0.123.
* **T7 SIG within-template AUROC** (2,024 rows):
  * SIGPROXY k = 3 0.930 [0.916, 0.943], c_score_sig 0.952, disguised judge 0.587;
  * SIGPROXY k = 3 minus c_score_sig: −0.022 [−0.036, −0.008].
* **T9 LOCAL2 usage rates:** GENUINE 0.814, SYNONYM 0.696, FOREIGN 0.112, DONOR 0.160, NONCE 0.143. Δanchor = 0 for
  ADD_FOREIGN and MEANING_RENAME (98 usable rows).
* **T10:** projected CSC FULL cost $0.000599 per candidate (K3); MARGINAL z3 median 0.051 s.
* **T11:** G3-P, G4 and MT are UNTESTED; G5 PASSES (projected).

Small numeric differences are possible for LOCAL2 (llama.cpp threading) and for z3 UNKNOWN verdicts on a loaded CPU.
All other numbers are deterministic.
