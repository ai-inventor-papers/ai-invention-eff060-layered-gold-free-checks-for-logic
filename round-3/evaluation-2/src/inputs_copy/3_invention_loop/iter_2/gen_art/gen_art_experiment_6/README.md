# Every baseline re-run on the held-out NL→FOL set E (iteration 2), plus the B2 world probe

This is the **baseline arm of the iteration-2 confirmation** (run `run_u75jRHUss0zo`, plan `gen_plan_experiment_2`).
Setting: a sentence and a candidate first-order-logic formula, with no gold formula available. Every baseline the user
asked for is scored on **held-out dataset E** (8,507 real candidates for 700 sentences; iteration-1 `gen_art_dataset_1`):
- parse / compile rate;
- the user's pilot structural metrics;
- round-trip (FOL→NL→NLI / embedding);
- LLM-as-judge (original and nonce-disguised);
- sampling self-consistency;
- a cross-fitted stack of all of them (S4);
- the new **B2 world probe**.

Everything uses the same label regimes, item ids, folds and sentence-clustered bootstrap as the sibling PEER+TEXT
confirmation. All settings were frozen in `prereg_baselines.json` (sha256 in `prereg_baselines.sha256`) **before** any
score was written or any E label was joined.

> **Read first — F-KEY deviation.** The run-shared OpenRouter key was already exhausted by other runs when this
> module started (`limit_remaining = 0` at 18:02 UTC; daily reset 00:00 UTC, after this module's deadline;
> `logs/key_poll.log` polled it every 20 min). A replacement key announced at 21:12 UTC was *also* already at its daily
> limit on first use (403 "Key limit exceeded"; `limit_remaining` 0, usage $50.06). `api_chain.sh` then polled it every
> 3 min (`logs/api_chain.log`), ready to run every planned API arm and re-analyse automatically. **No API call
> succeeded ($0 spent).** As pre-planned (fallback F-KEY),
> every LLM component ran locally on the GPU with open-weight models:
> - the judges from exp D's `prereg_local.json`: Qwen3-8B JSON rubric B, and Llama-3.1-8B P(YES);
> - Qwen3-14B-nf4 on the frame instead of the frontier judge;
> - the Qwen3-8B verbaliser;
> - Qwen3-8B SC-5 sampling;
> - the Qwen3-8B B2 reader.
>
> Consequences:
> - The pre-registered API bar (`judge_cheap_disg` = gemini-2.5-flash-lite) and the frontier judge
>   (gemini-3.1-pro-preview) **do not exist in this artifact**.
> - The bar used for every paired Δ is the local `judge_local_qwen8b_disg`, flagged everywhere.
> - The stack is reported as `S4_local`.
> - The API code paths (`--stage judges|sc_gen|verbalise|strong|retest|b2_read_api`) are implemented and cached. They will run
>   unchanged when a key is available; `analysis` then switches the bar back to the API judge automatically.

## Key results
Headline pool: E_POOL (10 LLM slots, 13 system×variant rows), PRIMARY (parseable), label regime **R_AB**: n = 2,686
rows (1,822 ERROR / 864 CORRECT), 292 sentences. CIs are sentence-cluster bootstrap intervals (2,000 resamples, seed 0).
Δ is paired vs the bar on identical rows. Every number is in `results/analysis_E.json` and `results/summary.md`.

**1. Item-level AUROC [95% CI] (oriented; higher = unfaithful)**

