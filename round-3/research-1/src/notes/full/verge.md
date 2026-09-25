URL: https://arxiv.org/html/2601.20055 | FULL FETCH | 2026-09-24T01:53:37Z
warning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
URL: https://arxiv.org/html/2601.20055
Type: HTML
Length: 98393 chars (truncated)

--- Content ---

##### Report GitHub Issue

×

Title:

Content selection saved. Describe the issue below:

Description:

Submit without GitHub Submit in GitHub

arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[ Back to arXiv ](/)

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) Report Issue [ Back to Abstract ](/abs/2601.20055v2 "Back to abstract page") [ Download PDF](/pdf/2601.20055v2 "Download PDF") [ ](javascript:toggleNavTOC\(\); "Toggle navigation") [ ](javascript:toggleReadingMode\(\); "Disable reading mode, show header and footer")

  1. Abstract
  2. 1 Introduction
     1. The Expressivity Trade-off and Pragmatic Verification.
  3. 2 Related Work
     1. Probabilistic vs. Formal Verification.
     2. Neuro-Symbolic Integration and the Semantic Gap.
     3. Automated Reasoning for Repair.
  4. 3 Methodology
     1. 3.1 Entity Extraction and Generation
     2. 3.2 Claim Decomposition and Classification
     3. 3.3 SMT Formalization with Consensus
     4. 3.4 Verification Cascade
        1. Semantic Routing (Flexibility Mechanism).
        2. SMT-Based Verification.
        3. Soft Verification.
        4. Hybrid Verification.
     5. 3.5 Score Aggregation
        1. Iterative Refinement.
  5. 4 Results
     1. Benchmarking Neuro-Symbolic Reasoning.
     2. General Performance Trends and Robustness.
     3. 4.1 Compute Parity and Search Baselines
     4. 4.2 Ablation study: The Role of MCS, Routing, and Feedback systems
        1. Impact of Architectural Components.
        2. Feedback Granularity.
        3. Semantic Router Reliability.
        4. Scoring sensitivity.
     5. 4.3 Efficiency and Convergence
     6. 4.4 Model Scalability and The Formalization Barrier
  6. 5 Conclusions
  7. 6 Limitations
     1. Computational Overhead.
     2. Formalization Barrier and Access Inequality.
  8. 7 Ethical Considerations
     1. Logical Correctness is not Ethical Correctness.
     2. Risk of Overconfidence and Misplaced Trust.
  9. References
  10. A VERGE: Algorithm / Pseudo code
  11. B Rationale for Greedy MCS Computation
     1. The Greedy Approximation.
     2. Stability & Order Dependence:
  12. C Semantic Claim Type Definitions
     1. C.1 Technical Implementation Details
        1. C.1.1 Atomic Decomposition Strategy
        2. C.1.2 Formalization into SMT-LIB2
     2. C.2 Formal Definition of Semantic Equivalence
        1. C.2.1 Logical Framework
        2. C.2.2 Equivalence Definition
        3. C.2.3 Verification Implementation
     3. C.3 Semantic Router Stress-Test Dataset
  13. D Adversarial Robustness and Context Faithfulness
  14. E Reproducibility & Implementation Details
     1. E.1 Hyperparameters and Configuration
     2. E.2 Prompt Templates
        1. E.2.1 Claim Decomposition & Classification
        2. E.2.2 Autoformalization (Natural Language →\rightarrowSMT-LIB2)
        3. E.2.3 Feedback Injection (Refinement Step)
     3. E.3 Consensus and Scoring Metrics
        1. Formalization Consensus.
        2. Variance-Based Scoring.
     4. E.4 Pipeline Reliability and Failure Modes
        1. Decomposition.
        2. Formalization funnel.
        3. Routing distribution.
        4. Error taxonomy.
        5. Entity extraction.
        6. Shared hallucinations.
        7. Bridges and cross-model consensus.
     5. E.5 Compute Infrastructure
     6. E.6 Benchmark Descriptions
  15. F Detailed Verification Trajectories



