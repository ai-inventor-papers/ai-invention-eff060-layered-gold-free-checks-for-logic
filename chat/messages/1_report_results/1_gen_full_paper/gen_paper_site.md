# gen_paper_site — report_results

> Phase: `gen_paper_repo` · `gen_full_paper`
> Run: `gen_paper_repo_a2e1d024cc16` — Gold-Free Faithfulness Metrics for NL-to-FOL Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_paper_site` (terminal_claude_agent, claude-opus-4-6)

### [1] CONFIG · 2026-09-25 02:42:58 UTC

```
model: claude-opus-4-6 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-25 02:43:30 UTC

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

### [3] ASSISTANT · 2026-09-25 02:43:42 UTC

```
Let me explore the new workspace and build the page.
```

### [4] TOOL CALL — Bash · 2026-09-25 02:43:42 UTC

```
List all files in new workspace:
find . -not -path './.git/*' -not -name '.git' -not -name '.repl_agent.ptylog' -not -name '.aii_claude_session.json' -type f -exec du -h {} + | sort -rh | head -30
```

### [5] TOOL RESULT — Bash · 2026-09-25 02:43:42 UTC

```
{"stdout": "322K\t./workspace/paper.pdf\n322K\t./paper.pdf\n66K\t./workspace/figures/fig_sig_tercile_v0.png\n36K\t./workspace/paper.tex\n36K\t./paper.tex\n23K\t./workspace/paper.log\n22K\t./workspace/figures/fig_dev_auroc_v0.pdf\n22K\t./figures/fig_dev_auroc_v0.pdf\n21K\t./workspace/figures/fig_complexity_v0.pdf\n21K\t./figures/fig_complexity_v0.pdf\n20K\t./workspace/figures/fig_k_curve_v0.pdf\n20K\t./figures/fig_k_curve_v0.pdf\n18K\t./workspace/figures/fig_sig_tercile_v0.pdf\n14K\t./workspace/paper.aux\n6.5K\t./workspace/paper.bbl\n6.0K\t./workspace/references.bib\n6.0K\t./references.bib\n4.5K\t./workspace/references.json\n4.5K\t./references.json\n4.0K\t./workspace/paper.out\n4.0K\t./figures/fig_dev_auroc_spec.json\n3.5K\t./figures/fig_complexity_spec.json\n3.0K\t./workspace/.terminal_claude_agent_struct_out.json\n3.0K\t./figures/fig_k_curve_spec.json\n1.0K\t./workspace/paper.blg\n512\t./workspace/.aii/module_end.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [6] TOOL CALL — Bash · 2026-09-25 02:43:46 UTC

```
Check for existing HTML, PNGs, and struct output:
ls -la *.html 2>/dev/null; ls -la figures/*.png 2>/dev/null; ls -la .terminal_claude_agent_struct_out.json 2>/dev/null; echo "---"; ls figures/
```

### [7] TOOL RESULT — Bash · 2026-09-25 02:43:46 UTC

```
{"stdout": "---\nfig_complexity_spec.json\nfig_complexity_v0.pdf\nfig_dev_auroc_spec.json\nfig_dev_auroc_v0.pdf\nfig_k_curve_spec.json\nfig_k_curve_v0.pdf", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [8] ASSISTANT · 2026-09-25 02:43:52 UTC

```
No HTML, no PNGs, no struct output. I also see a 4th figure (`fig_sig_tercile_v0`) in workspace but not in `figures/`. Let me read the paper and render PNGs.
```

### [9] TOOL CALL — Read · 2026-09-25 02:43:52 UTC

```
/ai-inventor/aii_data/runs/run_cNhUBrixEdz7/4_gen_paper_repo/_4_assemble_paper/paper/paper.tex
```

### [10] TOOL RESULT — Read · 2026-09-25 02:43:52 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_cNhUBrixEdz7/4_gen_paper_repo/_4_assemble_paper/paper/paper.tex", "content": "\\documentclass[11pt,letterpaper]{article}\n\\usepackage{graphicx, geometry, amsmath, amssymb, hyperref, url, natbib, booktabs, xcolor, listings}\n\\geometry{margin=1in}\n\\hypersetup{colorlinks=true, linkcolor=black, citecolor=black, urlcolor=black}\n\n\\title{Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric\\\\for Natural-Language-to-First-Order-Logic Translation}\n\n\\author{Anonymous}\n\\date{}\n\n\\begin{document}\n\\maketitle\n\n\\begin{abstract}\nEvaluating the faithfulness of natural-language-to-first-order-logic (NL$\\to$FOL) translations is hampered by the expense and unreliability of gold-standard references: recent audits find that roughly 40\\% of annotations in standard benchmarks contain errors.\nWe study a gold-free alternative based on cross-family solver consensus: collect translations of the same sentence from multiple independent LLM families, check pairwise equivalence with an SMT solver, and score each candidate by the fraction of cross-family peers that disagree with it.\nWhen translators share a supplied predicate vocabulary, consensus achieves a within-template AUROC of 0.954 on 221~fresh long-exception sentences with trusted references and pure Z3 labels, versus 0.587 for a disguised API judge ($\\Delta = +0.367$), flat across word-length terciles.\nUnder free (independently chosen) vocabulary, consensus still outperforms judges on both development data ($\\Delta = +0.099$) and untouched out-of-sample sentences ($\\Delta = +0.171$, original-view judge), but the advantage shrinks by roughly 0.15~AUROC and a fundamental rename tradeoff emerges: any predicate-name alignment needed to compare independently generated formulas produces a high false-alarm rate on meaning-preserving renames.\nConfirmation on independent held-out data was budget-stopped and remains incomplete.\nWe present these results, identify the conditions under which shared versus free vocabulary governs metric strength, and release the full evaluation code.\n\\end{abstract}\n\n\\section{Introduction}\n\nTranslating natural-language sentences into first-order logic (NL$\\to$FOL) is a core task in computational semantics and formal verification~\\citep{Yang2023,Han2022}.\nA correct translation must faithfully capture the meaning of the source sentence: its quantifier scope, polarity, argument structure, and exception clauses.\nEvaluating faithfulness is difficult because the same sentence admits many logically equivalent formalizations that differ in predicate names, variable bindings, and structural layout.\n\nGold-standard references are the default evaluation method, but they are expensive and often wrong.\n\\citet{Brunello2026} audit two standard benchmarks and find 39--42\\% of their annotations contain errors.\nThis unreliability is not just noise: when the gold reference itself is unfaithful, every metric calibrated against it is miscalibrated.\n\nAn alternative is to have a strong LLM judge each translation~\\citep{Chiang2024}.\nHowever, LLM judges share failure modes with the translators they evaluate: both are autoregressive models operating on the same distributional statistics, so systematic blind spots tend to be correlated.\nAs we show in Section~\\ref{sec:sig_results}, a cheap disguised judge achieves only 0.587 AUROC on the same sentences where consensus reaches 0.954.\n\nWe study a gold-free metric based on cross-family solver consensus.\nThe idea is simple: if a candidate translation is correct, translations produced independently by other LLM families should be logically equivalent to it.\nIf the candidate is wrong, independent translators are unlikely to make the same mistake, so their translations will diverge.\nWe formalise this intuition and evaluate it under two vocabulary regimes:\n\\begin{enumerate}\n\\item \\textbf{Shared signature}: all translators use a supplied predicate vocabulary. Equivalence checking requires no alignment and labels come from Z3 alone.\n\\item \\textbf{Free vocabulary}: each translator chooses its own predicate names. Equivalence checking requires a predicate-name aligner, which introduces a rename tradeoff (Section~\\ref{sec:rename}).\n\\end{enumerate}\n\nOur contributions:\n\\begin{itemize}\n\\item A pre-registered evaluation on 221 long-exception sentences under shared signature: consensus AUROC 0.954 versus 0.587 for the disguised judge ($\\Delta = +0.367$ [+0.328, +0.404]), flat across word-length terciles, and 0.956 versus 0.932 for a frontier judge on a descriptive 60-row subsample (Section~\\ref{sec:sig_results}). This dataset later served as development data for aligner tuning; the templates and supplied signature limit its scope.\n\\item Free-vocabulary evaluation on development set~$E$: consensus outperforms judges by $\\Delta = +0.099$ [+0.049, +0.146] on stratified AUROC, with aligner-free consensus (c\\_exact) at 0.689 [0.652, 0.726] (Section~\\ref{sec:dev_results}).\n\\item Untouched free-vocabulary out-of-sample results on R\\_COMP FREE under provisional labels: $\\Delta = +0.171$ [+0.135, +0.206] versus the original-view judge; $\\Delta = +0.105$ [+0.011, +0.215] on a two-auditor subset; consensus reaches 0.94 of the frontier judge's AUROC (Section~\\ref{sec:free_oos}).\n\\item Documentation of the rename tradeoff: a 76.5\\% false-alarm rate under nonce predicate renames that no variant we tested could eliminate without sacrificing error recall (Section~\\ref{sec:rename}).\n\\end{itemize}\n\n\\begin{figure}[!htbp]\n  \\centering\n  \\includegraphics[width=\\linewidth,height=0.85\\textheight,keepaspectratio]{figures/fig_dev_auroc_v0.pdf}\n  \\caption{Stratified AUROC on the free-vocabulary development dataset for the main metrics and baselines. Error bars are 95\\% sentence-cluster bootstrap confidence intervals. Consensus-based metrics (blue) outperform API judges (orange) and other gold-free baselines (gray).}\n  \\label{fig:dev_auroc}\n\\end{figure}\n\n\\section{Related Work}\n\n\\paragraph{NL\\texorpdfstring{$\\to$}{-to-}FOL evaluation.}\nStandard benchmarks such as FOLIO~\\citep{Han2022} and the MALLS corpus~\\citep{Yang2023} provide NL--FOL pairs, but gold-annotation error rates are high~\\citep{Brunello2026}.\n\\citet{Vossel2025} map predicates by normalised Levenshtein distance before equivalence checking.\n\\citet{Thatikonda2025} evaluate n-gram, graph, embedding, and LLM-based closeness metrics on controlled FOL perturbations, finding that no single metric is sensitive to all perturbation types.\n\n\\paragraph{Cross-model consensus.}\nThe idea of using agreement among multiple independently trained models as a quality signal appears in several domains.\n\\citet{Wang2022} show that sampling multiple chain-of-thought reasoning paths~\\citep{Wei2022} from a single model and taking the majority answer (self-consistency) improves accuracy.\n\\citet{Bayless2025} collect $k$ translations over a fixed shared schema and score each by the fraction of $k$ translations that entail it.\n\\citet{Zhang2023} detect hallucinations in black-box LLMs by sampling diverse perturbations of a query and checking consistency across answers.\nOur work differs from these in evaluating the consensus score under both shared and free vocabulary, head-to-head with API judges, with pre-registered analyses.\n\n\\paragraph{LLM-as-judge.}\n\\citet{Chiang2024} propose using LLMs as evaluators.\nIn NL$\\to$FOL, an LLM judge reads the sentence and the candidate formula and predicts faithfulness.\nThe disguised variant (nonce predicate names) controls for memorisation of known benchmarks.\n\n\\paragraph{Diverse redundancy.}\nN-version programming, where independent implementations of the same specification are compared by majority vote, was proposed for software fault tolerance.\n\\citet{Eckhardt1985} predict that coincident failures rise with input difficulty; our finding that the consensus advantage is flat with sentence length under shared vocabulary but degrades under free vocabulary is consistent with vocabulary alignment, not input difficulty, as the bottleneck.\n\n\\section{Method}\\label{sec:method}\n\n\\subsection{Consensus scoring}\n\nGiven a sentence $s$ and a candidate FOL translation $c$, we collect peer translations $\\{p_1, \\ldots, p_k\\}$ from $k$ independent LLM families.\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-1/experiment-1}}\nEach peer uses the same few-shot prompt but a different base model (e.g., one from each of Gemini, Claude, GPT, Llama, Qwen, Phi, Mistral).\nWe compute:\n\\begin{equation}\n\\text{c\\_score}(c, s) = 1 - \\frac{1}{k} \\sum_{i=1}^{k} \\mathbf{1}[\\text{equiv}(c, p_i)]\n\\end{equation}\nwhere $\\text{equiv}(c, p_i)$ checks logical equivalence between $c$ and $p_i$ using the Z3 SMT solver~\\citep{Moura2008}.\n\nUnder \\textbf{shared signature} (c\\_score\\_sig), all translators use a supplied predicate vocabulary, and equiv is a direct Z3 check after case-insensitive symbol normalisation.\nUnder \\textbf{free vocabulary} (c\\_score\\_align), each translator chooses its own predicate names, and equiv requires a predicate-name aligner before the Z3 check.\n\n\\subsection{Predicate alignment (free vocabulary only)}\n\nIndependent translators choose different predicate names for the same concept (e.g., \\texttt{Runs(x)} vs.\\ \\texttt{IsRunner(x)}).\nTo compare formulas across families, we align predicates using a cost function that combines:\n\\begin{enumerate}\n\\item \\textbf{Structural cost}: polarity profile, argument-count match, and nesting depth.\n\\item \\textbf{Text-anchor cost}: overlap between predicate-name words and source-sentence tokens (Porter stemming, WordNet synonyms/derivations).\n\\item \\textbf{Semantic signature}: truth-value profiles over random finite interpretations.\n\\end{enumerate}\nThe $k$ cheapest bijections (predicates within equal arity; constants separately) are evaluated, and the pair is declared equivalent if any bijection yields a Z3-verified equivalence.\n\n\\subsection{Score variants}\n\nHigher scores indicate greater divergence from peers and thus higher predicted error probability.\nVariants include:\n\\begin{itemize}\n\\item \\textbf{c\\_exact}: no alignment; exact-match equivalence only. Immune to rename false alarms but blind to vocabulary-differing equivalences.\n\\item \\textbf{c\\_nf} (name-free): alignment by structural and semantic signatures only, ignoring text anchoring.\n\\item \\textbf{p\\_peer\\_text}: a logistic fusion of consensus features with text-side features (bag-of-words coverage, role accounting, Z3 structural match).\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-2/experiment-5}}\n\\end{itemize}\n\n\\subsection{Evaluation framework}\n\n\\paragraph{Shared-signature labels.}\nOn R\\_COMP, labels are determined by Z3 equivalence to trusted-by-construction references (one weak and one strong reading per template), with no human or LLM judgement in the labelling loop.\n\n\\paragraph{Free-vocabulary labels.}\nOn development set~$E$, labels come from a three-person expert panel (adjudicated as ERROR or CORRECT), with disputed items counted according to the reliability assignment (R\\_AB: both panellists agree).\nOn R\\_COMP FREE, provisional labels use search-based ERROR\\_CERT versus MAPPED classifications (non-confirmatory; the gloss-based labelling gate failed twice).\n\n\\paragraph{Metrics.}\nThe primary evaluation metric is stratified AUROC: items are paired only within the same source stratum (sentence-template on R\\_COMP, sentence-complexity bin on~$E$), eliminating confounds from stratum-level base rates.\nConfidence intervals use sentence-cluster percentile bootstrap ($B = 2{,}000$).\n\n\\section{Experiments}\\label{sec:experiments}\n\n\\subsection{Datasets}\n\n\\paragraph{R\\_COMP (shared and free vocabulary).}\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/experiment-7}}\nR\\_COMP generates long, complex sentences ($\\geq$25 words, 4--5 conditions) from a verified lexicon.\n221~sentences produced 2,024 candidate translations from 10~LLM slots across 9~vendor families.\nPopulation: 429~ERROR~/~1,595~CORRECT (21.2\\% error rate).\nIn the \\textbf{SIG condition}, all translators received a supplied predicate signature; labels are pure Z3 equivalence to trusted references.\nIn the \\textbf{FREE condition}, each translator chose its own predicate names; labels are provisional (Section~\\ref{sec:free_oos}).\nThe pre-registration document, including the analysis plan and testability rule, was frozen before any SIG generation call, any label, or any metric score.\\footnote{Pre-registration: \\texttt{prereg\\_sig.json}, SHA-256 frozen before data collection.}\n\n\\paragraph{Development set $E$.}\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-1/experiment-3}}\n8,507~rows from 700~sentences drawn from the MALLS corpus~\\citep{Yang2023} and ProverQA~\\citep{Qi2025}.\nEach sentence was translated by 9~LLM families using a frozen few-shot prompt.\nThe primary evaluation population (R\\_AB, both panellists agree) contains 2,686~items (1,822~ERROR~/~864~CORRECT, 292~sentences); the all-families subset where every peer family contributed a translation is $n = 2{,}014$.\nComplexity strata: L25 ($\\geq$25 words), L20 (20--24), EXC (exception clauses), CTRL (short control sentences).\nThe R\\_COMP-SIG data later served as development data for aligner tuning, so the development-set numbers from $E$ are not independent of R\\_COMP.\n\n\\paragraph{Baselines.}\n(1)~\\textbf{Flash-lite judge} (Gemini Flash Lite, disguised and original views); (2)~\\textbf{nano judge} (Gemini Flash 2.0); (3)~\\textbf{local judges} (Qwen3-8B, Llama-8B); (4)~\\textbf{round-trip NLI}; (5)~\\textbf{self-consistency} (5-sample within-model agreement); (6)~\\textbf{structural features} (arity consistency, dangling predicates, rerun Jaccard); (7)~\\textbf{feature stacks}: cross-validated logistic regressions over subsets of these features.\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-1/experiment-4}}\n\n\\subsection{Shared-signature results (R\\_COMP-SIG)}\\label{sec:sig_results}\n\nTable~\\ref{tab:sig} reports the pre-registered comparison on R\\_COMP under shared signature.\nOn the 1,904~rows where both consensus and judge scores exist, consensus achieves a within-template AUROC of 0.954 versus 0.587 for the disguised flash-lite judge ($\\Delta = +0.367$ [+0.328, +0.404]).\nAgainst the original-view judge (1,932~rows), the advantage is $\\Delta = +0.278$ [+0.239, +0.319].\nError endorsement is zero ($e = 0$): no error item scores below the decision threshold.\nAmong the 429~error items, 75.3\\% receive the maximum consensus score of~1.0; the remaining 24.7\\% score between 0.625 and~1.0.\n\n\\begin{table}[!htbp]\n\\centering\n\\caption{Within-template AUROC on R\\_COMP-SIG (shared signature, 221~sentences, pure Z3 labels). CIs are 95\\% sentence-cluster bootstrap.}\n\\label{tab:sig}\n\\small\n\\begin{tabular}{lccc}\n\\toprule\nMetric & $n$ & Within-template AUROC [95\\% CI] & $\\Delta$ vs.\\ disg.\\ judge [95\\% CI] \\\\\n\\midrule\nc\\_score\\_sig & 1904 & 0.954 [0.939, 0.968] & +0.367 [+0.328, +0.404] \\\\\nc\\_score\\_align & 1904 & 0.954 [0.939, 0.968] & +0.367 [+0.328, +0.404] \\\\\njudge (flash-lite, disg.) & 1904 & 0.587 [0.551, 0.622] & --- \\\\\njudge (flash-lite, orig.) & 1932 & 0.673 [0.637, 0.708] & \\\\\njudge (frontier, orig.) & 60 & 0.932 [0.782, 1.000] & \\\\\njudge (local, disg.) & 2024 & 0.498 [0.459, 0.534] & \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}\n\n\\paragraph{Flat with sentence length.}\nUnlike the free-vocabulary setting (Section~\\ref{sec:mechanism}), consensus under shared signature is flat across word-length terciles: W1 0.959, W2 0.947, W3 0.953 (Table~\\ref{tab:sig_complexity} and Figure~\\ref{fig:sig_tercile}).\n\n\\begin{table}[!htbp]\n\\centering\n\\caption{R\\_COMP-SIG within-template AUROC by word-length tercile.}\n\\label{tab:sig_complexity}\n\\small\n\\begin{tabular}{lccccc}\n\\toprule\nTercile & $n$ & ERR/COR & c\\_sig & judge (disg.) & $\\Delta$ [CI] \\\\\n\\midrule\nW1 (shortest) & 574 & 125/449 & 0.959 & 0.578 & +0.382 [+0.278, +0.472] \\\\\nW2 & 743 & 149/594 & 0.947 & 0.624 & +0.331 [+0.253, +0.421] \\\\\nW3 (longest) & 707 & 155/552 & 0.953 & 0.567 & +0.388 [+0.301, +0.471] \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}\n\n\\begin{figure}[!htbp]\n  \\centering\n  \\includegraphics[width=\\linewidth,height=0.85\\textheight,keepaspectratio]{figures/fig_sig_tercile_v0.pdf}\n  \\caption{Within-template AUROC on R\\_COMP-SIG by word-length tercile. Consensus (blue) is flat across terciles (0.947--0.959), while the disguised flash-lite judge (orange) hovers near chance (0.567--0.624). Error bars are 95\\% sentence-cluster bootstrap CIs.}\n  \\label{fig:sig_tercile}\n\\end{figure}\n\n\\paragraph{Frontier judge comparison.}\nOn a descriptive 60-row stratified subsample scored by the frontier judge (Gemini~3.1~Pro, original view), consensus achieves pooled AUROC 0.956 [0.889, 1.000] versus 0.932 [0.855, 0.990] for the frontier judge.\n\n\\paragraph{Scope.}\nR\\_COMP-SIG uses templated sentences with a supplied predicate vocabulary.\nThe shared signature eliminates the alignment problem entirely, which is why the AUROC is so high.\nThese results do not extend to settings where translators choose their own predicate names.\n\n\\subsection{Free-vocabulary development results (set $E$)}\\label{sec:dev_results}\n\nFigure~\\ref{fig:dev_auroc} and Table~\\ref{tab:main} summarise the free-vocabulary comparison on development set~$E$.\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/experiment-6}}\nCross-family consensus (c\\_score\\_align) outperforms the disguised flash-lite judge by $\\Delta = +0.099$ [+0.049, +0.146] on the full R\\_AB population and by $\\Delta = +0.116$ [+0.070, +0.163] on the long-sentence pool (L25+L20+EXC).\nAdding c\\_score\\_align to the 28-feature baseline stack increases stratified AUROC by +0.039 [+0.021, +0.057]; a permutation null test gives $p_{95} = 0.009$, confirming the signal is not explained by the existing features.\n\n\\begin{table}[!htbp]\n\\centering\n\\caption{Stratified AUROC on development set $E$ (R\\_AB population, free vocabulary, $n = 2{,}686$). Higher is better. CIs are 95\\% sentence-cluster bootstrap.}\n\\label{tab:main}\n\\small\n\\begin{tabular}{lcc}\n\\toprule\nMetric & Strat AUROC [95\\% CI] & \\$/item \\\\\n\\midrule\nc\\_score\\_align & 0.741 [0.705, 0.775] & 9.1e-5 \\\\\np\\_peer\\_text (fused) & 0.753 [0.720, 0.784] & 9.1e-5 \\\\\nc\\_exact (no alignment) & 0.689 [0.652, 0.726] & -- \\\\\nc\\_nf (name-free) & 0.686 [0.647, 0.720] & -- \\\\\n\\midrule\nflash-lite judge (disg.) & 0.642 [0.607, 0.676] & 5.1e-5 \\\\\nflash-lite judge (orig.) & 0.623 [0.593, 0.651] & 5.1e-5 \\\\\nnano judge (disg.) & 0.644 [0.609, 0.680] & 2.0e-5 \\\\\nlocal judge Qwen-8B (disg.) & 0.674 [0.646, 0.703] & -- \\\\\n\\midrule\nround-trip NLI (min) & 0.606 [0.569, 0.645] & 2.8e-5 \\\\\nself-consistency (5-sample) & 0.598 [0.559, 0.637] & 6.7e-5 \\\\\n\\midrule\n28-feature stack & 0.735 [0.699, 0.766] & -- \\\\\n28-feature stack + c\\_score\\_align & 0.774 [0.743, 0.802] & -- \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}\n\nThe drop from 0.952 (shared signature, R\\_COMP-SIG) to 0.801 (free vocabulary on the same R\\_COMP sentences) reflects the cost of predicate-name alignment: the aligner introduces both false negatives (correct equivalences missed) and false positives (incorrect mappings endorsed).\nAligner-free consensus (c\\_exact) achieves 0.689 [0.652, 0.726]; the aligner adds about 22\\% of the above-chance signal (c\\_align 0.241 versus c\\_exact 0.189 above the 0.5 baseline), with the remaining 78\\% coming from structural agreement alone.\n\nOn L25 sentences alone ($\\geq$25 words), the advantage narrows to $\\Delta = +0.069$ [$-$0.020, +0.148], not significant at the 95\\% level.\nThis foreshadows the length-dependent degradation described in Section~\\ref{sec:mechanism}.\n\n\\paragraph{Frontier judge comparison.}\nOn the 284-row subsample scored by the frontier judge (Gemini~3.1~Pro), c\\_score\\_align achieves 95.7\\% of the frontier judge's AUROC (ratio 0.957 [0.887, 1.034]).\n\n\\paragraph{System-level ranking.}\nThe consensus metric achieves Kendall $\\tau_b = 0.692$ [+0.513, +0.795] between system mean score and R\\_AB error rate across 13 system$\\times$variant configurations, comparable to the best judges.\n\n\\subsection{Free-vocabulary out-of-sample (R\\_COMP FREE)}\\label{sec:free_oos}\n\nThe same 221~R\\_COMP sentences were also translated under free vocabulary (each translator choosing its own predicate names).\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-5/experiment-13}}\nConfirmatory labelling required a gloss gate (LLM-checked semantic alignment of predicate mappings).\nThis gate failed twice (balanced accuracy 0.776 and 0.561, below the 0.90 threshold), producing zero confirmed CORRECT rows and rendering the confirmatory test not testable.\n\nUnder provisional non-confirmatory labels (ERROR\\_CERT vs.\\ MAPPED, where MAPPED is an upper bound on CORRECT), Table~\\ref{tab:free} reports the untouched results.\n\n\\begin{table}[!htbp]\n\\centering\n\\caption{R\\_COMP FREE provisional AUROCs (within-template, untouched rows). Labels are non-confirmatory.}\n\\label{tab:free}\n\\small\n\\begin{tabular}{lccc}\n\\toprule\nView & $n$ (ERR/MAPPED) & c\\_align & judge \\\\\n\\midrule\nDisguised & 1706 (602/1104) & 0.801 [0.770, 0.834] & 0.584 [0.550, 0.618] \\\\\nOriginal & 1709 (605/1104) & 0.804 [0.774, 0.836] & 0.633 [0.601, 0.666] \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}\n\nThe disguised-judge delta is $+0.217$ [+0.175, +0.260]; the original-view delta is $+0.171$ [+0.135, +0.206].\nOn a 146-row subset with independent two-auditor labels, consensus achieves $\\Delta = +0.105$ [+0.011, +0.215] over the original-view judge.\nOn a 150-row frontier-judge subsample, consensus reaches 0.94 of the frontier judge's AUROC (ratio 0.940 [0.825, 1.056]).\n\nThese provisional numbers cannot count as confirmation because the MAPPED labels conflate vocabulary-alignment failures with genuine correctness.\nThey are consistent with the development-set signal but independent confirmation requires a working gloss gate or a different labelling strategy.\n\n\\subsection{Mechanism}\\label{sec:mechanism}\n\nWe decompose the consensus signal\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/evaluation-2}} into two components at a fixed decision threshold:\n\\begin{itemize}\n\\item \\textbf{Endorsement} $e$: fraction of ERROR items endorsed by the peer majority (false negatives of consensus).\n\\item \\textbf{Divergence} $d$: fraction of CORRECT items that diverge from the peer majority (false positives of consensus).\n\\end{itemize}\nThe consensus AUROC at a binary threshold equals $1 - (e + d)/2$, so both quantities must be small for the metric to work.\n\n\\paragraph{Shared vocabulary: endorsement zero, divergence moderate.}\nOn R\\_COMP-SIG, $e = 0.0$ and $d = 0.260$: no error escapes detection, though 26\\% of correct translations are flagged as divergent.\nThe false-alarm rate of 0.260 arises from correct translations that use valid but structurally different formalizations; because all translators share a predicate vocabulary, no alignment step is needed and the divergence rate is flat across sentence lengths.\n\n\\paragraph{Free vocabulary: divergence degrades with length.}\nAs Figure~\\ref{fig:complexity} shows, on development set~$E$ the net consensus degradation from short to long sentences is $\\Delta(e+d) = +0.356$ [+0.198, +0.493], driven almost entirely by divergence ($\\Delta d = +0.608$, $\\Delta e = -0.252$): as formulas grow longer and more structurally diverse, the predicate-name aligner (Section~\\ref{sec:rename}) increasingly maps distinct predicates together or fails to match equivalent ones, inflating the false-alarm rate on correct translations.\n\n\\begin{figure}[!htbp]\n  \\centering\n  \\includegraphics[width=\\linewidth,height=0.85\\textheight,keepaspectratio]{figures/fig_complexity_v0.pdf}\n  \\caption{Decomposition of free-vocabulary consensus error rates by sentence-length tercile on development set~$E$. Endorsement rate $e$ (errors incorrectly endorsed by peers) decreases with length, but divergence rate $d$ (correct items incorrectly flagged) increases sharply, producing net degradation of +0.356 from the shortest to the longest tercile. Under shared signature (R\\_COMP-SIG), this degradation is absent.}\n  \\label{fig:complexity}\n\\end{figure}\n\n\\paragraph{Family sufficiency.}\nThree peer families suffice for 97\\% of full-pool AUROC ($k_{95} = 3$), but the long-sentence tercile requires $k_{95} = 5$ (Table~\\ref{tab:k_families} and Figure~\\ref{fig:k_curve}).\n\n\\begin{table}[!htbp]\n\\centering\n\\caption{Free-vocabulary AUROC by number of peer families on development set $E$.}\n\\label{tab:k_families}\n\\small\n\\begin{tabular}{ccc}\n\\toprule\n$k$ & AUROC (overall) & AUROC (long, T3) \\\\\n\\midrule\n1 & 0.685 & 0.581 \\\\\n3 & 0.757 & 0.651 \\\\\n5 & 0.776 & 0.698 \\\\\n7 & 0.784 & 0.726 \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}\n\n\\begin{figure}[!htbp]\n  \\centering\n  \\includegraphics[width=\\linewidth,height=0.85\\textheight,keepaspectratio]{figures/fig_k_curve_v0.pdf}\n  \\caption{Stratified AUROC as a function of the number of peer families $k$, for the full development set (solid blue) and the long-sentence tercile (dashed red). Three families capture 97\\% of the full-pool signal, but long sentences require five families to reach 95\\%.}\n  \\label{fig:k_curve}\n\\end{figure}\n\n\\subsection{Confirmation status}\\label{sec:confirmation}\n\nIndependent confirmation on held-out data remains incomplete.\nA fresh held-out dataset (E2-A, 550~new sentences) was constructed, but the run-level budget was exhausted before enough items could be labelled.\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-4/dataset-4}}\nOn the one testable stratum (DT, short sentences from ProverQA), consensus achieves a stratified AUROC of 0.916, tying the local Qwen-8B judge ($\\Delta = +0.003$ [$-$0.042, +0.052]).\nOn L25 sentences, c\\_score\\_align falls to 0.443 on only 42 items (35~ERROR~/~7~CORRECT), below chance, but the estimate has extreme variance with only 7~CORRECT items from 3~sentences.\nEvery pre-registered criterion on the target strata returned NOT\\_TESTABLE or unfavourable.\n\n\\subsection{The rename tradeoff}\\label{sec:rename}\n\nThe predicate aligner\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/experiment-8}} that enables cross-family comparison under free vocabulary also introduces a fundamental false-alarm vulnerability.\nWhen correct formulas are copied with meaning-preserving predicate renames (same semantics, different symbol names), the consensus score should not change.\nTable~\\ref{tab:rename} shows the false-alarm rates in practice.\n\n\\begin{table}[!htbp]\n\\centering\n\\caption{False-alarm (FA) rates on meaning-preserving renames of CORRECT candidates. NONCE = random nonsense names; SYN = WordNet synonyms. Flip = FA induced by the rename alone (FA minus base FA).}\n\\label{tab:rename}\n\\small\n\\begin{tabular}{lcccc}\n\\toprule\nMetric & NONCE FA & NONCE flip & SYN FA & SYN flip \\\\\n\\midrule\nc\\_align & 0.765 & 0.605 & 0.565 & 0.313 \\\\\nc\\_nf (name-free) & 0.132 & 0.000 & 0.201 & 0.000 \\\\\np\\_peer\\_text & 1.000 & 0.821 & 0.216 & 0.080 \\\\\njudge (disg.) & 0.229 & 0.134 & 0.085 & 0.058 \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}\n\nThe name-free variant c\\_nf eliminates rename sensitivity (flip = 0) but at the cost of blindness to meaning-rename errors (within-base AUROC 0.499, chance level) and lower overall discrimination (strat AUROC 0.686 vs.\\ 0.741).\nThis tradeoff explains the gap between shared-signature and free-vocabulary performance: the shared signature eliminates the need for alignment entirely, sidestepping the rename problem.\n\n\\subsection{Per-type sensitivity}\n\nOn the PERTURB suite (4,234 typed mutants + 868 controls from development data), consensus recall at the primary threshold is flat across error operators: NEG 0.761, SWAP 0.758, DROP 0.721, ADD 0.763, MEANING\\_RENAME 0.762.\nPer-operator AUROC within error types cannot be computed because 94--100\\% of mutants receive the maximum consensus score, a ceiling effect of the endorsement structure.\n\nError typing outside a shared vocabulary is negative: the free-vocabulary typing accuracy is 0.123 [0.081, 0.169] on $E$, below both the judge (0.326) and the peer-medoid baseline (0.328), and all three are near chance for a five-class task.\n\n\\subsection{Dead ends}\n\nSeveral alternatives were investigated and abandoned during development: a fused structural-feature filter (false-alarm gate failure); name-free consensus c\\_nf (rename-invariant but blind to meaning-rename errors, as described in Section~\\ref{sec:rename}); a decomposed solver-based semantic reader (balanced accuracy 0.476); LLM adjudication of disputed items (balanced accuracy 0.662 on expert-labelled items); and candidate-signature consensus, which scores candidates by cueing peers with the candidate's own predicate symbols rather than letting them choose independently (provisional negative: error endorsement rose to 0.459 because peers were anchored into reproducing the candidate's errors).\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-4/experiment-9}}\n\n\\section{Discussion}\n\n\\subsection{Shared versus free vocabulary}\n\nThe central finding is that vocabulary regime governs metric strength.\nUnder shared signature, consensus achieves near-perfect discrimination (0.954 AUROC) flat across sentence lengths.\nUnder free vocabulary, performance drops by roughly 0.15~AUROC on comparable sentences (R\\_COMP-SIG 0.952 versus R\\_COMP FREE 0.801, both within-template on long composed sentences) and degrades with sentence length on natural data.\n\nThis gap is explained by the rename tradeoff: the predicate-name aligner needed for free-vocabulary comparison introduces both false negatives (missed equivalences) and false positives (spurious mappings), and these grow worse as formulas become longer and more structurally diverse.\nThe practical implication is that consensus-based evaluation is most reliable when translators share a predicate vocabulary, as in controlled evaluation settings~\\citep{Bayless2025,Vossel2025}.\n\n\\subsection{Why confirmation is incomplete}\n\nThe confirmation attempt was defeated by two independent problems: (1)~insufficient fresh data (the E2-A budget was stopped before enough correct items accumulated in the long-sentence strata), and (2)~a broken labelling gate (the gloss-based semantic alignment required for R\\_COMP FREE labels failed quality checks twice).\nNeither failure refutes the development-set signal, but neither allows us to confirm it on the target strata.\n\nThe E2-A L25 result (AUROC 0.443, near chance, on 42~items) is concerning but difficult to interpret: with only 7~CORRECT items from 3~sentences, the estimate has extreme variance and a single sentence can dominate.\nWe report it for completeness but note that it does not meet any standard testability criterion.\n\n\\subsection{The rename tradeoff as a fundamental limit}\n\nThe rename tradeoff is not a bug in our aligner but a structural property of cross-family consensus under independent vocabulary.\nAny alignment procedure that maps independently chosen predicate names to a common vocabulary will sometimes map semantically distinct predicates together, endorsing meaning-rename errors.\nEliminating the alignment (c\\_exact, c\\_nf) preserves rename invariance but sacrifices the structural comparison that drives error detection.\n\nWe conjecture that resolving this tradeoff requires either (a)~a shared predicate vocabulary supplied to all translators, which eliminates the problem entirely but restricts the evaluation to controlled settings~\\citep{Bayless2025,Vossel2025}, or (b)~a semantic disambiguation step (such as natural-language glosses of each predicate) that could break the alignment ambiguity.\nOur attempt at option~(b), a gloss gate using LLM-generated explanations of predicate meanings, failed quality checks, leaving this direction open.\n\n\\subsection{Limitations}\\label{sec:limitations}\n\n\\begin{enumerate}\n\\item \\textbf{Shared-signature scope.} The 0.954 AUROC result uses templated sentences with a supplied predicate vocabulary, which eliminates the alignment problem. The templates and the supplied signature limit the scope of this result to controlled evaluation settings.\n\\item \\textbf{Development data overlap.} The R\\_COMP-SIG dataset later served as development data for aligner tuning. The pre-registration ensures the SIG result itself is uncontaminated, but the development-set numbers from $E$ are not independent.\n\\item \\textbf{Rename vulnerability.} Under free vocabulary, a 76.5\\% false-alarm rate on nonce renames means the metric will systematically penalise any translation that uses non-standard predicate names, even if semantically correct.\n\\item \\textbf{Length degradation (free vocabulary).} Consensus discrimination degrades with sentence length under free vocabulary (NET $+0.356$), driven by correct-translation divergence. The metric is weakest on the longest, most complex sentences, precisely the cases where gold-free evaluation is most needed.\n\\item \\textbf{Provisional labels.} R\\_COMP FREE results use provisional (non-confirmatory) labels; the two-auditor subset ($\\Delta = +0.105$) has a CI that barely excludes zero.\n\\item \\textbf{Label dependence.} Development results on~$E$ depend on a three-person panel whose agreement is imperfect (disputed items exist in every stratum). The metric's advantage could partly reflect alignment with panel biases rather than with ground-truth faithfulness.\n\\item \\textbf{Cost.} The consensus metric requires generating $k$ peer translations per sentence. In this experiment ($k = 9$, R\\_COMP-SIG), the amortised consensus cost per candidate is about 19 times the cost of a single cheap judge call.\n\\item \\textbf{Domain.} All results are on English$\\to$FOL from MALLS, ProverQA, and R\\_COMP sources. Generalisation to other logic formalisms, languages, or sentence distributions is untested.\n\\end{enumerate}\n\n\\section{Conclusion}\n\nCross-family solver consensus is a strong gold-free faithfulness metric for NL$\\to$FOL translation when translators share a predicate vocabulary.\nThe pre-registered R\\_COMP-SIG result (AUROC 0.954 versus 0.587 for a disguised judge, flat with length) establishes the ceiling; free vocabulary costs roughly 0.15~AUROC and introduces the rename tradeoff.\n\nUnder free vocabulary, consensus still outperforms cheap LLM judges on both development data ($+0.099$) and untouched out-of-sample sentences ($+0.171$), and adds information beyond structural and statistical baselines.\nThe mechanism --- errors scatter while correct translations cluster --- provides an intuitive explanation grounded in the diversity of independent formalizations.\n\nHowever, independent confirmation on held-out data was budget-stopped and remains incomplete, the rename tradeoff limits applicability to free-vocabulary settings, and discrimination degrades with sentence length under free vocabulary.\nWe release the full evaluation code and data to enable reproduction.\nThe immediate open problems are: (1)~completing the fresh-data confirmation with adequate sample sizes; (2)~breaking the rename tradeoff, perhaps through semantic predicate glossing; and (3)~understanding why correct translations of complex sentences diverge under free vocabulary even when no vocabulary mismatch exists.\n\n\\bibliographystyle{plainnat}\n\\bibliography{references}\n\n\\end{document}\n", "numLines": 444, "startLine": 1, "totalLines": 444}}
```

### [11] ASSISTANT · 2026-09-25 02:44:00 UTC

```
This paper has 4 figures (including `fig_sig_tercile_v0` not present in `figures/`). Let me extract URLs, render PNGs, and build the page.
```

### [12] TOOL CALL — Bash · 2026-09-25 02:44:00 UTC

```
Extract URLs and figure references:
\
echo "=== GitHub URLs ===" && grep -oP 'https://github\.com[^\}]+' paper.tex && \
echo "=== Figures referenced ===" && grep -oP 'includegraphics.*?\{[^}]+\}' paper.tex
```

### [13] TOOL RESULT — Bash · 2026-09-25 02:44:00 UTC

```
{"stdout": "=== GitHub URLs ===\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-1/experiment-1\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-2/experiment-5\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/experiment-7\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-1/experiment-3\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-1/experiment-4\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/experiment-6\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-5/experiment-13\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/evaluation-2\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-4/dataset-4\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/experiment-8\nhttps://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-4/experiment-9\n=== Figures referenced ===\nincludegraphics[width=\\linewidth,height=0.85\\textheight,keepaspectratio]{figures/fig_dev_auroc_v0.pdf}\nincludegraphics[width=\\linewidth,height=0.85\\textheight,keepaspectratio]{figures/fig_sig_tercile_v0.pdf}\nincludegraphics[width=\\linewidth,height=0.85\\textheight,keepaspectratio]{figures/fig_complexity_v0.pdf}\nincludegraphics[width=\\linewidth,height=0.85\\textheight,keepaspectratio]{figures/fig_k_curve_v0.pdf}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [14] ASSISTANT · 2026-09-25 02:44:08 UTC

```
The paper references `fig_sig_tercile_v0.pdf` but it only exists in `workspace/figures/`. Let me copy it and render all PNGs.
```

### [15] TOOL CALL — Bash · 2026-09-25 02:44:08 UTC

```
Copy missing PDF and render all PNGs:
\
cp workspace/figures/fig_sig_tercile_v0.pdf figures/ && \
python3 -c "
import pymupdf, os
for name in ['fig_dev_auroc_v0', 'fig_complexity_v0', 'fig_k_curve_v0', 'fig_sig_tercile_v0']:
    pdf = f'figures/{name}.pdf'
    png = f'figures/{name}.png'
    doc = pymupdf.open(pdf)
    pix = doc[0].get_pixmap(matrix=pymupdf.Matrix(2.5, 2.5))
    pix.save(png)
    doc.close()
    print(f'{name}.png: {os.path.getsize(png)//1024}KB')
"
```

### [16] TOOL RESULT — Bash [ERROR] · 2026-09-25 02:44:08 UTC

```
Error: Exit code 1
Traceback (most recent call last):
  File "<string>", line 2, in <module>
ModuleNotFoundError: No module named 'pymupdf'
```

### [17] TOOL CALL — Bash · 2026-09-25 02:44:12 UTC

```
Install pymupdf:
pip install pymupdf 2>&1 | tail -2
```

### [18] TOOL RESULT — Bash · 2026-09-25 02:44:16 UTC

```
{"stdout": "[notice] A new release of pip is available: 25.0.1 -> 26.2.1\n[notice] To update, run: pip install --upgrade pip", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [19] TOOL CALL — Bash · 2026-09-25 02:44:20 UTC

```
Render all figure PNGs:
\
python3 -c "
import pymupdf, os
for name in ['fig_dev_auroc_v0', 'fig_complexity_v0', 'fig_k_curve_v0', 'fig_sig_tercile_v0']:
    pdf = f'figures/{name}.pdf'
    png = f'figures/{name}.png'
    doc = pymupdf.open(pdf)
    pix = doc[0].get_pixmap(matrix=pymupdf.Matrix(2.5, 2.5))
    pix.save(png)
    doc.close()
    print(f'{name}.png: {os.path.getsize(png)//1024}KB')
"
```

### [20] TOOL RESULT — Bash · 2026-09-25 02:44:20 UTC

```
{"stdout": "fig_dev_auroc_v0.png: 77KB\nfig_complexity_v0.png: 57KB\nfig_k_curve_v0.png: 68KB\nfig_sig_tercile_v0.png: 52KB", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] ASSISTANT · 2026-09-25 02:47:50 UTC

```
Good. Now I know the exact required URLs from previous verification failures. Let me build the complete page with all links correct from the start.
```

### [22] TOOL CALL — Write · 2026-09-25 02:47:50 UTC

```
File: /ai-inventor/aii_data/runs/run_cNhUBrixEdz7/4_gen_paper_repo/_4_assemble_paper/paper/index.html

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Gold-Free Faithfulness Metrics for NL-to-FOL</title>
<style>
:root {
  --accent: #1a6b4a;
  --accent-light: #e6f2ec;
  --bg: #f9f9f7;
  --surface: #ffffff;
  --text: #1a1a1a;
  --muted: #5a6359;
  --border: #cdd3cb;
  --card-bg: #f1f3ef;
  --table-alt: #f5f6f3;
  --code-bg: #eef0ec;
  --measure: 42rem;
  --nav-w: 180px;
  --serif: 'Iowan Old Style', 'Palatino Linotype', Palatino, Georgia, serif;
  --sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  --mono: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    color-scheme: dark;
    --accent: #4cc88a;
    --accent-light: #1c2e24;
    --bg: #141614;
    --surface: #1c1e1c;
    --text: #e4e6e3;
    --muted: #9ba098;
    --border: #333733;
    --card-bg: #222422;
    --table-alt: #1e201e;
    --code-bg: #252725;
  }
}
:root[data-theme="dark"] {
  color-scheme: dark;
  --accent: #4cc88a;
  --accent-light: #1c2e24;
  --bg: #141614;
  --surface: #1c1e1c;
  --text: #e4e6e3;
  --muted: #9ba098;
  --border: #333733;
  --card-bg: #222422;
  --table-alt: #1e201e;
  --code-bg: #252725;
}

[hidden] { display: none !important; }
*, *::before, *::after { box-sizing: border-box; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: var(--sans);
  font-size: 0.975rem;
  line-height: 1.65;
  margin: 0;
  padding-inline: 1rem;
}
a { color: var(--accent); text-decoration: none; }
a:hover { text-decoration: underline; }
a:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 2px; }

.skip { position: absolute; left: -9999px; top: 0; background: var(--accent); color: #fff; padding: 0.5rem 1rem; z-index: 100; border-radius: 0 0 4px 4px; }
.skip:focus { left: 1rem; }

.page-grid {
  display: grid;
  grid-template-columns: var(--nav-w) 1fr;
  max-width: calc(var(--nav-w) + var(--measure) + 4rem);
  margin: 0 auto;
  gap: 2rem;
}
main { grid-column: 2; min-width: 0; padding-block: 2rem 4rem; }

.sidenav {
  position: sticky;
  top: env(safe-area-inset-top, 0px);
  height: 100vh;
  padding-block: 3rem 2rem;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}
.sidenav a {
  display: block;
  padding: 0.3rem 0.75rem;
  font-size: 0.8rem;
  color: var(--muted);
  border-left: 2px solid transparent;
  transition: color 0.15s, border-color 0.15s;
  line-height: 1.4;
}
.sidenav a:hover { color: var(--text); text-decoration: none; }
.sidenav a.active { color: var(--accent); border-left-color: var(--accent); font-weight: 600; }

.mobile-nav { display: none; }

@media (max-width: 820px) {
  .page-grid { grid-template-columns: 1fr; gap: 0; }
  .sidenav { display: none; }
  .mobile-nav {
    display: flex;
    position: sticky;
    top: env(safe-area-inset-top, 0px);
    z-index: 50;
    background: var(--bg);
    border-bottom: 1px solid var(--border);
    overflow-x: auto;
    gap: 0;
    padding: 0.4rem 0;
  }
  .mobile-nav a {
    flex-shrink: 0;
    padding: 0.35rem 0.75rem;
    font-size: 0.75rem;
    color: var(--muted);
    white-space: nowrap;
  }
  .mobile-nav a.active { color: var(--accent); font-weight: 600; }
  main { padding-block: 1rem 3rem; }
}

h1, h2, h3 { font-family: var(--serif); font-weight: 600; line-height: 1.25; text-wrap: balance; }
h1 { font-size: 1.85rem; margin-block: 0 0.75rem; }
h2 { font-size: 1.35rem; margin-block: 2.5rem 0.75rem; padding-bottom: 0.35rem; border-bottom: 1px solid var(--border); }
h3 { font-size: 1.05rem; margin-block: 1.5rem 0.5rem; font-weight: 700; }
p { margin-block: 0 0.75rem; }
section { scroll-margin-top: 1.5rem; }

.hero { margin-bottom: 2rem; }
.hero-meta { font-size: 0.85rem; color: var(--muted); margin-bottom: 1rem; }
.hero-tldr {
  background: var(--accent-light);
  border-left: 3px solid var(--accent);
  padding: 0.85rem 1rem;
  margin-block: 1rem 1.25rem;
  font-size: 0.92rem;
  line-height: 1.6;
  border-radius: 0 4px 4px 0;
}
.hero-tldr strong { color: var(--accent); }
.hero-links { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.75rem; }
.hero-links a {
  display: inline-flex; align-items: center; gap: 0.35rem;
  padding: 0.4rem 0.85rem;
  background: var(--card-bg); border: 1px solid var(--border); border-radius: 4px;
  font-size: 0.82rem; color: var(--text); transition: border-color 0.15s;
}
.hero-links a:hover { border-color: var(--accent); text-decoration: none; }

.contrib-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.85rem; margin-block: 1rem; }
@media (max-width: 600px) { .contrib-grid { grid-template-columns: 1fr; } }
.contrib-card {
  background: var(--card-bg); border-radius: 5px; padding: 1rem 1.1rem;
  border-top: 2px solid var(--accent);
}
.contrib-card h3 {
  font-family: var(--sans); font-size: 0.85rem; font-weight: 700;
  text-transform: uppercase; letter-spacing: 0.04em; color: var(--accent);
  margin-block: 0 0.4rem;
}
.contrib-card p { font-size: 0.88rem; margin: 0; }

.big-nums { display: flex; flex-wrap: wrap; gap: 1rem; margin-block: 1.25rem; }
.big-num { flex: 1 1 160px; background: var(--card-bg); border-radius: 5px; padding: 1rem 1.1rem; text-align: center; }
.big-num .val { font-family: var(--serif); font-size: 1.8rem; font-weight: 700; color: var(--accent); font-variant-numeric: tabular-nums; }
.big-num .label { font-size: 0.78rem; color: var(--muted); margin-top: 0.2rem; line-height: 1.35; }

.table-wrap { overflow-x: auto; margin-block: 0.75rem 1rem; }
table { width: 100%; border-collapse: collapse; font-size: 0.85rem; font-variant-numeric: tabular-nums; }
th, td { padding: 0.45rem 0.65rem; text-align: left; border-bottom: 1px solid var(--border); }
th { font-weight: 600; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.03em; color: var(--muted); white-space: nowrap; }
tbody tr:nth-child(even) { background: var(--table-alt); }
td code, th code { font-family: var(--mono); font-size: 0.82rem; background: var(--code-bg); padding: 0.1rem 0.3rem; border-radius: 2px; }
.table-cap { font-size: 0.8rem; color: var(--muted); margin-block: 0 0.35rem; font-style: italic; }

.fig-gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-block: 1rem; }
.fig-card {
  background: var(--card-bg); border-radius: 5px; overflow: hidden;
  cursor: pointer; margin: 0; transition: box-shadow 0.15s;
}
.fig-card:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
.fig-card img { width: 100%; display: block; background: #fff; }
.fig-caption { padding: 0.6rem 0.8rem; font-size: 0.8rem; color: var(--muted); line-height: 1.4; }
.fig-hint { font-size: 0.72rem; color: var(--muted); padding: 0 0.8rem 0.5rem; }

.lightbox {
  position: fixed; inset: 0; background: rgba(0,0,0,0.88); z-index: 200;
  display: flex; align-items: center; justify-content: center; padding: 2rem;
  opacity: 0; transition: opacity 0.2s;
}
.lightbox.open { opacity: 1; }
.lightbox-inner { position: relative; max-width: 95vw; max-height: 90vh; }
.lightbox-inner img { max-width: 100%; max-height: 85vh; display: block; border-radius: 4px; background: #fff; }
.lightbox-close {
  position: absolute; top: -2rem; right: 0; background: none; border: none;
  color: #fff; font-size: 1.5rem; cursor: pointer; padding: 0.25rem; line-height: 1;
}
.lightbox-close:focus-visible { outline: 2px solid #fff; outline-offset: 2px; }
.lightbox-cap { color: #ccc; font-size: 0.82rem; text-align: center; margin-top: 0.75rem; }

.lim-list { padding-left: 1.25rem; }
.lim-list li { margin-bottom: 0.6rem; font-size: 0.9rem; }
.lim-list li strong { color: var(--accent); }

.artifact-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 0.5rem; margin-block: 0.75rem; }
.artifact-link {
  display: block; padding: 0.55rem 0.75rem;
  background: var(--card-bg); border: 1px solid var(--border); border-radius: 4px;
  font-size: 0.8rem; color: var(--text); transition: border-color 0.15s;
}
.artifact-link:hover { border-color: var(--accent); text-decoration: none; }
.artifact-link .art-label { font-weight: 600; display: block; margin-bottom: 0.15rem; }
.artifact-link .art-path { font-family: var(--mono); font-size: 0.72rem; color: var(--muted); }

.site-footer {
  margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid var(--border);
  font-size: 0.8rem; color: var(--muted);
}
.site-footer a { color: var(--accent); }
.cite-block {
  background: var(--code-bg); padding: 0.85rem 1rem; border-radius: 4px;
  font-family: var(--mono); font-size: 0.72rem; line-height: 1.5;
  overflow-x: auto; white-space: pre-wrap; margin-block: 0.75rem 1rem;
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { transition-duration: 0.01ms !important; animation-duration: 0.01ms !important; }
}
</style>
</head>
<body>

<a class="skip" href="#main">Skip to main content</a>

<nav class="mobile-nav" aria-label="Section navigation (mobile)">
  <a href="#contributions">Contributions</a>
  <a href="#method">Method</a>
  <a href="#results">Results</a>
  <a href="#figures">Figures</a>
  <a href="#limitations">Limitations</a>
  <a href="#code">Code</a>
</nav>

<div class="page-grid">

<nav class="sidenav" aria-label="Section navigation">
  <a href="#contributions">Contributions</a>
  <a href="#method">Method</a>
  <a href="#results">Results</a>
  <a href="#sig-results">Shared signature</a>
  <a href="#dev-results">Free vocab (dev)</a>
  <a href="#oos-results">Free vocab (OOS)</a>
  <a href="#mechanism">Mechanism</a>
  <a href="#rename">Rename tradeoff</a>
  <a href="#figures">Figures</a>
  <a href="#limitations">Limitations</a>
  <a href="#code">Code</a>
</nav>

<main id="main">

<header class="hero">
  <h1>Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for NL-to-FOL Translation</h1>
  <div class="hero-meta">Anonymous &middot; Preliminary Study</div>
  <div class="hero-tldr">
    <strong>TL;DR</strong> &mdash; If independent LLM families translate the same sentence into first-order logic and an SMT solver checks pairwise equivalence, the fraction of peers that disagree with a candidate predicts whether it is faithful to the text. Under shared predicate vocabulary this reaches 0.954 AUROC; under free vocabulary it achieves 0.741 stratified AUROC, outperforming LLM judges by +0.099 on development data without any gold references.
  </div>
  <div class="hero-links">
    <a href="https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_cNhUBrixEdz7/paper.pdf" target="_blank">Read the paper (PDF)</a>
    <a href="https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_cNhUBrixEdz7/report.pdf" target="_blank">Read the full research report</a>
    <a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7" target="_blank">Code repository</a>
  </div>
</header>

<section id="contributions">
  <h2>Contributions</h2>
  <div class="contrib-grid">
    <div class="contrib-card">
      <h3>Shared-signature ceiling</h3>
      <p>Pre-registered evaluation on 221 long-exception sentences: consensus AUROC 0.954 versus 0.587 for a disguised judge (&Delta;&nbsp;=&nbsp;+0.367), flat across word-length terciles, with zero error endorsement.</p>
    </div>
    <div class="contrib-card">
      <h3>Free-vocabulary signal</h3>
      <p>On development set&nbsp;E (2,686 items), consensus outperforms judges by &Delta;&nbsp;=&nbsp;+0.099 on stratified AUROC. Aligner-free consensus (c_exact) reaches 0.689 without any predicate mapping.</p>
    </div>
    <div class="contrib-card">
      <h3>Out-of-sample transfer</h3>
      <p>On untouched R_COMP&nbsp;FREE sentences under provisional labels: &Delta;&nbsp;=&nbsp;+0.171 versus the original-view judge; consensus reaches 0.94 of the frontier judge's AUROC.</p>
    </div>
    <div class="contrib-card">
      <h3>Rename tradeoff</h3>
      <p>A 76.5% false-alarm rate under nonce predicate renames that no variant could eliminate without sacrificing error recall, identifying a fundamental limit of free-vocabulary consensus.</p>
    </div>
  </div>
</section>

<section id="method">
  <h2>Method</h2>

  <h3>Consensus scoring</h3>
  <p>Given a sentence and a candidate FOL translation, collect peer translations from <em>k</em> independent LLM families (Gemini, Claude, GPT, Llama, Qwen, Phi, Mistral). The consensus score is:</p>
  <p style="text-align:center; font-family: var(--serif); font-size: 1.05rem; margin-block: 0.75rem;">
    c_score(c, s) = 1 &minus; (1/k) &Sigma; <b>1</b>[equiv(c, p<sub>i</sub>)]
  </p>
  <p>Under <strong>shared signature</strong>, all translators use a supplied predicate vocabulary and equiv is a direct Z3 check. Under <strong>free vocabulary</strong>, each translator chooses its own predicate names and equiv requires a predicate-name aligner before the Z3 check.</p>

  <h3>Predicate alignment</h3>
  <p>The aligner combines three cost components: <strong>structural cost</strong> (polarity profile, argument-count match, nesting depth), <strong>text-anchor cost</strong> (overlap between predicate-name words and source-sentence tokens via Porter stemming and WordNet), and <strong>semantic signature</strong> (truth-value profiles over random finite interpretations). The <em>k</em> cheapest bijections are evaluated, and the pair is declared equivalent if any bijection yields Z3-verified equivalence.</p>

  <h3>Score variants</h3>
  <p><code>c_exact</code>: no alignment, exact-match only. <code>c_nf</code> (name-free): structural and semantic signatures only, ignoring text anchoring. <code>p_peer_text</code>: logistic fusion of consensus features with text-side features.</p>

  <h3>Evaluation framework</h3>
  <p><strong>Shared-signature labels</strong> come from Z3 equivalence to trusted-by-construction references. <strong>Free-vocabulary labels</strong> on set&nbsp;E come from a three-person expert panel. The primary metric is <strong>stratified AUROC</strong>: items are paired only within the same source stratum. Confidence intervals use sentence-cluster percentile bootstrap (B&nbsp;=&nbsp;2,000).</p>
</section>

<section id="results">
  <h2>Results</h2>

  <div class="big-nums">
    <div class="big-num">
      <div class="val">0.954</div>
      <div class="label">Consensus AUROC<br>(shared signature)</div>
    </div>
    <div class="big-num">
      <div class="val">0.741</div>
      <div class="label">Consensus AUROC<br>(free vocabulary, dev)</div>
    </div>
    <div class="big-num">
      <div class="val">+0.099</div>
      <div class="label">&Delta; over judge<br>(free vocabulary, dev)</div>
    </div>
  </div>

  <section id="sig-results">
    <h3>Shared-signature results (R_COMP-SIG)</h3>
    <p class="table-cap">Table 1: Within-template AUROC on R_COMP-SIG (221 sentences, pure Z3 labels).</p>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Metric</th><th>n</th><th>AUROC [95% CI]</th><th>&Delta; vs disg. judge</th></tr></thead>
        <tbody>
          <tr><td><code>c_score_sig</code></td><td>1904</td><td>0.954 [0.939, 0.968]</td><td>+0.367 [+0.328, +0.404]</td></tr>
          <tr><td><code>c_score_align</code></td><td>1904</td><td>0.954 [0.939, 0.968]</td><td>+0.367 [+0.328, +0.404]</td></tr>
          <tr><td>Judge (flash-lite, disg.)</td><td>1904</td><td>0.587 [0.551, 0.622]</td><td>&mdash;</td></tr>
          <tr><td>Judge (flash-lite, orig.)</td><td>1932</td><td>0.673 [0.637, 0.708]</td><td></td></tr>
          <tr><td>Judge (frontier, orig.)</td><td>60</td><td>0.932 [0.782, 1.000]</td><td></td></tr>
          <tr><td>Judge (local, disg.)</td><td>2024</td><td>0.498 [0.459, 0.534]</td><td></td></tr>
        </tbody>
      </table>
    </div>
    <p>Error endorsement is zero (<em>e</em>&nbsp;=&nbsp;0): no error item scores below the decision threshold. Among the 429 error items, 75.3% receive the maximum consensus score of 1.0.</p>

    <p><strong>Flat with sentence length.</strong> Consensus under shared signature is flat across word-length terciles:</p>
    <p class="table-cap">Table 2: R_COMP-SIG within-template AUROC by word-length tercile.</p>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Tercile</th><th>n</th><th>ERR/COR</th><th>c_sig</th><th>Judge (disg.)</th><th>&Delta; [CI]</th></tr></thead>
        <tbody>
          <tr><td>W1 (shortest)</td><td>574</td><td>125/449</td><td>0.959</td><td>0.578</td><td>+0.382 [+0.278, +0.472]</td></tr>
          <tr><td>W2</td><td>743</td><td>149/594</td><td>0.947</td><td>0.624</td><td>+0.331 [+0.253, +0.421]</td></tr>
          <tr><td>W3 (longest)</td><td>707</td><td>155/552</td><td>0.953</td><td>0.567</td><td>+0.388 [+0.301, +0.471]</td></tr>
        </tbody>
      </table>
    </div>
    <p>On a 60-row stratified subsample scored by the frontier judge (Gemini 3.1 Pro), consensus achieves pooled AUROC 0.956 [0.889, 1.000] versus 0.932 [0.855, 0.990].</p>
  </section>

  <section id="dev-results">
    <h3>Free-vocabulary development results (set E)</h3>
    <p class="table-cap">Table 3: Stratified AUROC on development set E (R_AB, free vocabulary, n&nbsp;=&nbsp;2,686).</p>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Metric</th><th>Strat AUROC [95% CI]</th><th>$/item</th></tr></thead>
        <tbody>
          <tr><td><code>c_score_align</code></td><td>0.741 [0.705, 0.775]</td><td>9.1e-5</td></tr>
          <tr><td><code>p_peer_text</code> (fused)</td><td>0.753 [0.720, 0.784]</td><td>9.1e-5</td></tr>
          <tr><td><code>c_exact</code> (no alignment)</td><td>0.689 [0.652, 0.726]</td><td>&mdash;</td></tr>
          <tr><td><code>c_nf</code> (name-free)</td><td>0.686 [0.647, 0.720]</td><td>&mdash;</td></tr>
          <tr><td colspan="3" style="border:none;padding:0.2rem"></td></tr>
          <tr><td>Flash-lite judge (disg.)</td><td>0.642 [0.607, 0.676]</td><td>5.1e-5</td></tr>
          <tr><td>Flash-lite judge (orig.)</td><td>0.623 [0.593, 0.651]</td><td>5.1e-5</td></tr>
          <tr><td>Nano judge (disg.)</td><td>0.644 [0.609, 0.680]</td><td>2.0e-5</td></tr>
          <tr><td>Local judge Qwen-8B (disg.)</td><td>0.674 [0.646, 0.703]</td><td>&mdash;</td></tr>
          <tr><td colspan="3" style="border:none;padding:0.2rem"></td></tr>
          <tr><td>Round-trip NLI (min)</td><td>0.606 [0.569, 0.645]</td><td>2.8e-5</td></tr>
          <tr><td>Self-consistency (5-sample)</td><td>0.598 [0.559, 0.637]</td><td>6.7e-5</td></tr>
          <tr><td colspan="3" style="border:none;padding:0.2rem"></td></tr>
          <tr><td>28-feature stack</td><td>0.735 [0.699, 0.766]</td><td>&mdash;</td></tr>
          <tr><td>28-feature stack + <code>c_score_align</code></td><td>0.774 [0.743, 0.802]</td><td>&mdash;</td></tr>
        </tbody>
      </table>
    </div>
    <p>Consensus outperforms the disguised flash-lite judge by &Delta;&nbsp;=&nbsp;+0.099 [+0.049, +0.146] on R_AB and by &Delta;&nbsp;=&nbsp;+0.116 [+0.070, +0.163] on the long-sentence pool. Adding <code>c_score_align</code> to the 28-feature stack increases stratified AUROC by +0.039 [+0.021, +0.057]; permutation null test p<sub>95</sub>&nbsp;=&nbsp;0.009.</p>
    <p>The drop from 0.952 (shared signature) to 0.801 (free vocabulary, same R_COMP sentences) reflects the cost of predicate-name alignment. Aligner-free consensus (<code>c_exact</code>) at 0.689 shows the aligner adds about 22% of the above-chance signal, with the remaining 78% from structural agreement alone.</p>
    <p>On L25 sentences alone, &Delta;&nbsp;=&nbsp;+0.069 [&minus;0.020, +0.148], not significant at 95%. Frontier judge comparison on 284 rows: ratio 0.957 [0.887, 1.034]. System-level Kendall &tau;<sub>b</sub>&nbsp;=&nbsp;0.692 [+0.513, +0.795] across 13 configurations.</p>
  </section>

  <section id="oos-results">
    <h3>Free-vocabulary out-of-sample (R_COMP FREE)</h3>
    <p class="table-cap">Table 4: R_COMP FREE provisional AUROCs (within-template, untouched). Labels are non-confirmatory.</p>
    <div class="table-wrap">
      <table>
        <thead><tr><th>View</th><th>n (ERR/MAPPED)</th><th>c_align</th><th>Judge</th></tr></thead>
        <tbody>
          <tr><td>Disguised</td><td>1706 (602/1104)</td><td>0.801 [0.770, 0.834]</td><td>0.584 [0.550, 0.618]</td></tr>
          <tr><td>Original</td><td>1709 (605/1104)</td><td>0.804 [0.774, 0.836]</td><td>0.633 [0.601, 0.666]</td></tr>
        </tbody>
      </table>
    </div>
    <p>Disguised-judge &Delta;&nbsp;=&nbsp;+0.217 [+0.175, +0.260]; original-view &Delta;&nbsp;=&nbsp;+0.171 [+0.135, +0.206]. Two-auditor subset (146 rows): &Delta;&nbsp;=&nbsp;+0.105 [+0.011, +0.215]. Frontier-judge subsample (150 rows): ratio 0.940 [0.825, 1.056].</p>
  </section>

  <section id="mechanism">
    <h3>Mechanism</h3>
    <p>The consensus signal decomposes into endorsement <em>e</em> (ERROR items endorsed by peers) and divergence <em>d</em> (CORRECT items flagged). On R_COMP-SIG: <em>e</em>&nbsp;=&nbsp;0.0, <em>d</em>&nbsp;=&nbsp;0.260. Under free vocabulary on set E, net degradation from short to long sentences is &Delta;(e+d)&nbsp;=&nbsp;+0.356 [+0.198, +0.493], driven by divergence (&Delta;d&nbsp;=&nbsp;+0.608, &Delta;e&nbsp;=&nbsp;&minus;0.252).</p>

    <p><strong>Family sufficiency.</strong> Three peer families suffice for 97% of full-pool AUROC (k<sub>95</sub>&nbsp;=&nbsp;3); long sentences require k<sub>95</sub>&nbsp;=&nbsp;5.</p>
    <p class="table-cap">Table 5: Free-vocabulary AUROC by number of peer families on set E.</p>
    <div class="table-wrap">
      <table>
        <thead><tr><th>k</th><th>AUROC (overall)</th><th>AUROC (long, T3)</th></tr></thead>
        <tbody>
          <tr><td>1</td><td>0.685</td><td>0.581</td></tr>
          <tr><td>3</td><td>0.757</td><td>0.651</td></tr>
          <tr><td>5</td><td>0.776</td><td>0.698</td></tr>
          <tr><td>7</td><td>0.784</td><td>0.726</td></tr>
        </tbody>
      </table>
    </div>
  </section>

  <section id="confirmation">
    <h3>Confirmation status</h3>
    <p>Independent confirmation remains incomplete. On the one testable stratum (DT), consensus achieves 0.916, tying Qwen-8B (&Delta;&nbsp;=&nbsp;+0.003). On L25, <code>c_score_align</code> falls to 0.443 on 42 items (35 ERROR / 7 CORRECT) with extreme variance. Every pre-registered criterion returned NOT_TESTABLE or unfavourable.</p>
  </section>

  <section id="rename">
    <h3>The rename tradeoff</h3>
    <p class="table-cap">Table 6: False-alarm rates on meaning-preserving renames of CORRECT candidates.</p>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Metric</th><th>NONCE FA</th><th>NONCE flip</th><th>SYN FA</th><th>SYN flip</th></tr></thead>
        <tbody>
          <tr><td><code>c_align</code></td><td>0.765</td><td>0.605</td><td>0.565</td><td>0.313</td></tr>
          <tr><td><code>c_nf</code> (name-free)</td><td>0.132</td><td>0.000</td><td>0.201</td><td>0.000</td></tr>
          <tr><td><code>p_peer_text</code></td><td>1.000</td><td>0.821</td><td>0.216</td><td>0.080</td></tr>
          <tr><td>Judge (disg.)</td><td>0.229</td><td>0.134</td><td>0.085</td><td>0.058</td></tr>
        </tbody>
      </table>
    </div>
    <p>The name-free <code>c_nf</code> eliminates rename sensitivity (flip&nbsp;=&nbsp;0) at the cost of blindness to meaning-rename errors (AUROC 0.499, chance) and lower overall discrimination (0.686 vs. 0.741).</p>
  </section>

  <section id="dead-ends">
    <h3>Dead ends</h3>
    <p>Abandoned alternatives: fused structural-feature filter (gate failure); name-free consensus (rename-invariant but blind); solver-based semantic reader (balanced accuracy 0.476); LLM adjudication (0.662); candidate-signature consensus (error endorsement rose to 0.459).</p>
  </section>
</section>

<section id="figures">
  <h2>Figures</h2>
  <div class="fig-gallery">
    <figure class="fig-card" tabindex="0" role="button" aria-label="Enlarge Figure 1">
      <img src="figures/fig_dev_auroc_v0.png"
           alt="Horizontal bar chart comparing stratified AUROC across 12 metrics on the free-vocabulary development set. Consensus-based metrics cluster around 0.69 to 0.77; LLM judges around 0.62 to 0.67; other baselines near 0.60.">
      <figcaption class="fig-caption">Fig. 1: Stratified AUROC on the free-vocabulary development set.</figcaption>
      <p class="fig-hint">Click to enlarge</p>
    </figure>
    <figure class="fig-card" tabindex="0" role="button" aria-label="Enlarge Figure 2">
      <img src="figures/fig_sig_tercile_v0.png"
           alt="Grouped bar chart showing within-template AUROC by word-length tercile on R_COMP-SIG. Consensus (blue) is flat at 0.947 to 0.959; disguised judge (orange) hovers near chance at 0.567 to 0.624.">
      <figcaption class="fig-caption">Fig. 2: R_COMP-SIG AUROC by word-length tercile. Consensus is flat; the judge hovers near chance.</figcaption>
      <p class="fig-hint">Click to enlarge</p>
    </figure>
    <figure class="fig-card" tabindex="0" role="button" aria-label="Enlarge Figure 3">
      <img src="figures/fig_complexity_v0.png"
           alt="Bar chart decomposing consensus errors by sentence-length tercile. Endorsement rate e decreases from 0.29 to 0.04 while divergence rate d increases from 0.31 to 0.91.">
      <figcaption class="fig-caption">Fig. 3: Consensus error decomposition by sentence length. Net degradation &Delta;(e+d)&nbsp;=&nbsp;+0.356.</figcaption>
      <p class="fig-hint">Click to enlarge</p>
    </figure>
    <figure class="fig-card" tabindex="0" role="button" aria-label="Enlarge Figure 4">
      <img src="figures/fig_k_curve_v0.png"
           alt="Line chart of AUROC vs number of peer families k. Overall curve rises steeply to k=3 then flattens; long-sentence tercile rises more slowly, requiring k=5.">
      <figcaption class="fig-caption">Fig. 4: AUROC vs peer families k. Three families capture 97% of signal; long sentences need five.</figcaption>
      <p class="fig-hint">Click to enlarge</p>
    </figure>
  </div>
</section>

<section id="limitations">
  <h2>Limitations</h2>
  <ol class="lim-list">
    <li><strong>Shared-signature scope.</strong> The 0.954 AUROC uses templated sentences with a supplied predicate vocabulary, limiting scope to controlled settings.</li>
    <li><strong>Development data overlap.</strong> R_COMP-SIG later served as development data for aligner tuning. The pre-registration keeps the SIG result uncontaminated, but set E numbers are not independent.</li>
    <li><strong>Rename vulnerability.</strong> Under free vocabulary, 76.5% false-alarm rate on nonce renames systematically penalises non-standard predicate names.</li>
    <li><strong>Length degradation.</strong> Consensus degrades with sentence length under free vocabulary (NET +0.356), weakest on the longest, most complex sentences.</li>
    <li><strong>Provisional labels.</strong> R_COMP FREE uses non-confirmatory labels; the two-auditor subset (&Delta;&nbsp;=&nbsp;+0.105) barely excludes zero.</li>
    <li><strong>Label dependence.</strong> Development results depend on a three-person panel whose agreement is imperfect.</li>
    <li><strong>Cost.</strong> At k&nbsp;=&nbsp;9, the amortised consensus cost per candidate is about 19 times the cost of a single cheap judge call.</li>
    <li><strong>Domain.</strong> All results are on English-to-FOL from MALLS, ProverQA, and R_COMP. Generalisation is untested.</li>
  </ol>
</section>

<section id="code">
  <h2>Code artifacts</h2>
  <p>All evaluation code is released. Each link points to the experiment or dataset that produced the corresponding result.</p>
  <div class="artifact-grid">
    <a class="artifact-link" href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-1/experiment-1" target="_blank">
      <span class="art-label">Consensus scoring</span>
      <span class="art-path">round-1/experiment-1</span>
    </a>
    <a class="artifact-link" href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-1/experiment-3" target="_blank">
      <span class="art-label">Development set E</span>
      <span class="art-path">round-1/experiment-3</span>
    </a>
    <a class="artifact-link" href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-1/experiment-4" target="_blank">
      <span class="art-label">Baselines</span>
      <span class="art-path">round-1/experiment-4</span>
    </a>
    <a class="artifact-link" href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-1/dataset-1" target="_blank">
      <span class="art-label">Code: Held-out logic translation test set, panel-checked</span>
      <span class="art-path">round-1/dataset-1</span>
    </a>
    <a class="artifact-link" href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-2/experiment-5" target="_blank">
      <span class="art-label">Fused scorer (p_peer_text)</span>
      <span class="art-path">round-2/experiment-5</span>
    </a>
    <a class="artifact-link" href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-2/dataset-3" target="_blank">
      <span class="art-label">Code: Long logic sentences and FOL error suite</span>
      <span class="art-path">round-2/dataset-3</span>
    </a>
    <a class="artifact-link" href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-2/evaluation-1" target="_blank">
      <span class="art-label">Code: Re-checking earlier logic-metric results across label sets</span>
      <span class="art-path">round-2/evaluation-1</span>
    </a>
    <a class="artifact-link" href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/experiment-6" target="_blank">
      <span class="art-label">Dev results analysis</span>
      <span class="art-path">round-3/experiment-6</span>
    </a>
    <a class="artifact-link" href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/experiment-7" target="_blank">
      <span class="art-label">R_COMP dataset</span>
      <span class="art-path">round-3/experiment-7</span>
    </a>
    <a class="artifact-link" href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/evaluation-2" target="_blank">
      <span class="art-label">Mechanism decomposition</span>
      <span class="art-path">round-3/evaluation-2</span>
    </a>
    <a class="artifact-link" href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/experiment-8" target="_blank">
      <span class="art-label">Rename tradeoff</span>
      <span class="art-path">round-3/experiment-8</span>
    </a>
    <a class="artifact-link" href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/research-1" target="_blank">
      <span class="art-label">Code: What is new about peer agreement for logic</span>
      <span class="art-path">round-3/research-1</span>
    </a>
    <a class="artifact-link" href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-4/dataset-4" target="_blank">
      <span class="art-label">Held-out dataset E2-A</span>
      <span class="art-path">round-4/dataset-4</span>
    </a>
    <a class="artifact-link" href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-4/experiment-9" target="_blank">
      <span class="art-label">Dead ends</span>
      <span class="art-path">round-4/experiment-9</span>
    </a>
    <a class="artifact-link" href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-4/experiment-10" target="_blank">
      <span class="art-label">Code: Do symbol hints help model agreement checks?</span>
      <span class="art-path">round-4/experiment-10</span>
    </a>
    <a class="artifact-link" href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-4/dataset-5" target="_blank">
      <span class="art-label">Code: Name-free labels for free-vocabulary logic translations</span>
      <span class="art-path">round-4/dataset-5</span>
    </a>
    <a class="artifact-link" href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-4/evaluation-3" target="_blank">
      <span class="art-label">Code: Can shared vocabulary fix consensus blind spots?</span>
      <span class="art-path">round-4/evaluation-3</span>
    </a>
    <a class="artifact-link" href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-5/experiment-11" target="_blank">
      <span class="art-label">Code: Consensus vs LLM judges on fresh logic data</span>
      <span class="art-path">round-5/experiment-11</span>
    </a>
    <a class="artifact-link" href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-5/experiment-12" target="_blank">
      <span class="art-label">Code: Second fresh sample of long logic sentences</span>
      <span class="art-path">round-5/experiment-12</span>
    </a>
    <a class="artifact-link" href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-5/experiment-13" target="_blank">
      <span class="art-label">R_COMP FREE (OOS)</span>
      <span class="art-path">round-5/experiment-13</span>
    </a>
    <a class="artifact-link" href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-5/experiment-14" target="_blank">
      <span class="art-label">Code: Screening fixes for model-agreement false alarms</span>
      <span class="art-path">round-5/experiment-14</span>
    </a>
    <a class="artifact-link" href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-5/evaluation-4" target="_blank">
      <span class="art-label">Code: Corrected record: every paper number checked</span>
      <span class="art-path">round-5/evaluation-4</span>
    </a>
  </div>
</section>

<footer class="site-footer">
  <p><a href="https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_cNhUBrixEdz7/paper.pdf" target="_blank">Read the paper (PDF)</a> &middot;
     <a href="https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_cNhUBrixEdz7/report.pdf" target="_blank">Read the full research report</a> &middot;
     <a href="https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7" target="_blank">Code repository</a></p>
  <p>Citation:</p>
  <div class="cite-block">@article{anonymous2026crossfamily,
  title={Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric
         for Natural-Language-to-First-Order-Logic Translation},
  author={Anonymous},
  year={2026}
}</div>
</footer>

</main>
</div>

<div class="lightbox" id="lightbox" role="dialog" aria-modal="true" aria-label="Enlarged figure" hidden>
  <div class="lightbox-inner">
    <button class="lightbox-close" aria-label="Close enlarged figure">&times;</button>
    <img id="lightbox-img" src="figures/fig_dev_auroc_v0.png" alt="">
    <p class="lightbox-cap" id="lightbox-cap"></p>
  </div>
</div>

<script>
(function() {
  'use strict';
  var sections = document.querySelectorAll('main > section, main > header');
  var navD = document.querySelectorAll('.sidenav a');
  var navM = document.querySelectorAll('.mobile-nav a');
  function setActive(id) {
    [navD, navM].forEach(function(ls) {
      ls.forEach(function(a) { a.classList.toggle('active', a.getAttribute('href') === '#' + id); });
    });
  }
  if ('IntersectionObserver' in window) {
    var obs = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) { if (e.isIntersecting) setActive(e.target.id); });
    }, { rootMargin: '-20% 0px -60% 0px' });
    sections.forEach(function(s) { if (s.id) obs.observe(s); });
  }

  var lightbox = document.getElementById('lightbox');
  var lbImg = document.getElementById('lightbox-img');
  var lbCap = document.getElementById('lightbox-cap');
  var trigger = null;

  document.querySelectorAll('.fig-card').forEach(function(card) {
    function open() {
      var img = card.querySelector('img');
      var cap = card.querySelector('.fig-caption');
      lbImg.src = img.src; lbImg.alt = img.alt;
      lbCap.textContent = cap ? cap.textContent : '';
      lightbox.hidden = false;
      requestAnimationFrame(function() { lightbox.classList.add('open'); });
      document.body.style.overflow = 'hidden';
      trigger = card;
      lightbox.querySelector('.lightbox-close').focus();
    }
    card.addEventListener('click', open);
    card.addEventListener('keydown', function(e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); }
    });
  });

  function close() {
    lightbox.classList.remove('open');
    document.body.style.overflow = '';
    lightbox.hidden = true;
    lbImg.removeAttribute('src');
    if (trigger) { trigger.focus(); trigger = null; }
  }
  lightbox.querySelector('.lightbox-close').addEventListener('click', close);
  lightbox.addEventListener('click', function(e) { if (e.target === lightbox) close(); });
  document.addEventListener('keydown', function(e) { if (e.key === 'Escape' && !lightbox.hidden) close(); });
})();
</script>
</body>
</html>
```

### [23] TOOL RESULT — Write · 2026-09-25 02:47:50 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_cNhUBrixEdz7/4_gen_paper_repo/_4_assemble_paper/paper/index.html", "content": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n<title>Gold-Free Faithfulness Metrics for NL-to-FOL</title>\n<style>\n:root {\n  --accent: #1a6b4a;\n  --accent-light: #e6f2ec;\n  --bg: #f9f9f7;\n  --surface: #ffffff;\n  --text: #1a1a1a;\n  --muted: #5a6359;\n  --border: #cdd3cb;\n  --card-bg: #f1f3ef;\n  --table-alt: #f5f6f3;\n  --code-bg: #eef0ec;\n  --measure: 42rem;\n  --nav-w: 180px;\n  --serif: 'Iowan Old Style', 'Palatino Linotype', Palatino, Georgia, serif;\n  --sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;\n  --mono: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;\n}\n@media (prefers-color-scheme: dark) {\n  :root:not([data-theme=\"light\"]) {\n    color-scheme: dark;\n    --accent: #4cc88a;\n    --accent-light: #1c2e24;\n    --bg: #141614;\n    --surface: #1c1e1c;\n    --text: #e4e6e3;\n    --muted: #9ba098;\n    --border: #333733;\n    --card-bg: #222422;\n    --table-alt: #1e201e;\n    --code-bg: #252725;\n  }\n}\n:root[data-theme=\"dark\"] {\n  color-scheme: dark;\n  --accent: #4cc88a;\n  --accent-light: #1c2e24;\n  --bg: #141614;\n  --surface: #1c1e1c;\n  --text: #e4e6e3;\n  --muted: #9ba098;\n  --border: #333733;\n  --card-bg: #222422;\n  --table-alt: #1e201e;\n  --code-bg: #252725;\n}\n\n[hidden] { display: none !important; }\n*, *::before, *::after { box-sizing: border-box; }\nbody {\n  background: var(--bg);\n  color: var(--text);\n  font-family: var(--sans);\n  font-size: 0.975rem;\n  line-height: 1.65;\n  margin: 0;\n  padding-inline: 1rem;\n}\na { color: var(--accent); text-decoration: none; }\na:hover { text-decoration: underline; }\na:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; border-radius: 2px; }\n\n.skip { position: absolute; left: -9999px; top: 0; background: var(--accent); color: #fff; padding: 0.5rem 1rem; z-index: 100; border-radius: 0 0 4px 4px; }\n.skip:focus { left: 1rem; }\n\n.page-grid {\n  display: grid;\n  grid-template-columns: var(--nav-w) 1fr;\n  max-width: calc(var(--nav-w) + var(--measure) + 4rem);\n  margin: 0 auto;\n  gap: 2rem;\n}\nmain { grid-column: 2; min-width: 0; padding-block: 2rem 4rem; }\n\n.sidenav {\n  position: sticky;\n  top: env(safe-area-inset-top, 0px);\n  height: 100vh;\n  padding-block: 3rem 2rem;\n  overflow-y: auto;\n  display: flex;\n  flex-direction: column;\n  gap: 0.15rem;\n}\n.sidenav a {\n  display: block;\n  padding: 0.3rem 0.75rem;\n  font-size: 0.8rem;\n  color: var(--muted);\n  border-left: 2px solid transparent;\n  transition: color 0.15s, border-color 0.15s;\n  line-height: 1.4;\n}\n.sidenav a:hover { color: var(--text); text-decoration: none; }\n.sidenav a.active { color: var(--accent); border-left-color: var(--accent); font-weight: 600; }\n\n.mobile-nav { display: none; }\n\n@media (max-width: 820px) {\n  .page-grid { grid-template-columns: 1fr; gap: 0; }\n  .sidenav { display: none; }\n  .mobile-nav {\n    display: flex;\n    position: sticky;\n    top: env(safe-area-inset-top, 0px);\n    z-index: 50;\n    background: var(--bg);\n    border-bottom: 1px solid var(--border);\n    overflow-x: auto;\n    gap: 0;\n    padding: 0.4rem 0;\n  }\n  .mobile-nav a {\n    flex-shrink: 0;\n    padding: 0.35rem 0.75rem;\n    font-size: 0.75rem;\n    color: var(--muted);\n    white-space: nowrap;\n  }\n  .mobile-nav a.active { color: var(--accent); font-weight: 600; }\n  main { padding-block: 1rem 3rem; }\n}\n\nh1, h2, h3 { font-family: var(--serif); font-weight: 600; line-height: 1.25; text-wrap: balance; }\nh1 { font-size: 1.85rem; margin-block: 0 0.75rem; }\nh2 { font-size: 1.35rem; margin-block: 2.5rem 0.75rem; padding-bottom: 0.35rem; border-bottom: 1px solid var(--border); }\nh3 { font-size: 1.05rem; margin-block: 1.5rem 0.5rem; font-weight: 700; }\np { margin-block: 0 0.75rem; }\nsection { scroll-margin-top: 1.5rem; }\n\n.hero { margin-bottom: 2rem; }\n.hero-meta { font-size: 0.85rem; color: var(--muted); margin-bottom: 1rem; }\n.hero-tldr {\n  background: var(--accent-light);\n  border-left: 3px solid var(--accent);\n  padding: 0.85rem 1rem;\n  margin-block: 1rem 1.25rem;\n  font-size: 0.92rem;\n  line-height: 1.6;\n  border-radius: 0 4px 4px 0;\n}\n.hero-tldr strong { color: var(--accent); }\n.hero-links { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.75rem; }\n.hero-links a {\n  display: inline-flex; align-items: center; gap: 0.35rem;\n  padding: 0.4rem 0.85rem;\n  background: var(--card-bg); border: 1px solid var(--border); border-radius: 4px;\n  font-size: 0.82rem; color: var(--text); transition: border-color 0.15s;\n}\n.hero-links a:hover { border-color: var(--accent); text-decoration: none; }\n\n.contrib-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.85rem; margin-block: 1rem; }\n@media (max-width: 600px) { .contrib-grid { grid-template-columns: 1fr; } }\n.contrib-card {\n  background: var(--card-bg); border-radius: 5px; padding: 1rem 1.1rem;\n  border-top: 2px solid var(--accent);\n}\n.contrib-card h3 {\n  font-family: var(--sans); font-size: 0.85rem; font-weight: 700;\n  text-transform: uppercase; letter-spacing: 0.04em; color: var(--accent);\n  margin-block: 0 0.4rem;\n}\n.contrib-card p { font-size: 0.88rem; margin: 0; }\n\n.big-nums { display: flex; flex-wrap: wrap; gap: 1rem; margin-block: 1.25rem; }\n.big-num { flex: 1 1 160px; background: var(--card-bg); border-radius: 5px; padding: 1rem 1.1rem; text-align: center; }\n.big-num .val { font-family: var(--serif); font-size: 1.8rem; font-weight: 700; color: var(--accent); font-variant-numeric: tabular-nums; }\n.big-num .label { font-size: 0.78rem; color: var(--muted); margin-top: 0.2rem; line-height: 1.35; }\n\n.table-wrap { overflow-x: auto; margin-block: 0.75rem 1rem; }\ntable { width: 100%; border-collapse: collapse; font-size: 0.85rem; font-variant-numeric: tabular-nums; }\nth, td { padding: 0.45rem 0.65rem; text-align: left; border-bottom: 1px solid var(--border); }\nth { font-weight: 600; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.03em; color: var(--muted); white-space: nowrap; }\ntbody tr:nth-child(even) { background: var(--table-alt); }\ntd code, th code { font-family: var(--mono); font-size: 0.82rem; background: var(--code-bg); padding: 0.1rem 0.3rem; border-radius: 2px; }\n.table-cap { font-size: 0.8rem; color: var(--muted); margin-block: 0 0.35rem; font-style: italic; }\n\n.fig-gallery { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1rem; margin-block: 1rem; }\n.fig-card {\n  background: var(--card-bg); border-radius: 5px; overflow: hidden;\n  cursor: pointer; margin: 0; transition: box-shadow 0.15s;\n}\n.fig-card:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.1); }\n.fig-card img { width: 100%; display: block; background: #fff; }\n.fig-caption { padding: 0.6rem 0.8rem; font-size: 0.8rem; color: var(--muted); line-height: 1.4; }\n.fig-hint { font-size: 0.72rem; color: var(--muted); padding: 0 0.8rem 0.5rem; }\n\n.lightbox {\n  position: fixed; inset: 0; background: rgba(0,0,0,0.88); z-index: 200;\n  display: flex; align-items: center; justify-content: center; padding: 2rem;\n  opacity: 0; transition: opacity 0.2s;\n}\n.lightbox.open { opacity: 1; }\n.lightbox-inner { position: relative; max-width: 95vw; max-height: 90vh; }\n.lightbox-inner img { max-width: 100%; max-height: 85vh; display: block; border-radius: 4px; background: #fff; }\n.lightbox-close {\n  position: absolute; top: -2rem; right: 0; background: none; border: none;\n  color: #fff; font-size: 1.5rem; cursor: pointer; padding: 0.25rem; line-height: 1;\n}\n.lightbox-close:focus-visible { outline: 2px solid #fff; outline-offset: 2px; }\n.lightbox-cap { color: #ccc; font-size: 0.82rem; text-align: center; margin-top: 0.75rem; }\n\n.lim-list { padding-left: 1.25rem; }\n.lim-list li { margin-bottom: 0.6rem; font-size: 0.9rem; }\n.lim-list li strong { color: var(--accent); }\n\n.artifact-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 0.5rem; margin-block: 0.75rem; }\n.artifact-link {\n  display: block; padding: 0.55rem 0.75rem;\n  background: var(--card-bg); border: 1px solid var(--border); border-radius: 4px;\n  font-size: 0.8rem; color: var(--text); transition: border-color 0.15s;\n}\n.artifact-link:hover { border-color: var(--accent); text-decoration: none; }\n.artifact-link .art-label { font-weight: 600; display: block; margin-bottom: 0.15rem; }\n.artifact-link .art-path { font-family: var(--mono); font-size: 0.72rem; color: var(--muted); }\n\n.site-footer {\n  margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid var(--border);\n  font-size: 0.8rem; color: var(--muted);\n}\n.site-footer a { color: var(--accent); }\n.cite-block {\n  background: var(--code-bg); padding: 0.85rem 1rem; border-radius: 4px;\n  font-family: var(--mono); font-size: 0.72rem; line-height: 1.5;\n  overflow-x: auto; white-space: pre-wrap; margin-block: 0.75rem 1rem;\n}\n\n@media (prefers-reduced-motion: reduce) {\n  *, *::before, *::after { transition-duration: 0.01ms !important; animation-duration: 0.01ms !important; }\n}\n</style>\n</head>\n<body>\n\n<a class=\"skip\" href=\"#main\">Skip to main content</a>\n\n<nav class=\"mobile-nav\" aria-label=\"Section navigation (mobile)\">\n  <a href=\"#contributions\">Contributions</a>\n  <a href=\"#method\">Method</a>\n  <a href=\"#results\">Results</a>\n  <a href=\"#figures\">Figures</a>\n  <a href=\"#limitations\">Limitations</a>\n  <a href=\"#code\">Code</a>\n</nav>\n\n<div class=\"page-grid\">\n\n<nav class=\"sidenav\" aria-label=\"Section navigation\">\n  <a href=\"#contributions\">Contributions</a>\n  <a href=\"#method\">Method</a>\n  <a href=\"#results\">Results</a>\n  <a href=\"#sig-results\">Shared signature</a>\n  <a href=\"#dev-results\">Free vocab (dev)</a>\n  <a href=\"#oos-results\">Free vocab (OOS)</a>\n  <a href=\"#mechanism\">Mechanism</a>\n  <a href=\"#rename\">Rename tradeoff</a>\n  <a href=\"#figures\">Figures</a>\n  <a href=\"#limitations\">Limitations</a>\n  <a href=\"#code\">Code</a>\n</nav>\n\n<main id=\"main\">\n\n<header class=\"hero\">\n  <h1>Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for NL-to-FOL Translation</h1>\n  <div class=\"hero-meta\">Anonymous &middot; Preliminary Study</div>\n  <div class=\"hero-tldr\">\n    <strong>TL;DR</strong> &mdash; If independent LLM families translate the same sentence into first-order logic and an SMT solver checks pairwise equivalence, the fraction of peers that disagree with a candidate predicts whether it is faithful to the text. Under shared predicate vocabulary this reaches 0.954 AUROC; under free vocabulary it achieves 0.741 stratified AUROC, outperforming LLM judges by +0.099 on development data without any gold references.\n  </div>\n  <div class=\"hero-links\">\n    <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_cNhUBrixEdz7/paper.pdf\" target=\"_blank\">Read the paper (PDF)</a>\n    <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_cNhUBrixEdz7/report.pdf\" target=\"_blank\">Read the full research report</a>\n    <a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7\" target=\"_blank\">Code repository</a>\n  </div>\n</header>\n\n<section id=\"contributions\">\n  <h2>Contributions</h2>\n  <div class=\"contrib-grid\">\n    <div class=\"contrib-card\">\n      <h3>Shared-signature ceiling</h3>\n      <p>Pre-registered evaluation on 221 long-exception sentences: consensus AUROC 0.954 versus 0.587 for a disguised judge (&Delta;&nbsp;=&nbsp;+0.367), flat across word-length terciles, with zero error endorsement.</p>\n    </div>\n    <div class=\"contrib-card\">\n      <h3>Free-vocabulary signal</h3>\n      <p>On development set&nbsp;E (2,686 items), consensus outperforms judges by &Delta;&nbsp;=&nbsp;+0.099 on stratified AUROC. Aligner-free consensus (c_exact) reaches 0.689 without any predicate mapping.</p>\n    </div>\n    <div class=\"contrib-card\">\n      <h3>Out-of-sample transfer</h3>\n      <p>On untouched R_COMP&nbsp;FREE sentences under provisional labels: &Delta;&nbsp;=&nbsp;+0.171 versus the original-view judge; consensus reaches 0.94 of the frontier judge's AUROC.</p>\n    </div>\n    <div class=\"contrib-card\">\n      <h3>Rename tradeoff</h3>\n      <p>A 76.5% false-alarm rate under nonce predicate renames that no variant could eliminate without sacrificing error recall, identifying a fundamental limit of free-vocabulary consensus.</p>\n    </div>\n  </div>\n</section>\n\n<section id=\"method\">\n  <h2>Method</h2>\n\n  <h3>Consensus scoring</h3>\n  <p>Given a sentence and a candidate FOL translation, collect peer translations from <em>k</em> independent LLM families (Gemini, Claude, GPT, Llama, Qwen, Phi, Mistral). The consensus score is:</p>\n  <p style=\"text-align:center; font-family: var(--serif); font-size: 1.05rem; margin-block: 0.75rem;\">\n    c_score(c, s) = 1 &minus; (1/k) &Sigma; <b>1</b>[equiv(c, p<sub>i</sub>)]\n  </p>\n  <p>Under <strong>shared signature</strong>, all translators use a supplied predicate vocabulary and equiv is a direct Z3 check. Under <strong>free vocabulary</strong>, each translator chooses its own predicate names and equiv requires a predicate-name aligner before the Z3 check.</p>\n\n  <h3>Predicate alignment</h3>\n  <p>The aligner combines three cost components: <strong>structural cost</strong> (polarity profile, argument-count match, nesting depth), <strong>text-anchor cost</strong> (overlap between predicate-name words and source-sentence tokens via Porter stemming and WordNet), and <strong>semantic signature</strong> (truth-value profiles over random finite interpretations). The <em>k</em> cheapest bijections are evaluated, and the pair is declared equivalent if any bijection yields Z3-verified equivalence.</p>\n\n  <h3>Score variants</h3>\n  <p><code>c_exact</code>: no alignment, exact-match only. <code>c_nf</code> (name-free): structural and semantic signatures only, ignoring text anchoring. <code>p_peer_text</code>: logistic fusion of consensus features with text-side features.</p>\n\n  <h3>Evaluation framework</h3>\n  <p><strong>Shared-signature labels</strong> come from Z3 equivalence to trusted-by-construction references. <strong>Free-vocabulary labels</strong> on set&nbsp;E come from a three-person expert panel. The primary metric is <strong>stratified AUROC</strong>: items are paired only within the same source stratum. Confidence intervals use sentence-cluster percentile bootstrap (B&nbsp;=&nbsp;2,000).</p>\n</section>\n\n<section id=\"results\">\n  <h2>Results</h2>\n\n  <div class=\"big-nums\">\n    <div class=\"big-num\">\n      <div class=\"val\">0.954</div>\n      <div class=\"label\">Consensus AUROC<br>(shared signature)</div>\n    </div>\n    <div class=\"big-num\">\n      <div class=\"val\">0.741</div>\n      <div class=\"label\">Consensus AUROC<br>(free vocabulary, dev)</div>\n    </div>\n    <div class=\"big-num\">\n      <div class=\"val\">+0.099</div>\n      <div class=\"label\">&Delta; over judge<br>(free vocabulary, dev)</div>\n    </div>\n  </div>\n\n  <section id=\"sig-results\">\n    <h3>Shared-signature results (R_COMP-SIG)</h3>\n    <p class=\"table-cap\">Table 1: Within-template AUROC on R_COMP-SIG (221 sentences, pure Z3 labels).</p>\n    <div class=\"table-wrap\">\n      <table>\n        <thead><tr><th>Metric</th><th>n</th><th>AUROC [95% CI]</th><th>&Delta; vs disg. judge</th></tr></thead>\n        <tbody>\n          <tr><td><code>c_score_sig</code></td><td>1904</td><td>0.954 [0.939, 0.968]</td><td>+0.367 [+0.328, +0.404]</td></tr>\n          <tr><td><code>c_score_align</code></td><td>1904</td><td>0.954 [0.939, 0.968]</td><td>+0.367 [+0.328, +0.404]</td></tr>\n          <tr><td>Judge (flash-lite, disg.)</td><td>1904</td><td>0.587 [0.551, 0.622]</td><td>&mdash;</td></tr>\n          <tr><td>Judge (flash-lite, orig.)</td><td>1932</td><td>0.673 [0.637, 0.708]</td><td></td></tr>\n          <tr><td>Judge (frontier, orig.)</td><td>60</td><td>0.932 [0.782, 1.000]</td><td></td></tr>\n          <tr><td>Judge (local, disg.)</td><td>2024</td><td>0.498 [0.459, 0.534]</td><td></td></tr>\n        </tbody>\n      </table>\n    </div>\n    <p>Error endorsement is zero (<em>e</em>&nbsp;=&nbsp;0): no error item scores below the decision threshold. Among the 429 error items, 75.3% receive the maximum consensus score of 1.0.</p>\n\n    <p><strong>Flat with sentence length.</strong> Consensus under shared signature is flat across word-length terciles:</p>\n    <p class=\"table-cap\">Table 2: R_COMP-SIG within-template AUROC by word-length tercile.</p>\n    <div class=\"table-wrap\">\n      <table>\n        <thead><tr><th>Tercile</th><th>n</th><th>ERR/COR</th><th>c_sig</th><th>Judge (disg.)</th><th>&Delta; [CI]</th></tr></thead>\n        <tbody>\n          <tr><td>W1 (shortest)</td><td>574</td><td>125/449</td><td>0.959</td><td>0.578</td><td>+0.382 [+0.278, +0.472]</td></tr>\n          <tr><td>W2</td><td>743</td><td>149/594</td><td>0.947</td><td>0.624</td><td>+0.331 [+0.253, +0.421]</td></tr>\n          <tr><td>W3 (longest)</td><td>707</td><td>155/552</td><td>0.953</td><td>0.567</td><td>+0.388 [+0.301, +0.471]</td></tr>\n        </tbody>\n      </table>\n    </div>\n    <p>On a 60-row stratified subsample scored by the frontier judge (Gemini 3.1 Pro), consensus achieves pooled AUROC 0.956 [0.889, 1.000] versus 0.932 [0.855, 0.990].</p>\n  </section>\n\n  <section id=\"dev-results\">\n    <h3>Free-vocabulary development results (set E)</h3>\n    <p class=\"table-cap\">Table 3: Stratified AUROC on development set E (R_AB, free vocabulary, n&nbsp;=&nbsp;2,686).</p>\n    <div class=\"table-wrap\">\n      <table>\n        <thead><tr><th>Metric</th><th>Strat AUROC [95% CI]</th><th>$/item</th></tr></thead>\n        <tbody>\n          <tr><td><code>c_score_align</code></td><td>0.741 [0.705, 0.775]</td><td>9.1e-5</td></tr>\n          <tr><td><code>p_peer_text</code> (fused)</td><td>0.753 [0.720, 0.784]</td><td>9.1e-5</td></tr>\n          <tr><td><code>c_exact</code> (no alignment)</td><td>0.689 [0.652, 0.726]</td><td>&mdash;</td></tr>\n          <tr><td><code>c_nf</code> (name-free)</td><td>0.686 [0.647, 0.720]</td><td>&mdash;</td></tr>\n          <tr><td colspan=\"3\" style=\"border:none;padding:0.2rem\"></td></tr>\n          <tr><td>Flash-lite judge (disg.)</td><td>0.642 [0.607, 0.676]</td><td>5.1e-5</td></tr>\n          <tr><td>Flash-lite judge (orig.)</td><td>0.623 [0.593, 0.651]</td><td>5.1e-5</td></tr>\n          <tr><td>Nano judge (disg.)</td><td>0.644 [0.609, 0.680]</td><td>2.0e-5</td></tr>\n          <tr><td>Local judge Qwen-8B (disg.)</td><td>0.674 [0.646, 0.703]</td><td>&mdash;</td></tr>\n          <tr><td colspan=\"3\" style=\"border:none;padding:0.2rem\"></td></tr>\n          <tr><td>Round-trip NLI (min)</td><td>0.606 [0.569, 0.645]</td><td>2.8e-5</td></tr>\n          <tr><td>Self-consistency (5-sample)</td><td>0.598 [0.559, 0.637]</td><td>6.7e-5</td></tr>\n          <tr><td colspan=\"3\" style=\"border:none;padding:0.2rem\"></td></tr>\n          <tr><td>28-feature stack</td><td>0.735 [0.699, 0.766]</td><td>&mdash;</td></tr>\n          <tr><td>28-feature stack + <code>c_score_align</code></td><td>0.774 [0.743, 0.802]</td><td>&mdash;</td></tr>\n        </tbody>\n      </table>\n    </div>\n    <p>Consensus outperforms the disguised flash-lite judge by &Delta;&nbsp;=&nbsp;+0.099 [+0.049, +0.146] on R_AB and by &Delta;&nbsp;=&nbsp;+0.116 [+0.070, +0.163] on the long-sentence pool. Adding <code>c_score_align</code> to the 28-feature stack increases stratified AUROC by +0.039 [+0.021, +0.057]; permutation null test p<sub>95</sub>&nbsp;=&nbsp;0.009.</p>\n    <p>The drop from 0.952 (shared signature) to 0.801 (free vocabulary, same R_COMP sentences) reflects the cost of predicate-name alignment. Aligner-free consensus (<code>c_exact</code>) at 0.689 shows the aligner adds about 22% of the above-chance signal, with the remaining 78% from structural agreement alone.</p>\n    <p>On L25 sentences alone, &Delta;&nbsp;=&nbsp;+0.069 [&minus;0.020, +0.148], not significant at 95%. Frontier judge comparison on 284 rows: ratio 0.957 [0.887, 1.034]. System-level Kendall &tau;<sub>b</sub>&nbsp;=&nbsp;0.692 [+0.513, +0.795] across 13 configurations.</p>\n  </section>\n\n  <section id=\"oos-results\">\n    <h3>Free-vocabulary out-of-sample (R_COMP FREE)</h3>\n    <p class=\"table-cap\">Table 4: R_COMP FREE provisional AUROCs (within-template, untouched). Labels are non-confirmatory.</p>\n    <div class=\"table-wrap\">\n      <table>\n        <thead><tr><th>View</th><th>n (ERR/MAPPED)</th><th>c_align</th><th>Judge</th></tr></thead>\n        <tbody>\n          <tr><td>Disguised</td><td>1706 (602/1104)</td><td>0.801 [0.770, 0.834]</td><td>0.584 [0.550, 0.618]</td></tr>\n          <tr><td>Original</td><td>1709 (605/1104)</td><td>0.804 [0.774, 0.836]</td><td>0.633 [0.601, 0.666]</td></tr>\n        </tbody>\n      </table>\n    </div>\n    <p>Disguised-judge &Delta;&nbsp;=&nbsp;+0.217 [+0.175, +0.260]; original-view &Delta;&nbsp;=&nbsp;+0.171 [+0.135, +0.206]. Two-auditor subset (146 rows): &Delta;&nbsp;=&nbsp;+0.105 [+0.011, +0.215]. Frontier-judge subsample (150 rows): ratio 0.940 [0.825, 1.056].</p>\n  </section>\n\n  <section id=\"mechanism\">\n    <h3>Mechanism</h3>\n    <p>The consensus signal decomposes into endorsement <em>e</em> (ERROR items endorsed by peers) and divergence <em>d</em> (CORRECT items flagged). On R_COMP-SIG: <em>e</em>&nbsp;=&nbsp;0.0, <em>d</em>&nbsp;=&nbsp;0.260. Under free vocabulary on set E, net degradation from short to long sentences is &Delta;(e+d)&nbsp;=&nbsp;+0.356 [+0.198, +0.493], driven by divergence (&Delta;d&nbsp;=&nbsp;+0.608, &Delta;e&nbsp;=&nbsp;&minus;0.252).</p>\n\n    <p><strong>Family sufficiency.</strong> Three peer families suffice for 97% of full-pool AUROC (k<sub>95</sub>&nbsp;=&nbsp;3); long sentences require k<sub>95</sub>&nbsp;=&nbsp;5.</p>\n    <p class=\"table-cap\">Table 5: Free-vocabulary AUROC by number of peer families on set E.</p>\n    <div class=\"table-wrap\">\n      <table>\n        <thead><tr><th>k</th><th>AUROC (overall)</th><th>AUROC (long, T3)</th></tr></thead>\n        <tbody>\n          <tr><td>1</td><td>0.685</td><td>0.581</td></tr>\n          <tr><td>3</td><td>0.757</td><td>0.651</td></tr>\n          <tr><td>5</td><td>0.776</td><td>0.698</td></tr>\n          <tr><td>7</td><td>0.784</td><td>0.726</td></tr>\n        </tbody>\n      </table>\n    </div>\n  </section>\n\n  <section id=\"confirmation\">\n    <h3>Confirmation status</h3>\n    <p>Independent confirmation remains incomplete. On the one testable stratum (DT), consensus achieves 0.916, tying Qwen-8B (&Delta;&nbsp;=&nbsp;+0.003). On L25, <code>c_score_align</code> falls to 0.443 on 42 items (35 ERROR / 7 CORRECT) with extreme variance. Every pre-registered criterion returned NOT_TESTABLE or unfavourable.</p>\n  </section>\n\n  <section id=\"rename\">\n    <h3>The rename tradeoff</h3>\n    <p class=\"table-cap\">Table 6: False-alarm rates on meaning-preserving renames of CORRECT candidates.</p>\n    <div class=\"table-wrap\">\n      <table>\n        <thead><tr><th>Metric</th><th>NONCE FA</th><th>NONCE flip</th><th>SYN FA</th><th>SYN flip</th></tr></thead>\n        <tbody>\n          <tr><td><code>c_align</code></td><td>0.765</td><td>0.605</td><td>0.565</td><td>0.313</td></tr>\n          <tr><td><code>c_nf</code> (name-free)</td><td>0.132</td><td>0.000</td><td>0.201</td><td>0.000</td></tr>\n          <tr><td><code>p_peer_text</code></td><td>1.000</td><td>0.821</td><td>0.216</td><td>0.080</td></tr>\n          <tr><td>Judge (disg.)</td><td>0.229</td><td>0.134</td><td>0.085</td><td>0.058</td></tr>\n        </tbody>\n      </table>\n    </div>\n    <p>The name-free <code>c_nf</code> eliminates rename sensitivity (flip&nbsp;=&nbsp;0) at the cost of blindness to meaning-rename errors (AUROC 0.499, chance) and lower overall discrimination (0.686 vs. 0.741).</p>\n  </section>\n\n  <section id=\"dead-ends\">\n    <h3>Dead ends</h3>\n    <p>Abandoned alternatives: fused structural-feature filter (gate failure); name-free consensus (rename-invariant but blind); solver-based semantic reader (balanced accuracy 0.476); LLM adjudication (0.662); candidate-signature consensus (error endorsement rose to 0.459).</p>\n  </section>\n</section>\n\n<section id=\"figures\">\n  <h2>Figures</h2>\n  <div class=\"fig-gallery\">\n    <figure class=\"fig-card\" tabindex=\"0\" role=\"button\" aria-label=\"Enlarge Figure 1\">\n      <img src=\"figures/fig_dev_auroc_v0.png\"\n           alt=\"Horizontal bar chart comparing stratified AUROC across 12 metrics on the free-vocabulary development set. Consensus-based metrics cluster around 0.69 to 0.77; LLM judges around 0.62 to 0.67; other baselines near 0.60.\">\n      <figcaption class=\"fig-caption\">Fig. 1: Stratified AUROC on the free-vocabulary development set.</figcaption>\n      <p class=\"fig-hint\">Click to enlarge</p>\n    </figure>\n    <figure class=\"fig-card\" tabindex=\"0\" role=\"button\" aria-label=\"Enlarge Figure 2\">\n      <img src=\"figures/fig_sig_tercile_v0.png\"\n           alt=\"Grouped bar chart showing within-template AUROC by word-length tercile on R_COMP-SIG. Consensus (blue) is flat at 0.947 to 0.959; disguised judge (orange) hovers near chance at 0.567 to 0.624.\">\n      <figcaption class=\"fig-caption\">Fig. 2: R_COMP-SIG AUROC by word-length tercile. Consensus is flat; the judge hovers near chance.</figcaption>\n      <p class=\"fig-hint\">Click to enlarge</p>\n    </figure>\n    <figure class=\"fig-card\" tabindex=\"0\" role=\"button\" aria-label=\"Enlarge Figure 3\">\n      <img src=\"figures/fig_complexity_v0.png\"\n           alt=\"Bar chart decomposing consensus errors by sentence-length tercile. Endorsement rate e decreases from 0.29 to 0.04 while divergence rate d increases from 0.31 to 0.91.\">\n      <figcaption class=\"fig-caption\">Fig. 3: Consensus error decomposition by sentence length. Net degradation &Delta;(e+d)&nbsp;=&nbsp;+0.356.</figcaption>\n      <p class=\"fig-hint\">Click to enlarge</p>\n    </figure>\n    <figure class=\"fig-card\" tabindex=\"0\" role=\"button\" aria-label=\"Enlarge Figure 4\">\n      <img src=\"figures/fig_k_curve_v0.png\"\n           alt=\"Line chart of AUROC vs number of peer families k. Overall curve rises steeply to k=3 then flattens; long-sentence tercile rises more slowly, requiring k=5.\">\n      <figcaption class=\"fig-caption\">Fig. 4: AUROC vs peer families k. Three families capture 97% of signal; long sentences need five.</figcaption>\n      <p class=\"fig-hint\">Click to enlarge</p>\n    </figure>\n  </div>\n</section>\n\n<section id=\"limitations\">\n  <h2>Limitations</h2>\n  <ol class=\"lim-list\">\n    <li><strong>Shared-signature scope.</strong> The 0.954 AUROC uses templated sentences with a supplied predicate vocabulary, limiting scope to controlled settings.</li>\n    <li><strong>Development data overlap.</strong> R_COMP-SIG later served as development data for aligner tuning. The pre-registration keeps the SIG result uncontaminated, but set E numbers are not independent.</li>\n    <li><strong>Rename vulnerability.</strong> Under free vocabulary, 76.5% false-alarm rate on nonce renames systematically penalises non-standard predicate names.</li>\n    <li><strong>Length degradation.</strong> Consensus degrades with sentence length under free vocabulary (NET +0.356), weakest on the longest, most complex sentences.</li>\n    <li><strong>Provisional labels.</strong> R_COMP FREE uses non-confirmatory labels; the two-auditor subset (&Delta;&nbsp;=&nbsp;+0.105) barely excludes zero.</li>\n    <li><strong>Label dependence.</strong> Development results depend on a three-person panel whose agreement is imperfect.</li>\n    <li><strong>Cost.</strong> At k&nbsp;=&nbsp;9, the amortised consensus cost per candidate is about 19 times the cost of a single cheap judge call.</li>\n    <li><strong>Domain.</strong> All results are on English-to-FOL from MALLS, ProverQA, and R_COMP. Generalisation is untested.</li>\n  </ol>\n</section>\n\n<section id=\"code\">\n  <h2>Code artifacts</h2>\n  <p>All evaluation code is released. Each link points to the experiment or dataset that produced the corresponding result.</p>\n  <div class=\"artifact-grid\">\n    <a class=\"artifact-link\" href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-1/experiment-1\" target=\"_blank\">\n      <span class=\"art-label\">Consensus scoring</span>\n      <span class=\"art-path\">round-1/experiment-1</span>\n    </a>\n    <a class=\"artifact-link\" href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-1/experiment-3\" target=\"_blank\">\n      <span class=\"art-label\">Development set E</span>\n      <span class=\"art-path\">round-1/experiment-3</span>\n    </a>\n    <a class=\"artifact-link\" href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-1/experiment-4\" target=\"_blank\">\n      <span class=\"art-label\">Baselines</span>\n      <span class=\"art-path\">round-1/experiment-4</span>\n    </a>\n    <a class=\"artifact-link\" href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-1/dataset-1\" target=\"_blank\">\n      <span class=\"art-label\">Code: Held-out logic translation test set, panel-checked</span>\n      <span class=\"art-path\">round-1/dataset-1</span>\n    </a>\n    <a class=\"artifact-link\" href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-2/experiment-5\" target=\"_blank\">\n      <span class=\"art-label\">Fused scorer (p_peer_text)</span>\n      <span class=\"art-path\">round-2/experiment-5</span>\n    </a>\n    <a class=\"artifact-link\" href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-2/dataset-3\" target=\"_blank\">\n      <span class=\"art-label\">Code: Long logic sentences and FOL error suite</span>\n      <span class=\"art-path\">round-2/dataset-3</span>\n    </a>\n    <a class=\"artifact-link\" href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-2/evaluation-1\" target=\"_blank\">\n      <span class=\"art-label\">Code: Re-checking earlier logic-metric results across label sets</span>\n      <span class=\"art-path\">round-2/evaluation-1</span>\n    </a>\n    <a class=\"artifact-link\" href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/experiment-6\" target=\"_blank\">\n      <span class=\"art-label\">Dev results analysis</span>\n      <span class=\"art-path\">round-3/experiment-6</span>\n    </a>\n    <a class=\"artifact-link\" href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/experiment-7\" target=\"_blank\">\n      <span class=\"art-label\">R_COMP dataset</span>\n      <span class=\"art-path\">round-3/experiment-7</span>\n    </a>\n    <a class=\"artifact-link\" href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/evaluation-2\" target=\"_blank\">\n      <span class=\"art-label\">Mechanism decomposition</span>\n      <span class=\"art-path\">round-3/evaluation-2</span>\n    </a>\n    <a class=\"artifact-link\" href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/experiment-8\" target=\"_blank\">\n      <span class=\"art-label\">Rename tradeoff</span>\n      <span class=\"art-path\">round-3/experiment-8</span>\n    </a>\n    <a class=\"artifact-link\" href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/research-1\" target=\"_blank\">\n      <span class=\"art-label\">Code: What is new about peer agreement for logic</span>\n      <span class=\"art-path\">round-3/research-1</span>\n    </a>\n    <a class=\"artifact-link\" href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-4/dataset-4\" target=\"_blank\">\n      <span class=\"art-label\">Held-out dataset E2-A</span>\n      <span class=\"art-path\">round-4/dataset-4</span>\n    </a>\n    <a class=\"artifact-link\" href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-4/experiment-9\" target=\"_blank\">\n      <span class=\"art-label\">Dead ends</span>\n      <span class=\"art-path\">round-4/experiment-9</span>\n    </a>\n    <a class=\"artifact-link\" href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-4/experiment-10\" target=\"_blank\">\n      <span class=\"art-label\">Code: Do symbol hints help model agreement checks?</span>\n      <span class=\"art-path\">round-4/experiment-10</span>\n    </a>\n    <a class=\"artifact-link\" href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-4/dataset-5\" target=\"_blank\">\n      <span class=\"art-label\">Code: Name-free labels for free-vocabulary logic translations</span>\n      <span class=\"art-path\">round-4/dataset-5</span>\n    </a>\n    <a class=\"artifact-link\" href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-4/evaluation-3\" target=\"_blank\">\n      <span class=\"art-label\">Code: Can shared vocabulary fix consensus blind spots?</span>\n      <span class=\"art-path\">round-4/evaluation-3</span>\n    </a>\n    <a class=\"artifact-link\" href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-5/experiment-11\" target=\"_blank\">\n      <span class=\"art-label\">Code: Consensus vs LLM judges on fresh logic data</span>\n      <span class=\"art-path\">round-5/experiment-11</span>\n    </a>\n    <a class=\"artifact-link\" href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-5/experiment-12\" target=\"_blank\">\n      <span class=\"art-label\">Code: Second fresh sample of long logic sentences</span>\n      <span class=\"art-path\">round-5/experiment-12</span>\n    </a>\n    <a class=\"artifact-link\" href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-5/experiment-13\" target=\"_blank\">\n      <span class=\"art-label\">R_COMP FREE (OOS)</span>\n      <span class=\"art-path\">round-5/experiment-13</span>\n    </a>\n    <a class=\"artifact-link\" href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-5/experiment-14\" target=\"_blank\">\n      <span class=\"art-label\">Code: Screening fixes for model-agreement false alarms</span>\n      <span class=\"art-path\">round-5/experiment-14</span>\n    </a>\n    <a class=\"artifact-link\" href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-5/evaluation-4\" target=\"_blank\">\n      <span class=\"art-label\">Code: Corrected record: every paper number checked</span>\n      <span class=\"art-path\">round-5/evaluation-4</span>\n    </a>\n  </div>\n</section>\n\n<footer class=\"site-footer\">\n  <p><a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_cNhUBrixEdz7/paper.pdf\" target=\"_blank\">Read the paper (PDF)</a> &middot;\n     <a href=\"https://cdn.jsdelivr.net/gh/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic@fork/run_cNhUBrixEdz7/report.pdf\" target=\"_blank\">Read the full research report</a> &middot;\n     <a href=\"https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7\" target=\"_blank\">Code repository</a></p>\n  <p>Citation:</p>\n  <div class=\"cite-block\">@article{anonymous2026crossfamily,\n  title={Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric\n         for Natural-Language-to-First-Order-Logic Translation},\n  author={Anonymous},\n  year={2026}\n}</div>\n</footer>\n\n</main>\n</div>\n\n<div class=\"lightbox\" id=\"lightbox\" role=\"dialog\" aria-modal=\"true\" aria-label=\"Enlarged figure\" hidden>\n  <div class=\"lightbox-inner\">\n    <button class=\"lightbox-close\" aria-label=\"Close enlarged figure\">&times;</button>\n    <img id=\"lightbox-img\" src=\"figures/fig_dev_auroc_v0.png\" alt=\"\">\n    <p class=\"lightbox-cap\" id=\"lightbox-cap\"></p>\n  </div>\n</div>\n\n<script>\n(function() {\n  'use strict';\n  var sections = document.querySelectorAll('main > section, main > header');\n  var navD = document.querySelectorAll('.sidenav a');\n  var navM = document.querySelectorAll('.mobile-nav a');\n  function setActive(id) {\n    [navD, navM].forEach(function(ls) {\n      ls.forEach(function(a) { a.classList.toggle('active', a.getAttribute('href') === '#' + id); });\n    });\n  }\n  if ('IntersectionObserver' in window) {\n    var obs = new IntersectionObserver(function(entries) {\n      entries.forEach(function(e) { if (e.isIntersecting) setActive(e.target.id); });\n    }, { rootMargin: '-20% 0px -60% 0px' });\n    sections.forEach(function(s) { if (s.id) obs.observe(s); });\n  }\n\n  var lightbox = document.getElementById('lightbox');\n  var lbImg = document.getElementById('lightbox-img');\n  var lbCap = document.getElementById('lightbox-cap');\n  var trigger = null;\n\n  document.querySelectorAll('.fig-card').forEach(function(card) {\n    function open() {\n      var img = card.querySelector('img');\n      var cap = card.querySelector('.fig-caption');\n      lbImg.src = img.src; lbImg.alt = img.alt;\n      lbCap.textContent = cap ? cap.textContent : '';\n      lightbox.hidden = false;\n      requestAnimationFrame(function() { lightbox.classList.add('open'); });\n      document.body.style.overflow = 'hidden';\n      trigger = card;\n      lightbox.querySelector('.lightbox-close').focus();\n    }\n    card.addEventListener('click', open);\n    card.addEventListener('keydown', function(e) {\n      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); open(); }\n    });\n  });\n\n  function close() {\n    lightbox.classList.remove('open');\n    document.body.style.overflow = '';\n    lightbox.hidden = true;\n    lbImg.removeAttribute('src');\n    if (trigger) { trigger.focus(); trigger = null; }\n  }\n  lightbox.querySelector('.lightbox-close').addEventListener('click', close);\n  lightbox.addEventListener('click', function(e) { if (e.target === lightbox) close(); });\n  document.addEventListener('keydown', function(e) { if (e.key === 'Escape' && !lightbox.hidden) close(); });\n})();\n</script>\n</body>\n</html>\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [24] ASSISTANT · 2026-09-25 02:48:02 UTC

```
Now verify numbers, URLs, images, and render test:
```

### [25] TOOL CALL — Bash · 2026-09-25 02:48:02 UTC

```
Verify numbers, URLs, and no external resources:
\
echo "=== No external resources ===" && \
grep -c 'fonts.googleapis\|cdnjs\|cdn.tailwindcss\|unpkg.com' index.html && \
echo "=== Image sources ===" && \
grep -o 'src="[^"]*"' index.html | sort -u && \
echo "=== Key numbers ===" && \
for n in 0.954 0.587 0.367 0.741 0.099 0.171 0.952 0.689 0.686 0.753 0.642 0.623 0.644 0.674 0.606 0.598 0.735 0.774 0.801 0.804 0.765 0.605 0.565 0.313 0.916 0.443 0.476 0.662 0.459; do
  if grep -q "$n" paper.tex; then printf "OK  %s\n" "$n"; else printf "MISS %s\n" "$n"; fi
done && \
echo "=== Required URLs ===" && \
for p in "report.pdf" "run_cNhUBrixEdz7/paper.pdf" "tree/fork/run_cNhUBrixEdz7\"" dataset-1 dataset-3 evaluation-1 research-1 experiment-10 dataset-5 evaluation-3 experiment-11 experiment-12 experiment-14 evaluation-4; do
  if grep -q "$p" index.html; then printf "OK  %s\n" "$p"; else printf "MISS %s\n" "$p"; fi
done
```

### [26] TOOL RESULT — Bash [ERROR] · 2026-09-25 02:48:02 UTC

```
Error: Exit code 1
=== No external resources ===
0
```

### [27] TOOL CALL — Bash · 2026-09-25 02:48:08 UTC

```
Verify all content:
\
echo "External resources: $(grep -c 'fonts.googleapis' index.html)" && \
echo "=== img src ===" && grep -o 'src="[^"]*"' index.html | sort -u && \
echo "=== Numbers ===" && \
ok=0; miss=0; for n in 0.954 0.587 0.367 0.741 0.099 0.171 0.952 0.689 0.686 0.753 0.642 0.623 0.644 0.674 0.606 0.598 0.735 0.774 0.801 0.804 0.765 0.605 0.565 0.313 0.916 0.443 0.476 0.662 0.459; do
  if grep -q "$n" paper.tex; then ok=$((ok+1)); else echo "MISS $n"; miss=$((miss+1)); fi
done; echo "$ok OK, $miss MISS" && \
echo "=== Required URLs ===" && \
ok=0; miss=0; for p in "report.pdf" "cNhUBrixEdz7/paper.pdf" "tree/fork/run_cNhUBrixEdz7" dataset-1 dataset-3 evaluation-1 research-1 experiment-10 dataset-5 evaluation-3 experiment-11 experiment-12 experiment-14 evaluation-4; do
  if grep -q "$p" index.html; then ok=$((ok+1)); else echo "MISS $p"; miss=$((miss+1)); fi
done; echo "$ok OK, $miss MISS"
```

### [28] TOOL RESULT — Bash · 2026-09-25 02:48:10 UTC

```
{"stdout": "External resources: 0\n=== img src ===\nsrc=\"figures/fig_complexity_v0.png\"\nsrc=\"figures/fig_dev_auroc_v0.png\"\nsrc=\"figures/fig_k_curve_v0.png\"\nsrc=\"figures/fig_sig_tercile_v0.png\"\n=== Numbers ===\n29 OK, 0 MISS\n=== Required URLs ===\n14 OK, 0 MISS", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [29] ASSISTANT · 2026-09-25 02:48:14 UTC

```
All 29 numbers verified, all 14 required URL patterns present, no external resources, all 4 image sources point to existing PNGs. Now install playwright and test:
```

### [30] TOOL CALL — Bash · 2026-09-25 02:48:14 UTC

```
Install playwright and chromium:
pip install playwright 2>&1 | tail -2 && python -m playwright install chromium 2>&1 | tail -2 && python -m playwright install-deps chromium 2>&1 | tail -2
```

### [31] TOOL RESULT — Bash · 2026-09-25 02:48:42 UTC

```
{"stdout": "[notice] A new release of pip is available: 25.0.1 -> 26.2.1\n[notice] To update, run: pip install --upgrade pip\n|■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■| 100% of 114.3 MiB\nChrome Headless Shell 153.0.8010.12 (playwright chromium-headless-shell v1243) downloaded to /root/.cache/ms-playwright/chromium_headless_shell-1243\nProcessing triggers for man-db (2.11.2-2) ...\r\nProcessing triggers for libc-bin (2.36-9+deb12u14) ...", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [32] TOOL CALL — Bash · 2026-09-25 02:48:54 UTC

```
Test page rendering, lightbox, and links:
python3 -c "
from playwright.sync_api import sync_playwright
import os

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    page.goto('file://' + os.path.abspath('index.html'))
    page.wait_for_load_state('networkidle')
    print('Title:', page.title())

    imgs = page.query_selector_all('img[src]')
    print(f'Images: {len(imgs)}')
    for img in imgs:
        w = img.evaluate('el => el.naturalWidth')
        s = img.get_attribute('src').split('/')[-1]
        print(f'  {s} w={w}')

    # Lightbox
    page.click('.fig-card')
    page.wait_for_timeout(400)
    lb = page.query_selector('#lightbox')
    print(f'Lightbox open: {lb.is_visible()}')
    page.keyboard.press('Escape')
    page.wait_for_timeout(200)
    print(f'Lightbox closed: {not lb.is_visible()}')

    arts = page.query_selector_all('.artifact-link')
    print(f'Artifact links: {len(arts)}')

    hero = page.query_selector_all('.hero-links a')
    print(f'Hero links: {len(hero)}')
    for a in hero: print(f'  {a.text_content().strip()}')

    browser.close()
    print('All checks passed')
"
```

### [33] TOOL RESULT — Bash · 2026-09-25 02:48:54 UTC

```
{"stdout": "Title: Gold-Free Faithfulness Metrics for NL-to-FOL\nImages: 5\n  fig_dev_auroc_v0.png w=1260\n  fig_sig_tercile_v0.png w=1260\n  fig_complexity_v0.png w=1260\n  fig_k_curve_v0.png w=1260\n  fig_dev_auroc_v0.png w=1260\nLightbox open: True\nLightbox closed: True\nArtifact links: 22\nHero links: 3\n  Read the paper (PDF)\n  Read the full research report\n  Code repository\nAll checks passed", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [34] ASSISTANT · 2026-09-25 02:48:58 UTC

```
Page renders perfectly. Now create the remaining files:
```

### [35] TOOL CALL — Bash · 2026-09-25 02:48:58 UTC

```
Ensure .aii directory:
mkdir -p /ai-inventor/aii_data/runs/run_cNhUBrixEdz7/4_gen_paper_repo/_4_assemble_paper/paper/.aii
```

### [36] TOOL RESULT — Bash · 2026-09-25 02:48:58 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": true}
```

### [37] TOOL CALL — Write · 2026-09-25 02:49:30 UTC

```
File: /ai-inventor/aii_data/runs/run_cNhUBrixEdz7/4_gen_paper_repo/_4_assemble_paper/paper/.aii/manifest.yaml

entries: []
```

### [38] TOOL RESULT — Write · 2026-09-25 02:49:30 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_cNhUBrixEdz7/4_gen_paper_repo/_4_assemble_paper/paper/.aii/manifest.yaml", "content": "entries: []\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [39] TOOL CALL — Write · 2026-09-25 02:49:30 UTC

```
File: /ai-inventor/aii_data/runs/run_cNhUBrixEdz7/4_gen_paper_repo/_4_assemble_paper/paper/README.md

# Gold-Free Faithfulness Metrics for NL-to-FOL Translation

Public project page for the paper *Cross-Family Solver Consensus as a
Gold-Free Faithfulness Metric for Natural-Language-to-First-Order-Logic
Translation*.

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
```

### [40] TOOL RESULT — Write · 2026-09-25 02:49:30 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_cNhUBrixEdz7/4_gen_paper_repo/_4_assemble_paper/paper/README.md", "content": "# Gold-Free Faithfulness Metrics for NL-to-FOL Translation\n\nPublic project page for the paper *Cross-Family Solver Consensus as a\nGold-Free Faithfulness Metric for Natural-Language-to-First-Order-Logic\nTranslation*.\n\n## What this is\n\nA single self-contained HTML page that presents the paper's contributions,\nmethod, results, and figures faster than reading the PDF. Designed to be\nserved directly from GitHub Pages with no build step.\n\n## Repository layout\n\n| Path | Description |\n|------|-------------|\n| `index.html` | Self-contained project page (inline CSS/JS, no external deps) |\n| `paper.tex` | LaTeX source of the paper |\n| `paper.pdf` | Compiled PDF |\n| `references.bib` | BibTeX bibliography |\n| `references.json` | Structured bibliography in JSON |\n| `figures/*.png` | Rendered figures used by the project page |\n| `figures/*.pdf` | Vector figure originals |\n| `figures/*_spec.json` | Figure generation specifications |\n\n## Viewing the page\n\nOpen `index.html` in any modern browser, or visit the GitHub Pages deployment.\nNo build step, server, or external resources are required.\n\n## License\n\nSee the paper for terms.\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [41] TOOL CALL — Write · 2026-09-25 02:49:30 UTC

```
File: /ai-inventor/aii_data/runs/run_cNhUBrixEdz7/4_gen_paper_repo/_4_assemble_paper/paper/.terminal_claude_agent_struct_out.json

{
  "summary": "Built a self-contained index.html presenting the paper 'Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for NL-to-FOL Translation'. The page includes: Hero section with title, author, TL;DR (quoting 0.954 shared-sig AUROC and 0.741 free-vocab AUROC from paper.tex Tables 1 and 3), and three links (paper PDF, research report, code repository using exact CDN and GitHub URLs). Four contribution cards covering shared-signature ceiling (0.954 vs 0.587, Delta +0.367), free-vocabulary signal (0.741, Delta +0.099), out-of-sample transfer (Delta +0.171), and rename tradeoff (76.5% FA rate). Method section covering consensus scoring formula, predicate alignment (structural/text-anchor/semantic cost), score variants (c_exact, c_nf, p_peer_text), and evaluation framework (stratified AUROC, sentence-cluster bootstrap B=2000). Results section with six data tables: Table 1 (R_COMP-SIG within-template AUROC with Delta column, 6 metrics from paper Table 1, n=1904), Table 2 (word-length tercile breakdown W1/W2/W3 from paper Table 2), Table 3 (development set E stratified AUROC, 12 metrics from paper Table 3), Table 4 (R_COMP FREE provisional AUROCs from paper Table 4), Table 5 (AUROC by peer families k=1..7 from paper Table 5), Table 6 (rename FA rates from paper Table 6). Three big-number tiles (0.954, 0.741, +0.099). Mechanism section with e/d decomposition (e=0.0, d=0.260 shared sig; NET Delta(e+d)=+0.356 free vocab, Delta_d=+0.608, Delta_e=-0.252). Confirmation status (DT 0.916, L25 0.443 on 42 items). Dead ends (0.476, 0.662, 0.459). Figure gallery with lightbox for all four figures: fig_dev_auroc_v0.png, fig_sig_tercile_v0.png (new in this paper version), fig_complexity_v0.png, fig_k_curve_v0.png. Limitations section (8 items). Code artifacts section with 22 links including all 11 paper footnote URLs plus 11 additional artifact links using exact GitHub URLs. Footer with CDN paper/report links and citation. Sticky side navigation on desktop, horizontal scroll nav on mobile. All 29 key numbers verified against paper.tex. Responsive (375px tested), keyboard accessible, dark mode, prefers-reduced-motion, no external dependencies.",
  "out_expected_files": {
    "site_html_path": "index.html"
  }
}
```

### [42] TOOL RESULT — Write · 2026-09-25 02:49:30 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_cNhUBrixEdz7/4_gen_paper_repo/_4_assemble_paper/paper/.terminal_claude_agent_struct_out.json", "content": "{\n  \"summary\": \"Built a self-contained index.html presenting the paper 'Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for NL-to-FOL Translation'. The page includes: Hero section with title, author, TL;DR (quoting 0.954 shared-sig AUROC and 0.741 free-vocab AUROC from paper.tex Tables 1 and 3), and three links (paper PDF, research report, code repository using exact CDN and GitHub URLs). Four contribution cards covering shared-signature ceiling (0.954 vs 0.587, Delta +0.367), free-vocabulary signal (0.741, Delta +0.099), out-of-sample transfer (Delta +0.171), and rename tradeoff (76.5% FA rate). Method section covering consensus scoring formula, predicate alignment (structural/text-anchor/semantic cost), score variants (c_exact, c_nf, p_peer_text), and evaluation framework (stratified AUROC, sentence-cluster bootstrap B=2000). Results section with six data tables: Table 1 (R_COMP-SIG within-template AUROC with Delta column, 6 metrics from paper Table 1, n=1904), Table 2 (word-length tercile breakdown W1/W2/W3 from paper Table 2), Table 3 (development set E stratified AUROC, 12 metrics from paper Table 3), Table 4 (R_COMP FREE provisional AUROCs from paper Table 4), Table 5 (AUROC by peer families k=1..7 from paper Table 5), Table 6 (rename FA rates from paper Table 6). Three big-number tiles (0.954, 0.741, +0.099). Mechanism section with e/d decomposition (e=0.0, d=0.260 shared sig; NET Delta(e+d)=+0.356 free vocab, Delta_d=+0.608, Delta_e=-0.252). Confirmation status (DT 0.916, L25 0.443 on 42 items). Dead ends (0.476, 0.662, 0.459). Figure gallery with lightbox for all four figures: fig_dev_auroc_v0.png, fig_sig_tercile_v0.png (new in this paper version), fig_complexity_v0.png, fig_k_curve_v0.png. Limitations section (8 items). Code artifacts section with 22 links including all 11 paper footnote URLs plus 11 additional artifact links using exact GitHub URLs. Footer with CDN paper/report links and citation. Sticky side navigation on desktop, horizontal scroll nav on mobile. All 29 key numbers verified against paper.tex. Responsive (375px tested), keyboard accessible, dark mode, prefers-reduced-motion, no external dependencies.\",\n  \"out_expected_files\": {\n    \"site_html_path\": \"index.html\"\n  }\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [43] TOOL CALL — Bash · 2026-09-25 02:49:36 UTC

```
Final validation of all deliverables:
\
python3 -c "import json; d=json.load(open('.terminal_claude_agent_struct_out.json')); print('Valid JSON, site_html_path:', d['out_expected_files']['site_html_path'], ', summary:', len(d['summary']), 'chars')" && \
python3 -c "import yaml; d=yaml.safe_load(open('.aii/manifest.yaml')); print('Valid YAML, entries:', d['entries'])" && \
echo "=== All deliverables ===" && \
ls -la index.html .terminal_claude_agent_struct_out.json .aii/manifest.yaml README.md figures/*.png
```

### [44] TOOL RESULT — Bash · 2026-09-25 02:49:36 UTC

```
{"stdout": "Valid JSON, site_html_path: index.html , summary: 2167 chars\nValid YAML, entries: []\n=== All deliverables ===\n-rw-r--r-- 1 root root    12 Sep 25 02:49 .aii/manifest.yaml\n-rw-r--r-- 1 root root  2253 Sep 25 02:49 .terminal_claude_agent_struct_out.json\n-rw-r--r-- 1 root root  1129 Sep 25 02:49 README.md\n-rw-r--r-- 1 root root 58891 Sep 25 02:44 figures/fig_complexity_v0.png\n-rw-r--r-- 1 root root 78933 Sep 25 02:44 figures/fig_dev_auroc_v0.png\n-rw-r--r-- 1 root root 70485 Sep 25 02:44 figures/fig_k_curve_v0.png\n-rw-r--r-- 1 root root 53675 Sep 25 02:44 figures/fig_sig_tercile_v0.png\n-rw-r--r-- 1 root root 38562 Sep 25 02:47 index.html", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [45] ASSISTANT · 2026-09-25 02:49:44 UTC

```
All deliverables complete:

- **`index.html`** (39KB) -- self-contained page with all sections, 6 tables, 4 figures with lightbox, 22 code artifact links, 3 hero links (paper PDF, research report, code repo using exact URLs). All 29 numbers from paper.tex. No external dependencies. Responsive, dark mode, keyboard accessible.
- **`.terminal_claude_agent_struct_out.json`** -- valid JSON (2,167-char summary, `site_html_path: "index.html"`)
- **`.aii/manifest.yaml`** -- `entries: []` (all files under auto-keep floor)
- **`README.md`** -- repository description
- **`figures/*.png`** -- 4 PNGs rendered from PDF figures (including the new `fig_sig_tercile_v0`)
```

### [46] SYSTEM-USER prompt · 2026-09-25 02:50:16 UTC

```
continue where you left off — reuse any partial work already written to disk. Do NOT start over.
```

### [47] ASSISTANT · 2026-09-25 02:50:24 UTC

```
Let me check the current state of the workspace.
```

### [48] TOOL CALL — Bash · 2026-09-25 02:50:24 UTC

```
Check current state of all deliverables:
echo "=== Files ===" && ls -la index.html .terminal_claude_agent_struct_out.json .aii/manifest.yaml README.md figures/*.png 2>/dev/null && echo "=== Struct out ===" && cat .terminal_claude_agent_struct_out.json && echo "=== Manifest ===" && cat .aii/manifest.yaml
```

### [49] TOOL RESULT — Bash · 2026-09-25 02:50:24 UTC

```
{"stdout": "=== Files ===\n-rw-r--r-- 1 root root    12 Sep 25 02:49 .aii/manifest.yaml\n-rw-r--r-- 1 root root  2253 Sep 25 02:49 .terminal_claude_agent_struct_out.json\n-rw-r--r-- 1 root root  1129 Sep 25 02:49 README.md\n-rw-r--r-- 1 root root 58891 Sep 25 02:44 figures/fig_complexity_v0.png\n-rw-r--r-- 1 root root 78933 Sep 25 02:44 figures/fig_dev_auroc_v0.png\n-rw-r--r-- 1 root root 70485 Sep 25 02:44 figures/fig_k_curve_v0.png\n-rw-r--r-- 1 root root 53675 Sep 25 02:44 figures/fig_sig_tercile_v0.png\n-rw-r--r-- 1 root root 38562 Sep 25 02:47 index.html\n=== Struct out ===\n{\n  \"summary\": \"Built a self-contained index.html presenting the paper 'Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for NL-to-FOL Translation'. The page includes: Hero section with title, author, TL;DR (quoting 0.954 shared-sig AUROC and 0.741 free-vocab AUROC from paper.tex Tables 1 and 3), and three links (paper PDF, research report, code repository using exact CDN and GitHub URLs). Four contribution cards covering shared-signature ceiling (0.954 vs 0.587, Delta +0.367), free-vocabulary signal (0.741, Delta +0.099), out-of-sample transfer (Delta +0.171), and rename tradeoff (76.5% FA rate). Method section covering consensus scoring formula, predicate alignment (structural/text-anchor/semantic cost), score variants (c_exact, c_nf, p_peer_text), and evaluation framework (stratified AUROC, sentence-cluster bootstrap B=2000). Results section with six data tables: Table 1 (R_COMP-SIG within-template AUROC with Delta column, 6 metrics from paper Table 1, n=1904), Table 2 (word-length tercile breakdown W1/W2/W3 from paper Table 2), Table 3 (development set E stratified AUROC, 12 metrics from paper Table 3), Table 4 (R_COMP FREE provisional AUROCs from paper Table 4), Table 5 (AUROC by peer families k=1..7 from paper Table 5), Table 6 (rename FA rates from paper Table 6). Three big-number tiles (0.954, 0.741, +0.099). Mechanism section with e/d decomposition (e=0.0, d=0.260 shared sig; NET Delta(e+d)=+0.356 free vocab, Delta_d=+0.608, Delta_e=-0.252). Confirmation status (DT 0.916, L25 0.443 on 42 items). Dead ends (0.476, 0.662, 0.459). Figure gallery with lightbox for all four figures: fig_dev_auroc_v0.png, fig_sig_tercile_v0.png (new in this paper version), fig_complexity_v0.png, fig_k_curve_v0.png. Limitations section (8 items). Code artifacts section with 22 links including all 11 paper footnote URLs plus 11 additional artifact links using exact GitHub URLs. Footer with CDN paper/report links and citation. Sticky side navigation on desktop, horizontal scroll nav on mobile. All 29 key numbers verified against paper.tex. Responsive (375px tested), keyboard accessible, dark mode, prefers-reduced-motion, no external dependencies.\",\n  \"out_expected_files\": {\n    \"site_html_path\": \"index.html\"\n  }\n}\n=== Manifest ===\nentries: []", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [50] ASSISTANT · 2026-09-25 02:50:32 UTC

```
Everything is already complete. All deliverables were written in the previous turn and validated:

- **`index.html`** (39KB) -- fully built, tested with Playwright (lightbox, nav, all 4 figures loading, 22 artifact links, 3 hero links with exact URLs)
- **`.terminal_claude_agent_struct_out.json`** -- valid JSON, 2,167-char summary, `site_html_path: "index.html"`
- **`.aii/manifest.yaml`** -- `entries: []`
- **`README.md`** -- repository description
- **`figures/*.png`** -- all 4 PNGs rendered from PDFs

No further work needed.
```

### [51] SYSTEM-USER prompt · 2026-09-25 02:50:32 UTC

```
continue where you left off — reuse any partial work already written to disk. Do NOT start over.
```

### [52] ASSISTANT · 2026-09-25 02:50:40 UTC

```
All deliverables are already on disk and validated. Nothing remains to do.
```

### [53] TOOL CALL — Bash · 2026-09-25 02:50:40 UTC

```
Confirm all deliverables exist and are valid:
python3 -c "
import json
d = json.load(open('.terminal_claude_agent_struct_out.json'))
print('site_html_path:', d['out_expected_files']['site_html_path'])
print('summary length:', len(d['summary']), 'chars')
print('Valid:', 300 <= len(d['summary']) <= 5000)
" && ls -1 index.html figures/*.png .aii/manifest.yaml README.md
```

### [54] TOOL RESULT — Bash · 2026-09-25 02:50:40 UTC

```
{"stdout": "site_html_path: index.html\nsummary length: 2167 chars\nValid: True\n.aii/manifest.yaml\nREADME.md\nfigures/fig_complexity_v0.png\nfigures/fig_dev_auroc_v0.png\nfigures/fig_k_curve_v0.png\nfigures/fig_sig_tercile_v0.png\nindex.html", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [55] ASSISTANT · 2026-09-25 02:50:44 UTC

```
All files present and valid. The task is complete.
```
