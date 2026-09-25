# NOTE (published copy): this file names server paths this repository
# does not publish (a stage it does not ship, or another run's workspace),
# so the steps that read them will not run from a clone as written:
#   /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/prereg.json
"""$0 reproduction checks (before any CSC score is joined to labels): (1) eval 2's fixed 3-family pool
deepseek+microsoft+openai (m4_fixed_pools_k3.csv: AUROC 0.7845 / strat 0.7427) recomputed from the frozen label-free
pairwise matrix; (2) T1's c_score_align pooled/strat AUROC (tables_T1.md: 0.782 / 0.741) from per_item_T1 columns.
Stop-the-claims rule: |delta| > 0.01 -> deviation recorded and the join diagnosed."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from loguru import logger

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
sys.path.insert(0, str(ROOT / "vendor" / "ev2"))
sys.path.insert(0, str(SRC))
from consensus_mx import SentenceMatrix, c_from_fams, row_consensus  # noqa: E402
from stats import auc, strat_auc  # noqa: E402

from score import EV2_PAIRWISE, jl  # noqa: E402

EXP5_PREREG = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/prereg.json")


def run() -> dict:
    frame = {r["row_key"]: r for r in jl(ROOT / "data" / "frame_blind.jsonl")}
    lab = {r["row_key"]: r["y"] for r in jl(ROOT / "data" / "labels_RAB.jsonl")}
    neutral = json.loads(EXP5_PREREG.read_text())["imputation"]["neutral"]["c_score_align"]
    fam_stats = {}
    with open(EV2_PAIRWISE) as fh:
        for line in fh:
            sm = SentenceMatrix(json.loads(line))
            for rk in sm.row_meta:
                if rk in frame:
                    rc = row_consensus(sm, rk, "family")
                    fam_stats[rk] = rc["fam_stats"] if rc else None
    keys = sorted(frame)
    y = np.array([lab[k] for k in keys])
    st = np.array([frame[k]["stratum"] for k in keys])
    pool = ("deepseek", "microsoft", "openai")
    s = []
    for k in keys:
        fs = fam_stats.get(k)
        v = c_from_fams(fs, [f for f in pool if f != frame[k]["family"]]) if fs is not None else None
        s.append(neutral if v is None else v)
    s = np.array(s, float)
    a, sa = auc(y, s), strat_auc(y, s, st)
    c_al = np.array([frame[k]["T1__c_score_align"] for k in keys], float)
    out = {"m4_pool_deepseek+microsoft+openai": {"auroc": a, "strat_auroc": sa, "target_auroc": 0.784520131776288,
                                                  "target_strat": 0.7426532918903646,
                                                  "pass": abs(sa - 0.7426532918903646) <= 0.01 and abs(a - 0.784520131776288) <= 0.01,
                                                  "neutral": neutral, "n": len(keys)},
           "T1_c_score_align": {"auroc": auc(y, c_al), "strat_auroc": strat_auc(y, c_al, st), "target_auroc": 0.782,
                                "target_strat": 0.741, "pass": abs(auc(y, c_al) - 0.782) < 0.0015 and abs(strat_auc(y, c_al, st) - 0.741) < 0.0015}}
    (ROOT / "results" / "repro_checks.json").write_text(json.dumps(out, indent=1))
    logger.info(out)
    return out


if __name__ == "__main__":
    run()
