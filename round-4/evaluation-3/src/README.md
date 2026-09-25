# T8: predicting the vocabulary fix, a second population, iteration-5 power, and a verified record

This is an iteration-4 evaluation artifact of run `run_u75jRHUss0zo`. It runs on **CPU only, makes no LLM calls and spent $0**, and never reads the sibling CSC experiment's outputs.
Every quantity is computed from files produced by earlier rounds, which are read-only at absolute paths. The eval-2 functions (`row_consensus`, `pairwise_matrix`/`work`,
`ed_decomposition`, `scatter_index`, `net_test`, `gee_fit`, `SentBoot`, `record.get`/`md_tables`) are **imported unchanged** from the eval-2 workspace. Its code sha
`dd73975642f428cc` is identical to the one eval 2 recorded.

**E and R_COMP are development data.** Everything in Parts 1-2 is mechanism and selection evidence. None of it is confirmation.

## Results in one table

| Quantity | Value [95% sentence-cluster CI, B = 2000] | Source |
|---|---|---|
| Gates | **G0** END_MAJ e 0.1249 / d 0.5371 (targets 0.124 / 0.537), AUROC c_exact 0.748, c_align 0.784: PASS. **G1** pairs_E coverage 100% of 25,358 (candidate, peer) pairs. **G2** exp-8 align_eq vs matrix 99.97% (8 disagreements; the matrix wins). **G3** recomputed R_COMP c_score_sig / c_score_align (SIG, FREE) = exp 7 on 100% of 2,140 / 2,190 / 2,254 rows | `results/part1.json`, `results/part2.json` |
| Prereg | `prereg_d_split.json`, sha256 `2e28bd81…`, written 07:12:31 UTC, before Part 1 ran at 07:18 | `prereg_d_split.sha256` |
| **Part 1, 3-pool (PRIMARY)**: d under rules | exact 0.683 · END_MAJ **0.415** [0.348, 0.487] · R_name 0.415 · **R_point_label (prediction) 0.402** [0.336, 0.471] · R_liberal 0.396 · **no-anchoring oracle floor 0.385** (labelled denominator 0.345) | `tables/p1_rule_cuts.csv` |
| Part 1, 3-pool: e under rules | END_MAJ 0.157 · R_point_label (e_ceiling) 0.162 · R_liberal 0.171 | same |
| Part 1, 9-family (secondary) | END_MAJ d 0.537 · R_point_label 0.532 · R_liberal 0.522 · oracle **0.586** (> END_MAJ) | same |
| Where d comes from (pairs of a CORRECT candidate with a non-agreeing peer) | 9-family: **77% of those peers are labelled ERROR**, 13% CORRECT, 10% unlabelled. 3-pool: 61% / 28% / 11%. Among CORRECT-CORRECT disagreements only 9% are NF/HYB-resolvable (VOCAB); 91% are IRREDUCIBLE for every instrument we own | `tables/p1_class_shares.csv` |
| Pair classes (9-family, 25,358 pairs) | EXACT 13.6%, NAME_ONLY 0.3%, ALIGN_ONLY 15.1%, VOCAB 1.6%, IRREDUCIBLE 69.4% | same |
| Specificity placebo (VOCAB vs random IRREDUCIBLE pairs) | ratio 1.98 [0.43, 11.4] (3-pool); 0.83 [0.19, 3.29] (9-family). Label-shuffle audit: the VOCAB share is identical for CORRECT and ERROR candidates (−0.0014 vs null −0.0012 [−0.005, 0.002]). **VOCAB agreements are not label-specific** | `results/part1.json`, `audit/rederive.json` |
| Graded counterfactual c_vres (liberal vocabulary) | R_AB AUROC 0.780 vs c_score_align 0.784. **L25: −0.014 [−0.028, −0.001] vs c_score_align** (9-family); −0.032 [−0.079, 0.010] (3-pool) | `results/part1.json` c_vres |
| d slope over words (GEE, CORRECT rows) | R_align +1.99, R_point_label +1.98 per SD (9-family); the slope difference is +0.021 [−0.048, 0.084]. 3-pool: +1.60 vs +1.39, difference +0.25 [0.03, 0.55] | `results/part1.json` gee |
| NET Δ(e+d) words T3 − T1 | DEGRADES under **every** rule: R_align +0.354 [0.198, 0.492], R_point_label +0.368, R_liberal +0.368 (9-family); 3-pool R_align +0.390, R_point_label +0.348 | `results/part1_net.json` |
| **Part 2, SIG vs FREE** (same sentence, same cross-family slot pair; 8,088 pairs, 218 sentences) | exact agreement SIG **0.528** vs FREE **0.048**: drop **+0.479 [0.447, 0.513]**. FREE ALIGN 0.246, NF 0.136, ALIGN∪NF 0.266. **Post-hoc recovery of the drop: ALIGN 41%, NF 18%, ALIGN∪NF 45% [41%, 50%]**. Condition-permutation placebo 0.000 [−0.014, 0.015] | `results/part2.json`, `figures/fig_sig_vs_free_agreement.*` |
| Part 2, row endorsement (2,010 rows) | END_MAJ SIG 0.575 vs FREE 0.193 (+0.382 [0.332, 0.434]). Classes per sentence (eqmv, peer rows): SIG 3.4 vs FREE 5.1; plurality share 0.69 vs 0.49 | same |
| **Out-of-sample validation of the Part-1 method** | Predicted FREE endorsement (R_name 0.193, R_liberal 0.210, R_point_MC 0.202) vs actual SIG 0.575: **calibration error −0.372 [−0.423, −0.323]. NOT VALIDATED** (the bar was ≤ 0.05). The template ranking is preserved (Spearman 0.97) | `tables/p2_validation_by_template.csv` |
| Part 2, SIG mechanism (unchanged functions) | e 0.000, d **0.2596** (the exp-7 gate is reproduced exactly); d weak reading 0.143 / strong 0.965; SI_err 0.188 vs SI_cor 0.835, ratio 4.38 [3.18, 6.33] | `tables/p2_sig_ed_cuts.csv` |
| Part 2, FREE tier A (418 ERROR / 34 CORRECT, descriptive) | END_MAJ e 0.191, d 0.324 | `results/part2.json` |
| **Part 3, yields (sentences built → usable R_AB)** | L25 **0.37** (111/300), L20 0.53, EXC 0.64, CTRL 0.25 | `power_E2.json` |
| Part 3, planned E2 cells (vs flash-lite disguised) | L25 250/300/350/400 → ~92/111/130/148 usable → MDE80 0.130/0.119/0.110/0.103, power at 0.069 = 0.32-0.47: **all MARGINAL**. EXC 75/100: MARGINAL (0.125/0.108). L20 50: UNDERPOWERED (0.191). DT 100: UNDERPOWERED unless yield ≥ 0.8 | `tables/p3_planned_E2.csv` |
| Part 3, n needed | +0.069 on L25 at 80% power: **~326 usable = ~882 planned L25 sentences**. MDE 0.10: ~156 usable = ~422 planned. Long pool: ~237 usable for 0.069. SE ∝ n^−0.50 (fitted b = −0.503) | `power_E2.json` n_needed |
| Part 3, R_COMP FREE | With 34 CORRECT rows, MDE80 is 0.16-0.19 whatever the ERROR count. It needs ≥ 200 CORRECT rows to reach ~0.09-0.11 | `tables/p3_rcomp_free_scenarios.csv` |
| **Part 4, record** | 64 claims: **60 match, 1 mismatch, 0 NOT_IN_FILES** (3 context rows). The mismatch is the plan's `$0.000996 per candidate` peer-generation cost, a literal that is not in the hypothesis. The source gives $0.000116 per candidate and $0.00116 per SENTENCE, i.e. a unit error. Wording fix: "26.8% of controls at c = 1" holds for NON-RENAME controls only (42.8% counting all controls) | `record.md`, `tables/record_claims.csv` |
| Audit (`audit/rederive.py`, independent loops) | **11/11 pass**. The analytic (Poisson-binomial) d_floor_pred matches the MC value within 8e-5; deterministic rules match to 1e-9; the SIG-FREE drop matches to 1e-9; the L25 MDE is within 1.3% (sklearn AUROC); 5 headline numbers are re-read from raw files | `audit/rederive.json` |

