# Corrected record and paper-ready fixes (iteration 5, eval 4)

Every number below is read by code from the file named in `numbers.csv` (row id in the HTML comment after it). Struck text (`~~…~~`) is quoted verbatim from `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_report_text/gen_report_text/paper_draft.md` with its line number; the marker gives the change and the source path. All E, R_COMP SIG and PERTURB numbers are DEVELOPMENT data.


## 0. What this record verified

244<!-- n:s0_nclaims --> claims checked; hypothesis text mismatching its source: 0<!-- n:s0_nhm -->. **Hypothesis text corrected by this artifact:** none: every hypothesis §0.2–§0.3 and review literal matches its file at the literal's precision.

**Paper-vs-file mismatches (15<!-- n:s0_npm -->)** — the values the iteration-4 paper prints differ from the source file (each is struck in the sections below):

| claim | quantity | paper prints | file value |
|-|-|-|-|
| `x9_csc` | `c_csc strat AUROC` | `[0.545, 0.679]` (L1063) | 0.614 [0.493, 0.736]<!-- n:x9_csc --> |
| `x9_fexact` | `FREE_exact (same 3 families) strat AUROC` | `[0.704, 0.827]` (L1060) | 0.770 [0.686, 0.844]<!-- n:x9_fexact --> |
| `x9_calign` | `c_score_align strat AUROC on PRIMARY` | `[0.711, 0.827]` (L1059) | 0.774 [0.682, 0.857]<!-- n:x9_calign --> |
| `x9_ppt` | `p_peer_text strat AUROC on PRIMARY` | `[0.742, 0.848]` (L1058) | 0.799 [0.700, 0.880]<!-- n:x9_ppt --> |
| `x9_s4` | `S4_full strat AUROC on PRIMARY` | `[0.672, 0.791]` (L1061) | 0.736 [0.635, 0.826]<!-- n:x9_s4 --> |
| `x9_flash` | `flash-lite disguised strat AUROC on PRIMARY` | `[0.592, 0.731]` (L1062) | 0.664 [0.568, 0.750]<!-- n:x9_flash --> |
| `x9_t9_COMPOUND_CSC` | `e_CSC on COMPOUND errors (PRIMARY)` | `0.643` (L1079) | 0.282<!-- n:x9_t9_COMPOUND_CSC --> |
| `x9_t9_COMPOUND_FREE_exact` | `e_FREE_exact on COMPOUND errors (PRIMARY)` | `0.246` (L1079) | 0.107<!-- n:x9_t9_COMPOUND_FREE_exact --> |
| `x9_g2` | `G2 overall verdict` | `FAIL` (L1092) | NOT_READ<!-- n:x9_g2 --> |
| `x9_m3_boot` | `M3 bootstrap Δslope CSC − flash-lite` | `[−0.417, −0.041]` (L1085) | −0.232 [−0.770, −0.023]<!-- n:x9_m3_boot --> |
| `rv_spend3` | `§3.6 iteration-3 spend statement vs ledger sum` | `1.58` (L1023) | $4.33<!-- n:rv_spend3 --> |
| `rv_k3_cost` | `§3.5 k=3 $ per sentence (paper says $0.000073)` | `0.000073` (L980) | $0.000946<!-- n:rv_k3_cost --> |
| `rv_frontier_x` | `frontier judge $/item ÷ consensus $/item (per ITEM; §3.3's '6.07×' mixed units)` | `6.07` (L895) | 30.2<!-- n:rv_frontier_x --> |
| `rv_k1_cost` | `§3.5 k=1 cost column (paper says $0.000024 per sentence)` | `0.000024` (L979) | $0.000315<!-- n:rv_k1_cost --> |
| `rv_k7_cost` | `§3.5 k=7 cost column (paper says $0.000170 per sentence)` | `0.000170` (L982) | $0.002206<!-- n:rv_k7_cost --> |

Sources: `numbers.csv`; `mismatches.csv`


## 1. §3.4 PERTURB sensitivity and the rename trade-off (corrected)

Replaces: paper_draft.md `### 3.4 Tests T3 + T5: PERTURB sensitivity and rename tradeoff`, lines 901-954

~~MEANING_RENAME is the false-alarm diagnostic: it measures how often a metric flags a meaning-preserving predicate renaming as an error.~~ [Correction, iter 4: MEANING_RENAME replaces a predicate by one with a DIFFERENT meaning; it is an ERROR operator, not a meaning-preserving rewrite. A within-base AUROC near chance on it means the metric is BLIND to a real error class (c_nf 0.499<!-- n:e8_cnf_mr -->), not that it is rename-invariant; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/perturb_corrected.csv] (paper_draft.md L929)

~~The consensus metric is polarity-symmetric: the absolute difference |DOWN − UP| in within-base AUROC is < 0.01 for all operators and all consensus variants.~~ [Correction, iter 4: deleted: per-operator consensus within-base AUROC is a base-endorsement artefact (most mutants of a flagged base sit at the maximum score), so neither an operator ranking nor a polarity-symmetry claim can be read from it; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/perturb_corrected.csv] (paper_draft.md L933)

~~c_align achieves within-base AUROC ≥ 0.84 on every testable operator except DROP (0.841).~~ [Correction, iter 4: no per-operator ranking is reported for consensus scores (artefact above); the recall at the PRIMARY threshold is flat across operators (c_align NEG 0.761<!-- n:pc_calign_recall_NEG -->, SWAP 0.758<!-- n:pc_calign_recall_SWAP -->, DROP 0.721<!-- n:pc_calign_recall_DROP -->, ADD 0.763<!-- n:pc_calign_recall_ADD -->, MEANING_RENAME 0.762<!-- n:pc_calign_recall_MEANING_RENAME -->); source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/perturb_corrected.csv] (paper_draft.md L925)

~~It is polarity-symmetric (|DOWN − UP| < 0.01).~~ [Correction, iter 4: deleted (same artefact); source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/perturb_corrected.csv] (paper_draft.md L1011)

**Corrected text.** The eval-3 note on the source table reads verbatim: "MEANING_RENAME is typed as an ERROR operator; per-operator consensus AUROC is an ARTEFACT (94-100% of mutants at c=1); rt_nli_min_LOCAL = local NLI round-trip"<!-- v:perturb_corrected.csv -->. MEANING_RENAME is therefore typed as an ERROR operator throughout. The name-free score `c_nf` is blind to it (within-base AUROC 0.499<!-- n:e8_cnf_mr -->), which, together with the failed pre-registered selection below, is what ended the name-free line.

**Invariance on meaning-preserving renames of CORRECT E bases** (FA = share flagged; the paired base FA and the flip rate separate rename sensitivity from base over-flagging; development data):

| metric | NONCE FA [CI] | NONCE base FA | NONCE flip | SYN FA [CI] | SYN base FA | SYN flip |
|-|-|-|-|-|-|-|
| `c_align` | 0.765 [0.765, 0.765]<!-- n:pc_c_align_RENAME_NONCE_fa --> | 0.160<!-- n:pc_c_align_RENAME_NONCE_base --> | 0.605<!-- n:pc_c_align_RENAME_NONCE_flip --> | 0.565 [0.487, 0.634]<!-- n:pc_c_align_RENAME_SYN_fa --> | 0.252<!-- n:pc_c_align_RENAME_SYN_base --> | 0.313<!-- n:pc_c_align_RENAME_SYN_flip --> |
| `c_nf` | 0.132 [0.090, 0.175]<!-- n:pc_c_nf_RENAME_NONCE_fa --> | 0.132<!-- n:pc_c_nf_RENAME_NONCE_base --> | 0.000<!-- n:pc_c_nf_RENAME_NONCE_flip --> | 0.201 [0.148, 0.254]<!-- n:pc_c_nf_RENAME_SYN_fa --> | 0.201<!-- n:pc_c_nf_RENAME_SYN_base --> | 0.000<!-- n:pc_c_nf_RENAME_SYN_flip --> |
| `c_hyb` | 0.216 [0.146, 0.285]<!-- n:pc_c_hyb_RENAME_NONCE_fa --> | 0.139<!-- n:pc_c_hyb_RENAME_NONCE_base --> | 0.077<!-- n:pc_c_hyb_RENAME_NONCE_flip --> | 0.298 [0.212, 0.385]<!-- n:pc_c_hyb_RENAME_SYN_fa --> | 0.270<!-- n:pc_c_hyb_RENAME_SYN_base --> | 0.029<!-- n:pc_c_hyb_RENAME_SYN_flip --> |
| `judge_cheap_disg` | 0.229 [0.194, 0.264]<!-- n:pc_judge_cheap_disg_RENAME_NONCE_fa --> | 0.109<!-- n:pc_judge_cheap_disg_RENAME_NONCE_base --> | 0.134<!-- n:pc_judge_cheap_disg_RENAME_NONCE_flip --> | 0.085 [0.054, 0.121]<!-- n:pc_judge_cheap_disg_RENAME_SYN_fa --> | 0.099<!-- n:pc_judge_cheap_disg_RENAME_SYN_base --> | 0.058<!-- n:pc_judge_cheap_disg_RENAME_SYN_flip --> |
| `p_peer_text` | 1.000 [1.000, 1.000]<!-- n:pc_p_peer_text_RENAME_NONCE_fa --> | 0.179<!-- n:pc_p_peer_text_RENAME_NONCE_base --> | 0.821<!-- n:pc_p_peer_text_RENAME_NONCE_flip --> | 0.216 [0.136, 0.307]<!-- n:pc_p_peer_text_RENAME_SYN_fa --> | 0.136<!-- n:pc_p_peer_text_RENAME_SYN_base --> | 0.080<!-- n:pc_p_peer_text_RENAME_SYN_flip --> |
| `p_text` | 1.000 [1.000, 1.000]<!-- n:pc_p_text_RENAME_NONCE_fa --> | 0.109<!-- n:pc_p_text_RENAME_NONCE_base --> | 0.891<!-- n:pc_p_text_RENAME_NONCE_flip --> | 0.068 [0.023, 0.125]<!-- n:pc_p_text_RENAME_SYN_fa --> | 0.068<!-- n:pc_p_text_RENAME_SYN_base --> | 0.000<!-- n:pc_p_text_RENAME_SYN_flip --> |
| `l3_z3` | 0.385 [0.296, 0.473]<!-- n:pc_l3_z3_RENAME_NONCE_fa --> | 0.109<!-- n:pc_l3_z3_RENAME_NONCE_base --> | 0.276<!-- n:pc_l3_z3_RENAME_NONCE_flip --> | 0.023 [0.000, 0.057]<!-- n:pc_l3_z3_RENAME_SYN_fa --> | 0.023<!-- n:pc_l3_z3_RENAME_SYN_base --> | 0.000<!-- n:pc_l3_z3_RENAME_SYN_flip --> |
| `S4_local` | 0.804 [0.732, 0.875]<!-- n:pc_S4_local_RENAME_NONCE_fa --> | 0.241<!-- n:pc_S4_local_RENAME_NONCE_base --> | 0.616<!-- n:pc_S4_local_RENAME_NONCE_flip --> | 0.364 [0.273, 0.466]<!-- n:pc_S4_local_RENAME_SYN_fa --> | 0.193<!-- n:pc_S4_local_RENAME_SYN_base --> | 0.239<!-- n:pc_S4_local_RENAME_SYN_flip --> |

**Pre-registered rename-invariant selection FAILED** (exp 8 `selection.json`; the pre-registered selection rule uses FA only, no paired flip): HYB PERTURB RENAME_SYN / NONCE FA 0.841<!-- n:e8_hyb_syn --> / 0.700<!-- n:e8_hyb_nonce -->; NF-anchored 0.686<!-- n:e8_nf_syn --> / 0.485<!-- n:e8_nf_nonce -->; both INELIGIBLE, nothing was frozen.

**Coverage (T11).** 3,419<!-- n:e8_cov_ok --> of 5,402<!-- n:e8_cov_n --> PERTURB rows were scored by the consensus family; the rest are R_COMP rows without peers or rows whose peers were unavailable, counted, not dropped.

Sources: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/perturb_corrected.csv`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/perturb_sensitivity.csv`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/selection.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/coverage_perturb.csv`


## 2. §3.3 T2 on R_COMP: NOT CONFIRMED (corrected)

Replaces: paper_draft.md `### 3.3 Test T2: R_COMP (long composed sentences)`, lines 823-900

~~**T2 CONFIRMED: consensus dominates on R_COMP.** On long composed sentences with trusted references, c_score_sig achieves within-template AUROC 0.954 vs the judge's 0.587 (Δ = +0.367).~~ [Correction, iter 4: T2 is NOT CONFIRMED under the §3.1 rule: SIG passes (within-template 0.954<!-- n:t2_sig --> vs 0.587<!-- n:t2_judge -->; vs the ORIGINAL judge +0.278<!-- n:t2_vs_orig -->) but SIG is the controlled-vocabulary regime the user excluded, and FREE was NOT_TESTABLE; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/t2_record.csv] (paper_draft.md L1009)

~~The FREE tier-A delta is +0.214 [−0.034, +0.377] (c_align vs bar), but the CI includes zero and the sample is too thin for reliable inference.~~ [Correction, iter 4: the FREE tier-A deltas in this section are VOID: those labels over-call ERROR (297<!-- n:t2_free_mapped --> of 420<!-- n:t2_free_err --> old ERROR rows are MAPPED by the name-free search); source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results/old_label_agreement.json] (paper_draft.md L891)

~~The frontier judge costs $0.00605 per call (6.07× the consensus generation cost).~~ [Correction, iter 4: unit error: per ITEM the frontier judge costs 30.2<!-- n:rv_frontier_x -->× the consensus score (FULL, per candidate); see the single cost table (section 13); source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/cost_units.csv] (paper_draft.md L895)

**Corrected text.** On R_COMP SIG (out-of-scope controlled vocabulary; development data) `c_score_sig` reaches within-template AUROC 0.954<!-- n:t2_sig --> against the disguised flash-lite judge's 0.587<!-- n:t2_judge -->; against the ORIGINAL (undisguised) judge the gap is +0.278<!-- n:t2_vs_orig -->. This is the regime the user excluded, so it cannot confirm the operating condition. The in-scope FREE condition was NOT_TESTABLE in iteration 3, and the iteration-3 FREE tier-A labels were later shown to over-call ERROR (UP TO 70.7%<!-- n:d5_707 --> of old ERROR rows are MAPPED; MAPPED is an upper bound of CORRECT). Verdict: **T2 NOT CONFIRMED**; criterion (c) is pending on R_COMP FREE in iteration 5 (`confirm_verdict_rcomp.json`).

Sources: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/t2_record.csv`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results/old_label_agreement.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/cost_units.csv`


## 3. §3.5 Mechanism verdicts under the PRE-REGISTERED definitions (corrected)

Replaces: paper_draft.md `### 3.5 Test T4: Mechanism verification and hypothesis testing`, lines 955-1000

~~**M1 (Anna Karenina): errors are more diverse than correct translations (more distinct z3-equivalence classes per sentence among ERROR items than CORRECT items).** On E: ERROR items have 2.85 mean distinct classes per sentence vs 1.55 for CORRECT. On R_COMP: ERROR 1.93, CORRECT 1.42. The direction is consistent with M1 in both datasets, but no formal statistical test was pre-registered. Verdict: **INCONCLUSIVE** (direction consistent, not formally tested).~~ [Correction, iter 4: M1 was pre-registered and tested; its pre-registered text is given below with verdict INCONCLUSIVE; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/prereg_mech.json] (paper_draft.md L967)

