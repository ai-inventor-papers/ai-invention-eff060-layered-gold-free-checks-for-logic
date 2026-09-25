# E2-B tables (every row: value — source file :: key)

## 0. Status

- label regime: NO_PANEL_TIER_A_UNAUDITED — analysis/analysis_E2B.json :: label_regime
- completed label batches (panel end to end): [] — e2b/progress.jsonl
- run-budget stop: panel records moved aside from incomplete batches {'panel_heldout.jsonl': 14, 'panel_heldout_adj.jsonl': 0} — e2b/budget_stop_batches_complete.json
- label counts (all LLM rows): {'UNRESOLVED': 3151, 'UNPARSEABLE': 467, 'CORRECT': 48, 'ERROR': 334} — analysis/analysis_E2B.json :: label_counts
- tier counts: {'none': 3151, '-': 467, 'A_unaudited_ref': 382} — analysis/analysis_E2B.json :: tier_counts

## 1. Sample (selection)

| quantity | value | source |
|---|---|---|
| n | 400 | e2b/census_E2B.json :: E2B.n |
| from_E2_surplus | 98 | e2b/census_E2B.json :: E2B.from_E2_surplus |
| continuation | 302 | e2b/census_E2B.json :: E2B.continuation |
| word_bin_counts | {'25-29': 374, '30-34': 26} | e2b/census_E2B.json :: E2B.word_bin_counts |
| share_25_29 | 0.935 | e2b/census_E2B.json :: E2B.share_25_29 |
| mean_words | 26.82 | e2b/census_E2B.json :: E2B.mean_words |
| mean_n_conditions | 4.66 | e2b/census_E2B.json :: E2B.mean_n_conditions |
| E2 pool reproduced (sha256 98cdccff…) | True | e2b/census_E2B.json :: e2_reproduction.pool_ok |
| collisions with E / E2 (all must be 0) | {'E700_text': 0, 'E700_12gram': 0, 'E2_nonsurplus_id': 0, 'E2_nonsurplus_text': 0, 'E2_nonsurplus_12gram': 0, 'within_E2B_12gram': 0} | e2b/census_E2B.json :: collision_checks_all_zero |
| supply remaining after E2-B + reserve | {'25-29': 244, '>=30': 2} | e2b/census_E2B.json |

## 2. Testability (E's rule: >=50 ERROR, >=50 CORRECT, >=25 sentences each)

| cell | regime | CORRECT | ERROR | testable | source |
|---|---|---|---|---|---|
| L25 | R_AB | 0 | 0 | False | e2b/testability_E2B.json :: cells.L25.R_AB |
| L25 | R_A | 0 | 0 | False | e2b/testability_E2B.json :: cells.L25.R_A |
| L25 | R_VEX | 0 | 0 | False | e2b/testability_E2B.json :: cells.L25.R_VEX |
| L25 | R_A_UNAUDITED | 48 | 334 | False | e2b/testability_E2B.json :: cells.L25.R_A_UNAUDITED |
| L25_bin_25-29 | R_AB | 0 | 0 | False | e2b/testability_E2B.json :: cells.L25_bin_25-29.R_AB |
| L25_bin_25-29 | R_A | 0 | 0 | False | e2b/testability_E2B.json :: cells.L25_bin_25-29.R_A |
| L25_bin_25-29 | R_VEX | 0 | 0 | False | e2b/testability_E2B.json :: cells.L25_bin_25-29.R_VEX |
| L25_bin_25-29 | R_A_UNAUDITED | 47 | 325 | False | e2b/testability_E2B.json :: cells.L25_bin_25-29.R_A_UNAUDITED |
| L25_bin_30-34 | R_AB | 0 | 0 | False | e2b/testability_E2B.json :: cells.L25_bin_30-34.R_AB |
| L25_bin_30-34 | R_A | 0 | 0 | False | e2b/testability_E2B.json :: cells.L25_bin_30-34.R_A |
| L25_bin_30-34 | R_VEX | 0 | 0 | False | e2b/testability_E2B.json :: cells.L25_bin_30-34.R_VEX |
| L25_bin_30-34 | R_A_UNAUDITED | 1 | 9 | False | e2b/testability_E2B.json :: cells.L25_bin_30-34.R_A_UNAUDITED |

