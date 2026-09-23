"""Independent re-derivation of the headline numbers (TODO 4 audit).

Different code path from src/analysis.py + src/report.py: reads the raw per-unit score files and the frozen labels,
computes AUROC by explicit pairwise Mann-Whitney counting (no sklearn), bootstraps with python's `random` over
sentence clusters, re-fits the S4 combination with an sklearn Pipeline built here, and runs every test on shuffled labels
(placebo) to check that it does not pass vacuously. Writes results/audit_headlines.json.
"""
import json
import random
import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
R = ROOT / "results" / "scores"


def jl(name):
    return {json.loads(l)["key"]: json.loads(l) for l in (R / f"{name}.jsonl").read_text().splitlines() if l.strip()}


def normtxt(s):
    s = s.lower().replace("’", "'").replace("“", '"').replace("”", '"')
    return " ".join(re.sub(r"[^\w\s]", " ", s).split())


def auc_pairs(pos, neg):
    """Mann-Whitney AUROC by explicit pair counting, ties = 0.5."""
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    gt = (pos[:, None] > neg[None, :]).sum()
    eq = (pos[:, None] == neg[None, :]).sum()
    return (gt + 0.5 * eq) / (len(pos) * len(neg))


def auc_items(rows):
    pos = [s for s, y in rows if y == 1]
    neg = [s for s, y in rows if y == 0]
    return auc_pairs(pos, neg) if pos and neg else float("nan")


def cluster_boot(rows_by_cluster, stat, B=1000, seed=7):
    rng = random.Random(seed)
    keys = list(rows_by_cluster)
    out = []
    for _ in range(B):
        samp = [r for _ in keys for r in rows_by_cluster[rng.choice(keys)]]
        out.append(stat(samp))
    a = np.array(out)
    a = a[~np.isnan(a)]
    return [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]


items = json.loads((ROOT / "data" / "screen_items.json").read_text())
dev = set(json.loads((ROOT / "results" / "promptdev_local.json").read_text())["dev_slice_ids"])
j1, j2, j3 = jl("judge_cheap"), jl("judge_cheap2"), jl("judge_strong")
nli, pil = jl("roundtrip_nli"), jl("pilot")
out = {}

L = [r for r in items if r["track"] == "L" and r["label"] in ("CORRECT", "ERROR")]
H = [r for r in items if r["track"] == "H" and r["item_id"] not in dev and r["label_h_curator"] in ("CORRECT", "ERROR")]
yL = {r["item_id"]: int(r["label"] == "ERROR") for r in L}
yH = {r["item_id"]: int(r["label_h_curator"] == "ERROR") for r in H}


def score_j(src, k, cond):
    """Pre-registered convention: a judge call that returned no usable score counts as FLAGGED (score 1.0)."""
    r = src.get(f"{k}|{cond}")
    if r is None:
        return None
    return 1.0 if r.get("p") is None else 1 - r["p"]


def score_j_drop(src, k, cond):
    r = src.get(f"{k}|{cond}")
    return None if (r is None or r.get("p") is None) else 1 - r["p"]


# ---------- 1. headline AUROCs on track L
def auc_metric(ylab, f):
    rows = [(f(k), y) for k, y in ylab.items() if f(k) is not None]
    return auc_items(rows), len(rows)


heads = {
    "judge_cheap_disg": lambda k: score_j(j1, k, "disg"),
    "judge_cheap_orig": lambda k: score_j(j1, k, "orig"),
    "judge_cheap2_orig": lambda k: score_j(j2, k, "orig"),
    "judge_strong_disg": lambda k: score_j(j3, k, "disg"),
    "rt_nli_min": lambda k: (1 - nli[k]["rt_nli_min"]) if k in nli else None,
    "pilot_rerun_jacc": lambda k: (1 - pil[k]["pilot_rerun_jacc"]) if pil.get(k, {}).get("pilot_rerun_jacc") is not None else None,
    "pilot_joint_conflict": lambda k: pil[k].get("pilot_joint_conflict") if k in pil else None,
}
out["L_auroc"] = {m: {"auroc": a, "n": n} for m, (a, n) in ((m, auc_metric(yL, f)) for m, f in heads.items())}
out["L_auroc_judge_cheap_disg_failures_dropped"] = dict(zip(("auroc", "n"), auc_metric(yL, lambda k: score_j_drop(j1, k, "disg"))))

