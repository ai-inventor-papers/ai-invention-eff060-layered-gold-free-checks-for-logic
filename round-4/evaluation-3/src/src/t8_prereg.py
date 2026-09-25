#!/usr/bin/env python3
"""STEP 2: write prereg_d_split.json + prereg_d_split.sha256 BEFORE any Part-1 number is computed.

Contains no path to (and never reads) the sibling CSC experiment workspace."""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from t8_paths import E8, EV2, ROOT  # noqa: E402


def over_align() -> float:
    """exp 8 analysis_hyb.json new_agreement_audit.label_discordance.NEW_hyb_not_align.rate (0.388; ALIGN_agree 0.127)."""
    d = json.loads((E8 / "results" / "analysis_hyb.json").read_text())
    return float(d["new_agreement_audit"]["label_discordance"]["NEW_hyb_not_align"]["rate"])


def main() -> None:
    pm = json.loads((EV2 / "prereg_mech.json").read_text())
    OVER_ALIGN = over_align()
    hyb = json.loads((E8 / "results" / "analysis_hyb.json").read_text())["new_agreement_audit"]["label_discordance"]
    pre = {
        "title": "T8 PART 1 pre-registration: vocabulary-resolvable vs irreducible split of END_MAJ d, and the CSC d prediction",
        "written_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "status": "written BEFORE any Part-1 number (pair classes, rules, predictions) is computed; the sibling CSC experiment's outputs are never read",
        "development_data_caveat": "Dataset E and R_COMP are DEVELOPMENT data (scored in iterations 2-3). Everything in Parts 1-2 is mechanism/selection evidence, not confirmation; claims wait for E2 (iteration 5).",
        "conventions": {"y": "1 = ERROR, 0 = CORRECT",
                        "population": "R_AB E_POOL (tiers A+B, CONTESTED and reading_choice excluded, llm rows; eval-2 frame.regime), consensus-scorable = npc >= 2 family-disjoint peers",
                        "bootstrap": "sentence-cluster, B = 2000, seed 0, percentile 2.5/97.5 (eval-2 stats.SentBoot)",
                        "strat": "within-stratum pair-weighted AUROC (eval-2 stats.strat_auc)",
                        "unknown": "UNKNOWN / timeout pairs = NOT equivalent (as in the frozen score)"},
        "pair_classes_precedence": {
            "EXACT": "same node, or eval-2 matrix reason 'exact'",
            "NAME_ONLY": "not EXACT; z3-exact-equivalent (3 s, UNKNOWN = no) after predicate and constant symbols of BOTH formulas are rewritten with mechanism.normalise_name (lowercase, strip non-alphanumerics); arity must agree; a normalised-symbol collision inside ONE formula disqualifies the pair",
            "ALIGN_ONLY": "eval-2 matrix eq True with reason 'align' (or 'gran'), not in the classes above",
            "VOCAB": "exp-8 pairs_E nf_eq OR hyb_eq True, not in the classes above",
            "IRREDUCIBLE": "none of the above"},
        "reported_shares": ["all pairs", "pairs of CORRECT candidates", "disagreeing pairs of CORRECT candidates (END_MAJ not equivalent)",
                            "each split by the peer's own label (CORRECT / ERROR / unlabelled)"],
        "rules": {
            "R_exact": "agree = EXACT",
            "R_align": "agree = EXACT or ALIGN (= END_MAJ; must reproduce d = 0.537)",
            "R_name": "agree = EXACT or NAME_ONLY or ALIGN",
            "R_liberal": "R_name plus every VOCAB pair (LOWER bound on reachable d)",
            "R_point_MC": f"R_name plus each VOCAB pair accepted with probability 1 - {OVER_ALIGN} = {1 - OVER_ALIGN:.3f}; 500 Monte-Carlo draws (seed 0); mean and 2.5-97.5 band combined with the bootstrap",
            "R_point_label (PRIMARY point prediction; ORACLE-ASSISTED, never a gold-free metric)": f"R_name plus VOCAB pairs only where the peer is labelled CORRECT (CORRECT candidates) or both rows are ERROR with the same error_ops class (ERROR candidates); unlabelled peers accepted with probability {1 - OVER_ALIGN:.3f} (MC as above)",
            "R_oracle (no-anchoring floor)": "a CORRECT candidate is endorsed iff > half of its family-disjoint peers are labelled CORRECT in R_AB; unlabelled / CONTESTED / reading_choice peers count as non-agreeing; variant drops them from the denominator; ERROR candidates: endorsed iff > half of peers are ERROR in the same error_ops class (descriptive)",
            "endorsement": "endorsed iff #agreeing peers > npc/2"},
        "vocab_discount": {"value": OVER_ALIGN, "accept_prob": 1 - OVER_ALIGN, "source": f"{E8}/results/analysis_hyb.json :: new_agreement_audit.label_discordance.NEW_hyb_not_align.rate",
                           "align_reference_rate": hyb["ALIGN_agree"]["rate"]},
        "outputs": {"d_floor_pred": "d under R_point_label, bracket [d(R_liberal), d(R_name)], plus d(R_exact), d(R_oracle)",
                    "e_ceiling_pred": "e under R_point_label, bracket [e(R_name), e(R_liberal)]",
                    "Delta_d(rule)": "0.537 - d(rule)", "Delta_e(rule)": "e(rule) - 0.124",
                    "c_vres": "1 - (#agreeing peers under R_liberal) / npc (label-free); strat and pooled AUROC on R_AB and L25 next to c_score_align (predicted no-anchoring CSC AUROC, pre-check of G2)"},
        "cuts": {"words_tercile_cuts": pm["cuts"]["words_tercile_cuts"], "words_tercile_rule": pm["cuts"]["words_tercile_rule"],
                 "n_conditions_bins": pm["cuts"]["n_conditions_bins"], "strata": ["L25", "L20", "EXC", "CTRL", "long pool L25+L20+EXC"],
                 "min_cell": {"rows": 30, "sentences": 10, "source": "mechanism.MIN_ROWS / MIN_SENT"},
                 "copied_from": f"{EV2}/prereg_mech.json"},
        "slopes": {"model": "not_endorsed ~ z(words) + C(stratum) among CORRECT rows, per rule (mechanism.gee_fit: binomial logit, exchangeable, robust SE, sentence clusters)",
                   "slope_difference": "d_slope(R_align) - d_slope(R_point_label), cluster-bootstrap CI",
                   "NET": "Delta(e+d) words T3 - T1 per rule (mechanism.net_test)"},
        "pools": {"PRIMARY": "matched 3-family pool {deepseek, microsoft, openai} minus the candidate's own family (same family column and rule as m4.pool_scores / m4_fixed_pools_k3); rows with < 1 available pool row excluded and counted; endorsement needs > half of the available pool rows",
                  "SECONDARY": "all 9 vendor families (eval-2 family-disjoint peers)"},
        "specificity_placebo": {"draw": "within each sentence, the same number of IRREDUCIBLE pairs as VOCAB pairs, counted as agreements; 200 draws (seed 0)",
                                "ratio": "(Delta_d / Delta_e)_VOCAB / (Delta_d / Delta_e)_random with CI",
                                "reading": "ratio well above 1 = vocabulary agreements concentrated among correct translations; ~1 = indiscriminate (CSC raises e as fast as it lowers d)"},
        "decision_rule_verbatim": {
            "gap_closed": "(0.537_matched - d_CSC) / (0.537_matched - d_floor_pred_matched), where 0.537_matched is the 3-pool END_MAJ d computed here",
            "thresholds": {">= 0.67": "vocabulary divergence was the main cause", "<= 0.33": "it was not", "between": "partial"},
            "anchoring": "d_CSC < d(R_oracle) -> 'below the no-anchoring floor: anchoring (peers copying the candidate) is contributing', read with the sibling's e",
            "one_sentence": "If CSC's measured d lands near d_floor_pred (gap_closed >= 0.67), vocabulary divergence was the cause; if it lands near 0.537 (gap_closed <= 0.33), it was not."},
        "validation_criterion_part2": {"method": "apply the Part-1 pair classes to R_COMP FREE (NAME_ONLY via z3 normalisation; VOCAB via exp-7 peer_equal_nf) and predict the endorsement rate under R_name / R_liberal / R_point_MC",
                                       "target": "ACTUAL SIG END_MAJ-exact endorsement rate on the same (sentence, slot) rows",
                                       "report": "calibration error (predicted - actual) with sentence-cluster CI per template; Spearman across the 9 templates",
                                       "pass": "|error| <= 0.05 -> 'validated on R_COMP' (validates vocabulary sharing in general, NOT CSC's anchoring)"},
        "power_grid": {"effect": "strat Delta = strat AUROC(c_score_align) - strat AUROC(comparator); comparators flash-lite disguised (PRIMARY), flash-lite original, nano original",
                       "cells": ["L25", "L20", "EXC", "CTRL", "long", "all"],
                       "n_sent": [40, 60, 80, 100, 125, 150, 200, 250, 300, 400, 500], "B": 1000,
                       "MDE80": "2.80 x SE (two-sided alpha 0.05); one-sided 2.49 x SE",
                       "power_at": [0.05, 0.069, 0.099, 0.10, 0.15],
                       "planned_E2": {"L25": [250, 300, 350, 400], "EXC": [75, 100], "L20": [50], "DT": [100]},
                       "DT_yields": ["CTRL yield", 0.3, 0.5, 0.8],
                       "verdict": "ADEQUATE (MDE80 <= 0.10 and power at 0.069 >= 0.5) / MARGINAL (MDE80 <= 0.15 or power at 0.069 >= 0.3) / UNDERPOWERED",
                       "rcomp_free_scenarios": {"n_err": [420, 600, 900], "n_cor": [34, 100, 200, 400, 800], "n_sent": 221}},
        "gates": {"G0": "row_consensus over pairwise_classes_E reproduces e = 0.124, d = 0.537 (|diff| <= 0.002), c_exact AUROC 0.748, c_align AUROC 0.784 (<= 0.002)",
                  "G1": "pairs_E join coverage >= 0.95 of (R_AB candidate, family-disjoint peer) pairs, else primary restricted to rows with 100% coverage",
                  "G2": "concordance of exp-8 align_eq vs eval-2 matrix eq on joined pairs; the matrix wins",
                  "G3": "recomputed R_COMP matrix reproduces exp-7 c_score_sig (SIG exact) and c_score_align (SIG, FREE) on >= 99% of rows within 1e-6"},
    }
    p = ROOT / "prereg_d_split.json"
    txt = json.dumps(pre, indent=1, ensure_ascii=False)
    assert "gen_art_experiment_9" not in txt and "gen_art_experiment_10" not in txt
    p.write_text(txt)
    h = hashlib.sha256(p.read_bytes()).hexdigest()
    (ROOT / "prereg_d_split.sha256").write_text(f"{h}  prereg_d_split.json\n")
    print(h)


if __name__ == "__main__":
    main()
