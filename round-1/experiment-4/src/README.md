# Experiment D: disguised cheap judge and all baselines on the shared NL→FOL screen

This is the **baseline and null arm** of the iteration-1 wide screen (run `run_u75jRHUss0zo`). It takes a sentence and a
candidate first-order-logic formula, with no gold available, and scores how likely the formula is unfaithful using every
baseline the user asked for:
- the parse/compile rate;
- the user's own pilot structural metrics, adapted to FOL;
- round-trip scores (FOL→NL→compare), via NLI, embedding similarity, and re-formalisation checked with z3;
- LLM-as-judge: two cheap judges plus a larger judge, each scored on the ORIGINAL and on a nonce-DISGUISED version of
  the item (a contamination control).

Everything is measured on the same frozen, labelled screen that experiments A, B and C use (joined by `item_id`, with
label-vector sha1 in `data/label_vector.sha1`). It produces the **bar** that iteration-2 candidates must beat:
`judge_cheap_disg` and the cross-fitted `best_baseline_oof`.

> **Results:** `results/summary.md` has the plain-language tables. `results/analysis.json` has every number.
> `method_out.json` / `full_method_out.json` have the per-item scores (exp_gen_sol_out schema, validated).

## Key results (final: planned API judges)
All CIs are sentence-clustered bootstrap intervals (2,000 resamples). Track L means Logic-LM outputs labelled CORRECT
vs ERROR, n = 524 (230 errors). Judges:
- `judge_cheap`: gemini-2.5-flash-lite, rubric A.
- `judge_cheap2`: gpt-4.1-nano, P(YES).
- `judge_strong`: gemini-3.1-pro-preview on the pre-registered 200L + 96H subset.

Open-weight local judges (Qwen3-8B, Llama-3.1-8B, Qwen3-14B-nf4) are reported next to them as `judge_local_*`.

**The screen.**
- 1,090 items: track L 796 (3 Logic-LM systems; 108/202 curated conclusions and 128 agreed premises matched) and
  track H 294.
- Track-L labels: 294 CORRECT, 230 ERROR, 216 UNCERTAIN, 56 UNPARSEABLE.
- 128 of the 230 track-L ERRORs (56%) are "substitution-only" (ADD+DROP of an unaligned predicate), i.e. likely
  correct-but-not-equivalent.
- On track H, 27% of the parseable original public gold is wrong, 5.8% of it is unparseable, and 22% of the
  non-equivalent originals are VOCAB/GRAN.

**Track-L AUROC [95% CI]:**

| Group | Metric | AUROC [95% CI] |
|---|---|---|
| Cheap API judges | **judge_cheap_disg (the pre-registered bar)** | **0.777 [0.720, 0.827]** |
| | judge_cheap_orig | 0.749 [0.695, 0.801] |
| | judge_cheap2 (orig / disg) | 0.750 / 0.714 |
| Frontier judge (200-item subset) | judge_strong_orig | **0.802 [0.715, 0.877]** |
| | judge_strong_disg | 0.730 [0.655, 0.803] |
| Local judges | Qwen3-8B (orig / disg) | 0.755 / 0.757 |
| | Llama-3.1-8B (orig / disg) | 0.699 / 0.671 |
| | Qwen3-14B-nf4 (orig / disg) | 0.753 / 0.760 |
| Round-trip (API verbaliser) | NLI min | 0.710 [0.648, 0.769] |
| | alt NLI checkpoint | 0.689 |
| | mpnet cosine | 0.633 |
| | re-formalise + z3 | 0.513 (near chance: the literal verbalisation is almost always re-formalisable) |
| Round-trip (local verbaliser) | NLI min | 0.740 |
| User's pilot metrics | joint-load conflict, arity, shape, dangling, undeclared | 0.50–0.53: **a negative result** |
| | cross-system rerun Jaccard | 0.720 [0.659, 0.780] |
| Parse rate | parse_fail | 0.598 on the view that counts UNPARSEABLE as error |

**The frontier judge beats the cheap judge on the same items.** On the 200-item subset, the original-text frontier judge
scores 0.802 vs 0.725 for the cheap judge: Δ = +0.077 [0.006, 0.154], DeLong p = 0.015. Disguised, the gap
disappears.

**Cross-fitted combination of all cheap baselines (S4).** OOF AUROC is 0.817 [0.762, 0.867], which is only +0.039
[−0.010, 0.087] over the bar: not significant. The bar for iteration 2 is therefore `judge_cheap_disg` **0.777** and
`best_baseline_oof` **0.817**, with folds in `data/folds.json`.

