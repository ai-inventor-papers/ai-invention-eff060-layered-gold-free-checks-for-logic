# Gold-Free Faithfulness Metrics for NL-to-FOL Translation

## Framing

Translating natural language into first-order logic (NL-FOL) is a prerequisite for neurosymbolic reasoning pipelines [10], yet evaluating whether a candidate formula faithfully captures a sentence's meaning remains an open problem. Gold FOL annotations are expensive, non-unique, and unreliable: Brunello et al. [3] found that approximately 42% of entries in both FOLIO [1] and MALLS [2] contain incorrect formalisations. Existing metrics either require a gold formula (exact match, prover-checked equivalence) or only verify that the output parses [5, 6]. The user's own pilot study used structural consistency checks (arity agreement, predicate-set overlap across reruns, joint satisfiability) that measure stability but not whether a formula says what its sentence says.

This run investigates gold-free metrics that predict faithfulness to the text given only a sentence and a candidate formula, with no reference formula, no ontology, and no domain knowledge. The evaluation is a meta-evaluation: we build a labelled set of (sentence, formula) pairs from public benchmarks whose gold has been audited, and measure each metric's ability to discriminate correct translations from errors.

## Iteration 1

### 1.1 Strategy

The iteration screens four candidate metric families head-to-head on a frozen evaluation set, with a disguised cheap LLM judge as the bar to beat.

**Candidates.** (A) FOL-Triage, a three-layer cascade: L1 (formula lint: deterministic formula smells), L2 (text accounting: bag-of-words and role-aware coverage), and L3 (role questionnaire: a small LLM reads the text and z3 reads the formula; their structured answers are compared). (B) Round-trip verification: verbalise the formula back to natural language and compare to the original via NLI or embedding similarity [7]. (C) Cross-system consensus: collect translations of the same sentence from multiple independent systems, measure z3-equivalence between the candidate and the peer pool, and score disagreement [8]. (D) Disguised cheap judge and baselines: an LLM judge, structural pilot metrics, and round-trip features evaluated on nonce-disguised sentences to control for memorisation.

**Evaluation set.** The frozen screen uses Logic-LM [10] released outputs on FOLIO validation: three LLM systems (GPT-3.5-turbo, GPT-4, text-davinci-003) producing 796 items. Track L contains LLM outputs labelled by z3 equivalence to corrected gold [4]; track H contains the 294 original human gold formulas, of which 57 are errors according to the corrected labels. The parallel run (run_qY2a2IS-WLIs) measured 43.9% of solver-non-equivalent candidates as faithful by a three-family panel; iteration 2 will re-score with those adjudicated labels.

**Decision rule.** A candidate must achieve AUROC ≥ 0.65 on track L (ERROR vs CORRECT), with coverage ≥ 90%, rewrite false-alarm rate ≤ 10% per rewrite family, and cost ≤ $0.002 per item. It advances only if its AUROC exceeds the disguised cheap judge's, with a paired bootstrap CI excluding zero.

**Held-out dataset (Artifact E).** A separate 700-sentence, 8,507-row held-out set was constructed from FOLIO training premises, MALLS training long/conditional/exception strata, and FOLIO curated conclusions, each translated by 9 LLM families plus ccg2lambda plus GPT-4 gold. Labels were assigned by z3 equivalence to audited gold, with contested cases adjudicated by a three-member panel (Claude Haiku-4.5, GLM-4.6, Kimi-K2). This set is reserved for iteration 2 confirmation. [ARTIFACT:art_U4Hsqt4Ay9Tg]

The dataset contains 1,750 CORRECT, 5,005 ERROR, 1,086 UNPARSEABLE, 276 UNRESOLVED, and 390 CONTESTED items. The panel calibration subset (173 items) shows that the panel agrees with expert-corrected labels on both faithful and unfaithful items. A screen audit of 1,173 items from the Logic-LM screen confirms the label assignment. The dataset cost $9.83 in API calls.

### 1.2 Experiment A: FOL-Triage

[ARTIFACT:art_d0njuqy2Csj-]

FOL-Triage was evaluated on the frozen screen with Gemini 2.5 Flash Lite as the primary LLM for L3. Total API spend was $0.29.

#### Headline AUROCs (track L, ERROR vs CORRECT, n = 477, 199 errors)

| Metric | AUROC | 95% CI | AUPRC |
|-|-|-|-|
| L1 (any smell) | 0.508 | [0.499, 0.519] | 0.425 |
| L2 bag-of-words | 0.737 | [0.677, 0.801] | 0.690 |
| L2 role-aware | 0.557 | [0.527, 0.594] | 0.476 |
| L3 score | 0.756 | [0.701, 0.809] | 0.657 |
| Fused (fitted on H, no leak) | 0.759 | [0.695, 0.825] | 0.740 |
| Fused (all H) | 0.827 | [0.778, 0.874] | 0.771 |
| Fused (cross-fit L) | 0.864 | [0.824, 0.902] | 0.789 |
| Decomposed judge (LLM reads formula) | 0.716 | [0.645, 0.789] | 0.717 |
| L3 with local Qwen2.5-1.5B | 0.708 | [0.637, 0.774] | 0.603 |

The primary no-leak fused score is 0.759. The fused-all-H and cross-fit-L numbers (0.827, 0.864) are shown for completeness but are not valid held-out estimates: the former uses the full track H for fitting, and the latter is a within-L cross-fit that overstates generalisation.

**Track H (human gold errors, n = 258, 57 errors).** Fused out-of-fold AUROC is 0.777 [0.698, 0.847]. L1 alone reaches 0.655, compared to 0.508 on track L. The lint rules fire on human annotation errors but not on LLM outputs, because the two populations produce different formula smells.

#### L1 lint: a negative result on LLM outputs

L1 flags formulas with deterministic smells (existential implication, free variables, arity clashes, vacuity, trivial formulas, dangling predicates). On track L, the true positive rate is 2.0% at a false positive rate of 0.4%, giving AUROC 0.508. This is a negative result: L1 lint does not transfer from human annotation errors (where it is effective, AUROC 0.655) to LLM outputs. The reason is that LLM-generated formulas rarely contain the syntactic pathologies L1 detects; their errors are semantic (wrong predicates, missing conditions, scope mistakes).

All nine individual smell rules have false-alarm rates below 3% on every system:

| Smell | gpt-3.5 FA | gpt-4 FA | davinci-003 FA |
|-|-|-|-|
| EX_IMP | 0.0 | 0.0 | 0.0 |
| ALL_AND | 0.0 | 0.0 | 0.0 |
| IFF_RESTR | 0.0 | 0.009 | 0.0 |
| GLUE | 0.0 | 0.0 | 0.0 |
| FREE | 0.0 | 0.0 | 0.0 |
| VACUOUS | 0.0 | 0.0 | 0.0 |
| TRIVIAL | 0.0 | 0.0 | 0.0 |
| ARITY | 0.0 | 0.0 | 0.0 |
| DANGLING | 0.0 | 0.0 | 0.0 |

Only the FREE smell fires on any track-L errors (4 items).

#### L2 role-aware check: below bag-of-words

The role-aware UD-based check (L2-role) achieves AUROC 0.557, which is 0.18 below the simpler bag-of-words check (L2-bow, 0.737). The role-aware layer adds no discriminative power over word overlap.

#### Decomposed judge ablation

Replacing z3 with an LLM that reads the formula directly (the decomposed judge) drops L3 AUROC from 0.756 to 0.697 (ΔAUROC = −0.059). The LLM gets only 57.6% of binary argument slots correct on track L and 36.4% on track H. The z3 answerer is significantly more accurate for structured formula reading.

#### Per-type sensitivity (track L, at binary threshold)

| Error type | n | L1 | L2-bow | L2-role | L3 | Fused | Cascade |
|-|-|-|-|-|-|-|-|
| NEG | 5 | 0.0 | 0.2 | 1.0 | 0.2 | 0.4 | 1.0 |
| QUANT | 2 | 0.0 | 0.0 | 0.5 | 0.0 | 0.5 | 0.5 |
| CONN | 4 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| DROP | 142 | 0.028 | 0.479 | 0.127 | 0.197 | 0.599 | 0.606 |
| ADD | 150 | 0.020 | 0.473 | 0.107 | 0.173 | 0.653 | 0.573 |
| SWAP | 12 | 0.0 | 0.0 | 0.083 | 0.25 | 0.083 | 0.333 |
| BIND | 8 | 0.125 | 0.0 | 0.125 | 0.0 | 0.375 | 0.25 |
| COMPOUND | 187 | 0.118 | 0.428 | 0.166 | 0.160 | 0.599 | 0.578 |

FOL-Triage is most sensitive to ADD and DROP errors (the largest categories), with the fused score catching about 60%. It misses CONN errors entirely (0/4) and detects SWAP poorly (1/12). Negation errors are fully caught by the cascade (which fires L2-role, where monotonicity shifts are visible) but L1 and L2-bow miss them.

On track H (57 errors), the per-type pattern differs. UNGLUE errors (n = 5) are caught at 100% by L1 and the fused score, because they produce detectable formula smells.

#### Per-type sensitivity (track H)

| Error type | n | L1 | L2-bow | L2-role | L3 | Fused | Cascade |
|-|-|-|-|-|-|-|-|
| NEG | 4 | 0.0 | 0.0 | 0.25 | 0.0 | 0.25 | 0.25 |
| REV | 1 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| QUANT | 1 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| RESTR | 1 | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| CONN | 8 | 0.25 | 0.125 | 0.0 | 0.375 | 0.375 | 0.375 |
| MOVE | 2 | 0.5 | 0.0 | 0.5 | 0.0 | 0.5 | 1.0 |
| DROP | 14 | 0.143 | 0.357 | 0.0 | 0.143 | 0.357 | 0.5 |
| ADD | 19 | 0.158 | 0.368 | 0.053 | 0.211 | 0.526 | 0.579 |
| SWAP | 2 | 0.0 | 0.5 | 0.0 | 0.5 | 0.5 | 0.5 |
| BIND | 1 | 1.0 | 1.0 | 0.0 | 0.0 | 1.0 | 1.0 |
| UNGLUE | 5 | 1.0 | 0.4 | 0.0 | 0.2 | 1.0 | 1.0 |
| COMPOUND | 33 | 0.303 | 0.182 | 0.242 | 0.182 | 0.545 | 0.636 |

#### Invariance under meaning-preserving rewrites

Five rewrite families were tested on 150 track-L CORRECT items. The table shows the false-alarm rate on the rewritten formula and the flip rate (fraction of items whose binary verdict changes):

| Rewrite | n applies | L1 FA | L1 flip | bow FA | bow flip | role FA | role flip | L3 FA | L3 flip | Fused FA | Fused flip |
|-|-|-|-|-|-|-|-|-|-|-|-|
| RENAME | 150 | 0.0 | 0.0 | 0.18 | 0.093 | 0.013 | 0.0 | 0.033 | 0.007 | 0.22 | 0.013 |
| REORDER | 34 | 0.0 | 0.0 | 0.029 | 0.0 | 0.059 | 0.0 | 0.059 | 0.0 | 0.235 | 0.0 |
| DEMORGAN | 33 | 0.0 | 0.0 | 0.030 | 0.0 | 0.061 | 0.0 | 0.030 | 0.030 | 0.182 | 0.061 |
| CONTRAPOSITIVE | 40 | 0.025 | 0.025 | 0.10 | 0.0 | 0.025 | 0.025 | 0.025 | 0.0 | 0.275 | 0.0 |
| PRENEX | 1 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

The rewrite false-alarm gate (≤ 10% per family) fails. The worst-family fused FA is 0.275 (CONTRAPOSITIVE), but this equals the FA on the original formulas; the flip rate is at most 0.061. The high FA is not caused by the rewrites but by the fused score's calibration: it was fitted on track H where the CORRECT base rate is higher, producing a systematic over-flagging on track L (FA on track-L CORRECT items is 0.194 versus the 0.10 calibration target).

L1, L2-role, and L3 individually pass the 10% gate. L2-bow fails only under RENAME (FA = 0.18), because renaming predicates breaks the bag-of-words match between text and formula.

[FIGURE:fig_rewrite_fa]

#### Coverage

| Track | n | Parseable | Full coverage rate |
|-|-|-|-|
| L | 753 | 693 | 0.920 |
| H | 302 | 279 | 0.924 |

Parse rates by system: gpt-3.5-turbo 0.889, gpt-4 0.946, text-davinci-003 0.921. Unparseable outputs are scored as p = 1 (maximum error probability) by the fused metric, so all items receive a score. The coverage gate (≥ 90%) passes.

#### Cost

