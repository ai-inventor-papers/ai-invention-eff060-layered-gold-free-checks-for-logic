"""Shared-screen labeller: equivalence of a candidate FOL formula to a trusted reference MODULO VOCABULARY.

Exact sequence of iter-3 repair_census.work (equivalent -> align -> equivalent -> gran_bridge -> equivalent -> search),
wrapped as equivalent_modulo_vocab(cand, ref) -> dict. Differences from iter 3 (all logged in README):
  * fol.py PREC['xor'] = 3 (⊕ binds like ∨, tighter than →)  -- the iter-3 review bug fix;
  * the typed-repair search uses a DETERMINISTIC node budget (max level-2 candidates) instead of a wall-clock budget, so
    the label vector does not depend on machine load (a generous wall-clock guard remains and is reported if hit);
  * PYTHONHASHSEED must be fixed (the random-model fingerprint and set iteration orders use hash()); the caller
    (method.py) sets PYTHONHASHSEED=0 for every worker process.
"""
from __future__ import annotations

import re
import time

from .fol import parse, equivalent
from .repair_census import align, gran_bridge, edits, fp, toks

CORRECT_CLASSES = {"EQUIV", "VOCAB", "GRAN"}


def token_jaccard(a: str, b: str) -> float:
    ta, tb = set(toks(a)), set(toks(b))
    if not ta and not tb:
        return 1.0 if a.lower() == b.lower() else 0.0
    return len(ta & tb) / max(1, len(ta | tb))


def search_det(ao, target, max_l1: int = 4000, max_d2: int = 60000, wall_s: float = 150.0):
    """Breadth-first typed-repair search (depth <= 2), identical operator set to repair_census.search, but with a
    deterministic candidate budget. Returns (ops | None, n_equiv_timeouts, wall_hit)."""
    ft = fp(target)
    t0 = time.time()
    lvl1, seen = [], set()
    n_to = 0
    for lab, c in edits(ao, target):
        s = str(c)
        if s in seen:
            continue
        seen.add(s)
        if len(lvl1) < max_l1:
            lvl1.append((lab, c))
        if fp(c) == ft:
            r = equivalent(c, target, ms=1500)
            if r is True:
                return [lab], n_to, False
            if r is None:
                n_to += 1
    n = 0
    for lab1, c1 in lvl1:
        for lab2, c2 in edits(c1, target):
            n += 1
            if lab1 == "NEG" and lab2 == "NEG":
                continue
            if n > max_d2:
                return None, n_to, False
            if (n & 255) == 0 and time.time() - t0 > wall_s:
                return None, n_to, True
            if fp(c2) == ft:
                r = equivalent(c2, target, ms=1500)
                if r is True:
                    return sorted([lab1, lab2]), n_to, False
                if r is None:
                    n_to += 1
    return None, n_to, False


def equivalent_modulo_vocab(cand_str: str | None, ref_str: str, ms: int = 5000, do_search: bool = True) -> dict:
    """Classify a candidate against a reference.

    cls in {EQUIV, VOCAB, GRAN, ERROR, COMPOUND, TIMEOUT_UNKNOWN, UNPARSEABLE, REF_UNPARSEABLE}.
    VOCAB: equivalent after predicate/constant renaming (same arity) by the iter-3 aligner.
    GRAN: equivalent after a merge/split/reification definitional bridge.
    ERROR: a typed repair of depth <= 2 exists (ops = operator labels).
    COMPOUND: no repair within depth 2 (includes many vocabulary/granularity mismatches the aligner misses).
    TIMEOUT_UNKNOWN: every equivalence check timed out (never merged with EQUIV/UNSAT).
    """
    if cand_str is None or not str(cand_str).strip():
        return {"cls": "UNPARSEABLE", "why": "empty"}
    try:
        ref = parse(ref_str)
    except Exception as e:  # noqa: BLE001 - grammar errors are data, not bugs
        return {"cls": "REF_UNPARSEABLE", "why": str(e)[:120]}
    try:
        c = parse(cand_str)
    except Exception as e:  # noqa: BLE001
        return {"cls": "UNPARSEABLE", "why": str(e)[:120]}
    timeouts = 0
    try:
        r = equivalent(c, ref, ms)
    except Exception as e:  # noqa: BLE001 - z3 conversion failure (e.g. same name used as predicate and constant)
        return {"cls": "UNPARSEABLE", "why": "z3:" + str(e)[:100]}
    if r is True:
        return {"cls": "EQUIV"}
    if r is None:
        timeouts += 1
    ao, pmap, cmap = align(c, ref)
    renames = [(f"{k[0]}", v) for k, v in pmap.items()] + list(cmap.items())
    borderline = any(token_jaccard(p, q) < 0.5 for p, q in renames)
    pm = {f"{k[0]}/{k[1]}": v for k, v in pmap.items()}
    r = equivalent(ao, ref, ms)
    if r is True:
        return {"cls": "VOCAB", "pmap": pm, "cmap": cmap, "borderline": borderline}
    if r is None:
        timeouts += 1
    gb = gran_bridge(ao, ref)
    if gb:
        r = equivalent(gb[0], gb[1], ms)
        if r is True:
            return {"cls": "GRAN", "pmap": pm, "cmap": cmap, "borderline": True}
        if r is None:
            timeouts += 1
    if not do_search:
        return {"cls": "NONEQUIV_NOSEARCH", "pmap": pm, "cmap": cmap}
    base, tgt = (gb if gb else (ao, ref))
    ops, n_to, wall_hit = search_det(base, tgt)
    if ops:
        return {"cls": "ERROR", "ops": ops, "depth": len(ops), "pmap": pm, "cmap": cmap}
    n_calls = 3 if gb else 2
    if timeouts >= n_calls:  # every pre-search equivalence call timed out
        return {"cls": "TIMEOUT_UNKNOWN", "pmap": pm, "cmap": cmap}
    return {"cls": "COMPOUND", "pmap": pm, "cmap": cmap, "search_wall_hit": wall_hit, "search_equiv_timeouts": n_to}


def parse_ok(fol_str: str | None) -> bool:
    """Parses with the shared grammar AND converts to z3."""
    if fol_str is None:
        return False
    try:
        e = parse(fol_str)
        equivalent(e, e, 1000)
        return True
    except Exception:  # noqa: BLE001
        return False


def ast_depth(e) -> int:
    k = e[0]
    if k == "atom":
        return 1
    if k in ("all", "ex"):
        return 1 + ast_depth(e[2])
    if k == "not":
        return 1 + ast_depth(e[1])
    return 1 + max(ast_depth(e[1]), ast_depth(e[2]))


def n_quantifiers(e) -> int:
    k = e[0]
    if k == "atom":
        return 0
    if k in ("all", "ex"):
        return 1 + n_quantifiers(e[2])
    if k == "not":
        return n_quantifiers(e[1])
    return n_quantifiers(e[1]) + n_quantifiers(e[2])


def _conjuncts(e) -> int:
    return _conjuncts(e[1]) + _conjuncts(e[2]) if e[0] == "and" else 1


def n_conditions(e) -> int:
    """Number of conjuncts in the antecedents of → (and in ∀-restrictors, which are → antecedents in FOLIO notation)."""
    k = e[0]
    if k == "atom":
        return 0
    if k in ("all", "ex"):
        return n_conditions(e[2])
    if k == "not":
        return n_conditions(e[1])
    own = _conjuncts(e[1]) if k == "imp" else 0
    return own + n_conditions(e[1]) + n_conditions(e[2])


EXC_RE = re.compile(r"\b(unless|except|excluding|other than|apart from|but not|without)\b", re.I)
