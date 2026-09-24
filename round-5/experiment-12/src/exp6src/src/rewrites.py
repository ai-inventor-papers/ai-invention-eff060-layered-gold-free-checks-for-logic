"""Meaning-preserving rewrites of CORRECT candidates (invariance set). Every kept rewrite is z3-equivalent to its
base (RENAME: identical AST under the inverse name map) and differs as a string.

Families: RENAME (WordNet synonym of the head word, else name+'Thing'), REORDER (shuffle ∧/∨ operands),
DEMORGAN (push/pull one negation through ∧/∨), PRENEX (pull a quantifier out of ∧/∨/→-consequent when no clash),
CONTRAPOSITIVE (A→B => ¬B→¬A, first →), plus REPRINT (control: same AST, canonical re-printing) to separate
formatting sensitivity from meaning-preserving change.
"""
from __future__ import annotations

import random
import re

from .labeller.fol import parse, equivalent
from .labeller.repair_census import rename, symbols, bound_vars

PREC = {"iff": 1, "imp": 2, "or": 3, "xor": 3, "and": 4}
SYM = {"iff": "↔", "imp": "→", "or": "∨", "xor": "⊕", "and": "∧"}


def to_str(e) -> str:
    """Printer that round-trips through fol.parse (fully safe parenthesisation of binary sub-terms)."""
    k = e[0]
    if k == "atom":
        return f"{e[1]}({', '.join(e[2])})" if e[2] else e[1]
    if k in ("all", "ex"):
        q = "∀" if k == "all" else "∃"
        return f"{q}{e[1]} ({to_str(e[2])})"
    if k == "not":
        inner = e[1]
        s = to_str(inner)
        return f"¬{s}" if inner[0] in ("atom", "not") else f"¬({s})"
    op = k

    def side(x, right):
        s = to_str(x)
        if x[0] in PREC:
            px, p = PREC[x[0]], PREC[op]
            if px < p or (px == p and (x[0] != op or op in ("imp", "iff", "xor") or right)):
                return f"({s})"
        return s
    return f"{side(e[1], False)} {SYM[op]} {side(e[2], True)}"


def _vars_in(e):
    """All variable-like argument names occurring in e (bound anywhere in the whole formula are passed separately)."""
    k = e[0]
    if k == "atom":
        return set(e[2])
    if k in ("all", "ex"):
        return _vars_in(e[2])
    if k == "not":
        return _vars_in(e[1])
    return _vars_in(e[1]) | _vars_in(e[2])



def reorder(e, rng):
    k = e[0]
    if k in ("and", "or"):
        ops = []

        def flat(x):
            if x[0] == k:
                flat(x[1]); flat(x[2])
            else:
                ops.append(reorder(x, rng))
        flat(e)
        orig = list(ops)
        rng.shuffle(ops)
        if ops == orig and len(ops) > 1:  # force a different operand order when the shuffle is the identity
            ops = ops[1:] + ops[:1]
        out = ops[0]
        for x in ops[1:]:
            out = (k, out, x)
        return out
    if k == "atom":
        return e
    if k in ("all", "ex"):
        return (k, e[1], reorder(e[2], rng))
    if k == "not":
        return ("not", reorder(e[1], rng))
    return (k, reorder(e[1], rng), reorder(e[2], rng))


def _first(e, pred, path=()):
    if pred(e):
        return path
    k = e[0]
    kids = [] if k == "atom" else ([2] if k in ("all", "ex") else ([1] if k == "not" else [1, 2]))
    for i in kids:
        r = _first(e[i], pred, path + (i,))
        if r is not None:
            return r
    return None


def _get(e, path):
    for i in path:
        e = e[i]
    return e


def _set(e, path, new):
    if not path:
        return new
    lst = list(e)
    lst[path[0]] = _set(e[path[0]], path[1:], new)
    return tuple(lst)


def demorgan(e):
    p = _first(e, lambda x: x[0] == "not" and x[1][0] in ("and", "or"))
    if p is not None:
        n = _get(e, p)[1]
        dual = "or" if n[0] == "and" else "and"
        return _set(e, p, (dual, ("not", n[1]), ("not", n[2])))
    p = _first(e, lambda x: x[0] == "and")
    if p is not None:
        n = _get(e, p)
        return _set(e, p, ("not", ("or", ("not", n[1]), ("not", n[2]))))
    p = _first(e, lambda x: x[0] == "or")
    if p is not None:
        n = _get(e, p)
        return _set(e, p, ("not", ("and", ("not", n[1]), ("not", n[2]))))
    return None


def contrapositive(e):
    p = _first(e, lambda x: x[0] == "imp")
    if p is None:
        return None
    n = _get(e, p)
    return _set(e, p, ("imp", ("not", n[2]), ("not", n[1])))


