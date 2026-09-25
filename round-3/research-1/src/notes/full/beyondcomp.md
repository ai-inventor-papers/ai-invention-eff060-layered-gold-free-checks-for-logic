URL: https://arxiv.org/html/2606.31002 | FULL FETCH | 2026-09-24T01:47:32Z
warning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
URL: https://arxiv.org/html/2606.31002
Type: HTML
Length: 87050 chars (truncated)

--- Content ---

##### Report GitHub Issue

×

Title:

Content selection saved. Describe the issue below:

Description:

Submit without GitHub Submit in GitHub

arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[ Back to arXiv ](/)

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) Report Issue [ Back to Abstract ](/abs/2606.31002v2 "Back to abstract page") [ Download PDF](/pdf/2606.31002v2 "Download PDF") [ ](javascript:toggleNavTOC\(\); "Toggle navigation") [ ](javascript:toggleReadingMode\(\); "Disable reading mode, show header and footer")

  1. Abstract
  2. 1 Introduction
     1. Contributions.
  3. 2 Evaluation without Canonical Lean Targets
     1. Statement formalization vs. theorem proving.
     2. 2.1 Task Definition
     3. 2.2 Evaluation Context
     4. 2.3 Dataset Construction
     5. 2.4 Evaluation Protocol
        1. Cross-judge consensus.
  4. 3 Formalization Pipeline and Tool Factors
     1. 3.1 Tools and the Bottlenecks They Target
     2. 3.2 Controlled Prompt Assembly
  5. 4 Evaluation Results
     1. 4.1 Q1: Can LLM Judges Approximate Human Review?
        1. Same-sample comparison with LeanScorer.
        2. Independent judge and threshold robustness.
        3. Formal cross-check with BEq.
     2. 4.2 Q2: How Large Is the Compile–Faithfulness Gap?
  6. 5 Bottleneck Decomposition
     1. 5.1 Factorial Design over (T,F,S)
     2. 5.2 Main Effects: Validity vs. Faithfulness
     3. 5.3 Interactions and Per-Item Trajectory Churn
  7. 6 Limitations
  8. 7 Conclusion
  9. References
  10. A Artifact Availability
  11. B Agent Implementation Details
     1. B.1 Prompt Assembly
     2. B.2 Shared Base Prompt
     3. B.3 Tool-Availability Blocks
     4. B.4 Tool Interfaces
     5. B.5 Example Execution Trace
  12. C LLM-as-a-Judge Prompt and Rubric
  13. D Additional Metric Validation Results
  14. E Human-Check Validation Details
     1. What kind of “soundness” is supported?
     2. Reviewer score threshold and majority rule.
     3. E.1 Compact Human-Check Case Studies
     4. E.2 Four-Reviewer Theorem-Name Overlap Diagnostic
  15. F Additional Factorial and Tool-Usage Details
  16. G Additional Domain Results
     1. G.1 Domain Metrics under Full Configuration
     2. G.2 Judge Scores by Domain
     3. G.3 Domain-Level Feedback Effects
     4. G.4 Domain-Level Effects of Search (S)
     5. G.5 Multi-Model Orchestrator Comparison



