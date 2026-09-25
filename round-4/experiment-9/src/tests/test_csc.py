"""Unit tests for src/csc.py (run: PYTHONHASHSEED=0 .venv/bin/python -m pytest -q tests)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import csc  # noqa: E402

# (a, b, expected equivalence under (lowercased name, arity) identity)
PAIRS = [
    ("∀x (A(x) → B(x))", "∀y (A(y) → B(y))", True),                       # variable renaming
    ("∀x (A(x) → B(x))", "∀x (¬B(x) → ¬A(x))", True),                     # contrapositive
    ("¬(A(c) ∧ B(c))", "¬A(c) ∨ ¬B(c)", True),                            # De Morgan
    ("∀x (A(x) ∧ C(x) → B(x))", "∀x (C(x) ∧ A(x) → B(x))", True),         # conjunct reordering
    ("∀x (A(x) → (C(x) → B(x)))", "∀x ((A(x) ∧ C(x)) → B(x))", True),     # exportation
    ("Likes(john, mary)", "Likes(John, Mary)", True),                     # case-insensitive names
    ("∃x (Dog(x) ∧ Barks(x))", "∃y (Barks(y) ∧ dog(y))", True),           # case + reordering
    ("∀x (A(x) → B(x))", "∀x (A(x) → B(x)) ∧ (P(c) ∨ ¬P(c))", True),     # extra tautological conjunct is idle
    ("A(c) ⊕ B(c)", "(A(c) ∨ B(c)) ∧ ¬(A(c) ∧ B(c))", True),              # xor expansion
    ("∀x ∀y (R(x, y) → S(y, x))", "∀y ∀x (R(y, x) → S(x, y))", True),     # bound-variable swap
    ("∀x (A(x) → B(x))", "∀x (B(x) → A(x))", False),                      # converse
    ("∀x (A(x) → B(x))", "∃x (A(x) ∧ B(x))", False),                      # quantifier
    ("∀x (A(x) → B(x))", "∀x (A(x) → ¬B(x))", False),                     # polarity
    ("∀x (A(x) → B(x))", "∀x (Aa(x) → B(x))", False),                     # predicate rename = different symbol
    ("A(c)", "A(c, d)", False),                                           # arity clash
    ("∀x (A(x) ∧ C(x) → B(x))", "∀x (A(x) → B(x))", False),               # dropped condition
    ("R(a, b)", "R(b, a)", False),                                        # swapped arguments
    ("∀x (A(x) → B(x) ∧ C(x))", "∀x (A(x) → B(x))", False),               # dropped conclusion conjunct
    ("A(c)", "A(d)", False),                                              # different constant
    ("∀x (A(x) → B(x))", "∀x (A(x) → B(x) ∨ C(x))", False),               # added disjunct
]


@pytest.mark.parametrize("a,b,exp", PAIRS)
def test_known_pairs(a, b, exp):
    assert csc.exact_equiv(a, b) is exp


def test_unparseable():
    assert csc.exact_equiv("∀x (A(x) →", "A(c)") is None
    assert csc.norm_canon("") is None


def test_signature():
    s = csc.extract_signature("∀x ((Car(x) ∧ MadeIn(x, maranello)) → Carry(x, ferrariV12Engine))")
    assert [(n, a) for n, a, _ in s] == [("car", 1), ("carry", 2), ("ferrariv12engine", 0), ("madein", 2), ("maranello", 0)]
    assert csc.extract_signature("∀x (Dog(x) → ∃y (Owner(y, x)))") == [("dog", 1, "Dog"), ("owner", 2, "Owner")]
    assert csc.extract_signature("Rain") == [("rain", 0, "Rain")]
    assert csc.extract_signature("not a formula (((") is None


def test_order_determinism():
    s = csc.extract_signature("∀x ((A(x) ∧ B(x, c)) → D(x))")
    o1, o2 = csc.order_symbols("A sentence.", s), csc.order_symbols("A sentence.", s)
    assert o1 == o2 and sorted(o1) == sorted(["A/1", "B/2", "c/0", "D/1"])
    m1, m2 = csc.build_prompt("A sentence.", o1), csc.build_prompt("A sentence.", o2)
    assert json.dumps(m1) == json.dumps(m2)
    assert csc.prompt_key("m", m1) == csc.prompt_key("m", m2)
    base = csc.load_prompt()
    assert m1[0]["content"] == base["system"] and m1[1:-1] == base["exemplars"]
    assert m1[-1]["content"].startswith("Sentence: A sentence.\n\nSymbols from another translation")


def test_peer_family_rule():
    systems = ["G1:meta-llama/llama-3.1-8b-instruct", "G1b:meta-llama/llama-3.3-70b-instruct", "G2:qwen/qwen3-235b-a22b-2507",
               "G3:mistralai/mistral-small-3.2-24b-instruct", "G4:deepseek/deepseek-v3.2", "G5:google/gemma-3-27b-it",
               "G6:microsoft/phi-4", "G7:openai/gpt-4.1-mini", "G8:google/gemini-2.5-flash", "G9:cohere/command-r7b-12-2024",
               "F:openai/gpt-5.1"]
    for s in systems:
        fam = csc.family_of(s)
        peers = csc.peers_for(fam, 3)
        assert len(peers) == 3 and all(p[1] != fam for p in peers), s
    assert [p[1] for p in csc.peers_for("openai")] == ["deepseek", "microsoft", "qwen"]
    assert [p[1] for p in csc.peers_for("meta")] == ["deepseek", "microsoft", "openai"]
    assert len(csc.peers_for("meta", 4)) == 4


def test_consensus_edge_cases():
    cand = "∀x (A(x) → B(x))"
    eq = {"fol": "∀y (¬B(y) → ¬A(y))", "alt_fol": None}
    ne = {"fol": "∀y (B(y) → A(y))", "alt_fol": None}
    bad = {"fol": "((", "alt_fol": None}
    r0 = csc.consensus_score(cand, [])
    assert r0["status"] == "csc_insufficient_peers" and r0["c_csc"] == 0.5
    r1 = csc.consensus_score(cand, [eq, bad])
    assert r1["status"] == "csc_insufficient_peers" and r1["n_unparseable_peers"] == 1
    r2 = csc.consensus_score(cand, [eq, ne])
    assert r2["c_csc"] == 0.5 and r2["n_usable"] == 2
    r3 = csc.consensus_score(cand, [eq, eq, ne])
    assert abs(r3["c_csc"] - 1 / 3) < 1e-9
    ru = csc.consensus_score("((", [eq, eq, ne])
    assert ru["status"] == "UNPARSEABLE" and ru["c_csc"] == 1.0
    # multi: peer 2 gives the candidate as alt_fol, and peer 3 produces that reading too
    m = csc.consensus_score(cand, [ne, {"fol": "∀y (B(y) → A(y))", "alt_fol": "∀x (A(x) → B(x))"}, {"fol": "∀x (A(x) → B(x))", "alt_fol": None}])
    assert abs(m["c_csc"] - 2 / 3) < 1e-9 and abs(m["c_csc_multi"] - 1 / 3) < 1e-9


def test_parse_response_routes():
    assert csc.parse_response('{"fol": "A(c)", "alt_fol": null}')["route"] == "json"
    assert csc.parse_response('```json\n{"fol": "A(c)", "alt_fol": "B(c)"}\n```')["alt_fol"] == "B(c)"
    assert csc.parse_response("FOL: A(c)")["route"] == "fol_line"
    assert csc.parse_response("")["fol"] is None


def test_typed_repair_same_vocab():
    r = csc.typed_repair_same_vocab("∀x (A(x) ∧ C(x) → B(x))", "∀x (A(x) → B(x))")
    assert r["cls"] != "PARSE_FAIL" and r["ops"]
    assert csc.typed_repair_same_vocab("∀x (A(x) → B(x))", "∀y (A(y) → B(y))")["cls"] == "EQUIV"
