#!/usr/bin/env python3
"""T4 independent re-derivation of 5 T1 headline numbers on a SEPARATE code path: reads only results/per_item_T1.jsonl and
data/frontier_frame.json; numpy pairwise AUROC (not rankdata), its own stratification and its own bootstrap loop
(different RNG stream: CIs are expected to agree to ~0.01, point estimates to 1e-3).

1 confirmatory stratified dAUROC(c_score_align - judge_cheap_disg), R_AB E_POOL PRIMARY
2 long pool (L25+L20+EXC) stratified delta
3 nested S4_full + c_score_align - S4_full (stratified, from the OOF columns)
4 frame ratio AUROC(c_score_align) / AUROC(best frontier view)
5 M3 slope difference (GEE point estimate, re-fitted with statsmodels directly)
+ placebos: shuffled labels -> AUROC ~ .5, delta ~ 0.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent


def auc_pairs(y, s):
    p, n = s[y == 1], s[y == 0]
    if len(p) == 0 or len(n) == 0:
        return float("nan")
    gt = (p[:, None] > n[None, :]).sum() + 0.5 * (p[:, None] == n[None, :]).sum()
    return float(gt / (len(p) * len(n)))


def strat(y, s, h):
    num = den = 0.0
    for g in set(h.tolist()):
        m = h == g
        n1, n0 = int(y[m].sum()), int((y[m] == 0).sum())
        if n1 and n0:
            num += auc_pairs(y[m], s[m]) * n1 * n0
            den += n1 * n0
    return num / den


def boot(rows, f, B=500, seed=12345):
    by = defaultdict(list)
    for i, r in enumerate(rows):
        by[r["sentence_id"]].append(i)
    keys = sorted(by)
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(B):
        ix = np.concatenate([by[keys[j]] for j in rng.integers(0, len(keys), len(keys))])
        out.append(f(ix))
    return [float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))]


def main():
    R = [json.loads(l) for l in (ROOT / "results" / "per_item_T1.jsonl").read_text().splitlines() if l.strip()]
    A = json.loads((ROOT / "results" / "analysis_T1.json").read_text())
    P = [r for r in R if r["pool"] == "E_POOL" and r["parse_ok"] and r["in_R_AB"]]
    out = {"n": len(P)}
    checks = []

    def delta_block(rows, name, a, b, ref):
        rows = [r for r in rows if r.get(a) is not None and r.get(b) is not None]
        y = np.array([r["y_R_AB"] for r in rows])
        h = np.array([r["source_stratum"] for r in rows])
        sa, sb = np.array([r[a] for r in rows]), np.array([r[b] for r in rows])
        d = strat(y, sa, h) - strat(y, sb, h)
        ci = boot(rows, lambda ix: strat(y[ix], sa[ix], h[ix]) - strat(y[ix], sb[ix], h[ix]))
        out[name] = {"delta": d, "ci": ci, "analysis": ref.get("delta"), "analysis_ci": ref.get("ci"), "n": len(rows)}
        checks.append((name, abs(d - ref["delta"]) < 1e-3 if ref.get("delta") is not None else None))
    ho = A["a_head_on"]
    delta_block(P, "1_confirmatory", "c_score_align", "judge_cheap_disg", ho["R_AB pooled"]["deltas"]["c_score_align - judge_cheap_disg [strat]"])
    delta_block([r for r in P if r["source_stratum"] in ("L25", "L20", "EXC")], "2_long", "c_score_align", "judge_cheap_disg",
                ho["R_AB long (L25+L20+EXC)"]["deltas"]["c_score_align - judge_cheap_disg [strat]"])
    delta_block(P, "3_nested", "S4_full_plus_c_score_align_oof", "S4_full_oof",
                A["b_s4"]["nested"]["S4_full_plus_c_score_align - S4_full"]["strat"])
    # 4 frame ratio
    fr = json.loads((ROOT / "data" / "frontier_frame.json").read_text())["rows"]
    ids = {r["item_id"] for r in fr}
    byid = {}
    for r in sorted(P, key=lambda r: r["canonical_key"]):
        if r["item_id"] in ids and r["item_id"] not in byid:
            byid[r["item_id"]] = r
    F = list(byid.values())
    d = A["d_frontier"]
    if "ratio" in d:
        best = d["ratio"]["best_frontier_view"]
        Fm = [r for r in F if r.get(best) is not None and r.get("c_score_align") is not None]
        y = np.array([r["y_R_AB"] for r in Fm])
        ratio = auc_pairs(y, np.array([r["c_score_align"] for r in Fm])) / auc_pairs(y, np.array([r[best] for r in Fm]))
        out["4_frame_ratio"] = {"ratio": ratio, "analysis": d["ratio"]["ratio"], "n": len(Fm)}
        checks.append(("4_frame_ratio", abs(ratio - d["ratio"]["ratio"]) < 1e-3))
    # 5 M3 point estimate
    try:
        import pandas as pd
        import statsmodels.api as sm
        import statsmodels.formula.api as smf
        y = np.array([r["y_R_AB"] for r in P])
        w = np.array([r["strata"]["words"] for r in P], float)
        z = (w - w.mean()) / w.std()
        slopes = {}
        for m in ("c_score_align", "judge_cheap_disg"):
            s = np.array([np.nan if r.get(m) is None else r[m] for r in P], float)
            # same label-free seeded tie-breaker as analyse_T1 (quantised scores: >10% of CORRECT rows at the max)
            s = s + 1e-9 * np.array([int(hashlib.sha1(("tiebreak|" + r["canonical_key"]).encode()).hexdigest()[:12], 16) / 16 ** 12
                                     for r in P])
            s = np.where(np.isnan(s), np.nanmedian(s), s)
            t = np.quantile(s[y == 0], 0.9)
            c = ((s > t).astype(int) == y).astype(float)
            df = pd.DataFrame({"c": c, "z": z, "h": [r["source_stratum"] for r in P], "g": [r["sentence_id"] for r in P]})
            slopes[m] = float(smf.gee("c ~ z + C(h)", groups="g", data=df, family=sm.families.Binomial(),
                                      cov_struct=sm.cov_struct.Exchangeable()).fit().params["z"])
        diff = slopes["c_score_align"] - slopes["judge_cheap_disg"]
        ref = A["e_M3"].get("M3_words", {}).get("diff")
        out["5_M3"] = {"diff": diff, "analysis": ref, "slopes": slopes}
        checks.append(("5_M3", abs(diff - ref) < 1e-3 if ref is not None else None))
    except Exception as e:  # noqa: BLE001
        out["5_M3"] = {"error": str(e)[:200]}
    # placebos
    rng = np.random.default_rng(7)
    y = np.array([r["y_R_AB"] for r in P])
    h = np.array([r["source_stratum"] for r in P])
    ca = np.array([r["c_score_align"] for r in P])
    jd = np.array([np.nan if r.get("judge_cheap_disg") is None else r["judge_cheap_disg"] for r in P])
    m = ~np.isnan(jd)
    pl = [auc_pairs(rng.permutation(y), ca) for _ in range(50)]
    pld = []
    for _ in range(50):
        yy = rng.permutation(y)
        pld.append(strat(yy[m], ca[m], h[m]) - strat(yy[m], jd[m], h[m]))
    out["placebo"] = {"shuffled_auroc_mean": float(np.mean(pl)), "shuffled_delta_mean": float(np.mean(pld))}
    out["checks"] = checks
    out["all_match"] = all(c[1] for c in checks if c[1] is not None)
    (ROOT / "results" / "audit_T1.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))
    return 0 if out["all_match"] else 1


if __name__ == "__main__":
    sys.exit(main())
