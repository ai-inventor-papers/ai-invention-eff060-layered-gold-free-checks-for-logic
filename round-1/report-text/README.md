# gen_report_text — Iteration 1 Report

Internal research report for run_u75jRHUss0zo, iteration 1: gold-free
faithfulness metrics for NL-to-FOL translation.

## What this module did

Compiled results from four experiment artifacts (FOL-Triage, cross-system
consensus, disguised judge/baselines, held-out dataset) into a structured
research report with figures, citations, and artifact provenance markers.

## Layout

- `.terminal_claude_agent_struct_out.json` — final structured output (title, abstract, paper_text, figures array, summary)
- `report_draft.md` — the full report text used to build the structured output
- `references.bib` — BibTeX entries for 16 cited papers (fetched from Semantic Scholar, 4 written manually)
- `domain_terms.json` — 90 domain vocabulary terms used for the terminology sweep
- `style_exemplars.md` — verbatim passages from 4 field papers for register matching
- `.aii/manifest.yaml` — file inventory

## How to regenerate

All files in this workspace are text outputs of the report-writing agent.
No GPU, no external data downloads, no large binaries. To regenerate,
re-run the `gen_report_text` module for iteration 1 of this run.
