URL: https://arxiv.org/html/2311.01740v2 | FULL FETCH | 2026-09-24T01:46:15Z
warning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
URL: https://arxiv.org/html/2311.01740v2
Type: HTML
Length: 63885 chars (truncated)

--- Content ---

##### Report GitHub Issue

×

Title:

Content selection saved. Describe the issue below:

Description:

Submit without GitHub Submit in GitHub

arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[ Back to arXiv ](/)

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) Report Issue [ Back to Abstract ](/abs/2311.01740v2 "Back to abstract page") [ Download PDF](/pdf/2311.01740v2 "Download PDF") [ ](javascript:toggleNavTOC\(\); "Toggle navigation") [ ](javascript:toggleReadingMode\(\); "Disable reading mode, show header and footer")

  1. Abstract
  2. 1 Introduction
     1. Key Observations.
     2. Proposed Approach.
     3. Effectiveness of SAC3.
  3. 2 Related Work
     1. Hallucination in LMs.
     2. Consistency Evaluation of LMs.
  4. 3 Self-consistency Limitations in Factuality Assessment
  5. 4 SAC3 : Semantic-Aware Cross-check Consistency
     1. 4.1 Stage 1: Question-level Cross-checking via Semantically Equivalent Perturbations
     2. 4.2 Stage 2: Model-level Cross-check with Additional Verifier LM
     3. 4.3 Stage 3: Consistency Score Calculation
        1. 4.3.1 Semantic-aware Consistency Check of QA Pairs
        2. 4.3.2 Self-checking Consistency (SC2) Score
        3. 4.3.3 Question-level Consistency (SAC3-Q) Score
        4. 4.3.4 Model-level Consistency (SAC3-M & SAC3-QM) Score
        5. 4.3.5 Final Score and Model Confidence
  6. 5 Data and Annotation
  7. 6 Experiments
     1. 6.1 Experimental Setup
        1. Evaluation Models.
        2. Implementation Details.
     2. 6.2 Evaluation Results
        1. 6.2.1 Classification QA
           1. Balanced Dataset.
           2. Unbalanced Dataset.
           3. Impact of Threshold.
           4. Why Does Self-checking Fail?
        2. 6.2.2 Open-domain Generation QA
           1. Effect of Verifier LM Weight.
           2. Effect of the Number of Perturbed Questions.
           3. Effect of the Model Type.
           4. Computational Cost.
  8. 7 Conclusion and Discussion
  9. References
  10. A Factuality Assessment of LLMs
     1. A.1 Background
     2. A.2 Black-box Assessment via Checking Consistency in Sampled Responses
  11. B Complete Prompts
  12. C Additional Details and Discussions
     1. C.1 Computational Cost
     2. C.2 Semantic Consistency Checking
     3. C.3 Data Annotations
  13. D Additional Examples



[ License: CC BY 4.0 ](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2311.01740v2 [cs.CL] 18 Feb 2024

# SAC3: Reliable Hallucination Detection in Black-Box Language Models via Semantic-aware Cross-check Consistency

Jiaxin Zhang  Affiliation: Intuit AI Research  Email: [jiaxinzhang@intuit.com](mailto:) Zhuohang Li  Affiliation: Vanderbilt University  Email: [kamalikadas@intuit.com](mailto:) Kamalika Das  Affiliation: Intuit AI Research  Email: [sricharankumar@intuit.com](mailto:) Bradley Malin  Affiliation: Vanderbilt University  Affiliation: Vanderbilt University Medical Center  Email: [zhuohang.li@vanderbilt.edu](mailto:) Sricharan Kumar  Affiliation: Intuit AI Research  Email: [b.malin@vanderbilt.edu](mailto:)

###### Abstract

Hallucination detection is a critical step toward understanding the trustworthiness of modern language models (LMs). To achieve this goal, we re-examine existing detection approaches based on the self-consistency of LMs and uncover two types of hallucinations resulting from 1) question-level and 2) model-level, which cannot be effectively identified through self-consistency check alone. Building upon this discovery, we propose a novel sampling-based method, i.e., semantic-aware cross-check consistency (SAC3) that expands on the principle of self-consistency checking. Our SAC3 approach incorporates additional mechanisms to detect both question-level and model-level hallucinations by leveraging advances including semantically equivalent question perturbation and cross-model response consistency checking. Through extensive and systematic empirical analysis, we demonstrate that SAC3 outperforms the state of the art in detecting both non-factual and factual statements across multiple question-answering and open-domain generation benchmarks.11 1 All resources are available at <https://github.com/intuit/sac3>.

## 1 Introduction

Large-scale pre-trained language models (LMs) have demonstrated exceptional adaptability across a diverse array of natural language tasks that require generating open-ended responses based on user prompt comprehension Zhao et al. (2023). However, prominent LMs like GPT Brown et al. (2020) and PaLM Chowdhery et al. (2022), often exhibit a tendency to produce exceedingly confident, yet erroneous, assertions commonly referred to as hallucinations. This phenomenon significantly impedes their applicability in domains where factual accuracy is of utmost importance.

Hallucinations can be detected through the assistance of metrics that capture the uncertainty about the output sequences. However, these metrics require access to token-level log probabilities, which are not available in commercial black-box LMs like ChatGPT or Bard that only offer limited API access. To overcome this limitation, recent studies explore sampling-based approaches for approximating uncertainty estimation Lin et al. (2023) through establishing a connection between confidence and self-consistency Manakul et al. (2023); Mündler et al. (2023). The underlying premise of this principle is that LMs are more inclined to generate consistent responses when high probabilities are assigned to tokens in the answer, which, in turn, implies a level of factuality. In contrast, inconsistent responses are more likely to contain hallucinations. To operationalize this concept, current approaches are designed to sample multiple responses from the LMs for a given question and then compose a hallucination score for each sentence based on the level of response consistency.

Figure 1: Key observation: solely checking the self-consistency of LLMs is not sufficient for deciding factuality. Left: generated responses to the same question may be consistent but non-factual. Right: generated responses may be inconsistent with the original answer that is factually correct.

##### Key Observations.

In this work, we investigate the relationship between the self-consistency of LMs and the occurrence of hallucinations in a diverse range of tasks. Our investigation indicates that while self-inconsistency in LMs often coincides with hallucination, self-consistency does not necessarily guarantee factual answers, as shown in Figure 1. Our findings challenge the notion that self-consistency alone can serve as a reliable indicator of veracity, as it is demonstrated that LMs can exhibit various tiers of hallucination that elude detection through self-consistency checks. One such tier is question-level hallucination, where LMs consistently generate incorrect answers in response to specific questions (e.g., Table 1). We reveal that by reformulating the questions, it is possible to mitigate such instances of hallucinations. Additionally, our work further reveals the existence of model-level hallucinations, whereby different LMs show discrepancies in their propensity for hallucination. Surprisingly, we even observe cases where smaller LMs are capable of correctly answering questions for which larger LMs hallucinate. Together, these findings accentuate the need to consider model-specific characteristics when assessing the occurrence of hallucinations.

