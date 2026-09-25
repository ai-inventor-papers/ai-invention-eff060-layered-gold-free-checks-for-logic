#!/usr/bin/env python3
"""PART 1 NET: eval-2 mechanism.net_test (unchanged) per counting rule and pool -> results/part1_net.json."""
from __future__ import annotations

import json
import multiprocessing as mp
import os
import sys
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

os.environ["PYTHONHASHSEED"] = "0"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

from t8_paths import RESD, jdump  # noqa: E402

RULES = ["R_exact", "R_align", "R_name", "R_liberal", "R_oracle", "R_point_label_draw0"]


def one(task: tuple[str, str]) -> tuple[str, dict]:
    import t8_paths  # noqa: F401
    import mechanism as MC
    from stats import SentBoot
    pool, rule = task
    P = pd.read_pickle(RESD / "part1_rows.pkl")
    col = f"en_{pool}_{rule}"
    P["in_RAB"] = P[col].notna()
    P["_en"] = P[col].fillna(0).astype(int)
    out = {"full_B2000_delta": delta_full(P)}
    boot = SentBoot(P.sentence_id.values, b=200, seed=0)  # DEVIATION: B=200 for the unchanged net_test (AME refits too slow on the shared host)
    try:
        out["net_test_B200"] = MC.net_test(P, boot, "_en")
    except (ValueError, np.linalg.LinAlgError) as e:
        out["net_test_B200"] = {"error": str(e)[:200]}
    return f"{pool}|{rule}", out


def delta_full(P: pd.DataFrame) -> dict:
    """Delta(e+d) exactly as net_test's first block, with the B = 2000 sentence bootstrap."""
    from stats import SentBoot, ci
    boot = SentBoot(P.sentence_id.values, b=2000, seed=0)
    mask = P.in_RAB.values
    W = boot.W(mask)
    d = P[mask]
    y = d.y_AB.values.astype(int)
    en = d["_en"].values.astype(float)
    res = {}
    for nm, lo_m, hi_m in (("words_T3_minus_T1", d.words_t.values == "T1", d.words_t.values == "T3"),
                           ("ncond_4p_minus_01", d.ncond_bin.values == "0-1", d.ncond_bin.values == "4+")):
        def ed(Wm, m):
            with np.errstate(invalid="ignore", divide="ignore"):
                return ((Wm[..., m] @ (en[m] * y[m])) / (Wm[..., m] @ y[m]),
                        (Wm[..., m] @ ((1 - en[m]) * (1 - y[m]))) / (Wm[..., m] @ (1 - y[m])))
        one = np.ones(len(d))
        e_lo, d_lo = ed(one, lo_m)
        e_hi, d_hi = ed(one, hi_m)
        eb_lo, db_lo = ed(W, lo_m)
        eb_hi, db_hi = ed(W, hi_m)
        c = ci((eb_hi + db_hi) - (eb_lo + db_lo))
        res[nm] = {"delta_e_plus_d": float((e_hi + d_hi) - (e_lo + d_lo)), "ci": c, "delta_e": float(e_hi - e_lo),
                   "delta_d": float(d_hi - d_lo), "delta_d_ci": ci(db_hi - db_lo), "delta_e_ci": ci(eb_hi - eb_lo),
                   "verdict": ("IMPROVES_WITH_COMPLEXITY" if c[1] is not None and c[1] < 0 else
                               "DEGRADES_WITH_COMPLEXITY" if c[0] is not None and c[0] > 0 else "BALANCED_OR_UNDETERMINED")}
    return res


def main() -> None:
    tasks = [(p, r) for p in ("3pool", "9fam") for r in RULES]
    out = {}
    with ProcessPoolExecutor(max_workers=4, mp_context=mp.get_context("spawn")) as ex:
        for k, v in ex.map(one, tasks):
            out[k] = v
            print(k, {kk: (round(vv["delta_e_plus_d"], 3), vv["ci"]) for kk, vv in v["full_B2000_delta"].items()}, flush=True)
    jdump(RESD / "part1_net.json", out)


if __name__ == "__main__":
    main()
