# T1: peer-agreement consensus vs paid LLM judges on held-out NL→FOL set E

Iteration 3, experiment 1 of run `run_u75jRHUss0zo` (plan `gen_plan_experiment_1_idx1`).

**Setting.** We have a sentence and a candidate first-order-logic (FOL) formula, and no gold formula. The question is
whether the candidate is faithful to the sentence.

**Question.** Does the frozen consensus metric (`c_score_align`, the PEER metric of iteration 2, exp 5) beat the cheap
API LLM judge a practitioner would actually deploy? Does it still add signal once every baseline is stacked together?
Earlier iterations could not answer this: the shared OpenRouter key was dead, so iteration 2 had only local judges.

**What this artifact adds.** The consensus scores and all local baselines are frozen inputs; nothing on the metric side
is re-scored. This artifact adds only the missing API comparators, all on held-out dataset E:
- **gemini-2.5-flash-lite**, rubric-A JSON judge, disguised and original views, on every parseable row;
- **gpt-4.1-nano**, P(YES) judge, both views;
- **gemini-3.1-pro-preview**, frontier judge, on the frozen 284-row frame;
- an API **round trip**: flash-lite verbaliser, then DeBERTa NLI and mpnet cosine;
- API **SC-5**: nano, T = 0.7, 5 samples, z3 equivalence modulo vocabulary.

It then refits the cross-fitted stack of every baseline (`S4_full`, 28 features). All criteria were tested against
`prereg_T1.json`, which was sha256-frozen (`c2a6cf84…`, 01:54 UTC) after the label-blind pilots and **before any
full-sweep score existed**. `src/analyse_T1.py` refuses to run if the hash changed, or if any score file predates the
freeze.

## Verdict (`results/verdict_T1.json`)

Main population: E_POOL, PRIMARY (parseable) rows under label regime **R_AB**. That is n = 2,686 rows (1,822 ERROR /
864 CORRECT) over 292 sentences.

Conventions:
- Every Δ is paired, on identical rows.
- **strat** = within-stratum AUROC: only ERROR/CORRECT pairs from the same source stratum count.
- CIs are sentence-cluster percentile bootstraps (B = 2000, seed 0).

| criterion (pre-registered) | status | numbers |
|---|---|---|
| **(a)** `c_score_align` beats flash-lite (disguised). Intersection–union test over: R_AB strat CI > 0, long-pool strat CI > 0, and R_A L20+EXC Δ > 0 | **CONFIRMED** | R_AB strat Δ **+0.099 [+0.049, +0.146]**; long pool (L25+L20+EXC) **+0.116 [+0.070, +0.163]**; R_A L20+EXC +0.299 [+0.212, +0.390] |
| **(b)** adds signal beyond `S4_full`, the cross-fitted stack of every baseline including all 4 API judges, API round trip and API SC-5 | **CONFIRMED** | nested strat Δ **+0.039 [+0.021, +0.057]**; permutation-null p95 0.009 (observed at percentile 1.00 of 100 reps); pooled +0.030 [+0.015, +0.045] |
| **(d)** within 0.95× of the frontier judge at ≤ 10% of its cost, OR a nested gain over it | **CONFIRMED** (both branches) | ratio 0.957 [0.887, 1.034] (IPW 0.975); consensus $1.2e-4 vs frontier $3.65e-3 per item; nested [strong + c] − [strong] +0.037 [+0.008, +0.066] (n = 284) |
| **VEX**: aligner-confound control on vocab-exact rows, where labels need no symbol alignment | **CONFIRMED** | Δ +0.306 [+0.232, +0.376] (strong form, CI > 0); VEX_STRICT +0.202 [+0.144, +0.269]; tier-A-only +0.224 [+0.161, +0.297] |
| **M3**: consensus degrades less with sentence length than the judge (GEE slope difference, matched FA = 0.10) | **DISCONFIRMED** | words +0.146 [−0.051, +0.361]; n_conditions +0.116 [−0.044, +0.264] |

**Overall (this artifact): CONFIRMED.** Criteria (c) and (e) belong to sibling artifacts. Robustness checks:
- With the best cheap API judge post hoc as the bar (`judge_cheap2_orig`, nano P(YES) original view), (a) still holds:
  +0.089 [+0.043, +0.134].