##### Proposed Approach.

Motivated by these observations, we introduce SAC3, a new sampling-based approach utilizing semantic-aware cross-check consistency to improve the detection of hallucinations in black-box LMs. An overview of our approach is provided in Fig. 2. To address question-level hallucination, we introduce a mechanism that perturbs semantically equivalent questions to evaluate the consistency of LMs’ responses across variants of the same question. By examining the generated answers to these perturbed questions, we are able to identify cases where the LM consistently provides incorrect responses to a specific question, which is indicative of a question-level hallucination. Furthermore, we address model-level hallucination by introducing cross-model response consistency checking, which involves comparing the responses of different LMs to the same set of questions. By identifying discrepancies between the responses of different models, we are able to pinpoint cases where certain models exhibit hallucinations while others provide correct answers. Integrating these cross-checking extensions into our approach significantly improves its ability to detect hallucinations that go beyond self-consistency, thereby providing a more comprehensive assessment of the presence of question-level and model-level hallucinations.

##### Effectiveness of SAC3.

We demonstrate the effectiveness of SAC3 in multiple classification and open-domain generation QA datasets. In the classification QA tasks, our approach achieves a high AUROC score of 99.4% and 97.0% respectively, which significantly outperforms the self-consistency baseline. In the case of open-domain generation QA tasks, our approach achieves an AUROC score of 88.0% and 77.2%, which substantially improves upon the self-consistency baseline by a large margin (+13.8%, and +6.7% respectively).

Method | Input | Model | Output |  Consistency | Factuality  
---|---|---|---|---|---  
Self- consistency | Q: ‘‘Is 3691 a prime number?’’ | Target |  ‘‘No, 3691 is not a prime number as it is divisible by 7 and 13.’’ | ✓ | ✗  
Q: ‘‘Is 3691 a prime number?’’ | Target |  ‘‘No, 3691 is not a prime number as it is divisible by 7 and 13.’’  
Q: ‘‘Is 3691 a prime number?’’ | Target |  ‘‘No, 3691 is not a prime number. It can be divided evenly by 7 and 19.’’  
Cross-Q consistency | Q1: ‘‘Is the number 3691 prime?’’ | Target | ‘‘Yes, the number 3691 is prime.’’ | ✗ | ✓  
Q2: ‘‘Are the only factors of 3691 itself and one?’’ | Target |  ‘‘Yes, the only factors of 3691 are itself and one.’’  
Q3: ‘‘Can 3691 only be divided by 1 and 3691?’’ | Target |  ‘‘Yes, 3691 is a prime number and can only be divided by 1 and 3691.’’  
Cross-M consistency | Q: ‘‘Is 3691 a prime number?’’ | Verifier |  ‘‘Yes, 3691 is a prime number.’’ | ✗ | ✓  
Cross-M & Q consistency | Q1: ‘‘Is the number 3691 prime?’’ | Verifier | ‘‘Yes.’’ |  ✗ |  ✓  
Q2: ‘‘Are the only factors of 3691 itself and one?’’ | Verifier | ‘‘Yes, the only factors of 3691 are 1 and itself.’’  
Q3: ‘‘Can 3691 only be divided by 1 and 3691?’’ | Verifier | ‘‘Yes, 3691 can only be divided by 1 and 3691.’’  
  
Table 1: An illustrative example of self-consistency, cross-question consistency, and cross-model consistency check. The original question and answer are ‘‘Is 3691 a prime number?’’ and ‘‘No, 3691 is not a prime number. It is divisible by 7 and 13’’, respectively. Each row presents a set of sampled QA pairs along with its consistency regarding the original answer, and the predicted factuality of the original answer.

## 2 Related Work

##### Hallucination in LMs.

The issue of hallucination in language models (LMs) has gained significant attention due to its negative impact on performance and the risks it introduces in various natural language processing (NLP) tasks, such as machine translation Zhou et al. (2020), summarization Cao et al. (2022), dialogue generation Das et al. (2023), and question answering Zhang et al. (2023a); Zheng et al. (2023b); Dhuliawala et al. (2023). Recent survey Ji et al. (2023); Zhang et al. (2023c); Ye et al. (2023) and evaluation benchmarks Liu et al. (2021); Li et al. (2023a); Yang et al. (2023) have highlighted the importance of addressing this issue. Previous research has explored hallucination evaluation using confidence-based approaches Xiao and Wang (2021); Varshney et al. (2023); Chen and Mueller (2023) that require access to token-level log probability Kuhn et al. (2023); Cole et al. (2023) or supervised tuning Agrawal et al. (2023); Li et al. (2023b) that relies on internal states of the LM. However, these methods may not be applicable when only API access to the LM is available Agrawal et al. (2023). Another approach involves retrieving knowledge from external databases to tackle hallucinations Ji et al. (2022); Zheng et al. (2023a); Peng et al. (2023); Zhang et al. (2023b). In contrast to these studies, our work focuses on detecting hallucinations in open-domain QA tasks using black-box LMs, without relying on external resources.

##### Consistency Evaluation of LMs.

An essential characteristic of logically valid intelligent systems is self-consistency, which entails that no two statements provided by the system contradict each other. Self-consistency is defined by Elazar et al. (2021) as the invariance of an LM’s responses across various types of semantics-preserving prompt transformations. This definition is further enriched by multiple other consistency categories proposed by Jang et al. (2022). Wang et al. (2022) demonstrates that self-consistency can significantly enhance the chain of thought reasoning in LMs. Without self-consistency, it becomes challenging to regard LMs as reliable or trustworthy systems. Recent studies employ self-consistency to detect hallucinations based on pretrained LMs Manakul et al. (2023) and instruction-tuned LMs Mündler et al. (2023). Although these methods exhibit promising accuracy on several specific tasks, potential failures Chen et al. (2023) of self-consistency are overlooked in the current settings, as existing LMs frequently provide inconsistent responses to questions Mitchell et al. (2022) and factual knowledge inquiries Elazar et al. (2021); Tam et al. (2023); Gekhman et al. (2023). Our work addresses these concerns by introducing a cross-check consistency approach, aiming to bridge the gap between self-consistency and factual assessment.

## 3 Self-consistency Limitations in Factuality Assessment

The essential assumption of self-consistency in factuality assessment is that if the LM has the knowledge of the concept, responses sampled from its output distribution, should be similar and consistent; conversely, if the LM lacks corresponding knowledge, the sampled responses would contain hallucinated facts that are diverged and contradictory. Although this assumption may seem reasonable, it does not always hold in practice (more details are provided in the Appendix A). Specifically, we argue that solely checking the LM’s self-consistency is insufficient for detecting hallucination or verifying factuality under the following two circumstances:

1\. LMs may produce consistently hallucinated facts. We observe that for certain questions, LMs may output consistently wrong answers. For instance, as shown in Fig. 1, when prompted with the question ‘‘Is pi smaller than 3.2?’’, ChatGPT consistently generates incorrect answers. In this case, where the generated responses are consistent but non-factual, solely relying on self-consistency checking of a single model would yield false negative hallucination detection results.

2\. Even in cases when LMs generate factual statements in their original response, the stochastic sampled responses may lack veracity. For example, the original answer (Answer 1) of ChatGPT under zero temperature is correct regarding the senator search question as shown in Fig. 1. However, when sampled with a higher temperature, ChatGPT generates multiple incorrect responses (Answer 2 and Answer mm). In this scenario, where the sampled responses are inconsistent and disagree with the original response which itself is factually correct, methods that rely solely on model self-checking would produce false positives.

In summary, although the inconsistency of sampled responses has been empirically demonstrated to be correlated with hallucinated facts on certain tasks, in general, self-consistency is neither necessary nor sufficient to verify the veracity of large LMs’ statements. Therefore, methods based solely on self-consistency checking may not be able to accurately detect hallucinations in complex QA and open-domain generation tasks, which motivates us to design a more reliable and robust factuality assessment method that extends this idea.

Figure 2: Overview of the proposed semantic-aware cross-check consistency (SAC3) method.

## 4 SAC3 : Semantic-Aware Cross-check Consistency

This section describes the proposed semantic-aware cross-check consistency approach, a high-level overview of which is provided in Fig. 1. Additionally, an illustrative example of each component is presented in Table 1. Here, we walk through each component in detail.

### 4.1 Stage 1: Question-level Cross-checking via Semantically Equivalent Perturbations

Contrary to existing techniques that assess semantic equivalence through entailment or paraphrasing, our approach involves rephrasing the input query by generating alternative inputs that preserve semantic equivalence, i.e., semantically equivalent input perturbation. To achieve this, we leverage advances in LLM prompting. Starting with a queried input 𝒙0\boldsymbol{x}_{0}, we acquire a set of kk semantically equivalent inputs {𝒙1,𝒙2,…,𝒙k}\\{\boldsymbol{x}_{1},\boldsymbol{x}_{2},...,\boldsymbol{x}_{k}\\} through the prompt: ‘‘For the question [QUERIED QUESTION], provide kk semantically equivalent questions’’.

To ensure the quality of the generated inputs in this step, we further double-check the semantic equivalence between the generated inputs {𝒙1,𝒙2,…,𝒙k}\\{\boldsymbol{x}_{1},\boldsymbol{x}_{2},...,\boldsymbol{x}_{k}\\} and the queried input 𝒙0\boldsymbol{x}_{0} in a pair-wise manner using the prompt ‘‘Are the following two inputs semantically equivalent? [QUERIED INPUT] [GENERATED INPUT]’’ and filtering out the inputs that do not share the same semantic meaning as the original input. The complete prompt templates used in this work are provided in the Appendix B.

### 4.2 Stage 2: Model-level Cross-check with Additional Verifier LM

Let 𝒔0\boldsymbol{s}_{0} denote the original response from a target LM 𝒯\mathcal{T} based on a given query 𝒙0\boldsymbol{x}_{0}. Our objective is to detect whether 𝒔0\boldsymbol{s}_{0} is hallucinated by sampling responses from the predictive distribution of 𝒯\mathcal{T}. To avoid model-level hallucination, we introduce an additional verifier LM denoted as 𝒱\mathcal{V} for model-level cross-checking. We define the responses from both models as:

| 𝒔𝒯j=𝒯(𝒙j),𝒔𝒱j=𝒱(𝒙j),j=1,…,k,\boldsymbol{s}_{\mathcal{T}_{j}}=\mathcal{T}(\boldsymbol{x}_{j}),\ \boldsymbol{s}_{\mathcal{V}_{j}}=\mathcal{V}(\boldsymbol{x}_{j}),\ j=1,...,k, |  | (1)  
---|---|---|---  
  
where kk is the length of the generated semantically equivalent inputs {𝒙1,𝒙2,…,𝒙k}\\{\boldsymbol{x}_{1},\boldsymbol{x}_{2},...,\boldsymbol{x}_{k}\\} in stage 1. To assess the factuality of 𝒙0\boldsymbol{x}_{0}, the self-checking mechanism operates by drawing a set of nsn_{s} stochastic response samples from the target LM: 𝒮𝒯0={𝒔𝒯01,𝒔𝒯02,…,𝒔𝒯0ns}\mathcal{S}_{\mathcal{T}_{0}}=\\{\boldsymbol{s}_{\mathcal{T}_{0}}^{1},\boldsymbol{s}_{\mathcal{T}_{0}}^{2},...,\boldsymbol{s}_{\mathcal{T}_{0}}^{n_{s}}\\}. Similarly, we can apply the same self-checking mechanism to the verifier LM to generate another set of nmn_{m} responses: 𝒮𝒱0={𝒔𝒱01,𝒔𝒱02,…,𝒔𝒱0nm}\mathcal{S}_{\mathcal{V}_{0}}=\\{\boldsymbol{s}_{\mathcal{V}_{0}}^{1},\boldsymbol{s}_{\mathcal{V}_{0}}^{2},...,\boldsymbol{s}_{\mathcal{V}_{0}}^{n_{m}}\\}. To perform question-level cross-check, for each perturbed input 𝒙k\boldsymbol{x}_{k}, we generate nqn_{q} sampled response sequences 𝒮𝒯k={𝒔𝒯k1,𝒔𝒯k2,…,𝒔𝒯knq}\mathcal{S}_{\mathcal{T}_{k}}=\\{\boldsymbol{s}_{\mathcal{T}_{k}}^{1},\boldsymbol{s}_{\mathcal{T}_{k}}^{2},...,\boldsymbol{s}_{\mathcal{T}_{k}}^{n_{q}}\\} from the target LM 𝒯\mathcal{T} and nq​mn_{qm} sampled responses 𝒮𝒱k={𝒔𝒱k1,𝒔𝒱k2,…,𝒔𝒱knq​m}\mathcal{S}_{\mathcal{V}_{k}}=\\{\boldsymbol{s}_{\mathcal{V}_{k}}^{1},\boldsymbol{s}_{\mathcal{V}_{k}}^{2},...,\boldsymbol{s}_{\mathcal{V}_{k}}^{n_{qm}}\\} from the verifier LM 𝒱\mathcal{V}.

