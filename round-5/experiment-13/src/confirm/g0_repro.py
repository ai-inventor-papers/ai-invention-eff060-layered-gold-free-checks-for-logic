#!/usr/bin/env python3
"""G0 ($0, SIG only; no FREE label is touched): reproduce exp 7's SIG primary within-template AUROCs (c_score_sig 0.954,
judge_cheap_disg 0.587, n = 1,904) with the copied auc_tools.py, and check StratAUC against a brute-force U statistic.
Writes results/g0_repro.json."""
from __future__ import annotations

import numpy as np

from auc_tools import StratAUC
from cc import E7, RES, dump, jl, load_scores, setup_logger

logger = setup_logger("g0")


def brute_auc(s, y) -> float:
    pos, neg = s[y], s[~y]
    u = sum(float((p > neg).sum()) + 0.5 * float((p == neg).sum()) for p in pos)
    return u / (len(pos) * len(neg))


@logger.catch(reraise=True)
def main() -> None:
    rows = load_scores("SIG")
    lab = {r["row_key"]: r["label"] for r in jl(E7 / "results/sig_labels.jsonl")}
    P = [r for r in rows if lab.get(r["row_key"]) in ("CORRECT", "ERROR") and r["c_score_sig"] is not None
         and r["judge_cheap_disg"] is not None]
    y = np.array([lab[r["row_key"]] == "ERROR" for r in P])
    tm = np.array([r["template_id"] for r in P])
    sids = sorted({r["sentence_id"] for r in P})
    cl = np.array([sids.index(r["sentence_id"]) for r in P])
    out = {"n": len(P), "n_error": int(y.sum()), "n_correct": int((~y).sum()), "n_sentences": len(sids)}
    for k, want in (("c_score_sig", 0.954340046099721), ("judge_cheap_disg", 0.5872179424966638)):
        s = np.array([r[k] for r in P], dtype=float)
        a = StratAUC(s, y, tm, cl).value()
        out[k] = {"auroc_within_template": a, "exp7": want, "abs_diff": abs(a - want), "pass": abs(a - want) <= 1e-3}
        bf = []
        for t in sorted(set(tm))[:3]:
            m = tm == t
            bf.append(abs(StratAUC(s[m], y[m], tm[m], cl[m]).value() - brute_auc(s[m], y[m])))
        out[k]["brute_force_max_abs_diff_3_templates"] = max(bf)
        out[k]["brute_force_pass"] = max(bf) < 1e-9
    out["n_pass"] = out["n"] == 1904
    out["PASS"] = bool(out["n_pass"] and all(out[k]["pass"] and out[k]["brute_force_pass"] for k in ("c_score_sig", "judge_cheap_disg")))
    dump(RES / "g0_repro.json", out)
    logger.info(out)
    assert out["PASS"], "G0 failed"


if __name__ == "__main__":
    main()
