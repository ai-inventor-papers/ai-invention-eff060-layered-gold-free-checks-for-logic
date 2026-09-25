"""Hand-curated claim list: one locator per claim. Values are NEVER typed here as sources;
`value` is the literal as written in the hypothesis §0.2-0.3 / the review critique, and the
checker pulls the file value through the locator. Exported verbatim to claims_spec.yaml.

Fields: id, sec (section tag), text, value (claim literal), ci (claim CI literal or None),
loc (point locator), ciloc (locator returning [lo, hi] or a pair of locators),
role (data role), ps (paper section heading prefix used to search the paper), pp (paper regex
capturing the paper's own number for this quantity, when the review says it differs).
"""
from __future__ import annotations

from src.io_locators import I3, I4, RUN

E6 = f"{I3}/gen_art_experiment_6/results/analysis_T1.json"
E6L = f"{I3}/gen_art_experiment_6/results/api_cost_ledger.json"
E8 = f"{I3}/gen_art_experiment_8/results"
EV2 = f"{I3}/gen_art_evaluation_2"
EV3 = f"{I4}/gen_art_evaluation_3"
X9 = f"{I4}/gen_art_experiment_9"
A9 = f"{X9}/results/analysis.json"
X10 = f"{I4}/gen_art_experiment_10/results"
D4 = f"{I4}/gen_art_dataset_4"
D5 = f"{I4}/gen_art_dataset_5"
REVA = f"{RUN}/iter_4/review_report/review_report/audit"
T2R = f"{EV3}/tables/t2_record.csv"
CU = f"{EV3}/tables/cost_units.csv"
PC = f"{EV3}/tables/perturb_corrected.csv"


def J(f: str, k: str, **kw) -> dict:
    return {"t": "json", "f": f, "k": k, **kw}


def C(f: str, where: dict, col: str) -> dict:
    return {"t": "csv", "f": f, "where": where, "col": col}


def X(expr: str, **args) -> dict:
    return {"t": "expr", "expr": expr, "args": args}


def K(v, why: str) -> dict:
    return {"t": "const", "v": v, "why": why}


H1 = "a_head_on.R_AB pooled.deltas.c_score_align - judge_cheap_disg [strat]"
HL = "a_head_on.R_AB long (L25+L20+EXC).deltas.c_score_align - judge_cheap_disg [strat]"
D9 = "b_PRIMARY.deltas.R_AB [strat]"
M9 = "b_PRIMARY.metrics.R_AB [strat]"
MR = "MEANING_RENAME-type (MEANING_RENAME op or tier-B VOCAB_GRAN)"
STR = "structural(CONN/RESTR/BIND/MOVE/SWAP/SCOPE/UNGLUE)"
POL = "polarity(NEG/REV/QUANT)"
CTR = f"{X10}/controls_fa.csv"
ANC = f"{X10}/anchoring.csv"
TYP = f"{X10}/typing_csc.csv"

DEV, CONF, OOS, DESC, GOLD = "DEV", "CONFIRM-PENDING", "OUT-OF-SCOPE-SIG", "DESCRIPTIVE", "GOLD-USING-ORACLE"


def c(id, sec, text, value, loc, ci=None, ciloc=None, role=DEV, ps=None, pp=None):
    return dict(id=id, sec=sec, text=text, value=value, ci=ci, loc=loc, ciloc=ciloc, role=role, ps=ps, pp=pp)


