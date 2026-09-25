"""Unit tests for src/csc_lib.py (run: .venv/bin/python -m pytest -q tests/test_csc_lib.py)."""
from __future__ import annotations

import json
import os
import random
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import csc_lib as L  # noqa: E402
import views as DV  # noqa: E402

VIEW = ROOT / "data" / "perturb_view.jsonl"


def _view():
    if not VIEW.exists():
        pytest.skip("data view not built")
    return [json.loads(x) for x in VIEW.read_text().splitlines() if x.strip()]


# ------------------------------------------------------------------ signatures
def test_signature_predicates_and_constants():
    sig = L.extract_signature("∀x (Student(x) ∧ TeachesAt(x, harvard) → Smart(x))")
    assert ("Student", 1) in sig and ("TeachesAt", 2) in sig and ("harvard", 0) in sig and ("Smart", 1) in sig
    assert all(n != "x" for n, _ in sig)


def test_signature_propositional_atom_and_free_constant():
    sig = L.extract_signature("Raining → ¬Dry(ground)")
    assert ("Raining", 0) in sig and ("ground", 0) in sig and ("Dry", 1) in sig


def test_signature_excludes_bound_variables_nested():
    sig = L.extract_signature("∀x ∃y (Loves(x, y) ∧ Person(y))")
    assert sorted(sig) == [("Loves", 2), ("Person", 1)]


def test_signature_arity_distinguishes():
    sig = L.extract_signature("∀x (P(x) → P(x, a))")
    assert ("P", 1) in sig and ("P", 2) in sig


def test_signature_unparseable_empty():
    assert L.extract_signature("∀x (P(x) →") == []


# ------------------------------------------------------------------ prompt
def test_shuffle_determinism_same_bytes():
    sig = L.extract_signature("∀x (A(x) ∧ B(x) ∧ C(x) ∧ D(x) → E(x, k))")
    m1 = L.csc_prompt("Every A that is B, C and D is E of k.", sig)
    m2 = L.csc_prompt("Every A that is B, C and D is E of k.", list(reversed(sig)))
    assert json.dumps(m1, ensure_ascii=False) == json.dumps(m2, ensure_ascii=False)


def test_shuffle_is_permutation_and_varies():
    sig = [(f"Pred{i}", 1) for i in range(8)]
    orders = set()
    for t in ("s1", "s2", "s3", "s4", "s5"):
        blk = L.symbols_block(t, sig)
        items = blk.split("random order): ", 1)[1].split(". Use", 1)[0].split(", ")
        assert sorted(items) == sorted(f"Pred{i}/1" for i in range(8))
        orders.add(tuple(items))
    assert len(orders) > 1


def test_prompt_prefix_identical_to_dataset_e():
    pr = json.loads(L.PROMPT_PATH.read_text())
    m = L.csc_prompt("All dogs bark.", [("Dog", 1), ("Bark", 1)])
    assert m[0] == {"role": "system", "content": pr["system"]}
    assert m[1:-1] == pr["exemplars"]
    assert m[-1]["content"].startswith("Sentence: All dogs bark.\n\nSymbols from another translation of this sentence")
    assert m[-1]["content"].endswith('Return JSON {"fol": <formula>, "alt_fol": <a formula for a second legitimate reading, or null>}.')


def test_prompt_bytes_stable_across_processes():
    code = ("import sys,json;sys.path.insert(0,'src');import csc_lib as L;"
            "print(json.dumps(L.csc_prompt('Every A is B.', [('A',1),('B',1),('c',0),('D',2)]), ensure_ascii=False))")
    outs = set()
    for seed in ("1", "2"):
        env = {**os.environ, "PYTHONHASHSEED": seed}
        outs.add(subprocess.run([sys.executable, "-c", code], cwd=ROOT, env=env, capture_output=True, text=True).stdout)
    assert len(outs) == 1 and len(next(iter(outs))) > 100


# ------------------------------------------------------------------ equivalence
def test_lowercase_match():
    assert L.eq_exact("∀x (Dog(x) → Bark(x))", "∀y (dog(y) → BARK(y))") is True


def test_nonequivalent_detected():
    assert L.eq_exact("∀x (Dog(x) → Bark(x))", "∃x (Dog(x) ∧ Bark(x))") is False


def test_different_names_not_equivalent():
    assert L.eq_exact("∀x (Dog(x) → Bark(x))", "∀x (Canine(x) → Bark(x))") is False


