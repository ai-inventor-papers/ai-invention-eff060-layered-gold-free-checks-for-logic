# E2-A tables (iteration 5, untouched E2; frozen metrics; labels joined after both seals)

## T1. Verdict of the pre-registered confirmation
# source: results/confirm_verdict_E2A.json

- OVERALL: **NOT_TESTABLE ((a): too few rows with the pre-registered flash-lite disguised bar; see fallback_substitute_bar)**
- (a) R_AB long pool (L25+EXC): n = 94 rows (76 ERROR / 18 CORRECT, 12 sentences), testable = False
  - V0 − flash-lite disguised (PRIMARY): Δ = — — (n = —; pooled-cluster CI —)
  - V0 − flash-lite original: Δ = — — (n = —; pooled-cluster CI —)
  - V0 − nano original: Δ = — — (n = —; pooled-cluster CI —)
  - V0 − nano disguised: Δ = — — (n = —; pooled-cluster CI —)
- (b) nested [S4_E2 + V0] − S4_E2: Δ = -0.064 [-0.134, -0.002]; S4 features used ['judge_local_qwen8b_disg', 'judge_local_qwen8b_orig', 'l2_bow', 'l3_z3']; dropped (<95% coverage) ['judge_cheap_disg', 'judge_cheap_orig', 'judge_cheap2_disg', 'judge_cheap2_orig']
- FALLBACK (declared substitute bar, secondary): prereg_addendum_budgetstop.json: local Qwen3-8B rubric-A judge, DECLARED SUBSTITUTE, secondary, cannot CONFIRM
  - V0_minus_local_disg: Δ = -0.091 [-0.219, 0.017] (n = 94; 76 ERR / 18 COR; testable False)
  - V0_minus_local_orig: Δ = -0.111 [-0.302, 0.017] (n = 94; 76 ERR / 18 COR; testable False)
  - PT_minus_local_disg: Δ = 0.009 [-0.089, 0.117] (n = 94; 76 ERR / 18 COR; testable False)
  - L25_V0_minus_local_disg: Δ = -0.216 [-0.524, 0.025] (n = 42; 35 ERR / 7 COR; testable False)
  - EXC_V0_minus_local_disg: Δ = -0.023 [-0.149, 0.071] (n = 52; 41 ERR / 11 COR; testable False)
  - DT_V0_minus_local_disg: Δ = 0.003 [-0.042, 0.052] (n = 179; 74 ERR / 105 COR; testable True)
- (c) R_COMP FREE (sibling): "NOT_TESTABLE" (/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_13/results/confirm_verdict_rcomp.json)
- L25_alone: Δ = — —; testable False; MDE80 —
- EXC: None
- DT_sign: Δ = -0.083 [-0.266, 0.137] (n = 63)
- long_without_pilot: None
- R_A_long: None
- R_VEX_long: None

## AUROC — regime R_AB, cell LONG (L25+EXC)
# source: results/auroc_cells.json :: R_AB / LONG (L25+EXC)

n = 94 (76 ERROR / 18 CORRECT; 12 sentences); testable = False

| metric | n | strat AUROC | 95% CI | pooled |
|---|---|---|---|---|
| c_score_align | 94 | 0.603 | [0.463, 0.735] | 0.614 |
| p_peer_text | 94 | 0.704 | [0.577, 0.843] | 0.709 |
| S4_E2_plus_V0 | 94 | 0.623 | [0.479, 0.794] | 0.620 |
| S4_E2 | 94 | 0.687 | [0.513, 0.884] | 0.684 |
| c_exact | 94 | 0.573 | [0.393, 0.773] | 0.563 |
| g_align | 94 | 0.634 | [0.470, 0.774] | 0.645 |
| c_pn | 94 | 0.619 | [0.464, 0.744] | 0.613 |
| c_rw | 94 | 0.607 | [0.463, 0.736] | 0.615 |
| c_pn_rw | 94 | 0.626 | [0.470, 0.759] | 0.625 |
| c_two | 94 | 0.634 | [0.460, 0.795] | 0.626 |
| c_v5 | 92 | 0.628 | [0.488, 0.755] | 0.626 |
| judge_local_qwen8b_disg | 94 | 0.695 | [0.551, 0.837] | 0.692 |
| judge_local_qwen8b_orig | 94 | 0.714 | [0.551, 0.900] | 0.712 |
| l2_bow | 94 | 0.653 | [0.511, 0.785] | 0.655 |
| l3_z3 | 94 | 0.706 | [0.587, 0.792] | 0.704 |
| pilot_joint_conflict | 94 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_arity_incons | 94 | 0.505 | [0.500, 0.512] | 0.507 |
| pilot_shape_incons | 94 | 0.510 | [0.500, 0.525] | 0.513 |
| pilot_dangling | 94 | 0.564 | [0.471, 0.673] | 0.574 |
| pilot_rerun_jacc | 94 | 0.533 | [0.394, 0.745] | 0.527 |

| paired Δ (strat) | n | Δ | 95% CI | CI > 0 |
|---|---|---|---|---|
| c_score_align - judge_local_qwen8b_disg | 94 | -0.091 | [-0.219, 0.017] | False |
| c_score_align - judge_local_qwen8b_orig | 94 | -0.111 | [-0.302, 0.017] | False |
| p_peer_text - judge_local_qwen8b_disg | 94 | 0.009 | [-0.089, 0.117] | False |
| S4_E2_plus_V0 - S4_E2 | 94 | -0.064 | [-0.134, -0.002] | False |
| c_score_align - S4_E2 | 94 | -0.083 | [-0.281, 0.051] | False |
| c_score_align - c_exact | 94 | 0.031 | [-0.085, 0.173] | False |
| c_score_align - p_peer_text | 94 | -0.101 | [-0.211, -0.025] | False |
| c_pn - c_score_align | 94 | 0.015 | [-0.039, 0.087] | False |
| c_rw - c_score_align | 94 | 0.004 | [0.000, 0.013] | False |
| c_pn_rw - c_score_align | 94 | 0.023 | [-0.003, 0.092] | False |
| c_two - c_score_align | 94 | 0.031 | [-0.014, 0.121] | False |
| c_v5 - c_score_align | 92 | 0.022 | [-0.041, 0.103] | False |
| c_exact - c_score_align | 94 | -0.031 | [-0.173, 0.085] | False |

## AUROC — regime R_AB, cell L25
# source: results/auroc_cells.json :: R_AB / L25

n = 42 (35 ERROR / 7 CORRECT; 6 sentences); testable = False

| metric | n | strat AUROC | 95% CI | pooled |
|---|---|---|---|---|
| c_score_align | 42 | 0.443 | [0.375, 0.500] | 0.443 |
| p_peer_text | 42 | 0.673 | [0.471, 0.967] | 0.673 |
| S4_E2_plus_V0 | 42 | 0.573 | [0.228, 0.950] | 0.573 |
| S4_E2 | 42 | 0.618 | [0.256, 1.000] | 0.618 |
| c_exact | 42 | 0.471 | [0.393, 0.500] | 0.471 |
| g_align | 42 | 0.584 | [0.500, 0.661] | 0.584 |
| c_pn | 42 | 0.443 | [0.375, 0.500] | 0.443 |
| c_rw | 42 | 0.443 | [0.375, 0.500] | 0.443 |
| c_pn_rw | 42 | 0.443 | [0.375, 0.500] | 0.443 |
| c_two | 42 | 0.443 | [0.375, 0.500] | 0.443 |
| c_v5 | 40 | 0.500 | [0.500, 0.500] | 0.500 |
| judge_local_qwen8b_disg | 42 | 0.659 | [0.450, 0.967] | 0.659 |
| judge_local_qwen8b_orig | 42 | 0.639 | [0.320, 0.967] | 0.639 |
| l2_bow | 42 | 0.702 | [0.521, 0.958] | 0.702 |
| l3_z3 | 42 | 0.657 | [0.455, 0.910] | 0.657 |
| pilot_joint_conflict | 42 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_arity_incons | 42 | 0.514 | [0.500, 0.535] | 0.514 |
| pilot_shape_incons | 42 | 0.529 | [0.500, 0.569] | 0.529 |
| pilot_dangling | 42 | 0.749 | [0.555, 0.874] | 0.749 |
| pilot_rerun_jacc | 42 | 0.312 | [0.161, 0.527] | 0.312 |

