# Dataset E results (PEER+TEXT, frozen on the screen; prereg sha256 b9f28b1bf6bf)

## (a) Item-level AUROC [95% sentence-cluster bootstrap CI], identical rows per table

| subset | n (err/cor) | PEER+TEXT | TEXT | PEER (ALIGN g) | c_score_align | NF c_score | NF g | L2-bow | L3 |
|---|---|---|---|---|---|---|---|---|---|
| R_AB pooled | 2686 (1822/864) | 0.790 [0.75, 0.82] | 0.693 [0.65, 0.73] | 0.748 [0.71, 0.79] | 0.782 [0.74, 0.82] | 0.743 [0.70, 0.78] | 0.742 [0.70, 0.78] | 0.734 [0.71, 0.76] | 0.579 [0.53, 0.62] |
| R_AB L25 | 873 (697/176) | 0.755 [0.70, 0.80] | 0.691 [0.63, 0.74] | 0.676 [0.61, 0.73] | 0.712 [0.65, 0.77] | 0.651 [0.59, 0.71] | 0.650 [0.58, 0.71] | 0.722 [0.67, 0.77] | 0.560 [0.49, 0.63] |
| R_AB L20 | 821 (592/229) | 0.747 [0.69, 0.80] | 0.683 [0.63, 0.74] | 0.636 [0.56, 0.70] | 0.722 [0.66, 0.78] | 0.643 [0.58, 0.70] | 0.631 [0.56, 0.70] | 0.715 [0.66, 0.76] | 0.547 [0.48, 0.62] |
| R_AB EXC | 606 (384/222) | 0.777 [0.72, 0.83] | 0.666 [0.60, 0.73] | 0.782 [0.71, 0.84] | 0.814 [0.76, 0.86] | 0.782 [0.72, 0.84] | 0.787 [0.72, 0.84] | 0.669 [0.61, 0.72] | 0.620 [0.55, 0.69] |
| R_AB CTRL | 386 (149/237) | 0.708 [0.57, 0.84] | 0.559 [0.43, 0.70] | 0.769 [0.64, 0.88] | 0.742 [0.62, 0.86] | 0.741 [0.61, 0.86] | 0.759 [0.63, 0.87] | 0.613 [0.54, 0.72] | 0.490 [0.37, 0.62] |
| R_AB long (L25+L20+EXC) | 2300 (1673/627) | 0.768 [0.74, 0.80] | 0.690 [0.65, 0.72] | 0.705 [0.66, 0.74] | 0.759 [0.72, 0.79] | 0.704 [0.67, 0.74] | 0.697 [0.65, 0.73] | 0.717 [0.69, 0.75] | 0.580 [0.54, 0.62] |
| R_A pooled L20+EXC | 449 (261/188) | 0.818 [0.73, 0.88] | 0.665 [0.57, 0.74] | 0.812 [0.73, 0.88] | 0.860 [0.79, 0.92] | 0.802 [0.72, 0.87] | 0.799 [0.72, 0.86] | 0.678 [0.61, 0.74] | 0.587 [0.51, 0.66] |
| R_A L20 | 196 (132/64) | 0.747 [0.63, 0.84] | 0.594 [0.50, 0.68] | 0.732 [0.60, 0.85] | 0.773 [0.64, 0.87] | 0.688 [0.56, 0.80] | 0.710 [0.58, 0.83] | 0.665 [0.58, 0.75] | 0.461 [0.37, 0.56] |
| R_A EXC | 253 (129/124) | 0.858 [0.75, 0.94] | 0.687 [0.58, 0.78] | 0.852 [0.76, 0.92] | 0.898 [0.81, 0.97] | 0.852 [0.77, 0.92] | 0.846 [0.76, 0.91] | 0.656 [0.57, 0.74] | 0.656 [0.55, 0.75] |
| R_A all strata (sign only) | 867 (453/414) | 0.798 [0.72, 0.87] | 0.647 [0.56, 0.72] | 0.837 [0.77, 0.89] | 0.825 [0.75, 0.89] | 0.809 [0.74, 0.87] | 0.830 [0.76, 0.88] | 0.693 [0.64, 0.75] | 0.551 [0.47, 0.63] |
| R_A L25 (sign only) | 138 (98/40) | 0.790 [0.67, 0.89] | 0.626 [0.51, 0.74] | 0.823 [0.71, 0.91] | 0.783 [0.66, 0.88] | 0.735 [0.60, 0.84] | 0.774 [0.65, 0.87] | 0.727 [0.60, 0.84] | 0.423 [0.29, 0.57] |
| R_A CTRL (sign only) | 280 (94/186) | 0.692 [0.50, 0.88] | 0.496 [0.35, 0.67] | 0.826 [0.64, 0.97] | 0.777 [0.59, 0.93] | 0.805 [0.62, 0.95] | 0.827 [0.65, 0.96] | 0.521 [0.50, 0.56] | 0.482 [0.33, 0.65] |

