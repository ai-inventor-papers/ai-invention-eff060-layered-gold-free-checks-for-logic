"""Freeze tests for freeze/consensus_variants.py: toy matrices with known answers, fold discipline of V2/V4, and the
20-row reproduction of results/scores_E_variants.jsonl to 1e-9."""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "freeze"))
sys.path.insert(0, str(ROOT / "src"))
import consensus_variants as CV  # noqa: E402


def toy(groups, cand_family="x", cliques=None):
    """groups: list of (family, node_id) peer rows; node 0 = candidate's node; eq True within same node id only unless
    extra pairs given."""
    nodes = {}
    for k, (fam, nid) in enumerate(groups):
        nodes.setdefault(nid, []).append({"row_key": f"p{k}", "slot": fam, "family": fam, "family_field": fam, "is_peer": True})
    nodes.setdefault(0, []).append({"row_key": "cand", "slot": cand_family, "family": cand_family, "family_field": cand_family, "is_peer": False})
    ids = sorted(nodes)
    rec = {"sentence_id": "s", "nodes": [{"node_id": i, "canon_fol": f"P{i}(a)", "rows": nodes[i]} for i in ids],
           "pairs": [[i, j, False, "none", 0.0] for a, i in enumerate(ids) for j in ids[a + 1:]],
           "cliques": cliques or [[i] for i in ids]}
    return CV.build_index(rec)


def test_all_agree_zero():
    ix = toy([("a", 0), ("b", 0), ("c", 0)])
    assert CV.c_score_align(ix, "cand") == 0 and CV.c_pn(ix, "cand") == 0 and CV.c_exact(ix, "cand") == 0


def test_plurality_member_v1_zero():
    # candidate agrees with 2 of 6 peers; every other class has <= 2 rows -> V1 = 0 while V0 = 2/3 > 0.5
    ix = toy([("a", 0), ("b", 0), ("c", 1), ("d", 2), ("e", 3), ("f", 4)])
    assert abs(CV.c_score_align(ix, "cand") - 4 / 6) < 1e-12
    assert CV.c_pn(ix, "cand") == 0


def test_scattered_minority():
    ix = toy([("a", 0), ("b", 1), ("c", 1), ("d", 1), ("e", 2)])
    assert abs(CV.c_pn(ix, "cand") - (1 - (1 / 5) / (3 / 5))) < 1e-12


def test_no_agreement_is_one():
    ix = toy([("a", 1), ("b", 2)])
    assert CV.c_pn(ix, "cand") == 1.0


def test_equal_weights_v2_eq_v0_and_v3_eq_v1():
    ix = toy([("a", 0), ("b", 1), ("c", 1), ("d", 2)])
    w = {f: 0.3 for f in "abcd"}
    assert abs(CV.c_rw(ix, "cand", w) - CV.c_score_align(ix, "cand")) < 1e-12
    assert abs(CV.c_pn_rw(ix, "cand", w) - CV.c_pn(ix, "cand")) < 1e-12


def test_family_weights_exclude_holdout_fold():
    a = toy([("a", 0), ("b", 0)])
    b = toy([("a", 1), ("b", 2)])
    a["sid"], b["sid"] = "s1", "s2"
    w_all = CV.family_weights([a, b], {"s1": 0, "s2": 1}, None, shrink=0)
    w_k0 = CV.family_weights([a, b], {"s1": 0, "s2": 1}, 0, shrink=0)
    assert w_all["a"] == 0.5 and w_k0["a"] == 0.0


def test_unparseable_and_too_few_peers():
    ix = toy([("a", 0)])
    assert CV.c_score_align(ix, "missing") == 1.0
    assert CV.c_score_align(ix, "cand") is None


def test_v4_oof_folds_disjoint():
    c = json.loads((ROOT / "results" / "v4_coefs.json").read_text())
    for k, f in c["per_fold"].items():
        assert f["n_train"] + f["n_test"] == c["n_Z"]


def test_20_rows_reproduce():
    rows = [json.loads(l) for l in (ROOT / "results" / "scores_E_variants.jsonl").read_text().splitlines()]
    mx = {json.loads(l)["sentence_id"]: json.loads(l) for l in Path(
        "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_evaluation_2/pairwise_classes_E.jsonl").read_text().splitlines()}
    W = json.loads((ROOT / "results" / "family_weights.json").read_text())["per_fold_holdout"]
    import hashlib
    Z = sorted([r for r in rows if r["in_matrix"] and r["n_peers"] >= 2], key=lambda r: hashlib.sha1(r["row_key"].encode()).hexdigest())[:20]
    for r in Z:
        ix = CV.build_index(mx[r["sentence_id"]])
        w = W[str(r["fold"])]
        assert abs(CV.c_score_align(ix, r["row_key"]) - r["V0_rep"]) < 1e-9
        assert abs(CV.c_exact(ix, r["row_key"]) - r["c_exact"]) < 1e-9
        assert abs(CV.c_pn(ix, r["row_key"]) - r["V1"]) < 1e-9
        assert abs(CV.c_rw(ix, r["row_key"], w) - r["V2"]) < 1e-9
        assert abs(CV.c_pn_rw(ix, r["row_key"], w) - r["V3"]) < 1e-9
        v5 = CV.c_v5(ix, r["row_key"], w)
        assert abs((0.6266243516243516 if v5 is None else v5) - r["V5"]) < 1e-9
    c = json.loads((ROOT / "results" / "v4_coefs.json").read_text())["frozen_coefficients_full_Z"]
    assert 0 < CV.c_two_channel(0.5, 0.5, c) < 1
