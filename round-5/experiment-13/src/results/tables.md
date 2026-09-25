# R_COMP FREE confirmation (iteration 5): tables

Every number below comes from the file named on its `# source:` line. PROVISIONAL = ERROR_CERT vs MAPPED labels (non-confirmatory, see prereg_addendum_fallbackB.json). All AUROCs are within-template unless marked pooled; CIs are template-stratified sentence-cluster bootstrap percentiles (B=2000, seed 20260924).

## Gloss gate (PASS needs BA >= 0.90 for haiku, qwen and both_yes)
# source: results/gate_diagnostics.json :: gloss_v*_* (confirm/gate_diagnostics.py::main)

| run | checker | BA | recall YES | recall NO | NO_VERDICT | classes < 0.85 |
|---|---|---|---|---|---|---|
| gloss_v1_A | haiku | 0.776 | 0.779 | 0.774 | 0 | YES_SYN, YES_FORM, NO_NONCE, NO_ROLE |
| gloss_v1_A | qwen | 0.855 | 0.837 | 0.873 | 0 | YES_SYN, YES_FORM, NO_NONCE, NO_ROLE |
| gloss_v1_A | both_yes | 0.817 | 0.705 | 0.929 | 0 | YES_SYN, YES_FORM, NO_ROLE |
| gloss_v2_B | haiku | 0.561 | 0.600 | 0.522 | 141 | YES_IDENT, YES_SYN, YES_FORM, NO_NONCE, NO_DONOR, NO_ROLE, NO_MERGE |
| gloss_v2_B | qwen | 0.883 | 0.876 | 0.890 | 0 | YES_SYN, YES_FORM, NO_ROLE |
| gloss_v2_B | both_yes | 0.765 | 0.553 | 0.978 | 0 | YES_IDENT, YES_SYN, YES_FORM |

## Gate failure type (verdicted-only accuracy; single-checker rescue)
# source: results/gate_diagnostics.json (confirm/gate_diagnostics.py::main)

| run | haiku BA on verdicted items | haiku-only passes | qwen-only passes |
|---|---|---|---|
| gloss_v1_A | 0.7764 | False | False |
| gloss_v2_B | 0.8609 | False | False |

## Labels and confirmatory testability
# source: results/analysis_rcomp.json :: confirmatory (confirm/join_and_test.py::confirmatory)

| population | label counts | n ERROR | n CORRECT | TESTABLE |
|---|---|---|---|---|
| all rows | {"ERROR_CERT": 759, "UNRESOLVED_GLOSS_GATE_FAILED": 1506, "UNPARSEABLE": 188, "NO_OUTPUT": 199} |  |  |  |
| untouched | {"ERROR_CERT": 636, "UNRESOLVED_GLOSS_GATE_FAILED": 1175, "UNPARSEABLE": 188, "NO_OUTPUT": 199} |  |  |  |
| P0 disg |  | 602 | 0 | False |
| P0 orig |  | 605 | 0 | False |

**Confirmatory verdict for criterion (c): NOT_TESTABLE** (FALLBACK B: the gloss gate failed twice (gloss_v1 half A, gloss_v2 half B); every MAPPED row is UNRESOLVED_GLOSS_GATE_FAILED, so the gated label set has 0 CORRECT rows).

## PROVISIONAL headline: c_score_align vs flash-lite judge (untouched)
# source: results/analysis_rcomp.json :: provisional_headline (confirm/join_and_test.py::headline)

| view | n (ERR/MAPPED) | AUROC c_align | AUROC judge | delta | 95% CI | p |
|---|---|---|---|---|---|---|
| disg | 1706 (602/1104) | 0.801 [0.770, 0.834] | 0.584 [0.550, 0.618] | 0.217 | [0.175, 0.260] | 0.0000 |
| orig | 1709 (605/1104) | 0.804 [0.774, 0.836] | 0.633 [0.601, 0.666] | 0.171 | [0.135, 0.206] | 0.0000 |

## PROVISIONAL AUROC per metric (untouched, every scored row)
# source: results/analysis_rcomp.json :: metrics_untouched_all_scored (confirm/join_and_test.py::metric_table)

