URL: https://arxiv.org/html/2509.22338 | FULL FETCH | 2026-09-24T01:49:34Z
warning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
URL: https://arxiv.org/html/2509.22338
Type: HTML
Length: 49015 chars

--- Content ---

##### Report GitHub Issue

×

Title:

Content selection saved. Describe the issue below:

Description:

Submit without GitHub Submit in GitHub

arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[ Back to arXiv ](/)

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) Report Issue [ Back to Abstract ](/abs/2509.22338v2 "Back to abstract page") [ Download PDF](/pdf/2509.22338v2 "Download PDF") [ ](javascript:toggleNavTOC\(\); "Toggle navigation") [ ](javascript:toggleReadingMode\(\); "Disable reading mode, show header and footer")

  1. Abstract
  2. 1 Introduction
  3. 2 Related Work
     1. Natural Language to First-Order Logic Translation
     2. Evaluation Metrics
  4. 3 Methodology
     1. 3.1 Model Selection
     2. 3.2 Datasets
     3. 3.3 Fine-tuning Procedure
     4. 3.4 Experiment Details
        1. 1\. Standard fine-tuning
        2. 2\. Token extension.
        3. 3\. Fixed predicate list.
        4. 4\. Fixed predicate list with noise.
        5. 5\. Two-step fine-tuning.
        6. 6\. Three-step curriculum fine-tuning.
        7. 7\. Multilingual fine-tuning.
        8. 8\. Comparison to Other Approaches
     5. 3.5 Evaluation
        1. 1\. Exact match.
        2. 2\. Logical equivalence.
        3. 3\. Predicate matching.
        4. Baseline comparisons.
  5. 4 Results
     1. 4.1 Results of baselines and standard fine-tunning
     2. 4.2 Results of further experiments
     3. 4.3 Results for logical arguments
  6. 5 Conclusion
     1. Acknowledgements
     2. Disclosure of Interests.
  7. References



