# Candidate-Signature Consensus (CSC) on PERTURB and R_COMP: anchoring, rename invariance, typing

Run `run_u75jRHUss0zo`, iteration 4, `gen_art_experiment_10` (plan `gen_plan_experiment_2_idx2`, task T6-P).
Workspace: `.`
(every path below is relative to it). Every number in this README is copied from `results/tables.md`, which is generated
from the result files by `src/csc_tables.py`.

## What was planned, and what actually ran

**CSC** (Candidate-Signature Consensus) shows three peer model families (deepseek-v3.2, phi-4, gpt-4.1-mini; qwen3-235b
is the k = 4 arm) the sentence **and the candidate's own symbol list** (name/arity, deterministic shuffle), and asks them
to translate. A peer agrees when its formula is **exactly** z3-equivalent to the candidate after lower-casing names,
with no aligner. `c_csc = 1 − agree/used`, flag at `c > 0.5`. The pre-registered questions were:
1. Does the cue **anchor** peers onto wrong symbols (gate G4)?
2. Does it fix **rename false alarms** (gate G3-P)?
3. Can a same-vocabulary typed repair against the peer majority **identify the error type** (gate MT)?

**Deviation D-BUDGET (decisive).** Before the first pilot call, every OpenRouter request returned
`403 aii_run_budget_exhausted`. The run-wide "Test idea" budget ($7.00) had already been spent by other artifacts: $7.03
at 07:26 UTC, and the proxy says it does not reset during the run. `:free` models were also exhausted (daily 1,000-request
limit, resetting about 16.7 h later). This artifact spent **$0.0000088** in total, on one 1-token probe
(`results/api_cost_ledger.jsonl`). As a result:

* **G3-P, G4 and MT(E) are UNTESTED.** They are neither passed nor failed (`results/csc_gate_P.json`). No local model
  was substituted for the pre-registered peers, as the plan's fallback requires.
* The complete pipeline is built, unit-tested and **ready to run** once the budget is raised:
  `python method.py --stage peers,score,typing,manifest,analysis,output,rederive`. The job list is
  `data/csc_jobs.jsonl` (17,075 calls). Its projected cost is **$3.07** ($3.38 with a ×1.1 margin), using per-call prices
  the sibling exp 9 measured with the identical block template and model ids (`results/csc_job_manifest.json`).
* Everything that could be measured at $0 was measured, with each arm labelled in every table:
  * **SIGPROXY.** Signature-cued outputs from exp 7's SIG condition for the **same four families**, covering the 77
    R_COMP bases that exp 7 also translated. The cue there is the base/template signature in a closed, glossed block, not
    the candidate's own open list. Same K3/K4 rule, exact equivalence and thresholds.
  * **SIGPROXY on SIG.** A k = 3 family-matched ablation of signature-cued consensus on exp 7's labelled SIG rows.
  * **FREE3.** The matched-resource **uncued** baseline: the same three families' few-shot outputs, without a cue.
    Dataset E slots G4/G6/G7 for E bases; exp 7 FREE rows for R_COMP bases.
  * **Exp 8's free-peer consensus** (`c_align`, `c_hyb`) and the flash-lite judge, joined from exp 8 per row.
  * **ORACLE_samevocab** typing (the same-code ceiling).
  * **LOCAL2.** A labelled *secondary* arm: two small local peers (qwen2.5-1.5b, gemma-2-2b; llama.cpp on CPU) receive
    the **same CSC prompt bytes** on 40 E bases. It measures the anchoring *mechanism* only, never a gate.

The prereg (`results/prereg_csc_P.json`, sha256 in `prereg_csc_P.sha256`) was frozen before any score was joined to an
operator or label, with the deviation and the $0 arms written into it. `src/csc_analysis.py` verifies the hash before it
runs.

## Key structural fact (computed, `results/sig_sharing.csv`)

