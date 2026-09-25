"""Join for T1: one row per dataset-E row (8,507) keyed by canonical_key = item_id|prompt_variant.

base_rows(full)   exp-6 unit metadata + exp-5 FROZEN metric side (exp-5 imputation rule) + exp-6 local baseline columns
                  (E_baseline_features) + labels / tiers / regimes / error ops.  Asserts the key bijection.
api_columns(U)    NEW API columns from results/scores/*.jsonl, oriented (higher = unfaithful), with a status per row:
                  ok | fallback (JSON/no-verdict fallback 0.5) | fail (unparseable candidate: worst value 1.0, never sent)
                  | missing (not scored: budget / cap / partial sweep).
"""
from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path

from .common import DATA, RES, ROOT, jload, read_jsonl

SCORES = RES / "scores"
EXP5_COLS = ["c_score_align", "g_score", "nf_c_score", "nf_g_score", "p_peer_text", "p_text", "peer_only", "l2_bow", "l3_z3",
             "c_score_nf", "judge_local_qwen8b_disg", "judge_local_qwen8b_orig"]
EXP5_META = ["eqmv_medoid_eq", "nf_eq_medoid_nf", "top_code", "cost_usd_peer_text", "secs_pairs", "secs_sentence_total",
             "coverage_status", "family", "family_vendor", "slot", "n_peers_used", "nf_secs_pairs", "secs_text"]
LOCAL_COLS = ["parse_fail", "pilot_joint_conflict", "pilot_arity_incons", "pilot_shape_incons", "pilot_dangling",
              "pilot_rerun_jacc", "rt_nli_min_local", "rt_nli_fwd_local", "rt_nli_bwd_local", "rt_nli_contra_local",
              "rt_nli_min_alt_local", "rt_embed_cos_local", "judge_local_qwen8b_disg", "judge_local_qwen8b_orig",
              "judge_local_llama8b_disg", "judge_local_llama8b_orig", "judge_local_qwen14b_disg", "judge_local_qwen14b_orig",
              "sc5_local_eq_frac", "sc5_local_entropy", "b2_score"]
API_JUDGES = {"judge_cheap": "judge_cheap", "judge_cheap2": "judge_cheap2", "judge_strong": "judge_strong"}
RT_API = ["rt_nli_min", "rt_nli_fwd", "rt_nli_bwd", "rt_nli_contra", "rt_nli_min_alt", "rt_embed_cos"]
SC_API = ["sc5_eq_frac", "sc5_entropy"]


def ckey(item_id: str, variant: str | None) -> str:
    return f"{item_id}|{variant}"


def _last_by_key(p: Path) -> dict:
    out = {}
    if p.exists():
        for r in read_jsonl(p):
            out[r["key"]] = r
    return out


def exp5_imputation() -> dict:
    return jload(DATA / "exp5" / "prereg.json")["imputation"]


def load_exp5() -> dict:
    """{exp5 row_key: row} with exp 5's own imputation (analyse_E.py main(): unparseable -> 1.0; parseable-missing ->
    screen AGREE-set neutral; p_* missing -> 0.5 fallback)."""
    neutral = exp5_imputation()["neutral"]
    IMP = {"peer_only": neutral.get("ALIGN:g_score"), "g_score": neutral.get("ALIGN:g_score"),
           "c_score_nf": neutral.get("ALIGN:c_score_nf"), "c_score_align": neutral.get("c_score_align"),
           "nf_g_score": neutral.get("NF-anchored:g_score"), "nf_c_score": neutral.get("NF-anchored:c_score_nf"),
           "l2_bow": neutral.get("l2_bow"), "l3_z3": neutral.get("l3_z3")}
    out = {}
    n_imp = Counter()
    for r in read_jsonl(DATA / "exp5" / "per_item_E.jsonl"):
        unp = r["coverage_status"] == "UNPARSEABLE"
        for c, nv in IMP.items():
            r[c + "__imputed"] = False
            if unp:
                r[c] = 1.0
            elif r.get(c) is None:
                r[c] = nv
                r[c + "__imputed"] = True
                n_imp[c] += 1
        for c in ("p_peer_text", "p_text"):
            if r.get(c) is None:
                r[c] = 1.0 if unp else neutral.get("fallback", 0.5)
                n_imp[c] += 1
        out[r["row_key"]] = r
    out["__n_imputed__"] = dict(n_imp)
    return out


