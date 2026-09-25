# gen_report_doc — report_results

> Phase: `gen_paper_repo` · `gen_full_paper`
> Run: `gen_paper_repo_a2e1d024cc16` — Gold-Free Faithfulness Metrics for NL-to-FOL Translation
>
> Full, verbatim record of every prompt the AI Inventor pipeline gave this agent — system-user, human-user and skill-input — in the order they landed. Nothing truncated.

## Task: `gen_report_doc` (terminal_claude_agent)

### [1] SYSTEM-USER prompt · 2026-09-24 23:23:49 UTC

````
continue

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "ReportDocExpectedFiles": {
      "description": "All expected output files from report generation.",
      "properties": {
        "report_tex_path": {
          "description": "Path to the report's LaTeX source. Example: 'report.tex'",
          "title": "Report Tex Path",
          "type": "string"
        },
        "report_pdf_path": {
          "description": "Path to the compiled report PDF. Example: 'report.pdf'",
          "title": "Report Pdf Path",
          "type": "string"
        }
      },
      "required": [
        "report_tex_path",
        "report_pdf_path"
      ],
      "title": "ReportDocExpectedFiles",
      "type": "object"
    }
  },
  "description": "The typeset research report \u2014 structured output from the report task.",
  "properties": {
    "title": {
      "description": "Title of the report document. Plain and descriptive of what the run investigated; it is an internal record, not a paper title.",
      "maxLength": 120,
      "minLength": 12,
      "title": "Title",
      "type": "string"
    },
    "coverage_note": {
      "description": "What the report covers, stated so a reader can check it: how many iterations it narrates, how many artifacts it walks through, how many result tables it typesets, and anything named in the inputs that you could NOT include, with the reason. Never a summary of the findings.",
      "maxLength": 4000,
      "minLength": 200,
      "title": "Coverage Note",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/ReportDocExpectedFiles",
      "description": "All output files you created. Must include report.tex and report.pdf."
    }
  },
  "required": [
    "title",
    "coverage_note",
    "out_expected_files"
  ],
  "title": "ReportDoc",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [2] HUMAN-USER prompt · 2026-09-24 23:23:49 UTC

```
I work on converting natural-language text into first-order logic (NL→FOL, autoformalization) with
LLM pipelines. Evaluation is the bottleneck. Correct FOL for a sentence is not unique — different
predicate names, different decompositions of the same concept, and logically equivalent rewrites can
all be correct. Gold FOL annotations are rare and expensive. The metrics in use either need a gold
formula (exact match, BLEU, prover-checked equivalence to the gold) or only check that the output
parses. In my own pilot I used cheap structural metrics: whether a set of generated formulas loads
together without conflicts, whether predicate arities stay consistent, how many predicates are used
but never defined, and how similar the predicate sets are across reruns. Those measure stability and
composability, not whether a formula says what the sentence says.

Find new metrics for NL→FOL output quality. Operating situation: you are given a natural-language
sentence (or short passage) and a candidate FOL formalization produced by any system. There is no gold
formula, no ontology or controlled vocabulary, and no domain knowledge. The metric returns a score
that predicts whether the formalization is faithful to the text, and ideally which kind of error it
contains (quantifier or scope error, dropped or added condition, negation/polarity error, swapped
arguments, conflated or wrongly split concepts). Metrics may score a single formula or a set (several
samples for one sentence, or the formalizations of all sentences in one document). They must be
task-agnostic — usable for any NL→FOL setting, not tied to a domain, dataset or pipeline — and cheap
enough to run on every output (solver calls and small models are fine; a large-LLM judge per formula
only if shown to earn its cost).

Requirements:
- Keep the target fixed: the metric must predict faithfulness to the text. Detecting synthetic
  perturbations, parse validity, or run-to-run stability are not substitutes for that target.
- Validate against ground truth, never against the metric itself. Use public datasets with gold
  sentence-level FOL (e.g. FOLIO, MALLS, or others you find) to build a meta-evaluation set: real
  candidate formalizations from several different systems, plus controlled perturbations of gold
  formulas with known error types, labelled via prover-checked equivalence to gold. Handle two known
  problems: some gold annotations are wrong, and a candidate can be correct without being equivalent
  to the gold (different vocabulary or granularity). Estimate how often each happens and how it
  biases the labels. These datasets are public, so check whether LLM-based metrics benefit from having
  seen the gold.
- For each metric report: correlation with correctness at item and system level; sensitivity per error
  type; invariance under meaning-preserving rewrites (variable/predicate renaming, reordering,
  equivalent restatements); coverage — unparseable outputs are counted and reported, never silently
  dropped; and cost.
- Compare against baselines: parse/compile rate, round-trip (FOL→NL→compare) similarity,
  LLM-as-judge, sampling self-consistency, and the structural consistency metrics described above. A
  new metric matters only if it adds signal those don't.
- Report how each metric's reliability changes with sentence complexity (length, number of quantifiers,
  nesting depth, number of conditions and exceptions). Long, heavily conditioned sentences matter most
  to me.
- Negative results are welcome: if a family of metrics does not track correctness, show that clearly.

Out of scope: comparing grounded vs ungrounded generation (ontology vocabulary injected into prompts),
anything that depends on a particular ontology, and building a better NL→FOL translator. The
contribution is the measurement, not the translator.

Deliverables: reusable Python functions taking (text, fol) — or a set of such pairs — each with a
precise statement of what it measures; the meta-evaluation dataset with its labels; and the results.

I appended a pilot study of this problem with some metrics I already used but haven't verified. Just for reference.
```