Some operators keep the base's signature on 100% of rows: ADD_INTERNAL, CONN, NEG, QUANT, RESTR, REV, SWAP, MOVE and every
z3-equivalent rewrite control (REORDER_*, CONTRAPOSITIVE, DEMORGAN). For these rows the CSC peers **are** the base's
peers. A peer that endorses the (correct) base cannot also endorse a z3-non-equivalent mutant, so recall on these
operators is at least the base-endorsement rate, and **anchoring cannot act on them**.

Anchoring can act only through **new** symbols:
* ADD_FOREIGN, MEANING_RENAME, RENAME_SYN and RENAME_NONCE are 100% new;
* BIND is 94% new (it binds constants) and DROP 98%.

Only these rows need their own peers: 2,254 unique (text, signature) pairs out of 5,402 rows.

## Results (all from `results/tables.md`)

**1. Mutant endorsement e and recall (T2/T3; flag at c > 0.5; base-clustered bootstrap).**
* **SIGPROXY on 1,196 R_COMP mutants:** e = 0.000, so recall = 1.000 on every operator; at c == 1, recall = 0.999.
* **Conditional on the base being endorsed** (1,030 rows), recall = 1.000. This is the conditional recall the reviewer
  audit asked for, because within-base AUROC is banned.
* **Caveat:** for new-signature mutants these peers were cued with the *base* signature. Their e is therefore the
  "base-signature peers" term of Δanchor (≈ 0, as predicted), not a test of anchoring.
* **Free comparators:** exp 8 `c_align` on E mutants gives e = 0.001, FREE3 gives e ≈ 0. The free e is ≈ 0 by
  construction, because free peers never saw the mutant: the peer-asymmetry confound named in the plan. The flash-lite
  judge endorses 12.4% of E mutants and 4.8% of R_COMP mutants.

**2. False alarms on correct bases, d (T4, T4b).**
* On the same 74 long R_COMP bases (≥ 25 words), the same three families flag **d = 0.149** when cued (SIGPROXY K3)
  against **0.757** uncued (FREE3-ALIGN). The paired difference is **−0.608 [−0.716, −0.500]** (base bootstrap).
  Uncued FREE3-exact flags 0.986 (−0.838 [−0.919, −0.743]).
* Mutant recall is identical: 1.000 cued and uncued, on 1,148 rows (`results/paired_cue_effect.csv`).
* The cue therefore removes most vocabulary-driven false alarms without losing recall on these synthetic errors. Caveat:
  this cue is a closed, glossed template vocabulary.
* Cue-free d **grows with length on E**: exp 8 `c_align` d = 0.47 / 0.80 / 0.91 over the word terciles, with a logistic
  slope of +1.52 per 10 words [1.12, 2.08]. SIGPROXY's d on R_COMP shows no length trend (slope CI spans 0).

**3. Controls (T5).**
* Signature-preserving z3-equivalent rewrites keep the base verdict exactly under SIGPROXY: FA equals base FA and the
  flip rate is 0.000. The sanity check confirms per-peer verdicts are 100% identical.
* **Renames under a BASE-signature cue:** FA = 1.000 (RENAME_SYN / RENAME_NONCE, R_COMP). This is expected, because peers
  cannot use names they were never shown. It shows that rename invariance *requires* re-cueing with the renamed
  candidate's own list, which is exactly the untested CSC design (G3-P).
* Exp 8's reference rows are cited in T5: `c_align` SYN 0.565 / NONCE 0.765, `c_hyb` 0.298 / 0.216.

**4. Error-type identification (T6; same-vocabulary typed repair, depth ≤ 2).**

| target | rows | strict accuracy [95% CI] |
|---|---|---|
| ORACLE_samevocab (true base reference), E | 2,688 | **0.928** [0.919, 0.937] |
| ORACLE_samevocab, R_COMP | 1,546 | 0.909 [0.900, 0.919] |
| SIGPROXY K3 peer-majority, R_COMP | 1,196 | **0.784** [0.711, 0.849] |
| FREE3 (uncued, same families) majority, E | 2,688 | 0.123 [0.081, 0.169] |
| FREE3 majority, R_COMP | 1,196 | 0.000 |

