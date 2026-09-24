"""Independent re-derivation of the headline numbers from RAW files through a different code path
(sklearn roc_auc_score per stratum, raw sealed labels, raw consensus/judge caches; no analysis/ code imported)."""
import json, random, collections
import numpy as np
from sklearn.metrics import roc_auc_score
W = __import__("pathlib").Path(__file__).resolve().parents[1]
jl = lambda p: [json.loads(l) for l in open(p) if l.strip()]
lab = {r["row_key"]: r for r in jl(W / "e2src/sealed/labels_E2.jsonl") if r["system_class"] == "llm"}
cand = {r["row_key"]: r for r in jl(W / "e2/candidates_E2_nolabels.jsonl")}
order = json.load(open(W / "e2src/work/e2a_order.json"))[:110]
keep = set(order)
v0 = {}
for s in jl(W / "cache/consensus_sentences.jsonl"):
    for r in s["rows"]:
        v0[r["key"]] = r.get("c_score_align")
units = {u["key"]: u for u in jl(W / "cache/units_E2.jsonl")}
loc = {}
for r in jl(W / "cache/judge_local_qwen8b.jsonl"):
    if r.get("p") is not None:
        loc[r["key"]] = 1 - r["p"]
pil = {r["key"]: r for r in jl(W / "cache/pilot_E2.jsonl")}
rows = []
for k, l in lab.items():
    c = cand[k]
    if c["sentence_id"] not in keep or l["label"] not in ("CORRECT", "ERROR") or l["reading_choice"] or l["label_tier"] not in ("A", "B"):
        continue
    rows.append(dict(k=k, sid=c["sentence_id"], st=c["stratum"], y=int(l["label"] == "ERROR"), v0=v0.get(k),
                     loc=loc.get(k + "|disg"), **{m: pil[k].get(m) for m in ("pilot_joint_conflict", "pilot_arity_incons", "pilot_shape_incons", "pilot_dangling", "pilot_rerun_jacc")}))


def sauc(rs, col, ycol="y"):
    num = den = 0
    for st in set(r["st"] for r in rs):
        g = [r for r in rs if r["st"] == st and r[col] is not None]
        y = [r[ycol] for r in g]
        if 0 < sum(y) < len(y):
            w = sum(y) * (len(y) - sum(y))
            num += roc_auc_score(y, [r[col] for r in g]) * w
            den += w
    return num / den if den else None


out = {}
for cell, sts in (("ALL", ("L25", "EXC", "DT")), ("DT", ("DT",)), ("LONG", ("L25", "EXC"))):
    rs = [r for r in rows if r["st"] in sts]
    out[cell] = {"n": len(rs), "n_err": sum(r["y"] for r in rs), "n_cor": sum(1 - r["y"] for r in rs),
                 "V0": sauc(rs, "v0"), "local_disg": sauc(rs, "loc")}
    out[cell]["delta_V0_minus_local"] = out[cell]["V0"] - out[cell]["local_disg"]
    for m in ("pilot_joint_conflict", "pilot_arity_incons", "pilot_shape_incons", "pilot_dangling", "pilot_rerun_jacc"):
        out[cell][m] = sauc(rs, m)
# placebo: shuffled labels within stratum -> AUROC ~0.5 and the V0-local delta ~0
rng = random.Random(0)
pl = []
for b in range(200):
    rs = [dict(r) for r in rows]
    for st in set(r["st"] for r in rs):
        idx = [i for i, r in enumerate(rs) if r["st"] == st]
        ys = [rs[i]["y"] for i in idx]
        rng.shuffle(ys)
        for i, y in zip(idx, ys):
            rs[i]["y"] = y
    pl.append((sauc(rs, "v0"), sauc(rs, "v0") - sauc(rs, "loc")))
pa = np.array(pl)
out["placebo_shuffled"] = {"V0_mean": float(pa[:, 0].mean()), "V0_p2.5_97.5": np.percentile(pa[:, 0], [2.5, 97.5]).tolist(),
                           "delta_mean": float(pa[:, 1].mean()), "delta_p2.5_97.5": np.percentile(pa[:, 1], [2.5, 97.5]).tolist(),
                           "real_V0_ALL_above_placebo_p97.5": bool(out["ALL"]["V0"] > np.percentile(pa[:, 0], 97.5))}
# rename controls from their raw rows
rr = jl(W / "results/rename_V0_rows.jsonl")
for t in ("RENAME_SYN", "RENAME_NONCE"):
    g = [r for r in rr if r["type"] == t and r["v0_control"] is not None and r["v0_parent"] is not None]
    out[t] = {"n": len(g), "FA": sum(r["v0_control"] > 0.5 for r in g) / len(g), "base": sum(r["v0_parent"] > 0.5 for r in g) / len(g)}
# drift + spend from raw logs
d = json.load(open(W / "e2src/panel_drift_E2.json"))
out["drift_majority_agreement"] = d["combined"]["majority_agreement"]
spend = sum(r["cost_usd"] for r in jl(W / "e2src/cost_ledger.jsonl")) + sum(r["cost_usd"] for r in jl(W / "cache/l3_cost_ledger.jsonl")) \
    + sum((r.get("cost") or 0) for r in jl(W / "cache/t1_results/costs.jsonl"))
out["spend_usd"] = spend
# compare with the pipeline's aggregated numbers
A = json.load(open(W / "results/auroc_cells.json"))["R_AB"]
cmp = {}
for cell, key in (("ALL", "ALL"), ("DT", "DT"), ("LONG", "LONG (L25+EXC)")):
    m = A[key]["metrics"]
    cmp[cell] = {"n_match": A[key]["n_rows"] == out[cell]["n"], "V0_absdiff": abs(m["c_score_align"]["strat"] - out[cell]["V0"]),
                 "local_absdiff": abs(m["judge_local_qwen8b_disg"]["strat"] - out[cell]["local_disg"])}
out["comparison_with_pipeline"] = cmp
json.dump(out, open(W / "audit/rederive_out.json", "w"), indent=1)
print(json.dumps(out, indent=1))