# placebo: shuffled labels
rng = np.random.default_rng(11)
keysL = list(yL)
perm = dict(zip(keysL, rng.permutation([yL[k] for k in keysL])))
out["L_auroc_shuffled_labels"] = {m: auc_metric(perm, f)[0] for m, f in heads.items()}


# ---------- 2. contamination: disguise delta per track and DiD (independent cluster bootstrap)
def deltas(ylab, items_track):
    clus = {}
    for r in items_track:
        k = r["item_id"]
        o, d = score_j(j1, k, "orig"), score_j(j1, k, "disg")
        if o is None or d is None:
            continue
        clus.setdefault(normtxt(r["text"]), []).append((o, d, ylab[k]))
    return clus


def dstat(rows):
    return auc_items([(d, y) for _, d, y in rows]) - auc_items([(o, y) for o, _, y in rows])


cL, cH = deltas(yL, L), deltas(yH, H)
dL = dstat([r for v in cL.values() for r in v])
dH = dstat([r for v in cH.values() for r in v])


def did_boot(cH, cL, B=1000, seed=3):
    rng = random.Random(seed)
    kH, kL = list(cH), list(cL)
    res = []
    for _ in range(B):
        sh = [r for _ in kH for r in cH[rng.choice(kH)]]
        sl = [r for _ in kL for r in cL[rng.choice(kL)]]
        res.append(dstat(sh) - dstat(sl))
    a = np.array(res)
    a = a[~np.isnan(a)]
    return [float(np.percentile(a, 2.5)), float(np.percentile(a, 97.5))]


out["contamination_judge_cheap"] = {"delta_L": dL, "delta_H_curator": dH, "DiD": dH - dL, "DiD_ci": did_boot(cH, cL)}


# placebo: shuffle labels within each track -> DiD should be ~0 and its CI should include 0
def shuffle_clus(c, seed):
    rr = random.Random(seed)
    ys = [y for v in c.values() for _, _, y in v]
    rr.shuffle(ys)
    it = iter(ys)
    return {k: [(o, d, next(it)) for o, d, _ in v] for k, v in c.items()}


pH, pL = shuffle_clus(cH, 1), shuffle_clus(cL, 2)
pdid = dstat([r for v in pH.values() for r in v]) - dstat([r for v in pL.values() for r in v])
out["contamination_placebo_shuffled"] = {"DiD": pdid, "DiD_ci": did_boot(pH, pL)}

# ---------- 3. S4 combination re-fit (own feature build + sklearn Pipeline) and combo - judge delta
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

eq = jl("rt_equiv")


def feats(k):
    p = pil.get(k, {})
    n = nli.get(k, {})
    e = eq.get(k, {})
    f = [1 - float(p.get("parse_ok", False)), p.get("pilot_joint_conflict"), p.get("pilot_arity_incons"),
         p.get("pilot_shape_incons"), p.get("pilot_dangling"), p.get("pilot_undeclared"),
         None if p.get("pilot_rerun_jacc") is None else 1 - p["pilot_rerun_jacc"],
         None if n.get("rt_nli_min") is None else 1 - n["rt_nli_min"], None if n.get("rt_nli_fwd") is None else 1 - n["rt_nli_fwd"],
         None if n.get("rt_nli_bwd") is None else 1 - n["rt_nli_bwd"], n.get("rt_nli_contra"),
         None if n.get("rt_embed_cos") is None else 1 - n["rt_embed_cos"],
         None if e.get("rt_reformalise_eq") is None else 1 - e["rt_reformalise_eq"],
         score_j(j1, k, "disg"), score_j(j2, k, "disg"), score_j(j1, k, "orig"), score_j(j2, k, "orig")]
    return [np.nan if v is None else float(v) for v in f]


keys = [r["item_id"] for r in L]
X = np.array([feats(k) for k in keys])
y = np.array([yL[k] for k in keys])
groups = [normtxt(r["text"]) for r in L]


