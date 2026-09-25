"""edits_tracked must yield exactly repair_census.edits (same labels, same candidates, same order); polarity helper."""
import csv
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "labeller"))
sys.path.insert(0, str(ROOT / "src"))
from fol import parse  # noqa: E402
from repair_census import edits  # noqa: E402
from perturb import edits_tracked, syn_polarity, control_contra, control_reorder  # noqa: E402


def _formulas(n=25):
    rows = list(csv.DictReader(open(ROOT / "data_local" / "yfxiao__folio-refined__train.csv")))
    fols = [f for r in rows for f in r["fol premises"].split("\n") if f.strip()]
    random.Random(3).shuffle(fols)
    out = []
    for f in fols:
        try:
            out.append(parse(f))
        except Exception:
            continue
        if len(out) == n:
            break
    return out


def test_edits_tracked_mirrors_edits():
    fs = _formulas()
    for e, d in zip(fs, fs[1:] + fs[:1]):
        a = [(lab, str(c)) for lab, c in edits(e, d)]
        b = [(lab, str(c)) for lab, _, _, c in edits_tracked(e, d)]
        assert a == b


def test_polarity():
    e = parse("∀x (A(x) ∧ ¬B(x) → C(x))")
    assert syn_polarity(e, (2, 2)) == "UP"          # consequent
    assert syn_polarity(e, (2, 1, 1)) == "DOWN"     # restrictor conjunct
    assert syn_polarity(e, (2, 1, 2, 1)) == "UP"    # under ¬ inside the antecedent
    assert syn_polarity(parse("A(x) ↔ B(x)"), (1,)) == "NONMONO"


def test_controls_shapes():
    e = parse("∀x (A(x) ∧ B(x) → C(x))")
    k, c = control_contra(e)
    assert k == "CONTRAPOSITIVE" and c == ("all", "x", ("imp", ("not", ("atom", "C", ("x",))), ("not", ("and", ("atom", "A", ("x",)), ("atom", "B", ("x",))))))
    k, c = control_reorder(e)
    assert k == "REORDER_COMMUTE"
