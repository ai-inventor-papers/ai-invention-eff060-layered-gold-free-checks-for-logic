"""Recompute E2-B exploratory V0/flash-lite AUROC from exp 12 per_item_E2B.jsonl (reviewer audit)."""
import json
from pathlib import Path
from sklearn.metrics import roc_auc_score
P = Path(__file__).resolve().parents[3] / "round-5/experiment-12/src/analysis/per_item_E2B.jsonl"
rows = [json.loads(l) for l in P.open()]
R = [r for r in rows if r["label"] in ("ERROR","CORRECT") and r["tier"]=="A_unaudited_ref" and not r["reading_choice"] and not r["contested"]]
out = {"n": len(R), "n_err": sum(r["label"]=="ERROR" for r in R)}
for m in ["V0","flashlite_disg","p_peer_text","V4","V2"]:
    s = [r for r in R if r.get(m) is not None]
    out[m] = {"pooled": round(roc_auc_score([r["label"]=="ERROR" for r in s],[r[m] for r in s]),4), "n": len(s)}
# CORRECT-row flag rate for V0 (base FA)
cor = [r for r in R if r["label"]=="CORRECT" and r.get("V0") is not None]
out["V0_FA_on_CORRECT_gt0.5"] = round(sum(r["V0"]>0.5 for r in cor)/len(cor),3)
allv = [r["V0"] for r in rows if r.get("V0") is not None]
out["V0_flag_rate_all"] = round(sum(v>0.5 for v in allv)/len(allv),3)
print(json.dumps(out, indent=1)); json.dump(out, open("recompute_e2b.json","w"), indent=1)
