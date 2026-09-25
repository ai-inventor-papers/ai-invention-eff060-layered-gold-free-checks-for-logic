URL: https://arxiv.org/html/2305.15541 | FULL FETCH | 2026-09-24T01:49:34Z
warning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
URL: https://arxiv.org/html/2305.15541
Type: HTML
Length: 61875 chars (truncated)

--- Content ---

##### Report GitHub Issue

×

Title:

Content selection saved. Describe the issue below:

Description:

Submit without GitHub Submit in GitHub

arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[ Back to arXiv ](/)

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) Report Issue [ Back to Abstract ](/abs/2305.15541v1 "Back to abstract page") [ Download PDF](/pdf/2305.15541v1 "Download PDF") [ ](javascript:toggleNavTOC\(\); "Toggle navigation") [ ](javascript:toggleReadingMode\(\); "Disable reading mode, show header and footer")

  1. Abstract
  2. 1 Introduction
  3. 2 Related Work
  4. 3 Malls Dataset Creation
     1. 3.1 Prompt pipeline
     2. 3.2 Dataset statistics
  5. 4 Fine-tuning LogicLLaMA for NL-FOL Translation
     1. 4.1 Fine-tuning for direct translation and naive correction
     2. 4.2 Chain-of-Thought correction via SFT and RLHF
        1. 4.2.1 FOL Rule Perturbations and SFT
        2. 4.2.2 RLHF for CoT correction
        3. 4.2.3 FOL evaluation and reward design
  6. 5 Experiments
     1. 5.1 Results
     2. 5.2 Analysis
  7. 6 Conclusion
  8. References
  9. A Appendix
  10. B Malls Dataset Creation Details
     1. B.1 Data collection
     2. B.2 FOL parsing and verification
     3. B.3 Malls statistics
  11. C Computing Logical Equivalence and BLEU Score
  12. D Experimental Settings