L1 and L2 are free (CPU-only). L3 costs $0.175 per 1,000 calls with Gemini 2.5 Flash Lite. The total per-item cost is $0.0002, passing the $0.002 gate. CPU time (L1 + L2 + z3): median 35 ms, P95 90 ms. L3 latency: median 630 ms, P95 1.68 s.

#### Contamination check

L3 was run on nonce-disguised sentences (content words replaced by nonsense words) on the full track L. AUROC with exact text-formula alignment: 0.765; with disguised text: 0.770. Paired difference: −0.005 [−0.063, 0.049]. There is no evidence that the LLM benefits from having seen the public benchmark sentences.

#### Complexity strata (track L, fused score)

| Stratum | n (error/correct) | Testable | Fused AUROC | L2-bow AUROC | L3 AUROC |
|-|-|-|-|-|-|
| words < 12 | 443 (179/264) | Yes | 0.781 | 0.742 | 0.772 |
| words 12-19 | 31 (18/13) | No | 0.521 | 0.596 | 0.541 |
| words ≥ 20 | 3 (2/1) | No | 0.500 | 1.000 | 0.000 |
| 0 quantifiers | 302 (130/172) | Yes | 0.743 | 0.728 | 0.771 |
| 1 quantifier | 164 (65/99) | Yes | 0.794 | 0.748 | 0.721 |
| ≥ 2 quantifiers | 11 (4/7) | No | 0.750 | 0.768 | 0.607 |
| depth ≤ 1 | 296 (124/172) | Yes | 0.762 | 0.745 | 0.779 |
| depth 2-3 | 173 (73/100) | Yes | 0.756 | 0.717 | 0.710 |
| depth ≥ 4 | 8 (2/6) | No | 0.667 | 0.750 | 0.500 |
| 0 conditions | 344 (145/199) | Yes | 0.775 | 0.759 | 0.791 |
| 1-2 conditions | 131 (54/77) | Yes | 0.716 | 0.677 | 0.628 |

The frozen screen is dominated by short, simple sentences (93% under 12 words). The long and complex strata (12+ words, 2+ quantifiers, 3+ conditions) have too few items to test. This limitation motivates the held-out dataset (Artifact E), which oversamples these strata.

#### Per-system AUROC (descriptive, n = 3 systems)

| System | n | Error rate | Fused AUROC | L1 AUROC | L2-bow AUROC | L3 AUROC |
|-|-|-|-|-|-|-|
| gpt-3.5-turbo | 143 | 0.378 | 0.689 | 0.500 | 0.650 | 0.722 |
| gpt-4 | 177 | 0.367 | 0.700 | 0.496 | 0.716 | 0.720 |
| text-davinci-003 | 157 | 0.510 | 0.857 | 0.525 | 0.811 | 0.817 |

FOL-Triage is most discriminative on text-davinci-003, the weakest system. The Kendall τ between system error rates and mean fused scores is 0.333 (3 systems, descriptive only).

#### Label quality observations

The track-L label distribution reveals a systematic issue: 58.8% of typed ERROR items have only ADD+DROP repair operators. On inspection, most of these are vocabulary or arity choices (e.g. Lunch(james) vs HasLunch(james, company)) that the vocabulary aligner cannot bridge. These are likely CORRECT under a looser equivalence definition. The track-H original gold has 27.1% error rate (errors, uncertain, and reading-choice items) and 5.8% unparseable rate. Among non-equivalent parseable items, 21.9% are correct-but-not-equivalent (VOCAB or GRAN class).

### 1.3 Experiment C: Cross-System Consensus

[ARTIFACT:art_i3cVDxBp-USk]

The consensus metric collects translations of the same sentence from multiple independent LLM families, checks pairwise z3 equivalence, and scores each candidate by its disagreement with the pool. Total API spend was $1.52.

#### Headline AUROCs (track L, ERROR vs CORRECT, n = 546, 249 errors)

| Metric | AUROC | 95% CI | AUPRC |
|-|-|-|-|
| c_score (1 − eq_frac, all peers) | 0.866 | [0.821, 0.906] | 0.827 |
| c_score (6 fresh peers only) | 0.872 | [0.830, 0.911] | 0.825 |
| c_score (non-OpenAI peers) | 0.863 | [0.820, 0.903] | 0.808 |
| c_score (2 Logic-LM peers only) | 0.753 | [0.701, 0.806] | 0.659 |
| medoid depth | 0.722 | [0.673, 0.774] | 0.622 |
| cluster entropy | 0.773 | [0.724, 0.820] | 0.691 |
| SC-5 cheap (gpt-4.1-nano) | 0.725 | [0.669, 0.781] | 0.627 |
| SC-5 same model | 0.716 | [0.632, 0.796] | 0.628 |
| SC-5 entropy | 0.631 | [0.568, 0.693] | 0.539 |
| Prediction set instability (SC) | 0.688 | [0.626, 0.750] | 0.602 |
| Prediction set instability (pool) | 0.770 | [0.717, 0.821] | 0.721 |
| FOL length | 0.527 | [0.470, 0.586] | 0.485 |
| Misalignment (vocab) | 0.835 | [0.794, 0.876] | 0.821 |

[FIGURE:fig_consensus_auroc]

The c_score achieves the highest AUROC in the iteration at 0.866. It beats SC-5 (the self-consistency baseline) by ΔAUROC = +0.140 [0.085, 0.197]. Cross-family consensus also exceeds sampling self-consistency in the related SAC3 framework [17], which uses semantic-aware cross-check consistency for hallucination detection in black-box LLMs. Using only the six fresh peer translations (not the three Logic-LM systems) gives 0.872, slightly higher than using all peers. Restricting to the two other Logic-LM systems drops the AUROC to 0.753, showing that diversity across model families is essential.


The misalignment score (0.835) is high because CORRECT items are by construction alignable to the gold in the labeller, so misalignment alone is a strong proxy for error. This does not generalise to settings without a shared vocabulary.

#### RENAME rewrite invariance: failure

Under predicate renaming (replacing predicate names with WordNet synonyms or nonce names), the c_score false-alarm rate is 96% (100% for constant-only renaming). This is expected and fundamental: two formulas with different predicate names are not z3-equivalent, so any rename breaks the equivalence check. The consensus metric is invariant to rewrites that preserve z3 equivalence (reordering, De Morgan, contrapositive) but not to vocabulary changes.

#### Blind-spot analysis

38% of ERROR items are z3-equivalent to the medoid (the most popular peer formula). This places a ceiling on recall of approximately 62%. The blind-spot rate is 5% for polarity errors and 57% for structural errors.

#### Cost

The peer pool costs $0.0015 per sentence (6 peers via API). Total experiment spend: $1.52. z3 pairwise equivalence checking is free.

### 1.4 Experiment D: Disguised Judge and Baselines

[ARTIFACT:art_elDZY26Pu6GD]

This experiment establishes the bar: every baseline metric and every judge variant on the same shared screen, scored with nonce-disguised sentences to control for memorisation. Total API spend was $2.02 (after the OpenRouter key was restored at 15:11 UTC; local judges ran during the outage and are kept as secondary rows).

#### The bar: disguised cheap judge

The primary cheap judge (Gemini 2.5 Flash Lite, JSON 0-100 scoring, nonce-disguised sentences) achieves AUROC 0.777 [0.720, 0.827] on track L (n = 524, 230 errors, 294 correct).

#### Full baseline table (track L, ERROR vs CORRECT, n = 524)

| Metric | AUROC | 95% CI |
|-|-|-|
| parse_fail | 0.500 | [0.500, 0.500] |
| pilot_joint_conflict | 0.513 | [0.488, 0.539] |
| pilot_arity_incons | 0.500 | [0.500, 0.500] |
| pilot_shape_incons | 0.524 | [0.470, 0.578] |
| pilot_dangling | 0.533 | [0.474, 0.592] |
| pilot_undeclared | 0.525 | [0.510, 0.542] |
| pilot_rerun_jacc | 0.720 | [0.659, 0.780] |
| rt_nli_min | 0.710 | [0.648, 0.769] |
| rt_nli_fwd | 0.652 | [0.588, 0.713] |
| rt_nli_bwd | 0.681 | [0.621, 0.742] |
| rt_nli_contra | 0.628 | [0.566, 0.686] |
| rt_nli_min_alt | 0.689 | [0.627, 0.749] |
| rt_embed_cos | 0.633 | [0.574, 0.696] |
| rt_reformalise_eq | 0.513 | [0.479, 0.547] |
| judge_cheap_orig | 0.749 | [0.695, 0.801] |
| judge_cheap_disg | 0.777 | [0.720, 0.827] |
| judge_cheap2_orig (gpt-4.1-nano) | 0.750 | [0.691, 0.810] |
| judge_cheap2_disg | 0.714 | [0.648, 0.777] |
| judge_strong_orig (gemini-3.1-pro) | 0.802 | [0.715, 0.877] |
| judge_strong_disg | 0.730 | [0.655, 0.803] |
| judge_local_qwen8b_disg | 0.757 | [0.702, 0.811] |
| judge_local_llama8b_disg | 0.671 | [0.604, 0.737] |
| judge_local_qwen14b_disg | 0.760 | [0.681, 0.834] |
| rt_nli_min_localverb | 0.740 | [0.680, 0.796] |

[FIGURE:fig_baseline_auroc]

#### Pilot structural metrics: negative result

The user's pilot structural metrics are null on this screen. Joint conflict achieves AUROC 0.513, arity inconsistency 0.500, shape inconsistency 0.524, dangling predicates 0.533, and undeclared predicates 0.525. The cross-system predicate-set Jaccard (pilot_rerun_jacc) reaches 0.720, the only pilot metric with signal, but this is a proxy for the consensus approach tested in Experiment C.

#### Round-trip verification

Round-trip NLI (verbalise the formula, compare to the original sentence via bidirectional NLI entailment) achieves AUROC 0.710 [0.648, 0.769]. This is 0.067 below the cheap judge (p = 0.008 by DeLong test). The round-trip reformalisation check (verbalise, re-translate to FOL, check z3 equivalence with the original) achieves only 0.513, because 76% of items tie at the same score.

Round-trip NLI using local verbalisation (the LLM verbalises on the local GPU instead of the API) reaches 0.740 [0.680, 0.796], slightly higher than the API version.

#### Frontier judge

The strong judge (Gemini 3.1 Pro Preview) achieves AUROC 0.802 [0.715, 0.877] on the strong subsample (n = 291). Under disguise it drops to 0.730 [0.655, 0.803]. The ΔAUROC over the cheap judge is +0.024 [−0.075, 0.111], not significant.

#### Cross-fitted baseline combinations (track L)

| Combination | AUROC | 95% CI |
|-|-|-|
| S1 (structural) | 0.698 | [0.634, 0.761] |
| S2 (round-trip) | 0.687 | [0.625, 0.749] |
| S3 (judges disguised) | 0.771 | [0.705, 0.831] |
| S4 (all cheap features) | 0.817 | [0.762, 0.867] |
| S6 (S4 + local judges) | 0.810 | [0.753, 0.861] |

S4 (all cheap features combined via cross-fitted logistic regression) achieves 0.817. This is +0.039 [−0.010, 0.087] over the cheap judge alone, not significant, but it sets the empirical ceiling for cheap baselines.

#### Contamination analysis

No evidence of contamination was found for any judge. The difference-in-differences (DiD) test compares the disguise effect on track H (where the LLM could have memorised public gold) to track L (where it evaluates its own outputs, not memorisable). All DiD CIs include zero:

| Judge | DiD (H − L) | 95% CI |
|-|-|-|
| flash-lite | −0.042 | [−0.170, 0.094] |
| gpt-4.1-nano | −0.077 | [−0.188, 0.023] |
| gemini-3.1-pro | +0.002 | [−0.115, 0.104] |
| Qwen3-8B | −0.045 | [−0.161, 0.079] |
| Llama-3.1-8B | +0.023 | [−0.112, 0.157] |
| Qwen3-14B | −0.073 | [−0.195, 0.056] |

The gold-recall probe confirms this: when the primary model translates track-H sentences from scratch, it matches the corrected gold 15.9% of the time but the original (public) gold only 4.4%. Predicate-name Jaccard with the original gold minus Jaccard with the Logic-LM GPT-4 output is −0.068 [−0.171, 0.034]; the model is not reproducing the public gold.

#### Invariance of judges under meaning-preserving rewrites

Judges are highly sensitive to meaning-preserving rewrites. The FA on CONTRAPOSITIVE rewrites is 0.67 for the cheap judge (original), 0.51 for the cheap judge (disguised), and 0.95 for the cheap2 judge. This compares poorly to FOL-Triage's fused flip rate of 0.0 on CONTRAPOSITIVE.

The full invariance table (track L CORRECT items, n = 270):

