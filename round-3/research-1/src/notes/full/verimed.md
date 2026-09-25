URL: https://arxiv.org/html/2605.13817 | FULL FETCH | 2026-09-24T01:49:03Z
warning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
URL: https://arxiv.org/html/2605.13817
Type: HTML
Length: 62174 chars (truncated)

--- Content ---

##### Report GitHub Issue

×

Title:

Content selection saved. Describe the issue below:

Description:

Submit without GitHub Submit in GitHub

arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[ Back to arXiv ](/)

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) Report Issue [ Back to Abstract ](/abs/2605.13817v1 "Back to abstract page") [ Download PDF](/pdf/2605.13817v1 "Download PDF") [ ](javascript:toggleNavTOC\(\); "Toggle navigation") [ ](javascript:toggleReadingMode\(\); "Disable reading mode, show header and footer")

  1. Abstract
  2. 1 Introduction
  3. 2 Methodology
     1. 2.1 Problem Formulation
     2. 2.2 Approach
     3. 2.3 Experimental Setup
     4. 2.4 Experiment 1: Requirement Autoformalization
     5. 2.5 Experiment 2: Counterexample-Guided Repair (CEGR)
     6. 2.6 Experiment 3: End-to-End Fault Detection
     7. 2.7 Experiment 4: Ambiguity Resolution
  4. 3 Limitations
  5. 4 Related Work
  6. 5 Conclusion and Future Work
  7. References
  8. A Generalizability Check: PCA Pump Requirements
  9. B Redundancy Analysis
  10. C Tables
     1. Reading the table.
  11. D Prompt Templates
  12. E Compute Resources



