"""Shared solver-backed labeller (screen AND held-out use this one module).

Wraps repair_census.py's work() pipeline into reusable functions WITHOUT changing the algorithm
(same aligner thresholds, same gran/reify bridge, same typed operators and fingerprint pre-filter):

  equivalent_modulo_vocab(cand, ref) -> 'EQ' | 'VOCAB' | 'GRAN' | 'NONEQ' | 'UNKNOWN'
      EQ     plain z3 equivalence with identical symbols (fol.equivalent, 3 s timeout)
      VOCAB  equivalent after renaming cand's predicates/constants onto ref's (repair_census.align)
      GRAN   equivalent after a merge/split/reification definitional bridge (repair_census.gran_bridge)
      NONEQ  z3 refuted every stage
      UNKNOWN some stage timed out and no stage proved equivalence
  minimal_typed_repair(cand, ref, budget_s=8) -> (ops | None, secs, status)
      status FOUND (ops = sorted operator labels, depth <= 2), EXHAUSTED (full depth-2 space searched,
      no repair: COMPOUND_EXHAUSTED) or TIMEOUT (budget or candidate cap hit: COMPOUND_TIMEOUT).
  convention_flags(cand, ref) -> list of DIAGNOSTIC flags (never change auto_label):
      SORTAL, XOR_OR, ARITY_REIFY, CONST_VS_EXISTS
  auto_label(cand_str, ref_str, budget_s) -> dict(auto_label, equiv_status, repair_ops, repair_status, ...)

Arguments are parsed ASTs (fol.parse) unless the name says _str. Deviation from repair_census.search:
the depth-2 time budget is a parameter (default 8 s instead of 25 s), and the outcome of a failed
search is reported as EXHAUSTED vs TIMEOUT instead of a bare None.
"""
from __future__ import annotations

import time

import z3

from fol import parse, preds, to_z3, mkpred, valid
from repair_census import align, gran_bridge, edits, fp, symbols, atoms

EQ_MS = 3000


def _equiv(e1, e2, ms: int = EQ_MS):
    ar = {**preds(e1), **preds(e2)}
    P = {q: mkpred(q, m) for q, m in ar.items()}
    return valid(to_z3(e1, {}, P) == to_z3(e2, {}, P), ms)


def _stages(cand, ref):
    """Run ALIGN / GRAN exactly as repair_census.work(); return (status, base, tgt)."""
    unknown = False
    r = _equiv(cand, ref)
    if r is True:
        return "EQ", cand, ref
    unknown |= r is None
    ao, _, _ = align(cand, ref)
    r = _equiv(ao, ref)
    if r is True:
        return "VOCAB", ao, ref
    unknown |= r is None
    gb = gran_bridge(ao, ref)
    if gb:
        r = _equiv(gb[0], gb[1])
        if r is True:
            return "GRAN", gb[0], gb[1]
        unknown |= r is None
    base, tgt = gb if gb else (ao, ref)
    return ("UNKNOWN" if unknown else "NONEQ"), base, tgt


def equivalent_modulo_vocab(cand, ref) -> str:
    return _stages(cand, ref)[0]


def _search(ao, target, budget_s: float, max_d2: int = 6000):
    """repair_census.search with an explicit outcome status."""
    ft = fp(target)
    t0 = time.time()
    lvl1, seen = [], set()
    for lab, c in edits(ao, target):
        s = str(c)
        if s in seen:
            continue
        seen.add(s)
        lvl1.append((lab, c))
        if fp(c) == ft and _equiv(c, target, ms=1500) is True:
            return [lab], time.time() - t0, "FOUND"
        if time.time() - t0 > 3 * budget_s:  # guard only; level 1 is normally < 1 s
            return None, time.time() - t0, "TIMEOUT"
    n = 0
    for lab1, c1 in lvl1:
        for lab2, c2 in edits(c1, target):
            n += 1
            if lab1 == "NEG" and lab2 == "NEG":
                continue
            if n > max_d2 * 10 or time.time() - t0 > budget_s:
                return None, time.time() - t0, "TIMEOUT"
            if fp(c2) == ft and _equiv(c2, target, ms=1500) is True:
                return sorted([lab1, lab2]), time.time() - t0, "FOUND"
    return None, time.time() - t0, "EXHAUSTED"


def minimal_typed_repair(cand, ref, budget_s: float = 8.0):
    st, base, tgt = _stages(cand, ref)
    if st in ("EQ", "VOCAB", "GRAN"):
        return [], 0.0, "FOUND"
    return _search(base, tgt, budget_s)


