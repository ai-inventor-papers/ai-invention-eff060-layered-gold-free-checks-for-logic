URL: https://arxiv.org/html/2410.08047v2 | FULL FETCH | 2026-09-24T01:42:24Z
warning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
URL: https://arxiv.org/html/2410.08047v2
Type: HTML
Length: 100561 chars (truncated)

--- Content ---

##### Report GitHub Issue

×

Title:

Content selection saved. Describe the issue below:

Description:

Submit without GitHub Submit in GitHub

arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[ Back to arXiv ](/)

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) Report Issue [ Back to Abstract ](/abs/2410.08047v2 "Back to abstract page") [ Download PDF](/pdf/2410.08047v2 "Download PDF") [ ](javascript:toggleNavTOC\(\); "Toggle navigation") [ ](javascript:toggleReadingMode\(\); "Disable reading mode, show header and footer")

  1. Abstract
  2. 1 Introduction
  3. 2 Problem Formulation
     1. Prior works.
     2. First-order logic translation.
     3. SAT problem solving.
  4. 3 CLOVER
     1. 3.1 Logical Dependency Structures
     2. 3.2 Compositional First-Order Logic Translation
        1. Logical Dependency Parsing.
        2. Component Accumulation.
        3. Sequential Translation.
     3. 3.3 First-Order Logic Verification
        1. Logical Consistency.
        2. Disproving by Counter-Interpretation.
  5. 4 Experiments
     1. 4.1 Setup
        1. Tasks.
        2. Language Models.
        3. Baselines.
        4. Evaluation metrics.
     2. 4.2 Results
     3. 4.3 Ablations
     4. 4.4 Analysis
        1. Types of Errors.
        2. Robustness on Reasoning Length.
  6. 5 Related Works
     1. LLM-based neurosymbolic approach for reasoning.
     2. LLM-based problem decomposition.
     3. LLM-generated formal language verification.
  7. 6 Conclusion
  8. 7 Acknowledgments
  9. References
  10. A First-Order Logic Preliminaries
     1. A.1 Syntax
     2. A.2 Semantics
  11. B First-Order Logic Complexity
  12. C Component Accumulation Rules
  13. D Examples of Logical Dependency Parsing and Component Accumulation
  14. E SAT Solver Function Prediction on AR-LSAT
  15. F Dataset Statistics
     1. AR-LSAT-annotated.
     2. ZebraLogic.
     3. Puzzle.
     4. Symbol.
     5. Deduction.
     6. ProofWriter.
  16. G Performance on Different Language Models
  17. H Inference Time Costs
  18. I Impact of SAT-based First-Order Logic Verification
  19. J Few-shot Prompt Examples
  20. K Extensive Error Analysis of Logic-LM



[ License: arXiv.org perpetual non-exclusive license ](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2410.08047v2 [cs.CL] 25 Feb 2025

#  Divide and Translate: Compositional First-Order Logic Translation and Verification for Complex Logical Reasoning 

Hyun Ryu Gyeongman Kim Hyemin S. Lee Eunho Yang  Affiliation: KAIST MIT{ryuhyun1905,gmkim,eunhoy}@kaist.ac.kr, hmstella@mit.edu

###### Abstract

Complex logical reasoning tasks require a long sequence of reasoning, which a large language model (LLM) with chain-of-thought prompting still falls short. To alleviate this issue, neurosymbolic approaches incorporate a symbolic solver. Specifically, an LLM only translates a natural language problem into a satisfiability (SAT) problem that consists of first-order logic formulas, and a sound symbolic solver returns a mathematically correct solution. However, we discover that LLMs have difficulties to capture complex logical semantics hidden in the natural language during translation. To resolve this limitation, we propose a Compositional First-Order Logic Translation. An LLM first parses a natural language sentence into newly defined logical dependency structures that consist of an atomic subsentence and its dependents, then sequentially translate the parsed subsentences. Since multiple logical dependency structures and sequential translations are possible for a single sentence, we also introduce two Verification algorithms to ensure more reliable results. We utilize an SAT solver to rigorously compare semantics of generated first-order logic formulas and select the most probable one. We evaluate the proposed method, dubbed CLOVER, on seven logical reasoning benchmarks and show that it outperforms the previous neurosymbolic approaches and achieves new state-of-the-art results.11 1 The source code used in the paper is available at <https://github.com/Hyun-Ryu/clover>.  
  
---  
  
## 1 Introduction

Logical reasoning involves reaching conclusions through a structured process. It entails drawing inferences by converting information provided in a set of premises into a final conclusion (Nunes, 2012; Bronkhorst et al., 2020). Logical reasoning ability is one of the most challenging metrics to measure intelligence. As a model size grows exponentially, large language models (LLMs) (Brown et al., 2020; Chen et al., 2021; Thoppilan et al., 2022) unlock the ability of machine to reason.

Chain-of-thought (CoT) prompting (Wei et al., 2022) significantly improve the performance of LLMs on simple logical reasoning tasks that require few forward reasoning steps. However, CoT falls short in complex logical reasoning tasks which need longer sequence of reasoning (Ye et al., 2024; Pan et al., 2023). To resolve this issue, several neurosymbolic approaches (Ye et al., 2024; Pan et al., 2023; Kirtania et al., 2024; Olausson et al., 2023) utilize an LLM with a symbolic solver (e.g., an SAT solver) on these complex logical reasoning tasks by the following two steps: 1) an LLM translates the natural language logical reasoning problem into a set of first-order logic formulas, 2) a symbolic solver automatically plans the reasoning steps and executes those to predict an answer of the logical reasoning problem. These approaches take advantages by considering an LLM only as a semantic parser (i.e., a first-order logic translator), which can avoid planning and execution errors by using a symbolic solver.

(a) 

(b) 

Figure 1:  Comparison of a first-order logic translation of the proposed CLOVER and Logic-LM with gpt-4o on AR-LSAT. (a) Translation accuracy at different levels of first-order logic complexity. We group the formulas in one of five complexity ranges and report the averaged performance for each range. (b) A representative example. Given declarations of sorts and functions, each method translates the natural language sentence into the corresponding first-order logic formula. We colorize incorrect translation as red for visualization purpose. 

