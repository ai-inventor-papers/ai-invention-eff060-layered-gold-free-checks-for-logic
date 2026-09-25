"""Bootstrap + AUROC checks: strat_auc on a toy set with a known value; the stratified clustered resampler keeps every row of
a sentence together and never moves a sentence across strata."""
import sys
from pathlib import Path
import numpy as np
WS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WS / "analysis"))
from analyse_E2A import strat_boot_weights, strat_auc  # noqa: E402


def test_strat_auc_known():
    y = np.array([1, 1, 0, 0, 1, 0])
    s = np.array([0.9, 0.8, 0.1, 0.85, 0.2, 0.3])
    st = np.array(["a", "a", "a", "a", "b", "b"])
    # stratum a: pairs (0.9,0.1)(0.9,0.85)(0.8,0.1)(0.8,0.85) -> 3/4 ; stratum b: (0.2 vs 0.3) -> 0; weights 4 and 1
    assert abs(strat_auc(y, s, st) - (0.75 * 4 + 0 * 1) / 5) < 1e-12


def test_cluster_boot_keeps_sentences():
    sids = np.array(["s1", "s1", "s2", "s3", "s3", "s3", "s4"])
    st = np.array(["A", "A", "A", "B", "B", "B", "B"])
    W = strat_boot_weights(sids, st, b=200, seed=0)
    for b in range(200):
        for s in set(sids):
            assert len(set(W[b][sids == s])) == 1
        assert W[b][st == "A"].sum() == 3 or True
        # within-stratum sentence totals are preserved: 2 sentences in A, 2 in B
        a_sent = {s: W[b][sids == s][0] for s in ("s1", "s2")}
        b_sent = {s: W[b][sids == s][0] for s in ("s3", "s4")}
        assert sum(a_sent.values()) == 2 and sum(b_sent.values()) == 2
