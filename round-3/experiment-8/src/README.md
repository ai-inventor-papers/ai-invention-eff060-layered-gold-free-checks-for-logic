# Rename-invariant consensus (PEER_HYB) and per-error-type sensitivity of gold-free NL→FOL metrics

Iteration 3, tasks T3 + T5 of the AI-Inventor run `run_u75jRHUss0zo`. Workspace (all paths below are relative to it):
`/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8`

**What was tested.** Iteration 2 left one held-out survivor: cross-family solver consensus
(`c_score_align`: share of other model families' formalisations of the same sentence that are z3-equivalent to the
candidate *after name-similarity alignment*). It fails the user's rename-invariance requirement. This artifact:

* **Part A** builds **PEER_HYB**: a candidate agrees with a peer if the name-similarity ALIGN map **OR** the exp-5
  name-free NF-anchored map yields a z3-verified equivalence (`c_score_hyb`, `g_score_hyb`). It measures rename false
  alarms on three separate rename sources and over-alignment three ways. It then applies a rule, frozen before any label
  join (`results/prereg_hyb.json`, sha256 in `prereg_hyb.sha256`), to choose between HYB and NF-anchored.
* **Part B** scores **every available metric** on the synthetic PERTURB suite: 4,234 typed mutants, 868 z3-equivalent
  controls and 300 unmutated bases. It reports recall at a frozen FA = 0.10 threshold, within-base AUROC and the
  DOWN-vs-UP polarity test per operator. It never pools PERTURB with real-error AUROC
  (`results/prereg_perturb.json`, frozen before any PERTURB statistic).
* **Part C** asks whether a gold-free minimal typed repair against the peer medoid identifies the error type.
* **Part D** ships `src/consensus_lib.py`: reusable `(text, fol, peers)` functions with docstrings and unit tests.

All scores are oriented **higher = more likely ERROR**. The full tables are in `results/tables.md`, generated from
the JSON/CSV files, with no hand-typed numbers.

---

## Headline verdicts

1. **Selection (pre-registered): NEITHER HYB NOR NF-ANCHORED IS ELIGIBLE, so nothing is frozen and the sibling's
   R_COMP read uses ALIGN.** Both pass the exp-D rename source (FA 0.050 HYB, 0.030 NF). Both fail the PERTURB rename
   controls at the screen-derived thresholds: HYB 0.841 (RENAME_SYN) and 0.700 (RENAME_NONCE); NF 0.686 and 0.485.
   *Why (post hoc, does not change the verdict):* on long E sentences the unmutated reference itself is often not
   endorsed by the peers. For NF, the rename FA **equals** the base FA and the flip rate is **0.000**: NF-anchored
   keeps 100% of the base's endorsers under nonce and synonym renames (`results/sanity_checks.json`). NF is therefore
   perfectly rename-invariant, and the FA > 0.10 is a threshold-transfer and reference-endorsement effect. HYB has a
   real rename flip rate of 0.15–0.16, because it keeps only 74% (nonce) and 75% (synonym) of the base's endorsers: the
   agreements that only ALIGN supplied are lost. ALIGN keeps 0% (nonce) and 33% (synonym). Every mode keeps ≥ 99% under
   the z3-equivalent controls (sanity check passed). Post hoc, at the E-derived thresholds (`invariance_table.csv`,
   threshold `primary_E`), rename FA on RENAME_SYN / RENAME_NONCE is ALIGN 0.564 / 0.764, HYB 0.298 / 0.215 and
   NF 0.201 / 0.132, against unrenamed-base FAs of 0.200, 0.196 and 0.162. Only NF's excess over its base FA is ~0.
2. **Discrimination on real errors (E, R_AB, stratified AUROC, sentence-cluster CI):** HYB 0.738 [0.702, 0.771],
   ALIGN 0.741 [0.705, 0.775], NF 0.686 [0.647, 0.720]. **HYB − ALIGN = −0.004 [−0.011, 0.004]**, so the "within 0.01"
   target is met. HYB − NF = +0.052 [0.030, 0.073]. HYB − local Qwen3-8B judge (exp 5 bf16 column) = +0.060
   [0.018, 0.100]. HYB − flash-lite judge is untestable on E: the frozen column has only 20 R_AB rows. On L25
   (≥ 25 words) HYB loses a little: −0.014 [−0.028, −0.001]. On sentences with 30+ words: −0.019 [−0.036, −0.006].
   On R_A (tier A, L20+EXC): HYB 0.849 vs ALIGN 0.855. Placebo (labels shuffled within stratum): 0.516.