def prenex(e):
    """Pull one quantifier out: (Qx φ) ∘ ψ -> Qx (φ ∘ ψ) for ∘ ∈ {∧,∨}, ψ ∘ (Qx φ) likewise, ψ → Qx φ -> Qx (ψ → φ),
    when x does not occur in ψ (no clash)."""
    def pull(x):
        k = x[0]
        if k in ("and", "or"):
            a, b = x[1], x[2]
            if a[0] in ("all", "ex") and a[1] not in _vars_in(b) and a[1] not in bound_vars(b):
                return (a[0], a[1], (k, a[2], b))
            if b[0] in ("all", "ex") and b[1] not in _vars_in(a) and b[1] not in bound_vars(a):
                return (b[0], b[1], (k, a, b[2]))
        if k == "imp":
            a, b = x[1], x[2]
            if b[0] in ("all", "ex") and b[1] not in _vars_in(a) and b[1] not in bound_vars(a):
                return (b[0], b[1], ("imp", a, b[2]))
        return None
    p = _first(e, lambda x: pull(x) is not None)
    if p is None:
        return None
    return _set(e, p, pull(_get(e, p)))


def _synonym(word: str, avoid: set) -> str | None:
    from nltk.corpus import wordnet as wn
    for s in wn.synsets(word):
        for l in s.lemma_names():
            l2 = l.replace("-", "_")
            if "_" in l2 or l2.lower() == word.lower() or not l2.isalpha():
                continue
            if l2.lower() in avoid:
                continue
            return l2.lower()
    return None


def rename_symbols(e):
    """Predicate head word -> WordNet synonym (else +Thing); constants -> synonym or +Thing. Returns (e2, pmap, cmap)."""
    P, C = symbols(e)
    CAMEL = re.compile(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+")
    names = {p[0] for p in P} | set(C)
    avoid = {n.lower() for n in names}
    pmap, cmap, used = {}, {}, set(names)

    def newname(name, is_pred):
        parts = CAMEL.findall(name) or [name]
        head = parts[-1]
        syn = _synonym(head.lower(), avoid)
        if syn:
            rep = syn.capitalize() if head[:1].isupper() else syn
            cand = "".join(parts[:-1]) + rep if len(parts) > 1 else (rep.capitalize() if is_pred else rep)
        else:
            cand = name + ("Thing" if is_pred else "Thing")
        while cand in used:
            cand += "X"
        used.add(cand)
        return cand
    for p in sorted(P):
        pmap[p] = newname(p[0], True)
    for c in sorted(C):
        cmap[c] = newname(c, False)
    return rename(e, pmap, cmap), pmap, cmap


def make_rewrites(base_items: list[dict], seed: int = 0) -> tuple[list[dict], dict]:
    rng = random.Random(seed)
    out, stats = [], {}
    for it in base_items:
        s0 = it["candidate_fol"]
        try:
            e0 = parse(s0)
        except Exception:  # noqa: BLE001
            continue
        fams = {}
        fams["REPRINT"] = e0
        fams["REORDER"] = reorder(e0, rng)
        fams["DEMORGAN"] = demorgan(e0)
        fams["PRENEX"] = prenex(e0)
        fams["CONTRAPOSITIVE"] = contrapositive(e0)
        try:
            e_r, pmap, cmap = rename_symbols(e0)
            fams["RENAME"] = e_r
        except Exception:  # noqa: BLE001
            fams["RENAME"] = None
            pmap, cmap = {}, {}
        for fam, e1 in fams.items():
            st = stats.setdefault(fam, {"applicable": 0, "kept": 0, "not_equiv": 0, "same_string": 0})
            if e1 is None:
                continue
            st["applicable"] += 1
            s1 = to_str(e1)
            try:
                if parse(s1) != e1:
                    st["not_equiv"] += 1
                    continue
            except Exception:  # noqa: BLE001
                st["not_equiv"] += 1
                continue
            if s1.strip() == s0.strip():
                st["same_string"] += 1
                continue
            if fam == "RENAME":
                inv_p = {(v, k[1]): k[0] for k, v in pmap.items()}
                inv_c = {v: k for k, v in cmap.items()}
                ok = rename(parse(s1), inv_p, inv_c) == e0
            else:
                ok = equivalent(e0, e1, 5000) is True
            if not ok:
                st["not_equiv"] += 1
                continue
            st["kept"] += 1
            out.append({"rw_id": f"{it['item_id']}_{fam}", "base_item_id": it["item_id"], "family": fam,
                        "text": it["text"], "candidate_fol": s1, "system": it["system"], "track": it["track"],
                        "story_premises_fol": it.get("story_premises_fol", []),
                        "declared_predicates": it.get("declared_predicates", []),
                        "rename_map": {f"{k[0]}/{k[1]}": v for k, v in pmap.items()} | cmap if fam == "RENAME" else None})
    return out, stats
