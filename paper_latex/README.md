# Cross-Family Solver Consensus for Logic Translation Evaluation

Public web page for the paper "Cross-Family Solver Consensus Outperforms LLM Judges for Logic Translation Evaluation."

## What this is

A single self-contained HTML page (`index.html`) presenting the paper's findings. It is published as the run's GitHub Pages site.

## Layout

```
index.html          — the web page (all CSS/JS inline, no external deps)
interactive.html    — explorable views over the run's per-item scores (data embedded inline; linked from index.html)
paper.tex           — the paper source (read-only, not modified)
paper.pdf           — the compiled paper (read-only)
references.bib      — bibliography (read-only)
references.json     — bibliography in JSON (read-only)
figures/
  fig1_v0.pdf       — Figure 1: consensus vs baselines (vector, for LaTeX)
  fig1_v0.png       — Figure 1: rendered at 200 DPI for the web page
  fig3_v0.pdf       — Figure 3: per-stratum AUROC comparison (vector)
  fig3_v0.png       — Figure 3: rendered at 200 DPI
  fig4_v0.pdf       — Figure 4: k-family saturation curve (vector)
  fig4_v0.png       — Figure 4: rendered at 200 DPI
  fig*_spec.json    — figure generation specs (read-only)
workspace/          — LaTeX build scratch (not used by the page)
.aii/manifest.yaml  — disposable-output manifest (no heavy files)
```

## How to view

Open `index.html` in any browser. It renders offline with no build step, no bundler, and no network requests. The only external references are links to the paper PDF, code repository, and research reports on cdn.jsdelivr.net and github.com.

## How it was built

1. Read `paper.tex` to extract the title, contributions, headline numbers, and method description.
2. Rendered PDF figures to PNG at 200 DPI with `pdftoppm`.
3. Wrote `index.html` with inline CSS and JavaScript, system font stack, responsive layout (360px phone to wide desktop), lightbox for figure enlargement, sticky section navigation, and keyboard accessibility.
4. Verified every number on the page against `paper.tex`.
5. Screenshotted at phone (375px) and desktop (1280px) widths with Playwright/Chromium.
6. Ran an accessibility pass: heading hierarchy, alt text, focus management, ARIA landmarks.

## Restoring removed files

No files were marked for deletion. Nothing needs restoring.