Finally, we collect the total sampled sets 𝒮={𝒮𝒯0,𝒮𝒱0,𝒮𝒯k,𝒮𝒱k}\mathcal{S}=\\{\mathcal{S}_{\mathcal{T}_{0}},\mathcal{S}_{\mathcal{V}_{0}},\mathcal{S}_{\mathcal{T}_{k}},\mathcal{S}_{\mathcal{V}_{k}}\\} by combining all samples drawn from self-checking and cross-checking, which will be used next for calculating a consistency score.

### 4.3 Stage 3: Consistency Score Calculation

This stage uses the generated sample sets in all previous stages to calculate a numerical consistency score that captures the question-level and model-level cross-checking paradigm.

#### 4.3.1 Semantic-aware Consistency Check of QA Pairs

Most of the existing works mainly focus on examining the consistency of LM outputs while ignoring the effect of the inputs. However, in QA tasks, it is important to consider both inputs and outputs when measuring semantic equivalence, as the same question can be rephrased in many ways. Although the answers to these questions (e.g., ‘‘no’’ and ‘‘yes’’) may not be lexically equivalent, the QA pairs as a whole can be semantically equivalent. In light of this, we propose to check the semantic consistency of the QA pairs instead of the answer only.

#### 4.3.2 Self-checking Consistency (SC2) Score

Let 𝒞⁡(⋅,⋅)\mathcal{C}(\cdot,\cdot) denote a semantic equivalence checking operator that takes two QA pairs as inputs. The operator 𝒞\mathcal{C} returns ‘‘Yes’’ if the two QA pairs are semantically equivalent, and ‘‘No’’ otherwise. This operator should be reflexive, symmetric, and transitive. We implement the checking operator using an LM by leveraging the prompt: ‘‘Are the following two Question-Answering (QA) pairs semantically equivalent? [QA PAIR 1] [QA PAIR 2]’’. We then map the best guess to a numerical semantic equivalent score: {‘‘Yes’’ →\rightarrow 0.0, ‘‘No’’ →\rightarrow 1.0}. We use 𝒫0=(𝒙0,𝒔0)\mathcal{P}_{0}=(\boldsymbol{x}_{0},\boldsymbol{s}_{0}) to denote the original QA pair. The self-checking score 𝒵SC2\mathcal{Z}_{\texttt{SC${}^{2}$}} of the target LM 𝒯\mathcal{T} can be calculated by

| 𝒵SC2=1ns​∑i=1ns𝒞⁡(𝒫0,𝒫𝒮𝒯0i),\mathcal{Z}_{\texttt{SC${}^{2}$}}=\frac{1}{n_{s}}\sum_{i=1}^{n_{s}}\mathcal{C}(\mathcal{P}_{0},\mathcal{P}_{\mathcal{S}_{\mathcal{T}_{0}}}^{i}), |  | (2)  
---|---|---|---  
  
where 𝒫𝒮𝒯0={(𝒙0,𝒔𝒯01),…,(𝒙0,𝒔𝒯0ns)}\mathcal{P}_{\mathcal{S}_{\mathcal{T}_{0}}}=\\{(\boldsymbol{x}_{0},\boldsymbol{s}_{\mathcal{T}_{0}}^{1}),...,(\boldsymbol{x}_{0},\boldsymbol{s}_{\mathcal{T}_{0}}^{n_{s}})\\} represents the QA pairs generated in the self-checking scenario.

#### 4.3.3 Question-level Consistency (SAC3-Q) Score

Besides self-checking the original question 𝒙0\boldsymbol{x}_{0}, SAC3 further assesses cross-check consistency of perturbed questions {𝒙1,𝒙2,…,𝒙k}\\{\boldsymbol{x}_{1},\boldsymbol{x}_{2},...,\boldsymbol{x}_{k}\\}. The corresponding QA pairs compose a two-dimensional matrix, where each row corresponds to a perturbed question (kk in total), and each column corresponds to a sampled response (nqn_{q} in total):

| 𝒫𝒮𝒯ji=[(𝒙1,𝒮𝒯11)...(𝒙1,𝒮𝒯1nq).........(𝒙k,𝒮𝒯k1)...(𝒙k,𝒮𝒯knq)].\mathcal{P}_{\mathcal{S}_{\mathcal{T}_{j}}}^{i}=\begin{bmatrix}(\boldsymbol{x}_{1},\mathcal{S}_{\mathcal{T}_{1}}^{1})&...&(\boldsymbol{x}_{1},\mathcal{S}_{\mathcal{T}_{1}}^{n_{q}})\\\ ...&...&...\\\ (\boldsymbol{x}_{k},\mathcal{S}_{\mathcal{T}_{k}}^{1})&...&(\boldsymbol{x}_{k},\mathcal{S}_{\mathcal{T}_{k}}^{n_{q}})\end{bmatrix}. |  | (3)  
---|---|---|---  
  
Therefore, the question-level cross-checking consistency score 𝒵SAC3-Q\mathcal{Z}_{\texttt{SAC${}^{3}$-Q}} can be obtained by

| 𝒵SAC3-Q=1nq⋅k​∑i=1nq∑j=1k𝒞⁡(𝒫0,𝒫𝒮𝒯ji).\mathcal{Z}_{\texttt{SAC${}^{3}$-Q}}=\frac{1}{n_{q}\cdot k}\sum_{i=1}^{n_{q}}\sum_{j=1}^{k}\mathcal{C}(\mathcal{P}_{0},\mathcal{P}_{\mathcal{S}_{\mathcal{T}_{j}}}^{i}). |  | (4)  
---|---|---|---  
  
#### 4.3.4 Model-level Consistency (SAC3-M & SAC3-QM) Score

In addition to the question-level score, a model-level cross-check score is calculated by performing cross-model checking and cross-question checking using the verifier LM 𝒱\mathcal{V}. Specifically, for the original question 𝒙0\boldsymbol{x}_{0}, the model-level cross-checking consistency score 𝒵SAC3-M\mathcal{Z}_{\texttt{SAC${}^{3}$-M}} is computed by

| 𝒵SAC3-M=1nm​∑i=1nm𝒞⁡(𝒫0,𝒫𝒮𝒱0i),\mathcal{Z}_{\texttt{SAC${}^{3}$-M}}=\frac{1}{n_{m}}\sum_{i=1}^{n_{m}}\mathcal{C}(\mathcal{P}_{0},\mathcal{P}_{\mathcal{S}_{\mathcal{V}_{0}}}^{i}), |  | (5)  
---|---|---|---  
  
where 𝒫𝒮𝒱0={(𝒙0,𝒔𝒱01),…,(𝒙0,𝒔𝒱0nm)}\mathcal{P}_{\mathcal{S}_{\mathcal{V}_{0}}}=\\{(\boldsymbol{x}_{0},\boldsymbol{s}_{\mathcal{V}_{0}}^{1}),...,(\boldsymbol{x}_{0},\boldsymbol{s}_{\mathcal{V}_{0}}^{n_{m}})\\} is the QA pairs generated by the verified LM 𝒱\mathcal{V}.