### [3] SKILL-INPUT — aii-paper-to-latex · 2026-09-24 23:24:11 UTC

The agent loaded the **aii-paper-to-latex** skill; its `SKILL.md` (the instructions injected into the agent's context) follows verbatim.

````
---
name: aii-paper-to-latex
description: "Assembles and compiles a LaTeX paper into paper.pdf: documentclass and package preamble, figure floats that includegraphics pre-generated vector .pdf and .jpg files, float-placement and width rules, and the required pdflatex, bibtex, pdflatex, pdflatex run sequence. Use whenever pre-written text and pre-generated figures must become a compiled PDF, and whenever a build misbehaves — citations printing as question marks, figures drifting to the end or above the title, shrunken axis labels, undefined references. Triggers: latex, tex, pdflatex, bibtex, natbib, includegraphics, figure float, htbp, compile or build the paper, paper.tex, paper.pdf. NOT for: writing the paper's text or deciding its structure (use aii-paper-writing), creating the figure images (aii-data-fig-gen, aii-concept-fig-gen), or fetching bibliography entries (use aii-semscholar-bib); NOT for reshaping a PDF that already exists — merging, splitting, form filling, table extraction (use anthropic-pdf)."
---

## LaTeX Paper Assembly

Assembles a research paper from paper text, pre-generated figures (vector `.pdf` for data figures, `.jpg` for concept figures) and a bibliography into a compiled PDF.

### Document Setup

```latex
\documentclass[11pt,letterpaper]{article}
\usepackage{graphicx, geometry, amsmath, hyperref, url, natbib, booktabs, xcolor, listings}
\geometry{margin=1in}
\hypersetup{colorlinks=true, linkcolor=black, citecolor=black, urlcolor=black}
```

### Figure Inclusion

CRITICAL: Include ALL figures. Every figure MUST appear in the paper.

```latex
\begin{figure}[!htbp]
  \centering
  \includegraphics[width=\linewidth,height=0.85\textheight,keepaspectratio]{figures/filename.pdf}
  \caption{Descriptive caption.}
  \label{fig:label}
\end{figure}
```

Rules:
- ALWAYS `[!htbp]` — all four options, so a float can never be deferred to the end of the
  document, which `[t]` or `[h]` alone risks. Do not ask for a page TOP: `[!t]` and
  `[!tbp]` both floated a figure ABOVE the paper's own title on page 1, where `[!htbp]`
  on the same document did not. Where a figure lands is decided by where it is declared
  in the text
- Use `figure`, never `figure*`. This document class is ONE column, so `figure*` is exactly
  as wide as `figure` (469.76pt either way) and gains nothing, while restricting the float
  to a page top
- ALWAYS constrain with `width` and `keepaspectratio`. Add `height` only as a
  LAST RESORT against a very tall figure overrunning the page, and keep it
  generous — `0.85\textheight`. A tight height cap binds on ordinary figures
  and LaTeX then shrinks the TEXT with them: at `0.4\textheight` a square
  figure printed at 50.9%, putting 11 pt axis labels on the page at 5.6 pt.
  The figure generator measures legibility at the figure's OWN size, so it
  cannot see this happen
- Every figure needs `\caption`, `\label`, and a `\ref` in the text
- Do NOT convert figures to tables or describe them without inserting the image
- Do NOT skip any figures

### Compilation Process

Run each command separately (do NOT chain with `&&` — pdflatex often exits non-zero on warnings, which would skip bibtex and leave citations as `??`):

```bash
pdflatex -interaction=nonstopmode paper.tex
bibtex paper
pdflatex -interaction=nonstopmode paper.tex
pdflatex -interaction=nonstopmode paper.tex
```

All four commands are required. Skipping bibtex causes `??` in all citations.
Fix any errors between runs. Verify `./paper.pdf` was created.

### Output Files

- `./paper.tex` — LaTeX source
- `./references.bib` — bibliography file
- `./paper.pdf` — compiled PDF
- `./figures/` — all figure images (pre-generated, copied into workspace). Data
  figures are `.pdf` (vector — LaTeX renders their text at page resolution, which
  is what keeps axis labels sharp in print); concept figures are `.jpg`. Use each
  file's OWN extension in `\includegraphics`; there is no conversion step.
````