## (a) Paired ΔAUROC vs the judges (rows where the judge score exists)

| subset | judge | n (err/cor) | judge AUROC | Δ PEER+TEXT − judge [CI] | Δ TEXT − judge [CI] | DeLong p |
|---|---|---|---|---|---|---|
| R_AB pooled | judge_local_qwen8b_disg | 2686 (1822/864) | 0.712 | 0.078 [0.043, 0.112] | -0.019 [-0.065, 0.028] | 0.0000 |
| R_AB pooled | judge_cheap_disg | 20 (8/12) | 0.750 | 0.057 [-0.200, 0.360] | -0.047 [-0.324, 0.272] | 0.6195 |
| R_AB L25 | judge_local_qwen8b_disg | 873 (697/176) | 0.664 | 0.092 [0.031, 0.151] | 0.027 [-0.036, 0.088] | 0.0004 |
| R_AB L25 | judge_cheap_disg | 0 | untestable | | | |
| R_AB L20 | judge_local_qwen8b_disg | 821 (592/229) | 0.683 | 0.064 [-0.001, 0.129] | -0.000 [-0.072, 0.073] | 0.0046 |
| R_AB L20 | judge_cheap_disg | 0 | untestable | | | |
| R_AB EXC | judge_local_qwen8b_disg | 606 (384/222) | 0.663 | 0.114 [0.033, 0.194] | 0.004 [-0.088, 0.095] | 0.0000 |
| R_AB EXC | judge_cheap_disg | 0 | untestable | | | |
| R_AB CTRL | judge_local_qwen8b_disg | 386 (149/237) | 0.739 | -0.031 [-0.142, 0.089] | -0.180 [-0.331, -0.022] | 0.1890 |
| R_AB CTRL | judge_cheap_disg | 20 (8/12) | 0.750 | 0.057 [-0.200, 0.360] | -0.047 [-0.324, 0.272] | 0.6195 |
| R_AB long (L25+L20+EXC) | judge_local_qwen8b_disg | 2300 (1673/627) | 0.653 | 0.115 [0.075, 0.157] | 0.036 [-0.007, 0.083] | 0.0000 |
| R_AB long (L25+L20+EXC) | judge_cheap_disg | 0 | untestable | | | |
| R_A pooled L20+EXC | judge_local_qwen8b_disg | 449 (261/188) | 0.554 | 0.264 [0.157, 0.359] | 0.110 [-0.006, 0.216] | 0.0000 |
| R_A pooled L20+EXC | judge_cheap_disg | 0 | untestable | | | |
| R_A L20 | judge_local_qwen8b_disg | 196 (132/64) | 0.544 | 0.203 [0.024, 0.357] | 0.050 [-0.094, 0.180] | 0.0002 |
| R_A L20 | judge_cheap_disg | 0 | untestable | | | |
| R_A EXC | judge_local_qwen8b_disg | 253 (129/124) | 0.647 | 0.210 [0.075, 0.335] | 0.039 [-0.107, 0.183] | 0.0000 |
| R_A EXC | judge_cheap_disg | 0 | untestable | | | |
| R_A all strata (sign only) | judge_local_qwen8b_disg | 867 (453/414) | 0.669 | 0.129 [0.061, 0.203] | -0.023 [-0.114, 0.075] | 0.0000 |
| R_A all strata (sign only) | judge_cheap_disg | 15 | untestable | | | |
| R_A L25 (sign only) | judge_local_qwen8b_disg | 138 (98/40) | 0.560 | 0.230 [0.119, 0.365] | 0.066 [-0.064, 0.203] | 0.0000 |
| R_A L25 (sign only) | judge_cheap_disg | 0 | untestable | | | |
| R_A CTRL (sign only) | judge_local_qwen8b_disg | 280 (94/186) | 0.697 | -0.005 [-0.185, 0.191] | -0.200 [-0.427, 0.019] | 0.8771 |
| R_A CTRL (sign only) | judge_cheap_disg | 15 | untestable | | | |

