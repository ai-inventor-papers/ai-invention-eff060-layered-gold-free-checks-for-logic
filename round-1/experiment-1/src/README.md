# FOL-Triage wide screen: a gold-free, three-layer faithfulness check for NL→FOL

This is invention-loop iteration 1, experiment A of run `run_u75jRHUss0zo`. It is the first test of FOL-Triage on real
LLM outputs. The iter-3 pilot tested it only in-sample, on annotator errors.

**The question.** Given a sentence and a candidate FOL formula, and no gold formula, can a cheap score tell whether the
formula is faithful to the sentence? Can it also say which kind of error the formula contains?

**The metric** is four released functions, each taking `(text, fol)`, in `src/fol_triage.py`:

| layer | function | what it measures | cost |
|---|---|---|---|
| L1 | `fol_lint(fol)` | Text-free formula "smells": renderings that are improbable for any English sentence. They are EX_IMP ∃x(A→B), ALL_AND ∀x(A∧B), IFF_RESTR, GLUE, FREE, VACUOUS (z3), TRIVIAL (z3), ARITY and DANGLING. The list is frozen from iter-3. | $0, z3 |
| L2-bow | `content_accounting(text, fol)` | Baseline, iter-3. Counts predicates that no text word anchors (ADD) and the share of text content words that no symbol carries (DROP). | $0 |
| L2-role | `role_accounting(text, fol)` | spaCy dependency roles (condition, asserted, exception, negation) must agree with the **exact z3 monotonicity** of the aligned predicates: condition→DOWN, asserted→UP, exception→UP, each flipped by negation. It also checks subject/object slot order. | $0, z3 + spaCy |
| L3 | `formula_role_profile(fol)` + `role_questionnaire(text)` + `l3_compare` | A cheap LLM (gemini-2.5-flash-lite) reads **only the sentence** and fills a frozen role schema. z3 answers the same schema exactly on the formula side. Mismatches are counted per field. | about $0.17 per 1,000 sentences |
| fused | `method.py::triage` | A cascade L1 → L2 → L3 gives the fired layer and an error code. A logistic fusion fitted on track H only gives `p_error`. | |

## Key findings (primary set: track L, ERROR vs CORRECT, n=477 with 199 errors)

The fused FOL-Triage score is the pre-registered primary. It is trained on track H with the sentence-leak guard and frozen
before it is applied to track L. It reaches **AUROC 0.759, 95% CI [0.695, 0.825]**. This passes the pre-registered AUROC
gate (≥ 0.65), the coverage gate (0.92, with unparseable outputs counted as failures) and the cost gate ($0.0002 per item).
It **fails the rewrite-FA gate**: 0.275 of rewritten CORRECT items are flagged, the same rate as for their originals. The
fused threshold transfers poorly from H to L: 19% false alarms on track-L CORRECT, against 10% calibrated on H. The flip
rate under rewrites is at most 0.06.

* **Most of the fused score's signal comes from the bag-of-words baseline and L3.**
  * L2-bow alone reaches 0.737.
  * L3 alone reaches 0.756: flash-lite reads only the sentence and z3 answers the same schema from the formula.
  * Fused minus L2-bow is +0.022, CI [−0.019, 0.061], and fused minus L3 is +0.004, CI [−0.053, 0.067]. Neither gain is
    significant. A placebo with permuted labels gives a 95% range of [−0.025, 0.030] for the same difference.
  * Two secondary fusions score higher, but neither is a valid estimate:
    * the all-H model (no leak guard) reaches 0.827; it has seen the same FOLIO sentences;
    * a within-L cross-fit reaches 0.864; it is in-domain and optimistic.
  * On the secondary set that drops the ADD+DROP vocabulary artefacts, L3 beats L2-bow by +0.076, CI [−0.007, 0.162].
* **L1 (the text-free lint) does not transfer to real LLM outputs.** It fires on 2% of track-L errors, with 0.4% false
  alarms; its AUROC is 0.508. On track H (annotator errors) its AUROC is 0.655. The 2023 OpenAI systems rarely produce the
  smells that human annotators do.
* **L2-role (spaCy roles checked against z3 monotonicity) is a negative result.** Its AUROC is 0.557, significantly below
  L2-bow (−0.19). It does detect the NEG operator (5/5), but polarity and role errors are rare in this screen, where ADD and
  DROP dominate.
* **Replacing z3 by the LLM reading the formula (decomposed judge) hurts.** The L3 score falls from 0.756 to 0.697, a paired
  Δ of −0.059 with CI [−0.094, −0.022]. The LLM misreads argument slots (only 0.58 correct) and the role/monotonicity of the
  formula (0.86 correct), which z3 answers exactly.
* **Contamination: no sign of benefit from memorised gold.** On nonce-disguised sentences the track-L L3 AUROC is 0.770,
  against 0.765 for the originals (Δ −0.005, CI [−0.063, 0.049]). Field accuracy drops only slightly, for example role
  0.92 → 0.89.
* **L3 answerer accuracy** is measured on HREF, where the corrected gold serves as the formula. Field accuracies are
  role 0.91, claims 0.86, order 0.95, missing 0.92 and extra 0.92; these fields are gated. Force (0.69) and exception
  (n=1) are excluded. Test-retest agreement on role is 0.99. The second model, qwen3-30b-a3b, gives similar numbers.
  The local Qwen2.5-1.5B is weaker: role 0.76, and an L3 AUROC of 0.708 on track L.
