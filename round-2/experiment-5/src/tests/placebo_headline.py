#!/usr/bin/env python3
"""Placebo for the headline paired test (PEER+TEXT - local judge, pooled R_AB, sentence-cluster bootstrap): recompute it from
raw per_item_E.jsonl + E_labels.jsonl with numpy/sklearn (own bootstrap), then on labels shuffled across rows (x20) and on a
random score replacing PEER+TEXT; the CI must exclude 0 on real labels and (almost always) include 0 on the placebos."""
import json
from collections import defaultdict
from pathlib import Path
import numpy as np
from sklearn.metrics import roc_auc_score
R = Path(__file__).resolve().parent.parent
lab = {}
for l in (R / "data/E_labels.jsonl").read_text().splitlines():
    x = json.loads(l); lab[x["row_key"]] = x
rows = []
for l in (R / "results/per_item_E.jsonl").read_text().splitlines():
    r = json.loads(l); L = lab[r["row_key"]]
    if r["system_class"] == "llm" and not L["reading_choice"] and L["label_tier"] in ("A", "B") and L["final_label"] in ("CORRECT", "ERROR"):
        rows.append((int(L["final_label"] == "ERROR"), r["p_peer_text"], r["judge_local_qwen8b_disg"], r["sentence_id"]))
y = np.array([a for a, *_ in rows]); f = np.array([b for _, b, _, _ in rows]); j = np.array([c for _, _, c, _ in rows])
sid = [d for *_, d in rows]
by = defaultdict(list)
for i, s in enumerate(sid): by[s].append(i)
groups = [np.array(v) for v in by.values()]
def boot_ci(yv, a, b, B=500, seed=1):
    rng = np.random.default_rng(seed); ds = []
    for _ in range(B):
        ix = np.concatenate([groups[k] for k in rng.integers(0, len(groups), len(groups))])
        if 0 < yv[ix].sum() < len(ix): ds.append(roc_auc_score(yv[ix], a[ix]) - roc_auc_score(yv[ix], b[ix]))
    return [float(np.percentile(ds, 2.5)), float(np.percentile(ds, 97.5))]
out = {"n": len(rows), "real_delta": roc_auc_score(y, f) - roc_auc_score(y, j), "real_ci": boot_ci(y, f, j)}
rng = np.random.default_rng(7); sh = []
for k in range(20):
    ys = rng.permutation(y); ci = boot_ci(ys, f, j, B=200, seed=k)
    sh.append({"delta": roc_auc_score(ys, f) - roc_auc_score(ys, j), "ci_excludes_0": ci[0] > 0 or ci[1] < 0})
out["shuffled_labels_share_ci_excluding_0"] = float(np.mean([s["ci_excludes_0"] for s in sh]))
out["shuffled_labels_mean_delta"] = float(np.mean([s["delta"] for s in sh]))
rs = rng.random(len(y)); ci = boot_ci(y, rs, j, B=200)
out["random_score_vs_judge"] = {"delta": roc_auc_score(y, rs) - roc_auc_score(y, j), "ci": ci, "passes_(CI>0)": ci[0] > 0}
(R / "results/placebo_headline.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out))
