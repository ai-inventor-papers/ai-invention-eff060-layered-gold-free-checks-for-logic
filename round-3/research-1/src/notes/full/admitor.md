URL: https://arxiv.org/html/2608.15565 | FULL FETCH | 2026-09-24T01:49:03Z
warning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
URL: https://arxiv.org/html/2608.15565
Type: HTML
Length: 98331 chars (truncated)

--- Content ---

##### Report GitHub Issue

×

Title:

Content selection saved. Describe the issue below:

Description:

Submit without GitHub Submit in GitHub

arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[ Back to arXiv ](/)

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) Report Issue [ Back to Abstract ](/abs/2608.15565v4 "Back to abstract page") [ Download PDF](/pdf/2608.15565v4 "Download PDF") [ ](javascript:toggleNavTOC\(\); "Toggle navigation") [ ](javascript:toggleReadingMode\(\); "Disable reading mode, show header and footer")

  1. Abstract
  2. 1 Introduction
     1. Contributions.
  3. 2 Related Work
     1. Experience learning with labeled admission.
     2. Self-verification and its limits.
     3. Consensus, voting, and juries.
     4. Benchmark reliability.
     5. Verifiers for optimization modeling.
     6. Conformal selection.
  4. 3 The AdmitOR Gate
     1. Setup.
     2. Step 1: generate a decorrelated panel.
     3. Step 2: extract a base-anchored domain and resample.
     4. Step 3: compare value-function traces.
     5. Step 4: calibrate the admission threshold.
     6. Step 5: certified distillation.
  5. 4 Experiments
     1. Setup and pins.
     2. 4.1 Host reproduction and the measuring stick
     3. 4.2 The judge swap
        1. What produced the gain.
        2. The family-by-outcome matrix (K4).
     4. 4.3 Calibrated admission: the criterion that fails
  6. 5 Limitations
  7. 6 Conclusion
  8. References
  9. A Proofs
     1. A.1 Identifiability by resampling
        1. Assumptions.
        2. Remarks.
     2. A.2 Policy-matched calibration
        1. Setup.
        2. Remark.
  10. B Protocol registration and scoring
     1. Extraction guardrails.
     2. Model and solver pins.
     3. Preregistered decision criteria.
     4. Certification pseudocode.
     5. Scoring rule.
     6. Candidate-generation rules.
     7. Candidate-generation prompt (verbatim).
     8. Extraction prompt (verbatim).
     9. A certified skill (excerpt).
     10. B.1 The data-layer stage
  11. C Host reproduction details and supplementary tables
     1. The comparison against the ground-truth arm.
     2. Bootstrap and library-size bookkeeping.
     3. The ComplexOR label error at evaluation.
     4. Calibration-set counts.
     5. Decomposition of the uninformative verdicts.
     6. The audit protocol and its packets.
     7. Certification cost budget.
     8. The threshold sweep and the confidence bookkeeping.
     9. Reading the family-by-outcome matrix.
     10. Stream provenance and disjointness.
     11. Judge ablation details.
     12. The OptiBench selection anomaly.
     13. Case study: a label convicts the innocent.
     14. Annotations.



