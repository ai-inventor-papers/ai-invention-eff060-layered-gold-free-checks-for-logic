"""T1 outputs: analysis_T1.json, verdict_T1.json, tables_T1.md, per_item_T1.jsonl, method_out.json, api_cost_ledger.json,
figures (house style via the aii-data-fig-gen generator)."""
from __future__ import annotations

import json
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from loguru import logger

from .common import DATA, RES, ROOT, jdump, jload, read_jsonl

FIG = ROOT / "figures"
CHART = Path(__file__).resolve().parents[6] / "tools/aii-data-fig-gen/scripts/chart_gen.py"


def f3(x, d=3):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "–"
    return f"{x:.{d}f}"


def ci3(c):
    if not c or c[0] is None:
        return "[–]"
    return f"[{c[0]:+.3f}, {c[1]:+.3f}]"


def ci3u(c):
    if not c or c[0] is None:
        return "[–]"
    return f"[{c[0]:.3f}, {c[1]:.3f}]"


# ===================================================================================================== tables
def tables(A) -> str:
    L = ["# T1 head-on API bar on held-out dataset E — tables", "",
         f"prereg_T1 sha256 `{A['prereg_T1_sha256']}`. Population: E_POOL PRIMARY under R_AB, n = {A['population']['n']} "
         f"({A['population']['n_error']} ERROR / {A['population']['n_correct']} CORRECT, {A['population']['n_sentences']} sentences). "
         "Scores are oriented (higher = more likely unfaithful). CIs: sentence-cluster percentile bootstrap, B = 2000, seed 0. "
         "'strat' = within-stratum AUROC (only ERROR/CORRECT pairs from the same source stratum count).", ""]
    V = A["verdict"]
    L += ["## Verdict", "# source: results/verdict_T1.json", "", "| criterion | status | key numbers |", "|---|---|---|"]
    ca = V["criteria"]["a"]
    L.append(f"| (a) c_score_align beats flash-lite disguised | **{ca['status']}** | R_AB strat Δ {f3(ca.get('R_AB_strat', {}).get('delta'))} "
             f"{ci3(ca.get('R_AB_strat', {}).get('ci'))}; long strat Δ {f3(ca.get('long_strat', {}).get('delta'))} "
             f"{ci3(ca.get('long_strat', {}).get('ci'))}; R_A L20+EXC Δ {f3(ca.get('R_A_L20EXC', {}).get('delta'))} |")
    cb = V["criteria"]["b"]
    L.append(f"| (b) adds signal beyond S4_full (nested) | **{cb['status']}** | strat Δ {f3(cb.get('strat', {}).get('delta'))} "
             f"{ci3(cb.get('strat', {}).get('ci'))}, null p95 {f3(cb.get('null_p95_strat'))}; pooled Δ {f3(cb.get('pooled', {}).get('delta'))} "
             f"{ci3(cb.get('pooled', {}).get('ci'))} |")
    cd = V["criteria"]["d"]
    L.append(f"| (d) frontier ratio ≥ 0.95 at ≤ 10% cost, or nested gain | **{cd['status']}** | ratio {f3(cd.get('ratio'))} "
             f"{ci3u(cd.get('ratio_ci'))}; cost ok {cd.get('cost_le_0.10x')}; nested CI>0 {cd.get('nested_CI_gt0')} |")
    cv = V["criteria"]["VEX"]
    L.append(f"| VEX confound control (sign > 0) | **{cv['status']}** | Δ {f3(cv.get('delta'))} {ci3(cv.get('ci'))}; strong form "
             f"{cv.get('strong_form_CI_gt0')} |")
    cm = V["criteria"]["M3"]
    L.append(f"| M3 length slope (consensus − judge) | **{cm['status']}** | words Δslope {f3(cm.get('diff'))} {ci3(cm.get('ci'))}; "
             f"n_conditions {f3(cm.get('ncond_diff'))} {ci3(cm.get('ncond_ci'))} |")
    L += ["", f"**Overall (this artifact): {V['overall_T1_this_artifact']}**", ""]
    if "robustness_BEST_API_CHEAP" in V:
        r = V["robustness_BEST_API_CHEAP"]
        L += [f"Robustness, bar = BEST_API_CHEAP (`{r['bar']}`): criterion (a) {r['criterion_a']} (R_AB strat Δ "
              f"{f3(r.get('R_AB_strat', {}).get('delta'))} {ci3(r.get('R_AB_strat', {}).get('ci'))}).", ""]
    for vb in ("judge_cheap_disg_vfb",):
        if vb in A["criterion_a"]:
            r = A["criterion_a"][vb]
            L += [f"Sensitivity, JSON-failure verdict fallback (`{vb}`): (a) holds = {r['holds']} (R_AB strat Δ "
                  f"{f3(r['R_AB_strat'].get('delta'))} {ci3(r['R_AB_strat'].get('ci'))}).", ""]
    # ---- (a) main table
    L += ["## (a) Item-level AUROC on R_AB (E_POOL PRIMARY)", "# source: results/analysis_T1.json a_head_on['R_AB pooled'], metrics_R_AB", "",
          "| metric | pooled AUROC [CI] | strat AUROC [CI] | AUPRC (prev) | tie rate | recall@FA.10 | $/item |", "|---|---|---|---|---|---|---|"]
    for m, d in A["metrics_R_AB"].items():
        if d.get("untestable"):
            continue
        L.append(f"| `{m}` | {f3(d['auroc'])} {ci3u(d['ci'])} | {f3(d['strat']['auroc'])} {ci3u(d['strat']['ci'])} | "
                 f"{f3(d['auprc'])} ({f3(d['prevalence'], 2)}) | {f3(d['tie_rate'], 2)} | {f3(d['at_FA0.10_E']['recall'])} | "
                 f"{('%.2e' % d['usd_per_item']) if d.get('usd_per_item') else '–'} |")
    L += ["", "## (a) Paired Δ AUROC, challenger − bar (stratified; pooled cells marked)", "# source: results/analysis_T1.json a_head_on", ""]
    bars = [b for b in ("judge_cheap_disg", "judge_cheap_orig", "judge_cheap2_disg", "judge_cheap2_orig", "L:judge_local_qwen8b_disg")]
    L += ["| cell | n (E/C) | challenger | " + " | ".join(f"− `{b}`" for b in bars) + " |", "|---|---|---|" + "---|" * len(bars)]
    for cname, c in A["a_head_on"].items():
        st = "strat" if any(k.endswith("[strat]") for k in c["deltas"]) else "pooled"
        for ch in ("c_score_align", "p_peer_text", "nf_c_score", "g_score", "p_text"):
            cells_ = []
            for b in bars:
                d = c["deltas"].get(f"{ch} - {b} [{st}]", {})
                cells_.append("–" if d.get("untestable") or d.get("delta") is None else f"{d['delta']:+.3f} {ci3(d['ci'])}")
            L.append(f"| {cname} [{st}] | {c['n_error']}/{c['n_correct']} | `{ch}` | " + " | ".join(cells_) + " |")
    # ---- (b)
    b = A["b_s4"]
    L += ["", "## (b) Cross-fitted stacks (OOF, identical folds_E) and nesting", "# source: results/analysis_T1.json b_s4", "",
          f"API columns entered S4_full (≥95% R_AB coverage): {', '.join(b['entered_api_columns']) or 'none'}; substituted: "
          f"{', '.join(b['substituted']) or 'none'}", "", "| stack | #features | pooled OOF AUROC [CI] | strat OOF AUROC [CI] |", "|---|---|---|---|"]
    for nm, d in b["fits"].items():
        L.append(f"| `{nm}` | {len(b['sets'][nm])} | {f3(d['pooled'].get('auroc'))} {ci3u(d['pooled'].get('ci'))} | "
                 f"{f3(d['strat'].get('auroc'))} {ci3u(d['strat'].get('ci'))} |")
    L += ["", "| nested / paired contrast | strat Δ [CI] | pooled Δ [CI] |", "|---|---|---|"]
    for k, d in b["nested"].items():
        L.append(f"| {k} | {f3(d['strat'].get('delta'))} {ci3(d['strat'].get('ci'))} | {f3(d['pooled'].get('delta'))} {ci3(d['pooled'].get('ci'))} |")
    pn = b["permutation_null"]
    L += ["", f"Permutation null ({pn['reps']} reps, labels permuted within fold × stratum, both stacks refit): strat p95 "
          f"{f3(pn['strat']['p95'])} (mean {f3(pn['strat']['mean'])}), observed {f3(pn['strat']['observed'])} at percentile "
          f"{f3(pn['strat']['observed_percentile'], 2)}; pooled p95 {f3(pn['pooled']['p95'])}, observed {f3(pn['pooled']['observed'])}.", ""]
    L += ["Largest mean standardised coefficients of S4_full + c_score_align (5 folds):", ""]
    for k, v in list(b["S4_full_plus_c_mean_coef"].items())[:10]:
        L.append(f"- `{k}`: {v['mean']:+.3f} (fold range {v['min']:+.3f} … {v['max']:+.3f})")
    # ---- (c)
    c = A["c_vex"]
    L += ["", "## (c) Vocab-exact (VEX) confound control", "# source: results/analysis_T1.json c_vex; results/vex_declaration.json", "",
          "| subset | n (E/C) | sentences | testable | stat | c_score_align − judge_cheap_disg | nf_c_score − judge_cheap_disg | p_peer_text − judge_cheap_disg |",
          "|---|---|---|---|---|---|---|---|"]
    for nm in ("VEX", "VEX_STRICT", "VEX_tierA_only"):
        v = c.get(nm, {})
        ds = [v.get("deltas", {}).get(f"{a} - judge_cheap_disg", {}) for a in ("c_score_align", "nf_c_score", "p_peer_text")]
        L.append(f"| {nm} | {v.get('n_error')}/{v.get('n_correct')} | {v.get('n_sentences')} | {v.get('testable')} | {v.get('stat_used')} | "
                 + " | ".join("–" if not d or d.get('delta') is None else f"{d['delta']:+.3f} {ci3(d['ci'])}" for d in ds) + " |")
    mr = c["aligner_masked_errors"]
    L += ["", f"Aligner-masked errors (tier B, auto VOCAB_GRAN, panel ERROR; n = {mr['n']}): recall at FA = 0.10 — " +
          ", ".join(f"`{m}` {v['recall']:.2f}" for m, v in mr["recall_FA0.10"].items()), ""]
    # ---- (d)
    d = A["d_frontier"]
    L += ["## (d) Frontier judge on the 284-row frame", "# source: results/analysis_T1.json d_frontier", "",
          f"Frame rows with R_AB labels: {d['n_frame_rows']} ({d['n_error']} ERROR / {d['n_correct']} CORRECT).", "",
          "| metric | n | AUROC [CI] | IPW AUROC [CI] |", "|---|---|---|---|"]
    for m, v in d["metrics"].items():
        if v.get("untestable"):
            L.append(f"| `{m}` | {v['n']} | untestable | – |")
            continue
        L.append(f"| `{m}` | {v['n']} | {f3(v['auroc'])} {ci3u(v['ci'])} | {f3(v['auroc_ipw'])} {ci3u(v['auroc_ipw_ci'])} |")
    if "ratio" in d:
        r = d["ratio"]
        L += ["", f"Ratio AUROC(c_score_align)/AUROC({r['best_frontier_view']}) = {f3(r['ratio'])} {ci3u(r['ci'])} (IPW {f3(r['ratio_ipw'])}); "
              f"Δ = {f3(r['delta'].get('delta'))} {ci3(r['delta'].get('ci'))}."]
        if "nested_frame" in d:
            nf = d["nested_frame"]
            L.append(f"Nested in frame (GroupKFold 5): [strong_orig + c_score_align] − [strong_orig] = {f3(nf['delta'])} {ci3(nf['ci'])} (n = {nf['n']}).")
        cc = d.get("cost", {})
        L.append(f"Cost per item: frontier ({', '.join(cc.get('frontier_views', []))}) ${f3(cc.get('frontier_usd_per_item_views_used'), 5)}; "
                 f"consensus FULL ${f3(cc.get('consensus_full_usd_per_item'), 6)}, MARGINAL ${f3(cc.get('consensus_marginal_usd_per_item'), 7)}.")
        if "orig_minus_disg_frontier" in d:
            o = d["orig_minus_disg_frontier"]
            L.append(f"Frontier orig − disg (frame): {f3(o.get('delta'))} {ci3(o.get('ci'))} (n = {o.get('n')}).")
    # ---- (e)
    e = A["e_M3"]
    L += ["", "## (e) M3: GEE slope of P(correct flag at matched FA = 0.10) per SD of sentence length", "# source: results/analysis_T1.json e_M3", "",
          "| metric | slope per SD words [model CI] | slope per SD n_conditions [model CI] | fit |", "|---|---|---|---|"]
    for m, v in e["slopes_words"].items():
        if "slope" not in v:
            L.append(f"| `{m}` | {v.get('skipped')} | – | – |")
            continue
        w2 = e["slopes_ncond"].get(m, {})
        L.append(f"| `{m}` | {v['slope']:+.3f} {ci3(v['ci_model'])} | {f3(w2.get('slope'))} {ci3(w2.get('ci_model'))} | {v['fit']} |")
    if "M3_words" in e:
        L += ["", f"M3 = slope(c_score_align) − slope(judge_cheap_disg): words {e['M3_words']['diff']:+.3f} {ci3(e['M3_words']['ci'])} "
              f"(B = {e['M3_words']['B_ok']}); n_conditions {e['M3_ncond']['diff']:+.3f} {ci3(e['M3_ncond']['ci'])}. Stacked-GEE interaction: "
              f"{e.get('stacked_interaction', {}).get('coef', float('nan')):+.3f} {ci3(e.get('stacked_interaction', {}).get('ci'))}."]
    # ---- (f)
    L += ["", "## (f) AUROC by complexity bin (pooled within bin; * = fails the ≥50/50, ≥25-sentence testability rule)",
          "# source: results/analysis_T1.json f_complexity", ""]
    fc = A["f_complexity"]
    mets = ["c_score_align", "p_peer_text", "nf_c_score", "judge_cheap_disg", "judge_cheap_orig", "judge_cheap2_disg", "S4_full_oof", "L:judge_local_qwen8b_disg"]
    for var, bins in fc.items():
        L += [f"**{var}**", "", "| bin | n (E/C) | " + " | ".join(f"`{m}`" for m in mets) + " | Δ c − cheap_disg [CI] |", "|---|---|" + "---|" * (len(mets) + 1)]
        for lab, r in bins.items():
            vals = [f3(r["metrics"].get(m, {}).get("auroc")) for m in mets]
            dd = r.get("delta_c_minus_cheapdisg", {})
            L.append(f"| {lab}{'' if r['testable'] else '*'} | {r['n_error']}/{r['n_correct']} | " + " | ".join(vals) +
                     f" | {f3(dd.get('delta'))} {ci3(dd.get('ci'))} |")
        L.append("")
    # ---- (g)
    g = A["g_contamination"]
    L += ["## (g) Contamination (original vs nonce-disguised) and test-retest", "# source: results/analysis_T1.json g_contamination", ""]
    for nm in ("judge_cheap", "judge_cheap2"):
        if nm in g:
            v = g[nm]
            L.append(f"- `{nm}`: Δ(orig−disg) on public MALLS gold as candidate {f3(v['delta_orig_minus_disg_GOLDSYS'])} "
                     f"{ci3(v['delta_orig_minus_disg_GOLDSYS_ci'])}; on E_POOL {f3(v['delta_orig_minus_disg_E'])} {ci3(v['delta_orig_minus_disg_E_ci'])}; "
                     f"DiD {f3(v['DiD'])} {ci3(v['DiD_ci'])}, MDE {f3(v['MDE'])}.")
    L.append(f"- GOLDSYS rows: {g['n'].get('GOLDSYS')} ({g['n'].get('GOLDSYS_error')} ERROR / {g['n'].get('GOLDSYS_correct')} CORRECT).")
    if "retest" in g:
        r = g["retest"]
        L.append(f"- flash-lite disguised test-retest ({r['n']} rows): Spearman {f3(r['spearman'])}, exact-match share {f3(r['exact_match'])}, "
                 f"mean |Δp| {f3(r['mean_abs_diff'])}.")
    # ---- (h)
    h = A["h_recall_by_group"]["FA0.10"]
    ms = [m for m in ("c_score_align", "p_peer_text", "nf_c_score", "judge_cheap_disg", "judge_cheap_orig", "judge_cheap2_disg", "judge_strong_orig", "S4_full_oof") if m in h["thresholds"]]
    L += ["", "## (h) Recall per error group at matched FA = 0.10 (thresholds from R_AB CORRECT rows; descriptive)",
          "# source: results/analysis_T1.json h_recall_by_group", "", "| group | n | " + " | ".join(f"`{m}`" for m in ms) + " |", "|---|---|" + "---|" * len(ms)]
    for gname, r in h["groups"].items():
        L.append(f"| {gname} | {r['n']} | " + " | ".join(f3(r["recall"].get(m), 2) for m in ms) + " |")
    # ---- (i)
    s = A["i_system"]
    L += ["", "## (i) System level (Kendall τ-b, mean score vs R_AB error rate; descriptive)", "# source: results/analysis_T1.json i_system", "",
          "| metric | τ-b over system×variant [CI] | τ-b over families [CI] |", "|---|---|---|"]
    for m in s["sysvar"]["tau_b"]:
        a1, a2 = s["sysvar"]["tau_b"][m], s["family"]["tau_b"].get(m, {})
        L.append(f"| `{m}` | {f3(a1['tau'])} {ci3(a1['ci'])} | {f3(a2.get('tau'))} {ci3(a2.get('ci'))} |")
    L += ["", f"({s['sysvar']['n_units']} system×variant rows, {s['family']['n_units']} families.)", ""]
    # ---- coverage / cost
    L += ["## Coverage of the API columns (R_AB PRIMARY rows)", "# source: results/analysis_T1.json api_coverage", "", "| column | coverage | status counts |", "|---|---|---|"]
    for cn, v in A["api_coverage"].items():
        L.append(f"| `{cn}` | {f3(v['coverage_RAB'])} | {v['status_RAB_primary']} |")
    L += ["", "## Placebos", "# source: results/analysis_T1.json placebo", "", f"{json.dumps(A['placebo'])}", ""]
    return "\n".join(L)