**Contamination.** No evidence.
- Every DiD CI includes 0: cheap judge −0.042 / −0.053, nano −0.077 / −0.065, frontier +0.002.
- The frontier judge loses about 0.07 AUROC under disguise on BOTH tracks, i.e. disguise removes lexical meaning; it
  does not expose memorised gold.
- In the recall probe, flash-lite reproduces the erroneous ORIGINAL public gold on 4.4% of the 113 items where original
  and corrected differ, vs 15.9% for the CORRECTED gold.
- Its predicate-name overlap with the original gold does not exceed its overlap with an independent LLM translation:
  Δ = −0.068 [−0.171, 0.034].

**Invariance.** False-alarm rates on meaning-preserving rewrites of CORRECT items, FA base → FA rewrite:

| Metric | Contrapositive | De Morgan | Rename |
|---|---|---|---|
| judge_cheap_orig | 0.03→0.67 | 0.05→0.18 | 0.04→0.27 |
| judge_cheap_disg | 0.10→0.51 | 0.10→0.56 | 0.13→0.55 |
| gpt-4.1-nano | 0.03→0.97 | — | 0.19→0.65 |
| rt_reformalise_eq | 0.08→0.03 | — | 0.11→0.23 |

- REORDER is almost free for every metric.
- rt_reformalise_eq is the most invariant metric (overall 0.10→0.15), but it does not discriminate.
- The pilot structural metrics are rename-fragile by construction.

**Complexity.**
- Track L is dominated by short sentences (485/524 have fewer than 12 words), so no long, heavily conditioned stratum
  is testable on this screen.
- The disguised judge's correctness falls with sentence length on track L: logit slope per SD of words = −0.48,
  p = 1.6e-5.
- Track-H cells are descriptive only (n ≤ 41).

**Error types.** The judge's error-type labels are rarely right: track H 0/12 on single-op errors, track L 18/89.

**Label noise.** 158 track-L ERRORs are judged faithful by judge_cheap (84 of them substitution-only). They are exported
in `results/judge_label_disagreements.csv` for adjudication by dataset E.

**Cost per call (measured):**

| Judge / step | $ per call |
|---|---|
| flash-lite judge | $0.00004 |
| gpt-4.1-nano | $0.000014 |
| frontier judge | $0.0029 |
| verbalise / re-formalise | about $0.00003 |

Total API spend: **$2.02** (cap $9.5).

**Independent audit** (`tests/audit_headlines.py` → `results/audit_headlines.json`). This is a separate code path: raw
score files, explicit pairwise Mann-Whitney AUROC, a python-`random` cluster bootstrap, and an S4 re-fit with its own
sklearn Pipeline.

| Quantity | Original | Audit |
|---|---|---|
| judge_cheap_disg AUROC | 0.777 | 0.777 (0.785 if the 11 JSON failures are dropped rather than flagged) |
| rt_nli_min AUROC | 0.710 | 0.710 |
| pilot_rerun_jacc AUROC | 0.720 | 0.720 |
| S4 combination − judge | +0.039 | +0.038 [−0.010, 0.086] |
| frontier − cheap | +0.077 | +0.077 [0.008, 0.153] |
| DiD | −0.053 | −0.053 [−0.145, 0.039] |

Placebos (shuffled labels):
- Every AUROC is in 0.46–0.54.
- S4 OOF AUROC is 0.481.
- The frontier − cheap Δ CI includes 0.
- The placebo DiD CI includes 0, and the placebo DiD is the same size as the real one.

## Deviation 1: local open-weight judges during the key outage, then planned API judges
The run's shared OpenRouter key hit its $50/day limit at 13:29 UTC, before any sweep. Every LLM step was first run on
the local GPU (RTX 4000 Ada) with open-weight models, the same prompts and T=0:
- Qwen3-8B JSON judge;
- Llama-3.1-8B P(YES);
- Qwen3-14B-nf4;
- Qwen3-8B verbaliser and recall probe.

These are pre-registered in `prereg_local.json` (frozen 13:49 UTC) and stored under `results/scores/*_local*.jsonl`,
`results/promptdev_local.json` and `results/roundtrip_meta_local.json`.

When a fresh key arrived (15:11 UTC), the **planned API judges were run** under `prereg.json` (frozen 15:13 UTC):
- The rubric variant (A) comes from the pre-outage API dev-slice run (`results/promptdev_api_preoutage.json`).
- The frontier judge was chosen by a cost/validity-only 10-item dry run: gemini-3.1-pro-preview at $0.0033/call beat
  gpt-5 (low) at $0.0036 and gemini-2.5-pro at $0.0083, all 10/10 valid. gemini-3-pro-preview is no longer listed.
