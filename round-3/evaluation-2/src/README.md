# Do wrong NL→FOL translations scatter? A consensus-mechanism audit (T4 on dataset E), plus a verified record

This is an iteration-3 evaluation artifact of the AI-Inventor run `run_u75jRHUss0zo`. It is **CPU only and spent $0 on OpenRouter: it makes no LLM calls.**
Workspace (kept artifacts live here, by absolute path):
`.`

The artifact has two parts, both computed in one pass over dataset E:

- **A. Mechanism (T4).** Why does cross-family solver consensus (`c_score_align`) predict NL→FOL faithfulness? The
  "Anna Karenina" premise says correct translations converge while errors scatter. To test it:
  - We recompute the **label-free pairwise z3 equivalence-modulo-vocabulary (eqmv) matrix** among every parseable output of each of the 700 E sentences (29,107 node pairs). It uses exactly the iteration-1 `eqmv` behind the frozen score.
  - We prove that it reproduces exp 5's **frozen** `c_score_align` (gate G2).
  - We decompose binary majority consensus exactly as `AUROC_b = 1 − (e + d)/2`. Here **e** is the error-endorsement rate (ERROR rows endorsed by the cross-family peer majority) and **d** is the correct-divergence rate (CORRECT rows not endorsed). This is balanced accuracy, a *bookkeeping identity*, not a novel result.
  - We model e (M1) and d (M2) against complexity, test the NET balance, measure the scatter index, and run M4 peer-count scaling, fixed pools, leave-one-family-out (LOFO) and $/CPU cost.
- **B. Verified record.** Every iteration-2 number that the review flagged is re-read programmatically from files. Each CSV
  starts with `# source: <abs path> :: <key path>` lines. A value not found in any file would be written `NOT_IN_FILES`; after the fixes in this run, none remain.

## Headline results (R_AB = tiers A+B, CORRECT/ERROR, LLM rows, no reading_choice; 2,672 consensus-scorable rows, 283 sentences)

