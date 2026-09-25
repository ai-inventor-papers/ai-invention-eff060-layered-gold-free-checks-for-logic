URL: https://arxiv.org/html/2410.08437 | FULL FETCH | 2026-09-24T01:47:32Z
warning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
URL: https://arxiv.org/html/2410.08437
Type: HTML
Length: 141410 chars (truncated)

--- Content ---

##### Report GitHub Issue

×

Title:

Content selection saved. Describe the issue below:

Description:

Submit without GitHub Submit in GitHub

arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[ Back to arXiv ](/)

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) Report Issue [ Back to Abstract ](/abs/2410.08437v3 "Back to abstract page") [ Download PDF](/pdf/2410.08437v3 "Download PDF") [ ](javascript:toggleNavTOC\(\); "Toggle navigation") [ ](javascript:toggleReadingMode\(\); "Disable reading mode, show header and footer")

  1. Abstract
  2. 1 Introduction
  3. 2 Formal Framework
  4. 3 The ∀\foralluto∃\exists∨⁣∧\lor\\!\landL Approach for Assessing Truth Maintenance
     1. 3.1 Automatic evaluation of truth maintenance
     2. 3.2 ∀\foralluto∃\exists∨⁣∧\lor\\!\landL Metrics
     3. 3.3 Dynamic Dataset Generation
        1. 3.3.1 Auto-Generated Datasets
  5. 4 Assessment of SOTA LLMs on the ∀\foralluto∃\exists∨⁣∧\lor\\!\landL Benchmark
     1. 4.1 Evaluating LLMs Using ∀\foralluto∃\exists∨⁣∧\lor\\!\landL
     2. 4.2 Evaluating ∀\foralluto∃\exists∨⁣∧\lor\\!\landL as a Benchmark
     3. 4.3 Evaluating Large Reasoning Models using ∀\foralluto∃\exists∨⁣∧\lor\\!\landL
  6. 5 Related Work
  7. 6 Conclusion
  8. References
  9. A Appendix Organization
  10. B Dataset Generation
  11. C 3-CNF Prompt Calibration
  12. D Dataset Generation Hyperparameters
  13. E Experimental Setup
  14. F Prompting
  15. G Analysis of Main Paper Results
     1. G.1 Propositional Logic Results
     2. G.2 First-Order Logic Results
     3. G.3 Regular Expression Results
  16. H Standard Deviation Evaluation
  17. I Additional Zero-Shot Prompting Results
  18. J Few-Shot Prompting Results
  19. K Other Benchmark Correlation and ∀\foralluto∃\exists∨⁣∧\lor\\!\landL Predictive Power Evaluation
     1. K.1 FOLIO Experimental Setups
     2. K.2 Multi-LogiEval Experiment Setup
     3. K.3 HumanEval and Big Bench Hard Score Sources
     4. K.4 Computed Calibrated ∀\foralluto∃\exists∨⁣∧\lor\\!\landL Score
     5. K.5 FOLIO Additional Correlation Figures
  20. L LLM as Verifiers Evaluation
  21. M Dataset Diversity
  22. N Evaluation of LLMs
     1. N.1 Claude Evaluation