| paired Δ (strat) | n | Δ | 95% CI | CI > 0 |
|---|---|---|---|---|
| c_score_align - judge_local_qwen8b_disg | 42 | -0.216 | [-0.524, 0.025] | False |
| c_score_align - judge_local_qwen8b_orig | 42 | -0.196 | [-0.554, 0.154] | False |
| p_peer_text - judge_local_qwen8b_disg | 42 | 0.014 | [-0.167, 0.184] | False |
| S4_E2_plus_V0 - S4_E2 | 42 | -0.045 | [-0.150, 0.000] | False |
| c_score_align - S4_E2 | 42 | -0.176 | [-0.567, 0.212] | False |
| c_score_align - c_exact | 42 | -0.029 | [-0.081, 0.000] | False |
| c_score_align - p_peer_text | 42 | -0.231 | [-0.500, -0.064] | False |
| c_pn - c_score_align | 42 | 0.000 | [0.000, 0.000] | False |
| c_rw - c_score_align | 42 | 0.000 | [0.000, 0.000] | False |
| c_pn_rw - c_score_align | 42 | 0.000 | [0.000, 0.000] | False |
| c_two - c_score_align | 42 | 0.000 | [0.000, 0.000] | False |
| c_v5 - c_score_align | 40 | 0.061 | [0.000, 0.133] | False |
| c_exact - c_score_align | 42 | 0.029 | [0.000, 0.081] | False |

## AUROC — regime R_AB, cell EXC
# source: results/auroc_cells.json :: R_AB / EXC

n = 52 (41 ERROR / 11 CORRECT; 6 sentences); testable = False

| metric | n | strat AUROC | 95% CI | pooled |
|---|---|---|---|---|
| c_score_align | 52 | 0.691 | [0.490, 0.831] | 0.691 |
| p_peer_text | 52 | 0.721 | [0.557, 0.889] | 0.721 |
| S4_E2_plus_V0 | 52 | 0.650 | [0.510, 0.808] | 0.650 |
| S4_E2 | 52 | 0.724 | [0.534, 0.909] | 0.724 |
| c_exact | 52 | 0.627 | [0.356, 0.889] | 0.627 |
| g_align | 52 | 0.662 | [0.409, 0.854] | 0.662 |
| c_pn | 52 | 0.714 | [0.492, 0.833] | 0.714 |
| c_rw | 52 | 0.696 | [0.490, 0.833] | 0.696 |
| c_pn_rw | 52 | 0.726 | [0.503, 0.856] | 0.726 |
| c_two | 52 | 0.738 | [0.490, 0.905] | 0.738 |
| c_v5 | 52 | 0.693 | [0.480, 0.843] | 0.693 |
| judge_local_qwen8b_disg | 52 | 0.714 | [0.515, 0.861] | 0.714 |
| judge_local_qwen8b_orig | 52 | 0.755 | [0.595, 0.935] | 0.755 |
| l2_bow | 52 | 0.626 | [0.392, 0.774] | 0.626 |
| l3_z3 | 52 | 0.733 | [0.625, 0.800] | 0.733 |
| pilot_joint_conflict | 52 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_arity_incons | 52 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_shape_incons | 52 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_dangling | 52 | 0.463 | [0.438, 0.489] | 0.463 |
| pilot_rerun_jacc | 52 | 0.653 | [0.432, 0.906] | 0.653 |

| paired Δ (strat) | n | Δ | 95% CI | CI > 0 |
|---|---|---|---|---|
| c_score_align - judge_local_qwen8b_disg | 52 | -0.023 | [-0.149, 0.071] | False |
| c_score_align - judge_local_qwen8b_orig | 52 | -0.064 | [-0.221, 0.018] | False |
| p_peer_text - judge_local_qwen8b_disg | 52 | 0.007 | [-0.097, 0.131] | False |
| S4_E2_plus_V0 - S4_E2 | 52 | -0.074 | [-0.168, 0.025] | False |
| c_score_align - S4_E2 | 52 | -0.033 | [-0.221, 0.088] | False |
| c_score_align - c_exact | 52 | 0.063 | [-0.115, 0.265] | False |
| c_score_align - p_peer_text | 52 | -0.030 | [-0.161, 0.037] | False |
| c_pn - c_score_align | 52 | 0.023 | [-0.063, 0.122] | False |
| c_rw - c_score_align | 52 | 0.006 | [0.000, 0.017] | False |
| c_pn_rw - c_score_align | 52 | 0.035 | [-0.007, 0.126] | False |
| c_two - c_score_align | 52 | 0.048 | [-0.023, 0.168] | False |
| c_v5 - c_score_align | 52 | 0.002 | [-0.076, 0.115] | False |
| c_exact - c_score_align | 52 | -0.063 | [-0.265, 0.115] | False |

## AUROC — regime R_AB, cell DT
# source: results/auroc_cells.json :: R_AB / DT

n = 179 (74 ERROR / 105 CORRECT; 26 sentences); testable = True

| metric | n | strat AUROC | 95% CI | pooled |
|---|---|---|---|---|
| c_score_align | 179 | 0.916 | [0.858, 0.970] | 0.916 |
| p_peer_text | 179 | 0.919 | [0.860, 0.976] | 0.919 |
| S4_E2_plus_V0 | 179 | 0.949 | [0.899, 0.987] | 0.949 |
| S4_E2 | 179 | 0.953 | [0.911, 0.986] | 0.953 |
| c_exact | 179 | 0.854 | [0.763, 0.925] | 0.854 |
| g_align | 179 | 0.862 | [0.785, 0.928] | 0.862 |
| c_pn | 179 | 0.893 | [0.839, 0.949] | 0.893 |
| c_rw | 179 | 0.920 | [0.858, 0.975] | 0.920 |
| c_pn_rw | 179 | 0.918 | [0.859, 0.969] | 0.918 |
| c_two | 179 | 0.930 | [0.860, 0.984] | 0.930 |
| c_v5 | 179 | 0.918 | [0.870, 0.962] | 0.918 |
| judge_cheap_disg | 63 | 0.818 | [0.682, 0.935] | 0.818 |
| judge_local_qwen8b_disg | 179 | 0.913 | [0.858, 0.958] | 0.913 |
| judge_local_qwen8b_orig | 179 | 0.918 | [0.864, 0.960] | 0.918 |
| l2_bow | 179 | 0.760 | [0.687, 0.833] | 0.760 |
| l3_z3 | 179 | 0.572 | [0.480, 0.675] | 0.572 |
| pilot_joint_conflict | 179 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_arity_incons | 179 | 0.507 | [0.500, 0.521] | 0.507 |
| pilot_shape_incons | 179 | 0.510 | [0.484, 0.539] | 0.510 |
| pilot_dangling | 179 | 0.400 | [0.349, 0.446] | 0.400 |
| pilot_rerun_jacc | 179 | 0.729 | [0.636, 0.809] | 0.729 |