[ License: CC BY 4.0 ](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2605.13817v1 [cs.SE] 13 May 2026

# Neurosymbolic Auditing of Natural-Language Software Requirements

Bethel Hall  Affiliation: Stevens Institute of Technology  Email: [bhall2@stevens.edu](mailto:) William Eiers  Affiliation: Stevens Institute of Technology  Email: [weiers@stevens.edu](mailto:)

###### Abstract

Natural-language software requirements are often ambiguous, inconsistent, and underspecified; in safety-critical domains, these defects propagate into formal models that verify the wrong specification and into implementations that ship unsafe behavior. We show that large language models, equipped with an SMT solver, can audit such requirements: translating them into formal logic, detecting ambiguity through stochastic variation in the generated formalization, and exposing inconsistency, vacuousness, and safety violations through solver queries on the resulting specification. We present VeriMed, a neurosymbolic pipeline that operationalizes this idea for medical-device software requirements, and report two findings. First, stochastic variation across independent formalizations is a signal of ambiguity: requirements that admit multiple plausible interpretations produce SMT-inequivalent formalizations, and bidirectional SMT equivalence checking turns this disagreement into a solver-checkable test. Second, the usefulness of symbolic feedback depends on its granularity: in counterexample-guided repair on a hemodialysis question-answering benchmark, concrete SMT counterexamples raise verified accuracy from 55.4% to 98.5%. Over an extensive experimental evaluation on open-source hemodialysis safety requirements, we show that the LLM-based approach in VeriMed successfully reduces ambiguity-sensitive requirements and enables rigorous auditing of software requirements through SMT-based queries.

## 1 Introduction

Autoformalization, the translation of natural-language requirements into machine-verifiable specifications, has advanced rapidly with large language models [28]. Yet for safety-critical software requirements, syntactic validity is not enough. A well-formed formal specification can be globally inconsistent, contain requirements whose trigger conditions are unreachable, or admit multiple plausible readings of the same natural-language source. These failures are invisible by construction: when no ground-truth formalization exists, there is no oracle for correctness. This is inherent to LLM-generated formalizations, where the model resolves ambiguity by defaulting to the most statistically common reading in its training distribution or omits constraints implicit in the source.

This problem is especially acute in domains such as medical devices, where requirements specify alarm conditions, pump behavior, and safe parameter ranges. If the requirement set is inconsistent, or if the autoformalizer silently picks one reading among several, downstream verification can succeed while checking the wrong specification entirely. To address this, we propose VeriMed, a neurosymbolic framework that makes these failures detectable through two complementary checks. First, we audit the generated specification with solver queries that check global consistency, vacuousness, violatability, and redundancy at the requirement level, producing diagnostic flags that localize structural defects to specific requirements. Second, we detect and resolve ambiguity in the source text by exploiting the stochasticity of LLM-based autoformalizers as a diagnostic signal: sampling multiple independent SMT formalizations of the same requirement and comparing them with bidirectional SMT equivalence checking; persistent disagreement signals that the natural-language requirement admits more than one plausible reading. When defects are detected, we execute a targeted repair through a neurosymbolic feedback loop: solver feedback guides re-formalization for structural defects, and SMT-derived witnesses guide natural-language clarification for ambiguous requirements. The final requirement is then surfaced to the user for manual edits.

Our contributions are as follows:

  * •

We introduce a neurosymbolic framework for analyzing natural-language software requirements. The system, VeriMed, autoformalizes requirements into a single SMT model and uses the solver’s output as the primary signal for downstream review.

  * •

We formulate four requirement-level SMT audits — global consistency, vacuousness, violatability, and redundancy — that operationalize established requirement-quality criteria. Applied to a published hemodialysis specification, the audits flagged 2 of 64 requirements as redundant.

  * •

We show that the quality of solver feedback determines the effectiveness of LLM repair. In requirement-grounded question answering, using the violated requirements as feedback alone raises verified accuracy from 55.4% (no feedback) to 80.0%; providing an SMT counterexample as additional feedback raises accuracy to 98.5%.

  * •

We introduce ambiguity detection via bidirectional SMT inequivalence across independently sampled formalizations, using solver-generated witnesses to drive clarification. To our knowledge, this is the first application of solver-checked sample disagreement to software requirements analysis. On the hemodialysis benchmark, the procedure flagged 12 of 64 requirements (18.8%) as producing multiple distinct encodings; all 12 converged to a single encoding after clarification.




## 2 Methodology

### 2.1 Problem Formulation

Let R={r1,…,rn}R=\\{r_{1},\dots,r_{n}\\} be a set of natural-language software requirements. We translate RR into a single SMT model MM and use MM to answer three classes of queries: requirement-level audits, query verification against scenario-based safety questions, and ambiguity detection over the source text.

Encoding. Let TT denote the translation from a requirement rir_{i} to a formal encoding ρi=T⁡(ri)\rho_{i}=T(r_{i}). Most safety requirements take a conditional form: _“if condition PP holds, then action QQ must follow.”_ We encode each such requirement as ρi​(𝐱)≡pi​(𝐱)⇒qi​(𝐱)\rho_{i}(\mathbf{x})\equiv p_{i}(\mathbf{x})\Rightarrow q_{i}(\mathbf{x}), where 𝐱\mathbf{x} denotes the typed state variables of the system (Boolean control states and real-valued device parameters) and pi,qip_{i},q_{i} are quantifier-free formulas over Booleans and linear real arithmetic. Invariant requirements, those that must hold unconditionally, are encoded directly as state predicates ρi​(𝐱)\rho_{i}(\mathbf{x}) with no antecedent. We also maintain a set of global domain constraints C⁡(𝐱)C(\mathbf{x}) encoding background facts shared across all requirements, such as flow rates being non-negative. The full model is M=C∧⋀i=1nρi.M=C\wedge\bigwedge_{i=1}^{n}\rho_{i}.

Audit queries. We define four solver queries over MM that characterize the requirement set.

  1. 1.

_Global consistency_ asks whether MM is satisfiable. If MM is unsatisfiable, the requirements are mutually inconsistent, and an unsat core identifies a conflicting subset for repair.

  2. 2.

_Vacuousness_ applies to conditional requirements and asks whether the triggering condition pi​(𝐱)p_{i}(\mathbf{x}) can ever hold under the domain constraints. We check this by asking whether C∧pi​(𝐱)C\wedge p_{i}(\mathbf{x}) is satisfiable. If it is unsatisfiable, rir_{i} never applies and is therefore vacuous. Invariant requirements have no antecedent and are not subject to this check.

  3. 3.

_Violatability_ asks whether a requirement can be broken within the domain. We check C∧pi​(𝐱)∧¬qi​(𝐱)C\wedge p_{i}(\mathbf{x})\wedge\neg q_{i}(\mathbf{x}) for conditional requirements and C∧¬ρi​(𝐱)C\wedge\neg\rho_{i}(\mathbf{x}) for invariants; a satisfiable result returns a concrete violating assignment; an unsatisfiable result indicates that the violation is already ruled out by the domain constraints alone.

  4. 4.

_Redundancy_ asks whether M∖i=C∧⋀j≠iρjM_{\setminus i}=C\wedge\bigwedge_{j\neq i}\rho_{j} already enforces rir_{i}. We check M∖i∧pi​(𝐱)∧¬qi​(𝐱)M_{\setminus i}\wedge p_{i}(\mathbf{x})\wedge\neg q_{i}(\mathbf{x}) for conditional requirements and M∖i∧¬ρi​(𝐱)M_{\setminus i}\wedge\neg\rho_{i}(\mathbf{x}) for invariants; unsatisfiability in either case confirms redundancy, and the unsat core identifies the subsuming requirements.




Query verification. Given a scenario-based safety question translated into a formal claim ϕ\phi, we ask whether ϕ\phi is supported by the requirements by checking the formula M∧¬ϕM\wedge\neg\phi. If it is unsatisfiable, M⊧ϕM\models\phi and the claim is entailed; if it is satisfiable, the solver returns a counterexample showing a state consistent with MM but inconsistent with ϕ\phi, which is then used as feedback for repair.

Ambiguity detection. The previous queries treat MM as fixed; we now consider whether MM itself is well-determined by the source requirements. A natural-language requirement may admit more than one plausible reading, and the formalizer may silently commit to one. We define ambiguity operationally through agreement across independently sampled formalizations. Given two candidate encodings ρia\rho_{i}^{a} and ρib\rho_{i}^{b} of rir_{i}, we say they _agree_ if both C∧(ρia∧¬ρib)C\wedge(\rho_{i}^{a}\wedge\neg\rho_{i}^{b}) and C∧(ρib∧¬ρia)C\wedge(\rho_{i}^{b}\wedge\neg\rho_{i}^{a}) are unsatisfiable. If the first is satisfiable, the witnessing assignment exposes a state allowed by ρia\rho_{i}^{a} but ruled out by ρib\rho_{i}^{b}; if the second is satisfiable, the witness exposes a state allowed by ρib\rho_{i}^{b} but ruled out by ρia\rho_{i}^{a}. We sample NN formalizations of rir_{i} and apply this pairwise check; a requirement that produces more than one distinct encoding under bidirectional agreement is flagged as _ambiguity-sensitive_ , and the witnesses guide natural-language clarification. A requirement whose samples all agree is treated as admitting a single formalization under repeated sampling.

Figure 1: Architecture of VeriMed. Figure 2: Ambiguity-resolution loop with a dialysate-temperature example. VeriMed samples N=5N=5 independent formalizations and compares them via bidirectional SMT equivalence. Here, ρ1\rho_{1}, ρ2\rho_{2}, and ρ3\rho_{3} express different boundary interpretations of the same temperature range: ρ1\rho_{1} excludes both endpoints, ρ2\rho_{2} includes both endpoints, and ρ3\rho_{3} excludes 33∘C but includes 40∘C. The solver returns concrete disagreement witnesses (e.g., 33∘C, 40∘C), which the LLM uses to rewrite the requirement with explicit boundary semantics. The loop repeats until all samples are semantically equivalent, then surfaces the clarified requirement for the user to review. Schema Variable Type Description bolus_active Bool Bolus active volume Real Volume (mL) alarm_active Bool Alarm active |  NL If bolus is active and infused volume exceeds 400 mL, the alarm shall activate. SMT (=> (and bolus_active (> volume 400.0))   
alarm_active)  
---|---  
Figure 3: Example variable schema and SMT encoding generated from a requirement.

### 2.2 Approach

We introduce VeriMed11 1 Code and data will be released upon acceptance of the paper., a neurosymbolic framework for turning natural-language software requirements into a solver-checkable specification. VeriMed couples an LLM-based autoformalizer with an SMT solver to run the audit, query verification, and ambiguity checks defined in Section 2.1. A central design choice is that all requirements are expressed in the same symbolic namespace. We define a fixed schema of typed state variables, covering Boolean control states and real-valued device parameters, together with the domain constraints C⁡(𝐱)C(\mathbf{x}). The schema is injected into every LLM prompt, ensuring independently generated assertions compose into a single model MM.

VeriMed operates as a four-stage pipeline as shown in Figure 1: the Ambiguity Resolver screens each requirement for stable formalization before the requirement is formalized; the Autoformalizer translates the requirement set into SMT-LIB; the Property Verifier audits the resulting model; and the Query Verifier checks proposed answers to scenario-based safety questions against the model.

A

Ambiguity Resolver. Natural-language requirements are prone to ambiguity [22]: an LLM autoformalizing an ambiguous requirement may silently commit to one reading among several. The Ambiguity Resolver screens each requirement before it enters the formalization pipeline. For each ri∈Rr_{i}\in R, it samples the LLM NN times at elevated temperature to obtain candidate encodings ρi1,…,ρiN\rho_{i}^{1},\dots,\rho_{i}^{N} and applies the bidirectional agreement check defined in Section 2.1 to every pair. A requirement that produces more than one distinct encoding is flagged as ambiguity-sensitive: the witnessing assignments from the disagreeing pairs are surfaced as concrete distinguishing states, and the LLM is prompted to rewrite the source text until the samples converge. Only requirements that pass screening are forwarded to the Autoformalizer. Figure 2 illustrates the clarification loop.

B

Autoformalizer. The Autoformalizer translates the disambiguated requirement set into a single SMT-LIB specification [5]. The LLM receives the requirement set together with the canonical schema and the domain constraints, and produces the requirement predicates ρ1,…,ρn\rho_{1},\dots,\rho_{n} along with the declarations needed to assemble MM. The output is therefore not a collection of isolated formulas but a unified model whose assertions can be analyzed jointly. If the generated SMT (e.g., Figure 3) is malformed or rejected by the solver, the system enters a bounded syntactic repair loop. The solver error message and the failed output are returned to the LLM as feedback, and regeneration continues until a syntactically valid model is produced or the retry budget is exhausted. This loop addresses syntactic faults only; semantic audits are delegated to the Property Verifier.

C

Property Verifier. The Property Verifier runs the four audit queries defined in Section 2.1 over the assembled model MM: global consistency, vacuousness, violatability, and redundancy. For each requirement, the verifier records the outcome of every applicable check and, when an audit fails, returns the diagnostic information the solver provides: an unsat core for inconsistency or redundancy, and a concrete violating assignment for violatability. These diagnostics localize each defect to a specific requirement or subset of requirements and serve as the input to any downstream repair.

D

Query Verifier. The Query Verifier tests whether a proposed answer is entailed by MM under a given scenario. A scenario extractor maps the question to a structured state assignment ss, an action generator produces a schema-constrained candidate answer aa, and the verifier issues the entailment query M∧s∧¬aM\wedge s\wedge\neg a. Unsatisfiability confirms entailment by the requirements under the scenario and is accepted; a satisfiable result returns a counterexample exposing a state consistent with MM and ss but inconsistent with aa. A secondary check identifies the specific requirements violated in the counterexample, and a response builder translates the result into a natural-language explanation. When a violation is found, the repair loop re-prompts the LLM with the violated requirements and, in the counterexample-guided variant, the solver counterexample itself.

### 2.3 Experimental Setup

Domain and benchmark. We evaluate VeriMed on the hemodialysis machine case study of Mashkoor [19], using a corpus of 64 natural-language safety requirements drawn from the software requirements specification. The requirements cover alarm conditions, flow constraints, connectivity constraints, and numeric limits across multiple machine phases and subsystems.

Schema, formalism, and solver. All experiments share the same canonical typed schema and the same global domain constraints C⁡(𝐱)C(\mathbf{x}). The schema contains 85 typed variables covering Boolean machine states and real-valued device parameters. All formalizations are expressed in SMT-LIB2 over quantifier-free linear real arithmetic with Booleans. We use Z3 [11] for all SMT checks.

Language models. The primary LLM is claude-sonnet-4-6, used for SMT generation, answer generation, and repeated formalization across all experiments. Temperature is 0 for deterministic outputs (answer generation and repair), 1.0 for ambiguity detection (exposing alternative encodings), and 0.2 for clarification of ambiguous requirements. A secondary model, claude-haiku-4-5-20251001, is used at temperature 0 for the lightweight answer-to-assignment translation step, with a rule-based fallback parser if translation fails. SMT generation uses a 16,384-token output budget and a syntactic repair loop of up to five retries. LLM calls are stateless: each call reconstructs the full prompt, with explicit repair feedback appended when applicable.

### 2.4 Experiment 1: Requirement Autoformalization

Before any audit can be trusted, the formalization must be trustworthy. This experiment evaluates whether VeriMed can translate the 64 hemodialysis safety requirements into a single solver-checkable SMT model that is semantically faithful to the source, covering generation quality, round-trip fidelity, and sensitivity to requirement-level faults.

Setup: Generation. The Autoformalizer receives the full requirement set together with the canonical typed schema and produces the complete SMT-LIB model in a single batch translation, rather than encoding each requirement independently. If the generated output fails to parse or is rejected by Z3, the autoformalizer regenerates with the solver’s error message as feedback, capped at five retries. We then run the four audit queries from Section 2.1 over the assembled model.

Round-trip semantic equivalence check. To test whether the generated SMT is semantically faithful to the source requirements, following the round-trip faithfulness check approach of Amrollahi et al. [3], we run a round-trip translation cycle. The generated model is first translated back into structured natural-language requirements which are then re-formalized under the same canonical schema. Each reconstructed formula is compared to its original under bidirectional SMT equivalence. We also report the mean cosine similarity between original and reconstructed requirement texts using normalized embeddings from all-mpnet-base-v2.

Mutation stress test. To test model sensitivity to requirement-level faults, we construct 256 mutated requirements spanning four fault categories drawn from FDA MAUDE adverse-event reports for hemodialysis machines [24]: false-alarm trigger suppression, mode-transition guard removal, value mismatch, and limit violation. Each mutated requirement is compared against the canonical model using bidirectional SMT equivalence; a mutation is detected if either direction returns sat.

Metrics. We report parse success rate, the four requirement-level audit outcomes, round-trip equivalence and mean cosine similarity, and per-category and overall mutation detection rates. Binomial rates are reported with two-sided Wilson 95% confidence intervals.

Result and Insight. The results are shown in Table 1. The Autoformalizer produced a solver-checkable SMT model covering all 64 requirements on the first generation attempt. The resulting model was globally consistent and contained no vacuous requirements; 2 requirements were redundant under the rest of the specification. All 64 requirements survived the round-trip check: every reconstructed requirement re-formalized to a bidirectionally equivalent formula, with mean cosine similarity of 96.2% between original and reconstructed texts. Under mutation testing, the audit pipeline detected 249 of 256 single-requirement mutations (97.3%, Wilson 95% CI [94.5%, 98.7%]) across the four fault categories. Observation: Natural-language safety requirements contain latent defects that solver-level checks make visible. Our approach flagged r11r_{11} and r56r_{56} as redundant. For r11r_{11}, the unsat core contains r55r_{55}: r11r_{11} concerns venous pressure falling below its lower limit, while r55r_{55} requires venous pressure to remain at least 22.5 mmHg above that limit, making r11r_{11}’s trigger unreachable. For r56r_{56}, the unsat core contains r42r_{42}: r56r_{56} concerns dialysate conductivity outside the permissible range, while r42r_{42} requires conductivity to stay between 12.5 and 16.0 mS/cm. These requirements are not locally vacuous under the domain constraints alone; their guards are satisfiable against CC. They become redundant only once the surrounding requirements are added. This makes redundancy a review signal rather than a verdict: the engineer should inspect whether the subsuming requirement is intentionally ruling out the condition, or whether one of the requirements is too strong. Details anaylysis on the redundancy is provided in Appendix B.

Generalizability. To test whether the round-trip results transfer beyond the hemodialysis benchmark, we applied the same pipeline end-to-end to an open-source PCA (patient-controlled analgesia) pump specification with 144 requirements: the autoformalizer produced an SMT model from the new requirement set, and the round-trip check ran on that model. The cycle reconstructed all 144 requirements; initial bidirectional SMT equivalence held for 135 of 144 (93.75%), and a single repair iteration closed the remaining 9 cases, reaching full equivalence (144/144). Mean cosine similarity between original and reconstructed requirement texts was 0.87, lower than the hemodialysis result, with the largest textual gaps concentrated in compliance-related requirements where reconstruction paraphrased more aggressively. Despite the lexical drift, the repaired re-formalizations recovered the original SMT semantics exactly. Details of the audited redundant requirements are in Appendix B.

Table 1: Experiment 1 results. (a) Audit and round-trip results on 64 requirements. (b) Mutation stress test on 256 mutated cases. RT = round-trip; CIs are Wilson 95% for binomial rates.

Metric | Frac. | % | 95% CI  
---|---|---|---  
Requirements covered | 64/6464/64 | 100.0100.0 | [94.3,100.0][94.3,100.0]  
Non-vacuous (cond.) | 39/3939/39 | 100.0100.0 | [91.0,100.0][91.0,100.0]  
Violatable | 64/6464/64 | 100.0100.0 | [94.3,100.0][94.3,100.0]  
Redundant | 2/642/64 | 3.13.1 | [0.9,10.7][0.9,10.7]  
RT equivalence | 64/6464/64 | 100.0100.0 | [94.3,100.0][94.3,100.0]  
RT cosine sim. (mean) | — | 96.296.2 | —  
  
(a) Audit and round-trip.

Mutation type | Frac. | % | 95% CI  
---|---|---|---  
False alarm | 64/6464/64 | 100.0100.0 | [94.3,100.0][94.3,100.0]  
Mode transition | 63/6463/64 | 98.498.4 | [91.7,99.7][91.7,99.7]  
Value mismatch | 62/6462/64 | 96.996.9 | [89.3,99.1][89.3,99.1]  
Limit violation | 60/6460/64 | 93.893.8 | [85.0,97.5][85.0,97.5]  
Overall | 249/256249/256 | 97.397.3 | [94.5,98.7][94.5,98.7]  
  
(b) Mutation stress test.

### 2.5 Experiment 2: Counterexample-Guided Repair (CEGR)

We evaluate whether SMT feedback repairs incorrect LLM answers about mandatory machine actions, and in particular whether concrete counterexamples drive more repair than symbolic feedback alone.

Setup. We evaluate on 65 scenario-based safety questions derived from the HD machine case study, drafted with LLM assistance and reviewed manually to ensure that each question maps to a specific requirement subset and a solver-verifiable answer. Each question describes a concrete machine state and asks what mandatory device actions follow. The benchmark contains single-requirement queries (29), multi-requirement queries (15), and no-requirement queries (21). For each question, the LLM produces a structured JSON answer constrained to schema variables relevant to that question. Given model MM, scenario ss, and candidate answer aa, the verifier checks M∧s∧¬aM\wedge s\wedge\neg a, labeling results safe (unsat, no counterexample exists), violation (sat, a counterexample exists), or unknown. Only safe answers are counted as correct. All conditions use the same prompt, answer format, and verifier, differing only in rejection feedback: baseline (no feedback), self-repair (generic rejection message), requirement feedback only (violated requirements only), full CEGR (violated requirements and Z3 counterexample witness). Each condition has one initial attempt and up to five repair iterations.

Metrics. We report first-attempt accuracy (pass@1), final accuracy after the repair budget, and repair success rate. Accuracy is the fraction of questions labeled safe by the verifier. Repair success rate is the fraction of initially non-safe answers that become safe within the repair budget.

Result and Insight. Figure 4 shows the results. CEGR achieves 98.5% final accuracy, exceeding the no-feedback baseline (55.4%), self-repair (58.5%), and requirement-only feedback (80.0%). First-attempt accuracy is comparable across conditions (baseline 49.2%, self-repair 53.8%, requirement-only 46.2%, CEGR 46.2%); the divergence emerges entirely from repair behavior. Repair success rate follows the same pattern: 12.1%, 10.0%, 59.4%, and 97.1%, respectively. The 18.5-point gap between requirement-only feedback and full CEGR shows that the counterexample, not solver feedback in general, is what drives repair: returning a concrete witness state lets the LLM localize the fault in its previous answer in a way that violated requirements alone do not. Observation: With the LLM and prompt held fixed, the choice of feedback signal impacts repair outcomes. First-attempt accuracy across the four conditions ranged narrowly from 46.2% to 53.8%. After up to five repair iterations, final accuracy ranged from 55.4% to 98.5%, and repair success rate from 10.0% to 97.1%. The conditions differed only in what the verifier returned after a rejected answer, so the spread is attributable to the feedback signal. See Appendix 6 for a sample of questions and verified responses.

Figure 4: Effect of verifier feedback on question answering. (Left) accepted on the first attempt, fixed during repair, and rejected after the repair budget. (Right) Cumulative SMT-verified accuracy.

### 2.6 Experiment 3: End-to-End Fault Detection

Experiment 1 showed that the canonical SMT model distinguishes mutated formulas under bidirectional equivalence. This experiment tests the complementary claim: whether the full pipeline, including re-autoformalization, catches faults injected one at a time into the requirement set.

Setup. For each of the 64 hemodialysis requirements rir_{i}, we manually write a mutated natural-language version rimutr_{i}^{\text{mut}} representing a plausible safety defect: a changed threshold, a weakened trigger condition, or an incorrect control action. We autoformalize each mutated requirement into a mutant SMT block ρimut\rho_{i}^{\text{mut}}, and construct the modified model M(i)M^{(i)} by replacing ρioriginal\rho_{i}^{\text{original}} with ρimut\rho_{i}^{\text{mut}} in the canonical model while keeping the shared schema, the global domain constraints CC, and the remaining 63 requirement blocks fixed.

Figure 5: Mutation Detection. (Left) detection outcomes by fault type: circles denote a detected mutant, a red cross denotes the single missed mutant. (Right) benchmark composition by fault type.

Evaluation. A fault is detected if either of two conditions holds: (a) the modified model M(i)M^{(i)} is globally inconsistent, indicating that rimutr_{i}^{\text{mut}} contradicts the original requirements; or (b) the mutant and original requirements are semantically distinguishable, checked by bidirectional satisfiability between ρimut\rho_{i}^{\text{mut}} and ρioriginal\rho_{i}^{\text{original}} under CC. We test whether C∧ρimut∧¬ρioriginalC\wedge\rho_{i}^{\text{mut}}\wedge\neg\rho_{i}^{\text{original}} is satisfiable (the mutant permits a behavior ruled out by the original requirement) and whether C∧ρioriginal∧¬ρimutC\wedge\rho_{i}^{\text{original}}\wedge\neg\rho_{i}^{\text{mut}} is satisfiable (the original requirement allows a behavior ruled out by the mutant); a satisfiable result in either direction signals detection. This disjunction separates faults that produce immediate contradictions from faults that remain satisfiable but still change the intended safety behavior.

Result and Insight. Figure 5 shows the complete result: VeriMed detected 63 of 64 inserted defects (98.4%, Wilson 95% CI [91.7%, 99.7%]). All 64 mutated requirement sets autoformalized successfully and remained globally satisfiable, so detection came entirely from comparing original and mutated encodings. Detection was complete for limit violations (34/34), mode-transition changes (24/24), and false-alarm changes (2/2). For value mismatches, 3 of 4 mutants were detected; the missed case was the mutant for r2r_{2}, which was indistinguishable from the original under the current schema. Observation: Consistency alone does not always catch requirement faults. Every mutated specification remained globally satisfiable, yet 63 of 64 defects were detected. The r20r_{20} mutant shows why: the original requires disconnection and an alarm when dialysate temperature falls below 33∘C; the mutant requires the opposite. Both are still globally satisfiable, but only the original reflects the intended safe behavior. Internal consistency alone is therefor insufficient; the useful signal is behavioral preservation.

### 2.7 Experiment 4: Ambiguity Resolution

We evaluate whether the SMT-solver feedback can be used not only to detect ambiguous requirements, but also to reduce ambiguity in the natural-language specification.

Setup: We apply the Ambiguity Resolver (Section 2.2) to all 64 hemodialysis requirements with N=5N=5 samples per requirement. Requirements that remain ambiguity-sensitive after clarification are re-screened; the clarified requirements are stitched back into the full 64-requirement set. Result and Insight: Figure 6 shows the results. 12 out of the 64 requirements were flagged as ambiguity-sensitive (18.8%, CI [11.1%, 30.0%]); pairwise SMT agreement across all formalization pairs is 44.0% (CI [41.7%, 46.3%]). After SMT-guided clarification, ambiguity-sensitive requirements drop to 0/64 (0.0%, CI [0.0%, 5.7%]) and pairwise SMT agreement reaches 100% (CI [99.4%, 100.0%]), with mean distinct encodings per requirement falling from 1.59 to 1.00. All 320 clarified formalizations remain syntactically valid and locally verified, confirming that the clarification loop eliminates encoding ambiguity without introducing inconsistency. Observation: SMT disagreement across samples flags requirements that the formalizer reads in more than one way. One recurring source of ambiguity is overlapping numeric ranges: R-24 and R-25 [19] specify air-detection thresholds for _“0 to 200 mL/min”_ and _“200 to 400 mL/min,”_ leaving the endpoint 200 ambiguous. The autoformalizer split on this, producing encodings that disagreed at exactly 200 mL/min. Solver-generated witnesses surfaced each such disagreement as a concrete state, and the clarification loop converged on a single reading for every flagged requirement (see Appendix 5 for the full list).

Figure 6: Ambiguity detection and resolution via repeated autoformalization. (A) Share of requirements flagged as ambiguity-sensitive versus non-ambiguous. (B) Distinct SMT encodings per flagged requirement, ranked by count. (C) Ambiguity-sensitive count across five rounds of SMT-guided clarification. (D) Pairwise SMT agreement.

## 3 Limitations

Generalizability. Our evaluation targets hemodialysis machine requirements, with a secondary evaluation on a PCA pump specification (Appendix A). Both are infusion-related medical devices with shared structural features. We cannot establish that our findings transfer to structurally different device classes or to non-medical domains, and we make no such claim.

Faithfulness. Our approach does not directly measure whether an LLM-generated formalization is fully faithful to the intent of the original requirement. That is a non-trivial challenge. Instead, we use a collection of proxy signals, including consistency, mutation sensitivity, ambiguity detection, round-trip similarity, and downstream repair performance. These signals are useful but incomplete: a formalization can pass some of them while still missing subtle aspects of the intended meaning.

Temporal Requirements. A further limitation of our work is temporal expressiveness. Since we use SMT as our core formalism, temporal requirements are modeled using current state conditions rather than a full temporal logic. For example, requirements such as “the blood pump stops and remains stopped” or “after 400 mL have been reinfused, the alarm shall activate” are approximated in terms of the current system state instead of temporal relations across states.

Scalability and Deployment Risk. Industrial medical software requirements documents are often an order of magnitude larger than the datasets used in this work. The result of this work should not be used in safety-critical applications without independent review by experts.

## 4 Related Work

Autoformalization Since [28] demonstrated LLM-based autoformalization for mathematical theorems, neurosymbolic research has focused on combining autoformalization with downstream verification [7, 17, 28, 1]. However, the autoformalization step itself is rarely scrutinized. In particular, existing work rarely evaluates whether the generated formalizations are consistent, correct, and unambiguous as specifications [23, 29, 14]. Prior work on autoformalization has largely focused on mathematical domains, where formal statements are well-defined and can be verified against proofs [2, 16, 10]. However, VeriMed operates on natural language software requirement specifications: theorems are self-contained and unambiguous by construction, while natural-language requirements often contain underspecification and ambiguity that the formalization step must surface rather than ignore. VeriMed addresses both gaps: it checks the correctness of the formalization itself, and uses verifier feedback to drive repair.

Ambiguity Resolution. Ambiguity is a central obstacle in formalizing natural-language requirements. Recent work uses LLMs to detect and explain ambiguities [6], or surfaces them directly during code generation via clarifying questions [20, 26, 27]. These approaches treat ambiguity as a textual property to flag or paraphrase away without deterministic resolution. Our approach forces ambiguities to manifest in the form of multiple machine-checkable inequivalent encodings of the same requirement.

Requirements Formalization with LLMs. Recent efforts evaluate correctness only at the artifact level. Cao et al. [9] benchmark ten LLMs across five proof targets, scoring outputs by whether the checker accepts the output; however, acceptance can conceal incorrect properties. Mandal et al. [18] synthesize configuration specifications from software manuals, but evaluate only against gold labels with no semantic check. Beg et al. [8] survey LLM-based specification tools and frame the open problem as bridging informal natural language and rigorous formal specifications, with no system closing the loop at the requirement level. VeriMed closes this loop, using SMT equivalence between the original encoding and a re-formalization of the LLM’s own informalization to detect semantic drift at the requirement level.

Formal Analysis of Medical Device Software Requirements. Medical device software has long served as a testbed for requirements formalization. The FDA Generic Patient-Controlled Analgesia infusion pump was formalized as timed automata in UPPAAL by Kim et al. [15], and the hemodialysis machine case study introduced at ABZ 2016 [19] has since been formalized in Circus [12], Event-B [13], and Abstract State Machines [4], each constructed manually by formal-methods experts. More recent LLM-based work has begun to automate this translation: Wang et al. [25] pair Claude 3.5 Sonnet with the ESBMC bounded model checker on nine Lockheed Martin cyber-physical systems.

## 5 Conclusion and Future Work

We presented VeriMed, a neurosymbolic framework for autoformalizing and auditing natural-language medical-device software requirements with SMT solver feedback. Because software requirements typically lack a gold formal target, VeriMed relies on two solver-grounded signals: satisfiability queries over the assembled formal model and agreement among independently sampled formalizations. We show that concrete SMT counterexamples are the strongest repair signal for requirement-grounded question answering, and that repeated formalization exposes hidden ambiguity. Future work should extend VeriMed to automated schema construction and temporal formalisms.

## References

  * [1] A. Akinfaderin and S. Subramanian (2025) VERAFI: verified agentic financial intelligence through neurosymbolic policy generation.  arXiv preprint arXiv:2512.14744.  Cited by: §4. 
  * [2] M. Allamanis, S. Panthaplackel, and P. Yin (2024) Unsupervised evaluation of code llms with round-trip correctness.  arXiv preprint arXiv:2402.08699.  Cited by: §4. 
  * [3] D. Amrollahi, J. Lopez, and C. Barrett (2026) Faithful autoformalization via roundtrip verification and repair.  arXiv preprint arXiv:2604.25031.  Cited by: §2.4. 
  * [4] P. Arcaini, S. Bonfanti, A. Gargantini, and E. Riccobene (2016) How to assure correctness and safety of medical software: the hemodialysis machine case study.  In International Conference on Abstract State Machines, Alloy, B, TLA, VDM, and Z,  pp. 344–359.  Cited by: §4. 
  * [5] C. Barrett, P. Fontaine, and C. Tinelli (2016) The satisfiability modulo theories library (smt-lib). www.  SMT-LIB. org 2, pp. 68.  Cited by: §2.2. 
  * [6] S. Bashir, A. Ferrari, A. Khan, P. E. Strandberg, Z. Haider, M. Saadatmand, and M. Bohlin (2025) Requirements ambiguity detection and explanation with llms: an industrial study.  In 2025 IEEE International Conference on Software Maintenance and Evolution (ICSME),  pp. 620–631.  Cited by: §4. 
  * [7] S. Bayless, S. Buliani, D. Cassel, B. Cook, D. Clough, R. Delmas, N. Diallo, F. Erata, N. Feng, D. Giannakopoulou, et al. (2025) A neurosymbolic approach to natural language formalization and verification.  arXiv preprint arXiv:2511.09008.  Cited by: §4. 
  * [8] A. Beg, D. O’Donoghue, and R. Monahan (2025) Formalising software requirements with large language models.  In ADAPT Annual Conference,  Cited by: §4. 
  * [9] J. Cao, Y. Lu, M. Li, H. Ma, H. Li, M. He, C. Wen, L. Sun, H. Zhang, S. Qin, et al. (2025) From informal to formal–incorporating and evaluating llms on natural language requirements to verifiable formal proofs.  In Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers),  pp. 26984–27003.  Cited by: §4. 
  * [10] G. Chen, J. Wu, X. Chen, W. X. Zhao, R. Song, C. Li, K. Fan, D. Liu, and M. Liao (2025) ReForm: reflective autoformalization with prospective bounded sequence optimization.  arXiv preprint arXiv:2510.24592.  Cited by: §4. 
  * [11] L. De Moura and N. Bjørner (2008) Z3: an efficient smt solver.  In International conference on Tools and Algorithms for the Construction and Analysis of Systems,  pp. 337–340.  Cited by: §2.3. 
  * [12] A. O. Gomes and A. Butterfield (2016) Modelling the haemodialysis machine with circus.  In International Conference on Abstract State Machines, Alloy, B, TLA, VDM, and Z,  pp. 409–424.  Cited by: §4. 
  * [13] T. S. Hoang, C. Snook, L. Ladenberger, and M. Butler (2016) Validating the requirements and design of a hemodialysis machine using iuml-b, bmotion studio, and co-simulation.  In International Conference on Abstract State Machines, Alloy, B, TLA, VDM, and Z,  pp. 360–375.  Cited by: §4. 
  * [14] A. Q. Jiang, S. Welleck, J. P. Zhou, W. Li, J. Liu, M. Jamnik, T. Lacroix, Y. Wu, and G. Lample (2022) Draft, sketch, and prove: guiding formal theorem provers with informal proofs.  arXiv preprint arXiv:2210.12283.  Cited by: §4. 
  * [15] B. Kim, A. Ayoub, O. Sokolsky, I. Lee, P. Jones, Y. Zhang, and R. Jetley (2011) Safety-assured development of the gpca infusion pump software.  In Proceedings of the ninth ACM international conference on Embedded software,  pp. 155–164.  Cited by: §4. 
  * [16] Z. Li, Y. Wu, Z. Li, X. Wei, F. Yang, X. Zhang, and X. Ma (2024) Autoformalize mathematical statements by symbolic equivalence and semantic consistency.  Advances in Neural Information Processing Systems 37, pp. 53598–53625.  Cited by: §4. 
  * [17] Y. Liu, S. Yu, H. Jin, J. Wen, A. Qian, T. Lee, M. Ramsis, G. W. Choi, L. Qin, X. Liu, et al. (2026) A multi-agent framework combining large language models with medical flowcharts for self-triage.  Nature Health, pp. 1–10.  Cited by: §4. 
  * [18] S. Mandal, A. Chethan, V. Janfaza, S. Mahmud, T. A. Anderson, J. Turek, J. J. Tithi, and A. Muzahid (2023) Large language models based automatic synthesis of software specifications.  arXiv preprint arXiv:2304.09181.  Cited by: §4. 
  * [19] A. Mashkoor (2016) The hemodialysis machine case study.  In International Conference on Abstract State Machines, Alloy, B, TLA, VDM, and Z,  pp. 329–343.  Cited by: §2.3, §2.7, §4. 
  * [20] F. Mu, L. Shi, S. Wang, Z. Yu, B. Zhang, C. Wang, S. Liu, and Q. Wang (2024) Clarifygpt: a framework for enhancing llm-based code generation via requirements clarification.  Proceedings of the ACM on Software Engineering 1 (FSE), pp. 2332–2354.  Cited by: §4. 
  * [21] Ovasicek (2016) Open PCA pump requirements.  Note: <https://ovasicek.github.io/pca-pump-ec-artifacts/Open-PCA-Pump-Requirements.pdf>Accessed: 2026-05-07 Cited by: Appendix A. 
  * [22] M. Q. Riaz, W. H. Butt, and S. Rehman (2019) Automatic detection of ambiguous software requirements: an insight.  In 2019 5th International Conference on Information Management (ICIM),  pp. 1–6.  Cited by: §2.2. 
  * [23] C. Sun, Y. Sheng, O. Padon, and C. Barrett (2024) Clover: clo sed-loop ver ifiable code generation.  In International Symposium on AI Verification,  pp. 134–155.  Cited by: §4. 
  * [24] U.S. Food and Drug Administration (2026) MAUDE — manufacturer and user facility device experience.  Note: <https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/search.cfm> Cited by: §2.4. 
  * [25] W. Wang, M. Farrell, L. C. Cordeiro, and L. Zhao (2025) Supporting software formal verification with large language models: an experimental study.  In 2025 IEEE 33rd International Requirements Engineering Conference (RE),  pp. 423–431.  Cited by: §4. 
  * [26] J. J. Wu, M. Chaudhary, D. Abrahamyan, A. Khaku, A. Wei, and F. H. Fard (2025) Can code language models learn clarification-seeking behaviors?.  arXiv preprint arXiv:2504.16331.  Cited by: §4. 
  * [27] J. J. Wu and F. H. Fard (2025) Humanevalcomm: benchmarking the communication competence of code generation for llms and llm agents.  ACM Transactions on Software Engineering and Methodology 34 (7), pp. 1–42.  Cited by: §4. 
  * [28] Y. Wu, A. Q. Jiang, W. Li, M. Rabe, C. Staats, M. Jamnik, and C. Szegedy (2022) Autoformalization with large language models.  Advances in neural information processing systems 35, pp. 32353–32368.  Cited by: §1, §4. 
  * [29] K. Yang, A. Swope, A. Gu, R. Chalamala, P. Song, S. Yu, S. Godil, R. J. Prenger, and A. Anandkumar (2023) Leandojo: theorem proving with retrieval-augmented language models.  Advances in Neural Information Processing Systems 36, pp. 21573–21612.  Cited by: §4. 



