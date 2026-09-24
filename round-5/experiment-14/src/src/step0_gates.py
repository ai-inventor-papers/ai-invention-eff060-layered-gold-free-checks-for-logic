#!/usr/bin/env python3
"""STEP 0: population assertions + gate G0 (exp-6 estimator reproduces V0 strat AUROC 0.741, Δ(V0 - judge_cheap_disg)
+0.099 [0.049, 0.146] on R_AB and +0.116 on the long pool, to 1e-3) + words tercile cuts. Writes results/gate_G0.json."""
from __future__ import annotations

import json

import numpy as np

from common import E6, EV2, LONG, PER_ITEM, RES, jdump, jl, setup_logger
from stats import ClusterBoot, paired_boot

logger = setup_logger("step0_gates")


def r_ab(rows):
    return [r for r in rows if r["in_R_AB"] and r["pool"] == "E_POOL" and r["parse_ok"]]


@logger.catch(reraise=True)
def main():
    rows = jl(PER_ITEM)
    assert len(rows) == 8507, len(rows)
    R = r_ab(rows)
    y = np.array([r["y_R_AB"] for r in R], int)
    n_sent = len({r["sentence_id"] for r in R})
    logger.info(f"R_AB n={len(R)} err={y.sum()} cor={len(y)-y.sum()} sentences={n_sent}")
    assert (len(R), int(y.sum()), int(len(y) - y.sum()), n_sent) == (2686, 1822, 864, 292)
    pre = json.loads((E6 / "prereg_T1.json").read_text())
    crit_a = pre["criteria"]["a"]
    long_def_ok = "L25+L20+EXC" in crit_a
    out = {"population": {"n": len(R), "n_error": int(y.sum()), "n_correct": int(len(y) - y.sum()), "n_sentences": n_sent,
                          "definition": "per_item_T1 in_R_AB & pool == 'E_POOL' & parse_ok (exp 6 keys_for('R_AB'))"},
           "long_pool_exp6_text": crit_a, "long_pool_equals_L25_L20_EXC": long_def_ok}
    assert long_def_ok
    sid = [r["sentence_id"] for r in R]
    st = np.array([r["source_stratum"] for r in R])
    v0 = np.array([r["c_score_align"] for r in R], float)
    jd = np.array([r["judge_cheap_disg"] for r in R], float)
    assert not np.isnan(v0).any() and not np.isnan(jd).any()
    cb = ClusterBoot(sid, b=2000, seed=0)
    d_all = paired_boot(y, v0, jd, cb, "strat", st)
    m = np.isin(st, LONG)
    cbL = ClusterBoot(list(np.array(sid)[m]), b=2000, seed=0)
    d_long = paired_boot(y[m], v0[m], jd[m], cbL, "strat", st[m])
    tgt = {"V0_strat": 0.7414618757606236, "delta": 0.09897545149036036, "ci": [0.049345245474241926, 0.14599146000544172],
           "delta_long": 0.11625879215576673}
    g = {"V0_strat": d_all["a"], "delta": d_all["delta"], "ci": d_all["ci"], "delta_long": d_long["delta"], "ci_long": d_long["ci"],
         "targets_from_exp6_analysis_T1": tgt}
    g["pass"] = bool(abs(g["V0_strat"] - tgt["V0_strat"]) < 1e-3 and abs(g["delta"] - tgt["delta"]) < 1e-3
                     and abs(g["delta_long"] - tgt["delta_long"]) < 1e-3 and all(abs(a - b) < 1e-3 for a, b in zip(g["ci"], tgt["ci"])))
    out["G0"] = g
    logger.info(f"G0 {json.dumps(g)}")
    # words tercile cuts: eval-2 prereg_mech.json (frozen there)
    pm = json.loads((EV2 / "prereg_mech.json").read_text())
    out["words_tercile_cuts"] = pm["cuts"]["words_tercile_cuts"]
    out["words_tercile_rule"] = pm["cuts"]["words_tercile_rule"]
    jdump(out, RES / "gate_G0.json")
    if not g["pass"]:
        raise SystemExit("G0 FAILED")


if __name__ == "__main__":
    main()