| Quantity | Value [95% sentence-cluster bootstrap CI, B=2000] |
|---|---|
| Gates | **G0** R_AB 2686 (1822/864, 292 sent), R_A L20+EXC 449 (261/188): PASS. **G1** frozen AUROC 0.7824 (0.782) and 0.8599 (0.860): PASS. **G2** re-derived c = frozen on 99.67% of 7,383 rows (24 mismatches, 7 in R_AB; ≤0.5% accept rule), 0 UNKNOWN pairs, `|P_c|<2 ⇔ None` 0 violations |
| Matrix | 29,107 pairs: 26,184 none, 1,473 align, 1,165 gran, 285 exact. Median pair 0.005 s, max 3.2 s. **Bit-identical across 3 independent recomputations** (`results/matrix_determinism_check.json`) |
| Non-transitivity of eqmv | 15.8% of wedges (a~b, b~c, a≁c), L25 21.7%. **>5%, flagged**: "classes" are approximate (components vs greedy cliques both shipped) |
| Graded c_score_align vs END_MAJ binary | 0.784 vs 0.669; Δ = +0.114 [0.091, 0.140]. Majority voting throws away much of the signal |
| END_MAJ e / d | e = 0.124 [0.086, 0.164]; d = 0.537 [0.456, 0.619]. **d, not e, is the blind spot** |
| Other rules (AUROC_b) | PLUR 0.714, FAM2 0.748 (e 0.299, d 0.204), FAMMAJ 0.702, MAJ_EXACT 0.627 |
| Aligner-free c_score_exact | AUROC 0.748; align − exact = +0.036 [0.010, 0.062]. 53% of endorsements need align/gran (75% for ERROR rows, 38% for CORRECT) |
| VOCAB_EXACT (pure-z3 label, no aligner on the label side; 85 ERR / 412 COR, testable) | κ vs dataset label 0.910. c_score_align AUROC 0.929 vs y_exact; c_score_exact 0.892 |
| **M1** (e falls with n_conditions, GEE partial slope) | −0.04 [−0.53, 0.45]: **INCONCLUSIVE**. The words slope carries it (−0.77 [−1.39, −0.14]). Words and n_conditions are collinear (r = 0.70, VIF up to 11 with stratum dummies). Exploratory single-predictor fits are negative (n_conditions −0.76 [−1.16, −0.37]), so the Eckhardt-Lee/Knight-Leveson rival (positive slope) is not supported |
| **M2** (d rises with words) | +1.95 [1.12, 2.77] per SD: **CONFIRMED** by the pre-registered rule in every sensitivity. d = 0.73 for correct-but-not-equivalent rows vs 0.32 for reference-equivalent rows. **But it is NON-SPECIFIC** (audit): with shuffled labels the same fit still gives +1.75 [1.04, 2.45]; ERROR rows diverge with length almost as steeply (label×words interaction −0.29 [−0.77, 0.20]); only a small label-specific part survives a within-sentence shuffle (p = 0.005). Long sentences lose endorsement for *every* output |
| **NET** Δ(e+d), words T3 − T1 | +0.356 [0.198, 0.493]: **DEGRADES with length; driver = d** (Δe −0.252, Δd +0.608). n_conditions 4+ vs 0-1: +0.319 [0.129, 0.502] degrades. Long pool, words: degrades. Long pool, n_conditions: balanced |
| **SCATTER** | SI_err 0.159 [0.131, 0.189] vs SI_cor 0.760 [0.706, 0.810]; ratio 4.45 [3.57, 5.77]. SI_err falls with n_conditions (pair GEE −0.64 [−1.00, −0.28]): **CONFIRMED**. Joint failure P(both ERROR) *rises* 0.32→0.62 while identical-wrong stays 0.10–0.12 at 3/4+ conditions: errors co-occur but differ |
| M3-local (secondary) | Correctness slope, consensus − local judge (flag rate matched exactly) = +0.07 [−0.13, 0.23]: INCONCLUSIVE |
| **M4** AUROC(k), rows with all 7 other families (n = 2014) | k = 1…7: 0.685, 0.738, 0.757, 0.770, 0.776, 0.780, 0.784. **k95 = 3: CONFIRMED** (≤ 5). Per words tercile, k95 T1/T2/T3 = 2/3/5: long sentences need more peers |
| Fixed 3-family pool (cross-fitted on exp 6 folds_E) | deepseek+microsoft+openai, picked in 5/5 folds. Out-of-fold AUROC 0.785 = the full pool. Worst pool (cohere+meta+qwen) 0.697 |
| LOFO | Minimum Δ = −0.011 (deepseek). All LOFO AUROCs > 0.712: NO_SINGLE_FAMILY_CARRIES_EFFECT |
| Cost | Generation $/sentence ≈ $0.00032·k (expected over random k-subsets; the openai family is dearest at $0.0019). Best 3-pool $0.0020/sentence vs frontier judge $0.0029/call. Solver ≈ 0.016 CPU-s per family per candidate (mean pair 0.011 s) |
| Independent audit (`audit/`) | 13 headline numbers re-derived from raw files with separate code: all match to 1e-9. AUROC permutation p = 0.001 (null max 0.539). Placebos with shuffled labels fail as they should for NET (−0.034 [−0.108, 0.034]), M1 and SCATTER. **They do not fail for M2** (see above) |
| Verified record | 48 of 48 checkable clauses VERIFIED_MATCH. The reviewer's PT − S4 audit reproduces to 1e-4 (points) and 0.01 (CIs). Stratified PT − S4_local +0.059 [0.023, 0.093] |

**Interpretation.** The premise is half right. Errors do scatter:
- identical-wrong rates are low and fall with conditions (SCATTER, and e falls with length);
- the rival N-version prediction (coincident failures concentrate on hard inputs) is not supported for *identical* wrong outputs, although joint failures do rise.

However, on long and heavily conditioned sentences, correct outputs **also** stop agreeing (d → 0.8–0.9), mostly legitimately (vocabulary and granularity divergence among correct-but-not-equivalent rows). So binary majority consensus *degrades* with complexity. The graded score degrades less, and adding peers helps most on long sentences.

Because M2 is non-specific, the label-specific evidence is NET (d rises much more than e falls) and SCATTER (identical-wrong ≪ identical-correct). "d rises with words" alone would also hold if labels were random.

Caveats:
- Tier-A CORRECT labels are aligned-equivalence to the reference. Tier-A CORRECT rows are exactly the VOCAB_EXACT CORRECT rows (412/412), so the label side of d needs no aligner, while the consensus side does.
- The panel (tier B) over-calls ERROR (majority accuracy 0.727), which inflates e.

## Scope limits and deviations (also in `prereg_mech.json` → `deviations`, and `eval_out.json` → `metadata`)

