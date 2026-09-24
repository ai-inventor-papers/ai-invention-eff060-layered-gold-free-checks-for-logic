# Tables: iteration-5 FREEZE experiment (dataset E = DEVELOPMENT data)

Generated 2026-09-24T12:16:51Z by `src/make_tables.py`. Population Z = 2672 R_AB rows (1810 ERROR / 862 CORRECT, 283 sentences) with >= 2 cross-family peers. CIs: sentence-cluster percentile bootstrap, B = 2000, seed 20260924. Orientation: higher = more likely ERROR.

## T1. Reproduction gates

# source: results/gate_G0.json :: src/step0_gates.py main(); results/gate_G1_labelfree.json :: src/score_variants.py main(); results/screen_E.json['repro'], ['oracle'] :: src/screen.py main(), oracle()

| gate | reproduced | target | pass |
|---|---|---|---|
| G0 V0 strat AUROC (R_AB 2,686) | 0.7415 | 0.7415 | True |
| G0 Δ(V0 − judge_cheap_disg) strat | 0.0990 [0.049, 0.146] | +0.099 [0.049, 0.146] | True |
| G0 Δ long pool | 0.1163 | +0.116 | True |
| G1 V0_rep vs frozen (|diff| > 1e-6) | 24/8469 = 0.2834% | <= 0.5% | True |
| c_exact pooled AUROC on Z | 0.7477 | 0.748 | True |
| 3-pool plain c pooled AUROC | 0.7845 | 0.7845 (eval-2 c_k3_best_oof) | True |
| eval-3 d_oracle 3-pool ALL / L25 | 0.3854 / 0.5422 | 0.385 / 0.542 | True |
| eval-3 END_MAJ 3-pool L25 d | 0.7349 | 0.735 | True |

## T2. Part A: AUROC per variant and cell (Z)

# source: results/screen_E.json['auroc'] :: src/screen.py main()

| score | ALL-strat | pooled | LONG-strat | L25 | L20 | EXC | CTRL |
|---|---|---|---|---|---|---|---|
| V0 c_score_align (frozen) | 0.742 [0.707, 0.774] | 0.784 [0.746, 0.818] | 0.743 [0.706, 0.776] | 0.713 [0.649, 0.770] | 0.724 [0.662, 0.779] | 0.815 [0.758, 0.868] | 0.738 [0.604, 0.864] |
| V0 (matrix re-derivation) | 0.742 [0.707, 0.774] | 0.783 [0.746, 0.817] | 0.742 [0.706, 0.775] | 0.712 [0.648, 0.769] | 0.724 [0.662, 0.779] | 0.815 [0.758, 0.868] | 0.738 [0.603, 0.864] |
| c_exact (aligner-free) | 0.689 [0.652, 0.726] | 0.748 [0.707, 0.784] | 0.672 [0.634, 0.711] | 0.611 [0.553, 0.671] | 0.652 [0.591, 0.704] | 0.794 [0.725, 0.851] | 0.857 [0.762, 0.931] |
| V1 plurality-normalised | 0.729 [0.697, 0.759] | 0.766 [0.736, 0.795] | 0.739 [0.706, 0.770] | 0.704 [0.642, 0.759] | 0.727 [0.670, 0.778] | 0.809 [0.761, 0.854] | 0.628 [0.567, 0.722] |
| V2 reliability-weighted | 0.752 [0.718, 0.784] | 0.790 [0.753, 0.823] | 0.750 [0.715, 0.784] | 0.718 [0.654, 0.774] | 0.737 [0.676, 0.790] | 0.819 [0.762, 0.871] | 0.773 [0.648, 0.890] |
| V3 = V1+V2 | 0.737 [0.705, 0.769] | 0.774 [0.743, 0.803] | 0.750 [0.717, 0.782] | 0.714 [0.652, 0.771] | 0.743 [0.686, 0.793] | 0.812 [0.763, 0.859] | 0.613 [0.530, 0.729] |
| V4 two-channel logistic | 0.758 [0.724, 0.793] | 0.799 [0.762, 0.832] | 0.751 [0.714, 0.787] | 0.719 [0.648, 0.780] | 0.732 [0.665, 0.789] | 0.830 [0.772, 0.883] | 0.826 [0.683, 0.935] |
| V5 = V3 on 3-pool | 0.735 [0.701, 0.766] | 0.775 [0.743, 0.805] | 0.746 [0.711, 0.778] | 0.694 [0.632, 0.750] | 0.771 [0.716, 0.817] | 0.780 [0.726, 0.831] | 0.629 [0.541, 0.746] |
| judge_cheap_disg | 0.641 [0.607, 0.678] | 0.696 [0.655, 0.736] | 0.624 [0.591, 0.659] | 0.641 [0.577, 0.706] | 0.615 [0.563, 0.667] | 0.615 [0.555, 0.675] | 0.807 [0.691, 0.916] |
| judge_cheap_orig | 0.624 [0.593, 0.654] | 0.636 [0.598, 0.673] | 0.629 [0.599, 0.659] | 0.653 [0.598, 0.705] | 0.611 [0.563, 0.657] | 0.624 [0.577, 0.676] | 0.571 [0.457, 0.696] |
| judge_cheap2_orig | 0.653 [0.615, 0.688] | 0.701 [0.656, 0.740] | 0.644 [0.606, 0.680] | 0.671 [0.612, 0.727] | 0.631 [0.567, 0.692] | 0.624 [0.556, 0.686] | 0.740 [0.592, 0.873] |

Cell sizes (n / ERROR / CORRECT / sentences): ALL-strat: 2672/1810/862/283; pooled: 2672/1810/862/283; LONG-strat: 2289/1664/625/247; L25: 869/694/175/108; L20: 818/589/229/77; EXC: 602/381/221/62; CTRL: 383/146/237/36

## T3. Part A: paired Δ AUROC vs V0 (frozen), same rows

# source: results/screen_E.json['delta_vs_V0'] :: src/screen.py main()

