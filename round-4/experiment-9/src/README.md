# T6-E: Candidate-Signature Consensus (CSC) on development set E

Iteration 4 of the AI Inventor NL→FOL gold-free metric study (run `run_u75jRHUss0zo`). **All numbers are DEVELOPMENT E.** Dataset E was used by earlier rounds to choose consensus, so nothing here is a confirmation.

## What CSC measures

For a sentence `text` and a candidate formula `fol`, 3 cheap peer LLMs from families other than the candidate's (pool: DeepSeek-V3.2 with reasoning off, Phi-4, GPT-4.1-mini, Qwen3-235B-2507) translate `text`. They use the dataset-E few-shot prompt, byte-identical (sha256 `cdfd524e…`), plus one extra block: the candidate's own predicate and constant symbols as `Name/arity`, in seeded random order. Then:

```
c_csc(x) = 1 − (share of parseable family-disjoint peers whose formula is z3-equivalent to x.fol,
               with symbols identified by lowercased name + arity; no aligner)
```

Higher means more likely ERROR. c_csc estimates how far the candidate is from what independent models write for the same sentence in the same vocabulary. It does **not** measure truth against a reference. If the peers reproduce the candidate's error (anchoring on a listed symbol, or a shared bias), the error scores as faithful.

- **Variants.** `c_csc_graded` is claim-unit F1 with the identity map. `c_csc_multi` also accepts a peer's `alt_fol` when another peer produces that same reading.
- **Fallbacks.** Fewer than 2 usable peers gives 0.5. An unparseable candidate gets 1.0 in the coverage view. A z3 UNKNOWN (2 s timeout) counts as not equivalent.

Library: `src/csc.py` (`extract_signature`, `order_symbols`, `build_prompt`, `exact_equiv`, `consensus_score`, `majority_formula`, `typed_repair_same_vocab`, `csc_peers`). Tests: `tests/test_csc.py` (27 pass). The tests cover 20 known formula pairs, signatures, prompt determinism, the family rule and edge cases.

## What happened (read this first)

- **Paid sweep refused.** After 1,033 of about 9,000 planned calls, the platform refused all further paid calls: `HTTP 403 aii_run_budget_exhausted`. The run's shared "Test idea" phase budget of $7.00 had been used up, mostly by sibling artifacts. This artifact spent **$0.108** in total.
- **No fallback route.** The `:free` tier was also exhausted (`429`, 1000/day, shared key). There is no GPU for local peers.
- **Salvage population, fixed before scoring.** `prereg_csc_E_addendum1.json` was written before any CSC score existed. It defines **PRIMARY = the 354 R_AB rows (196 ERROR / 158 CORRECT, 144 sentences) whose 3 CSC peer calls all completed**, plus sensitivity sets GE2 (475 rows) and MINI200 (180 rows).
- **Not run.** FORMAT-ONLY, PLACEBO (random-sentence signature) and RENAME_SYN/NONCE are **NOT_RUN**. OTHER-SIG and k=4 are exploratory only. The L25 cell is **NOT_READ** (22 CORRECT rows).
- **Full-population analyses.** Every $0 analysis runs on all 2,686 rows: FREE-MATCHED exact vs ALIGN, the vocabulary decomposition, and the 9-peer rename FA.

## Main results (tables.md; results/analysis.json)

| PRIMARY rows (paired, B=2000 sentence bootstrap) | e = P(endorsed\|ERROR) | d = P(flagged\|CORRECT) | strat AUROC |
|---|---|---|---|
| **CSC c_csc** | 0.459 [0.360, 0.549] | **0.139** [0.075, 0.234] | **0.614** [0.493, 0.736] |
| FREE-MATCHED exact: same 3 families' existing E outputs, no signature | 0.173 | 0.323 | 0.770 [0.686, 0.844] |
| FREE-MATCHED ALIGN | 0.352 | 0.190 | 0.731 |
| c_score_align (9 free peers) / END_MAJ-9 | 0.209 | 0.348 | 0.774 [0.682, 0.857] |
| flash-lite judge (disguised) | – | – | 0.664 [0.568, 0.750] |
| HYB_MEAN = (c_csc + c_score_align)/2 | 0.316 | 0.190 | 0.709 [0.586, 0.817] |