[ License: CC BY-NC-SA 4.0 ](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2608.15565v4 [cs.AI] 16 Sep 2026

# Admission Without Answers: Label-Free   
Certification and Experience Learning for   
LLM-Based Optimization Modeling

Junbo Jacob Lian  Affiliation: Institute of Operations Research and Analytics  Affiliation: National University of Singapore, Singapore  Affiliation: Wenzhou Buyi Pharmacy, Wenzhou, China  Email: [jacoblian@u.northwestern.edu](mailto:) Huiling Chen  Affiliation: College of Computer Science and Artificial Intelligence  Affiliation: Wenzhou University, Wenzhou, China  Email: [chenhuiling.jlu@gmail.com](mailto:) Hanzhang Qin  Affiliation: Institute of Operations Research and Analytics  Affiliation: National University of Singapore, Singapore  Email: [hzqin@nus.edu.sg](mailto:) Chung-Piaw Teo  Affiliation: Institute of Operations Research and Analytics  Affiliation: National University of Singapore, Singapore  Email: [bizteocp@nus.edu.sg](mailto:)

###### Abstract

Agents that learn from experience improve at optimization modeling by storing solved trajectories and reusing them as skills. A wrong trajectory that enters the library can be retrieved again and again, and on a stream of new problems there is no ground-truth answer to decide with. Existing learners admit trajectories by matching known optima or labels, and label-free substitutes such as execution success or agreement at one instance can admit wrong models. We introduce AdmitOR, a label-free admission gate. It generates models from three model families, runs each on the stated problem and on instances with resampled parameters, keeps the largest group of models whose optimal values agree on every instance across families, and applies a threshold fitted on solver-verified problems to accept, abstain, or escalate, with a finite-sample bound on the false-discovery rate among accepted values. Inside a state-of-the-art skill learner, AdmitOR raises candidate-level admission precision to 0.927, against 0.871 for majority vote over the host’s own samples and 0.726 for execution success, and its library, the smallest of the four, reaches the highest macro accuracy over five public benchmarks, 58.4 against 54.8 for majority vote. An ablation on the same records shows that the gain comes from the accepted value being external to the learner and unanimous across families; on this stream, resampling never changed an accepted value and only reduced coverage. The false-discovery bound holds on the calibration set but not on the benchmark stream: an audit of every false certificate traces most of them to benchmark texts that omit or round the numbers needed to reproduce the labeled answer, and a label-free check of the extracted numbers against the text flags most of these cases. Code and data are available at <https://github.com/junbolian/AdmitOR>  
  
---  
  
## 1 Introduction

Large language models can translate natural-language descriptions of operational problems into executable optimization models, and recent agents improve further by learning from experience: solved trajectories are distilled into reusable insights, skills, or exemplars (Kong et al., 2025; Yang et al., 2026; Liang et al., 2026). Once stored, however, a wrong trajectory is no longer a single wrong answer: it can be retrieved repeatedly and affect many later decisions. Existing learners avoid this risk by admitting only trajectories that match known optima (Kong et al., 2025), are labeled against ground truth (Yang et al., 2026), or are curated by experts (Liang et al., 2026). A stream of real problems provides no such answers, and we refer to this lack of reliable answers as the label wall.

The natural label-free substitutes are unsafe. Execution success shows only that a program runs, not that it encodes the right objective, constraints, and data. Self-assessment is unreliable: models miss their own errors and prefer their own outputs (Huang et al., 2024a; Gou et al., 2024; Kamoi et al., 2024; Panickssery et al., 2024), and at the system level Xiu et al. (2026) admit memories by self-assessment and execution success and report that naive retrieval from the resulting store can reduce accuracy. On our 300-problem stream, an execution-only rule admits 878 candidate models, 241 of which disagree with the withheld answers. A useful admission rule therefore has to test how a model behaves, not whether it runs or how confident it reports itself to be.

Behavior at one instance is not enough either. Consider allocating up to 150 crates across three stores with capacities of 60, unit profits of 8, 6, and 4, and a contractual floor of 20 crates per store. At the stated instance the floor is inactive: the correct model and a model that omits the floor both ship 60, 60, and 30 crates and both return 960. Comparing final objective values, whether by majority vote or against an answer key, cannot distinguish the two formulations here; their agreement is accidental and breaks once the parameters change. On a resampled instance where the third store’s unit profit is negative, the floor becomes binding: the correct model still ships 20 crates to that store, the other model ships none, and the two optimal values differ (Figure 1a). The evidence we need is therefore about how a model’s optimal value changes with the parameters, not about one answer.

AdmitOR (read _admitter_) builds its decision on this kind of evidence. It generates candidate models from three model families with different prompting strategies and solver stacks and runs every candidate on the stated problem and on instances resampled from a parameter domain anchored at the stated values. Candidates that describe the same problem should return the same optimal value on every instance; because not every candidate is expected to agree, the gate keeps the largest group whose values agree on every instance and requires that group to span more than one family. Proposition 1 shows that two models with different value functions differ on a region of positive measure, so independent resampling misses that region with probability that decreases geometrically in the number of usable instances. A threshold fitted on solver-verified problems then turns the strength of the agreement into accept, abstain, or escalate, with the false-discovery rate (FDR) among accepted values as the quantity under control. Only accepted values are used for learning.

We evaluate the gate inside a running skill learner (Yang et al., 2026) with a collect-once, replay-many protocol: candidate models and solver logs are generated once on a 300-problem stream whose labels are withheld, and four judges replay the same records to build separate libraries, using sealed ground truth, majority vote over the host’s own sampled trajectories, execution success, or AdmitOR. Candidate-level admission precision rises from 0.726 for execution success to 0.871 for majority vote and 0.927 for AdmitOR, and the AdmitOR library is the smallest and reaches the highest macro accuracy across five public benchmarks. Two further analyses use the same records: an ablation over intermediate judges shows which part of the gate produced the gain, and the preregistered false-discovery criterion, which holds on solver-verified data, fails on the benchmark stream for a reason that an audit of every false certificate finds in the benchmark texts themselves. The paper thus reports where the method performs well, which of its parts did the work, and where its assumptions fail.

Figure 1: (a) Why one-point agreement is insufficient. A model omitting the floor constraint returns 960 at the stated instance, exactly as the correct models do, but its optimal value separates on resampled instances, and the cross-family agreement excludes it. (b) Candidate-level admission precision of three label-free judges on the same 300-problem stream, with poisoned-admission counts.

#### Contributions.

(i) Problem. Admission into a persistent library is the step that current experience learners leave to ground-truth labels. We argue that the right safety target for this step is the false-discovery rate among admitted items, not certainty about each one. (ii) Method. We design an admission procedure that compares independently generated models from several model families and tests whether their optimal values stay consistent under parameter changes, with an identifiability result and a finite-sample calibration whose transfer assumption is stated explicitly. (iii) Protocol. A collect-once, replay-many design holds candidate generations and solver logs fixed while changing only the judge, so that judges are compared on identical inputs. (iv) Evidence. AdmitOR produces 8×\times fewer poisoned admissions than execution success and reaches the highest downstream accuracy with the fewest library items, with a paired-bootstrap gain over majority vote; an ablation on the same records attributes the gain to an external, unanimous certificate and shows that resampling changed no accepted value on this stream. (v) Measurement. Auditing every false certificate shows that many failures come from missing or rounded numbers in the benchmark text rather than from the generated models: at least 10.9%10.9\% of admitted problems cannot be answered from the printed text alone, and a check of the extracted numbers against the text flags most of these cases without labels. Code, verdicts, run ledger, and complete case packets are released.

## 2 Related Work

#### Experience learning with labeled admission.

The systems closest to our setting learn reusable knowledge from solved problems, but all rely on answers for admission: insight libraries matched against known optima (Kong et al., 2025), skills distilled from ground-truth-labeled trajectories (Yang et al., 2026), and expert exemplar banks (Liang et al., 2026). AdmitOR replaces this supervision signal; we evaluate it inside one of these systems with the native ground-truth oracle as the reference (Section 4.2).

#### Self-verification and its limits.

Intrinsic self-correction can degrade reasoning (Huang et al., 2024a), effective critique requires external tools (Gou et al., 2024), and models miss their own errors (Kamoi et al., 2024) while favoring their own outputs (Panickssery et al., 2024); Xiu et al. (2026) show the failure at the system level. Li and Hai (2026) prove that no sound and nontrivial fixed-threshold perturbation tester exists; they establish sound tests for individual models, whereas we calibrate admission across several models.

#### Consensus, voting, and juries.

Self-consistency and its variants select the answer that recurs most often across sampled reasoning paths (Wang et al., 2023; Chen et al., 2023; Aggarwal et al., 2023). These methods, like jury-style aggregation (Liu, 2026), annotation-free routing (Niu et al., 2026; Guha et al., 2024), and cross-backbone debate (Lin et al., 2026), aggregate agreement at a single problem instance, and they select an answer rather than bound the error rate of what is accepted. Our majority-vote arm is self-consistency as the host runs it: the modal answer of the three trajectories the host samples for a problem, all from one backbone (Section 4.2). AdmitOR differs in both: agreement is measured over optimal values on resampled instances, and the output is an admission decision with a calibrated error budget. The shared-error floor of Liu (2026) motivates the use of several model families, and Zhou (2026) identifies the failure it protects against: a judge conditioned on a shown candidate scores plausibility rather than correctness, and a strict three-judge ensemble still admits 55%55\% of the resulting false positives unless each judge first commits an answer of its own. Every family in our panel commits its own executed answer before any comparison; the extractor is the one shared stage (Section 4.3).

#### Benchmark reliability.

The benchmarks used here (Xiao et al., 2024; Tang et al., 2024; Huang et al., 2024b; Lu et al., 2025; Yang et al., 2024) are known to contain errors. An expert audit with each case cross-validated by at least three reviewers reports rates of at least 54.0%54.0\% on IndustryOR, 24.3%24.3\% on ComplexOR and 23.7%23.7\% on Mamo ComplexLP, attributes them to inconsistent statements, underdetermined parameters and incorrect answers, and releases cleaned versions (Xiao et al., 2025). Those audits review datasets by hand; Section 4.3 reaches the same object from the other direction: the disagreements of a label-free judge locate one specific error, a printed text from which the reference answer cannot be recovered, and quantify it as a floor on the false-discovery rate that any text-faithful certifier can reach.

#### Verifiers for optimization modeling.

Modeling agents such as OptiMUS (AhmadiTeshnizi et al., 2024) check their own formulations by re-solving; recent verifiers, semantic checkers, and behavioral test batteries (Liu et al., 2026; Rahman et al., 2026; Zhang et al., 2025; Li et al., 2026; Lian et al., 2026) filter individual generations, and the test batteries of Lian et al. (2026) and Li and Hai (2026) perturb the instance of a single model and check its response. These methods verify or select single outputs without deciding admission into a persistent library or bounding the false-discovery rate of what is admitted, so Table 1 lists single-model perturbation testing as its own row.

#### Conformal selection.

Our admission layer is finite-sample calibrated selection toward an FDR target, with split-conformal Benjamini–Hochberg (Jin and Candès, 2023) as its large-sample version, applied to a new score, cross-family agreement over resampled optimal values, and combined with policy-matched calibration because escalation makes admission adaptive (Lemma 1). Table 1 summarizes four properties of an admission judge; to our knowledge, AdmitOR is the first label-free method designed for all four, and Section 4.3 shows where the calibrated budget stops transferring.

Table 1: Properties targeted by each admission judge. _Executed value_ : compares executed objective values rather than run status, text, or self-report. _Beyond one point_ : the comparison spans resampled instances. _Budget_ : targets a calibrated false-discovery rate. Judge | Label-free | Executed value | Beyond one point | Budget  
---|---|---|---|---  
Ground-truth labels | ×\times | ✓\checkmark | ×\times | ×\times  
Execution success | ✓\checkmark | ×\times | ×\times | ×\times  
Majority vote | ✓\checkmark | ✓\checkmark | ×\times | ×\times  
Single-model perturbation test | ✓\checkmark | ✓\checkmark | ✓\checkmark | ×\times  
AdmitOR | ✓\checkmark | ✓\checkmark | ✓\checkmark | ✓\checkmark  
  
## 3 The AdmitOR Gate

Figure 2: The AdmitOR gate. Candidates from three model families are run on instances resampled from a domain anchored at the stated problem, the largest group of candidates whose optimal values agree on every instance across families is found, and a calibrated threshold turns that agreement into a three-state decision toward α=5%\alpha=5\% with a controlled budget of 2​α2\alpha (Proposition 2). Accepted values relabel the host’s trajectories, which are then distilled into the library.

#### Setup.

The idea is that two models of the same problem should return the same optimal value whenever the parameters change. A _ticket_ is a natural-language optimization problem xx with stated parameter values θ0\theta_{0} and a perturbation domain Θ\Theta anchored at θ0\theta_{0}. A candidate MM is an executable program that builds and solves a model for any θ∈Θ\theta\in\Theta; its optimal objective defines the _value function_ VM​(θ)V_{M}(\theta). Two candidates are behaviorally equivalent when their value functions agree on Θ\Theta, whatever their code. The gate receives a panel 𝒞={M1,…,Mk}\mathcal{C}=\\{M_{1},\dots,M_{k}\\} with family labels f⁡(Mi)f(M_{i}) and returns accept with an accepted value z^=V⁡(θ0)\hat{z}=V(\theta_{0}), abstain, or escalate. We call an accept that carries a value at θ0\theta_{0} a _certificate_ ; the word refers to the agreement that supports the value, not to a proof of correctness. An accept whose agreeing group formed only on resampled instances certifies nothing and admits nothing. Insufficient comparable evidence is logged as uninformative and maps to escalation in deployment. Section 4.2 evaluates admitted candidate models; Section 4.3 evaluates problem-level certificates, the units of the FDR target. Figure 2 and Algorithm 1 (Appendix B) summarize the five steps.

#### Step 1: generate a decorrelated panel.

We generate candidates from three model families under different prompting strategies and solver stacks, each on a separate backend. Every consensus method has a shared-error floor, the probability that all panel members make the _same_ mistake, and the floor is higher within one family because related models share training data and failure modes (Liu, 2026). Diversity across families and solver APIs lowers several sources of correlated failure but cannot detect a misinterpretation of the input text shared by all of them (Section 5).

#### Step 2: extract a base-anchored domain and resample.

An extractor LLM reads xx and returns the stated base value and a relative or absolute perturbation domain for each parameter. The domain is anchored so that instance 00 is exactly the stated problem, and guardrails keep structural size parameters fixed so that resampled instances preserve their dimensions (Appendix B). The pilot runs a single extractor; Appendix B.1 specifies the check on the extracted numbers that Section 4.3 motivates. The harness then draws θ1,…,θm\theta_{1},\dots,\theta_{m} independently from the domain and runs every candidate on every instance, recording the objective value and solver status of each run. An instance is _informative_ when at least two candidates return a finite value; infeasible and failed runs make an instance uninformative, and the gate requires at least three informative instances before issuing a verdict.

#### Step 3: compare value-function traces.

Two candidates agree on an instance when their objective values aa and bb satisfy |a−b|≤10−4​max⁡(1,|a|,|b|)|a-b|\leq 10^{-4}\max(1,|a|,|b|), and they are consistent when they agree on every informative instance, including the stated one. Pairwise consistency defines a graph over 𝒞\mathcal{C}, and the gate takes a maximum clique of that graph, the largest group of candidates that are all consistent with one another. If the clique spans at least two model families, the gate returns accept with the common value at θ0\theta_{0}; otherwise it returns abstain. With one candidate per family, as in the pilot, clique size and family coverage coincide. Each candidate outside the clique is rejected with a diagnosis naming a resampled instance on which it differs, which localizes the modeling disagreement: in the crate example, a negative unit profit activates the omitted floor constraint. Proposition 1 states when random perturbations detect such a difference.

###### Proposition 1.

For linear and mixed-integer models over a full-dimensional perturbation domain, the candidate value functions are piecewise polynomial in θ\theta, and affine when only right-hand sides or only costs vary. If two candidates are not equivalent on the domain, the disagreement region contains an open set. Under continuous resampling, the probability that mm independent instances all miss this region decreases geometrically with mm, at a rate set by the probability measure of the disagreement region. With an agreement tolerance ε\varepsilon, the same bound holds for the region where the two value functions differ by more than ε\varepsilon whenever that region has positive measure; a modeling error whose effect on the optimal value stays within ε\varepsilon over the whole domain is not detectable by resampling. A formal statement, the proof, and the scope of the result for integer-valued parameters appear in Appendix A.

#### Step 4: calibrate the admission threshold.

Agreement is evidence rather than proof, so its strength is calibrated rather than thresholded by hand. The deployed score orders the number of families in the clique first, then the clique size, then the number of informative instances, encoded as the scalar 10⋅(families)+|Q|+(informative)/1010\cdot(\text{families})+|Q|+(\text{informative})/10 (Algorithm 1). It takes finitely many values, four of which occur in the pilot; pairwise agreement margins are recorded but do not enter the score. We fit the acceptance threshold τ\tau on problems whose ground truth is verified _by construction_ : the unchanged gate runs on a stratified sample of solver-verified synthetic instances, so every accepted certificate can be labeled true or false without benchmark data. A fixed threshold is not a valid substitute, because no sound and nontrivial fixed-threshold perturbation tester exists (Li and Hai, 2026), and the following pair licenses the selection.

###### Assumption 1 (Transfer).

(i) _Faithful encoding_ : the problem text determines the labeled instance, so the extracted base specification identifies it up to scoring tolerance. (ii) _Certificate exchangeability_ : accepted deployment certificates with score at least τ\tau are exchangeable with calibration certificates at the same score with respect to the true/false label.

###### Proposition 2 (Calibrated admission).

Let TT be the attainable score grid (|T|=4|T|=4 in the pilot), pτp_{\tau} the false-certificate probability among accepted certificates with score at least τ\tau, and UτU_{\tau} the level-(1−δ)(1{-}\delta) Clopper–Pearson upper bound from the calibration counts. The fit selects τ∗=min{τ∈T:p^τ≤α,Uτ≤2α}\tau^{\ast}=\min\\{\tau\in T:\hat{p}_{\tau}\leq\alpha,\ U_{\tau}\leq 2\alpha\\}. Then (i) for each fixed τ\tau, Pr⁡(pτ≤Uτ)≥1−δ\Pr(p_{\tau}\leq U_{\tau})\geq 1-\delta exactly; (ii) over the data-dependent selection, pτ∗≤2​αp_{\tau^{\ast}}\leq 2\alpha holds simultaneously with probability at least 1−|T|​δ1-|T|\delta; (iii) under Assumption 1, the same bounds apply to the false-certification rate among deployment admissions at τ∗\tau^{\ast}; and (iv) as the calibration null count grows, Benjamini–Hochberg over split-conformal p-values replaces the grid bound and controls the false-discovery rate, the expectation of the false-discovery proportion, at level α\alpha in finite samples under clause (ii) alone (Jin and Candès, 2023). Proof in Appendix A.

Throughout, α=5%\alpha=5\% is the nominal selection target applied to p^τ\hat{p}_{\tau} and 2​α=10%2\alpha=10\% is the finite-sample _controlled_ budget; the two figures should not be confused. The pilot uses δ=0.05\delta=0.05 per threshold and also reports the 95%95\%-simultaneous choice δ=0.0125\delta=0.0125 (Table 8). The judge swap of Section 4.2 ran with the admission rule of Step 3; the threshold was fitted afterwards on the calibration set and applied to the same stored verdicts in Section 4.3, which also measures how far Assumption 1 is violated on the benchmark stream. Deployment adds one requirement:

###### Lemma 1 (Policy-matched calibration, informal).

If admission is adaptive, borderline cases enter an escalation ladder that adds instances or candidates before a new decision. The guarantee then holds only when calibration uses the same ladder policy as deployment; calibration on single-pass decisions does not remain valid under escalated deployment (formal statement and proof in Appendix A).

#### Step 5: certified distillation.

Only certificates contribute to learning. The host’s own trajectories for the problem are relabeled with the accepted value: a trajectory whose answer matches it is admitted and passed to the unmodified distillation procedure of the host, with the accepted value in place of the missing answer; the panel candidates themselves are not stored. Admission is therefore a value test against an external certificate, and Section 4.2 measures what follows from this choice.

## 4 Experiments

#### Setup and pins.

The host experience learner (Yang et al., 2026) runs the released pipeline with a single fixed backbone. The panel of the gate uses the three model families of Section 3, one candidate per family, with prompting strategies and solver stacks divided across them; the extractor is the first family’s backbone. Each certification includes the mandatory stated instance and m=5m=5 resampled instances drawn under a fixed seed. The 300-problem stream consists of the first 300 problems, by index, of the training split of OptMATH (Lu et al., 2025), with labels withheld from every judge except the ground-truth reference; it shares no item with the 1,100 evaluation items at the exact, normalized, or near-duplicate level (Appendix C). Every remaining configuration choice is pinned in the release(Appendix B).

### 4.1 Host reproduction and the measuring stick

Before replacing the admission judge, we reproduce the complete host on five public benchmarks (Xiao et al., 2024; Tang et al., 2024; Huang et al., 2024b; Lu et al., 2025; Yang et al., 2024) using the released skill library and a uniform scorer, because the repository provides no scoring code. Appendices B and C give the scoring rule and per-benchmark differences. The reproduced macro accuracy is within 2.62.6 points of the reported result, with two findings that shape what follows. First, the evaluation labels are imperfect: on ComplexOR our pipeline is penalized for a correct answer, and correcting that single label recovers the reported score exactly (Appendix C). The protocol was fixed before any judge was evaluated, so the main results retain the published labels, and label errors count against every method, including AdmitOR. Second, the OptMATH reproduction has a known deficit of 33 to 55 points, attributed by partial reruns to solver contention and a capability gap (Appendix C); we base no central claim on its absolute scores.

### 4.2 The judge swap

For the 300-problem stream, we collect candidate generations and solver logs once. Four judges then replay the same logs, assign labels, and pass their admitted trajectories to the unmodified distillation procedure of the host: sealed ground truth, majority vote over the three trajectories the host samples per problem, execution success, and AdmitOR. Certification returns 174 accept, 114 uninformative, 10 abstain, and 2 error outcomes, the errors from truncated extractor output. abstain indicates value-level disagreement; none of the 114 uninformative cases arises from conflicting evidence, most being due to infeasible resampled instances and to candidates that never return a value (Appendix C). Figure 1b reports admission precision against the sealed vault over admitted _candidate models_ , the units on which each judge acts: 878 candidates for execution success, 721 for majority vote, and 413 for AdmitOR, whose admission recall, the proportion of correct executable candidates recovered, is 0.6010.601 against 1.01.0 by construction for execution success. The AdmitOR library was built with the admission rule of Step 3; the calibrated threshold of Section 4.3, applied to the same admissions, would remove 27 problems and 69 candidates, 8 of the 30 poisoned ones, for a precision of 0.9360.936. Library sizes fall from 163 files for execution success to 101 for AdmitOR (Appendix C).

Table 2: Downstream accuracy (%, round-aware scorer) of the host with the library produced by each judge; every arm replays the same collection logs. _Macro_ averages the five benchmarks equally, _Micro_ weights by item over all 1100 items; Mamo.C is Mamo ComplexLP. Bold marks the best result in each column. Judge | ComplexOR | IndustryOR | Mamo.C | OptMATH | OptiBench | Macro | Micro  
---|---|---|---|---|---|---|---  
Ground truth | 66.67 | 31.00 | 52.61 | 56.02 | 63.14 | 53.89 | 57.18  
Execution success | 66.67 | 35.00 | 53.08 | 55.42 | 72.40 | 56.51 | 62.64  
Majority vote | 61.11 | 33.00 | 53.55 | 54.22 | 72.23 | 54.82 | 62.18  
AdmitOR | 66.67 | 39.00 | 57.82 | 56.02 | 72.23 | 58.35 | 63.91  
  
Table 2 answers the judge-swap question. The clean comparison is among label-free judges on the same candidates: AdmitOR matches or exceeds majority vote on all five benchmarks and adds 3.53.5 macro points while using the smallest library. The ground-truth arm is not an upper bound, because its downstream result also depends on retrieval and skill selection. Intervals come from a paired stratified bootstrap on the macro scale (Appendix C). Against majority vote the gain is +3.53+3.53 points, with a 95% interval of [+0.87,+6.68][+0.87,+6.68]; repeating the comparison on the item set defined by the sensitivity analysis below leaves it at +3.49+3.49, [+0.78,+6.73][+0.78,+6.73], so the preregistered criterion K2 is met on both bases. Against execution success the macro gain of +1.84+1.84 has interval [−0.27,+3.96][-0.27,+3.96] and does not exclude zero, and three of the five benchmarks are at or near parity; what we claim over execution success is therefore equal accuracy with roughly one-third fewer items and an audit trail, not higher accuracy.

Two qualifications are necessary. First, on OptiBench the ground-truth arm fails at _skill selection_ rather than modeling on 85 of 605 items; the protocol counts these as errors in every arm, and excluding them raises ground-truth macro accuracy to 55.9555.95, still below AdmitOR, with the corrected intervals above using that item set (Appendix C). Second, downstream accuracy also depends on retrieval: on OptiBench, which holds 55% of the items, the label-free arms differ by 0.20.2 points while their libraries differ by 62 files, and the host selects from 19 distinct files in the AdmitOR arm against 30 for execution success, one file receiving 45%45\% of the AdmitOR selections (Appendix C). Library size is therefore not what separates the arms there; the differences arise on IndustryOR and Mamo ComplexLP.

Table 3: Judge ablation on the stored records, without new model calls. Certificates are problems with an accepted value, scored round-aware against the vault; admitted candidates are host trajectories matching the accepted value, scored under the host’s equality rule, with recall over the 637 vault-correct trajectories. Panel judges use the three family candidates at the stated instance only. Judge | Certificates | Wrong | Admitted | Poisoned | Precision | Recall  
---|---|---|---|---|---|---  
Execution success | – | – | 878 | 241 | 0.726 | 1.000  
Majority vote over host samples | 254 | 38 | 721 | 93 | 0.871 | 0.986  
Panel: any two families agree at θ0\theta_{0} | 245 | 38 | 610 | 45 | 0.926 | 0.887  
Panel: all three families agree at θ0\theta_{0} | 200 | 26 | 516 | 32 | 0.938 | 0.760  
AdmitOR, admission rule of Step 3 | 170 | 29 | 413 | 30 | 0.927 | 0.601  
AdmitOR, calibrated τ\tau | 138 | 22 | 344 | 22 | 0.936 | 0.505  
  
#### What produced the gain.

The judge swap shows that the gate improves on majority vote, but not which of its parts is responsible. Three further judges that separate the parts are computable from the stored verdicts: agreement of any two panel families at the stated instance, unanimity of all three at the stated instance, and the calibrated rule of Section 4.3. Table 3 reports all six judges on the same records, and two facts follow. First, the gain over majority vote comes from the accepted value being external to the learner: panel unanimity at the stated instance alone reaches precision 0.9380.938. The host’s own modal answer admits at least two trajectories whenever it is wrong, whereas an external value admits a wrong trajectory only when host and panel err on the same value; the 30 poisoned admissions of the deployed arm arise on only 15 problems. Second, resampling changed no accepted value. The calibrated gate admits a strict subset of the problems on which the panel is unanimous at the stated instance, with the same accepted value on all 138, and the 62 problems it withholds carry 4 wrong values and 58 correct ones: 57 are withheld for want of three informative instances, four because a candidate failed on perturbed instances, and one because the values diverged, with a correct stated-instance value in all five. Under the pilot’s admission rule this is the expected shape. A model whose omitted constraint is inactive at the stated instance returns the correct value there, so admission by value cannot register the model-level detections that resampling provides, and the judge swap measures the gate as a label-free value certifier. The lost coverage comes from the extracted domains, not from unlucky draws: 27%27\% of all resampled candidate-instance pairs are infeasible, and re-drawing the 57 withheld problems with solvability screening recovers 8, each with the same accepted value (Appendix C).

#### The family-by-outcome matrix (K4).

The remaining preregistered check concerns the panel itself: if the three arms failed in the same way, several families would add little over one. Their failure profiles differ (χ2=30.96\chi^{2}=30.96, df=8\mathrm{df}=8, p=1.4×10−4p=1.4\times 10^{-4}), and the difference survives restriction to candidates that reached value comparison (χ2=8.75\chi^{2}=8.75, df=2\mathrm{df}=2, p=0.013p=0.013), although execution failures, which track the solver stack, carry most of the full statistic. The matrix and the limits of its reading appear in Appendix C.

### 4.3 Calibrated admission: the criterion that fails

We fit the calibrated admission layer as Section 3 specifies: the unchanged gate runs on a stratified sample of 150 solver-verified NANO-CO instances (Yang et al., 2026) under the single-pass policy that deployment uses, so the requirement of Lemma 1 is met by construction. The gate returns 103 accepts, 64 of them three-family cliques. The deployed score takes only two bands, 22.x22.x for two-family and 33.x33.x for three-family cliques, so the selected τ=33.3\tau=33.3 means exactly that all three families agree and at least three instances are informative, and the four attainable thresholds differ only in the informative count. Among the 63 value-bearing three-family certificates one is false: p^=1.6%\hat{p}=1.6\%, with upper bound 7.3%7.3\% at δ=0.05\delta=0.05 and 9.7%9.7\% at δ=0.0125\delta=0.0125, the 95%95\%-simultaneous choice over the grid, so the rule of Proposition 2 holds under both choices and τ=33.3\tau=33.3 is its minimum (Table 8). Replaying this rule on the 170 value-bearing verdicts of Section 4.2 admits 138 cases, which we score out of sample against the sealed vault.

The preregistered criterion fails, and we report it without modification (Table 8 and Appendix C). Under the uniform scorer, 22 of 138 admitted certificates disagree with the sealed vault, a realized proportion of 15.9%15.9\% with a 95% upper bound of 22.0%22.0\%; the host’s stricter equality rule finds 26, and the two sets overlap in 21 cases. The realized proportion exceeds the 5%5\% target and its upper bound exceeds the 2​α=10%2\alpha=10\% budget, so the criterion fails under both readings. Tightening as the protocol permits does not recover the target: across the four thresholds the realized proportion stays between 14.7%14.7\% and 16.5%16.5\%, and sixteen of the twenty-two carry _full_ evidence, all three families agreeing on every sampled instance, so no threshold on the amount of agreement separates them (Figure 4a in Appendix C). More resampling from the same specification cannot show whether that specification represents the source data, and the audit below locates the defect there.

We audit all twenty-two under a protocol that assumes neither value correct and requires every verdict to cite the text against a code line or an explicit derivation (Appendix C); the audit is the authors’ own, and the released packets and per-case attribution file allow re-audit. It changes our initial taxonomy (Table 6 and Figure 4b). We expected gate defects, in which the agreeing models omitted a stated constraint, and legitimate alternative readings of ambiguous text; the audit finds no case in either category. Two cases are label errors, both re-derived independently of the gate, and in both the published label is _below_ the true minimum of the stated minimization problem and cannot be attained by any feasible solution.

The remaining twenty cases share a root cause that was not preregistered: _the problem text is not a faithful encoding of the labeled instance_. In fifteen cases, the printed text omits decisive data, typically a cost or demand matrix. In five cases, parameters are printed at insufficient precision, so the optimum of the stated text differs from the label by more than the scoring tolerance. One case is diagnosable from the sign of the objective alone: the accepted value is _negative_ , which is impossible under any nonnegative cost matrix, so the extractor must have supplied entries that the text never printed, while the magnitude of the label is consistent with a real instance of the stated form (Appendix C). We call this category (d): the text does not determine the label.

Category (d) is a property of the benchmark, not a solver failure. At least fifteen of the 138 admitted problems, 10.9%10.9\%, cannot be answered from the printed text by any method. The rate is measured on the admitted subset, where a false-discovery rate is defined, and it lower-bounds the measurable FDR of any system that, like ours, conditions its candidates on a single extraction of the printed text and admits a similar set. The estimate is conservative: only the disagreements were audited, and the five truncated-precision cases are excluded. Expert audits report aggregate error rates for these benchmarks without separating the errors behind them (Xiao et al., 2025); to our knowledge this category has not previously been isolated, nor quantified as a floor on the attainable false-discovery rate.

These failures reveal a limitation of consensus-based verification. All three families solve a common base specification produced by one extractor, so when the text omits a matrix the extractor fills it and the three independent families agree on the same fabricated instance; cross-family agreement certifies the extracted instance, not the one the benchmark author intended. NANO-CO texts are generated from their instances, so clause (i) of Assumption 1 holds there by construction, and the benchmark stream violates exactly that clause: the failure is a measured violation of a stated assumption, not a defect in Proposition 2. The remedy therefore has to act on the extracted numbers before any model is generated. Agreement between independent extractors, the obvious candidate, does not work at this granularity: on the 22 audited failures and 22 concordant controls, three extractor families never once agreed on parameter names, and after aligning parameters by shape and value, disagreement was as common on faithful texts, 21 of 22, as on unfaithful ones, 18 of 22. A simpler check does separate them: every base value in the extracted specification should be printed in the text. Applied after the fact to the pilot’s stored specifications, this numeric-coverage check flags 9 of the 15 missing-data cases, none of the 5 truncated-precision cases or the 2 label errors, none of the 116 concordant admissions, and none of the 148 calibration specifications (Appendix B.1); it is the check we specify for deployment.

The cost of the gate is predictable: relative to majority vote over the same panel, it adds one extraction call per problem and six solver runs per candidate, and on problems of this size the solver runs cost far less than one model call; complete call-level logs accompany the release.

## 5 Limitations

First, the gate certifies agreement across independently derived behaviors, not the intended meaning of the problem: a misinterpretation shared by every family survives any amount of resampling, which is why the target is the false-discovery rate over admitted items rather than a guarantee for each one.

Second, higher admission precision reduces coverage: the gate withholds a verdict on a substantial fraction of the stream, mostly for want of informative instances, and the withheld values were mostly correct; the cause lies in the extracted domains, which yield infeasible instances for most draws. Third, the pilot admits host trajectories by matching the accepted value, so the model-level evidence of resampling is not used at admission; applying the behavioral test to the host’s own trajectories would require parameterized code, which the host does not produce. Fourth, the guarantee of Proposition 2 is conditional on Assumption 1, whose violation Section 4.3 measures, and an escalation policy other than the calibrated one weakens it further (Lemma 1). Fifth, the host uses one generation backbone, and the intermediate judges of Table 3 were evaluated at admission but not downstream, because the host backbone was withdrawn by its providers during the study, and we do not evaluate a single-model selection judge, the configuration whose false-positive rate Zhou (2026) measures at 0.7190.719.

## 6 Conclusion

AdmitOR decides whether a solved trajectory should enter a persistent library before the agent reuses it. In the controlled judge swap it reaches the highest candidate-level admission precision and downstream macro accuracy with the smallest library, and the ablation on the same records attributes the gain to an accepted value that is external to the learner and unanimous across model families. The benchmark-stream experiment clarifies when the method succeeds and when it fails: calibrated FDR does not transfer when benchmark texts omit or round the numbers needed to reproduce the labeled answer, and a check of the extracted numbers against the text, which flags most of these cases without labels, must come before any model-level evidence.

### AI use statement

We used generative AI tools for the following tasks. In the required-disclosure categories: implementing analysis code used to compute reported statistics, providing feedback on experimental design, and assisting in the interpretation of experimental results. In the recommended-disclosure categories: editing the manuscript for readability, and editing, refactoring, and debugging research code. We did not use generative AI tools to generate data or to alter any recorded experimental output; all reported quantities are computed by the released code from the released logs, and the analysis scripts were validated against reconciliation checks that reproduce previously published values before any new number was accepted. All AI-assisted code was executed and verified by the authors, and all AI-assisted text was reviewed by the authors. We take responsibility for the final content of this work, including text, claims, and artifacts produced with the aid of generative AI.

## References

  * Aggarwal et al. (2023) P. Aggarwal, A. Madaan, Y. Yang, and Mausam Let’s sample step by step: adaptive-consistency for efficient reasoning and coding with LLMs.  In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP),  Cited by: §2. 
  * AhmadiTeshnizi et al. (2024) A. AhmadiTeshnizi, W. Gao, and M. Udell OptiMUS: scalable optimization modeling with (MI)LP solvers and large language models.  In International Conference on Machine Learning (ICML),  Cited by: §2. 
  * Chen et al. (2023) X. Chen, R. Aksitov, U. Alon, J. Ren, K. Xiao, P. Yin, S. Prakash, C. Sutton, X. Wang, and D. Zhou Universal self-consistency for large language model generation.  arXiv preprint arXiv:2311.17311.  Cited by: §2. 
  * Gou et al. (2024) Z. Gou, Z. Shao, Y. Gong, Y. Shen, Y. Yang, N. Duan, and W. Chen CRITIC: large language models can self-correct with tool-interactive critiquing.  In International Conference on Learning Representations (ICLR),  Cited by: §1, §2. 
  * Guha et al. (2024) N. Guha, M. F. Chen, T. Chow, I. S. Khare, and C. Ré Smoothie: label free language model routing.  Advances in Neural Information Processing Systems 37, pp. 127645–127672.  Cited by: §2. 
  * Huang et al. (2024a) J. Huang, X. Chen, S. Mishra, H. S. Zheng, A. W. Yu, X. Song, and D. Zhou Large language models cannot self-correct reasoning yet.  In International Conference on Learning Representations (ICLR),  Cited by: §1, §2. 
  * Huang et al. (2024b) X. Huang, Q. Shen, Y. Hu, A. Gao, and B. Wang Mamo: a mathematical modeling benchmark with solvers.  arXiv preprint arXiv:2405.13144.  Cited by: §2, §4.1. 
  * Jin and Candès (2023) Y. Jin and E. J. Candès Selection by prediction with conformal p-values.  Journal of Machine Learning Research 24 (244), pp. 1–41.  Cited by: §A.2, §A.2, §A.2, §2, Proposition 2. 
  * Kamoi et al. (2024) R. Kamoi, Y. Zhang, N. Zhang, J. Han, and R. Zhang When can LLMs actually correct their own mistakes? A critical survey of self-correction of LLMs.  Transactions of the Association for Computational Linguistics 12.  Cited by: §1, §2. 
  * Kong et al. (2025) M. Kong, A. Qu, X. Guo, W. Ouyang, C. Jiang, H. Zheng, Y. Ma, et al. AlphaOPT: formulating optimization programs with self-improving LLM experience library.  arXiv preprint arXiv:2510.18428.  Cited by: §1, §2. 
  * Li and Hai (2026) H. Li and M. Hai Falsification-based verification of LLM-generated optimization models: sound test batteries and their detection limits.  arXiv preprint arXiv:2607.16646.  Cited by: §2, §2, §3. 
  * Li et al. (2026) Z. Li, Z. Guo, X. Lu, J. Wang, J. Song, C. Shen, J. Wu, and M. Sun OptArgus: a multi-agent system to detect hallucinations in LLM-based optimization modeling.  arXiv preprint arXiv:2605.11738.  Cited by: §2. 
  * Lian et al. (2026) J. J. Lian, Y. Sun, H. Chen, C. Zhang, H. Qin, and C. Teo ReLoop: structured modeling and behavioral verification for reliable LLM-based optimization.  arXiv preprint arXiv:2602.15983.  Cited by: §2. 
  * Liang et al. (2026) K. Liang, Y. Lu, J. Mao, S. Sun, C. Yang, C. Zeng, X. Jin, H. Qin, R. Zhu, and C. Teo Large-scale optimization model auto-formulation: harnessing LLM flexibility via structured workflow.  arXiv preprint arXiv:2601.09635.  Cited by: §1, §2. 
  * Lin et al. (2026) J. Lin, Z. Ling, C. Zhou, T. Xu, R. Jiang, Z. Wang, and D. Ge From soliloquy to agora: memory-enhanced LLM agents with decentralized debate for optimization modeling.  arXiv preprint arXiv:2604.25847.  Cited by: §2. 
  * Liu et al. (2026) H. Liu, J. Wang, B. Niu, X. Han, Y. Xu, M. Ye, Z. Geng, et al. Opt-Verifier: unleashing the power of LLMs for optimization modeling via dual-side verification.  arXiv preprint arXiv:2605.29556.  Cited by: §2. 
  * Liu (2026) N. Liu LLMs as a jury: cross-model consensus can outperform process reward models for LLM reasoning.  arXiv preprint arXiv:2607.10139.  Cited by: §2, §3. 
  * Lu et al. (2025) H. Lu, Z. Xie, Y. Wu, C. Ren, Y. Chen, and Z. Wen OptMATH: a scalable bidirectional data synthesis framework for optimization modeling.  arXiv preprint arXiv:2502.11102.  Cited by: §2, §4, §4.1. 