~~**M2 (endorsement/divergence decomposition): the consensus signal decomposes into endorsement (e = fraction of errors endorsed by the majority) and divergence (d = fraction of correct items that diverge from the majority). On E, e should be low and d should be moderate, meaning the consensus works primarily because errors are NOT endorsed, not because correct items converge perfectly.** On E (R_AB, MAJ rule): e = 0.124, d = 0.537. On R_COMP: e = 0.0, d = 0.260. Both datasets show low e and moderate d. Verdict: **CONFIRMED**.~~ [Correction, iter 4: M2 is pre-registered as a slope claim (CONFIRMED but non-specific), not the e/d bookkeeping identity; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/tables/hypothesis_verdicts.csv] (paper_draft.md L969)

~~| 1 | 0.685 | $0.000024 |~~ [Correction, iter 4: the cost column was per-candidate arithmetic mislabelled as per sentence; per-sentence k-pool costs are in the table below; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/cost_units.csv] (paper_draft.md L979)

~~This has practical significance: a consensus metric with 3 peer families costs $0.000073 per sentence, compared to $0.000049 for the flash-lite judge.~~ [Correction, iter 4: unit error: a 3-family pool costs $0.000946<!-- n:cost_k3 --> per SENTENCE (FULL), vs flash-lite $4.9e-5<!-- n:cost_flash --> per item-call; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/cost_units.csv] (paper_draft.md L986)

**Corrected text (pre-registered definitions, eval 2 `prereg_mech.json`; development data E):**

- **M1** "peer-endorsement rate among errors falls with n_conditions (GEE slope < 0, CI excludes 0)"<!-- v:hypothesis_verdicts.csv -->: **INCONCLUSIVE<!-- n:ev2_m1 -->**.
- **M2** "divergence among CORRECT rows rises with words"<!-- v:hypothesis_verdicts.csv -->: **CONFIRMED but non-specific**: the shuffled-label placebo also passes (eval-2 README), so M2 alone does not show a label-specific mechanism.
- **M3** "consensus length slope less negative than the API judge's (difference CI > 0)"<!-- v:hypothesis_verdicts.csv -->: owned by T1, where it is **INCONCLUSIVE** because its two specifications conflict (bootstrap +0.146 [−0.051, 0.361]<!-- n:t1_m3_boot --> (n.s.: CI covers 0) vs stacked GEE +0.274 [0.190, 0.359]<!-- n:t1_m3_gee -->); the local-judge version (M3-local) is secondary.
- **M4** "k needed to reach 95% of the full-pool AUROC is <= 5 families"<!-- v:hypothesis_verdicts.csv -->: **CONFIRMED**, k95 = 3<!-- n:ev2_k95 --> overall; by words tercile k95 = 2<!-- n:ev2_k95_t1 --> / 3<!-- n:ev2_k95_t2 --> / 5<!-- n:ev2_k95_t3 -->: long sentences need more peers.
- **NET** Δ(e+d), words T3 − T1: +0.356 [0.198, 0.493]<!-- n:ev2_net -->: consensus DEGRADES with length, driven by d (Δd +0.608<!-- n:ev2_net_dd -->, Δe −0.252<!-- n:ev2_net_de -->).
- **SCATTER** SI_cor / SI_err 4.45 [3.57, 5.77]<!-- n:ev2_scatter -->; graded − binary AUROC +0.114 [0.091, 0.140]<!-- n:ev2_graded -->.

| k | AUROC | AUROC words T3 | $ per SENTENCE (FULL, peer generation) |
|-|-|-|-|
| 1 | 0.685<!-- n:ev2_k1 --> | 0.581<!-- n:ev2_k1_T3 --> | $0.000315<!-- n:cost_k1 --> |
| 3 | 0.757<!-- n:ev2_k3 --> | 0.651<!-- n:ev2_k3_T3 --> | $0.000946<!-- n:cost_k3 --> |
| 5 | 0.776<!-- n:ev2_k5 --> | 0.698<!-- n:ev2_k5_T3 --> | $0.001576<!-- n:cost_k5 --> |
| 7 | 0.784<!-- n:ev2_k7 --> | 0.726<!-- n:ev2_k7_T3 --> | $0.002206<!-- n:cost_k7 --> |

Sources: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/results/part_a.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/tables/hypothesis_verdicts.csv`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/prereg_mech.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/README.md`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/cost_units.csv`


## 4. Iteration-1/2 corrections applied in place

Replaces: the listed sentences in paper_draft.md §1.4, §1.5 and §2.5 (line numbers in each marker).

- ~~The ΔAUROC over the cheap judge is +0.024 [−0.075, 0.111], not significant.~~ [Correction, iter 4: C4: under panel labels the frontier-judge advantage STRENGTHENS (see corrections_iter12.csv row C4); source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/corrections_iter12.csv] (paper_draft.md L274)

- ~~The frontier judge (Gemini 3.1 Pro) adds nothing significant over the cheap judge.~~ [Correction, iter 4: C4: the frontier advantage is n.s. only under solver labels; under panel labels it STRENGTHENS; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/corrections_iter12.csv] (paper_draft.md L385)

- ~~The frontier judge advantage is large under adjudicated labels (+0.166 AUROC over the cheap judge under R_ADJ_AB, p < 0.001), reversing the non-significant iteration-1 finding under solver labels.~~ [Correction, iter 4: 'reversing' overstates: the iteration-1 solver-label advantage was already positive; the panel-label result STRENGTHENS it (C4); source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/corrections_iter12.csv] (paper_draft.md L572)

- [Correction, iter 4: the common-set size must be read from evaluation 1's tables (corrections_iter12.csv); source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/corrections_iter12.csv] (original sentence not found in paper_draft.md)

- ~~(d) Re-fit the PEER+TEXT fusion under R_ADJ labels (the current fusion was fitted under solver labels, which penalise it).~~ [Correction, iter 4: the fused score was calibrated on track H, not 'fitted under solver labels' (corrections_iter12.csv); source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/corrections_iter12.csv] (paper_draft.md L624)

The corrections table (verbatim; every row machine-verified by eval 3 against its source path):

| id | claim_as_reported | corrected_value | verified |
|-|-|-|-|
| C1a | iteration-2 report: contamination DiD on E not reported for exp 6 (only exp 5's orig-vs-disg delta) | Llama-8B DiD +0.162 [0.064, 0.261] | True |<!-- v:corrections_iter12.csv -->
| C1b | same | Qwen-8B DiD +0.036 [-0.039, 0.111] n.s., MDE 0.107 | True |<!-- v:corrections_iter12.csv -->
| C1c | exp 5 contamination arm: disguise IMPROVES the Qwen judge on E (orig - disg) | -0.064 [-0.098, -0.032] | True |<!-- v:corrections_iter12.csv -->
| C2_R_SOLVER_CONS | report: disguise 'forces structural reading' (disguised judge better) | ORIGINAL judge ahead at matched FA 0.10: recall orig - disg +0.106 [0.033, 0.178] (R_SOLVER_CONS) | True |<!-- v:corrections_iter12.csv -->
| C2_R_ADJ_AB | report: disguise 'forces structural reading' (disguised judge better) | ORIGINAL judge ahead at matched FA 0.10: recall orig - disg +0.198 [0.130, 0.260] (R_ADJ_AB) | True |<!-- v:corrections_iter12.csv -->
| C3 | report: fusion fit on AGREE items (screen) 0.943 presented as the fused metric's quality | screen AGREE-item fusion OOF AUROC 0.943 shrinks to held-out E R_AB 0.790 | True |<!-- v:corrections_iter12.csv -->
| C4 | report: frontier-judge advantage weakens under panel labels | STRENGTHENS: solver labels +0.077 [0.006, 0.154] -> panel A+B +0.166 [0.08577985739750449, 0.24360389976262184] n=90 | True |<!-- v:corrections_iter12.csv -->
| C5 | report: P1 group names mixed (PEER_ENDORSED vs PEER_ENDORSED_NF); judge column omitted | local judge recall at FA 0.10: PEER_ENDORSED 0.169, PEER_ENDORSED_NF 0.199 (highest recall on both endorsed groups) | True |<!-- v:corrections_iter12.csv -->
| C6 | report: P4 compared fused RENAME FA 0.385 with FOL-Triage '0.013' | FA vs FA: PEER+TEXT fused RENAME FA 0.385 vs FOL-Triage fused RENAME FA 0.22; 0.013 was FOL-Triage's FLIP rate (0.0133) | True |<!-- v:corrections_iter12.csv -->
| C7 | iteration-2 report spend statement | total $4.229 = exp5 (costs.jsonl judge 0.0008 + E_l3_q.jsonl L3 0.1544; README states $0.155) $0.155 + exp6 (analysis_E.json api_spend_total_usd) $0.000 + dataset2 (cost_ledger.jsonl sum cost_usd) $3.660 + dataset3 (cost_ledger.jsonl sum cost_usd) $0.414 + eva… | True |<!-- v:corrections_iter12.csv -->

Sources: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/corrections_iter12.csv`


## 5. Placeholder → real artifact IDs

Replaces: every `[ARTIFACT:...]` marker in paper_draft.md (16<!-- n:ids_total --> markers; 4<!-- n:ids_resolved --> placeholders resolved from `artifact_id_map.csv`, 0<!-- n:ids_unresolved --> unresolved; no ID is invented).

| paper line | marker | replacement | status |
|-|-|-|-|
| L21 | `art_U4Hsqt4Ay9Tg` | `art_U4Hsqt4Ay9Tg` | VALID |
| L27 | `art_d0njuqy2Csj-` | `art_d0njuqy2Csj-` | VALID |
| L180 | `art_i3cVDxBp-USk` | `art_i3cVDxBp-USk` | VALID |
| L223 | `art_elDZY26Pu6GD` | `art_elDZY26Pu6GD` | VALID |
| L407 | `art_TaxJRnPcJMuZ` | `art_TaxJRnPcJMuZ` | VALID |
| L482 | `art_HepAw8c6Eu7-` | `art_HepAw8c6Eu7-` | VALID |
| L533 | `art_zcwCQgTqk6DN` | `art_zcwCQgTqk6DN` | VALID |
| L640 | `art_T1_API_bar` | `art_7GxreYjATkC5` | RESOLVED |
| L825 | `art_R_COMP` | `art_cxnoDYQNFolW` | RESOLVED |
| L903 | `art_PERTURB_scoring` | `art_YYD-HDzfQfEj` | RESOLVED |
| L957 | `art_evaluation_2` | `art_FWy8D4_y9GBn` | RESOLVED |
| L1039 | `art_D7k2ZWgE3nVd` | `art_D7k2ZWgE3nVd` | VALID |
| L1109 | `art_pAmLrGqsmFUx` | `art_pAmLrGqsmFUx` | VALID |
| L1186 | `art_2OmxzMInZZJY` | `art_2OmxzMInZZJY` | VALID |
| L1204 | `art_Ia_FT284H33j` | `art_Ia_FT284H33j` | VALID |
| L1233 | `art_BvAL_KZTZuw8` | `art_BvAL_KZTZuw8` | VALID |

Sed-ready list (run in the paper directory):

```
sed -i '640s/\[ARTIFACT:art_T1_API_bar\]/[ARTIFACT:art_7GxreYjATkC5]/' paper_draft.md
sed -i '825s/\[ARTIFACT:art_R_COMP\]/[ARTIFACT:art_cxnoDYQNFolW]/' paper_draft.md
sed -i '903s/\[ARTIFACT:art_PERTURB_scoring\]/[ARTIFACT:art_YYD-HDzfQfEj]/' paper_draft.md
sed -i '957s/\[ARTIFACT:art_evaluation_2\]/[ARTIFACT:art_FWy8D4_y9GBn]/' paper_draft.md
```

Artifacts with NO marker in the paper (the paper step must add one where their results are cited): `art_VIF75I5R6f0v`. The research artifact `art_VIF75I5R6f0v` gets its own section (section 7 below).

Sources: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_report_text/gen_report_text/paper_draft.md`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/artifact_id_map.csv`


## 6. §3.7 Hypothesis verdicts (new section)

Insert after §3.6. Iteration-3 rows verbatim from eval 3 Part 4:

| clause | corrected_verdict_iter4_hypothesis | reason |
|-|-|-|
| T1(a) | CONFIRMED on development E; L25 n.s. | L25 stratum not significant (+0.069 [-0.020, 0.148]); E is development data |<!-- v:hypothesis_verdicts_iter3.csv -->
| T1(b) | CONFIRMED (nested only) |  |<!-- v:hypothesis_verdicts_iter3.csv -->
| T1(c) | SIG PASS / FREE NOT_TESTABLE, so NOT CONFIRMED | FREE NOT_TESTABLE (34 CORRECT tier-A rows) -> by the §3.1 rule NOT CONFIRMED |<!-- v:hypothesis_verdicts_iter3.csv -->
| T1(d) | point estimate only | ratio 0.957 meets 0.95 on the point estimate only (CI 0.887-1.034) |<!-- v:hypothesis_verdicts_iter3.csv -->
| T1(e) rename invariance | FAILED |  |<!-- v:hypothesis_verdicts_iter3.csv -->
| M1 | INCONCLUSIVE |  |<!-- v:hypothesis_verdicts_iter3.csv -->
| M2 | CONFIRMED, non-specific | shuffled-label placebo gives +1.75 [1.04, 2.45] (non-specific) |<!-- v:hypothesis_verdicts_iter3.csv -->
| M3 (specifications conflict) | INCONCLUSIVE (specifications conflict) | exp 6 says DISCONFIRMED from the bootstrap spec; the stacked-GEE spec gives +0.274 [0.190, 0.359] |<!-- v:hypothesis_verdicts_iter3.csv -->
| M4 | CONFIRMED |  |<!-- v:hypothesis_verdicts_iter3.csv -->
| NET | degrades |  |<!-- v:hypothesis_verdicts_iter3.csv -->
| Typing | at judge level (negative) |  |<!-- v:hypothesis_verdicts_iter3.csv -->

Iteration-4 rows (development data E / PERTURB; PROVISIONAL where stated):

| clause | verdict | source |
|-|-|-|
| CSC G1 (d ≤ `0.35` AND non-positive words slope) | FAIL: d 0.139<!-- n:x9_g1_d -->, slope +1.25 [0.41, 2.09]<!-- n:x9_g1_slope --> | `csc_gate_E.json` |
| CSC G2 (`strat AUROC(CSC) ≥ c_score_align − 0.01` on R_AB AND pooled AUROC(CSC) > c_score_align on L25) | NOT_READ (NOT_READ<!-- n:x9_g2 -->): R_AB part FAIL; L25 cell below `50/50` (Δ −0.067 [−0.183, 0.040]<!-- n:x9_g2_l25 -->, not read) | `csc_gate_E.json` |
| CSC G3-E (RENAME_SYN FA gate, flip not computed) | NOT_RUN<!-- n:x9_g3 --> | `csc_gate_E.json` |
| CSC G4 | null on E (sibling arm) | `csc_gate_E.json` |
| CSC G5 (FULL $/candidate ≤ `$0.002`) | PASS (PROVISIONAL): $5.25e-4<!-- n:x9_g5 --> per candidate; deduped $2.76e-4<!-- n:x9_g5_dd --> | `csc_gate_E.json`, `results/analysis.json g_cost` |
| exp-10 G3-P / G4 / MT | UNTESTED (0 CSC peers generated; budget) — G3_P: UNTESTED: no CSC peer could be generated (OpenRouter run budget exhausted before the first call; D-BUDGET); G4: UNTESTED: no CSC peer could be generated (OpenRouter run budget exhausted before the first call; D-BUDGET); MT: UNTESTED: no CSC peer could be generated (OpenRouter run budget exhausted before the first call; D-BUDGET)<!-- v:csc_gate_P.json --> | `csc_gate_P.json` |
| E2 confirmation cells | NOT TESTABLE (0<!-- n:d4_cor --> CORRECT rows) | `testability_E2.json`, `sealed/labels_E2.jsonl` |
| R_COMP FREE criterion (c) | NOT TESTABLE (0<!-- n:d5_cor --> CORRECT rows; gloss not run) | `testability_FREE_v2.json` |

