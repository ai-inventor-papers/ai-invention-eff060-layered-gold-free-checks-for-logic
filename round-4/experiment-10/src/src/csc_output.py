"""STAGE 9: per-row score files + method_out.json (exp_gen_sol_out).

results/perturb_csc_scores.jsonl   every PERTURB row (mutants, controls, bases) with every score column + typing preds
results/csc_rcomp_sig_scores.jsonl every exp-7 SIG row with the SIGPROXY scores (development)
method_out.json                    datasets PERTURB_E_CSC, PERTURB_RCOMP_CSC, RCOMP_SIG_CSC; FREE rows never included.
All predict_* are strings (a score, higher = more likely ERROR; 'NA' when the arm did not produce one).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
sys.path.insert(0, str(SRC))
import csc_analysis as A  # noqa: E402

RES = ROOT / "results"
DATA = ROOT / "data"
E7 = A.E7

SCORE_COLS = ["c_csc", "c_csc_k4", "c_csc_multi", "c_csc_graded", "c_proxy", "c_proxy_k4", "c_proxy_graded",
              "c_local", "c_localbase", "c_local_graded", "c_align_exp8", "c_hyb_exp8", "c_free3_exact", "c_free3_align",
              "c_free3_lc", "judge_cheap_disg_exp8"]
PRED_NAMES = {"c_csc": "c_csc", "c_csc_k4": "c_csc_k4", "c_csc_multi": "c_csc_multi", "c_csc_graded": "c_csc_graded",
              "c_proxy": "c_sigproxy_k3", "c_proxy_k4": "c_sigproxy_k4", "c_proxy_graded": "c_sigproxy_graded",
              "c_local": "c_local2_own_sig", "c_localbase": "c_local2_base_sig", "c_align_exp8": "c_align_exp8",
              "c_free3_exact": "c_free3_exact", "c_free3_align": "c_free3_align", "c_free3_lc": "c_free3_lc"}


def s(x) -> str:
    return "NA" if x is None else (f"{x:.6g}" if isinstance(x, float) else str(x))


def main() -> None:
    rows, _ = A.load_rows()
    typ = {x["key"]: x for x in A.jl(RES / "typing_rows_csc.jsonl")}
    base = {r["base_item_id"]: r for r in rows if r["fold"] == "BASE"}
    keep = ["key", "item_id", "base_item_id", "sentence_id", "base_source", "is_rcomp", "fold", "operator", "op_fine",
            "subtype", "control_type", "op_label", "polarity", "matched_pair_id", "y", "strata", "template_id", "sig_key",
            "sig_shared_with_base", "cand_parse_ok"]
    extra = ["proxy_status", "proxy_per_peer", "proxy_n_used", "proxy_n_unknown", "proxy_majority_status", "proxy_graded_status",
             "free3_exact_status", "free3_align_status", "free3_lc_status", "free3_majority_status", "local_status",
             "local_per_peer", "localbase_per_peer", "secs_csc", "secs_free3"]
    with (RES / "perturb_csc_scores.jsonl").open("w") as f:
        for r in rows:
            b = base[r["base_item_id"]]
            rec = {k: r.get(k) for k in keep}
            rec["csc_status"] = r.get("csc_status", "NOT_RUN_D_BUDGET")
            for c in SCORE_COLS:
                rec[c] = r.get(c)
                bv = b.get(c)
                rec[f"base_endorsed_{c}"] = None if bv is None else bool(bv <= 0.5)
                rec[f"flag_{c}"] = None if r.get(c) is None else bool(r[c] > 0.5)
            for c in extra:
                rec[c] = r.get(c)
            t = typ.get(r["key"], {})
            for tg in ("oracle", "proxy", "free3", "csc"):
                rec[f"typing_{tg}_pred"] = t.get(f"{tg}_pred")
                rec[f"typing_{tg}_strict"] = t.get(f"{tg}_strict")
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    sc = {x["key"][4:]: x for x in A.jl(RES / "scores_raw.jsonl") if x["key"].startswith("SIG:")}
    sig_rows = A.jl(DATA / "rcomp_sig_view.jsonl")
    with (RES / "csc_rcomp_sig_scores.jsonl").open("w") as f:
        for r in sig_rows:
            x = sc.get(r["row_key"], {})
            f.write(json.dumps({"row_key": r["row_key"], "sentence_id": r["sentence_id"], "template_id": r["template_id"],
                                "family": r["family"], "slot": r["slot"], "label": r["label"], "matched_reading": r.get("matched_reading"),
                                "c_proxy": x.get("c_proxy"), "c_proxy_k4": x.get("c_proxy_k4"), "c_proxy_graded": x.get("c_proxy_graded"),
                                "proxy_status": x.get("proxy_status"), "proxy_per_peer": x.get("proxy_per_peer"),
                                "proxy_models": x.get("proxy_models"), "c_score_sig": r.get("c_score_sig"),
                                "judge_cheap_disg": r.get("judge_cheap_disg"), "judge_cheap_orig": r.get("judge_cheap_orig"),
                                "judge_local_disg": r.get("judge_local_disg"), "judge_local_orig": r.get("judge_local_orig")},
                               ensure_ascii=False) + "\n")
    ds = {"PERTURB_E_CSC": [], "PERTURB_RCOMP_CSC": []}
    for r in rows:
        t = typ.get(r["key"], {})
        ex = {"input": json.dumps({"text": r["text"], "candidate_fol": r["candidate_fol"]}, ensure_ascii=False),
              "output": "ERROR" if r["y"] == 1 else "CORRECT"}
        for c, name in PRED_NAMES.items():
            ex[f"predict_{name}"] = s(r.get(c))
        ex.update({"metadata_key": r["key"], "metadata_fold": r["fold"], "metadata_operator": r["op_label"],
                   "metadata_polarity": r["polarity"], "metadata_base": r["base_item_id"], "metadata_sentence_id": r["sentence_id"],
                   "metadata_base_source": r["base_source"], "metadata_sig_shared_with_base": r["sig_shared_with_base"],
                   "metadata_words": r["strata"].get("words"), "metadata_n_conditions": r["strata"].get("n_conditions"),
                   "metadata_csc_status": r.get("csc_status", "NOT_RUN_D_BUDGET"),
                   "metadata_sigproxy_status": r.get("proxy_status"),
                   "metadata_typing_oracle_samevocab": t.get("oracle_pred"), "metadata_typing_sigproxy": t.get("proxy_pred"),
                   "metadata_typing_free3": t.get("free3_pred")})
        ds["PERTURB_RCOMP_CSC" if r["is_rcomp"] else "PERTURB_E_CSC"].append(ex)
    sig_ex = []
    for r in sig_rows:
        x = sc.get(r["row_key"], {})
        sig_ex.append({"input": json.dumps({"text": r["text"], "candidate_fol": r["candidate_fol"]}, ensure_ascii=False),
                       "output": r["label"],
                       "predict_c_sigproxy_k3": s(x.get("c_proxy")), "predict_c_sigproxy_k4": s(x.get("c_proxy_k4")),
                       "predict_c_sigproxy_graded": s(x.get("c_proxy_graded")), "predict_c_score_sig_exp7": s(r.get("c_score_sig")),
                       "predict_judge_cheap_disg_exp7": s(r.get("judge_cheap_disg")),
                       "metadata_row_key": r["row_key"], "metadata_sentence_id": r["sentence_id"],
                       "metadata_template_id": r["template_id"], "metadata_family": r["family"],
                       "metadata_matched_reading": r.get("matched_reading"), "metadata_sigproxy_status": x.get("proxy_status")})
    out = {"metadata": {"method_name": "Candidate-Signature Consensus (CSC) - PERTURB/R_COMP (iteration 4, T6-P)",
                        "orientation": "every predict_* is a score, higher = more likely ERROR; flag at > 0.5",
                        "status": "CSC peers NOT generated (OpenRouter run budget exhausted, deviation D-BUDGET); "
                                  "predict_c_csc* = 'NA'. Scored arms: SIGPROXY (exp-7 SIG outputs of the same families, "
                                  "R_COMP), LOCAL2 (secondary local peers), FREE3 and exp-8 free consensus baselines.",
                        "prereg": "results/prereg_csc_P.json", "firewall": "FREE rows excluded (results/firewall.json)"},
           "datasets": [{"dataset": k, "examples": v} for k, v in ds.items()] + [{"dataset": "RCOMP_SIG_CSC", "examples": sig_ex}]}
    (ROOT / "method_out.json").write_text(json.dumps(out, ensure_ascii=False))
    print({k: len(v) for k, v in ds.items()}, len(sig_ex))


if __name__ == "__main__":
    main()
