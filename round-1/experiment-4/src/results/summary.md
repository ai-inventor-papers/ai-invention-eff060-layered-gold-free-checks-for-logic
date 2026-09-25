# Experiment D — disguised cheap judge + all baselines: results summary

Label vector sha1 `122d01df41fef9b526c93307489e76a7250c23da` · prereg sha1 `ee5e87478f6a63e96bd3a8308c76bdd38cf05404` · API spend $2.0171

**Deviation / freeze context:** the shared OpenRouter key was exhausted 13:29-15:11 UTC; local open-weight judges (judge_local_*, prereg_local.json) were run meanwhile and are kept as secondary rows. This API prereg was frozen at 15:1x UTC on 2026-09-23 after the OpenRouter key was restored. The local-judge path (prereg_local.json, frozen 13:49 UTC) had ALREADY been joined to track-L labels. No API-judge setting was chosen with track-L information: the rubric variant comes from the dev-slice run of 13:29 UTC (results/promptdev_api_preoutage.json, rule 'higher AUROC, tie -> B' gives A), the strong judge from a cost/validity-only dry run on 10 dev-slice items, and the strong subsample, thresholds, feature sets and bootstrap settings are identical to prereg_local.json.

Judges: cheap = `google/gemini-2.5-flash-lite` (JSON 0-100), cheap2 = `openai/gpt-4.1-nano` (P(YES) logprobs), strong = `google/gemini-3.1-pro-preview`.

## L_primary  (n=524, errors=230, correct=294)

| metric | AUROC [95% CI] | AUPRC (prev) | tie rate | FA@thr | recall@thr | coverage |
|---|---|---|---|---|---|---|
| parse_fail | 0.500 [0.500, 0.500] | 0.439 (0.44) | 1.00 | 0.000 | 0.000 | 1.000 |
| pilot_joint_conflict | 0.513 [0.488, 0.539] | 0.447 (0.44) | 0.89 | 0.048 | 0.074 | 1.000 |
| pilot_arity_incons | 0.500 [0.500, 0.500] | 0.439 (0.44) | 1.00 | 0.000 | 0.000 | 1.000 |
| pilot_shape_incons | 0.524 [0.470, 0.578] | 0.468 (0.44) | 0.45 | 0.439 | 0.465 | 1.000 |
| pilot_dangling | 0.533 [0.474, 0.592] | 0.484 (0.44) | 0.28 | 0.122 | 0.187 | 1.000 |
| pilot_undeclared | 0.525 [0.510, 0.542] | 0.469 (0.44) | 0.94 | 0.007 | 0.057 | 1.000 |
| pilot_rerun_jacc | 0.720 [0.659, 0.780] | 0.662 (0.44) | 0.12 | 0.116 | 0.421 | 1.000 |
| rt_nli_min | 0.710 [0.648, 0.769] | 0.711 (0.44) | 0.00 | 0.143 | 0.443 | 1.000 |
| rt_nli_fwd | 0.652 [0.588, 0.713] | 0.653 (0.44) | 0.00 | 0.129 | 0.361 | 1.000 |
| rt_nli_bwd | 0.681 [0.621, 0.742] | 0.677 (0.44) | 0.00 | 0.153 | 0.457 | 1.000 |
| rt_nli_contra | 0.628 [0.566, 0.686] | 0.627 (0.44) | 0.00 | 0.095 | 0.291 | 1.000 |
| rt_nli_min_alt | 0.689 [0.627, 0.749] | 0.676 (0.44) | 0.00 | 0.245 | 0.526 | 1.000 |
| rt_embed_cos | 0.633 [0.574, 0.696] | 0.582 (0.44) | 0.00 | 0.187 | 0.300 | 1.000 |
| rt_reformalise_eq | 0.513 [0.479, 0.547] | 0.446 (0.44) | 0.76 | 0.126 | 0.152 | 0.962 |
| judge_cheap_orig | 0.749 [0.695, 0.801] | 0.682 (0.44) | 0.36 | 0.034 | 0.313 | 0.987 |
| judge_cheap_disg | 0.777 [0.720, 0.827] | 0.674 (0.44) | 0.24 | 0.129 | 0.557 | 0.979 |
| judge_cheap2_orig | 0.750 [0.691, 0.810] | 0.730 (0.44) | 0.00 | 0.153 | 0.561 | 1.000 |
| judge_cheap2_disg | 0.714 [0.648, 0.777] | 0.649 (0.44) | 0.00 | 0.248 | 0.548 | 1.000 |
| judge_strong_orig | 0.802 [0.715, 0.877] | 0.688 (0.34) | 0.16 | 0.174 | 0.632 | 1.000 |
| judge_strong_disg | 0.730 [0.655, 0.803] | 0.505 (0.34) | 0.22 | 0.455 | 0.809 | 1.000 |
| judge_local_qwen8b_orig | 0.755 [0.705, 0.809] | 0.706 (0.44) | 0.30 | 0.024 | 0.317 | 1.000 |
| judge_local_qwen8b_disg | 0.757 [0.702, 0.811] | 0.660 (0.44) | 0.17 | 0.102 | 0.352 | 1.000 |
| judge_local_llama8b_orig | 0.699 [0.633, 0.764] | 0.659 (0.44) | 0.00 | 0.119 | 0.335 | 1.000 |
| judge_local_llama8b_disg | 0.671 [0.604, 0.737] | 0.619 (0.44) | 0.00 | 0.279 | 0.535 | 1.000 |
| judge_local_qwen14b_orig | 0.753 [0.663, 0.834] | 0.623 (0.34) | 0.29 | 0.008 | 0.250 | 1.000 |
| judge_local_qwen14b_disg | 0.760 [0.681, 0.834] | 0.518 (0.34) | 0.12 | 0.167 | 0.500 | 1.000 |
| rt_nli_min_localverb | 0.740 [0.680, 0.796] | 0.736 (0.44) | 0.00 | 0.082 | 0.443 | 1.000 |
| rt_reformalise_eq_localverb | 0.524 [0.471, 0.578] | 0.452 (0.44) | 0.53 | 0.361 | 0.409 | 0.773 |

## L_exclude_subst_only  (n=396, errors=102, correct=294)