| metric | n | ERR/MAPPED | within-template AUROC | 95% CI | pooled AUROC |
|---|---|---|---|---|---|
| c_score_align | 1802 | 631/1171 | 0.802 | [0.772, 0.834] | 0.806 |
| c_exact | 1802 | 631/1171 | 0.606 | [0.580, 0.633] | 0.597 |
| c_score_hyb | 1802 | 631/1171 | 0.817 | [0.788, 0.848] | 0.825 |
| c_score_nf | 1802 | 631/1171 | 0.743 | [0.710, 0.776] | 0.746 |
| g_align | 1802 | 631/1171 | 0.704 | [0.672, 0.736] | 0.695 |
| g_nf | 1802 | 631/1171 | 0.720 | [0.689, 0.753] | 0.715 |
| judge_cheap_disg | 1715 | 607/1108 | 0.587 | [0.553, 0.621] | 0.583 |
| judge_cheap_orig | 1715 | 609/1106 | 0.633 | [0.603, 0.666] | 0.658 |
| judge_local_disg | 1811 | 636/1175 | 0.527 | [0.491, 0.563] | 0.565 |
| judge_local_orig | 0 | 0/0 | – | – | – |
| not_end_maj_align | 1802 | 631/1171 | 0.599 | [0.571, 0.627] | 0.612 |
| not_end_maj_exact | 1802 | 631/1171 | 0.507 | [0.500, 0.515] | 0.507 |

## PROVISIONAL secondary paired deltas
# source: results/analysis_rcomp.json :: secondary_deltas (confirm/analysis_lib.py::paired_delta)

| delta | n | estimate | 95% CI | p |
|---|---|---|---|---|
| c_align - judge_local_disg | 1802 | 0.275 | [0.230, 0.321] | 0.0000 |
| c_exact - c_align | 1802 | -0.196 | [-0.224, -0.171] | 0.0000 |
| c_hyb - judge_cheap_disg | 1706 | 0.232 | [0.193, 0.274] | 0.0000 |
| c_exact - judge_cheap_disg | 1706 | 0.018 | [-0.025, 0.059] | 0.4030 |
| c_exact - judge_cheap_orig | 1709 | -0.029 | [-0.066, 0.007] | 0.1040 |
| judge_cheap_orig - judge_cheap_disg (contamination view gap) | 1624 | 0.049 | [0.005, 0.094] | 0.0320 |

## PROVISIONAL nesting (5 sentence folds, cross-fitted logistic, rank features)
# source: results/analysis_rcomp.json :: nested (confirm/analysis_lib.py::nested_block)

| comparison | n | AUROC full | AUROC base | delta | 95% CI | perm null p95 | > null p95 |
|---|---|---|---|---|---|---|---|
| [judge_disg + c] - [judge_disg] | 1706 | 0.808 | 0.574 | 0.233 | [0.195, 0.273] | 0.027 | True |
| [judge_orig + c] - [judge_orig] | 1709 | 0.819 | 0.619 | 0.200 | [0.166, 0.231] | 0.033 | True |
| [c + judge_disg] - [c] | 1706 | 0.808 | 0.789 | 0.019 | [0.005, 0.032] | 0.021 | False |
| [c + judge_orig] - [c] | 1709 | 0.819 | 0.795 | 0.023 | [0.009, 0.038] | 0.027 | False |

## PROVISIONAL operating points
# source: results/analysis_rcomp.json :: operating_points (confirm/analysis_lib.py::op_point)

