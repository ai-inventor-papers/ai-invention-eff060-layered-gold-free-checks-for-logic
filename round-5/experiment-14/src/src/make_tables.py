#!/usr/bin/env python3
"""tables.md: every table carries a '# source:' line naming the file and the function that produced its numbers."""
from __future__ import annotations

import json

from common import FREEZE, RES, ROOT, utc

V = ["V0_frozen", "V0_rep", "c_exact", "V1", "V2", "V3", "V4", "V5"]
NAMES = {"V0_frozen": "V0 c_score_align (frozen)", "V0_rep": "V0 (matrix re-derivation)", "c_exact": "c_exact (aligner-free)",
         "V1": "V1 plurality-normalised", "V2": "V2 reliability-weighted", "V3": "V3 = V1+V2", "V4": "V4 two-channel logistic",
         "V5": "V5 = V3 on 3-pool", "c_gg": "GG (PRIMARY)", "c_gg_allyes": "GG bracket: all maps accepted", "c_ggb": "GG_B (SECONDARY, bridges)", "c_ggb_allyes": "GG_B bracket: every bridged map accepted"}


def f(x, n=3):
    return "NA" if x is None else (f"{x:.{n}f}" if isinstance(x, (int, float)) else str(x))


def ci(c, n=3):
    return "[NA]" if not c or c[0] is None else f"[{c[0]:.{n}f}, {c[1]:.{n}f}]"