| paired Δ (strat) | n | Δ | 95% CI | CI > 0 |
|---|---|---|---|---|
| c_score_align - judge_cheap_disg | 63 | -0.083 | [-0.266, 0.137] | False |
| c_score_align - judge_local_qwen8b_disg | 179 | 0.003 | [-0.042, 0.052] | False |
| c_score_align - judge_local_qwen8b_orig | 179 | -0.001 | [-0.053, 0.054] | False |
| p_peer_text - judge_cheap_disg | 63 | -0.055 | [-0.258, 0.171] | False |
| p_peer_text - judge_local_qwen8b_disg | 179 | 0.006 | [-0.041, 0.061] | False |
| S4_E2_plus_V0 - S4_E2 | 179 | -0.004 | [-0.032, 0.021] | False |
| S4_E2 - judge_cheap_disg | 63 | 0.085 | [-0.041, 0.219] | False |
| c_score_align - S4_E2 | 179 | -0.037 | [-0.082, 0.006] | False |
| c_score_align - c_exact | 179 | 0.062 | [-0.003, 0.131] | False |
| c_score_align - p_peer_text | 179 | -0.003 | [-0.022, 0.010] | False |
| c_pn - c_score_align | 179 | -0.023 | [-0.070, 0.022] | False |
| c_rw - c_score_align | 179 | 0.004 | [-0.006, 0.014] | False |
| c_pn_rw - c_score_align | 179 | 0.002 | [-0.032, 0.033] | False |
| c_two - c_score_align | 179 | 0.014 | [-0.028, 0.062] | False |
| c_v5 - c_score_align | 179 | 0.002 | [-0.023, 0.031] | False |
| c_exact - c_score_align | 179 | -0.062 | [-0.131, 0.003] | False |

## AUROC — regime R_AB, cell ALL
# source: results/auroc_cells.json :: R_AB / ALL

n = 273 (150 ERROR / 123 CORRECT; 38 sentences); testable = True

| metric | n | strat AUROC | 95% CI | pooled |
|---|---|---|---|---|
| c_score_align | 273 | 0.890 | [0.838, 0.940] | 0.889 |
| p_peer_text | 273 | 0.902 | [0.847, 0.956] | 0.900 |
| S4_E2_plus_V0 | 273 | 0.922 | [0.873, 0.964] | 0.909 |
| S4_E2 | 273 | 0.931 | [0.888, 0.967] | 0.912 |
| c_exact | 273 | 0.831 | [0.749, 0.900] | 0.820 |
| g_align | 273 | 0.844 | [0.771, 0.905] | 0.819 |
| c_pn | 273 | 0.871 | [0.818, 0.921] | 0.848 |
| c_rw | 273 | 0.894 | [0.840, 0.944] | 0.893 |
| c_pn_rw | 273 | 0.894 | [0.839, 0.942] | 0.884 |
| c_two | 273 | 0.906 | [0.842, 0.956] | 0.897 |
| c_v5 | 271 | 0.895 | [0.852, 0.937] | 0.872 |
| judge_cheap_disg | 71 | 0.814 | [0.680, 0.930] | 0.799 |
| judge_local_qwen8b_disg | 273 | 0.895 | [0.844, 0.938] | 0.875 |
| judge_local_qwen8b_orig | 273 | 0.901 | [0.850, 0.945] | 0.883 |
| l2_bow | 273 | 0.751 | [0.681, 0.818] | 0.770 |
| l3_z3 | 273 | 0.583 | [0.495, 0.676] | 0.574 |
| pilot_joint_conflict | 273 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_arity_incons | 273 | 0.507 | [0.500, 0.520] | 0.507 |
| pilot_shape_incons | 273 | 0.510 | [0.486, 0.536] | 0.503 |
| pilot_dangling | 273 | 0.413 | [0.365, 0.459] | 0.445 |
| pilot_rerun_jacc | 273 | 0.713 | [0.627, 0.789] | 0.704 |

| paired Δ (strat) | n | Δ | 95% CI | CI > 0 |
|---|---|---|---|---|
| c_score_align - judge_cheap_disg | 71 | -0.082 | [-0.262, 0.136] | False |
| c_score_align - judge_local_qwen8b_disg | 273 | -0.005 | [-0.047, 0.041] | False |
| c_score_align - judge_local_qwen8b_orig | 273 | -0.010 | [-0.058, 0.039] | False |
| p_peer_text - judge_cheap_disg | 71 | -0.051 | [-0.251, 0.174] | False |
| p_peer_text - judge_local_qwen8b_disg | 273 | 0.007 | [-0.037, 0.057] | False |
| S4_E2_plus_V0 - S4_E2 | 273 | -0.009 | [-0.034, 0.014] | False |
| S4_E2 - judge_cheap_disg | 71 | 0.085 | [-0.039, 0.217] | False |
| c_score_align - S4_E2 | 273 | -0.040 | [-0.085, 0.001] | False |
| c_score_align - c_exact | 273 | 0.060 | [-0.003, 0.124] | False |
| c_score_align - p_peer_text | 273 | -0.011 | [-0.031, 0.003] | False |
| c_pn - c_score_align | 273 | -0.020 | [-0.063, 0.022] | False |
| c_rw - c_score_align | 273 | 0.004 | [-0.005, 0.014] | False |
| c_pn_rw - c_score_align | 273 | 0.003 | [-0.027, 0.033] | False |
| c_two - c_score_align | 273 | 0.015 | [-0.023, 0.059] | False |
| c_v5 - c_score_align | 271 | 0.004 | [-0.020, 0.031] | False |
| c_exact - c_score_align | 273 | -0.060 | [-0.124, 0.003] | False |

## AUROC — regime R_A, cell LONG (L25+EXC)
# source: results/auroc_cells.json :: R_A / LONG (L25+EXC)

n = 17 (11 ERROR / 6 CORRECT; 4 sentences); testable = False

| metric | n | strat AUROC | 95% CI | pooled |
|---|---|---|---|---|
| c_score_align | 17 | 0.463 | [0.458, 1.000] | 0.447 |
| p_peer_text | 17 | 0.550 | [0.500, 1.000] | 0.576 |
| S4_E2_plus_V0 | 17 | 0.600 | [0.556, 1.000] | 0.515 |
| S4_E2 | 17 | 1.000 | [1.000, 1.000] | 0.848 |
| c_exact | 17 | 0.950 | [0.500, 1.000] | 0.788 |
| g_align | 17 | 0.575 | [0.556, 1.000] | 0.561 |
| c_pn | 17 | 0.700 | [0.500, 1.000] | 0.591 |
| c_rw | 17 | 0.475 | [0.472, 1.000] | 0.455 |
| c_pn_rw | 17 | 0.700 | [0.500, 1.000] | 0.591 |
| c_two | 17 | 0.950 | [0.500, 1.000] | 0.742 |
| c_v5 | 17 | 0.700 | [0.500, 1.000] | 0.606 |
| judge_local_qwen8b_disg | 17 | 0.900 | [0.500, 0.944] | 0.818 |
| judge_local_qwen8b_orig | 17 | 0.850 | [0.833, 1.000] | 0.758 |
| l2_bow | 17 | 0.675 | [0.667, 0.750] | 0.682 |
| l3_z3 | 17 | 0.613 | [0.611, 0.833] | 0.576 |
| pilot_joint_conflict | 17 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_arity_incons | 17 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_shape_incons | 17 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_dangling | 17 | 0.500 | [0.500, 0.750] | 0.538 |
| pilot_rerun_jacc | 17 | 0.588 | [0.556, 1.000] | 0.492 |

| paired Δ (strat) | n | Δ | 95% CI | CI > 0 |
|---|---|---|---|---|
| c_score_align - judge_local_qwen8b_disg | 17 | -0.438 | [-0.486, 0.167] | False |
| c_score_align - judge_local_qwen8b_orig | 17 | -0.387 | [-0.500, 0.000] | False |
| S4_E2_plus_V0 - S4_E2 | 17 | -0.400 | [-0.444, 0.000] | False |