| variant | ALL-strat | pooled | LONG-strat | L25 | L20 | EXC | CTRL |
|---|---|---|---|---|---|---|---|
| V0 (matrix re-derivation) | -0.0003 [-0.001, 0.000] | -0.0003 [-0.001, 0.000] | -0.0003 [-0.001, 0.000] | -0.0008 [-0.003, 0.000] | +0.0000 [0.000, 0.000] | +0.0000 [0.000, 0.000] | -0.0003 [-0.002, 0.000] |
| c_exact (aligner-free) | -0.0528 [-0.087, -0.018] | -0.0360 [-0.063, -0.010] | -0.0702 [-0.103, -0.038] | -0.1017 [-0.168, -0.038] | -0.0720 [-0.122, -0.022] | -0.0218 [-0.064, 0.017] | +0.1186 [0.028, 0.208] |
| V1 plurality-normalised | -0.0133 [-0.030, 0.003] | -0.0172 [-0.032, -0.002] | -0.0035 [-0.014, 0.010] | -0.0089 [-0.024, 0.005] | +0.0033 [-0.018, 0.027] | -0.0064 [-0.028, 0.017] | -0.1098 [-0.221, 0.013] |
| V2 reliability-weighted | +0.0101 [0.006, 0.016] | +0.0062 [0.004, 0.009] | +0.0075 [0.004, 0.011] | +0.0047 [0.000, 0.009] | +0.0129 [0.007, 0.020] | +0.0032 [-0.001, 0.008] | +0.0355 [-0.001, 0.085] |
| V3 = V1+V2 | -0.0048 [-0.024, 0.013] | -0.0095 [-0.025, 0.007] | +0.0074 [-0.004, 0.020] | +0.0011 [-0.014, 0.016] | +0.0196 [-0.002, 0.043] | -0.0031 [-0.024, 0.020] | -0.1248 [-0.247, 0.009] |
| V4 two-channel logistic | +0.0161 [0.002, 0.032] | +0.0155 [0.006, 0.026] | +0.0088 [-0.004, 0.021] | +0.0056 [-0.015, 0.024] | +0.0081 [-0.015, 0.030] | +0.0145 [-0.005, 0.034] | +0.0880 [-0.000, 0.180] |
| V5 = V3 on 3-pool | -0.0073 [-0.033, 0.018] | -0.0088 [-0.027, 0.011] | +0.0030 [-0.021, 0.027] | -0.0191 [-0.063, 0.020] | +0.0472 [0.012, 0.086] | -0.0358 [-0.064, -0.006] | -0.1091 [-0.229, 0.021] |

## T4. Part A: pre-registered selection (5 variants screened)

# source: results/selection_E.json :: src/select_rule.py rule(), main(); freeze/selection.json :: src/freeze_part_a.py

Rule: winner = variant with highest E LONG-strat AUROC (Z) that (i) beats V0 by >= +0.015 there AND (ii) >= V0 on L25 (point) AND (iii) >= V0 - 0.01 on CTRL; none -> 'NONE: V0 stands'; tie (|Δ| < 1e-4) -> cheaper (V5 < others)

**Decision: NONE: V0 stands**

| variant | Δ LONG-strat | (i) >= +0.015 | (ii) L25 >= V0 | (iii) CTRL >= V0 − 0.01 | qualifies |
|---|---|---|---|---|---|
| V1 plurality-normalised | -0.0035 | False | False | False | False |
| V2 reliability-weighted | +0.0075 | False | True | True | False |
| V3 = V1+V2 | +0.0074 | False | True | False | False |
| V4 two-channel logistic | +0.0088 | False | True | True | False |
| V5 = V3 on 3-pool | +0.0030 | False | False | False | False |

Selection stability (B = 500 within-stratum sentence resamples, reported not gating): {"NONE: V0 stands": 0.876, "V4": 0.118, "V3": 0.002, "V5": 0.004}. Permutation null (B = 200 within-stratum label permutations, V4 re-cross-fitted): share of permutations in which ANY variant qualifies = 0.035 (per variant {"V1": 0.0, "V2": 0.0, "V3": 0.0, "V4": 0.0, "V5": 0.035}).

## T5. Binary decomposition at c > 0.5 (V4: flag rate matched to V0)

# source: results/screen_E.json['ed'] :: src/screen.py ed_block()

| score | ALL e / d | LONG e / d | L25 e / d | CTRL e / d | words_T1 e / d | words_T2 e / d | words_T3 e / d |
|---|---|---|---|---|---|---|---|
| V0 c_score_align (frozen) | 0.140 / 0.490 | 0.094 / 0.651 | 0.050 / 0.811 | 0.671 / 0.063 | 0.311 / 0.254 | 0.082 / 0.716 | 0.053 / 0.913 |
| V0 (matrix re-derivation) | 0.141 / 0.490 | 0.094 / 0.651 | 0.050 / 0.811 | 0.678 / 0.063 | 0.313 / 0.254 | 0.082 / 0.716 | 0.053 / 0.913 |
| c_exact (aligner-free) | 0.018 / 0.722 | 0.008 / 0.918 | 0.003 / 0.994 | 0.123 / 0.203 | 0.043 / 0.502 | 0.010 / 0.982 | 0.004 / 1.000 |
| V1 plurality-normalised | 0.343 / 0.174 | 0.309 / 0.224 | 0.241 / 0.417 | 0.733 / 0.042 | 0.463 / 0.061 | 0.355 / 0.225 | 0.216 / 0.513 |
| V2 reliability-weighted | 0.137 / 0.483 | 0.091 / 0.642 | 0.045 / 0.811 | 0.658 / 0.063 | 0.307 / 0.254 | 0.081 / 0.695 | 0.047 / 0.913 |
| V3 = V1+V2 | 0.303 / 0.186 | 0.266 / 0.240 | 0.197 / 0.434 | 0.726 / 0.042 | 0.438 / 0.066 | 0.296 / 0.251 | 0.185 / 0.522 |
| V4 two-channel logistic | 0.126 / 0.457 | 0.079 / 0.606 | 0.033 / 0.834 | 0.664 / 0.063 | 0.287 / 0.201 | 0.076 / 0.687 | 0.037 / 0.957 |
| V5 = V3 on 3-pool | 0.240 / 0.240 | 0.202 / 0.312 | 0.150 / 0.509 | 0.678 / 0.051 | 0.371 / 0.114 | 0.219 / 0.316 | 0.144 / 0.574 |

V0 flag rate on Z 0.7403; V4 matched threshold 0.6272.

### T5b. KEY DIAGNOSTIC: does d fall without e rising? (Δ vs V0, CI)

# source: results/screen_E.json['key_diagnostic'] :: src/screen.py main()

