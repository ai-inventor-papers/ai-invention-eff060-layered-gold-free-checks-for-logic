# Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for NL-to-FOL Translation

## What this repository contains

A research paper evaluating cross-family solver consensus as a reference-free metric for detecting errors in natural-language to first-order logic translations.

## Layout

| Path | Description |
|---|---|
| `paper.tex` | LaTeX source for the paper |
| `paper.pdf` | Compiled PDF (15 pages) |
| `references.bib` | BibTeX bibliography (37 entries from Semantic Scholar) |
| `references.json` | Fetch record for bibliography entries |
| `figures/fig2_v0.pdf` | Figure 1: Consensus vs. LLM judges on held-out data (bar chart) |
| `figures/fig3_v0.pdf` | Figure 2: Consensus advantage by sentence complexity (strata) |
| `figures/fig4_v0.pdf` | Figure 3: Error scatter vs. correct convergence (histogram) |

## How to compile

```bash
pdflatex -interaction=nonstopmode paper.tex
bibtex paper
pdflatex -interaction=nonstopmode paper.tex
pdflatex -interaction=nonstopmode paper.tex
```

Requires a TeX Live installation with `pdflatex`, `bibtex`, and the `natbib` package.

## Restoring removed files

No files were marked for deletion; all outputs are under 10 MB.