* **Label artefact.** 59% of track-L ERRORs are pure ADD+DROP repairs, i.e. vocabulary or arity choices such as
  `Lunch(james)` vs `HasLunch(james, company)` that the aligner cannot bridge. Panel adjudication in iteration 2 is needed
  before any claim.
* **Complexity.** Only short sentences (under 12 words) are testable on this screen. Long and heavily conditioned sentences
  (≥ 20 words: 3 items; ≥ 3 conditions: 2 items) are UNTESTABLE here, as pre-declared, and are deferred to dataset E.
* **Out of scope for this artifact:** judge, round-trip and self-consistency baselines, which are compared in iteration 2 on
  the same item_ids.

## L3 model history and integrity notes (read before citing numbers)

* **L3 model.** The planned primary, `google/gemini-2.5-flash-lite` via OpenRouter, is the one used. Between 13:30 and
  about 15:00 UTC on 2026-09-23 the shared OpenRouter key was at its $50 daily limit: every model returned 403. During that
  window a local llama.cpp Qwen2.5-1.5B-Instruct Q4_K_M (CPU, JSON-schema grammar) answered all 421 L3 sentences. The key
  came back before the final `prereg.json` was written, and the planned models were restored: flash-lite as primary and
  qwen3-30b-a3b as the robustness row. The local answers are kept as an extra robustness row (`l3_score_local`,
  `L3_gate_local_model`). Total OpenRouter spend was **$0.29**.
* **L3 prompt.** The prompt carries a "compact on ONE line" instruction that was added for the local model and kept for
  every model.
* **L2-role calibration.** The role rules were refined on HREF (known-correct gold) only. The false-alarm rate fell from
  18% to 7.8%, the token resolution rate is 70%, and T4 still passes 10/10. This was done before any track-L score was
  inspected.
* **Dry runs.** Two dry runs of the whole pipeline joined track-L labels before the final run:
  * a full-size run with incomplete local-model L3 coverage;
  * a 15-item live run.

  After them, no scoring rule, threshold, feature or fusion setting was changed. The code hashes are in
  `results/code_freeze_after_fullsize_dryrun.json`. Later code edits fall into three kinds:
  * the model restore described above;
  * the not_run texts;
  * three reporting fixes in `analysis.py`:
    * a bug made secondary sets reuse the primary set's bootstrap subset, which yielded wrong CIs; fixed;
    * cost was rounded to $0.0; it is now reported per 1,000 calls;
    * the rewrite-FA gate note now adds the flip rate.

  None of these edits changes a score.
* **Headline re-derivation (TODO 4).** `src/audit_rederive.py` recomputes the headline numbers through a different code
  path, with the output in `results/audit_rederive.json`:
  * the primary AUROCs (fused 0.7589, L2-bow 0.7367, L3 0.7563, L1 0.5083), using a hand-written rank AUROC with labels
    read directly from `screen_items.json`;
  * fused p re-predicted from the pickled no-leak model; the maximum difference from the stored values is 2e-16;
  * fused FA/TPR at the pre-registered threshold (0.194 / 0.568), the parse rate (0.920) and the spend ($0.2919).

  Permuted-label placebos give AUROC ≈ 0.50 for every score. The bootstrap CIs and the stratum, invariance and ablation
  numbers were **not** independently re-derived.

## Data: the frozen shared screen (`screen_items.json`, built by `src/run_screen.py`)

* **Track L**: Logic-LM released FOLIO-dev programs from three systems: gpt-3.5-turbo, gpt-4 and text-davinci-003. Each
  file has 204 records. A line is kept when its normalised text equals one of the 202 curated conclusions (arXiv 2606.02837,
  HF DSAVlab-UNIUD); 112 distinct conclusions match. Because 112 is below 150, the set is extended, as planned, with premises
  of matched stories on which the original FOLIO and folio-refined formulas agree (EQUIV or VOCAB); 271 premise texts
  qualify. **753 items** remain after deduplication by `item_id = sha1(system|norm(text)|fol)[:16]`.
* **Track H**: 302 curated items (FOLIO conclusions and MALLS-test). The candidate is the original annotator gold; the
  reference is the corrected gold.
* **HREF**: the corrected gold formula used as its own candidate. These are known negatives for calibration and are not in
  `screen_items.json`.
* **Labels** come from `src/labeller.py`, the iter-3 repair census with the ⊕ precedence fixed. Parsing is followed by z3
  equivalence, then vocabulary alignment, then a granularity bridge, then a typed-repair search of depth ≤ 2:
  * EQUIV or VOCAB → CORRECT;
  * GRAN → UNCERTAIN;
  * a repair of depth 1–2 → ERROR, with the repair operators recorded;
  * no repair found → UNCERTAIN (COMPOUND);
  * candidate does not parse → UNPARSEABLE, which stays in every denominator.

  `auto_class` is emitted with every label, so later steps can remap it.
* **Strata** are computed from the REFERENCE formula and the text: length, number of quantifiers, nesting depth, number of
  conditions, and exception markers.
* **Invariance set**: the first 150 track-L CORRECT items. It has five rewrite families: RENAME (WordNet synonym),
  REORDER, DEMORGAN, PRENEX and CONTRAPOSITIVE. Every family except RENAME is verified equivalent by z3; a family that does
  not apply is recorded as n/a.

## Layout

