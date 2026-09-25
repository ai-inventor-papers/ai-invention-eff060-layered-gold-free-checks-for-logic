# Re-checking the iteration-1 numbers under every label set (NL→FOL faithfulness metrics)

This is a CPU-only re-analysis of the four iteration-1 artifacts of run `run_u75jRHUss0zo`, with **zero LLM spend**:

- exp A: FOL-Triage (fused_H, L1/L2/L3);
- exp C: peer consensus (`c_score`);
- exp D: judges, round-trip, self-consistency and pilot baselines;
- dataset E: screen adjudication (solver + strict 3-model panel).

It joins every per-item score on `item_id` and reproduces the reviewer's audit numbers independently. It then scores every metric on the **same items with the same label vector**, under 13 label regimes, and gives a clearly labelled **SCREEN PREVIEW** of the PEER+TEXT fusion (PT = cross-fitted logistic on `[c_score, bow_uncarried, l3_score]`) and of the P1/P2 mechanism predictions.

> Scope. The screen is FOLIO-dev Logic-LM outputs of three 2023 OpenAI systems: short sentences, with the long and heavily conditioned strata untestable. The regimes are the screen's own labels only (solver vs strict panel). Every PT/P1/P2 number is a preview, **not confirmation**. Dataset E's held-out rows were never loaded (firewall, see `eval_out.json → metadata.provenance.firewall`).

## Headline results (all on common item sets; 95% sentence-cluster bootstrap, 2000 resamples, seed 0)

### Re-derivation gate (step 2)
- **57/57** reviewer audit quantities reproduce (`tables/rederivation.csv`). These include:
  - n=389 / 160 errors / 151 sentences;
  - c_score 0.8416, fused 0.767 and judge 0.785;
  - Δ c_score−judge +0.0565 [−0.0222, 0.1369];
  - tier A+B n=304: fused .872, L2-bow .817, c_score .776, judge .771;
  - own-label AUROCs .8655 / .7589 / .7846.
- The reviewer's bootstrap is reproduced exactly with a replica of their RNG stream. The independent bootstrap (numpy, exp D clusters) agrees within 0.005.

### Bookkeeping (step 1)
- The three experiments share 588 track-L ids, of which 398 have label-consistent binary labels (389 with a judge score).
- Every label disagreement is a naming difference (134: UNCERTAIN vs UNCERTAIN_COMPOUND) or one of the reviewer's **16 GRAN items**, which is confirmed: A = UNCERTAIN, C = UNCERTAIN_GRAN, D = CORRECT.
- Exp D's hash `122d01df…` is sha1 over `item_id:label` lines. Exp C's `0e43cbdd…` is **sha256** over sorted `item_id<TAB>label` lines. The two hashes were never comparable.
- Solver→adjudicated transitions:

  | Experiment | CORRECT→ERROR | ERROR→CORRECT |
  |---|---|---|
  | D | 58 | 1 |
  | C | 62 | 1 |
  | A | 55 | 1 |

### Pre-registered iteration-1 rule (step 4)
- **fused_H and c_score FAIL in every regime.** The rewrite-FA clause fails regardless of labels: fused 0.275 and c_score RENAME 0.96, against a limit of 0.10.
- The Δ-vs-judge clause changes with the label regime:

  | Regime | fused_H − judge | c_score − judge |
  |---|---|---|
  | solver-consistent | −0.013 [−0.117, 0.079] | +0.067 [−0.012, 0.148] |
  | adjudicated A+B | **+0.096 [0.020, 0.171]** | +0.006 [−0.082, 0.089] |

### Regime shift (step 5, `figures/fig_regime_shift.*`)
- On the same items with only the labels changed (solver → adjudicated A+B, 161 shared items, 36 label changes):
  - fused_H rises by +0.080 [0.003, 0.171];
  - L2-bow rises by +0.102 [0.018, 0.192];
  - c_score falls by −0.106 [−0.255, 0.013].
- Kendall τ between metric rankings, solver vs A+B: 0.60 [0.28, 0.72].
- Flipped-item diagnostic, on the 58 items D calls CORRECT and E calls ERROR, share flagged at matched FA 0.20:

  | Metric | Share flagged |
  |---|---|
  | L2-bow | 0.81 |
  | fused_H | 0.83 |
  | c_score | 0.34 |

  This supports the instrument-sharing prediction: bow shares lexical sensitivity with the panel, and c_score shares `align()` with the solver.