[ License: arXiv.org perpetual non-exclusive license ](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2410.08437v3 [cs.AI] 11 Apr 2025

# Autonomous Evaluation of LLMs for   
Truth Maintenance and Reasoning Tasks

Rushang Karia* Daniel Bramblett ††thanks: These authors contributed equally. Daksh Dobhal  Siddharth Srivastava  Affiliation: School of Computing and Augmented Intelligence  Affiliation: Arizona State University  Email: [{rushang.karia,drbrambl,ddobhal,siddharths}@asu.edu](mailto:)

###### Abstract

This paper presents AutoEval, a novel benchmark for scaling Large Language Model (LLM) assessment in formal tasks with clear notions of correctness, such as truth maintenance in translation and logical reasoning. AutoEval is the first benchmarking paradigm that offers several key advantages necessary for scaling objective evaluation of LLMs without human labeling: (a) ability to evaluate LLMs of increasing sophistication by auto-generating tasks at different levels of difficulty; (b) auto-generation of ground truth that eliminates dependence on expensive and time-consuming human annotation; (c) the use of automatically generated, randomized datasets that mitigate the ability of successive LLMs to overfit to static datasets used in many contemporary benchmarks. Empirical analysis shows that an LLM’s performance on AutoEval is highly indicative of its performance on a diverse array of other benchmarks focusing on translation and reasoning tasks, making it a valuable autonomous evaluation paradigm in settings where hand-curated datasets can be hard to obtain and/or update.  
  
---  
  
## 1 Introduction

Large Language Models (LLMs) have been demonstrated to perform well in many natural language tasks involving formal languages such as _autoformalization_ – converting natural language (NL) to formal language (FL) such as source code, math etc., (Wu et al., 2022; Liang et al., 2023), _informalization_ – converting FL to NL (e.g. code summarization), and _reasoning_ – using LLMs to perform sound reasoning or derive proofs. Although these methods have been successful in small-scale scenarios, LLM’s effectiveness in maintaining factual accuracy or preserving which facts are true across translation remains unclear due to the difficulty in designing benchmarks that capture truth maintenance in such tasks. Multiple authors have noted that existing benchmarks and evaluation methodologies for such tasks are susceptible to the Benchmark Contamination Problem due to their use of static datasets, e.g., HumanEval (Chen et al., 2021; Wu et al., 2022; Han et al., 2024), and/or metrics that are insufficient/incomplete syntactic measures of evaluation (e.g, BLEU scores (Callison-Burch et al., 2006). As a result, existing methods provide misleading signals on the capabilities of LLM technology. One effective method to mitigate this problem in existing benchmarks is creating new data (Xu et al., 2024a). This is a tedious and expensive process since data generation requires expert annotators to hand-generate well-balanced datasets. While using LLMs as judges and/or metrics is a promising research direction (Zheng et al., 2023; Shankar et al., 2024; Xu et al., 2024b; Madaan et al., 2023), it is unknown whether LLMs can be used as accurate verifiers.

This paper addresses three key desiderata for benchmarking LLM capabilities in truth maintenance across NL and FL: _(D1) Can we dynamically generate out-of-distribution datasets without human annotators?_ _(D2) How do we accurately assess an LLM’s truth maintenance capabilities?_ _(D3) Can we develop a benchmark predictive of LLM performance on formal translation and reasoning tasks?_

Main contributions Our key contributions are as follows:

  1. 1.

A new approach for automatic synthesis of well-balanced test datasets using context-free grammars that are unlikely to be memorized during the LLM’s training process (§D1).

  2. 2.

The utilization of formal verifiers such as theorem provers to provably validate syntax-independent notions of correctness without having to exhaustively test over all possible truth valuations of formal syntax involving logic (§D2).

  3. 3.

∀\foralluto∃\exists∨⁣∧\lor\\!\landL: a scalable, plug-and-play assessment system for benchmarking new LLMs as and when they are developed. Our system can be extended to any class of formal syntax that uses a grammar and admits an equivalence checker.

  4. 4.

We show that LLM performance on our metric serves as an effective indicator of LLM performance on other metrics across a wide variety of tasks, such as first-order logic reasoning (§D3). Thus, our metric offers a scalable and efficient surrogate for evaluating new LLMs in tasks where other metrics may be limited due to the unavailability of new datasets. We also show that SOTA LLMs are unable to maintain truth effectively.




## 2 Formal Framework

Large Language Models (LLMs) are non-linear functions represented by (billons of) parameters θ\theta that, given a set of input tokens x1,…,xnx_{1},\ldots,x_{n}, typically from natural language NL, predict the output token yi+1y_{i+1} using the distribution P⁡(yi+1|x1,…,xn,y1,…,yi;θ)P(y_{i+1}|x_{1},\ldots,x_{n},y_{1},\ldots,y_{i};\theta). The input tokens contain _context_ κ\kappa (also known as a prompt) that provides the necessary information for the task (e.g., instructions, etc). It is known that κ\kappa significantly impacts the response quality y1,…,yny_{1},\ldots,y_{n} (Sahoo et al., 2024).

Propositional Logic is a branch of logic that utilizes _propositions_ and _logical operators_ (e.g., conjunction: ∧\land, etc) to construct sentences that can be used to perform reasoning using the rules of logic. For example, propositions, p1=It is rainingp_{1}=\textit{It is raining}, p2=It is sunnyp_{2}=\textit{It is sunny} can be used to create a sentence P=p1∨p2P=p_{1}\lor p_{2}. If PP is true and ¬p​1\neg p1 is observed, then one can use the rules of inference to deduce that p2p_{2} is true (Huth & Ryan, 2004). Two sentences in propositional logic, P1P_{1} and P2P_{2}, are equivalent, P1≡P2P_{1}\equiv P_{2}, iff their truth values agree for all possible assignments. E.g., ¬(p1∧p2)≡¬p1∨¬p2\neg(p_{1}\land p_{2})\equiv\neg p_{1}\lor\neg p_{2} since ∀p1,p2\forall p_{1},p_{2} ∈{True,False}×{True,False}\in\\{\textit{True},\textit{False}\\}\times\\{\textit{True},\textit{False}\\}, ¬(p1∧p2)=¬p1∨¬p2\neg(p_{1}\land p_{2})=\neg p_{1}\lor\neg p_{2}.

First-order Logic (FOL) differs from propositional logic in that sentences are constructed using _predicates_ , _quantifiers_ , _constants_ , _symbols_ , and _variables_. A popular example is the syllogism, where, given two FOL sentences ∀x. Man​(x)→Mortal​(x)\forall x.\text{ }\textit{Man}(x)\rightarrow\textit{Mortal}(x) and Man​(Socrates)\textit{Man}(\textit{Socrates}), one can conclude that Mortal​(Socrates)\textit{Mortal}(\textit{Socrates}). A FOL sentence FF can be interpreted using a universe 𝒰\mathcal{U}, a substitution operator σ\sigma, and an interpretation function ℐ\mathcal{I} (Russell & Norvig, 2020). Two FOL sentences, F1,F2F_{1},F_{2}, are equivalent, F1≡F2F_{1}\equiv F_{2}, iff they are equivalent under all possible models. E.g., ¬∀x. Man(x)≡∃y. ¬Man(y)\neg\forall x.\text{ }\textit{Man}(x)\equiv\exists y.\text{ }\neg\textit{Man}(y).

A regular expression (regex) is a sequence of characters used to determine whether a particular string matches the pattern or _language_ induced by the regex. For example, the regex 200​(00)∗200(00)^{\ast}1 using Σ={0,1,2}\Sigma=\\{0,1,2\\} matches all strings possible using Σ\Sigma that begin with a two, followed by one or more pairs of zeroes, and end with a one (Hopcroft et al., 2001). Two regexes, R1R_{1} and R2R_{2} are equivalent, R1≡R2R_{1}\equiv R_{2}, if they represent the same language. It is known that R1≡R2R_{1}\equiv R_{2} if their corresponding minimal deterministic finite automata, D1,D2D_{1},D_{2}, are isomorphic, i.e., D1≃D2D_{1}\simeq D_{2} (Hopcroft et al., 2001).

We refer to sentences (strings) in first-order and propositional logic (regexes) as formal language FL in this paper. We now provide a definition of (Auto/In)formalization in the context of LLMs.

###### Definition 2.1 (Autoformalization: 𝒜\mathcal{A}).

Given an LLM LL, a NL NN, a FL FF, a string ψ∈NL\psi\in\textit{NL}{}, and context κ′\kappa^{\prime}, autoformalization 𝒜\mathcal{A}, is defined as using LL to translate ψ\psi to φ=𝒜L​(ψ,κ′)\varphi=\mathcal{A}_{L}{}(\psi,\kappa^{\prime}) s.t. φ∈FL\varphi\in\textit{FL}{}.

###### Definition 2.2 (Informalization: ℐ\mathcal{I}).

Given an LLM LL, a NL NN, a FL FF, a string φ∈FL\varphi\in\textit{FL}{}, and context κ\kappa, informalization ℐ\mathcal{I}, is defined as using LL to translate φ\varphi to ψ=ℐL​(φ,κ)\psi=\mathcal{I}_{L}{}(\varphi,\kappa) s.t. ψ∈NL\psi\in\textit{NL}{}.

Example One possible autoformalization of “Every human drinks coffee but some are not dependent on it” in FOL is [∀x. Human(x)⟹Drinks(x,Coffee)]∧[∃y. Human(y)∧¬Dependent(y,Coffee)][\forall x.\text{ }\textit{Human}(x)\implies\textit{Drinks}(x,\textit{Coffee})]\land[\exists y.\text{ }\textit{Human}(y)\land\neg\textit{Dependent}(y,\textit{Coffee})]. Ideally, informalization will be an inverse of autoformalization. Therefore, the FOL formula [∀x. Human(x)⟹Drinks(x,Coffee)]∧[∃y. Human(y)∧¬Dependent(y,Coffee)][\forall x.\text{ }\textit{Human}(x)\implies\textit{Drinks}(x,\textit{Coffee})]\land[\exists y.\text{ }\textit{Human}(y)\land\neg\textit{Dependent}(y,\textit{Coffee})] can be informalized to the sentence “Every human drinks coffee but some are not dependent on it”.

We assume that the context κ,κ′\kappa,\kappa^{\prime} provided contains the prompt and any necessary vocabulary that is needed for the task (e.g., Human​(x)\textit{Human}(x) represents that xx is a human, etc.). We omit κ,κ′\kappa,\kappa^{\prime}, and LL in the notation for 𝒜\mathcal{A} and ℐ\mathcal{I} where they are clear from the context.

Informalization and autoformalization are non-deterministic functions. Therefore, it is possible that a different LLM (or the same LLM with a different seed) autoformalizes the same input text to a syntactically or even semantically different output. E.g., the example above could be autoformalized to the semantically equivalent form: ∀x. Human​(x)⟹Drinks​(x,Coffee)∧¬∀⁡y. Human​(y)⟹Dependent​(y,Coffee)\forall x.\text{ }\textit{Human}(x)\implies\textit{Drinks}(x,\textit{Coffee})\land\neg\forall y.\text{ }\textit{Human}(y)\implies\textit{Dependent}(y,\textit{Coffee}). Similarly, an LLM can informalize differently. The example above could be informalized by the same LLM to “All humans drink coffee but some are not dependent on it”. Thus, the informalization (autoformalization) of an autoformalization (informalization) of a string is possibly different from that string: 𝒜L​(ℐL​(φ,κ′),κ)≠φ{\mathcal{A}}_{L}({\mathcal{I}}_{L}(\varphi,\kappa^{\prime}),\kappa)\neq\varphi and ℐL​(𝒜L​(ψ,κ),κ′)≠ψ{\mathcal{I}}_{L}({\mathcal{A}}_{L}(\psi,\kappa),\kappa^{\prime})\neq\psi. Given n∈ℕ+n\in\mathbb{N}^{+}, let (𝒜∘ℐ)n​(φ0)(\mathcal{A}\circ\mathcal{I})^{n}(\varphi_{0}){} to refer to the sequence φ0→ψ0→…→φn\varphi_{0}\rightarrow\psi_{0}\rightarrow\ldots\rightarrow\varphi_{n} that is obtained using an LLM LL when starting with FL φ0\varphi_{0}, where ψi=ℐ⁡(φi)\psi_{i}=\mathcal{I}(\varphi_{i}) and φi+1=𝒜⁡(ψi)\varphi_{i+1}=\mathcal{A}(\psi_{i}).

While syntactic differences across (𝒜∘ℐ)n​(φ0)(\mathcal{A}\circ\mathcal{I})^{n}(\varphi_{0}) operations may be acceptable, the ability of an LLM to maintain semantic content across (𝒜∘ℐ)n​(φ0)(\mathcal{A}\circ\mathcal{I})^{n}(\varphi_{0}){} for FL such as first-order logic, regular expressions, etc., is foundational and underlies many aspects of the capabilities of LLMs surrounding reasoning, semantically accurate translation, etc. For programming, it has been shown that autoformalization accuracy is indicative of the reasoning abilities of LLMs since they frame reasoning as generation of FL (Chen et al., 2021). Others (Wu et al., 2022) have made similar observations and have highlighted the need for benchmarks and metrics for assessing the truth maintenance capabilities of LLMs. In this paper, we further show through our empirical evaluation that an LLM’s ability to preserve factual information or semantic truth across translations is indicative of its performance on related tasks.

Intuitively, truth maintenance captures an LLM’s ability to preserve truth across translation; operationally, it evaluates the ability of a system to be able to accurately invert its own translations. We say that an LLM maintains truth in translation iff (𝒜∘ℐ)n​(φ0)(\mathcal{A}\circ\mathcal{I})^{n}(\varphi_{0}){} always leads to a φn\varphi_{n} that is semantically equivalent to φ0\varphi_{0}. Recall that ≡\equiv denotes the semantic equivalence operator in FL. Formally,

###### Definition 2.3 (LLM Truth Maintenance).

An LLM LL maintains truth in translation iff ∀φ0,n\forall\varphi_{0},n, and for all sequences (𝒜∘ℐ)n​(φ0)(\mathcal{A}\circ\mathcal{I})^{n}(\varphi_{0}) obtained using LL, φn≡φ0\varphi_{n}\equiv\varphi_{0}.

In practice, we estimate the ability for truth maintenance through a sampling-based process. Naturally, LLMs may not autoformalize, reason, etc., correctly due to issues like hallucination (Ji et al., 2023), etc. For the earlier example, the LLM could autoformalize by omitting the H​u​m​a​n​(y)Human(y) statement to yield [∀x. Human(x)⟹Drinks(x,Coffee)]∧[∃y. ¬Dependent(y,Coffee)][\forall x.\text{ }\textit{Human}(x)\implies\textit{Drinks}(x,\textit{Coffee})]\land[\exists y.\text{ }\neg\textit{Dependent}(y,\textit{Coffee})]. This seems innocuous but changes the meaning since yy is no longer required to be human, and thus it interprets as “All humans drink coffee, but some element of the universe is not dependent on coffee.” Such issues have profound implications in synthesizing specifications and/or programs. Thus, an LLM must be able to understand its own generated output across NL and FL, and it is imperative to create a benchmark that can faithfully assess the truth maintenance of LLMs.

## 3 The ∀\foralluto∃\exists∨⁣∧\lor\\!\landL Approach for Assessing Truth Maintenance

We now describe our approach, ∀\foralluto∃\exists∨⁣∧\lor\\!\landL, for autonomously assessing an LLM’s ability for truth maintenance. ∀\foralluto∃\exists∨⁣∧\lor\\!\landL provides dynamically generated datasets that can be scaled arbitrarily by systematically generating out-of-distribution, well-balanced ground-truth data (§D1 – Sec. 1), provides §D2 by using intrinsic LLM capabilities to automatically assess (𝒜∘ℐ)n​(φ0)(\mathcal{A}\circ\mathcal{I})^{n}(\varphi_{0}) without requiring any labeled annotations and using formal verifiers to rigorously check and guarantee the correctness of (𝒜∘ℐ)n​(φ0)(\mathcal{A}\circ\mathcal{I})^{n}(\varphi_{0}) without having to engage in an exhaustive search process.

### 3.1 Automatic evaluation of truth maintenance

We develop a novel technique that can soundly assess truth maintenance without any human annotations by evaluating φi→ψi→φi+1\varphi_{i}\rightarrow\psi_{i}\rightarrow\varphi_{i+1}. Our approach is based on the following intuition. Let ℐ:φ→ψ\mathcal{I}:\varphi\rightarrow\psi be a non-deterministic function that maps FL φ\varphi to NL ψ\psi. Similarly, let 𝒜:ψ→φ\mathcal{A}:\psi\rightarrow\varphi be a non-deterministic function that maps NL ψ\psi to FL φ\varphi. In general, there are many possible correct informalizations (autoformalizations) of φ∈FL\varphi\in\textit{FL}{} (ψ∈NL\psi\in\textit{NL}{}). Because ℐ\mathcal{I} and 𝒜\mathcal{A} are non-deterministic functions, their inverses are thus not well-defined.

Our key observation is that if ℐ\mathcal{I} and 𝒜\mathcal{A} come from the same system (e.g., an LLM), then we can evaluate that system’s truth maintenance by _composing_ ℐ\mathcal{I} and 𝒜\mathcal{A}. Let φ\varphi be any FL expression and let LL be an LLM. If LL preserves truth, then ψ=ℐ⁡(φ)\psi=\mathcal{I}(\varphi) will be an accurate NL representation of φ\varphi and φ′=𝒜⁡(ψ)\varphi^{\prime}=\mathcal{A}(\psi) will be a semantically equivalent FL representation of ψ\psi. Since ψ\psi is an NL description, it is quite challenging to check whether ℐ⁡(φ)\mathcal{I}(\varphi) is indeed an accurate representation of φ\varphi without human intervention. However, if LL preserves truth, φ′=𝒜⁡(ℐ⁡(φ))\varphi^{\prime}=\mathcal{A}(\mathcal{I}(\varphi)) will be semantically equivalent to φ\varphi even if they are not syntactically identical. Thus, we only need to check if φ≡φ′\varphi\equiv\varphi^{\prime}. For example, let φ0=p1∧p1\varphi_{0}=p_{1}\land p_{1}, ψ0=ℐ⁡(φ1)=\psi_{0}=\mathcal{I}(\varphi_{1})= “A conjunction of propositions p1p_{1} and p1p_{1} that can be simplified to p1p_{1} using Idempotence.”, and φ1′=𝒜⁡(ψ0)=p1\varphi^{\prime}_{1}=\mathcal{A}(\psi_{0})=p_{1} for a sequence (𝒜∘ℐ)1​(φ0)(\mathcal{A}\circ\mathcal{I})^{1}(\varphi_{0}). It is challenging to check if ψ0\psi_{0} accurately represents φ0\varphi_{0}, but it is easy to check if φ0≡φ1\varphi_{0}\equiv\varphi_{1} using a formal verifier.

Figure 1: The ∀\foralluto∃\exists∨⁣∧\lor\\!\landL process for autonomous evaluation of LLM truth maintenance w.r.t. (𝒜∘ℐ)n​(φ0)(\mathcal{A}\circ\mathcal{I})^{n}(\varphi_{0}).

Since ∀\foralluto∃\exists∨⁣∧\lor\\!\landL uses formal syntax φ\varphi as input and produces formal syntax φ′\varphi^{\prime} as output, we can use formal verifiers to check whether φ≡φ′\varphi\equiv\varphi^{\prime}. As a result, ∀\foralluto∃\exists∨⁣∧\lor\\!\landL avoids brittle syntactic equivalence checks and exhaustive tests of semantic equivalence that require evaluations of all possible truth valuations of formulas or executions of regexes.

We use the above insights to automatically assess LLM truth maintenance by using the same LLM LL to represent ℐ\mathcal{I} and 𝒜\mathcal{A} respectively. Fig. 1 shows our overall assessment process. Briefly, we use a context-free grammar 𝒢\mathcal{G} to automatically generate a ground-truth FL expression φ0\varphi_{0}. Next, we use a vocabulary generation process to generate a context for φ0\varphi_{0}. This can either use abstract terms or use NL elements for more human-like scenarios (§D1). We then evaluate (𝒜∘ℐ)1​(φ0)(\mathcal{A}\circ\mathcal{I})^{1}(\varphi_{0}) by using LL to first generate ψ0=ℐ⁡(φ0,κ)\psi_{0}=\mathcal{I}(\varphi_{0},\kappa) using context κ\kappa designed for informalization. The context of LL is cleared (note that we only use the output of ℐ⁡(φ0)\mathcal{I}(\varphi_{0})), and we use LL to generate φ1=𝒜⁡(ψ0,κ′)\varphi_{1}=\mathcal{A}(\psi_{0},\kappa^{\prime}) using context κ′\kappa^{\prime} designed for autoformalization. We then use a verifier (e.g., Z3 (de Moura & Bjørner, 2008), Prover9 (McCune, 2010)) to assess if φ0≡φ1\varphi_{0}\equiv\varphi_{1} since both are elements of FL. If φ0≡φ1\varphi_{0}\equiv\varphi_{1} then we can repeat the process by evaluating (𝒜∘ℐ)1​(φ1)(\mathcal{A}\circ\mathcal{I})^{1}(\varphi_{1}) similarly.

Example: Consider case 2 in Fig. 1. ∀\foralluto∃\exists∨⁣∧\lor\\!\landL uses the grammar in Fig. 2b to automatically generate a ground truth FL sentence as φ0=p1∧p2∧p1\varphi_{0}=p_{1}\land p_{2}\land p_{1}. We can use any vocabulary to generate meaning for the propositions; p1:It is raining todayp_{1}:\textit{It is raining today}, p2:It was sunny yesterdayp_{2}:\textit{It was sunny yesterday}. Next, the LLM LL is prompted with Prompt 3.3.1 to perform informalization yielding NL ψ0=𝒜⁡(φ0)\psi_{0}=\mathcal{A}(\varphi_{0}). LL can perform any simplification or other paraphrasing necessary. For example, LL could informalize φ0\varphi_{0} above to ψ0=\psi_{0}=“The weather status was sunny yesterday whilst it is raining today.” Notice that the LLM-generated NL statement automatically reflects a simplification using the Commutative (a∧b≡b∧aa\land b\equiv b\land a) and Idempotent (a∧a≡aa\land a\equiv a) properties. Next, LL is asked to autoformalize ψ0\psi_{0} without any context other than the vocabulary to use and a prompt for autoformalization (App. F). In this case, the LLM could return φ1=𝒜⁡(ψ0)=p1∧p2\varphi_{1}=\mathcal{A}(\psi_{0})=p_{1}\land p_{2}. We use a theorem prover such as Prover9 (McCune, 2010) to show that φ0≡φ1\varphi_{0}\equiv\varphi_{1} and thus assess LL’s truth maintenance capabilities w.r.t. (𝒜∘ℐ)1​(φ0)(\mathcal{A}\circ\mathcal{I})^{1}(\varphi_{0}).

### 3.2 ∀\foralluto∃\exists∨⁣∧\lor\\!\landL Metrics

∀\foralluto∃\exists∨⁣∧\lor\\!\landL score When evaluating an LLM’s truth-maintenance capabilities, it is crucial to consider the intended application, because performance on FL strings of similar complexity typically indicates how the model will fare in practice. As such, ∀\foralluto∃\exists∨⁣∧\lor\\!\landL can be used in two distinct modes: parameterized and calibrated ∀\foralluto∃\exists∨⁣∧\lor\\!\landL scores. The parameterized ∀\foralluto∃\exists∨⁣∧\lor\\!\landL score computes performance with the descriptional complexity of FL strings as a parameter (e.g., the number of operators). The calibrated ∀\foralluto∃\exists∨⁣∧\lor\\!\landL score Sc​a​l​(D,d)S_{cal}(D,d) is computed using all FL strings from dataset DD with complexity up to dd, where there are equal number of examples for each complexity. In both modes, the score is computed as the fraction of FL strings in the corresponding dataset for which (𝒜∘ℐ)1​(φ1)≡φ1(\mathcal{A}\circ\mathcal{I})^{1}(\varphi_{1})\equiv\varphi_{1}.

Bounding false positives in computation of ∀\foralluto∃\exists∨⁣∧\lor\\!\landL scores A key advantage of the ∀\foralluto∃\exists∨⁣∧\lor\\!\landL score is its robustness to different informalizations of the same FL. Thus, when ∀\foralluto∃\exists∨⁣∧\lor\\!\landL outputs that an LLM maintains truth (𝒜∘ℐ)n​(φ0)(\mathcal{A}\circ\mathcal{I})^{n}(\varphi_{0}){} on FL φ0\varphi_{0}, the intermediate NL=ℐ⁡(ψ0)\textit{NL}{}=\mathcal{I}(\psi_{0}) is a semantically equivalent translation of φ0\varphi_{0}. We now bound the probability of false positives, i.e., cases where the LLM fails both autoformalizing and informalizing but yields an FL string equivalent to the original.

Given an LLM LL, let φ0→ℐL​(φ0)ψ0→𝒜L​(ψ0)φ1\varphi_{0}\xrightarrow{\mathcal{I}_{L}{}(\varphi_{0})}\psi_{0}\xrightarrow{\mathcal{A}_{L}{}(\psi_{0})}\varphi_{1} be an execution of the ∀\foralluto∃\exists∨⁣∧\lor\\!\landL process for (𝒜∘ℐ)1​(φ0)(\mathcal{A}\circ\mathcal{I})^{1}(\varphi_{0}) s.t. φ0≡φ1\varphi_{0}\equiv\varphi_{1} but ψ0\psi_{0} is not an accurate representation of φ0\varphi_{0}. We can derive the probability of ∀\foralluto∃\exists∨⁣∧\lor\\!\landL providing such false positives. Let pℐp_{\mathcal{I}} be the probability with which LL informalizes an FL expression ℐ⁡(φ0)=ψ0\mathcal{I}(\varphi_{0})=\psi_{0} s.t. ψ0\psi_{0} is an accurate representation of φ0\varphi_{0}. Similarly, let p𝒜p_{\mathcal{A}} be the probability of autoformalizing ψ0\psi_{0}, 𝒜⁡(ψ0)=φ1\mathcal{A}(\psi_{0})=\varphi_{1}, s.t. φ1\varphi_{1} is semantically equivalent to ψ0\psi_{0}, i.e. φ0≡φ1\varphi_{0}\equiv\varphi_{1}. Let pHp_{H} be the probability that LL hallucinates FL φ1\varphi_{1} by autoformalizing ψ0\psi_{0} s.t. φ1≡φ0\varphi_{1}\equiv\varphi_{0} given that ψ0\psi_{0} is not an accurate representation of φ0\varphi_{0}.

It can be seen that for a false positive to be outputted by ∀\foralluto∃\exists∨⁣∧\lor\\!\landL, the sequence φ0→ψ0\varphi_{0}\rightarrow\psi_{0} produces an incorrect NL description and the sequence ψ0→φ1\psi_{0}\rightarrow\varphi_{1} autoformalizes incorrectly but hallucinates just right to yield φ1≡φ0\varphi_{1}\equiv\varphi_{0}. The probability of such a sequence corresponds to LL making two mistakes, with the second mistake being such that it generated an expression equivalent to φ0\varphi_{0}. This can be expressed as (1−pℐ)​(1−p𝒜)​pH(1-p_{\mathcal{I}})(1-p_{\mathcal{A}})p_{H}. For (𝒜∘ℐ)n​(φ0)(\mathcal{A}\circ\mathcal{I})^{n}(\varphi_{0}), this probability is (1−pℐ)n​(1−p𝒜)n​pHn(1-p_{\mathcal{I}})^{n}(1-p_{\mathcal{A}})^{n}p_{H}^{n} since ∀\foralluto∃\exists∨⁣∧\lor\\!\landL computes (𝒜∘ℐ)1​(φi)(\mathcal{A}\circ\mathcal{I})^{1}(\varphi_{i}) if φi−1≡φi\varphi_{i-1}\equiv\varphi_{i} (Sec. 3). As LLM technology improves, we expect pℐ,p𝒜→1p_{\mathcal{I}},p_{\mathcal{A}}\rightarrow 1 and pH→0p_{H}\rightarrow 0. As a result, the probability of false positives provided by ∀\foralluto∃\exists∨⁣∧\lor\\!\landL decreases as nn increases. This low likelihood of false positives is further confirmed empirically by our analysis of correlation and predictive power w.r.t. other benchmarks (Sec. 4).

LLMs as verifiers score The llm-verifier score evaluates a given llm’s ability to determine equivalence between FL strings. It is measured by using FL strings produced by a LLM from the ∀\foralluto∃\exists∨⁣∧\lor\\!\landL process. For each dataset and descriptional complexity, we compute an F1F_{1} score by comparing the evaluated LLM’s equivalence predictions with the formal verifier’s results. We use Chain-of-Thought (CoT) to allow LLMs to utilize their generated outputs to improve their reasoning (Wei et al., 2022).

Predictive power In addition to using calibrated and parameterized ∀\foralluto∃\exists∨⁣∧\lor\\!\landL scores for assessing the ability for truth maintenance, we propose a new metric for evaluating the extent to which performance on a benchmark is indicative of performance on other benchmarks:

###### Definition 3.1 (Predictive Power).

Let L1L_{1} and L2L_{2} be language models evaluated on two benchmarks AA and BB with ranks ≥A\geq_{A} and ≥B\geq_{B}. The predictive power of AA over BB is formally defined as 𝒫|A(B)=Pr(L1≥BL2|L1≥AL2)\mathcal{P}_{|A}(B)=Pr(L_{1}\geq_{B}L_{2}|L_{1}\geq_{A}L_{2}).

In practice, we compute predictive power as a sampling-based maximum-likelihood estimate over multiple auto-generated datasets.

### 3.3 Dynamic Dataset Generation

We use context-free grammars (CFGs) (Hopcroft et al., 2001) – a set of _production rules_ over _terminal_ and _non-terminal_ symbols – for dynamically generating datasets. An _infix parse tree_ is obtained by repeatedly applying the rules, where the depth of this tree is often used to measure the _descriptional complexity_ of a given string generated using the CFG (Csuhaj-Varjú & Kelemenová, 1993). CFGs also can be used to generate arbitrarily large amounts of data dynamically.

Another advantage is that CFGs can be customized with minimal human effort to generate diverse datasets whose ground-truth data possesses specific properties. For example, a dynamic dataset that only consists of kk–CNF sentences – propositional logic in the Canonical Normal Form (P10∨…∨Pk0)∧(P11∨…∨Pk1)∧…(P^{0}_{1}\lor\ldots\lor P^{0}_{k})\land(P^{1}_{1}\lor\ldots\lor P^{1}_{k})\land\ldots where Pij∈{px,¬px}P^{j}_{i}\in\\{p_{x},\neg p_{x}\\} – can be easily generated. We enrich the generated sentence with context via a customizable Vocabulary Generation step, which automatically provides the necessary vocabulary for performing the task (e.g., providing English meanings to allow for human-like NL) by using terms from a vocabulary database or by using an LLM.

#### 3.3.1 Auto-Generated Datasets

∀\foralluto∃\exists∨⁣∧\lor\\!\landL is open-source11 1 The code for this project is available at: <https://github.com/AAIR-lab/autoeval>., is written in Python 3, includes several pre-computed datasets, and is easily customizable for adding new datasets, prompts, LLMs, etc. We now describe the datasets that any newly developed LLM can be evaluated on by using ∀\foralluto∃\exists∨⁣∧\lor\\!\landL out-of-the-box.

| S\displaystyle S | →S∧S\displaystyle\rightarrow S\land S |   
---|---|---|---  
| S\displaystyle S | →(P∨P∨P)\displaystyle\rightarrow(P\lor P\lor P) |   
| P\displaystyle P | →¬v|v\displaystyle\rightarrow\neg v|v |   
  
(a)(a) 33–CNF

| S\displaystyle S | →(S∧S)|(S∨S)\displaystyle\rightarrow(S\land S)|(S\lor S) |   
---|---|---|---  
| S\displaystyle S | →(¬S)\displaystyle\rightarrow(\neg S) |   
| S\displaystyle S | →¬v|v\displaystyle\rightarrow\neg v|v |   
  
(b)(b) Propositional Logic

| S\displaystyle S | →F|(∀f. S)|(∃f. S)\displaystyle\rightarrow F|(\forall f.\text{ }S)|(\exists f.\text{ }S) |   
---|---|---|---  
| F\displaystyle F | →(F∧F)|(F∨F)\displaystyle\rightarrow(F\land F)|(F\lor F) |   
| F\displaystyle F | →(¬F)​|¬p|​p\displaystyle\rightarrow(\neg F)|\neg p|p |   
  
(c)(c) First-order Logic

| S\displaystyle S | →(S)​K|Σ​K\displaystyle\rightarrow(S)K|\Sigma K |   
---|---|---|---  
| S\displaystyle S | →S​Σ​K\displaystyle\rightarrow S\Sigma K |   
| K\displaystyle K | →∗|ε\displaystyle\rightarrow\ast|\varepsilon |   
  
(d)(d) Regular Expression

Figure 2: CFGs (described in Sec. 3.3.1) used for synthesizing the datasets in ∀\foralluto∃\exists∨⁣∧\lor\\!\landL.

Our dataset generator (described in App. B) takes a user-provided CFG and vocabulary to dynamically generate user-controlled, diverse datasets up to a user-specified metric such as the number of operators, parse tree depth, etc. It is guaranteed to generate any representable string using the CFG (App. B). As a result, users can easily generate out-of-distribution datasets in ∀\foralluto∃\exists∨⁣∧\lor\\!\landL by simply providing CFGs and/or vocabularies.

The ∀\foralluto∃\exists∨⁣∧\lor\\!\landL core benchmark uses four CFGs (Fig. 2) for producing five datasets compromising FL strings. The 3-CNF(n)(n) (Fig. 2a) and propositional logic PL(n)(n) (Fig. 2b) CFGs replace the terminal by randomly selecting from a list of nn propositions. First-order logic FOL(np,no)(n_{p},n_{o}) (Fig. 2c) CFG replaces the terminal with predicates of the form p⁡(v1,…,vn)p(v_{1},\ldots,v_{n}) where pp is a predicate name selected from a list of npn_{p} predicates, viv_{i} is either an object oo from a list of non_{o} objects or is a free variable f∈{x1,x2,…}f\in\\{x_{1},x_{2},\ldots\\} that is appropriately annotated within the scoping rules. Finally, the regular expression RE(n)(n) (Fig. 2d) CFG uses the vocabulary set Σ={0,…,n−1}\Sigma=\\{0,\ldots,n-1\\}.

We provide 5 datasets with 2 generated from the FOL CFG and 1 each for the rest. We sampled 500 strings for each complexity level. The 3-CNF(12) dataset contains examples with up to 59 operators, totaling ∼10​k{\sim}10k strings. PL(12)(12) contains examples with up to 40 operators, for a total of ∼20​k{\sim}20k strings. The RE(2)(2) dataset contains examples with tree depth up to 40, also totaling ∼20​k{\sim}20k strings.

The FOL datasets, FOL(8,12)(8,12)–S and FOL(8,12)(8,12)–E, contain examples with up to 37 operators, for a total of ∼19​k{\sim}19k strings each. FOL(8,12)(8,12)–S uses auto-generated synthetic object and predicate names. Conversely, FOL(8,12)(8,12)–E uses verbs from VerbNet (Schuler, 2005) for predicate names and names from Faker (Faraglia, 2024) for object names. Using more descriptive names allows for informalization to produce more _abstract_ sentences that closely resemble the NL statements in SOTA autoformalization datasets. For example, a FL statement Boom(Richard)∧Exercise(Yolonda)\textit{Boom(Richard)}\land\textit{Exercise(Yolonda)} yields a more natural NL statement: “Richard experiences a boom, and Yolonda engages in exercise”.

While each dataset was generated in 10 separate pieces, each produced independently, our datasets contain ∼85​k{\sim}85k unique examples. We also provide zero-shot and 2-shot prompts for each dataset, for a total dataset size ∼170​k{\sim}170k for off-the-shelf evaluation and continual assessment of any new LLM. Of these examples, ∼\sim85% of them are composed of unique CFG parse trees (trees obtained by sampling the CFG but not injecting the vocabularies). Expressions with the same parse tree but different vocabularies (e.g., p1∧p2p_{1}\land p_{2} and p2∧p1p_{2}\land p_{1}) account for ∼\sim10% of our dataset, providing a robust check against positional bias in the LLM. Additional information is presented in App. M.

We use open-source libraries to robustly parse the LLM-generated output. We use the Natural Language Toolkit (NLTK) library (Bird et al., 2009) for parsing logic and use Reg2Dfa (Reg, 2017) for regexes. LLM output that cannot be parsed is said to be _syntactically non-compliant_. Additionally, we also use scripts to ensure that the informalization step does not copy elements of FL into NL (e.g., complete or any parts of FL) that would otherwise make autoformalization trivial.

Prompt 1: Informalization (ℐ\mathcal{I}) prompt for Fig. 1: Case 2 (other prompts available in App. F) Your task is to convert a ⟨\langlePropositional Logic, First-order Logic⟩\rangle formula, appearing after [FORMULA], to a natural description that represents the formula. Only natural language terms are allowed to be used and do not copy the formula in your description. Your description should allow one to reconstruct the formula without having access to it, so make sure to use the correct names in your description. Explicitly describe the predicates. You may use terms verbatim as specified in the vocabulary below.   
[VOCABULARY]   
Operators: List of operators followed by their NL interpretations Objects: The objects in the universe (if any) Propositions: The propositions in the universe and their NL interpretations (if any) Predicates: The predicates in the universe and their NL interpretations (if any) Examples: Few-shot examples of the task (if any) Example Prompt Your task …\ldots   
Operators: ∧\land represents conjunction, ∨\lor represents disjunction, …\ldots Propositions: p1:p_{1}: It is raining, p2:p_{2}: It was sunny yesterday Formula: p1∧p2∧p1p_{1}\land p_{2}\land p_{1} Example Response: The sun was bright the day before whilst it is raining today.

## 4 Assessment of SOTA LLMs on the ∀\foralluto∃\exists∨⁣∧\lor\\!\landL Benchmark

In this section we present an evaluation of several SOTA LLMs using ∀\foralluto∃\exists∨⁣∧\lor\\!\landL, as well as an evaluation of ∀\foralluto∃\exists∨⁣∧\lor\\!\landL as a benchmark for evaluating LLMs’ reasoning and translation ability using the predictive power score. In particular, we use the following assessment criteria for evaluating LLMs using ∀\foralluto∃\exists∨⁣∧\lor\\!\landL: _(A1) Can LLMs produce FL translations that are syntactically compliant?_ _(A2) Can LLMs maintain truth while translating FL?_ _(A3) Can LLMs accurately verify whether two FL strings are logically equivalent?_ In addition, we use the following criterion to assess ∀\foralluto∃\exists∨⁣∧\lor\\!\landL itself: _(A4) Is the performance on ∀\foralluto∃\exists∨⁣∧\lor\\!\landL indicative of performance on other benchmarks?_

### 4.1 Evaluating LLMs Using ∀\foralluto∃\exists∨⁣∧\lor\\!\landL

We assessed §A1 - §A3 using 17 SOTA closed and open-source LLMs (Fig. 3). For clarity, we plot select models, grey out the data from the others, and refer the reader to App. N for a comprehensive overview. We evaluated §A1 and §A2 using the parameterized ∀\foralluto∃\exists∨⁣∧\lor\\!\landL score on our generated datasets. For §A3, we calculated the LLMs as verifiers score for each descriptional complexity class by having each LLM verify the results produced by GPT-4o.

As stated in Sec. 2, prompts are crucial for LLM performance. To ensure our results reflect LLM capabilities rather than the effect of poorly designed prompts, we conducted extensive prompt engineering and ensured that at least one LLM could achieve a parameterized ∀\foralluto∃\exists∨⁣∧\lor\\!\landL score ≥95%\geq 95\% on the 3-CNF(12)(12) dataset, which has a constrained but representative grammar. Analysis on each LLM’s performance on the 3-CNF(12)(12) dataset is presented in App. C.

Figure 3: Zero-shot Pass@1 results from using ∀\foralluto∃\exists∨⁣∧\lor\\!\landL to assess LLMs w.r.t. §A1, §A2, §A3 on the packaged datasets (Sec. 3.3.1). The x-axis represents an increasing descriptional complexity. The y-axis is each evaluated LLM’s syntactic compliance rate (1st row), parameterized ∀\foralluto∃\exists∨⁣∧\lor\\!\landL score (2nd row), and F1F_{1} score as a verifier (3rd row). Additional results (prompt calibration, few-shot, etc.) are included in the Appendix.

As shown in Fig. 3, SOTA LLMs are able to produce syntactically compliant formal syntax (§A1) for formal syntax with low descriptional complexity (e.g., few operators in logic). However, as the complexity increases, the ability of LLMs to autoformalize their own informalizations diminishes. One surprising result here is that GPT-4o is less syntactically compliant for regexes than Phi and LLama-3, which are much smaller models. This is due to GPT-4o often repeating a token sequence when translating regex, resulting in hitting the token limit. For logic, we observed that LLMs often use the correct syntax but often misplace parentheses, creating malformed expressions.

Our analysis further shows, except on the 3-CNF(12)(12) dataset used for prompt calibration, LLMs cannot maintain truth in FL translation (§A2) as the descriptional complexity increases. For translating logic expressions with more than 20 operators, none exceeded 50% accuracy in maintaining truth. This is concerning since formal specifications often have hundreds of operators. A common issue was misunderstanding the formal syntax’s precedence and associativity rules. Misplaced operators led to quick verification failures. We provide an analysis of failing cases in App. G.

Moreover, even with CoT prompting, LLMs cannot serve as accurate verifiers of logical equivalence (§A3) for anything but toy expressions (low descriptional complexity), after which F1F_{1} scores fall sharply. For small FL strings, we found that LLMs have difficulties with negations in logic. Due to space limitations, we present some examples and an analysis of the kinds of syntactic structures that LLMs fail to verify correctly in the Appendix (App. L, Fig. 21).

### 4.2 Evaluating ∀\foralluto∃\exists∨⁣∧\lor\\!\landL as a Benchmark

For assessing §A4, we used the same 17 LLMs to evaluate the predictive power (Sec. 3.2) of ∀\foralluto∃\exists∨⁣∧\lor\\!\landL w.r.t 5 popular benchmarks: (a) FOLIO(R;{NL, FOL}) (Han et al., 2024), a popular logical reasoning benchmark with ground truth in both NL and FL; (b) FOLIO({𝒜/ℐ}\\{\mathcal{A}/\mathcal{I}\\}) evaluates if an LLM can (auto/in)formalize NL (FL) accurately; (c) LogiEval(R;{PL, FOL}) (Patel et al., 2024) a reasoning benchmark with ground truth in propositional and first-order logic; (d) HumanEval(𝒜\mathcal{A}) (Chen et al., 2021), a code autoformalization benchmark; (e) Big Bench Hard (BBH) (Suzgun et al., 2023). These benchmarks are contrasted in Sec. 5, and example prompts of these benchmarks are included in App. K. We ran 5 runs on each benchmark except BBH. For BBH, we use the reported numbers in the literature as scores for the models (sources are included in App K). We measured the correlation between each benchmark’s score and the calibrated ∀\foralluto∃\exists∨⁣∧\lor\\!\landL score (Fig. 4), which was calibrated based on the descriptional complexity of the examples found in the benchmark. We also measured the calibrated ∀\foralluto∃\exists∨⁣∧\lor\\!\landL score’s predictive power w.r.t these benchmarks (Fig. 5).

Figure 4: Correlation between scores on ∀\foralluto∃\exists∨⁣∧\lor\\!\landL and static benchmarks from the literature. The Pearson correlation coefficient (ρ\rho) and the pp-value (values ≤0.05\leq 0.05 are statistically significant) are annotated in the top left. The calibrated ∀\foralluto∃\exists∨⁣∧\lor\\!\landL score Sc​a​l​(D,d)S_{cal}(D,d) use all strings in dataset DD with descriptional complexity dd bounded above, as shown in the plots (App. K.4). Grey hexagons (⬣) represent data from 10 other models.

As shown in Fig. 4, there is a moderate-to-strong positive correlation between LLM performance on ∀\foralluto∃\exists∨⁣∧\lor\\!\landL and other logic-based benchmarks on a myriad of tasks such as autoformalization, logical reasoning, code generation, etc. The calibrated ∀\foralluto∃\exists∨⁣∧\lor\\!\landL score exhibits a strong, positive correlation (ρ≥0.7\rho\geq 0.7) with other static benchmarks on FL-based tasks, as well as reasoning tasks such as FOLIO. Notably, calculating the parameterized ∀\foralluto∃\exists∨⁣∧\lor\\!\landL score does not require hand-annotation unlike these benchmarks. Similar results appear in LogiEval for propositional logic, though the FOL version shows only a moderate correlation (0.5≤ρ<0.70.5\leq\rho<0.7). We traced this reduction to dataset imbalance, where 80%80\% of samples are from the positive class. Furthermore, the dataset is skewed towards lower difficulty. This leads to lower overall performance (and consequently correlation) of models like GPT-4o-mini that actually try to reason and provide no answers compared to models like LLama-3.1-8b, which mostly answered yes.

Figure 5: Predictive power of ∀\foralluto∃\exists∨⁣∧\lor\\!\landL w.r.t other benchmarks. Benchmark metrics appear after the colon.

Our results (Fig. 5) show that an LLM’s calibrated ∀\foralluto∃\exists∨⁣∧\lor\\!\landL score is a strong predictor of its performance on FL-based benchmarks. Our metric is also a more robust truth maintenance measure than length-dependent, NL-based metrics like BLEU scores (Papineni et al., 2002). For example, changing the generated NL ψ=\psi=“the weather status was sunny yesterday and is raining today” to ψ′=\psi^{\prime}=“the weather status was sunny yesterday and is not raining today” still achieves a high BLEU(ψ′,ψ)(\psi^{\prime},\psi) score of 0.74 (BLEU(ψ,ψ)=1(\psi,\psi)=1) but does not maintain truth. Even as a predictor for such metrics, ∀\foralluto∃\exists∨⁣∧\lor\\!\landL notably surpasses random-chance accuracy.

### 4.3 Evaluating Large Reasoning Models using ∀\foralluto∃\exists∨⁣∧\lor\\!\landL

Figure 6: Applying ∀\foralluto∃\exists∨⁣∧\lor\\!\landL with zero-shot prompts to LRMs on a small dataset of 400 strings.

Large Reasoning Models (LRMs) are LLMs that also perform some reasoning steps (e.g., search) as a part of their generation process. We assessed two SOTA LRMs – OpenAI’s o1 (OpenAI, 2024) and DeepSeek’s R1 (DeepSeek, 2024) – on §A1 and §A2 using ∀\foralluto∃\exists∨⁣∧\lor\\!\landL. Due to cost limitations, we regenerated a small dataset with 10 examples for each operator number for approximately 400 total examples. Our results (Fig. 6) show that even SOTA LRMs cannot maintain truth effectively in (𝒜∘ℐ)1​(φ0)(\mathcal{A}\circ\mathcal{I})^{1}(\varphi_{0}).

## 5 Related Work

Logical Reasoning RuleTaker (Clark et al., 2020) and ProntoQA (Saparov & He, 2023) generate datasets by using simple “if-then" and syllogisms rules to create reasoning questions. Similar grammars are used by LogicNLI (Tian et al., 2021) and CLUTRR (Sinha et al., 2019). LogiEval (Patel et al., 2024) uses fixed inference rules and LLMs to generate reasoning problems. Although these techniques are dynamic, they remain limited in generating interesting reasoning problems across different domains. In contrast, ∀\foralluto∃\exists∨⁣∧\lor\\!\landL is multi-dimensional, offering five distinct datasets, multiple customization options, and the ability to produce an infinite number of unique syntax trees.

FOLIO (Han et al., 2024) utilizes human experts to generate a set of reasoning questions based on real-world text sources. They generate questions in both NL and FL for propositional and first-order logic that require 7 levels of reasoning. A similar approach is employed by ReClor (Yu et al., 2020) and (Srivastava et al., 2023). A key weakness of these approaches is their reliance on human experts.

Autoformalization HumanEval is a popular benchmark for evaluating LLM capabilities of autoformalizing source code. LLM autoformalizations are evaluated via hand-written test cases. It has been shown by Liu et al. (2023) through the HumanEval+ dataset that the test cases in HumanEval are incomplete and can provide misleading rankings. StructuredRegex (Ye et al., 2020) used crowdsourcing for generating regex datasets. In contrast, ∀\foralluto∃\exists∨⁣∧\lor\\!\landL requires no human annotations and utilizes formal verifiers for checking the truth maintenance and thus does not share such drawbacks.

FOLIO({𝒜,ℐ}\\{\mathcal{A},\mathcal{I}\\}) (Han et al., 2024) tests the (auto/in)formalization abilities of LLMs by using hand-coded annotations of ⟨NL,FL⟩\langle\textit{NL}{},\textit{FL}{}\rangle pairs. However, as noted by the authors, they cannot check truth maintenance effectively and rely on an inference engine to compute truth values for each conclusion. ∀\foralluto∃\exists∨⁣∧\lor\\!\landL uses theorem provers to check equivalence and thus is sound in its accuracy evaluation.

MALLS (Yang et al., 2024) is an autoformalization dataset for first-order logic that was generated using GPT-4. Their use of LLMs for generating the data limits the diversity of the dataset since and the authors suggest to only use this dataset for fine-tuning and not for evaluation. In contrast, ∀\foralluto∃\exists∨⁣∧\lor\\!\landL generates correct FL and has a sound evaluation metric for truth maintenance.

Autoformalization approaches such LeanEuclid (Murphy et al., 2024), DTV (Zhou et al., 2024), LINC (Olausson et al., 2023), SatLM (Ye et al., 2020), Logic-LM (Pan et al., 2023) and others (Wu et al., 2022) utilize formal verifiers to provide sound evaluation metrics but utilize hand-coded datasets that limit their use in evaluating newer LLMs unlike ∀\foralluto∃\exists∨⁣∧\lor\\!\landL.

Informalization Wu et al. (2022) and ProofNet (Azerbayev et al., 2023) use static datasets to evaluate LLM informalization capabilities. They use metrics such as BLEU scores that are known to not be indicative of accuracy for FL-based tasks (Ren et al., 2020). Jiang et al. (2023) develop MMA, a dataset of formal and informal pairs generated using GPT-4. They note that their dataset is an approximate measure due to using LLMs without manual validation. In contrast, ∀\foralluto∃\exists∨⁣∧\lor\\!\landL is autonomous and provides sound measures of LLM capabilities w.r.t. truth maintenance.

## 6 Conclusion

We introduced ∀\foralluto∃\exists∨⁣∧\lor\\!\landL, a new benchmark for autonomously assessing LLM truth maintenance in formal language translation. ∀\foralluto∃\exists∨⁣∧\lor\\!\landL allows scalable data generation without human labeling and autonomously evaluates truth maintenance using formal verifiers to guarantee correctness. It is easily extensible and provides several prepackaged datasets and dataset generators to assess new LLMs quickly. Furthermore, our evaluation indicates that SOTA LLMs and LRMs are not performant in this task. Finally, we show that our metric is predictive of performance on other formal-language-based tasks and thus can be used as a surrogate benchmark for evaluating future LLMs.

Broader Impact ∀\foralluto∃\exists∨⁣∧\lor\\!\landL provides a robust framework for evaluating the suitability and safety of LLMs in FL-based tasks such as autoformalization and code generation. It also serves as a surrogate for estimating performance as LLMs emerge. Our work lays the foundation for developing autonomous evaluation techniques for LLMs in more flexible syntaxes, such as conversational AI.

Limitations and Future Work A limitation of our work is the use of formal verifiers: the equivalence problem for first-order logic is well known to be undecidable. We mitigate this by using an appropriate timeout and logging (only 0.66%0.66\% of our results experienced a timeout). This issue can be removed by using CFGs that generate decidable strings. An interesting application of ∀\foralluto∃\exists∨⁣∧\lor\\!\landL is using generated evaluations as datasets for back-translation, thereby improving the autoformalization capabilities of