```
method.py                 STAGES 4-7: prereg -> calibration (H + HREF) -> scoring of track L (labels hidden) -> analysis
prereg.json               pre-registration: code sha256, thresholds, L3 schema/prompt/model, fusion spec, calibration block
screen_items.json         frozen shared screen (track L + track H) with labels; screen_meta.json = counts, match rate, sha256
href_items.json           corrected-gold known negatives; invariance_set.json = rewrites of 150 CORRECT track-L items
method_out.json           exp_gen_sol_out: datasets screen_track_L / screen_track_H / href_calibration + all metrics
src/fol.py                Unicode FOL parser -> z3 (iter-3, PRECEDENCE_FIX xor=3), to_str printer
src/labeller.py           equivalent_modulo_vocab / minimal_typed_repair / label (iter-3 repair_census logic)
src/repair_census.py, lint_smells.py, content_accounting.py   frozen iter-3 code (copied verbatim)
src/screen.py, run_screen.py   STAGE 2 screen builder;  src/rewrites.py  invariance families
src/fol_triage.py         the released functions (L1, L2-bow, L2-role, formula profile, L3 questionnaire/compare, decomposed judge)
src/pipeline.py           CPU-layer workers (spawn pool, per-item timeouts, cache), LLM stage wrappers, scoring_view()
src/llm.py                OpenRouter client + cost ledger, read-only CachedLLM, LocalLLM (llama.cpp fallback)
src/run_cpu.py, run_local_llm.py   cache fillers (CPU layers; local LLM with a hard deadline)
src/disguise.py           nonce disguise of sentence + formula vocabulary (contamination control)
src/analysis.py           STAGE 7 - the ONLY module that joins labels to scores; metrics.json + per_item.jsonl
src/output.py             method_out.json writer
src/test_units.py         T3/T4 unit tests;  check_t0_t1.py  T0/T1 reproduction;  check_role_href.py  L2-role calibration
results/                  metrics.json, per_item.jsonl, calibration.json, invariance_scores.json, ablations.json,
                          fusion_H_noleak.pkl / fusion_H_all.pkl, t0_t1_checks.json, role_href_calibration.json, not_run.json
cache/                    labels.jsonl (z3 labeller), cpu_layers.jsonl, profiles_extra.jsonl, llm_cache.jsonl, cost_ledger.jsonl
data/                     inputs copied from iter_3/gen_hypo (curated FOLIO/MALLS, folio-refined) + data/logiclm/ (fetched)
logs/                     run logs
```

## How to run

```bash
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python z3-solver nltk spacy numpy scipy scikit-learn pandas aiohttp loguru requests \
    tenacity jsonschema psutil huggingface_hub
uv pip install --python .venv/bin/python llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu \
    --only-binary llama-cpp-python
.venv/bin/python -m spacy download en_core_web_sm
.venv/bin/python -c "import nltk; nltk.download('wordnet', download_dir='nltk_data'); nltk.download('omw-1.4', download_dir='nltk_data')"
cd src && ../.venv/bin/python run_screen.py          # screen (z3 labels cached in cache/labels.jsonl)
../.venv/bin/python run_cpu.py                       # L1 / L2 / z3 profiles
../.venv/bin/python run_local_llm.py $(( $(date +%s) + 7200 )) q   # OPTIONAL: local-model robustness row only
cd .. && .venv/bin/python method.py                  # prereg (if absent) -> calibration -> scoring -> analysis
```
With `cache/` present, `method.py` reproduces every number without any new LLM call: every answer is cached. `LLM_LIVE=0`
forces cache-only mode, and local-model answers are always read from the cache. `src/rerun_analysis.py` re-runs
STAGE 7 only; `src/make_report.py` regenerates the Results section below; `src/audit_rederive.py` is the independent
re-derivation.

## Restoring removed files

* `.venv/` (delete: regenerable): `uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu && .venv/bin/python -m spacy download en_core_web_sm`. All versions are pinned in `pyproject.toml`; the spaCy model en_core_web_sm is 3.8.0.
* `nltk_data/` (delete: redownloadable):
  `.venv/bin/python -c "import nltk; nltk.download('wordnet', download_dir='nltk_data'); nltk.download('omw-1.4', download_dir='nltk_data')"`.
* `__pycache__/` and `src/__pycache__/` (delete: regenerable): Python bytecode caches, recreated automatically by any
  run, e.g. `.venv/bin/python method.py`.
* The local GGUF model lives in the run's shared HF cache and is not in this directory. To restore it:
  `huggingface-cli download Qwen/Qwen2.5-1.5B-Instruct-GGUF qwen2.5-1.5b-instruct-q4_k_m.gguf`.

## Results (generated by `src/make_report.py` from `results/metrics.json`)

### Screen

