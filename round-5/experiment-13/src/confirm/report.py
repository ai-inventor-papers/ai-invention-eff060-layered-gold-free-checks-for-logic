#!/usr/bin/env python3
"""Deliverables from results/analysis_rcomp.json (no new statistics here):
- results/confirm_verdict_rcomp.json (the verdict + flags + headline numbers);
- results/tables.md (every table has a '# source:' line naming file :: key and the producing function);
- results/old_label_agreement.json (extended with the old-vs-new shares);
- method_out.json (exp_gen_sol_out; one example per FREE row; predict_* = the metric scores as strings, higher = ERROR)."""
from __future__ import annotations

import json
from collections import Counter

from cc import RES, WS, dump, jl, setup_logger

logger = setup_logger("report")
AN = "results/analysis_rcomp.json"


def f(x, d=3):
    if x is None:
        return "–"
    if isinstance(x, bool):
        return str(x)
    if isinstance(x, (int,)):
        return str(x)
    try:
        return f"{float(x):.{d}f}"
    except (TypeError, ValueError):
        return str(x)


def ci(c, d=3):
    if not c or c[0] is None:
        return "–"
    return f"[{f(c[0], d)}, {f(c[1], d)}]"


def table(title: str, source: str, head: list[str], rows: list[list]) -> str:
    out = [f"## {title}", f"# source: {source}", "", "| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out) + "\n"


def verdict(A: dict) -> dict:
    c = A["confirmatory"]
    h = A["provisional_headline"]
    aud = (A.get("noise_correction") or {}).get("sources", {})
    flags = {"gate_failed_twice_fallback_B": True, "gate_v2_used": True, "underpowered": True, "soundness_bar_failed": None,
             "s6_flip": None, "s3_flip": A["sensitivities"]["s3_all_rows_incl_seen_iter3"]["flip_vs_primary"],
             "s1a_flip": A["sensitivities"]["s1a_drop_detector_rows"]["flip_vs_primary"], "partial_budget": False}
    return {"criterion": "(c) c_score_align - flash-lite judge, within-template AUROC, both views, both 95% CIs > 0, on the untouched gated set",
            "VERDICT": c["verdict"], "reason": c["reason"], "confirmatory_counts": {k: c[k] for k in ("disg", "orig")},
            "flags": flags,
            "flags_note": "soundness_bar_failed / s6_flip are not applicable: the SIG e2e gloss check and the Haiku-only regime need gloss "
                          "verdicts, which do not exist under FALLBACK B",
            "PROVISIONAL_NON_CONFIRMATORY": {
                "labels": "ERROR_CERT (y=1) vs MAPPED = UNRESOLVED_GLOSS_GATE_FAILED (y=0), untouched rows",
                "disg": {k: h["disg"][k] for k in ("n", "n_err", "n_cor", "auroc_a", "auroc_a_ci", "auroc_b", "auroc_b_ci", "delta", "ci")},
                "orig": {k: h["orig"][k] for k in ("n", "n_err", "n_cor", "auroc_a", "auroc_a_ci", "auroc_b", "auroc_b_ci", "delta", "ci")},
                "both_ci_gt_0_provisional": h["both_ci_gt_0"],
                "noise_corrected_delta_blind_audit_consensus": {v: (aud.get("consensus") or {}).get(v, {}).get("delta_corrected") for v in ("disg", "orig")},
                "must_not_be_counted_as_confirmation": True},
            "seals": {"labels_all": A["seals"]["label_seal_all"], "labels_untouched": A["seals"]["label_seal_untouched"],
                      "scores": "results/score_seal_rcomp.json", "all_verified_before_join": A["seals"]["ALL_OK"]}}


def main() -> None:
    A = json.loads((WS / AN).read_text())
    V = verdict(A)
    dump(RES / "confirm_verdict_rcomp.json", V)
    gd = json.loads((RES / "gate_diagnostics.json").read_text())
    T = ["# R_COMP FREE confirmation (iteration 5): tables\n",
         "Every number below comes from the file named on its `# source:` line. PROVISIONAL = ERROR_CERT vs MAPPED labels "
         "(non-confirmatory, see prereg_addendum_fallbackB.json). All AUROCs are within-template unless marked pooled; CIs are "
         f"template-stratified sentence-cluster bootstrap percentiles (B={A['B']}, seed {A['seed']}).\n"]
    # gate
    rows = []
    for k in ("gloss_v1_A", "gloss_v2_B"):
        d = gd[k]
        for c in ("haiku", "qwen", "both_yes"):
            rows.append([k, c, f(d[c]["balanced_accuracy"]), f(d[c]["recall_YES"]), f(d[c]["recall_NO"]), d[c]["no_verdict"],
                         ", ".join(d["classes_below_0.85"][c]) or "–"])
    T.append(table("Gloss gate (PASS needs BA >= 0.90 for haiku, qwen and both_yes)", "results/gate_diagnostics.json :: gloss_v*_* (confirm/gate_diagnostics.py::main)",
                   ["run", "checker", "BA", "recall YES", "recall NO", "NO_VERDICT", "classes < 0.85"], rows))
    rows = [[k, gd[k]["haiku_verdicted_only"]["balanced_accuracy"], gd[k]["single_checker_rules"]["haiku_only_pass"], gd[k]["single_checker_rules"]["qwen_only_pass"]]
            for k in ("gloss_v1_A", "gloss_v2_B")]
    T.append(table("Gate failure type (verdicted-only accuracy; single-checker rescue)", "results/gate_diagnostics.json (confirm/gate_diagnostics.py::main)",
                   ["run", "haiku BA on verdicted items", "haiku-only passes", "qwen-only passes"], rows))
    c = A["confirmatory"]
    T.append(table("Labels and confirmatory testability", f"{AN} :: confirmatory (confirm/join_and_test.py::confirmatory)",
                   ["population", "label counts", "n ERROR", "n CORRECT", "TESTABLE"],
                   [["all rows", json.dumps(c["label_counts_all"]), "", "", ""], ["untouched", json.dumps(c["label_counts_untouched"]), "", "", ""],
                    ["P0 disg", "", c["disg"]["n_ERROR"], c["disg"]["n_CORRECT"], c["disg"]["TESTABLE"]],
                    ["P0 orig", "", c["orig"]["n_ERROR"], c["orig"]["n_CORRECT"], c["orig"]["TESTABLE"]]]))
    T.append(f"**Confirmatory verdict for criterion (c): {V['VERDICT']}** ({V['reason']}).\n")
    h = A["provisional_headline"]
    T.append(table("PROVISIONAL headline: c_score_align vs flash-lite judge (untouched)", f"{AN} :: provisional_headline (confirm/join_and_test.py::headline)",
                   ["view", "n (ERR/MAPPED)", "AUROC c_align", "AUROC judge", "delta", "95% CI", "p"],
                   [[v, f"{h[v]['n']} ({h[v]['n_err']}/{h[v]['n_cor']})", f"{f(h[v]['auroc_a'])} {ci(h[v]['auroc_a_ci'])}",
                     f"{f(h[v]['auroc_b'])} {ci(h[v]['auroc_b_ci'])}", f(h[v]["delta"]), ci(h[v]["ci"]), f(h[v]["p_two_sided"], 4)] for v in ("disg", "orig")]))
    rows = []
    for m, x in A["metrics_untouched_all_scored"].items():
        w, p = x["within_template"], x["pooled"]
        rows.append([m, w["n"], f"{w['n_err']}/{w['n_cor']}", f(w.get("est")), ci(w.get("ci")), f(p.get("est"))])
    T.append(table("PROVISIONAL AUROC per metric (untouched, every scored row)", f"{AN} :: metrics_untouched_all_scored (confirm/join_and_test.py::metric_table)",
                   ["metric", "n", "ERR/MAPPED", "within-template AUROC", "95% CI", "pooled AUROC"], rows))
    T.append(table("PROVISIONAL secondary paired deltas", f"{AN} :: secondary_deltas (confirm/analysis_lib.py::paired_delta)",
                   ["delta", "n", "estimate", "95% CI", "p"],
                   [[k, v["n"], f(v["delta"]), ci(v["ci"]), f(v["p_two_sided"], 4)] for k, v in A["secondary_deltas"].items()]))
    T.append(table("PROVISIONAL nesting (5 sentence folds, cross-fitted logistic, rank features)", f"{AN} :: nested (confirm/analysis_lib.py::nested_block)",
                   ["comparison", "n", "AUROC full", "AUROC base", "delta", "95% CI", "perm null p95", "> null p95"],
                   [[k, v["n"], f(v["auroc_full"]), f(v["auroc_base"]), f(v["delta"]), ci(v["ci"]), f(v["perm_null_p95"]), v["delta_gt_null_p95"]]
                    for k, v in A["nested"].items()]))
    T.append(table("PROVISIONAL operating points", f"{AN} :: operating_points (confirm/analysis_lib.py::op_point)",
                   ["rule", "threshold (score >)", "recall", "FA", "precision"],
                   [[k, f(v["threshold_gt"]), f"{f(v['recall'])} {ci(v['recall_ci'])}", f"{f(v['FA'])} {ci(v['FA_ci'])}",
                     f"{f(v['precision'])} {ci(v['precision_ci'])}"] for k, v in A["operating_points"].items()]))
    S = A["sensitivities"]
    rows = []
    for k, v in S.items():
        if isinstance(v, dict) and "disg" in v:
            rows.append([k, f"{f(v['disg']['delta'])} {ci(v['disg']['ci'])}", f"{f(v['orig']['delta'])} {ci(v['orig']['ci'])}", v["both_ci_gt_0"], v.get("flip_vs_primary")])
    s9 = S["s9_orig_view_exp7_scored_rows_only"]["orig"]
    rows.append(["s9_orig_view_exp7_scored_rows_only", "–", f"{f(s9['delta'])} {ci(s9['ci'])}", "–", "–"])
    T.append(table("PROVISIONAL sensitivities (delta c_align - judge)", f"{AN} :: sensitivities (confirm/join_and_test.py::sensitivities)",
                   ["regime", "disg delta [CI]", "orig delta [CI]", "both CIs > 0", "flip"], rows))
    T.append(table("PROVISIONAL per template (s4)", f"{AN} :: sensitivities.s4_per_template (confirm/join_and_test.py::sensitivities)",
                   ["template", "n disg", "disg delta [CI]", "orig delta [CI]"],
                   [[t, v["disg"]["n"], f"{f(v['disg']['delta'])} {ci(v['disg']['ci'])}", f"{f(v['orig']['delta'])} {ci(v['orig']['ci'])}"]
                    for t, v in S["s4_per_template"].items()]))
    H = A["h_mech"]
    rows = [[k, v["n_nonagreeing_peer_slots"], f"{f(v['share_ERROR_CERT'])} {ci(v['share_ERROR_CERT_ci'])}",
             f"{f(v['share_UNRESOLVED_GLOSS_GATE_FAILED'])} {ci(v['share_UNRESOLVED_GLOSS_GATE_FAILED_ci'])}", v.get("bar_share_ERROR_ge_0.50", "–")]
            for k, v in H["i_nonagreeing_peers"].items()]
    T.append(table("PROVISIONAL H-MECH (i): labels of non-agreeing peers", f"{AN} :: h_mech.i_nonagreeing_peers (confirm/join_and_test.py::mech_i)",
                   ["candidates | rule", "peer slots", "share ERROR_CERT", "share MAPPED", "bar >= 0.50"], rows))
    sc = H.get("scatter", {})
    ed = H["iv_e_d"]
    rows = [["(ii) SCATTER SI_cor/SI_err", f"{f(sc.get('ratio', {}).get('ratio'))} {ci(sc.get('ratio', {}).get('ci'))}", ">= 2", sc.get("bar_ratio_ge_2")]]
    for r, v in H["net"].items():
        w = v.get("words_T3_minus_T1", {})
        rows.append([f"(iii) NET delta(e+d) W3-W1, {r}", f"{f(w.get('delta_e_plus_d'))} {ci(w.get('ci'))}", "> 0", v.get("bar_words_delta_gt_0")])
    rows.append(["(iv) d_align - d_exact (MAPPED not endorsed)", f"{f(ed['d_contrast']['d_align_minus_d_exact'])} {ci(ed['d_contrast']['ci'])}", "< 0",
                 ed["d_contrast"]["prediction_d_lower_under_align"]])
    for cn, v in ed["cells"].items():
        rows.append([f"(iv) e_align - e_exact, {cn} (n={v['n']})", f"{f(v['e_align_minus_exact'])} {ci(v['ci'])}", "> 0", v["prediction_e_higher_under_align"]])
    T.append(table("PROVISIONAL H-MECH (ii)-(iv)", f"{AN} :: h_mech (eval-2 mechanism.scatter_index / net_test / ed_decomposition, unchanged)",
                   ["item", "estimate [CI]", "bar", "result"], rows))
    ev = A["exploratory_variants"]
    T.append(table("EXPLORATORY consensus variants (Holm over 8)", f"{AN} :: exploratory_variants (confirm/join_and_test.py::exploratory_variants)",
                   ["delta", "estimate", "95% CI", "p", "p Holm"],
                   [[k, f(v["delta"]), ci(v["ci"]), f(v["p_two_sided"], 4), f(v["p_holm"], 4)] for k, v in ev.items() if not k.startswith("_")]))
    rows = []
    for view, o in A["complexity"].items():
        for dim, x in o.items():
            for k, v in x.items():
                rows.append([view, dim, k, f(v.get("delta", v.get("est"))), ci(v.get("ci"))])
    T.append(table("PROVISIONAL complexity (delta c_align - judge per bin; T3-T1 delta-of-deltas; per-metric slopes)",
                   f"{AN} :: complexity (confirm/join_and_test.py::complexity)", ["view", "dimension", "cell", "estimate", "95% CI"], rows))
    T.append(table("PROVISIONAL system level (12 systems; descriptive)", f"{AN} :: system_level (confirm/join_and_test.py::system_level)",
                   ["metric", "Kendall tau-b (system mean score vs ERROR rate)", "95% CI"],
                   [[m, f(v["kendall_tau_b"]), ci(v["ci"])] for m, v in A["system_level"].items() if isinstance(v, dict)]))
    cv = A["coverage"]
    T.append(table("Coverage over all 2,652 FREE rows (UNPARSEABLE 188, NO_OUTPUT 199 in the denominator)",
                   f"{AN} :: coverage (confirm/join_and_test.py::coverage)", ["metric", "scored", "share"],
                   [[m, v["scored"], f(v["share_of_all_2652"])] for m, v in cv["per_metric"].items()]))
    u = cv["unparseable_as_ERROR_untouched"]
    T.append(table("PROVISIONAL unparseable-as-ERROR convention (every metric = 1.0 on UNPARSEABLE rows)",
                   f"{AN} :: coverage.unparseable_as_ERROR_untouched", ["view", "n", "AUROC c_align", "AUROC judge", "delta [CI]"],
                   [[v, u[v]["n"], f(u[v]["auroc_a"]), f(u[v]["auroc_b"]), f"{f(u[v]['delta'])} {ci(u[v]['ci'])}"] for v in ("disg", "orig")]))
    co = A["cost"]
    T.append(table("Cost (metric cost; the labelling cost is separate)", f"{AN} :: cost (confirm/join_and_test.py::costs)", ["quantity", "value"],
                   [[k, json.dumps(v) if isinstance(v, dict) else f(v, 6)] for k, v in co.items() if k != "note"]))
    au = json.loads((RES / "audit_report.json").read_text()) if (RES / "audit_report.json").exists() else None
    if au:
        rows = []
        for n, b in au["by_auditor"].items():
            rows.append([n, b["ERROR_CERT"]["n_verdict"], f"{f(b['ERROR_CERT']['unfaithful_share'])} {ci(b['ERROR_CERT']['unfaithful_ci'])}",
                         b["MAPPED"]["n_verdict"], f"{f(b['MAPPED']['faithful_share'])} {ci(b['MAPPED']['faithful_ci'])}",
                         f(b["contamination_a_error_side"]), f(b["contamination_b_mapped_side"])])
        T.append(table("Blind two-family audit of the provisional labels (100 ERROR_CERT + 100 MAPPED, untouched)",
                       "results/audit_report.json :: by_auditor (confirm/audit_blind.py::report)",
                       ["auditor", "n ERROR_CERT", "ERROR_CERT precision (UNFAITHFUL)", "n MAPPED", "MAPPED faithful", "a (ERR side, excl. UNSURE)",
                        "b (MAPPED side, excl. UNSURE)"], rows))
        T.append(f"Auditor agreement: {json.dumps(au.get('auditor_agreement'))}\n")
    nc = A.get("noise_correction")
    if nc:
        rows = []
        for s, b in nc["sources"].items():
            for v in ("disg", "orig"):
                x = b[v]
                rows.append([s, v, f(b["a"]), f(b["b"]), f(x["auroc_c_align_corrected"]), f(x["auroc_judge_corrected"]), f(x["delta_obs"]),
                             f(x["delta_corrected"]), ci(x["delta_ci_corrected"])])
        T.append(table("Noise-corrected PROVISIONAL AUROCs (non-differential contamination assumption)", f"{AN} :: noise_correction (confirm/join_and_test.py::noise_correction)",
                       ["contamination source", "view", "a", "b", "AUROC c_align corr.", "AUROC judge corr.", "delta obs", "delta corr.", "delta CI corr."], rows))
        T.append("Validity (all corrected AUROCs within [0, 1]): `" + json.dumps({s_: b["valid_all_corrected_auroc_in_0_1"] for s_, b in nc["sources"].items()})
                 + "`. A corrected AUROC above 1 means the non-differential assumption is violated; the differential check below shows why "
                 "(audited-faithful ERROR_CERT rows still get high consensus scores).\n")
        T.append("Differential check (mean score by label x auditor consensus): `" + json.dumps(nc["differential_check_mean_scores"]) + "`\n")
    av = A.get("audit_labelled_view")
    if av:
        rows = []
        for yc in ("y_aud", "y_aud_and_label"):
            for v in ("disg", "orig", "c_exact_minus_judge_disg"):
                x = av[yc][v]
                rows.append([yc, v, x["n"], f"{x['n_err']}/{x['n_cor']}", f(x.get("auroc_a")), f(x.get("auroc_b")), f(x.get("delta")), ci(x.get("ci"))])
        T.append(table("EXPLORATORY audit-labelled view (LLM-audited, gold-informed labels on the audit sample)",
                       f"{AN} :: audit_labelled_view (confirm/join_and_test.py::audit_view)",
                       ["labels", "comparison", "n", "ERR/COR", "AUROC a", "AUROC b", "delta", "95% CI"], rows))
    fr = A.get("frontier")
    if fr:
        rows = [[m, v["n"], f(v.get("est")), ci(v.get("ci"))] for m, v in fr["auroc"].items()]
        T.append(table("STEP F frontier judge (gemini-3.1-pro, original view; PROVISIONAL labels; 150-row sample)",
                       f"{AN} :: frontier (confirm/join_and_test.py::frontier_view)", ["metric", "n", "within-template AUROC", "95% CI"], rows))
        x, y = fr["c_align_minus_frontier"], fr["frontier_minus_flashlite_orig"]
        n1, n2 = fr["nested_[frontier + c] - [frontier]"], fr["nested_[c + frontier] - [c]"]
        T.append(table("STEP F paired comparisons", f"{AN} :: frontier", ["comparison", "estimate", "95% CI", "extra"],
                       [["c_align - frontier", f(x["delta"]), ci(x["ci"]), f"ratio {f(x['ratio'])} {ci(x['ratio_ci'])}"],
                        ["frontier - flash-lite (orig)", f(y["delta"]), ci(y["ci"]), ""],
                        ["[frontier + c] - [frontier]", f(n1["delta"]), ci(n1["ci"]), f"null p95 {f(n1['perm_null_p95'])}"],
                        ["[c + frontier] - [c]", f(n2["delta"]), ci(n2["ci"]), f"null p95 {f(n2['perm_null_p95'])}"],
                        ["frontier $/call, s/call", f(fr["cost_usd_per_call_mean"], 5), f(fr["seconds_per_call_mean"], 1), ""]]))
    pl = A["placebos"]
    T.append(table("Placebos", f"{AN} :: placebos (confirm/join_and_test.py::placebos)", ["check", "result", "pass"],
                   [["within-template label shuffles: delta CI covers 0", f"{pl['label_shuffle_within_template']['delta_ci_covers_0']}/{pl['label_shuffle_within_template']['n']}",
                     pl["label_shuffle_within_template"]["pass_ge_90pct"]],
                    ["post-hoc supplement: 100 shuffles, delta CI covers 0", f"{pl.get('supplement_100_shuffles', {}).get('delta_ci_covers_0')}/{pl.get('supplement_100_shuffles', {}).get('n')}",
                     "(nominal 95/100)"],
                    ["random score AUROC", f"{f(pl['random_score']['auroc'])} {ci(pl['random_score']['ci'])}", pl["random_score"]["covers_0.5"]]]))
    (RES / "tables.md").write_text("\n".join(T))
    # ---------------- old-label agreement extension
    ol = json.loads((RES / "old_label_agreement.json").read_text())
    labs = jl(RES / "rcomp_free_labels_final.jsonl")
    oe = [r for r in labs if r["seen_iter3"] and r["old_label_iter3"] == "ERROR"]
    oc = [r for r in labs if r["seen_iter3"] and r["old_label_iter3"] == "CORRECT"]
    ol["iter5_extension"] = {"old_tierA_ERROR_now_CORRECT_share": sum(r["label"] == "CORRECT" for r in oe) / max(len(oe), 1),
                             "old_tierA_ERROR_now_MAPPED_share": sum(r["label"] == "UNRESOLVED_GLOSS_GATE_FAILED" for r in oe) / max(len(oe), 1),
                             "old_tierA_ERROR_now_ERROR_CERT_share": sum(r["label"] == "ERROR_CERT" for r in oe) / max(len(oe), 1),
                             "old_tierA_CORRECT_now_ERROR_share": sum(r["label_binary"] == "ERROR" for r in oc) / max(len(oc), 1),
                             "n_old_ERROR": len(oe), "n_old_CORRECT": len(oc),
                             "note": "under FALLBACK B no row is CORRECT; MAPPED = UNRESOLVED_GLOSS_GATE_FAILED"}
    dump(RES / "old_label_agreement.json", ol)
    build_method_out(A, V)
    logger.info(f"verdict {V['VERDICT']}; tables.md written")


def build_method_out(A: dict, V: dict) -> None:
    items = jl(RES / "per_item_rcomp_free.jsonl")
    text = {r["row_key"]: r["text"] for r in jl(RES / "rcomp_free_labels_final.jsonl")}
    preds = ["c_score_align", "c_exact", "c_score_hyb", "c_score_nf", "g_align", "g_nf", "judge_cheap_disg", "judge_cheap_orig", "judge_local_disg",
             "V1_c_pn", "V2_c_rw", "V3_c_pn_rw", "V4_c_two_channel", "V5_c_v5"]
    ex = []
    for r in items:
        e = {"input": json.dumps({"text": text[r["row_key"]], "candidate_fol": r["candidate_fol"], "template_id": r["template_id"]},
                                 ensure_ascii=False),
             "output": r["label"]}
        for p in preds:
            e[f"predict_{p}"] = "" if r.get(p) is None else f"{float(r[p]):.6f}"
        for k in ("row_key", "sentence_id", "template_id", "slot", "system", "family", "prompt_variant", "words", "word_tercile", "nconds_weak",
                  "label_binary", "label_provisional", "untouched", "seen_iter3", "s1_flag", "cert_dominant", "coverage_status",
                  "judge_cheap_orig_source"):
            e[f"metadata_{k}"] = r.get(k)
        ex.append(e)
    h = A["provisional_headline"]
    meta = {"method_name": "cross-family solver consensus (c_score_align) vs LLM judge on R_COMP FREE",
            "description": "Iteration-5 confirmation attempt of criterion (c). Scores sealed before labels; labels from the dataset-5 labeller "
                           "resumed once; the gloss gate failed twice -> FALLBACK B -> NOT_TESTABLE. Predict_* are metric scores "
                           "(higher = more likely ERROR). output = the sealed final label.",
            "verdict": V["VERDICT"], "flags": V["flags"],
            "provisional_non_confirmatory": {v: {"auroc_c_align": h[v]["auroc_a"], "auroc_judge": h[v]["auroc_b"], "delta": h[v]["delta"],
                                                 "ci": h[v]["ci"]} for v in ("disg", "orig")},
            "label_seal": V["seals"], "orientation": "higher = more likely ERROR", "templated_text_caveat": "R_COMP is templated English (9 templates)"}
    out = {"metadata": meta, "datasets": [{"dataset": "R_COMP_FREE", "examples": ex}]}
    (WS / "method_out.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
    logger.info(f"method_out.json: {len(ex)} examples; label counts {dict(Counter(e['output'] for e in ex))}")


if __name__ == "__main__":
    main()
