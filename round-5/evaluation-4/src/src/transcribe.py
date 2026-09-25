"""Transcription rows: numbers that enter record_final.md from source tables but are not
hypothesis/review claims. They get numbers.csv rows with match status TRANSCRIBED (value read by
code; there is no claim literal to compare). `fmt` is a format template literal (precision only).
"""
from __future__ import annotations

from src.claims_spec import A9, ANC, C, CTR, CU, D4, E8, EV2, EV3, J, PC, X10, X9, D5
from src.io_locators import I3

T: list[dict] = []


def t(id: str, text: str, loc: dict, fmt: str = "0.000", ciloc=None, ci_fmt: str | None = None, role: str = "DESCRIPTIVE"):
    T.append(dict(id=id, sec="transcribed", text=text, value=None, fmt=fmt, loc=loc, ciloc=ciloc,
                  ci=ci_fmt, role=role, ps=None, pp=None))


# §3.4: invariance rows from eval-3 perturb_corrected.csv (T7), for the metrics the review names
for m in ("c_align", "c_nf", "c_hyb", "judge_cheap_disg", "p_peer_text", "p_text", "l3_z3", "S4_local"):
    for fam in ("RENAME_NONCE", "RENAME_SYN"):
        w = {"metric": m, "family": fam, "section": "T7. Invariance: false alarms (FA) on meaning-preserving rewrites of CORRECT bases, flip rate separately"}
        t(f"pc_{m}_{fam}_fa", f"{m} {fam} FA [CI] (E bases)", C(PC, w, "FA [CI]"), "0.000", ci_fmt="[0.000, 0.000]", role="DEV")
        t(f"pc_{m}_{fam}_base", f"{m} {fam} paired base FA", C(PC, w, "base_FA"), "0.000", role="DEV")
        t(f"pc_{m}_{fam}_flip", f"{m} {fam} flip rate", C(PC, w, "flip"), "0.000", role="DEV")

# §3.4 T8 recall at primary threshold for c_align (per operator), for the corrected sensitivity row
for op in ("NEG", "SWAP", "DROP", "ADD", "MEANING_RENAME"):
    t(f"pc_calign_recall_{op}", f"c_align recall at PRIMARY threshold, {op}",
      C(PC, {"metric": "c_align", "section": "T8. PERTURB recall at the PRIMARY threshold (E bases, polarities pooled)"}, op), "0.000", role="DEV")

# §10: FREE-consensus recall next to base FA (exp 10 anchoring.csv, ALL_MUTANTS)
for var, src in (("FREE_c_align_exp8", "E"), ("FREE3_exact", "E"), ("FREE3_exact", "RCOMP"), ("FREE3_align", "RCOMP"), ("FREE3_align", "E"),
                 ("JUDGE_flashlite_disg_exp8", "E"), ("LOCAL2_own_sig", "E"), ("LOCAL2_base_sig", "E")):
    w = {"variant": var, "op_label": "ALL_MUTANTS", "polarity": "ALL", "base_source": src}
    t(f"x10_rec_{var}_{src}", f"{var} mutant recall at c > 0.5 ({src})", C(ANC, w, "recall_gt05"), "0.000", role="DEV")
t("x10_bfa_fa_e", "base FA at c > 0.5, FREE3_align on E", C(f"{X10}/d_by_length.csv", {"variant": "FREE3_align", "base_source": "E"}, "d_all"), "0.000", role="DEV")
t("x10_bfa_judge_e", "base FA, flash-lite judge on E", C(f"{X10}/d_by_length.csv", {"variant": "JUDGE_flashlite_disg_exp8", "base_source": "E"}, "d_all"), "0.000", role="DEV")
for var in ("FREE_c_align_exp8", "FREE3_exact", "FREE3_align"):
    for k in ("d_T1", "d_T2", "d_T3"):
        t(f"x10_{var}_{k}", f"{var} d on E bases, words {k[2:]}", C(f"{X10}/d_by_length.csv", {"variant": var, "base_source": "E"}, k), "0.000", role="DEV")

