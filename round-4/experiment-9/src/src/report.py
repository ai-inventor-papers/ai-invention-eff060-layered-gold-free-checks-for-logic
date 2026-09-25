"""STEP H: csc_gate_E.json, per_item_csc_E.jsonl, tables.md (one '# source:' line per table, every table tagged
DEVELOPMENT E), deviations.json and method_out.json (exp_gen_sol_out; predict_* oriented higher = more likely ERROR)."""
from __future__ import annotations

import json
import sys
import time
from collections import defaultdict
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
RES = ROOT / "results"
DATA = ROOT / "data"
sys.path.insert(0, str(SRC))
from analyse import PRETTY, jdump, jl  # noqa: E402

A = json.loads((RES / "analysis.json").read_text())
DEV = "DEVELOPMENT E"


def f3(x, nd=3):
    return "–" if x is None else f"{x:.{nd}f}"


def mci(m, nd=3):
    if not m or m.get("point") is None:
        return "–"
    c = m.get("ci") or [None, None]
    s = f"{m['point']:.{nd}f}"
    if c[0] is not None:
        s += f" [{c[0]:.{nd}f}, {c[1]:.{nd}f}]"
    return s + ("" if m.get("read", True) else " (NOT_READ)")


def dci(m, nd=3):
    if not m or m.get("delta") is None:
        return "–"
    c = m.get("ci") or [None, None]
    s = f"{m['delta']:+.{nd}f}"
    if c[0] is not None:
        s += f" [{c[0]:+.{nd}f}, {c[1]:+.{nd}f}]"
    return s + ("" if m.get("read", True) else " (NOT_READ)")


def eci(r, k):
    if not r or r.get(k) is None:
        return "–"
    c = r.get(k + "_ci") or [None, None]
    return f"{r[k]:.3f}" + (f" [{c[0]:.3f}, {c[1]:.3f}]" if c[0] is not None else "")