# ===================================================================================================== per-item + method_out
PREDICT = ["c_score_align", "g_score", "nf_c_score", "nf_g_score", "p_peer_text", "p_text", "l2_bow", "l3_z3",
           "judge_cheap_disg", "judge_cheap_orig", "judge_cheap2_disg", "judge_cheap2_orig", "judge_strong_orig", "judge_strong_disg",
           "judge_cheap_disg_vfb", "rt_nli_min", "rt_nli_fwd", "rt_nli_bwd", "rt_nli_contra", "rt_nli_min_alt", "rt_embed_cos",
           "sc5_eq_frac", "sc5_entropy", "S4_full_oof", "S4_local_oof", "S4_full_plus_c_score_align_oof", "PT_refit_oof",
           "PT_refit_NF_oof", "L:judge_local_qwen8b_disg", "L:judge_local_qwen8b_orig", "L:judge_local_llama8b_disg",
           "L:rt_nli_min_local", "L:sc5_local_eq_frac", "L:parse_fail", "L:pilot_rerun_jacc"]


def per_item(T, rows, regimes, api):
    V = jload(DATA / "vex_rows.json")
    out = []
    for x in rows:
        k = x["canonical_key"]
        r = {kk: x[kk] for kk in ("canonical_key", "exp6_row_key", "exp5_row_key", "item_id", "sentence_id", "fold_E", "pool", "parse_ok",
                                  "system", "sysvar", "family", "prompt_variant", "strata", "source_stratum", "label_tier", "final_label",
                                  "auto_label", "reading_choice", "repair_ops", "error_ops")}
        r.update({f"in_{g}": k in regimes[g] for g in ("R_AB", "R_A", "COVERAGE")})
        r["y_R_AB"] = regimes["R_AB"].get(k)
        v = V.get(k, {})
        r["vex"], r["vex_strict"] = bool(v.get("include")), bool(v.get("include_strict"))
        for m in PREDICT:
            val = T.value(m, k)
            r[m.replace("L:", "local__")] = None if val is None else round(float(val), 6)
            if m in api:
                r[m + "__status"] = api[m]["st"].get(k, "na")
                if "cost" in api[m] and k in api[m]["cost"]:
                    r[m + "__usd"] = api[m]["cost"][k]
                    r[m + "__secs"] = api[m]["secs"].get(k)
        out.append(r)
    with (RES / "per_item_T1.jsonl").open("w") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return out


