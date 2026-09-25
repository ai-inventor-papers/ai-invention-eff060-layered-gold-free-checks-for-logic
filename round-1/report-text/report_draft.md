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
|---|---|---|---|
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
|---|---|---|---|
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
|---|---|---|---|---|---|---|---|
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
|---|---|---|---|---|---|---|---|
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
|---|---|---|---|---|---|---|---|---|---|---|---|
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
|---|---|---|---|
| L | 753 | 693 | 0.920 |
| H | 302 | 279 | 0.924 |

Parse rates by system: gpt-3.5-turbo 0.889, gpt-4 0.946, text-davinci-003 0.921. Unparseable outputs are scored as p = 1 (maximum error probability) by the fused metric, so all items receive a score. The coverage gate (≥ 90%) passes.

#### Cost

L1 and L2 are free (CPU-only). L3 costs $0.175 per 1,000 calls with Gemini 2.5 Flash Lite. The total per-item cost is $0.0002, passing the $0.002 gate. CPU time (L1 + L2 + z3): median 35 ms, P95 90 ms. L3 latency: median 630 ms, P95 1.68 s.

#### Contamination check

L3 was run on nonce-disguised sentences (content words replaced by nonsense words) on the full track L. AUROC with exact text-formula alignment: 0.765; with disguised text: 0.770. Paired difference: −0.005 [−0.063, 0.049]. There is no evidence that the LLM benefits from having seen the public benchmark sentences.

#### Complexity strata (track L, fused score)

| Stratum | n (error/correct) | Testable | Fused AUROC | L2-bow AUROC | L3 AUROC |
|---|---|---|---|---|---|
| words < 12 | 443 (179/264) | Yes | 0.781 | 0.742 | 0.772 |
| words 12–19 | 31 (18/13) | No | 0.521 | 0.596 | 0.541 |
| words ≥ 20 | 3 (2/1) | No | 0.500 | 1.000 | 0.000 |
| 0 quantifiers | 302 (130/172) | Yes | 0.743 | 0.728 | 0.771 |
| 1 quantifier | 164 (65/99) | Yes | 0.794 | 0.748 | 0.721 |
| ≥ 2 quantifiers | 11 (4/7) | No | 0.750 | 0.768 | 0.607 |
| depth ≤ 1 | 296 (124/172) | Yes | 0.762 | 0.745 | 0.779 |
| depth 2–3 | 173 (73/100) | Yes | 0.756 | 0.717 | 0.710 |
| depth ≥ 4 | 8 (2/6) | No | 0.667 | 0.750 | 0.500 |
| 0 conditions | 344 (145/199) | Yes | 0.775 | 0.759 | 0.791 |
| 1–2 conditions | 131 (54/77) | Yes | 0.716 | 0.677 | 0.628 |

The frozen screen is dominated by short, simple sentences (93% under 12 words). The long and complex strata (12+ words, 2+ quantifiers, 3+ conditions) have too few items to test. This limitation motivates the held-out dataset (Artifact E), which oversamples these strata.

#### Per-system AUROC (descriptive, n = 3 systems)

| System | n | Error rate | Fused AUROC | L1 AUROC | L2-bow AUROC | L3 AUROC |
|---|---|---|---|---|---|---|
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
|---|---|---|---|
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

The c_score achieves the highest AUROC in the iteration at 0.866. It beats SC-5 (the self-consistency baseline) by ΔAUROC = +0.140 [0.085, 0.197]. Using only the six fresh peer translations (not the three Logic-LM systems) gives 0.872, slightly higher than using all peers. Restricting to the two other Logic-LM systems drops the AUROC to 0.753, showing that diversity across model families is essential.

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

The primary cheap judge (Gemini 2.5 Flash Lite, JSON 0–100 scoring, nonce-disguised sentences) achieves AUROC 0.777 [0.720, 0.827] on track L (n = 524, 230 errors, 294 correct).

#### Full baseline table (track L, ERROR vs CORRECT, n = 524)

| Metric | AUROC | 95% CI |
|---|---|---|
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
|---|---|---|
| S1 (structural) | 0.698 | [0.634, 0.761] |
| S2 (round-trip) | 0.687 | [0.625, 0.749] |
| S3 (judges disguised) | 0.771 | [0.705, 0.831] |
| S4 (all cheap features) | 0.817 | [0.762, 0.867] |
| S6 (S4 + local judges) | 0.810 | [0.753, 0.861] |

S4 (all cheap features combined via cross-fitted logistic regression) achieves 0.817. This is +0.039 [−0.010, 0.087] over the cheap judge alone, not significant, but it sets the empirical ceiling for cheap baselines.

#### Contamination analysis

No evidence of contamination was found for any judge. The difference-in-differences (DiD) test compares the disguise effect on track H (where the LLM could have memorised public gold) to track L (where it evaluates its own outputs, not memorisable). All DiD CIs include zero:

| Judge | DiD (H − L) | 95% CI |
|---|---|---|
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
|---|---|---|---|---|---|
| judge_cheap_orig | 0.27 | 0.12 | 0.23 | 0.64 | 0.29 |
| judge_cheap_disg | 0.44 | 0.12 | 0.46 | 0.41 | 0.39 |
| judge_cheap2_orig | 0.49 | 0.12 | 0.46 | 0.95 | 0.49 |
| rt_nli_min | 0.37 | 0.10 | 0.31 | 0.33 | 0.31 |
| rt_embed_cos | 0.57 | 0.07 | 0.44 | 0.38 | 0.44 |
| FOL-Triage fused | 0.013 | 0.0 | 0.061 | 0.0 | 0.013 |

FOL-Triage has the lowest flip rate of any metric tested. Judges and round-trip methods change their verdict on 29–49% of meaning-preserving rewrites.

#### Per-error-type sensitivity of judges (track H, curator view, n = 46 errors)

| Group | n | judge_cheap_orig | judge_cheap_disg | judge_cheap2_orig | rt_nli_min |
|---|---|---|---|---|---|
| 1-op errors | 13 | 0.308 | 0.538 | 0.462 | 0.231 |
| 2-op errors | 11 | 0.545 | 0.818 | 0.727 | 0.273 |
| ADD | 12 | 0.500 | 0.750 | 0.667 | 0.250 |
| COMPOUND | 22 | 0.545 | 0.864 | 0.773 | 0.273 |
| DROP | 11 | 0.455 | 0.636 | 0.455 | 0.182 |
| CONN | 3 | 0.667 | 0.667 | 1.000 | 0.333 |
| NEG | 2 | 0.500 | 0.500 | 1.000 | 0.500 |
| SWAP | 2 | 0.000 | 1.000 | 0.500 | 0.000 |

The disguised judge is more sensitive than the original judge for most error types, suggesting that nonce disguise forces the model to read more carefully.

#### Judge error-type classification accuracy

The judge's ability to name the correct error type is poor. On track-H 1-op errors, it identifies the correct repair operator 0% of the time (0/12). On 2-op errors, it is correct 45% (5/11). On track L, accuracy is 20% for 1-op and 27% for 2-op errors.

#### Complexity analysis (track L)

A logistic regression of judge correctness on standardised word count yields a coefficient of −0.48 (SE 0.11, p < 0.001): the judge is significantly less reliable on longer sentences. On track H (where longer sentences are available), the coefficient is −0.14 (SE 0.17, p = 0.41), consistent in direction but underpowered.

| Stratum | n (err/cor) | judge_cheap_disg AUROC | rt_nli_min AUROC |
|---|---|---|---|
| words < 12 | 485 (210/275) | 0.784 | 0.713 |
| words 12–19 | 36 (18/18) | 0.667 | 0.670 |
| quantifiers 0–1 | 512 (226/286) | 0.784 | 0.712 |
| depth ≤ 3 | 466 (199/267) | 0.781 | 0.702 |
| depth 4–5 | 54 (30/24) | 0.762 | 0.828 |
| 0 conditions | 394 (182/212) | 0.783 | 0.745 |
| 1–2 conditions | 128 (48/80) | 0.765 | 0.653 |

#### System-level descriptive statistics (3 systems, descriptive only)

| System | True error rate | Judge flag rate | rt_nli_min mean | Parse failures |
|---|---|---|---|---|
| gpt-3.5-turbo | 0.415 | 0.444 | 0.516 | 26/248 |
| gpt-4 | 0.385 | 0.362 | 0.496 | 10/282 |
| text-davinci-003 | 0.527 | 0.553 | 0.663 | 20/266 |

#### API outage and robustness

The shared OpenRouter key was exhausted at 13:29 UTC and restored at 15:11 UTC. During the outage, all LLM judges ran on the local RTX 4000 Ada GPU with the same prompts (Qwen3-8B, Llama-3.1-8B, Qwen3-14B-nf4). After the key was restored, the API judges were run and designated as primary; the local judges are kept as secondary rows. The local Qwen3-8B judge achieves AUROC 0.757 (disguised), comparable to the API flash-lite judge at 0.777.

### 1.5 Iteration 1 Summary

The four candidates and the bar:

| Method | AUROC | 95% CI | n | Cost/item | Rewrite flip rate |
|---|---|---|---|---|---|
| c_score (consensus) | 0.866 | [0.821, 0.906] | 546 | $0.0015/sent | 96% (RENAME) |
| S4 baseline combo | 0.817 | [0.762, 0.867] | 524 | varies | varies |
| **Bar: judge_cheap_disg** | **0.777** | **[0.720, 0.827]** | **524** | **$0.00004** | **0.39** |
| FOL-Triage fused | 0.759 | [0.695, 0.825] | 477 | $0.0002 | 0.013 |
| rt_nli_min | 0.710 | [0.648, 0.769] | 524 | $0.00001 | 0.31 |
| L1 lint | 0.508 | [0.499, 0.519] | 477 | $0 | 0.0 |
| Pilot structural | 0.50–0.53 | n/a | 524 | $0 | n/a |