| rule | threshold (score >) | recall | FA | precision |
|---|---|---|---|---|
| c_align_majority_rule_gt_0.5 (label-free) | 0.500 | 0.960 [0.941, 0.973] | 0.691 [0.663, 0.718] | 0.431 [0.405, 0.458] |
| judge_disg_rubric_p_lt_0.5 | 0.500 | 0.766 [0.730, 0.798] | 0.617 [0.588, 0.645] | 0.404 [0.376, 0.432] |
| judge_orig_rubric_p_lt_0.5 | 0.500 | 0.564 [0.524, 0.603] | 0.272 [0.246, 0.299] | 0.532 [0.493, 0.570] |
| c_score_align_FA_bracket_0.10_t_le (label-chosen, descriptive) | 1.000 | 0.000 [0.000, 0.006] | 0.000 [0.000, 0.004] | 0.000 – |
| c_score_align_FA_bracket_0.10_t_gt (label-chosen, descriptive) | 0.889 | 0.787 [0.753, 0.818] | 0.231 [0.207, 0.257] | 0.650 [0.615, 0.684] |
| judge_cheap_disg_FA_bracket_0.10_t_le (label-chosen, descriptive) | 1.000 | 0.000 [0.000, 0.006] | 0.000 [0.000, 0.004] | 0.000 – |
| judge_cheap_disg_FA_bracket_0.10_t_gt (label-chosen, descriptive) | 0.900 | 0.478 [0.439, 0.518] | 0.382 [0.354, 0.411] | 0.406 [0.370, 0.442] |
| judge_cheap_orig_FA_bracket_0.10_t_le (label-chosen, descriptive) | 0.900 | 0.243 [0.210, 0.279] | 0.093 [0.077, 0.112] | 0.588 [0.526, 0.647] |
| judge_cheap_orig_FA_bracket_0.10_t_gt (label-chosen, descriptive) | 0.800 | 0.446 [0.407, 0.486] | 0.198 [0.176, 0.223] | 0.552 [0.508, 0.596] |

## PROVISIONAL sensitivities (delta c_align - judge)
# source: results/analysis_rcomp.json :: sensitivities (confirm/join_and_test.py::sensitivities)

| regime | disg delta [CI] | orig delta [CI] | both CIs > 0 | flip |
|---|---|---|---|---|
| primary_provisional | 0.217 [0.175, 0.260] | 0.171 [0.135, 0.206] | True | False |
| s1a_drop_detector_rows | 0.253 [0.212, 0.294] | 0.174 [0.136, 0.211] | True | False |
| s1b_drop_detector_ERROR_CERT_only | 0.252 [0.212, 0.293] | 0.175 [0.137, 0.212] | True | False |
| s3_all_rows_incl_seen_iter3 | 0.211 [0.171, 0.250] | 0.172 [0.138, 0.206] | True | False |
| s5_drop_qwen235b_slot | 0.221 [0.180, 0.264] | 0.171 [0.134, 0.208] | True | False |
| s7_fewshot_only | 0.215 [0.173, 0.260] | 0.174 [0.137, 0.209] | True | False |
| s10_common_support | 0.219 [0.177, 0.262] | 0.168 [0.131, 0.206] | True | False |
| s9_orig_view_exp7_scored_rows_only | – | 0.188 [0.140, 0.236] | – | – |

## PROVISIONAL per template (s4)
# source: results/analysis_rcomp.json :: sensitivities.s4_per_template (confirm/join_and_test.py::sensitivities)

| template | n disg | disg delta [CI] | orig delta [CI] |
|---|---|---|---|
| T1 | 186 | 0.196 [0.084, 0.313] | 0.187 [0.086, 0.284] |
| T2 | 217 | 0.054 [-0.034, 0.148] | 0.163 [0.072, 0.258] |
| T3 | 188 | 0.280 [0.064, 0.497] | 0.171 [0.074, 0.269] |
| T4 | 190 | 0.364 [0.240, 0.463] | 0.231 [0.142, 0.311] |
| T5 | 197 | 0.345 [0.229, 0.456] | 0.262 [0.147, 0.370] |
| T6 | 182 | 0.204 [0.081, 0.327] | 0.057 [-0.033, 0.152] |
| T7 | 212 | 0.208 [0.089, 0.328] | 0.227 [0.129, 0.321] |
| T8 | 170 | 0.097 [-0.000, 0.210] | 0.102 [-0.001, 0.200] |
| T9 | 164 | 0.240 [0.100, 0.378] | 0.023 [-0.130, 0.189] |

## PROVISIONAL H-MECH (i): labels of non-agreeing peers
# source: results/analysis_rcomp.json :: h_mech.i_nonagreeing_peers (confirm/join_and_test.py::mech_i)

