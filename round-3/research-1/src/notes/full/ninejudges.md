URL: https://arxiv.org/html/2605.29800 | FULL FETCH | 2026-09-24T01:50:35Z
warning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
URL: https://arxiv.org/html/2605.29800
Type: HTML
Length: 65138 chars (truncated)

--- Content ---

##### Report GitHub Issue

×

Title:

Content selection saved. Describe the issue below:

Description:

Submit without GitHub Submit in GitHub

arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[ Back to arXiv ](/)

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) Report Issue [ Back to Abstract ](/abs/2605.29800v1 "Back to abstract page") [ Download PDF](/pdf/2605.29800v1 "Download PDF") [ ](javascript:toggleNavTOC\(\); "Toggle navigation") [ ](javascript:toggleReadingMode\(\); "Disable reading mode, show header and footer")

  1. Abstract
  2. 1 Introduction
  3. 2 Related Work
     1. LLM-as-a-judge.
     2. LLM judge panels.
     3. Correlated errors and scaling limits.
     4. Condorcet Jury Theorem and ensembles.
     5. Statistically principled aggregation.
     6. Human label variation and ChaosNLI.
  4. 3 Methodology
     1. 3.1 Datasets
     2. 3.2 Judge Panel
     3. 3.3 Effective Sample Size (neffn_{\text{eff}})
        1. Kish design-effect neffn_{\text{eff}}.
        2. Eigenvalue neffn_{\text{eff}}.
        3. Bootstrap confidence interval.
     4. 3.4 Condorcet Null Model
        1. Confusion-matrix calibration.
        2. Item-aware simulation.
        3. Condorcet gap.
     5. 3.5 Statistical Tests
        1. Permutation omnibus test.
        2. Per-bin binomial tests.
  5. 4 Results
     1. 4.1 Effective Independence
     2. 4.2 Condorcet Gap
     3. 4.3 Permutation Test
     4. 4.4 Scaling: neff​(k)n_{\text{eff}}(k) vs. kk
     5. 4.5 Cross-Dataset Replication
     6. 4.6 Robustness to Prompt, Temperature, and Task
  6. 5 Analysis and Discussion
     1. 5.1 Leave-One-Out: Which Judges Matter?
     2. 5.2 Stratified and Subset Analyses
     3. 5.3 Same-Family vs. Cross-Family Correlation
     4. 5.4 Does Smarter Aggregation Help?
  7. 6 Conclusion
  8. Classification tasks.
  9. Gold standard validity.
  10. Snapshot in time.
  11. Condorcet model calibration.
  12. Prompt and decoding choices.
  13. Bootstrap CI interpretation.
  14. References
  15. A NLI Classification Prompt
     1. A.1 RewardBench Pairwise Preference Prompt
  16. B Phi Correlation Matrix
  17. C Condorcet Gap Visualization
  18. D Distributional Alignment Analysis
  19. E Split-Half Condorcet Validation
  20. F Sample Size Convergence
  21. G Scaling Curve Data
  22. H Supplementary Analysis Tables
  23. I Aggregation Method Details
  24. J All-Wrong Item Analysis
  25. K Tie-Breaking
     1. Gold-label ties (100 annotators).
     2. Majority-vote ties (9 judges).



