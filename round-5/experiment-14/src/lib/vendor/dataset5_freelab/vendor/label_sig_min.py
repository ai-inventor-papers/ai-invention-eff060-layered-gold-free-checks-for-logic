"""Extracted verbatim from ../../../../../../../round-3/experiment-7/src/src/label_sig.py (sha256 390349ae0f20d8f2a288a9e2c96e436dd2de34599f0b8a172168a6a4a1499f3e): _to_str, _rename, _free_consts."""
from __future__ import annotations


def _to_str(e) -> str:
    k = e[0]
    if k == "atom":
        return f"{e[1]}({', '.join(e[2])})" if e[2] else e[1]
    if k in ("all", "ex"):
        return f"{'∀' if k == 'all' else '∃'}{e[1]} ({_to_str(e[2])})"
    if k == "not":
        return f"¬({_to_str(e[1])})"
    sym = {"and": "∧", "or": "∨", "imp": "→", "iff": "↔", "xor": "⊕"}[k]
    return f"({_to_str(e[1])} {sym} {_to_str(e[2])})"


def _rename(e, pmap: dict, cmap: dict, bv=frozenset()):
    k = e[0]
    if k == "atom":
        return ("atom", pmap.get(e[1], e[1]), tuple(x if x in bv else cmap.get(x, x) for x in e[2]))
    if k in ("all", "ex"):
        return (k, e[1], _rename(e[2], pmap, cmap, bv | {e[1]}))
    if k == "not":
        return ("not", _rename(e[1], pmap, cmap, bv))
    return (k, _rename(e[1], pmap, cmap, bv), _rename(e[2], pmap, cmap, bv))


def _free_consts(e) -> set:
    out = set()

    def walk(x, bv):
        if x[0] == "atom":
            out.update(a for a in x[2] if a not in bv)
        elif x[0] in ("all", "ex"):
            walk(x[2], bv | {x[1]})
        elif x[0] == "not":
            walk(x[1], bv)
        else:
            walk(x[1], bv); walk(x[2], bv)
    walk(e, frozenset())
    return out