| metric | AUROC [95% CI] | AUPRC (prev) | tie rate | FA@thr | recall@thr | coverage |
|---|---|---|---|---|---|---|
| parse_fail | 0.500 [0.500, 0.500] | 0.258 (0.26) | 1.00 | 0.000 | 0.000 | 1.000 |
| pilot_joint_conflict | 0.486 [0.468, 0.508] | 0.255 (0.26) | 0.93 | 0.048 | 0.020 | 1.000 |
| pilot_arity_incons | 0.500 [0.500, 0.500] | 0.258 (0.26) | 1.00 | 0.000 | 0.000 | 1.000 |
| pilot_shape_incons | 0.546 [0.469, 0.621] | 0.310 (0.26) | 0.43 | 0.439 | 0.490 | 1.000 |
| pilot_dangling | 0.537 [0.460, 0.607] | 0.290 (0.26) | 0.27 | 0.122 | 0.176 | 1.000 |
| pilot_undeclared | 0.511 [0.495, 0.535] | 0.270 (0.26) | 0.96 | 0.007 | 0.029 | 1.000 |
| pilot_rerun_jacc | 0.672 [0.590, 0.754] | 0.397 (0.25) | 0.15 | 0.116 | 0.333 | 1.000 |
| rt_nli_min | 0.671 [0.586, 0.757] | 0.509 (0.26) | 0.00 | 0.143 | 0.382 | 1.000 |
| rt_nli_fwd | 0.647 [0.563, 0.737] | 0.502 (0.26) | 0.00 | 0.129 | 0.343 | 1.000 |
| rt_nli_bwd | 0.652 [0.570, 0.736] | 0.465 (0.26) | 0.00 | 0.153 | 0.422 | 1.000 |
| rt_nli_contra | 0.634 [0.551, 0.723] | 0.504 (0.26) | 0.00 | 0.095 | 0.314 | 1.000 |
| rt_nli_min_alt | 0.695 [0.615, 0.772] | 0.524 (0.26) | 0.00 | 0.245 | 0.471 | 1.000 |
| rt_embed_cos | 0.603 [0.525, 0.680] | 0.357 (0.26) | 0.00 | 0.187 | 0.294 | 1.000 |
| rt_reformalise_eq | 0.496 [0.461, 0.537] | 0.256 (0.26) | 0.79 | 0.126 | 0.118 | 0.970 |
| judge_cheap_orig | 0.723 [0.652, 0.794] | 0.499 (0.26) | 0.40 | 0.034 | 0.275 | 0.985 |
| judge_cheap_disg | 0.760 [0.687, 0.830] | 0.472 (0.26) | 0.26 | 0.129 | 0.520 | 0.980 |
| judge_cheap2_orig | 0.740 [0.661, 0.817] | 0.508 (0.26) | 0.00 | 0.153 | 0.500 | 1.000 |
| judge_cheap2_disg | 0.682 [0.600, 0.761] | 0.382 (0.26) | 0.00 | 0.248 | 0.471 | 1.000 |
| judge_strong_orig | 0.721 [0.580, 0.853] | 0.487 (0.20) | 0.21 | 0.174 | 0.515 | 1.000 |
| judge_strong_disg | 0.673 [0.568, 0.787] | 0.285 (0.20) | 0.23 | 0.455 | 0.758 | 1.000 |
| judge_local_qwen8b_orig | 0.731 [0.662, 0.801] | 0.526 (0.26) | 0.33 | 0.024 | 0.265 | 1.000 |
| judge_local_qwen8b_disg | 0.746 [0.678, 0.815] | 0.461 (0.26) | 0.18 | 0.102 | 0.284 | 1.000 |
| judge_local_llama8b_orig | 0.676 [0.591, 0.760] | 0.416 (0.26) | 0.00 | 0.119 | 0.255 | 1.000 |
| judge_local_llama8b_disg | 0.624 [0.542, 0.713] | 0.360 (0.26) | 0.00 | 0.279 | 0.451 | 1.000 |
| judge_local_qwen14b_orig | 0.649 [0.532, 0.762] | 0.328 (0.20) | 0.43 | 0.008 | 0.091 | 1.000 |
| judge_local_qwen14b_disg | 0.696 [0.588, 0.811] | 0.298 (0.20) | 0.15 | 0.167 | 0.364 | 1.000 |
| rt_nli_min_localverb | 0.720 [0.639, 0.801] | 0.544 (0.26) | 0.00 | 0.082 | 0.363 | 1.000 |
| rt_reformalise_eq_localverb | 0.531 [0.470, 0.595] | 0.271 (0.26) | 0.52 | 0.361 | 0.422 | 0.773 |

## H_primary  (n=177, errors=24, correct=153)

