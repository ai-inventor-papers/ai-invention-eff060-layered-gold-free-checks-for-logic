"""Assemble eval_out.json (exp_eval_sol_out schema), the VERDICT block and the two figures."""
from __future__ import annotations

import json
import re
import sys
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger

import steps_core as sc

FIG_SKILL = Path("/ai-inventor/.claude/skills/aii-data-fig-gen/scripts")


def jsafe(o):
    if isinstance(o, dict):
        return {str(k): jsafe(v) for k, v in o.items()}
    if isinstance(o, (list, tuple, set)):
        return [jsafe(v) for v in o]
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating, float)):
        return None if (np.isnan(o) or np.isinf(o)) else float(o)
    if isinstance(o, np.bool_):
        return bool(o)
    if isinstance(o, np.ndarray):
        return jsafe(o.tolist())
    if isinstance(o, pd.DataFrame):
        return jsafe(o.to_dict(orient="records"))
    if isinstance(o, pd.Series):
        return jsafe(o.to_dict())
    return o


def key(*parts) -> str:
    k = "_".join(str(p) for p in parts)
    k = re.sub(r"[^A-Za-z0-9_]", "_", k)
    k = re.sub(r"_+", "_", k).strip("_")
    return k if re.match(r"^[A-Za-z_]", k) else "m_" + k


def num(v):
    if v is None:
        return None
    if isinstance(v, (bool, np.bool_)):
        return float(v)
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return None if (np.isnan(f) or np.isinf(f)) else f


