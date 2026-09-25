URL: https://arxiv.org/html/2511.09008 | FULL FETCH | 2026-09-24T01:53:37Z
warning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
URL: https://arxiv.org/html/2511.09008
Type: HTML
Length: 86689 chars (truncated)

--- Content ---

##### Report GitHub Issue

×

Title:

Content selection saved. Describe the issue below:

Description:

Submit without GitHub Submit in GitHub

arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[ Back to arXiv ](/)

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) Report Issue [ Back to Abstract ](/abs/2511.09008v2 "Back to abstract page") [ Download PDF](/pdf/2511.09008v2 "Download PDF") [ ](javascript:toggleNavTOC\(\); "Toggle navigation") [ ](javascript:toggleReadingMode\(\); "Disable reading mode, show header and footer")

  1. Abstract
  2. 1 Introduction
  3. 2 Related Work
  4. 3 Methodology
     1. 3.1 Policy Model Creator (PMC)
        1. Autoformalizing Policies
        2. PMC Policy Vetting
     2. 3.2 Answer Verifier (AV)
  5. 4 Empirical Evaluation
     1. 4.1 Evaluation of Logical Accuracy Validation
     2. 4.2 Refining Real-World Policy Models and Answers
  6. 5 Conclusions, Limitations, and Future Work
  7. References
  8. 0.A Appendix
     1. 0.A.1 Additional Experiments
        1. Impact of Human Policy Vetting
        2. Effectiveness of Feedback for Mitigating Logical Inaccuracies
        3. Utilizing PMC Rules Beyond AV
        4. PMC Scaling
     2. 0.A.2 Experiment Details
        1. Dataset Details (Section ).
        2. Baseline Details (Section ).
     3. 0.A.3 Implementation Details
        1. Fragment of SMT-LIB Utilized by ARc
     4. 0.A.4 LLM-as-Judge System Prompt
     5. 0.A.5 Answer Refinement Prompt
     6. 0.A.6 LLM-as-Judge Prompt and Outputs for Running Example



