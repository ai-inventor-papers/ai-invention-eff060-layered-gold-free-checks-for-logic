"""consensus_variants (frozen freeze copy): hand-computed values on synthetic peer matrices, and the leave-own-family-out
rule over the 10 E2 slots (G1/G1b meta and G5/G8 google share a family)."""
import sys
from pathlib import Path
WS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WS / "freeze_copy"))
import consensus_variants as CV  # noqa: E402

FAM = {"G1": "meta", "G1b": "meta", "G2": "qwen", "G3": "mistral", "G4": "deepseek", "G5": "google", "G8": "google",
       "G6": "microsoft", "G7": "openai", "G9": "cohere"}


def rec(groups, eqs=()):
    """groups: list of node -> list of slots; eqs: extra equal node pairs (kind 'align')."""
    nodes, n = [], 0
    for i, slots in enumerate(groups):
        nodes.append({"node_id": i, "rows": [{"row_key": s, "slot": s, "family": FAM[s], "family_field": FAM[s], "is_peer": True} for s in slots]})
    pairs = []
    for i in range(len(groups)):
        for j in range(i + 1, len(groups)):
            pairs.append([i, j, (i, j) in eqs, "align" if (i, j) in eqs else "none", 0.0])
    return {"sentence_id": "x", "nodes": nodes, "pairs": pairs}


def test_lofo_and_v0():
    I = CV.build_index(rec([["G1", "G2", "G3"], ["G1b", "G4"], ["G5", "G6", "G7", "G8", "G9"]]))
    P = CV.peers_lofo(I, "G1")
    assert "G1b" not in P and "G1" not in P and len(P) == 8
    # G1's node = {G1,G2,G3}; agreeing peers among P: G2, G3 -> V0 = 1 - 2/8
    assert abs(CV.c_score_align(I, "G1") - 0.75) < 1e-12
    P5 = CV.peers_lofo(I, "G5")
    assert "G8" not in P5 and len(P5) == 8


def test_align_equivalence_counts():
    I = CV.build_index(rec([["G1", "G2"], ["G3", "G4"], ["G5", "G6", "G7", "G8", "G9", "G1b"]], eqs={(0, 1)}))
    # G2 peers: all but G2 (qwen) -> 9; agree: G1, G3, G4 (node 1 eq node 0) -> 1 - 3/9
    assert abs(CV.c_score_align(I, "G2") - (1 - 3 / 9)) < 1e-12
    # exact agreement ignores 'align'-kind equivalences -> only G1
    assert abs(CV.c_exact(I, "G2") - (1 - 1 / 9)) < 1e-12


def test_two_channel():
    v = CV.c_two_channel(0.5, 0.25, {"intercept": 0.0, "c_exact": 2.0, "c_align": 4.0})
    import math
    assert abs(v - 1 / (1 + math.exp(-2.0))) < 1e-12
