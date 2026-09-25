"""Reusable pair-class instruments for the vocabulary split (label-free, CPU only).

name_only_eq(fol_a, fol_b) -> (True/False/None, reason)
    WHAT IT MEASURES: whether two FOL formulas become z3-EXACTLY equivalent once every predicate and constant symbol
    of BOTH is rewritten with mechanism.normalise_name (lowercase, strip non-alphanumerics), i.e. whether they differ
    only in the SPELLING of their vocabulary (case, underscores, punctuation), never in its choice.
    Arity must agree (the normalised (name, arity) multisets and constant sets must be equal - a sound prefilter);
    two distinct symbols of ONE formula that normalise to the same string disqualify the pair ('collision').
    Pairs whose ORIGINAL signatures already coincide return False ('same_signature'): normalisation is then a
    consistent injective renaming of both sides and cannot create an equivalence z3 did not already find.
    z3 via the iteration-1 _eq (fingerprint prefilter + z3, 3000 ms), SIGALRM cap 30 s; UNKNOWN -> None (= no).
"""
from __future__ import annotations

from collections import Counter

import t8_paths  # noqa: F401  (eval-2 sys.path shim)


def _sig(PT, MC, e):
    """(normalised pred multiset, normalised constant set, collision?, original signature)."""
    pk = list(PT.pred_keys(e))
    cs = list(PT.constants(e))
    npred = [MC.normalise_name(n) for n, _ in pk]
    ncons = [MC.normalise_name(c) for c in cs]
    collide = len(set(npred)) < len(npred) or len(set(ncons)) < len(ncons)
    return (Counter((MC.normalise_name(n), a) for n, a in pk), frozenset(ncons), collide,
            (frozenset(pk), frozenset(cs)))


def name_only_prefilter(fa: str, fb: str) -> str:
    """'z3' if the pair needs a z3 call, otherwise the reason it cannot be NAME_ONLY."""
    import mechanism as MC
    import peer_text as PT
    a, b = PT.parse_fol(fa), PT.parse_fol(fb)
    if a is None or b is None:
        return "unparseable"
    sa, sb = _sig(PT, MC, a), _sig(PT, MC, b)
    if sa[2] or sb[2]:
        return "collision"
    if sa[3] == sb[3]:
        return "same_signature"
    if sa[0] != sb[0] or sa[1] != sb[1]:
        return "signature_differs"
    return "z3"


def normalise_formula(e):
    import mechanism as MC
    import peer_text as PT
    pmap = {k: MC.normalise_name(k[0]) for k in PT.pred_keys(e)}
    cmap = {c: MC.normalise_name(c) for c in PT.constants(e)}
    return PT.rename(e, pmap, cmap)


def name_only_eq(fa: str, fb: str, ms: int = 3000, cap_s: int = 30) -> tuple[bool | None, str]:
    """See module docstring."""
    pre = name_only_prefilter(fa, fb)
    if pre != "z3":
        return False, pre
    import pairwise as PW
    import peer_text as PT
    from common import _eq
    a, b = normalise_formula(PT.parse_fol(fa)), normalise_formula(PT.parse_fol(fb))
    res, to = PW._with_alarm(cap_s, _eq, a, b, ms)
    if to or res is None:
        return None, "unknown"
    return bool(res is True), "z3"


def work_name_only(pair: tuple[str, str]) -> tuple[str, str, bool | None, str]:
    r, why = name_only_eq(*pair)
    return pair[0], pair[1], r, why