| metric | AUROC [95% CI] | AUPRC (prev) | tie rate | FA@thr | recall@thr | coverage |
|---|---|---|---|---|---|---|
| parse_fail | 0.500 [0.500, 0.500] | 0.136 (0.14) | 1.00 | 0.000 | 0.000 | 1.000 |
| pilot_joint_conflict | 0.429 [0.384, 0.487] | 0.131 (0.14) | 0.79 | 0.183 | 0.042 | 1.000 |
| pilot_arity_incons | 0.518 [0.490, 0.565] | 0.151 (0.14) | 0.95 | 0.007 | 0.042 | 1.000 |
| pilot_shape_incons | 0.391 [0.285, 0.513] | 0.121 (0.14) | 0.37 | 0.569 | 0.333 | 1.000 |
| pilot_dangling | 0.672 [0.557, 0.790] | 0.303 (0.13) | 0.35 | 0.021 | 0.190 | 1.000 |
| rt_nli_min | 0.741 [0.633, 0.839] | 0.343 (0.14) | 0.00 | 0.105 | 0.250 | 1.000 |
| rt_nli_fwd | 0.722 [0.594, 0.834] | 0.393 (0.14) | 0.00 | 0.105 | 0.333 | 1.000 |
| rt_nli_bwd | 0.690 [0.563, 0.801] | 0.298 (0.14) | 0.00 | 0.105 | 0.333 | 1.000 |
| rt_nli_contra | 0.704 [0.586, 0.817] | 0.349 (0.14) | 0.00 | 0.105 | 0.292 | 1.000 |
| rt_nli_min_alt | 0.748 [0.624, 0.855] | 0.407 (0.14) | 0.00 | 0.105 | 0.417 | 1.000 |
| rt_embed_cos | 0.682 [0.569, 0.790] | 0.306 (0.14) | 0.01 | 0.105 | 0.333 | 1.000 |
| rt_reformalise_eq | 0.582 [0.489, 0.687] | 0.169 (0.14) | 0.61 | 0.170 | 0.333 | 0.932 |
| judge_cheap_orig | 0.753 [0.632, 0.857] | 0.372 (0.14) | 0.27 | 0.059 | 0.417 | 0.989 |
| judge_cheap_disg | 0.740 [0.632, 0.839] | 0.273 (0.14) | 0.26 | 0.229 | 0.667 | 0.960 |
| judge_cheap2_orig | 0.749 [0.650, 0.840] | 0.371 (0.14) | 0.00 | 0.275 | 0.583 | 1.000 |
| judge_cheap2_disg | 0.635 [0.517, 0.742] | 0.236 (0.14) | 0.00 | 0.425 | 0.583 | 1.000 |
| judge_strong_orig | 0.878 [0.788, 0.954] | 0.793 (0.32) | 0.13 | 0.100 | 0.750 | 1.000 |
| judge_strong_disg | 0.798 [0.687, 0.900] | 0.594 (0.32) | 0.16 | 0.220 | 0.708 | 1.000 |
| judge_local_qwen8b_orig | 0.774 [0.655, 0.874] | 0.390 (0.14) | 0.17 | 0.033 | 0.292 | 1.000 |
| judge_local_qwen8b_disg | 0.731 [0.615, 0.834] | 0.264 (0.14) | 0.12 | 0.111 | 0.458 | 1.000 |
| judge_local_llama8b_orig | 0.670 [0.535, 0.794] | 0.319 (0.14) | 0.00 | 0.144 | 0.542 | 1.000 |
| judge_local_llama8b_disg | 0.664 [0.535, 0.779] | 0.317 (0.14) | 0.00 | 0.412 | 0.625 | 1.000 |
| judge_local_qwen14b_orig | 0.755 [0.646, 0.851] | 0.591 (0.32) | 0.32 | 0.060 | 0.292 | 1.000 |
| judge_local_qwen14b_disg | 0.674 [0.529, 0.801] | 0.464 (0.32) | 0.12 | 0.260 | 0.667 | 1.000 |
| rt_nli_min_localverb | 0.701 [0.583, 0.806] | 0.335 (0.14) | 0.00 | 0.105 | 0.292 | 1.000 |
| rt_reformalise_eq_localverb | 0.533 [0.425, 0.643] | 0.144 (0.14) | 0.51 | 0.392 | 0.458 | 0.802 |

## H_curator_view  (n=199, errors=46, correct=153)

| metric | AUROC [95% CI] | AUPRC (prev) | tie rate | FA@thr | recall@thr | coverage |
|---|---|---|---|---|---|---|
| parse_fail | 0.500 [0.500, 0.500] | 0.231 (0.23) | 1.00 | 0.000 | 0.000 | 1.000 |
| pilot_joint_conflict | 0.419 [0.383, 0.457] | 0.227 (0.23) | 0.80 | 0.183 | 0.022 | 1.000 |
| pilot_arity_incons | 0.518 [0.493, 0.553] | 0.250 (0.23) | 0.95 | 0.007 | 0.043 | 1.000 |
| pilot_shape_incons | 0.398 [0.313, 0.483] | 0.219 (0.23) | 0.36 | 0.569 | 0.326 | 1.000 |
| pilot_dangling | 0.659 [0.566, 0.756] | 0.365 (0.19) | 0.37 | 0.021 | 0.182 | 1.000 |
| rt_nli_min | 0.772 [0.696, 0.845] | 0.485 (0.23) | 0.00 | 0.105 | 0.261 | 1.000 |
| rt_nli_fwd | 0.762 [0.676, 0.841] | 0.532 (0.23) | 0.00 | 0.105 | 0.500 | 1.000 |
| rt_nli_bwd | 0.709 [0.617, 0.791] | 0.436 (0.23) | 0.00 | 0.105 | 0.304 | 1.000 |
| rt_nli_contra | 0.718 [0.634, 0.795] | 0.446 (0.23) | 0.00 | 0.105 | 0.217 | 1.000 |
| rt_nli_min_alt | 0.753 [0.670, 0.830] | 0.521 (0.23) | 0.00 | 0.105 | 0.348 | 1.000 |
| rt_embed_cos | 0.757 [0.678, 0.827] | 0.501 (0.23) | 0.00 | 0.105 | 0.391 | 1.000 |
| rt_reformalise_eq | 0.589 [0.517, 0.668] | 0.283 (0.23) | 0.60 | 0.170 | 0.348 | 0.925 |
| judge_cheap_orig | 0.806 [0.734, 0.872] | 0.528 (0.23) | 0.22 | 0.059 | 0.478 | 0.990 |
| judge_cheap_disg | 0.782 [0.708, 0.849] | 0.450 (0.23) | 0.23 | 0.229 | 0.761 | 0.960 |
| judge_cheap2_orig | 0.790 [0.717, 0.858] | 0.554 (0.23) | 0.00 | 0.275 | 0.674 | 1.000 |
| judge_cheap2_disg | 0.688 [0.608, 0.769] | 0.381 (0.23) | 0.00 | 0.425 | 0.739 | 1.000 |
| judge_strong_orig | 0.915 [0.861, 0.963] | 0.895 (0.48) | 0.09 | 0.100 | 0.804 | 1.000 |
| judge_strong_disg | 0.846 [0.766, 0.920] | 0.773 (0.48) | 0.14 | 0.220 | 0.826 | 1.000 |
| judge_local_qwen8b_orig | 0.816 [0.738, 0.888] | 0.566 (0.23) | 0.13 | 0.033 | 0.283 | 1.000 |
| judge_local_qwen8b_disg | 0.755 [0.673, 0.829] | 0.409 (0.23) | 0.09 | 0.111 | 0.435 | 1.000 |
| judge_local_llama8b_orig | 0.736 [0.645, 0.824] | 0.507 (0.23) | 0.00 | 0.144 | 0.565 | 1.000 |
| judge_local_llama8b_disg | 0.709 [0.621, 0.793] | 0.471 (0.23) | 0.00 | 0.412 | 0.696 | 1.000 |
| judge_local_qwen14b_orig | 0.792 [0.708, 0.865] | 0.742 (0.48) | 0.26 | 0.060 | 0.370 | 1.000 |
| judge_local_qwen14b_disg | 0.727 [0.616, 0.823] | 0.653 (0.48) | 0.11 | 0.260 | 0.717 | 1.000 |
| rt_nli_min_localverb | 0.735 [0.652, 0.813] | 0.460 (0.23) | 0.00 | 0.105 | 0.261 | 1.000 |
| rt_reformalise_eq_localverb | 0.543 [0.461, 0.626] | 0.249 (0.23) | 0.50 | 0.392 | 0.478 | 0.824 |