| variant | cut | Δd [CI] | Δe [CI] | d falls without e rising |
|---|---|---|---|---|
| c_exact (aligner-free) | words_T3 | +0.087 [0.016, 0.182] | -0.049 [-0.097, -0.012] | False |
| V1 plurality-normalised | words_T3 | -0.400 [-0.500, -0.283] | +0.163 [0.124, 0.202] | False |
| V2 reliability-weighted | words_T3 | +0.000 [0.000, 0.000] | -0.005 [-0.018, 0.004] | False |
| V3 = V1+V2 | words_T3 | -0.391 [-0.486, -0.275] | +0.132 [0.098, 0.166] | False |
| V4 two-channel logistic | words_T3 | +0.043 [0.000, 0.111] | -0.016 [-0.042, 0.006] | False |
| V5 = V3 on 3-pool | words_T3 | -0.339 [-0.453, -0.212] | +0.091 [0.059, 0.123] | False |
| c_exact (aligner-free) | L25 | +0.183 [0.074, 0.304] | -0.048 [-0.086, -0.015] | False |
| V1 plurality-normalised | L25 | -0.394 [-0.503, -0.283] | +0.190 [0.152, 0.229] | False |
| V2 reliability-weighted | L25 | +0.000 [0.000, 0.000] | -0.006 [-0.016, 0.002] | False |
| V3 = V1+V2 | L25 | -0.377 [-0.482, -0.268] | +0.147 [0.115, 0.180] | False |
| V4 two-channel logistic | L25 | +0.023 [-0.078, 0.125] | -0.017 [-0.041, 0.004] | False |
| V5 = V3 on 3-pool | L25 | -0.303 [-0.438, -0.155] | +0.099 [0.067, 0.132] | False |
| c_exact (aligner-free) | LONG | +0.267 [0.197, 0.340] | -0.085 [-0.116, -0.058] | False |
| V1 plurality-normalised | LONG | -0.427 [-0.499, -0.359] | +0.215 [0.186, 0.244] | False |
| V2 reliability-weighted | LONG | -0.010 [-0.025, 0.002] | -0.002 [-0.009, 0.004] | False |
| V3 = V1+V2 | LONG | -0.411 [-0.483, -0.345] | +0.172 [0.147, 0.197] | False |
| V4 two-channel logistic | LONG | -0.045 [-0.098, 0.009] | -0.015 [-0.029, 0.000] | False |
| V5 = V3 on 3-pool | LONG | -0.339 [-0.408, -0.275] | +0.108 [0.085, 0.131] | False |
| c_exact (aligner-free) | ALL | +0.232 [0.174, 0.294] | -0.123 [-0.164, -0.088] | False |
| V1 plurality-normalised | ALL | -0.316 [-0.383, -0.256] | +0.203 [0.175, 0.231] | False |
| V2 reliability-weighted | ALL | -0.007 [-0.019, 0.001] | -0.003 [-0.010, 0.003] | False |
| V3 = V1+V2 | ALL | -0.304 [-0.368, -0.247] | +0.162 [0.139, 0.186] | False |
| V4 two-channel logistic | ALL | -0.032 [-0.073, 0.008] | -0.014 [-0.028, 0.000] | False |
| V5 = V3 on 3-pool | ALL | -0.249 [-0.309, -0.196] | +0.100 [0.078, 0.123] | False |
| c_exact (aligner-free) | CTRL | +0.139 [0.063, 0.233] | -0.548 [-0.713, -0.333] | False |
| V1 plurality-normalised | CTRL | -0.021 [-0.062, 0.000] | +0.062 [0.008, 0.123] | False |
| V2 reliability-weighted | CTRL | +0.000 [0.000, 0.000] | -0.014 [-0.052, 0.019] | False |
| V3 = V1+V2 | CTRL | -0.021 [-0.062, 0.000] | +0.055 [0.000, 0.115] | False |
| V4 two-channel logistic | CTRL | +0.000 [-0.036, 0.026] | -0.007 [-0.047, 0.037] | False |
| V5 = V3 on 3-pool | CTRL | -0.013 [-0.048, 0.010] | +0.007 [-0.051, 0.084] | False |

### T5c. NET Δ(e+d), words T3 − T1 (eval-2 definition)

# source: results/screen_E.json['NET_T3_minus_T1'] :: src/screen.py main()

| score | NET [CI] | Δe | Δd |
|---|---|---|---|
| V0 c_score_align (frozen) | +0.401 [0.259, 0.533] | -0.258 | +0.659 |
| V0 (matrix re-derivation) | +0.399 [0.257, 0.532] | -0.260 | +0.659 |
| c_exact (aligner-free) | +0.458 [0.323, 0.579] | -0.040 | +0.498 |
| V1 plurality-normalised | +0.205 [0.067, 0.352] | -0.246 | +0.452 |
| V2 reliability-weighted | +0.399 [0.260, 0.535] | -0.260 | +0.659 |
| V3 = V1+V2 | +0.202 [0.069, 0.344] | -0.254 | +0.456 |
| V4 two-channel logistic | +0.506 [0.378, 0.624] | -0.250 | +0.755 |
| V5 = V3 on 3-pool | +0.233 [0.087, 0.390] | -0.227 | +0.460 |

## T6. Error-endorsement e per T9 error class (ERROR rows of the class not flagged)

# source: results/screen_E.json['t9_e'] :: src/screen.py main(); classes = exp-9 analyse.py classes() via src/labels.py t9_classes()

| class | n | V0 c_score_align (frozen) | V0 (matrix re-derivation) | c_exact (aligner-free) | V1 plurality-normalised | V2 reliability-weighted | V3 = V1+V2 | V4 two-channel logistic | V5 = V3 on 3-pool |
|---|---|---|---|---|---|---|---|---|---|
| ADD | 1033 | 0.151 | 0.151 | 0.026 | 0.328 | 0.142 | 0.295 | 0.131 | 0.229 |
| DROP | 1395 | 0.151 | 0.151 | 0.019 | 0.337 | 0.147 | 0.304 | 0.129 | 0.249 |
| COMPOUND | 1141 | 0.032 | 0.032 | 0.006 | 0.194 | 0.029 | 0.155 | 0.030 | 0.119 |
| polarity(NEG/REV/QUANT) | 432 | 0.056 | 0.056 | 0.000 | 0.190 | 0.053 | 0.148 | 0.037 | 0.111 |
| structural(CONN/RESTR/BIND/MOVE/SWAP/SCOPE/UNGLUE) | 1293 | 0.082 | 0.083 | 0.004 | 0.275 | 0.081 | 0.228 | 0.073 | 0.172 |
| MEANING_RENAME-type (MEANING_RENAME op or tier-B VOCAB_GRAN) | 219 | 0.502 | 0.507 | 0.009 | 0.872 | 0.525 | 0.822 | 0.411 | 0.721 |

## T7. Oracle bound (eval-3 R_oracle, label-using diagnostic)

# source: results/screen_E.json['oracle'] :: src/screen.py oracle()