* The ORACLE_samevocab recomputation (0.928 on E) replaces exp 8's 0.802 oracle. It adds SUBST (for MEANING_RENAME) and
  ADD_ANY, and it uses no aligner.
* On the same 1,196 R_COMP rows, the oracle scores 0.914 and the majority class 0.186.
* The FREE3 target is usually missing: in 75% of E rows (82% of R_COMP rows) the uncued peers have no majority.
* Exp 8 baselines (cited): majority class 0.177, ALIGN-medoid typing 0.328, flash-lite judge 0.326.
* Only a signature-cued peer majority makes same-vocabulary typing work. MT's pre-registered 0.55 bar is met
  **descriptively** by the R_COMP proxy, but MT itself (CSC majority on E) is **UNTESTED**.

**5. Labelled SIG check (T7; development only, controlled vocabulary).** Within-template AUROC on 2,024 rows
(429 ERROR, 221 sentences), comparing against exp 7's 9-peer `c_score_sig` and the judges:

| metric | within-template AUROC [95% CI] | paired Δ vs c_score_sig |
|---|---|---|
| SIGPROXY k = 3 | **0.930** [0.916, 0.943] | −0.022 [−0.036, −0.008] |
| SIGPROXY k = 3, graded | 0.938 [0.926, 0.950] | −0.014 [−0.029, 0.002] |
| c_score_sig (9 peers, exp 7) | 0.952 [0.936, 0.966] | — |
| flash-lite judge, disguised / original | 0.587 / 0.673 | — |

* SIGPROXY k = 3 beats the disguised flash-lite judge by +0.346 [0.306, 0.383].
* At c > 0.5: e = 0.000, d = 0.176. By matched reading, d is 0.046 on weak-reading correct rows and 0.956 on
  strong-reading correct rows, so the remaining false alarms are valid minority readings.
* Three peers of these families retain most of the nine-peer signal.

**6. Cost (T10).**
* **Projected CSC FULL cost** is $0.000599 per candidate for K3 and $0.000719 for K4, measured by the sibling with
  identical prompts. That passes G5 (≤ $0.002), labelled "projected".
* **SIGPROXY's actual peer cost** is a median of $0.000497 per candidate.
* **MARGINAL cost** is z3 CPU only: a median of 0.051 s per candidate, p90 0.111 s.

**7. LOCAL2 anchoring mechanism (T9; secondary: qwen2.5-1.5b and gemma-2-2b, same CSC prompt bytes, k = 2).**
* **Coverage.** 27 of 40 seeded E bases were completed before the CPU deadline. A later test of the on-demand weight download also cached 43 more gemma calls; they are in `data/local_llm_cache.jsonl` but NOT in the reported numbers, which use `data/peers_local2.jsonl` (27 bases) (209 signatures, 486 rows). Calls slowed
  to 90–130 s under host load, and the job hit its own 6,000 s timeout. 158 rows have fewer than 2 parseable local peers.
* **Symbol usage by role.** Listed GENUINE symbols are used 0.814 of the time and SYNONYM renames 0.696. Wrong-meaning
  symbols are mostly refused: FOREIGN 0.112, DONOR 0.160, NONCE 0.143.
* **Copying never produced the mutant.** When a peer did use the foreign or donor symbol, its formula was equivalent to
  the mutant **0 of 25** times.
* **Within-sentence contrast.** On the 98 new-signature rows where both peer sets are usable, e is 0.000 with both
  own-signature and base-signature peers for ADD_FOREIGN, MEANING_RENAME and RENAME_*, so Δanchor = 0. DROP has
  Δanchor +0.083 [−0.167, 0.333] (n = 12).
* **Interpretation.** No anchoring-driven endorsement was observed, but power is low: these small peers endorse only
  0.30 of the correct bases. This is mechanism evidence, not a G4 verdict.
* **Controls.** Rename controls under own-signature local peers: FA 0.692 (SYN, n = 13) and 0.500 (NONCE, n = 14),
  against paired base FA 0.462 / 0.214 (T5).

