# gen_report_text — Iteration 2 Report

Internal research report for run_u75jRHUss0zo, iteration 2: gold-free
faithfulness metrics for NL-to-FOL translation.

## What this module did

Carried forward the iteration 1 report verbatim, applied reviewer-requested
factual corrections in place, and appended iteration 2 results from three
new artifacts: Experiment 5 (PEER+TEXT on held-out E), Evaluation 1 (regime
matrix and rederivation audit), and Dataset 3 (R_COMP templates and PERTURB
suite). Updated Related Work with SAC3 [17] and FormalAlign [18] citations.

## Layout

- `paper_draft.md` — full report text (iterations 1 and 2)
- `.terminal_claude_agent_struct_out.json` — structured output (title, abstract, figures, summary)
- `references.bib` — BibTeX entries for 18 cited papers
- `domain_terms.json` — 90 domain vocabulary terms
- `style_exemplars.md` — verbatim passages from 4 field papers
- `.aii/manifest.yaml` — file inventory
- `README.md` — this file

## Artifacts consumed

- art_TaxJRnPcJMuZ — Experiment 5: PEER+TEXT on held-out dataset E
- art_HepAw8c6Eu7- — Evaluation 1: regime matrix, rederivation audit, flipped items
- art_zcwCQgTqk6DN — Dataset 3: R_COMP templates + PERTURB suite

## How to regenerate

All files are text outputs. No GPU, no external data, no large binaries.
Re-run the gen_report_text module for iteration 2 of this run.