| pool | cut | d_oracle | d_V0 | variant | d_v | e_v | gap_closed |
|---|---|---|---|---|---|---|---|
| 9fam | ALL | 0.586 | 0.490 | V0 c_score_align (frozen) | 0.490 | 0.140 | ILL_CONDITIONED |
| 9fam | ALL | 0.586 | 0.490 | V1 plurality-normalised | 0.174 | 0.343 | ILL_CONDITIONED |
| 9fam | ALL | 0.586 | 0.490 | V2 reliability-weighted | 0.483 | 0.137 | ILL_CONDITIONED |
| 9fam | ALL | 0.586 | 0.490 | V3 = V1+V2 | 0.186 | 0.303 | ILL_CONDITIONED |
| 9fam | ALL | 0.586 | 0.490 | V4 two-channel logistic | 0.457 | 0.126 | ILL_CONDITIONED |
| 9fam | LONG | 0.758 | 0.651 | V0 c_score_align (frozen) | 0.651 | 0.094 | ILL_CONDITIONED |
| 9fam | LONG | 0.758 | 0.651 | V1 plurality-normalised | 0.224 | 0.309 | ILL_CONDITIONED |
| 9fam | LONG | 0.758 | 0.651 | V2 reliability-weighted | 0.642 | 0.091 | ILL_CONDITIONED |
| 9fam | LONG | 0.758 | 0.651 | V3 = V1+V2 | 0.240 | 0.266 | ILL_CONDITIONED |
| 9fam | LONG | 0.758 | 0.651 | V4 two-channel logistic | 0.606 | 0.079 | ILL_CONDITIONED |
| 9fam | L25 | 0.834 | 0.811 | V0 c_score_align (frozen) | 0.811 | 0.050 | ILL_CONDITIONED |
| 9fam | L25 | 0.834 | 0.811 | V1 plurality-normalised | 0.417 | 0.241 | ILL_CONDITIONED |
| 9fam | L25 | 0.834 | 0.811 | V2 reliability-weighted | 0.811 | 0.045 | ILL_CONDITIONED |
| 9fam | L25 | 0.834 | 0.811 | V3 = V1+V2 | 0.434 | 0.197 | ILL_CONDITIONED |
| 9fam | L25 | 0.834 | 0.811 | V4 two-channel logistic | 0.834 | 0.033 | ILL_CONDITIONED |
| 9fam | words_T3 | 0.887 | 0.913 | V0 c_score_align (frozen) | 0.913 | 0.053 | ILL_CONDITIONED |
| 9fam | words_T3 | 0.887 | 0.913 | V1 plurality-normalised | 0.513 | 0.216 | ILL_CONDITIONED |
| 9fam | words_T3 | 0.887 | 0.913 | V2 reliability-weighted | 0.913 | 0.047 | ILL_CONDITIONED |
| 9fam | words_T3 | 0.887 | 0.913 | V3 = V1+V2 | 0.522 | 0.185 | ILL_CONDITIONED |
| 9fam | words_T3 | 0.887 | 0.913 | V4 two-channel logistic | 0.957 | 0.037 | ILL_CONDITIONED |
| 3pool | ALL | 0.385 | 0.486 | V5 = V3 on 3-pool | 0.230 | 0.246 | +2.535 |
| 3pool | LONG | 0.488 | 0.649 | V5 = V3 on 3-pool | 0.301 | 0.207 | +2.162 |
| 3pool | L25 | 0.542 | 0.813 | V5 = V3 on 3-pool | 0.482 | 0.159 | +1.222 |
| 3pool | words_T3 | 0.624 | 0.917 | V5 = V3 on 3-pool | 0.550 | 0.154 | +1.250 |

## T8. Context: Δ vs the cheap API judges (frozen exp-6 columns)

# source: results/screen_E.json['delta_vs_judges'] :: src/screen.py main()

| contrast | ALL-strat | LONG-strat | L25 |
|---|---|---|---|
| V0_frozen - judge_cheap_disg | +0.101 [0.053, 0.145] | +0.118 [0.068, 0.163] | +0.072 [-0.015, 0.153] |
| V0_frozen - judge_cheap_orig | +0.119 [0.079, 0.157] | +0.114 [0.073, 0.153] | +0.060 [-0.003, 0.125] |
| V0_frozen - judge_cheap2_orig | +0.090 [0.044, 0.136] | +0.099 [0.053, 0.147] | +0.042 [-0.046, 0.129] |
| V1 - judge_cheap_disg | +0.088 [0.039, 0.131] | +0.115 [0.066, 0.159] | +0.063 [-0.020, 0.142] |
| V1 - judge_cheap_orig | +0.105 [0.066, 0.143] | +0.110 [0.069, 0.150] | +0.051 [-0.014, 0.117] |
| V1 - judge_cheap2_orig | +0.076 [0.032, 0.124] | +0.096 [0.051, 0.144] | +0.033 [-0.054, 0.120] |
| V2 - judge_cheap_disg | +0.111 [0.064, 0.155] | +0.126 [0.076, 0.171] | +0.076 [-0.011, 0.156] |
| V2 - judge_cheap_orig | +0.129 [0.089, 0.168] | +0.121 [0.081, 0.161] | +0.065 [0.001, 0.130] |
| V2 - judge_cheap2_orig | +0.100 [0.056, 0.147] | +0.107 [0.061, 0.155] | +0.046 [-0.041, 0.134] |
| V3 - judge_cheap_disg | +0.096 [0.046, 0.142] | +0.126 [0.078, 0.171] | +0.073 [-0.011, 0.153] |
| V3 - judge_cheap_orig | +0.114 [0.075, 0.151] | +0.121 [0.080, 0.160] | +0.062 [-0.004, 0.128] |
| V3 - judge_cheap2_orig | +0.085 [0.040, 0.133] | +0.106 [0.062, 0.154] | +0.043 [-0.044, 0.129] |
| V4 - judge_cheap_disg | +0.117 [0.069, 0.162] | +0.127 [0.077, 0.174] | +0.077 [-0.011, 0.160] |
| V4 - judge_cheap_orig | +0.135 [0.093, 0.175] | +0.122 [0.081, 0.164] | +0.066 [-0.006, 0.135] |
| V4 - judge_cheap2_orig | +0.106 [0.060, 0.154] | +0.108 [0.060, 0.159] | +0.047 [-0.049, 0.136] |
| V5 - judge_cheap_disg | +0.093 [0.042, 0.139] | +0.121 [0.071, 0.166] | +0.053 [-0.034, 0.135] |
| V5 - judge_cheap_orig | +0.111 [0.072, 0.150] | +0.117 [0.074, 0.157] | +0.041 [-0.029, 0.112] |
| V5 - judge_cheap2_orig | +0.082 [0.035, 0.129] | +0.102 [0.056, 0.149] | +0.022 [-0.071, 0.113] |

## T9. GG checker gates (google/gemini-2.5-flash, non-thinking, T = 0)

# source: results/gg_gates_dev_v1.json, results/gg_gates_confirm_v2.json :: src/gg_gates.py run(), score()