def tables() -> str:
    pops = A["populations"]
    out = [f"# T6-E Candidate-Signature Consensus on dataset E — tables ({DEV})\n",
           "All numbers are DEVELOPMENT E (dataset E was used by earlier rounds to choose consensus; no confirmation claim). "
           "Scores are oriented higher = more likely ERROR. CIs: sentence-cluster percentile bootstrap, B = 2000, seed 0, paired on identical rows. "
           "'strat' = within-source-stratum AUROC. Cells with < 50 ERROR or < 50 CORRECT rows are marked NOT_READ.\n",
           "**Budget event.** The paid peer sweep was refused by the platform after 1,033 of ~9,000 planned calls (HTTP 403 "
           "aii_run_budget_exhausted: the run's shared 'Test idea' phase budget of $7.00 was used up, mostly by sibling artifacts; this artifact "
           f"spent ${A['g_cost']['ledger_total_usd']:.3f}). CSC is therefore evaluated on PRIMARY = the {pops['PRIMARY']['n']} R_AB rows whose 3 CSC peer calls "
           "completed (fixed in prereg_csc_E_addendum1.json before scoring). FORMAT-ONLY, PLACEBO and RENAME arms are NOT_RUN. $0 analyses use all 2,686 rows.\n"]
    rows = [[k, v["n"], v["n_err"], v["n_cor"], v["n_sent"]] for k, v in pops.items() if isinstance(v, dict) and "n" in v]
    out.append(md_table(f"T0. Populations ({DEV})", "results/analysis.json populations; prereg_csc_E_addendum1.json",
                        ["population", "rows", "ERROR", "CORRECT", "sentences"], rows))
    ps = pops["PRIMARY_by_stratum"]
    out.append(md_table(f"T0b. PRIMARY rows by stratum ({DEV})", "results/analysis.json populations.PRIMARY_by_stratum",
                        ["stratum", "ERROR", "CORRECT", "readable (>=50/50)"], [[s, v["n_err"], v["n_cor"], v["n_err"] >= 50 and v["n_cor"] >= 50] for s, v in ps.items()]))
    st = A["status"]
    out.append(md_table(f"T0c. Coverage and prompt-following ({DEV})", "results/analysis.json status",
                        ["quantity", "value"],
                        [["CSC-OWN status on PRIMARY", st["own_status_PRIMARY"]], ["CSC insufficient-peer share (PRIMARY)", f3(st["own_insufficient_share_PRIMARY"])],
                         ["z3 UNKNOWN pairs (PRIMARY, CSC)", st["own_unknown_pairs_PRIMARY"]],
                         ["FREE-MATCHED status (FULL)", st["free_status_FULL"]], ["FREE-MATCHED insufficient share (FULL)", f3(st["free_insufficient_share_FULL"])],
                         ["peer-peer exact agreement, CSC peers (PRIMARY)", f3(st["peer_pair_agree_exact"]["CSC_OWN_PRIMARY"])],
                         ["peer-peer exact agreement, FREE-MATCHED peers (same rows)", f3(st["peer_pair_agree_exact"]["FREE_MATCHED_same_rows"])],
                         ["peer-peer exact agreement, FREE-MATCHED peers (FULL)", f3(st["peer_pair_agree_exact"]["FREE_MATCHED_FULL"])]]))
    # e/d
    ed = A["a_ed_PRIMARY"]["cells"]
    arms = ["CSC", "CSC_graded", "CSC_multi", "FREE_exact", "FREE_align", "END_MAJ9", "HYB_MEAN"]
    rws = []
    for cell in ["R_AB", "L25", "L20", "EXC", "CTRL", "words_T1", "words_T2", "words_T3", "ncond_0-1", "ncond_2", "ncond_3", "ncond_4+", "tierA", "VEX"]:
        if cell not in ed:
            continue
        c = ed[cell]
        for a in arms:
            r = c.get(a) or {}
            rws.append([cell, a, c["n_err"], c["n_cor"], eci(r, "e") + ("" if c["n_err"] >= 50 else " (NOT_READ)"), eci(r, "d") + ("" if c["n_cor"] >= 50 else " (NOT_READ)"),
                        f3(r.get("auroc_b"))])
    out.append(md_table(f"T1. Error endorsement e and correct-row divergence d at c > 0.5, PRIMARY ({DEV})", "results/analysis.json a_ed_PRIMARY.cells",
                        ["cell", "arm", "n ERR", "n COR", "e = P(endorsed|ERROR)", "d = P(flagged|CORRECT)", "AUROC_b = 1-(e+d)/2"], rws))
    pd_ = A["a_ed_PRIMARY"]["paired_CSC_minus"]
    out.append(md_table(f"T1b. Paired CSC − other arm on the same PRIMARY rows ({DEV})", "results/analysis.json a_ed_PRIMARY.paired_CSC_minus",
                        ["other arm", "Δe [CI]", "Δd [CI]"],
                        [[b, f"{v['delta_e']:+.3f} [{v['delta_e_ci'][0]:+.3f}, {v['delta_e_ci'][1]:+.3f}]", f"{v['delta_d']:+.3f} [{v['delta_d_ci'][0]:+.3f}, {v['delta_d_ci'][1]:+.3f}]"] for b, v in pd_.items()]))
    edf = A["a_ed_FULL"]["cells"]
    rws = []
    for cell in ["R_AB", "L25", "L20", "EXC", "CTRL", "words_T1", "words_T2", "words_T3", "ncond_0-1", "ncond_4+"]:
        c = edf[cell]
        for a in ("FREE_exact", "FREE_align", "FREE_graded", "END_MAJ9"):
            r = c.get(a) or {}
            rws.append([cell, a, c["n_err"], c["n_cor"], eci(r, "e"), eci(r, "d")])
    out.append(md_table(f"T2. $0 FULL population (2,686 rows): e / d of the matched free peers, exact names vs ALIGN ({DEV})", "results/analysis.json a_ed_FULL.cells",
                        ["cell", "arm", "n ERR", "n COR", "e", "d"], rws))
    pe = A["a_ed_FULL"]["paired_exact_minus_align"]
    out.append(f"\nPaired FREE exact − FREE ALIGN on FULL: Δe {pe['delta_e']:+.3f} [{pe['delta_e_ci'][0]:+.3f}, {pe['delta_e_ci'][1]:+.3f}], "
               f"Δd {pe['delta_d']:+.3f} [{pe['delta_d_ci'][0]:+.3f}, {pe['delta_d_ci'][1]:+.3f}] (# source: results/analysis.json a_ed_FULL.paired_exact_minus_align)\n")
    # GEE
    rws = []
    for pop in ("a_ed_PRIMARY", "a_ed_FULL"):
        for a, g in A[pop]["gee"].items():
            for k in ("d_words_ncond", "e_words_ncond", "d_words_ncond_stratum"):
                co = (g[k].get("coef") or {})
                for v in ("zw", "zn"):
                    if v in co:
                        rws.append([pop.replace("a_ed_", ""), a, k, v, f"{co[v]['b']:+.3f} [{co[v]['ci'][0]:+.3f}, {co[v]['ci'][1]:+.3f}]", g[k].get("n")])
    out.append(md_table(f"T3. GEE slopes (binomial logit, exchangeable, sentence clusters) of d and e on z(words), z(n_conditions) ({DEV})",
                        "results/analysis.json a_ed_*.gee", ["population", "arm", "model", "term", "coef [95% CI]", "n"], rws))
    rws = []
    for pop, dct in A["net"].items():
        for a, r in dct.items():
            if "error" in r:
                continue
            w = r["words_T3_minus_T1"]
            rws.append([pop, a, f"{w['delta_e_plus_d']:+.3f} [{w['ci'][0]:+.3f}, {w['ci'][1]:+.3f}]", f"{w['delta_e']:+.3f}", f"{w['delta_d']:+.3f}", w["verdict"]])
    out.append(md_table(f"T3b. NET Δ(e+d), words tercile T3 − T1 ({DEV})", "results/analysis.json net", ["population", "arm", "NET [CI]", "Δe", "Δd", "verdict"], rws))
    # AUROC
    bP = A["b_PRIMARY"]
    cols = ["c_csc", "c_csc_graded", "c_csc_multi", "HYB_MEAN", "HYB_MAX", "c_free_exact", "c_free_align", "c_free_graded", "T1__c_score_align",
            "T1__p_peer_text", "T1__judge_cheap_disg", "T1__judge_cheap_orig", "T1__judge_cheap2_orig", "T1__rt_nli_min", "T1__sc5_eq_frac", "T1__S4_full_oof"]
    cells = ["R_AB [strat]", "R_AB [pooled]", "long L25+L20+EXC [strat]", "L25 [pooled]", "L20 [pooled]", "EXC [pooled]", "CTRL [pooled]", "tier A only [strat]", "VEX subset [strat]"]
    rws = []
    for c in cols:
        rws.append([PRETTY.get(c, c)] + [mci(bP["metrics"][cl].get(c)) for cl in cells[:4]] + [f3((bP["metrics"]["R_AB [pooled]"].get(c) or {}).get("auprc"))])
    out.append(md_table(f"T4. AUROC on PRIMARY rows (n_err/n_cor R_AB = {bP['metrics']['R_AB [strat]']['n_err']}/{bP['metrics']['R_AB [strat]']['n_cor']}) ({DEV})",
                        "results/analysis.json b_PRIMARY.metrics", ["metric", *cells[:4], "AUPRC (R_AB)"], rws))
    rws = []
    for c in cols:
        rws.append([PRETTY.get(c, c)] + [mci(bP["metrics"][cl].get(c)) for cl in cells[4:]])
    out.append(md_table(f"T4b. AUROC on PRIMARY rows, other cells ({DEV})", "results/analysis.json b_PRIMARY.metrics", ["metric", *cells[4:]], rws))
    rws = []
    for v in ("c_csc", "c_csc_graded", "c_csc_multi", "HYB_MEAN"):
        for b in ["c_free_exact", "c_free_align", "T1__c_score_align", "T1__p_peer_text", "T1__judge_cheap_disg", "T1__judge_cheap_orig",
                  "T1__judge_cheap2_orig", "T1__rt_nli_min", "T1__sc5_eq_frac", "T1__S4_full_oof"]:
            k = f"{v} - {b}"
            rws.append([PRETTY.get(v, v), PRETTY.get(b, b)] + [dci(bP["deltas"][cl].get(k)) for cl in ("R_AB [strat]", "long L25+L20+EXC [strat]", "L25 [pooled]", "tier A only [strat]")])
    out.append(md_table(f"T5. Paired ΔAUROC, CSC variant − comparator, PRIMARY rows ({DEV})", "results/analysis.json b_PRIMARY.deltas",
                        ["CSC variant", "comparator", "R_AB strat", "long strat", "L25 pooled", "tier A strat"], rws))
    rws = []
    for pop in ("b_GE2", "b_MINI200", "b_PRIMARY_excl_insufficient"):
        b = A[pop]
        m = b["metrics"]["R_AB [strat]"]
        for comp in ("c_free_exact", "c_free_align", "T1__c_score_align", "T1__judge_cheap_disg"):
            d = b["deltas"]["R_AB [strat]"].get(f"c_csc - {comp}")
            if d:
                rws.append([pop.replace("b_", ""), m["n_err"], m["n_cor"], mci(m.get("c_csc")), PRETTY.get(comp, comp), dci(d)])
    out.append(md_table(f"T5b. Sensitivity populations: c_csc strat AUROC and paired Δ ({DEV})", "results/analysis.json b_GE2, b_MINI200, b_PRIMARY_excl_insufficient",
                        ["population", "n ERR", "n COR", "c_csc strat AUROC", "comparator", "Δ strat"], rws))
    bf = A["b_FULL_free"]
    rws = [[PRETTY.get(c, c)] + [mci(bf["metrics"][cl].get(c)) for cl in ("R_AB [strat]", "R_AB [pooled]", "long L25+L20+EXC [strat]", "L25 [pooled]")]
           for c in ("c_free_exact", "c_free_align", "c_free_graded", "T1__c_score_align", "T1__judge_cheap_disg", "T1__p_peer_text")]
    out.append(md_table(f"T6. $0 FULL population: matched 3-family free peers scored exactly vs with ALIGN ({DEV})", "results/analysis.json b_FULL_free.metrics",
                        ["metric", "R_AB strat", "R_AB pooled", "long strat", "L25 pooled"], rws))
    fr = A["b_frontier_frame"]
    out.append(f"\nFrontier-judge frame ∩ PRIMARY (n_err {fr['n_err']}, n_cor {fr['n_cor']}): c_csc {mci(fr['c_csc'])}; frontier judge {mci(fr['judge_strong_orig'])}; Δ {dci(fr['delta'])} "
               "(# source: results/analysis.json b_frontier_frame)\n")
    # nesting
    nst = A["c_nesting_PRIMARY"]
    if "nested" in nst:
        rws = [[k, dci(v["strat"]), dci(v["pooled"])] for k, v in nst["nested"].items()]
        out.append(md_table(f"T7. Nesting: OOF logistic stacks refit on folds_E within PRIMARY rows ({DEV})", "results/analysis.json c_nesting_PRIMARY.nested",
                            ["comparison", "Δ strat AUROC [CI]", "Δ pooled AUROC [CI]"], rws))
        out.append(f"\nS4_full refit on PRIMARY vs T1's S4_full_oof: corr {nst['reproduction_vs_T1_S4_full_oof']['corr']:.3f}; refit strat AUROC {mci(nst['fits']['S4_full']['strat'])}, "
                   f"T1 column on same rows {mci(nst['reproduction_vs_T1_S4_full_oof']['T1_S4_full_oof_strat_same_rows'])} (# source: results/analysis.json c_nesting_PRIMARY)\n")
    # where d went
    rws = []
    for k in ("d_where_FULL_free_align_flagged_CORRECT", "d_where_FULL_free_exact_flagged_CORRECT", "d_where_PRIMARY_free_flagged_csc_endorsed"):
        r = A[k]
        for c, v in r["pair_classes"].items():
            rws.append([k, r["n_rows"], c, v, f3(r["pair_shares"].get(c))])
        rws.append([k, r["n_rows"], "ROWS whose every free-peer disagreement is vocabulary-resolvable", r["rows_all_disagreements_vocabulary_resolvable"], f3(r["share_rows_vocab_resolvable"])])
    out.append(md_table(f"T8. Where d comes from: free-peer disagreements with CORRECT candidates, by pairs_E verdicts ({DEV})",
                        "results/analysis.json d_where_*", ["set", "rows", "disagreement class", "count", "share"], rws))
    tg = A["d_tagging"]
    out.append(md_table(f"T8b. CORRECT rows still flagged by CSC: automated tags (all such rows; the planned 60-row sample exceeds their number) ({DEV})", "results/analysis.json d_tagging; results/d_tagging_rows.json",
                        ["tag", "count"], [[k, v] for k, v in tg["tag_counts"].items()]))
    out.append("\nTagging rule (written before tagging):\n```\n" + tg["rule"] + "\n```\n")
    sib = A.get("d_vs_sibling_prediction", {})
    sp = sib.get("sibling_part1_predictions", {})
    ms = sib.get("measured", {})
    out.append(md_table(f"T8c. Measured CSC d / e vs the sibling evaluation's pre-registered prediction (read only after results/d_measured.json was written) ({DEV})",
                        "results/analysis.json d_vs_sibling_prediction; iter_4/gen_art_evaluation_3/results/part1.json (read-only)", ["quantity", "value"],
                        [["sibling d_floor_pred, 3-family pool (FULL population)", f"{f3((sp.get('3pool') or {}).get('d_floor_pred'))} {(sp.get('3pool') or {}).get('d_floor_pred_ci')}"],
                         ["sibling e_ceiling_pred, 3-family pool", f3((sp.get('3pool') or {}).get('e_ceiling_pred'))],
                         ["measured d, CSC (PRIMARY)", f3(ms.get("d_CSC_PRIMARY"))], ["measured e, CSC (PRIMARY)", f3(ms.get("e_CSC_PRIMARY"))],
                         ["measured d_CSC / d_FREE_exact on PRIMARY", f3(ms.get("ratio_d_CSC_over_d_FREE_exact_PRIMARY"))],
                         ["predicted d_floor / d_FREE_exact on FULL", f3(ms.get("sibling_ratio_d_floor_3pool_over_d_FREE_exact_FULL"))],
                         ["note", sib.get("note", "")]]))
    # anchoring
    rws = []
    for cl, r in A["e_anchoring_by_error_class"]["PRIMARY"].items():
        rws.append([cl, r["n"], eci(r.get("CSC"), "e"), eci(r.get("FREE_exact"), "e"), eci(r.get("FREE_align"), "e"), eci(r.get("END_MAJ9"), "e"),
                    (f"{r['paired_CSC_minus_FREE_align']['delta_e']:+.3f} [{r['paired_CSC_minus_FREE_align']['delta_e_ci'][0]:+.3f}, {r['paired_CSC_minus_FREE_align']['delta_e_ci'][1]:+.3f}]"
                     if r.get("paired_CSC_minus_FREE_align") else "–") + ("" if r["n"] >= 50 else " (NOT_READ)")])
    out.append(md_table(f"T9. Anchoring on real errors: e by error class, PRIMARY ({DEV})", "results/analysis.json e_anchoring_by_error_class.PRIMARY",
                        ["error class", "n", "e CSC", "e FREE exact", "e FREE ALIGN", "e END_MAJ-9", "Δe CSC − FREE ALIGN"], rws))
    rws = [[cl, r["n"], eci(r.get("FREE_exact"), "e"), eci(r.get("FREE_align"), "e"), eci(r.get("END_MAJ9"), "e")] for cl, r in A["e_anchoring_by_error_class"]["FULL"].items()]
    out.append(md_table(f"T9b. e by error class, FULL, free peers ($0) ({DEV})", "results/analysis.json e_anchoring_by_error_class.FULL",
                        ["error class", "n", "e FREE exact", "e FREE ALIGN", "e END_MAJ-9"], rws))
    ty = A["f_typing_PRIMARY"]
    if "n" in ty:
        rws = [[w, f3(ty[w]["acc_exact_opset"]) + f" [{f3(ty[w]['acc_exact_ci'][0])}, {f3(ty[w]['acc_exact_ci'][1])}]", f3(ty[w]["acc_coarse_class"]), f3(ty[w]["coverage_typed"])]
               for w in ("own_majority", "free_majority")]
        rws += [["majority class (" + str(ty["majority_class"]) + ")", f3(ty["majority_acc"]), "–", "–"], ["chance (1/#classes)", f3(ty["chance"]), "–", "–"],
                ["iteration-2 medoid typing (reference)", "0.371", "–", "–"]]
        out.append(md_table(f"T10. Error typing on R_A errors with 1–2 repair ops, PRIMARY (n = {ty['n']}) ({DEV})", "results/analysis.json f_typing_PRIMARY",
                            ["predictor", "exact op-set accuracy [CI]", "coarse-class accuracy", "share typed"], rws))
    g = A["g_cost"]
    out.append(md_table(f"T11. Cost per candidate ({DEV})", "results/analysis.json g_cost", ["quantity", "value"],
                        [["FULL $/candidate, undeduped (sum of its 3 peer calls)", f"{g['FULL_usd_per_candidate_undeduped_mean']:.2e}"],
                         ["FULL $/candidate, dedup-apportioned", f"{g['FULL_usd_per_candidate_dedup_apportioned_mean']:.2e}"],
                         ["MARGINAL z3 CPU s/candidate (mean / p95)", f"{g['MARGINAL_z3_cpu_s_per_candidate_mean']:.3f} / {g['MARGINAL_z3_cpu_s_p95']:.3f}"],
                         ["flash-lite judge $/item (T1)", "4.88e-05"], ["free 9-peer pool $/item FULL (T1)", "1.21e-04"],
                         ["$/call by model", ", ".join(f"{m}: {v:.2e}" for m, v in g["usd_per_call_by_model"].items())],
                         ["G5 (FULL <= $0.002)", g["G5_pass"]], ["this artifact's total API spend", f"${g['ledger_total_usd']:.4f}"]]))
    rws = []
    for var, bins in A["h_complexity_PRIMARY"].items():
        for b, r in bins.items():
            rws.append([var, b, r["n_err"], r["n_cor"]] + [mci(r.get(c)) for c in ("c_csc", "c_free_exact", "c_free_align", "T1__c_score_align", "T1__judge_cheap_disg")])
    out.append(md_table(f"T12. Complexity curves, strat AUROC per bin, PRIMARY ({DEV})", "results/analysis.json h_complexity_PRIMARY",
                        ["variable", "bin", "n ERR", "n COR", "CSC", "FREE exact", "FREE ALIGN", "c_score_align", "flash-lite disg"], rws))
    rws = []
    for k, r in A["h_M3"].items():
        s1 = r["spec1_bootstrap_delta_slope"]
        s2 = r["spec2_stacked_gee_interaction"] or {}
        rws.append([k, r["n"], f3(r["flag_rate"]), f3(r["acc_consensus"]), f3(r["acc_judge"]),
                    f"{s1['delta']:+.3f} [{s1['ci'][0]:+.3f}, {s1['ci'][1]:+.3f}]" if s1["delta"] is not None else "–",
                    f"{s2.get('b', float('nan')):+.3f} [{s2.get('ci', [float('nan')] * 2)[0]:+.3f}, {s2.get('ci', [float('nan')] * 2)[1]:+.3f}]" if s2 else "–"])
    out.append(md_table(f"T13. M3: length slope of decision correctness, consensus − judge (judge binarised at the consensus flag rate) ({DEV})", "results/analysis.json h_M3",
                        ["comparison", "n", "flag rate", "acc consensus", "acc judge", "spec 1 bootstrap Δslope [CI]", "spec 2 stacked-GEE interaction [CI]"], rws))
    rws = []
    for pop in ("i_system_level_PRIMARY", "i_system_level_FULL"):
        for c, r in A[pop].items():
            if isinstance(r, dict) and "tau_b" in r:
                rws.append([pop.replace("i_system_level_", ""), PRETTY.get(c, c), f3(r["tau_b"]), f3(r["p"]), r["n"]])
    out.append(md_table(f"T14. System-level Kendall τ-b (mean score vs error rate over system×variant rows) ({DEV})", "results/analysis.json i_system_level_*",
                        ["population", "metric", "τ-b", "p", "n systems"], rws))
    j = A["j_placebo"]
    k = A["k_rename"]["c_score_align_rederived_on_SYN_rows"]
    out.append(md_table(f"T15. Placebos and rename ({DEV})", "results/analysis.json j_placebo, k_rename", ["check", "value"],
                        [["shuffled labels: pooled AUROC of c_csc (PRIMARY)", f3(j["shuffled_labels_auroc_c_csc"])],
                         ["shuffled labels: strat AUROC of c_csc", f3(j["shuffled_labels_strat_auroc_c_csc"])],
                         ["random-sentence-signature PLACEBO arm", j["random_sentence_signature_arm"]],
                         ["CSC RENAME_SYN / RENAME_NONCE (G3-E)", "NOT_RUN"],
                         [f"$0: 9-peer c_score_align re-derived on SYN-renamed CORRECT rows (n = {k['n']}): FA base", f3(k["FA_base (c >= 0.5 = not END_MAJ endorsed)"])],
                         ["  FA after RENAME_SYN", f3(k["FA_syn"])],
                         ["  ΔFA [CI]", f"{k['delta_FA']:+.3f} [{k['delta_FA_ci'][0]:+.3f}, {k['delta_FA_ci'][1]:+.3f}]" if k["delta_FA"] is not None else "–"],
                         ["  re-derived base vs frozen c_score_align (corr)", f3(k["rederived_base_vs_frozen_c_score_align_corr"], 6)]]))
    for arm in ("K4", "OTHER"):
        x = A[f"exploratory_{arm}"]
        out.append(f"\nEXPLORATORY {arm} (incidental coverage, n_err {x['n_err']}, n_cor {x['n_cor']}, never gated): "
                   f"{arm} strat AUROC {mci(list(v for kk, v in x.items() if kk.startswith('c_') and kk != 'c_csc_same_rows')[0])}; CSC same rows {mci(x['c_csc_same_rows'])}; "
                   f"d {arm} {eci(x['ed_' + arm], 'd')} vs CSC {eci(x['ed_CSC_same_rows'], 'd')} (# source: results/analysis.json exploratory_{arm})\n")
    ph = RES / "posthoc_phi_contamination.json"
    if ph.exists():
        H = json.loads(ph.read_text())
        rws = [[c, mci(m), eci(H["ed"].get(c), "e") if c in H["ed"] else "–", eci(H["ed"].get(c), "d") if c in H["ed"] else "–"] for c, m in H["strat_auroc"].items()]
        rws += [[k, dci(v), "", ""] for k, v in H["delta_strat"].items()]
        out.append(md_table(f"T17. POST-HOC sensitivity: phi-4 exemplar leakage removed symmetrically from CSC and FREE-MATCHED peers, PRIMARY ({DEV})",
                            "results/posthoc_phi_contamination.json (src/posthoc_contam.py)", ["score / paired Δ", "strat AUROC or Δ [CI]", "e", "d"], rws))
        out.append(f"\nphi-4 copied the last few-shot exemplar (CanMake/Baker) in {sum(H['contaminated_calls_by_model_route'].values())} CSC calls "
                   f"(routes {H['contaminated_calls_by_model_route']}); peers dropped on PRIMARY: {H['peers_dropped_on_PRIMARY']}.\n")
    gt = A["gates"]
    rws = []
    for v, r in gt["variants"].items():
        if isinstance(r.get("G1"), dict):
            rws.append([v, f"d {f3(r['G1']['d'])} [{f3(r['G1']['d_ci'][0])}, {f3(r['G1']['d_ci'][1])}], slope {f3((r['G1']['words_slope'] or {}).get('b'))} → {'PASS' if r['G1']['pass'] else 'FAIL'}",
                        f"R_AB part {'PASS' if r['G2']['R_AB_part_pass'] else 'FAIL'}; L25 {r['G2']['L25_part']}", r["G3_E"], f"{r['G5']['FULL_usd_per_candidate']:.2e} → {'PASS' if r['G5']['pass'] else 'FAIL'}",
                        mci(r["strat_auroc_R_AB"])])
        else:
            rws.append([v, r["G1"], r["G2"], r["G3_E"], r["G5"], "–"])
    out.append(md_table(f"T16. Gate file summary (PROVISIONAL, PRIMARY subset) ({DEV})", "csc_gate_E.json", ["variant", "G1", "G2", "G3-E", "G5", "strat AUROC R_AB"], rws))
    return "\n".join(out)


