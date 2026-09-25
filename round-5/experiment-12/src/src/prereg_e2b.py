#!/usr/bin/env python3
"""E2-B step 0.5: write prereg_iter5_E2B.json + prereg_iter5_E2B.sha256 BEFORE any E2-B generation. Refuses to overwrite."""
import hashlib
import json
import sys
import time
from pathlib import Path

WS = Path(__file__).resolve().parents[1]
E2B = WS / "e2b"
P = WS / "prereg_iter5_E2B.json"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> int:
    if P.exists():
        print("prereg exists: refusing to overwrite")
        return 1
    census = json.loads((E2B / "census_E2B.json").read_text())
    pre = {
        "artifact": "E2-B: second untouched L25 replication sample (run_u75jRHUss0zo, iteration 5, gen_art_experiment_12, plan gen_plan_experiment_2)",
        "frozen_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "frozen_before": "any E2-B generation, label, judge call or metric score",
        "T0_utc": "2026-09-24T11:08:00Z",
        "deviations_declared": [
            {"id": "D-E2B", "what": "a pre-registered replication sample drawn by E2's frozen rule, beyond E2's freeze",
             "reason": "power (eval-3 power_E2.json: L25 needs ~882 planned sentences to detect +0.069 at 80%)"},
            {"id": "D-E2B-comp", "what": f"E2-B is {census['E2B']['share_25_29']:.1%} 25-29 words because the >=30 bin is exhausted after E2's surplus (census_E2B.json)",
             "handling": "word-bin strata in every AUROC; within-25-29-bin heterogeneity recheck; named as first candidate explanation of any A-vs-B heterogeneity"},
            {"id": "D-E2B-freeze-env", "what": "code_freeze_check_E2B.json: all 78 frozen files verified; or_client.py matches E2's D0 post-fix sha; pyproject/uv.lock differ from E's only in the project name and E2's added pyarrow pin"}],
        "selection": {"algorithm": "src_e2b/select_e2b.py: reproduce E2 selection (assert pool sha256 98cdccff...), then E2's 98 L25 surplus (e2_rank order), then E2's take(long_) then take(short) over sha1('E2_v1|'+sid) skipping every E2 id with accepted_grams seeded from all 658 E2 rows, to 400; reserve = next 150",
                      "expected_hashes": census["sha256"], "e2_reproduction": census["e2_reproduction"],
                      "composition": census["E2B"], "reserve_rule": "reserve used only if >10% of E2-B sentences fail gold parse or generation",
                      "batches": "sort by sha1('E2B_batch_v1|'+sid), 8 x 50; each batch is completed end to end (generation, solver labels, panel stage 1, adjudication, repair, repaired labels) or excluded entirely"},
        "label_protocol": "E2's byte-identical code (e2bsrc/, code_freeze_check_E2B.json): generation G1,G1b,G2..G9 fewshot_v1 T=0; solver labels; panel stage 1 P3+R1; adjudication P1 on disagreements; reference repair; repaired labels; E's final_rule/tiers via assemble_e2.py; rename controls via controls_e2.py; testability_e2.py; seal_e2.py + verify_seal.py",
        "drift": {"M2": "poll glob('.../iter_5/gen_art/*/e2/E2_DRIFT_DECISION.json') every 5 min, token 'aii_iter5_e2_drift_v1'; use its decision and pinned providers",
                  "fallback_at": "T+1:30 (12:38 UTC): run E2's gate.py --mode synthetic and --mode trackh (P1,P3,R1) + drift_report.py ourselves (deviation D-E2B-drift); E2 stop rule (majority agreement < 0.85 -> FAIL) AND hypothesis rule (track-H flag rate on original errors within the 95% CI of E's 0.84)",
                  "on_FAIL": "panel still runs; labels marked DRIFTED; every E2-B and union result SECONDARY; R_A reported alongside"},
        "metrics": {"contract_text_verbatim": (E2B / "contract_frozen_metric_definitions.txt").read_text(),
                    "PRIMARY": "V0 c_score_align (exp-5 pool_scoring.py leave-own-family-out, byte-identical, sha asserted)",
                    "secondary": ["PT p_peer_text (exp-5 fusion)", "V1-V5 from M1 freeze (only the carried variant is confirmatory, H-IMPROVE)", "GG (only if gg_gate PASS by T+4:00 and pilot estimate <= $0.4)"],
                    "V2_V3_V5_weights": "w_f out-of-fold over E2-B's own sentences, fold = sha1('E2_folds_v1|'+sid) % 5, shrunk with 20 pseudo-sentences (label-free); for the union recomputed out-of-fold over the union's sentences with the same recipe",
                    "V4": "coefficients from selection.json (fit on E), never refit",
                    "M1_fallback": "if no M1 by T+2:30 (13:38 UTC): V1, V2 implemented from the contract text as REPORTED-ONLY rows, V4/V5 not scored (D-E2B-M1)",
                    "unparseable": "an unparseable candidate is scored 1.0 by every metric and judge (flagged), never dropped; coverage reported",
                    "ties": "AUROC counts ties as 0.5 for every metric; tie rate reported per metric"},
        "comparators": {
            "flashlite_disg": "google/gemini-2.5-flash-lite, vendor_d judges.judge_json(RUBRIC_A, USER_JSON_A, max_tokens=150), disguised view (PRIMARY comparator)",
            "flashlite_orig": "same, original view", "nano_orig": "openai/gpt-4.1-nano judge_logprob(RUBRIC_A) -> 1 - P(YES), original view",
            "costmatched_disg": "deepseek/deepseek-v3.2, reasoning {enabled: false}, T=0, max_tokens 150, RUBRIC_A + USER_JSON_A byte-identical to flash-lite, judges.parse_judge_json; COST-MATCHED primary",
            "costmatched_orig": "same, original view; all rows if pilot $/call <= 1.6e-4, else frontier subsample + batch prefix",
            "costmatched_pilot": "30 rows (first 30 parseable rows of batch 1 in sha1 order), both views; parse failure > 10% -> one retry rule max_tokens 300; still > 10% -> NOT_TESTABLE_PARSE",
            "frontier": "google/gemini-3.1-pro-preview via exp-6 api_bar.frontier_judge (effort low, max_tokens 4000), original view, 300-row subsample",
            "frontier_subsample": "drawn after generation, before any label join: cells = words tercile (E2-B sentence cut points) x family (9); 300 rows proportional, min 3 per cell; within cell order sha1('E2B_frontier_v1|'+row_key); inclusion probabilities stored; pilot 10 rows; if > $6e-3/item cut to largest affordable prefix and recompute probabilities; ~2/3 expected usable in R_AB -> wide CI (descriptive)"},
        "populations": {"R_AB": "LLM systems only, tiers A+B, excluding CONTESTED and reading_choice (PRIMARY)", "R_A": "tier A only",
                        "CONTESTED_as_CORRECT": "sensitivity", "CONTESTED_as_ERROR": "sensitivity"},
        "confirmatory_hierarchy": {
            "E2B_alone": {"B1": "L25_E2B strat AUROC delta V0 - flashlite_disg, strata = word bin, sentence-cluster bootstrap B=2000 percentile 95% CI > 0 (MDE80 0.103, power 0.47 at +0.069; a null is EXPECTED and reported as underpowered alone)",
                          "B2": "nested [S4_E2B + V0] - S4_E2B cross-fitted by E2-B sentence folds, CI > 0",
                          "B3": "V0 - costmatched_disg with CI, NO directional prediction",
                          "B4": "frontier: IPW AUROC, ratio V0/frontier with CI, nested [frontier + V0] - frontier; descriptive"},
            "union_fixed_sequence_alpha_0.05": {
                "U1": "union LONG POOL (L25_E2A + L25_E2B + EXC_E2A) strat delta V0 - flashlite_disg CI > 0, with point > 0 vs flashlite_orig and nano (MDE ~0.057)",
                "U2": "union L25 delta, CI > 0 (MDE ~0.075, power ~0.73 at +0.069)",
                "U3": "union nested [S4 + V0] - S4, CI > 0",
                "U4": "carried H-IMPROVE variant - V0 on the union long pool, CI > 0",
                "rule": "each tested at alpha 0.05 only if the previous was confirmed; otherwise descriptive"},
            "union_strata": "{L25_E2A, L25_E2B, EXC_E2A} x word bin; bootstrap over sentence_id within stratum",
            "heterogeneity": "Delta_A - Delta_B with SE = sqrt(SE_A^2 + SE_B^2), Cochran's Q and I^2 over the two L25 samples; reported either way; if CI excludes 0 -> 'effect differs between samples', recheck within 25-29 bin",
            "meta_analysis": "fixed-effect inverse-variance pooling of per-sample strat deltas (L25_E2A, L25_E2B, EXC as 3rd component for the long pool); cross-check; disagreement > 0.02 with the pooled bootstrap reported; under significant heterogeneity per-sample results are primary",
            "duplicate_rule": "a sentence labelled by both E2-A and E2-B counts once in the union, taking E2-B's copy; kappa of final labels on duplicates reported (test-retest)",
            "regime_rule": "if E2-A and E2-B label regimes differ (PASS vs DRIFTED) the union is SECONDARY",
            "verdict_wording": {"U1_CI_gt_0": "confirmed on untouched long sentences", "U1_point_gt_0_CI_incl_0": "direction replicated, not significant at MDE ~0.057", "U1_point_le_0": "DISCONFIRM: E result was development-set optimism"},
            "residual_risk_text": "E2-A and E2-B share the label instrument (the panel): the union adds SAMPLING power, not label-regime independence; instrument-disjoint confirmation is R_COMP FREE's role"},
        "MDE80": {"E2B_L25": 0.103, "union_L25": 0.075, "union_long_pool": 0.057, "E2A_long_pool_alone": 0.076,
                  "source": "iter_4/gen_art/gen_art_evaluation_3/power_E2.json se_fit (L25|flashlite_disg a=-0.795 b=-0.503; long a=-0.890 b=-0.5145)"},
        "other_analyses": ["H-MECH (i)-(iv) on L25_E2B CORRECT rows (eval-3/eval-2/exp-9 definitions)", "H-IMPROVE carried variant - V0",
                           "rename FA at c > 0.5 + paired flip (Wilson CI) + base FA", "complexity curves at E2-B quartile bins",
                           "coverage with unparseables in the denominator", "$ and seconds per candidate FULL and MARGINAL",
                           "system-level Kendall tau-b (~10 systems, descriptive only)",
                           "judge own-family exclusion: flash-lite and frontier drop G8, nano drops G7, deepseek drops G4",
                           "tie rate per metric", "placebo: V0 with shuffled sentence peers (post-join, reported)"],
        "budget": {"hard_cap_usd": 9.5, "reserve_usd": 0.95, "plan_to_usd": 8.55,
                   "estimates": {"400 L25 x $0.01182": 4.73, "cheap judges x3": 0.55, "deepseek disguised": 0.9, "frontier 300": 1.1, "deepseek original": 0.9, "GG": 0.4, "drift fallback": 0.3},
                   "rule": "before each sweep estimate its cost from actuals; do not start if estimate > remaining - 0.95",
                   "shrink_order": ["GG scoring", "frontier (smaller affordable prefix, recomputed inclusion probabilities)", "deepseek original view (keep disguised)", "L25 sentences (floor 250, always a batch-order prefix)"],
                   "on_402_403": "finish CPU work, poll every 15 min until T+4:30, then report PARTIAL with the completed fraction per word bin"},
        "deadlines_utc": {"M2": "12:38 (T+1:30)", "M1_variants": "13:38 (T+2:30)", "M1_GG": "15:08 (T+4:00)", "last_paid_call": "15:38 (T+4:30)", "M3_E2A": "16:38 (T+5:30)"},
        "seals": {"labels": "e2bsrc/seal.json via seal_e2.py / verify_seal.py", "scores": "scores/score_seal.json: sha256 of scores_E2B.jsonl, every scoring source file, the frontier subsample and marker hashes; scoring code runs under an open() guard refusing sealed/ and any path containing 'label' or 'reference' (logged to scores/file_access_log.txt)",
                  "join": "only if verify_seal and verify_score_seal both pass"},
        "surplus_claim": "e2b/E2B_SURPLUS_CLAIM.json token 'aii_iter5_e2b_surplus_v1' with the 98 surplus ids",
        "input_hashes": {"census_E2B.json": sha(E2B / "census_E2B.json"), "prereg_E2.json": sha(WS / "e2bsrc" / "prereg_E2.json"),
                         "code_freeze_check_E2B.json": sha(WS / "e2bsrc" / "code_freeze_check_E2B.json")}}
    P.write_text(json.dumps(pre, indent=1))
    (WS / "prereg_iter5_E2B.sha256").write_text(f"{sha(P)}  prereg_iter5_E2B.json\n")
    sents = json.loads((E2B / "sentences_E2B.json").read_text())
    claim = {"token": "aii_iter5_e2b_surplus_v1", "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
             "ids": [s["sentence_id"] for s in sents if s["e2b_origin"] == "E2_surplus"],
             "rule": "a sentence labelled by both E2-A and E2-B counts once in the union, taking E2-B's copy"}
    (E2B / "E2B_SURPLUS_CLAIM.json").write_text(json.dumps(claim, indent=1))
    print("prereg", sha(P), "surplus ids", len(claim["ids"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