## Gates (`results/csc_gate_P.json`)

| gate | verdict |
|---|---|
| G3-P (RENAME_SYN FA ≤ base FA + 0.05) | UNTESTED (D-BUDGET) |
| G4 (CSC e ≤ free e + 0.05 on ADD / DROP / MEANING_RENAME) | UNTESTED (D-BUDGET) |
| MT (strict typing ≥ 0.55 on E) | UNTESTED (D-BUDGET); proxy on R_COMP 0.784 (descriptive) |
| G5 (FULL ≤ $0.002 per candidate) | PASS (projected, $0.000599) |

## Layout

| path | what |
|---|---|
| `method.py` | orchestrator: `--stage views,tests,pilot,prereg,peers,local,score,typing,manifest,analysis,output,rederive` or `all` (API stages are skipped when the key has no budget) |
| `src/csc_lib.py` | **library**: `extract_signature`, `csc_prompt`, `parse_peer`, `eq_exact`, `consensus_score` (CSC), `csc_multi_score`, `graded_consensus` (identity pair records), `peer_majority`, `symbol_usage`, `typed_repair_same_vocab`, `peer_assignment`, `csc_peers` (dry-run or live) |
| `src/views.py` | STAGE 1: data views, signatures, `sig_sharing.csv`, FIREWALLED FREE projection (`project_free`, `FreeRow`), FREE3 peers |
| `src/or_client.py`, `src/csc_budget.py` | async OpenRouter client (cache, retries, KeyLimit), append-only ledger with $9.5 hard stop |
| `src/peers_run.py` | STAGES 3 + 5: pilot, sweeps, test-retest (shrink order implemented) |
| `src/csc_prereg.py` | STAGE 4 freeze + `verify()` |
| `src/csc_score.py` | STAGE 6 scoring (CSC / SIGPROXY / FREE3; `--local` for LOCAL2) |
| `src/csc_typing.py` | same-vocabulary typed-repair searches (oracle / csc / proxy / free3 targets) |
| `src/local_peers.py` | LOCAL2 secondary arm (llama.cpp) |
| `src/csc_analysis.py`, `src/csc_tables.py` | STAGE 7 analysis, `tables.md`, `deviations.json` |
| `src/csc_manifest.py` | iteration-5 job manifest + `firewall.json` |
| `src/csc_output.py` | per-row score files + `method_out.json` |
| `src/vendor_x8/`, `src/vendor_x7/` | vendored exp 8 / exp 7 code, byte-identical to the sources (73 files; sha256 + `identical_to_source` in `VENDOR_SHA256.json`) |
| `tests/test_csc_lib.py` | 45 unit tests (signatures, prompt bytes across processes, parser formats, fp prefilter on 200 controls, synonym, meaning-rename, UNKNOWN, multi-reading, typing recovery on 50 mutants per operator, firewall) |
| `tests/test_vendored_x8_consensus_lib.py` | exp 8's own tests rerun against the vendored copy (path line edited). With `tests/test_firewall.py` and `tests/test_csc_lib.py`: 73 passed, 1 skipped (the live API test). Run them on an idle CPU: z3's 2 s timeouts turn into UNKNOWN under heavy load |
| `tests/test_firewall.py` | firewall checks on written files (whitelisted keys only, sha256 matches, no FREE row or label in outputs) |
| `tests/rederive.py` | independent re-derivation with pandas: 429 checks against the reported tables, 0 mismatches, plus a within-base label-shuffle placebo (`results/rederive.json`) |
| `data/perturb_view.jsonl`, `data/unique_sigs_perturb.jsonl` | label-blind PERTURB view (5,402 rows) and its 2,254 unique signatures |
| `data/rcomp_free_view.jsonl` | firewalled FREE projection (whitelisted fields only) |
| `data/rcomp_sig_view.jsonl`, `data/free3_peers.json` | SIG rows (development) and FREE3 peers |
| `data/csc_jobs.jsonl` | every CSC peer job (stage, text, signature, models, prompt sha1) for iteration 5 |
| `data/local_llm_cache.jsonl`, `data/peers_local2.jsonl` | LOCAL2 raw outputs and parsed peers |
| `results/prereg_csc_P.json` (+ `.sha256`) | pre-registration (frozen before any join) |
| `results/perturb_csc_scores.jsonl` | every PERTURB row × every score column (+ base endorsement per variant, typing predictions) |
| `results/csc_rcomp_sig_scores.jsonl` | SIG rows with SIGPROXY scores |
| `results/anchoring.csv`, `d_by_length.csv`, `paired_cue_effect.csv`, `controls_fa.csv` | parts 1–2 |
| `results/typing_csc.csv`, `typing_confusion_csc.csv`, `typing_rows_csc.jsonl`, `typing_search_rows.jsonl`, `typing_summary.json` | part 3 |
| `results/rcomp_sig_csc.json`, `rcomp_free_labelfree.json` | part 4 |
| `results/cost_table.csv`, `csc_job_manifest.json`, `api_cost_ledger.jsonl` | cost |
| `results/local2_anchoring.json` | LOCAL2 anchoring mechanism |
| `results/csc_gate_P.json`, `tables.md`, `deviations.json`, `sanity_checks.json`, `rederive.json`, `firewall.json` | gates, tables, deviations, checks |
| `method_out.json` (+ `full_`/`mini_`/`preview_`) | exp_gen_sol_out: `PERTURB_E_CSC` (3,456), `PERTURB_RCOMP_CSC` (1,946), `RCOMP_SIG_CSC` (2,210); FREE rows excluded |