def build_metrics_agg(OUT: dict) -> dict:
    M = {}

    def put(k, v):
        f = num(v)
        if f is not None:
            M[key(k)] = f
    rd = OUT["rederivation"]
    put("rederivation_n_checks", rd["n_checks"])
    put("rederivation_n_match", rd["n_match"])
    for k, v in OUT["bookkeeping"]["sets"].items():
        put(f"bookkeeping_{k}", v)
    for rn, d in OUT["regimes"].items():
        cs = d["common_set"]
        for q in ("n", "n_err", "n_correct", "n_sentences"):
            put(f"regime_{rn}_{q}", cs[q])
        put(f"regime_{rn}_testable", cs["testable"])
    for rn, d in OUT["common_items"].items():
        tab = d["table"]
        for _, r in tab.iterrows():
            m = r["col"] + ("" if r.get("item_set", "COMMON") == "COMMON" else "_subset")
            for q in ("auroc", "auroc_ci_lo", "auroc_ci_hi", "auprc", "tie_frac", "delta_vs_judge", "delta_ci_lo", "delta_ci_hi",
                      "delta_p_boot", "delong_p", "delong_clustered_p", "holm_p_boot", "thr_fa", "thr_recall", "thr_prec_at_prev10"):
                if q in r:
                    put(f"common_{rn}_{q}_{m}", r[q])
        for fr in d.get("frontier_same_item", []):
            put(f"frontier_{rn}_{fr['strong']}_minus_{fr['cheap']}_delta", fr["delta"])
            put(f"frontier_{rn}_{fr['strong']}_minus_{fr['cheap']}_ci_lo", fr["ci"][0])
            put(f"frontier_{rn}_{fr['strong']}_minus_{fr['cheap']}_p", fr["p_boot"])
    for rn, vv in OUT["rule_verdicts"].items():
        for cand, v in vv.items():
            put(f"rule_{rn}_{cand}_pass_expA", v["verdict_expA_prereg_plus_delta"] == "PASS")
            put(f"rule_{rn}_{cand}_pass_strategy_tie003", v["verdict_strategy_with_tie_margin_0.03"] == "PASS")
            put(f"rule_{rn}_{cand}_delta", v["delta"])
    ptp = OUT["SCREEN_PREVIEW_NOT_CONFIRMATION_peer_text_preview"]
    for rn, d in ptp.items():
        if rn == "F3_preview" or "models" not in d:
            continue
        for mname, md in d["models"].items():
            put(f"preview_{rn}_{mname}_auroc", md["oof_auroc_seed0_Dfolds"])
            put(f"preview_{rn}_{mname}_auroc_sd5seeds", md["oof_auroc_sd_5seeds"])
        for k, v in d.items():
            if k.startswith("delta_") and isinstance(v, dict):
                put(f"preview_{rn}_{k}", v["delta"])
                put(f"preview_{rn}_{k}_ci_lo", v["ci"][0])
                put(f"preview_{rn}_{k}_ci_hi", v["ci"][1])
                put(f"preview_{rn}_{k}_p", v["p_boot"])
    f3 = ptp["F3_preview"]
    put("preview_F3_recall_on_flipped_FA010", f3.get("recall_on_flipped_CORRECT_to_ERROR_at_FA0.10"))
    for rn, v in f3["per_regime"].items():
        put(f"preview_F3_{rn}_achieved_FA", v["achieved_FA_on_CORRECT"])
        put(f"preview_F3_{rn}_fusedH_shipped_FA", v["fused_H_shipped_flag_FA_same_items"])
    pp = OUT["SCREEN_PREVIEW_NOT_CONFIRMATION_P1_P2"]
    for rn in ("R_SOLVER_CONS", "R_ADJ_AB", "R_ADJ_ALL"):
        for k, v in pp[rn]["P1"].items():
            put(f"p1_{rn}_{k}_code", v["code"])
        p2 = pp[rn]["P2"]
        put(f"p2a_{rn}_code", {"CONFIRMED": 1, "PARTIAL": 0.5}.get(p2["P2a_verdict"], 0))
        put(f"p2b_{rn}_code", {"CONFIRMED": 1, "CONFIRMED_POINT_ONLY_DELTA_CI_INCLUDES_0": 0.5}.get(p2["P2b_verdict"], 0))
        for comp in ("PT_vs_c_score", "PT_vs_bow_uncarried", "PT_vs_l3_score", "PT_vs_judge"):
            dd = p2["decomposition"][comp]
            put(f"p2_{rn}_{comp}_delta", dd["delta"])
            put(f"p2_{rn}_{comp}_endorsed_part", dd["endorsed_part_auroc_units"])
            put(f"p2_{rn}_{comp}_nonendorsed_part", dd["nonendorsed_part_auroc_units"])
        put(f"p2_{rn}_rho_cscore_PTtext_errors", p2["spearman_c_score_vs_PTtext_oof_errors"]["rho"])
        put(f"p2_{rn}_rho_cscore_PTtext_errors_ci_hi", p2["spearman_c_score_vs_PTtext_oof_errors"]["ci"][1])
        dec = p2["decomposition"]["PT_vs_best_single"]
        put(f"p2_{rn}_delta_PT_vs_best_single", dec["delta"])
        put(f"p2_{rn}_endorsed_share", dec["endorsed_share"])
        put(f"p2_{rn}_endorsed_part", dec["endorsed_part_auroc_units"])
        put(f"p2_{rn}_nonendorsed_part", dec["nonendorsed_part_auroc_units"])
        put(f"p2_{rn}_peer_endorsed_share_of_errors", p2["peer_endorsed_share_of_errors"])
    ce = pp["C_endorsement_reproduction"]
    put("c_endorsement_share_reproduced", ce["endorsed_share"])
    C = OUT["judge_matched_fa_and_contamination"]["contamination"]
    for _, r in C.iterrows():
        put(f"contam_{r['judge']}_{r['quantity']}", r["value"])
        if r["mde_80"] is not None and not (isinstance(r["mde_80"], float) and np.isnan(r["mde_80"])):
            put(f"contam_{r['judge']}_{r['quantity']}_mde80", r["mde_80"])
    for _, r in OUT["judge_matched_fa_and_contamination"]["matched_fa_recall_FA010_ALL"].iterrows():
        put(f"judge_recall_FA010_{r['regime']}_{r['judge']}_orig", r["recall_orig"])
        put(f"judge_recall_FA010_{r['regime']}_{r['judge']}_disg", r["recall_disg"])
        put(f"judge_recall_FA010_{r['regime']}_{r['judge']}_diff_ci_lo", r["ci_lo"])
    mf = OUT["mustfix"]["flags"]
    for k, v in mf.items():
        put(f"mustfix_rows_{k}", v)
    for k, v in OUT["mustfix"]["panel_calibration_recomputed"].items():
        for kk, vv in v.items():
            put(f"panelcal_{k}_{kk}", vv)
    put("candidate_B_files_produced", OUT["candidate_B"]["files_produced"])
    for _, r in OUT["complexity"]["gee"].iterrows():
        put(f"gee_{r['regime']}_{r['metric']}_interaction", r["coef_interaction"])
    for _, r in OUT["regime_shift"]["kendall_tau"].iterrows():
        put(f"tau_{r['regime_1']}_vs_{r['regime_2']}", r["kendall_tau_b"])
    for _, r in OUT["regime_shift"]["label_only_shift"].iterrows():
        if r["from"] == "R_SOLVER_CONS" and r["to"] in ("R_ADJ_AB", "R_ADJ_ALL", "R_ADJ_A"):
            put(f"labelshift_{r['to']}_{r['metric']}", r["label_only_shift"])
            put(f"labelshift_{r['to']}_{r['metric']}_ci_lo", r["label_only_ci_lo"])
            put(f"labelshift_{r['to']}_{r['metric']}_ci_hi", r["label_only_ci_hi"])
    return M