The cross-question consistency score on the verifier LM is computed on the QA pairs produced by 𝒱\mathcal{V}:

| 𝒫𝒮𝒱ji=[(𝒙1,𝒮𝒱11)...(𝒙1,𝒮𝒱1nq​m).........(𝒙k,𝒮𝒱k1)...(𝒙k,𝒮𝒱knq​m)].\mathcal{P}_{\mathcal{S}_{\mathcal{V}_{j}}}^{i}=\begin{bmatrix}(\boldsymbol{x}_{1},\mathcal{S}_{\mathcal{V}_{1}}^{1})&...&(\boldsymbol{x}_{1},\mathcal{S}_{\mathcal{V}_{1}}^{n_{qm}})\\\ ...&...&...\\\ (\boldsymbol{x}_{k},\mathcal{S}_{\mathcal{V}_{k}}^{1})&...&(\boldsymbol{x}_{k},\mathcal{S}_{\mathcal{V}_{k}}^{n_{qm}})\end{bmatrix}. |  | (6)  
---|---|---|---  
  
The cross-model cross-question consistency score can thus be obtained through

| 𝒵SAC3-QM=1nq​m⋅k​∑i=1nq​m∑j=1k𝒞⁡(𝒫0,𝒫𝒮𝒱ji).\mathcal{Z}_{\texttt{SAC${}^{3}$-QM}}=\frac{1}{n_{qm}\cdot k}\sum_{i=1}^{n_{qm}}\sum_{j=1}^{k}\mathcal{C}(\mathcal{P}_{0},\mathcal{P}_{\mathcal{S}_{\mathcal{V}_{j}}}^{i}). |  | (7)  
---|---|---|---  
  
#### 4.3.5 Final Score and Model Confidence

The different variants of SAC3 capture different aspects of the uncertainty about the original response and should complement each other. We thus consider a combination of all variants including SAC3-Q , SAC3-M , SAC3-QM as the final score:

| 𝒵SAC3-all=𝒵SAC3-Q+λ⁡(𝒵SAC3-M+𝒵SAC3-QM),\mathcal{Z}_{\texttt{SAC${}^{3}$-all}}=\mathcal{Z}_{\texttt{SAC${}^{3}$-Q}}+\lambda(\mathcal{Z}_{\texttt{SAC${}^{3}$-M}}+\mathcal{Z}_{\texttt{SAC${}^{3}$-QM}}), |  | (8)  
---|---|---|---  
  
where λ\lambda is a weight factor for the verifier LM. Unless mentioned otherwise, we use λ=1\lambda=1 by default in our experiments. In practice, as the computation of each component is independent, they can be computed in parallel to reduce latency. The detection prediction is made by comparing the final score with a preset threshold. In addition to the computed score, we also ask the target LM to generate a verbalized confidence score Tian et al. (2023) along with its prediction when checking the semantic equivalence of QA pairs. More discussions are offered in the Appendix C.2.

## 5 Data and Annotation

We evaluate our hallucination detection approach on two categories of QA tasks, namely, classification QA and generation QA, with each category containing two datasets. Following prior work Zhang et al. (2023a), we use the following two binary classification datasets for evaluation on the classification QA task:

  * •

Prime number: this dataset contains 500 questions that query the primality of a randomly chosen prime number between 1,000 and 20,000, where the factual answer is always ‘‘Yes’’. The synthesized hallucinated answers are ‘‘No, it is not a prime number’’.

  * •

Senator search: the dataset consists of 500 questions that follow the following template: ‘‘Was there ever a US senator that represented the state of [US STATE NAME] and whose alma mater was [US COLLEGE NAME]?’’. The factual answer is always ‘‘No’’. We also generate hallucinated answers: ‘‘Yes, there was a US senator that represented the state of [US STATE NAME] and whose alma mater was [US COLLEGE NAME].’’.




As for the generation QA tasks, we take questions from the following two open-domain QA datasets and generate answers using LLMs. Then we manually annotate the factuality of the answers following previous work Li et al. (2023a).

  * •

HotpotQA-halu: We randomly sample 250 examples from the training set of HotpotQA Yang et al. (2018) and generate hallucinated answers drawn from gpt-3.5-turbo. Then we manually annotate the answers by comparing the ground truth and knowledge.

  * •

NQ-open-halu: Natural Questions (NQ)-open Lee et al. (2019) is a more challenging open domain QA benchmark Kwiatkowski et al. (2019). We use the same setting as HotpotQA-halu to create a small-scale dataset that consists of 250 non-factual and factual examples with manual annotations.




Please find more relevant details about data annotations in the Appendix C.3.

## 6 Experiments

### 6.1 Experimental Setup

##### Evaluation Models.

We use gpt-3.5-turbo from OpenAI as the target LM for our experiment. The verifier LM is chosen from the following two models: (1) Falcon-7b-instruct Almazrouei et al. (2023): an open-source causal decoder-only model built by TII that is trained on 1,500B tokens of RefinedWeb Penedo et al. (2023) and further enhanced using the curated corpora; and (2) Guanaco-33b: an open-source instruction-following models through QLoRA Dettmers et al. (2023) tuning of LLaMA Touvron et al. (2023) base model on the OASST1 dataset.

##### Implementation Details.

The evaluation is conducted using Azure OpenAI API. When performing semantic perturbations and consistency checking, we set the temperature to 0.0 to get deterministic high-quality outputs. Given a specific input query, we generate k=10k=10 semantically equivalent inputs using the prompt described in Section 4.1. For the self-checking-based method SC2 , we follow prior work Manakul et al. (2023) to set the temperature to 1.0 and generate ns=10n_{s}=10 stochastic samples. For SAC3-Q and SAC3-QM , we set nq=nq​m=1n_{q}=n_{qm}=1 to reduce computational cost. To further reduce the inference cost, we set nm=1n_{m}=1 by default and combine SAC3-M with SAC3-QM to report the model-level results. We use hallucination detection accuracy and area under the ROC curve (AUROC) to evaluate the performance. In addition to the estimated hallucination score, we also show the verbalized probabilities Tian et al. (2023) from the target LM for comparison. We execute all experiments on 8 NVIDIA V100 32G GPUs.

Method | Prime number | Senator search  
---|---|---  
Score | Confidence | Score | Confidence  
SC2 (gpt-3.5-turbo) | 65.9 | 67.5 | 56.1 | 53.1  
SAC3-Q (gpt-3.5-turbo) | 99.4 | 99.7 | 99.7 | 99.7  
  
Table 2: AUROC on classification QA tasks with 50% hallucinated samples and 50% factual samples.

### 6.2 Evaluation Results

#### 6.2.1 Classification QA

##### Balanced Dataset.