* Track L: 753 items, labels {'CORRECT': 278, 'UNPARSEABLE': 60, 'UNCERTAIN': 204, 'ERROR': 199, 'REF_UNPARSEABLE': 12}; auto classes {'VOCAB': 115, 'UNPARSEABLE': 60, 'COMPOUND': 187, 'ADD+DROP': 117, 'EQUIV': 163, 'ADD': 30, 'BIND': 3, 'SWAP': 6, 'GRAN': 17, 'BIND+DROP': 2, 'DROP': 22, 'QUANT': 2, 'REF_UNPARSEABLE': 12, 'ADD+SWAP': 2, 'CONN': 4, 'ADD+BIND': 1, 'SWAP+SWAP': 3, 'NEG': 4, 'BIND+NEG': 1, 'BIND+BIND': 1, 'DROP+SWAP': 1}.
* Track H: {'CORRECT': 201, 'REF_UNPARSEABLE': 8, 'ERROR': 35, 'UNCERTAIN': 22, 'READING_CHOICE': 19, 'UNPARSEABLE': 17}.
* Conclusion match 112/202 (extension with agreed premises applied). Premise agreement: {'EQUIV': 264, 'VOCAB': 7, 'UNPARSEABLE': 9, 'NONEQ': 10, 'REF_UNPARSEABLE': 31}.
* Label artefact: 0.588 of track-L ERRORs are pure ADD+DROP (one atom replaced by another). These are mostly predicate-vocabulary or arity choices the aligner cannot bridge, so the secondary set excludes them.

### Item-level discrimination (AUROC, 95% CI from a sentence-clustered bootstrap, B=2000)

**primary_L_ERROR_vs_CORRECT**: n=477, positives=199 (prevalence 0.417)

| score | AUROC | 95% CI | AUPRC | n scored |
|---|---|---|---|---|
| l1_any | 0.508 | [0.499, 0.519] | 0.425 | 477 |
| n_smells | 0.508 | [0.499, 0.519] | 0.425 | 477 |
| l2_bow | 0.737 | [0.677, 0.801] | 0.690 | 477 |
| l2_role | 0.557 | [0.527, 0.594] | 0.476 | 477 |
| l3_score | 0.756 | [0.701, 0.809] | 0.657 | 477 |
| p_fused_H | 0.759 | [0.695, 0.825] | 0.740 | 477 |
| p_fused_Hall | 0.827 | [0.778, 0.874] | 0.770 | 477 |
| p_fused_Lcf | 0.864 | [0.824, 0.902] | 0.789 | 477 |
| cascade_llmformula | 0.716 | [0.645, 0.789] | 0.717 | 477 |
| l3_score_llmformula | 0.697 | [0.639, 0.752] | 0.598 | 477 |
| l3_score_local | 0.708 | [0.637, 0.774] | 0.603 | 477 |

Paired ΔAUROC (same bootstrap resamples): p_fused_H - l1_any: 0.251 [0.187, 0.316]; p_fused_H - n_smells: 0.251 [0.187, 0.316]; p_fused_H - l2_bow: 0.022 [-0.019, 0.061]; p_fused_H - l2_role: 0.203 [0.128, 0.278]; p_fused_H - l3_score: 0.004 [-0.053, 0.067]; l2_role - l2_bow: -0.181 [-0.260, -0.101]; l3_score - l2_bow: 0.018 [-0.054, 0.087]; p_fused_H - p_fused_Lcf: -0.105 [-0.162, -0.052]; p_fused_H - p_fused_Hall: -0.068 [-0.107, -0.035]

Separately bootstrapped `cascade_llmformula` on its 477-item subset (199 positives): l1_any=0.508, n_smells=0.508, l2_bow=0.737, l2_role=0.557, l3_score=0.756, p_fused_H=0.759, p_fused_Hall=0.827, p_fused_Lcf=0.864, cascade_llmformula=0.716; paired vs l3_score {'delta_mean': -0.0396, 'CI95': [-0.1084, 0.0329], 'P(delta<=0)': 0.8625}

Separately bootstrapped `l3_score_llmformula` on its 477-item subset (199 positives): l1_any=0.508, n_smells=0.508, l2_bow=0.737, l2_role=0.557, l3_score=0.756, p_fused_H=0.759, p_fused_Hall=0.827, p_fused_Lcf=0.864, l3_score_llmformula=0.697; paired vs l3_score {'delta_mean': -0.0589, 'CI95': [-0.0944, -0.0224], 'P(delta<=0)': 0.9995}

Separately bootstrapped `l3_score_local` on its 477-item subset (199 positives): l1_any=0.508, n_smells=0.508, l2_bow=0.737, l2_role=0.557, l3_score=0.756, p_fused_H=0.759, p_fused_Hall=0.827, p_fused_Lcf=0.864, l3_score_local=0.708; paired vs l3_score {'delta_mean': -0.049, 'CI95': [-0.1189, 0.0204], 'P(delta<=0)': 0.92}

**secondary_L_ERRORuCOMPOUND_vs_CORRECT**: n=664, positives=386 (prevalence 0.581)

| score | AUROC | 95% CI | AUPRC | n scored |
|---|---|---|---|---|
| l1_any | 0.532 | [0.518, 0.547] | 0.607 | 664 |
| n_smells | 0.532 | [0.518, 0.547] | 0.608 | 664 |
| l2_bow | 0.756 | [0.708, 0.802] | 0.806 | 664 |
| l2_role | 0.565 | [0.542, 0.590] | 0.634 | 664 |
| l3_score | 0.761 | [0.713, 0.807] | 0.776 | 664 |
| p_fused_H | 0.778 | [0.723, 0.827] | 0.845 | 664 |
| p_fused_Hall | 0.836 | [0.793, 0.872] | 0.873 | 664 |
| p_fused_Lcf | 0.864 | [0.821, 0.903] | 0.789 | 477 |
| cascade_llmformula | 0.744 | [0.687, 0.799] | 0.830 | 664 |
| l3_score_llmformula | 0.705 | [0.656, 0.754] | 0.739 | 664 |
| l3_score_local | 0.723 | [0.664, 0.777] | 0.750 | 664 |