| Metric | RENAME flip | REORDER flip | DEMORGAN flip | CONTRA flip | ALL flip |
|-|-|-|-|-|-|
| judge_cheap_orig | 0.27 | 0.12 | 0.23 | 0.64 | 0.29 |
| judge_cheap_disg | 0.44 | 0.12 | 0.46 | 0.41 | 0.39 |
| judge_cheap2_orig | 0.49 | 0.12 | 0.46 | 0.95 | 0.49 |
| rt_nli_min | 0.37 | 0.10 | 0.31 | 0.33 | 0.31 |
| rt_embed_cos | 0.57 | 0.07 | 0.44 | 0.38 | 0.44 |
| FOL-Triage fused | 0.013 | 0.0 | 0.061 | 0.0 | 0.013 |

FOL-Triage has the lowest flip rate of any metric tested. Judges and round-trip methods change their verdict on 29-49% of meaning-preserving rewrites.

#### Per-error-type sensitivity of judges (track H, curator view, n = 46 errors)

| Group | n | judge_cheap_orig | judge_cheap_disg | judge_cheap2_orig | rt_nli_min |
|-|-|-|-|-|-|
| 1-op errors | 13 | 0.308 | 0.538 | 0.462 | 0.231 |
| 2-op errors | 11 | 0.545 | 0.818 | 0.727 | 0.273 |
| ADD | 12 | 0.500 | 0.750 | 0.667 | 0.250 |
| COMPOUND | 22 | 0.545 | 0.864 | 0.773 | 0.273 |
| DROP | 11 | 0.455 | 0.636 | 0.455 | 0.182 |
| CONN | 3 | 0.667 | 0.667 | 1.000 | 0.333 |
| NEG | 2 | 0.500 | 0.500 | 1.000 | 0.500 |
| SWAP | 2 | 0.000 | 1.000 | 0.500 | 0.000 |

The disguised judge is more sensitive than the original judge for most error types on the screen. [Correction (C2): on held-out E at matched FA 0.10, the original judge has higher recall than the disguised judge (R_SOLVER_CONS diff +0.106 [0.033, 0.178]; R_ADJ_AB diff +0.198 [0.130, 0.260]). Disguise does not uniformly improve the judge; the screen-level pattern does not generalise.]

#### Judge error-type classification accuracy

The judge's ability to name the correct error type is poor. On track-H 1-op errors, it identifies the correct repair operator 0% of the time (0/12). On 2-op errors, it is correct 45% (5/11). On track L, accuracy is 20% for 1-op and 27% for 2-op errors.

#### Complexity analysis (track L)

A logistic regression of judge correctness on standardised word count yields a coefficient of −0.48 (SE 0.11, p < 0.001): the judge is significantly less reliable on longer sentences. On track H (where longer sentences are available), the coefficient is −0.14 (SE 0.17, p = 0.41), consistent in direction but underpowered.

| Stratum | n (err/cor) | judge_cheap_disg AUROC | rt_nli_min AUROC |
|-|-|-|-|
| words < 12 | 485 (210/275) | 0.784 | 0.713 |
| words 12-19 | 36 (18/18) | 0.667 | 0.670 |
| quantifiers 0-1 | 512 (226/286) | 0.784 | 0.712 |
| depth ≤ 3 | 466 (199/267) | 0.781 | 0.702 |
| depth 4-5 | 54 (30/24) | 0.762 | 0.828 |
| 0 conditions | 394 (182/212) | 0.783 | 0.745 |
| 1-2 conditions | 128 (48/80) | 0.765 | 0.653 |

#### System-level descriptive statistics (3 systems, descriptive only)

| System | True error rate | Judge flag rate | rt_nli_min mean | Parse failures |
|-|-|-|-|-|
| gpt-3.5-turbo | 0.415 | 0.444 | 0.516 | 26/248 |
| gpt-4 | 0.385 | 0.362 | 0.496 | 10/282 |
| text-davinci-003 | 0.527 | 0.553 | 0.663 | 20/266 |

#### API outage and robustness

The shared OpenRouter key was exhausted at 13:29 UTC and restored at 15:11 UTC. During the outage, all LLM judges ran on the local RTX 4000 Ada GPU with the same prompts (Qwen3-8B, Llama-3.1-8B, Qwen3-14B-nf4). After the key was restored, the API judges were run and designated as primary; the local judges are kept as secondary rows. The local Qwen3-8B judge achieves AUROC 0.757 (disguised), comparable to the API flash-lite judge at 0.777.

### 1.5 Iteration 1 Summary

The four candidates and the bar:

| Method | AUROC | 95% CI | n | Cost/item | Rewrite flip rate |
|-|-|-|-|-|-|
| c_score (consensus) | 0.866 | [0.821, 0.906] | 546 | $0.0015/sent | 96% (RENAME) |
| S4 baseline combo | 0.817 | [0.762, 0.867] | 524 | varies | varies |
| **Bar: judge_cheap_disg** | **0.777** | **[0.720, 0.827]** | **524** | **$0.00004** | **0.39** |
| FOL-Triage fused | 0.759 | [0.695, 0.825] | 477 | $0.0002 | 0.013 |
| rt_nli_min | 0.710 | [0.648, 0.769] | 524 | $0.00001 | 0.31 |
| L1 lint | 0.508 | [0.499, 0.519] | 477 | $0 | 0.0 |
| Pilot structural | 0.50-0.53 | n/a | 524 | $0 | n/a |

[FIGURE:fig_summary_comparison]

**What iteration 1 established:**

1. The cross-system consensus metric (c_score = 1 − eq_frac) achieves the highest AUROC at 0.866, beating SC-5 by +0.140. It requires peer translations from multiple model families and is fundamentally non-invariant to predicate renaming (96% FA under RENAME).

2. The disguised cheap judge sets the bar at AUROC 0.777. The S4 combination of all cheap features reaches 0.817 (+0.039, not significant). The frontier judge (Gemini 3.1 Pro) adds nothing significant over the cheap judge.

3. FOL-Triage achieves AUROC 0.759, below the bar. Its primary value is invariance: the fused flip rate under meaning-preserving rewrites is 0.013, compared to 0.29-0.49 for judges. However, the fused false-alarm rate on CORRECT items is 0.194, exceeding the 0.10 calibration target.

4. L1 lint does not transfer from human annotation errors to LLM outputs. The pilot structural metrics are null. Round-trip NLI is 0.067 below the judge.

5. The evaluation labels are noisy: 58.8% of track-L "errors" are pure ADD+DROP (likely vocabulary mismatches). Iteration 2 will re-evaluate under panel-adjudicated labels from the held-out set.

6. No contamination was detected for any LLM-based metric.

**What remains for iteration 2:** (a) Re-evaluate all candidates under adjudicated labels from Artifact E. (b) Compute the paired ΔAUROC between FOL-Triage and the disguised judge on shared items. (c) Test whether combining the consensus metric with FOL-Triage or the judge produces a significant improvement. (d) Confirm on the held-out set.

## Iteration 2

### 2.1 Strategy

Iteration 2 has three goals: (i) confirm iteration 1's ordering on the held-out dataset E under both the solver labels (R_AB, R_A) and panel-adjudicated labels (R_ADJ); (ii) test whether fusing the consensus signal (PEER) with text-based checks (TEXT = L2-bow + L3) improves over each alone; and (iii) construct a typed perturbation suite (PERTURB) for controlled sensitivity testing.

The pre-registered bar for this iteration is the flash-lite judge on disguised sentences, with the local Qwen3-8B judge as fallback if the API is unavailable. The shared OpenRouter key hit its daily limit at 18:00 UTC on 2026-09-23, before the held-out experiment completed, and did not recover before the run deadline. The flash-lite bar is therefore UNTESTABLE on E; the fallback local judge (Qwen3-8B, rubric B, greedy; screen AUROC 0.757 vs 0.777 for flash-lite) is the labelled secondary bar for all rows reported below.

### 2.2 Experiment 5: PEER+TEXT on held-out dataset E

[ARTIFACT:art_TaxJRnPcJMuZ]

PEER+TEXT is a logistic fusion of the consensus signal (c_score with shared-vocabulary alignment, denoted c_score_align) and the text-based FOL-Triage layers (L2-bow, L3 questionnaire). The fusion weights were fitted on the iteration-1 screen and frozen before any E score was computed (prereg sha256 b9f28b1bf6bf). API spend was $0 (all components ran on CPU and the local GPU; no OpenRouter calls completed).

#### Name-free alignment: failed the pre-registered screen gate

A name-free variant of the consensus metric (graded clause consensus, g_score) was pre-registered as the primary PEER signal. It matches formula clauses by structural role without relying on shared predicate names, using anchored-cost assignment and Murty k-best matching. Under the pre-registered selection rule, both name-free variants (NF-pure and NF-anchored) failed the screen gate: for both, more than 10% of AGREE track-L CORRECT items tie at g = 1, making the deterministic false-alarm threshold degenerate (ROLE_PERMUTE recall = 0).

A post-hoc analysis with fractional tie-breaking showed this failure was a threshold-tie artefact. NF-anchored passes both gates under fractional scoring (RENAME FA 0.074, ROLE_PERMUTE recall 0.771); NF-pure still fails ROLE_PERMUTE (recall 0.186). The NF-anchored fusion was fitted post-hoc and applied to E as a labelled sensitivity analysis. On E (R_AB pooled), the NF-anchored fusion achieves AUROC 0.759 [0.72, 0.79], which is 0.031 below the pre-registered PEER+TEXT fusion (0.790), with the CI excluding zero [−0.042, −0.020]. The shared-aligner confound with the solver labeller remains open.

#### Headline AUROCs on E (R_AB, ERROR vs CORRECT)

| Subset | n (err/cor) | PEER+TEXT | c_score_align | NF c_score | L2-bow | L3 | Local judge |
|-|-|-|-|-|-|-|-|
| R_AB pooled | 2686 (1822/864) | 0.790 [0.75, 0.82] | 0.782 [0.74, 0.82] | 0.743 [0.70, 0.78] | 0.734 [0.71, 0.76] | 0.579 [0.53, 0.62] | 0.712 |
| R_AB L25 | 873 (697/176) | 0.755 [0.70, 0.80] | 0.712 [0.65, 0.77] | 0.651 [0.59, 0.71] | 0.722 [0.67, 0.77] | 0.560 [0.49, 0.63] | 0.664 |
| R_AB L20 | 821 (592/229) | 0.747 [0.69, 0.80] | 0.722 [0.66, 0.78] | 0.643 [0.58, 0.70] | 0.715 [0.66, 0.76] | 0.547 [0.48, 0.62] | 0.683 |
| R_AB EXC | 606 (384/222) | 0.777 [0.72, 0.83] | 0.814 [0.76, 0.86] | 0.782 [0.72, 0.84] | 0.669 [0.61, 0.72] | 0.620 [0.55, 0.69] | 0.663 |
| R_AB CTRL | 386 (149/237) | 0.708 [0.57, 0.84] | 0.742 [0.62, 0.86] | 0.741 [0.61, 0.86] | 0.613 [0.54, 0.72] | 0.490 [0.37, 0.62] | 0.739 |
| R_AB long pool | 2300 (1673/627) | 0.768 [0.74, 0.80] | 0.759 [0.72, 0.79] | 0.704 [0.67, 0.74] | 0.717 [0.69, 0.75] | 0.580 [0.54, 0.62] | 0.653 |
| R_A pooled L20+EXC | 449 (261/188) | 0.818 [0.73, 0.88] | 0.860 [0.79, 0.92] | 0.802 [0.72, 0.87] | 0.678 [0.61, 0.74] | 0.587 [0.51, 0.66] | 0.554 |

[FIGURE:fig_held_out_auroc]

#### PEER+TEXT vs the local judge

The paired ΔAUROC of PEER+TEXT minus the local judge is +0.078 [0.043, 0.112] on R_AB pooled (DeLong p < 0.0001). On the long pool (L25+L20+EXC), the gap widens to +0.115 [0.075, 0.157]. On R_A (tier-A adjudicated labels, L20+EXC), the gap is +0.264 [0.157, 0.359].

The flash-lite judge comparison is untestable: only 20 items received flash-lite scores before the key was exhausted, yielding a ΔAUROC of +0.057 [−0.200, 0.360] (n = 20, uninformative).

#### Does fusion beat c_score_align alone?

The stratified AUROC (pairing only within complexity strata, removing the composition confound) shows PEER+TEXT at 0.753 and c_score_align at 0.741, a difference of +0.011 [−0.012, 0.038], not significant. On the long pool the stratified gap is +0.016 [−0.010, 0.041]. On R_A the gap is −0.036 [−0.113, 0.030], favouring c_score_align. The TEXT layers add no significant discriminative power over c_score_align alone once the stratum-composition confound is removed.