def main():
    A = json.loads((RES / "screen_E.json").read_text())
    S = json.loads((RES / "selection_E.json").read_text())
    G0 = json.loads((RES / "gate_G0.json").read_text())
    G1 = json.loads((RES / "gate_G1_labelfree.json").read_text())
    D = json.loads((RES / "gg_dev.json").read_text())
    gv1 = json.loads((RES / "gg_gates_dev_v1.json").read_text())
    gv2 = json.loads((RES / "gg_gates_confirm_v2.json").read_text())
    AU = json.loads((RES / "audit_rederive.json").read_text())
    M1 = json.loads((FREEZE / "CONSENSUS_FREEZE_READY.json").read_text())
    GB = json.loads((RES / "ggb_dev.json").read_text()) if (RES / "ggb_dev.json").exists() else None
    L = [f"# Tables: iteration-5 FREEZE experiment (dataset E = DEVELOPMENT data)\n\nGenerated {utc()} by `src/make_tables.py`. "
         f"Population Z = {A['population']['Z']['n']} R_AB rows ({A['population']['Z']['n_error']} ERROR / {A['population']['Z']['n_correct']} CORRECT, "
         f"{A['population']['Z']['n_sentences']} sentences) with >= 2 cross-family peers. CIs: sentence-cluster percentile bootstrap, B = 2000, seed 20260924. "
         "Orientation: higher = more likely ERROR.\n"]
    # 1 gates
    L.append("## T1. Reproduction gates\n\n# source: results/gate_G0.json :: src/step0_gates.py main(); results/gate_G1_labelfree.json :: src/score_variants.py main(); results/screen_E.json['repro'], ['oracle'] :: src/screen.py main(), oracle()\n")
    L.append("| gate | reproduced | target | pass |\n|---|---|---|---|")
    g = G0["G0"]
    L.append(f"| G0 V0 strat AUROC (R_AB 2,686) | {g['V0_strat']:.4f} | 0.7415 | {g['pass']} |")
    L.append(f"| G0 Δ(V0 − judge_cheap_disg) strat | {g['delta']:.4f} {ci(g['ci'])} | +0.099 [0.049, 0.146] | {g['pass']} |")
    L.append(f"| G0 Δ long pool | {g['delta_long']:.4f} | +0.116 | {g['pass']} |")
    L.append(f"| G1 V0_rep vs frozen (|diff| > 1e-6) | {G1['n_mismatch']}/{G1['n_compared']} = {G1['mismatch_share']:.4%} | <= 0.5% | {G1['pass']} |")
    r = A["repro"]
    L.append(f"| c_exact pooled AUROC on Z | {r['c_exact_pooled_auroc_Z']:.4f} | 0.748 | {r['c_exact_pass']} |")
    L.append(f"| 3-pool plain c pooled AUROC | {r['c3_plain_pooled_auroc_Z']:.4f} | 0.7845 (eval-2 c_k3_best_oof) | {r['c3_pass']} |")
    o = A["oracle"]
    L.append(f"| eval-3 d_oracle 3-pool ALL / L25 | {o['3pool']['ALL']['d_oracle']:.4f} / {o['3pool']['L25']['d_oracle']:.4f} | 0.385 / 0.542 | {o['repro_pass']} |")
    L.append(f"| eval-3 END_MAJ 3-pool L25 d | {o['3pool']['L25']['d_END_MAJ_3pool']:.4f} | 0.735 | {abs(o['3pool']['L25']['d_END_MAJ_3pool'] - 0.735) < 0.002} |\n")
    # 2 AUROC
    L.append("## T2. Part A: AUROC per variant and cell (Z)\n\n# source: results/screen_E.json['auroc'] :: src/screen.py main()\n")
    cells = list(A["auroc"])
    L.append("| score | " + " | ".join(cells) + " |\n|---|" + "---|" * len(cells))
    for v in V + ["judge_cheap_disg", "judge_cheap_orig", "judge_cheap2_orig"]:
        L.append(f"| {NAMES.get(v, v)} | " + " | ".join(f"{A['auroc'][c][v]['auroc']:.3f} {ci(A['auroc'][c][v]['ci'])}" for c in cells) + " |")
    L.append("\nCell sizes (n / ERROR / CORRECT / sentences): " + "; ".join(
        f"{c}: {A['auroc'][c]['V0_frozen']['n']}/{A['auroc'][c]['V0_frozen']['n_err']}/{A['auroc'][c]['V0_frozen']['n_cor']}/{A['auroc'][c]['V0_frozen']['n_sent']}" for c in cells) + "\n")
    # 3 delta
    L.append("## T3. Part A: paired Δ AUROC vs V0 (frozen), same rows\n\n# source: results/screen_E.json['delta_vs_V0'] :: src/screen.py main()\n")
    L.append("| variant | " + " | ".join(cells) + " |\n|---|" + "---|" * len(cells))
    for v in ["V0_rep", "c_exact", "V1", "V2", "V3", "V4", "V5"]:
        L.append(f"| {NAMES[v]} | " + " | ".join(f"{A['delta_vs_V0'][c][v]['delta']:+.4f} {ci(A['delta_vs_V0'][c][v]['ci'])}" for c in cells) + " |")
    # 4 selection
    L.append(f"\n## T4. Part A: pre-registered selection (5 variants screened)\n\n# source: results/selection_E.json :: src/select_rule.py rule(), main(); freeze/selection.json :: src/freeze_part_a.py\n")
    L.append(f"Rule: {S['rule_text']}\n\n**Decision: {S['winner']}**\n")
    L.append("| variant | Δ LONG-strat | (i) >= +0.015 | (ii) L25 >= V0 | (iii) CTRL >= V0 − 0.01 | qualifies |\n|---|---|---|---|---|---|")
    for v, q in S["qualification"].items():
        L.append(f"| {NAMES[v]} | {q['delta_long']:+.4f} | {q['i_long_margin']} | {q['ii_L25']} | {q['iii_CTRL']} | {q['qualifies']} |")
    L.append(f"\nSelection stability (B = 500 within-stratum sentence resamples, reported not gating): {json.dumps(S['stability']['share_selected'])}. "
             f"Permutation null (B = 200 within-stratum label permutations, V4 re-cross-fitted): share of permutations in which ANY variant qualifies = "
             f"{S['permutation_null']['share_any_variant_qualifies']:.3f} (per variant {json.dumps(S['permutation_null']['share_per_variant'])}).\n")
    # 5 e/d
    L.append("## T5. Binary decomposition at c > 0.5 (V4: flag rate matched to V0)\n\n# source: results/screen_E.json['ed'] :: src/screen.py ed_block()\n")
    cuts = ["ALL", "LONG", "L25", "CTRL", "words_T1", "words_T2", "words_T3"]
    L.append("| score | " + " | ".join(f"{c} e / d" for c in cuts) + " |\n|---|" + "---|" * len(cuts))
    for v in V:
        L.append(f"| {NAMES[v]} | " + " | ".join(f"{A['ed'][c][v]['e']:.3f} / {A['ed'][c][v]['d']:.3f}" for c in cuts) + " |")
    L.append(f"\nV0 flag rate on Z {A['binary']['V0_flag_rate']:.4f}; V4 matched threshold {A['binary']['V4_threshold_flag_rate_matched']:.4f}.\n")
    L.append("### T5b. KEY DIAGNOSTIC: does d fall without e rising? (Δ vs V0, CI)\n\n# source: results/screen_E.json['key_diagnostic'] :: src/screen.py main()\n")
    L.append("| variant | cut | Δd [CI] | Δe [CI] | d falls without e rising |\n|---|---|---|---|---|")
    for c in ("words_T3", "L25", "LONG", "ALL", "CTRL"):
        for v in ["c_exact", "V1", "V2", "V3", "V4", "V5"]:
            k = A["key_diagnostic"][c][v]
            L.append(f"| {NAMES[v]} | {c} | {k['delta_d']:+.3f} {ci(k['delta_d_ci'])} | {k['delta_e']:+.3f} {ci(k['delta_e_ci'])} | {k['d_falls_without_e_rising']} |")
    L.append("\n### T5c. NET Δ(e+d), words T3 − T1 (eval-2 definition)\n\n# source: results/screen_E.json['NET_T3_minus_T1'] :: src/screen.py main()\n")
    L.append("| score | NET [CI] | Δe | Δd |\n|---|---|---|---|")
    for v in V:
        k = A["NET_T3_minus_T1"][v]
        L.append(f"| {NAMES[v]} | {k['net']:+.3f} {ci(k['ci'])} | {k['delta_e']:+.3f} | {k['delta_d']:+.3f} |")
    # 6 T9
    L.append("\n## T6. Error-endorsement e per T9 error class (ERROR rows of the class not flagged)\n\n# source: results/screen_E.json['t9_e'] :: src/screen.py main(); classes = exp-9 analyse.py classes() via src/labels.py t9_classes()\n")
    L.append("| class | n | " + " | ".join(NAMES[v] for v in V) + " |\n|---|---|" + "---|" * len(V))
    for cl, d in A["t9_e"].items():
        if d["n"]:
            L.append(f"| {cl} | {d['n']} | " + " | ".join(f"{d[v]['e']:.3f}" for v in V) + " |")
    # 7 oracle
    L.append("\n## T7. Oracle bound (eval-3 R_oracle, label-using diagnostic)\n\n# source: results/screen_E.json['oracle'] :: src/screen.py oracle()\n")
    L.append("| pool | cut | d_oracle | d_V0 | variant | d_v | e_v | gap_closed |\n|---|---|---|---|---|---|---|---|")
    for pool in ("9fam", "3pool"):
        for c in ("ALL", "LONG", "L25", "words_T3"):
            rec = A["oracle"][pool][c]
            for v, x in rec["variants"].items():
                gcl = x["gap_closed"] if isinstance(x["gap_closed"], str) else f"{x['gap_closed']:+.3f}"
                L.append(f"| {pool} | {c} | {rec['d_oracle']:.3f} | {x['d_V0']:.3f} | {NAMES[v]} | {x['d_v']:.3f} | {x['e_v']:.3f} | {gcl} |")
    # 8 context
    L.append("\n## T8. Context: Δ vs the cheap API judges (frozen exp-6 columns)\n\n# source: results/screen_E.json['delta_vs_judges'] :: src/screen.py main()\n")
    L.append("| contrast | ALL-strat | LONG-strat | L25 |\n|---|---|---|---|")
    for k in A["delta_vs_judges"]["ALL-strat"]:
        L.append(f"| {k} | " + " | ".join(f"{A['delta_vs_judges'][c][k]['delta']:+.3f} {ci(A['delta_vs_judges'][c][k]['ci'])}" for c in ("ALL-strat", "LONG-strat", "L25")) + " |")
    # 9 GG checker gates
    L.append("\n## T9. GG checker gates (google/gemini-2.5-flash, non-thinking, T = 0)\n\n# source: results/gg_gates_dev_v1.json, results/gg_gates_confirm_v2.json :: src/gg_gates.py run(), score()\n")
    L.append("| gate | half | prompt | balanced acc. | TPR | TNR | n YES / NO |\n|---|---|---|---|---|---|---|")
    for gx, half in ((gv1, "dev"), (gv2, "confirm")):
        for gate in ("G-A", "G-B"):
            x = gx[gate]
            L.append(f"| {gate} | {half} | {gx['version']} | {f(x['balanced_accuracy'])} | {f(x['tpr'])} | {f(x['tnr'])} | {x['n_yes']} / {x['n_no']} |")
    L.append(f"\nG-A per class, dev v1: {json.dumps({k: round(v['accuracy'], 3) for k, v in gv1['G-A']['per_class'].items()})}; "
             f"confirm v2: {json.dumps({k: round(v['accuracy'], 3) for k, v in gv2['G-A']['per_class'].items()})}. "
             f"G-B has {gv2['G-B']['n_yes_both_halves']} YES / {gv2['G-B']['n_no_both_halves']} NO pairs in total (< 60 YES): NOT_TESTABLE as a gate (F9), reported descriptively. "
             "The single allowed prompt revision (v1 -> v2) followed the failed G-A dev half (prompt_revision_v2.json).\n")
    # 10 GG dev gates
    gg_ = D["gates"]
    L.append(f"## T10. GG dev gates -> status {M1['GG']['status']}\n\n# source: results/gg_dev.json['gates'] :: src/gg_score.py main(), perturb_gates()\n")
    L.append("| gate | value | rule | pass |\n|---|---|---|---|")
    L.append(f"| g1 RENAME_SYN paired flip | {gg_['g1']['paired_flip']:.3f} (FA {gg_['g1']['FA_SYN']:.3f} vs paired-base FA {gg_['g1']['FA_paired_bases']:.3f}; all-base FA {gg_['g1']['FA_all_bases']:.3f}) | flip <= 0.05 and FA <= FA(base) + 0.05 | {gg_['g1']['pass']} |")
    L.append(f"| g2 MEANING_RENAME recall | GG {gg_['g2']['recall_gg']:.3f} vs c_align {gg_['g2']['recall_c_align']:.3f} (base FA GG {gg_['g2']['FA_base_gg']:.3f} / c_align {gg_['g2']['FA_base_c_align']:.3f}; recall given base endorsed {f(gg_['g2']['recall_given_base_endorsed_gg'])} / {f(gg_['g2']['recall_given_base_endorsed_c_align'])}) | >= c_align − 0.05 | {gg_['g2']['pass']} |")
    L.append(f"| g3 E strat AUROC | GG {gg_['g3']['gg']:.3f} vs V0 {gg_['g3']['V0']:.3f}, Δ CI {ci(gg_['g3']['delta_ci'])} | >= V0 − 0.01 | {gg_['g3']['pass']} |")
    L.append(f"| checker | G-A confirm BA {gg_['checker']['G-A_confirm_BA']:.3f}; G-B {gg_['checker']['G-B']} (descriptive BA {f(gg_['checker']['G-B_confirm_BA_descriptive'])}) | G-A >= 0.90 | {gg_['checker']['pass']} |")
    nn = gg_["NONCE_expected_failure"]
    L.append(f"\nRENAME_NONCE (pre-stated EXPECTED failure, not gated): FA {nn['FA']:.3f}, paired-base FA {nn['FA_paired_bases']:.3f}, paired flip {nn['paired_flip']:.3f} (n {nn['n']}).\n")
    L.append("### T10b. Rename invariance / MEANING_RENAME recall per metric and control type (PERTURB E-bases, c > 0.5)\n\n# source: results/gg_dev.json['perturb'] :: src/gg_score.py perturb_gates()\n")
    L.append("| metric | base FA (all) | SYN FA / flip | NONCE FA / flip | MEANING_RENAME recall | recall | base endorsed | by polarity |\n|---|---|---|---|---|---|---|")
    for m, x in D["perturb"].items():
        L.append(f"| {m} | {x['FA_base_all']:.3f} | {x['RENAME_SYN']['FA']:.3f} / {x['RENAME_SYN']['paired_flip']:.3f} | {x['RENAME_NONCE']['FA']:.3f} / {x['RENAME_NONCE']['paired_flip']:.3f} | "
                 f"{x['MEANING_RENAME']['recall']:.3f} | {f(x['MEANING_RENAME']['recall_given_base_endorsed'])} (n {x['MEANING_RENAME']['n_base_endorsed']}) | {json.dumps({k: round(v, 3) for k, v in x['MEANING_RENAME']['by_polarity'].items()})} |")
    L.append("\nBy base status (SYN, GG): " + json.dumps({k: {kk: round(vv, 3) if isinstance(vv, float) else vv for kk, vv in v.items()} for k, v in D["perturb"]["c_gg"]["RENAME_SYN"]["by_base_status"].items()}) + "\n")
    # 11 GG on E
    L.append("## T11. GG on E (Z): AUROC, e/d, T9 e\n\n# source: results/gg_dev.json['auroc'], ['ed'], ['t9_e'] :: src/gg_score.py main()\n")
    L.append("| score | " + " | ".join(D["auroc"]) + " |\n|---|" + "---|" * len(D["auroc"]))
    for s in ("c_gg", "c_gg_allyes", "c_exact", "V0_frozen"):
        L.append(f"| {NAMES.get(s, s)} | " + " | ".join(f"{D['auroc'][c][s]['auroc']:.3f} {ci(D['auroc'][c][s]['ci'])}" for c in D["auroc"]) + " |")
    for s in ("c_gg", "c_gg_allyes", "c_exact"):
        L.append(f"| Δ {NAMES.get(s, s)} − V0 | " + " | ".join(f"{D['auroc'][c][s + ' - V0']['delta']:+.3f} {ci(D['auroc'][c][s + ' - V0']['ci'])}" for c in D["auroc"]) + " |")
    L.append("\n| score | " + " | ".join(f"{c} e / d" for c in D["ed"]) + " |\n|---|" + "---|" * len(D["ed"]))
    for s in ("c_gg", "c_gg_allyes", "c_exact", "V0_frozen"):
        L.append(f"| {NAMES.get(s, s)} | " + " | ".join(f"{D['ed'][c][s]['e']:.3f} / {D['ed'][c][s]['d']:.3f}" for c in D["ed"]) + " |")
    L.append("\n| T9 class | n | GG e | GG all-yes e | exact e | V0 e |\n|---|---|---|---|---|---|")
    for cl, x in D["t9_e"].items():
        L.append(f"| {cl} | {x['n']} | {x['c_gg']:.3f} | {x['c_gg_allyes']:.3f} | {x['c_exact']:.3f} | {x['V0_frozen']:.3f} |")
    p = D["pairs_E"]
    L.append(f"\nNon-exact E node pairs: {p['n_nonexact_pairs']}; outcomes {json.dumps(p['why'])}; map found {p['share_map_found']:.3f}; gloss-rejected {p['share_gloss_rejected']:.3f}; capped {p['share_capped']:.3f}. "
             f"eqmv vs GG: {json.dumps(p['crosstab_align_vs_gg'])}.\n")
    L.append("### T11c. Gloss disagreements with the aligner (10 each)\n\n# source: results/gg_dev.json['examples'] :: src/gg_score.py main()\n")
    L.append("| direction | renamed pairs (GG YES: the accepting map; GG NO: the first kept map) | formula i | formula j |\n|---|---|---|---|")
    for lab_, key in (("GG YES, eqmv rejected", "GG_YES_align_rejected"), ("GG NO (gloss), eqmv accepted", "GG_NO_align_accepted")):
        for ex in D["examples"][key]:
            pairs = "; ".join(f"{it[1]} -> {it[2]}" for m in ex["maps"][:1] for it in m["nonidentity"]) or "(identity)"
            L.append(f"| {lab_} | {pairs} | `{ex['fol_i']}` | `{ex['fol_j']}` |")
    L.append("")
    c = D["cost"]
    L.append(f"## T12. GG cost\n\n# source: results/gg_dev.json['cost'] :: src/gg_score.py main(); cost_ledger.jsonl\n\n"
             f"| item | value |\n|---|---|\n| gloss sweep $ (E + PERTURB) | {c['gloss_sweep_usd_total_E_plus_PERTURB']:.4f} |\n| $ per call (<= 12 pairs) | {c['usd_per_call']:.6f} |\n"
             f"| FULL per E candidate: CPU s / $ (upper) | {c['FULL_per_E_candidate']['cpu_s']:.3f} / {c['FULL_per_E_candidate']['usd_upper']:.6f} |\n"
             f"| MARGINAL per candidate: CPU s / $ | {c['MARGINAL_per_candidate']['cpu_s']:.3f} / {c['MARGINAL_per_candidate']['usd']:.6f} |\n"
             f"| peer generation $ per sentence (7 families, shared with V0) | {c['peer_generation_usd_per_sentence']:.6f} |\n")
    if GB:
        L.append("## T13. SECONDARY GG_B (freelab family with B1-B5 bridges; PRIMARY-accepted pairs kept)\n\n# source: results/ggb_dev.json :: src/ggb_score.py main()\n")
        L.append(f"Status: {GB['status']}. {GB['bracket_note']}.\n")
        L.append("| score | " + " | ".join(GB["auroc"]) + " |\n|---|" + "---|" * len(GB["auroc"]))
        for s in ("c_ggb_allyes", "c_gg", "c_exact", "V0_frozen"):
            L.append(f"| {NAMES.get(s, s)} | " + " | ".join(f"{GB['auroc'][cc][s]['auroc']:.3f} {ci(GB['auroc'][cc][s]['ci'])}" for cc in GB["auroc"]) + " |")
        for s in ("c_ggb_allyes - V0", "c_gg - V0"):
            L.append(f"| Δ {s} | " + " | ".join(f"{GB['auroc'][cc][s]['delta']:+.3f} {ci(GB['auroc'][cc][s]['ci'])}" for cc in GB["auroc"]) + " |")
        L.append("\n| score | " + " | ".join(f"{cc} e / d" for cc in GB["ed"]) + " |\n|---|" + "---|" * len(GB["ed"]))
        for s in ("c_ggb_allyes", "c_gg", "c_exact", "V0_frozen"):
            L.append(f"| {NAMES.get(s, s)} | " + " | ".join(f"{GB['ed'][cc][s]['e']:.3f} / {GB['ed'][cc][s]['d']:.3f}" for cc in GB["ed"]) + " |")
        L.append("\n| T9 class | n | GG_B all-yes e (upper) | GG e (lower) | exact e | V0 e |\n|---|---|---|---|---|---|")
        for cl, x in GB["t9_e"].items():
            L.append(f"| {cl} | {x['n']} | {x['c_ggb_allyes']:.3f} | {x['c_gg']:.3f} | {x['c_exact']:.3f} | {x['V0_frozen']:.3f} |")
        L.append(f"\nGG_B search: {json.dumps(GB['search'])}; gloss: {GB['gloss']['n_items']} items, {GB['gloss']['n_calls']} calls, verdicts {json.dumps(GB['gloss']['verdict_counts'])}.\n")
    L.append("## T14. Independent audit (tests/audit_rederive.py; sklearn, no src/ import)\n\n# source: results/audit_rederive.json :: tests/audit_rederive.py main()\n")
    L.append(f"Decision re-derived: {AU['decision']} (match {AU['decision_match']}); best LONG Δ {AU['best_variant_long']} {AU['best_delta_long']:+.5f} (match 1e-9 {AU['delta_match_1e-9']}); "
             f"GG gate numbers match: {AU['gg']['match']}; shuffled-label placebo strat AUROCs {json.dumps({k: round(v, 3) for k, v in AU['placebo_shuffled_within_stratum'].items()})} (ok {AU['placebo_ok']}).\n")
    (ROOT / "tables.md").write_text("\n".join(L))
    print("tables.md", len(L), "lines")


if __name__ == "__main__":
    main()
