# R_COMP FREE: finish the free-vocabulary labels, then test consensus vs the LLM judge

Run `run_u75jRHUss0zo`, iteration 5, `gen_art_experiment_13`.
Workspace: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13`.

This artifact resumed the frozen dataset-5 labeller (art_Ia_FT284H33j) once, to give R_COMP FREE a CORRECT class. R_COMP FREE
has 2,652 free-vocabulary FOL translations of 221 **templated** long rule sentences, from 10 LLM slots and 9 families. The
artifact then tested criterion (c) once: does cross-family solver consensus (`c_score_align`) beat the flash-lite rubric-A
LLM judge in both the disguised and the original view?

## Result

**Criterion (c) = NOT_TESTABLE (pre-registered FALLBACK B).** The two-checker gloss gate failed twice:

| run | checker | balanced accuracy | failure type |
|---|---|---|---|
| gloss_v1, half A | Haiku 4.5 | 0.776 | judgement |
| gloss_v1, half A | Qwen3-235B | 0.855 | judgement |
| gloss_v2 (the ONE revision), held-out half B | Haiku 4.5 | 0.561 | format: 141/398 NO_VERDICT; 0.861 on verdicted items |
| gloss_v2 (the ONE revision), held-out half B | Qwen3-235B | 0.883 | judgement |

The bar is 0.90 per checker. Neither checker passes alone either, so fallback C is not available. Under the frozen rule, all
1,506 MAPPED rows became `UNRESOLVED_GLOSS_GATE_FAILED`, leaving 0 CORRECT rows. No ungated checker was substituted.

**PROVISIONAL, NON-CONFIRMATORY evidence** (addendum prereg, written before the join). Labels are ERROR_CERT vs MAPPED, on
untouched rows only. Every AUROC is within-template; every CI is a template-stratified sentence bootstrap with B = 2000.

| comparison | c_align AUROC | judge AUROC | delta [95% CI] |
|---|---|---|---|
| disguised view (n 1,706) | 0.801 | 0.584 | **+0.217 [0.175, 0.260]** |
| original view (n 1,709) | 0.804 | 0.633 | **+0.171 [0.135, 0.206]** |
| audit-consensus labels, disguised (n 146) | 0.899 | 0.522 | +0.377 [0.256, 0.502] |
| audit-consensus labels, original (n 136) | 0.903 | 0.798 | +0.105 [0.011, 0.215] |
| frontier gemini-3.1-pro, original (150 rows) | 0.801 | 0.852 | −0.051 [−0.153, 0.044] |

**Robustness:**
- The disguised- and original-view deltas stay positive in every sensitivity (s1a, s1b, s3, s5, s7, s9, s10) and in 8 of 9
  templates. T2's CI includes 0.
- Nesting: [judge + c] − [judge] = +0.23 / +0.20; [c + judge] − [c] = +0.02.
- Against the frontier judge: [c + frontier] − [c] = +0.086 [0.003, 0.166].

**Complexity:** the original-view advantage shrinks with sentence length: W1 +0.285, W3 +0.084 (delta-of-deltas −0.20,
CI [−0.31, −0.08]).

**Blind two-family audit** (Sonnet-5 + GLM-4.6, 100 ERROR_CERT + 100 MAPPED; kappa 0.62):

| auditor | ERROR_CERT precision | MAPPED faithful |
|---|---|---|
| Sonnet-5 | 0.845 | 0.722 |
| GLM-4.6 | 0.720 | 0.904 |
| rows where both auditors agree | 0.838 | 0.917 |

The noise correction that assumes non-differential contamination is not valid: corrected AUROCs exceed 1 for the
single-auditor rates. The contamination is differential: ERROR_CERT rows that the auditors call faithful still get high
consensus scores.

**H-MECH (provisional):**

| item | result | verdict |
|---|---|---|
| (i) share of ERROR among the non-agreeing peers of MAPPED candidates | 0.30 (exact rule), 0.41 (ALIGN rule) | bar ≥ 0.50 **failed**: legitimate divergence dominates |
| (ii) SCATTER ratio SI_cor / SI_err | 5.8 [4.1, 8.8] | bar ≥ 2 passed |
| (iv) ALIGN vs exact correct-divergence d | ALIGN lowers d by 0.24 | prediction confirmed |

**Other rows:**
- **Consensus variants:** V1–V5 do not beat V0. The sibling freeze verdict was "V0 stands".
- **Placebos:** within-template label shuffles covered 0 in 17 of 20 runs, one short of the 18/20 bar. A post-hoc
  100-shuffle supplement gave 95/100. A random score gets AUROC 0.48 [0.45, 0.51].
- **Independent re-derivation:** matches to 1e-9 (`results/rederive_raw.json`, `results/rederive_check.json`).

**Spend:**
- This artifact spent $1.97 of its $4 cap.
- The run-level OpenRouter budget was then exhausted by the run's parallel artifacts, and one optional audit retry was
  refused (D25).

## Layout

| path | what |
|---|---|
| `method.py` | entry point; runs each step script in pre-registered order (`uv run method.py --steps analysis,report,checks`) |
| `prereg_rcomp_confirm.json` (+ `.sha256`) | frozen prereg, git-committed 11:18:46Z before the first gloss call |
| `prereg_addendum_fallbackB.json` | provisional-view / audit / noise-correction plan, written before the join |
| `confirm/` | new code: `scores.py` (sealed score table), `judge_orig_complete.py`, `gloss_pilot.py`, `gate_diagnostics.py`, `audit_blind.py`, `frontier_judge.py`, `join_and_test.py`, `analysis_lib.py`, `auc_tools.py` (verbatim exp 7), `report.py`, `final_checks.py`, `write_deviations.py`, `g0_repro.py`, `prereg.py`, `cc.py` |
| `labeller/` | dataset-5 labeller copy (src, vendor, prompts incl. `gloss_v2.json`, work, results incl. `gate_report.json`, `gloss_cache.jsonl`, `seal.json`), `cost_ledger.jsonl` |
| `results/confirm_verdict_rcomp.json` | verdict, flags, provisional headline |
| `results/analysis_rcomp.json`, `results/tables.md` | every analysis; every table has a `# source:` line |
| `results/per_item_rcomp_free.jsonl` | one row per FREE record: labels, strata, flags, every score |
| `results/rcomp_free_labels_final.jsonl`, `results/seal.json`, `results/verify_seal.py` | sealed final labels |
| `results/scores_rcomp_free.jsonl`, `results/score_seal_rcomp.json`, `results/score_seal_rcomp_v.json` | sealed scores (V4 seal separate) |
| `results/gate_report.json`, `results/gate_diagnostics.json` | gate results and failure diagnosis |
| `results/audit_rows.jsonl`, `results/audit_report.json` | blind audit |
| `results/judge_orig_iter5_FREE.jsonl`, `results/judge_frontier_FREE.jsonl` | iteration-5 judge calls |
| `results/deviations.json` | D1–D9 (dataset 5) + D10–D26 |
| `results/cost_ledger.jsonl`, `results/final_checks.json` | ledger and final checks |
| `freeze_copy_prelim/`, `freeze_copy/` | sibling consensus_variants.py (pre-label copy) and the M1 marker + selection.json |
| `src/labelling_tools.py` | re-export of the GOLD-USING labelling functions (never a gold-free metric) |
| `tests/` | analysis tests, isolation firewall, `rederive_confirm.py`, `rederive_raw.py` |
| `method_out.json` (+ `full_`, `mini_`, `preview_`) | exp_gen_sol_out: one example per FREE row; `predict_*` = metric scores (higher = ERROR) |

## How to run

```bash
uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml
.venv/bin/python -m pytest -q -c pytest.ini tests/ && (cd labeller && ../.venv/bin/python -m pytest -q)
.venv/bin/python method.py                       # $0: verify seals, join, analyses, report, checks
.venv/bin/python tests/rederive_raw.py            # independent re-derivation from the raw files
```

The paid steps (`--steps judge_orig,pilot,gate,audit,frontier`) are cached and ledgered. See `reproducibility.md`.

## Restoring removed files

| path (manifest `delete`) | restore |
|---|---|
| `.venv/` | `uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml` |
| `**/__pycache__/` | regenerated automatically by Python on import |
| `**/.pytest_cache/` (incl. `labeller/.pytest_cache/`) | regenerated by `pytest` |

Everything else (results, labeller, code, logs) is kept in place at the workspace path above; the git history timestamps the prereg, the seals
and the gloss_v2 freeze.
