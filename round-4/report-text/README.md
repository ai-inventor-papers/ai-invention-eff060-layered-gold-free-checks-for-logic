# gen_report_text — iteration 4

Internal research report for the gold-free faithfulness metrics project
(NL-to-FOL translation). This step writes and updates the cumulative
`paper_draft.md`, appending iteration 4 results and updating the closing
sections, related work, and references.

## What was done

1. Carried the iteration 1-3 report forward verbatim from iter_3.
2. Applied correction C8 (SIG peer generation cost: $0.000116/candidate).
3. Appended iteration 4 sections covering five artifacts:
   - Experiment 9 (T6-E): CSC on held-out E — sharp negative result (anchoring).
   - Experiment 10 (T6-P): CSC on PERTURB — budget exhausted; zero-cost arms.
   - Dataset 4: E2 confirmation set — partial (30/550 sentences).
   - Dataset 5: R_COMP FREE name-free labels — search-only (gloss pending).
   - Evaluation 3: T8 vocabulary analysis — 64 claims verified.
4. Updated "What we have learned so far", Related Work ([19]-[26]), References.
5. Ran the REVISION_CHECKLIST pass; fixed reference [19] author name.
6. Built `references.bib` via Semantic Scholar / OpenAlex + manual fallbacks.
7. Emitted structured JSON output with 7 figure specs.

## File layout

| File | Description |
|---|---|
| `paper_draft.md` | Full report, iterations 1-4 (~1411 lines) |
| `references.bib` | BibTeX for references [1]-[26] |
| `.terminal_claude_agent_struct_out.json` | Structured output (title, abstract, figures, summary) |
| `style_exemplars.md` | Writing style exemplars from related papers |
| `domain_terms.json` | Project terminology glossary (98 entries) |
| `.aii/manifest.yaml` | Workspace manifest |
| `README.md` | This file |

## How to use

The report is plain Markdown. `[ARTIFACT:id]` markers link claims to
source artifacts. `[FIGURE:fig_id]` markers indicate figure placement;
figure specs are in the JSON output's `figures` array. References use
numbered `[n]` citations matching the `## References` section and
`references.bib`.

No code to run — this is a text-generation step. The structured output
(`.terminal_claude_agent_struct_out.json`) is consumed by the pipeline's
next steps.