| gate | half | prompt | balanced acc. | TPR | TNR | n YES / NO |
|---|---|---|---|---|---|---|
| G-A | dev | v1 | 0.780 | 0.789 | 0.770 | 190 / 252 |
| G-B | dev | v1 | 0.950 | 0.966 | 0.934 | 29 / 91 |
| G-A | confirm | v2 | 0.907 | 0.841 | 0.974 | 170 / 228 |
| G-B | confirm | v2 | 0.941 | 0.917 | 0.965 | 24 / 85 |

G-A per class, dev v1: {"NO_DONOR": 0.841, "NO_MERGE": 1.0, "NO_NONCE": 0.508, "NO_ROLE": 0.73, "YES_FORM": 0.492, "YES_IDENT": 0.968, "YES_SYN": 0.906}; confirm v2: {"NO_DONOR": 0.965, "NO_MERGE": 1.0, "NO_NONCE": 0.93, "NO_ROLE": 1.0, "YES_FORM": 0.754, "YES_IDENT": 0.965, "YES_SYN": 0.804}. G-B has 53 YES / 176 NO pairs in total (< 60 YES): NOT_TESTABLE as a gate (F9), reported descriptively. The single allowed prompt revision (v1 -> v2) followed the failed G-A dev half (prompt_revision_v2.json).

## T10. GG dev gates -> status FAIL(g3)

# source: results/gg_dev.json['gates'] :: src/gg_score.py main(), perturb_gates()

| gate | value | rule | pass |
|---|---|---|---|
| g1 RENAME_SYN paired flip | 0.034 (FA 0.932 vs paired-base FA 0.898; all-base FA 0.828) | flip <= 0.05 and FA <= FA(base) + 0.05 | True |
| g2 MEANING_RENAME recall | GG 1.000 vs c_align 1.000 (base FA GG 0.828 / c_align 0.712; recall given base endorsed 1.000 / 1.000) | >= c_align − 0.05 | True |
| g3 E strat AUROC | GG 0.696 vs V0 0.742, Δ CI [-0.071, -0.021] | >= V0 − 0.01 | False |
| checker | G-A confirm BA 0.907; G-B NOT_TESTABLE (descriptive BA 0.941) | G-A >= 0.90 | True |

RENAME_NONCE (pre-stated EXPECTED failure, not gated): FA 1.000, paired-base FA 0.773, paired flip 0.227 (n 110).

### T10b. Rename invariance / MEANING_RENAME recall per metric and control type (PERTURB E-bases, c > 0.5)

# source: results/gg_dev.json['perturb'] :: src/gg_score.py perturb_gates()

| metric | base FA (all) | SYN FA / flip | NONCE FA / flip | MEANING_RENAME recall | recall | base endorsed | by polarity |
|---|---|---|---|---|---|---|
| c_gg | 0.828 | 0.932 / 0.034 | 1.000 / 0.227 | 1.000 | 1.000 (n 239) | {"DOWN": 1.0, "UP": 1.0} |
| c_gg_allyes | 0.798 | 0.864 / 0.000 | 0.745 / 0.000 | 0.821 | 0.762 (n 239) | {"DOWN": 0.84, "UP": 0.799} |
| c_exact_pt | 0.894 | 1.000 / 0.068 | 1.000 / 0.136 | 1.000 | 1.000 (n 239) | {"DOWN": 1.0, "UP": 1.0} |
| c_align | 0.712 | 0.943 / 0.182 | 1.000 / 0.327 | 1.000 | 1.000 (n 239) | {"DOWN": 1.0, "UP": 1.0} |

By base status (SYN, GG): {"GOLD_PANEL_OK": {"n": 51, "FA": 0.98, "FA_base": 0.961, "flip": 0.02}, "PANEL_REPAIRED": {"n": 30, "FA": 0.967, "FA_base": 0.933, "flip": 0.033}, "TRUSTED_AGREED": {"n": 7, "FA": 0.429, "FA_base": 0.286, "flip": 0.143}}

## T11. GG on E (Z): AUROC, e/d, T9 e

# source: results/gg_dev.json['auroc'], ['ed'], ['t9_e'] :: src/gg_score.py main()

| score | ALL-strat | pooled | LONG-strat | L25 | CTRL |
|---|---|---|---|---|---|
| GG (PRIMARY) | 0.696 [0.659, 0.733] | 0.751 [0.711, 0.788] | 0.689 [0.650, 0.726] | 0.657 [0.596, 0.712] | 0.773 [0.638, 0.896] |
| GG bracket: all maps accepted | 0.685 [0.648, 0.722] | 0.745 [0.703, 0.782] | 0.683 [0.644, 0.722] | 0.652 [0.586, 0.710] | 0.709 [0.560, 0.852] |
| c_exact (aligner-free) | 0.689 [0.652, 0.726] | 0.748 [0.707, 0.784] | 0.672 [0.634, 0.711] | 0.611 [0.553, 0.671] | 0.857 [0.762, 0.931] |
| V0 c_score_align (frozen) | 0.742 [0.707, 0.774] | 0.784 [0.746, 0.818] | 0.743 [0.706, 0.776] | 0.713 [0.649, 0.770] | 0.738 [0.604, 0.864] |
| Δ GG (PRIMARY) − V0 | -0.046 [-0.071, -0.021] | -0.033 [-0.052, -0.015] | -0.054 [-0.080, -0.030] | -0.056 [-0.097, -0.018] | +0.035 [-0.032, 0.101] |
| Δ GG bracket: all maps accepted − V0 | -0.057 [-0.079, -0.037] | -0.039 [-0.056, -0.023] | -0.060 [-0.083, -0.037] | -0.061 [-0.097, -0.026] | -0.029 [-0.116, 0.046] |
| Δ c_exact (aligner-free) − V0 | -0.053 [-0.087, -0.018] | -0.036 [-0.063, -0.010] | -0.070 [-0.103, -0.038] | -0.102 [-0.168, -0.038] | +0.119 [0.028, 0.208] |

| score | ALL e / d | LONG e / d | L25 e / d | words_T3 e / d |
|---|---|---|---|---|
| GG (PRIMARY) | 0.081 / 0.629 | 0.038 / 0.822 | 0.022 / 0.960 | 0.026 / 0.983 |
| GG bracket: all maps accepted | 0.113 / 0.616 | 0.069 / 0.808 | 0.048 / 0.943 | 0.047 / 0.974 |
| c_exact (aligner-free) | 0.018 / 0.722 | 0.008 / 0.918 | 0.003 / 0.994 | 0.004 / 1.000 |
| V0 c_score_align (frozen) | 0.140 / 0.490 | 0.094 / 0.651 | 0.050 / 0.811 | 0.053 / 0.913 |

