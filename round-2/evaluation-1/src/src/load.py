"""Load and join the iteration-1 per-item files (exp A, C, D and dataset E's screen audit) into one master frame.

All inputs are READ-ONLY. Dataset E: only screen_adjudicated_labels.json (the screen audit) is read here; the held-out
candidate group of full_data_out.json is never loaded (see eval.py::step0_firewall).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger

from stats_utils import norm

IT1 = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1")
GA = IT1 / "gen_art"
EXP_A = GA / "gen_art_experiment_1"
EXP_C = GA / "gen_art_experiment_3"
EXP_D = GA / "gen_art_experiment_4"
DS_E = GA / "gen_art_dataset_1"
AUDIT = IT1 / "review_report" / "review_report" / "audit"

INPUT_FILES = [
    EXP_A / "screen_items.json", EXP_A / "results/per_item.jsonl", EXP_A / "results/metrics.json",
    EXP_A / "results/RESULTS.md", EXP_A / "README.md", EXP_A / "prereg.json", EXP_A / "invariance_set.json",
    EXP_A / "results/invariance_scores.json", EXP_A / "results/ablations.json", EXP_A / "results/calibration.json",
    EXP_A / "results/role_href_calibration.json", EXP_A / "results/audit_rederive.json", EXP_A / "src/fol_triage.py",
    EXP_A / "src/repair_census.py",
    EXP_C / "results/analysis_table.jsonl", EXP_C / "results/summary.json", EXP_C / "results/consensus.json",
    EXP_C / "results/screen_report.json", EXP_C / "results/screen_items.json", EXP_C / "results/prereg.json",
    EXP_C / "results/screen_label_hash.txt", EXP_C / "src/analysis.py", EXP_C / "src/common.py",
    EXP_C / "src/consensus.py", EXP_C / "src/repair_census.py",
    EXP_D / "results/per_item_scores.jsonl", EXP_D / "results/analysis.json", EXP_D / "results/summary.md",
    EXP_D / "results/rewrite_scores.jsonl", EXP_D / "results/rewrite_stats.json", EXP_D / "results/disguise_stats.json",
    EXP_D / "results/audit_headlines.json", EXP_D / "results/costs.jsonl", EXP_D / "data/folds.json",
    EXP_D / "data/screen_items.json", EXP_D / "data/invariance_items.json", EXP_D / "data/label_vector.sha1",
    EXP_D / "prereg.json", EXP_D / "src/common.py", EXP_D / "src/analysis.py",
    DS_E / "screen_adjudicated_labels.json", DS_E / "dataset_card.md", DS_E / "full_data_out.json",
    AUDIT / "join_audit.py", AUDIT / "join_audit.json", AUDIT / "paired_boot.py", AUDIT / "paired_boot.json",
    AUDIT / "rescore_adjudicated.py", AUDIT / "rescore_adjudicated.json",
]

A_SCORES = ["p_fused_H", "p_fused_Hall", "p_fused_Lcf", "bow_uncarried", "l3_score", "n_smells", "role_count", "l1_any",
            "l3_score_llmformula", "l3_score_disguised", "l3_score_local", "l3_score_exact"]
C_SCORES = ["c_score", "c_score_peers6", "c_score_nonoai", "c_score_llm2", "medoid_depth", "cluster_entropy", "sc5_cheap",
            "sc5_same", "predset_instab_pool", "fol_length", "misalign"]
D_EXTRA = ["best_baseline_oof", "baseline_combo_S1_structural_oof", "baseline_combo_S2_roundtrip_oof",
           "baseline_combo_S3_judges_disg_oof", "baseline_combo_S4_all_cheap_oof"]


def sha256(p: Path) -> str | None:
    if not p.exists():
        return None
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def rj(p: Path) -> list[dict]:
    return [json.loads(l) for l in open(p) if l.strip()]


def _f(v):
    if v is None:
        return np.nan
    if isinstance(v, bool):
        return float(v)
    try:
        return float(v)
    except (TypeError, ValueError):
        return np.nan


def load_all() -> dict:
    A = rj(EXP_A / "results/per_item.jsonl")
    sa = json.loads((EXP_A / "screen_items.json").read_text())
    sa = sa["items"] if isinstance(sa, dict) else sa
    C = rj(EXP_C / "results/analysis_table.jsonl")
    D = rj(EXP_D / "results/per_item_scores.jsonl")
    Dscreen = json.loads((EXP_D / "data/screen_items.json").read_text())
    E = json.loads((DS_E / "screen_adjudicated_labels.json").read_text())
    folds = json.loads((EXP_D / "data/folds.json").read_text())
    logger.info(f"loaded A per_item={len(A)} A screen={len(sa)} C={len(C)} D={len(D)} D screen={len(Dscreen)} E={len(E)} folds={len(folds)}")
    return {"A": A, "A_screen": sa, "C": C, "D": D, "D_screen": Dscreen, "E": E, "folds": folds}


def build_master(raw: dict) -> pd.DataFrame:
    A = {r["item_id"]: r for r in raw["A"] if r.get("track") in ("L", "H")}
    labA = {r["item_id"]: r.get("label") for r in raw["A_screen"]}
    refA = {r["item_id"]: r.get("reference_fol") for r in raw["A_screen"]}
    C = {r["item_id"]: r for r in raw["C"]}
    D = {r["item_id"]: r for r in raw["D"]}
    Ds = {r["item_id"]: r for r in raw["D_screen"]}
    E = raw["E"]
    ids = sorted(set(A) | set(C) | set(D) | set(E))
    rows = []
    for k in ids:
        a, c, d, e, ds = A.get(k, {}), C.get(k, {}), D.get(k, {}), E.get(k, {}), Ds.get(k, {})
        track = a.get("track") or c.get("track") or d.get("track") or e.get("track")
        if track not in ("L", "H"):
            continue
        text = a.get("text") or c.get("text") or ds.get("text") or (e.get("join_keys") or {}).get("raw_text") or ""
        cand = a.get("candidate_fol") or c.get("candidate_fol") or ds.get("candidate_fol") or ""
        ref = refA.get(k) or c.get("reference_fol") or ds.get("reference_fol") or e.get("reference_fol") or ""
        strata = a.get("strata") or ds.get("strata") or d.get("strata") or {}
        row = {
            "item_id": k, "track": track, "system": a.get("system") or c.get("system") or d.get("system") or e.get("system"),
            "text": text, "candidate_fol": cand, "reference_fol": ref, "cluster": norm(text),
            "in_A": k in A, "in_C": k in C, "in_D": k in D, "in_E": k in E,
            "lab_A": labA.get(k) if k in A else None, "lab_A_peritem": a.get("label"), "lab_C": c.get("label"),
            "lab_D": d.get("label"), "lab_D_hcur": d.get("label_h_curator"),
            "E_auto_label": e.get("auto_label"), "E_final_label": e.get("final_label"), "E_label_tier": e.get("label_tier"),
            "E_reading_choice": bool(e.get("reading_choice")) if e else None, "E_repair_ops": e.get("repair_ops"),
            "E_addrop_only_suspect": e.get("addrop_only_suspect"), "E_panel_votes": e.get("panel_votes"),
            "ops_A": a.get("repair_ops"), "ops_C": c.get("repair_ops"), "ops_D": d.get("repair_ops"),
            "auto_class_A": a.get("auto_class"), "auto_class_C": c.get("auto_class"), "auto_class_D": d.get("auto_class"),
            "D_subst_only": d.get("subst_only"), "D_vocab_borderline": d.get("vocab_borderline"),
            "D_census_class": d.get("census_class"), "C_vocab_strict": c.get("vocab_strict"),
            "C_medoid_depth": _f(c.get("medoid_depth")), "C_medoid_ops": c.get("medoid_ops"),
            "A_parse_ok": a.get("parse_ok"), "D_parse_ok": d.get("parse_ok"), "coverage_A": a.get("coverage_status"),
            "coverage_C": c.get("coverage_status"), "coverage_D": d.get("coverage_status"),
            "fused_flag": _f(a.get("fused_flag")), "role_flag": _f(a.get("role_flag")), "bow_flag": _f(a.get("bow_flag")), "l3_flag": _f(a.get("l3_flag")),
            "flag_medoid": _f(c.get("flag_medoid")),
            "fold_D": d.get("fold"), "words": _f(strata.get("words", c.get("words"))), "n_quant": _f(strata.get("n_quant")),
            "depth": _f(strata.get("depth")),
            "n_conditions": _f(strata.get("n_conditions", strata.get("n_cond"))),
            "exception": _f(strata.get("exception")),
            "D_cost_usd": _f(d.get("cost_usd")), "D_seconds": _f(d.get("seconds")),
            "sc5_eq_frac_cheap": _f(c.get("sc5_eq_frac_cheap")),
        }
        for m in A_SCORES:
            row[m] = _f(a.get(m)) if a else np.nan
        # exp A src/analysis.py::score_value('l2_bow') = bow_n_unanch + bow_uncarried (None unless parse_ok and cpu_status OK);
        # the reviewer audits and this plan's PT use bow_uncarried alone -> both are carried
        ok_a = a and str(a.get("parse_ok")) == "True" and a.get("cpu_status") == "OK"
        row["l2_bow_Adef"] = (_f(a.get("bow_n_unanch")) if a.get("bow_n_unanch") is not None else 0.0) + (_f(a.get("bow_uncarried")) if a.get("bow_uncarried") is not None else 0.0) if ok_a else np.nan
        for m in C_SCORES:
            row[m] = _f(c.get(m)) if c else np.nan
        for m, v in (d.get("oriented_scores") or {}).items():
            row[m] = _f(v)
        for m in D_EXTRA:
            row[m] = _f(d.get(m)) if d else np.nan
        rows.append(row)
    df = pd.DataFrame(rows).set_index("item_id", drop=False)
    logger.info(f"master frame: {len(df)} rows; tracks={df['track'].value_counts().to_dict()}")
    return df