# ---------------------------------------------------------------- diagnostic convention flags
SORTALS = {"Person", "Human", "People", "Thing", "Entity", "Object", "Individual", "Persons", "Humans"}
TAUT = ("or", ("atom", "TautAtom__", ()), ("not", ("atom", "TautAtom__", ())))


def _drop_sortals(e):
    k = e[0]
    if k == "atom":
        return TAUT if (e[1] in SORTALS and len(e[2]) == 1) else e
    if k in ("all", "ex"):
        return (k, e[1], _drop_sortals(e[2]))
    if k == "not":
        return ("not", _drop_sortals(e[1]))
    return (k, _drop_sortals(e[1]), _drop_sortals(e[2]))


def _xor_to_or(e):
    k = e[0]
    if k == "atom":
        return e
    if k in ("all", "ex"):
        return (k, e[1], _xor_to_or(e[2]))
    if k == "not":
        return ("not", _xor_to_or(e[1]))
    return ("or" if k == "xor" else k, _xor_to_or(e[1]), _xor_to_or(e[2]))


def _count(e, kind):
    if e[0] == "atom":
        return 0
    if e[0] in ("all", "ex"):
        return (e[0] == kind) + _count(e[2], kind)
    if e[0] == "not":
        return _count(e[1], kind)
    return (e[0] == kind) + _count(e[1], kind) + _count(e[2], kind)


def convention_flags(cand, ref) -> list[str]:
    flags = []
    try:
        pc = {p[0] for p in symbols(cand)[0]}
        pr = {p[0] for p in symbols(ref)[0]}
        if (pc ^ pr) & SORTALS and equivalent_modulo_vocab(_drop_sortals(cand), _drop_sortals(ref)) in ("EQ", "VOCAB", "GRAN"):
            flags.append("SORTAL")
        if (_count(cand, "xor") or _count(ref, "xor")) and _count(cand, "xor") != _count(ref, "xor"):
            if equivalent_modulo_vocab(_xor_to_or(cand), _xor_to_or(ref)) in ("EQ", "VOCAB", "GRAN"):
                flags.append("XOR_OR")
        ac = {p[0].lower(): p[1] for p in symbols(cand)[0]}
        ar = {p[0].lower(): p[1] for p in symbols(ref)[0]}
        if any(n in ar and ar[n] != a for n, a in ac.items()):
            flags.append("ARITY_REIFY")
        cc, cr = symbols(cand)[1], symbols(ref)[1]
        if (len(cc) != len(cr)) and (_count(cand, "ex") != _count(ref, "ex")):
            flags.append("CONST_VS_EXISTS")
    except (RecursionError, z3.Z3Exception, KeyError):
        flags.append("FLAG_ERROR")
    return flags


def auto_label(cand_str: str, ref_str: str, budget_s: float = 8.0, repair: bool = True) -> dict:
    """Label map: EQ->CORRECT; VOCAB/GRAN->VOCAB_GRAN; NONEQ+FOUND->ERROR(ops);
    NONEQ+EXHAUSTED/TIMEOUT->COMPOUND; parse failure->UNPARSEABLE; UNKNOWN->TIMEOUT_UNKNOWN."""
    t0 = time.time()
    if not (cand_str or "").strip():
        return {"auto_label": "UNPARSEABLE", "equiv_status": None, "repair_ops": None, "repair_status": None,
                "parse_error": "empty", "secs": 0.0}
    try:
        c = parse(cand_str)
    except Exception as ex:  # noqa: BLE001 - parser raises ValueError/IndexError/TypeError on junk
        return {"auto_label": "UNPARSEABLE", "equiv_status": None, "repair_ops": None, "repair_status": None,
                "parse_error": str(ex)[:120], "secs": 0.0}
    r = parse(ref_str)
    st, base, tgt = _stages(c, r)
    out = {"equiv_status": st, "repair_ops": None, "repair_status": None}
    if st == "EQ":
        out["auto_label"] = "CORRECT"
    elif st in ("VOCAB", "GRAN"):
        out["auto_label"] = "VOCAB_GRAN"
    elif st == "UNKNOWN":
        out["auto_label"] = "TIMEOUT_UNKNOWN"
    elif not repair:
        out["auto_label"] = "NONEQ_UNREPAIRED"
    else:
        ops, secs, rs = _search(base, tgt, budget_s)
        out["repair_status"] = rs if rs == "FOUND" else f"COMPOUND_{rs}"
        out["repair_secs"] = round(secs, 2)
        if rs == "FOUND":
            out["auto_label"], out["repair_ops"] = "ERROR", ops
        else:
            out["auto_label"] = "COMPOUND"
    out["convention_flags"] = convention_flags(c, r) if out["auto_label"] not in ("CORRECT",) else []
    out["secs"] = round(time.time() - t0, 2)
    return out