[ License: CC BY 4.0 ](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2606.31002v2 [cs.AI] 03 Sep 2026

# Beyond Compilation: Evaluating Faithful Natural-Language-to-Lean Statement Formalization

Ke Zhang  Affiliation: University of California, Riverside  Email: [kzhang153@ucr.edu](mailto:) Patricio Gallardo Candela ††thanks: Corresponding authors: Maziar Raissi and Patricio Gallardo Candela. Affiliation: University of California, Riverside  Email: [patricio.gallardocandela@ucr.edu](mailto:) Sudhir Murthy  Affiliation: University of California, Riverside  Email: [smurt002@ucr.edu](mailto:) Yi Xie  Affiliation: University of Arizona  Email: [yix@arizona.edu](mailto:) Zhi Wang  Affiliation: University of California, San Diego  Email: [zhw119@ucsd.edu](mailto:) Maziar Raissi* Affiliation: University of California, Riverside  Email: [maziar.raissi1@ucr.edu](mailto:)

###### Abstract

Lean verifies that a generated declaration is well typed, but not that it expresses the statement a user intended. We study two questions for autoformalization without canonical Lean targets: whether LLM judges can provide a usable proxy for human semantic review, and how much compilation overstates faithfulness across systems. Our criterion combines Lean compilation with strict semantic consensus between GPT-5.2 and Gemini-2.5-Pro. On an independently audited random sample, it agrees with human majority on 89.7% of cases (Wilson 95% CI: 82.1–94.3%). Across eight systems evaluated on 400 graduate-level statements, every system has a nonzero compile–faithfulness gap, whose observed magnitude ranges from 3.0 to 29.0 percentage points. The full GPT-5.2 tool-augmented agent shows the largest gap, compiling 89.5% while satisfying the semantic criterion on 60.5%. Human review, an independent third-family judge, and a BEq formal cross-check provide complementary evidence that the accepted core is reliable and that most audited outputs in the gap are genuine semantic mismatches. A secondary 232^{3} factorial analysis shows that elaboration feedback is the largest validity intervention, yet does not eliminate semantic drift. LLM judging is therefore useful as a human-calibrated, conservative aggregate measure, not as an equivalence oracle.

## 1 Introduction

Proof assistants such as Lean 4 de Moura and Ullrich (2021) provide a trusted kernel for checking formal syntax, types, and proofs. In theorem proving, the target statement is fixed, so checker acceptance is a strong success signal Zheng et al. (2022); Yang et al. (2023). In statement autoformalization, however, the model generates the target itself: a declaration may compile while omitting a hypothesis, changing a domain, or weakening the conclusion. The checker certifies the theorem the model wrote, not that it wrote the theorem the user meant.

This distinction is widely recognized. Existing work evaluates statement translation using reference pairs, back-translation, semantic scoring, human annotation, alignment models, or formal equivalence checks Azerbayev et al. (2023); Ying et al. (2024); Gao et al. (2025); Lu et al. (2025); Liu et al. (2025). The remaining practical difficulty is how to evaluate open-ended mathematical statements when multiple Lean encodings may be faithful and no canonical declaration is available. Compilation then measures formal validity, while exact-match or reference-dependent evaluation is unavailable.

We ask two empirical questions. Q1: Can an LLM-based semantic criterion approximate human review well enough for scalable evaluation? Q2: Is the compile–faithfulness gap systematic across model families, and how much does its size vary? We answer Q1 with blinded human audits, a same-sample comparison to LeanScorer Yu et al. (2025), a third-family judge, threshold sensitivity, and a BEq formal cross-check. We answer Q2 by applying one criterion to general LLMs, specialized formalizers, prover-oriented models, and tool-augmented agents on 400 graduate-level statements.

The answer is qualified but useful. On an independent random audit, the criterion agrees with human majority on 87/97 cases (89.7%, 95% CI: 82.1–94.3%). Every headline system shows a compile–faithfulness gap, ranging from 3.0 to 29.0 percentage points. For the full agent, compilation reaches 89.5%, but faithfulness reaches only 60.5%; human majority confirms 95/114 audited rejected compile-pass cases as genuine semantic failures. Thus LLM judging is not a semantic oracle, but human calibration makes it a practical aggregate measurement instrument.

#### Contributions.

First, we develop a reference-free, human-calibrated evaluation protocol that separates Lean validity from semantic faithfulness and triangulates the latter with human, cross-model, and formal evidence. Second, we quantify the compile–faithfulness gap across eight systems on a 400-statement graduate-level benchmark. Third, as a secondary diagnostic, we use a full 232^{3} factorial design to attribute validity, faithfulness, and efficiency changes to drafting, search, and elaboration feedback. We release the benchmark, outputs, evaluation scripts, human annotations, and tool-call logs.

## 2 Evaluation without Canonical Lean Targets

We address the task of statement formalization: automatically translating natural-language mathematical statements into valid Lean 4 theorem declarations. This task is the first step before proof search: it bridges informal human intent and machine-checkable syntax, but it does not attempt to prove the resulting declaration.

#### Statement formalization vs. theorem proving.

The distinction matters for evaluation. In theorem proving benchmarks, the formal statement is fixed; the system succeeds when it produces a proof accepted by the checker. In statement formalization, the statement is generated. The checker can reject ill-typed code, but it cannot decide whether a type-correct declaration is the intended translation of the natural-language input. Our benchmark and metrics therefore evaluate generated declarations, not proof search against trusted declarations.

### 2.1 Task Definition

Formally, let 𝒳\mathcal{X} be the space of informal mathematical statements and 𝒴\mathcal{Y} be the space of valid Lean 4 declarations. Given an input x∈𝒳x\in\mathcal{X}, the system must generate a statement y∈𝒴y\in\mathcal{Y} satisfying three criteria: syntactic validity (it compiles in Lean 4 with Mathlib), statement-centricity (it omits proofs via := by sorry), and semantic faithfulness (it expresses the same mathematical claim as xx).

### 2.2 Evaluation Context

Most Lean benchmarks study proof search from supplied formal statements Zheng et al. (2022); Yang et al. (2023); Ren et al. (2025); Wang et al. (2025); Lin et al. (2025). Autoformalization instead requires evaluating the generated target. ProofNet supplies Lean references Azerbayev et al. (2023); Lean Workbook combines compilation, back-translation, NLI, and human examination Ying et al. (2024); Herald uses compiler and back-translation checks Gao et al. (2025); FormalAlign evaluates informal–formal alignment Lu et al. (2025); Mathesis introduces LeanScorer Yu et al. (2025); and Beyond Gold Standards studies ensembles of LLM judges Zhang et al. (2025). BEq provides one-sided formal evidence by searching for verified implications between two formal statements Liu et al. (2025).

Our contribution is not the observation that compilation is insufficient, nor judge intersection by itself. It is a reference-free audited protocol and an empirical estimate of the resulting gap when no gold Lean target exists. Human review calibrates the decision boundary; LeanScorer, an independent model family, threshold tests, and BEq provide complementary checks.

### 2.3 Dataset Construction

To benchmark this task, we curated a dataset of 400 graduate-level statement entries derived from open-source LaTeX lecture notes and textbooks. We selected sources that provide natural-language statements without accompanying formal code, ensuring the task represents genuine translation rather than retrieval. As detailed in Table 1, the dataset is balanced across four domains—Real Analysis, Complex Analysis, Topology, and Algebra—with 100 examples from each; all benchmark rates are reported per entry rather than as counts of unique theorem schemas.

Table 1: Benchmark Dataset Composition. Domain |  Source Material | N  
---|---|---  
Real Analysis |  Basic Analysis (Lebl) Lebl (2025a) | 100  
Complex Analysis |  Cultivating Complex Analysis (Lebl) Lebl (2025b) | 100  
Topology |  Notes on Topology (McKay) McKay (2025) | 100  
Algebra |  Abstract Algebra (Doty) Doty (2025) | 100  
Total |  | 400  
  
### 2.4 Evaluation Protocol

We first compile each output in Lean 4 with Mathlib. For compiling outputs, GPT-5.2 and Gemini-2.5-Pro independently compare the natural-language source with the generated declaration and assign integer semantic-faithfulness grades from 0 to 10 under the shared rubric in Appendix C. Grades 9–10 indicate matching meaning, allowing at most a tiny discrepancy. We report the strict rule

| Faithful⁡(x,y)=Compiles⁡(y)∧gradeGPT​(x,y)≥9∧gradeGemini​(x,y)≥9.\mathrm{Faithful}(x,y)=\mathrm{Compiles}(y)\land\mathrm{grade}_{\mathrm{GPT}}(x,y)\geq 9\land\mathrm{grade}_{\mathrm{Gemini}}(x,y)\geq 9. |   
---|---|---  
  
This intersection is not itself a new judging algorithm. It is a deliberately strict operating point that we calibrate against human judgments. It neither certifies mathematical truth nor proves semantic equivalence.

#### Cross-judge consensus.

Across systems, Gemini-2.5-Pro consistently accepts more outputs than GPT-5.2, and most GPT-5.2 positives are also accepted by Gemini. Because our reported consensus label requires both judges, it is best viewed as an intersection rule accompanied by an empirical high-overlap pattern:

| PassConsensus=PassGPT∩PassGemini,|PassGPT∩PassGemini||PassGPT|​is high empirically.\mathrm{Pass}_{\text{Consensus}}=\mathrm{Pass}_{\text{GPT}}\cap\mathrm{Pass}_{\text{Gemini}},\qquad\frac{|\mathrm{Pass}_{\text{GPT}}\cap\mathrm{Pass}_{\text{Gemini}}|}{|\mathrm{Pass}_{\text{GPT}}|}\ \text{is high empirically}. |   
---|---|---  
  
Table 2 summarizes this GPT-to-Gemini empirical coverage at the system-family level; Appendix Table 12 gives the full per-system counts and the small number of GPT-only exceptions, and Appendix Figure 4 shows domain-level judge disagreement. Because the rows aggregate different numbers of systems, the consensus/GPT ratio rather than the raw count is the relevant quantity. This pattern supports using strict GPT∩\capGemini consensus as a conservative reported faithfulness metric.

Table 2: Cross-judge GPT-positive coverage summary. Counts are aggregated over different numbers of evaluated outputs; this table measures how often GPT-positive labels are also Gemini-positive and therefore counted by consensus, not system accuracy. Consensus counts outputs labeled faithful by both GPT-5.2 and Gemini-2.5-Pro. System group | Outputs | GPT-5.2 faithful | Consensus | Consensus/GPT  
---|---|---|---|---  
One-shot baselines | 3200 | 474 | 469 | 98.9%  
GPT-5.2 agent configs | 2800 | 1168 | 1144 | 97.9%  
Alt. orchestrators (111) | 800 | 534 | 524 | 98.1%  
Full system (111) | 400 | 248 | 242 | 97.6%  
  
## 3 Formalization Pipeline and Tool Factors

Figure 1: Agent orchestration logic. The orchestrator calls optional drafting, search, and compiler-feedback tools in Lean 4.

Figure 2: Multi-model agent comparison (config 111). All three orchestrators converge to 60–65% consensus-faithful outputs despite different one-shot baselines (19–28%).

The agent architecture, illustrated in Figure 2, is structured as a controlled implementation of three common remedies in autoformalization pipelines: drafting from a Lean-specialized prior, grounding through search, and repairing through verifier feedback. The core component is a central LLM orchestrator (GPT-5.2) that interacts with the Lean 4 environment via a defined API. Unlike static prompting, this architecture allows the model to maintain a persistent state, observing compiler errors, retrieved symbols, or draft translations before deciding on the next step. This design decouples natural-language reasoning from formal checking: Lean supplies high-precision validity feedback, while the orchestrator remains responsible for preserving the mathematical meaning of the input statement.

The purpose of this architecture is diagnostic rather than architectural novelty: it exposes separable information channels so that the same benchmark can ask which channel moves validity, faithfulness, or efficiency.

### 3.1 Tools and the Bottlenecks They Target

We equip the agent with tools that target different bottlenecks in statement formalization. Expert Drafting (T) is a parametric translation prior: the lean4_translator tool requests a specialized Lean statement draft from the fine-tuned Herald model before the general orchestrator edits or verifies it. Knowledge Search (S) provides Mathlib/context grounding through symbol lookup tools such as lean_inspect_name and lean_resolve_name, together with general web search; these tools return identifier candidates, types, and definitions, but they are not a dedicated semantic retrieval system such as LeanSearch Gao et al. (2024). Compiler Feedback (F) exposes Lean elaboration feedback through the lean_repl_runner, giving whole-statement validity checks and error messages for syntax, type, namespace, and elaboration repair.

We treat drafting (T), search (S), and elaboration feedback (F) as the three binary factors of a 232^{3} factorial study; the full design and notation are deferred to Section 5. Detailed specifications of the tool definitions and signatures are provided in Appendix B.

### 3.2 Controlled Prompt Assembly

To avoid confounding tool effects with prompt wording, all configurations use the same role definition and Lean-generation instructions: the agent must translate rather than prove, produce one theorem declaration ending in := by sorry, import Mathlib, and avoid invented definitions or axioms. The only part that changes is the tool-availability block, which declares which tools the agent may call. Thus, the factorial analysis varies access to drafting, search, and feedback tools while holding the task definition, output requirements, and anti-hallucination instructions fixed. Full prompt templates are provided in Appendix B.

## 4 Evaluation Results

### 4.1 Q1: Can LLM Judges Approximate Human Review?

We use three complementary audits rather than treating LLM agreement as ground truth (Table 3). The positive audit and Batch A condition on opposite regions of the full-agent decision boundary. Batch B is a separate full evaluation: 100 benchmark inputs are randomly sampled for Aristotle, with realized domain counts 28 Algebra, 26 Real Analysis, 23 Complex Analysis, and 23 Topology. Two missing Aristotle outputs leave 98 effective cases, of which 97 have a human-majority label. One reviewer performed the precise positive check; three different blinded reviewers covered the negative and independent audits, supplying the complementary negative check.

Table 3: Human calibration of the compile + GPT∩\capGemini criterion. Intervals are Wilson 95% CIs; conditional ranges below are descriptive, not pooled intervals. Audit |  System and selection |  Human coverage |  Calibrated result (95% CI)  
---|---|---|---  
Positive region |  GPT-5.2 full agent; random sample from compile-passing automatic positives. |  One expert; 140 selected, 138 scored; 133 satisfy the final strict rule. |  Precision: 130/133 = 97.7% [93.6, 99.2]%.  
Batch A: negative region |  Same full agent; all 116 compile-pass outputs rejected by strict consensus. |  Three blinded reviewers; 114/116 have a majority label. |  Negative confirmation: 95/114 = 83.3% [75.4, 89.1]%; 19 are human-rescued.  
Batch B: full evaluation |  Aristotle; 100 randomly sampled benchmark inputs; realized domains 28/26/23/23. |  Three blinded reviewers; 2 missing outputs leave 98 effective; 97 have a majority label. |  Agreement: 87/97 = 89.7% [82.1, 94.3]%. Precision: 64/69 = 92.8% [84.1, 96.9]%. Compile-pass negative confirmation: 17/22 = 77.3% [56.6, 89.9]%.  
  
Batch B gives the cleanest overall estimate: 89.7% human agreement (95% CI: 82.1–94.3%). Across the conditional audits, humans confirm 92.8–97.7% of automatic positives and 77.3–83.3% of compile-pass negatives. The rule is therefore a high-precision aggregate proxy, but conservative and imperfect per case. Appendix E reports the full review protocol and case-level analyses.

#### Same-sample comparison with LeanScorer.

On the same untuned Batch-B sample, our rule agrees with human majority on 87/97 cases versus 75/97 for the public two-stage LeanScorer rule (DeepSeek-V3-0324, threshold 0.6) Yu et al. (2025). The paired outcomes are 71 both correct, 16 ours only, 4 LeanScorer only, and 6 both wrong (exact McNemar p=0.0118p=0.0118). Six output-format variants were normalized deterministically and no calls failed. This supports our operating point on this sample, not universal evaluator superiority.

Table 4: Evaluator comparison on Batch B. Human-majority faithfulness is the comparison label; both rules use the same compilation results. Rule |  Human agreement |  Positive precision |  Negative confirmation  
---|---|---|---  
Compile + GPT∩\capGemini |  87/97 (89.7%) |  64/69 (92.8%) |  23/28 (82.1%)  
Compile + LeanScorer |  75/97 (77.3%) |  54/61 (88.5%) |  21/36 (58.3%)  
  
#### Independent judge and threshold robustness.

We apply the identical rubric and threshold to Claude Sonnet 5 (Table 5). Unresolved API calls are excluded from agreement denominators, not coded as unfaithful. Sonnet agrees with the primary rule on 91.8% of resolved full-agent outputs and 88.3% across all eight tool configurations. Varying the primary GPT/Gemini threshold from 7 to 10 preserves the ordering of factorial main effects: Feedback >> Search >> Translation, with effects of +27.2–35.6, +5.2–7.2, and +0.9–1.4 points, respectively. The winning configuration can change with the judge, so we claim robustness of the gap and bottleneck ordering, not a universal system ranking.

Table 5: Third-judge robustness. The final two columns partition agreements among resolved Sonnet calls. Scope |  Coverage |  Agreement |  Positive confirmed |  Negative confirmed  
---|---|---|---|---  
All 8 configurations |  2015/2055 (98.1%) |  1779/2015 (88.3%) |  1303/1413 (92.2%) |  476/602 (79.1%)  
Full configuration (111) |  354/358 (98.9%) |  325/354 (91.8%) |  228/242 (94.2%) |  97/112 (86.6%)  
  
#### Formal cross-check with BEq.

Because there is no canonical Lean target, we use 80 criterion-positive full-agent outputs independently confirmed by an expert (20 per domain) as anchors. Each source also has an accepted output from at least one of the other seven tool configurations; comparison with every such output yields 350 pairs. Adapted BEq-Normal Liu et al. (2025) requires Lean-verified implications in both directions and verifies that each proof uses its source statement. We run exact? first (204 certificates), then InternLM2-Math-Plus-20B with the published five-shot Normal-filter procedure (eight attempts, 512-token cap), adding 15. In total, BEq certifies 219/350 pairs (62.6%; anchor-cluster bootstrap 95% CI: 53.7–70.9%), including 128 pairs with different normalized encodings (Table 6). The other 131 are unresolved by bounded proof search, not disproved.

Table 6: BEq cross-check on accepted outputs. This is a formal-certification rate, not precision. Comparison subset |  Certified equivalent |  Not established  
---|---|---  
All accepted pairs |  219/350 (62.6%) |  131/350 (37.4%)  
Same normalized encoding |  91/91 (100%) |  0/91 (0%)  
Different normalized encodings |  128/259 (49.4%) |  131/259 (50.6%)  
  
Together, human review estimates agreement with the intended meaning, Sonnet tests model-family dependence, and BEq supplies sound positive certificates on a selected subset. None alone is an equivalence oracle; together they support a reliable accepted core and make the metric’s conservative boundary explicit.

### 4.2 Q2: How Large Is the Compile–Faithfulness Gap?

Figure 3 compares seven one-shot systems and the full agent on the same 400 statements. Compilation exceeds semantic acceptance for every system. The gap is system-dependent: 3.0–17.0 percentage points among the one-shot systems and 29.0 points for the full GPT-5.2 agent, an observed headline range of 3.0–29.0 points. Alternative full-agent orchestrators yield gaps of 15.0 and 27.5 points (Appendix G.5). The absolute faithful rates give context: general-purpose one-shot LLMs reach 19.8–28.0%, specialized formalizers 9.0–12.3%, and prover-oriented models 4.0–5.0%, compared with 60.5% for the full agent.

In prover-oriented runs, despite an explicit statement-only prompt requiring declarations ending in := by sorry, models frequently emit proof-oriented reasoning, tactic bodies, malformed declarations, or no extractable Lean statement. We therefore treat these baselines as a transfer diagnostic from proof training to statement generation, not as proof benchmarks. The conservative conclusion is not that prover models lack formalization ability in general, but that proof-oriented Lean competence does not automatically transfer to prompt-following, statement-centric, semantically faithful formalization when the formal target statement is not supplied.

The full agent makes the practical risk clearest: 358/400 outputs compile (89.5%), but only 242/400 (60.5%) satisfy the semantic criterion. Human majority confirms 95/114 reviewed cases in the rejected compile-pass bucket as genuine mismatches (83.3%, 95% CI: 75.4–89.1%), directly validating at least 95/400 = 23.8 percentage points of the 29.0-point gap. The gap is therefore not merely judge disagreement: compiler-guided repair can produce valid Lean without preserving the intended theorem.

Figure 3: Validity and semantic faithfulness across systems. Every system has a nonzero gap; the observed range is 3.0–29.0 percentage points on the same N=400N=400 statements.

Aggregate scores also hide substantial per-instance complementarity across tool settings (Table 7). The all-tools configuration is strong but not uniformly dominant: some cases it misses are solved by leaner configurations, and most of these recoverable misses already compile under 111 but fail strict semantic consensus. This makes the remaining bottleneck sharper than “REPL helps”: tool access changes the formalization trajectory, and the open problem includes per-instance routing or early stopping. Trajectory length is a useful warning signal specifically when feedback is enabled: pooling the four F=1F{=}1 configurations, faithfulness falls from 81.3% for 1–2 step runs to 12.0% for 19–24 step runs; across the nonempty no-feedback configurations, the corresponding drop is only 32.0% to 17.0% (Appendix Table 24).

Table 7: Across-configuration outcome structure for the custom GPT-5.2 agent. Counts are over the same 400 inputs and all eight tool configurations. The union row is an oracle diagnostic over completed experiments, not a deployed selector. Outcome | Count | Rate  
---|---|---  
All-tools config 111 faithful | 242/400 | 60.5%  
Best single config 011 faithful | 248/400 | 62.0%  
Faithful under at least one config | 313/400 | 78.2%  
Faithful under every config | 41/400 | 10.2%  
Never faithful under any config | 87/400 | 21.8%  
Missed by 111 but faithful elsewhere | 71/400 | 17.8%  
of missed: compile-pass under 111 | 55/400 | 13.8%  
of missed: compile-fail under 111 | 16/400 | 4.0%  
  
Additional orchestrator checks with Sonnet 4.5 and Gemini-2.5-Pro show the same pattern: all three 111 agents reach 60–65% consensus faithfulness despite different one-shot baselines (Figure 2; full table in Appendix G.5).

## 5 Bottleneck Decomposition

Aggregate accuracy collapses three different questions: whether an output compiles, whether it preserves the intended statement, and how much tool interaction it costs. A tool can raise compile rate while enlarging the compile-pass but semantically rejected bucket, so the diagnostic target is not just which tool helps on average, but which boundary each tool moves: validity, faithfulness, or efficiency.

### 5.1 Factorial Design over (T,F,S)

Formally, each tool setting is a bit vector

| c=(t,f,s)∈{0,1}3,𝒞={000,001,010,011,100,101,110,111},c=(t,f,s)\in\\{0,1\\}^{3},\qquad\mathcal{C}=\\{000,001,010,011,100,101,110,111\\}, |   
---|---|---  
  
where the bits denote access to (T,F,S). We run every benchmark item under every c∈𝒞c\in\mathcal{C} and evaluate metrics m⁡(c)m(c) such as compile rate, consensus-faithful rate, and tool cost. Main effects are high-minus-low averages over the other factors; for example,

| ΔF​(m)=14​∑t,s∈{0,1}[m⁡(t,1,s)−m⁡(t,0,s)].\Delta_{F}(m)=\frac{1}{4}\sum_{t,s\in\\{0,1\\}}\bigl[m(t,1,s)-m(t,0,s)\bigr]. |   
---|---|---  
  
Thus 111 is the full tool-augmented agent, while 000 is the One-Shot Baseline established in Section 4. The remaining seven configurations selectively toggle tool definitions in the system prompt while holding the task prompt fixed.

### 5.2 Main Effects: Validity vs. Faithfulness

Table 8 reports performance across all configurations, with each row comparing the same (T,S)(T,S) setting before and after elaboration feedback (F). To quantify the contribution of each factor, we compute standard factorial main and interaction effects, defined as differences in mean response between the high and low levels of a factor (averaged over the other factors).

Table 8: Bottleneck decomposition results. Performance across all 232^{3} configurations (N=400N=400). Each row fixes the translation prior (T) and search (S) factors and compares runs without vs. with elaboration feedback (F). Fixed factors | F=0F=0 | F=1F=1  
---|---|---  
T | S | Comp. | Faith. | Comp. | Faith.  
0 | 0 | 26.25 | 19.75 | 91.50 | 61.25  
1 | 0 | 30.25 | 24.50 | 93.50 | 58.75  
0 | 1 | 45.50 | 33.00 | 87.25 | 62.00  
1 | 1 | 50.00 | 36.00 | 89.50 | 60.50  
  
Beyond final accuracy, the key pattern is that tools move different boundaries. Feedback greatly expands validity: (000)→(010)(000)\to(010) increases compiled outputs from 105 to 366 and faithful outputs from 79 to 245, but also increases the compile-pass semantic gap from 26 to 121. Search has a different role: when feedback is enabled, it slightly changes final faithfulness but improves semantic selectivity, reducing the compile-pass gap from 121 to 101 for T=0T=0 and from 139 to 116 for T=1T=1. The full conditional table and tool-usage counts are in Appendix F.

Table 9: Bottleneck main effects on Faithful accuracy. Effects are average high-minus-low differences over the other two factors; 95% confidence intervals use paired item-level bootstrap resampling (B=10,000B=10{,}000). Factor | X=1X{=}1 | X=0X{=}0 | Effect | 95% CI  
---|---|---|---|---  
Elaboration feedback (F) | 60.6 | 28.3 | +32.3 | [28.6, 35.9]  
Grounding search (S) | 47.9 | 41.1 | +6.8 | [4.6, 9.1]  
Translation prior (T) | 44.9 | 44.0 | +0.9 | [−-1.3, 3.1]  
Table 10: Domain-wise effect of elaboration feedback. Effects are high-minus-low percentage-point differences for the feedback factor FF, computed within each domain under the same per-entry consensus metric. The gap column is compile-pass but consensus-unfaithful. Domain | Δ\Delta Compile | Δ\Delta Faithful | Δ\Delta Gap | Faithful|Compile (F=1F{=}1)  
---|---|---|---|---  
Complex Analysis | +66.2 | +54.2 | +12.0 | 81.5%  
Real Analysis | +56.8 | +31.2 | +25.5 | 57.4%  
Topology | +42.0 | +22.8 | +19.2 | 64.5%  
Algebra | +44.8 | +21.0 | +23.8 | 63.5%  
  
Feedback is therefore the largest validity intervention, but it is not a semantic oracle: it moves many noncompiling cases into both the faithful and compile-pass-but-unfaithful buckets. The domain split in Table 10 shows why this matters. Complex Analysis converts most feedback-driven validity gains into faithful statements, while Algebra and Topology gain far less in final faithfulness; for Topology, this pattern is consistent with advanced Mathlib encoding and coverage constraints in examples involving covering spaces and fundamental groups. Search improves final faithfulness mainly without feedback (ΔS​(F=0)=+12.4\Delta_{S}(F{=}0)=+12.4 pts vs. ΔS​(F=1)=+1.2\Delta_{S}(F{=}1)=+1.2 pts), and with feedback it mainly improves selectivity and efficiency: REPL calls fall by 29.8% for (010)→(011)(010)\to(011) and 26.6% for (110)→(111)(110)\to(111). The translation prior is not the limiting bottleneck in this tool stack: it helps without feedback (ΔT​(F=0)=+3.9\Delta_{T}(F{=}0)=+3.9 pts) but slightly hurts with feedback (ΔT​(F=1)=−2.0\Delta_{T}(F{=}1)=-2.0 pts), suggesting substitutability once a strong orchestrator has compiler feedback and grounding.

### 5.3 Interactions and Per-Item Trajectory Churn

The negative interactions make the result more specific than “REPL helps.” Paired item-level bootstrap intervals are F×S=−11.1F{\times}S=-11.1 [−15.8,−6.4-15.8,-6.4], F×T=−5.9F{\times}T=-5.9 [−10.0,−1.6-10.0,-1.6], and S×T=−0.4S{\times}T=-0.4 [−4.4,3.8-4.4,3.8] percentage points. Search and feedback partially substitute because both expose Mathlib-grounded information: search gives targeted symbol/type information, while feedback gives whole-statement elaboration diagnostics. Under this setup, Search is most valuable as a capability tool when feedback is absent and as an efficiency/selectivity tool when feedback is present. The same regime dependence appears for the translation prior: a specialist draft is useful in low-tool settings, but can anchor the repair loop once feedback is available. We treat this as an empirical observation about this tool stack, not as a claim that fine-tuned Lean translators are generally unnecessary.

The per-item transitions behind these aggregate effects are strongly nonmonotone (Table 11). Thus small net interaction effects can hide large trajectory churn. The useful design question is therefore not only which tool improves the average rate, but when an orchestrator should trust, ignore, or stop after a tool-induced repair path. This motivates per-instance routing or early-stopping policies, and the released trajectory logs are intended to support that follow-on analysis: final scores alone do not distinguish a clean first translation from a long repair loop that eventually compiles the wrong statement.

Table 11: Per-item transition ledger for tool additions. Each row compares the same 400 inputs before and after adding one tool under a fixed context. New faithful counts cases that become faithful; lost faithful counts cases that were faithful before but not after. Change | Configs | New faithful | Lost faithful | Net  
---|---|---|---|---  
Add F alone | 000→010000\to 010 | 175 | 9 | +166  
Add F with S | 001→011001\to 011 | 129 | 13 | +116  
Add F with T,S | 101→111101\to 111 | 117 | 19 | +98  
Add S with F | 010→011010\to 011 | 42 | 39 | +3  
Add S with T,F | 110→111110\to 111 | 38 | 31 | +7  
Add T with F,S | 011→111011\to 111 | 33 | 39 | -6  
  
## 6 Limitations

Our task is translating natural language into valid Lean 4 statement declarations, not generating proofs. Provability is neither necessary nor sufficient for statement faithfulness: a faithful declaration may be hard to prove automatically, while a provable declaration may formalize the wrong claim. Our LLM criterion is a scalable semantic proxy, not a formal equivalence proof, and its strict intersection rejects some human-accepted outputs. The region-conditional audits alone do not establish population-wide recall. Proprietary judges and overlap between the main orchestrator and one judge may introduce dependence; human review and Sonnet mitigate but do not eliminate it. The single-sample LeanScorer comparison does not establish universal metric superiority. The BEq analysis uses a selected subset anchored by expert-confirmed outputs; incomplete proof search supplies sound positive certificates but no conclusion for unresolved pairs.

The benchmark covers 400 statements from four open mathematical sources across four graduate areas; broader textbook coverage and research-level statements remain out of scope. The Search factor measures the retrieval tools implemented in this agent—Mathlib symbol lookup, namespace resolution, and general web search—not a dedicated semantic retriever such as LeanSearch Gao et al. (2024). Stronger retrieval may change the Search main effect and the F×SF{\times}S interaction. Finally, tool-augmented formalization is more expensive than one-shot generation; although Search reduces compiled iterations, the full REPL loop remains a barrier to real-time interactive use.

## 7 Conclusion

We reach two conclusions. First, compilation systematically overstates semantic success in this setting: the observed gap is 3.0–29.0 percentage points, and the strongest agent’s 89.5% compile rate falls to 60.5% under semantic evaluation. Second, LLM judging is usable when treated as a calibrated measurement instrument rather than ground truth: it reaches 89.7% human agreement on the independent audit, with human, third-judge, and formal checks supporting a reliable accepted core while exposing non-negligible false negatives.

The factorial analysis explains why the two conclusions belong together. Lean feedback is the largest validity intervention, yet it can move outputs into both the faithful and compile-pass-but-wrong buckets. Future autoformalization systems should therefore report validity and faithfulness separately and pair verifier-driven repair with semantic auditing, routing, and stopping policies.

## References

  * Azerbayev et al. (2023) Z. Azerbayev, B. Piotrowski, H. Schoelkopf, E. W. Ayers, D. Radev, and J. Avigad Proofnet: autoformalizing and formally proving undergraduate-level mathematics.  arXiv preprint arXiv:2302.12433.  Cited by: §1, §2.2. 
  * de Moura and Ullrich (2021) L. de Moura and S. Ullrich The Lean 4 theorem prover and programming language (system description).  In Automated Deduction – CADE 28,  LNCS, Vol. 12699, pp. 625–635.  External Links: [Document](https://dx.doi.org/10.1007/978-3-030-79876-5%5F37) Cited by: §1. 
  * Doty (2025) S. R. Doty Lecture notes on abstract algebra.  Note: <https://github.com/srdoty/AbstractAlgebraBook>GitHub repository; accessed 2025-09-04 Cited by: Table 1. 
  * Gao et al. (2024) G. Gao, H. Ju, J. Jiang, Z. Qin, and B. Dong A semantic search engine for mathlib4.  In Findings of the Association for Computational Linguistics: EMNLP 2024,  pp. 8001–8013.  External Links: [Document](https://dx.doi.org/10.18653/v1/2024.findings-emnlp.470), [Link](https://aclanthology.org/2024.findings-emnlp.470/) Cited by: §3.1, §6. 
  * Gao et al. (2025) G. Gao, Y. Wang, J. Jiang, Q. Gao, Z. Qin, T. Xu, and B. Dong Herald: a natural language annotated lean 4 dataset.  In The Thirteenth International Conference on Learning Representations,  Cited by: §1, §2.2. 
  * Lebl (2025a) J. Lebl Basic analysis: introduction to real analysis.  Note: <https://github.com/jirilebl/ra>GitHub repository; accessed 2025-09-04 Cited by: Table 1. 
  * Lebl (2025b) J. Lebl Guide to cultivating complex analysis: working the complex field.  Note: <https://github.com/jirilebl/ca>GitHub repository; accessed 2025-09-04 Cited by: Table 1. 
  * Lin et al. (2025) Y. Lin, S. Tang, B. Lyu, Z. Yang, J. Chung, H. Zhao, L. Jiang, Y. Geng, J. Ge, J. Sun, et al. Goedel-prover-v2: scaling formal theorem proving with scaffolded data synthesis and self-correction.  arXiv preprint arXiv:2508.03613.  External Links: [Link](https://arxiv.org/abs/2508.03613) Cited by: §2.2. 
  * Liu et al. (2025) Q. Liu, X. Zheng, X. Lu, Q. Cao, and J. Yan Rethinking and improving autoformalization: towards a faithful metric and a dependency retrieval-based approach.  In Proceedings of ICLR 2025 (Spotlight),  External Links: [Link](https://openreview.net/forum?id=hUb2At2DsQ) Cited by: §1, §2.2, §4.1. 
  * Lu et al. (2025) J. Lu, Y. Wan, Y. Huang, J. Xiong, Z. Liu, and Z. Guo FormalAlign: automated alignment evaluation for autoformalization.  In The Thirteenth International Conference on Learning Representations,  External Links: [Link](https://openreview.net/forum?id=B5RrIFMqbe) Cited by: §1, §2.2. 
  * McKay (2025) B. McKay Topology lecture notes.  Note: <https://github.com/Ben-McKay/topology-lecture-notes>GitHub repository; accessed 2025-09-04 Cited by: Table 1. 
  * Ren et al. (2025) Z. Ren, Z. Shao, J. Song, H. Xin, H. Wang, W. Zhao, L. Zhang, Z. Fu, Q. Zhu, D. Yang, et al. Deepseek-prover-v2: advancing formal mathematical reasoning via reinforcement learning for subgoal decomposition.  arXiv preprint arXiv:2504.21801.  Cited by: §2.2. 
  * Wang et al. (2025) H. Wang, M. Unsal, X. Lin, M. Baksys, J. Liu, M. D. Santos, F. Sung, M. Vinyes, Z. Ying, Z. Zhu, et al. Kimina-prover preview: towards large formal reasoning models with reinforcement learning.  arXiv preprint arXiv:2504.11354.  Cited by: §2.2. 
  * Yang et al. (2023) K. Yang, A. M. Swope, A. Gu, R. Chalamala, P. Song, S. Yu, S. Godil, R. Prenger, and A. Anandkumar LeanDojo: theorem proving with retrieval-augmented language models.  In Advances in Neural Information Processing Systems,  Vol. 36.  Cited by: §1, §2.2. 
  * Ying et al. (2024) H. Ying, Z. Wu, Y. Geng, J. Wang, D. Lin, and K. Chen Lean workbook: a large-scale lean problem set formalized from natural language math problems.  Advances in Neural Information Processing Systems 37, pp. 105848–105863.  Cited by: §1, §2.2. 
  * Yu et al. (2025) X. Yu, J. Zhong, Z. Feng, P. Zhai, R. Yousefzadeh, W. C. Ng, H. Liu, Z. Shou, J. Xiong, Y. Zhou, et al. Mathesis: towards formal theorem proving from natural languages.  arXiv preprint arXiv:2506.07047.  External Links: [Link](https://arxiv.org/abs/2506.07047) Cited by: §1, §2.2, §4.1. 
  * Zhang et al. (2025) L. Zhang, M. Valentino, J. Meadows, and A. Freitas Beyond gold standards: epistemic ensemble of LLM judges for formal mathematical reasoning.  arXiv preprint arXiv:2506.10903.  External Links: [Link](https://arxiv.org/abs/2506.10903) Cited by: §2.2. 
  * Zheng et al. (2022) K. Zheng, J. M. Han, and S. Polu MiniF2F: a cross-system benchmark for formal olympiad-level mathematics.  In ICLR,  Cited by: §1, §2.2. 



## Appendix A Artifact Availability

The repository containing the agent code, benchmark files, generated results, evaluation scripts, tool-call logs, and human-check materials is available at <https://anonymous.4open.science/r/neurips_happy_submission_anon-4AFF/README.md>.

## Appendix B Agent Implementation Details

### B.1 Prompt Assembly

The system prompt is constructed from three modular components: (i) a task definition establishing the core translation objective, (ii) a general usage guide containing fixed best practices for Lean 4 code generation, and (iii) a capability block that is dynamically populated based on the factorial configuration (T,F,S)(T,F,S). This structure holds the agent’s semantic goal and coding standards (i and ii) fixed, while selectively enabling or disabling external tools (iii) to isolate the causal effect of each capability. We assemble (i) and (ii) into a Shared Base Prompt, shown below, while the capability block definitions are provided in Appendix B.3.

### B.2 Shared Base Prompt

Base System Prompt You are an expert Lean4 translation agent. Your task is to translate a natural-language mathematical statement into faithful Lean4 syntax (NOT a proof). The final result must: \- import Mathlib at the very top \- compile in Mathlib \- be semantically faithful to the original statement \- end with ‘:= by sorry‘ You are NOT proving anything. You are only producing a correctly typed, correct-meaning Lean statement. GENERAL INSTRUCTIONS FOR CODE GENERATION •The Lean file MUST start with: import Mathlib •The Lean file MUST contain exactly ONE final translated statement representing the original natural-language meaning. •The final statement MUST end with: := by sorry •Do NOT write any proof code before ‘:= by sorry‘ (no ‘by‘, ‘simp‘, ‘have‘, ‘calc‘, etc. anywhere before the final ‘:= by sorry‘). •Do NOT invent new definitions, axioms, constants, or placeholder structures. •Prefer robust formulations: use quantifiers, membership, and ↔\leftrightarrow characterizations rather than fragile definitional equalities. •Only finish when the last written version: (1) compiles in Mathlib (if lean4_repl_runner is available) (2) is semantically faithful to the original statement When both are satisfied, return: "status": "success"

### B.3 Tool-Availability Blocks

Each factorial configuration (T,F,S)(T,F,S) determines which tools are exposed to the agent. We implement this by a modular prompt template in which the AVAILABLE TOOLS block is constructed by including the corresponding tool-specification entries and omitting inactive ones. We show the complete tool block for the fully enabled configuration (1,1,1)(1,1,1) below; other configurations are obtained by deleting the entries for tools that are disabled.

Tool Block (T=1, F=1, S=1) AVAILABLE TOOLS lean4_translator(statement)   
Draft a Lean 4 statement using the fine-tuned Herald translator (you may edit or ignore).  lean_write_file(code)   
Write the full Lean file to the workspace (imports + exactly one final statement).  lean4_repl_runner()   
Compile the current Lean file and return compiler feedback.  lean_inspect_name(name, imports?, include_print?)   
Query Mathlib about an identifier via #check/#print.  lean_resolve_name(token, namespace_hints?, imports?, top_k?)   
Suggest likely Mathlib identifiers for an unknown or ambiguous token.  search_online(query)   
Run a web search and return results for the query. 

### B.4 Tool Interfaces

Agent Tool API Tool |  Arguments |  Functionality  
---|---|---  
lean_inspect_name |  name, imports?, include_print? |  Checks whether a Mathlib symbol exists and returns its type (#check) and optionally its definition (#print).  
lean_resolve_name |  token, namespace_hints?, imports?, top_k? |  Performs fuzzy symbol resolution to map informal or incorrect names to valid Mathlib identifiers.  
lean4_repl_runner |  Lean 4 code to be executed |  Compiles the current Lean file and returns compiler diagnostics (errors, warnings, and success flags).  
lean4_translator |  statement |  Invokes the fine-tuned Herald translator to generate a draft Lean formalization of the natural-language input.  
search_online |  query |  Performs external web search to retrieve mathematical or documentation context not present in Mathlib.  
  
### B.5 Example Execution Trace

Example Execution Trace (agent tool calls) Step |  Tool |  Arguments (agent side)  
---|---|---  
1 |  lean_write_file |  path="jirilebl_ca_ca_17658.lean"; content = import Mathlib ... theorem jirilebl_ca_ca_17658 ... := by sorry  
2 |  lean4_repl_runner |  path="jirilebl_ca_ca_17658.lean"  
3 |  lean_inspect_name |  name="Polynomial.IsConstant"  
4 |  lean_inspect_name |  name="Polynomial.eval"  
5 |  lean_inspect_name |  name="Polynomial.isConstant"  
6 |  lean_inspect_name |  name="Polynomial.natDegree"  
7 |  lean_write_file |  path="jirilebl_ca_ca_17658.lean"; content = patched theorem uses p.natDegree ≠\neq 0 and Polynomial.eval  
8 |  lean4_repl_runner |  path="jirilebl_ca_ca_17658.lean"  
  
## Appendix C LLM-as-a-Judge Prompt and Rubric

We evaluate semantic faithfulness using an LLM-as-a-judge that receives: (i) the natural-language statement, (ii) the generated Lean 4 code, and (iii) a boolean compile_pass. The judge outputs a JSON object with fields faithful and grade (0–10). If compile_pass=false, we require faithful=false and restrict the grade to 0–3. The translation is considered as faithful if and only if the code compiles and the score is >=9>=9.

Judge system prompt (verbatim) You are an expert in Lean 4, Mathlib, and mathematics. You are judging TRANSLATION-ONLY. Input: (1) a natural-language statement, (2) a Lean 4 code snippet, (3) compile_pass boolean. Your job: decide whether the Lean code, AS A STATEMENT, matches the meaning of the natural-language statement. Key policy (NOT PICKY): \- If compile_pass = False: the translation is NOT faithful. grade must be 0..3. faithful=false. \- If compile_pass = True: ignore the proof/body entirely (including `by sorry`). Proof completeness is NOT part of the evaluation. \- A translation is faithful if the Lean statement expresses the same mathematical claim as the NL statement. Auxiliary definitions policy (lenient but not allowing cheating): \- Auxiliary defs/lemmas are allowed if they are reasonable encodings/abbreviations and do not change the meaning. \- However, if the code introduces a clearly vacuous placeholder for a nontrivial concept (e.g. `def X := True`, `:= none`, `:= 0` for something meant to be meaningful), and that placeholder is essential to making the final theorem appear to match, then the translation is NOT faithful. How to judge meaning (focus): \- Compare the MAIN theorem/definition statement(s) to the NL statement. \- Check quantifiers (forall/exists), logical structure (->/<->/and/or), and key hypotheses. \- Check main objects/domains: Nat/Int/Real, rings/groups, ZMod n, matrices, etc. \- Small implementation details are OK if the meaning is preserved. Scoring guide (integer 0..10): \- 0: unrelated. \- 1-3: compile_pass is False OR statement is clearly wrong. \- 4-6: compiles, but meaning is materially different / missing key hypotheses / wrong domain; might be "in the ballpark". \- 7-8: compiles, mostly matches, but has a noticeable mismatch (e.g. strengthened/weakened in an important way). \- 9: compiles, very close; only tiny mismatch. \- 10: compiles and meaning matches. Output contract (STRICT): Return a single JSON object with exactly these fields: { "faithful": true or false, "grade": 0..10, "thought": "### BEGIN THOUGHT\n<short explanation focusing on statement-level comparison>\n### END THOUGHT" } Return ONLY valid JSON. No extra keys. No markdown outside JSON.

## Appendix D Additional Metric Validation Results

Table 12: Full comparison of LLM judges and their consensus. Entries count translations that compile and are judged _Faithful_ by each judge; Consensus counts those labeled Faithful by both. GPT-only counts GPT-positive outputs not accepted by Gemini, showing that the GPT/Gemini relation is high-overlap rather than a deterministic hierarchy. System | Gemini | GPT-5.2 | Consensus | GPT-only  
---|---|---|---|---  
One-shot baselines  
Kimina-Prover | 18 | 16 | 16 | 0  
Goedel-Prover | 21 | 21 | 20 | 1  
Kimina-Autoformalizer | 43 | 36 | 36 | 0  
Herald Translator | 52 | 43 | 43 | 0  
StepFun-Formalizer | 55 | 49 | 49 | 0  
GPT-5.2 | 90 | 81 | 79 | 2  
Sonnet 4.5 | 145 | 116 | 114 | 2  
Gemini-2.5-Pro | 122 | 112 | 112 | 0  
Tool-augmented agents (GPT-5.2 orchestrator)  
Config 100 | 112 | 98 | 98 | 0  
Config 001 | 160 | 134 | 132 | 2  
Config 101 | 174 | 146 | 144 | 2  
Config 110 | 282 | 241 | 235 | 6  
Config 111 | 291 | 248 | 242 | 6  
Config 010 | 304 | 250 | 245 | 5  
Config 011 | 291 | 251 | 248 | 3  
Tool-augmented agents (alt. orchestrators, config 111)  
Sonnet 4.5 | 315 | 271 | 262 | 9  
Gemini-2.5-Pro | 307 | 263 | 262 | 1  
  
Across all rows in Table 12, the GPT-only colum
