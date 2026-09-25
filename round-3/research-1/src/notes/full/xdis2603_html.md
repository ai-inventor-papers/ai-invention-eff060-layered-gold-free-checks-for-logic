URL: https://arxiv.org/html/2603.25450 | FULL FETCH | 2026-09-24T03:00:18Z
warning: The `fitz` API is deprecated and will be removed in future. Use `import pymupdf` instead.
URL: https://arxiv.org/html/2603.25450
Type: HTML
Length: 81354 chars (truncated)

--- Content ---

##### Report GitHub Issue

×

Title:

Content selection saved. Describe the issue below:

Description:

Submit without GitHub Submit in GitHub

arXiv is now an independent nonprofit! [Learn more](https://info.arxiv.org/about) ×

[ Back to arXiv ](/)

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) Report Issue [ Back to Abstract ](/abs/2603.25450v2 "Back to abstract page") [ Download PDF](/pdf/2603.25450v2 "Download PDF") [ ](javascript:toggleNavTOC\(\); "Toggle navigation") [ ](javascript:toggleReadingMode\(\); "Disable reading mode, show header and footer")

  1. Abstract
  2. 1 Introduction
  3. 2 Related Work
  4. 3 Method
     1. 3.1 Cross-Model Perplexity
     2. 3.2 Cross-Model Entropy
  5. 4 Experiments
     1. 4.1 Results
        1. CMP targets the failure mode G-Ent misses.
        2. Task-dependent boundaries.
        3. Final-answer tokens vs. full chain-of-thought.
        4. Comparison to supervised routing.
     2. 4.2 Comparison to Baselines
  6. 5 Discussion
     1. 5.1 Routing performance and compute tradeoffs
     2. 5.2 When Does Capability Gap Matter?
     3. 5.3 Implications for Scalable Oversight
  7. 6 Conclusion
     1. Limitations.
     2. Future work.
  8. References
  9. A Full Results
  10. B Baseline Comparison
     1. B.1 Selective Prediction Analysis
        1. Single-pair examples.
        2. Aggregate trends.
  11. C Effect of Capability Gap
  12. D Experimental Setup Details
  13. E Relationship to Generation-Based Correctness Signals
  14. F Failure Mode: Very Weak Generators on Reasoning Tasks
  15. G GSM8K: Final-Answer Tokens and Verification Prompting
     1. Final-answer CMP.
     2. Verification prompting.



