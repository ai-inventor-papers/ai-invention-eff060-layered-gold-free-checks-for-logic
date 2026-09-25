"""Unit tests: the bookkeeping identity AUROC_b = 1 - (e + d)/2, the weighted (bootstrap-multiplicity) AUROC, the graded
trace trapezoid check, and the eqmv matrix readouts on a hand-built sentence."""
import sys
from pathlib import Path

import numpy as np
import pytest
from sklearn.metrics import roc_auc_score

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from consensus_mx import SentenceMatrix, c_from_fams, row_consensus  # noqa: E402
from mechanism import ed_decomposition, graded_trace  # noqa: E402
from stats import WAuc, WStratAuc, auc, strat_auc  # noqa: E402


@pytest.mark.parametrize("seed", range(20))
def test_identity_random(seed):
    rng = np.random.default_rng(seed)
    n = rng.integers(20, 400)
    y = rng.integers(0, 2, n)
    y[0], y[1] = 0, 1
    en = rng.integers(0, 2, n)
    r = ed_decomposition(y, en)
    assert abs(r["auroc_b"] - roc_auc_score(y, 1 - en)) < 1e-12
    assert abs(r["auroc_b"] - (1 - (r["e"] + r["d"]) / 2)) < 1e-12


def test_weighted_auc_equals_duplication():
    rng = np.random.default_rng(1)
    y = rng.integers(0, 2, 200)
    s = np.round(rng.random(200), 1)  # many ties
    w = rng.integers(0, 4, 200)
    rep = np.repeat(np.arange(200), w)
    assert abs(WAuc(y, s)(w) - roc_auc_score(y[rep], s[rep])) < 1e-12
    assert abs(auc(y, s) - roc_auc_score(y, s)) < 1e-12
    st = rng.choice(["A", "B", "C"], 200)
    assert abs(WStratAuc(y, s, st)(np.ones(200)) - strat_auc(y, s, st)) < 1e-12


def test_graded_trace_area():
    rng = np.random.default_rng(2)
    y = rng.integers(0, 2, 300)
    c = np.round(rng.random(300) * 10) / 10
    g = graded_trace(y, c)
    assert abs(g["trapezoid_area"] - roc_auc_score(y, c)) < 1e-9


def test_row_consensus_toy():
    # nodes 0..2; 0~1 True, 1~2 True, 0!~2 (non-transitive); peers from 3 families
    rec = {"sentence_id": "s", "nodes": [
        {"node_id": 0, "canon_fol": "a", "rows": [{"row_key": "r0", "slot": "G1", "family": "meta", "family_field": "meta", "system_class": "llm", "is_peer": True}]},
        {"node_id": 1, "canon_fol": "b", "rows": [{"row_key": "r1", "slot": "G2", "family": "qwen", "family_field": "qwen", "system_class": "llm", "is_peer": True},
                                                  {"row_key": "r1b", "slot": "G3", "family": "mistral", "family_field": "mistral", "system_class": "llm", "is_peer": True}]},
        {"node_id": 2, "canon_fol": "c", "rows": [{"row_key": "r2", "slot": "GOLD", "family": "gold_as_system_never_peer", "family_field": "x", "system_class": "gold", "is_peer": False}]}],
        "pairs": [[0, 1, True, "align", 0.1], [0, 2, False, "none", 0.1], [1, 2, True, "exact", 0.1]]}
    sm = SentenceMatrix(rec)
    assert sm.nontransitive() == (1, 1)
    r = row_consensus(sm, "r0")
    assert r["npc"] == 2 and r["n_eq"] == 2 and r["n_eq_exact"] == 0 and r["c_re"] == 0.0 and r["end_maj"] and r["end_fam2"]
    g = row_consensus(sm, "r2")  # GOLD candidate: peers r0, r1, r1b
    assert g["npc"] == 3 and g["n_eq"] == 2 and abs(g["c_re"] - 1 / 3) < 1e-12 and g["n_eq_exact"] == 2
    assert c_from_fams(g["fam_stats"], ["meta"]) == 1.0 and c_from_fams(g["fam_stats"], ["qwen"]) == 0.0