def test_fp_prefilter_never_rejects_equivalent_controls():
    rows = _view()
    base = {r["base_item_id"]: r for r in rows if r["fold"] == "BASE"}
    ctl = [r for r in rows if r["control_type"] in ("REORDER_COMMUTE", "REORDER_QUANT", "CONTRAPOSITIVE", "DEMORGAN")]
    rng = random.Random(0)
    sample = rng.sample(ctl, min(200, len(ctl)))
    bad = []
    for r in sample:
        a, b = L.prep(r["candidate_fol"]), L.prep(base[r["base_item_id"]]["candidate_fol"])
        if a[2] != b[2]:
            bad.append(r["key"])
    assert not bad, bad[:5]
    ok = sum(L.eq_exact(r["candidate_fol"], base[r["base_item_id"]]["candidate_fol"]) is True for r in sample[:60])
    assert ok == len(sample[:60])


# ------------------------------------------------------------------ scores
def test_synonym_renamed_candidate_with_synonym_peers_is_endorsed():
    cand = "∀x (Canine(x) → Barks(x))"
    peers = ["∀y (Canine(y) → Barks(y))", "∀x (canine(x) → barks(x))", "∀x ¬(Canine(x) ∧ ¬Barks(x))"]
    assert L.consensus_score("All dogs bark.", cand, peers)["c"] == 0.0


def test_meaning_rename_vs_base_peers_not_endorsed():
    cand = "∀x (AreaOfLandSaturatedWithWater(x) → Sad(x))"
    peers = ["∀x (Depressing(x) → Sad(x))"] * 3
    r = L.consensus_score("When something is depressing, it is sad.", cand, peers)
    assert r["c"] == 1.0 and r["c"] > 0.5


def test_insufficient_peers_flag():
    r = L.consensus_score("t", "∀x (A(x) → B(x))", ["∀x (A(x) → B(x))", None, "∀x (A(x) →"])
    assert r["c"] == 0.5 and r["status"] == "csc_insufficient_peers"


def test_unparseable_candidate_coverage_view():
    r = L.consensus_score("t", "∀x (A(x) →", ["∀x (A(x) → B(x))"] * 3)
    assert r["c"] == 1.0 and r["status"] == "UNPARSEABLE"


def test_unknown_counted_not_agreement(monkeypatch):
    monkeypatch.setattr(L, "eq_prepped", lambda a, b, ms=2000: None)
    r = L.consensus_score("t", "∀x (A(x) → B(x))", ["∀x (A(x) → B(x)) ∧ C(k)", "∀x (B(x))", "∀x (A(x))"])
    assert r["n_unknown"] == 3 and r["c"] == 1.0


def test_multi_reading_requires_second_peer():
    cand = "∀x (A(x) → B(x))"
    lone = [{"fol": "∀x (A(x) ∧ C(x) → B(x))", "alt_fol": cand}, {"fol": "∀x (D(x))", "alt_fol": None},
            {"fol": "∀x (E(x))", "alt_fol": None}]
    assert L.csc_multi_score("t", cand, lone)["c"] == 1.0
    corro = [{"fol": "∀x (A(x) ∧ C(x) → B(x))", "alt_fol": cand}, {"fol": "∀x (D(x))", "alt_fol": "∀y (A(y) → B(y))"},
             {"fol": "∀x (E(x))", "alt_fol": None}]
    r = L.csc_multi_score("t", cand, corro)
    assert r["n_alt_endorse"] == 2 and abs(r["c"] - 1 / 3) < 1e-9


def test_graded_identity_equal_is_zero_and_drop_is_positive():
    peers = ["∀x (A(x) ∧ C(x) → B(x))"] * 3
    assert L.graded_consensus("t", "∀x (A(x) ∧ C(x) → B(x))", peers)["g"] == pytest.approx(0.0)
    g = L.graded_consensus("t", "∀x (A(x) → B(x)) ∧ D(k)", peers)["g"]
    assert g is not None and g > 0


def test_peer_majority():
    p = ["∀x (A(x) → B(x))", "∀y (a(y) → b(y))", "∃x (A(x) ∧ B(x))"]
    m = L.peer_majority(p)
    assert m["status"] == "MAJORITY" and m["formula"] == p[0]
    assert L.peer_majority(["∀x A(x)", "∀x B(x)", "∀x C(x)"])["status"] == "NO_MAJORITY"


def test_symbol_usage():
    sig = [("Dog", 1), ("Bark", 1), ("Zorp", 1)]
    u = L.symbol_usage(sig, ["∀x (dog(x) → Bark(x))", None])
    assert u == [[True], [True], [False]]


