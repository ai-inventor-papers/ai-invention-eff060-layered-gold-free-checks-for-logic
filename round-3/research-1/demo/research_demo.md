# What is new about peer agreement for logic

## Summary

Prior-art positioning (web research, $0 LLM spend, 63 sources, 139 verbatim quotes machine-checked against fetched text) for the iteration-3 claim that cross-family solver consensus is a gold-free NL->FOL faithfulness metric. SCOOP RULE (multi-family translations + solver equivalence + faithfulness-label meta-eval on NL->FOL): no hit meets all three, so C1 is not scooped. Closest neighbours meet two of three each: ARc 2511.09008 (NL->SMT, k LLMs, per-translation confidence = share of k translations entailing it, i.e. the same score form as c_score, but a fixed schema and downstream-QA labels); NoTB 2608.21962 (RTL, 4 families, precision 63/85.3/87/94.7% at >=1..4 families, coverage 100/49/33/27%, spec-level, no AUROC); GenV 2609.11085 (NL->FOL, single trained verifier, AUROC 0.961 on Z3-reference labels; single-model SC K=5 = 0.863; the judge beats GenV 0.778 vs 0.679 when labels switch to panel intent). The closest meta-evaluation design is SCP-NL2TL 2608.05439 (NL->temporal logic, single-model SC vs judge vs back-translation AUROC by difficulty tier; SC AUROC rises with tier). VERDICTS: C1 NEEDS-QUALIFIER (the method is not new; claim the first meta-evaluation of cross-family consensus as a per-candidate NL->FOL faithfulness score vs an API judge, nested over the baseline stack; win and loss wordings are given); C2 SAFE (cite GenV's label-target reversal and wrong-gold rates, 2606.02837 v1 39%/36% vs v2 42.5%/42%); C3 NEEDS-QUALIFIER (predicate alignment exists in LogicLLaMA and Vossel; no neighbour reports a rename false-alarm rate); C4 NEEDS-QUALIFIER (balanced-accuracy maths; the scatter premise is stated by LLMs-as-Jury, CLOVER and Chen & Avizienis 1978, who noted identical wrong results from missing logic; the new piece is a measured identical-wrong vs both-wrong curve over number of conditions, set against Eckhardt-Lee's coincident-failure-rises-with-difficulty); C5 NEEDS-QUALIFIER (LLMs-as-Jury already recommend 3-4 cross-family models; effective-N results: 7 models ~ 2.58, 9 judges ~ 2). Also supplies: the positioning table on 10 axes; a premise-evidence table (60% agree-when-both-wrong on MCQ, rho 0.20-0.59, beta 0.052-0.127, KL 1255 tests); judge-degradation evidence (AutoEval: equivalence verification fails beyond toy complexity; >20 operators <50%); cost norms; 8 required extra rows (single-family SC, precision@coverage by k, endorsement vs both-wrong by conditions, k-curve per tercile, rename FA per matcher, label-protocol sensitivity, n_eff, cite ARc); AuthorYYYY citation strings; and a search log. Files: research_report.md (main), notes/QUOTES.md (quote ledger).

## Research Findings

VERDICT SUMMARY. No paper meets the pre-stated scoop rule, i.e. (i) multiple model families' formal translations + (ii) solver equivalence + (iii) meta-evaluation of the agreement score against faithfulness labels on NL->FOL. So C1 is NOT scooped as a method-plus-evaluation package. But the METHOD itself is not new, and all five claims except C2 need qualifiers.

CLOSEST NEIGHBOURS. (1) ARc [33] redundantly translates NL into SMT-LIB with several LLMs. It scores each translation by "the proportion of the k translations that non-vacuously entail" it. This is the same functional form as our c_score. But it works over a fixed shared schema, so no vocabulary alignment is needed, and it is validated on downstream QA soundness (98.4%->99.4%), not translation-faithfulness labels [33]. (2) NoTB [1] clusters RTL from four LLM families by formal equivalence. Specification-level precision rises from 63% to 85.3% / 87% / 94.7% at >=2/3/4 agreeing families, with coverage 49/33/27%. It is a triage selector against hidden-testbench labels. It compares LLM judges only at a different unit (completion level), and reports no AUROC and no complexity analysis [1]. (3) GenV [3] is NL->FOL/SMT with AUROC 0.961. It is a single trained verifier, and its labels are Z3-equivalence to the gold. Importantly, its single-model self-consistency (K=5) baseline already reaches AUROC 0.863 on NL->FOL. Its LLM judge wins (0.778 vs 0.679) when the target switches from Z3-reference equivalence to panel-majority intent [3]. (4) SCP-NL2TL [34] is the closest meta-evaluation design. It reports error-detection AUROC of single-model self-consistency vs back-translation vs judge vs fusion channels by difficulty tier (number of atomic propositions) for NL->temporal logic, and self-consistency AUROC rises with tier [34]. Other near-neighbours: LLMs-as-a-Jury [2] (answers), ADMITOR [30] (3 families, optimization models, precision 0.927 vs 0.871 for a single-model vote), VERGE [32] (cross-model consensus "supported but not yet evaluated"), and single-model selectors Li et al. [4], GoFU [5], SCD [35] and CLOVER [9].

C1 (beats API judge; adds over baseline stack): NEEDS-QUALIFIER. Claim only "the first meta-evaluation of cross-family solver consensus as a gold-free faithfulness score for individual NL->FOL candidates, against adjudicated labels, head-to-head with an API judge and nested over the parse / round-trip / judge / self-consistency / structural stack". Credit ARc [33] and NoTB [1] for the score form. Never say "we propose cross-model consensus", and never claim superiority over judges in general (GenV shows the reverse under intent labels [3]). If T1 loses to the API judge, report parity plus cost (~$0.0015/sentence vs ~$0.00004/judge call).

C2 (holds with aligner-free labels): SAFE as a methodological contribution. No neighbour controls for the labeller and the metric sharing an instrument. Cite GenV's label-target reversal [3], and wrong gold in FOLIO/MALLS, which is 39%/36% in v1 but 42.5%/42% in v2 (3 Sep 2026) of 2606.02837 [24].

C3 (rename-invariant hybrid matcher): NEEDS-QUALIFIER. Predicate alignment exists: LogicLLaMA greedy binding search [36], Levenshtein <=0.6 mapping [37], and leaf-matching left open by [31]. No neighbour reports a rename false-alarm rate. That is the novel piece (ours: 0.859 ALIGN vs 0.074 NF).

C4 (e/d decomposition; endorsement falls with conditions): NEEDS-QUALIFIER. AUROC = 1-(e+d)/2 at a fixed threshold is balanced accuracy. The scatter premise is stated by [2, 9, 40], and identical-wrong outputs from missing logic were noted in 1978 [60]. Coincident-FAILURE theory predicts that both-wrong rises with input difficulty [21, 22, 23]. Replications confirm concentration on hard inputs [18, 20]. LLM correlated-error work does not condition on difficulty: [14] names it as future work, and [2] uses a scalar attractor rate. So the candidate-new piece is the MEASURED identical-wrong (endorsement) vs both-wrong curve over number of conditions for NL->FOL. Indirect support for the falling direction: [34, 49, 54]. Counter-evidence: [14, 50, 52, 62].