We first experiment on balanced datasets with 50% hallucinated samples and 50% factual samples. Table 2 compares the detection performance of SC2 and SAC3-Q in terms of AUROC and verbalized confidence score. We observe that self-checking (SC2) performs poorly on both datasets, with a low AUROC of 65.9%65.9\% and 56.1%56.1\%, respectively. Our question-level cross-checking (SAC3-Q) significantly outperforms the SC2 baseline achieving >99%>99\% AUROC on both datasets and is in line with the verbalized confidence score, confirming the effectiveness of cross-checking.

##### Unbalanced Dataset.

We further evaluate our method in a more challenging scenario where the dataset only contains hallucinated samples. Table 3 presents the accuracy of detecting hallucinated samples using a preset threshold of 0.5. In this case, the performance of self-check drops significantly to 48.2% and 29.6% respectively. SAC3-Q still outperforms SC2 by a large margin. The model-level cross-check with verifier LMs performs well in the prime number dataset but fails to accurately detect hallucination in the senator search dataset. This is because both verifier LMs refuse to answer a large portion of the questions on this dataset due to a lack of sufficient information. By combining the target LM, SAC3-all with Guanaco-33b achieves the highest detection accuracy compared to other baselines SC2 (+51.2%), SAC3-Q (+6.2%), and SAC3-QM (+ 5.0%).

Method | Prime number | Senator search  
---|---|---  
Score | Confidence | Score | Confidence  
SC2 (gpt-3.5-turbo) | 48.2 | 51.0 | 29.6 | 30.6  
SAC3-Q (gpt-3.5-turbo) | 93.2 | 96.4 | 97.0 | 97.4  
SAC3-QM (Falcon-7b) | 89.8 | 91.2 | 21.0 | 21.8  
SAC3-QM (Guanaco-33b) | 94.4 | 96.3 | 45.6 | 46.2  
SAC3-all (Falcon-7b) | 97.8 | 98.0 | 84.6 | 85.6  
SAC3-all (Guanaco-33b) | 99.4 | 99.4 | 85.6 | 86.7  
  
Table 3: Accuracy on classification QA tasks with 100% hallucinated samples (with the threshold set to 0.5).

##### Impact of Threshold.

Since the choice of threshold has a significant impact on the detection accuracy in the case where the dataset only contains positive (hallucinated) samples, we further experiment with different thresholds and present the results in Fig. 3. We observe that SAC3-Q and SAC3-all with Guanaco-33b are more robust against large threshold values and outperform SC2 in most cases.

Figure 3: Impact of threshold on detection accuracy.

##### Why Does Self-checking Fail?

To further understand why self-checking methods fail to detect some hallucinated responses, we visualize the distribution of consistency scores using histogram plots in Fig. 4. We observe that for SC2, a significant portion of hallucinated samples received highly consistent predictions. In other words, the target LM made consistently wrong predictions due to a lack of question and model diversity, which aligns with our analysis in Section 3. On the other hand, benefiting from the semantically equivalent question perturbation, SAC3-Q’s scores are more spread out in the inconsistent region, which helps to improve the effectiveness of detecting hallucinations by choosing a proper threshold.

Figure 4: Histogram of hallucination score.

#### 6.2.2 Open-domain Generation QA

Compared to the classification QA tasks, detecting hallucinations in open-domain generation QA tasks is more challenging. As shown in Table 4, SAC3-Q exhibits better AUROC than SC2 (+7%) in both datasets. Compared to SAC3-Q , SAC3-QM shows 6.7% improvement in the HotpotQA-halu dataset but is slightly worse in the NQ open dataset. SAC3-all leverages the advantages of question-level and model-level cross-checking and achieves consistently good performance in both datasets.

Method | HotpotQA-halu | NQ-open-halu  
---|---|---  
Score | Confidence | Score | Confidence  
SC2 (gpt-3.5-turbo) | 74.2 | 77.0 | 70.5 | 72.7  
SAC3-Q (gpt-3.5-turbo) | 81.3 | 81.4 | 77.2 | 78.5  
SAC3-QM (Falcon-7b) | 83.0 | 79.5 | 67.5 | 62.0  
SAC3-QM (Guanaco-33b) | 88.0 | 85.2 | 72.7 | 72.7  
SAC3-all (Falcon-7b) | 84.5 | 84.5 | 77.1 | 77.2  
SAC3-all (Guanaco-33b) | 87.0 | 86.8 | 77.2 | 77.8  
  
Table 4: AUROC on open-domain generation QA tasks.

##### Effect of Verifier LM Weight.

In our previous experiments, we assigned equal importance to the consistency score computed by the target and verifier LM. However, typically, the target LM and the verifier LM have different architectures and scales such that the user may have different levels of trust in their output truthfulness. This difference in trust can be incorporated by introducing a weight λ\lambda to the consistency score produced by the verifier LM. For instance, if the goal is to detect hallucination in a specialized domain and the verifier LM is a domain-specific model developed for this domain, we can assign a large weight to its scores (e.g., λ>1.0\lambda>1.0). In the general case, where the verifier LM is a small-sized open-source model, we can apply a small weight value (e.g., λ<1.0\lambda<1.0) to discount the influence of the verifier LM in the final score. Fig. 5 visualizes the effect of various weight factors on the generation QA datasets. We observe that SAC3-all with a higher weight would result in a larger advantage over SAC3-Q in the HotpotQA-halu task, where the verifier LM outperforms the target LM. On the contrary, in the NQ open task where the target LM shows competitive performance, a smaller weight would yield better results.

Figure 5: Effect of verifier LM weight on AUROC.

##### Effect of the Number of Perturbed Questions.

The performance of sampling-based methods is expected to improve as the sample size increases, at the cost of higher latency and computational cost. In Fig. 6, we study this trade-off by varying the number of perturbed questions kk from 2 to 10. We observe that the performance of SAC3 increases as more question samples are used but the performance gain gradually diminishes after using more than 5 question samples. This suggests that in practice we could use 2-4 question samples to achieve reasonably good performance at a low computational cost.

Figure 6: Performance of SAC3 with varying number of perturbed questions.

##### Effect of the Model Type.

Our proposed SAC3 framework does not restrict the type of LLM employed and can be naturally extended to various types of target LLMs. To verify this, in addition to GPT-3.5 (gpt-3.5-turbo), we conduct experiments using GPT-4 (gpt-4) and PaLM 2 (chat-bison) on the considered four datasets in the setting of the balanced dataset. The experimental results of comparing the proposed SAC3-Q with the SC2 baseline are summarized in Table 5. We observe that the proposed SAC3-Q consistently outperforms the SC2 baseline across all LLM variants.

