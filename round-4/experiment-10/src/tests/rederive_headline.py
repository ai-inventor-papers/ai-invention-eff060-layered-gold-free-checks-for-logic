"""Headline re-derivation (TODO 5): each headline number recomputed from RAW per-row files through a DIFFERENT code path
(explicit pair counting / pandas; no import of src/), each with a placebo that must fail.

H1 SIG within-template AUROC of SIGPROXY k=3 (and c_score_sig) from results/csc_rcomp_sig_scores.jsonl
   -> explicit ERROR x CORRECT pair counting per template; placebo: labels permuted within template (expect ~0.5).
H2 paired cue effect on R_COMP bases: d(SIGPROXY K3) vs d(FREE3 align) from results/scores_raw.jsonl + data view
   -> placebo: arm labels swapped at random per base (expect diff ~0).
H3 typing strict accuracy (oracle E, proxy R_COMP, free3 E) from results/typing_search_rows.jsonl (raw searches) +
   operator map re-implemented here; placebo: true operators permuted across rows (expect ~ chance 0.12).
H4 FREE c_align d by word tercile on E bases from exp-8 perturb_scores.jsonl (raw) with our own tercile cut.
Writes results/rederive_headline.json.
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
E8 = Path("../../../../round-3/experiment-8/src/results/perturb_scores.jsonl")
rng = np.random.default_rng(12345)


def jl(p):
    return [json.loads(x) for x in Path(p).read_text().splitlines() if x.strip()]


def auc_within(rows, score, lab="label"):
    U = P = 0.0
    by = defaultdict(list)
    for r in rows:
        by[r["template_id"]].append(r)
    for rs in by.values():
        pos = [r[score] for r in rs if r[lab] == "ERROR"]
        neg = [r[score] for r in rs if r[lab] == "CORRECT"]
        for a in pos:
            for b in neg:
                U += 1.0 if a > b else (0.5 if a == b else 0.0)
        P += len(pos) * len(neg)
    return U / P


def main():
    out = {}
    # H1
    s = [r for r in jl(RES / "csc_rcomp_sig_scores.jsonl") if r["label"] in ("CORRECT", "ERROR")]
    for m in ("c_proxy", "c_score_sig"):
        rs = [r for r in s if r.get(m) is not None]
        a = auc_within(rs, m)
        pl = []
        for _ in range(20):
            by = defaultdict(list)
            for r in rs:
                by[r["template_id"]].append(r)
            perm = []
            for t, g in by.items():
                labs = [r["label"] for r in g]
                rng.shuffle(labs)
                perm += [{**r, "plab": l} for r, l in zip(g, labs)]
            pl.append(auc_within(perm, m, "plab"))
        out[f"H1_auroc_within_template_{m}"] = {"n": len(rs), "value": round(a, 4), "placebo_mean": round(float(np.mean(pl)), 4),
                                                "placebo_max": round(float(np.max(pl)), 4)}
    # H2
    view = {r["key"]: r for r in jl(ROOT / "data" / "perturb_view.jsonl")}
    sc = {r["key"]: r for r in jl(RES / "scores_raw.jsonl") if r["key"].startswith("PB:")}
    pairs = [(sc[k]["c_proxy"] > 0.5, sc[k]["c_free3_align"] > 0.5) for k, v in view.items()
             if v["fold"] == "BASE" and v["is_rcomp"] and k in sc and sc[k].get("c_proxy") is not None
             and sc[k].get("c_free3_align") is not None]
    a = np.array(pairs, float)
    swaps = []
    for _ in range(2000):
        flip = rng.random(len(a)) < 0.5
        x = np.where(flip, a[:, 1], a[:, 0])
        y = np.where(flip, a[:, 0], a[:, 1])
        swaps.append(x.mean() - y.mean())
    out["H2_paired_d_rcomp_bases"] = {"n_bases": len(a), "d_sigproxy_k3": round(a[:, 0].mean(), 4),
                                      "d_free3_align": round(a[:, 1].mean(), 4), "diff": round(a[:, 0].mean() - a[:, 1].mean(), 4),
                                      "placebo_swap_mean": round(float(np.mean(swaps)), 4),
                                      "placebo_p_abs_ge_observed": round(float(np.mean(np.abs(swaps) >= abs(a[:, 0].mean() - a[:, 1].mean()))), 4)}
    # H3
    MAP = {"DROP": "ADD", "ADD": "DROP", "ADD_ANY": "DROP", "SUBST": "MEANING_RENAME"}
    srch = defaultdict(dict)
    for x in jl(RES / "typing_search_rows.jsonl"):
        srch[x["which"]][x["key"]] = x
    muts = {k: v for k, v in view.items() if v["fold"] == "PERTURB"}
    sc_all = {r["key"]: r for r in jl(RES / "scores_raw.jsonl")}
    for which, src, statuskey in (("oracle", False, None), ("proxy", True, "proxy_majority_status"), ("free3", False, "free3_majority_status")):
        keys = [k for k, v in muts.items() if v["is_rcomp"] == src and (statuskey is None or sc_all.get(k, {}).get(statuskey))]
        truth = ["ADD" if muts[k]["operator"] == "ADD" else muts[k]["operator"] for k in keys]
        preds = []
        for k in keys:
            x = srch[which].get(k)
            ops = (x or {}).get("ops") or []
            preds.append(MAP.get(ops[0], ops[0]) if len(ops) == 1 else None)
        acc = np.mean([p == t for p, t in zip(preds, truth)])
        pl = []
        for _ in range(200):
            tp = list(truth)
            rng.shuffle(tp)
            pl.append(np.mean([p == t for p, t in zip(preds, tp)]))
        out[f"H3_typing_strict_{which}_{'RCOMP' if src else 'E'}"] = {"n": len(keys), "value": round(float(acc), 4),
                                                                       "placebo_mean": round(float(np.mean(pl)), 4),
                                                                       "placebo_max": round(float(np.max(pl)), 4)}
    # H4
    e8 = [x for x in jl(E8) if x["key"].startswith("PB:") and not x["is_rcomp"] and x.get("c_align") is not None]
    w = np.array([x["strata"]["words"] for x in e8], float)
    f = np.array([x["c_align"] > 0.5 for x in e8], float)
    c1, c2 = np.percentile(w, [100 / 3, 200 / 3])
    out["H4_c_align_d_by_tercile_E"] = {"n": len(e8), "cuts": [c1, c2], "T1": round(f[w <= c1].mean(), 4),
                                        "T2": round(f[(w > c1) & (w <= c2)].mean(), 4), "T3": round(f[w > c2].mean(), 4)}
    (RES / "rederive_headline.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