def md_table(title, source, header, rows):
    s = f"\n## {title}\n# source: {source}\n\n| " + " | ".join(str(h) for h in header) + " |\n|" + "---|" * len(header) + "\n"
    for r in rows:
        s += "| " + " | ".join(str(x).replace("|", "/") for x in r) + " |\n"
    return s


def gate_file():
    g = A["gates"]
    out = {"artifact": "T6-E CSC on development set E (iteration 4)", "status": "PROVISIONAL",
           "why_provisional": "platform refused paid calls after 1,033 of ~9,000 planned; CSC scored on the 354-row PRIMARY subset; FORMAT-ONLY/RENAME/PLACEBO NOT_RUN",
           "population": A["populations"]["PRIMARY"], "prereg_sha256": A["guard"]["prereg_sha256"], "addendum1_sha256": A["guard"]["addendum1_sha256"],
           "scores_labelblind_sha256": A["guard"]["scores_sha256"], "G4": None, "variants": g["variants"], "iteration5_rule_note": g["iteration5_rule_note"],
           "NOT_RUN": ["FORMAT-ONLY", "PLACEBO (random-sentence signature)", "RENAME_SYN", "RENAME_NONCE", "G3-E"],
           "NOT_READ": ["L25 cell (PRIMARY has < 50 CORRECT L25 rows)", "k=4 variant (incidental coverage)"]}
    jdump(out, ROOT / "csc_gate_E.json")


