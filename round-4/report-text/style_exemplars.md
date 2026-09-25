Style note: These papers use short declarative sentences interleaved with longer compound ones. Hedging is sparse and precise ("should be viewed as lower bounds"). First person is "we" or "our" throughout. Numbers are stated directly in sentences. Citation density is high—typically 2–4 per paragraph.

---

## Thatikonda, Buntine & Shareghi (2025). "Assessing the Sensitivity and Alignment of FOL Closeness Metrics." EMNLP 2025 Findings.
https://arxiv.org/abs/2501.08613

**Abstract.** "The recent successful paradigm of solving logical reasoning problems with tool-augmented large language models (LLMs) leverages translation of natural language statements into First-Order Logic (FOL) and external theorem provers."

**Introduction (first paragraph).** "Large language models (LLMs) have advanced natural language reasoning, but logical and mathematical reasoning have long relied on formal, structured languages for proving deductions and theorems."

**Results paragraph.** "From Table 4, we observe that quantifier perturbations have minimal impact overall. However, when metrics are combined (Table 5), Smatch++ proves to be a more sensitive metric for detecting changes in quantifiers. Negation perturbations, applied to nearly all records, exhibit a pronounced effect on the BL score, with SP scores showing the highest sensitivity to negation changes."

**Limitations paragraph.** "We recognize that GPT models used in our experiments are continually evolving, which may lead to variations in results over time. To manage the computational cost of generating multiple samples, we limited the data sample used in the experiments."

---

## Pagnoni, Balachandran & Tsvetkov (2021). "Understanding Factuality in Abstractive Summarization with FRANK: A Benchmark for Factuality Metrics." NAACL 2021.
https://arxiv.org/abs/2104.13346

**Abstract.** "Modern summarization models generate highly fluent but often factually unreliable outputs. This motivated a surge of metrics attempting to measure the factuality of automatically generated summaries."

**Introduction (first paragraph).** "Factuality is defined as a measure of 'whether eventualities are characterized as corresponding to facts, possibilities, or situations that do not hold in the world.'"

**Results paragraph.** "From our annotations, we observe that 60% of the summaries that were annotated contain at least one factual error. From Figure 2, we see that the XSum dataset has more factually incorrect model summaries (92%) than CNN/DM (43%)."

**Limitations paragraph.** The confusion matrix analysis reveals that "all categories with the exception of OutE are frequently confused with NE" (no error), largely due to annotation noise. Notably, coreference errors show 69.7% confusion with non-errors, suggesting annotators overlook missing antecedents despite clear instructions.

---

## Brunello, Geatti, Mignani, Montanari & Saccomanno (2025). "Do LLMs Really Struggle at NL-FOL Translation?" AAAI 2026.
https://arxiv.org/abs/2511.11816

**Abstract.** "Due to its expressiveness and unambiguous nature, First-Order Logic (FOL) is a powerful formalism for representing concepts expressed in natural language (NL). This is useful, e.g., for specifying and verifying desired system properties. While translating FOL into human-readable English is relatively straightforward, the inverse problem, converting NL to FOL (NL-FOL translation), has remained a longstanding challenge, for both humans and machines."

**Introduction (first paragraph).** "Natural language (NL) stands as humanity's primary and most intuitive means of encoding and transmitting knowledge, thanks to its expressiveness and remarkable flexibility. Nevertheless, these very characteristics, while enabling rich communication, also introduce challenges such as inherent ambiguity and often a lack of complete context."

**Results paragraph.** "All the models perform well on the considered datasets. The weakest result is the .72 achieved by Qwen3-8B on D_FOLIO, meaning that, nevertheless, in 72% of the cases the model translates a NL sentence into a FOL formula equivalent to the reference."

**Limitations paragraph.** "Because we performed no prompt engineering (e.g., we did not use any few-shot exemplars) the reported scores should be viewed as lower bounds on the models' capabilities. A thorough analysis of prompting strategies, which is beyond the scope of the present paper, is left for future work."

---

## Brunello, Curaba, Geatti, Mignani, Montanari & Saccomanno (2026). "Fixing FOLIO and MALLS: Verified Annotations and an LLM-assisted Framework to Focus Human Relabeling."
https://arxiv.org/abs/2606.02837

**Abstract.** "Accurate translation from Natural Language to First-Order Logic (NL-to-FOL) underpins neurosymbolic AI systems and Natural Language Inference (NLI), making the quality of NL-to-FOL benchmarks essential—yet these datasets have never been rigorously audited. Our first contribution is to present a systematic human inspection of the validation split of FOLIO and a subset of MALLS test instances, finding that approximately 42.5% and 42% of entries, respectively, contain incorrect FOL formalizations (i.e., ground truth labels), with additional rates of ambiguous NL sentences (17.8% and 51%) and incorrect NLI labels in FOLIO (8.4%)."

**Introduction (first paragraph).** "Automatically translating Natural Language (NL) into a machine-readable formalism—often called autoformalization—is a fundamental building block of neurosymbolic AI, with applications ranging from Natural Language Inference (NLI) to runtime verification and AI safety. Among the target formalisms, First-Order Logic (FOL) stands out for its expressiveness and computational tractability. Yet, NL-to-FOL translation remains a longstanding challenge for both humans and automated systems."

**Results paragraph.** "On FOLIO, 90% accuracy is reached after reviewing only 20% of instances— a third of the effort required by the Green Baseline (61%) and less than a third of that required by the Black Baseline (76%). On MALLS, the reduction is even more pronounced: 5% suffices against 29% for the Green Baseline (a >5× reduction) and against 76% for the Black Baseline (a 15× reduction)."

**Limitations paragraph.** "Dataset curation is inherently delicate and error-prone. Despite the strategies adopted to remain as objective as possible, curation remains an inherently subjective process, and residual annotation mistakes may persist. We therefore expect that the exact error and ambiguity counts reported here could shift slightly upon further scrutiny."

---

## Section outlines

### Thatikonda et al. 2025 — "Assessing the Sensitivity and Alignment of FOL Closeness Metrics"
1. Introduction
2. Closeness Metrics
3. Evaluation Framework
4. Experiments
5. Results and Discussion
6. Conclusion
Method organised by: metric family (n-gram, graph, embedding, LLM).
Results organised by: perturbation type, then metric comparison.

### Pagnoni et al. 2021 — "FRANK"
1. Introduction
2. Typology of Factual Errors
3. Dataset Creation
4. Summarization Model Analysis
5. Factuality Metric Evaluation
6. Related Work
7. Conclusion
Method organised by: component (typology, then annotation protocol, then metric evaluation).
Results organised by: dataset (CNN/DM vs XSum), then metric-by-metric correlation.

### Brunello et al. 2025 — "Do LLMs Really Struggle at NL-FOL Translation?"
1. Introduction
2. Related Work
3. Limitations of Current Evaluation Protocols
4. Our Novel Benchmarking Strategy
5. Experiments
6. Results and Discussion
7. Conclusions and Future Work
Method organised by: pipeline stage (ontology extraction, then translation, then equivalence check).
Results organised by: dataset, then model family.

### Brunello et al. 2026 — "Fixing FOLIO and MALLS"
1. Introduction (Contributions)
2. Datasets and Their Quality Analysis (Datasets; Quality Analysis; LLM Re-evaluation)
3. LLM-assisted Human Oversight (Verdict-and-Refinement Task; Pipelines; Prioritization)
4. Experimental Setup
5. Results and Discussion
6. Conclusions and Future Works
7. Limitations
Method organised by: component (audit, then LLM-assisted review framework).
Results organised by: dataset (FOLIO vs MALLS), then evaluation metric.