C5 (3-5 families suffice): NEEDS-QUALIFIER. It is already recommended ("three to four cross-family models" [2]), and it is consistent with NoTB's curve [1] and effective-N results (7 models ~ 2.58 [15]; 9 judges ~ 2 votes [48]; 16 models ~ 1.69 formulations [63]). Novelty exists only per complexity tercile with cost.

CONTEXT NUMBERS TO QUOTE. 60% agreement when both wrong (MCQ) [14]; rho 0.20-0.59 [16]; all-wrong beta 0.052-0.127 [50]; Knight-Leveson 1255 coincident-failure tests [20]. Judge limits: equivalence verification collapses beyond toy complexity and >20 operators yields <50% truth maintenance [28]; judges disagree 26-37 pp [26]; judge 87/97 agreement with humans but "not an equivalence oracle" [29]. Costs: NoTB $14.93 generation for 78 specs and 1,556 judge calls per judge [1]; GenV ~12 H100 GPU-hours of training [3].

CONFIDENCE. High that the method is not new (verbatim quotes from [1, 33]). Medium that no NL->FOL cross-family meta-evaluation exists: the sweep was logged but not systematic, and forward citations of NoTB and roundtrip were rate-limited. Medium on C4: the classical papers [21, 22] were read as abstracts plus review [23]. A 1990s tabulation of identical-wrong outputs vs input complexity, or a GenV/VERGE follow-up evaluating cross-model mode, would change the verdicts.

## Sources