[ License: arXiv.org perpetual non-exclusive license ](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2605.29800v1 [cs.CL] 28 May 2026

# Nine Judges, Two Effective Votes:   
Correlated Errors Undermine LLM Evaluation Panels

Guneet Kohli  Affiliation: Apple  Email: [g_kohli@apple.com](mailto:)

###### Abstract

LLM-as-a-judge panels aggregate votes from multiple models, with the expectation that diverse models yield more reliable evaluations. We develop a framework to measure the true informational value of such panels and quantify how far their reliability falls short of the independent-voting ideal. Testing a panel of 9 frontier LLMs from 7 model families on three natural language inference datasets (each with 100 human annotations per item), we find that the 9 judges effectively provide only about 2 independent votes’ worth of information. Roughly three-quarters of the panel’s nominal independence is lost because the models make the same mistakes on the same items. The consequences are stark: the panel’s actual accuracy falls 8–22 percentage points short of what independent voting would achieve, and the best single judge matches or outperforms the full panel across all conditions. Neither adding more judges nor using smarter aggregation algorithms helps — established methods close at most 11% of this gap, even with access to the correct answers. We quantify these findings using the Kish effective sample size (neffn_{\text{eff}}) and a Condorcet null model, and show the deficit is robust across prompt variants, temperatures, chain-of-thought reasoning, and a pairwise preference task (RewardBench). The bottleneck is correlated judges, not the aggregation algorithm, implying that scaling up panels cannot substitute for genuinely independent evaluation.

## 1 Introduction

LLM-as-a-judge evaluation has become a standard methodology for scalable assessment of language model outputs (Zheng et al., 2023). To mitigate single-model biases, researchers have turned to multi-model panels — ensembles of diverse LLMs that vote on evaluation items — with the expectation that cross-model diversity yields something approaching independent assessment (Verga et al., 2024). The intuition is compelling: if models from different providers, trained on different data, make different errors, then majority voting should be robust.

This intuition draws on the logic of the Condorcet Jury Theorem (de Condorcet, 1785): if each voter is better than chance and votes independently, majority-vote accuracy increases monotonically with panel size and approaches certainty. The practical appeal is clear — adding more judges should always help, and a panel of 9 should be far more reliable than any single judge.

But is it? We evaluate a 9-judge panel spanning 7 model families on three natural language inference (NLI) benchmarks — MNLI, SNLI, and AlphaNLI — each with 100 human annotations per item (§3). The panel provides negligible or negative lift over its single best member. On MNLI, the panel (72.0%) barely edges the best judge (Qwen3-32B, 71.8%) by 0.2pp — within noise; on SNLI, the best judge dominates (Claude Sonnet 4.5, 84.2% vs. panel 77.7%); and on AlphaNLI, an abductive reasoning task with a different label set, the pattern persists (91.2% vs. 88.7%). These results are impossible under the independence assumption but expected when errors are highly correlated. Recent work has documented such correlated errors across LLMs on standard benchmarks (Kim et al., 2025), and conceptual arguments suggest that shared training paradigms should induce dependence (Lefort et al., 2024). However, no prior work has _quantified_ the effective independence of LLM judge panels in a way that directly connects to majority-vote reliability, using a ground truth rich enough to validate the measurement.

We address this gap with three contributions:

  1. 1.

A diagnostic framework for LLM judge panels. We combine the Kish effective sample size (neffn_{\text{eff}}) — a measure of how many truly independent votes a panel contains — with a Condorcet null model that simulates what majority-vote accuracy _would be_ if judges voted independently. Applied to a 9-judge, 7-family panel on three ChaosNLI datasets (Nie et al., 2020), we find neff≈2.0n_{\text{eff}}\approx 2.0–2.52.5: the panel contains roughly two independent votes worth of information. The accuracy shortfall relative to this independent prediction (the _Condorcet gap_) is 8–22 percentage points (pp; permutation p<10−4p<10^{-4}).

  2. 2.

A severe independence deficit, stable across tasks, prompts, and temperatures. The deficit is remarkably consistent: neff≈2.0n_{\text{eff}}\approx 2.0–2.52.5 across three NLI datasets, three prompt variants, two temperature settings, and a pairwise preference task (RewardBench; neff=2.0n_{\text{eff}}=2.0) — despite panel accuracy ranging from 69% to 93%. Across all conditions, the panel fails to meaningfully outperform the single best judge. The scaling curve shows that adding judges beyond 5 yields negligible benefit, with effective independence asymptoting at roughly 2.3–3.1 (varying by dataset).

  3. 3.

A negative result: aggregation cannot overcome correlation. Established aggregation methods — Dawid-Skene EM (Dawid and Skene, 1979) and accuracy-weighted voting — close at most 11% of the Condorcet gap across all four datasets, even with oracle access to gold labels. The bottleneck is correlated inputs, not the algorithm: no weighting scheme can extract a third independent vote from ∼\sim2.2 effective votes of information.




These results have direct practical implications: paying for 9 opinions but receiving the informational equivalent of ∼\sim2 is a substantial inefficiency. The marginal value of additional judges is near zero, and unanimous panel agreement is far less diagnostic than it appears. The path forward is not larger ensembles of similar models, but diversification of the underlying reasoning — models that genuinely differ in how they process information.

## 2 Related Work

#### LLM-as-a-judge.

Zheng et al. (2023) established the LLM-as-a-judge paradigm, and subsequent work has revealed systematic biases (Wang et al., 2024; Ye et al., 2025; Thakur et al., 2025) and raised measurement-theory concerns about validity and reliability (Chehbouni et al., 2025; Calderon et al., 2025). Our work goes beyond cataloguing individual biases to quantify the _structural_ dependence among judges — a more fundamental constraint on panel reliability.

#### LLM judge panels.

Verga et al. (2024) proposed PoLL (Panel of LLM Evaluators), demonstrating that panels of smaller, diverse models outperform single large judges across six datasets. Importantly, PoLL compares panels to the _average_ individual judge, where panels naturally win by diversifying away individual quirks. Our finding — that the _best_ individual outperforms the panel — does not contradict PoLL but reveals a different phenomenon: when judges are highly correlated, majority voting dilutes the best judge’s signal with redundant weaker votes. Our work complements PoLL by showing that the panel’s effective information content is far lower than the raw panel size suggests.

The Trust-or-Escalate framework (Jung et al., 2025) provides provable guarantees using _single-model_ confidence to decide when to escalate to human review. Our approach differs fundamentally: we use _cross-model_ disagreement and show that this disagreement is itself unreliable due to correlated errors.

#### Correlated errors and scaling limits.

Most closely related to our work, Kim et al. (2025) conducted a large-scale study of error correlation across 350+ LLMs, finding that models agree on wrong answers 60% of the time on some benchmarks. Jiang et al. (2025) demonstrated what they term the “artificial hivemind” effect: LLMs produce strikingly homogeneous outputs on open-ended tasks, both within and across model families, and LLM judges are poorly calibrated on items where human annotators disagree — our neff≈2.0n_{\text{eff}}\approx 2.0–2.42.4 provides a precise quantification of this qualitative insight. Dorner et al. (2025) proved a complementary theoretical result: when the judge is no more capable than the evaluated model, no debiasing method can reduce the required ground-truth data by more than half, establishing a fundamental scaling ceiling. We build on this body of work by (a) measuring effective independence in the LLM-as-a-judge setting using Kish neffn_{\text{eff}}, (b) quantifying the Condorcet gap that correlation creates, and (c) showing that established aggregation methods cannot close this gap.

#### Condorcet Jury Theorem and ensembles.

The Condorcet Jury Theorem (de Condorcet, 1785) underpins much of the intuition behind ensemble methods (Dietterich, 2000; Surowiecki, 2004): diverse, independent voters collectively outperform individuals. Austen-Smith and Banks (1996) showed that independence is necessary, not just sufficient — correlated voters can perform _worse_ than individuals. In the LLM setting, Lefort et al. (2024) applied the Condorcet Jury Theorem to sentiment analysis ensembles, finding marginal improvement consistent with a lack of independence. Turkmen et al. (2026) formalized this via an information-theoretic error floor. Our work empirically validates these theoretical concerns, providing the first item-level measurement of effective independence in a judge evaluation setting.

#### Statistically principled aggregation.

Zhao et al. (2025) proposed CARE, a confounder-aware aggregation framework that models inter-judge correlations, reducing aggregation error by up to 25%. The crowdsourcing literature offers related methods: the Dawid-Skene model (Dawid and Skene, 1979) estimates annotator error rates via EM, and Raykar et al. (2010) extended this to learning from noisy crowds. Where these methods propose _solutions_ (better aggregation), our paper provides both the _diagnosis_ — quantifying how much independence is actually present — and a _negative result_ : even with oracle access to gold labels, established aggregation methods close at most 11% of the Condorcet gap (§5.4), suggesting that the problem is structural rather than algorithmic.

#### Human label variation and ChaosNLI.

Human disagreement on NLI items is systematic, not mere noise (Pavlick and Kwiatkowski, 2019; Plank, 2022). Nie et al. (2020) created ChaosNLI with 100 annotator labels per item, built on MNLI (Williams et al., 2018), providing the richest available ground truth for studying disagreement patterns. Lee et al. (2023) showed that single LLMs fail to capture the distributional properties of human disagreement on ChaosNLI. We extend this line by testing whether _multi-model panels_ can capture human disagreement patterns, finding that correlated errors severely limit their ability to do so.

## 3 Methodology

### 3.1 Datasets

We use ChaosNLI (Nie et al., 2020), which provides 100 annotator labels per item. Our primary dataset is ChaosNLI-MNLI (1,599 MNLI items; Williams et al. 2018), with labels entailment (e), neutral (n), or contradiction (c). We replicate on ChaosNLI-SNLI (1,514 SNLI items; Bowman et al. 2015) as a same-task robustness check, and on ChaosNLI-AlphaNLI (1,532 abductive NLI items; Bhagavatula et al. 2020) as a cross-task replication with a different label set (2-class: hypothesis 1 vs. hypothesis 2) and reasoning type (abductive rather than textual entailment). From each dataset, we sample 1,000 items using entropy-stratified sampling (equal proportions from low, medium, and high human-entropy terciles) with seed 42.

The gold standard for each item is the majority vote of 100 annotators (tie-breaking details in Appendix K). Human entropy (Shannon entropy, base-2) ranges from 0.00 to 1.58 bits on MNLI/SNLI and 0.00 to 1.00 bits on AlphaNLI (lower maximum due to 2-class), providing rich ground truth against which to validate panel behavior. We present MNLI results in the main body and report SNLI and AlphaNLI replication results in §4.5.

### 3.2 Judge Panel

Our panel consists of 9 judges from 7 model families (Table 1). All judges use temperature 0.0 and receive a standardized NLI classification prompt (Appendix A). Rare parse failures (<<0.1% of all judgments; 21 of 28 from Llama 4 Maverick, with 5 from Gemini 2.5 Pro and 2 from Claude Sonnet 4.5) are handled via deterministic hash-based random assignment to {e, n, c} to avoid systematic bias. With an odd number of judges, majority-vote ties are eliminated on 2-class tasks (AlphaNLI, RewardBench); on 3-class tasks (MNLI, SNLI), the rare remaining ties (0.4–1.1% of items) are broken via deterministic SHA-256 hashing of the item index and vote sequence, ensuring reproducibility (Appendix K).

Judge | Family | Error Rate  
---|---|---  
GPT-4o | OpenAI | 0.354  
GPT-4o-mini | OpenAI | 0.356  
Claude Sonnet 4.5 | Anthropic | 0.317  
Gemini 2.5 Pro | Google | 0.324  
Llama 4 Maverick | Meta | 0.299  
Llama 4 Scout | Meta | 0.332  
Qwen3-32B | Alibaba | 0.282  
Mistral Large 3 | Mistral | 0.338  
DeepSeek-V3 | DeepSeek | 0.321  
Table 1: Judge panel: 9 judges from 7 model families. Error rates are computed on ChaosNLI-MNLI against the 100-annotator majority label. The panel does not meaningfully outperform the best individual judge on any dataset (Table 3).

### 3.3 Effective Sample Size (neffn_{\text{eff}})

We measure effective independence using two complementary approaches.

#### Kish design-effect neffn_{\text{eff}}.

For each judge, we construct a binary error vector 𝐞j∈{0,1}1000\mathbf{e}_{j}\in\\{0,1\\}^{1000} where ej,i=1e_{j,i}=1 if judge jj disagrees with the ChaosNLI majority label on item ii. We compute the pairwise phi coefficient ϕj​k\phi_{jk} between all (92)=36\binom{9}{2}=36 judge pairs, then apply the Kish formula:

| neff=k1+(k−1)​ϕ¯n_{\text{eff}}=\frac{k}{1+(k-1)\bar{\phi}} |  | (1)  
---|---|---|---  
  
where kk is the number of judges and ϕ¯=1(k2)​∑j<kϕj​k\bar{\phi}=\frac{1}{\binom{k}{2}}\sum_{j<k}\phi_{jk} is the mean pairwise correlation (Kish, 1965). For binary error vectors, the phi coefficient reduces to the Pearson product-moment correlation, which is the quantity the Kish formula requires (Kish, 1965). Alternative association measures (e.g., Cohen’s kappa) conflate prevalence with dependence; phi isolates the linear dependence that directly degrades majority-vote performance. This formula assumes exchangeability (approximately equal pairwise correlations); we validate this assumption against the eigenvalue method below.

#### Eigenvalue neffn_{\text{eff}}.

As a robustness check that does not assume exchangeability, we compute neffeigen=k/λmaxn_{\text{eff}}^{\text{eigen}}=k/\lambda_{\max}, where λmax\lambda_{\max} is the largest eigenvalue of the k×kk\times k phi correlation matrix (Bretherton et al., 1999, cf.). Under perfect independence, λmax=1\lambda_{\max}=1 and neffeigen=kn_{\text{eff}}^{\text{eigen}}=k; under perfect correlation, λmax=k\lambda_{\max}=k and neffeigen=1n_{\text{eff}}^{\text{eigen}}=1.

#### Bootstrap confidence interval.

We resample the 1,000 items with replacement 10,000 times, recomputing neffn_{\text{eff}} (Kish) for each resample, and report the 2.5th–97.5th percentile interval. This captures uncertainty over the item sample for _these specific judges_ on ChaosNLI; it does not generalize to other datasets or judge panels.

### 3.4 Condorcet Null Model

To translate neffn_{\text{eff}} into a concrete accuracy gap, we construct a Condorcet null model that simulates what majority-vote accuracy _would be_ if judges voted independently with the same error characteristics. Crucially, this tests _conditional_ independence: whether judges vote independently given the item’s gold label and difficulty level. Some correlation from shared item difficulty is expected and accounted for; the gap measures dependence _beyond_ what difficulty explains.

#### Confusion-matrix calibration.

For each judge jj, we estimate the 3×\times3 confusion matrix P⁡(y^=c′∣y=c,j)P(\hat{y}=c^{\prime}\mid y=c,j) from their labels on the 1,000 items. This captures class-specific error patterns (e.g., a judge that confuses entailment with neutral more than with contradiction).

#### Item-aware simulation.

We stratify items into three difficulty bins by human entropy (terciles at the 33rd and 67th percentiles) and estimate per-judge, per-bin confusion matrices. We report results for 3 bins (terciles) as the default; §4 reports sensitivity to 10 bins, and split-half cross-validation confirms minimal overfitting (Appendix E). For each item, we run 10,000 Monte Carlo simulations: sample each judge’s vote independently from the appropriate bin-specific confusion matrix given the item’s gold label, compute majority vote, and record accuracy. This yields a predicted accuracy for each panel-entropy bin under the independence assumption, accounting for shared item difficulty.

#### Condorcet gap.

The Condorcet gap is the difference between predicted (independent) and actual majority-vote accuracy, computed as a weighted average across panel-entropy bins (weighted by bin size). A negative gap indicates that actual accuracy falls _below_ the independent prediction. We compute a 95% bootstrap confidence interval by resampling items 1,000 times and re-estimating the full pipeline for each resample.

### 3.5 Statistical Tests

#### Permutation omnibus test.

To test whether the observed ϕ¯\bar{\phi} is significantly above chance, we conduct a stratified permutation test (10,000 permutations). Within each human-entropy stratum, we independently shuffle each judge’s error vector, breaking inter-judge correlations while preserving per-judge error rates and the difficulty structure. We compute ϕ¯\bar{\phi} on each permuted dataset and report the fraction of permuted statistics that equal or exceed the observed value.

#### Per-bin binomial tests.

For each discrete panel-entropy value, we conduct a one-sided binomial test of whether actual accuracy is significantly below the Condorcet prediction, with Wilson score confidence intervals. These per-bin tests are exploratory; the stratified permutation test serves as our primary omnibus significance test.

## 4 Results

### 4.1 Effective Independence

The 9-judge panel yields neff=2.18n_{\text{eff}}=2.18 with 95% bootstrap CI [2.07,2.31][2.07,2.31] (Table 2). The eigenvalue estimate (neffeigen=2.16n_{\text{eff}}^{\text{eigen}}=2.16) closely matches, validating the Kish exchangeability assumption for this panel. The mean pairwise phi is ϕ¯=0.391\bar{\phi}=0.391 (σ=0.111\sigma=0.111, range: [0.161,0.603][0.161,0.603]), and the independence ratio is neff/k=24.2%n_{\text{eff}}/k=24.2\%.

Metric | Value  
---|---  
Judges (kk) | 9  
Families | 7  
Items (nn) | 1,000  
neffn_{\text{eff}} (Kish) | 2.18 [2.07, 2.31]  
neffn_{\text{eff}} (eigenvalue) | 2.16  
λmax\lambda_{\max} | 4.17  
Mean ϕ\phi | 0.391 ±\pm 0.111  
Independence ratio | 24.2%  
Panel accuracy | 72.0%  
Best individual (Qwen3-32B) | 71.8%  
Panel lift | ++0.2pp  
Condorcet gap (weighted) | 22.0pp [19.5, 24.1]  
Gap explained by difficulty | 6.8%  
Permutation pp | <10−4<10^{-4}  
Table 2: Headline results. The 9-judge panel provides only 2.18 effective independent voters. The Condorcet gap measures the shortfall of actual accuracy below the Condorcet prediction for independent voters with the same per-judge error profiles. The panel’s 0.2pp lift is within noise and tie-breaking margin (11 ties, 1.1%).

The error distribution across items (Figure 1) reveals the signature of correlated errors: 290 items (29%) have all 9 judges correct and 51 (5.1%) have all 9 wrong — far more than any independence model predicts (<<1). Over-prediction of _contradiction_ accounts for 51% of all-wrong confusions despite comprising only 16.5% of gold labels (Appendix J).

Figure 1: Distribution of errors per item. Under independence, errors would concentrate around 2–4 per item (right bars). The observed distribution (left bars) shows excess mass at the extremes — 290 items with 0 errors and 51 with all 9 wrong (vs. <<1 expected) — the hallmark of correlated errors.

### 4.2 Condorcet Gap

Majority-vote accuracy is 72.0%, compared to the Condorcet prediction of approximately 94% for the item-aware model. The weighted Condorcet gap is 22.0 percentage points (95% CI: [19.5,24.1][19.5,24.1]pp). Only 6.8% of this gap is attributable to shared item difficulty; with 10 difficulty bins, the explained fraction rises to 13.5% on MNLI but 66–87% remains unexplained across all datasets. Split-half validation (ratio = 1.00) and the permutation test (p<10−4p<10^{-4}) confirm this is not overfitting.

The per-bin breakdown (Appendix C, Table 6) shows the gap is significant (p<0.05p<0.05) in 8 of 12 discrete panel-entropy levels. Even for unanimous items (panel entropy = 0, n=319n=319), accuracy is 90.9% — not the 99.99% that Condorcet would predict for 9 independent voters each with ∼\sim68% accuracy.

### 4.3 Permutation Test

The permutation omnibus test yields p<10−4p<10^{-4} (0 of 10,000 permutations reached the observed ϕ¯=0.391\bar{\phi}=0.391; permutation null: mean =0.060=0.060, SD =0.005=0.005, z=65.6z=65.6). This decisively rejects the null hypothesis that the observed inter-judge correlation is attributable to shared item difficulty alone.

### 4.4 Scaling: neff​(k)n_{\text{eff}}(k) vs. kk

Figure 2 shows how neffn_{\text{eff}} varies with panel size kk across all (9k)\binom{9}{k} subsets (full data in Appendix G). The empirical curve closely tracks the Kish prediction neff​(k)=k/(1+(k−1)⋅0.391)n_{\text{eff}}(k)=k/(1+(k-1)\cdot 0.391), with a hard asymptote at 1/ϕ¯≈2.61/\bar{\phi}\approx 2.6. The diminishing returns are severe: the first 5 judges contribute 90% of the achievable independence (neff=1.96n_{\text{eff}}=1.96 vs. 2.18). Adding judges 6–9 provides only +0.22+0.22 effective votes.

Figure 2: Effective independence neffn_{\text{eff}} as a function of panel size kk. The empirical mean (blue circles) closely follows the Kish prediction (red dashes), far below the perfect-independence diagonal (gray). The shaded region shows the min–max range across all (9k)\binom{9}{k} subsets. The asymptote at 1/ϕ¯≈2.61/\bar{\phi}\approx 2.6 means no panel of current models can exceed ∼\sim2.6 effective independent votes.

### 4.5 Cross-Dataset Replication

To test whether the independence deficit generalizes beyond a single NLI source corpus, we replicate the full analysis on 1,000 ChaosNLI-SNLI items (Bowman et al., 2015) (same 3-class task, different corpus) and 1,000 ChaosNLI-AlphaNLI items (Bhagavatula et al., 2020) (2-class abductive reasoning, fundamentally different task type). Table 3 summarizes the comparison.

Metric | MNLI | SNLI | AlphaNLI  
---|---|---|---  
Task type | 3-class NLI | 3-class NLI | 2-class abd.  
neffn_{\text{eff}} (Kish) | 2.18 [2.07, 2.31] | 2.35 [2.21, 2.51] | 2.48 [2.32, 2.69]  
Mean ϕ\phi | 0.391 | 0.354 | 0.328  
Panel acc. | 72.0% | 77.7% | 88.7%  
Best indiv. | 71.8% | 84.2% | 91.2%  
Panel lift | ++0.2pp | −-6.5pp | −-2.5pp  
Cond. gap (pp) | 22.0 [19.5, 24.1] | 14.0 [11.9, 16.1] | 7.6 [6.0, 9.1]  
Kripp. α\alpha | .550 [.528, .573] | .546 [.521, .568] | .577 [.549, .601]  
Human neffn_{\text{eff}} | 5.79 | 4.78 | 4.03  
Perm. pp | <10−4<10^{-4} | <10−4<10^{-4} | <10−4<10^{-4}  
Split-half | 1.00 | 0.96 | 1.00  
Table 3: Cross-dataset comparison. All three datasets show neff≪kn_{\text{eff}}\ll k, significant Condorcet gaps, and negligible or negative panel lift. The independence deficit is remarkably stable (neff≈2.2n_{\text{eff}}\approx 2.2–2.52.5) despite varying task types, label sets, and base accuracy levels. Krippendorff’s α<0.667\alpha<0.667 on all datasets, indicating only moderate inter-judge agreement by annotation science standards. Human neffn_{\text{eff}} is estimated under an exchangeability assumption by sampling from the aggregate ChaosNLI label distribution (see footnote in text).

The core finding replicates across all three datasets: neffn_{\text{eff}} remains in the narrow 2.2–2.5 range despite panel accuracy ranging from 72% to 89%, and the best individual judge matches or outperforms the panel in every case. On MNLI, the panel edges the best judge by a negligible 0.2pp; on SNLI and AlphaNLI, the best individual wins convincingly (−-6.5pp and −-2.5pp). The panel underperforms relative to the _Condorcet prediction_ , which already accounts for each judge’s individual accuracy — the gap is driven by correlated errors, not merely vote dilution. The AlphaNLI result is particularly noteworthy: a 2-class abductive reasoning task with fundamentally different cognitive demands, yet neff=2.48n_{\text{eff}}=2.48. Condorcet gaps decrease with base accuracy (22.0pp →\to 14.0pp →\to 7.6pp), as expected when higher accuracy leaves less room for correlated errors.

Krippendorff’s α<0.667\alpha<0.667 on all datasets, indicating only moderate agreement by annotation standards (Krippendorff, 2011). Human annotator panels achieve roughly 2×2\times higher neffn_{\text{eff}} (4.04.0–5.85.8 vs. LLMs’ 2.22.2–2.52.5), suggesting the deficit is specific to LLM judges.11 1 Human neffn_{\text{eff}} is estimated by sampling 10 labels per item from the aggregate ChaosNLI distribution, treating annotators as exchangeable.

Split-half cross-validation confirms no overfitting (ratios 0.96–1.00), and neffn_{\text{eff}} stabilizes by N≈200N\approx 200 (Appendix F).

### 4.6 Robustness to Prompt, Temperature, and Task

To test whether the independence deficit is a prompt or decoding artifact, we re-run all 9 judges on the same 1,000 MNLI items under four variants: (1) reframed wording, (2) reversed label order, (3) chain-of-thought reasoning, and (4) temperature T=0.5T=0.5. We also evaluate on 1,000 RewardBench items (Lambert et al., 2025) — a pairwise preference task with deterministic gold labels, sampled via proportional stratified sampling across four categories, using the official MT-Bench pairwise judge prompt with A/B position randomization.

Condition | neffn_{\text{eff}} [95% CI] | ϕ¯\bar{\phi} | Panel | Gap  
---|---|---|---|---  
Baseline (T=0T{=}0) | 2.18 [2.07, 2.31] | .391 | 72.0% | 22.0pp  
Reframed prompt | 2.17 [2.05, 2.30] | .394 | 72.5% | 21.5pp  
Reversed labels | 2.15 [2.03, 2.27] | .399 | 72.9% | 21.3pp  
Chain-of-thought | 1.94 [1.85, 2.04] | .456 | 69.2% | 22.3pp  
Temp T=0.5T{=}0.5 | 2.17 [2.06, 2.30] | .393 | 71.8% | 21.9pp  
RewardBench | 1.99 [1.83, 2.20] | .440 | 92.7% | 6.8pp  
Table 4: Robustness of neffn_{\text{eff}} across prompt variants and chain-of-thought (same 1,000 MNLI items, 9 judges) and a different task type (RewardBench: pairwise preference, 9 judges, 1,000 items). “Gap” is the Condorcet gap (predicted −- actual panel accuracy). neffn_{\text{eff}} is stable in the 1.94–2.18 range across all conditions; chain-of-thought increases correlation.

Table 4 shows that neffn_{\text{eff}} is remarkably stable. Varying prompt wording, label ordering, and temperature has essentially no effect: neffn_{\text{eff}} ranges from 2.15 to 2.18, with overlapping 95% bootstrap CIs. The reversed-label variant rules out position bias (Wang et al., 2024) as a driver: the near-identical neffn_{\text{eff}} (2.15 vs. 2.18) confirms that correlation is robust to label ordering. Chain-of-thought actually _increases_ correlation (ϕ¯=.456\bar{\phi}=.456, neff=1.94n_{\text{eff}}=1.94) — shared reasoning amplifies shared errors. This stability rules out prompt engineering artifacts.

On RewardBench — a binary pairwise preference task with deterministic gold labels — neff=1.99n_{\text{eff}}=1.99 [1.83, 2.20]. The smaller Condorcet gap (6.8pp vs. 21–22pp on MNLI) reflects higher panel accuracy (92.7%), but ϕ=0.44\phi=0.44 confirms high error correlation regardless of task type. Same-family correlation is larger on RewardBench (+0.109+0.109) than MNLI (+0.047+0.047). All 9 judges show residual A-preference despite the anti-bias prompt; the NLI results, structurally immune to position effects, confirm that correlation is not a position-bias artifact.

## 5 Analysis and Discussion

### 5.1 Leave-One-Out: Which Judges Matter?

Leave-one-out analysis (Appendix H, Table 9) reveals that herding is systemic: Δ​neff\Delta n_{\text{eff}} ranges narrowly from −0.13-0.13 to +0.02+0.02 across judges, with no single model driving the effect. Removing DeepSeek-V3 or Mistral Large 3 _increases_ neffn_{\text{eff}} (their errors are most correlated with the panel), while removing Llama 4 Scout decreases it the most.

Most strikingly, removing Gemini 2.5 Pro — highly correlated with Claude (ϕ=0.60\phi=0.60) and GPT-4o (0.520.52) — _increases_ accuracy by 1.3pp (95% CI [+0.1,+2.6][+0.1,+2.6]), and 6 of 9 removals improve accuracy. The three judges whose removal hurts (Maverick, Scout, Qwen3) include the two most individually accurate. That adding voters can _hurt_ is theoretically predicted under positive correlation (Austen-Smith and Banks, 1996), but has not previously been demonstrated in the LLM judge setting.

### 5.2 Stratified and Subset Analyses

When stratified by gold NLI class (Appendix H, Table 10), herding is present across all three classes: neffn_{\text{eff}} ranges from 1.85 (contradiction, ϕ¯=0.482\bar{\phi}=0.482) to 2.40 (neutral). Even on the 179 “easy” items (17.9%) where ≥\geq80% of human annotators agree, neff=2.67n_{\text{eff}}=2.67 — higher than the full set but far from 9, ruling out the explanation that herding is merely a response to item ambiguity. Panel entropy correlates with human entropy (ρs=0.301\rho_{s}=0.301) and predicts majority-vote correctness (rp​b=−0.342r_{pb}=-0.342). Among unanimous items (n=319n=319), accuracy is 90.9%; with any disagreement (n=681n=681), it drops to 63.1%. The 9.1% error rate on unanimous items is dramatically higher than the ∼\sim0.02% that independence would predict.

### 5.3 Same-Family vs. Cross-Family Correlation

Same-family pairs (OpenAI-OpenAI: ϕ=0.437\phi=0.437; Meta-Meta: ϕ=0.435\phi=0.435) are only slightly more correlated than the cross-family mean (ϕ¯cross=0.389\bar{\phi}_{\text{cross}}=0.389, difference = 0.047). The three highest-correlated pairs are all _cross-family_ : Claude ×\times Gemini (ϕ=0.603\phi=0.603), GPT-4o ×\times Claude (ϕ=0.588\phi=0.588), and Mistral ×\times DeepSeek (ϕ=0.564\phi=0.564). When restricted to one judge per family (7 judges, selecting the best in each), neffn_{\text{eff}} _decreases_ to 1.93 — a selection effect where the best judges concentrate errors on the same hard items (full matrix in Appendix B). Family diversity alone does not recover independence.

### 5.4 Does Smarter Aggregation Help?

A natural question is whether the Condorcet gap can be closed by replacing naïve majority voting with more sophisticated aggregation. We test three established methods: (1) Dawid-Skene EM (Dawid and Skene, 1979), which estimates per-judge confusion matrices and true label posteriors via expectation-maximization without access to gold labels; (2) accuracy-weighted voting, which weights each judge by their individual accuracy (using 5-fold cross-validation to avoid label leakage); and (3) Markowitz-optimal weighting, which selects weights to minimize correlated error via the inverse phi correlation matrix (also cross-validated). The latter two methods use gold labels for weight estimation — giving them an _oracle advantage_ that would be unavailable in practice.

Method | Orac. | MNLI | SNLI | Alpha. | RB  
---|---|---|---|---|---  
Majority vote | No | 72.0 | 77.7 | 88.7 | 92.7  
Dawid-Skene EM | No | 70.7 | 77.6 | 89.5 | 92.7  
Acc-weighted (CV) | Yes | 72.2 | 77.7 | 88.7 | 92.7  
Best individual | — | 71.8 | 84.2 | 91.2 | 95.5  
Condorcet pred. | — | 94.0 | 91.7 | 96.3 | 99.5  
Table 5: Aggregation methods vs. the Condorcet gap. Even with oracle access to gold labels (accuracy-weighted, 5-fold CV), the best stable method closes at most 11% of the gap across all four datasets. The best individual judge outperforms all aggregation methods on SNLI, AlphaNLI, and RewardBench (RB). Markowitz-optimal weighting is omitted from the main table due to instability (Appendix I).

Table 5 shows the results. On MNLI, accuracy-weighted voting (5-fold CV) achieves 72.2% — a gain of just 0.2pp over majority vote, closing less than 1% of the 22.0pp Condorcet gap. Dawid-Skene actually _underperforms_ majority vote on MNLI (70.7%), illustrating that unsupervised EM can misestimate error rates when judges are highly correlated. On AlphaNLI, Dawid-Skene closes 10.5% of the gap — the best stable result across all four datasets. On SNLI, AlphaNLI, and RewardBench, the best individual judge outperforms _every_ aggregation method, including those with oracle access. Note that identifying the best individual also requires oracle access to gold labels; the comparison highlights that even oracle-informed _weighting_ cannot overcome correlation. Markowitz-optimal (phi-optimal) weighting closes 20.6% of the gap on RewardBench but underperforms majority vote on AlphaNLI, illustrating the instability of correlation-based weighting (Appendix I).

With only ∼\sim2.2 effective independent votes, no weighting scheme can extract a third independent perspective — including calibrated soft voting (Ni et al., 2026; Maia Polo et al., 2025). Our oracle-access stable methods close at most 11% of the gap. Confounder-aware methods (Zhao et al., 2025) face the same structural limit: same-family pairs are only marginally more correlated than cross-family (++0.047; §5.3), and the three highest-correlated pairs are all cross-family.

## 6 Conclusion

We have applied the Kish effective sample size framework to LLM judge panels, providing the first measurement that directly connects inter-judge correlation to majority-vote reliability via Condorcet theory. The independence deficit (neff≈2.0n_{\text{eff}}\approx 2.0–2.52.5) is stable across three NLI datasets, three prompt variants, two temperature settings, and a pairwise preference task (RewardBench), confirming that the correlation is structural rather than an artifact of any particular experimental choice. Adding judges does not help: the panel matches or underperforms the best individual judge across all conditions. Established stable aggregation methods close at most 11% of the Condorcet gap (unstable correlation-aware weighting reaches 21% on one dataset but hurts on others), confirming that the bottleneck is in the inputs, not the algorithm.

These results have direct practical implications. Paying for 9 opinions but receiving the informational equivalent of ∼\sim2 is a substantial inefficiency: a 5-judge panel already captures 90% of achievable independence. Unanimous panel agreement carries far less weight than it appears — our data show a 9.1% error rate on unanimous items, vs. ∼\sim0.02% under independence. We recommend computing neffn_{\text{eff}} as a standard panel diagnostic: if neff/k<0.5n_{\text{eff}}/k<0.5, results should be treated with caution.

Our findings complement Dorner et al. (2025) and Jiang et al. (2025). The path forward requires models that genuinely differ in how they process information — not merely different brand names on similar architectures. The Kish formula makes progress measurable: halving ϕ¯\bar{\phi} from 0.39 to 0.20 would raise neffn_{\text{eff}} from 2.2 to 3.5, closing roughly half the Condorcet gap. Whether architecturally diverse models, specialist fine-tuning, or hybrid human-LLM panels can achieve this remains an open question.

## Limitations

#### Classification tasks.

Our results are replicated across three ChaosNLI NLI datasets and a pairwise preference task (RewardBench), with consistent neff≈2.0n_{\text{eff}}\approx 2.0–2.52.5. The cross-task replication strengthens generalizability, but all four remain classification or binary preference tasks. The degree of inter-judge correlation may differ on open-ended generation evaluation or code review, where output structure differs fundamentally.

#### Gold standard validity.

The 100-annotator majority label is our ground truth, but for high-entropy items, the majority label may represent a plurality preference rather than a “correct” answer. Appendix D reports distributional alignment metrics confirming the same pattern without reducing labels to binary accuracy.

#### Snapshot in time.

Our results reflect a snapshot of current frontier models. Future models may exhibit lower correlation, but the _framework_ (neffn_{\text{eff}} and Condorcet gap) remains applicable.

#### Condorcet model calibration.

The confusion matrices are estimated from the same items on which we measure the gap. Split-half cross-validation (Appendix E) yields overfitting ratios of 0.96–1.00 across the three datasets, confirming negligible overfitting.

#### Prompt and decoding choices.

We test four prompt variants (including chain-of-thought) and two temperature settings (§4.6), finding neffn_{\text{eff}} stable in the 1.94–2.18 range. Chain-of-thought actually _increases_ correlation (neff=1.94n_{\text{eff}}=1.94). More radical prompt reformulations — such as few-shot exemplars or persona-based prompting — could in principle alter the correlation structure. We use RewardBench (Lambert et al., 2025) rather than the more recent RewardBench 2 (Malik et al., 2025) because the latter uses LLM-derived gold labels for several categories (e.g., GPT-4o and Claude consensus for Factuality), which would introduce circularity when evaluating LLM judges drawn from the same model families.

#### Bootstrap CI interpretation.

Our bootstrap CI captures uncertainty over items for _these specific judges_. It does not account for judge selection uncertainty — a different panel might yield a different neffn_{\text{eff}}.

## Ethics Statement

This work uses publicly available benchmark data (ChaosNLI) and commercial LLMs. No human subjects were recruited for this study. The ChaosNLI annotations were collected by Nie et al. (2020) and are publicly released. Our findings highlight limitations of LLM judge panels, which we believe serve the public interest by encouraging more careful deployment of automated evaluation systems. Claude (Anthropic) was used for writing assistance.

## Data Availability

ChaosNLI-MNLI is publicly available via HuggingFace (metaeval/chaos-mnli-ambiguity); ChaosNLI-SNLI and ChaosNLI-AlphaNLI are available from the ChaosNLI GitHub repository (Nie et al., 2020). RewardBench is available via HuggingFace (allenai/reward-bench; Lambert et al. 2025).

## References

  * Austen-Smith and Banks (1996) David Austen-Smith and Jeffrey S. Banks. 1996.  Information aggregation, rationality, and the Condorcet jury theorem.  _American Political Science Review_ , 90(1):34–45. 
  * Bhagavatula et al. (2020) Chandra Bhagavatula, Ronan Le Bras, Chaitanya Malaviya, Keisuke Sakaguchi, Ari Holtzman, Hannah Rashkin, Doug Downey, Scott Wen-tau Yih, and Yejin Choi. 2020\.  Abductive commonsense reasoning.  In _Proceedings of the International Conference on Learning Representations (ICLR)_. 
  * Bowman et al. (2015) Samuel R. Bowman, Gabor Angeli, Christopher Potts, and Christopher D. Manning. 2015\.  A large annotated corpus for learning natural language inference.  In _Proceedings of the 2015 Conference on Empirical Methods in Natural Language Processing (EMNLP)_ , pages 632–642. 
  * Bretherton et al. (1999) Christopher S Bretherton, Martin Widmann, Viktor P Dymnikov, John M Wallace, and Ileana Bladé. 1999.  The effective number of spatial degrees of freedom of a time-varying field.  _Journal of Climate_ , 12(7):1990–2009. 
  * Calderon et al. (2025) Nitay Calderon, Roi Reichart, and Rotem Dror. 2025.  The alternative annotator test for LLM-as-a-judge: How to statistically justify replacing human annotators with LLMs.  In _Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (ACL)_ , pages 16051–16081. 
  * Chehbouni et al. (2025) Khaoula Chehbouni, Mohammed Haddou, Jackie Chi Kit Cheung, and Golnoosh Farnadi. 2025.  Neither valid nor reliable? investigating the use of LLMs as judges.  In _Advances in Neural Information Processing Systems (NeurIPS)_. 
  * Dawid and Skene (1979) A. P. Dawid and A. M. Skene. 1979.  Maximum likelihood estimation of observer error-rates using the EM algorithm.  _Journal of the Royal Statistical Society: Series C (Applied Statistics)_ , 28(1):20–28. 
  * de Condorcet (1785) Marquis de Condorcet. 1785.  _Essai sur l’application de l’analyse à la probabilité des décisions rendues à la pluralité des voix_.  Imprimerie Royale, Paris. 
  * Dietterich (2000) Thomas G. Dietterich. 2000.  Ensemble methods in machine learning.  In _International Workshop on Multiple Classifier Systems (MCS)_ , pages 1–15. Springer. 
  * Dorner et al. (2025) Florian E. Dorner, Vivian Yvonne Nastl, and Moritz Hardt. 2025.  Limits to scalable evaluation at the frontier: LLM as judge won’t beat twice the data.  In _International Conference on Learning Representations (ICLR)_.  Oral presentation. 
  * Jiang et al. (2025) Liwei Jiang, Yuanjun Chai, Margaret Li, Mickel Liu, Raymond Fok, Nouha Dziri, Yulia Tsvetkov, Maarten Sap, Alon Albalak, and Yejin Choi. 2025.  Artificial hivemind: The open-ended homogeneity of language models (and beyond).  In _Advances in Neural Information Processing Systems (NeurIPS)_.  Best Paper Award. 
  * Jung et al. (2025) Jaehun Jung, Faeze Brahman, and Yejin Choi. 2025.  Trust or escalate: LLM judges with provable guarantees for human agreement.  In _International Conference on Learning Representations (ICLR)_. 
  * Kim et al. (2025) Elliot Kim, Avi Garg, Kenny Peng, and Nikhil Garg. 2025.  Correlated errors in large language models.  In _International Conference on Machine Learning (ICML)_. 
  * Kish (1965) Leslie Kish. 1965.  _Survey Sampling_.  John Wiley & Sons, New York. 
  * Krippendorff (2011) Klaus Krippendorff. 2011.  [Computing Krippendorff’s alpha-reliability](https://repository.upenn.edu/entities/publication/034a6030-c584-4d14-9d3d-7b7e8d16df20).  _Departmental Papers (ASC), University of Pennsylvania_. 
  * Lambert et al. (2025) Nathan Lambert, Valentina Pyatkin, Jacob Morrison, LJ Miranda, Bill Yuchen Lin, Khyathi Chandu, Nouha Dziri, Sachin Kumar, Tom Zick, Yejin Choi, Noah A. Smith, and Hannaneh Hajishirzi. 2025.  RewardBench: Evaluating reward models for language modeling.  In _Findings of the Association for Computational Linguistics: NAACL 2025_ , pages 1755–1797. 
  * Lee et al. (2023) Noah Lee, Na Min An, and James Thorne. 2023.  Can large language models capture dissenting human voices?  In _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP)_ , pages 4569–4585. 
  * Lefort et al. (2024) Baptiste Lefort, Eric Benhamou, Jean-Jacques Ohana, Beatrice Guez, David Saltiel, and Thomas Jacquot. 2024.  Examining independence in ensemble sentiment analysis: A study on the limits of large language models using the Condorcet jury theorem.  _arXiv preprint arXiv:2409.00094_. 
  * Maia Polo et al. (2025) Felipe Maia Polo, Xinhe Wang, Mikhail Yurochkin, Gongjun Xu, Moulinath Banerjee, and Yuekai Sun. 2025.  Bridging human and LLM judgments: Understanding and narrowing the gap.  In _Advances in Neural Information Processing Systems (NeurIPS)_. 
  * Malik et al. (2025) Saumya Malik, Valentina Pyatkin, Sander Land, Jacob Morrison, Noah A. Smith, Hannaneh Hajishirzi, and Nathan Lambert. 2025.  Rewardbench 2: Advancing reward model evaluation.  _arXiv preprint arXiv:2506.01937_. 
  * Ni et al. (2026) Jingwei Ni, Yu Fan, Vilém Zouhar, Donya Rooein, Alexander Miserlis Hoyle, Mrinmaya Sachan, Markus Leippold, Dirk Hovy, and Elliott Ash. 2026.  Can reasoning help large language models capture human annotator disagreement?  In _Proceedings of the 2026 Conference of the European Chapter of the Association for Computational Linguistics (EACL)_. 
  * Nie et al. (2020) Yixin Nie, Xiang Zhou, and Mohit Bansal. 2020.  What can we learn from collective human opinions on natural language inference data?  In _Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP)_ , pages 9131–9143. 
  * Pavlick and Kwiatkowski (2019) Ellie Pavlick and Tom Kwiatkowski. 2019.  Inherent disagreements in human textual inferences.  _Transactions of the Association for Computational Linguistics_ , 7:677–694. 
  * Plank (2022) Barbara Plank. 2022.  The “problem” of human label variation: On ground truth in data, modeling and evaluation.  In _Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing (EMNLP)_. 
  * Raykar et al. (2010) Vikas C. Raykar, Shipeng Yu, Linda H. Zhao, Gerardo Hermosillo Valadez, Charles Florin, Luca Bogoni, and Linda Moy. 2010.  Learning from crowds.  _Journal of Machine Learning Research_ , 11:1297–1322. 
  * Surowiecki (2004) James Surowiecki. 2004.  _The Wisdom of Crowds_.  Doubleday, New York. 
  * Thakur et al. (2025) Aman Singh Thakur, Kartik Choudhary, Venkat Srinik Ramayapally, Sankaran Vaidyanathan, and Dieuwke Hupkes. 2025.  Judging the judges: Evaluating alignment and vulnerabilities in LLMs-as-judges.  In _Proceedings of the Fourth Workshop on Generation, Evaluation and Metrics (GEM)_ , pages 404–430. 
  * Turkmen et al. (2026) Yigit Turkmen, Baturalp Buyukates, and Melih Bastopcu. 2026.  Don’t always pick the highest-performing model: An information theoretic view of LLM ensemble selection.  _arXiv preprint arXiv:2602.08003_. 
  * Verga et al. (2024) Pat Verga, Sebastian Hofstätter, Sophia Althammer, Yixuan Su, Aleksandra Piktus, Arkady Arkhangorodsky, Minjie Xu, Naomi White, and Patrick Lewis. 2024\.  Replacing judges with juries: Evaluating LLM generations with a panel of diverse models.  _arXiv preprint arXiv:2404.18796_. 
  * Wang et al. (2024) Peiyi Wang, Lei Li, Liang Chen, Zefan Cai, Dawei Zhu, Binghuai Lin, Yunbo Cao, Lingpeng Kong, Qi Liu, Tianyu Liu, and Zhifang Sui. 2024.  Large language models are not fair evaluators.  In _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (ACL)_ , pages 9440–9450. 
  * Williams et al. (2018) Adina Williams, Nikita Nangia, and Samuel R. Bowman. 2018.  A broad-coverage challenge corpus for sentence understanding through inference.  In _Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics (NAACL)_ , pages 1112–1122. 
  * Ye et al. (2025) Jiayi Ye, Yanbo Wang, Yue Huang, Dongping Chen, Qihui Zhang, Nuno Moniz, Tian Gao, Werner Geyer, Chao Huang, Pin-Yu Chen, Nitesh V Chawla, and Xiangliang Zhang. 2025.  Justice or prejudice? quantifying biases in LLM-as-a-judge.  In _International Conference on Learning Representations (ICLR)_. 
  * Zhao et al. (2025) Jitian Zhao, Changho Shin, Tzu-Heng Huang, Satya Sai Srinath Namburi, and Frederic Sala. 2025.  From many voices to one: A statistically principled aggregation of LLM judges.  In _NeurIPS 2025 Workshop on Reliable ML from Unreliable Data_. 
  * Zheng et al. (2023) Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, and Ion Stoica. 2023.  Judging LLM-as-a-judge with MT-Bench and Chatbot Arena.  In _Advances in Neural Info