## Appendix A Generalizability Check: PCA Pump Requirements

To assess whether the round-trip faithfulness evaluation generalizes beyond the hemodialysis benchmark, we applied the same evaluator to a second medical device domain: a PCA pump requirement set [21]. The setup mirrors Experiment 1, we used the same LLM and a similar repair budget of 5 iterations was applied to 144 PCA pump requirements formalized into a separate SMT model.

Table 2: Round-trip evaluation on the PCA pump requirement set. Formal equivalence is measured between the original SMT predicates and those obtained by reconstructing requirements from the model and re-formalizing. Metric | Value  
---|---  
Requirements reconstructed | 144 / 144  
Missing requirements | 0  
Mean cosine similarity | 0.8688  
Median cosine similarity | 0.8868  
90th percentile cosine similarity | 0.9688  
Initial formal equivalence | 135 / 144 (93.75%)  
Final formal equivalence after repair | 144 / 144 (100.0%)  
Non-equivalent requirements repaired | 9 / 9  
Repair attempts needed | 1  
  
Textual similarity was high overall: median cosine similarity 0.8868, 90th percentile 0.9688. The lowest-similarity cases were concentrated in standards, compliance, and security requirements, where reconstruction paraphrased the source text more aggressively. At the SMT level, 135 of 144 requirements were equivalent on the initial re-formalization pass; the bounded repair loop resolved all nine remaining mismatches in a single attempt. Common mismatch patterns included enum and value remapping errors in alarm and infusion-mode encodings, dropped else branches in conditional behavior, omitted structural constraints from table-driven requirements, and symbolic-versus-literal substitutions in alarm-table ranges.