## AUROC — regime R_A, cell L25
# source: results/auroc_cells.json :: R_A / L25

n = 4 (2 ERROR / 2 CORRECT; 2 sentences); testable = False

| metric | n | strat AUROC | 95% CI | pooled |
|---|---|---|---|---|

| paired Δ (strat) | n | Δ | 95% CI | CI > 0 |
|---|---|---|---|---|

## AUROC — regime R_A, cell EXC
# source: results/auroc_cells.json :: R_A / EXC

n = 13 (9 ERROR / 4 CORRECT; 2 sentences); testable = False

| metric | n | strat AUROC | 95% CI | pooled |
|---|---|---|---|---|
| c_score_align | 13 | 0.458 | [0.458, 1.000] | 0.458 |
| p_peer_text | 13 | 0.556 | [0.556, 1.000] | 0.556 |
| S4_E2_plus_V0 | 13 | 0.556 | [0.556, 1.000] | 0.556 |
| S4_E2 | 13 | 1.000 | [1.000, 1.000] | 1.000 |
| c_exact | 13 | 1.000 | [1.000, 1.000] | 1.000 |
| g_align | 13 | 0.556 | [0.556, 1.000] | 0.556 |
| c_pn | 13 | 0.722 | [0.722, 1.000] | 0.722 |
| c_rw | 13 | 0.472 | [0.472, 1.000] | 0.472 |
| c_pn_rw | 13 | 0.722 | [0.722, 1.000] | 0.722 |
| c_two | 13 | 1.000 | [1.000, 1.000] | 1.000 |
| c_v5 | 13 | 0.722 | [0.722, 1.000] | 0.722 |
| judge_local_qwen8b_disg | 13 | 0.944 | [0.833, 0.944] | 0.944 |
| judge_local_qwen8b_orig | 13 | 0.833 | [0.833, 1.000] | 0.833 |
| l2_bow | 13 | 0.667 | [0.667, 0.667] | 0.667 |
| l3_z3 | 13 | 0.611 | [0.611, 0.833] | 0.611 |
| pilot_joint_conflict | 13 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_arity_incons | 13 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_shape_incons | 13 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_dangling | 13 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_rerun_jacc | 13 | 0.556 | [0.556, 1.000] | 0.556 |

| paired Δ (strat) | n | Δ | 95% CI | CI > 0 |
|---|---|---|---|---|
| c_score_align - judge_local_qwen8b_disg | 13 | -0.486 | [-0.486, 0.167] | False |
| c_score_align - judge_local_qwen8b_orig | 13 | -0.375 | [-0.375, 0.000] | False |
| S4_E2_plus_V0 - S4_E2 | 13 | -0.444 | [-0.444, 0.000] | False |

## AUROC — regime R_A, cell DT
# source: results/auroc_cells.json :: R_A / DT

n = 15 (15 ERROR / 0 CORRECT; 11 sentences); testable = False

## AUROC — regime R_VEX, cell LONG (L25+EXC)
# source: results/auroc_cells.json :: R_VEX / LONG (L25+EXC)

n = 10 (4 ERROR / 6 CORRECT; 5 sentences); testable = False

| metric | n | strat AUROC | 95% CI | pooled |
|---|---|---|---|---|
| c_score_align | 10 | 0.700 | [0.500, 1.000] | 0.833 |
| p_peer_text | 10 | 0.800 | [0.500, 1.000] | 0.833 |
| S4_E2_plus_V0 | 10 | 1.000 | [1.000, 1.000] | 1.000 |
| S4_E2 | 10 | 1.000 | [1.000, 1.000] | 1.000 |
| c_exact | 10 | 0.700 | [0.500, 1.000] | 0.833 |
| g_align | 10 | 0.850 | [0.500, 1.000] | 0.917 |
| c_pn | 10 | 0.700 | [0.500, 1.000] | 0.833 |
| c_rw | 10 | 0.700 | [0.500, 1.000] | 0.833 |
| c_pn_rw | 10 | 0.700 | [0.500, 1.000] | 0.833 |
| c_two | 10 | 0.700 | [0.500, 1.000] | 0.833 |
| c_v5 | 10 | 0.700 | [0.500, 1.000] | 0.833 |
| judge_local_qwen8b_disg | 10 | 0.800 | [0.500, 1.000] | 0.917 |
| judge_local_qwen8b_orig | 10 | 1.000 | [1.000, 1.000] | 1.000 |
| l2_bow | 10 | 0.700 | [0.500, 1.000] | 0.750 |
| l3_z3 | 10 | 0.650 | [0.500, 1.000] | 0.708 |
| pilot_joint_conflict | 10 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_arity_incons | 10 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_shape_incons | 10 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_dangling | 10 | 0.550 | [0.417, 0.875] | 0.458 |
| pilot_rerun_jacc | 10 | 0.750 | [0.000, 1.000] | 0.854 |

| paired Δ (strat) | n | Δ | 95% CI | CI > 0 |
|---|---|---|---|---|
| c_score_align - judge_local_qwen8b_disg | 10 | -0.100 | [-0.500, 0.000] | False |
| c_score_align - judge_local_qwen8b_orig | 10 | -0.300 | [-0.500, 0.000] | False |
| S4_E2_plus_V0 - S4_E2 | 10 | 0.000 | [0.000, 0.000] | False |

## AUROC — regime R_VEX, cell L25
# source: results/auroc_cells.json :: R_VEX / L25

n = 5 (3 ERROR / 2 CORRECT; 3 sentences); testable = False

| metric | n | strat AUROC | 95% CI | pooled |
|---|---|---|---|---|

| paired Δ (strat) | n | Δ | 95% CI | CI > 0 |
|---|---|---|---|---|

## AUROC — regime R_VEX, cell EXC
# source: results/auroc_cells.json :: R_VEX / EXC

n = 5 (1 ERROR / 4 CORRECT; 2 sentences); testable = False

| metric | n | strat AUROC | 95% CI | pooled |
|---|---|---|---|---|

| paired Δ (strat) | n | Δ | 95% CI | CI > 0 |
|---|---|---|---|---|

## AUROC — regime R_VEX, cell DT
# source: results/auroc_cells.json :: R_VEX / DT

n = 38 (7 ERROR / 31 CORRECT; 10 sentences); testable = False

| metric | n | strat AUROC | 95% CI | pooled |
|---|---|---|---|---|
| c_score_align | 38 | 0.924 | [0.741, 1.000] | 0.924 |
| p_peer_text | 38 | 0.924 | [0.738, 1.000] | 0.924 |
| S4_E2_plus_V0 | 38 | 1.000 | [1.000, 1.000] | 1.000 |
| S4_E2 | 38 | 0.991 | [0.969, 1.000] | 0.991 |
| c_exact | 38 | 0.922 | [0.757, 1.000] | 0.922 |
| g_align | 38 | 0.929 | [0.750, 1.000] | 0.929 |
| c_pn | 38 | 0.929 | [0.833, 1.000] | 0.929 |
| c_rw | 38 | 0.935 | [0.745, 1.000] | 0.935 |
| c_pn_rw | 38 | 0.926 | [0.826, 1.000] | 0.926 |
| c_two | 38 | 0.940 | [0.760, 1.000] | 0.940 |
| c_v5 | 38 | 0.929 | [0.833, 1.000] | 0.929 |
| judge_cheap_disg | 21 | 1.000 | [1.000, 1.000] | 1.000 |
| judge_local_qwen8b_disg | 38 | 0.995 | [0.972, 1.000] | 0.995 |
| judge_local_qwen8b_orig | 38 | 0.986 | [0.966, 1.000] | 0.986 |
| l2_bow | 38 | 0.714 | [0.562, 0.889] | 0.714 |
| l3_z3 | 38 | 0.493 | [0.402, 0.556] | 0.493 |
| pilot_joint_conflict | 38 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_arity_incons | 38 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_shape_incons | 38 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_dangling | 38 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_rerun_jacc | 38 | 0.558 | [0.243, 0.750] | 0.558 |