However, we have discovered that LLMs still cannot translate sentences that represent complex first-order logic. Our experimental evidence in Fig. 1(a) presents the drastic performance drop of the previous work (Pan et al., 2023) on complex first-order logic translation.22 2 To evaluate the complexity and performance of each first-order logic formula, we sample the first problem from each set of problems that share the same context in the AR-LSAT test set and manually annotate the ground truth formulas. Detailed information of measuring complexity is in Appendix B and the process of the annotated subset construction is described in Appendix F. The result indicates that an LLM performs first-order logic translation faithfully to a certain degree of complexity but falls short beyond that limit. A representative example in Fig. 1(b) presents an incorrect output of the previous work (Pan et al., 2023) on complex first-order logic translation. The task is to translate a sentence “The Sales division is toured on two consecutive days, and on no other days.” into a corresponding first-order logic formula given declarations. An LLM correctly translates a natural language clause “The Sales division is toured on two consecutive days.” into a subformula (∃d:days)​(toured​(d)=Sales)∧(toured​(d+1)=Sales)(\exists d:\textit{days})\,(\textit{toured}(d)=\textit{Sales})\land(\textit{toured}(d+1)=\textit{Sales}) which contains simple logic, but fails to translate “and on no other days” which represents more complex logic. Specifically, the incorrectly translated subformula is always true, which has no semantic meaning. After further extensive qualitative error analysis (Appendix K), we conclude that LLMs show promising performance on simple first-order logic translations but does not on complex ones, and the reason is that LLMs have difficulties to discover complex logical structures hidden behind the natural language.

To resolve this limitation, we take a hint from how humans perceive a complex logical sentence to their mind and how they translate it to a first-order logic formula. Since it is hard to immediately comprehend the semantics of a complex logical sentence, humans first understand the semantics of a simpler subsentence and then understand the whole (Montague et al., 1970; Frazier & Fodor, 1978; Sweller, 1988). Inspired by this observation, we use LLM to find the atomic subsentence that does not contain any complex logic and understand other sentence components as dependents of the atomic subsentence. Then, starting with the atomic subsentence, we use LLM to translate subsentences by accumulating sentence components. This could help LLM to preserve first-order logic semantics during translation. To rigorously define the atomic subsentence and sentence components with logical meaning, we introduce a new parsing method for natural language that represents first-order logic, called logical dependency parsing (Section 3.1).

Based on logical dependency parsing, we propose a compositional first-order logic translation (Section 3.2) by few-shot learning with an LLM. It consists of the following three steps: logical dependency parsing, component accumulation, and sequential translation. First, a target sentence is parsed into logical dependency structures which consist of components of the sentence and their logical dependencies. Second, components are accumulated while preserving their logical dependencies, where the last accumulated sentence is the target sentence. Finally, each accumulated sentence is sequentially translated into first-order logic formula in the order of accumulations, where the last formula is an estimated formula of the target sentence.

Not only that, since there could be multiple outputs on logical dependency parsing and sequential translation, we introduce verification algorithms to ensure more reliable first-order logic translation (Section 3.3). We propose two verification algorithms: logical consistency and disproving by counter-interpretation. To fully leverage the deterministic nature of first-order logic, we use an SAT solver to compare any two formulas. Logical consistency selects the most frequent logically equivalent formulas. However, we observe that an LLM sometimes make logically consistent translation errors. To overcome such a limitation, we devise disproving by counter-interpretation. It sequentially compares two formulas and disprove one of them by determining if a counter-interpretation to equivalence of two formulas satisfies the target sentence. The last formula remained is then selected. To save computational cost, we compare each one of logically equivalent formulas.

We evaluate the proposed CLOVER, a Compositional First-Order Logic Translation and Verification, on seven logical reasoning benchmarks (Section 4). CLOVER outperforms the previous neurosymbolic approaches and achieves the new state-of-the-art performance. It also significantly enhances the first-order logic translation accuracy across all levels of complexity and the largest performance gain occurs at the highest first-order logic complexity (Fig. 1(a)).

To summarize our contributions,

  1. 1.

We introduce CLOVER, a novel neurosymbolic approach that enhances complex logical reasoning in LLMs by compositional translation of natural language into first-order logic and verification of logical semantics.

  2. 2.

We newly define a logical dependency structure to decompose logical sentences while preserving an underlying first-order logic semantics.

  3. 3.

We also propose two SAT-based first-order logic verification algorithms that can faithfully select a correctly translated formula.

  4. 4.

We evaluate CLOVER on seven logical reasoning benchmarks and show that CLOVER outperforms the previous neurosymbolic apporoaches and achieves the new state-of-the-art performance.




## 2 Problem Formulation

Through the lens of (many-sorted) first-order logic33 3 Many-sorted first-order logic is one of the variants of the standard first-order logic that allows variables to have different domains, which is called sorts SS. We provide related preliminaries in Appendix A., a logical reasoning problem xx is a natural language description of a Σ\Sigma-theory 𝒯\mathcal{T}44 4 A theory assigns specific meanings to symbols of formulas. For simplicity, we presume that a theory 𝒯\mathcal{T} incorporates the most commonly applied theories (e.g., theory of equality, arithmetic, etc.)., constraints Φ\Phi, and a query qq, denoted as x=N​L​(𝒯,Φ,q)x=NL(\mathcal{T},\Phi,q). A Σ\Sigma-theory 𝒯\mathcal{T} is a non-empty set of any Σ\Sigma-structure where a signature Σ=(S,F,P)\Sigma=(S,F,P) consists of sorts SS, function symbols FF, and predicate symbols PP. Hereinafter, we denote the vocabulary of first-order logic as italic for clarity, and omit the prefix “Σ\Sigma-” for simplicity. A structure of a theory indicates the semantics of formulas. Constraints Φ\Phi are a set of formulas that are true, denoted as Φ={ϕ1,ϕ2,⋯,ϕK}\Phi=\\{\phi_{1},\phi_{2},\cdots,\phi_{K}\\}. A query qq is also a formula which is yet determined as true, false, or unknown given the constraints Φ\Phi.

#### Prior works.

Prior neurosymbolic approaches (Ye et al., 2024; Pan et al., 2023; Kirtania et al., 2024; Olausson et al., 2023) directly translate the logical reasoning problem xx into a set of first-order logic using an LLM and then employ a symbolic solver (e.g., an SAT solver) to solve an SAT problem. In these methods, an LLM performs a single inference for the first-order logic translation as follows:

| 𝒯^,{φ^k,N​L^(φk)}k=1K+1∼PLLM(𝒯,{φk,NL(φk)}k=1K+1∣x,𝐱fs)\hat{\mathcal{T}},\\{\hat{\varphi}_{k},\hat{NL}(\varphi_{k})\\}_{k=1}^{K+1}\sim P_{\text{LLM}}(\mathcal{T},\\{\varphi_{k},NL(\varphi_{k})\\}_{k=1}^{K+1}\mid x,\mathbf{x}_{\text{fs}}) |  | (1)  
---|---|---|---  
  
where φk=ϕk\varphi_{k}=\phi_{k} for 1≤k≤K1\leq k\leq K and φK+1=q\varphi_{K+1}=q, and a few-shot exemplar set 𝐱fs={x(i),𝒯(i),{φk(i),N​L​(φk(i))}k=1K(i)+1}i=1N\mathbf{x}_{\text{fs}}=\\{x^{(i)},\mathcal{T}^{(i)},\\{\varphi_{k}^{(i)},NL(\varphi_{k}^{(i)})\\}_{k=1}^{K^{(i)}+1}\\}_{i=1}^{N} with the size of the set NN. However, it often generates more than one formulas for a single target sentence or generates a formula which is a translation of combination of a target sentence and part of other sentences. Though it might be logically correct as a whole, we cannot further analyze and verify the translation at a sentence-level.

