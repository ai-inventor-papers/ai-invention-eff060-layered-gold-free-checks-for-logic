URL: https://arxiv.org/html/2608.05439 | FULL FETCH | 2026-09-24T01:53:37Z
warning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
URL: https://arxiv.org/html/2608.05439
Type: HTML
Length: 83754 chars (truncated)

--- Content ---

##### Report GitHub Issue

×

Title:

Content selection saved. Describe the issue below:

Description:

Submit without GitHub Submit in GitHub

arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[ Back to arXiv ](/)

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) Report Issue [ Back to Abstract ](/abs/2608.05439v1 "Back to abstract page") [ Download PDF](/pdf/2608.05439v1 "Download PDF") [ ](javascript:toggleNavTOC\(\); "Toggle navigation") [ ](javascript:toggleReadingMode\(\); "Disable reading mode, show header and footer")

  1. Abstract
  2. 1 Introduction
  3. 2 Background and Problem
  4. 3 Methodology
     1. 3.1 Semantic Consistency Scoring
     2. 3.2 Risk-Calibrated Selection
     3. 3.3 Filtering Out-of-Distribution Instructions
  5. 4 Experimental Results
     1. Tasks and data.
     2. LLM Translators.
     3. Scoring and calibration configuration.
     4. Baseline and metrics.
  6. References
  7. A Appendix
     1. A.1 Reproducing Results
     2. A.2 Computing infrastructure.
     3. A.3 Example Prompt
     4. A.4 Additional Results: LTL
     5. A.5 Executed-Error Counts
     6. A.6 Proof of Theorem 