| paired Δ (strat) | n | Δ | 95% CI | CI > 0 |
|---|---|---|---|---|
| c_score_align - judge_cheap_disg | 21 | -0.575 | [-0.938, -0.132] | False |
| c_score_align - judge_local_qwen8b_disg | 38 | -0.071 | [-0.259, 0.026] | False |
| c_score_align - judge_local_qwen8b_orig | 38 | -0.062 | [-0.257, 0.029] | False |
| S4_E2_plus_V0 - S4_E2 | 38 | 0.009 | [0.000, 0.031] | False |

## AUROC — regime R_AB_nopilot, cell LONG (L25+EXC)
# source: results/auroc_cells.json :: R_AB_nopilot / LONG (L25+EXC)

n = 74 (58 ERROR / 16 CORRECT; 10 sentences); testable = False

| metric | n | strat AUROC | 95% CI | pooled |
|---|---|---|---|---|
| c_score_align | 74 | 0.615 | [0.381, 0.756] | 0.598 |
| p_peer_text | 74 | 0.710 | [0.526, 0.863] | 0.693 |
| S4_E2_plus_V0 | 74 | 0.658 | [0.483, 0.831] | 0.633 |
| S4_E2 | 74 | 0.706 | [0.533, 0.900] | 0.691 |
| c_exact | 74 | 0.604 | [0.412, 0.806] | 0.583 |
| g_align | 74 | 0.636 | [0.428, 0.790] | 0.629 |
| c_pn | 74 | 0.610 | [0.381, 0.758] | 0.587 |
| c_rw | 74 | 0.617 | [0.381, 0.757] | 0.597 |
| c_pn_rw | 74 | 0.622 | [0.381, 0.776] | 0.601 |
| c_two | 74 | 0.624 | [0.381, 0.809] | 0.602 |
| c_v5 | 72 | 0.631 | [0.453, 0.776] | 0.612 |
| judge_local_qwen8b_disg | 74 | 0.696 | [0.536, 0.842] | 0.688 |
| judge_local_qwen8b_orig | 74 | 0.746 | [0.564, 0.932] | 0.727 |
| l2_bow | 74 | 0.662 | [0.526, 0.795] | 0.656 |
| l3_z3 | 74 | 0.702 | [0.551, 0.790] | 0.690 |
| pilot_joint_conflict | 74 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_arity_incons | 74 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_shape_incons | 74 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_dangling | 74 | 0.566 | [0.468, 0.703] | 0.593 |
| pilot_rerun_jacc | 74 | 0.572 | [0.390, 0.795] | 0.537 |

| paired Δ (strat) | n | Δ | 95% CI | CI > 0 |
|---|---|---|---|---|
| c_score_align - judge_local_qwen8b_disg | 74 | -0.081 | [-0.244, 0.012] | False |
| c_score_align - judge_local_qwen8b_orig | 74 | -0.130 | [-0.403, -0.009] | False |
| S4_E2_plus_V0 - S4_E2 | 74 | -0.048 | [-0.123, -0.008] | False |

## AUROC — regime R_AB_nopilot, cell L25
# source: results/auroc_cells.json :: R_AB_nopilot / L25

n = 32 (25 ERROR / 7 CORRECT; 5 sentences); testable = False

| metric | n | strat AUROC | 95% CI | pooled |
|---|---|---|---|---|
| c_score_align | 32 | 0.420 | [0.340, 0.500] | 0.420 |
| p_peer_text | 32 | 0.594 | [0.433, 0.900] | 0.594 |
| S4_E2_plus_V0 | 32 | 0.603 | [0.364, 1.000] | 0.603 |
| S4_E2 | 32 | 0.620 | [0.379, 1.000] | 0.620 |
| c_exact | 32 | 0.460 | [0.364, 0.500] | 0.460 |
| g_align | 32 | 0.571 | [0.469, 0.675] | 0.571 |
| c_pn | 32 | 0.420 | [0.340, 0.500] | 0.420 |
| c_rw | 32 | 0.420 | [0.340, 0.500] | 0.420 |
| c_pn_rw | 32 | 0.420 | [0.340, 0.500] | 0.420 |
| c_two | 32 | 0.420 | [0.340, 0.500] | 0.420 |
| c_v5 | 30 | 0.500 | [0.500, 0.500] | 0.500 |
| judge_local_qwen8b_disg | 32 | 0.643 | [0.503, 0.900] | 0.643 |
| judge_local_qwen8b_orig | 32 | 0.649 | [0.379, 1.000] | 0.649 |
| l2_bow | 32 | 0.646 | [0.480, 0.925] | 0.646 |
| l3_z3 | 32 | 0.566 | [0.399, 0.838] | 0.566 |
| pilot_joint_conflict | 32 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_arity_incons | 32 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_shape_incons | 32 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_dangling | 32 | 0.754 | [0.562, 0.891] | 0.754 |
| pilot_rerun_jacc | 32 | 0.380 | [0.190, 0.594] | 0.380 |

| paired Δ (strat) | n | Δ | 95% CI | CI > 0 |
|---|---|---|---|---|
| c_score_align - judge_local_qwen8b_disg | 32 | -0.223 | [-0.521, -0.057] | False |
| c_score_align - judge_local_qwen8b_orig | 32 | -0.229 | [-0.604, 0.076] | False |
| S4_E2_plus_V0 - S4_E2 | 32 | -0.017 | [-0.107, 0.000] | False |

## AUROC — regime R_AB_nopilot, cell EXC
# source: results/auroc_cells.json :: R_AB_nopilot / EXC

n = 42 (33 ERROR / 9 CORRECT; 5 sentences); testable = False

| metric | n | strat AUROC | 95% CI | pooled |
|---|---|---|---|---|
| c_score_align | 42 | 0.731 | [0.357, 0.869] | 0.731 |
| p_peer_text | 42 | 0.778 | [0.495, 0.939] | 0.778 |
| S4_E2_plus_V0 | 42 | 0.690 | [0.493, 0.866] | 0.690 |
| S4_E2 | 42 | 0.756 | [0.509, 0.946] | 0.756 |
| c_exact | 42 | 0.689 | [0.386, 0.937] | 0.689 |
| g_align | 42 | 0.673 | [0.346, 0.871] | 0.673 |
| c_pn | 42 | 0.722 | [0.357, 0.859] | 0.722 |
| c_rw | 42 | 0.732 | [0.357, 0.869] | 0.732 |
| c_pn_rw | 42 | 0.741 | [0.357, 0.879] | 0.741 |
| c_two | 42 | 0.744 | [0.357, 0.931] | 0.744 |
| c_v5 | 42 | 0.702 | [0.400, 0.878] | 0.702 |
| judge_local_qwen8b_disg | 42 | 0.727 | [0.429, 0.895] | 0.727 |
| judge_local_qwen8b_orig | 42 | 0.803 | [0.654, 0.982] | 0.803 |
| l2_bow | 42 | 0.672 | [0.443, 0.822] | 0.672 |
| l3_z3 | 42 | 0.783 | [0.629, 0.809] | 0.783 |
| pilot_joint_conflict | 42 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_arity_incons | 42 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_shape_incons | 42 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_dangling | 42 | 0.455 | [0.429, 0.485] | 0.455 |
| pilot_rerun_jacc | 42 | 0.685 | [0.393, 0.975] | 0.685 |