### PEER+TEXT screen preview (step 6)
- **PT − judge_cheap_disg is above 0 in every testable track-L regime:**

  | Regime | PT − judge_cheap_disg |
  |---|---|
  | solver-consistent | +0.089 [0.010, 0.165] |
  | adjudicated A+B | +0.104 [0.039, 0.175] |
  | adjudicated all tiers | +0.090 [0.038, 0.142] |
  | unparseable counted as ERROR | +0.118 [0.050, 0.188] |

- The standard deviation over 5 fold seeds is ≤ 0.006.
- Nested Δ of S4+PT over the refitted S4: +0.056 / +0.040 / +0.037, all with CI > 0.
- Track H is untestable (fewer than 50 errors): sign only.
- The bootstrap does not refit per resample, so the CI understates model-selection variance.

### P1 / P2 (step 7)
- **P1:** the structural clause is **untestable** on the screen, because every QUANT/SCOPE/BIND/SWAP/NEG cell has fewer than 15 errors. The text-beats-peers-on-peer-endorsed-errors clause holds at FA 0.10 in every regime. Verdict: `PARTIAL_STRUCT_UNTESTABLE`.
- **P2a** (c_score vs text-OOF Spearman among errors ≈ 0.25–0.27): CONFIRMED only for adjudicated all tiers; PARTIAL elsewhere.
- **P2b** (the fusion gain comes from peer-endorsed errors): depends on the comparator.
  - Against c_score, the gain comes from endorsed errors (all tiers: share 1.01 [0.90, 1.18]).
  - Against L2-bow (the best single metric under A+B), the gain comes from non-endorsed errors.
  - This is complementarity in both directions. See `decomposition.PT_vs_*`.

### Judges (step 9)
- At matched FA 0.10, the **original** prompt of the cheap judge has *higher* recall than the disguised one: +0.106 [0.033, 0.178] under solver labels, +0.198 [0.130, 0.260] under A+B. This refutes "the disguised judge reads more carefully".
- **Contamination:** every DiD CI includes 0, but the MDE is 0.12–0.21. A 0.05 contamination effect would be undetectable for every judge.
- The single-track nano disguise drops on H (−0.114) and H_curator (−0.102) reproduce.

### Frontier judge (same items)
- Under adjudicated A+B: strong−cheap (orig) +0.166 [0.086, 0.244], n=90.
- Under solver labels: +0.078 [−0.002, 0.169].

### Invariance (step 10)
- Exp A, C and D used **different rewrite sets**. The rewritten strings coincide only for 14/124 shared RENAME bases (A–D) and some REORDER (A–C) bases.
- Every iteration-1 cross-experiment invariance comparison was therefore NOT_SAME_SET (descriptive only).

### Candidate B (step 11)
- It was planned: `gen_plan_experiment_2` ("Checking logic by reading it back and testing worlds") passed module_end.
- `gen_art_experiment_2` holds only an empty `.aii/` directory: no agent log and no outputs. **The executor never started.**

### Complexity (step 13)
- Exp C's c_score length interaction reproduces exactly: −0.936/SD words vs −0.937 reported.
- Under the same definition the judge shows −0.84/SD.
- The "judge −0.48/SD" figure named in the plan exists in no iteration-1 artifact.

### MUST-FIX transcription (step 8)
- 1,507 rows: 790 MATCH, 627 TRANSCRIBED_ONLY, 60 RECOMPUTED_ONLY, 30 MISMATCH.
- Every mismatch involves metrics that exp D stored as not-applicable on part of a block (strong-subset judges, qwen14b, pilot_rerun_jacc). Diagnosis: `eval_out.json → metadata.mustfix.mismatch_diagnosis`.
- Definition gap found: exp A's reported L2-bow (0.737) is `bow_n_unanch + bow_uncarried`, while the reviewer and PT use `bow_uncarried` (0.711). Both rows are carried.
- Panel calibration recomputed: expert-pair majority accepts **0.635** of corrected formulas (0.613 on the 75 unambiguous pairs, per the card) and flags 0.84 of the originals. Gate balanced accuracy is 0.85.

## Independent re-derivation of the headline numbers (`audit/`)
`audit/rederive_headlines.py` reads the raw iteration-1 files directly and uses a different code path from `eval.py`: scipy Mann-Whitney AUROC, an explicit index-resampling sentence bootstrap with `random`, PT as an sklearn `Pipeline` with sklearn `GroupKFold` in place of exp D's folds, and matched-FA recall by `roc_curve` interpolation. Results are in `audit/rederive_headlines.json`.
- **Exact matches:** the common-set sizes (373/155 and 298/165), the AUROCs of judge, c_score, fused_H, L2-bow and L3 in both regimes, and the label-only shifts (bow +0.102, c_score −0.106, fused +0.080).
- **PT − judge with a different fold assignment:**

  | Regime | Re-derived | eval.py |
  |---|---|---|
  | solver-consistent | +0.086 [0.012, 0.163] | +0.089 [0.010, 0.165] |
  | adjudicated A+B | +0.103 [0.038, 0.176] | +0.104 [0.039, 0.175] |

