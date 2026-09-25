#!/usr/bin/env python3
"""POST-HOC SENSITIVITY (not pre-registered; written after the E analysis): the pre-registered selection rule declared F1
FAILED because its deterministic FA-0.10 threshold is degenerate when >10% of screen CORRECT items tie at g=1. With
fractional tie-breaking NF-anchored passes both gates. This script fits the NF-based fusion [NF-anchored g, NF-anchored
c_score_nf, l2_bow, l3_z3] on the SAME screen AGREE set with the SAME procedure (screen only), applies it unchanged to E and
reports AUROC next to the pre-registered PEER+TEXT (ALIGN). Output: results/posthoc_nf_fusion.json. Labelled post hoc
everywhere it is reported."""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import peer_text as PT  # noqa: E402
from screen_fit import adj_label, fit_logistic, jl, solver_label, thr_at_fa  # noqa: E402
from analyse_E import Boot, auc_fast, ci, matched_fa, flagp  # noqa: E402

RES = ROOT / "results"
rows = {}
for s in jl(RES / "screen_scores.jsonl"):
    for r in s["rows"]:
        r["sentence_key"] = s["sentence_key"]
        rows[r["key"]] = r
labs = json.loads((ROOT / "data" / "screen" / "screen_adjudicated_labels.json").read_text())
agree = [(i, adj_label(v)) for i, v in labs.items() if i in rows and v["track"] in ("L", "H") and solver_label(v["auto_label"]) is not None
         and adj_label(v) is not None and solver_label(v["auto_label"]) == adj_label(v)]
ids = [i for i, _ in agree]
y = np.array([1 if l == "ERROR" else 0 for _, l in agree])
feats = ["NF-anchored:g_score", "NF-anchored:c_score_nf", "l2_bow", "l3_z3"]
X = np.array([[np.nan if rows[i].get(f) is None else float(rows[i][f]) for f in feats] for i in ids])
m = fit_logistic(X, y, [rows[i]["sentence_key"] for i in ids], feats)
m.pop("_oof"); ins = m.pop("_insample")
Lc = {i for i, l in agree if l == "CORRECT" and labs[i]["track"] == "L"}
m["threshold"] = thr_at_fa([p for i, p in zip(ids, ins) if i in Lc], 0.10)
# fractional selection-gate numbers on the screen (what the rule would have said with exact FA)
gate = {}
for v in ("NF-pure", "NF-anchored"):
    neg = [rows[i][f"{v}:g_score"] for i in Lc if rows[i].get(f"{v}:g_score") is not None]
    t, lam = matched_fa(neg, 0.10)
    rn = [r for k, r in rows.items() if k.startswith("RW:") and "_RENAME" in k and labs.get(k[3:].rsplit("_RENAME", 1)[0], {}).get("final_label") == "CORRECT"]
    rp = [r for k, r in rows.items() if k.startswith("PR:ROLE_PERMUTE:")]
    fl = lambda r: 1.0 if r.get(f"{v}:g_score") is None else flagp(r[f"{v}:g_score"], t, lam)
    gate[v] = {"t": t, "lambda": lam, "rename_fa": float(np.mean([fl(r) for r in rn])), "role_permute_recall": float(np.mean([fl(r) for r in rp]))}
# apply to E
lab = {r["row_key"]: r for r in jl(ROOT / "data" / "E_labels.jsonl")}
pre = json.loads((RES / "prereg.json").read_text())
sc = {}
for s in jl(RES / "E_sentences.jsonl"):
    for r in s["rows"]:
        sc[r["key"]] = r
items = jl(RES / "per_item_E.jsonl")
out = {"note": "POST-HOC sensitivity, not pre-registered", "screen_model": m, "fractional_selection_gates_screen": gate, "E": {}}
for name, cond in (("R_AB pooled", lambda L, r: L["label_tier"] in ("A", "B")),
                   ("R_AB long (L25+L20+EXC)", lambda L, r: L["label_tier"] in ("A", "B") and r["stratum"] != "CTRL"),
                   ("R_A pooled L20+EXC", lambda L, r: L["label_tier"] == "A" and r["stratum"] in ("L20", "EXC"))):
    sub = []
    for r in items:
        L = lab[r["row_key"]]
        if r["system_class"] != "llm" or L["reading_choice"] or L["final_label"] not in ("CORRECT", "ERROR") or not cond(L, r):
            continue
        if r["coverage_status"] == "UNPARSEABLE":
            p_nf = 1.0
        else:
            f = sc.get(r["row_key"], {})
            p_nf = PT.apply_logistic(m, f) if f.get("NF-anchored:g_score") is not None else PT.apply_logistic(pre["frozen"]["text_only"], f)
        sub.append({"y": int(L["final_label"] == "ERROR"), "sid": r["sentence_id"], "p_nf": p_nf, "p_align": r["p_peer_text"],
                    "judge": r.get("judge_local_qwen8b_disg")})
    yy = np.array([x["y"] for x in sub])
    a_nf = auc_fast(yy, np.array([x["p_nf"] for x in sub]))
    a_al = auc_fast(yy, np.array([x["p_align"] for x in sub]))
    bt = Boot([x["sid"] for x in sub], b=2000)
    pn = np.array([x["p_nf"] for x in sub]); pa = np.array([x["p_align"] for x in sub])
    jj = np.array([x["judge"] if x["judge"] is not None else np.nan for x in sub])
    okj = ~np.isnan(jj)
    d1 = [auc_fast(yy[ix], pn[ix]) - auc_fast(yy[ix], pa[ix]) for ix in bt.idx]
    d2 = [auc_fast(yy[ix][okj[ix]], pn[ix][okj[ix]]) - auc_fast(yy[ix][okj[ix]], jj[ix][okj[ix]]) for ix in bt.idx]
    out["E"][name] = {"n": len(sub), "auroc_nf_fusion": a_nf, "auroc_prereg_align_fusion": a_al, "delta_nf_minus_align": a_nf - a_al,
                      "ci": ci(d1), "auroc_local_judge": auc_fast(yy[okj], jj[okj]),
                      "delta_nf_fusion_minus_local_judge": auc_fast(yy[okj], pn[okj]) - auc_fast(yy[okj], jj[okj]), "ci_vs_judge": ci(d2)}
(RES / "posthoc_nf_fusion.json").write_text(json.dumps(out, indent=1, default=float))
print(json.dumps({"gate": gate, "oof": m["oof_auroc"], "E": out["E"]}, indent=1, default=float))
