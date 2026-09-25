URL: https://arxiv.org/html/2505.20047 | FULL FETCH | 2026-09-24T01:36:08Z
warning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
URL: https://arxiv.org/html/2505.20047
Type: HTML
Length: 141338 chars (truncated)

--- Content ---

##### Report GitHub Issue

×

Title:

Content selection saved. Describe the issue below:

Description:

Submit without GitHub Submit in GitHub

arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[ Back to arXiv ](/)

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) Report Issue [ Back to Abstract ](/abs/2505.20047v1 "Back to abstract page") [ Download PDF](/pdf/2505.20047v1 "Download PDF") [ ](javascript:toggleNavTOC\(\); "Toggle navigation") [ ](javascript:toggleReadingMode\(\); "Disable reading mode, show header and footer")

  1. Abstract
  2. 1 Introduction
  3. 2 Methodology
     1. 2.1 Probabilistic Context-Free Grammar (PCFG) Derived Metrics
  4. 3 Results
     1. 3.1 Performance of Uncertainty Metrics
  5. 4 Related Works
  6. 5 Conclusion
  7. References
  8. A Appendix: Proofs
     1. A.1 Coverage Guarantees
     2. A.2 Temperature Sampling & Ablations
  9. B Temperature-Varied SMT Generation and PCFG Analysis
  10. C Detailed Results
     1. C.1 Benchmarking Autoformalization
     2. C.2 Detailed Performance of Uncertainty Metrics for Ground Truth Prediction
     3. C.3 Detailed Performance of SMT-Based Uncertainty Metrics for Text-Answer Prediction
  11. D Supplementary Experimental Details
  12. E SMT Error Ratios vs Text Error Ratios
  13. F Qualitative Analysis
     1. Formalization Aliasing and Representational Stability
     2. Variance in Logical Decomposition and Structural Complexity
     3. Identification of Atypical or Anomalous Assertions
     4. Semantic Divergence in Axiomatization
     5. Fidelity in Representing Ground Facts



[ License: CC BY 4.0 ](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2505.20047v1 [cs.CL] 26 May 2025

# Grammars of Formal Uncertainty: When to Trust LLMs in Automated Reasoning Tasks

Debargha Ganguly  Affiliation: Case Western Reserve University  Email: [debargha@case.edu](mailto:) Vikash Singh  Affiliation: Case Western Reserve University  Email: [vikash@case.edu](mailto:) Sreehari Sankar  Affiliation: Case Western Reserve University  Email: [sreehari@case.edu](mailto:) Biyao Zhang  Affiliation: Case Western Reserve University  Email: [bxz297@case.edu](mailto:) Xuecen Zhang  Affiliation: Case Western Reserve University  Email: [xxz1037@case.edu](mailto:) Srinivasan Iyengar  Affiliation: Microsoft Corporation  Email: [xhan@case.edu](mailto:) Xiaotian Han  Affiliation: Case Western Reserve University  Email: [vipin@case.edu](mailto:) Amit Sharma  Affiliation: Microsoft Research  Email: [sriyengar@microsoft.com](mailto:) Shivkumar Kalyanaraman  Affiliation: Microsoft Corporation  Email: [amshar@microsoft.com](mailto:) Vipin Chaudhary  Affiliation: Case Western Reserve University  Email: [shkalya@microsoft.com](mailto:)

###### Abstract

Large language models (LLMs) show remarkable promise for democratizing automated reasoning by generating formal specifications. However, a fundamental tension exists: LLMs are probabilistic, while formal verification demands deterministic guarantees. This paper addresses this epistemological gap by comprehensively investigating failure modes and uncertainty quantification (UQ) in LLM-generated formal artifacts. Our systematic evaluation of five frontier LLMs reveals Satisfiability Modulo Theories (SMT) based autoformalization’s domain-specific impact on accuracy (from +34.8% on logical tasks to -44.5% on factual ones), with known UQ techniques like the entropy of token probabilities failing to identify these errors. We introduce a probabilistic context-free grammar (PCFG) framework to model LLM outputs, yielding a refined uncertainty taxonomy. We find uncertainty signals are task-dependent (e.g., grammar entropy for logic, AUROC>0.93). Finally, a lightweight fusion of these signals enables selective verification, drastically reducing errors (14-100%) with minimal abstention, transforming LLM-driven formalization into a reliable engineering discipline.

## 1 Introduction

Formal methods offer robust mathematical guarantees for system reliability (Huth and Ryan, 2004), but their widespread adoption is impeded by high expertise and labor demands, traditionally limiting their application to safety-critical domains where failures have catastrophic consequences (Clarke et al., 2018; Woodcock et al., 2009). Concurrently, Large Language Models (LLMs) have emerged with a remarkable ability to generate formal artifacts such as code, proofs, and specifications (Brown et al., 2020; Chen et al., 2021; Jiang et al., 2023a), potentially democratizing formal methods (Hou et al., 2023) and finding new roles in formally correct reasoning and LLM verification (Ganguly et al., 2024; Pan et al., 2023). However, these two approaches embody fundamentally different epistemological paradigms. Formal methods are rooted in deterministic logical calculi, where conclusions derive necessarily from premises via unambiguous inference rules. LLMs, in contrast, operate probabilistically, representing knowledge as distributions over tokens where multiple, even contradictory, outputs can possess non-zero probability (Wei et al., 2022a). This inherent tension presents a core challenge: how can we harness the generative power of LLMs for formal reasoning while upholding the rigorous guarantees that define formal verification’s value?

The central thesis of this paper is that the inherent probabilistic uncertainty in LLM outputs for formal reasoning tasks, particularly when generating formal artifacts like SMT-LIB programs, is not a mere nuisance but a valuable source of information for guiding verification. Existing methods often ignore this by selecting only the highest-probability output (Chen et al., 2022), a simplification that we argue undermines the rigorous standards required for formal reasoning. In contrast, we demonstrate how to systematically capture and analyze this output uncertainty by modeling LLM-generated SMT-LIB program distributions with Probabilistic Context-Free Grammars (PCFGs). Instead of focusing on a single output, we analyze ensembles of LLM-generated SMT-LIB programs, treating these as samples from the model’s internal probability distribution (Kadavath et al., 2022), which we then approximate by applying PCFGs to the ensembles. This approximation not only identifies the most likely solutions but also reveals strategic diversity, common structural motifs, and areas of high model uncertainty. Deriving a comprehensive suite of metrics from this structured, quantifiable understanding of uncertainty can then directly guide the verification workflow—for instance, by assessing artifact reliability, focusing human review on more ambiguous or structurally complex candidates, and improving error detection strategies.

The core contributions of this paper are:

  * •

We systematically evaluated frontier LLMs on four formal reasoning datasets, finding SMT-based autoformalization significantly boosted accuracy on tasks like ProofWriter (+34.8%) but harmed others like FOLIO (-44.5%), thus quantifying LLM-driven formal verification’s failure modes. We then demonstrate that known uncertainty quantification techniques do not capture enough information to identify errors in FV artifacts.

  * •

Introduce a probabilistic framework using probabilistic context-free grammars to model LLM-generated SMT-LIB programs, enabling mathematically sound uncertainty quantification and bridging neural models with formal verification.

  * •

Developed and evaluated 25 uncertainty metrics, revealing a refined taxonomy (epistemic-knowledge, epistemic-procedural, recursive-complexity, capacity-limited) that offers a more nuanced understanding of uncertainty in neurosymbolic systems than the traditional epistemic/aleatoric dichotomy.

  * •

Demonstrated that formal reasoning uncertainty is task-dependent and introduced a lightweight, model-agnostic fusion of these varied uncertainty signals. This approach outperforms individual metrics, improves calibration, enables selective verification to cut error rates by 14-100% with minimal abstention, and suggests modality-aware architectures for enhanced reliability.




## 2 Methodology

Generating formal artifacts using ad-hoc Domain-Specific Languages (DSLs) introduces significant engineering friction. This friction arises from the need to redesign generators, models, and parsers for syntax changes, and it also complicates debugging erroneous outputs (e.g. syntactically incorrect FV artifacts). To mitigate this overhead, we adopt the stable, widely supported SMT-LIB standard as a common intermediate representation targeting SMT solvers. In this section, we consequently present a theoretical framework linking language models and verification to analyze LLM-generated SMT-LIB program distributions, enabling principled reasoning about their uncertainty.

Problem Setup We formalize the probability space over SMT-LIB programs. Let Σ\Sigma be a finite alphabet. The set of all finite strings Σ∗\Sigma^{*} forms a measurable space (Σ∗,ℱ)(\Sigma^{*},\mathcal{F}), where ℱ\mathcal{F} is the σ\sigma-algebra generated by cylinder sets (strings sharing a common prefix ww). The SMT-LIB language LS​M​T⊆Σ∗L_{SMT}\subseteq\Sigma^{*}, approximated by its standard context-free grammar GS​M​TG_{SMT}, is measurable in ℱ\mathcal{F}. For a task TT and an LLM with parameters θ\theta, the LLM induces a probability measure μT,θ\mu_{T,\theta} on (Σ∗,ℱ)(\Sigma^{*},\mathcal{F}). The measure over valid SMT-LIB programs is then the conditional measure μT,θ,S​M​T​(A)=μT,θ​(A∩LS​M​T)μT,θ​(LS​M​T)\mu_{T,\theta,SMT}(A)=\frac{\mu_{T,\theta}(A\cap L_{SMT})}{\mu_{T,\theta}(L_{SMT})} for A∈ℱA\in\mathcal{F}. This definition requires μT,θ​(LS​M​T)>0\mu_{T,\theta}(L_{SMT})>0, a reasonable assumption that is empirically validated, as LLMs are generally trained to generate syntactically valid code and formal specifications.

Modeling Background: To model distributions over structured programs like μT,θ,S​M​T\mu_{T,\theta,SMT}, we employ Probabilistic Context-Free Grammars (PCFGs). PCFGs extend standard Context-Free Grammars (CFGs) by associating probabilities with their production rules. Formally, a PCFG is a 5-tuple G=(V,Σ,R,S,p)G=(V,\Sigma,R,S,p), where VV is a finite set of non-terminals; Σ\Sigma is a finite set of terminals disjoint from VV; R⊆V×(V∪Σ)∗R\subseteq V\times(V\cup\Sigma)^{*} is a finite set of production rules; and S∈VS\in V is the start symbol, such that (V,Σ,R,S)(V,\Sigma,R,S) collectively form a CFG. The fifth component, p:R→[0,1]p:R\rightarrow[0,1], is a probability function assigning a probability p⁡(r)p(r) to each rule r∈Rr\in R. For each non-terminal A∈VA\in V, these probabilities must satisfy ∑r∈RAp⁡(r)=1\sum_{r\in R_{A}}p(r)=1, where RAR_{A} denotes the set of rules with AA as their left-hand side. The probability of a derivation π\pi that applies rules r1,…,rkr_{1},\ldots,r_{k} in sequence is p⁡(π)=∏i=1kp⁡(ri)p(\pi)=\prod_{i=1}^{k}p(r_{i}). Consequently, for any terminal string w∈L⁡(G)w\in L(G), where L⁡(G)L(G) is the language generated by the underlying CFG, its probability under GG is μG​(w)=∑π∈Π⁡(w)p⁡(π)=∑π∈Π⁡(w)∏r∈πp⁡(r)\mu_{G}(w)=\sum_{\pi\in\Pi(w)}p(\pi)=\sum_{\pi\in\Pi(w)}\prod_{r\in\pi}p(r), where Π⁡(w)\Pi(w) represents the set of all leftmost derivations of ww from SS. It is important to note that a PCFG GG defines a consistent probability measure (i.e., ∑w∈L⁡(G)μG​(w)=1\sum_{w\in L(G)}\mu_{G}(w)=1) if and only if the spectral radius of its moment matrix MGM_{G} is less than or equal to 1. This condition ensures that probabilities are well-defined and sum to one across the entire language generated by GG.

Figure 1: Analysis of empirically observed LLM-generated SMT-LIB formalizations for the statement ‘Everyone who studies math or physics and works hard will succeed.’ The figure presents actual outputs and measurements: LLM-generated logical variations (left), measured PCFG rule frequencies (center), and computed probability distributions (right). The calculated uncertainty metrics are derived from the observed PCFG patterns and successfully predict formalization uncertainty. No synthetic or simulated data is used.

Approximation: To connect the theoretical LLM distribution μT,θ,S​M​T\mu_{T,\theta,SMT} with a tractable probabilistic model, we estimate parameters for a PCFG. We use the SMT-LIB v2 grammar GS​M​T=(VS​M​T,ΣS​M​T,RS​M​T,SS​M​T)G_{SMT}=(V_{SMT},\Sigma_{SMT},R_{SMT},S_{SMT}) as its structural basis. We now generate NN SMT-LIB program samples 𝒫N={P1,…,PN}\mathcal{P}_{N}=\\{P_{1},\ldots,P_{N}\\} from the target LLM (parameterized by θ\theta) and parse them using GS​M​TG_{SMT}. This yields a set of parse trees Π⁡(𝒫N)\Pi(\mathcal{P}_{N}) from the successfully parsed programs. From each parse tree π∈Π⁡(𝒫N)\pi\in\Pi(\mathcal{P}_{N}), we identify and record every applied production rule r=(A→β)∈RS​M​Tr=(A\rightarrow\beta)\in R_{SMT}. This record typically includes the rule itself, its source program identifier, structural context (such as depth), and optionally, the corresponding source text mapping for qualitative analysis. This data collection also allows for extracting richer contextual features than those used by standard Maximum Likelihood Estimation for estimating the rule probability function p:RS​M​T→[0,1]p:R_{SMT}\rightarrow[0,1] from these rule application frequencies.

Maximum Likelihood Estimation (MLE) is used to estimate rule probabilities p⁡(r)p(r) using counts from Π⁡(𝒫N)\Pi(\mathcal{P}_{N}). Given total application counts C⁡(r)C(r) for a rule r=(A→β)r=(A\rightarrow\beta) and C⁡(A)=∑r′∈RAC⁡(r′)C(A)=\sum_{r^{\prime}\in R_{A}}C(r^{\prime}) for its left-hand side (LHS) non-terminal AA (where OPENRA={r′∈RS​M​T∣left​(r′)=A})R_{A}=\\{r^{\prime}\in R_{SMT}\mid\text{left}(r^{\prime})=A\\}), the MLE is its relative frequency p^M​L​E​(r)=C⁡(r)/C⁡(A)\hat{p}_{MLE}(r)=C(r)/C(A), defined if C⁡(A)>0C(A)>0. If C⁡(A)=0C(A)=0, rules in RAR_{A} are assigned a uniform probability 1/|RA|1/|R_{A}|. For independent and identically distributed (i.i.d.) samples 𝒫N\mathcal{P}_{N} from μT,θ,S​M​T\mu_{T,\theta,SMT}, these estimated probabilities p^N​(r)\hat{p}_{N}(r) converge almost surely (a.s.) to p∗​(r)p^{*}(r) as N→∞N\rightarrow\infty. The limits p∗​(r)p^{*}(r) are the parameters of the GS​M​TG_{SMT}-based PCFG that is closest in Kullback-Leibler (KL) divergence to the true distribution μT,θ,S​M​T\mu_{T,\theta,SMT} (i.e., p∗=argminpDK​L(μT,θ,S​M​T∥μG(p))p^{*}=\operatorname*{argmin}_{p}D_{KL}(\mu_{T,\theta,SMT}\parallel\mu_{G}(p))). For finite NN, additive (Lidstone) smoothing with βs>0\beta_{s}>0 (e.g., βs=1\beta_{s}=1 for Laplace smoothing) addresses problematic zero counts where C⁡(r)=0C(r)=0 but C⁡(A)>0C(A)>0, yielding p^N(βs)​(r)=(C⁡(r)+βs)/(C⁡(A)+βs​|RA|)\hat{p}_{N}^{(\beta_{s})}(r)=(C(r)+\beta_{s})/(C(A)+\beta_{s}|R_{A}|).

Beyond this (smoothed) MLE, other PCFG estimation models exist. The Bayesian PCFG Model offers one such alternative. It interprets additive smoothing, using a parameter α\alpha such that p^N(α)​(r)=(C⁡(r)+α)/(C⁡(A)+α​|RA|)\hat{p}_{N}^{(\alpha)}(r)=(C(r)+\alpha)/(C(A)+\alpha|R_{A}|), as computing the posterior mean. This is under a symmetric Dirichlet prior, Dir​(α,…,α)\text{Dir}(\alpha,\dots,\alpha), over rule choices for each non-terminal, where the concentration parameter α>0\alpha>0 reflects the prior’s strength. Another approach is the Neural PCFG Model. This model utilizes a neural network fϕ​(r)f_{\phi}(r) to score rules r=(A→β)r=(A\rightarrow\beta). As alluded to in the Approximation section’s discussion of data collection, this model can leverage richer contextual features. Probabilities are then defined as pNeural​(r)=exp⁡(fϕ​(r))/∑r′∈RAexp⁡(fϕ​(r′))p_{\text{Neural}}(r)=\exp(f_{\phi}(r))/\sum_{r^{\prime}\in R_{A}}\exp(f_{\phi}(r^{\prime})). Network parameters ϕ\phi are trained by maximizing the log-likelihood of the corpus Π⁡(𝒫N)\Pi(\mathcal{P}_{N}), enabling the capture of complex dependencies.

###### Theorem 1 (Coverage Guarantee).

Let μ\mu be a distribution on a discrete sample space Σ∗\Sigma^{*}, with Shannon entropy H(μ)=−∑x∈Σ∗μ(x)log2μ(x).H(\mu)\;=\;-\sum_{x\in\Sigma^{*}}\mu(x)\,\log_{2}\mu(x). Suppose we draw NN i.i.d. samples from μ\mu. Then, for _any_ measurable subset A⊆Σ∗A\subseteq\Sigma^{*} with μ⁡(A)=ϵ\mu(A)=\epsilon, the probability that none of the NN samples land in AA is at most exp⁡(−N​ϵ2H⁡(μ)),\exp\\!\Bigl(-\,\tfrac{N\,\epsilon}{2^{\,H(\mu)}}\Bigr), provided NN is sufficiently large. Equivalently, the probability of failing to sample at least one point in _every_ region of mass ϵ\epsilon is at most exp(−Nϵ/ 2H⁡(μ))\exp(-\,N\,\epsilon/\,2^{H(\mu)}). Moreover, the largest ϵ\epsilon for which this “miss probability” is itself at most ϵ\epsilon satisfies ϵ=2H⁡(μ)N​W​(N2H⁡(μ)),\epsilon\;=\;\frac{2^{\,H(\mu)}}{N}\,W\\!\Bigl(\tfrac{N}{2^{\,H(\mu)}}\Bigr), where W⁡(⋅)W(\cdot) is the Lambert WW-function. As NN grows large, ϵ≈2H⁡(μ)N​ln⁡(N2H⁡(μ)),\epsilon\;\approx\;\frac{2^{\,H(\mu)}}{N}\,\ln\\!\Bigl(\tfrac{N}{2^{\,H(\mu)}}\Bigr), which vanishes at rate on the order of ln⁡(N)/N\ln(N)/N. Proof is provided in the appendix.

### 2.1 Probabilistic Context-Free Grammar (PCFG) Derived Metrics

We derive several PCFG metrics to quantify different facets of uncertainty, using established notation (e.g., RAR_{A} for the set of rules expanding non-terminal AA).

Static Metrics for Grammar Structure and Complexity Basic structural properties of the grammar GS​M​TG_{SMT} provide a foundational understanding of its scale and potential complexity. These include the number of non-terminals (|VS​M​T||V_{SMT}|) and rules (|RS​M​T||R_{SMT}|), the average number of rules per non-terminal (|RS​M​T||VS​M​T|\frac{|R_{SMT}|}{|V_{SMT}|}), and the average right-hand side (RHS) length (1|RS​M​T|​∑A→β∈RS​M​T|β|\frac{1}{|R_{SMT}|}\sum_{A\rightarrow\beta\in R_{SMT}}|\beta|, where |β||\beta| denotes the length of β\beta). Further metrics cover the maximum branching factor (maxA∈VS​M​T⁡|RA|\max_{A\in V_{SMT}}|R_{A}|), and the detection of various forms of recursion (e.g., left-recursion A→A​γA\rightarrow A\gamma or right-recursion A→γ​AA\rightarrow\gamma A). These metrics collectively characterize the grammar’s static architecture.

