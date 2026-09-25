"""E2 VEX flag (additive; changes no label). Instrument-disjoint label subset: no aligner, no rename search.

vex(cand, ref) -> {"vex": bool|None, "vex_eq": bool|None}
  vex    = set of normalised (kind, name, arity) symbols of the candidate  ⊆  that of the reference, where kind is
           'pred' or 'const', a constant is any argument not bound by a quantifier, and normalisation is
           lowercase + drop every non-alphanumeric character (HasEmpathy ~ has_empathy). Nothing is renamed.
  vex_eq = plain z3 equivalence of candidate and reference after that SAME surface normalisation (names are identified
           by equal normalised spelling only, no alignment), 5 s budget; None if undecided or unparseable.
Both are None when either formula does not parse.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "labeller"))
sys.setrecursionlimit(10000)
from fol import parse, equivalent  # noqa: E402


def _n(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def _norm_ast(e, bound=frozenset()):
    k = e[0]
    if k == "atom":
        return ("atom", _n(e[1]) or e[1], tuple(a if a in bound else "k" + _n(a) for a in e[2]))
    if k in ("all", "ex"):
        return (k, e[1], _norm_ast(e[2], bound | {e[1]}))
    if k == "not":
        return ("not", _norm_ast(e[1], bound))
    return (k, _norm_ast(e[1], bound), _norm_ast(e[2], bound))


def symbols(e, bound=frozenset(), acc=None) -> set:
    acc = set() if acc is None else acc
    k = e[0]
    if k == "atom":
        acc.add(("pred", _n(e[1]), len(e[2])))
        for a in e[2]:
            if a not in bound:
                acc.add(("const", _n(a), 0))
    elif k in ("all", "ex"):
        symbols(e[2], bound | {e[1]}, acc)
    elif k == "not":
        symbols(e[1], bound, acc)
    else:
        symbols(e[1], bound, acc)
        symbols(e[2], bound, acc)
    return acc


def vex(cand: str, ref: str, ms: int = 5000) -> dict:
    try:
        if not (cand or "").strip():
            raise ValueError("empty")
        c, r = parse(cand), parse(ref)
    except Exception:  # noqa: BLE001 - parser raises assorted errors on junk
        return {"vex": None, "vex_eq": None}
    sub = symbols(c) <= symbols(r)
    try:
        eq = equivalent(_norm_ast(c), _norm_ast(r), ms=ms)
        eq = bool(eq) if eq is not None else None
    except Exception:  # noqa: BLE001
        eq = None
    return {"vex": sub, "vex_eq": eq}


if __name__ == "__main__":
    assert vex("∀x (HasEmpathy(x) → Calm(x))", "∀x (has_empathy(x) → calm(x))") == {"vex": True, "vex_eq": True}
    assert vex("∀x (Dog(x) → Animal(x))", "∀x (Dog(x) → Mammal(x))")["vex"] is False
    assert vex("∀x (Dog(x) → Animal(x))", "∀x (Animal(x) → Dog(x))") == {"vex": True, "vex_eq": False}
    assert vex("Kitten(piper)", "Kitten(Piper)") == {"vex": True, "vex_eq": True}
    assert vex("", "A(x)") == {"vex": None, "vex_eq": None}
    print("vex self-tests ok")