def oof_auc(X, y, groups):
    oof = np.zeros(len(y))
    for tr, te in GroupKFold(n_splits=5).split(X, y, groups):
        pipe = make_pipeline(SimpleImputer(strategy="mean", add_indicator=True), StandardScaler(),
                             LogisticRegression(C=1.0, max_iter=3000))
        pipe.fit(X[tr], y[tr])
        oof[te] = pipe.predict_proba(X[te])[:, 1]
    return oof


oof = oof_auc(X, y, groups)
judge = np.array([score_j(j1, k, "disg") for k in keys])
a_combo = auc_items(list(zip(oof, y)))
a_judge = auc_items(list(zip(judge, y)))
clus = {}
for g, o, jv, yy in zip(groups, oof, judge, y):
    clus.setdefault(g, []).append((o, jv, yy))
ci_delta = cluster_boot(clus, lambda rows: auc_items([(o, yy) for o, _, yy in rows]) - auc_items([(jv, yy) for _, jv, yy in rows]))
out["S4_combo_refit"] = {"oof_auroc": a_combo, "judge_cheap_disg_auroc": a_judge, "delta": a_combo - a_judge, "delta_ci": ci_delta}
# placebo: shuffled labels -> OOF AUROC ~0.5 and delta CI should include 0 or be negative
ys = np.random.default_rng(5).permutation(y)
oof_s = oof_auc(X, ys, groups)
clus_s = {}
for g, o, jv, yy in zip(groups, oof_s, judge, ys):
    clus_s.setdefault(g, []).append((o, jv, yy))
out["S4_combo_placebo_shuffled"] = {"oof_auroc": auc_items(list(zip(oof_s, ys))),
                                    "delta_ci": cluster_boot(clus_s, lambda rows: auc_items([(o, yy) for o, _, yy in rows]) - auc_items([(jv, yy) for _, jv, yy in rows]))}

# ---------- 3b. strong (frontier) judge vs cheap judge on the SAME pre-registered subset (paired, cluster bootstrap)
pre = json.loads((ROOT / "prereg.json").read_text())
sub = set(pre["strong_subsample"]["L"])
cs = {}
for r in L:
    k = r["item_id"]
    if k not in sub:
        continue
    so, co = score_j(j3, k, "orig"), score_j(j1, k, "orig")
    if so is None or co is None:
        continue
    cs.setdefault(normtxt(r["text"]), []).append((so, co, yL[k]))
rows = [x for v in cs.values() for x in v]
d_sc = lambda rr: auc_items([(a, yy) for a, _, yy in rr]) - auc_items([(b, yy) for _, b, yy in rr])
out["strong_vs_cheap_orig_L_subset"] = {"n": len(rows), "auroc_strong": auc_items([(a, yy) for a, _, yy in rows]),
                                        "auroc_cheap": auc_items([(b, yy) for _, b, yy in rows]), "delta": d_sc(rows),
                                        "delta_ci": cluster_boot(cs, d_sc)}
ys_ = [yy for v in cs.values() for *_, yy in v]
random.Random(9).shuffle(ys_)
it_ = iter(ys_)
cs_p = {k: [(a, b, next(it_)) for a, b, _ in v] for k, v in cs.items()}
out["strong_vs_cheap_placebo_shuffled"] = {"delta": d_sc([x for v in cs_p.values() for x in v]), "delta_ci": cluster_boot(cs_p, d_sc)}

# ---------- 4. recall probe: predicate-name overlap via regex (not the parser)
rp = jl("recall_probe")
name_re = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\s*\(")
def names(f):
    return {m.lower() for m in name_re.findall(f or "")}
jo, jc = [], []
for r in items:
    if r["track"] != "H" or r["item_id"] not in rp or not rp[r["item_id"]].get("formula"):
        continue
    p = names(rp[r["item_id"]]["formula"])
    o, c = names(r["orig_gold"]), names(r["reference_fol"])
    if p and o:
        jo.append(len(p & o) / len(p | o))
    if p and c:
        jc.append(len(p & c) / len(p | c))
out["recall_probe_regex_names"] = {"J_probe_orig_mean": float(np.mean(jo)), "J_probe_corr_mean": float(np.mean(jc)), "n": len(jo)}

(ROOT / "results" / "audit_headlines.json").write_text(json.dumps(out, indent=1, default=float))
print(json.dumps(out, indent=1, default=float))
