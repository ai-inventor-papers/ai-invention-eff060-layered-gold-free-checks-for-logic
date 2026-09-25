"""STEP 0.4: the analysis frame (exp 5 per_item_E + E_labels + E_blind + exp 6 metadata, joined on row_key) and gates
G0 (R_AB / R_A L20+EXC counts) and G1 (frozen c_score_align AUROCs reproduce tables.md)."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd
from loguru import logger

from paths import E5, E6, jl
from stats import auc

LONG = ("L25", "L20", "EXC")
STRATA = ("L25", "L20", "EXC", "CTRL")


def regime(r: dict, which: str) -> int | None:
    """analyse_E.regime(r, which) with default args (tiers A+B, no CONTESTED, no reading_choice, llm rows only)."""
    if r["system_class"] != "llm" or r.get("reading_choice"):
        return None
    fl = r["final_label"]
    if fl not in ("CORRECT", "ERROR"):
        return None
    if r["label_tier"] not in ("A", "B"):
        return None
    if which == "R_A" and r["label_tier"] != "A":
        return None
    return 1 if fl == "ERROR" else 0


def build_frame() -> tuple[pd.DataFrame, dict]:
    pre = json.loads((E5 / "results" / "prereg.json").read_text())
    neutral = pre["imputation"]["neutral"]["c_score_align"]
    labels = {r["row_key"]: r for r in jl(E5 / "data" / "E_labels.jsonl")}
    blind = {r["row_key"]: r for r in jl(E5 / "data" / "E_blind.jsonl")}
    items = jl(E5 / "results" / "per_item_E.jsonl")
    assert len(items) == len({r["row_key"] for r in items}) == 8507, "per_item_E row_key not unique / wrong size"
    # exp 6 metadata keyed on (item_id, prompt_variant) == exp 5 row_key
    e6 = json.loads((E6 / "full_method_out.json").read_text())
    m6 = {}
    for ds in e6["datasets"]:
        if ds["dataset"] != "E_heldout":
            continue
        for ex in ds["examples"]:
            pv = json.loads(ex["input"]).get("prompt_variant")
            m6.setdefault(f"{ex['metadata_item_id']}|{pv}", []).append(ex)
    del e6
    recs = []
    n_imp = {"unparseable": 0, "parseable_none": 0}
    for r in items:
        L, B = labels[r["row_key"]], blind[r["row_key"]]
        st = r["strata"]
        ex = m6.get(r["row_key"], [])
        ex1 = ex[0] if len(ex) == 1 else None
        unp = r["coverage_status"] == "UNPARSEABLE"
        c = r["c_score_align"]
        if unp:
            c_imp = 1.0
            n_imp["unparseable"] += 1
        elif c is None:
            c_imp = neutral
            n_imp["parseable_none"] += 1
        else:
            c_imp = c
        d = {"row_key": r["row_key"], "item_id": r["item_id"], "sentence_id": r["sentence_id"], "slot": r["slot"],
             "family_vendor": r["family_vendor"], "family_field": r["family"], "system": r["system"],
             "system_class": r["system_class"], "prompt_variant": r["prompt_variant"], "stratum": st["source_stratum"],
             "words": st["words"], "n_conditions": st["n_conditions"], "n_quant": st["n_quant"], "depth": st["depth"],
             "exception_type": st["exception_type"], "topup": bool(st.get("l25_topup_batch")), "fold_E": r["fold_E"],
             "coverage_status": r["coverage_status"], "parseable": not unp, "c_frozen_raw": c, "c_frozen": c_imp,
             "judge_local": r.get("judge_local_qwen8b_disg"), "p_peer_text": r.get("p_peer_text"),
             "nf_c_score": r.get("nf_c_score"), "l2_bow": r.get("l2_bow"),
             "final_label": L["final_label"], "label_tier": L["label_tier"], "reading_choice": L["reading_choice"],
             "correct_not_equivalent": L["correct_not_equivalent"], "error_ops": L["error_ops"],
             "reference_fol": L["reference_fol"], "reference_status": L["reference_status"],
             "gold_audit_flag": L["gold_audit_flag"], "text": B["text"], "candidate_fol": B["candidate_fol"],
             "e6_n_match": len(ex), "e6_in_R_AB": (ex1 or {}).get("metadata_in_R_AB"),
             "S4_local_oof": ex1.get("predict_S4_local_oof_RAB") if ex1 else None,
             "S4_noLLMjudge_oof": ex1.get("predict_S4_local_noLLMjudge_oof_RAB") if ex1 else None,
             "e6_output": ex1.get("output") if ex1 else None}
        d["y_AB"] = regime(d, "R_AB")
        d["y_A"] = regime(d, "R_A")
        recs.append(d)
    df = pd.DataFrame(recs)
    info = {"n_rows": len(df), "n_imputed": n_imp, "neutral_c_score_align": neutral}
    return df, info


def gates_G0_G1(df: pd.DataFrame) -> dict:
    ab = df[df.y_AB.notna()]
    ra = df[df.y_A.notna() & df.stratum.isin(["L20", "EXC"])]
    g0 = {"R_AB_n": len(ab), "R_AB_err": int(ab.y_AB.sum()), "R_AB_cor": int((ab.y_AB == 0).sum()),
          "R_AB_sent": int(ab.sentence_id.nunique()), "R_A_L20EXC_n": len(ra), "R_A_L20EXC_err": int(ra.y_A.sum()),
          "R_A_L20EXC_cor": int((ra.y_A == 0).sum())}
    exp = {"R_AB_n": 2686, "R_AB_err": 1822, "R_AB_cor": 864, "R_AB_sent": 292, "R_A_L20EXC_n": 449, "R_A_L20EXC_err": 261,
           "R_A_L20EXC_cor": 188}
    g0["pass"] = all(g0[k] == v for k, v in exp.items())
    g0["expected"] = exp
    # cross-check vs exp 6 metadata_in_R_AB flag (only rows with a unique exp 6 match)
    m = df[df.e6_n_match == 1]
    g0["exp6_flag_agreement"] = float(np.mean(m.y_AB.notna().values == m.e6_in_R_AB.astype(bool).values))
    g0["exp6_flag_disagree_n"] = int(np.sum(m.y_AB.notna().values != m.e6_in_R_AB.astype(bool).values))
    g0["rows_without_unique_exp6_match"] = int((df.e6_n_match != 1).sum())
    dis = m[m.y_AB.notna().values != m.e6_in_R_AB.astype(bool).values]
    g0["exp6_flag_disagreement_breakdown"] = {
        "ours_in_exp6_out": int(dis.y_AB.notna().sum()), "exp6_in_ours_out": int((~dis.y_AB.notna()).sum()),
        "by_system_class": {str(k): int(v) for k, v in dis.system_class.value_counts().items()},
        "explanation": ("exp 6 metadata_in_R_AB = tiers A+B CORRECT/ERROR of ANY system (incl. MALLS gold-as-system and "
                        "ccg2lambda); exp 5 analyse_E.regime (used here, G0 counts reproduced) keeps llm rows only. "
                        "Every disagreeing row is a non-LLM row; no LLM row disagrees.")}
    a1 = auc(ab.y_AB.values, ab.c_frozen.values)
    a2 = auc(ra.y_A.values, ra.c_frozen.values)
    g1 = {"auroc_R_AB_pooled": a1, "target_R_AB": 0.782, "auroc_R_A_L20EXC": a2, "target_R_A": 0.860,
          "tolerance": 5e-4, "pass": abs(a1 - 0.782) <= 5e-4 and abs(a2 - 0.860) <= 5e-4,
          "n_imputed_parseable_none_R_AB": int((ab.parseable & ab.c_frozen_raw.isna()).sum()),
          "n_unparseable_R_AB": int((~ab.parseable).sum())}
    logger.info(f"G0 {g0}")
    logger.info(f"G1 {g1}")
    return {"G0": g0, "G1": g1}
