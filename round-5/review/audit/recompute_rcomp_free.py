"""Recompute R_COMP FREE provisional within-template AUROCs (exp 13 per_item_rcomp_free.jsonl), reviewer audit."""
import json
from pathlib import Path
P = Path(__file__).resolve().parents[3] / "round-5/experiment-13/src/results/per_item_rcomp_free.jsonl"
rows = [json.loads(l) for l in P.open()]
U = [r for r in rows if r["untouched"] and r["label_binary"] in ("ERROR","MAPPED","CORRECT") or (r["untouched"] and r["label"] in ("ERROR_CERT","UNRESOLVED_GLOSS_GATE_FAILED"))]
U = [r for r in rows if r["untouched"] and r["label"] in ("ERROR_CERT","UNRESOLVED_GLOSS_GATE_FAILED")]
def wt(sub, m):
    num = den = 0.0
    for t in set(r["template_id"] for r in sub):
        s = [r for r in sub if r["template_id"]==t and r.get(m) is not None]
        e = [r[m] for r in s if r["label"]=="ERROR_CERT"]; c = [r[m] for r in s if r["label"]!="ERROR_CERT"]
        for a in e:
            for b in c: num += 1 if a>b else .5 if a==b else 0; den += 1
    return round(num/den,4)
out = {}
both = [r for r in U if r.get("c_score_align") is not None and r.get("judge_cheap_disg") is not None]
out["paired_disg_n"] = len(both)
out["c_align_on_paired"] = wt(both,"c_score_align"); out["judge_disg_on_paired"] = wt(both,"judge_cheap_disg")
for m in ["c_score_align","c_exact","c_score_hyb","c_score_nf","judge_cheap_disg","judge_cheap_orig"]:
    out[m] = wt(U, m)
mapped = [r for r in U if r["label"]!="ERROR_CERT" and r.get("c_score_align") is not None]
out["c_align_flag_rate_MAPPED_gt0.5"] = round(sum(r["c_score_align"]>0.5 for r in mapped)/len(mapped),3)
print(json.dumps(out, indent=1)); json.dump(out, open("recompute_rcomp_free.json","w"), indent=1)