def base_rows(full: list[dict]) -> tuple[list[dict], dict]:
    """full = e_pool.load_E(blind=False). Returns (rows, info)."""
    U = {u["row_key"]: u for u in jload(DATA / "E_units.json")}
    E5 = load_exp5()
    n_imp = E5.pop("__n_imputed__")
    F6 = {r["row_key"]: r for r in (json.loads(l) for l in (DATA / "exp6_E_baseline_features.jsonl").read_text().splitlines() if l.strip())}
    folds = jload(DATA / "folds_E.json")
    sents = {}
    from .e_pool import load_sentences
    for s in load_sentences(blind=False):
        sents[s["metadata_sentence_id"]] = s
    rows, seen = [], set()
    for r in full:
        rk6 = r["row_key"]
        u = U[rk6]
        var = r.get("prompt_variant") or r.get("metadata_prompt_variant")
        ck = ckey(r["metadata_item_id"], var)
        assert ck not in seen, f"canonical key collision {ck}"
        seen.add(ck)
        e5 = E5[ck]
        f6 = F6[rk6]
        assert e5["item_id"] == r["metadata_item_id"] == u["item_id"] == f6["item_id"]
        assert e5["sentence_id"] == r["metadata_sentence_id"] == u["sentence_id"]
        assert e5["fold_E"] == u["fold_E"] == f6["metadata_fold_E"] == folds["row_fold"][rk6]
        s = sents[r["metadata_sentence_id"]]
        x = {"canonical_key": ck, "exp6_row_key": rk6, "exp5_row_key": ck, "item_id": r["metadata_item_id"],
             "sentence_id": r["metadata_sentence_id"], "fold_E": u["fold_E"], "pool": u["pool"], "parse_ok": u["parse_ok"],
             "text": u["text"], "candidate_fol": u["candidate_fol"], "reference_fol": r.get("reference_fol"),
             "text_d": u.get("text_d"), "fol_d": u.get("fol_d"), "system": u["system"], "sysvar": u["sysvar"],
             "family": e5.get("family"), "family_vendor": e5.get("family_vendor"), "slot": u.get("slot"),
             "prompt_variant": var, "strata": u["strata"], "source_stratum": u["strata"]["source_stratum"],
             "label_tier": r["metadata_label_tier"], "final_label": r["metadata_final_label"],
             "auto_label": r["metadata_auto_label"], "reading_choice": bool(r.get("metadata_reading_choice")),
             "repair_ops": r.get("metadata_repair_ops"), "error_ops": r.get("metadata_error_ops"),
             "reference_status": r.get("metadata_reference_status"),
             "labelling_ref_sentence": json.loads(s["input"]).get("reference_fol"), "sentence_ref_status": s["output"],
             "gen_cost_usd": r.get("metadata_cost_usd") or 0.0}
        for c in EXP5_COLS:
            x[c] = e5.get(c)
            if c + "__imputed" in e5:
                x[c + "__imputed"] = e5[c + "__imputed"]
        for c in EXP5_META:
            x["e5_" + c] = e5.get(c)
        for c in LOCAL_COLS:
            if c in f6:
                x["L:" + c] = f6[c]
                x["L:" + c + "__status"] = f6.get(c + "__status")
        rows.append(x)
    assert len(rows) == len(U) == len(E5) == len(F6) == 8507, (len(rows), len(U), len(E5), len(F6))
    assert len({x["exp6_row_key"] for x in rows}) == 8507
    info = {"n_rows": len(rows), "bijection": True, "n_exp5_imputed_parseable": n_imp,
            "n_colliding_item_ids": sum(1 for x in rows if "~" in x["exp6_row_key"])}
    return rows, info


def _judge(rows, fname, name, conds=("orig", "disg"), subset=None):
    J = _last_by_key(SCORES / f"{fname}.jsonl")
    if not J:
        return None
    cols = {}
    for cond in conds:
        c = f"{name}_{cond}"
        vals, st, cost, secs, typ = {}, {}, {}, {}, {}
        for x in rows:
            k = x["canonical_key"]
            if subset is not None and x["item_id"] not in subset:
                continue
            if not x["parse_ok"]:
                vals[k], st[k] = 1.0, "fail"
                continue
            r = J.get(f"{x['item_id']}|{cond}")
            if r is None:
                vals[k], st[k] = None, "missing"
                continue
            if r.get("p") is None:
                if str(r.get("fail") or "").startswith(("budget", "api", "exc")):
                    vals[k], st[k] = None, "missing"
                else:
                    vals[k], st[k] = 0.5, "fallback"
            else:
                vals[k], st[k] = 1.0 - float(r["p"]), "ok"
            cost[k], secs[k], typ[k] = r.get("cost"), r.get("seconds"), r.get("type")
        cols[c] = {"v": vals, "st": st, "cost": cost, "secs": secs, "type": typ}
    return cols


def api_columns(rows: list[dict]) -> dict:
    """{column: {'v': {ckey: value}, 'st': {ckey: status}, ...}} for every NEW API column that has any score."""
    out = {}
    frame_ids = {r["item_id"] for r in jload(DATA / "frontier_frame.json")["rows"]}
    for name, fname in API_JUDGES.items():
        r = _judge(rows, fname, name, subset=frame_ids if name == "judge_strong" else None)
        if r:
            out.update(r)
    R = _last_by_key(SCORES / "rt_nli_api.jsonl")
    V = _last_by_key(SCORES / "rt_verbal_api.jsonl")
    if R:
        for base in RT_API:
            vals, st = {}, {}
            for x in rows:
                k = x["canonical_key"]
                if not x["parse_ok"]:
                    vals[k], st[k] = 1.0, "fail"
                    continue
                r = R.get(x["item_id"])
                if r is None or r.get(base) is None:
                    v = V.get(x["item_id"])
                    # verbaliser returned nothing usable (empty / refusal) -> worst value, counted as a metric failure
                    if v is not None and not v.get("verbalisation") and not str(v.get("fail") or "").startswith(("budget", "api")):
                        vals[k], st[k] = 1.0, "fail_verbaliser"
                    else:
                        vals[k], st[k] = None, "missing"
                    continue
                vals[k] = r[base] if base == "rt_nli_contra" else 1.0 - r[base]
                st[k] = "ok"
            out[base] = {"v": vals, "st": st}
    S = _last_by_key(SCORES / "sc5.jsonl")
    if S:
        for base in SC_API:
            vals, st = {}, {}
            for x in rows:
                k = x["canonical_key"]
                if not x["parse_ok"]:
                    vals[k], st[k] = (1.0 if base == "sc5_eq_frac" else math.log(6)), "fail"
                    continue
                r = S.get(x["item_id"])
                if r is None:
                    vals[k], st[k] = None, "missing"
                    continue
                vals[k] = 1.0 - r["sc5_eq_frac"] if base == "sc5_eq_frac" else r["sc5_entropy"]
                st[k] = "ok"
            out[base] = {"v": vals, "st": st}
    return out