Spectral Properties The spectral radius of the grammar’s mean matrix (often referred to as the Jacobian matrix in this context), B∈ℝ|VS​M​T|×|VS​M​T|B\in\mathbb{R}^{|V_{SMT}|\times|V_{SMT}|}, offers insights into its recursive structure and complexity. An element Bj​iB_{ji} is the expected number of times non-terminal AjA_{j} appears on the right-hand side (RHS) of a production chosen for AiA_{i}: Bj​i=∑Ai→β∈RAip⁡(Ai→β)×count​(Aj,β)B_{ji}=\sum_{A_{i}\rightarrow\beta\in R_{A_{i}}}p(A_{i}\rightarrow\beta)\times\text{count}(A_{j},\beta), where count​(Aj,β)\text{count}(A_{j},\beta) is AjA_{j}’s occurrences in β\beta. The spectral radius ρ⁡(B)=max⁡{|λ|∣det(B−λ​I)=0}\rho(B)=\max\\{|\lambda|\mid\det(B-\lambda I)=0\\} is BB’s maximum absolute eigenvalue. Typically, ρ⁡(B)<1\rho(B)<1 indicates a ‘proper’ grammar with finite expected derivation lengths, while ρ⁡(B)≥1\rho(B)\geq 1 suggests potentially unbounded derivations or higher complexity, contributing to structural uncertainty. This spectral radius is also a key component of the NSUI metric (introduced later in this section).

Information-Theoretic Measures Information theory provides principled ways to measure the uncertainty associated with probabilistic choices within the grammar. The Shannon Entropy per Non-terminal, for each A∈VS​M​TA\in V_{SMT}, quantifies the average uncertainty (in bits) in selecting a production rule from RAR_{A}: H(A)=−∑A→β∈RAp(A→β)log2p(A→β)H(A)=-\sum_{A\rightarrow\beta\in R_{A}}p(A\rightarrow\beta)\log_{2}p(A\rightarrow\beta) A higher H⁡(A)H(A) indicates greater uncertainty or variability in the expansions of AA. The Rényi Entropy per Non-terminal, Hα​(A)H_{\alpha}(A), generalizes Shannon entropy and is parameterized by an order α≥0\alpha\geq 0. For α≠1\alpha\neq 1: Hα​(A)=11−α​log⁡∑A→β∈RA2⁡p​(A→β)αH_{\alpha}(A)=\frac{1}{1-\alpha}\log_{2}\sum_{A\rightarrow\beta\in R_{A}}p(A\rightarrow\beta)^{\alpha} Key special cases include Shannon entropy (H1​(A)=H​(A)H_{1}(A)=H(A) as α→1\alpha\to 1), max-entropy (H0​(A)=log2⁡|RA|H_{0}(A)=\log_{2}|R_{A}| for α=0\alpha=0, reflecting the number of choices), collision entropy (H2​(A)=−log⁡∑A→β∈RA2⁡p​(A→β)2H_{2}(A)=-\log_{2}\sum_{A\rightarrow\beta\in R_{A}}p(A\rightarrow\beta)^{2} for α=2\alpha=2, sensitive to rule choice repetition), and min-entropy (H∞​(A)=−log2⁡maxA→β∈RA⁡p⁡(A→β)H_{\infty}(A)=-\log_{2}\max_{A\rightarrow\beta\in R_{A}}p(A\rightarrow\beta) for α→∞\alpha\to\infty, determined by the most probable rule). Calculating Rényi entropy for different α\alpha values (e.g., 0.5,20.5,2) provides a richer characterization of the uncertainty profile than Shannon entropy alone. The Overall Grammar Entropy is typically defined as the weighted average of the Shannon entropies of its non-terminals, H⁡(A)H(A), where weights π⁡(A)\pi(A) correspond to the stationary distribution or expected frequency of non-terminal AA in derivations starting from SS​M​TS_{SMT}: H⁡(G)=∑A∈VS​M​Tπ⁡(A)​H​(A)H(G)=\sum_{A\in V_{SMT}}\pi(A)H(A). The frequencies π⁡(A)\pi(A) can be estimated iteratively. H⁡(G)H(G) represents the average uncertainty per derivation step across the entire grammar. Perplexity, P​P​(G)PP(G), measures how well the PCFG predicts derivations and is the exponentiated grammar entropy: P​P​(G)=2H⁡(G)PP(G)=2^{H(G)}. It can be interpreted as the effective average number of choices the grammar presents at each derivation step, weighted by likelihood; lower perplexity indicates a more predictable grammar. The KL divergence, DK​L(pA||UA)=log2|RA|−H(A)D_{KL}(p_{A}||U_{A})=\log_{2}|R_{A}|-H(A), quantifies the inefficiency (in bits) of assuming a uniform rule distribution (U⁡(A→β)=1/|RA|U(A\rightarrow\beta)=1/|R_{A}|) for a non-terminal AA compared to using the true PCFG probabilities (p⁡(A→β)p(A\rightarrow\beta)). The overall grammar KL divergence from uniform, DK​L(G||U)=∑A∈VS​M​Tπ(A)DK​L(pA||UA)D_{KL}(G||U)=\sum_{A\in V_{SMT}}\pi(A)D_{KL}(p_{A}||U_{A}), quantifies the PCFG’s deviation from maximum uncertainty.

Finally, we hypothesize a novel composite metric, N​S​U​I​(G)NSUI(G), for probabilistic uncertainty and structural complexity. This metric, which ranges from 00 to 11, combines normalized grammar entropy with a factor reflecting the grammar’s recursive structure (via its spectral radius ρ⁡(B)\rho(B)). It is calculated as N​S​U​I​(G)=Er​a​t​i​o×Sf​a​c​t​o​rNSUI(G)=E_{ratio}\times S_{factor}. The entropy ratio Er​a​t​i​o=H⁡(G)/Hmax​(G)∈[0,1]E_{ratio}=H(G)/H_{\max}(G)\in[0,1] uses the maximum grammar entropy Hmax​(G)=∑A∈VS​M​Tπ⁡(A)​log2​|RA|H_{\max}(G)=\sum_{A\in V_{SMT}}\pi(A)\log_{2}|R_{A}| (assuming uniform rule choices). The spectral factor is Sf​a​c​t​o​r=ρ⁡(B)/(1+ρ⁡(B))∈[0,1)S_{factor}=\rho(B)/(1+\rho(B))\in[0,1). The motivation was to link higher NSUI values to indicate greater probabilistic uncertainty via structural/recursive complexity.

Rule Probability Distribution Metrics Analyzing the set of all rule probabilities 𝒫={p⁡(A→β)∣A→β∈RS​M​T}\mathcal{P}=\\{p(A\rightarrow\beta)\mid A\rightarrow\beta\in R_{SMT}\\} involves computing descriptive statistics such as mean, median, minimum, maximum, standard deviation (σ⁡(𝒫)\sigma(\mathcal{P})), skewness (γ1​(𝒫)\gamma_{1}(\mathcal{P})), and kurtosis (γ2​(𝒫)\gamma_{2}(\mathcal{P})). These statistics characterize the shape and spread of the learned probabilities. Fitting parametric distributions (e.g., Pareto, power-law) can further reveal structural patterns like Zipfian distributions, which are common in linguistic phenomena.

Text SC reflects solution consistency (e.g., via majority vote) across multiple LLM textual outputs, while SMT SC measures it (e.g., via SMT solver agreement) across diverse LLM-generated SMT-LIB programs for the same prompt, adapting principles from (Wang et al., 2022). We also implement four distinct ensemble predictors for enhanced uncertainty quantification. These are: (1) Ensemble Simple, an unweighted average of a key subset of metrics; (2) Ensemble Average, a comprehensive unweighted average of all metric scores; (3) Ensemble Weighted, where individual metric contributions are varied based on validation performance or theoretical importance; and (4) Ensemble ML, a meta-machine learning model (e.g., logistic regression) trained on the vector of metric scores to predict errors. This approach aims to improve overall predictive accuracy, calibration, and robustness by combining varied uncertainty signals.

Metrics for Evaluating Uncertainty-Based Error Detection To evaluate uncertainty quantification (UQ) methods for identifying prediction errors, we examine several facets: Error Discrimination utilizes the Area Under the Receiver Operating Characteristic Curve (AUROC) to assess if uncertainty scores distinguish correct from incorrect predictions; a higher AUROC signifies better uncertainty-error alignment. Selective Prediction Utility employs the Area Under the Risk-Coverage Curve (AURC) to measure practical risk mitigation via abstention (including analysis of optimal abstention percentages, associated error rates, and relative error reduction); lower AURC indicates effective error identification, improving performance on retained samples. Finally, Calibration Assessment evaluates the probabilistic reliability of confidence scores using metrics like Expected Calibration Error (ECE), Reliability Diagrams, and the Brier Score; lower ECE and Brier scores denote better calibration, where predicted confidence accurately reflects empirical correctness rates.

## 3 Results

We have evaluated five frontier LLMs, namely o3-mini, DeepSeekR1 (with CoT enabled (Wei et al., 2022b)), DeepSeek-v3-04-21, Gemini Flash 2.0 & Lite (non-reasoning), on four datasets which are widely adopted and used for reasoning tasks; StrategyQA (Geva et al., 2021), ProntoQA (Saparov and He, 2023), ProofWriter(Tafjord et al., 2021) and FOLIO (Han et al., 2024). From 5 LLM samples per question, answers were derived via: 1) Text: direct LLM output (intrinsic reasoning over text); 2) SMT: LLM-generated SMT-LIB solved by Z3 (autoformalization). Notably, SMT-LIB generation required significantly less effort (more syntactically valid programs in fewer attempts) and used dramatically fewer tokens per prompt compared to (Ganguly et al., 2024), while also offering multi-solver interoperability.

On ProofWriter, a task closely aligned with symbolic logic, SMT-based methods yielded substantial improvements for three models, particularly benefiting those that struggle with direct formal reasoning. Conversely, on ProntoQA and FOLIO, direct textual reasoning consistently outperformed SMT across most models, suggesting that for these QA tasks, the overhead introduced during autoformalization outweighs potential benefits. StrategyQA showed mixed results, with o3-mini slightly benefiting from SMT while other models performed better with direct reasoning.

The SMT approach systematically alters error profiles compared to direct reasoning, often trading precision for recall. For struggling models, autoformalization frequently increases recall dramatically while reducing precision, reflecting a tendency to provide formal answers more often but introducing additional false positives—consistent with LLMs’ documented proclivity toward proving satisfiability in (Ganguly et al., 2024). On ProofWriter, where SMT generally helped, performance gains stemmed from simultaneous improvements in both precision and recall, indicating the approach successfully addressed fundamental reasoning errors. Conversely, on datasets where direct reasoning excelled, SMT’s underperformance typically manifested as reduced recall, suggesting failures in the formalization process resulted in missed correct answers.

[htbp] Benchmarking accuracy of frontier LLMs using direct text output (Text) versus SMT-LIB generation solved by Z3 (SMT). No approach universally outperforms the other across all models and datasets. Finer grained results are available in the supplementary material. ACCURACY StrategyQA ProntoQA ProofWriter FOLIO Text SMT δ\delta Text SMT δ\delta Text SMT δ\delta Text SMT δ\delta o3-mini 0.7828 0.7980 -0.0152 1.0000 0.9980 0.0020 0.8893 0.9418 -0.0524 0.9450 0.5000 0.4450 DeepSeekv3 0.8292 0.6720 0.1572 1.0000 0.4501 0.5499 0.8057 0.5800 0.2257 0.9333 0.5961 0.3372 DeepSeek R1 0.8580 0.7760 0.0820 0.9939 0.7440 0.2499 0.9423 0.4935 0.4488 0.9252 0.5200 -0.4052 Flash 2.0 0.7188 0.5360 0.1828 0.9820 0.9000 0.0820 0.4900 0.6660 -0.1760 0.9010 0.5625 0.3385 Flash 2.0 Lite 0.6760 0.4500 0.2260 0.9980 0.9980 0.0000 0.4060 0.7540 -0.3480 0.9017 0.7321 0.1696

Our results reveal predominantly epistemic uncertainty in both reasoning approaches. Direct reasoning fails through knowledge gaps and procedural errors, while SMT introduces formalization errors when translating to formal specifications. This explains task-dependent performance: SMT benefits tasks with explicit premises (ProofWriter) by isolating deductive reasoning, while knowledge-intensive tasks (StrategyQA) expose formalization bottlenecks. These findings highlight the critical need for Uncertainty Quantification on LLM-generated formal artifacts to prevent upstream formalization errors from propagating through otherwise sound solvers.

Table 1: Token-level Uncertainty quantification metrics and their results at detecting autoformalization errors w.r.t. ground truth for DeepSeek-v3-0324 across reasoning datasets. While conventional metrics (AUROC, ECE, Brier) show moderate performance, they inadequately capture the distinct epistemic uncertainties in formalization versus reasoning processes. Notably, no UQ method consistently excels across tasks . The uncertainty-aware abstention metrics reflect how the model can selectively answer questions by applying an optimal uncertainty threshold (Opt.Thresh) that minimizes error rate (Err@T) and maximizes error reduction (RelErrRed) compared to answering all questions.This suggests the need for specialized UQ approaches that explicitly model the distribution of formal artifacts. DeepSeekv3 is the only model we examined that provides token logprobs. |  | AUROC | ECE | Brier | AURC | Opt.T | Err@T | RelErrRed  
---|---|---|---|---|---|---|---|---  
StrategyQA | Entropy | 0.5872 | 0.1415 | 0.2433 | 0.2399 | 0.0500 | 0.3221 | 0.0180  
| Perplexity | 0.6179 | 0.0802 | 0.2218 | 0.2218 | 0.5000 | 0.2520 | 0.2317  
| Kurtosis | 0.6227 | 0.3038 | 0.3075 | 0.2236 | 0.5000 | 0.2440 | 0.2561  
ProntoQA | Entropy | 0.5622 | 0.1395 | 0.2685 | 0.4585 | 0.0500 | 0.5408 | 0.0166  
| Perplexity | 0.6118 | 0.1009 | 0.2522 | 0.4218 | 0.0500 | 0.5365 | 0.0244  
| Kurtosis | 0.6078 | 0.2390 | 0.2990 | 0.4265 | 0.2000 | 0.5102 | 0.0722  
ProofWriter | Entropy | 0.5165 | 0.1666 | 0.2761 | 0.3938 | 0.0500 | 0.4105 | 0.0226  
| Perplexity | 0.5893 | 0.2430 | 0.3021 | 0.3214 | 0.4000 | 0.3633 | 0.1349  
| Kurtosis | 0.5656 | 0.1657 | 0.2705 | 0.3322 | 0.4500 | 0.3564 | 0.1515  
FOLIO | Entropy | 0.7001 | 0.2101 | 0.2465 | 0.4737 | 0.5000 | 0.4767 | 0.2679  
| Perplexity | 0.5609 | 0.2385 | 0.2926 | 0.5514 | 0.0500 | 0.6380 | 0.0202  
| Kurtosis | 0.5548 | 0.1761 | 0.2428 | 0.5560 | 0.0500 | 0.6319 | 0.0296  
  
### 3.1 Performance of Uncertainty Metrics

We evaluated our uncertainty metrics in two distinct prediction tasks: (1) whether LLM-generated SMT programs, when executed by Z3, would yield the correct ground truth answer, and (2) whether the SMT output would be consistent with the model’s own natural language reasoning. It is important to note here that PCFG computation for uncertainty quantification imposes minimal computational overhead. Since we utilize the well-defined SMT-LIB grammar rather than learning it, parsers operate efficiently on the structured outputs. While we explored various estimation techniques (e.g., Bayesian PCFG, Neural PCFG), Maximum Likelihood Estimation (MLE) proved to be both computationally efficient and sufficiently accurate for uncertainty modeling, aligning with established practices.

Experiments for model and dataset combinations were chosen where a performance gap was observed, with N=100 samples, thereby making UQ analysis meaningful, but where the SMT performance was not close to random guessing. Our argument here is that because we are relying on information within the FV artifacts, and those artifacts are not well-calibrated for the task (i.e., operating at the level of random guessing), we cannot extract information about failure from them.

Task-Dependent Signal Dominance in SMT vs Ground Truth Prediction:

Knowledge-Intensive Reasoning: For StrategyQA, cross-modal agreement metrics consistently dominated. O3-mini showed strong performance with grammar entropy (AUROC=0.7448, AURC=0.1113) and text consistency (AUROC=0.7369, AURC=0.1081). For DeepSeek-R1, text consistency substantially outperformed all pure PCFG metrics (AUROC=0.7835, AURC=0.0983). This indicates epistemic uncertainty in world knowledge as the primary correctness bottleneck as these cross-modal metrics effectively gauge if the SMT formalization aligns with the LLM’s initial (potentially flawed) semantic interpretation.

Premise-Explicit Reasoning: For ProofWriter, PCFG-derived metrics demonstrated exceptional discriminative power for ground truth prediction. O3-mini achieved near-perfect performance with grammar entropy (AUROC=0.9301, AURC=0.0008) and perplexity (AUROC=0.9194, AURC=0.0008). This confirms procedural epistemic uncertainty dominates in formal reasoning tasks, where an LLM’s primary challenge shifts from knowledge recall to the correct application of formal rules. Thus, PCFG metrics assessing structural variance in the SMT-LIB output can identify such deductive missteps with high precision—o3-mini’s AURC of 0.0008 using grammar entropy, for instance, enables filtering nearly all errors by abstaining on a minute fraction of outputs.

[!htb] Uncertainty quantification metrics for predicting ground truth correctness via PCFGs of LLM-generated SMT programs. Results show AUROC, ECE, Brier, and AURC across models and reasoning tasks, with ensemble methods consistently outperforming individual metrics. Color intensity indicates performance strength (darker green = better) StrategyQA ProofWriter o3-mini DeepSeek-v3-0324 o3-mini Gemini 2.0 Flash Lite Metric AUROC ECE Brier AURC AUROC ECE Brier AURC AUROC ECE Brier AURC AUROC ECE Brier AURC Grammar Entropy 0.7448 0.3058 0.2340 0.1113 0.7087 0.1575 0.2302 0.2097 0.9301 0.4419 0.2500 0.0008 0.5380 0.3185 0.2869 0.1405 Perplexity 0.5589 0.3107 0.2862 0.1811 0.6122 0.1601 0.2641 0.2497 0.9194 0.5358 0.3515 0.0008 0.5934 0.3888 0.3182 0.1267 KL Divergence 0.6428 0.2485 0.2385 0.1471 0.5723 0.1393 0.2322 0.2878 0.5108 0.5167 0.3260 0.0074 0.5164 0.3080 0.2797 0.1573 NSUI 0.6334 0.2436 0.2539 0.1250 0.5997 0.0781 0.2191 0.2672 0.5645 0.5710 0.3843 0.0084 0.5243 0.3186 0.2642 0.1514 Renyi Ent (2) 0.5175 0.3303 0.2997 0.1977 0.6195 0.1622 0.2679 0.2429 0.8871 0.5405 0.3598 0.0013 0.5996 0.4102 0.3368 0.1285 Renyi Ent (0.5) 0.5973 0.3398 0.3042 0.1634 0.6126 0.1623 0.2626 0.2517 0.9301 0.4724 0.2879 0.0008 0.5933 0.4401 0.3581 0.1258 Max Ent 0.6649 0.3553 0.2935 0.1297 0.6851 0.0473 0.2099 0.2271 0.9086 0.7198 0.5550 0.0013 0.5417 0.3503 0.3045 0.1420 Ent Ratio 0.5385 0.3283 0.3028 0.1834 0.5311 0.1336 0.2538 0.3306 0.5860 0.5714 0.3764 0.0055 0.5177 0.3943 0.3426 0.1548 Spectral Factor 0.6334 0.2173 0.2364 0.1319 0.6800 0.0992 0.2236 0.2365 0.7473 0.3458 0.2247 0.0032 0.5011 0.5048 0.4157 0.1578 Spectral Radius 0.6334 0.2892 0.2747 0.1319 0.6800 0.0686 0.2148 0.2365 0.7473 0.3545 0.2305 0.0032 0.5011 0.3930 0.3172 0.1578 # Nonterminals 0.5111 0.3540 0.3188 0.2006 0.6115 0.1329 0.2469 0.2547 0.8011 0.4267 0.2397 0.0019 0.5167 0.4838 0.4215 0.1672 # Rules 0.5548 0.2117 0.2385 0.1855 0.6197 0.1109 0.2252 0.2583 0.5108 0.4186 0.2201 0.0084 0.5549 0.2422 0.2315 0.1370 Avg Rules / NT 0.5737 0.2400 0.2415 0.1752 0.6021 0.0902 0.2260 0.2616 0.9301 0.5393 0.3499 0.0008 0.5840 0.2790 0.2656 0.1301 Avg RHS Len 0.5350 0.6141 0.5651 0.1979 0.5122 0.1753 0.2712 0.3279 0.8011 0.6535 0.5086 0.0026 0.5631 0.3413 0.2906 0.1480 Max Branch Factor 0.5181 0.1500 0.1997 0.1990 0.6180 0.1450 0.2270 0.2688 0.5914 0.2979 0.1377 0.0055 0.5745 0.2189 0.2293 0.1355 Rule Dist Mean 0.5740 0.3161 0.2836 0.1752 0.6021 0.1811 0.2534 0.2616 0.9301 0.4945 0.3034 0.0008 0.5838 0.4368 0.3713 0.1301 Rule Dist StdDev 0.5291 0.3995 0.3517 0.1811 0.5281 0.1251 0.2573 0.3116 0.5108 0.5555 0.3723 0.0074 0.5144 0.4474 0.3795 0.1559 Rule Dist Skew 0.5833 0.3178 0.2850 0.1689 0.6036 0.1431 0.2489 0.2610 0.9301 0.4923 0.2987 0.0008 0.5844 0.4511 0.3779 0.1313 Rule Dist Kurtosis 0.5659 0.3948 0.3420 0.1785 0.5787 0.1720 0.2600 0.2754 0.5860 0.5107 0.3115 0.0055 0.5044 0.1437 0.1913 0.1726 Self Consistency Text 0.7369 0.1604 0.1603 0.1081 0.6017 0.2874 0.3048 0.2882 0.8990 0.0423 0.0280 0.0020 0.5525 0.2283 0.2419 0.1376 Self Consistency SMT 0.7416 0.1523 0.1609 0.1051 0.6203 0.2318 0.2745 0.2513 0.7121 0.8501 0.7764 0.0025 0.7364 0.3535 0.2751 0.1031 Ensemble Average 0.7622 0.3724 0.2916 0.1103 0.6795 0.1214 0.2077 0.2182 0.9949 0.3356 0.1414 0.0005 0.6140 0.3922 0.3192 0.1240 Ensemble Weighted 0.7657 0.1738 0.1617 0.1099 0.7211 0.1257 0.2135 0.1989 0.9785 0.4612 0.2566 0.0003 0.7235 0.3327 0.2539 0.1035 Ensemble ML 0.7850 0.2090 0.1756 0.1013 0.7709 0.0877 0.1968 0.1847 0.9892 0.0572 0.0280 0.0003 0.7631 0.2897 0.2229 0.0823 Ensemble Simple 0.6702 0.2055 0.2104 0.1410 0.6401 0.1763 0.2514 0.2483 0.9355 0.4419 0.2582 0.0008 0.6476 0.3867 0.3039 0.1071