| T9 class | n | GG e | GG all-yes e | exact e | V0 e |
|---|---|---|---|---|---|
| ADD | 1033 | 0.085 | 0.118 | 0.026 | 0.151 |
| DROP | 1395 | 0.081 | 0.116 | 0.019 | 0.151 |
| COMPOUND | 1141 | 0.018 | 0.030 | 0.006 | 0.032 |
| polarity(NEG/REV/QUANT) | 432 | 0.023 | 0.030 | 0.000 | 0.056 |
| structural(CONN/RESTR/BIND/MOVE/SWAP/SCOPE/UNGLUE) | 1293 | 0.039 | 0.062 | 0.004 | 0.082 |
| MEANING_RENAME-type (MEANING_RENAME op or tier-B VOCAB_GRAN) | 219 | 0.224 | 0.338 | 0.009 | 0.502 |

Non-exact E node pairs: 11889; outcomes {"PREFILTER": 10514, "gloss_rejected": 403, "gloss_yes": 675, "identity_map": 12, "NO_MAP": 285}; map found 0.092; gloss-rejected 0.034; capped 0.000. eqmv vs GG: {"align=True,gg=True": 583, "align=True,gg=False": 946, "align=False,gg=True": 104, "align=False,gg=False": 10256}.

### T11c. Gloss disagreements with the aligner (10 each)

# source: results/gg_dev.json['examples'] :: src/gg_score.py main()