def method_out(T, rows, regimes, A):
    V = jload(DATA / "vex_rows.json")
    ex = []
    for x in rows:
        k = x["canonical_key"]
        e = {"input": json.dumps({"text": x["text"], "candidate_fol": x["candidate_fol"], "system": x["system"],
                                  "prompt_variant": x["prompt_variant"]}, ensure_ascii=False), "output": x["final_label"]}
        for m in PREDICT:
            val = T.value(m, k)
            e["predict_" + m.replace("L:", "local_")] = "NA" if val is None else f"{float(val):.6f}"
        e.update({"metadata_canonical_key": k, "metadata_exp6_row_key": x["exp6_row_key"], "metadata_item_id": x["item_id"],
                  "metadata_sentence_id": x["sentence_id"], "metadata_fold_E": x["fold_E"], "metadata_pool": x["pool"],
                  "metadata_parse_ok": x["parse_ok"], "metadata_sysvar": x["sysvar"], "metadata_family": x["family"],
                  "metadata_strata": x["strata"], "metadata_label_tier": x["label_tier"], "metadata_in_R_AB": k in regimes["R_AB"],
                  "metadata_in_R_A": k in regimes["R_A"], "metadata_vex": bool(V.get(k, {}).get("include"))})
        ex.append(e)
    out = {"metadata": {"method_name": "T1 head-on API bar on held-out dataset E",
                        "description": "Oriented scores (higher = more likely unfaithful): frozen consensus metrics (exp 5), the new "
                                       "API judges (flash-lite / gpt-4.1-nano, original + disguised; gemini-3.1-pro-preview on the "
                                       "frame), API round trip, API SC-5, cross-fitted stacks (OOF), and local baselines (exp 6). "
                                       "output = dataset-E final label. NA = not scored (frame-only / outside the stack pool).",
                        "prereg_T1_sha256": A["prereg_T1_sha256"], "verdict": A["verdict"]["overall_T1_this_artifact"]},
           "datasets": [{"dataset": "E_heldout_T1", "examples": ex}]}
    jdump(out, ROOT / "method_out.json", indent=None)
    return len(ex)