# §10: controls split by base_source, FA + paired base FA + flip
for var in ("FREE_c_align_exp8", "FREE3_exact", "FREE3_align", "JUDGE_flashlite_disg_exp8", "SIGPROXY_K3"):
    for ctl in ("RENAME_SYN", "RENAME_NONCE", "REORDER_COMMUTE", "CONTRAPOSITIVE"):
        for src in ("E", "RCOMP"):
            if var == "FREE_c_align_exp8" and src == "RCOMP":
                continue
            if var == "SIGPROXY_K3" and src == "E":
                continue
            w = {"variant": var, "control_type": ctl, "base_source": src}
            key = f"ctl_{var}_{ctl}_{src}"
            t(key + "_fa", f"{var} {ctl} FA ({src})", C(CTR, w, "FA_gt05"), "0.000", role="DEV")
            t(key + "_base", f"{var} {ctl} paired base FA ({src})", C(CTR, w, "paired_base_FA"), "0.000", role="DEV")
            t(key + "_flip", f"{var} {ctl} flip ({src})", C(CTR, w, "flip_rate"), "0.000",
              ciloc=[C(CTR, w, "flip_lo"), C(CTR, w, "flip_hi")], ci_fmt="[0.000, 0.000]", role="DEV")

# §9: T4 terciles and T8 exp-10 label-free ALIGN (R_COMP FREE) and T4 PRIMARY tercile AUROCs (exp 9 T12)
for tt in ("T1", "T2", "T3"):
    t(f"x9_t12_csc_{tt}", f"c_csc strat AUROC, words {tt} (PRIMARY)", J(A9, f"h_complexity_PRIMARY.words_t.{tt}.c_csc.point"), "0.000", role="DEV")
    t(f"x9_t12_ca_{tt}", f"c_score_align AUROC, words {tt} (PRIMARY)", J(A9, f"h_complexity_PRIMARY.words_t.{tt}.T1__c_score_align.point"), "0.000", role="DEV")
t("x9_nest", "nested [S4_full + c_csc] − S4_full, strat (PRIMARY)", J(A9, "c_nesting_PRIMARY.nested.S4_full+c_csc - S4_full.strat.delta"), "+0.000",
  ciloc=J(A9, "c_nesting_PRIMARY.nested.S4_full+c_csc - S4_full.strat.ci"), ci_fmt="[0.000, 0.000]", role="DEV")
t("x9_e_fa", "FREE_align e (PRIMARY R_AB)", J(A9, "a_ed_PRIMARY.cells.R_AB.FREE_align.e"), "0.000", role="DEV")
t("x9_d_fa", "FREE_align d (PRIMARY R_AB)", J(A9, "a_ed_PRIMARY.cells.R_AB.FREE_align.d"), "0.000", role="DEV")
t("x9_full_e_fx", "FULL FREE_exact e", J(A9, "a_ed_FULL.cells.R_AB.FREE_exact.e"), "0.000", role="DEV")
t("x9_full_e_fa", "FULL FREE_ALIGN e", J(A9, "a_ed_FULL.cells.R_AB.FREE_align.e"), "0.000", role="DEV")
for g, key in (("graded", "c_csc_graded"), ("multi", "c_csc_multi")):
    t(f"x9_{g}", f"{key} strat AUROC (PRIMARY)", J(A9, f"{'b_PRIMARY.metrics.R_AB [strat]'}.{key}.point"), "0.000",
      ciloc=J(A9, f"b_PRIMARY.metrics.R_AB [strat].{key}.ci"), ci_fmt="[0.000, 0.000]", role="DEV")
    t(f"x9_{g}_g1d", f"{key} G1 d", J(f"{X9}/csc_gate_E.json", f"variants.{key}.G1.d"), "0.000", role="DEV")
t("x9_hyb_g1d", "HYB_MEAN G1 d", J(f"{X9}/csc_gate_E.json", "variants.HYB_MEAN.G1.d"), "0.000", role="DEV")
t("x9_hyb_g1s", "HYB_MEAN G1 words slope", J(f"{X9}/csc_gate_E.json", "variants.HYB_MEAN.G1.words_slope.b"), "0.00", role="DEV")
t("x9_repro", "eval-2 3-pool strat reproduction (exp 9 repro check)", J(f"{X9}/results/repro_checks.json", "m4_pool_deepseek+microsoft+openai.strat_auroc"), "0.0000", role="DESCRIPTIVE")