def build_verdict(OUT: dict) -> dict:
    V = {"per_regime_rule_verdicts": {}, "P1": {}, "P2": {}}
    for rn, vv in OUT["rule_verdicts"].items():
        V["per_regime_rule_verdicts"][rn] = {c: {"expA_prereg+delta": v["verdict_expA_prereg_plus_delta"],
                                                 "strategy_tie_margin_0.03": v["verdict_strategy_with_tie_margin_0.03"],
                                                 "failing_clauses": v["failing_clauses"], "testable": v["testable"],
                                                 "delta_vs_judge_cheap_disg": v["delta"], "ci": v["delta_ci"]} for c, v in vv.items()}
    pp = OUT["SCREEN_PREVIEW_NOT_CONFIRMATION_P1_P2"]
    for rn in ("R_SOLVER_CONS", "R_ADJ_AB", "R_ADJ_ALL"):
        V["P1"][rn] = {k: v["verdict"] for k, v in pp[rn]["P1"].items()}
        V["P2"][rn] = {"P2a_disjointness": pp[rn]["P2"]["P2a_verdict"], "P2b_gain_from_endorsed": pp[rn]["P2"]["P2b_verdict"]}
    ptp = OUT["SCREEN_PREVIEW_NOT_CONFIRMATION_peer_text_preview"]
    beats, bar = {}, {}
    for rn, d in ptp.items():
        if rn == "F3_preview" or "delta_PT_oof_vs_judge_cheap_disg" not in d:
            continue
        dd = d["delta_PT_oof_vs_judge_cheap_disg"]
        testable = OUT["regimes"][rn]["common_set"]["testable"]
        sig = dd["ci"][0] is not None and dd["ci"][0] > 0
        beats[rn] = {"delta": dd["delta"], "ci": dd["ci"], "testable": testable, "CI_above_0": bool(sig)}
        bar[rn] = f"PT - judge_cheap_disg = {dd['delta']:+.3f} [{dd['ci'][0]:+.3f}, {dd['ci'][1]:+.3f}]" + ("" if testable else " (UNTESTABLE: sign only)")
    testable_L = {k: v for k, v in beats.items() if v["testable"] and OUT["regimes"][k]["track"] == "L"}
    if testable_L and all(v["CI_above_0"] for v in testable_L.values()):
        verdict = "YES"
    elif testable_L and not any(v["CI_above_0"] for v in testable_L.values()):
        verdict = "NO"
    else:
        verdict = "REGIME_DEPENDENT"
    V["PEER_TEXT_beats_judge_on_screen_every_testable_L_regime"] = verdict
    V["PEER_TEXT_vs_judge_per_regime"] = beats
    V["what_iteration2_confirmation_must_beat"] = bar
    V["caveat"] = ("SCREEN PREVIEW: 2023 Logic-LM outputs, short sentences; PT is cross-fitted on the same screen; the bootstrap does not "
                   "refit per resample (CI understates model-selection variance; 5-seed spread reported). Not confirmation.")
    return V


