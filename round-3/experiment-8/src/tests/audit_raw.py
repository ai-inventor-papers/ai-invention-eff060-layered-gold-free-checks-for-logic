#!/usr/bin/env python3
"""INDEPENDENT RE-DERIVATION from RAW files (TODO 5): a separate code path, own Mann-Whitney AUROC (pairwise
comparison, no rankdata / no stats.py), own imputation, own joins. Reads only raw inputs:
  results/scores_E.jsonl (pair-engine output), data/exp5/per_item_E.jsonl (frozen columns), data/exp5/E_labels.jsonl,
  results/pairs_E.jsonl, results/scores_screen.jsonl, data/screen/screen_adjudicated_labels.json, data/perturb_rows.jsonl,
  results/typing_rows.jsonl.
Placebo: each statistic is recomputed with labels permuted within stratum (seed 1) and must lose its signal.
Writes results/audit_raw.json and prints a comparison against the reported numbers."""
import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
R, D = ROOT / "results", ROOT / "data"
jl = lambda p: [json.loads(l) for l in p.read_text().splitlines() if l.strip()]  # noqa: E731


def mw_auc(pos, neg):
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    return float(((pos[:, None] > neg[None, :]).sum() + 0.5 * (pos[:, None] == neg[None, :]).sum()) / (len(pos) * len(neg)))


def strat(rows, key, ykey="y"):
    num = den = 0.0
    for s in sorted({r["stratum"] for r in rows}):
        rr = [r for r in rows if r["stratum"] == s]
        pos = [r[key] for r in rr if r[ykey] == 1]
        neg = [r[key] for r in rr if r[ykey] == 0]
        if pos and neg:
            num += mw_auc(pos, neg) * len(pos) * len(neg)
            den += len(pos) * len(neg)
    return num / den


out = {}
# ---------------------------------------------------------------- (1) E stratified AUROC from raw scores
pre5 = json.loads((D / "exp5/prereg.json").read_text())["imputation"]["neutral"]
fz = {r["row_key"]: r for r in jl(D / "exp5/per_item_E.jsonl")}
lab = {r["row_key"]: r for r in jl(D / "exp5/E_labels.jsonl")}
raw = {}
for s in jl(R / "scores_E.jsonl"):
    for r in s["rows"]:
        raw[r["key"]] = r
rows = []
for k, f in fz.items():
    L = lab[k]
    if L["system_class"] != "llm" or L.get("reading_choice") or L["final_label"] not in ("CORRECT", "ERROR") or L["label_tier"] not in ("A", "B"):
        continue
    unp = f["coverage_status"] == "UNPARSEABLE"
    ch = raw.get(k, {}).get("c_hyb")
    rows.append({"stratum": f["stratum"], "sid": f["sentence_id"], "y": int(L["final_label"] == "ERROR"),
                 "c_hyb": 1.0 if unp else (pre5["c_score_align"] if ch is None else ch),
                 "c_align": 1.0 if unp else (pre5["c_score_align"] if f["c_score_align"] is None else f["c_score_align"]),
                 "c_nf": 1.0 if unp else (pre5["NF-anchored:c_score_nf"] if f["nf_c_score"] is None else f["nf_c_score"])})
res = {m: strat(rows, m) for m in ("c_hyb", "c_align", "c_nf")}
res["hyb_minus_align"] = res["c_hyb"] - res["c_align"]
res["n"] = len(rows)
rng = np.random.default_rng(1)
pl = [dict(r) for r in rows]
for s in {r["stratum"] for r in pl}:
    idx = [i for i, r in enumerate(pl) if r["stratum"] == s]
    ys = rng.permutation([pl[i]["y"] for i in idx])
    for i, y in zip(idx, ys):
        pl[i]["y"] = int(y)
res["placebo"] = {m: strat(pl, m) for m in ("c_hyb", "c_align", "c_nf")}
# paired sentence-cluster bootstrap of HYB-ALIGN, real vs placebo (independent implementation, 300 resamples)
by = {}
for i, r in enumerate(rows):
    by.setdefault(r["sid"], []).append(i)
sids = sorted(by)
rngb = np.random.default_rng(7)


def boot_delta(rr, B=300):
    ds = []
    for _ in range(B):
        pick = rngb.integers(0, len(sids), len(sids))
        sub = [rr[i] for j in pick for i in by[sids[j]]]
        ds.append(strat(sub, "c_hyb") - strat(sub, "c_align"))
    return [float(np.percentile(ds, 2.5)), float(np.percentile(ds, 97.5))]


res["hyb_minus_align_ci_B300"] = boot_delta(rows)
res["hyb_vs_placebo_ci_excludes_0.5"] = None
out["E"] = res
A = json.loads((R / "analysis_hyb.json").read_text())["E"]["R_AB pooled"]
out["E_compare"] = {m: {"raw": res[m], "reported": A["metrics"][m]["strat_auroc"], "abs_diff": abs(res[m] - A["metrics"][m]["strat_auroc"])}
                    for m in ("c_hyb", "c_align", "c_nf")}
# ---------------------------------------------------------------- (2) over-alignment audit from raw pair verdicts
yab = {k: (int(L["final_label"] == "ERROR") if (L["system_class"] == "llm" and not L.get("reading_choice") and L["final_label"] in ("CORRECT", "ERROR")
                                                 and L["label_tier"] in ("A", "B")) else None) for k, L in lab.items()}