# §13 cost table: every cost_units.csv row with a per-unit value
COST_ITEMS = [("judge_cheap", "USD per item-call"), ("judge_cheap2", "USD per item-call"), ("strong", "USD per item-call"),
              ("roundtrip", "USD per item-call"), ("sc5", "USD per item-call"), ("consensus c_score_align", "USD per item (candidate)"),
              ("k-pool k=1.0", "USD per sentence"), ("k-pool k=3.0", "USD per sentence"), ("k-pool k=5.0", "USD per sentence"),
              ("k-pool k=7.0", "USD per sentence"), ("SIG peer generation", "USD per candidate"),
              ("SIG peer generation", "USD per sentence (10 slots)"), ("marginal z3 check", "USD per candidate")]
for item, unit in COST_ITEMS:
    key = "cu_" + "".join(ch if ch.isalnum() else "_" for ch in f"{item}_{unit}")[:60]
    t(key, f"cost_units.csv: {item} ({unit})", C(CU, {"item": item, "unit": unit}, "value"), "0.00e0", role="DESCRIPTIVE")

# §3.5 eval-2 M3-local, M2 placebo reference, k=5 AUROC
t("ev2_k5", "M4 AUROC(k=5)", J(f"{EV2}/results/part_a.json", "M4.random_k_primary.k.5.auroc_mean"), "0.000", role="DEV")
t("ev2_net_de", "NET Δe words T3 − T1", J(f"{EV2}/results/part_a.json", "NET.R_AB.words_T3_minus_T1.delta_e"), "+0.000", role="DEV")
t("ev2_net_dd", "NET Δd words T3 − T1", J(f"{EV2}/results/part_a.json", "NET.R_AB.words_T3_minus_T1.delta_d"), "+0.000", role="DEV")
for tt in ("T1", "T2", "T3"):
    for k in ("1", "3", "5", "7"):
        t(f"ev2_k{k}_{tt}", f"M4 AUROC(k={k}) words {tt}", J(f"{EV2}/results/part_a.json", f"M4.random_k_primary.k.{k}.tercile_auroc_mean.{tt}"), "0.000", role="DEV")
for k in ("2", "4", "6"):
    t(f"ev2_k{k}", f"M4 AUROC(k={k})", J(f"{EV2}/results/part_a.json", f"M4.random_k_primary.k.{k}.auroc_mean"), "0.000", role="DEV")
    for tt in ("T1", "T2", "T3"):
        t(f"ev2_k{k}_{tt}", f"M4 AUROC(k={k}) words {tt}", J(f"{EV2}/results/part_a.json", f"M4.random_k_primary.k.{k}.tercile_auroc_mean.{tt}"), "0.000", role="DEV")
for k in ("2", "4", "6"):
    t(f"cost_k{k}", f"k={k} pool $ per SENTENCE", C(CU, {"item": f"k-pool k={k}.0"}, "value"), "0.000000", role="DESCRIPTIVE")

# §11 dataset 4/5 extras
t("d4_trackh_repl", "track-H judgements replayed with >= 2 new votes", J(f"{D4}/panel_drift_E2.json", "trackh_192_judgements.n_replayed_with_>=2_new_votes"), "0", role="DESCRIPTIVE")
t("d4_trackh_n", "track-H judgements total", J(f"{D4}/panel_drift_E2.json", "trackh_192_judgements.n_items"), "0", role="DESCRIPTIVE")
t("d4_proj", "E2 projected total cost to complete", J(f"{D4}/pilot_projection.json", "projected_total_usd"), "$0.00", role="DESCRIPTIVE")
t("d5_resc_ci_n_lo", "nonce rescue CI lo", J(f"{D5}/results/soundness_audit.json", "i_sig_replay.nonce.rescue_ci", idx=0), "0.000", role="DESCRIPTIVE")
t("d5_resc_ci_n_hi", "nonce rescue CI hi", J(f"{D5}/results/soundness_audit.json", "i_sig_replay.nonce.rescue_ci", idx=1), "0.000", role="DESCRIPTIVE")
t("d5_old_cor_mapped", "old CORRECT rows that are MAPPED", J(f"{D5}/results/old_label_agreement.json", "agreement_table_old_tierA_vs_new.CORRECT|MAPPED"), "0", role="DESCRIPTIVE")
t("d5_old_cor", "old CORRECT tier-A rows", J(f"{D5}/results/old_label_agreement.json", "old_label_counts_on_new_rows.CORRECT"), "0", role="DESCRIPTIVE")