#### First-order logic translation.

To resolve this drawback, we perform first-order logic translation for each sentence. Since sentence-level translations require a pre-defined theory and target sentences, we first generate a theory 𝒯^\hat{\mathcal{T}} and a set of natural language sentences {N​L^​(φk)}k=1K+1\\{\hat{NL}(\varphi_{k})\\}_{k=1}^{K+1} from xx, and then generate 𝒯^\hat{\mathcal{T}}-satisfiable formula φ^k\hat{\varphi}_{k} for each sentence N​L^​(φk)\hat{NL}(\varphi_{k}). To be specific, the single inference by the LLM in Eq. 1 is separated into the following two steps: 1) given a logical reasoning problem xx and a few-shot exemplar set 𝐱fsprep={x(i),𝒯(i),{N​L​(φk(i))}k=1K(i)+1}i=1N\mathbf{x}_{\text{fs}}^{\text{prep}}=\\{x^{(i)},\mathcal{T}^{(i)},\\{NL(\varphi_{k}^{(i)})\\}_{k=1}^{K^{(i)}+1}\\}_{i=1}^{N}, the LLM generates a tuple of an estimated theory and a set of natural language sentences, denoted xprep=(𝒯^,{N​L^​(φk)}k=1K+1)x^{\text{prep}}=(\hat{\mathcal{T}},\\{\hat{NL}(\varphi_{k})\\}_{k=1}^{K+1}), 2) given the theory 𝒯^\hat{\mathcal{T}} and a set of few-shot exemplar sets 𝐗fs\mathbf{X}_{\text{fs}}, the proposed CLOVER translates each natural language sentence N​L^​(φk)\hat{NL}(\varphi_{k}) into the estimated formula φ^k\hat{\varphi}_{k} that is 𝒯^\hat{\mathcal{T}}-satisfiable as follows:

| 𝒯^,{N​L^​(φk)}k=1K+1\displaystyle\hat{\mathcal{T}},\\{\hat{NL}(\varphi_{k})\\}_{k=1}^{K+1} | ∼PLLM(𝒯,{NL(φk)}k=1K+1∣x,𝐱fsprep)\displaystyle\sim P_{\text{LLM}}(\mathcal{T},\\{NL(\varphi_{k})\\}_{k=1}^{K+1}\mid x,\mathbf{x}_{\text{fs}}^{\text{prep}}) |  | (2)  
---|---|---|---|---  
| φ^k\displaystyle\hat{\varphi}_{k} | =CLOVER(𝒯^,N​L^(φk),𝐗fs),∀k∈{1,2,⋯,K+1}.\displaystyle=\text{CLOVER}(\hat{\mathcal{T}},\hat{NL}(\varphi_{k}),\mathbf{X}_{\text{fs}}),\forall{k}\in\\{1,2,\cdots,K+1\\}. |   
  
A detailed description of the set of few-shot exemplar sets 𝐗fs={𝐱fsparse,𝐱fsaccum,𝐱fstrans,𝐱fsdisprv}\mathbf{X}_{\text{fs}}=\\{\mathbf{x}_{\text{fs}}^{\text{parse}},\mathbf{x}_{\text{fs}}^{\text{accum}},\mathbf{x}_{\text{fs}}^{\text{trans}},\mathbf{x}_{\text{fs}}^{\text{disprv}}\\} and the proposed CLOVER for xprep=(𝒯^,{N​L^​(φk)}k=1K+1)x^{\text{prep}}=(\hat{\mathcal{T}},\\{\hat{NL}(\varphi_{k})\\}_{k=1}^{K+1}) will be discussed in the following section.

#### SAT problem solving.

Once estimations of the theory 𝒯^\hat{\mathcal{T}}, constraints Φ^={φ^1,φ^2,⋯,φ^K}\hat{\Phi}=\\{\hat{\varphi}_{1},\hat{\varphi}_{2},\cdots,\hat{\varphi}_{K}\\}, and a query q^=φ^K+1\hat{q}=\hat{\varphi}_{K+1} are completed for the logical reasoning problem xx, these form an SAT problem 𝒫=(𝒯^,Φ^,q^)\mathcal{P}=(\hat{\mathcal{T}},\hat{\Phi},\hat{q}). An automated SAT solver then determines the 𝒯^\hat{\mathcal{T}}-satisfiability55 5 For AR-LSAT, we need to check the 𝒯^\hat{\mathcal{T}}-validity depending on the problem. More details in Appendix E. of the query q^\hat{q} under the constraints Φ^\hat{\Phi}, which is a final prediction of an answer of the logical reasoning problem xx. We use a Z3 theorem prover (De Moura & Bjørner, 2008) as an SAT solver in the implementation.

## 3 CLOVER

Figure 2:  Overview of CLOVER. Given declarations of a theory, CLOVER parses a target sentence to several possible logical dependency structures, accumulates components according to logical dependencies, and sequentially translates subsentences to first-order logic formulas. Then, CLOVER verifies a set of estimated formulas. Logical consistency selects the most frequent logically equivalent formulas. Disproving by counter-interpretation sequentially compares two formulas and disprove one by determining if a counter-interpretation satisfies the target sentence. 

In this section, we propose CLOVER, a Compositional First-Order Logic Translation and Verification for complex logical reasoning. To fully capture first-order logic semantics in natural language, it first parses a single natural language sentence into logical dependency structures. Then, it sequentially translates parsed subsentences with an LLM. Since there are multiple ways to parse and translate the sentences, we also introduce two SAT-based verification algorithms to thoroughly compare semantics of translated first-order logic formulas.

### 3.1 Logical Dependency Structures

Logical dependency structure 𝒜\mathcal{A} of a sentence N​L​(φ)NL(\varphi) under the theory 𝒯\mathcal{T} where φ\varphi is 𝒯\mathcal{T}-satisfiable is defined by components and their logical dependencies. First, components are natural language building blocks of logical dependency structures of a sentence, which consist of logic units UU, logic couplers CC, and logic dependents DD. The following definitions formally describe each of them.

###### Definition 1 (Logic units).

Given a sentence N​L​(φ)NL(\varphi) and a theory 𝒯\mathcal{T} where φ\varphi is 𝒯\mathcal{T}-satisfiable, logic units UU are the natural language descriptions of an atom of φ\varphi.

###### Definition 2 (Logic couplers).

Logic couplers CC are either conjunctions or an operator named merge. Merge combines two logic units which contain the natural language describing the same term without adding any conjunction.

###### Definition 3 (Logic dependents).

Logic dependents DD are components neither logic units nor logic couplers which logically depend on another component.

Second, we define logical dependency between two components, and the following definition formally describes it.

###### Definition 4 (Logical dependency).

