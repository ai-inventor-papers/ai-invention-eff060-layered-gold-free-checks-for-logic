# Screening fixes for model-agreement false alarms (iteration 5 FREEZE, dataset E)

AI-Inventor run `run_u75jRHUss0zo`, iteration 5, `gen_art_experiment_14` (plan `gen_plan_experiment_4_idx4`).
Workspace, and the location of every kept artifact:
`/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_14`

**Everything here is computed on dataset E, which is DEVELOPMENT data.** Its labels were seen in iterations 2–4. The
numbers below screen candidates; they confirm nothing. E2 / R_COMP FREE does the confirming.
Total OpenRouter spend of this artifact: **$0.219** (own hard cap $2.00; `cost_ledger.jsonl`).

## What was done

**Part A (H-IMPROVE, $0, CPU).** The consensus metric scores a candidate FOL translation by how many translations from
other model families agree with it. The iteration-4 diagnosis was that wrong peers scatter and dilute a correct
candidate's support. Part A tests five label-free rescorings aimed at that diagnosis against the frozen incumbent
**V0 = `c_score_align`**:

| id | rescoring |
|---|---|
| V1 | plurality-normalised: 1 − min(1, share of agreeing peers / share of the largest peer class) |
| V2 | reliability-weighted: label-free family weights (cross-family agreement rate, shrunk, out of fold) |
| V3 | V1 + V2 |
| V4 | cross-fitted logistic on the two channels (c_exact, c_align) |
| V5 | V3 on the cost-matched 3-family pool (deepseek, microsoft, openai) |

The only scoring input is eval-2's label-free pairwise equivalence matrix (29,107 node pairs). The steps ran in this
order, and the selection rule was applied mechanically:

1. Wrote `prereg_improve.json`.
2. Scored all variants.
3. Sealed the scores (sha256 in `prereg_improve_addendum.json`).
4. Joined the labels (and cross-fitted V4).

**Part B (H-RENAME, $0.22).** **GG (gloss-gated name-free agreement)** replaces the name-similarity aligner. Two
formulas agree if either:

- they are exactly z3-equivalent, or
- an exhaustive injective, arity-consistent map between their symbols makes them z3-equivalent, **and** a
  gemini-2.5-flash gloss check accepts every renamed symbol pair (e.g. "Loves/2 vs Adores/2 in this sentence").

There is no peer cueing and no name similarity. Before the sweep, the checker was gated on known-answer items. GG was
then scored on the PERTURB E-base rename items and on E.

**Part C.** A vendored library with a provenance manifest: every earlier reusable function behind one API, plus a
smoke test.

## Headline results

### Marker M1: `freeze/CONSENSUS_FREEZE_READY.json`

| part | status |
|---|---|
| V | **FROZEN**, winner **"NONE: V0 stands"** (written 12 min after the first line of code) |
| GG | **FAIL(g3)** |

### Part A: population Z = 2,672 R_AB rows

Z has 1,810 ERROR and 862 CORRECT rows from 283 sentences; each row has at least 2 cross-family peers. CIs come from a
sentence-cluster bootstrap (B = 2000).

| score | ALL-strat AUROC | LONG-strat (L25+L20+EXC) | Δ LONG vs V0 [CI] | L25 | CTRL |
|---|---|---|---|---|---|
| V0 c_score_align (frozen) | 0.742 | 0.743 | – | 0.713 | 0.738 |
| V1 plurality-normalised | 0.729 | 0.739 | −0.004 [−0.014, 0.010] | 0.704 | 0.628 |
| V2 reliability-weighted | 0.752 | 0.750 | **+0.0075 [0.004, 0.011]** | 0.718 | 0.773 |
| V3 = V1 + V2 | 0.737 | 0.750 | +0.007 [−0.004, 0.020] | 0.714 | 0.613 |
| V4 two-channel logistic | 0.758 | 0.751 | +0.009 [−0.004, 0.021] | 0.719 | 0.826 |
| V5 = V3 on 3-pool | 0.735 | 0.746 | +0.003 [−0.021, 0.027] | 0.694 | 0.629 |
| c_exact (aligner-free) | 0.689 | 0.672 | −0.070 [−0.103, −0.038] | 0.611 | 0.857 |