- Under the JSON-failure sensitivity fill (`judge_cheap_disg_vfb`), (a) still holds: +0.100 [+0.051, +0.144].

### Headline AUROCs, R_AB (`results/tables_T1.md`, section (a))

| metric | pooled AUROC | strat AUROC | $/item |
|---|---|---|---|
| `p_peer_text` (frozen PEER+TEXT fusion) | 0.790 [0.752, 0.825] | 0.753 | 1.2e-4 (full) |
| `c_score_align` (frozen consensus) | 0.782 [0.745, 0.816] | 0.741 | 1.2e-4 (full) / 2.5e-7 (marginal) |
| `S4_full_oof` (stack of all baselines) | 0.777 [0.739, 0.809] | 0.735 | sum of its parts |
| `S4_full + c_score_align` | 0.807 [0.772, 0.838] | 0.774 | |
| flash-lite, disguised (**primary bar**) | 0.696 [0.655, 0.733] | 0.642 | 4.9e-5 |
| flash-lite, original | 0.635 | 0.623 | 4.9e-5 |
| gpt-4.1-nano P(YES), original / disguised | 0.700 / 0.681 | 0.653 / 0.644 | 2.0e-5 |
| API round trip `rt_nli_min` / `rt_nli_fwd` | 0.639 / 0.674 | 0.606 / 0.611 | 2.7e-5 |
| API SC-5 `sc5_eq_frac` | 0.656 | 0.598 | 3.0e-5 |
| local Qwen3-8B judge, disguised (iteration-2 bar) | 0.710 | 0.674 | – |

On the 284-row frame, gemini-3.1-pro-preview (original view) scores 0.741; `c_score_align` scores 0.710 there.

### Findings that qualify the confirmation

These are also in `results/tables_T1.md`.
- **Consensus ≈ the whole baseline stack.** `c_score_align − S4_full_oof` = +0.006 [−0.031, +0.042]. Consensus alone
  matches a 28-feature stack. The two are complementary: the nested gain is +0.039.
- **FOLIO control stratum (CTRL, short sentences).** Consensus does *not* beat flash-lite here: −0.069 [−0.232, +0.098],
  n = 386. Flash-lite is also better on sentences under 12 words (−0.040) and on ≤ 1 condition (−0.028). The advantage
  sits in the long and heavily conditioned sentences:
  - EXC: +0.197 [+0.124, +0.269];
  - 3 conditions: +0.197;
  - 4+ conditions: +0.095 [+0.036, +0.152];
  - depth > 4: +0.155 [+0.060, +0.244].
- **Aligner-masked and peer-endorsed errors are consensus's blind spot.** These are tier-B MEANING_RENAME errors
  (n = 221). At FA = 0.10:
  - `c_score_align` recall is 0.07; the judges reach 0.13–0.20;
  - on PEER_ENDORSED errors (the peer medoid agrees with the wrong candidate), `c_score_align` recall is 0.00 by
    construction.
- **Contamination.** Flash-lite's original view gains on public MALLS gold relative to held-out candidates:
  DiD +0.105 [+0.006, +0.201]. This is consistent with memorisation, but the point estimate is below the MDE of 0.14.
  For nano, DiD is −0.009. On E itself, the nonce-disguised view is the *better* flash-lite view (+0.061).
- **Reliability.** Flash-lite test–retest on 187 rows: Spearman 0.975, exact-match share 0.984.
- **System level (descriptive).** Kendall τ-b against the error rate over 13 system × variant rows:
  - `c_score_align` 0.69;
  - `p_peer_text` 0.72;
  - flash-lite, disguised 0.56;
  - nano, disguised 0.72.

### Integrity checks

- **Reproduction gates** (`results/repro_gates.json`, all pass):
  - key bijection over 8,507 rows;
  - R_AB / R_A label-vector sha1 matches the prereg;
  - S4_local OOF 0.748; pooled PT 0.790, c 0.782; stratified PT 0.753, c 0.741;
  - within-stratum placebo 0.590; PT − S4_local +0.042 [0.014, 0.070], identical to the iteration-2 reviewer audit.
