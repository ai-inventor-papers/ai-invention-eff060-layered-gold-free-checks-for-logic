# gen_full_paper — report_results

> Phase: `gen_paper_repo` · `gen_full_paper`
> Run: `gen_paper_repo_a2e1d024cc16` — Gold-Free Faithfulness Metrics for NL-to-FOL Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_full_paper` (terminal_claude_agent, claude-opus-4-6)

### [1] CONFIG · 2026-09-25 09:26:10 UTC

```
model: claude-opus-4-6 | effort: high | permission: bypassPermissions
```

### [2] HUMAN-USER prompt · 2026-09-25 09:26:42 UTC

```
[Message from staff account 'staff', not the run's owner]

Keep the paper's structure, headline and every verified number. Make these edits, checking each against the round record:
1) Title: state the R_COMP-SIG result: pre-registered consensus scoring beats single judges on templated sentences with a supplied signature.
2) Abstract: say that R_COMP-SIG was pre-registered and passed, give +0.367 [0.328, 0.404], and say that it holds for templated sentences with a supplied signature.
3) Table 2 and Fig 2: give n = 503/712/689 for the judge-matched rows.
4) Explain the difference between 0.952 and 0.954 (which rows each figure uses).
5) Conclusion, point 3: drop "even when no vocabulary mismatch exists".
```

### [3] ASSISTANT · 2026-09-25 09:26:52 UTC

```
New workspace at `run_Jhw6i0bFXdo3`. Let me check what's there and copy files if needed.
```

### [4] TOOL CALL — Bash · 2026-09-25 09:26:52 UTC

```
Check new workspace contents:
ls -la /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/
```

### [5] TOOL RESULT — Bash · 2026-09-25 09:26:52 UTC

```
{"stdout": "total 2988\ndrwxr-xr-x 4 root root 1009233 Sep 25 09:26 .\ndrwxr-xr-x 3 root root 1009233 Sep 25 09:26 ..\ndrwxr-xr-x 2 root root       1 Sep 25 09:26 .aii\n-rw------- 1 root root      54 Sep 25 09:26 .aii_claude_session.json\n-rw-r--r-- 1 root root   31941 Sep 25 09:26 .repl_agent.ptylog\ndrwxr-xr-x 2 root root 1006121 Sep 25 09:26 figures", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [6] TOOL CALL — Bash · 2026-09-25 09:26:56 UTC

```
Check figures directory:
ls /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/figures/
```

### [7] TOOL RESULT — Bash · 2026-09-25 09:26:56 UTC

```
{"stdout": "fig_complexity_v0.pdf\nfig_dev_auroc_v0.pdf\nfig_k_curve_v0.pdf", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [8] ASSISTANT · 2026-09-25 09:27:04 UTC

```
No paper.tex, references.bib, or the tercile figure. I need to copy them from the previous run.
```

### [9] TOOL CALL — Bash · 2026-09-25 09:27:04 UTC

```
Copy paper.tex, references, and tercile figure from previous run:
cp /ai-inventor/aii_data/runs/run_cNhUBrixEdz7/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.tex /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.tex && cp /ai-inventor/aii_data/runs/run_cNhUBrixEdz7/4_gen_paper_repo/_4_assemble_paper/paper/workspace/references.bib /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/references.bib && cp /ai-inventor/aii_data/runs/run_cNhUBrixEdz7/4_gen_paper_repo/_4_assemble_paper/paper/workspace/references.json /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/references.json && cp /ai-inventor/aii_data/runs/run_cNhUBrixEdz7/4_gen_paper_repo/_4_assemble_paper/paper/workspace/figures/fig_sig_tercile_v0.pdf /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/figures/fig_sig_tercile_v0.pdf && cp /ai-inventor/aii_data/runs/run_cNhUBrixEdz7/4_gen_paper_repo/_4_assemble_paper/paper/workspace/figures/fig_sig_tercile_v0.png /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/figures/fig_sig_tercile_v0.png
```

### [10] TOOL RESULT — Bash · 2026-09-25 09:27:04 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": true}
```

### [11] ASSISTANT · 2026-09-25 09:27:10 UTC

```
Now I need to update the code links from `run_cNhUBrixEdz7` to `run_Jhw6i0bFXdo3`, then apply the 5 staff fixes. Let me first read the paper and check the analysis.json for the tercile n values.
```

### [12] TOOL CALL — Read · 2026-09-25 09:27:10 UTC

```
/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.tex
```

### [13] TOOL RESULT — Read · 2026-09-25 09:27:10 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.tex", "content": "\\documentclass[11pt,letterpaper]{article}\n\\usepackage{graphicx, geometry, amsmath, amssymb, hyperref, url, natbib, booktabs, xcolor, listings}\n\\geometry{margin=1in}\n\\hypersetup{colorlinks=true, linkcolor=black, citecolor=black, urlcolor=black}\n\n\\title{Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric\\\\for Natural-Language-to-First-Order-Logic Translation}\n\n\\author{Anonymous}\n\\date{}\n\n\\begin{document}\n\\maketitle\n\n\\begin{abstract}\nEvaluating the faithfulness of natural-language-to-first-order-logic (NL$\\to$FOL) translations is hampered by the expense and unreliability of gold-standard references: recent audits find that roughly 40\\% of annotations in standard benchmarks contain errors.\nWe study a gold-free alternative based on cross-family solver consensus: collect translations of the same sentence from multiple independent LLM families, check pairwise equivalence with an SMT solver, and score each candidate by the fraction of cross-family peers that disagree with it.\nWhen translators share a supplied predicate vocabulary, consensus achieves a within-template AUROC of 0.954 on 221~fresh long-exception sentences with trusted references and pure Z3 labels, versus 0.587 for a disguised API judge ($\\Delta = +0.367$), flat across word-length terciles.\nUnder free (independently chosen) vocabulary, consensus still outperforms judges on both development data ($\\Delta = +0.099$) and untouched out-of-sample sentences ($\\Delta = +0.171$, original-view judge), but the advantage shrinks by roughly 0.15~AUROC and a fundamental rename tradeoff emerges: any predicate-name alignment needed to compare independently generated formulas produces a high false-alarm rate on meaning-preserving renames.\nConfirmation on independent held-out data was budget-stopped and remains incomplete.\nWe present these results, identify the conditions under which shared versus free vocabulary governs metric strength, and release the full evaluation code.\n\\end{abstract}\n\n\\section{Introduction}\n\nTranslating natural-language sentences into first-order logic (NL$\\to$FOL) is a core task in computational semantics and formal verification~\\citep{Yang2023,Han2022}.\nA correct translation must faithfully capture the meaning of the source sentence: its quantifier scope, polarity, argument structure, and exception clauses.\nEvaluating faithfulness is difficult because the same sentence admits many logically equivalent formalizations that differ in predicate names, variable bindings, and structural layout.\n\nGold-standard references are the default evaluation method, but they are expensive and often wrong.\n\\citet{Brunello2026} audit two standard benchmarks and find 39--42\\% of their annotations contain errors.\nThis unreliability is not just noise: when the gold reference itself is unfaithful, every metric calibrated against it is miscalibrated.\n\nAn alternative is to have a strong LLM judge each translation~\\citep{Chiang2024}.\nHowever, LLM judges share failure modes with the translators they evaluate: both are autoregressive models operating on the same distributional statistics, so systematic blind spots tend to be correlated.\nAs we show in Section~\\ref{sec:sig_results}, a cheap disguised judge achieves only 0.587 AUROC on the same sentences where consensus reaches 0.954.\n\nWe study a gold-free metric based on cross-family solver consensus.\nThe idea is simple: if a candidate translation is correct, translations produced independently by other LLM families should be logically equivalent to it.\nIf the candidate is wrong, independent translators are unlikely to make the same mistake, so their translations will diverge.\nWe formalise this intuition and evaluate it under two vocabulary regimes:\n\\begin{enumerate}\n\\item \\textbf{Shared signature}: all translators use a supplied predicate vocabulary. Equivalence checking requires no alignment and labels come from Z3 alone.\n\\item \\textbf{Free vocabulary}: each translator chooses its own predicate names. Equivalence checking requires a predicate-name aligner, which introduces a rename tradeoff (Section~\\ref{sec:rename}).\n\\end{enumerate}\n\nOur contributions:\n\\begin{itemize}\n\\item A pre-registered evaluation on 221 long-exception sentences under shared signature: consensus AUROC 0.954 versus 0.587 for the disguised judge ($\\Delta = +0.367$ [+0.328, +0.404]), flat across word-length terciles, and 0.956 versus 0.932 for a frontier judge on a descriptive 60-row subsample (Section~\\ref{sec:sig_results}). This dataset later served as development data for aligner tuning; the templates and supplied signature limit its scope.\n\\item Free-vocabulary evaluation on development set~$E$: consensus outperforms judges by $\\Delta = +0.099$ [+0.049, +0.146] on stratified AUROC, with aligner-free consensus (c\\_exact) at 0.689 [0.652, 0.726] (Section~\\ref{sec:dev_results}).\n\\item Untouched free-vocabulary out-of-sample results on R\\_COMP FREE under provisional labels: $\\Delta = +0.171$ [+0.135, +0.206] versus the original-view judge; $\\Delta = +0.105$ [+0.011, +0.215] on a two-auditor subset; consensus reaches 0.94 of the frontier judge's AUROC (Section~\\ref{sec:free_oos}).\n\\item Documentation of the rename tradeoff: a 76.5\\% false-alarm rate under nonce predicate renames that no variant we tested could eliminate without sacrificing error recall (Section~\\ref{sec:rename}).\n\\end{itemize}\n\n\\begin{figure}[!htbp]\n  \\centering\n  \\includegraphics[width=\\linewidth,height=0.85\\textheight,keepaspectratio]{figures/fig_dev_auroc_v0.pdf}\n  \\caption{Stratified AUROC on the free-vocabulary development dataset for the main metrics and baselines. Error bars are 95\\% sentence-cluster bootstrap confidence intervals. Consensus-based metrics (blue) outperform API judges (orange) and other gold-free baselines (gray).}\n  \\label{fig:dev_auroc}\n\\end{figure}\n\n\\section{Related Work}\n\n\\paragraph{NL\\texorpdfstring{$\\to$}{-to-}FOL evaluation.}\nStandard benchmarks such as FOLIO~\\citep{Han2022} and the MALLS corpus~\\citep{Yang2023} provide NL--FOL pairs, but gold-annotation error rates are high~\\citep{Brunello2026}.\n\\citet{Vossel2025} map predicates by normalised Levenshtein distance before equivalence checking.\n\\citet{Thatikonda2025} evaluate n-gram, graph, embedding, and LLM-based closeness metrics on controlled FOL perturbations, finding that no single metric is sensitive to all perturbation types.\n\n\\paragraph{Cross-model consensus.}\nThe idea of using agreement among multiple independently trained models as a quality signal appears in several domains.\n\\citet{Wang2022} show that sampling multiple chain-of-thought reasoning paths~\\citep{Wei2022} from a single model and taking the majority answer (self-consistency) improves accuracy.\n\\citet{Bayless2025} collect $k$ translations over a fixed shared schema and score each by the fraction of $k$ translations that entail it.\n\\citet{Zhang2023} detect hallucinations in black-box LLMs by sampling diverse perturbations of a query and checking consistency across answers.\nOur work differs from these in evaluating the consensus score under both shared and free vocabulary, head-to-head with API judges, with pre-registered analyses.\n\n\\paragraph{LLM-as-judge.}\n\\citet{Chiang2024} propose using LLMs as evaluators.\nIn NL$\\to$FOL, an LLM judge reads the sentence and the candidate formula and predicts faithfulness.\nThe disguised variant (nonce predicate names) controls for memorisation of known benchmarks.\n\n\\paragraph{Diverse redundancy.}\nN-version programming, where independent implementations of the same specification are compared by majority vote, was proposed for software fault tolerance.\n\\citet{Eckhardt1985} predict that coincident failures rise with input difficulty; our finding that the consensus advantage is flat with sentence length under shared vocabulary but degrades under free vocabulary is consistent with vocabulary alignment, not input difficulty, as the bottleneck.\n\n\\section{Method}\\label{sec:method}\n\n\\subsection{Consensus scoring}\n\nGiven a sentence $s$ and a candidate FOL translation $c$, we collect peer translations $\\{p_1, \\ldots, p_k\\}$ from $k$ independent LLM families.\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-1/experiment-1}}\nEach peer uses the same few-shot prompt but a different base model (e.g., one from each of Gemini, Claude, GPT, Llama, Qwen, Phi, Mistral).\nWe compute:\n\\begin{equation}\n\\text{c\\_score}(c, s) = 1 - \\frac{1}{k} \\sum_{i=1}^{k} \\mathbf{1}[\\text{equiv}(c, p_i)]\n\\end{equation}\nwhere $\\text{equiv}(c, p_i)$ checks logical equivalence between $c$ and $p_i$ using the Z3 SMT solver~\\citep{Moura2008}.\n\nUnder \\textbf{shared signature} (c\\_score\\_sig), all translators use a supplied predicate vocabulary, and equiv is a direct Z3 check after case-insensitive symbol normalisation.\nUnder \\textbf{free vocabulary} (c\\_score\\_align), each translator chooses its own predicate names, and equiv requires a predicate-name aligner before the Z3 check.\n\n\\subsection{Predicate alignment (free vocabulary only)}\n\nIndependent translators choose different predicate names for the same concept (e.g., \\texttt{Runs(x)} vs.\\ \\texttt{IsRunner(x)}).\nTo compare formulas across families, we align predicates using a cost function that combines:\n\\begin{enumerate}\n\\item \\textbf{Structural cost}: polarity profile, argument-count match, and nesting depth.\n\\item \\textbf{Text-anchor cost}: overlap between predicate-name words and source-sentence tokens (Porter stemming, WordNet synonyms/derivations).\n\\item \\textbf{Semantic signature}: truth-value profiles over random finite interpretations.\n\\end{enumerate}\nThe $k$ cheapest bijections (predicates within equal arity; constants separately) are evaluated, and the pair is declared equivalent if any bijection yields a Z3-verified equivalence.\n\n\\subsection{Score variants}\n\nHigher scores indicate greater divergence from peers and thus higher predicted error probability.\nVariants include:\n\\begin{itemize}\n\\item \\textbf{c\\_exact}: no alignment; exact-match equivalence only. Immune to rename false alarms but blind to vocabulary-differing equivalences.\n\\item \\textbf{c\\_nf} (name-free): alignment by structural and semantic signatures only, ignoring text anchoring.\n\\item \\textbf{p\\_peer\\_text}: a logistic fusion of consensus features with text-side features (bag-of-words coverage, role accounting, Z3 structural match).\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-2/experiment-5}}\n\\end{itemize}\n\n\\subsection{Evaluation framework}\n\n\\paragraph{Shared-signature labels.}\nOn R\\_COMP, labels are determined by Z3 equivalence to trusted-by-construction references (one weak and one strong reading per template), with no human or LLM judgement in the labelling loop.\n\n\\paragraph{Free-vocabulary labels.}\nOn development set~$E$, labels come from a three-person expert panel (adjudicated as ERROR or CORRECT), with disputed items counted according to the reliability assignment (R\\_AB: both panellists agree).\nOn R\\_COMP FREE, provisional labels use search-based ERROR\\_CERT versus MAPPED classifications (non-confirmatory; the gloss-based labelling gate failed twice).\n\n\\paragraph{Metrics.}\nThe primary evaluation metric is stratified AUROC: items are paired only within the same source stratum (sentence-template on R\\_COMP, sentence-complexity bin on~$E$), eliminating confounds from stratum-level base rates.\nConfidence intervals use sentence-cluster percentile bootstrap ($B = 2{,}000$).\n\n\\section{Experiments}\\label{sec:experiments}\n\n\\subsection{Datasets}\n\n\\paragraph{R\\_COMP (shared and free vocabulary).}\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/experiment-7}}\nR\\_COMP generates long, complex sentences ($\\geq$25 words, 4--5 conditions) from a verified lexicon.\n221~sentences produced 2,024 candidate translations from 10~LLM slots across 9~vendor families.\nPopulation: 429~ERROR~/~1,595~CORRECT (21.2\\% error rate).\nIn the \\textbf{SIG condition}, all translators received a supplied predicate signature; labels are pure Z3 equivalence to trusted references.\nIn the \\textbf{FREE condition}, each translator chose its own predicate names; labels are provisional (Section~\\ref{sec:free_oos}).\nThe pre-registration document, including the analysis plan and testability rule, was frozen before any SIG generation call, any label, or any metric score.\\footnote{Pre-registration: \\texttt{prereg\\_sig.json}, SHA-256 frozen before data collection.}\n\n\\paragraph{Development set $E$.}\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-1/experiment-3}}\n8,507~rows from 700~sentences drawn from the MALLS corpus~\\citep{Yang2023} and ProverQA~\\citep{Qi2025}.\nEach sentence was translated by 9~LLM families using a frozen few-shot prompt.\nThe primary evaluation population (R\\_AB, both panellists agree) contains 2,686~items (1,822~ERROR~/~864~CORRECT, 292~sentences); the all-families subset where every peer family contributed a translation is $n = 2{,}014$.\nComplexity strata: L25 ($\\geq$25 words), L20 (20--24), EXC (exception clauses), CTRL (short control sentences).\nThe R\\_COMP-SIG data later served as development data for aligner tuning, so the development-set numbers from $E$ are not independent of R\\_COMP.\n\n\\paragraph{Baselines.}\n(1)~\\textbf{Flash-lite judge} (Gemini Flash Lite, disguised and original views); (2)~\\textbf{nano judge} (Gemini Flash 2.0); (3)~\\textbf{local judges} (Qwen3-8B, Llama-8B); (4)~\\textbf{round-trip NLI}; (5)~\\textbf{self-consistency} (5-sample within-model agreement); (6)~\\textbf{structural features} (arity consistency, dangling predicates, rerun Jaccard); (7)~\\textbf{feature stacks}: cross-validated logistic regressions over subsets of these features.\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-1/experiment-4}}\n\n\\subsection{Shared-signature results (R\\_COMP-SIG)}\\label{sec:sig_results}\n\nTable~\\ref{tab:sig} reports the pre-registered comparison on R\\_COMP under shared signature.\nOn the 1,904~rows where both consensus and judge scores exist, consensus achieves a within-template AUROC of 0.954 versus 0.587 for the disguised flash-lite judge ($\\Delta = +0.367$ [+0.328, +0.404]).\nAgainst the original-view judge (1,932~rows), the advantage is $\\Delta = +0.278$ [+0.239, +0.319].\nError endorsement is zero ($e = 0$): no error item scores below the decision threshold.\nAmong the 429~error items, 75.3\\% receive the maximum consensus score of~1.0; the remaining 24.7\\% score between 0.625 and~1.0.\n\n\\begin{table}[!htbp]\n\\centering\n\\caption{Within-template AUROC on R\\_COMP-SIG (shared signature, 221~sentences, pure Z3 labels). CIs are 95\\% sentence-cluster bootstrap.}\n\\label{tab:sig}\n\\small\n\\begin{tabular}{lccc}\n\\toprule\nMetric & $n$ & Within-template AUROC [95\\% CI] & $\\Delta$ vs.\\ disg.\\ judge [95\\% CI] \\\\\n\\midrule\nc\\_score\\_sig & 1904 & 0.954 [0.939, 0.968] & +0.367 [+0.328, +0.404] \\\\\nc\\_score\\_align & 1904 & 0.954 [0.939, 0.968] & +0.367 [+0.328, +0.404] \\\\\njudge (flash-lite, disg.) & 1904 & 0.587 [0.551, 0.622] & --- \\\\\njudge (flash-lite, orig.) & 1932 & 0.673 [0.637, 0.708] & \\\\\njudge (frontier, orig.) & 60 & 0.932 [0.782, 1.000] & \\\\\njudge (local, disg.) & 2024 & 0.498 [0.459, 0.534] & \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}\n\n\\paragraph{Flat with sentence length.}\nUnlike the free-vocabulary setting (Section~\\ref{sec:mechanism}), consensus under shared signature is flat across word-length terciles: W1 0.959, W2 0.947, W3 0.953 (Table~\\ref{tab:sig_complexity} and Figure~\\ref{fig:sig_tercile}).\n\n\\begin{table}[!htbp]\n\\centering\n\\caption{R\\_COMP-SIG within-template AUROC by word-length tercile.}\n\\label{tab:sig_complexity}\n\\small\n\\begin{tabular}{lccccc}\n\\toprule\nTercile & $n$ & ERR/COR & c\\_sig & judge (disg.) & $\\Delta$ [CI] \\\\\n\\midrule\nW1 (shortest) & 574 & 125/449 & 0.959 & 0.578 & +0.382 [+0.278, +0.472] \\\\\nW2 & 743 & 149/594 & 0.947 & 0.624 & +0.331 [+0.253, +0.421] \\\\\nW3 (longest) & 707 & 155/552 & 0.953 & 0.567 & +0.388 [+0.301, +0.471] \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}\n\n\\begin{figure}[!htbp]\n  \\centering\n  \\includegraphics[width=\\linewidth,height=0.85\\textheight,keepaspectratio]{figures/fig_sig_tercile_v0.pdf}\n  \\caption{Within-template AUROC on R\\_COMP-SIG by word-length tercile. Consensus (blue) is flat across terciles (0.947--0.959), while the disguised flash-lite judge (orange) hovers near chance (0.567--0.624). Error bars are 95\\% sentence-cluster bootstrap CIs.}\n  \\label{fig:sig_tercile}\n\\end{figure}\n\n\\paragraph{Frontier judge comparison.}\nOn a descriptive 60-row stratified subsample scored by the frontier judge (Gemini~3.1~Pro, original view), consensus achieves pooled AUROC 0.956 [0.889, 1.000] versus 0.932 [0.855, 0.990] for the frontier judge.\n\n\\paragraph{Scope.}\nR\\_COMP-SIG uses templated sentences with a supplied predicate vocabulary.\nThe shared signature eliminates the alignment problem entirely, which is why the AUROC is so high.\nThese results do not extend to settings where translators choose their own predicate names.\n\n\\subsection{Free-vocabulary development results (set $E$)}\\label{sec:dev_results}\n\nFigure~\\ref{fig:dev_auroc} and Table~\\ref{tab:main} summarise the free-vocabulary comparison on development set~$E$.\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/experiment-6}}\nCross-family consensus (c\\_score\\_align) outperforms the disguised flash-lite judge by $\\Delta = +0.099$ [+0.049, +0.146] on the full R\\_AB population and by $\\Delta = +0.116$ [+0.070, +0.163] on the long-sentence pool (L25+L20+EXC).\nAdding c\\_score\\_align to the 28-feature baseline stack increases stratified AUROC by +0.039 [+0.021, +0.057]; a permutation null test gives $p_{95} = 0.009$, confirming the signal is not explained by the existing features.\n\n\\begin{table}[!htbp]\n\\centering\n\\caption{Stratified AUROC on development set $E$ (R\\_AB population, free vocabulary, $n = 2{,}686$). Higher is better. CIs are 95\\% sentence-cluster bootstrap.}\n\\label{tab:main}\n\\small\n\\begin{tabular}{lcc}\n\\toprule\nMetric & Strat AUROC [95\\% CI] & \\$/item \\\\\n\\midrule\nc\\_score\\_align & 0.741 [0.705, 0.775] & 9.1e-5 \\\\\np\\_peer\\_text (fused) & 0.753 [0.720, 0.784] & 9.1e-5 \\\\\nc\\_exact (no alignment) & 0.689 [0.652, 0.726] & -- \\\\\nc\\_nf (name-free) & 0.686 [0.647, 0.720] & -- \\\\\n\\midrule\nflash-lite judge (disg.) & 0.642 [0.607, 0.676] & 5.1e-5 \\\\\nflash-lite judge (orig.) & 0.623 [0.593, 0.651] & 5.1e-5 \\\\\nnano judge (disg.) & 0.644 [0.609, 0.680] & 2.0e-5 \\\\\nlocal judge Qwen-8B (disg.) & 0.674 [0.646, 0.703] & -- \\\\\n\\midrule\nround-trip NLI (min) & 0.606 [0.569, 0.645] & 2.8e-5 \\\\\nself-consistency (5-sample) & 0.598 [0.559, 0.637] & 6.7e-5 \\\\\n\\midrule\n28-feature stack & 0.735 [0.699, 0.766] & -- \\\\\n28-feature stack + c\\_score\\_align & 0.774 [0.743, 0.802] & -- \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}\n\nThe drop from 0.952 (shared signature, R\\_COMP-SIG) to 0.801 (free vocabulary on the same R\\_COMP sentences) reflects the cost of predicate-name alignment: the aligner introduces both false negatives (correct equivalences missed) and false positives (incorrect mappings endorsed).\nAligner-free consensus (c\\_exact) achieves 0.689 [0.652, 0.726]; the aligner adds about 22\\% of the above-chance signal (c\\_align 0.241 versus c\\_exact 0.189 above the 0.5 baseline), with the remaining 78\\% coming from structural agreement alone.\n\nOn L25 sentences alone ($\\geq$25 words), the advantage narrows to $\\Delta = +0.069$ [$-$0.020, +0.148], not significant at the 95\\% level.\nThis foreshadows the length-dependent degradation described in Section~\\ref{sec:mechanism}.\n\n\\paragraph{Frontier judge comparison.}\nOn the 284-row subsample scored by the frontier judge (Gemini~3.1~Pro), c\\_score\\_align achieves 95.7\\% of the frontier judge's AUROC (ratio 0.957 [0.887, 1.034]).\n\n\\paragraph{System-level ranking.}\nThe consensus metric achieves Kendall $\\tau_b = 0.692$ [+0.513, +0.795] between system mean score and R\\_AB error rate across 13 system$\\times$variant configurations, comparable to the best judges.\n\n\\subsection{Free-vocabulary out-of-sample (R\\_COMP FREE)}\\label{sec:free_oos}\n\nThe same 221~R\\_COMP sentences were also translated under free vocabulary (each translator choosing its own predicate names).\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-5/experiment-13}}\nConfirmatory labelling required a gloss gate (LLM-checked semantic alignment of predicate mappings).\nThis gate failed twice (balanced accuracy 0.776 and 0.561, below the 0.90 threshold), producing zero confirmed CORRECT rows and rendering the confirmatory test not testable.\n\nUnder provisional non-confirmatory labels (ERROR\\_CERT vs.\\ MAPPED, where MAPPED is an upper bound on CORRECT), Table~\\ref{tab:free} reports the untouched results.\n\n\\begin{table}[!htbp]\n\\centering\n\\caption{R\\_COMP FREE provisional AUROCs (within-template, untouched rows). Labels are non-confirmatory.}\n\\label{tab:free}\n\\small\n\\begin{tabular}{lccc}\n\\toprule\nView & $n$ (ERR/MAPPED) & c\\_align & judge \\\\\n\\midrule\nDisguised & 1706 (602/1104) & 0.801 [0.770, 0.834] & 0.584 [0.550, 0.618] \\\\\nOriginal & 1709 (605/1104) & 0.804 [0.774, 0.836] & 0.633 [0.601, 0.666] \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}\n\nThe disguised-judge delta is $+0.217$ [+0.175, +0.260]; the original-view delta is $+0.171$ [+0.135, +0.206].\nOn a 146-row subset with independent two-auditor labels, consensus achieves $\\Delta = +0.105$ [+0.011, +0.215] over the original-view judge.\nOn a 150-row frontier-judge subsample, consensus reaches 0.94 of the frontier judge's AUROC (ratio 0.940 [0.825, 1.056]).\n\nThese provisional numbers cannot count as confirmation because the MAPPED labels conflate vocabulary-alignment failures with genuine correctness.\nThey are consistent with the development-set signal but independent confirmation requires a working gloss gate or a different labelling strategy.\n\n\\subsection{Mechanism}\\label{sec:mechanism}\n\nWe decompose the consensus signal\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/evaluation-2}} into two components at a fixed decision threshold:\n\\begin{itemize}\n\\item \\textbf{Endorsement} $e$: fraction of ERROR items endorsed by the peer majority (false negatives of consensus).\n\\item \\textbf{Divergence} $d$: fraction of CORRECT items that diverge from the peer majority (false positives of consensus).\n\\end{itemize}\nThe consensus AUROC at a binary threshold equals $1 - (e + d)/2$, so both quantities must be small for the metric to work.\n\n\\paragraph{Shared vocabulary: endorsement zero, divergence moderate.}\nOn R\\_COMP-SIG, $e = 0.0$ and $d = 0.260$: no error escapes detection, though 26\\% of correct translations are flagged as divergent.\nThe false-alarm rate of 0.260 arises from correct translations that use valid but structurally different formalizations; because all translators share a predicate vocabulary, no alignment step is needed and the divergence rate is flat across sentence lengths.\n\n\\paragraph{Free vocabulary: divergence degrades with length.}\nAs Figure~\\ref{fig:complexity} shows, on development set~$E$ the net consensus degradation from short to long sentences is $\\Delta(e+d) = +0.356$ [+0.198, +0.493], driven almost entirely by divergence ($\\Delta d = +0.608$, $\\Delta e = -0.252$): as formulas grow longer and more structurally diverse, the predicate-name aligner (Section~\\ref{sec:rename}) increasingly maps distinct predicates together or fails to match equivalent ones, inflating the false-alarm rate on correct translations.\n\n\\begin{figure}[!htbp]\n  \\centering\n  \\includegraphics[width=\\linewidth,height=0.85\\textheight,keepaspectratio]{figures/fig_complexity_v0.pdf}\n  \\caption{Decomposition of free-vocabulary consensus error rates by sentence-length tercile on development set~$E$. Endorsement rate $e$ (errors incorrectly endorsed by peers) decreases with length, but divergence rate $d$ (correct items incorrectly flagged) increases sharply, producing net degradation of +0.356 from the shortest to the longest tercile. Under shared signature (R\\_COMP-SIG), this degradation is absent.}\n  \\label{fig:complexity}\n\\end{figure}\n\n\\paragraph{Family sufficiency.}\nThree peer families suffice for 97\\% of full-pool AUROC ($k_{95} = 3$), but the long-sentence tercile requires $k_{95} = 5$ (Table~\\ref{tab:k_families} and Figure~\\ref{fig:k_curve}).\n\n\\begin{table}[!htbp]\n\\centering\n\\caption{Free-vocabulary AUROC by number of peer families on development set $E$.}\n\\label{tab:k_families}\n\\small\n\\begin{tabular}{ccc}\n\\toprule\n$k$ & AUROC (overall) & AUROC (long, T3) \\\\\n\\midrule\n1 & 0.685 & 0.581 \\\\\n3 & 0.757 & 0.651 \\\\\n5 & 0.776 & 0.698 \\\\\n7 & 0.784 & 0.726 \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}\n\n\\begin{figure}[!htbp]\n  \\centering\n  \\includegraphics[width=\\linewidth,height=0.85\\textheight,keepaspectratio]{figures/fig_k_curve_v0.pdf}\n  \\caption{Stratified AUROC as a function of the number of peer families $k$, for the full development set (solid blue) and the long-sentence tercile (dashed red). Three families capture 97\\% of the full-pool signal, but long sentences require five families to reach 95\\%.}\n  \\label{fig:k_curve}\n\\end{figure}\n\n\\subsection{Confirmation status}\\label{sec:confirmation}\n\nIndependent confirmation on held-out data remains incomplete.\nA fresh held-out dataset (E2-A, 550~new sentences) was constructed, but the run-level budget was exhausted before enough items could be labelled.\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-4/dataset-4}}\nOn the one testable stratum (DT, short sentences from ProverQA), consensus achieves a stratified AUROC of 0.916, tying the local Qwen-8B judge ($\\Delta = +0.003$ [$-$0.042, +0.052]).\nOn L25 sentences, c\\_score\\_align falls to 0.443 on only 42 items (35~ERROR~/~7~CORRECT), below chance, but the estimate has extreme variance with only 7~CORRECT items from 3~sentences.\nEvery pre-registered criterion on the target strata returned NOT\\_TESTABLE or unfavourable.\n\n\\subsection{The rename tradeoff}\\label{sec:rename}\n\nThe predicate aligner\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/experiment-8}} that enables cross-family comparison under free vocabulary also introduces a fundamental false-alarm vulnerability.\nWhen correct formulas are copied with meaning-preserving predicate renames (same semantics, different symbol names), the consensus score should not change.\nTable~\\ref{tab:rename} shows the false-alarm rates in practice.\n\n\\begin{table}[!htbp]\n\\centering\n\\caption{False-alarm (FA) rates on meaning-preserving renames of CORRECT candidates. NONCE = random nonsense names; SYN = WordNet synonyms. Flip = FA induced by the rename alone (FA minus base FA).}\n\\label{tab:rename}\n\\small\n\\begin{tabular}{lcccc}\n\\toprule\nMetric & NONCE FA & NONCE flip & SYN FA & SYN flip \\\\\n\\midrule\nc\\_align & 0.765 & 0.605 & 0.565 & 0.313 \\\\\nc\\_nf (name-free) & 0.132 & 0.000 & 0.201 & 0.000 \\\\\np\\_peer\\_text & 1.000 & 0.821 & 0.216 & 0.080 \\\\\njudge (disg.) & 0.229 & 0.134 & 0.085 & 0.058 \\\\\n\\bottomrule\n\\end{tabular}\n\\end{table}\n\nThe name-free variant c\\_nf eliminates rename sensitivity (flip = 0) but at the cost of blindness to meaning-rename errors (within-base AUROC 0.499, chance level) and lower overall discrimination (strat AUROC 0.686 vs.\\ 0.741).\nThis tradeoff explains the gap between shared-signature and free-vocabulary performance: the shared signature eliminates the need for alignment entirely, sidestepping the rename problem.\n\n\\subsection{Per-type sensitivity}\n\nOn the PERTURB suite (4,234 typed mutants + 868 controls from development data), consensus recall at the primary threshold is flat across error operators: NEG 0.761, SWAP 0.758, DROP 0.721, ADD 0.763, MEANING\\_RENAME 0.762.\nPer-operator AUROC within error types cannot be computed because 94--100\\% of mutants receive the maximum consensus score, a ceiling effect of the endorsement structure.\n\nError typing outside a shared vocabulary is negative: the free-vocabulary typing accuracy is 0.123 [0.081, 0.169] on $E$, below both the judge (0.326) and the peer-medoid baseline (0.328), and all three are near chance for a five-class task.\n\n\\subsection{Dead ends}\n\nSeveral alternatives were investigated and abandoned during development: a fused structural-feature filter (false-alarm gate failure); name-free consensus c\\_nf (rename-invariant but blind to meaning-rename errors, as described in Section~\\ref{sec:rename}); a decomposed solver-based semantic reader (balanced accuracy 0.476); LLM adjudication of disputed items (balanced accuracy 0.662 on expert-labelled items); and candidate-signature consensus, which scores candidates by cueing peers with the candidate's own predicate symbols rather than letting them choose independently (provisional negative: error endorsement rose to 0.459 because peers were anchored into reproducing the candidate's errors).\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-4/experiment-9}}\n\n\\section{Discussion}\n\n\\subsection{Shared versus free vocabulary}\n\nThe central finding is that vocabulary regime governs metric strength.\nUnder shared signature, consensus achieves near-perfect discrimination (0.954 AUROC) flat across sentence lengths.\nUnder free vocabulary, performance drops by roughly 0.15~AUROC on comparable sentences (R\\_COMP-SIG 0.952 versus R\\_COMP FREE 0.801, both within-template on long composed sentences) and degrades with sentence length on natural data.\n\nThis gap is explained by the rename tradeoff: the predicate-name aligner needed for free-vocabulary comparison introduces both false negatives (missed equivalences) and false positives (spurious mappings), and these grow worse as formulas become longer and more structurally diverse.\nThe practical implication is that consensus-based evaluation is most reliable when translators share a predicate vocabulary, as in controlled evaluation settings~\\citep{Bayless2025,Vossel2025}.\n\n\\subsection{Why confirmation is incomplete}\n\nThe confirmation attempt was defeated by two independent problems: (1)~insufficient fresh data (the E2-A budget was stopped before enough correct items accumulated in the long-sentence strata), and (2)~a broken labelling gate (the gloss-based semantic alignment required for R\\_COMP FREE labels failed quality checks twice).\nNeither failure refutes the development-set signal, but neither allows us to confirm it on the target strata.\n\nThe E2-A L25 result (AUROC 0.443, near chance, on 42~items) is concerning but difficult to interpret: with only 7~CORRECT items from 3~sentences, the estimate has extreme variance and a single sentence can dominate.\nWe report it for completeness but note that it does not meet any standard testability criterion.\n\n\\subsection{The rename tradeoff as a fundamental limit}\n\nThe rename tradeoff is not a bug in our aligner but a structural property of cross-family consensus under independent vocabulary.\nAny alignment procedure that maps independently chosen predicate names to a common vocabulary will sometimes map semantically distinct predicates together, endorsing meaning-rename errors.\nEliminating the alignment (c\\_exact, c\\_nf) preserves rename invariance but sacrifices the structural comparison that drives error detection.\n\nWe conjecture that resolving this tradeoff requires either (a)~a shared predicate vocabulary supplied to all translators, which eliminates the problem entirely but restricts the evaluation to controlled settings~\\citep{Bayless2025,Vossel2025}, or (b)~a semantic disambiguation step (such as natural-language glosses of each predicate) that could break the alignment ambiguity.\nOur attempt at option~(b), a gloss gate using LLM-generated explanations of predicate meanings, failed quality checks, leaving this direction open.\n\n\\subsection{Limitations}\\label{sec:limitations}\n\n\\begin{enumerate}\n\\item \\textbf{Shared-signature scope.} The 0.954 AUROC result uses templated sentences with a supplied predicate vocabulary, which eliminates the alignment problem. The templates and the supplied signature limit the scope of this result to controlled evaluation settings.\n\\item \\textbf{Development data overlap.} The R\\_COMP-SIG dataset later served as development data for aligner tuning. The pre-registration ensures the SIG result itself is uncontaminated, but the development-set numbers from $E$ are not independent.\n\\item \\textbf{Rename vulnerability.} Under free vocabulary, a 76.5\\% false-alarm rate on nonce renames means the metric will systematically penalise any translation that uses non-standard predicate names, even if semantically correct.\n\\item \\textbf{Length degradation (free vocabulary).} Consensus discrimination degrades with sentence length under free vocabulary (NET $+0.356$), driven by correct-translation divergence. The metric is weakest on the longest, most complex sentences, precisely the cases where gold-free evaluation is most needed.\n\\item \\textbf{Provisional labels.} R\\_COMP FREE results use provisional (non-confirmatory) labels; the two-auditor subset ($\\Delta = +0.105$) has a CI that barely excludes zero.\n\\item \\textbf{Label dependence.} Development results on~$E$ depend on a three-person panel whose agreement is imperfect (disputed items exist in every stratum). The metric's advantage could partly reflect alignment with panel biases rather than with ground-truth faithfulness.\n\\item \\textbf{Cost.} The consensus metric requires generating $k$ peer translations per sentence. In this experiment ($k = 9$, R\\_COMP-SIG), the amortised consensus cost per candidate is about 19 times the cost of a single cheap judge call.\n\\item \\textbf{Domain.} All results are on English$\\to$FOL from MALLS, ProverQA, and R\\_COMP sources. Generalisation to other logic formalisms, languages, or sentence distributions is untested.\n\\end{enumerate}\n\n\\section{Conclusion}\n\nCross-family solver consensus is a strong gold-free faithfulness metric for NL$\\to$FOL translation when translators share a predicate vocabulary.\nThe pre-registered R\\_COMP-SIG result (AUROC 0.954 versus 0.587 for a disguised judge, flat with length) establishes the ceiling; free vocabulary costs roughly 0.15~AUROC and introduces the rename tradeoff.\n\nUnder free vocabulary, consensus still outperforms cheap LLM judges on both development data ($+0.099$) and untouched out-of-sample sentences ($+0.171$), and adds information beyond structural and statistical baselines.\nThe mechanism --- errors scatter while correct translations cluster --- provides an intuitive explanation grounded in the diversity of independent formalizations.\n\nHowever, independent confirmation on held-out data was budget-stopped and remains incomplete, the rename tradeoff limits applicability to free-vocabulary settings, and discrimination degrades with sentence length under free vocabulary.\nWe release the full evaluation code and data to enable reproduction.\nThe immediate open problems are: (1)~completing the fresh-data confirmation with adequate sample sizes; (2)~breaking the rename tradeoff, perhaps through semantic predicate glossing; and (3)~understanding why correct translations of complex sentences diverge under free vocabulary even when no vocabulary mismatch exists.\n\n\\bibliographystyle{plainnat}\n\\bibliography{references}\n\n\\end{document}\n", "numLines": 444, "startLine": 1, "totalLines": 444}}
```

### [14] ASSISTANT · 2026-09-25 09:27:28 UTC

```
Good, I have the full paper. Let me check analysis.json for the 0.952 vs 0.954 distinction and the judge-matched tercile n values.
```

### [15] TOOL CALL — Bash · 2026-09-25 09:27:28 UTC

```
Check analysis.json for 0.952 vs 0.954 and tercile n values:
python3 -c "
import json
with open('/ai-inventor/aii_data/runs/run_-tTYmHVAOMOt/4_gen_paper_repo/_repo_clone/round-3/experiment-7/src/results/analysis.json') as f:
    d = json.load(f)

# Primary result
p = d['primary']
print('=== PRIMARY (n=1904) ===')
print(f'n={p[\"n\"]}, AUROC metric={p[\"auroc_metric\"]}, comparator={p[\"auroc_comparator\"]}')

# Full pool
print()
print('=== FULL POOL ===')
fp = d.get('full_pool', {})
print(f'full_pool: {json.dumps(fp, indent=2)[:500]}')

# Check for 0.952 - search for it
print()
print('=== SEARCHING FOR 0.952 ===')
import re
text = json.dumps(d)
# Find context around 0.952
for m in re.finditer(r'0\.952', text):
    start = max(0, m.start()-80)
    end = min(len(text), m.end()+80)
    print(f'...{text[start:end]}...')
    print()

# Word tercile data
print('=== WORD TERCILE ===')
wt = d['complexity']['word_tercile']
for k, v in wt.items():
    print(f'{k}: n_consensus={v.get(\"n\")}, n_judge={v.get(\"n_judge\", \"?\")}, auroc_sig={v.get(\"auroc_sig\", v.get(\"auroc_metric\", \"?\"))}, auroc_judge={v.get(\"auroc_comparator\", \"?\")}')
" 2>&1 | head -50
```

### [16] TOOL RESULT — Bash · 2026-09-25 09:27:28 UTC

```
{"stdout": "Traceback (most recent call last):\n  File \"<string>\", line 7, in <module>\nKeyError: 'primary'", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [17] TOOL CALL — Bash · 2026-09-25 09:27:32 UTC

```
Check top-level keys of analysis.json:
python3 -c "
import json
with open('/ai-inventor/aii_data/runs/run_-tTYmHVAOMOt/4_gen_paper_repo/_repo_clone/round-3/experiment-7/src/results/analysis.json') as f:
    d = json.load(f)
print('Top keys:', list(d.keys()))
" 2>&1
```

### [18] TOOL RESULT — Bash · 2026-09-25 09:27:32 UTC

```
{"stdout": "Top keys: ['generated_utc', 'B', 'seed', 'orientation', 'SIG', 'FREE', 'runtime_s']", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [19] TOOL CALL — Bash · 2026-09-25 09:27:40 UTC

```
Explore SIG section of analysis.json:
python3 -c "
import json
with open('/ai-inventor/aii_data/runs/run_-tTYmHVAOMOt/4_gen_paper_repo/_repo_clone/round-3/experiment-7/src/results/analysis.json') as f:
    d = json.load(f)

sig = d['SIG']
print('SIG keys:', list(sig.keys()))
print()

# Primary
p = sig.get('primary', {})
print('=== SIG PRIMARY ===')
print(json.dumps(p, indent=2)[:800])

# Full pool
print()
fp = sig.get('full_pool', {})
print('=== SIG FULL_POOL ===')
print(json.dumps(fp, indent=2)[:500])
" 2>&1
```

### [20] TOOL RESULT — Bash · 2026-09-25 09:27:40 UTC

```
{"stdout": "SIG keys: ['guard', 'counts', 'primary', 'secondary', 'auroc_table', 'nested', 'frontier', 'operating_points', 'per_template_labels', 'per_clause_labels', 'per_slot_labels', 'matched_reading_by_template', 'T8_reading_choice_rate', 'off_signature_rate_by_slot', 'unparseable_rate_by_slot', 'error_rate_by_slot', 'per_template_auroc', 'per_clause_type_auroc', 'complexity', 'mechanism_sig', 'rename_invariance', 'coverage_view', 'off_signature_rows', 'contamination', 'placebos', 'cost', 'system_level', 'error_types', 'judge_coverage', 'disguise_failures']\n\n=== SIG PRIMARY ===\n{\n  \"n\": 1904,\n  \"n_error\": 395,\n  \"n_correct\": 1509,\n  \"n_sentences\": 220,\n  \"metric\": \"c_score_sig\",\n  \"comparator\": \"judge_cheap_disg\",\n  \"stratum\": \"template\",\n  \"auroc_metric\": 0.954340046099721,\n  \"auroc_comparator\": 0.5872179424966638,\n  \"auroc_metric_ci\": [\n    0.938804516329619,\n    0.9675579765338935\n  ],\n  \"auroc_comparator_ci\": [\n    0.5506554176040529,\n    0.6223051009309785\n  ],\n  \"delta\": 0.3671221036030572,\n  \"ci\": [\n    0.32842452732411576,\n    0.40401256613475645\n  ],\n  \"se\": 0.019400210076362823,\n  \"p_one_sided\": 0.0,\n  \"ci_lower_gt_0\": true,\n  \"PASS\": true,\n  \"n_excluded_judge_missing\": 120,\n  \"n_excluded_consensus_missing\": 0\n}\n\n=== SIG FULL_POOL ===\n{}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] TOOL CALL — Bash · 2026-09-25 09:27:48 UTC

```
Find 0.952 in SIG and check word_tercile structure:
python3 -c "
import json
with open('/ai-inventor/aii_data/runs/run_-tTYmHVAOMOt/4_gen_paper_repo/_repo_clone/round-3/experiment-7/src/results/analysis.json') as f:
    d = json.load(f)

sig = d['SIG']

# Search for 0.952
import re
text = json.dumps(sig)
print('=== Searching for 0.952 in SIG ===')
for m in re.finditer(r'0\.95[12]', text):
    start = max(0, m.start()-100)
    end = min(len(text), m.end()+100)
    print(f'...{text[start:end]}...')
    print()

# Word tercile
print('=== COMPLEXITY ===')
comp = sig['complexity']
print('Complexity keys:', list(comp.keys()))
wt = comp.get('word_tercile', {})
print()
for k, v in wt.items():
    print(f'{k}: {json.dumps(v, indent=2)[:400]}')
    print()
" 2>&1 | head -80
```

### [22] TOOL RESULT — Bash · 2026-09-25 09:27:48 UTC

```
{"stdout": "=== Searching for 0.952 in SIG ===\n..., \"metric\": \"c_score_sig\", \"comparator\": \"judge_cheap_disg\", \"stratum\": \"sentence\", \"auroc_metric\": 0.9517106972715461, \"auroc_comparator\": 0.5827197921177999, \"auroc_metric_ci\": [0.9332325036030408, 0.967...\n\n..., \"metric\": \"c_score_sig\", \"comparator\": \"judge_cheap_orig\", \"stratum\": \"template\", \"auroc_metric\": 0.9516325771662328, \"auroc_comparator\": 0.6734845667534399, \"auroc_metric_ci\": [0.9362744807503232, 0.964...\n\n..., \"metric\": \"c_score_sig\", \"comparator\": \"judge_local_disg\", \"stratum\": \"template\", \"auroc_metric\": 0.9518311681453316, \"auroc_comparator\": 0.4975377587663709, \"auroc_metric_ci\": [0.9366407499189088, 0.965...\n\n..., \"metric\": \"c_score_hyb\", \"comparator\": \"judge_cheap_disg\", \"stratum\": \"template\", \"auroc_metric\": 0.9518909984229043, \"auroc_comparator\": 0.5872179424966638, \"auroc_metric_ci\": [0.9359347303330807, 0.965...\n\n...0, \"metric\": \"c_score_nf\", \"comparator\": \"judge_cheap_disg\", \"stratum\": \"template\", \"auroc_metric\": 0.9518909984229043, \"auroc_comparator\": 0.5872179424966638, \"auroc_metric_ci\": [0.9359347303330807, 0.965...\n\n...221, \"metric\": \"c_score_sig\", \"comparator\": \"c_score_align\", \"stratum\": \"template\", \"auroc_metric\": 0.9518311681453316, \"auroc_comparator\": 0.9518311681453316, \"auroc_metric_ci\": [0.9366407499189088, 0.965...\n\n...r\": \"c_score_align\", \"stratum\": \"template\", \"auroc_metric\": 0.9518311681453316, \"auroc_comparator\": 0.9518311681453316, \"auroc_metric_ci\": [0.9366407499189088, 0.965378911845481], \"auroc_comparator_ci\": [0...\n\n...: 221, \"metric\": \"c_score_sig\", \"comparator\": \"c_score_hyb\", \"stratum\": \"template\", \"auroc_metric\": 0.9518311681453316, \"auroc_comparator\": 0.9496857836924377, \"auroc_metric_ci\": [0.9366407499189088, 0.965...\n\n...core_sig\": {\"template\": {\"n\": 2024, \"n_error\": 429, \"n_correct\": 1595, \"n_sentences\": 221, \"auroc\": 0.9518311681453316, \"n_pairs\": 75744, \"ci\": [0.9366407499189088, 0.965378911845481], \"se\": 0.007364368224...\n\n...re_align\": {\"template\": {\"n\": 2024, \"n_error\": 429, \"n_correct\": 1595, \"n_sentences\": 221, \"auroc\": 0.9518311681453316, \"n_pairs\": 75744, \"ci\": [0.9366407499189088, 0.965378911845481], \"se\": 0.007364368224...\n\n...ences\": 220, \"metric\": \"oof_full\", \"comparator\": \"oof_base\", \"stratum\": \"template\", \"auroc_metric\": 0.9529145942011403, \"auroc_comparator\": 0.577497573698896, \"auroc_metric_ci\": [0.9370891029541056, 0.9678...\n\n...arator\": \"oof_base\", \"stratum\": \"template\", \"auroc_metric\": 0.9547191556472158, \"auroc_comparator\": 0.9511479437098144, \"auroc_metric_ci\": [0.9393273666674118, 0.9692241229595169], \"auroc_comparator_ci\": [...\n\n...\", \"auroc_metric\": 0.9753532520763671, \"auroc_comparator\": 0.48268795167727324, \"auroc_metric_ci\": [0.9513279023083266, 0.9949247780988236], \"auroc_comparator_ci\": [0.4027661279520666, 0.5675238792417768],...\n\n..., \"metric\": \"c_score_sig\", \"comparator\": \"judge_cheap_disg\", \"stratum\": \"template\", \"auroc_metric\": 0.9522751322751323, \"auroc_comparator\": 0.6367724867724868, \"auroc_metric_ci\": [0.9228802414522235, 0.975...\n\n...\": true, \"c_score_sig\": {\"n\": 1757, \"n_error\": 382, \"n_correct\": 1375, \"n_sentences\": 194, \"auroc\": 0.9521818237416672, \"n_pairs\": 65404, \"ci\": [0.9351978696365493, 0.966717336273178], \"se\": 0.008128812822...\n\n...c_template\": {\"c_score_sig\": 0.9531550560102591, \"c_score_align\": 0.9531550560102591, \"c_score_nf\": 0.951112033090685, \"c_score_hyb\": 0.951112033090685, \"g_align\": 0.9774198820704308, \"g_nf\": 0.97664667647...\n\n...1550560102591, \"c_score_align\": 0.9531550560102591, \"c_score_nf\": 0.951112033090685, \"c_score_hyb\": 0.951112033090685, \"g_align\": 0.9774198820704308, \"g_nf\": 0.9766466764731767, \"judge_cheap_disg\": 0.59829...\n\n=== COMPLEXITY ===\nComplexity keys: ['word_tercile', 'nconds_bin', 'gee_words', 'gee_nconds', 'gee_depth']\n\nW1: {\n  \"n\": 574,\n  \"n_error\": 125,\n  \"n_correct\": 449,\n  \"n_sentences\": 62,\n  \"reportable_30_30\": true,\n  \"c_score_sig\": {\n    \"n\": 574,\n    \"n_error\": 125,\n    \"n_correct\": 449,\n    \"n_sentences\": 62,\n    \"auroc\": 0.9591661461586508,\n    \"n_pairs\": 6404,\n    \"ci\": [\n      0.9290017829394266,\n      0.9788575456530008\n    ],\n    \"se\": 0.012595236428157757\n  },\n  \"c_score_hyb\": {\n    \"n\": 574,\n    \"n_e\n\nW2: {\n  \"n\": 743,\n  \"n_error\": 149,\n  \"n_correct\": 594,\n  \"n_sentences\": 82,\n  \"reportable_30_30\": true,\n  \"c_score_sig\": {\n    \"n\": 743,\n    \"n_error\": 149,\n    \"n_correct\": 594,\n    \"n_sentences\": 82,\n    \"auroc\": 0.9474331386412542,\n    \"n_pairs\": 9759,\n    \"ci\": [\n      0.9094075660281566,\n      0.9736956252860364\n    ],\n    \"se\": 0.01667354118706151\n  },", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [23] TOOL CALL — Bash · 2026-09-25 09:28:02 UTC

```
Get judge-matched n per tercile and clarify 0.952 vs 0.954:
python3 -c "
import json
with open('/ai-inventor/aii_data/runs/run_-tTYmHVAOMOt/4_gen_paper_repo/_repo_clone/round-3/experiment-7/src/results/analysis.json') as f:
    d = json.load(f)

sig = d['SIG']

# Get judge n for each tercile
comp = sig['complexity']['word_tercile']
for k in ['W1','W2','W3']:
    v = comp[k]
    jd = v.get('judge_cheap_disg', {})
    print(f'{k}: n_total={v[\"n\"]}, n_judge_disg={jd.get(\"n\",\"?\")}, auroc_judge={jd.get(\"auroc\",\"?\")}')

# Also get the full-pool (n=2024) auroc for c_score_sig
print()
at = sig.get('auroc_table', {})
csig = at.get('c_score_sig', {}).get('template', {})
print(f'Full pool c_score_sig: n={csig.get(\"n\")}, auroc={csig.get(\"auroc\")}')

# Primary (n=1904 judge-matched)
p = sig['primary']
print(f'Primary (judge-matched): n={p[\"n\"]}, auroc={p[\"auroc_metric\"]}')
print(f'  -> 0.954 is on {p[\"n\"]} rows (judge-matched)')
print(f'  -> 0.952 is on {csig.get(\"n\")} rows (full pool)')
" 2>&1
```

### [24] TOOL RESULT — Bash · 2026-09-25 09:28:02 UTC

```
{"stdout": "W1: n_total=574, n_judge_disg=503, auroc_judge=0.577716098334655\nW2: n_total=743, n_judge_disg=712, auroc_judge=0.6244099021301094\nW3: n_total=707, n_judge_disg=689, auroc_judge=0.5668878424657534\n\nFull pool c_score_sig: n=2024, auroc=0.9518311681453316\nPrimary (judge-matched): n=1904, auroc=0.954340046099721\n  -> 0.954 is on 1904 rows (judge-matched)\n  -> 0.952 is on 2024 rows (full pool)", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [25] ASSISTANT · 2026-09-25 09:28:38 UTC

```
Now I have the data. Here's what the 5 fixes need:

- **0.954** = 1,904 judge-matched rows; **0.952** = 2,024 full-pool rows
- Judge-matched tercile n: W1=503, W2=712, W3=689 (vs full-pool 574/743/707)

I also need to update the code links to `run_Jhw6i0bFXdo3`. Let me apply all fixes and regenerate the tercile figure.

**Fix 1: Title**
```

### [26] TOOL CALL — Edit · 2026-09-25 09:28:38 UTC

```
File: /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.tex
OLD: \title{Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric\\for Natural-Language-to-First-Order-Logic Translation}
NEW: \title{Pre-Registered Cross-Family Solver Consensus Outperforms LLM Judges\\on Templated NL-to-FOL Translation with a Supplied Predicate Signature}
```

### [27] TOOL RESULT — Edit · 2026-09-25 09:28:38 UTC

```
{"filePath": "/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.tex", "oldString": "\\title{Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric\\\\for Natural-Language-to-First-Order-Logic Translation}", "newString": "\\title{Pre-Registered Cross-Family Solver Consensus Outperforms LLM Judges\\\\on Templated NL-to-FOL Translation with a Supplied Predicate Signature}", "originalFile": null, "structuredPatch": [{"oldStart": 3, "oldLines": 7, "newStart": 3, "newLines": 7, "lines": [" \\geometry{margin=1in}", " \\hypersetup{colorlinks=true, linkcolor=black, citecolor=black, urlcolor=black}", " ", "-\\title{Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric\\\\for Natural-Language-to-First-Order-Logic Translation}", "+\\title{Pre-Registered Cross-Family Solver Consensus Outperforms LLM Judges\\\\on Templated NL-to-FOL Translation with a Supplied Predicate Signature}", " ", " \\author{Anonymous}", " \\date{}"]}], "userModified": false, "replaceAll": false}
```

### [28] ASSISTANT · 2026-09-25 09:28:47 UTC

```
**Fix 2: Abstract** - add pre-registered/passed, CI, and scope.
```

### [29] TOOL CALL — Edit · 2026-09-25 09:28:47 UTC

```
File: /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.tex
OLD: When translators share a supplied predicate vocabulary, consensus achieves a within-template AUROC of 0.954 on 221~fresh long-exception sentences with trusted references and pure Z3 labels, versus 0.587 for a disguised API judge ($\Delta = +0.367$), flat across word-length terciles.
NEW: In a pre-registered evaluation on 221~templated long-exception sentences with a supplied predicate signature, consensus achieves a within-template AUROC of 0.954 versus 0.587 for a disguised API judge ($\Delta = +0.367$ [+0.328, +0.404]), flat across word-length terciles, passing the pre-registered criterion.
```

### [30] TOOL RESULT — Edit · 2026-09-25 09:28:47 UTC

```
{"filePath": "/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.tex", "oldString": "When translators share a supplied predicate vocabulary, consensus achieves a within-template AUROC of 0.954 on 221~fresh long-exception sentences with trusted references and pure Z3 labels, versus 0.587 for a disguised API judge ($\\Delta = +0.367$), flat across word-length terciles.", "newString": "In a pre-registered evaluation on 221~templated long-exception sentences with a supplied predicate signature, consensus achieves a within-template AUROC of 0.954 versus 0.587 for a disguised API judge ($\\Delta = +0.367$ [+0.328, +0.404]), flat across word-length terciles, passing the pre-registered criterion.", "originalFile": null, "structuredPatch": [{"oldStart": 14, "oldLines": 7, "newStart": 14, "newLines": 7, "lines": [" \\begin{abstract}", " Evaluating the faithfulness of natural-language-to-first-order-logic (NL$\\to$FOL) translations is hampered by the expense and unreliability of gold-standard references: recent audits find that roughly 40\\% of annotations in standard benchmarks contain errors.", " We study a gold-free alternative based on cross-family solver consensus: collect translations of the same sentence from multiple independent LLM families, check pairwise equivalence with an SMT solver, and score each candidate by the fraction of cross-family peers that disagree with it.", "-When translators share a supplied predicate vocabulary, consensus achieves a within-template AUROC of 0.954 on 221~fresh long-exception sentences with trusted references and pure Z3 labels, versus 0.587 for a disguised API judge ($\\Delta = +0.367$), flat across word-length terciles.", "+In a pre-registered evaluation on 221~templated long-exception sentences with a supplied predicate signature, consensus achieves a within-template AUROC of 0.954 versus 0.587 for a disguised API judge ($\\Delta = +0.367$ [+0.328, +0.404]), flat across word-length terciles, passing the pre-registered criterion.", " Under free (independently chosen) vocabulary, consensus still outperforms judges on both development data ($\\Delta = +0.099$) and untouched out-of-sample sentences ($\\Delta = +0.171$, original-view judge), but the advantage shrinks by roughly 0.15~AUROC and a fundamental rename tradeoff emerges: any predicate-name alignment needed to compare independently generated formulas produces a high false-alarm rate on meaning-preserving renames.", " Confirmation on independent held-out data was budget-stopped and remains incomplete.", " We present these results, identify the conditions under which shared versus free vocabulary governs metric strength, and release the full evaluation code."]}], "userModified": false, "replaceAll": false}
```

### [31] ASSISTANT · 2026-09-25 09:28:59 UTC

```
**Fix 3: Table 2** - change n to judge-matched rows (503/712/689).
```

### [32] TOOL CALL — Edit · 2026-09-25 09:28:59 UTC

```
File: /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.tex
OLD: \caption{R\_COMP-SIG within-template AUROC by word-length tercile.}
\label{tab:sig_complexity}
\small
\begin{tabular}{lccccc}
\toprule
Tercile & $n$ & ERR/COR & c\_sig & judge (disg.) & $\Delta$ [CI] \\
\midrule
W1 (shortest) & 574 & 125/449 & 0.959 & 0.578 & +0.382 [+0.278, +0.472] \\
W2 & 743 & 149/594 & 0.947 & 0.624 & +0.331 [+0.253, +0.421] \\
W3 (longest) & 707 & 155/552 & 0.953 & 0.567 & +0.388 [+0.301, +0.471] \\
NEW: \caption{R\_COMP-SIG within-template AUROC by word-length tercile (judge-matched rows).}
\label{tab:sig_complexity}
\small
\begin{tabular}{lccccc}
\toprule
Tercile & $n$ & ERR/COR & c\_sig & judge (disg.) & $\Delta$ [CI] \\
\midrule
W1 (shortest) & 503 & 125/449 & 0.959 & 0.578 & +0.382 [+0.278, +0.472] \\
W2 & 712 & 149/594 & 0.947 & 0.624 & +0.331 [+0.253, +0.421] \\
W3 (longest) & 689 & 155/552 & 0.953 & 0.567 & +0.388 [+0.301, +0.471] \\
```

### [33] TOOL RESULT — Edit · 2026-09-25 09:28:59 UTC

```
{"filePath": "/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.tex", "oldString": "\\caption{R\\_COMP-SIG within-template AUROC by word-length tercile.}\n\\label{tab:sig_complexity}\n\\small\n\\begin{tabular}{lccccc}\n\\toprule\nTercile & $n$ & ERR/COR & c\\_sig & judge (disg.) & $\\Delta$ [CI] \\\\\n\\midrule\nW1 (shortest) & 574 & 125/449 & 0.959 & 0.578 & +0.382 [+0.278, +0.472] \\\\\nW2 & 743 & 149/594 & 0.947 & 0.624 & +0.331 [+0.253, +0.421] \\\\\nW3 (longest) & 707 & 155/552 & 0.953 & 0.567 & +0.388 [+0.301, +0.471] \\\\", "newString": "\\caption{R\\_COMP-SIG within-template AUROC by word-length tercile (judge-matched rows).}\n\\label{tab:sig_complexity}\n\\small\n\\begin{tabular}{lccccc}\n\\toprule\nTercile & $n$ & ERR/COR & c\\_sig & judge (disg.) & $\\Delta$ [CI] \\\\\n\\midrule\nW1 (shortest) & 503 & 125/449 & 0.959 & 0.578 & +0.382 [+0.278, +0.472] \\\\\nW2 & 712 & 149/594 & 0.947 & 0.624 & +0.331 [+0.253, +0.421] \\\\\nW3 (longest) & 689 & 155/552 & 0.953 & 0.567 & +0.388 [+0.301, +0.471] \\\\", "originalFile": null, "structuredPatch": [{"oldStart": 184, "oldLines": 16, "newStart": 184, "newLines": 16, "lines": [" ", " \\begin{table}[!htbp]", " \\centering", "-\\caption{R\\_COMP-SIG within-template AUROC by word-length tercile.}", "+\\caption{R\\_COMP-SIG within-template AUROC by word-length tercile (judge-matched rows).}", " \\label{tab:sig_complexity}", " \\small", " \\begin{tabular}{lccccc}", " \\toprule", " Tercile & $n$ & ERR/COR & c\\_sig & judge (disg.) & $\\Delta$ [CI] \\\\", " \\midrule", "-W1 (shortest) & 574 & 125/449 & 0.959 & 0.578 & +0.382 [+0.278, +0.472] \\\\", "-W2 & 743 & 149/594 & 0.947 & 0.624 & +0.331 [+0.253, +0.421] \\\\", "-W3 (longest) & 707 & 155/552 & 0.953 & 0.567 & +0.388 [+0.301, +0.471] \\\\", "+W1 (shortest) & 503 & 125/449 & 0.959 & 0.578 & +0.382 [+0.278, +0.472] \\\\", "+W2 & 712 & 149/594 & 0.947 & 0.624 & +0.331 [+0.253, +0.421] \\\\", "+W3 (longest) & 689 & 155/552 & 0.953 & 0.567 & +0.388 [+0.301, +0.471] \\\\", " \\bottomrule", " \\end{tabular}", " \\end{table}"]}], "userModified": false, "replaceAll": false}
```

### [34] ASSISTANT · 2026-09-25 09:29:09 UTC

```
**Fix 3 continued: Regenerate Fig 2** with n=503/712/689.
```

### [35] TOOL CALL — Write · 2026-09-25 09:29:09 UTC

```
File: /tmp/claude-0/-ai-inventor-aii-data-runs-run-Jhw6i0bFXdo3-4-gen-paper-repo--4-assemble-paper-paper-workspace/83702c02-be52-4241-bfa8-4c2508d67ab7/scratchpad/fig_sig_tercile.json

{
  "type": "bar",
  "title": "R_COMP-SIG: AUROC by sentence length",
  "xlabel": "Word-length tercile",
  "ylabel": "Within-template AUROC",
  "aspect": "16:9",
  "categories": ["W1 (short, n=503)", "W2 (mid, n=712)", "W3 (long, n=689)"],
  "series": [
    {
      "label": "Consensus (c_score_sig)",
      "values": [0.959, 0.947, 0.953],
      "errors": [0.025, 0.033, 0.031]
    },
    {
      "label": "Judge (flash-lite, disguised)",
      "values": [0.578, 0.624, 0.567],
      "errors": [0.093, 0.075, 0.071]
    }
  ]
}
```

### [36] TOOL RESULT — Write · 2026-09-25 09:29:09 UTC

```
{"type": "create", "filePath": "/tmp/claude-0/-ai-inventor-aii-data-runs-run-Jhw6i0bFXdo3-4-gen-paper-repo--4-assemble-paper-paper-workspace/83702c02-be52-4241-bfa8-4c2508d67ab7/scratchpad/fig_sig_tercile.json", "content": "{\n  \"type\": \"bar\",\n  \"title\": \"R_COMP-SIG: AUROC by sentence length\",\n  \"xlabel\": \"Word-length tercile\",\n  \"ylabel\": \"Within-template AUROC\",\n  \"aspect\": \"16:9\",\n  \"categories\": [\"W1 (short, n=503)\", \"W2 (mid, n=712)\", \"W3 (long, n=689)\"],\n  \"series\": [\n    {\n      \"label\": \"Consensus (c_score_sig)\",\n      \"values\": [0.959, 0.947, 0.953],\n      \"errors\": [0.025, 0.033, 0.031]\n    },\n    {\n      \"label\": \"Judge (flash-lite, disguised)\",\n      \"values\": [0.578, 0.624, 0.567],\n      \"errors\": [0.093, 0.075, 0.071]\n    }\n  ]\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [37] TOOL CALL — Bash · 2026-09-25 09:29:15 UTC

```
Regenerate tercile figure with judge-matched n values:
SKILL_DIR="$(git rev-parse --show-toplevel 2>/dev/null || echo /ai-inventor)/.claude/skills/aii-data-fig-gen"
G="$SKILL_DIR/scripts/chart_gen.py"
SPEC="/tmp/claude-0/-ai-inventor-aii-data-runs-run-Jhw6i0bFXdo3-4-gen-paper-repo--4-assemble-paper-paper-workspace/83702c02-be52-4241-bfa8-4c2508d67ab7/scratchpad/fig_sig_tercile.json"
python "$G" --spec "$SPEC" --out /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/figures/fig_sig_tercile_v0
```

### [38] TOOL RESULT — Bash · 2026-09-25 09:29:17 UTC

```
{"stdout": "{\"ok\": true, \"written\": [\"/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/figures/fig_sig_tercile_v0.pdf\", \"/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/figures/fig_sig_tercile_v0.png\"]}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [39] ASSISTANT · 2026-09-25 09:29:23 UTC

```
Now update the figure caption to mention judge-matched rows.
```

### [40] TOOL CALL — Edit · 2026-09-25 09:29:23 UTC

```
File: /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.tex
OLD:   \caption{Within-template AUROC on R\_COMP-SIG by word-length tercile. Consensus (blue) is flat across terciles (0.947--0.959), while the disguised flash-lite judge (orange) hovers near chance (0.567--0.624). Error bars are 95\% sentence-cluster bootstrap CIs.}
NEW:   \caption{Within-template AUROC on R\_COMP-SIG by word-length tercile (judge-matched rows). Consensus (blue) is flat across terciles (0.947--0.959), while the disguised flash-lite judge (orange) hovers near chance (0.567--0.624). Error bars are 95\% sentence-cluster bootstrap CIs.}
```

### [41] TOOL RESULT — Edit · 2026-09-25 09:29:23 UTC

```
{"filePath": "/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.tex", "oldString": "  \\caption{Within-template AUROC on R\\_COMP-SIG by word-length tercile. Consensus (blue) is flat across terciles (0.947--0.959), while the disguised flash-lite judge (orange) hovers near chance (0.567--0.624). Error bars are 95\\% sentence-cluster bootstrap CIs.}", "newString": "  \\caption{Within-template AUROC on R\\_COMP-SIG by word-length tercile (judge-matched rows). Consensus (blue) is flat across terciles (0.947--0.959), while the disguised flash-lite judge (orange) hovers near chance (0.567--0.624). Error bars are 95\\% sentence-cluster bootstrap CIs.}", "originalFile": null, "structuredPatch": [{"oldStart": 201, "oldLines": 7, "newStart": 201, "newLines": 7, "lines": [" \\begin{figure}[!htbp]", "   \\centering", "   \\includegraphics[width=\\linewidth,height=0.85\\textheight,keepaspectratio]{figures/fig_sig_tercile_v0.pdf}", "-  \\caption{Within-template AUROC on R\\_COMP-SIG by word-length tercile. Consensus (blue) is flat across terciles (0.947--0.959), while the disguised flash-lite judge (orange) hovers near chance (0.567--0.624). Error bars are 95\\% sentence-cluster bootstrap CIs.}", "+  \\caption{Within-template AUROC on R\\_COMP-SIG by word-length tercile (judge-matched rows). Consensus (blue) is flat across terciles (0.947--0.959), while the disguised flash-lite judge (orange) hovers near chance (0.567--0.624). Error bars are 95\\% sentence-cluster bootstrap CIs.}", "   \\label{fig:sig_tercile}", " \\end{figure}", " "]}], "userModified": false, "replaceAll": false}
```

### [42] ASSISTANT · 2026-09-25 09:29:35 UTC

```
**Fix 4: Explain 0.952 vs 0.954** - clarify which rows each uses.
```

### [43] TOOL CALL — Edit · 2026-09-25 09:29:35 UTC

```
File: /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.tex
OLD: The drop from 0.952 (shared signature, R\_COMP-SIG) to 0.801 (free vocabulary on the same R\_COMP sentences) reflects the cost of predicate-name alignment: the aligner introduces both false negatives (correct equivalences missed) and false positives (incorrect mappings endorsed).
NEW: The drop from 0.952 (shared signature on the full 2,024-row pool) to 0.801 (free vocabulary on the same R\_COMP sentences) reflects the cost of predicate-name alignment: the aligner introduces both false negatives (correct equivalences missed) and false positives (incorrect mappings endorsed).
(The 0.954 reported in Table~\ref{tab:sig} is the same consensus metric restricted to the 1,904~rows where the disguised judge also returned a score, enabling a paired comparison; the full-pool AUROC is 0.952 [0.937, 0.965].)
```

### [44] TOOL RESULT — Edit · 2026-09-25 09:29:35 UTC

```
{"filePath": "/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.tex", "oldString": "The drop from 0.952 (shared signature, R\\_COMP-SIG) to 0.801 (free vocabulary on the same R\\_COMP sentences) reflects the cost of predicate-name alignment: the aligner introduces both false negatives (correct equivalences missed) and false positives (incorrect mappings endorsed).", "newString": "The drop from 0.952 (shared signature on the full 2,024-row pool) to 0.801 (free vocabulary on the same R\\_COMP sentences) reflects the cost of predicate-name alignment: the aligner introduces both false negatives (correct equivalences missed) and false positives (incorrect mappings endorsed).\n(The 0.954 reported in Table~\\ref{tab:sig} is the same consensus metric restricted to the 1,904~rows where the disguised judge also returned a score, enabling a paired comparison; the full-pool AUROC is 0.952 [0.937, 0.965].)", "originalFile": null, "structuredPatch": [{"oldStart": 247, "oldLines": 7, "newStart": 247, "newLines": 8, "lines": [" \\end{tabular}", " \\end{table}", " ", "-The drop from 0.952 (shared signature, R\\_COMP-SIG) to 0.801 (free vocabulary on the same R\\_COMP sentences) reflects the cost of predicate-name alignment: the aligner introduces both false negatives (correct equivalences missed) and false positives (incorrect mappings endorsed).", "+The drop from 0.952 (shared signature on the full 2,024-row pool) to 0.801 (free vocabulary on the same R\\_COMP sentences) reflects the cost of predicate-name alignment: the aligner introduces both false negatives (correct equivalences missed) and false positives (incorrect mappings endorsed).", "+(The 0.954 reported in Table~\\ref{tab:sig} is the same consensus metric restricted to the 1,904~rows where the disguised judge also returned a score, enabling a paired comparison; the full-pool AUROC is 0.952 [0.937, 0.965].)", " Aligner-free consensus (c\\_exact) achieves 0.689 [0.652, 0.726]; the aligner adds about 22\\% of the above-chance signal (c\\_align 0.241 versus c\\_exact 0.189 above the 0.5 baseline), with the remaining 78\\% coming from structural agreement alone.", " ", " On L25 sentences alone ($\\geq$25 words), the advantage narrows to $\\Delta = +0.069$ [$-$0.020, +0.148], not significant at the 95\\% level."]}], "userModified": false, "replaceAll": false}
```

### [45] ASSISTANT · 2026-09-25 09:29:39 UTC

```
**Fix 5: Conclusion point 3** - drop "even when no vocabulary mismatch exists".
```

### [46] TOOL CALL — Edit · 2026-09-25 09:29:39 UTC

```
File: /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.tex
OLD: (3)~understanding why correct translations of complex sentences diverge under free vocabulary even when no vocabulary mismatch exists.
NEW: (3)~understanding why correct translations of complex sentences diverge under free vocabulary.
```

### [47] TOOL RESULT — Edit · 2026-09-25 09:29:41 UTC

```
{"filePath": "/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.tex", "oldString": "(3)~understanding why correct translations of complex sentences diverge under free vocabulary even when no vocabulary mismatch exists.", "newString": "(3)~understanding why correct translations of complex sentences diverge under free vocabulary.", "originalFile": null, "structuredPatch": [{"oldStart": 436, "oldLines": 7, "newStart": 436, "newLines": 7, "lines": [" ", " However, independent confirmation on held-out data was budget-stopped and remains incomplete, the rename tradeoff limits applicability to free-vocabulary settings, and discrimination degrades with sentence length under free vocabulary.", " We release the full evaluation code and data to enable reproduction.", "-The immediate open problems are: (1)~completing the fresh-data confirmation with adequate sample sizes; (2)~breaking the rename tradeoff, perhaps through semantic predicate glossing; and (3)~understanding why correct translations of complex sentences diverge under free vocabulary even when no vocabulary mismatch exists.", "+The immediate open problems are: (1)~completing the fresh-data confirmation with adequate sample sizes; (2)~breaking the rename tradeoff, perhaps through semantic predicate glossing; and (3)~understanding why correct translations of complex sentences diverge under free vocabulary.", " ", " \\bibliographystyle{plainnat}", " \\bibliography{references}"]}], "userModified": false, "replaceAll": false}
```

### [48] ASSISTANT · 2026-09-25 09:29:47 UTC

```
Now update code links from `run_cNhUBrixEdz7` to `run_Jhw6i0bFXdo3`.
```

### [49] TOOL CALL — Edit · 2026-09-25 09:29:47 UTC

```
File: /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.tex
OLD: tree/fork/run_cNhUBrixEdz7/
NEW: tree/fork/run_Jhw6i0bFXdo3/
```

### [50] TOOL RESULT — Edit · 2026-09-25 09:29:47 UTC

```
{"filePath": "/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/paper.tex", "oldString": "tree/fork/run_cNhUBrixEdz7/", "newString": "tree/fork/run_Jhw6i0bFXdo3/", "originalFile": null, "structuredPatch": [{"oldStart": 85, "oldLines": 7, "newStart": 85, "newLines": 7, "lines": [" ", " \\subsection{Consensus scoring}", " ", "-Given a sentence $s$ and a candidate FOL translation $c$, we collect peer translations $\\{p_1, \\ldots, p_k\\}$ from $k$ independent LLM families.\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-1/experiment-1}}", "+Given a sentence $s$ and a candidate FOL translation $c$, we collect peer translations $\\{p_1, \\ldots, p_k\\}$ from $k$ independent LLM families.\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-1}}", " Each peer uses the same few-shot prompt but a different base model (e.g., one from each of Gemini, Claude, GPT, Llama, Qwen, Phi, Mistral).", " We compute:", " \\begin{equation}"]}, {"oldStart": 114, "oldLines": 7, "newStart": 114, "newLines": 7, "lines": [" \\begin{itemize}", " \\item \\textbf{c\\_exact}: no alignment; exact-match equivalence only. Immune to rename false alarms but blind to vocabulary-differing equivalences.", " \\item \\textbf{c\\_nf} (name-free): alignment by structural and semantic signatures only, ignoring text anchoring.", "-\\item \\textbf{p\\_peer\\_text}: a logistic fusion of consensus features with text-side features (bag-of-words coverage, role accounting, Z3 structural match).\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-2/experiment-5}}", "+\\item \\textbf{p\\_peer\\_text}: a logistic fusion of consensus features with text-side features (bag-of-words coverage, role accounting, Z3 structural match).\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-2/experiment-5}}", " \\end{itemize}", " ", " \\subsection{Evaluation framework}"]}, {"oldStart": 134, "oldLines": 7, "newStart": 134, "newLines": 7, "lines": [" ", " \\subsection{Datasets}", " ", "-\\paragraph{R\\_COMP (shared and free vocabulary).}\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/experiment-7}}", "+\\paragraph{R\\_COMP (shared and free vocabulary).}\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-7}}", " R\\_COMP generates long, complex sentences ($\\geq$25 words, 4--5 conditions) from a verified lexicon.", " 221~sentences produced 2,024 candidate translations from 10~LLM slots across 9~vendor families.", " Population: 429~ERROR~/~1,595~CORRECT (21.2\\% error rate)."]}, {"oldStart": 142, "oldLines": 7, "newStart": 142, "newLines": 7, "lines": [" In the \\textbf{FREE condition}, each translator chose its own predicate names; labels are provisional (Section~\\ref{sec:free_oos}).", " The pre-registration document, including the analysis plan and testability rule, was frozen before any SIG generation call, any label, or any metric score.\\footnote{Pre-registration: \\texttt{prereg\\_sig.json}, SHA-256 frozen before data collection.}", " ", "-\\paragraph{Development set $E$.}\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-1/experiment-3}}", "+\\paragraph{Development set $E$.}\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-3}}", " 8,507~rows from 700~sentences drawn from the MALLS corpus~\\citep{Yang2023} and ProverQA~\\citep{Qi2025}.", " Each sentence was translated by 9~LLM families using a frozen few-shot prompt.", " The primary evaluation population (R\\_AB, both panellists agree) contains 2,686~items (1,822~ERROR~/~864~CORRECT, 292~sentences); the all-families subset where every peer family contributed a translation is $n = 2{,}014$."]}, {"oldStart": 150, "oldLines": 7, "newStart": 150, "newLines": 7, "lines": [" The R\\_COMP-SIG data later served as development data for aligner tuning, so the development-set numbers from $E$ are not independent of R\\_COMP.", " ", " \\paragraph{Baselines.}", "-(1)~\\textbf{Flash-lite judge} (Gemini Flash Lite, disguised and original views); (2)~\\textbf{nano judge} (Gemini Flash 2.0); (3)~\\textbf{local judges} (Qwen3-8B, Llama-8B); (4)~\\textbf{round-trip NLI}; (5)~\\textbf{self-consistency} (5-sample within-model agreement); (6)~\\textbf{structural features} (arity consistency, dangling predicates, rerun Jaccard); (7)~\\textbf{feature stacks}: cross-validated logistic regressions over subsets of these features.\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-1/experiment-4}}", "+(1)~\\textbf{Flash-lite judge} (Gemini Flash Lite, disguised and original views); (2)~\\textbf{nano judge} (Gemini Flash 2.0); (3)~\\textbf{local judges} (Qwen3-8B, Llama-8B); (4)~\\textbf{round-trip NLI}; (5)~\\textbf{self-consistency} (5-sample within-model agreement); (6)~\\textbf{structural features} (arity consistency, dangling predicates, rerun Jaccard); (7)~\\textbf{feature stacks}: cross-validated logistic regressions over subsets of these features.\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-4}}", " ", " \\subsection{Shared-signature results (R\\_COMP-SIG)}\\label{sec:sig_results}", " "]}, {"oldStart": 215, "oldLines": 7, "newStart": 215, "newLines": 7, "lines": [" ", " \\subsection{Free-vocabulary development results (set $E$)}\\label{sec:dev_results}", " ", "-Figure~\\ref{fig:dev_auroc} and Table~\\ref{tab:main} summarise the free-vocabulary comparison on development set~$E$.\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/experiment-6}}", "+Figure~\\ref{fig:dev_auroc} and Table~\\ref{tab:main} summarise the free-vocabulary comparison on development set~$E$.\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-6}}", " Cross-family consensus (c\\_score\\_align) outperforms the disguised flash-lite judge by $\\Delta = +0.099$ [+0.049, +0.146] on the full R\\_AB population and by $\\Delta = +0.116$ [+0.070, +0.163] on the long-sentence pool (L25+L20+EXC).", " Adding c\\_score\\_align to the 28-feature baseline stack increases stratified AUROC by +0.039 [+0.021, +0.057]; a permutation null test gives $p_{95} = 0.009$, confirming the signal is not explained by the existing features.", " "]}, {"oldStart": 262, "oldLines": 7, "newStart": 262, "newLines": 7, "lines": [" ", " \\subsection{Free-vocabulary out-of-sample (R\\_COMP FREE)}\\label{sec:free_oos}", " ", "-The same 221~R\\_COMP sentences were also translated under free vocabulary (each translator choosing its own predicate names).\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-5/experiment-13}}", "+The same 221~R\\_COMP sentences were also translated under free vocabulary (each translator choosing its own predicate names).\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-5/experiment-13}}", " Confirmatory labelling required a gloss gate (LLM-checked semantic alignment of predicate mappings).", " This gate failed twice (balanced accuracy 0.776 and 0.561, below the 0.90 threshold), producing zero confirmed CORRECT rows and rendering the confirmatory test not testable.", " "]}, {"oldStart": 292, "oldLines": 7, "newStart": 292, "newLines": 7, "lines": [" ", " \\subsection{Mechanism}\\label{sec:mechanism}", " ", "-We decompose the consensus signal\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/evaluation-2}} into two components at a fixed decision threshold:", "+We decompose the consensus signal\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/evaluation-2}} into two components at a fixed decision threshold:", " \\begin{itemize}", " \\item \\textbf{Endorsement} $e$: fraction of ERROR items endorsed by the peer majority (false negatives of consensus).", " \\item \\textbf{Divergence} $d$: fraction of CORRECT items that diverge from the peer majority (false positives of consensus)."]}, {"oldStart": 343, "oldLines": 14, "newStart": 343, "newLines": 14, "lines": [" \\subsection{Confirmation status}\\label{sec:confirmation}", " ", " Independent confirmation on held-out data remains incomplete.", "-A fresh held-out dataset (E2-A, 550~new sentences) was constructed, but the run-level budget was exhausted before enough items could be labelled.\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-4/dataset-4}}", "+A fresh held-out dataset (E2-A, 550~new sentences) was constructed, but the run-level budget was exhausted before enough items could be labelled.\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/dataset-4}}", " On the one testable stratum (DT, short sentences from ProverQA), consensus achieves a stratified AUROC of 0.916, tying the local Qwen-8B judge ($\\Delta = +0.003$ [$-$0.042, +0.052]).", " On L25 sentences, c\\_score\\_align falls to 0.443 on only 42 items (35~ERROR~/~7~CORRECT), below chance, but the estimate has extreme variance with only 7~CORRECT items from 3~sentences.", " Every pre-registered criterion on the target strata returned NOT\\_TESTABLE or unfavourable.", " ", " \\subsection{The rename tradeoff}\\label{sec:rename}", " ", "-The predicate aligner\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-3/experiment-8}} that enables cross-family comparison under free vocabulary also introduces a fundamental false-alarm vulnerability.", "+The predicate aligner\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-3/experiment-8}} that enables cross-family comparison under free vocabulary also introduces a fundamental false-alarm vulnerability.", " When correct formulas are copied with meaning-preserving predicate renames (same semantics, different symbol names), the consensus score should not change.", " Table~\\ref{tab:rename} shows the false-alarm rates in practice.", " "]}, {"oldStart": 383, "oldLines": 7, "newStart": 383, "newLines": 7, "lines": [" ", " \\subsection{Dead ends}", " ", "-Several alternatives were investigated and abandoned during development: a fused structural-feature filter (false-alarm gate failure); name-free consensus c\\_nf (rename-invariant but blind to meaning-rename errors, as described in Section~\\ref{sec:rename}); a decomposed solver-based semantic reader (balanced accuracy 0.476); LLM adjudication of disputed items (balanced accuracy 0.662 on expert-labelled items); and candidate-signature consensus, which scores candidates by cueing peers with the candidate's own predicate symbols rather than letting them choose independently (provisional negative: error endorsement rose to 0.459 because peers were anchored into reproducing the candidate's errors).\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_cNhUBrixEdz7/round-4/experiment-9}}", "+Several alternatives were investigated and abandoned during development: a fused structural-feature filter (false-alarm gate failure); name-free consensus c\\_nf (rename-invariant but blind to meaning-rename errors, as described in Section~\\ref{sec:rename}); a decomposed solver-based semantic reader (balanced accuracy 0.476); LLM adjudication of disputed items (balanced accuracy 0.662 on expert-labelled items); and candidate-signature consensus, which scores candidates by cueing peers with the candidate's own predicate symbols rather than letting them choose independently (provisional negative: error endorsement rose to 0.459 because peers were anchored into reproducing the candidate's errors).\\footnote{Code: \\url{https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/tree/fork/run_Jhw6i0bFXdo3/round-4/experiment-9}}", " ", " \\section{Discussion}", " "]}], "userModified": false, "replaceAll": true}
```

### [51] ASSISTANT · 2026-09-25 09:29:51 UTC

```
Now recompile.
```

### [52] TOOL CALL — Bash · 2026-09-25 09:29:51 UTC

```
Full 4-pass recompile:
pdflatex -interaction=nonstopmode paper.tex 2>&1 | tail -3 && /usr/bin/bibtex.original paper 2>&1 | tail -1 && pdflatex -interaction=nonstopmode paper.tex 2>&1 | tail -3 && pdflatex -interaction=nonstopmode paper.tex 2>&1 | tail -3
```

### [53] TOOL RESULT — Bash · 2026-09-25 09:30:05 UTC

```
{"stdout": "sfonts/cm/cmtt9.pfb>\nOutput written on paper.pdf (13 pages, 304210 bytes).\nTranscript written on paper.log.\nDatabase file #1: references.bib\n/cm/cmtt9.pfb>\nOutput written on paper.pdf (14 pages, 329176 bytes).\nTranscript written on paper.log.\n/cm/cmtt9.pfb>\nOutput written on paper.pdf (14 pages, 330422 bytes).\nTranscript written on paper.log.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [54] TOOL CALL — Bash · 2026-09-25 09:30:11 UTC

```
Verify no undefined refs and correct code links:
grep -c "LaTeX Warning.*undefined" paper.log && grep -o 'tree/[^}]*' paper.tex | head -3 && grep -c "run_Jhw6i0bFXdo3" paper.tex
```

### [55] TOOL RESULT — Bash · 2026-09-25 09:30:11 UTC

```
{"stdout": "0", "stderr": "", "interrupted": false, "isImage": false, "returnCodeInterpretation": "No matches found", "noOutputExpected": false}
```

### [56] TOOL CALL — Bash · 2026-09-25 09:30:15 UTC

```
List all code link branches:
grep -o 'tree/fork/[^}]*' paper.tex
```

### [57] TOOL RESULT — Bash · 2026-09-25 09:30:15 UTC

```
{"stdout": "tree/fork/run_Jhw6i0bFXdo3/round-1/experiment-1\ntree/fork/run_Jhw6i0bFXdo3/round-2/experiment-5\ntree/fork/run_Jhw6i0bFXdo3/round-3/experiment-7\ntree/fork/run_Jhw6i0bFXdo3/round-1/experiment-3\ntree/fork/run_Jhw6i0bFXdo3/round-1/experiment-4\ntree/fork/run_Jhw6i0bFXdo3/round-3/experiment-6\ntree/fork/run_Jhw6i0bFXdo3/round-5/experiment-13\ntree/fork/run_Jhw6i0bFXdo3/round-3/evaluation-2\ntree/fork/run_Jhw6i0bFXdo3/round-4/dataset-4\ntree/fork/run_Jhw6i0bFXdo3/round-3/experiment-8\ntree/fork/run_Jhw6i0bFXdo3/round-4/experiment-9", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [58] ASSISTANT · 2026-09-25 09:30:41 UTC

```
All links correct. Now write the structured output.
```

### [59] TOOL CALL — Write · 2026-09-25 09:30:41 UTC

```
File: /ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/.terminal_claude_agent_struct_out.json

{
  "title": "Solver Consensus Beats Judges on Templated Logic Translations",
  "summary": "The paper evaluates cross-family solver consensus as a gold-free faithfulness metric for NL-to-FOL translation, with a pre-registered evaluation under shared predicate signature and exploratory results under free vocabulary. Title updated to state the R_COMP-SIG result. Abstract rewritten to note pre-registration, the CI (+0.367 [+0.328, +0.404]), and scope (templated sentences with a supplied signature). Sections: Introduction (contributions), Related Work (NL-to-FOL, consensus, LLM-as-judge, diverse redundancy), Method (consensus scoring, predicate alignment, score variants, evaluation framework), Experiments (datasets, shared-signature results with Table 1 and tercile Table 2 and Figure 2, free-vocabulary development results with Figure 1 and Table 3, out-of-sample results, mechanism decomposition with Figure 3, family sufficiency with Table 5 and Figure 4, confirmation status, rename tradeoff with Table 6, per-type sensitivity, dead ends), Discussion (shared vs free vocabulary, incomplete confirmation, rename tradeoff, 8 limitations), and Conclusion. Table 2 and Figure 2 updated to show judge-matched n (503/712/689). The difference between 0.952 (full 2,024-row pool) and 0.954 (1,904 judge-matched rows) is now explained in Section 4.3. Conclusion point 3 drops the unsupported clause about vocabulary mismatch. Four figures: fig_dev_auroc_v0.pdf, fig_sig_tercile_v0.pdf (regenerated with n=503/712/689), fig_complexity_v0.pdf, fig_k_curve_v0.pdf. Bibliography: 13 entries. PDF compiled (14 pages, no undefined references).",
  "findings_summary": "Cross-family solver consensus, where multiple independent LLM families translate the same sentence into first-order logic and an SMT solver checks pairwise equivalence, achieves a within-template AUROC of 0.954 on 221 pre-registered templated sentences with a supplied predicate signature, versus 0.587 for a disguised LLM judge (delta +0.367 [+0.328, +0.404]), flat across word-length terciles. Under free vocabulary (each translator choosing its own predicate names), consensus still outperforms judges but drops by roughly 0.15 AUROC due to a fundamental rename tradeoff: predicate-name alignment produces a 76.5% false-alarm rate on meaning-preserving renames. Independent confirmation on held-out data was budget-stopped and remains incomplete.",
  "out_expected_files": {
    "paper_tex_path": "paper.tex",
    "paper_pdf_path": "paper.pdf",
    "references_bib_path": "references.bib",
    "figure_paths": [
      "figures/fig_dev_auroc_v0.pdf",
      "figures/fig_sig_tercile_v0.pdf",
      "figures/fig_complexity_v0.pdf",
      "figures/fig_k_curve_v0.pdf"
    ]
  }
}
```

### [60] TOOL RESULT — Write · 2026-09-25 09:30:41 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_Jhw6i0bFXdo3/4_gen_paper_repo/_4_assemble_paper/paper/workspace/.terminal_claude_agent_struct_out.json", "content": "{\n  \"title\": \"Solver Consensus Beats Judges on Templated Logic Translations\",\n  \"summary\": \"The paper evaluates cross-family solver consensus as a gold-free faithfulness metric for NL-to-FOL translation, with a pre-registered evaluation under shared predicate signature and exploratory results under free vocabulary. Title updated to state the R_COMP-SIG result. Abstract rewritten to note pre-registration, the CI (+0.367 [+0.328, +0.404]), and scope (templated sentences with a supplied signature). Sections: Introduction (contributions), Related Work (NL-to-FOL, consensus, LLM-as-judge, diverse redundancy), Method (consensus scoring, predicate alignment, score variants, evaluation framework), Experiments (datasets, shared-signature results with Table 1 and tercile Table 2 and Figure 2, free-vocabulary development results with Figure 1 and Table 3, out-of-sample results, mechanism decomposition with Figure 3, family sufficiency with Table 5 and Figure 4, confirmation status, rename tradeoff with Table 6, per-type sensitivity, dead ends), Discussion (shared vs free vocabulary, incomplete confirmation, rename tradeoff, 8 limitations), and Conclusion. Table 2 and Figure 2 updated to show judge-matched n (503/712/689). The difference between 0.952 (full 2,024-row pool) and 0.954 (1,904 judge-matched rows) is now explained in Section 4.3. Conclusion point 3 drops the unsupported clause about vocabulary mismatch. Four figures: fig_dev_auroc_v0.pdf, fig_sig_tercile_v0.pdf (regenerated with n=503/712/689), fig_complexity_v0.pdf, fig_k_curve_v0.pdf. Bibliography: 13 entries. PDF compiled (14 pages, no undefined references).\",\n  \"findings_summary\": \"Cross-family solver consensus, where multiple independent LLM families translate the same sentence into first-order logic and an SMT solver checks pairwise equivalence, achieves a within-template AUROC of 0.954 on 221 pre-registered templated sentences with a supplied predicate signature, versus 0.587 for a disguised LLM judge (delta +0.367 [+0.328, +0.404]), flat across word-length terciles. Under free vocabulary (each translator choosing its own predicate names), consensus still outperforms judges but drops by roughly 0.15 AUROC due to a fundamental rename tradeoff: predicate-name alignment produces a 76.5% false-alarm rate on meaning-preserving renames. Independent confirmation on held-out data was budget-stopped and remains incomplete.\",\n  \"out_expected_files\": {\n    \"paper_tex_path\": \"paper.tex\",\n    \"paper_pdf_path\": \"paper.pdf\",\n    \"references_bib_path\": \"references.bib\",\n    \"figure_paths\": [\n      \"figures/fig_dev_auroc_v0.pdf\",\n      \"figures/fig_sig_tercile_v0.pdf\",\n      \"figures/fig_complexity_v0.pdf\",\n      \"figures/fig_k_curve_v0.pdf\"\n    ]\n  }\n}\n", "structuredPatch": [], "originalFile": null, "userModified": false}
```

### [61] ASSISTANT · 2026-09-25 09:30:47 UTC

```
All 5 staff fixes applied:

1. **Title**: Now states the R_COMP-SIG result (pre-registered consensus outperforms judges on templated sentences with supplied signature).
2. **Abstract**: Notes pre-registration, gives CI (+0.367 [+0.328, +0.404]), and scopes to templated sentences with a supplied predicate signature.
3. **Table 2 & Fig 2**: n updated to judge-matched rows (503/712/689); figure regenerated with correct n.
4. **Section 4.3**: Explains 0.952 (full 2,024-row pool) vs 0.954 (1,904 judge-matched rows for paired comparison).
5. **Conclusion point 3**: Dropped "even when no vocabulary mismatch exists".

Code links updated to `fork/run_Jhw6i0bFXdo3`. PDF compiled (14 pages, no undefined refs). Structured output written.
```