The component XX is said to logically depend on the component YY in the given sentence if and only if the meaning of YY is (or includes) a predicate and the meaning of XX is an argument of this predicate in the sentence.

We also introduce properties of logical dependency structure stemmed from its definition.

###### Remark 1.

A given sentence and theory can have multiple logical dependency structures.

###### Remark 2.

All components except for one should logically depend on another component.

###### Remark 3.

No logic dependent logically depends on a logic coupler.

We present examples of logical dependency structures in Fig. 2 and in Appendix D.

### 3.2 Compositional First-Order Logic Translation

To compositionally translate natural language sentences to first-order logic formulas under given theory for xprep=(𝒯^,{N​L^​(φk)}k=1K+1)x^{\text{prep}}=(\hat{\mathcal{T}},\\{\hat{NL}(\varphi_{k})\\}_{k=1}^{K+1}), we adhere to the following three steps by few-shot learning with an LLM. We describe the following steps for a single target sentence N​L^​(φ)\hat{NL}(\varphi) of a formula φ∈{φk}k=1K+1\varphi\in\\{\varphi_{k}\\}_{k=1}^{K+1}.

#### Logical Dependency Parsing.

In the first step, a target sentence is parsed into different possible logical dependency structures. An LLM is given a definition of logical dependency structures (Section 3.1), a target sentence N​L^​(φ)\hat{NL}(\varphi) and its theory 𝒯^\hat{\mathcal{T}}, and a few-shot exemplar set 𝐱fsparse={𝒯(i),N​L​(φ(i)),{𝒜l(i)}l=1L(i)}i=1N\mathbf{x}_{\text{fs}}^{\text{parse}}=\\{\mathcal{T}^{(i)},NL(\varphi^{(i)}),\\{\mathcal{A}^{(i)}_{l}\\}_{l=1}^{L^{(i)}}\\}_{i=1}^{N} for logical dependency parsing. L(i)L^{(i)} is a size of a set of different possible logical dependency structures of a sentence N​L​(φ(i))NL(\varphi^{(i)}) under the theory 𝒯(i)\mathcal{T}^{(i)}, and NN is a size of the few-shot exemplar set. Then, LLM generates a set of different possible logical dependency structures {𝒜^l}l=1L^\\{\hat{\mathcal{A}}_{l}\\}_{l=1}^{\hat{L}} of the target sentence with the size of the set L^\hat{L} as follows:

| L^,{𝒜^l}l=1L^∼PLLM(L,{𝒜l}l=1L∣𝒯^,N​L^(φ),𝐱fsparse).\displaystyle\hat{L},\\{\hat{\mathcal{A}}_{l}\\}_{l=1}^{\hat{L}}\sim P_{\text{LLM}}(L,\\{\mathcal{A}_{l}\\}_{l=1}^{L}\mid\hat{\mathcal{T}},\hat{NL}(\varphi),\mathbf{x}_{\text{fs}}^{\text{parse}}). |  | (3)  
---|---|---|---  
  
#### Component Accumulation.

In the second step, components of a logical dependency structure are accumulated to gradually compose new sentences until those reach the target sentence. We present the rules for component accumulation in Appendix C. An LLM is given a definition of logical dependency structures (Section 3.1), rules for component accumulation (Appendix C), a target sentence N​L^​(φ)\hat{NL}(\varphi) and one of its logical dependency structures 𝒜^l\hat{\mathcal{A}}_{l} where l∈{1,2,⋯,L^}l\in\\{1,2,\cdots,\hat{L}\\}, and a few-shot exemplar set 𝐱fsaccum={N​L​(φ(i)),𝒜(i),(Sm(i))m=1M(i)}i=1N\mathbf{x}_{\text{fs}}^{\text{accum}}=\\{NL(\varphi^{(i)}),\mathcal{A}^{(i)},(S^{(i)}_{m})_{m=1}^{M^{(i)}}\\}_{i=1}^{N} for component accumulation. (Sm(i))m=1M(i)(S^{(i)}_{m})_{m=1}^{M^{(i)}} is a sequence of accumulated sentences where M(i)M^{(i)} is the length of the sequence. Then, LLM generates a sequence of sentences (S^l,m)m=1M^l(\hat{S}_{l,m})_{m=1}^{\hat{M}_{l}} where M^l\hat{M}_{l} is the length of the estimated sequence as follows:

| M^l,(S^l,m)m=1M^l∼PLLM(Ml,(Sl,m)m=1Ml∣N​L^(φ),𝒜^l,𝐱fsaccum),∀l∈{1,2,⋯,L^}.\displaystyle\hat{M}_{l},(\hat{S}_{l,m})_{m=1}^{\hat{M}_{l}}\sim P_{\text{LLM}}(M_{l},(S_{l,m})_{m=1}^{M_{l}}\mid\hat{NL}(\varphi),\hat{\mathcal{A}}_{l},\mathbf{x}_{\text{fs}}^{\text{accum}}),\forall l\in\\{1,2,\cdots,\hat{L}\\}. |  | (4)  
---|---|---|---  
  
The last sentence of accumulation S^l,M^l\hat{S}_{l,\hat{M}_{l}} is the target sentence N​L^​(φ)\hat{NL}(\varphi). We present examples of component accumulation in Appendix D.

#### Sequential Translation.

In the last step, accumulated natural language sentences are sequentially translated into first-order logic formulas, which the target sentence is finally translated. An LLM is given a sequence of accumulated sentences (S^l,m)m=1M^l(\hat{S}_{l,m})_{m=1}^{\hat{M}_{l}} of a target sentence where l∈{1,2,⋯,L^}l\in\\{1,2,\cdots,\hat{L}\\}, a theory 𝒯^\hat{\mathcal{T}}, and a few-shot exemplar set 𝐱fstrans={𝒯(i),(Sm(i))m=1M(i),(φm(i))m=1M(i)}i=1N\mathbf{x}_{\text{fs}}^{\text{trans}}=\\{\mathcal{T}^{(i)},(S^{(i)}_{m})_{m=1}^{M^{(i)}},(\varphi^{(i)}_{m})_{m=1}^{M^{(i)}}\\}_{i=1}^{N} for first-order logic translation. Then, LLM generates a sequence of formulas (φ^l,m)m=1M^l(\hat{\varphi}_{l,m})_{m=1}^{\hat{M}_{l}} as follows:

| (φ^l,m)m=1M^l∼PLLM((φl,m)m=1M^l∣𝒯^,(S^l,m)m=1M^l,𝐱fstrans),∀l∈{1,2,⋯,L^}.\displaystyle(\hat{\varphi}_{l,m})_{m=1}^{\hat{M}_{l}}\sim P_{\text{LLM}}((\varphi_{l,m})_{m=1}^{\hat{M}_{l}}\mid\hat{\mathcal{T}},(\hat{S}_{l,m})_{m=1}^{\hat{M}_{l}},\mathbf{x}_{\text{fs}}^{\text{trans}}),\forall l\in\\{1,2,\cdots,\hat{L}\\}. |  | (5)  
---|---|---|---  
  