- **Independent re-derivation** (`tests/audit_T1.py` → `results/audit_T1.json`). A separate code path (numpy pairwise
  AUROC, its own bootstrap loop) reproduces all 5 headline numbers to 1e-3: confirmatory Δ, long-pool Δ, nested Δ, frame
  ratio and M3.
- **Placebos.** Shuffled-label AUROC 0.501; shuffled strat Δ 0.001, with 95% band [−0.029, +0.035].

## API spend (`results/api_cost_ledger.json`, per-call `usage.cost`)

| component | model | calls | $ |
|---|---|---|---|
| judge_cheap | google/gemini-2.5-flash-lite | 13,496 | 0.658 |
| judge_cheap2 | openai/gpt-4.1-nano | 12,996 | 0.261 |
| strong | google/gemini-3.1-pro-preview | 289 | 1.056 |
| roundtrip (verbaliser) | google/gemini-2.5-flash-lite | 6,448 | 0.177 |
| sc5 | openai/gpt-4.1-nano | 3,500 | 0.233 |
| retest | google/gemini-2.5-flash-lite | 200 | 0.010 |
| **total** | | | **2.395** (hard cap 4.60) |

The frontier **disguised** view was not run. The pre-registered shared-key reserve rule stopped it: sibling artifacts
had drained the run key to $0.33. See `results/deviations.json` D4.

## Deviations

All ten are in `results/deviations.json`. The ones that matter for reading the numbers:
- **D5.** Quantised scores put more than 10% of CORRECT rows at the maximum, so the matched-FA operating points use a
  label-free, seeded tie-breaker (a randomised test). No AUROC uses it.
- **D4.** The frontier disguised view is missing (see above).
- **D3.** Flash-lite JSON outputs without `faithful_prob` get the pre-registered 0.5. This affects 4% of R_AB rows.
- **D7.** Cost reconciliation against the key's usage counter is impossible because the key is shared. Spend therefore
  comes from each response's `usage.cost`.

## Layout

| path | what |
|---|---|
| `method.py` | Orchestrator, `--stage NAME`. T1 stages: `t1_prep` (gates, key map, VEX declaration), `t1_pilot`, `t1_freeze`, `judges`, `strong`, `verbalise`, `nli --which api`, `sc_gen`, `sc_score --which sc5_samples`, `retest`, `t1_analysis`. The iteration-2 stages (local judges, B2, …) are kept from exp 6. |
| `prereg_T1.json`, `prereg_T1.sha256` | Frozen T1 pre-registration: models and prices, prompt sha1s, caps, decision rules, criteria verbatim, S4 sets, VEX declaration hash. |
| `prereg_baselines.json` | Exp 6's frozen prereg: prompts, label-vector hashes, frame hash. Used as-is. |
| `src/api_bar.py` | Documented reusable functions: API judges, P(YES) judge, frontier judge, SC-5, round trip, `strat_auroc`, `paired_boot`, `ClusterBoot`, `delong`, `ipw_auroc`, `matched_fa_threshold`, `gee_slope(_diff)`, `consensus_cost_per_item`, `vex_subset`. |
| `src/analyse_T1.py` | Every T1 analysis, (a)–(j). The only place where new scores meet labels. |
| `src/join_T1.py` | Canonical key map (item_id, prompt_variant) across dataset E, exp 5 and exp 6; API column loader. |
| `src/vocab_exact.py` | VEX subset: normalised symbol signatures, and label re-verification by plain z3 equivalence. |
| `src/report_T1.py` | Tables, cost ledger, `per_item_T1.jsonl`, `method_out`, figures. |
| `src/budget.py` | Budget-guarded async OpenRouter client. Base URL comes from `OPENROUTER_BASE_URL`; caps come from the prereg; `costs.jsonl` is written on every call. |
| `src/{judges,roundtrip,consensus_min,disguise,e_pool,s4,labeller/}` | Exp 6 code, reused. |
| `tests/audit_T1.py` | Independent re-derivation of the 5 headline numbers. |
| `tests/audit_raw_T1.py` → `results/audit_raw_T1.json` | Re-derivation from RAW files (dataset E labels, exp 5 scores, raw API score files) with its own rank-sum AUROC and bootstrap, plus placebo tests (permuted labels, random challenger) that must fail and do. |
| `reproducibility.md`, `pyproject.toml` | Step-by-step reproduction of what was actually run; all 132 packages pinned. |
| `t1_api_chain.sh` | The sweep chain, in pre-registered order. |
| `results/analysis_T1.json` | Every number, with n, CIs and sources. |
| `results/verdict_T1.json`, `results/tables_T1.md` | Verdict and plain-language tables. Each table has a `# source:` line. |
| `results/per_item_T1.jsonl` | One row per E row (8,507): keys, strata, labels, flags, every metric column with its status. |
| `results/scores/*.jsonl` | Raw API score files: `judge_cheap`, `judge_cheap2`, `judge_strong`, `judge_cheap_retest`, `rt_verbal_api`, `rt_nli_api`, `sc5_samples`, `sc5`. |
| `results/llm_cache.jsonl` | Every API response. Re-running any API stage is free with it. |
| `results/costs.jsonl`, `results/api_cost_ledger.json`, `results/budget_state.json` | Per-call spend and totals. |
| `results/repro_gates.json`, `results/vex_declaration.json`, `results/pilot/` | Pre-freeze gates, the VEX declaration, and the label-blind pilots. |
| `results/s4_full_coefs.json` | Per-fold standardised coefficients of every stack. |
| `results/deviations.json`, `results/audit_T1.json` | Deviations and the audit. |
| `figures/forest_T1.{png,pdf}` | Δ(consensus − flash-lite disguised) over every cell. |
| `figures/complexity_curves.{png,pdf}` | AUROC by words and by n_conditions bin. |
| `method_out.json`, `full_method_out.json`, `mini_…`, `preview_…` | `exp_gen_sol_out` output: dataset `E_heldout_T1`, one example per E row, with `predict_*` = oriented scores of every metric. |
| `data/` | Frozen inputs, copied read-only. `E_units.json` (label-free units), `exp5/` (frozen consensus scores `per_item_E.jsonl`, prereg, analysis), `exp6_*` (local baselines, results, scores), `folds_E.json`, `frontier_frame.json`, `vex_rows.json`, `t1_priority.json`. |