- The strong subsample is identical to the local prereg.

The local judges' track-L results had been seen before this prereg, but no API setting was tuned on track L
(`freeze_context` in `prereg.json`).

Two budget notes:
- A budget-guard bug made queued coroutines pre-reserve budget, so the first frontier sweep refused 263 calls. It was
  fixed (`src/budget.py`: reservation inside the semaphore), and the sweep was completed from the cache.
- Parallel stages raced on `budget_state.json`; it was reconciled from the append-only `costs.jsonl`.

## Other departures from the plan text (all logged)
- **Labeller determinism.** The iter-3 repair search used a 25 s wall-clock budget, which makes labels depend on machine
  load. `src/labeller/labeller.py:search_det` uses a deterministic candidate budget (60k level-2 candidates) and
  `PYTHONHASHSEED=0`, because the fingerprint uses `hash()`. Regression against iter-3 `repair_census.rows.json`: 96/99
  unchanged, and exactly the 3 ⊕/→-bracketing COMPOUNDs become EQUIV (`results/labeller_regression.json`). T1 unit tests
  pass.
- **Disguise.** The formula is disguised by token-level substitution of identifiers, so bracketing and whitespace are
  byte-identical between the orig and disg conditions. It is verified on the AST: the inverse map gives an identical AST
  and the arity multiset is unchanged. Lemmas are keyed by their Porter stem, so "engaged"/"Engaged" share one nonce.
  0/1,090 items fail an assertion, and the formula leak rate is 0 (`results/disguise_audit.txt`,
  `results/disguise_stats.json`).
- **Verbalisation cleaning.** The local verbaliser sometimes answers `The formula ¬(…) says: "…"`. A deterministic
  cleaner (`judges.clean_verbalisation`) keeps only the English sentence, so the formula cannot leak into NLI or
  re-formalisation.
- **Track H labels.** The plan's literal mapping sends COMPOUND to UNCERTAIN; this is `label`, the shared label vector.
  A second view, `label_h_curator`, counts COMPOUND as ERROR, because curators certified the original was wrong. It is
  used for per-type sensitivity and reported as `H_curator_view`.
- **Extra sensitivity set** `L_exclude_subst_only`. ERROR items whose only repair is ADD+DROP of an unaligned predicate
  (e.g. `EatSalads(taylor)` vs `RegularlyEat(taylor, salad)`) are mostly vocabulary mismatches the aligner missed.
- **Extra metrics:**
  - `pilot_shape_incons`, from the pilot's metric2 argument-shape check;
  - `rt_nli_contra`;
  - `rt_nli_min_alt`, the alt NLI checkpoint;
  - `REPRINT`, a formatting-only rewrite control.
- `HF_HOME` stays on the run's shared cache (harness rule), not `./hf_cache`.