The last formula of the sequence is the first-order logic translation of the target sentence (i.e., φ^l=φ^l,M^l\hat{\varphi}_{l}=\hat{\varphi}_{l,\hat{M}_{l}}). For ∀l∈{1,2,⋯,L^}\forall l\in\\{1,2,\cdots,\hat{L}\\}, we could generate a set of estimated formulas Ψ^={φ^l}l=1L^\hat{\Psi}=\\{\hat{\varphi}_{l}\\}_{l=1}^{\hat{L}} for a target sentence N​L^​(φ)\hat{NL}(\varphi). In practice, we randomly sample multiple times to enrich the pool of estimated formulas that benefits the second stage of CLOVER, first-order logic verification.

### 3.3 First-Order Logic Verification

To select the most probable formula in a set of compositionally translated first-order logic formulas Ψ^\hat{\Psi}, we introduce the following two algorithms using an SAT solver (and few-shot learning with an LLM). As in Section 3.2, we describe the following algorithms for a single target sentence N​L^​(φ)\hat{NL}(\varphi) under the theory 𝒯^\hat{\mathcal{T}} (i.e., The algorithms select a verified formula φ∗\varphi^{*} in a set of estimated formulas Ψ^\hat{\Psi}). Prior to describing the detailed algorithms, we filter out the formulas that are syntactically incorrect or 𝒯^\hat{\mathcal{T}}-unsatisfiable in Ψ^\hat{\Psi} using an SAT solver and call the processed set Ψ^sat\hat{\Psi}_{\text{sat}}.

#### Logical Consistency.

We select the most frequent logically equivalent formulas, which we call this algorithm logical consistency. It presumes an LLM utilizes different logical dependency structures to generate several formulas that are logically equivalent. An LLM might also make mistake in intermediate steps of compositional first-order logic translation and generate incorrect formulas, but these are less likely to be logically equivalent. For each pair of formulas (φp,φq)(\varphi_{p},\varphi_{q}) such that φp∈Ψ^sat\varphi_{p}\in\hat{\Psi}_{\text{sat}}, φq∈Ψ^sat\varphi_{q}\in\hat{\Psi}_{\text{sat}}, and p≠qp\neq q, an SAT solver determines their 𝒯^\hat{\mathcal{T}}-equivalence. Then, we group 𝒯^\hat{\mathcal{T}}-equivalent formulas and select any formula in the group that has the largest number of elements. However, we observe that an LLM sometimes makes consistent mistakes in the last step of compositional first-order logic translation, which leads to logically equivalent incorrect formulas.

#### Disproving by Counter-Interpretation.

To resolve this issue, we introduce an advanced algorithm that sequentially disproves incorrect formulas by counter-interpretation. Following this algorithm, an accurate formula remains the last if it exists in Ψ^sat\hat{\Psi}_{\text{sat}}. Specifically, we select a random element φ^0\hat{\varphi}_{0} in Ψ^sat\hat{\Psi}_{\text{sat}} and initialize the verified formula φ∗\varphi^{*} to φ^0\hat{\varphi}_{0}. For each estimated formula φ^\hat{\varphi} in Ψ^sat∖{φ^0}\hat{\Psi}_{\text{sat}}\setminus\\{\hat{\varphi}_{0}\\}, an SAT solver determines if (φ∗∧¬φ^)(\varphi^{*}\land\lnot\hat{\varphi}) is 𝒯^\hat{\mathcal{T}}-satisfiable. First, if it is 𝒯^\hat{\mathcal{T}}-satisfiable, an SAT solver finds a counter-interpretation II to a 𝒯^\hat{\mathcal{T}}-equivalence of φ∗\varphi^{*} and φ^\hat{\varphi} that satisfies (φ∗∧¬φ^)(\varphi^{*}\land\lnot\hat{\varphi}). Given a target sentence N​L^​(φ)\hat{NL}(\varphi), a counter-interpretation II, and a few-shot exemplar set 𝐱fsdisprv={N​L​(φ)(i),I(i),e(i)}i=1N\mathbf{x}_{\text{fs}}^{\text{disprv}}=\\{NL(\varphi)^{(i)},I^{(i)},e^{(i)}\\}_{i=1}^{N} for disproving, an LLM decides if II satisfies φ\varphi, which returns a boolean value e^\hat{e}. If e^\hat{e} is True, then φ^\hat{\varphi} is disproved since II does not satisfy φ^\hat{\varphi} but satisfies φ\varphi. If e^\hat{e} is False, then φ∗\varphi^{*} is disproved since II satisfies φ∗\varphi^{*} but does not satisfy φ\varphi. Second, if (φ∗∧¬φ^)(\varphi^{*}\land\lnot\hat{\varphi}) is 𝒯^\hat{\mathcal{T}}-unsatisfiable, it is equivalent to (φ∗→φ^)(\varphi^{*}\rightarrow\hat{\varphi}) is 𝒯^\hat{\mathcal{T}}-satisfiable, and no II exists. After repeating this decision process for (φ^∧¬φ∗)(\hat{\varphi}\land\lnot\varphi^{*}), we can consider a counter-interpretation II that satisfies (φ^∧¬φ∗)(\hat{\varphi}\land\lnot\varphi^{*}) and disproves accordingly. We select the verified formula φ∗\varphi^{*} that remains the last. Algorithm 1 summarizes the whole process.

Algorithm 1 First-Order Logic Verification (Disproving by Counter-Interpretation)

Input: Theory 𝒯\mathcal{T}, a natural language sentence N​L​(φ)NL(\varphi) of a first-order logic formula φ\varphi, and a set of estimated 𝒯\mathcal{T}-satisfiable formulas Ψ^sat\hat{\Psi}_{\text{sat}}

Output: Verified formula φ∗\varphi^{*}

φ^0∼Ψ^s​a​t\hat{\varphi}_{0}\sim\hat{\Psi}_{sat} ⊳\triangleright Select an element φ^0\hat{\varphi}_{0} in Ψ^s​a​t\hat{\Psi}_{sat} randomly

φ∗←φ^0\varphi^{*}\leftarrow\hat{\varphi}_{0} ⊳\triangleright Initialize φ∗\varphi^{*} to a random element φ^0\hat{\varphi}_{0}

for each φ^∈Ψ^s​a​t∖{φ^0}\hat{\varphi}\in\hat{\Psi}_{sat}\setminus\\{\hat{\varphi}_{0}\\} do

φtemp←φ∗\varphi_{\text{temp}}\leftarrow\varphi^{*} ⊳\triangleright Use a temporary variable φtemp\varphi_{\text{temp}} for the update

for each (φp,φq)∈{(φ∗,φ^),(φ^,φ∗)}(\varphi_{p},\varphi_{q})\in\\{(\varphi^{*},\hat{\varphi}),(\hat{\varphi},\varphi^{*})\\} do

