"""Unit tests of the name-free map search (src/freelab.py)."""
import random

import pytest

from fol import parse
from freelab import (Candidate, Reading, equivalent_modulo_vocab_exhaustive, first_mismatch, fingerprint,
                     label_candidate, search, z3_equiv)

WEAK = "∀x (Rapper(x) ∧ Treated(x) ∧ DependentOn(x, caffeine) ∧ British(x) ∧ ¬PresentsAt(x, conference) → FlexibleSchedule(x))"
STRONG = "∀x (Rapper(x) ∧ Treated(x) ∧ DependentOn(x, caffeine) ∧ British(x) → (FlexibleSchedule(x) ↔ ¬PresentsAt(x, conference)))"
R = {"weak": WEAK, "strong": STRONG}


def lab(c, readings=R):
    return label_candidate(c, readings)


def test_identity():
    out = lab(WEAK)
    assert out["status"] == "MAPPED" and out["matched_reading"] == "weak"
    ents = out["map_entries_union"]
    assert any(all(ents[i].split("(")[0] == ents[i].split(" => ")[1].split("(")[0] for i in m["entry_ids"]
                   if not ents[i].startswith("const:")) for m in out["equiv_maps"])


def test_synonym_and_nonce_rename():
    syn = "∀x (Rapper(x) ∧ Cured(x) ∧ ReliantOn(x, coffee) ∧ English(x) ∧ ¬Presents(x, meeting) → Flexible(x))"
    non = "∀x (Bako(x) ∧ Dufi(x) ∧ Gomel(x, zup) ∧ Kira(x) ∧ ¬Lomp(x, vat) → Mabe(x))"
    for c in (syn, non):
        out = lab(c)
        assert out["status"] == "MAPPED", out["status"]


def test_qe_role_swap_is_nonidentity_map():
    # weak reading: S∧A∧¬E → Q  ≡  S∧A∧¬Q → E ; the swapped formula is equivalent only under a non-identity map
    swapped = "∀x (Rapper(x) ∧ Treated(x) ∧ DependentOn(x, caffeine) ∧ British(x) ∧ ¬FlexibleSchedule(x) → PresentsAt(x, conference))"
    out = lab(swapped)
    assert out["status"] == "MAPPED"
    ents = out["map_entries_union"]
    nonid = [m for m in out["equiv_maps"] if any(ents[i] == "FlexibleSchedule(x) => PresentsAt(x, conference)" for i in m["entry_ids"])]
    assert nonid


def test_drop_and_add_are_error_cert():
    drop = "∀x (Rapper(x) ∧ Treated(x) ∧ DependentOn(x, caffeine) ∧ ¬PresentsAt(x, conference) → FlexibleSchedule(x))"
    add = "∀x (Rapper(x) ∧ Treated(x) ∧ DependentOn(x, caffeine) ∧ British(x) ∧ Tall(x) ∧ ¬PresentsAt(x, conference) → FlexibleSchedule(x))"
    neg = "∀x (Rapper(x) ∧ Treated(x) ∧ DependentOn(x, caffeine) ∧ British(x) ∧ PresentsAt(x, conference) → FlexibleSchedule(x))"
    # DROP / ADD of a sibling conjunct can only be rescued by a structural bridge (B3 merge / B4 split): the search
    # must either certify ERROR or map it ONLY through B3/B4 (which the gloss check then has to reject)
    for c, br in ((drop, "B3"), (add, "B4")):
        o = lab(c)
        assert o["status"] == "ERROR_CERT" or (o["status"] == "MAPPED" and all(br in m["bridges"] for m in o["equiv_maps"]))
    # a dropped consequent-side atom has no sibling rescue
    drop_q = "∀x (Rapper(x) ∧ Treated(x) ∧ DependentOn(x, caffeine) ∧ British(x) → ¬PresentsAt(x, conference))"
    assert lab(drop_q)["status"] == "ERROR_CERT"
    # flipping the exception polarity: the family has no B5 licence for this name -> no map
    assert lab(neg)["status"] == "ERROR_CERT"