- **D4: E only.** R_COMP has no candidates or labels yet; the iteration-3 T2 experiment owns them. `pairwise_matrix()` (src/pairwise.py) and `ed_decomposition()` (src/mechanism.py) are shipped so iteration 4 can apply them unchanged.
- **E is development data**, not pristine held-out: it was scored in iteration 2. Nothing is tuned here except the fixed pool, which is cross-fitted. The prereg guards against analysis-choice drift, **not** against label peeking.
- **D1:** eqmv timeout is 3000 ms, not the direction's 2 s, because reproduction needs identical settings.
- **D2:** k = 1..7 (8 vendor families), not 1..9. The slot-level sensitivity (`family` field) goes to k = 9 on 856 rows (k95 = 3).
- **D3:** the G2 mismatches (0.33%). eqmv's align/fingerprint iterate Python sets/str-hashes, which depend on PYTHONHASHSEED. Exp 5 set the seed inside spawned workers, which has no effect, so its hash seeds were random. `results/diag/` re-runs the mismatch sentences under 6 seeds, and 3 of 387 pairs flip. This artifact runs everything under PYTHONHASHSEED = 0. Every AUROC of `c_score_align` uses the FROZEN column.
- **D5:** the prereg was written after the label-free matrix and before any label join.
- **M1/M2 collinearity:** partial slopes with a VIF are reported. The EXPLORATORY single-predictor fits are labelled as such and are not the pre-registered test.
- **M3-local:** the local judge score is discrete (0, .05, …). The primary flags exactly END_MAJ's flag rate (top rows by score, boundary ties split by `sha1('M3|'+row_key)`). The nearest plain threshold (0.05, flag rate 0.877) is a sensitivity (+slope diff −0.10 [−0.30, 0.08]). The API-judge M3 belongs to T1.
- **Cost:** each slot is costed per sentence it actually covered (F = GPT-5.1 covers 200 sentences; G1b/G4/G5/G7/G8 cover 600), and a family's cost is the sum of its slots. The "as-run" totals/700 are also kept.
- **Unparseable rows:** none in R_AB. Unparseable rows elsewhere get no matrix node and are listed per sentence (`unparseable_row_keys`). 14 R_AB rows with `|P_c| < 2` are excluded from the consensus-scorable population, with counts in `population`.
- **G0 cross-check:** our R_AB flag agrees with exp 6's `metadata_in_R_AB` on 97.0% of rows. All 255 disagreements are non-LLM rows (240 gold-as-system, 15 ccg2lambda), which exp 6 included and exp 5's `regime()` excludes.

## Layout