if (φp∧¬φq)(\varphi_{p}\land\lnot\varphi_{q}) is 𝒯\mathcal{T}-satisfiable then

find 𝒯\mathcal{T}-interpretation II such that I⊨(φp∧¬φq)I\vDash(\varphi_{p}\land\lnot\varphi_{q}) ⊳\triangleright SAT solver finds II if it exists

e^∼PL​L​M​(e∣N​L​(φ),I,𝐱f​sd​i​s​p​r​v),e∈{⊤,⊥}\hat{e}\sim P_{LLM}(e\mid NL(\varphi),I,\mathbf{x}_{fs}^{disprv}),e\in\\{\top,\bot\\} ⊳\triangleright LLM determines if I⊨φI\vDash\varphi

if (φp=φ∗∧¬e^)(\varphi_{p}=\varphi^{*}\land\lnot\hat{e}) or (φp=φ^∧e^)(\varphi_{p}=\hat{\varphi}\land\hat{e}) then

φtemp←φ^\varphi_{\text{temp}}\leftarrow\hat{\varphi}

end if

end if

end for

φ∗←φtemp\varphi^{*}\leftarrow\varphi_{\text{temp}} ⊳\triangleright Update φ∗\varphi^{*} after checking 𝒯\mathcal{T}-interpretations from both side

end for

return φ∗\varphi^{*}

## 4 Experiments

### 4.1 Setup

#### Tasks.

We evaluate CLOVER on seven logical reasoning tasks: AR-LSAT (Zhong et al., 2022), ZebraLogic (Lin et al., 2025), Logic grid puzzle (Puzzle), Symbol interpretation (Symbol), and Logical deduction (Deduction) from the BigBench collaborative benchmark (Srivastava et al., 2022), FOLIO (Han et al., 2022), and ProofWriter (Tafjord et al., 2021). AR-LSAT consists of analytical reasoning problems of the law school admission test, and ZebraLogic is a benchmark for zebra puzzles. Puzzle, Symbol, and Deduction are tasks from logical reasoning category in the BigBench. FOLIO66 6 We use a revised version of FOLIO that improves sample quality and fixes errors, which is released on: <https://huggingface.co/datasets/yale-nlp/FOLIO>. is an expert-written first-order logic reasoning task, and ProofWriter is a deductive reasoning benchmark. Note that all tasks except ZebraLogic are multiple choice problems, and Appendix F describes details of each task.

#### Language Models.

We perform our experiments mainly on gpt-4o (Achiam et al., 2023), a current state-of-the-art LLM for complex, multi-step tasks, unless stated. We also evaluate CLOVER and the baselines using a smaller model, gpt-4o-mini (Achiam et al., 2023).77 7 To specify language model versions provided by OpenAI, we use gpt-4o-2024-05-13 and gpt-4o-mini-2024-07-18 on our experiments. To reproduce our experiments, we set the temperature to 0 and select the highest probability response from the model.

#### Baselines.

We compare CLOVER primarily to Logic-LM (Pan et al., 2023), a state-of-the-art neurosymbolic approach for logical reasoning. There are few more works (Ye et al., 2024; Olausson et al., 2023) nearly the same to Logic-LM, but we focus on Logic-LM since their difference is marginal. We also compare CLOVER to another neurosymbolic approach (Xu et al., 2024) which uses an LLM to solve SAT problems instead of using a symbolic solver. In addition, we compare to the standard prompting and CoT prompting that leverages in-context learning capability of the base LLMs. For fair comparison, we manually sample or derive our few-shot exemplar sets from those in the previous works (Pan et al., 2023; Xu et al., 2024) if it is possible. Since the previous works do not evaluate their models on ZebraLogic, Puzzle, and Symbol, we randomly select a single exemplar problem outside the test set. We demonstrate exemplar few-shot prompts in Appendix J.

#### Evaluation metrics.

We measure the performance of CLOVER and the baselines primarily by the correctness of logical reasoning problems. For neurosymbolic approaches with a symbolic solver, if the solver cannot execute the translated SAT problem, we fall back to CoT predictions. From this unique property, following Pan et al. (2023), we use three additional evaluation metrics: program accuracy, execution rate, and execution accuracy, for multiple choice problems. Program accuracy does not include the CoT predictions for unexecutable problems. Execution rate measures the portion of executable problems, and execution accuracy indicates the accuracy for executable problems.

### 4.2 Results

Table 1: Performance on logical reasoning tasks using CLOVER and the baseline methods.

AR-LSAT ZebraLogic Puzzle Symbol Deduction FOLIO ProofWriter Standard 30.3 0.4 63.0 74.7 84.7 70.9 53.7 CoT 36.8 0.4 51.0 80.8 94.0 73.9 78.0 SymbCoT 34.2 0.8 66.5 55.6 90.7 76.9 80.2 Logic-LM 42.4 45.4 64.0 81.8 95.3 75.4 95.3 CLOVER 62.8 75.4 83.5 89.9 99.3 78.8 96.7

Table 2: Comparison of program accuracy, execution rate, and execution accuracy of CLOVER and Logic-LM.

Program Acc Execution Rate Execution Acc Logic-LM CLOVER Logic-LM CLOVER Logic-LM CLOVER AR-LSAT 17.3 46.8 33.8 59.7 51.3 78.3 Puzzle 60.0 79.0 79.5 80.0 75.5 98.8 Symbol 49.5 76.8 52.5 82.8 94.2 92.7 Deduction 92.7 99.0 97.3 99.7 95.2 99.3 FOLIO 51.2 62.6 65.5 74.9 78.2 83.6 ProofWrtier 94.2 96.5 96.8 99.2 97.2 97.3

We present the performance of CLOVER and the baselines on different tasks, different evaluation metrics, and different language model scales. First, Table 1 compares the performance of CLOVER and the baselines on seven logical reasoning tasks. CLOVER outperforms Logic-LM and other baselines by a significant margin across different logical reasoning tasks. CLOVER shows marked improvement on hard logical reasoning tasks. Specifically, it enhances the performance of Logic-LM on AR-LSAT by 20.4% and ZebraLogic by 30.0%. Overall, neurosymbolic approaches with a symbolic solver (CLOVER and Logic-LM) show remarkable improvement on these hard reasoning tasks. The inference time costs of CLOVER and the baselines are reported in Appendix H.

Second, Table 2 presents three additional evaluations for the neurosymbolic approaches with a symbolic solver. CLOVER shows higher execution rate on every task, which indicates that CLOVER has better capability to generate syntactically correct first-order logic formulas than Logic-LM. CLOVER also shows higher execution accuracy on most tasks, which indicates that CLOVER has better capability to generate logically (or semantically) correct formulas than Logic-LM. These two observations lead to an outperforming program accuracy of CLOVER across different logical reasoning tasks. Specifically, CLOVER increases the execution rate of Logic-LM on AR-LSAT by 25.9% and the execution accuracy by 27.0%, which finally leads to more than doubled program accuracy of Logic-LM. Lastly, we compare the performance of CLOVER and the baselines on different languange models in Appendix G.

