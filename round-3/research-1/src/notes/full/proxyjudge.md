URL: https://arxiv.org/html/2606.09449 | FULL FETCH | 2026-09-24T01:36:08Z
warning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
URL: https://arxiv.org/html/2606.09449
Type: HTML
Length: 79678 chars (truncated)

--- Content ---

##### Report GitHub Issue

×

Title:

Content selection saved. Describe the issue below:

Description:

Submit without GitHub Submit in GitHub

arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[ Back to arXiv ](/)

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) Report Issue [ Back to Abstract ](/abs/2606.09449v1 "Back to abstract page") [ Download PDF](/pdf/2606.09449v1 "Download PDF") [ ](javascript:toggleNavTOC\(\); "Toggle navigation") [ ](javascript:toggleReadingMode\(\); "Disable reading mode, show header and footer")

  1. Abstract
  2. 1 Introduction
  3. 2 Related Work
     1. Autoformalization and neural theorem proving.
     2. Inference-time refinement and judge calibration.
  4. 3 Proposed Framework
     1. 3.1 Judges and Local Properties
     2. 3.2 Reflective Refinement Loop
        1. Prover-grounded return policy.
  5. 4 Proxy Theory Grounded in Explicit Language and Inference
     1. 4.1 Intrinsic Properties and the Proxy Score
     2. 4.2 Refinement and the Drift Assumption
     3. 4.3 Plateau Convergence and Correctness
  6. 5 Empirical Evaluation
     1. 5.1 Experimental Setup
        1. Benchmarks and provers.
        2. Formalization and judge backbones.
        3. Metrics.
        4. Baseline.
     2. 5.2 Main Results
        1. Our refinement framework improves Pass Rate across the seven backbones and four datasets.
        2. Refinement gain is inversely correlated with baseline Pass Rate, irrespective of whether the benchmark is math or explanation.
        3. Refinement helps every backbone, but absolute Pass Rates scale with backbone capacity.
     3. 5.3 Judge Calibration
        1. The proxy trajectory follows the same per-iteration shape as the external oracle, even though they measure quality on different scales.
        2. Where the proxy and oracle curves disagree, the proxy gives credit for repairs the oracle does not.
     4. 5.4 Judge Capacity
        1. Swapping the judge for a stronger or weaker model changes the final Pass Rate by much less than swapping the dataset does.
     5. 5.5 Effect of Judge Context Size
        1. Letting the judge see the entire formal candidate does not help compared to letting it see only the local module being scored.
     6. 5.6 Decomposed versus Scalar Feedback
        1. A per-axis verdict outperforms a single end-to-end score wherever the baseline Pass Rate is below saturation, and matches it where the baseline already saturates.
  7. 6 Conclusion
  8. References
  9. A Auxiliary Bounds
     1. A.1 Audit-Unit Framework
  10. B Microscopic Motivation for the Drift Assumption
  11. C Amplification by Repeated Judging
  12. D Operationalization Details
     1. D.1 Operational Objects
        1. Intrinsic property vector in practice.
     2. D.2 Judge Calibration Protocol
     3. D.3 Refinement Operators and Bounded Regress
     4. D.4 Estimating Drift Parameters
  13. E Proofs
  14. F Theory-Aligned Aggregates
  15. G Dataset Details
  16. H Direct Few-Shot Baseline Configuration
  17. I Extended Judge-Calibration Analysis
     1. The oracles are themselves proxies, not ground truth.
     2. Oracle and proxy bands measure different noise sources.
     3. Proxy and oracle move in opposite directions on saturating Isabelle ProntoQA.
     4. Cross-seed oracle voting reduces single-sample LLM-judge noise in the calibration setup.



