#!/usr/bin/env python3
"""OUTPUT: method_out.json (exp_gen_sol_out). Dataset groups:
  E_heldout          one example per dataset-E row (8,507, unparseable included with coverage_status); predictions
                     predict_V0 (frozen c_score_align) ... predict_V5, predict_c_exact, predict_gg, predict_gg_allyes,
                     predict_gg_b (secondary, if run), predict_p_peer_text / predict_judge_cheap_disg (frozen context);
                     higher = ERROR; 'NA' where not computed.
  PERTURB_E_bases    the 722 PERTURB E-base items GG was evaluated on (MEANING_RENAME, RENAME_SYN, RENAME_NONCE, BASE).
  GG_checker_gates   G-A (840) and G-B (229) items with the checker's verdicts (v1 dev, v2 confirm).
metadata = headline decisions (M1), gates, cost."""
from __future__ import annotations

import hashlib
import json
import sys

import numpy as np

from common import DS_E, FREEZE, PER_ITEM, RES, ROOT, jl, utc

sys.path.insert(0, str(FREEZE))
import gg  # noqa: E402


def fmt(v) -> str:
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "NA"
    return f"{float(v):.6g}"


def main():
    d = json.loads((DS_E / "full_data_out.json").read_text())
    groups = {g["dataset"]: g["examples"] for g in d["datasets"]}
    del d
    cand = {}
    for e in groups["heldout_candidates"]:
        inp = json.loads(e["input"])
        cand[f"{e['metadata_item_id']}|{inp.get('prompt_variant')}"] = inp
    texts = {e["metadata_sentence_id"]: json.loads(e["input"])["text"] for e in groups["heldout_sentences"]}
    del groups
    S = {r["canonical_key"]: r for r in jl(RES / "scores_E_variants.jsonl")}
    V4 = {r["row_key"]: r for r in jl(RES / "scores_E_V4.jsonl")}
    G = {r["row_key"]: r for r in jl(RES / "scores_gg_E.jsonl")}
    GB = {r["row_key"]: r for r in jl(RES / "scores_ggb_E.jsonl")} if (RES / "scores_ggb_E.jsonl").exists() else {}
    ex_E = []
    for r in jl(PER_ITEM):
        k = r["canonical_key"]
        s = S[k]
        inp = cand.get(r["exp5_row_key"], {})
        rab = bool(r["in_R_AB"] and r["pool"] == "E_POOL" and r["parse_ok"])
        z = rab and s["in_matrix"] and s["n_peers"] >= 2
        g = G.get(s["row_key"], {})
        ex = {"input": json.dumps({"text": inp.get("text"), "candidate_fol": inp.get("candidate_fol"), "system": r["system"],
                                   "prompt_variant": r["prompt_variant"]}, ensure_ascii=False),
              "output": r["final_label"],
              "predict_V0": fmt(r["c_score_align"]), "predict_V0_rep": fmt(s["V0_rep"]), "predict_V1": fmt(s["V1"]),
              "predict_V2": fmt(s["V2"]), "predict_V3": fmt(s["V3"]), "predict_V4": fmt(V4.get(s["row_key"], {}).get("V4")),
              "predict_V5": fmt(s["V5"]), "predict_c_exact": fmt(s["c_exact"]), "predict_gg": fmt(g.get("c_gg")),
              "predict_gg_allyes": fmt(g.get("c_gg_allyes")),
              "predict_p_peer_text": fmt(r.get("p_peer_text")), "predict_judge_cheap_disg": fmt(r.get("judge_cheap_disg")),
              "metadata_row_key": s["row_key"], "metadata_sentence_id": r["sentence_id"], "metadata_stratum": r["source_stratum"],
              "metadata_fold": r["fold_E"], "metadata_in_R_AB": rab, "metadata_in_Z": bool(z), "metadata_y_R_AB": r["y_R_AB"],
              "metadata_family": s["family"], "metadata_words": r["strata"]["words"], "metadata_n_conditions": r["strata"]["n_conditions"],
              "metadata_n_peers": s["n_peers"], "metadata_coverage_status": s["coverage_status"],
              "metadata_label_tier": r["label_tier"], "metadata_error_ops": r["error_ops"], "metadata_gg_status": g.get("gg_status", "NOT_SEARCHED")}
        if GB:
            ex["predict_gg_b_allyes"] = fmt(GB.get(s["row_key"], {}).get("c_ggb_allyes"))
        ex_E.append(ex)
    # PERTURB
    ex_P = []
    for r in jl(RES / "scores_gg_perturb.jsonl"):
        ex_P.append({"input": json.dumps({"text": texts.get(r["sentence_id"]), "item_key": r["key"], "kind": r["kind"]}, ensure_ascii=False),
                     "output": "ERROR" if r["y"] == 1 else "CORRECT",
                     "predict_gg": fmt(r["c_gg"]), "predict_gg_allyes": fmt(r["c_gg_allyes"]), "predict_c_exact_identity_map": fmt(r["c_exact_pt"]),
                     "predict_c_align_exp8": fmt(r["c_align"]),
                     "metadata_kind": r["kind"], "metadata_base": r["base"], "metadata_sentence_id": r["sentence_id"],
                     "metadata_base_status": r["base_status"], "metadata_polarity": r["polarity"], "metadata_base_endorsed": r["base_endorsed"],
                     "metadata_stratum": r["stratum"], "metadata_n_peer_rows": r["n_peer_rows"]})
    # gate items with verdicts
    import gloss_client as GC
    import gg_gates as GT
    cache = GC.load_cache()
    pre = json.loads((ROOT / "prereg_gg.json").read_text())
    sha = lambda p: hashlib.sha256(json.dumps(p, sort_keys=True, ensure_ascii=False).encode()).hexdigest()  # noqa: E731
    pa1, pa2 = pre["prompt_gloss_gg_gateA_v1"], json.loads((RES / "prompt_gateA_v2.json").read_text())
    pg1, pg2 = gg.PROMPT_GG_V1, json.loads((RES / "prompt_gg_v2.json").read_text())
    M = pre["checker"]["model"]
    ex_G = []
    for it in GT.gate_a_items():
        k = ["gateA", it["atom"], it["meaning"]]
        ex_G.append({"input": json.dumps({"gate": "G-A", "sentence": it["text"], "candidate_atom": it["atom"], "proposed_meaning": it["meaning"]}, ensure_ascii=False),
                     "output": it["expected"],
                     "predict_checker_v1": cache.get(GC.ckey(M, sha(pa1), it["sid"], k), "NOT_RUN"),
                     "predict_checker_v2": cache.get(GC.ckey(M, sha(pa2), it["sid"], k), "NOT_RUN"),
                     "metadata_half": it["half"], "metadata_class": it["cls"], "metadata_gate": "G-A"})
    for it in json.loads((RES / "gg_gate_items_B.json").read_text())["items"]:
        k = list(gg.pair_key(("pred", it["a"], it["b"])))
        ex_G.append({"input": json.dumps({"gate": "G-B", "sentence": it["text"], "symbol_a": it["a"], "use_a": it["a_use"], "symbol_b": it["b"],
                                          "use_b": it["b_use"]}, ensure_ascii=False),
                     "output": it["expected"],
                     "predict_checker_v1": cache.get(GC.ckey(M, sha(pg1), it["sid"], k), "NOT_RUN"),
                     "predict_checker_v2": cache.get(GC.ckey(M, sha(pg2), it["sid"], k), "NOT_RUN"),
                     "metadata_half": it["half"], "metadata_class": it["kind"], "metadata_gate": "G-B"})
    m1 = json.loads((FREEZE / "CONSENSUS_FREEZE_READY.json").read_text())
    sel = json.loads((FREEZE / "selection.json").read_text())
    ggd = json.loads((RES / "gg_dev.json").read_text())
    meta = {"method_name": "Iteration-5 FREEZE: label-free consensus rescoring screen (V0-V5) + gloss-gated name-free agreement (GG)",
            "written_utc": utc(), "orientation": "every predict_* is higher = more likely ERROR; 'NA' = not computed",
            "M1": m1, "part_A_winner": sel["winner"], "part_A_qualification": sel["qualification"],
            "part_A_stability": sel["stability"], "part_A_null": sel["permutation_null"],
            "GG_status": m1["GG"]["status"], "GG_gates": ggd["gates"], "GG_cost": ggd["cost"],
            "spend_usd_total": sum(float(json.loads(l).get("usd") or 0) for l in (ROOT / "cost_ledger.jsonl").read_text().splitlines() if l.strip()),
            "E_status": "development data; every E number is a development number"}
    out = {"metadata": meta, "datasets": [{"dataset": "E_heldout", "examples": ex_E},
                                          {"dataset": "PERTURB_E_bases", "examples": ex_P},
                                          {"dataset": "GG_checker_gates", "examples": ex_G}]}
    (ROOT / "method_out.json").write_text(json.dumps(out, ensure_ascii=False, default=str))
    print(len(ex_E), len(ex_P), len(ex_G))


if __name__ == "__main__":
    main()