## For iteration 5 (paths to cite)

* **CSC FREE peer cache:** NOT GENERATED. `results/csc_rcomp_free_peers.jsonl` does not exist.
* **Firewall record:** `./results/firewall.json`.
  It holds the whitelist, the fact that `free_labels.jsonl` was never opened, and the sha256 of the firewalled view.
* **Job list** (the FREE stage has 1,813 unique signatures and 6,712 calls, projected $1.21):
  `./data/csc_jobs.jsonl`.
* **Prompt:** block template sha256 `227e0db8…a460`, prompt file sha256 `cdfd524e…7a9e` (byte-identical to the dataset E
  and dataset 3 copies).

## How to run

```bash
./restore.sh                                              # venv, local GGUF models, NLTK data
.venv/bin/python method.py --stage all                    # $0 stages; API stages run only if the key has budget
.venv/bin/python -m pytest -q tests/test_csc_lib.py       # 45 unit tests
.venv/bin/python tests/rederive.py                        # independent re-derivation
```
Library:
```python
import sys; sys.path.insert(0, "src"); import csc_lib as L
sig = L.extract_signature(candidate_fol)
L.csc_peers(text, sig, dry_run=True)                      # messages + $ estimate; dry_run=False calls OpenRouter
L.consensus_score(text, candidate_fol, peer_fols)         # {'c', 'per_peer', 'n_used', 'n_unknown', 'status'}
L.typed_repair_same_vocab(candidate_fol, peer_majority_fol)
```

## Restoring removed files

`.aii/manifest.yaml` marks two paths for deletion after the round:

| path | restore |
|---|---|
| `.venv/` | `uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r requirements.txt`, then `uv pip install --python .venv/bin/python llama-cpp-python==0.3.35 --only-binary llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu` (both steps are in `./restore.sh`) |
| `__pycache__/` | recreated automatically when Python imports the modules |

Two other inputs are not stored here:
* **Local GGUF weights** (`models/`, git-ignored; only for re-running LOCAL2). They are downloaded on demand by
  `src/local_peers.py`, or by `./restore.sh`.
* **The copy of exp 8's NLTK data** (`src/data/nltk_data/`, only for the vendored exp-8 tests). Restore it with
  `cp -r ../../../round-3/experiment-8/src/data/nltk_data src/data/`
  or `python -m nltk.downloader -d src/data/nltk_data wordnet omw-1.4 words`.
