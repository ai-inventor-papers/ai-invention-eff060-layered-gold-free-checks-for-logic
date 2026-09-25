"""method_out.json in the exp_gen_sol_out schema (datasets: screen_track_L, screen_track_H, href_calibration)."""
from __future__ import annotations

import json
from pathlib import Path


def _s(x) -> str:
    if x is None:
        return "NA"
    if isinstance(x, float):
        return f"{x:.6f}"
    return str(x)


def example(s: dict) -> dict:
    l3 = s.get("l3") or {}
    ex = {
        "input": f"TEXT: {s['text']}\nFOL: {s['candidate_fol']}",
        "output": s["label"],
        "predict_fol_triage": _s(s.get("p_fused_H") if s["track"] != "H" else s.get("p_fused_H_oof")),
        "predict_fol_triage_fired_layer": _s(s.get("fired_layer")),
        "predict_l1_lint": _s(s.get("l1_any")),
        "predict_l2_bow": _s((s.get("bow_n_unanch") or 0) + (s.get("bow_uncarried") or 0.0) if s.get("parse_ok") else None),
        "predict_l2_role": _s(s.get("role_count")),
        "predict_l3_score": _s(s.get("l3_score") if s.get("l3_ok") else None),
        "predict_cascade_llmformula": _s(s.get("p_cascade_llmformula")),
        "metadata_item_id": s["item_id"],
        "metadata_track": s["track"],
        "metadata_system": s["system"],
        "metadata_role": s["role"],
        "metadata_strata": s["strata"],
        "metadata_l1_codes": s.get("l1_codes"),
        "metadata_l2_bow": {"uncarried_frac": s.get("bow_uncarried"), "n_unanchored": s.get("bow_n_unanch"),
                            "unanchored": s.get("bow_unanchored"), "flag": s.get("bow_flag")},
        "metadata_l2_role": {"count": s.get("role_count"), "codes": s.get("role_codes"), "flag": s.get("role_flag")},
        "metadata_l3_mismatch_fields": {k: l3.get(k) for k in ("mm_role", "mm_force", "mm_claims", "mm_order",
                                                               "mm_exception", "missing_frac", "extra_frac")} if l3 else None,
        "metadata_error_code": s.get("error_code"),
        "metadata_p_fused_Hall": s.get("p_fused_Hall"),
        "metadata_fused_flag": s.get("fused_flag"),
        "metadata_cost_usd": s.get("cost_usd_l3"),
        "metadata_seconds": {"cpu": s.get("secs_cpu"), "l3": s.get("secs_l3")},
        "metadata_coverage_status": s.get("coverage_status"),
        "metadata_auto_class": s.get("auto_class"),
        "metadata_repair_ops": s.get("repair_ops"),
        "metadata_ambiguous": s.get("ambiguous"),
    }
    return ex


def write_method_out(root: Path, res_dir: Path, scored: list[dict], M: dict):
    ds = []
    for name, tr in (("screen_track_L", "L"), ("screen_track_H", "H"), ("href_calibration", "HREF")):
        exs = [example(s) for s in scored if s["track"] == tr]
        if exs:
            ds.append({"dataset": name, "examples": exs})
    pre = json.loads(((res_dir / "prereg.json") if (res_dir / "prereg.json").exists() else (root / "prereg.json")).read_text())
    headline = {}
    for k, ev in M["evaluations"].items():
        headline[k] = {n: {"AUROC": v["AUROC"], "CI95": v["AUROC_CI95_cluster"], "AUPRC": v["AUPRC"], "n": v["n_scored"]}
                       for n, v in ev["scores"].items()}
        headline[k]["_n_pos"] = ev["n_pos"]; headline[k]["_n"] = ev["n"]
    not_run = json.loads((res_dir / "not_run.json").read_text()) if (res_dir / "not_run.json").exists() else []
    out = {
        "metadata": {
            "method_name": "FOL-Triage (L1 text-free lint -> L2 bag-of-words / role-aware accounting -> L3 text-only "
                           "role questionnaire answered exactly by z3 on the formula side; fused logistic fitted on track H)",
            "baselines_inside_artifact": ["L2 bag-of-words content accounting (iter-3)", "each single layer",
                                          "decomposed judge: same LLM reads the formula instead of z3 (cascade_llmformula)",
                                          "within-L cross-fitted fusion (secondary)"],
            "baselines_elsewhere": "LLM judge / round-trip / self-consistency / structural pilot metrics live in sibling "
                                   "experiments C and D on the same item_ids; ΔAUROC vs the disguised judge is computed "
                                   "in iteration 2",
            "primary_model": pre["L3_model_primary"], "prereg_timestamp": pre["timestamp_utc"],
            "headline_AUROC": headline,
            "gates_fused_primary": M["gates_fused_primary"],
            "metrics_file": "results/metrics.json",
            "per_item_file": "results/per_item.jsonl",
            "not_run": not_run,
            "metrics": M,
        },
        "datasets": ds,
    }
    ((res_dir / "method_out.json") if res_dir.name == "results_dry" else (root / "method_out.json")).write_text(json.dumps(out, ensure_ascii=False, indent=1, default=str))
