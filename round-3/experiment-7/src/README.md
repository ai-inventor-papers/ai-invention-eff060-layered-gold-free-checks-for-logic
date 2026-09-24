# R_COMP: model agreement vs LLM judges on long rule sentences

Run `run_u75jRHUss0zo`, iteration 3, `gen_art_experiment_7`. This artifact finishes **R_COMP** (dataset 3: templated
long rule sentences, each with at least 25 words, at least 3 conditions and one *unless / except / provided that / only if*
clause, whose weak and strong references are trusted by construction). It then scores R_COMP with **cross-family
consensus** metrics and compares them with **LLM judges**.

Each sentence is translated by 10 few-shot LLM slots from 9 vendor families, in two conditions:

- **SIG**: the frozen `fewshot_v1` prompt plus an alphabetically sorted signature block (predicates and constants only).
  Labels are **pure z3 equivalence** to the weak or strong reading, so no aligner, panel or LLM touches them. This removes
  the shared-aligner confound by construction.
- **FREE**: the unchanged `fewshot_v1` prompt, labelled by dataset 3's solver-modulo-alignment rule (tier A only, see D9).

**Headline:** see `results/tables.md` (every number with its n and 95% CI) and `results/analysis.json`.

### Key results (R_COMP-SIG: 221 sentences, 2,024 primary rows = 429 ERROR / 1,595 CORRECT; TESTABLE)

| result | value |
|---|---|
| **Primary (criterion c)**: within-template AUROC, c_score_sig vs judge_cheap_disg (n = 1,904 with both scores, 220 sentences) | 0.954 vs 0.587, **delta +0.367 [0.328, 0.404]**, one-sided p < 0.0005 → **PASS** |
| Same, vs the original-text cheap judge (the conservative bar; see the next row) | 0.952 vs 0.673, delta +0.278 [0.239, 0.319] |
| Disguise cost on R_COMP (judge orig − disg, within-template): templated sentences cannot be memorised, so this is the disguise's own cost | cheap +0.085 [0.034, 0.132]; local Qwen3-8B +0.175 [0.140, 0.212] (on E, exp 5 found −0.064) |
| Pooled / within-sentence deltas (robustness) | +0.388 [0.350, 0.427] / +0.369 [0.324, 0.412] |
| Nested adds-signal: [judge_disg + c_sig] over [judge_disg] (OOF, within-template) | +0.377 [0.338, 0.416]; the reverse, [c_sig + judge] over [c_sig], is +0.004 [−0.000, 0.008] (the judge adds nothing) |
| Frontier gemini-3.1-pro, 60-row subsample (30/30, descriptive) | c_sig 0.956, frontier orig 0.932, frontier disg 0.735; [frontier + c_sig] over frontier +0.088 [0.019, 0.172]; one frontier call costs 6.1× the peer generations one consensus score needs |
| Local Qwen3-8B judge (disg / orig) | 0.498 / 0.672 |
| Variants on SIG (shared names) | c_align = c_sig on 2,134 of 2,140 rows; c_nf and c_hyb 0.950; graded g_align / g_nf 0.977 / 0.976 |
| Rename false alarms (CORRECT copies, nonce / synonym rename) | c_sig 1.00 / 1.00 (by design); c_align 1.00 / 0.64; **c_nf and c_hyb 0.26 / 0.25 (= unrenamed 0.26: invariant)**; g_nf 0.09 / 0.09 |
| Mechanism | e (ERROR rows endorsed by a peer majority) = 0.00; d (CORRECT rows flagged) = 0.26, of which **strong-reading CORRECT rows 0.96 vs weak 0.14**: consensus false alarms are valid minority readings |
| Operating point (flag at c ≥ 0.5) | c_sig: precision 0.51, recall 1.00, FA 0.26; g_nf: precision 0.75, recall 0.97, FA 0.09; judge_disg: precision 0.25, recall 0.80, FA 0.63 |
| Complexity (GEE slope of decision correctness per SD of words) | consensus −0.06 [−0.27, 0.16]; judge_disg −0.15 [−0.31, 0.01]; interaction n.s. Within-template AUROC is flat across word terciles (0.96 / 0.95 / 0.95) |
| Placebos | composition (words) 0.49; permutation: observed 0.367 vs 95th percentile 0.154 (p = 0.005); label shuffle 0.51 |
| Coverage view (UNPARSEABLE = ERROR) | delta +0.357 [0.321, 0.393] |
| FREE (tier A only, NOT_TESTABLE: 34 CORRECT / 420 ERROR, no panel) | sign positive but CIs include 0: c_align − judge_disg +0.214 [−0.034, 0.377]; c_hyb +0.191 [−0.043, 0.348]. Consensus AUROC drops from 0.95 (SIG) to about 0.80 (FREE tier A): the cost of vocabulary divergence |
| API spend of this artifact | $1.58 (ledger `cost_ledger.jsonl`; hard cap $9.5), plus $0.414 spent by dataset 3 before this artifact |

