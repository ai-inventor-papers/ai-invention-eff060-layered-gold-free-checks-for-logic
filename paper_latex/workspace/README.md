# Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for NL→FOL Translation

A preliminary study evaluating cross-family solver consensus as a gold-free metric for NL-to-first-order-logic translation faithfulness.

## Layout

- `paper.tex` — LaTeX source (11pt, letterpaper, single-column)
- `paper.pdf` — Compiled PDF (12 pages)
- `references.bib` — BibTeX bibliography (13 cited entries, fetched via Semantic Scholar)
- `references.json` — Fetch record for each bibliography entry
- `figures/` — Pre-generated vector figures (PDF)
  - `fig_dev_auroc_v0.pdf` — Development-set AUROC comparison bar chart
  - `fig_complexity_v0.pdf` — Consensus degradation by sentence-length tercile
  - `fig_k_curve_v0.pdf` — AUROC vs number of peer families
- `.aii/manifest.yaml` — Asset manifest (no heavy files to manage)

## Compilation

```bash
pdflatex -interaction=nonstopmode paper.tex
/usr/bin/bibtex.original paper
pdflatex -interaction=nonstopmode paper.tex
pdflatex -interaction=nonstopmode paper.tex
```

Note: `bibtex` may not be in PATH on this system; use `/usr/bin/bibtex.original`.

## Restoring removed files

No files were marked for deletion; all workspace files are under the 10 MB auto-keep floor.