## What this means for the CSC result (the pre-registered prediction and how to read it)

1. **The post-hoc vocabulary instruments predict almost no fix.** On the matched 3-pool, END_MAJ d is 0.415. The instrument bracket is [0.396, 0.415], with point 0.402.
   The pre-registered `gap_closed` rule therefore has a denominator of only 0.013. It is **ill-conditioned**: any CSC d below 0.406 would read as "vocabulary was the main cause". We report this rather than hide it. The rule stays as registered, but it cannot discriminate.
2. **The instruments are shown to under-count.** Part 2 is the one setting where the true effect of a shared vocabulary is known. There, the Part-1 method predicts 0.20 endorsement against an actual 0.575. Post-hoc ALIGN∪NF recovers only 45% of the agreement a shared vocabulary creates. So "vocabulary divergence is small" is **not** supported. What is supported is that "our instruments cannot see most vocabulary divergence".
3. **The label-based bound does not depend on any instrument.** Most of the peer disagreement behind d on E is with peers **labelled ERROR**: 61% on the 3-pool, 77% on 9 families. No vocabulary fix can turn those into agreements unless the peers copy the candidate (anchoring). The no-anchoring oracle floor is therefore the informative reference:
   - **3-pool d_oracle = 0.385** (0.345 with a labelled-only denominator);
   - **L25: 0.542** (vs END_MAJ 0.735);
   - on 9 families, oracle 0.586 > END_MAJ 0.537, because most peers are wrong.

   **Reading guide for the sibling's CSC d (3-pool):**
   - **d_CSC ≈ 0.40-0.415**: nothing beyond what post-hoc alignment already does.
   - **0.385 ≤ d_CSC < 0.40**: consistent with shared vocabulary removing CORRECT-CORRECT divergence that the instruments miss.
   - **d_CSC < 0.385 (0.345)**: below the no-anchoring floor. Anchoring (peers adopting the candidate's reading) or tier-B label noise must be contributing. Read it with CSC's e, which must then rise; our e_ceiling is 0.162.

   Two caveats apply:
   - The tier-B panel over-calls ERROR (majority accuracy 0.727), so the floor is soft.
   - This reading guide is an interpretation added after the prereg. It is **not** a pre-registered rule.
4. **Pre-check for G2 (CSC > c_score_align on L25).** The label-free no-anchoring counterfactual c_vres does **not** beat c_score_align on L25 (−0.014 [−0.028, −0.001]). The plan's logic then predicts that G2 fails for reasons other than anchoring. That prediction holds unless CSC's in-prompt vocabulary sharing does far more than post-hoc alignment, which Part 2 shows is possible.
5. **Length degradation is not a vocabulary artefact that the instruments can remove.** NET stays DEGRADES and the d-slope is unchanged under R_point_label (9-family slope difference +0.02 [−0.05, 0.08]).
6. **Iteration 5 power.** Under E's yield (L25 0.37), even L25 = 400 gives MDE80 ≈ 0.10 and power 0.47 at +0.069. Recommendations:
   - either build **~880 L25 sentences**, or raise the yield: only 37% of built L25 sentences contributed any R_AB row;
   - or **pre-declare the long pool (L25+L20+EXC) as criterion (c)'s primary cell** (~237 usable sentences for 0.069).
   - Criterion (c) on R_COMP FREE needs **≥ 200 labelled CORRECT rows**.

## Reusable functions (each takes (text, fol) or sets of formulas; label-free unless stated)

| Function | What it measures |
|---|---|
| `src/t8_classes.py: name_only_eq(fol_a, fol_b)` | Whether two formulas are z3-exactly equivalent after both vocabularies are normalised (lowercase, strip non-alphanumerics; arity must agree; an in-formula collision disqualifies). In other words: do they differ only in how their symbols are *spelled*? Returns `(True/False/None, reason)`; UNKNOWN = None |
| `src/t8_classes.py: name_only_prefilter(fol_a, fol_b)` | The sound, cheap reason a pair cannot be NAME_ONLY (`signature_differs`, `same_signature`, `collision`, `unparseable`), or `'z3'` if a solver call is needed |
| `src/t8_part1.py: endorse_det / endorse_mc` | Endorsement of every candidate under the counting rules R_exact / R_align / R_name / R_liberal / R_oracle (deterministic) and R_point_MC / R_point_label (500 MC draws). **R_point_label and R_oracle use gold-side labels: they are oracle-assisted predictions, never gold-free metrics** |
| `src/t8_part1.py: ed_ci(y, en, W)` | e, d and AUROC_b with sentence-cluster CIs for binary endorsements or MC draws (replicate b uses draw b mod 500) |
| eval-2 `pairwise_matrix`, `ed_decomposition`, `scatter_index`, `net_test` | Unchanged, now applied to R_COMP (`pairwise_classes_RCOMP.jsonl`, with a `condition` field) |

## Deviations and caveats

- **D1: NET AME refits use B = 200.** The host was shared (load average ~180 on a 4-CPU cgroup). The Δ(e+d) CIs use B = 2000, computed by vectorised code identical to `net_test`'s first block (`full_B2000_delta`). The unchanged `net_test` output at B = 200 is stored next to it.
- **D2: NAME_ONLY adds a signature prefilter.** The normalised (name, arity) multiset and the constant set must be equal before z3 runs. Pairs whose original signatures already coincide are excluded, because renaming cannot create an equivalence there. Only 16 of 8,988 node pairs needed z3, and 10 were NAME_ONLY. Spelling variants are essentially absent: vocabulary divergence is about word choice, not spelling.
- **D3: ALIGN_ONLY includes eqmv's `gran` reason** (1,165 E pairs), because END_MAJ counts it. Declared in the prereg.
- **D4: R_oracle for ERROR candidates** is defined as "> half of peers ERROR with the same error_ops class" (descriptive). The oracle e values are therefore not comparable to END_MAJ e.
- **D5: R_COMP `net_test` n_conditions contrast.** R_COMP has only n_conditions 4 and 5, so they are mapped to the function's '0-1' and '4+' labels: the "ncond" contrast means 5 minus 4. R_COMP word terciles W1/W3 map to T1/T3.
- **D6: validation population.** The out-of-sample validation uses few-shot (peer) rows paired by (sentence, slot). FREE zero-shot rows are candidates only in exp 7 and are not peers here either.
- **D7: SIG changes more than vocabulary.** The signature prompt can also change granularity and structure, so the SIG−FREE drop is an upper bound on the pure-vocabulary effect. Part 2 validates vocabulary *sharing in general*, not CSC's anchoring.
- **D8: DT power has no E analogue.** It uses the 'all' SE curve with yields {CTRL 0.25, 0.3, 0.5, 0.8}.
- **D9: specificity placebo capping.** In 2 sentences per draw there were fewer IRREDUCIBLE pairs than VOCAB pairs, so the draw took all of them (`n_sentence_draws_capped` = 400 over 200 draws).
- **D10: rewritten bytecode caches.** Importing eval-2 rewrote its `__pycache__/*.pyc` (regenerable bytecode, which eval-2's manifest marks as such). No source file outside this workspace changed: the code sha is identical and 0 non-pyc files are newer. `run_all.sh` sets `PYTHONDONTWRITEBYTECODE=1`.
- The 3-pool excludes 52 candidates that have no {deepseek, microsoft, openai} peer row (counted in `part1.json`).
- Tier-B labels over-call ERROR, which inflates e and makes the oracle floor soft.

## How to run

```bash
uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml
.venv/bin/python eval.py              # full pipeline (prereg -> matrix -> Parts 1-4 -> figures -> audit -> eval_out.json)
.venv/bin/python eval.py --skip-matrix --from part1   # reuse the stored R_COMP matrix
```
See `reproducibility.md` for versions, seeds and runtimes.

## Restoring removed files

| Removed path | Restore with |
|---|---|
| `.venv/` | `uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml` |

## Layout

| Path | What |
|---|---|
| `prereg_d_split.json` / `.sha256` | Pre-registration: classes, rules, 0.388 discount (read from exp 8), cuts (from eval 2), pools, decision rule, validation criterion, power grid |
| `src/t8_run_rcomp_matrix.py` → `results/pair_matrix_RCOMP.jsonl`, `pairwise_classes_RCOMP.jsonl` | R_COMP eqmv matrix (442 tasks, 11,912 pairs, 0 UNKNOWN), staged mini → 50 → all |
| `src/t8_part1.py`, `src/t8_part1_net.py` | Part 1 → `results/part1.json`, `results/part1_net.json`, `tables/p1_*.csv` |
| `src/t8_part2.py` | Part 2 → `results/part2.json`, `tables/p2_*.csv` |
| `src/t8_part3.py` | Part 3 → `power_E2.json`, `tables/p3_*.csv` |
| `src/t8_part4.py`, `src/t8_record_md.py` | Part 4 → tables (a)-(m): `hypothesis_verdicts_iter3.csv`, `delta_per_stratum.csv`, `perturb_corrected.csv`, `rename_selection_dead_end.csv`, `t2_record.csv`, `deviations.csv`, `cost_units.csv`, `coverage_vs_request_iter3.csv`, `function_inventory.csv`, `label_facts.csv`, `corrections_iter12.csv`, `artifact_id_map.csv`, `prior_art.csv`; plus `record_claims.csv`, `record_mismatches.csv`, `source_hashes.csv` and `record.md` |
| `figures/` | `fig_d_floor_vs_words`, `fig_sig_vs_free_agreement` (PDF, PNG and a JSON spec each) |
| `audit/rederive.py` → `audit/rederive.json` | Independent re-derivation and placebos |
| `eval_out.json` (+ full/mini/preview) | exp_eval_sol_out (validated): 157 flat metrics; 2,672 E rows and 4,862 R_COMP rows |
| `eval.py` / `run_all.sh` | Full reproduction in plan order (`eval.py --skip-matrix` reuses the stored R_COMP matrix); `reproducibility.md` has the exact environment, commands, seeds and runtimes |