[ License: CC BY 4.0 ](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2509.22338v2 [cs.CL] 30 Nov 2025

# Advancing Natural Language Formalization to First Order Logic with Fine-tuned LLMs

Felix Vossel  [](https://orcid.org/0009-0005-2367-9022 "ORCID 0009-0005-2367-9022") Affiliation: Osnabrück University, Germany  E-mail [{fvossel, till.mossakowski, bjoern.gehrke}@uos.de](mailto:%7Bfvossel,%20till.mossakowski,%20bjoern.gehrke%7D@uos.de) Till Mossakowski  [](https://orcid.org/0000-0002-8938-5204 "ORCID 0000-0002-8938-5204") Affiliation: Osnabrück University, Germany  E-mail [{fvossel, till.mossakowski, bjoern.gehrke}@uos.de](mailto:%7Bfvossel,%20till.mossakowski,%20bjoern.gehrke%7D@uos.de) Björn Gehrke  [](https://orcid.org/0009-0007-7488-0257 "ORCID 0009-0007-7488-0257") Affiliation: Osnabrück University, Germany  E-mail [{fvossel, till.mossakowski, bjoern.gehrke}@uos.de](mailto:%7Bfvossel,%20till.mossakowski,%20bjoern.gehrke%7D@uos.de) Affiliation: University of Zurich, Switzerland 

###### Abstract

Automating the translation of natural language to first-order logic (FOL) is crucial for knowledge representation and formal methods, yet remains challenging. We present a systematic evaluation of fine-tuned LLMs for this task, comparing architectures (encoder-decoder vs. decoder-only) and training strategies. Using the MALLS and Willow datasets, we explore techniques like vocabulary extension, predicate conditioning, and multilingual training, introducing metrics for exact match, logical equivalence, and predicate alignment. Our fine-tuned Flan-T5-XXL achieves 70% accuracy with predicate lists, outperforming GPT-4o and even the DeepSeek-R1-0528 model with CoT reasoning ability as well as symbolic systems like ccg2lambda. Key findings show: (1) predicate availability boosts performance by 15-20%, (2) T5 models surpass larger decoder-only LLMs, and (3) models generalize to unseen logical arguments (FOLIO dataset) without specific training. While structural logic translation proves robust, predicate extraction emerges as the main bottleneck.

###### Keywords: 

First Order Logic Fine-tuning Formalisation LLM Natural Language Processing. 

## 1 Introduction

Both knowledge representation and formal specification essentially depend on formalisation of knowledge as logical theories. The formalisation process is often a bottleneck, because high-quality formalisation requires manual human effort. As a result, in many ontologies, annotations in natural language are often much richer than the formalised logical theory. Likewise, informal requirement specifications in natural language are often much more extensive than formal specifications. This leads to a limitation of usefulness of formal methods like theorem proving, model finding and model checking, because the involved logical theory is often incomplete and only partially captures the informal natural language specification.

In order to address this problem, we aim to automate the translation from natural language to formal logic, more specifically, to first-order logic. While this problem has been solved to a certain extent by different methods, we aim at improving the quality of existing automated translation methods. Our approach uses large language models, which are fine-tuned and evaluated for this specific task, while being simultanesously available as general-purpose LLMs.

## 2 Related Work

##### Natural Language to First-Order Logic Translation

Translating NL to FOL can be used to enable logical reasoning with natural language. Early approaches to this problem relied mainly on symbolic methods. They used rule-based systems with hand-crafted linguistic rules and syntactic patterns, maping natural language structures directly to logical expressions. Pease and Murray developed an early translator from controlled English to logic for ontology-based knowledge representation [25]. Bos and Markert explored logical inference techniques for recognizing textual entailment [2]. They used model building from automated reasoning to approximate entailment relationships. Other systems often utilize frameworks like Combinatory Categorial Grammar (CCG) to build compositional semantic representations which can then be transformed to lambda expressions, FOL, or other formal languages. For example, ccg2lambda is a compositional semantics system generating logical semantic representations by combining semantic formulas bottom-up, guided by CCG parse trees [20].

Barker-Plummer et al. systematically analysed the difficulties of students during a translation task. They identified, among other, the ambiguity of natural language, complex sentence structures, and uninformative automated feedback as the students key challenges in mapping natural language to formal logic [1]. Cai and Yates addressed the identified scalability by developing techniques for large-scale semantic parsing [4]. They used schema matching and lexicon extension to improve performance on database-grounded tasks. Martínez-Gómez et al. further refined compositional semantics with the ccg2lambda system [20]. This system produces logical semantic representations by composing formulas bottom-up from CCG parse trees.

More recently, researchers have explored methods beyond purely symbolic systems. Lu et al. demonstrated the use of Dual Reinforcement Learning (DRL) to translate NL to both Propositional and First-Order Logic [19].

The emergence of large language models (LLMs) offered a new potential solution. However, LLMs often struggle with complex logical reasoning. Several recent works approach this limitations in different ways.

LogicLLaMA, a LLaMA-7B model fine-tuned specifically for NL-FOL translation, achieved performance comparable to GPT-4, but at a much lower computational cost [30]. During their work they created the dataset MALLS, a dataset of 34K high-quality NL-FOL pairs generated using GPT-4. Other frameworks combine LLMs with symbolic reasoners. For example, LogicLM first translates NL to FOL using LLMs and then applies symbolic reasoning [24]. Experiments showed this combination performed better than using the LLM directly for reasoning. Building on top of that, Lalwani et al. presented NL2FOL [13], a framework to translate NL to FOL in multiple steps with few-shot prompting of an LLM. It is designed to detect logical fallacies in natural language statements.

Thatikonda et al. focused on fine-tuning LLMs for NL to FOL translation [29]. They explored various fine-tuning strategies and data augmentation techniques. Their results show that fine-tuning significantly improves performance compared to zero-shot settings. They also found that incrementally translating premises and conclusions of (natural language) logical arguments can improve logical inference checking.

##### Evaluation Metrics

For the evaluation of NL to FOL translation tasks, various metrics are used in the literature. A common method is an exact, character-by-character match to evaluate whether a prediction of a model is correct [15, 19]. However, this metric is very strict as it does not account for syntactic variations in FOL expressions which do not change the underlying semantics.

Other approaches use logical equivalence as a more robust metric. Using automated theorem provers this metric checks whether the predicted FOL expression is logically equivalent to the ground truth expression, even if they are syntactically different [3, 11]. However, this approach either requires static signatures ensuring that the same predicates are used in both expressions or a normalization step to align predicate names. Experiments which include NL to FOL translation only as a subtask of logical entailment use the accuracy of the entailment task as a metric [29, 13].

Yang et al. defined a new metric called “Logical Equivalence” which is also used in other experiments [30, 17]. In contrast to the previous methods, which rate a prediction either “correct” or “incorrect”, this metric assigns a score based on the number of matching propositional valuations. However, it is questionable whether this metric is suitable for FOL, as it does not account for the complexity of quantifiers and a prediction which differs in only one valuation can still be worse than a prediction which differs in many valuations. For example, A∧B∧C∧DA\wedge B\wedge C\wedge D is closer to A∧BA\wedge B than to 𝑓𝑎𝑙𝑠𝑒\mathit{false}, but differs from the former for 316\frac{3}{16} of the valuations, but from latter only for 116\frac{1}{16}.

## 3 Methodology

### 3.1 Model Selection

For our formalization task, we employ both encoder-decoder and decoder-only large language models (LLMs) with different sizes to enable a systematic comparison across architectures and model sizes. Encoder-decoder models, such as T5-base [26], T5-3B [26], and Flan-T5-XXL [5], are chosen based on their successful application to structured prediction tasks like text-to-text translation and semantic parsing [16], which parallel the formality and compositionality of natural language to logic translation. For the decoder-only setting, we fine-tune LLaMA3.1-8B [10], which is widely used in recent research on fine tuning LLMs for formal language and reasoning tasks [30], as well as Mistral-24B, recognized for its strong performance and efficiency [21]. Additionally, we include Olmo-32B [22] as a representative of modern open-source approaches in large-scale language modeling.

This selection enables an analysis of architectural influences while spanning a diverse range of parameter sizes and recent model families. Table 1 summarizes the models considered in our experiments.

Model | Architecture | Parameters | Reference  
---|---|---|---  
T5-base | Encoder-Decoder | 220M | [26]  
T5-3B | Encoder-Decoder | 3B | [26]  
Flan-T5-XXL | Encoder-Decoder | 11B | [5]  
Olmo-32B | Decoder-Only | 32B | [22]  
Mistral-24B | Decoder-Only | 24B | [21]  
LLaMA3.1-8B | Decoder-Only | 8B | [10]  
Table 1: Large language models used for fine-tuning in our experiments.

### 3.2 Datasets

For our experiments, we leverage two of the largest publicly available Natural Language to First-Order Logic (NL-FOL) datasets: MALLS [30] and Willow [9]. These datasets were selected because their considerable size makes them more suitable for training large models than, for instance, FOLIO [11], and they contain significantly more complex natural language utterances compared to simpler resources such as Text2Log [15].

Each instance in both datasets consists of a natural language string paired with its corresponding FOL string. To ensure consistency and facilitate model training, we store the combined corpus in a unified json format, where each record contains both fields. For example:

"NL": | "Not every student is hardworking."  
---|---  
"FOL": | "¬∀\forallx (Student(x) →\rightarrow Hardworking(x))"  
  
Property | Value | Description  
---|---|---  
Total examples | 49950 | NL→\rightarrowFOL pairs in dataset  
Training examples | 35964 | Size of train set  
Validation examples | 3996 | Size of validation set  
Test examples | 9990 | Size of test set  
Unique predicates | 62981 | Distinct predicates occurring in FOL  
Unique constants | 2011 | Distinct constants (entities/objects) in FOL  
Avg. NL length (chars) | 86.73 | Mean input (NL) string length [characters]  
Avg. FOL length (chars) | 85.02 | Mean FOL string length [characters]  
Avg. quantifiers per sample | 1.56 | Mean number of quantifiers per FOL entry  
Avg. formula depth per sample | 6.75 | Mean parse tree depth per FOL formula  
Avg. logical connectives/sample | 3.68 | Mean number of logical connectives (∧,∨,¬,→\wedge,\vee,\neg,\rightarrow)  
Table 2: Summary statistics for our unified NL-FOL dataset.

### 3.3 Fine-tuning Procedure

To adapt the selected pre-trained language models to the NL-to-FOL formalization task, we fine-tune each model on the combined training split described above. For the decoder-only models (LLaMA3.1-8B, Mistral-24B, and Olmo-32B), we apply Low-Rank Adaptation (LoRA) [12] with rank r=16r=16, scaling factor α=32\alpha=32, a dropout rate of 0.05, and targeting all attention and feed-forward projection layers, following recommended settings for large-scale language modeling [12]. For Flan-T5-XXL, LoRA was analogously applied to attention and feed-forward layers. T5-base and T5-3B were trained with full fine-tuning. In all LoRa settings mixed precision training was enabled.

All models were trained with the AdamW optimizer [18], a maximum of 12 epochs, early stopping (patience 4) based on validation loss, and cosine (Decoder-Only models)/linear (T5 models) learning rate scheduling with a warmup ratio of 0.05 and weight decay of 0.01. Batch sizes and learning rates are detailed in Table 3. Multi-GPU training was used for larger models as required.

All experiments were conducted on a high-performance computing cluster equipped with Intel® Xeon® Platinum 8480+ CPUs and either NVIDIA H100 80GB or NVIDIA A100-SXM4-80GB GPUs. The cluster and computational resources were funded by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) – 456666331.

Except for T5-base and T5-3B (trained in float32), all models were fine-tuned using bfloat16 precision. Distributed training was performed using the NCCL backend with unused parameter detection disabled. All experiments leveraged the HuggingFace transformers, peft, and trl libraries.

Table 3 summarizes the main training hyperparameters and hardware used for each model.

Model | Arch. | LoRA | F-FT | Batch Size | LR | Max Epochs | GPUs  
---|---|---|---|---|---|---|---  
T5-base | Enc-Dec | – | ✓ | 8 | 1×10−31\times 10^{-3} | 12 | 1  
T5-3B | Enc-Dec | – | ✓ | 8 | 1×10−41\times 10^{-4} | 12 | 1  
Flan-T5-XXL | Enc-Dec | ✓ | – | 8 | 1×10−41\times 10^{-4} | 12 | 1  
LLaMA3.1-8B | Dec-Only | ✓ | – | 16 | 1×10−51\times 10^{-5} | 12 | 1  
Mistral-24B | Dec-Only | ✓ | – | 32 | 1×10−51\times 10^{-5} | 12 | 2  
Olmo-32B | Dec-Only | ✓ | – | 32 | 1×10−51\times 10^{-5} | 12 | 2  
Table 3: Training hyperparameters and hardware for model fine-tuning. LR denotes learning rate; LoRA indicates Low-Rank Adaptation; F-FT denotes full fine-tuning. 

### 3.4 Experiment Details

We design a sequence of eight experiments to systematically analyze the impact of different fine-tuning strategies, data augmentations, and evaluation settings on the NL-to-FOL formalization task. Each experiment builds on the findings and methodology of the previous ones, allowing us to isolate and compare the effects of key choices in model adaptation.

##### 1\. Standard fine-tuning

We fine-tune all models on pairs of natural language statements and their corresponding FOL expressions in a standard sequence-to-sequence or causal language modeling setting. For decoder-only and chat-based transformer models, we use a ChatML-style prompt structure: each instance is formatted into system, user, and assistant messages, with the system prompt instructing the model to output only the FOL formula (using the set ∀,∃,¬,∧,∨,→,↔,⊕\forall,\exists,\neg,\wedge,\vee,\rightarrow,\leftrightarrow,\oplus) and to begin with “Φ=\Phi=”. For encoder–decoder (T5) models, we use a simple input–output format, prepending the source with "translate English natural language statements into first-order logic (FOL): " and setting the target to the corresponding FOL expression. Since T5 models rely on the SentencePiece tokenizer, they are unable to generate logical operator symbols by default. Consequently, all logical operators were substituted with their respective textual forms. The prompt templates are automatically converted to match the input requirements of each model architecture. This baseline serves as our primary reference point for all subsequent augmentations and curriculum strategies.

After fine-tuning, we save the resulting model and evaluate its performance on the test set. For decoder-only models, text generation is performed with sampling enabled and a maximum of 250 new tokens; all other generation parameters are left at their default values. For T5 models, we use beam search with five beams, a maximum output length of 256 tokens, a length penalty of 2.0, and early stopping disabled; the remaining settings follow the respective model defaults.

##### 2\. Token extension.

In this experiment, we augment the model’s vocabulary with dedicated tokens for all logical connectives and quantifiers used in First-Order Logic (∀\forall, ∃\exists, ¬\neg, ∧\wedge, ∨\vee, →\rightarrow, ↔\leftrightarrow, ⊕\oplus). Each special symbol is represented as a unique token in the tokenizer and the model’s embedding matrix, ensuring they are treated as atomic units during both input encoding and output generation. This direct symbolic mapping facilitates the handling of logical structure and reduces token fragmentation of FOL expressions.

A key motivation for this experiment stems from the observation that models like T5, which rely on the SentencePiece tokenizer, cannot represent such symbols by default. In the baseline scenario, logical operators had to be replaced with textual tokens (e.g., “forall” instead of “∀\forall”), which may introduce ambiguity or inefficiency. By explicitly extending the vocabulary with the required logic symbols, we aim to assess the impact of direct symbolic encoding on formalization accuracy and model performance. Training and evaluation procedures otherwise mirror those of the baseline.

##### 3\. Fixed predicate list.

In this experiment, for each NL–FOL pair in the dataset, the model receives an explicit, alphabetically sorted list of predicates that must appear in the FOL formalization, encouraging precise and consistent predicate usage. The list is sorted to ensure that the order of predicates does not reveal information about the logical structure of the FOL expression. This experimental setup is motivated by initial evaluation results, which indicated that one of the main challenges for large language models is correctly identifying the relevant predicates from the input. To test the hypothesis that predicate selection poses a greater difficulty than generating the correct logical structure, we provide the gold predicate list as an additional input to the model. A more detailed analysis of this issue is presented in our evaluation metrics section.

##### 4\. Fixed predicate list with noise.

In this experiment, for each NL–FOL pair in the dataset, the model receives an explicit, alphabetically sorted list of predicates that must appear in the FOL formalization, but this list is augmented with additional randomly sampled predicates drawn from the predicates used in five other FOL formulas. This setup requires the model to robustly distinguish the relevant predicates among distractors when constructing the FOL expression. Such a scenario is also of practical importance, as in many downstream applications one may only be able to provide a superset of potentially relevant predicates, rather than the exact set needed for a particular formalization.

##### 5\. Two-step fine-tuning.

Building on the practical consideration that gold predicate lists are rarely available in real-world scenarios, we design a two-step curriculum: In the first step, models are trained to extract the relevant predicates from the natural language input, producing a predicted predicate list. In the second step, this predicted list is provided as input to the model trained in Experiment 3 (fixed predicate list) for FOL formalization. This approach allows us to investigate whether intermediate predicate prediction can facilitate more accurate and robust logic translation when compared to direct end-to-end training.

##### 6\. Three-step curriculum fine-tuning.

As an alternative to the two-step fine-tuning in Experiment 5, we address the predicate prediction challenge through a curriculum learning scheme with three stages. In the first stage, models are trained with the exact predicate list provided as input (as in Experiment 3). In the second stage, the input predicate list is augmented with noisy distractors (as in Experiment 4), increasing task difficulty. Finally, models are trained on the standard NL–FOL formalization task without any predicate hints. This progressive training approach is designed to gradually reduce the model’s reliance on explicit predicate information, with the goal of improving its ability to correctly identify predicates and generate FOL expressions in a more realistic, unprompted setting.

##### 7\. Multilingual fine-tuning.

In this experiment, we explore a fundamentally different approach to improving predicate understanding and generalization by leveraging multilingual training data. Specifically, we use the Mistral model and translate all natural language statements in the training set into German and French, two languages that are frequently covered in LLM pretraining alongside English. The corresponding FOL predicates, however, remain in English, serving as a consistent formal target language. Training follows the same procedure as in Experiment 1, but now includes NL–FOL pairs in three languages, while validation and test sets remain in the original English. This setting encourages the model to capture the semantic meaning of predicates independently of source language syntax, since predicates can no longer be directly mapped from the NL input. Our goal is to evaluate the cross-lingual robustness of logical formalization and to test whether multilingual exposure improves predicate abstraction and transfer.

##### 8\. Comparison to Other Approaches

While previous experiments evaluated the performance of our models either internally or in comparison to other neural methods following the same approach, this section extends the analysis by comparing LLaMA3.1-8B to LLaMA-2 13B [29] and the symbolic system ccg2lambda. For the comparison with LLaMA-2 13B, we use the eval subset of the FOLIO dataset, noticing that our model has not been trained on FOLIO. For the evaluation against ccg2lambda, we preprocessed the natural language inputs by removing all commas and appending a period to each sentence, in accordance with the input format expected by the tool.

Each experiment is designed to isolate a specific methodological or representational variable, enabling a systematic analysis of model capabilities and the underlying task. In the following, we present the detailed setup and training procedure for each experiment; results and discussion are provided in the results Section.

### 3.5 Evaluation

With all models and experimental variants in place, we systematically assess performance using three complementary metrics and robust baseline comparisons.

##### 1\. Exact match.

Exact match evaluates whether the predicted and ground truth FOL expressions are identical under whitespace-insensitive string comparison, thereby abstracting away from superficial formatting differences.

##### 2\. Logical equivalence.

To account for syntactically different but semantically equivalent expressions, we determine logical equivalence using an automated theorem proving (ATP) approach. Both predicted and ground truth FOL expressions are parsed using a context-free grammar that we specifically designed and implemented with the Lark parsing library [27]. The resulting syntax trees are then transformed into Z3 format. To check for logical equivalence, we construct a Z3 solver [6] to test the unsatisfiability of the negated bi-implication ¬(φ↔ψ)\lnot(\varphi\leftrightarrow\psi), where φ\varphi denotes the model output and ψ\psi the ground truth formula. We use the Z3 solver with a timeout of 10 seconds for each check. If the solver establishes unsatisfiability within this timeframe, the formulas are considered logically equivalent. Our approach follows the general structure proposed by [3].

##### 3\. Predicate matching.

To further disentangle errors caused by incorrect predicate naming from structural or logical errors, we introduce a predicate matching step. For each predicted FOL expression, predicates are mapped to ground truth predicates using the normalized Levenshtein distance (threshold 0.6) [14]. Once predicates are aligned, both exact match and logical equivalence are recomputed on the normalized formulas. This procedure provides additional insight into whether errors are due to predicate identification or deeper logical misunderstandings.

##### Baseline comparisons.

For Experiment 1, we first establish a baseline by evaluating each model on the dataset without any fine-tuning, in order to verify that fine-tuning indeed improves performance. We further compare the fine-tuned models to strong proprietary, open-source and reasoning models—namely, GPT-4o [23], DeepSeek-R1-0528 [8] with a hybrid 2500 tokens CoT setting, DeepSeek-V3-0324 [7] and LogicLLaMA [30]—for an additional performance reference. Notably, LogicLLaMA was trained on the MALLS dataset but not on Willow, providing an informative benchmark for both in-domain and out-of-domain generalization. In addition, we evaluate the symbolic system ccg2lambda on the dataset to obtain a symbolic reference point for the neural baselines established in this experiment.

For Experiment 2, the results of Experiment 1 (i.e., fine-tuned model performance) are used as the baseline to assess whether the vocabulary extension yields further improvements.

For Experiments 6 and 7, Experiment 1 also serves as the baseline, allowing us to assess the relative benefits of three-step curriculum learning and multilingual training, respectively.

For Experiment 5, we use both the model’s zero-shot or pre-trained performance (without any targeted fine-tuning) and the performance from Experiment 1 as baselines, in order to capture the potential gains from intermediate predicate prediction in addition to direct fine-tuning.

For Experiments 3 and 4, we compare both to the model’s zero-shot or pre-trained performance and to the Experiment 1 baseline (i.e., standard fine-tuning). This allows us to measure not only the incremental benefit of providing explicit or noisy predicate lists, but also the overall performance gain compared to conventional fine-tuning without additional predicate information. It is important to note that zero-shot or pre-trained performance is only evaluated for the decoder-only models, since the T5 models do not produce meaningful FOL translations without fine-tuning

In all cases, this systematic baseline setup enables robust conclusions on the effectiveness of each method and fair comparisons across experimental conditions.

## 4 Results

### 4.1 Results of baselines and standard fine-tunning

Table 4 compares the accuracy of the evaluated LLMs in the baseline setup. As expected, GPT-4o, DeepSeek-R1-0528, DeepSeek-V3-0324 and LogicLLaMA perform better than the other models, particularly in the few-shot setting. This can be attributed to significantly larger scale and broader pretraining corpus, as well as to the fact that LogicLLaMA was trained on a subset of our dataset, which may overlap with the test set. Overall, the higher scores for logical equivalence compared to exact match can likely be attributed to the model’s tendency to produce non-canonical formula representations, as exemplified in Table 6. The results after predicate normalization are particularly insightful, as they provide initial evidence supporting our hypothesis: LLMs struggle more with correctly reproducing predicate names than with capturing the underlying logical structure.

In Table 5, we compare the accuracy of the fine-tuned LLMs in the baseline fine-tuning setup. Among the evaluated models, Olmo-32B performs the worst across all metrics. This may be attributed to its relatively limited pretraining, suggesting that large language models already acquire a rudimentary understanding of logical structure from pretraining on natural language alone.

If this hypothesis holds, the performance of the T5 models becomes particularly noteworthy. Despite being encoder-decoder models—unlike the decoder-only architecture of the other LLMs—they perform on par with or even outperform larger models such as LLaMA3.1-8B and Mistral-24B. This indicates that T5 models might benefit from their architecture, which explicitly encodes the input sequence before generating output. Such structural guidance during encoding could facilitate the mapping from natural language to logical forms, especially in tasks that require understanding and transformation rather than open-ended generation.

Model | Exact | Exact (Pred.) | Equiv. | Equiv. (Pred.)  
---|---|---|---|---  
LLaMA3.1-8B* | 2.37 | 4.10 | 4.17 | 6.83  
Mistral-24B* | 7.24 | 10.73 | 11.44 | 17.57  
Olmo-32B* | 1.91 | 3.44 | 4.37 | 8.58  
GPT-4o* | 8.16 | 11.92 | 13.02 | 20.28  
LogicLLaMA* | 0.97 | 1.16 | 3.06 | 5.27  
GPT-4o** | 10.98 | 16.60 | 18.22 | 29.08  
LogicLLaMA** | 16.05 | 24.79 | 18.71 | 29.45  
DeepSeek-V3-0324** | 10.33 | 15.33 | 15.53 | 23.17  
DeepSeek-R1-0528**** | 8.27 | 12.87 | 18.11 | 30.53  
ccg2lambda*** | 0.00 | 0.00 | 0.27 | 0.43  
Table 4:  Baseline: Model accuracy by exact and logical match, before/after predicate normalization without fine tuning. *zero-shot **few-shot *** only 8225 NL sentences could be parsed. ****CoT reasoning was used in a few-shot scenario. All scores are in %.  Model | Exact | Exact (Pred.) | Equiv. | Equiv. (Pred.)  
---|---|---|---|---  
T5-base | 29.52 | 44.33 | 32.71 | 50.17  
T5-3B | 32.96 | 45.85 | 36.21 | 51.54  
Flan-T5-XXL | 35.79 | 49.47 | 38.83 | 54.79  
LLaMA3.1-8B | 28.46 | 41.87 | 32.02 | 47.90  
Mistral-24B | 34.83 | 48.23 | 38.18 | 53.92  
Olmo-32B | 24.29 | 36.49 | 27.89 | 42.66  
Table 5:  Experiment 1: Model accuracy by exact and logical match, before/after predicate normalization with standard fine tuning. All scores are in %.  NL (Input) |  Tomatoes are red and round, while cucumbers are green and elongated.  
---|---  
FOL_PRED |  ∀x⁡(Tomato​(x)→(Red​(x)∧Round​(x)))\forall x\,(\text{Tomato}(x)\rightarrow(\text{Red}(x)\land\text{Round}(x)))  
|  ∧∀y(Cucumber(y)→(Green(y)∧Elongated(y)))\land\ \forall y\,(\text{Cucumber}(y)\rightarrow(\text{Green}(y)\land\text{Elongated}(y)))  
FOL_GT |  ∀x​∀y⁡(Tomato​(x)→(Red​(x)∧Round​(x)))\forall x\,\forall y\,(\text{Tomato}(x)\rightarrow(\text{Red}(x)\land\text{Round}(x)))  
|  ∧(Cucumber​(y)→(Green​(y)∧Elongated​(y)))\land\ (\text{Cucumber}(y)\rightarrow(\text{Green}(y)\land\text{Elongated}(y)))  
Table 6: Equivalent but not identical FOL translations. FOL_PRED is the formula predicted by the FLAN-T5-XXL model and FOL_GT is the ground-truth formula.

In contrast, ccg2lambda fails to produce correct logical forms for the vast majority of inputs (0.00% on not/predicate matched exact match and 0.43% on predicate matched equivalence match). Its performance is severely constrained by the rigidity of its manually constructed grammar, which lacks the flexibility to handle the syntactic and semantic variety present in natural language. These findings highlight the superiority of neural approaches over purely symbolic systems in the task of semantic parsing.

### 4.2 Results of further experiments

Adding explicit tokens for logical symbols yielded only marginal improvements for Olmo-32B and T5-base (less than one percentage point), while other models showed slight performance drops. This suggests that representing logical symbols using multiple subword tokens does not substantially hinder model understanding, and dedicated tokens offer no consistent performance benefit.

Models fine-tuned with ground-truth predicate names substantially outperform all other configurations. The best-performing model (Flan-T5-XXL) achieves 63.45% on the exact match and 70.27% on the equivalence match with only marginal improvements if predicate matching (63.54% on exact match) was applied. Adding noise to predicate names leads to a slight performance drop, but the effect is marginal, confirming that the main benefit stems from access to correct predicate structure rather than stability under perturbations (Table 7).

By contrast, initial training for predicate name prediction yields considerably worse results. For example, FLAN-T5-XXL reaches only 25.96% on the exact match and 28.26% on the equivalence match. If predicate matching was applied FLAN-T5-XXL reaches 35.11% on the exact match and 38.95% on the equivalence match. This confirms our hypothesis that exact predicate alignment presents a hard constraint. Given the more than 60,000 unique predicates in the dataset and substantial variation in predicate usage, models struggle to generalize under these strict conditions.

The stepwise training procedure—starting with gold predicates, followed by noisy and then free-form formulas—also underperforms relative to the baseline, despite access to complete target structures during early training. FLAN-T5-XXL achieves just 33.83% on the exact match and 36.69% on the equivalence match, suggesting that training on ground-truth predicates might lead to overfitting on the given predicates which then reduces final performance.

Multilingual training leads to only minor degradation compared to monolingual models. T5-3B achieves 30.33% on the exact match and 32.90% on the equivalence match, demonstrating that multilingual inputs are compatible with consistent logical form generation and may support future cross-lingual extensions.

Model | Exact | Exact (Pred.) | Equiv. | Equiv. (Pred.)  
---|---|---|---|---  
T5-base | 57.02 | 57.92 | 63.22 | 64.34  
T5-3B | 60.04 | 60.35 | 66.28 | 66.66  
Flan-T5-XXL | 62.39 | 62.53 | 69.06 | 69.23  
LLaMA3.1-8B | 43.76 | 43.91 | 53.68 | 53.95  
Mistral-24B | 50.80 | 50.89 | 59.93 | 60.07  
Olmo-32B | 36.58 | 36.90 | 46.15 | 46.65  
Table 7:  Experiment 4: Model accuracy by exact and logical match, before/after predicate normalization with fine-tuning on fixed predicate list with noise. All scores are in %. 

### 4.3 Results for logical arguments

[29] argue that with traditional datasets, it is difficult to assess the quality of NL to FOL translations automatically. As an automated santiy check, they suggest to use hand-crafted sets of natural language logical arguments, whose (in)validity is known. Then, after translation to FOL, (in)validity of the argument can be checked with an automated theorem prover, and if the validity disagrees with the manually annoteted one, an error in the translation has been spotted. FOLIO [11] is such a dataset of NL arguments.

Our model achieves competitive results (39.70% valid conclusions) compared to the best version of LLaMA-2 13B (37.44% valid conlsusions with inkremental fine-tuning and predicate verifier), even though it was not trained on the FOLIO dataset. This suggests that the iterative fine-tuning procedure on FOLIO proposed by previous work [29] is not strictly required to attain strong performance. Additionally, our model exhibits robust behavior in multi-premise inference settings, where earlier premises are provided as contextual input—despite such scenarios not being part of the training data. This points to the model’s capacity to generalize to more complex reasoning setups without explicit supervision.

## 5 Conclusion

For the task of translating natural language into first-order logic, we have fined-tuned several large language models using the MALLS and Willow datasets, and have conducted experiments with several settings. An important aspect was the provision or learning of a list of predicate names that shall occur in the translation. While the provision of ground-truth predicate names greatly helps, learning them in a two-step process did not lead to good results. Our fine-tuned Flan-T5-XXL model with 11 billion parameters, can outperform baselines like GPT-4o, LogicLLaMA and even DeepSeek-R1-0528, as well as a symbolic baseline. The accuracy of translations of natural language arguments from the FOLIO dataset is comparable to the baseline (note that here only (in)validity of the translated argument is considered). The source code for our fine-tuned models is available on [GitHub](https://github.com/fvossel/NL2FOL), and the models themselves can be accessed on [Hugging Face](https://huggingface.co/collections/fvossel/nl-to-fol-685464200cad67e2cd5b0e73). A common mistake in NL to FOL translation that is also present in the MALLS dataset is the confusion of hard-to-recognise Aristotelian forms: “A pineapple is a fruit with spiky skin” is translated to

| ∃x⁡(P​i​n​e​a​p​p​l​e​(x)∧F​r​u​i​t​(x)∧S​p​i​k​y​S​k​i​n​(x)).\exists x(Pineapple(x)\wedge Fruit(x)\wedge SpikySkin(x)). |   
---|---|---  
  
Despite being trained with MALLS, our model correctly translates this to

| OPEN∀x⁡(P​i​n​e​a​p​p​l​e​(x)→(F​r​u​i​t​(x)∧H​a​s​S​p​i​k​y​S​k​i​n​(x)))),\forall x(Pineapple(x)\to(Fruit(x)\wedge HasSpikySkin(x)))), |   
---|---|---  
  