**Decision: NONE qualifies. V0 stands.** The rule needs Δ LONG ≥ +0.015, L25 ≥ V0 and CTRL ≥ V0 − 0.01. The best
variant is V4 at +0.0088.

- **Stability** (500 within-stratum sentence resamples): NONE is selected 87.6% of the time, V4 11.8%.
- **Permutation null** (200 label permutations): some variant qualifies by chance 3.5% of the time.
- **V2** is a small but consistent gain whose CI excludes 0 (ALL-strat +0.010 [0.006, 0.016]). It is far below the
  pre-registered margin, and its d is essentially V0's.

**Why the scatter-targeted rescorings do not help.** Take plurality normalisation (V1, T5/T5b in `tables.md`):

- On long sentences it cuts d (the share of CORRECT candidates flagged) sharply: ALL 0.490 → 0.174, words-T3
  0.913 → 0.513.
- It raises e (the share of ERROR candidates endorsed) just as much: ALL 0.140 → 0.343.
- On MEANING_RENAME-type errors, e rises from 0.502 to 0.872.

Wrong candidates also sit in the plurality of a scattered pool, so the rescoring trades d for e. **No variant lowers d
without raising e** on T3, L25, LONG or ALL. V1/V3/V5 halve the length degradation (NET Δ(e+d) T3 − T1: V0 +0.401, V1
+0.205) only through this trade. The eval-3 oracle diagnostic is ILL_CONDITIONED for the 9-family pool: its oracle d
(0.586) exceeds V0's d (0.490). For the 3-pool, V5 pushes d below the no-anchoring oracle floor (0.230 < 0.385) and pays
with e 0.246.

### Part B: GG

**Checker gates.**

- **G-A** (840 dataset-5 items): dev half with prompt v1 scored 0.780, which failed. The single allowed revision (v2)
  scored **0.907** on the confirm half: pass.
- **G-B** (symbol pairs from R_COMP-base renames): 0.950 dev / 0.941 confirm. It is NOT_TESTABLE as a gate because it
  has only 53 YES pairs, below the pre-registered 60.
- The checker never reasoned (0 reasoning tokens) and returned 0 unparseable answers.

**Dev gates.**

| gate | value | pass |
|---|---|---|
| g1 RENAME_SYN paired flip | 0.034 (FA 0.932 vs paired-base FA 0.898) | yes (trivially: bases are already flagged) |
| g2 MEANING_RENAME recall | 1.000 vs c_align 1.000; base FA 0.83 vs 0.71 | yes (trivially) |
| g3 E ALL-strat AUROC | **0.696 vs V0 0.742, Δ −0.046 [−0.071, −0.021]** | **no** |
| RENAME_NONCE (expected failure, not gated) | FA 1.000, flip 0.227 | – |

**What GG does.**

- It **halves error endorsement**: e 0.140 → 0.081. On MEANING_RENAME-type errors, e falls 0.502 → 0.224; the
  aligner-free exact score gets 0.009.
- It **raises d**: 0.490 → 0.629. Of the 946 node pairs that eqmv accepts and GG does not:
  - all 678 `gran` pairs fail the arity prefilter, because granularity differences cannot be bridged by a symbol
    bijection;
  - 268 `align` pairs are gloss-rejected.
- GG accepts 104 pairs that eqmv rejects.
- Rename non-invariance of consensus therefore stays a measured boundary. The boundary statement is in
  `freeze/gg_gate.json`.

**Cost.**

- Gloss: $0.163 for 3,481 unique symbol pairs (415 calls, $0.00039 per call).
- FULL cost per E candidate: 0.038 CPU-s and ≤ $0.00005 of gloss, on top of the shared peer generation
  ($0.0022 per sentence).

**Secondary GG_B.** GG_B adds dataset-5's freelab bridges (B1 reification, B2 de-reification, B3 merge, B4 split,
B5 lexical negation) on the 11,202 E pairs that PRIMARY GG rejects.

- The CPU search mapped 3,133 pairs (170 capped). 53 pairs were stopped at the wall deadline and count as not agreeing
  (D12).
- **The gloss for those maps could not run.** The run-level OpenRouter budget ($12, shared by every artifact of the run)
  was exhausted, and every call returned HTTP 403 `aii_run_budget_exhausted` (D13). So GG_B is **UNTESTED(budget)** and
  only its $0 brackets are reported.