Method |  | Prime  
---  
Number  
| Senator  
---  
Search  
| HotpotQA  
---  
-halu  
| NQ-open  
---  
-halu  
SC2 (gpt-3.5-turbo) | 48.2 | 29.6 | 74.2 | 70.5  
SC2 (gpt-4) | 38.3 | 18.4 | 79.7 | 76.3  
SC2 (chat-bison) | 26.9 | 19.2 | 75.8 | 67.9  
SAC3-Q (gpt-3.5-turbo) | 93.2 | 97.0 | 81.3 | 77.2  
SAC3-Q (gpt-4) | 91.1 | 61.6 | 87.2 | 82.9  
SAC3-Q (chat-bison) | 90.3 | 66.3 | 82.8 | 72.7  
  
Table 5: Accuracy of different LLMs (GPT-3.5, GPT-4, and PaLM 2) on classification and generation QA tasks.

##### Computational Cost.

We monitor the computational cost of our approach based on the number of model evaluations consumed by OpenAI API and open-source LLMs inference. Assuming the number of samples equals the number of perturbed questions, i.e., ns=nm=nq=nq​mn_{s}=n_{m}=n_{q}=n_{qm}, the cost of SC2 is nsn_{s} API calls, and our SAC3-all needs nsn_{s} target LM calls plus 2×ns2\times n_{s} verifier LM calls. Beyond the model evaluations, SAC3 may have additional costs from question perturbations and semantic equivalence checking via prompting. Additional discussions can be found in the Appendix C.1.

## 7 Conclusion and Discussion

We investigate the relationship between the self-consistency of LM and the factuality of the response and propose SAC3 as a robust hallucination detection approach for black-box LMs. Through extensive empirical analysis, our work highlights several findings. First, self-consistency checking alone is insufficient to effectively detect question-level and model-level hallucinations, where LMs generate consistently wrong responses to certain questions. Second, cross-checking between semantically equivalent questions can reduce the occurrence of persistent hallucinations, potentially by reducing question-level ambiguity. Third, there exists a model-level disparity in hallucinations, which we attribute to the inherent differences in LM capabilities originating from different training procedures and data. Thus, the verifier LM can be selected according to specific tasks to maximize detection accuracy. We believe that our work is an important step towards building reliable LLMs.

## Ethics Statement

This paper studies hallucination detection in LMs, which has significant broader impacts in the field of natural language processing (NLP) and helps to address ethical considerations regarding trustworthiness and reliability. The research outcome may contribute to the development of more accurate and reliable LMs by mitigating the risks of misinformation and biased outputs and promoting accountability and trust in AI systems.

## Limintations

Our current experiments focus on the question-answering setting. Further research is needed to assess the generalizability of the proposed framework and the accuracy of semantic equivalence checks on more complex tasks such as conversational or dialogue-based prompting. Additionally, it would be interesting to investigate the efficiency-utility trade-off: we expect increasing sample sizes to improve detection accuracy but may introduce additional cost and latency. Speeding up the implementation through parallelization is also worth exploring.