def per_item():
    S = defaultdict(dict)
    for r in jl(RES / "scores_labelblind.jsonl"):
        S[r["row_key"]][r["arm"]] = r
    sal = json.loads((RES / "salvage_rows.json").read_text())
    pri, ge2 = set(sal["PRIMARY"]), set(sal["GE2"])
    F = jl(DATA / "frame_blind.jsonl")
    L = {r["row_key"]: r for r in jl(DATA / "labels_RAB.jsonl")}
    rows = []
    for f in F:
        s = S[f["row_key"]]
        o, fr = s.get("OWN", {}), s.get("FREE", {})
        rows.append({"row_key": f["row_key"], "sentence_id": f["sentence_id"], "stratum": f["stratum"], "system": f["system"], "family": f["family"],
                     "text": f["text"], "candidate_fol": f["candidate_fol"], "y_R_AB": L[f["row_key"]]["y"], "label_tier": L[f["row_key"]]["label_tier"],
                     "in_PRIMARY": f["row_key"] in pri, "in_GE2": f["row_key"] in ge2,
                     "c_csc": o.get("c_csc"), "c_csc_graded": o.get("c_csc_graded"), "c_csc_multi": o.get("c_csc_multi"), "csc_status": o.get("status", "NOT_RUN"),
                     "csc_n_usable": o.get("n_usable"), "csc_n_missing_calls": o.get("n_missing_calls"), "csc_n_unknown": o.get("n_unknown"),
                     "csc_peer_majority_fol": o.get("peer_majority_fol"), "csc_z3_cpu_s": o.get("z3_cpu_s"), "csc_unit_codes": o.get("unit_codes"),
                     "csc_peers": o.get("peers"), "csc_usd_undeduped": sum((p.get("usd") or 0) for p in o.get("peers", [])) if o else None,
                     "c_free_exact": fr.get("c_csc"), "c_free_graded": fr.get("c_csc_graded"), "c_free_align": fr.get("c_free_align"),
                     "free_status": fr.get("status"), "free_peers": fr.get("peers"),
                     "c_k4": s.get("K4", {}).get("c_csc"), "c_other_exact": s.get("OTHER", {}).get("c_csc"), "c_other_align": s.get("OTHER", {}).get("c_align"),
                     "c_align9_base": s.get("ALIGN9_BASE", {}).get("c_align9"), "c_align9_syn": s.get("ALIGN9_SYN", {}).get("c_align9"),
                     "c_score_align": f["T1__c_score_align"], "HYB_MEAN": (o["c_csc"] + f["T1__c_score_align"]) / 2 if o.get("c_csc") is not None else None})
    with open(RES / "per_item_csc_E.jsonl", "w") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    return rows