def cost_ledger(A):
    costs = read_jsonl(RES / "costs.jsonl") if (RES / "costs.jsonl").exists() else []
    by = defaultdict(lambda: {"calls": 0, "usd": 0.0, "secs": [], "models": Counter()})
    for c in costs:
        b = by[c["component"]]
        b["calls"] += 1
        b["usd"] += c["cost"]
        b["secs"].append(c["seconds"])
        b["models"][c["model"]] += 1
    out = {"components": {k: {"calls": v["calls"], "usd": round(v["usd"], 6), "mean_s_call": float(np.mean(v["secs"])),
                              "mean_usd_call": v["usd"] / max(1, v["calls"]), "models": dict(v["models"])} for k, v in by.items()},
           "total_usd_from_usage_cost": round(sum(v["usd"] for v in by.values()), 6),
           "caps": jload(ROOT / "prereg_T1.json")["budget"]}
    ks = RES / "key_usage_log.json"
    if ks.exists():
        out["key_usage"] = jload(ks)
    jdump(out, RES / "api_cost_ledger.json")
    jdump({"spent": out["total_usd_from_usage_cost"], "by_component": {k: v["usd"] for k, v in out["components"].items()},
           "caps": out["caps"]["caps"], "cap_total": out["caps"]["cap_total"]}, RES / "budget_state.json")
    return out


