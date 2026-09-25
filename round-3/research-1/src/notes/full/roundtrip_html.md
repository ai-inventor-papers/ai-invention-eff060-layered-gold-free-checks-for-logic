URL: https://arxiv.org/html/2604.25031 | FULL FETCH | 2026-09-24T01:46:15Z
warning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
URL: https://arxiv.org/html/2604.25031
Type: HTML
Length: 78389 chars (truncated)

--- Content ---

##### Report GitHub Issue

×

Title:

Content selection saved. Describe the issue below:

Description:

Submit without GitHub Submit in GitHub

arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[ Back to arXiv ](/)

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) Report Issue [ Back to Abstract ](/abs/2604.25031v3 "Back to abstract page") [ Download PDF](/pdf/2604.25031v3 "Download PDF") [ ](javascript:toggleNavTOC\(\); "Toggle navigation") [ ](javascript:toggleReadingMode\(\); "Disable reading mode, show header and footer")

  1. Abstract
  2. 1 Introduction
  3. 2 Related Work
     1. Autoformalization.
     2. Verification-integrated repair.
     3. Faithfulness estimation.
     4. Roundtrip agreement.
     5. Semantic consistency checks.
  4. 3 Roundtrip Autoformalization Framework
     1. Target formalism and notation.
     2. Three translation stages.
     3. Roundtrip instance.
     4. Why roundtrip?
     5. Formal equivalence.
     6. Syntactic well-formedness as prerequisite.
  5. 4 Stage-Based Diagnosis and Iterative Repair
     1. 4.1 First-Failure Diagnosis
        1. First-failed stage.
        2. Diagnosis function.
        3. Scoped diagnostic reasoning.
     2. 4.2 Targeted Repair Operators
        1. Repair operators.
     3. 4.3 Iterative Repair Loop
        1. Iterative procedure.
  6. 5 Auxiliary Semantic Signal
     1. Bidirectional NLI as a semantic proxy.
     2. Diagnostic categories.
     3. Diagnostic, not supervisory.
  7. 6 Experimental Setup
     1. 6.1 Domains and Datasets
        1. From law to logic.
        2. Traffic corpus.
        3. Wildlife corpus.
     2. 6.2 Models and Configuration
        1. Formalism.
        2. Language models and repair.
        3. NLI model.
        4. Compute.
     3. 6.3 Ablation Conditions
  8. 7 Results and Analysis
     1. 7.1 Roundtrip Equivalence and Repair
        1. Method comparison.
     2. 7.2 Stage Diagnosis Distribution
     3. 7.3 Formal vs. Semantic Alignment
        1. Formal equivalence predicts semantic faithfulness.
     4. 7.4 Residual Failure Analysis
     5. 7.5 Why does GPT’s diagnosis collapse?
        1. Non-sequential prompt.
        2. Cross-model diagnosis.
  9. 8 Conclusion
  10. Domain scope.
  11. Verification is heuristic, not a proof.
  12. Rules are formalized in isolation.
  13. References
  14. A Prompt Templates
  15. B Schemas
     1. Construction process.
     2. Design principles.
     3. Excerpts.
  16. C Stage Diagnosis Details
  17. D NLI Category Detail
  18. E Drift Before Repair
  19. F Human Evaluation
     1. Faithfulness.
     2. Diagnosis.
  20. G Run-to-Run Variance
  21. H Data Availability



