# gen_paper_site — report_results

> Phase: `gen_paper_repo` · `gen_full_paper`
> Run: `gen_paper_repo_a2e1d024cc16` — Gold-Free Faithfulness Metrics for NL-to-FOL Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_paper_site` (terminal_claude_agent, claude-opus-4-6)

### [1] CONFIG · 2026-09-25 09:30:59 UTC

```
model: claude-opus-4-6 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-25 09:31:31 UTC

````
continue

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "PaperSiteExpectedFiles": {
      "description": "All expected output files from paper-site generation.",
      "properties": {
        "site_html_path": {
          "description": "Path to the single self-contained HTML page. Example: 'index.html'",
          "title": "Site Html Path",
          "type": "string"
        }
      },
      "required": [
        "site_html_path"
      ],
      "title": "PaperSiteExpectedFiles",
      "type": "object"
    }
  },
  "description": "Paper site \u2014 structured output from presentation-page generation.",
  "properties": {
    "summary": {
      "description": "Brief summary of the page you built: the sections it carries, which figures it shows, which numbers it quotes and where each came from in the paper.",
      "maxLength": 5000,
      "minLength": 300,
      "title": "Summary",
      "type": "string"
    },
    "out_expected_files": {
      "$ref": "#/$defs/PaperSiteExpectedFiles",
      "description": "All output files you created. Must include index.html."
    }
  },
  "required": [
    "summary",
    "out_expected_files"
  ],
  "title": "PaperSite",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.

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
````

### [3] SYSTEM-USER prompt · 2026-09-25 09:33:21 UTC

```
This session is being continued from a previous conversation that ran out of context. The summary below covers the earlier portion of the conversation.

Summary:
1. Primary Request and Intent:
   The user's task across three run directories was to build a paper's public web page: ONE self-contained `index.html` that presents a research paper ("Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for NL-to-FOL Translation") faster than reading the PDF, published as a GitHub Pages site. The page must be fully self-contained (all CSS/JS inline, no external scripts, stylesheets, web fonts, or resources fetched at load time), responsive, keyboard accessible, with dark mode support. Additionally, three supporting files must be created: `.terminal_claude_agent_struct_out.json` (with a specific JSON schema including `site_html_path`), `.aii/manifest.yaml` (with `entries:` list format), and `README.md`. The task was completed across three runs (run_u75jRHUss0zo, run_-tTYmHVAOMOt, run_cNhUBrixEdz7), each with a slightly different paper version but the same structure. The JSON schema requires `site_html_path: "index.html"` (not `page_html_path`).

2. Key Technical Concepts:
   - NL-to-FOL (Natural Language to First-Order Logic) translation evaluation
   - Cross-family solver consensus as a gold-free faithfulness metric
   - Stratified AUROC as evaluation metric
   - Z3 SMT solver for logical equivalence checking
   - Predicate alignment (structural cost, text-anchor cost, semantic signature)
   - Endorsement rate (e) and divergence rate (d) decomposition
   - Rename tradeoff (false-alarm vulnerability under predicate renaming)
   - Self-contained HTML/CSS/JS single-page design
   - System font stacks (no external fonts allowed)
   - IntersectionObserver for scroll-based section highlighting
   - Lightbox with keyboard accessibility (focus trap, Escape close)
   - CSS custom properties for dark/light theming
   - pymupdf for PDF-to-PNG figure rendering
   - Playwright for headless browser testing

3. Files and Code Sections:
   - `/ai-inventor/aii_data/runs/run_cNhUBrixEdz7/4_gen_paper_repo/_4_assemble_paper/paper/paper.tex`
     - Source of truth for all numbers (444 lines). Title: "Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for Natural-Language-to-First-Order-Logic Translation". Author: "Anonymous". Contains 4 figures (including fig_sig_tercile_v0 new to this version), 6 tables, 11 footnote URLs, 8 limitations, 29 key numbers verified.

   - `/ai-inventor/aii_data/runs/run_cNhUBrixEdz7/4_gen_paper_repo/_4_assemble_paper/paper/index.html`
     - The main deliverable (38.5KB). Complete self-contained HTML with:
       - Full HTML document structure (DOCTYPE, html, head, body)
       - `[hidden] { display: none !important; }` rule
       - System serif font stack: `'Iowan Old Style', 'Palatino Linotype', Palatino, Georgia, serif`
       - CSS custom properties for theming with dark mode support
       - Green accent color (#1a6b4a light / #4cc88a dark)
       - Hero with 3 links using exact CDN/GitHub URLs
       - 4 contribution cards, method section, 6 results tables, 3 big-number tiles
       - 4 figures with lightbox (lightbox img has valid default src: `figures/fig_dev_auroc_v0.png`)
       - 22 code artifact links (11 from paper footnotes + 11 additional required links)
       - Footer with CDN paper/report links and citation
       - Sticky side nav (desktop) / horizontal scroll nav (mobile)
       - IntersectionObserver-based active section highlighting
       - Lightbox with `removeAttribute('src')` on close

   - `/ai-inventor/aii_data/runs/run_cNhUBrixEdz7/4_gen_paper_repo/_4_assemble_paper/paper/.terminal_claude_agent_struct_out.json`
     - Valid JSON matching required schema with `site_html_path: "index.html"` and 2,167-char summary

   - `/ai-inventor/aii_data/runs/run_cNhUBrixEdz7/4_gen_paper_repo/_4_assemble_paper/paper/.aii/manifest.yaml`
     - `entries: []` (all files under auto-keep floor)

   - `/ai-inventor/aii_data/runs/run_cNhUBrixEdz7/4_gen_paper_repo/_4_assemble_paper/paper/README.md`
     - Repository description with layout table, viewing instructions

   - `figures/fig_dev_auroc_v0.png` (79KB), `figures/fig_sig_tercile_v0.png` (54KB), `figures/fig_complexity_v0.png` (59KB), `figures/fig_k_curve_v0.png` (70KB)
     - All 4 PNGs rendered from PDF originals using pymupdf at 2.5x matrix
     - fig_sig_tercile_v0.pdf was copied from workspace/figures/ since it wasn't in figures/

4. Errors and fixes:
   - **Lightbox empty src (run_u75jRHUss0zo)**: Verifier flagged `src=""` as not starting with `figures/`. First fix (removing src attribute entirely) didn't satisfy verifier. Final fix: set `src="figures/fig_dev_auroc_v0.png"` as default and use `removeAttribute('src')` on close.
   - **Manifest format (run_u75jRHUss0zo)**: Verifier required `entries:` list, not `files:` list. Then all entries were flagged as "nothing that needs a decision" (under auto-keep floor). Final fix: `entries: []`.
   - **Lightbox intercepting clicks (run_-tTYmHVAOMOt)**: Playwright showed hidden lightbox overlay intercepting pointer events. Fixed by adding `[hidden] { display: none !important; }` CSS rule and proper HTML document structure (DOCTYPE, html, head, body tags).
   - **15 verification failures (run_-tTYmHVAOMOt)**: Google Fonts external resource, wrong paper/report/repo URLs, 10 missing artifact links. Fixed by removing Google Fonts (switched to system serif), using exact CDN URLs for paper/report, full GitHub URL for repo, and adding all required artifact links.
   - **Missing pymupdf/playwright**: Installed with pip on each new run environment.
   - **Missing fig_sig_tercile_v0.pdf (run_cNhUBrixEdz7)**: PDF existed in workspace/figures/ but not in figures/. Copied it before rendering.

5. Problem Solving:
   All problems were solved across the three runs. The final run (run_cNhUBrixEdz7) incorporated all lessons learned and produced a clean build with no verification failures. Key lessons applied: no external resources, exact CDN/GitHub URLs, all 22 artifact links, proper HTML structure, valid lightbox src, system fonts only, empty manifest entries list.

6. All user messages:
   - (Initial context from compacted conversation about run_u75jRHUss0zo - completing 3 remaining files)
   - "SITE VERIFICATION FAILED: 1 problem(s) in index.html. - image source '' does not start with 'figures/'..." (with instructions to fix, keep self-contained, point images at figures/, re-open and confirm)
   - "SITE VERIFICATION FAILED: 1 problem(s) in index.html. - image source '' does not start with 'figures/'..." (same error persisted after first fix)
   - "CRITICAL_ERROR: The module-end file check FAILED (attempt 1/3). PROBLEMS: .aii/manifest.yaml has no top-level 'entries:' list" (with manifest format instructions)
   - "CRITICAL_ERROR: The module-end file check FAILED (attempt 2/3). PROBLEMS: [9 entries] matches nothing that needs a decision — remove it"
   - (New run_-tTYmHVAOMOt) "continue" with JSON schema and full research prompt about NL→FOL metrics
   - "SITE VERIFICATION FAILED: 15 problem(s) in index.html" listing: Google Fonts external fetch, missing report.pdf link, wrong paper.pdf link, wrong code repo link, 10 missing artifact links with exact URLs and labels
   - (New run_cNhUBrixEdz7) "continue" with same JSON schema and research prompt
   - "continue where you left off — reuse any partial work already written to disk. Do NOT start over."
   - "continue where you left off — reuse any partial work already written to disk. Do NOT start over."
   - Security constraint from CLAUDE.md: "Do not print or save the key" (referring to shared OpenRouter API key with $50 daily limit)

7. Pending Tasks:
   - None. All deliverables for run_cNhUBrixEdz7 are complete and validated.

8. Current Work:
   The most recent work was confirming that all deliverables for run_cNhUBrixEdz7 are complete. The user sent "continue where you left off" twice, and both times I verified everything was already done: index.html (38.5KB, tested with Playwright), .terminal_claude_agent_struct_out.json (valid JSON, 2167 chars, site_html_path: "index.html"), .aii/manifest.yaml (entries: []), README.md, and 4 PNG figures. The last validation output confirmed all files exist and the struct out JSON is valid.

9. Optional Next Step:
   No next step needed. All deliverables are complete and validated. The task is finished unless the user requests changes or the site verifier reports issues.

If you need specific details from before compaction (like exact code snippets, error messages, or content you generated), read the full transcript at: /root/.claude/projects/-ai-inventor-aii-data-runs-run-Jhw6i0bFXdo3-4-gen-paper-repo--4-assemble-paper-paper/bf7fe44a-e441-4da9-8474-86e4d0bfd56a.jsonl
Continue the conversation from where it left off without asking the user any further questions. Resume directly — do not acknowledge the summary, do not recap what was happening, do not preface with "I'll continue" or similar. Pick up the last task as if the break never happened.
```

### [4] ASSISTANT · 2026-09-25 09:33:33 UTC

```
New run directory — let me check what's already on disk and read the paper.
```

### [5] TOOL CALL — Bash · 2026-09-25 09:33:33 UTC

```
List files in the new run's paper directory:
ls -la /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/ && echo "---" && ls -la /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/figures/ 2>/dev/null || echo "No figures dir"
```

### [6] TOOL RESULT — Bash · 2026-09-25 09:33:33 UTC

