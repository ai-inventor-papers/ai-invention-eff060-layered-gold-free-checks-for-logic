# Corrected record and paper-ready fixes (iteration 5, evaluation 4)

This is an erratum and reproducibility pass for the NL→FOL gold-free metric meta-evaluation of run `run_u75jRHUss0zo`. It is **CPU only, makes no LLM or network calls, and spent $0**; `eval.py` asserts that `openai` and `requests` are never imported. It addresses the 11 blocking critiques of the iteration-4 review (score 3) with file-sourced, paste-ready paper text. **Every number is read by code from its source file through a recorded locator. None is typed by hand.**

All E, R_COMP SIG and PERTURB numbers are **DEVELOPMENT** data. This artifact confirms nothing: it transcribes, re-derives and labels data roles.

## Results in one table

| Quantity | Value | File |
|---|---|---|
| Hypothesis §0.2–0.3 + review claims checked against their files | **244 / 244 MATCH** at the literal's precision (0 MISMATCH, 0 NOT_FOUND, 0 AMBIGUOUS). The hypothesis text needs no correction | `numbers.csv` |
| Additional table cells transcribed by code (no claim literal) | 258 TRANSCRIBED + 52 COMPUTED rows (counts, spend, placeholder resolution), 554 rows in total | `numbers.csv` |
| Paper (iter-4 `paper_draft.md`) vs file | **15 MISMATCH**. They are: all six §4.2 headline CIs (narrower than the source); COMPOUND 0.643/0.246 (source: 0.282/0.107); G2 "FAIL" (source: NOT_READ); the M3 CI; the §3.6 spend ($1.58 vs $4.33); the §3.5 cost column (k = 1/3/7, per-candidate arithmetic labelled "per sentence"); the frontier ratio "6.07×" (source: 30.2× per item). A further 153 match and 76 claims do not appear in the paper | `mismatches.csv`, `record_final.md` §0 |
| Correction markers `~~original~~ [Correction, iter 4: …; source <path>]` | 43. For 42 of them the struck text is quoted verbatim from the paper with its line number. The remaining one ('588 common items') is not present in the paper | `tables/correction_markers.csv` |
| Lints (held-out E, recall without base FA, FA without flip, 0.683 as an AUROC, CIs not verbatim, costs without units, missing marker paths, untraced numbers) | **0 failures** | `lint_report.json` |
| Reviewer items | **9 CLOSED, 2 PARTIAL**. Critique 7 (scope) can only be closed by the iteration-5 experiments. Critique 8: part of the $7 budget stays unaccounted | `reviewer_checklist.csv` |
| Placeholder artifact IDs | 4 resolved from `artifact_id_map.csv` (sed-ready), 0 unresolved, none invented | `tables/placeholder_ids.csv`, record §5 |
| Independent re-derivation from raw per-item files (second code path; imports nothing from `src/`) | **17 / 17 pass**, including 0.614 / 0.770 / 0.774, e/d, base FA 0.712/0.803/0.986/0.757, the E2 and R_COMP FREE label counts, 77% / 61%, and iteration-4 spend. Shuffled-label placebo AUROC 0.458 (CI covers 0.5). Our B = 2000 c_csc CI is [0.487, 0.734]. The record transcribes T4 [0.493, 0.736] | `audit/rederive.json` |
| Definition check | Exp-9 "strat AUROC" is the **pair-weighted** (n_pos·n_neg) mean of within-stratum AUROCs, not the n-weighted one: n-weighting gives 0.598 for c_csc | `audit/rederive.json` extra |
| Checker mutation test | 10 / 10 injected errors caught (last digit, swapped CI bounds, flipped sign); 10 / 10 untouched claims still MATCH | `audit/checker_mutation.json` |
| Iteration-4 spend (ledgers only; 59 ledger files, byte-identical clones dropped, records de-duplicated across files) | Iteration-4 artifacts **$0.349**. Other artifacts whose records fall in the same window (iteration-3 experiments) $4.338. Evidenced total $4.687 vs the $7.00 phase budget: **$2.313 unaccounted (no ledger in the run tree records it)**. One ledger note reads "run Test-idea budget $7.04 of $7.00 already spent by earlier steps" | `results/spend_iter4.json`, record §14 |
| Claims ledger | 45 claims: DEV 23, CONFIRM-PENDING 7, DESCRIPTIVE 11, OUT-OF-SCOPE-SIG 2, GOLD-USING-ORACLE 2. Each names the iteration-5 sibling file that confirms or refutes it | `claims_ledger.csv` |
| Iteration-5 skeleton | 42 shell cells `{{file::json.path}}`. At the last run, 9 of the named sibling files existed (freeze, gg_gate, drift decision, screen, R_COMP score seal), with 7 fields present. Values are filled only when the file AND its seal/token exist | `skeleton_iter5.md`, `skeleton_resolution.json` |