# ===================================================================================================== figures
def _style():
    import sys
    sys.path.insert(0, str(CHART.parent))
    import matplotlib
    matplotlib.use("Agg")
    from chart_style import apply_house_style, PALETTE  # noqa: PLC0415
    apply_house_style()
    return PALETTE


def _finish(fig, name):
    from chart_geometry import assert_text_is_legible  # noqa: PLC0415
    from chart_style import (clear_legends_of_data, fit_legends, fit_tick_labels, fit_titles)  # noqa: PLC0415
    fit_legends(fig)
    clear_legends_of_data(fig)
    fit_tick_labels(fig)
    fit_titles(fig)
    clear_legends_of_data(fig)
    try:
        assert_text_is_legible(fig)
    except Exception as e:  # noqa: BLE001 - reported, the figure is still written for inspection
        logger.warning(f"legibility check {name}: {str(e)[:200]}")
    FIG.mkdir(exist_ok=True)
    fig.savefig(FIG / f"{name}.pdf")
    fig.savefig(FIG / f"{name}.png", dpi=200)


def figures(A):
    """forest_T1: ΔAUROC(c_score_align − judge_cheap_disg) with asymmetric percentile CIs over every cell;
    complexity_curves: AUROC (± CI) per words bin and per n_conditions bin."""
    PAL = _style()
    import matplotlib.pyplot as plt
    from chart_style import literal, place_legend  # noqa: PLC0415
    ok = {}
    rows = []
    for cname in ("R_AB pooled", "R_AB long (L25+L20+EXC)", "R_A L20+EXC", "R_A L20+EXC+CTRL", "COVERAGE (unparseable = ERROR)",
                  "R_AB L25", "R_AB L20", "R_AB EXC", "R_AB CTRL", "CONTESTED_AS_CORRECT", "CONTESTED_AS_ERROR", "ALL_TIERS", "R_AB_L25_NO_TOPUP"):
        c = A["a_head_on"].get(cname)
        if not c:
            continue
        st = "strat" if "c_score_align - judge_cheap_disg [strat]" in c["deltas"] else "pooled"
        for ch, off in (("c_score_align", -0.15), ("p_peer_text", 0.15)):
            d = c["deltas"].get(f"{ch} - judge_cheap_disg [{st}]", {})
            if d.get("delta") is not None and d.get("ci") and d["ci"][0] is not None:
                rows.append((f"{cname} [{st}]", ch, d["delta"], d["ci"], off))
    for nm in ("VEX", "VEX_STRICT"):
        v = A["c_vex"].get(nm, {})
        for ch, off in (("c_score_align", -0.15), ("p_peer_text", 0.15)):
            d = v.get("deltas", {}).get(f"{ch} - judge_cheap_disg", {})
            if d.get("delta") is not None and d.get("ci") and d["ci"][0] is not None:
                rows.append((f"{nm} [{v['stat_used']}]", ch, d["delta"], d["ci"], off))
    if rows:
        labels = list(dict.fromkeys(r[0] for r in rows))
        fig, ax = plt.subplots(figsize=(7, 0.36 * len(labels) + 1.4), layout="constrained")
        for j, (ch, name) in enumerate((("c_score_align", "consensus c_score_align"), ("p_peer_text", "PEER+TEXT fusion"))):
            rr = [r for r in rows if r[1] == ch]
            y = np.array([labels.index(r[0]) + r[4] for r in rr])
            x = np.array([r[2] for r in rr])
            lo = x - np.array([r[3][0] for r in rr])
            hi = np.array([r[3][1] for r in rr]) - x
            ax.errorbar(x, y, xerr=[lo, hi], fmt="o", color=PAL[j], ecolor=PAL[j], capsize=2.5, markersize=4.5, label=literal(name))
        ax.axvline(0, color="#999999", linestyle="--", linewidth=1)
        ax.set_yticks(range(len(labels)), labels=[literal(l) for l in labels])
        ax.invert_yaxis()
        ax.set_xlabel(literal("ΔAUROC vs flash-lite judge, disguised (95% CI)"))
        ax.set_title(literal("Consensus minus the cheap API judge on held-out E"))
        fig.legend(*ax.get_legend_handles_labels(), loc="outside lower center", ncol=2, frameon=False)  # no data under it
        _finish(fig, "forest_T1")
        plt.close(fig)
        ok["forest_T1"] = True
    fc = A["f_complexity"]
    fig, axes = plt.subplots(1, 2, figsize=(7, 3.3), layout="constrained", sharey=True)
    for ax, var in zip(axes, ("words", "n_conditions")):
        bins = list(fc[var].keys())
        xs = np.arange(len(bins))
        for j, (m, lab) in enumerate((("c_score_align", "c_score_align"), ("p_peer_text", "PEER+TEXT"),
                                      ("judge_cheap_disg", "flash-lite disg"), ("judge_cheap_orig", "flash-lite orig"),
                                      ("S4_full_oof", "S4_full"))):
            vals = [fc[var][b]["metrics"].get(m, {}) for b in bins]
            if any(v.get("auroc") is None for v in vals):
                continue
            y = np.array([v["auroc"] for v in vals])
            lo = y - np.array([v["ci"][0] for v in vals])
            hi = np.array([v["ci"][1] for v in vals]) - y
            ax.errorbar(xs + (j - 2) * 0.07, y, yerr=[lo, hi], marker="o", markersize=3.5, capsize=2, linewidth=1.2, color=PAL[j],
                        label=literal(lab) if ax is axes[0] else None)
        ax.set_xticks(xs, labels=[literal(b + ("" if fc[var][b]["testable"] else "*")) for b in bins])
        ax.set_xlabel(literal(var.replace("_", " ") + " (* = descriptive)"))
        ax.axhline(0.5, color="#bbbbbb", linewidth=0.8, linestyle=":")
    axes[0].set_ylabel(literal("AUROC on R_AB"))
    fig.legend(loc="outside lower center", ncols=5, fontsize=7)
    _finish(fig, "complexity_curves")
    plt.close(fig)
    ok["complexity_curves"] = True
    return ok
