# E2-B: a second untouched sample of long, heavily conditioned sentences (iteration 5, experiment 12)

run_u75jRHUss0zo · invention iteration 5 · artifact `gen_art_experiment_12` (plan `gen_plan_experiment_2`, "Second fresh sample of long sentences").
Workspace (absolute): `.`

## Status: PARTIAL — no confirmatory cell is testable (run-level API budget exhausted)

**Read this first.** At 11:39 UTC the run-level OpenRouter budget for this phase ($12, shared by every concurrent artifact of the run)
was exhausted. From then on every paid call returned `HTTP 403 aii_run_budget_exhausted`. This artifact had spent **$0.83** of its
$9.5 cap. It probed the API every 15 minutes from 11:41 to 14:41 UTC and every probe was refused (`logs/budget_polls.jsonl`). Polling stopped at 14:47, because a restore after that could not complete the pre-registered 250-sentence floor before the last paid call at 15:38.

What completed:
- selection, prereg and the surplus claim;
- all 4,000 generations;
- solver labels for all 400 sentences;
- every label-free score: V0 and PT (exp-5 code), V1-V5, c_exact, local features, the pairwise matrix, flash-lite disguised on
  the first 2,735 parseable rows in batch order, the frontier pilot (10 rows);
- both seals, the join and all analyses.

What did not complete:
- the blind panel for any batch (stage 1 had finished for 14/50 sentences of batch 1; the incomplete batch is excluded, as
  pre-registered);
- flash-lite original, nano, the cost-matched deepseek-v3.2 judge, the frontier run and GG.

Consequence: without the panel, E's final rule leaves every non-equivalent candidate UNRESOLVED. So R_AB, the primary population,
has **no CORRECT class**. E2's pre-registered no-panel regime R_A_UNAUDITED (tier A against the *unaudited* MALLS gold) has
48 CORRECT / 334 ERROR rows. That is below E's testability floor of 50 CORRECT, so **B1-B4 and U1-U4 are NOT TESTABLE**.
The numbers below are exploratory. The union with E2-A is `NOT_COMPUTED_E2A_MISSING`.


## What this artifact does

E2-B is a pre-registered replication sample for the run's one live lead: frozen cross-family consensus
`c_score_align` (V0) as a gold-free NL→FOL faithfulness score, compared with LLM judges on long sentences.

- **Sample.** 400 untouched MALLS-v0.1-train sentences with ≥25 words and ≥3 gold conditions (L25). They are drawn by E2's frozen rule,
  continued: E2's 98-sentence pre-ranked surplus first, then the same sha1(`'E2_v1|'+sentence_id`) order, skipping every E2 sentence
  and every sentence that shares a 12-gram with E or E2 (`e2bsrc/src_e2b/select_e2b.py`). The script first re-runs E2's selection
  and checks that it reproduces `work/pool_E2.json` byte for byte (sha256 `98cdccff…`). The ≥30-word bin is exhausted, so E2-B is
  93.5% 25-29 words (deviation D-E2B-comp).
- **Candidates.** 4,000 formalisations from E2's 10 frozen generator slots (9 families, few-shot, temperature 0).
- **Labels.** E2's byte-identical solver + blind-panel code (`e2bsrc/`, 78 files hash-verified in `code_freeze_check_E2B.json`), run in
  8 hash-ordered batches of 50. The panel uses E2-A's drift decision (M2 = PASS) with pinned providers.
- **Scores.** Computed before any label was read, under a file-access guard, then sealed (`scores/score_seal.json`):
  - V0 and PT with exp 5's byte-identical code (the copy reproduces the stored exp-5 values on 50/50 dataset-E rows);
  - V1-V5 with the M1 freeze code (winner "NONE: V0 stands", so these are development-only rows);
  - flash-lite disguised/original, nano, the cost-matched deepseek-v3.2 judge and the frontier judge gemini-3.1-pro-preview,
    all with the byte-identical rubric-A prompt (PROMPT_SHA asserted).
