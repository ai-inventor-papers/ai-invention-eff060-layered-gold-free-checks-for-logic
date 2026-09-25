#!/usr/bin/env python3
"""eval_out.json (exp_eval_sol_out): flat metrics_agg + one example per R_AB consensus-scorable E row and per R_COMP row."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from t8_paths import RESD, ROOT  # noqa: E402


def f(x):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else float(x)


def main() -> None:
    p1 = json.loads((RESD / "part1.json").read_text())
    p2 = json.loads((RESD / "part2.json").read_text())
    p3 = json.loads((ROOT / "power_E2.json").read_text())
    p4 = json.loads((RESD / "part4.json").read_text())
    au = json.loads((ROOT / "audit/rederive.json").read_text())
    net = json.loads((RESD / "part1_net.json").read_text())
    shares = pd.read_csv(ROOT / "tables/p1_class_shares.csv", comment="#")
    M = {"p1_G0_e_END_MAJ": p1["G0"]["e_END_MAJ_matrix"], "p1_G0_d_END_MAJ": p1["G0"]["d_END_MAJ_matrix"],
         "p1_G0_auroc_c_exact": p1["G0"]["auroc_c_exact"], "p1_G0_auroc_c_align": p1["G0"]["auroc_c_align_frozen"],
         "p1_G1_pairs_E_coverage": p1["G1"]["overall"], "p1_G2_align_concordance": p1["G2"]["agreement"],
         "p1_n_scorable_rows": p1["G0"]["n_scorable"], "p1_n_peer_pairs": sum(p1["n_pairs_by_class"].values())}
    for pool in ("3pool", "9fam"):
        pp = p1["pools"][pool]
        h = pp["heads"]
        M[f"p1_d_floor_pred_{pool}"] = pp["d_floor_pred"]
        M[f"p1_d_floor_pred_{pool}_ci_lo"], M[f"p1_d_floor_pred_{pool}_ci_hi"] = pp["d_floor_pred_ci"]
        for r in ("R_exact", "R_align", "R_name", "R_liberal", "R_oracle", "R_oracle_labdenom", "R_point_MC", "R_point_label"):
            M[f"p1_d_{r}_{pool}"] = h[r]["d"]
            M[f"p1_e_{r}_{pool}"] = h[r]["e"]
        M[f"p1_e_ceiling_pred_{pool}"] = pp["e_ceiling_pred"]
        M[f"p1_gap_rule_d_CSC_at_gap067_{pool}"] = pp["decision_rule"]["d_CSC_for_gap_0.67"]
        M[f"p1_gap_rule_d_CSC_at_gap033_{pool}"] = pp["decision_rule"]["d_CSC_for_gap_0.33"]
        M[f"p1_gap_rule_denominator_{pool}"] = pp["decision_rule"]["d_matched"] - pp["decision_rule"]["d_floor_pred_matched"]
        M[f"p1_specificity_ratio_{pool}"] = pp["placebo"]["specificity_ratio"]
        M[f"p1_placebo_delta_d_vocab_{pool}"] = pp["placebo"]["delta_d_vocab"]
        M[f"p1_placebo_delta_d_random_{pool}"] = pp["placebo"]["delta_d_random_mean"]
        for cell in ("R_AB", "L25"):
            M[f"p1_c_vres_auroc_{cell}_{pool}"] = pp["c_vres"][cell]["auroc_c_vres"]
            M[f"p1_c_vres_strat_auroc_{cell}_{pool}"] = pp["c_vres"][cell]["strat_auroc_c_vres"]
            M[f"p1_c_vres_minus_c_align_auroc_{cell}_{pool}"] = pp["c_vres"][cell]["delta_auroc_vres_minus_frozen"]
        s = shares[(shares.pool == pool) & (shares.pair_set == "disagreeing_CORRECT_cand_pairs")]
        tot = s[s.peer_label == "ALL"].n_pairs.iloc[0]
        M[f"p1_disagreeing_cor_pairs_peer_ERROR_share_{pool}"] = float(s[s.peer_label == "ERROR"].n_pairs.iloc[0] / tot)
        M[f"p1_disagreeing_cor_pairs_peer_CORRECT_share_{pool}"] = float(s[s.peer_label == "CORRECT"].n_pairs.iloc[0] / tot)
        M[f"p1_vocab_share_in_disagreeing_cor_cor_pairs_{pool}"] = float(s[s.peer_label == "CORRECT"].share_VOCAB.iloc[0])
        for rule in ("R_align", "R_point_label_draw0", "R_liberal", "R_oracle"):
            M[f"p1_net_words_{rule}_{pool}"] = net[f"{pool}|{rule}"]["full_B2000_delta"]["words_T3_minus_T1"]["delta_e_plus_d"]
    M["p1_c_vres_strat_auroc_L25"] = M["p1_c_vres_strat_auroc_L25_9fam"]
    M["p1_specificity_ratio"] = M["p1_specificity_ratio_3pool"]
    sd = p2["SIG_ed"]["END_MAJ_align"]
    M.update({"p2_G3_match_sig_exact": p2["G3"]["SIG|c_score_sig"]["match_rate"], "p2_G3_match_sig_align": p2["G3"]["SIG|c_score_align"]["match_rate"],
              "p2_G3_match_free_align": p2["G3"]["FREE|c_score_align"]["match_rate"], "p2_sig_e": sd["e"], "p2_sig_d": sd["d"],
              "p2_sig_auroc_b": sd["auroc_b"]})
    for r in p2["SIG_d_by_reading"]:
        if r["rule"] == "END_MAJ_align" and r["cell"] in ("weak", "strong"):
            M[f"p2_sig_d_{r['cell']}"] = r["d"]
    sc = p2.get("SIG_scatter", {}).get("overall", {})
    if "ratio_SI_cor_over_SI_err_same_sentences" in sc:
        M["p2_SI_ratio"] = sc["ratio_SI_cor_over_SI_err_same_sentences"]["ratio"]
        M["p2_SI_err"] = sc["SI_err"]["mean"]
        M["p2_SI_cor"] = sc["SI_cor"]["mean"]
    for rule in ("exact", "align", "NF", "align_or_NF"):
        M[f"p2_drop_{rule}_mean"] = p2["drop_pairs"][rule]["overall"]["mean"]
    for k, v in p2["agreement_rates_pairs"].items():
        M[f"p2_agree_{k}"] = v["mean"]
    for k, v in p2["recovered_share"].items():
        M[f"p2_recovered_share_{k}"] = v["share"]
    for k, v in p2["row_endorsement_drop"].items():
        M["p2_row_endorse_drop_" + k.replace(" - ", "_minus_")] = v["mean"]
    for rule in ("R_align", "R_name", "R_liberal", "R_point_MC"):
        M[f"p2_validation_calib_err_{rule}"] = p2["validation"][rule]["calib_err"]["mean"]
        M[f"p2_validation_pred_rate_{rule}"] = p2["validation"][rule]["pred_rate"]
    M["p2_validation_actual_SIG_rate"] = p2["validation"]["actual_SIG_exact_rate"]
    M["p2_validation_calib_err"] = M["p2_validation_calib_err_R_point_MC"]
    M["p2_free_tierA_d_END_MAJ"] = p2["FREE_tierA"]["END_MAJ_align"]["d"]
    M["p2_free_tierA_e_END_MAJ"] = p2["FREE_tierA"]["END_MAJ_align"]["e"]
    M["p2_nontransitivity_SIG"] = p2["nontransitivity"]["SIG"]["rate"]
    M["p2_nontransitivity_FREE"] = p2["nontransitivity"]["FREE"]["rate"]
    for r in p3["planned_E2"]:
        if r["cell"] == "L25" and r["comparator"] == "flashlite_disg":
            M[f"p3_mde80_L25_{r['planned_sentences']}"] = r["mde80"]
            M[f"p3_power069_L25_{r['planned_sentences']}"] = r["power_at_0.069"]
        if r["cell"] in ("EXC", "L20") and r["comparator"] == "flashlite_disg":
            M[f"p3_mde80_{r['cell']}_{r['planned_sentences']}"] = r["mde80"]
    for st, v in p3["yield"].items():
        M[f"p3_yield_{st}"] = v["yield"]
    nn = p3["n_needed"]["L25"]["flashlite_disg"]
    M["p3_n_for_mde_0p069_L25"] = nn["planned_for_mde_0.069"]
    M["p3_n_usable_for_mde_0p069_L25"] = nn["usable_for_mde_0.069"]
    M["p3_n_usable_for_mde_0p069_long"] = p3["n_needed"]["long"]["flashlite_disg"]["usable_for_mde_0.069"]
    M["p3_se_slope_b_L25"] = p3["se_fit"]["L25|flashlite_disg"]["b"]
    M["p3_criterion_c_optimistic_effect"] = p3["criterion_c_effects"]["optimistic"]["value"]
    M.update({"p4_n_claims": p4["n_claims"], "p4_n_match": p4["n_match"], "p4_n_mismatches": p4["n_mismatch"],
              "p4_n_not_in_files": p4["n_not_in_files"], "audit_n_checks": au["n_checks"], "audit_n_pass": au["n_pass"]})
    M = {k: float(v) for k, v in M.items() if v is not None and np.isfinite(v)}
    # ---------------- examples
    P = pd.read_pickle(RESD / "part1_rows.pkl")
    exE = []
    for r in P.itertuples():
        d = r._asdict()
        inp = {"sentence_id": r.sentence_id, "row_key": r.row_key, "stratum": r.stratum, "words": int(r.words), "n_conditions": int(r.n_conditions),
               "family": r.family_vendor, "candidate_fol": r.candidate_fol}
        ex = {"input": json.dumps(inp, ensure_ascii=False), "output": "ERROR" if r.y_AB == 1 else "CORRECT",
              "metadata_sentence_id": r.sentence_id, "metadata_stratum": r.stratum, "metadata_words": int(r.words),
              "metadata_n_conditions": int(r.n_conditions), "metadata_label": "ERROR" if r.y_AB == 1 else "CORRECT", "metadata_npc": int(r.npc)}
        for c in ("EXACT", "NAME_ONLY", "ALIGN_ONLY", "VOCAB", "IRREDUCIBLE"):
            ex[f"metadata_n_pairs_{c}"] = int(d.get(c, 0) or 0) if not pd.isna(d.get(c, 0)) else 0
            v = d.get(f"{c}_3pool", 0)
            ex[f"metadata_n_pairs_{c}_3pool"] = 0 if v is None or pd.isna(v) else int(v)
        for pool in ("9fam", "3pool"):
            for rule in ("R_exact", "R_align", "R_name", "R_point_label", "R_liberal", "R_oracle"):
                v = d.get(f"en_{pool}_{rule}")
                ex[f"predict_endorse_{rule}_{pool}"] = "NA" if v is None or pd.isna(v) else f"{v:.4f}"
            v = d.get(f"c_vres_{pool}")
            ex[f"predict_c_vres_{pool}"] = "NA" if v is None or pd.isna(v) else f"{v:.4f}"
        ex["eval_y_error"] = float(r.y_AB)
        exE.append(ex)
    C = pd.read_pickle(RESD / "part2_rows.pkl")
    exR = []
    for r in C.itertuples():
        inp = {"sentence_id": r.sentence_id, "row_key": r.row_key, "condition": r.condition, "template_id": r.template_id, "slot": r.slot, "family": r.family}
        ex = {"input": json.dumps(inp), "output": str(r.label), "metadata_condition": r.condition, "metadata_template_id": r.template_id,
              "metadata_slot": r.slot, "metadata_is_peer": bool(r.is_peer) if not pd.isna(r.is_peer) else False,
              "metadata_npc": None if pd.isna(r.npc) else int(r.npc)}
        for nm, v in (("endorse_END_MAJ_align", r.end_maj), ("endorse_MAJ_EXACT", r.end_maj_exact), ("c_align_recomputed", r.c_re), ("c_exact_recomputed", r.c_exact)):
            ex[f"predict_{nm}"] = "NA" if v is None or pd.isna(v) else (f"{float(v):.4f}")
        ex["eval_is_labelled"] = float(r.label in ("CORRECT", "ERROR"))
        exR.append(ex)
    out = {"metadata": {"evaluation_name": "T8: predicting the vocabulary fix (d split), R_COMP second population, iteration-5 power, verified record",
                        "cpu_only": True, "llm_calls": 0, "spend_usd": 0.0, "prereg_sha256": p1["prereg_sha256"],
                        "development_data": "E and R_COMP are development data; nothing here is confirmation",
                        "deviations": ["net_test AME refits at B = 200 (shared host); Delta(e+d) CIs at B = 2000 by vectorised code identical to net_test's first block",
                                       "gap_closed denominator tiny (0.013 3-pool): the decision rule is ill-conditioned (see record.md)",
                                       "out-of-sample validation FAILED (calibration error -0.37): Part-1 instruments under-predict what shared vocabulary does"]},
           "metrics_agg": M,
           "datasets": [{"dataset": "E_R_AB_consensus_scorable", "examples": exE}, {"dataset": "R_COMP_rows", "examples": exR}]}
    (ROOT / "eval_out.json").write_text(json.dumps(out, ensure_ascii=False))
    print(len(M), len(exE), len(exR))


if __name__ == "__main__":
    main()