| Metric | R_AB pooled | Δ vs bar | R_A (tier A, L20+EXC+CTRL; n=729) | Long pool L25+L20+EXC (n=2,300) |
|---|---|---|---|---|
| **bar** `judge_local_qwen8b_disg` (Qwen3-8B, disguised) | **0.710** [0.674, 0.746] | — | 0.673 [0.585, 0.750] | 0.651 [0.619, 0.680] |
| `S4_local_oof_RAB` (cross-fitted stack of all local baselines) | **0.748** [0.709, 0.782] | **+0.038 [+0.005, +0.069]** | 0.749 (+0.076 [+0.015, +0.145]) | 0.709 (+0.059 [+0.019, +0.097]) |
| `S4_local_noLLMjudge` (pilot + NLI + SC, no LLM judge) | 0.703 [0.660, 0.742] | −0.007 [−0.050, +0.037] | 0.728 | 0.667 |
| `S4_local_plus_B2` | 0.750 [0.711, 0.785] | +0.040 [+0.009, +0.070] | 0.744 | 0.712 |
| `judge_local_qwen8b_orig` (undisguised) | 0.649 [0.604, 0.693] | −0.061 [−0.095, −0.031] | 0.628 | 0.586 |
| `judge_local_llama8b_disg` / `_orig` (P(YES)) | 0.636 / 0.581 | −0.074 / −0.129 | 0.632 / 0.572 | 0.575 / 0.519 |
| `sc5_local_eq_frac` (SC-5, Qwen3-8B T=0.7, z3 modulo vocabulary) | 0.664 [0.617, 0.706] | −0.046 [−0.091, −0.001] | 0.681 | 0.630 |
| `sc5_local_entropy` | 0.631 | −0.079 | 0.649 | 0.596 |
| `pilot_rerun_jacc` (1 − predicate Jaccard, rerun / cross-system) | 0.660 [0.621, 0.695] | −0.050 [−0.088, −0.011] | 0.713 | 0.602 |
| `rt_nli_min_local` / `rt_nli_min_alt_local` (round-trip NLI) | 0.626 / 0.631 | −0.084 / −0.080 | 0.655 / 0.668 | 0.562 / 0.593 |
| `rt_embed_cos_local` (round-trip mpnet cosine) | 0.578 | −0.133 | 0.536 | 0.566 |
| `b2_score` (B2 world probe, local reader) | 0.574 [0.529, 0.619] | −0.136 [−0.184, −0.092] | 0.591 | **0.509** |
| `pilot_joint_conflict` / `arity` / `shape` / `dangling` (user's pilot) | 0.500 / 0.503 / 0.504 / 0.541 | ≈ −0.21 | ≈0.50–0.54 | ≈0.50–0.57 |
| `parse_fail` (COVERAGE view, unparseable = ERROR, n = 3,748) | 0.684 [0.665, 0.705] | (bar 0.817 in this view) | — | — |

Reading:
- **The only baseline that beats the bar is the cross-fitted stack.** S4_local gains +0.038 pooled, +0.076 on tier A and
  +0.059 on the long pool, and all these CIs exclude 0.
- **Without an LLM judge the stack only ties the judge** (0.703 vs 0.710).
- **The user's pilot structural metrics are null again** (0.50–0.54, with tie rates of 0.96–0.99). The exception is the
  rerun/cross-system predicate Jaccard (0.660), which is a consensus signal, not a structural one.
- **The pooled AUROC flatters every metric.** Per stratum, the bar is 0.663 (L25), 0.675 (L20), 0.663 (EXC) and 0.739
  (CTRL), all under R_AB and all testable.
- **Other pools.** MALLS GPT-4 gold used as a candidate (GOLDSYS, n = 240): bar 0.619, SC-5 0.542, round-trip NLI
  0.482. ccg2lambda (33 labelled rows) is untestable.
- **Sensitivity views keep the ordering** (bar / S4): CONTESTED→CORRECT 0.678/0.708, CONTESTED→ERROR 0.695/0.733,
  ALL_TIERS 0.725/0.753, L25 without the top-up 0.666/0.685.

**2. Long, heavily conditioned sentences (the user's focus).**
- Judge AUROC by word bin: 0.719 (<12 words) and 0.655–0.691 from 25 words up (the ≥35 cell is descriptive: 24 CORRECT).
- By number of conditions: 0.795 for ≤1 condition, 0.524 for 2, 0.673 for 3 and 0.667 for 4+.
- GEE (exchangeable, sentence clusters), log-odds slope of a correct flag at the frozen threshold, per SD of sentence
  length:

| Metric | Slope per SD of words |
|---|---|
| judge_local_qwen8b_disg | −0.56 [−0.86, −0.26] |
| rt_nli_min_local | −0.70 [−1.01, −0.39] |
| b2_score | −0.62 [−0.95, −0.28] |
| S4_local | −0.29 [−0.55, −0.04] |
| SC-5 | +0.27 [−0.09, +0.63] (n.s.) |

- The n_conditions slopes are all n.s.
- So judge, round-trip and B2 degrade with length. S4 degrades least, and SC-5 does not degrade.

**3. Larger vs cheap judge on the 284-row frame.**
- There is no frontier result: F-KEY, so gemini-3.1-pro-preview was never called and the $0.002 cost gate could not be
  checked.
- The local larger judge (Qwen3-14B-nf4) vs Qwen3-8B:
  - orig +0.025 [−0.016, +0.066];
  - disg −0.024 [−0.073, +0.022];
  - IPW-weighted: +0.018 / −0.020.
- Both are n.s., so scale within the local family buys nothing measurable.

**4. Contamination.** Here DiD = Δdisg(public MALLS gold as candidate) − Δdisg(E_POOL), and MDE = 2.8 × bootstrap SE.

Qwen3-8B judge:
- **Disguise helps it on LLM outputs** (Δdisg = orig − disg = −0.061 [−0.095, −0.031]).
- DiD +0.036 [−0.039, +0.111], MDE 0.107: **no evidence at this MDE.**
- The gold-recognition probe runs the opposite way to memorisation (DiD −0.071 [−0.125, −0.020]). On wrong public gold
  the original wording makes the judge *less* willing to accept it (0.81 vs 0.86).

Llama-3.1-8B P(YES):
- DiD +0.162 [+0.064, +0.261] (MDE 0.139). Its original-wording advantage is larger on public gold, which is *consistent
  with* memorisation.
- But its probe is n.s. (−0.074 [−0.170, +0.019]).
- Disguise flips its calibration: P(faithful) on ERROR rows falls from 0.71 to 0.30.
- So the DiD is confounded by that calibration shift. Report as "not established".

**5. Per error type, recall at matched FA = 0.10** (thresholds set on E CORRECT rows; descriptive). Rows are types, from
tier-A repair ops mapped to error codes and tier-B panel ops.

| Error type (n) | Qwen disg | S4_local | B2 |
|---|---|---|---|
| COMPOUND (1,029) | 0.34 | 0.50 | 0.12 |
| missing content, A:DROP (46) | 0.15 | 0.33 | 0.26 |
| extra content, A:ADD (22) | 0.09 | 0.09 | 0.09 |
| CONN (38) | 0.26 | 0.26 | 0.08 |
| BIND (22) | 0.27 | 0.27 | 0.09 |
| MEANING_RENAME (221) | 0.14 | 0.14 | 0.14 |
| two-op (309) | 0.18 | 0.17 | 0.09 |

The judge's own `error_type` field is useless:
- it matches the single tier-A op on 0.03 (orig) / 0.01 (disg) of 144 rows;
- it matches 0.11 of the rows where it names a code at all;
- majority-class chance is 0.32.

**6. System level** (Kendall τ-b over 13 system×variant rows; descriptive; CIs from a sentence bootstrap):

| Metric | τ-b |
|---|---|
| judge | 0.667 [0.487, 0.769] |
| S4 | 0.590 |
| SC-5 | 0.487 |
| round-trip NLI | 0.462 |
| B2 | −0.026 [−0.359, 0.205] |

**7. Invariance on exp D's 282 meaning-preserving rewrites** (same rw_ids; FA at the frozen threshold).
- **B2 is the most invariant metric measured so far.**
  - Contrapositive, De Morgan, reorder, reprint and prenex: FA 0.00 → 0.00, flip 0.
  - RENAME: flip 0.127, because predicate words change the world text.
- For comparison, exp D's API judge_cheap_disg on the same ids: contrapositive 0.10 → 0.51, De Morgan 0.10 → 0.56,
  RENAME 0.13 → 0.55.
- SC-5 (exp C nano samples, no new calls) never flips except on RENAME (0.53 → 0.93 FA, flip 0.41).
- B2's invariance is cheap to get: at its frozen threshold (0.75) it flags only 9% of E CORRECT rows.

**8. B2 world probe: a negative result with this reader.**
- Worlds build for 96% of formulas (5.7 per formula, 53% φ-TRUE). Every world is re-verified by an independent Python
  evaluator.
- **The pre-registered local reader fails the gate.**
  - Balanced accuracy 0.476 on 262 held-out track-H expert-corrected formulas (gate ≥ 0.85), and 0.356 on E's trusted
    references (0.32 on L25, 0.30 on L20).
  - It answers UNDETERMINED on 20% of worlds, and batched vs single-world verdicts agree only 58%.
  - B2 is therefore **NOT_ELIGIBLE_FOR_FUSION** (`results/b2_gate.json`).
- On E it reaches 0.574 pooled and 0.509 in the long pool, and it adds nothing to S4 (0.750 vs 0.748).
- The dropped-condition hypothesis (UNDETERMINED share flags missing-content errors) is not supported: AUROC 0.529.
- **Post-hoc diagnostic** (not pre-registered; screen gate items only; `results/b2_think_diagnostic.json`):
  - The same worlds were read by Qwen3-8B with thinking on. On the 124 of 251 items that finished within 2,048
    tokens, balanced accuracy rises from 0.60 (the non-thinking reader on the same items) to **0.79**.
  - That is still below the 0.85 gate, at about 9.5 s/item, and 51% of items ran out of the token budget.
  - So the world construction is readable by a reasoning reader, but an 8B non-thinking reader cannot use it.
  - Whether an API reader (the plan's gemini-2.5-flash-lite) would pass the gate is open for iteration 3.

**9. Coverage, cost, label quality.**
- Coverage: 1,062 of the 7,900 E_POOL rows (13.4%) are unparseable. They are kept in the COVERAGE view with the
  worst score, so every metric's usable share is 0.866. B2 has another 272 fallbacks (271 z3 failures, 5 reader failures;
  usable share 0.831).
- Cost: $0 API. GPU seconds per unit (RTX 4090, batched):

| Component | Seconds per unit |
|---|---|
| Qwen3-8B judge | 0.13 |
| Llama P(YES) | 0.04 |
| verbaliser | 0.07 |
| B2 reader | 0.18 (+ about 0.01 s CPU z3 per formula) |
| Qwen3-14B-nf4 | 0.36 |

- Label quality, recomputed from E metadata, reproduces the card:
  - MALLS gold judged wrong 0.822 [0.788, 0.853];
  - correct-but-not-equivalent share of CORRECT: 0.773 (L25), 0.721 (L20), 0.441 (EXC), 0.215 (CTRL).

**10. Checks.**
- T0 unit tests pass (`results/test_units.json`, `tests/test_b2.py`). T1 is from the pilot runs: 0 JSON failures, and
  B2 has ≥4 worlds on 91% of formulas.
- T2: the local Qwen3-8B judge reproduces exp D's cached local scores: Spearman 0.985, 95% exact matches over 300 units.
- T4: `tests/audit_E.py` re-derives 5 headline numbers on a separate code path, and all agree to 3 decimals: bar AUROC,
  S4 − bar, frame Δ, DiD and B2 AUROC. An independent sklearn S4 refit gives 0.7478 vs 0.7478.
- Shuffled-label placebos all come out at 0.50, and S4 on permuted labels gives 0.490.
- The R_AB / R_A label-vector hashes match the prereg.
- **The sibling PEER+TEXT pool is identical.** Its R_AB pooled table has n = 2,686 (1,822 / 864, 292 sentences). It did
  not export a label-vector hash, so the hash comparison is left to iteration 3.
- **Test-retest of the local judge** (stands in for the API test-retest 4f, which F-KEY made impossible). Two
  independent runs (this artifact vs the sibling, separate processes, caches and batches) give Spearman 0.989 (disg) /
  0.993 (orig) and 94% / 96% exact matches over 7,283 rows (`results/retest_vs_sibling.json`). The sibling's local-judge
  AUROC is 0.712 vs 0.710 here.

## Departures from the plan (all logged)
- **F-KEY: every LLM component is local; no API call succeeded.** Consequently:
  - there is no API bar, no frontier judge, no API test-retest (4f) and no API verbaliser;
  - SC-5 uses Qwen3-8B samples instead of gpt-4.1-nano;
  - S4 is `S4_local`: S1 + S2_local + the four local judge columns + SC_local;
  - local thresholds follow exp D's local screen thresholds where those exist (`rt_nli_min_local` = exp D
    `rt_nli_min_localverb`), otherwise exp D's API-verbaliser values (`results/feature_meta.json`).
- **Frame size 284, not 300.** The frozen rule (≤1 row per sentence per cell, ≤2 per sentence) exhausted the CTRL cells
  at 31 CORRECT and 28 ERROR.
- **Dangling connectives.** `labeller.parse_ok` accepts outputs that end in a dangling connective (the parser reads an
  atom named None). Three such rows are counted as unparseable, so the parseable count is 7,421: exactly dataset E's
  non-UNPARSEABLE count.
- **115 colliding item_ids** are handled via `row_key` (see the iteration-3 deliverables).
- **`disguise_item` is called with its default seed** (= text), as the sibling does. 15 of 6,548 unique pairs (0.23%)
  failed an assertion and fell back to E's audited disguise.
- **B2 reader prompt.** v2 was chosen on the 40-item dev slice (0.436 vs 0.418 balanced accuracy; `prereg_b2.json`),
  but the reader failed the gate. B2 is NOT_ELIGIBLE_FOR_FUSION and was scored as pre-registered.
- **Post-hoc B2 diagnostic (not pre-registered, screen data only).** A thinking-mode Qwen3-8B reader was run on the 249
  non-dev gate items and 300 sha1-ordered track-L items (`results/b2_think_diagnostic.json`). Nothing on E depends on it.
- **SC-5 invariance** on the shared rewrites is computed from exp C's existing gpt-4.1-nano samples (393/432 items
  matched by sentence); no new calls.