| candidates | rule | peer slots | share ERROR_CERT | share MAPPED | bar >= 0.50 |
|---|---|---|---|---|
| MAPPED_candidates|exact | 9009 | 0.295 [0.269, 0.319] | 0.705 [0.681, 0.731] | False |
| MAPPED_candidates|align | 6456 | 0.407 [0.371, 0.442] | 0.593 [0.558, 0.629] | False |
| ERROR_candidates|exact | 4926 | 0.433 [0.384, 0.480] | 0.567 [0.520, 0.616] | – |
| ERROR_candidates|align | 4688 | 0.414 [0.367, 0.461] | 0.586 [0.539, 0.633] | – |

## PROVISIONAL H-MECH (ii)-(iv)
# source: results/analysis_rcomp.json :: h_mech (eval-2 mechanism.scatter_index / net_test / ed_decomposition, unchanged)

| item | estimate [CI] | bar | result |
|---|---|---|---|
| (ii) SCATTER SI_cor/SI_err | 5.832 [4.141, 8.759] | >= 2 | True |
| (iii) NET delta(e+d) W3-W1, END_MAJ_align | 0.146 [0.008, 0.319] | > 0 | True |
| (iii) NET delta(e+d) W3-W1, MAJ_EXACT | 0.037 [-0.023, 0.099] | > 0 | True |
| (iv) d_align - d_exact (MAPPED not endorsed) | -0.242 [-0.293, -0.190] | < 0 | CONFIRMED |
| (iv) e_align - e_exact, ALL_ERROR (n=631) | 0.032 [0.005, 0.064] | > 0 | CONFIRMED |
| (iv) e_align - e_exact, ERROR_CERT:count_prune_subtree (n=301) | 0.000 [0.000, 0.000] | > 0 | INCONCLUSIVE |
| (iv) e_align - e_exact, ERROR_CERT:no_polarity_compatible_target (n=217) | 0.055 [0.000, 0.127] | > 0 | INCONCLUSIVE |
| (iv) e_align - e_exact, ERROR_CERT:countermodel (n=57) | 0.123 [0.000, 0.308] | > 0 | INCONCLUSIVE |

## EXPLORATORY consensus variants (Holm over 8)
# source: results/analysis_rcomp.json :: exploratory_variants (confirm/join_and_test.py::exploratory_variants)

| delta | estimate | 95% CI | p | p Holm |
|---|---|---|---|---|
| V1_c_pn - c_score_align | -0.009 | [-0.020, 0.001] | 0.0870 | 0.3480 |
| V1_c_pn - judge_cheap_disg | 0.208 | [0.167, 0.250] | 0.0000 | 0.0000 |
| V2_c_rw - c_score_align | 0.002 | [-0.001, 0.006] | 0.1590 | 0.4770 |
| V2_c_rw - judge_cheap_disg | 0.219 | [0.178, 0.262] | 0.0000 | 0.0000 |
| V3_c_pn_rw - c_score_align | -0.006 | [-0.016, 0.004] | 0.2750 | 0.5500 |
| V3_c_pn_rw - judge_cheap_disg | 0.211 | [0.170, 0.254] | 0.0000 | 0.0000 |
| V5_c_v5 - c_score_align | -0.058 | [-0.076, -0.041] | 0.0000 | 0.0000 |
| V5_c_v5 - judge_cheap_disg | 0.159 | [0.117, 0.201] | 0.0000 | 0.0000 |
| V4_c_two_channel - c_score_align | -0.003 | [-0.012, 0.005] | 0.5160 | 0.5500 |
| V4_c_two_channel - judge_cheap_disg | 0.214 | [0.169, 0.259] | 0.0000 | 0.0000 |

## PROVISIONAL complexity (delta c_align - judge per bin; T3-T1 delta-of-deltas; per-metric slopes)
# source: results/analysis_rcomp.json :: complexity (confirm/join_and_test.py::complexity)