[ License: arXiv.org perpetual non-exclusive license ](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2606.09449v1 [cs.CL] 08 Jun 2026

# Reasoning without Gold Standards:   
A Proxy-Judge Theory of Autoformalization

Lei Xu  Affiliation: Idiap Research Institute, Switzerland  Affiliation: École Polytechnique Fédérale de Lausanne (EPFL), Switzerland  Email: [lei.xu@idiap.ch](mailto:) Xin Quan  Affiliation: Idiap Research Institute, Switzerland  Email: [xin.quan@idiap.ch](mailto:) André Freitas  Affiliation: Idiap Research Institute, Switzerland  Affiliation: Department of Computer Science, University of Manchester, United Kingdom  Affiliation: CRUK National Biomarker Centre, University of Manchester, United Kingdom  Email: [andre.freitas@idiap.ch](mailto:)

###### Abstract

Complex reasoning tasks increasingly require systems to produce outputs whose correctness cannot be judged by exact match against a single reference. Autoformalization (AF) is a representative example; it asks a model to translate informal mathematical or logical reasoning into a formally checkable object, yet expert-validated formalizations do not scale beyond toy cases and a single informal argument can admit many valid formal renderings. Progress therefore depends on whether partial, structured proxies can substitute for exact references.

We introduce a reference-free proxy-judge framework for AF that replaces gold-standard matching with a vector of per-axis property checks. The framework organizes the proxy along three structural scopes that cover global properties of the elicited object, per-module properties internal to its sub-components, and cross-domain properties that re-align it to the informal source, and aggregates each axis into a verdict vector. The vector drives a reflective refinement loop in which a violated coordinate routes the controller to a matching repair target, so each iteration changes only what is judged wrong.

Under bounded judge noise, the expected intrinsic gap contracts geometrically to a noise-dependent plateau. Across seven formalization backbones on miniF2F, ProofNet, e-SNLI, and ProntoQA, refinement consistently lifts Pass Rate over the single-shot ICL baseline, and the per-axis proxy outperforms a matched scalar proxy on benchmarks where the baseline has room to improve. Structured proxy judgments therefore provide both a practical refinement signal and a theoretical handle on convergence when exact references are unavailable.

## 1 Introduction

Reasoning benchmarks often assume that correctness can be specified in advance: an expert provides a reference output, and predictions are judged by comparison to it. For highly specialized domains such as mathematics and formal logic, this assumption breaks once complexity scales, since constructing a reference may itself require solving the task: choosing a representation, recovering implicit assumptions, resolving notation and background facts, and certifying coherence inside a larger theory (Wu et al., 2022; Jiang et al., 2023; Azerbayev et al., 2023). Beyond toy cases, gold-standard annotation is therefore not only expensive but can also become fundamentally non-scalable.

The difficulty is compounded by non-uniqueness. A single informal argument can admit many valid renderings, differing in definitions, encodings, lemma decompositions, proof strategies, or library alignments (Zhang et al., 2025). Any one gold standard captures only one point in this equivalence class, so exact-match evaluation can penalize correct alternatives while collapsing distinct kinds of errors into a single score.

This creates a scalability dilemma: the tasks most worth evaluating are also those for which exhaustive expert annotation is least feasible. Evaluation must therefore move from reference reproduction to structured evidence of correctness. Instead of asking whether a candidate matches a canonical solution, we ask whether it satisfies localized, task-internal constraints that provide proxy evidence of correctness without requiring a complete expert reference for every instance.

Autoformalization (AF) is a representative case in which this dilemma is especially sharp. AF asks a model to translate an informal mathematical or logical argument into a formally checkable object (Wu et al., 2022; Jiang et al., 2023; Azerbayev et al., 2023). A proof assistant can reject malformed syntax, inconsistent types, broken bindings, and failed elaborations (Polu and Sutskever, 2020; Yang et al., 2023); however, the kernel alone cannot decide whether the formal artifact preserves the intended meaning of the informal source (Zhang et al., 2025). At the same time, obtaining expert-written formalizations at scale is prohibitive, and treating one formalization as the unique reference is conceptually wrong because many correct formal renderings may exist.

The key observation of this paper is that AF is globally hard to annotate but locally amenable to systematic assessment once the linguistic and reasoning properties have been made explicit. The signal that drives evaluation already exists inside the formal system itself. Once an argument is rendered as explicit statements, inferential links, and grounding into a shared context, correctness decomposes into finitely many locally checkable constraints whose violations admit bounded, targeted repair. AF is therefore hard to verify globally but easy to verify locally once it is made explicit, and this asymmetry is what we exploit.

Building on this observation, we introduce a reference-free proxy-judge framework for AF. The framework decomposes evaluation into audit-unit axes organized by three structural scopes: global properties of the elicited object, per-module properties internal to its sub-components, and cross-domain properties that align it back to the informal source and the per-instance fact context. The resulting verdict vector drives a reflective refinement loop in which each detected violation routes the controller toward a localized repair, turning refinement into constraint-directed repair rather than undifferentiated retry.

Figure 1: Reflective Refinement Loop. At each iteration the system proposes a candidate formalization, scores it on a fixed set of property axes, finds the worst-scoring axis, and applies a repair targeted to that axis.

From this local-verifiability gap, we decompose AF evaluation into a finite vector of intrinsic properties drawn from the language and inference system itself, and estimate that vector with a family of specialized judges acting on small, controlled contexts. Recent work shows that calibrated LLM judges can stand in for human evaluation in formal mathematical reasoning (Zhang et al., 2025; Zheng et al., 2023), and that step-level verifiers outperform outcome-only scalars for learned reasoning signals (Lightman et al., 2024; Uesato et al., 2022). Both observations fit a reflective refinement loop that proposes a candidate, measures its properties, localizes a violation, and repairs it (see Figure 1); we analyze the convergence properties of this loop when the judges themselves are imperfect.

In summary, the contributions are organized as follows.

  1. 1.

_Framework._ We design a reference-free framework for autoformalization that decomposes evaluation into audit-unit axes spanning three structural scopes—global, per-module, and cross-domain to the informal source—and closes the loop with a prover-grounded return policy, casting refinement as constraint-directed optimization in which each violation maps to an identifiable repair target (Section 3).

  2. 2.

_Convergence analysis._ Under a drift assumption that we adopt as a primitive of the analysis (Assumption 2, with microscopic motivation in Appendix B), we give a drift-Lyapunov argument showing the expected intrinsic gap contracts geometrically to an O⁡(η)O(\eta) plateau (Theorem 1); the bound targets the asymptotic gap height, while concurrent work on LLM-verifier loops (Dantas et al., 2025) bounds expected iteration count.

  3. 3.

_Empirical result._ We evaluate seven formalization backbones on four datasets, and our refinement loop consistently outperforms the single-shot ICL baseline; on the frontier backbones, average gains reach 19%19\% on ProofNet and 16%16\% on e-SNLI. Within the loop, pass rate further rises by 8.28.2–8.4%8.4\% on ProofNet and 1717–18%18\% on e-SNLI when we replace a single end-to-end judge with a per-axis proxy. The granularity gain captures a sizeable share of the loop’s overall gain over the ICL baseline on these two benchmarks (1515–21%21\% on ProofNet, 22–25%25\% on e-SNLI), which indicates that structured per-axis feedback, rather than raw refinement compute, is the main source of the empirical advantage (Section 5.6).




## 2 Related Work

#### Autoformalization and neural theorem proving.

LLM-guided autoformalization (Wu et al., 2022; Jiang et al., 2023; Azerbayev et al., 2023) and neural proof search (Polu and Sutskever, 2020; Zheng et al., 2022; Yang et al., 2023) use proof assistants as a binary success signal. Reference-free iterative refinement was recently formalized for full-theorem AF with four scalar acceptance criteria (Zhang et al., 2026), and explanation-style AF gains were reported on Isabelle natural-language inference (Quan et al., 2025). These frameworks leave open how to exploit partial, local structure when proof completion is unavailable or the judge is noisy. We instead target proxy signals induced by explicit inference constraints and decompose evaluation into a property-vector that a per-axis controller can act on.

#### Inference-time refinement and judge calibration.

Self-Refine and Reflexion use verbal feedback without weight updates (Madaan et al., 2023; Shinn et al., 2023); Tree-of-Thought (Yao et al., 2023) and self-consistency (Wang et al., 2023) aggregate or score candidate traces. Step-level process supervision (Uesato et al., 2022; Lightman et al., 2024) and calibrated LLM-as-judge (Zheng et al., 2023; Ouyang et al., 2022; Bai et al., 2022) push evaluation below the outcome level. These methods motivate local evaluation, but they report no finite property vector whose per-axis errors govern refinement, and no convergence statement under imperfect judges. Our framework supplies both ingredients: a structured per-axis verdict ξ⁡(P^)∈[0,1]m\xi(\widehat{P})\in[0,1]^{m} organized by global, per-module, and cross-domain scopes, whose violated coordinate routes the controller to the corresponding repair target, and a drift-Lyapunov analysis that exposes the asymptotic noise floor. Concurrent work on LLM-verifier loops (Dantas et al., 2025) bounds expected iteration count rather than asymptotic gap height.

Figure 2: Implicit-to-Explicit Transition. Correctness is checked at three scopes: the whole object, each module, and the alignment back to the informal source n​lnl and context Γ\Gamma. Each scope has its own judge.

## 3 Proposed Framework

We now formalize the framework introduced in Section 1 as a staged operator Π\Pi together with a judge family Ξ\Xi acting on a structured elicited object (see Figure 2). Concretely, Π\Pi takes the informal input n​lnl together with a per-instance fact context Γ\Gamma, and produces

| P^=Π⁡(n​l,Γ)={M1,M2,…,MK},\widehat{P}=\Pi(nl,\Gamma)=\\{M_{1},M_{2},\ldots,M_{K}\\}, |  | (1)  
---|---|---|---  
  
where each module MM holds a coherent set of explicit statements p^j\widehat{p}_{j} together with their declarations and the references they make into Γ\Gamma. The context Γ\Gamma collects per-instance facts surfaced for the example at hand, such as “a violin is an instrument”. We write P^i\widehat{P}_{i} for the iteration-ii candidate and P^⋆\widehat{P}^{\star} for a correct elicited target, both living in the ambient space ℰ\mathcal{E}; Γ\Gamma remains fixed across iterations.

Because the same n​lnl admits many valid formalizations, exact-match scoring against any single reference P^⋆\widehat{P}^{\star} unfairly punishes alternatives. We instead evaluate P^\widehat{P} along a finite vector of property probes computable on the explicit side. Some probes are kernel-side and deterministic, while others cross back to the informal source. None consults a reference formalization, so the family bypasses gold-standard scarcity at the global level. Section 3.1 formalizes the probes as judges, and Section 3.2 closes the loop into a reflective refinement cycle (Figure 1).

### 3.1 Judges and Local Properties

A finite family of mm judges Ξ={ξ1,…,ξm}\Xi=\\{\xi_{1},\ldots,\xi_{m}\\}, each a computable functional ξk:ℰ→[0,1]\xi_{k}:\mathcal{E}\to[0,1], evaluates properties of P^\widehat{P} and its bindings; in this paper we use m=8m=8, with one judge per audit axis, partitioned by the three structural scopes introduced in Section 1.

_Global scope_ (judge consumes the whole elicited object P^\widehat{P}; kernel-decided):

  * •

ξglb​(P^)\xi_{\mathrm{glb}}(\widehat{P}): the prover completes the full elaboration and inference pass on P^\widehat{P} without crash, timeout, or non-termination.

  * •

ξdoc​(P^)\xi_{\mathrm{doc}}(\widehat{P}): P^\widehat{P} is a structurally valid source artifact under the prover’s document conventions (declaration order, scope brackets, presence of required resources).




_Per-module scope_ (judge consumes a single module M∈P^M\in\widehat{P}; kernel-decided):

  * •

ξsyn​(M)\xi_{\mathrm{syn}}(M): every statement inside module MM is accepted by the parser and rule schemas.

  * •

ξtyp​(M)\xi_{\mathrm{typ}}(M): the types and schemas declared inside MM are mutually consistent across its statements.

  * •

ξbnd​(M)\xi_{\mathrm{bnd}}(M): the inferential links inside MM wire its local premises and conclusions through structurally complete steps and preserve variable bindings.




_Cross-domain scope_ (judge additionally consults the informal source n​lnl and per-instance context Γ\Gamma; externally judged):

  * •

ξgnd​(M,n​l,Γ)\xi_{\mathrm{gnd}}(M,nl,\Gamma): every predicate, constant, or symbol used inside MM traces back to an entity introduced by n​lnl or by Γ\Gamma.

  * •

ξsp​(M,n​l)\xi_{\mathrm{sp}}(M,nl): each explicit statement inside MM aligns with some implicit claim in n​lnl, with the alignment constructed by the judge.

  * •

ξcov​(n​l,P^)\xi_{\mathrm{cov}}(nl,\widehat{P}): the key claim units of n​lnl are represented explicitly somewhere in P^\widehat{P}.




Each violation points to an identifiable repair target.

### 3.2 Reflective Refinement Loop

A controller aggregates these localized signals, picks which subcomponent to repair next, and repeats the cycle until an acceptance threshold is met. We index the AF process by ii with parameters θi\theta_{i} that collect prompts, transformations, or policy parameters. At each iteration:

  1. 1.

Propose. Produce P^i\widehat{P}_{i} via Πθi​(n​l,Γ)\Pi_{\theta_{i}}(nl,\Gamma).

  2. 2.

Measure. Evaluate the judge vector ξ⁡(P^i)=(ξ1​(P^i),…,ξm​(P^i))\xi(\widehat{P}_{i})=(\xi_{1}(\widehat{P}_{i}),\ldots,\xi_{m}(\widehat{P}_{i})).

  3. 3.

Localize. Select a target subcomponent tit_{i} responsible for the strongest violation.

  4. 4.

Repair. Update θi+1←Refine⁡(θi,ti,ξ⁡(P^i))\theta_{i+1}\leftarrow\mathrm{Refine}(\theta_{i},t_{i},\xi(\widehat{P}_{i})).




The loop is constraint-directed, with update axes drawn from the finite constraint families that Section 4 formalizes; Figure 1 summarizes the resulting pipeline.

#### Prover-grounded return policy.

Because the LLM-evaluated axes ξsp,ξcov\xi_{\mathrm{sp}},\xi_{\mathrm{cov}} may report false violations, a repair guided by them can break a kernel-verifiable axis without the judge noticing. We therefore return the latest iterate that the prover accepts, and roll back whenever the prover moves from accept to reject between consecutive iterations.

## 4 Proxy Theory Grounded in Explicit Language and Inference

The reflective loop of Section 3 converges at a rate determined by judge noise and a contraction parameter.

### 4.1 Intrinsic Properties and the Proxy Score

To measure intrinsic progress without a reference formalization, we attach to the elicited object P^∈ℰ\widehat{P}\in\mathcal{E} a latent quality vector 𝒒:ℰ→[0,1]m\boldsymbol{q}:\mathcal{E}\to[0,1]^{m} whose components measure the satisfaction of mm intrinsic properties. Each component qk​(P^)q_{k}(\widehat{P}) records the fraction of audit units of property kk that pass on P^\widehat{P}, in a strict modular sense in which a single internal violation fails its host module.

Each component ξk​(P^)∈[0,1]\xi_{k}(\widehat{P})\in[0,1] aggregates the binary judge verdicts on the audit units of property kk, with the audit-unit definition and aggregation formula detailed in Appendix A.

We adopt 𝒒⁡(P^⋆)=𝟏\boldsymbol{q}(\widehat{P}^{\star})=\mathbf{1} as the marker of intrinsic correctness. Fixing weights w∈ℝ≥0mw\in\mathbb{R}^{m}_{\geq 0} with ‖w‖1=1\|w\|_{1}=1, the intrinsic progress measure is μ⋆​(P^)=⟨w,𝒒⁡(P^)⟩\mu^{\star}(\widehat{P})=\langle w,\boldsymbol{q}(\widehat{P})\rangle with observable counterpart μ^​(P^)=⟨w,𝝃​(P^)⟩\widehat{\mu}(\widehat{P})=\langle w,\boldsymbol{\xi}(\widehat{P})\rangle.

###### Assumption 1 (Audit sufficiency of the property vector).

𝒒⁡(P^)=𝟏\boldsymbol{q}(\widehat{P})=\mathbf{1} implies P^\widehat{P} passes every prover-decidable check and aligns with the informal source n​lnl on every cross-domain axis within the judge family Ξ\Xi of Section 3.1.

Theorem 1 is a score-level result and uses only this audit-level sufficiency.

### 4.2 Refinement and the Drift Assumption

A refinement step takes the current object and the judge readings and returns the next iterate, P^i+1=𝖱𝖾𝖿𝗂𝗇𝖾⁡(P^i,𝝃⁡(P^i))\widehat{P}_{i+1}=\mathsf{Refine}(\widehat{P}_{i},\boldsymbol{\xi}(\widehat{P}_{i})); 𝖱𝖾𝖿𝗂𝗇𝖾\mathsf{Refine} folds the Localize and Repair sub-steps of Section 3.2 (target selection on 𝝃\boldsymbol{\xi}, parameter update to θi+1\theta_{i+1}, and reproposal through Πθi+1\Pi_{\theta_{i+1}}), and the analysis below uses only its input/output signature.

Following the drift-Lyapunov tradition for stochastic optimization with bounded noise (Bottou et al., 2018), we adopt an expected-contraction-with-residual form on the gap dynamics.

###### Assumption 2 (Bounded regress with contractive drift).

There exist constants λ∈(0,1]\lambda\in(0,1] and b≥0b\geq 0, independent of ii and of η\eta, such that 𝔼⁡[gi+1∣P^i]\displaystyle\mathbb{E}\\!\left[\,g_{i+1}\mid\widehat{P}_{i}\,\right] ≤(1−λ)​gi+b​η,\displaystyle\leq(1-\lambda)\,g_{i}+b\,\eta, (2) gi\displaystyle g_{i} :=1−μ⋆​(P^i),\displaystyle:=1-\mu^{\star}(\widehat{P}_{i}), for all ii, where η\eta is the per-audit-unit judge misclassification rate of Assumption 4.

The factor 1−λ1-\lambda contracts the remaining gap by a fixed fraction each round, and the additive b​ηb\,\eta absorbs the residual judge noise and imperfect-localization terms. The microscopic motivation in Appendix B suggests that the underlying per-step repair probability scales as ρ≥ρ0−c​η\rho\geq\rho_{0}-c\eta, so the contraction rate λ\lambda implicitly degrades as η\eta grows. We treat λ\lambda and bb as constants in the analysis and interpret the plateau bound b​η/λb\eta/\lambda as valid in the regime η≪ρ0/c\eta\ll\rho_{0}/c.

### 4.3 Plateau Convergence and Correctness

Iterating the drift inequality across ii produces a closed-form bound on the intrinsic gap gi:=1−μ⋆​(P^i)g_{i}:=1-\mu^{\star}(\widehat{P}_{i}).

###### Theorem 1 (Geometric convergence to a noise-dependent plateau).

Under Assumption 2, the expected intrinsic gap satisfies 𝔼⁡[gi+1]\displaystyle\mathbb{E}[g_{i+1}] ≤(1−λ)​𝔼​[gi]+b​η,\displaystyle\leq(1-\lambda)\,\mathbb{E}[g_{i}]+b\,\eta, (3) lim supi→∞𝔼⁡[gi]\displaystyle\limsup_{i\to\infty}\mathbb{E}[g_{i}] ≤b​ηλ,\displaystyle\leq\tfrac{b\,\eta}{\lambda}, lim infi→∞𝔼⁡[μ⋆​(P^i)]\displaystyle\liminf_{i\to\infty}\mathbb{E}[\mu^{\star}(\widehat{P}_{i})] ≥1−b​ηλ,\displaystyle\geq 1-\tfrac{b\,\eta}{\lambda}, and the plateau approaches 11 when η→0\eta\to 0.

Each round shrinks the expected gap by a factor 1−λ1-\lambda until further contraction is balanced by the noise residual b​η/λb\eta/\lambda, so the plateau height is proportional to η\eta (proof in Appendix E). Reducing η\eta therefore tightens the plateau directly, and repeated judging provides such a reduction.

###### Lemma 1 (Majority vote reduces effective uncertainty).

Under Assumption 4, write ηeff\eta_{\mathrm{eff}} for the per-audit-unit misclassification rate of the majority vote over TT independent calls on the same audit unit. Then ηeff≤exp⁡(−2​T​(12−η)2).\eta_{\mathrm{eff}}\leq\exp\\!\bigl(-2T\bigl(\tfrac{1}{2}-\eta\bigr)^{2}\bigr). (4)

Substituting Equation 4 into the plateau bound yields

| 1−lim infi→∞𝔼⁡[μ⋆​(P^i)]≲ηeffλ.1-\liminf_{i\to\infty}\mathbb{E}[\mu^{\star}(\widehat{P}_{i})]\;\lesssim\;\frac{\eta_{\mathrm{eff}}}{\lambda}. |  | (5)  
---|---|---|---  
  
In the zero-noise limit, 𝔼⁡[μ⋆​(P^i)]→1\mathbb{E}[\mu^{\star}(\widehat{P}_{i})]\to 1 certifies that the refinement converges to objects that pass every audit-sufficient probe of Assumption 1.

Table 1: Backbones and Judge Model. Seven formalization backbones and one fixed judge. Llama and DeepSeek identifiers are abbreviated (e.g. Llama-3.3-70B); other names match the released identifiers. Model | Family | Tier (Architecture)  
---|---|---  
Formalization Backbones  
GPT-5.4 | GPT | Frontier (Proprietary)  
DeepSeek-V4 | DeepSeek | Frontier MoE  
DeepSeek-V3.1 | DeepSeek | Frontier MoE  
Llama-4-17B | Llama | Mid-Tier MoE  
Llama-3.3-70B | Llama | Compact Dense  
Llama-3.1-8B | Llama | Compact Dense  
Qwen-3.5-9B | Qwen | Compact Dense  
Judge Model  
GPT-5.4-mini | GPT | Mid-Tier (Proprietary)  
Table 2: Per-Backbone Pass Rate (%): Baseline / Ours. Results are shown in Mean ±\pm std across seeds. ↑\uparrow: ours exceeds baseline. Bold marks the higher mean in each cell. Cross-backbone μ⋆\mu^{\star} aggregate is in Appendix F. Backbone | miniF2F ↑\uparrow | ProofNet ↑\uparrow | e-SNLI ↑\uparrow | ProntoQA ↑\uparrow  
---|---|---|---|---  
GPT-5.4 | 91.4±\pm1.1 / 97.7±\pm0.2↑\uparrow | 68.1±\pm3.9 / 88.5±\pm2.0↑\uparrow | 98.0±\pm1.0 / 99.7±\pm0.6↑\uparrow | 100.0±\pm0.0 / 100.0±\pm0.0  
DeepSeek-V4 | 83.6±\pm0.4 / 91.5±\pm0.2↑\uparrow | 49.8±\pm2.7 / 70.5±\pm3.3↑\uparrow | 78.3±\pm1.1 / 100.0±\pm0.0↑\uparrow | 100.0±\pm0.0 / 100.0±\pm0.0  
DeepSeek-V3.1 | 79.9±\pm2.1 / 88.5±\pm2.6↑\uparrow | 53.9±\pm0.9 / 69.2±\pm1.4↑\uparrow | 75.3±\pm2.5 / 100.0±\pm0.0↑\uparrow | 100.0±\pm0.0 / 100.0±\pm0.0  
Llama-4-17B | 70.9±\pm1.6 / 84.3±\pm1.7↑\uparrow | 39.9±\pm2.2 / 59.5±\pm4.6↑\uparrow | 69.0±\pm1.0 / 99.0±\pm1.0↑\uparrow | 96.3±\pm0.3 / 100.0±\pm0.0↑\uparrow  
Llama-3.3-70B | 67.6±\pm1.4 / 73.4±\pm2.2↑\uparrow | 8.1±\pm1.6 / 10.4±\pm2.2↑\uparrow | 62.7±\pm4.0 / 83.0±\pm3.6↑\uparrow | 89.2±\pm1.3 / 98.3±\pm1.1↑\uparrow  
Llama-3.1-8B | 57.0±\pm2.4 / 61.6±\pm3.4↑\uparrow | 12.1±\pm1.4 / 14.0±\pm2.9↑\uparrow | 72.7±\pm2.1 / 83.7±\pm3.5↑\uparrow | 97.0±\pm1.0 / 99.2±\pm1.0↑\uparrow  
Qwen-3.5-9B | 82.4±\pm2.3 / 91.4±\pm1.4↑\uparrow | 57.1±\pm4.0 / 65.6±\pm1.3↑\uparrow | 77.3±\pm5.7 / 79.7±\pm2.3↑\uparrow | 97.3±\pm0.8 / 98.7±\pm0.3↑\uparrow  
Table 3: Judge-Capacity Ablation. Per-benchmark rows. Results are shown in Mean ±\pm std across seeds; μ⋆±\mu^{\star}\pm is cross-fixture std. Bold: column maximum. Data | Judge | 𝝁𝟎⋆↑\boldsymbol{\mu^{\star}_{0}}\,\uparrow | 𝝁∞⋆↑\boldsymbol{\mu^{\star}_{\infty}}\,\uparrow | Pass Rate ↑\uparrow  
---|---|---|---|---  
ProofNet | Llama-3.3-70B | 0.90±\pm0.10 | 0.91±\pm0.13 | 65.9±\pm5.3  
GPT-5.4 | 0.86±\pm0.13 | 0.88±\pm0.16 | 66.5±\pm2.0  
GPT-5.4-mini | 0.90±\pm0.10 | 0.92±\pm0.13 | 69.2±\pm1.4  
ProntoQA | Llama-3.3-70B | 0.93±\pm0.07 | 0.98±\pm0.06 | 100.0±\pm0.0  
GPT-5.4 | 0.93±\pm0.07 | 0.99±\pm0.04 | 100.0±\pm0.0  
GPT-5.4-mini | 1.00±\pm0.03 | 1.00±\pm0.00 | 100.0±\pm0.0  
Table 4: Locality Ablation. Judge sees only the local module (local) vs. the whole candidate (global, LJ=LAFL_{J}{=}L_{\mathrm{AF}}). Results are shown in Mean ±\pm std across seeds; μ⋆±\mu^{\star}\pm is cross-fixture std. Bold: column maximum. Data | Judge Scope | 𝝁𝟎⋆↑\boldsymbol{\mu^{\star}_{0}}\,\uparrow | 𝝁∞⋆↑\boldsymbol{\mu^{\star}_{\infty}}\,\uparrow | Pass Rate ↑\uparrow  
---|---|---|---|---  
ProofNet | Global | 0.90±\pm0.10 | 0.92±\pm0.12 | 65.9±\pm0.6  
Local | 0.91±\pm0.10 | 0.92±\pm0.12 | 66.1±\pm3.1  
ProntoQA | Global | 0.99±\pm0.02 | 1.00±\pm0.00 | 100.0±\pm0.0  
Local | 0.99±\pm0.03 | 1.00±\pm0.02 | 100.0±\pm0.0  
  
## 5 Empirical Evaluation

### 5.1 Experimental Setup

#### Benchmarks and provers.

We evaluate on two formal-proof benchmarks, miniF2F (Zheng et al., 2022) and ProofNet (Azerbayev et al., 2023), and two natural-language-IR benchmarks, e-SNLI (Camburu et al., 2018) with a typed neo-Davidsonian IR and ProntoQA (Saparov and He, 2023) with FOL. miniF2F and ProofNet are formalized in Lean 4 (de Moura and Ullrich, 2021), whose kernel-level elaboration decides the kernel-verified coordinates of qq (ξglb,ξdoc,ξsyn,ξtyp,ξbnd\xi_{\mathrm{glb}},\xi_{\mathrm{doc}},\xi_{\mathrm{syn}},\xi_{\mathrm{typ}},\xi_{\mathrm{bnd}}). e-SNLI and ProntoQA are formalized in Isabelle/HOL (Nipkow et al., 2002), whose higher-order logic kernel together with the bidirectional ATP oracle certifies the cross-domain coordinates (ξgnd,ξsp,ξcov\xi_{\mathrm{gnd}},\xi_{\mathrm{sp}},\xi_{\mathrm{cov}}) on the IR side. Sample sizes, splits, and per-dataset sampling protocols are in Appendix G.

#### Formalization and judge backbones.

Seven formalization backbones span four families and three scale tiers: a frontier API tier (GPT-5.4, DeepSeek-V4, DeepSeek-V3.1), a mid-tier MoE point (Llama-4-17B), and three compact-dense open-weight models (Llama-3.3-70B, Llama-3.1-8B, Qwen-3.5-9B); see Table 1 for full upstream identifiers. The judge is fixed to GPT-5.4-mini in all experiments except the judge-capacity ablation of Section 5.4, with low-temperature decoding (≤0.2\leq 0.2) and the same per-axis prompt across all experiments.

#### Metrics.

We report three metrics in each results table. 𝝁𝟎⋆\boldsymbol{\mu^{\star}_{0}} and 𝝁∞⋆\boldsymbol{\mu^{\star}_{\infty}} are the audit-unit pass rate at the initial and final iterates P^0\widehat{P}_{0} and P^∞\widehat{P}_{\infty}. Pass Rate is the fraction of instances for which the prover accepts P^∞\widehat{P}_{\infty}. Every setting is run with three random seeds; table captions specify which standard deviation is reported in each column.

#### Baseline.

Following prior autoformalization work (Wu et al., 2022; Jiang et al., 2023; Zhang et al., 2026; Quan et al., 2025), we use a single in-context learning prompt with three demonstrations per setting (Appendix H) as the baseline, keeping the backbone, prompt, and judge model identical to those used by the refinement loop. This matched-setup comparison is preferred over cross-paper absolute pass rates, which are not directly comparable when each system targets a different proof assistant on non-overlapping splits.

(a) DS-V3.1 / miniF2F

(b) DS-V3.1 / ProofNet

(c) DS-V3.1 / e-SNLI

(d) DS-V3.1 / ProntoQA

(e) Qwen-9B / miniF2F

(f) Qwen-9B / ProofNet

(g) Qwen-9B / e-SNLI

(h) Qwen-9B / ProntoQA

Figure 3: Refinement Trajectories. Each panel shows the proxy μ^\widehat{\mu} (solid) and the external oracle pass rate (dashed) per iteration, on DeepSeek-V3.1 (top) and Qwen-3.5-9B (bottom); the band is the mean ±\pm std across three seeds. The yy-axis range differs per panel, so values are not comparable across panels. Table 5: Per-Axis vs. Scalar Verdict. Pass Rate (%). Rows above and below the midrule differ only in the verdict format: per-axis vector (decomposed) or single end-to-end score (scalar). Results are shown in Mean ±\pm std across seeds. Bold: column maximum. Method | Judge | miniF2F ↑\uparrow | ProofNet ↑\uparrow | e-SNLI ↑\uparrow | ProntoQA ↑\uparrow  
---|---|---|---|---|---  
Scalar | GPT-5.4 | 84.7±\pm0.2 | 58.8±\pm2.4 | 81.0±\pm2.7 | 100.0±\pm0.0  
GPT-5.4-mini | 86.9±\pm0.4 | 58.4±\pm1.1 | 82.0±\pm1.0 | 100.0±\pm0.0  
Decomposed (Ours) | GPT-5.4 | 86.1±\pm1.6 | 67.0±\pm1.1 | 98.0±\pm1.0 | 100.0±\pm0.0  
GPT-5.4-mini | 88.5±\pm0.7 | 66.8±\pm1.7 | 100.0±\pm0.0 | 100.0±\pm0.0  
  
### 5.2 Main Results

Per-backbone Pass Rate across the seven formalization backbones and four datasets is shown in Table 2. We can see that:

#### Our refinement framework improves Pass Rate across the seven backbones and four datasets.

Across the seven backbones and four datasets, our refinement framework exceeds the single-shot ICL baseline on most settings. The frontier three backbones gain +19%+19\% on ProofNet and +16%+16\% on e-SNLI on average. These gains are an order of magnitude above the per-row seed std we observe in Table 2, so the improvement is not a within-seed fluctuation but a stable shift of the candidate that the proposer alone cannot deliver.

#### Refinement gain is inversely correlated with baseline Pass Rate, irrespective of whether the benchmark is math or explanation.

ProofNet (frontier baseline 5050–68%68\%) gains 1515–21%21\%; e-SNLI (baseline 7575–98%98\%) gains 22–25%25\%; miniF2F (baseline 8080–91%91\%) gains only 66–9%9\%; ProntoQA stays at the dataset ceiling. The largest gains land on the two lowest-baseline benchmarks, one math (ProofNet) and one explanation (e-SNLI); the math benchmark with the higher baseline (miniF2F) yields less than half the gain of ProofNet. The size of the refinement gain therefore tracks how much headroom the baseline leaves rather than which family the benchmark belongs to.

#### Refinement helps every backbone, but absolute Pass Rates scale with backbone capacity.

The frontier three backbones reach 6969–89%89\% on ProofNet, ≥99.7%\geq 99.7\% on e-SNLI, 100%100\% on ProntoQA, and 8888–98%98\% on miniF2F, whereas the two compact-dense Llamas remain at ≤14%\leq 14\% on ProofNet even after refinement. The same compact-dense backbones nonetheless gain +5+5–6%6\% on miniF2F, +2+2–9%9\% on ProntoQA, and +11+11–20%20\% on e-SNLI. Backbone capacity therefore bounds the absolute Pass Rate, but the gain from refinement does not vanish at smaller scales.

### 5.3 Judge Calibration

Because autoformalization lacks a scalable gold-standard corpus at the sizes used here, reference-free evaluation through LLM-judge proxies is the established practice in the closest concurrent work (Zhang et al., 2025; Zhang et al., 2026; Quan et al., 2025). To check how well our proxy reflects the true correctness signal, we construct an approximate stand-in for the gold label, which we call the _oracle_ , and compare its per-iteration pass rate against the proxy score μ^\widehat{\mu} on two representative backbones (DeepSeek-V3.1, Qwen-3.5-9B). The oracle is chosen per benchmark to match what each prover can decide: on the Lean math benchmarks (miniF2F, ProofNet) it is a GPT-5.4 judge that compares the candidate against the gold Lean reference, and on the Isabelle natural-language benchmarks (e-SNLI, ProntoQA) it queries the candidate’s axiomatization with the ATP in both directions and checks the verdict against the dataset label. We can see from Figure 3 that:

#### The proxy trajectory follows the same per-iteration shape as the external oracle, even though they measure quality on different scales.

On every panel of Figure 3, the proxy μ^\widehat{\mu} and the oracle pass rate trace qualitatively the same per-iteration curve. Both rise sharply over the first few iterations and flatten by iteration 33–55, reproducing the geometric approach to a plateau predicted by Theorem 1, with the aggregate proxy plateau at 0.890.89–0.990.99 across math and explanation (Table 6). The two curves nonetheless differ in absolute level because the proxy and the oracle score quality on incompatible scales, so the yy-axis offset between the solid and dashed curves reflects this scale mismatch rather than the noise floor η\eta.

#### Where the proxy and oracle curves disagree, the proxy gives credit for repairs the oracle does not.

On Qwen-3.5-9B’s ProntoQA panel the oracle stays flat while the proxy continues to climb. The proxy credits any per-axis repair its judge accepts, including surface-level fixes that tighten the axiomatization, whereas the oracle only changes when the ATP’s verdict flips on the dataset label. Seed-band and judge-noise diagnostics are reported in Appendix I.

### 5.4 Judge Capacity

Fixing DeepSeek-V3.1 as the formalizer, we run the loop under three judge models that span a wide capacity range: the open-weight Llama-3.3-70B, the mid-sized GPT-5.4-mini default, and the frontier GPT-5.4, as shown in Table 3. The same DeepSeek-V3.1 formalizer carries through Sections 5.5 and 5.6. We can see that:

#### Swapping the judge for a stronger or weaker model changes the final Pass Rate by much less than swapping the dataset does.

On ProofNet, the three judges span only 3.3%3.3\% (Llama-3.3-70B 65.9±5.3%65.9\pm 5.3\%, GPT-5.4-mini 69.2±1.4%69.2\pm 1.4\%, GPT-5.4 66.5±2.0%66.5\pm 2.0\%). The cross-dataset spread on the same DeepSeek-V3.1 backbone is ≈19\approx 19–31%31\%, an order of magnitude larger, so a mid-sized judge already exhausts the available signal under audit-unit feedback.

### 5.5 Effect of Judge Context Size

We contrast the default per-axis judge (which sees only the local audit unit) against a context-expanded variant that receives the entire elicited object P^\widehat{P} as LJ=LAFL_{J}{=}L_{\mathrm{AF}}, as shown in Table 4. We can see that:

#### Letting the judge see the entire formal candidate does not help compared to letting it see only the local module being scored.

ProntoQA reaches 100%100\% under both views, and on ProofNet the two are statistically tied (65.9±0.6%65.9\pm 0.6\% global vs. 66.1±3.1%66.1\pm 3.1\% local). The local module already supplies what a global view would add.

### 5.6 Decomposed versus Scalar Feedback

Holding the loop fixed, we vary only the verdict format—per-axis audit-unit vector (ours) versus a single end-to-end scalar with a natural-language rationale—and cross it with judge capacity (GPT-5.4 vs. GPT-5.4-mini) on the four datasets.

#### A per-axis verdict outperforms a single end-to-end score wherever the baseline Pass Rate is below saturation, and matches it where the baseline already saturates.

On the two datasets where the baseline is below saturation the per-axis proxy beats the scalar proxy on both judge tiers (Table 5): ProofNet sees an 8.28.2–8.4%8.4\% gap and e-SNLI sees a 1717–18%18\% gap. ProntoQA reaches 100%100\% under both, and miniF2F (baseline ≥84%\geq 84\%) shows only a 1.41.4–1.6%1.6\% gap within seed variance. The split tracks headroom rather than benchmark family.

## 6 Conclusion

We recast autoformalization evaluation as constraint-directed optimization over a per-axis vector of verifiable property checks. Across seven backbones and four datasets the resulting refinement loop consistently improves Pass Rate, and ablations identify the per-axis proxy as the source of this advantage.

## Limitations

Our notion of correctness is audit-sufficient rather than fully semantic. The calibration in Section 5.3 nonetheless shows that the audit-unit score μ^\widehat{\mu} and an independently constructed external oracle move together in per-iteration shape on every panel, so audit-sufficient acceptance and semantic correctness are empirically correlated even though they are not formally identified. Formalizing this correlation through paired-target oracles, on benchmarks where such oracles can be sourced at scale, is left to future work.

Second, the empirical advantage of per-axis decomposition is currently dataset-conditional. We see clear effects on Lean ProofNet and Isabelle e-SNLI, where the baseline Pass Rate is below saturation and the kernel admits multiple violation modes, but the gap collapses on Lean miniF2F and Isabelle ProntoQA where the baseline already saturates. Whether the audit-unit construction generalizes as a dataset-agnostic refinement signal will require evaluation on benchmarks with broader topic coverage and iter-00 pools that are below saturation, particularly outside the four-dataset slice we used here.

Third, the framework as presented is purely an inference-time refinement procedure. The per-axis verdict vector is in principle a richer training signal than a scalar reward, and integrating it into reinforcement-learning fine-tuning of either the proposer or the judge, so as to close the loop between calibration and policy improvement, is a natural next step that we have not pursued in this work. Beyond autoformalization, we expect the same audit-unit decomposition to apply wherever correctness can be approximated by a calibrated family of property checks, including program synthesis and multi-hop natural-language reasoning.

## Acknowledgments

This work was partially funded by the Swiss National Science Foundation (SNSF) projects RATIONAL and M-RATIONAL.

## References

  * Azerbayev et al. (2023) Z. Azerbayev, B. Piotrowski, H. Schoelkopf, E. W. Ayers, D. Radev, and J. Avigad ProofNet: autoformalizing and formally proving undergraduate-level mathematics.  arXiv preprint arXiv:2302.12433.  External Links: [Link](https://arxiv.org/abs/2302.12433) Cited by: §1, §1, §2, §5.1. 
  * Bai et al. (2022) Y. Bai, S. Kadavath, S. Kundu, A. Askell, J. Kernion, A. Jones, A. Chen, A. Goldie, A. Mirhoseini, C. McKinnon, C. Chen, C. Olsson, C. Olah, D. Hernandez, D. Drain, D. Ganguli, D. Li, E. Tran-Johnson, E. Perez, J. Kerr, J. Mueller, J. Ladish, J. Landau, K. Ndousse, K. Lukosuite, L. Lovitt, M. Sellitto, N. Elhage, N. Schiefer, N. Mercado, N. DasSarma, R. Lasenby, R. Larson, S. Ringer, S. Johnston, S. Kravec, S. El Showk, S. Fort, T. Lanham, T. Telleen-Lawton, T. Conerly, T. Henighan, T. Hume, S. R. Bowman, Z. Hatfield-Dodds, B. Mann, D. Amodei, N. Joseph, S. McCandlish, T. Brown, and J. Kaplan Constitutional ai: harmlessness from ai feedback.  arXiv preprint arXiv:2212.08073.  External Links: [Link](https://arxiv.org/abs/2212.08073) Cited by: §2. 
  * Bottou et al. (2018) L. Bottou, F. E. Curtis, and J. Nocedal Optimization methods for large-scale machine learning.  SIAM Review 60 (2), pp. 223–311.  Cited by: §4.2. 
  * Camburu et al. (2018) O. Camburu, T. Rocktäschel, T. Lukasiewicz, and P. Blunsom E-SNLI: natural language inference with natural language explanations.  In Advances in Neural Information Processing Systems,  Vol. 31.  Cited by: §5.1. 
  * Dantas et al. (2025) P. Dantas, L. Cordeiro, Y. Sun, and W. Junior The 4/δ\delta bound: designing predictable LLM-verifier systems for formal method guarantee.  arXiv preprint arXiv:2512.02080.  External Links: [Link](https://arxiv.org/abs/2512.02080) Cited by: item 2, §2. 
  * de Moura and Ullrich (2021) L. de Moura and S. Ullrich The Lean 4 theorem prover and programming language.  In Automated Deduction – CADE 28, A. Platzer and G. Sutcliffe (Eds.),  Cham, pp. 625–635.  Cited by: §5.1. 
  * Jiang et al. (2023) A. Q. Jiang, S. Welleck, J. P. Zhou, W. Li, J. Liu, M. Jamnik, T. Lacroix, Y. Wu, and G. Lample Draft, sketch, and prove: guiding formal theorem provers with informal proofs.  In International Conference on Learning Representations (ICLR),  External Links: [Link](https://arxiv.org/abs/2210.12283) Cited by: §1, §1, §2, §5.1. 
  * Lightman et al. (2024) H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and K. Cobbe Let’s verify step by step.  In International Conference on Learning Representations (ICLR),  External Links: [Link](https://arxiv.org/abs/2305.20050) Cited by: §1, §2. 
  * Madaan et al. (2023) A. Madaan, N. Tandon, P. Gupta, S. Hallinan, L. Gao, S. Wiegreffe, U. Alon, N. Dziri, S. Prabhumoye, Y. Yang, S. Gupta, B. P. Majumder, K. Hermann, S. Welleck, A. Yazdanbakhsh, and P. Clark Self-refine: iterative refinement with self-feedback.  In Advances in Neural Information Processing Systems,  External Links: [Link](https://arxiv.org/abs/2303.17651) Cited by: §2. 
  * Nipkow et al. (2002) T. Nipkow, L. C. Paulson, and M. Wenzel Isabelle/HOL: a proof assistant for higher-order logic.  Lecture Notes in Computer Science, Vol. 2283, Springer.  Cited by: §5.1. 
  * Ouyang et al. (2022) L. Ouyang, J. Wu, X. Jiang, D. Almeida, C. L. Wainwright, P. Mishkin, C. Zhang, S. Agarwal, K. Slama, A. Ray, J. Schulman, J. Hilton, F. Kelton, L. Miller, M. Simens, A. Askell, P. Welinder, P. Christiano, J. Leike, and R. Lowe Training language models to follow instructions with human feedback.  In Advances in Neural Information Processing Systems,  External Links: [Link](https://arxiv.org/abs/2203.02155) Cited by: §2. 
  * Polu and Sutskever (2020) S. Polu and I. Sutskever Generative language modeling for automated theorem proving.  arXiv preprint arXiv:2009.03393.  External Links: [Link](https://arxiv.org/abs/2009.03393) Cited by: §1, §2. 
  * Quan et al. (2025) X. Quan, M. Valentino, L. A. Dennis, and A. Freitas Faithful and robust LLM-driven theorem proving for NLI explanations.  arXiv preprint arXiv:2505.24264.  External Links: [Link](https://arxiv.org/abs/2505.24264) Cited by: §2, §5.1, §5.3. 
  * Saparov and He (2023) A. Saparov and H. He Language models are greedy reasoners: a systematic formal analysis of chain-of-thought.  In International Conference on Learning Representations (ICLR),  External Links: [Link](https://arxiv.org/abs/2210.01240) Cited by: §5.1. 
  * Shinn et al. (2023) N. Shinn, F. Cassano, E. Berman, A. Gopinath, K. Narasimhan, and S. Yao Reflexion: language agents with verbal reinforcement learning.  In Advances in Neural Information Processing Systems,  External Links: [Link](https://arxiv.org/abs/2303.11366) Cited by: §2. 
  * Uesato et al. (2022) J. Uesato, N. Kushman, R. Kumar, F. Song, N. Siegel, L. Wang, A. Creswell, G. Irving, and I. Higgins Solving math word problems with process- and outcome-based feedback.  arXiv preprint arXiv:2211.14275.  External Links: [Link](https://arxiv.org/abs/2211.14275) Cited by: §1, §2. 
  * Valentino et al. (2021) M. Valentino, I. Pratt-Hartmann, and A. Freitas Do natural language explanations represent valid logical arguments? verifying entailment in explainable NLI gold standards.  In Proceedings of the 14th International Conference on Computational Semantics (IWCS),  pp. 76–86.  External Links: [Link](https://aclanthology.org/2021.iwcs-1.8/) Cited by: Appendix G. 
  * Wang et al. (2023) X. Wang, J. Wei, D. Schuurmans, Q. Le, E. H. Chi, S. Narang, A. Chowdhery, and D. Zhou Self-consistency improves chain of thought reasoning in language models.  In International Conference on Learning Representations (ICLR),  External Links: [Link](https://arxiv.org/abs/2203.11171) Cited by: §2. 
  * Wu et al. (2022) Y. Wu, A. Q. Jiang, W. Li, M. N. Rabe, C. Staats, M. Jamnik, and C. Szegedy Autoformalization with large language models.  In Advances in Neural Information Processing Systems,  External Links: [Link](https://proceedings.neurips.cc/paper_files/paper/2022/file/d0c6bc641a56bebee9d985b937307367-Paper-Conference.pdf) Cited by: §1, §1, §2, §5.1. 
  * Yang et al. (2023) K. Yang, A. M. Swope, A. Gu, R. Chalamala, P. Song, S. Yu, S. Godil, R. Prenger, and A. Anandkumar LeanDojo: theorem proving with retrieval-augmented language models.  In Advances in Neural Information Processing Systems (Datasets and Benchmarks Track),  External Links: [Link](https://arxiv.org/abs/2306.15626) Cited by: §1, §2. 
  * Yao et al. (2023) S. Yao, D. Yu, J. Zhao, I. Shafran, T. L. Griffiths, Y. Cao, and K. Narasimhan Tree of thoughts: deliberate problem solving with large language models.  In Advances in Neural Information Processing Systems,  External Links: [Link](https://arxiv.org/abs/2305.10601) Cited by: §2. 
  * Zhang et al. (2025) L. Zhang, M. Valentino, and A. Freitas Beyond gold standards: epistemic ensemble of LLM judges for formal mathematical reasoning.  arXiv preprint arXiv:2506.10903.  External Links: [Link](https://arxiv.org/abs/2506.10903) Cited by: §1, §1, §1, §5.3. 
  * Zhang et al. (2026) L. Zhang, M. Valentino, and A. Freitas Monotonic reference-free refinement for autoformalization.  arXiv preprint arXiv:2601.23166.  External Links: [Link](https://arxiv.org/abs/2601.23166) Cited by: §2, §5.1, §5.3. 
  * Zheng et al. (2022) K. Zheng, J. M. Han, and S. Polu MiniF2F: a cross-system benchmark for formal olympiad-level mathematics.  In International Conference on Learning Representations (ICLR),  External Links: [Link](https://arxiv.org/abs/2109.00110) Cited by: §2, §5.1. 
  * Zheng et al. (2023) L. Zheng, W. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang, Z. Lin, Z. Li, D. Li, E. P. Xing, H. Zhang, J. E. Gonzalez, and I. Stoica Judging LLM-as-a-judge with MT-Bench and chatbot arena.  In Advances in Neural Information Processing Systems (Datasets and Benchmarks Track),  External Links: [Link](https://arxiv.org/abs/2306.05685) Cited by: §1, §2. 



## Appendix A Auxiliary Bounds

### A.1 Audit-Unit Framework

Each elicited object P^={M1,…,MK}∈ℰ\widehat{P}=\\{M_{1},\ldots,M_{K}\\}\in\mathcal{E} decomposes into K≥1K\geq 1 modules. The audit-unit definition for each property follows the scope at which the property is defined in Section 3.1.

For the four module-scoped properties k∈{syn,typ,bnd,gnd}k\in\\{\mathrm{syn},\mathrm{typ},\mathrm{bnd},\mathrm{gnd}\\}, the audit units are the modules; a single judge call on module MM returns a binary value ξk​(M)∈{0,1}\xi_{k}(M)\in\\{0,1\\}, with latent counterpart qk​(M)∈{0,1}q_{k}(M)\in\\{0,1\\} understood as the strict conjunction of the underlying per-statement, per-binding, or per-symbol checks, where a single internal violation suffices to set qk​(M)=0q_{k}(M)=0. For the two whole-object axes k∈{glb,doc}k\in\\{\mathrm{glb},\mathrm{doc}\\}, the audit units are P^\widehat{P} itself (a single unit per instance), with ξk​(P^),qk​(P^)∈{0,1}\xi_{k}(\widehat{P}),q_{k}(\widehat{P})\in\\{0,1\\}.

For statement-scoped semantic preservation k=spk=\mathrm{sp}, the audit units are the explicit statements p^j∈P^\widehat{p}_{j}\in\widehat{P} taken across modules. For coverage k=covk=\mathrm{cov}, the audit units are the source claim units c∈C⁡(n​l)c\in C(nl), with ξcov​(c),qcov​(c)∈{0,1}\xi_{\mathrm{cov}}(c),q_{\mathrm{cov}}(c)\in\\{0,1\\} defined on whether cc is represented somewhere in the current P^\widehat{P}. This batch-AND framing is the strict modular evaluation semantics already implied by Section 3.1; the per-item view is conceptual, and both the judge interface and the noise 

model live at the audit-unit level corresponding to each axis’s scope.

We write uu for a generic audit unit and Nk​(P^)N_{k}(\widehat{P}) for its count, with Nk​(P^)=KN_{k}(\widehat{P})=K for the four module-scoped axes, Nk​(P^)=1N_{k}(\widehat{P})=1 for k∈{glb,doc}k\in\\{\mathrm{glb},\mathrm{doc}\\}, Nsp​(P^)=∑M|M|N_{\mathrm{sp}}(\widehat{P})=\sum_{M}|M| for statement-scoped semantic preservation, and Ncov​(P^)=|C⁡(n​l)|≥1N_{\mathrm{cov}}(\widehat{P})=|C(nl)|\geq 1 for coverage. Inactive coordinates are dropped, and ww is renormalized over the active set. The property-level aggregates of Section 4.1 are sample means over audit units:

| ξk​(P^)\displaystyle\xi_{k}(\widehat{P}) | =1Nk​(P^)​∑uξk​(u),\displaystyle=\tfrac{1}{N_{k}(\widehat{P})}\sum_{u}\xi_{k}(u), |   
---|---|---|---  
| qk​(P^)\displaystyle q_{k}(\widehat{P}) | =1Nk​(P^)​∑uqk​(u).\displaystyle=\tfrac{1}{N_{k}(\widehat{P})}\sum_{u}q_{k}(u). |   
  
The observable ξk​(P^)∈[0,1]\xi_{k}(\widehat{P})\in[0,1] is the empirically computed proxy, while qk​(P^)∈[0,1]q_{k}(\widehat{P})\in[0,1] is the idealized aggregate of conceptual per-unit ground-truth labels qk​(u)q_{k}(u) that the proxy approximates. The per-audit-unit binary judge model of Assumption 4 (Appendix C) propagates through this aggregation to a one-step concentration bound between the observable proxy μ^\widehat{\mu} and the latent μ⋆\mu^{\star}.

###### Lemma 2 (Proxy accuracy bound, one-step).

Under Assumption 4 with per-audit-unit misclassification rate η\eta, write Nmin(P^)=mink:wk>0Nk(P^)N_{\min}(\widehat{P})=\min_{k:\,w_{k}>0}N_{k}(\widehat{P}) for the smallest audit-unit count on P^\widehat{P} across active axes. For any P^∈ℰ\widehat{P}\in\mathcal{E} and any δ∈(0,1)\delta\in(0,1),

| ℙ⁡(|μ^​(P^)−μ⋆​(P^)|>η+log⁡(2​m/δ)2​Nmin​(P^))≤δ.\mathbb{P}\\!\Bigg(|\widehat{\mu}(\widehat{P})-\mu^{\star}(\widehat{P})|>\eta+\sqrt{\frac{\log(2m/\delta)}{2\,N_{\min}(\widehat{P})}}\Bigg)\leq\delta. |   
---|---|---  
  
A proof is given in Appendix E. The bound has two levers. Amplification through repeated judging (Lemma 1) shrinks η\eta, and larger audit-unit counts shrink the finite-sample term. The whole-object axes (ξglb\xi_{\mathrm{glb}}, ξdoc\xi_{\mathrm{doc}}) contribute a single unit and therefore depend purely on the η\eta lever; on these axes, with m=8m{=}8 and δ=0.05\delta{=}0.05, the finite-sample term log⁡(2​m/δ)/2≈1.7\sqrt{\log(2m/\delta)/2}\approx 1.7 exceeds 11 and the bound is vacuous, so concentration must come from majority voting rather than from accumulating audit units. The module-scoped, statement-scoped, and source-claim-unit-scoped axes additionally benefit from larger KK, ∑M|M|\sum_{M}|M|, or |C⁡(n​l)||C(nl)|. For instances with few modules the concentration term remains a non-trivial fraction of the bound, and we treat it accordingly in Section 6.

## Appendix B Microscopic Motivation for the Drift Assumption

Assumption 2 is motivated by a “finite constraints + local repair” view intrinsic to explicit languages; this appendix proves the additive form of the recursion rigorously and then identifies the modeling step that converts it to the multiplicative form of Assumption 2. The appendix does not derive Assumption 2: the additive and multiplicative forms are mathematically distinct, and the conversion is a modeling assumption adopted as a primitive of the analysis, not a logical consequence of the microscopic recursion.

###### Definition 1 (Finite constraint set per instance).

For each P^∈ℰ\widehat{P}\in\mathcal{E}, let 𝒦⁡(P^)={1,…,n⁡(P^)}\mathcal{K}(\widehat{P})=\\{1,\dots,n(\widehat{P})\\} index the locally checkable constraints induced by the prover on that instance (each statement’s well-formedness, each binding site, each inference-step check). Let vj​(P^)∈{0,1}v_{j}(\widehat{P})\in\\{0,1\\} indicate whether constraint jj is satisfied; these are exactly the per-item predicates that the batch-AND framing of Section 4.1 aggregates internally to a module verdict, and we use them here to expose the microscopic dynamics that motivate Assumption 2. Setting

| μ⋆​(P^)=1n⁡(P^)​∑j=1n⁡(P^)vj​(P^)\mu^{\star}(\widehat{P})=\tfrac{1}{n(\widehat{P})}\sum_{j=1}^{n(\widehat{P})}v_{j}(\widehat{P}) |   
---|---|---  
  
is the unweighted constraint-fraction view that coincides with the audit-unit aggregate of Section 4.1 when modules are sized proportionally to their internal constraint counts.

The microscopic analysis attaches to each refinement step a model of how many constraints it repairs versus newly violates.

###### Assumption 3 (Local repair efficacy and bounded regress).

Fix iteration ii and let UiU_{i} be the number of unsatisfied constraints in P^i\widehat{P}_{i}. Conditional on Ui>0U_{i}>0, there exist ρ∈(0,1]\rho\in(0,1] and κ≥0\kappa\geq 0 such that one refinement step: (i) repairs at least one truly violated constraint with probability at least ρ\rho; (ii) introduces at most κ\kappa newly violated constraints in expectation.

If judges and localization are imperfect, ρ\rho decreases as the per-audit-unit misclassification rate η\eta of Assumption 4 increases. A typical minimal relationship is ρ≥ρ0−c​η\rho\geq\rho_{0}-c\eta for some baseline ρ0\rho_{0} and constant c>0c>0 (problem- and implementation-dependent).

###### Lemma 3 (Gap recursion from local repair).

Under Assumption 3, for Ui>0U_{i}>0,

| 𝔼⁡[Ui+1∣P^i]≤Ui−ρ+κ.\mathbb{E}[U_{i+1}\mid\widehat{P}_{i}]\leq U_{i}-\rho+\kappa. |   
---|---|---  
  
If the constraint count is preserved across the step, n⁡(P^i+1)=n⁡(P^i)n(\widehat{P}_{i+1})=n(\widehat{P}_{i}), then with μ⋆​(P^i)=1−Ui/n⁡(P^i)\mu^{\star}(\widehat{P}_{i})=1-U_{i}/n(\widehat{P}_{i}) this is equivalent to

| 𝔼⁡[1−μ⋆​(P^i+1)∣P^i]≤(1−μ⋆​(P^i))−ρ−κn⁡(P^i).\mathbb{E}[1-\mu^{\star}(\widehat{P}_{i+1})\mid\widehat{P}_{i}]\leq(1-\mu^{\star}(\widehat{P}_{i}))-\tfrac{\rho-\kappa}{n(\widehat{P}_{i})}. |   
---|---|---  
  
Lemma 3 gives monotone improvement whenever ρ>κ\rho>\kappa. The contractive form of Assumption 2 follows once diminishing returns are acknowledged. As fewer violations remain, repairs target subtler issues and effective progress shrinks proportionally to the residual gap, yielding a contraction factor 1−λ1-\lambda plus a noise-dependent residual. The transition from the additive recursion of Lemma 3 to the multiplicative form of Assumption 2 is itself a modeling step rather than a formal derivation; we treat Assumption 2 as a primitive of the analysis and rely on the empirical fit of gi+1=a​gi+c+ϵig_{i+1}=ag_{i}+c+\epsilon_{i} in Appendix D to validate it. A proof of Lemma 3 is given in Appendix E.

## Appendix C Amplification by Repeated Judging

If a judge is noisy, we can reduce uncertainty by repeating local judgments and aggregating.

###### Assumption 4 (Binary per-audit-unit judge with primitive error rate).

For each property kk, each elicited object P^∈ℰ\widehat{P}\in\mathcal{E}, and each audit unit uu of property kk on P^\widehat{P} as defined in Section A.1 (P^\widehat{P} itself for k∈{glb,doc}k\in\\{\mathrm{glb},\mathrm{doc}\\}, a module M∈P^M\in\widehat{P} for k∈{syn,typ,bnd,gnd}k\in\\{\mathrm{syn},\mathrm{typ},\mathrm{bnd},\mathrm{gnd}\\}, an explicit statement p^j∈P^\widehat{p}_{j}\in\widehat{P} for k=spk=\mathrm{sp}, or a source claim unit c∈C⁡(n​l)c\in C(nl) for k=covk=\mathrm{cov}), the latent value qk​(u)∈{0,1}q_{k}(u)\in\\{0,1\\} admits a judge estimate ξk(t)​(u)∈{0,1}\xi_{k}^{(t)}(u)\in\\{0,1\\} on the tt-th call, t∈{1,2,…}t\in\\{1,2,\ldots\\}, with

| ℙ[ξk(t)(u)≠qk(u)]≤η<12.\mathbb{P}\big[\xi_{k}^{(t)}(u)\neq q_{k}(u)\big]\leq\eta<\tfrac{1}{2}. |   
---|---|---  
  
Calls are taken to be mutually independent both across repetitions tt and across audit units of the same property. We take η\eta as a primitive per-audit-unit misclassification rate. The strict inequality η<1/2\eta<1/2 asks only that the judge be informative on average, the necessary condition for majority-vote amplification (Lemma 1) to apply, and is comfortably satisfied by kernel-verified judges (where η≈0\eta\approx 0) and by well-calibrated LLM judges on focused per-property checks.

The independence assumption is the strongest part of Assumption 4 in our implementation: repeated LLM judge calls use the same model and prompt with low-temperature decoding, so the calls share correlated errors. The exponential bound of Lemma 1 should therefore be read as an upper bound under the idealised independent-call regime, and the achievable suppression in practice is closer to ηeff∝η\eta_{\mathrm{eff}}\propto\eta under high correlation. Our experiments do not exploit the exponential rate as a quantitative prediction; we report only the qualitative direction that increasing TT is expected to be non-worsening for the plateau under the independent-call regime, and we do not claim empirical verification on the saturated benchmarks studied here.

## Appendix D Operationalization Details

### D.1 Operational Objects

Fix a target dataset such as Lean, Coq, Isabelle, or a typed logical intermediate representation with a kernel checker, and fix a per-instance fact context Γ\Gamma. Each iteration produces an elicited object P^i∈ℰ\widehat{P}_{i}\in\mathcal{E} (Section 3), partitioned into KK modules M1,M2,…,MKM_{1},M_{2},\ldots,M_{K}. In practice, each module stores explicit statements and inference links as proof steps or step-typed edges, declarations elicited from n​lnl as IR terms, and resolved symbol identifiers referenced against Γ\Gamma. Optional alignment metadata ties spans or claim units back to n​lnl. The object P^i\widehat{P}_{i} is the optimization variable, and refinement changes it through localized edits.

#### Intrinsic property vector in practice.

The full instantiation of qq in this paper uses the audit-unit axes of Section 3.1, organized by the prover stage at which each is decided. The global axis ξglb\xi_{\mathrm{glb}} is read off the prover’s end-to-end acceptance verdict on P^\widehat{P}. The document axis ξdoc\xi_{\mathrm{doc}} is read off the prover’s parse-only verdict on P^\widehat{P} as a source artifact, before elaboration. Sentence-level ξsyn\xi_{\mathrm{syn}} and ξtyp\xi_{\mathrm{typ}} aggregate the parser and type-checker verdicts across statements; inter-sentence ξbnd\xi_{\mathrm{bnd}} aggregates the binding-resolution verdicts across statements within each module. The cross-domain axes are LLM-judged with decomposed criteria: ξgnd\xi_{\mathrm{gnd}} aggregates per-symbol grounding verdicts against n​lnl and Γ\Gamma, ξsp\xi_{\mathrm{sp}} aggregates per-statement faithfulness verdicts, and ξcov\xi_{\mathrm{cov}} aggregates per-source-claim-unit completeness verdicts. Each coordinate lies in [0,1][0,1], yielding q⁡(P^)∈[0,1]mq(\widehat{P})\in[0,1]^{m} with m=8m=8 in this paper (the kernel-decided and cross-domain axes enumerated in Section 3.1).

### D.2 Judge Calibration Protocol

The misclassification rate η\eta is empirically grounded by treating intrinsic checks qq as measurement ground truth wherever possible. Collect a calibration set of audit units sampled from AF trajectories along the scope at which each axis is defined in Section A.1: whole elicited objects P^\widehat{P} for k∈{glb,doc}k\in\\{\mathrm{glb},\mathrm{doc}\\}, modules drawn from definition blocks, binding sites, and reference sites for k∈{syn,typ,bnd,gnd}k\in\\{\mathrm{syn},\mathrm{typ},\mathrm{bnd},\mathrm{gnd}\\}, individual explicit statements p^j\widehat{p}_{j} for k=spk=\mathrm{sp}, and source claim units in n​lnl for k=covk=\mathrm{cov}.

For each audit unit uu and property kk, compute the ground-truth value qk​(u)q_{k}(u) through the kernel, the released gold formalization, or a small reviewer-facing annotation subset (depending on benchmark family; see Section 5.3), and the judge value ξk​(u)\xi_{k}(u) through the corresponding judge. Estimate per-property error rates:

| η^k=ℙ[ξk(u)≠qk(u)].\hat{\eta}_{k}=\mathbb{P}[\xi_{k}(u)\neq q_{k}(u)]. |   
---|---|---  
  
Define the global η^\hat{\eta} as maxk⁡η^k\max_{k}\hat{\eta}_{k}, the conservative aggregator that matches the per-audit-unit bound of Assumption 4; the ww-weighted mean of η^k\hat{\eta}_{k} is a strictly smaller quantity that we record only as a diagnostic of average judge reliability. If judge calls are stochastic, repeat them TT times on the same audit unit and aggregate by majority vote. Increasing TT pushes the per-audit-unit misclassification rate down exponentially via Lemma 1 and the plateau closer to 11, consistent with the amplification lever of the proxy-convergence law (Section 4).

### D.3 Refinement Operators and Bounded Regress

Define a finite set of repair operators 𝒜\mathcal{A} that act on a localized target tt, as listed in Section 5. The set covers binding, definition, step, and coverage repairs. Each operator must act on a small context, and its effect on qq must be verifiable. For each iteration record

| Δ​qi\displaystyle\Delta q_{i} | =q⁡(P^i+1)−q⁡(P^i),\displaystyle=q(\widehat{P}_{i+1})-q(\widehat{P}_{i}), |   
---|---|---|---  
| Δ​μi⋆\displaystyle\Delta\mu^{\star}_{i} | =μ⋆​(P^i+1)−μ⋆​(P^i).\displaystyle=\mu^{\star}(\widehat{P}_{i+1})-\mu^{\star}(\widehat{P}_{i}). |   
  
Bounded regress is empirically supported if negative jumps are rare and shallow, or are compensated by subsequent iterations.

### D.4 Estimating Drift Parameters

The theorem-level recursion 𝔼⁡[1−μi+1⋆]≤(1−λ)​(1−μi⋆)+b​η\mathbb{E}[1-\mu^{\star}_{i+1}]\leq(1-\lambda)(1-\mu^{\star}_{i})+b\eta can be fit empirically without overfitting. Let gi=1−μi⋆g_{i}=1-\mu^{\star}_{i} and fit gi+1=a​gi+c+ϵig_{i+1}=a\,g_{i}+c+\epsilon_{i} with a≈1−λa\approx 1-\lambda and c≈b​ηc\approx b\eta. Estimate confidence intervals by bootstrapping over instances. The predicted plateau is g∞≈c/(1−a)g_{\infty}\approx c/(1-a), equivalently μ∞⋆≈1−c/(1−a)\mu^{\star}_{\infty}\approx 1-c/(1-a). To validate the η\eta-dependence rather than merely fit a curve, vary η\eta experimentally. The interventions can change the judge context window size, change TT, inject controlled noise into judge outputs, or swap judge models. If cc scales linearly with measured η\eta while aa is stable or degrades predictably, this supports the plateau theory.

## Appendix E Proofs

###### Proof of Theorem 1.

Taking expectations on both sides of Assumption 2 gives

| 𝔼⁡[gi+1]≤(1−λ)​𝔼​[gi]+b​η.\mathbb{E}[g_{i+1}]\leq(1-\lambda)\,\mathbb{E}[g_{i}]+b\,\eta. |   
---|---|---  
  
Unrolling the recursion,

| 𝔼⁡[gi]\displaystyle\mathbb{E}[g_{i}] | ≤(1−λ)i​𝔼​[g0]+b​η​∑k=0i−1(1−λ)k\displaystyle\leq(1-\lambda)^{i}\,\mathbb{E}[g_{0}]+b\,\eta\sum_{k=0}^{i-1}(1-\lambda)^{k} |   
---|---|---|---  
|  | =(1−λ)i​𝔼​[g0]+b​η​(1−(1−λ)i)λ.\displaystyle=(1-\lambda)^{i}\,\mathbb{E}[g_{0}]+\tfrac{b\,\eta\bigl(1-(1-\lambda)^{i}\bigr)}{\lambda}. |   
  
Since λ∈(0,1]\lambda\in(0,1], (1−λ)i→0(1-\lambda)^{i}\to 0 as i→∞i\to\infty, hence lim supi𝔼⁡[gi]≤b​η/λ\limsup_{i}\mathbb{E}[g_{i}]\leq b\eta/\lambda. Equivalently, lim infi𝔼⁡[μ⋆​(P^i)]≥1−b​η/λ\liminf_{i}\mathbb{E}[\mu^{\star}(\widehat{P}_{i})]\geq 1-b\eta/\lambda. When η=0\eta=0, the plateau distance vanishes. ∎

###### Proof of Lemma 3.

Let RiR_{i} be the number of constraints repaired at cycle ii and Ri′R^{\prime}_{i} the number of newly violated constraints introduced. Conditional on Ui>0U_{i}>0, Assumption 3(i) gives 𝔼⁡[Ri∣P^i]≥ρ\mathbb{E}[R_{i}\mid\widehat{P}_{i}]\geq\rho, and Assumption 3(ii) gives 𝔼⁡[Ri′∣P^i]≤κ\mathbb{E}[R^{\prime}_{i}\mid\widehat{P}_{i}]\leq\kappa. The update is Ui+1=Ui−Ri+Ri′U_{i+1}=U_{i}-R_{i}+R^{\prime}_{i}, so 𝔼⁡[Ui+1∣P^i]≤Ui−ρ+κ\mathbb{E}[U_{i+1}\mid\widehat{P}_{i}]\leq U_{i}-\rho+\kappa. Dividing by n⁡(P^i)n(\widehat{P}_{i}) gives the stated recursion on 1−μ⋆1-\mu^{\star}. ∎

###### Proof of Lemma 1.

Fix kk, P^\widehat{P}, and an audit unit uu of property kk on P^\widehat{P} as defined in Section A.1. Under Assumption 4, the TT independent judge calls {ξk(t)​(u)}t=1T\\{\xi_{k}^{(t)}(u)\\}_{t=1}^{T} have error indicators with mean at most η<1/2\eta<1/2. The majority vote errs only if strictly more than T/2T/2 of the calls err; by Hoeffding’s inequality,

| ℙ[1T∑t=1T𝟏[ξk(t)(u)≠qk(u)]>12]≤exp⁡(−2​T​(12−η)2).∎\begin{aligned} &\mathbb{P}\\!\left[\tfrac{1}{T}\sum_{t=1}^{T}\mathbf{1}[\xi_{k}^{(t)}(u)\neq q_{k}(u)]>\tfrac{1}{2}\right]\\\ &\qquad\leq\exp\\!\big(-2T(\tfrac{1}{2}-\eta)^{2}\big).\end{aligned}\qed |   
---|---|---  
  
###### Proof of Lemma 2.

Fix P^\widehat{P}, and let Nk​(P^)N_{k}(\widehat{P}) denote the audit-unit count for property kk as defined in Section A.1: Nk​(P^)=1N_{k}(\widehat{P})=1 for k∈{glb,doc}k\in\\{\mathrm{glb},\mathrm{doc}\\}, Nk​(P^)=KN_{k}(\widehat{P})=K for k∈{syn,typ,bnd,gnd}k\in\\{\mathrm{syn},\mathrm{typ},\mathrm{bnd},\mathrm{gnd}\\}, Nsp​(P^)=∑M|M|N_{\mathrm{sp}}(\widehat{P})=\sum_{M}|M|, and Ncov​(P^)=|C⁡(n​l)|N_{\mathrm{cov}}(\widehat{P})=|C(nl)|. By Assumption 4 the judge values ξk​(u)∈{0,1}\xi_{k}(u)\in\\{0,1\\} over the audit units of property kk are mutually independent, so ξk​(P^)−qk​(P^)\xi_{k}(\widehat{P})-q_{k}(\widehat{P}) is the centered average of Nk​(P^)N_{k}(\widehat{P}) independent indicators in [−1,1][-1,1], each with 𝔼​|ξk​(u)−qk​(u)|≤η\mathbb{E}|\xi_{k}(u)-q_{k}(u)|\leq\eta. Hoeffding’s inequality on the bounded summands ξk​(u)∈[0,1]\xi_{k}(u)\in[0,1] around their means gives, for any t>0t>0,

| ℙ⁡(|ξk​(P^)−𝔼​ξk​(P^)|>t)≤2​exp⁡(−2​Nk​(P^)​t2),\mathbb{P}\\!\big(|\xi_{k}(\widehat{P})-\mathbb{E}\xi_{k}(\widehat{P})|>t\big)\leq 2\exp(-2N_{k}(\widehat{P})\,t^{2}), |   
---|---|---  
  
and the bias bound |𝔼​ξk​(P^)−qk​(P^)|≤η|\mathbb{E}\xi_{k}(\widehat{P})-q_{k}(\widehat{P})|\leq\eta yields |ξk​(P^)−qk​(P^)|≤η+t|\xi_{k}(\widehat{P})-q_{k}(\widehat{P})|\leq\eta+t on the same high-probability event. A union bound over k∈{1,…,m}k\in\\{1,\ldots,m\\} gives

|  | ℙ⁡(maxk⁡|ξk​(P^)−qk​(P^)|>η+t)\displaystyle\mathbb{P}\\!\Big(\max_{k}|\xi_{k}(\widehat{P})-q_{k}(\widehat{P})|>\eta+t\Big) |   
---|---|---|---  
|  | ≤2​m​exp⁡(−2​Nmin​(P^)​t2),\displaystyle\leq 2m\exp\\!\big(-2\,N_{\min}(\widehat{P})\,t^{2}\big), |   
  
where Nmin(P^)=mink:wk>0Nk(P^)N_{\min}(\widehat{P})=\min_{k:\,w_{k}>0}N_{k}(\widehat{P}). Choosing t=log⁡(2​m/δ)/(2​Nmin​(P^))t=\sqrt{\log(2m/\delta)/(2N_{\min}(\widehat{P}))} makes the right-hand side equal to δ\delta. Since w∈ℝ≥0mw\in\mathbb{R}^{m}_{\geq 0} with ‖w‖1=1\|w\|_{1}=1, |μ^​(P^)−μ⋆​(P^)|≤∑kwk​|ξk−qk|≤maxk⁡|ξk−qk||\widehat{\mu}(\widehat{P})-\mu^{\star}(\widehat{P})|\leq\sum_{k}w_{k}|\xi_{k}-q_{k}|\leq\max_{k}|\xi_{k}-q_{k}|, and the stated bound follows. ∎

## Appendix F Theory-Aligned Aggregates

Table 6 reports the cross-backbone aggregate of the multi-seed trajectory evaluation along the proxy-side columns μ0⋆\mu^{\star}_{0}, μ∞⋆\mu^{\star}_{\infty}, and pass rate, complementing the per-backbone pass-rate breakdown in Table 2 in the main body.

Table 6: End-to-End Trajectories: Cross-Backbone Aggregate. Each row pools instances from all seven backbones and both methods (single-shot baseline and our refinement framework). μ0⋆\mu^{\star}_{0} and μ∞⋆\mu^{\star}_{\infty} are the initial and final audit-unit scores; Pass Rate (%) is the prover’s acceptance on P^∞\widehat{P}_{\infty}. Domain | Prover | Benchmark | 𝝁𝟎⋆\boldsymbol{\mu^{\star}_{0}} | 𝝁∞⋆\boldsymbol{\mu^{\star}_{\infty}} | Pass Rate (%)  
---|---|---|---|---|---  
Explanation | Isabelle | e-SNLI | 0.95±\pm0.09 | 0.96±\pm0.09 | 81.6  
Explanation | Isabelle | ProntoQA (2799/2800) | 0.99±\pm0.05 | 0.99±\pm0.03 | 98.1  
Math | Lean | miniF2F | 0.94±\pm0.10 | 0.95±\pm0.11 | 78.8  
Math | Lean | ProofNet | 0.89±\pm0.12 | 0.89±\pm0.14 | 47.6  
  
## Appendix G Dataset Details

Table 7: Benchmark Details. nn is the evaluation sample size; “judge-stress” indicates which qq coordinates are LLM-estimated on this dataset. Benchmark | Prover | 𝒏\boldsymbol{n} | Split | Judge-Stressed Axes  
---|---|---|---|---  
miniF2F | Lean 4 | 244 | Test | ξgnd,ξsp\xi_{\mathrm{gnd}},\xi_{\mathrm{sp}}  
ProofNet | Lean 4 | 182 | Test | ξgnd,ξsp,ξcov\xi_{\mathrm{gnd}},\xi_{\mathrm{sp}},\xi_{\mathrm{cov}}  
e-SNLI | Isabelle | 100 | Test | ξsp,ξcov\xi_{\mathrm{sp}},\xi_{\mathrm{cov}}  
ProntoQA | Isabelle | 200 | Dev | ξsp,ξcov\xi_{\mathrm{sp}},\xi_{\mathrm{cov}}  
  
Table 7 summarizes sample sizes, splits, and judge-stressed coordinates per benchmark. For the two formal-proof benchmarks (miniF2F, ProofNet) we use the standard test splits in their entirety. The four-dataset axiomatization stresses different subsets of the per-axis qq vector: on Lean both grounding ξgnd\xi_{\mathrm{gnd}} (for symbol-resolution against mathlib) and statement-level semantic preservation ξsp\xi_{\mathrm{sp}} are judge-estimated; on ProofNet coverage ξcov\xi_{\mathrm{cov}} additionally enters because the library-alignment requirement leaves residual claim units that the candidate may not represent. On Isabelle both ξsp\xi_{\mathrm{sp}} and ξcov\xi_{\mathrm{cov}} are judge-estimated because the natural-language source admits multiple valid Davidsonian or FOL renderings.

For e-SNLI we follow the sampling strategy of Valentino et al. (2021), which selects instances to maximize representativeness and mutual exclusivity across syntactic and semantic features; our subset draws 100 entailment-labeled items for which the bidirectional ATP oracle has a well-defined positive ground truth. For ProntoQA we draw a 200-sample subset from the official dev split with approximately balanced True\- and False-label rule chains (103/97). All splits are disjoint from the few-shot demonstration pools described in Appendix H.

## Appendix H Direct Few-Shot Baseline Configuration

The baseline used in Section 5.2 runs the same seven backbones at temperature 0.20.2 producing one sample per instance, with no resampling or majority voting; the instance set per benchmark matches the main evaluation. The few-shot pools contain three demonstrations per (dataset, benchmark) setting, matched to the target distribution.

For miniF2F and ProofNet the three Lean 4 demonstrations are drawn from the validation split (disjoint from the test split used for evaluation): the miniF2F pool covers a no-hypothesis numerical identity, an ℕ\mathbb{N}-typed divisibility goal with a single hypothesis, and a real-typed proportion goal; the ProofNet pool covers a negation-of-existence statement, a goal with an instance-binder hypothesis, and a polynomial-irreducibility statement that exercises typeclass binders.

For e-SNLI and ProntoQA no published Davidsonian or FOL Isabelle pool is available. We disclose the data-provenance asymmetry explicitly: each three-shot pool is drawn from clean iter-1 generations in our own loop runs, with instances held out from the test split used for evaluation; selection criteria are kernel acceptance, zero failed proxy dimensions, and stylistic regularity. Concretely, the e-SNLI pool covers an event-typed entailment, an entity-typed entailment with a single attribute, and a multi-attribute entailment; the ProntoQA pool covers two True-label rule chains and one False-label chain so that the literal-hypothesis shows clause is illustrated for both polarities.

This setup favors the baseline relative to a hypothetical pool drawn from unfiltered LLM outputs and therefore makes the baseline a tighter (rather than looser) point of comparison; on datasets where iter-1 generation quality is itself a confound (miniF2F, ProofNet), we use the disjoint validation pools above. The single-shot output is scored through the same evaluation pipeline as the loop (kernel prover plus per-axis proxy ξ\xi); the external oracle of Section 5.3 is not run on baseline outputs.

## Appendix I Extended Judge-Calibration Analysis

This appendix collects analysis material moved out of Section 5.3 for space. The oracle referenced throughout is the approximate stand-in for the gold label introduced in Section 5.3.

#### The oracles are themselves proxies, not ground truth.

On math (miniF2F, ProofNet) a ref-anchored GPT-5.4 judge produces a binary ours_correct verdict from the natural-language statement, gold reference, and candidate; on explanation (e-SNLI, ProntoQA), a bidirectional ATP probes the hypothesis and its negation against the candidate’s formal context, and the pair is mapped through the dataset label. Neither the math oracle nor the explanation oracle is reference-grade. The math oracle compares two LLMs at different capacity tiers, and the explanation oracle can be satisfied incidentally by an over-permissive axiomatization. We therefore decline to identify the oracle distance with η\eta and report no point estimate of λ^\widehat{\lambda} or η^eff\widehat{\eta}_{\mathrm{eff}}.

#### Oracle and proxy bands measure different noise sources.

The seed-bands on the DeepSeek-V3.1 row carry different widths for the two curves. The proxy curve reports the driver-visible composite (kernel-decided dimensions and the LLM-judged SP/COV verdicts) and is the signal the loop early-stops on; per-instance verdicts feed back into refinement so the cohort mean converges narrowly across seeds (σ≤3.0%\sigma\\!\leq\\!3.0\% on every dataset, peaking on ProofNet and tightening to 1.2%1.2\% on ProntoQA). The oracle curve reports a separate per-instance whole-object verdict from a deterministic external scorer queried independently of refinement; with no aggregation across axes and no driver coupling, the cohort-mean seed-band is a direct projection of how much the final formalization varies instance-by-instance across driver seeds. On miniF2F that variability is largest (σ≈5.6%\sigma\\!\approx\\!5.6\%); on ProofNet (3.7%3.7\%), e-SNLI (2.0%2.0\%), and ProntoQA (1.8%1.8\%) the dataset’s tighter acceptance template narrows the dispersion.

#### Proxy and oracle move in opposite directions on saturating Isabelle ProntoQA.

The DeepSeek-V3.1 ProntoQA panel is the only setting where the proxy rises monotonically while the oracle declines: between iter 11 and iter 22 the proxy gains 1.4%1.4\% and the oracle pass rate drops by 2.4%2.4\% across all three seeds, so the divergence is not a cohort-aggregation artifact. Iter-11 candidates already satisfy the kernel and most per-axis judges at μ^≈0.97\widehat{\mu}\approx 0.97, and the loop’s residual repair signal targets SP and COV verdicts on a small remainder. The bidirectional ATP probe is more sensitive to axiomatization soundness than to any single hypothesis’s derivability, and tightening the axiomatization in service of SP/COV can eliminate the incidental derivability paths the iter-11 over-permissive axiomatization relied on, dropping a handful of fixtures from yes to partial. The other three panels show no such divergence because their iter-11 proxy is well below ceiling.

#### Cross-seed oracle voting reduces single-sample LLM-judge noise in the calibration setup.

The math oracle (temperature-00 ref-anchored GPT-5.4) is deterministic at the call level but its tristate output, {yes,no,partial}\\{\texttt{yes},\texttt{no},\texttt{partial}\\}, is per-instance and can collapse to a different bucket on small perturbations of the candidate. On DeepSeek-V3.1 ProofNet the per-instance terminal verdict differs across three driver seeds for 11.5%11.5\% of instances even after restricting to non-abstention seeds (35%35\% of seed-instance pairs land on partial and are treated as abstentions). A majority rule (yes/no/partial →+1/−1/0\\!\to\\!\\!+1/{-1}/0; sign of the sum) keeps the cohort pass rate within ±1.2%\pm 1.2\% of any seed ([80.9,82.1]%[80.9,82.1]\% across four views) and cuts abstentions from 5151–6161 per cohort to 4848.

Experimental support, please [view the build logs](./2606.09449v1/__stdout.txt) for errors. Generated by [ L A T E xml ](https://math.nist.gov/~BMiller/LaTeXML/). 

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