# ------------------------------------------------------------------------------------------------ figures
def _style():
    sys.path.insert(0, str(FIG_SKILL))
    import chart_style as cs  # noqa: E402
    cs.apply_house_style()
    return cs


def fig_regime_shift(OUT, fig_dir: Path):
    import matplotlib.pyplot as plt
    M = pd.DataFrame(OUT["regime_shift"]["auroc_matrix"]).set_index("metric")
    regs = [r for r in ["R_SOLVER_CONS", "R_SOLVER_OWN_A", "R_SOLVER_OWN_C", "R_SOLVER_OWN_D", "R_ADJ_ALL", "R_ADJ_AB", "R_ADJ_A",
                        "R_ADJ_AB_CONT_C", "R_ADJ_AB_CONT_E", "L_UNPARSEABLE_AS_ERROR"] if r in M.columns]
    mets = [m for m in sc.HEADLINE_L + ["PT_oof", "PTJ_oof"] if m in M.index]
    A = M.loc[mets, regs].astype(float)
    SH = pd.DataFrame(OUT["regime_shift"]["label_only_shift"])
    tgt = [r for r in ["R_ADJ_ALL", "R_ADJ_AB", "R_ADJ_A"] if r in regs]
    S = pd.DataFrame(index=[sc.nice(m) for m in mets], columns=tgt, dtype=float)
    for _, r in SH[SH["from"] == "R_SOLVER_CONS"].iterrows():
        if r["to"] in tgt and r["metric"] in S.index:
            S.loc[r["metric"], r["to"]] = r["label_only_shift"]
    spec = {"type": "custom_two_panel_heatmap", "panel_a": {"title": "Common-set AUROC per label regime", "row_labels": [sc.nice(m) for m in mets],
            "col_labels": regs, "matrix": A.round(4).where(A.notna(), None).values.tolist()},
            "panel_b": {"title": "Label-only AUROC shift from R_SOLVER_CONS (same items, labels changed)", "row_labels": list(S.index),
                        "col_labels": tgt, "matrix": S.round(4).where(S.notna(), None).values.tolist(), "diverging_center": 0}}
    (fig_dir / "fig_regime_shift.json").write_text(json.dumps(spec, indent=1))
    cs = _style()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fig, axes = plt.subplots(1, 2, figsize=(13, 7.2), layout="constrained", gridspec_kw={"width_ratios": [len(regs), max(len(tgt), 1) + 0.6]})
        ax = axes[0]
        im = ax.imshow(A.values, cmap="viridis", vmin=0.45, vmax=0.95, aspect="auto")
        ax.set_xticks(range(len(regs)), labels=[re.sub(r"^R_", "", r).replace("_", " ") for r in regs], rotation=50, ha="right", fontsize=8)
        ax.set_yticks(range(len(mets)), labels=[sc.nice(m) for m in mets], fontsize=8)
        for i in range(A.shape[0]):
            for j in range(A.shape[1]):
                v = A.values[i, j]
                if not np.isnan(v):
                    ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=6.5, color="white" if v < 0.72 else "black")
        fig.colorbar(im, ax=ax, fraction=0.035, pad=0.02, label="AUROC (common set)")
        ax.set_title("a  Common-set AUROC by label regime", fontsize=10, loc="left")
        ax = axes[1]
        vmax = float(np.nanmax(np.abs(S.values))) if np.isfinite(np.nanmax(np.abs(S.values))) else 0.1
        im2 = ax.imshow(S.values.astype(float), cmap="RdBu_r", vmin=-vmax, vmax=vmax, aspect="auto")
        ax.set_xticks(range(len(tgt)), labels=[re.sub(r"^R_", "", t).replace("_", " ") + ("\n(0 label changes)" if t == "R_ADJ_A" and np.nanmax(np.abs(S[t].values.astype(float))) == 0 else "") for t in tgt], rotation=50, ha="right", fontsize=8)
        ax.set_yticks(range(len(S.index)), labels=list(S.index), fontsize=8)
        for i in range(S.shape[0]):
            for j in range(S.shape[1]):
                v = S.values[i, j]
                if not np.isnan(v):
                    ax.text(j, i, f"{v:+.2f}", ha="center", va="center", fontsize=6.5)
        fig.colorbar(im2, ax=ax, fraction=0.08, pad=0.02, label="label-only shift (AUROC)")
        ax.set_title("b  Label-only shift vs solver labels", fontsize=10, loc="left")
        fig.savefig(fig_dir / "fig_regime_shift.png", dpi=200)
        fig.savefig(fig_dir / "fig_regime_shift.pdf")
        plt.close(fig)