3. **Over-alignment is real and quantified on real outputs.** The 686 candidate–peer pairs that HYB adds on top of
   ALIGN are label-discordant (one side CORRECT, the other ERROR) at **0.388**, against 0.127 for ALIGN-agreeing pairs
   and 0.406 for disagreeing pairs. HYB's extra agreements are therefore about as uninformative as disagreements. On
   PERTURB MEANING_RENAME (a wrong predicate in the right place), recall at the screen threshold is ALIGN 0.997,
   HYB 0.27 and NF 0.60. The screen MEANING_RENAME probe recall is 0.99, 0.25 and 0.20 respectively.
4. **Per-error-type sensitivity (PERTURB, E bases, within-base AUROC mutants vs same-base controls):**
   equivalence consensus is flat across operators (ALIGN 0.84–0.88, HYB 0.84–0.91, NF 0.79–0.86) except MEANING_RENAME.
   There, NF = 0.50, meaning it is blind to meaning renames by construction, and HYB = 0.68. Surface/text metrics are
   operator-specific: L2-bow ≈ 0.50 on NEG/QUANT/REV/SWAP but 0.96–0.99 on DROP/ADD/MEANING_RENAME, because it
   detects vocabulary changes only. The disguised flash-lite judge is weak on every operator (0.56–0.72). The pilot
   structural metrics are at chance (≈ 0.50) except joint-conflict on RESTR (0.87) and NEG (0.59).
   See T8/T9 in `results/tables.md` and `results/figures/fig_wbauroc_heatmap.png`.
5. **Polarity (pre-registered prediction CONFIRMED):** equivalence consensus is polarity-symmetric: DOWN − UP recall is
   ALIGN 0.000, HYB −0.007 [−0.017, 0.001], NF −0.004, all inside ±0.05. The text/role metrics miss restrictor-side
   (DOWN) edits more often: l3_z3 −0.126 [−0.148, −0.103], p_text −0.059 [−0.076, −0.041], flash-lite judge
   −0.028 [−0.040, −0.016]; pilot joint-conflict −0.070.
6. **Error-type identification (Part C):** minimal typed repair against the ALIGN peer medoid identifies the PERTURB
   operator with strict accuracy 0.328 [0.277, 0.387]. This beats the majority class (0.177) and chance (0.116), but a
   repair is found for only 44% of mutants. The oracle, which repairs against the true reference, reaches 0.802, so the
   ceiling is set by the medoid, not the typer. The flash-lite judge's type label scores 0.326 and is concentrated on
   ADD/NEG. MEANING_RENAME is uncodable by every typer. On the 500-mutant fallback sample (plan fallback 10, triggered
   because 52% of medoid searches ended without a repair), doubling the search budget to 20 s leaves accuracy unchanged
   (0.328 → 0.328; no-repair share 0.54 → 0.51). The medoid failures are therefore genuine multi-edit differences between
   the peer medoid and the reference, not search timeouts (`results/typing_s20.json`). Typing is above chance but weak,
   and it is limited by how far the peer medoid is from the truth.
7. **Every baseline on the same PERTURB rows (all 27 metrics).** Pooled within-base AUROC over all E-base mutants (the
   subset of 3,419 rows where every metric exists): PEER+TEXT fusion 0.948, ALIGN consensus 0.866, HYB 0.847, TEXT-only
   0.845, L3 0.816, NF 0.785, S4_local 0.753, round-trip NLI-min 0.749, flash-lite judge (disguised) 0.680, SC-5 local
   0.666, L2-bow 0.659, local Llama-3.1-8B judge 0.653, local Qwen3-8B judge 0.643, pilot metrics 0.50–0.54.
   The local judges and the embedding round trip miss restrictor-side (DOWN) edits: DOWN−UP is Qwen −0.154, Llama
   −0.144 and embedding cosine −0.124, all CIs below 0. These are synthetic sensitivity profiles, NOT real-error
   detection (foreign vocabulary in ADD_FOREIGN/MEANING_RENAME makes lexical metrics look strong). Real-error numbers
   are the E rows above.