### 4.3 Ablations

Table 3: Ablation of CLOVER on AR-LSAT and ZebraLogic. The first three rows are ablations of CLOVER, and the last two rows correspond to CLOVER.

Is CLOVER? Translation Verification AR-LSAT ZebraLogic ✗ direct ✗ 53.3 45.4 ✗ direct (5×5\times) logical consistency 54.6 59.6 ✗ compositional ✗ 55.0 70.0 ✓ compositional logical consistency 61.9 74.2 ✓ compositional disproving 62.8 75.4

We conduct ablation studies of CLOVER on two perspectives: compositional translation and verification, in Table 3. Ablating verification from CLOVER (i.e., random selection) shows 6.9% and 4.2% performance degradation on AR-LSAT and ZebraLogic, respectively. It clearly supports the effectiveness of the verification. Ablating compositional translation from CLOVER (i.e., direct translation) shows 7.3% and 14.6% performance degradation on AR-LSAT and ZebraLogic, respectively. It also clearly supports the effectiveness of the compositional translation. To maintain the verification stage as is, we repeat the sampling of direct translation five times, which is slightly larger than the average number of estimated formulas of CLOVER. Ablating both compositional translation and verification from CLOVER shows further performance loss. Additionally, disproving by counter-interpretation yields better performance than logical consistency.

### 4.4 Analysis

#### Types of Errors.

We analyze error types of CLOVER on AR-LSAT and compare those to Logic-LM’s in Figure 3. Since an SAT solver is sound and does not cause any error, our error analysis focuses on the first-order logic translation. Logic-LM’s errors are mainly caused by incorrect logic (or semantic) and incorrect syntax, which take 53.7% of the total errors. There are preprocessing errors and other errors caused by an incorrect selection of a satisfiability function and limited expressiveness of a Z3 theorem prover. In contrast, we highlight that CLOVER has nearly no logic or syntax error. CLOVER’s errors are primarily caused by preprocessing and other errors, which takes 78.6% of the total errors. This analysis indicates that CLOVER significantly enhances the ability of a language model to generate both syntactically and semantically precise first-order logic formulas.

#### Robustness on Reasoning Length.

We present robustness of CLOVER on long sequence of reasoning and compare the results with CoT-based reasoning LLMs (Jaech et al., 2024)88 8 We use CoT-based reasoning LLMs that were recently released from OpenAI, specifically o1-preview-2024-09-12 and o1-mini-2024-09-12, for our analysis. in Figure 4. We also add the results of Logic-LM to measure the effect of neurosymbolic approach on reasoning length. We observe a noticeable performance drop of CoT-based reasoning LLMs on long sequence of reasoning, which is a frequently pointed-out drawback of the CoT-based approaches. However, neurosymbolic approaches show robustness to the reasoning length. Specifically, CLOVER shows only 12.5% performance drop between the tasks of the shortest and longest sequence of reasoning.

Figure 3: Occurences of different error types of CLOVER and Logic-LM on AR-LSAT annotated subset.

Figure 4:  Performance on different reasoning lengths using CoT-based reasoning LLMs and neurosymbolic approaches on ZebraLogic. Each example is a puzzle of five houses with varying # of features. 

## 5 Related Works

#### LLM-based neurosymbolic approach for reasoning.

Previous works (Ye et al., 2024; Pan et al., 2023; Olausson et al., 2023; Kirtania et al., 2024) utilize an LLM as a semantic parser which translates the natural language logical reasoning problems into first-order logic formulas, and then use a symbolic solver to automatically solve an SAT problem. There is another work (Xu et al., 2024) that utilizes an LLM as not only a semantic parser but also a symbolic solver and a verifier for semantic parsing and symbolic solving. However, these previous works share a common drawback that an LLM cannot faithfully perform complex first-order logic translation, which fundamentally limits the performance of neurosymbolic approaches on complex logical reasoning tasks.

#### LLM-based problem decomposition.

To solve natural language tasks, previous works explore decomposing complex problems into several simpler ones using LLMs. Drozdov et al. (2022) use an LLM to syntactically parse the natural language sentence into several subsentences and performs compositional semantic parsing for simple tasks such as text-to-SQL. However, since a syntactic parsing cannot preserve the semantic of logic, Drozdov et al. (2022) is not applicable to complex logical reasoning tasks. Other works (Zhou et al., 2023; Khot et al., 2023; Press et al., 2023; Dua et al., 2022; Ye et al., 2023) focus on decomposing simple question-answering problems by prompting LLMs with few-shot examples. However, if LLMs simply rely on few-shot examples for decomposing complex logical reasoning problems, then the problems might be incorrectly decomposed, which leads to an unexpected performance loss.

#### LLM-generated formal language verification.

There are lines of works to verify formal language generated by LLMs. Chen et al. (2024) and Madaan et al. (2024) first generate a code from natural language, get feedback from an LLM, and refine the code based on the feedback. Chen et al. (2024) additionally utilizes an external feedback signal from an executor. Ni et al. (2023) first generates candidate codes from natural language and then verify by predicting their correctness using a trained neural network. However, these model-based verifications show limited performance on complex logical reasoning tasks (Appendix I).

## 6 Conclusion

We propose CLOVER, a compositional first-order logic translation and verification for complex logical reasoning. CLOVER first parses the natural language sentence into newly defined logical dependency structures, which reflect first-order logic semantics hidden in the natural language, and then compositionally translates the sentence. We also introduce two verification algorithms using satisfiability to fully cover first-order logic semantics. Empirical results show that CLOVER achieves state-of-the-art performance on seven logical reasoning benchmarks.

## 7 Acknowledgments

This work was supported by Institute for Information &\& communications Technology Planning &\& Evaluation(IITP) grant funded by the Korea government(MSIT) (RS-2019-II190075, Artificial Intelligence Graduate School Program(KAIST)).