1. **The signature fixes d but causes anchoring; the net effect is negative.**
   - Paired CSC − FREE exact: Δd = −0.184 [−0.314, −0.087] and Δe = **+0.286** [+0.179, +0.391].
   - Paired Δ strat AUROC: **−0.156** [−0.290, −0.031] vs FREE exact, −0.160 [−0.275, −0.064] vs c_score_align, −0.050 [−0.212, +0.107] vs the flash-lite judge.
   - The same sign holds on GE2, on MINI200 and after removing phi-4's exemplar leakage (T17 post-hoc: −0.132 [−0.251, −0.023]).
2. **The anchoring is concentrated where the prediction said it would be** (T9). Peers endorse:
   - MEANING_RENAME-type errors at 0.82, vs 0.04 when the same peers are scored exactly without a signature;
   - ADD errors at 0.49 vs 0.14, and DROP errors at 0.47 vs 0.17.
   - The sibling evaluation's pre-registered e ceiling was 0.162; measured e is 0.459.
3. **d still grows with length.** The GEE slope of d on z(words) is +1.25 [+0.41, +2.09], so G1 fails. NET words T3−T1 is +0.64 [+0.23, +0.98]. On M3, CSC's decision correctness degrades faster with length than the judge's under both specifications (Δslope −0.23 [−0.77, −0.02]; stacked-GEE interaction −0.35 [−0.69, −0.01]).
4. **No incremental signal.** [S4_full + c_csc] − S4_full = +0.006 [−0.013, +0.025]; with c_score_align already in the stack it is −0.004. The matched free-exact score *does* add (+0.056 [+0.008, +0.122]).
5. **$0 mechanism facts on all 2,686 rows** (T2, T8):
   - Scoring the same matched free peers with exact names instead of ALIGN raises d from 0.328 to 0.583 and lowers e from 0.268 to 0.130.
   - Of the free-exact disagreements with CORRECT candidates, 45% are ALIGN-resolvable, 2% are only name-free-resolvable and **53% are structural**.
   - Only 20% of the flagged CORRECT rows have *all* their disagreements vocabulary-resolvable. So most of d is not vocabulary.
6. **Incumbent rename weakness ($0).** Re-derived 9-peer c_score_align reproduces the frozen column exactly (r = 1.000). Its false-alarm rate on CORRECT rows rises from 0.595 to **0.868** after a one-predicate WordNet-synonym rename (+0.273 [+0.164, +0.384]). CSC's own rename arm could not run (G3-E NOT_RUN).
7. **Cost** (G5 passes): **$5.25e-4 per candidate** undeduped, or $2.76e-4 apportioned over shared calls, plus 0.024 s of z3 CPU.
8. **Prompt-following sanity check.** CSC peers agree with each other exactly on 0.55 of pairs, vs 0.36 for the free peers on the same rows. Shuffled-label AUROC is 0.48.
9. **Typing.** Typed same-vocabulary repair toward the CSC peer majority gets 0.185 exact op-set accuracy on 65 R_A errors, below the majority class (0.262).

**Gate file** (`csc_gate_E.json`, PROVISIONAL):

| gate | result | detail |
|---|---|---|
| G1 | FAIL | for every variant; the words slope is > 0 |
| G2 | FAIL | R_AB part; the L25 part is NOT_READ |
| G3-E | NOT_RUN | |
| G4 | null | sibling experiment |
| G5 | PASS | |

**Answer for iteration 5:** the E-side evidence says CSC is **not** a fix. It trades legitimate divergence for anchoring into the candidate's errors, at a net loss. The iteration-5 rule should fall back to the frozen c_score_align + p_peer_text. The E-side numbers are PROVISIONAL, because the population is a 354-row subset.

## Integrity checks

- **Independent re-derivation** (`src/audit_rederive.py`, `results/audit_rederive.json`) uses its own z3 encoding, sklearn AUROC, its own stratified AUROC and a seed-1 bootstrap, reading raw cache/arm files. It reproduces:
  - on PRIMARY: c_csc 0.614, FREE exact 0.770, c_score_align 0.774 (strat AUROC); e/d 0.459/0.139 vs 0.173/0.323; Δ −0.156 [−0.295, −0.027]; per-row c_csc and c_free_exact identical to the pipeline (100% of rows);
  - on FULL: free-exact e/d 0.130/0.583;
  - the CSC d-vs-words slope, positive (clustered logit +1.49 [+0.54, +2.44]);
  - cost $5.25e-4 per candidate.
  - Placebo: with labels permuted within stratum, the paired Δ CI is [−0.079, +0.058] (includes 0), and c_csc strat AUROC is 0.52.
- Not independently re-derived: nesting, M3, NET, ALIGN-based numbers, rename FA, the error-class e table, typing.

