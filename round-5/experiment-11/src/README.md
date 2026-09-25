# E2-A: frozen cross-family consensus on the untouched E2 set (iteration 5, direction 1)

Run `run_u75jRHUss0zo`, `round-5/experiment-11/src`, following plan `gen_plan_experiment_1`.
The prompt that reached this session held only the tail of the research question. The step's identity was inferred from
the workspace path and from how iteration 4 mapped plans to artifacts (`deviations.json` D-STEP). Every number below is
copied from `tables.md` / `results/*.json`, which `analysis/` generates.

## Status: PARTIAL. The pre-registered confirmation is NOT_TESTABLE (run budget exhausted)

At about 11:40 UTC the run-level OpenRouter budget for the "Test idea" phase ran out: $12.00, shared by every
concurrent artifact of the run (HTTP 403 `aii_run_budget_exhausted`). This artifact had spent **$2.05** of its $9.5 cap.
The key was polled every 15 min until the cutoff pre-registered in `prereg_addendum_budgetstop.json` (15:30 UTC). It
never recovered (`e2src/logs_e2a/key_poll.log`). Only a person can raise that limit, in the run's Configure settings.

| step | state |
|---|---|
| Drift gate (pinned providers, fresh cache) | **PASS**: majority agreement 0.955 on 269 replayed items; all panel ids served; track-H flag rate 0.827 inside E's Wilson CI [0.773, 0.890]. Marker M2 `e2/E2_DRIFT_DECISION.json` |
| Generation | complete: 550 sentences × 10 slots, 5,500 candidates, $0.49 |
| Solver labels | complete (550) |
| Panel (stage 1 + P1 adjudication) | complete only for the **first sha1-order prefix of 110 sentences** (37 L25 / 37 EXC / 36 DT). This is a random prefix, not completion-selected. No reference repair |
| Label-free scores | complete for all 5,500 rows: V0, PT, c_exact, V1–V5, L2, L3, the user's pilot metrics, local Qwen3-8B judge ×2. Sealed at 13:01 UTC (`score_seal.json`, 162 files) before any label was assembled (label seal 15:12, join 15:30; `results/join_record.json`) |
| API judges | flash-lite disguised on only 707 of 4,780 parseable rows; flash-lite original, gpt-4.1-nano and the round trip **not run** |

With labels on 110 sentences, the R_AB long pool (L25+EXC) has **94 rows (76 ERROR / 18 CORRECT, 12 sentences)**. That
is below the frozen testability rule (≥50 / ≥50, ≥25 sentences per class). Pre-registered criterion (a) is therefore
**NOT_TESTABLE**, (b) is not testable in that cell, and (c) is NOT_TESTABLE in the R_COMP sibling (its gloss gate failed
twice, leaving 0 CORRECT rows). **This artifact neither confirms nor disconfirms the lead.** The two cells that do pass
the testability rule are DT (prover-built ProverQA gold) and ALL. There the comparison bar is the declared substitute:
T1's local Qwen3-8B rubric-A judge. That is secondary evidence and cannot produce CONFIRM.

## What the primary metric measures (stated precisely)

`c_score_align(text, fol, peers)` (V0, frozen iteration-2 exp-5 code) = 1 − (share of the parseable peer formalizations
of the same sentence, from model families other than the candidate's, that the iteration-1 eqmv procedure proves
z3-equivalent to the candidate modulo a predicate/constant vocabulary alignment). It is a **gold-free error score**:
higher means more likely unfaithful. It measures how far the candidate sits from what independent systems write for the
same text.

It does **not** measure agreement with a reference, or truth. An error most peers share scores as faithful (peer-endorsed
error). A correct but idiosyncratic reading scores as an error. And on E2, **renaming symbols alone breaks it** (see the
rename section). The reusable entry points and their "measures / does not measure" statements are in `lib/nl2fol_metrics.py`:
- `c_score_align`
- `c_exact`
- `peer_text`
- `variants_for_sentence` (V1–V5)
- `family_weights_from_sentences`
- `evaluate`

`lib/tests/test_lib.py` checks that the library reproduces the pipeline's sealed scores to 1e-9.

## Results on the completed prefix

Stratified AUROC for predicting ERROR (R_AB, stratified sentence-cluster bootstrap, B = 2000, seed 0). Source:
`results/auroc_cells.json`.

| metric | ALL (273 rows: 150 ERR / 123 COR, 38 sent.) | DT (179: 74 / 105, 26 sent.) | LONG, **not testable** (94: 76 / 18) |
|---|---|---|---|
| S4_E2 stack (local judge ×2, L2, L3; OOF) | 0.931 [0.888, 0.967] | 0.953 [0.911, 0.986] | 0.687 |
| PT p_peer_text (frozen fusion) | 0.902 [0.847, 0.956] | 0.919 [0.860, 0.976] | 0.704 |
| local Qwen3-8B judge, original view | 0.901 [0.850, 0.945] | 0.918 [0.864, 0.960] | 0.714 |
| local Qwen3-8B judge, disguised view | 0.895 [0.844, 0.938] | 0.913 [0.858, 0.958] | 0.695 |
| **V0 c_score_align** | **0.890 [0.838, 0.940]** | **0.916 [0.858, 0.970]** | 0.603 |
| c_exact (no aligner) | 0.831 [0.749, 0.900] | 0.854 [0.763, 0.925] | 0.573 |
| flash-lite disguised (the pre-registered bar; 71 / 63 rows only) | 0.814 [0.680, 0.930] | 0.818 [0.682, 0.935] | — |
| L2-bow | 0.751 | 0.760 | 0.653 |
| L3 | 0.583 | 0.572 | 0.706 |

