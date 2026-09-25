URL: https://arxiv.org/html/2608.30258 | FULL FETCH | 2026-09-24T01:42:43Z
warning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
URL: https://arxiv.org/html/2608.30258
Type: HTML
Length: 44167 chars

--- Content ---

##### Report GitHub Issue

×

Title:

Content selection saved. Describe the issue below:

Description:

Submit without GitHub Submit in GitHub

arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[ Back to arXiv ](/)

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) Report Issue [ Back to Abstract ](/abs/2608.30258v1 "Back to abstract page") [ Download PDF](/pdf/2608.30258v1 "Download PDF") [ ](javascript:toggleNavTOC\(\); "Toggle navigation") [ ](javascript:toggleReadingMode\(\); "Disable reading mode, show header and footer")

  1. Abstract
  2. 1 Introduction
  3. 2 Preliminary
  4. 3 Stratified Consistency Distillation
     1. 3.1 Stratified Consistency Distillation
  5. 4 Experiment
     1. 4.1 Experiment Settings
     2. 4.2 Logical NL2SMT Translation
     3. 4.3 Downstream Analysis
  6. 5 Related Works
  7. 6 Conclusion
  8. References
  9. A Prompt for Translation Generation



[ License: CC BY 4.0 ](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2608.30258v1 [cs.CL] 31 Aug 2026

#  Stratified Consistency Distillation for   
Natural Language Formalization 

Zhichao Hou  Affiliation: North Carolina State University  Ferhat Erata  Affiliation: Amazon Web Services  Joe Lilien  Affiliation: Amazon Web Services  MohamadAli Torkamani ††thanks: Corresponding author. Affiliation: Amazon Web Services  zhou4@ncsu.edu, {erata,lilienj,alitor}@amazon.com

###### Abstract

Neurosymbolic reasoning has shown promising success in addressing complex reasoning tasks by combining large language models (LLMs) and symbolic solvers. While this approach shows promise, a fundamental challenge remains: improving the accuracy of translations from natural language to logical formulas. Current methods predominantly rely on prompt engineering, which is difficult to scale across different domains and input formats. Drawing inspiration from the success of fine-tuning in other model adaptation and alignment applications, we propose a fine-tuning-based Stratified Consistency Distillation approach: (1) We generate K logical translations per input using a frontier LLM and cluster them by semantic equivalence (2) Based on the entropy level, we apply majority voting (low entropy), LLM-as-a-Judge (medium entropy), or unification/abstention (high entropy), and (3) fine-tune a smaller model using the selected pseudo-labels. Our experiments show significant and consistent improvements in both Pass@K and our novel Equivalent Logical Similarity metrics, demonstrating the potential of advancing logical translation through consistency distillation.  
  
---  
  
## 1 Introduction

Large Language Models (LLMs) have become a cornerstone technology for building customer-facing chatbot systems, enabling natural, context-aware, and highly interactive conversations across diverse application domains. Despite their impressive capabilities, LLMs are inherently prone to hallucinations—the generation of factually incorrect or logically inconsistent outputs—which may directly contradict authoritative source-of-truth documents. Such errors can be catastrophic in high-stakes domains such as compliance, pricing, and regulations, where a single incorrect response may result in financial loss, legal liability, or reputational damage.

A principled way to ensure the _logical soundness_ and _policy compliance_ of chatbot responses is to convert human-written natural language into _verifiable formal representations_ (e.g., SMT-LIB) and to verify their correctness using automated reasoning tools such as the Z3 solver. This leads us to a fundamental research question in the emerging field of _LLM reasoning and autoformalization_ :

> Can LLMs accurately understand human-written natural language and translate it into formal logical formulas that can be verified by a symbolic solver?

Recent advances in frontier LLMs (OpenAI and et al., 2024; Anthropic, 2024; Team and et al., 2024)—empowered by few-shot in-context learning and chain-of-thought prompting (Fu et al., 2023; Wei et al., 2023)—have demonstrated remarkable capabilities in such translation tasks. However, prompt-based approaches using frontier LLMs face two major limitations: (1) Frontier models are extremely large, with parameter counts ranging from 7070B to over 500500B, leading to high inference latency and prohibitive computational cost; and (2) These models are generally closed-source and only available through black-box APIs, preventing fine-tuning and constraining performance improvements beyond prompt engineering.

To address these limitations, we propose a systematic and scalable framework— _Stratified Consistency Distillation_ —for translating policy-governed natural language into formal logic, which distills the reasoning and translation capabilities of a frontier LLM into a smaller, more efficient open-source language model. Our main contributions are summarized as follows:

  * •

Synthetic Dataset Generation from Policy Documents. We design a robust pipeline to automatically extract domain-relevant rules from unstructured policy documents and generate aligned natural language–SMT-LIB training pairs, enabling scalable data creation without manual annotation.

  * •

Stratified Consistency Distillation (SCD). We introduce a novel distillation strategy that leverages semantic equivalence clustering and entropy-based stratification to selectively transfer knowledge from a high-capability frontier LLM into a smaller LM, preserving logical consistency while reducing inference cost.

  * •

Comprehensive Evaluation and Analysis. We conduct extensive experiments across multiple policy-driven reasoning benchmarks. Our method achieves substantial improvements in logical translation accuracy over both prompt-based frontier LLM approaches and fine-tuned baselines, while offering 5×5\times–20×20\times lower inference cost.




## 2 Preliminary

As large language models (LLMs) are increasingly used to power customer-facing chatbots, ensuring that their outputs remain accurate and aligned with formal company policies has become a critical challenge, especially in high-stakes domains such as compliance, pricing, and regulation. Despite their impressive capabilities, LLMs may generate hallucinated or logically inconsistent responses that contradict authoritative source documents. To improve chatbot reliability, we combine the natural language understanding capabilities of LLMs with formal logical reasoning, ensuring that generated responses are not only fluent but also logically sound and policy-compliant. In this section, we introduce our pipeline for generating synthetic data from policy documents, the resulting SMT-LIB representation, the NL2SMT problem formulation, and the evaluation metrics.

Figure 1: Synthetic dataset generation pipeline.

Synthetic dataset generation from policy documents. We generate natural language question-answer pairs and their corresponding SMT-LIB translations using information extracted from source policy documents. The pipeline consists of the following steps, as illustrated in Figure 1:

  1. 1.

Extract semantic context. The process begins with a source policy document. An LLM is used to construct a semantic model of the document, including an SMT-LIB specification consisting of relevant declarations, variables, and policy rules. The extracted declarations and contextual information guide the subsequent data-generation steps.

  2. 2.

Generate natural language Q&A pairs. An LLM generates natural language question-answer pairs based on the extracted semantic context. These pairs represent realistic user-chatbot interactions and are grounded in the content and rules of the source policy document.

  3. 3.

Translate natural language into SMT-LIB. The generated natural language content and the extracted semantic context are incorporated into the translation prompt. Using its reasoning capabilities, the LLM translates each natural language instance into a complete and syntactically valid SMT-LIB representation that captures the logical semantics of the question-answer pair.

  4. 4.

Construct the final training pairs. Each generated example is organized in the following format:

| <Natural Language Prompt>→<SMT-LIB Completion>.\texttt{\textless Natural Language Prompt\textgreater{}}\;\rightarrow{}\;\texttt{\textless SMT-LIB Completion\textgreater{}}. |   
---|---|---  
  
These prompt-completion pairs form the training dataset used to align natural language inputs with their formal logical representations.




SMT-LIB data representation. The resulting dataset consists of natural language prompts paired with their corresponding SMT-LIB translations. Each translation expresses the logical content of the input using the declarations, variables, and rules extracted from the relevant semantic context. Depending on the input, an SMT-LIB completion may contain logical operators, quantified expressions, constraints, or relationships between conditions and their consequences. All examples nevertheless follow a unified SMT-LIB representation and are treated as instances of the same NL2SMT translation task.

NL2SMT problem setup. We aim to improve the translation of natural language inputs into formal SMT-LIB representations. Given a natural language prompt 𝐩{\mathbf{p}}, which may include task instructions, contextual information, and a question-answer pair, the goal is to generate an SMT-LIB completion 𝐭{\mathbf{t}} that accurately captures its logical semantics. Formally, we define a training dataset 𝒟\mathcal{D} consisting of paired samples (𝐩,𝐭)({\mathbf{p}},{\mathbf{t}}), where 𝐭{\mathbf{t}} is the ground-truth SMT-LIB translation of 𝐩{\mathbf{p}}. Let 𝕃​𝕄θ\mathbb{LM}_{\theta} denote a parameterized language model with parameters θ\theta. Our objective is to maximize the expected similarity 𝒮\mathcal{S} between the generated translation 𝕃​𝕄θ​(𝐩)\mathbb{LM}_{\theta}({\mathbf{p}}) and the ground-truth translation 𝐭{\mathbf{t}}, where 𝒮\mathcal{S} measures either exact logical equivalence or continuous logical similarity:

| maxθ⁡𝔼(𝐩,𝐭)∼𝒟​[𝒮⁡(𝕃​𝕄θ​(𝐩),𝐭)].\max_{\theta}\mathbb{E}_{({\mathbf{p}},{\mathbf{t}})\sim\mathcal{D}}\left[\mathcal{S}\left(\mathbb{LM}_{\theta}({\mathbf{p}}),{\mathbf{t}}\right)\right]. |  | (1)  
---|---|---|---  
  
Equivalence measurements. To evaluate the quality of the generated SMT-LIB translations, we consider two complementary measurements of 𝒮\mathcal{S}:

  * •

Binary Equivalence Check. We use the Z3 theorem prover to determine whether a generated SMT-LIB formula is logically equivalent to its ground-truth counterpart. The check returns True when the two formulas are equivalent and False otherwise. We report Pass@10, which measures whether at least one of ten generated candidates is logically equivalent to the ground-truth formula.

  * •

Continuous Similarity Score. When exact equivalence is not achieved, we compute a graded similarity score in the range [0,1][0,1] using structural compression and anti-unification over the generated and ground-truth SMT-LIB formulas. Specifically, we use Egglog to extract an anti-unifier according to the defined SMT-LIB specification. The resulting score measures the degree of shared logical structure between the formulas.




Together, these measurements provide both a strict assessment of logical equivalence and a continuous assessment of partial logical alignment between generated and ground-truth SMT-LIB formulas.

## 3 Stratified Consistency Distillation

In this section, we introduce a systematic framework for logical translation-Stratified Consistency Distillation-which transfers knowledge from a frontier LLM to a smaller LM. The systematic overview of our framework is provided in Figure 2.

Figure 2:  Schematic overview of Stratified Consistency Distillation: For each training sample, we generate 10 SMT-LIB translations using a frontier LLM (e.g., Claude Sonnet 3.7). These translations are clustered based on semantic equivalence, and semantic entropy is computed. The data is then stratified into three groups by entropy: Low entropy: Apply majority voting for self-consistency; Medium entropy: Use LLM-as-a-Judge to select among the top-2 clusters; High entropy: Perform unification of the top-2 translations or abstain the data. Finally, we distill the knowledge into a smaller model (e.g., Qwen) via fine-tuning on Q&A pairs and pseudo-labels derived from stratified selection. 

### 3.1 Stratified Consistency Distillation

The pretrained frontier large language models (LLMs) (OpenAI and et al., 2024; Anthropic, 2024; Team and et al., 2024) have demonstrated superior reasoning capabilities, especially when combined with prompting techniques such as chain-of-thought (Fu et al., 2023; Wei et al., 2023). However, deploying these powerful LLMs in real-world scenarios remains challenging due to two main limitations: (1) They are typically extremely large, with model sizes ranging from 70B to over 500B parameters, resulting in significant latency and computational overhead during inference; and (2) These models are generally closed-source and only accessible through black-box APIs, which prevents fine-tuning and thus limits performance improvements beyond prompt engineering.

To overcome these limitations, we propose a Stratified Consistency Distillation pipeline that transfers knowledge from frontier teacher LLMs to a smaller student generator, as illustrated in Figure 2(a). At a high level, our pipeline consists of four main steps:

  1. 1.

Generation: Sample output sequences of tokens from the predictive distribution of a frontier LLM given an input prompt 𝐩{\mathbf{p}}.

  2. 2.

Clustering: Cluster the generated translations based on their logical equivalence using our proposed clustering algorithm. Estimate semantic entropy by summing the probabilities of clusters, following a defined entropy formulation.

  3. 3.

Selection: Select pseudo labels using different strategies depending on the estimated entropy.

  4. 4.

Distillation: Use the input and selected pseudo label from the frontier LLM to train a smaller student model.




Redundant Generation. Given a prompt 𝐩{\mathbf{p}} (including necessary instructions, few-shot examples, and the Q&A to be translated), we sample MM SMT-LIB translations {𝐭(1),𝐭(2),…,𝐭(M)}\\{{\mathbf{t}}^{(1)},{\mathbf{t}}^{(2)},\ldots,{\mathbf{t}}^{(M)}\\} from a frontier LLM (e.g., Claude Sonnet 3.7 (Anthropic, 2024)), denoted as 𝕃​𝕃​𝕄\mathbb{LLM}. To accelerate the sampling process, we employ vLLM (Kwon et al., 2023), a high-throughput and memory-efficient inference and serving engine.

Equivalent Clustering & Symbolic Semantic Entropy. We invoke our check_smt_equivalence function 𝔼⁡(⋅,⋅)\mathbb{E}(\cdot,\cdot) to group the MM translations into equivalence clusters based on logical equivalence. The check_smt_equivalence function verifies whether two SMT-LIB expressions (smt1 and smt2) are logically equivalent under given declarations using the Z3 SMT solver. The function constructs implication trees, writes them to an SMT-LIB file, and checks the satisfiability of the negated equality condition. A return value of unsat from Z3 indicates logical equivalence. The function outputs a dictionary containing the equivalence result, Z3 output, and any errors. Semantic entropy (Farquhar et al., 2024) has been introduced in natural language reasoning as a means to improve the correctness and soundness of LLM-generated reasoning. Extending this concept, we introduce symbolic semantic equivalence as an alternative formulation, described as follows. Recall that an equivalence relation is reflexive, symmetric, and transitive. Any such relation induces a set of equivalence classes. Each semantic equivalence class groups outputs expressing the same logical meaning. That is, for the set of classes 𝒞\mathcal{C}, all sentences 𝐭,𝐭′∈𝐜∈𝒞{\mathbf{t}},{\mathbf{t}}^{\prime}\in\mathbf{c}\in\mathcal{C} satisfy 𝔼⁡(𝐭,𝐭′)=True\mathbb{E}({\mathbf{t}},{\mathbf{t}}^{\prime})=\texttt{True}. New sentences are added to an existing class if they match any existing member, otherwise a new class is formed. Given the clusters 𝒞\mathcal{C}, we compute semantic entropy as: SE(𝐩)=−∑i=1|𝒞|P(𝒞i|𝐩)logP(𝒞i|𝐩),\text{SE}({\mathbf{p}})=-\sum_{i=1}^{|\mathcal{C}|}P(\mathcal{C}_{i}|{\mathbf{p}})\log P(\mathcal{C}_{i}|{\mathbf{p}}), where P⁡(𝒞i|𝐩)P(\mathcal{C}_{i}|{\mathbf{p}}) is the normalized probability of cluster 𝒞i\mathcal{C}_{i}.

Stratified Selection for Pseudo Labels. After computing entropy for each input, we construct a training dataset {𝐩i,{𝐭i(j)}j=1M,ei}i=1N\left\\{{\mathbf{p}}_{i},\\{{\mathbf{t}}_{i}^{(j)}\\}_{j=1}^{M},e_{i}\right\\}_{i=1}^{N}, where eie_{i} is the entropy value. We stratify the data into three groups based on entropy and apply different strategies to select pseudo labels:

  * •

Low entropy: The generation distribution is concentrated on a dominant cluster. We select a translation from the largest cluster: 𝐭∈arg⁡max𝒞i∈𝒞​|𝒞i|{\mathbf{t}}\in\arg\max_{\mathcal{C}_{i}\in\mathcal{C}}|\mathcal{C}_{i}|.

  * •

Medium entropy: There is some ambiguity across top candidates. We use the frontier LLM as a judge to select from the top-2 clusters.

  * •

High entropy: High disagreement across generations necessitates either unifying top translations or abstaining from using the sample.




Knowledge Distillation. Following the pipeline above, we obtain a final dataset {(𝐩i,𝐭i)}i=1N\left\\{({\mathbf{p}}_{i},{\mathbf{t}}_{i})\right\\}_{i=1}^{N}. We fine-tune a smaller student model (e.g., Qwen2.5-7B) using LoRA, distilling knowledge from the frontier LLM.

## 4 Experiment

### 4.1 Experiment Settings

We conduct experiments to evaluate the translation of natural language prompts into SMT-LIB formulas under the NL2SMT framework.

Datasets. We evaluate our method on NL2SMT FOLIO dataset. FOLIO is an open-domain first-order logic reasoning benchmark comprising natural language premises and conclusions paired with SMT-LIB assertions constructed using predefined logical declarations. Together, these datasets evaluate NL2SMT translation in both realistic policy-oriented conversations and controlled logical-reasoning scenarios.

Training Strategy. We fine-tune pretrained language models using _LoRA_ (Low-Rank Adaptation), a parameter-efficient fine-tuning method. We use a learning rate of 5×10−55\times 10^{-5}, a batch size of 32, a LoRA rank of 32, and a LoRA scaling factor α\alpha of 64.

Evaluated Models. Our primary student model is Qwen2.5-7B-Instruct, on which all fine-tuning experiments and ablation studies are conducted. For comparison, we evaluate the few-shot performance of several open-source and proprietary LLMs, including Qwen2.5-7B-Instruct, Qwen3-4B, Qwen3-8B, Qwen3-14B, Mistral-7B-Instruct, and Claude Sonnet 3.7.

Evaluation Metrics. We adopt two complementary metrics to evaluate translation quality. First, for the _Binary Equivalence Check_ , we use the Z3 theorem prover to determine whether a generated SMT-LIB formula is logically equivalent to the ground-truth formula. We report Pass@10, which measures whether at least one of ten generated candidates passes the equivalence check. Second, for the _Continuous Similarity Score_ , we measure partial logical similarity in the range [0,1][0,1] when exact equivalence is not achieved. This score is computed through symbolic compression and anti-unification of the generated and ground-truth SMT-LIB formulas using an SMT-LIB specification implemented in Egglog.

### 4.2 Logical NL2SMT Translation

Table 1: Pass@K scores (%) for FOLIO Translation.

Model | Pass@10 | Pass@9 | Pass@8 | Pass@7 | Pass@6 | Pass@5 | Pass@4 | Pass@3 | Pass@2 | Pass@1  
---|---|---|---|---|---|---|---|---|---|---  
Qwen3-4B | 19.792 | 19.792 | 19.792 | 19.792 | 19.792 | 19.792 | 19.792 | 19.792 | 18.750 | 17.708  
Qwen3-8B | 18.750 | 18.750 | 18.750 | 18.750 | 18.750 | 18.750 | 16.667 | 16.667 | 16.667 | 16.667  
Qwen3-14B | 42.708 | 42.708 | 42.708 | 42.708 | 42.708 | 42.708 | 42.708 | 42.708 | 42.708 | 42.708  
Mistral-7B-Instruct | 6.250 | 6.250 | 6.250 | 6.250 | 6.250 | 5.208 | 5.208 | 4.167 | 4.167 | 4.167  
Qwen2.5-7B-Instruct | 21.875 | 21.875 | 21.875 | 21.875 | 20.833 | 19.792 | 18.750 | 18.750 | 18.750 | 15.625  
Distillation | 50.347 | 50.347 | 49.306 | 48.264 | 47.222 | 46.181 | 45.486 | 43.750 | 42.708 | 39.931  
SCD | 55.208 | 55.208 | 54.514 | 52.778 | 50.083 | 49.653 | 48.958 | 47.917 | 46.528 | 44.097  
  
FOLIO Dataset. We evaluate our method on FOLIO and report Pass@K for K=1,…,10K=1,\ldots,10 in Table 1. We make the following observations:

  * •

Both distillation methods substantially outperform the pretrained baselines. For example, Qwen2.5-7B-Instruct achieves a Pass@10 of 21.875% in the few-shot setting, whereas vanilla distillation improves it to 50.347%.

  * •

Vanilla distillation also outperforms the strongest pretrained baseline, Qwen3-14B, by 7.639 percentage points in Pass@10 (50.347% versus 42.708%), despite using a smaller student model.

  * •

SCD achieves the best Pass@10 performance of 55.208%, exceeding Qwen3-14B by 12.500 percentage points and vanilla distillation by 4.861 percentage points.




### 4.3 Downstream Analysis

Visualization. Figures 3 and 4 visualize the per-example Pass@10 outcomes and continuous similarity scores, respectively, under different model and training configurations. In Figure 3, red denotes an unsuccessful translation and green denotes a successful translation. In Figure 4, colors range from red for low similarity to green for high similarity. The evaluated configurations include pretrained Mistral-7B-Instruct, pretrained Qwen2.5-7B-Instruct, Qwen2.5-7B-Instruct fine-tuned on NL2SMT dataset, and the corresponding model trained using our consistency-distillation framework. The Pass@10 heatmaps show a gradual transition from predominantly unsuccessful predictions for the pretrained models to broader coverage of correct translations after fine-tuning and distillation. Mistral-7B-Instruct exhibits the sparsest coverage of successful predictions, followed by pretrained Qwen2.5-7B-Instruct. Fine-tuning on the NL2SMT dataset increases the number of correctly translated examples, while consistency distillation produces the broadest coverage. The similarity heatmaps exhibit a comparable trend. The pretrained models contain larger regions of low similarity, whereas fine-tuning and consistency distillation shift the distribution toward higher similarity values, indicating stronger logical alignment with the ground-truth translations.

Figure 3: Per-example Pass@10 results under different model and training configurations. Figure 4: Per-example similarity scores under different model and training configurations. Table 2: Latency percentiles (P50, P90, P99) of different models on P4d EC2 instance.

Model | P50 | P90 | P99  
---|---|---|---  
Claude Sonnet 3.7 | 16.680 | 28.042 | 29.425  
Qwen2.5-7B-Instruct | 4.040 | 5.074 | 5.651  
Qwen3-4B | 4.294 | 5.698 | 6.281  
Qwen3-8B | 2.860 | 4.809 | 4.835  
Qwen3-14B | 7.454 | 13.939 | 14.604  
Mistral-7B-Instruct-v0.2 | 4.350 | 7.307 | 14.191  
  
Latency. Table 2 reports the P50, P90, and P99 inference latency of the evaluated models. The fine-tuned Qwen2.5-7B-Instruct model achieves substantially lower latency than Claude Sonnet 3.7 across all three percentiles. Its P50 latency is 4.040 seconds, approximately 4.1×4.1\times faster than the 16.680 seconds required by Claude Sonnet 3.7. The same advantage is observed at P90 (5.074 versus 28.042 seconds) and P99 (5.651 versus 29.425 seconds), indicating that the efficiency improvement remains consistent at higher latency percentiles. Among the open-source models, Qwen2.5-7B-Instruct also provides a favorable efficiency profile. It achieves lower P90 and P99 latency than Qwen3-4B, Qwen3-14B, and Mistral-7B-Instruct, although Qwen3-8B is faster. These results demonstrate that our approach improves translation quality while retaining practical efficiency.

Reliability of Symbolic Semantic Entropy. To validate the motivation for stratified consistency distillation, we investigate whether the sizes of semantic-equivalence clusters provide a reliable signal for selecting the correct translation. We treat _symbolic semantic entropy_ as an indicator of prediction uncertainty, as illustrated in Figure 5. In the low-entropy regime, the largest cluster is dominant and is therefore likely to contain the correct translation. In the medium-entropy regime, the correct translation may instead occur in a secondary cluster. In the high-entropy regime, candidate translations are more evenly distributed across clusters, making the largest cluster less reliable. Table 3 compares different cluster-based selection strategies. Selecting the largest cluster (Top@1) performs better than randomly selecting a candidate (Pass@1). Moreover, Top@2 approaches the oracle upper bound represented by Pass@10, indicating that the correct translation is usually contained within one of the two largest clusters.

Figure 5: Illustration of semantic-equivalence clusters at different uncertainty levels. Each cluster groups logically equivalent SMT-LIB candidates, and the gold star (⋆\star) denotes the ground-truth translation. As entropy increases, the candidates become more evenly distributed across clusters, reducing the reliability of the largest cluster. (a) Low entropy: the largest cluster contains the ground truth; (b) Medium entropy: the ground truth appears in a secondary cluster; and (c) High entropy: the largest cluster is no longer a reliable indicator of correctness. Table 3: Performance of cluster-based candidate-selection. Pass@1 (Random) randomly selects one candidate, whereas Top@kk considers candidates from the kk largest semantic-equivalence clusters.

Model | Pass@10 | Pass@1 (Random) | Top@1 | Top@2 | Top@3  
---|---|---|---|---|---  
Qwen2.5-7B | 17.593 | 13.889 | 15.741 | 17.593 | 17.593  
SCD | 31.481 | 24.074 | 25.926 | 30.556 | 31.481  
  
Stratified Consistency Distillation. The ablation results in Table 4 show that the distillation strategies substantially improve Pass@K over the pretrained Qwen2.5-7B baseline. Vanilla distillation already produces a considerable improvement, demonstrating the value of transferring high-quality outputs from the teacher model. Among the entropy-specific variants, training with low-entropy samples consistently outperforms training with high-entropy samples across all values of KK, suggesting that more consistent teacher predictions provide a stronger supervision signal. Most importantly, stratified SCD achieves the highest or tied-highest performance across all reported Pass@K metrics. This result demonstrates that applying different selection strategies according to semantic entropy produces a more effective and robust distillation signal than relying on a single entropy regime.

Table 4:  Ablation study of stratified consistency distillation on the Customer Service dataset.

Model | Pass@10 | Pass@9 | Pass@8 | Pass@7 | Pass@6 | Pass@5 | Pass@4 | Pass@3 | Pass@2 | Pass@1  
---|---|---|---|---|---|---|---|---|---|---  
Qwen2.5-7B | 17.593 | 17.593 | 17.593 | 17.593 | 16.667 | 16.667 | 15.741 | 15.741 | 14.815 | 13.889  
Vanilla Distillation | 27.469 | 27.469 | 27.116 | 26.543 | 25.926 | 25.617 | 24.383 | 23.148 | 22.222 | 19.753  
SCD (High Entropy) | 26.235 | 26.235 | 25.000 | 24.691 | 23.765 | 22.679 | 20.679 | 19.753 | 18.519 | 18.519  
SCD (Low Entropy) | 28.704 | 28.704 | 28.704 | 28.086 | 27.778 | 26.852 | 25.926 | 25.926 | 24.074 | 23.457  
SCD (Stratified) | 31.481 | 31.481 | 31.481 | 30.247 | 29.938 | 26.852 | 26.852 | 26.852 | 26.852 | 26.852  
  
## 5 Related Works

Improving Logical Reasoning of LLMs. Substantial research has been devoted to enhancing the logical reasoning capabilities of large language models (LLMs), with a particular focus on mathematical reasoning tasks. Early studies have shown that pretrained LLMs (Team and et al., 2024; OpenAI and et al., 2024; Anthropic, 2024) can solve reasoning problems through prompting strategies such as Chain-of-Thought (CoT) reasoning (Fu et al., 2022; Wei et al., 2022), which guides the model to generate intermediate steps before producing the final answer. Beyond prompting, supervised fine-tuning (SFT) (Cobbe et al., 2021; Yu et al., 2023) on high-quality, human-annotated datasets has been shown to yield further improvements in reasoning accuracy. More recently, reinforcement learning from human feedback (RLHF) (Ziegler et al., 2019) has emerged as a powerful approach for improving reasoning performance, leveraging reward models (Lightman et al., 2023; Wang et al., 2023) to align LLM outputs with desired reasoning processes and solutions. However, these techniques for translating informal natural language into formal SMT-LIB formulas remain largely underexplored.

Automalization of LLMs. Autoformalization, the task of converting informal natural language into verifiable formal representations, plays a foundational role in both mathematical formalization and the emerging verification of LLM-generated outputs. In mathematical contexts, it enables the translation of human-written proofs into machine-checkable formats for proof assistants such as Coq (Team, 2024), Lean (De Moura et al., 2015), and Isabelle (Ait Mohamed et al., 2008). More recently, its scope has expanded to address reliability issues in LLMs by translating generated text into precise, logically consistent forms using systems such as first-order logic (Ryu et al., 2024) or arithmetic frameworks like Peano arithmetic (Kennedy and Amsler, 1974). By bridging the expressive flexibility of natural language and the rigor of formal verification, autoformalization mitigates semantic ambiguity and supports robust reasoning. However, translating LLM outputs directly into SMT-LIB—a critical formalism for automated reasoning over logical constraints—remains largely unexplored. This gap motivates our work, which aims to advance LLM automatization in this under-addressed direction.

## 6 Conclusion

In this work, we addressed the challenge of ensuring the logical soundness of LLM-generated responses in high-stakes domains. We proposed a principled NL2SMT framework that translates natural language into verifiable SMT-LIB formulas, enabling automated verification with symbolic solvers. Our Stratified Consistency Distillation method selectively distills the logical translation capability of a frontier teacher model into a smaller open-source student, allocating supervision according to the uncertainty of the generated translations. Experiments on FOLIO show that our method improves translation accuracy over both pretrained and vanilla-distillation baselines, and matches or exceeds substantially larger models despite using far fewer parameters. The distilled model further offers considerably lower inference latency, making the framework more practical to deploy. Overall, this work provides a scalable route to efficient, reliable, and verifiable language models for domains in which logical correctness is essential.

## References

  * Ait Mohamed et al. (2008) O. Ait Mohamed, C. Munoz, and S. Tahar Theorem proving in higher order logics: 21st international conference, tphols 2008, montreal, canada, august 18-21, 2008, proceedings.  Vol. 5170, Springer Science & Business Media.  Cited by: §5. 
  * Anthropic (2024) Anthropic Claude 3 model family.  Note: Accessed: 2024-10-XX External Links: [Link](https://www.anthropic.com/news/claude-3-family) Cited by: §1, §3.1, §3.1, §5. 
  * Cobbe et al. (2021) K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano, et al. Training verifiers to solve math word problems.  arXiv preprint arXiv:2110.14168.  Cited by: §5. 
  * De Moura et al. (2015) L. De Moura, S. Kong, J. Avigad, F. Van Doorn, and J. von Raumer The lean theorem prover (system description).  In International Conference on Automated Deduction,  pp. 378–388.  Cited by: §5. 
  * Farquhar et al. (2024) S. Farquhar, J. Kossen, L. Kuhn, and Y. Gal Detecting hallucinations in large language models using semantic entropy.  Nature 630 (8017), pp. 625–630.  Cited by: §3.1. 
  * Fu et al. (2022) Y. Fu, H. Peng, A. Sabharwal, P. Clark, and T. Khot Complexity-based prompting for multi-step reasoning.  arXiv preprint arXiv:2210.00720.  Cited by: §5. 
  * Fu et al. (2023) Y. Fu, H. Peng, A. Sabharwal, P. Clark, and T. Khot Complexity-based prompting for multi-step reasoning.  External Links: 2210.00720, [Link](https://arxiv.org/abs/2210.00720) Cited by: §1, §3.1. 
  * Kennedy and Amsler (1974) H. C. Kennedy and R. Amsler Giuseppe peano.  Birkhäuser.  Cited by: §5. 
  * Kwon et al. (2023) W. Kwon, Z. Li, S. Zhuang, Y. Sheng, L. Zheng, C. H. Yu, J. E. Gonzalez, H. Zhang, and I. Stoica Efficient memory management for large language model serving with pagedattention.  In Proceedings of the ACM SIGOPS 29th Symposium on Operating Systems Principles,  Cited by: §3.1. 
  * Lightman et al. (2023) H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and K. Cobbe Let’s verify step by step.  In The Twelfth International Conference on Learning Representations,  Cited by: §5. 
  * OpenAI and et al. (2024) OpenAI and J. A. et al. GPT-4 technical report.  External Links: 2303.08774, [Link](https://arxiv.org/abs/2303.08774) Cited by: §1, §3.1, §5. 
  * Ryu et al. (2024) H. Ryu, G. Kim, H. S. Lee, and E. Yang Divide and translate: compositional first-order logic translation and verification for complex logical reasoning.  arXiv preprint arXiv:2410.08047.  Cited by: §5. 
  * Team and et al. (2024) G. Team and P. G. et al. Gemini 1.5: unlocking multimodal understanding across millions of tokens of context.  External Links: 2403.05530, [Link](https://arxiv.org/abs/2403.05530) Cited by: §1, §3.1, §5. 
  * Team (2024) The coq proof assistant External Links: [Document](https://dx.doi.org/10.5281/zenodo.11551307), [Link](https://doi.org/10.5281/zenodo.11551307) Cited by: §5. 
  * Wang et al. (2023) P. Wang, L. Li, Z. Shao, R. Xu, D. Dai, Y. Li, D. Chen, Y. Wu, and Z. Sui Math-shepherd: verify and reinforce llms step-by-step without human annotations.  arXiv preprint arXiv:2312.08935.  Cited by: §5. 
  * Wei et al. (2023) J. Wei, X. Wang, D. Schuurmans, M. Bosma, B. Ichter, F. Xia, E. Chi, Q. Le, and D. Zhou Chain-of-thought prompting elicits reasoning in large language models.  External Links: 2201.11903, [Link](https://arxiv.org/abs/2201.11903) Cited by: §1, §3.1. 
  * Wei et al. (2022) J. Wei, X. Wang, D. Schuurmans, M. Bosma, F. Xia, E. Chi, Q. V. Le, D. Zhou, et al. Chain-of-thought prompting elicits reasoning in large language models.  Advances in neural information processing systems 35, pp. 24824–24837.  Cited by: §5. 
  * Yu et al. (2023) L. Yu, W. Jiang, H. Shi, J. Yu, Z. Liu, Y. Zhang, J. T. Kwok, Z. Li, A. Weller, and W. Liu Metamath: bootstrap your own mathematical questions for large language models.  arXiv preprint arXiv:2309.12284.  Cited by: §5. 
  * Ziegler et al. (2019) D. M. Ziegler, N. Stiennon, J. Wu, T. B. Brown, A. Radford, D. Amodei, P. Christiano, and G. Irving Fine-tuning language models from human preferences.  arXiv preprint arXiv:1909.08593.  Cited by: §5. 



## Appendix A Prompt for Translation Generation

Prompt for Translation Generation (FOLIO) [⬇](data:text/plain;base64,WW91IGFyZSBhbiBleHBlcnQgaW4gYXV0b2Zvcm1hbGl6YXRpb24gLSB0cmFuc2xhdGluZyBuYXR1cmFsIGxhbmd1YWdlIGxvZ2ljYWwgcmVhc29uaW5nIGludG8gU01ULUxJQiBmb3JtYXQuCgpZb3VyIHRhc2s6IEdpdmVuIG5hdHVyYWwgbGFuZ3VhZ2UgcHJlbWlzZXMgYW5kIGNvbmNsdXNpb24sIGdlbmVyYXRlIFNNVC1MSUIgYXNzZXJ0aW9ucyB1c2luZyB0aGUgcHJvdmlkZWQgZGVjbGFyYXRpb25zLgoKPGluc3RydWN0aW9ucz4KMS4gQW5hbHl6ZSB0aGUgU01ULUxJQiB2YXJpYWJsZXMgcHJvdmlkZWQgd2l0aGluIHRoZSAnZGVjbGFyYXRpb25zJyBzZWN0aW9uIHRvIHVuZGVyc3RhbmQgYWxsIGFsbG93ZWQgdmFyaWFibGVzLCB0aGVpciB0eXBlcywgYW5kIGRlc2NyaXB0aW9ucy4KMi4gVHJhbnNsYXRlIHRoZSBuYXR1cmFsIGxhbmd1YWdlIHByZW1pc2VzIGFuZCBjb25jbHVzaW9uIGludG8gU01ULUxJQiBhc3NlcnRpb25zCjMuIFVzZSBvbmx5IHRoZSBjb25zdGFudHMgYW5kIGZ1bmN0aW9ucyBkZWNsYXJlZCBpbiB0aGUgZGVjbGFyYXRpb25zIHNlY3Rpb24KNC4gRWFjaCBhc3NlcnRpb24gc2hvdWxkIGJlIHdyYXBwZWQgaW4gKGFzc2VydCAuLi4pCjUuIFVzZSBwcm9wZXIgU01ULUxJQiBzeW50YXggZm9yIGxvZ2ljYWwgb3BlcmF0b3JzOiBhbmQsIG9yLCBub3QsID0+LCB4b3IsIGZvcmFsbCwgZXhpc3RzCjYuIERPIE5PVCBpbmNsdWRlIGFueSBYTUwgdGFncyBvciBtYXJrZG93biBmb3JtYXR0aW5nIC0gb3V0cHV0IG9ubHkgcHVyZSBTTVQtTElCIGFzc2VydGlvbnMKPC9pbnN0cnVjdGlvbnM+CgpIZXJlIGlzIGFuIGV4YW1wbGU6Cgo8ZXhhbXBsZT4KPGlucHV0PgpQcmVtaXNlczogQWxsIHBlb3BsZSB3aG8gcmVndWxhcmx5IGRyaW5rIGNvZmZlZSBhcmUgZGVwZW5kZW50IG9uIGNhZmZlaW5lLiBQZW9wbGUgcmVndWxhcmx5IGRyaW5rIGNvZmZlZSwgb3IgdGhleSBkb24ndCB3YW50IHRvIGJlIGFkZGljdGVkIHRvIGNhZmZlaW5lLCBvciBib3RoLiBObyBvbmUgd2hvIGRvZXNuJ3Qgd2FudCB0byBiZSBhZGRpY3RlZCB0byBjYWZmZWluZSBpcyBhd2FyZSB0aGF0IGNhZmZlaW5lIGlzIGEgZHJ1Zy4gUmluYSBpcyBlaXRoZXIgYSBzdHVkZW50IG9yIHVuYXdhcmUgdGhhdCBjYWZmZWluZSBpcyBhIGRydWcsIGJ1dCBub3QgYm90aC4gUmluYSBpcyBlaXRoZXIgZGVwZW5kZW50IG9uIGNhZmZlaW5lIG9yIGEgc3R1ZGVudCwgYnV0IG5vdCBib3RoLgpDb25jbHVzaW9uOiBSaW5hIGRvZXNuJ3Qgd2FudCB0byBiZSBhZGRpY3RlZCB0byBjYWZmZWluZSBvciBpcyB1bmF3YXJlIHRoYXQgY2FmZmVpbmUgaXMgYSBkcnVnLgo8L2lucHV0PgoKPGRlY2xhcmF0aW9ucz4KKGRlY2xhcmUtc29ydCBJbmRpdmlkdWFsKQooZGVjbGFyZS1jb25zdCByaW5hIEluZGl2aWR1YWwpCihkZWNsYXJlLWNvbnN0IGNvZmZlZSBJbmRpdmlkdWFsKQooZGVjbGFyZS1jb25zdCBjYWZmZWluZSBJbmRpdmlkdWFsKQooZGVjbGFyZS1mdW4gRHJpbmtSZWd1bGFybHkgKEluZGl2aWR1YWwgSW5kaXZpZHVhbCkgQm9vbCkKKGRlY2xhcmUtZnVuIElzRGVwZW5kZW50T24gKEluZGl2aWR1YWwgSW5kaXZpZHVhbCkgQm9vbCkKKGRlY2xhcmUtZnVuIFdhbnRUb0JlQWRkaWN0ZWRUbyAoSW5kaXZpZHVhbCBJbmRpdmlkdWFsKSBCb29sKQooZGVjbGFyZS1mdW4gQXdhcmVUaGF0RHJ1ZyAoSW5kaXZpZHVhbCBJbmRpdmlkdWFsKSBCb29sKQooZGVjbGFyZS1mdW4gU3R1ZGVudCAoSW5kaXZpZHVhbCkgQm9vbCkKPC9kZWNsYXJhdGlvbnM+CgpPdXRwdXQgKHB1cmUgU01ULUxJQiBhc3NlcnRpb25zIG9ubHkpOgooYXNzZXJ0IChmb3JhbGwgKCh4IEluZGl2aWR1YWwpKSAoPT4gKERyaW5rUmVndWxhcmx5IHggY29mZmVlKSAoSXNEZXBlbmRlbnRPbiB4IGNhZmZlaW5lKSkpKQooYXNzZXJ0IChmb3JhbGwgKCh4IEluZGl2aWR1YWwpKSAob3IgKERyaW5rUmVndWxhcmx5IHggY29mZmVlKSAobm90IChXYW50VG9CZUFkZGljdGVkVG8geCBjYWZmZWluZSkpKSkpCihhc3NlcnQgKGZvcmFsbCAoKHggSW5kaXZpZHVhbCkpICg9PiAobm90IChXYW50VG9CZUFkZGljdGVkVG8geCBjYWZmZWluZSkpIChub3QgKEF3YXJlVGhhdERydWcgeCBjYWZmZWluZSkpKSkpCihhc3NlcnQgKG5vdCAoeG9yIChTdHVkZW50IHJpbmEpIChub3QgKEF3YXJlVGhhdERydWcgcmluYSBjYWZmZWluZSkpKSkpCihhc3NlcnQgKG5vdCAoeG9yIChJc0RlcGVuZGVudE9uIHJpbmEgY2FmZmVpbmUpIChTdHVkZW50IHJpbmEpKSkpCihhc3NlcnQgKG9yIChub3QgKFdhbnRUb0JlQWRkaWN0ZWRUbyByaW5hIGNhZmZlaW5lKSkgKG5vdCAoQXdhcmVUaGF0RHJ1ZyByaW5hIGNhZmZlaW5lKSkpKQo8L2V4YW1wbGU+CgpOb3cgdHJhbnNsYXRlIHRoaXMgbmF0dXJhbCBsYW5ndWFnZSBpbnB1dCB1c2luZyB0aGUgcHJvdmlkZWQgZGVjbGFyYXRpb25zOgoKPGlucHV0PgpQcmVtaXNlczogTm8gc2FuZHdpY2ggY29va2llcyBhcmUgaGVhbHRoeS4KT3Jlb3MgYXJlIHNhbmR3aWNoIGNvb2tpZXMuCkNvbmNsdXNpb246IEFsbCBzYW5kd2ljaCBjb29raWVzIGFyZSBkZWxpY2lvdXMuCjwvaW5wdXQ+Cgo8ZGVjbGFyYXRpb25zPgooZGVjbGFyZS1zb3J0IEluZGl2aWR1YWwpCihkZWNsYXJlLWNvbnN0IG9yZW9zIEluZGl2aWR1YWwpCihkZWNsYXJlLWZ1biBTYW5kd2ljaENvb2tpZSAoSW5kaXZpZHVhbCkgQm9vbCkKKGRlY2xhcmUtZnVuIEhlYWx0aHkgKEluZGl2aWR1YWwpIEJvb2wpCihkZWNsYXJlLWZ1biBEZWxpY2lvdXMgKEluZGl2aWR1YWwpIEJvb2wpCjwvZGVjbGFyYXRpb25zPgo=) You are an expert in autoformalization - translating natural language logical reasoning into SMT-LIB format. Your task: Given natural language premises and conclusion, generate SMT-LIB assertions using the provided declarations. <instructions> 1. Analyze the SMT-LIB variables provided within the ’declarations’ section to understand all allowed variables, their types, and descriptions. 2. Translate the natural language premises and conclusion into SMT-LIB assertions 3. Use only the constants and functions declared in the declarations section 4. Each assertion should be wrapped in (assert ...) 5. Use proper SMT-LIB syntax for logical operators: and, or, not, =>, xor, forall, exists 6. DO NOT include any XML tags or markdown formatting - output only pure SMT-LIB assertions </instructions> Here is an example: <example> <input> Premises: All people who regularly drink coffee are dependent on caffeine. People regularly drink coffee, or they don’t␣want␣to␣be␣addicted␣to␣caffeine,␣or␣both.␣No␣one␣who␣doesn’t want to be addicted to caffeine is aware that caffeine is a drug. Rina is either a student or unaware that caffeine is a drug, but not both. Rina is either dependent on caffeine or a student, but not both. Conclusion: Rina doesn’t␣want␣to␣be␣addicted␣to␣caffeine␣or␣is␣unaware␣that␣caffeine␣is␣a␣drug. </input> <declarations> (declare-sort␣Individual) (declare-const␣rina␣Individual) (declare-const␣coffee␣Individual) (declare-const␣caffeine␣Individual) (declare-fun␣DrinkRegularly␣(Individual␣Individual)␣Bool) (declare-fun␣IsDependentOn␣(Individual␣Individual)␣Bool) (declare-fun␣WantToBeAddictedTo␣(Individual␣Individual)␣Bool) (declare-fun␣AwareThatDrug␣(Individual␣Individual)␣Bool) (declare-fun␣Student␣(Individual)␣Bool) </declarations> Output␣(pure␣SMT-LIB␣assertions␣only): (assert␣(forall␣((x␣Individual))␣(=>␣(DrinkRegularly␣x␣coffee)␣(IsDependentOn␣x␣caffeine)))) (assert␣(forall␣((x␣Individual))␣(or␣(DrinkRegularly␣x␣coffee)␣(not␣(WantToBeAddictedTo␣x␣caffeine))))) (assert␣(forall␣((x␣Individual))␣(=>␣(not␣(WantToBeAddictedTo␣x␣caffeine))␣(not␣(AwareThatDrug␣x␣caffeine))))) (assert␣(not␣(xor␣(Student␣rina)␣(not␣(AwareThatDrug␣rina␣caffeine))))) (assert␣(not␣(xor␣(IsDependentOn␣rina␣caffeine)␣(Student␣rina)))) (assert␣(or␣(not␣(WantToBeAddictedTo␣rina␣caffeine))␣(not␣(AwareThatDrug␣rina␣caffeine)))) </example> Now␣translate␣this␣natural␣language␣input␣using␣the␣provided␣declarations: <input> Premises:␣No␣sandwich␣cookies␣are␣healthy. Oreos␣are␣sandwich␣cookies. Conclusion:␣All␣sandwich␣cookies␣are␣delicious. </input> <declarations> (declare-sort␣Individual) (declare-const␣oreos␣Individual) (declare-fun␣SandwichCookie␣(Individual)␣Bool) (declare-fun␣Healthy␣(Individual)␣Bool) (declare-fun␣Delicious␣(Individual)␣Bool) </declarations>’

Experimental support, please [view the build logs](./2608.30258v1/__stdout.txt) for errors. Generated by [ L A T E xml ](https://math.nist.gov/~BMiller/LaTeXML/). 

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