Predicting SMT-Text Consistency:

Arithmetic Reasoning: On ProntoQA with Gemini Flash 2.0, SMT consistency achieved remarkable performance in predicting text-SMT alignment (AUROC=0.9291, AURC=0.0084), while spectral radius (AUROC=0.6425, AURC=0.0379) emerged as the only effective structural metric. This isolates recursive complexity as a distinct source of uncertainty in arithmetic formalization, as excessively convoluted SMT structures, indicated by a high spectral radius, risk diverging from the model’s more direct textual reasoning on numerical problems.

Model-Specific Patterns: For Gemini Flash 2.0 Lite on StrategyQA, kurtosis of the rule distribution was the strongest predictor of SMT-Text consistency (AUROC=0.8695). Analysis revealed a distinctive switching" behavior between minimal and verbose SMT patterns, producing a bimodal distribution with heavy tails—a novel diagnostic for capacity limitations in formalization, whereby such stylistic oscillations between overly terse or verbose SMT, captured by kurtosis, make the resulting formal artifact more prone to misalign with the intended textual meaning.

[!htb] Uncertainty metrics based on PCFGs for predicting consistency between LLM’s SMT formalization and its natural language reasoning. Task-specific uncertainty patterns emerge: rule distribution kurtosis dominates for StrategyQA (AUROC=0.8695), while different metrics excel for each model-task combination, highlighting the multifaceted nature of formalization uncertainty. StrategyQA ProofWriter DeepSeek R1 DeepSeekv3-0324 Gemini 2.0 Flash Lite o3-mini Metric AUROC ECE Brier AURC AUROC ECE Brier AURC AUROC ECE Brier AURC AUROC ECE Brier AURC Grammar Entropy 0.7609 0.4617 0.2968 0.0216 0.7354 0.3058 0.2551 0.0970 0.6622 0.1277 0.2095 0.5689 0.8602 0.4419 0.2542 0.0013 Perplexity 0.6211 0.3789 0.2640 0.0361 0.6721 0.3282 0.2718 0.1205 0.7212 0.3255 0.2849 0.5273 0.9032 0.4429 0.2616 0.0013 KL Divergence 0.5776 0.4408 0.2855 0.0443 0.5335 0.1195 0.1780 0.1633 0.5486 0.2387 0.2630 0.6341 0.6667 0.5167 0.3238 0.0039 NSUI 0.5963 0.2529 0.1433 0.0462 0.5973 0.1768 0.1919 0.1411 0.6741 0.1195 0.1624 0.5221 0.9355 0.4077 0.2172 0.0008 Renyi Ent (2) 0.6242 0.3980 0.2746 0.0378 0.6799 0.3403 0.2808 0.1160 0.7624 0.3192 0.2624 0.5037 0.9032 0.4382 0.2580 0.0013 Renyi Ent (0.5) 0.6149 0.3942 0.2755 0.0376 0.6667 0.3333 0.2751 0.1223 0.6994 0.2766 0.2619 0.5438 0.8925 0.5063 0.3246 0.0013 Max Ent 0.7174 0.3994 0.2341 0.0262 0.6353 0.1309 0.1738 0.1247 0.5982 0.3401 0.3083 0.5900 0.9355 0.2589 0.1029 0.0008 Ent Ratio 0.5217 0.5047 0.3529 0.0543 0.6154 0.4091 0.3307 0.1446 0.5511 0.1641 0.2511 0.6346 0.9677 0.4074 0.2082 0.0003 Spectral Factor 0.5481 0.1533 0.0927 0.0640 0.7034 0.1254 0.1580 0.1206 0.6538 0.0943 0.1677 0.5316 0.5269 0.6329 0.5061 0.0084 Spectral Radius 0.5481 0.2067 0.1166 0.0640 0.7034 0.1896 0.1752 0.1206 0.6538 0.1648 0.1703 0.5316 0.5269 0.6243 0.4953 0.0084 # Nonterminals 0.5264 0.5679 0.4237 0.0557 0.5549 0.2271 0.2455 0.1480 0.5166 0.4180 0.3958 0.6509 0.6505 0.5520 0.3650 0.0047 # Rules 0.6087 0.3083 0.1839 0.0396 0.5675 0.2025 0.2077 0.1485 0.5749 0.4256 0.3818 0.6252 0.5108 0.4186 0.2201 0.0064 Avg Rules / NT 0.7034 0.4068 0.2532 0.0273 0.6034 0.1393 0.1854 0.1399 0.6565 0.2913 0.2761 0.5923 0.8011 0.4394 0.2554 0.0026 Avg RHS Len 0.5637 0.2491 0.1566 0.0544 0.5208 0.1254 0.1818 0.1972 0.6014 0.4855 0.4420 0.6098 0.5054 0.6535 0.5116 0.0074 Max Branch Factor 0.6801 0.3325 0.2042 0.0324 0.5937 0.1563 0.1920 0.1457 0.5818 0.5167 0.4747 0.6313 0.7419 0.6809 0.5100 0.0032 Rule Dist Mean 0.7034 0.5352 0.3733 0.0273 0.6034 0.3210 0.2742 0.1399 0.6565 0.2197 0.2280 0.5923 0.8011 0.4842 0.2971 0.0026 Rule Dist StdDev 0.6056 0.6755 0.5361 0.0413 0.6281 0.2226 0.2221 0.1445 0.7183 0.3136 0.2807 0.5455 0.8710 0.4232 0.2392 0.0013 Rule Dist Skew 0.6848 0.4800 0.3260 0.0309 0.5986 0.3057 0.2619 0.1406 0.6796 0.1783 0.2199 0.5720 0.8172 0.4864 0.2964 0.0019 Rule Dist Kurtosis 0.5311 0.2521 0.1588 0.0534 0.6600 0.0731 0.1576 0.1256 0.8695 0.3187 0.2412 0.4448 0.9462 0.5107 0.3056 0.0008 Self Consistency Text 0.8245 0.1002 0.0751 0.0155 0.5778 0.1874 0.2008 0.1754 0.5350 0.2788 0.2616 0.6064 0.7050 0.9352 0.9023 0.0030 Self Consistency SMT 0.7570 0.2062 0.1373 0.0268 0.7116 0.1662 0.1909 0.1054 0.7505 0.5380 0.4357 0.4822 0.7100 0.8600 0.7863 0.0030 Ensemble Average 0.8183 0.4695 0.3058 0.0180 0.7064 0.1876 0.1831 0.0983 0.7927 0.1531 0.1702 0.4848 0.9300 0.3560 0.1741 0.0007 Ensemble Weighted 0.8494 0.3256 0.1711 0.0155 0.7709 0.2340 0.1971 0.0798 0.8070 0.1673 0.1632 0.4718 1.0000 0.4231 0.2375 0.0003 Ensemble ML 0.8245 0.3084 0.2003 0.0170 0.8517 0.1861 0.1703 0.0573 0.7946 0.1308 0.1592 0.4784 1.0000 0.0496 0.0199 0.0003 Ensemble Simple 0.6957 0.4363 0.2748 0.0316 0.6727 0.3021 0.2567 0.1119 0.7584 0.0796 0.1568 0.4929 0.6667 0.4419 0.2661 0.0039

Ablation Study Results PCFG spectral radius from LLM-generated SMT-LIB programs consistently decreases with sampling temperature, as broader exploration diversifies rule selections, reducing fixation on recursive productions that heavily influence moment matrix eigenvalues. Probability mass spreads more uniformly across production alternatives, diminishing single recursive pattern dominance and thus lowering the mean matrix’s maximum absolute eigenvalue. Notably, grammatical properties lack sharp phase transitions across temperature ranges; derived PCFGs show smooth, monotonic changes in spectral and information-theoretic characteristics, implying a continuous, rather than abrupt, generative response to temperature. Non-terminal expansion distributions shift from concentrated to broader with increasing temperature, though this plateaus, indicating finite exploration capacity, possibly constrained by inherent model biases or the grammar’s finite structure. The striking consistency of these spectral-temperature curves across diverse LLMs points to a fundamental, universal mechanism by which these models navigate the coherence-diversity trade-off when generating structured formal languages. Finally, our fine-grained localized entropy within PCFG production rules surpasses global or non-grammatical standard techniques in error prediction, confirming that granular structural uncertainty in specific grammatical constructs directly flags component-level semantic error likelihood, offering more precise diagnostics.

Discussion Our analysis reveals a fundamental insight: the syntactic atypicality (e.g., in PCFG rule entropy or usage kurtosis) of LLM-generated formal artifacts serves as a powerful signal for semantic errors, reminiscent of OOD detection (Ganguly et al., 2025). When LLMs correctly understand logical relationships, they consistently produce high-probability rule sequences, whereas semantic misunderstandings manifest as statistical anomalies—creating distinctive "syntactic fingerprints" of reasoning failure that enable our exceptional error detection (AUROC=0.9301 on ProofWriter). This typicality-based approach transcends architectures, its PCFG metric rankings consistently capturing intrinsic difficulties like formalizing ambiguous language across diverse models. However, the relationship between typicality and correctness isn’t straightforward; metrics with superior discriminative ability often exhibit poor calibration (ECE=0.4419), indicating anomaly magnitude doesn’t linearly predict error probability—necessitating calibration-aware fusion, perhaps by integrating consistency signals. Even more revealing is asymmetric self-consistency (e.g., Gemini/ProntoQA: SMT AUROC=0.9291 vs. text AUROC=0.5108), suggesting LLMs may use distinct, imperfectly aligned formal versus textual reasoning pathways, not just translate a unified process. Such insights shift neurosymbolic design from translation-focus to pathway-alignment and grounding, e.g., via joint training, as SMT syntactic typicality alone is insufficient if its pathway misaligns with textual reasoning.

## 4 Related Works

Formal Reasoning with LLMs LLMs show proficiency in formal reasoning (Welleck et al., 2022a; Chen et al., 2022), but face challenges including hallucination, uncertainty expression (Lin et al., 2022a), self-verification (Hou et al., 2023), and reasoning opacity (Wei et al., 2022b). Hybrid approaches combine LLMs with formal tools but often overlook model uncertainty. For autoformalization, early sequence-to-sequence models (Wang et al., 2018; Wang et al., 2020) evolved into LLM-based approaches (Wu et al., 2022; Agrawal et al., 2022; Gadgil et al., 2022; Murphy et al., 2024), with structured methods (Jiang et al., 2023b; Zhao et al., 2024) combining LLMs with ATPs, and various applications (Liu et al., 2023; Pan et al., 2023; Olausson et al., 2023; Ye et al., 2023; Zhou et al., 2024; Huang et al., 2024a; Xin et al., 2024a; Jiang et al., 2024; Quan et al., 2024; Xin et al., 2024b). Proofstep generation advanced from classification (Whalen, 2016; Huang et al., 2019; Bansal et al., 2019) to language modeling (Polu and Sutskever, 2020; First et al., 2023; Wang et al., 2024; Welleck et al., 2022b; Jiang et al., 2022), with recent work exploring zero-shot capabilities (Zhang et al., 2023; Yousefzadeh and Cao, 2023; Scheidt, 2023; Frieder et al., 2023a; Frieder et al., 2023b; Frieder et al., 2023c; Zhang et al., 2024a) and formal proof generation (Zheng et al., 2024; Xin et al., 2024a; Huang et al., 2024a; Thakur et al., 2024). Proof search strategies include supervised learning (Loos et al., 2017; Chvalovskỳ et al., 2019), reinforcement learning (Kusumoto et al., 2018; Crouse et al., 2021; Piepenbrock et al., 2021), MCTS (Wu et al., 2021; Lample et al., 2022; Wang et al., 2023a), and language-agent methods (Thakur et al., 2024; An et al., 2024).

Uncertainty in LLM Reasoning Research explores various uncertainty estimation approaches in language models: information-theoretic methods using entropy (Kadavath et al., 2022; Kuhn et al., 2023; Duan et al., 2024), perplexity (Mora-Cross and Calderon-Ramirez, 2024; Margatina et al., 2023), and mutual information (Malinin, 2019; Wimmer et al., 2023; Depeweg, 2019; Ash, 1965); ensemble strategies like MC Dropout (Srivastava et al., 2014; Gal and Ghahramani, 2016a; Lakshminarayanan et al., 2017), Deep Ensembles (Fadeeva et al., 2023; Lakshminarayanan et al., 2017), and BatchEnsemble (Gal and Ghahramani, 2016b; Lakshminarayanan et al., 2017; Wen et al., 2020) for hallucination detection (Arteaga et al., 2024); consistency techniques evaluating output agreement (Wang et al., 2023b; Cole et al., 2023; Huang et al., 2024b; Zhang et al., 2024b; Lakshminarayanan et al., 2017; Gawlikowski et al., 2023; Manakul et al., 2023; Chen and Mueller, 2024); similarity-based methods (Lin et al., 2024); Bayesian approaches including BNNs (Shridhar et al., 2019; Blundell et al., 2015), variational inference (Graves, 2011; Jordan et al., 1999; Kullback and Leibler, 1951), Gaussian processes (Iwata and Ghahramani, 2017; Liu et al., 2020), and MCMC (Xiao and Wang, 2018); and language-based methods extracting uncertainty from verbalizations (Cosmides and Tooby, 1996; Lin et al., 2022b; Tian et al., 2023; Xiong et al., 2024; Kojima et al., 2022; Groot and Valdenegro-Toro, 2024). Our work models implicit uncertainty in distributions over multiple formal outputs rather than relying on individual response signals.

Verification and Reasoning Uncertainty DTV (Zhou et al., 2024), SAT-LM (Ye et al., 2023), and related approaches (Quan et al., 2024) connect LLMs with formal verification, while latent space methods (Lee et al., 2020; Wu and Wu, 2021) complement uncertainty estimation research (Kadavath et al., 2022; Lin et al., 2022b). PCFGs, which add probabilities to CFGs, have applications in NLP (Manning and Schutze, 1999), bioinformatics (Durbin et al., 1998), and program analysis (Alur et al., 2014), along with enabling probabilistic analysis for LLM generated DSL programs(Barke et al., 2024). Our work extends PCFG inference (De la Higuera, 2010) to verification artifacts.

## 5 Conclusion

Our research presents a PCFG-based framework for SMT-LIB UQ, establishing that syntactic atypicalities in LLM-generated formal artifacts, previously underexploited, serve as potent, quantifiable

ntification for o3-mini on StrategyQA: Ensemble ML (AUROC 0.7850) and Self-Consistency metrics (Text/SMT AUROC 0.74) outperform most individual PCFG metrics (Grammar Entropy AUROC 0.7448 being a strong contender). This suggests that for o3-mini on this knowledge-intensive task, learned combinations or behavioral consistency signals are more potent than isolated SMT structural properties for error detection. StrategyQA - o3-mini  
---  
Metric | AUROC | ECE | Brier | AURC | Opt.T | Err@T | RelErrRed  
Grammar Entropy | 0.7448 | 0.3058 | 0.2340 | 0.1113 | 0.0500 | 0.1895 | 0.1388  
Perplexity | 0.5589 | 0.3107 | 0.2862 | 0.1811 | 0.2000 | 0.1750 | 0.2045  
KL Divergence | 0.6428 | 0.2485 | 0.2385 | 0.1471 | 0.3000 | 0.1429 | 0.3506  
NSUI | 0.6334 | 0.2436 | 0.2539 | 0.1250 | 0.1500 | 0.1882 | 0.1444  
Renyi Ent (2) | 0.5175 | 0.3303 | 0.2997 | 0.1977 | 0.3000 | 0.1857 | 0.1558  
Renyi Ent (0.5) | 0.5973 | 0.3398 | 0.3042 | 0.1634 | 0.2500 | 0.1600 | 0.2727  
Max Ent | 0.6649 | 0.3553 | 0.2935 | 0.1297 | 0.0500 | 0.1895 | 0.1388  
Ent Ratio | 0.5385 | 0.3283 | 0.3028 | 0.1834 | 0.3000 | 0.1857 | 0.1558  
Spectral Factor | 0.6334 | 0.2173 | 0.2364 | 0.1319 | 0.1500 | 0.1882 | 0.1444  
Spectral Radius | 0.6334 | 0.2892 | 0.2747 | 0.1319 | 0.1500 | 0.1882 | 0.1444  
# Nonterminals | 0.5111 | 0.3540 | 0.3188 | 0.2006 | 0.2000 | 0.2125 | 0.0341  
# Rules | 0.5548 | 0.2117 | 0.2385 | 0.1855 | 0.2000 | 0.1750 | 0.2045  
Avg Rules / NT | 0.5737 | 0.2400 | 0.2415 | 0.1752 | 0.2000 | 0.1625 | 0.2614  
Avg RHS Len | 0.5350 | 0.6141 | 0.5651 | 0.1979 | 0.0500 | 0.2105 | 0.0431  
Max Branch Factor | 0.5181 | 0.1500 | 0.1997 | 0.1990 | 0.1500 | 0.1882 | 0.1444  
Rule Dist Mean | 0.5740 | 0.3161 | 0.2836 | 0.1752 | 0.2000 | 0.1625 | 0.2614  
Rule Dist StdDev | 0.5291 | 0.3995 | 0.3517 | 0.1811 | 0.0500 | 0.2105 | 0.0431  
Rule Dist Skew | 0.5833 | 0.3178 | 0.2850 | 0.1689 | 0.1500 | 0.1765 | 0.1979  
Rule Dist Kurtosis | 0.5659 | 0.3948 | 0.3420 | 0.1785 | 0.0500 | 0.2000 | 0.0909  
Self Consistency Text | 0.7369 | 0.1604 | 0.1603 | 0.1081 | 0.1500 | 0.1529 | 0.3048  
Self Consistency SMT | 0.7416 | 0.1523 | 0.1609 | 0.1051 | 0.1500 | 0.1529 | 0.3048  
Ensemble Average | 0.7622 | 0.3724 | 0.2916 | 0.1103 | 0.1000 | 0.1556 | 0.2929  
Ensemble Weighted | 0.7657 | 0.1738 | 0.1617 | 0.1099 | 0.0500 | 0.1895 | 0.1388  
Ensemble ML | 0.7850 | 0.2090 | 0.1756 | 0.1013 | 0.1000 | 0.1556 | 0.2929  
Ensemble Simple | 0.6702 | 0.2055 | 0.2104 | 0.1410 | 0.2000 | 0.1500 | 0.3182  
  