Paired strat Δ (source: `results/auroc_cells.json`):
- ALL, V0 − local judge (disguised): −0.005 [−0.047, +0.041].
- DT, V0 − local judge (disguised): +0.003 [−0.042, +0.052].
- ALL, [S4_E2 + V0] − S4_E2: −0.009 [−0.034, +0.014]. V0 adds nothing over the local-judge stack.
- DT, V0 − c_exact: +0.062 [−0.003, +0.131].

**Reading.** On prover-built gold (DT), frozen consensus is as good as a local 8B judge, and no better. On the long
MALLS strata, which are the lead's claim, the prefix is too small to test. There, the point estimates put V0 *below* the
local judge: long pool −0.091 [−0.219, +0.017]; L25 V0 0.443 on 42 rows with only 7 CORRECT. Development-set E's +0.10
advantage over flash-lite is not reproduced by anything testable here.

### The user's pilot metrics: most do not track correctness

These are the pilot study's structural metrics, using T1's frozen adaptation. E2 sentences are single sentences, so the
pilot's "documents" are built artificially. AUROC 0.5 means the metric does not separate ERROR from CORRECT. Source:
`results/auroc_cells.json`.

| pilot metric (higher = more suspicious) | ALL | DT | EXC | reading |
|---|---|---|---|---|
| m1 joint-load conflict (story ∪ cand UNSAT) | **0.500** [0.500, 0.500] | 0.500 | 0.500 | never fires: does not track correctness |
| m2 arity inconsistency | **0.507** [0.500, 0.520] | 0.507 | 0.500 | chance |
| m2 shape inconsistency | **0.510** [0.486, 0.536] | 0.510 | 0.500 | chance |
| m3 dangling symbols | **0.413** [0.365, 0.459] | 0.400 | 0.463 | *inverted*: correct candidates have more dangling symbols |
| m5 1 − rerun Jaccard (cross-system proxy) | 0.713 [0.627, 0.789] | 0.729 | 0.653 | tracks correctness, but only because it is a lexical form of cross-system agreement |

Placebo check (`results/placebo_E2.json`): shuffled labels give V0 0.501 (p95 0.606). Within-stratum score permutation
gives 0.497.

### H-MECH: the mechanism, replicated on new labels

Source: `results/hmech_E2.json`. The prefix is dominated by DT.
- (i) **CONFIRMED**. 0.909 [0.842, 0.977] of the peers that disagree with a CORRECT candidate are themselves labelled
  ERROR (352 peer judgements, 32 sentences). The 3-pool gives 0.918.
- (ii) Scatter ratio SI_cor/SI_err = 7.3 [4.0, 20.8]. **NOT_READ**: 24 sentences, one short of the 25 required.
- (iii) NET Δ(e+d), words T3 − T1 = +0.347. The point is > 0, but the CI [−0.036, +0.855] includes 0. Degradation is
  suggested, not established.
- (iv) **CONFIRMED**. ALIGN versus exact: the false-alarm rate on CORRECT rows falls from 0.740 to 0.179 (d; Δ −0.561
  [−0.732, −0.386]). The share of errors endorsed rises: meaning-rename-type 0.125 → 0.625 (n = 8), ADD/DROP 0.00 → 0.093
  (n = 118).

### H-IMPROVE and H-RENAME (the freeze sibling's markers)

- **H-IMPROVE: V0 stands.** The freeze selected no variant (`freeze_copy/selection.json`). On E2 ALL, V1–V5 − V0 lie
  between −0.020 and +0.015, and every CI includes 0 (`results/improve_E2.json`).
- **H-RENAME: NOT CONFIRMED.** GG failed its development gate (FAIL(g3)), so c_gg was not computed.
- **V0 rename controls** (`results/rename_V0.json`): these are dataset 3's frozen `control_rename`, applied to
  final-CORRECT rows; each control is z3-equivalent to its parent and the text is unchanged.
  - RENAME_SYN (n = 36): false-alarm rate 0.944 versus 0.361 for the parents; paired flip 0.583.
  - RENAME_NONCE (n = 145): false-alarm rate **1.000** versus 0.262; paired flip 0.738.
  - So V0 is **not rename-invariant**. A correct formula whose predicate names change is flagged as an error.

### Other reported items

- **System level.** Kendall τ-b between a system's mean score and its error rate, over 10 generator slots: V0 0.733
  (p = 0.002), PT 0.778 (p = 0.001). Source: `results/system_level_E2.json`.
