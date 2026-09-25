#!/usr/bin/env python3
"""Independent re-derivation of the E2-B headline numbers from RAW files, through code paths different from
src/analyse_e2b.py (which uses exp-6 api_bar rankdata AUROC, ClusterBoot and consensus_variants):
  - labels straight from e2bsrc/sealed/labels_E2.jsonl, joined via e2bsrc/candidates_E2_nolabels.jsonl (row_key -> sid, slot);
  - scores straight from scores/scores_E2B.jsonl; AUROC = sklearn.metrics.roc_auc_score; stratified AUROC = n1*n0-weighted
    mean over word bins; bootstrap = numpy resampling of sentence ids (seed 12345, B=2000), own loop;
  - V0_decoupled recomputed from the raw eval-2 matrix lines with this file's own agreement logic;
  - rename paired flips recomputed from scores/controls_lf_scores_E2B.jsonl;
  - PLACEBOS that must fail: labels permuted within word bin (200 permutations: permutation p for the delta; and one
    permuted-label bootstrap whose CI must include 0), and a random-score baseline.
-> analysis/rederive_headline.json"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr
from sklearn.metrics import roc_auc_score

WS = Path(__file__).resolve().parents[1]


def jl(p):
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]


def strat_auc(y, s, h):
    num = den = 0.0
    for b in set(h):
        m = h == b
        n1 = int(y[m].sum())
        n0 = int(m.sum()) - n1
        if n1 and n0:
            num += roc_auc_score(y[m], s[m]) * n1 * n0
            den += n1 * n0
    return num / den if den else float("nan")


def boot_delta(y, a, b, h, sid, B=2000, seed=12345):
    rng = np.random.default_rng(seed)
    idx_by = defaultdict(list)
    for i, s in enumerate(sid):
        idx_by[s].append(i)
    keys = list(idx_by)
    out = []
    for _ in range(B):
        ix = np.concatenate([idx_by[keys[k]] for k in rng.integers(0, len(keys), len(keys))])
        yy, hh = y[ix], h[ix]
        if len(set(yy)) < 2:
            continue
        d = strat_auc(yy, a[ix], hh) - strat_auc(yy, b[ix], hh)
        if not np.isnan(d):
            out.append(d)
    return [float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))]


def main():
    lab = {r["row_key"]: r for r in jl(WS / "e2bsrc/sealed/labels_E2.jsonl")}
    nol = jl(WS / "e2bsrc/candidates_E2_nolabels.jsonl")
    sc = {r["row_key"]: r for r in jl(WS / "scores/scores_E2B.jsonl")}
    wb = {s["sentence_id"]: s["word_bin"] for s in json.loads((WS / "e2b/sentences_E2B.json").read_text())}
    rows = []
    for n in nol:
        L = lab[n["row_key"]]
        if L["system_class"] != "llm":
            continue
        s = sc[f"{n['sentence_id']}|{n['slot']}"]
        rows.append({"k": f"{n['sentence_id']}|{n['slot']}", "sid": n["sentence_id"], "label": L["label"], "tier": L["label_tier"],
                     "rc": bool(L["reading_choice"]), "V0": s["V0"], "FL": s["flashlite_disg"], "bin": wb[n["sentence_id"]]})
    out = {"label_counts_all_llm_rows": {k: sum(r["label"] == k for r in rows) for k in ("CORRECT", "ERROR", "UNRESOLVED", "UNPARSEABLE")}}
    P = [r for r in rows if r["label"] in ("CORRECT", "ERROR") and r["tier"] == "A_unaudited_ref" and not r["rc"]]
    out["population_R_A_UNAUDITED"] = {"n": len(P), "ERROR": sum(r["label"] == "ERROR" for r in P), "CORRECT": sum(r["label"] == "CORRECT" for r in P),
                                       "CORRECT_sentences": len({r["sid"] for r in P if r["label"] == "CORRECT"})}
    V = [r for r in P if r["V0"] is not None]
    y = np.array([r["label"] == "ERROR" for r in V], int)
    out["V0_strat_auroc"] = strat_auc(y, np.array([r["V0"] for r in V]), np.array([r["bin"] for r in V]))
    Q = [r for r in P if r["V0"] is not None and r["FL"] is not None]
    yq = np.array([r["label"] == "ERROR" for r in Q], int)
    a = np.array([r["V0"] for r in Q])
    b = np.array([r["FL"] for r in Q])
    h = np.array([r["bin"] for r in Q])
    sid = [r["sid"] for r in Q]
    d = strat_auc(yq, a, h) - strat_auc(yq, b, h)
    out["paired"] = {"n": len(Q), "n_correct": int((yq == 0).sum()), "V0_auroc": strat_auc(yq, a, h), "flashlite_disg_auroc": strat_auc(yq, b, h),
                     "delta": d, "delta_ci": boot_delta(yq, a, b, h, sid)}
    # placebo 1: permutation null of the delta (labels permuted within word bin)
    rng = np.random.default_rng(7)
    perm = []
    for _ in range(200):
        yp = yq.copy()
        for bb in set(h):
            m = np.where(h == bb)[0]
            yp[m] = rng.permutation(yp[m])
        perm.append(strat_auc(yp, a, h) - strat_auc(yp, b, h))
    perm = np.array(perm)
    out["placebo_permuted_labels"] = {"null_mean": float(perm.mean()), "null_sd": float(perm.std()),
                                      "permutation_p_two_sided": float(np.mean(np.abs(perm) >= abs(d))),
                                      "one_permuted_label_bootstrap_ci": None}
    yp = yq.copy()
    for bb in set(h):
        m = np.where(h == bb)[0]
        yp[m] = rng.permutation(yp[m])
    ci_p = boot_delta(yp, a, b, h, sid, B=1000, seed=99)
    out["placebo_permuted_labels"]["one_permuted_label_bootstrap_ci"] = ci_p
    out["placebo_permuted_labels"]["one_permuted_delta"] = strat_auc(yp, a, h) - strat_auc(yp, b, h)
    out["placebo_permuted_labels"]["ci_includes_0_as_required"] = bool(ci_p[0] <= 0 <= ci_p[1])
    # placebo 2: random score instead of V0
    rs = np.random.default_rng(3).random(len(Q))
    ci_r = boot_delta(yq, rs, b, h, sid, B=1000, seed=5)
    out["placebo_random_score_vs_flashlite"] = {"delta": strat_auc(yq, rs, h) - strat_auc(yq, b, h), "ci": ci_r,
                                                "ci_includes_0_as_required": bool(ci_r[0] <= 0 <= ci_r[1])}
    # V0_decoupled from raw matrix lines, own agreement logic
    labk = {r["k"]: r["label"] for r in rows}
    fam = {k: sc[k]["family_vendor"] for k in sc}
    dec = {}
    for m in jl(WS / "scores/pairwise_classes_E2B.jsonl"):
        node = {r["row_key"]: nd["node_id"] for nd in m["nodes"] for r in nd["rows"]}
        eq = set()
        for i, j, e, _k, _s in m["pairs"]:
            if e is True:
                eq.add((i, j))
                eq.add((j, i))
        for x in node:
            peers = [p for p in node if p != x and fam[p] != fam[x] and labk.get(p) != "CORRECT"]
            if len(peers) >= 2:
                ag = sum(node[p] == node[x] or (node[x], node[p]) in eq for p in peers)
                dec[x] = 1 - ag / len(peers)
    D = [r for r in P if r["k"] in dec]
    yd = np.array([r["label"] == "ERROR" for r in D], int)
    out["V0_decoupled_strat_auroc"] = strat_auc(yd, np.array([dec[r["k"]] for r in D]), np.array([r["bin"] for r in D]))
    # label-free: concordance and rename flips
    both = [s for s in sc.values() if s["parse_ok"] and s["V0"] is not None and s.get("flashlite_disg_status") == "ok"]
    out["concordance_spearman_V0_flashlite"] = float(spearmanr([s["V0"] for s in both], [s["flashlite_disg"] for s in both]).statistic)
    out["concordance_n"] = len(both)
    fl = {}
    for c in jl(WS / "scores/controls_lf_scores_E2B.jsonl"):
        par = sc[c["parent_row_key"]]["V0"]
        if c["V0_control"] is None or par is None:
            continue
        t = c["control_type"]
        f = fl.setdefault(t, [0, 0])
        f[0] += int(c["V0_control"] > 0.5 and not par > 0.5)
        f[1] += 1
    out["rename_paired_flip"] = {t: {"flip": v[0] / v[1], "n": v[1]} for t, v in fl.items()}
    (WS / "analysis/rederive_headline.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