## The bar for iteration 2

Candidates must beat **judge_cheap_disg AUROC = 0.777 [0.720, 0.827]** and **best_baseline_oof AUROC = 0.817 [0.762, 0.867]** (S4_all_cheap) on track L (CORRECT vs ERROR, n=524), using the fold assignment in data/folds.json.

Cross-fitted combinations (track L): S1_structural: 0.698 [0.634, 0.761]; S2_roundtrip: 0.687 [0.625, 0.749]; S3_judges_disg: 0.771 [0.705, 0.831]; S4_all_cheap: 0.817 [0.762, 0.867]; S6_exploratory_S4_plus_local: 0.810 [0.753, 0.861]

## Contamination

- judge_cheap L_primary: AUROC orig 0.749 → disg 0.777 (Δ +0.029, CI [-0.02369828992643567, 0.08511689987008292])
- judge_cheap H_primary: AUROC orig 0.753 → disg 0.740 (Δ -0.013, CI [-0.13401906625324544, 0.10806943220648595])
- judge_cheap H_curator_view: AUROC orig 0.806 → disg 0.782 (Δ -0.024, CI [-0.0937244068558028, 0.049666098323387316])
- judge_cheap DiD_H_primary_minus_L_primary: DiD = -0.042, CI [-0.17038457841505933, 0.09406198126185984], contamination evidence = False
- judge_cheap DiD_H_curator_view_minus_L_primary: DiD = -0.053, CI [-0.1421514821239283, 0.040190886430923035], contamination evidence = False
- judge_cheap2 L_primary: AUROC orig 0.750 → disg 0.714 (Δ -0.037, CI [-0.09917661322655541, 0.023506811251230525])
- judge_cheap2 H_primary: AUROC orig 0.749 → disg 0.635 (Δ -0.114, CI [-0.20737702384796342, -0.031575951986755064])
- judge_cheap2 H_curator_view: AUROC orig 0.790 → disg 0.688 (Δ -0.102, CI [-0.17587350090743153, -0.032610319787739185])
- judge_cheap2 DiD_H_primary_minus_L_primary: DiD = -0.077, CI [-0.18789415674122745, 0.02328646481292426], contamination evidence = False
- judge_cheap2 DiD_H_curator_view_minus_L_primary: DiD = -0.065, CI [-0.16127128863840914, 0.028408155804871275], contamination evidence = False
- judge_strong L_strong_subset: AUROC orig 0.802 → disg 0.730 (Δ -0.071, CI [-0.14030826416387457, 0.008243044166827418])
- judge_strong H_strong_subset: AUROC orig 0.915 → disg 0.846 (Δ -0.070, CI [-0.14678662800614015, 0.002845874205581595])
- judge_strong DiD_H_strong_subset_minus_L_strong_subset: DiD = +0.002, CI [-0.11473121638515123, 0.10353848340587568], contamination evidence = False
- judge_local_qwen8b L_primary: AUROC orig 0.755 → disg 0.757 (Δ +0.002, CI [-0.05778294292523042, 0.060715283243182566])
- judge_local_qwen8b H_primary: AUROC orig 0.774 → disg 0.731 (Δ -0.043, CI [-0.13980557500778085, 0.0686643685907358])
- judge_local_qwen8b H_curator_view: AUROC orig 0.816 → disg 0.755 (Δ -0.062, CI [-0.13867976955384556, 0.01352595853462817])
- judge_local_qwen8b DiD_H_primary_minus_L_primary: DiD = -0.045, CI [-0.16051716047966536, 0.07908345979339564], contamination evidence = False
- judge_local_qwen8b DiD_H_curator_view_minus_L_primary: DiD = -0.064, CI [-0.16036651943931404, 0.0320147142966988], contamination evidence = False
- judge_local_llama8b L_primary: AUROC orig 0.699 → disg 0.671 (Δ -0.028, CI [-0.09550932755916183, 0.04145196610129224])
- judge_local_llama8b H_primary: AUROC orig 0.670 → disg 0.664 (Δ -0.006, CI [-0.11943672550407285, 0.10623715915455378])
- judge_local_llama8b H_curator_view: AUROC orig 0.736 → disg 0.709 (Δ -0.027, CI [-0.10372337736148476, 0.049283522205833055])
- judge_local_llama8b DiD_H_primary_minus_L_primary: DiD = +0.023, CI [-0.11152263528706434, 0.15650078240548632], contamination evidence = False
- judge_local_llama8b DiD_H_curator_view_minus_L_primary: DiD = +0.001, CI [-0.09946863265287222, 0.10306581350062032], contamination evidence = False
- judge_local_qwen14b L_strong_subset: AUROC orig 0.753 → disg 0.760 (Δ +0.007, CI [-0.07569455436045835, 0.09732451992919315])
- judge_local_qwen14b H_strong_subset: AUROC orig 0.792 → disg 0.727 (Δ -0.065, CI [-0.15501405423280418, 0.029204508628081938])
- judge_local_qwen14b DiD_H_strong_subset_minus_L_strong_subset: DiD = -0.073, CI [-0.1954766263205166, 0.056094465870773255], contamination evidence = False

Gold-recall probe (the primary model translates each track-H sentence from scratch; ALL items):
- probe ≡ ORIGINAL public gold on the 113 items where original ≠ corrected: 0.044; ≡ CORRECTED gold: 0.159
- predicate-name Jaccard(probe, original gold) − Jaccard(probe, Logic-LM gpt-4): {"n": 63, "mean": -0.06838624338624338, "ci": [-0.17050264550264552, 0.03386243386243386]}