## 3. Confirmatory E2-B cell (L25_E2B, R_AB; strat AUROC by word bin; sentence-cluster bootstrap B=2000)

NOT TESTABLE: {'status': 'NOT_TESTABLE', 'n': 0} — analysis/analysis_E2B.json :: cells.L25_E2B_R_AB

## 3b. EXPLORATORY cell L25_E2B_R_A_UNAUDITED (no-panel regime: CORRECT = z3-equivalent to the UNAUDITED MALLS gold; NOT testable by E's rule; structurally favours agreement-based metrics, see the label-coupling diagnostic)

| metric | strat AUROC [95% CI] | pooled | AUPRC | tie rate | n (ERR/COR) | source |
|---|---|---|---|---|---|---|
| V0 | 0.737 [0.645, 0.827] | 0.742 | 0.949 | 0.065 | 381 (333/48) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.metrics.V0 |
| p_peer_text | 0.655 [0.546, 0.767] | 0.659 | 0.930 | 0.000 | 382 (334/48) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.metrics.p_peer_text |
| c_exact | 0.678 [0.564, 0.779] | 0.675 | 0.921 | 0.324 | 381 (333/48) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.metrics.c_exact |
| V1 | 0.733 [0.654, 0.808] | 0.740 | 0.940 | 0.269 | 381 (333/48) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.metrics.V1 |
| V2 | 0.750 [0.659, 0.838] | 0.755 | 0.954 | 0.030 | 381 (333/48) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.metrics.V2 |
| V3 | 0.761 [0.681, 0.835] | 0.767 | 0.947 | 0.215 | 381 (333/48) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.metrics.V3 |
| V4 | 0.764 [0.666, 0.851] | 0.766 | 0.954 | 0.039 | 381 (333/48) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.metrics.V4 |
| V5 | 0.759 [0.676, 0.834] | 0.763 | 0.944 | 0.249 | 378 (330/48) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.metrics.V5 |
| flashlite_disg | 0.496 [0.356, 0.620] | 0.491 | 0.886 | 0.259 | 276 (245/31) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.metrics.flashlite_disg |
| S4_E2B | 0.498 [0.402, 0.594] | 0.498 | 0.888 | 0.001 | 382 (334/48) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.metrics.S4_E2B |
| S4_E2B_plus_V0 | 0.618 [0.487, 0.754] | 0.622 | 0.908 | 0.000 | 382 (334/48) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.metrics.S4_E2B_plus_V0 |
| l2_bow | 0.603 [0.492, 0.709] | 0.605 | 0.909 | 0.132 | 382 (334/48) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.metrics.l2_bow |
| l3_z3 | 0.442 [0.344, 0.552] | 0.443 | 0.867 | 0.167 | 382 (334/48) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.metrics.l3_z3 |
| pilot_joint_conflict | 0.500 [0.500, 0.500] | 0.500 | 0.874 | 1.000 | 382 (334/48) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.metrics.pilot_joint_conflict |