---

## Layout

| path | what |
|---|---|
| `method.py` | orchestrator: `run` executes every stage (resumable, frozen files never overwritten); `output` builds `method_out.json` |
| `method_out.json` (+ `full_/mini_/preview_`) | exp_gen_sol_out: E rows, PERTURB rows (every Part B metric as `predict_*`), exp D rewrites, screen items/probes |
| `src/pairs.py` | **pair engine**: `pair_verdicts` (align_eq / nf_eq / hyb_eq), leave-one-family-out c/g scores, medoids |
| `src/consensus_lib.py` | **library** (Part D): `consensus_score`, `graded_consensus`, `name_free_align`, `peer_pool`, `equivalent_modulo_vocab`, `minimal_typed_repair` |
| `src/peer_text.py`, `src/vendor_*/`, `vendor_e6/` | vendored exp 5 / exp C / exp D / dataset E / exp 6 code (sha1s in `logs/vendor_manifest.json`) |
| `src/tasks.py`, `src/run_scoring.py`, `src/gate_check.py` | label-free task builders, scoring driver, regression gate |
| `src/freeze_prereg_hyb.py`, `src/analyse_hyb.py` | Part A freeze + analysis (selection, E AUROCs, invariance, audit, complexity) |
| `src/prep_calib.py`, `src/run_api_perturb.py`, `src/perturb_cpu.py`, `src/perturb_gpu.py`, `src/fit_s4_perturb.py` | Part B scorers |
| `src/freeze_prereg_perturb.py`, `src/analyse_perturb.py` | Part B freeze + analysis |
| `src/typing_perturb.py`, `src/typing_fallback20.py` | Part C |
| `src/sanity_checks.py`, `src/make_figures.py`, `src/write_tables.py`, `src/write_deviations_iter3.py` | sanity signals, figures, tables, deviations |
| `reproducibility.md` | exact commands, versions, hardware and expected numbers |
| `tests/audit_raw.py` → `results/audit_raw.json` | independent re-derivation from RAW score files with its own AUROC code + label-permutation placebos (all headline numbers match; placebos ~0.5) |
| `tests/` | `test_consensus_lib.py` (20+ known pairs × modes, mocked + live `peer_pool`), `test_threshold.py`, `test_isolation.py`, `audit_rederive.py` |
| `results/prereg_hyb.json`, `results/prereg_perturb.json` (+ `.sha256`) | the two freezes |
| `results/selection.json` | selection evidence + verdict |
| `results/scores_E.jsonl`, `results/scores_screen.jsonl` | per-sentence pair-engine output (c/g for align, nf, hyb; medoids) |
| `results/pairs_E.jsonl` | pair-level verdicts (sentence_id, cand row_key, peer row_key, align_eq, nf_eq, hyb_eq, nf_cost); joinable by T4 / iteration 4 |
| `results/per_item_hyb_E.jsonl`, `results/per_item_screen_hyb.jsonl` | per-row consensus scores + labels |
| `results/perturb_scores.jsonl` | every PERTURB row × every metric (+ status, operator, polarity, pair id, base status, endorsement) |
| `results/perturb_sensitivity.csv`, `perturb_downup.csv`, `perturb_breakdowns.csv`, `invariance_table.csv`, `invariance_table_consensus.csv`, `tradeoff.csv`, `coverage_perturb.csv` | Part B tables |
| `results/typing.csv`, `typing_confusion.csv`, `analysis_typing.json`, `typing_s20.json` | Part C |
| `results/analysis_hyb.json`, `analysis_perturb.json`, `tables.md`, `figures/` | analyses, tables, figures (+ JSON figure specs) |
| `results/deviations.json`, `results/sanity_checks.json`, `results/audit_rederive.json`, `results/regression_gate.json` | deviations, sanity (endorser retention under each control type), independent re-derivation (all_pass = true), regression gate |
| `results/quant_shift.json`, `results/thresholds_gpu.json`, `results/s4_perturb_coefs.json` | nf4-vs-bf16 shift, GPU-metric thresholds, S4_local coefficients |
| `results/typing_rows.jsonl`, `results/typing_rows_s20.jsonl`, `results/typing_per_row.jsonl` | raw repair searches (10 s; 20 s fallback sample) and per-mutant typing |
| `results/perturb_scores/*.jsonl` | raw metric outputs (flash-lite judge, nf4 local judges, round trip, CPU metrics) |
| `results/costs.jsonl`, `results/cost_ledger.jsonl`, `results/llm_cache.jsonl`, `results/local_cache.jsonl` | API cost ledger and caches |
| `data/` | copied read-only inputs: `exp5/` (E blind view, labels, frozen columns, prereg), `screen/`, `perturb_rows.jsonl` (dataset 3's perturb_suite, flattened), `E_calib_units.jsonl`, `prompts/fewshot_v1.txt`, `nltk_data/` |

## How to run

```bash
./restore.sh                                  # venv (uv), NLTK data, model weights
.venv/bin/python method.py run                # every stage in order (resumable; freezes are never overwritten)
.venv/bin/python method.py output             # method_out.json only
.venv/bin/python -m pytest -c pytest.ini tests   # unit tests (AII_LIVE=1 adds one live peer_pool call, < $0.002)
.venv/bin/python tests/audit_rederive.py      # independent re-derivation of headline numbers
```

Library use:
```python
import sys; sys.path.insert(0, "src")
import consensus_lib as CL
CL.consensus_score("All dogs bark.", "∀x (Dog(x) → Bark(x))", peers, mode="align")   # modes: exact | align | nf | hyb
CL.graded_consensus(text, fol, peers, mode="align")
CL.peer_pool(text, families=["G1", "G9"], dry_run=True)   # cost estimate; dry_run=False calls OpenRouter
```
Based on these results, use **`mode="align"`** when names are meaningful. Use **`mode="nf"`** when rename invariance is
required: it has 0 rename flips, but it is blind to MEANING_RENAME and loses 0.055 E AUROC. `hyb` is not recommended:
it inherits ALIGN's rename flips at a reduced rate and adds label-discordant agreements.

## Methods in brief

* **Peers.** For each E sentence: every parseable real LLM output (10 slots, 9 families), leave-one-family-out for E rows
  (exp 5 vendor family map; the MALLS gold and ccg2lambda are never peers). PERTURB rows of the 200 E bases are scored
  against all peers. The 100 R_COMP bases have no peers yet (`rcomp_candidates.jsonl` absent), so consensus is NA there.
* **Regression gate (passed).** Re-derived `c_align` equals the frozen `c_score_align` on 99.81% of 8,507 E rows, and
  `c_nf` equals `nf_c_score` on 99.91%. Screen `c_align` track-L AUROC is 0.870 against exp C's 0.866 ± 0.005.
* **Thresholds.** Matched FA = 0.10 with **fractional tie-breaking**: at the tie level t, rows with score = t are
  flagged with weight λ. Part A thresholds come from the screen (AGREE-set track-L CORRECT). Part B PRIMARY thresholds
  come from E R_AB LLM CORRECT rows. For nf4 local models and flash-lite, they come from 864 E CORRECT calibration rows
  scored here. On E, every consensus threshold sits at c = 1.0, i.e. "no peer agrees", so PERTURB consensus recall is
  bounded by λ (0.52–0.85). **Use within-base AUROC for cross-metric comparison.**
* **Invariance.** FA = share of rewritten CORRECT items flagged. `flip_rate` = |flag(rewrite) − flag(base)| under a
  coupled tie draw, reported in a separate column and never used in the rule.
* **Statistics.** Stratified AUROC (strata CTRL/EXC/L20/L25) with a sentence-cluster bootstrap on E; base-cluster
  bootstrap on PERTURB (B = 2000, seed 0).

## GPU arm (nf4 local judges, round trip, S4_local)

* Local Qwen3-8B JSON judge and Llama-3.1-8B P(YES) judge, both on disguised text (dataset 3's per-sentence bijection).
  Also a Qwen3-8B verbaliser followed by DeBERTa-v3-large NLI both ways and an mpnet cosine (round trip). All ran on
  6,666 units (5,402 PERTURB + 1,264 E calibration) with **0 failures** and full coverage. Wall time: judge 66 min,
  Llama 20 min, verbaliser 37 min, NLI 3 min on an RTX 2000 Ada 16 GB.
* **Quantisation cost** (`results/quant_shift.json`, the same 1,264 E rows): E AUROC with nf4 vs bf16 is Qwen judge
  0.664 vs 0.699 and Llama judge 0.623 vs 0.639 (Spearman nf4~bf16 0.86 / 0.82). Round-trip NLI-min is 0.626 vs 0.610
  (different verbaliser outputs). The flash-lite disguised judge scores 0.680 on the same rows.
* **S4_local** (full-E fit, bf16 features, applied to nf4 PERTURB inputs): its E threshold transfers badly (FA on PERTURB
  controls 0.50; the base FA is 0.22). Its within-base AUROC is 0.753 overall and 0.58–0.86 per operator. Use the
  in-sample secondary threshold column (`recall_secondary_insample`) for S4 comparisons.
* Judge thresholds on the E calibration rows: Qwen at t = 0.20 (faithful_prob ≤ 0.8 flags), Llama at t = 0.94. Both
  are in `results/thresholds_gpu.json`.

## Deviations (full list: `results/deviations.json`)

* **Machine migration mid-run.** `.venv` and the HF cache were wiped, and the GPU changed from 21 GB to 16 GB. The 8B
  local judges and the verbaliser run **nf4**, and their thresholds are refit on nf4 E calibration rows.
* flash-lite E threshold from 864 EC CORRECT rows scored here, because the frozen E flash-lite column covers too few rows.
* S4_local is one full-E fit (plan-declared), without pilot_rerun_jacc or *_orig judges.
* Local judges are run on disguised text only (plan). L3 is NA on R_COMP rows (no cached questionnaires).
* Typing: the peer medoid is the ALIGN medoid because no variant was frozen. Fallback (10) was triggered (52% of
  medoid searches timed out), so there is a 20 s budget on a 500-mutant sample.
* `transformers/__init__.py` in `.venv` was patched to read a cached file list instead of an import-time `rglob`, which
  took more than 10 min on this network filesystem. `restore.sh` re-applies it.
* A 1-in-20 flash-lite JSON parse failure appeared in the pilot, and 197/6,666 (3.0%) overall. The plan's pilot bar was
  < 2%. Failures are scored 1.0 and counted in coverage.

## Costs

OpenRouter: flash-lite PERTURB + calibration judge **$0.351** (6,666 calls), plus the live `peer_pool` smoke call
(< $0.002). Total < $0.36 of the $2 cap; ledger in `results/costs.jsonl` and `results/cost_ledger.jsonl`. CPU: pair
engine ~0.16 CPU-s per E row; typed repair ≤ 10 s per search. GPU: about 2.1 h on an RTX 2000 Ada (see the GPU arm);
equivalent to $0.26/h × 2.1 h ≈ $0.55 at the RunPod on-demand price used by exp 6.

## Restoring removed files

The `.aii/manifest.yaml` `delete` entries and how to get them back:

| path | restore |
|---|---|
| `.venv/` | `uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r requirements.txt`, plus the transformers patch (both in `./restore.sh`) |
| `cache/pair_cache.sqlite` | `.venv/bin/python src/run_scoring.py E --stage all && .venv/bin/python src/run_scoring.py screen --stage all` (rebuilds the pair cache; scores are already in `results/`) |
| `data/nltk_data/` (kept in place; only if missing) | `.venv/bin/python -c "import nltk; [nltk.download(x, download_dir='data/nltk_data') for x in ('wordnet','omw-1.4','words')]"` |
| model weights (shared HF cache, not in this workspace) | `scripts/download_models.sh` (Qwen/Qwen3-8B, meta-llama/Llama-3.1-8B-Instruct, MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli, cross-encoder/nli-deberta-v3-large, sentence-transformers/all-mpnet-base-v2) |
| `**/__pycache__/` (src, src/vendor_*, vendor_e6/src, vendor_e6/src/labeller, tests) | recreated automatically on first import, or `.venv/bin/python -m compileall src vendor_e6/src tests` |