| paired Δ (strat) | n | Δ | 95% CI | CI > 0 |
|---|---|---|---|---|
| c_score_align - judge_local_qwen8b_disg | 42 | 0.003 | [-0.214, 0.090] | False |
| c_score_align - judge_local_qwen8b_orig | 42 | -0.072 | [-0.414, 0.014] | False |
| S4_E2_plus_V0 - S4_E2 | 42 | -0.066 | [-0.200, 0.000] | False |

## AUROC — regime R_AB_nopilot, cell DT
# source: results/auroc_cells.json :: R_AB_nopilot / DT

n = 135 (56 ERROR / 79 CORRECT; 20 sentences); testable = False

| metric | n | strat AUROC | 95% CI | pooled |
|---|---|---|---|---|
| c_score_align | 135 | 0.910 | [0.842, 0.970] | 0.910 |
| p_peer_text | 135 | 0.914 | [0.847, 0.980] | 0.914 |
| S4_E2_plus_V0 | 135 | 0.949 | [0.890, 0.989] | 0.949 |
| S4_E2 | 135 | 0.945 | [0.888, 0.987] | 0.945 |
| c_exact | 135 | 0.867 | [0.769, 0.942] | 0.867 |
| g_align | 135 | 0.856 | [0.767, 0.933] | 0.856 |
| c_pn | 135 | 0.884 | [0.818, 0.952] | 0.884 |
| c_rw | 135 | 0.915 | [0.844, 0.978] | 0.915 |
| c_pn_rw | 135 | 0.898 | [0.827, 0.966] | 0.898 |
| c_two | 135 | 0.929 | [0.854, 0.986] | 0.929 |
| c_v5 | 135 | 0.905 | [0.847, 0.961] | 0.905 |
| judge_cheap_disg | 53 | 0.789 | [0.640, 0.923] | 0.789 |
| judge_local_qwen8b_disg | 135 | 0.914 | [0.840, 0.969] | 0.914 |
| judge_local_qwen8b_orig | 135 | 0.915 | [0.845, 0.967] | 0.915 |
| l2_bow | 135 | 0.750 | [0.667, 0.839] | 0.750 |
| l3_z3 | 135 | 0.573 | [0.465, 0.688] | 0.573 |
| pilot_joint_conflict | 135 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_arity_incons | 135 | 0.500 | [0.500, 0.500] | 0.500 |
| pilot_shape_incons | 135 | 0.514 | [0.488, 0.542] | 0.514 |
| pilot_dangling | 135 | 0.403 | [0.344, 0.457] | 0.403 |
| pilot_rerun_jacc | 135 | 0.725 | [0.600, 0.825] | 0.725 |

| paired Δ (strat) | n | Δ | 95% CI | CI > 0 |
|---|---|---|---|---|
| c_score_align - judge_cheap_disg | 53 | -0.078 | [-0.301, 0.173] | False |
| c_score_align - judge_local_qwen8b_disg | 135 | -0.004 | [-0.053, 0.054] | False |
| c_score_align - judge_local_qwen8b_orig | 135 | -0.005 | [-0.064, 0.063] | False |
| S4_E2_plus_V0 - S4_E2 | 135 | 0.005 | [-0.024, 0.037] | False |

## H-MECH
# source: results/hmech_E2.json

- i_all_families: {"share_nonagreeing_peers_labelled_ERROR": 0.9090909090909091, "ci": [0.8423645320197044, 0.9767475467132678], "n_peer_judgements": 352, "n_sentences": 32, "verdict": "CONFIRMED"}
- i_pool3_deepseek_microsoft_openai: {"share_nonagreeing_peers_labelled_ERROR": 0.9181818181818182, "ci": [0.8416530373831775, 0.9811320754716981], "n_peer_judgements": 110, "n_sentences": 25, "verdict": "CONFIRMED"}
- ii_scatter: {"SI_err": 0.1132716049382716, "SI_cor": 0.8287698412698412, "ratio": 7.316660179057999, "ci": [4.002864505955566, 20.804995465288847], "n_sentences": 24, "verdict": "NOT_READ"}
- iii_net: {"delta_e_plus_d_T3_minus_T1": 0.3471721137521222, "ci": [-0.035838403865423654, 0.8549673143088443], "e_T1": 0.12903225806451613, "d_T1": 0.078125, "e_T3": 0.08064516129032258, "d_T3": 0.47368421052631576, "tercile_cuts_words": [17.0, 19.0], "n_T1": 126, "n_T3": 81, "verdict": "CONFIRMED"}
- iv_exact_vs_align: {"ALIGN_lower_d": true, "ALIGN_higher_e_on_rename_and_adddrop": true, "verdict": "CONFIRMED"}
  - CORRECT: {"n": 123, "stat": "d", "exact": 0.7398373983739838, "ALIGN": 0.17886178861788618, "ALIGN_minus_exact": -0.5609756097560976, "ci": [-0.7317479674796747, -0.38594693701466787]}
  - MEANING_RENAME_type (tier-B VOCAB_GRAN->ERROR): {"n": 8, "stat": "e", "exact": 0.125, "ALIGN": 0.625, "ALIGN_minus_exact": 0.5, "ci": [0.125, 0.875]}
  - ADD/DROP: {"n": 118, "stat": "e", "exact": 0.0, "ALIGN": 0.09322033898305085, "ALIGN_minus_exact": 0.09322033898305085, "ci": [0.0, 0.19445058997050144]}
  - OTHER_ERROR: {"n": 24, "stat": "e", "exact": 0.0, "ALIGN": 0.0, "ALIGN_minus_exact": 0.0, "ci": [0.0, 0.0]}

## H-IMPROVE
# source: results/improve_E2.json

```
{
 "carried_variant": "NONE: V0 stands",
 "rule": "winner = variant with highest E LONG-strat AUROC (Z) that (i) beats V0 by >= +0.015 there AND (ii) >= V0 on L25 (point) AND (iii) >= V0 - 0.01 on CTRL; none -> 'NONE: V0 stands'; tie (|\u0394| < 1e-4) -> cheaper (V5 < others)",
 "verdict": "V0 STANDS (no variant carried by the freeze; V1-V5 below are DEVELOPMENT-ONLY/exploratory rows)",
 "exploratory_long_pool_deltas_vs_V0": {
  "c_pn": {
   "n": 94,
   "n_error": 76,
   "n_correct": 18,
   "testable": false,
   "delta": 0.015086206896551713,
   "ci": [
    -0.038523274478330705,
    0.08721139020943085
   ],
   "p_le0": 0.2925,
   "ci_gt0": false,
   "pooled_delta": -0.0003654970760234022,
   "ci_pooled_cluster_boot": [
    -0.03266963205427367,
    0.08379403369534935
   ]
  },
  "c_rw": {
   "n": 94,
   "n_error": 76,
   "n_correct": 18,
   "testable": false,
   "delta": 0.0035919540229885083,
   "ci": [
    0.0,
    0.012967430285659363
   ],
   "p_le0": 0.158,
   "ci_gt0": false,
   "pooled_delta": 0.0010964912280702066,
   "ci_pooled_cluster_boot": [
    0.0,
    0.012430939226519389
   ]
  },
  "c_pn_rw": {
   "n": 94,
   "n_error": 76,
   "n_correct": 18,
   "testable": false,
   "delta": 0.02298850574712641,
   "ci": [
    -0.0034662045060658286,
    0.0923077702155241
   ],
   "p_le0": 0.066,
   "ci_gt0": false,
   "pooled_delta": 0.011695906432748537,
   "ci_pooled_cluster_boot": [
    -0.0007151823281116853,
    0.08855951554100297
   ]
  },
  "c_two": {
   "n": 94,
   "n_error": 76,
   "n_correct": 18,
   "testable": false,
   "delta": 0.030890804597701216,
   "ci": [
    -0.013821969880393177,
    0.12114621064363348
   ],
   "p_le0": 0.328,
   "ci_gt0": false,
   "pooled_delta": 0.012792397660818744,
   "ci_pooled_cluster_boot": [
    -0.01403508771929829,
    0.12052769709662639
   ]
  },
  "c_v5": {
   "n": 92,
   "n_error": 74,
   "n_correct": 18,
   "testable": false,
   "delta": 0.021994134897360684,
   "ci": [
    -0.04081841325487249,
    0.10322721516465122
   ],
   "p_le0": 0.2295,
   "ci_gt0": false,
   "pooled_delta": 0.01501501501501501,
   "ci_pooled_cluster_boot": [
    -0.046363296478326384,
    0.10282146315402849
   ]
  },
  "c_exact": {
   "n": 94,
   "n_error": 76,
   "n_correct": 18,
   "testable": false,
   "delta": -0.030890804597701105,
   "ci": [
    -0.17295166560816214,
    0.0854704301075269
   ],
   "p_le0": 0.675,
   "ci_gt0": false,
   "pooled_delta": -0.05080409356725146,
   "ci_pooled_cluster_boot": [
    -0.19857907645958373,
    0.08358155976581756
   ]
  }
 },
 "holm_over_5": {
  "c_pn_rw": 0.33,
  "c_rw": 0.632,
  "c_v5": 0.6885,
  "c_pn": 0.585,
  "c_two": 0.328,
  "c_exact": 0.0
 }
}
```

