"""Meaning-preserving rewrite families for the invariance set (seed 0, deterministic).

RENAME          each predicate/constant -> WordNet synonym of its head (last) CamelCase token; same arity; injective
REORDER         commute every ∧ / ∨ operand
DEMORGAN        ¬(A∧B) <-> ¬A∨¬B (or ¬(A∨B) <-> ¬A∧¬B) at the first site; else A∧B -> ¬(¬A∨¬B) at the first conjunction
PRENEX          pull quantifiers outward where legal (bound variable not free in the sibling), repeated to fixpoint
CONTRAPOSITIVE  A→B => ¬B→¬A at the top implication under the leading quantifier block
Every family except RENAME is z3-verified equivalent to the original; a family that does not apply or fails verification
is recorded as n/a (never silently dropped).
"""
from __future__ import annotations

import re

from fol import parse, equivalent, to_str

TOKRE = re.compile(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+")


def _wn():
    import nltk
    from pathlib import Path
    nltk.data.path.insert(0, str(Path(__file__).resolve().parent.parent / "nltk_data"))
    from nltk.corpus import wordnet as wn
    return wn


def _free(e, bv=frozenset()):
    k = e[0]
    if k == "atom":
        return {a for a in e[2] if a in _VARS and a not in bv}
    if k in ("all", "ex"):
        return _free(e[2], bv | {e[1]})
    if k == "not":
        return _free(e[1], bv)
    return _free(e[1], bv) | _free(e[2], bv)


_VARS: set = set()


def _bound(e, acc=None):
    acc = set() if acc is None else acc
    if e[0] in ("all", "ex"):
        acc.add(e[1]); _bound(e[2], acc)
    elif e[0] == "not":
        _bound(e[1], acc)
    elif e[0] != "atom":
        _bound(e[1], acc); _bound(e[2], acc)
    return acc


def synonym(word: str, taken: set) -> str:
    wn = _wn()
    lw = word.lower()
    for s in wn.synsets(lw)[:1]:
        for l in s.lemmas():
            n = l.name()
            if n.lower() != lw and "_" not in n and "-" not in n and n.isalpha():
                return n
    return None


def rename_map(e) -> tuple[dict, dict]:
    """Injective predicate/constant renaming: head CamelCase token -> first differing WordNet lemma, else prefix 'Is'."""
    from repair_census import symbols
    P, C = symbols(e)
    names_taken = {p[0] for p in P} | set(C)
    pmap, cmap = {}, {}
    for (name, ar) in sorted(P):
        toks = TOKRE.findall(name)
        new = None
        if toks:
            head = toks[-1]
            syn = synonym(head, names_taken)
            if syn:
                syn = syn[0].upper() + syn[1:] if head[0].isupper() else syn
                new = name[: len(name) - len(head)] + syn if name.endswith(head) else None
        if not new or new in names_taken:
            new = "Is" + name[0].upper() + name[1:]
        while new in names_taken:
            new = new + "X"
        names_taken.add(new)
        pmap[(name, ar)] = new
    for c in sorted(C):
        toks = TOKRE.findall(c)
        new = None
        if toks:
            head = toks[-1]
            syn = synonym(head, names_taken)
            if syn and c.endswith(head):
                syn = syn[0].upper() + syn[1:] if head[0].isupper() else syn.lower()
                new = c[: len(c) - len(head)] + syn
        if not new or new in names_taken:
            new = "is" + c[0].upper() + c[1:]
        while new in names_taken:
            new = new + "x"
        names_taken.add(new)
        cmap[c] = new
    return pmap, cmap


def rw_rename(e):
    from repair_census import rename
    pmap, cmap = rename_map(e)
    return rename(e, pmap, cmap)


def rw_reorder(e):
    k = e[0]
    if k == "atom":
        return e
    if k in ("all", "ex"):
        return (k, e[1], rw_reorder(e[2]))
    if k == "not":
        return ("not", rw_reorder(e[1]))
    a, b = rw_reorder(e[1]), rw_reorder(e[2])
    return (k, b, a) if k in ("and", "or") else (k, a, b)


def _first(e, pred, path=()):
    if pred(e):
        return path
    k = e[0]
    kids = [] if k == "atom" else [2] if k in ("all", "ex") else [1] if k == "not" else [1, 2]
    for i in kids:
        r = _first(e[i], pred, path + (i,))
        if r is not None:
            return r
    return None


def _get(e, path):
    for i in path:
        e = e[i]
    return e


def _put(e, path, new):
    if not path:
        return new
    lst = list(e)
    lst[path[0]] = _put(e[path[0]], path[1:], new)
    return tuple(lst)


def rw_demorgan(e):
    p = _first(e, lambda x: x[0] == "not" and x[1][0] in ("and", "or"))
    if p is not None:
        n = _get(e, p)[1]
        op = "or" if n[0] == "and" else "and"
        return _put(e, p, (op, ("not", n[1]), ("not", n[2])))
    p = _first(e, lambda x: x[0] == "and")
    if p is not None:
        n = _get(e, p)
        return _put(e, p, ("not", ("or", ("not", n[1]), ("not", n[2]))))
    return None


def rw_prenex(e):
    changed = [False]

    def go(x):
        k = x[0]
        if k == "atom":
            return x
        if k in ("all", "ex"):
            return (k, x[1], go(x[2]))
        if k == "not":
            return ("not", go(x[1]))
        a, b = go(x[1]), go(x[2])
        if k in ("and", "or"):
            if b[0] in ("all", "ex") and b[1] not in _free(a) and b[1] not in _bound(a):
                changed[0] = True
                return (b[0], b[1], go((k, a, b[2])))
            if a[0] in ("all", "ex") and a[1] not in _free(b) and a[1] not in _bound(b):
                changed[0] = True
                return (a[0], a[1], go((k, a[2], b)))
        if k == "imp" and b[0] in ("all", "ex") and b[1] not in _free(a) and b[1] not in _bound(a):
            changed[0] = True
            return (b[0], b[1], go(("imp", a, b[2])))
        return (k, a, b)
    out = go(e)
    return out if changed[0] else None


def rw_contrapositive(e):
    path, x = (), e
    while x[0] in ("all", "ex"):
        path += (2,); x = x[2]
    if x[0] != "imp":
        return None
    return _put(e, path, ("imp", ("not", x[2]), ("not", x[1])))


FAMILIES = {"RENAME": rw_rename, "REORDER": rw_reorder, "DEMORGAN": rw_demorgan, "PRENEX": rw_prenex,
            "CONTRAPOSITIVE": rw_contrapositive}


def rewrite_all(fol: str) -> list[dict]:
    e = parse(fol)
    global _VARS
    _VARS = _bound(e)
    out = []
    for fam, fn in FAMILIES.items():
        try:
            r = fn(e)
        except Exception as ex:  # noqa: BLE001
            out.append({"family": fam, "rewritten_fol": None, "verified_equiv": "n/a", "note": f"error {ex}"[:100]})
            continue
        if r is None or r == e:
            out.append({"family": fam, "rewritten_fol": None, "verified_equiv": "n/a", "note": "family does not apply"})
            continue
        s = to_str(r)
        if fam == "RENAME":
            out.append({"family": fam, "rewritten_fol": s, "verified_equiv": "rename-bijection (not z3; lexical)"})
            continue
        v = equivalent(parse(s), e, ms=5000)
        if v is True:
            out.append({"family": fam, "rewritten_fol": s, "verified_equiv": True})
        else:
            out.append({"family": fam, "rewritten_fol": None, "verified_equiv": "n/a",
                        "note": f"z3 did not verify ({v})"})
    return out