## Paired ΔAUROC vs judge_cheap_disg (track L; sentence-cluster bootstrap CI; DeLong p)

| metric | ΔAUROC | 95% CI | DeLong p |
|---|---|---|---|
| parse_fail | -0.277 | [-0.327, -0.220] | 0.000 |
| pilot_joint_conflict | -0.264 | [-0.319, -0.204] | 0.000 |
| pilot_arity_incons | -0.277 | [-0.327, -0.220] | 0.000 |
| pilot_shape_incons | -0.254 | [-0.325, -0.183] | 0.000 |
| pilot_dangling | -0.244 | [-0.325, -0.160] | 0.000 |
| pilot_undeclared | -0.252 | [-0.304, -0.193] | 0.000 |
| pilot_rerun_jacc | -0.058 | [-0.125, 0.011] | 0.037 |
| rt_nli_min | -0.068 | [-0.136, -0.003] | 0.008 |
| rt_nli_fwd | -0.126 | [-0.199, -0.051] | 0.000 |
| rt_nli_bwd | -0.096 | [-0.164, -0.029] | 0.000 |
| rt_nli_contra | -0.150 | [-0.227, -0.075] | 0.000 |
| rt_nli_min_alt | -0.089 | [-0.165, -0.019] | 0.001 |
| rt_embed_cos | -0.144 | [-0.218, -0.070] | 0.000 |
| rt_reformalise_eq | -0.264 | [-0.330, -0.202] | 0.000 |
| judge_cheap_orig | -0.029 | [-0.085, 0.024] | 0.173 |
| judge_cheap2_orig | -0.027 | [-0.091, 0.041] | 0.268 |
| judge_cheap2_disg | -0.064 | [-0.125, -0.002] | 0.009 |
| judge_strong_orig | +0.024 | [-0.075, 0.111] | 0.071 |
| judge_strong_disg | -0.047 | [-0.133, 0.031] | 0.896 |
| judge_local_qwen8b_orig | -0.023 | [-0.079, 0.032] | 0.290 |
| judge_local_qwen8b_disg | -0.021 | [-0.066, 0.025] | 0.263 |
| judge_local_llama8b_orig | -0.078 | [-0.150, -0.012] | 0.002 |
| judge_local_llama8b_disg | -0.107 | [-0.173, -0.038] | 0.000 |
| judge_local_qwen14b_orig | -0.025 | [-0.120, 0.059] | 0.497 |
| judge_local_qwen14b_disg | -0.018 | [-0.089, 0.053] | 0.245 |
| rt_nli_min_localverb | -0.038 | [-0.105, 0.029] | 0.138 |
| rt_reformalise_eq_localverb | -0.253 | [-0.326, -0.176] | 0.000 |

Best combination − judge_cheap_disg: +0.039 [-0.010, 0.087]

## Invariance: false-alarm rate on meaning-preserving rewrites of track-L CORRECT items (FA base → FA rewrite, flip rate)