which can be explained with the usage of the Willow dataset that translates such situations correctly.

We observe that reasoning strategies such as CoT can sometimes degrade performance in NL-to-FOL translation, as initially correct outputs are overwritten during the reasoning process. This aligns with the illusion of thinking phenomenon described by Apple [28]. Future work may benefit from a two-stage approach, where base model outputs are first generated and then verified or refined using a reasoning model, as suggested by Thatikonda et al [29].

Flan-T5-XXL achieves 55% accuracy without a predicate list and 70% with a noisy one, as is realistic in practice. A correlation of −0.318-0.318 between sentence length and exact match further suggests that shorter sentences are translated more accurately. Future work includes improving predicate extraction—e.g., splitting composite names like ProtectFromRain, tokenizing given predicate names, and correcting errors in the MALLS dataset to boost accuracy.

Furthermore, we plan to correct the errors in the MALLS dataset, in order to improve accuracy.

As another line of future work, we plan to cover also less and more expressive logics used for specification and ontology development.

#### Acknowledgements

The authors want to thank Christoph Benzmüller, Dave Barker-Plummer and İbrahim Ethem Deveci for helpful discussions.

This work was supported by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) – 456666331.

#### Disclosure of Interests.

The authors have no competing interests to declare that are relevant to the content of this article.