Paired ΔAUROC (same bootstrap resamples): p_fused_H - l1_any: 0.246 [0.192, 0.294]; p_fused_H - n_smells: 0.246 [0.192, 0.294]; p_fused_H - l2_bow: 0.022 [-0.013, 0.057]; p_fused_H - l2_role: 0.212 [0.157, 0.267]; p_fused_H - l3_score: 0.017 [-0.032, 0.068]; l2_role - l2_bow: -0.190 [-0.244, -0.132]; l3_score - l2_bow: 0.005 [-0.058, 0.068]; p_fused_H - p_fused_Hall: -0.058 [-0.082, -0.034]

Separately bootstrapped `p_fused_Lcf` on its 477-item subset (199 positives): l1_any=0.508, n_smells=0.508, l2_bow=0.737, l2_role=0.557, l3_score=0.756, p_fused_H=0.759, p_fused_Hall=0.827, p_fused_Lcf=0.864; paired vs l3_score {'delta_mean': 0.1081, 'CI95': [0.0576, 0.1594], 'P(delta<=0)': 0.0}

Separately bootstrapped `cascade_llmformula` on its 664-item subset (386 positives): l1_any=0.532, n_smells=0.532, l2_bow=0.756, l2_role=0.565, l3_score=0.761, p_fused_H=0.778, p_fused_Hall=0.836, cascade_llmformula=0.744; paired vs l3_score {'delta_mean': -0.0164, 'CI95': [-0.0733, 0.0423], 'P(delta<=0)': 0.717}

Separately bootstrapped `l3_score_llmformula` on its 664-item subset (386 positives): l1_any=0.532, n_smells=0.532, l2_bow=0.756, l2_role=0.565, l3_score=0.761, p_fused_H=0.778, p_fused_Hall=0.836, l3_score_llmformula=0.705; paired vs l3_score {'delta_mean': -0.0549, 'CI95': [-0.0897, -0.0206], 'P(delta<=0)': 0.998}

Separately bootstrapped `l3_score_local` on its 664-item subset (386 positives): l1_any=0.532, n_smells=0.532, l2_bow=0.756, l2_role=0.565, l3_score=0.761, p_fused_H=0.778, p_fused_Hall=0.836, l3_score_local=0.723; paired vs l3_score {'delta_mean': -0.0379, 'CI95': [-0.0982, 0.0219], 'P(delta<=0)': 0.8915}

**secondary_L_ERROR_minus_pureADDDROP_vs_CORRECT**: n=360, positives=82 (prevalence 0.228)

| score | AUROC | 95% CI | AUPRC | n scored |
|---|---|---|---|---|
| l1_any | 0.504 | [0.495, 0.519] | 0.231 | 360 |
| n_smells | 0.504 | [0.495, 0.519] | 0.231 | 360 |
| l2_bow | 0.701 | [0.614, 0.781] | 0.457 | 360 |
| l2_role | 0.558 | [0.523, 0.603] | 0.293 | 360 |
| l3_score | 0.776 | [0.701, 0.848] | 0.482 | 360 |
| p_fused_H | 0.731 | [0.622, 0.831] | 0.496 | 360 |
| p_fused_Hall | 0.813 | [0.743, 0.874] | 0.546 | 360 |
| p_fused_Lcf | 0.873 | [0.819, 0.916] | 0.584 | 360 |
| cascade_llmformula | 0.660 | [0.538, 0.777] | 0.459 | 360 |
| l3_score_llmformula | 0.709 | [0.628, 0.792] | 0.396 | 360 |
| l3_score_local | 0.731 | [0.654, 0.803] | 0.409 | 360 |

Paired ΔAUROC (same bootstrap resamples): p_fused_H - l1_any: 0.227 [0.115, 0.328]; p_fused_H - n_smells: 0.227 [0.115, 0.328]; p_fused_H - l2_bow: 0.031 [-0.034, 0.097]; p_fused_H - l2_role: 0.173 [0.055, 0.281]; p_fused_H - l3_score: -0.045 [-0.121, 0.027]; l2_role - l2_bow: -0.142 [-0.238, -0.039]; l3_score - l2_bow: 0.076 [-0.007, 0.162]; p_fused_H - p_fused_Lcf: -0.140 [-0.232, -0.061]; p_fused_H - p_fused_Hall: -0.082 [-0.146, -0.026]

Separately bootstrapped `cascade_llmformula` on its 360-item subset (82 positives): l1_any=0.504, n_smells=0.504, l2_bow=0.701, l2_role=0.558, l3_score=0.776, p_fused_H=0.731, p_fused_Hall=0.813, p_fused_Lcf=0.873, cascade_llmformula=0.660; paired vs l3_score {'delta_mean': -0.1158, 'CI95': [-0.2132, -0.0225], 'P(delta<=0)': 0.9915}

Separately bootstrapped `l3_score_llmformula` on its 360-item subset (82 positives): l1_any=0.504, n_smells=0.504, l2_bow=0.701, l2_role=0.558, l3_score=0.776, p_fused_H=0.731, p_fused_Hall=0.813, p_fused_Lcf=0.873, l3_score_llmformula=0.709; paired vs l3_score {'delta_mean': -0.0667, 'CI95': [-0.1164, -0.0176], 'P(delta<=0)': 0.9955}