CLAIMS: list[dict] = [
    # ---------------- §0.2 T1 (exp 6) ----------------
    c("t1_strat_c", "hyp §0.2 T1", "c_score_align strat AUROC on E R_AB", "0.741", J(E6, H1 + ".auroc_a"), ps="### 3.2"),
    c("t1_strat_j", "hyp §0.2 T1", "flash-lite disguised strat AUROC on E R_AB", "0.642", J(E6, H1 + ".auroc_b"), ps="### 3.2"),
    c("t1_delta", "hyp §0.2 T1", "Δ c_score_align − flash-lite disguised, strat, R_AB", "+0.099", J(E6, H1 + ".delta"), "[0.049, 0.146]", J(E6, H1 + ".ci"), ps="### 3.2"),
    c("t1_long", "hyp §0.2 T1", "Δ long pool (L25+L20+EXC), strat", "+0.116", J(E6, HL + ".delta"), "[0.070, 0.163]", J(E6, HL + ".ci"), ps="### 3.2"),
    c("t1_exc", "hyp §0.2 T1", "Δ EXC stratum (pooled within stratum)", "+0.197", J(E6, "a_head_on.R_AB EXC.deltas.c_score_align - judge_cheap_disg [pooled].delta"), ps="### 3.2"),
    c("t1_nano", "hyp §0.2 T1", "Δ vs gpt-4.1-nano original, strat", "+0.089", J(E6, "a_head_on.R_AB pooled.deltas.c_score_align - judge_cheap2_orig [strat].delta"), "[0.043, 0.134]", J(E6, "a_head_on.R_AB pooled.deltas.c_score_align - judge_cheap2_orig [strat].ci"), ps="### 3.2"),
    c("t1_l25", "hyp §0.2 T1", "Δ L25 stratum (n.s.)", "+0.069", J(E6, "a_head_on.R_AB L25.deltas.c_score_align - judge_cheap_disg [pooled].delta"), "[−0.020, 0.148]", J(E6, "a_head_on.R_AB L25.deltas.c_score_align - judge_cheap_disg [pooled].ci"), ps="### 3.2"),
    c("t1_ctrl", "hyp §0.2 T1", "Δ CTRL stratum", "−0.069", J(E6, "a_head_on.R_AB CTRL.deltas.c_score_align - judge_cheap_disg [pooled].delta"), "[−0.23, 0.10]", J(E6, "a_head_on.R_AB CTRL.deltas.c_score_align - judge_cheap_disg [pooled].ci"), ps="### 3.2"),
    c("t1_l20", "hyp §0.2 T1", "Δ L20 stratum", "+0.108", J(E6, "a_head_on.R_AB L20.deltas.c_score_align - judge_cheap_disg [pooled].delta"), "[0.031, 0.183]", J(E6, "a_head_on.R_AB L20.deltas.c_score_align - judge_cheap_disg [pooled].ci"), ps="### 3.2"),
    c("t1_vs_s4", "hyp §0.2 T1", "c alone ≈ S4_full: c − S4_full strat (sign-flipped S4−c)", "+0.006", X("-a", a=J(E6, "a_head_on.R_AB pooled.deltas.S4_full_oof - c_score_align [strat].delta")), "[−0.031, 0.042]", None, ps="### 3.2"),
    c("t1_nested", "hyp §0.2 T1", "nested [S4_full + c] − S4_full, strat", "+0.039", J(E6, "b_s4.nested.S4_full_plus_c_score_align - S4_full.strat.delta"), "[0.021, 0.057]", J(E6, "b_s4.nested.S4_full_plus_c_score_align - S4_full.strat.ci"), ps="### 3.2"),
    c("t1_fr_judge", "hyp §0.2 T1", "frontier frame (n=284) AUROC judge_strong_orig", "0.741", J(E6, "d_frontier.metrics.judge_strong_orig.auroc"), ps="### 3.2"),
    c("t1_fr_s4", "hyp §0.2 T1", "frontier frame AUROC S4_full", "0.745", J(E6, "d_frontier.metrics.S4_full_oof.auroc"), ps="### 3.2"),
    c("t1_fr_c", "hyp §0.2 T1", "frontier frame AUROC c_score_align", "0.710", J(E6, "d_frontier.metrics.c_score_align.auroc"), ps="### 3.2"),
    c("t1_ratio", "hyp §0.2 T1", "frontier ratio c / judge (0.95 bar met on point only)", "0.957", J(E6, "d_frontier.ratio.ratio"), "[0.887, 1.034]", J(E6, "d_frontier.ratio.ci"), ps="### 3.2"),
    c("t1_fr_nested", "hyp §0.2 T1", "frontier frame nested gain", "+0.037", J(E6, "d_frontier.nested_frame.delta"), "[0.008, 0.066]", J(E6, "d_frontier.nested_frame.ci"), ps="### 3.2"),
    c("t1_m3_boot", "hyp §0.2 T1", "M3 bootstrap slope difference (words)", "+0.146", J(E6, "e_M3.M3_words.diff"), "[−0.051, 0.361]", J(E6, "e_M3.M3_words.ci"), ps="### 3.2"),
    c("t1_m3_gee", "hyp §0.2 T1", "M3 stacked-GEE interaction", "+0.274", J(E6, "e_M3.stacked_interaction.coef"), "[0.190, 0.359]", J(E6, "e_M3.stacked_interaction.ci"), ps="### 3.2"),
    c("t1_did", "hyp §0.2 T1", "flash-lite contamination DiD", "+0.105", J(E6, "g_contamination.judge_cheap.DiD"), "[0.006, 0.201]", J(E6, "g_contamination.judge_cheap.DiD_ci"), ps="### 3.2"),
    c("t1_spend", "hyp §0.2 T1", "T1 spend (USD, ledger total)", "2.395", J(E6L, "total_usd_from_usage_cost"), role=DESC),
    # ---------------- §0.2 T2 ----------------
    c("t2_sig", "hyp §0.2 T2", "SIG within-template AUROC c_score_sig (out-of-scope controlled vocabulary)", "0.954", C(T2R, {"section": "SIG: primary test, criterion (c)"}, "c_score_sig"), role=OOS, ps="### 3.3"),
    c("t2_judge", "hyp §0.2 T2", "SIG within-template AUROC flash-lite disguised", "0.587", C(T2R, {"section": "SIG: primary test, criterion (c)"}, "judge_cheap_disg"), role=OOS, ps="### 3.3"),
    c("t2_vs_orig", "hyp §0.2 T2", "SIG Δ vs the original (undisguised) judge", "+0.278", C(T2R, {"comparison": "vs_judge_cheap_orig"}, "delta [95% CI]"), role=OOS, ps="### 3.3"),
    c("t2_free_err", "hyp §0.2 T2 [Correction]", "old iter-3 FREE tier-A ERROR rows", "420", J(f"{D5}/results/old_label_agreement.json", "old_label_counts_on_new_rows.ERROR"), role=DESC, ps="### 3.3"),
    c("t2_free_mapped", "hyp §0.2 T2 [Correction]", "old ERROR rows that are MAPPED (upper bound of old false errors)", "297", J(f"{D5}/results/old_label_agreement.json", "agreement_table_old_tierA_vs_new.ERROR|MAPPED"), role=DESC, ps="### 4.5"),
    c("t2_free_void", "hyp §0.2 T2 [Correction]", "VOID iter-3 FREE tier-A delta (c_align − judge) as printed in §3.3", "+0.214", K(0.214, "value reported on the invalidated iter-3 FREE tier-A labels; VOID"), role=DESC, ps="### 3.3"),
    # ---------------- §0.2 exp 8 ----------------
    c("e8_hyb_syn", "hyp §0.2 exp8", "HYB PERTURB RENAME_SYN FA (selection)", "0.841", J(f"{E8}/selection.json", "evidence.HYB.rename_FA.ii_PERTURB_RENAME_SYN"), ps="### 3.4"),
    c("e8_hyb_nonce", "hyp §0.2 exp8", "HYB PERTURB RENAME_NONCE FA (selection)", "0.700", J(f"{E8}/selection.json", "evidence.HYB.rename_FA.iii_PERTURB_RENAME_NONCE"), ps="### 3.4"),
    c("e8_nf_syn", "hyp §0.2 exp8", "NF-anchored PERTURB RENAME_SYN FA", "0.686", J(f"{E8}/selection.json", "evidence.NF-anchored.rename_FA.ii_PERTURB_RENAME_SYN"), ps="### 3.4"),
    c("e8_nf_nonce", "hyp §0.2 exp8", "NF-anchored PERTURB RENAME_NONCE FA", "0.485", J(f"{E8}/selection.json", "evidence.NF-anchored.rename_FA.iii_PERTURB_RENAME_NONCE"), ps="### 3.4"),
    c("e8_cnf_mr", "hyp §0.2 exp8", "c_nf within-base AUROC on MEANING_RENAME (an ERROR operator)", "0.499", C(f"{E8}/perturb_sensitivity.csv", {"metric": "c_nf", "operator": "MEANING_RENAME", "polarity": "ALL", "subset": "E_bases"}, "within_base_auroc"), ps="### 3.4"),
    c("e8_cov_ok", "hyp §0.2 exp8", "PERTURB rows scored (coverage numerator)", "3,419", C(f"{E8}/coverage_perturb.csv", {"metric": "c_align"}, "n_scored_ok"), role=DESC, ps="### 3.4"),
    c("e8_cov_n", "hyp §0.2 exp8", "PERTURB rows total (coverage denominator)", "5,402", C(f"{E8}/coverage_perturb.csv", {"metric": "c_align"}, "n_rows"), role=DESC, ps="### 3.4"),
    c("e8_typ_medoid", "hyp §0.2 exp8", "typing: peer-medoid accuracy", "0.328", J(f"{X10}/typing_summary.json", "medoid_align_exp8.acc"), ps="### 3.4"),
    c("e8_typ_judge", "hyp §0.2 exp8", "typing: flash-lite judge accuracy", "0.326", J(f"{X10}/typing_summary.json", "judge_flashlite_exp8.acc"), ps="### 3.4"),
    c("e8_typ_oracle", "hyp §0.2 exp8", "typing: gold-using oracle accuracy", "0.802", J(f"{X10}/typing_summary.json", "oracle_strict_exp8"), role=GOLD, ps="### 3.4"),
    c("e8_calign_nonce", "hyp §2 boundary", "c_align PERTURB RENAME_NONCE FA (E bases)", "0.765", C(PC, {"metric": "c_align", "family": "RENAME_NONCE"}, "FA [CI]"), ps="### 3.4"),
    c("e8_calign_syn", "hyp §2 boundary", "c_align PERTURB RENAME_SYN FA (E bases)", "0.565", C(PC, {"metric": "c_align", "family": "RENAME_SYN"}, "FA [CI]"), ps="### 3.4"),
    c("e8_calign_base", "hyp §2 boundary", "c_align PERTURB base FA (E bases)", "0.201", C(PC, {"metric": "c_align", "family": "BASE"}, "FA [CI]"), ps="### 3.4"),
    # ---------------- §0.2 eval 2 ----------------
    c("ev2_m1", "hyp §0.2 eval2", "M1 verdict (pre-registered)", "INCONCLUSIVE", J(f"{EV2}/results/part_a.json", "M1_M2.M1.MAJ|primary.verdict"), role=DESC, ps="### 3.5"),
    c("ev2_k95", "hyp §0.2 eval2", "M4 k95 overall", "3", J(f"{EV2}/results/part_a.json", "M4.random_k_primary.k95"), ps="### 3.5"),
    c("ev2_k95_t1", "hyp §0.2 eval2", "M4 k95 words tercile T1", "2", J(f"{EV2}/results/part_a.json", "M4.random_k_primary.k95_tercile.T1"), ps="### 3.5"),
    c("ev2_k95_t2", "hyp §0.2 eval2", "M4 k95 words tercile T2", "3", J(f"{EV2}/results/part_a.json", "M4.random_k_primary.k95_tercile.T2"), ps="### 3.5"),
    c("ev2_k95_t3", "hyp §0.2 eval2", "M4 k95 words tercile T3 (long)", "5", J(f"{EV2}/results/part_a.json", "M4.random_k_primary.k95_tercile.T3"), ps="### 3.5"),
    c("ev2_net", "hyp §0.2 eval2", "NET Δ(e+d) words T3 − T1 (degrades)", "+0.356", J(f"{EV2}/results/part_a.json", "NET.R_AB.words_T3_minus_T1.delta_e_plus_d"), "[0.198, 0.493]", J(f"{EV2}/results/part_a.json", "NET.R_AB.words_T3_minus_T1.ci"), ps="### 3.5"),
    c("ev2_scatter", "hyp §0.2 eval2", "SCATTER ratio SI_cor/SI_err", "4.45", J(f"{EV2}/results/part_a.json", "SCATTER.overall.ratio_SI_cor_over_SI_err_same_sentences.ratio"), "[3.57, 5.77]", J(f"{EV2}/results/part_a.json", "SCATTER.overall.ratio_SI_cor_over_SI_err_same_sentences.ci"), ps="### 3.5"),
    c("ev2_graded", "hyp §0.2 eval2", "graded − binary AUROC", "+0.114", J(f"{EV2}/results/part_a.json", "graded_vs_binary.delta_graded_minus_binary"), "[0.091, 0.140]", J(f"{EV2}/results/part_a.json", "graded_vs_binary.delta_ci"), ps="### 3.5"),
    c("ev2_k1", "hyp §0.2 eval2", "M4 AUROC(k=1)", "0.685", J(f"{EV2}/results/part_a.json", "M4.random_k_primary.k.1.auroc_mean"), ps="### 3.5"),
    c("ev2_k3", "hyp §0.2 eval2", "M4 AUROC(k=3)", "0.757", J(f"{EV2}/results/part_a.json", "M4.random_k_primary.k.3.auroc_mean"), ps="### 3.5"),
    c("ev2_k7", "hyp §0.2 eval2", "M4 AUROC(k=7)", "0.784", J(f"{EV2}/results/part_a.json", "M4.random_k_primary.k.7.auroc_mean"), ps="### 3.5"),
    # ---------------- costs ----------------
    c("cost_cons", "hyp §0.2 costs", "consensus $ per candidate FULL", "$1.21e-4", C(CU, {"item": "consensus c_score_align"}, "value"), role=DESC, ps="### 4.6"),
    c("cost_k1", "hyp §0.2 costs", "k=1 pool $ per SENTENCE", "$0.000315", C(CU, {"item": "k-pool k=1.0"}, "value"), role=DESC, ps="### 4.6"),
    c("cost_k3", "hyp §0.2 costs", "k=3 pool $ per SENTENCE", "$0.000946", C(CU, {"item": "k-pool k=3.0"}, "value"), role=DESC, ps="### 4.6"),
    c("cost_k5", "hyp §0.2 costs", "k=5 pool $ per SENTENCE", "$0.001576", C(CU, {"item": "k-pool k=5.0"}, "value"), role=DESC, ps="### 4.6"),
    c("cost_k7", "hyp §0.2 costs", "k=7 pool $ per SENTENCE", "$0.002206", C(CU, {"item": "k-pool k=7.0"}, "value"), role=DESC, ps="### 4.6"),
    c("cost_flash", "hyp §0.2 costs", "flash-lite judge $ per item-call", "$4.9e-5", C(CU, {"item": "judge_cheap"}, "value"), role=DESC, ps="### 4.6"),
    c("cost_frontier", "hyp §0.2 costs", "frontier judge $ per item-call", "$3.65e-3", C(CU, {"item": "strong"}, "value"), role=DESC),
    c("cost_sig", "hyp §0.2 costs", "SIG peer generation $ per candidate", "$0.000116", C(CU, {"item": "SIG peer generation", "unit": "USD per candidate"}, "value"), role=DESC, ps="### 4.6"),
    c("cost_z3", "hyp §0.2 costs", "MARGINAL z3 $ per candidate", "$2.5e-7", J(E6, "cost.consensus.marginal_mean_usd_per_item"), role=DESC),
    c("cost_iter3", "hyp §0.2 costs", "iteration-3 spend (sum of ledgers)", "$4.33", C(CU, {"artifact": "iteration 3"}, "value"), role=DESC, ps="### 4.6"),
    # ---------------- §0.3A exp 9 ----------------
    c("x9_n", "hyp §0.3A", "PRIMARY rows", "354", J(A9, "populations.PRIMARY.n"), role=DESC, ps="### 4.2"),
    c("x9_nerr", "hyp §0.3A", "PRIMARY ERROR rows", "196", J(A9, "populations.PRIMARY.n_err"), role=DESC, ps="### 4.2"),
    c("x9_ncor", "hyp §0.3A", "PRIMARY CORRECT rows", "158", J(A9, "populations.PRIMARY.n_cor"), role=DESC, ps="### 4.2"),
    c("x9_nsent", "hyp §0.3A", "PRIMARY sentences", "144", J(A9, "populations.PRIMARY.n_sent"), role=DESC, ps="### 4.2"),
    c("x9_ctrl_prim", "hyp §0.3A", "CTRL share of PRIMARY CORRECT rows", "44.9%", X("a/b", a=J(A9, "populations.PRIMARY_by_stratum.CTRL.n_cor"), b=J(A9, "populations.PRIMARY.n_cor")), role=DESC),
    c("x9_ctrl_full", "hyp §0.3A", "CTRL share of FULL CORRECT rows (reviewer recompute; re-derived in audit)", "27.4%", J(f"{REVA}/recompute_csc.json", "full_CTRL_share_of_CORRECT"), role=DESC),
    c("x9_l25_err", "hyp §0.3A", "PRIMARY L25 ERROR rows (< 50 → NOT_READ)", "59", J(A9, "populations.PRIMARY_by_stratum.L25.n_err"), role=DESC),
    c("x9_l25_cor", "hyp §0.3A", "PRIMARY L25 CORRECT rows (< 50 → NOT_READ)", "22", J(A9, "populations.PRIMARY_by_stratum.L25.n_cor"), role=DESC),
    c("x9_tie", "hyp §0.3A", "c_csc tie rate", "0.986", J(A9, M9 + ".c_csc.tie_rate"), role=DESC),
    c("x9_csc", "hyp §0.3A T4", "c_csc strat AUROC", "0.614", J(A9, M9 + ".c_csc.point"), "[0.493, 0.736]", J(A9, M9 + ".c_csc.ci"), ps="### 4.2", pp=r"\*\*CSC\*\* \| \*\*0\.614 (\[[^\]]+\])"),
    c("x9_fexact", "hyp §0.3A T4", "FREE_exact (same 3 families) strat AUROC", "0.770", J(A9, M9 + ".c_free_exact.point"), "[0.686, 0.844]", J(A9, M9 + ".c_free_exact.ci"), ps="### 4.2", pp=r"FREE_exact \(matched\) \| 0\.770 (\[[^\]]+\])"),
    c("x9_falign", "hyp §0.3A T4", "FREE_ALIGN strat AUROC", "0.731", J(A9, M9 + ".c_free_align.point"), "[0.635, 0.825]", J(A9, M9 + ".c_free_align.ci"), ps="### 4.2"),
    c("x9_calign", "hyp §0.3A T4", "c_score_align strat AUROC on PRIMARY", "0.774", J(A9, M9 + ".T1__c_score_align.point"), "[0.682, 0.857]", J(A9, M9 + ".T1__c_score_align.ci"), ps="### 4.2", pp=r"\| c_score_align \| 0\.774 (\[[^\]]+\])"),
    c("x9_ppt", "hyp §0.3A T4", "p_peer_text strat AUROC on PRIMARY", "0.799", J(A9, M9 + ".T1__p_peer_text.point"), "[0.700, 0.880]", J(A9, M9 + ".T1__p_peer_text.ci"), ps="### 4.2", pp=r"\| p_peer_text \| 0\.799 (\[[^\]]+\])"),
    c("x9_s4", "hyp §0.3A T4", "S4_full strat AUROC on PRIMARY", "0.736", J(A9, M9 + ".T1__S4_full_oof.point"), "[0.635, 0.826]", J(A9, M9 + ".T1__S4_full_oof.ci"), ps="### 4.2", pp=r"\| S4_full \| 0\.736 (\[[^\]]+\])"),
    c("x9_flash", "hyp §0.3A T4", "flash-lite disguised strat AUROC on PRIMARY", "0.664", J(A9, M9 + ".T1__judge_cheap_disg.point"), "[0.568, 0.750]", J(A9, M9 + ".T1__judge_cheap_disg.ci"), ps="### 4.2", pp=r"\| flash-lite judge \| 0\.664 (\[[^\]]+\])"),
    c("x9_hyb", "hyp §0.3A T4", "HYB_MEAN strat AUROC on PRIMARY (fails G1)", "0.709", J(A9, M9 + ".HYB_MEAN.point"), "[0.586, 0.817]", J(A9, M9 + ".HYB_MEAN.ci"), ps="### 4.2"),
    c("x9_d_fexact", "hyp §0.3A T5", "Δ c_csc − FREE_exact", "−0.156", J(A9, D9 + ".c_csc - c_free_exact.delta"), "[−0.290, −0.031]", J(A9, D9 + ".c_csc - c_free_exact.ci"), ps="### 4.2"),
    c("x9_d_calign", "hyp §0.3A T5", "Δ c_csc − c_score_align", "−0.160", J(A9, D9 + ".c_csc - T1__c_score_align.delta"), "[−0.275, −0.064]", J(A9, D9 + ".c_csc - T1__c_score_align.ci"), ps="### 4.2"),
    c("x9_d_flash", "hyp §0.3A T5", "Δ c_csc − flash-lite (n.s.)", "−0.050", J(A9, D9 + ".c_csc - T1__judge_cheap_disg.delta"), "[−0.212, 0.107]", J(A9, D9 + ".c_csc - T1__judge_cheap_disg.ci"), ps="### 4.2"),
    c("x9_d_s4", "hyp §0.3A T5", "Δ c_csc − S4_full (n.s.)", "−0.123", J(A9, D9 + ".c_csc - T1__S4_full_oof.delta"), "[−0.269, 0.010]", J(A9, D9 + ".c_csc - T1__S4_full_oof.ci"), ps="### 4.2"),
    c("x9_d_ppt", "review crit 2", "Δ c_csc − p_peer_text (paper value)", "−0.185", J(A9, D9 + ".c_csc - T1__p_peer_text.delta"), "[−0.281, −0.103]", J(A9, D9 + ".c_csc - T1__p_peer_text.ci"), ps="### 4.2"),
    c("x9_phi_calls", "hyp §0.3A T17", "phi-4 CSC calls that copied the exemplar", "58", X("a+b", a=J(f"{X9}/results/posthoc_phi_contamination.json", "contaminated_calls_by_model_route.microsoft/phi-4|json_fenced"), b=J(f"{X9}/results/posthoc_phi_contamination.json", "contaminated_calls_by_model_route.microsoft/phi-4|reask_json_fenced")), role=DESC),
    c("x9_clean", "hyp §0.3A T17", "c_csc_clean strat AUROC", "0.639", J(f"{X9}/results/posthoc_phi_contamination.json", "strat_auroc.c_csc_clean.point")),
    c("x9_clean_d", "hyp §0.3A T17", "Δ c_csc_clean − FREE_exact_clean", "−0.132", J(f"{X9}/results/posthoc_phi_contamination.json", "delta_strat.c_csc_clean - c_free_exact_clean.delta"), "[−0.251, −0.023]", J(f"{X9}/results/posthoc_phi_contamination.json", "delta_strat.c_csc_clean - c_free_exact_clean.ci")),
    c("x9_e_csc", "hyp §0.3A", "CSC e (PRIMARY R_AB)", "0.459", J(A9, "a_ed_PRIMARY.cells.R_AB.CSC.e"), ps="### 4.2"),
    c("x9_e_fx", "hyp §0.3A", "FREE_exact e (PRIMARY R_AB)", "0.173", J(A9, "a_ed_PRIMARY.cells.R_AB.FREE_exact.e"), ps="### 4.2"),
    c("x9_d_csc", "hyp §0.3A", "CSC d (PRIMARY R_AB)", "0.139", J(A9, "a_ed_PRIMARY.cells.R_AB.CSC.d"), ps="### 4.2"),
    c("x9_d_fx", "hyp §0.3A", "FREE_exact d (PRIMARY R_AB)", "0.323", J(A9, "a_ed_PRIMARY.cells.R_AB.FREE_exact.d"), ps="### 4.2"),
    c("x9_full_d_fx", "hyp §0.3A T2", "FULL FREE_exact d", "0.583", J(A9, "a_ed_FULL.cells.R_AB.FREE_exact.d")),
    c("x9_full_d_fa", "hyp §0.3A T2", "FULL FREE_ALIGN d", "0.328", J(A9, "a_ed_FULL.cells.R_AB.FREE_align.d")),
]