For DeepSeek-v3 on StrategyQA, UQ metrics show a somewhat different pattern compared to o3-mini. Ensemble ML again provides the best overall discrimination (AUROC 0.7709), achieving a relative error reduction of 8.96% by abstaining on 5% of the samples. Interestingly, several individual PCFG-derived metrics, such as Grammar Entropy (AUROC 0.7087), Max Entropy (AUROC 0.6851), and Spectral Factor/Radius (AUROC 0.6800), demonstrate better discriminative power than the self-consistency metrics (AUROCs 0.60-0.62). This suggests that for DeepSeek-v3 on this task, intrinsic structural characteristics of the generated SMT are more indicative of correctness than its consistency with textual outputs. While Ensemble Simple yields the highest relative error reduction (35.14%), this comes at the cost of a high abstention rate (Opt.T 0.50), indicating practical trade-offs in selective prediction.

Table 3: Uncertainty Quantification for DeepSeek-v3 on StrategyQA: Ensemble ML leads with an AUROC of 0.7709. Several individual PCFG-based metrics like Grammar Entropy (AUROC 0.7087) and Max Entropy (AUROC 0.6851) show reasonable efficacy, outperforming self-consistency measures for this model. Metric | AUROC | ECE | Brier | AURC | Opt.T | Err@T | RelErrRed  
---|---|---|---|---|---|---|---  
Grammar Entropy | 0.7087 | 0.1575 | 0.2302 | 0.2097 | 0.05 | 0.3474 | 0.0612  
Perplexity | 0.6122 | 0.1601 | 0.2641 | 0.2497 | 0.5 | 0.28 | 0.2432  
KL Divergence | 0.5723 | 0.1393 | 0.2322 | 0.2878 | 0.05 | 0.3579 | 0.0327  
NSUI | 0.5997 | 0.0781 | 0.2191 | 0.2672 | 0.1 | 0.3222 | 0.1291  
Renyi Ent (2) | 0.6195 | 0.1622 | 0.2679 | 0.2429 | 0.45 | 0.2727 | 0.2629  
Renyi Ent (0.5) | 0.6126 | 0.1623 | 0.2626 | 0.2517 | 0.5 | 0.28 | 0.2432  
Max Ent | 0.6851 | 0.0473 | 0.2099 | 0.2271 | 0.1 | 0.3222 | 0.1291  
Ent Ratio | 0.5311 | 0.1336 | 0.2538 | 0.3306 | 0.05 | 0.3684 | 0.0043  
Spectral Factor | 0.68 | 0.0992 | 0.2236 | 0.2365 | 0.05 | 0.3474 | 0.0612  
Spectral Radius | 0.68 | 0.0686 | 0.2148 | 0.2365 | 0.05 | 0.3474 | 0.0612  
# Nonterminals | 0.6115 | 0.1329 | 0.2469 | 0.2547 | 0.45 | 0.2909 | 0.2138  
# Rules | 0.6197 | 0.1109 | 0.2252 | 0.2583 | 0.15 | 0.3176 | 0.1415  
Avg Rules / NT | 0.6021 | 0.0902 | 0.226 | 0.2616 | 0.05 | 0.3579 | 0.0327  
Avg RHS Len | 0.5122 | 0.1753 | 0.2712 | 0.3279 | 0.1 | 0.3444 | 0.0691  
Max Branch Factor | 0.618 | 0.145 | 0.227 | 0.2688 | 0.05 | 0.3474 | 0.0612  
Rule Dist Mean | 0.6021 | 0.1811 | 0.2534 | 0.2616 | 0.05 | 0.3579 | 0.0327  
Rule Dist StdDev | 0.5281 | 0.1251 | 0.2573 | 0.3116 | 0.5 | 0.32 | 0.1351  
Rule Dist Skew | 0.6036 | 0.1431 | 0.2489 | 0.261 | 0.1 | 0.3444 | 0.0691  
Rule Dist Kurtosis | 0.5787 | 0.172 | 0.26 | 0.2754 | 0.05 | 0.3579 | 0.0327  
Self Consistency Text | 0.6017 | 0.2874 | 0.3048 | 0.2882 | 0.1 | 0.3444 | 0.0691  
Self Consistency SMT | 0.6203 | 0.2318 | 0.2745 | 0.2513 | 0.1 | 0.3444 | 0.0691  
Ensemble Average | 0.6795 | 0.1214 | 0.2077 | 0.2182 | 0.1 | 0.3222 | 0.1291  
Ensemble Weighted | 0.7211 | 0.1257 | 0.2135 | 0.1989 | 0.05 | 0.3474 | 0.0612  
Ensemble ML | 0.7709 | 0.0877 | 0.1968 | 0.1847 | 0.05 | 0.3368 | 0.0896  
Ensemble Simple | 0.6401 | 0.1763 | 0.2514 | 0.2483 | 0.5 | 0.24 | 0.3514  
  
The UQ performance for o3-mini on ProofWriter is remarkably high, demonstrating the strong potential of PCFG-based metrics in formal reasoning contexts. Numerous individual metrics, including Grammar Entropy, Perplexity (AUROC 0.9194), Renyi Entropy (0.5) (AUROC 0.9301), Average Rules / NT (AUROC 0.9301), and various rule distribution statistics, achieve AUROC scores exceeding 0.90. More impressively, their AURC values are exceptionally low (e.g., 0.0008 for Grammar Entropy), translating to a 100% relative error reduction by abstaining on a small fraction of samples (e.g., 10%). This strongly supports the hypothesis that syntactic irregularities in generated formal artifacts are highly indicative of underlying semantic errors when the task aligns well with the formal language. Ensemble methods elevate this performance to near-perfection (Ensemble Average AUROC 0.9949). Despite the excellent discrimination, some metrics show high ECE values (e.g., Grammar Entropy ECE 0.4419), suggesting that while they can effectively rank outputs by correctness likelihood, their raw scores may not be perfectly calibrated across the entire probability spectrum.

Table 4: Uncertainty Quantification for o3-mini on ProofWriter: PCFG-derived metrics achieve exceptional discriminative power (e.g., Grammar Entropy AUROC 0.9301, AURC 0.0008), enabling near-perfect error detection with minimal abstention (100% RelErrRed at Opt.T 0.10). Ensemble methods (e.g., Ensemble Average AUROC 0.9949) further refine this, confirming that SMT structural properties are extremely strong predictors of correctness for o3-mini on this formal reasoning task. ProofWriter  
---  
Metric | AUROC | ECE | Brier | AURC | Opt.T | Err@T | RelErrRed  
Grammar Entropy | 0.9301 | 0.4419 | 0.25 | 0.0008 | 0.1000 | 0.0000 | 1.0000  
Perplexity | 0.9194 | 0.5358 | 0.3515 | 0.0008 | 0.1000 | 0.0000 | 1.0000  
KL Divergence | 0.5108 | 0.5167 | 0.326 | 0.0074 | 0.0000 | 0.0106 | 0.0000  
NSUI | 0.5645 | 0.571 | 0.3843 | 0.0084 | 0.0000 | 0.0106 | 0.0000  
Renyi Ent (2) | 0.8871 | 0.5405 | 0.3598 | 0.0013 | 0.1500 | 0.0000 | 1.0000  
Renyi Ent (0.5) | 0.9301 | 0.4724 | 0.2879 | 0.0008 | 0.1000 | 0.0000 | 1.0000  
Max Ent | 0.9086 | 0.7198 | 0.555 | 0.0013 | 0.1000 | 0.0000 | 1.0000  
Ent Ratio | 0.586 | 0.5714 | 0.3764 | 0.0055 | 0.4500 | 0.0000 | 1.0000  
Spectral Factor | 0.7473 | 0.3458 | 0.2247 | 0.0032 | 0.3000 | 0.0000 | 1.0000  
Spectral Radius | 0.7473 | 0.3545 | 0.2305 | 0.0032 | 0.3000 | 0.0000 | 1.0000  
# Nonterminals | 0.8011 | 0.4267 | 0.2397 | 0.0019 | 0.2000 | 0.0000 | 1.0000  
# Rules | 0.5108 | 0.4186 | 0.2201 | 0.0084 | 0.0000 | 0.0106 | 0.0000  
Avg Rules / NT | 0.9301 | 0.5393 | 0.3499 | 0.0008 | 0.1000 | 0.0000 | 1.0000  
Avg RHS Len | 0.8011 | 0.6535 | 0.5086 | 0.0026 | 0.2500 | 0.0000 | 1.0000  
Max Branch Factor | 0.5914 | 0.2979 | 0.1377 | 0.0055 | 0.4500 | 0.0000 | 1.0000  
Rule Dist Mean | 0.9301 | 0.4945 | 0.3034 | 0.0008 | 0.1000 | 0.0000 | 1.0000  
Rule Dist StdDev | 0.5108 | 0.5555 | 0.3723 | 0.0074 | 0.5000 | 0.0000 | 1.0000  
Rule Dist Skew | 0.9301 | 0.4923 | 0.2987 | 0.0008 | 0.1000 | 0.0000 | 1.0000  
Rule Dist Kurtosis | 0.586 | 0.5107 | 0.3115 | 0.0055 | 0.4500 | 0.0000 | 1.0000  
Self Consistency Text | 0.899 | 0.0423 | 0.028 | 0.002 | 0.0500 | 0.0105 | 0.4684  
Self Consistency SMT | 0.7121 | 0.8501 | 0.7764 | 0.0025 | 0.1500 | 0.0000 | 1.0000  
Ensemble Average | 0.9949 | 0.3356 | 0.1414 | 0.0005 | 0.0500 | 0.0000 | 1.0000  
Ensemble Weighted | 0.9785 | 0.4612 | 0.2566 | 0.0003 | 0.0500 | 0.0000 | 1.0000  
Ensemble ML | 0.9892 | 0.0572 | 0.028 | 0.0003 | 0.0500 | 0.0000 | 1.0000  
Ensemble Simple | 0.9355 | 0.4419 | 0.2582 | 0.0008 | 0.1000 | 0.0000 | 1.0000  
  
The UQ results for Gemini 2.0 Flash Lite on ProofWriter present a mixed picture, contrasting with o3-mini’s strong performance on the same task. Many individual PCFG-derived metrics demonstrate weak discriminative ability, with AUROC scores often between 0.50 and 0.59 (e.g., Grammar Entropy at 0.5380, Spectral Radius at 0.5011). However, SMT Self Consistency stands out as a significantly stronger individual performer with an AUROC of 0.7364. Ensemble methods, particularly Ensemble ML, achieve the best overall performance (AUROC 0.7631, AURC 0.0823), leading to a 14.61% relative error reduction when abstaining on 5% of the samples. This suggests that for Gemini 2.0 Flash Lite on ProofWriter, the structural variations in its SMT outputs are less consistently tied to semantic correctness compared to o3-mini. Instead, behavioral consistency (specifically, how its SMT outputs align with each other across multiple generations) and learned patterns across a combination of (often individually weaker) signals provide more reliable error detection.

Table 5: Uncertainty Quantification for Gemini 2.0 Flash Lite on ProofWriter: Performance is moderate; SMT Self Consistency (AUROC 0.7364) and Ensemble ML (AUROC 0.7631) are the strongest UQ signals. Most individual PCFG structural metrics show weak discriminative power (many AUROCs 0.50-0.59), indicating that for this model on ProofWriter, behavioral consistency (SMT-based) and learned combinations are more indicative of correctness than raw SMT syntactic properties alone. Metric | AUROC | ECE | Brier | AURC | Opt.T | Err@T | RelErrRed  
---|---|---|---|---|---|---|---  
Grammar Entropy | 0.5380 | 0.3185 | 0.2869 | 0.1405 | 0.4500 | 0.1667 | 0.1081  
Perplexity | 0.5934 | 0.3888 | 0.3182 | 0.1267 | 0.1000 | 0.1742 | 0.0680  
KL Divergence | 0.5164 | 0.3080 | 0.2797 | 0.1573 | 0.0000 | 0.1869 | 0.0000  
NSUI | 0.5243 | 0.3186 | 0.2642 | 0.1514 | 0.1500 | 0.1845 | 0.0125  
Renyi Ent (2) | 0.5996 | 0.4102 | 0.3368 | 0.1285 | 0.1000 | 0.1742 | 0.0680  
Renyi Ent (0.5) | 0.5933 | 0.4401 | 0.3581 | 0.1258 | 0.1000 | 0.1742 | 0.0680  
Max Ent | 0.5417 | 0.3503 | 0.3045 | 0.1420 | 0.5000 | 0.1717 | 0.0811  
Ent Ratio | 0.5177 | 0.3943 | 0.3426 | 0.1548 | 0.2000 | 0.1835 | 0.0178  
Spectral Factor | 0.5011 | 0.5048 | 0.4157 | 0.1578 | 0.0000 | 0.1869 | 0.0000  
Spectral Radius | 0.5011 | 0.3930 | 0.3172 | 0.1578 | 0.0000 | 0.1869 | 0.0000  
# Nonterminals | 0.5167 | 0.4838 | 0.4215 | 0.1672 | 0.1000 | 0.1854 | 0.0079  
# Rules | 0.5549 | 0.2422 | 0.2315 | 0.1370 | 0.4000 | 0.1610 | 0.1383  
Avg Rules / NT | 0.5840 | 0.2790 | 0.2656 | 0.1301 | 0.3000 | 0.1377 | 0.2632  
Avg RHS Len | 0.5631 | 0.3413 | 0.2906 | 0.1480 | 0.1000 | 0.1685 | 0.0981  
Max Branch Factor | 0.5745 | 0.2189 | 0.2293 | 0.1355 | 0.3000 | 0.1522 | 0.1857  
Rule Dist Mean | 0.5838 | 0.4368 | 0.3713 | 0.1301 | 0.3000 | 0.1377 | 0.2632  
Rule Dist StdDev | 0.5144 | 0.4474 | 0.3795 | 0.1559 | 0.3500 | 0.1797 | 0.0384  
Rule Dist Skew | 0.5844 | 0.4511 | 0.3779 | 0.1313 | 0.3000 | 0.1522 | 0.1857  
Rule Dist Kurtosis | 0.5044 | 0.1437 | 0.1913 | 0.1726 | 0.4000 | 0.1610 | 0.1383  
Self Consistency Text | 0.5525 | 0.2283 | 0.2419 | 0.1376 | 0.4500 | 0.1545 | 0.1866  
Self Consistency SMT | 0.7364 | 0.3535 | 0.2751 | 0.1031 | 0.2000 | 0.1062 | 0.4408  
Ensemble Average | 0.6140 | 0.3922 | 0.3192 | 0.1240 | 0.1000 | 0.1722 | 0.0936  
Ensemble Weighted | 0.7235 | 0.3327 | 0.2539 | 0.1035 | 0.1000 | 0.1404 | 0.2484  
Ensemble ML | 0.7631 | 0.2897 | 0.2229 | 0.0823 | 0.0500 | 0.1596 | 0.1461  
Ensemble Simple | 0.6476 | 0.3867 | 0.3039 | 0.1071 | 0.2000 | 0.1519 | 0.1871  
  
### C.3 Detailed Performance of SMT-Based Uncertainty Metrics for Text-Answer Prediction

This section evaluates the efficacy of uncertainty quantification (UQ) metrics derived from SMT-LIB generations in predicting the correctness of the SMT results with the corresponding textual answers. The goal is to identify when the formalization (SMT output) aligns or diverges from the model’s natural language reasoning output (textual answer). On StrategyQA, o3 mini had 100% agreement between SMT and text answers, so UQ analysis for SMT-Text consistency prediction was not applicable for that specific model-dataset pair as there were no disagreements to predict. Results for other cases are detailed below.

For DeepSeek R1 on StrategyQA, we assesses how well metrics derived from its SMT generations can predict alignment with its textual answers. The results are strong: ensemble methods integrating these SMT features, such as Ensemble Weighted (AUROC 0.8494) and Ensemble Average (AUROC 0.8183), are highly effective. Notably, Text Self Consistency (AUROC 0.8245) is a top individual performer, suggesting that instability in textual outputs often correlates with SMT-Text divergence. Among metrics purely derived from SMT structure, Grammar Entropy (AUROC 0.7609) is noteworthy, achieving a 100% relative error reduction in identifying SMT-Text disagreements if one abstains on 45% of cases. This performance in predicting SMT-Text consistency is robust and highlights that both SMT structural integrity and textual stability are key indicators. The AURC values are generally very low for top performers (e.g., 0.0155 for Ensemble Weighted), indicating high utility in selectively flagging potential cross-modal disagreements.

Table 6: UQ for SMT-Text Consistency (DeepSeek R1, StrategyQA): SMT-derived metrics, especially ensembles (Ensemble Weighted AUROC 0.8494), effectively predict SMT-Text answer agreement. Text Self Consistency (AUROC 0.8245) is a strong predictor, while SMT-derived Grammar Entropy (AUROC 0.7609) also shows good utility, enabling high error reduction (100% RelErrRed at Opt.T 0.45) in identifying SMT-Text divergences. Metric | AUROC | ECE | Brier | AURC | Opt.T | Err@T | RelErrRed  
---|---|---|---|---|---|---|---  
Grammar Entropy | 0.7609 | 0.4617 | 0.2968 | 0.0216 | 0.4500 | 0.0000 | 1.0000  
Perplexity | 0.6211 | 0.3789 | 0.2640 | 0.0361 | 0.5000 | 0.0204 | 0.7114  
KL Divergence | 0.5776 | 0.4408 | 0.2855 | 0.0443 | 0.3000 | 0.0580 | 0.1801  
NSUI | 0.5963 | 0.2529 | 0.1433 | 0.0462 | 0.1000 | 0.0562 | 0.2055  
Renyi Ent (2) | 0.6242 | 0.3980 | 0.2746 | 0.0378 | 0.5000 | 0.0204 | 0.7114  
Renyi Ent (0.5) | 0.6149 | 0.3942 | 0.2755 | 0.0376 | 0.5000 | 0.0408 | 0.4227  
Max Ent | 0.7174 | 0.3994 | 0.2341 | 0.0262 | 0.0500 | 0.0638 | 0.0973  
Ent Ratio | 0.5217 | 0.5047 | 0.3529 | 0.0543 | 0.3000 | 0.0580 | 0.1801  
Spectral Factor | 0.5481 | 0.1533 | 0.0927 | 0.0640 | 0.1500 | 0.0476 | 0.3265  
Spectral Radius | 0.5481 | 0.2067 | 0.1166 | 0.0640 | 0.1500 | 0.0476 | 0.3265  
# Nonterminals | 0.5264 | 0.5679 | 0.4237 | 0.0557 | 0.5000 | 0.0408 | 0.4227  
# Rules | 0.6087 | 0.3083 | 0.1839 | 0.0396 | 0.4000 | 0.0508 | 0.2809  
Avg Rules / NT | 0.7034 | 0.4068 | 0.2532 | 0.0273 | 0.0500 | 0.0638 | 0.0973  
Avg RHS Len | 0.5637 | 0.2491 | 0.1566 | 0.0544 | 0.1000 | 0.0562 | 0.2055  
Max Branch Factor | 0.6801 | 0.3325 | 0.2042 | 0.0324 | 0.0500 | 0.0638 | 0.0973  
Rule Dist Mean | 0.7034 | 0.5352 | 0.3733 | 0.0273 | 0.0500 | 0.0638 | 0.0973  
Rule Dist StdDev | 0.6056 | 0.6755 | 0.5361 | 0.0413 | 0.2000 | 0.0506 | 0.2839  
Rule Dist Skew | 0.6848 | 0.4800 | 0.3260 | 0.0309 | 0.0500 | 0.0638 | 0.0973  
Rule Dist Kurtosis | 0.5311 | 0.2521 | 0.1588 | 0.0534 | 0.1000 | 0.0674 | 0.0465  
Self Consistency Text | 0.8245 | 0.1002 | 0.0751 | 0.0155 | 0.0500 | 0.0319 | 0.5486  
Self Consistency SMT | 0.7570 | 0.2062 | 0.1373 | 0.0268 | 0.0500 | 0.0532 | 0.2477  
Ensemble Average | 0.8183 | 0.4695 | 0.3058 | 0.0180 | 0.2500 | 0.0135 | 0.8089  
Ensemble Weighted | 0.8494 | 0.3256 | 0.1711 | 0.0155 | 0.0500 | 0.0319 | 0.5486  
Ensemble ML | 0.8245 | 0.3084 | 0.2003 | 0.0170 | 0.2000 | 0.0380 | 0.4629  
Ensemble Simple | 0.6957 | 0.4363 | 0.2748 | 0.0316 | 0.1000 | 0.0562 | 0.2055  
  