# ------------------------------------------------------------------ parser
RAW = [
    ('{"fol": "∀x (A(x) → B(x))", "alt_fol": null}', "json", "∀x (A(x) → B(x))", None),
    ('```json\n{"fol": "∀x (A(x) → B(x))", "alt_fol": "∃x A(x)"}\n```', "json", "∀x (A(x) → B(x))", "∃x A(x)"),
    ("FOL: ∀x (A(x) → B(x))", "fol_line", "∀x (A(x) → B(x))", None),
    ('Here you go:\n{"fol":"∀x (A(x) → B(x))","alt_fol":"null"}', "json", "∀x (A(x) → B(x))", None),
    ("∀x (A(x) → B(x))", "bare", "∀x (A(x) → B(x))", None),
    ("I cannot do that.", "fail", None, None),
    ("", "fail", None, None),
    ('{"formula": "x"}\nFOL: ∀x (A(x))', "fol_line", "∀x (A(x))", None),
    ('{"fol": "FOL: ∀x (A(x) → B(x))", "alt_fol": ""}', "json", "∀x (A(x) → B(x))", None),
    ('{"fol": "∀x (A(x) → B(x))", "alt_fol": "∀x (B(x) → A(x))"} trailing text', "json", "∀x (A(x) → B(x))", "∀x (B(x) → A(x))"),
]


@pytest.mark.parametrize("raw,fmt,fol,alt", RAW)
def test_parse_peer_formats(raw, fmt, fol, alt):
    r = L.parse_peer(raw)
    assert r["format"] == fmt and r["fol"] == fol and r["alt_fol"] == alt


# ------------------------------------------------------------------ typing
def test_typed_repair_known_ops_small():
    base = "∀x (A(x) ∧ C(x) → B(x))"
    assert L.typed_repair_same_vocab("∀x (A(x) ∧ C(x) → ¬B(x))", base)["ops"] == ["NEG"]
    assert L.typed_repair_same_vocab("∀x (A(x) → B(x))", base)["ops"] == ["ADD"]
    assert L.typed_repair_same_vocab("∀x (A(x) ∧ C(x) ∧ D(x) → B(x))", base)["ops"] == ["DROP"]
    assert L.typed_repair_same_vocab("∀x (A(x) ∧ Zed(x) → B(x))", base)["ops"] == ["SUBST"]


EXPECT = {"NEG": {"NEG"}, "REV": {"REV"}, "QUANT": {"QUANT"}, "RESTR": {"RESTR"}, "CONN": {"CONN", "RESTR"},
          "DROP": {"ADD", "ADD_ANY"}, "ADD": {"DROP"}, "SWAP": {"SWAP"}, "BIND": {"BIND"}, "MEANING_RENAME": {"SUBST"}}


@pytest.mark.parametrize("op", sorted(EXPECT))
def test_typed_repair_recovers_operator_against_true_base(op):
    rows = [r for r in _view() if r["fold"] == "PERTURB" and r["operator"] == op and not r["is_rcomp"]]
    rng = random.Random(1)
    sample = rng.sample(rows, min(50, len(rows)))
    hit = 0
    for r in sample:
        x = L.typed_repair_same_vocab(r["candidate_fol"], r["reference_fol"], budget_s=6)
        hit += len(x["ops"]) == 1 and x["ops"][0] in EXPECT[op]
    # depth-1 recovery against the TRUE base should be the rule; label ambiguity (e.g. NEG vs CONN) allowed.
    # DROP removes whole sub-formulas (several atoms / a whole clause) in PERTURB, which one ADD cannot restore.
    assert hit / len(sample) >= (0.4 if op == "DROP" else 0.6), (op, hit, len(sample))


# ------------------------------------------------------------------ firewall
def test_firewall_projection_raises_on_label():
    line = json.dumps({"condition": "FREE", "row_key": "k", "candidate_fol": "∀x A(x)", "label": "ERROR",
                       "family": "meta", "sentence_id": "s"})
    r = DV.project_free(line)
    assert r["row_key"] == "k"
    assert "label" not in dict.keys(r)
    with pytest.raises(DV.FirewallError):
        r["label"]
    with pytest.raises(DV.FirewallError):
        r.get("matched_reading")


def test_peer_assignment():
    a = L.peer_assignment(None)
    assert a["k3"] == ["deepseek/deepseek-v3.2", "microsoft/phi-4", "openai/gpt-4.1-mini"] and len(a["k4"]) == 4
    b = L.peer_assignment("openai")
    assert "openai/gpt-4.1-mini" not in b["k3"] and len(b["k3"]) == 3 and b["k4"] is None