## References

  * [1] D. Barker-Plummer, R. Cox, and R. Dale (2009) Dimensions of difficulty in translating natural language into first order logic..  International Working Group on Educational Data Mining.  Cited by: §2. 
  * [2] J. Bos and K. Markert (2005) Recognising textual entailment with logical inference.  In HLT ’05,  Vancouver, British Columbia, Canada, pp. 628–635.  External Links: [Document](https://dx.doi.org/10.3115/1220575.1220654) Cited by: §2. 
  * [3] A. Brunello et al. (2025) Evaluating LLMs Capabilities at Natural Language to Logic Translation: A Preliminary Investigation.  In CEUR workshop proceedings,  Vol. 3904, pp. 103–110.  Cited by: §2, §3.5. 
  * [4] Q. Cai and A. Yates (2013) Large-scale Semantic Parsing via Schema Matching and Lexicon Extension.  In Proceedings of the 51st Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers),  pp. 423–433.  Cited by: §2. 
  * [5] H. W. Chung, L. Hou, S. Longpre, B. Zoph, Y. Tay, W. Fedus, Y. Li, X. Wang, M. Dehghani, S. Brahma, et al. (2024) Scaling instruction-finetuned language models.  Journal of Machine Learning Research 25 (70), pp. 1–53.  Cited by: §3.1, Table 1. 
  * [6] L. de Moura et al. (2024) Z3 Theorem Prover.  Note: <https://github.com/Z3Prover/z3>Accessed: 2025-06-07 Cited by: §3.5. 
  * [7] DeepSeek-AI (2024) DeepSeek-v3 technical report.  External Links: 2412.19437, [Link](https://arxiv.org/abs/2412.19437) Cited by: §3.5. 
  * [8] DeepSeek-AI (2025) DeepSeek-r1: incentivizing reasoning capability in llms via reinforcement learning.  External Links: 2501.12948, [Link](https://arxiv.org/abs/2501.12948) Cited by: §3.5. 
  * [9] I. E. Deveci (2024) Transformer models for translating natural language sentences into formal logical expressions.  Master’s Thesis, Middle East Technical University (Turkey).  Cited by: §3.2. 
  * [10] A. Grattafiori et al. (2024) The LLama 3 herd of models.  arXiv preprint arXiv:2407.21783.  Cited by: §3.1, Table 1. 
  * [11] S. Han et al. (2022) Folio: natural language reasoning with first-order logic.  arXiv preprint arXiv:2209.00840.  Cited by: §2, §3.2, §4.3. 
  * [12] E. J. Hu, Y. Shen, P. Wallis, Z. Allen-Zhu, Y. Li, S. Wang, L. Wang, W. Chen, et al. (2022) Lora: low-rank adaptation of large language models..  ICLR 1 (2), pp. 3.  Cited by: §3.3. 
  * [13] A. Lalwani et al. (2024) NL2FOL: translating natural language to first-order logic for logical fallacy detection.  arXiv preprint arXiv:2405.02318.  Cited by: §2, §2. 
  * [14] V. I. Levenshtein et al. (1966) Binary codes capable of correcting deletions, insertions, and reversals.  In Soviet physics doklady,  8, pp. 707–710.  Cited by: §3.5. 
  * [15] O. Levkovskyi and W. Li (2021) Generating Predicate Logic Expressions from Natural Language.  In SoutheastCon 2021,  Atlanta, GA, USA, pp. 1–8.  External Links: [Document](https://dx.doi.org/10.1109/SoutheastCon45413.2021.9401852), ISBN 978-1-6654-0379-5 Cited by: §2, §3.2. 
  * [16] Y. Li, Z. Su, Y. Li, H. Zhang, S. Wang, W. Wu, and Y. Zhang (2023) T5-sr: a unified seq-to-seq decoding strategy for semantic parsing.  In ICASSP 2023-2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP),  pp. 1–5.  Cited by: §3.1. 
  * [17] J. Liu (2025) Few-shot natural language to first-order logic translation via code generation.  In Proceedings of the 2025 Conference of the Nations of the Americas Chapter of the Association for Computational Linguistics: Human Language Technologies (Volume 1: Long Papers),  pp. 10939–10960.  Cited by: §2. 
  * [18] I. Loshchilov and F. Hutter (2017) Decoupled weight decay regularization.  arXiv preprint arXiv:1711.05101.  Cited by: §3.3. 
  * [19] X. Lu, J. Liu, Z. Gu, H. Tong, C. Xie, J. Huang, Y. Xiao, and W. Wang (2022) Parsing natural language into propositional and first-order logic with dual reinforcement learning.  In Proceedings of the 29th International Conference on Computational Linguistics,  pp. 5419–5431.  Cited by: §2, §2. 
  * [20] P. Martínez-Gómez, K. Mineshima, Y. Miyao, and D. Bekki (2016) Ccg2lambda: A Compositional Semantics System.  In Proceedings of ACL-2016 System Demonstrations,  Berlin, Germany, pp. 85–90.  External Links: [Document](https://dx.doi.org/10.18653/v1/P16-4015) Cited by: §2, §2. 
  * [21] Mistral AI Team (2025) Mistral small 3: apache 2.0, 81% mmlu, 150 tokens/s.  Note: Accessed on June 7, 2025 External Links: [Link](https://mistral.ai/news/mistral-small-3) Cited by: §3.1, Table 1. 
  * [22] T. OLMo, P. Walsh, L. Soldaini, D. Groeneveld, K. Lo, S. Arora, A. Bhagia, Y. Gu, S. Huang, M. Jordan, et al. (2024) 2 olmo 2 furious.  arXiv preprint arXiv:2501.00656.  Cited by: §3.1, Table 1. 
  * [23] OpenAI (2024) GPT-4o: openai’s new flagship model.  Note: <https://openai.com/index/gpt-4o>Accessed: 2025-06-07 Cited by: §3.5. 
  * [24] L. Pan, A. Albalak, X. Wang, and W. Y. Wang (2023) Logic-LM: empowering large language models with symbolic solvers for faithful logical reasoning.  External Links: 2305.12295, [Link](https://arxiv.org/abs/2305.12295) Cited by: §2. 
  * [25] A. Pease and W. Murray (2003) An english to logic translator for ontology-based knowledge representation languages.  In International Conference on Natural Language Processing and Knowledge Engineering,,  pp. 777–783.  Cited by: §2. 
  * [26] C. Raffel, N. Shazeer, A. Roberts, K. Lee, S. Narang, M. Matena, Y. Zhou, W. Li, and P. J. Liu (2020) Exploring the limits of transfer learning with a unified text-to-text transformer.  Journal of machine learning research 21 (140), pp. 1–67.  Cited by: §3.1, Table 1, Table 1. 
  * [27] E. Shinan et al. (2024) Lark: A modern parsing library for Python.  Note: <https://github.com/lark-parser/lark>Accessed: 2025-06-07 Cited by: §3.5. 
  * [28] P. Shojaee et al. (2025) The illusion of thinking: understanding the strengths and limitations of reasoning models via the lens of problem complexity.  External Links: [Link](https://ml-site.cdn-apple.com/papers/the-illusion-of-thinking.pdf) Cited by: §5. 
  * [29] R. K. Thatikonda, J. Han, W. Buntine, and E. Shareghi (2024) Strategies for improving NL-to-FOL translation with LLMs: data generation, incremental fine-tuning, and verification.  arXiv:2409.16461.  Cited by: §2, §2, §3.4, §4.3, §4.3, §5. 
  * [30] Y. Yang, S. Xiong, A. Payani, E. Shareghi, and F. Fekri (2024) Harnessing the Power of Large Language Models for Natural Language to First-Order Logic Translation.  In Proceedings of the 62nd Annual Meeting of the Association for Computational Linguistics,  pp. 6942–6959.  External Links: [Document](https://dx.doi.org/10.18653/v1/2024.acl-long.375) Cited by: §2, §2, §3.1, §3.2, §3.5. 



Experimental support, please [view the build logs](./2509.22338v2/__stdout.txt) for errors. Generated by [ L A T E xml ](https://math.nist.gov/~BMiller/LaTeXML/). 

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