| view | dimension | cell | estimate | 95% CI |
|---|---|---|---|---|
| disg | word_tercile | W1 | 0.221 | [0.122, 0.329] |
| disg | word_tercile | W2 | 0.213 | [0.131, 0.291] |
| disg | word_tercile | W3 | 0.182 | [0.107, 0.270] |
| disg | word_tercile | delta_of_deltas_W3_minus_W1 | -0.040 | [-0.178, 0.107] |
| disg | word_tercile | slope_c_align_W3_minus_W1 | -0.133 | [-0.223, -0.035] |
| disg | word_tercile | slope_judge_W3_minus_W1 | -0.093 | [-0.203, 0.023] |
| disg | nconds_weak | 4 | 0.208 | [0.089, 0.328] |
| disg | nconds_weak | 5 | 0.218 | [0.173, 0.264] |
| disg | nconds_weak | delta_of_deltas_5_minus_4 | 0.009 | [-0.115, 0.134] |
| disg | nconds_weak | slope_c_align_5_minus_4 | -0.026 | [-0.102, 0.048] |
| disg | nconds_weak | slope_judge_5_minus_4 | -0.035 | [-0.170, 0.094] |
| orig | word_tercile | W1 | 0.285 | [0.196, 0.361] |
| orig | word_tercile | W2 | 0.164 | [0.107, 0.217] |
| orig | word_tercile | W3 | 0.084 | [0.012, 0.155] |
| orig | word_tercile | delta_of_deltas_W3_minus_W1 | -0.201 | [-0.307, -0.083] |
| orig | word_tercile | slope_c_align_W3_minus_W1 | -0.116 | [-0.206, -0.018] |
| orig | word_tercile | slope_judge_W3_minus_W1 | 0.086 | [-0.030, 0.187] |
| orig | nconds_weak | 4 | 0.227 | [0.129, 0.321] |
| orig | nconds_weak | 5 | 0.162 | [0.125, 0.200] |
| orig | nconds_weak | delta_of_deltas_5_minus_4 | -0.065 | [-0.168, 0.039] |
| orig | nconds_weak | slope_c_align_5_minus_4 | -0.023 | [-0.097, 0.049] |
| orig | nconds_weak | slope_judge_5_minus_4 | 0.042 | [-0.063, 0.139] |

## PROVISIONAL system level (12 systems; descriptive)
# source: results/analysis_rcomp.json :: system_level (confirm/join_and_test.py::system_level)

| metric | Kendall tau-b (system mean score vs ERROR rate) | 95% CI |
|---|---|---|
| c_score_align | 0.697 | [0.364, 0.818] |
| judge_cheap_disg | 0.333 | [0.061, 0.576] |
| judge_cheap_orig | 0.333 | [0.121, 0.667] |
| c_exact | 0.667 | [0.242, 0.788] |

## Coverage over all 2,652 FREE rows (UNPARSEABLE 188, NO_OUTPUT 199 in the denominator)
# source: results/analysis_rcomp.json :: coverage (confirm/join_and_test.py::coverage)

| metric | scored | share |
|---|---|---|
| c_score_align | 2254 | 0.850 |
| c_exact | 2254 | 0.850 |
| c_score_hyb | 2254 | 0.850 |
| c_score_nf | 2254 | 0.850 |
| g_align | 2254 | 0.850 |
| g_nf | 2254 | 0.850 |
| judge_cheap_disg | 2134 | 0.805 |
| judge_cheap_orig | 2148 | 0.810 |
| judge_local_disg | 2265 | 0.854 |
| judge_local_orig | 0 | 0.000 |
| V1_c_pn | 2254 | 0.850 |
| V2_c_rw | 2254 | 0.850 |
| V3_c_pn_rw | 2254 | 0.850 |
| V5_c_v5 | 2250 | 0.848 |
| V4_c_two_channel | 2254 | 0.850 |

## PROVISIONAL unparseable-as-ERROR convention (every metric = 1.0 on UNPARSEABLE rows)
# source: results/analysis_rcomp.json :: coverage.unparseable_as_ERROR_untouched

| view | n | AUROC c_align | AUROC judge | delta [CI] |
|---|---|---|---|---|
| disg | 1894 | 0.820 | 0.636 | 0.184 [0.147, 0.222] |
| orig | 1897 | 0.822 | 0.708 | 0.114 [0.081, 0.147] |

## Cost (metric cost; the labelling cost is separate)
# source: results/analysis_rcomp.json :: cost (confirm/join_and_test.py::costs)