[ License: CC BY 4.0 ](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2604.25031v3 [cs.CL] 21 Sep 2026

# Faithful Autoformalization via Roundtrip Verification and Repair

Daneshvar Amrollahi† Email: [daneshvar@cs.stanford.edu](mailto:) Jerry Lopez‡ Email: [lopezjerry721@gmail.com](mailto:) Clark Barrett† Email: [barrett@cs.stanford.edu](mailto:) †Stanford University  ‡Independent Researcher 

###### Abstract

When an LLM formalizes natural language, how do we know the output is faithful? We propose a roundtrip verification approach which does not require ground-truth annotations: formalize a statement, translate the result back to natural language, re-formalize, and use a formal tool to check logical equivalence. When the two formalizations agree, this provides evidence of a faithful formalization. When they disagree, a stage-level diagnosis localizes the error to a specific translation step, and a scoped repair operator attempts to correct that step. We evaluate the framework on two statutory domains (the Texas Transportation Code and the Texas Parks and Wildlife Code) using two LLMs (Claude Opus 4.6 and GPT-5.2) with three repair baselines. Diagnosis-guided scoped repair is the most effective method, with effectiveness contingent on the reliability of the diagnosis function. Across both domains and both models, under our full repair system, rules that fail the equivalence check show 1.4×\times-2.5×\times more natural language inference (NLI) drift than rules that pass it.

## 1 Introduction

Autoformalization, the automatic translation of natural-language statements into formal, machine-checkable representations, is a rapidly growing area of NLP research (Wu et al., 2022). Yet a fundamental question remains largely unaddressed: _when an LLM produces a formalization, how do we know it faithfully captures the meaning of the original text?_ Existing evaluations rely on syntactic validity or downstream task success, neither of which directly tests semantic fidelity. Furthermore, when errors are found, repair is limited to end-to-end regeneration with no diagnosis of where meaning was lost (§2).

We propose a framework that addresses both problems (verification and repair) without requiring ground-truth formalizations. The key idea is simple (Figure 1): given a natural-language specification xx, we formalize it (T1T_{1}), translate the result back to natural language (T2T_{2}), and then re-formalize the result (T3T_{3}). We call each of these translation steps a _stage_. If the pipeline preserves meaning, the initial and final formalizations should be semantically equivalent. When they disagree, the point of divergence localizes the error to a specific stage, enabling both valuable diagnostic information as well as the possibility of _scoped repair_ : attempting to correct only the faulty component rather than regenerating everything. The framework is agnostic to the choice of the formalism: it applies whenever a target formalism admits an equivalence check, e.g., automated reasoning tools for logical formulas, type-checkers for proof assistants, test suites for code, etc.

We evaluate the framework on two statutory domains: 150 rules from the Texas Transportation Code and 77 rules from the Texas Parks and Wildlife Code. We use two LLMs, Claude Opus 4.6 (Anthropic) and GPT-5.2 (OpenAI). The target formalism is based on many-sorted first-order logic, with equivalence checked by an SMT solver Barrett et al. (2021). We compare our diagnosis-guided scoped repair against three baselines: no repair, repair with random stage selection, and full-pipeline regeneration. The results yield two principal findings:

  1. 1.

Formal equivalence predicts semantic faithfulness. Across both domains and both models, under our full repair system, rules that fail the equivalence check show 1.4×\times-2.5×\times more NLI drift than rules that pass it.

  2. 2.

Diagnosis-guided scoped repair achieves the highest verified-equivalence rate at the lowest cost when the diagnosis step is reliable. With Claude performing the pipeline, repair, and diagnosis, scoped repair leads on both domains. With GPT in those roles, diagnosis is unreliable, causing scoped repair to lose its lead. Replacing only the diagnosis step with Claude (keeping GPT for the pipeline and repair) restores scoped repair to a clear lead at lower cost on both domains.




Our contributions are: (i) A roundtrip verification framework that signals faithfulness of autoformalization without requiring ground-truth formalizations, instantiated with SMT in our experiments and applicable in principle to any target formalism with an equivalence check. (ii) A stage-level diagnosis and scoped repair procedure that localizes errors to individual translation steps. Repair is driven by formal equivalence alone. A bidirectional NLI signal serves as an independent post-hoc semantic check. (iii) An empirical study across two statutory domains and two model families that identifies the diagnosis step (not the pipeline or repair operators) as the bottleneck for scoped repair.

xxyorigy^{\mathrm{orig}}x′x^{\prime}yrty^{\mathrm{rt}}T1T_{1}T2T_{2}T3T_{3}≡Σ\equiv_{\Sigma} ?

Figure 1: Roundtrip loop. An input xx is formalized (T1T_{1}), reconstructed back to natural language (T2T_{2}), and re-formalized (T3T_{3}). The diagonal compares yorigy^{\mathrm{orig}} and yrty^{\mathrm{rt}} for semantic equivalence under Σ\Sigma.

## 2 Related Work

#### Autoformalization.

Autoformalization (Wu et al., 2022) has produced NL-formal benchmarks for proof assistants (Zheng et al., 2022; Azerbayev et al., 2023; Ying et al., 2024; Gao et al., 2025; Jiang et al., 2023a) and methods that use prover or compiler feedback to improve formalization quality (Jiang et al., 2023b; Lu et al., 2024; Yang et al., 2023; Murphy et al., 2024). Both lines score a formalization by whether it compiles or whether a downstream proof succeeds. Concurrent work formalizes non-mathematical text (Manas et al., 2024). Formal specifications have also been derived from natural-language system requirements (Cosler et al., 2023). These two efforts target temporal logic, whereas we target many-sorted first-order logic. Across these settings, fidelity to the source text is either untested or left to a human.

#### Verification-integrated repair.

Several systems couple verification with repair: Clover checks mutual consistency among LLM-generated code, docstrings, and formal annotations via a Dafny verifier (Sun et al., 2024), but it assumes the existence of the formalization from the start. ProofBridge iteratively repairs Lean proofs from type-checker feedback (Jana et al., 2026). DeepSeek-Prover-V1.5 uses RL with proof-assistant rewards (Xin et al., 2025). Self-debugging repairs code from execution results (Chen et al., 2024). In a related approach, LLMs translate a problem into a formal representation and a solver performs the reasoning (Pan et al., 2023; Olausson et al., 2023; Ye et al., 2023), with Logic-LM feeding solver error messages back to revise the formalization. Where feedback drives repair, the system regenerates the artifact it checked. To our knowledge, none localizes the error to a particular stage of a multi-step translation pipeline. A parallel self-refinement line (Madaan et al., 2023; Shinn et al., 2023; Pan et al., 2024) forgoes external verification entirely and uses the LLM as its own feedback source.

#### Faithfulness estimation.

Faithfulness in natural language generation (NLG) asks whether generated text is supported by its source, and it is widely studied (Maynez et al., 2020; Honovich et al., 2022). Support between two natural-language texts has no decision procedure, so faithfulness is estimated by a learned metric rather than decided. Our equivalence check is decided by a solver, and we use a learned metric only as an auxiliary diagnostic (§5).

#### Roundtrip agreement.

In machine translation, roundtrip agreement between a sentence and its back-translation estimates quality without a reference (Moon et al., 2020; Zhuo et al., 2023). Roundtrip correctness has been used as an evaluation signal in code generation when checking equivalence via test suites (Allamanis et al., 2024). Closest to our setting, Karia et al. (2025) assess LLMs with a roundtrip between formal expressions and natural language. Their roundtrip starts from a formal expression the system generates from a grammar, so that expression is its own reference. The framework therefore measures how well LLMs translate, rather than producing a trustworthy formalization of a given input. Our input is a human-written rule with no formal reference.

#### Semantic consistency checks.

Agreement among model outputs is also used as evidence of correctness, as in hallucination detection by self-consistency (Manakul et al., 2023). In autoformalization, recent work checks a formalization for semantic consistency with its source text. Li et al. (2024) generate several candidate formalizations of a mathematical statement and select one by self-consistency, combining agreement among the candidates with the similarity of each re-informalized candidate to the original. Chen et al. (2026) train a model to critique a formalization directly against the source text and to self-correct over successive revisions. Lu et al. (2025) train a scorer for the same purpose, which yields a learned alignment estimate rather than a decision. In each case the judgment applies to a formalization as a whole. We instead localize the failure to one translation step and repair only that step (§4).

## 3 Roundtrip Autoformalization Framework

#### Target formalism and notation.

Let 𝒳\mathcal{X} denote the set of natural-language strings. We use Σ\Sigma to represent the target formalism. The framework is agnostic to the specific choice of Σ\Sigma: all that is required is for there to be a notion of well-formed expressions and a notion of formal equivalence. Let 𝒴Σ\mathcal{Y}_{\Sigma} denote the set of well-formed Σ−\Sigma-expressions. We write ya≡Σyby_{a}\equiv_{\Sigma}y_{b} when two formulas ya,yb∈𝒴Σy_{a},y_{b}\in\mathcal{Y}_{\Sigma} are equivalent according to Σ\Sigma. For example, Σ\Sigma could be first-order logic with the standard notion of logical equivalence, or it could be a formalism based on dependent type theory such as that used by the Lean 4 theorem prover (Moura and Ullrich, 2021).

#### Three translation stages.

We model roundtrip autoformalization as a composition of three translation functions:

| T1\displaystyle T_{1} | :𝒳→𝒴Σ\displaystyle:\mathcal{X}\rightarrow\mathcal{Y}_{\Sigma} |  | (1)  
---|---|---|---|---  
| T2\displaystyle T_{2} | :𝒴Σ→𝒳\displaystyle:\mathcal{Y}_{\Sigma}\rightarrow\mathcal{X} |  | (2)  
| T3\displaystyle T_{3} | :𝒳→𝒴Σ\displaystyle:\mathcal{X}\rightarrow\mathcal{Y}_{\Sigma} |  | (3)  
  
where T1T_{1} performs _autoformalization_ , T2T_{2} performs _back-translation_ , and T3T_{3} performs _re-formalization_. All three stages operate under the same fixed target formalism Σ\Sigma. Each TiT_{i} is assumed to be _stateless_ : successive calls are mutually independent, with no shared memory or parameter updates between stages. The framework is agnostic to how each TiT_{i} is realized (e.g., an LLM, a rule-based translator, or a human annotator). Note that T1T_{1} and T3T_{3} share the same type: both translate from natural language strings to well-formed Σ\Sigma expressions. We consider them distinct to maintain generality and also so that stage-level diagnosis and scoped repair can refer unambiguously to the pipeline stage at which an error originates.

#### Roundtrip instance.

Consider again Figure 1. Given an input x∈𝒳x\in\mathcal{X}, the roundtrip pipeline produces:

| yorig\displaystyle y^{\mathrm{orig}} | =T1​(x)∈𝒴Σ\displaystyle=T_{1}(x)\in\mathcal{Y}_{\Sigma} |  | (4)  
---|---|---|---|---  
| x′\displaystyle x^{\prime} | =T2​(yorig)∈𝒳\displaystyle=T_{2}(y^{\mathrm{orig}})\in\mathcal{X} |  | (5)  
| yrt\displaystyle y^{\mathrm{rt}} | =T3​(x′)∈𝒴Σ.\displaystyle=T_{3}(x^{\prime})\in\mathcal{Y}_{\Sigma}. |  | (6)  
  
We refer to yorigy^{\mathrm{orig}} as the _original formalization_ and to yrty^{\mathrm{rt}} as the _roundtrip formalization_.

#### Why roundtrip?

The roundtrip construction yields a verification signal _without requiring ground-truth formalizations_. If T1T_{1} faithfully captures the meaning of xx, then back-translating and re-formalizing should recover the same formal semantics. When the two formalizations disagree, the point of divergence localizes the error.

#### Formal equivalence.

The primary verification question is whether yorig≡Σyrty^{\mathrm{orig}}\equiv_{\Sigma}y^{\mathrm{rt}}. If not, at least one translation stage has introduced or lost meaning, triggering a diagnosis step in which an LLM judge examines all four pipeline artifacts (x,yorig,x′,yrtx,y^{\mathrm{orig}},x^{\prime},y^{\mathrm{rt}}) to identify the responsible stage and produce a scoped explanation for repair (§4). Note that if the roundtrip is consistent with the original (i.e., yorig≡Σyrty^{\mathrm{orig}}\equiv_{\Sigma}y^{\mathrm{rt}}), correctness is still not guaranteed: the pipeline may stabilize at a semantically different fixed point where both formalizations agree yet neither faithfully represents xx. We therefore treat formal consistency as _necessary but not sufficient_. In §5, we discuss how to supplement roundtrip verification with an additional NLI-based check.

#### Syntactic well-formedness as prerequisite.

Before semantic equivalence can be checked, each formula must be syntactically valid according to Σ\Sigma. LLM-generated formulas occasionally violate grammar or type constraints. We allow up to five LLM-based correction attempts per formula, which in our experience suffices to ensure that at least one parsable encoding is produced.

## 4 Stage-Based Diagnosis and Iterative Repair

When yorig≢Σyrty^{\mathrm{orig}}\not\equiv_{\Sigma}y^{\mathrm{rt}}, the roundtrip instance is formally inconsistent, implying that at least one of the translation stages introduced semantic drift. However, the equivalence test alone does not identify which stage is responsible. We therefore introduce a stage-based diagnosis and repair procedure that localizes the failure and applies a targeted repair operator (Figure 2).

### 4.1 First-Failure Diagnosis

#### First-failed stage.

We view the pipeline as an ordered sequence of stages T1≺T2≺T3T_{1}\prec T_{2}\prec T_{3}. Intuitively, an error introduced earlier may propagate downstream, so we aim to identify the earliest stage at which the pipeline ceases to preserve semantics. Formally specifying natural-language semantics is beyond the scope of this work. Instead, diagnosis operates over the observable artifacts (x,yorig,x′,yrt)(x,y^{\mathrm{orig}},x^{\prime},y^{\mathrm{rt}}) and returns an index in {1,2,3}\\{1,2,3\\}.

#### Diagnosis function.

Let

| D:𝒳×𝒴Σ×𝒳×𝒴Σ→{1,2,3}×ℰD:\;\mathcal{X}\times\mathcal{Y}_{\Sigma}\times\mathcal{X}\times\mathcal{Y}_{\Sigma}\rightarrow\\{1,2,3\\}\times\mathcal{E} |  | (7)  
---|---|---|---  
  
be a diagnosis procedure which, given the roundtrip artifacts, predicts the first failed stage and produces an _explanation_ e∈ℰe\in\mathcal{E}, where ℰ\mathcal{E} is the set of possible explanations. In our system, DD is implemented as a constrained LLM-based judge and ℰ\mathcal{E} is simply 𝒳\mathcal{X}, the set of natural language strings. We enforce a _sequential checking protocol_ : DD must examine stages strictly in order (first comparing xx with yorigy^{\mathrm{orig}} for Stage 1, then yorigy^{\mathrm{orig}} with x′x^{\prime} for Stage 2, and finally x′x^{\prime} with yrty^{\mathrm{rt}} for Stage 3), halting at the first detected inconsistency.

#### Scoped diagnostic reasoning.

Critically, the explanation ee returned by DD is constrained to reference _only_ the artifacts relevant to the diagnosed stage. For instance, if Stage 2 is diagnosed as faulty, the explanation must describe the mismatch between yorigy^{\mathrm{orig}} and x′x^{\prime} without mentioning xx or yrty^{\mathrm{rt}}. This scoping ensures that the diagnostic feedback can be directly incorporated into the corresponding repair prompt without introducing confounding information from other pipeline stages.

### 4.2 Targeted Repair Operators

#### Repair operators.

A key design principle is that repairing stage ii invalidates all downstream artifacts produced by later stages; after repair, we therefore regenerate all subsequent stages to maintain a coherent pipeline state. Each repair operator receives the relevant artifacts together with the diagnostic explanation ee produced by DD:

| R1\displaystyle R_{1} | :𝒳×𝒴Σ×ℰ→𝒴Σ\displaystyle:\mathcal{X}\times\mathcal{Y}_{\Sigma}\times\mathcal{E}\rightarrow\mathcal{Y}_{\Sigma} |  | (8)  
---|---|---|---|---  
| R2\displaystyle R_{2} | :𝒴Σ×𝒳×ℰ→𝒳\displaystyle:\mathcal{Y}_{\Sigma}\times\mathcal{X}\times\mathcal{E}\rightarrow\mathcal{X} |  | (9)  
| R3\displaystyle R_{3} | :𝒳×𝒴Σ×ℰ→𝒴Σ\displaystyle:\mathcal{X}\times\mathcal{Y}_{\Sigma}\times\mathcal{E}\rightarrow\mathcal{Y}_{\Sigma} |  | (10)  
  
where R1R_{1} repairs the original formalization, R2R_{2} repairs the reconstructed NL, and R3R_{3} repairs the roundtrip formalization. Each RiR_{i} is instantiated as an LLM call operating under the same target formalism Σ\Sigma. The diagnostic explanation ee is injected into the repair prompt, instructing the model to address the _specific_ issues identified during diagnosis rather than regenerating blindly. This feedback-driven design enables targeted corrections: the repair prompt explicitly states what semantic mismatch was detected, and the LLM is required to resolve that mismatch while preserving other aspects of the encoding.

xxyorigy^{\mathrm{orig}}x′x^{\prime}yrty^{\mathrm{rt}}NL inputFormalNL reconFormalT1T_{1}T2T_{2}T3T_{3}A. Roundtrip autoformalizationSMT solveryorig≡Σyrty^{\mathrm{orig}}\equiv_{\Sigma}y^{\mathrm{rt}} ?✓ Success: self-consistentUNSATDiagnosis DD (LLM judge)B. Diagnosis and scoped repairSATx,yorig,x′,yrtx,\,y^{\mathrm{orig}},\,x^{\prime},\,y^{\mathrm{rt}}R1R_{1}x,yorig,ex,\,y^{\mathrm{orig}},\,e→\to new yorigy^{\mathrm{orig}}R2R_{2}yorig,x′,ey^{\mathrm{orig}},\,x^{\prime},\,e→\to new x′x^{\prime}R3R_{3}x′,yrt,ex^{\prime},\,y^{\mathrm{rt}},\,e→\to new yrty^{\mathrm{rt}}if i=1i{=}1if i=2i{=}2if i=3i{=}3rerun downstream TiT_{i}, and then SMT check Figure 2: The roundtrip autoformalization framework. (A) The pipeline produces two formal encodings of xx and an SMT solver checks them for equivalence. (B) On disagreement, diagnosis DD localizes the failed stage and repair operator RiR_{i} corrects it before re-checking.

### 4.3 Iterative Repair Loop

#### Iterative procedure.

We combine verification, diagnosis, and repair into an iterative loop that attempts to reach formal self-consistency within a bounded budget. Starting from (x,yorig,x′,yrt)(x,y^{\mathrm{orig}},x^{\prime},y^{\mathrm{rt}}), we repeatedly: (i) check whether yorig≡Σyrty^{\mathrm{orig}}\equiv_{\Sigma}y^{\mathrm{rt}}, (ii) if not, diagnose the first-failed stage, apply the corresponding repair operator, and regenerate downstream artifacts. The loop terminates when equivalence is achieved (success) or after a fixed maximum number of iterations (failure). We reiterate that when the procedure reports success, this does not guarantee correctness with respect to the original natural-language intent, but it does provide a measure of reassurance and confidence.

Algorithm 1 Roundtrip Verification and Stage-Based Repair

0: Natural-language input x∈𝒳x\in\mathcal{X}, formalism Σ\Sigma, max iterations KK

1: yorig←T1​(x)y^{\mathrm{orig}}\leftarrow T_{1}(x)

2: x′←T2​(yorig)x^{\prime}\leftarrow T_{2}(y^{\mathrm{orig}})

3: yrt←T3​(x′)y^{\mathrm{rt}}\leftarrow T_{3}(x^{\prime})

4: for k=1k=1 to KK do

5: if yorig≡Σyrty^{\mathrm{orig}}\equiv_{\Sigma}y^{\mathrm{rt}} then

6: Return SUCCESS, (yorig,x′,yrt)(y^{\mathrm{orig}},x^{\prime},y^{\mathrm{rt}})

7: end if

8: i←D⁡(x,yorig,x′,yrt)i\leftarrow D(x,y^{\mathrm{orig}},x^{\prime},y^{\mathrm{rt}}) {first-failed stage} 

9: if i=1i=1 then

10: yorig←R1​(x,yorig)y^{\mathrm{orig}}\leftarrow R_{1}(x,y^{\mathrm{orig}})

11: x′←T2​(yorig)x^{\prime}\leftarrow T_{2}(y^{\mathrm{orig}})

12: yrt←T3​(x′)y^{\mathrm{rt}}\leftarrow T_{3}(x^{\prime})

13: else if i=2i=2 then

14: x′←R2​(yorig,x′)x^{\prime}\leftarrow R_{2}(y^{\mathrm{orig}},x^{\prime})

15: yrt←T3​(x′)y^{\mathrm{rt}}\leftarrow T_{3}(x^{\prime})

16: else if i=3i=3 then

17: yrt←R3​(x′,yrt)y^{\mathrm{rt}}\leftarrow R_{3}(x^{\prime},y^{\mathrm{rt}})

18: end if

19: end for

20: Return FAILURE, (yorig,x′,yrt)(y^{\mathrm{orig}},x^{\prime},y^{\mathrm{rt}})

## 5 Auxiliary Semantic Signal

#### Bidirectional NLI as a semantic proxy.

We use natural language inference (NLI) to compare the original rule xx with the reconstructed natural-language description x′=T2​(yorig)x^{\prime}=T_{2}(y^{\mathrm{orig}}). NLI has been used as a faithfulness proxy across NLG tasks (Falke et al., 2019; Honovich et al., 2022; Laban et al., 2022). If the roundtrip preserves semantics, xx and x′x^{\prime} should be mutually entailing: xx entails x′x^{\prime} (nothing lost) and x′x^{\prime} entails xx (nothing spuriously added). We operationalize this using a BART-large model fine-tuned on MultiNLI, computing entailment probabilities in both directions:

| E→\displaystyle E_{\rightarrow} | =P⁡(entailment∣x,x′)\displaystyle=P(\text{entailment}\mid x,x^{\prime}) |  | (11)  
---|---|---|---|---  
| E←\displaystyle E_{\leftarrow} | =P⁡(entailment∣x′,x)\displaystyle=P(\text{entailment}\mid x^{\prime},x) |  | (12)  
  
along with contradiction probabilities C→C_{\rightarrow} and C←C_{\leftarrow}.

#### Diagnostic categories.

We derive Emin=min⁡(E→,E←)E_{\min}=\min(E_{\rightarrow},E_{\leftarrow}) for mutual entailment and Cmax=max⁡(C→,C←)C_{\max}=\max(C_{\rightarrow},C_{\leftarrow}) for contradiction. Each rule pair is classified into one of six categories via the decision tree in Figure 3 (first match wins). The six categories (_Contradiction_ , _Equivalent_ , _Strengthened_ , _Weakened_ , _Related_ , _Unrelated_) capture not only whether meaning is preserved but _how_ it drifts, a distinction that a binary test would obscure.

Cmax≥0.6C_{\max}\\!\geq\\!0.6Emin≥0.7∧Cmax<0.2E_{\min}\\!\geq\\!0.7\;\wedge\;C_{\max}\\!<\\!0.2E→≥0.6∧E←<0.4E_{\\!\rightarrow}\\!\geq\\!0.6\;\wedge\;E_{\\!\leftarrow}\\!<\\!0.4E←≥0.6∧E→<0.4E_{\\!\leftarrow}\\!\geq\\!0.6\;\wedge\;E_{\\!\rightarrow}\\!<\\!0.4Emin≥0.3∧Cmax<0.3E_{\min}\\!\geq\\!0.3\;\wedge\;C_{\max}\\!<\\!0.3ContradictionEquivalentStrengthenedWeakenedRelatedUnrelatedyesyesyesyesyesno no no no no 

Figure 3: NLI diagnostic decision tree (first match wins). Thresholds are conservative. _Equivalent_ demands strong bidirectional entailment (≥ 0.7{\geq}\,0.7) with near-zero contradiction (< 0.2{<}\,0.2), while _Contradiction_ requires high conflict (≥ 0.6{\geq}\,0.6).

#### Diagnostic, not supervisory.

NLI scores are used _only for post-hoc analysis_ , not as optimization targets. The repair loop (§4) operates solely on formal equivalence. NLI serves as an independent diagnostic lens, allowing us to ask: _when formal self-consistency is achieved, does semantic fidelity follow?_ This separation avoids optimizing for a noisy proxy while still providing a meaningful signal. In §7, we cross-tabulate formal equivalence with NLI categories to reveal where formal consistency diverges from semantic alignment.

## 6 Experimental Setup

### 6.1 Domains and Datasets

#### From law to logic.

We instantiate the framework on statutory regulation, which combines natural-language ambiguity with precise operational requirements. Applying statutes to facts is an established NLP task (Holzenberger et al., 2020). LLMs reason over statutes unreliably (Blair-Stanek et al., 2023), and their formalizations of legal text introduce axioms absent from the source (Wang et al., 2026). We evaluate on two corpora: traffic law and wildlife regulation. Any statutory domain admitting a formal equivalence check could serve equally well (§3).

#### Traffic corpus.

We evaluate on 150 rules drawn from the Texas Transportation Code. These rules govern vehicle behavior on roadways, covering lane positioning, passing maneuvers, signaling requirements, speed limits, and interactions with special vehicles (e.g., streetcars, school buses, emergency vehicles).

#### Wildlife corpus.

We evaluate on 77 rules drawn from the Texas Parks and Wildlife Code, a second statutory domain. These rules cover hunting and fishing licensing, season and bag-limit restrictions, equipment and method restrictions, and protected-species rules.

### 6.2 Models and Configuration

#### Formalism.

A _Satisfiability Modulo Theories_ (SMT) solver is a tool that can formally determine whether a set of first-order formulas is _satisfiable_ (i.e., whether there exists an interpretation that makes all of the formulas true) with respect to some background theory TT (Barrett et al., 2010). An SMT solver returns one of two verdicts: sat (a satisfying interpretation exists) or unsat (no such interpretation exists). SMT solvers can check whether two formulas φ\varphi and ψ\psi are logically equivalent (with respect to a theory TT), by checking the satisfiability of ¬(φ=ψ)\lnot(\varphi=\psi). If the result is unsat, no interpretation can distinguish the two formulas, certifying equivalence. If sat, the solver can return a counterexample demonstrating the difference. We construct a _domain schema_ for each corpus, a set of SMT declarations and definitions that provide a fixed vocabulary for that domain’s concepts. Schemas are produced semi-automatically: we draft a sketch by hand, scale it up with an LLM, and curate the result against a list of design principles to avoid common issues (Appendix B). We use the Z3 SMT solver (De Moura and Bjørner, 2008) (version 4.15.3) to check equivalence, and all queries resolve in under one second.

#### Language models and repair.

To assess framework generalizability across model families, we run the full pipeline with two frontier LLMs: Claude Opus 4.6 (Anthropic) and GPT-5.2 (OpenAI). Both use temperature 0.3. Each translation stage (T1T_{1}, T2T_{2}, T3T_{3}) and repair operator (R1R_{1}, R2R_{2}, R3R_{3}) is realized as a single stateless LLM call. The domain schema is injected into every prompt, and no context is carried between calls. All stages and operators use the same prompts for both models. The iterative repair loop (§4) runs for at most K=3K{=}3 iterations per rule, since gains flatten quickly. Each reported result is from a single run. We re-ran every experiment twice more, end to end, and report the spread in Appendix G.

#### NLI model.

For semantic comparison between original and reconstructed natural language, we use BART-large fine-tuned on MultiNLI (Lewis et al., 2020; Williams et al., 2018) (facebook/bart-large-mnli). Inference is performed bidirectionally as described in §5.

#### Compute.

Claude Opus 4.6 and GPT-5.2 are commercial APIs whose parameter counts are not publicly disclosed. NLI inference uses BART-large (approximately 0.4B parameters) on a single laptop. Per-repair LLM call counts, the dominant cost, are reported in Table 1.

### 6.3 Ablation Conditions

We compare four approaches:

  1. 1.

No Repair (Baseline 0): The roundtrip pipeline runs without any repair loop. The initial equivalence check result is final.

  2. 2.

Random Stage (Baseline 1): When the equivalence check fails, select a stage i∈{1,2,3}i\in\\{1,2,3\\} uniformly at random, repair it, and regenerate downstream stages. Repeat up to K=3K{=}3 times, stopping as soon as equivalence holds. No diagnosis is performed.

  3. 3.

Regenerate (Baseline 2): When the equivalence check fails, regenerate the entire pipeline from the original input xx and check again. Repeat up to K=3K{=}3 times, stopping as soon as equivalence holds. No diagnosis is performed.

  4. 4.

Full (Ours): We use the complete pipeline with diagnosis (§4.1) followed by targeted repair of the diagnosed stage. This is the system described in Algorithm 1.




All four approaches share the same initial roundtrip pass (identical yorig,x′,yrty^{\mathrm{orig}},x^{\prime},y^{\mathrm{rt}}). They differ only in the repair strategy applied to rules where the initial equivalence check returns SAT.

The two new baselines isolate two design choices in Full. Random Stage controls for the value of _diagnosis_ (which stage is selected for repair). Regenerate controls for the value of _scoping_ (re-running only the diagnosed stage rather than the whole pipeline).

## 7 Results and Analysis

### 7.1 Roundtrip Equivalence and Repair

Table 1 reports final equivalence outcomes for each experiment. Without repair, equivalence ranges from 44.7 % (Traffic / Claude) to 67.1 % (Wildlife / GPT). Each repair method substantially raises equivalence.

#### Method comparison.

The most effective repair method depends on the model, and the same pattern holds across both domains. For Claude, Full leads on both UNSAT count and cost-per-repair. For GPT with same-model diagnosis, Regenerate surpasses Full on UNSAT count, and Full is the most expensive of the three methods. This split reflects the diagnosis distribution: GPT repeatedly diagnoses T1T_{1}, which forces regenerating T2T_{2} and T3T_{3} downstream on every iteration (§7.2). The third row of each GPT block reports results from a cross-model approach, where Claude performs only the diagnosis step. We analyze this approach in §7.5.

|  |  | Final UNSAT count (%) | LLM calls / repair  
---|---|---|---|---  
Domain | Model | Diagnoser | None | Random | Regen | Full | Random | Regen | Full  
Traffic (N=150N{=}150) | Claude | Claude | 67 (44.7) | 100 (66.7) | 97 (64.7) | 128 (85.3) | 12.27 | 19.90 | 7.21  
GPT | GPT | 92 (61.3) | 118 (78.7) | 127 (84.7) | 124 (82.7) | 9.77 | 10.54 | 14.56  
GPT | Claude | — | — | — | 136 (90.7) | — | — | 7.86  
Wildlife (N=77N{=}77)†\dagger | Claude | Claude | 48 (62.3) | 60 (77.9) | 63 (81.8) | 66 (85.7) | 11.67 | 12.20 | 9.50  
GPT | GPT | 51 (67.1) | 59 (77.6) | 65 (85.5) | 60 (78.9) | 12.75 | 11.57 | 26.44  
GPT | Claude | — | — | — | 72 (94.7) | — | — | 6.05  
Table 1: Roundtrip equivalence outcomes across two domains and four repair conditions. The Model column performs pipeline and repair. The Diagnoser performs diagnosis. Bold marks the per-row best. †\daggerClaude rows use all 77 rules. GPT rows use N=76N{=}76: one rule yielded no Stage-1 encoding under GPT and is excluded from every GPT count.

### 7.2 Stage Diagnosis Distribution

The two models diagnose pipeline failures very differently, and the pattern is consistent across both domains (Table 3, Appendix C). Claude distributes its diagnoses across all three stages. GPT collapses almost all of its diagnoses onto T1T_{1}. The Random baseline distributes approximately uniformly across stages in every case, so the concentration is a property of the diagnosis function, not the data. The distribution does not say whether those diagnoses are correct. Appendix F reports a human evaluation of the diagnosed stage.

Repairing T1T_{1} cascades: it forces a fresh T2T_{2} and a fresh T3T_{3} on every iteration, while repairing T3T_{3} does not. GPT’s T1T_{1}-heavy diagnosis therefore behaves like full-pipeline regeneration plus a diagnosis call, which explains Full’s higher cost than Regenerate for GPT (Table 1). §7.5 tests whether this T1T_{1} concentration is a property of the protocol or of the model.

### 7.3 Formal vs. Semantic Alignment

Figure 4: NLI drift rate among UNSAT (formally equivalent) and SAT (not equivalent) post-repair rules under Full repair, one domain-model pair. The annotation above each pair is the SAT-to-UNSAT drift ratio. Domain / Model | Method | UNSAT | SAT | Ratio  
---|---|---|---|---  
Traffic / Claude | Random | 14.0% | 20.0% | 1.43  
Regenerate | 12.4% | 20.8% | 1.68  
Full | 09.4% | 13.6% | 1.45  
Traffic / GPT | Random | 15.3% | 28.1% | 1.84  
Regenerate | 15.0% | 26.1% | 1.74  
Full | 13.7% | 34.6% | 2.52  
Full (Claude dx)∗\ast | 12.5% | 35.7% | 2.86  
Wildlife / Claude | Random | 25.0% | 35.3% | 1.41  
Regenerate | 25.4% | 28.6% | 1.13  
Full | 24.2% | 45.5% | 1.88  
Wildlife / GPT | Random | 18.6% | 35.3% | 1.89  
Regenerate | 20.0% | 54.5% | 2.73  
Full | 20.0% | 37.5% | 1.88  
Full (Claude dx)∗\ast | 19.4% | 75.0%‡\ddagger | 3.86‡\ddagger  
Pooled |  | 16.2% | 28.7% | 1.78  
Table 2: Post-repair drift rate (share of rules NLI-classified as Unrelated or Contradiction), split by SMT verdict. SAT denotes every rule not verified equivalent. Ratio is SAT drift divided by UNSAT drift. ∗\astCross-model: GPT pipeline + Claude diagnosis (§7.5). ‡\ddaggerThis SAT pool has only 4 rules, so the rate is noisy.

We examined the rate of every NLI category in each pool (Appendix D, Table 4). Related and Weakened distribute similarly between UNSAT and SAT. Strengthened concentrates in UNSAT. This reflects an artifact of the back-translation: the reconstructed NL tends to use the schema’s predicate names verbatim, which produces wordier text than the original lawyer-written rule. NLI interprets the wordier reconstruction as a stricter version of the original, so NLI-Strengthened arises even when the formalization is faithful. Only Unrelated and Contradiction discriminate cleanly between UNSAT and SAT, motivating their use as our Drift measure.

#### Formal equivalence predicts semantic faithfulness.

Figure 4 shows that under Full repair, SAT rules drift 1.45×\times-2.52×\times more often than UNSAT rules across the four domain-model pairs. Pooled across these four Full configurations, SAT rules drift 2.03 times more often than UNSAT rules. The same pattern holds when baselines are included: pooled across all 14 rows in Table 2, SAT rules still drift 1.78 times more often than UNSAT rules. The pattern is consistent across both model families and both statutory domains. Appendix F reports a human evaluation of faithfulness against the equivalence verdict. Appendix E shows the same gap before any repair runs. Formal equivalence does not guarantee semantic fidelity, but it predicts it.

### 7.4 Residual Failure Analysis

A rule is _residual_ if none of Random, Regenerate, or Full repairs it within K=3K{=}3 iterations. 26 unique rules are residual across the four domain-model pairs. Manual inspection identifies four recurring patterns of intrinsic rule difficulty: schema vocabulary gaps (the schema lacks a needed predicate, so T1T_{1} and T3T_{3} approximate with different substitutes), compound conditions (disjunctive or nested premises where T1T_{1} and T3T_{3} encode the AND/OR structure differently), exception clauses (rules that suspend an obligation under a condition, where T2T_{2} back-translates the exception as a positive restatement and T3T_{3} then encodes the inverted meaning), and conditional thresholds (numeric thresholds that depend on another variable, where the pipeline often drops the dependency). The bottleneck is intrinsic rule structure, not iteration budget.

### 7.5 Why does GPT’s diagnosis collapse?

The GPT/Full underperformance we report in §7.2 stems from a single design point: the diagnosis function. GPT selects the first translation step T1T_{1} in 83 % of iterations on Traffic and 97 % on Wildlife, regardless of where the actual error occurs (Table 3). Two hypotheses are compatible with this: the prompt’s sequential checking protocol biases GPT toward the first stage examined, or GPT has an intrinsic preference for blaming initial formalization. We test both directly.

#### Non-sequential prompt.

We rewrite the diagnosis prompt to drop the “examine T1T_{1} first, then T2T_{2}, then T3T_{3}, halt at first failure” instruction and ask the judge to consider all three stages together. Re-running diagnosis on the existing GPT SAT pools, T1T_{1} selection drops from 84 % to 9 % on Traffic and from 96 % to 16 % on Wildlife. These baselines are first-iteration rates over the re-diagnosed pools of 58 and 25 rules, so they differ from the 83 % and 97 % pooled over all iterations in Table 3. The protocol explains most of the collapse.

#### Cross-model diagnosis.

We rerun the Full repair loop on the existing GPT pipeline outputs and change one thing: Claude acts as the diagnosis judge, while GPT still writes every formalization and performs every repair. Equivalence rises on both domains and cost per repair falls on both (Table 1, last row of each block). Scoped repair recovers the lead it had lost to Regenerate. The diagnosis function was the bottleneck, not the pipeline or the repair operators.

## 8 Conclusion

We evaluated a roundtrip verification and scoped repair framework on two statutory domains and two model families. Two findings stand out. First, formal equivalence is a useful predictor of semantic faithfulness: across the four Full configurations spanning both domains and both models, SAT rules show 1.4×\times-2.5×\times more NLI drift than UNSAT rules. Second, diagnosis-guided scoped repair achieves the highest verified-equivalence rate at the lowest cost when the diagnosis function is reliable. On Claude pipelines, same-model scoped repair wins on both domains. On GPT pipelines, the diagnosis step is the bottleneck for scoped repair (not the pipeline or repair operators): replacing only the diagnoser with a different model restores scoped repair’s lead at lower cost (§7.5). About 16 % of formally equivalent rules still drift on NLI. Future work could integrate additional checks into the repair loop, such as NLI or an LLM-based check, rather than relying on formal equivalence alone.

## Limitations

#### Domain scope.

Both corpora are English statutory text from Texas. Mathematical autoformalization benchmarks typically operate one theorem at a time, where a human author can read the formal statement and verify it against the informal one. Statutory text involves a large domain schema (close to 200 predicates) and operational ambiguity, so hand verification at scale is impractical and a ground-truth-free faithfulness signal is most directly motivated by this setting. We do not claim the framework transfers to other genres such as code or scientific text without further evaluation.

#### Verification is heuristic, not a proof.

The roundtrip check detects when T1​(x)T_{1}(x) and T3​(T2​(T1​(x)))T_{3}(T_{2}(T_{1}(x))) disagree, but it cannot detect errors that affect both stages in the same way. For example, if T1T_{1} silently drops a conjunct of xx and T3T_{3} reproduces the same omission from the back-translation, the equivalence check passes despite both being wrong. The NLI cross-check (§5) is a partial mitigation, but it relies on a general-purpose model with known lexical-overlap biases (McCoy et al., 2019) on legal text, so its drift signal is itself noisy.

#### Rules are formalized in isolation.

Statutory text can be heavily cross-referenced. A rule may incorporate definitions from another section, suspend obligations stated elsewhere, or impose conditions on rules outside its own clause. Our pipeline formalizes one rule at a time and treats each rule as self-contained. Faithful formalization of densely cross-referenced rules likely requires presenting the connected cluster of rules together as input, rather than a single rule node. We leave this to future work.

## Risks

Autoformalization outputs generated by this system, including those that pass roundtrip verification, should not be used in safety-critical applications, including but not limited to autonomous systems, medical devices, or safety case documentation, without independent review by a qualified formal methods expert. Regarding environmental impact, the pipeline relies on API-based LLM inference and a locally-run SMT solver. We did not train or fine-tune any models, so the compute footprint is bounded by inference calls.

## Acknowledgements

This work was supported in part by the Stanford Center for Automated Reasoning (Centaur).

## Use of AI Assistants

Claude Code was carefully used to assist with code implementation, LaTeX formatting, and paraphrasing during paper writing. All scientific content, experimental design, analysis, and claims are entirely the authors’ own.

## References

  * Allamanis et al. (2024) M. Allamanis, S. Panthaplackel, and P. Yin Unsupervised evaluation of code llms with round-trip correctness.  In Proceedings of the 41st International Conference on Machine Learning,  ICML’24.  Cited by: §2. 
  * Azerbayev et al. (2023) Z. Azerbayev, B. Piotrowski, H. Schoelkopf, E. W. Ayers, D. Radev, and J. Avigad ProofNet: autoformalizing and formally proving undergraduate-level mathematics.  External Links: 2302.12433, [Link](https://arxiv.org/abs/2302.12433) Cited by: §2. 
  * Barrett et al. (2021) C. Barrett, R. Sebastiani, S. Seshia, and C. Tinelli Satisfiability modulo theories.  In Handbook of Satisfiability, Second Edition, A. Biere, M. J. H. Heule, H. van Maaren, and T. Walsh (Eds.),  Frontiers in Artificial Intelligence and Applications, Vol. 336, pp. 825–885.  External Links: [Link](http://theory.stanford.edu/~barrett/pubs/BSST21.pdf) Cited by: §1. 
  * Barrett et al. (2010) C. Barrett, A. Stump, and C. Tinelli The SMT-LIB standard: version 2.0.  In Proceedings of the 8th International Workshop on Satisfiability Modulo Theories,  Cited by: §6.2. 
  * Blair-Stanek et al. (2023) A. Blair-Stanek, N. Holzenberger, and B. Van Durme Can GPT-3 perform statutory reasoning?.  In Proceedings of the Nineteenth International Conference on Artificial Intelligence and Law,  ICAIL ’23, New York, NY, USA, pp. 22–31.  External Links: ISBN 9798400701979, [Link](https://doi.org/10.1145/3594536.3595163), [Document](https://dx.doi.org/10.1145/3594536.3595163) Cited by: §6.1. 
  * Chen et al. (2026) G. Chen, W. Jing, X. Chen, X. Zhao, R. Song, C. Li, K. Fan, D. Liu, and M. Liao ReForm: reflective autoformalization with prospective bounded sequence optimization.  In The Fourteenth International Conference on Learning Representations,  External Links: [Link](https://openreview.net/forum?id=KfxRzCmRSX) Cited by: §2. 
  * Chen et al. (2024) X. Chen, M. Lin, N. Schärli, and D. Zhou Teaching large language models to self-debug.  In The Twelfth International Conference on Learning Representations,  External Links: [Link](https://openreview.net/forum?id=KuPixIqPiq) Cited by: §2. 
  * Cosler et al. (2023) M. Cosler, C. Hahn, D. Mendoza, F. Schmitt, and C. Trippel Nl2spec: interactively translating unstructured natural language to temporal logics with large language models.  In Computer Aided Verification, C. Enea and A. Lal (Eds.),  Cham, pp. 383–396.  External Links: ISBN 978-3-031-37703-7 Cited by: §2. 
  * De Moura and Bjørner (2008) L. De Moura and N. Bjørner Z3: an efficient smt solver.  In Proceedings of the Theory and Practice of Software, 14th International Conference on Tools and Algorithms for the Construction and Analysis of Systems,  TACAS’08/ETAPS’08, Berlin, Heidelberg, pp. 337–340.  External Links: ISBN 3540787992 Cited by: §6.2. 
  * Falke et al. (2019) T. Falke, L. F. R. Ribeiro, P. A. Utama, I. Dagan, and I. Gurevych Ranking generated summaries by correctness: an interesting but challenging application for natural language inference.  In Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics, A. Korhonen, D. Traum, and L. Màrquez (Eds.),  Florence, Italy, pp. 2214–2220.  External Links: [Link](https://aclanthology.org/P19-1213/), [Document](https://dx.doi.org/10.18653/v1/P19-1213) Cited by: §5. 
  * Gao et al. (2025) G. Gao, Y. Wang, J. Jiang, Q. Gao, Z. Qin, T. Xu, and B. Dong Herald: a natural language annotated lean 4 dataset.  In The Thirteenth International Conference on Learning Representations,  External Links: [Link](https://openreview.net/forum?id=Se6MgCtRhz) Cited by: §2. 
  * Holzenberger et al. (2020) N. Holzenberger, A. Blair-Stanek, and B. V. Durme A dataset for statutory reasoning in tax law entailment and question answering.  External Links: 2005.05257, [Link](https://arxiv.org/abs/2005.05257) Cited by: §6.1. 
  * Honovich et al. (2022) O. Honovich, R. Aharoni, J. Herzig, H. Taitelbaum, D. Kukliansy, V. Cohen, T. Scialom, I. Szpektor, A. Hassidim, and Y. Matias TRUE: re-evaluating factual consistency evaluation.  In Proceedings of the 2022 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, M. Carpuat, M. de Marneffe, and I. V. Meza Ruiz (Eds.),  Seattle, United States, pp. 3905–3920.  External Links: [Link](https://aclanthology.org/2022.naacl-main.287/), [Document](https://dx.doi.org/10.18653/v1/2022.naacl-main.287) Cited by: §2, §5. 
  * Jana et al. (2026) P. Jana, K. Kale, A. E. Tanriverdi, C. Song, S. Vishwanath, and V. Ganesh ProofBridge: auto-formalization of natural language proofs in lean via joint embeddings.  External Links: 2510.15681, [Link](https://arxiv.org/abs/2510.15681) Cited by: §2. 
  * Jiang et al. (2023a) A. Q. Jiang, W. Li, and M. Jamnik Multilingual mathematical autoformalization.  External Links: 2311.03755, [Link](https://arxiv.org/abs/2311.03755) Cited by: §2. 
  * Jiang et al. (2023b) A. Q. Jiang, S. Welleck, J. P. Zhou, T. Lacroix, J. Liu, W. Li, M. Jamnik, G. Lample, and Y. Wu Draft, sketch, and prove: guiding formal theorem provers with informal proofs.  In The Eleventh International Conference on Learning Representations,  External Links: [Link](https://openreview.net/forum?id=SMa9EAovKMC) Cited by: §2. 
  * Karia et al. (2025) R. Karia, D. R. Bramblett, D. Dobhal, and S. Srivastava AutoEval: autonomous evaluation of LLMs for truth maintenance and reasoning tasks.  In The Thirteenth International Conference on Learning Representations,  External Links: [Link](https://openreview.net/forum?id=iv1TpRCJeK) Cited by: §2. 
  * Laban et al. (2022) P. Laban, T. Schnabel, P. N. Bennett, and M. A. Hearst SummaC: re-visiting NLI-based models for inconsistency detection in summarization.  Transactions of the Association for Computational Linguistics 10, pp. 163–177.  External Links: [Link](https://aclanthology.org/2022.tacl-1.10/), [Document](https://dx.doi.org/10.1162/tacl%5Fa%5F00453) Cited by: §5. 
  * Lewis et al. (2020) M. Lewis, Y. Liu, N. Goyal, M. Ghazvininejad, A. Mohamed, O. Levy, V. Stoyanov, and L. Zettlemoyer BART: denoising sequence-to-sequence pre-training for natural language generation, translation, and comprehension.  In Proceedings of the 58th Annual Meeting of the Association for Computational Linguistics, D. Jurafsky, J. Chai, N. Schluter, and J. Tetreault (Eds.),  Online, pp. 7871–7880.  External Links: [Link](https://aclanthology.org/2020.acl-main.703/), [Document](https://dx.doi.org/10.18653/v1/2020.acl-main.703) Cited by: §6.2. 
  * Li et al. (2024) Z. Li, Y. Wu, Z. Li, X. Wei, X. Zhang, F. Yang, and X. Ma Autoformalize mathematical statements by symbolic equivalence and semantic consistency.  In The Thirty-eighth Annual Conference on Neural Information Processing Systems,  External Links: [Link](https://openreview.net/for