| delta (paired rows) | point | 95% CI | n (COR, both-class sentences) | source |
|---|---|---|---|---|
| V0 - flashlite_disg | 0.208 | [0.066, 0.363] | 276 (31, 17) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.deltas.V0 - flashlite_disg |
| p_peer_text - flashlite_disg | 0.183 | [0.045, 0.334] | 276 (31, 17) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.deltas.p_peer_text - flashlite_disg |
| S4_E2B_plus_V0 - S4_E2B (nested, B2) | 0.120 | [0.013, 0.237] | 382 (48, 24) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.deltas.S4_E2B_plus_V0 - S4_E2B (nested, B2) |
| V0 - S4_E2B | 0.238 | [0.111, 0.366] | 381 (48, 24) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.deltas.V0 - S4_E2B |
| V1 - V0 (development-only) | -0.004 | [-0.053, 0.051] | 381 (48, 24) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.deltas.V1 - V0 (development-only) |
| V2 - V0 (development-only) | 0.013 | [0.002, 0.026] | 381 (48, 24) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.deltas.V2 - V0 (development-only) |
| V3 - V0 (development-only) | 0.024 | [-0.025, 0.077] | 381 (48, 24) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.deltas.V3 - V0 (development-only) |
| V4 - V0 (development-only) | 0.027 | [-0.026, 0.081] | 381 (48, 24) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.deltas.V4 - V0 (development-only) |
| V5 - V0 (development-only) | 0.022 | [-0.043, 0.085] | 378 (48, 24) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.deltas.V5 - V0 (development-only) |
| c_exact - V0 (development-only) | -0.059 | [-0.163, 0.033] | 381 (48, 24) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.deltas.c_exact - V0 (development-only) |
| V0 - flashlite_disg_vfb (T1 sensitivity: verdict-median fill) | 0.206 | [0.062, 0.363] | 276 (31, 17) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.deltas.V0 - flashlite_disg_vfb (T1 sensitivity: verdict-median fill) |
| V0 - flashlite_disg (judge-ok rows only) | 0.206 | [0.054, 0.362] | 264 (29, 16) | analysis/analysis_E2B.json :: cells.L25_E2B_R_A_UNAUDITED.deltas.V0 - flashlite_disg (judge-ok rows only) |

- label-coupling diagnostic: V0 with gold-equivalent (CORRECT-labelled) peers removed: strat AUROC 0.611 [0.490, 0.738] vs V0 0.737; V0_decoupled − flash-lite disg 0.133 [-0.024, 0.314] — analysis/analysis_E2B.json :: label_coupling_diagnostic


## 4. Verdicts