| quantity | value |
|---|---|
| consensus_full_usd_per_candidate_peer_generations | 0.000770 |
| consensus_amortised_usd_per_candidate | 0.000091 |
| consensus_marginal_z3_cpu_seconds_per_candidate_mean | 0.052731 |
| consensus_marginal_z3_cpu_seconds_per_candidate_median | 0.044250 |
| consensus_marginal_api_usd | 0.000000 |
| judge_cheap_usd_per_call_mean | 0.000051 |
| judge_cheap_seconds_per_call_mean | 3.381224 |
| judge_cheap_seconds_per_call_median | 2.009179 |
| labelling_cost_by_phase_usd (NOT a metric cost) | {"gate_gloss_v1_A": 0.06683596600000001, "probe": 0.0, "probe_free_models": 0.0, "gloss_pilot_gate_A": 0.002690015, "gate_gloss_v2_B": 0.17257299850000005, "audit_blind_iter5": 0.94869872, "audit_blind_iter5_probe": 0.00171, "audit_blind_iter5_retry": 0.0} |
| metric_scoring_cost_by_phase_usd (judge completion / frontier judge) | {"judge_orig_completion_iter5": 0.06227909999999987, "frontier_judge_iter5": 0.7149760000000001} |

## Blind two-family audit of the provisional labels (100 ERROR_CERT + 100 MAPPED, untouched)
# source: results/audit_report.json :: by_auditor (confirm/audit_blind.py::report)

| auditor | n ERROR_CERT | ERROR_CERT precision (UNFAITHFUL) | n MAPPED | MAPPED faithful | a (ERR side, excl. UNSURE) | b (MAPPED side, excl. UNSURE) |
|---|---|---|---|---|---|---|
| glm46 | 93 | 0.720 [0.622, 0.801] | 94 | 0.904 [0.828, 0.949] | 0.280 | 0.096 |
| sonnet5 | 97 | 0.845 [0.760, 0.904] | 97 | 0.722 [0.625, 0.801] | 0.155 | 0.278 |
| consensus | 74 | 0.838 [0.738, 0.905] | 72 | 0.917 [0.830, 0.961] | 0.162 | 0.083 |

Auditor agreement: {"n_both": 181, "kappa_4way": 0.5607, "kappa_3way_F_U_S": 0.6205, "raw_agreement_3way": 0.8066}

## Noise-corrected PROVISIONAL AUROCs (non-differential contamination assumption)
# source: results/analysis_rcomp.json :: noise_correction (confirm/join_and_test.py::noise_correction)

| contamination source | view | a | b | AUROC c_align corr. | AUROC judge corr. | delta obs | delta corr. | delta CI corr. |
|---|---|---|---|---|---|---|---|---|
| glm46 | disg | 0.280 | 0.096 | 1.254 | 0.711 | 0.217 | 0.543 | [0.440, 0.653] |
| glm46 | orig | 0.280 | 0.096 | 1.262 | 0.833 | 0.171 | 0.429 | [0.340, 0.518] |
| sonnet5 | disg | 0.155 | 0.278 | 1.103 | 0.669 | 0.217 | 0.434 | [0.352, 0.522] |
| sonnet5 | orig | 0.155 | 0.278 | 1.110 | 0.766 | 0.171 | 0.343 | [0.272, 0.414] |
| consensus | disg | 0.162 | 0.083 | 0.986 | 0.636 | 0.217 | 0.350 | [0.283, 0.420] |
| consensus | orig | 0.162 | 0.083 | 0.991 | 0.714 | 0.171 | 0.276 | [0.219, 0.333] |
| dataset5_executor_audit | disg | 0.133 | 0.133 | 0.973 | 0.632 | 0.217 | 0.340 | [0.275, 0.409] |
| dataset5_executor_audit | orig | 0.133 | 0.133 | 0.978 | 0.709 | 0.171 | 0.269 | [0.213, 0.324] |

Validity (all corrected AUROCs within [0, 1]): `{"glm46": false, "sonnet5": false, "consensus": true, "dataset5_executor_audit": true}`. A corrected AUROC above 1 means the non-differential assumption is violated; the differential check below shows why (audited-faithful ERROR_CERT rows still get high consensus scores).