## (a') Stratified AUROC (within-stratum pairs only; removes the stratum-composition confound) [B=1000 CI]

| subset | n | PEER+TEXT | TEXT | PEER | c_score_align | NF c_score | local judge | Δ PEER+TEXT − judge [CI] | Δ PEER+TEXT − c_score_align [CI] |
|---|---|---|---|---|---|---|---|---|---|
| R_AB pooled | 2686 | 0.753 | 0.670 | 0.694 | 0.741 | 0.686 | 0.677 | 0.075 [0.036, 0.114] | 0.011 [-0.012, 0.038] |
| R_AB long (L25+L20+EXC) | 2300 | 0.757 | 0.682 | 0.686 | 0.741 | 0.680 | 0.671 | 0.086 [0.049, 0.126] | 0.016 [-0.010, 0.041] |
| R_A pooled L20+EXC | 449 | 0.819 | 0.655 | 0.811 | 0.855 | 0.795 | 0.612 | 0.208 [0.105, 0.305] | -0.036 [-0.113, 0.030] |

Placebos: within-stratum label permutation {"p_peer_text": 0.59, "p_text": 0.552, "peer_only": 0.58, "c_score_align": 0.592} (composition part of pooled AUROC); global shuffle {"p_peer_text": 0.5, "p_text": 0.501, "peer_only": 0.501, "judge_local_qwen8b_disg": 0.5}

## Criteria
```
{
 "judge_cheap_disg": {
  "testable_pooled_R_AB (>=300/class)": false,
  "a_R_AB_CI_gt_0": false,
  "a_R_A_sign_gt_0": false,
  "criterion_a_this_artifact": false,
  "criterion_c_long_CI_gt_0": false
 },
 "judge_local_qwen8b_disg": {
  "testable_pooled_R_AB (>=300/class)": true,
  "a_R_AB_CI_gt_0": true,
  "a_R_A_sign_gt_0": true,
  "criterion_a_this_artifact": true,
  "criterion_c_long_CI_gt_0": true
 }
}
```

## P-tests
- **P1 R_AB**: INCONCLUSIVE
- **P1 R_A**: INCONCLUSIVE
- **P2**: REFUTED
- **P3**: INCONCLUSIVE
- **P4**: REFUTED

### P1 recall by error group at matched FA 0.10 (R_AB; fractional tie-breaking = exact FA; deterministic thresholds are degenerate for tied scores)

| group | n | PEER | TEXT | PEER+TEXT | c_score_align | local judge | PEER−TEXT [CI] |
|---|---|---|---|---|---|---|---|
| COVERAGE | 246 | 0.213 | 0.120 | 0.260 | 0.258 | 0.145 | 0.093 [0.046, 0.147] |
| PEER_ENDORSED_NF | 340 | 0.032 | 0.136 | 0.115 | 0.045 | 0.199 | -0.103 [-0.171, -0.051] |
| MEANING_RENAME | 221 | 0.084 | 0.118 | 0.100 | 0.059 | 0.181 | -0.034 [-0.142, 0.043] |
| PEER_ENDORSED | 398 | 0.059 | 0.089 | 0.058 | 0.000 | 0.169 | -0.030 [-0.090, 0.021] |
| STRUCT | 36 | 0.125 | 0.177 | 0.250 | 0.255 | 0.290 | -0.052 [-0.258, 0.110] |

