# NOTE (published copy): this file names server paths this repository
# does not publish (a stage it does not ship, or another run's workspace),
# so the steps that read them will not run from a clone as written:
#   /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/perturb_scores.jsonl
"""GG search unit tests: synthetic pairs, identity-map recovery on RENAME_SYN controls vs their base (z3-equivalent by
construction), map found for MEANING_RENAME mutants (the gloss must reject them), gloss decision rule and parser."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "freeze"))
import gg  # noqa: E402

PS = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/results/perturb_scores.jsonl")


def test_synthetic():
    s = gg.gg_map_search("∀x ∀y (Loves(x, y) → Happy(x))", "∀x ∀y (Adores(x, y) → Happy(x))")
    assert s["status"] == "MAPPED" and s["maps"][0]["nonidentity"][0][1:3] == ("Loves/2", "Adores/2")
    assert gg.gg_map_search("∀x ∀y (Loves(x, y) → Happy(x))", "∀x ∀y (Loves(y, x) → Happy(x))")["status"] == "NO_MAP"
    assert gg.gg_map_search("∀x (A(x) → B(x))", "∀x (C(x) ∧ D(x) → E(x))")["status"].startswith("PREFILTER")
    s = gg.gg_map_search("∀x (Cat(x) → ¬Dog(x))", "∀x (Dog(x) → ¬Cat(x))")
    assert any(not m["nonidentity"] for m in s["maps"])  # identity map (contrapositive) found


def test_decision_rule():
    s = {"maps": [{"nonidentity": [("pred", "A/1", "B/1", "A(x)", "B(x)")]}, {"nonidentity": []}]}
    assert gg.gg_decision(s, {})[0] is True
    s = {"maps": [{"nonidentity": [("pred", "A/1", "B/1", "A(x)", "B(x)")]}]}
    assert gg.gg_decision(s, {gg.pair_key(("pred", "A/1", "B/1")): "YES"}) == (True, 0)
    assert gg.gg_decision(s, {gg.pair_key(("pred", "A/1", "B/1")): "NO"}) == (False, None)
    assert gg.parse_verdicts('{"1": "YES", "2": "no"}', 2) == {1: "YES", 2: "NO"}
    assert gg.parse_verdicts('{"1": "YES"}', 2) is None


def test_rename_syn_and_meaning_rename_maps():
    rows = [json.loads(l) for l in PS.read_text().splitlines()]
    base = {r["base"]: r for r in rows if r["control_type"] == "BASE"}
    syn = [r for r in rows if r["control_type"] == "RENAME_SYN" and r["base"] in base][:20]
    for r in syn:
        s = gg.gg_map_search(r["fol"], base[r["base"]]["fol"])
        assert s["status"] == "MAPPED", (r["fol"], base[r["base"]]["fol"], s["status"])
    mr = [r for r in rows if r["operator"] == "MEANING_RENAME" and r["base"] in base][:20]
    found = sum(gg.gg_map_search(r["fol"], base[r["base"]]["fol"])["status"] == "MAPPED" for r in mr)
    assert found >= 18