[ License: CC BY 4.0 ](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2305.15541v1 [cs.CL] 24 May 2023

# Harnessing the Power of Large Language Models for Natural Language to First-Order Logic Translation

Yuan Yang  Affiliation: Georgia Institute of Technology  Email: [yyang754@](mailto:) Siheng Xiong  Affiliation: Georgia Institute of Technology  Email: [sxiong45@](mailto:) Ali Payani  Affiliation: Cisco  Email: [faramarz.fekri@ece.gatech.edu](mailto:) Ehsan Shareghi & Faramarz Fekri  Affiliation: Georgia Institute of Technology  Affiliation: Monash University  Email: [apayani@cisco.comehsan.shareghi@monash.edu](mailto:apayani@cisco.comehsan.shareghi@monash.edu)

###### Abstract

Translating natural language sentences to first-order logic (NL-FOL translation) is a longstanding challenge in the NLP and formal logic literature. This paper introduces LogicLLaMA, a LLaMA-7B model fine-tuned for NL-FOL translation using LoRA on a single GPU. LogicLLaMA is capable of directly translating natural language into FOL rules, which outperforms GPT-3.5. LogicLLaMA is also equipped to correct FOL rules predicted by GPT-3.5, and can achieve similar performance as GPT-4 with a fraction of the cost. This correction ability was achieved by a novel supervised fine-tuning (SFT) + reinforcement learning with human feedback (RLHF) framework, which initially trains on synthetically perturbed NL-FOL pairs to encourage chain-of-thought reasoning and then fine-tunes with RLHF on GPT-3.5 outputs using a FOL verifier as the reward model.

To train LogicLLaMA, we present Malls (large language Model generAted NL-FOL pairS), a dataset of 34K high-quality and diverse sentence-level NL-FOL pairs collected from GPT-4. The dataset was created by implementing a pipeline that prompts GPT-4 for pairs, and dynamically adjusts the prompts to ensure the collection of pairs with rich and diverse contexts at different levels of complexity, and verifies the validity of the generated FOL rules. Codes, weights, and data are available at <https://github.com/gblackout/LogicLLaMA>.

## 1 Introduction

Large language models (LLMs) have established state-of-the-art results on several reasoning and generation benchmark tasks (OpenAI, 2023; Chowdhery et al., 2022). Despite their success, LLMs struggle with logical reasoning (a prime example of System 2 task (Kahneman, 2011)), or maintaining logical consistency during generation (Nye et al., 2021). The common denominator of both is the absence of explicit logical grounding which could impose the consistency of a generated output and the state of the world (i.e., premises of the reasoning task, or the previously generated text). While desired, the existing tools and systems that foster such explicit grounding (Abzianidze, 2017; Bos and Markert, 2005) of Natural Language (NL) are brittle, and rely on hard-coded First-Order Logic (FOL) rules and facts, which is impractical for real-world use.

Recent variants of LLMs (i.e., GPT-4) exhibit impressive few-shot capabilities in NL-FOL translation tasks. This rapid improvement comes after recent observations (Han et al., 2022) which highlighted major defects of previous LLMs (e.g., GPT-3 davinci). Nonetheless, even the most powerful LLMs to this date cannot solve the NL-FOL translation task entirely, and for complex NL statements, they typically generate an answer which still requires a few “corrections”. However, in the absence of fine-tuning option (not available for RLHF-trained LLMs), most of the heavy lifting in this translation task is offloaded on the few-shot examples and prompt engineering. Not to mention, the cost element of using an LLM as a dedicated tool (or fine-tuning them) for NL-FOL translation could be prohibitive.

In order to improve the translation quality of LLMs (i.e., GPT-3.5), we present a framework that runs every output from GPT-3.5 through a small language model (LogicLLaMA), a LLaMA-7B model (Touvron et al., 2023) for NL-FOL translation fine-tuned with LoRA (Hu et al., 2021). LogicLLaMA is trained to correct outputs from GPT-3.5 (through an iterative correction) while also being able to act as a standalone direct NL-to-FOL translator. For training LogicLLaMA, we collected a high-quality and diversified dataset of 34K sentence-level NL-FOL pairs from GPT-4. We then created a perturbed version of the FOL in each pair to produce a controlled perturbation dataset, where each perturbed pair is accompanied by a “correction instruction” to undo the perturbation. We propose a novel SFT+RLHF framework that first trains LogicLLaMA on the synthetically perturbed NL-FOL pairs, equipping LogicLLaMA with generating corrective prompts, and then fine-tunes it with RLHF on the GPT-3.5 outputs using a FOL verifier as the reward model.

In our experiments, we probe the capabilities of the most recent LLMs in both zero- and few-shot settings in the NL-FOL translation task on two benchmarks with different levels of complexity, LogicNLI (Tian et al., 2021) and FOLIO (Han et al., 2022). We highlight, on the challenging dataset of FOLIO, the latest GPT-3.5 with 5-shot examples in the prompt does not go above 0.767 logical equivalence (LE) score, our proposed approach could iteratively improve its performance and reduce the gap between GPT-3.5 and GPT-4 (i.e., GPT-3.5+LogicLLaMA achieves 0.849 LE compared with GPT-4 score of 0.855) with a fraction of the cost.11 1 As of May 2023, GPT-3.5 costs $0.002/1K tokens whereas GPT4 costs $0.03/1K for prompt and $0.06/1K for completion. Additionally, we demonstrate LogicLLaMA capabilities as a standalone model for NL-FOL translation task, outperforming GPT-3.5 on both FOLIO and LogicNLI, while being highly competitive with GPT-4.

## 2 Related Work

NL-FOL translation. Natural language to first-order logic (NL-FOL) translation is a critical task that serves as the foundation of a wide range of logic-backed NLP applications, such as textual entailment (Bos and Markert, 2005), NL inference (Angeli and Manning, 2014) and theorem proving (Polu and Sutskever, 2020). Traditionally, NL-FOL translation has been addressed via rule-based methods (Abzianidze, 2017; Zettlemoyer and Collins, 2005; Bos and Markert, 2005). Due to the complexity of natural language, these methods are difficult to scale to real-world applications. Recently, there has been an increasing interest in approaching this task via neural approaches (Lu et al., 2022; Cao et al., 2019; Hahn et al., 2022; Wang et al., 2021; Singh et al., 2020; Levkovskyi and Li, 2021). The recent release of powerful LLMs such as GPT-3.5 and GPT-4 gives rise to a new paradigm: using LLMs to perform the bulk of the translation task, thereby benefiting from their generalization capabilities and capacity to handle complex and diverse language constructs. In this work, we investigate this paradigm and propose to collect NL-FOL pairs from GPT-4 and fine-tune a LLaMA-7B model on it.

NL-FOL datasets. Many datasets that focus on logical reasoning ability have been proposed recently. For example, LogiQA (Liu et al., 2020), RuleTaker (Clark et al., 2020), ReClor (Yu et al., 2020) and text2log (Levkovskyi and Li, 2021). However, these datasets either do not provide sentence-level FOL annotations, or the annotations are generated without verification. Among these works, LogicNLI (Tian et al., 2021) and FOLIO (Han et al., 2022) are closest to our work, which provides NL statements with parallel FOL annotations. However, pairs in LogicNLI are generated synthetic and share a similar FOL template. FOLIO consists of real-world expert-written pairs, but the size of 2K is insufficient for fine-tuning an LLM. This work extends the prior work and proposes to collect “silver” NL-FOL pairs from GPT-4. As a result, Malls has collected 34K pairs that are more diverse in terms of context and complexity. In experiments, we use LogicNLI and FOLIO as the “gold” sets to evaluate the LLM fine-tuned on Malls and demonstrate that it is of high quality.

## 3 Malls Dataset Creation

We create the Malls dataset by collecting NL-FOL pairs from GPT-4 which is considered to be the most powerful LLM to date. As of May 2023, Malls has reached the size of 34K and we plan to continue expanding the dataset in future versions.

Motivation. One of the goals to create such a dataset is to provide a corpus for fine-tuning and evaluating NL-FOL translation models. However, one may ask “if Malls is to be generated by yet another LLM, i.e., GPT-4, then why shouldn’t one use GPT-4 for the task already?” The motivation lies in the cost and privacy. While GPT-4 yields state-of-the-art performance, its API access is costly and not entirely publicly available to date; on the other hand, institutes and companies may have sensitive data that cannot be shared with a third party and they want to deploy a local LLM with similar performance. In §4, we show this can be achieved by fine-tuning a LLaMA-7B model on Malls on a single GPU.

Table 1: Statistics of Malls, LogicNLI, and FOLIO datasets.

Dataset | Source |  #NL-FOL pairs | NL |  | FOL  
---|---|---|---|---|---  
| Vocab  
---  
size  
| Avg.  
---  
#words  
|  | Avg.  
---  
#literals  
∀\forall | ∃\exists | ¬\neg | ∧\land | ∨\lor | →\to | ↔\leftrightarrow | ⊕\oplus  
FOLIO3 | Expert | 2K | 5105 | 10.4 |  | 2.1 | 1111 | 182 | 421 | 631 | 167 | 1137 | 17 | 121  
LogicNLI3 | Synthetic | 12K | 2061 | 13.9 |  | 2.8 | 2783 | 5327 | 10230 | 6590 | 2373 | 8712 | 3288 | 0  
Malls | GPT-4 | 34K | 22715 | 16.1 |  | 4.6 | 32865 | 2036 | 4567 | 30143 | 6402 | 30667 | 3726 | 2150  
  
Figure 1: Snippet from the top 200 frequent FOL term pairs in Malls (for full version see Appendix B). Many terms are associated with a wide range of other terms, which suggests the rules are semantically and contextually diverse.

### 3.1 Prompt pipeline

To collect data from GPT-4, we implemented a prompting pipeline that dynamically adjusts the prompts to both ensure the _diversity_ and _validity_ of the NL-FOL pairs. The pipeline consists of the following modules: (1) N-gram frequency counter; (2) Prompter; and (3) FOL rule verifier.

N-gram frequency counter. During prompting, we keep track of the frequencies of the N-grams in the entire NL statement corpus. Specifically, we track 1- and 3-grams. Once the frequency of a specific N-gram in the collected data reaches the frequency threshold (500 and 250 respectively), we will instruct GPT-4 to not produce any NL-FOL pairs including it. For example, “… DO NOT involve concepts and terms (and the synonyms) such as animal, food, …”. The list of N-grams in the instruction grows as more reach the frequency threshold.

Prompter. A prompter assembles the prompts generated from different modules (prompt table shown in Appendix B): (1) system prompt: specifying the basic requirements such as the syntax and generation format. (2) few-shot examples prompt: consisting 5 NL-FOL pair examples randomly sampled from the corpus. Initially, pairs are sampled from the FOLIO dataset and later on from the GPT-4-generated ones (we checked to ensure none of the FOLIO examples, or close variations are leaked into the GPT-4 generated NL-FOL pairs.). This diversifies the prompts and leads to less similar examples .(3) negative N-gram prompt: instructing GPT-4 not to involve frequent N-grams (introduced earlier) in the generated NL-FOL pairs. (4)FOL prompts: generating prompts that specify the desired form of FOL rules, i.e., the number of variables and whether or not to include more logic operators such as ⊕\oplus, ¬\neg, and ∨\lor which we found GPT-4 tends to ignore in default generation. These configurations are picked randomly every time the prompt is generated. (5) break-down prompt: We found GPT-4 by default tends to make over-complicated predicates that absorb important logical meanings. For example, “ ### NL: A fruit is considered ripe if it is mature and its color has changed from green to red. ### FOL: ∀x⁡(Fruit​(x)∧Mature​(x)∧ColorChangedToRed​(x)→Ripe​(x))\forall x(\texttt{Fruit}(x)\land\texttt{Mature}(x)\land\texttt{ColorChangedToRed}(x)\to\texttt{Ripe}(x)). ” The predicate ColorChangedToRed is complicated and should be broken down into “ColorBefore​(x,y)∧ColorAfter​(x,z)∧Green​(y)∧Red​(z)\texttt{ColorBefore}(x,y)\land\texttt{ColorAfter}(x,z)\land\texttt{Green}(y)\land\texttt{Red}(z)”. We alleviate this by detecting long predicate names and including a prompt encouraging the model to break down the rules.

FOL rule verifier. GPT-4 can sometimes generate syntactically invalid FOL rules. We implement a verifier that checks the syntax of the rules. Specifically, we specify the context-free grammar (CFG) of the expected FOL rule and parse the generated FOL with NLTK 22 2 https://www.nltk.org/ CFG parser, and erase those that could not be parsed (grammar and example parse trees in Appendix B).

### 3.2 Dataset statistics

General statistics. We show the general statistics in Table 1 together with those of LogicNLI and FOLIO33 3 Note that the FOLIO statistics are different from those reported in (Han et al., 2022). As of May 2023, the released dataset misses the ground truth FOL annotations for conclusions in the training set, and some pairs contain duplicates and invalid FOL rules. We removed those during pre-processing. Also, the LogicNLI statistics are obtained from the official repo [here](https://github.com/omnilabNLP/LogicNLI), which contains 12K samples instead of the 20K reported in the paper. . Malls contains 34K NL-FOL pairs, which is significantly larger than LogicNLI and FOLIO, and different from LogicNLI which is synthetically generated, the pairs are also more diverse and contextually rich, where the NL statements have a vocabulary size of 22.7K and an average length of 16 compared to 10 in FOLIO. For FOL rules, the average number of literals reached 4.6 indicating more complex rules (also see Figure 9 in Appendix B).

Pair diversity. The NL-FOL rules in Malls are highly diverse. To see this, we investigate the frequencies and the correlations of the FOL terms. A _term_ is either a predicate name or a named entity in a FOL rule. For example, “∀x⁡((Person​(x)∧Drinks​(x))→DependentOn​(x,Caffeine))\forall x((\texttt{Person}(x)\land\texttt{Drinks}(x))\to\texttt{DependentOn}(x,\texttt{Caffeine}))” consists of 4 terms, i.e., Person, Drinks, DependentOn and Caffeine. Malls has a total term vocabulary size of 49394 and the most frequent terms occur less than 2K times (Figure 8 in Appendix B), suggesting a diverse vocabulary distribution. On the other hand, we investigate the correlations between terms and illustrate the top 200 frequent term pairs. We show a snippet of this in Figure 1 (for the full version, see Figure 7 in Appendix B). Note that if a term is associated with many other terms, this typically means the rules involving that term are diverse in semantics and context, and Figure 1 suggests that it is indeed the case. For example, for rules involving Book, they cover the knowledge of its genre (e.g., Fiction), places (e.g., Library), viewership (e.g., Bestseller and PositiveReviews), and so on.

NL-FOL alignment. Apart from checking the FOL validity, we also implemented a simplistic verifier that checks the alignment between the NL statement and the FOL rule. This is done by treating the FOL as a query and computing its term frequency in the NL, and then rejecting those that are below a threshold. Apart from this, we did not conduct a rigorous alignment check in the creation of Malls. In fact, the best way to date to ensure alignment correctness is checking them manually as that in FOLIO dataset creation. This is prohibitive to do for a dataset of this size for an academic budget. That said, we recommend treating the dataset as “silver” labels and using it for training, and using another dataset with “gold” labels for evaluation. Nevertheless, in §5, we demonstrate that a model trained solely on this silver dataset can still achieve a similar performance as GPT-4, when evaluated on the gold sets such as FOLIO and LogicNLI.

## 4 Fine-tuning LogicLLaMA for NL-FOL Translation

In this section, we discuss how to fine-tune the LLaMA-7B (Touvron et al., 2023) model on the Malls to reach a GPT-4 level performance. We refer to this model as LogicLLaMA. Throughout the remainder of this section, we will refer to the silver FOLs in Malls as ground truth.

Unlike typical NLP tasks, where one fine-tunes it with a task-agnostic objective such as autoregression, fine-tuning for NL-FOL translation is nontrivial. Specifically, we address the following challenges:

(C1) What is the input and output of the LogicLLaMA? And how to prepare the training data from Malls? In §4.1, we first consider the naive approach, where LogicLLaMA is trained to predict the correct FOL directly. While it does not need any additional data other than the original Malls, it yields sub-optimal performance. We found better performance is achieved by eliciting the chain-of-thought (CoT) steps and gradually correcting the FOL predicted by another model, e.g., GPT-3.5. But, such training requires the ground-truth CoT steps which are not available in Malls. In §4.2, we propose to address this by first fine-tuning the model on synthetically perturbed FOLs with ground-truth CoT steps and then conducting the RLHF to correct the real outputs of GPT-3.5.

(C2) How to evaluate the generated FOL rules? Consider two FOL rules (denoted as RR and R′R^{\prime}) generated from an LLM “R:¬(P⁡(A)∧P⁡(B))R:\neg(P(A)\land P(B))” and “R′:¬P⁡(A)∨¬P⁡(B)R^{\prime}:\neg P(A)\lor\neg P(B)” — RR and R′R^{\prime} are logically equivalent but are different in the text; also consider a pair of rules “R:∀x​P​(x)R:\forall xP(x)” and “R′:∀x​∀y​P​(x)∧Q⁡(y)R^{\prime}:\forall x\forall yP(x)\land Q(y)”— if RR is the ground-truth and R′R^{\prime} the LLM prediction, how should one measure the distance and supervise the model? We address this in §4.2.3.

Figure 2: Input and expected outputs for direct translation, naive correction, and CoT correction.

### 4.1 Fine-tuning for direct translation and naive correction

The LogicLLaMA can be trained to directly translate the FOL from NL, which we refer to as (T1) direct translation task; it can also be trained to correct the generated FOL from a more powerful model such as GPT-3.5, which we refer to as the correction task. In this section, we consider the (T2) naive correction approach, where the correction is done in one go. The intuition is that we found in experiments GPT-3.5 is good at doing the “heavy-lifting” part of the translation and can capture the main part of the FOL rule; then presumably, one can train a smaller model that corrects the output from the GPT-3.5 to get a better result.

We train both (T1) and (T2) via standard autoregression objective. Specifically, we fine-tune a LLaMA-7B model with LoRA (for all the attention weight matrices) on Malls. The left two columns in Figure 2 show the input and output sequence of the two tasks: let ⟨𝒙NL,𝒙FOL⟩\langle{\bm{x}}_{\text{NL}},{\bm{x}}_{\text{FOL}}\rangle be an NL-FOL pair from Malls; for (T1), the input and output are the original sequences 𝒙NL{\bm{x}}_{\text{NL}} and 𝒙FOL{\bm{x}}_{\text{FOL}} respectively; and for (T2), let 𝒙^FOL=GPT​(𝒙NL)\hat{{\bm{x}}}_{\text{FOL}}=\text{GPT}({\bm{x}}_{\text{NL}}) be the FOL predicted by GPT-3.5, the input is the NL and the prediction put together [𝒙NL,𝒙^FOL][{\bm{x}}_{\text{NL}},\hat{{\bm{x}}}_{\text{FOL}}] and the output is the ground-truth FOL, 𝒙FOL{\bm{x}}_{\text{FOL}}.

### 4.2 Chain-of-Thought correction via SFT and RLHF

Figure 3: Overview of the SFT and RLHF training for the Chain-of-Thought (CoT) correction mode of LogicLLaMA.

While (T1) direct translation and (T2) naive correction are easy to train, they do not lead to optimal performance. Inspired by the Chain-of-Thought (CoT) technique (Wei et al., 2022), we found that training the model to produce the intermediate steps during the correction often leads to better performance. Such examples are shown in Figure 6.

To train such a model, one needs a dataset consisting of not only the ground-truth ⟨𝒙NL,𝒙FOL⟩\langle{\bm{x}}_{\text{NL}},{\bm{x}}_{\text{FOL}}\rangle, but also the CoT steps specific to a predicted FOL. Formally, recall that 𝒙^FOL\hat{{\bm{x}}}_{\text{FOL}} is the predicted FOL by GPT-3.5, then we need the ground-truth steps 𝒳^Δ=[𝒙^Δ,1,𝒙^Δ,2,…,𝒙^Δ,T]\hat{{\mathcal{X}}}_{\Delta}=[\hat{{\bm{x}}}_{\Delta,1},\hat{{\bm{x}}}_{\Delta,2},...,\hat{{\bm{x}}}_{\Delta,T}], such that they form a valid CoT sequence [𝒙^FOL,𝒙^Δ,1,𝒙^Δ,2,…,𝒙^Δ,T,𝒙FOL][\hat{{\bm{x}}}_{\text{FOL}},\hat{{\bm{x}}}_{\Delta,1},\hat{{\bm{x}}}_{\Delta,2},...,\hat{{\bm{x}}}_{\Delta,T},{\bm{x}}_{\text{FOL}}]. For example, the right column of Figure 2 shows a 4-step CoT correction.

However, as stated in (C1), we do not have ground-truth CoT steps 𝒳^Δ\hat{{\mathcal{X}}}_{\Delta} for the predicted FOL from GPT-3.5. We propose to address this issue using a combination of supervised fine-tuning (SFT) on a _synthetically perturbed_ dataset with ground-truth CoT steps, and reinforcement learning with human feedback (RLHF) training on the real GPT-3.5 output with a logical equivalence solver (discussed in §4.2.3) as the reward model.

Specifically, we refer to the SFT step as (T3) SFT CoT Correction. And as shown in the left column of Figure 3, we create a synthetic FOL dataset by perturbing the ground-truth FOL rule and obtaining the ground-truth CoT steps by reversing the past perturbations. And, we refer to the RLHF step as (T4) RLHF CoT Correction, which is shown in the right column of Figure 3.

#### 4.2.1 FOL Rule Perturbations and SFT

Table 2: The list of all atomic perturbations.

Operation Type | Subtypes | Original | Perturbed  
---|---|---|---  
Label Change | Change Predicate | P⁡(A)∧R⁡(B){{\color[rgb]{0,0,1}P}}(A)\land R(B) | R⁡(A)∧R⁡(B){{\color[rgb]{1,0,0}R}}(A)\land R(B)  
Change Term | ∀x​P​(x)∧P⁡(B)\forall{{\color[rgb]{0,0,1}x}}\;\;P(x)\land P(B) | ∀y​P​(x)∧P⁡(B)\forall{{\color[rgb]{1,0,0}y}}\;\;P(x)\land P(B)  
∀x​P​(x)∧P⁡(x)\forall x\;\;P(x)\land P({{\color[rgb]{1,0,0}x}})  
Change Operator | ∀x​P​(x)∧P⁡(B)\forall x\;\;P(x)\;{{\color[rgb]{0,0,1}\land}}\;P(B) | ∀x​P​(x)∨P⁡(B)\forall x\;\;P(x)\;{{\color[rgb]{1,0,0}\lor}}\;P(B)  
Insert | Insert Term | ∀x​P​(x)∧P⁡(B)\forall x\;\;P(x)\land P(B) | ∀x​∃y​P​(x)∧P⁡(B)\forall x\;{{\color[rgb]{1,0,0}\exists y}}\;\;P(x)\land P(B)  
∀x​P​(x)∧P⁡(x,B)\forall x\;\;P(x)\land P({{\color[rgb]{1,0,0}x,}}\;B)  
Insert Negation | P⁡(A)∧P⁡(B)∧P⁡(C)P(A)\land P(B)\land P(C) | P⁡(A)∧¬(P⁡(B)∧P⁡(C))P(A)\land{{\color[rgb]{1,0,0}\neg(}}P(B)\land P(C){{\color[rgb]{1,0,0})}}  
Insert Formula | P⁡(A)∧P⁡(B)P(A)\land P(B) | P⁡(A)∧P⁡(B)→R⁡(C)P(A)\land P(B)\;{{\color[rgb]{1,0,0}\to R(C)}}  
Delete | Delete Term | ∀x​∀y​P​(x)∧R⁡(x,y){{\color[rgb]{0,0,1}\forall x}}\;\forall y\;\;P(x)\land R(x,y) | ∀y​P​(x)∧R⁡(x,y)\forall y\;\;P(x)\land R(x,y)  
∀x​∀y​P​(x)∧R⁡(x,y)\forall x\;\forall y\;\;P(x)\land R({{\color[rgb]{0,0,1}x,}}\;y) | ∀x​∀y​P​(x)∧R⁡(y)\forall x\;\forall y\;\;P(x)\land R(y)  
Delete Negation | ¬(P⁡(A)∧P⁡(B)){{\color[rgb]{0,0,1}\neg(}}P(A)\land P(B){{\color[rgb]{0,0,1})}} | ¬(P⁡(A)∧P⁡(B))\neg(P(A)\land P(B))  
Delete Formula | P⁡(A)∧P⁡(B)∧P⁡(C)P(A)\;{{\color[rgb]{0,0,1}\land}}\;{{\color[rgb]{0,0,1}P(B)}}\;\land P(C) | P⁡(A)∧P⁡(C)P(A)\land P(C)  
  
Figure 4: Example of computing the Logical Equivalence score, 7/8=0.875.

Since we do not have the ground-truth CoT steps 𝒳^Δ\hat{{\mathcal{X}}}_{\Delta} for the real output 𝒙^FOL\hat{{\bm{x}}}_{\text{FOL}}, we generate synthetic steps and the output sequence by randomly perturbing the FOL rules in Malls.

We consider three types of atomic perturbations: label change, insert, and delete. As shown in Table 2, label change can be conducted on any terms or logic operators in a FOL rule; insert operation is applicable to term, negation, and formula; and delete operation can be considered as the inverse of insertion. Note that, we restrict the perturbations to only produce valid rules. The reasons are two-fold: (1) the invalid rule space is effectively the space of all possible strings which is prohibitive to explore; and (2) we found GPT-3.5 rarely generates syntactically invalid rule, thus, limiting the synthetic data in the valid rule space will already cover a wide range of the actual GPT-3.5 outputs.

Perturbation process. Given a ground-truth pair ⟨𝒙NL,𝒙FOL⟩\langle{\bm{x}}_{\text{NL}},{\bm{x}}_{\text{FOL}}\rangle, a parser (Appendix B) will parse 𝒙FOL{\bm{x}}_{\text{FOL}} into an abstract syntax tree (AST). We randomly perturb the AST with atomic operations in Table 2 and for NPerturbN_{\text{Perturb}} times. Here, NPerturbN_{\text{Perturb}} is also picked randomly from a list of numbers, and in the experiments, we set it to {0,1,2,…,10}\\{0,1,2,...,10\\}. In the case NPerturb=0N_{\text{Perturb}}=0, the perturbed rule remains the same as the ground truth and the CoT step is simply “No changes needed”; this is effectively a negative example that penalizes the model for over-correcting. During training, we found LogicLLaMA still tends to over-correct the samples as negative samples by default account for around 10% of the data, so we manually set the probability of negative sample generation to 0.2.

Iterative correction. Depending on the capacity of the LLM, it might be difficult for the model to learn to output many steps (say 10) within one generation. We propose to break down the correction into multiple generations, where the model is tasked to output at most NCorrectN_{\text{Correct}} steps of correction given the perturbed rule and the previous corrections up to NPerturb−NCorrectN_{\text{Perturb}}-N_{\text{Correct}} steps. For example, the right column of Figure 2 shows an iterative correction sample: it requires total NPerturb=4N_{\text{Perturb}}=4 steps to correct the rule, but we picked a correction steps of NCorrect=2N_{\text{Correct}}=2; this means the perturbed rule together with the previous two steps are treated as input and the last two steps are the output. Similar to NPerturbN_{\text{Perturb}}, we randomly choose NCorrectN_{\text{Correct}} from a list, where we set it to {0,1,2,3}\\{0,1,2,3\\}. And apparently, NCorrectN_{\text{Correct}} should be no greater than the total steps NCorrect=min⁡(NCorrect,NPerturb)N_{\text{Correct}}=\min(N_{\text{Correct}},N_{\text{Perturb}}).

SFT for CoT correction. For this (T3) task, we generate the synthetic dataset consisting of 150K examples in the form of ⟨𝒙NL,𝒙FOL,𝒳^Δ,prev,𝒳^Δ,corr,𝒙^FOL⟩\langle{\bm{x}}_{\text{NL}},{\bm{x}}_{\text{FOL}},\hat{{\mathcal{X}}}_{\Delta,\text{prev}},\hat{{\mathcal{X}}}_{\Delta,\text{corr}},\hat{{\bm{x}}}_{\text{FOL}}\rangle using the above method, where 𝒳^Δ,prev,𝒳^Δ,corr,𝒙^FOL\hat{{\mathcal{X}}}_{\Delta,\text{prev}},\hat{{\mathcal{X}}}_{\Delta,\text{corr}},\hat{{\bm{x}}}_{\text{FOL}} are the previous correction steps, target correction steps and the perturbed FOL rule respectively. We then fine-tune the LLaMA-7B model with LoRA again using the standard autoregression objective: the input is [𝒙NL,𝒙^FOL,𝒳^Δ,prev][{\bm{x}}_{\text{NL}},\hat{{\bm{x}}}_{\text{FOL}},\hat{{\mathcal{X}}}_{\Delta,\text{prev}}] and the output is [𝒳^Δ,corr,𝒙FOL][\hat{{\mathcal{X}}}_{\Delta,\text{corr}},{\bm{x}}_{\text{FOL}}].

#### 4.2.2 RLHF for CoT correction

With (T3) SFT CoT correction, we enable the model to generate intermediate correction steps for synthetic data. Now, we train the model to correct the actual outputs from GPT-3.5, which is (T4) RLHF CoT Correction task.

Why do we need RLHF? Note that to achieve this goal for (T4), we can no longer use the autoregression objective as in (T1), (T2), or (T3), since we still do not have the ground-truth CoT steps for GPT-3.5 outputs. However, on the other hand, we can still compare the final corrected rule to the ground-truth rule and measure how close they are. And this gives rise to an RL approach to the problem. Formally, let RM:𝒳×𝒳↦[0,1]\texttt{RM}:{\mathcal{X}}\times{\mathcal{X}}\mapsto[0,1] be a function that maps a pair of FOL sequences, 𝒙FOL{\bm{x}}_{\text{FOL}} and 𝒙FOL′{\bm{x}}_{\text{FOL}}^{\prime}, to a scalar score representing the pair similarity, our objective can be formalized as maximizing the score (effectively the expected return in RL),

| maxπRM(𝒙FOL,𝒙FOL′),where𝒙FOL′∼πθ(𝒙FOL,𝒳^Δ,corr|𝒙NL,𝒳^Δ,prev,𝒙^FOL),\displaystyle\max_{\pi}\texttt{RM}({\bm{x}}_{\text{FOL}},{\bm{x}}_{\text{FOL}}^{\prime}),\;\text{where}\;{\bm{x}}_{\text{FOL}}^{\prime}\sim\pi_{\theta}({\bm{x}}_{\text{FOL}},\hat{{\mathcal{X}}}_{\Delta,\text{corr}}|{\bm{x}}_{\text{NL}},\hat{{\mathcal{X}}}_{\Delta,\text{prev}},\hat{{\bm{x}}}_{\text{FOL}}), |  | (1)  
---|---|---|---  
  
for all tuples ⟨𝒙NL,𝒙FOL,𝒙^FOL⟩\langle{\bm{x}}_{\text{NL}},{\bm{x}}_{\text{FOL}},\hat{{\bm{x}}}_{\text{FOL}}\rangle in Malls via a policy πθ(𝒙FOL,𝒳^Δ,corr|𝒙NL,𝒳^Δ,prev,𝒙^FOL)\pi_{\theta}({\bm{x}}_{\text{FOL}},\hat{{\mathcal{X}}}_{\Delta,\text{corr}}|{\bm{x}}_{\text{NL}},\hat{{\mathcal{X}}}_{\Delta,\text{prev}},\hat{{\bm{x}}}_{\text{FOL}}) which is exactly the autoregressive model we trained in (T3) and would like to fine-tune in (T4). With objective Eq.(1), task (T4) is now similar to the RLHF proposed in InstructGPT (Ouyang et al., 2022) with the only difference being the reward model RM, where in our case, RM is a logical equivalence solver (§4.2.3) instead of a language model.

Training process. In (T4) RLHF CoT correction, we fine-tune the LogicLLaMA model obtained in (T3) SFT CoT correction via RLHF. For every tuple ⟨𝒙NL,𝒙FOL,𝒙^FOL⟩\langle{\bm{x}}_{\text{NL}},{\bm{x}}_{\text{FOL}},\hat{{\bm{x}}}_{\text{FOL}}\rangle, we let the model to continuously generate the corrections [⟨𝒙FOL′(1),𝒳^Δ,corr(1)⟩,⟨𝒙FOL′(2),𝒳^Δ,corr(2)⟩,…][\langle{\bm{x}}_{\text{FOL}}^{\prime(1)},\hat{{\mathcal{X}}}_{\Delta,\text{corr}}^{(1)}\rangle,\langle{\bm{x}}_{\text{FOL}}^{\prime(2)},\hat{{\mathcal{X}}}_{\Delta,\text{corr}}^{(2)}\rangle,...] until the model outputs “No changes needed” in the CoT steps or hits the token limit; the previous correction 𝒳^Δ,prev\hat{{\mathcal{X}}}_{\Delta,\text{prev}} is set to empty initially and we update it with the output steps in every generation. In other words, at iteration (t)(t), the previous correction is 𝒳^Δ,prev=[𝒳^Δ,corr(1),𝒳^Δ,corr(2),…,𝒳^Δ,corr(t−1),]\hat{{\mathcal{X}}}_{\Delta,\text{prev}}=[\hat{{\mathcal{X}}}_{\Delta,\text{corr}}^{(1)},\hat{{\mathcal{X}}}_{\Delta,\text{corr}}^{(2)},...,\hat{{\mathcal{X}}}_{\Delta,\text{corr}}^{(t-1)},]. For every generated text FOL at iteration (t)(t), we collect the experience tuple ⟨𝒙FOL′(t),𝒙NL,𝒳^Δ,prev,𝒙^FOL,r(t)⟩\langle{\bm{x}}_{\text{FOL}}^{\prime(t)},{\bm{x}}_{\text{NL}},\hat{{\mathcal{X}}}_{\Delta,\text{prev}},\hat{{\bm{x}}}_{\text{FOL}},r^{(t)}\rangle where r(t)=RM​(𝒙FOL,𝒙FOL′(t))r^{(t)}=\texttt{RM}({\bm{x}}_{\text{FOL}},{\bm{x}}_{\text{FOL}}^{\prime(t)}), and once enough experience is collected, we update the model parameter θ\theta via PPO (Schulman et al., 2017).

#### 4.2.3 FOL evaluation and reward design

The last component for (T4) is the reward model RM. This requires a metric that measures the similarity between two text FOLs 𝒙FOL{\bm{x}}_{\text{FOL}}, 𝒙FOL′{\bm{x}}_{\text{FOL}}^{\prime} to be implemented, and the metric should take into account the scenarios mentioned in challenge (C2).

Logical equivalence (LE). We propose to measure the logical equivalence between the rules by matching their truth tables and computing the overlap ratio. We introduce this with a running example in Figure 4. Specifically, let RR and R′R^{\prime} be the two rules parsed from the text 𝒙FOL{\bm{x}}_{\text{FOL}} and 𝒙FOL′{\bm{x}}_{\text{FOL}}^{\prime}. We identify the set of literals in each rule 𝒫=[p1,p2,…]{\mathcal{P}}=[p_{1},p_{2},...] and 𝒬=[q1,q2,…]{\mathcal{Q}}=[q_{1},q_{2},...]. In the case of Figure 4, 𝒫=[Country​(x),InEU​(x),EUCountry​(x)]{\mathcal{P}}=[\texttt{Country}(x),\texttt{InEU}(x),\texttt{EUCountry}(x)] and 𝒬=[LocatedInEU(y),EUCountry​(y)]{\mathcal{Q}}=[\texttt{LocatedInEU(y)},\texttt{EUCountry}(y)]. One can consider the set of literals as an array of Boolean variables, and the FOL as a circuit that takes in the Boolean values and outputs a single Boolean value. Therefore, we can represent a FOL with a truth table that enumerates all possible inputs and the resulting outputs. And to compare RR and R′R^{\prime}, we count the number of configurations that match and divide it by the total number of configurations; this yields a score in [0,1][0,1]. In Figure 4, this is 7/8=0.8757/8=0.875. The main issue with this approach is finding the right input bindings between 𝒫{\mathcal{P}} and 𝒬{\mathcal{Q}}, and dealing with the case where the numbers of inputs are different (i.e., |𝒫|≠|𝒬||{\mathcal{P}}|\neq|{\mathcal{Q}}|). We solve this by finding the binding that gives the highest LE score via greedy search and filling the rest of the missing inputs with dummy inputs. In Figure 4, InEU​(x)\texttt{InEU}(x) binds to LocatedInEU(y) and EUCountry​(x)\texttt{EUCountry}(x) binds to EUCountry​(y)\texttt{EUCountry}(y); and we fill in a dummy in 𝒬{\mathcal{Q}} to match Country​(x)\texttt{Country}(x) in 𝒫{\mathcal{P}}. We leave more details in Appendix C.

Reward design. We use the LE score as the main source of the reward. However, we also want the model to extract the right predicate and entity names from the NL statement. We incorporate this aspect by computing the BLEU score between the text 𝒙FOL{\bm{x}}_{\text{FOL}} and 𝒙FOL′{\bm{x}}_{\text{FOL}}^{\prime} with a specialized FOL tokenizer. We set the final reward as the mixture of the two: RM​(𝒙FOLCLOSE\texttt{RM}({\bm{x}}_{\text{FOL}}, OPEN𝒙FOL′)=ω∗LE​(R,R′)+(1−ω)∗BLEU​(𝒙FOLCLOSE{\bm{x}}_{\text{FOL}}^{\prime})=\omega*\text{LE}(R,R^{\prime})+(1-\omega)*\text{BLEU}({\bm{x}}_{\text{FOL}}, OPEN𝒙FOL′){\bm{x}}_{\text{FOL}}^{\prime}) , where ω\omega is the mixing ratio and in experiments we set it to 0.7.

## 5 Experiments

We address the following questions in the experiment section: (Q1) How good is Malls? Can we train a strong NL-FOL translation model with a “silver-labels-only” dataset? (Q2) How well does the LogicLLaMA perform in direct translation mode and CoT correction mode? (Q3) How do the CoT corrections influence the performance of LogicLLaMA?

Dataset. We use the entire Malls as the training set for (T1)-(T4); we also include 1K pairs from the training set of LogicNLI since it has a different rule distribution where rules are mostly grounded rules (i.e., many of them do not contain any variables) instead of FOL rules. We evaluate the LLMs on the full FOLIO dataset and the test set of LogicNLI.

Training, generation, and hardware settings. For all training tasks, we fine-tune LogicLLaMA using LoRA with rank=16, α=16\alpha=16, and dropout 0.05 on all the LLaMA-7B attention weights. We use the AdamW optimizer (Loshchilov and Hutter, 2017) with l​r=0.0003lr=0.0003. For the generation, we use a cutoff length of 256 for (T1) and (T2); and 1024 for (T3) and (T4), where 748 and 256 are allocated for the input prompt and output sequences respectively. All experiments are conducted on a Xeon 6140 machine with 256G RAM and a single V100 GPU (Detailed settings at Appendix D).

Metrics. We evaluate the translated and the final corrected FOL rules with two metrics: FOL BLEU score and FOL logical equivalence (LE) score (§4.2.3).

Table 3: BLEU and the logical equivalence (LE) scores of LogicLLaMA and GPT models on LogicNLI and FOLIO. Direct translation using LogicLLaMA outperforms GPT-3.5 and CoT correction achieves a similar performance as 5-shot GPT-4.

Methods | LogicNLI |  | FOLIO  
---|---|---|---  
FOL BLEU | FOL LE |  | FOL BLEU | FOL LE  
GPT-3.5 0-shot | 0.584 | 0.589 |  | 0.248 | 0.429  
GPT-3.5 5-shot | 0.905 | 0.918 |  | 0.341 | 0.767  
GPT-4 0-shot | 0.740 | 0.863 |  | 0.372 | 0.799  
GPT-4 5-shot | 0.913 | 0.989 |  | 0.400 | 0.855  
Direct Translation | 0.926 | 0.965 |  | 0.372 | 0.818  
Naive Correction | 0.934 | 0.970 |  | 0.373 | 0.840  
SFT CoT Correction | 0.663 | 0.830 |  | 0.332 | 0.730  
RLHF CoT Correction | 0.935 | 0.978 |  | 0.385 | 0.849  
  
Table 4: RLHF CoT correction performance vs. Max # generations.

Metrics | Max # Generations  
---|---  
1 |  | 3 |  | 5 |  | 10  
FOL BLEU | 0.361 |  | 0.370 |  | 0.384 |  | 0.385  
FOL LE | 0.815 |  | 0.841 |  | 0.846 |  | 0.849  
  
Figure 5: LogicLLaMA correction performance averaged over corresponding GPT-3.5 LE and BLEU scores.

Figure 6: Examples of correcting GPT-3.5’s output via naive and RLHF CoT correction.

### 5.1 Results

Table 3 shows the results of LogicLLaMA and GPT models on the LogicNLI and the FOLIO dataset. In general, we found that 5-shot GPT-4, as the most powerful LLM to date, achieves the best performance for both benchmarks. On the other hand, LogicLLaMA outperforms GPT-3.5 models in both translation and correction modes, and the best performance is achieved by RLHF CoT correction which leads to a GPT-4 level performance. This suggests that Malls—while being a silver label dataset—can indeed produce an LLM comparable to GPT-4 on a gold set, which addresses the question (Q1). Benchmark-wise, all methods achieve near-perfect results on LogicNLI except for 0-shot GPT-3.5, which has trouble generating syntactically valid rules due to the lack of examples. This is because LogicNLI is synthetically generated and the rules all share a similar FOL template. On the other hand, FOLIO is more challenging as they are expert-written.

### 5.2 Analysis

Translation vs. Correction. Table 3 suggested that the correction mode LogicLLaMA leads to better performance than the direct translation mode. This confirms our intuition in §4.1 and addresses the question (Q2). More importantly, these results suggest a new paradigm of future LLM development: by training a local LLM on the output of a more powerful model, one can conduct in-depth customization on the model behavior while still leveraging the generalizability of the powerful LLMs for heavy lifting. This paradigm is beneficial as GPT-3.5 and GPT-4 nowadays do not support fine-tuning and have a limited context window for customization.

Effect of CoT correction. To see how and why CoT correction improves performance, we compare the (T2) naive and the (T4) CoT correction performance on samples grouped by their “difficulty” level. To do this, we group samples by the GPT-3.5’s LE and BLEU scores into several bins (e.g., [1.0-0.9], [0.9-0.8] and etc.). Within each bin, we average the scores of GPT-3.5, (T2), and (T4). The results are shown in Figure 5. And correction examples are shown in Figure 6. We find the correction leads to a better performance generally by improving the difficult examples where GPT-3.5 fails significantly. The same trend is also present between (T2) and (T4), where CoT leads to better performance, especially on the BLEU score. We conjecture this is because CoT elicits the intermediate steps making it easy to find the right predicate and entity names.

Effect of CoT steps. We study the effect of the CoT steps by varying the maximum number of allowed generations on a single sample, which effectively limits the number of CoT steps that could be made by the model. The results are shown in Table 5. We found the performance saturated quickly starting from a max of three generations. For the one-generation case, it is slightly worse than the naive correction counterpart due to only a limited number of corrections could be made.

## 6 Conclusion

We present LogicLLaMA, the first specialized LM for the NL-FOL translation task. We release a high quality dataset of 34K sentence-level NL-FOL pairs collected from GPT-4, used for fine-tuning LogicLLaMA. LogicLLaMA with only 7B parameters shows competitive performance with GPT-4, while outperforming GPT-3.5 on challenging held-out NL-FOL benchmark. Through a novel SFT+RLHF training framework, we equip LogicLLaMA with step-by-step corrective capability, allowing it to consistently correct its own outputs, as well as outputs from a large LM (i.e., GPT-3.5).

## References

  * Abzianidze [2017] Lasha Abzianidze.  LangPro: Natural language theorem prover.  In _Proceedings of the 2017 Conference on Empirical Methods in Natural Language Processing: System Demonstrations_ , pages 115–120, Copenhagen, Denmark, September 2017. Association for Computational Linguistics.  doi: 10.18653/v1/D17-2020.  URL <https://www.aclweb.org/anthology/D17-2020>. 
  * Angeli and Manning [2014] Gabor Angeli and Christopher D Manning.  Naturalli: Natural logic inference for common sense reasoning.  In _Proceedings of the 2014 conference on empirical methods in natural language processing (EMNLP)_ , pages 534–545, 2014. 
  * Bos and Markert [2005] Johan Bos and Katja Markert.  Recognising textual entailment with logical inference.  In _Proceedings of Human Language Technology Conference and Conference on Empirical Methods in Natural Language Processing_ , pages 628–635, Vancouver, British Columbia, Canada, October 2005. Association for Computational Linguistics.  URL <https://aclanthology.org/H05-1079>. 
  * Cao et al. [2019] Ruisheng Cao, Su Zhu, Chen Liu, Jieyu Li, and Kai Yu.  Semantic parsing with dual learning.  In _Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics_ , pages 51–64, Florence, Italy, July 2019. Association for Computational Linguistics.  doi: 10.18653/v1/P19-1007.  URL <https://aclanthology.org/P19-1007>. 
  * Chowdhery et al. [2022] Aakanksha Chowdhery, Sharan Narang, Jacob Devlin, Maarten Bosma, Gaurav Mishra, Adam Roberts, Paul Barham, Hyung Won Chung, Charles Sutton, Sebastian Gehrmann, Parker Schuh, Kensen Shi, Sasha Tsvyashchenko, Joshua Maynez, Abhishek Rao, Parker Barnes, Yi Tay, Noam Shazeer, Vinodkumar Prabhakaran, Emily Reif, Nan Du, Ben Hutchinson, Reiner Pope, James Bradbury, Jacob Austin, Michael Isard, Guy Gur-Ari, Pengcheng Yin, Toju Duke, Anselm Levskaya, Sanjay Ghemawat, Sunipa Dev, Henryk Michalewski, Xavier Garcia, Vedant Misra, Kevin Robinson, Liam Fedus, Denny Zhou, Daphne Ippolito, David Luan, Hyeontaek Lim, Barret Zoph, Alexander Spiridonov, Ryan Sepassi, David Dohan, Shivani Agrawal, Mark Omernick, Andrew M. Dai, Thanumalayan Sankaranarayana Pillai, Marie Pellat, Aitor Lewkowycz, Erica Moreira, Rewon Child, Oleksandr Polozov, Katherine Lee, Zongwei Zhou, Xuezhi Wang, Brennan Saeta, Mark Diaz, Orhan Firat, Michele Catasta, Jason Wei, Kathy Meier-Hellstern, Douglas Eck, Jeff Dean, Slav Petrov, and Noah Fiedel.  Palm: Scaling language modeling with pathways.  _CoRR_ , abs/2204.02311, 2022.  doi: 10.48550/arXiv.2204.02311.  URL <https://doi.org/10.48550/arXiv.2204.02311>. 
  * Clark et al. [2020] Peter Clark, Oyvind Tafjord, and Kyle Richardson.  Transformers as soft reasoners over language.  _arXiv preprint arXiv:2002.05867_ , 2020. 
  * Hahn et al. [2022] Christopher Hahn, Frederik Schmitt, Julia J Tillman, Niklas Metzger, Julian Siber, and Bernd Finkbeiner.  Formal specifications from natural language.  _arXiv preprint arXiv:2206.01962_ , 2022. 
  * Han et al. [2022] Simeng Han, Hailey Schoelkopf, Yilun Zhao, Zhenting Qi, Martin Riddell, Luke Benson, Lucy Sun, Ekaterina Zubova, Yujie Qiao, Matthew Burtell, David Peng, Jonathan Fan, Yixin Liu, Brian Wong, Malcolm Sailor, Ansong Ni, Linyong Nan, Jungo Kasai, Tao Yu, Rui Zhang, Shafiq Joty, Alexander R. Fabbri, Wojciech Kryscinski, Xi Victoria Lin, Caiming Xiong, and Dragomir Radev.  FOLIO: Natural Language Reasoning with First-Order Logic, September 2022.  URL <http://arxiv.org/abs/2209.00840>.  arXiv:2209.00840 [cs]. 
  * Hu et al. [2021] Edward J Hu, Yelong Shen, Phillip Wallis, Zeyuan Allen-Zhu, Yuanzhi Li, Shean Wang, Lu Wang, and Weizhu Chen.  Lora: Low-rank adaptation of large language models.  _arXiv preprint arXiv:2106.09685_ , 2021. 
  * Kahneman [2011] Daniel Kahneman.  _Thinking, fast and slow_.  macmillan, 2011. 
  * Levkovskyi and Li [2021] Oleksii Levkovskyi and Wei Li.  Generating predicate logic expressions from natural language.  In _SoutheastCon 2021_ , pages 1–8. IEEE, 2021. 
  * Liu et al. [2020] Jian Liu, Leyang Cui, Hanmeng Liu, Dandan Huang, Yile Wang, and Yue Zhang.  Logiqa: A challenge dataset for machine reading comprehension with logical reasoning.  _arXiv preprint arXiv:2007.08124_ , 2020. 
  * Loshchilov and Hutter [2017] Ilya Loshchilov and Frank Hutter.  Decoupled weight decay regularization.  _arXiv preprint arXiv:1711.05101_ , 2017. 
  * Lu et al. [2022] Xuantao Lu, Jingping Liu, Zhouhong Gu, Hanwen Tong, Chenhao Xie, Junyang Huang, Yanghua Xiao, and Wenguang Wang.  Parsing natural language into propositional and first-order logic with dual reinforcement learning.  In _Proceedings of the 29th International Conference on Computational Linguistics_ , pages 5419–5431, Gyeongju, Republic of Korea, October 2022. International Committee on Computational Linguistics.  URL <https://aclanthology.org/2022.coling-1.481>. 
  * Nye et al. [2021] Maxwell I. Nye, Michael Henry Tessler, Joshua B. Tenenbaum, and Brenden M. Lake.  Improving coherence and consistency in neural sequence models with dual-system, neuro-symbolic reasoning.  In Marc’Aurelio Ranzato, Alina Beygelzimer, Yann N. Dauphin, Percy Liang, and Jennifer Wortman Vaughan, editors, _Advances in Neural Information Processing Systems 34: Annual Conference on Neural Information Processing Systems 2021, NeurIPS 2021, December 6-14, 2021, virtual_ , pages 25192–25204, 2021.  URL <https://proceedings.neurips.cc/paper/2021/hash/d3e2e8f631bd9336ed25b8162aef8782-Abstract.html>. 
  * OpenAI [2023] OpenAI.  GPT-4 technical report.  _CoRR_ , abs/2303.08774, 2023.  doi: 10.48550/arXiv.2303.08774.  URL <https://doi.org/10.48550/arXiv.2303.08774>. 
  * Ouyang et al. [2022] Long Ouyang, Jeffrey Wu, Xu Jiang, Diogo Almeida, Carroll Wainwright, Pamela Mishkin, Chong Zhang, Sandhini Agarwal, Katarina Slama, Alex Ray, et al.  Training language models to follow instructions with human feedback.  _Advances in Neural Information Processing Systems_ , 35:27730–27744, 2022. 
  * Polu and Sutskever [2020] Stanislas Polu and Ilya Sutskever.  Generative language modeling for automated theorem proving.  _arXiv preprint arXiv:2009.03393_ , 2020. 
  * Schulman et al. [2017] John Schulman, Filip Wolski, Prafulla Dhariwal, Alec Radford, and Oleg Klimov.  Proximal policy optimization algorithms.  _arXiv preprint arXiv:1707.06347_ , 2017. 
  * Singh et al. [2020] Hrituraj Singh, Milan Aggrawal, and Balaji Krishnamurthy.  Exploring neural models for parsing natural language into first-order logic.  _arXiv preprint arXiv:2002.06544_ , 2020. 
  * Tian et al. [2021] Jidong Tian, Yitian Li, Wenqing Chen, Liqiang Xiao, Hao He, and Yaohui Jin.  Diagnosing the first-order logical reasoning ability through LogicNLI.  In _Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing_ , pages 3738–3747, Online and Punta Cana, Dominican Republic, November 2021. Association for Computational Linguistics.  doi: 10.18653/v1/2021.emnlp-main.303.  URL <https://aclanthology.org/2021.emnlp-main.303>. 
  * Touvron et al. [2023] Hugo Touvron, Thibaut Lavril, Gautier Izacard, Xavier Martinet, Marie-Anne Lachaux, Timothée Lacroix, Baptiste Rozière, Naman Goyal, Eric Hambro, Faisal Azhar, et al.  Llama: Open and efficient foundation language models.  _arXiv preprint arXiv:2302.13971_ , 2023. 
  * Wang et al. [2021] Siyuan Wang, Wanjun Zhong, Duyu Tang, Zhongyu Wei, Zhihao Fan, Daxin Jiang, Ming Zhou, and Nan Duan.  Logic-driven context extension and data augmentation for logical reasoning of text.  _arXiv preprint arXiv:2105.03659_ , 2021. 
  * Wei et al. [2022] Jason Wei, Xuezhi Wang, Dale Schuurmans, Maarten Bosma, Ed Chi, Quoc Le, and Denny Zhou.  Chain of thought prompting elicits reasoning in large language models.  _arXiv preprint arXiv:2201.11903_ , 2022. 
  * Yu et al. [2020] Weihao Yu, Zihang Jiang, Yanfei Dong, and Jiashi Feng.  Reclor: A reading comprehension dataset requiring logical reasoning.  _arXiv preprint arXiv:2002.04326_ , 2020. 
  * Zettlemoyer and Collins [2005] Luke S. Zettlemoyer and Michael Collins.  Learning to map sentences to logical form: Structured classification with probabilistic categorial grammars.  In _UAI ’05, Proceedings of the 21st Conference in Uncertainty in Artificial Intelligence, Edinburgh, Scotland, July 26-29, 2005_ , pages 658–666. AUAI Press, 2005.  URL [https://dslpitt.org/uai/displayArticleDetails.jsp?mmnu=1&smnu=2&article_id=1209&proceeding_id=21](https://dslpitt.org/uai/displayArticleDetails.jsp?mmnu=1&smnu