### P2: Spearman(PEER, TEXT) among errors = 0.294 [0.224, 0.365]; gain over best single (peer_only) = 0.042; share from peer-endorsed = -0.200

### P3: complexity interaction z(score)·z(words) (logistic, cluster bootstrap)
- c_score_align: 0.008 [-0.247, 0.231]
- g_score: -0.131 [-0.316, 0.050]
- nf_c_score: -0.029 [-0.238, 0.218]
- nf_g_score: -0.159 [-0.331, 0.017]
- p_peer_text: -0.023 [-0.228, 0.185]
- p_text: 0.027 [-0.160, 0.211]
- judge_local_qwen8b_disg: -0.154 [-0.511, 0.151]
- diff-in-Δ (long − CTRL) of PEER+TEXT − local judge: 0.146 [0.020, 0.269]

### P4: rewrite false alarms on CORRECT bases (screen pools)

| family | n | fused | g_score | c_score_align | nf_g | l2_bow | l3_z3 | judge_cheap_disg | judge_local_qwen8b_disg |
|---|---|---|---|---|---|---|---|---|---|
| CONTRAPOSITIVE | 28 | 0.107 | 0.214 | 0.063 | 0.237 | 0.075 | 0.188 | 0.407 | 0.214 |
| RENAME | 104 | 0.385 | 0.594 | 0.859 | 0.074 | 0.216 | 0.168 | 0.485 | 0.683 |
| REORDER | 27 | 0.222 | 0.063 | 0.178 | 0.037 | 0.044 | 0.444 | 0.154 | 0.000 |
| DEMORGAN | 26 | 0.154 | 0.066 | 0.185 | 0.038 | 0.046 | 0.231 | 0.520 | 0.231 |
| REPRINT | 8 | 0.375 | 0.214 | 0.220 | 0.125 | 0.138 | 0.500 | 0.000 | 0.125 |
| PRENEX | 1 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 |

Probe recall (synthetic, descriptive): {"ROLE_PERMUTE": {"g_score": 0.703, "c_score_align": 1.0, "nf_g": 0.771, "l2_bow": 0.062, "l3_z3": 0.705, "fused": 1.0}, "MEANING_RENAME": {"g_score": 0.622, "c_score_align": 0.987, "nf_g": 0.145, "l2_bow": 0.98, "l3_z3": 0.85, "fused": 0.987}, "SWAP": {"g_score": 0.637, "c_score_align": 0.973, "nf_g": 0.665, "l2_bow": 0.125, "l3_z3": 0.666, "fused": 0.887}}

### (f) Error typing on R_A errors with 1-2 ops (n=453): top-code accuracy 0.371 (codable-only 0.561, n=262); chance 0.382; medoid_ops exact 0.362; judge types {"judge_local_qwen8b_disg_type": {"n": 453, "acc": 0.02207505518763797}, "judge_cheap_disg_type": {"n": 4, "acc": 0.0}}

### (g) System level (13 system × variant rows, descriptive): Kendall τ-b vs R_AB error rate: p_peer_text 0.718 [0.590, 0.846], p_text 0.769 [0.590, 0.846], peer_only 0.692 [0.538, 0.795], judge_local_qwen8b_disg 0.667 [0.513, 0.783], judge_cheap_disg 0.125 [-0.161, 0.628]

