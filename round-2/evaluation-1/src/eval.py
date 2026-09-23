#!/usr/bin/env python3
"""Zero-LLM-spend re-analysis of the iteration-1 artifacts (exp A FOL-Triage, exp C consensus, exp D judges/baselines,
dataset E screen adjudication) under every label regime. See README.md for the step list and outputs.

Run:  .venv/bin/python eval.py            (all steps, ~10-20 min on 4 CPUs)
      .venv/bin/python eval.py --quick    (B=200 bootstrap, 1 fold seed; smoke test)
"""
from __future__ import annotations

import argparse
import gc
import json
import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger

WS = Path(__file__).resolve().parent
sys.path.insert(0, str(WS / "src"))

import load  # noqa: E402
import stats_utils as su  # noqa: E402
import steps_core as sc  # noqa: E402
import steps_models as sm  # noqa: E402

TAB = WS / "tables"
FIG = WS / "figures"
LOGS = WS / "logs"
for d in (TAB, FIG, LOGS, WS / "data"):
    d.mkdir(exist_ok=True)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(LOGS / "eval.log", rotation="30 MB", level="DEBUG")

# all-NaN feature columns inside a CV fold and single-class bootstrap resamples raise RuntimeWarnings that the code
# already handles (mean -> 0, resample -> NaN and counted as skipped)
warnings.filterwarnings("ignore", category=RuntimeWarning)

SOURCES = {}


def out_tab(t: pd.DataFrame, name: str, src: str) -> None:
    """Write a CSV whose first line is a comment naming its source files."""
    p = TAB / name
    with open(p, "w") as f:
        f.write(f"# source: {src}\n")
        t.to_csv(f, index=False)
    SOURCES[name] = src
    logger.debug(f"wrote {p} ({len(t)} rows)")


def jsafe(o):
    """Recursively convert numpy/pandas objects and NaN to JSON-safe values."""
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


# ================================================================================================= STEP 0
def step0() -> dict:
    prov = {str(p): load.sha256(p) for p in load.INPUT_FILES}
    missing = [p for p, h in prov.items() if h is None]
    fw = {"heldout_candidates_loaded": False, "heldout_sentences_loaded": False,
          "groups_read_from_full_data_out": ["panel_calibration (saved to data/panel_calibration.json)"],
          "screen_audit_source": "screen_adjudicated_labels.json (identical rows to the screen_audit group)",
          "E_side_numbers": "transcribed from dataset_card.md, never recomputed from held-out rows",
          "openrouter_spend_usd": 0.0}
    pc = WS / "data/panel_calibration.json"
    if not pc.exists():
        d = json.loads((load.DS_E / "full_data_out.json").read_text())
        keep = [g for g in d["datasets"] if g["dataset"] == "panel_calibration"][0]["examples"]
        del d
        gc.collect()
        pc.write_text(json.dumps(keep))
        fw["note"] = "full_data_out.json parsed once; every group except panel_calibration deleted from memory immediately"
    else:
        fw["note"] = "panel_calibration group was extracted earlier (full_data_out.json parsed once, other groups deleted immediately)"
    logger.info(f"step0: hashed {len(prov)} inputs ({len(missing)} missing); firewall respected (held-out rows never loaded)")
    return {"provenance_sha256": prov, "missing_inputs": missing, "firewall": fw}


def shipped_rule_inputs(df: pd.DataFrame) -> dict:
    mA = json.loads((load.EXP_A / "results/metrics.json").read_text())
    g = mA["gates_fused_primary"]
    smC = json.loads((load.EXP_C / "results/summary.json").read_text())
    covC = smC["coverage"]["coverage_status_counts"]
    nL = sum(v for k, v in covC.items() if k.startswith("L|"))
    fams = {k: v for k, v in smC["rewrite_invariance"].items() if isinstance(v, dict) and "false_alarm_rate" in v}
    worst = max(fams.items(), key=lambda kv: kv[1]["false_alarm_rate"] or 0)
    return {
        "p_fused_H": {"coverage": g["coverage>=0.90"]["value"], "cost": g["cost<=0.002/item"]["value"],
                      "max_rewrite_fa": g["rewrite_FA<=0.10_per_family"]["worst_family_FA"],
                      "source": "exp A results/metrics.json gates_fused_primary"},
        "c_score": {"coverage": covC["L|ok"] / nL, "cost": smC["cost"]["C_story_amortised_per_sentence_usd"],
                    "max_rewrite_fa": worst[1]["false_alarm_rate"], "worst_family": worst[0],
                    "source": "exp C results/summary.json coverage.coverage_status_counts, cost.C_story_amortised_per_sentence_usd, rewrite_invariance"},
    }