| Path | What |
|---|---|
| `eval.py` | Orchestrator: copies inputs → matrix (staged) → PART A → PART B → figures → `eval_out.json` |
| `src/pairwise.py` | **`pairwise_matrix(rows)`**: reusable label-free eqmv matrix for one sentence (vendored exp 5 eqmv, 3000 ms, 30 s pair cap) |
| `src/run_matrix.py` | Staged, resumable, parallel (spawn, 4 workers, RLIMIT_AS 3.5 GB) matrix driver (`--stage mini/rab/rest`) |
| `src/consensus_mx.py` | Matrix readouts: re-derived c (G2), c_exact, END_MAJ/PLUR/FAM2/FAMMAJ, classes, cliques, non-transitivity |
| `src/mechanism.py` | **`ed_decomposition(y, endorsed)`**, cuts, graded trace, VOCAB_EXACT helpers, GEE, M1/M2/NET/SCATTER/M3-local |
| `src/m4.py` | AUROC(k), fixed pools (cross-fitted), LOFO, cost table |
| `src/frame.py`, `src/stats.py`, `src/paths.py` | Join + gates G0/G1; AUROC, stratified AUROC, sentence-cluster bootstrap (multiplicity weights); input paths |
| `src/part_a.py`, `src/record.py`, `src/copy_inputs.py` | PART A driver; PART B verified record (i)–(x); input copy + sha256 |
| `vendor_exp5/` | Read-only copy of exp 5 `src/` (peer_text, pool_scoring, vendor_c/common.py eqmv, …); hashes in `tables/source_hashes.csv` (identical_to_source=True) |
| `audit/rederive.py`, `audit/m2_specificity.py` (+ `.json`) | Independent re-derivation of headline numbers (no `src/` import) + placebo tests; M2 specificity (interaction model, permutation nulls). Run by `eval.py` |
| `reproducibility.md` | Exact environment, commands, seeds, runtimes and expected numbers |
| `tests/test_identity.py` | 23 unit tests (identity, weighted AUROC = duplication, trapezoid, matrix readouts). `uv run pytest -q tests` |
| `prereg_mech.json` (+`.sha256`) | Every analysis choice: rules, bins, frozen tercile cuts, GEE spec, confirm rules, seeds, B, min cells, deviations |
| `results/pair_matrix_E.jsonl` | Raw matrix, 700 sentences (label-free) |
| `pairwise_classes_E.jsonl` | **Join key for iteration 4**: per sentence, nodes/rows/families, pairs [i, j, equiv, reason, secs], components, cliques, non-transitive triples, z3 version, code sha. **No labels** |
| `results/part_a.json` | Every PART A number (gates, G2, population, cuts headline, M1–M4, SCATTER, cost …) |
| `results/population_RAB.pkl`, `results/rab_all.pkl`, `results/frame_min.pkl` | Analysis frames (regenerable) |
| `results/matrix_determinism_check.json`, `results/prev_run*/` | Two earlier matrix computations; 0 of 29,107 pairs differ |
| `results/diag/` | PYTHONHASHSEED diagnostic for the G2 mismatches |
| `tables/ed_decomposition_cuts.csv` | e, d, AUROC_b, AUROC(c) with CIs by regime (R_AB, R_A, VOCAB_EXACT) × rule × {ALL, stratum, long pool, words tercile, n_conditions bin, exception type, tier} |
| `tables/graded_trace_*.csv`, `tables/g2_mismatches.csv`, `tables/scatter_sentence_table.csv` | Graded ROC traces; G2 mismatch rows; per-sentence SI |
| `tables/m4_*.csv` | AUROC(k) + cost frontier; all fixed pools k = 2/3/4; LOFO |
| `tables/exp6_*.csv`, `b2_dead_end.csv`, `radj_gate.csv`, `pt_vs_s4_rerun.csv`, `corrections.csv`, `regimes_R_PANEL.csv`, `hypothesis_verdicts.csv`, `coverage_vs_request.csv`, `function_inventory.csv`, `perturb_counts.csv`, `label_facts.csv` | PART B verified record (i)–(x) |
| `figures/fig1…fig4 (.png/.pdf/.json)` | e/d vs complexity; AUROC(k) + $; SI_err vs SI_cor; graded ROC with named operating points |
| `eval_out.json` (+ `full_/mini_/preview_`) | `exp_eval_sol_out`: 324 `metrics_agg`, verdicts/deviations in `metadata`, one example per R_AB row (2,686) with `predict_c_score_align` (frozen), `predict_c_score_exact`, `predict_b_endmaj/endfam2/endplur/endfammaj`, `predict_c_k3_best_oof` |
| `inputs_copy/` | Every small (<10 MB) input actually read, mirrored under `3_invention_loop/…` (large inputs are referenced by absolute path) |
| `logs/` | Run logs (`eval_full_run.log` = the final run) |

## How to run

```bash
uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml   # z3-solver==5.1.0.0 pinned (= exp 5)
uv run pytest -q tests                        # 23 tests
uv run eval.py --stage mini                   # 12-sentence matrix smoke test
uv run eval.py --stage rab                    # matrix for the 292 R_AB sentences + every analysis
uv run eval.py --stage all                    # all 700 sentences (≈ 2 min matrix + 3 min analysis on 4 vCPU)
uv run eval.py --stage all --skip-matrix      # analyses only, reusing results/pair_matrix_E.jsonl
```

The matrix stage appends to `results/pair_matrix_E.jsonl` and skips sentences already present. Move that file away to force a recompute. `eval.py` re-executes itself with `PYTHONHASHSEED=0`.
To regenerate the mini/preview files: `python .claude/skills/aii-json/scripts/aii_json_format_mini_preview.py --input eval_out.json`.

## Restoring removed files

`.aii/manifest.yaml` marks only these for deletion:

- `.venv/` (regenerable): `uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml`
- `__pycache__/`, `src/__pycache__/`, `tests/__pycache__/`, `vendor_exp5/**/__pycache__/`, `.pytest_cache/` (regenerable): created automatically by `uv run eval.py` or `uv run pytest -q tests`

Everything else (results, tables, figures, the matrix, `pairwise_classes_E.jsonl`, `eval_out*.json`, prereg, code, inputs copy) is kept.