Reading: when every system uses the same vocabulary, cross-family agreement is a far stronger faithfulness signal than
the cheap LLM judge (disguised or not), and it adds signal even over a frontier judge on the subsample. Its failure mode
is flagging correct translations that follow the minority (strong) reading of the exception clause. These are SIG
(upper-bound) numbers; the FREE contrast shows how much vocabulary divergence costs.

## Layout

| path | what |
|---|---|
| `method.py` | entry point: `stages` (the pipeline, in order), `analyse` (S10 + audit + records + method_out), `build` |
| `src/consensus_rcomp.py` | **reusable metric functions**: `consensus_exact(fol, peers)` (SIG-exact) and `consensus_scores(text, fol, peers)` (frozen exp-5 ALIGN / NF-anchored / HYB / graded), each with a precise docstring |
| `src/sig_prompt.py` | SIG signature block (sorted by predicate name; no exception or reading wording) |
| `src/gen_sig.py` | S3 SIG generation (dataset-3 slots, normaliser and client) -> `rcomp/raw/generations_sig.jsonl` |
| `src/label_sig.py` | S5 SIG labels (case-only canonicalisation onto the signature, exact z3 classes, weak/strong/converse), plus typed repair ops |
| `src/testability.py` | S6/S8 testability declaration with the label-vector sha256, written before any score |
| `src/score_consensus.py` | S7a/S9 label-blind consensus scoring (c_score_sig + frozen exp-5 variants + HYB) and the S10.8 rename pass |
| `src/run_judges.py` | S7b/S7c/S9 flash-lite rubric-A judge (disguised = the bar, and original), frontier subsample, T4 regression |
| `src/local_judge_rcomp.py` | S7d local Qwen3-8B judge (GPU env `.venv_gpu`) |
| `src/panel_rcomp.py` | S8 FREE panel routing / assembly (`assemble` ran; `check`/`run` not run, D9) |
| `src/analyse.py`, `src/auc_tools.py` | S10: stratified cluster-bootstrap AUROC engine, every pre-registered statistic |
| `src/artifact_budget.py` | the ONE budget guard: artifact ledger `cost_ledger.jsonl`, $9.5 hard stop, shared-key floor |
| `src/write_records.py`, `src/key_poll.py` | deviations + vendor patch hashes; F1 key poller |
| `src/vendor_x5/`, `src/vendor_e_panel/` | vendored exp-5 / exp-D / dataset-E code (hashes and patches in `results/VENDOR_SHA256.json`) |
| `rcomp/` | copy of dataset 3 (code, lexicon, prereg_rcomp.json); `rcomp/raw/` = generations; `rcomp/work/` = frozen sentences, FREE solver labels |
| `tests/` | `test_label_sig.py` (T2), `test_consensus_rcomp.py` (T3 incl. exp-5 regression), `test_peer_text_x5.py`, `audit_rederive.py` (T8) |
| `results/prereg_sig.json` + `.sha256` | SIG pre-registration, git-committed before the first SIG call |
| `results/testability*.json` | testability declarations (SIG committed before any SIG score) |
| `results/sig_labels.jsonl`, `sig_classes.json`, `sig_repairs.jsonl` | SIG labels, exact z3 classes, typed repair ops of ERROR classes |
| `results/free_labels.jsonl` | FREE labels (tier A; routed rows UNRESOLVED) |
| `results/scores_{SIG,FREE}.jsonl`, `scores_rename_SIG.jsonl` | consensus scores per row (label-blind) |
| `results/judge_*.jsonl`, `disguise_map_*.jsonl` | judge outputs (cheap, frontier, local) and disguises |
| `results/rcomp_candidates.jsonl` | one row per candidate per condition: labels, strata, class ids, every score |
| `results/analysis.json`, `results/tables.md` | all S10 numbers |
| `results/deviations.json` | every departure from the plan, with its cost |
| `reproducibility.md`, `requirements_gpu.txt` | exact commands in the order they ran, hardware, runtimes; pins of the GPU env |
| `tests/rederive_raw.py` → `results/rederive_raw.json` | independent re-derivation of every headline number from the raw files (brute-force AUROC, own bootstrap) + placebos that must fail |
| `method_out.json` (+ `full_`/`mini_`/`preview_`) | exp_gen_sol_out: datasets `R_COMP_SIG` and `R_COMP_FREE` |
| `cost_ledger.jsonl` | artifact API ledger (every call: utc, phase, model, usd, tokens) |