[ License: CC BY 4.0 ](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2603.25450v2 [cs.AI] 11 Jun 2026

# Cross-Model Disagreement as a Label-Free Correctness Signal

Matt Gorbett  Affiliation: Independent Researcher  Email: [matthewgorbett@gmail.com](mailto:) Suman Jana  Affiliation: Department of Computer Science  Affiliation: Columbia University  Affiliation: New York, NY 10027, USA  Email: [sj2536@columbia.edu](mailto:)

###### Abstract

Detecting when a language model is wrong without ground truth labels is a fundamental challenge for safe deployment. Existing approaches rely on a model’s own uncertainty, such as token entropy or confidence scores, but these signals fail critically on the most dangerous failure mode: confident errors, where a model is wrong but certain. In this work we introduce cross-model disagreement as a correctness indicator — a simple, training-free signal that can be dropped into existing production systems, routing pipelines, and deployment monitoring infrastructure without modification. Given a model’s generated answer, cross-model disagreement computes how surprised or uncertain a second verifier model is when reading that answer via a single forward pass. No generation from the verifying model is required, and no correctness labels are needed. We instantiate this principle as Cross-Model Perplexity (CMP), which measures the verifying model’s surprise at the generating model’s answer tokens, and Cross-Model Entropy (CME), which measures the verifying model’s uncertainty at those positions. Both CMP and CME outperform within-model uncertainty baselines across benchmarks spanning reasoning, retrieval, and mathematical problem solving (MMLU, TriviaQA, and GSM8K), and dominate other label-free signals operating in the single-prefill cost regime. On MMLU, CMP achieves a mean AUROC of 0.73 against a within-model entropy baseline of 0.59. These results establish cross-model disagreement as a practical, training-free approach to label-free correctness estimation, with direct applications in deployment monitoring, model routing, selective prediction, data filtering, and scalable oversight of production systems.  
  
---  
  
## 1 Introduction

Language models fail in two distinct ways. The first is ignorance: the model does not know the answer and signals this through uncertainty. Token entropy, maximum softmax probability (Hendrycks and Gimpel, 2017), and related signals are reasonable proxies for this failure mode, and the routing literature has built effective systems around them (Ding et al., 2024; Ong et al., 2025). The second failure mode is harder: the model is wrong but certain. It produces a fluent, high-confidence answer that happens to be incorrect. Within-model uncertainty signals are blind to this case by construction, since a confident model has low entropy regardless of whether its answer is right (Guo et al., 2017). Yet this is precisely the failure mode that matters most in practice. A medical assistant confidently stating the wrong drug interaction, a legal summarizer confidently misreading a statute, a student model confidently propagating a misconception: these are the errors that cause harm, and existing signals give no warning.

The confident error problem is not merely a calibration issue. Even well-calibrated models (Srinivas et al., 2024) cannot detect their own errors through introspection: a model that is wrong has, by definition, already committed to a wrong answer. Any signal derived solely from the generating model’s own distribution is fundamentally limited. It can tell you how confident the model is, but not whether that confidence is warranted. What is needed is an external perspective: a second model that can evaluate the generating model’s answer and flag disagreement.

Figure 1: Cross-model disagreement as a label-free correctness indicator. Given a prompt xx, the generator (Llama-3-8B) produces an answer y^\hat{y}. The verifier (Qwen2.5-7B) performs a single forward pass over (x,y^)(x,\hat{y}) with no generation required. The verifier assigns low probability to the token “1942”, the generator’s confident but incorrect answer. Cross-model perplexity (CMP) aggregates this surprise signal into a single correctness indicator, and high CMP flags a likely error.

This observation motivates cross-model disagreement as a practical signal. Rather than asking whether a model is uncertain about its own answer, we ask whether a second model is surprised by it. Concretely, given prompt xx and generating model answer y^\hat{y}, we perform a single forward pass through a verifying model on (x,y^)(x,\hat{y}) and extract two signals: CMP, which aggregates the verifying model’s token-level surprise, and CME, which aggregates its token-level uncertainty. No generation from the verifier is required and no correctness labels are needed. The two signals are complementary: CMP is most effective when the generator is confidently wrong and the verifier assigns low probability to the specific incorrect tokens; CME is more informative on retrieval tasks where distributional uncertainty better reflects whether an answer is grounded. Across our evaluation, CMP outperforms within-model entropy on MMLU across 12 of 15 model pairs by AUROC, and CME leads on TriviaQA where distributional uncertainty is more informative than token-level surprise. When used as a routing signal—directing queries to the verifier only when disagreement is high—CMP recovers a substantial fraction of the performance gap between generator and verifier with no labels required, as measured by APGR (Ong et al., 2025). CMP wins 14 of 15 routing comparisons against within-model entropy on GSM8K, and achieves mean APGR of 0.803 on MMLU versus 0.546 for G-Ent.

The closest prior work uses cross-model consistency as a hallucination signal. SelfCheckGPT (Manakul et al., 2023) checks consistency across stochastic samples from the same model; CrossCheckGPT (Sun et al., 2024) compares outputs generated by multiple independent models. Both require multiple generations. Our setting is fundamentally different: we use a single greedy answer and a single forward pass through the verifier, with no generation from either model after the initial answer, and we target per-instance correctness prediction rather than hallucination ranking. More broadly, the uncertainty quantification literature has focused entirely on signals derived from the generating model itself (Kadavath et al., 2022; Kuhn et al., 2023; Liu et al., 2020), and prior work explicitly notes that within-model perplexity fails (Srinivas et al., 2024). To our knowledge, no prior work uses a verifying model’s logit-based signals on a generating model’s answer.

CMP and CME have direct applications in several settings. In deployment monitoring, CMP and CME can be evaluated on every query without ground truth labels, serving as a cheap triage signal that flags likely errors for more expensive downstream verification—whether human review, re-querying, or generation-based methods such as LLM-as-judge (Zheng et al., 2023). In model routing, high disagreement triggers escalation to a stronger model, recovering a large fraction of the performance gap at a fraction of the cost of always using the strong model. Unlike supervised routers such as RouteLLM (Ong et al., 2025), CMP and CME require no preference labels and no router training, occupying a different point on the supervision-cost tradeoff. In data filtering, high CMP on a candidate example identifies instances where models disagree—a label-free signal for hard or ambiguous examples useful for training data curation and hard negative mining. Finally, in selective prediction (Geifman and El-Yaniv, 2017), high CMP serves as an abstention signal, allowing a system to withhold predictions on inputs where confident errors are most likely — improving accuracy on the subset it does answer without any labeled data or threshold calibration.

We further characterize when cross-model signals are most effective: on MMLU, CMP AUROC is uncorrelated with capability gap (ρ=0.11\rho=0.11, p=0.72p=0.72), suggesting architectural diversity drives correctness detection rather than capability asymmetry; on TriviaQA, CME is more robust across gap sizes; on GSM8K both signals improve modestly but without a significant trend. We discuss implications for scalable oversight and deployment monitoring in Section 5.

Our contributions are as follows:

  * •

We introduce cross-model disagreement as a label-free, training-free correctness indicator, instantiated as CMP and CME, each requiring only a single forward pass through a verifying model with no generation or no correctness labels.

  * •

We show that CMP and CME outperform within-model uncertainty baselines across MMLU, TriviaQA, and GSM8K, and provide the strongest label-free correctness signal available in the single-prefill compute regime. Methods that achieve higher AUROC (verifier answer agreement, semantic entropy) require autoregressive generation, costing one to two orders of magnitude more per query.

  * •

We show that on knowledge-intensive tasks, architectural diversity between same-sized models is sufficient for effective correctness detection, and capability asymmetry is not required, while on open-ended retrieval a stronger verifier provides meaningful additional benefit.




## 2 Related Work

Our work sits at the intersection of LLM uncertainty estimation, cross-model disagreement, trained verifiers, model routing, scalable oversight, and speculative decoding.

Uncertainty Estimation. A standard approach to predicting correctness uses the model’s own confidence. Maximum softmax probability (Hendrycks and Gimpel, 2017), predictive entropy, and network features (Gorbett and Blanchard, 2022) are common baselines, but modern networks are poorly calibrated (Guo et al., 2017) and frequently assign high confidence to incorrect predictions; Srinivas et al. (2024) show explicitly that within-model perplexity has limited predictive power in open-ended settings. A complementary line elicits confidence directly, either by prompting for a yes/no token (Kadavath et al., 2022) or a verbalized score (Tian et al., 2023). Sampling-based methods—self-consistency, semantic entropy (Kuhn et al., 2023; Farquhar et al., 2024), and ensemble disagreement (Lakshminarayanan et al., 2017; Manakul et al., 2023; Sun et al., 2024)—require multiple generation passes. See Shorinwa et al. (2024) for a broader taxonomy. CMP and CME require a single verifier forward pass and remain informative precisely where within-model entropy is flat.

Cross-Model Disagreement and Multi-LLM Uncertainty. A growing line of work uses signals from a second model to improve uncertainty estimation beyond what self-consistency provides. Hamidieh et al. (2026) show that cross-model semantic disagreement among a scale-matched ensemble captures epistemic uncertainty that self-consistency misses. Xue et al. (2025) observe that self-consistency saturates near a black-box oracle and propose a two-stage scheme that invokes a verifier on uncertain cases. Feng et al. (2025) estimate uncertainty across multi-agent reformulations of the same query; Dey et al. (2025) fuse predictions from multiple LLMs weighted by self-assessment; and Chen et al. (2026) switch between LLMs based on cross-model sample agreement. All require generation from one or more additional models—to produce response samples, drive multi-agent interaction, or obtain explicit verifier outputs—and measure agreement between generated answers rather than logit-level signals on a fixed answer. CMP and CME require a single verifier forward pass with no generation, no sampling, and no agent-style interaction, producing a scalar signal directly from the verifier’s distribution over the generator’s greedy answer.

Trained Verifiers and Judges. A separate body of work trains a verifier or judge to score candidate solutions. Outcome and process reward models (Lightman et al., 2024) assign correctness scores to full solutions or intermediate steps. Most closely related to our setup, generative verifiers (Zhang et al., 2024) reframe verification as next-token prediction: a verifier trained to assign probability mass to a “Yes” or “No” token after the candidate solution. LLM-as-Judge methods (Zheng et al., 2023; Dubois et al., 2024; Kim et al., 2024) extend this by having a stronger model generate a scalar rating or structured critique. CMP differs in two ways: it requires no verifier training, and the signal is the verifier’s existing log-probability over the generator’s actual answer tokens rather than an explicit yes/no judgment or generated critique. Our P(True) ablation (Appendix F) confirms that explicit correctness prompting is far less informative than implicit token-level perplexity for off-the-shelf verifiers.

LLM Routing. Routing systems reduce inference cost by directing queries to a stronger model only when needed. HybridLLM (Ding et al., 2024), RouteLLM (Ong et al., 2025), and FrugalGPT (Chen et al., 2023b) train routers on labeled preference data; AutoMix (Aggarwal et al., 2024) uses a smaller model to self-verify before escalating but still requires a calibration step. CMP and CME are parameter-free and require no router training, though they require a single forward pass through a second model at inference time. We adopt the APGR metric from Ong et al. (2025) to measure routing quality.

Scalable Oversight. Scalable oversight (Bowman et al., 2022) and weak-to-strong generalization (Burns et al., 2024) study how to supervise AI systems whose capabilities may exceed those of the overseer, generally assuming that effective verification requires a more capable model. We examine whether capability gap is necessary or whether architectural diversity alone suffices, evaluating pairs with similar task accuracy alongside asymmetric ones.

Speculative Decoding. Speculative decoding (Leviathan et al., 2023; Chen et al., 2023a) accelerates inference by using a small draft model to propose tokens, which a larger target model verifies via acceptance sampling. CMP is the sequence-level analogue: rather than per-token accept/reject decisions, we aggregate verifier log-probabilities across the full answer into a single routing score. This connection grounds why CMP is most effective on tasks where errors manifest as low token-level acceptance probability.

## 3 Method

In this section we describe cross-model disagreement. Given a generating model ℳg\mathcal{M}_{g} and a verifying model ℳv\mathcal{M}_{v}, we define two label-free signals for predicting whether ℳg\mathcal{M}_{g}’s answer is correct.

Problem Setup. Let xx denote an input prompt. The generating model produces an answer y^g∼ℳg(⋅∣x)\hat{y}_{g}\sim\mathcal{M}_{g}(\cdot\mid x) autoregressively by greedy decoding. Our goal is to predict whether y^g\hat{y}_{g} is correct without access to ground truth labels. We make no assumptions about the relative capability of ℳg\mathcal{M}_{g} and ℳv\mathcal{M}_{v}.

### 3.1 Cross-Model Perplexity

Given y^g\hat{y}_{g}, we concatenate the prompt and answer to form (x,y^g)(x,\hat{y}_{g}) and perform a single forward pass through ℳv\mathcal{M}_{v}. At each answer token position t∈{1,…,T}t\in\\{1,\ldots,T\\}, the forward pass yields logits over the full vocabulary. We define CMP as:

| CMP(x,y^g)=exp(−1T∑t=1Tlogpv(y^g(t)∣x,y^g(<t)))\text{CMP}(x,\hat{y}_{g})=\exp\left(-\frac{1}{T}\sum_{t=1}^{T}\log p_{v}\\!\left(\hat{y}_{g}^{(t)}\mid x,\hat{y}_{g}^{(<t)}\right)\right) |  | (1)  
---|---|---|---  
  
where pvp_{v} denotes the verifying model’s conditional distribution and TT is the number of answer tokens. High CMP indicates that ℳv\mathcal{M}_{v} assigns low probability to ℳg\mathcal{M}_{g}’s answer—the models disagree. CMP connects formally to speculative decoding (Leviathan et al., 2023; Chen et al., 2023a), where the acceptance probability for a draft token xtx_{t} is min⁡(1,pv​(xt)/pg​(xt))\min(1,p_{v}(x_{t})/p_{g}(x_{t})). CMP aggregates this token-level acceptance signal across the full answer sequence, making a single binary decision rather than a token-level correction.

### 3.2 Cross-Model Entropy

From the same single forward pass, we also compute CME as the mean entropy of the verifying model’s output distribution over answer token positions:

| CME(x,y^g)=−1T∑t=1T∑vpv(v∣x,y^g(<t))logpv(v∣x,y^g(<t))\text{CME}(x,\hat{y}_{g})=-\frac{1}{T}\sum_{t=1}^{T}\sum_{v}p_{v}(v\mid x,\hat{y}_{g}^{(<t)})\log p_{v}(v\mid x,\hat{y}_{g}^{(<t)}) |  | (2)  
---|---|---|---  
  
Where CMP measures the verifying model’s surprise at the specific tokens produced, CME measures its general uncertainty at those positions. The two signals are complementary: CMP is most informative when the generator is confidently wrong and the verifier assigns low probability to the specific incorrect tokens; CME is most informative on retrieval tasks where the verifier’s distributional uncertainty better reflects whether the answer is grounded. Both signals are obtained at no additional computational cost beyond the single forward pass required for CMP.

Figure 2: CMP and CME performance across datasets compared to baselines. (A) Mean AUROC over all model pairs. G-Ent and G-PPL measure the generator’s own entropy and perplexity; CME and CMP measure the corresponding signals from a verifier model on the generator’s answer. APGR measures the fraction of the performance gap between weak and strong model that is recovered by routing, normalized so that random routing scores 0 and oracle routing scores 1; pairs with small gaps are excluded because the small denominator in the PGR formula produces unstable estimates. Error bars show standard error across pairs; nn indicates the number of pairs per dataset. 

## 4 Experiments

We evaluate CMP and CME across four benchmarks datasets. Table 1 summarizes selected results; full results appear in Appendix A.

Datasets. We evaluate on MMLU (Hendrycks et al., 2021) (multiple-choice), TriviaQA (Joshi et al., 2017) (with and without context), and GSM8K (Cobbe et al., 2021) (chain-of-thought reasoning), covering knowledge retrieval, reading comprehension, and multi-step arithmetic.

Models. We evaluate seven instruction-tuned models spanning five families: Qwen2.5 (0.5B, 7B), Llama-3 (1B, 8B), Gemma-3 (270M), Mistral (7B), and OLMo-3 (7B). We construct ordered model pairs across four datasets, covering both asymmetric pairs (small generator verified by large model, e.g. Qwen-0.5B →\to Qwen-7B) and same-sized cross-family pairs among the four 7–8B models (Qwen-7B, Llama-3-8B, Mistral-7B, OLMo-7B), which isolate architectural diversity from capability asymmetry. Full model details and per-pair results are in Appendix D.

Within-model baselines and metrics. We compare CMP and CME against two within-model baselines: generator entropy (G-Ent), the mean token-level entropy H=−∑vpvlogpvH=-\sum_{v}p_{v}\log p_{v} over the generator’s answer tokens, and generator perplexity (G-PPL), the mean token-level perplexity of the generator on its own answer. Both are standard unsupervised signals requiring no verifier. Together these serve as direct ablations of CME and CMP respectively: if the cross-model signals merely recover information already present in the generator’s own distribution, G-Ent and G-PPL should perform comparably. We additionally test explicit verification prompting (P(True); Kadavath et al., 2022) on GSM8K, where the verifier is asked directly whether the generator’s answer is correct (Appendix G). We also compare against RouteLLM (Ong et al., 2025), the strongest supervised routing baseline, which trains a router on human preference labels augmented with LLM-judge data; unlike our signals, it requires labeled data and a trained router model, and we treat it as an upper bound on what supervision buys in this setting.

For correctness prediction we report AUROC against weak model incorrectness, which is threshold-free, requires no routing setup, and is our primary metric for evaluating signal quality across all pairs. For routing quality we report APGR (Average Performance Gap Recovered) (Ong et al., 2025). At each routing threshold, a fraction cc of queries are sent to the strong model while the rest use the weak model’s answer, yielding accuracy a⁡(c)a(c). The performance gap recovered at cost cc is:

| PGR​(c)=a⁡(c)−awas−aw,\text{PGR}(c)=\frac{a(c)-a_{w}}{a_{s}-a_{w}}, |  | (3)  
---|---|---|---  
  
where awa_{w} and asa_{s} are the weak and strong model accuracies. APGR averages PGR over c∈(0,1)c\in(0,1): a value of 0 corresponds to random routing and 1 to oracle routing. Small accuracy gaps produce unstable APGR estimates due to the small denominator in PGR​(c)\text{PGR}(c); we therefore exclude such pairs from Figure 2.

Table 1: Selected results across all four benchmarks. Bold = best per row separately for AUROC and APGR among G-Ent, G-PPL, CMP, CME. Same-size cross-family pairs marked †\dagger. See Appendix for full results. |  |  |  |  | Acc. | AUROC ↑\uparrow | APGR ↑\uparrow  
---|---|---|---|---|---|---|---  
Dataset | Generator | Verifier | Accg | Accv | Gap | G-Ent | G-PPL | CMP | CME | G-Ent | G-PPL | CMP | CME  
MMLU | Qwen-0.5B | Qwen-7B | 0.42 | 0.72 | 0.30 | 0.588 | 0.556 | 0.841 | 0.583 | 0.521 | 0.501 | 0.793 | 0.497  
Llama-1B | Llama-3-8B | 0.43 | 0.62 | 0.19 | 0.654 | 0.655 | 0.817 | 0.679 | 0.562 | 0.605 | 0.869 | 0.540  
Llama-1B | Qwen-7B | 0.43 | 0.72 | 0.29 | 0.654 | 0.655 | 0.786 | 0.634 | 0.569 | 0.595 | 0.807 | 0.558  
OLMo-7B† | Qwen-7B | 0.56 | 0.72 | 0.15 | 0.503 | 0.599 | 0.896 | 0.697 | 0.486 | 0.546 | 0.914 | 0.447  
TriviaQA | Llama-3-8B | Mistral-7B | 0.43 | 0.64 | 0.20 | 0.859 | 0.885 | 0.825 | 0.922 | 0.822 | 0.831 | 0.849 | 0.789  
Qwen-0.5B | Qwen-7B | 0.41 | 0.65 | 0.24 | 0.778 | 0.730 | 0.816 | 0.825 | 0.621 | 0.604 | 0.738 | 0.610  
Llama-1B | Qwen-7B | 0.55 | 0.65 | 0.10 | 0.804 | 0.810 | 0.688 | 0.789 | 0.691 | 0.720 | 0.761 | 0.574  
Llama-3-8B† | Qwen-7B | 0.43 | 0.65 | 0.21 | 0.859 | 0.885 | 0.772 | 0.875 | 0.796 | 0.808 | 0.807 | 0.757  
TriviaQA (no ctx) | Llama-1B | Llama-3-8B | 0.42 | 0.67 | 0.25 | 0.840 | 0.851 | 0.938 | 0.814 | 0.685 | 0.693 | 0.811 | 0.589  
Qwen-0.5B | Qwen-7B | 0.21 | 0.59 | 0.38 | 0.782 | 0.775 | 0.793 | 0.817 | 0.530 | 0.532 | 0.644 | 0.510  
Llama-1B | Qwen-7B | 0.42 | 0.59 | 0.17 | 0.840 | 0.851 | 0.738 | 0.806 | 0.653 | 0.671 | 0.759 | 0.501  
Qwen-7B† | Llama-3-8B | 0.59 | 0.67 | 0.08 | 0.823 | 0.793 | 0.748 | 0.625 | 0.980 | 0.946 | 0.964 | 0.533  
GSM8K | Mistral-7B† | Llama-3-8B | 0.54 | 0.61 | 0.07 | 0.658 | 0.542 | 0.704 | 0.675 | 0.955 | 0.663 | 1.155 | 0.977  
Llama-1B | Qwen-7B | 0.37 | 0.90 | 0.53 | 0.559 | 0.531 | 0.652 | 0.659 | 0.515 | 0.506 | 0.563 | 0.556  
Llama-1B | Llama-3-8B | 0.37 | 0.61 | 0.25 | 0.559 | 0.531 | 0.653 | 0.614 | 0.536 | 0.517 | 0.633 | 0.589  
Qwen-0.5B | Qwen-7B | 0.24 | 0.90 | 0.66 | 0.640 | 0.630 | 0.664 | 0.698 | 0.527 | 0.528 | 0.537 | 0.543  
  
### 4.1 Results

We evaluate CMP and CME against within-model baselines across four benchmarks and model pairs spanning asymmetric and same-sized cross-family configurations. Table 1 and Figure 2 summarize the main results: CMP leads on MMLU and GSM8K while CME is more competitive on TriviaQA, and both cross-model signals consistently outperform their within-model counterparts on tasks where the generator makes confident errors. The paragraphs below analyze the per-case signal structure, quintile separation, and conditions under which cross-model signals succeed or fail.

Figure 3: Top row: per-case signal means. Mean CMP (left axis, blue) and G-Ent (right axis, red) by outcome category. The shaded column highlights the “generator wrong only” case—confident errors the verifier does not share. On MMLU, CMP spikes 9×9\times above the mean of the other three cases while G-Ent is flat (1.0×1.0\times); on TriviaQA the spike is 18×18\times vs. 1.6×1.6\times; on GSM8K both signals rise modestly (3×3\times and 1.4×1.4\times), reflecting the difficulty of isolating chain-of-thought errors with token-level signals. Bottom row: accuracy by signal quintile. Samples sorted by signal strength (Q1 = lowest, Q5 = highest); bars show weak model accuracy within each bin. On MMLU, CMP produces a 74pp spread versus 23pp for G-Ent and 18pp for G-PPL. On TriviaQA (no context), all three signals are competitive (93pp, 80pp, 81pp). On GSM8K, CMP achieves a 50pp spread while G-PPL nearly collapses to 8pp, confirming that generator self-perplexity is uninformative on chain-of-thought tasks and that cross-model disagreement is doing genuine work.

#### CMP targets the failure mode G-Ent misses.

Figure 3 isolates the four outcome categories. On MMLU (OLMo-7B →\to Llama-8B), CMP in the “generator wrong only” case is 154×154\times the both-correct baseline—a 9×\times spike over the remaining cases—while G-Ent is flat across all four (≤1.0×\leq 1.0\times variation). On TriviaQA (Llama-8B →\to Qwen-7B) the pattern sharpens: CMP reaches 46​k46\mathrm{k} versus 9797 when both models are correct (18×\times selectivity), while G-Ent rises by only 1.6×\times. G-Ent is elevated whenever the generator is uncertain regardless of whether the verifier concurs; CMP selectively spikes only when the generator’s error is not shared by the verifier.

Figure 2A reports mean AUROC across all model pairs. On MMLU, CMP wins 12 of 15 pairs by AUROC, with a mean of 0.727 versus 0.595 for G-Ent and 0.607 for G-PPL. On GSM8K, CMP (0.623) and CME (0.621) both outperform G-Ent (0.584) and G-PPL (0.533), with G-PPL performing worst of all four signals—consistent with the near-flat quintile spread in Figure 3. On TriviaQA (context), CME leads (0.743) with G-Ent close behind (0.732), while CMP underperforms on several pairs where the verifier shares similar knowledge gaps to the generator. On TriviaQA (no context) the AUROC signals cluster (G-Ent 0.779, CMP 0.750, CME 0.738, G-PPL 0.687): G-Ent is the strongest AUROC signal on this dataset, while CMP leads on routing-relevant APGR, consistent with retrieval errors being detectable by within-model signals when context is absent.

#### Task-dependent boundaries.

On GSM8K, CMP achieves mean APGR of 0.628 versus 0.583 for G-Ent, winning 14 of 15 routing comparisons against G-Ent, but the per-case spike is weaker than on MMLU or TriviaQA, and CME is preferable on several pairs (Table 1). The Mistral-7B →\to Qwen-7B pair on TriviaQA is a more extreme case: with only a 1pp accuracy gap, CMP and G-PPL collapse near chance (AUROC 0.42 and 0.30) while G-Ent remains strong (0.847). Both cases point to the same boundary condition: when the verifier shares the generator’s failure mode—either through similar knowledge gaps or nearly identical accuracy—cross-model disagreement loses its signal, and within-model entropy is the more reliable fallback.

#### Final-answer tokens vs. full chain-of-thought.

On GSM8K, we test whether CMP’s signal comes from the full chain-of-thought or only the final numerical answer. CMP restricted to answer tokens only (CMP-Final) achieves mean APGR of 0.665 versus 0.682 for the full trace (CMP-Full), indicating that the final answer carries most of the signal with a small additional benefit from the reasoning steps. This suggests CMP could be applied more efficiently by scoring only the answer tokens, avoiding the cost of processing the full chain-of-thought through the verifier.

#### Comparison to supervised routing.

RouteLLM (Ong et al., 2025) provides the nearest supervised baseline: a causal LLM classifier trained on tens of thousands of human preference labels from Chatbot Arena, augmented with LLM-judge synthetic labels, routing between GPT-4 and Mixtral-8x7B. Their best augmented router achieves APGR of 0.622 on GSM8K and 0.603 on MMLU. On the 8-pair GSM8K subset used for our chain-of-thought ablation (Appendix G), CMP-Full achieves APGR of 0.682; over the full set of pairs with measurable capability gap (gap>0.05\text{gap}>0.05), CMP achieves mean APGR of 0.628 on GSM8K and 0.803 on MMLU with zero labeled data and no router training. These evaluations are not directly comparable: RouteLLM routes between a proprietary strong model and an open-weight weak model across a different task and label distribution, while we route between open-weight pairs on standard benchmarks. We include the comparison not as a controlled benchmark but to situate CMP on the broader supervision-cost tradeoff: a single verifier prefill with no labeled data is competitive with a trained supervised router on reasoning tasks, and the gap is substantial on knowledge-intensive multiple-choice. Where labeled routing data can be collected, supervised routers remain the appropriate choice.

Table 2: Mean AUROC across model pairs with capability gap >> 5pp, comparing CMP and CME against label-free baselines. Methods are grouped by computational cost tier; cost is per-sample overhead relative to a single verifier prefill, excluding shared generator inference. TT = answer tokens; k=10k{=}10 for Semantic Entropy. Bold = best per column within tier; underline = best overall per column. Full per-pair results in Appendix 7. | Mean AUROC ↑\uparrow |  |   
---|---|---|---  
Method | MMLU | TriviaQA | TriviaQA | GSM8K | Verifier work | Cost  
|  | (ctx) | (no ctx) |  |  | vs. CMP  
_Single verifier prefill_  
P(True) | 0.518 | 0.510 | 0.526 | 0.603 | 1 prefill | ∼\sim1×\times  
CME (ours) | 0.628 | 0.759 | 0.737 | 0.621 | 1 prefill | 1×\times  
CMP (ours) | 0.749 | 0.679 | 0.761 | 0.623 | 1 prefill | 1×\times  
_Autoregressive generation required_  
V-Agree | 0.756 | 0.782 | 0.789 | 0.898 | 1 gen (TT tok) | 1–T×T\times  
Sem-Ent (k=10k{=}10) | 0.611 | 0.747 | 0.804 | 0.728 | kk gens + NLI | kk–kT×kT\times  
  
### 4.2 Comparison to Baselines

To situate CMP and CME against a broader range of label-free correctness signals, we evaluate three baselines that vary the source and form of disagreement. Each baseline targets a distinct point on the supervision-cost spectrum and isolates a different aspect of what the verifier contributes.

Verifier Answer Agreement (V-Agree) uses string-level disagreement between greedy answers from MgM_{g} and MvM_{v}, ablating verifier logits while preserving cross-model structure. P(True) (Kadavath et al., 2022) prompts the verifier with the generator’s answer and extracts the probability on the “Yes” token, replacing CMP’s implicit token-level perplexity with an explicit verification judgment in the same single-prefill regime. Semantic Entropy (Kuhn et al., 2023) removes the verifier entirely, drawing kk generator samples at T>0T>0, clustering them via an NLI model, and computing entropy over clusters; it is the strongest within-model consistency baseline in the uncertainty quantification literature. The three baselines span a range of compute regimes from a single verifier prefill (P(True)) to kk full generations plus an auxiliary NLI model (Semantic Entropy); Table 2 summarizes per-sample cost alongside results.

Results Among single-prefill signals, CMP or CME achieves the highest AUROC on every benchmark, with the choice between them tracking task structure: CMP wins on tasks where errors are token-localized (MMLU multiple-choice, TriviaQA without context), CME wins on retrieval. P(True), despite operating in the same compute regime, performs near chance — consistent with known limitations of explicit self-evaluation prompting for off-the-shelf verifiers. Generation-based baselines (V-Agree, Sem-Ent) achieve higher AUROC on TriviaQA (no context) and GSM8K, but at substantially higher cost: V-Agree requires autoregressive decode steps from the verifier, and Sem-Ent requires kk full generations from the generator plus an auxiliary NLI model. CMP and CME occupy the cheapest point on the cost-quality curve.

## 5 Discussion

### 5.1 Routing performance and compute tradeoffs

Figure 2B reports mean APGR across pairs with accuracy gap >> 5pp. CMP leads on MMLU and GSM8K; on TriviaQA, G-Ent and CME are competitive, consistent with the AUROC results.

The practical regime where CMP is most attractive is one where generation cost dominates and no labeled routing data is available. Routing with CMP or CME requires a single verifier prefill on every query, with no autoregressive generation from the verifier and no router model. On MMLU this prefill is negligible; on GSM8K, where chain-of-thought traces reach up to 256 tokens, it is more substantial but still well below the cost of strong-model generation. Critically, the prefill is incurred only to make a routing decision: queries correctly identified as easy are served by the weak model with no further large-model compute. If the verifier is generated rather than prefilled, verifier compute would be incurred on every query regardless of the routing outcome, largely eliminating the cost benefit. Prefill-only is therefore what makes label-free routing economically viable on long-form tasks, not a concession.

Existing approaches occupy different points on this tradeoff. Label-based routers such as RouteLLM (Ong et al., 2025) and HybridLLM (Ding et al., 2024) add negligible inference overhead but require labeled preference data and a trained router model. FrugalGPT (Chen et al., 2023b) and AutoMix (Aggarwal et al., 2024) avoid large-model compute on easy queries entirely but require calibration steps or supervised signals. CMP and CME occupy the opposite corner: zero labeled data, zero router training, one verifier prefill per query. The tradeoff is explicit: where labeled routing data can be collected, supervised routers remain the appropriate choice; CMP and CME are most valuable precisely when such data is unavailable.

### 5.2 When Does Capability Gap Matter?

Figure 4 plots CMP AUROC against accuracy gap for all pairs across three benchmarks. The task-dependent pattern is stark. On MMLU, CMP is essentially uncorrelated with capability gap (ρ=+0.12\rho=+0.12, p=0.71p=0.71): pairs with a 6-point accuracy gap perform as well as pairs with a 47-point gap, and the highest-scoring points are same-size cross-family pairs (blue), not the largest-gap pairs. The operative mechanism on knowledge-intensive multiple-choice tasks appears to be diversity of training rather than capability asymmetry—models from different families make different confident errors, and CMP captures this disagreement regardless of relative accuracy.

On TriviaQA the picture is different. CMP shows a significant positive correlation with capability gap (ρ=+0.63\rho=+0.63, p=0.03p=0.03), with large-gap pairs substantially outperforming small-gap pairs (AUROC 0.78 vs. 0.59). Open-ended knowledge retrieval requires the verifier to have genuine knowledge the generator lacks; a same-sized peer from a different family may share the same knowledge gaps, reducing the informativeness of its surprise. The two same-size cross-family pairs on TriviaQA (blue) sit at the lower end of the performance range, consistent with this interpretation. CME is more robust to this effect, remaining competitive across gap sizes.

On GSM8K there is no significant trend (ρ=−0.22\rho=-0.22, p=0.43p=0.43), with high variance across pairs at similar gap sizes. Signal quality on chain-of-thought tasks appears driven more by model family and architectural diversity than by capability gap, though the modest overall AUROC levels make these patterns harder to interpret cleanly.

Figure 4: CMP AUROC versus capability gap across three benchmarks. On MMLU, AUROC is uncorrelated with gap (ρ=+0.12\rho=+0.12, p=0.71p=0.71) and same-size cross-family pairs (blue) achieve the highest scores, suggesting model diversity drives the signal rather than capability asymmetry. On TriviaQA, gap correlates positively with AUROC (ρ=+0.63\rho=+0.63, p=0.03p=0.03), indicating a stronger verifier helps when errors are knowledge-driven. GSM8K shows no significant trend (ρ=−0.22\rho=-0.22, p=0.43p=0.43).

### 5.3 Implications for Scalable Oversight

The scalable oversight literature (Bowman et al., 2022; Burns et al., 2024) has largely assumed that verifying a model’s outputs requires a more capable supervisor. Our results qualify this assumption in a task-dependent way. On MMLU, peer verification between same-sized models of different families is as effective as verification by a substantially stronger model, suggesting that for knowledge-intensive tasks the capability hierarchy is not a prerequisite for correctness detection — architectural diversity is sufficient. On open-ended retrieval tasks, a stronger verifier does provide meaningful benefit, consistent with the intuition that the verifier needs knowledge the generator lacks.

The practical implication is straightforward: the right verification strategy depends on the likely failure mode of the deployed model. For knowledge-intensive tasks with constrained output formats, a diverse peer model is a sufficient and efficient verifier. For open-ended retrieval, a stronger verifier improves detection quality. This task-dependent characterization is a concrete and actionable finding for deployment monitoring without labeled data.

## 6 Conclusion

We have shown that cross-model disagreement—measured as CMP or CME via a single forward pass through a verifying model—is a reliable label-free correctness signal for language model outputs. The signal works between same-sized models of different families and requires no labeled data or router training.

#### Limitations.

CMP and CME require the verifier’s distribution to be a better proxy for correctness than the generator’s. All evaluated pairs have non-negative capability gap; the reverse case (weaker verifier) is not directly tested, though our boundary analysis on Mistral→\toQwen TriviaQA (1pp gap, CMP AUROC 0.42) suggests signal degrades as the gap shrinks or reverses. Token-level scoring is also sensitive to paraphrase: when the verifier knows a wording the generator did not produce, CMP can penalize the phrasing rather than the answer, and CME is more robust to this.

#### Future work.

Several directions remain open. Extending cross-model disagreement beyond greedy decoding to sampled or long-form chain-of-thought outputs — and to code generation and multi-step reasoning at scale — would test the framework’s limits. A theoretical account of which signal (CMP vs. CME) works for which failure mode would deepen the empirical characterization we provide. The diversity mechanism we identify raises a concrete design question: given a fixed verifier budget, how should one select a verifying model to maximize correctness signal? Representational similarity metrics may offer a principled answer. Finally, our scalable oversight results are inference-time on static benchmarks; whether peer verification supports iterative oversight loops as both models scale is the central open question connecting this work to the broader alignment agenda.

## References

  * Aggarwal et al. (2024) P. Aggarwal, A. Madaan, Y. Yang, and Mausam AutoMix: automatically mixing language models.  In Findings of the Association for Computational Linguistics: EMNLP 2024,  Cited by: §2, §5.1. 
  * Bowman et al. (2022) S. R. Bowman, J. Hyun, E. Perez, E. Chen, C. Pettit, S. Heiner, K. Lukošiūtē, A. Askell, A. Jones, A. Chen, et al. Measuring progress on scalable oversight for large language models.  arXiv preprint arXiv:2211.03540.  Cited by: §2, §5.3. 
  * Burns et al. (2024) C. Burns, P. Izmailov, J. H. Kirchner, B. Baker, L. Gao, L. Aschenbrenner, Y. Chen, A. Ecoffet, M. Joglekar, J. Leike, I. Sutskever, and J. Wu Weak-to-strong generalization: eliciting strong capabilities with weak supervision.  In International Conference on Machine Learning,  Cited by: §2, §5.3. 
  * Chen et al. (2023a) C. Chen, S. Borgeaud, G. Irving, J. Lespiau, L. Sifre, and J. Jumper Accelerating large language model decoding with speculative sampling.  arXiv preprint arXiv:2302.01318.  Cited by: §2, §3.1. 
  * Chen et al. (2026) J. Chen, Z. Xun, B. Zhou, H. Qi, H. Zhang, Q. Zhang, Y. Chen, W. Hu, Y. Qu, W. Ouyang, and S. Hu Do we truly need so many samples? multi-LLM repeated sampling efficiently scales test-time compute.  In Proceedings of the AAAI Conference on Artificial Intelligence,  Vol. 40, pp. 20083–20091.  Cited by: §2. 
  * Chen et al. (2023b) L. Chen, M. Zaharia, and J. Zou FrugalGPT: how to use large language models while reducing cost and improving performance.  External Links: 2305.05176, [Link](https://arxiv.org/abs/2305.05176) Cited by: §2, §5.1. 
  * Cobbe et al. (2021) K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano, et al. Training verifiers to solve math word problems.  In arXiv preprint arXiv:2110.14168,  Cited by: Appendix D, §4. 
  * Dey et al. (2025) P. Dey, S. Merugu, and S. Kaveri Uncertainty-aware fusion: an ensemble framework for mitigating hallucinations in large language models.  In Companion Proceedings of the ACM Web Conference (WWW Companion),  Cited by: §2. 
  * Ding et al. (2024) D. Ding, A. Mallick, C. Wang, R. Sim, S. Mukherjee, V. Ruhle, L. V. Lakshmanan, and A. H. Awadallah Hybrid LLM: cost-efficient and quality-aware query routing.  In International Conference on Learning Representations,  Cited by: §1, §2, §5.1. 
  * Dubois et al. (2024) Y. Dubois, C. X. Li, R. Taori, T. Zhang, I. Gulrajani, J. Ba, C. Guestrin, P. S. Liang, and T. B. Hashimoto AlpacaFarm: a simulation framework for methods that learn from human feedback.  In Advances in Neural Information Processing Systems,  Vol. 36.  Cited by: Appendix E, §2. 
  * Farquhar et al. (2024) S. Farquhar, J. Kossen, L. Kuhn, and Y. Gal Detecting hallucinations in large language models using semantic entropy.  Nature 630 (8017), pp. 625–630.  Cited by: §2. 
  * Feng et al. (2025) Y. Feng, P. M. Htut, Z. Qi, W. Xiao, M. Mager, N. Pappas, K. Halder, Y. Li, Y. Benajiba, and D. Roth Rethinking LLM uncertainty: a multi-agent approach to estimating black-box model uncertainty.  In Findings of the Association for Computational Linguistics: EMNLP,  Cited by: §2. 
  * Geifman and El-Yaniv (2017) Y. Geifman and R. El-Yaniv Selective classification for deep neural networks.  In Advances in Neural Information Processing Systems,  Vol. 30.  Cited by: §B.1, §1. 
  * Gorbett and Blanchard (2022) M. Gorbett and N. Blanchard Utilizing network features to detect erroneous inputs.  In Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision,  pp. 34–43.  Cited by: §2. 
  * Guo et al. (2017) C. Guo, G. Pleiss, Y. Sun, and K. Q. Weinberger On calibration of modern neural networks.  In International Conference on Machine Learning,  pp. 1321–1330.  Cited by: §1, §2. 
  * Hamidieh et al. (2026) K. Hamidieh, V. Thost, W. Gerych, M. Yurochkin, and M. Ghassemi Complementing self-consistency with cross-model disagreement for uncertainty quantification.  In International Conference on Learning Representations (ICLR),  Cited by: §2. 
  * Hendrycks et al. (2021) D. Hendrycks, C. Burns, S. Basart, A. Zou, M. Mazeika, D. Song, and J. Steinhardt Measuring massive multitask language understanding.  In International Conference on Learning Representations,  Cited by: Appendix D, §4. 
  * Hendrycks and Gimpel (2017) D. Hendrycks and K. Gimpel A baseline for detecting misclassified and out-of-distribution examples in neural networks.  In International Conference on Learning Representations,  Cited by: §1, §2. 
  * Joshi et al. (2017) M. Joshi, E. Choi, D. S. Weld, and L. Zettlemoyer TriviaQA: a reading comprehension dataset containing trivia questions.  arXiv preprint arXiv:1705.03551.  Cited by: Appendix D, §4. 
  * Kadavath et al. (2022) S. Kadavath, T. Conerly, A. Askell, T. Henighan, D. Drain, E. Perez, N. Schiefer, Z. Hatfield-Dodds, N. DasSarma, E. Tran-Johnson, et al. Language models (mostly) know what they know.  In arXiv preprint arXiv:2207.05221,  Cited by: Appendix E, Appendix G, §1, §2, §4.2, §4. 
  * Kim et al. (2024) S. Kim, J. Shin, Y. Cho, J. Han, S. Longpre, H. Moon, S. Yun, S. Shin, S. Kim, J. Thorne, et al. Prometheus: inducing fine-grained evaluation capability in language models.  In The Twelfth International Conference on Learning Representations,  Cited by: Appendix E, §2. 
  * Kuhn et al. (2023) L. Kuhn, Y. Gal, and S. Farquhar Semantic uncertainty: linguistic invariances for uncertainty estimation in natural language generation.  In International Conference on Learning Representations,  Cited by: Table 7, §1, §2, §4.2. 
  * Lakshminarayanan et al. (2017) B. Lakshminarayanan, A. Pritzel, and C. Blundell Simple and scalable predictive uncertainty estimation using deep ensembles.  In Advances in Neural Information Processing Systems,  Cited by: §2. 
  * Leviathan et al. (2023) Y. Leviathan, M. Kalman, and Y. Matias Fast inference from transformers via speculative decoding.  In International Conference on Machine Learning,  pp. 19274–19286.  Cited by: §2, §3.1. 
  * Lightman et al. (2024) H. Lightman, V. Kosaraju, Y. Burda, H. Edwards, B. Baker, T. Lee, J. Leike, J. Schulman, I. Sutskever, and K. Cobbe Let’s verify step by step.  In International Conference on Learning Representations (ICLR),  Cited by: §2. 
  * Liu et al. (2020) W. Liu, X. Wang, J. Owens, and Y. Li Energy-based out-of-distribution detection.  In Advances in Neural Information Processing Systems,  Vol. 33, pp. 21464–21475.  Cited by: §1. 
  * Manakul et al. (2023) P. Manakul, A. Liusie, and M. J. Gales SelfCheckGPT: zero-resource black-box hallucination detection for generative large language models.  In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing,  pp. 9004–9017.  Cited by: Appendix E, §1, §2. 
  * Ong et al. (2025) I. Ong, A. Almahairi, V. Wu, W. Chiang, T. Wu, J. E. Gonzalez, M. W. Kadous, and I. Stoica RouteLLM: learning to route LLMs with preference data.  In International Conference on Learning Representations,  Cited by: §1, §1, §1, §2, §4.1, §4, §4, §5.1. 
  * Shorinwa et al. (2024) O. Shorinwa, Z. Mei, J. Lidard, A. Z. Ren, and A. Majumdar A survey on uncertainty quantification of large language models: taxonomy, open research challenges, and future directions.  arXiv preprint arXiv:2412.05563.  Cited by: §2. 
  * Srinivas et al. (2024) N. Srinivas, M. Shoaib, and H. Lakkaraju Large language models must be taught to know what they don’t know.  In Advances in Neural Information Processing Systems,  Cited by: §1, §1, §2. 
  * Sun et al. (2024) G. Sun, P. Manakul, A. Liusie, K. Pipatanakul, C. Zhang, P. Woodland, and M. Gales CrossCheckGPT: universal hallucination ranking for multimodal foundation models.  arXiv preprint arXiv:2405.13684.  Cited by: Appendix E, §1, §2. 
  * Tian et al. (2023) K. Tian, E. Mitchell, A. Zhou, A. Sharma, R. Rafailov, H. Yao, C. Finn, and C. D. Manning Just ask for calibration: strategies for eliciting calibrated confidence scores from language models fine-tuned with human feedback.  In Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing (EMNLP),  pp. 5433–5442.  Cited by: §2. 
  * Xue et al. (2025) Y. Xue, K. Greenewald, Y. Mroueh, and B. Mirzasoleiman Verify when uncertain: beyond self-consistency in black box hallucination detection.  arXiv preprint arXiv:2502.15845.  Cited by: §2. 
  * Zhang et al. (2024) L. Zhang, A. Hosseini, H. Bansal, M. Kazemi, A. Kumar, and R. Agarwal Generative verifiers: reward modeling as next-token prediction.  In Advances in Neural Information Processing Systems (NeurIPS),  Cited by: §2. 
  * Zheng et al. (2023) L. Zheng, W. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang, Z. Lin, Z. Li, D. Li, E. Xing, et al. Judging LLM-as-a-judge with MT-bench and chatbot arena.  In Advances in Neural Information Processing Systems,  Vol. 36.  Cited by: Appendix E, §1, §2. 



## Appendix

## Appendix A Full Results

Tables 3–6 report per-pair results across all four benchmarks. Pairs are grouped by type—same-size cross-family, cross-family asymmetric, and same-family asymmetric—and sorted by capability gap (descending) within each group. For each pair we report AUROC and APGR for the within-model entro