- The prompt sha256 matches between iteration 1 and iteration 2.
- The R_AB label sha1 matches prereg_baselines (`1bfcb306…`).
- The frame has 2,686 rows and joins 1:1.
- The $0 reproduction of eval 2's deepseek+microsoft+openai pool gives strat AUROC 0.7428 (target 0.7427). T1's c_score_align gives 0.741 (`results/repro_checks.json`).
- `prereg_csc_E.json` (sha256 `d1f51857…`) predates addendum 1, which predates the label-blind score table (sha256 in `prereg_csc_E_addendum.json`). `analyse.py` asserts both.

## Layout

| path | content |
|---|---|
| `method.py` | pipeline entry point (stages prep, pilot, prereg, mini, full, repro, score, analyse, posthoc, report, test) |
| `src/csc.py` | the CSC metric library |
| `src/prep.py` | integrity checks, label-blind frame (`data/frame_blind.jsonl`), labels (`data/labels_RAB.jsonl`), FREE-MATCHED peers |
| `src/arms.py`, `src/gen.py`, `src/csc_llm.py`, `src/pilot.py` | arm selection, prereg, async cached OpenRouter client with ledger and hard stop, pilot |
| `src/rename.py` | RENAME_SYN (dataset-3 control_rename logic) |
| `src/score.py` | label-blind scoring: all arms, FREE-MATCHED exact + ALIGN, 9-peer ALIGN re-derivation on renamed rows |
| `src/repro.py` | $0 reproduction checks |
| `src/analyse.py` | analyses (a)–(k) and gates |
| `src/posthoc_contam.py` | post-hoc phi-4 leakage sensitivity |
| `src/report.py` | writes the tables and gate files |
| `vendor/` | read-only copies of exp 8 `src/` (E parser, z3, repair search), eval 2 `stats.py` / `mechanism.py` / `consensus_mx.py`, exp 6 `s4.py`, and the few-shot prompt |
| `prereg_csc_E.json` (+`.sha256`), `prereg_csc_E_addendum1.json` (+`.sha256`), `prereg_csc_E_addendum.json` | pre-registration, salvage addendum, score-table hash |
| `csc_gate_E.json` | E-side gates per variant, for the iteration-5 freeze |
| `tables.md` | every table, each with a `# source:` line |
| `method_out.json` (+ `full_`/`mini_`/`preview_`) | exp_gen_sol_out; 2,686 examples; `predict_*` oriented higher = ERROR; `NA` where CSC was not generated |
| `results/per_item_csc_E.jsonl` | per row: every CSC / FREE / arm column, peer formulas, alt_fols, $ |
| `results/llm_cache.jsonl`, `results/api_cost_ledger.jsonl`, `api_cost_ledger.json` | the 599 paid peer generations (the only copy) and the per-call ledger |
| `results/analysis.json`, `results/scores_labelblind.jsonl`, `results/d_measured.json`, `results/typing_rows.json`, `results/d_tagging_rows.json`, `results/pilot.json`, `results/repro_checks.json`, `results/posthoc_phi_contamination.json` | analysis outputs |
| `deviations.json` | D1–D9 |
| `inputs_manifest.json`, `inputs/` | sha256 of every read-only input; copies of the small ones |

## How to run

```bash
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python numpy pandas scipy scikit-learn statsmodels z3-solver==5.1.0.0 loguru aiohttp tenacity nltk pytest requests psutil pyyaml
PYTHONHASHSEED=0 .venv/bin/python method.py test                                # unit tests
PYTHONHASHSEED=0 .venv/bin/python method.py                                     # $0 stages: repro score analyse posthoc report (~7 min, 4 CPUs)
PYTHONHASHSEED=0 .venv/bin/python method.py prep pilot prereg mini full         # API stages (needs OPENROUTER_BASE_URL/KEY; cached calls are never repeated)
```

WordNet for RENAME_SYN is read from the exp 8 `data/nltk_data` directory (read-only). Running `full` with budget available would complete the pre-registered arms. The cache keeps every finished call, so only the missing ~8,000 calls (about $1.7 estimated) would be spent.

## Restoring removed files

| entry | how to restore |
|---|---|
| `.venv/` (delete: regenerable) | the `uv venv` + `uv pip install` commands above |
| `.pytest_cache/` (delete: regenerable) | `PYTHONHASHSEED=0 .venv/bin/python -m pytest -q -c pytest.ini tests` |

Nothing else is deleted. `results/` is kept because it holds the only copy of the paid peer generations, at `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/results/llm_cache.jsonl`.