[1] [NoTB: Oracle-Free Triage of LLM-Generated RTL via Cross-Model Formal Consensus](https://arxiv.org/html/2608.21962v1) (Elisavet Lydia Alvanaki, Je Yang, Biruk Seyoum, Luca P. Carloni; 2026) — Closest cross-family formal-consensus system (RTL, MLCAD 2026, arXiv v1): 4 LLM families, SEC clustering; spec-level precision 63/85.3/87/94.7% at >=1..4 families, coverage 100/49/33/27%; judge baseline only at completion level; no AUROC, no complexity analysis; port-name heuristics.

> On 78 CVDP RTL-generation tasks, four-family formal consensus achieves 94.7% precision at 27% coverage; three-family consensus achieves 87% precision at 33% coverage.

Locator: Q1a; arXiv v1 (22 Aug 2026), MLCAD 2026; Abstract

> raises precision to 85.3% and 87%, respectively

Locator: Q1b; v1; Sec 4.3.1

> Tool errors, interface mismatches, and inconclusive results do not contribute equivalence edges.

Locator: Q1c; v1; Sec 3.2

[2] [LLMs as a Jury: Cross-Model Consensus Can Outperform Process Reward Models for LLM Reasoning](https://arxiv.org/html/2607.10139) (Ning Liu; 2026) — States the scatter premise verbatim and gives a closed-form law with latent difficulty and a scalar per-benchmark shared-attractor rate s; shared-error floor ~0 on math, non-trivial on science; recommends 3-4 cross-family models; decorrelation beats more samples (arXiv v3).

> wrong answers scatter while the correct one accumulates agreement

Locator: Q2a; arXiv v3 (17 Aug 2026); Sec 1

> the probability that, when a model is wrong, it produces the single attractor wrong answer that other erring models also tend to produce.

Locator: Q2b; v3; Sec 3.2

> This is the minimal model that couples the two forces governing agreement: a shared difficulty that correlates errors, and a shared attractor that makes some errors agree.

Locator: Q2c; v3; Sec 3.2 Generative model

[3] [Beyond Solver Verdicts: Generative Reward Models for Autoformalization (GenV)](https://arxiv.org/html/2609.11085) (Vikash Singh, Debargha Ganguly, Aman Goel, Ali Torkamani; 2026) — Reference-free score distilled from a Z3-equivalence oracle for NL->FOL/SMT (AUROC 0.961); single-model SC K=5 baseline 0.863; judge wins (0.778 vs 0.679) when labels switch from Z3-reference to panel intent (arXiv v2).

> we introduce Generative Verification (GenV), which distills an offline Z3-equivalence oracle into a reference-free, continuous reference-equivalence score

Locator: Q3a; arXiv v2 (11 Sep 2026); Abstract

> On the combined benchmark of 950 rows containing 260 VPUs, GenV+HN achieves 0.961 AUROC.

Locator: Q3b; v2; Sec 5 RQ1

> achieving 0.964 on ProverQA, 0.925 on MALLS, 0.915 on ProntoQA, 0.842 on ProofWriter, 0.830 on FOLIO, and 0.642 on LogicNLI

Locator: Q3c; v2; Sec 5 RQ2

[4] [Autoformalize Mathematical Statements by Symbolic Equivalence and Semantic Consistency](https://arxiv.org/html/2410.20936) (Zenan Li, Yifan Wu, Zhaoyu Li, Xinming Wei, Xian Zhang, Fan Yang, Xiaoxing Ma; 2024) — NeurIPS 2024: selection among k temperature samples of one model using prover-checked symbolic equivalence; labels by manual check; a selector, not a score.

> we employ few-shot prompting, and set the temperature of the generation process to

Locator: Q4a; arXiv v2, NeurIPS 2024; Sec 5 Model

> the MATH dataset does not contain aligned formal statements, we manually check each formalization result.

Locator: Q4b; v2; Sec 5 Metric

> The relative efficiency of our method, ranging from 8.4% to 21.9%

Locator: Q4c; v2; Sec 1

[5] [Grammars of Formal Uncertainty (GoFU)](https://arxiv.org/html/2505.20047) — Single-model multi-sample PCFG uncertainty over SMT-LIB programs; selective verification cuts errors 14-100%; SMT autoformalization hurts FOLIO (-44.5%).

> enables selective verification to cut error rates by 14-100% with minimal abstention

Locator: Q5a; arXiv v1; NeurIPS 2025 (proceedings); Sec 1 contributions

> SMT-based autoformalization significantly boosted accuracy on tasks like ProofWriter (+34.8%) but harmed others like FOLIO (-44.5%)

Locator: Q5b; v1; Sec 1

[6] [SAC3: Reliable Hallucination Detection in Black-Box Language Models via Semantic-aware Cross-check Consistency](https://arxiv.org/html/2311.01740v2) (Jiaxin Zhang, Zhuohang Li, Kamalika Das, Bradley A. Malin, Sricharan Kumar; 2023) — Cross-model + cross-question consistency beats self-consistency for QA hallucination detection (AUROC 99.4/97.0).

> achieves a high AUROC score of 99.4% and 97.0% respectively, which significantly outperforms the self-consistency baseline

Locator: Q6a; arXiv v2; EMNLP 2023 (arXiv comment); Sec 1

[7] [FormalAlign: Automated Alignment Evaluation for Autoformalization](https://arxiv.org/abs/2410.10135) (Jianqiao Lu, Yingjia Wan, Yinya Huang, Jing Xiong, Zhengying Liu, Zhijiang Guo; 2024) — Trained alignment scorer (dual loss) for Lean autoformalization; GenV reports it at 0.752 AUROC on its expanded split.

> employing a dual loss that combines a pair of mutually enhancing autoformalization and alignment tasks

Locator: Q7a; arXiv v1; ICLR 2025 (OpenReview PDF header); Abstract

[8] [Faithful Autoformalization via Roundtrip Verification and Repair](https://arxiv.org/abs/2604.25031) (Daneshvar Amrollahi, Jerry Lopez, Clark Barrett; 2026) — Gold-free roundtrip equivalence check for many-sorted FOL statutes with two LLMs; failing rules show 1.4-2.5x more NLI drift; occupies the roundtrip lane (arXiv v3).

> We propose a roundtrip verification approach which does not require ground-truth annotations

Locator: Q8a; arXiv v3 (21 Sep 2026); Abstract

> rules that fail the equivalence check show 1.4x-2.5x more natural language inference (NLI) drift than rules that pass it

Locator: Q8b; v3; Abstract

[9] [Divide and Translate: Compositional First-Order Logic Translation and Verification for Complex Logical Reasoning (CLOVER)](https://arxiv.org/html/2410.08047v2) (Hyun Ryu, Gyeongman Kim, Hyemin S. Lee, Eunho Yang; 2024) — ICLR 2025 NL->FOL: states that incorrect formulas are less likely to be logically equivalent, but notes consistent last-step mistakes yielding equivalent incorrect formulas; selector.

> An LLM might also make mistake in intermediate steps of compositional first-order logic translation and generate incorrect formulas, but these are less likely to be logically equivalent.

Locator: Q9a; arXiv v2; ICLR 2025 camera-ready; Sec 3.3 Logical Consistency

> However, we observe that an LLM sometimes makes consistent mistakes in the last step of compositional first-order logic translation, which leads to logically equivalent incorrect formulas.

Locator: Q9b; v2; Sec 3.3 Logical Consistency

[10] [Clover: Closed-Loop Verifiable Code Generation](https://arxiv.org/abs/2310.17807) (Chuyue Sun, Ying Sheng, Oded Padon, Clark Barrett; 2023) — Consistency checks among code, docstrings and formal annotations; the other 'Clover' (distinct from CLOVER [9]).

> Clover performs consistency checks among code, docstrings, and formal annotations.

Locator: Q10a; arXiv v4; Abstract

[11] [Reasoning without Gold Standards: A Proxy-Judge Theory of Autoformalization](https://arxiv.org/html/2606.09449) (Lei Xu, Xin Quan, André Freitas; 2026) — Reference-free per-axis property checks for autoformalization; no cross-model consensus or label meta-evaluation found.

> We introduce a reference-free proxy-judge framework for AF that replaces gold-standard matching with a vector of per-axis property checks.

Locator: Q11a; arXiv v1 (8 Jun 2026); Abstract

[12] [Monotonic Reference-Free Refinement for Autoformalization](https://arxiv.org/abs/2601.23166) (Lan Zhang, Marco Valentino, André Freitas; 2026) — Reference-free refinement from prover + LLM-judge feedback; not a consensus metric.

> leverages complementary feedback from theorem provers and LLM-based judges, without access to ground-truth or existing formalizations

Locator: Q12a; arXiv v2 (7 May 2026); Abstract

[13] [When Does Consensus Mean Correctness? Measuring the Agreement-Accuracy Coupling](https://arxiv.org/html/2608.05670) (Rasul Khanbayov, Hasan Kurban; 2026) — Agreement certifies correctness only above a threshold set by error diffuseness (diffuse at level L if leading wrong mass <= (1-P(correct))/L); single-model VLM chart QA; disclaims novelty of the concentration-vs-correctness distinction.

> it certifies correctness only above a threshold set by how diffuse the model

Locator: Q13a; arXiv v1 (6 Aug 2026); Sec 1 contributions

> nor novelty for the concentration-versus-correctness distinction itself, which the self-consistency literature states.

Locator: Q13b; v1; Sec 1

> dispersion spread over many wrong answers cannot produce a confidently wrong consensus

Locator: Q13c; v1; Sec 4, after Prop. 5

[14] [Correlated Errors in Large Language Models](https://arxiv.org/html/2506.07962) (Elliot Kim, Avi Garg, Kenny Peng, Nikhil Garg; 2025) — ICML 2025: models agree 60% when both err (MCQ); more accurate pairs have more correlated errors; difficulty conditioning explicitly left to future work.

> on one leaderboard dataset, models agree 60% of the time when both models err.

Locator: Q14a; arXiv v1; ICML 2025; Abstract

> Importantly, even after conditioning on these factors, pairs of models that are more accurate individually also have more correlated errors.

Locator: Q14b; v1; Sec 1

> judges overinflate the accuracy of models that are less accurate than it

Locator: Q14c; v1; Sec 1

[15] [Wavering Oracles: Selective Updating and Correlated Failures in LLMs](https://arxiv.org/html/2609.11428) (Xiaoshn Nee, Haobo Zhong, Xiaomin Ni; 2026) — Mean error correlation 0.285 reduces 7 models to 2.58 effective independent models (4-option MCQ, 600 items).

> The published models have 70.5 percent mean exact answer agreement and 0.285 mean pairwise error correlation.

Locator: Q15a; arXiv v1 (10 Sep 2026); Sec 5 (ensemble)

> SycoBench-600 contains 600 English four option questions

Locator: Q15b; v1; Sec 4 data

> Mean error correlation of 0.285 reduces seven models to an effective independent count of 2.58.

Locator: Q15c; v1; Abstract

[16] [When LLMs Agree, Are They Right? Auditing Self-Consistency and Cross-Model Agreement](https://arxiv.org/abs/2607.08065) (Kaihua Ding; 2026) — Agreement is a positive but weak predictor (rho 0.20-0.59); confident errors recur across providers.

> agreement is a positive but weak predictor (rho 0.20-0.59, all positive under item-clustered resampling)

Locator: Q16a; arXiv v2 (28 Jul 2026); Abstract

> with confident errors recurring across providers above a marginal-preserving null

Locator: Q16b; v2; Abstract

[17] [Decomposing Wrong-Consensus Agreement in LLM Self-Consistency](https://arxiv.org/abs/2608.18795) (2026) — Wrong-consensus decomposition; coverage phi higher on MCQ than open-domain; 'Agreement is graded evidence, not certification.'

> coverage phi (the mechanical/empirical ratio) shows a benchmark-associated direction: 0.81-0.93 on multiple-choice GPQA-Diamond against 0.59-0.78 on open-domain AIME

Locator: Q17a; arXiv v2 (31 Aug 2026); Abstract

> Agreement is graded evidence, not certification.

Locator: Q17b; v2; Abstract

[18] [N-Version Programming with Coding Agents](https://arxiv.org/html/2606.20158) (Javier Ron, Benoit Baudry, Martin Monperrus; 2026) — Knight-Leveson replication with 48 agent implementations: 429 coincident failures vs 115.36 expected; failures concentrate in hard spec parts.

> the experiment produces 429 coincident-failure cases where the random independence model predicts only 115.36

Locator: Q18a; arXiv v1 (18 Jun 2026); Sec 1

> Failures overwhelmingly concentrate in LICs 9 and 14

Locator: Q18b; v1; Fig 7 caption

[19] [SHADOWBENCH: Toward Reliable Automatic Evaluation of Semantic Alignment in Autoformalization](https://arxiv.org/abs/2608.29270) (2026) — Benchmark for automatic semantic-alignment evaluation in autoformalization (arXiv v3; EMNLP 2026 per arXiv comment); no cross-model consensus.

> that characterize the intended statement

Locator: Q19a; arXiv v3; EMNLP 2026; Abstract

[20] [An Experimental Evaluation of the Assumption of Independence in Multiversion Programming](https://dspace.mit.edu/server/api/core/bitstreams/1331578f-65c1-4665-a0be-1bc3cdc001d5/content) (John C. Knight, Nancy G. Leveson; 1986) — IEEE TSE 12(1): 27 versions, 10^6 tests, 1255 tests with >1 version failing; independence rejected; counts coincident failures, Boolean outputs.

> incorrect output given the same input) is very low for independently developed software

Locator: Q20a; IEEE TSE 12(1):96-109, 1986 (author PDF); Sec 1

> Table 2 shows the number of test cases in which more than one version failed on the same input.

Locator: Q20b; 1986; Sec 4

> which more than one version failed was 1255

Locator: Q20c; 1986; Sec 5

[21] [A Theoretical Basis for the Analysis of Multiversion Software Subject to Coincident Errors](https://dl.acm.org/doi/10.1109/TSE.1985.231895) (Dave E. Eckhardt, Larry D. Lee; 1985) — IEEE TSE 11(12) (abstract only): intensity of coincident errors; varying input difficulty implies dependent failures.

> An intensity function, called the intensity of coincident errors, has

Locator: Q21a; IEEE TSE 11(12):1511-1517, 1985 (abstract only); Abstract

[22] [Conceptual Modeling of Coincident Failures in Multiversion Software](https://ntrs.nasa.gov/citations/19900036555) (Bev Littlewood, Douglas R. Miller; 1989) — IEEE TSE 15(12) (abstract only): forced diversity can decrease simultaneous failure probability.

> The use of diverse methodologies is shown to decrease the probability of the simultaneous failure of several

Locator: Q22a; IEEE TSE 15(12):1596-1614, 1989 (abstract only); Abstract

[23] [Software Fault Tolerance by Design Diversity (chapter, Lyu ed.)](https://www.adelard.com/media/vfngprxq/divchap.pdf) (Peter Bishop; 1995) — Review: dissimilar faults do not guarantee dissimilar failures; degree-of-difficulty theory; binary failure-bias example of negatively correlated failures.

> dissimilar faults do not guarantee dissimilar failures

Locator: Q23a; Bishop, shortened chapter of Lyu (ed.) Software Fault Tolerance, Wiley 1995; Sec 2

> any variation in the degree of difficulty for particular input

Locator: Q23b; 1995; Sec 4

> In one program the failure (when it occurred) produced a

Locator: Q23c; 1995; Sec 2

[24] [Fixing FOLIO and MALLS: Verified Annotations and an LLM-assisted Framework to Focus Human Relabeling](https://arxiv.org/abs/2606.02837) (Andrea Brunello, Cristian Curaba, Luca Geatti, Michele Mignani, Angelo Montanari, Nicola Saccomanno; 2026) — Wrong-gold rates: v1 (1 Jun 2026) 39%/36%; v2 (3 Sep 2026) 42.5%/42% for FOLIO/MALLS; cite v2 and note v1.

> contain incorrect FOL formalizations (i.e., ground truth labels)

Locator: Q24a; arXiv v2 (3 Sep 2026), accepted EMNLP 2026; Abstract

[25] [Do LLMs Really Struggle at NL-FOL Translation? Revealing their Strengths via a Novel Benchmarking Strategy](https://arxiv.org/abs/2511.11816) (Andrea Brunello, Luca Geatti, Michele Mignani, Angelo Montanari, Nicola Saccomanno; 2025) — AAAI 2026: critiques NL-FOL evaluation protocols; proposes a contamination-aware protocol; forward-citation seed (1 citer).

> we propose a novel evaluation protocol explicitly designed to distinguish genuine semantic-level logical understanding from superficial pattern recognition, memorization, and dataset contamination

Locator: Q25a; arXiv v1; AAAI 2026 (arXiv comment); Abstract

[26] [The Signal-Coverage Matrix: Stratifying Type and Semantic Errors in Statement Autoformalization](https://arxiv.org/abs/2606.28013) (Chengxiao Dai, Zhaokun Yan, Zhanhui Lin; 2026) — Lean: two judges disagree 26-37 pp on elab-feedback outputs vs 7 pp vanilla; residual traced to gold errors.

> The two judges disagree by 26 to 37 pp on elab-feedback outputs (vs. 7 pp on Vanilla)

Locator: Q26a; arXiv v1 (26 Jun 2026); Abstract

[27] [Assessing the Sensitivity and Alignment of FOL Closeness Metrics](https://arxiv.org/abs/2501.08613) (Ramya Keerthy Thatikonda, Wray Buntine, Ehsan Shareghi; 2025) — Reference-based FOL metrics; BertScore aligns more closely with LLM judgement.

> We observe a closer alignment between BertScore and LLM judgement, proving the importance of semantic evaluation.

Locator: Q27a; arXiv v3; EMNLP 2025 (arXiv comment); Abstract

[28] [Autonomous Evaluation of LLMs for Truth Maintenance and Reasoning Tasks (AutoEval)](https://arxiv.org/html/2410.08437) (Rushang Karia, Daniel Bramblett, Daksh Dobhal, Siddharth Srivastava; 2024) — ICLR 2025: LLMs cannot verify logical equivalence beyond toy complexity; >20 operators none exceed 50% truth maintenance. Closest formal evidence for judge degradation (M3).

> For translating logic expressions with more than 20 operators, none exceeded 50% accuracy in maintaining truth.

Locator: Q28a; arXiv v3; ICLR 2025; Sec 4

> LLMs cannot serve as accurate verifiers of logical equivalence

Locator: Q28b; v3; Sec 4

> for anything but toy expressions (low descriptional complexity), after which

Locator: Q28c; v3; Sec 4

[29] [Beyond Compilation: Evaluating Faithful Natural-Language-to-Lean Statement Formalization](https://arxiv.org/html/2606.31002) (Ke Zhang, Patricio Gallardo Candela, Sudhir Murthy, Yi Xie, Zhi Wang, Maziar Raissi; 2026) — LLM judging agrees with human majority 87/97 but is not an equivalence oracle.

> the criterion agrees with human majority on 87/97 cases

Locator: Q29a; arXiv v2 (3 Sep 2026); Sec 1

[30] [Admission Without Answers: Label-Free Certification and Experience Learning for LLM-Based Optimization Modeling](https://arxiv.org/abs/2608.15565) (Junbo Jacob Lian, Huiling Chen, Hanzhang Qin, Chung-Piaw Teo; 2026) — Three model families + resampled-instance execution: admission precision 0.927 vs 0.871 host majority vote vs 0.726 execution success.

> It generates models from three model families, runs each on the stated problem and on instances with resampled parameters

Locator: Q30a; arXiv v4 (16 Sep 2026); Abstract

> raises candidate-level admission precision to 0.927, against 0.871 for majority vote over the host's own samples and 0.726 for execution success

Locator: Q30b; v4; Abstract

[31] [By Their Fruits You Will Know Them: Comparing Formalizations of Law by the Decisions They Encode](https://arxiv.org/html/2605.25186) (Julius Vernie, Matthias Grabmair; 2026) — Different formalizations rarely share leaf nodes; matching correctness left open (C3 context).

> A Boolean comparison requires a shared input vocabulary, but different formalizations rarely share the same leaf nodes

Locator: Q31b; v2; Sec 4.3.2

> We therefore use the consistency study only to select among candidate models and treat matching correctness as an open limitation.

Locator: Q31c; v2; Sec 4.2.1

[32] [VERGE: Formal Refinement and Guidance Engine for Verifiable LLM Reasoning](https://arxiv.org/html/2601.20055) (Vikash Singh, Darion Cassel, Nathaniel Weir, Nick Feng, Sam Bayless; 2026) — Multi-sample consensus with one formalizer; cross-model consensus 'supported but not yet evaluated' (scoop-risk signal).

> Multi-sample consensus uses one formalizer; cross-model consensus is supported but not yet evaluated.

Locator: Q32a; arXiv v2 (2 May 2026); App E.4 'Bridges and cross-model consensus'

[33] [A Neurosymbolic Approach to Natural Language Formalization and Verification (ARc)](https://arxiv.org/html/2511.09008) (2025) — NL->SMT over a fixed schema; redundant translation with k LLMs; confidence = share of k translations entailing the candidate (same form as c_score); evaluated on downstream QA soundness, not faithfulness labels.

> ARc cross-checks per-query translations across diverse models using a notion of symbolic equivalence, with confidence thresholds indicating semantic agreement.

Locator: Q33a; arXiv v2 (13 Jul 2026); Sec 2

> soundness rises from 98.4% to 99.4% and FPR drops from 4.8% to 1.8%, at the cost of reduced recall (28.0% to 14.9%).

Locator: Q33b; v2; Sec 5 RQ2

> the confidence score of a premise-conclusion pair

Locator: Q33c; v2; Sec 3.2

[34] [SCP-NL2TL: Selective Conformal Prediction with Semantic Verification for NL to Temporal Logic](https://arxiv.org/html/2608.05439) (Yixuan Wang, Licheng Luo, Yu Fu, Kaidi Xu, Yue Dong, Mingyu Cai; 2026) — Closest meta-evaluation design: error-detection AUROC for single-model self-consistency, back-translation, judge and fusion channels by difficulty tier (#atomic propositions); SC AUROC rises with tier.

> This extends self-consistency [60] to formal specifications, where equivalence can be checked exactly [35].

Locator: Q34b; v1; Sec 3

> tiers are defined post hoc by the number of atomic propositions in the reference formula

Locator: Q34c; v1; Sec 4 Tasks and data

> Error-detection AUROC by scoring channel, grouped by information source.

Locator: Q34d; v1; Table 1 caption

[35] [Stratified Consistency Distillation for Natural Language Formalization](https://arxiv.org/abs/2608.30258) (Zhichao Hou, Ferhat Erata, Joe Lilien, MohamadAli Torkamani; 2026) — K translations from one frontier LLM clustered by semantic equivalence for pseudo-labelling; selector.

> We generate K logical translations per input using a frontier LLM and cluster them by semantic equivalence

Locator: Q35a; arXiv v1 (31 Aug 2026); Abstract

[36] [Harnessing the Power of Large Language Models for Natural Language to First-Order Logic Translation (LogicLLaMA)](https://arxiv.org/html/2305.15541) (Yuan Yang, Siheng Xiong, Ali Payani, Ehsan Shareghi, Faramarz Fekri; 2023) — LE metric uses greedy search for the predicate binding that maximises LE (C3 precedent).

> We solve this by finding the binding that gives the highest LE score via greedy search and filling the rest of the missing inputs with dummy inputs.

Locator: Q36a; arXiv v1; ACL 2024 (as cited by GenV); Sec 4.2.3

[37] [Advancing Natural Language Formalization to First Order Logic with Fine-tuned LLMs](https://arxiv.org/html/2509.22338) (Felix Vossel, Till Mossakowski, Björn Gehrke; 2025) — Maps predicates by normalised Levenshtein distance (threshold 0.6) before equivalence checking (C3 precedent).

> predicates are mapped to ground truth predicates using the normalized Levenshtein distance (threshold 0.6)

Locator: Q37a; arXiv v2; IJCLR 2025; Sec 3 Predicate matching

> this approach either requires static signatures ensuring that the same predicates are used in both expressions or a normalization step to align predicate names

Locator: Q37b; v2; Sec 2

[38] [Natural Language to Code Translation with Execution (MBR-exec)](https://arxiv.org/abs/2204.11454) (Freda Shi, Daniel Fried, Marjan Ghazvininejad, Luke Zettlemoyer, Sida I. Wang; 2022) — Execution-semantics MBR selection among samples; selector.

> We select output programs from a generated candidate set by marginalizing over program implementations that share the same semantics.

Locator: Q38a; arXiv v2; EMNLP 2022; Abstract

[39] [CodeT: Code Generation with Generated Tests](https://arxiv.org/abs/2207.10397) (Bei Chen, Fengji Zhang, Anh Nguyen, Daoguang Zan, Zeqi Lin, Jian-Guang Lou, Weizhu Chen; 2022) — Dual execution agreement among code samples and generated tests; selector.

> considers both the consistency of the outputs against the generated test cases and the agreement of the outputs with other code samples

Locator: Q39a; arXiv v2; Abstract

[40] [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171) (2022) — ICLR 2023: unique-correct-answer intuition behind agreement-based selection.

> Self-consistency leverages the intuition that a complex reasoning problem typically admits multiple different ways of thinking leading to its unique correct answer.

Locator: Q40a; arXiv v4; ICLR 2023; Abstract

[41] [Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation](https://arxiv.org/abs/2302.09664) (Lorenz Kuhn, Yarin Gal, Sebastian Farquhar; 2023) — Single-model semantic entropy (meaning-level clustering).

> Our method is unsupervised, uses only a single model, and requires no modifications to off-the-shelf language models.

Locator: Q41a; arXiv v3; ICLR 2023; Abstract

[42] [Detecting hallucinations in large language models using semantic entropy](https://www.nature.com/articles/s41586-024-07421-0) (Sebastian Farquhar, Jannik Kossen, Lorenz Kuhn, Yarin Gal; 2024) — Nature 2024: semantic entropy detects confabulations; single model.

> proposing entropy-based uncertainty estimators for LLMs to detect a subset of hallucinations

Locator: Q42a; Nature 630, 2024; Abstract

[43] [Replacing Judges with Juries: Evaluating LLM Generations with a Panel of Diverse Models (PoLL)](https://arxiv.org/abs/2404.18796) (2024) — Judge panel from disjoint families, >7x cheaper than a single large judge.

> exhibits less intra-model bias due to its composition of disjoint model families, and does so while being over seven times less expensive

Locator: Q43a; arXiv v2; Abstract

[44] [Error Detection for Text-to-SQL Semantic Parsing](https://aclanthology.org/2023.findings-emnlp.785/) (2023) — Findings EMNLP 2023: trained parser-independent error detector (semantic-parsing analogue; abstract only).

> we propose a parser-independent error detection model for text-to-SQL semantic parsing

Locator: Q44a; Findings of EMNLP 2023; Abstract

[45] [PET-SQL: A Prompt-Enhanced Two-Round Refinement of Text-to-SQL with Cross-consistency](https://arxiv.org/abs/2403.09732) (2024) — Cross-consistency across different LLMs for SQL selection (abstract only).

> we propose using cross-consistency across different LLMs rather than self-consistency within a particular LLM

Locator: Q45a; arXiv v4; Abstract

[46] [Competition-Level Code Generation with AlphaCode](https://arxiv.org/abs/2203.07814) (2022) — Behavioural clustering/filtering of samples; selector.

> large-scale model sampling to explore the search space, followed by filtering based on program behavior to a small set of submissions

Locator: Q46a; arXiv v1 (Science 2022 version not fetched); Abstract

[47] [Measures of diversity in classifier ensembles (Kuncheva & Whitaker 2003) - author page](https://lucykuncheva.co.uk/ensemble_diversity.html) (Ludmila I. Kuncheva, Christopher J. Whitaker; 2003) — Classical ensemble diversity measures incl. double fault and coincident failure diversity.

> Coincident Failure Diveristy (CFD)

Locator: Q47a; Machine Learning 51, 2003 (listed on author page); Diversity toolbox list

[48] [Nine Judges, Two Effective Votes: Correlated Errors Undermine LLM Evaluation Panels](https://arxiv.org/abs/2605.29800) (Guneet Kohli; 2026) — 9 judges ~ 2 independent votes; difficulty explains 6.8% of the Condorcet gap.

> we find that the 9 judges effectively provide only about 2 independent votes

Locator: Q48a; arXiv v1 (28 May 2026); Abstract

[49] [The Hot Mess of AI: How Does Misalignment Scale With Model Intelligence and Task Complexity?](https://arxiv.org/abs/2601.23045) (Alexander Hägele, Aryo Pradipta Gema, Henry Sleight, Ethan Perez, Jascha Sohl-Dickstein; 2026) — Error-incoherence (variance share) rises with reasoning length/task difficulty (within-model) - supports M1 direction.

> Across all tasks and frontier models we measure, the longer models spend reasoning and taking actions,

Locator: Q49a; arXiv v2; ICLR 2026; Abstract

> as more capable AIs pursue harder tasks, requiring more sequential action and thought, our results predict failures to be accompanied by more incoherent behavior

Locator: Q49b; v2; Abstract

[50] [When Does Combining Language Models Help? A Co-Failure Ceiling on Routing, Voting, and Mixture-of-Agents Across 67 Frontier Models](https://arxiv.org/abs/2606.27288) (Josef Chen; 2026) — All-wrong rate beta caps ensemble gains; rho cannot identify beta; co-failure depends on answer format.

> average pairwise error correlation rho, cannot identify beta: error laws with identical marginals and pairwise correlations can have different all-wrong rates

Locator: Q50a; arXiv v1 (25 Jun 2026); Abstract

> locating co-failure in answer format rather than subject

Locator: Q50b; v1; Abstract

[51] [State-dependent error correlations shape voting thresholds in committees of AI agents](https://arxiv.org/abs/2607.23931) (Haifeng Li, Mo Hai; 2026) — Shared errors create a positive asymptotic error floor for majority voting; dependence differs between good and bad cases.

> shared errors create a positive asymptotic error floor for majority voting

Locator: Q51a; arXiv v1 (27 Jul 2026); Abstract

[52] [Consensus is Not Verification: Why Crowd Wisdom Strategies Fail for LLM Truthfulness](https://arxiv.org/abs/2603.06612) (Yegor Denisov-Blanch, Joshua Kazdan, Jessica Chudnovsky, Rylan Schaeffer, Sheng Guan, Soji Adeshina, Sanmi Koyejo; 2026) — Aggregation fails as a truth signal where errors are strongly correlated (contradicting evidence for consensus).

> aggregation fails to provide a robust truth signal because language model errors are strongly correlated

Locator: Q52a; arXiv v1 (20 Feb 2026); Abstract

[53] [Stochastic Sampling is Epistemically Shallow](https://arxiv.org/abs/2607.20464) (Izhar Ali; 2026) — Self-consistency lacks cross-question structure; only a diverse ensemble surfaces what a model does not know.

> Self-consistency gives accurate per-question uncertainty but no detectable cross-question structure; only a diverse ensemble surfaces what a model does not know.

Locator: Q53a; arXiv v1; EIML@ICML 2026; Abstract

[54] [Simulating Students' Java Programming Errors with Large Language Models](https://arxiv.org/html/2606.14113) (Ali Keramati, Jie Cao, Iman Mohammadi, Mark Warschauer, Yang Shi; 2026) — Harder problems elicited more heterogeneous erroneous outputs (analogy only for M1).

> This indicates that harder problems elicited more heterogeneous erroneous outputs

Locator: Q54a; arXiv v1 (12 Jun 2026); Sec 5

[55] [Beyond accuracy: quantifying trial-by-trial behaviour of CNNs and humans by measuring error consistency](https://arxiv.org/abs/2006.16736) (Robert Geirhos, Kristof Meding, Felix A. Wichmann; 2020) — NeurIPS 2020 error-consistency (kappa) metric for whether systems err on the same inputs.

> a quantitative analysis for measuring whether two decision making systems systematically make errors on the same inputs

Locator: Q55a; arXiv v3; NeurIPS 2020; Abstract

[56] [FormInv: A Measurement Protocol for Semantic Invariance in Mathematical Reasoning Benchmarks](https://arxiv.org/abs/2605.29001) (Nishal Thomas, Noel Thomas; 2026) — Cross-model unanimity used to find paraphrase errors.

> Cross-model unanimity found these errors automatically

Locator: Q56a; arXiv v1; Abstract

[57] [Beyond Gold Standards: Epistemic Ensemble of LLM Judges for Formal Mathematical Reasoning](https://arxiv.org/abs/2506.10903) (Lan Zhang, Marco Valentino, Jordan Meadows, Andre Freitas; 2025) — Ensemble of LLM judges for autoformalization evaluation (judge-side, not translation consensus).

> epistemically and formally grounded ensemble (EFG) of LLM judges

Locator: Q57a; arXiv v2 (21 Aug 2026); Abstract

[58] [Neurosymbolic Auditing of Natural-Language Software Requirements](https://arxiv.org/abs/2605.13817) (Bethel Hall, William Eiers; 2026) — Variation across independent formalizations treated as an ambiguity signal (requirements).

> stochastic variation across independent formalizations is a signal of ambiguity

Locator: Q58a; arXiv v1 (13 May 2026); Abstract

[59] [Inferred Generative-Process Diversity Predicts Correlated Failure Across Language Models](https://arxiv.org/abs/2609.03422) (Ross Tieman, Evan Markou; 2026) — Generative-process diversity associated with reduced correlated failure across 38 models.

> increased generative-process diversity is associated with reduced correlated failure in model pairs

Locator: Q59a; arXiv v1 (3 Sep 2026); Abstract

[60] [N-Version Programming: A Fault-Tolerance Approach to Reliability of Software Operation](https://www.inf.pucrs.br/~zorzo/cs/n-versionprogramming.pdf) (Liming Chen, Algirdas Avizienis; 1978) — FTCS-8 1978: 'faulty but identical results (due to missing logic) may outvote correct results'; defines inexact voting - the identical-wrong vs coincident-failure distinction for C4.

> faulty but identical results (due to missing logic) may outvote correct results

Locator: Q60a; FTCS-8 1978, pp. 3-9 (reprint in FTCS-25, 1995); Sec 5 (experiments)

> For cases in which missing logic is the cause of incorrect software operation, error symptoms

Locator: Q60b; 1978; Sec 5

> These voting processes will be called "inexact voting".

Locator: Q60c; 1978; Sec 3

[61] [Cross-Model Disagreement as a Label-Free Correctness Signal](https://arxiv.org/abs/2603.25450) (Matt Gorbett, Suman Jana; 2026) — Cross-model perplexity as a label-free correctness score (MMLU AUROC 0.75 vs 0.59); not solver-based.

> On MMLU, CMP achieves a mean AUROC of 0.75 against a within-model entropy baseline of 0.59.

Locator: Q61a; arXiv v2 (11 Jun 2026); Abstract

[62] [Harnessing Disagreement: Detecting Correlated Agreement Blindness in Multi-Agent Triage](https://arxiv.org/abs/2607.19899) (Shay Seiya McDonnell, Avantika Singh, Quoc-Viet Pham, Vratislav Havlik, Gregory M.P. O'Hare; 2026) — Stronger base learners increase error correlation and reduce disagreement; 57.2% of errors under agreement (non-LLM).

> ablation shows that strengthening base learners increases error correlation while reducing disagreement

Locator: Q62a; arXiv v1; PAAMS 2026 (arXiv comment); Abstract

[63] [Sixteen models, fewer than two voices: measuring ensemble dispersion where no answer is uniquely correct](https://arxiv.org/abs/2608.00285) (Mario Vega-Barbas, Lidia Mora-Valenciano, Iván Pau, Fernando Seoane, Farhad Abtahi; 2026) — 16 models from 10 families give 1.69 distinct formulations vs 1.43 for one model (effective diversity bound, C5).

> Sixteen language models drawn from ten families produced, on average, the semantic diversity of 1.69 distinct formulations

Locator: Q63a; arXiv (31 Jul 2026); Abstract

## Verification

Numbered citations resolve to unique listed sources. Passage checks test text occurrence, not claim truth or entailment. Author/year metadata and locators are not independently verified. Details: `research_verification.json`.

- Source [1]: text found — On 78 CVDP RTL-generation tasks, four-family formal consensus achieves 94.7% precision at 27% covera
- Source [1]: text found — raises precision to 85.3% and 87%, respectively
- Source [1]: text found — Tool errors, interface mismatches, and inconclusive results do not contribute equivalence edges.
- Source [2]: text found — wrong answers scatter while the correct one accumulates agreement
- Source [2]: text found — the probability that, when a model is wrong, it produces the single attractor wrong answer that othe
- Source [2]: text found — This is the minimal model that couples the two forces governing agreement: a shared difficulty that 
- Source [3]: text found — we introduce Generative Verification (GenV), which distills an offline Z3-equivalence oracle into a 
- Source [3]: text found — On the combined benchmark of 950 rows containing 260 VPUs, GenV+HN achieves 0.961 AUROC.
- Source [3]: text found — achieving 0.964 on ProverQA, 0.925 on MALLS, 0.915 on ProntoQA, 0.842 on ProofWriter, 0.830 on FOLIO
- Source [4]: text found — we employ few-shot prompting, and set the temperature of the generation process to
- Source [4]: text found — the MATH dataset does not contain aligned formal statements, we manually check each formalization re
- Source [4]: text found — The relative efficiency of our method, ranging from 8.4% to 21.9%
- Source [5]: text found — enables selective verification to cut error rates by 14-100% with minimal abstention
- Source [5]: text found — SMT-based autoformalization significantly boosted accuracy on tasks like ProofWriter (+34.8%) but ha
- Source [6]: text found — achieves a high AUROC score of 99.4% and 97.0% respectively, which significantly outperforms the sel
- Source [7]: text found — employing a dual loss that combines a pair of mutually enhancing autoformalization and alignment tas
- Source [8]: text found — We propose a roundtrip verification approach which does not require ground-truth annotations
- Source [8]: text found — rules that fail the equivalence check show 1.4x-2.5x more natural language inference (NLI) drift tha
- Source [9]: text found — An LLM might also make mistake in intermediate steps of compositional first-order logic translation 
- Source [9]: text found — However, we observe that an LLM sometimes makes consistent mistakes in the last step of compositiona
- Source [10]: text found — Clover performs consistency checks among code, docstrings, and formal annotations.
- Source [11]: text found — We introduce a reference-free proxy-judge framework for AF that replaces gold-standard matching with
- Source [12]: text found — leverages complementary feedback from theorem provers and LLM-based judges, without access to ground
- Source [13]: text found — it certifies correctness only above a threshold set by how diffuse the model
- Source [13]: text found — nor novelty for the concentration-versus-correctness distinction itself, which the self-consistency 
- Source [13]: text found — dispersion spread over many wrong answers cannot produce a confidently wrong consensus
- Source [14]: text found — on one leaderboard dataset, models agree 60% of the time when both models err.
- Source [14]: text found — Importantly, even after conditioning on these factors, pairs of models that are more accurate indivi
- Source [14]: text found — judges overinflate the accuracy of models that are less accurate than it
- Source [15]: text found — The published models have 70.5 percent mean exact answer agreement and 0.285 mean pairwise error cor
- Source [15]: text found — SycoBench-600 contains 600 English four option questions
- Source [15]: text found — Mean error correlation of 0.285 reduces seven models to an effective independent count of 2.58.
- Source [16]: text found — agreement is a positive but weak predictor (rho 0.20-0.59, all positive under item-clustered resampl
- Source [16]: text found — with confident errors recurring across providers above a marginal-preserving null
- Source [17]: text found — coverage phi (the mechanical/empirical ratio) shows a benchmark-associated direction: 0.81-0.93 on m
- Source [17]: text found — Agreement is graded evidence, not certification.
- Source [18]: text found — the experiment produces 429 coincident-failure cases where the random independence model predicts on
- Source [18]: text found — Failures overwhelmingly concentrate in LICs 9 and 14
- Source [19]: text found — that characterize the intended statement
- Source [20]: text found — incorrect output given the same input) is very low for independently developed software
- Source [20]: text found — Table 2 shows the number of test cases in which more than one version failed on the same input.
- Source [20]: text found — which more than one version failed was 1255
- Source [21]: UNVERIFIED — An intensity function, called the intensity of coincident errors, has
- Source [22]: text found — The use of diverse methodologies is shown to decrease the probability of the simultaneous failure of
- Source [23]: text found — dissimilar faults do not guarantee dissimilar failures
- Source [23]: text found — any variation in the degree of difficulty for particular input
- Source [23]: text found — In one program the failure (when it occurred) produced a
- Source [24]: text found — contain incorrect FOL formalizations (i.e., ground truth labels)
- Source [25]: text found — we propose a novel evaluation protocol explicitly designed to distinguish genuine semantic-level log
- Source [26]: text found — The two judges disagree by 26 to 37 pp on elab-feedback outputs (vs. 7 pp on Vanilla)
- Source [27]: text found — We observe a closer alignment between BertScore and LLM judgement, proving the importance of semanti
- Source [28]: text found — For translating logic expressions with more than 20 operators, none exceeded 50% accuracy in maintai
- Source [28]: text found — LLMs cannot serve as accurate verifiers of logical equivalence
- Source [28]: text found — for anything but toy expressions (low descriptional complexity), after which
- Source [29]: text found — the criterion agrees with human majority on 87/97 cases
- Source [30]: text found — It generates models from three model families, runs each on the stated problem and on instances with
- Source [30]: text found — raises candidate-level admission precision to 0.927, against 0.871 for majority vote over the host's
- Source [31]: text found — A Boolean comparison requires a shared input vocabulary, but different formalizations rarely share t
- Source [31]: text found — We therefore use the consistency study only to select among candidate models and treat matching corr
- Source [32]: text found — Multi-sample consensus uses one formalizer; cross-model consensus is supported but not yet evaluated
- Source [33]: text found — ARc cross-checks per-query translations across diverse models using a notion of symbolic equivalence
- Source [33]: text found — soundness rises from 98.4% to 99.4% and FPR drops from 4.8% to 1.8%, at the cost of reduced recall (
- Source [33]: text found — the confidence score of a premise-conclusion pair
- Source [34]: text found — This extends self-consistency [60] to formal specifications, where equivalence can be checked exactl
- Source [34]: text found — tiers are defined post hoc by the number of atomic propositions in the reference formula
- Source [34]: text found — Error-detection AUROC by scoring channel, grouped by information source.
- Source [35]: text found — We generate K logical translations per input using a frontier LLM and cluster them by semantic equiv
- Source [36]: text found — We solve this by finding the binding that gives the highest LE score via greedy search and filling t
- Source [37]: text found — predicates are mapped to ground truth predicates using the normalized Levenshtein distance (threshol
- Source [37]: text found — this approach either requires static signatures ensuring that the same predicates are used in both e
- Source [38]: text found — We select output programs from a generated candidate set by marginalizing over program implementatio
- Source [39]: text found — considers both the consistency of the outputs against the generated test cases and the agreement of 
- Source [40]: text found — Self-consistency leverages the intuition that a complex reasoning problem typically admits multiple 
- Source [41]: text found — Our method is unsupervised, uses only a single model, and requires no modifications to off-the-shelf
- Source [42]: text found — proposing entropy-based uncertainty estimators for LLMs to detect a subset of hallucinations
- Source [43]: text found — exhibits less intra-model bias due to its composition of disjoint model families, and does so while 
- Source [44]: text found — we propose a parser-independent error detection model for text-to-SQL semantic parsing
- Source [45]: text found — we propose using cross-consistency across different LLMs rather than self-consistency within a parti
- Source [46]: text found — large-scale model sampling to explore the search space, followed by filtering based on program behav
- Source [47]: text found — Coincident Failure Diveristy (CFD)
- Source [48]: text found — we find that the 9 judges effectively provide only about 2 independent votes
- Source [49]: text found — Across all tasks and frontier models we measure, the longer models spend reasoning and taking action
- Source [49]: text found — as more capable AIs pursue harder tasks, requiring more sequential action and thought, our results p
- Source [50]: text found — average pairwise error correlation rho, cannot identify beta: error laws with identical marginals an
- Source [50]: text found — locating co-failure in answer format rather than subject
- Source [51]: text found — shared errors create a positive asymptotic error floor for majority voting
- Source [52]: text found — aggregation fails to provide a robust truth signal because language model errors are strongly correl
- Source [53]: text found — Self-consistency gives accurate per-question uncertainty but no detectable cross-question structure;
- Source [54]: text found — This indicates that harder problems elicited more heterogeneous erroneous outputs
- Source [55]: text found — a quantitative analysis for measuring whether two decision making systems systematically make errors
- Source [56]: text found — Cross-model unanimity found these errors automatically
- Source [57]: text found — epistemically and formally grounded ensemble (EFG) of LLM judges
- Source [58]: text found — stochastic variation across independent formalizations is a signal of ambiguity
- Source [59]: text found — increased generative-process diversity is associated with reduced correlated failure in model pairs
- Source [60]: text found — faulty but identical results (due to missing logic) may outvote correct results
- Source [60]: text found — For cases in which missing logic is the cause of incorrect software operation, error symptoms
- Source [60]: text found — These voting processes will be called "inexact voting".
- Source [61]: text found — On MMLU, CMP achieves a mean AUROC of 0.75 against a within-model entropy baseline of 0.59.
- Source [62]: text found — ablation shows that strengthening base learners increases error correlation while reducing disagreem
- Source [63]: text found — Sixteen language models drawn from ten families produced, on average, the semantic diversity of 1.69

## Follow-up Questions

- Report precision@coverage by number of agreeing families (k = 2..9) alongside AUROC, so the NL->FOL results are directly comparable to NoTB's 85.3/87/94.7% curve and ADMITOR's admission precision.
- Does the identical-wrong (peer-endorsement) rate fall with the number of logical conditions while the both-wrong rate rises, as Eckhardt-Lee predicts for coincident failures, and does this hold per error type (polarity vs dropped-condition vs structural)?
- Does the consensus-vs-judge ranking survive a label protocol that does not use z3 or the vocabulary aligner (aligner-free and human-intent labels), given that GenV's metric-vs-judge ranking reverses between Z3-reference and panel-intent targets?

---
*Generated by AI Inventor Pipeline*
