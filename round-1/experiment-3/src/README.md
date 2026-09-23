# Candidate C: do other models' translations agree? (cross-system z3 consensus for NL→FOL faithfulness)

This is experiment 3 of iteration 1 (GEN_ART) of run `run_u75jRHUss0zo`. It screens a **text-free, gold-free consensus
metric** for NL→FOL output quality on the shared frozen screen, and compares it with the sampling self-consistency
baselines that reviewers ask for first.

For a candidate formalisation `c` of sentence `t`, the pool is every OTHER system's translation of `t`: six fresh
OpenRouter model families plus the released Logic-LM systems, always leaving out `c`'s own system. The scores are:

| score | definition (higher = more likely an error) |
|---|---|
| `c_score` (primary, pre-registered) | `1 - eq_frac`: the share of pool members that are **not** z3-equivalent to `c` modulo vocabulary (`eqmv` = exact z3 equivalence, else `align()` renaming in either direction, else a merge/split/reification `gran_bridge`) |
| `medoid_depth` | minimal typed-repair distance (0–3) from `c` to the pool medoid; `medoid_ops` gives the operator(s) |
| `cluster_entropy` | semantic entropy of the z3-eqmv equivalence classes of pool ∪ {c} |
| `c_score_peers6` / `_nonoai` / `_llm2` | the same as `c_score`, over the six fresh peers only / the five non-OpenAI peers / the other Logic-LM systems only |
| `sc5_cheap` (baseline) | `1 -` the share of K=5 gpt-4.1-nano samples (T=0.7, same prompt) that are eqmv to `c` |
| `sc5_same` (baseline) | the same with gpt-3.5-turbo; this is a true same-model SC, but only for the gpt-3.5 candidates |
| `predset_instab_sc` / `_pool` (baselines) | `1 -` the mean Jaccard of predicate names, `c` vs the SC samples / vs the pool (the user's rerun predicate-set similarity metric) |
| `fol_length` (baseline) | number of atoms |
| `misalign` (confound probe only; **uses the gold**) | `1 - alignable_frac` of `c`'s predicates against the reference |

All reusable functions live in `src/common.py` (`eqmv`, `label`, `strata`, `medoid_repair`, `alignable_frac`) and
`src/consensus.py` (`score_candidate`, `sc_scores`). Each takes `(text, fol)` or a set of FOL strings, and none of
them needs a gold formula.

## Headline results

Primary contrast: track L (the released Logic-LM FOLIO-dev outputs), CORRECT (297) vs ERROR (249), n=546.
95% CIs come from 2,000 bootstrap resamples clustered by sentence.

| score | AUROC [95% CI] | notes |
|---|---|---|
| **c_score** | **0.866 [0.821, 0.906]** | AUPRC 0.827 at prevalence 0.456 |
| c_score_peers6 (fresh peers only) | 0.872 [0.830, 0.911] | adding the Logic-LM systems to the pool adds nothing |
| c_score_nonoai (five non-OpenAI peers) | 0.863 [0.820, 0.903] | the signal does not come from OpenAI lineage |
| c_score_llm2 (two other Logic-LM systems) | 0.753 [0.701, 0.806] | a smaller pool that shares the prompt |
| cluster_entropy | 0.773 [0.724, 0.820] | ΔAUROC vs c_score −0.092 [−0.127, −0.061] |
| medoid_depth | 0.722 [0.673, 0.774] | quantised (0–3) |
| sc5_cheap (gpt-4.1-nano K=5) | 0.725 [0.669, 0.781] (n=546) | **ΔAUROC c_score − sc5_cheap = +0.140 [0.085, 0.197]** (all 546 items) |
| sc5_same (gpt-3.5 K=5, gpt-3.5 candidates) | 0.716 [0.632, 0.796] (n=167) | ΔAUROC c_score − sc5_same = +0.140 [0.057, 0.227] |
| predset_instab_pool | 0.770 [0.717, 0.821] | ΔAUROC c_score − it = +0.096 [0.050, 0.144] |
| fol_length | 0.527 | trivial baseline |
| misalign (gold-using probe) | 0.835 | CORRECT ⇒ alignable **by construction of the labeller**; see the confound section |

Pre-registered threshold (flag iff the candidate is not eqmv to the medoid): recall 0.62 [0.56, 0.68], false alarms
0.14 [0.10, 0.18], precision 0.79. Re-weighted to 10% / 25% prevalence, precision is 0.33 / 0.60.
Cross-fitted logistic regression (GroupKFold by sentence): [c_score, sc5_cheap] vs [sc5_cheap] alone gives ΔAUROC
+0.147 [0.099, 0.199]. So **consensus adds signal beyond sampling self-consistency**. SC adds nothing on top of
consensus: the cross-fitted [c_score, sc5_cheap] model scores 0.865, the same as c_score alone (0.866).

**Secondary contrasts.** Lenient contrast (ERROR ∪ COMPOUND): 0.882. Vocab-strict contrast: 0.875. Track H (human
original gold vs corrected gold, 35 errors): 0.832. Secondary multi-family sample (the 6 peers' own outputs as
candidates, n=1,686): 0.825, with every family between 0.81 and 0.85.

**Shared-aligner confound.** The metric and the labeller share `align()`. In the labeller, CORRECT implies
alignable_frac = 1 (100% of CORRECT items), while only 33% of ERROR items have it. That is why `misalign` alone reaches
0.835. On the **vocab-clean subset**, where every item has alignable_frac = 1 so the artefact cannot act, c_score
AUROC is **0.852 [0.765, 0.929]** (82 errors vs 297 correct), against 0.714 for sc5_cheap (paired Δ +0.138 [0.035, 0.236]).
The partial Spearman of c_score with the label, controlling for alignable_frac, is 0.51. [c_score, misalign] vs
[misalign] adds +0.132 [0.086, 0.185]. **So c_score is not mainly the alignment artefact.**

**Where consensus fails, and its ceiling.** 38% [32%, 44%] of the track-L ERROR items are eqmv to the pool medoid
(shared blind spot), so recall at the medoid threshold is capped at 0.62. The medoid is itself correct for only 34%
of the error items. For CORRECT items it is correct 81% of the time.
Blind spots by error type:

| error type | blind-spot rate | recall at threshold |
|---|---|---|
| POLARITY | 5% | 0.95 |
| COVERAGE (ADD/DROP) | 41% | 0.59 |
| STRUCT | 57% | 0.43 |

GPT-4 errors are the most "consensual" (48% blind). Among depth-1/2 errors, the medoid repair operators match the
labeller's operators exactly in 81% of cases, against a majority-class chance of 46%. The coarse class matches in 92%
of cases (chance 78%). So the repair readout **does** type errors.

**Rewrite invariance** (CORRECT candidates, scored against an unchanged pool):

| rewrite | flip rate | false alarms |
|---|---|---|
| REORDER / DEMORGAN / CONTRAPOSITIVE / PRENEX | 0% (z3 ⇒ invariant by construction) | — |
| RENAME (WordNet synonym heads + hashed constants) | 77% | **96%** (base 19%) |
| RENAME_PRED_ONLY | — | 84% |
| RENAME_CONST_ONLY | — | 100% |

**The aligner does not survive synonym or constant renaming.** This is the metric's main invariance failure. It is
the same G2 failure seen in the sibling runs.

**Complexity.** FOLIO-dev track L is almost all short: 505/546 items are under 12 words, and there are no exception
sentences. Only these strata are testable (≥50 errors and ≥50 correct items):

| stratum | c_score | sc5_cheap |
|---|---|---|
| <12 words | 0.871 | 0.722 |
| n_cond = 0 | 0.878 | 0.730 |
| n_cond = 1–2 (54/82) | 0.822 | 0.705 |

The long, heavily conditioned stratum has **5 items (descriptive only)** and is deferred to held-out dataset E, as
designed. The complexity interaction term is negative for c_score (−0.94 per SD of words) and near zero for SC; this
is descriptive only.

**System level (descriptive).** Across 9 systems (3 Logic-LM + 6 peers), the Spearman correlation of error rate with
mean c_score is 0.87.

**Cost.**

| item | cost |
|---|---|
| Total OpenRouter spend (logs/cost_log.jsonl) | $1.5194 |
| C's 6 peers, per sentence, amortised over story-level calls | $0.00149 |
| C's 6 peers, single-sentence (MALLS) prompt | $0.00058 |
| SC_cheap (gpt-4.1-nano K=5), per unit | $0.00087 |

C's per-sentence cost passes the $0.002 gate in both deployment modes. z3 time is 0.15 s per candidate on 4 CPUs
(cold full run: 15,265 pairwise eqmv calls in 7 s, 599 medoid repairs in 45 s, 1,575 labels in 205 s).

**Sanity checks** (pipeline checks, not validation):
- The corrected gold, scored as a pseudo-candidate, gets mean eq_frac 0.48; ERROR items get 0.32 and CORRECT items
  0.82.
- Planted DROP/NEG edits raise c_score in 29/30 cases.
- The screen label hash `0e43cbdd…` was reproduced by an independent re-run of `screen.py`.
- F8 (consensus degenerate) did **not** fire: only 17% of primary items have eq_frac = 0.

## Independent re-derivation audit (`tests/audit_rederive.py` → `results/audit_rederive.json`)

The audit rebuilds everything from the raw files through a separate code path:
- pools, from `peer_outputs.jsonl` and the screen;
- equivalences, read directly from `pairwise_eq.jsonl`;
- medoids, SC shares and alignability, recomputed inline;
- AUROC, by brute-force pairwise win counting.

It does not read `consensus.json` or `summary.json`, except for the final comparison. It reproduces these numbers
**exactly**:

| quantity | value |
|---|---|
| c_score AUROC | 0.8655 |
| sc5_cheap AUROC | 0.7254 |
| Δ (n=546) | +0.140 |
| vocab-clean AUROC (n=379, 82 errors) | 0.8518 |
| recall at threshold | 0.6185 |
| false alarms at threshold | 0.138 |
| total cost (from the raw response cache as well as the cost log) | $1.5194 |

Placebos:
- 200 label permutations give mean AUROC 0.5001 (95th percentile 0.539; permutation p = 0.005 for 0.866).
- Permuted Δ has mean −0.0007 (97.5th percentile 0.036).
- A constant score gives AUROC 0.5.

**Not independently re-derived:** the bootstrap CIs, the other contrasts and per-stratum tables, the rewrite-invariance
rates, the blind-spot / operator-agreement rates, and the secondary peer-as-candidate sample.

## Deviations and limitations (read before citing)

1. **SC_cheap was completed in a second pass.** The first run hit the shared $50/day OpenRouter key limit (HTTP 403,
   13:33 UTC), leaving SC_cheap at 231/307 units. After the key was replaced, the missing calls were made (15:12–15:19
   UTC; +$0.10). Cached responses were not re-billed. SC_cheap now covers **all 307 units and all 546 primary items**.
   Every number in this README comes from the complete run. Against the partial run, sc5_cheap moved from 0.736
   (n=392) to 0.725 (n=546), and Δ moved from +0.154 to +0.140; the conclusion is unchanged. SC_same (117 units)
   and all peers were already complete. The optional F8 vocabulary-shared variant was not run: its trigger (more than
   80% of items with eq_frac = 0) did not fire (17%).
   The rerun exposed that WordNet was missing from the environment. Without it, RENAME silently falls back to nonce
   names, which gave false alarms of 99% instead of 96%. WordNet now lives in `data/nltk_data/`. `consensus.py`
   refuses to run without it, and `summary.json → rewrite_invariance.rename_head_token_source` records how each head
   token was renamed: 132 by WordNet synonym, 64 by nonce fallback for tokens WordNet lacks.
2. **Format-only system message.** Modern chat models do not continue the Logic-LM few-shot pattern: dry run v0
   (kept in `data/peer_raw_dryrun_v0/`) produced prose and re-solved the demo problems. Every peer and SC call
   therefore gets one fixed system message stating the output format. The user prompt is Logic-LM's `FOLIO.txt`
   verbatim.
   Peers often echoed the label `FOL ::: <formula>`. The parser strips this deterministically, with no re-billing.
3. **SC for gpt-4 / davinci candidates is a "single-other-model agreement" baseline** (gpt-4.1-nano), not a
   same-model SC.
   SC_same uses `openai/gpt-3.5-turbo`, the current snapshot, not 2023's 0301/0613.
4. **Screen facts.**
   - Conclusion match is 112/202 (below 150), so the match-rate fallback fired.
   - Track L = 336 conclusion items + 531 agreed-premise items (premise ref = original ≡mv folio-refined).
   - Premise-only units (U_P, 5 of them) were added so that every agreed premise has peer translations.
   - 20 items whose corrected gold does not parse with `fol.py` (e.g. `=`, `ś`, numerals) are `REF_UNPARSEABLE` and
     excluded. The parser was left unchanged by design.
5. **Bug found and fixed before the final numbers.** Identical formula strings were not treated as equivalent, because
   such pairs were never sent to z3. This had depressed every consensus and SC score: preliminary AUROC was 0.60. It
   was fixed in `eqcache.PairCache.get`. All reported numbers come from the fixed run.
6. Labels are automatic (the census labeller). COMPOUND and GRAN items are excluded from the primary contrast. Dataset
   E's adjudicated labels will re-score this screen by `item_id` in iteration 2.
7. The ⊕ precedence fix changed exactly the 3 ⊕ census rows predicted by the iter-3 audit (COMPOUND → EQUIV) and 0 of
   the 20 plain rows (`results/census_regression.json`).

## Layout

```
src/fol.py              parser + z3 (⊕ precedence fix: PREC xor=3, like ∨)
src/repair_census.py    align / gran_bridge / typed repair search (unchanged except data path)
src/common.py           norm, item_id, LABEL(), eqmv(), strata(), medoid_repair(), alignable_frac()
src/screen.py           STEP 1: shared screen (track L/H), labels, units -> results/screen_items.json, units.json, hash
src/peers.py            STEP 3/4: OpenRouter peers + SC samples (cached, cost-guarded) and parse/map (build)
src/eqcache.py          resumable parallel caches: pairwise eqmv, labels, medoid repairs
src/consensus.py        STEP 5/6 + T5: pool scores, medoid repair, SC scores, rewrites, planted errors, peer-as-candidate
src/rewrites.py         RENAME / REORDER / DEMORGAN / PRENEX / CONTRAPOSITIVE (+ RENAME_PRED_ONLY / _CONST_ONLY)
src/analysis.py         STEP 7/8: AUROC/AUPRC/CI, paired deltas, tie-aware acc, confound, blind spots, strata, cost
method.py               entry point: runs the whole pipeline (tests -> screen -> peers/SC -> consensus -> analysis -> audit)
src/make_previews.py    (superseded by the aii-json format script: full_/mini_/preview_method_out.json)
tests/audit_rederive.py independent re-derivation of the headline numbers + permutation/constant placebos
tests/test_fol.py       T0 unit tests (precedence, eqmv symmetry, rename/contrapositive, item_id, labeller)
tests/census_regression.py  T0/F7 census regression under the precedence fix
method_out.json         per-item predictions (exp_gen_sol_out schema; 4 datasets, 1,169 examples) + headline metadata
results/summary.json    every table (auroc per contrast x score, deltas, cross-fit, per-system, per-type, pool-size
                        curve, confound, blind spots, operator agreement, complexity, coverage, cost, secondary, sanity)
results/prereg.json     pre-registration (written before any AUROC; contains the screen label hash) + prereg.sha256
results/screen_items.json  the frozen screen (item_id, track, system, text, candidate, reference, label, ops, strata)
results/screen_label_hash.txt, screen_report.json (T1 counts, match rate), census_regression.json
results/units.json      translation units (prompts' problem/question + premise slots)
results/peer_outputs.jsonl        parsed/mapped peer translations (6 families)
results/peer_outputs_labelled.json  peer outputs as candidates with labels, consensus and SC scores (secondary sample)
results/sc_samples.jsonl          parsed/mapped self-consistency samples (sc_cheap, sc_same)
results/pairwise_eq.jsonl, label_cache.jsonl, repair_cache.jsonl   z3 caches (resumable)
results/consensus.json, analysis_table.jsonl   per-candidate records
results/consensus_mini20.json     T3 mini end-to-end run (20 sentences)
data/logiclm/           Logic-LM FOLIO_dev outputs (3 systems) + FOLIO.txt prompt
data/peer_raw/          every raw OpenRouter response (JSON with usage/cost), the only copy of paid outputs
data/peer_raw_dryrun_v0/  dry run without the format system message (documents deviation 2)
logs/cost_log.jsonl     per-call cost ledger (total = $1.5194)
data/nltk_data/         WordNet (used by the RENAME rewrite; 40 MB, redownloadable)
```

The kept artifacts live at
`/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/`.
All of them are small text files.

## How to run

```bash
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r <(python3 -c "import tomllib;print('\n'.join(tomllib.load(open('pyproject.toml','rb'))['project']['dependencies']))")   # exact pinned versions
.venv/bin/python -c "import nltk; nltk.download('wordnet', download_dir='data/nltk_data'); nltk.download('omw-1.4', download_dir='data/nltk_data')"
bash run_all.sh      # or: .venv/bin/python method.py [--skip-api]   (cached responses; no re-billing)
```

`peers.py call` re-uses `data/peer_raw/` and only calls OpenRouter for missing (model, unit, sample) triples. It needs
`OPENROUTER_API_KEY`. It stops optional arms at $8 and everything at $9.5.

## Restoring removed files

| removed path | how to restore |
|---|---|
| `.venv/` | regenerable; see the install command above (`uv venv` + `uv pip install` of the pyproject dependencies) |
| `__pycache__/` (src/, tests/) | regenerable; recreated automatically by Python |
| `.pytest_cache/` | regenerable; `.venv/bin/python -m pytest -c /dev/null --rootdir . --noconftest -q tests/test_fol.py` |
| `data/nltk_data/` | redownloadable; `.venv/bin/python -c "import nltk; nltk.download('wordnet', download_dir='data/nltk_data'); nltk.download('omw-1.4', download_dir='data/nltk_data')"` |