- In the upper bracket (every bridged map accepted), ALL-strat AUROC is **0.653**, *below* GG (0.696) and V0 (0.742).
  e rises to 0.334 (ADD 0.367, MEANING_RENAME-type 0.689) while d falls to 0.358.
- The bridges absorb real ADD/DROP errors: a B3 merge can map one symbol onto a conjunction. Any gain from GG_B would
  therefore have to come entirely from the gloss rejecting those maps.
- Per row, GG_B's scores lie between c_gg and c_ggb_allyes, and so do its e and d at c > 0.5. Its AUROC is not bounded
  by the brackets. See `tables.md` T13 and `results/ggb_dev.json`.

## Layout

| path | what |
|---|---|
| `method.py` | orchestrator: runs every stage in the pre-registered order under PYTHONHASHSEED=0 (idempotent; `--stage A,B,GGB,C,OUT,TEST`) |
| `reproducibility.md` | environment, seeds, commands, runtimes, spend, expected numbers |
| `freeze/CONSENSUS_FREEZE_READY.json` | **marker M1** (token `aii_iter5_consensus_freeze_v1`): V FROZEN (winner, sha256s), GG status + sha256s |
| `freeze/selection.json` | IMMUTABLE Part-A decision: rule, per-variant E numbers (AUROC + CI, Δ + CI, e/d), V4 coefficients, V2 recipe + full-E weights, V5 families, stability, null, sha256s |
| `freeze/consensus_variants.py` | IMMUTABLE pure functions: build_index, peers_lofo, c_score_align (reproduction only), c_exact, c_pn (V1), family_weights, c_rw (V2), c_pn_rw (V3), c_two_channel (V4), c_v5 |
| `freeze/gg.py`, `freeze/gg_fol.py` | GG: gg_map_search, gg_agree, consensus_score_gg, gloss prompt v1 and parser (`gg_fol.py` = dataset-5 `vendor/fol.py`, verbatim) |
| `freeze/gg_gate.json` | GG status FAIL(g3), all gates, checker model + prompt sha, caps, boundary statement |
| `prereg_improve.json` (+ `.sha256`, `_addendum.json`, `_addendum_v4.json`) | Part-A pre-registration and the score seals written before the label join |
| `prereg_gg.json` (+ `.sha256`), `prompt_revision_v2.json` | Part-B pre-registration (definition, family, caps, checker, prompts, gates) and the one prompt revision |
| `src/step0_gates.py` | STEP 0: population asserts, gate G0 with exp-6's own estimator |
| `src/make_row_index.py`, `src/score_variants.py` | label-stripped row index; LABEL-FREE scorer (allowed-inputs hashed) + gate G1 + seal |
| `src/fit_v4.py` | V4 cross-fit (label-using by construction, after the seal) |
| `src/screen.py`, `src/select_rule.py`, `src/freeze_part_a.py` | label join, AUROC/Δ/e-d/T9/oracle tables; mechanical rule + stability + null; freeze + M1 |
| `src/prereg_gg.py`, `src/gg_search.py`, `src/gg_gates.py`, `src/gloss_client.py`, `src/gg_gloss.py`, `src/gg_score.py`, `src/freeze_part_b.py` | GG pipeline: prereg, CPU map search, checker gates, async OpenRouter client (cache, ledger, $2 hard stop), gloss sweep, scores + dev gates, M1 update |
| `src/ggb_search.py`, `src/ggb_score.py` | SECONDARY GG_B (freelab family with B1–B5 bridges) |
| `src/labels.py`, `src/stats.py`, `src/common.py` | T9 classes (exp-9 verbatim) + op_class; exp-6 / eval-2 statistics (verbatim); paths |
| `src/make_outputs.py`, `src/make_tables.py`, `src/copy_inputs.py`, `src/vendor_lib.py`, `src/probe.py` | outputs, tables, input copy + manifest, library vendoring, API probe |
| `lib/api.py`, `lib/vendor/`, `lib/PROVENANCE.json`, `lib/INVENTORY.csv` | Part C: one API over every reusable function; vendored byte-identical code with source path + sha256 |
| `tests/` | `test_variants.py` (toy matrices, fold discipline, 20-row reproduction to 1e-9), `test_gg.py`, `test_budget.py`, `smoke_lib.py` (10 E rows through lib/api.py), `audit_rederive.py` (independent re-derivation + placebo) |
| `results/` | scores (`scores_E_variants.jsonl`, `scores_E_V4.jsonl`, `scores_gg_E.jsonl`, `scores_gg_perturb.jsonl`, `scores_ggb_E.jsonl`), `screen_E.json`, `selection_E.json`, `gg_dev.json`, `ggb_dev.json`, gates, `gg_search.jsonl` / `ggb_search.jsonl` (per-pair maps), `gloss_cache.jsonl` (paid verdicts), `audit_rederive.json`, `smoke_lib.json` |
| `tables.md`, `tables/*.csv` | every table with a `# source:` line (file + function) |
| `method_out.json` (+ `full_/mini_/preview_`) | exp_gen_sol_out: `E_heldout` (8,507 rows, predict_V0…V5, c_exact, gg, gg_allyes, gg_b_allyes, frozen context), `PERTURB_E_bases` (722), `GG_checker_gates` (1,069) |
| `deviations.json` | D1–D11 |
| `cost_ledger.jsonl` | every OpenRouter call (ts, model, tokens, reasoning tokens, usd, cumulative) |
| `inputs_copy/`, `inputs_manifest.json` | copies of every small input read (sha256); large inputs referenced by path + sha256 |

