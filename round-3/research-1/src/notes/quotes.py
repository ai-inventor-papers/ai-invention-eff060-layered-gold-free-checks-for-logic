"""Quote ledger: every load-bearing quote used in research_report.md, checked
verbatim (whitespace-normalised) against the text fetched on 2026-09-24.

Run:  python3 notes/quotes.py   -> writes notes/QUOTES.md and notes/quotes.json
Fetched texts live in notes/full/*.md and notes/raw/*.txt (not published; see README).
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
FULL, RAW = HERE / "full", HERE / "raw"

# (qid, source index in research_out.json, file, url, version/venue, locator, quote)
Q = [
    # --- NoTB [1]
    ("Q1a", 1, "full/notb.md", "https://arxiv.org/html/2608.21962v1", "arXiv v1 (22 Aug 2026), MLCAD 2026", "Abstract",
     "On 78 CVDP RTL-generation tasks, four-family formal consensus achieves 94.7% precision at 27% coverage; three-family consensus achieves 87% precision at 33% coverage."),
    ("Q1b", 1, "full/notb.md", "https://arxiv.org/html/2608.21962v1", "v1", "Sec 4.3.1",
     "raises precision to 85.3% and 87%, respectively"),
    ("Q1c", 1, "full/notb.md", "https://arxiv.org/html/2608.21962v1", "v1", "Sec 3.2",
     "Tool errors, interface mismatches, and inconclusive results do not contribute equivalence edges."),
    ("Q1d", 1, "full/notb.md", "https://arxiv.org/html/2608.21962v1", "v1", "Sec 3.2",
     "NoTB infers clock and reset signals from port names such as clk, reset, and rst_n."),
    ("Q1e", 1, "full/notb.md", "https://arxiv.org/html/2608.21962v1", "v1", "Sec 4.3.4",
     "Generating 20 implementations per specification across four model families costs $14.93 over the full dataset."),
    ("Q1f", 1, "full/notb.md", "https://arxiv.org/html/2608.21962v1", "v1", "Sec 4.3.4",
     "the LLM-as-a-judge baseline requires 1,556 additional model calls in our evaluation."),
    ("Q1g", 1, "full/notb.md", "https://arxiv.org/html/2608.21962v1", "v1", "Sec 3.4",
     "Hence, NoTB is a selective-prediction method, not a universal correctness classifier."),
    ("Q1h", 1, "full/notb.md", "https://arxiv.org/html/2608.21962v1", "v1", "Sec 1",
     "false-acceptance rates vary by up to 45% across generating models despite similar ground-truth pass rates"),
    ("Q1i", 1, "full/notb.md", "https://arxiv.org/html/2608.21962v1", "v1", "Sec 4.3.2",
     "high-precision triage remains possible in every leave-one-out setting"),
    # --- LLMs as a Jury [2]
    ("Q2a", 2, "full/jury.md", "https://arxiv.org/html/2607.10139", "arXiv v3 (17 Aug 2026)", "Sec 1",
     "wrong answers scatter while the correct one accumulates agreement"),
    ("Q2b", 2, "full/jury.md", "https://arxiv.org/html/2607.10139", "v3", "Sec 3.2",
     "the probability that, when a model is wrong, it produces the single attractor wrong answer that other erring models also tend to produce."),
    ("Q2c", 2, "full/jury.md", "https://arxiv.org/html/2607.10139", "v3", "Sec 3.2 Generative model",
     "This is the minimal model that couples the two forces governing agreement: a shared difficulty that correlates errors, and a shared attractor that makes some errors agree."),
    ("Q2d", 2, "full/jury.md", "https://arxiv.org/html/2607.10139", "v3", "Fig 2 caption",
     "where many-option multiple choice forces wrong answers to collide"),
    ("Q2e", 2, "full/jury.md", "https://arxiv.org/html/2607.10139", "v3", "App D",
     "Two of the six are not genuine errors but grading artifacts where the unanimous answer is correct in a different surface form"),
    ("Q2f", 2, "full/jury.md", "https://arxiv.org/html/2607.10139", "v3", "Sec 5.3 On cost",
     "Because disagreement concentrates on the hard problems, this recovers the full-panel accuracy at close to two-model cost"),
    ("Q2g", 2, "full/jury.md", "https://arxiv.org/html/2607.10139", "v3", "Table 8 caption",
     "while distinct models decorrelate them, most so across families"),
    ("Q2h", 2, "full/jury.md", "https://arxiv.org/html/2607.10139", "v3", "Sec 6",
     "a panel of three to four cross-family models, with the majority verdict as the answer and the agreement fraction as a calibrated abstention signal"),
    # --- GenV [3]
    ("Q3a", 3, "full/genv.md", "https://arxiv.org/html/2609.11085", "arXiv v2 (11 Sep 2026)", "Abstract",
     "we introduce Generative Verification (GenV), which distills an offline Z3-equivalence oracle into a reference-free, continuous reference-equivalence score"),
    ("Q3b", 3, "full/genv.md", "https://arxiv.org/html/2609.11085", "v2", "Sec 5 RQ1",
     "On the combined benchmark of 950 rows containing 260 VPUs, GenV+HN achieves 0.961 AUROC."),
    ("Q3c", 3, "full/genv.md", "https://arxiv.org/html/2609.11085", "v2", "Sec 5 RQ2",
     "achieving 0.964 on ProverQA, 0.925 on MALLS, 0.915 on ProntoQA, 0.842 on ProofWriter, 0.830 on FOLIO, and 0.642 on LogicNLI"),
    ("Q3d", 3, "full/genv.md", "https://arxiv.org/html/2609.11085", "v2", "App B, three-model panel",
     "indicating that much of the disagreement with the Z3 oracle is systematic and repeatable across model judges"),
    ("Q3e", 3, "full/genv.md", "https://arxiv.org/html/2609.11085", "v2", "Limitations",
     "GenV+HN optimizes for strict reference-equivalence under the Z3 oracle rather than subjective human intent"),
    ("Q3f", 3, "full/genv.md", "https://arxiv.org/html/2609.11085", "v2", "Computational Budget",
     "Training the GenV models via Low-Rank Adaptation (LoRA) required approximately 12 GPU hours on a single NVIDIA H100-80GB GPU."),
    # --- Li et al. 2024 [4]
    ("Q4a", 4, "full/li2024.md", "https://arxiv.org/html/2410.20936", "arXiv v2, NeurIPS 2024", "Sec 5 Model",
     "we employ few-shot prompting, and set the temperature of the generation process to"),
    ("Q4b", 4, "full/li2024.md", "https://arxiv.org/html/2410.20936", "v2", "Sec 5 Metric",
     "the MATH dataset does not contain aligned formal statements, we manually check each formalization result."),
    ("Q4c", 4, "full/li2024.md", "https://arxiv.org/html/2410.20936", "v2", "Sec 1",
     "The relative efficiency of our method, ranging from 8.4% to 21.9%"),
    # --- GoFU [5]
    ("Q5a", 5, "full/gofu.md", "https://arxiv.org/html/2505.20047", "arXiv v1; NeurIPS 2025 (proceedings)", "Sec 1 contributions",
     "enables selective verification to cut error rates by 14-100% with minimal abstention"),
    ("Q5b", 5, "full/gofu.md", "https://arxiv.org/html/2505.20047", "v1", "Sec 1",
     "SMT-based autoformalization significantly boosted accuracy on tasks like ProofWriter (+34.8%) but harmed others like FOLIO (-44.5%)"),
    # --- SAC3 [6]
    ("Q6a", 6, "full/sac3_html.md", "https://arxiv.org/html/2311.01740v2", "arXiv v2; EMNLP 2023 (arXiv comment)", "Sec 1",
     "achieves a high AUROC score of 99.4% and 97.0% respectively, which significantly outperforms the self-consistency baseline"),
    # --- FormalAlign [7]
    ("Q7a", 7, "full/formalalign.md", "https://arxiv.org/abs/2410.10135", "arXiv v1; ICLR 2025 (OpenReview PDF header)", "Abstract",
     "employing a dual loss that combines a pair of mutually enhancing autoformalization and alignment tasks"),
    # --- Roundtrip [8]
    ("Q8a", 8, "full/roundtrip.md", "https://arxiv.org/abs/2604.25031", "arXiv v3 (21 Sep 2026)", "Abstract",
     "We propose a roundtrip verification approach which does not require ground-truth annotations"),
    ("Q8b", 8, "full/roundtrip.md", "https://arxiv.org/abs/2604.25031", "v3", "Abstract",
     "rules that fail the equivalence check show 1.4x-2.5x more natural language inference (NLI) drift than rules that pass it"),
    # --- CLOVER (Ryu) [9]
    ("Q9a", 9, "full/clover_ryu.md", "https://arxiv.org/html/2410.08047v2", "arXiv v2; ICLR 2025 camera-ready", "Sec 3.3 Logical Consistency",
     "An LLM might also make mistake in intermediate steps of compositional first-order logic translation and generate incorrect formulas, but these are less likely to be logically equivalent."),
    ("Q9b", 9, "full/clover_ryu.md", "https://arxiv.org/html/2410.08047v2", "v2", "Sec 3.3 Logical Consistency",
     "However, we observe that an LLM sometimes makes consistent mistakes in the last step of compositional first-order logic translation, which leads to logically equivalent incorrect formulas."),
    # --- Clover (Sun) [10]
    ("Q10a", 10, "full/clover.md", "https://arxiv.org/abs/2310.17807", "arXiv v4", "Abstract",
     "Clover performs consistency checks among code, docstrings, and formal annotations."),
    # --- Proxy-judge [11]
    ("Q11a", 11, "full/proxyjudge.md", "https://arxiv.org/html/2606.09449", "arXiv v1 (8 Jun 2026)", "Abstract",
     "We introduce a reference-free proxy-judge framework for AF that replaces gold-standard matching with a vector of per-axis property checks."),
    # --- Monotonic [12]
    ("Q12a", 12, "full/monotonic.md", "https://arxiv.org/abs/2601.23166", "arXiv v2 (7 May 2026)", "Abstract",
     "leverages complementary feedback from theorem provers and LLM-based judges, without access to ground-truth or existing formalizations"),
    # --- 2608.05670 [13]
    ("Q13a", 13, "full/consensus_correct.md", "https://arxiv.org/html/2608.05670", "arXiv v1 (6 Aug 2026)", "Sec 1 contributions",
     "it certifies correctness only above a threshold set by how diffuse the model"),
    ("Q13b", 13, "full/consensus_correct.md", "https://arxiv.org/html/2608.05670", "v1", "Sec 1",
     "nor novelty for the concentration-versus-correctness distinction itself, which the self-consistency literature states."),
    ("Q13c", 13, "full/consensus_correct.md", "https://arxiv.org/html/2608.05670", "v1", "Sec 4, after Prop. 5",
     "dispersion spread over many wrong answers cannot produce a confidently wrong consensus"),
    # --- Kim et al. [14]
    ("Q14a", 14, "full/kim2025.md", "https://arxiv.org/html/2506.07962", "arXiv v1; ICML 2025", "Abstract",
     "on one leaderboard dataset, models agree 60% of the time when both models err."),
    ("Q14b", 14, "full/kim2025.md", "https://arxiv.org/html/2506.07962", "v1", "Sec 1",
     "Importantly, even after conditioning on these factors, pairs of models that are more accurate individually also have more correlated errors."),
    ("Q14c", 14, "full/kim2025.md", "https://arxiv.org/html/2506.07962", "v1", "Sec 1",
     "judges overinflate the accuracy of models that are less accurate than it"),
    # --- Wavering Oracles [15]
    ("Q15a", 15, "full/wavering.md", "https://arxiv.org/html/2609.11428", "arXiv v1 (10 Sep 2026)", "Sec 5 (ensemble)",
     "The published models have 70.5 percent mean exact answer agreement and 0.285 mean pairwise error correlation."),
    ("Q15b", 15, "full/wavering.md", "https://arxiv.org/html/2609.11428", "v1", "Sec 4 data",
     "SycoBench-600 contains 600 English four option questions"),
    # --- Ding 2607.08065 [16]
    ("Q16a", 16, "full/x2607_08065.md", "https://arxiv.org/abs/2607.08065", "arXiv v2 (28 Jul 2026)", "Abstract",
     "agreement is a positive but weak predictor (rho 0.20-0.59, all positive under item-clustered resampling)"),
    ("Q16b", 16, "full/x2607_08065.md", "https://arxiv.org/abs/2607.08065", "v2", "Abstract",
     "with confident errors recurring across providers above a marginal-preserving null"),
    # --- 2608.18795 [17]
    ("Q17a", 17, "full/x2608_18795.md", "https://arxiv.org/abs/2608.18795", "arXiv v2 (31 Aug 2026)", "Abstract",
     "coverage phi (the mechanical/empirical ratio) shows a benchmark-associated direction: 0.81-0.93 on multiple-choice GPQA-Diamond against 0.59-0.78 on open-domain AIME"),
    ("Q17b", 17, "full/x2608_18795.md", "https://arxiv.org/abs/2608.18795", "v2", "Abstract",
     "Agreement is graded evidence, not certification."),
    # --- N-version agents [18]
    ("Q18a", 18, "full/ronnver.md", "https://arxiv.org/html/2606.20158", "arXiv v1 (18 Jun 2026)", "Sec 1",
     "the experiment produces 429 coincident-failure cases where the random independence model predicts only 115.36"),
    ("Q18b", 18, "full/ronnver.md", "https://arxiv.org/html/2606.20158", "v1", "Fig 7 caption",
     "Failures overwhelmingly concentrate in LICs 9 and 14"),
    # --- SHADOWBENCH [19]
    ("Q19a", 19, "full/shadowbench.md", "https://arxiv.org/abs/2608.29270", "arXiv v3; EMNLP 2026", "Abstract",
     "that characterize the intended statement"),
    # --- Knight & Leveson [20]
    ("Q20a", 20, "raw/kl_mit.txt", "https://dspace.mit.edu/server/api/core/bitstreams/1331578f-65c1-4665-a0be-1bc3cdc001d5/content", "IEEE TSE 12(1):96-109, 1986 (author PDF)", "Sec 1",
     "incorrect output given the same input) is very low for independently developed software"),
    ("Q20b", 20, "raw/kl_mit2.txt", "https://dspace.mit.edu/server/api/core/bitstreams/1331578f-65c1-4665-a0be-1bc3cdc001d5/content", "1986", "Sec 4",
     "Table 2 shows the number of test cases in which more than one version failed on the same input."),
    ("Q20c", 20, "raw/kl_mit.txt", "https://dspace.mit.edu/server/api/core/bitstreams/1331578f-65c1-4665-a0be-1bc3cdc001d5/content", "1986", "Sec 5",
     "which more than one version failed was 1255"),
    ("Q20d", 20, "raw/kl_mit.txt", "https://dspace.mit.edu/server/api/core/bitstreams/1331578f-65c1-4665-a0be-1bc3cdc001d5/content", "1986", "Sec 3",
     "executed, each program produces a 15 by 15 Boolean array, a 15 element Boolean"),
    # --- Eckhardt & Lee [21]
    ("Q21a", 21, "full/el1985_acm.md", "https://dl.acm.org/doi/10.1109/TSE.1985.231895", "IEEE TSE 11(12):1511-1517, 1985 (abstract only)", "Abstract",
     "An intensity function, called the intensity of coincident errors, has"),
    # --- Littlewood & Miller [22]
    ("Q22a", 22, "full/lm1989_ntrs.md", "https://ntrs.nasa.gov/citations/19900036555", "IEEE TSE 15(12):1596-1614, 1989 (abstract only)", "Abstract",
     "The use of diverse methodologies is shown to decrease the probability of the simultaneous failure of several"),
    # --- Bishop review [23]
    ("Q23a", 23, "raw/adelard.txt", "https://www.adelard.com/media/vfngprxq/divchap.pdf", "Bishop, shortened chapter of Lyu (ed.) Software Fault Tolerance, Wiley 1995", "Sec 2",
     "dissimilar faults do not guarantee dissimilar failures"),
    ("Q23b", 23, "raw/adelard.txt", "https://www.adelard.com/media/vfngprxq/divchap.pdf", "1995", "Sec 4",
     "any variation in the degree of difficulty for particular input"),
    ("Q23c", 23, "raw/adelard.txt", "https://www.adelard.com/media/vfngprxq/divchap.pdf", "1995", "Sec 2",
     "In one program the failure (when it occurred) produced a"),
    # --- Fixing FOLIO and MALLS [24]
    ("Q24a", 24, "full/gold2606.md", "https://arxiv.org/abs/2606.02837", "arXiv v2 (3 Sep 2026), accepted EMNLP 2026", "Abstract",
     "contain incorrect FOL formalizations (i.e., ground truth labels)"),
    ("Q24b", 24, "full/gold2606v1.md", "https://arxiv.org/abs/2606.02837v1", "arXiv v1 (1 Jun 2026)", "Abstract",
     "finding that approximately 39% and 36% of entries, respectively, contain incorrect FOL formalizations"),
    # --- Signal-coverage matrix [26]
    ("Q26a", 26, "full/scm.md", "https://arxiv.org/abs/2606.28013", "arXiv v1 (26 Jun 2026)", "Abstract",
     "The two judges disagree by 26 to 37 pp on elab-feedback outputs (vs. 7 pp on Vanilla)"),
    # --- Thatikonda 2501.08613 [27]
    ("Q27a", 27, "full/fol2501.md", "https://arxiv.org/abs/2501.08613", "arXiv v3; EMNLP 2025 (arXiv comment)", "Abstract",
     "We observe a closer alignment between BertScore and LLM judgement, proving the importance of semantic evaluation."),
    # --- Karia et al. [28]
    ("Q28a", 28, "full/karia.md", "https://arxiv.org/html/2410.08437", "arXiv v3; ICLR 2025", "Sec 4",
     "For translating logic expressions with more than 20 operators, none exceeded 50% accuracy in maintaining truth."),
    ("Q28b", 28, "full/karia.md", "https://arxiv.org/html/2410.08437", "v3", "Sec 4",
     "LLMs cannot serve as accurate verifiers of logical equivalence"),
    # --- Beyond Compilation [29]
    ("Q29a", 29, "full/beyondcomp.md", "https://arxiv.org/html/2606.31002", "arXiv v2 (3 Sep 2026)", "Sec 1",
     "the criterion agrees with human majority on 87/97 cases"),
    ("Q29b", 29, "full/abs_2606.31002.md", "https://arxiv.org/abs/2606.31002", "v2", "Abstract",
     "LLM judging is therefore useful as a human-calibrated, conservative aggregate measure, not as an equivalence oracle."),
    # --- ADMITOR [30]
    ("Q30a", 30, "full/abs_2608.15565.md", "https://arxiv.org/abs/2608.15565", "arXiv v4 (16 Sep 2026)", "Abstract",
     "It generates models from three model families, runs each on the stated problem and on instances with resampled parameters"),
    ("Q30b", 30, "full/abs_2608.15565.md", "https://arxiv.org/abs/2608.15565", "v4", "Abstract",
     "raises candidate-level admission precision to 0.927, against 0.871 for majority vote over the host's own samples and 0.726 for execution success"),
    # --- Vernie & Grabmair [31]
    ("Q31a", 31, "full/abs_2605.25186.md", "https://arxiv.org/abs/2605.25186", "arXiv v2; EMNLP 2026", "Abstract",
     "We find that behavioral divergence between formalizations is essentially uncorrelated with their structural agreement"),
    ("Q31b", 31, "full/vernie.md", "https://arxiv.org/html/2605.25186", "v2", "Sec 4.3.2",
     "A Boolean comparison requires a shared input vocabulary, but different formalizations rarely share the same leaf nodes"),
    ("Q31c", 31, "full/vernie.md", "https://arxiv.org/html/2605.25186", "v2", "Sec 4.2.1",
     "We therefore use the consistency study only to select among candidate models and treat matching correctness as an open limitation."),
    # --- VERGE [32]
    ("Q32a", 32, "raw/verge_bridges.txt", "https://arxiv.org/html/2601.20055", "arXiv v2 (2 May 2026)", "App E.4 'Bridges and cross-model consensus'",
     "Multi-sample consensus uses one formalizer; cross-model consensus is supported but not yet evaluated."),
    # --- ARc [33]
    ("Q33a", 33, "raw/arc_rq2.txt", "https://arxiv.org/html/2511.09008", "arXiv v2 (13 Jul 2026)", "Sec 2",
     "ARc cross-checks per-query translations across diverse models using a notion of symbolic equivalence, with confidence thresholds indicating semantic agreement."),
    ("Q33b", 33, "raw/arc_rq2.txt", "https://arxiv.org/html/2511.09008", "v2", "Sec 5 RQ2",
     "soundness rises from 98.4% to 99.4% and FPR drops from 4.8% to 1.8%, at the cost of reduced recall (28.0% to 14.9%)."),
    # --- SCP-NL2TL [34]
    ("Q34a", 34, "full/abs_2608.05439.md", "https://arxiv.org/abs/2608.05439", "arXiv v1 (5 Aug 2026)", "Abstract",
     "the dispersion of repeated translations under exact semantic equivalence"),
    ("Q34b", 34, "full/scpnl2tl.md", "https://arxiv.org/html/2608.05439", "v1", "Sec 3",
     "This extends self-consistency [60] to formal specifications, where equivalence can be checked exactly [35]."),
    # --- SCD [35]
    ("Q35a", 35, "full/scd2608.md", "https://arxiv.org/abs/2608.30258", "arXiv v1 (31 Aug 2026)", "Abstract",
     "We generate K logical translations per input using a frontier LLM and cluster them by semantic equivalence"),
    # --- LogicLLaMA [36]
    ("Q36a", 36, "full/logicllama.md", "https://arxiv.org/html/2305.15541", "arXiv v1; ACL 2024 (as cited by GenV)", "Sec 4.2.3",
     "We solve this by finding the binding that gives the highest LE score via greedy search and filling the rest of the missing inputs with dummy inputs."),
    # --- Vossel [37]
    ("Q37a", 37, "full/vossel.md", "https://arxiv.org/html/2509.22338", "arXiv v2; IJCLR 2025", "Sec 3 Predicate matching",
     "predicates are mapped to ground truth predicates using the normalized Levenshtein distance (threshold 0.6)"),
    ("Q37b", 37, "full/vossel.md", "https://arxiv.org/html/2509.22338", "v2", "Sec 2",
     "this approach either requires static signatures ensuring that the same predicates are used in both expressions or a normalization step to align predicate names"),
    # --- MBR-exec [38], CodeT [39], SC [40], SE [41], Farquhar [42], PoLL [43], PET-SQL [45], AlphaCode [46]
    ("Q38a", 38, "full/mbrexec.md", "https://arxiv.org/abs/2204.11454", "arXiv v2; EMNLP 2022", "Abstract",
     "We select output programs from a generated candidate set by marginalizing over program implementations that share the same semantics."),
    ("Q39a", 39, "full/codet.md", "https://arxiv.org/abs/2207.10397", "arXiv v2", "Abstract",
     "considers both the consistency of the outputs against the generated test cases and the agreement of the outputs with other code samples"),
    ("Q40a", 40, "full/selfcons.md", "https://arxiv.org/abs/2203.11171", "arXiv v4; ICLR 2023", "Abstract",
     "Self-consistency leverages the intuition that a complex reasoning problem typically admits multiple different ways of thinking leading to its unique correct answer."),
    ("Q41a", 41, "full/sement.md", "https://arxiv.org/abs/2302.09664", "arXiv v3; ICLR 2023", "Abstract",
     "Our method is unsupervised, uses only a single model, and requires no modifications to off-the-shelf language models."),
    ("Q43a", 43, "full/poll.md", "https://arxiv.org/abs/2404.18796", "arXiv v2", "Abstract",
     "exhibits less intra-model bias due to its composition of disjoint model families, and does so while being over seven times less expensive"),
    ("Q45a", 45, "full/petsql.md", "https://arxiv.org/abs/2403.09732", "arXiv v4", "Abstract",
     "we propose using cross-consistency across different LLMs rather than self-consistency within a particular LLM"),
    ("Q46a", 46, "full/alphacode.md", "https://arxiv.org/abs/2203.07814", "arXiv v1 (Science 2022 version not fetched)", "Abstract",
     "large-scale model sampling to explore the search space, followed by filtering based on program behavior to a small set of submissions"),
    # --- Nine judges [48]
    ("Q48a", 48, "full/abs_2605.29800.md", "https://arxiv.org/abs/2605.29800", "arXiv v1 (28 May 2026)", "Abstract",
     "we find that the 9 judges effectively provide only about 2 independent votes"),
    ("Q48b", 48, "full/ninejudges.md", "https://arxiv.org/html/2605.29800", "v1", "Table (Condorcet gap decomposition)",
     "Gap explained by difficulty | 6.8%"),
    # --- Hot mess [49]
    ("Q49a", 49, "full/abs_2601.23045.md", "https://arxiv.org/abs/2601.23045", "arXiv v2; ICLR 2026", "Abstract",
     "Across all tasks and frontier models we measure, the longer models spend reasoning and taking actions,"),
    # --- Co-failure ceiling [50]
    ("Q50a", 50, "full/abs_2606.27288.md", "https://arxiv.org/abs/2606.27288", "arXiv v1 (25 Jun 2026)", "Abstract",
     "average pairwise error correlation rho, cannot identify beta: error laws with identical marginals and pairwise correlations can have different all-wrong rates"),
    # --- State-dependent [51]
    ("Q51a", 51, "full/abs_2607.23931.md", "https://arxiv.org/abs/2607.23931", "arXiv v1 (27 Jul 2026)", "Abstract",
     "shared errors create a positive asymptotic error floor for majority voting"),
    # --- Consensus is not verification [52]
    ("Q52a", 52, "full/abs_2603.06612.md", "https://arxiv.org/abs/2603.06612", "arXiv v1 (20 Feb 2026)", "Abstract",
     "aggregation fails to provide a robust truth signal because language model errors are strongly correlated"),
    # --- Stochastic sampling shallow [53]
    ("Q53a", 53, "full/abs_2607.20464.md", "https://arxiv.org/abs/2607.20464", "arXiv v1; EIML@ICML 2026", "Abstract",
     "Self-consistency gives accurate per-question uncertainty but no detectable cross-question structure; only a diverse ensemble surfaces what a model does not know."),
    # --- Java errors [54]
    ("Q54a", 54, "full/javaerr.md", "https://arxiv.org/html/2606.14113", "arXiv v1 (12 Jun 2026)", "Sec 5",
     "This indicates that harder problems elicited more heterogeneous erroneous outputs"),
    # --- Geirhos [55]
    ("Q55a", 55, "full/geirhos.md", "https://arxiv.org/abs/2006.16736", "arXiv v3; NeurIPS 2020", "Abstract",
     "a quantitative analysis for measuring whether two decision making systems systematically make errors on the same inputs"),
    # --- FormInv [56]
    ("Q56a", 56, "full/abs_2605.29001.md", "https://arxiv.org/abs/2605.29001", "arXiv v1", "Abstract",
     "Cross-model unanimity found these errors automatically"),
    # --- VERIMED [58]
    ("Q58a", 58, "full/abs_2605.13817.md", "https://arxiv.org/abs/2605.13817", "arXiv v1 (13 May 2026)", "Abstract",
     "stochastic variation across independent formalizations is a signal of ambiguity"),
    # --- generative-process diversity [59]
    ("Q59a", 59, "full/abs_2609.03422.md", "https://arxiv.org/abs/2609.03422", "arXiv v1 (3 Sep 2026)", "Abstract",
     "increased generative-process diversity is associated with reduced correlated failure in model pairs"),
    # --- EFG ensemble [57]
    ("Q57a", 57, "full/abs_2506.10903.md", "https://arxiv.org/abs/2506.10903", "arXiv v2 (21 Aug 2026)", "Abstract",
     "epistemically and formally grounded ensemble (EFG) of LLM judges"),
    # --- additions (second session, 2026-09-24 ~03:00 UTC)
    ("Q1j", 1, "full/notb.md", "https://arxiv.org/html/2608.21962v1", "v1", "Sec 4.1 Metrics",
     "We report precision (correct accepts / total accepts) and coverage (accepts / evaluable specs) at the specification level"),
    ("Q1k", 1, "full/notb.md", "https://arxiv.org/html/2608.21962v1", "v1", "Sec 4.2.1",
     "Thus, LLM-as-a-judge does not provide a stable high-confidence triage signal."),
    ("Q1l", 1, "full/notb.md", "https://arxiv.org/html/2608.21962v1", "v1", "Sec 4.3.1",
     "For each specification, we measure the model diversity of the largest equivalence cluster and analyze how this signal relates to correctness."),
    ("Q2i", 2, "full/jury.md", "https://arxiv.org/html/2607.10139", "v3", "Sec 3.2 Generative model",
     "Per problem, draw a latent difficulty"),
    ("Q2j", 2, "full/jury.md", "https://arxiv.org/html/2607.10139", "v3", "App C Multi-attractor refinement",
     "the single-attractor floor overshoots substantially"),
    ("Q2k", 2, "full/jury.md", "https://arxiv.org/html/2607.10139", "v3", "Sec 5.4",
     "Resampling one model cannot escape that model's correlated errors at any"),
    ("Q3g", 3, "full/genv.md", "https://arxiv.org/html/2609.11085", "v2", "Table 1 (a)",
     "Self-consistency vote (K=5) | 0.863"),
    ("Q3h", 3, "full/genv.md", "https://arxiv.org/html/2609.11085", "v2", "Table 4 / Table 10",
     "Z3-equivalence to reference | 0.907 | 0.654 Panel-majority intent | 0.679 | 0.778"),
    ("Q3i", 3, "full/genv.md", "https://arxiv.org/html/2609.11085", "v2", "App B, contested slice",
     "When shifting the target from strict reference-equivalence to panel-majority intent,"),
    ("Q3j", 3, "full/genv.md", "https://arxiv.org/html/2609.11085", "v2", "Table 1 (b)",
     "Round-trip back-translationrf{}^{\\text{rf}} | 0.578"),
    ("Q13d", 13, "full/consensus_correct.md", "https://arxiv.org/html/2608.05670", "v1", "Prop. 5 (iii)",
     "Call the errors _diffuse at level_"),
    ("Q14d", 14, "full/kim2025.md", "https://arxiv.org/html/2506.07962", "v1", "Limitations",
     "some questions may also be harder than others. Future work should consider developing a metric that is robust to these characteristics."),
    ("Q14e", 14, "full/kim2025.md", "https://arxiv.org/html/2506.07962", "v1", "Sec 1",
     "choosing between incorrect answers uniformly at random would lead to an agreement rate of"),
    ("Q15c", 15, "full/wavering.md", "https://arxiv.org/html/2609.11428", "v1", "Abstract",
     "Mean error correlation of 0.285 reduces seven models to an effective independent count of 2.58."),
    ("Q25a", 25, "full/brunello.md", "https://arxiv.org/abs/2511.11816", "arXiv v1; AAAI 2026 (arXiv comment)", "Abstract",
     "we propose a novel evaluation protocol explicitly designed to distinguish genuine semantic-level logical understanding from superficial pattern recognition, memorization, and dataset contamination"),
    ("Q33c", 33, "full/arc.md", "https://arxiv.org/html/2511.09008", "v2", "Sec 3.2",
     "the confidence score of a premise-conclusion pair"),
    ("Q33d", 33, "full/arc.md", "https://arxiv.org/html/2511.09008", "v2", "Sec 3.2",
     "is the proportion of the"),
    ("Q33e", 33, "full/arc.md", "https://arxiv.org/html/2511.09008", "v2", "Sec 3",
     "autoformalizes the statement under validation into logic formulas (over the policy model schema)"),
    ("Q42a", 42, "full/farquhar.md", "https://www.nature.com/articles/s41586-024-07421-0", "Nature 630, 2024", "Abstract",
     "proposing entropy-based uncertainty estimators for LLMs to detect a subset of hallucinations"),
    ("Q44a", 44, "full/chen_sql.md", "https://aclanthology.org/2023.findings-emnlp.785/", "Findings of EMNLP 2023", "Abstract",
     "we propose a parser-independent error detection model for text-to-SQL semantic parsing"),
    ("Q47a", 47, "full/kuncheva.md", "https://lucykuncheva.co.uk/ensemble_diversity.html", "Machine Learning 51, 2003 (listed on author page)", "Diversity toolbox list",
     "Coincident Failure Diveristy (CFD)"),
    ("Q49b", 49, "full/abs_2601.23045.md", "https://arxiv.org/abs/2601.23045", "v2", "Abstract",
     "as more capable AIs pursue harder tasks, requiring more sequential action and thought, our results predict failures to be accompanied by more incoherent behavior"),
    ("Q50b", 50, "full/abs_2606.27288.md", "https://arxiv.org/abs/2606.27288", "v1", "Abstract",
     "locating co-failure in answer format rather than subject"),
    ("Q60a", 60, "full/zorzo_nvp.md", "https://www.inf.pucrs.br/~zorzo/cs/n-versionprogramming.pdf", "FTCS-8 1978, pp. 3-9 (reprint in FTCS-25, 1995)", "Sec 5 (experiments)",
     "faulty but identical results (due to missing logic) may outvote correct results"),
    ("Q60b", 60, "full/zorzo_nvp.md", "https://www.inf.pucrs.br/~zorzo/cs/n-versionprogramming.pdf", "1978", "Sec 5",
     "For cases in which missing logic is the cause of incorrect software operation, error symptoms"),
    ("Q60c", 60, "full/zorzo_nvp.md", "https://www.inf.pucrs.br/~zorzo/cs/n-versionprogramming.pdf", "1978", "Sec 3",
     "These voting processes will be called \"inexact voting\"."),
    ("Q61a", 61, "full/xdis2603.md", "https://arxiv.org/abs/2603.25450", "arXiv v2 (11 Jun 2026)", "Abstract",
     "On MMLU, CMP achieves a mean AUROC of 0.75 against a within-model entropy baseline of 0.59."),
    ("Q62a", 62, "full/abs_2607.19899.md", "https://arxiv.org/abs/2607.19899", "arXiv v1; PAAMS 2026 (arXiv comment)", "Abstract",
     "ablation shows that strengthening base learners increases error correlation while reducing disagreement"),
    ("Q28c", 28, "full/karia.md", "https://arxiv.org/html/2410.08437", "v3", "Sec 4",
     "for anything but toy expressions (low descriptional complexity), after which"),
    ("Q8c", 8, "full/roundtrip_html.md", "https://arxiv.org/html/2604.25031", "v3", "Sec 1",
     "We use two LLMs, Claude Opus 4.6 (Anthropic) and GPT-5.2 (OpenAI)."),
    ("Q4d", 4, "full/li2024.md", "https://arxiv.org/html/2410.20936", "v2", "Sec 1 / Fig 1 caption",
     "scores and selects the best result from k autoformalization candidates based on two complementary self-consistency methods"),
    ("Q34c", 34, "full/scpnl2tl.md", "https://arxiv.org/html/2608.05439", "v1", "Sec 4 Tasks and data",
     "tiers are defined post hoc by the number of atomic propositions in the reference formula"),
    ("Q34d", 34, "full/scpnl2tl.md", "https://arxiv.org/html/2608.05439", "v1", "Table 1 caption",
     "Error-detection AUROC by scoring channel, grouped by information source."),
    ("Q34e", 34, "full/scpnl2tl.md", "https://arxiv.org/html/2608.05439", "v1", "Sec 4 Tasks and data",
     "Translation correctness is determined using the benchmark-provided canonical equivalence checker"),
    ("Q34f", 34, "full/scpnl2tl.md", "https://arxiv.org/html/2608.05439", "v1", "Sec 4 LLM Translators",
     "Two translators spanning a wide reliability range are evaluated."),
    ("Q63a", 63, "full/abs_2608.00285.md", "https://arxiv.org/abs/2608.00285", "arXiv (31 Jul 2026)", "Abstract",
     "Sixteen language models drawn from ten families produced, on average, the semantic diversity of 1.69 distinct formulations"),
]


def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip()


def main() -> None:
    rows, bad = [], []
    for qid, src, f, url, ver, loc, quote in Q:
        p = HERE / f
        ok = p.exists() and norm(quote) in norm(p.read_text(encoding="utf-8", errors="ignore"))
        rows.append(dict(qid=qid, source_index=src, file=f"notes/{f}", url=url, version=ver, locator=loc, quote=quote, verified_in_fetched_text=ok))
        if not ok:
            bad.append(qid)
    (HERE / "quotes.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    md = ["# Quote ledger (verbatim, whitespace-normalised check against the fetched text of 2026-09-24)\n",
          "| id | src | version / venue | locator | quote | in fetched text |", "|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['qid']} | [{r['source_index']}] | {r['version']} | {r['locator']} | \"{r['quote'].replace('|', '/')}\" ([link]({r['url']})) | {'yes' if r['verified_in_fetched_text'] else 'NO'} |")
    (HERE / "QUOTES.md").write_text("\n".join(md) + "\n")
    print(f"{len(rows)} quotes, {len(bad)} not found: {bad}")


if __name__ == "__main__":
    main()