# ================================================================================================= main
@logger.catch(reraise=True)
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true")
    args = ap.parse_args()
    B = 200 if args.quick else 2000
    n_seeds = 1 if args.quick else 5
    t0 = time.time()
    OUT = {"metadata": {"evaluation_name": "iter1_relabel_audit", "created": time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "bootstrap": {"resamples": B, "seed": 0, "cluster": "exp D norm(text)", "ci": "percentile 95%"},
                        "orientation": "every score oriented so that higher = more likely ERROR",
                        "scope_note": ("SCREEN = FOLIO-dev Logic-LM outputs of gpt-3.5 / gpt-4 / davinci-003 (2023), short sentences; "
                                       "every P1/P2/PEER+TEXT number is SCREEN PREVIEW, not confirmation. Regimes are the screen's "
                                       "own labels only (solver vs strict panel); no family-disjoint reference-aware adjudicator (R_ADJ) "
                                       "or composed-long regime (R_COMP) exists yet, so 'robust across regimes' means robust across "
                                       "solver vs strict-panel labels only.")}}
    s0 = step0()
    OUT["provenance"] = s0
    raw = load.load_all()
    df = load.build_master(raw)
    d_folds = raw["folds"]
    d_thr = json.loads((load.EXP_D / "results/analysis.json").read_text())["thresholds"]

    # ---- step 1 + 2
    OUT["bookkeeping"] = sc.step1_bookkeeping(df, raw, out_tab)
    r2 = sc.step2_rederive(df, out_tab)
    OUT["rederivation"] = r2
    if not r2["gate_passed"]:
        logger.error(f"re-derivation gate FAILED: {r2['mismatch_diagnoses']}")
        raise SystemExit("step 2 gate failed; fix before continuing")
    logger.info(f"t={time.time() - t0:.0f}s step2 gate passed")

    # ---- step 3: declare regimes before any further AUROC
    regimes = sc.step3_regimes(df)
    commons, metrics_by_regime, decl = {}, {}, {}
    for rn, reg in regimes.items():
        base = sc.HEADLINE_L if reg["track"] == "L" else sc.HEADLINE_H
        sub, y, mets, dropped = sc.common_set(df, reg, base)
        commons[rn] = (sub, y)
        metrics_by_regime[rn] = mets
        decl[rn] = {"track": reg["track"], "description": reg["desc"], "n_regime_items": int(len(reg["y"])),
                    "n_regime_err": int(reg["y"].sum()), "common_set": sc.testability(sub, y),
                    "headline_metrics": mets, "metrics_dropped_low_coverage": dropped,
                    "untestable_rule": "TESTABLE = >=50 ERROR and >=50 CORRECT and >=25 sentences each side; untestable -> sign-only"}
    (WS / "regimes.json").write_text(json.dumps(jsafe(decl), indent=1))
    OUT["regimes"] = decl
    logger.info("step3 regimes: " + "; ".join(f"{k}: n={v['common_set']['n']} err={v['common_set']['n_err']} T={v['common_set']['testable']}" for k, v in decl.items()))

    # ---- step 6 (needed by step 4 tables): PEER+TEXT preview per regime
    ptp = {}
    for rn in regimes:
        sub, y = commons[rn]
        if y.sum() < 5 or (1 - y).sum() < 5:
            ptp[rn] = {"skipped": "fewer than 5 items in a class"}
            for mname in sm.MODELS:
                sub[mname] = np.nan
            continue
        ptp[rn] = sm.step6_regime(sub, y, d_folds, n_seeds=n_seeds)
        ptp[rn]["testable"] = decl[rn]["common_set"]["testable"]
        logger.info(f"step6 {rn}: PT={ptp[rn]['models']['PT_oof']['oof_auroc_seed0_Dfolds']:.3f} PTJ={ptp[rn]['models']['PTJ_oof']['oof_auroc_seed0_Dfolds']:.3f} "
                    f"S4refit={ptp[rn]['models']['S4_refit_oof']['oof_auroc_seed0_Dfolds']:.3f} dPT-judge={ptp[rn]['delta_PT_oof_vs_judge_cheap_disg']['delta']:+.3f}")
    ptp["F3_preview"] = sm.f3_preview(df, regimes, commons, d_folds)
    OUT["SCREEN_PREVIEW_NOT_CONFIRMATION_peer_text_preview"] = ptp
    logger.info(f"t={time.time() - t0:.0f}s step6 done")

    # ---- step 4: common-item tables + rule verdicts + available-case + frontier
    shipped = shipped_rule_inputs(df)
    OUT["rule_inputs_shipped"] = shipped
    common_out, verdicts, boots_by_regime = {}, {}, {}
    extra = ["PT_oof", "PTJ_oof", "PTg_oof", "S4_refit_oof", "S4PT_oof"]
    for rn in regimes:
        sub, y = commons[rn]
        if y.sum() < 5 or (1 - y).sum() < 5:
            continue
        mets = metrics_by_regime[rn] + [m for m in extra if m in sub.columns]
        tab, aux = sc.eval_table(sub, y, mets, d_thr, B=B)
        tab.insert(0, "regime", rn)
        tab["testable"] = decl[rn]["common_set"]["testable"]
        # SUBSET block: label-conditional / sparse metrics on (common set AND non-null), judge re-scored on the same items
        sec = sc.SECONDARY_L if regimes[rn]["track"] == "L" else sc.SECONDARY_H
        for m2 in sec:
            ok = sub[m2].notna().values
            if ok.sum() < 20 or len(np.unique(y[ok])) < 2:
                continue
            t2, _ = sc.eval_table(sub[ok], y[ok], [m2, sc.REF], d_thr, holm_family=[], B=B)
            t2 = t2[t2.col == m2].copy()
            t2.insert(0, "regime", rn)
            t2["item_set"] = f"SUBSET common AND {m2} non-null"
            tab = pd.concat([tab, t2], ignore_index=True)
        tab["item_set"] = tab["item_set"].fillna("COMMON") if "item_set" in tab.columns else "COMMON"
        out_tab(tab, f"common_items_{rn}.csv", f"common-item set of {rn} (all headline metrics non-null); A per_item.jsonl, C analysis_table.jsonl, D per_item_scores.jsonl oriented_scores, E screen_adjudicated_labels.json")
        common_out[rn] = {"n": len(y), "n_err": int(y.sum()), "n_sentences": int(sub.cluster.nunique()), "testable": decl[rn]["common_set"]["testable"],
                          "n_boot_skipped_single_class": aux["n_skipped_single_class"], "table": tab}
        boots_by_regime[rn] = aux["boots"]
        if rn.startswith("R_") or rn == "L_UNPARSEABLE_AS_ERROR":
            verdicts[rn] = {c: sc.rule_verdict(tab, c, shipped, decl[rn]["common_set"]["testable"]) for c in ("p_fused_H", "c_score") if c in tab.col.values}
        else:
            verdicts[rn] = {c: sc.rule_verdict(tab, c, {**shipped}, decl[rn]["common_set"]["testable"]) for c in ("c_score",) if c in tab.col.values}
        # available-case table
        reg = regimes[rn]
        rows = []
        all_sub = df.loc[reg["y"].index]
        yy_all = reg["y"].values.astype(int)
        for m in metrics_by_regime[rn]:
            ok = all_sub[m].notna().values
            if ok.sum() < 10 or len(np.unique(yy_all[ok])) < 2:
                continue
            s_ = all_sub[m].values[ok].astype(float)
            cbm = su.ClusterBoot(list(all_sub.cluster.values[ok]), B=min(B, 1000))
            ci = su.ci95(su.boot_auc_w(yy_all[ok], s_, cbm.item_W()))
            rows.append({"regime": rn, "metric": sc.nice(m), "n": int(ok.sum()), "n_err": int(yy_all[ok].sum()),
                         "auroc": su.auroc(yy_all[ok], s_), "ci_lo": ci[0], "ci_hi": ci[1], "coverage_in_regime": float(ok.mean())})
        out_tab(pd.DataFrame(rows), f"available_case_{rn}.csv", "each metric on its own non-null items within the regime (secondary; NOT same-item)")
        # frontier same-item table
        frows = []
        for strong, cheap in [("judge_strong_orig", "judge_cheap_orig"), ("judge_strong_disg", "judge_cheap_disg"),
                              ("judge_strong_orig", "judge_cheap_disg"), ("judge_strong_disg", "judge_cheap_orig")]:
            fs = all_sub[all_sub[strong].notna() & all_sub[cheap].notna()]
            yf = reg["y"].loc[fs.index].values.astype(int)
            if len(fs) < 20 or yf.sum() < 3 or (1 - yf).sum() < 3:
                continue
            cbf = su.ClusterBoot(list(fs.cluster.values), B=B)
            Wf = cbf.item_W()
            d = su.boot_auc_w(yf, fs[strong].values, Wf) - su.boot_auc_w(yf, fs[cheap].values, Wf)
            frows.append({"regime": rn, "strong": strong, "cheap": cheap, "n": len(fs), "n_err": int(yf.sum()),
                          "auroc_strong": su.auroc(yf, fs[strong].values), "auroc_cheap": su.auroc(yf, fs[cheap].values),
                          "delta": su.auroc(yf, fs[strong].values) - su.auroc(yf, fs[cheap].values), "ci": su.ci95(d),
                          "p_boot": su.boot_p_two_sided(d), "delong_p": su.delong_paired(yf, fs[strong].values, fs[cheap].values)["p"]})
        common_out[rn]["frontier_same_item"] = frows
    fr_all = pd.DataFrame([r for v in common_out.values() for r in v.get("frontier_same_item", [])])
    out_tab(fr_all, "frontier_same_item.csv", "exp D judge_strong_* subset (200L/96H) intersected with each regime")
    OUT["common_items"] = common_out
    OUT["rule_verdicts"] = verdicts
    logger.info(f"t={time.time() - t0:.0f}s step4 done")

    # ---- step 5: regime-shift matrix, tau, flipped items
    r5 = sc.step5_regime_shift(df, regimes, commons, metrics_by_regime, out_tab, B_tau=100 if args.quick else 500)
    flip = sc.flipped_diagnostic(df, commons, regimes, ["p_fused_H", "bow_uncarried", "l3_score", "c_score", "c_score_peers6", "medoid_depth",
                                                         "cluster_entropy", "sc5_cheap", "judge_cheap_disg", "judge_cheap_orig",
                                                         "rt_nli_min", "best_baseline_oof"], out_tab)
    OUT["regime_shift"] = {"auroc_matrix": r5["matrix"].reset_index().to_dict(orient="records"), "label_only_shift": r5["shift"],
                           "kendall_tau": r5["tau"], "tau_metrics": r5["tau_metrics"], "flipped_item_diagnostic": flip}
    logger.info(f"t={time.time() - t0:.0f}s step5 done")

    # ---- step 7: P1/P2
    p = {"C_endorsement_reproduction": sm.reproduce_c_endorsement(df)}
    for rn, adj in [("R_SOLVER_CONS", False), ("R_ADJ_AB", True), ("R_ADJ_ALL", True)]:
        sub, y = commons[rn]
        r7 = sm.step7_regime(sub, y, adj, ["c_score", "bow_uncarried", "l3_score", "judge_cheap_disg", "judge_cheap_orig", "PT_oof", "PTJ_oof"], B=B)
        out_tab(r7["recall_table"], f"p1_crossover_{rn}.csv", f"matched-FA interpolated recall per error type, common set of {rn}")
        out_tab(r7["diff_table"], f"p1_diff_{rn}.csv", f"c_score minus text recall differences at matched FA, {rn}")
        p[rn] = {"P1": r7["P1"], "P2": r7["P2"], "testable": decl[rn]["common_set"]["testable"]}
        logger.info(f"step7 {rn}: P1 {[(k, v['verdict']) for k, v in r7['P1'].items()]} P2a {r7['P2']['P2a_verdict']} P2b {r7['P2']['P2b_verdict']}")
    p2rows = []
    for rn in ("R_SOLVER_CONS", "R_ADJ_AB", "R_ADJ_ALL"):
        for k, v in p[rn]["P2"].items():
            if k.startswith("spearman"):
                p2rows.append({"regime": rn, "quantity": k, "value": v["rho"], "ci_lo": v["ci"][0], "ci_hi": v["ci"][1], "n": v["n"]})
        for k, v in p[rn]["P2"]["decomposition"].items():
            for kk, vv in v.items():
                if isinstance(vv, (int, float)) or vv is None:
                    p2rows.append({"regime": rn, "quantity": f"{k}.{kk}", "value": vv, "ci_lo": None, "ci_hi": None, "n": None})
                elif isinstance(vv, list) and len(vv) == 2:
                    p2rows.append({"regime": rn, "quantity": f"{k}.{kk}", "value": None, "ci_lo": vv[0], "ci_hi": vv[1], "n": None})
    out_tab(pd.DataFrame(p2rows), "p2.csv", "P2 Spearman among errors/correct + exact placement-value decomposition of the PT gain")
    OUT["SCREEN_PREVIEW_NOT_CONFIRMATION_P1_P2"] = p
    logger.info(f"t={time.time() - t0:.0f}s step7 done")

    # ---- steps 8-13 + outputs
    import steps_audit as sa  # noqa: E402
    sa.run_all(OUT, df, raw, regimes, commons, metrics_by_regime, decl, out_tab, B=B, ws=WS, quick=args.quick)
    import outputs  # noqa: E402
    outputs.write_all(OUT, df, regimes, commons, metrics_by_regime, decl, ws=WS, sources=SOURCES)
    logger.info(f"DONE in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