Separately bootstrapped `l3_score_local` on its 360-item subset (82 positives): l1_any=0.504, n_smells=0.504, l2_bow=0.701, l2_role=0.558, l3_score=0.776, p_fused_H=0.731, p_fused_Hall=0.813, p_fused_Lcf=0.873, l3_score_local=0.731; paired vs l3_score {'delta_mean': -0.0453, 'CI95': [-0.133, 0.0409], 'P(delta<=0)': 0.8385}

**track_H**: n=258, positives=57 (prevalence 0.221)

| score | AUROC | 95% CI | AUPRC | n scored |
|---|---|---|---|---|
| l1_any | 0.655 | [0.598, 0.716] | 0.450 | 258 |
| n_smells | 0.655 | [0.598, 0.716] | 0.451 | 258 |
| l2_bow | 0.721 | [0.646, 0.791] | 0.430 | 258 |
| l2_role | 0.520 | [0.480, 0.566] | 0.232 | 258 |
| l3_score | 0.704 | [0.626, 0.778] | 0.401 | 258 |
| p_fused_H_oof | 0.777 | [0.698, 0.847] | 0.636 | 258 |

Paired ΔAUROC (same bootstrap resamples): l2_role - l2_bow: -0.200 [-0.282, -0.117]; p_fused_H_oof - l2_bow: 0.057 [-0.009, 0.122]

### Binary layers at the operating thresholds (primary set)

| layer | TPR | FPR | precision | prec@10% | prec@25% | acc_eq (L, eps tuned on H) |
|---|---|---|---|---|---|---|
| l1_any | 0.020 | 0.004 | 0.800 | 0.383 | 0.651 | 0.513 |
| l2_bow_flag | 0.407 | 0.065 | 0.818 | 0.411 | 0.677 | 0.513 |
| l2_role_flag | 0.131 | 0.018 | 0.839 | 0.447 | 0.708 | 0.513 |
| l3_flag | 0.176 | 0.018 | 0.875 | 0.521 | 0.765 | 0.534 |
| fused_flag | 0.568 | 0.194 | 0.677 | 0.245 | 0.493 | 0.543 |
| l1_or_l2 | 0.518 | 0.083 | 0.818 | 0.410 | 0.676 | 0.605 |
| cascade_any | 0.553 | 0.097 | 0.803 | 0.387 | 0.655 | 0.513 |

### L3 field gate on HREF (known-correct gold)

Fields below 0.70 are excluded and fields from 0.70 to 0.85 are flagged.

| field | accuracy | n | Wilson 95% |
|---|---|---|---|
| mm_role | 0.913 | 655 | [0.889, 0.932] |
| mm_force | 0.690 | 799 | [0.657, 0.721] |
| mm_claims | 0.863 | 182 | [0.805, 0.905] |
| mm_order | 0.947 | 57 | [0.856, 0.982] |
| mm_exception | 0.000 | 1 | [0.000, 0.793] |
| missing_frac | 0.916 | 814 | [0.895, 0.934] |
| extra_frac | 0.919 | 765 | [0.897, 0.936] |

* Gated fields: ['mm_role', 'mm_claims', 'mm_order', 'missing_frac', 'extra_frac']. Flagged: []. Excluded: ['mm_force', 'mm_exception']. Alignment rate: 0.9062.
* L3 threshold (HREF p90): 1.000. Fused thresholds: no-leak 0.559, all-H 0.653.
* Fusion training set: {'pos': 57, 'neg': 495, 'noleak_pos': 43, 'noleak_neg': 303}.
* No-leak fusion coefficients (standardised features): {'intercept': -0.407, 'l1_any': 1.208, 'n_smells': -0.486, 'bow_uncarried': 0.534, 'bow_n_unanch': -0.057, 'role_count': 0.111, 'l3_score': 0.351, 'log_words': -0.02}.
* Test-retest: {'n': 60, 'field_agreement': {'concept_phrase_reproduced': 0.9967, 'role': 0.9934, 'negated': 1.0, 'exception': 1.0, 'force': 0.9443}, 'exact_json_identical': 0.9167}.
* Second model qwen/qwen3-30b-a3b-instruct-2507 on HREF (n answered=294): field accuracy {'mm_role': 0.9068, 'mm_force': 0.7339, 'missing_frac': 0.9111, 'extra_frac': 0.9111, 'mm_exception': 0.3333, 'mm_order': 0.9538, 'mm_claims': 0.8919}.
* Local outage model local/qwen2.5-1.5b-instruct-q4_k_m on HREF: field accuracy {'mm_role': 0.7603, 'mm_force': 0.677, 'missing_frac': 0.7998, 'extra_frac': 0.9059, 'mm_order': 1.0, 'mm_claims': 0.8887}.

### Invariance (share of rewrites flagged, and flip rate against the original, on CORRECT items)

| family | applies | L1 FA / flip | L2-bow FA / flip | L2-role FA / flip | L3 FA / flip | fused FA / flip |
|---|---|---|---|---|---|---|
| CONTRAPOSITIVE | 40/150 | 0.025 / 0.025 | 0.100 / 0.000 | 0.025 / 0.025 | 0.025 / 0.000 | 0.275 / 0.000 |
| DEMORGAN | 33/150 | 0.000 / 0.000 | 0.030 / 0.000 | 0.061 / 0.000 | 0.030 / 0.030 | 0.182 / 0.061 |
| PRENEX | 1/150 | 0.000 / 0.000 | 0.000 / 0.000 | 0.000 / 0.000 | 0.000 / 0.000 | 0.000 / 0.000 |
| RENAME | 150/150 | 0.000 / 0.000 | 0.180 / 0.093 | 0.013 / 0.000 | 0.033 / 0.007 | 0.220 / 0.013 |
| REORDER | 34/150 | 0.000 / 0.000 | 0.029 / 0.000 | 0.059 / 0.000 | 0.059 / 0.000 | 0.235 / 0.000 |