| direction | renamed pairs (GG YES: the accepting map; GG NO: the first kept map) | formula i | formula j |
|---|---|---|---|
| GG YES, eqmv rejected | ArtFormFrom/2 -> FormOfArtFrom/2; specificPaper -> specificTypeOfPaper | `∀v0 (((((Painting(v0) ∧ CreatedUsing(v0, waterSolublePigments)) ∧ AppliedTo(v0, specificPaper)) ∧ ArtFormFrom(v0, particularRegion)) → WatercolorPainting(v0)))` | `∀v0 (((((Painting(v0) ∧ CreatedUsing(v0, waterSolublePigments)) ∧ AppliedTo(v0, specificTypeOfPaper)) ∧ FormOfArtFrom(v0, particularRegion)) → WatercolorPainting(v0)))` |
| GG YES, eqmv rejected | ArtFormFrom/2 -> FromRegion/2; CreatedUsing/2 -> CreatedWith/2; WatercolorPainting/1 -> UsuallyWatercolor/1 | `∀v0 (((((Painting(v0) ∧ CreatedUsing(v0, waterSolublePigments)) ∧ AppliedTo(v0, specificPaper)) ∧ ArtFormFrom(v0, particularRegion)) → WatercolorPainting(v0)))` | `∀v0 (((((Painting(v0) ∧ CreatedWith(v0, waterSolublePigments)) ∧ AppliedTo(v0, specificPaper)) ∧ FromRegion(v0, particularRegion)) → UsuallyWatercolor(v0)))` |
| GG YES, eqmv rejected | ArtFrom/2 -> FormOfArtFrom/2; specificPaper -> specificTypeOfPaper | `∀v0 (((((Painting(v0) ∧ CreatedUsing(v0, waterSolublePigments)) ∧ AppliedTo(v0, specificPaper)) ∧ ArtFrom(v0, particularRegion)) → WatercolorPainting(v0)))` | `∀v0 (((((Painting(v0) ∧ CreatedUsing(v0, waterSolublePigments)) ∧ AppliedTo(v0, specificTypeOfPaper)) ∧ FormOfArtFrom(v0, particularRegion)) → WatercolorPainting(v0)))` |
| GG YES, eqmv rejected | ArtFrom/2 -> FromRegion/2; CreatedUsing/2 -> CreatedWith/2; WatercolorPainting/1 -> UsuallyWatercolor/1 | `∀v0 (((((Painting(v0) ∧ CreatedUsing(v0, waterSolublePigments)) ∧ AppliedTo(v0, specificPaper)) ∧ ArtFrom(v0, particularRegion)) → WatercolorPainting(v0)))` | `∀v0 (((((Painting(v0) ∧ CreatedWith(v0, waterSolublePigments)) ∧ AppliedTo(v0, specificPaper)) ∧ FromRegion(v0, particularRegion)) → UsuallyWatercolor(v0)))` |
| GG YES, eqmv rejected | CreatedUsing/2 -> CreatedWith/2; FormOfArtFrom/2 -> FromRegion/2; WatercolorPainting/1 -> UsuallyWatercolor/1; specificTypeOfPaper -> specificPaper | `∀v0 (((((Painting(v0) ∧ CreatedUsing(v0, waterSolublePigments)) ∧ AppliedTo(v0, specificTypeOfPaper)) ∧ FormOfArtFrom(v0, particularRegion)) → WatercolorPainting(v0)))` | `∀v0 (((((Painting(v0) ∧ CreatedWith(v0, waterSolublePigments)) ∧ AppliedTo(v0, specificPaper)) ∧ FromRegion(v0, particularRegion)) → UsuallyWatercolor(v0)))` |
| GG YES, eqmv rejected | UsuallyWatercolorPainting/1 -> Watercolor/1; specificTypeOfPaper -> specificTypePaper | `∀v0 ((((CreatedUsing(v0, waterSolublePigments) ∧ AppliedTo(v0, specificTypeOfPaper)) ∧ FormOfArt(v0, particularRegion)) → UsuallyWatercolorPainting(v0)))` | `∀v0 ((((CreatedUsing(v0, waterSolublePigments) ∧ AppliedTo(v0, specificTypePaper)) ∧ FormOfArt(v0, particularRegion)) → Watercolor(v0)))` |
| GG YES, eqmv rejected | Requires/2 -> RequiresWaterLevel/2; moderateWater -> moderate | `∀v0 (((((Plant(v0) ∧ GrowsWellIn(v0, partialShade)) ∧ HasColorfulFlowers(v0)) ∧ Requires(v0, moderateWater)) → SuitableFor(v0, shadedGarden)))` | `∀v0 (((((Plant(v0) ∧ GrowsWellIn(v0, partialShade)) ∧ HasColorfulFlowers(v0)) ∧ RequiresWaterLevel(v0, moderate)) → SuitableFor(v0, shadedGarden)))` |
| GG YES, eqmv rejected | CanBeDisplayedOn/2 -> DisplayableOn/2 | `∀v0 ((((CreatedUsing(v0, digitalTools) ∧ CanBeDisplayedOn(v0, electronicDevices)) ∧ Interactive(v0)) → DigitalInteractiveArtwork(v0)))` | `∀v0 ((((CreatedUsing(v0, digitalTools) ∧ DisplayableOn(v0, electronicDevices)) ∧ Interactive(v0)) → DigitalInteractiveArtwork(v0)))` |
| GG YES, eqmv rejected | CreatedByDeposition/1 -> DepositedBySediment/1 | `∀v0 (((((GeologicalFormation(v0) ∧ CreatedByDeposition(v0)) ∧ FormsLayersOverTime(v0)) ∧ ContainsFossils(v0)) → SedimentaryRock(v0)))` | `∀v0 (((((GeologicalFormation(v0) ∧ DepositedBySediment(v0)) ∧ FormsLayersOverTime(v0)) ∧ ContainsFossils(v0)) → SedimentaryRock(v0)))` |
| GG YES, eqmv rejected | Activities/2 -> UsedFor/2; FlatSurface/1 -> HasFlatSurface/1; Furniture/1 -> PieceOfFurniture/1 | `∀v0 (((((Furniture(v0) ∧ FlatSurface(v0)) ∧ SupportedByLegs(v0)) ∧ ((Activities(v0, eating) ∨ Activities(v0, writing)) ∨ Activities(v0, working))) → Table(v0)))` | `∀v0 (((((PieceOfFurniture(v0) ∧ HasFlatSurface(v0)) ∧ SupportedByLegs(v0)) ∧ ((UsedFor(v0, eating) ∨ UsedFor(v0, writing)) ∨ UsedFor(v0, working))) → Table(v0)))` |
| GG NO (gloss), eqmv accepted | GrowsWell/2 -> GrowsWellIn/2; RequiresWater/2 -> Requires/2; moderate -> moderateWater | `∀v0 (((((Plant(v0) ∧ GrowsWell(v0, partialShade)) ∧ HasColorfulFlowers(v0)) ∧ RequiresWater(v0, moderate)) → SuitableFor(v0, shadedGarden)))` | `∀v0 (((((Plant(v0) ∧ GrowsWellIn(v0, partialShade)) ∧ HasColorfulFlowers(v0)) ∧ Requires(v0, moderateWater)) → SuitableFor(v0, shadedGarden)))` |
| GG NO (gloss), eqmv accepted | ColorfulFlowers/1 -> GrowsWellInPartialShade/1; GrowsWellInPartialShade/1 -> HasColorfulFlowers/1 | `∀v0 (((((Plant(v0) ∧ GrowsWellInPartialShade(v0)) ∧ ColorfulFlowers(v0)) ∧ RequiresModerateWater(v0)) → SuitableForShadedGarden(v0)))` | `∀v0 (((((Plant(v0) ∧ GrowsWellInPartialShade(v0)) ∧ HasColorfulFlowers(v0)) ∧ RequiresModerateWater(v0)) → SuitableForShadedGarden(v0)))` |
| GG NO (gloss), eqmv accepted | CanBeDisplayedOn/2 -> CreatedUsing/2; CreatedUsing/2 -> DisplayedOn/2; digitalTools -> electronicDevices; electronicDevices -> digitalTools | `∀v0 (((((Artwork(v0) ∧ CreatedUsing(v0, digitalTools)) ∧ CanBeDisplayedOn(v0, electronicDevices)) ∧ Interactive(v0)) → DigitalInteractiveArtwork(v0)))` | `∀v0 (((((Artwork(v0) ∧ CreatedUsing(v0, digitalTools)) ∧ DisplayedOn(v0, electronicDevices)) ∧ Interactive(v0)) → DigitalInteractiveArtwork(v0)))` |
| GG NO (gloss), eqmv accepted | CreatedUsing/2 -> CanBeDisplayedOn/2; DisplayedOn/2 -> CreatedWith/2; digitalTools -> electronicDevices; electronicDevices -> digitalTools | `∀v0 (((((Artwork(v0) ∧ CreatedUsing(v0, digitalTools)) ∧ DisplayedOn(v0, electronicDevices)) ∧ Interactive(v0)) → DigitalInteractiveArtwork(v0)))` | `∀v0 (((((Artwork(v0) ∧ CreatedWith(v0, digitalTools)) ∧ CanBeDisplayedOn(v0, electronicDevices)) ∧ Interactive(v0)) → DigitalInteractiveArtwork(v0)))` |
| GG NO (gloss), eqmv accepted | ConsistsOfMultipleMovements/1 -> MusicalComposition/1; FeaturesSoloInstrumentAccompaniedByOrchestra/1 -> OftenFeaturesSoloInstrumentWithOrchestra/1; MusicalComposition/1 -> TypicallyConsistsOfMultipleMovements/1 | `∀v0 ((((MusicalComposition(v0) ∧ ConsistsOfMultipleMovements(v0)) ∧ FeaturesSoloInstrumentAccompaniedByOrchestra(v0)) → Concerto(v0)))` | `∀v0 ((((MusicalComposition(v0) ∧ TypicallyConsistsOfMultipleMovements(v0)) ∧ OftenFeaturesSoloInstrumentWithOrchestra(v0)) → Concerto(v0)))` |
| GG NO (gloss), eqmv accepted | HasAdaptedDigestiveSystem/2 -> HasDigestiveSystem/2; meat -> adaptedForMeat | `∀v0 ((Animal(v0) → (Carnivore(v0) ↔ (PrimarilyFeedsOn(v0, otherAnimals) ∧ HasAdaptedDigestiveSystem(v0, meat)))))` | `∀v0 ((Animal(v0) → (Carnivore(v0) ↔ (PrimarilyFeedsOn(v0, otherAnimals) ∧ HasDigestiveSystem(v0, adaptedForMeat)))))` |
| GG NO (gloss), eqmv accepted | HasAdaptedDigestiveSystemFor/2 -> HasDigestiveSystem/2; meat -> adaptedForMeat | `∀v0 ((Animal(v0) → (Carnivore(v0) ↔ (PrimarilyFeedsOn(v0, otherAnimals) ∧ HasAdaptedDigestiveSystemFor(v0, meat)))))` | `∀v0 ((Animal(v0) → (Carnivore(v0) ↔ (PrimarilyFeedsOn(v0, otherAnimals) ∧ HasDigestiveSystem(v0, adaptedForMeat)))))` |
| GG NO (gloss), eqmv accepted | CreatedBy/2 -> CreatedByDeposition/2; DepositionOfSediment -> sediment | `∀v0 (((((GeologicalFormation(v0) ∧ CreatedBy(v0, DepositionOfSediment)) ∧ FormsLayersOverTime(v0)) ∧ Contains(v0, Fossils)) → SedimentaryRock(v0)))` | `∀v0 (((((GeologicalFormation(v0) ∧ CreatedByDeposition(v0, sediment)) ∧ FormsLayersOverTime(v0)) ∧ Contains(v0, fossils)) → SedimentaryRock(v0)))` |
| GG NO (gloss), eqmv accepted | CreatedBy/2 -> CreatedByDepositionOf/2; DepositionOfSediment -> sediment | `∀v0 (((((GeologicalFormation(v0) ∧ CreatedBy(v0, DepositionOfSediment)) ∧ FormsLayersOverTime(v0)) ∧ Contains(v0, Fossils)) → SedimentaryRock(v0)))` | `∀v0 (((((GeologicalFormation(v0) ∧ CreatedByDepositionOf(v0, sediment)) ∧ FormsLayersOverTime(v0)) ∧ Contains(v0, fossils)) → SedimentaryRock(v0)))` |
| GG NO (gloss), eqmv accepted | CreatedBy/2 -> CreatedByDeposition/2; depositionOfSediment -> sediment | `∀v0 (((((GeologicalFormation(v0) ∧ CreatedBy(v0, depositionOfSediment)) ∧ FormsLayersOverTime(v0)) ∧ Contains(v0, fossils)) → SedimentaryRock(v0)))` | `∀v0 (((((GeologicalFormation(v0) ∧ CreatedByDeposition(v0, sediment)) ∧ FormsLayersOverTime(v0)) ∧ Contains(v0, fossils)) → SedimentaryRock(v0)))` |