# §12 eval 3 extras
t("e3_placebo3", "specificity placebo ratio, 3-pool", J(f"{EV3}/results/part1.json", "pools.3pool.placebo.specificity_ratio"), "0.00", ciloc=J(f"{EV3}/results/part1.json", "pools.3pool.placebo.specificity_ratio_ci"), ci_fmt="[0.00, 0.0]", role="DEV")
t("e3_placebo9", "specificity placebo ratio, 9-family", J(f"{EV3}/results/part1.json", "pools.9fam.placebo.specificity_ratio"), "0.00", ciloc=J(f"{EV3}/results/part1.json", "pools.9fam.placebo.specificity_ratio_ci"), ci_fmt="[0.00, 0.00]", role="DEV")
t("e3_labdenom", "oracle floor with labelled-only denominator (3-pool)", J(f"{EV3}/results/part1.json", "pools.3pool.d_R_oracle_labdenom"), "0.000", role="DEV")
t("e3_endmaj3", "END_MAJ d, 3-pool", J(f"{EV3}/results/part1.json", "pools.3pool.d_bracket", idx=1), "0.000", role="DEV")
t("e3_ecap", "e ceiling (R_point_label), 3-pool", C(f"{EV3}/tables/p1_rule_cuts.csv", {"pool": "3pool", "rule": "R_point_label", "dim": "ALL", "cell": "ALL"}, "e"), "0.000", role="DEV")
t("e3_vres3", "c_vres − c_score_align L25, 3-pool", J(f"{EV3}/results/part1.json", "pools.3pool.c_vres.L25.delta_strat_auroc_vres_minus_frozen"), "+0.000",
  ciloc=J(f"{EV3}/results/part1.json", "pools.3pool.c_vres.L25.delta_strat_auroc_vres_minus_frozen_ci"), ci_fmt="[0.000, 0.000]", role="DEV")
t("e3_sigrow", "row endorsement SIG (END_MAJ)", J(f"{EV3}/results/part2.json", "row_endorsement_rates.end_maj_sig"), "0.000", role="DEV")
t("e3_freerow", "row endorsement FREE (END_MAJ)", J(f"{EV3}/results/part2.json", "row_endorsement_rates.end_maj_free"), "0.000", role="DEV")
t("e3_net9_pl", "NET 9-family R_point_label", J(f"{EV3}/results/part1_net.json", "9fam|R_point_label_draw0.full_B2000_delta.words_T3_minus_T1.delta_e_plus_d"), "+0.000", role="DEV")
t("e3_net3_pl", "NET 3-pool R_point_label", J(f"{EV3}/results/part1_net.json", "3pool|R_point_label_draw0.full_B2000_delta.words_T3_minus_T1.delta_e_plus_d"), "+0.000", role="DEV")
for n in ("250", "300", "350", "400"):
    t(f"pw_mde_{n}", f"MDE80 L25 planned {n} (flash-lite disguised)", C(f"{EV3}/tables/p3_planned_E2.csv", {"cell": "L25", "planned_sentences": n, "comparator": "flashlite_disg", "yield_scenario": "E_yield"}, "mde80"), "0.000", role="DESCRIPTIVE")
    t(f"pw_pow_{n}", f"power at +0.069, L25 planned {n}", C(f"{EV3}/tables/p3_planned_E2.csv", {"cell": "L25", "planned_sentences": n, "comparator": "flashlite_disg", "yield_scenario": "E_yield"}, "power_at_0.069"), "0.00", role="DESCRIPTIVE")
t("iter1_triage_fa", "FOL-Triage fused worst-family rewrite FA (gate <= 0.10)", {"t": "regex", "f": f"{I3.replace('iter_3', 'iter_1')}/gen_art_experiment_1/README.md", "pat": r"fails the rewrite-FA gate\*\*: (\d\.\d+) of rewritten"}, "0.000", role="DEV")

HV2 = f"{EV2}/tables/hypothesis_verdicts.csv"
t("ev2_b2_gate", "B2 gate balanced accuracy (track-H corrected)", C(HV2, {"clause_id": "v.B2_gate"}, "file_value"), "0.000", role="DEV")
t("ev2_radj_h", "R_ADJ Sonnet-5 balanced accuracy on expert track-H", C(HV2, {"clause_id": "v.RADJ_sonnet_H"}, "file_value"), "0.000", role="DEV")
t("ev2_radj_all", "R_ADJ Sonnet-5 gate balanced accuracy overall", C(HV2, {"clause_id": "v.RADJ_sonnet"}, "file_value"), "0.000", role="DEV")