When predicting SMT-Text consistency for DeepSeek v3 on StrategyQA, UQ metrics based on SMT generations prove highly effective. The Ensemble ML approach, which learns from various SMT-derived features, achieves an impressive AUROC of 0.8517 and offers a 55.56% relative error reduction in spotting SMT-Text disagreements when abstaining on 25% of samples. Good individual predictors include SMT-derived Grammar Entropy (AUROC 0.7354) and SMT Self Consistency (AUROC 0.7116). This demonstrates that for DeepSeek v3, deviations from typical SMT structure (signaled by grammar entropy) or inconsistencies in the SMT generation process itself are strong indicators that the SMT output might not align with the model’s textual answer. The low AURC (0.0573) for Ensemble ML highlights its practical utility. This task of predicting internal consistency (SMT-Text) shows strong signals, comparable to or even clearer (e.g. for Ensemble ML) than predicting SMT-Ground Truth correctness for this model on the same dataset.

Table 7: UQ for SMT-Text Consistency (DeepSeek v3, StrategyQA): Ensemble ML using SMT-derived features shows excellent performance (AUROC 0.8517) in predicting SMT-Text agreement, with a 55.56% relative error reduction. SMT-derived Grammar Entropy (AUROC 0.7354) and SMT Self Consistency (AUROC 0.7116) also serve as solid individual predictors, indicating that atypical SMT structures and generation instability can flag potential SMT-Text divergences. Metric | AUROC | ECE | Brier | AURC | Opt.T | Err@T | RelErrRed  
---|---|---|---|---|---|---|---  
Grammar Entropy | 0.7354 | 0.3058 | 0.2551 | 0.097 | 0.0500 | 0.1789 | 0.1479  
Perplexity | 0.6721 | 0.3282 | 0.2718 | 0.1205 | 0.3000 | 0.1143 | 0.4558  
KL Divergence | 0.5335 | 0.1195 | 0.178 | 0.1633 | 0.0500 | 0.2000 | 0.0476  
NSUI | 0.5973 | 0.1768 | 0.1919 | 0.1411 | 0.0500 | 0.1895 | 0.0977  
Renyi Ent (2) | 0.6799 | 0.3403 | 0.2808 | 0.116 | 0.3000 | 0.1000 | 0.5238  
Renyi Ent (0.5) | 0.6667 | 0.3333 | 0.2751 | 0.1223 | 0.3500 | 0.1077 | 0.4872  
Max Ent | 0.6353 | 0.1309 | 0.1738 | 0.1247 | 0.1000 | 0.1889 | 0.1005  
Ent Ratio | 0.6154 | 0.4091 | 0.3307 | 0.1446 | 0.5000 | 0.1000 | 0.5238  
Spectral Factor | 0.7034 | 0.1254 | 0.158 | 0.1206 | 0.1000 | 0.1667 | 0.2063  
Spectral Radius | 0.7034 | 0.1896 | 0.1752 | 0.1206 | 0.1000 | 0.1667 | 0.2063  
# Nonterminals | 0.5549 | 0.2271 | 0.2455 | 0.148 | 0.0500 | 0.2000 | 0.0476  
# Rules | 0.5675 | 0.2025 | 0.2077 | 0.1485 | 0.1000 | 0.1778 | 0.1534  
Avg Rules / NT | 0.6034 | 0.1393 | 0.1854 | 0.1399 | 0.0500 | 0.1895 | 0.0977  
Avg RHS Len | 0.5208 | 0.1254 | 0.1818 | 0.1972 | 0.0500 | 0.2000 | 0.0476  
Max Branch Factor | 0.5937 | 0.1563 | 0.192 | 0.1457 | 0.1000 | 0.1889 | 0.1005  
Rule Dist Mean | 0.6034 | 0.321 | 0.2742 | 0.1399 | 0.0500 | 0.1895 | 0.0977  
Rule Dist StdDev | 0.6281 | 0.2226 | 0.2221 | 0.1445 | 0.3000 | 0.1571 | 0.2517  
Rule Dist Skew | 0.5986 | 0.3057 | 0.2619 | 0.1406 | 0.0500 | 0.1895 | 0.0977  
Rule Dist Kurtosis | 0.66 | 0.0731 | 0.1576 | 0.1256 | 0.0500 | 0.1895 | 0.0977  
Self Consistency Text | 0.5778 | 0.1874 | 0.2008 | 0.1754 | 0.1500 | 0.1765 | 0.1597  
Self Consistency SMT | 0.7116 | 0.1662 | 0.1909 | 0.1054 | 0.1000 | 0.1778 | 0.1534  
Ensemble Average | 0.7064 | 0.1876 | 0.1831 | 0.0983 | 0.1000 | 0.1667 | 0.2063  
Ensemble Weighted | 0.7709 | 0.234 | 0.1971 | 0.0798 | 0.0500 | 0.1895 | 0.0977  
Ensemble ML | 0.8517 | 0.1861 | 0.1703 | 0.0573 | 0.2500 | 0.0933 | 0.5556  
Ensemble Simple | 0.6727 | 0.3021 | 0.2567 | 0.1119 | 0.1500 | 0.1765 | 0.1597  
  
For Gemini Flash 2.0 Lite on StrategyQA, the task of predicting SMT-Text consistency reveals a standout individual metric: Rule Distribution Kurtosis from the SMT generations achieves a very high AUROC of 0.8695. This is a particularly interesting finding, as it suggests that the "tailedness" or outlier presence in the distribution of PCFG rules used during SMT generation is a very strong signal of whether the SMT output will align with the textual answer for this model. This metric’s performance surpasses many other individual PCFG metrics (e.g., Grammar Entropy AUROC 0.6622, Perplexity AUROC 0.7212). Ensemble methods, like Ensemble Weighted (AUROC 0.8070) and Ensemble Average (AUROC 0.7927), provide robust overall performance, leveraging combinations of signals. The strong performance of kurtosis aligns with the our discussion about “syntactic fingerprints" and how atypical SMT patterns (like bimodal distributions captured by kurtosis) can signal reasoning issues or misalignments. The AURC for Kurtosis (0.4448) suggests that while discriminative, its practical utility in terms of risk reduction might require careful thresholding, achieving a 30.56% error reduction at a 50% abstention rate.

Table 8: UQ for SMT-Text Consistency (Gemini Flash 2.0 Lite, StrategyQA): Rule Distribution Kurtosis (AUROC 0.8695) from SMT generations is an exceptionally strong individual predictor of SMT-Text agreement, significantly outperforming other PCFG metrics. Ensemble methods (e.g., Ensemble Weighted AUROC 0.8070) also perform well. This highlights a specific SMT structural feature as a key indicator of cross-modal alignment for this model. Metric | AUROC | ECE | Brier | AURC | Opt.T | Err@T | RelErrRed  
---|---|---|---|---|---|---|---  
Grammar Entropy | 0.6622 | 0.1277 | 0.2095 | 0.5689 | 0.1000 | 0.6889 | 0.0432  
Perplexity | 0.7212 | 0.3255 | 0.2849 | 0.5273 | 0.0500 | 0.7053 | 0.0205  
KL Divergence | 0.5486 | 0.2387 | 0.263 | 0.6341 | 0.1000 | 0.7000 | 0.0278  
NSUI | 0.6741 | 0.1195 | 0.1624 | 0.5221 | 0.5000 | 0.6600 | 0.0833  
Renyi Ent (2) | 0.7624 | 0.3192 | 0.2624 | 0.5037 | 0.1000 | 0.6889 | 0.0432  
Renyi Ent (0.5) | 0.6994 | 0.2766 | 0.2619 | 0.5438 | 0.0500 | 0.7053 | 0.0205  
Max Ent | 0.5982 | 0.3401 | 0.3083 | 0.59 | 0.3000 | 0.6714 | 0.0675  
Ent Ratio | 0.5511 | 0.1641 | 0.2511 | 0.6346 | 0.2500 | 0.6667 | 0.0741  
Spectral Factor | 0.6538 | 0.0943 | 0.1677 | 0.5316 | 0.5000 | 0.6600 | 0.0833  
Spectral Radius | 0.6538 | 0.1648 | 0.1703 | 0.5316 | 0.5000 | 0.6600 | 0.0833  
# Nonterminals | 0.5166 | 0.418 | 0.3958 | 0.6509 | 0.3500 | 0.6769 | 0.0598  
# Rules | 0.5749 | 0.4256 | 0.3818 | 0.6252 | 0.1000 | 0.6889 | 0.0432  
Avg Rules / NT | 0.6565 | 0.2913 | 0.2761 | 0.5923 | 0.2500 | 0.6400 | 0.1111  
Avg RHS Len | 0.6014 | 0.4855 | 0.442 | 0.6098 | 0.0500 | 0.7053 | 0.0205  
Max Branch Factor | 0.5818 | 0.5167 | 0.4747 | 0.6313 | 0.0500 | 0.7053 | 0.0205  
Rule Dist Mean | 0.6565 | 0.2197 | 0.228 | 0.5923 | 0.2500 | 0.6400 | 0.1111  
Rule Dist StdDev | 0.7183 | 0.3136 | 0.2807 | 0.5455 | 0.1500 | 0.6706 | 0.0686  
Rule Dist Skew | 0.6796 | 0.1783 | 0.2199 | 0.572 | 0.2500 | 0.6400 | 0.1111  
Rule Dist Kurtosis | 0.8695 | 0.3187 | 0.2412 | 0.4448 | 0.5000 | 0.5000 | 0.3056  
Self Consistency Text | 0.535 | 0.2788 | 0.2616 | 0.6064 | 0.3500 | 0.6462 | 0.1026  
Self Consistency SMT | 0.7505 | 0.538 | 0.4357 | 0.4822 | 0.5000 | 0.5600 | 0.2222  
Ensemble Average | 0.7927 | 0.1531 | 0.1702 | 0.4848 | 0.4000 | 0.5833 | 0.1898  
Ensemble Weighted | 0.807 | 0.1673 | 0.1632 | 0.4718 | 0.3000 | 0.6143 | 0.1468  
Ensemble ML | 0.7946 | 0.1308 | 0.1592 | 0.4784 | 0.5000 | 0.5400 | 0.2500  
Ensemble Simple | 0.7584 | 0.0796 | 0.1568 | 0.4929 | 0.1500 | 0.6824 | 0.0523  
  
The results for o3-mini on ProofWriter for predicting SMT-Text consistency are exceptional. Ensemble ML and Ensemble Weighted methods achieve perfect AUROC scores of 1.0000, signifying an ability to flawlessly distinguish SMT outputs that align with textual answers from those that diverge. This allows for a 100% relative error reduction with a very low 5% abstention rate. Beyond ensembles, many individual PCFG metrics derived from the SMT generations show extremely high predictive capabilities. For instance, Ent Ratio (AUROC 0.9677), Rule Dist Kurtosis (AUROC 0.9462), Max Ent (AUROC 0.9355), and NSUI (AUROC 0.9355) are all remarkably strong predictors, each achieving 100% relative error reduction at their respective optimal thresholds. This indicates that for o3-mini, particularly on a formal reasoning task like ProofWriter, the structural and probabilistic characteristics of its SMT generations are almost perfectly indicative of whether its formal and textual reasoning pathways are aligned. The exceptionally low AURC values (e.g., 0.0003 for Ensemble ML) further emphasize the practical certainty offered by these UQ measures in this context. This level of predictability for SMT-Text consistency is even more pronounced than some of the SMT-Ground Truth prediction results for this model, demonstrating the power of SMT features for diagnosing internal reasoning coherence.

Table 9: UQ for SMT-Text Consistency (o3-mini, ProofWriter): SMT-derived UQ metrics demonstrate outstanding performance, with Ensemble ML and Ensemble Weighted achieving perfect AUROC (1.0000) in predicting SMT-Text agreement. Numerous individual PCFG metrics, such as Ent Ratio (AUROC 0.9677) and Rule Dist Kurtosis (AUROC 0.9462), are also exceptionally effective, enabling complete identification of SMT-Text inconsistencies with minimal abstention. This underscores a very strong link between SMT formalization properties and cross-modal reasoning alignment for o3-mini on this formal task. Metric | AUROC | ECE | Brier | AURC | Opt.T | Err@T | RelErrRed  
---|---|---|---|---|---|---|---  
Grammar Entropy | 0.8602 | 0.4419 | 0.2542 | 0.0013 | 0.15 | 0.00 | 1.00  
Perplexity | 0.9032 | 0.4429 | 0.2616 | 0.0013 | 0.10 | 0.00 | 1.00  
KL Divergence | 0.6667 | 0.5167 | 0.3238 | 0.0039 | 0.35 | 0.00 | 1.00  
NSUI | 0.9355 | 0.4077 | 0.2172 | 0.0008 | 0.10 | 0.00 | 1.00  
Renyi Ent (2) | 0.9032 | 0.4382 | 0.2580 | 0.0013 | 0.10 | 0.00 | 1.00  
Renyi Ent (0.5) | 0.8925 | 0.5063 | 0.3246 | 0.0013 | 0.15 | 0.00 | 1.00  
Max Ent | 0.9355 | 0.2589 | 0.1029 | 0.0008 | 0.10 | 0.00 | 1.00  
Ent Ratio | 0.9677 | 0.4074 | 0.2082 | 0.0003 | 0.05 | 0.00 | 1.00  
Spectral Factor | 0.5269 | 0.6329 | 0.5061 | 0.0084 | 0.00 | 0.01 | 0.00  
Spectral Radius | 0.5269 | 0.6243 | 0.4953 | 0.0084 | 0.00 | 0.01 | 0.00  
# Nonterminals | 0.6505 | 0.5520 | 0.3650 | 0.0047 | 0.40 | 0.00 | 1.00  
# Rules | 0.5108 | 0.4186 | 0.2201 | 0.0064 | 0.50 | 0.00 | 1.00  
Avg Rules / NT | 0.8011 | 0.4394 | 0.2554 | 0.0026 | 0.25 | 0.00 | 1.00  
Avg RHS Len | 0.5054 | 0.6535 | 0.5116 | 0.0074 | 0.50 | 0.00 | 1.00  
Max Branch Factor | 0.7419 | 0.6809 | 0.5100 | 0.0032 | 0.30 | 0.00 | 1.00  
Rule Dist Mean | 0.8011 | 0.4842 | 0.2971 | 0.0026 | 0.25 | 0.00 | 1.00  
Rule Dist StdDev | 0.8710 | 0.4232 | 0.2392 | 0.0013 | 0.15 | 0.00 | 1.00  
Rule Dist Skew | 0.8172 | 0.4864 | 0.2964 | 0.0019 | 0.20 | 0.00 | 1.00  
Rule Dist Kurtosis | 0.9462 | 0.5107 | 0.3056 | 0.0008 | 0.10 | 0.00 | 1.00  
Self Consistency Text | 0.7050 | 0.9352 | 0.9023 | 0.0030 | 0.30 | 0.00 | 1.00  
Self Consistency SMT | 0.7100 | 0.8600 | 0.7863 | 0.0030 | 0.30 | 0.00 | 1.00  
Ensemble Average | 0.9300 | 0.3560 | 0.1741 | 0.0007 | 0.10 | 0.00 | 1.00  
Ensemble Weighted | 1.0000 | 0.4231 | 0.2375 | 0.0003 | 0.05 | 0.00 | 1.00  
Ensemble ML | 1.0000 | 0.0496 | 0.0199 | 0.0003 | 0.05 | 0.00 | 1.00  
Ensemble Simple | 0.6667 | 0.4419 | 0.2661 | 0.0039 | 0.35 | 0.00 | 1.00  
  
## Appendix D Supplementary Experimental Details

The comprehensive PCFG analysis underpinning our uncertainty quantification was conducted on a focused set of benchmarks. Specifically, for 100100 questions each from the StrategyQA, ProofWriter, and ProntoQA datasets, a corpus of NS​M​T=100N_{SMT}=100 SMT-LIB v2 program samples per question was generated. The FOLIO dataset was excluded from this detailed PCFG study due to challenges in obtaining consistently robust SMT formalizations from the evaluated LLMs. Each SMT program within these corpora was parsed using an ANTLR-based parser to extract its constituent production rules. For the generation of these primary SMT samples used in uncertainty quantification (distinct from the temperature ablation study), LLM sampling temperature was maintained at its default setting to promote more deterministic outputs, with up to 1010 generation attempts per SMT sample to ensure corpus completeness.

For each of the selected questions, a unique PCFG was induced from its corresponding 100100 SMT samples. Rule probabilities within these per-question PCFGs were estimated via Maximum Likelihood Estimation (MLE), incorporating Lidstone smoothing (specifically, Laplace smoothing with βs=1\beta_{s}=1) to manage unseen production rules. Beyond the metrics detailed in the main methodology, specific configurations included the computation of Rényi entropy for orders α=0.5\alpha=0.5 and α=2.0\alpha=2.0 (Collision Entropy).

The evaluation framework for the derived uncertainty metrics incorporated specific settings. Expected Calibration Error (ECE) was calculated using 1010 discretization bins for confidence scores. In the analysis of selective prediction utility (error vs. abstention), optimal abstention thresholds were determined by targeting maximum relative error reduction while considering abstention levels up to a practical maximum of 50%. For our Ensemble ML predictor, a Logistic Regression model was employed, configured with balanced class weights and trained for up to 10,00010,000 iterations on scaled features derived from the suite of PCFG uncertainty metrics.

## Appendix E SMT Error Ratios vs Text Error Ratios

Figure 14: SMT vs. Text Error Ratio Analysis for o3-mini: Illustrates well-calibrated SMT generation, indicated by a strong correlation between SMT and Text error patterns.

Figure 15: SMT vs. Text Error Ratio Analysis for Gemini Flash 2.0: Depicts less-calibrated SMT generation, evidenced by a weaker correlation between SMT and Text error patterns.

The figures juxtapose SMT versus Text error ratios (with marginals) for o3-mini (Fig. 15) and Gemini Flash 2.0 (Fig. 15); the Text error ratio is defined as the proportion of incorrect direct textual answers from the LLM per question out of the many samples, while the SMT error ratio is the proportion of incorrect answers derived from its SMT-LIB formalizations. O3-mini exhibits a notable correlation between its SMT and Text error distributions, characteristic of a well-calibrated SMT generation process where formalization errors tend to align with textual reasoning errors. In contrast, Gemini Flash 2.0 shows a weaker correlation, suggesting its SMT generations may introduce errors or exhibit patterns less consistently coupled with its textual output, indicative of poorer calibration. This comparative error ratio analysis is valuable for assessing the fidelity of an LLM’s autoformalization. Strong SMT-Text error correlation implies that the SMT modality can be a more reliable indicator of the LLM’s general reasoning tendencies for a problem, making SMT-derived uncertainty metrics potentially more transferable. Poor correlation, however, signals a divergence between textual reasoning and formalization, cautioning against using SMT outputs as direct proxies without careful consideration of modality-specific error sources and motivating efforts towards better SMT-Text reasoning alignment.

## Appendix F Qualitative Analysis

Beyond quantitative uncertainty metrics, the PCFG framework, by its nature of parsing and structuring program ensembles, lends itself to a nuanced qualitative analysis of LLM-generated formal artifacts. Initial explorations can focus on broad characteristics such as the distribution of SMT-LIB sorts (datatypes) employed or the prevalent logical fragments (e.g., ‘QF_LIA‘, ‘QF_AUFBV‘) selected by the LLM for a given problem class. However, a more profound understanding of an LLM’s formalization strategy emerges from a detailed examination of substrctures, like the assert statements, which constitute the semantic core of an SMT program by stipulating the conditions and axioms for the solver. Our PCFG-based analysis of these assertions, and the logical architectures therein, reveals critical patterns in how LLMs attempt to translate natural language problem specifications into rigorous, machine-interpretable logic.

When an LLM generates multiple SMT program samples for a single natural language input, the per-problem induced PCFG captures a distribution over grammatical structures. This distribution inherently models the LLM’s normative formalization pathways alongside its idiosyncratic variations, particularly in the construction of assert statements and their nested logical terms—including quantifiers (forall, exists), logical connectives (=>, and, or, not), and predicate applications. Analyzing the probabilities and diversity of production rules within these PCFGs allows for the identification and interpretation of several key types of divergences and tendencies in formal specification:

#### Formalization Aliasing and Representational Stability

A core aspect of a problem specification may elicit syntactically diverse, yet ideally logically equivalent, assert statements across an ensemble of LLM generations. For instance, an implication A⇒BA\Rightarrow B might be directly asserted or rendered as ¬A∨B\neg A\lor B. The PCFG reflects such syntactic polymorphism through multiple, lower-probability rule sequences mapping to the same underlying semantic constraint. A high degree of such variability for asserting fundamental problem axioms often signals the LLM’s lack of a converged or canonical formalization strategy, potentially indicating uncertainty or representational underspecification for that particular logical construct.

#### Variance in Logical Decomposition and Structural Complexity

