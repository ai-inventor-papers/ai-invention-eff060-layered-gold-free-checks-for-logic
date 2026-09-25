#!/usr/bin/env python3
"""Post-hoc audit: recompute the pooled R_AB / R_A AUROCs and the headline ΔAUROCs from results/per_item_E.jsonl +
data/E_labels.jsonl through a separate, minimal code path (sklearn only, own imputation), assert agreement with
results/analysis.json to 1e-9, check identical n across paired metrics, and run a within-stratum permutation placebo.
Writes results/audit_rederive.json."""
import json
from pathlib import Path

import numpy as np
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parent.parent
R = ROOT / "results"
A = json.loads((R / "analysis.json").read_text())
pre = json.loads((R / "prereg.json").read_text())
neutral = pre["imputation"]["neutral"]
lab = {json.loads(l)["row_key"]: json.loads(l) for l in (ROOT / "data" / "E_labels.jsonl").read_text().splitlines()}
items = [json.loads(l) for l in (R / "per_item_E.jsonl").read_text().splitlines()]
IMP = {"p_peer_text": None, "p_text": None, "peer_only": neutral["ALIGN:g_score"], "c_score_align": neutral["c_score_align"],
       "l2_bow": neutral["l2_bow"], "l3_z3": neutral["l3_z3"]}
rows = []
for r in items:
    L = lab[r["row_key"]]
    if r["system_class"] != "llm" or L["reading_choice"] or L["label_tier"] not in ("A", "B") or L["final_label"] not in ("CORRECT", "ERROR"):
        continue
    x = {"y": int(L["final_label"] == "ERROR"), "tier": L["label_tier"], "stratum": r["stratum"], "sid": r["sentence_id"]}
    for m, nv in IMP.items():
        v = r.get(m)
        x[m] = (1.0 if r["coverage_status"] == "UNPARSEABLE" else nv) if v is None else v
    x["judge_local_qwen8b_disg"] = r.get("judge_local_qwen8b_disg")
    rows.append(x)
out = {"checks": {}}


def check(name, sub, m, ref):
    y = [x["y"] for x in sub]
    s = [x[m] for x in sub]
    v = roc_auc_score(y, s)
    ok = abs(v - ref) < 1e-9
    out["checks"][f"{name}:{m}"] = {"rederived": v, "analysis": ref, "n": len(sub), "match": ok}
    return ok


ok_all = True
for name, cond in (("R_AB pooled", lambda x: True), ("R_A pooled L20+EXC", lambda x: x["tier"] == "A" and x["stratum"] in ("L20", "EXC"))):
    sub = [x for x in rows if cond(x)]
    assert len(sub) == A["a_tables"][name]["n"], (name, len(sub), A["a_tables"][name]["n"])
    for m in ("p_peer_text", "p_text", "peer_only", "c_score_align", "l2_bow", "l3_z3"):
        ok_all &= check(name, sub, m, A["a_tables"][name]["metrics"][m]["auroc"])
    sj = [x for x in sub if x["judge_local_qwen8b_disg"] is not None]
    e = A["a_tables"][name]["vs_judge_local_qwen8b_disg"]
    if not e.get("untestable"):
        assert len(sj) == e["n"]
        d = roc_auc_score([x["y"] for x in sj], [x["p_peer_text"] for x in sj]) - roc_auc_score([x["y"] for x in sj], [x["judge_local_qwen8b_disg"] for x in sj])
        ref = e["paired"]["p_peer_text - judge_local_qwen8b_disg"]["delta"]
        out["checks"][f"{name}:delta_vs_local_judge"] = {"rederived": d, "analysis": ref, "n": len(sj), "match": abs(d - ref) < 1e-9}
        ok_all &= abs(d - ref) < 1e-9
rng = np.random.default_rng(0)
sub = rows
y = np.array([x["y"] for x in sub])
st = np.array([x["stratum"] for x in sub])
pl = {m: [] for m in ("p_peer_text", "p_text", "peer_only")}
for _ in range(200):
    yy = y.copy()
    for s_ in set(st):
        ix = np.where(st == s_)[0]
        yy[ix] = rng.permutation(yy[ix])
    for m in pl:
        pl[m].append(roc_auc_score(yy, [x[m] for x in sub]))
out["placebo"] = {m: {"mean": float(np.mean(v)), "p97.5": float(np.percentile(v, 97.5))} for m, v in pl.items()}
out["all_match"] = bool(ok_all)
(R / "audit_rederive.json").write_text(json.dumps(out, indent=1))
print(json.dumps({"all_match": ok_all, "placebo": out["placebo"]}))
assert ok_all