[FIGURE:fig_summary_comparison]

**What iteration 1 established:**

1. The cross-system consensus metric (c_score = 1 − eq_frac) achieves the highest AUROC at 0.866, beating SC-5 by +0.140. It requires peer translations from multiple model families and is fundamentally non-invariant to predicate renaming (96% FA under RENAME).

2. The disguised cheap judge sets the bar at AUROC 0.777. The S4 combination of all cheap features reaches 0.817 (+0.039, not significant). The frontier judge (Gemini 3.1 Pro) adds nothing significant over the cheap judge.

3. FOL-Triage achieves AUROC 0.759, below the bar. Its primary value is invariance: the fused flip rate under meaning-preserving rewrites is 0.013, compared to 0.29–0.49 for judges. However, the fused false-alarm rate on CORRECT items is 0.194, exceeding the 0.10 calibration target.

4. L1 lint does not transfer from human annotation errors to LLM outputs. The pilot structural metrics are null. Round-trip NLI is 0.067 below the judge.

5. The evaluation labels are noisy: 58.8% of track-L "errors" are pure ADD+DROP (likely vocabulary mismatches). Iteration 2 will re-evaluate under panel-adjudicated labels from the held-out set.

6. No contamination was detected for any LLM-based metric.

**What remains for iteration 2:** (a) Re-evaluate all candidates under adjudicated labels from Artifact E. (b) Compute the paired ΔAUROC between FOL-Triage and the disguised judge on shared items. (c) Test whether combining the consensus metric with FOL-Triage or the judge produces a significant improvement. (d) Confirm on the held-out set.

## Related Work

**NL-FOL datasets and their quality.** FOLIO [1] provides 1,435 FOL-annotated NLI problems. MALLS [2] uses GPT-4 to generate and verify NL-FOL pairs at scale. Brunello et al. [4] found that approximately 42% of entries in both datasets contain incorrect FOL formalisations, with additional ambiguity rates of 17.8% (FOLIO) and 51% (MALLS). Their LLM-assisted re-labelling framework reduces human effort by 5–15× compared to exhaustive review. Logic-LM [10] prompts LLMs for FOL and calls a prover, releasing outputs that we use as our evaluation screen.

**FOL closeness metrics.** Thatikonda et al. [5] evaluate n-gram, graph, embedding, and LLM-based metrics on controlled FOL perturbations, finding that no single metric is sensitive to all perturbation types. Smatch++ is the most sensitive to quantifier changes, while BL-score responds most to negation. Their work measures sensitivity to synthetic perturbations; ours measures faithfulness prediction on real LLM outputs with noisy labels.

**NL-FOL error taxonomies.** Thatikonda et al. [6] propose a verification pipeline with a 28-category error taxonomy. Brunello et al. [4] classify errors into semantic and structural categories. Our typed repair operators (NEG, REV, QUANT, RESTR, CONN, MOVE, DROP, ADD, SWAP, BIND, SCOPE, UNGLUE) follow the same tradition but are derived from z3 equivalence-class differences rather than manual annotation.

**Factuality metrics.** FRANK [11] defines a typology of factuality errors in abstractive summarisation and evaluates correlation of automatic metrics with human judgments. QuestEval [13] uses question generation and answering to assess factual consistency. QAGS [12] similarly generates questions from a summary and checks whether the source answers them the same way. Our L3 questionnaire layer is closest to this family: it generates structured questions from the text and checks the formula's answers via z3, rather than using another LLM.

**Round-trip and self-consistency.** Amrollahi et al. [7] propose verbalising a formal statement back to natural language and checking consistency, reporting high accuracy on mathematical autoformalization. Li et al. [8] use symbolic equivalence and semantic consistency for Lean/Isabelle autoformalization. Our round-trip baseline follows the same pattern but achieves only AUROC 0.710 on NL-FOL, below the LLM judge.

**Monotonicity and polarity.** SyGNS [14] tests monotonicity reasoning in NLI models. Udep2Mono [15] computes monotonicity profiles from Universal Dependencies. Our L2 role-aware layer attempted to use monotonicity-aware comparisons but achieved AUROC 0.557, a negative result.

**Counter-interpretation methods.** CLOVER [9] generates counter-interpretations to test logical validity via an LLM oracle. Our consensus approach is related in spirit: it uses multiple independent translations as implicit counter-proposals, but relies on z3 equivalence rather than LLM-generated counterexamples.

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

[16] Kupferman and Vardi (2003). Vacuity Detection in Temporal Model Checking. STTT 4(2):224–233.