- **DeLong p-values ignore sentence clustering.** The cluster-bootstrap CI is the primary inference; DeLong is reported
  for completeness.

## What was run (all label-blind until `--stage analysis`)
| Column(s) | What it measures (oriented: higher = more likely unfaithful) | Model / tool |
|---|---|---|
| `parse_fail` | 1 if the candidate does not parse with the shared grammar + z3 (or ends in a dangling connective) | `src/labeller/fol.py` |
| `pilot_joint_conflict`, `pilot_arity_incons`, `pilot_shape_incons`, `pilot_dangling` | The user's pilot metrics on artificial "documents" (system×variant, stratum, sha1 bucket of ~20 sentences). See `results/pilot_mapping_E.md` | z3 |
| `pilot_rerun_jacc` | 1 − predicate-token Jaccard: zero-shot vs few-shot output of the same system (Llama-3.3-70B, Qwen3-235B), otherwise cross-system | — |
| `rt_nli_{min,fwd,bwd,contra}_local`, `rt_nli_min_alt_local`, `rt_embed_cos_local` | Round trip: the local Qwen3-8B verbaliser (exp D VERBALISE prompt) → NLI in both directions (DeBERTa-v3-large MNLI/FEVER/ANLI/LING/WANLI; alt = cross-encoder/nli-deberta-v3-large) and mpnet cosine vs the sentence | GPU |
| `judge_local_qwen8b_{orig,disg}` | 1 − P(faithful), exp D rubric B JSON judge, on the original and on the nonce-disguised item (exp D `disguise_item`) | Qwen3-8B |
| `judge_local_llama8b_{orig,disg}` | 1 − P(YES) from next-token logprobs | Llama-3.1-8B-Instruct |
| `judge_local_qwen14b_{orig,disg}` | Larger local judge on the 284-row frame (**not** a frontier model) | Qwen3-14B nf4 |
| `sc5_local_eq_frac`, `sc5_local_entropy` | SC-5: 1 − share of 5 samples (T=0.7, dataset E's few-shot generation prompt) equivalent modulo vocabulary to the candidate; entropy of the equivalence classes | Qwen3-8B + z3 |
| `b2_score`, `b2_mismatch_det`, `b2_undet_share` | B2 world probe (below) | z3 + Qwen3-8B reader |
| `S4_local_oof_RAB` (+ variants) | Cross-fitted L2 logistic stack of S1 + S2_local + local judges + SC_local on `folds_E.json` | sklearn |

### B2 world probe (`src/b2_world_probe.py`)
1. Parse φ.
2. Take typed single-edit mutants ψ of φ (NEG/REV/QUANT/RESTR/CONN/DROP/SWAP/SCOPE), each z3-verified
   non-equivalent.
3. For each mutant, solve for a small grounded world where φ and ψ disagree. The direction alternates between φ-TRUE
   and φ-FALSE, and z3 Optimize keeps the world minimal. Every world is re-checked by an independent Python evaluator.
4. Verbalise the world by a fixed template (no logic symbols).
5. Ask a text-only reader, which never sees a formula, whether the SENTENCE is TRUE / FALSE / UNDETERMINED in each
   world.
6. `b2_score` = (determined verdicts ≠ φ's truth value + ½ × UNDETERMINED) / #worlds.

## Deliverables for iteration 3 (no API calls needed to rescore)
- **`E_baseline_features.jsonl`**: one row per E row (8,507). It has every oriented column, a per-column status
  (`ok` / `fail` / `fallback` / `na`), `metadata_fold_E`, the pool and the parse flag.
- **`folds_E.json`**: `fold = int(sha1('E_folds_v1|'+sentence_id),16) % 5`, stored per sentence, per item and per row.
- **`src/s4.py::fit_s4_oof(table, labels, folds, feats)`**:
  - refits S4 under any label regime (e.g. R_ADJ) on identical folds, and returns OOF p, per-fold coefficients and
    nested FA=0.10 flags;
  - PEER+TEXT columns can be appended to the table and nested on the same folds.
- **Label-vector hashes** (`prereg_baselines.json.label_vectors`, recomputed in `results/analysis_E.json`):
  - R_AB `1bfcb30634ab6e9c3f00d40d398584b5892a805f` (n = 2,941 rows, all pools);
  - R_A `715bfc1e28599a58343f379820f6990254ab30ef` (n = 897).
  - Both are sha1 of the sorted `metadata_item_id:label` lines over rows.
- **Id collision.** 115 `metadata_item_id`s collide in dataset E: the zero-shot and few-shot outputs of the same system
  are identical strings. Rows are therefore keyed by `row_key` (`item_id~variant` for the colliding rows), and scores by
  `item_id` (identical inputs, identical scores).

## Layout
| Path | What |
|---|---|
| `method.py` | Orchestrator; one stage per step (`--stage NAME [--limit N] [--which a,b]`), all idempotent and cached; see its docstring |
| `src/e_pool.py` | Label-blind loader `load_E(blind=True)` (strips 18 label keys + 4 class-structure keys); pools; label regimes; `label_vector_sha1`; folds |
| `src/b2_world_probe.py` | B2: mutants, grounding, z3 worlds, template verbaliser, reader prompt (v1/v2), parsing, scoring, `world_probe(text, fol, key, reader)` |
| `src/s4.py` | Feature table + `fit_s4_oof` |
| `src/analysis_E.py` | Analyses (a)-(k): eval blocks, frame/IPW, contamination DiD + gold-recognition probe, recall per error type, complexity + GEE, label quality, system level |
| `src/consensus_min.py` | SC-5 scorer (`components`/`entropy` copied from exp C) |
| `src/judges.py`, `src/disguise.py`, `src/roundtrip.py`, `src/pilot_metrics.py`, `src/analysis.py`, `src/local_llm.py`, `src/common.py`, `src/labeller/` | Copied verbatim from exp D. Exceptions: `budget.py` caps plus dead-key detection, and `local_llm.sample_many` added |
| `prereg_baselines.json` / `.sha256` | Frozen pre-registration (models, prompts + sha1s, feature sets, folds, thresholds, B2 spec, frame rule, label-vector hashes) |
| `prereg_b2.json` / `.sha256` | B2 reader prompt choice (v1 vs v2 on the 40-item track-H dev slice), frozen before the gate |
| `data/E_units.json` | Label-free unit table: text, candidate, parse flag, disguised pair, strata, system, fold |
| `data/frontier_frame.json` | The 284-row stratified frame with inclusion probabilities |
| `data/b2_worlds.jsonl` | Every B2 world (7,702 formulas), including mutant, direction, φ-truth and world text |
| `data/expA_*`, `data/expD_*`, `data/invariance_items.json` | Copied screen items, exp D prereg/analysis/thresholds, and the 282 shared rewrites |
| `results/scores/*.jsonl` | Raw per-unit scores (append-only; the last line per key wins) |
| `results/analysis_E.json` | Every number (sets × metrics, paired Δ, frame, contamination, per-type, complexity, GEE, coverage, label quality, system level, invariance, B2) |
| `results/summary.md` | Plain-language tables |
| `results/tables/*.csv` | CSV versions of the main tables |
| `results/b2_gate.json`, `results/b2_threshold.json`, `results/b2_build_meta.json`, `results/b2_think_diagnostic.json` | B2 gate, thresholds, construction stats, post-hoc reader diagnostic |
| `results/local_cache.jsonl`, `results/llm_cache.jsonl` | Every local generation (and API call, none succeeded) for exact re-runs |
| `results/test_units.json`, `results/audit_E.json`, `results/t2_repro_local_judge.json` | T0 unit tests, independent re-derivation + placebos, T2 local-judge reproducibility vs exp D |
| `E_baseline_features.jsonl`, `folds_E.json` | Iteration-3 hand-off (above) |
| `method_out.json` (+ `full_`/`mini_`/`preview_`) | exp_gen_sol_out: `E_heldout` (all 8,507 rows, `predict_<metric>`), `screen_B2` (B2 on the 1,055 screen items) |
| `tests/test_units.py`, `tests/test_b2.py`, `tests/audit_E.py` | T0 unit tests, B2 construction tests, independent audit |
| `gpu_pipeline.sh`, `gpu_pipeline2.sh`, `key_poll.sh`, `finalize.sh` | The GPU stage chains, the F-KEY key poller, and the final label-joined pass (gate report → s4 → analysis → audit → schema check → previews) |
| `results/retest_vs_sibling.json` | Local-judge test-retest against the sibling PEER+TEXT run |

## How to run
```bash
bash restore.sh                                   # venv (+cu128 torch) and NLTK data; model weights -> shared HF cache
export PYTHONHASHSEED=0
.venv/bin/python method.py --stage prep           # label-blind units, parse check, disguise
.venv/bin/python method.py --stage prereg && .venv/bin/python method.py --stage frame   # freeze (refuses to overwrite)
.venv/bin/python tests/test_units.py && .venv/bin/python tests/test_b2.py
.venv/bin/python method.py --stage cpu            # parse + pilot metrics
.venv/bin/python method.py --stage b2_build       # B2 worlds (CPU)
./gpu_pipeline.sh                                  # local judges, verbaliser, SC samples, B2 reader, NLI, larger judge
.venv/bin/python method.py --stage sc_score && .venv/bin/python method.py --stage sc_invariance
.venv/bin/python method.py --stage b2_gate_report
.venv/bin/python method.py --stage retest_sibling    # optional: needs the sibling experiment's results
./finalize.sh                                      # b2_gate_report, s4, analysis, audit, schema check, previews
# API path (when an OpenRouter key has budget): judges, sc_gen + sc_score --which sc5_samples, verbalise + nli --which api,
# strong, retest; then s4 + analysis again (the bar switches to judge_cheap_disg automatically).
```

## Restoring removed files
| Deleted path (`.aii/manifest.yaml`) | Restore |
|---|---|
| `.venv/` | `bash restore.sh venv` (`uv venv` + `requirements.txt` + the cu128 torch wheel: this box's driver is CUDA 12.8) |
| `data/nltk_data/` | `bash restore.sh nltk` (WordNet, omw-1.4, words: the disguise needs them) |
| `src/**/__pycache__/` | regenerated automatically |
| model weights (never in this workspace; they are in the run's shared HF cache) | `bash restore.sh models` (Qwen3-8B, Qwen3-14B, Llama-3.1-8B-Instruct, the two DeBERTa NLI checkpoints, all-mpnet-base-v2) |