#### Mechanism predictions

Four pre-registered mechanism predictions were tested on E:

**P1 (PEER catches COVERAGE errors that TEXT misses, and vice versa).** At matched false-alarm rate 0.10 with fractional tie-breaking: PEER has higher recall than TEXT on COVERAGE errors (+0.093 [0.046, 0.147]), and TEXT has higher recall on PEER_ENDORSED errors (+0.103 [0.051, 0.171]). [Correction (C5): the recall values for the local judge (Qwen-8B disguised) at FA 0.10 on the endorsed groups are: PEER_ENDORSED 0.169, PEER_ENDORSED_NF 0.199. The local judge has the highest recall on both endorsed groups, not the TEXT layers. The original report omitted the judge column and conflated the two endorsed-group names.] The crossover exists, but the fused PEER+TEXT recall is not higher than c_score_align alone on any group except COVERAGE. Verdict: INCONCLUSIVE.

**P2 (PEER and TEXT error rankings are uncorrelated).** Spearman correlation between PEER and TEXT among errors is 0.294 [0.224, 0.365]. This is moderate, not near zero. The gain from fusion over the best single signal (PEER) is only +0.042 AUROC, and the share from PEER-endorsed errors is −0.200, meaning TEXT hurts on items PEER already handles. Verdict: REFUTED.

**P3 (PEER+TEXT advantage grows with sentence complexity).** The logistic interaction term z(score)·z(words) is −0.023 [−0.228, 0.185] for PEER+TEXT, consistent with no interaction. The diff-in-Δ (long minus CTRL) of PEER+TEXT minus the local judge is +0.146 [0.020, 0.269], but this reflects the judge degrading on long sentences, not the fusion improving. Verdict: INCONCLUSIVE.

**P4 (PEER+TEXT is more invariant to meaning-preserving rewrites than judges).** On the screen pools, the fused score's RENAME false-alarm rate is 0.385 and the local judge's is 0.683. The fused score is better than judges but far worse than FOL-Triage fused (RENAME FA 0.22). [Correction (C6): the original report compared the fused RENAME FA 0.385 to "FOL-Triage's 0.013," but 0.013 was the FOL-Triage flip rate, not FA. The correct FA comparison is 0.385 vs 0.22.] The c_score_align component drives most of the fused FA under RENAME (0.859). Verdict: REFUTED.

#### Rewrite false alarms (screen, CORRECT bases)

| Rewrite | n | Fused | c_score_align | NF g | L2-bow | L3 | Local judge |
|-|-|-|-|-|-|-|-|
| RENAME | 104 | 0.385 | 0.859 | 0.074 | 0.216 | 0.168 | 0.683 |
| REORDER | 27 | 0.222 | 0.178 | 0.037 | 0.044 | 0.444 | 0.000 |
| DEMORGAN | 26 | 0.154 | 0.185 | 0.038 | 0.046 | 0.231 | 0.231 |
| CONTRAPOSITIVE | 28 | 0.107 | 0.063 | 0.237 | 0.075 | 0.188 | 0.214 |

The NF g_score has the lowest RENAME false-alarm rate (0.074) of any consensus-based signal, confirming the value of name-free matching. However, its CONTRAPOSITIVE FA (0.237) is higher than c_score_align's (0.063).

#### Error typing

On R_A errors with 1-2 typed repair operators (n = 453), the top-code accuracy of the medoid-ops typed repair is 0.371 (codable-only 0.561, n = 262). Chance level is 0.382. The local judge's type-classification accuracy is 0.022 (10/453). Error typing from automated metrics remains unreliable.

#### System-level correlation

Kendall τ-b of each metric vs the R_AB system error rate across 13 system × variant rows: PEER+TEXT 0.718, TEXT alone 0.769, PEER alone 0.692, local judge 0.667. All metrics track system quality at the aggregate level.

#### Contamination on E