def fig_forest(OUT, fig_dir: Path):
    import matplotlib.pyplot as plt
    regs = [r for r in ["R_SOLVER_CONS", "R_ADJ_ALL", "R_ADJ_AB", "R_ADJ_A", "L_UNPARSEABLE_AS_ERROR", "H_CURATOR"] if r in OUT["common_items"]]
    show = ["p_fused_H", "c_score", "bow_uncarried", "l3_score", "S4_refit_oof", "PT_oof", "PTJ_oof", "sc5_cheap", "rt_nli_min", "judge_cheap_orig"]
    spec = {"type": "custom_forest_panels", "reference": "judge_cheap_disg", "panels": []}
    for rn in regs:
        tab = OUT["common_items"][rn]["table"]
        tab = tab[(tab.get("item_set", "COMMON") == "COMMON") & tab.col.isin(show)].set_index("col")
        rows = [(sc.nice(m), tab.loc[m, "delta_vs_judge"], tab.loc[m, "delta_ci_lo"], tab.loc[m, "delta_ci_hi"]) for m in show if m in tab.index]
        spec["panels"].append({"regime": rn, "testable": OUT["regimes"][rn]["common_set"]["testable"], "n": OUT["regimes"][rn]["common_set"]["n"],
                               "n_err": OUT["regimes"][rn]["common_set"]["n_err"],
                               "rows": [{"metric": a, "delta": num(b), "ci_lo": num(c), "ci_hi": num(d)} for a, b, c, d in rows]})
    (fig_dir / "fig_forest_common.json").write_text(json.dumps(spec, indent=1))
    cs = _style()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        n = len(spec["panels"])
        ncol = 3
        nrow = int(np.ceil(n / ncol))
        fig, axes = plt.subplots(nrow, ncol, figsize=(12.5, 3.6 * nrow), layout="constrained", sharex=True, squeeze=False)
        for k, p in enumerate(spec["panels"]):
            ax = axes[k // ncol][k % ncol]
            labels = [r["metric"] for r in p["rows"]]
            y = np.arange(len(labels))
            col = cs.PALETTE[0] if p["testable"] else "#9a9a9a"
            for i, r in enumerate(p["rows"]):
                if p["testable"] and r["ci_lo"] is not None:
                    ax.plot([r["ci_lo"], r["ci_hi"]], [i, i], color="#333333", lw=1.2)
                ax.plot(r["delta"], i, "o", color=col, ms=5)
            ax.axvline(0, color="#999999", ls="--", lw=1)
            ax.set_yticks(y, labels=labels, fontsize=8)
            ax.invert_yaxis()
            t = f"{p['regime']} (n={p['n']}, err={p['n_err']})" + ("" if p["testable"] else "\nuntestable: point estimate only")
            ax.set_title(t, fontsize=8.5, loc="left")
            ax.grid(axis="x", visible=True)
        for k in range(n, nrow * ncol):
            axes[k // ncol][k % ncol].axis("off")
        fig.supxlabel("ΔAUROC vs disguised cheap judge (95% sentence-cluster bootstrap CI; grey = untestable regime)", fontsize=9)
        fig.savefig(fig_dir / "fig_forest_common.png", dpi=200)
        fig.savefig(fig_dir / "fig_forest_common.pdf")
        plt.close(fig)


# ------------------------------------------------------------------------------------------------ datasets block
def build_examples(df, regimes, commons) -> list[dict]:
    ex = []
    oof_cols = {}
    for rn, (sub, y) in commons.items():
        for c in ("PT_oof", "PTJ_oof"):
            if c in sub.columns:
                oof_cols[(rn, c)] = sub[c].to_dict()
    score_cols = sc.HEADLINE_L + sc.SECONDARY_L + ["c_score_nonoai", "predset_instab_pool", "fol_length", "judge_strong_orig", "judge_strong_disg",
                                                   "judge_local_qwen8b_orig", "judge_local_qwen8b_disg", "judge_local_llama8b_orig",
                                                   "judge_local_llama8b_disg", "l3_score_disguised", "l3_score_llmformula"]
    for k, r in df.iterrows():
        labels = {rn: (int(reg["y"].loc[k]) if k in reg["y"].index else None) for rn, reg in regimes.items()}
        labels_txt = {rn: ("ERROR" if v == 1 else "CORRECT" if v == 0 else "not_in_regime") for rn, v in labels.items()}
        labels_txt["_raw"] = {"lab_A": r.lab_A, "lab_C": r.lab_C, "lab_D": r.lab_D, "E_final_label": r.E_final_label, "E_label_tier": r.E_label_tier}
        e = {"input": json.dumps({"text": r.text, "candidate_fol": r.candidate_fol}, ensure_ascii=False),
             "output": json.dumps(labels_txt, ensure_ascii=False),
             "metadata_item_id": k, "metadata_track": r.track, "metadata_system": r.system, "metadata_cluster": r.cluster,
             "metadata_E_label_tier": r.E_label_tier, "metadata_in_common_set": [rn for rn, (sub, _) in commons.items() if k in sub.index]}
        # shipped-threshold verdicts of the iteration-1 metrics (ERROR = flagged as unfaithful)
        for pname, col, rule in (("fused_H", "fused_flag", lambda v: v > 0.5), ("L2_bow", "bow_flag", lambda v: v > 0.5),
                                 ("L3", "l3_flag", lambda v: v > 0.5), ("c_score_medoid", "flag_medoid", lambda v: v > 0.5),
                                 ("judge_cheap_disg", "judge_cheap_disg", lambda v: v > 0.5), ("judge_cheap_orig", "judge_cheap_orig", lambda v: v > 0.5)):
            v = num(r[col]) if col in df.columns else None
            if v is not None:
                e[key("predict", pname)] = "ERROR" if rule(v) else "CORRECT"
        for c in score_cols:
            if c in df.columns:
                v = num(r[c])
                if v is not None:
                    e[key("eval", c)] = v
        for (rn, c), d in oof_cols.items():
            if k in d:
                v = num(d[k])
                if v is not None:
                    e[key("eval", c, rn)] = v
        ex.append(e)
    return ex


def write_all(OUT, df, regimes, commons, metrics_by_regime, decl, ws: Path, sources: dict):
    fig_dir = ws / "figures"
    OUT["VERDICT"] = build_verdict(OUT)
    try:
        fig_regime_shift(OUT, fig_dir)
        fig_forest(OUT, fig_dir)
        OUT["figures"] = {"fig_regime_shift": "figures/fig_regime_shift.{json,png,pdf}", "fig_forest_common": "figures/fig_forest_common.{json,png,pdf}"}
    except (ImportError, ValueError, KeyError, TypeError) as ex:
        logger.error(f"figure rendering failed: {ex}")
        OUT["figures"] = {"error": str(ex)}
    OUT["tables_index"] = sources
    agg = build_metrics_agg(OUT)
    meta = {k: v for k, v in OUT.items() if k not in ("metrics_agg",)}
    doc = {"metadata": jsafe(meta), "metrics_agg": agg,
           "datasets": [{"dataset": "folio_dev_logiclm_screen_trackL_trackH", "examples": build_examples(df, regimes, commons)}]}
    p = ws / "eval_out.json"
    p.write_text(json.dumps(jsafe(doc), ensure_ascii=False, indent=1))
    logger.info(f"wrote {p} ({p.stat().st_size / 1e6:.1f} MB); metrics_agg keys={len(agg)}; examples={len(doc['datasets'][0]['examples'])}")
