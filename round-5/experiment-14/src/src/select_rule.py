#!/usr/bin/env python3
"""A6: apply the pre-registered selection rule mechanically to results/screen_E.json, then the reported-not-gating checks:
(a) selection stability (B=500 sentence-cluster resamples drawn within strata), (b) permutation null (B=200 within-stratum
label permutations; V4 is re-cross-fitted on each permuted label vector). Writes results/selection_E.json."""
from __future__ import annotations

import json

import numpy as np
from sklearn.linear_model import LogisticRegression

from common import RES, SEED, jdump, setup_logger
from labels import frame
from stats import WAuc, WStratAuc, auroc, strat_auroc

logger = setup_logger("select")
VARIANTS = ["V1", "V2", "V3", "V4", "V5"]
COST_RANK = {"V5": 0, "V1": 1, "V2": 1, "V3": 1, "V4": 1}
MARGIN, L25_TOL, CTRL_TOL, TIE = 0.015, 0.0, 0.01, 1e-4
RULE_TEXT = ("winner = variant with highest E LONG-strat AUROC (Z) that (i) beats V0 by >= +0.015 there AND (ii) >= V0 on L25 "
             "(point) AND (iii) >= V0 - 0.01 on CTRL; none -> 'NONE: V0 stands'; tie (|Δ| < 1e-4) -> cheaper (V5 < others)")


def rule(stats: dict) -> tuple[str, dict]:
    """stats[v] = {'LONG', 'L25', 'CTRL'} for v in V0 + VARIANTS -> (winner, per-variant qualification)."""
    q = {}
    for v in VARIANTS:
        c1 = stats[v]["LONG"] - stats["V0"]["LONG"] >= MARGIN
        c2 = stats[v]["L25"] >= stats["V0"]["L25"] - L25_TOL
        c3 = stats[v]["CTRL"] >= stats["V0"]["CTRL"] - CTRL_TOL
        q[v] = {"i_long_margin": bool(c1), "ii_L25": bool(c2), "iii_CTRL": bool(c3), "qualifies": bool(c1 and c2 and c3),
                "delta_long": stats[v]["LONG"] - stats["V0"]["LONG"]}
    ok = [v for v in VARIANTS if q[v]["qualifies"]]
    if not ok:
        return "NONE: V0 stands", q
    best = max(stats[v]["LONG"] for v in ok)
    tied = [v for v in ok if best - stats[v]["LONG"] < TIE]
    return sorted(tied, key=lambda v: (COST_RANK[v], v))[0], q


def cell_stats(y, S, st, w=None) -> dict:
    """LONG-strat, L25 pooled, CTRL pooled AUROC for each score column in S (dict name -> array); w = row weights."""
    out = {}
    L = np.isin(st, ["L25", "L20", "EXC"])
    for name, s in S.items():
        if w is None:
            out[name] = {"LONG": strat_auroc(y[L], s[L], st[L]), "L25": auroc(y[st == "L25"], s[st == "L25"]),
                         "CTRL": auroc(y[st == "CTRL"], s[st == "CTRL"])}
        else:
            out[name] = {"LONG": WStratAuc(y[L], s[L], st[L])(w[L]), "L25": WAuc(y[st == "L25"], s[st == "L25"])(w[st == "L25"]),
                         "CTRL": WAuc(y[st == "CTRL"], s[st == "CTRL"])(w[st == "CTRL"])}
    return out


def v4_oof(X, y, fold):
    p = np.zeros(len(y))
    for k in range(5):
        tr, te = fold != k, fold == k
        m = LogisticRegression(C=1e6, max_iter=2000).fit(X[tr], y[tr])
        p[te] = m.predict_proba(X[te])[:, 1]
    return p


@logger.catch(reraise=True)
def main():
    A = json.loads((RES / "screen_E.json").read_text())
    obs = {v: {"LONG": A["auroc"]["LONG-strat"][v]["auroc"], "L25": A["auroc"]["L25"][v]["auroc"], "CTRL": A["auroc"]["CTRL"][v]["auroc"]}
           for v in VARIANTS}
    obs["V0"] = {"LONG": A["auroc"]["LONG-strat"]["V0_frozen"]["auroc"], "L25": A["auroc"]["L25"]["V0_frozen"]["auroc"],
                 "CTRL": A["auroc"]["CTRL"]["V0_frozen"]["auroc"]}
    winner, q = rule(obs)
    logger.info(f"DECISION: {winner}; " + json.dumps({v: round(q[v]['delta_long'], 4) for v in VARIANTS}))
    # ---------------- (a) stability: within-stratum sentence resamples
    df = frame()
    P = df[df.Z].reset_index(drop=True)
    y = P.y.values.astype(int)
    st = P.stratum.values
    S = {v: P[v].astype(float).values for v in VARIANTS}
    S["V0"] = P.V0_frozen.astype(float).values
    rng = np.random.default_rng(SEED + 1)
    sids = P.sentence_id.values
    by_stratum = {h: np.unique(sids[st == h]) for h in np.unique(st)}
    sent_ix = {s: i for i, s in enumerate(np.unique(sids))}
    row_sent = np.array([sent_ix[s] for s in sids])
    picks = []
    for b in range(500):
        cnt = np.zeros(len(sent_ix))
        for h, ss in by_stratum.items():
            draw = rng.integers(0, len(ss), len(ss))
            np.add.at(cnt, [sent_ix[x] for x in ss[draw]], 1)
        w = cnt[row_sent]
        wb, _ = rule(cell_stats(y, S, st, w))
        picks.append(wb)
    from collections import Counter
    stab = {k: v / 500 for k, v in Counter(picks).items()}
    logger.info(f"stability {stab}")
    # ---------------- (b) permutation null
    rng2 = np.random.default_rng(SEED + 2)
    X4 = np.column_stack([P.c_exact.astype(float).values, P.V0_frozen.astype(float).values])
    fold = P.fold.values
    any_q = 0
    per_v = Counter()
    for b in range(200):
        yp = y.copy()
        for h in np.unique(st):
            m = np.where(st == h)[0]
            yp[m] = rng2.permutation(y[m])
        Sb = dict(S)
        Sb["V4"] = v4_oof(X4, yp, fold)
        wb, qb = rule(cell_stats(yp, Sb, st))
        if wb != "NONE: V0 stands":
            any_q += 1
        for v in VARIANTS:
            per_v[v] += qb[v]["qualifies"]
    null = {"B": 200, "share_any_variant_qualifies": any_q / 200, "share_per_variant": {v: per_v[v] / 200 for v in VARIANTS},
            "note": "within-stratum label permutation of Z; V4 re-cross-fitted on each permuted label vector"}
    logger.info(f"null {null}")
    out = {"winner": winner, "rule_text": RULE_TEXT, "observed": obs, "qualification": q, "n_screened": 5,
           "margin": MARGIN, "stability": {"B": 500, "scheme": "sentence-cluster resample within strata", "share_selected": stab},
           "permutation_null": null}
    jdump(out, RES / "selection_E.json")


if __name__ == "__main__":
    main()