```
{"stdout": "total 6424\ndrwxr-xr-x 5 root root 2000144 Sep 25 09:30 .\ndrwxr-xr-x 5 root root 2000428 Sep 25 09:26 ..\ndrwxr-xr-x 2 root root       1 Sep 25 09:30 .aii\n-rw------- 1 root root      54 Sep 25 09:30 .aii_claude_session.json\n-rw-r--r-- 1 root root   94937 Sep 25 09:33 .repl_agent.ptylog\ndrwxr-xr-x 2 root root 1007061 Sep 25 09:30 figures\n-rw-r--r-- 1 root root  330422 Sep 25 09:30 paper.pdf\n-rw-r--r-- 1 root root   36278 Sep 25 09:30 paper.tex\n-rw-r--r-- 1 root root    5651 Sep 25 09:30 references.bib\n-rw-r--r-- 1 root root    4154 Sep 25 09:30 references.json\ndrwxr-xr-x 4 root root 1094788 Sep 25 09:30 workspace\n---\ntotal 3010\ndrwxr-xr-x 2 root root 1007061 Sep 25 09:30 .\ndrwxr-xr-x 5 root root 2000144 Sep 25 09:30 ..\n-rw-r--r-- 1 root root    3170 Sep 25 09:30 fig_complexity_spec.json\n-rw-r--r-- 1 root root   21257 Sep 25 09:30 fig_complexity_v0.pdf\n-rw-r--r-- 1 root root    3885 Sep 25 09:30 fig_dev_auroc_spec.json\n-rw-r--r-- 1 root root   21556 Sep 25 09:30 fig_dev_auroc_v0.pdf\n-rw-r--r-- 1 root root    2574 Sep 25 09:30 fig_k_curve_spec.json\n-rw-r--r-- 1 root root   19867 Sep 25 09:30 fig_k_curve_v0.pdf", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [7] TOOL CALL — Bash · 2026-09-25 09:33:33 UTC

```
Check if .aii directory exists:
ls -la /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/.aii/ 2>/dev/null || echo "No .aii dir"
```

### [8] TOOL RESULT — Bash · 2026-09-25 09:33:33 UTC

```
{"stdout": "total 1954\ndrwxr-xr-x 2 root root       1 Sep 25 09:30 .\ndrwxr-xr-x 5 root root 2000144 Sep 25 09:30 ..", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [9] ASSISTANT · 2026-09-25 09:33:43 UTC

```
No index.html yet. This run has 3 figure PDFs (no fig_sig_tercile). Let me read the paper and check workspace.
```

### [10] TOOL CALL — Read · 2026-09-25 09:33:43 UTC

```
/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/paper.tex
```

### [11] TOOL RESULT — Read · 2026-09-25 09:33:43 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/paper.tex", "content": "\\documentclass[11pt,letterpaper]{article}\n\\usepackage{graphicx, geometry, amsmath, amssymb, hyperref, url, natbib, booktabs, xcolor, listings}\n\\geometry{margin=1in}\n\\hypersetup{colorlinks=true, linkcolor=black, citecolor=black, urlcolor=black}\n\n\\title{Pre-Registered Cross-Family Solver Consensus Outperforms LLM Judges\\\\on Templated NL-to-FOL Translation with a Supplied Predicate Signature}\n\n\\author{Anonymous}\n\\date{}\n\n\\begin{document}\n\\maketitle\n\n\\begin{abstract}\nEvaluating the faithfulness of natural-language-to-first-order-logic (NL$\\to$FOL) translations is hampered by the expense and unreliability of gold-standard references: recent audits find that roughly 40\\% of annotations in standard benchmarks contain errors.\nWe study a gold-free alternative based on cross-family solver consensus: collect translations of the same sentence from multiple independent LLM families, check pairwise equivalence with an SMT solver, and score each candidate by the fraction of cross-family peers that disagree with it.\nIn a pre-registered evaluation on 221~templated long-exception sentences with a supplied predicate signature, consensus achieves a within-template AUROC of 0.954 versus 0.587 for a disguised API judge ($\\Delta = +0.367$ [+0.328, +0.404]), flat across word-length terciles, passing the pre-registered criterion.\nUnder free (independently chosen) vocabulary, consensus still outperforms judges on both development data ($\\Delta = +0.099$) and untouched out-of-sample sentences ($\\Delta = +0.171$, original-view judge), but the advantage shrinks by roughly 0.15~AUROC and a fundamental rename tradeoff emerges: any predicate-name alignment needed to compare independently generated formulas produces a high false-alarm rate on meaning-preserving renames.\nConfirmation on independent held-out data was budget-stopped and remains incomplete.\nWe present these results, identify the conditions under which shared versus free vocabulary governs metric strength, and release the full evaluation code.\n\\end{abstract}\n\n\\section{Introduction}\n\nTranslating natural-language sentences into first-order logic (NL$\\to$FOL) is a core task in computational semantics and formal verification~\\citep{Yang2023,Han2022}.\nA correct translation must faithfully capture the meaning of the source sentence: its quantifier scope, polarity, argument structure, and exception clauses.\nEvaluating faithfulness is difficult because the same sentence admits many logically equivalent formalizations that differ in predicate names, variable bindings, and structural layout.\n\nGold-standard references are the default evaluation method, but they are expensive and often wrong.\n\\citet{Brunello2026} audit two standard benchmarks and find 39--42\\% of their annotations contain errors.\nThis unreliability is not just noise: when the gold reference itself is unfaithful, every metric calibrated against it is miscalibrated.\n\nAn alternative is to have a strong LLM judge each translation~\\citep{Chiang2024}.\nHowever, LLM judges share failure modes with the translators they evaluate: both are autoregressive models operating on the same distributional statistics, so systematic blind spots tend to be correlated.\nAs we show in Section~\\ref{sec:sig_results}, a cheap disguised judge achieves only 0.587 AUROC on the same sentences where consensus reaches 0.954.\n\nWe study a gold-free metric based on cross-family solver consensus.\nThe idea is simple: if a candidate translation is correct, translations produced independently by other LLM families should be logically equivalent to it.\nIf the candidate is wrong, independent translators are unlikely to make the same mistake, so their translations will diverge.\nWe formalise this intuition and evaluate it under two vocabulary regimes:\n\\begin{enumerate}\n\\item \\textbf{Shared signature}: all translators use a supplied predicate vocabulary. Equivalence checking requires no alignment and labels come from Z3 alone.\n\\item \\textbf{Free vocabulary}: each translator chooses its own predicate names. Equivalence checking requires a predicate-name aligner, which introduces a rename tradeoff (Section~\\ref{sec:rename}).\n\\end{enumerate}\n\nOur contributions:\n\\begin{itemize}\n\\item A pre-registered evaluation on 221 long-exception sentences under shared signature: consensus AUROC 0.954 versus 0.587 for the disguised judge ($\\Delta = +0.367$ [+0.328, +0.404]), flat across word-length terciles, and 0.956 versus 0.932 for a frontier judge on a descriptive 60-row subsample (Section~\\ref{sec:sig_results}). This dataset later served as development data for aligner tuning; the templates and supplied signature limit its scope.\n\\item Free-vocabulary evaluation on development set~$E$: consensus outperforms judges by $\\Delta = +0.099$ [+0.049, +0.146] on stratified AUROC, with aligner-free consensus (c\\_exact) at 0.689 [0.652, 0.726] (Section~\\ref{sec:dev_results}).\n\\item Untouched free-vocabulary out-of-sample results on R\\_COMP FREE under provisional labels: $\\Delta = +0.171$ [+0.135, +0.206] versus the original-view judge; $\\Delta = +0.105$ [+0.011, +0.215] on a two-auditor subset; consensus reaches 0.94 of the frontier judge's AUROC (Section~\\ref{sec:free_oos}).\n\\item Documentation of the rename tradeoff: a 76.5\\% false-alarm rate under nonce predicate renames that no variant we tested could eliminate without sacrificing error recall (Section~\\ref{sec:rename}).\n\\end{itemize}\n\n\\begin{figure}[!htbp]\n  \\centering\n  \\includegraphics[width=\\linewidth,height=0.85\\textheight,keepaspectratio]{figures/fig_dev_auroc_v0.pdf}\n  \\caption{Stratified AUROC on the free-vocabulary development dataset for the main metrics and baselines. Error bars are 95\\% sentence-cluster bootstrap confidence intervals. Consensus-based metrics (blue) outperform API judges (orange) and other gold-free baselines (gray).}\n  \\label{fig:dev_auroc}\n\\end{figure}\n\n\\section{Related Work}\n\n\\paragraph{NL\\texorpdfstring{$\\to$}{-to-}FOL evaluation.}\nStandard benchmarks such as FOLIO~\\citep{Han2022} and the MALLS corpus~\\citep{Yang2023} provide NL--FOL pairs, but gold-annotation error rates are high~\\citep{Brunello2026}.\n\\citet{Vossel2025} map predicates by normalised Levenshtein distance before equivalence checking.\n\\citet{Thatikonda2025} evaluate n-gram, graph, embedding, and LLM-based closeness metrics on controlled FOL perturbations, finding that no single metric is sensitive to all perturbation types.\n\n\\paragraph{Cross-model consensus.}\nThe idea of using agreement among multiple independently trained models as a quality signal appears in several domains.\n\\citet{Wang2022} show that sampling multiple chain-of-thought reasoning paths~\\citep{Wei2022} from a single model and taking the majority answer (self-consistency) improves accuracy.\n\\citet{Bayless2025} collect $k$ translations over a fixed shared schema and score each by the fraction of $k$ translations that entail it.\n\\citet{Zhang2023} detect hallucinations in black-box LLMs by sampling diverse perturbations of a query and checking consistency across answers.\nOur work differs from these in evaluating the consensus score under both shared and free vocabulary, head-to-head with API judges, with pre-registered analyses.\n\n\\paragraph{LLM-as-judge.}\n\\citet{Chiang2024} propose using LLMs as evaluators.\nIn NL$\\to$FOL, an LLM judge reads the sentence and the candidate formula and predicts faithfulness.\nThe disguised variant (nonce predicate names) controls for memorisation of known benchmarks.\n\n\\paragraph{Diverse redundancy.}\nN-version programming, where independent implementations of the same specification are compared by majority vote, was proposed for software fault tolerance.\n\\citet{Eckhardt1985} predict that coincident failures rise with input difficulty; our finding that the consensus advantage is flat with sentence length under shared vocabulary but degrades under free vocabulary is consistent with vocabulary alignment, not input difficulty, as the bottleneck.\n\n\\section{Method}\\label{sec:method}\n\n\\subsection{Consensus scoring}\n\nGiven a sentence $s$ and a candidate FOL translation $c$, we collect peer translations $\\{p_1, \\ldots, p_k\\}$ from $k$ independent LLM families.\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-1}}\nEach peer uses the same few-shot prompt but a different base model (e.g., one from each of Gemini, Claude, GPT, Llama, Qwen, Phi, Mistral).\nWe compute:\n\\begin{equation}\n\\text{c\\_score}(c, s) = 1 - \\frac{1}{k} \\sum_{i=1}^{k} \\mathbf{1}[\\text{equiv}(c, p_i)]\n\\end{equation}\nwhere $\\text{equiv}(c, p_i)$ checks logical equivalence between $c$ and $p_i$ using the Z3 SMT solver~\\citep{Moura2008}.\n\nUnder \\textbf{shared signature} (c\\_score\\_sig), all translators use a supplied predicate vocabulary, and equiv is a direct Z3 check after case-insensitive symbol normalisation.\nUnder \\textbf{free vocabulary} (c\\_score\\_align), each translator chooses its own predicate names, and equiv requires a predicate-name aligner before the Z3 check.\n\n\\subsection{Predicate alignment (free vocabulary only)}\n\nIndependent translators choose different predicate names for the same concept (e.g., \\texttt{Runs(x)} vs.\\ \\texttt{IsRunner(x)}).\nTo compare formulas across families, we align predicates using a cost function that combines:\n\\begin{enumerate}\n\\item \\textbf{Structural cost}: polarity profile, argument-count match, and nesting depth.\n\\item \\textbf{Text-anchor cost}: overlap between predicate-name words and source-sentence tokens (Porter stemming, WordNet synonyms/derivations).\n\\item \\textbf{Semantic signature}: truth-value profiles over random finite interpretations.\n\\end{enumerate}\nThe $k$ cheapest bijections (predicates within equal arity; constants separately) are evaluated, and the pair is declared equivalent if any bijection yields a Z3-verified equivalence.\n\n\\subsection{Score variants}\n\nHigher scores indicate greater divergence from peers and thus higher predicted error probability.\nVariants include:\n\\begin{itemize}\n\\item \\textbf{c\\_exact}: no alignment; exact-match equivalence only. Immune to rename false alarms but blind to vocabulary-differing equivalences.\n\\item \\textbf{c\\_nf} (name-free): alignment by structural and semantic signatures only, ignoring text anchoring.\n\\item \\textbf{p\\_peer\\_text}: a logistic fusion of consensus features with text-side features (bag-of-words coverage, role accounting, Z3 structural match).\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-2/experiment-5}}\n\\end{itemize}\n\n\\subsection{Evaluation framework}\n\n\\paragraph{Shared-signature labels.}\nOn R\\_COMP, labels are determined by Z3 equivalence to trusted-by-construction references (one weak and one strong reading per template), with no human or LLM judgement in the labelling loop.\n\n\\paragraph{Free-vocabulary labels.}\nOn development set~$E$, labels come from a three-person expert panel (adjudicated as ERROR or CORRECT), with disputed items counted according to the reliability assignment (R\\_AB: both panellists agree).\nOn R\\_COMP FREE, provisional labels use search-based ERROR\\_CERT versus MAPPED classifications (non-confirmatory; the gloss-based labelling gate failed twice).\n\n\\paragraph{Metrics.}\nThe primary evaluation metric is stratified AUROC: items are paired only within the same source stratum (sentence-template on R\\_COMP, sentence-complexity bin on~$E$), eliminating confounds from stratum-level base rates.\nConfidence intervals use sentence-cluster percentile bootstrap ($B = 2{,}000$).\n\n\\section{Experiments}\\label{sec:experiments}\n\n\\subsection{Datasets}\n\n\\paragraph{R\\_COMP (shared and free vocabulary).}\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-7}}\nR\\_COMP generates long, complex sentences ($\\geq$25 words, 4--5 conditions) from a verified lexicon.\n221~sentences produced 2,024 candidate translations from 10~LLM slots across 9~vendor families.\nPopulation: 429~ERROR~/~1,595~CORRECT (21.2\\% error rate).\nIn the \\textbf{SIG condition}, all translators received a supplied predicate signature; labels are pure Z3 equivalence to trusted references.\nIn the \\textbf{FREE condition}, each translator chose its own predicate names; labels are provisional (Section~\\ref{sec:free_oos}).\nThe pre-registration document, including the analysis plan and testability rule, was frozen before any SIG generation call, any label, or any metric score.\\footnote{Pre-registration: \\texttt{prereg\\_sig.json}, SHA-256 frozen before data collection.}\n\n\\paragraph{Development set $E$.}\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-3}}\n8,507~rows from 700~sentences drawn from the MALLS corpus~\\citep{Yang2023} and ProverQA~\\citep{Qi2025}.\nEach sentence was translated by 9~LLM families using a frozen few-shot prompt.\nThe primary evaluation population (R\\_AB, both panellists agree) contains 2,686~items (1,822~ERROR~/~864~CORRECT, 292~sentences); the all-families subset where every peer family contributed a translation is $n = 2{,}014$.\nComplexity strata: L25 ($\\geq$25 words), L20 (20--24), EXC (exception clauses), CTRL (short control sentences).\nThe R\\_COMP-SIG data later served as development data for aligner tuning, so the development-set numbers from $E$ are not independent of R\\_COMP.\n\n\\paragraph{Baselines.}\n(1)~\\textbf{Flash-lite judge} (Gemini Flash Lite, disguised and original views); (2)~\\textbf{nano judge} (Gemini Flash 2.0); (3)~\\textbf{local judges} (Qwen3-8B, Llama-8B); (4)~\\textbf{round-trip NLI}; (5)~\\textbf{self-consistency} (5-sample within-model agreement); (6)~\\textbf{structural features} (arity consistency, dangling predicates, rerun Jaccard); (7)~\\textbf{feature stacks}: cross-validated logistic regressions over subsets of these features.\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-4}}\n\n\\subsection{Shared-signature results (R\\_COMP-SIG)}\\label{sec:sig_results}\n\nTable~\\ref{tab:sig} reports the pre-registered comparison on R\\_COMP under shared signature.\nOn the 1,904~rows where both consensus and judge scores exist, consensus achieves a within-template AUROC of 0.954 versus 0.587 for the disguised flash-lite judge ($\\Delta = +0.367$ [+0.328, +0.404]).\nAgainst the original-view judge (1,932~rows), the advantage is $\\Delta = +0.278$ [+0.239, +0.319].\nError endorsement is zero ($e = 0$): no error item scores below the decision threshold.\nAmong the 429~error items, 75.3\\% receive the maximum consensus score of~1.0; the remaining 24.7\\% score between 0.625 and~1.0.\n\n\\begin{table}[!htbp]\n\\centering\n\\caption{Within-template AUROC on R\\_COMP-SIG (shared signature, 221~sentences, pure Z3 labels). CIs are 95\\% sentence-cluster bootstrap.}\n\\label{tab:sig}\n\\small\n\\begin{tabular}{lccc}\n\\toprule\nMetric & $n$ & Within-template AUROC [95\\% CI] & $\\Delta$ vs.\\ disg.\\ judge [95\\% CI] \\\\\n\\midrule\nc\\_score\\_sig & 1904 & 0.954 [0.939, 0.968] & +0.367 [+0.328, +0.404] \\\\\nc\\_score\\_align & 1904 & 0.954 [0.939, 0.968] & +0.367 [+0.328, +0.404] \\\\\njudge (flash-lite, disg.) & 1904 & 0.587 [0.551, 0.622] & --- \\\\\njudge (flash-lite, orig.) & 1932 & 0.673 [0.637, 0.708] & \\\\\njudge (frontier, orig.) & 60 & 0.932 [0.782, 1.000] & \\\\\njudge (local, disg.) & 2024 & 0.498 [0.459, 0.534] & \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}\n\n\\paragraph{Flat with sentence length.}\nUnlike the free-vocabulary setting (Section~\\ref{sec:mechanism}), consensus under shared signature is flat across word-length terciles: W1 0.959, W2 0.947, W3 0.953 (Table~\\ref{tab:sig_complexity} and Figure~\\ref{fig:sig_tercile}).\n\n\\begin{table}[!htbp]\n\\centering\n\\caption{R\\_COMP-SIG within-template AUROC by word-length tercile (judge-matched rows).}\n\\label{tab:sig_complexity}\n\\small\n\\begin{tabular}{lccccc}\n\\toprule\nTercile & $n$ & ERR/COR & c\\_sig & judge (disg.) & $\\Delta$ [CI] \\\\\n\\midrule\nW1 (shortest) & 503 & 125/449 & 0.959 & 0.578 & +0.382 [+0.278, +0.472] \\\\\nW2 & 712 & 149/594 & 0.947 & 0.624 & +0.331 [+0.253, +0.421] \\\\\nW3 (longest) & 689 & 155/552 & 0.953 & 0.567 & +0.388 [+0.301, +0.471] \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}\n\n\\begin{figure}[!htbp]\n  \\centering\n  \\includegraphics[width=\\linewidth,height=0.85\\textheight,keepaspectratio]{figures/fig_sig_tercile_v0.pdf}\n  \\caption{Within-template AUROC on R\\_COMP-SIG by word-length tercile (judge-matched rows). Consensus (blue) is flat across terciles (0.947--0.959), while the disguised flash-lite judge (orange) hovers near chance (0.567--0.624). Error bars are 95\\% sentence-cluster bootstrap CIs.}\n  \\label{fig:sig_tercile}\n\\end{figure}\n\n\\paragraph{Frontier judge comparison.}\nOn a descriptive 60-row stratified subsample scored by the frontier judge (Gemini~3.1~Pro, original view), consensus achieves pooled AUROC 0.956 [0.889, 1.000] versus 0.932 [0.855, 0.990] for the frontier judge.\n\n\\paragraph{Scope.}\nR\\_COMP-SIG uses templated sentences with a supplied predicate vocabulary.\nThe shared signature eliminates the alignment problem entirely, which is why the AUROC is so high.\nThese results do not extend to settings where translators choose their own predicate names.\n\n\\subsection{Free-vocabulary development results (set $E$)}\\label{sec:dev_results}\n\nFigure~\\ref{fig:dev_auroc} and Table~\\ref{tab:main} summarise the free-vocabulary comparison on development set~$E$.\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-6}}\nCross-family consensus (c\\_score\\_align) outperforms the disguised flash-lite judge by $\\Delta = +0.099$ [+0.049, +0.146] on the full R\\_AB population and by $\\Delta = +0.116$ [+0.070, +0.163] on the long-sentence pool (L25+L20+EXC).\nAdding c\\_score\\_align to the 28-feature baseline stack increases stratified AUROC by +0.039 [+0.021, +0.057]; a permutation null test gives $p_{95} = 0.009$, confirming the signal is not explained by the existing features.\n\n\\begin{table}[!htbp]\n\\centering\n\\caption{Stratified AUROC on development set $E$ (R\\_AB population, free vocabulary, $n = 2{,}686$). Higher is better. CIs are 95\\% sentence-cluster bootstrap.}\n\\label{tab:main}\n\\small\n\\begin{tabular}{lcc}\n\\toprule\nMetric & Strat AUROC [95\\% CI] & \\$/item \\\\\n\\midrule\nc\\_score\\_align & 0.741 [0.705, 0.775] & 9.1e-5 \\\\\np\\_peer\\_text (fused) & 0.753 [0.720, 0.784] & 9.1e-5 \\\\\nc\\_exact (no alignment) & 0.689 [0.652, 0.726] & -- \\\\\nc\\_nf (name-free) & 0.686 [0.647, 0.720] & -- \\\\\n\\midrule\nflash-lite judge (disg.) & 0.642 [0.607, 0.676] & 5.1e-5 \\\\\nflash-lite judge (orig.) & 0.623 [0.593, 0.651] & 5.1e-5 \\\\\nnano judge (disg.) & 0.644 [0.609, 0.680] & 2.0e-5 \\\\\nlocal judge Qwen-8B (disg.) & 0.674 [0.646, 0.703] & -- \\\\\n\\midrule\nround-trip NLI (min) & 0.606 [0.569, 0.645] & 2.8e-5 \\\\\nself-consistency (5-sample) & 0.598 [0.559, 0.637] & 6.7e-5 \\\\\n\\midrule\n28-feature stack & 0.735 [0.699, 0.766] & -- \\\\\n28-feature stack + c\\_score\\_align & 0.774 [0.743, 0.802] & -- \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}\n\nThe drop from 0.952 (shared signature on the full 2,024-row pool) to 0.801 (free vocabulary on the same R\\_COMP sentences) reflects the cost of predicate-name alignment: the aligner introduces both false negatives (correct equivalences missed) and false positives (incorrect mappings endorsed).\n(The 0.954 reported in Table~\\ref{tab:sig} is the same consensus metric restricted to the 1,904~rows where the disguised judge also returned a score, enabling a paired comparison; the full-pool AUROC is 0.952 [0.937, 0.965].)\nAligner-free consensus (c\\_exact) achieves 0.689 [0.652, 0.726]; the aligner adds about 22\\% of the above-chance signal (c\\_align 0.241 versus c\\_exact 0.189 above the 0.5 baseline), with the remaining 78\\% coming from structural agreement alone.\n\nOn L25 sentences alone ($\\geq$25 words), the advantage narrows to $\\Delta = +0.069$ [$-$0.020, +0.148], not significant at the 95\\% level.\nThis foreshadows the length-dependent degradation described in Section~\\ref{sec:mechanism}.\n\n\\paragraph{Frontier judge comparison.}\nOn the 284-row subsample scored by the frontier judge (Gemini~3.1~Pro), c\\_score\\_align achieves 95.7\\% of the frontier judge's AUROC (ratio 0.957 [0.887, 1.034]).\n\n\\paragraph{System-level ranking.}\nThe consensus metric achieves Kendall $\\tau_b = 0.692$ [+0.513, +0.795] between system mean score and R\\_AB error rate across 13 system$\\times$variant configurations, comparable to the best judges.\n\n\\subsection{Free-vocabulary out-of-sample (R\\_COMP FREE)}\\label{sec:free_oos}\n\nThe same 221~R\\_COMP sentences were also translated under free vocabulary (each translator choosing its own predicate names).\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-13}}\nConfirmatory labelling required a gloss gate (LLM-checked semantic alignment of predicate mappings).\nThis gate failed twice (balanced accuracy 0.776 and 0.561, below the 0.90 threshold), producing zero confirmed CORRECT rows and rendering the confirmatory test not testable.\n\nUnder provisional non-confirmatory labels (ERROR\\_CERT vs.\\ MAPPED, where MAPPED is an upper bound on CORRECT), Table~\\ref{tab:free} reports the untouched results.\n\n\\begin{table}[!htbp]\n\\centering\n\\caption{R\\_COMP FREE provisional AUROCs (within-template, untouched rows). Labels are non-confirmatory.}\n\\label{tab:free}\n\\small\n\\begin{tabular}{lccc}\n\\toprule\nView & $n$ (ERR/MAPPED) & c\\_align & judge \\\\\n\\midrule\nDisguised & 1706 (602/1104) & 0.801 [0.770, 0.834] & 0.584 [0.550, 0.618] \\\\\nOriginal & 1709 (605/1104) & 0.804 [0.774, 0.836] & 0.633 [0.601, 0.666] \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}\n\nThe disguised-judge delta is $+0.217$ [+0.175, +0.260]; the original-view delta is $+0.171$ [+0.135, +0.206].\nOn a 146-row subset with independent two-auditor labels, consensus achieves $\\Delta = +0.105$ [+0.011, +0.215] over the original-view judge.\nOn a 150-row frontier-judge subsample, consensus reaches 0.94 of the frontier judge's AUROC (ratio 0.940 [0.825, 1.056]).\n\nThese provisional numbers cannot count as confirmation because the MAPPED labels conflate vocabulary-alignment failures with genuine correctness.\nThey are consistent with the development-set signal but independent confirmation requires a working gloss gate or a different labelling strategy.\n\n\\subsection{Mechanism}\\label{sec:mechanism}\n\nWe decompose the consensus signal\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/evaluation-2}} into two components at a fixed decision threshold:\n\\begin{itemize}\n\\item \\textbf{Endorsement} $e$: fraction of ERROR items endorsed by the peer majority (false negatives of consensus).\n\\item \\textbf{Divergence} $d$: fraction of CORRECT items that diverge from the peer majority (false positives of consensus).\n\\end{itemize}\nThe consensus AUROC at a binary threshold equals $1 - (e + d)/2$, so both quantities must be small for the metric to work.\n\n\\paragraph{Shared vocabulary: endorsement zero, divergence moderate.}\nOn R\\_COMP-SIG, $e = 0.0$ and $d = 0.260$: no error escapes detection, though 26\\% of correct translations are flagged as divergent.\nThe false-alarm rate of 0.260 arises from correct translations that use valid but structurally different formalizations; because all translators share a predicate vocabulary, no alignment step is needed and the divergence rate is flat across sentence lengths.\n\n\\paragraph{Free vocabulary: divergence degrades with length.}\nAs Figure~\\ref{fig:complexity} shows, on development set~$E$ the net consensus degradation from short to long sentences is $\\Delta(e+d) = +0.356$ [+0.198, +0.493], driven almost entirely by divergence ($\\Delta d = +0.608$, $\\Delta e = -0.252$): as formulas grow longer and more structurally diverse, the predicate-name aligner (Section~\\ref{sec:rename}) increasingly maps distinct predicates together or fails to match equivalent ones, inflating the false-alarm rate on correct translations.\n\n\\begin{figure}[!htbp]\n  \\centering\n  \\includegraphics[width=\\linewidth,height=0.85\\textheight,keepaspectratio]{figures/fig_complexity_v0.pdf}\n  \\caption{Decomposition of free-vocabulary consensus error rates by sentence-length tercile on development set~$E$. Endorsement rate $e$ (errors incorrectly endorsed by peers) decreases with length, but divergence rate $d$ (correct items incorrectly flagged) increases sharply, producing net degradation of +0.356 from the shortest to the longest tercile. Under shared signature (R\\_COMP-SIG), this degradation is absent.}\n  \\label{fig:complexity}\n\\end{figure}\n\n\\paragraph{Family sufficiency.}\nThree peer families suffice for 97\\% of full-pool AUROC ($k_{95} = 3$), but the long-sentence tercile requires $k_{95} = 5$ (Table~\\ref{tab:k_families} and Figure~\\ref{fig:k_curve}).\n\n\\begin{table}[!htbp]\n\\centering\n\\caption{Free-vocabulary AUROC by number of peer families on development set $E$.}\n\\label{tab:k_families}\n\\small\n\\begin{tabular}{ccc}\n\\toprule\n$k$ & AUROC (overall) & AUROC (long, T3) \\\\\n\\midrule\n1 & 0.685 & 0.581 \\\\\n3 & 0.757 & 0.651 \\\\\n5 & 0.776 & 0.698 \\\\\n7 & 0.784 & 0.726 \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}\n\n\\begin{figure}[!htbp]\n  \\centering\n  \\includegraphics[width=\\linewidth,height=0.85\\textheight,keepaspectratio]{figures/fig_k_curve_v0.pdf}\n  \\caption{Stratified AUROC as a function of the number of peer families $k$, for the full development set (solid blue) and the long-sentence tercile (dashed red). Three families capture 97\\% of the full-pool signal, but long sentences require five families to reach 95\\%.}\n  \\label{fig:k_curve}\n\\end{figure}\n\n\\subsection{Confirmation status}\\label{sec:confirmation}\n\nIndependent confirmation on held-out data remains incomplete.\nA fresh held-out dataset (E2-A, 550~new sentences) was constructed, but the run-level budget was exhausted before enough items could be labelled.\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/dataset-4}}\nOn the one testable stratum (DT, short sentences from ProverQA), consensus achieves a stratified AUROC of 0.916, tying the local Qwen-8B judge ($\\Delta = +0.003$ [$-$0.042, +0.052]).\nOn L25 sentences, c\\_score\\_align falls to 0.443 on only 42 items (35~ERROR~/~7~CORRECT), below chance, but the estimate has extreme variance with only 7~CORRECT items from 3~sentences.\nEvery pre-registered criterion on the target strata returned NOT\\_TESTABLE or unfavourable.\n\n\\subsection{The rename tradeoff}\\label{sec:rename}\n\nThe predicate aligner\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-8}} that enables cross-family comparison under free vocabulary also introduces a fundamental false-alarm vulnerability.\nWhen correct formulas are copied with meaning-preserving predicate renames (same semantics, different symbol names), the consensus score should not change.\nTable~\\ref{tab:rename} shows the false-alarm rates in practice.\n\n\\begin{table}[!htbp]\n\\centering\n\\caption{False-alarm (FA) rates on meaning-preserving renames of CORRECT candidates. NONCE = random nonsense names; SYN = WordNet synonyms. Flip = FA induced by the rename alone (FA minus base FA).}\n\\label{tab:rename}\n\\small\n\\begin{tabular}{lcccc}\n\\toprule\nMetric & NONCE FA & NONCE flip & SYN FA & SYN flip \\\\\n\\midrule\nc\\_align & 0.765 & 0.605 & 0.565 & 0.313 \\\\\nc\\_nf (name-free) & 0.132 & 0.000 & 0.201 & 0.000 \\\\\np\\_peer\\_text & 1.000 & 0.821 & 0.216 & 0.080 \\\\\njudge (disg.) & 0.229 & 0.134 & 0.085 & 0.058 \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}\n\nThe name-free variant c\\_nf eliminates rename sensitivity (flip = 0) but at the cost of blindness to meaning-rename errors (within-base AUROC 0.499, chance level) and lower overall discrimination (strat AUROC 0.686 vs.\\ 0.741).\nThis tradeoff explains the gap between shared-signature and free-vocabulary performance: the shared signature eliminates the need for alignment entirely, sidestepping the rename problem.\n\n\\subsection{Per-type sensitivity}\n\nOn the PERTURB suite (4,234 typed mutants + 868 controls from development data), consensus recall at the primary threshold is flat across error operators: NEG 0.761, SWAP 0.758, DROP 0.721, ADD 0.763, MEANING\\_RENAME 0.762.\nPer-operator AUROC within error types cannot be computed because 94--100\\% of mutants receive the maximum consensus score, a ceiling effect of the endorsement structure.\n\nError typing outside a shared vocabulary is negative: the free-vocabulary typing accuracy is 0.123 [0.081, 0.169] on $E$, below both the judge (0.326) and the peer-medoid baseline (0.328), and all three are near chance for a five-class task.\n\n\\subsection{Dead ends}\n\nSeveral alternatives were investigated and abandoned during development: a fused structural-feature filter (false-alarm gate failure); name-free consensus c\\_nf (rename-invariant but blind to meaning-rename errors, as described in Section~\\ref{sec:rename}); a decomposed solver-based semantic reader (balanced accuracy 0.476); LLM adjudication of disputed items (balanced accuracy 0.662 on expert-labelled items); and candidate-signature consensus, which scores candidates by cueing peers with the candidate's own predicate symbols rather than letting them choose independently (provisional negative: error endorsement rose to 0.459 because peers were anchored into reproducing the candidate's errors).\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/experiment-9}}\n\n\\section{Discussion}\n\n\\subsection{Shared versus free vocabulary}\n\nThe central finding is that vocabulary regime governs metric strength.\nUnder shared signature, consensus achieves near-perfect discrimination (0.954 AUROC) flat across sentence lengths.\nUnder free vocabulary, performance drops by roughly 0.15~AUROC on comparable sentences (R\\_COMP-SIG 0.952 versus R\\_COMP FREE 0.801, both within-template on long composed sentences) and degrades with sentence length on natural data.\n\nThis gap is explained by the rename tradeoff: the predicate-name aligner needed for free-vocabulary comparison introduces both false negatives (missed equivalences) and false positives (spurious mappings), and these grow worse as formulas become longer and more structurally diverse.\nThe practical implication is that consensus-based evaluation is most reliable when translators share a predicate vocabulary, as in controlled evaluation settings~\\citep{Bayless2025,Vossel2025}.\n\n\\subsection{Why confirmation is incomplete}\n\nThe confirmation attempt was defeated by two independent problems: (1)~insufficient fresh data (the E2-A budget was stopped before enough correct items accumulated in the long-sentence strata), and (2)~a broken labelling gate (the gloss-based semantic alignment required for R\\_COMP FREE labels failed quality checks twice).\nNeither failure refutes the development-set signal, but neither allows us to confirm it on the target strata.\n\nThe E2-A L25 result (AUROC 0.443, near chance, on 42~items) is concerning but difficult to interpret: with only 7~CORRECT items from 3~sentences, the estimate has extreme variance and a single sentence can dominate.\nWe report it for completeness but note that it does not meet any standard testability criterion.\n\n\\subsection{The rename tradeoff as a fundamental limit}\n\nThe rename tradeoff is not a bug in our aligner but a structural property of cross-family consensus under independent vocabulary.\nAny alignment procedure that maps independently chosen predicate names to a common vocabulary will sometimes map semantically distinct predicates together, endorsing meaning-rename errors.\nEliminating the alignment (c\\_exact, c\\_nf) preserves rename invariance but sacrifices the structural comparison that drives error detection.\n\nWe conjecture that resolving this tradeoff requires either (a)~a shared predicate vocabulary supplied to all translators, which eliminates the problem entirely but restricts the evaluation to controlled settings~\\citep{Bayless2025,Vossel2025}, or (b)~a semantic disambiguation step (such as natural-language glosses of each predicate) that could break the alignment ambiguity.\nOur attempt at option~(b), a gloss gate using LLM-generated explanations of predicate meanings, failed quality checks, leaving this direction open.\n\n\\subsection{Limitations}\\label{sec:limitations}\n\n\\begin{enumerate}\n\\item \\textbf{Shared-signature scope.} The 0.954 AUROC result uses templated sentences with a supplied predicate vocabulary, which eliminates the alignment problem. The templates and the supplied signature limit the scope of this result to controlled evaluation settings.\n\\item \\textbf{Development data overlap.} The R\\_COMP-SIG dataset later served as development data for aligner tuning. The pre-registration ensures the SIG result itself is uncontaminated, but the development-set numbers from $E$ are not independent.\n\\item \\textbf{Rename vulnerability.} Under free vocabulary, a 76.5\\% false-alarm rate on nonce renames means the metric will systematically penalise any translation that uses non-standard predicate names, even if semantically correct.\n\\item \\textbf{Length degradation (free vocabulary).} Consensus discrimination degrades with sentence length under free vocabulary (NET $+0.356$), driven by correct-translation divergence. The metric is weakest on the longest, most complex sentences, precisely the cases where gold-free evaluation is most needed.\n\\item \\textbf{Provisional labels.} R\\_COMP FREE results use provisional (non-confirmatory) labels; the two-auditor subset ($\\Delta = +0.105$) has a CI that barely excludes zero.\n\\item \\textbf{Label dependence.} Development results on~$E$ depend on a three-person panel whose agreement is imperfect (disputed items exist in every stratum). The metric's advantage could partly reflect alignment with panel biases rather than with ground-truth faithfulness.\n\\item \\textbf{Cost.} The consensus metric requires generating $k$ peer translations per sentence. In this experiment ($k = 9$, R\\_COMP-SIG), the amortised consensus cost per candidate is about 19 times the cost of a single cheap judge call.\n\\item \\textbf{Domain.} All results are on English$\\to$FOL from MALLS, ProverQA, and R\\_COMP sources. Generalisation to other logic formalisms, languages, or sentence distributions is untested.\n\\end{enumerate}\n\n\\section{Conclusion}\n\nCross-family solver consensus is a strong gold-free faithfulness metric for NL$\\to$FOL translation when translators share a predicate vocabulary.\nThe pre-registered R\\_COMP-SIG result (AUROC 0.954 versus 0.587 for a disguised judge, flat with length) establishes the ceiling; free vocabulary costs roughly 0.15~AUROC and introduces the rename tradeoff.\n\nUnder free vocabulary, consensus still outperforms cheap LLM judges on both development data ($+0.099$) and untouched out-of-sample sentences ($+0.171$), and adds information beyond structural and statistical baselines.\nThe mechanism --- errors scatter while correct translations cluster --- provides an intuitive explanation grounded in the diversity of independent formalizations.\n\nHowever, independent confirmation on held-out data was budget-stopped and remains incomplete, the rename tradeoff limits applicability to free-vocabulary settings, and discrimination degrades with sentence length under free vocabulary.\nWe release the full evaluation code and data to enable reproduction.\nThe immediate open problems are: (1)~completing the fresh-data confirmation with adequate sample sizes; (2)~breaking the rename tradeoff, perhaps through semantic predicate glossing; and (3)~understanding why correct translations of complex sentences diverge under free vocabulary.\n\n\\bibliographystyle{plainnat}\n\\bibliography{references}\n\n\\end{document}\n", "numLines": 445, "startLine": 1, "totalLines": 445}}
```

### [12] TOOL CALL — Bash · 2026-09-25 09:33:43 UTC

```
List workspace files:
find /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace -type f | head -50
```

### [13] TOOL RESULT — Bash · 2026-09-25 09:33:43 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/.terminal_claude_agent_struct_out.json\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.bbl\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.blg\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.pdf\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.out\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.aux\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.log\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.tex\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/references.json\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/references.bib\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/.repl_agent.ptylog\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/.aii_claude_session.json\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/.aii/module_end.json\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/figures/fig_sig_tercile_v0.png\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/figures/fig_sig_tercile_v0.pdf\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/figures/fig_k_curve_v0.pdf\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/figures/fig_complexity_v0.pdf\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/figures/fig_dev_auroc_v0.pdf", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [14] ASSISTANT · 2026-09-25 09:34:39 UTC

```
The paper references 4 figures (including fig_sig_tercile which is only in workspace). Let me render the PNGs and check references.json for any URLs I need.
```

### [15] TOOL CALL — Read · 2026-09-25 09:34:39 UTC

```
/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/references.json
```

### [16] TOOL RESULT — Read · 2026-09-25 09:34:39 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/references.json", "content": "{\n  \"Brunello2026\": {\n    \"source\": \"semantic_scholar\",\n    \"title\": \"Fixing FOLIO and MALLS: Verified Annotations and an LLM-assisted Framework to Focus Human Relabeling\",\n    \"first_author\": \"Brunello\",\n    \"year\": 2026,\n    \"s2_paper_id\": \"ecbee7abfea235f4d6445a26bce913c40c799a45\",\n    \"doi\": \"10.48550/arXiv.2606.02837\",\n    \"arxiv\": \"2606.02837\"\n  },\n  \"Han2022\": {\n    \"source\": \"semantic_scholar\",\n    \"title\": \"FOLIO: Natural Language Reasoning with First-Order Logic\",\n    \"first_author\": \"Han\",\n    \"year\": 2022,\n    \"s2_paper_id\": \"5581bf85386737bd3378eec68189759a05280bea\",\n    \"doi\": \"10.48550/arXiv.2209.00840\",\n    \"arxiv\": \"2209.00840\"\n  },\n  \"Yang2023\": {\n    \"source\": \"semantic_scholar\",\n    \"title\": \"Harnessing the Power of Large Language Models for Natural Language to First-Order Logic Translation\",\n    \"first_author\": \"Yang\",\n    \"year\": 2023,\n    \"s2_paper_id\": \"e4e625f8e8ae5ee82e75de5ad6e07af57cca7f53\",\n    \"doi\": \"10.48550/arXiv.2305.15541\",\n    \"arxiv\": \"2305.15541\"\n  },\n  \"Chiang2024\": {\n    \"source\": \"semantic_scholar\",\n    \"title\": \"Chatbot Arena: An Open Platform for Evaluating LLMs by Human Preference\",\n    \"first_author\": \"Chiang\",\n    \"year\": 2024,\n    \"s2_paper_id\": \"53f4fb0e9972989194368faf288ff8e3cba5bd60\",\n    \"doi\": \"10.48550/arXiv.2403.04132\",\n    \"arxiv\": \"2403.04132\"\n  },\n  \"Wei2022\": {\n    \"source\": \"semantic_scholar\",\n    \"title\": \"Chain of Thought Prompting Elicits Reasoning in Large Language Models\",\n    \"first_author\": \"Wei\",\n    \"year\": 2022,\n    \"s2_paper_id\": \"1b6e810ce0afd0dd093f789d2b2742d047e316d5\",\n    \"doi\": \"10.52202/068431-1800\",\n    \"arxiv\": \"2201.11903\"\n  },\n  \"Wang2022\": {\n    \"source\": \"semantic_scholar\",\n    \"title\": \"Self-Consistency Improves Chain of Thought Reasoning in Language Models\",\n    \"first_author\": \"Wang\",\n    \"year\": 2022,\n    \"s2_paper_id\": \"5f19ae1135a9500940978104ec15a5b8751bc7d2\",\n    \"arxiv\": \"2203.11171\"\n  },\n  \"Bayless2025\": {\n    \"source\": \"semantic_scholar\",\n    \"title\": \"A Neurosymbolic Approach to Natural Language Formalization and Verification\",\n    \"first_author\": \"Bayless\",\n    \"year\": 2025,\n    \"s2_paper_id\": \"8b6d7956c8a4f5418847316a69fded71de370339\",\n    \"doi\": \"10.48550/arXiv.2511.09008\",\n    \"arxiv\": \"2511.09008\"\n  },\n  \"Vossel2025\": {\n    \"source\": \"semantic_scholar\",\n    \"title\": \"Advancing Natural Language Formalization to First Order Logic with Fine-tuned LLMs\",\n    \"first_author\": \"Vossel\",\n    \"year\": 2025,\n    \"s2_paper_id\": \"8d1d88b8befa4e0c493b5c9361ebe6a32fb59e77\",\n    \"doi\": \"10.48550/arXiv.2509.22338\",\n    \"arxiv\": \"2509.22338\"\n  },\n  \"Thatikonda2025\": {\n    \"source\": \"semantic_scholar\",\n    \"title\": \"Assessing the Sensitivity and Alignment of FOL Closeness Metrics\",\n    \"first_author\": \"Thatikonda\",\n    \"year\": 2025,\n    \"s2_paper_id\": \"412f0d746b470d51e6a03d56b20b5ea8c3b0f35f\",\n    \"doi\": \"10.18653/v1/2025.findings-emnlp.910\",\n    \"arxiv\": \"2501.08613\"\n  },\n  \"Zhang2023\": {\n    \"source\": \"semantic_scholar\",\n    \"title\": \"SAC3: Reliable Hallucination Detection in Black-Box Language Models via Semantic-aware Cross-check Consistency\",\n    \"first_author\": \"Zhang\",\n    \"year\": 2023,\n    \"s2_paper_id\": \"6af460d34bfc8e955e43fbe15cedcf329b48bc19\",\n    \"doi\": \"10.48550/arXiv.2311.01740\",\n    \"arxiv\": \"2311.01740\"\n  },\n  \"Eckhardt1985\": {\n    \"source\": \"semantic_scholar\",\n    \"title\": \"A Theoretical Basis for the Analysis of Multiversion Software Subject to Coincident Errors\",\n    \"first_author\": \"Eckhardt\",\n    \"year\": 1985,\n    \"s2_paper_id\": \"c3a7e368f1faecb0bdfb4e1f757edb883d690ff8\",\n    \"doi\": \"10.1109/TSE.1985.231895\"\n  },\n  \"Moura2008\": {\n    \"source\": \"semantic_scholar\",\n    \"title\": \"Z3: An Efficient SMT Solver\",\n    \"first_author\": \"Moura\",\n    \"year\": 2008,\n    \"s2_paper_id\": \"3960dda299e0f8615a7db675b8e6905b375ecf8a\",\n    \"doi\": \"10.1007/978-3-540-78800-3_24\"\n  },\n  \"Qi2025\": {\n    \"source\": \"semantic_scholar\",\n    \"title\": \"Large Language Models Meet Symbolic Provers for Logical Reasoning Evaluation\",\n    \"first_author\": \"Qi\",\n    \"year\": 2025,\n    \"s2_paper_id\": \"f8192ee0765fe874d2259536e92aa33a48e50bb1\",\n    \"doi\": \"10.48550/arXiv.2502.06563\",\n    \"arxiv\": \"2502.06563\"\n  }\n}\n", "numLines": 117, "startLine": 1, "totalLines": 117}}
```

### [17] TOOL CALL — Bash · 2026-09-25 09:34:39 UTC

```
Copy fig_sig_tercile PDF from workspace to figures dir:
cp /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/figures/fig_sig_tercile_v0.pdf /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/figures/fig_sig_tercile_v0.pdf
```

### [18] TOOL RESULT — Bash · 2026-09-25 09:34:39 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": true}
```

### [19] TOOL CALL — Bash · 2026-09-25 09:34:39 UTC

```
Install pymupdf for PDF-to-PNG rendering:
pip install pymupdf 2>&1 | tail -3
```

### [20] TOOL RESULT — Bash · 2026-09-25 09:34:39 UTC

```
{"stdout": "[notice] A new release of pip is available: 25.0.1 -> 26.2.1\n[notice] To update, run: pip install --upgrade pip", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] ASSISTANT · 2026-09-25 09:34:49 UTC

```
Now let me render all 4 figure PDFs to PNGs.
```

### [22] TOOL CALL — Bash · 2026-09-25 09:34:49 UTC

```
Render all 4 figure PDFs to PNGs at 2.5x resolution:
python3 -c "
import fitz
import os

figs = ['fig_dev_auroc_v0', 'fig_sig_tercile_v0', 'fig_complexity_v0', 'fig_k_curve_v0']
for fig in figs:
    pdf_path = f'figures/{fig}.pdf'
    png_path = f'figures/{fig}.png'
    if not os.path.exists(pdf_path):
        print(f'MISSING: {pdf_path}')
        continue
    doc = fitz.open(pdf_path)
    page = doc[0]
    mat = fitz.Matrix(2.5, 2.5)
    pix = page.get_pixmap(matrix=mat)
    pix.save(png_path)
    print(f'{png_path}: {os.path.getsize(png_path)} bytes')
    doc.close()
"
```

### [23] TOOL RESULT — Bash · 2026-09-25 09:34:49 UTC

```
{"stdout": "warning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.\nfigures/fig_dev_auroc_v0.png: 78933 bytes\nfigures/fig_sig_tercile_v0.png: 54343 bytes\nfigures/fig_complexity_v0.png: 58891 bytes\nfigures/fig_k_curve_v0.png: 70485 bytes", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [24] ASSISTANT · 2026-09-25 09:34:55 UTC

```
All 4 PNGs rendered. Now I'll build the index.html. Let me check for CDN URLs and the repo pattern from the previous run's index.html for reference.
```

### [25] TOOL CALL — Bash · 2026-09-25 09:34:55 UTC

```
Extract URLs from the previous run's index.html for reference:
grep -o 'https://[^"]*' /ai-inventor/aii_data/runs/run_cNhUBrixEdz7/4_gen_paper_repo/_4_assemble_paper/paper/index.html 2>/dev/null | sort -u | head -30
```

### [26] TOOL RESULT — Bash · 2026-09-25 09:34:55 UTC

```
{"stdout": "https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_cNhUBrixEdz7/paper.pdf\nhttps://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_cNhUBrixEdz7/report.pdf\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-1/dataset-1\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-1/experiment-1\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-1/experiment-3\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-1/experiment-4\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-2/dataset-3\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-2/evaluation-1\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-2/experiment-5\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/evaluation-2\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/experiment-6\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/experiment-7\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/experiment-8\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/research-1\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-4/dataset-4\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-4/dataset-5\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-4/evaluation-3\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-4/experiment-10\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-4/experiment-9\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-5/evaluation-4\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-5/experiment-11\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-5/experiment-12\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-5/experiment-13\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-5/experiment-14", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [27] ASSISTANT · 2026-09-25 09:35:07 UTC

```
Let me check what experiment/evaluation/dataset directories exist for this run to include all artifact links.
```

### [28] TOOL CALL — Bash · 2026-09-25 09:35:07 UTC

```
Find all experiment/evaluation/dataset directories in this run:
find /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3 -maxdepth 3 -mindepth 3 -type d | grep -E 'round-[0-9]+/(experiment|evaluation|dataset|research)-[0-9]+' | sort
```

### [29] TOOL RESULT — Bash · 2026-09-25 09:35:07 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [30] TOOL CALL — Bash · 2026-09-25 09:35:15 UTC

```
Explore this run's directory structure:
find /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3 -maxdepth 4 -type d | head -40
```

### [31] TOOL RESULT — Bash · 2026-09-25 09:35:15 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/.shared_cache\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/sinks\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/user_uploads\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/logs\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/.shared_cache/pip\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/.shared_cache/hf\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/.shared_cache/hf/hub\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/round_reports\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_1_gh_repo\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/report_latex\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/report_workspace\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/report_workspace/.aii\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/report_workspace/figures\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/.shared_cache/pip/selfcheck\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/.shared_cache/pip/http-v2\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/report_latex/figures\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/.aii\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/figures\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/sinks/otel\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/sinks/events\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/.shared_cache/pip/http-v2/a\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/.shared_cache/pip/http-v2/d\n/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/.shared_cache/pip/http-v2/6", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [32] TOOL CALL — Bash · 2026-09-25 09:35:19 UTC

```
Check gh_repo directory for artifact metadata:
ls /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_1_gh_repo/ 2>/dev/null && echo "---" && cat /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_1_gh_repo/*.json 2>/dev/null | head -50
```

### [33] TOOL RESULT — Bash · 2026-09-25 09:35:19 UTC

```
{"stdout": "repo_info.json\n---\n{\n  \"repo_name\": \"ai-invention-eff060-layered-gold-free-checks-for-logic\",\n  \"repo_url\": \"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic\",\n  \"repo_owner\": \"ai-inventor-papers\",\n  \"error\": null,\n  \"description\": \"THE METRIC (headline deliverable). A three-layer, gold-free check, FOL-Triage(text, fol). It returns P(unfaithful), the layer that fired and an error-type code. It is built around where REAL NL->FOL e\",\n  \"branch\": \"fork/run_Jhw6i0bFXdo3\",\n  \"base_branch\": \"fork/run_cNhUBrixEdz7\",\n  \"metadata\": {\n    \"generated_at\": \"2026-09-25T09:18:48.018505+00:00\",\n    \"module\": \"own_repo_info\",\n    \"llm_provider\": \"gh_cli\",\n    \"output_dir\": \"/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo\"\n  }\n}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [34] TOOL CALL — Bash · 2026-09-25 09:35:25 UTC

```
Check round reports for artifact listings:
ls /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/round_reports/ 2>/dev/null
```

### [35] TOOL RESULT — Bash · 2026-09-25 09:35:25 UTC

```
{"stdout": "round-1.pdf\nround-2.pdf\nround-3.pdf\nround-4.pdf\nround-5.pdf", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [36] TOOL CALL — Bash · 2026-09-25 09:35:31 UTC

```
Extract artifact names from round reports:
cd /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo && python3 -c "
import pymupdf
import re

# Extract artifact names from each round report
for i in range(1,6):
    doc = pymupdf.open(f'round_reports/round-{i}.pdf')
    text = ''
    for page in doc:
        text += page.get_text()
    doc.close()
    # Find experiment/dataset/evaluation/research names
    matches = re.findall(r'(experiment|evaluation|dataset|research)-\d+', text)
    unique = sorted(set(matches))
    print(f'Round {i}: {unique}')
"
```

### [37] TOOL RESULT — Bash · 2026-09-25 09:35:31 UTC

```
{"stdout": "Round 1: []\nRound 2: []\nRound 3: []\nRound 4: []\nRound 5: ['dataset']", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [38] TOOL CALL — Bash · 2026-09-25 09:35:37 UTC

```
List top-level directories on the GitHub branch:
gh api repos/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/git/trees/fork/run_Jhw6i0bFXdo3 --jq '.tree[] | .path' 2>/dev/null | head -30
```

### [39] TOOL RESULT — Bash · 2026-09-25 09:35:37 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [40] TOOL CALL — Bash · 2026-09-25 09:35:39 UTC

```
List repo contents via GitHub API:
gh api "repos/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/contents/?ref=fork/run_Jhw6i0bFXdo3" --jq '.[].name' 2>&1 | head -20
```

### [41] TOOL RESULT — Bash · 2026-09-25 09:35:39 UTC

```
{"stdout": "To get started with GitHub CLI, please run:  gh auth login\nAlternatively, populate the GH_TOKEN environment variable with a GitHub API authentication token.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [42] TOOL CALL — Bash · 2026-09-25 09:35:51 UTC

```
Search round reports for artifact path references:
cd /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo && python3 -c "
import pymupdf
import re

for i in range(1,6):
    doc = pymupdf.open(f'round_reports/round-{i}.pdf')
    text = ''
    for page in doc:
        text += page.get_text()
    doc.close()
    # Look for 'round-X/something-Y' patterns
    matches = re.findall(r'round-\d+/(?:experiment|evaluation|dataset|research)-\d+', text)
    unique = sorted(set(matches))
    if unique:
        print(f'Round {i}: {unique}')
    else:
        # Try broader pattern
        matches2 = re.findall(r'(?:experiment|evaluation|dataset|research)[_-]\d+', text)
        unique2 = sorted(set(matches2))
        print(f'Round {i}: {unique2}')
"
```

### [43] TOOL RESULT — Bash · 2026-09-25 09:35:53 UTC

```
{"stdout": "Round 1: []\nRound 2: []\nRound 3: []\nRound 4: []\nRound 5: ['dataset-5']", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [44] TOOL CALL — Bash · 2026-09-25 09:35:59 UTC

```
Read round report summaries for artifact context:
cd /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo && python3 -c "
import pymupdf

for i in range(1,6):
    doc = pymupdf.open(f'round_reports/round-{i}.pdf')
    text = ''
    for page in doc:
        text += page.get_text()
    doc.close()
    # Extract the first ~500 chars to see the structure
    print(f'=== Round {i} (first 800 chars) ===')
    print(text[:800])
    print()
"
```

### [45] TOOL RESULT — Bash · 2026-09-25 09:35:59 UTC

```
{"stdout": "=== Round 1 (first 800 chars) ===\nResearch report after round 1. The run is still in progress: this is the report text as it stands after this round, text only, with\nno ﬁgures. The results and the writing are not ﬁnal.\nGold-Free Faithfulness Metrics for NL-to-FOL Translation\nFraming\nTranslating natural language into ﬁrst-order logic (NL-FOL) is a prerequisite for neurosymbolic\nreasoning pipelines [10], yet evaluating whether a candidate formula faithfully captures a\nsentence's meaning remains an open problem. Gold FOL annotations are expensive, non-unique,\nand unreliable: Brunello et al. [3] found that approximately 42% of entries in both FOLIO [1] and\nMALLS [2] contain incorrect formalisations. Existing metrics either require a gold formula (exact\nmatch, prover-checked equivalence) or only verify that the output parses [5\n\n=== Round 2 (first 800 chars) ===\nResearch report after round 2. The run is still in progress: this is the report text as it stands after this round, text only, with\nno ﬁgures. The results and the writing are not ﬁnal.\nGold-Free Faithfulness Metrics for NL-to-FOL Translation\nFraming\nTranslating natural language into ﬁrst-order logic (NL-FOL) is a prerequisite for neurosymbolic\nreasoning pipelines [10], yet evaluating whether a candidate formula faithfully captures a\nsentence's meaning remains an open problem. Gold FOL annotations are expensive, non-unique,\nand unreliable: Brunello et al. [3] found that approximately 42% of entries in both FOLIO [1] and\nMALLS [2] contain incorrect formalisations. Existing metrics either require a gold formula (exact\nmatch, prover-checked equivalence) or only verify that the output parses [5\n\n=== Round 3 (first 800 chars) ===\nResearch report after round 3. The run is still in progress: this is the report text as it stands after this round, text only, with\nno ﬁgures. The results and the writing are not ﬁnal.\nGold-Free Faithfulness Metrics for NL-to-FOL Translation\nFraming\nTranslating natural language into ﬁrst-order logic (NL-FOL) is a prerequisite for neurosymbolic\nreasoning pipelines [10], yet evaluating whether a candidate formula faithfully captures a\nsentence's meaning remains an open problem. Gold FOL annotations are expensive, non-unique,\nand unreliable: Brunello et al. [3] found that approximately 42% of entries in both FOLIO [1] and\nMALLS [2] contain incorrect formalisations. Existing metrics either require a gold formula (exact\nmatch, prover-checked equivalence) or only verify that the output parses [5\n\n=== Round 4 (first 800 chars) ===\nResearch report after round 4. The run is still in progress: this is the report text as it stands after this round, text only, with\nno ﬁgures. The results and the writing are not ﬁnal.\nGold-Free Faithfulness Metrics for NL-to-FOL Translation\nFraming\nTranslating natural language into ﬁrst-order logic (NL-FOL) is a prerequisite for neurosymbolic\nreasoning pipelines [10], yet evaluating whether a candidate formula faithfully captures a\nsentence's meaning remains an open problem. Gold FOL annotations are expensive, non-unique,\nand unreliable: Brunello et al. [3] found that approximately 42% of entries in both FOLIO [1] and\nMALLS [2] contain incorrect formalisations. Existing metrics either require a gold formula (exact\nmatch, prover-checked equivalence) or only verify that the output parses [5\n\n=== Round 5 (first 800 chars) ===\nResearch report after round 5. The run is still in progress: this is the report text as it stands after this round, text only, with\nno ﬁgures. The results and the writing are not ﬁnal.\nGold-Free Faithfulness Metrics for NL-to-FOL Translation\nFraming\nTranslating natural language into ﬁrst-order logic (NL-FOL) is a prerequisite for neurosymbolic\nreasoning pipelines [10], yet evaluating whether a candidate formula faithfully captures a\nsentence's meaning remains an open problem. Gold FOL annotations are expensive, non-unique,\nand unreliable: Brunello et al. [3] found that approximately 42% of entries in both FOLIO [1] and\nMALLS [2] contain incorrect formalisations. Existing metrics either require a gold formula (exact\nmatch, prover-checked equivalence) or only verify that the output parses [5", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [46] TOOL CALL — Bash · 2026-09-25 09:36:07 UTC

```
Extract all GitHub URLs from round reports:
cd /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo && python3 -c "
import pymupdf
import re

all_urls = set()
for i in range(1,6):
    doc = pymupdf.open(f'round_reports/round-{i}.pdf')
    for page in doc:
        text = page.get_text()
        urls = re.findall(r'https?://github\.com/[^\s\)\"]+', text)
        for u in urls:
            u = u.rstrip('.,;:')
            all_urls.add(u)
        # Also check links
        for link in page.get_links():
            uri = link.get('uri', '')
            if 'github.com' in uri:
                all_urls.add(uri)
    doc.close()

for u in sorted(all_urls):
    print(u)
"
```

### [47] TOOL RESULT — Bash · 2026-09-25 09:36:07 UTC

```
{"stdout": "", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [48] TOOL CALL — Bash · 2026-09-25 09:36:13 UTC

```
Check for hyperlinks in round report PDFs:
cd /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo && python3 -c "
import pymupdf

# Check links in each round report
for i in range(1,6):
    doc = pymupdf.open(f'round_reports/round-{i}.pdf')
    links = []
    for page in doc:
        for link in page.get_links():
            uri = link.get('uri', '')
            if uri:
                links.append(uri)
    doc.close()
    if links:
        print(f'Round {i}: {len(links)} links')
        for l in links[:5]:
            print(f'  {l}')
    else:
        print(f'Round {i}: no links')
"
```

### [49] TOOL RESULT — Bash · 2026-09-25 09:36:13 UTC

```
{"stdout": "Round 1: no links\nRound 2: no links\nRound 3: no links\nRound 4: no links\nRound 5: no links", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [50] ASSISTANT · 2026-09-25 09:36:33 UTC

```
Let me check if there's a report PDF and extract URLs from the paper PDF.
```

### [51] TOOL CALL — Bash · 2026-09-25 09:36:33 UTC

```
Extract all URLs/links from the paper PDF:
python3 -c "
import pymupdf, re

doc = pymupdf.open('paper.pdf')
links = []
for page in doc:
    for link in page.get_links():
        uri = link.get('uri', '')
        if uri:
            links.append(uri)
doc.close()
for l in sorted(set(links)):
    print(l)
"
```

### [52] TOOL RESULT — Bash · 2026-09-25 09:36:33 UTC

```
{"stdout": "https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-1\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-3\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-4\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-2/experiment-5\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/evaluation-2\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-6\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-7\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-8\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/dataset-4\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/experiment-9\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-13", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [53] TOOL CALL — Bash · 2026-09-25 09:36:41 UTC

```
Find report files:
cd /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper && python3 -c "
import pymupdf, re, os

# Check report workspace for report PDF
for root, dirs, files in os.walk('report_workspace'):
    for f in files:
        print(os.path.join(root, f))
" && echo "---" && ls -la report_latex/ 2>/dev/null
```

### [54] TOOL RESULT — Bash · 2026-09-25 09:36:41 UTC

```
{"stdout": "report_workspace/.terminal_claude_agent_struct_out.json\nreport_workspace/exec_summary.pdf\nreport_workspace/exec_summary.out\nreport_workspace/exec_summary.aux\nreport_workspace/exec_summary.log\nreport_workspace/report.toc\nreport_workspace/report.pdf\nreport_workspace/report.out\nreport_workspace/report.aux\nreport_workspace/report.log\nreport_workspace/exec_summary.tex\nreport_workspace/report.tex\nreport_workspace/.aii_claude_session.json\nreport_workspace/.repl_agent.ptylog\nreport_workspace/.aii/module_end.json\nreport_workspace/.aii/manifest.yaml\nreport_workspace/figures/fig_confirmation_landscape_v0.pdf\nreport_workspace/figures/fig_vocabulary_source_v0.pdf\nreport_workspace/figures/fig_csc_anchoring_v0.pdf\nreport_workspace/figures/fig_dev_set_auroc_v0.pdf\nreport_workspace/figures/fig_summary_comparison_v0.pdf\nreport_workspace/figures/fig_baseline_auroc_v0.pdf\nreport_workspace/figures/fig_consensus_auroc_v0.pdf\nreport_workspace/figures/fig_rewrite_fa_v0.pdf\n---\ntotal 4119\ndrwxr-xr-x 3 root root 1037915 Sep 25 09:26 .\ndrwxr-xr-x 5 root root 2000475 Sep 25 09:26 ..\n-rw-r--r-- 1 root root    6796 Sep 25 09:26 exec_summary.tex\ndrwxr-xr-x 2 root root 1022753 Sep 25 09:26 figures\n-rw-r--r-- 1 root root  148454 Sep 25 09:26 report.tex", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [55] TOOL CALL — Bash · 2026-09-25 09:36:47 UTC

```
Extract GitHub URLs from the report PDF:
cd /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper && python3 -c "
import pymupdf

doc = pymupdf.open('report_workspace/report.pdf')
links = []
for page in doc:
    for link in page.get_links():
        uri = link.get('uri', '')
        if uri and 'github.com' in uri:
            links.append(uri)
doc.close()
for l in sorted(set(links)):
    print(l)
"
```

### [56] TOOL RESULT — Bash · 2026-09-25 09:36:47 UTC

```
{"stdout": "", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [57] TOOL CALL — Bash · 2026-09-25 09:36:51 UTC

```
Extract all URLs from the report PDF:
cd /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper && python3 -c "
import pymupdf

doc = pymupdf.open('report_workspace/report.pdf')
links = []
for page in doc:
    for link in page.get_links():
        uri = link.get('uri', '')
        if uri:
            links.append(uri)
doc.close()
for l in sorted(set(links)):
    print(l)
"
```

### [58] TOOL RESULT — Bash · 2026-09-25 09:36:51 UTC

```
{"stdout": "", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [59] TOOL CALL — Bash · 2026-09-25 09:36:55 UTC

```
Extract GitHub URLs from report LaTeX source:
grep -o 'https://github\.com[^}]*' /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/report_workspace/report.tex | sort -u
```

### [60] TOOL RESULT — Bash · 2026-09-25 09:36:55 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [61] TOOL CALL — Bash · 2026-09-25 09:37:01 UTC

```
Find round/artifact references in report.tex:
grep -o 'round-[0-9]*/[a-z]*-[0-9]*' /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/report_workspace/report.tex | sort -u
```

### [62] TOOL RESULT — Bash · 2026-09-25 09:37:01 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [63] TOOL CALL — Bash · 2026-09-25 09:37:05 UTC

```
Search for artifact references in report.tex:
grep -iE '(experiment|evaluation|dataset|research)[\-_][0-9]+' /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/report_workspace/report.tex | head -20
```

### [64] TOOL RESULT — Bash · 2026-09-25 09:37:05 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [65] ASSISTANT · 2026-09-25 09:40:42 UTC

```
Good. I have 11 footnote URLs from the paper and the CDN/repo URL patterns from the previous run. Let me build the index.html now.
```

### [66] TOOL CALL — Write · 2026-09-25 09:40:42 UTC

```
File: /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/index.html

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pre-Registered Cross-Family Solver Consensus Outperforms LLM Judges on Templated NL-to-FOL Translation</title>
<style>
:root {
  --bg: #faf9f6;
  --fg: #1a1a1a;
  --fg2: #444;
  --fg3: #666;
  --border: #ddd;
  --card-bg: #fff;
  --card-shadow: rgba(0,0,0,.08);
  --accent: #1a6b4a;
  --accent-bg: #e8f5ee;
  --accent2: #c77d1a;
  --accent2-bg: #fff5e6;
  --hero-bg: #f0f7f3;
  --table-stripe: #f7f7f5;
  --code-bg: #f4f3f0;
  --nav-bg: rgba(250,249,246,.95);
  --lightbox-bg: rgba(0,0,0,.85);
  --tile-bg: #f0f7f3;
}
@media(prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --bg: #181a1b;
    --fg: #e0ddd8;
    --fg2: #b0ada6;
    --fg3: #8a8780;
    --border: #333;
    --card-bg: #222;
    --card-shadow: rgba(0,0,0,.3);
    --accent: #4cc88a;
    --accent-bg: #1a2e23;
    --accent2: #e8a940;
    --accent2-bg: #2a2010;
    --hero-bg: #1a2e23;
    --table-stripe: #1e2021;
    --code-bg: #1e1e1e;
    --nav-bg: rgba(24,26,27,.95);
    --lightbox-bg: rgba(0,0,0,.92);
    --tile-bg: #1a2e23;
  }
}
:root[data-theme="dark"]{
  --bg: #181a1b;
  --fg: #e0ddd8;
  --fg2: #b0ada6;
  --fg3: #8a8780;
  --border: #333;
  --card-bg: #222;
  --card-shadow: rgba(0,0,0,.3);
  --accent: #4cc88a;
  --accent-bg: #1a2e23;
  --accent2: #e8a940;
  --accent2-bg: #2a2010;
  --hero-bg: #1a2e23;
  --table-stripe: #1e2021;
  --code-bg: #1e1e1e;
  --nav-bg: rgba(24,26,27,.95);
  --lightbox-bg: rgba(0,0,0,.92);
  --tile-bg: #1a2e23;
}
[hidden]{display:none !important}
*,*::before,*::after{box-sizing:border-box}
body{
  margin:0; padding:0;
  font-family:'Iowan Old Style','Palatino Linotype',Palatino,Georgia,serif;
  background:var(--bg); color:var(--fg);
  line-height:1.65; font-size:17px;
}
a{color:var(--accent); text-decoration:none}
a:hover{text-decoration:underline}
h1,h2,h3{font-weight:600; line-height:1.25; margin:0 0 .5em}
h1{font-size:1.6em}
h2{font-size:1.3em; border-bottom:2px solid var(--accent); padding-bottom:.25em; margin-top:2em}
h3{font-size:1.1em; color:var(--fg2)}
code{font-family:'SF Mono',Monaco,'Cascadia Code','Consolas',monospace; font-size:.88em; background:var(--code-bg); padding:1px 5px; border-radius:3px}
.wrap{max-width:860px; margin:0 auto; padding:0 16px}
/* --- Hero --- */
.hero{background:var(--hero-bg); padding:2.5em 0 2em; border-bottom:1px solid var(--border)}
.hero h1{color:var(--accent); font-size:1.5em; margin-bottom:.3em}
.hero .author{color:var(--fg3); font-size:.95em; margin-bottom:.8em}
.hero-links{display:flex; flex-wrap:wrap; gap:.5em}
.hero-links a{
  display:inline-flex; align-items:center; gap:.3em;
  background:var(--accent); color:#fff; padding:.4em 1em;
  border-radius:5px; font-size:.88em; font-weight:600;
}
.hero-links a:hover{opacity:.85; text-decoration:none}
/* --- Nav --- */
nav.side{
  position:sticky; top:1em; float:left; width:170px;
  margin-left:-190px; font-size:.82em;
}
nav.side a{
  display:block; padding:3px 8px; color:var(--fg3);
  border-left:2px solid transparent; margin-bottom:2px;
}
nav.side a.active{border-left-color:var(--accent); color:var(--accent); font-weight:600}
nav.side a:hover{color:var(--accent); text-decoration:none}
nav.mobile{
  display:none; position:sticky; top:0; z-index:50;
  background:var(--nav-bg); border-bottom:1px solid var(--border);
  overflow-x:auto; white-space:nowrap; padding:6px 16px;
  -webkit-overflow-scrolling:touch;
}
nav.mobile a{
  display:inline-block; padding:4px 10px; font-size:.8em; color:var(--fg3);
  border-bottom:2px solid transparent;
}
nav.mobile a.active{color:var(--accent); border-bottom-color:var(--accent); font-weight:600}
nav.mobile a:hover{color:var(--accent); text-decoration:none}
@media(max-width:1100px){
  nav.side{display:none}
  nav.mobile{display:block}
}
/* --- Main --- */
main{margin-left:0; padding:1.5em 0 3em}
@media(min-width:1101px){
  main{margin-left:0; position:relative}
}
/* --- Cards --- */
.cards{display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:1em; margin:1em 0}
.card{
  background:var(--card-bg); border:1px solid var(--border);
  border-radius:8px; padding:1em; box-shadow:0 1px 4px var(--card-shadow);
}
.card h3{font-size:1em; color:var(--accent); margin-bottom:.4em}
.card p{font-size:.9em; color:var(--fg2); margin:0}
/* --- Tables --- */
.tbl-wrap{overflow-x:auto; margin:1em 0}
table{width:100%; border-collapse:collapse; font-size:.88em}
th{text-align:left; font-weight:600; border-bottom:2px solid var(--border); padding:6px 10px}
td{padding:6px 10px; border-bottom:1px solid var(--border)}
tr:nth-child(even){background:var(--table-stripe)}
/* --- Tiles --- */
.tiles{display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:1em; margin:1em 0}
.tile{
  background:var(--tile-bg); border-radius:8px; padding:1.2em;
  text-align:center; border:1px solid var(--border);
}
.tile .num{font-size:2em; font-weight:700; color:var(--accent); line-height:1.1}
.tile .lbl{font-size:.82em; color:var(--fg3); margin-top:.3em}
/* --- Figures --- */
.fig{margin:1.5em 0; text-align:center}
.fig img{
  max-width:100%; height:auto; border:1px solid var(--border);
  border-radius:6px; cursor:pointer; transition:box-shadow .2s;
}
.fig img:hover{box-shadow:0 2px 12px var(--card-shadow)}
.fig figcaption{font-size:.82em; color:var(--fg3); margin-top:.5em; max-width:700px; display:inline-block; text-align:left}
/* --- Lightbox --- */
.lightbox{
  position:fixed; inset:0; z-index:1000;
  background:var(--lightbox-bg);
  display:flex; align-items:center; justify-content:center;
  padding:2em;
}
.lightbox img{max-width:100%; max-height:90vh; border-radius:6px}
.lightbox-close{
  position:absolute; top:12px; right:16px;
  background:none; border:none; color:#fff; font-size:2em;
  cursor:pointer; line-height:1;
}
/* --- Artifacts --- */
.artifacts{list-style:none; padding:0; margin:1em 0; columns:2; column-gap:1.5em}
.artifacts li{break-inside:avoid; margin-bottom:.5em; font-size:.9em}
.artifacts li::before{content:""; display:inline-block; width:6px; height:6px; background:var(--accent); border-radius:50%; margin-right:6px; vertical-align:middle}
@media(max-width:600px){.artifacts{columns:1}}
/* --- Footer --- */
footer{border-top:1px solid var(--border); padding:2em 0; margin-top:2em}
footer .links{display:flex; flex-wrap:wrap; gap:1em; margin-bottom:1em}
footer .links a{font-size:.9em}
.citation{background:var(--code-bg); padding:1em; border-radius:6px; font-size:.82em; font-family:'SF Mono',Monaco,'Cascadia Code','Consolas',monospace; white-space:pre-wrap; word-break:break-all}
/* --- Abstract --- */
.abstract{
  background:var(--card-bg); border:1px solid var(--border);
  border-radius:8px; padding:1.2em 1.5em; margin:1em 0;
  font-size:.95em; color:var(--fg2);
}
.abstract strong{color:var(--fg)}
/* --- Limitations --- */
.limitations{list-style:decimal; padding-left:1.5em}
.limitations li{margin-bottom:.6em; font-size:.92em}
</style>
</head>
<body>

<div class="hero">
  <div class="wrap">
    <h1>Pre-Registered Cross-Family Solver Consensus Outperforms LLM Judges on Templated NL-to-FOL Translation with a Supplied Predicate Signature</h1>
    <div class="author">Anonymous</div>
    <div class="hero-links">
      <a href="https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/paper.pdf">Paper (PDF)</a>
      <a href="https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/report.pdf">Report (PDF)</a>
      <a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3">Code Repository</a>
    </div>
  </div>
</div>

<nav class="mobile" aria-label="Sections">
  <a href="#abstract">Abstract</a>
  <a href="#contributions">Contributions</a>
  <a href="#method">Method</a>
  <a href="#results-sig">SIG Results</a>
  <a href="#results-dev">Dev Results</a>
  <a href="#results-free">Free OOS</a>
  <a href="#mechanism">Mechanism</a>
  <a href="#rename">Rename</a>
  <a href="#confirmation">Confirmation</a>
  <a href="#limitations">Limitations</a>
  <a href="#artifacts">Artifacts</a>
</nav>

<div class="wrap" style="position:relative">
  <nav class="side" aria-label="Sections">
    <a href="#abstract">Abstract</a>
    <a href="#contributions">Contributions</a>
    <a href="#method">Method</a>
    <a href="#results-sig">SIG Results</a>
    <a href="#results-dev">Dev Results</a>
    <a href="#results-free">Free OOS</a>
    <a href="#mechanism">Mechanism</a>
    <a href="#rename">Rename</a>
    <a href="#confirmation">Confirmation</a>
    <a href="#limitations">Limitations</a>
    <a href="#artifacts">Artifacts</a>
  </nav>

  <main>

    <section id="abstract">
      <h2>Abstract</h2>
      <div class="abstract">
        Evaluating the faithfulness of NL&#8594;FOL translations is hampered by the expense and unreliability of gold-standard references: roughly <strong>40%</strong> of annotations in standard benchmarks contain errors. We study a gold-free alternative based on <strong>cross-family solver consensus</strong>: collect translations from multiple independent LLM families, check pairwise equivalence with an SMT solver, and score each candidate by the fraction of cross-family peers that disagree with it. In a pre-registered evaluation on <strong>221 templated long-exception sentences</strong> with a supplied predicate signature, consensus achieves a within-template AUROC of <strong>0.954</strong> versus <strong>0.587</strong> for a disguised API judge (&Delta;&nbsp;=&nbsp;+0.367 [+0.328,&nbsp;+0.404]), flat across word-length terciles. Under free vocabulary, consensus still outperforms judges on both development data (&Delta;&nbsp;=&nbsp;+0.099) and untouched out-of-sample sentences (&Delta;&nbsp;=&nbsp;+0.171), but the advantage shrinks by roughly 0.15&nbsp;AUROC and a fundamental <strong>rename tradeoff</strong> emerges: any predicate-name alignment needed to compare independently generated formulas produces a high false-alarm rate on meaning-preserving renames. Confirmation on independent held-out data was budget-stopped and remains incomplete.
      </div>
    </section>

    <section id="contributions">
      <h2>Contributions</h2>
      <div class="cards">
        <div class="card">
          <h3>Pre-Registered SIG Evaluation</h3>
          <p>Within-template AUROC 0.954 vs 0.587 for a disguised judge (&Delta;&nbsp;=&nbsp;+0.367) on 221 sentences under shared signature, flat across word-length terciles. Zero error endorsement.</p>
        </div>
        <div class="card">
          <h3>Free-Vocabulary Dev Results</h3>
          <p>Consensus outperforms judges by &Delta;&nbsp;=&nbsp;+0.099 [+0.049,&nbsp;+0.146] on stratified AUROC (n&nbsp;=&nbsp;2,686). Aligner-free c_exact at 0.689 provides 78% of above-chance signal from structural agreement alone.</p>
        </div>
        <div class="card">
          <h3>Untouched Free OOS</h3>
          <p>R_COMP FREE: &Delta;&nbsp;=&nbsp;+0.171 vs original-view judge under provisional labels. Consensus reaches 94% of frontier judge AUROC. Two-auditor &Delta;&nbsp;=&nbsp;+0.105.</p>
        </div>
        <div class="card">
          <h3>Rename Tradeoff</h3>
          <p>76.5% false-alarm rate under nonce renames. No alignment variant eliminates this without sacrificing error recall. The name-free variant (c_nf) has zero rename flip but AUROC drops to 0.686.</p>
        </div>
      </div>
    </section>

    <section id="method">
      <h2>Method</h2>
      <h3>Consensus Scoring</h3>
      <p>Given a sentence <em>s</em> and candidate FOL translation <em>c</em>, collect peer translations {<em>p</em><sub>1</sub>,&nbsp;&hellip;,&nbsp;<em>p<sub>k</sub></em>} from <em>k</em> independent LLM families. Score the candidate as:</p>
      <p style="text-align:center; font-size:1.05em"><code>c_score(c, s) = 1 - (1/k) &sum; 1[equiv(c, p<sub>i</sub>)]</code></p>
      <p>Under <strong>shared signature</strong> (c_score_sig), all translators use a supplied predicate vocabulary and <code>equiv</code> is a direct Z3 check. Under <strong>free vocabulary</strong> (c_score_align), each translator chooses its own names and <code>equiv</code> requires a predicate-name aligner before Z3.</p>

      <h3>Predicate Alignment (Free Vocabulary)</h3>
      <p>Independent translators choose different predicate names (e.g. <code>Runs(x)</code> vs <code>IsRunner(x)</code>). The aligner combines three cost components:</p>
      <ol>
        <li><strong>Structural cost</strong>: polarity profile, argument-count match, nesting depth</li>
        <li><strong>Text-anchor cost</strong>: overlap between predicate-name words and source-sentence tokens (Porter stemming, WordNet synonyms)</li>
        <li><strong>Semantic signature</strong>: truth-value profiles over random finite interpretations</li>
      </ol>
      <p>The <em>k</em> cheapest bijections are evaluated; the pair is declared equivalent if any bijection yields a Z3-verified equivalence.</p>

      <h3>Score Variants</h3>
      <ul>
        <li><strong>c_exact</strong>: no alignment; exact-match equivalence only. Immune to rename false alarms.</li>
        <li><strong>c_nf</strong> (name-free): alignment by structural and semantic signatures only, ignoring text anchoring.</li>
        <li><strong>p_peer_text</strong>: logistic fusion of consensus features with text-side features (bag-of-words coverage, role accounting, Z3 structural match).</li>
      </ul>

      <h3>Evaluation Framework</h3>
      <p><strong>Shared-signature labels</strong> (R_COMP): Z3 equivalence to trusted-by-construction references (one weak, one strong reading per template). No human or LLM judgement in the labelling loop.</p>
      <p><strong>Free-vocabulary labels</strong> (set E): three-person expert panel. R_COMP FREE: provisional search-based classifications (non-confirmatory).</p>
      <p><strong>Primary metric</strong>: stratified AUROC (items paired only within the same source stratum). Confidence intervals via sentence-cluster percentile bootstrap (B&nbsp;=&nbsp;2,000).</p>
    </section>

    <section id="results-sig">
      <h2>Shared-Signature Results (R_COMP-SIG)</h2>

      <div class="tiles">
        <div class="tile">
          <div class="num">0.954</div>
          <div class="lbl">Consensus AUROC<br>(c_score_sig)</div>
        </div>
        <div class="tile">
          <div class="num">0.587</div>
          <div class="lbl">Judge AUROC<br>(flash-lite, disguised)</div>
        </div>
        <div class="tile">
          <div class="num">+0.367</div>
          <div class="lbl">&Delta; Consensus &minus; Judge<br>[+0.328, +0.404]</div>
        </div>
      </div>

      <p>On 1,904 rows where both scores exist. Population: 429 ERROR / 1,595 CORRECT (21.2% error rate) from 221 sentences, 10 LLM slots across 9 vendor families. Error endorsement is zero (<em>e</em>&nbsp;=&nbsp;0): no error item scores below the decision threshold. Among 429 error items, 75.3% receive the maximum score of 1.0.</p>

      <div class="tbl-wrap">
        <table>
          <caption style="text-align:left; font-size:.85em; color:var(--fg3); margin-bottom:.5em">Table 1: Within-template AUROC on R_COMP-SIG (221 sentences, pure Z3 labels)</caption>
          <thead><tr><th>Metric</th><th><em>n</em></th><th>AUROC [95% CI]</th><th>&Delta; vs disg. judge</th></tr></thead>
          <tbody>
            <tr><td>c_score_sig</td><td>1,904</td><td>0.954 [0.939, 0.968]</td><td>+0.367 [+0.328, +0.404]</td></tr>
            <tr><td>c_score_align</td><td>1,904</td><td>0.954 [0.939, 0.968]</td><td>+0.367 [+0.328, +0.404]</td></tr>
            <tr><td>judge (flash-lite, disg.)</td><td>1,904</td><td>0.587 [0.551, 0.622]</td><td>&mdash;</td></tr>
            <tr><td>judge (flash-lite, orig.)</td><td>1,932</td><td>0.673 [0.637, 0.708]</td><td></td></tr>
            <tr><td>judge (frontier, orig.)</td><td>60</td><td>0.932 [0.782, 1.000]</td><td></td></tr>
            <tr><td>judge (local, disg.)</td><td>2,024</td><td>0.498 [0.459, 0.534]</td><td></td></tr>
          </tbody>
        </table>
      </div>

      <h3>Flat with Sentence Length</h3>
      <p>Unlike the free-vocabulary setting, consensus under shared signature is flat across word-length terciles: W1 0.959, W2 0.947, W3 0.953.</p>

      <div class="tbl-wrap">
        <table>
          <caption style="text-align:left; font-size:.85em; color:var(--fg3); margin-bottom:.5em">Table 2: R_COMP-SIG AUROC by word-length tercile</caption>
          <thead><tr><th>Tercile</th><th><em>n</em></th><th>ERR/COR</th><th>c_sig</th><th>judge (disg.)</th><th>&Delta; [CI]</th></tr></thead>
          <tbody>
            <tr><td>W1 (shortest)</td><td>503</td><td>125/449</td><td>0.959</td><td>0.578</td><td>+0.382 [+0.278, +0.472]</td></tr>
            <tr><td>W2</td><td>712</td><td>149/594</td><td>0.947</td><td>0.624</td><td>+0.331 [+0.253, +0.421]</td></tr>
            <tr><td>W3 (longest)</td><td>689</td><td>155/552</td><td>0.953</td><td>0.567</td><td>+0.388 [+0.301, +0.471]</td></tr>
          </tbody>
        </table>
      </div>

      <figure class="fig" id="fig-sig-tercile">
        <img src="figures/fig_sig_tercile_v0.png" alt="R_COMP-SIG AUROC by word-length tercile" loading="lazy" width="800" height="500">
        <figcaption>Figure 1: Within-template AUROC on R_COMP-SIG by word-length tercile. Consensus (blue) is flat (0.947&ndash;0.959); the disguised judge (orange) hovers near chance (0.567&ndash;0.624).</figcaption>
      </figure>

      <p><strong>Frontier judge comparison</strong>: On a 60-row subsample, consensus achieves 0.956 [0.889, 1.000] vs 0.932 [0.855, 0.990] for the frontier judge (Gemini 3.1 Pro).</p>

      <p><strong>Scope</strong>: R_COMP-SIG uses templated sentences with a supplied predicate vocabulary. The shared signature eliminates the alignment problem entirely. These results do not extend to free-vocabulary settings.</p>
    </section>

    <section id="results-dev">
      <h2>Free-Vocabulary Development Results (Set E)</h2>

      <figure class="fig" id="fig-dev-auroc">
        <img src="figures/fig_dev_auroc_v0.png" alt="Stratified AUROC on development set E" loading="lazy" width="800" height="500">
        <figcaption>Figure 2: Stratified AUROC on the free-vocabulary development dataset. Consensus-based metrics (blue) outperform API judges (orange) and other baselines (gray). Error bars: 95% sentence-cluster bootstrap CIs.</figcaption>
      </figure>

      <div class="tbl-wrap">
        <table>
          <caption style="text-align:left; font-size:.85em; color:var(--fg3); margin-bottom:.5em">Table 3: Stratified AUROC on development set E (R_AB, n = 2,686)</caption>
          <thead><tr><th>Metric</th><th>Strat AUROC [95% CI]</th><th>$/item</th></tr></thead>
          <tbody>
            <tr><td>c_score_align</td><td>0.741 [0.705, 0.775]</td><td>9.1e-5</td></tr>
            <tr><td>p_peer_text (fused)</td><td>0.753 [0.720, 0.784]</td><td>9.1e-5</td></tr>
            <tr><td>c_exact (no alignment)</td><td>0.689 [0.652, 0.726]</td><td>&mdash;</td></tr>
            <tr><td>c_nf (name-free)</td><td>0.686 [0.647, 0.720]</td><td>&mdash;</td></tr>
            <tr style="border-top:2px solid var(--border)"><td>flash-lite judge (disg.)</td><td>0.642 [0.607, 0.676]</td><td>5.1e-5</td></tr>
            <tr><td>flash-lite judge (orig.)</td><td>0.623 [0.593, 0.651]</td><td>5.1e-5</td></tr>
            <tr><td>nano judge (disg.)</td><td>0.644 [0.609, 0.680]</td><td>2.0e-5</td></tr>
            <tr><td>local judge Qwen-8B (disg.)</td><td>0.674 [0.646, 0.703]</td><td>&mdash;</td></tr>
            <tr style="border-top:2px solid var(--border)"><td>round-trip NLI (min)</td><td>0.606 [0.569, 0.645]</td><td>2.8e-5</td></tr>
            <tr><td>self-consistency (5-sample)</td><td>0.598 [0.559, 0.637]</td><td>6.7e-5</td></tr>
            <tr style="border-top:2px solid var(--border)"><td>28-feature stack</td><td>0.735 [0.699, 0.766]</td><td>&mdash;</td></tr>
            <tr><td>28-feature stack + c_score_align</td><td>0.774 [0.743, 0.802]</td><td>&mdash;</td></tr>
          </tbody>
        </table>
      </div>

      <p>The drop from 0.952 (shared signature, full 2,024-row pool) to 0.801 (free vocabulary on the same R_COMP sentences) reflects the cost of predicate-name alignment. Aligner-free c_exact at 0.689 provides 78% of the above-chance signal from structural agreement alone; the aligner adds the remaining 22%.</p>
      <p>Adding c_score_align to the 28-feature baseline stack increases stratified AUROC by +0.039 [+0.021,&nbsp;+0.057]; permutation null test <em>p</em><sub>95</sub>&nbsp;=&nbsp;0.009.</p>
      <p><strong>Frontier judge comparison</strong>: c_score_align achieves 95.7% of the frontier judge's AUROC (ratio 0.957 [0.887, 1.034]) on a 284-row subsample.</p>
      <p><strong>System-level ranking</strong>: Kendall &tau;<sub>b</sub>&nbsp;=&nbsp;0.692 [+0.513,&nbsp;+0.795] between system mean score and error rate across 13 configurations.</p>
    </section>

    <section id="results-free">
      <h2>Free-Vocabulary Out-of-Sample (R_COMP FREE)</h2>

      <p>The same 221 R_COMP sentences translated under free vocabulary. Confirmatory labelling required a gloss gate that failed twice (balanced accuracy 0.776 and 0.561, below the 0.90 threshold), producing zero confirmed CORRECT rows. Results use provisional non-confirmatory labels.</p>

      <div class="tbl-wrap">
        <table>
          <caption style="text-align:left; font-size:.85em; color:var(--fg3); margin-bottom:.5em">Table 4: R_COMP FREE provisional AUROCs (within-template, untouched rows)</caption>
          <thead><tr><th>View</th><th><em>n</em> (ERR/MAPPED)</th><th>c_align</th><th>judge</th></tr></thead>
          <tbody>
            <tr><td>Disguised</td><td>1,706 (602/1,104)</td><td>0.801 [0.770, 0.834]</td><td>0.584 [0.550, 0.618]</td></tr>
            <tr><td>Original</td><td>1,709 (605/1,104)</td><td>0.804 [0.774, 0.836]</td><td>0.633 [0.601, 0.666]</td></tr>
          </tbody>
        </table>
      </div>

      <p>Disguised-judge &Delta;&nbsp;=&nbsp;+0.217 [+0.175, +0.260]. Original-view &Delta;&nbsp;=&nbsp;+0.171 [+0.135, +0.206]. On a 146-row two-auditor subset: &Delta;&nbsp;=&nbsp;+0.105 [+0.011, +0.215]. On a 150-row frontier-judge subsample: consensus reaches 0.94 of the frontier judge's AUROC.</p>
    </section>

    <section id="mechanism">
      <h2>Mechanism</h2>

      <p>The consensus signal decomposes into <strong>endorsement</strong> <em>e</em> (fraction of ERROR items endorsed by peers, i.e. false negatives) and <strong>divergence</strong> <em>d</em> (fraction of CORRECT items that diverge from peers, i.e. false positives). AUROC at a binary threshold equals 1&nbsp;&minus;&nbsp;(<em>e</em>&nbsp;+&nbsp;<em>d</em>)/2.</p>

      <p><strong>Shared vocabulary</strong>: <em>e</em>&nbsp;=&nbsp;0.0, <em>d</em>&nbsp;=&nbsp;0.260. Zero error endorsement; 26% false-alarm rate from valid alternative formalizations. Flat across sentence lengths.</p>

      <p><strong>Free vocabulary</strong>: Net degradation &Delta;(<em>e</em>&nbsp;+&nbsp;<em>d</em>)&nbsp;=&nbsp;+0.356 [+0.198,&nbsp;+0.493] from short to long sentences, driven almost entirely by divergence (&Delta;<em>d</em>&nbsp;=&nbsp;+0.608, &Delta;<em>e</em>&nbsp;=&nbsp;&minus;0.252). As formulas grow longer, the predicate-name aligner increasingly makes mistakes.</p>

      <figure class="fig" id="fig-complexity">
        <img src="figures/fig_complexity_v0.png" alt="Endorsement and divergence by sentence-length tercile" loading="lazy" width="800" height="500">
        <figcaption>Figure 3: Decomposition of free-vocabulary consensus error rates by sentence-length tercile. Endorsement <em>e</em> decreases with length, but divergence <em>d</em> increases sharply, producing net degradation of +0.356. Under shared signature, this degradation is absent.</figcaption>
      </figure>

      <h3>Family Sufficiency</h3>
      <p>Three peer families suffice for 97% of full-pool AUROC (<em>k</em><sub>95</sub>&nbsp;=&nbsp;3), but the long-sentence tercile requires <em>k</em><sub>95</sub>&nbsp;=&nbsp;5.</p>

      <div class="tbl-wrap">
        <table>
          <caption style="text-align:left; font-size:.85em; color:var(--fg3); margin-bottom:.5em">Table 5: Free-vocabulary AUROC by number of peer families</caption>
          <thead><tr><th><em>k</em></th><th>AUROC (overall)</th><th>AUROC (long, T3)</th></tr></thead>
          <tbody>
            <tr><td>1</td><td>0.685</td><td>0.581</td></tr>
            <tr><td>3</td><td>0.757</td><td>0.651</td></tr>
            <tr><td>5</td><td>0.776</td><td>0.698</td></tr>
            <tr><td>7</td><td>0.784</td><td>0.726</td></tr>
          </tbody>
        </table>
      </div>

      <figure class="fig" id="fig-k-curve">
        <img src="figures/fig_k_curve_v0.png" alt="AUROC vs number of peer families" loading="lazy" width="800" height="500">
        <figcaption>Figure 4: Stratified AUROC as a function of peer families <em>k</em>. Three families capture 97% of the full-pool signal, but long sentences require five families to reach 95%.</figcaption>
      </figure>
    </section>

    <section id="rename">
      <h2>The Rename Tradeoff</h2>

      <p>The predicate aligner that enables free-vocabulary comparison introduces a fundamental false-alarm vulnerability. When correct formulas are copied with meaning-preserving renames, the consensus score should not change. In practice:</p>

      <div class="tbl-wrap">
        <table>
          <caption style="text-align:left; font-size:.85em; color:var(--fg3); margin-bottom:.5em">Table 6: False-alarm rates on meaning-preserving renames of CORRECT candidates</caption>
          <thead><tr><th>Metric</th><th>NONCE FA</th><th>NONCE flip</th><th>SYN FA</th><th>SYN flip</th></tr></thead>
          <tbody>
            <tr><td>c_align</td><td>0.765</td><td>0.605</td><td>0.565</td><td>0.313</td></tr>
            <tr><td>c_nf (name-free)</td><td>0.132</td><td>0.000</td><td>0.201</td><td>0.000</td></tr>
            <tr><td>p_peer_text</td><td>1.000</td><td>0.821</td><td>0.216</td><td>0.080</td></tr>
            <tr><td>judge (disg.)</td><td>0.229</td><td>0.134</td><td>0.085</td><td>0.058</td></tr>
          </tbody>
        </table>
      </div>

      <p>The name-free variant c_nf eliminates rename sensitivity (flip&nbsp;=&nbsp;0) but at the cost of within-base AUROC 0.499 (chance level) and lower overall discrimination (0.686 vs 0.741). This tradeoff explains the gap between shared-signature and free-vocabulary performance.</p>

      <h3>Per-Type Sensitivity</h3>
      <p>On the PERTURB suite (4,234 typed mutants + 868 controls), consensus recall at the primary threshold is flat across error operators: NEG 0.761, SWAP 0.758, DROP 0.721, ADD 0.763, MEANING_RENAME 0.762. Error typing under free vocabulary achieves only 0.123 [0.081, 0.169] accuracy, below both the judge (0.326) and peer-medoid baseline (0.328).</p>
    </section>

    <section id="confirmation">
      <h2>Confirmation Status</h2>
      <p>Independent confirmation on held-out data remains incomplete. A fresh dataset (E2-A, 550 new sentences) was constructed but the budget was exhausted before enough items could be labelled.</p>
      <ul>
        <li><strong>DT stratum</strong> (short, ProverQA): consensus AUROC 0.916, tying Qwen-8B judge (&Delta;&nbsp;=&nbsp;+0.003 [&minus;0.042, +0.052]).</li>
        <li><strong>L25 stratum</strong>: c_score_align falls to 0.443 on only 42 items (35 ERROR / 7 CORRECT), below chance, but extreme variance with only 7 CORRECT items from 3 sentences.</li>
      </ul>
      <p>Every pre-registered criterion on the target strata returned NOT_TESTABLE or unfavourable.</p>

      <h3>Dead Ends</h3>
      <p>Investigated and abandoned: fused structural-feature filter (false-alarm gate failure); name-free consensus c_nf (rename-invariant but blind to meaning-rename errors); decomposed solver-based semantic reader (balanced accuracy 0.476); LLM adjudication of disputed items (balanced accuracy 0.662); candidate-signature consensus (error endorsement rose to 0.459 because peers reproduced the candidate's errors).</p>
    </section>

    <section id="limitations">
      <h2>Limitations</h2>
      <ol class="limitations">
        <li><strong>Shared-signature scope.</strong> The 0.954 AUROC uses templated sentences with a supplied predicate vocabulary. The templates and supplied signature limit scope to controlled evaluation settings.</li>
        <li><strong>Development data overlap.</strong> R_COMP-SIG later served as development data for aligner tuning. Pre-registration ensures the SIG result is uncontaminated, but the dev-set numbers from E are not independent.</li>
        <li><strong>Rename vulnerability.</strong> Under free vocabulary, a 76.5% false-alarm rate on nonce renames means the metric systematically penalises non-standard predicate names, even if semantically correct.</li>
        <li><strong>Length degradation (free vocabulary).</strong> Net degradation +0.356 from short to long sentences, driven by correct-translation divergence. Weakest on the longest, most complex sentences.</li>
        <li><strong>Provisional labels.</strong> R_COMP FREE uses non-confirmatory labels; the two-auditor subset &Delta;&nbsp;=&nbsp;+0.105 has a CI that barely excludes zero.</li>
        <li><strong>Label dependence.</strong> Development results on E depend on a three-person panel whose agreement is imperfect. The metric's advantage could partly reflect panel biases.</li>
        <li><strong>Cost.</strong> Consensus requires <em>k</em> peer translations per sentence. In this experiment (k&nbsp;=&nbsp;9), amortised cost is about 19&times; a single cheap judge call.</li>
        <li><strong>Domain.</strong> All results are English&#8594;FOL from MALLS, ProverQA, and R_COMP. Generalisation to other formalisms, languages, or distributions is untested.</li>
      </ol>
    </section>

    <section id="artifacts">
      <h2>Code Artifacts</h2>
      <ul class="artifacts">
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-1">Consensus scoring</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-3">Development set E</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-4">Baselines</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-2/experiment-5">p_peer_text (fused)</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-6">Dev results evaluation</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-7">R_COMP dataset</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-8">Rename tradeoff</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/evaluation-2">Mechanism decomposition</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/dataset-4">E2-A held-out data</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/experiment-9">Dead ends</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-13">R_COMP FREE</a></li>
      </ul>
    </section>

    <footer>
      <div class="links">
        <a href="https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/paper.pdf">Paper (PDF)</a>
        <a href="https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/report.pdf">Report (PDF)</a>
        <a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3">Code Repository</a>
      </div>
      <div class="citation">@article{anonymous2026consensus,
  title={Pre-Registered Cross-Family Solver Consensus Outperforms LLM Judges on Templated NL-to-FOL Translation with a Supplied Predicate Signature},
  author={Anonymous},
  year={2026}
}</div>
    </footer>

  </main>
</div>

<!-- Lightbox -->
<div class="lightbox" id="lightbox" hidden>
  <button class="lightbox-close" aria-label="Close">&times;</button>
  <img src="figures/fig_dev_auroc_v0.png" alt="">
</div>

<script>
(function(){
  var sections = document.querySelectorAll('section[id]');
  var sideLinks = document.querySelectorAll('nav.side a');
  var mobLinks = document.querySelectorAll('nav.mobile a');

  var observer = new IntersectionObserver(function(entries){
    entries.forEach(function(entry){
      if(entry.isIntersecting){
        var id = entry.target.id;
        sideLinks.forEach(function(a){a.classList.toggle('active', a.getAttribute('href')==='#'+id)});
        mobLinks.forEach(function(a){a.classList.toggle('active', a.getAttribute('href')==='#'+id)});
      }
    });
  }, {rootMargin:'-20% 0px -60% 0px'});

  sections.forEach(function(s){observer.observe(s)});

  // Lightbox
  var lb = document.getElementById('lightbox');
  var lbImg = lb.querySelector('img');
  var lbClose = lb.querySelector('.lightbox-close');
  var prevFocus = null;

  document.querySelectorAll('.fig img').forEach(function(img){
    img.setAttribute('tabindex','0');
    img.addEventListener('click', openLb);
    img.addEventListener('keydown', function(e){if(e.key==='Enter')openLb.call(this,e)});
  });

  function openLb(e){
    prevFocus = document.activeElement;
    lbImg.src = this.src;
    lbImg.alt = this.alt;
    lb.removeAttribute('hidden');
    lbClose.focus();
  }

  function closeLb(){
    lb.setAttribute('hidden','');
    lbImg.removeAttribute('src');
    if(prevFocus) prevFocus.focus();
  }

  lbClose.addEventListener('click', closeLb);
  lb.addEventListener('click', function(e){if(e.target===lb) closeLb()});
  document.addEventListener('keydown', function(e){
    if(e.key==='Escape' && !lb.hasAttribute('hidden')) closeLb();
  });
})();
</script>

</body>
</html>
```

### [67] TOOL RESULT — Write · 2026-09-25 09:40:42 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/index.html", "content": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<title>Pre-Registered Cross-Family Solver Consensus Outperforms LLM Judges on Templated NL-to-FOL Translation</title>\n<style>\n:root {\n  --bg: #faf9f6;\n  --fg: #1a1a1a;\n  --fg2: #444;\n  --fg3: #666;\n  --border: #ddd;\n  --card-bg: #fff;\n  --card-shadow: rgba(0,0,0,.08);\n  --accent: #1a6b4a;\n  --accent-bg: #e8f5ee;\n  --accent2: #c77d1a;\n  --accent2-bg: #fff5e6;\n  --hero-bg: #f0f7f3;\n  --table-stripe: #f7f7f5;\n  --code-bg: #f4f3f0;\n  --nav-bg: rgba(250,249,246,.95);\n  --lightbox-bg: rgba(0,0,0,.85);\n  --tile-bg: #f0f7f3;\n}\n@media(prefers-color-scheme:dark){\n  :root:not([data-theme=\"light\"]){\n    --bg: #181a1b;\n    --fg: #e0ddd8;\n    --fg2: #b0ada6;\n    --fg3: #8a8780;\n    --border: #333;\n    --card-bg: #222;\n    --card-shadow: rgba(0,0,0,.3);\n    --accent: #4cc88a;\n    --accent-bg: #1a2e23;\n    --accent2: #e8a940;\n    --accent2-bg: #2a2010;\n    --hero-bg: #1a2e23;\n    --table-stripe: #1e2021;\n    --code-bg: #1e1e1e;\n    --nav-bg: rgba(24,26,27,.95);\n    --lightbox-bg: rgba(0,0,0,.92);\n    --tile-bg: #1a2e23;\n  }\n}\n:root[data-theme=\"dark\"]{\n  --bg: #181a1b;\n  --fg: #e0ddd8;\n  --fg2: #b0ada6;\n  --fg3: #8a8780;\n  --border: #333;\n  --card-bg: #222;\n  --card-shadow: rgba(0,0,0,.3);\n  --accent: #4cc88a;\n  --accent-bg: #1a2e23;\n  --accent2: #e8a940;\n  --accent2-bg: #2a2010;\n  --hero-bg: #1a2e23;\n  --table-stripe: #1e2021;\n  --code-bg: #1e1e1e;\n  --nav-bg: rgba(24,26,27,.95);\n  --lightbox-bg: rgba(0,0,0,.92);\n  --tile-bg: #1a2e23;\n}\n[hidden]{display:none !important}\n*,*::before,*::after{box-sizing:border-box}\nbody{\n  margin:0; padding:0;\n  font-family:'Iowan Old Style','Palatino Linotype',Palatino,Georgia,serif;\n  background:var(--bg); color:var(--fg);\n  line-height:1.65; font-size:17px;\n}\na{color:var(--accent); text-decoration:none}\na:hover{text-decoration:underline}\nh1,h2,h3{font-weight:600; line-height:1.25; margin:0 0 .5em}\nh1{font-size:1.6em}\nh2{font-size:1.3em; border-bottom:2px solid var(--accent); padding-bottom:.25em; margin-top:2em}\nh3{font-size:1.1em; color:var(--fg2)}\ncode{font-family:'SF Mono',Monaco,'Cascadia Code','Consolas',monospace; font-size:.88em; background:var(--code-bg); padding:1px 5px; border-radius:3px}\n.wrap{max-width:860px; margin:0 auto; padding:0 16px}\n/* --- Hero --- */\n.hero{background:var(--hero-bg); padding:2.5em 0 2em; border-bottom:1px solid var(--border)}\n.hero h1{color:var(--accent); font-size:1.5em; margin-bottom:.3em}\n.hero .author{color:var(--fg3); font-size:.95em; margin-bottom:.8em}\n.hero-links{display:flex; flex-wrap:wrap; gap:.5em}\n.hero-links a{\n  display:inline-flex; align-items:center; gap:.3em;\n  background:var(--accent); color:#fff; padding:.4em 1em;\n  border-radius:5px; font-size:.88em; font-weight:600;\n}\n.hero-links a:hover{opacity:.85; text-decoration:none}\n/* --- Nav --- */\nnav.side{\n  position:sticky; top:1em; float:left; width:170px;\n  margin-left:-190px; font-size:.82em;\n}\nnav.side a{\n  display:block; padding:3px 8px; color:var(--fg3);\n  border-left:2px solid transparent; margin-bottom:2px;\n}\nnav.side a.active{border-left-color:var(--accent); color:var(--accent); font-weight:600}\nnav.side a:hover{color:var(--accent); text-decoration:none}\nnav.mobile{\n  display:none; position:sticky; top:0; z-index:50;\n  background:var(--nav-bg); border-bottom:1px solid var(--border);\n  overflow-x:auto; white-space:nowrap; padding:6px 16px;\n  -webkit-overflow-scrolling:touch;\n}\nnav.mobile a{\n  display:inline-block; padding:4px 10px; font-size:.8em; color:var(--fg3);\n  border-bottom:2px solid transparent;\n}\nnav.mobile a.active{color:var(--accent); border-bottom-color:var(--accent); font-weight:600}\nnav.mobile a:hover{color:var(--accent); text-decoration:none}\n@media(max-width:1100px){\n  nav.side{display:none}\n  nav.mobile{display:block}\n}\n/* --- Main --- */\nmain{margin-left:0; padding:1.5em 0 3em}\n@media(min-width:1101px){\n  main{margin-left:0; position:relative}\n}\n/* --- Cards --- */\n.cards{display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:1em; margin:1em 0}\n.card{\n  background:var(--card-bg); border:1px solid var(--border);\n  border-radius:8px; padding:1em; box-shadow:0 1px 4px var(--card-shadow);\n}\n.card h3{font-size:1em; color:var(--accent); margin-bottom:.4em}\n.card p{font-size:.9em; color:var(--fg2); margin:0}\n/* --- Tables --- */\n.tbl-wrap{overflow-x:auto; margin:1em 0}\ntable{width:100%; border-collapse:collapse; font-size:.88em}\nth{text-align:left; font-weight:600; border-bottom:2px solid var(--border); padding:6px 10px}\ntd{padding:6px 10px; border-bottom:1px solid var(--border)}\ntr:nth-child(even){background:var(--table-stripe)}\n/* --- Tiles --- */\n.tiles{display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:1em; margin:1em 0}\n.tile{\n  background:var(--tile-bg); border-radius:8px; padding:1.2em;\n  text-align:center; border:1px solid var(--border);\n}\n.tile .num{font-size:2em; font-weight:700; color:var(--accent); line-height:1.1}\n.tile .lbl{font-size:.82em; color:var(--fg3); margin-top:.3em}\n/* --- Figures --- */\n.fig{margin:1.5em 0; text-align:center}\n.fig img{\n  max-width:100%; height:auto; border:1px solid var(--border);\n  border-radius:6px; cursor:pointer; transition:box-shadow .2s;\n}\n.fig img:hover{box-shadow:0 2px 12px var(--card-shadow)}\n.fig figcaption{font-size:.82em; color:var(--fg3); margin-top:.5em; max-width:700px; display:inline-block; text-align:left}\n/* --- Lightbox --- */\n.lightbox{\n  position:fixed; inset:0; z-index:1000;\n  background:var(--lightbox-bg);\n  display:flex; align-items:center; justify-content:center;\n  padding:2em;\n}\n.lightbox img{max-width:100%; max-height:90vh; border-radius:6px}\n.lightbox-close{\n  position:absolute; top:12px; right:16px;\n  background:none; border:none; color:#fff; font-size:2em;\n  cursor:pointer; line-height:1;\n}\n/* --- Artifacts --- */\n.artifacts{list-style:none; padding:0; margin:1em 0; columns:2; column-gap:1.5em}\n.artifacts li{break-inside:avoid; margin-bottom:.5em; font-size:.9em}\n.artifacts li::before{content:\"\"; display:inline-block; width:6px; height:6px; background:var(--accent); border-radius:50%; margin-right:6px; vertical-align:middle}\n@media(max-width:600px){.artifacts{columns:1}}\n/* --- Footer --- */\nfooter{border-top:1px solid var(--border); padding:2em 0; margin-top:2em}\nfooter .links{display:flex; flex-wrap:wrap; gap:1em; margin-bottom:1em}\nfooter .links a{font-size:.9em}\n.citation{background:var(--code-bg); padding:1em; border-radius:6px; font-size:.82em; font-family:'SF Mono',Monaco,'Cascadia Code','Consolas',monospace; white-space:pre-wrap; word-break:break-all}\n/* --- Abstract --- */\n.abstract{\n  background:var(--card-bg); border:1px solid var(--border);\n  border-radius:8px; padding:1.2em 1.5em; margin:1em 0;\n  font-size:.95em; color:var(--fg2);\n}\n.abstract strong{color:var(--fg)}\n/* --- Limitations --- */\n.limitations{list-style:decimal; padding-left:1.5em}\n.limitations li{margin-bottom:.6em; font-size:.92em}\n</style>\n</head>\n<body>\n\n<div class=\"hero\">\n  <div class=\"wrap\">\n    <h1>Pre-Registered Cross-Family Solver Consensus Outperforms LLM Judges on Templated NL-to-FOL Translation with a Supplied Predicate Signature</h1>\n    <div class=\"author\">Anonymous</div>\n    <div class=\"hero-links\">\n      <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/paper.pdf\">Paper (PDF)</a>\n      <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/report.pdf\">Report (PDF)</a>\n      <a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3\">Code Repository</a>\n    </div>\n  </div>\n</div>\n\n<nav class=\"mobile\" aria-label=\"Sections\">\n  <a href=\"#abstract\">Abstract</a>\n  <a href=\"#contributions\">Contributions</a>\n  <a href=\"#method\">Method</a>\n  <a href=\"#results-sig\">SIG Results</a>\n  <a href=\"#results-dev\">Dev Results</a>\n  <a href=\"#results-free\">Free OOS</a>\n  <a href=\"#mechanism\">Mechanism</a>\n  <a href=\"#rename\">Rename</a>\n  <a href=\"#confirmation\">Confirmation</a>\n  <a href=\"#limitations\">Limitations</a>\n  <a href=\"#artifacts\">Artifacts</a>\n</nav>\n\n<div class=\"wrap\" style=\"position:relative\">\n  <nav class=\"side\" aria-label=\"Sections\">\n    <a href=\"#abstract\">Abstract</a>\n    <a href=\"#contributions\">Contributions</a>\n    <a href=\"#method\">Method</a>\n    <a href=\"#results-sig\">SIG Results</a>\n    <a href=\"#results-dev\">Dev Results</a>\n    <a href=\"#results-free\">Free OOS</a>\n    <a href=\"#mechanism\">Mechanism</a>\n    <a href=\"#rename\">Rename</a>\n    <a href=\"#confirmation\">Confirmation</a>\n    <a href=\"#limitations\">Limitations</a>\n    <a href=\"#artifacts\">Artifacts</a>\n  </nav>\n\n  <main>\n\n    <section id=\"abstract\">\n      <h2>Abstract</h2>\n      <div class=\"abstract\">\n        Evaluating the faithfulness of NL&#8594;FOL translations is hampered by the expense and unreliability of gold-standard references: roughly <strong>40%</strong> of annotations in standard benchmarks contain errors. We study a gold-free alternative based on <strong>cross-family solver consensus</strong>: collect translations from multiple independent LLM families, check pairwise equivalence with an SMT solver, and score each candidate by the fraction of cross-family peers that disagree with it. In a pre-registered evaluation on <strong>221 templated long-exception sentences</strong> with a supplied predicate signature, consensus achieves a within-template AUROC of <strong>0.954</strong> versus <strong>0.587</strong> for a disguised API judge (&Delta;&nbsp;=&nbsp;+0.367 [+0.328,&nbsp;+0.404]), flat across word-length terciles. Under free vocabulary, consensus still outperforms judges on both development data (&Delta;&nbsp;=&nbsp;+0.099) and untouched out-of-sample sentences (&Delta;&nbsp;=&nbsp;+0.171), but the advantage shrinks by roughly 0.15&nbsp;AUROC and a fundamental <strong>rename tradeoff</strong> emerges: any predicate-name alignment needed to compare independently generated formulas produces a high false-alarm rate on meaning-preserving renames. Confirmation on independent held-out data was budget-stopped and remains incomplete.\n      </div>\n    </section>\n\n    <section id=\"contributions\">\n      <h2>Contributions</h2>\n      <div class=\"cards\">\n        <div class=\"card\">\n          <h3>Pre-Registered SIG Evaluation</h3>\n          <p>Within-template AUROC 0.954 vs 0.587 for a disguised judge (&Delta;&nbsp;=&nbsp;+0.367) on 221 sentences under shared signature, flat across word-length terciles. Zero error endorsement.</p>\n        </div>\n        <div class=\"card\">\n          <h3>Free-Vocabulary Dev Results</h3>\n          <p>Consensus outperforms judges by &Delta;&nbsp;=&nbsp;+0.099 [+0.049,&nbsp;+0.146] on stratified AUROC (n&nbsp;=&nbsp;2,686). Aligner-free c_exact at 0.689 provides 78% of above-chance signal from structural agreement alone.</p>\n        </div>\n        <div class=\"card\">\n          <h3>Untouched Free OOS</h3>\n          <p>R_COMP FREE: &Delta;&nbsp;=&nbsp;+0.171 vs original-view judge under provisional labels. Consensus reaches 94% of frontier judge AUROC. Two-auditor &Delta;&nbsp;=&nbsp;+0.105.</p>\n        </div>\n        <div class=\"card\">\n          <h3>Rename Tradeoff</h3>\n          <p>76.5% false-alarm rate under nonce renames. No alignment variant eliminates this without sacrificing error recall. The name-free variant (c_nf) has zero rename flip but AUROC drops to 0.686.</p>\n        </div>\n      </div>\n    </section>\n\n    <section id=\"method\">\n      <h2>Method</h2>\n      <h3>Consensus Scoring</h3>\n      <p>Given a sentence <em>s</em> and candidate FOL translation <em>c</em>, collect peer translations {<em>p</em><sub>1</sub>,&nbsp;&hellip;,&nbsp;<em>p<sub>k</sub></em>} from <em>k</em> independent LLM families. Score the candidate as:</p>\n      <p style=\"text-align:center; font-size:1.05em\"><code>c_score(c, s) = 1 - (1/k) &sum; 1[equiv(c, p<sub>i</sub>)]</code></p>\n      <p>Under <strong>shared signature</strong> (c_score_sig), all translators use a supplied predicate vocabulary and <code>equiv</code> is a direct Z3 check. Under <strong>free vocabulary</strong> (c_score_align), each translator chooses its own names and <code>equiv</code> requires a predicate-name aligner before Z3.</p>\n\n      <h3>Predicate Alignment (Free Vocabulary)</h3>\n      <p>Independent translators choose different predicate names (e.g. <code>Runs(x)</code> vs <code>IsRunner(x)</code>). The aligner combines three cost components:</p>\n      <ol>\n        <li><strong>Structural cost</strong>: polarity profile, argument-count match, nesting depth</li>\n        <li><strong>Text-anchor cost</strong>: overlap between predicate-name words and source-sentence tokens (Porter stemming, WordNet synonyms)</li>\n        <li><strong>Semantic signature</strong>: truth-value profiles over random finite interpretations</li>\n      </ol>\n      <p>The <em>k</em> cheapest bijections are evaluated; the pair is declared equivalent if any bijection yields a Z3-verified equivalence.</p>\n\n      <h3>Score Variants</h3>\n      <ul>\n        <li><strong>c_exact</strong>: no alignment; exact-match equivalence only. Immune to rename false alarms.</li>\n        <li><strong>c_nf</strong> (name-free): alignment by structural and semantic signatures only, ignoring text anchoring.</li>\n        <li><strong>p_peer_text</strong>: logistic fusion of consensus features with text-side features (bag-of-words coverage, role accounting, Z3 structural match).</li>\n      </ul>\n\n      <h3>Evaluation Framework</h3>\n      <p><strong>Shared-signature labels</strong> (R_COMP): Z3 equivalence to trusted-by-construction references (one weak, one strong reading per template). No human or LLM judgement in the labelling loop.</p>\n      <p><strong>Free-vocabulary labels</strong> (set E): three-person expert panel. R_COMP FREE: provisional search-based classifications (non-confirmatory).</p>\n      <p><strong>Primary metric</strong>: stratified AUROC (items paired only within the same source stratum). Confidence intervals via sentence-cluster percentile bootstrap (B&nbsp;=&nbsp;2,000).</p>\n    </section>\n\n    <section id=\"results-sig\">\n      <h2>Shared-Signature Results (R_COMP-SIG)</h2>\n\n      <div class=\"tiles\">\n        <div class=\"tile\">\n          <div class=\"num\">0.954</div>\n          <div class=\"lbl\">Consensus AUROC<br>(c_score_sig)</div>\n        </div>\n        <div class=\"tile\">\n          <div class=\"num\">0.587</div>\n          <div class=\"lbl\">Judge AUROC<br>(flash-lite, disguised)</div>\n        </div>\n        <div class=\"tile\">\n          <div class=\"num\">+0.367</div>\n          <div class=\"lbl\">&Delta; Consensus &minus; Judge<br>[+0.328, +0.404]</div>\n        </div>\n      </div>\n\n      <p>On 1,904 rows where both scores exist. Population: 429 ERROR / 1,595 CORRECT (21.2% error rate) from 221 sentences, 10 LLM slots across 9 vendor families. Error endorsement is zero (<em>e</em>&nbsp;=&nbsp;0): no error item scores below the decision threshold. Among 429 error items, 75.3% receive the maximum score of 1.0.</p>\n\n      <div class=\"tbl-wrap\">\n        <table>\n          <caption style=\"text-align:left; font-size:.85em; color:var(--fg3); margin-bottom:.5em\">Table 1: Within-template AUROC on R_COMP-SIG (221 sentences, pure Z3 labels)</caption>\n          <thead><tr><th>Metric</th><th><em>n</em></th><th>AUROC [95% CI]</th><th>&Delta; vs disg. judge</th></tr></thead>\n          <tbody>\n            <tr><td>c_score_sig</td><td>1,904</td><td>0.954 [0.939, 0.968]</td><td>+0.367 [+0.328, +0.404]</td></tr>\n            <tr><td>c_score_align</td><td>1,904</td><td>0.954 [0.939, 0.968]</td><td>+0.367 [+0.328, +0.404]</td></tr>\n            <tr><td>judge (flash-lite, disg.)</td><td>1,904</td><td>0.587 [0.551, 0.622]</td><td>&mdash;</td></tr>\n            <tr><td>judge (flash-lite, orig.)</td><td>1,932</td><td>0.673 [0.637, 0.708]</td><td></td></tr>\n            <tr><td>judge (frontier, orig.)</td><td>60</td><td>0.932 [0.782, 1.000]</td><td></td></tr>\n            <tr><td>judge (local, disg.)</td><td>2,024</td><td>0.498 [0.459, 0.534]</td><td></td></tr>\n          </tbody>\n        </table>\n      </div>\n\n      <h3>Flat with Sentence Length</h3>\n      <p>Unlike the free-vocabulary setting, consensus under shared signature is flat across word-length terciles: W1 0.959, W2 0.947, W3 0.953.</p>\n\n      <div class=\"tbl-wrap\">\n        <table>\n          <caption style=\"text-align:left; font-size:.85em; color:var(--fg3); margin-bottom:.5em\">Table 2: R_COMP-SIG AUROC by word-length tercile</caption>\n          <thead><tr><th>Tercile</th><th><em>n</em></th><th>ERR/COR</th><th>c_sig</th><th>judge (disg.)</th><th>&Delta; [CI]</th></tr></thead>\n          <tbody>\n            <tr><td>W1 (shortest)</td><td>503</td><td>125/449</td><td>0.959</td><td>0.578</td><td>+0.382 [+0.278, +0.472]</td></tr>\n            <tr><td>W2</td><td>712</td><td>149/594</td><td>0.947</td><td>0.624</td><td>+0.331 [+0.253, +0.421]</td></tr>\n            <tr><td>W3 (longest)</td><td>689</td><td>155/552</td><td>0.953</td><td>0.567</td><td>+0.388 [+0.301, +0.471]</td></tr>\n          </tbody>\n        </table>\n      </div>\n\n      <figure class=\"fig\" id=\"fig-sig-tercile\">\n        <img src=\"figures/fig_sig_tercile_v0.png\" alt=\"R_COMP-SIG AUROC by word-length tercile\" loading=\"lazy\" width=\"800\" height=\"500\">\n        <figcaption>Figure 1: Within-template AUROC on R_COMP-SIG by word-length tercile. Consensus (blue) is flat (0.947&ndash;0.959); the disguised judge (orange) hovers near chance (0.567&ndash;0.624).</figcaption>\n      </figure>\n\n      <p><strong>Frontier judge comparison</strong>: On a 60-row subsample, consensus achieves 0.956 [0.889, 1.000] vs 0.932 [0.855, 0.990] for the frontier judge (Gemini 3.1 Pro).</p>\n\n      <p><strong>Scope</strong>: R_COMP-SIG uses templated sentences with a supplied predicate vocabulary. The shared signature eliminates the alignment problem entirely. These results do not extend to free-vocabulary settings.</p>\n    </section>\n\n    <section id=\"results-dev\">\n      <h2>Free-Vocabulary Development Results (Set E)</h2>\n\n      <figure class=\"fig\" id=\"fig-dev-auroc\">\n        <img src=\"figures/fig_dev_auroc_v0.png\" alt=\"Stratified AUROC on development set E\" loading=\"lazy\" width=\"800\" height=\"500\">\n        <figcaption>Figure 2: Stratified AUROC on the free-vocabulary development dataset. Consensus-based metrics (blue) outperform API judges (orange) and other baselines (gray). Error bars: 95% sentence-cluster bootstrap CIs.</figcaption>\n      </figure>\n\n      <div class=\"tbl-wrap\">\n        <table>\n          <caption style=\"text-align:left; font-size:.85em; color:var(--fg3); margin-bottom:.5em\">Table 3: Stratified AUROC on development set E (R_AB, n = 2,686)</caption>\n          <thead><tr><th>Metric</th><th>Strat AUROC [95% CI]</th><th>$/item</th></tr></thead>\n          <tbody>\n            <tr><td>c_score_align</td><td>0.741 [0.705, 0.775]</td><td>9.1e-5</td></tr>\n            <tr><td>p_peer_text (fused)</td><td>0.753 [0.720, 0.784]</td><td>9.1e-5</td></tr>\n            <tr><td>c_exact (no alignment)</td><td>0.689 [0.652, 0.726]</td><td>&mdash;</td></tr>\n            <tr><td>c_nf (name-free)</td><td>0.686 [0.647, 0.720]</td><td>&mdash;</td></tr>\n            <tr style=\"border-top:2px solid var(--border)\"><td>flash-lite judge (disg.)</td><td>0.642 [0.607, 0.676]</td><td>5.1e-5</td></tr>\n            <tr><td>flash-lite judge (orig.)</td><td>0.623 [0.593, 0.651]</td><td>5.1e-5</td></tr>\n            <tr><td>nano judge (disg.)</td><td>0.644 [0.609, 0.680]</td><td>2.0e-5</td></tr>\n            <tr><td>local judge Qwen-8B (disg.)</td><td>0.674 [0.646, 0.703]</td><td>&mdash;</td></tr>\n            <tr style=\"border-top:2px solid var(--border)\"><td>round-trip NLI (min)</td><td>0.606 [0.569, 0.645]</td><td>2.8e-5</td></tr>\n            <tr><td>self-consistency (5-sample)</td><td>0.598 [0.559, 0.637]</td><td>6.7e-5</td></tr>\n            <tr style=\"border-top:2px solid var(--border)\"><td>28-feature stack</td><td>0.735 [0.699, 0.766]</td><td>&mdash;</td></tr>\n            <tr><td>28-feature stack + c_score_align</td><td>0.774 [0.743, 0.802]</td><td>&mdash;</td></tr>\n          </tbody>\n        </table>\n      </div>\n\n      <p>The drop from 0.952 (shared signature, full 2,024-row pool) to 0.801 (free vocabulary on the same R_COMP sentences) reflects the cost of predicate-name alignment. Aligner-free c_exact at 0.689 provides 78% of the above-chance signal from structural agreement alone; the aligner adds the remaining 22%.</p>\n      <p>Adding c_score_align to the 28-feature baseline stack increases stratified AUROC by +0.039 [+0.021,&nbsp;+0.057]; permutation null test <em>p</em><sub>95</sub>&nbsp;=&nbsp;0.009.</p>\n      <p><strong>Frontier judge comparison</strong>: c_score_align achieves 95.7% of the frontier judge's AUROC (ratio 0.957 [0.887, 1.034]) on a 284-row subsample.</p>\n      <p><strong>System-level ranking</strong>: Kendall &tau;<sub>b</sub>&nbsp;=&nbsp;0.692 [+0.513,&nbsp;+0.795] between system mean score and error rate across 13 configurations.</p>\n    </section>\n\n    <section id=\"results-free\">\n      <h2>Free-Vocabulary Out-of-Sample (R_COMP FREE)</h2>\n\n      <p>The same 221 R_COMP sentences translated under free vocabulary. Confirmatory labelling required a gloss gate that failed twice (balanced accuracy 0.776 and 0.561, below the 0.90 threshold), producing zero confirmed CORRECT rows. Results use provisional non-confirmatory labels.</p>\n\n      <div class=\"tbl-wrap\">\n        <table>\n          <caption style=\"text-align:left; font-size:.85em; color:var(--fg3); margin-bottom:.5em\">Table 4: R_COMP FREE provisional AUROCs (within-template, untouched rows)</caption>\n          <thead><tr><th>View</th><th><em>n</em> (ERR/MAPPED)</th><th>c_align</th><th>judge</th></tr></thead>\n          <tbody>\n            <tr><td>Disguised</td><td>1,706 (602/1,104)</td><td>0.801 [0.770, 0.834]</td><td>0.584 [0.550, 0.618]</td></tr>\n            <tr><td>Original</td><td>1,709 (605/1,104)</td><td>0.804 [0.774, 0.836]</td><td>0.633 [0.601, 0.666]</td></tr>\n          </tbody>\n        </table>\n      </div>\n\n      <p>Disguised-judge &Delta;&nbsp;=&nbsp;+0.217 [+0.175, +0.260]. Original-view &Delta;&nbsp;=&nbsp;+0.171 [+0.135, +0.206]. On a 146-row two-auditor subset: &Delta;&nbsp;=&nbsp;+0.105 [+0.011, +0.215]. On a 150-row frontier-judge subsample: consensus reaches 0.94 of the frontier judge's AUROC.</p>\n    </section>\n\n    <section id=\"mechanism\">\n      <h2>Mechanism</h2>\n\n      <p>The consensus signal decomposes into <strong>endorsement</strong> <em>e</em> (fraction of ERROR items endorsed by peers, i.e. false negatives) and <strong>divergence</strong> <em>d</em> (fraction of CORRECT items that diverge from peers, i.e. false positives). AUROC at a binary threshold equals 1&nbsp;&minus;&nbsp;(<em>e</em>&nbsp;+&nbsp;<em>d</em>)/2.</p>\n\n      <p><strong>Shared vocabulary</strong>: <em>e</em>&nbsp;=&nbsp;0.0, <em>d</em>&nbsp;=&nbsp;0.260. Zero error endorsement; 26% false-alarm rate from valid alternative formalizations. Flat across sentence lengths.</p>\n\n      <p><strong>Free vocabulary</strong>: Net degradation &Delta;(<em>e</em>&nbsp;+&nbsp;<em>d</em>)&nbsp;=&nbsp;+0.356 [+0.198,&nbsp;+0.493] from short to long sentences, driven almost entirely by divergence (&Delta;<em>d</em>&nbsp;=&nbsp;+0.608, &Delta;<em>e</em>&nbsp;=&nbsp;&minus;0.252). As formulas grow longer, the predicate-name aligner increasingly makes mistakes.</p>\n\n      <figure class=\"fig\" id=\"fig-complexity\">\n        <img src=\"figures/fig_complexity_v0.png\" alt=\"Endorsement and divergence by sentence-length tercile\" loading=\"lazy\" width=\"800\" height=\"500\">\n        <figcaption>Figure 3: Decomposition of free-vocabulary consensus error rates by sentence-length tercile. Endorsement <em>e</em> decreases with length, but divergence <em>d</em> increases sharply, producing net degradation of +0.356. Under shared signature, this degradation is absent.</figcaption>\n      </figure>\n\n      <h3>Family Sufficiency</h3>\n      <p>Three peer families suffice for 97% of full-pool AUROC (<em>k</em><sub>95</sub>&nbsp;=&nbsp;3), but the long-sentence tercile requires <em>k</em><sub>95</sub>&nbsp;=&nbsp;5.</p>\n\n      <div class=\"tbl-wrap\">\n        <table>\n          <caption style=\"text-align:left; font-size:.85em; color:var(--fg3); margin-bottom:.5em\">Table 5: Free-vocabulary AUROC by number of peer families</caption>\n          <thead><tr><th><em>k</em></th><th>AUROC (overall)</th><th>AUROC (long, T3)</th></tr></thead>\n          <tbody>\n            <tr><td>1</td><td>0.685</td><td>0.581</td></tr>\n            <tr><td>3</td><td>0.757</td><td>0.651</td></tr>\n            <tr><td>5</td><td>0.776</td><td>0.698</td></tr>\n            <tr><td>7</td><td>0.784</td><td>0.726</td></tr>\n          </tbody>\n        </table>\n      </div>\n\n      <figure class=\"fig\" id=\"fig-k-curve\">\n        <img src=\"figures/fig_k_curve_v0.png\" alt=\"AUROC vs number of peer families\" loading=\"lazy\" width=\"800\" height=\"500\">\n        <figcaption>Figure 4: Stratified AUROC as a function of peer families <em>k</em>. Three families capture 97% of the full-pool signal, but long sentences require five families to reach 95%.</figcaption>\n      </figure>\n    </section>\n\n    <section id=\"rename\">\n      <h2>The Rename Tradeoff</h2>\n\n      <p>The predicate aligner that enables free-vocabulary comparison introduces a fundamental false-alarm vulnerability. When correct formulas are copied with meaning-preserving renames, the consensus score should not change. In practice:</p>\n\n      <div class=\"tbl-wrap\">\n        <table>\n          <caption style=\"text-align:left; font-size:.85em; color:var(--fg3); margin-bottom:.5em\">Table 6: False-alarm rates on meaning-preserving renames of CORRECT candidates</caption>\n          <thead><tr><th>Metric</th><th>NONCE FA</th><th>NONCE flip</th><th>SYN FA</th><th>SYN flip</th></tr></thead>\n          <tbody>\n            <tr><td>c_align</td><td>0.765</td><td>0.605</td><td>0.565</td><td>0.313</td></tr>\n            <tr><td>c_nf (name-free)</td><td>0.132</td><td>0.000</td><td>0.201</td><td>0.000</td></tr>\n            <tr><td>p_peer_text</td><td>1.000</td><td>0.821</td><td>0.216</td><td>0.080</td></tr>\n            <tr><td>judge (disg.)</td><td>0.229</td><td>0.134</td><td>0.085</td><td>0.058</td></tr>\n          </tbody>\n        </table>\n      </div>\n\n      <p>The name-free variant c_nf eliminates rename sensitivity (flip&nbsp;=&nbsp;0) but at the cost of within-base AUROC 0.499 (chance level) and lower overall discrimination (0.686 vs 0.741). This tradeoff explains the gap between shared-signature and free-vocabulary performance.</p>\n\n      <h3>Per-Type Sensitivity</h3>\n      <p>On the PERTURB suite (4,234 typed mutants + 868 controls), consensus recall at the primary threshold is flat across error operators: NEG 0.761, SWAP 0.758, DROP 0.721, ADD 0.763, MEANING_RENAME 0.762. Error typing under free vocabulary achieves only 0.123 [0.081, 0.169] accuracy, below both the judge (0.326) and peer-medoid baseline (0.328).</p>\n    </section>\n\n    <section id=\"confirmation\">\n      <h2>Confirmation Status</h2>\n      <p>Independent confirmation on held-out data remains incomplete. A fresh dataset (E2-A, 550 new sentences) was constructed but the budget was exhausted before enough items could be labelled.</p>\n      <ul>\n        <li><strong>DT stratum</strong> (short, ProverQA): consensus AUROC 0.916, tying Qwen-8B judge (&Delta;&nbsp;=&nbsp;+0.003 [&minus;0.042, +0.052]).</li>\n        <li><strong>L25 stratum</strong>: c_score_align falls to 0.443 on only 42 items (35 ERROR / 7 CORRECT), below chance, but extreme variance with only 7 CORRECT items from 3 sentences.</li>\n      </ul>\n      <p>Every pre-registered criterion on the target strata returned NOT_TESTABLE or unfavourable.</p>\n\n      <h3>Dead Ends</h3>\n      <p>Investigated and abandoned: fused structural-feature filter (false-alarm gate failure); name-free consensus c_nf (rename-invariant but blind to meaning-rename errors); decomposed solver-based semantic reader (balanced accuracy 0.476); LLM adjudication of disputed items (balanced accuracy 0.662); candidate-signature consensus (error endorsement rose to 0.459 because peers reproduced the candidate's errors).</p>\n    </section>\n\n    <section id=\"limitations\">\n      <h2>Limitations</h2>\n      <ol class=\"limitations\">\n        <li><strong>Shared-signature scope.</strong> The 0.954 AUROC uses templated sentences with a supplied predicate vocabulary. The templates and supplied signature limit scope to controlled evaluation settings.</li>\n        <li><strong>Development data overlap.</strong> R_COMP-SIG later served as development data for aligner tuning. Pre-registration ensures the SIG result is uncontaminated, but the dev-set numbers from E are not independent.</li>\n        <li><strong>Rename vulnerability.</strong> Under free vocabulary, a 76.5% false-alarm rate on nonce renames means the metric systematically penalises non-standard predicate names, even if semantically correct.</li>\n        <li><strong>Length degradation (free vocabulary).</strong> Net degradation +0.356 from short to long sentences, driven by correct-translation divergence. Weakest on the longest, most complex sentences.</li>\n        <li><strong>Provisional labels.</strong> R_COMP FREE uses non-confirmatory labels; the two-auditor subset &Delta;&nbsp;=&nbsp;+0.105 has a CI that barely excludes zero.</li>\n        <li><strong>Label dependence.</strong> Development results on E depend on a three-person panel whose agreement is imperfect. The metric's advantage could partly reflect panel biases.</li>\n        <li><strong>Cost.</strong> Consensus requires <em>k</em> peer translations per sentence. In this experiment (k&nbsp;=&nbsp;9), amortised cost is about 19&times; a single cheap judge call.</li>\n        <li><strong>Domain.</strong> All results are English&#8594;FOL from MALLS, ProverQA, and R_COMP. Generalisation to other formalisms, languages, or distributions is untested.</li>\n      </ol>\n    </section>\n\n    <section id=\"artifacts\">\n      <h2>Code Artifacts</h2>\n      <ul class=\"artifacts\">\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-1\">Consensus scoring</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-3\">Development set E</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-4\">Baselines</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-2/experiment-5\">p_peer_text (fused)</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-6\">Dev results evaluation</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-7\">R_COMP dataset</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-8\">Rename tradeoff</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/evaluation-2\">Mechanism decomposition</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/dataset-4\">E2-A held-out data</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/experiment-9\">Dead ends</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-13\">R_COMP FREE</a></li>\n      </ul>\n    </section>\n\n    <footer>\n      <div class=\"links\">\n        <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/paper.pdf\">Paper (PDF)</a>\n        <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/report.pdf\">Report (PDF)</a>\n        <a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3\">Code Repository</a>\n      </div>\n      <div class=\"citation\">@article{anonymous2026consensus,\n  title={Pre-Registered Cross-Family Solver Consensus Outperforms LLM Judges on Templated NL-to-FOL Translation with a Supplied Predicate Signature},\n  author={Anonymous},\n  year={2026}\n}</div>\n    </footer>\n\n  </main>\n</div>\n\n<!-- Lightbox -->\n<div class=\"lightbox\" id=\"lightbox\" hidden>\n  <button class=\"lightbox-close\" aria-label=\"Close\">&times;</button>\n  <img src=\"figures/fig_dev_auroc_v0.png\" alt=\"\">\n</div>\n\n<script>\n(function(){\n  var sections = document.querySelectorAll('section[id]');\n  var sideLinks = document.querySelectorAll('nav.side a');\n  var mobLinks = document.querySelectorAll('nav.mobile a');\n\n  var observer = new IntersectionObserver(function(entries){\n    entries.forEach(function(entry){\n      if(entry.isIntersecting){\n        var id = entry.target.id;\n        sideLinks.forEach(function(a){a.classList.toggle('active', a.getAttribute('href')==='#'+id)});\n        mobLinks.forEach(function(a){a.classList.toggle('active', a.getAttribute('href')==='#'+id)});\n      }\n    });\n  }, {rootMargin:'-20% 0px -60% 0px'});\n\n  sections.forEach(function(s){observer.observe(s)});\n\n  // Lightbox\n  var lb = document.getElementById('lightbox');\n  var lbImg = lb.querySelector('img');\n  var lbClose = lb.querySelector('.lightbox-close');\n  var prevFocus = null;\n\n  document.querySelectorAll('.fig img').forEach(function(img){\n    img.setAttribute('tabindex','0');\n    img.addEventListener('click', openLb);\n    img.addEventListener('keydown', function(e){if(e.key==='Enter')openLb.call(this,e)});\n  });\n\n  function openLb(e){\n    prevFocus = document.activeElement;\n    lbImg.src = this.src;\n    lbImg.alt = this.alt;\n    lb.removeAttribute('hidden');\n    lbClose.focus();\n  }\n\n  function closeLb(){\n    lb.setAttribute('hidden','');\n    lbImg.removeAttribute('src');\n    if(prevFocus) prevFocus.focus();\n  }\n\n  lbClose.addEventListener('click', closeLb);\n  lb.addEventListener('click', function(e){if(e.target===lb) closeLb()});\n  document.addEventListener('keydown', function(e){\n    if(e.key==='Escape' && !lb.hasAttribute('hidden')) closeLb();\n  });\n})();\n</script>\n\n</body>\n</html>\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [68] ASSISTANT · 2026-09-25 09:40:54 UTC

```
Now let me create the supporting files and test with Playwright.
```

### [69] TOOL CALL — Write · 2026-09-25 09:40:54 UTC

```
File: /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/.aii/manifest.yaml

entries: []
```

### [70] TOOL RESULT — Write · 2026-09-25 09:40:54 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/.aii/manifest.yaml", "content": "entries: []\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [71] TOOL CALL — Write · 2026-09-25 09:40:54 UTC

```
File: /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/README.md

# Gold-Free Faithfulness Metrics for NL-to-FOL Translation

Public project page for the paper *Pre-Registered Cross-Family Solver Consensus
Outperforms LLM Judges on Templated NL-to-FOL Translation with a Supplied
Predicate Signature*.

## What this is

A single self-contained HTML page that presents the paper's contributions,
method, results, and figures faster than reading the PDF. Designed to be
served directly from GitHub Pages with no build step.

## Repository layout

| Path | Description |
|------|-------------|
| `index.html` | Self-contained project page (inline CSS/JS, no external deps) |
| `paper.tex` | LaTeX source of the paper |
| `paper.pdf` | Compiled PDF |
| `references.bib` | BibTeX bibliography |
| `references.json` | Structured bibliography in JSON |
| `figures/*.png` | Rendered figures used by the project page |
| `figures/*.pdf` | Vector figure originals |
| `figures/*_spec.json` | Figure generation specifications |

## Viewing the page

Open `index.html` in any modern browser, or visit the GitHub Pages deployment.
No build step, server, or external resources are required.

## License

See the paper for terms.

## Restoring removed files

Nothing in this folder is marked for deletion in `.aii/manifest.yaml`, so there is nothing to restore.
```

### [72] TOOL RESULT — Write · 2026-09-25 09:40:54 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/README.md", "content": "# Gold-Free Faithfulness Metrics for NL-to-FOL Translation\n\nPublic project page for the paper *Pre-Registered Cross-Family Solver Consensus\nOutperforms LLM Judges on Templated NL-to-FOL Translation with a Supplied\nPredicate Signature*.\n\n## What this is\n\nA single self-contained HTML page that presents the paper's contributions,\nmethod, results, and figures faster than reading the PDF. Designed to be\nserved directly from GitHub Pages with no build step.\n\n## Repository layout\n\n| Path | Description |\n|------|-------------|\n| `index.html` | Self-contained project page (inline CSS/JS, no external deps) |\n| `paper.tex` | LaTeX source of the paper |\n| `paper.pdf` | Compiled PDF |\n| `references.bib` | BibTeX bibliography |\n| `references.json` | Structured bibliography in JSON |\n| `figures/*.png` | Rendered figures used by the project page |\n| `figures/*.pdf` | Vector figure originals |\n| `figures/*_spec.json` | Figure generation specifications |\n\n## Viewing the page\n\nOpen `index.html` in any modern browser, or visit the GitHub Pages deployment.\nNo build step, server, or external resources are required.\n\n## License\n\nSee the paper for terms.\n\n## Restoring removed files\n\nNothing in this folder is marked for deletion in `.aii/manifest.yaml`, so there is nothing to restore.\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [73] ASSISTANT · 2026-09-25 09:40:58 UTC

```
Now let me install Playwright and test the page.
```

### [74] TOOL CALL — Bash · 2026-09-25 09:40:58 UTC

```
Install Playwright and Chromium for headless testing:
pip install playwright 2>&1 | tail -3 && python3 -m playwright install chromium 2>&1 | tail -5
```

### [75] TOOL RESULT — Bash · 2026-09-25 09:41:16 UTC

```
{"stdout": "[notice] A new release of pip is available: 25.0.1 -> 26.2.1\n[notice] To update, run: pip install --upgrade pip\n|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                        |  70% of 114.3 MiB\n|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■                |  80% of 114.3 MiB\n|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■        |  90% of 114.3 MiB\n|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■| 100% of 114.3 MiB\nChrome Headless Shell 153.0.8010.12 (playwright chromium-headless-shell v1243) downloaded to /root/.cache/ms-playwright/chromium_headless_shell-1243", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [76] TOOL CALL — Bash · 2026-09-25 09:41:32 UTC

```
Test index.html with Playwright at 390px and 1440px:
python3 << 'PYEOF'
import asyncio
from playwright.async_api import async_playwright
import os

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        errors = []

        for width in [390, 1440]:
            page = await browser.new_page(viewport={"width": width, "height": 900})
            page.on("console", lambda msg: errors.append(f"[{width}px] console.{msg.type}: {msg.text}") if msg.type == "error" else None)
            page.on("pageerror", lambda err: errors.append(f"[{width}px] pageerror: {err}"))

            url = "file://" + os.path.abspath("index.html")
            await page.goto(url, wait_until="networkidle")

            # Check no horizontal scroll
            scroll_w = await page.evaluate("document.documentElement.scrollWidth")
            client_w = await page.evaluate("document.documentElement.clientWidth")
            if scroll_w > client_w + 2:
                errors.append(f"[{width}px] horizontal scroll: scrollWidth={scroll_w} > clientWidth={client_w}")

            # Check all images load
            imgs = await page.query_selector_all(".fig img")
            for img in imgs:
                src = await img.get_attribute("src")
                nat_w = await img.evaluate("el => el.naturalWidth")
                if nat_w == 0:
                    errors.append(f"[{width}px] image not loaded: {src}")
                else:
                    print(f"[{width}px] OK: {src} ({nat_w}px wide)")

            # Click first figure to open lightbox
            first_img = await page.query_selector(".fig img")
            if first_img:
                await first_img.click()
                lb = await page.query_selector("#lightbox")
                hidden = await lb.get_attribute("hidden")
                if hidden is not None:
                    errors.append(f"[{width}px] lightbox did not open")
                else:
                    print(f"[{width}px] lightbox opened OK")
                    # Close with Escape
                    await page.keyboard.press("Escape")
                    hidden = await lb.get_attribute("hidden")
                    if hidden is None:
                        errors.append(f"[{width}px] lightbox did not close on Escape")
                    else:
                        print(f"[{width}px] lightbox closed on Escape OK")

            # Check lightbox img src after close
            lb_img = await page.query_selector("#lightbox img")
            lb_src = await lb_img.get_attribute("src")
            if lb_src and lb_src != "":
                errors.append(f"[{width}px] lightbox img src not cleared: {lb_src}")

            # Check nav links
            nav_links = await page.query_selector_all("nav a")
            print(f"[{width}px] nav links: {len(nav_links)}")

            # Check all sections exist
            sections = await page.query_selector_all("section[id]")
            for s in sections:
                sid = await s.get_attribute("id")
                print(f"[{width}px] section: {sid}")

            # Check all external links
            links = await page.query_selector_all("a[href^='https://']")
            hrefs = set()
            for link in links:
                href = await link.get_attribute("href")
                hrefs.add(href)
            print(f"[{width}px] external links: {len(hrefs)}")
            for h in sorted(hrefs):
                print(f"  {h}")

            await page.close()

        await browser.close()

        if errors:
            print("\n=== ERRORS ===")
            for e in errors:
                print(e)
        else:
            print("\n=== ALL TESTS PASSED ===")

asyncio.run(test())
PYEOF
```

### [77] TOOL RESULT — Bash [ERROR] · 2026-09-25 09:41:34 UTC

```
Error: Exit code 1
Traceback (most recent call last):
  File "<stdin>", line 89, in <module>
  File "/usr/local/lib/python3.12/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/asyncio/base_events.py", line 691, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "<stdin>", line 7, in test
  File "/usr/local/lib/python3.12/site-packages/playwright/async_api/_generated.py", line 16851, in launch
    await self._impl_obj.launch(
  File "/usr/local/lib/python3.12/site-packages/playwright/_impl/_browser_type.py", line 101, in launch
    await self._channel.send(
  File "/usr/local/lib/python3.12/site-packages/playwright/_impl/_connection.py", line 76, in send
    return await self._connection.wrap_api_call(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/site-packages/playwright/_impl/_connection.py", line 632, in wrap_api_call
    raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
playwright._impl._errors.TargetClosedError: BrowserType.launch: Target page, context or browser has been closed
Browser logs:

<launching> /root/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell --disable-field-trial-config --disable-background-networking --disable-background-timer-throttling --disable-backgrounding-occluded-windows --disable-back-forward-cache --disable-breakpad --disable-client-side-phishing-detection --disable-component-extensions-with-background-pages --disable-component-update --no-default-browser-check --disable-default-apps --disable-dev-shm-usage --disable-edgeupdater --disable-extensions --disable-features=AvoidUnnecessaryBeforeUnloadCheckSync,DestroyProfileOnBrowserClose,DialMediaRouteProvider,GlobalMediaControls,HttpsUpgrades,LensOverlay,MediaRouter,PaintHolding,ThirdPartyStoragePartitioning,BlockOriginHeaderModificationOnRedirect,Translate,AutoDeElevate,OptimizationHints,msForceBrowserSignIn,msEdgeUpdateLaunchServicesPreferredVersion --enable-features=CDPScreenshotNewSurface --allow-pre-commit-input --disable-hang-monitor --disable-ipc-flooding-protection --disable-popup-blocking --disable-prompt-on-repost --disable-renderer-backgrounding --disable-updater-scheduler --force-color-profile=srgb --metrics-recording-only --no-first-run --password-store=basic --use-mock-keychain --no-service-autorun --export-tagged-pdf --disable-search-engine-choice-screen --unsafely-disable-devtools-self-xss-warnings --edge-skip-compat-layer-relaunch --disable-infobars --disable-search-engine-choice-screen --disable-sync --enable-unsafe-swiftshader --headless --hide-scrollbars --mute-audio --blink-settings=primaryHoverType=2,availableHoverTypes=2,primaryPointerType=4,availablePointerTypes=4 --no-sandbox --user-data-dir=/tmp/playwright_chromiumdev_profile-3LJomU --remote-debugging-pipe --no-startup-window
<launched> pid=1816
[pid=1816][err] /root/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell: error while loading shared libraries: libatk-bridge-2.0.so.0: cannot open shared object file: No such file or directory
Call log:
  - <launching> /root/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell --disable-field-trial-config --disable-background-networking --disable-background-timer-throttling --disable-backgrounding-occluded-windows --disable-back-forward-cache --disable-breakpad --disable-client-side-phishing-detection --disable-component-extensions-with-background-pages --disable-component-update --no-default-browser-check --disable-default-apps --disable-dev-shm-usage --disable-edgeupdater --disable-extensions --disable-features=AvoidUnnecessaryBeforeUnloadCheckSync,DestroyProfileOnBrowserClose,DialMediaRouteProvider,GlobalMediaControls,HttpsUpgrades,LensOverlay,MediaRouter,PaintHolding,ThirdPartyStoragePartitioning,BlockOriginHeaderModificationOnRedirect,Translate,AutoDeElevate,OptimizationHints,msForceBrowserSignIn,msEdgeUpdateLaunchServicesPreferredVersion --enable-features=CDPScreenshotNewSurface --allow-pre-commit-input --disable-hang-monitor --disable-ipc-flooding-protection --disable-popup-blocking --disable-prompt-on-repost --disable-renderer-backgrounding --disable-updater-scheduler --force-color-profile=srgb --metrics-recording-only --no-first-run --password-store=basic --use-mock-keychain --no-service-autorun --export-tagged-pdf --disable-search-engine-choice-screen --unsafely-disable-devtools-self-xss-warnings --edge-skip-compat-layer-relaunch --disable-infobars --disable-search-engine-choice-screen --disable-sync --enable-unsafe-swiftshader --headless --hide-scrollbars --mute-audio --blink-settings=primaryHoverType=2,availableHoverTypes=2,primaryPointerType=4,availablePointerTypes=4 --no-sandbox --user-data-dir=/tmp/playwright_chromiumdev_profile-3LJomU --remote-debugging-pipe --no-startup-window
  - <launched> pid=1816
  - [pid=1816][err] /root/.cache/ms-playwright/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell: error while loading shared libraries: libatk-bridge-2.0.so.0: cannot open shared object file: No such file or directory
  - [pid=1816] <gracefully close start>
  - [pid=1816] <kill>
  - [pid=1816] <will force kill>
  - [pid=1816] exception while trying to kill process: Error: kill ESRCH
  - [pid=1816] <process did exit: exitCode=127, signal=null>
  - [pid=1816] starting temporary directories cleanup
  - [pid=1816] finished temporary directories cleanup
  - [pid=1816] <gracefully close end>
```

### [78] TOOL CALL — Bash · 2026-09-25 09:41:40 UTC

```
Install Playwright system dependencies for Chromium:
python3 -m playwright install-deps chromium 2>&1 | tail -10
```

### [79] TOOL RESULT — Bash · 2026-09-25 09:41:52 UTC

```
{"stdout": "Setting up libxmu6:amd64 (2:1.1.3-3) ...\r\nSetting up libglx-mesa0:amd64 (22.3.6-1+deb12u2) ...\r\nSetting up libglx0:amd64 (1.6.0-1) ...\r\nSetting up libxaw7:amd64 (2:1.0.14-1) ...\r\nSetting up libgl1:amd64 (1.6.0-1) ...\r\nSetting up x11-xkb-utils (7.7+7) ...\r\nSetting up xserver-common (2:21.1.7-3+deb12u13) ...\r\nSetting up xvfb (2:21.1.7-3+deb12u13) ...\r\nProcessing triggers for man-db (2.11.2-2) ...\r\nProcessing triggers for libc-bin (2.36-9+deb12u14) ...", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [80] TOOL CALL — Bash · 2026-09-25 09:42:08 UTC

```
Test index.html with Playwright:
python3 << 'PYEOF'
import asyncio
from playwright.async_api import async_playwright
import os

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        errors = []

        for width in [390, 1440]:
            page = await browser.new_page(viewport={"width": width, "height": 900})
            page.on("console", lambda msg: errors.append(f"[{width}px] console.{msg.type}: {msg.text}") if msg.type == "error" else None)
            page.on("pageerror", lambda err: errors.append(f"[{width}px] pageerror: {err}"))

            url = "file://" + os.path.abspath("index.html")
            await page.goto(url, wait_until="networkidle")

            # Check no horizontal scroll
            scroll_w = await page.evaluate("document.documentElement.scrollWidth")
            client_w = await page.evaluate("document.documentElement.clientWidth")
            if scroll_w > client_w + 2:
                errors.append(f"[{width}px] horizontal scroll: scrollWidth={scroll_w} > clientWidth={client_w}")

            # Check all images load
            imgs = await page.query_selector_all(".fig img")
            for img in imgs:
                src = await img.get_attribute("src")
                nat_w = await img.evaluate("el => el.naturalWidth")
                if nat_w == 0:
                    errors.append(f"[{width}px] image not loaded: {src}")
                else:
                    print(f"[{width}px] OK: {src} ({nat_w}px wide)")

            # Click first figure to open lightbox
            first_img = await page.query_selector(".fig img")
            if first_img:
                await first_img.click()
                lb = await page.query_selector("#lightbox")
                hidden = await lb.get_attribute("hidden")
                if hidden is not None:
                    errors.append(f"[{width}px] lightbox did not open")
                else:
                    print(f"[{width}px] lightbox opened OK")
                    await page.keyboard.press("Escape")
                    hidden = await lb.get_attribute("hidden")
                    if hidden is None:
                        errors.append(f"[{width}px] lightbox did not close on Escape")
                    else:
                        print(f"[{width}px] lightbox closed on Escape OK")

            # Check all sections
            sections = await page.query_selector_all("section[id]")
            for s in sections:
                sid = await s.get_attribute("id")
                print(f"[{width}px] section: {sid}")

            # Count external links
            links = await page.query_selector_all("a[href^='https://']")
            hrefs = set()
            for link in links:
                href = await link.get_attribute("href")
                hrefs.add(href)
            print(f"[{width}px] external links: {len(hrefs)}")

            await page.close()

        await browser.close()

        if errors:
            print("\n=== ERRORS ===")
            for e in errors:
                print(e)
        else:
            print("\n=== ALL TESTS PASSED ===")

asyncio.run(test())
PYEOF
```

### [81] TOOL RESULT — Bash · 2026-09-25 09:42:10 UTC

```
{"stdout": "[390px] OK: figures/fig_dev_auroc_v0.png (1260px wide)\n[390px] lightbox opened OK\n[390px] lightbox closed on Escape OK\n[390px] section: abstract\n[390px] section: contributions\n[390px] section: method\n[390px] section: results-sig\n[390px] section: results-dev\n[390px] section: results-free\n[390px] section: mechanism\n[390px] section: rename\n[390px] section: confirmation\n[390px] section: limitations\n[390px] section: artifacts\n[390px] external links: 14\n[1440px] OK: figures/fig_sig_tercile_v0.png (1260px wide)\n[1440px] OK: figures/fig_dev_auroc_v0.png (1260px wide)\n[1440px] lightbox opened OK\n[1440px] lightbox closed on Escape OK\n[1440px] section: abstract\n[1440px] section: contributions\n[1440px] section: method\n[1440px] section: results-sig\n[1440px] section: results-dev\n[1440px] section: results-free\n[1440px] section: mechanism\n[1440px] section: rename\n[1440px] section: confirmation\n[1440px] section: limitations\n[1440px] section: artifacts\n[1440px] external links: 14\n\n=== ERRORS ===\n[390px] image not loaded: figures/fig_sig_tercile_v0.png\n[390px] image not loaded: figures/fig_complexity_v0.png\n[390px] image not loaded: figures/fig_k_curve_v0.png\n[1440px] image not loaded: figures/fig_complexity_v0.png\n[1440px] image not loaded: figures/fig_k_curve_v0.png", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [82] ASSISTANT · 2026-09-25 09:42:20 UTC

```
Images with `loading="lazy"` don't load until scrolled into view. Let me remove lazy loading since it's a small page.
```

### [83] TOOL CALL — Edit · 2026-09-25 09:42:20 UTC

```
File: /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/index.html
OLD:  loading="lazy"
NEW: 
```

### [84] TOOL RESULT — Edit · 2026-09-25 09:42:20 UTC

```
{"filePath": "/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/index.html", "oldString": " loading=\"lazy\"", "newString": "", "originalFile": null, "structuredPatch": [{"oldStart": 342, "oldLines": 7, "newStart": 342, "newLines": 7, "lines": ["       </div>", " ", "       <figure class=\"fig\" id=\"fig-sig-tercile\">", "-        <img src=\"figures/fig_sig_tercile_v0.png\" alt=\"R_COMP-SIG AUROC by word-length tercile\" loading=\"lazy\" width=\"800\" height=\"500\">", "+        <img src=\"figures/fig_sig_tercile_v0.png\" alt=\"R_COMP-SIG AUROC by word-length tercile\" width=\"800\" height=\"500\">", "         <figcaption>Figure 1: Within-template AUROC on R_COMP-SIG by word-length tercile. Consensus (blue) is flat (0.947&ndash;0.959); the disguised judge (orange) hovers near chance (0.567&ndash;0.624).</figcaption>", "       </figure>", " "]}, {"oldStart": 355, "oldLines": 7, "newStart": 355, "newLines": 7, "lines": ["       <h2>Free-Vocabulary Development Results (Set E)</h2>", " ", "       <figure class=\"fig\" id=\"fig-dev-auroc\">", "-        <img src=\"figures/fig_dev_auroc_v0.png\" alt=\"Stratified AUROC on development set E\" loading=\"lazy\" width=\"800\" height=\"500\">", "+        <img src=\"figures/fig_dev_auroc_v0.png\" alt=\"Stratified AUROC on development set E\" width=\"800\" height=\"500\">", "         <figcaption>Figure 2: Stratified AUROC on the free-vocabulary development dataset. Consensus-based metrics (blue) outperform API judges (orange) and other baselines (gray). Error bars: 95% sentence-cluster bootstrap CIs.</figcaption>", "       </figure>", " "]}, {"oldStart": 415, "oldLines": 7, "newStart": 415, "newLines": 7, "lines": ["       <p><strong>Free vocabulary</strong>: Net degradation &Delta;(<em>e</em>&nbsp;+&nbsp;<em>d</em>)&nbsp;=&nbsp;+0.356 [+0.198,&nbsp;+0.493] from short to long sentences, driven almost entirely by divergence (&Delta;<em>d</em>&nbsp;=&nbsp;+0.608, &Delta;<em>e</em>&nbsp;=&nbsp;&minus;0.252). As formulas grow longer, the predicate-name aligner increasingly makes mistakes.</p>", " ", "       <figure class=\"fig\" id=\"fig-complexity\">", "-        <img src=\"figures/fig_complexity_v0.png\" alt=\"Endorsement and divergence by sentence-length tercile\" loading=\"lazy\" width=\"800\" height=\"500\">", "+        <img src=\"figures/fig_complexity_v0.png\" alt=\"Endorsement and divergence by sentence-length tercile\" width=\"800\" height=\"500\">", "         <figcaption>Figure 3: Decomposition of free-vocabulary consensus error rates by sentence-length tercile. Endorsement <em>e</em> decreases with length, but divergence <em>d</em> increases sharply, producing net degradation of +0.356. Under shared signature, this degradation is absent.</figcaption>", "       </figure>", " "]}, {"oldStart": 436, "oldLines": 7, "newStart": 436, "newLines": 7, "lines": ["       </div>", " ", "       <figure class=\"fig\" id=\"fig-k-curve\">", "-        <img src=\"figures/fig_k_curve_v0.png\" alt=\"AUROC vs number of peer families\" loading=\"lazy\" width=\"800\" height=\"500\">", "+        <img src=\"figures/fig_k_curve_v0.png\" alt=\"AUROC vs number of peer families\" width=\"800\" height=\"500\">", "         <figcaption>Figure 4: Stratified AUROC as a function of peer families <em>k</em>. Three families capture 97% of the full-pool signal, but long sentences require five families to reach 95%.</figcaption>", "       </figure>", "     </section>"]}], "userModified": false, "replaceAll": true}
```

### [85] TOOL CALL — Bash · 2026-09-25 09:42:34 UTC

```
Retest with lazy loading removed:
python3 << 'PYEOF'
import asyncio
from playwright.async_api import async_playwright
import os

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        errors = []

        for width in [390, 1440]:
            page = await browser.new_page(viewport={"width": width, "height": 900})
            page.on("console", lambda msg: errors.append(f"[{width}px] console.{msg.type}: {msg.text}") if msg.type == "error" else None)
            page.on("pageerror", lambda err: errors.append(f"[{width}px] pageerror: {err}"))

            url = "file://" + os.path.abspath("index.html")
            await page.goto(url, wait_until="networkidle")

            sw = await page.evaluate("document.documentElement.scrollWidth")
            cw = await page.evaluate("document.documentElement.clientWidth")
            if sw > cw + 2:
                errors.append(f"[{width}px] horizontal scroll: {sw} > {cw}")

            imgs = await page.query_selector_all(".fig img")
            for img in imgs:
                src = await img.get_attribute("src")
                nw = await img.evaluate("el => el.naturalWidth")
                if nw == 0:
                    errors.append(f"[{width}px] img not loaded: {src}")
                else:
                    print(f"[{width}px] OK: {src}")

            # Lightbox test
            first_img = await page.query_selector(".fig img")
            if first_img:
                await first_img.click()
                lb = await page.query_selector("#lightbox")
                h = await lb.get_attribute("hidden")
                if h is not None:
                    errors.append(f"[{width}px] lightbox did not open")
                else:
                    await page.keyboard.press("Escape")
                    h2 = await lb.get_attribute("hidden")
                    if h2 is None:
                        errors.append(f"[{width}px] lightbox did not close")

            await page.close()

        await browser.close()
        if errors:
            print("\n=== ERRORS ===")
            for e in errors:
                print(e)
        else:
            print("\n=== ALL TESTS PASSED ===")

asyncio.run(test())
PYEOF
```

### [86] TOOL RESULT — Bash · 2026-09-25 09:42:34 UTC

```
{"stdout": "[390px] OK: figures/fig_sig_tercile_v0.png\n[390px] OK: figures/fig_dev_auroc_v0.png\n[390px] OK: figures/fig_complexity_v0.png\n[390px] OK: figures/fig_k_curve_v0.png\n[1440px] OK: figures/fig_sig_tercile_v0.png\n[1440px] OK: figures/fig_dev_auroc_v0.png\n[1440px] OK: figures/fig_complexity_v0.png\n[1440px] OK: figures/fig_k_curve_v0.png\n\n=== ALL TESTS PASSED ===", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [87] ASSISTANT · 2026-09-25 09:43:04 UTC

```
All tests pass. Now let me create the struct out JSON.
```

### [88] TOOL CALL — Write · 2026-09-25 09:43:04 UTC

```
File: /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/.terminal_claude_agent_struct_out.json

{
  "summary": "Single self-contained index.html project page (inline CSS/JS, system serif font, no external resources fetched at load time). Presents the paper 'Pre-Registered Cross-Family Solver Consensus Outperforms LLM Judges on Templated NL-to-FOL Translation with a Supplied Predicate Signature' with these sections: Abstract (40% benchmark error rate, gold-free consensus alternative), Contributions (4 cards: pre-registered SIG evaluation, free-vocabulary dev results, untouched free OOS, rename tradeoff), Method (consensus scoring formula c_score = 1 - (1/k) sum equiv(c,p_i), predicate alignment with structural/text-anchor/semantic signature costs, score variants c_exact/c_nf/p_peer_text, evaluation framework with stratified AUROC), Shared-Signature Results (3 big-number tiles: 0.954 consensus vs 0.587 judge, Delta +0.367 from Table 1; Table 2 word-length terciles W1 0.959 W2 0.947 W3 0.953; Figure 1 fig_sig_tercile_v0.png; frontier judge 0.956 vs 0.932 on 60-row subsample), Free-Vocabulary Dev Results (Figure 2 fig_dev_auroc_v0.png; Table 3 with all 12 metrics from paper Table 3: c_score_align 0.741, p_peer_text 0.753, c_exact 0.689, flash-lite disg 0.642, nano 0.644, Qwen-8B 0.674, round-trip 0.606, self-consistency 0.598, 28-feature stack 0.735, stack+c_align 0.774; Delta +0.099; permutation p95=0.009), Free-Vocabulary OOS (Table 4 R_COMP FREE provisional: disguised c_align 0.801 vs judge 0.584, original 0.804 vs 0.633; Delta +0.171; two-auditor Delta +0.105), Mechanism (e/d decomposition: SIG e=0 d=0.260; free vocab Delta(e+d)=+0.356; Figure 3 fig_complexity_v0.png; Table 5 k-families: k=3 gives 97% AUROC; Figure 4 fig_k_curve_v0.png), Rename Tradeoff (Table 6: c_align NONCE FA 0.765, c_nf flip=0.000, p_peer_text NONCE FA 1.000; per-type recall NEG 0.761 SWAP 0.758 DROP 0.721 ADD 0.763; error typing accuracy 0.123), Confirmation Status (E2-A budget-stopped; DT AUROC 0.916; L25 AUROC 0.443 on 42 items; dead ends listed), Limitations (8 items from paper Section 7.7). Four PNG figures rendered from paper PDFs at 2.5x. Lightbox with keyboard accessibility. Dark mode via CSS custom properties. Sticky side nav (desktop) / horizontal scroll nav (mobile). Hero with CDN paper/report and GitHub repo links. Footer with citation and links. 11 code artifact links from paper footnotes. All numbers verified against paper.tex.",
  "out_expected_files": {
    "site_html_path": "index.html"
  }
}
```

### [89] TOOL RESULT — Write · 2026-09-25 09:43:04 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/.terminal_claude_agent_struct_out.json", "content": "{\n  \"summary\": \"Single self-contained index.html project page (inline CSS/JS, system serif font, no external resources fetched at load time). Presents the paper 'Pre-Registered Cross-Family Solver Consensus Outperforms LLM Judges on Templated NL-to-FOL Translation with a Supplied Predicate Signature' with these sections: Abstract (40% benchmark error rate, gold-free consensus alternative), Contributions (4 cards: pre-registered SIG evaluation, free-vocabulary dev results, untouched free OOS, rename tradeoff), Method (consensus scoring formula c_score = 1 - (1/k) sum equiv(c,p_i), predicate alignment with structural/text-anchor/semantic signature costs, score variants c_exact/c_nf/p_peer_text, evaluation framework with stratified AUROC), Shared-Signature Results (3 big-number tiles: 0.954 consensus vs 0.587 judge, Delta +0.367 from Table 1; Table 2 word-length terciles W1 0.959 W2 0.947 W3 0.953; Figure 1 fig_sig_tercile_v0.png; frontier judge 0.956 vs 0.932 on 60-row subsample), Free-Vocabulary Dev Results (Figure 2 fig_dev_auroc_v0.png; Table 3 with all 12 metrics from paper Table 3: c_score_align 0.741, p_peer_text 0.753, c_exact 0.689, flash-lite disg 0.642, nano 0.644, Qwen-8B 0.674, round-trip 0.606, self-consistency 0.598, 28-feature stack 0.735, stack+c_align 0.774; Delta +0.099; permutation p95=0.009), Free-Vocabulary OOS (Table 4 R_COMP FREE provisional: disguised c_align 0.801 vs judge 0.584, original 0.804 vs 0.633; Delta +0.171; two-auditor Delta +0.105), Mechanism (e/d decomposition: SIG e=0 d=0.260; free vocab Delta(e+d)=+0.356; Figure 3 fig_complexity_v0.png; Table 5 k-families: k=3 gives 97% AUROC; Figure 4 fig_k_curve_v0.png), Rename Tradeoff (Table 6: c_align NONCE FA 0.765, c_nf flip=0.000, p_peer_text NONCE FA 1.000; per-type recall NEG 0.761 SWAP 0.758 DROP 0.721 ADD 0.763; error typing accuracy 0.123), Confirmation Status (E2-A budget-stopped; DT AUROC 0.916; L25 AUROC 0.443 on 42 items; dead ends listed), Limitations (8 items from paper Section 7.7). Four PNG figures rendered from paper PDFs at 2.5x. Lightbox with keyboard accessibility. Dark mode via CSS custom properties. Sticky side nav (desktop) / horizontal scroll nav (mobile). Hero with CDN paper/report and GitHub repo links. Footer with citation and links. 11 code artifact links from paper footnotes. All numbers verified against paper.tex.\",\n  \"out_expected_files\": {\n    \"site_html_path\": \"index.html\"\n  }\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [90] ASSISTANT · 2026-09-25 09:43:14 UTC

```
Let me validate the JSON and check all files.
```

### [91] TOOL CALL — Bash · 2026-09-25 09:43:14 UTC

```
Validate all deliverables:
python3 -c "
import json, os

# Validate struct out JSON
with open('.terminal_claude_agent_struct_out.json') as f:
    data = json.load(f)
assert 'summary' in data, 'missing summary'
assert len(data['summary']) >= 300, f'summary too short: {len(data[\"summary\"])}'
assert len(data['summary']) <= 5000, f'summary too long: {len(data[\"summary\"])}'
assert data['out_expected_files']['site_html_path'] == 'index.html', 'wrong site_html_path'
print(f'JSON valid. Summary length: {len(data[\"summary\"])} chars')

# Check all expected files
files = {
    'index.html': True,
    '.terminal_claude_agent_struct_out.json': True,
    '.aii/manifest.yaml': True,
    'README.md': True,
    'figures/fig_dev_auroc_v0.png': True,
    'figures/fig_sig_tercile_v0.png': True,
    'figures/fig_complexity_v0.png': True,
    'figures/fig_k_curve_v0.png': True,
}

for f, required in files.items():
    exists = os.path.exists(f)
    size = os.path.getsize(f) if exists else 0
    status = 'OK' if exists else 'MISSING'
    print(f'{status}: {f} ({size:,} bytes)')
    if required and not exists:
        raise RuntimeError(f'Required file missing: {f}')

# Check manifest
with open('.aii/manifest.yaml') as f:
    content = f.read().strip()
assert content == 'entries: []', f'unexpected manifest: {content}'
print('Manifest: OK')
print('All files validated.')
"
```

### [92] TOOL RESULT — Bash · 2026-09-25 09:43:14 UTC

```
{"stdout": "JSON valid. Summary length: 2344 chars\nOK: index.html (35,018 bytes)\nOK: .terminal_claude_agent_struct_out.json (2,430 bytes)\nOK: .aii/manifest.yaml (12 bytes)\nOK: README.md (1,281 bytes)\nOK: figures/fig_dev_auroc_v0.png (78,933 bytes)\nOK: figures/fig_sig_tercile_v0.png (54,343 bytes)\nOK: figures/fig_complexity_v0.png (58,891 bytes)\nOK: figures/fig_k_curve_v0.png (70,485 bytes)\nManifest: OK\nAll files validated.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [93] ASSISTANT · 2026-09-25 09:43:22 UTC

```
All deliverables are complete and validated:

- **index.html** (35KB): Self-contained project page with all CSS/JS inline, system serif font, no external resources. 4 figures, 6 tables, 3 big-number tiles, 11 code artifact links, lightbox with keyboard accessibility, dark mode, responsive layout with sticky nav.
- **.terminal_claude_agent_struct_out.json**: Valid JSON with `site_html_path: "index.html"` and 2,344-char summary.
- **.aii/manifest.yaml**: `entries: []`
- **README.md**: Repository description with layout table.
- **figures/**: 4 PNGs rendered from paper PDFs at 2.5x resolution.

Playwright tests pass at both 390px and 1440px: all images load, lightbox opens/closes, no console errors, no horizontal scroll.
```

### [94] SYSTEM-USER prompt · 2026-09-25 09:43:24 UTC

```
SITE VERIFICATION FAILED: 17 problem(s) in index.html.

- the page does not link to https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/dataset-1 - add the link, labelled 'Code: Held-out logic translation test set, panel-checked', using that URL exactly as given
- the page does not link to https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-2/dataset-3 - add the link, labelled 'Code: Long logic sentences and FOL error suite', using that URL exactly as given
- the page does not link to https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-2/evaluation-1 - add the link, labelled 'Code: Re-checking earlier logic-metric results across label sets', using that URL exactly as given
- the page does not link to https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/research-1 - add the link, labelled 'Code: What is new about peer agreement for logic', using that URL exactly as given
- the page does not link to https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/experiment-10 - add the link, labelled 'Code: Do symbol hints help model agreement checks?', using that URL exactly as given
- the page does not link to https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/dataset-5 - add the link, labelled 'Code: Name-free labels for free-vocabulary logic translations', using that URL exactly as given
- the page does not link to https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/evaluation-3 - add the link, labelled 'Code: Can shared vocabulary fix consensus blind spots?', using that URL exactly as given
- the page does not link to https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-11 - add the link, labelled 'Code: Consensus vs LLM judges on fresh logic data', using that URL exactly as given
- the page does not link to https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-12 - add the link, labelled 'Code: Second fresh sample of long logic sentences', using that URL exactly as given
- the page does not link to https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-14 - add the link, labelled 'Code: Screening fixes for model-agreement false alarms', using that URL exactly as given
- the page does not link to https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/evaluation-4 - add the link, labelled 'Code: Corrected record: every paper number checked', using that URL exactly as given
- the page does not link to https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/exec_summary.pdf - add the link, labelled 'Read the executive summary', using that URL exactly as given
- the page does not link to https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/round-1/report.pdf - add the link, labelled 'Round 1', using that URL exactly as given
- the page does not link to https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/round-2/report.pdf - add the link, labelled 'Round 2', using that URL exactly as given
- the page does not link to https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/round-3/report.pdf - add the link, labelled 'Round 3', using that URL exactly as given
- the page does not link to https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/round-4/report.pdf - add the link, labelled 'Round 4', using that URL exactly as given
- the page does not link to https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/round-5/report.pdf - add the link, labelled 'Round 5', using that URL exactly as given

You MUST:
1. Fix every problem listed above in index.html.
2. Keep the page ONE self-contained file — all CSS and JavaScript inline, no external scripts, stylesheets or web fonts, nothing fetched at load time.
3. Point every image at figures/<filename>, where <filename> is a browser-renderable image that really exists in your figures/ folder. A vector PDF figure needs a PNG rendered beside it first; reference the PNG.
4. Re-open the page and confirm it still renders before finishing.
```

### [95] ASSISTANT · 2026-09-25 09:43:30 UTC

```
Adding the 17 missing links: 11 additional code artifacts, 1 executive summary, and 5 round reports.
```

### [96] TOOL CALL — Read · 2026-09-25 09:43:30 UTC

```
/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/index.html
```

### [97] TOOL RESULT — Read · 2026-09-25 09:43:30 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/index.html", "content": "      <p><strong>Free-vocabulary labels</strong> (set E): three-person expert panel. R_COMP FREE: provisional search-based classifications (non-confirmatory).</p>\n      <p><strong>Primary metric</strong>: stratified AUROC (items paired only within the same source stratum). Confidence intervals via sentence-cluster percentile bootstrap (B&nbsp;=&nbsp;2,000).</p>\n    </section>\n\n    <section id=\"results-sig\">\n      <h2>Shared-Signature Results (R_COMP-SIG)</h2>\n\n      <div class=\"tiles\">\n        <div class=\"tile\">\n          <div class=\"num\">0.954</div>\n          <div class=\"lbl\">Consensus AUROC<br>(c_score_sig)</div>\n        </div>\n        <div class=\"tile\">\n          <div class=\"num\">0.587</div>\n          <div class=\"lbl\">Judge AUROC<br>(flash-lite, disguised)</div>\n        </div>\n        <div class=\"tile\">\n          <div class=\"num\">+0.367</div>\n          <div class=\"lbl\">&Delta; Consensus &minus; Judge<br>[+0.328, +0.404]</div>\n        </div>\n      </div>\n\n      <p>On 1,904 rows where both scores exist. Population: 429 ERROR / 1,595 CORRECT (21.2% error rate) from 221 sentences, 10 LLM slots across 9 vendor families. Error endorsement is zero (<em>e</em>&nbsp;=&nbsp;0): no error item scores below the decision threshold. Among 429 error items, 75.3% receive the maximum score of 1.0.</p>\n\n      <div class=\"tbl-wrap\">\n        <table>\n          <caption style=\"text-align:left; font-size:.85em; color:var(--fg3); margin-bottom:.5em\">Table 1: Within-template AUROC on R_COMP-SIG (221 sentences, pure Z3 labels)</caption>\n          <thead><tr><th>Metric</th><th><em>n</em></th><th>AUROC [95% CI]</th><th>&Delta; vs disg. judge</th></tr></thead>\n          <tbody>\n            <tr><td>c_score_sig</td><td>1,904</td><td>0.954 [0.939, 0.968]</td><td>+0.367 [+0.328, +0.404]</td></tr>\n            <tr><td>c_score_align</td><td>1,904</td><td>0.954 [0.939, 0.968]</td><td>+0.367 [+0.328, +0.404]</td></tr>\n            <tr><td>judge (flash-lite, disg.)</td><td>1,904</td><td>0.587 [0.551, 0.622]</td><td>&mdash;</td></tr>\n            <tr><td>judge (flash-lite, orig.)</td><td>1,932</td><td>0.673 [0.637, 0.708]</td><td></td></tr>\n            <tr><td>judge (frontier, orig.)</td><td>60</td><td>0.932 [0.782, 1.000]</td><td></td></tr>\n            <tr><td>judge (local, disg.)</td><td>2,024</td><td>0.498 [0.459, 0.534]</td><td></td></tr>\n          </tbody>\n        </table>\n      </div>\n\n      <h3>Flat with Sentence Length</h3>\n      <p>Unlike the free-vocabulary setting, consensus under shared signature is flat across word-length terciles: W1 0.959, W2 0.947, W3 0.953.</p>\n\n      <div class=\"tbl-wrap\">\n        <table>\n          <caption style=\"text-align:left; font-size:.85em; color:var(--fg3); margin-bottom:.5em\">Table 2: R_COMP-SIG AUROC by word-length tercile</caption>\n          <thead><tr><th>Tercile</th><th><em>n</em></th><th>ERR/COR</th><th>c_sig</th><th>judge (disg.)</th><th>&Delta; [CI]</th></tr></thead>\n          <tbody>\n            <tr><td>W1 (shortest)</td><td>503</td><td>125/449</td><td>0.959</td><td>0.578</td><td>+0.382 [+0.278, +0.472]</td></tr>\n            <tr><td>W2</td><td>712</td><td>149/594</td><td>0.947</td><td>0.624</td><td>+0.331 [+0.253, +0.421]</td></tr>\n            <tr><td>W3 (longest)</td><td>689</td><td>155/552</td><td>0.953</td><td>0.567</td><td>+0.388 [+0.301, +0.471]</td></tr>\n          </tbody>\n        </table>\n      </div>\n\n      <figure class=\"fig\" id=\"fig-sig-tercile\">\n        <img src=\"figures/fig_sig_tercile_v0.png\" alt=\"R_COMP-SIG AUROC by word-length tercile\" width=\"800\" height=\"500\">\n        <figcaption>Figure 1: Within-template AUROC on R_COMP-SIG by word-length tercile. Consensus (blue) is flat (0.947&ndash;0.959); the disguised judge (orange) hovers near chance (0.567&ndash;0.624).</figcaption>\n      </figure>\n\n      <p><strong>Frontier judge comparison</strong>: On a 60-row subsample, consensus achieves 0.956 [0.889, 1.000] vs 0.932 [0.855, 0.990] for the frontier judge (Gemini 3.1 Pro).</p>\n\n      <p><strong>Scope</strong>: R_COMP-SIG uses templated sentences with a supplied predicate vocabulary. The shared signature eliminates the alignment problem entirely. These results do not extend to free-vocabulary settings.</p>\n    </section>\n\n    <section id=\"results-dev\">\n      <h2>Free-Vocabulary Development Results (Set E)</h2>\n\n      <figure class=\"fig\" id=\"fig-dev-auroc\">\n        <img src=\"figures/fig_dev_auroc_v0.png\" alt=\"Stratified AUROC on development set E\" width=\"800\" height=\"500\">\n        <figcaption>Figure 2: Stratified AUROC on the free-vocabulary development dataset. Consensus-based metrics (blue) outperform API judges (orange) and other baselines (gray). Error bars: 95% sentence-cluster bootstrap CIs.</figcaption>\n      </figure>\n\n      <div class=\"tbl-wrap\">\n        <table>\n          <caption style=\"text-align:left; font-size:.85em; color:var(--fg3); margin-bottom:.5em\">Table 3: Stratified AUROC on development set E (R_AB, n = 2,686)</caption>\n          <thead><tr><th>Metric</th><th>Strat AUROC [95% CI]</th><th>$/item</th></tr></thead>\n          <tbody>\n            <tr><td>c_score_align</td><td>0.741 [0.705, 0.775]</td><td>9.1e-5</td></tr>\n            <tr><td>p_peer_text (fused)</td><td>0.753 [0.720, 0.784]</td><td>9.1e-5</td></tr>\n            <tr><td>c_exact (no alignment)</td><td>0.689 [0.652, 0.726]</td><td>&mdash;</td></tr>", "numLines": 80, "startLine": 290, "totalLines": 588}}
```

### [98] TOOL CALL — Read · 2026-09-25 09:43:34 UTC

```
/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/index.html
```

### [99] TOOL RESULT — Read · 2026-09-25 09:43:34 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/index.html", "content": "      </figure>\n\n      <h3>Family Sufficiency</h3>\n      <p>Three peer families suffice for 97% of full-pool AUROC (<em>k</em><sub>95</sub>&nbsp;=&nbsp;3), but the long-sentence tercile requires <em>k</em><sub>95</sub>&nbsp;=&nbsp;5.</p>\n\n      <div class=\"tbl-wrap\">\n        <table>\n          <caption style=\"text-align:left; font-size:.85em; color:var(--fg3); margin-bottom:.5em\">Table 5: Free-vocabulary AUROC by number of peer families</caption>\n          <thead><tr><th><em>k</em></th><th>AUROC (overall)</th><th>AUROC (long, T3)</th></tr></thead>\n          <tbody>\n            <tr><td>1</td><td>0.685</td><td>0.581</td></tr>\n            <tr><td>3</td><td>0.757</td><td>0.651</td></tr>\n            <tr><td>5</td><td>0.776</td><td>0.698</td></tr>\n            <tr><td>7</td><td>0.784</td><td>0.726</td></tr>\n          </tbody>\n        </table>\n      </div>\n\n      <figure class=\"fig\" id=\"fig-k-curve\">\n        <img src=\"figures/fig_k_curve_v0.png\" alt=\"AUROC vs number of peer families\" width=\"800\" height=\"500\">\n        <figcaption>Figure 4: Stratified AUROC as a function of peer families <em>k</em>. Three families capture 97% of the full-pool signal, but long sentences require five families to reach 95%.</figcaption>\n      </figure>\n    </section>\n\n    <section id=\"rename\">\n      <h2>The Rename Tradeoff</h2>\n\n      <p>The predicate aligner that enables free-vocabulary comparison introduces a fundamental false-alarm vulnerability. When correct formulas are copied with meaning-preserving renames, the consensus score should not change. In practice:</p>\n\n      <div class=\"tbl-wrap\">\n        <table>\n          <caption style=\"text-align:left; font-size:.85em; color:var(--fg3); margin-bottom:.5em\">Table 6: False-alarm rates on meaning-preserving renames of CORRECT candidates</caption>\n          <thead><tr><th>Metric</th><th>NONCE FA</th><th>NONCE flip</th><th>SYN FA</th><th>SYN flip</th></tr></thead>\n          <tbody>\n            <tr><td>c_align</td><td>0.765</td><td>0.605</td><td>0.565</td><td>0.313</td></tr>\n            <tr><td>c_nf (name-free)</td><td>0.132</td><td>0.000</td><td>0.201</td><td>0.000</td></tr>\n            <tr><td>p_peer_text</td><td>1.000</td><td>0.821</td><td>0.216</td><td>0.080</td></tr>\n            <tr><td>judge (disg.)</td><td>0.229</td><td>0.134</td><td>0.085</td><td>0.058</td></tr>\n          </tbody>\n        </table>\n      </div>\n\n      <p>The name-free variant c_nf eliminates rename sensitivity (flip&nbsp;=&nbsp;0) but at the cost of within-base AUROC 0.499 (chance level) and lower overall discrimination (0.686 vs 0.741). This tradeoff explains the gap between shared-signature and free-vocabulary performance.</p>\n\n      <h3>Per-Type Sensitivity</h3>\n      <p>On the PERTURB suite (4,234 typed mutants + 868 controls), consensus recall at the primary threshold is flat across error operators: NEG 0.761, SWAP 0.758, DROP 0.721, ADD 0.763, MEANING_RENAME 0.762. Error typing under free vocabulary achieves only 0.123 [0.081, 0.169] accuracy, below both the judge (0.326) and peer-medoid baseline (0.328).</p>\n    </section>\n\n    <section id=\"confirmation\">\n      <h2>Confirmation Status</h2>\n      <p>Independent confirmation on held-out data remains incomplete. A fresh dataset (E2-A, 550 new sentences) was constructed but the budget was exhausted before enough items could be labelled.</p>\n      <ul>\n        <li><strong>DT stratum</strong> (short, ProverQA): consensus AUROC 0.916, tying Qwen-8B judge (&Delta;&nbsp;=&nbsp;+0.003 [&minus;0.042, +0.052]).</li>\n        <li><strong>L25 stratum</strong>: c_score_align falls to 0.443 on only 42 items (35 ERROR / 7 CORRECT), below chance, but extreme variance with only 7 CORRECT items from 3 sentences.</li>\n      </ul>\n      <p>Every pre-registered criterion on the target strata returned NOT_TESTABLE or unfavourable.</p>\n\n      <h3>Dead Ends</h3>\n      <p>Investigated and abandoned: fused structural-feature filter (false-alarm gate failure); name-free consensus c_nf (rename-invariant but blind to meaning-rename errors); decomposed solver-based semantic reader (balanced accuracy 0.476); LLM adjudication of disputed items (balanced accuracy 0.662); candidate-signature consensus (error endorsement rose to 0.459 because peers reproduced the candidate's errors).</p>\n    </section>\n\n    <section id=\"limitations\">\n      <h2>Limitations</h2>\n      <ol class=\"limitations\">\n        <li><strong>Shared-signature scope.</strong> The 0.954 AUROC uses templated sentences with a supplied predicate vocabulary. The templates and supplied signature limit scope to controlled evaluation settings.</li>\n        <li><strong>Development data overlap.</strong> R_COMP-SIG later served as development data for aligner tuning. Pre-registration ensures the SIG result is uncontaminated, but the dev-set numbers from E are not independent.</li>\n        <li><strong>Rename vulnerability.</strong> Under free vocabulary, a 76.5% false-alarm rate on nonce renames means the metric systematically penalises non-standard predicate names, even if semantically correct.</li>\n        <li><strong>Length degradation (free vocabulary).</strong> Net degradation +0.356 from short to long sentences, driven by correct-translation divergence. Weakest on the longest, most complex sentences.</li>\n        <li><strong>Provisional labels.</strong> R_COMP FREE uses non-confirmatory labels; the two-auditor subset &Delta;&nbsp;=&nbsp;+0.105 has a CI that barely excludes zero.</li>\n        <li><strong>Label dependence.</strong> Development results on E depend on a three-person panel whose agreement is imperfect. The metric's advantage could partly reflect panel biases.</li>\n        <li><strong>Cost.</strong> Consensus requires <em>k</em> peer translations per sentence. In this experiment (k&nbsp;=&nbsp;9), amortised cost is about 19&times; a single cheap judge call.</li>\n        <li><strong>Domain.</strong> All results are English&#8594;FOL from MALLS, ProverQA, and R_COMP. Generalisation to other formalisms, languages, or distributions is untested.</li>\n      </ol>\n    </section>\n\n    <section id=\"artifacts\">\n      <h2>Code Artifacts</h2>\n      <ul class=\"artifacts\">\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-1\">Consensus scoring</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-3\">Development set E</a></li>", "numLines": 80, "startLine": 420, "totalLines": 588}}
```

### [100] TOOL CALL — Read · 2026-09-25 09:43:40 UTC

```
/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/index.html
```

### [101] TOOL RESULT — Read · 2026-09-25 09:43:40 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/index.html", "content": "    <section id=\"artifacts\">\n      <h2>Code Artifacts</h2>\n      <ul class=\"artifacts\">\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-1\">Consensus scoring</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-3\">Development set E</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-4\">Baselines</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-2/experiment-5\">p_peer_text (fused)</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-6\">Dev results evaluation</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-7\">R_COMP dataset</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-8\">Rename tradeoff</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/evaluation-2\">Mechanism decomposition</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/dataset-4\">E2-A held-out data</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/experiment-9\">Dead ends</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-13\">R_COMP FREE</a></li>\n      </ul>\n    </section>\n\n    <footer>\n      <div class=\"links\">\n        <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/paper.pdf\">Paper (PDF)</a>\n        <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/report.pdf\">Report (PDF)</a>\n        <a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3\">Code Repository</a>\n      </div>\n      <div class=\"citation\">@article{anonymous2026consensus,\n  title={Pre-Registered Cross-Family Solver Consensus Outperforms LLM Judges on Templated NL-to-FOL Translation with a Supplied Predicate Signature},\n  author={Anonymous},\n  year={2026}\n}</div>\n    </footer>\n\n  </main>\n</div>\n\n<!-- Lightbox -->\n<div class=\"lightbox\" id=\"lightbox\" hidden>\n  <button class=\"lightbox-close\" aria-label=\"Close\">&times;</button>\n  <img src=\"figures/fig_dev_auroc_v0.png\" alt=\"\">\n</div>\n\n<script>\n(function(){\n  var sections = document.querySelectorAll('section[id]');\n  var sideLinks = document.querySelectorAll('nav.side a');\n  var mobLinks = document.querySelectorAll('nav.mobile a');\n\n  var observer = new IntersectionObserver(function(entries){\n    entries.forEach(function(entry){\n      if(entry.isIntersecting){\n        var id = entry.target.id;\n        sideLinks.forEach(function(a){a.classList.toggle('active', a.getAttribute('href')==='#'+id)});\n        mobLinks.forEach(function(a){a.classList.toggle('active', a.getAttribute('href')==='#'+id)});\n      }\n    });\n  }, {rootMargin:'-20% 0px -60% 0px'});\n\n  sections.forEach(function(s){observer.observe(s)});\n\n  // Lightbox\n  var lb = document.getElementById('lightbox');\n  var lbImg = lb.querySelector('img');", "numLines": 60, "startLine": 495, "totalLines": 588}}
```

### [102] ASSISTANT · 2026-09-25 09:44:10 UTC

```
Now I'll add the 11 missing code artifact links and replace the footer to include the executive summary and round report links.
```

### [103] TOOL CALL — Edit · 2026-09-25 09:44:10 UTC

```
File: /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/index.html
OLD:       <ul class="artifacts">
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-1">Consensus scoring</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-3">Development set E</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-4">Baselines</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-2/experiment-5">p_peer_text (fused)</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-6">Dev results evaluation</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-7">R_COMP dataset</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-8">Rename tradeoff</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/evaluation-2">Mechanism decomposition</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/dataset-4">E2-A held-out data</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/experiment-9">Dead ends</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-13">R_COMP FREE</a></li>
      </ul>
NEW:       <ul class="artifacts">
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-1">Consensus scoring</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-3">Development set E</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-4">Baselines</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/dataset-1">Code: Held-out logic translation test set, panel-checked</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-2/experiment-5">p_peer_text (fused)</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-2/dataset-3">Code: Long logic sentences and FOL error suite</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-2/evaluation-1">Code: Re-checking earlier logic-metric results across label sets</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-6">Dev results evaluation</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-7">R_COMP dataset</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-8">Rename tradeoff</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/evaluation-2">Mechanism decomposition</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/research-1">Code: What is new about peer agreement for logic</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/dataset-4">E2-A held-out data</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/experiment-9">Dead ends</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/experiment-10">Code: Do symbol hints help model agreement checks?</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/dataset-5">Code: Name-free labels for free-vocabulary logic translations</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/evaluation-3">Code: Can shared vocabulary fix consensus blind spots?</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-11">Code: Consensus vs LLM judges on fresh logic data</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-12">Code: Second fresh sample of long logic sentences</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-13">R_COMP FREE</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-14">Code: Screening fixes for model-agreement false alarms</a></li>
        <li><a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/evaluation-4">Code: Corrected record: every paper number checked</a></li>
      </ul>
```

### [104] TOOL RESULT — Edit · 2026-09-25 09:44:10 UTC

```
{"filePath": "/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/index.html", "oldString": "      <ul class=\"artifacts\">\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-1\">Consensus scoring</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-3\">Development set E</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-4\">Baselines</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-2/experiment-5\">p_peer_text (fused)</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-6\">Dev results evaluation</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-7\">R_COMP dataset</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-8\">Rename tradeoff</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/evaluation-2\">Mechanism decomposition</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/dataset-4\">E2-A held-out data</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/experiment-9\">Dead ends</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-13\">R_COMP FREE</a></li>\n      </ul>", "newString": "      <ul class=\"artifacts\">\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-1\">Consensus scoring</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-3\">Development set E</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-4\">Baselines</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/dataset-1\">Code: Held-out logic translation test set, panel-checked</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-2/experiment-5\">p_peer_text (fused)</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-2/dataset-3\">Code: Long logic sentences and FOL error suite</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-2/evaluation-1\">Code: Re-checking earlier logic-metric results across label sets</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-6\">Dev results evaluation</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-7\">R_COMP dataset</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-8\">Rename tradeoff</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/evaluation-2\">Mechanism decomposition</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/research-1\">Code: What is new about peer agreement for logic</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/dataset-4\">E2-A held-out data</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/experiment-9\">Dead ends</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/experiment-10\">Code: Do symbol hints help model agreement checks?</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/dataset-5\">Code: Name-free labels for free-vocabulary logic translations</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/evaluation-3\">Code: Can shared vocabulary fix consensus blind spots?</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-11\">Code: Consensus vs LLM judges on fresh logic data</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-12\">Code: Second fresh sample of long logic sentences</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-13\">R_COMP FREE</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-14\">Code: Screening fixes for model-agreement false alarms</a></li>\n        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/evaluation-4\">Code: Corrected record: every paper number checked</a></li>\n      </ul>", "originalFile": null, "structuredPatch": [{"oldStart": 498, "oldLines": 14, "newStart": 498, "newLines": 25, "lines": ["         <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-1\">Consensus scoring</a></li>", "         <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-3\">Development set E</a></li>", "         <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-4\">Baselines</a></li>", "+        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/dataset-1\">Code: Held-out logic translation test set, panel-checked</a></li>", "         <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-2/experiment-5\">p_peer_text (fused)</a></li>", "+        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-2/dataset-3\">Code: Long logic sentences and FOL error suite</a></li>", "+        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-2/evaluation-1\">Code: Re-checking earlier logic-metric results across label sets</a></li>", "         <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-6\">Dev results evaluation</a></li>", "         <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-7\">R_COMP dataset</a></li>", "         <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-8\">Rename tradeoff</a></li>", "         <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/evaluation-2\">Mechanism decomposition</a></li>", "+        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/research-1\">Code: What is new about peer agreement for logic</a></li>", "         <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/dataset-4\">E2-A held-out data</a></li>", "         <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/experiment-9\">Dead ends</a></li>", "+        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/experiment-10\">Code: Do symbol hints help model agreement checks?</a></li>", "+        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/dataset-5\">Code: Name-free labels for free-vocabulary logic translations</a></li>", "+        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/evaluation-3\">Code: Can shared vocabulary fix consensus blind spots?</a></li>", "+        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-11\">Code: Consensus vs LLM judges on fresh logic data</a></li>", "+        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-12\">Code: Second fresh sample of long logic sentences</a></li>", "         <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-13\">R_COMP FREE</a></li>", "+        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-14\">Code: Screening fixes for model-agreement false alarms</a></li>", "+        <li><a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/evaluation-4\">Code: Corrected record: every paper number checked</a></li>", "       </ul>", "     </section>", " "]}], "userModified": false, "replaceAll": false, "contentNotInModelContext": true}
```

### [105] ASSISTANT · 2026-09-25 09:44:24 UTC

```
Now add the executive summary and round report links to the footer.
```

### [106] TOOL CALL — Edit · 2026-09-25 09:44:24 UTC

```
File: /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/index.html
OLD:     <footer>
      <div class="links">
        <a href="https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/paper.pdf">Paper (PDF)</a>
        <a href="https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/report.pdf">Report (PDF)</a>
        <a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3">Code Repository</a>
      </div>
NEW:     <footer>
      <div class="links">
        <a href="https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/paper.pdf">Paper (PDF)</a>
        <a href="https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/report.pdf">Report (PDF)</a>
        <a href="https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/exec_summary.pdf">Read the executive summary</a>
        <a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3">Code Repository</a>
      </div>
      <h3 style="font-size:.95em; margin-top:1em">Round Reports</h3>
      <div class="links">
        <a href="https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/round-1/report.pdf">Round 1</a>
        <a href="https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/round-2/report.pdf">Round 2</a>
        <a href="https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/round-3/report.pdf">Round 3</a>
        <a href="https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/round-4/report.pdf">Round 4</a>
        <a href="https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/round-5/report.pdf">Round 5</a>
      </div>
```

### [107] TOOL RESULT — Edit · 2026-09-25 09:44:24 UTC

```
{"filePath": "/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/index.html", "oldString": "    <footer>\n      <div class=\"links\">\n        <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/paper.pdf\">Paper (PDF)</a>\n        <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/report.pdf\">Report (PDF)</a>\n        <a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3\">Code Repository</a>\n      </div>", "newString": "    <footer>\n      <div class=\"links\">\n        <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/paper.pdf\">Paper (PDF)</a>\n        <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/report.pdf\">Report (PDF)</a>\n        <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/exec_summary.pdf\">Read the executive summary</a>\n        <a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3\">Code Repository</a>\n      </div>\n      <h3 style=\"font-size:.95em; margin-top:1em\">Round Reports</h3>\n      <div class=\"links\">\n        <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/round-1/report.pdf\">Round 1</a>\n        <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/round-2/report.pdf\">Round 2</a>\n        <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/round-3/report.pdf\">Round 3</a>\n        <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/round-4/report.pdf\">Round 4</a>\n        <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/round-5/report.pdf\">Round 5</a>\n      </div>", "originalFile": null, "structuredPatch": [{"oldStart": 524, "oldLines": 8, "newStart": 524, "newLines": 17, "lines": ["       <div class=\"links\">", "         <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/paper.pdf\">Paper (PDF)</a>", "         <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/report.pdf\">Report (PDF)</a>", "+        <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/exec_summary.pdf\">Read the executive summary</a>", "         <a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3\">Code Repository</a>", "       </div>", "+      <h3 style=\"font-size:.95em; margin-top:1em\">Round Reports</h3>", "+      <div class=\"links\">", "+        <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/round-1/report.pdf\">Round 1</a>", "+        <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/round-2/report.pdf\">Round 2</a>", "+        <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/round-3/report.pdf\">Round 3</a>", "+        <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/round-4/report.pdf\">Round 4</a>", "+        <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/round-5/report.pdf\">Round 5</a>", "+      </div>", "       <div class=\"citation\">@article{anonymous2026consensus,", "   title={Pre-Registered Cross-Family Solver Consensus Outperforms LLM Judges on Templated NL-to-FOL Translation with a Supplied Predicate Signature},", "   author={Anonymous},"]}], "userModified": false, "replaceAll": false, "contentNotInModelContext": true}
```

### [108] ASSISTANT · 2026-09-25 09:44:40 UTC

```
Now let me verify all 17 required URLs are present and retest with Playwright.
```

### [109] TOOL CALL — Bash · 2026-09-25 09:44:40 UTC

```
Verify all 17 required URLs are in index.html:
python3 << 'PYEOF'
required = [
    "https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/dataset-1",
    "https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-2/dataset-3",
    "https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-2/evaluation-1",
    "https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/research-1",
    "https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/experiment-10",
    "https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/dataset-5",
    "https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/evaluation-3",
    "https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-11",
    "https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-12",
    "https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-14",
    "https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/evaluation-4",
    "https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/exec_summary.pdf",
    "https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/round-1/report.pdf",
    "https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/round-2/report.pdf",
    "https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/round-3/report.pdf",
    "https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/round-4/report.pdf",
    "https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_Jhw6i0bFXdo3/round-5/report.pdf",
]

with open("index.html") as f:
    html = f.read()

missing = []
for url in required:
    if url not in html:
        missing.append(url)

if missing:
    print(f"MISSING {len(missing)} URLs:")
    for u in missing:
        print(f"  {u}")
else:
    print(f"All {len(required)} required URLs present.")
PYEOF
```

### [110] TOOL RESULT — Bash · 2026-09-25 09:44:40 UTC

```
{"stdout": "All 17 required URLs present.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [111] TOOL CALL — Bash · 2026-09-25 09:44:58 UTC

```
Retest page with Playwright after adding missing links:
python3 << 'PYEOF'
import asyncio
from playwright.async_api import async_playwright
import os

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        errors = []

        for width in [390, 1440]:
            page = await browser.new_page(viewport={"width": width, "height": 900})
            page.on("console", lambda msg: errors.append(f"[{width}px] console.{msg.type}: {msg.text}") if msg.type == "error" else None)
            page.on("pageerror", lambda err: errors.append(f"[{width}px] pageerror: {err}"))

            url = "file://" + os.path.abspath("index.html")
            await page.goto(url, wait_until="networkidle")

            sw = await page.evaluate("document.documentElement.scrollWidth")
            cw = await page.evaluate("document.documentElement.clientWidth")
            if sw > cw + 2:
                errors.append(f"[{width}px] horizontal scroll: {sw} > {cw}")

            imgs = await page.query_selector_all(".fig img")
            for img in imgs:
                src = await img.get_attribute("src")
                nw = await img.evaluate("el => el.naturalWidth")
                if nw == 0:
                    errors.append(f"[{width}px] img not loaded: {src}")
                else:
                    print(f"[{width}px] OK img: {src}")

            # Lightbox
            first_img = await page.query_selector(".fig img")
            if first_img:
                await first_img.click()
                lb = await page.query_selector("#lightbox")
                h = await lb.get_attribute("hidden")
                if h is not None:
                    errors.append(f"[{width}px] lightbox did not open")
                else:
                    await page.keyboard.press("Escape")
                    h2 = await lb.get_attribute("hidden")
                    if h2 is None:
                        errors.append(f"[{width}px] lightbox did not close")
                    else:
                        print(f"[{width}px] lightbox OK")

            # Count links
            links = await page.query_selector_all("a[href^='https://']")
            print(f"[{width}px] external links: {len(links)}")

            await page.close()

        await browser.close()
        if errors:
            print("\n=== ERRORS ===")
            for e in errors:
                print(e)
        else:
            print("\n=== ALL TESTS PASSED ===")

asyncio.run(test())
PYEOF
```

### [112] TOOL RESULT — Bash · 2026-09-25 09:45:24 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false, "backgroundTaskId": "bo5txgvmt", "timedOutAfterMs": 30000}
```

### [113] TOOL CALL — Bash · 2026-09-25 09:45:28 UTC

```
Check Playwright test output:
cat /tmp/claude-0/-ai-inventor-aii-data-runs-run-Jhw6i0bFXdo3-4-gen-paper-repo--4-assemble-paper-paper/bf7fe44a-e441-4da9-8474-86e4d0bfd56a/tasks/bo5txgvmt.output 2>/dev/null
```

### [114] TOOL RESULT — Bash · 2026-09-25 09:45:28 UTC

```
{"stdout": "[390px] OK img: figures/fig_sig_tercile_v0.png\n[390px] OK img: figures/fig_dev_auroc_v0.png\n[390px] OK img: figures/fig_complexity_v0.png\n[390px] OK img: figures/fig_k_curve_v0.png\n[390px] lightbox OK\n[390px] external links: 34\n[1440px] OK img: figures/fig_sig_tercile_v0.png\n[1440px] OK img: figures/fig_dev_auroc_v0.png\n[1440px] OK img: figures/fig_complexity_v0.png\n[1440px] OK img: figures/fig_k_curve_v0.png\n[1440px] lightbox OK\n[1440px] external links: 34", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [115] TOOL CALL — Bash · 2026-09-25 09:45:36 UTC

```
Check if test completed:
sleep 5 && cat /tmp/claude-0/-ai-inventor-aii-data-runs-run-Jhw6i0bFXdo3-4-gen-paper-repo--4-assemble-paper-paper/bf7fe44a-e441-4da9-8474-86e4d0bfd56a/tasks/bo5txgvmt.output 2>/dev/null | tail -5
```

### [116] TOOL RESULT — Bash · 2026-09-25 09:45:38 UTC

```
{"stdout": "[1440px] external links: 34\n\n=== ALL TESTS PASSED ===\n\n[exited with code 0]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [117] ASSISTANT · 2026-09-25 09:45:43 UTC

```
All tests pass. 4 images loaded, lightbox works, no horizontal scroll, no console errors, 34 external links at both 390px and 1440px. All 17 previously missing URLs are now included. The page remains fully self-contained with all CSS/JS inline.
```