## H-RENAME
# source: results/rename_E2.json

```
{
 "GG_dev_gate": "FAIL(g3)",
 "verdict": "NOT CONFIRMED (GG failed its pre-registered development gate g3; c_gg not computed on E2)",
 "V0_rename_controls": {
  "n_controls": 181,
  "RENAME_SYN": {
   "n": 36,
   "FA_control": 0.9444444444444444,
   "FA_parent_base": 0.3611111111111111,
   "paired_flip": 0.5833333333333334,
   "mean_v0_shift": 0.46423059964726626,
   "by_stratum": {
    "L25": {
     "n": 13,
     "paired_flip": 0.0
    },
    "EXC": {
     "n": 1,
     "paired_flip": 0.0
    },
    "DT": {
     "n": 22,
     "paired_flip": 0.9545454545454546
    }
   }
  },
  "RENAME_NONCE": {
   "n": 145,
   "FA_control": 1.0,
   "FA_parent_base": 0.2620689655172414,
   "paired_flip": 0.7379310344827587,
   "mean_v0_shift": 0.5501149425287356,
   "by_stratum": {
    "L25": {
     "n": 22,
     "paired_flip": 0.18181818181818182
    },
    "EXC": {
     "n": 18,
     "paired_flip": 0.2777777777777778
    },
    "DT": {
     "n": 105,
     "paired_flip": 0.9333333333333333
    }
   }
  }
 }
}
```

## Complexity
# source: results/complexity_E2.json

```
{
 "words": {
  "-1-17": {
   "n": 126,
   "auroc": {
    "c_score_align": 0.8954359673024523,
    "judge_cheap_disg": 0.7682481751824818,
    "p_peer_text": 0.8979904632152589
   },
   "delta_V0_minus_bar": {
    "n": 45,
    "n_error": 10,
    "n_correct": 35,
    "testable": false,
    "delta": -0.17153284671532854,
    "ci": [
     -0.4268315018315018,
     0.1773115299334811
    ],
    "p_le0": 0.836,
    "ci_gt0": false,
    "pooled_delta": -0.12857142857142856,
    "ci_pooled_cluster_boot": [
     -0.4208018338779691,
     0.1954125648827633
    ]
   },
   "binary_e_d_thr0.5": {
    "c_score_align": {
     "e": 0.12903225806451613,
     "d": 0.078125
    },
    "judge_cheap_disg": {
     "e": 0.6,
     "d": 0.02857142857142857
    },
    "p_peer_text": {
     "e": 0.12903225806451613,
     "d": 0.0625
    }
   }
  },
  "17-19": {
   "n": 66,
   "auroc": {
    "c_score_align": 0.9201030927835051,
    "judge_cheap_disg": 0.9,
    "p_peer_text": 0.9381443298969072
   },
   "delta_V0_minus_bar": {
    "n": 15,
    "n_error": 5,
    "n_correct": 10,
    "testable": false,
    "delta": -0.06000000000000005,
    "ci": [
     -0.4285714285714286,
     0.2669940476190475
    ],
    "p_le0": 0.677,
    "ci_gt0": false,
    "pooled_delta": -0.06000000000000005,
    "ci_pooled_cluster_boot": [
     -0.4,
     0.2857142857142857
    ]
   },
   "binary_e_d_thr0.5": {
    "c_score_align": {
     "e": 0.11538461538461539,
     "d": 0.2
    },
    "judge_cheap_disg": {
     "e": 1.0,
     "d": 0.0
    },
    "p_peer_text": {
     "e": 0.11538461538461539,
     "d": 0.025
    }
   }
  },
  "19-1e+09": {
   "n": 81,
   "auroc": {
    "c_score_align": 0.5491573033707865,
    "judge_cheap_disg": 0.5,
    "p_peer_text": 0.7162921348314607
   },
   "delta_V0_minus_bar": {
    "n": 11,
    "n_error": 3,
    "n_correct": 8,
    "testable": false,
    "delta": -0.16666666666666669,
    "ci": [
     -0.5,
     0.5
    ],
    "p_le0": 0.603,
    "ci_gt0": false,
    "pooled_delta": 0.08333333333333337,
    "ci_pooled_cluster_boot": [
     -0.5,
     0.5
    ]
   },
   "binary_e_d_thr0.5": {
    "c_score_align": {
     "e": 0.08064516129032258,
     "d": 0.47368421052631576
    },
    "judge_cheap_disg": {
     "e": 0.6666666666666666,
     "d": 0.0
    },
    "p_peer_text": {
     "e": 0.08064516129032258,
     "d": 0.42105263157894735
    }
   }
  }
 },
 "n_conditions": {
  "0-1": {
   "n": 0,
   "auroc": {},
   "delta_V0_minus_bar": null,
   "binary_e_d_thr0.5": {
    "c_score_align": {
     "e": null,
     "d": null
    },
    "judge_cheap_disg": {
     "e": null,
     "d": null
    },
    "p_peer_text": {
     "e": null,
     "d": null
    }
   }
  },
  "2-2": {
   "n": 187,
   "auroc": {
    "c_score_align": 0.9156487077279155,
    "judge_cheap_disg": 0.8176923076923077,
    "p_peer_text": 0.9190561913334191
   },
   "delta_V0_minus_bar": {
    "n": 64,
    "n_error": 14,
    "n_correct": 50,
    "testable": false,
    "delta": -0.08307692307692305,
    "ci": [
     -0.26649739583333326,
     0.13743950393224424
    ],
    "p_le0": 0.7725,
    "ci_gt0": false,
    "pooled_delta": -0.07714285714285718,
    "ci_pooled_cluster_boot": [
     -0.26209523150925573,
     0.12796560484658948
    ]
   },
   "binary_e_d_thr0.5": {
    "c_score_align": {
     "e": 0.12345679012345678,
     "d": 0.07547169811320754
    },
    "judge_cheap_disg": {
     "e": 0.7857142857142857,
     "d": 0.0
    },
    "p_peer_text": {
     "e": 0.12345679012345678,
     "d": 0.018867924528301886
    }
   }
  },
  "3-3": {
   "n": 36,
   "auroc": {
    "c_score_align": 0.7181069958847737,
    "judge_cheap_disg": null,
    "p_peer_text": 0.6995884773662552
   },
   "delta_V0_minus_bar": null,
   "binary_e_d_thr0.5": {
    "c_score_align": {
     "e": 0.2222222222222222,
     "d": 0.6666666666666666
    },
    "judge_cheap_disg": {
     "e": 0.5,
     "d": 1.0
    },
    "p_peer_text": {
     "e": 0.2222222222222222,
     "d": 0.3333333333333333
    }
   }
  },
  "4-99": {
   "n": 50,
   "auroc": {
    "c_score_align": 0.44047619047619047,
    "judge_cheap_disg": null,
    "p_peer_text": 0.6706349206349206
   },
   "delta_V0_minus_bar": null,
   "binary_e_d_thr0.5": {
    "c_score_align": {
     "e": 0.0,
     "d": 1.0
    },
    "judge_cheap_disg": {
     "e": 0.5,
     "d": 0.0
    },
    "p_peer_text": {
     "e": 0.0,
     "d": 1.0
    }
   }
  }
 },
 "n_quant": {
  "0-0": {
   "n": 179,
   "auroc": {
    "c_score_align": 0.9161518661518661,
    "judge_cheap_disg": 0.8176923076923077,
    "p_peer_text": 0.9193693693693694
   },
   "delta_V0_minus_bar": {
    "n": 63,
    "n_error": 13,
    "n_correct": 50,
    "testable": false,
    "delta": -0.08307692307692305,
    "ci": [
     -0.26649739583333326,
     0.13743950393224424
    ],
    "p_le0": 0.7725,
    "ci_gt0": false,
    "pooled_delta": -0.08307692307692305,
    "ci_pooled_cluster_boot": [
     -0.2722046551626513,
     0.12857216343327452
    ]
   },
   "binary_e_d_thr0.5": {
    "c_score_align": {
     "e": 0.13513513513513514,
     "d": 0.06666666666666667
    },
    "judge_cheap_disg": {
     "e": 0.8461538461538461,
     "d": 0.0
    },
    "p_peer_text": {
     "e": 0.13513513513513514,
     "d": 0.009523809523809525
    }
   }
  },
  "1-1": {
   "n": 68,
   "auroc": {
    "c_score_align": 0.5912698412698413,
    "judge_cheap_disg": null,
    "p_peer_text": 0.7063492063492064
   },
   "delta_V0_minus_bar": null,
   "binary_e_d_thr0.5": {
    "c_score_align": {
     "e": 0.1111111111111111,
     "d": 0.7857142857142857
    },
    "judge_cheap_disg": {
     "e": 0.5,
     "d": 0.0
    },
    "p_peer_text": {
     "e": 0.1111111111111111,
     "d": 0.5714285714285714
    }
   }
  },
  "2-99": {
   "n": 26,
   "auroc": {
    "c_score_align": 0.6428571428571429,
    "judge_cheap_disg": null,
    "p_peer_text": 0.7678571428571429
   },
   "delta_V0_minus_bar": null,
   "binary_e_d_thr0.5": {
    "c_score_align": {
     "e": 0.0,
     "d": 1.0
    },
    "judge_cheap_disg": 
```