## References

  * Agrawal et al. (2023) Ayush Agrawal, Lester Mackey, and Adam Tauman Kalai. 2023.  Do language models know when they’re hallucinating references?  _arXiv preprint arXiv:2305.18248_. 
  * Almazrouei et al. (2023) Ebtesam Almazrouei, Hamza Alobeidli, Abdulaziz Alshamsi, Alessandro Cappelli, Ruxandra Cojocaru, Merouane Debbah, Etienne Goffinet, Daniel Heslow, Julien Launay, Quentin Malartic, Badreddine Noune, Baptiste Pannier, and Guilherme Penedo. 2023.  Falcon-40B: an open large language model with state-of-the-art performance. 
  * Brown et al. (2020) Tom Brown, Benjamin Mann, Nick Ryder, Melanie Subbiah, Jared D Kaplan, Prafulla Dhariwal, Arvind Neelakantan, Pranav Shyam, Girish Sastry, Amanda Askell, et al. 2020.  Language models are few-shot learners.  _Advances in neural information processing systems_ , 33:1877–1901. 
  * Cao et al. (2022) Meng Cao, Yue Dong, and Jackie Chi Kit Cheung. 2022.  Hallucinated but factual! inspecting the factuality of hallucinations in abstractive summarization.  In _Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)_ , pages 3340–3354. 
  * Chen et al. (2023) Angelica Chen, Jason Phang, Alicia Parrish, Vishakh Padmakumar, Chen Zhao, Samuel R Bowman, and Kyunghyun Cho. 2023.  Two failures of self-consistency in the multi-step reasoning of llms.  _arXiv preprint arXiv:2305.14279_. 
  * Chen and Mueller (2023) Jiuhai Chen and Jonas Mueller. 2023.  Quantifying uncertainty in answers from any language model via intrinsic and extrinsic confidence assessment.  _arXiv preprint arXiv:2308.16175_. 
  * Chowdhery et al. (2022) Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra, Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian Gehrmann, et al. 2022.  Palm: Scaling language modeling with pathways.  _arXiv preprint arXiv:2204.02311_. 
  * Cole et al. (2023) Jeremy R Cole, Michael JQ Zhang, Daniel Gillick, Julian Martin Eisenschlos, Bhuwan Dhingra, and Jacob Eisenstein. 2023.  Selectively answering ambiguous questions.  _arXiv preprint arXiv:2305.14613_. 
  * Das et al. (2023) Souvik Das, Sougata Saha, and Rohini K Srihari. 2023.  Diving deep into modes of fact hallucinations in dialogue systems.  _arXiv preprint arXiv:2301.04449_. 
  * Dettmers et al. (2023) Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, and Luke Zettlemoyer. 2023.  Qlora: Efficient finetuning of quantized llms.  _arXiv preprint arXiv:2305.14314_. 
  * Dhuliawala et al. (2023) Shehzaad Dhuliawala, Mojtaba Komeili, Jing Xu, Roberta Raileanu, Xian Li, Asli Celikyilmaz, and Jason Weston. 2023.  Chain-of-verification reduces hallucination in large language models.  _arXiv preprint arXiv:2309.11495_. 
  * Elazar et al. (2021) Yanai Elazar, Nora Kassner, Shauli Ravfogel, Abhilasha Ravichander, Eduard Hovy, Hinrich Schütze, and Yoav Goldberg. 2021.  Measuring and improving consistency in pretrained language models.  _Transactions of the Association for Computational Linguistics_ , 9:1012–1031. 
  * Gekhman et al. (2023) Zorik Gekhman, Jonathan Herzig, Roee Aharoni, Chen Elkind, and Idan Szpektor. 2023\.  Trueteacher: Learning factual consistency evaluation with large language models.  _arXiv preprint arXiv:2305.11171_. 
  * Jang et al. (2022) Myeongjun Jang, Deuk Sin Kwon, and Thomas Lukasiewicz. 2022.  Becel: Benchmark for consistency evaluation of language models.  In _Proceedings of the 29th International Conference on Computational Linguistics_ , pages 3680–3696. 
  * Ji et al. (2023) Ziwei Ji, Nayeon Lee, Rita Frieske, Tiezheng Yu, Dan Su, Yan Xu, Etsuko Ishii, Ye Jin Bang, Andrea Madotto, and Pascale Fung. 2023.  Survey of hallucination in natural language generation.  _ACM Computing Surveys_ , 55(12):1–38. 
  * Ji et al. (2022) Ziwei Ji, Zihan Liu, Nayeon Lee, Tiezheng Yu, Bryan Wilie, Min Zeng, and Pascale Fung. 2022.  Rho: Reducing hallucination in open-domain dialogues with knowledge grounding.  _arXiv preprint arXiv:2212.01588_. 
  * Kuhn et al. (2023) Lorenz Kuhn, Yarin Gal, and Sebastian Farquhar. 2023.  Semantic uncertainty: Linguistic invariances for uncertainty estimation in natural language generation.  _arXiv preprint arXiv:2302.09664_. 
  * Kwiatkowski et al. (2019) Tom Kwiatkowski, Jennimaria Palomaki, Olivia Redfield, Michael Collins, Ankur Parikh, Chris Alberti, Danielle Epstein, Illia Polosukhin, Jacob Devlin, Kenton Lee, et al. 2019.  Natural questions: a benchmark for question answering research.  _Transactions of the Association for Computational Linguistics_ , 7:453–466. 
  * Lee et al. (2019) Kenton Lee, Ming-Wei Chang, and Kristina Toutanova. 2019.  Latent retrieval for weakly supervised open domain question answering.  In _Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics_ , pages 6086–6096. 
  * Li et al. (2023a) Junyi Li, Xiaoxue Cheng, Wayne Xin Zhao, Jian-Yun Nie, and Ji-Rong Wen. 2023a.  Halueval: A large-scale hallucination evaluation benchmark for large language models.  _arXiv e-prints_ , pages arXiv–2305. 
  * Li et al. (2023b) Kenneth Li, Oam Patel, Fernanda Viégas, Hanspeter Pfister, and Martin Wattenberg. 2023b.  Inference-time intervention: Eliciting truthful answers from a language model.  _arXiv preprint arXiv:2306.03341_. 
  * Lin et al. (2023) Zhen Lin, Shubhendu Trivedi, and Jimeng Sun. 2023.  Generating with confidence: Uncertainty quantification for black-box large language models.  _arXiv preprint arXiv:2305.19187_. 
  * Liu et al. (2021) Tianyu Liu, Yizhe Zhang, Chris Brockett, Yi Mao, Zhifang Sui, Weizhu Chen, and Bill Dolan. 2021.  A token-level reference-free hallucination detection benchmark for free-form text generation.  _arXiv preprint arXiv:2104.08704_. 
  * Manakul et al. (2023) Potsawee Manakul, Adian Liusie, and Mark JF Gales. 2023.  Selfcheckgpt: Zero-resource black-box hallucination detection for generative large language models.  _arXiv preprint arXiv:2303.08896_. 
  * Mitchell et al. (2022) Eric Mitchell, Joseph J Noh, Siyan Li, William S Armstrong, Ananth Agarwal, Patrick Liu, Chelsea Finn, and Christopher D Manning. 2022.  Enhancing self-consistency and performance of pre-trained language models through natural language inference.  _arXiv preprint arXiv:2211.11875_. 
  * Mündler et al. (2023) Niels Mündler, Jingxuan He, Slobodan Jenko, and Martin Vechev. 2023.  Self-contradictory hallucinations of large language models: Evaluation, detection and mitigation.  _arXiv preprint arXiv:2305.15852_. 
  * Penedo et al. (2023) Guilherme Penedo, Quentin Malartic, Daniel Hesslow, Ruxandra Cojocaru, Alessandro Cappelli, Hamza Alobeidli, Baptiste Pannier, Ebtesam Almazrouei, and Julien Launay. 2023.  [The RefinedWeb dataset for Falcon LLM: outperforming curated corpora with web data, and web data only](http://arxiv.org/abs/2306.01116).  _arXiv preprint arXiv:2306.01116_. 
  * Peng et al. (2023) Baolin Peng, Michel Galley, Pengcheng He, Hao Cheng, Yujia Xie, Yu Hu, Qiuyuan Huang, Lars Liden, Zhou Yu, Weizhu Chen, et al. 2023.  Check your facts and try again: Improving large language models with external knowledge and automated feedback.  _arXiv preprint arXiv:2302.12813_. 
  * Tam et al. (2023) Derek Tam, Anisha Mascarenhas, Shiyue Zhang, Sarah Kwan, Mohit Bansal, and Colin Raffel. 2023.  Evaluating the factual consistency of large language models through news summarization.  In _Findings of the Association for Computational Linguistics: ACL 2023_ , pages 5220–5255. 
  * Tian et al. (2023) Katherine Tian, Eric Mitchell, Allan Zhou, Archit Sharma, Rafael Rafailov, Huaxiu Yao, Chelsea Finn, and Christopher D Manning. 2023.  Just ask for calibration: Strategies for eliciting calibrated confidence scores from language models fine-tuned with human feedback.  _arXiv preprint arXiv:2305.14975_. 
  * Touvron et al. (2023) Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, et al. 2023.  Llama: Open and efficient foundation language models.  _arXiv preprint arXiv:2302.13971_. 
  * Varshney et al. (2023) Neeraj Varshney, Wenlin Yao, Hongming Zhang, Jianshu Chen, and Dong Yu. 2023.  A stitch in time saves nine: Detecting and mitigating hallucinations of llms by validating low-confidence generation.  _arXiv preprint arXiv:2307.03987_. 
  * Wang et al. (2022) Xuezhi Wang, Jason Wei, Dale Schuurmans, Quoc Le, Ed Chi, Sharan Narang, Aakanksha Chowdhery, and Denny Zhou. 2022.  Self-consistency improves chain of thought reasoning in language models.  _arXiv preprint arXiv:2203.11171_. 
  * Xiao and Wang (2021) Yijun Xiao and William Yang Wang. 2021.  On hallucination and predictive uncertainty in conditional language generation.  _arXiv preprint arXiv:2103.15025_. 
  * Yang et al. (2023) Shiping Yang, Renliang Sun, and Xiaojun Wan. 2023.  A new benchmark and reverse validation method for passage-level hallucination detection.  _arXiv preprint arXiv:2310.06498_. 
  * Yang et al. (2018) Zhilin Yang, Peng Qi, Saizheng Zhang, Yoshua Bengio, William Cohen, Ruslan Salakhutdinov, and Christopher D Manning. 2018.  Hotpotqa: A dataset for diverse, explainable multi-hop question answering.  In _Proceedings of the 2018 Conference on Empirical Methods in Natural Language Processing_ , pages 2369–2380. 
  * Ye et al. (2023) Hongbin Ye, Tong Liu, Aijia Zhang, Wei 