## Layout

| Path | What |
|---|---|
| `eval.py` | Orchestrator, in this order: claims → `numbers.csv` → `record_final.md` + lints → claims ledger → checklist → skeleton → figures → audit → mutation test → `eval_out.json` |
| `src/io_locators.py` | Loaders returning (value, locator): `json_key`, `csv_cell`, `md_table_cell` (fallback), `regex`, `jsonl_count`, `ledger_sum`, `expr`. Hashes every file read |
| `src/claims_spec.py` → `claims_spec.yaml` | The hand-curated claim list: the literal as written in the hypothesis or review, plus one locator per claim |
| `src/transcribe.py` | Table cells transcribed by code (controls, cost table, T7 invariance, k-curve, …) |
| `src/checker.py` | Precision rule (MATCH iff \|claim − file\| ≤ 0.5·10^−d; CIs bound by bound; signs must agree; percentages compared as fractions), paper grep within section ranges re-derived from `^#+` headings |
| `src/sections.py`, `src/ctx.py` | The 17 paste-ready sections plus a §0 summary. Every number is rendered from a `numbers.csv` row and tagged `<!-- n:id -->`; verbatim table rows are tagged `<!-- v:file -->` |
| `src/lints.py` | The 8 lints |
| `src/spend.py` | Ledger scan, de-duplication and window |
| `src/ledger_checklist.py`, `src/skeleton.py`, `src/figures.py`, `src/mutation.py`, `src/eval_out.py` | Parts 3–5 and the outputs |
| `audit/rederive.py` | Independent re-derivation (numpy/pandas only) → `audit/rederive.json` |
| `record_final.md` | **The paste-ready corrected record** (§0 summary + sections 1–17; each has a 'Replaces: … lines a–b' line and a 'Sources:' line) |
| `numbers.csv` / `mismatches.csv` | Every number: claim, locator, file value, file CI, hyp-vs-file and paper-vs-file status, data role |
| `claims_ledger.csv`, `reviewer_checklist.csv` | Data roles + confirming files; critique → action → anchor → source → status |
| `skeleton_iter5.md`, `skeleton_resolution.json` | §5 skeleton for the final paper, and the sibling files and fields found |
| `figures/F1–F4` (`.pdf`, `.png`, `.json` with values, ids and a `# source:` line) | F1 development Δ forest plot, F2 "bridge trades d for e", F3 wrong-peer decomposition, F4 k-curve with the $/sentence axis |
| `tables/` | `source_hashes.csv` (sha256 of every file read), `correction_markers.csv`, `placeholder_ids.csv`, `review_numbers.csv` (205 of 207 decimal literals in the critiques map to a `numbers.csv` row; the 2 unmapped are a section title and the §1.4 "+0.024") |
| `eval_out.json` (+ `full_`/`mini_`/`preview_`) | exp_eval_sol_out, validated: `metrics_agg` plus datasets `numbers_check` (one example per `numbers.csv` row), `reviewer_checklist` and `claims_ledger` |

## How to run

```bash
./run_all.sh          # creates .venv if missing, then .venv/bin/python eval.py (~30 s, exits non-zero on any lint failure)
```

The sources are read-only at absolute paths under `../../../` (iterations 1–5). A missing source yields NOT_FOUND rows rather than a crash. The skeleton resolution depends on when you run it, because the iteration-5 siblings are still writing: re-run `eval.py` at paper time.

## Deviations and caveats

- `claims_spec.yaml` is exported from `src/claims_spec.py`; the locators were written in Python for brevity.
- `record_final.md` §0 lists hypothesis corrections. There are none: the iteration-4 hypothesis §0 already matches every file.
- The two c_align rename flip rates differ between eval 3 (`perturb_corrected.csv`, NONCE flip 0.605) and exp 10 (`controls_fa.csv`, 0.327), because they pair renames with different base rows. Both are reported with their sources and are not harmonised.
- The CTRL-share-of-FULL figure (27.4%) is read from the reviewer's `recompute_csc.json` and independently re-derived in the audit.
- Skeleton field names inside the sibling JSONs are **proposed** where the iteration-5 contract names only the file. Every missing field is flagged `FIELD_MISSING`.
- The spend window, per the plan rule, starts 6 h before the first iteration-4 ledger record. Iteration-3 experiment records fall inside it. The ledgers do not say which phase budget they were charged to, so they are listed and not attributed.
- F4 plots the eval-2 k-curve (rows with all 7 other families). The top axis gives the FULL peer-generation cost per SENTENCE.

## Restoring removed files

| Removed path | Restore with |
|---|---|
| `.venv/` | `uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml` (or `./run_all.sh`) |
| `src/__pycache__/` | regenerated automatically on the next `.venv/bin/python eval.py` |

Nothing heavy is kept. All deliverables are small text or figure files in this workspace (`.`).