These results mirror the HD round-trip findings: textual reconstruction may paraphrase the original requirement, yet the SMT-level check can still recover the original formal semantics. After bounded repair, every reconstructed PCA requirement formalized back to a predicate equivalent to the original in the generated model. This provides evidence that the round-trip evaluator is not specific to the HD benchmark and can serve as an internal consistency check for autoformalized requirement models across medical-device domains.

## Appendix B Redundancy Analysis

Table 3: The two requirements flagged as redundant by VeriMed’s audit (r11r_{11}, r56r_{56}), shown alongside the surrounding requirements that subsume them (r55r_{55}, r42r_{42}). Each subsuming requirement appears in the unsat core of the corresponding redundancy check. ID |  Requirement  
---|---  
r11r_{11} |  During initiation, if the pressure at the VP transducer falls below the lower pressure limit, the software shall stop the BP and execute an alarm signal.  
r55r_{55} |  The minimum distance between the venous lower pressure limit and the actual VP is always at least 22.5 mmHg.  
r56r_{56} |  Bypass mode occurs when the DF conductivity goes beyond permissible limits; the dialyzer is separated from the DF flow.  
r42r_{42} |  The DF conductivity parameter must be within 12.5 to 16.0 mS/cm.  
Table 4: Experimental setup summary. All SMT queries use Z3.