## System-level Kendall τ-b
# source: results/system_level_E2.json

```
{
 "c_score_align": {
  "tau_b": 0.7333333333333333,
  "p": 0.002212852733686067,
  "n_systems": 10
 },
 "judge_cheap_disg": {
  "tau_b": 1.0,
  "p": 1.0,
  "n_systems": 2
 },
 "p_peer_text": {
  "tau_b": 0.7777777777777777,
  "p": 0.0009463183421516755,
  "n_systems": 10
 },
 "judge_cheap2_orig": {
  "tau_b": NaN,
  "p": NaN,
  "n_systems": 0
 }
}
```

## Coverage
# source: results/coverage_E2.json

```
{
 "n_rows": 1100,
 "label_counts": {
  "ERROR": 590,
  "CORRECT": 339,
  "UNPARSEABLE": 115,
  "CONTESTED": 56
 },
 "parse_ok": 985,
 "consensus_imputed_lt2_peers": 0,
 "judge_missing_on_parseable": {
  "judge_cheap_disg": 803,
  "judge_cheap_orig": 985,
  "judge_cheap2_disg": 985,
  "judge_cheap2_orig": 985,
  "judge_local_qwen8b_disg": 0,
  "judge_local_qwen8b_orig": 0
 },
 "COVERAGE_view_long_deltas": {
  "c_score_align - judge_cheap_disg": {
   "n": 96,
   "n_error": 93,
   "n_correct": 3,
   "testable": false,
   "delta": -0.23015873015873012,
   "ci": [
    -0.5,
    0.5151515151515151
   ],
   "p_le0": 0.774,
   "ci_gt0": false,
   "pooled_delta": -0.15591397849462363,
   "ci_pooled_cluster_boot": [
    -0.5,
    0.5
   ]
  }
 },
 "COVERAGE_view_long_auroc": {
  "c_score_align": 0.6340782122905028,
  "judge_cheap_disg": 0.8492063492063492,
  "p_peer_text": 0.8561452513966481
 }
}
```

## Placebos
# source: results/placebo_E2.json

```
{
 "shuffled_labels_mean_auroc": 0.5008755017735967,
 "shuffled_labels_p95": 0.6064295977011493,
 "within_stratum_score_permutation_mean": 0.49735272988505747,
 "pass_0.5pm0.03": true
}
```

## Cost
# source: results/cost_E2A.json

```
{
 "spend_by_phase_usd": {
  "probe": 0.0,
  "pin_probe": 5e-05,
  "generation": 0.4889,
  "gate": 0.11022,
  "gate_trackh": 0.50926,
  "panel_heldout": 0.55802,
  "panel_heldout_adj": 0.22394,
  "judges_judge_cheap": 0.02951,
  "l3_questionnaire": 0.1251
 },
 "total_usd": 2.045,
 "cap_usd": 9.5,
 "iter4_dataset4_spend_excluded_usd": 0.2409,
 "consensus_cost_per_candidate": {
  "FULL_usd": 9.381944064545455e-05,
  "FULL_note": "the peers' generation cost: every slot's output of the sentence (10 slots) / candidates",
  "FULL_usd_per_sentence": 0.0009381944064545454,
  "MARGINAL_usd": 0.0,
  "MARGINAL_cpu_seconds": 1.4579636363636364,
  "MARGINAL_note": "eqmv z3 + text side CPU seconds per candidate (peers already exist)"
 },
 "judge_cost_per_call_usd": {
  "judge_cheap": 5.33022630834512e-05,
  "judge_cheap2": 0.0
 }
}
```

## Union with E2-B
# source: results/union_longpool.json

```
{
 "marker": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_12/e2b/E2B_FINAL_READY.json",
 "sha256_ok": true,
 "union_long_pool": {
  "n_rows": 94,
  "n_error": 76,
  "n_correct": 18,
  "n_sentences": 12,
  "n_err_sent": 12,
  "n_cor_sent": 8,
  "metrics": {
   "c_score_align": {
    "n": 94,
    "strat": 0.603448275862069,
    "strat_ci": [
     0.4625514159152033,
     0.7345736361361361
    ],
    "pooled": 0.6136695906432749,
    "coverage": 1.0
   },
   "judge_cheap_disg": {
    "n": 8,
    "strat": null
   },
   "judge_cheap_orig": {
    "n": 0,
    "strat": null
   }
  },
  "deltas": {},
  "testable": false
 },
 "note": "The label regime (the panel) is shared by E2-A and E2-B: the union adds SAMPLING power, not label-regime independence."
}
```

## Prefix used
# source: results/prefix_used.json

```
{
 "prefix_sentences": 110,
 "n_rows": 1100,
 "by_stratum": {
  "EXC": 370,
  "L25": 370,
  "DT": 360
 },
 "sentences_by_stratum": {
  "EXC": 37,
  "L25": 37,
  "DT": 36
 }
}
```