The PCFG rule sets unveil the LLM’s implicit preferences regarding the structural complexity and granularity of asserted logical terms. For a given problem, some SMT samples might employ deeply nested quantifiers and connectives within a monolithic assert statement. In contrast, other samples might exhibit a preference for flatter, more direct assertions or decompose a complex axiom into several simpler, conjoined assert statements. This divergence in logical decomposition strategies is captured by differing rule probabilities and derivation depths within the PCFG, pointing to variations in the LLM’s approach to abstraction and information chunking during the formalization process.

#### Identification of Atypical or Anomalous Assertions

Occasionally, an LLM may generate assert statements possessing highly unusual or infrequent syntactic structures relative to the typical formalizations observed for a given problem context or across a dataset. The PCFG methodology inherently highlights these as low-probability production rules or derivations. Qualitative inspection of the SMT code corresponding to these rare assertion patterns can uncover unique, potentially innovative, or conversely, flawed and overly convoluted ways the LLM attempts to axiomatize specific constraints, offering insights into its error modes or its capacity for novel formal expression.

#### Semantic Divergence in Axiomatization

More critically, divergences can be semantic rather than merely syntactic, leading to logically distinct problem formalizations from the same natural language input. Such semantic drift often manifests as significantly different asserted terms within assert statements, pointing to LLM misinterpretation, unresolved ambiguity, or flaws in its inferential reasoning. For example, if an input "All engineers use LaTeX" is ambiguously formalized, one SMT sample might correctly assert (forall ((x Engineer)) (usesLaTeX x)), while a semantically divergent sample might erroneously assert (forall ((x User)) (implies (usesLaTeX x) (isEngineer x))). The PCFG rules governing the predicates, variables, and logical structure of terms within these assertions would markedly differ, directly reflecting this semantic incongruity and providing a diagnostic trace.

#### Fidelity in Representing Ground Facts

For declarative factual statements present in the input (e.g., "Constantine is a logician"), the LLM is expected to consistently assert the corresponding ground fact in a stable manner. If the PCFG reveals multiple, conflicting, or unstable rule applications for asserting properties of specific entities (e.g., some derivations asserting ‘(isLogician constantine)‘ while others, for the same conceptual input fact, generate ‘(isPhilosopher constantine)‘ or vary the predicate structure), this indicates a deficiency in the LLM’s fidelity in extracting and consistently formalizing elementary factual information, pointing to potential grounding issues.

Program 1 |  Program 2 |  Program 3 |  Program 4  
---|---|---|---  
(set-logic QF_LIA)   
(declare-const relation_count_G Int)   
(declare-const relation_count_J Int)   
(assert (> relation_count_G relation_count_J))   
(assert (>= relation_count_G 1))   
(assert (>= relation_count_J 0))   
(check-sat)   
(get-model) |  (set-logic QF_LIA)   
(declare-const GC Int)   
(declare-const JC Int)   
(assert (> GC 0))   
(assert (> JC 0))   
(assert (> GC JC))   
(assert (>= GC 10))   
(assert (>= JC 1))   
(check-sat)   
(get-model) |  (set-logic QF_LIA)   
(declare-fun people_genghis () Int)   
(declare-fun people_caesar () Int)   
(assert (>= people_genghis 0))   
(assert (>= people_caesar 0))   
(assert (> people_genghis people_caesar))   
(assert (>= people_genghis 1000000))   
(assert (<= people_caesar 500000))   
(check-sat)   
(get-model) |  (set-logic QF_LIA)   
(declare-const KN Int)   
(declare-const CA Int)   
(assert (> KN CA))   
(assert (= KN 16))   
(assert (= CA 1))   
(check-sat)   
(get-model)  
Table 10: Divergent LLM Formalizations of a StrategyQA Problem: Sample SMT-LIB outputs illustrating varied axiomatization strategies, with assert statements highlighted (blue). Such variations are central to the qualitative PCFG analysis discussed.