| metric | RENAME | REORDER | DEMORGAN | CONTRAPOSITIVE | REPRINT (format only) | ALL meaning-preserving |
|---|---|---|---|---|---|---|
| parse_fail | 0.00→0.00 (flip 0.00, n=150) | 0.00→0.00 (flip 0.00, n=41) | 0.00→0.00 (flip 0.00, n=39) | 0.00→0.00 (flip 0.00, n=39) | 0.00→0.00 (flip 0.00, n=12) | 0.00→0.00 (flip 0.00, n=270) |
| pilot_joint_conflict | 0.05→0.01 (flip 0.04, n=150) | 0.05→0.05 (flip 0.00, n=41) | 0.05→0.05 (flip 0.00, n=39) | 0.03→0.03 (flip 0.00, n=39) | 0.08→0.08 (flip 0.00, n=12) | 0.05→0.03 (flip 0.02, n=270) |
| pilot_arity_incons | 0.00→0.00 (flip 0.00, n=150) | 0.00→0.00 (flip 0.00, n=41) | 0.00→0.00 (flip 0.00, n=39) | 0.00→0.00 (flip 0.00, n=39) | 0.00→0.00 (flip 0.00, n=12) | 0.00→0.00 (flip 0.00, n=270) |
| pilot_shape_incons | 0.46→0.00 (flip 0.46, n=150) | 0.41→0.41 (flip 0.00, n=41) | 0.41→0.41 (flip 0.00, n=39) | 0.46→0.46 (flip 0.00, n=39) | 0.33→0.33 (flip 0.00, n=12) | 0.45→0.19 (flip 0.26, n=270) |
| pilot_dangling | 0.13→1.00 (flip 0.87, n=150) | 0.15→0.15 (flip 0.00, n=41) | 0.15→0.15 (flip 0.00, n=39) | 0.08→0.08 (flip 0.00, n=39) | 0.08→0.08 (flip 0.00, n=12) | 0.13→0.61 (flip 0.49, n=270) |
| pilot_undeclared | 0.01→1.00 (flip 0.99, n=150) | 0.02→0.02 (flip 0.00, n=41) | 0.03→0.03 (flip 0.00, n=39) | 0.03→0.03 (flip 0.00, n=39) | 0.08→0.08 (flip 0.00, n=12) | 0.01→0.57 (flip 0.55, n=270) |
| pilot_rerun_jacc | 0.12→0.87 (flip 0.78, n=143) | 0.29→0.29 (flip 0.00, n=38) | 0.31→0.31 (flip 0.00, n=36) | 0.16→0.16 (flip 0.00, n=37) | 0.20→0.20 (flip 0.00, n=10) | 0.18→0.60 (flip 0.44, n=255) |
| rt_nli_min | 0.15→0.41 (flip 0.37, n=150) | 0.10→0.15 (flip 0.10, n=41) | 0.10→0.31 (flip 0.31, n=39) | 0.26→0.38 (flip 0.33, n=39) | 0.08→0.08 (flip 0.00, n=12) | 0.15→0.35 (flip 0.31, n=270) |
| rt_nli_fwd | 0.15→0.64 (flip 0.52, n=150) | 0.12→0.17 (flip 0.05, n=41) | 0.10→0.59 (flip 0.49, n=39) | 0.36→0.95 (flip 0.59, n=39) | 0.33→0.42 (flip 0.08, n=12) | 0.17→0.60 (flip 0.45, n=270) |
| rt_nli_bwd | 0.15→0.41 (flip 0.29, n=150) | 0.10→0.17 (flip 0.12, n=41) | 0.10→0.31 (flip 0.31, n=39) | 0.31→0.36 (flip 0.31, n=39) | 0.08→0.08 (flip 0.00, n=12) | 0.16→0.35 (flip 0.27, n=270) |
| rt_nli_contra | 0.08→0.58 (flip 0.54, n=150) | 0.10→0.00 (flip 0.10, n=41) | 0.08→0.38 (flip 0.36, n=39) | 0.15→0.36 (flip 0.26, n=39) | 0.25→0.08 (flip 0.17, n=12) | 0.09→0.43 (flip 0.40, n=270) |
| rt_nli_min_alt | 0.25→0.51 (flip 0.40, n=150) | 0.29→0.34 (flip 0.15, n=41) | 0.28→0.67 (flip 0.38, n=39) | 0.23→0.51 (flip 0.44, n=39) | 0.50→0.50 (flip 0.17, n=12) | 0.26→0.51 (flip 0.36, n=270) |
| rt_embed_cos | 0.17→0.73 (flip 0.57, n=150) | 0.32→0.34 (flip 0.07, n=41) | 0.31→0.74 (flip 0.44, n=39) | 0.18→0.51 (flip 0.38, n=39) | 0.50→0.58 (flip 0.08, n=12) | 0.22→0.64 (flip 0.44, n=270) |
| rt_reformalise_eq | 0.11→0.23 (flip 0.19, n=150) | 0.07→0.05 (flip 0.07, n=41) | 0.08→0.10 (flip 0.13, n=39) | 0.08→0.03 (flip 0.05, n=39) | 0.08→0.00 (flip 0.08, n=12) | 0.10→0.15 (flip 0.14, n=270) |
| judge_cheap_orig | 0.04→0.27 (flip 0.27, n=150) | 0.05→0.07 (flip 0.12, n=41) | 0.05→0.18 (flip 0.23, n=39) | 0.03→0.67 (flip 0.64, n=39) | 0.17→0.17 (flip 0.00, n=12) | 0.04→0.28 (flip 0.29, n=270) |
| judge_cheap_disg | 0.13→0.55 (flip 0.44, n=150) | 0.10→0.17 (flip 0.12, n=41) | 0.10→0.56 (flip 0.46, n=39) | 0.10→0.51 (flip 0.41, n=39) | 0.08→0.08 (flip 0.17, n=12) | 0.12→0.49 (flip 0.39, n=270) |
| judge_cheap2_orig | 0.19→0.65 (flip 0.49, n=150) | 0.17→0.20 (flip 0.12, n=41) | 0.18→0.44 (flip 0.46, n=39) | 0.03→0.97 (flip 0.95, n=39) | 0.08→0.25 (flip 0.17, n=12) | 0.16→0.60 (flip 0.49, n=270) |
| judge_cheap2_disg | 0.31→0.76 (flip 0.49, n=150) | 0.24→0.37 (flip 0.32, n=41) | 0.26→0.38 (flip 0.44, n=39) | 0.18→0.77 (flip 0.69, n=39) | 0.17→0.33 (flip 0.17, n=12) | 0.27→0.64 (flip 0.49, n=270) |
| judge_local_qwen8b_orig | 0.03→0.42 (flip 0.39, n=150) | 0.00→0.02 (flip 0.02, n=41) | 0.00→0.46 (flip 0.46, n=39) | 0.00→0.59 (flip 0.59, n=39) | 0.00→0.00 (flip 0.00, n=12) | 0.01→0.39 (flip 0.37, n=270) |
| judge_local_qwen8b_disg | 0.13→0.73 (flip 0.59, n=150) | 0.00→0.00 (flip 0.00, n=41) | 0.00→0.23 (flip 0.23, n=39) | 0.03→0.26 (flip 0.23, n=39) | 0.00→0.08 (flip 0.08, n=12) | 0.08→0.47 (flip 0.40, n=270) |
| judge_local_llama8b_orig | 0.11→0.40 (flip 0.31, n=150) | 0.05→0.17 (flip 0.17, n=41) | 0.05→0.46 (flip 0.41, n=39) | 0.05→0.95 (flip 0.90, n=39) | 0.17→0.17 (flip 0.00, n=12) | 0.09→0.45 (flip 0.39, n=270) |
| judge_local_llama8b_disg | 0.28→0.69 (flip 0.41, n=150) | 0.22→0.41 (flip 0.20, n=41) | 0.21→0.44 (flip 0.33, n=39) | 0.08→0.77 (flip 0.69, n=39) | 0.17→0.25 (flip 0.08, n=12) | 0.23→0.63 (flip 0.41, n=270) |
| rt_nli_min_localverb | 0.09→0.40 (flip 0.36, n=150) | 0.05→0.02 (flip 0.02, n=41) | 0.05→0.18 (flip 0.23, n=39) | 0.13→0.26 (flip 0.28, n=39) | 0.00→0.00 (flip 0.00, n=12) | 0.09→0.29 (flip 0.28, n=270) |
| rt_reformalise_eq_localverb | 0.36→0.45 (flip 0.27, n=150) | 0.41→0.37 (flip 0.15, n=41) | 0.44→0.10 (flip 0.44, n=39) | 0.10→0.10 (flip 0.10, n=39) | 0.17→0.17 (flip 0.00, n=12) | 0.34→0.34 (flip 0.25, n=270) |

## Per-error-type sensitivity at the pre-registered threshold (track-H curator view errors)

