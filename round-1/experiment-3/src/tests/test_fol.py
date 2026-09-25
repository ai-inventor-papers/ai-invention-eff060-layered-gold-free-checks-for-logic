"""T0 unit tests: precedence fix, eqmv symmetry, rewrite invariance, item_id, census regression."""
import hashlib
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from common import eqmv, item_id, label, norm, safe_parse  # noqa: E402
from fol import equivalent, parse  # noqa: E402

A, B, C = ("atom", "A", ()), ("atom", "B", ()), ("atom", "C", ())


def test_xor_precedence():
    assert parse("A ⊕ B → C") == ("imp", ("xor", A, B), C)
    assert parse("A → B ⊕ C") == ("imp", A, ("xor", B, C))
    assert parse("A ⊕ B ∧ C") == ("xor", A, ("and", B, C))
    assert parse("A ↔ B ⊕ C") == ("iff", A, ("xor", B, C))


def test_contrapositive_equivalent():
    assert equivalent(parse("∀x (P(x) → Q(x))"), parse("∀y (¬Q(y) → ¬P(y))")) is True


def test_item_id_hand_computed():
    for sysname, text, fol in [("gpt-4", "Bonnie performs in school talent shows often.", "Perform(bonnie)"),
                               ("human_original", "All dogs bark!", " ∀x (Dog(x) → Bark(x)) "),
                               ("P1", "  A  vacation, is relaxing ", "Relaxing(v)")]:
        want = hashlib.sha1((sysname + "|" + norm(text) + "|" + fol.strip()).encode()).hexdigest()[:16]
        assert item_id(sysname, text, fol) == want
    assert norm("  A  vacation, is relaxing ") == "a vacation is relaxing"


def _gold_formulas(n=30):
    rows = json.loads((ROOT / "data" / "repair_census.rows.json").read_text())
    out = [safe_parse(r["new"]) for r in rows]
    return [e for e in out if e is not None][:n]


def test_eqmv_symmetric():
    rnd = random.Random(0)
    fs = _gold_formulas(40)
    for _ in range(30):
        a, b = rnd.choice(fs), rnd.choice(fs)
        assert eqmv(a, b)[0] == eqmv(b, a)[0]


def test_eqmv_rename_and_contrapositive():
    from rewrites import contrapositive, rename_rewrite
    fs = _gold_formulas(20)
    n_ok = 0
    for f in fs:
        assert eqmv(f, contrapositive(f))[0] is True
        rn, _ = rename_rewrite(f, token_alignable=True)
        n_ok += eqmv(f, rn)[0] is True
    assert n_ok == len(fs)


def test_label_basic():
    assert label("∀x (Dog(x) → Bark(x))", "∀y (¬Bark(y) → ¬Dog(y))")["label"] == "CORRECT"
    assert label("∀x (Dogs(x) → Barks(x))", "∀x (Dog(x) → Bark(x))")["auto_class"] == "VOCAB"
    r = label("∀x (Dog(x) → ¬Bark(x))", "∀x (Dog(x) → Bark(x))")
    assert r["label"] == "ERROR" and r["repair_ops"] == ["NEG"]
    assert label("∀x (Dog(x) ∈ Bark(x))", "∀x (Dog(x) → Bark(x))")["label"] == "UNPARSEABLE"
    assert label("¬Bark(rex)", "Bark(rex)", ambiguous=True, track="H")["label"] == "READING_CHOICE"
