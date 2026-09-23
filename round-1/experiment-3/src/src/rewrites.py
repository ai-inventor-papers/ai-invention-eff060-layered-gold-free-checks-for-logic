"""Deterministic meaning-preserving rewrites of FOL ASTs (STEP 6, rewrite invariance).

RENAME          head CamelCase token of every predicate -> first WordNet synonym from a different word of the
                first synset (CamelCased), else token reversed + 'Q'; constants -> 'c_' + sha1(name)[:4]
                (equivalent only after the inverse map; this is the real test of the aligner)
RENAME(token_alignable=True)  pluralise the head token and keep constants (the aligner must undo it; used by T0)
REORDER         swap the operands of every ∧ / ∨
DEMORGAN        rewrite the first ∧ as ¬(¬A ∨ ¬B) (or, if there is no ∧, the first ∨ as ¬(¬A ∧ ¬B))
PRENEX          pull ONE quantifier outwards across ∧ / ∨ or across the consequent of → when sound, else n/a
CONTRAPOSITIVE  every A → B becomes ¬B → ¬A
"""
from __future__ import annotations

import hashlib
import re
from functools import lru_cache

from repair_census import bound_vars, symbols

TOKRE = re.compile(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+")


@lru_cache(maxsize=None)
def _synonym(tok: str) -> str:
    try:
        from nltk.corpus import wordnet as wn
        ss = wn.synsets(tok.lower())
    except LookupError:
        ss = []
    if ss:
        for lem in ss[0].lemma_names():
            w = lem.replace("_", " ").replace("-", " ")
            if w.lower() != tok.lower() and w.split()[0].isalpha():
                return "".join(p.capitalize() for p in w.split())
    return tok[::-1].capitalize() + "Q"


def _rename_pred(name: str, token_alignable: bool) -> str:
    parts = TOKRE.findall(name)
    if not parts:
        return name + "Q"
    head = parts[0]
    new = (head + "s") if token_alignable else _synonym(head)
    i = name.find(head)
    out = name[:i] + new[0].upper() + new[1:] + name[i + len(head):]
    return out if out != name else name + "Q"


def _map_atoms(e, pmap, cmap, bv=frozenset()):
    k = e[0]
    if k == "atom":
        return ("atom", pmap.get(e[1], e[1]), tuple(x if x in bv else cmap.get(x, x) for x in e[2]))
    if k in ("all", "ex"):
        return (k, e[1], _map_atoms(e[2], pmap, cmap, bv | {e[1]}))
    if k == "not":
        return ("not", _map_atoms(e[1], pmap, cmap, bv))
    return (k, _map_atoms(e[1], pmap, cmap, bv), _map_atoms(e[2], pmap, cmap, bv))


def rename_rewrite(e, token_alignable: bool = False, preds: bool = True, consts: bool = True):
    P, C = symbols(e)
    names = sorted({p[0] for p in P}) if preds else []
    pmap, used = {}, set(names)
    for n in names:
        new = _rename_pred(n, token_alignable)
        while new in used:
            new += "Q"
        used.add(new)
        pmap[n] = new
    cmap = {} if (token_alignable or not consts) else {c: "c_" + hashlib.sha1(c.encode()).hexdigest()[:4] for c in sorted(C)}
    return _map_atoms(e, pmap, cmap), {"pmap": pmap, "cmap": cmap}


def inverse_rename(e, maps):
    return _map_atoms(e, {v: k for k, v in maps["pmap"].items()}, {v: k for k, v in maps["cmap"].items()})


def reorder(e):
    k = e[0]
    if k == "atom":
        return e
    if k in ("all", "ex"):
        return (k, e[1], reorder(e[2]))
    if k == "not":
        return ("not", reorder(e[1]))
    a, b = reorder(e[1]), reorder(e[2])
    return (k, b, a) if k in ("and", "or") else (k, a, b)


def _first(e, kind):
    """Rewrite the first (preorder) node of `kind` with De Morgan; returns (new, done)."""
    k = e[0]
    if k == kind:
        dual = "or" if kind == "and" else "and"
        return ("not", (dual, ("not", e[1]), ("not", e[2]))), True
    if k == "atom":
        return e, False
    if k in ("all", "ex"):
        b, d = _first(e[2], kind)
        return (k, e[1], b), d
    if k == "not":
        b, d = _first(e[1], kind)
        return ("not", b), d
    a, d = _first(e[1], kind)
    if d:
        return (k, a, e[2]), True
    b, d = _first(e[2], kind)
    return (k, e[1], b), d


def demorgan(e):
    new, done = _first(e, "and")
    if not done:
        new, done = _first(e, "or")
    return new if done else None


def free_vars(e, bound=frozenset()) -> set:
    k = e[0]
    if k == "atom":
        return set()  # atom arguments that are not bound are constants in this notation
    if k in ("all", "ex"):
        return free_vars(e[2], bound | {e[1]})
    if k == "not":
        return free_vars(e[1], bound)
    return free_vars(e[1], bound) | free_vars(e[2], bound)


def _args(e) -> set:
    k = e[0]
    if k == "atom":
        return set(e[2])
    if k in ("all", "ex"):
        return _args(e[2]) | {e[1]}
    if k == "not":
        return _args(e[1])
    return _args(e[1]) | _args(e[2])


def _prenex_once(e):
    k = e[0]
    if k in ("and", "or"):
        for qi, oi in ((1, 2), (2, 1)):
            q, other = e[qi], e[oi]
            if q[0] in ("all", "ex") and q[1] not in _args(other):
                body = (k, q[2], other) if qi == 1 else (k, other, q[2])
                return (q[0], q[1], body)
    if k == "imp":
        q, other = e[2], e[1]
        if q[0] in ("all", "ex") and q[1] not in _args(other):
            return (q[0], q[1], ("imp", other, q[2]))
    if k == "atom":
        return None
    kids = [2] if k in ("all", "ex") else ([1] if k == "not" else [1, 2])
    for i in kids:  # an equivalence-preserving move inside a sub-formula is sound anywhere
        sub = _prenex_once(e[i])
        if sub is not None:
            lst = list(e)
            lst[i] = sub
            return tuple(lst)
    return None


def prenex(e):
    """Pull one quantifier to a wider scope where the move is sound; None when no such move exists."""
    return _prenex_once(e)


def contrapositive(e):
    k = e[0]
    if k == "atom":
        return e
    if k in ("all", "ex"):
        return (k, e[1], contrapositive(e[2]))
    if k == "not":
        return ("not", contrapositive(e[1]))
    a, b = contrapositive(e[1]), contrapositive(e[2])
    return ("imp", ("not", b), ("not", a)) if k == "imp" else (k, a, b)


FAMILIES = {"RENAME": lambda e: rename_rewrite(e)[0], "REORDER": reorder, "DEMORGAN": demorgan,
            "PRENEX": prenex, "CONTRAPOSITIVE": contrapositive,
            # decomposition of RENAME (added after the first run to locate where the aligner fails)
            "RENAME_PRED_ONLY": lambda e: rename_rewrite(e, consts=False)[0],
            "RENAME_CONST_ONLY": lambda e: rename_rewrite(e, preds=False)[0]}


def to_str(e) -> str:
    """Render an AST back to FOLIO-style Unicode FOL (fully parenthesised binary nodes)."""
    k = e[0]
    if k == "atom":
        return f"{e[1]}({', '.join(e[2])})" if e[2] else e[1]
    if k in ("all", "ex"):
        return f"{'∀' if k == 'all' else '∃'}{e[1]} ({to_str(e[2])})"
    if k == "not":
        return f"¬({to_str(e[1])})"
    sym = {"and": "∧", "or": "∨", "imp": "→", "iff": "↔", "xor": "⊕"}[k]
    return f"({to_str(e[1])} {sym} {to_str(e[2])})"
