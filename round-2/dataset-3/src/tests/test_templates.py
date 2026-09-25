"""Hand-written instances for each R_COMP template: exact text, exact weak/strong FOL, and the semantic
relations the readings must satisfy (checked with z3 through E's fol.py)."""
import sys
from pathlib import Path

import z3

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "labeller"))
sys.path.insert(0, str(ROOT / "src"))
from fol import parse, preds, mkpred, to_z3, valid, equivalent, profile  # noqa: E402
from templates import fill, plural_vp  # noqa: E402

C = [{"atom": "LivesIn(x, paris)", "vp": "lives in Paris", "neg_vp": "does not live in Paris"},
     {"atom": "CanMake(x, cookies)", "vp": "can make cookies", "neg_vp": "cannot make cookies", "neg": True},
     {"atom": "Baker(x)", "vp": "is a baker", "neg_vp": "is not a baker"}]
Q = {"atom": "PlaysTennis(x)", "vp": "plays tennis"}
X = {"atom": "Sick(x)", "vp": "is sick"}


def _z(*fs):
    es = [parse(f) for f in fs]
    ar = {}
    for e in es:
        ar.update(preds(e))
    P = {q: mkpred(q, m) for q, m in ar.items()}
    return [to_z3(e, {}, P) for e in es]


def entails(a, b):
    za, zb = _z(a, b)
    return valid(z3.Implies(za, zb))


def mk(t, v=0, person=True):
    return fill(t, v, "student", "Student(x)", C, Q, X, person)


def test_T1_text_and_readings():
    r = mk("T1")
    assert r["text"] == "Every student who lives in Paris, who cannot make cookies, and who is a baker plays tennis, unless the student is sick."
    assert r["reference_fol_weak"] == "∀x (Student(x) ∧ LivesIn(x, paris) ∧ ¬CanMake(x, cookies) ∧ Baker(x) ∧ ¬Sick(x) → PlaysTennis(x))"
    assert r["reference_fol_strong"] == "∀x (Student(x) ∧ LivesIn(x, paris) ∧ ¬CanMake(x, cookies) ∧ Baker(x) → (PlaysTennis(x) ↔ ¬Sick(x)))"


def test_exception_templates_strong_entails_weak_not_converse():
    for t in ("T1", "T2", "T4", "T5", "T6", "T7", "T9"):
        for v in (0, 1):
            r = mk(t, v)
            assert entails(r["reference_fol_strong"], r["reference_fol_weak"]) is True, t
            assert entails(r["reference_fol_weak"], r["reference_fol_strong"]) is False, t
            assert equivalent(parse(r["reference_fol_weak"]), parse(r["reference_fol_strong"])) is False


def test_T2_T4_T5_T6_share_T1_readings():
    base = mk("T1")
    for t in ("T2", "T4", "T5", "T6"):
        r = mk(t)
        assert r["reference_fol_weak"] == base["reference_fol_weak"], t
        assert r["reference_fol_strong"] == base["reference_fol_strong"], t
    assert mk("T5")["nested"] is True and mk("T4")["nested"] is False


def test_T3_proviso():
    r = mk("T3")
    assert r["text"] == "Any student that lives in Paris and that cannot make cookies plays tennis, provided that the student is sick and is a baker."
    assert r["reference_fol_weak"] == "∀x (Student(x) ∧ LivesIn(x, paris) ∧ ¬CanMake(x, cookies) ∧ Sick(x) ∧ Baker(x) → PlaysTennis(x))"
    assert r["reference_fol_strong"] == "∀x (Student(x) ∧ LivesIn(x, paris) ∧ ¬CanMake(x, cookies) → (PlaysTennis(x) ↔ (Sick(x) ∧ Baker(x))))"
    assert entails(r["reference_fol_strong"], r["reference_fol_weak"]) is True


def test_T7_no_sortal_plural_they():
    r = mk("T7")
    assert r["text"] == "Anyone who lives in Paris, cannot make cookies, and is a baker plays tennis unless they are sick."
    assert "Student" not in r["reference_fol_weak"] + r["reference_fol_strong"]
    assert plural_vp("has a pet") == "have a pet" and plural_vp("does not swim") == "do not swim"
    assert plural_vp("watches TV") == "watch TV" and plural_vp("studies law") == "study law"
    assert plural_vp("can fly") == "can fly" and plural_vp("lives in Paris") == "live in Paris"


def test_T8_only_if():
    r = mk("T8")
    assert r["text"] == "If a student lives in Paris, cannot make cookies, and is a baker, then the student plays tennis, but only if the student is sick."
    assert r["reference_fol_weak"] == "∀x (Student(x) ∧ LivesIn(x, paris) ∧ ¬CanMake(x, cookies) ∧ Baker(x) ∧ PlaysTennis(x) → Sick(x))"
    w, s, c = r["reference_fol_weak"], r["reference_fol_strong"], r["reading_converse"]
    # strong (iff) = weak (only-if) ∧ converse (if); the converse alone is NOT an accepted reading
    zw, zs, zc = _z(w, s, c)
    assert valid(zs == z3.And(zw, zc)) is True
    assert equivalent(parse(w), parse(c)) is False and equivalent(parse(s), parse(c)) is False


def test_T9_negative_universal():
    r = mk("T9")
    assert r["text"] == "No student who lives in Paris, who cannot make cookies, and who is a baker plays tennis, unless the student is sick."
    assert r["reference_fol_weak"] == "∀x (Student(x) ∧ LivesIn(x, paris) ∧ ¬CanMake(x, cookies) ∧ Baker(x) ∧ ¬Sick(x) → ¬PlaysTennis(x))"
    alt = "∀x (Student(x) ∧ LivesIn(x, paris) ∧ ¬CanMake(x, cookies) ∧ Baker(x) → (PlaysTennis(x) ↔ Sick(x)))"
    assert equivalent(parse(r["reference_fol_strong"]), parse(alt)) is True


def test_no_vacuous_atoms_and_nontrivial():
    for t in ("T1", "T3", "T7", "T8", "T9"):
        r = mk(t)
        e = parse(r["reference_fol_weak"])
        assert "VACUOUS" not in profile(e).values()
        z, = _z(r["reference_fol_weak"])
        assert valid(z) is False and valid(z3.Not(z)) is False


def test_non_person_uses_that():
    r = mk("T1", person=False)
    assert r["text"].startswith("Every student that lives in Paris, that cannot")