def method_out(rows):
    def s(x):
        return "NA" if x is None else (f"{x:.6f}" if isinstance(x, float) else str(x))
    F = {r["row_key"]: r for r in jl(DATA / "frame_blind.jsonl")}
    ex = []
    for r in rows:
        f = F[r["row_key"]]
        ex.append({"input": json.dumps({"text": r["text"], "candidate_fol": r["candidate_fol"], "system": r["system"], "prompt_variant": f["prompt_variant"]}, ensure_ascii=False),
                   "output": "ERROR" if r["y_R_AB"] == 1 else "CORRECT",
                   "predict_c_csc": s(r["c_csc"]), "predict_c_csc_graded": s(r["c_csc_graded"]), "predict_c_csc_multi": s(r["c_csc_multi"]),
                   "predict_HYB_MEAN": s(r["HYB_MEAN"]), "predict_baseline_free_matched_exact": s(r["c_free_exact"]),
                   "predict_baseline_free_matched_align": s(r["c_free_align"]), "predict_baseline_c_score_align_9peer": s(r["c_score_align"]),
                   "predict_baseline_judge_flashlite_disguised": s(f["T1__judge_cheap_disg"]), "predict_baseline_judge_flashlite_original": s(f["T1__judge_cheap_orig"]),
                   "predict_baseline_judge_nano_original": s(f["T1__judge_cheap2_orig"]), "predict_baseline_roundtrip_nli_min": s(f["T1__rt_nli_min"]),
                   "predict_baseline_selfconsistency_sc5": s(f["T1__sc5_eq_frac"]), "predict_baseline_p_peer_text": s(f["T1__p_peer_text"]),
                   "predict_baseline_S4_full_oof": s(f["T1__S4_full_oof"]),
                   "metadata_row_key": r["row_key"], "metadata_sentence_id": r["sentence_id"], "metadata_stratum": r["stratum"], "metadata_family": r["family"],
                   "metadata_label_tier": r["label_tier"], "metadata_in_PRIMARY": r["in_PRIMARY"], "metadata_csc_status": r["csc_status"],
                   "metadata_csc_n_usable": r["csc_n_usable"], "metadata_csc_n_missing_calls": r["csc_n_missing_calls"], "metadata_free_status": r["free_status"],
                   "metadata_words": f["words"], "metadata_n_conditions": f["n_conditions"], "metadata_csc_peer_majority_fol": r["csc_peer_majority_fol"],
                   "metadata_csc_peer_fols": [p.get("fol") for p in (r["csc_peers"] or [])], "metadata_csc_usd": r["csc_usd_undeduped"]})
    out = {"metadata": {"method_name": "Candidate-Signature Consensus (CSC), T6-E, iteration 4", "status": "DEVELOPMENT E; PROVISIONAL (paid sweep stopped by the platform budget)",
                        "orientation": "every predict_* is higher = more likely ERROR; 'NA' = not computed for that row (CSC exists only for rows whose peer calls completed)",
                        "what_c_csc_measures": "1 - share of family-disjoint peers (given the candidate's own symbol list) whose formula is z3-equivalent to the candidate with symbols matched by lowercased name and arity; not truth against a reference",
                        "populations": A["populations"], "gate_file": "csc_gate_E.json", "tables": "tables.md", "analysis": "results/analysis.json"},
           "datasets": [{"dataset": "dataset_E_R_AB_E_POOL", "examples": sorted(ex, key=lambda e: (not e["metadata_in_PRIMARY"], e["metadata_row_key"]))}]}
    (ROOT / "method_out.json").write_text(json.dumps(out, ensure_ascii=False))