- **Coverage.** 1,100 prefix rows: 115 unparseable, 56 CONTESTED, 0 rows with fewer than 2 peers. In the COVERAGE view,
  unparseable rows count as errors scored 1.0. Source: `results/coverage_E2.json`.
- **Cost.** Source: `results/cost_E2A.json`.
  - FULL cost of consensus: $9.4e-5 per candidate ($0.00094 per sentence of peer generation).
  - MARGINAL cost: $0, and 1.46 CPU-seconds per candidate.
  - Flash-lite: $5.3e-5 per call.
- **Union with E2-B.** E2-B finalized with no panel labels, so the union adds no R_AB rows (`results/union_longpool.json`).

## Meta-evaluation dataset (labels)

| file | contents |
|---|---|
| `e2/candidates_E2_nolabels.jsonl` | 5,500 label-free candidate rows (text, candidate_fol, slot, family, strata) |
| `e2src/sealed/labels_E2.jsonl` + `e2src/seal.json` | E's frozen labels: label, tier, reading_choice, vex, error_ops, panel votes. Verify with `e2src/src_e2/verify_seal.py` |
| `per_item_E2A.jsonl` | the join: every score + label + complexity per row (sha256 in marker M3 `e2/E2A_FINAL_READY.json`) |

Only the 110-sentence prefix has panel-based (tier A/B) labels. The other sentences keep solver-only labels: UNRESOLVED
or A_unaudited_ref.

## Layout

| path | what |
|---|---|
| `prereg_iter5_E2A.json` (+sha256), `prereg_addendum_budgetstop.json` (+sha256) | pre-registration (hypothesis criteria verbatim) and the budget-stop addendum, both written before any label was assembled |
| `e2src/` | copy of dataset 4 (the frozen E protocol). `src_e2a/` holds the E2-A drivers: pin, order, prefix, activation, poller |
| `frozen/`, `freeze_copy/`, `inputs_manifest.json` | byte-identical copies of exp-5, T1, eval-2 and the freeze files (131/131 identical) |
| `scoring/` | label-free scoring under the file-access guard (`guard.py`): consensus, API/local judges, pilot metrics, assembly + score seal; tests |
| `analysis/` | join (checks both seals), analyses, E2-B union, rename controls, output builder; tests |
| `lib/nl2fol_metrics.py` | reusable metric functions with `measures` docstrings |
| `results/*.json`, `tables.md` | all results; every table carries a `# source:` line |
| `method_out.json` (+ full/mini/preview) | `exp_gen_sol_out` (validated). `predict_*` scores are oriented higher = ERROR |
| `deviations.json`, `cost_E2A` in `results/`, `e2src/cost_ledger.jsonl` | deviations D-STEP … D-PREFIXCUT; spend |

## How to reproduce

```
cd e2src && bash restore.sh                      # E's venv; then src_e2a/*.sh in order: run_drift, run_gen, run_panel
env/.venv/bin/python scoring/score_consensus.py --stage l3|score|pairwise|exact
env/.venv/bin/python scoring/api_judges.py --stage prep|judges ; /root/e2a_gpu/.venv/bin/python scoring/local_judge.py
env/.venv/bin/python scoring/pilot_metrics_E2.py && env/.venv/bin/python scoring/assemble_scores.py
(e2src) src_e2/{assemble_e2,controls_e2,testability_e2,seal_e2,verify_seal}.py
env/.venv/bin/python analysis/analyse_E2A.py --stage join && ... --stage analyse --prefix 110
env/.venv/bin/python analysis/{rename_V0,union_E2B,make_outputs}.py
```

`env/` is exp-6's pinned CPU environment (on local disk; `deviations.json` D-ENV). If the budget is raised, run the rest
without re-billing anything already paid: `e2src/src_e2a/run_panel.sh`, then `scoring/api_judges.py --stage judges`.
Then re-run the $0 chain without `--prefix`; the analyses reproduce the full pre-registered test.

## Restoring removed files

The paths marked `delete` in `.aii/manifest.yaml` can be regenerated:

```bash
# e2src/.venv/ (regenerable)
cd e2src && uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r pyproject.toml && cd ..
# e2src/nltk_data/ (redownloadable; NLTK refuses world-writable dirs: download to ~/nltk_data first, then copy)
e2src/.venv/bin/python -c "import nltk; [nltk.download(p, download_dir='e2src/nltk_data') for p in ('wordnet','omw-1.4')]"
# frozen/nltk_data/ (redownloadable)
e2src/.venv/bin/python -c "import nltk; [nltk.download(p, download_dir='frozen/nltk_data') for p in ('wordnet','omw-1.4','words','stopwords')]"
# e2src/.pytest_cache/ (regenerable)
cd e2src && .venv/bin/python -m pytest -q -c pytest.ini tests/test_fol.py && cd ..
```

The scoring environment `env` is a symlink to a local-disk venv outside this folder. Recreate it from `pyproject.toml` with
`uv venv env/.venv --python=3.12 && uv pip install --python=env/.venv/bin/python -r pyproject.toml --extra-index-url https://download.pytorch.org/whl/cu128`
(see `reproducibility.md` §2).