Exp | Task | NN | Model | Temp | Iter. / Samples  
---|---|---|---|---|---  
Exp1 | Formalization audit | 64 | Sonnet 4.6 | default | 5 repairs  
Exp2 | Question answering & repair | 65 | Sonnet 4.6 / Haiku 4.5† | 0 | 5 iterations  
Exp3 | End-to-end fault detection | 64 | Sonnet 4.6 | default | 6 repairs  
Exp4 | Ambiguity detection | 64 | Sonnet 4.6 | 1.0/ 0.2‡1.0\,/\,0.2^{\ddagger} | N=5N{=}5 samples  
  
† Haiku 4.5 (temp. 0) for answer-to-schema translation; Sonnet 4.6 for generation and repair.   
‡ Temp. 1.0 for repeated formalization; 0.2 for SMT-guided clarification.

## Appendix C Tables

Table 5: Original and clarified natural-language requirements for the 12 requirements whose repeated formalizations were ambiguity-sensitive before SMT-guided clarification. Req. | Before | Final | Δ\Delta |  Original requirement |  Clarified requirement  
---|---|---|---|---|---  
r3 | 14 | 1 | -13 |  To prevent coagulation of blood, the anti-coagulation pump doses anti-coagulant into the bloodline between the BP and the dialyzer at the set rate or set volume during treatment. |  To prevent coagulation of blood, the anti-coagulation pump doses anti-coagulant into the bloodline between the BP and the dialyzer at exactly the set rate during treatment, while the patient is connected and anti-coagulant delivery is active and not stopped.  
r56 | 6 | 1 | -5 |  Bypass mode occurs when the DF conductivity goes beyond permissible limits; the dialyzer is separated from the DF flow. |  Whenever the DF conductivity goes outside permissible limits (below 12.5 mS/cm or above 16.0 mS/cm), both of the following consequences must hold simultaneously: (1) bypass mode becomes active, and (2) the dialyzer is disconnected from the DF fl