- **Analysis.** Join only after both seals verify, then the pre-registered analyses (`src/analyse_e2b.py`, statistics = exp 6's
  `api_bar.py`, reproducing T1's L25 delta +0.0694 exactly), and the union with E2-A if its marker exists (`src/union.py`).

## Results (exploratory; `analysis/tables.md` gives every number with its source)

**Label-free: valid without labels.**
- Coverage:
  - parse rate 0.883 (467 of 4,000 candidates unparseable, all scored 1.0 by every metric);
  - V0 scorable on 0.881 (8 parseable rows have fewer than 2 other-family peers).
- Agreement structure (eval-2 matrix, 12,150 pairs, 0 timeouts):
  - 6.37 equivalence classes per sentence;
  - the largest class holds 32.9% of the outputs;
  - only 13.4% of cross-family pairs agree;
  - 19.1% of sentences have no agreeing cross-family pair.

  On these long sentences, disagreement is the norm.
- V0 vs flash-lite disguised on 2626 rows scored by both:
  - Spearman 0.296;
  - flag agreement at 0.5: 0.697 (κ 0.168);
  - V0 flags 89.6% of rows, the judge 67.2%.
- Rename invariance on a hash sample of parseable candidates of any label. The controls come from E2's frozen generator and are
  z3-verified meaning-preserving.
  - Paired flip (control flagged while its parent is not): RENAME_SYN 0.088 [0.051, 0.147]
    (n=137); RENAME_NONCE 0.107 [0.077, 0.148] (n=298).
  - Reverse flips: 0. Renaming only ever raises V0 (mean shift +0.099 / +0.141).
  - This is the known rename non-invariance of the aligner-based score, replicated on fresh data.
- Placebo: V0 computed against the peers of a *different* sentence scores 1.0 on every row (AUROC 0.50).
- Cost:
  - V0 needs no API call beyond the peers' generations: $0 MARGINAL, and $0.00086
    FULL per candidate for its 9 peer generations;
  - z3 time 0.059 s per candidate;
  - flash-lite $5.61e-05 per call;
  - the frontier judge $4.57e-03 per call (10-row pilot).

**Label-based, EXPLORATORY: population R_A_UNAUDITED, L25_E2B.** This is not a faithfulness test. CORRECT means z3-equivalent to the
unaudited MALLS gold, and E's panel judged most MALLS gold wrong.

| metric | strat AUROC [95% CI] | n (ERR/COR) |
|---|---|---|
| V0 c_score_align | 0.737 [0.645, 0.827] | 333/48 |
| PT p_peer_text | 0.655 [0.546, 0.767] | 334/48 |
| flash-lite disguised | 0.496 [0.356, 0.620] | 245/31 |
| S4_E2B (cheap-baseline stack, CPU-feasible) | 0.498 [0.402, 0.594] | 334/48 |

- V0 − flash-lite disguised = 0.208 [0.066, 0.363], on 276 paired rows with only
  31 CORRECT and 17 both-class sentences.
- Nested [S4 + V0] − S4 = 0.120 [0.013, 0.237].
- **Label-coupling diagnostic.** Under gold-equivalence labels every CORRECT row agrees with every other CORRECT row, which
  mechanically lowers V0 on CORRECT rows. With gold-equivalent peers removed from the pool, V0's AUROC falls to
  0.611 [0.490, 0.738], and its lead over flash-lite falls to
  0.133 [-0.024, 0.314]. About half of the exploratory advantage is label/metric coupling.
- H-MECH (i) and (ii) are tautological in this regime. (iii) NET is negative, with narrow word terciles. (iv) holds for d and for
  ADD/DROP e; MEANING_RENAME is not testable without the panel.
- H-IMPROVE: M1's winner is "NONE: V0 stands". V1-V5 are development-only rows.

**Independent re-derivation** (`analysis/rederive_headline.json`): every headline number above was recomputed from the raw sealed label file and score file through a different code path, and all of them reproduce. The placebos fail as required: labels permuted within word bin give a null mean Δ of +0.001 (SD 0.066; permutation p = 0.005 for the observed +0.208), and both a permuted-label bootstrap CI and a random-score CI include 0.


## Layout

| Path | What |
|---|---|
| `method.py` | entry point: runs the pipeline stages in order (`python3 method.py --stage all` or one stage) |
| `reproducibility.md` | what was actually run, in order, with versions, seeds, hardware and expected numbers |
| `pyproject.toml` | exact pins of the scoring/analysis venv (`exp5src/.venv`); E2's labelling venv is pinned in `e2bsrc/pyproject.toml` |
| `analysis/rederive_headline.json` (`src/rederive_headline.py`) | independent re-derivation of every headline number (sklearn AUROC, own bootstrap, own matrix logic) + placebos |
| `method_out.json` (+ `full_`/`mini_`/`preview_`) | aii `exp_gen_sol_out`: one example per E2-B candidate row (`predict_V0`, `predict_flashlite_disg`, …, `metadata_*`), plus rename-control rows |
| `analysis/tables.md` | every reported number with its source file and key |
| `analysis/analysis_E2B.json` | all E2-B analyses (cells, deltas, S4 nesting, frontier IPW, H-MECH, rename, complexity, coverage, cost, τ-b, placebo) |
| `analysis/confirm_verdict_E2B.json` | the pre-registered claims (B1-B4, H-MECH, H-IMPROVE) with verdicts and populations |
| `analysis/descriptive_nolabels_E2B.json` | label-free descriptives: coverage, concordance with flash-lite, agreement structure, rename invariance on any-label candidates |
| `analysis/per_item_E2B.jsonl` | the joined per-row file (labels + every score), pointed to by `e2b/E2B_FINAL_READY.json` |
| `analysis/union_longpool.json` | union with E2-A + heterogeneity + meta-analysis, or `NOT_COMPUTED_E2A_MISSING` |
| `prereg_iter5_E2B.json` (+ `.sha256`) | pre-registration, frozen before any E2-B generation |
| `deviations.json` | every departure from the plan, with evidence |
| `cost_ledger_master.jsonl` | every paid call (E2 scripts, judges, L3 questionnaires, probes) |
| `e2b/` | `sentences_E2B.json`, `reserve_E2B.json`, `batches_E2B.json`, `census_E2B.json`, `E2B_SURPLUS_CLAIM.json`, `E2B_FINAL_READY.json` (marker M3), `drift_decision.json` (M2 copy), `m1_copy_record.json`, `progress.jsonl`, `seal.json`, `testability_E2B.json`, `exp5_repro_check.json`, `T1_repro_check.json` |
| `scores/` | label-free per-row scores (`scores_E2B.jsonl`), judge caches, pool/matrix/variant files, frontier subsample, rename-control scores, `score_seal.json`, `file_access_log.txt` |
| `e2bsrc/` | copy of E2's frozen pipeline (`src/`, `labeller/`, `src_e2/`, `src_d3/`, prompts, data) + E2-B wrappers in `e2bsrc/src_e2b/` (selection, pinned-provider runner, batch drivers, budget, quarantine); `raw/generations.jsonl` (all 4,000 generator responses), `work/` (solver labels, panel records, assembled rows), `sealed/` (sealed labels + references), `candidates_E2_nolabels.jsonl` |
| `exp5src/`, `exp6src/`, `eval2src/`, `freeze_copy/` | byte-identical copies of the frozen scoring code (exp 5), statistics/S4 (exp 6), pairwise matrix (eval 2) and the M1 freeze files |
| `src/` | this artifact's code: `prereg_e2b.py`, `poll_markers.py`, `score_e2b.py`, `pairwise_e2b.py`, `descriptive_e2b.py`, `seal_scores.py`, `analyse_e2b.py`, `union.py`, `make_method_out.py`, `make_tables.py`, `write_deviations.py`, `finalize.sh`, budget/judge chains, repro checks |
| `tests/` | synthetic-row code tests of the union duplicate rule and the analysis functions |
| `logs/` | every run log, marker polls, budget polls |

## How to run

```bash
bash restore.sh                                              # venvs, NLTK data, HF sources, parser regression test
cd e2bsrc && .venv/bin/python src_e2b/code_freeze_check.py   # 78 frozen files
.venv/bin/python src_e2b/select_e2b.py && cd ..              # reproduces E2's pool, draws E2-B (deterministic)
python3 src/prereg_e2b.py                                    # refuses to overwrite the frozen prereg
bash e2bsrc/src_e2b/gen_all.sh                               # generation (10 slots), resumable
bash e2bsrc/src_e2b/run_batches_resume.sh                    # solver labels + panel per batch (needs budget), resumable
bash src/scoring_pipeline.sh && bash src/cpu_chain.sh        # label-free scoring (build, disguise, L3, pool, matrix, variants)
bash src/judge_resume.sh                                     # judges (flash-lite, nano, cost-matched, frontier), resumable
bash src/finalize.sh                                         # score seal -> label seal -> join -> analyses -> union -> outputs
```
Paid steps are resumable and cached (`raw/generations.jsonl`, `work/panel_cache.jsonl`, `exp5src/results/llm_cache.jsonl`), so a rerun
that keeps them re-bills nothing.

## Restoring removed files

Everything marked `delete` in `.aii/manifest.yaml` is restored by `bash restore.sh`:
- `e2bsrc/.venv/`, `exp5src/.venv/` (regenerable): `uv venv` + `uv pip install -r pyproject.toml` in each directory.
- `e2bsrc/nltk_data/` (redownloadable): `nltk.download('wordnet')`, `nltk.download('omw-1.4')` into `e2bsrc/nltk_data`.
- `exp5src/data/nltk_data/` (redownloadable): the `wordnet`, `omw-1.4` and `words` corpora zips from `raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/`.
- `e2bsrc/raw/hf/` (redownloadable): `opendatalab/ProverQA` dev files at revision `e2561beed450272690da658d21ae667570dbbafc`, and
  `tasksource/folio` `folio_v2_{train,validation}.jsonl` at revision `295b95fb4fe9be4ff3f933b73142d142cf6b2c97` (needed only to
  re-run E2's selection reproduction).
- `**/__pycache__/` (regenerable): Python bytecode.
- `e2bsrc/.pytest_cache/` (regenerable): `e2bsrc/.venv/bin/python -m pytest -q -c e2bsrc/pytest.ini e2bsrc/tests/test_fol.py`.

## Licences
MALLS-v0.1: CC-BY-NC-4.0. Generator and judge outputs are under their providers' terms.