def deviations():
    d = {"deviations": [
        {"id": "D1", "what": "Paid sweep stopped by the platform (HTTP 403 aii_run_budget_exhausted, shared 'Test idea' phase budget $7.00) after 1,033 calls; free tier also exhausted (429, 1000/day shared).",
         "effect": "CSC scored on 354 PRIMARY rows (475 with >= 2 peers) instead of 2,686; OWN floor 1,500 not met; FORMAT-ONLY, PLACEBO, RENAME NOT_RUN; OTHER-SIG / K4 exploratory only; L25 NOT_READ",
         "handling": "populations fixed in prereg_csc_E_addendum1.json before any CSC score existed; every comparison paired on identical rows; gates marked PROVISIONAL"},
        {"id": "D2", "what": "phi-4 pilot parse rate 0.85 < 0.9 go criterion (>= 0.8 drop rule); failures are function terms, not JSON format", "effect": "kept; unparseable peers leave the denominator"},
        {"id": "D3", "what": "FORMAT-ONLY expanded to all rows and RENAME to all CORRECT rows in the prereg (cheap after dedup)", "effect": "moot: both NOT_RUN (D1)"},
        {"id": "D4", "what": "large inputs read in place (sha256 in inputs_manifest.json), small ones copied into ./inputs"},
        {"id": "D5", "what": "60-row tagging of still-flagged CORRECT rows done by a mechanical rule (READING_CHOICE / PEER_SCATTER / GRANULARITY / SINGLE_OP_DIFF / MULTI_OP_DIFF) instead of hand tagging; rule written before tagging"},
        {"id": "D6", "what": "Nesting (fit_s4_oof on folds_E) refit on the PRIMARY rows only (small n, ~28 features); T1's S4_full reproduction on those rows reported alongside"},
        {"id": "D7", "what": "$0 addition: 9-peer c_score_align re-derived (eqmv against every other-family E row) on RENAME_SYN-renamed CORRECT rows, giving the incumbent's rename FA (HYB_MEAN's second half) although CSC's rename arm could not run"},
        {"id": "D9", "what": "POST-HOC (not pre-registered): phi-4 exemplar leakage (58/177 CSC calls, 24/292 of its E outputs) found by inspection; symmetric drop-rule sensitivity in results/posthoc_phi_contamination.json; the pre-registered scores are unchanged"},
        {"id": "D8", "what": "Label counts (not scores) of the >= 2-peer subset were printed once before addendum 1, to size the cells (disclosed in the addendum)"}],
        "reproduction_checks": json.loads((RES / "repro_checks.json").read_text())}
    jdump(d, ROOT / "deviations.json")


