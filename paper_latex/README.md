# Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for NL-to-Logic Translation

This directory contains the assembled paper and its public-facing web page.

## Layout

| Path | Description |
|------|-------------|
| `index.html` | Self-contained public web page (GitHub Pages site) |
| `interactive.html` | Self-contained interactive explainer built from the run's per-candidate results (no external dependencies) |
| `paper.tex` | LaTeX source of the paper |
| `paper.pdf` | Compiled paper PDF |
| `references.bib` | Bibliography |
| `references.json` | Structured reference data |
| `figures/` | All figures (PDF originals + PNG renders for the web) |
| `workspace/` | LaTeX compilation scratch (ignorable) |

## Running

The web page is a single `index.html` file with no build step and no external dependencies. Open it directly in a browser, or serve with any static file server:

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

The page references figures via relative paths (`figures/*.png`), so the `figures/` directory must be served alongside it.

## Restoring removed files

The `workspace/` directory contains LaTeX build artifacts and can be regenerated:

```bash
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex
```