### (i) Contamination
```
{
 "judge_local_qwen8b": {
  "n": 2686,
  "auroc_orig": {
   "auroc": 0.6477793912875554,
   "ci": [
    0.6027313999019183,
    0.6910919429850932
   ],
   "auprc": 0.7810857268965038,
   "prevalence": 0.6783320923306031
  },
  "auroc_disg": {
   "auroc": 0.7117560068301012,
   "ci": [
    0.6726968900329906,
    0.747156982680061
   ],
   "auprc": 0.8160344574623001,
   "prevalence": 0.6783320923306031
  },
  "orig_minus_disg": {
   "delta": -0.06397661554254586,
   "ci": [
    -0.09822851070892955,
    -0.032207955124332124
   ],
   "p_boot_le0": 1.0,
   "delong_z": -6.898429208769716,
   "delong_p": 5.258016244624741e-12
  },
  "MDE_2.8SE": 0.047157539703283874
 },
 "judge_cheap": {
  "n": 0,
  "untestable": true
 },
 "l3": {
  "n": 0,
  "untestable": true,
  "reason": "disguised L3 questionnaires need the OpenRouter key"
 },
 "note": "PEER signals never see text or names from the benchmark prompt, so they have no contamination channel; the fused score's only LLM component is the L3 questionnaire (text only)."
}
```
### (j) Coverage and cost
```
{
 "n_rows": 8507,
 "coverage_status": {
  "UNPARSEABLE": 1086,
  "OK": 7421
 },
 "peer_unavailable": 38,
 "n_unknown_gt0_share": 0.023312222072496967,
 "l3_missing": 0,
 "judge_cheap_disg_present": 1106,
 "judge_local_disg_present": 8474,
 "per_stratum": {
  "CTRL": {
   "n": 1907,
   "unparseable": 315,
   "median_secs_pairs": 0.002,
   "median_secs_text": 0.026,
   "median_sentence_secs": 2.64,
   "mean_cost_usd_peer_text": 1.4503618248557944e-05,
   "mean_judge_cost_usd": 4.1788148925013103e-07
  },
  "L20": {
   "n": 2000,
   "unparseable": 207,
   "median_secs_pairs": 0.007,
   "median_secs_text": 0.069,
   "median_sentence_secs": 11.98,
   "mean_cost_usd_peer_text": 1.634495e-05,
   "mean_judge_cost_usd": 0.0
  },
  "L25": {
   "n": 3260,
   "unparseable": 433,
   "median_secs_pairs": 0.019,
   "median_secs_text": 0.176,
   "median_sentence_secs": 22.06,
   "mean_cost_usd_peer_text": 2.2588220858895704e-05,
   "mean_judge_cost_usd": 0.0
  },
  "EXC": {
   "n": 1340,
   "unparseable": 131,
   "median_secs_pairs": 0.006,
   "median_secs_text": 0.049,
   "median_sentence_secs": 8.25,
   "mean_cost_usd_peer_text": 1.522686567164179e-05,
   "mean_judge_cost_usd": 0.0
  }
 },
 "mean_cpu_secs_per_row": {
  "peer_pairs": 0.02616480258725239,
  "nf_pairs": 0.20798908502897184,
  "text": 0.21951637245654224
 },
 "mean_usd_per_row": {
  "peer_text_L3_share": 1.8148571764429296e-05,
  "judge_cheap_orig+disg": 3.9845e-05
 }
}
```
### (k) Misc
```
{
 "gold_as_system": {
  "n": 535,
  "panel_reject_rate": 0.8130841121495327,
  "fused_flag_rate": 0.8074766355140187,
  "auroc_vs_panel_gold_audit": {
   "p_peer_text": 0.794080459770115,
   "p_text": 0.749367816091954,
   "peer_only": 0.667080459770115,
   "c_score_align": 0.7046436781609196,
   "judge_local_qwen8b_disg": 0.6792873563218391
  }
 },
 "FA_fused_tier_A_CORRECT": {
  "n": 414,
  "FA": 0.14492753623188406,
  "FA_text": 0.043478260869565216,
  "mean_p": 0.29016285727211355
 },
 "FA_fused_tier_B_CORRECT": {
  "n": 450,
  "FA": 0.4177777777777778,
  "FA_text": 0.06888888888888889,
  "mean_p": 0.5631265923111134
 },
 "recall_fused_at_frozen_thr_R_AB": 0.7063666300768386,
 "FA_fused_at_frozen_thr_R_AB": 0.28703703703703703,
 "precision_fused_at_frozen_thr_R_AB": 0.8384364820846906,
 "note": "threshold-based numbers carry the screen->E scale shift (frozen on short screen sentences)"
}
```