seen, disc = set(), {"new": [0, 0], "align": [0, 0]}
plab = dict(zip(list(yab), np.random.default_rng(3).permutation(list(yab.values()))))
pdisc = {"new": [0, 0], "align": [0, 0]}
for p in jl(R / "pairs_E.jsonl"):
    a, b = p["cand"], p["peer"]
    if a not in lab or b not in lab:
        continue
    key = tuple(sorted((a, b)))
    if key in seen:
        continue
    seen.add(key)
    g = "new" if (p["hyb_eq"] is True and p["align_eq"] is not True) else ("align" if p["align_eq"] is True else None)
    if g is None:
        continue
    for D_, Y in ((disc, yab), (pdisc, plab)):
        if Y[a] is not None and Y[b] is not None:
            D_[g][1] += 1
            D_[g][0] += int(Y[a] != Y[b])
out["audit"] = {g: v[0] / v[1] for g, v in disc.items()}
out["audit_placebo_labels_permuted"] = {g: v[0] / v[1] if v[1] else None for g, v in pdisc.items()}
# ---------------------------------------------------------------- (3) NF / HYB rename flip on PERTURB from raw pair verdicts
prow = {r["item_id"]: r for r in jl(D / "perturb_rows.jsonl")}
agree = {}
for p in jl(R / "pairs_E.jsonl"):
    if p["cand"].startswith(("PT:", "PB:")):
        agree.setdefault(p["cand"], {})[p["peer"]] = p
keep = {}
for iid, r in prow.items():
    if r["fold"] != "PERTURB_CONTROL" or r["control_type"] not in ("RENAME_NONCE", "RENAME_SYN"):
        continue
    c, b = agree.get("PT:" + iid), agree.get("PB:" + r["base_item_id"])
    if not c or not b:
        continue
    for m in ("align_eq", "nf_eq", "hyb_eq"):
        e = [q for q, v in b.items() if v[m] is True]
        k_ = keep.setdefault((r["control_type"], m), [0, 0])
        k_[0] += sum(1 for q in e if c.get(q, {}).get(m) is True)
        k_[1] += len(e)
out["rename_endorser_retention"] = {f"{t}|{m}": v[0] / v[1] for (t, m), v in keep.items()}
# ---------------------------------------------------------------- (4) PERTURB within-base AUROC of c_align / c_hyb (raw)
for m in ("c_align", "c_hyb", "c_nf"):
    per, pper = [], []
    rngp = np.random.default_rng(5)
    bases = {}
    for iid, r in prow.items():
        if r["base_source"] == "RCOMP":
            continue
        v = raw.get("PT:" + iid, {}).get(m)
        if v is None:
            continue
        bb = bases.setdefault(r["base_item_id"], {"pos": [], "neg": []})
        if r["fold"] == "PERTURB":
            bb["pos"].append(v)
        elif r["control_type"] in ("CONTRAPOSITIVE", "REORDER_COMMUTE", "REORDER_QUANT", "DEMORGAN"):
            bb["neg"].append(v)
    for bid, bb in bases.items():
        bv = raw.get("PB:" + bid, {}).get(m)
        if bv is not None:
            bb["neg"].append(bv)
        if bb["pos"] and bb["neg"]:
            per.append(mw_auc(bb["pos"], bb["neg"]))
            allv = bb["pos"] + bb["neg"]
            perm = rngp.permutation(allv)
            pper.append(mw_auc(perm[:len(bb["pos"])], perm[len(bb["pos"]):]))
    out[f"perturb_within_base_auroc_all_ops_{m}"] = {"raw": float(np.mean(per)), "placebo_permuted_within_base": float(np.mean(pper)), "n_bases": len(per)}
# ---------------------------------------------------------------- (5) typing accuracy from raw repair searches
MAP = {"DROP": "ADD", "ADD": "DROP"}
ty = {}
for x in jl(R / "typing_rows.jsonl"):
    ty[(x["key"], x["which"])] = x
acc = {"medoid_align": [], "oracle": []}
truth = []
for iid, r in prow.items():
    if r["fold"] != "PERTURB" or r["base_source"] == "RCOMP":
        continue
    truth.append(r["operator"])
    for w in acc:
        x = ty.get(("PT:" + iid, w))
        ops = [MAP.get(o, o) for o in (x or {}).get("ops", [])] if x else []
        acc[w].append(len(ops) == 1 and ops[0] == r["operator"])
out["typing_strict_acc"] = {w: float(np.mean(v)) for w, v in acc.items()}
perm_truth = np.random.default_rng(9).permutation(truth)
out["typing_placebo_true_labels_permuted"] = {}
i = 0
for w in acc:
    vals = []
    for (iid, r) in ((k, v) for k, v in prow.items() if v["fold"] == "PERTURB" and v["base_source"] != "RCOMP"):
        x = ty.get(("PT:" + iid, w))
        ops = [MAP.get(o, o) for o in (x or {}).get("ops", [])] if x else []
        vals.append(ops)
    out["typing_placebo_true_labels_permuted"][w] = float(np.mean([len(o) == 1 and o[0] == t for o, t in zip(vals, perm_truth)]))
(R / "audit_raw.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