Kept artifacts live at
`/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/`, for example
`…/results/llm_cache.jsonl` and `…/results/per_item_T1.jsonl`. Dataset E itself is at
`/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json`.

## How to run

```bash
bash restore.sh venv && bash restore.sh nltk      # environment (uv, torch 2.11.0+cu128) + WordNet
export PYTHONHASHSEED=0
.venv/bin/python method.py --stage t1_prep         # gates, key map, VEX declaration (no scores)
.venv/bin/python method.py --stage t1_pilot        # label-blind 20-row pilots
.venv/bin/python method.py --stage t1_freeze       # writes prereg_T1.json + sha256 (already frozen: do not re-run)
bash t1_api_chain.sh                               # API sweeps (cached; free to re-run with results/llm_cache.jsonl)
.venv/bin/python method.py --stage nli --which api # GPU NLI on the API verbalisations
.venv/bin/python method.py --stage sc_score --which sc5_samples
.venv/bin/python method.py --stage t1_analysis     # ~9 min on 6 CPUs; writes results/*_T1.*, figures, method_out.json
.venv/bin/python tests/audit_T1.py
```

`t1_analysis` writes `method_out.json`; `aii_json_format_mini_preview.py --input method_out.json` (aii-json skill) makes the full / mini / preview variants.

## Restoring removed files

These `delete` entries in `.aii/manifest.yaml` are removed after the round. Everything else, including `results/` with the paid API scores and `results/llm_cache.jsonl`, stays.
- `.venv/` → `bash restore.sh venv`: `uv venv .venv --python=3.12`, then `uv pip install -r requirements.txt` and
  torch 2.11.0 from the cu128 index.
- `src/__pycache__/`, `src/labeller/__pycache__/` → regenerated by any Python run.
- The NLI and embedding weights are not in this workspace. They are in the run's shared HF cache. To refetch them:
  `.venv/bin/python scripts_download.py MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli cross-encoder/nli-deberta-v3-large sentence-transformers/all-mpnet-base-v2`.