| group | n | judge_cheap_orig | judge_cheap_disg | judge_cheap2_orig | rt_nli_min | rt_reformalise_eq | pilot_joint_conflict |
|---|---|---|---|---|---|---|---|
| 1-op | 13 | 0.308 | 0.538 | 0.462 | 0.231 | 0.308 | 0.000 |
| 2-op | 11 | 0.545 | 0.818 | 0.727 | 0.273 | 0.364 | 0.091 |
| ADD | 12 | 0.500 | 0.750 | 0.667 | 0.250 | 0.417 | 0.083 |
| BIND | 1 | 0.000 | 1.000 | 0.000 | 1.000 | 1.000 | 0.000 |
| COMPOUND | 22 | 0.545 | 0.864 | 0.773 | 0.273 | 0.364 | 0.000 |
| CONN | 3 | 0.667 | 0.667 | 1.000 | 0.333 | 0.333 | 0.000 |
| DROP | 11 | 0.455 | 0.636 | 0.455 | 0.182 | 0.273 | 0.091 |
| NEG | 2 | 0.500 | 0.500 | 1.000 | 0.500 | 0.000 | 0.000 |
| RESTR | 1 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |
| REV | 1 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| SWAP | 2 | 0.000 | 1.000 | 0.500 | 0.000 | 0.000 | 0.000 |
| UNGLUE | 2 | 0.500 | 1.000 | 1.000 | 0.500 | 0.000 | 0.000 |

Judge error-type label accuracy (type ∈ census ops): track H {"1-op": {"correct": 0, "n": 12, "acc": 0.0}, "2-op": {"correct": 5, "n": 11, "acc": 0.45454545454545453}}; track L {"1-op": {"correct": 18, "n": 89, "acc": 0.20224719101123595}, "2-op": {"correct": 37, "n": 139, "acc": 0.26618705035971224}}

## Reliability vs sentence complexity (L_primary; cells with <50 per class are descriptive only)

| stratum | n (err/cor) | testable | judge_cheap_disg AUROC | judge_cheap_orig AUROC | rt_nli_min AUROC | judge_cheap_disg FA |
|---|---|---|---|---|---|---|
| words_bin=12-19 | 36 (18/18) | False | 0.667 | 0.593 | 0.670 | 0.278 |
| words_bin=<12 | 485 (210/275) | True | 0.784 | 0.759 | 0.713 | 0.116 |
| words_bin=>=20 | 3 (2/1) | False | 0.000 | 1.000 | 1.000 | 1.000 |
| n_quant_bin=0-1 | 512 (226/286) | True | 0.784 | 0.749 | 0.712 | 0.129 |
| n_quant_bin=2 | 11 (4/7) | False | 0.429 | 0.714 | 0.571 | 0.000 |
| n_quant_bin=>=3 | 1 (0/1) | False | — | — | — | 1.000 |
| depth_bin=4-5 | 54 (30/24) | False | 0.762 | 0.613 | 0.828 | 0.125 |
| depth_bin=<=3 | 466 (199/267) | True | 0.781 | 0.764 | 0.702 | 0.127 |
| depth_bin=>=6 | 4 (1/3) | False | 0.333 | 0.667 | 0.333 | 0.333 |
| n_cond_bin=0 | 394 (182/212) | True | 0.783 | 0.781 | 0.745 | 0.127 |
| n_cond_bin=1-2 | 128 (48/80) | False | 0.765 | 0.644 | 0.653 | 0.138 |
| n_cond_bin=>=3 | 2 (0/2) | False | — | — | — | 0.000 |
| exception=False | 524 (230/294) | True | 0.777 | 0.749 | 0.710 | 0.129 |

Logistic slope (judge_cheap_disg correct ~ z(words) + label): {"coef_z_words": -0.48020416971018964, "se": 0.11116128435521769, "p": 1.561092283816229e-05, "coef_label": -1.4789192208574307}

## Reliability vs sentence complexity (H_curator_view; cells with <50 per class are descriptive only)

| stratum | n (err/cor) | testable | judge_cheap_disg AUROC | judge_cheap_orig AUROC | rt_nli_min AUROC | judge_cheap_disg FA |
|---|---|---|---|---|---|---|
| words_bin=12-19 | 37 (14/23) | False | 0.865 | 0.786 | 0.736 | 0.174 |
| words_bin=<12 | 146 (22/124) | False | 0.713 | 0.778 | 0.759 | 0.210 |
| words_bin=>=20 | 16 (10/6) | False | 0.625 | 0.533 | 0.617 | 0.833 |
| n_quant_bin=0-1 | 186 (36/150) | False | 0.755 | 0.814 | 0.754 | 0.227 |
| n_quant_bin=2 | 10 (7/3) | False | 0.810 | 0.595 | 0.952 | 0.333 |
| n_quant_bin=>=3 | 3 (3/0) | False | — | — | — | — |
| depth_bin=4-5 | 47 (16/31) | False | 0.683 | 0.787 | 0.766 | 0.387 |
| depth_bin=<=3 | 138 (20/118) | False | 0.753 | 0.807 | 0.742 | 0.186 |
| depth_bin=>=6 | 14 (10/4) | False | 0.863 | 0.725 | 0.750 | 0.250 |
| n_cond_bin=0 | 146 (27/119) | False | 0.731 | 0.788 | 0.807 | 0.210 |
| n_cond_bin=1-2 | 41 (12/29) | False | 0.815 | 0.773 | 0.532 | 0.345 |
| n_cond_bin=>=3 | 12 (7/5) | False | 1.000 | 0.886 | 0.714 | 0.000 |
| exception=False | 197 (44/153) | False | 0.783 | 0.803 | 0.778 | 0.229 |
| exception=True | 2 (2/0) | False | — | — | — | — |

Logistic slope (judge_cheap_disg correct ~ z(words) + label): {"coef_z_words": -0.1398023635095974, "se": 0.17056641861481808, "p": 0.41242369000234924, "coef_label": 0.07197364124042346}

## System level (3 Logic-LM systems; descriptive only)

| system | true error rate (CORRECT vs ERROR) | judge_cheap_disg flag rate | rt_nli_min mean | parse-fail |
|---|---|---|---|---|
| gpt-3.5-turbo | 0.415 | 0.444 | 0.516 | 26/248 |
| gpt-4 | 0.385 | 0.362 | 0.496 | 10/282 |
| text-davinci-003 | 0.527 | 0.553 | 0.663 | 20/266 |

## Cost per item