def ledger_summary():
    led = jl(RES / "api_cost_ledger.jsonl")
    by = defaultdict(lambda: {"calls": 0, "usd": 0.0, "in_tok": 0, "out_tok": 0, "zero_cost_rows": 0})
    for r in led:
        b = by[r["model"]]
        b["calls"] += 1
        b["usd"] += r.get("usd") or 0.0
        b["in_tok"] += r.get("in_tok") or 0
        b["out_tok"] += r.get("out_tok") or 0
        b["zero_cost_rows"] += int(not r.get("usd"))
    cache_n = sum(1 for l in (RES / "llm_cache.jsonl").read_text().splitlines() if l.strip())
    jdump({"total_usd": sum(v["usd"] for v in by.values()), "by_model": dict(by), "ledger_rows": len(led), "successful_cached_calls": cache_n,
           "note": "zero-cost rows = calls refused by the platform (HTTP 403 aii_run_budget_exhausted) or transient failures; they are logged, never cached",
           "hard_stop_usd": 9.5, "source": "results/api_cost_ledger.jsonl (one row per call, usd from OpenRouter usage.cost)"}, ROOT / "api_cost_ledger.json")


if __name__ == "__main__":
    ledger_summary()
    gate_file()
    rows = per_item()
    method_out(rows)
    deviations()
    (ROOT / "tables.md").write_text(tables())
    print("report written", time.ctime())
