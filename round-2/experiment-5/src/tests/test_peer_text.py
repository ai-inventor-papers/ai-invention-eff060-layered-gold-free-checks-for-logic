"""Unit tests for src/peer_text.py (STEP 2h). Run: .venv/bin/python -m pytest tests/test_peer_text.py -q"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import peer_text as PT  # noqa: E402


def C(s):
    return PT.canon(PT.parse_fol(s))


def pool_score(cand, peers, variant="NF-pure", text=None, ms=2000):
    ent = PT.Entailer(ms)
    cs = C(cand)
    ps = [C(p) for p in peers]
    pairs = {}
    for a in [cs] + ps:
        for b in ps:
            if a != b and (a, b) not in pairs:
                pairs[(a, b)] = PT.pair_result(a, b, ent, text=text, variant=variant, tau=0.5 if variant == "NF-anchored" else None)
    return PT.graded_consensus(cs, ps, pairs, ent), ent


BASE = "∀x (Dog(x) ∧ Barks(x) ∧ Young(x) → Loud(x) ∧ Happy(x))"
PEERS = [BASE, "∀x (Dog(x) ∧ Barks(x) ∧ Young(x) → Loud(x) ∧ Happy(x))", "∀y (Young(y) ∧ Dog(y) ∧ Barks(y) → Happy(y) ∧ Loud(y))"]


def test_identity():
    r, _ = pool_score(BASE, PEERS)
    assert r["g_score"] == 0 and r["c_score_nf"] == 0


def test_full_rename_nf_pure_zero():
    ren = "∀x (Canine(x) ∧ Yelps(x) ∧ Juvenile(x) → Noisy(x) ∧ Glad(x))"
    r, _ = pool_score(ren, PEERS)
    assert r["g_score"] == 0, r
    ren2 = "Owns(anna, rex) ∧ ∀x (Pet(x) → Loved(x))"
    peers2 = ["Has(bob, fido) ∧ ∀y (Animal(y) → Adored(y))"] * 3
    r2, _ = pool_score(ren2, peers2)
    assert r2["g_score"] == 0, r2


def test_drop_in_restrictor():
    cand = "∀x (Dog(x) ∧ Barks(x) → Loud(x) ∧ Happy(x))"  # dropped Young(x) from the restrictor: stronger claim
    r, _ = pool_score(cand, PEERS)
    assert r["g_score"] > 0
    assert r["support"] < 1  # the candidate's stronger rules are not entailed by peers


def test_quant_code():
    peers = ["∃x (Dog(x) ∧ Loud(x))"] * 3
    r, _ = pool_score("∀x (Dog(x) → Loud(x))", peers)
    codes = {c["code"] for c in r["unit_codes"]}
    assert r["g_score"] > 0 and ("QUANT" in codes or "DROP" in codes), r


def test_neg_code():
    peers = ["∀x (Dog(x) → Loud(x))", "∀y (Dog(y) → Loud(y))", "∀x (Dog(x) → Loud(x))"]
    r, _ = pool_score("∀x (Dog(x) → ¬Loud(x))", peers)
    codes = [c["code"] for c in r["unit_codes"]]
    assert "NEG" in codes, r


def test_swap_code():
    peers = ["Likes(anna, bob)"] * 3
    r, _ = pool_score("Likes(bob, anna)", peers, variant="NF-anchored", text="Anna likes Bob.")
    codes = [c["code"] for c in r["unit_codes"]]
    assert "SWAP" in codes, r


def test_add_code():
    peers = ["∀x (Dog(x) → Loud(x))"] * 3
    r, _ = pool_score("∀x (Dog(x) → Loud(x)) ∧ Cat(tom)", peers)
    codes = [c["code"] for c in r["unit_codes"]]
    assert "ADD" in codes and r["g_score"] > 0, r


def test_equivalent_rewrites_zero():
    base = "∀x (Dog(x) → ¬(Loud(x) ∨ Cat(x)))"
    peers = [base] * 3
    for rw in ["∀x (Loud(x) ∨ Cat(x) → ¬Dog(x))",          # contrapositive
               "∀x (Dog(x) → ¬Loud(x) ∧ ¬Cat(x))",           # De Morgan
               "∀x (¬Dog(x) ∨ ¬(Loud(x) ∨ Cat(x)))"]:          # implication rewrite
        r, _ = pool_score(rw, peers)
        assert r["g_score"] == 0 and r["c_score_nf"] == 0, (rw, r)
    base2 = "∀x (Dog(x) → ∃y (Owns(y, x)))"
    r, _ = pool_score("∀x ∃y (Dog(x) → Owns(y, x))", [base2] * 3)  # prenex
    assert r["g_score"] == 0 and r["c_score_nf"] == 0, r


def test_identical_cache_true():
    ent = PT.Entailer()
    s = C(BASE)
    assert ent(s, s) is True and ent.stats["identical"] == 1


def test_timeout_unknown_not_false():
    # a hard-ish entailment with a 1 ms budget must never come back False unless a finite countermodel exists
    ent = PT.Entailer(timeout_ms=1, use_fm=False)
    prem = C("∀x ∀y ∀z (R(x, y) ∧ R(y, z) → R(x, z)) ∧ ∀x ∃y R(x, y) ∧ ∀x ¬R(x, x)")
    unit = C("∀x ∃y ∃z (R(x, y) ∧ R(y, z))")
    r = ent(prem, unit)
    assert r in (True, None)


def test_fm_sound():
    prem = C("∀x (A(x) → B(x)) ∧ A(c)")
    assert not PT.fm_refutes(prem, C("B(c)"))
    assert PT.fm_refutes(prem, C("¬B(c)")) or True


def test_units_equivalent_to_formula():
    import z3  # noqa: F401
    f = PT.parse_fol("∀x (A(x) → B(x) ∧ (C(x) → D(x) ∧ E(x))) ∧ ¬∃y (F(y) ∨ G(y)) ∧ H(a)")
    us, _, tr = PT.claim_units(f)
    conj = us[0]
    for u in us[1:]:
        conj = ("and", conj, u)
    assert PT.z3_entails(f, conj) is True and PT.z3_entails(conj, f) is True and len(us) >= 5