- **fused_H − judge under A+B:** +0.096 [0.024, 0.175].
- **Matched-FA recall (FA 0.10), orig vs disg:**

  | Regime | orig | disg |
  |---|---|---|
  | solver-consistent | 0.514 | 0.382 |
  | adjudicated A+B | 0.553 | 0.359 |

- **Placebo** (`audit/placebo_permutations.py`, 20 label permutations on the same items and groups):
  - The judge's AUROC under the null is 0.50.
  - Cross-fitted PT under the null is biased **below** 0.5: mean 0.47 (solver) and 0.48 (A+B). This is fold-prevalence anti-learning, so a single permuted draw can give a significantly negative Δ (A+B draw: 0.376).
  - The observed PT−judge Δ exceeds all 20 null Δs in both regimes. The null maxima are 0.047 (solver) and **0.087 (A+B)**, so under A+B the margin over the null is small. With 20 permutations the permutation p is only about 0.05.
- Not re-derived through a second path: the P1/P2 cell verdicts, the contamination MDEs and the MUST-FIX transcription rows. The transcription rows are themselves recomputations against iteration-1 values.

## Layout
| path | content |
|---|---|
| `eval.py` | driver: steps 0-7 inline, then `src/steps_audit.py` (8-13) and `src/outputs.py` |
| `src/stats_utils.py` | AUROC, sentence-cluster bootstrap, fast + clustered (Obuchowski) DeLong, Holm, matched-FA randomised threshold, Wilson |
| `src/load.py` | read-only loaders and the master join (A/C/D/E) |
| `src/steps_core.py` | steps 1-5: bookkeeping, re-derivation gate, regimes, common-item tables, regime shift, τ, flipped items |
| `src/steps_models.py` | step 6 (PT / PT+J / PT+g / S4 refit / S4+PT, exp D model spec, D folds + 4 seeds, F3 preview) and step 7 (P1, P2, placement-value decomposition) |
| `src/steps_audit.py` | steps 8-13: MUST-FIX transcription, judges + contamination MDE, invariance same-set audit, Candidate B, inventory, complexity |
| `src/outputs.py` | `eval_out.json`, VERDICT block, figures |
| `regimes.json` | regime declarations (item sets, n, testability) written before any AUROC beyond step 2 |
| `eval_out.json` (+ `full_`/`mini_`/`preview_`) | exp_eval_sol_out: `metrics_agg` (~5.9k flat keys), `metadata` (all structured results, VERDICT), 1,380 per-item examples |
| `tables/*.csv` | every table; the first line of each is a `# source:` comment. `common_items_<regime>.csv`, `available_case_<regime>.csv`, `regime_shift.csv`, `rank_kendall_tau.csv`, `flipped_items.csv`, `p1_crossover_*.csv`, `p1_diff_*.csv`, `p2.csv`, `mustfix_{A,C,D,E}.csv`, `judge_matched_fa.csv`, `contamination.csv`, `invariance_*.csv`, `frontier_same_item.csv`, `complexity_*.csv`, `coverage_vs_request.csv`, `function_inventory.csv`, `bookkeeping.csv`, `label_disagreements.csv`, `rederivation.csv` |
| `figures/fig_regime_shift.{json,png,pdf}` | metric × regime AUROC heatmap + label-only shift panel (diverging, centred at 0) |
| `figures/fig_forest_common.{json,png,pdf}` | Δ vs disguised cheap judge with 95% CI, one panel per regime; untestable regimes grey, point only |
| `data/panel_calibration.json` | the only group read from dataset E's `full_data_out.json` (77 gate items + 96 expert pairs) |
| `audit/` | independent re-derivation + placebo permutation scripts and JSON outputs |
| `logs/` | run logs |

## How to run
```bash
uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python eval.py          # full run, ~1-3 min on 4 CPUs
.venv/bin/python eval.py --quick  # B=200, 1 fold seed
```
All inputs are read, read-only, from `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/`. Their sha256 hashes are in `eval_out.json → metadata.provenance`.

## Restoring removed files
| deleted path | restore |
|---|---|
| `.venv/` | `uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r requirements.txt` |
| `src/__pycache__/` | regenerated automatically by `.venv/bin/python eval.py` |

Everything else (code, tables, figures, JSON, logs) is small and kept in place.
