#!/usr/bin/env python3
"""STEP 5d PREREG_PERTURB FREEZE, written before ANY PERTURB label-based statistic (perturb labels / operators are never read
here). PRIMARY threshold of every metric = matched FA 0.10 (fractional ties) on E R_AB LLM CORRECT rows:
  consensus / l2_bow / l3_z3 / p_peer_text / p_text : dataset-E rows (frozen exp 5 columns; HYB re-derived), exp 5 imputation
  parse_fail / pilot_* / sc5_local_*                 : exp 6 E_baseline_features (fail -> fail_fill)
  S4_local                                           : results/s4_perturb_coefs.json (in-sample E fit)
  judge_cheap_disg                                   : E calibration rows EC: (flash-lite, this artifact) -- CORRECT rows
  GPU metrics (nf4 local judges, round trip)         : SAME rule on the EC: CORRECT rows once scored (rule frozen here, values
                                                       added to results/thresholds_gpu.json by analyse_perturb before any
                                                       PERTURB statistic; EC keys sha256 recorded below)
Writes results/prereg_perturb.json + .sha256.
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import an_common as C  # noqa: E402
import fit_s4_perturb as S4  # noqa: E402
import stats as ST  # noqa: E402

CONS = ["c_align", "c_nf", "c_hyb", "g_align", "g_nf", "g_hyb"]
E_COLS = CONS + ["l2_bow", "l3_z3", "p_peer_text", "p_text"]
E6_COLS = ["parse_fail", "pilot_joint_conflict", "pilot_arity_incons", "pilot_shape_incons", "pilot_dangling",
           "sc5_local_eq_frac", "sc5_local_entropy"]
GPU_COLS = ["judge_local_qwen8b_disg", "judge_local_llama8b_disg", "rt_nli_min_local", "rt_nli_fwd_local", "rt_nli_bwd_local",
            "rt_nli_contra_local", "rt_nli_min_alt_local", "rt_embed_cos_local"]


def main():
    out = C.RES / "prereg_perturb.json"
    assert not out.exists(), "prereg_perturb.json already frozen"
    C.guard()
    for p in C.RES.glob("perturb_sensitivity*"):
        raise SystemExit(f"PERTURB statistic exists before the freeze: {p}")
    thr, info = {}, {}
    rows = C.load_E()
    neg = [r for r in rows if r["y_AB"] == 0]
    for m in E_COLS:
        v = [r[m] for r in neg]
        thr[m] = ST.matched_fa(v, 0.10)
        info[m] = {"source": "dataset E R_AB LLM CORRECT (exp 5 columns / HYB re-derived)", "n_neg": len(v),
                   "tie_share_at_t": ST.tie_share_at(v, thr[m][0])}
    lab = {r["row_key"]: r for r in rows}
    feat = S4.e6_features()
    meta = json.loads((S4.E6 / "results" / "feature_meta.json").read_text())
    for m in E6_COLS:
        v = []
        for k, r in feat.items():
            if lab[k]["y_AB"] != 0:
                continue
            if r.get(m + "__status") == "fail":
                v.append(meta["fail_fill"].get(m, 1.0))
            elif r.get(m) is not None:
                v.append(r[m])
        thr[m] = ST.matched_fa(v, 0.10)
        info[m] = {"source": "exp 6 E_baseline_features, R_AB LLM CORRECT", "n_neg": len(v), "tie_share_at_t": ST.tie_share_at(v, thr[m][0])}
    s4 = json.loads((C.RES / "s4_perturb_coefs.json").read_text())
    thr["S4_local"] = (s4["threshold_FA0.10_E_RAB_correct"]["t"], s4["threshold_FA0.10_E_RAB_correct"]["lambda"])
    info["S4_local"] = {"source": "s4_perturb_coefs.json in-sample E R_AB CORRECT", "n_neg": s4["n_train"] - s4["n_error"]}
    cal = C.jl(C.DATA / "E_calib_units.jsonl")
    calC = {c["key"] for c in cal if c["label"] == "CORRECT"}
    jc = {r["key"]: r for r in C.jl(C.RES / "perturb_scores" / "judge_cheap_disg.jsonl")}
    v = [1.0 - jc[k]["p"] if jc.get(k, {}).get("p") is not None else 1.0 for k in sorted(calC)]
    thr["judge_cheap_disg"] = ST.matched_fa(v, 0.10)
    info["judge_cheap_disg"] = {"source": "EC CORRECT rows (flash-lite, rubric A, exp-D disguise as in exp 6); failure -> 1.0",
                                "n_neg": len(v), "tie_share_at_t": ST.tie_share_at(v, thr["judge_cheap_disg"][0]),
                                "n_fail": sum(1 for k in calC if jc.get(k, {}).get("p") is None)}
    sa = json.loads((C.RES / "analysis_hyb.json").read_text())["screen"]["thresholds"]
    pre = {
        "title": "PREREG_PERTURB (iteration 3, T5): per-error-type sensitivity on the synthetic PERTURB suite",
        "timestamp_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "prereg_hyb_sha256": C.sha256_file(C.RES / "prereg_hyb.json"),
        "orientation": "higher = more likely ERROR for every metric; judges 1 - faithful_prob / 1 - P(YES); round trip 1 - entail / 1 - cos; contra as is; sc5 1 - eq_frac",
        "rows": "4,234 PERTURB mutants (ERROR) + 868 PERTURB_CONTROL (CORRECT) + 300 unmutated bases (CORRECT, control type BASE); consensus scored only on the 200 E bases (R_COMP bases: NA, no peers yet; rcomp_candidates.jsonl absent at run time)",
        "thresholds_primary": {m: {"t": t[0], "lambda": t[1], **info.get(m, {})} for m, t in thr.items()},
        "thresholds_gpu_rule": {"metrics": GPU_COLS, "rule": "matched FA 0.10 with fractional ties on the nf4 scores of the EC: CORRECT rows (failure -> fail_fill 1.0)",
                                "ec_correct_keys_sha256": hashlib.sha256("\n".join(sorted(calC)).encode()).hexdigest(), "n": len(calC)},
        "thresholds_consensus_screen_secondary": sa,
        "threshold_secondary": "FA 0.10 on PERTURB non-rename controls (CONTRAPOSITIVE, REORDER_*, DEMORGAN) + BASE, in-sample, labelled as such",
        "statistics": {
            "recall": "tie-aware recall at the PRIMARY threshold per operator x polarity, base-clustered bootstrap CI (B=2000, seed 0)",
            "base_matched_auroc": "within-base AUROC of the operator's mutants vs the same base's non-rename controls + BASE, averaged over bases with both (primary), and pooled AUROC over those bases",
            "down_vs_up": "on complete matched pairs: mean(flag_DOWN - flag_UP) (tie-aware), base-clustered bootstrap CI, McNemar discordant counts at hard flags (score > t), plus mean paired score difference",
            "breakdowns": ["base reference_status (TRUSTED_AGREED / GOLD_PANEL_OK / PANEL_REPAIRED / R_COMP)", "base endorsement: base c_hyb < 1 (>=1 peer agrees) vs not"],
            "tradeoff": "per metric: (RENAME_SYN FA, MEANING_RENAME recall) and (RENAME_NONCE FA, MEANING_RENAME recall)",
            "add_split": "ADD by subtype ADD_FOREIGN vs ADD_INTERNAL",
            "testability": "cells with < 30 rows after unscorable exclusion: point estimates only, 'untestable'; MOVE (6 rows) reported, not analysed; SCOPE/UNGLUE absent (0 rows)",
            "never_pooled": "PERTURB is never pooled with the real-error E AUROC"},
        "predictions": {"consensus_polarity_symmetric": "equivalence-based consensus (c_*) is polarity-symmetric: |mean(flag_DOWN - flag_UP)| < 0.05",
                        "surface_metrics_miss_DOWN": "lexical (l2_bow), NLI round-trip and judge metrics may miss DOWN (restrictor-side) edits more often (flag_DOWN - flag_UP < 0)"},
        "typing_operator_map": {"repair ops -> PERTURB operator": {"NEG": "NEG", "REV": "REV", "QUANT": "QUANT", "RESTR": "RESTR", "CONN": "CONN",
                                                                   "MOVE": "MOVE", "DROP": "ADD", "ADD": "DROP", "SWAP": "SWAP", "BIND": "BIND",
                                                                   "SCOPE": "SCOPE", "UNGLUE": "UNGLUE", "RENAME": "MEANING_RENAME"},
                                "note": "a repair maps the MUTANT back to the reference: a mutant made by ADD (extra conjunct) is repaired by a DROP op and vice versa; ADD_INTERNAL -> ADD for scoring (fine label also reported); a repair not found -> 'unrepairable'; MEANING_RENAME has no repair op in the search vocabulary except predicate substitution -> reported as uncodable when no op maps"},
        "deviations_at_freeze": ["D-GPU16: 16 GB GPU -> local 8B judges and verbaliser run nf4; thresholds for them from nf4 E calibration rows",
                                 "D-S4FULL: S4_local one full-E fit; PERTURB inputs nf4",
                                 "D-JUDGE-E: flash-lite E threshold from 864 EC CORRECT rows scored here (frozen E judge_cheap_disg covers too few rows)"],
    }
    out.write_text(json.dumps(pre, indent=1))
    (C.RES / "prereg_perturb.sha256").write_text(f"{C.sha256_file(out)}  prereg_perturb.json  {pre['timestamp_utc']}\n")
    print(json.dumps({m: (round(t[0], 4), round(t[1], 3)) for m, t in thr.items()}))


if __name__ == "__main__":
    main()