[ License: arXiv.org perpetual non-exclusive license ](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2608.05439v1 [cs.AI] 05 Aug 2026

# SCP-NL2TL: Selective Conformal Prediction with Semantic Verification for Natural Language to Temporal Logic Specifications 

Yixuan Wang  Affiliation: University of California, Riverside, Riverside, CA, USA  Licheng Luo  Affiliation: University of California, Riverside, Riverside, CA, USA  Yu Fu  Affiliation: University of California, Riverside, Riverside, CA, USA  Kaidi Xu  Affiliation: City University of Hong Kong, Hong Kong SAR, China  Yue Dong  Affiliation: University of California, Riverside, Riverside, CA, USA  Mingyu Cai  Email: [ ywang1457@ucr.edu, lichengl@ucr.edu, yfu093@ucr.edu kaidixu at cityu.edu.hk, yue.dong@ucr.edu, mingyuc@ucr.edu ](mailto:) Affiliation: University of California, Riverside, Riverside, CA, USA 

###### Abstract

Translating natural language instructions into machine-interpretable formal specifications enables robots and autonomous systems to plan, reason, and formally verify their behavior. However, existing translation models typically generate a specification for every input, even when the result is unreliable or fails to capture the user’s intent, creating risks in safety-critical applications. Inspired by selective conformal prediction, we propose a selective translation framework that not only generates formal specifications but also determines when they can be trusted. Reliability is scored by two complementary black-box signals, the fidelity of the specification back-translated into natural language and the dispersion of repeated translations under exact semantic equivalence, which fail on different errors and jointly separate incorrect translations more sharply than either alone. Conformal risk control calibrates this score into a decision that accepts a specification or abstains, with a distribution-free bound on the rate at which incorrect specifications are accepted for execution, and a conformal anomaly detector on instruction embeddings screens out-of-distribution inputs before any translation is attempted. The proposed framework is general across formal specification languages, with experiments on Signal Temporal Logic (STL), Linear Temporal Logic (LTL), and geometric Spatio-Temporal Logic (SpaTiaL) demonstrating improved translation reliability, robustness under the evaluated cross-tier shifts, and effective uncertainty-aware abstention. This work establishes a foundation for trustworthy natural language interfaces by enabling AI systems to recognize when generated specifications may not be reliable. Project materials are available at [sites.google.com/ucr.edu/scpnl2tl](https://sites.google.com/ucr.edu/scpnl2tl?usp=sharing).

A Preprint   
  
  
---  
  
_Keywords_ Natural Language to Temporal Logic Translation ⋅\cdot Conformal Risk Control ⋅\cdot Selective Prediction

## 1 Introduction

Translating natural language instructions into machine-interpretable formal specifications enables robots and autonomous systems to plan, reason, and formally verify their behavior [1, 2, 3, 4]. Formal languages such as Linear Temporal Logic (LTL), Signal Temporal Logic (STL), and geometric Spatio-Temporal Logic (SpaTiaL) provide representations of temporal and spatial requirements [5, 6, 7], but writing them requires formal methods expertise. Recent natural language to temporal logic (NL2TL) systems have made this process more accessible using semantic parsing, sequence models, and, more recently, pretrained language models with structured intermediate representations [8, 9, 10]. Although these methods substantially improve translation accuracy and structural validity, they invariably generate a specification for every input.

Always producing a specification is undesirable in safety-critical applications. A formula may be syntactically valid yet semantically incorrect by assigning an incorrect predicate, argument, temporal operator, interval, logical scope, or spatial relation, causing downstream planners or verifiers to execute behavior that does not reflect the user’s intent. A practical NL2TL system should therefore determine not only what specification to generate, but also whether it is sufficiently reliable to be executed. Standard evaluation metrics offer no such judgment, as exact-match accuracy characterizes average benchmark performance rather than the trustworthiness of an individual translation [11, 12, 13, 14]. Conformal prediction (CP) supplies the statistical machinery for such a judgment. From any heuristic score and a set of calibration examples, it produces a prediction set that covers the true label at a user-specified rate, requiring only that calibration and test data be exchangeable [15]. The guarantee, however, is stated over sets, and a planner executes one formula rather than weighing several [16, 17]; a set of candidate specifications has nothing to hand it. Recent work has redirected this machinery from covering an answer toward declining to give one. Conformal risk control generalizes the coverage target to any bounded monotone loss [18], and selective conformal procedures add a second decision ahead of the first, testing whether the calibration data speak for a given test point and withholding a response when they do not [19]. Across this line, abstention becomes an outcome the procedure is calibrated to produce rather than an admission that it failed.

We propose a selective layer to any translator that either returns or withholds its generated formula, calibrating the decision so the rate of incorrect specifications reaching execution satisfies a user-defined risk budget. Unlike prior conformal methods that calibrate prediction sets using model confidence, our framework treats the translator as a black box and directly controls the risk of the single specification executed by the planner. Instead of relying on token likelihoods, we score translations using two complementary semantic signals: back-translation, which measures agreement with the instruction, and repeated sampling, which measures semantic consistency across translations. An instruction-level conformal test further rejects out-of-distribution inputs before translation. Across STL, LTL, and SpaTiaL, our method consistently satisfies the target risk budget, while coverage-calibrated baselines do not, and the instruction-level filter further improves robustness under distribution shift. The core contributions can be summarized as follows:

  * •

To the best of our knowledge, this is the first selective translation framework for NL2TL that augments any translator with an accept-or-abstain mechanism and bounds the rate at which incorrect temporal logic specifications are accepted for execution.

  * •

We introduce a semantic consistency score that combines back-translation fidelity and semantic agreement across repeated translations, improving discrimination between correct and incorrect specifications.

  * •

We incorporate an instruction-level conformal anomaly detector before calibration to identify out-of-distribution inputs, bound in-distribution deferrals, and improve robustness under distribution shift.




Related Work. Translating natural language into formal task specifications has been studied using grammar-based methods, semantic parsing, and sequence models for robotics and cyber-physical systems [20, 21, 22, 8]. Recent approaches leverage pretrained language models, structured intermediate representations, retrieval augmentation, model-checker feedback, and grammar-constrained decoding to improve translation accuracy and structural validity [9, 23, 24, 25, 26, 10, 27]. These methods focus on generating or refining executable specifications, but they always return a formula regardless of its reliability. ConformalNL2LTL attains a guaranteed translation success rate by building the formula through conformal QA steps that escalate uncertain decisions to a stronger model or the user [28]. Our work is complementary: instead of modifying the translator, we develop a model-agnostic selection layer that determines whether a generated specification should be accepted or withheld.

Conformal prediction has recently been applied to language models for generation sets, prompt selection, API-only uncertainty estimation, response validity, factuality, and selective generation [29, 30, 31, 32, 33, 34]. Related work has also studied semantic uncertainty [35], conformal procedures under non-exchangeability and distribution shift [36, 37, 38], and conformal significance testing for uncertainty outlier detection [19]. A parallel line acquires specifications from system behavior rather than language, learning STL formulas through differentiable robustness and neural structures [39, 40, 41, 42], with conformal prediction certifying the inferred formulas [43, 44]. Conformal risk control further extends conformal calibration from coverage guarantees to bounded monotone losses [18]. The language-model frameworks calibrate over a prediction set and derive their nonconformity from model confidence, token likelihoods, or sampled responses, none of which is available for a black-box translator whose output is a single executable formula. Conformal prediction has also entered language-instructed robot planning, calibrating when an LLM planner should proceed, seek help, or escalate [45, 46, 47, 48].

Selective conformal procedures add a decision ahead of the conformal one. SConU tests each incoming sample against the uncertainty distribution of the calibration set and declines to answer when the evidence for exchangeability is insufficient [19], building on conformal outlier testing [49, 50] and on rank-based anomaly detection under exchangeability [51]. A related line pursues conditional rather than marginal risk guarantees through two-stage calibration, at the cost of a modified exchangeability requirement [52]. Nearest neighbours in embedding space serve as an out-of-distribution statistic in the detection literature independently of conformal calibration [53]. We place such a statistic inside the admission gate, computed from the instruction alone so that screening precedes translation, and calibrate what follows it on the rate at which incorrect specifications are accepted.

## 2 Background and Problem

Formal Logic Languages. Temporal Logic (TL) specifications as formal languages provide mathematically precise descriptions of desired system behaviors, enabling automated planning and formal verification for autonomous and cyber-physical systems [5, 54, 55]. Unlike natural language, which is inherently ambiguous, a formal specification has well-defined syntax and semantics, allowing its correctness to be rigorously analyzed and verified. Let Φ\Phi denote the space of well-formed formulas in a target formal language. Although numerous formal specification languages have been proposed, including LTL [5], STL [6], and SpaTiaL [7], they share a common compositional structure. A specification is recursively constructed from _atomic predicates_ , _Boolean operators_ , and _domain-specific operators_ , such as temporal or spatial modalities:

| φ::=μ​∣¬φ∣​φ1∧φ2​∣φ1∨φ2∣​𝒪​(φ),\varphi::=\mu\mid\neg\varphi\mid\varphi_{1}\land\varphi_{2}\mid\varphi_{1}\lor\varphi_{2}\mid\mathcal{O}(\varphi), |  | (1)  
---|---|---|---  
  
where μ\mu is an atomic predicate and 𝒪\mathcal{O} denotes one or more logic-specific operators. For example, LTL employs temporal operators such as Eventually (𝐅\mathbf{F}), Always (𝐆\mathbf{G}), and Until (𝐔\mathbf{U}); STL augments these operators with bounded time intervals over continuous-valued signals; and SpaTiaL further introduces geometric predicates and spatial operators. Each logic pairs this grammar with a formal semantics specifying when a system trajectory satisfies a specification, which is what makes generated formulas executable and verifiable downstream.

Natural Language to Formal Specification.

Given a natural language instruction u∈𝒰u\in\mathcal{U}, NL2TL aims to generate a formal specification φ^=fθ​(u)∈Φ\hat{\varphi}=f_{\theta}(u)\in\Phi. Most approaches learn the conditional distribution pθ​(φ|u)p_{\theta}(\varphi|u) and predict the most likely specification [9, 23, 24, 10], but the predicted formula may be syntactically valid while failing to preserve the semantic intent of the instruction, and likelihood under pθp_{\theta} offers no measure of this semantic correctness [56].

Conformal Prediction (CP). CP provides a model-agnostic framework for quantifying prediction reliability with finite-sample, distribution-free guarantees [15]. Given a calibration set and a nonconformity score s⁡(x,y)s(x,y), CP computes a threshold from calibration scores and constructs a prediction set 𝒞α​(x)={y:s⁡(x,y)≤q^},\mathcal{C}_{\alpha}(x)=\\{y:s(x,y)\leq\hat{q}\\}, which satisfies Pr⁡(Y∈𝒞α​(X))≥1−α\Pr\\!\left(Y\in\mathcal{C}_{\alpha}(X)\right)\geq 1-\alpha under exchangeability. While this guarantee ensures the correct label is contained in the prediction set with high probability, it is not directly suitable for NL2TL, where downstream planners typically require a single executable formal specification rather than a set of candidates. This limitation motivates conformal methods tailored to selective and reliable formal specification generation.

Problem Formulation. Let x∈𝒳x\in\mathcal{X} be a natural-language instruction and let Φ\Phi be the space of well-formed formulas in a target specification language, as in the preliminaries; the formulation applies to any logic generated by the grammar in Eq. 1, with STL, LTL, and SpaTiaL serving as our experimental instances. A translator φ^=f⁡(x)∈Φ\hat{\varphi}=f(x)\in\Phi is treated as a black box: the framework uses only the final pair (x,φ^)(x,\hat{\varphi}), with no access to parameters, likelihoods, or internal states. The translator may be of any construction [10, 57, 9]; only the instruction and the final formula enter the framework. We augment ff with a selection function g⁡(x,φ^)∈{0,1}g(x,\hat{\varphi})\in\\{0,1\\}, where g=1g=1 indicates that φ^\hat{\varphi} is returned and g=0g=0 indicates abstention. Let φ⋆\varphi^{\star} denote the reference formula and define the translation error as z(x,φ^,φ⋆)=[φ^≢φ⋆]z(x,\hat{\varphi},\varphi^{\star})=\mathbf{1}\\!\left[\hat{\varphi}\not\equiv\varphi^{\star}\right], where ≡\equiv is the semantic-equivalence criterion of the target benchmark. The selective translator is evaluated by its joint risk and coverage,

| ℛjoint=𝐄⁡[g⁡(x,φ^)⋅z⁡(x,φ^,φ⋆)],𝒞=𝐏⁡(g⁡(x,φ^)=1).\mathcal{R}_{\mathrm{joint}}=\mathbf{E}\\!\left[\,g(x,\hat{\varphi})\cdot z(x,\hat{\varphi},\varphi^{\star})\,\right],\qquad\mathcal{C}=\mathbf{P}\\!\left(g(x,\hat{\varphi})=1\right). |  | (2)  
---|---|---|---  
  
The joint risk is the probability that a translation is both accepted and incorrect, taken over the full input stream rather than over the accepted subset; an abstention contributes zero regardless of the underlying error.

Challenges and Motivation. Designing a conformal framework for NL2TL differs fundamentally from standard classification. First, the output space Φ\Phi is effectively unbounded, making prediction sets impractical while downstream planners require a single executable specification or abstention. Second, the objective is selective risk rather than coverage: standard conformal prediction guarantees that the correct specification belongs to a prediction set but does not control the probability that an accepted translation is incorrect, nor the joint rate at which incorrect translations reach execution. Third, conventional nonconformity scores depend on model confidences or token likelihoods, which are unavailable for black-box translators and often poorly aligned with semantic correctness. Therefore, reliable NL2TL requires a framework that (i) performs accept-or-abstain decisions instead of prediction-set construction, (ii) calibrates acceptance risk rather than set coverage, and (iii) uses scores computable solely from the instruction and the generated specification.

## 3 Methodology

Figure 1: Overview of the selective translation framework: instructions are screened before translation (level δ\delta), scored by two complementary signals after it, and returned only when a threshold calibrated to the joint-risk budget α\alpha admits the evidence.

Conformal risk control (CRC) [18] extends conformal calibration from coverage guarantees to arbitrary bounded monotone losses by selecting the largest acceptance threshold whose expected loss remains below a prescribed budget under exchangeability. However, CRC provides only the calibration mechanism, not the scoring function, selection criterion, or robustness to distribution shift. Building on CRC, we propose a black-box conformal selection framework that augments any NL2TL translator with an accept-or-abstain decision layer: an instruction-level screen, two semantic scores, and a calibrated threshold (Fig. 1). The objective is to maximize acceptance subject to a prescribed budget α∈(0,1)\alpha\in(0,1) on the joint risk of Eq. 2:

| maxg⁡𝒞s.t.ℛjoint≤α.\max_{g}\;\mathcal{C}\qquad\text{s.t.}\qquad\mathcal{R}_{\mathrm{joint}}\leq\alpha. |  | (3)  
---|---|---|---  
  
### 3.1 Semantic Consistency Scoring

The decision function in Eq. 3 requires a scalar nonconformity score computed from the instruction–translation pair (x,φ^)(x,\hat{\varphi}) that assigns higher values to less reliable translations. Our default score is based on back-translation. A back-translator BB (an LLM prompted with the target logic) converts φ^\hat{\varphi} into natural language, u^=B⁡(φ^)\hat{u}=B(\hat{\varphi}), and an LLM judge evaluates its semantic consistency with the original instruction across four dimensions: logical structure, temporal operators, time constraints, and overall meaning. The average agreement A⁡(x,u^)∈[0,1]A(x,\hat{u})\in[0,1] defines the nonconformity score

| Sbt​(x,φ^)=1−A⁡(x,B⁡(φ^)).S_{\mathrm{bt}}(x,\hat{\varphi})=1-A\left(x,B(\hat{\varphi})\right). |  | (4)  
---|---|---|---  
  
Invalid or unparsable formulas receive the maximum score, Sbt=1S_{\mathrm{bt}}=1, enforcing syntactic correctness before semantic evaluation. This design isolates logic-specific knowledge within the back-translator, while the judge operates entirely in natural language, making the scoring pipeline applicable to any target logic generated by Eq. 1. The approach combines the round-trip principle from machine translation [58] with the LLM-as-judge paradigm [59]. Because back-translation inspects only the final output, a complementary score measures the stability of repeated stochastic translations. Given kk samples, translator uncertainty is measured by

| Ssc​(x)=1−1k​max1≤j≤k​|{m:φ^(m)≃φ^(j)}|,S_{\mathrm{sc}}(x)=1-\frac{1}{k}\,\max_{1\leq j\leq k}\;\Bigl|\bigl\\{\,m:\hat{\varphi}^{(m)}\simeq\hat{\varphi}^{(j)}\,\bigr\\}\Bigr|, |  | (5)  
---|---|---|---  
  
where the maximum is the size of the largest cluster of mutually equivalent samples, ≃\simeq denotes semantic equivalence under logic-specific canonicalization, and invalid formulas are equivalent only to themselves. This extends self-consistency [60] to formal specifications, where equivalence can be checked exactly [35]. Since SbtS_{\mathrm{bt}} detects semantic mismatches while SscS_{\mathrm{sc}} captures translation uncertainty, their equal-weight fusion

| Sfu=12​(Sbt+Ssc)S_{\mathrm{fu}}=\tfrac{1}{2}\left(S_{\mathrm{bt}}+S_{\mathrm{sc}}\right) |  | (6)  
---|---|---|---  
  
provides the default reliability score. When repeated sampling is unavailable, such as for deterministic or offline translators, SbtS_{\mathrm{bt}} alone can be used without changing the subsequent calibration procedure, which accepts any score in [0,1][0,1].

### 3.2 Risk-Calibrated Selection

The score orders translations by suspicion but does not say where acceptance should stop; that boundary must come from data. A threshold is calibrated on translations whose outcomes are known,

| 𝒟cal\displaystyle\mathcal{D}_{\mathrm{cal}} | ={(xi,φ^i,φi⋆)}i=1n,\displaystyle=\\{(x_{i},\hat{\varphi}_{i},\varphi_{i}^{\star})\\}_{i=1}^{n}, |  | (7)  
---|---|---|---|---  
| Si\displaystyle S_{i} | =S(xi,φ^i),zi=[φ^i≢φi⋆],\displaystyle=S(x_{i},\hat{\varphi}_{i}),\qquad z_{i}=\mathbf{1}\\!\left[\hat{\varphi}_{i}\not\equiv\varphi_{i}^{\star}\right], |  | (8)  
  
where SS is the deployed consistency score, either the fusion SfuS_{\mathrm{fu}} or the output-only SbtS_{\mathrm{bt}}. A candidate threshold τ\tau accepts every translation scoring at or below it, and its empirical joint risk on the calibration set is

| ℛ^(τ)=1n∑i=1n[Si≤τ]zi.\widehat{\mathcal{R}}(\tau)=\frac{1}{n}\sum_{i=1}^{n}\mathbf{1}\\!\left[S_{i}\leq\tau\right]z_{i}. |  | (9)  
---|---|---|---  
  
Every calibration sample contributes to this sum: an abstention counts zero, an accepted error counts one. The quantity is therefore an average over the full sample rather than over the accepted subset, which is what permits the direct application of conformal risk control. Following the calibration rule of Angelopoulos et al. [18], the threshold is

| τ^=max⁡{τ∈𝒯:nn+1​ℛ^​(τ)+1n+1≤α},\hat{\tau}=\max\Bigl\\{\tau\in\mathcal{T}:\tfrac{n}{n+1}\,\widehat{\mathcal{R}}(\tau)+\tfrac{1}{n+1}\leq\alpha\Bigr\\}, |  | (10)  
---|---|---|---  
  
where 𝒯\mathcal{T} is the set of distinct calibration scores together with −∞-\infty, and ties are resolved by admitting all samples that share a score. The correction term accounts for the unseen test point and is what turns an empirical constraint into a population guarantee. At test time,

| g(x,φ^)=[S(x,φ^)≤τ^].g(x,\hat{\varphi})=\mathbf{1}\\!\left[S(x,\hat{\varphi})\leq\hat{\tau}\right]. |  | (11)  
---|---|---|---  
  
###### Theorem 1 (Joint risk control).

Fix a calibration group. If the calibration pairs of this group and the test pair are exchangeable and τ^\hat{\tau} is chosen by Eq. 10 on this group’s calibration scores, then the decision rule of Eq. 11 satisfies, for test inputs of the same group,

| ℛjoint=𝐄⁡[g⁡(X,φ^)⋅Z]≤α.\mathcal{R}_{\mathrm{joint}}=\mathbf{E}\\!\left[\,g(X,\hat{\varphi})\cdot Z\,\right]\leq\alpha. |   
---|---|---  
  
###### Proof.

The loss ℓτ=𝟏[S≤τ]z\ell_{\tau}=\mathbf{1}[S\leq\tau]\,z is bounded in [0,1][0,1] and non-increasing as τ\tau decreases, since lowering the threshold can only remove accepted samples. The claim is the conformal risk control theorem of Angelopoulos et al. [18] applied to this loss. ∎

The guarantee in Theorem 1 holds in expectation over the calibration and test samples. Consequently, a threshold that fully utilizes the risk budget will achieve expected risk close to α\alpha, while individual realizations may exceed α\alpha. Feasibility depends on both the calibration size and score distribution. Since the empirical risk is evaluated at resolution 1n+1\tfrac{1}{n+1}, risk budgets below this level cannot be certified, analogous to the minimum conformal pp-value attainable with nn calibration samples [19, 15]. Moreover, tied scores force samples to enter the acceptance region together. If the smallest nonempty acceptance region contains L0L_{0} calibration errors, a feasible threshold exists only when

| α≥αℓ=L0+1n+1.\alpha\geq\alpha_{\ell}=\frac{L_{0}+1}{n+1}. |  | (12)  
---|---|---|---  
  
Otherwise, Eq. 10 returns τ^=−∞\hat{\tau}=-\infty, causing the system to abstain on every input rather than provide an uncertifiable guarantee. Since αℓ\alpha_{\ell} is determined entirely by the calibration data, feasibility can be assessed before deployment. It can be improved by increasing the calibration set or relaxing the risk budget. Calibrating each group separately in this way yields group-conditional guarantees, at the cost of fewer calibration samples per group and thus a potentially larger αℓ\alpha_{\ell}.

Coverage is maximized by construction through the largest feasible threshold in Eq. 10. Its performance is naturally bounded by two references. For a translator with error rate pp under budget α\alpha, the maximum achievable acceptance rate is min⁡(1, 1−p+α)\min(1,\,1-p+\alpha), attained by a perfect score that ranks all correct translations above all incorrect ones. At the other extreme, an uninformative score achieves acceptance rate α/p\alpha/p by accepting a random subset with the population error rate. The realized acceptance rate therefore quantifies how closely the score approaches the optimal ranking.

### 3.3 Filtering Out-of-Distribution Instructions

Theorem 1 assumes exchangeability between calibration and test data, an assumption that may fail under distribution shift. We therefore introduce an upstream input filter that defers instructions outside the calibration distribution before translation and scoring. Unlike the CRC threshold in Eq. 10, which abstains when translation evidence is insufficient, the filter abstains when no statistical guarantee can be provided.

The filter measures the atypicality of an instruction using its embedding. Scores are computed against a fixed reference set 𝒳ref\mathcal{X}_{\mathrm{ref}} of training-sourced instructions, disjoint from the instructions on which the deferral level is calibrated and from the test stream. Let e⁡(x)∈ℝde(x)\in\mathbb{R}^{d} denote the normalized embedding of instruction xx, and define its average kk-nearest-neighbor distance to the reference set as

| D⁡(x)=1k​∑xj∈𝒩k​(x)‖e⁡(x)−e⁡(xj)‖2,D(x)=\frac{1}{k}\sum_{x_{j}\in\mathcal{N}_{k}(x)}\bigl\|e(x)-e(x_{j})\bigr\|_{2}, |  | (13)  
---|---|---|---  
  
where 𝒩k​(x)\mathcal{N}_{k}(x) is the set of kk nearest reference embeddings. The same function scores the mm deferral-calibration instructions x1,…,xmx_{1},\ldots,x_{m} and any test instruction, and the conformal pp-value of a test instruction is

| p⁡(x)=1+∑i=1m[D(xi)≥D(x)]m+1,p(x)=\frac{1+\sum_{i=1}^{m}\mathbf{1}\\!\left[D(x_{i})\geq D(x)\right]}{m+1}, |  | (14)  
---|---|---|---  
  
###### Theorem 2 (Filter validity).

If the test instruction is exchangeable with the deferral-calibration instructions, then the filter defers it with probability at most δ\delta,

| 𝐏⁡(p⁡(X)<δ)≤δ.\mathbf{P}\\!\left(p(X)<\delta\right)\leq\delta. |   
---|---|---  
  
###### Proof.

The score function DD is fixed by 𝒳ref\mathcal{X}_{\mathrm{ref}} and depends on none of x1,…,xmx_{1},\ldots,x_{m} or the test instruction, so exchangeability of the instructions carries over to their scores. The rank of D⁡(X)D(X) among {D⁡(x1),…,D⁡(xm),D⁡(X)}\\{D(x_{1}),\ldots,D(x_{m}),D(X)\\} is then uniformly distributed up to ties, and ties only enlarge p⁡(X)p(X) through the inequality in Eq. 14, so 𝐏⁡(p⁡(X)<δ)≤δ\mathbf{P}(p(X)<\delta)\leq\delta. ∎

Theorem 2 guarantees that an in-distribution instruction is deferred with probability at most δ\delta. Under distribution shift, the filter removes detected atypical inputs before translation; Theorem 1 applies to the retained stream to the extent that its exchangeability with the calibration data is preserved. Since no finite-sample procedure can detect every shifted input, the filter replaces the assumption of no distribution shift with the weaker assumption that significant shifts are detected, and the residual risk under partial detection is evaluated experimentally.

## 4 Experimental Results

Table 1:  Error-detection AUROC by scoring channel, grouped by information source. Best values in each column are shown in bold. Darker cells indicate higher AUROC within each formalism. The Δ\Delta row reports the fusion margin over the best single channel. 

STL (GPT-5.2 few-shot) SpaTiaL (fine-tuned LLaMA) Source Channel D2 D3 D4 All D2† D3 D4 All Intrinsic self-consistency SscS_{\mathrm{sc}} 0.614 0.644 0.693 0.655 0.773 0.786 0.906 0.867 Extrinsic back-translation mean-4 SbtS_{\mathrm{bt}} 0.586 0.580 0.720 0.634 0.774 0.815 0.918 0.871 direct judge mean-4 0.614 0.520 0.728 0.630 0.661 0.858 0.939 0.892 single-question 0.640 0.569 0.700 0.635 0.870 0.824 0.881 0.863 embedding cosine SembS_{\mathrm{emb}} 0.673 0.536 0.571 0.585 0.825 0.599 0.691 0.662 Fusion 3-judge mean 0.660 0.556 0.727 0.656 0.842 0.875 0.944 0.915 12​(Ssc+Sbt)\frac{1}{2}\left(S_{\mathrm{sc}}+S_{\mathrm{bt}}\right) 0.679 0.663 0.752 0.706 0.824 0.870 0.953 0.920 Δ\Delta over best single +0.006+0.006 +0.018+0.018 +0.025+0.025 +0.051+0.051 – +0.012+0.012 +0.015+0.015 +0.028+0.028

† SpaTiaL D2 contains only seven incorrect translations, too few to estimate ranking quality reliably. The bootstrap 95% confidence interval for SbtS_{\mathrm{bt}} spans [0.49,0.96][0.49,0.96], so the reported values indicate at most the direction of the ranking. No per-column boldface or Δ\Delta is shown for this column.

#### Tasks and data.

Three specification languages instantiate the framework: STL and interval-free LTL from the NL2TL benchmark [9], and SpaTiaL from the NL2SpaTiaL benchmark [10]. Each language is divided into three difficulty tiers (D2–D4). For SpaTiaL, tiers are determined during data generation by controlling the depth and branching of logical trees [10]. For STL and LTL, tiers are defined post hoc by the number of atomic propositions in the reference formula (at most two, three, and at least four), serving as a proxy for logical complexity. The tier labels indicate increasing difficulty within each language and are not comparable across languages. For each random resplit 200 examples per tier are assigned to calibration and 150 disjoint examples to testing. Paraphrases associated with the same reference formula are always kept in the same partition to prevent semantic leakage. Translation correctness is determined using the benchmark-provided canonical equivalence checker, which accounts for commutativity, De Morgan transformations, and argument-order normalization.

#### LLM Translators.

Two translators spanning a wide reliability range are evaluated. The first is the fine-tuned LLaMA-3-8B model of Luo et al. [10], equipped with tier-specific LoRA adapters, achieving a raw error rate of approximately 15%15\%. The second is GPT-5.2 prompted with twenty in-context examples for STL and LTL, following the few-shot setup of the unfine-tuned baselines in Chen et al. [9], with prompts and exemplars developed independently, yielding a 48%48\% error rate under semantic-equivalence evaluation. For completeness, the fine-tuned T5 model of Chen et al. [9] (approximately 2%2\% error) is included only to verify the applicability of the self-consistency score, as its error rate is too low for meaningful tier-level risk evaluation.

#### Scoring and calibration configuration.

Back-translation uses GPT-5.2 with a prompt frozen before any evaluation run; judging uses GPT-5.4 with the four-dimensional rubric defined above; self-consistency draws k=5k=5 samples at temperature 1.01.0. STL and LTL share the same back-translation and judging prompts, while SpaTiaL uses its own back-translation prompt and a categorical rubric. Within each language, prompts and rubric texts are fixed once and identical across translators and evaluation runs. Thresholds are calibrated per language and tier. Every reported risk and coverage figure is the mean over 100 random calibration–test resplits, with its standard error; the resplit protocol, the filtering level δ=0.05\delta=0.05, and the rule that marks a cell as borderline when its mean lies within one standard error of α\alpha were all fixed before either arm of any comparison was inspected.

#### Baseline and metrics.

The baseline adapts standard conformal calibration to selective prediction by applying the coverage-based conformal quantile rule to the same nonconformity score and using the resulting threshold for acceptance. Thus, both methods share the score, data, and decision rule, differing only in the calibration objective. They are compared using three metrics: the joint risk in Eq. 9, the acceptance rate, and the number of resplits in which the realized joint risk exceeds α\alpha. The exceedance count reflects the expectation-level nature of the guarantee rather than a failure. The guarantee constrains the mean risk over resplits, not each realization, so a method that spends its budget operates near α\alpha and individual resplits land on either side; the count locates the operating point relative to the budget rather than measuring compliance. Score quality is evaluated independently of calibration. Let 𝒫\mathcal{P} and 𝒩\mathcal{N} denote the correct and incorrect translations within a tier. We report

|  | AUROC(S)=1|𝒫|​|𝒩|∑p∈𝒫∑q∈𝒩([S(q)>S(p)]+12[S(q)=S(p)]),\displaystyle\mathrm{AUROC}(S)=\frac{1}{|\mathcal{P}|\,|\mathcal{N}|}\sum_{p\in\mathcal{P}}\sum_{q\in\mathcal{N}}\Bigl(\mathbf{1}\\!\left[S(q)>S(p)\right]+\tfrac{1}{2}\mathbf{1}\\!\left[S(q)=S(p)\right]\Bigr), |  | (15)  
---|---|---|---|---  
  
which equals the area under the ROC curve [61]. AUROC measures the probability that the score ranks an incorrect translation above a correct one, assigning half credit to ties. It ranges from 0.50.5 (random ranking) to 11 (perfect separation), is invariant to monotone score transformations, and is independent of any acceptance threshold or risk budget, making it well suited for comparing scoring methods before calibration. Results are reported per tier, with bootstrap confidence intervals for low-error cases and uninformative intervals explicitly marked.

Table 2: From score to selective prediction. AUROC↑\uparrow is computed over all tiers. The acceptance rate at α=0.10\alpha=0.10 and the feasibility floor αℓ\alpha_{\ell} are calibrated on the three tiers of each language merged into a single calibration set (n=600n=600), and are therefore not comparable to the per-tier compliance tables. Domain | Score | AUROC↑\uparrow | Acc. rate@α=0.10\alpha{=}0.10 | αℓ\alpha_{\ell}  
---|---|---|---|---  
STL | SscS_{\mathrm{sc}} | 0.655 | 0.000 | 0.2696  
SbtS_{\mathrm{bt}} | 0.634 | 0.280 | 0.0582  
SfuS_{\mathrm{fu}} | 0.706 | 0.347 | 0.0483  
SpaTiaL | SscS_{\mathrm{sc}} | 0.867 | 0.857 | 0.0483  
SbtS_{\mathrm{bt}} | 0.871 | 0.748 | 0.0083  
SfuS_{\mathrm{fu}} | 0.920 | 0.889 | 0.0083  
Table 3:  Joint-risk compliance under the stated calibration sizes. Entries report mean joint risk ±\pm standard error over 100 random calibration/test splits. Green cells indicate clear CRC compliance; red cells indicate violations by more than one standard error; gray cells lie within one standard error of the target risk budget. Uncolored Split CP cells are numerically below the risk budget but carry no joint-risk guarantee. _No sel._ accepts all translations, and ‡ denotes full abstention when no valid CRC threshold exists.  Tier |  No sel. |  Method | Risk budget α\alpha  
---|---|---|---  
|  |  |  0.05 |  0.10 |  0.15 |  0.20 |  0.25 |  0.30  
(a) STL GPT-5.2 few-shot translator  
D2 |  0.423 |  CRC |  abst.‡ |  0.069 ±\pm0.006 ✓ |  0.133 ±\pm0.003 ✓ |  0.190 ±\pm0.004 ✓ |  0.243 ±\pm0.005 ✓ |  0.293 ±\pm0.005 ✓  
|  |  Split CP |  0.349 ±\pm0.003 ✗ |  0.326 ±\pm0.003 ✗ |  0.312 ±\pm0.003 ✗ |  0.275 ±\pm0.003 ✗ |  0.252 ±\pm0.003† |  0.237 ±\pm0.003  
D3 |  0.434 |  CRC |  0.046 ±\pm0.002 ✓ |  0.097 ±\pm0.004† |  0.151 ±\pm0.004† |  0.192 ±\pm0.004 ✓ |  0.250 ±\pm0.005† |  0.301 ±\pm0.005†  
|  |  Split CP |  0.371 ±\pm0.003 ✗ |  0.329 ±\pm0.003 ✗ |  0.306 ±\pm0.003 ✗ |  0.296 ±\pm0.003 ✗ |  0.293 ±\pm0.003 ✗ |  0.278 ±\pm0.003  
D4 |  0.551 |  CRC |  0.012 ±\pm0.003 ✓ |  0.094 ±\pm0.003 ✓ |  0.143 ±\pm0.003 ✓ |  0.184 ±\pm0.004 ✓ |  0.235 ±\pm0.004 ✓ |  0.291 ±\pm0.004 ✓  
|  |  Split CP |  0.485 ±\pm0.004 ✗ |  0.373 ±\pm0.004 ✗ |  0.292 ±\pm0.004 ✗ |  0.233 ±\pm0.003 ✗ |  0.205 ±\pm0.003 |  0.183 ±\pm0.003  
(b) SpaTiaL fine-tuned LLaMA translator  
D2 |  0.0372 |  CRC |  0.034 ±\pm0.001 ✓ |  0.035 ±\pm0.001 ✓ |  0.035 ±\pm0.001 ✓ |  0.035 ±\pm0.001 ✓ |  0.035 ±\pm0.001 ✓ |  0.035 ±\pm0.001 ✓  
|  |  Split CP |  0.017 ±\pm0.001 |  0.016 ±\pm0.001 |  0.016 ±\pm0.001 |  0.016 ±\pm0.001 |  0.016 ±\pm0.001 |  0.013 ±\pm0.001  
D3 |  0.149 |  CRC |  0.049 ±\pm0.002† |  0.095 ±\pm0.004 ✓ |  0.140 ±\pm0.003 ✓ |  0.149 ±\pm0.002 ✓ |  0.149 ±\pm0.002 ✓ |  0.149 ±\pm0.002 ✓  
|  |  Split CP |  0.052 ±\pm0.001 ✗ |  0.050 ±\pm0.001 |  0.046 ±\pm0.001 |  0.046 ±\pm0.001 |  0.040 ±\pm0.001 |  0.035 ±\pm0.001  
D4 |  0.309 |  CRC |  0.046 ±\pm0.002 ✓ |  0.088 ±\pm0.003 ✓ |  0.138 ±\pm0.004 ✓ |  0.190 ±\pm0.004 ✓ |  0.242 ±\pm0.004 ✓ |  0.274 ±\pm0.005 ✓  
|  |  Split CP |  0.066 ±\pm0.002 ✗ |  0.061 ±\pm0.002 |  0.055 ±\pm0.002 |  0.039 ±\pm0.001 |  0.034 ±\pm0.001 |  0.034 ±\pm0.001  
  
Scoring Ablation. Although CRC can calibrate any score in [0,1][0,1], its practical efficiency depends on both error-ranking quality and score resolution. We therefore evaluate ranking quality before calibration and then examine the operating behavior induced by each score. Table 1 reports per-tier AUROC for the three proposed scores—back-translation (SbtS_{\mathrm{bt}}), self-consistency (SscS_{\mathrm{sc}}), and their fusion (SfuS_{\mathrm{fu}})—together with four ablations: a direct judge without back-translation, a single-question judge, cosine similarity between instruction and back-translation embeddings, and mean/max ensembles of the judge-based scores.

Three observations emerge. First, judge-side variants offer little benefit: on STL, back-translation, direct judging, and single-question judging achieve similar AUROCs (0.6340.634–0.6350.635), while ensembling improves only marginally to 0.6560.656, indicating correlated errors. Second, self-consistency provides complementary information. Although SscS_{\mathrm{sc}} alone achieves AUROCs of 0.6550.655 (STL) and 0.8670.867 (SpaTiaL), combining it with back-translation yields the best overall performance (0.7060.706 and 0.9200.920), consistently across STL tiers and robust to mixing weights λ∈[0.3,0.7]\lambda\in[0.3,0.7]. Third, the gain reflects complementary failure modes rather than averaging. On STL, 77.8%77.8\% of inconsistent translation samples are erroneous, while among consistent samples, where self-consistency is uninformative, back-translation still distinguishes errors (AUROC 0.6000.600), with 37.5%37.5\% of confidently generated translations remaining incorrect. Thus, self-consistency detects uncertain failures, whereas back-translation detects confident semantic mismatches.

The remaining errors are largely intrinsic to the task. Invalid formulas are assigned the maximum score by construction, but syntactically valid convention errors and genuinely ambiguous instructions often remain indistinguishable. The benchmark itself contains 114 instruction strings paired with conflicting reference formulas, limiting the achievable discriminability of any score derived solely from the instruction and translation. The self-consistency score also requires sufficient translation errors for reliable ranking; the fine-tuned T5 baseline (≈2%\approx 2\% error) contains too few negatives for meaningful AUROC estimation and is therefore used only to verify the applicability of the score.

Table 2 translates ranking into selective prediction, reporting acceptance at α=0.10\alpha=0.10 and the minimum certifiable risk αℓ\alpha_{\ell}, which AUROC alone does not determine. On STL, self-consistency and back-translation have similar AUROCs, yet SscS_{\mathrm{sc}} cannot certify risks below 0.2700.270 because many tied scores concentrate calibration errors, causing complete abstention at α=0.10\alpha=0.10, whereas SbtS_{\mathrm{bt}} accepts 28.0%28.0\% of inputs. The fusion inherits the continuous resolution of back-translation, reducing the certifiable floor to 0.0480.048 and increasing acceptance to 34.7%34.7\%. On SpaTiaL, where back-translation already achieves αℓ=0.008\alpha_{\ell}=0.008, the fusion preserves this guarantee while improving acceptance by 14 percentage points. On LTL, error rates of 0.5030.503–0.6490.649 place αℓ\alpha_{\ell} above 0.100.10 for every score, and the calibration abstains in full at this budget; the complete LTL results appear in the appendix. Effective calibration thus requires accurate ranking and sufficient score resolution together, and the fusion supplies both wherever any score does.

Table 4: Deployment drift on STL with frozen τ\tau, α=0.10\alpha=0.10, gate level δ=0.05\delta=0.05, and 100 reseeds. Columns denote the calibration tier and rows denote the test tier. The three panels report joint risk without gating, joint risk with gating, and abstention rate. Bold entries are the in-distribution diagonal; off-diagonal entries are cross-tier shifts.

No gate Gated Abstained Test tier D2 D3 D4 D2 D3 D4 D2 D3 D4 D2 0.061 0.109 0.109 0.061 0.026 0.026 0.006 0.395 0.321 D3 0.064 0.125 0.151 0.056 0.110 0.151 0.056 0.054 0.026 D4 0.083 0.123 0.137 0.062 0.076 0.137 0.164 0.253 0.007

Risk Control.  Table 3 compares CRC calibration with coverage calibration on two translators. A cell is compliant if its mean joint risk does not exceed the budget. For the few-shot translator, with unconditional error rates of 0.4230.423, 0.4340.434, and 0.5510.551 across the STL tiers, the calibration target decides the outcome. CRC satisfies the budget in all eighteen settings, with joint risk rising toward each budget as α\alpha widens and several operating points within one standard error of their targets, the position of an expectation-level guarantee spending its budget in full; the single infeasible cell, the easiest tier at α=0.05\alpha=0.05, lies below the feasibility floor of Eq. 12 and abstains in full. Using the same score and data, Split CP violates the budget in thirteen cells. Its risk may decrease as α\alpha increases because the relaxed coverage target can produce a stricter acceptance threshold; it tracks coverage rather than joint risk.

The fine-tuned translator, with error rates of 0.0370.037, 0.1490.149, and 0.3090.309, inverts the reading: many budgets already exceed the unconditional error, so compliance on the easier tiers reflects the translator rather than the selection. The deepest tier shows the mechanism at work, abstaining on approximately 23%23\% of inputs at α=0.10\alpha=0.10 to reduce joint risk from 0.3090.309 to 0.0880.088; acceptance rates for all cells appear in the appendix ledger. Split CP reports lower risk on this translator, decreasing from 0.0660.066 to 0.0340.034 on the deepest tier as α\alpha increases because acceptance becomes more restrictive, yet it still violates the two tightest budgets. Abstention thus arises from two mechanisms: a threshold declining individual translations, active throughout the feasible cells, and a budget below the feasibility floor, which declines the entire stream and occurs once.

Deployment Drift. 

The acceptance threshold guarantees risk only under exchangeability, and the instruction-level filter rejects out-of-distribution inputs before translation. Table 4 evaluates the full pipeline on STL under the cross-tier protocol of Wang et al. [19]. Each column fixes a calibration tier, threshold and kkNN reference included, and each row supplies the test stream, replaced off the diagonal by another tier’s without recalibration. On the diagonal the filter defers 0.6%0.6\%, 5.4%5.4\%, and 0.7%0.7\% of clean in-distribution inputs across the three tiers, consistent with the level δ=0.05\delta=0.05 up to Monte Carlo variation at m=50m=50. All six shifted settings raise joint risk (0.1090.109–0.1510.151) over their diagonals. The filter reduces risk in five of the six and returns four below the budget, and the largest recovery, from 0.1230.123 to 0.0760.076, occurs where the deepest-tier stream meets the intermediate calibration.

Some instructions the filter rejects would have been rejected by the CRC threshold as well and therefore do not affect execution. Both settings that test the intermediate stream are of this kind, with the filter adding 0.8%0.8\% abstention against the shallow calibration and none against the deep one, so protection there falls entirely to the threshold. Intermediate instructions sit inside both neighboring reference distributions, and detectability is directional in general, with deeper streams standing out against shallower references while the reverse shift passes the filter, the pattern anticipated in the Sec. 3. In the remaining four settings the filter rejects 5.2%5.2\%–15.6%15.6\% of inputs the threshold would have accepted, and 39%39\%–72%72\% of these are incorrect translations that read plausibly, reflecting the distinct evidence the two components use, instruction typicality and translation reliability. Abstention alone still overstates the filter, as the two settings on the shallowest stream abstain at 39.5%39.5\% and 32.1%32.1\% with identical gated risk because the extra rejections fall on correct translations. Screening before translation also avoids 3131–474474 downstream model calls per 150150 shifted instructions.

## References

  * [1] Z. Xu, Y. Chen, and U. Topcu (2021) Adaptive teaching of temporal logic formulas to preference-based learners.  In Proceedings of the AAAI Conference on Artificial Intelligence,  Vol. 35, pp. 5061–5068.  Cited by: §1. 
  * [2] R. Roy, J. Gaglione, N. Baharisangari, D. Neider, Z. Xu, and U. Topcu (2023) Learning interpretable temporal properties from positive examples only.  In Proceedings of the AAAI Conference on Artificial Intelligence,  Vol. 37, pp. 6507–6515.  Cited by: §1. 
  * [3] T. Chakraborti, J. Kang, F. Fuggitti, M. Katz, and S. Sohrabi (2024) Interactive plan selection using linear temporal logic, disjunctive action landmarks, and natural language instruction.  In Proceedings of the AAAI Conference on Artificial Intelligence,  Vol. 38, pp. 23775–23777.  Cited by: §1. 
  * [4] X. Zhao, V. Robu, D. Flynn, F. Dinmohammadi, M. Fisher, and M. Webster (2019) Probabilistic model checking of robots deployed in extreme environments.  In Proceedings of the AAAI Conference on Artificial Intelligence,  Vol. 33, pp. 8066–8074.  Cited by: §1. 
  * [5] A. Pnueli (1977) The temporal logic of programs.  In 18th annual symposium on foundations of computer science (sfcs 1977),  pp. 46–57.  Cited by: §1, §2. 
  * [6] O. Maler and D. Nickovic (2004) Monitoring temporal properties of continuous signals.  In International symposium on formal techniques in real-time and fault-tolerant systems,  pp. 152–166.  Cited by: §1, §2. 
  * [7] C. Pek, G. F. Schuppe, F. Esposito, J. Tumova, and D. Kragic (2023) SpaTiaL: monitoring and planning of robotic tasks using spatio-temporal logic specifications.  Autonomous Robots 47 (8), pp. 1439–1462.  Cited by: §1, §2. 
  * [8] J. He, E. Bartocci, D. Ničković, H. Isakovic, and R. Grosu (2022) Deepstl: from english requirements to signal temporal logic.  In Proceedings of the 44th International Conference on Software Engineering,  pp. 610–622.  Cited by: §1, §1. 
  * [9] Y. Chen, R. Gandhi, Y. Zhang, and C. Fan (2023) Nl2tl: transforming natural languages to temporal logics using large language models.  In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing,  pp. 15880–15903.  Cited by: §1, §1, §2, §2, §4, §4. 
  * [10] L. Luo, K. Liang, Y. Xia, and M. Cai (2026) NL2SpaTiaL: generating geometric spatio-temporal logic specifications from natural language for manipulation tasks.  The IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS).  Cited by: §1, §1, §2, §2, §4, §4. 
  * [11] E. Stengel-Eskin and B. Van Durme (2023) Calibrated interpretation: confidence estimation in semantic parsing.  Transactions of the Association for Computational Linguistics 11, pp. 1213–1231.  Cited by: §1. 
  * [12] Y. Chen, W. Walden, T. Chen, A. S. White, and B. Van Durme (2023) A unified view of evaluation metrics for structured prediction.  In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing,  pp. 12868–12882.  Cited by: §1. 
  * [13] R. Zhong, T. Yu, and D. Klein (2020) Semantic evaluation for text-to-sql with distilled test suites.  In Proceedings of the 2020 Conference on Empirical Methods in Natural Language Processing (EMNLP),  pp. 396–411.  Cited by: §1. 
  * [14] O. Somov and E. Tutubalina (2025) Confidence estimation for error detection in text-to-sql systems.  In Proceedings of the AAAI Conference on Artificial Intelligence,  Vol. 39, pp. 25137–25145.  Cited by: §1. 
  * [15] V. Vovk, A. Gammerman, and G. Shafer (2005) Algorithmic learning in a random world.  Springer.  Cited by: §1, §2, §3.2. 
  * [16] Y. Geifman and R. El-Yaniv (2019) Selectivenet: a deep neural network with an integrated reject option.  In International conference on machine learning,  pp. 2151–2159.  Cited by: §1. 
  * [17] M. Lee, K. Kim, T. Kim, and S. Park (2024) Selective generation for controllable langu