Sources: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/hypothesis_verdicts_iter3.csv`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/csc_gate_E.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/results/csc_gate_P.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/testability_E2.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results/testability_FREE_v2.json`


## 7. Prior-art positioning [ARTIFACT:art_VIF75I5R6f0v] (new section)

Insert as §3.x. The research artifact's scoop rule, neighbour table and C1–C5 verdicts, verbatim from eval 3 `prior_art.csv` (built from `research_report.md`):

| section | line |
|-|-|
| C-claims | Prior-art positioning (web research, $0 LLM spend, 63 sources, 139 verbatim quotes machine-checked against fetched text) for the iteration-3 claim that cross-family solver consensus is a gold-free NL->FOL faithfulness metric. SCOOP RULE (multi-family translations + solver equivalence + faithfulness-label meta-eval on NL->FOL): no hit meets all three, so C1 is not scooped. Closest neighbours meet two of three each: ARc 2511.09008 (NL->SMT, k LLMs, per-translation confidence = share of k translations entailing it, i.e. the same score form as c_score, but a fixed schema and downstream-QA labels); NoTB 2608.21962 (RTL, 4 families, precision 63/85.3/87/94.7% at >=1..4 families, coverage 100/49/33… |<!-- v:prior_art.csv -->
| C-claims | VERDICT SUMMARY. No paper meets the pre-stated scoop rule, i.e. (i) multiple model families' formal translations + (ii) solver equivalence + (iii) meta-evaluation of the agreement score against faithfulness labels on NL->FOL. So C1 is NOT scooped as a method-plus-evaluation package. But the METHOD itself is not new, and all five claims except C2 need qualifiers. |<!-- v:prior_art.csv -->
| C-claims | C1 (beats API judge; adds over baseline stack): NEEDS-QUALIFIER. Claim only "the first meta-evaluation of cross-family solver consensus as a gold-free faithfulness score for individual NL->FOL candidates, against adjudicated labels, head-to-head with an API judge and nested over the parse / round-trip / judge / self-consistency / structural stack". Credit ARc [33] and NoTB [1] for the score form. Never say "we propose cross-model consensus", and never claim superiority over judges in general (GenV shows the reverse under intent labels [3]). If T1 loses to the API judge, report parity plus cost (~$0.0015/sentence vs ~$0.00004/judge call). |<!-- v:prior_art.csv -->
| C-claims | C2 (holds with aligner-free labels): SAFE as a methodological contribution. No neighbour controls for the labeller and the metric sharing an instrument. Cite GenV's label-target reversal [3], and wrong gold in FOLIO/MALLS, which is 39%/36% in v1 but 42.5%/42% in v2 (3 Sep 2026) of 2606.02837 [24]. |<!-- v:prior_art.csv -->
| C-claims | C3 (rename-invariant hybrid matcher): NEEDS-QUALIFIER. Predicate alignment exists: LogicLLaMA greedy binding search [36], Levenshtein <=0.6 mapping [37], and leaf-matching left open by [31]. No neighbour reports a rename false-alarm rate. That is the novel piece (ours: 0.859 ALIGN vs 0.074 NF). |<!-- v:prior_art.csv -->
| C-claims | C4 (e/d decomposition; endorsement falls with conditions): NEEDS-QUALIFIER. AUROC = 1-(e+d)/2 at a fixed threshold is balanced accuracy. The scatter premise is stated by [2, 9, 40], and identical-wrong outputs from missing logic were noted in 1978 [60]. Coincident-FAILURE theory predicts that both-wrong rises with input difficulty [21, 22, 23]. Replications confirm concentration on hard inputs [18, 20]. LLM correlated-error work does not condition on difficulty: [14] names it as future work, and [2] uses a scalar attractor rate. So the candidate-new piece is the MEASURED identical-wrong (endorsement) vs both-wrong curve over number of conditions for NL->FOL. Indirect support for the falling … |<!-- v:prior_art.csv -->
| C-claims | C5 (3-5 families suffice): NEEDS-QUALIFIER. It is already recommended ("three to four cross-family models" [2]), and it is consistent with NoTB's curve [1] and effective-N results (7 models ~ 2.58 [15]; 9 judges ~ 2 votes [48]; 16 models ~ 1.69 formulations [63]). Novelty exists only per complexity tercile with cost. |<!-- v:prior_art.csv -->
| C-claims | CONFIDENCE. High that the method is not new (verbatim quotes from [1, 33]). Medium that no NL->FOL cross-family meta-evaluation exists: the sweep was logged but not systematic, and forward citations of NoTB and roundtrip were rate-limited. Medium on C4: the classical papers [21, 22] were read as abstracts plus review [23]. A 1990s tabulation of identical-wrong outputs vs input complexity, or a GenV/VERGE follow-up evaluating cross-model mode, would change the verdicts. |<!-- v:prior_art.csv -->
| C-claims | [31] [By Their Fruits You Will Know Them: Comparing Formalizations of Law by the Decisions They Encode](https://arxiv.org/html/2605.25186) (Julius Vernie, Matthias Grabmair; 2026) — Different formalizations rarely share leaf nodes; matching correctness left open (C3 context). |<!-- v:prior_art.csv -->
| C-claims | [36] [Harnessing the Power of Large Language Models for Natural Language to First-Order Logic Translation (LogicLLaMA)](https://arxiv.org/html/2305.15541) (Yuan Yang, Siheng Xiong, Ali Payani, Ehsan Shareghi, Faramarz Fekri; 2023) — LE metric uses greedy search for the predicate binding that maximises LE (C3 precedent). |<!-- v:prior_art.csv -->
| C-claims | [37] [Advancing Natural Language Formalization to First Order Logic with Fine-tuned LLMs](https://arxiv.org/html/2509.22338) (Felix Vossel, Till Mossakowski, Björn Gehrke; 2025) — Maps predicates by normalised Levenshtein distance (threshold 0.6) before equivalence checking (C3 precedent). |<!-- v:prior_art.csv -->
| C-claims | [60] [N-Version Programming: A Fault-Tolerance Approach to Reliability of Software Operation](https://www.inf.pucrs.br/~zorzo/cs/n-versionprogramming.pdf) (Liming Chen, Algirdas Avizienis; 1978) — FTCS-8 1978: 'faulty but identical results (due to missing logic) may outvote correct results'; defines inexact voting - the identical-wrong vs coincident-failure distinction for C4. |<!-- v:prior_art.csv -->
| C-claims | [63] [Sixteen models, fewer than two voices: measuring ensemble dispersion where no answer is uniquely correct](https://arxiv.org/abs/2608.00285) (Mario Vega-Barbas, Lidia Mora-Valenciano, Iván Pau, Fernando Seoane, Farhad Abtahi; 2026) — 16 models from 10 families give 1.69 distinct formulations vs 1.43 for one model (effective diversity bound, C5). |<!-- v:prior_art.csv -->

**Two sentences to add under the iteration-4 claims:**

- Under §4.3's shared-vocabulary result: supplying a predicate list is a documented NL→FOL lever — Vossel et al. (`arXiv:2509.22338`) report that "predicate availability boosts performance by 15-20%"<!-- v:vossel.md --> (verbatim quote verified in `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_research_1/notes/full/vossel.md`), and ARc (`arXiv:2511.09008`) scores translations over a fixed shared schema precisely so that k translations can be compared. What SIGPROXY adds is only a measured d reduction (0.149<!-- n:x10_d_cued --> cued vs 0.757<!-- n:x10_d_uncued --> uncued on the same long templated bases, −0.608 [−0.716, −0.500]<!-- n:x10_d_diff -->) in the controlled-vocabulary regime the user excluded.
- Under §4.2's anchoring result: peers given the candidate's symbols copying its errors is the correlated-failure mode of N-version programming (Chen & Avizienis, `FTCS-8`). The new element is the per-class e measurement; its sharpest contrast, MEANING_RENAME-type, is CSC 0.821<!-- n:x9_t9_MR_CSC --> vs FREE_exact 0.036<!-- n:x9_t9_MR_FREE_exact -->, but against FREE_ALIGN (the aligner c_score_align uses) the difference is only +0.071 [−0.083, 0.269]<!-- n:x9_t9_mr_d --> (n.s.: CI covers 0), NOT_READ.

Sources: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/prior_art.csv`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_research_1/research_report.md`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_research_1/notes/full/vossel.md`


## 8. §4.1 Reasoning block (new; opens §4)

Replaces: paper_draft.md `### 4.1 Strategy`, lines 1031-1036 (the reasoning block below goes before the strategy paragraph).

~~Pre-registered gates for CSC (experiment 9, sha256 in prereg): G1 (d slope non-positive), G2 (strat AUROC ≥ 0.700 on E), G3-E (E2 confirmation), G5 (cost ≤ $0.002/candidate).~~ [Correction, iter 4: the gates are quoted verbatim from the prereg below; G2 is not a fixed-AUROC bar and G3-E is the RENAME_SYN false-alarm gate, not E2 confirmation; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/prereg_csc_E.json] (paper_draft.md L1035)

**Why iteration 4 did what it did.**
1. The previous review scored the record 3<!-- n:rv3_score --> (blocking) with 12<!-- n:rv3_n --> critiques; eval 3 Part 4 was built to answer its record items (corrected verdicts, cost units, artifact IDs).
2. The iter-3 hypothesis update chose move **DEEPEN** with title "Peer agreement in the candidate's own words"<!-- v:iter_3/upd_hypo -->.
3. The CSC prediction: cueing peers with the candidate's own symbols should give a LOWER d without a HIGHER e; eval 3's pre-registered d_floor (instrument bracket 0.396<!-- n:e3_br_lo -->–0.415<!-- n:e3_br_hi -->, no-anchoring oracle floor 0.385<!-- n:e3_oracle3 -->) was the yardstick; stopping rule: CSC is dropped if G1 or G2 fails.
4. The gates, verbatim from `prereg_csc_E.json`:
  - G1: "d(c_csc > 0.5 | R_AB CORRECT) <= 0.35 AND the words slope of GEE d ~ z(words) + z(n_conditions) among CORRECT rows has CI including 0 or entirely < 0"<!-- v:prereg_csc_E.json -->
  - G2: "stratified AUROC(CSC) >= stratified AUROC(c_score_align) - 0.01 on R_AB AND pooled AUROC(CSC) > AUROC(c_score_align) on L25 (point estimates; the L25 paired CI is reported whatever its sign)"<!-- v:prereg_csc_E.json -->
  - G3-E: "FA(c > 0.5) on RENAME_SYN CORRECT rows <= base FA (same rows, CSC-OWN) + 0.05 (point estimate; CI reported); NONCE reported as the stress boundary, not gated"<!-- v:prereg_csc_E.json -->
  - G4: "null here (sibling PERTURB experiment)"<!-- v:prereg_csc_E.json -->
  - G5: "FULL cost per candidate (sum of its peer calls, dedup-apportioned) <= $0.002"<!-- v:prereg_csc_E.json -->
  - variants: "{c_csc, c_csc_graded, c_csc_multi} x k {3, 4 on the K4 rows} + HYB_MEAN; graded variants binarised at the same c > 0.5"<!-- v:prereg_csc_E.json -->
5. Planned artifacts and caps (iteration-4 strategy) vs actual spend (ledgers; section 14):

| type | objective (truncated) | planned cap |
|-|-|-|
| experiment | T6-E: Candidate-Signature Consensus on development set E. Measure whether giving peers only the candidate's ow…<!-- v:gen_strat_1 --> | $9.5<!-- n:i4_cap_0 --> |
| experiment | T6-P: the opposing force and the boundary. On PERTURB (known labels), measure whether showing peers the candid…<!-- v:gen_strat_1 --> | $9.5<!-- n:i4_cap_1 --> |
| dataset | T7a: E2, the first confirmation set no decision has touched, sized for power where iteration 3 was null. About…<!-- v:gen_strat_1 --> | $9.5<!-- n:i4_cap_2 --> |
| dataset | T7b: make the in-scope FREE condition of R_COMP testable, with labels that share no instrument with any consen…<!-- v:gen_strat_1 --> | $4.0<!-- n:i4_cap_3 --> |
| evaluation | T8 ($0, CPU): the mechanism PREDICTION for CSC, the second-population e/d, the iteration-5 power analysis, and…<!-- v:gen_strat_1 --> | $0.0<!-- n:i4_cap_4 --> |

   Actual: exp 9 $0.108<!-- n:x9_spend -->, exp 10 $0.0000088<!-- n:x10_spend -->, dataset 4 $0.241<!-- n:d4_spend -->, dataset 5 $0<!-- n:sp_d5 -->, eval 3 no ledger (CPU only). The platform refused paid calls at the first HTTP 403 (section 14 gives the time and the evidenced vs unaccounted spend).

Sources: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/review_report/review_report/.terminal_claude_agent_struct_out.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_strat/gen_strat_1/.terminal_claude_agent_struct_out.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/prereg_csc_E.json`


## 9. §4.2 Experiment 9, CSC on DEVELOPMENT set E: re-transcribed

Replaces: paper_draft.md `### 4.2 Experiment 9: CSC on held-out E (T6-E) — negative result`, lines 1037-1106

~~### 4.2 Experiment 9: CSC on held-out E (T6-E) — negative result~~ [Correction, iter 4: E is DEVELOPMENT data; heading becomes "§4.2 Experiment 9: CSC on development set E — provisional negative"; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json] (paper_draft.md L1037)

~~| **CSC** | **0.614 [0.545, 0.679]** |~~ [Correction, iter 4: every CI in the headline table was narrower than the source; the T4 table below is transcribed from analysis.json; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/results/analysis.json] (paper_draft.md L1063)

~~| COMPOUND | 0.643 | 0.246 |~~ [Correction, iter 4: COMPOUND e_CSC / e_FREE_exact are 0.282<!-- n:x9_t9_COMPOUND_CSC --> / 0.107<!-- n:x9_t9_COMPOUND_FREE_exact --> (T9); the struck values were a different quantity; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/results/analysis.json] (paper_draft.md L1079)

~~The M3-style length interaction for CSC is negative: −0.232 [−0.417, −0.041] (CSC vs flash-lite judge).~~ [Correction, iter 4: M3 under both specifications: bootstrap −0.232 [−0.770, −0.023]<!-- n:x9_m3_boot -->, stacked GEE −0.351 [−0.694, −0.009]<!-- n:x9_m3_gee -->; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/results/analysis.json] (paper_draft.md L1085)

~~| G2 (strat AUROC ≥ 0.700) | **FAIL** (0.614) |~~ [Correction, iter 4: G2 is NOT_READ (R_AB part FAIL; L25 below the readable cell size); source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/csc_gate_E.json] (paper_draft.md L1092)

~~| G3-E (E2 confirmation) | NOT_RUN (E2 not testable) |~~ [Correction, iter 4: G3-E is the RENAME_SYN false-alarm gate: NOT_RUN; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/prereg_csc_E.json] (paper_draft.md L1093)

~~CSC degrades the decision boundary relative to the FREE baseline.~~ [Correction, iter 4: NET is the within-arm change from words T1 to T3; every arm degrades (FULL FREE_exact +0.452<!-- n:x9_net_fx -->, FREE_align +0.401<!-- n:x9_net_fa -->); source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/results/analysis.json] (paper_draft.md L1105)

~~CSC fails both quality gates. It is a dead end for the same reason it was promising: sharing the candidate's vocabulary helps correct candidates converge (reducing d) but also helps incorrect candidates recruit agreement (raising e).~~ [Correction, iter 4: 'dead end' becomes 'provisional negative on a completion-selected subset; L25 and RENAME untested'; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/csc_gate_E.json] (paper_draft.md L1096)

**Population and selection.** The platform refused paid calls after 1,033<!-- n:x9_calls_done --> of ~9,000<!-- n:x9_calls_plan --> planned peer calls, so CSC is scored on a COMPLETION-SELECTED subset: PRIMARY = 354<!-- n:x9_n --> R_AB rows (196<!-- n:x9_nerr --> ERROR / 158<!-- n:x9_ncor --> CORRECT, 144<!-- n:x9_nsent --> sentences). CTRL makes up 44.9%<!-- n:x9_ctrl_prim --> of PRIMARY CORRECT rows vs 27.4%<!-- n:x9_ctrl_full --> on FULL. No stratum reaches `50/50` (L25: 59<!-- n:x9_l25_err --> / 22<!-- n:x9_l25_cor -->), so L25 is NOT_READ. c_csc is almost binary (tie rate 0.986<!-- n:x9_tie -->). The prereg calls every gate PROVISIONAL. CIs: sentence-cluster percentile bootstrap, B = 2000, seed 0, stratified by source stratum (tables.md header).

**T4. Strat AUROC on PRIMARY** (CIs verbatim):

| metric | strat AUROC [95% CI] |
|-|-|
| c_csc | 0.614 [0.493, 0.736]<!-- n:x9_csc --> |
| FREE_exact (same 3 families) | 0.770 [0.686, 0.844]<!-- n:x9_fexact --> |
| FREE_ALIGN | 0.731 [0.635, 0.825]<!-- n:x9_falign --> |
| c_score_align | 0.774 [0.682, 0.857]<!-- n:x9_calign --> |
| p_peer_text | 0.799 [0.700, 0.880]<!-- n:x9_ppt --> |
| S4_full | 0.736 [0.635, 0.826]<!-- n:x9_s4 --> |
| flash-lite disguised | 0.664 [0.568, 0.750]<!-- n:x9_flash --> |
| HYB_MEAN (fails G1) | 0.709 [0.586, 0.817]<!-- n:x9_hyb --> |

**T5. Paired Δ, same rows:**

| contrast | Δ [95% CI] |
|-|-|
| c_csc − FREE_exact | −0.156 [−0.290, −0.031]<!-- n:x9_d_fexact --> |
| c_csc − c_score_align | −0.160 [−0.275, −0.064]<!-- n:x9_d_calign --> |
| c_csc − flash-lite | −0.050 [−0.212, 0.107]<!-- n:x9_d_flash --> (n.s.: CI covers 0) |
| c_csc − S4_full | −0.123 [−0.269, 0.010]<!-- n:x9_d_s4 --> (n.s.: CI covers 0) |
| c_csc − p_peer_text | −0.185 [−0.281, −0.103]<!-- n:x9_d_ppt --> |

Nesting: [S4_full + c_csc] − S4_full +0.006 [−0.013, 0.025]<!-- n:x9_nest --> (n.s.: CI covers 0). Phi-4 exemplar leakage (T17, POST-HOC): 58<!-- n:x9_phi_calls --> CSC calls copied the few-shot exemplar; removing them symmetrically gives c_csc_clean 0.639<!-- n:x9_clean --> and Δ vs FREE_exact_clean −0.132 [−0.251, −0.023]<!-- n:x9_clean_d -->.

**e and d.** CSC e 0.459<!-- n:x9_e_csc --> vs FREE_exact 0.173<!-- n:x9_e_fx --> vs FREE_ALIGN 0.352<!-- n:x9_e_fa -->; d 0.139<!-- n:x9_d_csc --> vs 0.323<!-- n:x9_d_fx --> vs 0.190<!-- n:x9_d_fa -->. FULL population ($0, T2): FREE_exact d 0.583<!-- n:x9_full_d_fx --> vs ALIGN 0.328<!-- n:x9_full_d_fa --> (e 0.130<!-- n:x9_full_e_fx --> vs 0.268<!-- n:x9_full_e_fa -->).

**T9. e by error class, PRIMARY** (FREE_exact AND FREE_ALIGN side by side):

| class | e_CSC | e_FREE_exact | e_FREE_ALIGN |
|-|-|-|-|
| ADD | 0.490<!-- n:x9_t9_ADD_CSC --> | 0.135<!-- n:x9_t9_ADD_FREE_exact --> | 0.375<!-- n:x9_t9_ADD_FREE_align --> |
| DROP | 0.472<!-- n:x9_t9_DROP_CSC --> | 0.169<!-- n:x9_t9_DROP_FREE_exact --> | 0.380<!-- n:x9_t9_DROP_FREE_align --> |
| COMPOUND | 0.282<!-- n:x9_t9_COMPOUND_CSC --> | 0.107<!-- n:x9_t9_COMPOUND_FREE_exact --> | 0.184<!-- n:x9_t9_COMPOUND_FREE_align --> |
| MEANING_RENAME-type (n = 28<!-- n:x9_t9_mr_n -->) | 0.821<!-- n:x9_t9_MR_CSC --> | 0.036<!-- n:x9_t9_MR_FREE_exact --> | 0.750<!-- n:x9_t9_MR_FREE_align --> |
| structural | 0.336<!-- n:x9_t9_STRUCT_CSC --> | 0.153<!-- n:x9_t9_STRUCT_FREE_exact --> | 0.282<!-- n:x9_t9_STRUCT_FREE_align --> |
| polarity | 0.200<!-- n:x9_t9_POL_CSC --> | 0.133<!-- n:x9_t9_POL_FREE_exact --> | 0.200<!-- n:x9_t9_POL_FREE_align --> |

MEANING_RENAME-type Δe CSC − FREE_ALIGN +0.071 [−0.083, 0.269]<!-- n:x9_t9_mr_d --> (n.s.: CI covers 0) (NOT_READ). T9b (FULL, free peers): FREE_ALIGN e on MEANING_RENAME-type 0.624<!-- n:x9_t9b_mr_fa --> vs FREE_exact 0.104<!-- n:x9_t9b_mr_fx -->. Reading: every vocabulary bridge (the aligner, or peers cued with the candidate's symbols) lowers d AND raises e; the aligner that c_score_align uses already endorses meaning-rename errors almost as often as CSC.

**Gates (verbatim definitions in section 8).** G1 FAIL (d 0.139<!-- n:x9_g1_d --> passes the bar but the words slope is +1.25 [0.41, 2.09]<!-- n:x9_g1_slope -->); G2 NOT_READ (R_AB part FAIL; L25 Δ −0.067 [−0.183, 0.040]<!-- n:x9_g2_l25 -->, n below the readable size); G3-E NOT_RUN<!-- n:x9_g3 -->; G4 null; G5 PASS $5.25e-4<!-- n:x9_g5 --> per candidate ($2.76e-4<!-- n:x9_g5_dd --> deduped). CSC_graded (0.608 [0.487, 0.734]<!-- n:x9_graded -->) and CSC_multi (0.601 [0.480, 0.720]<!-- n:x9_multi -->) and HYB_MEAN (d 0.190<!-- n:x9_hyb_g1d -->, slope 1.15<!-- n:x9_hyb_g1s -->) also fail G1.

**Length.** M3 (CSC − flash-lite, decision correctness vs words): bootstrap −0.232 [−0.770, −0.023]<!-- n:x9_m3_boot -->; stacked GEE −0.351 [−0.694, −0.009]<!-- n:x9_m3_gee -->. NET is within-arm length degradation: FULL FREE_exact +0.452<!-- n:x9_net_fx -->, FREE_align +0.401<!-- n:x9_net_fa -->. Words-tercile strat AUROC, PRIMARY: c_csc 0.562<!-- n:x9_t12_csc_T1 --> / 0.670<!-- n:x9_t12_csc_T2 --> / 0.409<!-- n:x9_t12_csc_T3 -->; c_score_align 0.806<!-- n:x9_t12_ca_T1 --> / 0.695<!-- n:x9_t12_ca_T2 --> / 0.601<!-- n:x9_t12_ca_T3 -->.

**T8 (where d comes from, FULL).** 53%<!-- n:x9_t8_struct --> of free-exact disagreements with CORRECT candidates are structural (no vocabulary map makes them equivalent); only 20.2%<!-- n:x9_t8_vocab --> of flagged CORRECT rows have every disagreement vocabulary-resolvable. **T10 typing:** own_majority 0.185<!-- n:x9_t10_own -->, below the majority class 0.262<!-- n:x9_t10_maj -->. **T14 system level:** CSC τ-b 0.256<!-- n:x9_t14_csc --> (p = 0.25<!-- n:x9_t14_csc_p -->) vs c_score_align 0.513<!-- n:x9_t14_ca --> (p = 0.015<!-- n:x9_t14_ca_p -->). **T15 rename (9-peer c_score_align, WordNet synonyms):** FA 0.595<!-- n:x9_t15_base --> → 0.868<!-- n:x9_t15_syn -->, ΔFA +0.273 [0.164, 0.384]<!-- n:x9_t15_d -->. Reproduction check: eval-2 3-pool strat 0.7428<!-- n:x9_repro -->. Spend $0.108<!-- n:x9_spend -->.

**Verdict wording.** "Provisional negative on a completion-selected subset; L25 and RENAME untested." CSC vs flash-lite and vs S4_full is n.s. on PRIMARY.

Sources: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/results/analysis.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/tables.md`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/csc_gate_E.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/prereg_csc_E.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/results/posthoc_phi_contamination.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/results/repro_checks.json`


## 10. §4.3 Experiment 10 (CSC on PERTURB, budget-stopped): corrected

Replaces: paper_draft.md `### 4.3 Experiment 10: CSC on PERTURB (T6-P) — budget exhausted`, lines 1107-1183

~~FREE consensus achieves near-perfect recall on PERTURB (e ≈ 0, recall ≈ 1.0).~~ [Correction, iter 4: FREE-consensus recall ≈ 1 comes with base FA on verified-CORRECT bases of 0.712<!-- n:x10_bfa_calign --> / 0.803<!-- n:x10_bfa_fx_e --> / 0.986<!-- n:x10_bfa_fx_r --> / 0.757<!-- n:x10_bfa_fa_r --> (table below): that recall is trivial; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/results/d_by_length.csv] (paper_draft.md L1171)

~~LOCAL2 (small 1.5-2B local peers) has substantial endorsement (0.276-0.341), consistent with weaker models failing to distinguish mutants from bases.~~ [Correction, iter 4: every LOCAL2 endorsement is an insufficient-peer tie at `c = 0.5` (tie share 0.341<!-- n:x10_l2_tie -->); excluding ties e is 0.012<!-- n:x10_l2_excl_own --> / 0.007<!-- n:x10_l2_excl_base -->; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/results/anchoring.csv] (paper_draft.md L1171)

~~The flash-lite judge endorses 12.4% of mutants, matching the iteration-3 E endorsement rate.~~ [Correction, iter 4: the judge misses 0.124<!-- n:x10_judge_e --> of PERTURB mutants; this is NOT END_MAJ e on real errors (a different quantity); source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/results/anchoring.csv] (paper_draft.md L1171)

~~| free3 (independent vocab) | ALL | 3884 | 0.085 [0.058, 0.118] |~~ [Correction, iter 4: free3 on E is 0.123 [0.081, 0.169]<!-- n:x10_free3 -->; the pooled 0.085<!-- n:x10_free3_pool --> includes R_COMP rows at zero; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/results/typing_csc.csv] (paper_draft.md L1156)

~~All consensus variants flag RENAME controls at 85-100% FA.~~ [Correction, iter 4: most rename FA is base FA: the paired flip rates are the rename effect (c_align E SYN 0.182<!-- n:x10_flip_syn -->, NONCE 0.327<!-- n:x10_flip_nonce -->); controls split by base source below; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/results/controls_fa.csv] (paper_draft.md L1182)

~~| FREE3_exact | 1.000 | 1.000 | 0.986 (R_COMP) | 0.986 (R_COMP) |~~ [Correction, iter 4: mixed sources: FREE3_exact REORDER / CONTRA FA on E is 0.842<!-- n:x10_reorder_e --> / 0.840<!-- n:x10_contra_e -->; on R_COMP 0.986<!-- n:x10_contra_r -->; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/results/controls_fa.csv] (paper_draft.md L1178)

**Status.** 0 CSC peers were generated (run budget refused the first call; spend $0.0000088<!-- n:x10_spend -->); G3-P, G4 and MT are UNTESTED, not failed. Zero-cost arms follow (development data).

**Recall next to base FA** (`c > 0.5`; mutants vs the verified-CORRECT bases they were derived from):

| arm | bases | mutant recall | base FA |
|-|-|-|-|
| c_align (exp 8) | E | recall 0.999<!-- n:x10_rec_FREE_c_align_exp8_E --> | base FA 0.712<!-- n:x10_bfa_calign --> |
| FREE3_exact | E | recall 1.000<!-- n:x10_rec_FREE3_exact_E --> | base FA 0.803<!-- n:x10_bfa_fx_e --> |
| FREE3_align | E | recall 0.998<!-- n:x10_rec_FREE3_align_E --> | base FA 0.503<!-- n:x10_bfa_fa_e --> |
| FREE3_exact | R_COMP | recall 1.000<!-- n:x10_rec_FREE3_exact_RCOMP --> | base FA 0.986<!-- n:x10_bfa_fx_r --> |
| FREE3_align | R_COMP | recall 1.000<!-- n:x10_rec_FREE3_align_RCOMP --> | base FA 0.757<!-- n:x10_bfa_fa_r --> |
| flash-lite judge | E | recall 0.876<!-- n:x10_rec_JUDGE_flashlite_disg_exp8_E --> | base FA 0.320<!-- n:x10_bfa_judge_e --> |

**d rises with length (T4, uncued, E bases, words terciles):** c_align 0.47<!-- n:x10_t1 --> / 0.80<!-- n:x10_t2 --> / 0.91<!-- n:x10_t3 -->; FREE3_exact 0.667<!-- n:x10_FREE3_exact_d_T1 --> / 0.852<!-- n:x10_FREE3_exact_d_T2 --> / 0.925<!-- n:x10_FREE3_exact_d_T3 -->.

**Controls split by base source** (FA / paired base FA / flip):

| variant | bases | RENAME_SYN | RENAME_NONCE | REORDER_COMMUTE | CONTRAPOSITIVE |
|-|-|-|-|-|-|
| `FREE_c_align_exp8` | E | FA 0.943<!-- n:ctl_FREE_c_align_exp8_RENAME_SYN_E_fa --> / base FA 0.761<!-- n:ctl_FREE_c_align_exp8_RENAME_SYN_E_base --> / flip 0.182<!-- n:ctl_FREE_c_align_exp8_RENAME_SYN_E_flip --> | FA 1.000<!-- n:ctl_FREE_c_align_exp8_RENAME_NONCE_E_fa --> / base FA 0.673<!-- n:ctl_FREE_c_align_exp8_RENAME_NONCE_E_base --> / flip 0.327<!-- n:ctl_FREE_c_align_exp8_RENAME_NONCE_E_flip --> | FA 0.741<!-- n:ctl_FREE_c_align_exp8_REORDER_COMMUTE_E_fa --> / base FA 0.741<!-- n:ctl_FREE_c_align_exp8_REORDER_COMMUTE_E_base --> / flip 0.000<!-- n:ctl_FREE_c_align_exp8_REORDER_COMMUTE_E_flip --> | FA 0.765<!-- n:ctl_FREE_c_align_exp8_CONTRAPOSITIVE_E_fa --> / base FA 0.765<!-- n:ctl_FREE_c_align_exp8_CONTRAPOSITIVE_E_base --> / flip 0.000<!-- n:ctl_FREE_c_align_exp8_CONTRAPOSITIVE_E_flip --> |
| `FREE3_exact` | E | FA 1.000<!-- n:ctl_FREE3_exact_RENAME_SYN_E_fa --> / base FA 0.867<!-- n:ctl_FREE3_exact_RENAME_SYN_E_base --> / flip 0.133<!-- n:ctl_FREE3_exact_RENAME_SYN_E_flip --> | FA 1.000<!-- n:ctl_FREE3_exact_RENAME_NONCE_E_fa --> / base FA 0.755<!-- n:ctl_FREE3_exact_RENAME_NONCE_E_base --> / flip 0.245<!-- n:ctl_FREE3_exact_RENAME_NONCE_E_flip --> | FA 0.842<!-- n:ctl_FREE3_exact_REORDER_COMMUTE_E_fa --> / base FA 0.842<!-- n:ctl_FREE3_exact_REORDER_COMMUTE_E_base --> / flip 0.000<!-- n:ctl_FREE3_exact_REORDER_COMMUTE_E_flip --> | FA 0.840<!-- n:ctl_FREE3_exact_CONTRAPOSITIVE_E_fa --> / base FA 0.840<!-- n:ctl_FREE3_exact_CONTRAPOSITIVE_E_base --> / flip 0.000<!-- n:ctl_FREE3_exact_CONTRAPOSITIVE_E_flip --> |
| `FREE3_exact` | RCOMP | FA 1.000<!-- n:ctl_FREE3_exact_RENAME_SYN_RCOMP_fa --> / base FA 1.000<!-- n:ctl_FREE3_exact_RENAME_SYN_RCOMP_base --> / flip 0.000<!-- n:ctl_FREE3_exact_RENAME_SYN_RCOMP_flip --> | FA 1.000<!-- n:ctl_FREE3_exact_RENAME_NONCE_RCOMP_fa --> / base FA 0.971<!-- n:ctl_FREE3_exact_RENAME_NONCE_RCOMP_base --> / flip 0.029<!-- n:ctl_FREE3_exact_RENAME_NONCE_RCOMP_flip --> | FA 0.986<!-- n:ctl_FREE3_exact_REORDER_COMMUTE_RCOMP_fa --> / base FA 0.986<!-- n:ctl_FREE3_exact_REORDER_COMMUTE_RCOMP_base --> / flip 0.000<!-- n:ctl_FREE3_exact_REORDER_COMMUTE_RCOMP_flip --> | FA 0.986<!-- n:ctl_FREE3_exact_CONTRAPOSITIVE_RCOMP_fa --> / base FA 0.986<!-- n:ctl_FREE3_exact_CONTRAPOSITIVE_RCOMP_base --> / flip 0.000<!-- n:ctl_FREE3_exact_CONTRAPOSITIVE_RCOMP_flip --> |
| `FREE3_align` | E | FA 0.853<!-- n:ctl_FREE3_align_RENAME_SYN_E_fa --> / base FA 0.547<!-- n:ctl_FREE3_align_RENAME_SYN_E_base --> / flip 0.307<!-- n:ctl_FREE3_align_RENAME_SYN_E_flip --> | FA 1.000<!-- n:ctl_FREE3_align_RENAME_NONCE_E_fa --> / base FA 0.469<!-- n:ctl_FREE3_align_RENAME_NONCE_E_base --> / flip 0.531<!-- n:ctl_FREE3_align_RENAME_NONCE_E_flip --> | FA 0.525<!-- n:ctl_FREE3_align_REORDER_COMMUTE_E_fa --> / base FA 0.525<!-- n:ctl_FREE3_align_REORDER_COMMUTE_E_base --> / flip 0.000<!-- n:ctl_FREE3_align_REORDER_COMMUTE_E_flip --> | FA 0.545<!-- n:ctl_FREE3_align_CONTRAPOSITIVE_E_fa --> / base FA 0.545<!-- n:ctl_FREE3_align_CONTRAPOSITIVE_E_base --> / flip 0.000<!-- n:ctl_FREE3_align_CONTRAPOSITIVE_E_flip --> |
| `FREE3_align` | RCOMP | FA 0.850<!-- n:ctl_FREE3_align_RENAME_SYN_RCOMP_fa --> / base FA 0.700<!-- n:ctl_FREE3_align_RENAME_SYN_RCOMP_base --> / flip 0.150<!-- n:ctl_FREE3_align_RENAME_SYN_RCOMP_flip --> | FA 1.000<!-- n:ctl_FREE3_align_RENAME_NONCE_RCOMP_fa --> / base FA 0.824<!-- n:ctl_FREE3_align_RENAME_NONCE_RCOMP_base --> / flip 0.176<!-- n:ctl_FREE3_align_RENAME_NONCE_RCOMP_flip --> | FA 0.757<!-- n:ctl_FREE3_align_REORDER_COMMUTE_RCOMP_fa --> / base FA 0.757<!-- n:ctl_FREE3_align_REORDER_COMMUTE_RCOMP_base --> / flip 0.000<!-- n:ctl_FREE3_align_REORDER_COMMUTE_RCOMP_flip --> | FA 0.757<!-- n:ctl_FREE3_align_CONTRAPOSITIVE_RCOMP_fa --> / base FA 0.757<!-- n:ctl_FREE3_align_CONTRAPOSITIVE_RCOMP_base --> / flip 0.000<!-- n:ctl_FREE3_align_CONTRAPOSITIVE_RCOMP_flip --> |
| `JUDGE_flashlite_disg_exp8` | E | FA 0.261<!-- n:ctl_JUDGE_flashlite_disg_exp8_RENAME_SYN_E_fa --> / base FA 0.295<!-- n:ctl_JUDGE_flashlite_disg_exp8_RENAME_SYN_E_base --> / flip 0.170<!-- n:ctl_JUDGE_flashlite_disg_exp8_RENAME_SYN_E_flip --> | FA 0.652<!-- n:ctl_JUDGE_flashlite_disg_exp8_RENAME_NONCE_E_fa --> / base FA 0.339<!-- n:ctl_JUDGE_flashlite_disg_exp8_RENAME_NONCE_E_base --> / flip 0.366<!-- n:ctl_JUDGE_flashlite_disg_exp8_RENAME_NONCE_E_flip --> | FA 0.418<!-- n:ctl_JUDGE_flashlite_disg_exp8_REORDER_COMMUTE_E_fa --> / base FA 0.285<!-- n:ctl_JUDGE_flashlite_disg_exp8_REORDER_COMMUTE_E_base --> / flip 0.222<!-- n:ctl_JUDGE_flashlite_disg_exp8_REORDER_COMMUTE_E_flip --> | FA 0.939<!-- n:ctl_JUDGE_flashlite_disg_exp8_CONTRAPOSITIVE_E_fa --> / base FA 0.348<!-- n:ctl_JUDGE_flashlite_disg_exp8_CONTRAPOSITIVE_E_base --> / flip 0.591<!-- n:ctl_JUDGE_flashlite_disg_exp8_CONTRAPOSITIVE_E_flip --> |
| `JUDGE_flashlite_disg_exp8` | RCOMP | FA 0.736<!-- n:ctl_JUDGE_flashlite_disg_exp8_RENAME_SYN_RCOMP_fa --> / base FA 0.679<!-- n:ctl_JUDGE_flashlite_disg_exp8_RENAME_SYN_RCOMP_base --> / flip 0.132<!-- n:ctl_JUDGE_flashlite_disg_exp8_RENAME_SYN_RCOMP_flip --> | FA 0.851<!-- n:ctl_JUDGE_flashlite_disg_exp8_RENAME_NONCE_RCOMP_fa --> / base FA 0.660<!-- n:ctl_JUDGE_flashlite_disg_exp8_RENAME_NONCE_RCOMP_base --> / flip 0.234<!-- n:ctl_JUDGE_flashlite_disg_exp8_RENAME_NONCE_RCOMP_flip --> | FA 0.580<!-- n:ctl_JUDGE_flashlite_disg_exp8_REORDER_COMMUTE_RCOMP_fa --> / base FA 0.670<!-- n:ctl_JUDGE_flashlite_disg_exp8_REORDER_COMMUTE_RCOMP_base --> / flip 0.210<!-- n:ctl_JUDGE_flashlite_disg_exp8_REORDER_COMMUTE_RCOMP_flip --> | FA 1.000<!-- n:ctl_JUDGE_flashlite_disg_exp8_CONTRAPOSITIVE_RCOMP_fa --> / base FA 0.670<!-- n:ctl_JUDGE_flashlite_disg_exp8_CONTRAPOSITIVE_RCOMP_base --> / flip 0.330<!-- n:ctl_JUDGE_flashlite_disg_exp8_CONTRAPOSITIVE_RCOMP_flip --> |
| `SIGPROXY_K3` | RCOMP | FA 1.000<!-- n:ctl_SIGPROXY_K3_RENAME_SYN_RCOMP_fa --> / base FA 0.119<!-- n:ctl_SIGPROXY_K3_RENAME_SYN_RCOMP_base --> / flip 0.881<!-- n:ctl_SIGPROXY_K3_RENAME_SYN_RCOMP_flip --> | FA 1.000<!-- n:ctl_SIGPROXY_K3_RENAME_NONCE_RCOMP_fa --> / base FA 0.171<!-- n:ctl_SIGPROXY_K3_RENAME_NONCE_RCOMP_base --> / flip 0.829<!-- n:ctl_SIGPROXY_K3_RENAME_NONCE_RCOMP_flip --> | FA 0.143<!-- n:ctl_SIGPROXY_K3_REORDER_COMMUTE_RCOMP_fa --> / base FA 0.143<!-- n:ctl_SIGPROXY_K3_REORDER_COMMUTE_RCOMP_base --> / flip 0.000<!-- n:ctl_SIGPROXY_K3_REORDER_COMMUTE_RCOMP_flip --> | FA 0.143<!-- n:ctl_SIGPROXY_K3_CONTRAPOSITIVE_RCOMP_fa --> / base FA 0.143<!-- n:ctl_SIGPROXY_K3_CONTRAPOSITIVE_RCOMP_base --> / flip 0.000<!-- n:ctl_SIGPROXY_K3_CONTRAPOSITIVE_RCOMP_flip --> |

The eval-3 table in section 1 gives a larger c_align NONCE flip (0.605<!-- n:pc_c_align_RENAME_NONCE_flip -->) than exp 10 (0.327<!-- n:x10_flip_nonce -->); they pair renames with different base rows (eval 3: exp-8 PERTURB scoring; exp 10: its own base join) and are reported side by side, not harmonised.

**SIGPROXY (out-of-scope controlled vocabulary; R_COMP SIG).** k = 3 within-template AUROC 0.930 [0.916, 0.943]<!-- n:x10_sigproxy -->. On the same long templated bases, correct-base FA d is 0.149<!-- n:x10_d_cued --> cued vs 0.757<!-- n:x10_d_uncued --> uncued FREE3-ALIGN, paired −0.608 [−0.716, −0.500]<!-- n:x10_d_diff --> — with base FA shown, not recall alone. Prior art: see section 7 (Vossel; ARc).

**Typing (which kind of error).** free3 on E 0.123 [0.081, 0.169]<!-- n:x10_free3 -->; peer-medoid 0.328<!-- n:e8_typ_medoid --> ≈ judge 0.326<!-- n:e8_typ_judge --> (exp 8). `oracle` repairs against the known gold base: it is **GOLD-USING**, not a gold-free metric (0.928<!-- n:x10_oracle --> on E). SIGPROXY majority 0.784 [0.711, 0.849]<!-- n:x10_proxy --> is within a shared vocabulary (out of scope). **Answer to the user's "which kind of error": NEGATIVE outside a shared vocabulary.**

**T8 (R_COMP FREE, label-free).** ALIGN pairwise agreement among FREE candidates 0.219<!-- n:x10_t8_align -->.

Sources: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/results/tables.md`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/results/anchoring.csv`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/results/controls_fa.csv`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/results/d_by_length.csv`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/results/typing_csc.csv`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/results/rcomp_sig_csc.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/results/paired_cue_effect.csv`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/results/api_cost_ledger.jsonl`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/review_report/review_report/audit/recompute_perturb_csc.json`


## 11. §4.4 / §4.5 caveats (E2 and R_COMP FREE)

Replaces: paper_draft.md `### 4.4 Dataset 4: E2 confirmation set — partial`, lines 1184-1201; Replaces: paper_draft.md `### 4.5 Dataset 5: R_COMP FREE name-free labels`, lines 1202-1230

~~Gate balanced accuracies (P1 0.861, P3 0.875, R1 0.837) all pass the gate.~~ [Correction, iter 4: the drift stop rule is UNDECIDED (passes = False<!-- n:d4_passes -->): the replay was cut off; the combined agreement 0.394<!-- n:d4_comb --> counts unreplayed items, while on the replayed items majority agreement is 0.9725<!-- n:d4_repl -->; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/panel_drift_E2.json] (paper_draft.md L1198)

~~Of 420 old tier-A ERROR rows, 297 are MAPPED (70.7%).~~ [Correction, iter 4: 'up to 70.7%<!-- n:d5_707 -->' (MAPPED is an upper bound: in the executor audit only 0.867<!-- n:d5_mapped_f --> of MAPPED rows are faithful); source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results/old_label_agreement.json] (paper_draft.md L1229)

**E2 (dataset 4).** 550 sentences are frozen and sealed; a 30-sentence pilot gave 36<!-- n:d4_err --> ERROR / 274<!-- n:d4_unres --> UNRESOLVED (incl. gold-as-system) / 20<!-- n:d4_unp --> UNPARSEABLE / 0<!-- n:d4_cor --> CORRECT: no cell is testable. **Panel drift:** the stop rule is UNDECIDED. The replay was incomplete (32<!-- n:d4_trackh_repl --> of 192<!-- n:d4_trackh_n --> track-H judgements got ≥ 2 new votes); synthetic gate items agree 0.974<!-- n:d4_syn -->; on the 22<!-- n:d4_n22 --> replayed unambiguous track-H judgements today's panel flags 0.12<!-- n:d4_flag_today --> of original errors vs 0.84<!-- n:d4_flag_E --> in E — a drift ALARM on small n that came from the incomplete replay, whose replayed items agree 0.9725<!-- n:d4_repl -->. Iteration 5's E2-A decides it (`e2/E2_DRIFT_DECISION.json`). Spend $0.241<!-- n:d4_spend -->; projected completion $6.79<!-- n:d4_proj -->. Deviations D0–D7 (verbatim from `dataset_card.md`):

- **D0**: or_client.py base-URL transport fix (none on labels).<!-- v:dataset_card.md -->
- **D1**: src_e2/compat.py makes E's MALLS-only branches (gold row as a system, blind gold audit counted as GOLD_WRONG, reference repair) apply to the ProverQA DT gold, as the plan requires ('MALLS gold and ProverQA gold get the same audit'). E's code is unmodified; the shim wraps the source string. (DT sentences get the MALLS treatment instead of E's CTRL treatment (DISPUTED_REFERENCE)).<!-- v:dataset_card.md -->
- **D2**: E's code is copied to ./src and ./labeller (not ./src_E) because its ROOT-relative paths require that layout; E2 wrappers live in ./src_e2 (none).<!-- v:dataset_card.md -->
- **D3**: EXC core-marker supply is exhausted: pools (a) and (b) are empty (E took all 67 MALLS-train core items; MALLS-test has only 3 core-marker items, all excluded). EXC = 'without' + non-XOR 'but not' items; core-marker share 0.0. Fallback (iv): keep EXC, never borrow E sentences. (EXC on E2 is about weaker exception constructions; the EXC-core testability row is empty by construction).<!-- v:dataset_card.md -->
- **D4**: generator calls whose final failure was a transient provider error (HTTP 429 upstream rate limit on microsoft/phi-4 during the pilot: 11 calls) were re-issued at lower concurrency by `src_e2/gen_retry.py`, which calls E's frozen generate.amain; the later record wins, as in E. E had no such failures, so treating them as data would have made E2 differ from E. Deterministic failures remain data.<!-- v:dataset_card.md -->
- **D5**: the run-level budget stop (§0). Panel, repair, the remaining generation and the rest of the drift check are pending. The final rule, applied without votes, gives UNRESOLVED / A_unaudited_ref exactly as E's assemble does in that case.<!-- v:dataset_card.md -->
- **D6**: generation latency is not recorded (E's frozen generate.py does not store it), so `metadata_latency_s` is null.<!-- v:dataset_card.md -->
- **D7**: the plan's `dataset_search_plan` names `gen_plan/gen_plan_dataset_1/` as the write location. All files are in this artifact's workspace instead, because gen_art executors may write only there.<!-- v:dataset_card.md -->

**R_COMP FREE (dataset 5).** Search-only labels: ERROR_CERT 759<!-- n:d5_err -->, MAPPED 1,506<!-- n:d5_map -->, UNPARSEABLE 188<!-- n:d5_unp -->, NO_OUTPUT 199<!-- n:d5_noout -->; CORRECT 0<!-- n:d5_cor --> (gloss not run). Search soundness: 0<!-- n:d5_false --> false ERROR_CERT on 1,595<!-- n:d5_1595 --> renamed SIG-CORRECT rows; known-ERROR rescue 9%<!-- n:d5_resc_n --> (nonce) / 10%<!-- n:d5_resc_s --> (synonym), by template up to T8 0.27<!-- n:d5_t8 --> and T9 0.37<!-- n:d5_t9n -->–0.43<!-- n:d5_t9s -->. Executor audit: ERROR_CERT precision 0.867 [0.76, 0.93]<!-- n:d5_prec -->; MAPPED faithful 0.867<!-- n:d5_mapped_f -->; the disagreement sample includes a MAPPED certificate that swaps `LivesIn` and `StudentInClass` (a real error passing the search; `old_label_agreement.json` sample 0). Old iter-3 labels: UP TO 70.7%<!-- n:d5_707 --> of old ERROR rows are MAPPED; old/new kappa 0.058<!-- n:d5_kappa -->. Pointer: §3.3 carries the VOID marker (section 2). Deviations D1–D9 (verbatim, incl. D6, the map-family amendment after the freeze):

- **D1**: a 12-row FREE dev trial of the search code (seed 3) printed maps before the v1 freeze; no labels / scores / gloss<!-- v:deviations.json -->
- **D2**: B1/B2/B5 uncapped; only structural bridges (B3/B4) capped at 2, instead of the plan's 'at most 2 bridge uses'<!-- v:deviations.json -->
- **D3**: B2 generalised to n-ary constant absorption; gate class NO_MERGE added (7 classes)<!-- v:deviations.json -->
- **D5**: audit (i) uses all 2,140 on-signature SIG rows (CORRECT/ERROR/READING_CHOICE), not the plan's 1,904 scored subset<!-- v:deviations.json -->
- **D6**: a map never combines a B3 merge with a B4 split (structural uses <= 2 of ONE kind)<!-- v:deviations.json -->
- **D7**: verify.py from dataset 3 not vendored (it depends on dataset-3 common.py and is not called); vendored functions are ast-extracted, not whole files, where the source file also holds aligner / similarity helpers (repair_census, perturb, fol_triage, sig_prompt, l<!-- v:deviations.json -->
- **D8**: T8 reading choice resolved at the gloss level: converse-equivalent maps are stored with reading=converse; label CORRECT if some weak/strong map passes both checkers, else READING_CHOICE if some converse map does, else ERROR_GLOSS / UNRESOLVED_GLOSS<!-- v:deviations.json -->
- **D9**: NO LLM CALL COULD BE MADE. The first gate call returned HTTP 403 aii_run_budget_exhausted ("AI Inventor per-run OpenRouter budget reached for Test idea: $7.04 of $7.00 spent by this run in that phase ... It does not reset while this run goes on"); the budget h<!-- v:deviations.json -->

Sources: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/panel_drift_E2.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/dataset_card.md`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/sealed/labels_E2.jsonl`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/pilot_projection.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results/soundness_audit.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results/old_label_agreement.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/deviations.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_5/results/testability_FREE_v2.json`


## 12. §4.6 Evaluation 3 rewritten (wrong peers, not words)

Replaces: paper_draft.md `### 4.6 Evaluation 3: T8 vocabulary analysis`, lines 1231-1269

~~The predicted d_floor (0.402) closely matches the observed END_MAJ d (0.415), indicating that the Part-1 model accounts for the observed disagreement among correct translations.~~ [Correction, iter 4: the reverse: the post-hoc instruments predict almost no fix (bracket 0.396<!-- n:e3_br_lo -->–0.415<!-- n:e3_br_hi -->); the pre-registered gap_closed rule is ill-conditioned (denominator 0.013<!-- n:e3_denom -->); source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/README.md] (paper_draft.md L1252)

~~The R_exact AUROC (0.683) is the theoretical performance of cross-family exact-match consensus on R_COMP under independent vocabulary—substantially below the SIG condition's 0.952.~~ [Correction, iter 4: the struck number is d under the exact rule on E's 3-pool (0.683<!-- n:e3_683 -->); it is a divergence rate on E, not a ranking statistic and not R_COMP; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/p1_rule_cuts.csv] (paper_draft.md L1252)

~~| R_exact AUROC | 0.683 |~~ [Correction, iter 4: row relabelled "d under R_exact (E 3-pool)"; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/p1_rule_cuts.csv] (paper_draft.md L1248)

~~**NOT VALIDATED.** The Part-1 model systematically underestimates d in the FREE regime, because it does not account for vocabulary-driven non-transitivity of equivalence (FREE nontransitivity rate: 0.131; SIG: 0.000).~~ [Correction, iter 4: the method UNDER-COUNTS vocabulary effects (predicted endorsement 0.20<!-- n:e3_pred_rate --> vs actual SIG 0.575<!-- n:e3_sig_rate -->); non-transitivity (0.131<!-- n:e3_nontrans -->) is a separate diagnostic; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/results/part2.json] (paper_draft.md L1260)

~~The Part-1 d_floor model closely matches observed d (0.402 predicted vs 0.415 observed) but is NOT VALIDATED against FREE data (calibration error −0.372).~~ [Correction, iter 4: the instruments are shown to under-count vocabulary effects (calibration error −0.372 [−0.423, −0.323]<!-- n:e3_calib -->); source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/results/part2.json] (paper_draft.md L1286)

**Main finding (label-based; no instrument needed).** Among pairs of a CORRECT candidate and a non-agreeing peer, 77%<!-- n:e3_77 --> (9 families) / 61%<!-- n:e3_61 --> (3-pool) of those peers are labelled ERROR, so d on E is mostly peer error, not vocabulary. Among CORRECT–CORRECT disagreements only 9%<!-- n:e3_9 --> are vocabulary-resolvable. Pair classes (9 families): IRREDUCIBLE 69.4%<!-- n:e3_irr -->, EXACT 13.6%<!-- n:e3_exact -->, ALIGN_ONLY 15.1%<!-- n:e3_align -->, VOCAB 1.6%<!-- n:e3_vocab -->, NAME_ONLY 0.3%<!-- n:e3_name -->.

**The instruments.** On the 3-pool, END_MAJ d is 0.415<!-- n:e3_endmaj3 -->; the instrument bracket is 0.396<!-- n:e3_br_lo -->–0.415<!-- n:e3_br_hi --> with prediction 0.402<!-- n:e3_pred -->, so the pre-registered gap_closed denominator is 0.013<!-- n:e3_denom --> (ill-conditioned). Where the true effect of a shared vocabulary is known (R_COMP SIG vs FREE), the method predicts endorsement 0.20<!-- n:e3_pred_rate --> against an actual 0.575<!-- n:e3_sig_rate -->: calibration error −0.372 [−0.423, −0.323]<!-- n:e3_calib -->, NOT VALIDATED. The post-hoc instruments predict almost no fix and are shown to under-count vocabulary effects. SIG also changes granularity (D7), so the SIG − FREE exact-agreement drop +0.479 [0.447, 0.513]<!-- n:e3_drop --> (pairwise exact agreement SIG 0.528<!-- n:e3_sigx --> vs FREE 0.048<!-- n:e3_freex -->) is an upper bound; row endorsement SIG 0.575<!-- n:e3_sigrow --> vs FREE 0.193<!-- n:e3_freerow -->.

**Oracle floors (no anchoring).** 3-pool 0.385<!-- n:e3_oracle3 --> (labelled denominator 0.345<!-- n:e3_labdenom -->); L25 0.542<!-- n:e3_oracle_l25 --> vs END_MAJ 0.735<!-- n:e3_endmaj_l25 -->; 9 families 0.586<!-- n:e3_oracle9 --> > END_MAJ 0.537<!-- n:e3_endmaj9 -->, because most peers are wrong. e ceiling 0.162<!-- n:e3_ecap -->.

**Other diagnostics.** Specificity placebo (VOCAB vs random IRREDUCIBLE pairs): ratio 1.98 [0.43, 11.4]<!-- n:e3_placebo3 --> (3-pool), 0.83 [0.19, 3.29]<!-- n:e3_placebo9 --> (9 families): VOCAB agreements are not label-specific. Label-free counterfactual c_vres − c_score_align on L25: −0.014 [−0.028, −0.001]<!-- n:e3_vres --> (9 families), −0.032 [−0.079, 0.010]<!-- n:e3_vres3 --> (n.s.: CI covers 0) (3-pool). NET Δ(e+d) words T3 − T1 degrades under every rule: +0.35<!-- n:e3_net_lo --> (9-family R_align), +0.368<!-- n:e3_net9_pl --> (9-family R_point_label), +0.348<!-- n:e3_net3_pl --> (3-pool R_point_label), +0.39<!-- n:e3_net_hi --> (3-pool R_align).

**Power (iteration 5).** L25 yield 0.37<!-- n:pw_yield -->. MDE80 vs flash-lite disguised at 250 / 300 / 350 / 400 planned L25: 0.130<!-- n:pw_mde_250 --> / 0.119<!-- n:pw_mde_300 --> / 0.110<!-- n:pw_mde_350 --> / 0.103<!-- n:pw_mde_400 -->; power at the observed L25 Δ (+0.069<!-- n:t1_l25 -->): 0.32<!-- n:pw_pow_250 --> / 0.37<!-- n:pw_pow_300 --> / 0.42<!-- n:pw_pow_350 --> / 0.47<!-- n:pw_pow_400 --> (all MARGINAL). Detecting the observed L25 effect needs ~882<!-- n:pw_882 --> planned L25 sentences; the long pool needs ~237<!-- n:pw_237 --> usable sentences. R_COMP FREE needs ≥ 200<!-- n:e3_200 --> CORRECT rows. Eval-3 deviations D1–D10 are in its README; its reusable functions are in `function_inventory.csv` (section 16).

Sources: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/README.md`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/results/part1.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/results/part1_net.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/results/part2.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/p1_rule_cuts.csv`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/p1_class_shares.csv`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/power_E2.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/p3_planned_E2.csv`


## 13. ONE cost table (units explicit)

Replaces: every cost statement in §3.3, §3.5, §3.6 and §4.6 (markers in sections 2 and 3). FULL = all API spend to produce the score; MARGINAL = only the extra work given peers already exist. Ratio = cost ÷ the flash-lite judge per item-call ($4.9e-5<!-- n:cost_flash --> per item-call); ratios are given only where the unit is per item/candidate.

| item | unit | FULL / MARGINAL | $ | ratio vs flash-lite | source |
|-|-|-|-|-|-|
| `judge_cheap` | per item-call | FULL (API) | $4.88e−5<!-- n:cu_judge_cheap_USD_per_item_call --> | 1.00<!-- n:cu_judge_cheap_USD_per_item_call_ratio -->× | `cost_units.csv` |
| `judge_cheap2` | per item-call | FULL (API) | $2.01e−5<!-- n:cu_judge_cheap2_USD_per_item_call --> | 0.41<!-- n:cu_judge_cheap2_USD_per_item_call_ratio -->× | `cost_units.csv` |
| `strong` | per item-call | FULL (API) | $3.65e−3<!-- n:cu_strong_USD_per_item_call --> | 74.91<!-- n:cu_strong_USD_per_item_call_ratio -->× | `cost_units.csv` |
| `roundtrip` | per item-call | FULL (API) | $2.75e−5<!-- n:cu_roundtrip_USD_per_item_call --> | 0.56<!-- n:cu_roundtrip_USD_per_item_call_ratio -->× | `cost_units.csv` |
| `sc5` | per item-call | FULL (API) | $6.65e−5<!-- n:cu_sc5_USD_per_item_call --> | 1.36<!-- n:cu_sc5_USD_per_item_call_ratio -->× | `cost_units.csv` |
| `consensus c_score_align` | per item (candidate) | FULL (peer generation + z3) | $1.21e−4<!-- n:cu_consensus_c_score_align_USD_per_item__candidate_ --> | 2.48<!-- n:cu_consensus_c_score_align_USD_per_item__candidate__ratio -->× | `cost_units.csv` |
| `k-pool k=1.0` | per sentence | FULL (peer generation, expected over random k-subsets) | $3.15e−4<!-- n:cu_k_pool_k_1_0_USD_per_sentence --> |  | `cost_units.csv` |
| `k-pool k=3.0` | per sentence | FULL (peer generation, expected over random k-subsets) | $9.46e−4<!-- n:cu_k_pool_k_3_0_USD_per_sentence --> |  | `cost_units.csv` |
| `k-pool k=5.0` | per sentence | FULL (peer generation, expected over random k-subsets) | $1.58e−3<!-- n:cu_k_pool_k_5_0_USD_per_sentence --> |  | `cost_units.csv` |
| `k-pool k=7.0` | per sentence | FULL (peer generation, expected over random k-subsets) | $2.21e−3<!-- n:cu_k_pool_k_7_0_USD_per_sentence --> |  | `cost_units.csv` |
| `SIG peer generation` | per candidate | FULL (generation) | $1.16e−4<!-- n:cu_SIG_peer_generation_USD_per_candidate --> | 2.39<!-- n:cu_SIG_peer_generation_USD_per_candidate_ratio -->× | `cost_units.csv` |
| `SIG peer generation` | per sentence (10 slots) | FULL (generation) | $1.16e−3<!-- n:cu_SIG_peer_generation_USD_per_sentence__10_slots_ --> |  | `cost_units.csv` |
| `marginal z3 check` | per candidate | MARGINAL (z3 only) | $2.50e−7<!-- n:cu_marginal_z3_check_USD_per_candidate --> | 0.01<!-- n:cu_marginal_z3_check_USD_per_candidate_ratio -->× | `cost_units.csv` |
| CSC (exp 9, G5) | per candidate | FULL (undeduped) | $5.25e-4<!-- n:x9_g5 --> | 10.77<!-- n:g5_ratio -->× | `csc_gate_E.json` |
| CSC (exp 9, G5) | per candidate | FULL (dedup-apportioned) | $2.76e-4<!-- n:x9_g5_dd --> | 5.67<!-- n:g5dd_ratio -->× | `results/analysis.json g_cost` |
| E2 pilot, L25 (generation + panel + repair) | per sentence | FULL (projection) | $0.0118<!-- n:d4_pilot_usd --> | — | `pilot_projection.json` |

The frontier judge costs 30.2<!-- n:rv_frontier_x -->× the consensus score per ITEM (FULL); the ratio struck in section 2 mixed a per-call judge price with a per-candidate generation price.

Sources: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/cost_units.csv`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/csc_gate_E.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/pilot_projection.json`


## 14. Iteration-4 spend table (ledgers only)

Replaces: the three different budget statements in §4.1–§4.4 (`budget event at $0.108`, `run-wide budget exhausted by earlier artifacts`, `exhausted at 07:26 UTC`).

Method: every `*ledger*.json(l)` and `budget_state.json` under the run root was read (60 files; 13 byte-identical copies dropped, e.g. repo clones), and records were de-duplicated across files by (second, model, cost). Window: 2026-09-24T01:13:50+00:00 (earliest iteration-4 ledger record minus 6 h) to 2026-09-24T07:26:41+00:00 (first HTTP 403 budget refusal, `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4/logs/gate.log`).

| artifact (ledger dir) | $ in window | records |
|-|-|-|
| `3_invention_loop/iter_3/gen_art/gen_art_experiment_6` | $2.3953<!-- n:spend_loop_iter_3_gen_art_gen_art_experiment_6 --> | 36926 |
| `3_invention_loop/iter_3/gen_art/gen_art_experiment_7` | $1.5974<!-- n:spend_loop_iter_3_gen_art_gen_art_experiment_7 --> | 11389 |
| `3_invention_loop/iter_3/gen_art/gen_art_experiment_8` | $0.3452<!-- n:spend_loop_iter_3_gen_art_gen_art_experiment_8 --> | 6710 |
| `3_invention_loop/iter_4/gen_art/gen_art_dataset_4` | $0.2409<!-- n:spend_on_loop_iter_4_gen_art_gen_art_dataset_4 --> | 412 |
| `3_invention_loop/iter_4/gen_art/gen_art_experiment_9` | $0.1082<!-- n:spend_loop_iter_4_gen_art_gen_art_experiment_9 --> | 1166 |
| `3_invention_loop/iter_4/gen_art/gen_art_experiment_10` | $0.0000<!-- n:spend_oop_iter_4_gen_art_gen_art_experiment_10 --> | 2 |
| `3_invention_loop/iter_3/gen_art/gen_art_research_1` | $0.0000<!-- n:spend_n_loop_iter_3_gen_art_gen_art_research_1 --> | 8 |

- Iteration-4 artifacts: $0.349<!-- n:spend_iter4 --> (exp 9 $0.108<!-- n:x9_spend -->, exp 10 $0.0000088<!-- n:x10_spend -->, dataset 4 $0.241<!-- n:d4_spend -->, dataset 5 $0<!-- n:sp_d5 -->; eval 3 has no ledger, CPU only).
- Other artifacts whose ledger records fall inside the same window: $4.338<!-- n:spend_other --> (iteration-3 experiments). The ledgers do not record which phase budget these calls were charged to; this table does not attribute them.
- Evidenced total in the window: $4.687<!-- n:spend_evidenced --> vs the $7.00<!-- n:spend_budget --> 'Test idea' phase budget: **unaccounted $2.313<!-- n:spend_unacc --> (no ledger in the run tree records it)**.
- What the ledgers themselves say about the budget (verbatim notes): "run Test-idea budget $7.04 of $7.00 already spent by earlier steps; nothing billed"<!-- v:cost_ledger.jsonl --> "run-level Test-idea budget $12.08 of $12.00 spent by the run (all parallel artifacts); nothing billed"<!-- v:cost_ledger.jsonl -->
- iter_4 gen_art directories without any ledger: `gen_art_evaluation_3`.

Sources: `results/spend_iter4.json`; `src/spend.py`


## 15. Dead ends (extended, with sources)

Replaces: the "Dead ends accumulated across all iterations" table in §4.7.

~~| Name-free consensus (c_nf) | 2-3 | SWAP recall 0.512 (sacrifices structural-error detection) |~~ [Correction, iter 4: the reason is the pre-registered selection failure (PERTURB RENAME_SYN / NONCE FA, selection rule without paired flip, 0.686<!-- n:e8_nf_syn --> / 0.485<!-- n:e8_nf_nonce -->) plus blindness to MEANING_RENAME (0.499<!-- n:e8_cnf_mr -->); source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/selection.json] (paper_draft.md L1300)

| dead end | iteration | reason | source |
|-|-|-|-|
| Rename-invariant selection (NF-anchored and HYB) | 3 | both INELIGIBLE (FA-only selection rule, no flip): RENAME_SYN / NONCE FA NF 0.686<!-- n:e8_nf_syn --> / 0.485<!-- n:e8_nf_nonce -->, HYB 0.841<!-- n:e8_hyb_syn --> / 0.700<!-- n:e8_hyb_nonce -->; nothing frozen | `rename_selection_dead_end.csv`, `selection.json` |
| Name-free consensus `c_nf` | 2-3 | pre-registered selection failure + MEANING_RENAME blindness (0.499<!-- n:e8_cnf_mr -->) | `selection.json`, `perturb_sensitivity.csv` |
| Candidate B1 | 1 | planned, never ran (workspace holds 0<!-- n:b1_files --> files — empty) | `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_2` |
| FOL-Triage fused score | 1 | fails the rewrite-FA gate (worst-family FA 0.275<!-- n:iter1_triage_fa --> vs a `0.10` bar; equals the FA on originals) | `iter_1/gen_art/gen_art_experiment_1/README.md` |
| P2 / P4 (exp 5) | 2 | P2 REFUTED, P4 REFUTED<!-- v:p_tests.json --> | `p_tests.json` |
| B2 decomposed z3 reader | 2 | gate failure: balanced accuracy 0.476<!-- n:ev2_b2_gate --> | `b2_dead_end.csv`, eval-2 `hypothesis_verdicts.csv` |
| R_ADJ LLM adjudicator | 2 | gate failure: Sonnet-5 balanced accuracy 0.767<!-- n:ev2_radj_all --> overall, 0.662<!-- n:ev2_radj_h --> on expert track-H | `radj_gate.csv`, eval-2 `hypothesis_verdicts.csv` |
| CSC, CSC_graded, CSC_multi, HYB_MEAN | 4 | all fail G1 (d slopes positive); CSC provisional negative on a completion-selected subset; L25 and RENAME untested | `csc_gate_E.json` |
| E2 EXC-core stratum | 4 | core-exception supply exhausted (D3) | dataset 4 `dataset_card.md` |
| CSC arms and the panel route for R_COMP FREE | 4→5 | CLOSED by the iteration-5 hypothesis | iter_4 `upd_hypo` |
| Vocabulary-divergence diagnosis of iteration 3 | 3→4 | refuted on E by the label-based decomposition (section 12) | eval 3 `p1_class_shares.csv` |

Sources: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/rename_selection_dead_end.csv`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/selection.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/perturb_sensitivity.csv`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/p_tests.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/tables/b2_dead_end.csv`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/tables/radj_gate.csv`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/csc_gate_E.json`


## 16. Coverage against the request (iteration 4 update + iteration-5 pending cells)

Insert as a table in §4.7 (and the final summary).

**One-line answers (iteration 4):**

| requirement | answer after iteration 4 | pending in iteration 5 |
|-|-|-|
| Long, heavily conditioned sentences | UNTESTED in iteration 4 (CSC L25 NOT_READ; E2 0<!-- n:d4_cor --> CORRECT rows); on development E, L25 Δ +0.069 [−0.020, 0.148]<!-- n:t1_l25 --> (n.s.: CI covers 0) | `confirm_verdict_E2A.json`, `confirm_verdict_E2B.json`, `union_longpool.json` |
| No ontology / controlled vocabulary | consensus UNVALIDATED (R_COMP FREE CORRECT class empty); the only positive iteration-4 numbers (SIGPROXY 0.930<!-- n:x10_sigproxy -->; d 0.149<!-- n:x10_d_cued -->) are in the excluded SIG regime | `confirm_verdict_rcomp.json` |
| Which kind of error | NEGATIVE outside a shared vocabulary: free3 0.123<!-- n:x10_free3 --> on E; medoid 0.328<!-- n:e8_typ_medoid --> ≈ judge 0.326<!-- n:e8_typ_judge --> | none (no new budget) |
| Invariance | rename non-invariance measured: c_align NONCE / SYN FA 0.765<!-- n:e8_calign_nonce --> / 0.565<!-- n:e8_calign_syn --> with flips 0.327<!-- n:x10_flip_nonce --> / 0.182<!-- n:x10_flip_syn -->; 9-peer ΔFA +0.273<!-- n:x9_t15_d --> | `freeze/gg_gate.json`, `rename_E2.json` |
| Per-type sensitivity | per-operator consensus AUROC is an artefact; per-class e on real errors (section 9) | `hmech_E2.json` |
| Coverage | counted: PERTURB 3,419<!-- n:e8_cov_ok --> / 5,402<!-- n:e8_cov_n --> scored | E2 coverage with unparseables in the denominator |
| Cost | one table with units (section 13) | $ and seconds per candidate on E2 |
| Baselines | flash-lite (both views), nano, S4 stacks, frontier ratio 0.957<!-- n:t1_ratio --> (point only) | `judges_costmatched`, `judge_frontier` (E2-B) |
| Complexity | d rises with length in every arm (sections 3, 9, 10) | `hmech_E2.json` (NET) |
| Contamination | flash-lite DiD +0.105 [0.006, 0.201]<!-- n:t1_did --> (marginal) | — |
| Deliverable functions | inventory below (each marked gold-free / gold-using in its row) | `freeze/` library |

Iteration-3 coverage table (verbatim):

| requirement | status | gap | iteration |
|-|-|-|-|
| item-level correlation with correctness | ANSWERED | screen only; long sentences untestable | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| system-level correlation | PARTIAL | <10 systems: descriptive, CI very wide | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| per-error-type sensitivity | SCREEN_ONLY | many cells <15 errors (UNINFORMATIVE) | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| invariance (renaming, reordering, equivalent restatement) | PARTIAL | rewrite sets differ across experiments; RENAME FA 96% (C), fused FA 0.275 (A) | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| coverage with unparseables counted | ANSWERED |  | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| cost | ANSWERED |  | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| baselines: parse rate, round-trip, judge, SC, pilot structural | ANSWERED | SC only in cheap-model form on all items | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| complexity curves (words, quantifiers, depth, conditions, exceptions) | SCREEN_ONLY | long/conditioned strata untestable on the screen; dataset E held-out needed | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| contamination | PARTIAL | null DiD with MDE > 0.05 for most judges | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| gold-error rate | PARTIAL | panel is strict (accepts 0.613 of expert-corrected formulas) | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| correct-but-not-equivalent rate | PARTIAL | panel-dependent | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| error-type identification | PARTIAL | labeller-dependent; screen only | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| reusable (text, fol) functions with docstrings | PARTIAL | several functions lack docstrings / do not take (text, fol) | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| dataset with labels | ANSWERED | held-out labels not analysed here (firewall) | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| negative results | ANSWERED |  | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| Candidate B (template NLI + z3 distinguishing worlds) | MISSING | never executed in iteration 1 | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| item-level correlation with correctness | answered | held-out E; local judge bar only (API bar = T1) | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| system-level correlation | partial | descriptive; wide CIs | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| per-error-type sensitivity | partial | real-error cells thin; PERTURB scoring owned by T5 | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| invariance under meaning-preserving rewrites | answered | fails for aligner consensus; NF variant passes | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| coverage (unparseable counted) | answered |  | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| cost | answered | generation cost of the peer pool from the dataset-E ledger | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| complexity (length, quantifiers, depth, conditions, exceptions) | answered | E only | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| contamination | answered | MDE 0.107-0.139 | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| gold-error rate | answered |  | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| correct-but-not-equivalent rate | answered |  | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| baseline: parse/compile rate | answered |  | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| baseline: round-trip | partial | API round-trip = T1 | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| baseline: LLM-as-judge | partial | API judge on E = T1 | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| baseline: sampling self-consistency | partial | API SC-5 = T1 | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| baseline: structural pilot metrics | answered |  | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| adds signal beyond baselines | partial | API stack = T1 | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| reusable functions | answered |  | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| dataset with labels | answered |  | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| mechanism: why consensus works (errors scatter) | answered | E only; R_COMP rerun in iteration 4 | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
| label bias estimate (adjudicator ceiling) | answered | R_ADJ DROPPED | iter2 (eval-2 table) |<!-- v:coverage_vs_request_iter3.csv -->
|  |  |  | iter3 update |<!-- v:coverage_vs_request_iter3.csv -->
|  |  |  | iter3 update |<!-- v:coverage_vs_request_iter3.csv -->
|  |  |  | iter3 update |<!-- v:coverage_vs_request_iter3.csv -->
|  |  |  | iter3 update |<!-- v:coverage_vs_request_iter3.csv -->
|  |  |  | iter3 update |<!-- v:coverage_vs_request_iter3.csv -->
|  |  |  | iter3 update |<!-- v:coverage_vs_request_iter3.csv -->

Function inventory (verbatim; `oracle`, `exhaustive_map_label`, `gloss_decision` and anything reading a reference are GOLD-USING labelling tools, all others gold-free):

| file | function | what_it_measures |
|-|-|-|
| fol_triage.py | fol_lint | L1. Returns {'codes': sorted smell codes, 'parse_ok': bool, 'z3_unknown': bool}. |<!-- v:function_inventory.csv -->
| fol_triage.py | content_accounting | L2-bow baseline (iter-3 code, LEX matching). flag iff >=1 unanchored predicate or uncarried share > 0.34. |<!-- v:function_inventory.csv -->
| fol_triage.py | formula_role_profile | Formula side of L3, exact. -> {pred_key: {'mono','pos','local_neg','role','force','claim','slots'}}. |<!-- v:function_inventory.csv -->
| fol_triage.py | name_words |  |<!-- v:function_inventory.csv -->
| fol_triage.py | word_match | Text word w matches predicate-name word pw: same Porter stem (exact) or WordNet lemma/synonym/derivation. |<!-- v:function_inventory.csv -->
| fol_triage.py | const_match |  |<!-- v:function_inventory.csv -->
| fol_triage.py | nlp |  |<!-- v:function_inventory.csv -->
| fol_triage.py | text_roles | spaCy dependency roles -> {'tokens': [{'i','w','lemma','role','neg','pos'}], 'generic': bool, 'no_subject': bool} |<!-- v:function_inventory.csv -->
| fol_triage.py | role_accounting | L2-role. -> {'cond_in_up','assert_in_down','pol_flip','slot_swap','exc_wrong','n_role_words','n_resolved','flag', |<!-- v:function_inventory.csv -->
| fol_triage.py | validate_questionnaire | Schema check (frozen). Raises ValueError on invalid structure; returns the normalised object. |<!-- v:function_inventory.csv -->
| fol_triage.py | parse_json_text |  |<!-- v:function_inventory.csv -->
| fol_triage.py | phrase_words |  |<!-- v:function_inventory.csv -->
| fol_triage.py | align_concepts | concept id -> ('pred', key) / ('const', name) / None.  Predicate match: overlap coefficient of phrase content |<!-- v:function_inventory.csv -->
| fol_triage.py | expected_mono |  |<!-- v:function_inventory.csv -->
| fol_triage.py | l3_compare | Per-field mismatch between the text questionnaire q and a formula profile (z3 or LLM-read). |<!-- v:function_inventory.csv -->
| fol_triage.py | l3_score | Sum of the gated field mismatches (weights frozen = 1; each field already a fraction; None -> 0). |<!-- v:function_inventory.csv -->
| consensus.py | jl |  |<!-- v:function_inventory.csv -->
| consensus.py | entry_num |  |<!-- v:function_inventory.csv -->
| consensus.py | fol_ok |  |<!-- v:function_inventory.csv -->
| consensus.py | build_sentences |  |<!-- v:function_inventory.csv -->
| consensus.py | entropy |  |<!-- v:function_inventory.csv -->
| consensus.py | components |  |<!-- v:function_inventory.csv -->
| consensus.py | score_candidate | Pool statistics for one candidate formula (medoid repair filled in later). |<!-- v:function_inventory.csv -->
| consensus.py | sc_scores |  |<!-- v:function_inventory.csv -->
| consensus.py | plant | One typed edit: DROP the right operand of the first ∧/∨, else NEG the first atom. |<!-- v:function_inventory.csv -->
| consensus.py | main |  |<!-- v:function_inventory.csv -->
| peer_text.py | parse_fol | Dataset-E parser. Returns the AST or None (unparseable = coverage failure, never silently dropped). |<!-- v:function_inventory.csv -->
| peer_text.py | to_str | Fully parenthesised Unicode rendering; parse_fol(to_str(e)) == e. |<!-- v:function_inventory.csv -->
| peer_text.py | free_vars |  |<!-- v:function_inventory.csv -->
| peer_text.py | mentions |  |<!-- v:function_inventory.csv -->
| peer_text.py | alpha | Alpha-normalise bound variables to v0, v1, ... in order of their binders (canonical strings; unique binders). |<!-- v:function_inventory.csv -->
| peer_text.py | canon |  |<!-- v:function_inventory.csv -->
| peer_text.py | pred_keys | {(name, arity): True} in order of first occurrence. |<!-- v:function_inventory.csv -->
| peer_text.py | constants |  |<!-- v:function_inventory.csv -->
| peer_text.py | rename | pmap: {(name, arity): new_name}; cmap: {const: new_const}. Bound variables untouched. |<!-- v:function_inventory.csv -->
| peer_text.py | claim_units | -> (units, locations, truncated). The formula is logically equivalent to the conjunction of its units |<!-- v:function_inventory.csv -->
| peer_text.py | units_of | Cached claim units of a canonical formula string -> (tuple(unit canon strings), tuple(unit ASTs), truncated). |<!-- v:function_inventory.csv -->
| peer_text.py | clamp_profile | Rewrite-invariant SEMANTIC signature: for every predicate P, the truth rate of the formula over 128 random finite |<!-- v:function_inventory.csv -->
| peer_text.py | symbol_signature | NAME-FREE signature of every predicate and constant of formula e. |<!-- v:function_inventory.csv -->
| peer_text.py | pred_cost | Structural cost in [0,1]; five components weighted 0.2 each, fixed a priori (not tuned): polarity profile L1/2, |<!-- v:function_inventory.csv -->
| peer_text.py | text_anchor | Sentence token indices matched by the words of a predicate/constant name (exp A word_match: Porter stem or |<!-- v:function_inventory.csv -->
| peer_text.py | anchor_cost |  |<!-- v:function_inventory.csv -->
| peer_text.py | name_free_align | k cheapest peer->candidate symbol bijections (predicates within equal arity; constants separately; arity mismatch = |<!-- v:function_inventory.csv -->
| peer_text.py | fm_vector | Cached truth vectors of formula string s over the fixed random interpretations (one array per domain). |<!-- v:function_inventory.csv -->
| peer_text.py | fm_refutes | True iff some random finite interpretation makes the premise true and the unit false (a genuine countermodel, |<!-- v:function_inventory.csv -->
| peer_text.py | z3_entails | z3: prem ∧ ¬unit unsat -> True; sat -> False; unknown/timeout -> None. |<!-- v:function_inventory.csv -->
| peer_text.py | Entailer | entails(premise, unit) with a per-process cache keyed by canonical strings. |<!-- v:function_inventory.csv -->
| peer_text.py | pair_result | Align peer into the candidate's vocabulary and verify unit entailments in both directions. |<!-- v:function_inventory.csv -->
| peer_text.py | graded_consensus | Graded, name-free consensus of candidate formula cand_s (canonical string) against its peer pool. |<!-- v:function_inventory.csv -->
| peer_text.py | g_from_subset | g_score with a restricted pool (used for the k=6 subsample check); no unit codes. |<!-- v:function_inventory.csv -->
| peer_text.py | nf_medoid | Index of the pool member NF-equivalent to the most other pool members (ties -> first). |<!-- v:function_inventory.csv -->
| peer_text.py | l2_bow | L2-bow (exp A, unchanged): n_unanchored predicates + share of uncarried content words; continuous score = sum. |<!-- v:function_inventory.csv -->
| peer_text.py | l3_z3 | L3 (exp A, unchanged): text questionnaire q vs the exact z3 role profile of the formula; score = sum of gated |<!-- v:function_inventory.csv -->
| peer_text.py | text_side | All TEXT-side columns: l2_bow (+parts), l3_z3 (+fields), l1 lint codes, l2_role count (columns only). |<!-- v:function_inventory.csv -->
| peer_text.py | apply_logistic | model = {'features', 'mean', 'sd', 'coef', 'intercept'}; missing feature -> z = 0. |<!-- v:function_inventory.csv -->
| peer_text.py | fused_score | Frozen PEER+TEXT fusion. Unparseable -> p_error 1.0. peer_unavailable -> frozen TEXT-only model (pre-registered). |<!-- v:function_inventory.csv -->
| peer_text.py | peer_text_score | One-call API: score candidate `fol` for `text` against a list of peer formalisations (other systems / families). |<!-- v:function_inventory.csv -->
| consensus_lib.py | equivalent_modulo_vocab | Iteration-1 eqmv on two formula STRINGS. Returns (True/False/None=UNKNOWN, how in {exact, align, gran, none}). |<!-- v:function_inventory.csv -->
| consensus_lib.py | consensus_score | Binary cross-family consensus of candidate `fol` for sentence `text` against peer formulas. |<!-- v:function_inventory.csv -->
| consensus_lib.py | graded_consensus | Graded (claim-unit) consensus. g_score = 1 - F1(support, coverage): support = share of the candidate's claim units |<!-- v:function_inventory.csv -->
| consensus_lib.py | minimal_typed_repair | Smallest typed edit sequence (depth <= 2; NEG, REV, QUANT, RESTR, CONN, MOVE, DROP, ADD, SWAP, BIND, SCOPE, UNGLUE) |<!-- v:function_inventory.csv -->
| consensus_lib.py | peer_pool | Generate peer formalisations of `text` with dataset E's fewshot_v1 prompt on the E generator slots (one per family; |<!-- v:function_inventory.csv -->
| pairwise.py | init_worker | Same worker limits as exp 5's pool_scoring.init_worker (RLIMIT_AS 3.5 GB, SIGALRM handler). |<!-- v:function_inventory.csv -->
| pairwise.py | pairwise_matrix | Full node x node eqmv matrix for one sentence (see module docstring). |<!-- v:function_inventory.csv -->
| pairwise.py | work | Worker entry: one sentence task -> matrix record (label-free). |<!-- v:function_inventory.csv -->
| pairwise.py | code_sha |  |<!-- v:function_inventory.csv -->
| mechanism.py | ed_decomposition | y: 1 = ERROR, 0 = CORRECT; endorsed: 1 = the cross-family peer rule endorses the candidate. |<!-- v:function_inventory.csv -->
| mechanism.py | normalise_name |  |<!-- v:function_inventory.csv -->
| mechanism.py | make_bins |  |<!-- v:function_inventory.csv -->
| mechanism.py | prereg_cuts |  |<!-- v:function_inventory.csv -->
| mechanism.py | cell_stats | e, d, AUROC_b per rule and AUROC(score) for one cell, with sentence-cluster bootstrap CIs. |<!-- v:function_inventory.csv -->
| mechanism.py | run_cuts | P = consensus-scorable population frame (aligned with boot rows). regimes = {name: (mask, ycol)}. |<!-- v:function_inventory.csv -->
| mechanism.py | graded_trace | (e_t, d_t) at every distinct threshold t of the graded score (flag = c >= t); the ROC = (d_t, 1 - e_t). |<!-- v:function_inventory.csv -->
| mechanism.py | gee_fit | Binomial-logit GEE, exchangeable working correlation, robust SE; falls back to Independence. |<!-- v:function_inventory.csv -->
| mechanism.py | vif_table |  |<!-- v:function_inventory.csv -->
| mechanism.py | verdict_slope |  |<!-- v:function_inventory.csv -->
| mechanism.py | zcols |  |<!-- v:function_inventory.csv -->
| mechanism.py | mechanism_M1_M2 | M1: endorsed ~ z(n_conditions) + z(words) + C(stratum) among R_AB ERROR rows (prediction: n_conditions < 0). |<!-- v:function_inventory.csv -->
| mechanism.py | net_test | Delta(e+d) top vs bottom words tercile (and n_conditions 4+ vs 0-1) with cluster-bootstrap CIs, plus the summed |<!-- v:function_inventory.csv -->
| mechanism.py | scatter_index | Anna-Karenina quantities over CROSS-FAMILY pairs of labelled LLM rows per sentence. |<!-- v:function_inventory.csv -->
| mechanism.py | m3_local | Row-level correctness of the binary decision ~ z(words) on R_AB: consensus END_MAJ vs the local judge thresholded |<!-- v:function_inventory.csv -->
| consensus_rcomp.py | consensus_exact | Share of family-disjoint peers NOT z3-equivalent to `fol` under identical vocabulary (see module docstring). |<!-- v:function_inventory.csv -->
| consensus_rcomp.py | consensus_scores | Frozen exp-5 consensus variants for a candidate against family-disjoint peers with FREE vocabularies. |<!-- v:function_inventory.csv -->
| t8_classes.py | name_only_prefilter | 'z3' if the pair needs a z3 call, otherwise the reason it cannot be NAME_ONLY. |<!-- v:function_inventory.csv -->
| t8_classes.py | normalise_formula |  |<!-- v:function_inventory.csv -->
| t8_classes.py | name_only_eq | See module docstring. |<!-- v:function_inventory.csv -->
| t8_classes.py | work_name_only |  |<!-- v:function_inventory.csv -->

Sources: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/coverage_vs_request_iter3.csv`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/function_inventory.csv`


## 17. "What we have learned" (draft replacement)

Replaces: paper_draft.md `## What we have learned so far`, lines 1307-1326

~~It achieves stratified AUROC 0.741 on held-out E, beating the best cheap LLM judge (0.642) by +0.099 [+0.049, +0.146] and adding +0.039 [+0.021, +0.057] beyond a 28-feature baseline stack.~~ [Correction, iter 4: E is DEVELOPMENT data (it was used to choose the method); nothing on E is confirmation; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json] (paper_draft.md L1309)

~~On long composed sentences with trusted references (R_COMP), it reaches 0.954 within-template AUROC with zero error endorsement.~~ [Correction, iter 4: out-of-scope SIG (controlled vocabulary) result; not evidence for the user's operating condition; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/t2_record.csv] (paper_draft.md L1309)

~~It achieves 96% of the frontier judge's discriminative power at 30× lower cost, and three peer families suffice for 97% of full-pool performance.~~ [Correction, iter 4: point estimate only: ratio 0.957 [0.887, 1.034]<!-- n:rv_frontier_ratio -->; and three families suffice overall but the long tercile needs k95 = 5<!-- n:ev2_k95_t3 -->; source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/results/analysis_T1.json] (paper_draft.md L1309)

~~This creates a practical constraint: the consensus metric works well when a shared ontology or template vocabulary is available (as in R_COMP SIG, AUROC 0.954) but degrades when translators choose vocabulary independently (R_COMP FREE d_floor 0.402, theoretical AUROC 0.683).~~ [Correction, iter 4: both numbers are E quantities and neither is an AUROC; the vocabulary-divergence diagnosis is refuted on E (section 12); source /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/p1_rule_cuts.csv] (paper_draft.md L1317)

**Draft.** On DEVELOPMENT data E, frozen cross-family solver consensus (`c_score_align`) beats the disguised cheap API judge: strat Δ +0.099 [0.049, 0.146]<!-- n:t1_delta -->, long pool +0.116 [0.070, 0.163]<!-- n:t1_long -->, and it adds signal over a 28-feature stack only when nested (+0.039 [0.021, 0.057]<!-- n:t1_nested -->). On L25, the user's priority stratum, it is n.s. (+0.069 [−0.020, 0.148]<!-- n:t1_l25 -->). The frontier ratio 0.957 [0.887, 1.034]<!-- n:t1_ratio --> meets the 95% bar on the point estimate only. k95 = 3<!-- n:ev2_k95 --> peer families overall, but the long-sentence tercile needs 5<!-- n:ev2_k95_t3 -->. Consensus degrades with length (NET +0.356 [0.198, 0.493]<!-- n:ev2_net -->).

The iteration-3 explanation — correct translations disagree about WORDS — is refuted on E: 77%<!-- n:e3_77 --> / 61%<!-- n:e3_61 --> of the peers that disagree with a correct candidate are themselves labelled ERROR, and only 9%<!-- n:e3_9 --> of correct–correct disagreement is vocabulary-resolvable. Every vocabulary bridge trades d for e: the aligner lowers FULL d from 0.583<!-- n:x9_full_d_fx --> to 0.328<!-- n:x9_full_d_fa --> but raises meaning-rename e from 0.104<!-- n:x9_t9b_mr_fx --> to 0.624<!-- n:x9_t9b_mr_fa -->; cueing peers with the candidate's symbols (CSC) lowers d to 0.139<!-- n:x9_d_csc --> but raises e to 0.459<!-- n:x9_e_csc -->. CSC is a **provisional negative on a completion-selected subset; L25 and RENAME untested**. Error typing is negative outside a shared vocabulary (free3 0.123<!-- n:x10_free3 -->). The SIG results (0.954<!-- n:t2_sig -->; SIGPROXY 0.930<!-- n:x10_sigproxy -->) are out of scope. Nothing here is confirmed; the confirmation verdict (CONFIRM / PARTIAL / DISCONFIRM) comes from E2, E2-B and R_COMP FREE in iteration 5 (skeleton_iter5.md).

Sources: `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/results/analysis_T1.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/results/part_a.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_evaluation_3/tables/p1_class_shares.csv`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_9/results/analysis.json`; `/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_experiment_10/results/typing_csc.csv`