[ License: CC BY-NC-ND 4.0 ](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2601.20055v2 [cs.CL] 02 May 2026

# VERGE: Formal Refinement and Guidance Engine for Verifiable LLM Reasoning

Vikash Singh Darion Cassel ††thanks: Work done during internship at Amazon Web Services Affiliation: Case Western Reserve University  Affiliation: Amazon Web Services  Nathaniel Weir  Affiliation: Amazon Web Services  Nick Feng  Affiliation: Amazon Web Services  Sam Bayless  Affiliation: Amazon Web Services 

###### Abstract

Despite the syntactic fluency of Large Language Models (LLMs), ensuring their logical correctness in high-stakes domains remains a fundamental challenge. We present a neurosymbolic framework that combines LLMs with SMT solvers to produce verification-guided answers through iterative refinement. Our approach decomposes LLM outputs into atomic claims, autoformalizes them into first-order logic, and verifies their logical consistency using automated theorem proving. We introduce three key innovations: (1) multi-sample consensus via formal semantic equivalence checking to ensure logic-level alignment between candidates, eliminating the syntactic bias of surface-form metrics, (2) semantic routing that directs different claim types to appropriate verification strategies: symbolic solvers for logical claims and LLM ensembles for commonsense reasoning, and (3) precise logical error localization via Minimal Correction Subsets (MCS), which pinpoint the exact subset of claims to revise, transforming binary failure signals into actionable feedback. Our framework classifies claims by their logical status and aggregates multiple verification signals into a unified score with variance-based penalty. The system iteratively refines answers using structured feedback until acceptance criteria are met or convergence is achieved. This hybrid approach delivers formal guarantees where possible and consensus verification elsewhere, advancing trustworthy AI. With the GPT-OSS-120B model, VERGE demonstrates an average performance uplift of 18.7% at convergence across a set of reasoning benchmarks compared to single-pass approaches.

## 1 Introduction

Figure 1: VERGE correcting LLM Hallucinations via Formal Verification. The solver detects an unsupported claim and guides the LLM to a consistent answer through MCS-based feedback.

Large Language Models (LLMs) have demonstrated remarkable capabilities across diverse reasoning tasks, from mathematical problem-solving (Lewkowycz et al., 2022; Hendrycks et al., 2021) to code generation (Chen et al., 2021; Austin et al., 2021) and logical inference (Tafjord et al., 2021). Despite these advances, ensuring the correctness of LLM-generated answers remains a critical barrier in high-stakes domains such as legal policy compliances, healthcare and finance etc. While recent models achieve impressive benchmark performance (OpenAI, 2025; Anthropic, 2025), they rely on statistical likelihood maximization (Ouyang et al., 2022) rather than logical deduction. Consequently, they operate without mechanisms for provable correctness, making them prone to hallucinations and internal contradictions.

Current verification strategies such as self-consistency (Wang et al., 2022), process supervision (Lightman et al., 2023), and self-refinement (Madaan et al., 2023; Shinn et al., 2023) provide heuristic rather than formal guarantees. Even multi-agent debate frameworks (Du et al., 2023; Liang et al., 2023) merely achieve consensus, which does not imply correctness. To achieve verifiable reasoning, neuro-symbolic methods (Singh et al., 2026; Ganguly et al., 2025; Ganguly et al., 2024; Feng et al., 2025; Pan et al., 2023; Callewaert et al., 2025; Olausson et al., 2023; Garcez et al., 2019; Mao et al., 2019) and semantic parsing (Wang et al., 2026; McGinness and Baumgartner, 2024; Zettlemoyer and Collins, 2005; Dong and Lapata, 2016; Zhang et al., 2025) have attempted to bridge natural language with formal logic. However, these approaches face a fundamental _semantic gap_ : natural language is inherently ambiguous, and rigid formalization often fails on open-domain claims (Church, 1936; Turing, 1936).

We present VERGE, a framework that mitigates this gap by combining LLMs with Satisfiability Modulo Theories (SMT) solvers (Barrett et al., 2009; De Moura and Bjørner, 2008) to produce verification-guided answers with formal guarantees for logical/mathematical claims through iterative refinement, as illustrated in Figure 1. Unlike standard feedback loops, VERGE leverages the SMT solver’s ability to extract unsatisfied assertions (Zhang and Malik, 2003; Nadel et al., 2013). This allows us to compute Minimal Correction Subsets (MCS) (Marques-Silva et al., 2013a; Marques-Silva et al., 2013b), identifying a minimal set of modifications to the atomic claims sufficient to restore consistency and move from probabilistic self-correction to provable self-consistency correction.

##### The Expressivity Trade-off and Pragmatic Verification.

A key insight of our work is that enforcing formal verification on all claims is fundamentally misaligned with the ambiguity of natural language. Rather than attempting to bridge this gap universally, a theoretically intractable goal, we adopt a pragmatic stance: Apply formal verification where the semantic gap is narrow (mathematical/logical claims), and fall back to consensus-based verification where it is wide (commonsense/vague claims). VERGE introduces a verification cascade with semantic routing to implement this strategy. This hybrid approach provides formal guarantees for a verifiable subset of claims while maintaining the system’s ability to handle broad, real-world reasoning tasks.

Our work introduces:

  1. 1.

High-Fidelity Consensus via SMT: We bridge the semantic gap by enforcing semantic equivalence (ϕa⇔ϕb\phi_{a}\iff\phi_{b}) among candidate formalizations. Unlike syntactic metrics (e.g., BLEU, Jaccard) which fail on variable renaming or structural permutation, we utilize the solver to prove that different candidate formulas yield identical truth tables, ensuring robust consensus.

  2. 2.

Actionable Feedback via MCS: We adapt greedy MCS computation (Marques-Silva et al., 2013b; Morgado et al., 2013; Bacchus and Katsirelos, 2016) to provide polynomial-time, specific feedback (e.g., "claim C2C_{2} does not hold") rather than generic error signals.

  3. 3.

Flexible Neuro-symbolic Integration: A semantic routing framework that balances the precision of SMT solvers with the flexibility of LLMs, avoiding the pitfalls of forcing undecidable language into decidable theories.




## 2 Related Work

##### Probabilistic vs. Formal Verification.

Standard LLM reasoning strategies rely on probabilistic confidence. Methods like self-consistency (Wang et al., 2022) and process supervision (Ganguly et al., 2026; Chen et al., 2025; Lightman et al., 2023; Uesato et al., 2022; Yang et al., 2026) aggregate samples or train verifiers on human labels, but cannot guarantee logical soundness. Self-refinement approaches (Madaan et al., 2023; Shinn et al., 2023; Welleck et al., 2022) use the model to critique itself, often failing due to the faithfulness gap where reasoning does not match output (Lyu et al., 2023; Huang et al., 2023). Multi-agent debate (Du et al., 2023; Liang et al., 2023) achieves consensus, not truth, recent work shows self-correction can even degrade performance (Huang et al., 2023; Kamoi et al., 2024). In contrast, VERGE uses SMT solvers (Barrett et al., 2009; De Moura and Bjørner, 2008) to provide mathematically proven feedback. Unlike tool-augmented LLMs (Schick et al., 2023; Gou et al., 2024) that use tools for execution (e.g., calculators), we use tools for consistency checking, computing MCS. (Zhang and Malik, 2003; Nadel et al., 2013) to identify exactly which premises contradict the generated answer.

##### Neuro-Symbolic Integration and the Semantic Gap.

Traditional semantic parsing (Zafar et al., 2026; Dong and Lapata, 2016; Berant et al., 2013; Zettlemoyer and Collins, 2005) maps language to executable logical forms but requires expensive supervision. Recent work extends this to theorem proving (Polu and Sutskever, 2020; Polu et al., 2022; Jiang et al., 2022; Azerbayev et al., 2023) and augmenting LLMs with symbolic solvers (Pan et al., 2023; Olausson et al., 2023; Callewaert et al., 2025), but these require fully formalizable domains. Prior neuro-symbolic integration (Mao et al., 2019; Garcez et al., 2019; Kautz, 2022) and grammar-based approaches (Ganguly et al., 2024) struggle with the semantic gap (Church, 1936; Turing, 1936) the mismatch between ambiguous natural language and rigid formal systems. VERGE targets open-domain natural language where full formalization is often impossible. We introduce semantic routing, rather than forcing vague or commonsense claims into rigid first-order logic, we route them to a consensus-based soft verifier. This treats the semantic gap as an inherent property of language requiring hybrid verification.

##### Automated Reasoning for Repair.

Our feedback mechanism adapts MCS computation (Marques-Silva et al., 2013b; Liffiton and Sakallah, 2008) from constraint programming to NLP. MCS identifies the minimal set of constraints to delete to restore satisfiability. Recent work applies MCS to constraint relaxation (Bacchus and Katsirelos, 2016) and automated debugging (Morgado et al., 2013). We innovate by translating MCS output into natural language feedback, guiding the LLM to rewrite specific atomic claims. This prioritizes interpretability and convergence speed (O⁡(m×SAT)O(m\times\text{SAT}) greedy approximation) over theoretical optimality. To our knowledge, VERGE is the first to apply MCS-based feedback to guide iterative refinement in LLM reasoning, converting abstract unsat cores into actionable guidance (see Appendix B).

Figure 2: Overview of VERGE: The pipeline is structured into five distinct stages: Setup prepares the context 𝒞\mathcal{C} and entities ℰ\mathcal{E}; Generation produces and refines answers 𝒜(t)\mathcal{A}^{(t)} iteratively; Formalization classifies claim types τi\tau_{i} and generates SMT formulas φci\varphi_{c_{i}}; Verification routes claims to SMT, Soft, or Hybrid verifiers based on semantic type; and Decision computes the aggregate score 𝒮⁡(𝒜)\mathcal{S}(\mathcal{A}) to either accept the answer 𝒜∗\mathcal{A}^{*} or generate feedback ℱ(t)\mathcal{F}^{(t)} for the next iteration.

## 3 Methodology

Problem Formulation. Given a context 𝒞={p1,…,pm}\mathcal{C}=\\{p_{1},\ldots,p_{m}\\} of premise statements and a query qq, we aim to produce a verified answer 𝒜∗\mathcal{A}^{*} composed of atomic claims {c1,…,cn}\\{c_{1},\ldots,c_{n}\\} with maximal verification coverage. Here, 𝒜∗\mathcal{A}^{*} is a refined version of the candidate answer 𝒜\mathcal{A} obtained through verification. We formalize this as maximizing the verification score 𝒮⁡(𝒜)∈[0,1]\mathcal{S}(\mathcal{A})\in[0,1] subject to two constraints for each claim cic_{i}: (1) Consistency: SAT​(φ𝒞∧φci)=true\text{SAT}(\varphi_{\mathcal{C}}\wedge\varphi_{c_{i}})=\text{true}, and (2) Entailment: SAT​(φ𝒞∧¬φci)=false\text{SAT}(\varphi_{\mathcal{C}}\wedge\neg\varphi_{c_{i}})=\text{false}, where φ\varphi denotes the logical formalization function that maps natural language statements to SMT constraints. The consistency constraint verifies that each claim is compatible with the context, while the entailment constraint ensures that each claim is a logical consequence of the context. These constraints provide formal equivalence guarantees where logic permits, while falling back to semantic consistency (soft verification, see §3.4) otherwise. Pipeline. The pipeline (Fig. 2) executes iteratively: (1) entity extraction, (2) generation, (3) decomposition, (4) formalization & verification, and (5) refinement.

### 3.1 Entity Extraction and Generation

We first extract entities ℰ=Extract​(𝒞,q)\mathcal{E}=\text{Extract}(\mathcal{C},q) (e.g., ‘Felix’, ‘Monday’, ‘Process A’) to serve as typed constants in SMT. At iteration tt, we generate answer 𝒜(t)\mathcal{A}^{(t)} via a language model MM:

| 𝒜(t)=M⁡(𝒞,q,𝒜(t−1),ℱ(t−1))\mathcal{A}^{(t)}=M(\mathcal{C},q,\mathcal{A}^{(t-1)},\mathcal{F}^{(t-1)}) |  | (1)  
---|---|---|---  
  
where ℱ(t−1)\mathcal{F}^{(t-1)} is structured feedback (see §3.5). The initial iteration (t=1t=1) utilizes zero-shot prompting (e.g., A0=M⁡(𝒞,q,∅,∅)A^{0}=M(\mathcal{C},q,\emptyset,\emptyset)).

### 3.2 Claim Decomposition and Classification

We decompose 𝒜\mathcal{A} into atomic claims {c1,…,cn}\\{c_{1},\ldots,c_{n}\\}. To ensure our system is honest about what it can and cannot formally prove, we classify each claim cic_{i} into a semantic type τi∈𝒯\tau_{i}\in\mathcal{T} via MM:

| τi=arg⁡maxτ∈{τM,τL,τT,τP,τC,τV}​PM​(τ∣ci)\tau_{i}=\arg\max_{\tau\in\\{\tau_{\text{M}},\tau_{\text{L}},\tau_{\text{T}},\tau_{\text{P}},\tau_{\text{C}},\tau_{\text{V}}\\}}P_{M}(\tau\mid c_{i}) |  | (2)  
---|---|---|---  
  
where types correspond to Mathematical, Logical, Temporal, Probabilistic, Commonsense, and Vague claims. These categories align with standard distinctions in semantic parsing to differentiate verifiable facts from subjective or probabilistic statements. This classification is crucial for minimizing "false formalization", the error of forcing ambiguous natural language into rigid logic. Vague claims are identified by the model as containing subjective predicates (e.g., "likely", "possibly") that lack binary truth values, preventing brittle SMT assertions.

### 3.3 SMT Formalization with Consensus

For claims classified as logical or mathematical, we target the QF_UF (Quantifier-Free Uninterpreted Functions) and QF_LIA (Quantifier-Free Linear Integer Arithmetic) fragments within the SMT-LIB2 standard. Given the context 𝒞\mathcal{C} and query qq, we first extract entities ℰ\mathcal{E} as a set of typed constants. For example, from the statement “All humans above age 18 are adults”, we extract entities a​g​eage of type ℤ\mathbb{Z} and a​d​u​l​tadult of type AGE_GROUP, which are declared as uninterpreted constants of the corresponding sorts. We then use generate candidate formulas ϕ=M⁡(ci,ℰ)\phi=M(c_{i},\mathcal{E}) for each claim cic_{i} over the vocabulary in ℰ\mathcal{E}. To mitigate the stochastic nature of autoformalization, we generate K=3K=3 candidate formulas {ϕ1,…,ϕK}\\{\phi_{1},\ldots,\phi_{K}\\} and check for consensus. Instead of relying on brittle syntactic overlap, we compute consensus based on semantic equivalence (see Appendix C.2 for the formal definition). Two formulas ϕa\phi_{a} and ϕb\phi_{b} are deemed equivalent if and only if their bidirectional entailment is valid, which we verify by querying the SMT solver:

| Equiv​(ϕa,ϕb)⇔UNSAT​(Σℰ∧¬(ϕa↔ϕb))\text{Equiv}(\phi_{a},\phi_{b})\iff\text{UNSAT}\left(\Sigma_{\mathcal{E}}\wedge\neg(\phi_{a}\leftrightarrow\phi_{b})\right) |  | (3)  
---|---|---|---  
  
where Σℰ\Sigma_{\mathcal{E}} represents the declarations of constants and uninterpreted functions derived from the entity extraction phase. This procedure constructs a semantic equivalence graph where edges represent proven logical identity.

A formalization is accepted only if a majority consensus is reached (i.e., the size of the largest semantic equivalence clique is ≥⌈K/2⌉\geq\lceil K/2\rceil). Additionally, we employ Round-Trip Translation (SMT →\to Natural Language) as a semantic sanity check to ensure alignment with the source text. If consensus fails or the confidence (derived from clique size and round-trip similarity) is low, we trigger a self-correction step φnew=M⁡(φ,…)\varphi^{\text{new}}=M(\varphi,\dots), constrained such that φnew⊧φ\varphi^{\text{new}}\models\varphi. This ensures the system strictly strengthens (and never weakens) the constraints during refinement. The strengthening constraint is verified by checking the unsatisfiability of φnew∧¬φ\varphi^{\text{new}}\wedge\neg\varphi. To ensure decidability, we perform this check over the finite domain of entities ℰ\mathcal{E} extracted in the setup phase, effectively reducing the check to propositional logic or quantifier-free first-order logic(QF-FOL).

### 3.4 Verification Cascade

We employ a hybrid strategy that routes claims to the most rigorous verifier available for their type, prioritizing formal guarantees where applicable.

##### Semantic Routing (Flexibility Mechanism).

We define a routing function 𝒱τi\mathcal{V}_{\tau_{i}}:

| 𝒱τi={SMT-Verifyif ​τi∈{τM,τL,τT}Soft-Verifyif ​τi∈{τC,τV,τP}Hybridelse (or SMT error)\mathcal{V}_{\tau_{i}}=\begin{cases}\text{{SMT-Verify}}&\text{if }\tau_{i}\in\\{\tau_{\text{M}},\tau_{\text{L}},\tau_{\text{T}}\\}\\\ \text{{Soft-Verify}}&\text{if }\tau_{i}\in\\{\tau_{\text{C}},\tau_{\text{V}},\tau_{\text{P}}\\}\\\ \text{{Hybrid}}&\text{else (or SMT error)}\end{cases} |  | (4)  
---|---|---|---  
  
While SMT provides provable correctness, it cannot natively handle vague predicates (e.g., ‘is similar to’) without excessive and fragile axioms. By routing these to Soft-Verify, VERGE preserves logical rigor where possible while preventing the system from falsely treating probabilistic or ambiguous reasoning as logical certainty.

##### SMT-Based Verification.

For logic-amenable claims, we check satisfiability using the Z3 solver. We assign statuses based on rigorous logical tests:

  * •

Contradictory (σC\sigma_{\text{C}}): SAT​(φ𝒞∧φci)=False\text{SAT}(\varphi_{\mathcal{C}}\wedge\varphi_{c_{i}})=\text{False}. The claim violates the context.   


  * •

Entailed (σE\sigma_{\text{E}}): SAT​(φ𝒞∧¬φci)=False\text{SAT}(\varphi_{\mathcal{C}}\wedge\neg\varphi_{c_{i}})=\text{False}. The claim is proven true (proof by contradiction).   


  * •

Possible (σP\sigma_{\text{P}}): Consistent (SAT​(φ𝒞∧φci)=True\text{SAT}(\varphi_{\mathcal{C}}\wedge\varphi_{c_{i}})=\text{True}) but not entailed. The context allows the claim but does not force it.   


  * •

Unknown (σU\sigma_{\text{U}}): Solver timeout or execution error.




Minimal Correction Sets (MCS). For contradictions (σC\sigma_{\text{C}}), we compute the MCS to generate precise feedback. Let φci\varphi_{c_{i}} be a set of clauses, the subset S⊂o​f​φciS\subset of\varphi_{c_{i}} is a minimal correction set (MCS) if

  * •

SAT(φ𝒞∧φci∖S\varphi_{\mathcal{C}}\wedge\varphi_{c_{i}}\setminus S) = true

  * •

∀S′⊂S\forall S^{\prime}\subset S, SAT(φ𝒞∧φci∖S′\varphi_{\mathcal{C}}\wedge\varphi_{c_{i}}\setminus S^{\prime}) = false




Intuitively, MCS is small subset of clauses to remove to restore satisfibility. This provides actionable guidance to address contradictions (e.g., "remove constraint X") rather than generic error messages. See Appendix B for details about MCS computation.

##### Soft Verification.

For claims unsuitable for SMT, we use an ensemble of LLM judges. We compute a confidence weighted majority vote (using self-reported confidence of the judge) by defining verdicts v∈{Supported, Plausible, Unsupported, Uncertain}v\in\\{\text{Supported, Plausible, Unsupported, Uncertain}\\}.

Constraint: To penalize the lack of formal guarantees, soft-verified claims are capped at a lower maximum score contribution than SMT-verified claims (see §3.5).

##### Hybrid Verification.

The Hybrid strategy acts as a robustness fallback. Claims routed to SMT that fail due to non-logical errors (e.g., syntax errors, undeclared variables, or timeouts) are automatically re-routed to Soft Verification. This prevents the pipeline from stalling on "Unknown" (σU\sigma_{U}) statuses due to correctable formalization issues, allowing the system to degrade gracefully from formal proof to probabilistic consensus.

### 3.5 Score Aggregation

We compute an aggregated verification score for the entire answer by combining verification results from both soft and hard verification across all atomic claims. Let 𝒜\mathcal{A} be an answer to query qq given context 𝒞\mathcal{C}. Suppose 𝒜\mathcal{A} is decomposed into atomic claims c1,…,cnc_{1},\ldots,c_{n} and verified against qq and 𝒞\mathcal{C} to produce verification results σ1,…,σn\sigma_{1},\ldots,\sigma_{n}, respectively. The verification score S⁡(σi)S(\sigma_{i}) for each result is defined as:

| S⁡(σi)={1.0if Entailed(σi)0.9if Supported(σi)0.7if Possible(σi)0.0if Contradictory(σi) or elseS(\sigma_{i})=\begin{cases}1.0&\text{if {Entailed}($\sigma_{i}$)}\\\ 0.9&\text{if {Supported}($\sigma_{i}$)}\\\ 0.7&\text{if {Possible}($\sigma_{i}$)}\\\ 0.0&\text{if {Contradictory}($\sigma_{i}$) or else}\end{cases} |  | (5)  
---|---|---|---  
  
These weights reflect verification rigor: formally entailed claims receive the maximum score (1.0), while soft-verified supported claims receive 0.9, ensuring the system favors provable logic over semantic consistency. The final aggregated score 𝒮⁡(𝒜)\mathcal{S}(\mathcal{A}) integrates a variance-based penalty (Eq. 6) to discourage “gaming” the system, where a model might generate claims that are individually confident but mutually contradictory under joint verification:

| 𝒮⁡(𝒜)=S¯⋅max⁡(0.5,1.0−σSS¯+0.01)\mathcal{S}(\mathcal{A})=\bar{S}\cdot\max\left(0.5,1.0-\frac{\sigma_{S}}{\bar{S}+0.01}\right) |  | (6)  
---|---|---|---  
  
where S¯\bar{S} is the mean of the verification scores {S⁡(σ1),…,S⁡(σn)}\\{S(\sigma_{1}),\ldots,S(\sigma_{n})\\} and σS\sigma_{S} is their standard deviation.

##### Iterative Refinement.

At each iteration tt, we generate feedback ℱ(t)\mathcal{F}^{(t)} containing: (1) Unsat Cores & MCS for contradictions, pinpointing exact logical conflicts; (2) Joint Conflicts for mutually incompatible claims; and (3) Formalization Alerts for low-confidence mappings. The process repeats until 𝒮⁡(𝒜)≥0.75\mathcal{S}(\mathcal{A})\geq 0.75 and JointSAT=True (where JointSAT is the boolean result of the joint satisfiability check), or until convergence (Δ​𝒮<0.01\Delta\mathcal{S}<0.01). For Joint Consistency, soft-verified claims are treated as atomic boolean variables (bib_{i}) within the SMT solver. To capture interactions between soft and hard claims, the context formalization φ𝒞\varphi_{\mathcal{C}} includes bridging axioms generated by the LLM (e.g., assertions linking vague predicates like “small” to numerical bounds). This allows the solver to detect if a mathematically proven claim (τM\tau_{M}) contradicts a commonsense claim (τC\tau_{C}) (e.g., Mathematical Claim “X>10X>10” vs Commonsense Claim “XX is a small single-digit number” which implies X<10X<10), ensuring holistic consistency even without full formalization of the commonsense component. If claims are not jointly consistent, we compute the MCS over the claims as refinement feedback, signaling a minimal patch to restore joint consistency. Algorithm 1 (Appendix) details the complete refinement procedure.

## 4 Results

Prompting Neuro-Symbolic Baselines VERGE (Ours) Dataset Model CoT SC SR DSB LogicLM LINC PoT w/o MCS w/o Rt Full FOLIO GPT-20B 40.4 52.2 34.0 53.7 29.9 18.6 48.8 73.9 86.7 89.2±1.1 GPT-120B 32.0 35.5 42.9 14.0 27.5 47.5 54.2 80.7 81.6 84.7±0.9 Sonnet-3.7 70.4 72.4 62.1 44.5 71.6 65.2 58.1 86.7 83.0 87.9±0.7 ProofWriter GPT-20B 74.6 71.4 56.8 38.8 35.8 42.8 94.0 82.7 85.8 85.2±1.3 GPT-120B 52.4 65.6 67.2 31.4 32.0 76.4 98.4 88.7 84.6 89.9±0.8 Sonnet-3.7 71.6 86.6 74.0 42.8 64.7 71.1 98.2 90.2 88.0 93.0±0.5 ZebraLogic GPT-20B 67.6 72.2 46.2 44.8 - - - 80.9 83.6 87.3±1.0 GPT-120B 84.0 77.8 72.2 28.2 - - - 88.9 90.9 91.0±0.6 Sonnet-3.7 52.0 51.0 58.8 48.0 - - - 58.0 62.8 64.8±1.4 AR-LSAT GPT-20B 81.7 89.1 63.9 59.6 21.7 - - 82.6 86.8 89.5±0.8 GPT-120B 87.8 88.7 84.8 32.2 19.9 - - 83.0 87.4 91.7±0.5 Sonnet-3.7 61.7 58.7 73.5 67.8 31.2 - - 88.2 87.7 88.6±0.9 BBEH GPT-20B 34.4 38.4 28.0 10.0 - - - 42.2 43.7 49.9±1.5 GPT-120B 38.4 41.8 37.4 20.2 - - - 54.1 50.2 58.9±1.2 Sonnet-3.7 33.0 29.4 37.8 24.0 - - - 40.4 43.5 45.9±1.4 HLE GPT-20B 9.6 15.0 8.6 1.4 - - - 12.2 13.7 19.9±1.1 GPT-120B 14.2 14.0 12.8 6.4 - - - 21.0 15.2 30.5±1.6 Sonnet-3.7 5.8 5.0 6.8 0.6 - - - 16.7 14.7 17.2±0.9

Table 1: Comprehensive Performance Analysis. Results are averaged over 5 independent runs, with error bars (subscript) indicating standard deviation. We compare VERGE against standard prompting (CoT, SC, SR) and neuro-symbolic baselines (DSB, LogicLM, LINC, PoT) across three different backbone models: GPT-OSS-20B, GPT-OSS-120B, and Claude 3.7 Sonnet. VERGE consistently outperforms baselines across diverse domains and model sizes, except on ProofWriter where the specialized PoT method remains dominant. `​`−"``-" indicates that the baseline does not support the dataset. 

##### Benchmarking Neuro-Symbolic Reasoning.

Table 1 presents a systematic evaluation of VERGE against state-of-the-art inference-time compute (prompting) strategies. To ensure comparable computational budgets, we configure Self-Consistency (SC) with k=3k=3 samples and Self-Refinement (SR) with n=3n=3 iterations with self-critique. Results for established neuro-symbolic baselines (Proof of Thought, LINC, Logic-LM) were computed using their officially released codebase.

Consistent with these parameters, VERGE operates with a maximum budget of Tmax=3T_{\max}=3 iterations. This setting balances accuracy with computational cost, whereas baselines like CoT represent single-pass performance (for convergence analysis up to Tmax=10T_{\max}=10, see Figure 3). Consequently, the improvements shown represent the specific value of iterative verification-guided refinement. To distinguish these gains from those achieved by iteration alone, we refer to our ablation study (Table 3). By comparing the full system against the “w/o MCS” and “w/o Routing” variants (both of which also operate iteratively), we isolate the substantial performance contributions of VERGE’s verification and feedback mechanisms.

##### General Performance Trends and Robustness.

As evidenced in Table 1, VERGE consistently outperforms standard prompting and existing neuro-symbolic baselines on 5 out of the 6 evaluated benchmarks. The method demonstrates robust scaling across model sizes, notably on the Humanities Last Exam (HLE), where it improves GPT-OSS-120B performance from 14.2% (CoT) to 30.5%. This contrasts with traditional neuro-symbolic baselines (DSB, LogicLM), which suffer from a “translation bottleneck”, where invalid SMT specifications cause the solver to fail silently or reject valid reasoning. VERGE overcomes this via its Verification Cascade, which utilizes Minimal Correction Sets (MCS) to isolate specific formalization errors. By iteratively refining the context based on solver feedback (Unsat Cores) rather than discarding the entire proof, VERGE successfully salvages logical entailments that probabilistic baselines miss (see Appendix F).

A notable outlier is the ProofWriter dataset, where Proof of Thought (PoT) retains dominance (98.4% vs. 89.9%). This performance gap highlights a fundamental methodological distinction between monolithic execution and modular verification. PoT approaches reasoning as program synthesis, converting the full context into a single executable artifact to derive the answer in one pass. This is ideal for the rigid, deductive structure of synthetic datasets like ProofWriter. In contrast, VERGE treats reasoning as a semantic entailment task, employing a routing mechanism to decompose and verifying individual atomic claims. On purely synthetic tasks, this general-purpose machinery specifically the overhead of claim decomposition and semantic routing, introduces unnecessary complexity compared to PoT’s direct solver execution. However, it is precisely this modular flexibility that allows VERGE to generalize to semantically complex domains like Law (AR-LSAT), where a monolithic translation to executable logic often fails due to linguistic ambiguity.

### 4.1 Compute Parity and Search Baselines

Table 2 in the appendix reports the per-problem cost on GPT-OSS-120B.VERGE at T=1T{=}1 uses fewer tokens than SR yet beats it on every benchmark, isolating verification from refinement. SC at k=10k{=}10 matches VERGE’s T=3T{=}3 token budget but trails by 46.646.6 pts on FOLIO, 1.91.9 on AR-LSAT, 15.215.2 on HLE. ToT-BFS (b=5,k=3,T=2b{=}5,k{=}3,T{=}2) on GPT-OSS-20B reaches 64.764.7 (FOLIO) and 55.955.9 (AR-LSAT) versus VERGE’s 88.588.5 and 90.190.1, at 4×4{\times} the tokens and 2×2{\times} the calls; search and verification are composable, not competitive.

Method | LLM | Solver | Tokens | Wall  
---|---|---|---|---  
| calls | calls | (I+O) | (s)  
CoT (1-pass) | 1 | 0 | 2.1K | 3.2  
SC (k=3k{=}3) | 3 | 0 | 6.3K | 8.7  
SC (k=10k{=}10) | 10 | 0 | 21.0K | 28.3  
SR (n=3n{=}3) | 6 | 0 | 11.4K | 15.3  
PoT | 2 | 1 | 4.8K | 5.4  
LINC | 3 | 1 | 5.1K | 6.1  
ToT-BFS | 40 | 0 | 63.0K | 71.2  
VERGE (T=1T{=}1) | ∼8{\sim}8 | ∼5{\sim}5 | 8.4K | 11.8  
VERGE (T=3T{=}3) | ∼17{\sim}17 | ∼15{\sim}15 | 18.2K | 32.6  
Table 2: Per-problem cost on GPT-OSS-120B, averaged across six benchmarks. Solver calls are CPU-only (<<200ms each). VERGE at T=1T{=}1 is cheaper than SR yet outperforms it; SC at k=10k{=}10 matches VERGE’s token budget but not its accuracy.

### 4.2 Ablation study: The Role of MCS, Routing, and Feedback systems

Architectural Components Feedback Granularity Dataset Full w/o MCS w/o Routing Soft-Only Unsat-Core Only MSF FOLIO 84.7 80.7 81.6 80.8 79.3 76.5 ProofWriter 89.9 88.7 84.6 75.8 82.4 80.1 ZebraLogic 91.0 88.9 90.9 70.2 85.3 72.5 AR-LSAT 91.7 83.0 87.4 84.6 89.4 89.2 BBEH 58.9 54.1 50.2 41.7 42.7 40.1 HLE 30.5 21.0 15.2 13.2 23.2 19.8 Avg. Drop – -6.8% -8.3% -22.8% -10.9% -15.3%

Table 3: Ablation Study on Component Contributions (GPT-OSS-120B). We isolate the impact of Minimal Correction Subsets (MCS), Semantic Routing (Rt), and the SMT Solver itself. Full represents the complete VERGE pipeline. w/o Routing forces SMT verification for all claims. Soft-Only removes the SMT solver entirely, relying solely on LLM consensus. Unsat-Core-Only and MSF vary the granularity of the feedback.

##### Impact of Architectural Components.

Table 3 isolates the contributions of VERGE’s key components using GPT-OSS-120B. The full pipeline consistently outperforms all ablated variants, confirming that both Minimal Correction Sets (MCS) and Semantic Routing are integral to maximizing VERGE’s performance. We observe that MCS is particularly critical for strict constraint satisfaction tasks. On AR-LSAT, removing MCS causes a sharp drop from 91.7% to 83.0%. This indicates that while the solver can detect contradictions, the model struggles to resolve complex scheduling conflicts without the precise, minimal deletion guidance provided by the MCS. Conversely, Semantic Routing proves advantageous for open-ended and commonsense reasoning. Removing the routing mechanism, thereby forcing all claims into formal logic, substantially impacts HLE and BBEH, with HLE scores halving from 30.5% to 15.2%. This lends support to the “Formalization Barrier” hypothesis (discussed in §4.4): attempting to formalize vague or fuzzy predicates leads to brittle systems that reject valid reasoning (e.g., a solver might reject a valid commonsense claim due to a missing axiom). Routing allows VERGE to fallback to soft verification when necessary, a benefit most pronounced in domains with high ambiguity like HLE.

##### Feedback Granularity.

The right side of Table 3 demonstrates the value of high-resolution feedback. There is a clear hierarchy of performance correlated with feedback specificity. Unsat-Core Only feedback, which identifies conflicting constraints but does not prescribe a fix, lags behind the full model by 10.9% on average. Minimal Solver Feedback (MSF) performs worst, with a 15.3% average drop. This confirms that simply telling an LLM “you are wrong (UNSAT)” (binary feedback) is insufficient for complex reasoning; the model requires the actionable, structural guidance that VERGE provides.

To address the converse hypothesis whether formal verification is necessary at all we evaluated a Soft-Only variant where all claims are routed to the LLM consensus mechanism, bypassing the SMT solver entirely. As shown in Table 3, this results in the most significant performance degradation across the board (average drop: -22.8%). The impact is most severe on strict constraint satisfaction tasks like ZebraLogic (91.0% →\rightarrow 70.2%) and ProofWriter (89.9% →\rightarrow 75.8%), confirming that while soft verification is useful for ambiguity, it lacks the precision required to resolve complex logical dependencies. This effectively validates the necessity of the hybrid approach: VERGE requires SMT for precision and Semantic Routing for flexibility.

##### Semantic Router Reliability.

To validate our routing mechanism, we evaluated the classifier on a stress-test dataset (also see Appendix C.3) of N=54N=54 claims, including adversarial edge cases such as idioms (e.g., “gave 110%”) and vague quantifiers. The router achieved an overall accuracy of 94%, with strong discrimination between categories (SMT: F1=0.93; Soft: F1=0.95). Crucially, the error patterns reveal a safe failure mode: only 1 out of 32 soft claims was misrouted to SMT; a recoverable error that triggers autoformalization fallback. The high recall for Soft claims (0.97) and precision for SMT claims (0.95) confirm the system effectively shields the solver from ambiguity while preserving logical rigor.

##### Scoring sensitivity.

The weights (1.0,0.9,0.7,0.0) encode an ordinal hierarchy, not a tuned operating point. Varying the Supported weight wSw_{S} on GPT-OSS-120B (Table 4) yields worst-case −1.3%-1.3\% and mean |Δ|<0.6%|\Delta|{<}0.6\%; collapsing wS=1.0w_{S}{=}1.0 slightly hurts, confirming the discount appropriately favors entailment over consensus.

### 4.3 Efficiency and Convergence

Fig. 3 (in Appendix) reveals a striking divergence in refinement dynamics. VERGE achieves monotonic improvement across all six datasets (Kendall’s τ=1.0\tau=1.0, p<0.001p<0.001), with average convergence at iteration 6.2 (σ=1.3\sigma=1.3), beyond T=10 (Table 13) , the gains in performance are negligible (<0.3%<0.3\% across all benchmarks), validating our convergence criterion (Δ​S<ϵ=0.01)(\Delta{S}<\epsilon=0.01). In contrast, probabilistic self-refinement exhibits what we term the correlation cliff phenomenon: performance systematically degrades in 85.2% of trials (χ2=26.7\chi^{2}=26.7, p<0.001p<0.001), characterized by a strong negative correlation between iteration and accuracy (τ=−0.84\tau=-0.84 average, p<0.001p<0.001). This could be due to self-refinement (without formal verification) introducing hallucinations where the model "corrects" valid reasoning into invalid states. This convergence analysis provides the strongest statistical evidence for VERGE’s value: while final accuracy gains are modest (average +9.3 points), the observed consistent monotonic improvement has high practical value in production systems where reliability matters more than peak performance.

### 4.4 Model Scalability and The Formalization Barrier

We observe that effectiveness is contingent on the model’s ability to produce syntactically valid SMT code. We term this threshold the Formalization Barrier. Our tested model under 20B parameters (GPT-OSS-20B) struggles, achieving only ∼\sim30% syntax validity. In this regime, the solver acts merely as a spell-checker. However, models in the 120B+ and frontier regime (GPT-OSS-120B, Sonnet) cross the barrier (>90% validity). Here, solver feedback shifts from generic error messages to semantic logical contradictions, enabling VERGE’s MCS mechanism to perform actual reasoning repairs. This suggests that neuro-symbolic verification is a capability that emerges with scale, and VERGE is uniquely positioned to leverage the next generation of highly capable reasoning models.

## 5 Conclusions

We present VERGE, a neuro-symbolic framework combining LLMs with SMT solvers for verified reasoning via iterative refinement. Our approach introduces three key innovations: (1) high-fidelity formalization via multi-sample consensus, (2) semantic routing that balances symbolic solvers with soft verification, and (3) actionable feedback via Minimal Correction Subsets (MCS) for precise error localization. Evaluation shows VERGE excels in formal reasoning and achieves convergence across all datasets, contrasting with the degradation often observed in probabilistic self-refinement. Our analysis identifies a “Formalization Barrier” at the 70B+ parameter scale where semantic verification becomes viable. By bridging neural generation with symbolic reasoning, VERGE provides a practical step toward trustworthy AI with provable correctness where logic permits.

## 6 Limitations

##### Computational Overhead.

VERGE incurs significantly higher latency than single-pass generation. Each iteration requires claim decomposition, multiple formalization attempts (K=3K=3), consensus computation, SMT solver calls, and feedback generation. For problems with n>20n>20 atomic claims, the pipeline requires 15-30 seconds per iteration compared to >2>2 seconds for standard Chain-of-Thought prompting. While our greedy MCS approximation reduces complexity from exponential O⁡(2n)O(2^{n}) to linear O⁡(n×SAT)O(n\times\text{SAT}), the multiplicative overhead remains substantial. This latency-accuracy trade-off limits deployment in interactive applications requiring sub-second response times (e.g., conversational AI, real-time decision support).

##### Formalization Barrier and Access Inequality.

Our analysis reveals models under 20B parameters achieve only ∼\sim30% formalization validity, restricting the solver to syntax checking rather than semantic verification. This creates a capability threshold where only organizations with access to frontier models (≥\geq70B parameters) can leverage VERGE’s full potential. Additionally, restricting to decidable logics (QF-UF, LIA) sacrifices expressiveness claims requiring universal quantification, non-linear arithmetic, or recursive definitions cannot be formally verified and must fall back to soft verification. This undermines the framework’s promise of provability for complex mathematical or algorithmic reasoning.

## 7 Ethical Considerations

##### Logical Correctness is not Ethical Correctness.

VERGE verifies internal consistency and logical entailment, not moral soundness or factual truth. The system could formally prove harmful reasoning—discriminatory policies that satisfy legal constraints, exploit chains in cybersecurity, or conspiracy theories with internally consistent logic but false premises. SMT solvers are fundamentally value-neutral tools. Deploying VERGE in high-stakes domains (legal, medical, military decision-making) requires additional ethical oversight layers: premise provenance tracking, factuality verification orthogonal to logic, and human expert review for consequential decisions.

##### Risk of Overconfidence and Misplaced Trust.

Labeling outputs as "verified" may induce false confidence in users unfamiliar with the distinction between formal and soft verification. Our scoring system assigns high scores (0.9) to soft-verified commonsense claims that lack mathematical guarantees. More critically, if autoformalization misrepresents a claim’s semantics producing syntactically valid but semantically incorrect SMT code the solver verifies the wrong statement, creating "verified hallucinations." Users may over-rely on verification badges without understanding rigor gradations. Clear interface design distinguishing "formally proven" (σE\sigma_{E}) from "consensus-supported" (νS\nu_{S}) claims is essential but insufficient if users lack technical literacy.

## References

  * Anthropic (2025) Anthropic Introducing Claude Opus 4.5.  Note: Accessed: 2025-12-19 External Links: [Link](https://www.anthropic.com/news/claude-opus-4-5) Cited by: §1. 
  * Austin et al. (2021) J. Austin, A. Odena, M. Nye, M. Bosma, H. Michalewski, D. Dohan, E. Jiang, C. Cai, M. Terry, Q. Le, et al. Program synthesis with large language models.  arXiv preprint arXiv:2108.07732.  Cited by: §1. 
  * Azerbayev et al. (2023) Z. Azerbayev, B. Piotrowski, H. Schoelkopf, E. W. Ayers, D. Radev, and J. Avigad ProofNet: autoformalizing and formally proving undergraduate-level mathematics.  arXiv preprint arXiv:2302.12433.  Cited by: §2. 
  * Bacchus and Katsirelos (2016) F. Bacchus and G. Katsirelos Finding a collection of muses incrementally.  In Integration of AI and OR Techniques in Constraint Programming, C. Quimper (Ed.),  Cham, pp. 35–44.  External Links: ISBN 978-3-319-33954-2 Cited by: item 2, §2. 
  * Barrett et al. (2009) C. Barrett, R. Sebastiani, S. A. Seshia, and C. Tinelli Satisfiability modulo theories.  In Handbook of Satisfiability,  Vol. 185, pp. 825–885.  Cited by: §1, §2. 
  * Berant et al. (2013) J. Berant, A. Chou, R. Frostig, and P. Liang Semantic parsing on Freebase from question-answer pairs.  In Proceedings of the 2013 Conference on Empirical Methods in Natural Language Processing,  pp. 1533–1544.  Cited by: §2. 
  * Callewaert et al. (2025) B. Callewaert, S. Vandevelde, and J. Vennekens Verus-lm: a versatile framework for combining llms with symbolic reasoning.  arXiv preprint arXiv:2501.14540.  Cited by: §1, §2. 
  * Chen et al. (2021) M. Chen, J. Tworek, H. Jun, Q. Yuan, H. P. d. O. Pinto, J. Kaplan, H. Edwards, Y. Burda, N. Joseph, G. Brockman, et al. Evaluating large language models trained on code.  arXiv preprint arXiv:2107.03374.  Cited by: §1. 
  * Chen et al. (2025) W. Chen, V. Singh, Z. Rahmani, D. Ganguly, M. Hariri, and V. Chaudhary K4: online log anomaly detection via unsupervised typicality learning.  In 2025 IEEE 32nd International Conference on High Performance Computing, Data, and Analytics (HiPC),  Vol. , pp. 96–107.  External Links: [Document](https://dx.doi.org/10.1109/HiPC66333.2025.00019) Cited by: §2. 
  * Church (1936) A. Church An unsolvable problem of elementary number theory.  American Journal of Mathematics 58 (2), pp. 345–363.  Cited by: §1, §2. 
  * De Moura and Bjørner (2008) L. De Moura and N. Bjørner Z3: an efficient SMT solver.  In International Conference on Tools and Algorithms for the Construction and Analysis of Systems,  pp. 337–340.  Cited by: §1, §2. 
  * Dong and Lapata (2016) L. Dong and M. Lapata Language to logical form with neural attention.  In Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics,  Vol. 1, pp. 33–43.  Cited by: §1, §2. 
  * Du et al. (2023) Y. Du, S. Li, A. Torralba, J. B. Tenenbaum, and I. Mordatch Improving factuality and reasoning in language models through multiagent debate.  arXiv preprint arXiv:2305.14325.  Cited by: §1, §2. 
  * Feng et al. (2025) Y. Feng, N. Weir, K. Bostrom, S. Bayless, D. Cassel, S. Chaudhary, B. Kiesl-Reiter, and H. Rangwala VeriCoT: neuro-symbolic chain-of-thought validation via logical consistency checks.  arXiv preprint arXiv:2511.04662.  Cited by: §1. 
  * Ganguly et al. (2024) D. Ganguly, S. Iyengar, V. Chaudhary, and S. Kalyanaraman PROOF OF THOUGHT : neurosymbolic program synthesis allows robust and interpretable reasoning.  In The First Workshop on System-2 Reasoning at Scale, NeurIPS’24,  External Links: [Link](https://openreview.net/forum?id=Pxx3r14j3U) Cited by: §1, §2. 
  * Ganguly et al. (2026) D. Ganguly, S. Sankar, B. Zhang, V. Singh, K. Gupta, H. Kavuru, A. Luo, W. Chen, W. Morningstar, R. Machiraju, and V. Chaudhary Trust the typical.  External Links: 2602.04581, [Link](https://arxiv.org/abs/2602.04581) Cited by: §2. 
  * Ganguly et al. (2025) D. Ganguly, V. Singh, S. Sankar, B. Zhang, X. Zhang, S. Iyengar, X. Han, A. Sharma, S. Kalyanaraman, and V. Chaudhary Grammars of formal uncertainty: when to trust LLMs in automated reasoning tasks.  In The Thirty-ninth Annual Conference on Neural Information Processing Systems,  External Links: [Link](https://openreview.net/forum?id=QfKpJ00t2L) Cited by: §1. 
  * Garcez et al. (2019) A. d. Garcez, M. Gori, L. C. Lamb, L. Serafini, M. Spranger, and S. N. Tran Neural-symbolic computing: an effective methodology for principled integration of machine learning and reasoning.  Journal of Applied Logics 6 (4), pp. 611–632.  Cited by: §1, §2. 
  * Gou et al. (2024) Z. Gou, Z. Shao, Y. Gong, Y. Shen, Y. Yang, N. Duan, and W. Chen CRITIC: large language models can self-correct with tool-interactive critiquing.  In International Conference on Learning Representations (ICLR),  Cited by: §2. 
  * Han et al. (2024) S. Han, H. Schoelkopf, Y. Zhao, Z. Qi, M. Riddell, W. Zhou, J. Coady, D. Peng, Y. Qiao, L. Benson, et al. Folio: natural language reasoning with first-order logic.  In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing,  pp. 22017–22031.  Cited by: §E.6. 
  * Hendrycks et al. (2021) D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and J. Steinhardt Measuring mathematical problem solving with the MATH dataset.  Advances in Neural Information Processing Systems 34, pp. 6901–6914.  Cited by: §1. 
  * Huang et al. (2023) J. Huang, X. Chen, S. Mishra, H. S. Zheng, A. W. Yu, X. Song, and D. Zhou Large language models cannot self-correct reasoning yet.  arXiv preprint arXiv:2310.01798.  Cited by: §2. 
  * Jiang et al. (2022) A. Q. Jiang, S. Welleck, J. P. Zhou, W. Li, J. Liu, M. Jamnik, T. Lacroix, Y. Wu, and G. Lample Draft, sketch, and prove: guiding formal theorem provers with informal proofs.  arXiv preprint arXiv:2210.12283.  Cited by: §2. 
  * Kamoi et al. (2024) R. Kamoi, Y. Zhang, N. Zhang, J. Han, and R. Zhang When can llms actually correct their own mistakes? a critical survey of self-correction of llms.  Transactions of the Association for Computational Linguistics 12, pp. 1417–1440.  Cited by: §2. 
  * Kautz (2022) H. Kautz The third AI summer: AAAI Robert S. Engelmore memorial lecture.  AI Magazine 43 (1), pp. 105–125.  Cited by: §2. 
  * Kazemi et al. (2025) M. Kazemi, B. Fatemi, H. Bansal, J. Palowitch, C. Anastasiou, S. V. Mehta, L. K. Jain, V. Aglietti, D. Jindal, Y. P. Chen, et al. Big-bench extra hard.  In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers),  pp. 26473–26501.  Cited by: §E.6. 
  * Lewkowycz et al. (2022) A. Lewkowycz, A. Andreassen, D. Dohan, E. Dyer, H. Michalewski, V. Ramasesh, A. Slone, C. Anil, I. Schlag, T. Gutman-Solo, et al. Solving quantitative reasoning problems with language models.  In Advances in Neural Information Processing Systems,  Vol. 35, pp. 3843–3857.  Cited by: §1. 
  * Liang et
