"""Unit tests for src/consensus_lib.py: 20 known pairs x modes (+ peer_pool mocked and one live smoke call).
Each case = (sentence, candidate, peer) with the expected pair verdict per mode; None in the table = 'not asserted'
(behaviour documented as a blind spot). Every case also asserts the OR identity hyb == (align or nf) and that UNKNOWN is
never agreement. Run: .venv/bin/python -m pytest tests/test_consensus_lib.py -q  (AII_LIVE=1 enables the live call)."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import consensus_lib as CL  # noqa: E402

T_DOG = "All dogs bark."
T_JM = "John loves Mary."
# name: (text, candidate, peer, {mode: expected pair verdict})
PAIRS = {
    "identity": (T_DOG, "∀x (Dog(x) → Bark(x))", "∀x (Dog(x) → Bark(x))", {"exact": True, "align": True, "nf": True, "hyb": True}),
    "full_rename_nonce": (T_DOG, "∀x (Dog(x) → Bark(x))", "∀x (Qzv(x) → Wblk(x))", {"exact": False, "align": False}),
    "synonym_rename_similar_tokens": (T_DOG, "∀x (Dog(x) → Bark(x))", "∀x (IsDog(x) → Barks(x))", {"exact": False, "align": True, "hyb": True}),
    "contrapositive": (T_DOG, "∀x (Dog(x) → Bark(x))", "∀x (¬Bark(x) → ¬Dog(x))", {"exact": True, "align": True, "nf": True, "hyb": True}),
    "de_morgan": ("John is not both tall and rich.", "¬(Tall(john) ∧ Rich(john))", "¬Tall(john) ∨ ¬Rich(john)", {"exact": True, "align": True, "hyb": True}),
    "prenex": ("Every student reads some book.", "∀x (Student(x) → ∃y (Book(y) ∧ Reads(x, y)))",
               "∀x ∃y (Student(x) → (Book(y) ∧ Reads(x, y)))", {"exact": True, "align": True, "hyb": True}),
    "reorder": ("John is tall and rich.", "Tall(john) ∧ Rich(john)", "Rich(john) ∧ Tall(john)", {"exact": True, "align": True, "nf": True, "hyb": True}),
    "meaning_rename": (T_DOG, "∀x (Dog(x) → Bark(x))", "∀x (Cat(x) → Bark(x))", {"exact": False, "align": False}),
    "swap_args": (T_JM, "Loves(john, mary)", "Loves(mary, john)", {"exact": False, "align": False, "nf": False, "hyb": False}),
    "neg": (T_DOG, "∀x (Dog(x) → Bark(x))", "∀x (Dog(x) → ¬Bark(x))", {"exact": False, "align": False, "nf": False, "hyb": False}),
    "quant": (T_DOG, "∀x (Dog(x) → Bark(x))", "∃x (Dog(x) ∧ Bark(x))", {"exact": False, "align": False, "nf": False, "hyb": False}),
    "drop": ("All big dogs bark.", "∀x ((Big(x) ∧ Dog(x)) → Bark(x))", "∀x (Dog(x) → Bark(x))", {"exact": False, "align": False, "nf": False, "hyb": False}),
    "add": (T_DOG, "∀x (Dog(x) → Bark(x))", "∀x ((Dog(x) ∧ Big(x)) → Bark(x))", {"exact": False, "align": False, "nf": False, "hyb": False}),
    "rev_role_swap": (T_DOG, "∀x (Dog(x) → Bark(x))", "∀x (Bark(x) → Dog(x))", {"exact": False, "align": False}),
    # ALIGN-only (real dataset-E pair): constant reification bridges arity 1 <-> 2; the name-free map needs equal arities
    "align_only_reification": ("John has a high salary.", "HighSalary(john)", "Salary(john, high)",
                               {"exact": False, "align": True, "nf": False, "hyb": True}),
}


@pytest.mark.parametrize("name", sorted(PAIRS))
def test_known_pairs(name):
    text, cand, peer, exp = PAIRS[name]
    got = {}
    for mode in CL.MODES:
        r = CL.consensus_score(text, cand, [peer, peer], mode=mode)  # two identical peers -> c = 0 or 1
        assert r["status"] == "OK"
        v = r["per_peer"][0]
        got[mode] = v
        assert r["n_agree"] == 2 * (v is True)  # UNKNOWN (None) never counts as agreement
        assert r["c_score"] == (0.0 if v is True else 1.0)
    for mode, e in exp.items():
        assert got[mode] is e, f"{name}: {mode} expected {e}, got {got[mode]} (all {got})"
    assert (got["hyb"] is True) == (got["align"] is True or got["nf"] is True), got  # OR identity


def test_nf_only_match_exists():
    """NF-only match: a dissimilar-name rename that ALIGN rejects but the name-free map accepts (anchored by structure)."""
    r_al = CL.consensus_score(T_DOG, "∀x (Dog(x) → Bark(x))", ["∀x (Canine(x) → MakeNoise(x))"] * 2, mode="align")
    r_nf = CL.consensus_score(T_DOG, "∀x (Dog(x) → Bark(x))", ["∀x (Canine(x) → MakeNoise(x))"] * 2, mode="nf")
    r_hy = CL.consensus_score(T_DOG, "∀x (Dog(x) → Bark(x))", ["∀x (Canine(x) → MakeNoise(x))"] * 2, mode="hyb")
    assert r_al["per_peer"][0] is False
    assert r_nf["per_peer"][0] is True
    assert r_hy["c_score"] == 0.0


def test_unknown_never_agreement(monkeypatch):
    """Forced UNKNOWN (simulated z3 timeout on every pair) -> n_unknown counted, c_score = 1 (no agreement)."""
    def fake(cs, p, text, ent, P, cache, modes):
        return {"align_eq": None, "nf_eq": None, "hyb_eq": None}
    monkeypatch.setattr(CL.PR, "pair_verdicts", fake)
    r = CL.consensus_score(T_DOG, "∀x (Dog(x) → Bark(x))", ["∀x (¬Bark(x) → ¬Dog(x))"] * 3, mode="hyb")
    assert r["n_unknown"] == 3 and r["n_agree"] == 0 and r["c_score"] == 1.0


def test_z3_timeout_1ms_exact_mode():
    """A real 1 ms z3 budget: the verdict may be UNKNOWN (None) but is never counted as agreement unless proven."""
    r = CL.consensus_score(T_DOG, "∀x (Dog(x) → Bark(x))", ["∀x (¬Bark(x) → ¬Dog(x))"] * 2, mode="exact", params={"timeout_ms": 1})
    assert r["n_agree"] == sum(v is True for v in r["per_peer"])
    assert r["n_unknown"] == sum(v is None for v in r["per_peer"])


def test_identical_string_true_without_solver(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("solver called on identical strings")
    monkeypatch.setattr(CL.PR, "pair_verdicts", boom)
    r = CL.consensus_score(T_DOG, "∀x (Dog(x) → Bark(x))", ["∀x (Dog(x) → Bark(x))", "∀x(Dog(x)→Bark(x))"], mode="hyb")
    assert r["c_score"] == 0.0 and r["n_agree"] == 2


def test_unparseable_candidate():
    r = CL.consensus_score(T_DOG, "∀x (Dog(x) → ", ["∀x (Dog(x) → Bark(x))"] * 2, mode="hyb")
    assert r["status"] == "UNPARSEABLE" and r["c_score"] == 1.0
    g = CL.graded_consensus(T_DOG, "∀x (Dog(x) → ", ["∀x (Dog(x) → Bark(x))"] * 2)
    assert g["status"] == "UNPARSEABLE" and g["g_score"] == 1.0


def test_fewer_than_two_peers():
    r = CL.consensus_score(T_DOG, "∀x (Dog(x) → Bark(x))", ["∀x (Dog(x) → Bark(x))", "∀x (Dog(x) → "], mode="align")
    assert r["status"] == "PEER_UNAVAILABLE" and r["c_score"] is None and r["n_peers_unparseable"] == 1


def test_graded_consensus_orientation():
    good = CL.graded_consensus(T_DOG, "∀x (Dog(x) → Bark(x))", ["∀x (Dog(x) → Bark(x))", "∀x (¬Bark(x) → ¬Dog(x))"], mode="hyb")
    bad = CL.graded_consensus(T_DOG, "∀x (Dog(x) → ¬Bark(x))", ["∀x (Dog(x) → Bark(x))", "∀x (¬Bark(x) → ¬Dog(x))"], mode="hyb")
    assert good["status"] == bad["status"] == "OK"
    assert good["g_score"] < bad["g_score"]


def test_minimal_typed_repair_neg():
    r = CL.minimal_typed_repair("∀x (Dog(x) → ¬Bark(x))", "∀x (Dog(x) → Bark(x))", budget_s=5)
    assert r["ops"] == ["NEG"], r


def test_equivalent_modulo_vocab():
    assert CL.equivalent_modulo_vocab("∀x (Dog(x) → Bark(x))", "∀x (IsDog(x) → Barks(x))")[0] is True
    assert CL.equivalent_modulo_vocab("∀x (Dog(x) → Bark(x))", "∀x (Dog(x) → ¬Bark(x))")[0] is False


def test_peer_pool_mocked_and_dry_run(tmp_path):
    est = CL.peer_pool(T_DOG, families=["G1", "G9"], dry_run=True)
    assert est["slots"] == ["G1", "G9"] and est["estimate_usd"] > 0
    calls = []

    def client(model, messages, params):
        calls.append((model, messages[-1]["content"], params["temperature"]))
        return "FOL: ∀x (Dog(x) → Bark(x))", 0.0001
    out = CL.peer_pool(T_DOG, families=["G1", "G9"], dry_run=False, client=client, ledger=tmp_path / "l.jsonl")
    assert [p["fol"] for p in out["peers"]] == ["∀x (Dog(x) → Bark(x))"] * 2
    assert calls[0][1] == f"Sentence: {T_DOG}" and calls[0][2] == 0.0
    assert abs(out["cost_usd"] - 0.0002) < 1e-12
    assert len((tmp_path / "l.jsonl").read_text().splitlines()) == 2


@pytest.mark.skipif(os.environ.get("AII_LIVE") != "1", reason="live call only with AII_LIVE=1")
def test_peer_pool_live_smoke():
    out = CL.peer_pool(T_DOG, families=["G1", "G9"], dry_run=False,
                       ledger=Path(__file__).resolve().parent.parent / "results" / "cost_ledger.jsonl")
    assert out["cost_usd"] < 0.002
    assert all(p["fol"] for p in out["peers"])
    r = CL.consensus_score(T_DOG, "∀x (Dog(x) → Bark(x))", [p["fol"] for p in out["peers"]], mode="hyb")
    assert r["status"] == "OK"