## T12. GG cost

# source: results/gg_dev.json['cost'] :: src/gg_score.py main(); cost_ledger.jsonl

| item | value |
|---|---|
| gloss sweep $ (E + PERTURB) | 0.1630 |
| $ per call (<= 12 pairs) | 0.000393 |
| FULL per E candidate: CPU s / $ (upper) | 0.038 / 0.000047 |
| MARGINAL per candidate: CPU s / $ | 0.106 / 0.000010 |
| peer generation $ per sentence (7 families, shared with V0) | 0.002206 |

## T13. SECONDARY GG_B (freelab family with B1-B5 bridges; PRIMARY-accepted pairs kept)

# source: results/ggb_dev.json :: src/ggb_score.py main()

Status: UNTESTED(budget): the run-level OpenRouter budget was exhausted before the GG_B gloss (HTTP 403 aii_run_budget_exhausted); GG_B agreement is bracketed by c_gg (no bridged map accepted; c_ggb == c_gg as run) and c_ggb_allyes (every bridged map accepted). agreement sets are nested (GG ⊆ GG_B ⊆ GG_B all-yes), so per row c_ggb_allyes <= c_ggb <= c_gg and, at c > 0.5, GG_B's e lies in [e(c_gg), e(c_ggb_allyes)] and its d in [d(c_ggb_allyes), d(c_gg)]; AUROC is NOT guaranteed to lie between the brackets.

| score | ALL-strat | pooled | LONG-strat | L25 | CTRL |
|---|---|---|---|---|---|
| GG_B bracket: every bridged map accepted | 0.653 [0.614, 0.691] | 0.697 [0.657, 0.737] | 0.669 [0.631, 0.705] | 0.631 [0.572, 0.688] | 0.495 [0.369, 0.649] |
| GG (PRIMARY) | 0.696 [0.659, 0.733] | 0.751 [0.711, 0.788] | 0.689 [0.650, 0.726] | 0.657 [0.596, 0.712] | 0.773 [0.638, 0.896] |
| c_exact (aligner-free) | 0.689 [0.652, 0.726] | 0.748 [0.707, 0.784] | 0.672 [0.634, 0.711] | 0.611 [0.553, 0.671] | 0.857 [0.762, 0.931] |
| V0 c_score_align (frozen) | 0.742 [0.707, 0.774] | 0.784 [0.746, 0.818] | 0.743 [0.706, 0.776] | 0.713 [0.649, 0.770] | 0.738 [0.604, 0.864] |
| Δ c_ggb_allyes - V0 | -0.090 [-0.121, -0.059] | -0.087 [-0.113, -0.064] | -0.074 [-0.103, -0.046] | -0.082 [-0.133, -0.032] | -0.243 [-0.403, -0.084] |
| Δ c_gg - V0 | -0.046 [-0.071, -0.021] | -0.033 [-0.052, -0.015] | -0.054 [-0.080, -0.030] | -0.056 [-0.097, -0.018] | +0.035 [-0.032, 0.101] |

| score | ALL e / d | LONG e / d | L25 e / d | words_T3 e / d |
|---|---|---|---|---|
| GG_B bracket: every bridged map accepted | 0.334 / 0.358 | 0.294 / 0.472 | 0.264 / 0.623 | 0.246 / 0.739 |
| GG (PRIMARY) | 0.081 / 0.629 | 0.038 / 0.822 | 0.022 / 0.960 | 0.026 / 0.983 |
| c_exact (aligner-free) | 0.018 / 0.722 | 0.008 / 0.918 | 0.003 / 0.994 | 0.004 / 1.000 |
| V0 c_score_align (frozen) | 0.140 / 0.490 | 0.094 / 0.651 | 0.050 / 0.811 | 0.053 / 0.913 |

| T9 class | n | GG_B all-yes e (upper) | GG e (lower) | exact e | V0 e |
|---|---|---|---|---|---|
| ADD | 1033 | 0.367 | 0.085 | 0.026 | 0.151 |
| DROP | 1395 | 0.353 | 0.081 | 0.019 | 0.151 |
| COMPOUND | 1141 | 0.209 | 0.018 | 0.006 | 0.032 |
| polarity(NEG/REV/QUANT) | 432 | 0.116 | 0.023 | 0.000 | 0.056 |
| structural(CONN/RESTR/BIND/MOVE/SWAP/SCOPE/UNGLUE) | 1293 | 0.219 | 0.039 | 0.004 | 0.082 |
| MEANING_RENAME-type (MEANING_RENAME op or tier-B VOCAB_GRAN) | 219 | 0.689 | 0.224 | 0.009 | 0.502 |

GG_B search: {"n_pairs": 11202, "status": {"MAPPED": 3133, "NO_MAP": 7899, "CAPPED": 170}, "capped": 248, "cpu_s": 3325.558, "n_killed_at_deadline": 53, "bridges_in_accepted_maps": {"B2": 1983, "B1": 2616, "B4": 1470, "B3": 367, "B5": 34}}; gloss: 11956 items, 1090 calls, verdicts {"NOT_RUN(QuotaError)": 11956}.

## T14. Independent audit (tests/audit_rederive.py; sklearn, no src/ import)

# source: results/audit_rederive.json :: tests/audit_rederive.py main()

Decision re-derived: NONE: V0 stands (match True); best LONG Δ V4 +0.00880 (match 1e-9 True); GG gate numbers match: True; shuffled-label placebo strat AUROCs {"V0": 0.498, "V1": 0.497, "V2": 0.497, "V3": 0.495, "V5": 0.498, "V4": 0.494, "c_gg": 0.506} (ok True).
