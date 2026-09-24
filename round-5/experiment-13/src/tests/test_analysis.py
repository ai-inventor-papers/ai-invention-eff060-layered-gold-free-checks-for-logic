"""Analysis code tests run BEFORE the join (testing plan item 11): synthetic sanity and the SIG G0 reproduction through
confirm/analysis_lib (no FREE label is read here)."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "confirm"))
import analysis_lib as AL  # noqa: E402
from cc import E7, jl, load_scores  # noqa: E402


def _synthetic(n_sent=60, per=8, seed=0):
    rng = np.random.default_rng(seed)
    rows = []
    for s in range(n_sent):
        t = f"T{s % 3}"
        for k in range(per):
            y = float(rng.random() < 0.4)
            rows.append({"sentence_id": f"s{s}", "template_id": t, "y": y, "perfect": y + 0.01 * rng.random(), "reversed": -y,
                         "random": rng.random(), "fold": s % 5})
    d = pd.DataFrame(rows)
    return d, AL.Boot(sorted(d.sentence_id.unique()), dict(zip(d.sentence_id, d.template_id)), 200, 1)


def test_synthetic_auroc():
    d, b = _synthetic()
    assert abs(AL.auc_block(d, "perfect", b)["est"] - 1.0) < 1e-12
    assert abs(AL.auc_block(d, "reversed", b)["est"] - 0.0) < 1e-12
    r = AL.auc_block(d, "random", b)
    assert 0.35 < r["est"] < 0.65 and r["ci"][0] < 0.5 < r["ci"][1]
    pdl = AL.paired_delta(d, "perfect", "random", b)
    assert pdl["ci"][0] > 0


def test_holm():
    adj = AL.holm({"a": 0.01, "b": 0.04, "c": 0.03})
    assert abs(adj["a"] - 0.03) < 1e-12 and abs(adj["c"] - 0.06) < 1e-12 and abs(adj["b"] - 0.06) < 1e-12


def test_nested_runs():
    d, b = _synthetic()
    r = AL.nested_block(d, ["random"], ["perfect"], b, n_perm=3)
    assert r["delta"] > 0.2


def test_sig_reproduction():
    rows = load_scores("SIG")
    lab = {r["row_key"]: r["label"] for r in jl(E7 / "results/sig_labels.jsonl")}
    P = pd.DataFrame([r for r in rows if lab.get(r["row_key"]) in ("CORRECT", "ERROR") and r["c_score_sig"] is not None
                      and r["judge_cheap_disg"] is not None])
    P["y"] = [float(lab[k] == "ERROR") for k in P.row_key]
    b = AL.Boot(sorted(P.sentence_id.unique()), dict(zip(P.sentence_id, P.template_id)), 50, 20260924)
    assert abs(AL.auc_block(P, "c_score_sig", b, with_boot=False)["est"] - 0.954340046099721) < 1e-9
    assert abs(AL.auc_block(P, "judge_cheap_disg", b, with_boot=False)["est"] - 0.5872179424966638) < 1e-9