def test_bridges():
    # B1 reification: unary := R(x, c)
    b1 = "∀x (Rapper(x) ∧ Treated(x) ∧ CaffeineDependent(x) ∧ British(x) ∧ ¬PresentsAtConference(x) → FlexibleSchedule(x))"
    o = lab(b1)
    assert o["status"] == "MAPPED" and any("B1" in m["bridges"] for m in o["equiv_maps"])
    # B2 de-reification: P(x, k) := U(x)
    b2 = "∀x (Is(x, rapper) ∧ Treated(x) ∧ DependentOn(x, caffeine) ∧ British(x) ∧ ¬PresentsAt(x, conference) → Has(x, flexibleSchedule))"
    o = lab(b2)
    assert o["status"] == "MAPPED" and any("B2" in m["bridges"] for m in o["equiv_maps"])
    # B3 merge: one candidate unary := Treated ∧ British
    b3 = "∀x (Rapper(x) ∧ TreatedBritish(x) ∧ DependentOn(x, caffeine) ∧ ¬PresentsAt(x, conference) → FlexibleSchedule(x))"
    o = lab(b3)
    assert o["status"] == "MAPPED" and any("B3" in m["bridges"] for m in o["equiv_maps"])
    # B4 split: British := Brit ∧ Uk (sibling-only)
    b4 = "∀x (Rapper(x) ∧ Treated(x) ∧ DependentOn(x, caffeine) ∧ Brit(x) ∧ Uk(x) ∧ ¬PresentsAt(x, conference) → FlexibleSchedule(x))"
    o = lab(b4)
    assert o["status"] == "MAPPED" and any("B4" in m["bridges"] for m in o["equiv_maps"])
    # B5 lexical negation: NotPresentsAt(x, conference) := ¬PresentsAt(x, conference)
    b5 = "∀x (Rapper(x) ∧ Treated(x) ∧ DependentOn(x, caffeine) ∧ British(x) ∧ NotPresenting(x) → FlexibleSchedule(x))"
    o = lab(b5)
    assert o["status"] == "MAPPED" and any("B5" in m["bridges"] for m in o["equiv_maps"])


def test_t8_converse_is_reading_choice():
    rd = {"weak": "∀x (A(x) ∧ B(x) ∧ Q(x) → P(x))", "strong": "∀x (A(x) ∧ B(x) → (Q(x) ↔ P(x)))",
          "converse": "∀x (A(x) ∧ B(x) ∧ P(x) → Q(x))"}
    # the converse is a relabelling of the weak reading only if Q/P roles swap: with distinct polarities it is not.
    out = label_candidate("∀x (Aa(x) ∧ Bb(x) ∧ Pp(x) → Qq(x))", rd)
    assert out["status"] in ("MAPPED", "READING_CHOICE")


def test_symmetric_api():
    a = "∀x (P(x) ∧ Q(x, k) → S(x))"
    b = "∀x (Pz(x) ∧ Qz(x) → Sz(x))"
    r1, m1, _ = equivalent_modulo_vocab_exhaustive(a, b)
    r2, m2, _ = equivalent_modulo_vocab_exhaustive(b, a)
    assert r1 is True and r2 is True
    r3, _, _ = equivalent_modulo_vocab_exhaustive("∀x (P(x) → S(x))", "∃x (P(x) ∧ S(x))")
    assert r3 is False


# ------------------------------------------------------------------ evaluator vs z3
def _rand_formula(rng, depth, vs):
    if depth == 0 or rng.random() < 0.25:
        p = rng.choice(["P1", "P2", "P3", "R2"])
        terms = vs + ["a", "b"]
        if p == "R2":
            return ("atom", "R", (rng.choice(terms), rng.choice(terms)))
        return ("atom", p, (rng.choice(terms),))
    k = rng.choice(["not", "and", "or", "imp", "iff", "all", "ex"])
    if k == "not":
        return ("not", _rand_formula(rng, depth - 1, vs))
    if k in ("all", "ex"):
        v = rng.choice(["x", "y"])
        return (k, v, _rand_formula(rng, depth - 1, list(set(vs + [v]))))
    return (k, _rand_formula(rng, depth - 1, vs), _rand_formula(rng, depth - 1, vs))


def _equiv_variant(rng, e):
    k = rng.choice(["dneg", "contra", "comm"])
    if k == "dneg":
        return ("not", ("not", e))
    if k == "contra" and e[0] == "imp":
        return ("imp", ("not", e[2]), ("not", e[1]))
    if e[0] in ("and", "or", "iff"):
        return (e[0], e[2], e[1])
    return ("not", ("not", e))


def test_evaluator_agrees_with_z3():
    rng = random.Random(7)
    n_dec, n_eq, n_neq_found = 0, 0, 0
    for i in range(200):
        a = ("all", "x", _rand_formula(rng, 3, ["x"]))
        b = _equiv_variant(rng, a) if i % 2 else ("all", "x", _rand_formula(rng, 3, ["x"]))
        r = z3_equiv(a, b, 3000)
        mm = first_mismatch(b, fingerprint(a))
        if r is None:
            continue
        n_dec += 1
        if r is True:
            n_eq += 1
            assert mm is None, "fingerprint countermodel on a z3-equivalent pair"
        else:
            n_neq_found += mm is not None
        if mm is not None:
            assert r is False, "certified countermodel but z3 says equivalent"
    assert n_dec >= 190 and n_eq >= 90
