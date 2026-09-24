# Name-free labels for free-vocabulary rule translations (T7b)

Run `run_u75jRHUss0zo`, iteration 4, `gen_art_dataset_5`. Workspace:
`/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5`.

This artifact labels the **FREE** condition of R_COMP: 2,652 free-vocabulary FOL translations of 221 templated
rule sentences, produced by 10 LLM slots from 9 families. The labeller shares **no instrument** with any consensus metric
or LLM evaluator:
- no name similarity, no aligner and no evaluator code (a firewall test enforces this);
- an exhaustive, certificate-backed search over a declared family of symbol maps decides whether the candidate can be
  z3-equivalent to an accepted reading;
- a pre-registered, gated two-family gloss check is meant to decide whether the mapped names mean the template atoms.

**Status: the gloss check could not run (deviation D9).** The run's OpenRouter budget was exhausted by earlier steps
before this artifact's first call ($0 spent here). The released labels are therefore **search-only**, but sealed:
- **ERROR_CERT (759)** is final;
- **MAPPED rows (1,506)** are `UNRESOLVED_GLOSS_NOT_RUN`;
- `src/resume_gloss.py all` finishes everything once the budget is raised.

`dataset_card.md` holds every number and caveat.

## Key results

| | value |
|---|---|
| FREE rows / unique (sentence, candidate) classes | 2,652 / 2,163 (+188 UNPARSEABLE, 199 NO_OUTPUT kept as rows) |
| search | 156k maps enumerated, 0 cap hits, 0 z3 UNKNOWN, median 0.25 s per class (4 CPUs, 3.5 min total) |
| search-only labels | ERROR_CERT 759 · UNRESOLVED_GLOSS_NOT_RUN 1,506 · UNPARSEABLE 188 · NO_OUTPUT 199 |
| SIG replay (2,140 rows, names replaced by nonces) | false ERROR_CERT on known-CORRECT **0/1,595**; identity map recovered 100%; known-ERROR rescued by a non-identity map 9.1% (the gloss check's job); oracle-checker ceiling: recall 1.00, false CORRECT 0.00 |
| executor audit (non-blind, 60 + 60) | ERROR_CERT precision 0.867 [0.76, 0.93] (out-of-family faithful forms: disjunctive split, ∃-for-constant, in-name negation); MAPPED faithful 0.867 [0.76, 0.93] |
| iteration-3 tier-A labels | 34/34 old CORRECT are MAPPED; 297/420 old ERROR are MAPPED; 17 of 20 hand-checked disagreements are old false errors (aligner failures) |
| testability | search-only: NOT_TESTABLE (no CORRECT class yet); provisional ERROR_CERT vs MAPPED: TESTABLE on all rows (759/1,506) and on the untouched subset (636/1,175) |

## Layout

| path | what |
|---|---|
| `data.py` | `uv run data.py`: standardises the top-6 candidates (3 plan groups + FOLIO, MALLS-v0 test, LogicNLI test from `temp/datasets/`) to exp_sel_data_out -> `temp/candidates_data_out.json`, and writes the best 3 (the plan groups) to `full_data_out.json` |
| `full_data_out.json` (+ `mini_`, `preview_`) | exp_sel_data_out, the selected 3 groups: `rcomp_free_labels` (2,652), `gloss_gate_items` (840), `sig_soundness_replay` (4,280) |
| `dataset_card.md` | provenance, label semantics, exactness, audits, known out-of-family forms, licences, intended use |
| `prereg_freelab.json` + `.sha256` | frozen pre-registration v1.1 (family, bridges, prunes, caps, label + gloss rules, gloss_v1 prompt, gate, testability, audits); `prereg_freelab_v1.*` = the superseded v1 |
| `deviations.json` | D1-D9 with timestamps (D6 family amendment, D8 T8 converse at the gloss level, D9 no API budget) |
| `VENDOR_SHA256.json`, `vendor/` | reused code with sha256 of sources and copies: `fol.py`, `templates.py` whole; `*_min.py` are single functions extracted by `src/vendor_copy.py` (no aligner / similarity helpers) |
| `src/freelab.py` | **reusable functions** `exhaustive_map_label(candidate_fol, readings, atoms, glosses, checker)`, `equivalent_modulo_vocab_exhaustive(a_fol, b_fol)` (symmetric, name-free), `label_candidate`, `gloss_decision`; the docstrings state what is exact and what is bounded |
| `src/inputs.py` | STEP A: sentences + glosses, FREE rows from raw generations only, count table, label-free shape census |
| `src/prereg.py` | STEP B: pre-registration writer |
| `src/run_search.py` | STEP C: parallel map search (FREE classes; renamed SIG classes) |
| `src/gate.py`, `src/gloss.py`, `prompts/gloss_v1.json` | STEP D/E: gate items + evaluation; async OpenRouter gloss client with cache, ledger, budget guard |
| `src/sig_rename.py`, `src/soundness.py` | STEP F: nonce / synonym renames of SIG rows; audits (i)-(iii) |
| `src/assemble_labels.py` | STEP G: labels, testability, seal (search_only / final mode) |
| `src/post_seal_join.py` | STEP H: whitelist join of iteration-3 labels, untouched subset, agreement table |
| `src/provisional_view.py` | provisional ERROR_CERT vs MAPPED testability + contamination |
| `src/build_output.py` | STEP I: full_data_out.json |
| `src/resume_gloss.py` | runs every pending paid step in order |
| `src/hf_survey.py`, `temp/dataset_survey.md`, `temp/datasets/` | external dataset survey (context only; not used for labels) |
| `results/free_labels_v2.jsonl` | one row per FREE record with all label metadata (the source of group 1) |
| `results/map_search.jsonl` | one line per unique class: status, counts, certificates, every equivalent map (as pair ids) and the gloss pair union |
| `results/sig_replay_{nonce,syn}.jsonl`, `results/sig_replay_rows.jsonl` | audit (i) search output and per-row metrics |
| `results/seal.json` | label-vector sha256 (all rows; untouched subset), prereg / vendor / code hashes |
| `results/testability_FREE_v2.json` | testability per population and stratum (+ provisional view) |
| `results/soundness_audit.json`, `results/old_label_agreement.json` | audits (i)-(iii) |
| `results/gate_items.json`, `results/gate_report.json` | gate items (built); gate NOT_RUN (D9) |
| `results/input_counts.json`, `results/shape_census.json` | input reconciliation; label-free census that set the bridge list |
| `work/` | intermediate inputs (sentences.json, free_rows.jsonl, renamed SIG rows, executor-audit verdicts, dev-trial / probe scripts) |
| `cost_ledger.jsonl` | API ledger ($0 billed; refused calls recorded) |
| `tests/` | pytest: identity / synonym / nonce recovery, Q/E swap, DROP/ADD, bridges B1-B5, T8, symmetric API, evaluator vs z3 on 200 random pairs, gloss rule, client (mocked transport), firewall |

## How to run

```bash
uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml
.venv/bin/python -m pytest -q                       # 13 tests
.venv/bin/python src/vendor_copy.py                 # re-vendor (hashes -> VENDOR_SHA256.json)
.venv/bin/python src/inputs.py                      # STEP A
.venv/bin/python src/prereg.py                      # STEP B (writes v1; the v1.1 amendment is in deviations.json / prereg_freelab.json)
.venv/bin/python src/run_search.py free             # STEP C (~3.5 min on 4 CPUs)
.venv/bin/python src/gate.py build                  # gate items
.venv/bin/python src/sig_rename.py && .venv/bin/python src/run_search.py sig --rename nonce && .venv/bin/python src/run_search.py sig --rename syn
.venv/bin/python src/assemble_labels.py --mode search_only && .venv/bin/python src/post_seal_join.py
.venv/bin/python src/soundness.py && .venv/bin/python src/provisional_view.py && uv run data.py
# once the OpenRouter budget is available (~$1.8):
.venv/bin/python src/resume_gloss.py all
```

`common.py` points `NLTK_DATA` at exp 7's `data/nltk_data` (WordNet), read-only.

## Restoring removed files

`.aii/manifest.yaml` marks only regenerable environment bulk for deletion:

| path | restore |
|---|---|
| `.venv/` | `uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml` |
| `**/__pycache__/`, `.pytest_cache/` | regenerated automatically by `python` / `pytest` |

Every result, label, audit and log stays in place at the workspace path above. There are no large binaries.
