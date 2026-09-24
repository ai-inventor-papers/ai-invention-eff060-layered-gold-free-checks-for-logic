# T6-E Candidate-Signature Consensus on dataset E — tables (DEVELOPMENT E)

All numbers are DEVELOPMENT E (dataset E was used by earlier rounds to choose consensus; no confirmation claim). Scores are oriented higher = more likely ERROR. CIs: sentence-cluster percentile bootstrap, B = 2000, seed 0, paired on identical rows. 'strat' = within-source-stratum AUROC. Cells with < 50 ERROR or < 50 CORRECT rows are marked NOT_READ.

**Budget event.** The paid peer sweep was refused by the platform after 1,033 of ~9,000 planned calls (HTTP 403 aii_run_budget_exhausted: the run's shared 'Test idea' phase budget of $7.00 was used up, mostly by sibling artifacts; this artifact spent $0.108). CSC is therefore evaluated on PRIMARY = the 354 R_AB rows whose 3 CSC peer calls completed (fixed in prereg_csc_E_addendum1.json before scoring). FORMAT-ONLY, PLACEBO and RENAME arms are NOT_RUN. $0 analyses use all 2,686 rows.


## T0. Populations (DEVELOPMENT E)
# source: results/analysis.json populations; prereg_csc_E_addendum1.json

| population | rows | ERROR | CORRECT | sentences |
|---|---|---|---|---|
| PRIMARY | 354 | 196 | 158 | 144 |
| GE2 | 475 | 232 | 243 | 145 |
| MINI200 | 180 | 120 | 60 | 130 |
| FULL | 2686 | 1822 | 864 | 292 |


## T0b. PRIMARY rows by stratum (DEVELOPMENT E)
# source: results/analysis.json populations.PRIMARY_by_stratum

| stratum | ERROR | CORRECT | readable (>=50/50) |
|---|---|---|---|
| L25 | 59 | 22 | False |
| L20 | 77 | 20 | False |
| EXC | 41 | 45 | False |
| CTRL | 19 | 71 | False |


## T0c. Coverage and prompt-following (DEVELOPMENT E)
# source: results/analysis.json status

| quantity | value |
|---|---|
| CSC-OWN status on PRIMARY | {'OK': 354} |
| CSC insufficient-peer share (PRIMARY) | 0.000 |
| z3 UNKNOWN pairs (PRIMARY, CSC) | 0 |
| FREE-MATCHED status (FULL) | {'OK': 2463, 'csc_insufficient_peers': 223} |
| FREE-MATCHED insufficient share (FULL) | 0.083 |
| peer-peer exact agreement, CSC peers (PRIMARY) | 0.552 |
| peer-peer exact agreement, FREE-MATCHED peers (same rows) | 0.362 |
| peer-peer exact agreement, FREE-MATCHED peers (FULL) | 0.209 |


## T1. Error endorsement e and correct-row divergence d at c > 0.5, PRIMARY (DEVELOPMENT E)
# source: results/analysis.json a_ed_PRIMARY.cells

| cell | arm | n ERR | n COR | e = P(endorsed|ERROR) | d = P(flagged|CORRECT) | AUROC_b = 1-(e+d)/2 |
|---|---|---|---|---|---|---|
| R_AB | CSC | 196 | 158 | 0.459 [0.360, 0.549] | 0.139 [0.075, 0.234] | 0.701 |
| R_AB | CSC_graded | 196 | 158 | 0.643 [0.554, 0.719] | 0.089 [0.037, 0.163] | 0.634 |
| R_AB | CSC_multi | 196 | 158 | 0.531 [0.430, 0.623] | 0.127 [0.067, 0.213] | 0.671 |
| R_AB | FREE_exact | 196 | 158 | 0.173 [0.094, 0.257] | 0.323 [0.203, 0.473] | 0.752 |
| R_AB | FREE_align | 196 | 158 | 0.352 [0.250, 0.452] | 0.190 [0.101, 0.308] | 0.729 |
| R_AB | END_MAJ9 | 196 | 158 | 0.209 [0.108, 0.314] | 0.348 [0.232, 0.504] | 0.721 |
| R_AB | HYB_MEAN | 196 | 158 | 0.316 [0.216, 0.414] | 0.190 [0.110, 0.307] | 0.747 |
| L25 | CSC | 59 | 22 | 0.441 [0.281, 0.591] | 0.409 [0.176, 0.667] (NOT_READ) | 0.575 |
| L25 | CSC_graded | 59 | 22 | 0.627 [0.500, 0.742] | 0.318 [0.100, 0.556] (NOT_READ) | 0.527 |
| L25 | CSC_multi | 59 | 22 | 0.492 [0.333, 0.643] | 0.364 [0.148, 0.611] (NOT_READ) | 0.572 |
| L25 | FREE_exact | 59 | 22 | 0.186 [0.083, 0.318] | 0.591 [0.333, 0.840] (NOT_READ) | 0.611 |
| L25 | FREE_align | 59 | 22 | 0.424 [0.234, 0.607] | 0.318 [0.100, 0.579] (NOT_READ) | 0.629 |
| L25 | END_MAJ9 | 59 | 22 | 0.136 [0.000, 0.339] | 0.864 [0.667, 1.000] (NOT_READ) | 0.500 |
| L25 | HYB_MEAN | 59 | 22 | 0.254 [0.083, 0.444] | 0.591 [0.333, 0.850] (NOT_READ) | 0.577 |
| L20 | CSC | 77 | 20 | 0.390 [0.232, 0.554] | 0.300 [0.100, 0.667] (NOT_READ) | 0.655 |
| L20 | CSC_graded | 77 | 20 | 0.597 [0.447, 0.738] | 0.150 [0.000, 0.400] (NOT_READ) | 0.626 |
| L20 | CSC_multi | 77 | 20 | 0.506 [0.347, 0.663] | 0.250 [0.067, 0.571] (NOT_READ) | 0.622 |
| L20 | FREE_exact | 77 | 20 | 0.026 [0.000, 0.085] | 0.600 [0.333, 1.000] (NOT_READ) | 0.687 |
| L20 | FREE_align | 77 | 20 | 0.221 [0.094, 0.353] | 0.300 [0.100, 0.643] (NOT_READ) | 0.740 |
| L20 | END_MAJ9 | 77 | 20 | 0.169 [0.063, 0.290] | 0.400 [0.172, 0.800] (NOT_READ) | 0.716 |
| L20 | HYB_MEAN | 77 | 20 | 0.234 [0.111, 0.369] | 0.250 [0.067, 0.583] (NOT_READ) | 0.758 |
| EXC | CSC | 41 | 45 | 0.415 [0.200, 0.571] (NOT_READ) | 0.133 [0.017, 0.368] (NOT_READ) | 0.726 |
| EXC | CSC_graded | 41 | 45 | 0.610 [0.405, 0.766] (NOT_READ) | 0.089 [0.000, 0.286] (NOT_READ) | 0.651 |
| EXC | CSC_multi | 41 | 45 | 0.439 [0.214, 0.600] (NOT_READ) | 0.133 [0.017, 0.368] (NOT_READ) | 0.714 |
| EXC | FREE_exact | 41 | 45 | 0.244 [0.000, 0.418] (NOT_READ) | 0.400 [0.148, 0.773] (NOT_READ) | 0.678 |
| EXC | FREE_align | 41 | 45 | 0.341 [0.103, 0.500] (NOT_READ) | 0.333 [0.095, 0.688] (NOT_READ) | 0.663 |
| EXC | END_MAJ9 | 41 | 45 | 0.195 [0.000, 0.375] (NOT_READ) | 0.533 [0.291, 1.000] (NOT_READ) | 0.636 |
| EXC | HYB_MEAN | 41 | 45 | 0.341 [0.111, 0.508] (NOT_READ) | 0.178 [0.036, 0.458] (NOT_READ) | 0.740 |
| CTRL | CSC | 19 | 71 | 0.895 [0.667, 1.000] (NOT_READ) | 0.014 [0.000, 0.058] | 0.546 |
| CTRL | CSC_graded | 19 | 71 | 0.947 [0.875, 1.000] (NOT_READ) | 0.000 [0.000, 0.000] | 0.526 |
| CTRL | CSC_multi | 19 | 71 | 0.947 [0.667, 1.000] (NOT_READ) | 0.014 [0.000, 0.058] | 0.519 |
| CTRL | FREE_exact | 19 | 71 | 0.579 [0.000, 0.800] (NOT_READ) | 0.113 [0.012, 0.303] | 0.654 |
| CTRL | FREE_align | 19 | 71 | 0.684 [0.000, 0.944] (NOT_READ) | 0.028 [0.000, 0.094] | 0.644 |
| CTRL | END_MAJ9 | 19 | 71 | 0.632 [0.000, 0.880] (NOT_READ) | 0.056 [0.000, 0.167] | 0.656 |
| CTRL | HYB_MEAN | 19 | 71 | 0.789 [0.400, 0.951] (NOT_READ) | 0.056 [0.000, 0.167] | 0.577 |
| words_T1 | CSC | 58 | 118 | 0.517 [0.303, 0.673] | 0.051 [0.015, 0.110] | 0.716 |
| words_T1 | CSC_graded | 58 | 118 | 0.655 [0.466, 0.797] | 0.017 [0.000, 0.047] | 0.664 |
| words_T1 | CSC_multi | 58 | 118 | 0.552 [0.333, 0.719] | 0.051 [0.015, 0.110] | 0.699 |
| words_T1 | FREE_exact | 58 | 118 | 0.362 [0.154, 0.515] | 0.229 [0.106, 0.397] | 0.705 |
| words_T1 | FREE_align | 58 | 118 | 0.466 [0.229, 0.625] | 0.136 [0.045, 0.269] | 0.699 |
| words_T1 | END_MAJ9 | 58 | 118 | 0.397 [0.143, 0.574] | 0.220 [0.115, 0.381] | 0.692 |
| words_T1 | HYB_MEAN | 58 | 118 | 0.483 [0.268, 0.641] | 0.085 [0.032, 0.174] | 0.716 |
| words_T2 | CSC | 86 | 32 | 0.419 [0.274, 0.566] | 0.312 [0.118, 0.538] (NOT_READ) | 0.634 |
| words_T2 | CSC_graded | 86 | 32 | 0.640 [0.505, 0.760] | 0.219 [0.048, 0.423] (NOT_READ) | 0.571 |
| words_T2 | CSC_multi | 86 | 32 | 0.535 [0.382, 0.673] | 0.281 [0.095, 0.500] (NOT_READ) | 0.592 |
| words_T2 | FREE_exact | 86 | 32 | 0.035 [0.000, 0.095] | 0.562 [0.341, 0.786] (NOT_READ) | 0.701 |
| words_T2 | FREE_align | 86 | 32 | 0.244 [0.125, 0.375] | 0.312 [0.118, 0.535] (NOT_READ) | 0.722 |
| words_T2 | END_MAJ9 | 86 | 32 | 0.116 [0.032, 0.216] | 0.688 [0.455, 0.917] (NOT_READ) | 0.598 |
| words_T2 | HYB_MEAN | 86 | 32 | 0.233 [0.115, 0.356] | 0.406 [0.194, 0.652] (NOT_READ) | 0.681 |
| words_T3 | CSC | 52 | 8 | 0.462 [0.289, 0.630] | 0.750 [0.333, 1.000] (NOT_READ) | 0.394 |
| words_T3 | CSC_graded | 52 | 8 | 0.635 [0.484, 0.760] | 0.625 [0.198, 1.000] (NOT_READ) | 0.370 |
| words_T3 | CSC_multi | 52 | 8 | 0.500 [0.317, 0.667] | 0.625 [0.198, 1.000] (NOT_READ) | 0.438 |
| words_T3 | FREE_exact | 52 | 8 | 0.192 [0.081, 0.334] | 0.750 [0.333, 1.000] (NOT_READ) | 0.529 |
| words_T3 | FREE_align | 52 | 8 | 0.404 [0.197, 0.609] | 0.500 [0.000, 0.889] (NOT_READ) | 0.548 |
| words_T3 | END_MAJ9 | 52 | 8 | 0.154 [0.000, 0.377] | 0.875 [0.571, 1.000] (NOT_READ) | 0.486 |
| words_T3 | HYB_MEAN | 52 | 8 | 0.269 [0.075, 0.482] | 0.875 [0.571, 1.000] (NOT_READ) | 0.428 |
| ncond_0-1 | CSC | 25 | 77 | 0.640 [0.231, 0.844] (NOT_READ) | 0.078 [0.010, 0.208] | 0.641 |
| ncond_0-1 | CSC_graded | 25 | 77 | 0.720 [0.400, 0.880] (NOT_READ) | 0.039 [0.000, 0.143] | 0.621 |
| ncond_0-1 | CSC_multi | 25 | 77 | 0.680 [0.231, 0.889] (NOT_READ) | 0.078 [0.010, 0.208] | 0.621 |
| ncond_0-1 | FREE_exact | 25 | 77 | 0.440 [0.000, 0.667] (NOT_READ) | 0.182 [0.045, 0.406] | 0.689 |
| ncond_0-1 | FREE_align | 25 | 77 | 0.520 [0.000, 0.786] (NOT_READ) | 0.078 [0.010, 0.208] | 0.701 |
| ncond_0-1 | END_MAJ9 | 25 | 77 | 0.440 [0.000, 0.730] (NOT_READ) | 0.130 [0.036, 0.304] | 0.715 |
| ncond_0-1 | HYB_MEAN | 25 | 77 | 0.480 [0.000, 0.757] (NOT_READ) | 0.104 [0.019, 0.256] | 0.708 |
| ncond_2 | CSC | 14 | 21 | 0.571 [0.000, 0.800] (NOT_READ) | 0.000 [0.000, 0.000] (NOT_READ) | 0.714 |
| ncond_2 | CSC_graded | 14 | 21 | 0.714 [0.429, 1.000] (NOT_READ) | 0.000 [0.000, 0.000] (NOT_READ) | 0.643 |
| ncond_2 | CSC_multi | 14 | 21 | 0.571 [0.000, 0.800] (NOT_READ) | 0.000 [0.000, 0.000] (NOT_READ) | 0.714 |
| ncond_2 | FREE_exact | 14 | 21 | 0.286 [0.000, 0.533] (NOT_READ) | 0.238 [0.000, 1.000] (NOT_READ) | 0.738 |
| ncond_2 | FREE_align | 14 | 21 | 0.286 [0.000, 0.533] (NOT_READ) | 0.238 [0.000, 1.000] (NOT_READ) | 0.738 |
| ncond_2 | END_MAJ9 | 14 | 21 | 0.357 [0.000, 0.565] (NOT_READ) | 0.333 [0.000, 1.000] (NOT_READ) | 0.655 |
| ncond_2 | HYB_MEAN | 14 | 21 | 0.500 [0.000, 0.700] (NOT_READ) | 0.048 [0.000, 1.000] (NOT_READ) | 0.726 |
| ncond_3 | CSC | 35 | 27 | 0.257 [0.074, 0.425] (NOT_READ) | 0.148 [0.029, 0.375] (NOT_READ) | 0.797 |
| ncond_3 | CSC_graded | 35 | 27 | 0.543 [0.320, 0.731] (NOT_READ) | 0.111 [0.000, 0.300] (NOT_READ) | 0.673 |
| ncond_3 | CSC_multi | 35 | 27 | 0.314 [0.115, 0.500] (NOT_READ) | 0.148 [0.029, 0.375] (NOT_READ) | 0.769 |
| ncond_3 | FREE_exact | 35 | 27 | 0.257 [0.053, 0.464] (NOT_READ) | 0.296 [0.036, 0.621] (NOT_READ) | 0.723 |
| ncond_3 | FREE_align | 35 | 27 | 0.314 [0.087, 0.531] (NOT_READ) | 0.296 [0.036, 0.621] (NOT_READ) | 0.695 |
| ncond_3 | END_MAJ9 | 35 | 27 | 0.114 [0.000, 0.300] (NOT_READ) | 0.519 [0.250, 0.895] (NOT_READ) | 0.684 |
| ncond_3 | HYB_MEAN | 35 | 27 | 0.114 [0.000, 0.300] (NOT_READ) | 0.259 [0.077, 0.591] (NOT_READ) | 0.813 |
| ncond_4+ | CSC | 122 | 33 | 0.467 [0.344, 0.584] | 0.364 [0.174, 0.577] (NOT_READ) | 0.585 |
| ncond_4+ | CSC_graded | 122 | 33 | 0.648 [0.531, 0.742] | 0.242 [0.081, 0.426] (NOT_READ) | 0.555 |
| ncond_4+ | CSC_multi | 122 | 33 | 0.557 [0.429, 0.664] | 0.303 [0.125, 0.500] (NOT_READ) | 0.570 |
| ncond_4+ | FREE_exact | 122 | 33 | 0.082 [0.034, 0.141] | 0.727 [0.545, 0.891] (NOT_READ) | 0.595 |
| ncond_4+ | FREE_align | 122 | 33 | 0.336 [0.219, 0.458] | 0.333 [0.154, 0.541] (NOT_READ) | 0.665 |
| ncond_4+ | END_MAJ9 | 122 | 33 | 0.172 [0.069, 0.295] | 0.727 [0.519, 0.931] (NOT_READ) | 0.550 |
| ncond_4+ | HYB_MEAN | 122 | 33 | 0.320 [0.207, 0.437] | 0.424 [0.222, 0.639] (NOT_READ) | 0.628 |
| tierA | CSC | 65 | 114 | 0.585 [0.391, 0.745] | 0.035 [0.007, 0.083] | 0.690 |
| tierA | CSC_graded | 65 | 114 | 0.738 [0.575, 0.865] | 0.018 [0.000, 0.051] | 0.622 |
| tierA | CSC_multi | 65 | 114 | 0.662 [0.478, 0.812] | 0.035 [0.007, 0.083] | 0.652 |
| tierA | FREE_exact | 65 | 114 | 0.338 [0.139, 0.500] | 0.158 [0.059, 0.312] | 0.752 |
| tierA | FREE_align | 65 | 114 | 0.446 [0.218, 0.625] | 0.105 [0.021, 0.231] | 0.724 |
| tierA | END_MAJ9 | 65 | 114 | 0.338 [0.103, 0.526] | 0.175 [0.078, 0.319] | 0.743 |
| tierA | HYB_MEAN | 65 | 114 | 0.446 [0.231, 0.624] | 0.053 [0.010, 0.125] | 0.751 |
| VEX | CSC | 22 | 115 | 0.091 [0.000, 0.278] (NOT_READ) | 0.043 [0.010, 0.099] | 0.933 |
| VEX | CSC_graded | 22 | 115 | 0.227 [0.062, 0.480] (NOT_READ) | 0.017 [0.000, 0.050] | 0.878 |
| VEX | CSC_multi | 22 | 115 | 0.136 [0.000, 0.375] (NOT_READ) | 0.043 [0.010, 0.099] | 0.910 |
| VEX | FREE_exact | 22 | 115 | 0.136 [0.000, 0.409] (NOT_READ) | 0.165 [0.065, 0.319] | 0.849 |
| VEX | FREE_align | 22 | 115 | 0.136 [0.000, 0.409] (NOT_READ) | 0.113 [0.029, 0.239] | 0.875 |
| VEX | END_MAJ9 | 22 | 115 | 0.000 [0.000, 0.000] (NOT_READ) | 0.183 [0.085, 0.333] | 0.909 |
| VEX | HYB_MEAN | 22 | 115 | 0.045 [0.000, 0.167] (NOT_READ) | 0.061 [0.016, 0.138] | 0.947 |


## T1b. Paired CSC − other arm on the same PRIMARY rows (DEVELOPMENT E)
# source: results/analysis.json a_ed_PRIMARY.paired_CSC_minus

| other arm | Δe [CI] | Δd [CI] |
|---|---|---|
| CSC_graded | -0.184 [-0.249, -0.123] | +0.051 [+0.017, +0.099] |
| CSC_multi | -0.071 [-0.126, -0.028] | +0.013 [+0.000, +0.036] |
| FREE_exact | +0.286 [+0.179, +0.391] | -0.184 [-0.314, -0.087] |
| FREE_align | +0.107 [+0.019, +0.196] | -0.051 [-0.139, +0.020] |
| END_MAJ9 | +0.250 [+0.175, +0.332] | -0.209 [-0.333, -0.121] |
| HYB_MEAN | +0.143 [+0.090, +0.199] | -0.051 [-0.111, -0.010] |


## T2. $0 FULL population (2,686 rows): e / d of the matched free peers, exact names vs ALIGN (DEVELOPMENT E)
# source: results/analysis.json a_ed_FULL.cells

| cell | arm | n ERR | n COR | e | d |
|---|---|---|---|---|---|
| R_AB | FREE_exact | 1822 | 864 | 0.130 [0.098, 0.162] | 0.583 [0.510, 0.660] |
| R_AB | FREE_align | 1822 | 864 | 0.268 [0.224, 0.312] | 0.328 [0.270, 0.395] |
| R_AB | FREE_graded | 1822 | 864 | 0.194 [0.159, 0.231] | 0.406 [0.351, 0.468] |
| R_AB | END_MAJ9 | 1822 | 864 | 0.123 [0.087, 0.164] | 0.538 [0.462, 0.621] |
| L25 | FREE_exact | 697 | 176 | 0.208 [0.144, 0.276] | 0.716 [0.592, 0.822] |
| L25 | FREE_align | 697 | 176 | 0.291 [0.224, 0.368] | 0.506 [0.385, 0.623] |
| L25 | FREE_graded | 697 | 176 | 0.248 [0.183, 0.318] | 0.562 [0.452, 0.676] |
| L25 | END_MAJ9 | 697 | 176 | 0.039 [0.009, 0.077] | 0.841 [0.734, 0.940] |
| L20 | FREE_exact | 592 | 229 | 0.041 [0.012, 0.078] | 0.838 [0.756, 0.920] |
| L20 | FREE_align | 592 | 229 | 0.189 [0.136, 0.246] | 0.415 [0.310, 0.532] |
| L20 | FREE_graded | 592 | 229 | 0.105 [0.063, 0.155] | 0.559 [0.477, 0.649] |
| L20 | END_MAJ9 | 592 | 229 | 0.103 [0.057, 0.158] | 0.699 [0.573, 0.827] |
| EXC | FREE_exact | 384 | 222 | 0.078 [0.030, 0.137] | 0.667 [0.536, 0.804] |
| EXC | FREE_align | 384 | 222 | 0.193 [0.124, 0.264] | 0.396 [0.279, 0.535] |
| EXC | FREE_graded | 384 | 222 | 0.161 [0.098, 0.232] | 0.437 [0.331, 0.563] |
| EXC | END_MAJ9 | 384 | 222 | 0.109 [0.045, 0.177] | 0.622 [0.487, 0.762] |
| CTRL | FREE_exact | 149 | 237 | 0.248 [0.087, 0.422] | 0.160 [0.087, 0.261] |
| CTRL | FREE_align | 149 | 237 | 0.664 [0.467, 0.815] | 0.046 [0.014, 0.096] |
| CTRL | FREE_graded | 149 | 237 | 0.376 [0.244, 0.509] | 0.114 [0.057, 0.189] |
| CTRL | END_MAJ9 | 149 | 237 | 0.638 [0.424, 0.783] | 0.080 [0.032, 0.151] |
| words_T1 | FREE_exact | 540 | 473 | 0.119 [0.058, 0.185] | 0.416 [0.319, 0.522] |
| words_T1 | FREE_align | 540 | 473 | 0.328 [0.234, 0.423] | 0.192 [0.131, 0.270] |
| words_T1 | FREE_graded | 540 | 473 | 0.220 [0.155, 0.290] | 0.268 [0.200, 0.348] |
| words_T1 | END_MAJ9 | 540 | 473 | 0.289 [0.189, 0.393] | 0.307 [0.221, 0.404] |
| words_T2 | FREE_exact | 710 | 276 | 0.070 [0.037, 0.109] | 0.790 [0.704, 0.873] |
| words_T2 | FREE_align | 710 | 276 | 0.200 [0.151, 0.252] | 0.435 [0.338, 0.535] |
| words_T2 | FREE_graded | 710 | 276 | 0.127 [0.085, 0.174] | 0.562 [0.485, 0.643] |
| words_T2 | END_MAJ9 | 710 | 276 | 0.065 [0.033, 0.107] | 0.779 [0.680, 0.872] |
| words_T3 | FREE_exact | 572 | 115 | 0.213 [0.144, 0.295] | 0.774 [0.650, 0.875] |
| words_T3 | FREE_align | 572 | 115 | 0.295 [0.221, 0.385] | 0.626 [0.495, 0.745] |
| words_T3 | FREE_graded | 572 | 115 | 0.252 [0.181, 0.335] | 0.600 [0.482, 0.726] |
| words_T3 | END_MAJ9 | 572 | 115 | 0.040 [0.006, 0.086] | 0.913 [0.822, 0.982] |
| ncond_0-1 | FREE_exact | 256 | 310 | 0.160 [0.063, 0.278] | 0.313 [0.211, 0.434] |
| ncond_0-1 | FREE_align | 256 | 310 | 0.406 [0.259, 0.554] | 0.152 [0.078, 0.237] |
| ncond_0-1 | FREE_graded | 256 | 310 | 0.270 [0.176, 0.374] | 0.197 [0.128, 0.285] |
| ncond_0-1 | END_MAJ9 | 256 | 310 | 0.324 [0.171, 0.481] | 0.219 [0.127, 0.331] |
| ncond_4+ | FREE_exact | 1164 | 350 | 0.129 [0.091, 0.173] | 0.826 [0.767, 0.879] |
| ncond_4+ | FREE_align | 1164 | 350 | 0.247 [0.201, 0.297] | 0.471 [0.386, 0.559] |
| ncond_4+ | FREE_graded | 1164 | 350 | 0.168 [0.126, 0.213] | 0.617 [0.551, 0.686] |
| ncond_4+ | END_MAJ9 | 1164 | 350 | 0.070 [0.040, 0.104] | 0.797 [0.711, 0.876] |


Paired FREE exact − FREE ALIGN on FULL: Δe -0.138 [-0.171, -0.107], Δd +0.256 [+0.203, +0.313] (# source: results/analysis.json a_ed_FULL.paired_exact_minus_align)


## T3. GEE slopes (binomial logit, exchangeable, sentence clusters) of d and e on z(words), z(n_conditions) (DEVELOPMENT E)
# source: results/analysis.json a_ed_*.gee

| population | arm | model | term | coef [95% CI] | n |
|---|---|---|---|---|---|
| PRIMARY | CSC | d_words_ncond | zw | +1.251 [+0.412, +2.090] | 158 |
| PRIMARY | CSC | d_words_ncond | zn | +0.199 [-0.607, +1.004] | 158 |
| PRIMARY | CSC | e_words_ncond | zw | -0.099 [-0.526, +0.327] | 196 |
| PRIMARY | CSC | e_words_ncond | zn | -0.023 [-0.504, +0.457] | 196 |
| PRIMARY | CSC | d_words_ncond_stratum | zw | +2.506 [+0.745, +4.267] | 158 |
| PRIMARY | CSC | d_words_ncond_stratum | zn | +0.357 [-0.529, +1.242] | 158 |
| PRIMARY | CSC_graded | d_words_ncond | zw | +1.614 [+0.568, +2.661] | 158 |
| PRIMARY | CSC_graded | d_words_ncond | zn | +0.321 [-0.830, +1.473] | 158 |
| PRIMARY | CSC_graded | e_words_ncond | zw | +0.040 [-0.367, +0.447] | 196 |
| PRIMARY | CSC_graded | e_words_ncond | zn | -0.294 [-0.750, +0.162] | 196 |
| PRIMARY | CSC_graded | d_words_ncond_stratum | zw | +3.989 [+1.749, +6.230] | 158 |
| PRIMARY | CSC_graded | d_words_ncond_stratum | zn | +0.791 [-0.233, +1.816] | 158 |
| PRIMARY | CSC_multi | d_words_ncond | zw | +1.218 [+0.371, +2.065] | 158 |
| PRIMARY | CSC_multi | d_words_ncond | zn | +0.117 [-0.727, +0.961] | 158 |
| PRIMARY | CSC_multi | e_words_ncond | zw | -0.080 [-0.530, +0.371] | 196 |
| PRIMARY | CSC_multi | e_words_ncond | zn | -0.026 [-0.510, +0.457] | 196 |
| PRIMARY | CSC_multi | d_words_ncond_stratum | zw | +2.476 [+0.752, +4.200] | 158 |
| PRIMARY | CSC_multi | d_words_ncond_stratum | zn | +0.321 [-0.624, +1.267] | 158 |
| PRIMARY | FREE_exact | d_words_ncond | zw | +0.317 [-0.420, +1.054] | 158 |
| PRIMARY | FREE_exact | d_words_ncond | zn | +0.554 [-0.145, +1.253] | 158 |
| PRIMARY | FREE_exact | e_words_ncond | zw | +0.249 [-0.608, +1.105] | 196 |
| PRIMARY | FREE_exact | e_words_ncond | zn | -0.374 [-1.127, +0.379] | 196 |
| PRIMARY | FREE_exact | d_words_ncond_stratum | zw | +1.102 [-0.121, +2.325] | 158 |
| PRIMARY | FREE_exact | d_words_ncond_stratum | zn | +0.815 [-0.002, +1.632] | 158 |
| PRIMARY | FREE_align | d_words_ncond | zw | +0.324 [-0.440, +1.087] | 158 |
| PRIMARY | FREE_align | d_words_ncond | zn | +0.252 [-0.431, +0.934] | 158 |
| PRIMARY | FREE_align | e_words_ncond | zw | +0.154 [-0.416, +0.724] | 196 |
| PRIMARY | FREE_align | e_words_ncond | zn | -0.039 [-0.534, +0.456] | 196 |
| PRIMARY | FREE_align | d_words_ncond_stratum | zw | +0.914 [-0.245, +2.074] | 158 |
| PRIMARY | FREE_align | d_words_ncond_stratum | zn | +0.284 [-0.646, +1.214] | 158 |
| PRIMARY | END_MAJ9 | d_words_ncond | zw | +0.598 [-0.128, +1.323] | 158 |
| PRIMARY | END_MAJ9 | d_words_ncond | zn | +0.521 [-0.260, +1.302] | 158 |
| PRIMARY | END_MAJ9 | e_words_ncond | zw | -0.956 [-1.584, -0.327] | 196 |
| PRIMARY | END_MAJ9 | e_words_ncond | zn | +0.422 [-0.047, +0.890] | 196 |
| PRIMARY | END_MAJ9 | d_words_ncond_stratum | zw | +0.611 [-0.415, +1.637] | 158 |
| PRIMARY | END_MAJ9 | d_words_ncond_stratum | zn | +0.366 [-0.687, +1.419] | 158 |
| PRIMARY | HYB_MEAN | d_words_ncond | zw | +1.154 [+0.328, +1.980] | 158 |
| PRIMARY | HYB_MEAN | d_words_ncond | zn | -0.018 [-0.646, +0.610] | 158 |
| PRIMARY | HYB_MEAN | e_words_ncond | zw | -0.508 [-1.026, +0.010] | 196 |
| PRIMARY | HYB_MEAN | e_words_ncond | zn | +0.269 [-0.209, +0.747] | 196 |
| PRIMARY | HYB_MEAN | d_words_ncond_stratum | zw | +1.568 [+0.251, +2.885] | 158 |
| PRIMARY | HYB_MEAN | d_words_ncond_stratum | zn | +0.272 [-0.577, +1.121] | 158 |
| FULL | FREE_exact | d_words_ncond | zw | +0.291 [-0.130, +0.712] | 864 |
| FULL | FREE_exact | d_words_ncond | zn | +0.304 [-0.107, +0.714] | 864 |
| FULL | FREE_exact | e_words_ncond | zw | +0.552 [+0.191, +0.913] | 1822 |
| FULL | FREE_exact | e_words_ncond | zn | -0.201 [-0.540, +0.139] | 1822 |
| FULL | FREE_exact | d_words_ncond_stratum | zw | +1.212 [+0.536, +1.888] | 864 |
| FULL | FREE_exact | d_words_ncond_stratum | zn | +0.305 [-0.207, +0.818] | 864 |
| FULL | FREE_align | d_words_ncond | zw | +0.511 [+0.177, +0.846] | 864 |
| FULL | FREE_align | d_words_ncond | zn | +0.205 [-0.143, +0.553] | 864 |
| FULL | FREE_align | e_words_ncond | zw | +0.232 [-0.045, +0.509] | 1822 |
| FULL | FREE_align | e_words_ncond | zn | -0.231 [-0.500, +0.038] | 1822 |
| FULL | FREE_align | d_words_ncond_stratum | zw | +1.239 [+0.661, +1.817] | 864 |
| FULL | FREE_align | d_words_ncond_stratum | zn | +0.364 [-0.060, +0.787] | 864 |
| FULL | FREE_graded | d_words_ncond | zw | +0.265 [-0.049, +0.579] | 864 |
| FULL | FREE_graded | d_words_ncond | zn | +0.297 [-0.008, +0.601] | 864 |
| FULL | FREE_graded | e_words_ncond | zw | +0.420 [+0.138, +0.701] | 1822 |
| FULL | FREE_graded | e_words_ncond | zn | -0.302 [-0.569, -0.035] | 1822 |
| FULL | FREE_graded | d_words_ncond_stratum | zw | +0.648 [+0.160, +1.136] | 864 |
| FULL | FREE_graded | d_words_ncond_stratum | zn | +0.306 [-0.064, +0.676] | 864 |
| FULL | END_MAJ9 | d_words_ncond | zw | +1.144 [+0.665, +1.622] | 864 |
| FULL | END_MAJ9 | d_words_ncond | zn | +0.268 [-0.214, +0.751] | 864 |
| FULL | END_MAJ9 | e_words_ncond | zw | -0.852 [-1.214, -0.490] | 1822 |
| FULL | END_MAJ9 | e_words_ncond | zn | -0.092 [-0.487, +0.302] | 1822 |
| FULL | END_MAJ9 | d_words_ncond_stratum | zw | +1.950 [+1.127, +2.773] | 864 |
| FULL | END_MAJ9 | d_words_ncond_stratum | zn | +0.577 [-0.152, +1.305] | 864 |


## T3b. NET Δ(e+d), words tercile T3 − T1 (DEVELOPMENT E)
# source: results/analysis.json net

| population | arm | NET [CI] | Δe | Δd | verdict |
|---|---|---|---|---|---|
| PRIMARY | CSC | +0.643 [+0.229, +0.980] | -0.056 | +0.699 | DEGRADES_WITH_COMPLEXITY (legitimate divergence dominates) |
| PRIMARY | FREE_align | +0.303 [-0.211, +0.721] | -0.062 | +0.364 | BALANCED_OR_UNDETERMINED |
| PRIMARY | END_MAJ9 | +0.412 [+0.114, +0.684] | -0.243 | +0.655 | DEGRADES_WITH_COMPLEXITY (legitimate divergence dominates) |
| FULL | FREE_exact | +0.452 [+0.290, +0.602] | +0.095 | +0.357 | DEGRADES_WITH_COMPLEXITY (legitimate divergence dominates) |
| FULL | FREE_align | +0.401 [+0.242, +0.548] | -0.032 | +0.434 | DEGRADES_WITH_COMPLEXITY (legitimate divergence dominates) |
| FULL | END_MAJ9 | +0.358 [+0.210, +0.489] | -0.249 | +0.606 | DEGRADES_WITH_COMPLEXITY (legitimate divergence dominates) |


## T4. AUROC on PRIMARY rows (n_err/n_cor R_AB = 196/158) (DEVELOPMENT E)
# source: results/analysis.json b_PRIMARY.metrics

| metric | R_AB [strat] | R_AB [pooled] | long L25+L20+EXC [strat] | L25 [pooled] | AUPRC (R_AB) |
|---|---|---|---|---|---|
| CSC c_csc | 0.614 [0.493, 0.736] | 0.715 [0.620, 0.799] | 0.684 [0.576, 0.785] | 0.570 [0.423, 0.747] (NOT_READ) | 0.740 |
| CSC c_csc_graded | 0.608 [0.487, 0.734] | 0.691 [0.601, 0.772] | 0.677 [0.571, 0.772] | 0.546 [0.390, 0.722] (NOT_READ) | 0.732 |
| CSC c_csc_multi | 0.601 [0.480, 0.720] | 0.693 [0.601, 0.776] | 0.672 [0.569, 0.769] | 0.576 [0.425, 0.751] (NOT_READ) | 0.720 |
| HYB_MEAN | 0.709 [0.586, 0.817] | 0.788 [0.691, 0.873] | 0.741 [0.625, 0.837] | 0.605 [0.460, 0.780] (NOT_READ) | 0.824 |
| HYB_MAX | 0.707 [0.586, 0.819] | 0.788 [0.692, 0.874] | 0.733 [0.617, 0.834] | 0.625 [0.480, 0.809] (NOT_READ) | 0.803 |
| FREE-MATCHED exact (same 3 families, no signature) | 0.770 [0.686, 0.844] | 0.837 [0.756, 0.897] | 0.739 [0.642, 0.827] | 0.698 [0.557, 0.823] (NOT_READ) | 0.808 |
| FREE-MATCHED ALIGN | 0.731 [0.635, 0.825] | 0.801 [0.711, 0.875] | 0.745 [0.638, 0.843] | 0.611 [0.449, 0.791] (NOT_READ) | 0.796 |
| FREE-MATCHED graded (identity) | 0.751 [0.657, 0.832] | 0.829 [0.743, 0.894] | 0.710 [0.605, 0.805] | 0.637 [0.485, 0.779] (NOT_READ) | 0.796 |
| c_score_align (9 free peers, ALIGN) | 0.774 [0.682, 0.857] | 0.815 [0.726, 0.892] | 0.765 [0.659, 0.861] | 0.637 [0.489, 0.811] (NOT_READ) | 0.834 |
| p_peer_text | 0.799 [0.700, 0.880] | 0.848 [0.767, 0.910] | 0.819 [0.722, 0.894] | 0.701 [0.541, 0.857] (NOT_READ) | 0.868 |
| flash-lite judge (disguised) | 0.664 [0.568, 0.750] | 0.754 [0.665, 0.825] | 0.632 [0.534, 0.719] | 0.653 [0.481, 0.812] (NOT_READ) | 0.728 |
| flash-lite judge (original) | 0.549 [0.476, 0.625] | 0.571 [0.465, 0.674] | 0.565 [0.482, 0.645] | 0.552 [0.432, 0.681] (NOT_READ) | 0.621 |
| gpt-4.1-nano judge (original) | 0.591 [0.478, 0.703] | 0.684 [0.582, 0.771] | 0.583 [0.475, 0.685] | 0.644 [0.461, 0.797] (NOT_READ) | 0.716 |
| round-trip NLI (min) | 0.622 [0.490, 0.744] | 0.710 [0.593, 0.813] | 0.590 [0.458, 0.711] | 0.629 [0.461, 0.773] (NOT_READ) | 0.709 |
| self-consistency sc5 | 0.658 [0.552, 0.759] | 0.727 [0.621, 0.815] | 0.663 [0.543, 0.774] | 0.549 [0.425, 0.711] (NOT_READ) | 0.709 |
| S4_full stack (OOF) | 0.736 [0.635, 0.826] | 0.822 [0.734, 0.891] | 0.747 [0.637, 0.835] | 0.724 [0.553, 0.856] (NOT_READ) | 0.812 |


## T4b. AUROC on PRIMARY rows, other cells (DEVELOPMENT E)
# source: results/analysis.json b_PRIMARY.metrics

| metric | L20 [pooled] | EXC [pooled] | CTRL [pooled] | tier A only [strat] | VEX subset [strat] |
|---|---|---|---|---|---|
| CSC c_csc | 0.697 [0.468, 0.840] (NOT_READ) | 0.753 [0.576, 0.911] (NOT_READ) | 0.370 [0.189, 0.626] (NOT_READ) | 0.546 [0.354, 0.790] | 0.905 [0.747, 0.993] (NOT_READ) |
| CSC c_csc_graded | 0.730 [0.527, 0.865] (NOT_READ) | 0.725 [0.560, 0.887] (NOT_READ) | 0.369 [0.188, 0.626] (NOT_READ) | 0.534 [0.351, 0.778] | 0.905 [0.747, 0.992] (NOT_READ) |
| CSC c_csc_multi | 0.723 [0.494, 0.864] (NOT_READ) | 0.697 [0.529, 0.847] (NOT_READ) | 0.355 [0.169, 0.626] (NOT_READ) | 0.512 [0.333, 0.745] | 0.895 [0.726, 0.989] (NOT_READ) |
| HYB_MEAN | 0.760 [0.538, 0.888] (NOT_READ) | 0.821 [0.633, 0.960] (NOT_READ) | 0.596 [0.330, 0.977] (NOT_READ) | 0.667 [0.464, 0.902] | 0.960 [0.836, 1.000] (NOT_READ) |
| HYB_MAX | 0.726 [0.481, 0.868] (NOT_READ) | 0.815 [0.617, 0.961] (NOT_READ) | 0.615 [0.340, 0.993] (NOT_READ) | 0.678 [0.480, 0.914] | 0.960 [0.865, 1.000] (NOT_READ) |
| FREE-MATCHED exact (same 3 families, no signature) | 0.738 [0.542, 0.873] (NOT_READ) | 0.769 [0.569, 0.913] (NOT_READ) | 0.876 [0.735, 0.983] (NOT_READ) | 0.861 [0.719, 0.954] | 0.857 [0.638, 0.986] (NOT_READ) |
| FREE-MATCHED ALIGN | 0.827 [0.665, 0.927] (NOT_READ) | 0.772 [0.578, 0.937] (NOT_READ) | 0.680 [0.515, 1.000] (NOT_READ) | 0.704 [0.576, 0.900] | 0.881 [0.665, 1.000] (NOT_READ) |
| FREE-MATCHED graded (identity) | 0.734 [0.537, 0.870] (NOT_READ) | 0.742 [0.530, 0.907] (NOT_READ) | 0.893 [0.768, 0.992] (NOT_READ) | 0.840 [0.677, 0.949] | 0.896 [0.754, 0.975] (NOT_READ) |
| c_score_align (9 free peers, ALIGN) | 0.778 [0.574, 0.899] (NOT_READ) | 0.846 [0.672, 0.986] (NOT_READ) | 0.804 [0.636, 0.993] (NOT_READ) | 0.812 [0.673, 0.948] | 0.966 [0.848, 1.000] (NOT_READ) |
| p_peer_text | 0.822 [0.679, 0.917] (NOT_READ) | 0.899 [0.765, 0.977] (NOT_READ) | 0.730 [0.517, 1.000] (NOT_READ) | 0.853 [0.681, 0.980] | 0.971 [0.898, 1.000] (NOT_READ) |
| flash-lite judge (disguised) | 0.560 [0.400, 0.722] (NOT_READ) | 0.678 [0.517, 0.788] (NOT_READ) | 0.774 [0.558, 0.990] (NOT_READ) | 0.685 [0.522, 0.828] | 0.626 [0.423, 0.767] (NOT_READ) |
| flash-lite judge (original) | 0.538 [0.358, 0.706] (NOT_READ) | 0.598 [0.473, 0.726] (NOT_READ) | 0.491 [0.333, 0.719] (NOT_READ) | 0.495 [0.393, 0.616] | 0.632 [0.416, 0.796] (NOT_READ) |
| gpt-4.1-nano judge (original) | 0.476 [0.300, 0.646] (NOT_READ) | 0.629 [0.426, 0.816] (NOT_READ) | 0.619 [0.278, 0.924] (NOT_READ) | 0.604 [0.363, 0.835] | 0.661 [0.409, 0.849] (NOT_READ) |
| round-trip NLI (min) | 0.679 [0.480, 0.839] (NOT_READ) | 0.487 [0.277, 0.738] (NOT_READ) | 0.732 [0.397, 0.990] (NOT_READ) | 0.607 [0.367, 0.860] | 0.381 [0.134, 0.695] (NOT_READ) |
| self-consistency sc5 | 0.592 [0.412, 0.738] (NOT_READ) | 0.802 [0.595, 0.958] (NOT_READ) | 0.640 [0.385, 0.915] (NOT_READ) | 0.704 [0.514, 0.881] | 0.815 [0.596, 0.955] (NOT_READ) |
| S4_full stack (OOF) | 0.725 [0.539, 0.870] (NOT_READ) | 0.781 [0.579, 0.926] (NOT_READ) | 0.700 [0.404, 0.962] (NOT_READ) | 0.756 [0.552, 0.932] | 0.851 [0.634, 0.982] (NOT_READ) |


## T5. Paired ΔAUROC, CSC variant − comparator, PRIMARY rows (DEVELOPMENT E)
# source: results/analysis.json b_PRIMARY.deltas

| CSC variant | comparator | R_AB strat | long strat | L25 pooled | tier A strat |
|---|---|---|---|---|---|
| CSC c_csc | FREE-MATCHED exact (same 3 families, no signature) | -0.156 [-0.290, -0.031] | -0.055 [-0.144, +0.036] | -0.128 [-0.280, +0.051] (NOT_READ) | -0.316 [-0.547, -0.022] |
| CSC c_csc | FREE-MATCHED ALIGN | -0.117 [-0.205, -0.029] | -0.062 [-0.138, +0.020] | -0.042 [-0.151, +0.084] (NOT_READ) | -0.159 [-0.340, +0.023] |
| CSC c_csc | c_score_align (9 free peers, ALIGN) | -0.160 [-0.275, -0.064] | -0.081 [-0.155, -0.006] | -0.067 [-0.183, +0.040] (NOT_READ) | -0.266 [-0.487, -0.042] |
| CSC c_csc | p_peer_text | -0.185 [-0.281, -0.103] | -0.135 [-0.208, -0.059] | -0.132 [-0.253, -0.008] (NOT_READ) | -0.307 [-0.497, -0.131] |
| CSC c_csc | flash-lite judge (disguised) | -0.050 [-0.212, +0.107] | +0.051 [-0.074, +0.180] | -0.083 [-0.304, +0.165] (NOT_READ) | -0.140 [-0.414, +0.196] |
| CSC c_csc | flash-lite judge (original) | +0.065 [-0.050, +0.183] | +0.119 [-0.003, +0.232] | +0.018 [-0.154, +0.213] (NOT_READ) | +0.051 [-0.138, +0.256] |
| CSC c_csc | gpt-4.1-nano judge (original) | +0.023 [-0.140, +0.175] | +0.101 [-0.034, +0.232] | -0.074 [-0.310, +0.209] (NOT_READ) | -0.058 [-0.352, +0.254] |
| CSC c_csc | round-trip NLI (min) | -0.008 [-0.198, +0.179] | +0.094 [-0.072, +0.260] | -0.060 [-0.249, +0.169] (NOT_READ) | -0.062 [-0.424, +0.311] |
| CSC c_csc | self-consistency sc5 | -0.044 [-0.178, +0.093] | +0.021 [-0.108, +0.159] | +0.020 [-0.135, +0.195] (NOT_READ) | -0.159 [-0.397, +0.115] |
| CSC c_csc | S4_full stack (OOF) | -0.123 [-0.269, +0.010] | -0.063 [-0.185, +0.068] | -0.154 [-0.369, +0.095] (NOT_READ) | -0.210 [-0.477, +0.057] |
| CSC c_csc_graded | FREE-MATCHED exact (same 3 families, no signature) | -0.162 [-0.291, -0.034] | -0.062 [-0.149, +0.034] | -0.152 [-0.308, +0.032] (NOT_READ) | -0.327 [-0.553, -0.040] |
| CSC c_csc_graded | FREE-MATCHED ALIGN | -0.123 [-0.207, -0.038] | -0.068 [-0.140, +0.011] | -0.065 [-0.193, +0.062] (NOT_READ) | -0.170 [-0.351, +0.013] |
| CSC c_csc_graded | c_score_align (9 free peers, ALIGN) | -0.166 [-0.279, -0.066] | -0.088 [-0.164, -0.007] | -0.091 [-0.226, +0.033] (NOT_READ) | -0.278 [-0.493, -0.060] |
| CSC c_csc_graded | p_peer_text | -0.191 [-0.285, -0.107] | -0.142 [-0.214, -0.065] | -0.155 [-0.294, -0.019] (NOT_READ) | -0.319 [-0.507, -0.142] |
| CSC c_csc_graded | flash-lite judge (disguised) | -0.056 [-0.218, +0.105] | +0.045 [-0.080, +0.181] | -0.106 [-0.342, +0.138] (NOT_READ) | -0.151 [-0.421, +0.182] |
| CSC c_csc_graded | flash-lite judge (original) | +0.059 [-0.057, +0.175] | +0.112 [-0.009, +0.225] | -0.005 [-0.202, +0.203] (NOT_READ) | +0.039 [-0.146, +0.235] |
| CSC c_csc_graded | gpt-4.1-nano judge (original) | +0.017 [-0.147, +0.174] | +0.094 [-0.043, +0.229] | -0.098 [-0.349, +0.198] (NOT_READ) | -0.070 [-0.360, +0.231] |
| CSC c_csc_graded | round-trip NLI (min) | -0.013 [-0.200, +0.171] | +0.087 [-0.076, +0.248] | -0.083 [-0.275, +0.130] (NOT_READ) | -0.073 [-0.433, +0.295] |
| CSC c_csc_graded | self-consistency sc5 | -0.050 [-0.180, +0.086] | +0.014 [-0.114, +0.147] | -0.003 [-0.171, +0.174] (NOT_READ) | -0.170 [-0.406, +0.091] |
| CSC c_csc_graded | S4_full stack (OOF) | -0.128 [-0.268, -0.000] | -0.070 [-0.187, +0.055] | -0.178 [-0.398, +0.059] (NOT_READ) | -0.222 [-0.482, +0.033] |
| CSC c_csc_multi | FREE-MATCHED exact (same 3 families, no signature) | -0.169 [-0.301, -0.041] | -0.067 [-0.153, +0.029] | -0.122 [-0.273, +0.055] (NOT_READ) | -0.349 [-0.575, -0.059] |
| CSC c_csc_multi | FREE-MATCHED ALIGN | -0.130 [-0.219, -0.040] | -0.074 [-0.154, +0.012] | -0.035 [-0.145, +0.090] (NOT_READ) | -0.192 [-0.370, -0.013] |
| CSC c_csc_multi | c_score_align (9 free peers, ALIGN) | -0.173 [-0.288, -0.072] | -0.093 [-0.175, -0.012] | -0.060 [-0.176, +0.048] (NOT_READ) | -0.299 [-0.517, -0.076] |
| CSC c_csc_multi | p_peer_text | -0.198 [-0.295, -0.110] | -0.147 [-0.225, -0.065] | -0.125 [-0.248, +0.001] (NOT_READ) | -0.340 [-0.516, -0.169] |
| CSC c_csc_multi | flash-lite judge (disguised) | -0.063 [-0.225, +0.096] | +0.040 [-0.083, +0.176] | -0.076 [-0.296, +0.160] (NOT_READ) | -0.173 [-0.430, +0.151] |
| CSC c_csc_multi | flash-lite judge (original) | +0.052 [-0.063, +0.169] | +0.107 [-0.016, +0.223] | +0.025 [-0.160, +0.222] (NOT_READ) | +0.017 [-0.164, +0.221] |
| CSC c_csc_multi | gpt-4.1-nano judge (original) | +0.010 [-0.161, +0.170] | +0.089 [-0.054, +0.224] | -0.068 [-0.307, +0.213] (NOT_READ) | -0.091 [-0.394, +0.226] |
| CSC c_csc_multi | round-trip NLI (min) | -0.020 [-0.205, +0.160] | +0.082 [-0.075, +0.245] | -0.053 [-0.241, +0.169] (NOT_READ) | -0.095 [-0.446, +0.274] |
| CSC c_csc_multi | self-consistency sc5 | -0.057 [-0.188, +0.077] | +0.009 [-0.114, +0.145] | +0.027 [-0.129, +0.190] (NOT_READ) | -0.192 [-0.425, +0.077] |
| CSC c_csc_multi | S4_full stack (OOF) | -0.135 [-0.279, -0.005] | -0.075 [-0.198, +0.051] | -0.148 [-0.359, +0.087] (NOT_READ) | -0.243 [-0.498, +0.013] |
| HYB_MEAN | FREE-MATCHED exact (same 3 families, no signature) | -0.061 [-0.187, +0.046] | +0.002 [-0.089, +0.089] | -0.093 [-0.255, +0.088] (NOT_READ) | -0.194 [-0.427, +0.057] |
| HYB_MEAN | FREE-MATCHED ALIGN | -0.022 [-0.094, +0.049] | -0.004 [-0.068, +0.066] | -0.006 [-0.108, +0.114] (NOT_READ) | -0.037 [-0.188, +0.109] |
| HYB_MEAN | c_score_align (9 free peers, ALIGN) | -0.065 [-0.157, -0.003] | -0.024 [-0.067, +0.018] | -0.032 [-0.101, +0.038] (NOT_READ) | -0.145 [-0.339, -0.001] |
| HYB_MEAN | p_peer_text | -0.090 [-0.170, -0.028] | -0.078 [-0.145, -0.019] | -0.096 [-0.191, +0.001] (NOT_READ) | -0.186 [-0.367, -0.029] |
| HYB_MEAN | flash-lite judge (disguised) | +0.044 [-0.107, +0.186] | +0.109 [-0.024, +0.235] | -0.047 [-0.264, +0.212] (NOT_READ) | -0.018 [-0.280, +0.293] |
| HYB_MEAN | flash-lite judge (original) | +0.160 [+0.049, +0.266] | +0.176 [+0.057, +0.289] | +0.054 [-0.099, +0.232] (NOT_READ) | +0.172 [-0.014, +0.370] |
| HYB_MEAN | gpt-4.1-nano judge (original) | +0.117 [-0.044, +0.255] | +0.158 [+0.028, +0.280] | -0.039 [-0.268, +0.241] (NOT_READ) | +0.063 [-0.244, +0.353] |
| HYB_MEAN | round-trip NLI (min) | +0.087 [-0.095, +0.261] | +0.152 [-0.023, +0.315] | -0.024 [-0.223, +0.222] (NOT_READ) | +0.060 [-0.261, +0.377] |
| HYB_MEAN | self-consistency sc5 | +0.051 [-0.073, +0.169] | +0.078 [-0.041, +0.204] | +0.056 [-0.090, +0.221] (NOT_READ) | -0.037 [-0.274, +0.239] |
| HYB_MEAN | S4_full stack (OOF) | -0.028 [-0.155, +0.090] | -0.006 [-0.124, +0.110] | -0.119 [-0.317, +0.128] (NOT_READ) | -0.089 [-0.331, +0.144] |


## T5b. Sensitivity populations: c_csc strat AUROC and paired Δ (DEVELOPMENT E)
# source: results/analysis.json b_GE2, b_MINI200, b_PRIMARY_excl_insufficient

| population | n ERR | n COR | c_csc strat AUROC | comparator | Δ strat |
|---|---|---|---|---|---|
| GE2 | 232 | 243 | 0.618 [0.513, 0.728] | FREE-MATCHED exact (same 3 families, no signature) | -0.178 [-0.300, -0.056] |
| GE2 | 232 | 243 | 0.618 [0.513, 0.728] | FREE-MATCHED ALIGN | -0.105 [-0.198, -0.014] |
| GE2 | 232 | 243 | 0.618 [0.513, 0.728] | c_score_align (9 free peers, ALIGN) | -0.151 [-0.256, -0.054] |
| GE2 | 232 | 243 | 0.618 [0.513, 0.728] | flash-lite judge (disguised) | -0.034 [-0.183, +0.111] |
| MINI200 | 120 | 60 | 0.630 [0.521, 0.730] | FREE-MATCHED exact (same 3 families, no signature) | -0.058 [-0.150, +0.038] |
| MINI200 | 120 | 60 | 0.630 [0.521, 0.730] | FREE-MATCHED ALIGN | -0.084 [-0.172, +0.006] |
| MINI200 | 120 | 60 | 0.630 [0.521, 0.730] | c_score_align (9 free peers, ALIGN) | -0.094 [-0.181, -0.000] |
| MINI200 | 120 | 60 | 0.630 [0.521, 0.730] | flash-lite judge (disguised) | -0.012 [-0.132, +0.114] |
| PRIMARY_excl_insufficient | 196 | 158 | 0.614 [0.493, 0.736] | FREE-MATCHED exact (same 3 families, no signature) | -0.156 [-0.290, -0.031] |
| PRIMARY_excl_insufficient | 196 | 158 | 0.614 [0.493, 0.736] | FREE-MATCHED ALIGN | -0.117 [-0.205, -0.029] |
| PRIMARY_excl_insufficient | 196 | 158 | 0.614 [0.493, 0.736] | c_score_align (9 free peers, ALIGN) | -0.160 [-0.275, -0.064] |


## T6. $0 FULL population: matched 3-family free peers scored exactly vs with ALIGN (DEVELOPMENT E)
# source: results/analysis.json b_FULL_free.metrics

| metric | R_AB strat | R_AB pooled | long strat | L25 pooled |
|---|---|---|---|---|
| FREE-MATCHED exact (same 3 families, no signature) | 0.673 [0.636, 0.708] | 0.721 [0.681, 0.756] | 0.654 [0.616, 0.689] | 0.594 [0.537, 0.656] |
| FREE-MATCHED ALIGN | 0.732 [0.698, 0.764] | 0.775 [0.737, 0.808] | 0.733 [0.697, 0.767] | 0.666 [0.604, 0.723] |
| FREE-MATCHED graded (identity) | 0.677 [0.640, 0.711] | 0.728 [0.689, 0.763] | 0.658 [0.620, 0.693] | 0.607 [0.544, 0.665] |
| c_score_align (9 free peers, ALIGN) | 0.741 [0.705, 0.775] | 0.782 [0.745, 0.816] | 0.741 [0.705, 0.777] | 0.712 [0.649, 0.768] |
| flash-lite judge (disguised) | 0.642 [0.607, 0.676] | 0.696 [0.655, 0.733] | 0.625 [0.589, 0.659] | 0.643 [0.579, 0.704] |
| p_peer_text | 0.753 [0.720, 0.784] | 0.790 [0.752, 0.825] | 0.757 [0.725, 0.790] | 0.755 [0.704, 0.803] |


Frontier-judge frame ∩ PRIMARY (n_err 18, n_cor 18): c_csc 0.648 [0.454, 0.820] (NOT_READ); frontier judge 0.744 [0.571, 0.888] (NOT_READ); Δ -0.096 [-0.239, +0.028] (NOT_READ) (# source: results/analysis.json b_frontier_frame)


## T7. Nesting: OOF logistic stacks refit on folds_E within PRIMARY rows (DEVELOPMENT E)
# source: results/analysis.json c_nesting_PRIMARY.nested

| comparison | Δ strat AUROC [CI] | Δ pooled AUROC [CI] |
|---|---|---|
| S4_full+c_csc - S4_full | +0.006 [-0.013, +0.025] | +0.006 [-0.005, +0.018] |
| S4_full+c_csc_graded - S4_full | +0.008 [-0.012, +0.028] | +0.007 [-0.005, +0.019] |
| S4_full+c_csc_multi - S4_full | +0.003 [-0.014, +0.019] | +0.003 [-0.006, +0.012] |
| S4_full+c_free_exact - S4_full | +0.056 [+0.008, +0.122] | +0.031 [+0.008, +0.059] |
| S4_full+c_score_align - S4_full | +0.032 [-0.011, +0.076] | +0.023 [+0.001, +0.046] |
| S4_full+c_score_align+c_csc - S4_full+c_score_align | -0.004 [-0.014, +0.004] | -0.002 [-0.008, +0.002] |
| S4_full+c_score_align+c_csc_graded - S4_full+c_score_align | -0.001 [-0.005, +0.001] | -0.001 [-0.003, +0.001] |


S4_full refit on PRIMARY vs T1's S4_full_oof: corr 0.889; refit strat AUROC 0.742 [0.623, 0.839], T1 column on same rows 0.736 [0.635, 0.826] (# source: results/analysis.json c_nesting_PRIMARY)


## T8. Where d comes from: free-peer disagreements with CORRECT candidates, by pairs_E verdicts (DEVELOPMENT E)
# source: results/analysis.json d_where_*

| set | rows | disagreement class | count | share |
|---|---|---|---|---|
| d_where_FULL_free_align_flagged_CORRECT | 283 | structural (no vocabulary map makes them equivalent) | 653 | 0.806 |
| d_where_FULL_free_align_flagged_CORRECT | 283 | align_equivalent (vocabulary/granularity resolved by the aligner) | 130 | 0.160 |
| d_where_FULL_free_align_flagged_CORRECT | 283 | pair_missing_or_peer_unparseable | 39 | – |
| d_where_FULL_free_align_flagged_CORRECT | 283 | vocabulary-only (NF/HYB name-free equivalent, ALIGN not) | 27 | 0.033 |
| d_where_FULL_free_align_flagged_CORRECT | 283 | ROWS whose every free-peer disagreement is vocabulary-resolvable | 2 | 0.007 |
| d_where_FULL_free_exact_flagged_CORRECT | 504 | align_equivalent (vocabulary/granularity resolved by the aligner) | 649 | 0.446 |
| d_where_FULL_free_exact_flagged_CORRECT | 504 | structural (no vocabulary map makes them equivalent) | 774 | 0.532 |
| d_where_FULL_free_exact_flagged_CORRECT | 504 | pair_missing_or_peer_unparseable | 57 | – |
| d_where_FULL_free_exact_flagged_CORRECT | 504 | vocabulary-only (NF/HYB name-free equivalent, ALIGN not) | 32 | 0.022 |
| d_where_FULL_free_exact_flagged_CORRECT | 504 | ROWS whose every free-peer disagreement is vocabulary-resolvable | 102 | 0.202 |
| d_where_PRIMARY_free_flagged_csc_endorsed | 13 | structural (no vocabulary map makes them equivalent) | 29 | 0.744 |
| d_where_PRIMARY_free_flagged_csc_endorsed | 13 | align_equivalent (vocabulary/granularity resolved by the aligner) | 10 | 0.256 |
| d_where_PRIMARY_free_flagged_csc_endorsed | 13 | ROWS whose every free-peer disagreement is vocabulary-resolvable | 0 | 0.000 |


## T8b. CORRECT rows still flagged by CSC: automated tags (all such rows; the planned 60-row sample exceeds their number) (DEVELOPMENT E)
# source: results/analysis.json d_tagging; results/d_tagging_rows.json

| tag | count |
|---|---|
| MULTI_OP_DIFF | 7 |
| READING_CHOICE | 4 |
| PEER_SCATTER | 10 |
| SINGLE_OP_DIFF | 1 |


Tagging rule (written before tagging):
```
Automated tagging rule for CORRECT rows still flagged by CSC (written before tagging; applied mechanically):
 1 READING_CHOICE  : the candidate is z3-equivalent (same vocabulary) to some peer's alt_fol (a second legitimate reading was produced)
 2 PEER_SCATTER    : no two peers agree with each other (no peer majority) -> peers diverge among themselves
 3 GRANULARITY     : the candidate and the peer-majority formula are eqmv-equivalent (ALIGN/granularity bridge) but not same-vocabulary equivalent
 4 SINGLE_OP_DIFF  : the typed same-vocabulary repair from candidate to peer majority is one op (peer error OR label error; not separable without a human)
 5 MULTI_OP_DIFF   : otherwise (compound structural difference)
```


## T8c. Measured CSC d / e vs the sibling evaluation's pre-registered prediction (read only after results/d_measured.json was written) (DEVELOPMENT E)
# source: results/analysis.json d_vs_sibling_prediction; iter_4/gen_art_evaluation_3/results/part1.json (read-only)

| quantity | value |
|---|---|
| sibling d_floor_pred, 3-family pool (FULL population) | 0.402 [0.33647929249783104, 0.471449720918307] |
| sibling e_ceiling_pred, 3-family pool | 0.162 |
| measured d, CSC (PRIMARY) | 0.139 |
| measured e, CSC (PRIMARY) | 0.459 |
| measured d_CSC / d_FREE_exact on PRIMARY | 0.431 |
| predicted d_floor / d_FREE_exact on FULL | 0.689 |
| note | sibling predictions are for the FULL R_AB population; CSC was measured on PRIMARY, where the matched free peers scored exactly already have d = 0.323 (FULL: 0.583), so compare RATIOS d_CSC / d_FREE_exact, not levels |


## T9. Anchoring on real errors: e by error class, PRIMARY (DEVELOPMENT E)
# source: results/analysis.json e_anchoring_by_error_class.PRIMARY

| error class | n | e CSC | e FREE exact | e FREE ALIGN | e END_MAJ-9 | Δe CSC − FREE ALIGN |
|---|---|---|---|---|---|---|
| ADD | 96 | 0.490 [0.345, 0.615] | 0.135 [0.046, 0.254] | 0.375 [0.237, 0.516] | 0.250 [0.100, 0.389] | +0.115 [+0.000, +0.235] |
| COMPOUND | 103 | 0.282 [0.182, 0.382] | 0.107 [0.043, 0.183] | 0.184 [0.103, 0.282] | 0.039 [0.000, 0.091] | +0.097 [-0.012, +0.213] |
| DROP | 142 | 0.472 [0.352, 0.578] | 0.169 [0.082, 0.266] | 0.380 [0.254, 0.500] | 0.232 [0.104, 0.361] | +0.092 [-0.000, +0.194] |
| MEANING_RENAME-type (MEANING_RENAME op or tier-B VOCAB_GRAN) | 28 | 0.821 [0.600, 0.947] | 0.036 [0.000, 0.143] | 0.750 [0.481, 0.923] | 0.536 [0.182, 0.786] | +0.071 [-0.083, +0.269] (NOT_READ) |
| polarity(NEG/REV/QUANT) | 30 | 0.200 [0.048, 0.381] | 0.133 [0.000, 0.286] | 0.200 [0.034, 0.385] | 0.000 [0.000, 0.000] | +0.000 [-0.214, +0.208] (NOT_READ) |
| structural(CONN/RESTR/BIND/MOVE/SWAP/SCOPE/UNGLUE) | 131 | 0.336 [0.230, 0.432] | 0.153 [0.070, 0.241] | 0.282 [0.184, 0.380] | 0.122 [0.040, 0.210] | +0.053 [-0.043, +0.144] |


## T9b. e by error class, FULL, free peers ($0) (DEVELOPMENT E)
# source: results/analysis.json e_anchoring_by_error_class.FULL

| error class | n | e FREE exact | e FREE ALIGN | e END_MAJ-9 |
|---|---|---|---|---|
| ADD | 1044 | 0.144 [0.103, 0.187] | 0.282 [0.227, 0.335] | 0.133 [0.085, 0.185] |
| COMPOUND | 1148 | 0.118 [0.085, 0.154] | 0.175 [0.139, 0.216] | 0.024 [0.009, 0.045] |
| DROP | 1402 | 0.127 [0.092, 0.164] | 0.280 [0.231, 0.329] | 0.133 [0.090, 0.180] |
| MEANING_RENAME-type (MEANING_RENAME op or tier-B VOCAB_GRAN) | 221 | 0.104 [0.052, 0.166] | 0.624 [0.507, 0.730] | 0.448 [0.320, 0.573] |
| polarity(NEG/REV/QUANT) | 434 | 0.120 [0.075, 0.168] | 0.173 [0.121, 0.227] | 0.039 [0.009, 0.081] |
| structural(CONN/RESTR/BIND/MOVE/SWAP/SCOPE/UNGLUE) | 1302 | 0.117 [0.085, 0.151] | 0.210 [0.170, 0.256] | 0.072 [0.041, 0.107] |


## T10. Error typing on R_A errors with 1–2 repair ops, PRIMARY (n = 65) (DEVELOPMENT E)
# source: results/analysis.json f_typing_PRIMARY

| predictor | exact op-set accuracy [CI] | coarse-class accuracy | share typed |
|---|---|---|---|
| own_majority | 0.185 [0.068, 0.333] | 0.246 | 0.600 |
| free_majority | 0.200 [0.083, 0.347] | 0.308 | 0.723 |
| majority class (ADD+DROP) | 0.262 | – | – |
| chance (1/#classes) | 0.071 | – | – |
| iteration-2 medoid typing (reference) | 0.371 | – | – |


## T11. Cost per candidate (DEVELOPMENT E)
# source: results/analysis.json g_cost

| quantity | value |
|---|---|
| FULL $/candidate, undeduped (sum of its 3 peer calls) | 5.25e-04 |
| FULL $/candidate, dedup-apportioned | 2.76e-04 |
| MARGINAL z3 CPU s/candidate (mean / p95) | 0.024 / 0.044 |
| flash-lite judge $/item (T1) | 4.88e-05 |
| free 9-peer pool $/item FULL (T1) | 1.21e-04 |
| $/call by model | 4 pool models: 1.41e-05, openai/gpt-4.1-mini: 3.49e-04, deepseek/deepseek-v3.2: 1.53e-04, microsoft/phi-4: 7.60e-05, qwen/qwen3-235b-a22b-2507: 7.27e-05 |
| G5 (FULL <= $0.002) | True |
| this artifact's total API spend | $0.1082 |


## T12. Complexity curves, strat AUROC per bin, PRIMARY (DEVELOPMENT E)
# source: results/analysis.json h_complexity_PRIMARY

| variable | bin | n ERR | n COR | CSC | FREE exact | FREE ALIGN | c_score_align | flash-lite disg |
|---|---|---|---|---|---|---|---|---|
| words_t | T1 | 58 | 118 | 0.562 [0.369, 0.796] | 0.811 [0.673, 0.914] | 0.724 [0.587, 0.916] | 0.806 [0.684, 0.942] | 0.732 [0.592, 0.858] |
| words_t | T2 | 86 | 32 | 0.670 [0.450, 0.840] (NOT_READ) | 0.718 [0.537, 0.858] (NOT_READ) | 0.732 [0.554, 0.873] (NOT_READ) | 0.695 [0.505, 0.858] (NOT_READ) | 0.483 [0.308, 0.647] (NOT_READ) |
| words_t | T3 | 52 | 8 | 0.409 [0.278, 0.600] (NOT_READ) | 0.591 [0.403, 0.825] (NOT_READ) | 0.511 [0.328, 0.782] (NOT_READ) | 0.601 [0.449, 0.794] (NOT_READ) | 0.844 [0.582, 0.977] (NOT_READ) |
| nq_bin | 0-1 | 152 | 138 | 0.623 [0.466, 0.783] | 0.783 [0.671, 0.867] | 0.749 [0.633, 0.863] | 0.804 [0.702, 0.891] | 0.691 [0.586, 0.795] |
| nq_bin | 2 | 18 | 8 | 0.578 [0.000, 0.750] (NOT_READ) | 0.716 [0.000, 1.000] (NOT_READ) | 0.627 [0.000, 0.933] (NOT_READ) | 0.902 [0.000, 1.000] (NOT_READ) | 0.667 [0.000, 1.000] (NOT_READ) |
| nq_bin | 3+ | 26 | 12 | 0.596 [0.361, 0.908] (NOT_READ) | 0.870 [0.662, 0.974] (NOT_READ) | 0.686 [0.432, 0.996] (NOT_READ) | 0.625 [0.368, 0.992] (NOT_READ) | 0.580 [0.293, 0.878] (NOT_READ) |
| depth_bin | 0-1 | 15 | 44 | 0.402 [0.163, 0.655] (NOT_READ) | 0.962 [0.848, 1.000] (NOT_READ) | 0.584 [0.446, 1.000] (NOT_READ) | 0.828 [0.604, 1.000] (NOT_READ) | 0.821 [0.583, 1.000] (NOT_READ) |
| depth_bin | 2 | 7 | 19 | 0.416 [0.083, 1.000] (NOT_READ) | 0.900 [0.667, 1.000] (NOT_READ) | 0.958 [0.740, 1.000] (NOT_READ) | 0.884 [0.511, 1.000] (NOT_READ) | 0.653 [0.267, 0.962] (NOT_READ) |
| depth_bin | 3+ | 174 | 95 | 0.676 [0.566, 0.778] | 0.735 [0.637, 0.823] | 0.739 [0.632, 0.837] | 0.759 [0.653, 0.856] | 0.627 [0.528, 0.715] |
| ncond_bin | 0-1 | 25 | 77 | 0.392 [0.215, 0.826] (NOT_READ) | 0.843 [0.640, 0.941] (NOT_READ) | 0.615 [0.483, 0.983] (NOT_READ) | 0.789 [0.619, 1.000] (NOT_READ) | 0.790 [0.572, 0.985] (NOT_READ) |
| ncond_bin | 2 | 14 | 21 | 0.787 [0.205, 1.000] (NOT_READ) | 0.897 [0.251, 1.000] (NOT_READ) | 0.895 [0.189, 1.000] (NOT_READ) | 0.809 [0.000, 1.000] (NOT_READ) | 0.748 [0.448, 0.938] (NOT_READ) |
| ncond_bin | 3 | 35 | 27 | 0.767 [0.543, 0.968] (NOT_READ) | 0.713 [0.537, 0.942] (NOT_READ) | 0.696 [0.511, 0.968] (NOT_READ) | 0.804 [0.593, 0.993] (NOT_READ) | 0.495 [0.336, 0.616] (NOT_READ) |
| ncond_bin | 4+ | 122 | 33 | 0.597 [0.458, 0.736] (NOT_READ) | 0.668 [0.559, 0.781] (NOT_READ) | 0.676 [0.525, 0.812] (NOT_READ) | 0.680 [0.533, 0.810] (NOT_READ) | 0.645 [0.509, 0.764] (NOT_READ) |
| exc_bin | but_not | 9 | 2 | 0.938 [0.900, 1.000] (NOT_READ) | 0.375 [0.150, 0.750] (NOT_READ) | 1.000 [1.000, 1.000] (NOT_READ) | 1.000 [1.000, 1.000] (NOT_READ) | 0.500 [0.000, 0.667] (NOT_READ) |
| exc_bin | except | 3 | 11 | 1.000 [1.000, 1.000] (NOT_READ) | 0.682 [0.375, 0.792] (NOT_READ) | 0.682 [0.375, 0.792] (NOT_READ) | 1.000 [1.000, 1.000] (NOT_READ) | 0.636 [0.444, 0.711] (NOT_READ) |
| exc_bin | none | 146 | 111 | 0.534 [0.392, 0.686] | 0.779 [0.683, 0.860] | 0.701 [0.587, 0.813] | 0.738 [0.628, 0.834] | 0.660 [0.539, 0.780] |
| exc_bin | other_exc | 0 | 1 | – | – | – | – | – |
| exc_bin | unless | 25 | 29 | 0.725 [0.448, 0.958] (NOT_READ) | 0.770 [0.399, 0.973] (NOT_READ) | 0.775 [0.455, 1.000] (NOT_READ) | 0.800 [0.552, 1.000] (NOT_READ) | 0.741 [0.484, 0.892] (NOT_READ) |
| exc_bin | without | 13 | 4 | 0.519 [0.271, 0.909] (NOT_READ) | 0.625 [0.500, 1.000] (NOT_READ) | 0.625 [0.247, 1.000] (NOT_READ) | 0.654 [0.286, 1.000] (NOT_READ) | 0.654 [0.125, 0.925] (NOT_READ) |


## T13. M3: length slope of decision correctness, consensus − judge (judge binarised at the consensus flag rate) (DEVELOPMENT E)
# source: results/analysis.json h_M3

| comparison | n | flag rate | acc consensus | acc judge | spec 1 bootstrap Δslope [CI] | spec 2 stacked-GEE interaction [CI] |
|---|---|---|---|---|---|---|
| CSC_vs_flashlite_disg_PRIMARY | 354 | 0.362 | 0.684 | 0.650 | -0.232 [-0.770, -0.023] | -0.351 [-0.694, -0.009] |
| FREEalign_vs_flashlite_disg_PRIMARY | 354 | 0.444 | 0.720 | 0.681 | -0.176 [-0.497, +0.314] | -0.065 [-0.443, +0.312] |
| END_MAJ9_vs_flashlite_disg_PRIMARY | 354 | 0.593 | 0.729 | 0.718 | +0.184 [-0.295, +0.504] | +0.115 [-0.273, +0.503] |


## T14. System-level Kendall τ-b (mean score vs error rate over system×variant rows) (DEVELOPMENT E)
# source: results/analysis.json i_system_level_*

| population | metric | τ-b | p | n systems |
|---|---|---|---|---|
| PRIMARY | CSC c_csc | 0.256 | 0.252 | 13 |
| PRIMARY | CSC c_csc_graded | 0.077 | 0.765 | 13 |
| PRIMARY | FREE-MATCHED exact (same 3 families, no signature) | 0.385 | 0.076 | 13 |
| PRIMARY | FREE-MATCHED ALIGN | 0.462 | 0.030 | 13 |
| PRIMARY | c_score_align (9 free peers, ALIGN) | 0.513 | 0.015 | 13 |
| PRIMARY | flash-lite judge (disguised) | 0.359 | 0.100 | 13 |
| FULL | FREE-MATCHED exact (same 3 families, no signature) | 0.538 | 0.010 | 13 |
| FULL | FREE-MATCHED ALIGN | 0.718 | 0.000 | 13 |
| FULL | c_score_align (9 free peers, ALIGN) | 0.692 | 0.001 | 13 |
| FULL | flash-lite judge (disguised) | 0.564 | 0.007 | 13 |


## T15. Placebos and rename (DEVELOPMENT E)
# source: results/analysis.json j_placebo, k_rename

| check | value |
|---|---|
| shuffled labels: pooled AUROC of c_csc (PRIMARY) | 0.483 |
| shuffled labels: strat AUROC of c_csc | 0.508 |
| random-sentence-signature PLACEBO arm | NOT_RUN (platform budget refusal; 0 peer calls) |
| CSC RENAME_SYN / RENAME_NONCE (G3-E) | NOT_RUN |
| $0: 9-peer c_score_align re-derived on SYN-renamed CORRECT rows (n = 348): FA base | 0.595 |
|   FA after RENAME_SYN | 0.868 |
|   ΔFA [CI] | +0.273 [+0.164, +0.384] |
|   re-derived base vs frozen c_score_align (corr) | 1.000000 |


EXPLORATORY K4 (incidental coverage, n_err 5, n_cor 7, never gated): K4 strat AUROC 1.000 [1.000, 1.000] (NOT_READ); CSC same rows 1.000 [1.000, 1.000] (NOT_READ); d K4 0.000 [0.000, 0.000] vs CSC 0.000 [0.000, 0.000] (# source: results/analysis.json exploratory_K4)


EXPLORATORY OTHER (incidental coverage, n_err 25, n_cor 3, never gated): OTHER strat AUROC 0.500 [0.500, 0.500] (NOT_READ); CSC same rows 0.375 [0.100, 1.000] (NOT_READ); d OTHER 1.000 [1.000, 1.000] vs CSC 0.000 [0.000, 0.000] (# source: results/analysis.json exploratory_OTHER)


## T17. POST-HOC sensitivity: phi-4 exemplar leakage removed symmetrically from CSC and FREE-MATCHED peers, PRIMARY (DEVELOPMENT E)
# source: results/posthoc_phi_contamination.json (src/posthoc_contam.py)

| score / paired Δ | strat AUROC or Δ [CI] | e | d |
|---|---|---|---|
| c_csc | 0.614 [0.493, 0.736] | 0.459 [0.360, 0.549] | 0.139 [0.075, 0.234] |
| c_csc_clean | 0.639 [0.529, 0.744] | 0.546 [0.455, 0.631] | 0.108 [0.050, 0.188] |
| c_free_exact | 0.770 [0.686, 0.844] | 0.173 [0.094, 0.257] | 0.323 [0.203, 0.473] |
| c_free_exact_clean | 0.770 [0.686, 0.843] | 0.179 [0.100, 0.262] | 0.272 [0.171, 0.408] |
| T1__c_score_align | 0.774 [0.682, 0.857] | – | – |
| c_csc_clean - c_free_exact_clean | -0.132 [-0.251, -0.023] |  |  |
| c_csc_clean - T1__c_score_align | -0.135 [-0.233, -0.046] |  |  |
| c_csc_clean - c_csc | +0.025 [-0.013, +0.071] |  |  |


phi-4 copied the last few-shot exemplar (CanMake/Baker) in 58 CSC calls (routes {'microsoft/phi-4|reask_json_fenced': 6, 'microsoft/phi-4|json_fenced': 52}); peers dropped on PRIMARY: {'OWN': 88, 'FREE': 21}.


## T16. Gate file summary (PROVISIONAL, PRIMARY subset) (DEVELOPMENT E)
# source: csc_gate_E.json

| variant | G1 | G2 | G3-E | G5 | strat AUROC R_AB |
|---|---|---|---|---|---|
| c_csc | d 0.139 [0.075, 0.234], slope 1.251 → FAIL | R_AB part FAIL; L25 NOT_READ (cell < 50/50) | NOT_RUN | 5.25e-04 → PASS | 0.614 [0.493, 0.736] |
| c_csc_graded | d 0.089 [0.037, 0.163], slope 1.614 → FAIL | R_AB part FAIL; L25 NOT_READ (cell < 50/50) | NOT_RUN | 5.25e-04 → PASS | 0.608 [0.487, 0.734] |
| c_csc_multi | d 0.127 [0.067, 0.213], slope 1.218 → FAIL | R_AB part FAIL; L25 NOT_READ (cell < 50/50) | NOT_RUN | 5.25e-04 → PASS | 0.601 [0.480, 0.720] |
| HYB_MEAN | d 0.190 [0.110, 0.307], slope 1.154 → FAIL | R_AB part FAIL; L25 NOT_READ (cell < 50/50) | NOT_RUN | 6.46e-04 → PASS | 0.709 [0.586, 0.817] |
| c_csc_k4 | NOT_READ (incidental coverage only) | NOT_READ | NOT_RUN | NOT_READ | – |