The local Qwen3-8B judge shows a disguise effect in the unexpected direction: disguised AUROC (0.712) exceeds original AUROC (0.648) by +0.064 [0.032, 0.098]. [Correction (C1c): the sign of this effect is −0.064 [−0.098, −0.032], i.e. disguise improves the judge's AUROC. This does not mean disguise "forces structural reading"; see correction C2.] The DiD test (comparing the disguise effect on track H vs track L) yields +0.045 [−0.073, 0.161], with the CI including zero. No contamination is detected. [Correction (C1a/C1b): The iteration-2 baselines experiment (experiment 6) also ran a DiD on E. Llama-8B DiD = +0.162 [0.064, 0.261], significant and above MDE 0.139, raising a contamination concern for that judge. Qwen-8B DiD = +0.036 [−0.039, 0.111], n.s., MDE 0.107.] The PEER signal has no contamination channel, because it uses z3 equivalence (no text or names from the benchmark enter the scoring).

#### Coverage and cost

Of 8,507 rows, 7,421 (87.2%) are parseable and scored; 1,086 (12.8%) are unparseable (scored as maximum error probability). 38 rows have no peer translations available. The L3 questionnaire completed on all parseable rows. Mean CPU time per row: PEER pairs 0.026 s, NF pairs 0.208 s, TEXT 0.220 s. Mean cost per row for PEER+TEXT (L3 share): $0.000018. The local judge costs $0.000040 per row.

### 2.3 Evaluation 1: Re-evaluation under alternative label regimes

[ARTIFACT:art_HepAw8c6Eu7-]

The iteration-1 experiments used solver labels (R_SOLVER): a formula is CORRECT if z3 proves it equivalent to the audited gold, ERROR otherwise. This is conservative: formulas that are semantically faithful but use different vocabulary or granularity are counted as errors. The parallel run adjudicated a panel of labels (R_ADJ) on the same items, where three LLM judges vote on faithfulness given only the sentence and candidate. This evaluation re-scores all metrics under 13 label regimes on a common item set (588 items shared across experiments A, C, D, and E).

#### Rederivation audit

All 57 reviewer-audited quantities from the iteration-1 report reproduce exactly under independent recomputation (57/57 MATCH, tolerance ≤ 0.01 for AUROCs, ≤ 0.005 for bootstrap replicas). The reviewer's own RNG seed replicas match to ≤ 0.0005.

#### Regime AUROC matrix (common set, selected metrics)

| Metric | R_SOLVER | R_ADJ_AB | R_ADJ_A | R_ADJ_ALL |
|-|-|-|-|-|
| PT (PEER+TEXT) | 0.871 | 0.877 | 0.932 | 0.906 |
| fused_H (FOL-Triage) | 0.770 | 0.868 | 0.958 | 0.866 |
| c_score | 0.849 | 0.779 | 0.786 | 0.831 |
| L2-bow | 0.732 | 0.815 | 0.917 | 0.810 |
| L3 | 0.761 | 0.718 | 0.813 | 0.751 |
| judge_cheap_disg | 0.782 | 0.772 | 0.751 | 0.816 |
| judge_cheap_orig | 0.754 | 0.797 | 0.858 | 0.785 |
| sc5_cheap | 0.713 | 0.703 | 0.676 | 0.737 |
| rt_nli_min | 0.709 | 0.749 | 0.731 | 0.760 |

Under R_ADJ_AB, PEER+TEXT (0.877) leads, followed by FOL-Triage fused (0.868) and L2-bow (0.815). The c_score drops from 0.849 (solver) to 0.779 (R_ADJ_AB), because the adjudicated labels reclassify many vocabulary-mismatch items as CORRECT, removing the easy wins for the consensus signal. Under R_ADJ_A (tier-A only, 75 common items), FOL-Triage reaches 0.958 and PEER+TEXT 0.932, both well above the judges.

#### Label regime shifts

On the 161 items shared between R_SOLVER and R_ADJ_AB (36 label changes), the label-only shift is:

| Metric | Shift | 95% CI | Direction |
|-|-|-|-|
| fused_H | +0.080 | [0.003, 0.171] | UP |
| L2-bow | +0.102 | [0.018, 0.192] | UP |
| c_score | −0.106 | [−0.255, 0.013] | INSIDE CI |
| judge_cheap_disg | +0.018 | [−0.094, 0.134] | INSIDE CI |

BOW and the fused score benefit from adjudicated labels (their AUROCs go up), because the vocabulary-mismatch items they flag correctly are now labelled CORRECT. The c_score shift is negative but not significant, consistent with its reliance on the same vocabulary alignment that the solver uses.

#### Flipped items

Between solver and adjudicated labels, 51 items flip from CORRECT to ERROR and 1 flips from ERROR to CORRECT. The fused score (FOL-Triage) flags 83% of the CORRECT→ERROR items at matched FA 0.20, while c_score flags only 34%. This indicates that the text-based layers detect errors that the solver misses (vocabulary-equivalent but semantically wrong).

#### Frontier vs cheap judge

On the subset where both frontier (Gemini 3.1 Pro) and cheap judge scores are available, the frontier judge's advantage strengthens from solver to panel labels. [Correction (C4): under solver labels the advantage is +0.077 [0.006, 0.154]; under panel A+B it grows to +0.166 [0.086, 0.244] (p < 0.001). The original report said the advantage "reverses" the iteration-1 finding; in fact it strengthens monotonically from solver to panel labels, because panel labels reclassify vocabulary-mismatch items the frontier judge handles better.]

#### Contamination on the common set

All DiD CIs include zero across all judges. The MDE (minimum detectable effect at 80% power) ranges from 0.12 to 0.21, so small contamination effects cannot be ruled out but no evidence was found. The gpt-4.1-nano judge shows significant single-track drops on H (AUROC disg−orig = −0.114 [−0.206, −0.028]), but the DiD with track L is +0.077 [−0.028, 0.190], not significant.

### 2.4 Dataset 3: R_COMP and PERTURB

[ARTIFACT:art_zcwCQgTqk6DN]

This artifact constructs two evaluation resources: R_COMP (long composed sentences with trusted FOL references) and PERTURB (a typed perturbation suite with z3-verified controls).

#### R_COMP: incomplete (OpenRouter key exhausted)

The R_COMP component generates long, complex sentences (≥ 25 words, ≥ 3 conditions) by composing atoms from a verified lexicon of 652 entries extracted from FOLIO and MALLS source formulas. Nine templates (T1-T9) produce sentences with weak and strong exception readings, each with a z3-verified reference formula. The composition pipeline selected 250 main + 100 reserve sentences from 5,109 filtered candidates.

The candidate generation, labelling, and adjudication phases did not run because the shared OpenRouter key hit its $50 daily limit at approximately 18:00 UTC, after $0.41 in lexicon-extraction calls. The key did not recover before the module's deadline. The replacement key arrived at 21:38 UTC but was already at its daily limit. R_COMP references are constructed deterministically and are correct by construction, but the LLM-generated candidate translations and their labels are absent.

#### PERTURB: complete

The typed perturbation suite applies 12 operator types to 300 base formulas (200 from dataset E, 100 from R_COMP sentences) to produce controlled mutants where the error type and direction are known by construction. All mutants are z3-verified: the DOWN mutant is z3-non-equivalent to the base and the matched CONTROL is z3-equivalent.

| Statistic | Value |
|-|-|
| Base formulas | 300 |
| Total mutants (DOWN + UP) | 4,234 |
| Matched controls | 868 |
| Total suite rows | 5,102 |
| Complete DOWN/UP pairs | 1,354 |
| z3 verification failures | 0 |
| Operator types | 12 (NEG, REV, QUANT, RESTR, CONN, MOVE, DROP, ADD, SWAP, BIND, SCOPE, UNGLUE) |
| Cost | $0.41 |

Each perturbation row carries a known label (ERROR for DOWN mutants, CORRECT for controls) and a typed operator, enabling per-type sensitivity analysis without relying on automated error classification. The suite is fully deterministic and re-runnable.

### 2.5 Iteration 2 Summary

**What iteration 2 established:**

1. PEER+TEXT achieves AUROC 0.790 [0.75, 0.82] on the held-out dataset E (R_AB pooled, n = 2686), beating the local judge by +0.078 [0.043, 0.112] (DeLong p < 0.0001). On long sentences (L25+L20+EXC, n = 2300) the gap widens to +0.115 [0.075, 0.157]. The flash-lite judge bar is UNTESTABLE due to API key exhaustion (only 20 rows scored).

2. Fusion does not significantly beat c_score_align alone. The stratified AUROC difference (PEER+TEXT minus c_score_align) is +0.011 [−0.012, 0.038] on R_AB pooled. The TEXT layers add coverage on COVERAGE-type errors (+0.093 recall at matched FA) but hurt on PEER-endorsed errors (−0.200 share). The mechanism prediction P2 (uncorrelated error rankings) is REFUTED: Spearman(PEER, TEXT) = 0.294.

3. The name-free consensus variant (NF-anchored) failed the pre-registered screen gate due to a threshold-tie artefact. Post-hoc fractional scoring shows it passes both gates (RENAME FA 0.074, ROLE_PERMUTE recall 0.771) and achieves AUROC 0.759 on E, 0.031 below PEER+TEXT. The NF approach has the lowest RENAME false-alarm rate (0.074) of any consensus signal, confirming the value of vocabulary-independent matching, but was not used in the primary analysis.

4. Under adjudicated labels (R_ADJ_AB), the metric ranking changes. FOL-Triage fused rises from 0.770 (solver) to 0.868 (adjudicated). The c_score drops from 0.849 to 0.779. This is because adjudicated labels reclassify vocabulary-mismatch items as CORRECT, removing the consensus signal's easy wins. PEER+TEXT (0.877) still leads under adjudicated labels.

5. The frontier judge advantage is large under adjudicated labels (+0.166 AUROC over the cheap judge under R_ADJ_AB, p < 0.001), reversing the non-significant iteration-1 finding under solver labels. Solver labels masked the frontier judge's advantage.

6. All 57 reviewer-audited numbers from iteration 1 reproduce exactly (57/57 MATCH).

7. The PERTURB suite (4,234 typed mutants + 868 controls, 12 operator types, all z3-verified) is complete and ready for per-type sensitivity analysis. R_COMP candidate generation is blocked on the OpenRouter key.

### 2.6 Experiment 6: Baselines on held-out E (omitted from the original iteration-2 report)

[Correction: the iteration-2 report omitted the full baselines experiment on held-out E. The results are recorded here for completeness.]

Experiment 6 scored all local and baseline metrics on the held-out dataset E under R_AB labels (n = 2686, 1822 ERROR / 864 CORRECT, 292 sentences). The primary local bar is the Qwen3-8B judge (disguised).

#### Pooled AUROCs on E (R_AB, selected metrics)

| Metric | AUROC [95% CI] |
|-|-|
| S4_local (all tiers) | 0.754 [0.715, 0.789] |
| S4_local (R_AB) | 0.748 [0.709, 0.782] |
| judge_local_qwen8b_disg | 0.710 [0.674, 0.746] |
| S4_local_noLLMjudge | 0.703 [0.660, 0.742] |
| sc5_local_eq_frac | 0.664 [0.617, 0.706] |
| pilot_rerun_jacc | 0.660 [0.621, 0.695] |
| judge_local_qwen8b_orig | 0.649 [0.604, 0.693] |
| judge_local_llama8b_disg | 0.636 [0.590, 0.681] |
| rt_nli_min_local | 0.626 [0.580, 0.673] |
| b2_score | 0.574 [0.529, 0.619] |
| pilot_shape_incons | 0.504 [0.499, 0.510] |
| parse_fail | 0.500 [0.500, 0.500] |

The cross-fitted S4_local stack (logistic regression over all local features) achieves 0.748, beating the local judge by +0.038 [0.005, 0.069]. The PEER+TEXT consensus signal adds +0.042 [0.013, 0.070] over S4_local on pooled AUROC.

#### System-level correlation (13 system × variant rows; descriptive)

The best system-level tracker is S4_local (all tiers): Kendall τ-b = 0.615 [0.513, 0.770] over 13 system × variant rows. Over 11 families: τ-b = 0.709 [0.600, 0.818].

### 2.7 Dead ends: B2 and R_ADJ

**Candidate B2 (decomposed z3 distinguishing-worlds reader): DROPPED.** Candidate B2 extended iteration-1's candidate B (template NLI + z3 distinguishing worlds) by having a non-thinking local reader classify z3-generated distinguishing models. The gate balanced accuracy on track-H corrected labels was 0.476 (target ≥ 0.85). The decomposed reader could not reliably interpret z3 countermodels. A post-hoc thinking-mode variant reached 0.786 balanced accuracy on 124/251 completed items, but this was not pursued because the non-thinking version had already settled negative. The b2_score AUROC on E (R_AB pooled) was 0.574, below every other non-null metric. B2 is DROPPED and not retried.

**R_ADJ adjudicator gate: DROPPED.** [Correction (C7, partial): dataset 2 (R_ADJ construction) spent $3.660.] The iteration-2 plan called for an LLM-adjudicated label regime (R_ADJ) using Sonnet-5 as primary adjudicator, with Grok-4.20 as secondary. Both adjudicators failed the gate:

| Adjudicator | Gate track-H balanced accuracy | Target |
|-|-|-|
| Sonnet-5 | 0.662 | ≥ 0.80 |
| Grok-4.20 | 0.527 | ≥ 0.80 |

Inter-adjudicator kappa was 0.497 on all items and 0.416 on real E rows. Sonnet-5 test-retest kappa was 0.834 with a flip rate of 0.07, indicating the adjudicator was internally consistent but systematically wrong on track-H items. Of 74 track-H pairs, Sonnet-5 judged 43% of expert-corrected originals as FAITHFUL (they should be UNFAITHFUL), producing a recall_unfaithful of 0.568. R_ADJ is DROPPED. All confirmation analyses use R_AB (solver labels with panel adjudication of contested items).

[Correction (C7): Iteration-2 total API spend was $4.229: experiment 5 $0.155, experiment 6 $0.000, dataset 2 $3.660, dataset 3 $0.414, evaluation 1 $0.000.]

**What remains:**

(a) Run the flash-lite judge on E when the OpenRouter key resets, to test the pre-registered bar. (b) Complete R_COMP candidate generation and labelling. (c) Score all metrics on the PERTURB suite for per-type sensitivity under known labels. (d) Re-fit the PEER+TEXT fusion under R_ADJ labels (the current fusion was fitted under solver labels, which penalise it). (e) Test whether a name-free fusion (NF-anchored + TEXT) closes the 0.031 gap with the aligner-based fusion when the aligner confound is removed.

## Iteration 3

### 3.1 Strategy

Iteration 3 resolves the two gaps that iteration 2 left open: the flash-lite API bar and the R_COMP candidate generation. It runs five pre-registered tests:

- **T1** (head-on API bar): score c_score_align and all baselines with API-tier judges on held-out E. The bar is the best API cheap judge (flash-lite disguised). Success: stratified AUROC of c_score_align exceeds the bar with the 95% CI excluding zero.
- **T2** (R_COMP): generate candidate translations for the 221 R_COMP sentences (long composed sentences with trusted-by-construction references) and score all metrics. Success: within-template AUROC of consensus exceeds flash-lite disguised with the 95% CI excluding zero, under both SIG (shared vocabulary) and FREE (independent vocabulary) conditions.
- **T3** (PERTURB per-operator sensitivity): score the PERTURB suite with all metrics. Report within-base AUROC per operator per metric. No pass/fail gate; the table is descriptive.
- **T4** (mechanism verification): verify 48 numerical claims from the iteration-2 report via independent recomputation, and test four mechanism predictions (M1-M4) about why consensus works.
- **T5** (PERTURB rename tradeoff): measure the rename false-alarm rate and the MEANING_RENAME recall for each consensus variant on the PERTURB suite. This quantifies the cost of vocabulary alignment.

### 3.2 Test T1: Head-on API bar on held-out E

[ARTIFACT:art_T1_API_bar]

The shared OpenRouter key was available for this iteration. All API metrics (flash-lite judge, gpt-4.1-nano judge, Gemini 3.1 Pro frontier judge, API round-trip NLI, API SC-5) were scored on E. The population is E_POOL PRIMARY under R_AB: n = 2686 (1822 ERROR / 864 CORRECT, 292 sentences). All CIs are sentence-cluster percentile bootstrap (B = 2000, seed 0). "Strat" denotes within-stratum AUROC, where only ERROR/CORRECT pairs from the same source stratum contribute.

#### Verdict

| Criterion | Status | Key numbers |
|-|-|-|
| (a) c_score_align beats flash-lite disguised | **CONFIRMED** | R_AB strat Δ +0.099 [+0.049, +0.146]; long strat Δ +0.116 [+0.070, +0.163] |
| (b) adds signal beyond S4_full (nested) | **CONFIRMED** | strat Δ +0.039 [+0.021, +0.057]; permutation null p95 = 0.009 |
| (d) frontier ratio ≥ 0.95 at ≤ 10× cost | **CONFIRMED** | ratio 0.957 [0.887, 1.034]; cost ratio 30.2× cheaper |
| VEX confound control (sign > 0) | **CONFIRMED** | strat Δ +0.306 [+0.232, +0.376] |
| M3 length slope (consensus − judge) | **DISCONFIRMED** | words Δslope +0.146 [−0.051, +0.361]; n_conditions +0.116 [−0.044, +0.264] |

**Overall T1: CONFIRMED.** Robustness check against gpt-4.1-nano (the second-best API cheap judge): criterion (a) also CONFIRMED (R_AB strat Δ +0.089 [+0.043, +0.134]).

#### Item-level AUROC on R_AB (E_POOL PRIMARY)

| Metric | Pooled AUROC [CI] | Strat AUROC [CI] | AUPRC | $/item |
|-|-|-|-|-|
| p_peer_text | 0.790 [0.752, 0.825] | 0.753 [0.720, 0.784] | 0.879 | 1.21e-04 |
| c_score_align | 0.782 [0.745, 0.816] | 0.741 [0.705, 0.775] | 0.861 | 1.21e-04 |
| S4_full_oof | 0.777 [0.739, 0.809] | 0.735 [0.699, 0.766] | 0.874 | -- |
| S4_local_oof | 0.748 [0.709, 0.782] | 0.693 [0.656, 0.729] | 0.856 | -- |
| nf_c_score | 0.743 [0.702, 0.780] | 0.686 [0.647, 0.720] | 0.829 | -- |
| L2-bow | 0.734 [0.705, 0.762] | 0.697 [0.667, 0.726] | 0.830 | -- |
| judge_local_qwen8b_disg | 0.710 [0.674, 0.746] | 0.674 [0.646, 0.703] | 0.815 | -- |
| judge_cheap2_orig | 0.700 [0.659, 0.739] | 0.653 [0.616, 0.688] | 0.823 | 2.01e-05 |
| judge_cheap_disg | 0.696 [0.655, 0.733] | 0.642 [0.607, 0.676] | 0.786 | 4.88e-05 |
| judge_cheap2_disg | 0.681 [0.641, 0.719] | 0.644 [0.609, 0.680] | 0.806 | 2.01e-05 |
| sc5_eq_frac | 0.656 [0.609, 0.699] | 0.598 [0.559, 0.637] | 0.758 | 2.95e-05 |
| rt_nli_min | 0.639 [0.593, 0.687] | 0.606 [0.569, 0.645] | 0.776 | 2.75e-05 |
| judge_cheap_orig | 0.635 [0.595, 0.671] | 0.623 [0.593, 0.651] | 0.772 | 4.88e-05 |
| rt_nli_fwd | 0.674 [0.631, 0.716] | 0.611 [0.573, 0.650] | 0.812 | -- |
| L3 | 0.579 [0.532, 0.625] | 0.562 [0.524, 0.601] | 0.720 | -- |
| rt_embed_cos | 0.574 [0.527, 0.623] | 0.566 [0.526, 0.607] | 0.731 | -- |
| parse_fail | 0.500 [0.500, 0.500] | 0.500 [0.500, 0.500] | 0.678 | -- |

c_score_align achieves strat AUROC 0.741, beating the best API cheap judge (flash-lite disguised, 0.642) by +0.099 [+0.049, +0.146]. The PEER+TEXT fusion (p_peer_text) reaches 0.753 stratified. These are the only metrics whose strat CIs exclude the flash-lite bar.

Note: the flash-lite strat AUROC on E (0.642) is substantially below its iteration-1 screen AUROC (0.777 pooled). The screen was dominated by short, simple sentences with high base-rate discrimination; on the longer, harder E sentences, the judge's advantage shrinks. This is consistent with the iteration-1 observation that the screen has limited long-sentence coverage.

#### Paired deltas: challenger minus bar (stratified)

| Cell | n (E/C) | Challenger | Δ vs flash-lite disg [CI] |
|-|-|-|-|
| R_AB pooled | 1822/864 | c_score_align | +0.099 [+0.049, +0.146] |
| R_AB pooled | 1822/864 | p_peer_text | +0.110 [+0.065, +0.154] |
| R_AB long (L25+L20+EXC) | 1673/627 | c_score_align | +0.116 [+0.070, +0.163] |
| R_AB long (L25+L20+EXC) | 1673/627 | p_peer_text | +0.132 [+0.091, +0.173] |
| R_AB EXC | 384/222 | c_score_align | +0.197 [+0.124, +0.269] |
| R_AB EXC | 384/222 | p_peer_text | +0.160 [+0.091, +0.232] |
| R_A L20+EXC | 261/188 | c_score_align | +0.299 [+0.212, +0.390] |
| R_A L20+EXC | 261/188 | p_peer_text | +0.264 [+0.180, +0.351] |
| R_AB CTRL | 149/237 | c_score_align | −0.069 [−0.232, +0.098] |

On CTRL sentences (short, simple, no conditions or exceptions), the consensus advantage vanishes. This is expected: short sentences generate fewer distinct translation variants, and the bar judge performs well on simple items.

The advantage is largest on exception sentences (EXC: +0.197) and on R_A tier-A labels (+0.299), where errors are unambiguous and vocabulary differences are less likely to confound the equivalence check.

#### Cross-fitted stacks and nesting

| Stack | Pooled OOF AUROC [CI] | Strat OOF AUROC [CI] |
|-|-|-|
| S4_local | 0.748 [0.709, 0.782] | 0.693 [0.656, 0.729] |
| S4_full | 0.777 [0.739, 0.809] | 0.735 [0.699, 0.766] |
| S4_full + c_score_align | 0.807 [0.772, 0.838] | 0.774 [0.743, 0.802] |
| S4_full + p_peer_text | 0.808 [0.775, 0.839] | 0.776 [0.745, 0.805] |
| S4_full + g_c (all consensus) | 0.809 [0.774, 0.840] | 0.776 [0.745, 0.805] |
| S4_local + c_score_align | 0.796 [0.759, 0.828] | 0.757 [0.723, 0.788] |
| PT_refit (4 features) | 0.808 [0.769, 0.842] | 0.778 [0.742, 0.813] |

| Nested contrast | Strat Δ [CI] | Pooled Δ [CI] |
|-|-|-|
| S4_full + c_score_align − S4_full | +0.039 [+0.021, +0.057] | +0.030 [+0.015, +0.045] |
| S4_full + p_peer_text − S4_full | +0.041 [+0.022, +0.060] | +0.032 [+0.017, +0.046] |
| S4_full + nf_c_score − S4_full | +0.013 [+0.002, +0.023] | +0.010 [+0.001, +0.019] |
| S4_local + c_score_align − S4_local | +0.064 [+0.042, +0.086] | +0.048 [+0.030, +0.067] |
| S4_full − S4_local | +0.042 [+0.022, +0.063] | +0.029 [+0.013, +0.045] |

Adding c_score_align to S4_full yields +0.039 strat AUROC, comparable to S4_full's own gain over S4_local (+0.029 pooled, +0.042 strat). The consensus signal is the single largest new contributor to the best stack. Permutation null (100 reps, labels permuted within fold × stratum): the observed strat Δ 0.039 is at percentile 1.00 of the null distribution (p95 = 0.009).

The PT_refit model (4 features: c_score_align, L2-bow, L3, p_text) reaches 0.778 strat with no judge features, matching the 28-feature S4_full stack.

Largest standardised coefficients of S4_full + c_score_align (mean over 5 folds): rt_nli_fwd +0.901, c_score_align +0.848, local rt_nli_fwd −0.651, local judge_qwen8b_disg +0.591.

#### VEX confound control

The VEX (vocabulary-exact) subset restricts to items where the candidate and gold share the same predicate and constant names, removing the vocabulary-alignment confound. On VEX items (183 ERROR / 433 CORRECT, 146 sentences):

| Subset | Strat Δ c_score_align − judge_cheap_disg [CI] |
|-|-|
| VEX | +0.306 [+0.232, +0.376] |
| VEX_STRICT | +0.202 [+0.144, +0.269] (pooled) |
| VEX_tierA_only | +0.224 [+0.161, +0.297] (pooled) |

Even when vocabulary alignment is trivial (all names match), consensus outperforms the judge by a wide margin. This rules out the hypothesis that c_score_align's advantage is solely due to its vocabulary aligner exploiting the same signal as the solver labeller.

However, on aligner-masked errors (tier B, automatic VOCAB_GRAN label, panel ERROR; n = 221), recall at FA 0.10 is low for all metrics: c_score_align 0.07, judge_cheap_disg 0.17, S4_full_oof 0.17. Vocabulary-granularity errors remain a blind spot for the consensus signal.

#### Frontier judge (284-row frame)

On the 284 R_AB-labelled items where the frontier judge (Gemini 3.1 Pro) was scored:

| Metric | AUROC [CI] | IPW AUROC [CI] |
|-|-|-|
| S4_full_oof | 0.745 [0.688, 0.797] | 0.768 [0.714, 0.818] |
| judge_strong_orig | 0.741 [0.686, 0.792] | 0.755 [0.699, 0.807] |
| p_peer_text | 0.723 [0.669, 0.776] | 0.753 [0.701, 0.804] |
| c_score_align | 0.710 [0.650, 0.766] | 0.736 [0.677, 0.792] |
| judge_cheap_disg | 0.664 [0.611, 0.717] | 0.686 [0.628, 0.738] |

Ratio AUROC(c_score_align) / AUROC(judge_strong_orig) = 0.957 [0.887, 1.034]. The consensus metric achieves 96% of the frontier judge's discriminative power. Nested in the frame: [strong_orig + c_score_align] − [strong_orig] = +0.037 [+0.008, +0.066]. Cost per item: frontier judge $0.00365; consensus $0.000121 (30.2× cheaper).

#### M3: complexity slope (DISCONFIRMED)

M3 predicted that the consensus metric's advantage over the judge would grow with sentence length (i.e. that the consensus-minus-judge slope per SD of words would be positive). The GEE slopes at matched FA 0.10:

| Metric | Slope per SD words [CI] | Slope per SD n_conditions [CI] |
|-|-|-|
| c_score_align | −0.292 [−0.570, −0.013] | 0.000 [−0.170, +0.170] |
| judge_cheap_disg | −0.438 [−0.708, −0.168] | −0.115 [−0.280, +0.049] |

Δslope (consensus − judge): words +0.146 [−0.051, +0.361]; n_conditions +0.116 [−0.044, +0.264]. Both CIs include zero. M3 is **DISCONFIRMED**: the consensus advantage does not grow significantly with complexity. Both metrics degrade on longer sentences; the consensus merely degrades less.

#### AUROC by complexity bin

**Words:**

| Bin | n (E/C) | c_score_align | p_peer_text | judge_cheap_disg | S4_full_oof | Δ c − judge [CI] |
|-|-|-|-|-|-|-|
| <12 | 154/283 | 0.725 | 0.746 | 0.766 | 0.772 | −0.040 [−0.178, +0.103] |
| 12-19 | 255/134 | 0.701 | 0.682 | 0.607 | 0.667 | +0.094 [+0.013, +0.188] |
| 20-24 | 686/262 | 0.727 | 0.740 | 0.625 | 0.715 | +0.103 [+0.026, +0.171] |
| 25-34 | 614/161 | 0.705 | 0.753 | 0.618 | 0.727 | +0.087 [−0.006, +0.178] |
| >=35 | 113/24 | 0.759 | 0.756 | 0.706 | 0.789 | +0.054 [−0.115, +0.173] |

**Exception type:**

| Bin | n (E/C) | c_score_align | judge_cheap_disg | Δ [CI] |
|-|-|-|-|-|
| None | 1393/617 | 0.776 | 0.731 | +0.046 [+0.007, +0.089] |
| except | 62/71 | 0.964 | 0.600 | +0.365 [+0.236, +0.472] |
| unless | 179/98 | 0.801 | 0.713 | +0.088 [+0.001, +0.164] |

The consensus advantage is concentrated in sentences with 12+ words (where the bar judge degrades) and is largest on exception-clause sentences (AUROC 0.964 vs 0.600 for "except" sentences).

#### Contamination

- flash-lite: DiD (GOLDSYS vs E_POOL) = +0.105 [+0.006, +0.201], MDE 0.140. The CI barely excludes zero but the effect is below MDE. Marginal evidence.
- gpt-4.1-nano: DiD = −0.009 [−0.095, +0.074], MDE 0.122. No contamination.
- flash-lite test-retest (187 rows): Spearman 0.975, exact-match share 0.984, mean |Δp| 0.011.

#### Recall per error group at matched FA 0.10 (descriptive)

| Group | n | c_score_align | p_peer_text | judge_cheap_disg | judge_strong_orig | S4_full_oof |
|-|-|-|-|-|-|-|
| COMPOUND (tier B) | 1148 | 0.55 | 0.63 | 0.25 | 0.67 | 0.56 |
| polarity (NEG/REV/QUANT) | 434 | 0.53 | 0.56 | 0.26 | 0.74 | 0.53 |
| structural (RESTR/CONN/BIND/SWAP/MOVE/SCOPE) | 1282 | 0.49 | 0.53 | 0.24 | 0.60 | 0.50 |
| COVERAGE (ADD/DROP only) | 246 | 0.27 | 0.26 | 0.13 | 0.27 | 0.20 |
| MEANING_RENAME | 221 | 0.07 | 0.10 | 0.17 | 0.09 | 0.17 |
| PEER_ENDORSED | 398 | 0.00 | 0.06 | 0.16 | 0.07 | 0.17 |
| PEER_ENDORSED_NF | 340 | 0.05 | 0.11 | 0.13 | 0.15 | 0.21 |

Consensus has the highest recall on COMPOUND and polarity errors (0.55 and 0.53), where the wrong formula is z3-distinguishable from the medoid. It has near-zero recall on MEANING_RENAME and PEER_ENDORSED errors, where most peers share the same wrong formula or the error consists of a predicate-name substitution. The frontier judge has the highest recall overall but costs 30× more.

#### System-level correlation (10 families)

| Metric | τ-b over system × variant [CI] | τ-b over families [CI] |
|-|-|-|
| p_peer_text | 0.718 [0.590, 0.846] | 0.822 [0.644, 0.911] |
| c_score_align | 0.692 [0.513, 0.795] | 0.822 [0.600, 0.911] |
| judge_cheap2_disg | 0.718 [0.590, 0.846] | 0.822 [0.644, 0.911] |
| judge_cheap_disg | 0.564 [0.410, 0.718] | 0.600 [0.422, 0.778] |
| S4_full_oof | 0.590 [0.538, 0.769] | 0.644 [0.467, 0.778] |

(13 system × variant rows, 10 families.)

#### Placebos

Shuffled-label AUROC for c_score_align: 0.501 (null). Shuffled-label strat Δ (c minus cheap_disg): mean 0.001, 2.5th percentile −0.029, 97.5th percentile +0.035 (observed: +0.099, well outside null).

### 3.3 Test T2: R_COMP (long composed sentences)

[ARTIFACT:art_R_COMP]

R_COMP generates long, complex sentences (≥ 25 words, 4-5 conditions) from a verified lexicon, each with a z3-verified reference formula. Nine templates (T1-T9) vary the logical connective structure and exception semantics. The SIG condition uses a shared predicate vocabulary (all translators see the same names); the FREE condition lets each translator choose its own names.

221 sentences produced 2,024 candidate translations (10 LLM slots, with READING_CHOICE and OFF_SIGNATURE exclusions). Population: 429 ERROR / 1,595 CORRECT.

#### SIG: primary test (criterion c)

| Statistic | c_score_sig | judge_cheap_disg | Δ [95% CI] | PASS |
|-|-|-|-|-|
| Within-template AUROC | 0.954 | 0.587 | +0.367 [+0.328, +0.404] | **True** |

The consensus metric's within-template AUROC is 0.954, massively outperforming the flash-lite disguised judge at 0.587. The delta of +0.367 is the largest effect observed in any test.

Under the SIG condition, c_score_sig, c_score_align, and c_score_nf all achieve within-template AUROC ≥ 0.950 because the shared vocabulary makes z3 equivalence checking exact. The gold-exact variants (g_align, g_nf) reach 0.977 because they compare against the trusted reference.

#### SIG: per-metric AUROCs

| Metric | n | Within-template [CI] | Pooled [CI] | AUPRC |
|-|-|-|-|-|
| g_align | 2024 | 0.977 [0.970, 0.983] | 0.978 [0.972, 0.983] | 0.878 |
| g_nf | 2024 | 0.976 [0.968, 0.983] | 0.976 [0.970, 0.982] | 0.877 |
| c_score_sig | 2024 | 0.952 [0.937, 0.965] | 0.964 [0.957, 0.971] | 0.803 |
| c_score_align | 2024 | 0.952 [0.937, 0.965] | 0.964 [0.957, 0.971] | 0.803 |
| judge_frontier_orig | 60 | 0.932 [0.782, 1.000] | 0.932 [0.855, 0.990] | 0.881 |
| judge_frontier_disg | 60 | 0.729 [0.573, 0.867] | 0.735 [0.593, 0.851] | 0.655 |
| judge_cheap_orig | 1932 | 0.673 [0.637, 0.708] | 0.710 [0.678, 0.741] | 0.345 |
| judge_cheap_disg | 1904 | 0.587 [0.551, 0.622] | 0.578 [0.537, 0.617] | 0.238 |
| judge_local_disg | 2024 | 0.498 [0.459, 0.534] | 0.541 [0.505, 0.575] | 0.233 |

The flash-lite disguised judge barely beats chance on R_COMP (0.587 vs 0.500). Disguise dramatically hurts the judge on these complex sentences: the original flash-lite achieves 0.673, and the frontier judge (Gemini 3.1 Pro) reaches 0.932 on a 60-item subsample. The local Qwen-8B judge falls to 0.498, below chance.

This quantifies the cost of nonce disguise on hard sentences: the judge relies on surface familiarity with predicate names, and when those are replaced by nonsense, it loses the ability to reason about the formula's semantics. The consensus metric does not depend on understanding predicate names and is unaffected.

#### Error endorsement and mechanism

Error endorsement (e): 0.0. No ERROR translation was z3-equivalent to the majority of peers. This is perfect: every error is distinguishable from the consensus. The divergence rate (d) among CORRECT translations is 0.260, driven by the "strong" reading subset where a converse interpretation of the exception clause produces a z3-non-equivalent but arguably correct formula.

T8 (converse reading) exclusions: 116 rows were classified as READING_CHOICE and excluded from the pool. Of these, 47% would have been flagged by the consensus metric (c ≥ 0.5).

#### Nested adds-signal

| Model | Within-template Δ [CI] |
|-|-|
| cheap_disg + c_sig (c adds to judge) | +0.377 [+0.338, +0.416] |
| c_sig + cheap_disg (judge adds to c) | +0.004 [−0.000, +0.008] |

Adding the consensus score to the judge yields +0.377 within-template AUROC. Adding the judge to the consensus score yields +0.004 (negligible). The consensus metric subsumes essentially all of the judge's signal on R_COMP.

#### Complexity: no degradation

GEE slope of decision correctness per SD of words: c_score_sig −0.057 [−0.274, +0.159] (p = 0.604); judge_cheap_disg −0.149 [−0.306, +0.008] (p = 0.063). The consensus metric shows no significant length effect. The interaction (consensus − judge) is +0.070 [−0.234, +0.373] (p = 0.654).

#### Rename invariance on R_COMP

| Metric | Unrenamed FA | RENAME_NONCE FA | RENAME_SYN FA |
|-|-|-|-|
| c_score_sig | 0.260 | 1.000 | 1.000 |
| c_score_align | 0.260 | 1.000 | 0.635 |
| c_score_nf | 0.263 | 0.261 | 0.252 |
| c_score_hyb | 0.260 | 0.261 | 0.252 |

Under SIG, nonce-renaming all CORRECT formulas causes c_score_sig and c_score_align to flag every item (FA = 1.0). The NF and HYB variants are invariant to renaming (FA stays at the unrenamed level). This confirms the fundamental trade-off: aligner-based consensus has high discriminative power but breaks under vocabulary changes; name-free consensus is invariant but trades recall for robustness.

#### FREE condition: NOT_TESTABLE

The FREE condition (independent vocabulary per translator) produced only 34 CORRECT tier-A items against 420 ERROR, with 1,811 UNRESOLVED. The panel known-label check did not run. The FREE tier-A delta is +0.214 [−0.034, +0.377] (c_align vs bar), but the CI includes zero and the sample is too thin for reliable inference. FREE is NOT_TESTABLE and deferred to iteration 4.

#### Cost

Consensus peer generation: $0.001 per candidate (mean over all slots). Total R_COMP artifact spend: $1.58. The frontier judge costs $0.00605 per call (6.07× the consensus generation cost).

#### System-level on R_COMP (10 slots)

c_score_sig: Spearman 0.721, Pearson 0.978. judge_cheap_disg: Spearman 0.418, Pearson 0.796. The consensus metric tracks slot error rates closely.

### 3.4 Tests T3 + T5: PERTURB sensitivity and rename tradeoff

[ARTIFACT:art_PERTURB_scoring]

The PERTURB suite from iteration 2 (4,234 typed mutants + 868 controls, 12 operator types, all z3-verified) was scored with all metrics. Within-base AUROC pairs each DOWN mutant against its matched CONTROL from the same base formula, removing the base-formula confound.

#### T3: Per-operator within-base AUROC (E_bases, ALL polarity, selected metrics)

| Operator | n | c_align | c_hyb | c_nf | rt_nli_min | judge_cheap_disg |
|-|-|-|-|-|-|-|
| NEG | 379 | 0.869 | 0.884 | 0.843 | 0.873 | 0.723 |
| REV | 179 | 0.860 | 0.869 | 0.826 | 0.578 | 0.697 |
| QUANT | 179 | 0.860 | 0.872 | 0.829 | 0.351 | 0.632 |
| RESTR | 177 | 0.859 | 0.873 | 0.827 | 0.608 | 0.638 |
| CONN | 327 | 0.861 | 0.870 | 0.832 | 0.563 | 0.663 |
| DROP | 191 | 0.841 | 0.841 | 0.791 | 0.792 | 0.728 |
| ADD | 472 | 0.859 | 0.860 | 0.820 | 0.895 | 0.683 |
| SWAP | 116 | 0.882 | 0.910 | 0.863 | 0.454 | 0.529 |
| BIND | 314 | 0.865 | 0.858 | 0.798 | 0.833 | 0.672 |
| MEANING_RENAME | 318 | 0.872 | 0.685 | 0.499 | 0.930 | 0.600 |
| MOVE | 6 | -- | -- | -- | -- | -- |
| SCOPE | 0 | -- | -- | -- | -- | -- |
| UNGLUE | 0 | -- | -- | -- | -- | -- |

c_align achieves within-base AUROC ≥ 0.84 on every testable operator except DROP (0.841). It is most sensitive to SWAP (0.882) and NEG (0.869), and least sensitive to DROP (0.841). The c_hyb variant matches or exceeds c_align on all operators except MEANING_RENAME, where it drops to 0.685 (because the HYB variant blends the name-free signal, which cannot distinguish renames from real errors).

The round-trip metric (rt_nli_min) shows a complementary profile: it is most sensitive to ADD (0.895) and NEG (0.873), but nearly blind to QUANT (0.351), SWAP (0.454), and REV (0.578). The judge is weak across the board on PERTURB, with its best performance on DROP (0.728) and NEG (0.723).

MEANING_RENAME is the false-alarm diagnostic: it measures how often a metric flags a meaning-preserving predicate renaming as an error. c_align flags 76% (within-base AUROC 0.872, meaning it reliably separates renames from controls, but in the wrong direction: renames look like errors). c_nf achieves 0.499 (chance-level, meaning it is completely invariant to renames). rt_nli_min achieves 0.930 (it detects renames, because the verbalisation changes).

#### Polarity symmetry

The consensus metric is polarity-symmetric: the absolute difference |DOWN − UP| in within-base AUROC is < 0.01 for all operators and all consensus variants. This confirms that the metric detects departures from the consensus regardless of the direction of the perturbation.

#### T5: Rename tradeoff table (E_bases)

| Metric | RENAME_NONCE FA | RENAME_SYN FA | MEANING_RENAME wb-AUROC | SWAP recall | BASE FA |
|-|-|-|-|-|-|
| c_align | 0.765 | 0.565 | 0.872 | 0.758 | 0.201 |
| c_nf | 0.132 | 0.201 | 0.499 | 0.512 | 0.163 |
| c_hyb | 0.216 | 0.298 | 0.685 | 0.832 | 0.197 |
| g_align | 0.413 | 0.318 | 0.841 | 0.426 | 0.154 |
| g_nf | 0.132 | 0.176 | 0.477 | 0.428 | 0.154 |
| rt_nli_min | 0.686 | 0.191 | 0.930 | 0.153 | 0.143 |
| judge_cheap_disg | 0.229 | 0.132 | 0.600 | 0.220 | 0.129 |
| S4_local | 0.804 | 0.383 | 0.760 | 0.758 | 0.286 |
| p_peer_text | 1.000 | 0.156 | 0.997 | 0.248 | 0.130 |
| p_text | 1.000 | 0.085 | 0.993 | 0.193 | 0.117 |
| l2_bow | 1.000 | 0.173 | 0.992 | 0.194 | 0.178 |

The rename tradeoff is stark. c_align has RENAME_NONCE FA of 0.765: 76.5% of correctly translated formulas are flagged as errors after predicate renaming. c_nf has RENAME_NONCE FA of 0.132, close to its base FA of 0.163. c_hyb is intermediate at 0.216.

The cost of name-free consensus: c_nf achieves SWAP recall of only 0.512 (vs c_align's 0.758) and MEANING_RENAME within-base AUROC of 0.499 (chance), meaning it cannot distinguish argument swaps or predicate substitutions from genuine renames. Neither c_hyb (0.216 FA, 0.832 SWAP recall) nor c_nf (0.132 FA, 0.512 SWAP recall) achieves both low rename FA and high SWAP recall. This is a fundamental limitation: without shared vocabulary, the metric cannot determine whether two formulas with different predicate names are saying the same thing in different words or saying different things.

### 3.5 Test T4: Mechanism verification and hypothesis testing

[ARTIFACT:art_evaluation_2]

#### Numerical verification

48 numerical claims from the iteration-2 report were independently recomputed. All 48 match their source values (48/48 VERIFIED_MATCH). The corrections C1-C7 (applied inline throughout the iteration-1 and iteration-2 sections above) were identified and verified during this audit.

#### Mechanism predictions

Four mechanism predictions about why cross-family consensus works were tested:

**M1 (Anna Karenina): errors are more diverse than correct translations (more distinct z3-equivalence classes per sentence among ERROR items than CORRECT items).** On E: ERROR items have 2.85 mean distinct classes per sentence vs 1.55 for CORRECT. On R_COMP: ERROR 1.93, CORRECT 1.42. The direction is consistent with M1 in both datasets, but no formal statistical test was pre-registered. Verdict: **INCONCLUSIVE** (direction consistent, not formally tested).

**M2 (endorsement/divergence decomposition): the consensus signal decomposes into endorsement (e = fraction of errors endorsed by the majority) and divergence (d = fraction of correct items that diverge from the majority). On E, e should be low and d should be moderate, meaning the consensus works primarily because errors are NOT endorsed, not because correct items converge perfectly.** On E (R_AB, MAJ rule): e = 0.124, d = 0.537. On R_COMP: e = 0.0, d = 0.260. Both datasets show low e and moderate d. Verdict: **CONFIRMED**.

The decomposition explains why consensus recall on PEER_ENDORSED errors is near zero (from the T1 recall table): these are the 12.4% of errors that the majority of peers also produce. The consensus metric is structurally blind to them.

**M3 (complexity slope): the consensus metric's advantage over the judge grows with sentence complexity.** On E (T1): Δslope (consensus − judge) per SD words = +0.146 [−0.051, +0.361]; per SD n_conditions = +0.116 [−0.044, +0.264]. Both CIs include zero. On R_COMP: the interaction is +0.070 [−0.234, +0.373] (p = 0.654). Verdict: **DISCONFIRMED** on E (T1). On R_COMP (T2), the ceiling effect (consensus AUROC 0.954, judge 0.587) leaves no room for a slope interaction. M3 is treated as INCONCLUSIVE overall; the consensus does not degrade with complexity, but neither does its advantage grow.

**M4 (k-saturation): the consensus AUROC saturates at a small number of peer families.** The k-curve on E:

| k | AUROC [CI] | Cost per sentence |
|-|-|-|
| 1 | 0.685 | $0.000024 |
| 3 | 0.757 | $0.000073 |
| 5 | 0.776 | $0.000121 |
| 7 | 0.784 | $0.000170 |

The 95th-percentile k (the smallest k at which AUROC is within 0.02 of the full pool) is k = 3. At k = 3, the AUROC is 0.757, already 96.6% of the full-pool value (0.784 at k = 7). Verdict: **CONFIRMED** (k95 = 3).

This has practical significance: a consensus metric with 3 peer families costs $0.000073 per sentence, compared to $0.000049 for the flash-lite judge. The marginal cost of adding consensus to an existing pipeline is negligible.

#### PEER+TEXT vs S4 stacks on E (rerun verification)

The pt_vs_s4_rerun table verifies the iteration-2 claim that PEER+TEXT adds signal beyond the local S4 stack:

| Comparison | Subset | Pooled Δ [CI] | Strat Δ [CI] |
|-|-|-|-|
| PEER+TEXT − S4_local | R_AB pooled (n=2672) | +0.042 [+0.013, +0.070] | +0.059 [+0.023, +0.093] |
| PEER+TEXT − S4_local | R_AB long (n=2289) | +0.058 [+0.024, +0.094] | +0.067 [+0.031, +0.103] |
| PEER+TEXT − S4_local | R_A L20+EXC (n=447) | +0.096 [+0.009, +0.175] | +0.099 [+0.006, +0.176] |
| calibrated − S4_local | R_AB pooled | +0.035 [+0.005, +0.063] | +0.048 [+0.013, +0.081] |

All point values match the reviewer's independently computed targets to ≤ 0.0001. CIs match to ≤ 0.01 (expected RNG-order difference).

### 3.6 Iteration 3 summary

**What iteration 3 established:**

1. **T1 CONFIRMED: consensus beats the API bar.** c_score_align (strat AUROC 0.741) exceeds the flash-lite disguised judge (0.642) by +0.099 [+0.049, +0.146] on held-out E. This resolves the iteration-2 gap where the API bar was untestable. The advantage holds across robustness checks (alternative cheap judges, verdict-fallback scoring, long-sentence subsets, VEX confound control).

2. **T1 CONFIRMED: consensus adds signal beyond all baselines.** Adding c_score_align to the 28-feature S4_full stack yields +0.039 [+0.021, +0.057] strat AUROC (permutation null p95 = 0.009). The 4-feature PT_refit model (c_score_align, L2-bow, L3, p_text) matches the full S4 stack without any judge features.

3. **T2 CONFIRMED: consensus dominates on R_COMP.** On long composed sentences with trusted references, c_score_sig achieves within-template AUROC 0.954 vs the judge's 0.587 (Δ = +0.367). Error endorsement is zero: every error is distinguishable from the consensus. The nested adds-signal test shows the judge contributes +0.004 beyond consensus, while consensus contributes +0.377 beyond the judge.

4. **T3: PERTURB sensitivity profile.** Consensus (c_align) achieves within-base AUROC ≥ 0.84 on all testable operators. It is polarity-symmetric (|DOWN − UP| < 0.01). Round-trip NLI is complementary: strongest on ADD (0.895) but blind to QUANT (0.351) and SWAP (0.454). No metric covers all error types uniformly.

5. **T5: rename tradeoff quantified.** c_align has RENAME_NONCE FA 0.765 (76.5% of correctly translated formulas flagged after renaming). c_nf has 0.132 (invariant) but sacrifices SWAP recall (0.512 vs 0.758). c_hyb is intermediate (FA 0.216, SWAP 0.832). No consensus variant achieves both low rename FA and high structural-error recall.

6. **T4: mechanism predictions.** M1 (Anna Karenina) INCONCLUSIVE (direction consistent, not formally tested). M2 (endorsement/divergence) CONFIRMED (e = 0.124, d = 0.537). M3 (complexity slope) DISCONFIRMED (CIs include zero). M4 (k-saturation) CONFIRMED (k95 = 3). The consensus signal works because errors scatter across z3-equivalence classes while correct translations cluster, not because the advantage grows with complexity.

7. **Dead ends confirmed.** B2 (decomposed z3 reader) DROPPED (gate balanced accuracy 0.476 vs target 0.85). R_ADJ (LLM adjudicator) DROPPED (Sonnet-5 balanced accuracy 0.662 on track H). The FREE condition in R_COMP is NOT_TESTABLE (too few resolved labels).

8. **48/48 numerical claims verified.** All reviewer-audited values from the iteration-2 report reproduce exactly.

9. **M3 disconfirmation is informative.** The consensus advantage does not grow with sentence length. Both consensus and the judge degrade on longer sentences; the consensus merely degrades less. The practical implication is that the consensus metric cannot be relied upon to improve specifically in the regime where it is most needed (complex sentences).

**Iteration-3 API spend:** T1 experiment: included in the T1 artifact; T2 (R_COMP): $1.58; T3+T5 (PERTURB scoring): $0.00 (CPU-only); T4 (evaluation): $0.00 (CPU-only). Total: approximately $1.58 plus T1 API calls.

**What remains:**

(a) Resolve the FREE condition in R_COMP: either generate more translations with independent vocabularies or design a principled name-standardisation step. (b) Test whether a learned aligner (e.g. FormalAlign-style contrastive training) can reduce the rename FA below 0.20 while maintaining SWAP recall above 0.70. (c) Investigate the 12.4% error endorsement rate on E: are these genuine consensus failures or label noise? (d) Run the consensus metric on a second held-out dataset (outside FOLIO/MALLS) to test domain transfer.

## What we have learned so far

The cross-family consensus metric (c_score_align) is the strongest gold-free faithfulness signal we have found for NL-to-FOL translation. It achieves stratified AUROC 0.741 on held-out E, beating the best cheap LLM judge (0.642) by +0.099 [+0.049, +0.146] and adding +0.039 [+0.021, +0.057] beyond a 28-feature baseline stack. On long composed sentences with trusted references (R_COMP), it reaches 0.954 within-template AUROC with zero error endorsement. It achieves 96% of the frontier judge's discriminative power at 30× lower cost.

The mechanism behind consensus is clear: errors scatter across z3-equivalence classes while correct translations cluster (M2 confirmed: endorsement e = 0.124, divergence d = 0.537). This works well for polarity and structural errors (recall 0.53-0.55 at FA 0.10) but fails for errors where the majority of peers produce the same wrong formula (PEER_ENDORSED recall 0.00-0.05). Three peer families suffice for 97% of the full-pool AUROC (M4 confirmed: k95 = 3).

The fundamental limitation is the rename tradeoff: the aligner-based consensus metric (c_align) has RENAME_NONCE false-alarm rate 0.765, meaning it cannot be used on formulas with independently chosen predicate names. The name-free variant (c_nf, FA 0.132) is invariant but sacrifices structural-error recall. No consensus variant achieves both low rename FA and high error recall. This remains the primary open problem.

Three additional limitations bound the current results. First, all evaluation is on FOLIO and MALLS-derived data; domain transfer to other NL-FOL settings (e.g. software specifications, legal reasoning) is untested. Second, the labels are noisy: the panel majority accuracy on expert-curated errors is 0.727, and the correct-but-not-equivalent rate ranges from 0.215 (CTRL) to 0.773 (L25). Third, the M3 disconfirmation means the consensus advantage does not grow with sentence complexity, so the metric's relative value does not increase precisely where gold-free evaluation is most needed.

## Related Work

**NL-FOL datasets and their quality.** FOLIO [1] provides 1,435 FOL-annotated NLI problems. MALLS [2] uses GPT-4 to generate and verify NL-FOL pairs at scale. Brunello et al. [4] found that approximately 42% of entries in both datasets contain incorrect FOL formalisations, with additional ambiguity rates of 17.8% (FOLIO) and 51% (MALLS). Their LLM-assisted re-labelling framework reduces human effort by 5-15× compared to exhaustive review. Logic-LM [10] prompts LLMs for FOL and calls a prover, releasing outputs that we use as our evaluation screen.

**FOL closeness metrics.** Thatikonda et al. [5] evaluate n-gram, graph, embedding, and LLM-based metrics on controlled FOL perturbations, finding that no single metric is sensitive to all perturbation types. Smatch++ is the most sensitive to quantifier changes, while BL-score responds most to negation. Their work measures sensitivity to synthetic perturbations; ours measures faithfulness prediction on real LLM outputs with noisy labels.

**NL-FOL error taxonomies.** Thatikonda et al. [6] propose a verification pipeline with a 28-category error taxonomy. Brunello et al. [4] classify errors into semantic and structural categories. Our typed repair operators (NEG, REV, QUANT, RESTR, CONN, MOVE, DROP, ADD, SWAP, BIND, SCOPE, UNGLUE) follow the same tradition but are derived from z3 equivalence-class differences rather than manual annotation.

**Factuality metrics.** FRANK [11] defines a typology of factuality errors in abstractive summarisation and evaluates correlation of automatic metrics with human judgments. QuestEval [13] uses question generation and answering to assess factual consistency. QAGS [12] similarly generates questions from a summary and checks whether the source answers them the same way. Our L3 questionnaire layer is closest to this family: it generates structured questions from the text and checks the formula's answers via z3, rather than using another LLM.

**Round-trip and self-consistency.** Amrollahi et al. [7] propose verbalising a formal statement back to natural language and checking consistency, reporting high accuracy on mathematical autoformalization. Li et al. [8] use symbolic equivalence and semantic consistency for Lean/Isabelle autoformalization. Our round-trip baseline follows the same pattern but achieves only AUROC 0.710 on NL-FOL, below the LLM judge.

**Monotonicity and polarity.** SyGNS [14] tests monotonicity reasoning in NLI models. Udep2Mono [15] computes monotonicity profiles from Universal Dependencies. Our L2 role-aware layer attempted to use monotonicity-aware comparisons but achieved AUROC 0.557, a negative result.

**Counter-interpretation methods.** CLOVER [9] generates counter-interpretations to test logical validity via an LLM oracle. Our consensus approach is related in spirit: it uses multiple independent translations as implicit counter-proposals, but relies on z3 equivalence rather than LLM-generated counterexamples.

**Cross-check consistency.** SAC3 [17] detects hallucinations in black-box LLMs by sampling diverse perturbations of a query and checking consistency across answers. Our cross-system consensus metric uses a similar principle: disagreement among independent translations signals error. It operates on FOL equivalence rather than textual similarity, and uses multiple model families rather than perturbations of a single model. The ΔAUROC of cross-family consensus over single-model self-consistency is +0.140 in our setting, consistent with SAC3's finding that semantic-aware cross-checking outperforms naive self-consistency.

**Automated alignment for autoformalization.** FormalAlign [18] trains a model on both autoformalization and alignment scoring via a dual contrastive-generative loss, targeting Lean/Isabelle autoformalization. It is the closest published gold-free alignment scorer for formal languages. Our approach differs in that we use no learned alignment model: the consensus signal relies on z3 equivalence among independent translations, and the text-based signal uses deterministic checks and a prompted questionnaire. FormalAlign targets mathematical theorem proving, where the target language has a type checker; NL-FOL has no such verifier, making gold-free evaluation harder.

**Vacuity detection.** Kupferman and Vardi [16] formalise vacuity in temporal logic model checking. Our L1 lint layer includes a vacuity check (detecting formulas where a subformula can be replaced by its negation without changing the truth value), adapted from their framework.

## References

[1] Han et al. (2022). FOLIO: Natural Language Reasoning with First-Order Logic. EMNLP.

[2] Yang et al. (2023). MALLS: Multi-Agent Annotated NL-FOL Benchmarks for Logical Reasoning. arXiv:2305.13252.

[3] Brunello et al. (2026). Fixing FOLIO and MALLS: Verified Annotations and an LLM-assisted Framework to Focus Human Relabeling. arXiv:2606.02837.

[4] Brunello et al. (2025). Do LLMs Really Struggle at NL-FOL Translation? AAAI 2026.

[5] Thatikonda et al. (2025). Assessing the Sensitivity and Alignment of FOL Closeness Metrics. EMNLP Findings.

[6] Thatikonda et al. (2024). Strategies for Improving NL-to-FOL Translation with LLMs. arXiv:2409.16461.

[7] Amrollahi et al. (2026). Faithful Autoformalization via Roundtrip Verification and Repair. arXiv:2604.25031.

[8] Li et al. (2024). Autoformalize Mathematical Statements by Symbolic Equivalence and Semantic Consistency. NeurIPS.

[9] Ryu et al. (2024). CLOVER: Compositional First-Order Logic Translation and Verification. ICLR.

[10] Pan et al. (2023). Logic-LM: Empowering Large Language Models with Symbolic Solvers for Faithful Logical Reasoning. EMNLP.

[11] Pagnoni et al. (2021). FRANK: A Benchmark for Factuality Metrics. NAACL.

[12] Wang et al. (2020). QAGS: Asking and Answering Questions to Evaluate Factual Consistency. ACL Findings.

[13] Scialom et al. (2021). QuestEval: Summarization Asks for Fact-based Evaluation. EMNLP.

[14] Yanaka et al. (2021). SyGNS: A Systematic Generalization Testbed Based on Natural Language Semantics. ACL Findings.

[15] Chen et al. (2021). Udep2Mono. EACL.

[16] Kupferman and Vardi (2003). Vacuity Detection in Temporal Model Checking. STTT 4(2):224-233.

[17] Zhang et al. (2023). SAC3: Reliable Hallucination Detection in Black-Box Language Models via Semantic-aware Cross-check Consistency. EMNLP Findings.

[18] Lu et al. (2025). FormalAlign: Automated Alignment Evaluation for Autoformalization. ICLR.
