"""Recompute E2-A headline AUROCs from exp 11 per_item_E2A.jsonl (reviewer audit, iter 5)."""
import json, collections
from pathlib import Path
from sklearn.metrics import roc_auc_score
P = Path(__file__).resolve().parents[3] / "round-5/experiment-11/src/per_item_E2A.jsonl"
rows = [json.loads(l) for l in P.open()]
def rab(r): return r["label"] in ("ERROR","CORRECT") and r["label_tier"] in ("A","B") and not r["reading_choice"]
out = {}
tiers = collections.Counter((r["label"], r["label_tier"]) for r in rows)
out["label_tier_counts"] = {f"{a}|{b}": c for (a,b), c in tiers.items()}
def auc(sub, m):
    s = [r for r in sub if r.get(m) is not None]
    y = [1 if r["label"]=="ERROR" else 0 for r in s]
    if len(set(y)) < 2: return None
    return round(roc_auc_score(y, [r[m] for r in s]), 4), len(s), sum(y)
def strat_auc(sub, m):
    num = den = 0.0
    for st in set(r["stratum"] for r in sub):
        s = [r for r in sub if r["stratum"]==st and r.get(m) is not None]
        e = [r[m] for r in s if r["label"]=="ERROR"]; c = [r[m] for r in s if r["label"]=="CORRECT"]
        for a in e:
            for b in c:
                num += 1.0 if a > b else 0.5 if a == b else 0.0; den += 1
    return round(num/den, 4) if den else None
R = [r for r in rows if rab(r)]
for cell, f in {"DT": lambda r: r["stratum"]=="DT", "L25": lambda r: r["stratum"]=="L25",
                "LONG": lambda r: r["stratum"] in ("L25","EXC"), "ALL": lambda r: True}.items():
    sub = [r for r in R if f(r)]
    out[cell] = {"n": len(sub), "n_err": sum(r["label"]=="ERROR" for r in sub),
                 **{m: {"pooled": auc(sub, m), "strat": strat_auc(sub, m)} for m in
                    ["c_score_align","p_peer_text","judge_local_qwen8b_disg","judge_cheap_disg","l3_z3"]}}
out["flash_lite_scored_rows_all"] = sum(r["judge_cheap_disg"] is not None for r in rows)
out["flash_lite_scored_rows_RAB"] = sum(r["judge_cheap_disg"] is not None for r in R)
out["flash_lite_scored_RAB_long"] = sum(r["judge_cheap_disg"] is not None for r in R if r["stratum"] in ("L25","EXC"))
print(json.dumps(out, indent=1))
json.dump(out, open("recompute_e2a.json","w"), indent=1)