### L1 false alarms on track-L CORRECT items, by system (all lengths)

| system | n correct | FA | Wilson | n error | TPR | precision |
|---|---|---|---|---|---|---|
| gpt-3.5-turbo | 89 | 0.000 | [0.000, 0.041] | 54 | 0.000 | – |
| gpt-4 | 112 | 0.009 | [0.002, 0.049] | 65 | 0.000 | 0.000 |
| text-davinci-003 | 77 | 0.000 | [0.000, 0.048] | 80 | 0.050 | 1.000 |

Smells above 3% FA on some system's CORRECT items: none.

### Per-error-type sensitivity at the operating thresholds (track L: ERROR ∪ COMPOUND)

| operator | n | L1 | L2-bow | L2-role | L3 | fused | any layer of the cascade |
|---|---|---|---|---|---|---|---|
| NEG | 5 | 0.000 | 0.200 | 1.000 | 0.200 | 0.400 | 1.000 |
| QUANT | 2 | 0.000 | 0.000 | 0.500 | 0.000 | 0.500 | 0.500 |
| CONN | 4 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| DROP | 142 | 0.028 | 0.479 | 0.127 | 0.197 | 0.599 | 0.606 |
| ADD | 150 | 0.020 | 0.473 | 0.107 | 0.173 | 0.653 | 0.573 |
| SWAP | 12 | 0.000 | 0.000 | 0.083 | 0.250 | 0.083 | 0.333 |
| BIND | 8 | 0.125 | 0.000 | 0.125 | 0.000 | 0.375 | 0.250 |
| COMPOUND | 187 | 0.118 | 0.428 | 0.166 | 0.160 | 0.599 | 0.578 |

FA on track-L CORRECT: {'L1': 0.0036, 'L2_bow': 0.0647, 'L2_role': 0.018, 'L3': 0.018, 'fused': 0.1942}.

Error-type readout on depth-1 errors: P(error_code ∈ true ops | fired) = 0.3261 (n_fired=46/92).

### Complexity strata (primary set; UNTESTABLE = fewer than 50 errors or fewer than 50 correct)

| stratum | bin | n err | n cor | AUROC fused | AUROC L1 | AUROC L2-bow | AUROC L2-role | AUROC L3 | FA fused | untestable |
|---|---|---|---|---|---|---|---|---|---|---|
| len_bin | 12-19 | 18 | 13 | 0.521 | 0.489 | 0.596 | 0.556 | 0.541 | 0.385 | True |
| len_bin | <12 | 179 | 264 | 0.781 | 0.508 | 0.742 | 0.558 | 0.772 | 0.186 | False |
| len_bin | >=20 | 2 | 1 | 0.500 | 0.500 | 1.000 | 0.500 | 0.000 | 0.000 | True |
| n_quant | 0 | 130 | 172 | 0.743 | 0.511 | 0.728 | 0.536 | 0.771 | 0.180 | False |
| n_quant | 1 | 65 | 99 | 0.794 | 0.503 | 0.748 | 0.601 | 0.721 | 0.212 | False |
| n_quant | >=2 | 4 | 7 | 0.750 | 0.500 | 0.768 | 0.500 | 0.607 | 0.286 | True |
| depth | 2-3 | 73 | 100 | 0.756 | 0.502 | 0.717 | 0.603 | 0.710 | 0.240 | False |
| depth | <=1 | 124 | 172 | 0.762 | 0.512 | 0.745 | 0.530 | 0.779 | 0.174 | False |
| depth | >=4 | 2 | 6 | 0.667 | 0.500 | 0.750 | 0.500 | 0.500 | 0.000 | True |
| n_conditions | 0 | 145 | 199 | 0.775 | 0.514 | 0.759 | 0.543 | 0.791 | 0.171 | False |
| n_conditions | 1-2 | 54 | 77 | 0.716 | 0.493 | 0.677 | 0.593 | 0.628 | 0.260 | False |
| n_conditions | >=3 | 0 | 2 | – | – | – | – | – | 0.000 | True |
| exception | False | 199 | 278 | 0.759 | 0.508 | 0.737 | 0.557 | 0.756 | 0.194 | False |

### Coverage, cost, contamination, ablation, gates