for cls, key, vals in [("ADD", "ADD", ("0.490", "0.135", "0.375")), ("DROP", "DROP", ("0.472", "0.169", "0.380")),
                       ("COMPOUND", "COMPOUND", ("0.282", "0.107", "0.184")), ("MR", MR, ("0.821", "0.036", "0.750")),
                       ("STRUCT", STR, ("0.336", "0.153", "0.282")), ("POL", POL, ("0.200", "0.133", "0.200"))]:
    for arm, v in zip(("CSC", "FREE_exact", "FREE_align"), vals):
        pp = None
        if cls == "COMPOUND" and arm in ("CSC", "FREE_exact"):
            pp = r"\| COMPOUND \| (\d\.\d+) \| (\d\.\d+) \|"
        CLAIMS.append(c(f"x9_t9_{cls}_{arm}", "hyp §0.3A T9", f"e_{arm} on {cls} errors (PRIMARY)", v,
                        J(A9, f"e_anchoring_by_error_class.PRIMARY.{key}.{arm}.e"), ps="### 4.2",
                        pp=(pp, 1 if arm == "CSC" else 2) if pp else None))

CLAIMS += [
    c("x9_t9_mr_n", "hyp §0.3A T9", "MEANING_RENAME-type n (PRIMARY)", "28", J(A9, f"e_anchoring_by_error_class.PRIMARY.{MR}.n"), role=DESC),
    c("x9_t9_mr_d", "hyp §0.3A T9", "MEANING_RENAME-type Δe CSC − FREE_ALIGN (NOT_READ)", "+0.071", J(A9, f"e_anchoring_by_error_class.PRIMARY.{MR}.paired_CSC_minus_FREE_align.delta_e"), "[−0.083, 0.269]", J(A9, f"e_anchoring_by_error_class.PRIMARY.{MR}.paired_CSC_minus_FREE_align.delta_e_ci")),
    c("x9_t9b_mr_fa", "hyp §0.3A T9b", "FULL FREE_ALIGN e on MEANING_RENAME-type", "0.624", J(A9, f"e_anchoring_by_error_class.FULL.{MR}.FREE_align.e")),
    c("x9_t9b_mr_fx", "hyp §0.3A T9b", "FULL FREE_exact e on MEANING_RENAME-type", "0.104", J(A9, f"e_anchoring_by_error_class.FULL.{MR}.FREE_exact.e")),
    c("x9_g1_d", "hyp §0.3A gates", "G1 d (≤ 0.35 part passes)", "0.139", J(f"{X9}/csc_gate_E.json", "variants.c_csc.G1.d")),
    c("x9_g1_slope", "hyp §0.3A gates", "G1 words slope of d (GEE)", "+1.25", J(f"{X9}/csc_gate_E.json", "variants.c_csc.G1.words_slope.b"), "[0.41, 2.09]", J(f"{X9}/csc_gate_E.json", "variants.c_csc.G1.words_slope.ci")),
    c("x9_g1_pass", "hyp §0.3A gates", "G1 pass flag", "False", J(f"{X9}/csc_gate_E.json", "variants.c_csc.G1.pass"), role=DESC),
    c("x9_g2", "hyp §0.3A gates", "G2 overall verdict", "NOT_READ", J(f"{X9}/csc_gate_E.json", "variants.c_csc.G2.pass"), role=DESC, ps="### 4.2", pp=(r"\| G2 \(strat AUROC ≥ 0\.700\) \| \*\*(FAIL)\*\*", 1)),
    c("x9_g2_rab", "hyp §0.3A gates", "G2 R_AB part pass flag", "False", J(f"{X9}/csc_gate_E.json", "variants.c_csc.G2.R_AB_part_pass"), role=DESC),
    c("x9_g2_l25", "hyp §0.3A gates", "G2 L25 Δ vs c_score_align (n = 81, not read)", "−0.067", J(f"{X9}/csc_gate_E.json", "variants.c_csc.G2.L25_delta_vs_c_score_align.delta"), "[−0.183, 0.040]", J(f"{X9}/csc_gate_E.json", "variants.c_csc.G2.L25_delta_vs_c_score_align.ci")),
    c("x9_g3", "hyp §0.3A gates", "G3-E (RENAME_SYN FA gate) status", "NOT_RUN", J(f"{X9}/csc_gate_E.json", "variants.c_csc.G3_E"), role=DESC),
    c("x9_g5", "hyp §0.3A gates", "G5 FULL $ per candidate (undeduped)", "$5.25e-4", J(f"{X9}/csc_gate_E.json", "variants.c_csc.G5.FULL_usd_per_candidate"), role=DESC),
    c("x9_g5_dd", "hyp §0.3A gates", "G5 $ per candidate, deduped", "$2.76e-4", J(A9, "g_cost.FULL_usd_per_candidate_dedup_apportioned_mean"), role=DESC),
    c("x9_m3_boot", "hyp §0.3A length", "M3 bootstrap Δslope CSC − flash-lite", "−0.232", J(A9, "h_M3.CSC_vs_flashlite_disg_PRIMARY.spec1_bootstrap_delta_slope.delta"), "[−0.770, −0.023]", J(A9, "h_M3.CSC_vs_flashlite_disg_PRIMARY.spec1_bootstrap_delta_slope.ci"), ps="### 4.2", pp=r"length interaction for CSC is negative: −0\.232 (\[[^\]]+\])"),
    c("x9_m3_gee", "hyp §0.3A length", "M3 stacked-GEE interaction CSC − flash-lite", "−0.351", J(A9, "h_M3.CSC_vs_flashlite_disg_PRIMARY.spec2_stacked_gee_interaction.b"), "[−0.694, −0.009]", J(A9, "h_M3.CSC_vs_flashlite_disg_PRIMARY.spec2_stacked_gee_interaction.ci")),
    c("x9_net_fx", "hyp §0.3A length", "NET FULL FREE_exact T3 − T1", "+0.452", J(A9, "net.FULL.FREE_exact.words_T3_minus_T1.delta_e_plus_d")),
    c("x9_net_fa", "hyp §0.3A length", "NET FULL FREE_align T3 − T1", "+0.401", J(A9, "net.FULL.FREE_align.words_T3_minus_T1.delta_e_plus_d")),
    c("x9_t8_struct", "hyp §0.3A T8", "share of free-exact disagreements with CORRECT candidates that are structural", "53%", J(A9, "d_where_FULL_free_exact_flagged_CORRECT.pair_shares.structural (no vocabulary map makes them equivalent)")),
    c("x9_t8_vocab", "hyp §0.3A T8", "flagged CORRECT rows fully vocabulary-resolvable", "20.2%", J(A9, "d_where_FULL_free_exact_flagged_CORRECT.share_rows_vocab_resolvable")),
    c("x9_t10_own", "hyp §0.3A T10", "typing own_majority exact accuracy", "0.185", J(A9, "f_typing_PRIMARY.own_majority.acc_exact_opset")),
    c("x9_t10_maj", "hyp §0.3A T10", "typing majority-class baseline", "0.262", J(A9, "f_typing_PRIMARY.majority_acc")),
    c("x9_t14_csc", "hyp §0.3A T14", "system-level τ-b CSC", "0.256", J(A9, "i_system_level_PRIMARY.c_csc.tau_b")),
    c("x9_t14_csc_p", "hyp §0.3A T14", "system-level τ-b CSC p", "0.25", J(A9, "i_system_level_PRIMARY.c_csc.p")),
    c("x9_t14_ca", "hyp §0.3A T14", "system-level τ-b c_score_align", "0.513", J(A9, "i_system_level_PRIMARY.T1__c_score_align.tau_b")),
    c("x9_t14_ca_p", "hyp §0.3A T14", "system-level τ-b c_score_align p", "0.015", J(A9, "i_system_level_PRIMARY.T1__c_score_align.p")),
    c("x9_t15_base", "hyp §0.3A T15", "9-peer c_score_align FA base (SYN rows)", "0.595", J(A9, "k_rename.c_score_align_rederived_on_SYN_rows.FA_base (c >= 0.5 = not END_MAJ endorsed)")),
    c("x9_t15_syn", "hyp §0.3A T15", "9-peer c_score_align FA under WordNet-synonym rename", "0.868", J(A9, "k_rename.c_score_align_rederived_on_SYN_rows.FA_syn")),
    c("x9_t15_d", "hyp §0.3A T15", "ΔFA rename", "+0.273", J(A9, "k_rename.c_score_align_rederived_on_SYN_rows.delta_FA"), "[0.164, 0.384]", J(A9, "k_rename.c_score_align_rederived_on_SYN_rows.delta_FA_ci")),
    c("x9_spend", "hyp §0.3A", "exp-9 spend (ledger total)", "$0.108", J(A9, "g_cost.ledger_total_usd"), role=DESC, ps="### 4.2"),
    # ---------------- §0.3B exp 10 ----------------
    c("x10_sigproxy", "hyp §0.3B", "SIGPROXY k=3 within-template AUROC (out-of-scope SIG)", "0.930", J(f"{X10}/rcomp_sig_csc.json", "auroc_within_template.c_proxy.est"), "[0.916, 0.943]", J(f"{X10}/rcomp_sig_csc.json", "auroc_within_template.c_proxy.ci"), role=OOS, ps="### 4.3"),
    c("x10_d_cued", "hyp §0.3B", "d on bases, cued SIGPROXY_K3", "0.149", C(f"{X10}/paired_cue_effect.csv", {"a": "SIGPROXY_K3", "b": "FREE3_align", "quantity": "d_bases"}, "a_value"), role=OOS, ps="### 4.3"),
    c("x10_d_uncued", "hyp §0.3B", "d on bases, uncued FREE3-ALIGN", "0.757", C(f"{X10}/paired_cue_effect.csv", {"a": "SIGPROXY_K3", "b": "FREE3_align", "quantity": "d_bases"}, "b_value"), role=OOS, ps="### 4.3"),
    c("x10_d_diff", "hyp §0.3B", "paired d difference cued − uncued", "−0.608", C(f"{X10}/paired_cue_effect.csv", {"a": "SIGPROXY_K3", "b": "FREE3_align", "quantity": "d_bases"}, "a_minus_b"), "[−0.716, −0.500]",
      [C(f"{X10}/paired_cue_effect.csv", {"a": "SIGPROXY_K3", "b": "FREE3_align", "quantity": "d_bases"}, "lo"), C(f"{X10}/paired_cue_effect.csv", {"a": "SIGPROXY_K3", "b": "FREE3_align", "quantity": "d_bases"}, "hi")], role=OOS, ps="### 4.3"),
    c("x10_bfa_calign", "hyp §0.3B", "base FA at c > 0.5, c_align_exp8 on E", "0.712", C(f"{X10}/d_by_length.csv", {"variant": "FREE_c_align_exp8", "base_source": "E"}, "d_all"), ps="### 4.3"),
    c("x10_bfa_fx_e", "hyp §0.3B", "base FA at c > 0.5, FREE3_exact on E", "0.803", C(f"{X10}/d_by_length.csv", {"variant": "FREE3_exact", "base_source": "E"}, "d_all"), ps="### 4.3"),
    c("x10_bfa_fx_r", "hyp §0.3B", "base FA at c > 0.5, FREE3_exact on R_COMP", "0.986", C(f"{X10}/d_by_length.csv", {"variant": "FREE3_exact", "base_source": "RCOMP"}, "d_all"), ps="### 4.3"),
    c("x10_bfa_fa_r", "hyp §0.3B", "base FA at c > 0.5, FREE3_align on R_COMP", "0.757", C(f"{X10}/d_by_length.csv", {"variant": "FREE3_align", "base_source": "RCOMP"}, "d_all"), ps="### 4.3"),
    c("x10_flip_syn", "hyp §0.3B", "c_align E RENAME_SYN paired flip", "0.182", C(CTR, {"variant": "FREE_c_align_exp8", "control_type": "RENAME_SYN", "base_source": "E"}, "flip_rate"), ps="### 4.3"),
    c("x10_flip_nonce", "hyp §0.3B", "c_align E RENAME_NONCE paired flip", "0.327", C(CTR, {"variant": "FREE_c_align_exp8", "control_type": "RENAME_NONCE", "base_source": "E"}, "flip_rate"), ps="### 4.3"),
    c("x10_l2_e", "hyp §0.3B", "LOCAL2_own_sig e on E mutants", "0.341", C(ANC, {"variant": "LOCAL2_own_sig", "op_label": "ALL_MUTANTS", "polarity": "ALL", "base_source": "E"}, "e"), ps="### 4.3"),
    c("x10_l2_tie", "hyp §0.3B", "LOCAL2 share of mutants at exactly c = 0.5 (reviewer recompute)", "0.341", J(f"{REVA}/recompute_perturb_csc.json", "LOCAL2_share_exact_0.5"), role=DESC),
    c("x10_l2_excl_own", "hyp §0.3B", "LOCAL2_own_sig e excluding insufficient-peer ties", "0.012", C(ANC, {"variant": "LOCAL2_own_sig", "op_label": "ALL_MUTANTS", "polarity": "ALL", "base_source": "E"}, "e_excl_insufficient")),
    c("x10_l2_excl_base", "hyp §0.3B", "LOCAL2_base_sig e excluding insufficient-peer ties", "0.007", C(ANC, {"variant": "LOCAL2_base_sig", "op_label": "ALL_MUTANTS", "polarity": "ALL", "base_source": "E"}, "e_excl_insufficient")),
    c("x10_judge_e", "hyp §0.3B", "flash-lite mutant endorsement on PERTURB E (NOT END_MAJ e)", "0.124", C(ANC, {"variant": "JUDGE_flashlite_disg_exp8", "op_label": "ALL_MUTANTS", "polarity": "ALL", "base_source": "E"}, "e"), ps="### 4.3"),
    c("x10_free3", "hyp §0.3B", "typing free3 strict accuracy on E", "0.123", C(TYP, {"target": "free3", "base_source": "E", "true_op": "ALL"}, "strict"), "[0.081, 0.169]", [C(TYP, {"target": "free3", "base_source": "E", "true_op": "ALL"}, "lo"), C(TYP, {"target": "free3", "base_source": "E", "true_op": "ALL"}, "hi")], ps="### 4.3"),
    c("x10_free3_pool", "hyp §0.3B", "typing free3 pooled E+R_COMP (includes R_COMP rows at 0)", "0.085", C(TYP, {"target": "free3", "base_source": "ALL", "true_op": "ALL"}, "strict"), ps="### 4.3"),
    c("x10_oracle", "hyp §0.3B", "typing oracle on E (GOLD-USING)", "0.928", C(TYP, {"target": "oracle", "base_source": "E", "true_op": "ALL"}, "strict"), role=GOLD),
    c("x10_proxy", "hyp §0.3B", "typing SIGPROXY majority on R_COMP", "0.784", C(TYP, {"target": "proxy", "base_source": "RCOMP", "true_op": "ALL"}, "strict"), "[0.711, 0.849]", [C(TYP, {"target": "proxy", "base_source": "RCOMP", "true_op": "ALL"}, "lo"), C(TYP, {"target": "proxy", "base_source": "RCOMP", "true_op": "ALL"}, "hi")], role=OOS, ps="### 4.3"),
    c("x10_reorder_e", "hyp §0.3B", "FREE3_exact REORDER_COMMUTE FA on E", "0.842", C(CTR, {"variant": "FREE3_exact", "control_type": "REORDER_COMMUTE", "base_source": "E"}, "FA_gt05")),
    c("x10_contra_e", "hyp §0.3B", "FREE3_exact CONTRAPOSITIVE FA on E", "0.840", C(CTR, {"variant": "FREE3_exact", "control_type": "CONTRAPOSITIVE", "base_source": "E"}, "FA_gt05")),
    c("x10_contra_r", "hyp §0.3B", "FREE3_exact CONTRAPOSITIVE FA on R_COMP", "0.986", C(CTR, {"variant": "FREE3_exact", "control_type": "CONTRAPOSITIVE", "base_source": "RCOMP"}, "FA_gt05"), ps="### 4.3"),
    c("x10_t1", "hyp §0.3B", "uncued c_align d on bases, words T1", "0.47", C(f"{X10}/d_by_length.csv", {"variant": "FREE_c_align_exp8", "base_source": "E"}, "d_T1")),
    c("x10_t2", "hyp §0.3B", "uncued c_align d on bases, words T2", "0.80", C(f"{X10}/d_by_length.csv", {"variant": "FREE_c_align_exp8", "base_source": "E"}, "d_T2")),
    c("x10_t3", "hyp §0.3B", "uncued c_align d on bases, words T3", "0.91", C(f"{X10}/d_by_length.csv", {"variant": "FREE_c_align_exp8", "base_source": "E"}, "d_T3")),
    c("x10_t8_align", "review crit 4", "R_COMP FREE label-free ALIGN pairwise agreement (T8)", "0.219", {"t": "regex", "f": f"{X10}/tables.md", "pat": r"Pairwise equivalence among FREE few-shot candidates of a sentence: ALIGN (\d\.\d+)"}),
    c("x10_spend", "hyp §0.3B", "exp-10 spend", "$0.0000088", {"t": "ledger", "f": f"{X10}/api_cost_ledger.jsonl", "field": "cost_usd"}, role=DESC, ps="### 4.3"),
    # ---------------- §0.3C dataset 4 ----------------
    c("d4_err", "hyp §0.3C", "E2 pilot ERROR rows", "36", {"t": "jsonl_count", "f": f"{D4}/sealed/labels_E2.jsonl", "where": {"label": "ERROR"}}, role=DESC, ps="### 4.4"),
    c("d4_unres", "hyp §0.3C", "E2 pilot UNRESOLVED rows (incl. gold-as-system)", "274", {"t": "jsonl_count", "f": f"{D4}/sealed/labels_E2.jsonl", "where": {"label": "UNRESOLVED"}}, role=DESC),
    c("d4_unp", "hyp §0.3C", "E2 pilot UNPARSEABLE rows", "20", {"t": "jsonl_count", "f": f"{D4}/sealed/labels_E2.jsonl", "where": {"label": "UNPARSEABLE"}}, role=DESC),
    c("d4_cor", "hyp §0.3C", "E2 pilot CORRECT rows", "0", {"t": "jsonl_count", "f": f"{D4}/sealed/labels_E2.jsonl", "where": {"label": "CORRECT"}}, role=DESC),
    c("d4_comb", "hyp §0.3C", "panel drift combined majority agreement over ALL items (counts unreplayed items)", "0.394", J(f"{D4}/panel_drift_E2.json", "combined_majority_agreement_all_items"), role=DESC),
    c("d4_repl", "review/plan", "panel drift majority agreement on REPLAYED items", "0.9725", J(f"{D4}/panel_drift_E2.json", "combined_majority_agreement_replayed_items"), role=DESC),
    c("d4_syn", "hyp §0.3C", "synthetic gate items majority agreement", "0.974", J(f"{D4}/panel_drift_E2.json", "synthetic_gate_77.majority_agreement"), role=DESC, ps="### 4.4"),
    c("d4_flag_today", "hyp §0.3C", "track-H unambiguous: today's panel flags original errors", "0.12", J(f"{D4}/panel_drift_E2.json", "trackh_majority_vs_experts.today.orig_flagged_rate_unamb"), role=DESC),
    c("d4_flag_E", "hyp §0.3C", "track-H unambiguous: E's panel flagged original errors", "0.84", J(f"{D4}/panel_drift_E2.json", "trackh_majority_vs_experts.E.orig_flagged_rate_unamb"), role=DESC),
    c("d4_n22", "hyp §0.3C", "track-H unambiguous judgements replayed today", "22", J(f"{D4}/panel_drift_E2.json", "trackh_majority_vs_experts.today.unambiguous.n_judgements"), role=DESC),
    c("d4_passes", "hyp §0.3C", "drift stop-rule passes flag", "False", J(f"{D4}/panel_drift_E2.json", "passes"), role=DESC),
    c("d4_spend", "hyp §0.3C", "dataset-4 spend so far", "$0.241", J(f"{D4}/pilot_projection.json", "spent_so_far_usd"), role=DESC, ps="### 4.4"),
    c("d4_pilot_usd", "plan (13)", "E2 pilot projected $ per L25 sentence", "$0.0118", J(f"{D4}/pilot_projection.json", "per_sentence_cost_usd.L25.total"), role=DESC),
    c("pw_yield", "hyp §0.3C power", "L25 yield (eval 3)", "0.37", J(f"{EV3}/power_E2.json", "yield.L25.yield"), role=DESC, ps="### 4.6"),
    c("pw_mde", "hyp §0.3C power", "MDE80 at 350 planned L25 (vs flash-lite disguised)", "0.110", C(f"{EV3}/tables/p3_planned_E2.csv", {"cell": "L25", "planned_sentences": "350", "comparator": "flashlite_disg", "yield_scenario": "E_yield"}, "mde80"), role=DESC),
    c("pw_882", "hyp §0.3C power", "planned L25 sentences for +0.069 at 80% power", "882", J(f"{EV3}/power_E2.json", "n_needed.L25.flashlite_disg.planned_for_mde_0.069"), role=DESC, ps="### 4.6"),
    c("pw_237", "hyp §0.3C power", "usable long-pool sentences for +0.069", "237", J(f"{EV3}/power_E2.json", "n_needed.long.flashlite_disg.usable_for_mde_0.069"), role=DESC),
    # ---------------- §0.3D dataset 5 ----------------
    c("d5_err", "hyp §0.3D", "ERROR_CERT rows", "759", J(f"{D5}/results/testability_FREE_v2.json", "all_rows.label_counts.ERROR_CERT"), role=DESC, ps="### 4.5"),
    c("d5_map", "hyp §0.3D", "MAPPED (UNRESOLVED_GLOSS_NOT_RUN) rows", "1,506", J(f"{D5}/results/testability_FREE_v2.json", "all_rows.label_counts.UNRESOLVED_GLOSS_NOT_RUN"), role=DESC, ps="### 4.5"),
    c("d5_unp", "hyp §0.3D", "UNPARSEABLE rows", "188", J(f"{D5}/results/testability_FREE_v2.json", "all_rows.label_counts.UNPARSEABLE"), role=DESC, ps="### 4.5"),
    c("d5_noout", "hyp §0.3D", "NO_OUTPUT rows", "199", J(f"{D5}/results/testability_FREE_v2.json", "all_rows.label_counts.NO_OUTPUT"), role=DESC, ps="### 4.5"),
    c("d5_cor", "hyp §0.3D", "CORRECT rows (empty class)", "0", J(f"{D5}/results/testability_FREE_v2.json", "all_rows.n_CORRECT"), role=DESC),
    c("d5_false", "hyp §0.3D", "false ERROR_CERT on SIG-CORRECT (nonce)", "0", J(f"{D5}/results/soundness_audit.json", "i_sig_replay.nonce.ERROR_CERT_false_error_rate_on_SIG_CORRECT"), role=DESC),
    c("d5_1595", "hyp §0.3D", "SIG-CORRECT rows replayed", "1,595", J(f"{D5}/results/soundness_audit.json", "i_sig_replay.nonce.n_CORRECT"), role=DESC, ps="### 4.5"),
    c("d5_resc_n", "hyp §0.3D", "known-ERROR rescue (nonce)", "9%", J(f"{D5}/results/soundness_audit.json", "i_sig_replay.nonce.rescue_rate_on_SIG_ERROR (non-identity equivalent map exists)"), role=DESC),
    c("d5_resc_s", "hyp §0.3D", "known-ERROR rescue (synonym)", "10%", J(f"{D5}/results/soundness_audit.json", "i_sig_replay.syn.rescue_rate_on_SIG_ERROR (non-identity equivalent map exists)"), role=DESC),
    c("d5_t8", "hyp §0.3D", "rescue template T8 (nonce)", "0.27", J(f"{D5}/results/soundness_audit.json", "i_sig_replay.nonce.rescue_by_template.T8"), role=DESC),
    c("d5_t9n", "hyp §0.3D", "rescue template T9 (nonce)", "0.37", J(f"{D5}/results/soundness_audit.json", "i_sig_replay.nonce.rescue_by_template.T9"), role=DESC),
    c("d5_t9s", "hyp §0.3D", "rescue template T9 (synonym)", "0.43", J(f"{D5}/results/soundness_audit.json", "i_sig_replay.syn.rescue_by_template.T9"), role=DESC),
    c("d5_prec", "hyp §0.3D", "ERROR_CERT executor-audit precision", "0.867", J(f"{D5}/results/soundness_audit.json", "ii_executor_audit.ERROR_CERT.implied_precision_not_rated_faithful"), "[0.76, 0.93]", J(f"{D5}/results/soundness_audit.json", "ii_executor_audit.ERROR_CERT.ci"), role=DESC, ps="### 4.5"),
    c("d5_mapped_f", "hyp §0.3D", "MAPPED faithful share (audit)", "0.867", J(f"{D5}/results/soundness_audit.json", "ii_executor_audit.MAPPED.share_faithful (upper bound of CORRECT precision if the gloss check accepted every MAPPED row)"), role=DESC),
    c("d5_707", "hyp §0.3D", "old iter-3 ERROR labels that are MAPPED (UP TO, upper bound)", "70.7%", X("a/b", a=J(f"{D5}/results/old_label_agreement.json", "agreement_table_old_tierA_vs_new.ERROR|MAPPED"), b=J(f"{D5}/results/old_label_agreement.json", "old_label_counts_on_new_rows.ERROR")), role=DESC, ps="### 4.5"),
    c("d5_kappa", "hyp §0.3D", "old/new kappa", "0.058", J(f"{D5}/results/old_label_agreement.json", "kappa_old_vs_new_search_view"), role=DESC),
    c("d5_seal_all", "hyp §0.1", "seal prefix, all rows", "9609ebbb", {"t": "regex", "f": f"{D5}/results/seal.json", "pat": r'"label_vector_sha256_all_rows": "([0-9a-f]{8})'}, role=DESC),
    c("d5_seal_unt", "hyp §0.1", "seal prefix, untouched subset", "b364a49a", {"t": "regex", "f": f"{D5}/results/seal.json", "pat": r'"(b364a49a)[0-9a-f]+"'}, role=DESC),
    c("d5_untouched", "hyp §0.1", "R_COMP FREE untouched rows", "2,198", J(f"{D5}/results/old_label_agreement.json", "untouched"), role=DESC),
    # ---------------- §0.3E eval 3 ----------------
    c("e3_77", "hyp §0.3E", "9-family: non-agreeing peers of CORRECT candidates labelled ERROR", "77%",
      X("a/b", a=C(f"{EV3}/tables/p1_class_shares.csv", {"pool": "9fam", "pair_set": "disagreeing_CORRECT_cand_pairs", "peer_label": "ERROR"}, "n_pairs"),
        b=C(f"{EV3}/tables/p1_class_shares.csv", {"pool": "9fam", "pair_set": "disagreeing_CORRECT_cand_pairs", "peer_label": "ALL"}, "n_pairs"))),
    c("e3_61", "hyp §0.3E", "3-pool: non-agreeing peers of CORRECT candidates labelled ERROR", "61%",
      X("a/b", a=C(f"{EV3}/tables/p1_class_shares.csv", {"pool": "3pool", "pair_set": "disagreeing_CORRECT_cand_pairs", "peer_label": "ERROR"}, "n_pairs"),
        b=C(f"{EV3}/tables/p1_class_shares.csv", {"pool": "3pool", "pair_set": "disagreeing_CORRECT_cand_pairs", "peer_label": "ALL"}, "n_pairs"))),
    c("e3_9", "hyp §0.3E", "CORRECT-CORRECT disagreements that are vocabulary-resolvable (9-family)", "9%", C(f"{EV3}/tables/p1_class_shares.csv", {"pool": "9fam", "pair_set": "disagreeing_CORRECT_cand_pairs", "peer_label": "CORRECT"}, "share_VOCAB")),
    c("e3_irr", "hyp §0.3E", "pair class IRREDUCIBLE (9-family, all pairs)", "69.4%", C(f"{EV3}/tables/p1_class_shares.csv", {"pool": "9fam", "pair_set": "all_pairs", "peer_label": "ALL"}, "share_IRREDUCIBLE")),
    c("e3_exact", "hyp §0.3E", "pair class EXACT", "13.6%", C(f"{EV3}/tables/p1_class_shares.csv", {"pool": "9fam", "pair_set": "all_pairs", "peer_label": "ALL"}, "share_EXACT")),
    c("e3_align", "hyp §0.3E", "pair class ALIGN_ONLY", "15.1%", C(f"{EV3}/tables/p1_class_shares.csv", {"pool": "9fam", "pair_set": "all_pairs", "peer_label": "ALL"}, "share_ALIGN_ONLY")),
    c("e3_vocab", "hyp §0.3E", "pair class VOCAB", "1.6%", C(f"{EV3}/tables/p1_class_shares.csv", {"pool": "9fam", "pair_set": "all_pairs", "peer_label": "ALL"}, "share_VOCAB")),
    c("e3_name", "hyp §0.3E", "pair class NAME_ONLY", "0.3%", C(f"{EV3}/tables/p1_class_shares.csv", {"pool": "9fam", "pair_set": "all_pairs", "peer_label": "ALL"}, "share_NAME_ONLY")),
    c("e3_oracle3", "hyp §0.3E", "no-anchoring oracle d floor, 3-pool", "0.385", J(f"{EV3}/results/part1.json", "pools.3pool.d_R_oracle"), ps="### 4.6"),
    c("e3_oracle_l25", "hyp §0.3E", "oracle d floor, L25", "0.542", C(f"{EV3}/tables/p1_rule_cuts.csv", {"pool": "3pool", "rule": "R_oracle", "dim": "stratum", "cell": "L25"}, "d")),
    c("e3_endmaj_l25", "hyp §0.3E", "END_MAJ d, L25 (3-pool)", "0.735", C(f"{EV3}/tables/p1_rule_cuts.csv", {"pool": "3pool", "rule": "R_align", "dim": "stratum", "cell": "L25"}, "d")),
    c("e3_oracle9", "hyp §0.3E", "oracle d floor, 9-family", "0.586", J(f"{EV3}/results/part1.json", "pools.9fam.d_R_oracle"), ps="### 4.6"),
    c("e3_endmaj9", "hyp §0.3E", "END_MAJ d, 9-family", "0.537", J(f"{EV3}/results/part1.json", "G0.d_END_MAJ_matrix"), ps="### 4.6"),
    c("e3_br_lo", "hyp §0.3E", "instrument bracket low", "0.396", J(f"{EV3}/results/part1.json", "pools.3pool.d_bracket", idx=0), ps="### 4.6"),
    c("e3_br_hi", "hyp §0.3E", "instrument bracket high (= END_MAJ d 3-pool)", "0.415", J(f"{EV3}/results/part1.json", "pools.3pool.d_bracket", idx=1), ps="### 4.6"),
    c("e3_pred", "review crit 5", "R_point_label predicted d_floor (3-pool)", "0.402", C(f"{EV3}/tables/p1_rule_cuts.csv", {"pool": "3pool", "rule": "R_point_label", "dim": "ALL", "cell": "ALL"}, "d"), ps="### 4.6"),
    c("e3_denom", "hyp §0.3E", "gap_closed denominator (END_MAJ − prediction)", "0.013", J(f"{EV3}/results/part1.json", "pools.3pool.Delta_d_vs_pool_END_MAJ.R_point_label")),
    c("e3_pred_rate", "hyp §0.3E", "predicted FREE endorsement (R_point_MC)", "0.20", J(f"{EV3}/results/part2.json", "validation.R_point_MC.pred_rate")),
    c("e3_sig_rate", "hyp §0.3E", "actual SIG endorsement", "0.575", J(f"{EV3}/results/part2.json", "row_endorsement_rates.end_maj_sig")),
    c("e3_calib", "hyp §0.3E", "calibration error of the Part-1 method", "−0.372", J(f"{EV3}/results/part2.json", "validation.R_point_MC.calib_err.mean"), "[−0.423, −0.323]", J(f"{EV3}/results/part2.json", "validation.R_point_MC.calib_err.ci"), ps="### 4.6"),
    c("e3_drop", "hyp §0.3E", "SIG − FREE exact agreement drop (upper bound; D7)", "+0.479", J(f"{EV3}/results/part2.json", "drop_pairs.exact.overall.mean"), "[0.447, 0.513]", J(f"{EV3}/results/part2.json", "drop_pairs.exact.overall.ci"), ps="### 4.6"),
    c("e3_sigx", "hyp §0.3E", "pairwise exact agreement SIG", "0.528", J(f"{EV3}/results/part2.json", "agreement_rates_pairs.sig_exact.mean")),
    c("e3_freex", "hyp §0.3E", "pairwise exact agreement FREE", "0.048", J(f"{EV3}/results/part2.json", "agreement_rates_pairs.free_exact.mean")),
    c("e3_nontrans", "hyp §0.3E", "FREE non-transitivity rate (separate diagnostic)", "0.131", J(f"{EV3}/results/part2.json", "nontransitivity.FREE.rate"), ps="### 4.6"),
    c("e3_683", "hyp §0.3E", "0.683 = d under the exact rule on E's 3-pool (NOT an AUROC)", "0.683", C(f"{EV3}/tables/p1_rule_cuts.csv", {"pool": "3pool", "rule": "R_exact", "dim": "ALL", "cell": "ALL"}, "d"), ps="### 4.6"),
    c("e3_vres", "hyp §0.3E", "c_vres − c_score_align on L25 (9-family)", "−0.014", J(f"{EV3}/results/part1.json", "pools.9fam.c_vres.L25.delta_strat_auroc_vres_minus_frozen"), "[−0.028, −0.001]", J(f"{EV3}/results/part1.json", "pools.9fam.c_vres.L25.delta_strat_auroc_vres_minus_frozen_ci")),
    c("e3_net_lo", "hyp §0.3E", "NET under every rule, low end (9-family R_align)", "+0.35", J(f"{EV3}/results/part1_net.json", "9fam|R_align.full_B2000_delta.words_T3_minus_T1.delta_e_plus_d")),
    c("e3_net_hi", "hyp §0.3E", "NET under every rule, high end (3-pool R_align)", "+0.39", J(f"{EV3}/results/part1_net.json", "3pool|R_align.full_B2000_delta.words_T3_minus_T1.delta_e_plus_d")),
    c("e3_200", "hyp §0.3E", "R_COMP FREE needs ≥ 200 CORRECT rows (scenario grid max)", "200", K(200, "design threshold stated in eval-3 README Part 3; no single cell"), role=DESC),
    # ---------------- §0.3F spend ----------------
    c("sp_d5", "hyp §0.3F", "dataset-5 spend", "$0", {"t": "ledger", "f": f"{D5}/cost_ledger.jsonl", "field": "cost_usd"}, role=DESC),
    c("sp_d4", "hyp §0.3F", "dataset-4 ledger sum", "$0.241", {"t": "ledger", "f": f"{D4}/cost_ledger.jsonl", "field": "cost_usd"}, role=DESC),
    c("sp_x9", "hyp §0.3F", "exp-9 ledger sum", "$0.108", {"t": "ledger", "f": f"{X9}/results/api_cost_ledger.jsonl", "field": "usd"}, role=DESC),
    # ---------------- review-only paper checks ----------------
    c("rv_frontier_ratio", "review crit 11", "'96% of frontier' (point estimate only)", "0.957", J(E6, "d_frontier.ratio.ratio"), "[0.887, 1.034]", J(E6, "d_frontier.ratio.ci"), ps="## What we have learned"),
    c("rv_spend3", "review crit 11", "§3.6 iteration-3 spend statement vs ledger sum", "$4.33", C(CU, {"artifact": "iteration 3"}, "value"), role=DESC, ps="### 3.6", pp=(r"Total: approximately \$(\d+\.\d+) plus T1", 1)),
    c("rv_k3_cost", "review crit 11", "§3.5 k=3 $ per sentence (paper says $0.000073)", "$0.000946", C(CU, {"item": "k-pool k=3.0"}, "value"), role=DESC, ps="### 3.5", pp=(r"\| 3 \| 0\.757 \| \$(0\.\d+) \|", 1)),
    c("rv_frontier_x", "review crit 11", "frontier judge $/item ÷ consensus $/item (per ITEM; §3.3's '6.07×' mixed units)", "30.2", X("a/b", a=C(CU, {"item": "strong"}, "value"), b=C(CU, {"item": "consensus c_score_align"}, "value")), role=DESC, ps="### 3.3", pp=(r"\((\d+\.\d+)× the consensus generation cost\)", 1)),
    c("rv_csc_ci_rev", "review crit 2", "reviewer's own sentence-cluster CI for c_csc (B = 300; the paper transcribes T4)", "0.614", J(f"{REVA}/recompute_csc.json", "c_csc.strat"), "[0.501, 0.728]", J(f"{REVA}/recompute_csc.json", "c_csc.ci_B300"), role=DESC),
    c("rv_compound_ci", "review crit 2", "T9 COMPOUND e_CSC with CI", "0.282", J(A9, f"e_anchoring_by_error_class.PRIMARY.COMPOUND.CSC.e"), "[0.182, 0.382]", J(A9, "e_anchoring_by_error_class.PRIMARY.COMPOUND.CSC.e_ci")),
    c("rv_mde_d4", "review crit 7", "E2 L25 MDE80 at 350 as stated by dataset 4 (eval 3 gives 0.110 with its SE model)", "0.112", J(f"{D4}/testability_E2.json", "expected_power_if_completed.L25_350"), role=DESC, ps="### 4.4"),
    c("rv_swap_nf", "review crit 10", "c_nf SWAP recall at the PRIMARY threshold (the reason the paper gave)", "0.512", C(f"{E8}/perturb_sensitivity.csv", {"metric": "c_nf", "operator": "SWAP", "polarity": "ALL", "subset": "E_bases"}, "recall_primary")),
    c("rv_k1_cost", "review crit 1", "§3.5 k=1 cost column (paper says $0.000024 per sentence)", "$0.000315", C(CU, {"item": "k-pool k=1.0"}, "value"), role=DESC, ps="### 3.5", pp=(r"\| 1 \| 0\.685 \| \$(0\.\d+) \|", 1)),
    c("rv_k7_cost", "review crit 1", "§3.5 k=7 cost column (paper says $0.000170 per sentence)", "$0.002206", C(CU, {"item": "k-pool k=7.0"}, "value"), role=DESC, ps="### 3.5", pp=(r"\| 7 \| 0\.784 \| \$(0\.\d+) \|", 1)),
    c("rv_gloss_usd", "review crit 7", "R_COMP FREE gloss resume cost estimate (~$1.8)", "$1.8", {"t": "regex", "f": f"{D5}/README.md", "pat": r"budget is available \(~\$(\d\.\d)\)"}, role=DESC),
]