## How to run

`.venv/bin/python method.py` runs everything (idempotent). The same steps by hand:

```bash
uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml
export PYTHONHASHSEED=0; cd src
../.venv/bin/python copy_inputs.py && ../.venv/bin/python step0_gates.py          # G0
../.venv/bin/python make_row_index.py && ../.venv/bin/python score_variants.py     # label-free scores + G1 + seal
../.venv/bin/python fit_v4.py && ../.venv/bin/python screen.py && ../.venv/bin/python select_rule.py
../.venv/bin/python freeze_part_a.py        # refuses if freeze/selection.json exists (immutable)
../.venv/bin/python gg_search.py all        # ~30 s on 6 workers
../.venv/bin/python gg_gates.py dev v1 && ../.venv/bin/python gg_gates.py confirm v2   # cached verdicts: $0 on re-run
../.venv/bin/python gg_gloss.py && ../.venv/bin/python gg_score.py && ../.venv/bin/python freeze_part_b.py
../.venv/bin/python ggb_search.py all && ../.venv/bin/python ggb_score.py           # secondary
../.venv/bin/python make_outputs.py && ../.venv/bin/python make_tables.py
cd .. && .venv/bin/python -m pytest -q tests/test_variants.py tests/test_gg.py tests/test_budget.py
.venv/bin/python tests/audit_rederive.py && PYTHONHASHSEED=0 .venv/bin/python tests/smoke_lib.py
```

Every paid call is cached in `results/gloss_cache.jsonl`, so a re-run costs $0.

Using the library:

```python
import sys; sys.path.insert(0, "lib"); import api
api.consensus_score(text, fol, peers, mode="align")   # also exact | nf | hyb | pn | rw | gg
```

## Restoring removed files

`.aii/manifest.yaml` marks only these for deletion; everything else is kept.

- `.venv/` (regenerable): `uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml`
- `**/__pycache__/`, `.pytest_cache/` (regenerable): recreated by any `python src/*.py` or `pytest` run.

The NLTK data used by the exp-1 / exp-8 text helpers is not copied (182 MB). `lib/api.py` reads it read-only from
`/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/nltk_data`.
Elsewhere, `python -m nltk.downloader wordnet omw-1.4` restores it.

## Caveats

- E is development data. The +0.015 screen margin is a heuristic, far below the E long-pool SE (~0.02); no E advantage
  is a claim.
- **PERTURB rename gates.** The unmutated E references are rarely endorsed by peers on long sentences (base FA 0.83 at
  c > 0.5). As a result, g1 and g2 are near-trivial for every metric: MEANING_RENAME recall is 1.0 for both GG and
  c_align.
- **Checker.** The GG checker is google/gemini-2.5-flash, the same family as the flash-lite judge comparator; this is a
  limitation for any judge-vs-GG comparison. Prompt v2 is stricter on synonyms (G-A YES_SYN accuracy 0.80 on the confirm
  half), which contributes to GG's higher d.
- The oracle and T9 diagnostics use labels and are post-seal only; they never entered selection.