## References

  * Achiam et al. (2023) Josh Achiam, Steven Adler, Sandhini Agarwal, Lama Ahmad, Ilge Akkaya, Florencia Leoni Aleman, Diogo Almeida, Janko Altenschmidt, Sam Altman, Shyamal Anadkat, et al.  Gpt-4 technical report.  _arXiv preprint arXiv:2303.08774_ , 2023. 
  * Arias & Khardon (2003) Marta Arias and Roni Khardon.  Complexity parameters for first-order classes.  In _Inductive Logic Programming: 13th International Conference, ILP 2003, Szeged, Hungary, September 29-October 1, 2003. Proceedings 13_ , pp. 22–37. Springer, 2003. 
  * Bronkhorst et al. (2020) Hugo Bronkhorst, Gerrit Roorda, Cor Suhre, and Martin Goedhart.  Logical reasoning in formal and everyday reasoning tasks.  _International Journal of Science and Mathematics Education_ , 18:1673–1694, 2020. 
  * Brown et al. (2020) Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al.  Language models are few-shot learners.  _Advances in neural information processing systems_ , 33:1877–1901, 2020. 
  * Chen et al. (2021) Mark Chen, Jerry Tworek, Heewoo Jun, Qiming Yuan, Henrique Ponde De Oliveira Pinto, Jared Kaplan, Harri Edwards, Yuri Burda, Nicholas Joseph, Greg Brockman, et al.  Evaluating large language models trained on code.  _arXiv preprint arXiv:2107.03374_ , 2021. 
  * Chen et al. (2024) Xinyun Chen, Maxwell Lin, Nathanael Schärli, and Denny Zhou.  Teaching large language models to self-debug.  In _The Twelfth International Conference on Learning Representations_ , 2024. 
  * De Moura & Bjørner (2008) Leonardo De Moura and Nikolaj Bjørner.  Z3: An efficient smt solver.  In _International conference on Tools and Algorithms for the Construction and Analysis of Systems_ , pp. 337–340. Springer, 2008. 
  * Drozdov et al. (2022) Andrew Drozdov, Nathanael Schärli, Ekin Akyürek, Nathan Scales, Xinying Song, Xinyun Chen, Olivier Bousquet, and Denny Zhou.  Compositional semantic parsing with large language models.  In _The Eleventh International Conference on Learning Representations_ , 2022. 
  * Dua et al. (2022) Dheeru Dua, Shivanshu Gupta, Sameer Singh, and Matt Gardner.  Successive prompting for decomposing complex questions.  In _Proceedings of the 2022 Conference on Empirical Methods in Natural Language Processing_ , pp. 1251–1265, 2022. 
  * Frazier & Fodor (1978) Lyn Frazier and Janet Dean Fodor.  The sausage machine: A new two-stage parsing model.  _Cognition_ , 6(4):291–325, 1978. 
  * Han et al. (2022) Simeng Han, Hailey Schoelkopf, Yilun Zhao, Zhenting Qi, Martin Riddell, Luke Benson, Lucy Sun, Ekaterina Zubova, Yujie Qiao, Matthew Burtell, et al.  Folio: Natural language reasoning with first-order logic.  _arXiv preprint arXiv:2209.00840_ , 2022. 
  * Jaech et al. (2024) Aaron Jaech, Adam Kalai, Adam Lerer, Adam Richardson, Ahmed El-Kishky, Aiden Low, Alec Helyar, Aleksander Madry, Alex Beutel, Alex Carney, et al.  Openai o1 system card.  _arXiv preprint arXiv:2412.16720_ , 2024. 
  * Jovanović & Barrett (2011) Dejan Jovanović and Clark Barrett.  Sharing is caring: Combination of theories.  In _Frontiers of Combining Systems: 8th International Symposium, FroCoS 2011, Saarbrücken, Germany, October 5-7, 2011. Proceedings 8_ , pp. 195–210. Springer, 2011. 
  * Khot et al. (2023) Tushar Khot, Harsh Trivedi, Matthew Finlayson, Yao Fu, Kyle Richardson, Peter Clark, and Ashish Sabharwal.  Decomposed prompting: A modular approach for solving complex tasks.  In _The Eleventh International Conference on Learning Representations_ , 2023. 
  * Kirtania et al. (2024) Shashank Kirtania, Priyanshu Gupta, and Arjun Radhakirshna.  Logic-lm++: Multi-step refinement for symbolic formulations.  _arXiv preprint arXiv:2407.02514_ , 2024. 
  * Lin et al. (2025) Bill Yuchen Lin, Ronan Le Bras, Kyle Richardson, Ashish Sabharwal, Radha Poovendran, Peter Clark, and Yejin Choi.  Zebralogic: On the scaling limits of llms for logical reasoning.  _arXiv preprint arXiv:2502.01100_ , 2025. 
  * Madaan et al. (2024) Aman Madaan, Niket Tandon, Prakhar Gupta, Skyler Hallinan, Luyu Gao, Sarah Wiegreffe, Uri Alon, Nouha Dziri, Shrimai Prabhumoye, Yiming Yang, et al.  Self-refine: Iterative refinement with self-feedback.  _Advances in Neural Information Processing Systems_ , 36, 2024. 
  * Montague et al. (1970) Richard Montague et al.  Universal grammar.  _1974_ , pp. 222–46, 1970. 
  * Ni et al. (2023) Ansong Ni, Srini Iyer, Dragomir Radev, Veselin Stoyanov, Wen-tau Yih, Sida Wang, and Xi Victoria Lin.  Lever: Learning to verify language-to-code generation with execution.  In _International Conference on Machine Learning_ , pp. 26106–26128. PMLR, 2023. 
  * Nunes (2012) Terezinha Nunes.  Logical reasoning and learning.  _Encyclopedia of the sciences of learning_ , pp. 2066–2069, 2012. 
  * Olausson et al. (2023) Theo X Olausson, Alex Gu, Benjamin Lipkin, Cedegao E Zhang, Armando Solar-Lezama, Joshua B Tenenbaum, and Roger Levy.  Linc: A neurosymbolic approach for logical reasoning by combining language models with first-order logic provers.  _arXiv preprint arXiv:2310.15164_ , 2023. 
  * Pan et al. (2023) Liangming Pan, Alon Albalak, Xinyi Wang, and William Yang Wang.  Logic-lm: Empowering large language models with symbolic solvers for faithful logical reasoning.  _arXiv preprint arXiv:2305.12295_ , 2023. 
  * Press et al. (2023) Ofir Press, Muru Zhang, Sewon Min, Ludwig Schmidt, Noah A Smith, and Mike Lewis.  Measuring and narrowing the compositionality gap in language models.  In _Findings of the Association for Computational Linguistics: EMNLP 2023_ , pp. 5687–5711, 2023. 
  * Ranise et al. (2005) Silvio Ranise, Christophe Ringeissen, and Calogero G Zarba.  Combining data structures with nonstably infinite theories using many-sorted logic.  In _International Workshop on Frontiers of Combining Systems_ , pp. 48–64. Springer, 2005. 
  * Srivastava et al. (2022) Aarohi Srivastava, Abhinav Rastogi, Abhishek Rao, Abu Awal Md Shoeb, Abubakar Abid, Adam Fisch, Adam R Brown, Adam Santoro, Aditya Gupta, Adrià Garriga-Alonso, et al.  Beyond the imitation game: Quantifying and extrapolating the capabilities of language models.  _arXiv preprint arXiv:2206.04615_ , 2022. 
  * Sweller (1988) John Sweller.  Cognitive load during problem solving: Effects on learning.  _Cognitive science_ , 12(2):257–285, 1988. 
  * Tafjord et al. (2021) Oyvind Tafjord, Bhavana Dalvi, and Peter Clark.  Proofwriter: Generating implications, proofs, and abductive statements over natural language