[ License: CC BY-NC-ND 4.0 ](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2511.09008v2 [cs.CL] 13 Jul 2026

#  A Neurosymbolic Approach to Natural   
Language Formalization and Verification 

Chenyang An1 Sam Bayless1 Stefano Buliani1 Darion Cassel1 Byron Cook1,2 Duncan Clough1 Rémi Delmas1 Nafi Diallo1 Ferhat Erata1 Nick Feng1 Dimitra Giannakopoulou1 Aman Goel1 Aditya Gokhale1 Joe Hendrix1 Victor Heorhiadi1 Marc Hudak1 Dejan Jovanović1 Andrew M. Kent1 Benjamin Kiesl-Reiter1(🖂)  Jeffrey J. Kuna1 Nadia Labai1 Joseph Lilien1 Divya Raghunathan1 Zvonimir Rakamarić1 Niloofar Razavi1 Michael Tautschnig1,4 Affiliation:  Amazon Web Services University College London University of Toronto Queen Mary University of London  Ali Torkamani1 Nathaniel Weir1 Michael W. Whalen1 Jianan Yao3

###### Abstract

Large Language Models perform well at natural language interpretation and reasoning, but their lack of formal correctness guarantees limits their adoption in regulated industries like finance and healthcare that operate under strict policies. To address this limitation, we launched Automated Reasoning checks (ARc): a public service that (1) uses LLMs with optional human guidance to formalize natural language policies, allowing fine-grained control of the formalization process, and (2) uses inference-time autoformalization to validate logical correctness of natural language statements against those policies. ARc performs multiple redundant formalization steps at inference time, checking the formalizations for semantic equivalence. Our benchmarks show that ARc exceeds 99% soundness and achieves a near-zero false positive rate in identifying logical validity. Our approach produces auditable artifacts that substantiate the verification outcomes and can be used to improve the original text. ARc is the first commercial offering from a major cloud provider to integrate automated reasoning into a generative AI guardrail.

## 1 Introduction

The capabilities of Large Language Models (LLMs) continue to advance rapidly, demonstrating unprecedented improvements in coherence and analytical accuracy [38, 43, 20]. Despite these advances, their tendency to generate plausible but incorrect information (hallucinations, cf. [41]) remains a barrier to widespread adoption in regulated sectors. Industries such as healthcare, financial services, and legal practices have legal and regulatory obligations for accuracy and auditability that current LLM technology has yet to meet [9].

Companies develop institutional policies to ensure compliance with laws and regulations. Such policies are typically captured in natural language (NL), defining rules, procedures, or guidelines. When deploying LLMs to answer questions about these policies, a key challenge emerges: can we develop _guardrails_ to ensure that the LLM outputs are correct? Consider an airline implementing a chatbot to assist customer service representatives in navigating refund policies: if the chatbot incorrectly claims that a customer is eligible for a refund, this could lead to legal exposure and loss of customer trust.

An effective guardrail would enable representatives to rely on chatbot responses by ensuring that when it reports an answer as valid, it actually is. Inspired by the concept of soundness in logic, we define _soundness_ in our context as (1−r)(1-r), where rr is the rate of incorrect validity claims across all decisions. High soundness thus means that across all requests, incorrect approvals are rare. Following established practices in safety-critical systems, where reliability is often measured in “nines” (e.g., 99% = “two nines,” 99.9% = “three nines”), we target soundness levels of at least 99%, and secondarily focus on recall to maximize the probability of accepting valid content. We also pursue actionable feedback that steers LLMs toward content that a conservative guardrail can accept.

A natural candidate for robust guardrails are symbolic reasoning systems, as they use formal logic to generate independently verifiable guarantees [29]. This aligns well with policy documents, which rely on logical, rule-like statements (e.g., “if a flight is canceled or …, then passengers are entitled to a refund”). But symbolic methods struggle with interpreting natural language, triggering the development of neurosymbolic approaches that combine the NL processing capabilities of neural networks with the mathematical rigor of symbolic systems [12].

This paper presents Automated Reasoning checks (ARc), a neurosymbolic approach exceeding 99% soundness on datasets it was not trained on. High soundness is also reflected in metrics such as false positive rate and precision. In addition, ARc delivers explainable verdicts and provides actionable feedback for revising LLM outputs. ARc is the first commercial offering from a major cloud provider to integrate automated reasoning into a generative AI guardrail.

ARc operates through two complementary components. The first, called Policy Model Creator (PMC), combines LLMs with symbolic reasoning to translate NL policies into formal _policy models_ expressed in logic. It begins with an autoformalization phase that generates an initial policy model. This is followed by an optional vetting phase where domain experts refine the policy model with assistance from the system. Vetting enables domain experts to resolve ambiguities and inconsistencies in the original documents, or to correct potential imprecisions from autoformalization. Policy model creation occurs offline; its computation cost will be amortized across subsequent verification tasks.

The second component, called Answer Verifier (AV), verifies NL content against policy models. The AV uses LLMs to translate NL content into individual logical claims in the scope of the policy model. Each claim is analyzed separately and assigned a verification result, together with detailed logical explanations and corrective guidance. To increase reliability, the AV uses multiple LLMs to simultaneously formalize the same NL content, then uses symbolic reasoning to compare formalizations and assign confidence scores. The AV delivers auditable logical artifacts that substantiate the verification outcomes.

## 2 Related Work

Recent approaches use LLMs as judges to evaluate factual accuracy [16], though these rely on the same LLMs that are subject to inaccuracies to evaluate LLM-generated content. MiniCheck [34] provides efficient fact-checking by decomposing claims. RefChecker [13] introduces knowledge-centric verification against structured knowledge bases. SelfCheckGPT [22] leverages consistency across responses to detect hallucinations. FactCheck-GPT [37] provides comprehensive evaluation with fine-grained error categorization. While promising, these methods cannot provide formal guarantees. Our neurosymbolic framework verifies logical validity against formalized policies, achieving near-zero false positives.

Neurosymbolic systems combine LLMs (sometimes enhanced with Chain-of-Thought prompting [40, 21, 10]) with symbolic reasoning. They typically translate NL to formal representations that are then solved by external reasoners [26, 25, 4, 30]. LINC [25] uses first-order logic with Prover9 [23]. Verus-LM [4] provides a multi-paradigm framework with IDP-Z3 [5]. SAT-LM [44] employs declarative prompting with SMT [7]. Logic-LM [26] supports multiple formalisms with self-refinement. Other approaches use custom DSLs [8] or Answer Set Programming [15, 42, 3].

These neurosymbolic systems formalize both the background knowledge and the query in a single step for each problem instance (or, in the case of [42], rely on hand-written background knowledge). In contrast, ARc autoformalizes both but separates them: the policy model can be vetted independently (through linting, symbolic test case generation, and human review) before being reused across many verifications. Regarding translation correctness, most of these systems offer only syntactic error detection and basic consistency checks (e.g., satisfiability of the formalized theory). LINC goes further by sampling multiple translations from a single model and applying majority voting over solver outcomes (Valid, Invalid, Unknown) rather than comparing translations at the logic level. ARc cross-checks per-query translations across diverse models using a notion of symbolic equivalence, with confidence thresholds indicating semantic agreement.

Autoformalization has been studied extensively in mathematics [36, 32, 39, 17]. In contrast to ARc, these efforts typically assume that the background knowledge (the mathematical theory) has been pre-formalized, often by humans, and only the problem to be solved must be formalized by an LLM.

There is also a substantial body of work on dedicated formal languages for capturing policies and legislation, see, e.g., the Programming Languages and the Law (ProLaLa) workshops at POPL. Catala [24] is a notable example: a domain-specific language designed for systematic translation of statutory law into executable code, using defeasible reasoning to handle the general-case/exceptions logic common in legal texts. Such approaches capture laws directly in the dedicated language, whereas ARc autoformalizes existing NL policy documents into logic. Casadio et al. [6] propose a methodology for certifying the robustness of NLP models, showing how verification errors can stem from the NL representation layer. Their work on robustness guarantees for NL models is complementary to our redundant translation approach for mitigating translation errors.

## 3 Methodology

Pipeline diagram with two main components. Top: Policy Model Creator (PMC) takes a natural-language policy document, splits it into text spans, autoformalizes each span with self-refinement, and composes them into a policy model. It then applies logical test case enumeration and conflict detection, which serve as user feedback that can be leveraged for manual and LLM-guided repair to arrive at the final policy model. Bottom: Answer Verifier (AV) takes a question-answer conversation, produces multiple autoformalizations, aggregates them via logical equivalence, verifies against the policy model using an SMT solver, and outputs verification results with feedback.

Figure 1: End-to-end architecture of ARc

Fig. 1 shows ARc’s two main components: the PMC (§3.1) and the AV (§3.2). We illustrate our approach with an NL policy about park admission fees:

General admission: The regular admission to the park is $50. The admission fee in the low season is 75% of the regular admission fee. Discount: Seniors (age greater than 65) qualify for a 40% discount. Whenever a discount applies, there will be a $10 flat discount processing fee. Credit: You can use credit for up to 50% of your final admission (1 credit for 1 dollar). However, if credits are used, then the discount rate is capped at 25%. You can purchase credit at a rate of $0.60 per credit. You can only purchase credit in increments of 5 (cost $3). Tax: A federal tax of 10% applies to the final expense.

Suppose a user asks “I am a senior and want to visit the park in the low season, and I have a budget of $35.40. Can I visit the park?”, and we want to verify a chatbot’s answer of “No, $35.40 is not enough.”

ARc tackles the verification problem in two stages. In the first stage, the PMC autoformalizes the policy into a _policy model_ : a set of logic rules, expressed in SMT-LIB [2], together with a _schema_ that defines variables with their types and NL descriptions. SMT-LIB is a standardized logic language that uses prefix notation, where operators precede their arguments; e.g., “if xx, then yy” is written as (=> x y). Fig. 2 shows snippets of the policy model. In the second stage, the AV autoformalizes the statement under validation into logic formulas (over the policy model schema), then uses an SMT solver to verify those formulas against the policy model. The result includes the logic translation (with a confidence score between 0 and 1), the validation result, and further feedback (see Fig. 3).

In our example, the result is Satisfiable: the claim (cannot visit the park) is consistent with the premises (the person is a senior, it is low season, and they have a fund of $35.40 available) but doesn’t necessarily follow from them. AV provides two assignments as feedback: one showing a counter-example where admission is possible, and a case where the person cannot enter the park. The key difference is in the use of credits (𝑐𝑟𝑒𝑑𝑖𝑡𝑈𝑛𝑖𝑡=3\mathit{creditUnit=3} vs. 𝑐𝑟𝑒𝑑𝑖𝑡𝑈𝑛𝑖𝑡=0\mathit{creditUnit=0}).

_Explanation._ The person needs to use $15 worth of credits for admission. The admission fee in the low season is $37.5 (75% of $50). After applying the 25% senior discount (capped at 25% because of credit use) and adding the $10 discount processing fee, the actual admission fee becomes $38.12538.125. This fee can be paid by combining $15 of credit (cost: $9) with a $23.12523.125 cash payment, for an expense of $32.12532.125. After adding a federal tax of 10%, the final expense becomes $35.337535.3375, which is within the budget of $35.40. Both Claude Sonnet 3.7 and Opus 4.1 (with reasoning mode) incorrectly classified the answer as valid, providing plausible but flawed reasoning (see Appendix Figs 10 and 11).

Variable | Type |  Description  
---|---|---  
isLowSeason | Bool |  Whether the admission day is in the low season  
feeAfterDiscount | ℝ\mathbb{R} |  Admission fee after discounts are applied but before tax  
  
Rule 1: (=> isLowSeason (= admissionFee (* 0.75 baseFee)))   
Rule 2: (<= (* 2.0 customerCredits) feeAfterDiscount)

Figure 2: Snippets of policy model (top: variable schema; bottom: rules)

Translation (Confidence: 1.0) PP: (and (= ageClass SENIOR) isLowSeason (= totalAdmissionFund 35.4)) CC: (not isEntryAllowed) Result: Satisfiable (not Valid) Counter-Example (shows CC can be false): creditUnit=3, customerCredits=15.0, creditDollarValue=9.0, cashAmount=23.181, totalPaymentAvailable=38.181, finalAdmissionFee=38.125, isEntryAllowed=true, … Satisfying Assignment (shows CC can be true): creditUnit=0, finalAdmissionFee=35.75, isEntryAllowed=false, …

Figure 3: Snippet of validation feedback

### 3.1 Policy Model Creator (PMC)

The PMC takes a policy document written in natural language and autoformalizes it into a policy model. It also provides an array of utilities to support users in policy vetting, described in detail in the _Policy Vetting_ paragraph below.

#### Autoformalizing Policies

To handle the size and complexity of real-world policy documents in the face of known LLM reasoning limitations around context size and distractors [28, 19], the PMC takes a divide-and-conquer approach to autoformalize documents into logic (see Fig. 1).

The PMC first splits the input document into a set of text spans. These are processed using an incremental, refinement-guided autoformalization procedure: A language model processes each span and identifies statements that express coherent, formalizable meaning. For each statement, the LLM translates the semantic content into a list of SMT-LIB datatypes, variables, and logical constraints (_rules_). The LLM’s context maintains existing declarations within a span to avoid duplicated or conflicting declarations. The complete formalization of a span is what we call a _policy unit_. If this process introduces an error (e.g., malformed syntax), we provide the invalid declarations and their failure causes to the LLM for repair in a refinement loop.

After the PMC has formalized all text spans, it composes the policy units into a single policy model. The PMC generates textual embeddings of variables and clusters them using cosine similarity. Variables within a cluster are unified, while variables that share the same name but are not clustered are renamed. Consistent replacement of original variables with unified variables is performed for the rules of each policy unit, then the rules are aggregated, dropping syntactic duplicates. The resulting policy model is a structured representation of the document, consisting of three fields: datatypes, variables, and rules. Each variable is associated with an NL description that explains its meaning in terms of the source document, as shown in Fig. 2. This initial policy model is then vetted, as described in §3.1. We measure the relationship between document size and formalized policy size in §0.A.1.

#### PMC Policy Vetting

The initial policy model might contain errors and omissions. Additionally, as shown in §4.2, NL policies often contain ambiguities that only subject matter experts can resolve. We therefore provide users with several methods for vetting of their policy models: linting, inspection, and testing (both manual and automatic). We also develop automated repair approaches around these vetting methods.

_Linting._ A linter for our policy models that checks integrity and consistency properties beyond the simple malformedness errors caught during autoformalization. We perform a mix of syntax-based and semantic checks: we detect unused variables and types, contradictory rules, and disjoint rule sets. The list of warnings is shown to the user, who can address them directly (e.g., by deleting an unused variable) or through more detailed policy inspection and repair.

_Inspection._ Manual inspection allows users to review the generated policy model, similar to code review in software development. We assist users by providing two views of the rules for inspection: SMT-LIB for experts and structured English for non-experts. Structured English is generated using templates (like “if … then …”) to avoid potential hallucinations from LLMs. Users also can provide NL feedback on the policy, which triggers an automatic LLM-based policy repair step that adjusts the policy model. Manual inspection provides strong correctness guarantees when all rules are carefully reviewed, but it can be challenging with large numbers of complex rules that have intricate interactions. The PMC therefore also provides testing as an additional policy vetting methodology.

_Testing._ Testing provides a systematic way to validate policy models through examples. Similar to unit tests, test cases in the PMC are either NL question-answer pairs or simple NL statements with their expected outcomes provided by the user (e.g., valid, invalid). Test cases can either be provided manually by users or generated automatically. For manually provided test cases, the PMC “executes” them by running the AV to compute the findings; a mismatch indicates an error in the policy model or in the AV translation. The PMC also offers automatic, symbolic test-case generation that leverages an SMT solver to systematically explore the state space of the policy model. Since such test cases are generated symbolically, each comes with its provably-correct actual finding, so a mismatch isolates the error to the policy model. Either way, the supplied information (e.g., rules justifying the result) helps users diagnose and repair.

### 3.2 Answer Verifier (AV)

The AV uses LLMs to translate natural language (i.e., question-answer pairs) into a list of premise-conclusion pairs, where premises (PP) and conclusions (CC) are expressed in the policy model’s schema. For example, "Since you have at least $50, you can enter the park" translates to premise (≥𝑡𝑜𝑡𝑎𝑙𝐴𝑑𝑚𝑖𝑠𝑠𝑖𝑜𝑛𝐹𝑢𝑛𝑑​50)(\geq\mathit{totalAdmissionFund}~50) and conclusion 𝑖𝑠𝐸𝑛𝑡𝑟𝑦𝐴𝑙𝑙𝑜𝑤𝑒𝑑\mathit{isEntryAllowed} which represent the contextual facts and logical consequences, respectively.

To increase translation confidence, the AV _redundantly translates_ the NL statement using kk LLMs (Alg. 1), then compares the resulting premise-conclusion pairs semantically using an SMT solver to estimate a confidence score for each pair. Intuitively, the confidence score of a premise-conclusion pair ⟨P,C⟩\langle P,C\rangle is the proportion of the kk translations that non-vacuously entail the implication P⇒CP\Rightarrow C (i.e., entail it without rendering PP contradictory). For example, consider the text from §3 and the policy model in Fig. 2. Redundant translation with three LLMs produces three identical premise-conclusion pairs, thus producing the results in Fig. 3 with confidence score 3/33/3 (1.0). If one LLM instead produced a pair with a different conclusion (isEntryAllowed), AV would return two distinct pairs: the original from Fig. 3 with confidence 2/32/3, and the alternative with confidence 1/31/3.

Algorithm 1 AV Redundant Translation

1: procedure RedundantTranslation(m​s​gmsg, policy, L​L​M​sLLMs) 

2: F←∅F\leftarrow\emptyset; Ts←\textit{Ts}\leftarrow [Translate(m​s​gmsg, policy, l​l​mllm) ∣\mid l​l​m∈LLMsllm\in\textit{LLMs}] 

3: for each ⟨P,C⟩\langle P,C\rangle in every T∈T​sT\in Ts do

4: FF.add(⟨P,C,𝑐𝑓⟩\langle P,C,\mathit{cf}\rangle) where 𝑐𝑓=|{T′∈Ts∣T′⊧(P⇒C)∧T′⊧̸¬P}|/|T​s|\mathit{cf}=|\\{T^{\prime}\in\textit{Ts}\mid T^{\prime}\models(P\Rightarrow C)\land T^{\prime}\not\models\neg P\\}|/|Ts|

5: return FF

_Validation Feedback._ After translation, the AV uses an SMT solver to validate each claim ⟨P,C,𝑐𝑜𝑛𝑓⟩\langle P,C,\mathit{conf}\rangle against ℳ\mathcal{M} while producing logically grounded feedback given the following precedence order:

Finding | Condition  
---|---  
TooComplex | Text or SMT-LIB translation exceeds token limits  
TranslationAmbiguous | Confidence below threshold (default: 3/33/3)  
NoTranslations | LLM cannot translate text to policy model vocabulary  
Impossible | ℳ⊨¬P\mathcal{M}\vDash\lnot P (premises contradict policy model)  
Invalid | ℳ∧P⊨¬C\mathcal{M}\land P\vDash\lnot C (conclusion is inconsistent)  
Valid | ℳ∧P⊨C\mathcal{M}\land P\vDash C (conclusion is entailed)  
Satisfiable | ℳ∧P⊭C\mathcal{M}\land P\nvDash C and ℳ∧P⊭¬C\mathcal{M}\land P\nvDash\lnot C (consistent, not entailed)  
  
For Impossible, Invalid, and Valid findings, the feedback includes relevant rules from the policy model extracted from the SMT solver, providing sufficient information for independent verification via theorem prover. For Satisfiable findings, the feedback returns assignments ("scenarios") demonstrating how the answer can be correct or wrong, thus providing hints on how the premises could be extended to make the conclusion valid (see Fig. 3, for example, where the use of credits is a differentiator between the scenarios). For TranslationAmbiguous findings, the feedback presents two differing translations, together with an assignment that is satisfiable in one translation but not in the other. NoTranslations findings return the untranslatable text segments. Logic warnings are surfaced if premises or conclusions are always true or false irrespective of policy rules.

## 4 Empirical Evaluation

In order to understand ARc’s effectiveness as a guardrail, and the impact of our design choices, we evaluate ARc, and more specifically the AV, around the following research questions (RQs):

RQ1 (Reliability of Validating Logical Accuracy):
    

How reliably does ARc validate logical accuracy compared to alternative baselines?

RQ2 (Impact of Redundant Translation):
    

How does redundant translation (§3.2) impact ARc’s performance?

RQ3 (Effectiveness of ARc’s feedback):
    

Is ARc’s feedback effective in driving improvement of LLM outputs?

_Metrics._ We frame logical accuracy detection as a binary classification problem: decide whether NL statements are Valid or not.

To target high-stakes applications, our primary objective is to eliminate false positives across the entire pipeline. In this context, rejecting borderline cases (not-valid) is favorable: such outputs can either be refined by the answer-generating LLM using ARc feedback, or escalated to human experts. We thus define _soundness_ as 1−#​False Positives#​Samples1-\frac{\\#\text{False Positives}}{\\#\text{Samples}}, measuring the rate at which incorrect approvals occur across all decisions.

A natural alternative to soundness would be precision. The two metrics differ in perspective: precision estimates a posterior (“Given a request was classified as Valid, how likely is that verdict to be correct?”), while soundness estimates a prior (“How likely is a request to receive an incorrect Valid verdict?”). Based on customer feedback, we prioritized the prior perspective: ARc’s customers are service operators deploying chatbots across thousands of daily interactions, where the relevant operational question is how likely any given request is to be incorrectly approved. Like any soundness notion, our soundness rewards abstention and is incomplete on its own, so we use recall to complement it. As mentioned in §1, we target soundness levels of at least 99%.

In addition to soundness, we use standard classification metrics (precision, recall, F1, accuracy), treating Valid as the positive class and all others as negative. When comparing alternative methods, Valid recall is used as a tie-breaker under the requirement of maintaining high soundness.

### 4.1 Evaluation of Logical Accuracy Validation

Table 1: Comparison of logical accuracy detection performance on ConditionalQA-logic [31]. The columns show soundness (S), false-positive rate (FPR), precision (Pr), recall (Re), F1 score (F1), accuracy (Ac), counts of true/false positives/negatives (TP/FP/TN/FN), and error count (Error#). Approaches meeting soundness threshold are highlighted, as well as best and worst values for other metrics. 

Method | S ↑\uparrow | FPR ↓\downarrow | Pr ↑\uparrow | Re ↑\uparrow | F1 ↑\uparrow | Ac ↑\uparrow | TP ↑\uparrow | FP ↓\downarrow | TN ↑\uparrow | FN ↓\downarrow | Error# ↓\downarrow  
---|---|---|---|---|---|---|---|---|---|---|---  
ARc (#3-ensemble, threshold=3/3) | 99.4 | 1.8 | 94.4 | 14.9 | 25.8 | 42.4 | 169 | 10 | 548 | 962 | 5  
ARc (#3-ensemble, threshold=2/3) | 99.2 | 2.5 | 93.2 | 16.9 | 28.6 | 43.5 | 191 | 14 | 544 | 940 | 9  
ARc (without redundant translation) | 98.4 | 4.8 | 92.2 | 28.0 | 43.0 | 50.2 | 317 | 27 | 531 | 814 | 1  
LLMaJ (#3-ensemble, threshold=3/3) | 98.2 | 5.4 | 92.4 | 32.4 | 47.9 | 52.9 | 366 | 30 | 528 | 765 | -  
LLMaJ (#3-ensemble, threshold=2/3) | 97.9 | 6.3 | 92.1 | 36.3 | 52.0 | 55.2 | 410 | 35 | 523 | 721 | -  
LLMaJ (1x Sonnet4.5) | 97.9 | 6.3 | 92.0 | 35.4 | 51.1 | 54.6 | 400 | 35 | 523 | 731 | -  
LLMaJ (1x Sonnet4.5 w/ extended thinking) | 97.1 | 8.8 | 92.7 | 55.0 | 69.0 | 67.0 | 622 | 49 | 509 | 509 | -  
FG Implicit span-level [16] | 95.0 | 15.2 | 90.4 | 70.6 | 79.2 | 75.3 | 798 | 85 | 473 | 333 | -  
FG JSON [16] | 94.6 | 16.5 | 89.7 | 70.5 | 78.9 | 74.8 | 797 | 92 | 466 | 334 | -  
FG Response-level [16] | 83.8 | 49.1 | 78.3 | 87.6 | 82.7 | 75.5 | 991 | 274 | 284 | 140 | -  
MiniCheck [18] | 88.5 | 34.9 | 83.0 | 84.4 | 83.7 | 78.0 | 954 | 195 | 363 | 177 | -  
RefChecker [13] | 91.9 | 24.6 | 86.3 | 76.0 | 80.8 | 75.8 | 860 | 137 | 421 | 271 | -  
SelfCheckGPT [22] | 93.0 | 21.1 | 89.2 | 86.3 | 87.7 | 83.8 | 976 | 118 | 440 | 155 | -  
Logic-LM [26] | 98.0 | 5.9 | 86.4 | 18.6 | 30.6 | 43.5 | 210 | 33 | 525 | 921 | 1149  
Proof of Thought [8] | 88.8 | 33.9 | 81.2 | 72.2 | 76.4 | 70.2 | 817 | 189 | 369 | 314 | 0  
LINC [25] | 99.9 | 0.2 | 98.7 | 6.6 | 12.4 | 37.4 | 75 | 1 | 557 | 1056 | 696  
  
_Dataset._ Several reasoning benchmarks (e.g., FOLIO [11], ProofWriter [33], and LogicNLI [35]) test logical inference, but our focus is on validating whether NL answers comply with formalized policy documents. We therefore focus on the ConditionalQA dataset [31] because it is well-aligned with our task, featuring: 1) questions that require compositional logical reasoning, 2) variety of questions (yes/no, multiple answers, not-answerable), and 3) human annotated answers.

We enrich the ConditionalQA dev dataset (391 labeled QAs over 59 source documents) with several types of “not valid” examples beyond its original “valid” / “not_answerable” classification. The resulting set includes the following categories: Valid (logically correct), Invalid (incorrect due to wrong conditions), Satisfiable (missing necessary conditions), Impossible (contradictory conditions), and NoTranslations (content that cannot be formalized, originally classified as not-answerable). These categories were created by systematically manipulating the conditional structure of original answers: removing conditions (Valid →\rightarrow Satisfiable), negating the claim (Valid →\rightarrow Invalid), or merging contradictory conditions (Valid →\rightarrow Impossible). The extended dataset (ConditionalQA-logic) contains 377 Valid examples and 186 examples that are not Valid (112 Invalid, 56 Satisfiable, 4 Impossible, and 14 NoTranslations).

Our goal in this section is to evaluate the AV’s soundness in an end-to-end setting with automatically generated, unvetted policy models. The policy models used for Table 1 were autoformalized by the PMC and not manually refined. Section 4.2 provides initial evidence that human vetting can further improve both soundness and recall.

_RQ1: Reliability of Validating Logical Accuracy._ Table 1 reports on the comparison of ARc against alternative methods: LLM-as-Judge (LLMaJ) with different prompting strategies, FACTS Grounding (FG) [16], fine-grained hallucination detection methods [34, 18, 22, 13], and other neurosymbolic approaches [26, 8, 25]. This evaluation focuses on the ability of each approach to predict validation labels for QA pairs about given NL policy documents. We evaluate each of the 563 benchmark instances three times to account for nondeterminism in LLM outputs, yielding 1689 total decisions.

We first examine the approaches that meet our soundness threshold, which are only ARc and LINC [25]. Between the two, ARc has a higher recall (14.9% vs 6.6%) and significantly fewer errors (5 vs 696 out of 1689 instances), where errors are instances in which the system was unable to formalize the QA contents and thus could not produce a verdict. Second, we compare ARc to others that did not achieve the required soundness threshold of 99%. ARc’s reliability comes with lower recall (14.9% for the configuration with soundness over 99%), but the tradeoff is intentional: in safety-critical domains, false approvals are far more costly than false rejections. Among the methods below the soundness threshold, LLMaJ (#3-ensemble, threshold=3/3) comes closest at 98.2% soundness with precision similar to ARc’s (92.4% vs 94.4%), but produces 3 times as many false positives (30 vs 10, or 5.4% vs 1.8% FPR). In contrast, FG Response-level has the highest recall of 87.6%, but this comes at the cost of soundness dropping to just 83.8%, the second-lowest of all methods.

_RQ2: Impact of Redundant Translation._ ARc uses redundant translation (Alg. 1) to increase confidence in NL-to-logic translations. Comparing the first 3 rows of Table 1: soundness rises from 98.4% to 99.4% and FPR drops from 4.8% to 1.8%, at the cost of reduced recall (28.0% to 14.9%). Lowering the confidence threshold from 3/33/3 to 2/32/3 recovers recall to 16.9%, with soundness dropping to 99.2%.

ARc’s recall is low compared to the other techniques in Table 1, meaning that in many cases it returns results other than Valid for content that should be Valid. ARc is intended to be deployed as a guardrail for chatbots in regulated industries, where an incorrect approval (e.g., ‘you qualify at 0% interest’) causes real harm at scale. In this setting, a non-Valid verdict is not a failure: the system can revise the answer using ARc’s feedback (see RQ3) or route to a customer support agent. Low recall thus means more deferrals, not more failures, and at 99.4% soundness, Valid verdicts carry strong enough assurance to reduce the review burden. In Section 4.2, we demonstrate that three rounds of revision with ARc’s feedback can drive the rate of Valid answers from 9% to 46% on a real-world policy.

### 4.2 Refining Real-World Policy Models and Answers

Figure 4: ARc validation finding distribution after kk iterations of answer revision using ARc feedback. At k=0k=0, we plot the finding distribution before any revisions.

To understand the applicability of ARc to real-world policies, we collected customer-facing policy documents from six different businesses, refined with human-in-the-loop vetting (§3.1). We use these policies to evaluate iterated self-refinement of LLM answers using ARc feedback (RQ3); in Appendix 0.A.1, we additionally share one policy as a case study of the manual refinement process itself (soundness: 96.8%→\to100%, recall: 25%→\to45.5%).

_RQ3: Effectiveness of ARc’s Feedback._ In a real-world setting, users may deploy LLM-based chatbots to answer questions about policies, requiring assurance of answer correctness. The formally-grounded feedback that ARc provides (Section 3.2) can be used for automated answer revision: given a non-Valid verdict, an LLM iteratively revises its answer using ARc’s feedback. Fig. 4 shows how the relative percentages of each finding type evolve as an LLM iteratively revises AV-judged non-Valid answers using ARc feedback (#3-ensemble, threshold=3/3). After just three iterations, the LLM goes from 9% to 46% Valid answers. Primarily, this comes from a sharp reduction in AV-judged Satisfiable answers (where the answer could be true or false depending on context not provided in the question or answer). By providing logically-derived scenarios showing when the answer is true and when it is false, ARc enables the LLM to effectively revise these into Valid answers. ARc’s feedback is less effective in revising TranslationAmbiguous and NoTranslations answers. Our analysis shows that in these cases revising the policy model is more effective; e.g., the policy model could be missing variables, leading to a failure to formalize the answer, or the policy model could have variables that overlap in meaning, leading to a failure to generate a consistent formalization of the answer. Average iterations to Valid and success rate per finding type can be seen in Appendix Table 5.

## 5 Conclusions, Limitations, and Future Work

We presented ARc, a neurosymbolic guardrail that exceeds 99% soundness when validating LLM answers against NL policies. This soundness comes at the cost of recall, a tradeoff we believe appropriate for regulated industries. Since its launch, ARc has been adopted across industries, including responsible AI in education [27], financial AI agents [14], and logistics operations [1]. Soundness of ARc heavily depends on the quality of the policy model that it uses for validation. For this reason, ARc enables human oversight. As we have shown, ARc provides meaningful feedback to aid automated answer revision, resulting in an increase of Valid answers. Despite ARc’s high soundness, there are limitations:

  * •

Document types: Policies with numerical tables, cross-references, or implicit assumptions can be challenging to formalize without human vetting.

  * •

Autoformalization challenges: Subtle issues like ambiguous pronouns or implicit temporal scoping can lead to incorrect formalizations.

  * •

Computational cost: Redundant translation requires multiple (3) LLM calls, resulting in average 5-15 second latency and increased API cost per Q/A validation with our current implementation.

  * •

Human effort: The investment for human vetting of policies, while amortized over time, remains a significant upfront cost, especially for large documents.

  * •

Dataset representativeness: The mechanically mutated evaluation examples (removing conditions, negating claims, merging contradictory conditions) may not fully capture the kinds of errors real LLMs produce in practice. Evaluating on naturally occurring LLM failures is a direction for future work.




Future work includes exploring automatic and confidence-aware focused vetting, fine-tuned translation models for improving accuracy and latency/costs, and improved logical formalisms to address current limitations. Our approach directly benefits from advances in LLMs and generative AI techniques: as models improve, their ability to formalize natural language to logic will too. We are confident ARc will inherit these improvements while maintaining the mathematical guarantees provided by symbolic reasoning.

#### Disclosure of Interests.

The authors have no competing interests to declare that are relevant to the content of this article.

#### Data-Availability Statement.

ARc is publicly available as part of Amazon Bedrock Guardrails at <https://aws.amazon.com/bedrock/guardrails/>. The evaluation uses a non-public augmentation of ConditionalQA [31].

## References

  * [1] Amazon Web Services (2025) Amazon logistics automates electric vehicle design reviews on AWS.  Note: <https://aws.amazon.com/solutions/case-studies/amazon-logistics-case-study/>Accessed: 2026-05-01 Cited by: §5. 
  * [2] C. Barrett, P. Fontaine, and C. Tinelli (2016) The Satisfiability Modulo Theories Library (SMT-LIB).  Note: www.SMT-LIB.org Cited by: §3. 
  * [3] G. Brewka, T. Eiter, and M. Truszczyński (2011) Answer set programming at a glance.  Communications of the ACM 54 (12), pp. 92–103.  External Links: [Document](https://dx.doi.org/10.1145/2043174.2043195) Cited by: §2. 
  * [4] B. Callewaert, S. Vandevelde, and J. Vennekens (2025) VERUS-LM: a versatile framework for combining LLMs with symbolic reasoning.  In Proceedings 41st International Conference on Logic Programming, ICLP 2025, Rende, Italy, 12-19th September 2025, M. Gebser, D. Inclezan, F. Ricca, M. Carro, and M. Truszczynski (Eds.),  EPTCS, pp. 47–62.  External Links: [Link](https://doi.org/10.4204/EPTCS.439.5), [Document](https://dx.doi.org/10.4204/EPTCS.439.5) Cited by: §2. 
  * [5] P. Carbonnelle, S. Vandevelde, J. Vennekens, and M. Denecker (2022) Interactive configurator with fo (.) and idp-z3.  arXiv preprint arXiv:2202.00343.  Cited by: §2. 
  * [6] M. Casadio, T. Dinkar, E. Komendantskaya, L. Arnaboldi, M. L. Daggitt, O. Isac, G. Katz, V. Rieser, and O. Lemon (2026) NLP verification: towards a general methodology for certifying robustness.  European Journal of Applied Mathematics 37 (1), pp. 180–237.  External Links: [Document](https://dx.doi.org/10.1017/S0956792525000099) Cited by: §2. 
  * [7] L. M. de Moura and N. S. Bjørner (2008) Z3: an efficient SMT solver.  In Tools and Algorithms for the Construction and Analysis of Systems, 14th International Conference, TACAS 2008, Held as Part of the Joint European Conferences on Theory and Practice of Software, ETAPS 2008, Budapest, Hungary, March 29-April 6, 2008. Proceedings, C. R. Ramakrishnan and J. Rehof (Eds.),  Lecture Notes in Computer Science, pp. 337–340.  External Links: [Link](https://doi.org/10.1007/978-3-540-78800-3%5C_24), [Document](https://dx.doi.org/10.1007/978-3-540-78800-3%5F24) Cited by: §2. 
  * [8] D. Ganguly, S. Iyengar, V. Chaudhary, and S. Kalyanaraman (2024) Proof of thought : neurosymbolic program synthesis allows robust and interpretable reasoning.  CoRR abs/2409.17270.  External Links: [Link](https://doi.org/10.48550/arXiv.2409.17270), [Document](https://dx.doi.org/10.48550/ARXIV.2409.17270), 2409.17270 Cited by: §2, §4.1, Table 1. 
  * [9] J. Haltaufderheide and R. Ranisch (2024) The ethics of chatgpt in medicine and healthcare: a systematic review on large language models (llms).  npj Digit. Medicine 7 (1).  External Links: [Document](https://dx.doi.org/10.1038/S41746-024-01157-X), [Link](https://doi.org/10.1038/s41746-024-01157-x) Cited by: §1. 
  * [10] S. Han, T. Liu, C. Li, X. Xiong, and A. Cohan (2024) HYBRIDMIND: Meta Selection of Natural Language and Symbolic Language for Enhanced LLM Reasoning.  arXiv e-prints, pp. arXiv:2409.19381.  External Links: [Document](https://dx.doi.org/10.48550/arXiv.2409.19381), 2409.19381 Cited by: §2. 
  * [11] S. Han, H. Schoelkopf, Y. Zhao, Z. Qi, M. Riddell, W. Zhou, J. Coady, D. Peng, Y. Qiao, L. Benson, L. Sun, A. Wardle-Solano, H. Szabó, E. Zubova, M. Burtell, J. Fan, Y. Liu, B. Wong, M. Sailor, A. Ni, L. Nan, J. Kasai, T. Yu, R. Zhang, A. R. Fabbri, W. Kryscinski, S. Yavuz, Y. Liu, X. V. Lin, S. Joty, Y. Zhou, C. Xiong, R. Ying, A. Cohan, and D. Radev (2024) FOLIO: natural language reasoning with first-order logic.  In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, EMNLP 2024, Miami, FL, USA, November 12-16, 2024, Y. Al-Onaizan, M. Bansal, and Y. Chen (Eds.),  pp. 22017–22031.  External Links: [Link](https://doi.org/10.18653/v1/2024.emnlp-main.1229), [Document](https://dx.doi.org/10.18653/V1/2024.EMNLP-MAIN.1229) Cited by: §4.1. 
  * [12] P. Hitzler and Md. K. Sarker (Eds.) (2021) Neuro-symbolic artificial intelligence: the state of the art.  Frontiers in Artificial Intelligence and Applications, Vol. 342, IOS Press.  External Links: [Link](https://doi.org/10.3233/FAIA342), [Document](https://dx.doi.org/10.3233/FAIA342), ISBN 978-1-64368-244-0 Cited by: §1. 
  * [13] X. Hu, D. Ru, L. Qiu, Q. Guo, T. Zhang, Y. Xu, Y. Luo, P. Liu, Y. Zhang, and Z. Zhang (2024) Knowledge-centric hallucination detection.  In Proceedings of the 2024 Conference on Empirical Methods in Natural Language Processing, Y. Al-Onaizan, M. Bansal, and Y. Chen (Eds.),  Miami, Florida, USA, pp. 6953–6975.  External Links: [Document](https://dx.doi.org/10.18653/v1/2024.emnlp-main.395), [Link](https://aclanthology.org/2024.emnlp-main.395/) Cited by: §0.A.2, §2, §4.1, Table 1. 
  * [14] ICME (2026) AI agents can move money – Lobstar & Wilde proved they can lose it too.  Note: <https://blog.icme.io/ai-agents-can-move-money-lobstar-wilde-proved-they-can-lose-it-too/>Accessed: 2026-05-01 Cited by: §5. 
  * [15] A. Ishay, Z. Yang, and J. Lee (2023) Leveraging large language models to generate answer set programs.  In Proceedings of the 20th International Conference on Principles of Knowledge Representation and Reasoning, KR 2023, Rhodes, Greece, September 2-8, 2023, P. Marquis, T. C. Son, and G. Kern-Isberner (Eds.),  pp. 374–383.  External Links: [Link](https://doi.org/10.24963/kr.2023/37), [Document](https://dx.doi.org/10.24963/KR.2023/37) Cited by: §2. 
  * [16] A. Jacovi, A. Wang, C. Alberti, C. Tao, J. Lipovetz, K. Olszewska, L. Haas, M. Liu, N. Keating, A. Bloniarz, C. Saroufim, C. Fry, D. Marcus, D. Kukliansky, G. S. Tomar, J. Swirhun, J. Xing, L. Wang, M. Gurumurthy, M. Aaron, M. Ambar, R. Fellinger, R. Wang, Z. Zhang, S. Goldshtein, and D. Das (2025) The FACTS grounding leaderboard: benchmarking llms’ ability to ground responses to long-form input.  CoRR abs/2501.03200.  External Links: [Link](https://doi.org/10.48550/arXiv.2501.03200), [Document](https://dx.doi.org/10.48550/ARXIV.2501.03200), 2501.03200 Cited by: §0.A.2, §2, §4.1, Table 1, Table 1, Table 1. 
  * [17] A. Q. Jiang, S. Welleck, J. P. Zhou, T. Lacroix, J. Liu, W. Li, M. Jamnik, G. Lample, and Y. Wu (2023) Draft, sketch, and prove: guiding formal theorem provers with informal proofs.  In The Eleventh International Conference on Learning Representations, ICLR 2023, Kigali, Rwanda, May 1-5, 2023,  External Links: [Link](https://openreview.net/forum?id=SMa9EAovKMC) Cited by: §2. 
  * [18] B. Labs (2024) Bespoke-minicheck-7b.  External Links: [Link](https://huggingface.co/bespokelabs/Bespoke-MiniCheck-7B) Cited by: §0.A.2, §4.1, Table 1. 
  * [19] M. Levy, A. Jacoby, and Y. Goldberg (2024) Same task, more tokens: the impact of input length on the reasoning performance of large language models.  In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2024, Bangkok, Thailand, August 11-16, 2024, L. Ku, A. Martins, and V. Srikumar (Eds.),  pp. 15339–15353.  External Links: [Link](https://doi.org/10.18653/v1/2024.acl-long.818), [Document](https://dx.doi.org/10.18653/V1/2024.ACL-LONG.818) Cited by: §3.1. 
  * [20] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis, W. Yih, T. Rocktäschel, S. Riedel, and D. Kiela (2021) Retrieval-augmented generation for knowledge-intensive nlp tasks.  External Links: [Link](https://arxiv.org/abs/2005.11401) Cited by: §1. 
  * [21] T. Liu, W. Xu, W. Huang, Y. Zeng, J. Wang, X. Wang, H. Yang, and J. Li (2025) Logic-of-thought: injecting logic into contexts for full reasoning in large language models.  In Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers), L. Chiruzzo, A. Ritter, and L. Wang (Eds.),  Albuquerque, New Mexico, pp. 10168–10185.  External Links: [Document](https://dx.doi.org/10.18653/v1/2025.naacl-long.510), ISBN 979-8-89176-189-6, [Link](https://aclanthology.org/2025.naacl-long.510/) Cited by: §2. 
  * [22] P. Manakul, A. Liusie, and M. J. F. Gales (2023) SelfCheckGPT: zero-resource black-box hallucination detection for generative large language models.  In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, EMNLP 2023, Singapore, December 6-10, 2023, H. Bouamor, J. Pino, and K. Bali (Eds.),  pp. 9004–9017.  External Links: [Link](https://doi.org/10.18653/v1/2023.emnlp-main.557), [Document](https://dx.doi.org/10.18653/V1/2023.EMNLP-MAIN.557) Cited by: §0.A.2, §2, §4.1, Table 1. 
  * [23] W. McCune (2005) Release of prover9.  In Mile high conference on quasigroups, loops and nonassociative systems, Denver, Colorado,  Cited by: §2. 
  * [24] D. Merigoux, N. Chataing, and J. Protzenko (2021) Catala: a programming language for the law.  Proc. ACM Program. Lang. 5 (ICFP), pp. 1–29.  External Links: [Link](https://doi.org/10.1145/3473582), [Document](https://dx.doi.org/10.1145/3473582) Cited by: §2. 
  * [25] T. Olausson, A. Gu, B. Lipkin, C. Zhang, A. Solar-Lezama, J. Tenenbaum, and R. Levy (2023) LINC: a neurosymbolic approach for logical reasoning by combining language models with first-order logic provers.  In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing, H. Bouamor, J. Pino, and K. Bali (Eds.),  Singapore, pp. 5153–5176.  External Links: [Document](https://dx.doi.org/10.18653/v1/2023.emnlp-main.313), [Link](https://aclanthology.org/2023.emnlp-main.313/) Cited by: §2, §4.1, §4.1, Table 1. 
  * [26] L. Pan, A. Albalak, X. Wang, and W. Wang (2023) Logic-LM: empowering large language models with symbolic solvers for faithful logical reasoning.  In Findings of the Association for Computational Linguistics: EMNLP 2023, H. Bouamor, J. Pino, and K. Bali (Eds.),  Singapore, pp. 3806–3824.  External Links: [Document](https://dx.doi.org/10.18653/v1/2023.findings-emnlp.248), [Link](https://aclanthology.org/2023.findings-emnlp.248/) Cited by: §0.A.2, §2, §4.1, Table 1. 
  * [27] PwC Australia (2026) Operationalising responsible AI in education: automated reasoning and deterministic guardrails on AWS.  Note: <https://www.pwc.com.au/alliances/amazon-web-services/operationalising-responsible-ai-in-education.html>Accessed: 2026-05-01 Cited by: §5. 
  * [28] M. A. Rajeev, R. Ramamurthy, P. Trivedi, V. Yadav, O. Bamgbose, S. T. Madhusudhan, J. Zou, and N. Rajani (2025) Cats confuse reasoning LLM: query agnostic adversarial triggers for reasoning models.  CoRR abs/2503.01781.  External Links: [Link](https://doi.org/10.48550/arXiv.2503.01781), [Document](https://dx.doi.org/10.48550/ARXIV.2503.01781), 2503.01781 Cited by: §3.1. 
  * [29] J. A. Robinson and A. Voronkov (Eds.) (2001) Handbook of automated reasoning (in 2 volumes).  Elsevier and MIT Press.  External Links: [Link](https://www.sciencedirect.com/book/9780444508133/handbook-of-automated-reasoning), ISBN 0-444-50813-9 Cited by: §1. 
  * [30] H. Ryu, G. Kim, H. S. Lee, and E. Yang (2025) Divide and translate: compositional first-order logic translation and verification for complex logical reasoning.  In The Thirteenth International Conference on Learning Representations, ICLR 2025, Singapore, April 24-28, 2025,  External Links: [Link](https://openreview.net/forum?id=09FiNmvNMw) Cited by: §2. 
  * [31] H. Sun, W. W. Cohen, and R. Salakhutdinov (2022) ConditionalQA: A complex reading comprehension dataset with conditional answers.  In Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), ACL 2022, Dublin, Ireland, May 22-27, 2022, S. Muresan, P. Nakov, and A. Villavicencio (Eds.),  pp. 3627–3637.  External Links: [Link](https://doi.org/10.186