```
{
 "judge_cheap (API, per condition)": {
  "usd_per_call": 3.973874289772727e-05,
  "seconds_per_call": 0.5990205965909091,
  "n_calls": 2816
 },
 "judge_cheap2 (API, per condition)": {
  "usd_per_call": 1.4056130690161527e-05,
  "seconds_per_call": 0.968648678414097,
  "n_calls": 2724
 },
 "judge_strong (API, per condition)": {
  "usd_per_call": 0.0028561202749140895,
  "seconds_per_call": 4.674072164948454,
  "n_calls": 582
 },
 "verbalise+reformalise calls (API, per call)": {
  "usd_per_call": 1.4933910799852562e-05,
  "seconds_per_call": 0.5704113527460376,
  "n_calls": 2713
 },
 "gold_recall_probe (API, per call)": {
  "usd_per_call": 1.6731292517006802e-05,
  "seconds_per_call": 0.6199353741496599,
  "n_calls": 294
 },
 "rt_nli_* (API verbalise + local NLI)": {
  "usd_per_item": 1.2922626849753131e-05
 },
 "rt_embed_cos (API verbalise + local embed)": {
  "usd_per_item": 1.2668752643380074e-05
 },
 "rt_reformalise_eq (API verbalise + reformalise + z3)": {
  "usd_per_item": 2.8706341107871725e-05
 },
 "judge_local_qwen8b (local GPU, per condition)": {
  "gpu_seconds_per_item": 0.4174773989000925,
  "usd_equiv_per_item": 3.015114547611779e-05
 },
 "judge_local_llama8b (local GPU, per condition)": {
  "gpu_seconds_per_item": 0.07407202469537974,
  "usd_equiv_per_item": 5.349646227999648e-06
 },
 "judge_local_qwen14b (local GPU, per condition)": {
  "gpu_seconds_per_item": 0.6431233804874323,
  "usd_equiv_per_item": 4.644779970187011e-05
 },
 "pilot_* (z3, CPU)": {
  "cpu_seconds_per_item": 0.006645881447267129,
  "usd_per_item": 0.0
 },
 "parse_fail": {
  "cpu_seconds_per_item": 0.001,
  "usd_per_item": 0.0
 },
 "_api_spend_total_usd": 2.01711495,
 "_api_spend_by_component": {
  "prompt_dev": 0.0067508,
  "strong_dryrun": 0.15247425,
  "judge_cheap_primary": 0.1119043,
  "judge_cheap_secondary": 0.0382889,
  "roundtrip": 0.0405157,
  "gold_recall_probe": 0.004919,
  "strong": 1.662262
 },
 "_gpu_usd_per_hour": 0.26
}
```

## Label quality

```
{
 "track_H_original_gold_vs_corrected": {
  "n": 294,
  "auto_class": {
   "EQUIV": 181,
   "ERROR": 42,
   "COMPOUND": 33,
   "UNPARSEABLE": 17,
   "VOCAB": 20,
   "GRAN": 1
  },
  "label": {
   "CORRECT": 202,
   "ERROR": 35,
   "UNCERTAIN": 22,
   "READING_CHOICE": 18,
   "UNPARSEABLE": 17
  },
  "orig_gold_wrong_rate_(ERROR+UNCERTAIN+READING_CHOICE)/parseable": 0.27075812274368233,
  "orig_gold_unparseable_rate": 0.05782312925170068,
  "correct_but_not_equivalent_rate_(VOCAB/GRAN among non-EQUIV parseable)": 0.21875
 },
 "track_L_logiclm": {
  "n": 796,
  "auto_class": {
   "EQUIV": 155,
   "ERROR": 230,
   "VOCAB": 122,
   "UNPARSEABLE": 56,
   "COMPOUND": 216,
   "GRAN": 17
  },
  "vocab_or_gran_share_of_CORRECT": 0.47278911564625853,
  "vocab_borderline_share_of_CORRECT": 0.14285714285714285,
  "subst_only_share_of_ERROR": 0.5565217391304348,
  "uncertain_share_of_parseable": 0.2918918918918919
 },
 "note": "subst_only ERROR = the only typed repair is ADD+DROP of an unaligned predicate, i.e. most likely a vocabulary mismatch the aligner missed (correct-but-not-equivalent). The parallel run run_qY2a2IS-WLIs measured 43.9% of solver-non-equivalent candidates judged faithful by a 3-family panel; iteration 2 re-scores with the adjudicated labels of dataset artifact E."
}
```

## Diagnostics

```
{
 "pilot_joint_conflict_by_folio_answer_L_primary": {
  "False": {
   "n": 50,
   "n_pos": 32,
   "auroc": 0.5121527777777778,
   "flag_rate_correct": 0.4444444444444444,
   "flag_rate_error": 0.46875
  },
  "None": {
   "n": 9,
   "n_pos": 1,
   "auroc": 0.5,
   "flag_rate_correct": 0.0,
   "flag_rate_error": 0.0
  },
  "True": {
   "n": 53,
   "n_pos": 17,
   "auroc": 0.4722222222222222,
   "flag_rate_correct": 0.05555555555555555,
   "flag_rate_error": 0.0
  },
  "Uncertain": {
   "n": 100,
   "n_pos": 43,
   "auroc": 0.514483884128927,
   "flag_rate_correct": 0.017543859649122806,
   "flag_rate_error": 0.046511627906976744
  }
 },
 "pilot_joint_conflict_by_folio_answer_H_curator_view": {
  "False": {
   "n": 46,
   "n_pos": 9,
   "auroc": 0.24474474474474475,
   "flag_rate_correct": 0.6216216216216216,
   "flag_rate_error": 0.1111111111111111
  },
  "None": {
   "n": 6,
   "n_pos": 0,
   "auroc": null,
   "flag_rate_correct": 0.0,
   "flag_rate_error": null
  },
  "True": {
   "n": 60,
   "n_pos": 12,
   "auroc": 0.46875,
   "flag_rate_correct": 0.0625,
   "flag_rate_error": 0.0
  },
  "Uncertain": {
   "n": 65,
   "n_pos": 12,
   "auroc": 0.4811320754716981,
   "flag_rate_correct": 0.03773584905660377,
   "flag_rate_error": 0.0
  }
 },
 "T7_gold_roundtrip_reformalise_equiv_rate": {
  "n": 181,
  "rate": 0.856353591160221,
  "n_fail": 11
 }
}
```