Experimental support, please [view the build logs](./2505.20047v1/__stdout.txt) for errors. Generated by [ L A T E xml ](https://math.nist.gov/~BMiller/LaTeXML/). 

## Instructions for reporting errors

We are continuing to improve HTML versions of papers, and your feedback helps enhance accessibility and mobile support. To report errors in the HTML that will help us improve conversion and rendering, choose any of the methods listed below:

  * Click the "Report Issue" ( ) button, located in the page header.



**Tip:** You can select the relevant text first, to include it in your report.

Our team has already identified [the following issues](https://github.com/arXiv/html_feedback/issues). We appreciate your time reviewing and reporting rendering errors we may not have found yet. Your efforts will help us improve the HTML versions for all readers, because disability should not be a barrier to accessing research. Thank you for your continued support in championing open access for all.

Have a free development cycle? Help support accessibility at arXiv! Our collaborators at LaTeXML maintain a [list of packages that need conversion](https://github.com/brucemiller/LaTeXML/wiki/Porting-LaTeX-packages-for-LaTeXML), and welcome [developer contributions](https://github.com/brucemiller/LaTeXML/issues).

We gratefully acknowledge support from our **major funders** , [**member institutions**](https://info.arxiv.org/about/ourmembers.html) , ****, and all contributors.

[About](https://info.arxiv.org/about) * [Help](https://info.arxiv.org/help) * [Contact](https://info.arxiv.org/help/contact.html) * [Subscribe](https://info.arxiv.org/help/subscribe) * [Copyright](https://info.arxiv.org/help/license/index.html) * [Privacy](https://info.arxiv.org/help/policies/privacy_policy.html) * [Accessibility](https://info.arxiv.org/help/web_accessibility.html) * [Operational Status (opens in new tab)](https://status.arxiv.org)

Major funding support from

[ ](https://www.simonsfoundation.org/) [ ](https://www.sfi.org.bm/) [ ](https://www.schmidtsciences.org/)

[ ](javascript:toggleReadingMode\(\); "Disable reading mode, show header and footer")


 signals of underlying semantic errors. Our evaluations revealed nuanced LLM behaviors—task-dependent uncertainty responses, localized PCFG entropy’s diagnostic power, and asymmetric self-consistency suggesting distinct, imperfectly aligned formal versus textual reasoning pathways. Building on these discoveries, we introduced a novel uncertainty taxonomy and a lightweight, model-agnostic signal fusion technique that improves metric synergy and calibration. Applied together, this PCFG framework and fusion strategy achieve substantial error rate reductions via selective verification, offering an empirically validated methodology to significantly enhance LLM reliability in formal verification workflows.

## References

  * Huth and Ryan (2004) Michael Huth and Mark Ryan.  _Logic in Computer Science: Modelling and reasoning about systems_.  Cambridge university press, 2004. 
  * Clarke et al. (2018) Edmund M Clarke, Thomas A Henzinger, Helmut Veith, Roderick Bloem, et al.  _Handbook of model checking_ , volume 10.  Springer, 2018. 
  * Woodcock et al. (2009) Jim Woodcock, Peter Gorm Larsen, Juan Bicarregui, and John Fitzgerald.  Formal methods: Practice and experience.  _ACM computing surveys (CSUR)_ , 41(4):1–36, 2009. 
  * Brown et al. (2020) Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al.  Language models are few-shot learners.  _Advances in neural information processing systems_ , 33:1877–1901, 2020. 
  * Chen et al. (2021) Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde De Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al.  Evaluating large language models trained on code.  _arXiv preprint arXiv:2107.03374_ , 2021. 
  * Jiang et al. (2023a) Albert Q. Jiang, Alexandre Sablayrolles, Arthur Mensch, Chris Bamford, Devendra Singh Chaplot, Diego de las Casas, Florian Bressand, Gianna Lengyel, Guillaume Lample, Lucile Saulnier, Lélio Renard Lavaud, Marie-Anne Lachaux, Pierre Stock, Teven Le Scao, Thibaut Lavril, Thomas Wang, Timothée Lacroix, and William El Sayed.  Mistral 7b, 2023a.  URL <https://arxiv.org/abs/2310.06825>. 
  * Hou et al. (2023) Bairu Hou, Yujian Liu, Kaizhi Qian, Jacob Andreas, Shiyu Chang, and Yang Zhang.  Decomposing uncertainty for large language models through input clarification ensembling.  _arXiv preprint arXiv:2311.08718_ , 2023. 
  * Ganguly et al. (2024) Debargha Ganguly, Srinivasan Iyengar, Vipin Chaudhary, and Shivkumar Kalyanaraman.  PROOF OF THOUGHT : Neurosymbolic program synthesis allows robust and interpretable reasoning.  In _The First Workshop on System-2 Reasoning at Scale, NeurIPS’24_ , 2024.  URL <https://openreview.net/forum?id=Pxx3r14j3U>. 
  * Pan et al. (2023) Liangming Pan, Alon Albalak, Xinyi Wang, and William Yang Wang.  Logic-LM: Empowering Large Language Models with Symbolic Solvers for Faithful Logical Reasoning.  In _Findings of the Association for Computational Linguistics: EMNLP_ , 2023. 
  * Wei et al. (2022a) Jason Wei, Yi Tay, Rishi Bommasani, Colin Raffel, Barret Zoph, Sebastian Borgeaud, Dani Yogatama, Maarten Bosma, Denny Zhou, Donald Metzler, et al.  Emergent abilities of large language models.  _arXiv preprint arXiv:2206.07682_ , 2022a. 
  * Chen et al. (2022) Wenhu Chen, Xueguang Ma, Xinyi Wang, and William W Cohen.  Program of thoughts prompting: Disentangling computation from reasoning for numerical reasoning tasks.  _arXiv preprint arXiv:2211.12588_ , 2022. 
  * Kadavath et al. (2022) Saurav Kadavath, Tom Conerly, Amanda Askell, Tom Henighan, Dawn Drain, Ethan Perez, Nicholas Schiefer, Zac Hatfield-Dodds, Nova DasSarma, Eli Tran-Johnson, et al.  Language models (mostly) know what they know.  _arXiv preprint arXiv:2207.05221_ , 2022. 
  * Wang et al. (2022) Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou.  Self-consistency improves chain of thought reasoning in language models.  _arXiv preprint arXiv:2203.11171_ , 2022. 
  * Wei et al. (2022b) Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Fei Xia, Ed Chi, Quoc V Le, Denny Zhou, et al.  Chain-of-thought prompting elicits reasoning in large language models.  _Advances in neural information processing systems_ , 35:24824–24837, 2022b. 
  * Geva et al. (2021) Mor Geva, Daniel Khashabi, Elad Segal, Tushar Khot, Dan Roth, and Jonathan Berant.  Did aristotle use a laptop? a question answering benchmark with implicit reasoning strategies.  _Transactions of the Association for Computational Linguistics_ , 9:346–361, 2021.  doi: 10.1162/tacl_a_00370.  URL <https://aclanthology.org/2021.tacl-1.21/>. 
  * Saparov and He (2023) Abulhair Saparov and He He.  Language models are greedy reasoners: A systematic formal analysis of chain-of-thought.  In _The Eleventh International Conference on Learning Representations_ , 2023.  URL <https://openreview.net/forum?id=qFVVBzXxR2V>. 
  * Tafjord et al. (2021) Oyvind Tafjord, Bhavana Dalvi Mishra, and Peter Clark.  ProofWriter: Generating Implications, Proofs, and Abductive Statements over Natural Language.  In _Findings of the Association for Computational Linguistics: ACL-IJCNLP_ , 2021. 
  * Han et al. (2024) Simeng Han, Hailey Schoelkopf, Yilun Zhao, Zhenting Qi, Martin Riddell, Wenfei Zhou, James Coady, David Peng, Yujie Qiao, Luke Benson, Lucy Sun, Alexander Wardle-Solano, Hannah Szabó, Ekaterina Zubova, Matthew Burtell, Jonathan Fan, Yixin Liu, Brian Wong, Malcolm Sailor, Ansong Ni, Linyong Nan, Jungo Kasai, Tao Yu, Rui Zhang, Alexander Fabbri, Wojciech Maciej Kryscinski, Semih Yavuz, Ye Liu, Xi Victoria Lin, Shafiq Joty, Yingbo Zhou, Caiming Xiong, Rex Ying, Arman Cohan, and Dragomir Radev.  FOLIO: Natural language reasoning with first-order logic.  In Yaser Al-Onaizan, Mohit Bansal, and Yun-Nung Chen, editors, _Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing_ , pages 22017–22031, Miami, Florida, USA, November 2024. Association for Computational Linguistics.  doi: 10.18653/v1/2024.emnlp-main.1229.  URL <https://aclanthology.org/2024.emnlp-main.1229/>. 
  * Ganguly et al. (2025) Debargha Ganguly, Warren Richard Morningstar, Andrew Seohwan Yu, and Vipin Chaudhary.  Forte : Finding outliers with representation typicality estimation.  In _The Thirteenth International Conference on Learning Representations_ , 2025.  URL <https://openreview.net/forum?id=7XNgVPxCiA>. 
  * Welleck et al. (2022a) Sean Welleck, Jiacheng Liu, Ximing Lu, Hannaneh Hajishirzi, and Yejin Choi.  Naturalprover: Grounded mathematical proof generation with language models.  _Advances in Neural Information Processing Systems_ , 35:4913–4927, 2022a. 
  * Lin et al. (2022a) Stephanie Lin, Jacob Hilton, and Owain Evans.  Teaching models to express their uncertainty in words.  _arXiv preprint arXiv:2205.14334_ , 2022a. 
  * Wang et al. (2018) Qingxiang Wang, Cezary Kaliszyk, and Josef Urban.  First Experiments with Neural Translation of Informal to Formal Mathematics.  In _Proceedings of the International Conference on Intelligent Computer Mathematics_ , 2018. 
  * Wang et al. (2020) Qingxiang Wang, Chad Brown, Cezary Kaliszyk, and Josef Urban.  Exploration of Neural Machine Translation in Autoformalization of Mathematics in Mizar.  In _Proceedings of the ACM SIGPLAN International Conference on Certified Programs and Proofs_ , 2020. 
  * Wu et al. (2022) Yuhuai Wu, Albert Q Jiang, Wenda Li, Markus Rabe, Charles Staats, Mateja Jamnik, and Christian Szegedy.  Autoformalization with Large Language Models.  In _Proceedings of the International Conference on Neural Information Processing Systems_ , 2022. 
  * Agrawal et al. (2022) Ayush Agrawal, Siddhartha Gadgil, Navin Goyal, Ashvni Narayanan, and Anand Tadipatri.  Towards a Mathematics Formalisation Assistant using Large Language Models.  _arXiv preprint arXiv:2211.07524_ , 2022. 
  * Gadgil et al. (2022) Siddhartha Gadgil, Anand Rao Tadipatri, Ayush Agrawal, Ashvni Narayanan, and Navin Goyal.  Towards Automating Formalisation of Theorem Statements using Large Language Models.  In _International Conference on Neural Information Processing Systems Workshop on MATH-AI_ , 2022. 
  * Murphy et al. (2024) Logan Murphy, Kaiyu Yang, Jialiang Sun, Zhaoyu Li, Anima Anandkumar, and Xujie Si.  Autoformalizing Euclidean Geometry.  In _Proceedings of the International Conference on Machine Learning_ , 2024. 
  * Jiang et al. (2023b) Albert Q Jiang, Sean Welleck, Jin Peng Zhou, Wenda Li, Jiacheng Liu, Mateja Jamnik, Timothée Lacroix, Yuhuai Wu, and Guillaume Lample.  Draft, Sketch, and Prove: Guiding Formal Theorem Provers with Informal Proofs.  In _Proceedings of the International Conference on Learning Representations_ , 2023b. 
  * Zhao et al. (2024) Xueliang Zhao, Wenda Li, and Lingpeng Kong.  Subgoal-Based Demonstration Learning for Formal Theorem Proving.  In _Proceedings of the International Conference on Machine Learning_ , 2024. 
  * Liu et al. (2023) Chengwu Liu, Jianhao Shen, Huajian Xin, Zhengying Liu, Ye Yuan, Haiming Wang, Wei Ju, Chuanyang Zheng, Yichun Yin, Lin Li, et al.  FIMO: A Challenge Formal Dataset for Automated Theorem Proving.  _arXiv preprint arXiv:2309.04295_ , 2023. 
  * Olausson et al. (2023) Theo X Olausson, Alex Gu, Benjamin Lipkin, Cedegao E Zhang, Armando Solar-Lezama, Joshua B Tenenbaum, and Roger Levy.  LINC: A Neurosymbolic Approach for Logical Reasoning by Combining Language Models with First-Order Logic Provers.  In _Proceedings of the Conference on Empirical Methods in Natural Language Processing_ , 2023. 
  * Ye et al. (2023) Xi Ye, Qiaochu Chen, Isil Dillig, and Greg Durrett.  SATLM: Satisfiability-Aided Language Models using Declarative Prompting.  In _Proceedings of the International Conference on Neural Information Processing Systems_ , 2023. 
  * Zhou et al. (2024) Jin Peng Zhou, Charles E Staats, Wenda Li, Christian Szegedy, Kilian Q Weinberger, and Yuhuai Wu.  Don’t Trust: Verify–Grounding LLM Quantitative Reasoning with Autoformalization.  In _Proceedings of the International Conference on Learning Representations_ , 2024. 
  * Huang et al. (2024a) Yinya Huang, Xiaohan Lin, Zhengying Liu, Qingxing Cao, Huajian Xin, Haiming Wang, Zhenguo Li, Linqi Song, and Xiaodan Liang.  MUSTARD: Mastering Uniform Synthesis of Theorem and Proof Data.  In _Proceedings of the International Conference on Learning Representations_ , 2024a. 
  * Xin et al. (2024a) Huajian Xin, Haiming Wang, Chuanyang Zheng, Lin Li, Zhengying Liu, Qingxing Cao, Yinya Huang, Jing Xiong, Han Shi, Enze Xie, et al.  LEGO-Prover: Neural Theorem Proving with Growing Libraries.  In _Proceedings of the International Conference on Learning Representations_ , 2024a. 
  * Jiang et al. (2024) Dongwei Jiang, Marcio Fonseca, and Shay B Cohen.  LeanReasoner: Boosting Complex Logical Reasoning with Lean.  In _Proceedings of the Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies_ , 2024. 
  * Quan et al. (2024) Xin Quan, Marco Valentino, Louise A Dennis, and André Freitas.  Verification and Refinement of Natural Language Explanations through LLM-Symbolic Theorem Proving.  _arXiv preprint arXiv:2405.01379_ , 2024. 
  * Xin et al. (2024b) Huajian Xin, Daya Guo, Zhihong Shao, Zhizhou Ren, Qihao Zhu, Bo Liu, Chong Ruan, Wenda Li, and Xiaodan Liang.  DeepSeek-Prover: Advancing Theorem Proving in LLMs through Large-Scale Synthetic Data.  _arXiv preprint arXiv:2405.14333_ , 2024b. 
  * Whalen (2016) Daniel Whalen.  Holophrasm: A Neural Automated Theorem Prover for Higher-Order Logic.  _arXiv preprint arXiv:1608.02644_ , 2016. 
  * Huang et al. (2019) Daniel Huang, Prafulla Dhariwal, Dawn Song, and Ilya Sutskever.  GamePad: A Learning Environment for Theorem Proving.  In _Proceedings of the International Conference on Learning Representations_ , 2019. 
  * Bansal et al. (2019) Kshitij Bansal, Sarah M. Loos, Markus Norman Rabe, Christian Szegedy, and Stewart Wilcox.  HOList: An Environment for Machine Learning of Higher Order Logic Theorem Proving.  In _Proceedings of the International Conference on Machine Learning_ , 2019. 
  * Polu and Sutskever (2020) Stanislas Polu and Ilya Sutskever.  Generative Language Modeling for Automated Theorem Proving.  _arXiv preprint arXiv:2009.03393_ , 2020. 
  * First et al. (2023) Emily First, Markus Rabe, Talia Ringer, and Yuriy Brun.  Baldur: Whole-Proof Generation and Repair with Large Language Models.  In _Proceedings of the ACM Joint European Software Engineering Conference and Symposium on the Foundations of Software Engineering_ , 2023. 
  * Wang et al. (2024) Haiming Wang, Huajian Xin, Zhengying Liu, Wenda Li, Yinya Huang, Jianqiao Lu, Zhicheng Yang, Jing Tang, Jian Yin, Zhenguo Li, et al.  Proving Theorems Recursively.  _arXiv preprint arXiv:2405.14414_ , 2024. 
  * Welleck et al. (2022b) Sean Welleck, Jiacheng Liu, Ximing Lu, Hannaneh Hajishirzi, and Yejin Choi.  NaturalProver: Grounded Mathematical Proof Generation with Language Models.  In _Proceedings of the International Conference on Neural Information Processing Systems_ , 2022b. 
  * Jiang et al. (2022) Albert Q Jiang, Wenda Li, Szymon Tworkowski, Konrad Czechowski, Tomasz Odrzygóźdź, Piotr Miłoś, Yuhuai Wu, and Mateja Jamnik.  Thor: Wielding Hammers to Integrate Language Models and Automated Theorem Provers.  In _Proceedings of the International Conference on Neural Information Processing Systems_ , 2022. 
  * Zhang et al. (2023) Shizhuo Dylan Zhang, Talia Ringer, and Emily First.  Getting More out of Large Language Models for Proofs.  In _Proceedings of the Conference on Artificial Intelligence and Theorem Proving_ , 2023. 
  * Yousefzadeh and Cao (2023) Roozbeh Yousefzadeh and Xuenan Cao.  Large Language Models’ Understanding of Math: Source Criticism and Extrapolation.  _arXiv preprint arXiv:2311.07618_ , 2023. 
  * Scheidt (2023) Gregor vom Scheidt.  Experimental Results from Applying GPT-4 to An Unpublished Formal Language.  _arXiv preprint arXiv:2305.12196_ , 2023. 
  * Frieder et al. (2023a) Simon Frieder, Julius Berner, Philipp Petersen, and Thomas Lukasiewicz.  Large Language Models for Mathematicians.  _arXiv preprint arXiv:2312.04556_ , 2023a. 
  * Frieder et al. (2023b) Simon Frieder, Luca Pinchetti, Alexis Chevalier, Ryan-Rhys Griffiths, Tommaso Salvatori, Thomas Lukasiewicz, Philipp Christian Petersen, and Julius Berner.  Mathematical Capabilities of ChatGPT.  In _Proceedings of the International Conference on Neural Information Processing Systems Datasets and Benchmarks Track_ , 2023b. 
  * Frieder et al. (2023c) Simon Frieder, Martin Trimmel, Rashid Alawadhi, and Klaus Gy.  LLM vs ITP.  In _International Conference on Neural Information Processing Systems Workshop on MATH-AI_ , 2023c. 
  * Zhang et al. (2024a) Lichen Zhang, Shuai Lu, and Nan Duan.  Selene: Pioneering Automated Proof in Software Verification.  In _Proceedings of the Annual Meeting of the Association for Computational Linguistics_ , 2024a. 
  * Zheng et al. (2024) Chuanyang Zheng, Haiming Wang, Enze Xie, Zhengying Liu, Jiankai Sun, Huajian Xin, Jianhao Shen, Zhenguo Li, and Yu Li.  Lyra: Orchestrating Dual Correction in Automated Theorem Proving.  _Transactions on Machine Learning Research_ , 2024. 
  * Thakur et al. (2024) Amitayush Thakur, George Tsoukalas, Yeming Wen, Jimmy Xin, and Swarat Chaudhuri.  An In-Context Learning Agent for Formal Theorem-Proving.  _arXiv preprint arXiv:2310.04353_ , 2024. 
  * Loos et al. (2017) Sarah Loos, Geoffrey Irving, Christian Szegedy, and Cezary Kaliszyk.  Deep Network Guided Proof Search.  In _Proceedings of the International Conference on Logic for Programming, Artificial Intelligence and Reasoning_ , 2017. 
  * Chvalovskỳ et al. (2019) Karel Chvalovskỳ, Jan Jakubüv, Martin Suda, and Josef Urban.  ENIGMA-NG: Efficient Neural and Gradient-Boosted Inference Guidance for E.  In _Proceedings of the International Conference on Automated Deduction_ , 2019. 
  * Kusumoto et al. (2018) Mitsuru Kusumoto, Keisuke Yahata, and Masahiro Sakai.  Automated Theorem Proving in Intuitionistic Propositional Logic by Deep Reinforcement Learning.  _arXiv preprint arXiv:1811.00796_ , 2018. 
  * Crouse et al. (2021) Maxwell Crouse, Ibrahim Abdelaziz, Bassem Makni, Spencer Whitehead, Cristina Cornelio, Pavan Kapanipathi, Kavitha Srinivas, Veronika Thost, Michael Witbrock, and Achille Fokoue.  A Deep Reinforcement Learning Approach to First-Order Logic Theorem Proving.  In _Proceedings of the AAAI Conference on Artificial Intelligence_ , 2021. 
  * Piepenbrock et al. (2021) Jelle Piepenbrock, Tom Heskes, Mikoláš Janota, and Josef Urban.  Learning Equational Theorem Proving.  In _Proceedings of the Conference on Artificial Intelligence and Theorem Proving_ , 2021. 
  * Wu et al. (2021) Minchao Wu, Michael Norrish, Christian Walder, and Amir Dezfouli.  TacticZero: Learning to Prove Theorems from Scratch with Deep Reinforcement Learning.  _Proceedings of the International Conference on Neural Information Processing Systems_ , 2021. 
  * Lample et al. (2022) Guillaume Lample, Timothee Lacroix, Marie-Anne Lachaux, Aurelien Rodriguez, Amaury Hayat, Thibaut Lavril, Gabriel Ebner, and Xavier Martinet.  Hypertree Proof Search for Neural Theorem Proving.  In _Proceedings of the International Conference on Neural Information Processing Systems_ , 2022. 
  * Wang et al. (2023a) Haiming Wang, Ye Yuan, Zhengying Liu, Jianhao Shen, Yichun Yin, Jing Xiong, Enze Xie, Han Shi, Yujun Li, Lin Li, et al.  DT-Solver: Automated Theorem Proving with Dynamic-Tree Sampling Guided by Proof-level Value Function.  In _Proceedings of the Annual Meeting of the Association for Computational Linguistics_ , 2023a. 
  * An et al. (2024) Chenyang An, Zhibo Chen, Qihao Ye, Emily First, Letian Peng, Jiayun Zhang, Zihan Wang, Sorin Lerner, and Jingbo Shang.  Learn from Failure: Fine-Tuning LLMs with Trial-and-Error Data for Intuitionistic Propositional Logic Proving.  _arXiv preprint arXiv:2404.07382_ , 2024. 
  * Kuhn et al. (2023) Lorenz Kuhn, Yarin Gal, and Sebastian Farquhar.  Semantic uncertainty: Linguistic invariances for uncertainty estimation in natural language generation.  _arXiv preprint arXiv:2302.09664_ , 2023. 
  * Duan et al. (2024) Jinhao Duan, Renming Zhang, James Diffenderfer, Bhavya Kailkhura, Lichao Sun, Elias Stengel-Eskin, Mohit Bansal, Tianlong Chen, and Kaidi Xu.  Gtbench: Uncovering the strategic reasoning limitations of llms via game-theoretic evaluations.  _arXiv preprint arXiv:2402.12348_ , 2024. 
  * Mora-Cross and Calderon-Ramirez (2024) Maria Mora-Cross and Saul Calderon-Ramirez.  Uncertainty estimation in large language models to support biodiversity conservation.  In _Proceedings of the 2024 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 6: Industry Track)_ , pages 368–378, 2024. 
  * Margatina et al. (2023) Katerina Margatina, Timo Schick, Nikolaos Aletras, and Jane Dwivedi-Yu.  Active learning principles for in-context learning with large language models, 2023.  URL <https://arxiv.org/abs/2305.14264>. 
  * Malinin (2019) Andrey Malinin.  _Uncertainty estimation in deep learning with application to spoken language assessment_.  PhD thesis, University of Cambridge, 2019. 
  * Wimmer et al. (2023) Lisa Wimmer, Yusuf Sale, Paul Hofman, Bernd Bischl, and Eyke Hüllermeier.  Quantifying aleatoric and epistemic uncertainty in machine learning: Are conditional entropy and mutual information appropriate measures?  In Robin J. Evans and Ilya Shpitser, editors, _Proceedings of the Thirty-Ninth Conference on Uncertainty in Artificial Intelligence_ , volume 216 of _Proceedings of Machine Learning Research_ , pages 2282–2292. PMLR, 31 Jul–04 Aug 2023.  URL <https://proceedings.mlr.press/v216/wimmer23a.html>. 
  * Depeweg (2019) Stefan Depeweg.  Modeling epistemic and aleatoric uncertainty with bayesian neural networks and latent variables.  2019\.  URL <https://api.semanticscholar.org/CorpusID:208224498>. 
  * Ash (1965) Robert B Ash.  _Information theory_.  Dover Publications, 1965. 
  * Srivastava et al. (2014) Nitish Srivastava, Geoffrey Hinton, Alex Krizhevsky, Ilya Sutskever, and Ruslan Salakhutdinov.  Dropout: a simple way to prevent neural networks from overfitting.  _The journal of machine learning research_ , 15(1):1929–1958, 2014. 
  * Gal and Ghahramani (2016a) Yarin Gal and Zoubin Ghahramani.  Dropout as a bayesian approximation: Representing model uncertainty in deep learning.  In Maria Florina Balcan and Kilian Q. Weinberger, editors, _Proceedings of The 33rd International Conference on Machine Learning_ , volume 48 of _Proceedings of Machine Learning Research_ , pages 1050–1059, New York, New York, USA, 20–22 Jun 2016a. PMLR.  URL <https://proceedings.mlr.press/v48/gal16.html>. 
  * Lakshminarayanan et al. (2017) Balaji Lakshminarayanan, Alexander Pritzel, and Charles Blundell.  Simple and scalable predictive uncertainty estimation using deep ensembles.  _Advances in neural information processing systems_ , 30, 2017. 
  * Fadeeva et al. (2023) Ekaterina Fadeeva, Roman Vashurin, Akim Tsvigun, Artem Vazhentsev, Sergey Petrakov, Kirill Fedyanin, Daniil Vasilev, Elizaveta Goncharova, Alexander Panchenko, Maxim Panov, et al.  Lm-polygraph: Uncertainty estimation for language models.  _arXiv preprint arXiv:2311.07383_ , 2023. 
  * Gal and Ghahramani (2016b) Yarin Gal and Zoubin Ghahramani.  Dropout as a bayesian approximation: Representing model uncertainty in deep learning.  In _international conference on machine learning_ , pages 1050–1059. PMLR, 2016b. 
  * Wen et al. (2020) Yeming Wen, Dustin Tran, and Jimmy Ba.  Batchensemble: An alternative approach to efficient ensemble and lifelong learning, 2020.  URL <https://arxiv.org/abs/2002.06715>. 
  * Arteaga et al. (2024) Gabriel Y. Arteaga, Thomas B. Schön, and Nicolas Pielawski.  Hallucination detection in llms: Fast and memory-efficient finetuned models, 2024.  URL <https://arxiv.org/abs/2409.02976>. 
  * Wang et al. (2023b) Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou.  Self-consistency improves chain of thought reasoning in language models, 2023b.  URL <https://arxiv.org/abs/2203.11171>. 
  * Cole et al. (2023) Jeremy R. Cole, Michael J. Q. Zhang, Daniel Gillick, Julian Martin Eisenschlos, Bhuwan Dhingra, and Jacob Eisenstein.  Selectively answering ambiguous questions, 2023.  URL <https://arxiv.org/abs/2305.14613>. 
  * Huang et al. (2024b) Hsiu-Yuan Huang, Zichen Wu, Yutong Yang, Junzhao Zhang, and Yunfang Wu.  Unc-ttp: A method for classifying llm uncertainty to improve in-context example selection, 2024b.  URL <https://arxiv.org/abs/2408.09172>. 
  * Zhang et al. (2024b) Jiaxin Zhang, Zhuohang Li, Kamalika Das, Bradley A. Malin, and Sricharan Kumar.  Sac3: Reliable hallucination detection in black-box language models via semantic-aware cross-check consistency, 2024b.  URL <https://arxiv.org/abs/2311.01740>. 
  * Gawlikowski et al. (2023) Jakob Gawlikowski, Cedrique Rovile Njieutcheu Tassi, Mohsin Ali, Jongseok Lee, Matthias Humt, Jianxiang Feng, Anna Kruspe, Rudolph Triebel, Peter Jung, Ribana Roscher, et al.  A survey of uncertainty in deep neural networks.  _Artificial Intelligence Review_ , 56(Suppl 1):1513–1589, 2023. 
  * Manakul et al. (2023) Potsawee Manakul, Adian Liusie, and Mark J. F. Gales.  Selfcheckgpt: Zero-resource black-box hallucination detection for generative large language models, 2023.  URL <https://arxiv.org/abs/2303.08896>. 
  * Chen and Mueller (2024) Jiuhai Chen and Jonas Mueller.  Quantifying uncertainty in answers from any language model and enhancing their trustworthiness.  In Lun-Wei Ku, Andre Martins, and Vivek Srikumar, editors, _Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pages 5186–5200, Bangkok, Thailand, August 2024. Association for Computational Linguistics.  URL <https://aclanthology.org/2024.acl-long.283>. 
  * Lin et al. (2024) Zhen Lin, Shubhendu Trivedi, and Jimeng Sun.  Generating with confidence: Uncertainty quantification for black-box large language models, 2024.  URL <https://arxiv.org/abs/2305.19187>. 
  * Shridhar et al. (2019) Kumar Shridhar, Felix Laumann, and Marcus Liwicki.  A comprehensive guide to bayesian convolutional neural network with variational inference, 2019.  URL <https://arxiv.org/abs/1901.02731>. 
  * Blundell et al. (2015) Charles Blundell, Julien Cornebise, Koray Kavukcuoglu, and Daan Wierstra.  Weight uncertainty in neural network.  In _International conference on machine learning_ , pages 1613–1622. PMLR, 2015. 
  * Graves (2011) Alex Graves.  Practical variational inference for neural networks.  _Advances in neural information processing systems_ , 24, 2011. 
  * Jordan et al. (1999) Michael I Jordan, Zoubin Ghahramani, Tommi S Jaakkola, and Lawrence K Saul.  An introduction to variational methods for graphical models.  _Machine learning_ , 37:183–233, 1999. 
  * Kullback and Leibler (1951) S. Kullback and R. A. Leibler.  On information and sufficiency.  _The Annals of Mathematical Statistics_ , 22(1):79–86, 1951.  ISSN 00034851.  URL <http://www.jstor.org/stable/2236703>. 
  * Iwata and Ghahramani (2017) Tomoharu Iwata and Zoubin Ghahramani.  Improving output uncertainty estimation and generalization in deep learning via neural network gaussian processes, 2017.  URL <https://arxiv.org/abs/1707.05922>. 
  * Liu et al. (2020) Jeremiah Zhe Liu, Zi Lin, Shreyas Padhy, Dustin Tran, Tania Bedrax-Weiss, and Balaji Lakshminarayanan.  Simple and principled uncertainty estimation with deterministic deep learning via distance awareness, 2020.  URL <https://arxiv.org/abs/2006.10108>. 
  * Xiao and Wang (2018) Yijun Xiao and William Yang Wang.  Quantifying uncertainties in natural language processing tasks, 2018.  URL <https://arxiv.org/abs/1811.07253>. 
  * Cosmides and Tooby (1996) Leda Cosmides and John Tooby.  Are humans good intuitive statisticians after all? rethinking some conclusions from the literature on judgment under uncertainty.  _cognition_ , 58(1):1–73, 1996. 
  * Lin et al. (2022b) Stephanie Lin, Jacob Hilton, and Owain Evans.  Teaching models to express their uncertainty in words, 2022b.  URL <https://arxiv.org/abs/2205.14334>. 
  * Tian et al. (2023) Katherine Tian, Eric Mitchell, Allan Zhou, Archit Sharma, Rafael Rafailov, Huaxiu Yao, Chelsea Finn, and Christopher D. Manning.  Just ask for calibration: Strategies for eliciting calibrated confidence scores from language models fine-tuned with human feedback, 2023.  URL <https://arxiv.org/abs/2305.14975>. 
  * Xiong et al. (2024) Miao Xiong, Zhiyuan Hu, Xinyang Lu, Yifei Li, Jie Fu, Junxian He, and Bryan Hooi.  Can llms express their uncertainty? an empirical evaluation of confidence elicitation in llms, 2024.  URL <https://arxiv.org/abs/2306.13063>. 
  * Kojima et al. (2022) Takeshi Kojima, Shixiang (Shane) Gu, Machel Reid, Yutaka Matsuo, and Yusuke Iwasawa.  Large language models are zero-shot reasoners.  In S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh, editors, _Advances in Neural Information Processing Systems_ , volume 35, pages 22199–22213. Curran Associates, Inc., 2022.  URL <https://proceedings.neurips.cc/paper_files/paper/2022/file/8bb0d291acd4acf06ef112099c16f326-Paper-Conference.pdf>. 
  * Groot and Valdenegro-Toro (2024) Tobias Groot and Matias Valdenegro-Toro.  Overconfidence is key: Verbalized uncertainty evaluation in large language and vision-language models, 2024.  URL <https://arxiv.org/abs/2405.02917>. 
  * Lee et al. (2020) Dennis Lee, Christian Szegedy, Markus N Rabe, Sarah M Loos, and Kshitij Bansal.  Mathematical Reasoning in Latent Space.  In _Proceedings of the International Conference on Learning Representations_ , 2020. 
  * Wu and Wu (2021) Minchao Wu and Yuhuai Wu.  Latent Action Space for Efficient Planning in Theorem Proving.  In _Proceedings of the Conference on Artificial Intelligence and Theorem Proving_ , 2021. 
  * Manning and Schutze (1999) Christopher Manning and Hinrich Schutze.  _Foundations of statistical natural language processing_.  MIT press, 1999. 
  * Durbin et al. (1998) Richard Durbin, Sean R Eddy, Anders Krogh, and Graeme Mitchison.  _Biological sequence analysis: probabilistic models of proteins and nucleic acids_.  Cambridge university press, 1998. 
  * Alur et al. (2014) Rajeev Alur, Milo Martin, Mukund Raghothaman, Christos Stergiou, Stavros Tripakis, and Abhishek Udupa.  Synthesizing finite-state protocols from scenarios and requirements.  In _Hardware and Software: Verification and Testing: 10th International Haifa Verification Conference, HVC 2014, Haifa, Israel, November 18-20, 2014. Proceedings 10_ , pages 75–91. Springer, 2014. 
  * Barke et al. (2024) Shraddha Barke, Emmanuel Anaya Gonzalez, Saketh Ram Kasibatla, Taylor Berg-Kirkpatrick, and Nadia Polikarpova.  Hysynth: Context-free llm approximation for guiding program synthesis.  _Advances in Neural Information Processing Systems_ , 37:15612–15645, 2024. 
  * De la Higuera (2010) Colin De la Higuera.  _Grammatical inference: learning automata and grammars_.  Cambridge University Press, 2010. 



## Appendix A Appendix: Proofs

### A.1 Coverage Guarantees

Theorem 1 : Coverage Guarantees

###### Proof.

Step 1: Construct a “high-probability” set. By definition of Shannon entropy in bits, there can be at most 2H⁡(μ)2^{H(\mu)} points x∈Σ∗x\in\Sigma^{*} each having probability μ⁡(x)≥2−H⁡(μ)\mu(x)\geq 2^{-H(\mu)}. Gather all such points into a set

| Shigh={x∈Σ∗:μ⁡(x)≥ 2−H⁡(μ)}.S_{\text{high}}\;=\;\\{\,x\in\Sigma^{*}:\mu(x)\,\geq\,2^{-H(\mu)}\\}. |   
---|---|---  
  
A standard “typical-set” argument shows that μ⁡(Shigh)≥1/2\mu(S_{\text{high}})\geq 1/2 (or at least a fixed positive constant).

Step 2: Missing ShighS_{\text{high}}. The probability that one sample X∼μX\sim\mu does _not_ land in ShighS_{\text{high}} is at most 1−μ⁡(Shigh)≤1/21-\mu(S_{\text{high}})\leq 1/2. Hence the probability that _none_ of NN i.i.d. draws land in ShighS_{\text{high}} is at most (1/2)N=2−N(1/2)^{N}=2^{-N}. Thus any set of measure at least 1/21/2 is missed with exponentially small probability.

Step 3: Missing a smaller-mass region AA. If μ⁡(A)=ϵ≤1/2\mu(A)=\epsilon\leq 1/2, the probability that one draw misses AA is 1−ϵ1-\epsilon, so the probability _all_ NN draws miss AA is (1−ϵ)N≈exp⁡(−N​ϵ)(1-\epsilon)^{N}\approx\exp(-N\,\epsilon) if N​ϵN\epsilon is not too large.

However, we need a _uniform_ guarantee over _all_ possible AA of measure ϵ\epsilon. By representing Σ∗\Sigma^{*} as composed of at most 2H⁡(μ)2^{H(\mu)} “atoms” each of probability at least 2−H⁡(μ)2^{-H(\mu)}, the number of distinct subsets is at most exp⁡(2H⁡(μ)​ln⁡2)\exp\bigl(2^{H(\mu)}\ln 2\bigr). A union bound then modifies the exponent by about a factor of 1/2H⁡(μ)1/2^{H(\mu)}, so for large NN one has

| Pr[∃A:μ(A)=ϵandall N samples miss A]≤exp(−N​ϵ2H⁡(μ)).\Pr\bigl[\exists\,A:\mu(A)=\epsilon\;\text{and}\;\text{all $N$ samples miss $A$}\bigr]\;\leq\;\exp\\!\Bigl(-\,\tfrac{N\,\epsilon}{2^{H(\mu)}}\Bigr). |   
---|---|---  
  
This is the desired exponential coverage bound.

Step 4: Inverting the bound with the Lambert WW-function. We have

| Pr⁡[miss some set of mass ​ϵ]≤exp⁡(−N​ϵ2H⁡(μ)).\Pr\Bigl[\text{miss some set of mass }\epsilon\Bigr]\;\leq\;\exp\\!\Bigl(-\,\tfrac{N\,\epsilon}{2^{H(\mu)}}\Bigr). |   
---|---|---  
  
We want to find ϵ\epsilon such that this probability is itself at most ϵ\epsilon:

| exp⁡(−N​ϵ2H⁡(μ))=ϵ.\exp\\!\Bigl(-\,\tfrac{N\,\epsilon}{2^{H(\mu)}}\Bigr)\;=\;\epsilon. |   
---|---|---  
  
Rearrange as

| ϵ=exp(−N​ϵ2H⁡(μ))⟺ϵexp(N​ϵ2H⁡(μ))= 1.\epsilon\;=\;\exp\\!\Bigl(-\tfrac{N\,\epsilon}{2^{H(\mu)}}\Bigr)\quad\Longleftrightarrow\quad\epsilon\,\exp\\!\Bigl(\tfrac{N\,\epsilon}{2^{H(\mu)}}\Bigr)\;=\;1. |   
---|---|---  
  
Let x=N​ϵ2H⁡(μ)x=\tfrac{N\,\epsilon}{2^{H(\mu)}}. Then ϵ=2H⁡(μ)N​x\epsilon=\tfrac{2^{H(\mu)}}{N}x, and the above becomes

| 2H⁡(μ)Nxexp(x)= 1⟺xex=N2H⁡(μ).\frac{2^{H(\mu)}}{N}\;x\;\exp(x)\;=\;1\quad\Longleftrightarrow\quad x\,e^{x}\;=\;\frac{N}{2^{H(\mu)}}. |   
---|---|---  
  
By definition of the Lambert WW-function, x=W⁡(N2H⁡(μ))x=W\\!\Bigl(\tfrac{N}{2^{H(\mu)}}\Bigr). Substituting back, we get

| ϵ=2H⁡(μ)N​W​(N2H⁡(μ)).\epsilon\;=\;\frac{2^{H(\mu)}}{N}\;W\\!\Bigl(\tfrac{N}{2^{H(\mu)}}\Bigr). |   
---|---|---  
  
Thus ϵ\epsilon decreases to 00 as N→∞N\to\infty, roughly like

2H⁡(μ)N​ln⁡(N2H⁡(μ)).\frac{2^{H(\mu)}}{N}\,\ln\bigl(\tfrac{N}{2^{H(\mu)}}\bigr).

Hence, the probability of missing _any_ set of mass at least ϵ\epsilon is ≤ϵ\leq\epsilon, with ϵ\epsilon scaling on the order of ln⁡(N)N\tfrac{\ln(N)}{N}. This completes the proof. ∎

### A.2 Temperature Sampling & Ablations

Sampling from an LLM at higher temperatures effectively “flattens” its probability distribution over next-token choices, increasing the entropy of the samples and thus encouraging exploration of lower-probability (more diverse) regions of the program space. Conversely, sampling at lower temperatures sharpens the distribution, concentrating probability mass on the model’s highest-confidence predictions and yielding lower-entropy (more conservative) samples. In other words, low-temperature sampling focuses on the most likely, canonical SMT-LIB programs (small effective support), while high-temperature sampling ventures into rarer, more varied corners of the output space (large effective support). If instead of a smoothly varying temperature schedule you simply draw many samples at fixed temperatures—say 0.5, 1.0, 1.5, and 2.0—you will still span low- to high-entropy regimes, but less systematically. You risk oversampling similar outputs at each temperature (especially near the extremes) and undersampling the intermediate entropy levels that lie between 0.5->1.0 and 1.5->2.0. A continuous schedule allocates exactly one sample per intermediate temperature, guaranteeing uniform coverage of entropy levels; fixed-temperature repetition may require substantially more draws to approximate that coverage, potentially leaving gaps in the distribution of generated programs.

###### Definition 1 (Gaussian Temperature Schedule).

To smoothly explore the distribution over SMT-LIB programs, we can define a temperature schedule for NN samples as:

| τi=τmin+(τmax−τmin)⋅exp⁡(−(i−N/2)22​σ2)\tau_{i}=\tau_{\min}+(\tau_{\max}-\tau_{\min})\cdot\exp\left(-\frac{(i-N/2)^{2}}{2\sigma^{2}}\right) |  | (1)  
---|---|---|---  
  
where τmin=0.1\tau_{\min}=0.1, τmax=1.5\tau_{\max}=1.5, and σ=N5\sigma=\frac{N}{5} controls the spread of the Gaussian.

We can also skew this gaussian towards lower temperatures.

###### Definition 2 (Exponential Temperature Schedule).

We can define a schedule that emphasizes sampling at lower temperatures using:

| τi=τmin+(τmax−τmin)⋅exp(−λ⋅i)\tau_{i}=\tau_{\min}+(\tau_{\max}-\tau_{\min})\cdot\exp\left(-\lambda\cdot i\right) |  | (2)  
---|---|---|---  
  
where λ>0\lambda>0 controls the decay rate, and i=0,1,…,N−1i=0,1,\dots,N-1.

Comparison: From a purely coverage-guarantee standpoint (i.e. our goal of hitting every “significant" region of the SMT-LIB output distribution at least once), the Systematic uniform schedule remains the most theoretically justified. It uniformly samples every temperature exactly once, from low to high. Provably minimizes the worst-case “miss probability” by evenly covering the full entropy range. Gaussians concentrates samples near the middle temperature; fewer at extremes. It does provide smooth transitions; and avoids extreme high-entropy noise. However undersamples both very low-entropy (conservative) and very high-entropy (creative) regions resulting in weaker uniform coverage. The exponential decay schedule heavily biases toward low temperatures (low entropy), and therefore quickly focuses on high-confidence outputs. However, there is almost no exploration of rare programs; poor coverage of tail regions.

## Appendix B Temperature-Varied SMT Generation and PCFG Analysis

To empirically investigate the influence of LLM sampling temperature on the characteristics of generated formal artifacts, we performed SMT-LIB v2 program generation across a defined temperature spectrum (e.g., Tm​i​n=0.0T_{min}=0.0 to Tm​a​x=2.0T_{max}=2.0). Distinct Probabilistic Context-Free Grammars (PCFGs) were induced from the SMT program ensembles parsed at each temperature point TiT_{i}, modeling the LLM’s syntactic and structural tendencies under each generative condition.

Our analysis of these per-temperature PCFGs revealed distinct and significant trends as sampling temperature was varied. Notably, the PCFG spectral radius generally trended upwards with increasing temperature. This intriguing behavior suggests that higher temperatures, while fostering diversity, may also enable the LLM to access and generate SMT structures with more pronounced or varied recursive complexity, perhaps by activating a broader range of complex production rules rather than simplifying structural choices. Consistent with expectations of increased diversity, grammar entropy and its associated perplexity also demonstrated an upward trend, quantifying the heightened uncertainty and the expanded set of effective choices exercised by the LLM at higher temperatures.

Figure 2: Spectral Radius VS Temperature

Figure 3: Grammar Entropy VS Temperature

Figure 4: KLD vs Temp

Figure 5: Entropy Ratio vs Temp

A particularly interesting observation was that the KL divergence from a uniform distribution also tended to increase with temperature. This implies that as the LLM explores a wider variety of production rules (evidenced by increased entropy), its choices within this expanded repertoire become, in a relative sense, more specific or structured, deviating further from a purely random uniform selection over the increasingly diverse set of utilized rules. Correspondingly, the entropy ratio generally decreased, which could occur if the maximum possible entropy (based on the growing set of observed rules and non-terminals at higher temperatures) increases at a faster rate than the actual grammar entropy. The composite metric NSUI showed fluctuating behavior without a clear monotonic direction, reflecting the complex interplay of its underlying components. The spectral factor, linked to the spectral radius, also exhibited a slight upward trend.

Figure 6: NSUI vs Temp

Figure 7: Spectral Factor vs Temp

Figure 8: Perplexity vs Temp

Figure 9: Average Rules per Non-terminal vs Temp

Metrics related to the observed grammar structure, such as the average number of rules utilized per non-terminal, the maximum observed branching factor, and the average right-hand side (RHS) length of applied rules, all generally increased with temperature. This supports the notion that higher temperatures lead the LLM to explore and employ a more extensive and potentially more elaborate subset of the SMT-LIB grammar. Regarding the shape of the rule probability distributions, kurtosis consistently decreased, indicating that these distributions become flatter (less peaked) as temperature promotes more uniform rule selection among the actively used rules. Conversely, the skew of these distributions tended to increase, suggesting a shift in the asymmetry of rule preferences as temperature changes.

Figure 10: Max Branching Factor vs Temp

Figure 11: Average RHS Length vs Temp

Figure 12: Kurtosis vs Temp

Figure 13: Skew vs Temp

These ablation studies are meaningful as they reveal a nuanced picture of the LLM’s generative process for formal languages. The trends suggest that increasing temperature doesn’t merely lead to random, uniform outputs, but rather allows the LLM to explore a richer, potentially more complex, and structurally diverse portion of the language space defined by GS​M​TG_{SMT}. This expansion, however, may also come with its own emergent structural specificities, as indicated by the KL divergence. These findings are crucial for understanding the coherence-diversity trade-off, for validating the sensitivity of PCFG-derived metrics, and for interpreting uncertainty scores, as the baseline characteristics of generated artifacts are systematically altered by temperature in complex ways. The observed responses underscore the value of empirical studies in characterizing LLM behavior for formal code generation.

## Appendix C Detailed Results

### C.1 Benchmarking Autoformalization

The performance benchmarks detailed in C.1, C.1, C.1, C.1, C.1 were generated by evaluating five Large Language Models (o3-mini, DeepSeekR1 with Chain-of-Thought, DeepSeek-v3-04-21, Gemini Flash 2.0, and Gemini Flash 2.0 Lite) on four reasoning datasets. For each question, five samples were generated, and answers were derived either directly from the LLM’s textual output or by solving LLM-generated SMT-LIB programs using the Z3 solver. The “medium effort" designation for o3-mini indicates a specific prompting or iteration level for that model. In Table C.1, the SMT approach for models like Deepseek v3 not only altered precision and recall but also resulted in substantial numbers of both False Positives (144) and True Positives (199), suggesting that while it attempted more proofs, a large fraction of these new attempts were erroneous. This contrasts with its text performance (42 FP, 174 TP). For the ProntoQA training set, with only true answers (Table C.1), the SMT Precision of 1.0000 across all models is a direct consequence of the experimental design (no false statements to misclassify as true if TN is inherently 0); the variance in False Negatives (e.g., 270 for Deepseek v3 SMT) thus purely reflects the inability to successfully formalize and prove statements known to be true, a direct measure of formalization completeness for affirmatives.

[!htb] LLM Performance on StrategyQA (Text vs. SMT): SMT often boosts recall (e.g., Deepseek v3 from 0.81 to 0.91) but can reduce precision and overall accuracy for several models, highlighting model-dependent autoformalization success on knowledge-intensive tasks. StrategyQA Text SMT Accuracy Precision Recall F1 TP TN FP FN Accuracy Precision Recall F1 TP TN FP FN o3-mini (medium effort) 0.7828 0.8609 0.6047 0.7104 130 260 21 80 0.7980 0.8688 0.6347 0.7335 139 260 21 80 Deepseek v3 0324 0.8292 0.8055 0.8055 0.8055 174 234 42 42 0.6720 0.5801 0.9086 0.7081 199 137 144 20 DeepSeek R1 0.8580 0.8364 0.8402 0.8383 184 245 36 35 0.7760 0.7184 0.8037 0.7586 176 212 69 43 Gemini Flash 2.0 0.7188 0.6880 0.6570 0.6720 144 214 65 75 0.5360 0.4840 0.9269 0.6363 203 65 216 16 Gemini Flash 2.0 Lite 0.6760 0.6770 0.4970 0.5736 109 229 52 110 0.4500 0.4419 0.9726 0.6077 213 12 269 6

[!htb] LLM Performance on ProntoQA Train (True Statements Only; Text vs. SMT): SMT exposes significant failures in formalizing and proving known true statements for models like Deepseek v3 (Accuracy 0.45 vs. Text 1.00), indicating critical autoformalization recall deficiencies rather than precision issues (SMT Precision remains 1.00 for all). ProntoQA Train - ONLY TRUE Answers Text SMT Accuracy Precision Recall F1 TP TN FP FN Accuracy Precision Recall F1 TP TN FP FN o3-mini (medium effort) 1.0000 1.0000 1.0000 1.0000 499 0 0 0 0.9980 1.0000 0.9980 0.9889 499 0 0 1 Deepseek v3 0324 1.0000 1.0000 1.0000 1.0000 450 0 0 0 0.4501 1.0000 0.4501 0.6200 221 0 0 270 DeepSeek R1 0.9939 1.0000 0.9939 0.9969 489 0 0 3 0.7440 1.0000 0.7440 0.8532 372 0 0 128 Gemini Flash 2.0 0.9820 1.0000 0.9820 0.9900 491 0 0 9 0.9000 1.0000 0.9000 0.9470 450 0 0 50 Gemini Flash 2.0 Lite 0.9980 1.0000 0.9980 0.9980 499 0 0 1 0.9980 1.0000 0.9980 0.9989 499 0 0 1

The ProofWriter results Table C.1 are notable. We advise the reader to ignore DeepSeek R1’s SMT performance, since it is based on a “Partial Run," because of poor model ability to autoformalize, due to the overuse of thinking tokens, thereby causing an intractable timeline for converging to any solution and API call explosion. Here, o3-mini (medium effort) showcases a successful SMT application, where its accuracy improved to 0.9418 with a reduction in both False Positives (from 34 to 19) and False Negatives (from 21 to 10) compared to its text output. On the FOLIO dataset (Table C.1), a common pattern observed in the SMT condition, beyond just low precision, was the significant reduction in True Negatives compared to the Text condition for several models (e.g., Deepseek v3 dropped from 34 TN via Text to 5 TN via SMT; Gemini Flash 2.0 from 37 TN to 0 TN). This suggests a systemic challenge in generating SMT formulas that correctly evaluate to unsatisfiable for statements that are indeed false within the FOLIO logical structure. Finally, the ProntoQA test set which includes both true and false statements (Table C.1) revealed extreme model-specific behaviors under SMT. DeepSeek R1’s SMT output, for instance, correctly identified all 242 false statements (0 FP, 242 TN) but failed to correctly identify any of the 258 true statements (0 TP, 258 FN), indicating a systematic bias in its SMT generation towards unsatisfiability or an inability to complete proofs for satisfiable formulas in a mixed-distribution context, a stark contrast to its perfect text performance and its SMT performance on true-only statements.

[!htb] LLM Performance on ProofWriter (Text vs. SMT): SMT substantially improves models struggling with formal logic (e.g., Gemini Flash 2.0 Lite accuracy from 0.41 to 0.75), yet can degrade performance for models already strong in textual formal reasoning (e.g., DeepSeek R1 accuracy from 0.94 to 0.49), showcasing task-specific SMT utility. ProofWriter Text SMT Accuracy Precision Recall F1 TP TN FP FN Accuracy Precision Recall F1 TP TN FP FN o3-mini (medium effort) 0.8893 0.8697 0.9153 0.8919 227 215 34 21 0.9418 0.9261 0.9597 0.9426 238 231 19 10 Deepseek v3 0324 0.8057 0.8016 0.8225 0.8110 190 175 47 41 0.5800 0.6587 0.3320 0.4414 83 207 43 167 DeepSeek R1 (Partial Run) 0.9423 0.9597 0.9220 0.9400 143 151 6 12 0.4935 0.4750 0.1870 0.2685 29 125 32 126 Gemini Flash 2.0 0.4900 0.4960 0.5710 0.5300 140 106 142 105 0.6660 0.6844 0.6160 0.5313 154 106 71 96 Gemini Flash 2.0 Lite 0.4060 0.3609 0.2440 0.2911 61 142 108 189 0.7540 0.7275 0.8120 0.7674 203 174 76 47

[!htb] LLM Performance on FOLIO (Text vs. SMT): Textual reasoning largely outperforms SMT. For many models, SMT results in high recall but poor precision (e.g., Gemini Flash 2.0 SMT F1 0.72 vs Text 0.92) and a failure to identify false statements (e.g., 0 SMT True Negatives for Gemini Flash 2.0), indicating issues with formalizing negation or complex FOL conditions. Folio Text SMT Accuracy Precision Recall F1 TP TN FP FN Accuracy Precision Recall F1 TP TN FP FN o3-mini (medium effort) 0.9450 0.9682 0.9384 0.9531 61 43 2 4 0.5000 0.6890 0.2985 0.4166 20 36 9 47 Deepseek v3 0324 0.9333 0.9259 0.9615 0.9433 50 34 4 2 0.5961 0.6063 0.9193 0.7307 57 5 37 5 DeepSeek R1 0.9252 0.9670 0.9090 0.9374 60 39 2 6 0.5200 0.6363 0.5303 0.5785 35 21 20 31 Gemini Flash 2.0 0.9010 0.9275 0.9142 0.9200 64 37 5 6 0.5625 0.6000 0.9000 0.7200 63 0 42 7 Gemini Flash 2.0-lite 0.9017 0.904 0.9428 0.923 66 35 7 4 0.7321 0.7 1 0.8235 70 12 30 0

[!htb] LLM Performance on ProntoQA Test (True/False Mix; Text vs. SMT): SMT shows divergent outcomes: catastrophic failure for some (e.g., DeepSeek R1 SMT F1 0.00 vs. Text 1.00), yet significant improvement for others (Gemini Flash 2.0 Lite SMT Accuracy 0.78 vs. Text 0.56), highlighting inconsistent SMT reliability on mixed arithmetic statements. ProntoQA TEST - BOTH TRUE AND FALSE Text SMT Accuracy Precision Recall F1 TP TN FP FN Accuracy Precision Recall F1 TP TN FP FN o3-mini (medium effort) 1.0000 1.0000 1.0000 1.0000 258 240 0 0 1.0000 1.0000 1.0000 1.0000 258 242 0 0 Deepseek v3 0324 0.7200 0.7138 0.7635 0.7378 197 163 79 61 0.5140 0.5484 0.3295 0.4116 85 172 70 173 DeepSeek R1 1.0000 1.0000 1.0000 1.0000 253 242 0 0 0.4840 0.0000 0.0000 0.0000 0 242 0 258 Gemini Flash 2.0 0.7180 0.8232 0.5770 0.6780 149 210 32 109 0.4560 0.4753 0.5232 0.4981 135 93 149 123 Gemini Flash 2.0 Lite 0.5630 0.5811 0.5333 0.5562 136 144 98 119 0.7820 0.7210 0.9418 0.8168 243 148 94 15

### C.2 Detailed Performance of Uncertainty Metrics for Ground Truth Prediction

This section provides a granular view of the performance of various Probabilistic Context-Free Grammar (PCFG) derived metrics, self-consistency measures, and ensemble methods in predicting the correctness of SMT-LIB outputs (with respect to ground truth) for specific LLM and dataset combinations. The metrics evaluated include AUROC (Area Under the Receiver Operating Characteristic Curve) for discrimination, ECE (Expected Calibration Error) and Brier score for calibration, and AURC (Area Under the Risk-Coverage Curve) along with optimal threshold (Opt.T), error rate at threshold (Err@T), and relative error reduction (RelErrRed) for selective prediction utility.

The UQ results for o3-mini on StrategyQA demonstrate moderate success in distinguishing correct SMT outputs from incorrect ones. While Grammar Entropy shows good individual discriminative power (AUROC 0.7448, AURC 0.1113), achieving a 13.88% relative error reduction by abstaining on just 5% of samples, many other standalone PCFG metrics exhibit weaker performance. The self-consistency metrics (Text and SMT) also perform well (AUROC 0.74), indicating that agreement between the LLM’s own reasoning modalities is a key signal. Notably, the Ensemble ML method achieves the highest AUROC (0.7850) and a significant relative error reduction (29.29% by abstaining on 10% of samples), underscoring the benefit of integrating diverse uncertainty signals through a learned model. The comparatively higher ECE for many metrics suggests that while discriminative, their raw scores may not always be well-calibrated probabilities.

Table 2: Uncertainty Qua