All kept artifacts stay at their workspace path:
`./<path>`.

## How to run

```bash
./restore.sh                                   # venvs + NLTK data (see below)
source env.sh
.venv/bin/python method.py stages              # the ordered pipeline (all stages are resumable; caches avoid re-billing)
.venv/bin/python method.py analyse --B 2000    # S10 analysis, T8 audit, deviations, method_out.json ($0, ~3 min)
.venv/bin/python -m pytest tests/test_label_sig.py tests/test_consensus_rcomp.py tests/test_peer_text_x5.py -q
(cd rcomp && .venv/bin/python -m pytest tests -q)
```

Scoring only (label-blind): `.venv/bin/python src/score_consensus.py run --cond SIG`. Judges:
`src/run_judges.py cheap --cond SIG`. Every API stage goes through `src/artifact_budget.py`, which checks the artifact total
and the shared key after every call.

## Design in one paragraph

Primary test (criterion c): the within-template stratified paired delta AUROC(c_score_sig) − AUROC(judge_cheap_disg) on
the SIG primary pool (10 few-shot slots, CORRECT/ERROR), restricted to rows where both scores exist. Its CI comes from a
sentence-clustered bootstrap stratified by template (B = 2000, seed 20260924), and it PASSES iff the 95% CI lower bound is
above 0. All metric parameters are frozen from exp 5, with no fitting on R_COMP. Metrics are oriented so that higher =
more likely ERROR. Secondary analyses: pooled and within-sentence deltas, a nested adds-signal logistic model
(cross-fitted by sentence folds), the frontier subsample, operating points, per template and clause type, complexity
(terciles, nconds, GEE slopes and interactions), mechanism inputs (e/d, z3 class ids), rename invariance, a coverage view,
a contamination negative control, placebos (composition, 200 within-sentence permutations, label and score shuffles),
system-level correlations, error types, and cost.

## Caveats (read before citing)

- R_COMP is **semi-synthetic** (9 templates, one exception clause each). SIG removes vocabulary choice, so its errors are
  structural; SIG is therefore an upper-bound regime for consensus. It is never pooled with real-distribution results (E, T1).
- `c_score_sig` needs a shared signature: its rename false-alarm rate is 1.0 **by design**, so it is a labelling-regime
  metric. The deployable, rename-invariant variants are NF-anchored and HYB (see the rename table).
- The shared OpenRouter key had a **$7 total daily limit for all concurrent runs**. Consequences (deviations D1, D5, D7–D9):
  no Sonnet audits, no GPT-5.1 FREE arm, a 60-row frontier subsample, and **no FREE panel**. FREE is therefore tier-A only
  and NOT_TESTABLE, reported sign-only and descriptive.
- No human labels. SIG labels are exact by construction; FREE labels are solver labels.

## Restoring removed files

`.aii/manifest.yaml` marks these for deletion after the round; `./restore.sh` rebuilds the environments:

| path | restore |
|---|---|
| `.venv/` (`rcomp/.venv` is a symlink to it) | `uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml && ln -sfn ../.venv rcomp/.venv` |
| `.venv_gpu/` | `uv venv .venv_gpu --python=3.12 && uv pip install --python .venv_gpu/bin/python -r requirements_gpu.txt` |
| `**/__pycache__/` | regenerated automatically on import |
| `.pytest_cache/`, `rcomp/.pytest_cache/` | regenerated by `.venv/bin/python -m pytest tests -q` (and `cd rcomp && .venv/bin/python -m pytest tests -q`) |

Everything else (results, generations, NLTK data, method outputs) is kept in place.

The local judge weights (`Qwen/Qwen3-8B`) live in the run's shared HF cache, not in this workspace:
`.venv_gpu/bin/python -c "from huggingface_hub import snapshot_download; snapshot_download('Qwen/Qwen3-8B')"`.