Differential check (mean score by label x auditor consensus): `{"c_score_align": {"label=MAPPED|auditors=FAITHFUL": {"mean": 0.5841450216450217, "n": 66}, "label=MAPPED|auditors=UNFAITHFUL": {"mean": 0.9100529100529101, "n": 6}, "label=ERROR_CERT|auditors=FAITHFUL": {"mean": 0.7418981481481483, "n": 12}, "label=ERROR_CERT|auditors=UNFAITHFUL": {"mean": 0.9731246799795188, "n": 62}}, "judge_cheap_disg": {"label=MAPPED|auditors=FAITHFUL": {"mean": 0.7734848484848484, "n": 66}, "label=MAPPED|auditors=UNFAITHFUL": {"mean": 0.6666666666666666, "n": 6}, "label=ERROR_CERT|auditors=FAITHFUL": {"mean": 0.9125, "n": 12}, "label=ERROR_CERT|auditors=UNFAITHFUL": {"mean": 0.7588709677419355, "n": 62}}, "judge_cheap_orig": {"label=MAPPED|auditors=FAITHFUL": {"mean": 0.23852459016393446, "n": 61}, "label=MAPPED|auditors=UNFAITHFUL": {"mean": 0.5599999999999999, "n": 5}, "label=ERROR_CERT|auditors=FAITHFUL": {"mean": 0.27083333333333337, "n": 12}, "label=ERROR_CERT|auditors=UNFAITHFUL": {"mean": 0.6517241379310346, "n": 58}}}`

## EXPLORATORY audit-labelled view (LLM-audited, gold-informed labels on the audit sample)
# source: results/analysis_rcomp.json :: audit_labelled_view (confirm/join_and_test.py::audit_view)

| labels | comparison | n | ERR/COR | AUROC a | AUROC b | delta | 95% CI |
|---|---|---|---|---|---|---|---|
| y_aud | disg | 146 | 68/78 | 0.899 | 0.522 | 0.377 | [0.256, 0.502] |
| y_aud | orig | 136 | 63/73 | 0.903 | 0.798 | 0.105 | [0.011, 0.215] |
| y_aud | c_exact_minus_judge_disg | 146 | 68/78 | 0.690 | 0.522 | 0.168 | [0.038, 0.292] |
| y_aud_and_label | disg | 128 | 62/66 | 0.921 | 0.544 | 0.377 | [0.248, 0.508] |
| y_aud_and_label | orig | 119 | 58/61 | 0.926 | 0.797 | 0.129 | [0.027, 0.251] |
| y_aud_and_label | c_exact_minus_judge_disg | 128 | 62/66 | 0.693 | 0.544 | 0.149 | [0.004, 0.286] |

## STEP F frontier judge (gemini-3.1-pro, original view; PROVISIONAL labels; 150-row sample)
# source: results/analysis_rcomp.json :: frontier (confirm/join_and_test.py::frontier_view)

| metric | n | within-template AUROC | 95% CI |
|---|---|---|---|
| c_score_align | 150 | 0.801 | [0.704, 0.886] |
| judge_frontier_orig | 150 | 0.852 | [0.763, 0.922] |
| judge_cheap_orig | 150 | 0.694 | [0.585, 0.788] |
| judge_cheap_disg | 139 | 0.557 | [0.462, 0.653] |
| c_exact | 150 | 0.557 | [0.498, 0.611] |

## STEP F paired comparisons
# source: results/analysis_rcomp.json :: frontier

| comparison | estimate | 95% CI | extra |
|---|---|---|---|
| c_align - frontier | -0.051 | [-0.153, 0.044] | ratio 0.940 [0.825, 1.056] |
| frontier - flash-lite (orig) | 0.158 | [0.043, 0.271] |  |
| [frontier + c] - [frontier] | 0.038 | [-0.015, 0.090] | null p95 0.063 |
| [c + frontier] - [c] | 0.086 | [0.003, 0.166] | null p95 0.088 |
| frontier $/call, s/call | 0.00477 | 28.1 |  |

## Placebos
# source: results/analysis_rcomp.json :: placebos (confirm/join_and_test.py::placebos)

| check | result | pass |
|---|---|---|
| within-template label shuffles: delta CI covers 0 | 17/20 | False |
| post-hoc supplement: 100 shuffles, delta CI covers 0 | 95/100 | (nominal 95/100) |
| random score AUROC | 0.482 [0.453, 0.510] | True |