- **label_regime**: "NO_PANEL_TIER_A_UNAUDITED" — analysis/confirm_verdict_E2B.json :: label_regime
- **analysis_population**: {"population": "R_A_UNAUDITED", "status": "SECONDARY: R_AB not testable (no panel regime); E2's pre-registered no-panel regime 'tier-A-only' (solver vs UNAUDITED MALLS gold; E's panel judged most MALLS gold wrong, so ERROR means 'not equivalent to the gold' and CORRECT means 'z3-equivalent to the gold')", "testable": false, "R_AB": {"ERROR_rows": 0, "CORRECT_rows": 0, "ERROR_sentences": 0, "CORRECT_sentences": 0, "sentences_with_both": 0, "testable": false}, "R_A_UNAUDITED": {"ERROR_rows": 334, "CORRECT_rows": 48, "ERROR_sentences": 138, "CORRECT_sentences": 31, "sentences_with_both": 24, "tes — analysis/confirm_verdict_E2B.json :: analysis_population
- **population**: "L25_E2B R_A_UNAUDITED (LLM systems, tier A_unaudited_ref: solver vs unaudited MALLS gold; SECONDARY)" — analysis/confirm_verdict_E2B.json :: population
- **testable_under_E_rule**: false — analysis/confirm_verdict_E2B.json :: testable_under_E_rule
- **testability_note**: "NOT TESTABLE by E's pre-registered rule in any regime (no panel: R_AB has no CORRECT class; R_A_UNAUDITED has 48 CORRECT rows < 50); the numbers below are EXPLORATORY estimates in a gold-equivalence label regime that structurally favours agreement-based metrics. " — analysis/confirm_verdict_E2B.json :: testability_note
- **B1_V0_minus_flashlite_disg**: {"delta": 0.20828043447594868, "ci": [0.06551897794741308, 0.36291368777804556], "n": 276, "sentences_with_both_classes": 17, "verdict": "NOT TESTABLE (E's rule); exploratory CI > 0", "observed_MDE80_from_bootstrap_SE": 0.21650794499366116, "also_vs": {"V0 - flashlite_orig": {"delta": null, "ci": null}, "V0 - nano_orig": {"delta": null, "ci": null}, "V0 - nano_disg": {"delta": null, "ci": null}, "V0 - costmatched_disg": {"delta": null, "ci": null}, "V0 - costmatched_orig": {"delta": null, "ci": null}, "V0 - frontier_orig (unweighted, subsample rows)": {"delta": null, "ci": null}, "V0 - S4_E2B" — analysis/confirm_verdict_E2B.json :: B1_V0_minus_flashlite_disg
- **B2_nested_S4_plus_V0_minus_S4**: {"delta": 0.11996205181889552, "ci": [0.013260873187767116, 0.23665410026737932], "verdict": "NOT TESTABLE (E's rule); exploratory CI > 0", "substituted": {"judge_local_qwen8b_disg/orig, judge_local_llama8b_disg/orig": "dropped: no GPU on this machine (4 CPUs, no CUDA); exp-6 rule", "rt_nli_* / rt_embed_cos (API and local round trip)": "dropped: NLI/embedding models need a GPU; no local counterpart available", "sc5_* (API and local self-consistency)": "dropped: needs 5 extra samples per sentence + a local model; not in the E2-B budget", "pilot_dangling / pilot_rerun_jacc / pilot_undeclared": " — analysis/confirm_verdict_E2B.json :: B2_nested_S4_plus_V0_minus_S4
- **label_coupling_diagnostic**: {"V0_decoupled": 0.6106845179497277, "V0_same_rows": 0.7372514274463478, "V0_decoupled - flashlite_disg": 0.13288192975031732, "V0_decoupled - V0": -0.12656690949662008, "n_rows_with_decoupled": 381} — analysis/confirm_verdict_E2B.json :: label_coupling_diagnostic
- **B3_V0_minus_costmatched_disg**: {"delta": null, "ci": null, "directional_prediction": "none (pre-registered)", "reading": "NOT RUN: every cost-matched call was refused (HTTP 403 run budget exhausted)"} — analysis/confirm_verdict_E2B.json :: B3_V0_minus_costmatched_disg
- **B4_frontier**: {"status": "NOT_TESTABLE", "ratio_V0_over_frontier": null, "delta_V0_minus_frontier": null, "nested_frontier_plus_V0_minus_frontier": null, "n_in_R_AB_complete": 2} — analysis/confirm_verdict_E2B.json :: B4_frontier
- **H_IMPROVE**: "no carried variant: M1 selection.json winner = 'NONE: V0 stands'; V1-V5 reported as development-only rows" — analysis/confirm_verdict_E2B.json :: H_IMPROVE
- **H_MECH**: {"i_share_nonagreeing_peers_ERROR": "UNINFORMATIVE (tautological under gold-equivalence labels)", "ii_scatter_ratio_SI_cor_over_SI_err": "UNINFORMATIVE (tautological under gold-equivalence labels)", "iii_NET_delta_e_plus_d_words_T3_minus_T1": "REFUTED", "iv_exact_vs_ALIGN_e_d": "PARTIAL: tested components hold, MEANING_RENAME component NOT_TESTABLE (no MEANING_RENAME labels without the panel)"} — analysis/confirm_verdict_E2B.json :: H_MECH
- **sensitivity_B1**: {"R_A": null, "CONTESTED_as_CORRECT": null, "CONTESTED_as_ERROR": null} — analysis/confirm_verdict_E2B.json :: sensitivity_B1
- **secondary_note**: "NO PANEL: the run-level OpenRouter budget was exhausted before any batch completed the panel; labels are E's final rule without votes (tier A against the unaudited MALLS gold). Nothing is confirmatory; every number is exploratory" — analysis/confirm_verdict_E2B.json :: secondary_note

## 5. Frontier (B4), H-MECH, rename, cost

- **frontier_B4**: {"n_subsample_rows_scored": 49, "n_in_R_AB_complete": 2, "status": "NOT_TESTABLE"} — analysis/analysis_E2B.json :: frontier_B4
- **H_MECH**: {"i_share_nonagreeing_peers_ERROR": {"share": 1.0, "ci": [1.0, 1.0], "n_pairs": 94, "n_sentences": 24, "threshold": 0.5, "verdict": "UNINFORMATIVE (tautological under gold-equivalence labels)", "ci_excludes_threshold": true, "verdict_as_computed": "CONFIRMED", "regime_note": "UNINFORMATIVE in the no-panel regime: CORRECT = z3-equivalent to the (unaudited) gold, so two CORRECT rows are always mutually equivalent and a CORRECT candidate can only disagree with non-CORRECT peers (tautological)"}, "ii_scatter_ratio_SI_cor_over_SI_err": {"SI_cor": 1.0, "SI_err": 0.24814814814814815, "ratio": 4.029850746268656, "ci": [2.3893805309734515, 11.25], "n_sentences": 9, "threshold": 2.0, "verdict": "UNINFORMATIVE (tautological under gold-equivalence labels)", "verdict_as_computed": "CONFIRMED", "regime_note": "UNINFORMATIVE in the no-panel regime: CORRECT = z3-equivalent to the (unaudited) gold, so two CORRECT rows are always mutually equivalent and a CORRECT candidate can only disagree with non-CORRECT peers (tautological)"}, "iii_NET_delta_e_plus_d_words_T3_minus_T1": {"delta": -0.22503502938285547, "ci": [-0.5369048438263863, 0.1134536652067627], "e_T1": 0.09259259259259259, "d_T1": 0.9523809 — analysis/analysis_E2B.json :: H_MECH
- **rename**: {"RENAME_SYN": {"n_pairs": 31, "FA_control": 0.967741935483871, "FA_control_ci": [0.8380554282383037, 0.9942829259130554], "base_FA_parent": 0.8387096774193549, "base_FA_ci": [0.6736529727502113, 0.9290748009456006], "paired_flip": 0.12903225806451613, "paired_flip_ci": [0.05134201164644764, 0.28852756954385356], "reverse_flip": 0.0, "mean_delta_V0_control_minus_parent": 0.21236559139784944, "parent_V0_recomputed_matches": 31, "n_controls_total": 31, "n_unscorable": 0}, "RENAME_NONCE": {"n_pairs": 48, "FA_control": 1.0, "FA_control_ci": [0.9258973488472576, 0.9999999999999999], "base_FA_parent": 0.8333333333333334, "base_FA_ci": [0.7042189996260375, 0.9130458996054678], "paired_flip": 0.16666666666666666, "paired_flip_ci": [0.08695410039453222, 0.29578100037396254], "reverse_flip": 0.0, "mean_delta_V0_control_minus_parent": 0.3740079365079365, "parent_V0_recomputed_matches": 48, "n_controls_total": 48, "n_unscorable": 0}, "definition": "FA at c > 0.5 on meaning-preserving renames of final-CORRECT parents; paired flip = control flagged while its parent is not; base FA = parent flagged"} — analysis/analysis_E2B.json :: rename
- **cost**: {"V0_c_score_align": {"FULL_usd_per_candidate_(its_9_peer_generations)": 0.000859381835265, "FULL_usd_per_candidate_amortised_(sentence_generations/10)": 9.548687058499999e-05, "MARGINAL_usd_per_candidate": 0.0, "z3_seconds_per_candidate_(align_readout)": 0.05949, "note": "peers are the other systems' outputs: in a multi-system evaluation they already exist (MARGINAL = CPU only)"}, "p_peer_text": {"extra_usd_per_candidate_(L3_questionnaire_per_sentence/10)": 2.2914575e-05}, "flashlite_disg": {"usd_per_call": 5.6089897510980965e-05, "n_calls_with_cost": 2732, "seconds_per_call": 2.687434532791376}, "flashlite_orig": {"usd_per_call": null, "n_calls_with_cost": 0, "seconds_per_call": null}, "nano_orig": {"usd_per_call": null, "n_calls_with_cost": 0, "seconds_per_call": null}, "nano_disg": {"usd_per_call": null, "n_calls_with_cost": 0, "seconds_per_call": null}, "costmatched_disg": {"usd_per_call": null, "n_calls_with_cost": 0, "seconds_per_call": 0.21451823711395263}, "costmatched_orig": {"usd_per_call": null, "n_calls_with_cost": 0, "seconds_per_call": null}, "frontier_orig": {"usd_per_call": 0.0045654, "n_calls_with_cost": 10, "seconds_per_call": 4.564939427375793}} — analysis/analysis_E2B.json :: cost
- **system_tau_b**: {"V0": {"tau_b": 0.4666666666666666, "ci": [0.055263661852880175, 0.7777777777777777], "n_systems": 10}, "p_peer_text": {"tau_b": 0.4222222222222222, "ci": [-0.022222222222222223, 0.6372286056920369], "n_systems": 10}, "flashlite_disg": {"tau_b": -0.31462660248284624, "ci": [-0.45160481873147146, 0.23002185311411807], "n_systems": 10}, "flashlite_orig": {"tau_b": null, "ci": [null, null], "n_systems": 0}, "nano_orig": {"tau_b": null, "ci": [null, null], "n_systems": 0}, "costmatched_disg": {"tau_b": null, "ci": [null, null], "n_systems": 0}, "costmatched_orig": {"tau_b": null, "ci": [null, null], "n_systems": 0}, "S4_E2B": {"tau_b": 0.19999999999999998, "ci": [-0.3333333333333333, 0.45501956888318373], "n_systems": 10}, "note": "system = generator slot (10 slots, 9 families); system mean of (-score) vs system accuracy on R_AB; DESCRIPTIVE only (far fewer systems than WMT)"} — analysis/analysis_E2B.json :: system_tau_b
- **placebo_shuffled_peers**: {"n": 294, "auroc_V0_shuffled_peers": 0.5, "auroc_V0_same_rows": 0.7578660164867062, "share_shuffled_score_1.0": 1.0, "secs": 10.9} — analysis/analysis_E2B.json :: placebo_shuffled_peers

## 6. Label-free descriptives (no faithfulness claim)

- **coverage_all**: {"parse_rate": 0.88325, "V0_scorable": 0.88125, "V0_missing_reason": {"peers<2": 8}, "judge_status": {"flashlite_disg": {"unparseable": 467, "ok": 2632, "not_run": 333, "fallback": 103, "fail:api:OpenRouter error: {'code': 'aii_run_": 465}, "flashlite_orig": {"unparseable": 467, "not_run": 3533}, "nano_orig": {"unparseable": 467, "not_run": 3133, "fail:api:OpenRouter error: {'code': 'aii_run_": 400}, "nano_disg": {"unparseable": 467, "not_run": 3533}, "costmatched_disg": {"unparseable": 467, "not_run": 3503, "fail:api:OpenRouter error: {'code': 'aii_run_": 30}, "costmatched_orig": {"unparseable": 467, "not_run": 3503, "fail:api:OpenRouter error: {'code': 'aii_run_": 30}, "frontier_orig": {"unparseable": 467, "not_run": 3523, "ok": 10}}} — analysis/descriptive_nolabels_E2B.json :: coverage_all
- **concordance_V0_vs_flashlite_disg**: {"n": 2626, "spearman": 0.29589633244181873, "flag_agreement": 0.6972581873571972, "flag_kappa": 0.1678219878007657, "V0_flag_rate": 0.8956587966488957, "judge_flag_rate": 0.6721249047981721} — analysis/descriptive_nolabels_E2B.json :: concordance_V0_vs_flashlite_disg
- **system_rankings**: {"mean_V0": {"G1": 0.9027907884465262, "G1b": 0.8392063492063493, "G2": 0.8458645302984927, "G3": 0.8473214285714284, "G4": 0.8314610190300797, "G5": 0.8923867912287532, "G6": 0.8254582127510305, "G7": 0.8176020408163267, "G8": 0.8588871912401326, "G9": 0.928610116284211}, "mean_flashlite_disg": {"G1": 0.7698660714285716, "G1b": 0.6697318007662836, "G2": 0.6480769230769231, "G3": 0.7053956834532374, "G4": 0.603202846975089, "G5": 0.7172727272727273, "G6": 0.6314338235294118, "G7": 0.5899239543726235, "G8": 0.5537906137184114, "G9": 0.8451310861423222}, "parse_rate": {"G1": 0.7625, "G1b": 0.9025, "G2": 0.795, "G3": 0.92, "G4": 0.9075, "G5": 0.9225, "G6": 0.9075, "G7": 0.875, "G8": 0.94, "G9": 0.9}, "tau_b_V0_vs_flashlite": 0.6444444444444444} — analysis/descriptive_nolabels_E2B.json :: system_rankings
- **agreement_structure**: {"n_sentences": 399, "mean_classes_per_sentence": 6.370927318295739, "mean_largest_class_share": 0.328676850857302, "mean_cross_family_agreement": 0.13435997714959755, "share_sentences_no_cross_family_agreement": 0.19143576826196473, "pair_timeouts_unknown": 0, "n_pairs_total": 12150} — analysis/descriptive_nolabels_E2B.json :: agreement_structure
- **rename_invariance_any_label**: {"RENAME_SYN": {"n_pairs": 137, "paired_flip": 0.08759124087591241, "paired_flip_ci": [0.050815009419275796, 0.14686522142161212], "reverse_flip": 0.0, "reverse_flip_ci": [0.0, 0.027276032081430486], "flag_rate_parent": 0.8905109489051095, "flag_rate_control": 0.9781021897810219, "mean_shift_control_minus_parent": 0.09893117831074034, "share_score_unchanged": 0.6788321167883211, "parent_recomputed_matches_sealed": 137}, "RENAME_NONCE": {"n_pairs": 298, "paired_flip": 0.10738255033557047, "paired_flip_ci": [0.0770964540642678, 0.14766249235001042], "reverse_flip": 0.0, "reverse_flip_ci": [0.0, 0.012727205262627815], "flag_rate_parent": 0.8926174496644296, "flag_rate_control": 1.0, "mean_shift_control_minus_parent": 0.14073985298817512, "share_score_unchanged": 0.5570469798657718, "parent_recomputed_matches_sealed": 298}, "sample": "sha1('E2B_lfctrl|'+row_key) first 300 PARSEABLE candidates, any label; controls from E2's frozen generator (dataset-3 perturb.control_rename), z3-verified under the inverse map"} — analysis/descriptive_nolabels_E2B.json :: rename_invariance_any_label
- **distribution_by_word_bin**: {"25-29": {"V0": {"n": 3286, "mean": 0.8554864794365707, "median": 1.0, "share_gt_0.5": 0.8959220937309799, "share_eq_0": 0.010955569080949483, "share_eq_1": 0.5544735240413877, "n_distinct": 26}, "p_peer_text": {"n": 3294, "mean": 0.7816333227881306, "median": 0.8636205622017021, "share_gt_0.5": 0.8649058894960534, "share_eq_0": 0.0, "share_eq_1": 0.0, "n_distinct": 2205}, "flashlite_disg": {"n": 2535, "mean": 0.6667258382642999, "median": 1.0, "share_gt_0.5": 0.6481262327416174, "share_eq_0": 0.05680473372781065, "share_eq_1": 0.5112426035502958, "n_distinct": 11}, "V1": {"n": 3286, "mean": 0.6450134770889487, "median": 1.0, "share_gt_0.5": 0.6141205112598904, "share_eq_0": 0.28088861838101037, "share_eq_1": 0.5544735240413877, "n_distinct": 17}, "V2": {"n": 3286, "mean": 0.8483817765224153, "median": 1.0, "share_gt_0.5": 0.9013998782714546, "share_eq_0": 0.010955569080949483, "share_eq_1": 0.5544735240413877, "n_distinct": 1173}, "c_exact": {"n": 3286, "mean": 0.9629671091402681, "median": 1.0, "share_gt_0.5": 0.9884357881923311, "share_eq_0": 0.0030432136335970784, "share_eq_1": 0.8247108947048083, "n_distinct": 21}}, "30-34": {"V0": {"n": 239, "mean": 0.9004283721856943, "median": 1.0, "share_gt_0.5": 0.9707112970711297, "share_eq_0": 0.0, "share_eq_1": 0.606694560669456, "n_distinct": 15}, "p_peer_text": {"n": 239, "mean": 0.785611523920843, "median": 0.8350341551979662, "share_gt_0.5": 0.9037656903765691, "share_eq_0": 0.0, "share_eq_1": 0.0, "n_distinct": 208}, "flash — analysis/descriptive_nolabels_E2B.json :: distribution_by_word_bin

### Coverage per system

| slot | system | parse rate | V0 scorable | flash-lite disg answered | mean V0 | source |
|---|---|---|---|---|---|---|
| G1 | G1:meta-llama/llama-3.1-8b-instruct | 0.762 | 0.762 | 0.585 | 0.903 | analysis/descriptive_nolabels_E2B.json :: coverage_per_system.G1 |
| G1b | G1b:meta-llama/llama-3.3-70b-instruct | 0.902 | 0.900 | 0.693 | 0.839 | analysis/descriptive_nolabels_E2B.json :: coverage_per_system.G1b |
| G2 | G2:qwen/qwen3-235b-a22b-2507 | 0.795 | 0.795 | 0.613 | 0.846 | analysis/descriptive_nolabels_E2B.json :: coverage_per_system.G2 |
| G3 | G3:mistralai/mistral-small-3.2-24b-instruct | 0.920 | 0.920 | 0.713 | 0.847 | analysis/descriptive_nolabels_E2B.json :: coverage_per_system.G3 |
| G4 | G4:deepseek/deepseek-v3.2 | 0.907 | 0.905 | 0.723 | 0.831 | analysis/descriptive_nolabels_E2B.json :: coverage_per_system.G4 |
| G5 | G5:google/gemma-3-27b-it | 0.922 | 0.917 | 0.715 | 0.892 | analysis/descriptive_nolabels_E2B.json :: coverage_per_system.G5 |
| G6 | G6:microsoft/phi-4 | 0.907 | 0.905 | 0.705 | 0.825 | analysis/descriptive_nolabels_E2B.json :: coverage_per_system.G6 |
| G7 | G7:openai/gpt-4.1-mini | 0.875 | 0.875 | 0.682 | 0.818 | analysis/descriptive_nolabels_E2B.json :: coverage_per_system.G7 |
| G8 | G8:google/gemini-2.5-flash | 0.940 | 0.935 | 0.720 | 0.859 | analysis/descriptive_nolabels_E2B.json :: coverage_per_system.G8 |
| G9 | G9:cohere/command-r7b-12-2024 | 0.900 | 0.897 | 0.690 | 0.929 | analysis/descriptive_nolabels_E2B.json :: coverage_per_system.G9 |

## 7. Union with E2-A

- status: NOT_COMPUTED_E2A_MISSING — analysis/union_longpool.json :: status

## 8. Checks

- code freeze: 78 files checked, 0 mismatches — e2bsrc/code_freeze_check_E2B.json
- exp-5 copy reproduces stored E scores: c_score_align 50/50, p_peer_text 50/50 — e2b/exp5_repro_check.json
- exp-6 statistics reproduce T1: L25 0.06942089474370672 (expected 0.06942), long 0.11625879215576673 — e2b/T1_repro_check.json
- score seal: 77 files hashed at 2026-09-24T12:45:26Z, access violations 0 — scores/score_seal.json
- seals verified before the join: {'label_seal_verify': '{"seal_intact": true, "candidate_identical_to_reference": 22}', 'label_seal_rc': 0, 'score_seal_verify': '{"score_seal_intact": true, "mismatches": []}', 'score_seal_rc': 0} — analysis/analysis_E2B.json :: seals
