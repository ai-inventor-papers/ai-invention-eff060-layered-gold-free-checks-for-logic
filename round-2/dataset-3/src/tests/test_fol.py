import csv, random, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "labeller"))
from fol import parse, equivalent  # noqa: E402

A, B, C = ("atom", "A", ("x",)), ("atom", "B", ("x",)), ("atom", "C", ("x",))


def test_xor_binds_tighter_than_imp():
    assert parse("A(x) ⊕ B(x) → C(x)") == ("imp", ("xor", A, B), C)


def test_iff_lowest():
    assert parse("A(x) ↔ B(x) → C(x)") == ("iff", A, ("imp", B, C))


def test_ascii_iff():
    assert parse("A(x) <-> B(x)") == ("iff", A, B)


def test_folio_roundtrip_equiv():
    rows = list(csv.DictReader(open(ROOT / "data_local" / "yfxiao__folio-refined__train.csv")))
    fols = [f for r in rows for f in r["fol premises"].split("\n") if f.strip()]
    random.Random(0).shuffle(fols)
    ok = 0
    for f in fols:
        try:
            e = parse(f)
        except Exception:
            continue
        assert equivalent(e, e) is True
        ok += 1
        if ok == 10:
            break
    assert ok == 10


def test_truncated_and_empty_rejected():
    import pytest
    for bad in ("", "A(x) ∧", "∀x (A(x) →", "P(x, )"):
        with pytest.raises(Exception):
            parse(bad)