## Layout
| Path | What |
|---|---|
| `method.py` | Orchestrator; every step is a stage (`--stage NAME [--limit N]`), see its docstring |
| `src/labeller/fol.py` | iter-3 FOL parser/z3 with the ⊕ precedence fix (`PREC['xor']=3`) |
| `src/labeller/repair_census.py` | iter-3 aligner, granularity bridge and typed-repair operators (unchanged except the import) |
| `src/labeller/labeller.py` | `equivalent_modulo_vocab(cand, ref)`: the shared labeller; strata helpers |
| `src/screen.py` | Shared frozen screen: Logic-LM parsing, sentence matching, agreed premises, labelling, strata, `item_id` |
| `src/disguise.py` | Nonce disguise of text and formula, with assertions (i)-(v) |
| `src/rewrites.py` | Meaning-preserving rewrites (RENAME/REORDER/DEMORGAN/PRENEX/CONTRAPOSITIVE/REPRINT), z3-verified |
| `src/judges.py` | Prompts (rubric A/B, JSON, YES/NO, verbalise, re-formalise, recall), parsing, and the API judge path |
| `src/local_llm.py` | Local GPU backend: batched greedy generation, P(YES) scoring, cache |
| `src/budget.py` | Budget-guarded async OpenRouter client (per-component caps, cost ledger) |
| `src/roundtrip.py` | NLI (both directions, two checkpoints) and mpnet cosine |
| `src/pilot_metrics.py` | The user's pilot metrics adapted to FOL (see `results/pilot_mapping.md`) |
| `src/analysis.py`, `src/report.py` | Meta-evaluation: AUROC/AUPRC, cluster bootstrap, DeLong, contamination, combination, per-type, invariance, complexity, coverage, cost |
| `tests/test_labeller.py` | T1 unit tests |
| `tests/audit_headlines.py` | Independent re-derivation of the headline numbers, with shuffled-label placebos |
| `prereg.json`, `prereg.sha1` | API-judge pre-registration (frozen before any API score was joined to a label; see `freeze_context`) |
| `prereg_local.json`, `prereg_local.sha1` | Local-judge pre-registration (frozen 13:49 UTC, before any local score was joined) |
| `data/screen_items.json` | **The meta-evaluation dataset**: 1,090 items (track L 796, track H 294) with labels, repair ops, strata and story context |
| `data/label_vector.sha1` | sha1 of the sorted `item_id:label` lines (identity check against A/B/C) |
| `data/invariance_items.json` | 282 z3-verified meaning-preserving rewrites of 150 track-L CORRECT items |
| `data/disguise_map.json` | Per item (and rewrite): disguised text/formula, lemma→nonce map, audit flags |
| `data/folds.json` | GroupKFold fold per track-L CORRECT/ERROR item (reuse for nested ΔAUROC in iteration 2) |
| `data/logiclm/` | Logic-LM released `FOLIO_dev_{gpt-3.5-turbo,gpt-4,text-davinci-003}.json` |
| `data/screen_build_log.json` | Match rates, premise agreement, label distributions, parse stats |
| `results/scores/*.jsonl` | Raw per-unit scores (judges orig/disg, round-trip, pilot, recall probe) |
| `results/analysis.json` | Every table: sets × metrics, paired deltas, contamination, combination, per-type, invariance, complexity, system level, coverage, cost, label quality |
| `method_out.json`, `full_method_out.json`, `mini_method_out.json`, `preview_method_out.json` | exp_gen_sol_out per-item output at the workspace root (full = identical copy; mini = 3 examples per dataset; preview = mini with strings truncated); `uv run method.py` (default stage `analysis`) regenerates them from the cached scores |
| `results/method_out.json` | Same content, next to the other results |
| `results/tables/*.csv` | CSV versions of the main tables |
| `results/judge_label_disagreements.csv` | Track-L items where the judge disagrees with the auto label (for adjudication in iteration 2) |
| `results/per_item_scores.jsonl`, `results/rewrite_scores.jsonl` | Flat per-item / per-rewrite scores |
| `results/local_cache.jsonl`, `results/llm_cache.jsonl` | Every LLM input→output (local and API), for exact re-runs |
| `results/summary.md` | Plain-language results |
| `logs/` | Stage logs |

## How to run
```bash
bash restore.sh all                      # venv, NLTK corpora, pilot unzip, model weights into the shared HF cache
export PYTHONHASHSEED=0
for s in labeller screen prep pilot; do .venv/bin/python method.py --stage $s; done
# planned API path (OpenRouter; ≈$2; every call cached in results/llm_cache.jsonl)
for s in promptdev prereg; do .venv/bin/python method.py --stage $s; done
.venv/bin/python method.py --stage judges --limit 20 && .venv/bin/python method.py --stage judges
.venv/bin/python method.py --stage strong --limit 20 && .venv/bin/python method.py --stage strong
.venv/bin/python method.py --stage llm_api            # API verbalise/re-formalise + recall probe
.venv/bin/python method.py --stage rt_equiv && .venv/bin/python method.py --stage roundtrip   # z3 + GPU NLI/embeddings
# secondary local-GPU judges (open weights; ≈75 min on an RTX 4000 Ada; cached in results/local_cache.jsonl)
for s in promptdev_local prereg_local; do .venv/bin/python method.py --stage $s; done
.venv/bin/python method.py --stage llm_local && .venv/bin/python method.py --stage rt_llm_local
.venv/bin/python method.py --stage rt_equiv --variant local && .venv/bin/python method.py --stage roundtrip --variant local
.venv/bin/python method.py --stage analysis
.venv/bin/python tests/audit_headlines.py              # independent re-derivation + placebos
```

## Restoring removed files
| Deleted path (see `.aii/manifest.yaml`) | Restore |
|---|---|
| `.venv/` | `bash restore.sh venv` (uv venv + `requirements.txt` + `python -m spacy download en_core_web_sm`) |
| `pilot_ref/` | `bash restore.sh pilot` (unzips `user_uploads/dpv_pilot_study.zip`) |
| `src/**/__pycache__/` | regenerated automatically |
| model weights (not in this workspace; they live in the shared HF cache) | `bash restore.sh models` |