* Coverage on track L: {'n': 753, 'status_counts': {'OK': 693, 'UNPARSEABLE': 60}, 'full_coverage_rate': 0.9203, 'parse_rate': 0.9203, 'L3_ok_rate': 0.9203, 'scored_by_fused_rate(any output incl. unparseable->p=1)': 1.0}. Parse rate by system: {'gpt-3.5-turbo': 0.8889, 'gpt-4': 0.9455, 'text-davinci-003': 0.9209}.
* Cost: {'L1_usd_per_item': 0.0, 'L2_usd_per_item': 0.0, 'L3_usd_per_item_mean(track L, text-shared across systems)': 0.0, 'L3_usd_per_1000_items(track L)': 0.0409, 'L3_usd_per_1000_calls(flash-lite, from cache records)': 0.1749, 'decomposed_judge_usd_per_1000_calls': 0.0693, 'total_spend_usd(all stages incl. ablations)': 0.2919, 'secs_cpu_p50': 0.035, 'secs_cpu_p95': 0.09, 'secs_l3_p50': 0.63, 'secs_l3_p95': 1.684}.
* Contamination, track-L l3_score AUROC with exact alignment, original vs nonce-disguised: {'n': 477, 'orig_exact_align': 0.7647, 'disguised': 0.7703, 'paired_orig_minus_disguised': {'delta_mean': -0.0051, 'CI95': [-0.0633, 0.0488], 'P(delta<=0)': 0.574}}.
* Contamination, HREF field accuracy with exact alignment: original {'mm_role': 0.9244, 'mm_force': 0.6886, 'missing_frac': 0.9079, 'extra_frac': 0.9163, 'mm_exception': 0.0, 'mm_order': 0.9474, 'mm_claims': 0.8603}; disguised {'mm_role': 0.8897, 'mm_force': 0.5874, 'missing_frac': 0.8401, 'extra_frac': 0.9058, 'mm_exception': 0.0, 'mm_order': 0.9661, 'mm_claims': 0.8364} (n=294).
* Decomposed judge, i.e. the LLM reading the formula, scored against exact z3 answers: {'L': {'predicate_covered': {'acc': 0.9941, 'n': 1180}, 'role(mono)': {'acc': 0.8591, 'n': 1121}, 'negated': {'acc': 0.965, 'n': 1173}, 'force': {'acc': 0.9539, 'n': 1171}, 'args': {'acc': 0.5762, 'n': 361}, 'claims_rand': {'acc': 0.721, 'n': 371}}, 'H': {'predicate_covered': {'acc': 0.996, 'n': 751}, 'role(mono)': {'acc': 0.8807, 'n': 679}, 'negated': {'acc': 0.9479, 'n': 748}, 'force': {'acc': 0.9626, 'n': 748}, 'claims_rand': {'acc': 0.8409, 'n': 191}, 'args': {'acc': 0.3643, 'n': 129}}, 'HREF': {'predicate_covered': {'acc': 0.9988, 'n': 805}, 'role(mono)': {'acc': 0.9062, 'n': 736}, 'negated': {'acc': 0.9391, 'n': 804}, 'force': {'acc': 0.9726, 'n': 804}, 'claims_rand': {'acc': 0.8574, 'n': 204}, 'args': {'acc': 0.4845, 'n': 161}}}.
* Per-system item AUROC: {'gpt-3.5-turbo': {'n': 143, 'n_error': 54, 'AUROC_p_fused_H': 0.6893, 'AUROC_l1_any': 0.5, 'AUROC_l2_bow': 0.6499, 'AUROC_l3_score': 0.7218}, 'gpt-4': {'n': 177, 'n_error': 65, 'AUROC_p_fused_H': 0.6999, 'AUROC_l1_any': 0.4955, 'AUROC_l2_bow': 0.7162, 'AUROC_l3_score': 0.7197}, 'text-davinci-003': {'n': 157, 'n_error': 80, 'AUROC_p_fused_H': 0.8567, 'AUROC_l1_any': 0.525, 'AUROC_l2_bow': 0.8112, 'AUROC_l3_score': 0.8173}}.
* System level (3 systems, descriptive): {'systems': {'gpt-3.5-turbo': {'error_rate(ERROR/(ERROR+CORRECT))': 0.3776, 'mean_p_fused_H(parseable)': 0.443, 'parse_rate': 0.8889}, 'gpt-4': {'error_rate(ERROR/(ERROR+CORRECT))': 0.3672, 'mean_p_fused_H(parseable)': 0.4516, 'parse_rate': 0.9455}, 'text-davinci-003': {'error_rate(ERROR/(ERROR+CORRECT))': 0.5096, 'mean_p_fused_H(parseable)': 0.5573, 'parse_rate': 0.9209}}, 'kendall_tau_error_rate_vs_mean_p': 0.3333, 'note': '3 systems: descriptive only, no power'}.
* Track H paired same-text AUROC (original vs corrected, comparable with iter-3's 0.59 for L2-bow): {'n_smells': {'auroc': 0.6491, 'n': 57}, 'l2_bow': {'auroc': 0.5965, 'n': 57}, 'l2_role': {'auroc': 0.5263, 'n': 57}, 'l3_score': {'auroc': 0.6053, 'n': 57}}.
* **Gates (fused, primary)**: {'AUROC>=0.65': {'value': 0.7589, 'pass': True}, 'coverage>=0.90': {'value': 0.9203, 'pass': True, 'note': 'full coverage = parse ok + all layers scored; unparseable outputs count as failures'}, 'rewrite_FA<=0.10_per_family': {'worst_family_FA': 0.275, 'worst_family_FA_on_originals': 0.275, 'pass': False, 'worst_family_flip_rate': 0.0606, 'note': 'as pre-registered: share of rewritten CORRECT items flagged; the originals are flagged at the same rate (fused FA on track-L CORRECT ~0.19 vs 0.10 calibrated on H), so the flip rate isolates rewrite sensitivity'}, 'cost<=0.002/item': {'value': 0.0002, 'pass': True}, 'dAUROC_over_disguised_judge': 'computed in iteration 2 by joining experiment D on item_id (not in this artifact)'}.
