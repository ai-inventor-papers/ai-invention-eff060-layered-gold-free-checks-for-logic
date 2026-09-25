"""Shared primitives of the frozen screen: text normalisation, item ids, the automatic labeller,
equivalence-modulo-vocabulary (eqmv) and the complexity strata.

The labeller reproduces the iter-3 repair census (repair_census.work) stage by stage, so the label
vector is identical to sibling experiments A/B/D and dataset E (EQUIV+VOCAB -> CORRECT,
GRAN -> UNCERTAIN_GRAN, depth<=2 repair -> ERROR[ops], no repair -> UNCERTAIN_COMPOUND).
"""
from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.setrecursionlimit(10000)

from fol import equivalent, parse  # noqa: E402
from repair_census import align, atoms, fp, gran_bridge, search, toks  # noqa: E402

LLM_SYSTEMS = ["gpt-3.5-turbo", "gpt-4", "text-davinci-003"]
EXC_RE = re.compile(r"\b(unless|except|excluding|other than|apart from|but not|without)\b")
COARSE = {"ADD": "COVERAGE", "DROP": "COVERAGE", "NEG": "POLARITY", "REV": "POLARITY", "QUANT": "POLARITY"}


def norm(t: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", t.lower())).strip()


def item_id(system: str, text: str, fol: str) -> str:
    return hashlib.sha1((system + "|" + norm(text) + "|" + fol.strip()).encode()).hexdigest()[:16]


def safe_parse(s: str | None):
    if s is None or not str(s).strip():
        return None
    try:
        return parse(str(s))
    except (ValueError, IndexError, RecursionError, TypeError):
        return None


def vocab_strict(pmap: dict) -> bool:
    """Every renamed predicate pair has identical CamelCase token multisets."""
    return all(sorted(toks(k[0])) == sorted(toks(v)) for k, v in pmap.items())


def op_class(ops: list[str]) -> str:
    if not ops:
        return "NONE"
    cs = {COARSE.get(o, "STRUCT") for o in ops}
    return cs.pop() if len(cs) == 1 else "MIXED"


def label(cand: str, ref: str, ambiguous: bool = False, track: str = "L", budget_s: float = 25.0) -> dict:
    """LABEL(cand, ref, ambiguous) -> {label, auto_class, repair_ops, vocab_strict, pmap}.

    Stage order and z3 timeouts are those of repair_census.work (equivalent() default ms=5000)."""
    out = {"label": None, "auto_class": None, "repair_ops": [], "vocab_strict": None, "pmap": {}}
    ce, re_ = safe_parse(cand), safe_parse(ref)
    if re_ is None:
        out.update(label="REF_UNPARSEABLE", auto_class="REF_UNPARSEABLE")
        return out
    if ce is None:
        out.update(label="UNPARSEABLE", auto_class="UNPARSEABLE")
        return _reading(out, ambiguous, track)
    timeouts = False
    r = equivalent(ce, re_)
    if r is True:
        out.update(label="CORRECT", auto_class="EQUIV", vocab_strict=True)
        return out
    timeouts |= r is None
    ac, pmap, cmap = align(ce, re_)
    out["pmap"] = {f"{k[0]}/{k[1]}": v for k, v in pmap.items()}
    r = equivalent(ac, re_)
    if r is True:
        out.update(label="CORRECT", auto_class="VOCAB", vocab_strict=vocab_strict(pmap))
        return out
    timeouts |= r is None
    gb = gran_bridge(ac, re_)
    if gb:
        r = equivalent(gb[0], gb[1])
        if r is True:
            out.update(label="UNCERTAIN_GRAN", auto_class="GRAN")
            return _reading(out, ambiguous, track)
        timeouts |= r is None
    if timeouts:
        out.update(label="TIMEOUT_UNKNOWN", auto_class="TIMEOUT")
        return _reading(out, ambiguous, track)
    base, tgt = gb if gb else (ac, re_)
    ops, _ = search(base, tgt, budget_s=budget_s)
    if ops:
        out.update(label="ERROR", auto_class="+".join(ops), repair_ops=list(ops))
    else:
        out.update(label="UNCERTAIN_COMPOUND", auto_class="COMPOUND")
    return _reading(out, ambiguous, track)


def _reading(out: dict, ambiguous: bool, track: str) -> dict:
    """Track H: curator-flagged ambiguous items that are not CORRECT become READING_CHOICE."""
    if track == "H" and ambiguous and out["label"] != "CORRECT":
        out["underlying_label"] = out["label"]
        out["label"] = "READING_CHOICE"
    return out


# ------------------------------------------------------------------ equivalence modulo vocabulary
def _eq(a, b, ms):
    """z3 equivalence with the random-model fingerprint as a sound necessary-condition pre-filter."""
    if fp(a) != fp(b):
        return False
    return equivalent(a, b, ms=ms)


def eqmv(a, b, ms: int = 3000) -> tuple[bool | None, str]:
    """Symmetric equivalence modulo vocabulary: exact, then align() either direction, then gran_bridge."""
    to = False
    r = _eq(a, b, ms)
    if r is True:
        return True, "exact"
    to |= r is None
    for x, y in ((a, b), (b, a)):
        ax = align(x, y)[0]
        r = _eq(ax, y, ms)
        if r is True:
            return True, "align"
        to |= r is None
        gb = gran_bridge(ax, y)
        if gb:
            r = _eq(gb[0], gb[1], ms)
            if r is True:
                return True, "gran"
            to |= r is None
    return (None if to else False), "none"


# ------------------------------------------------------------------ strata
def _depth(e) -> int:
    k = e[0]
    if k == "atom":
        return 0
    if k in ("all", "ex"):
        return 1 + _depth(e[2])
    if k == "not":
        return 1 + _depth(e[1])
    return 1 + max(_depth(e[1]), _depth(e[2]))


def _count(e, kinds) -> int:
    k = e[0]
    n = 1 if k in kinds else 0
    if k == "atom":
        return n
    if k in ("all", "ex"):
        return n + _count(e[2], kinds)
    if k == "not":
        return n + _count(e[1], kinds)
    return n + _count(e[1], kinds) + _count(e[2], kinds)


def _conjuncts(e) -> int:
    return _conjuncts(e[1]) + _conjuncts(e[2]) if e[0] == "and" else 1


def _ncond(e) -> int:
    k = e[0]
    if k == "atom":
        return 0
    if k in ("all", "ex"):
        return _ncond(e[2])
    if k == "not":
        return _ncond(e[1])
    n = _conjuncts(e[1]) if k == "imp" else 0
    return n + _ncond(e[1]) + _ncond(e[2])


def strata(text: str, ref_fol: str) -> dict:
    words = len(text.split())
    e = safe_parse(ref_fol)
    m = EXC_RE.search(text.lower())
    out = {"words": words, "len_bin": "<12" if words < 12 else ("12-19" if words < 20 else ">=20"),
           "exception": bool(m), "exception_marker": m.group(1) if m else None}
    if e is None:
        out.update(n_quant=None, depth=None, n_cond=None)
    else:
        out.update(n_quant=_count(e, ("all", "ex")), depth=_depth(e), n_cond=_ncond(e))
    return out


def medoid_repair(c, m, budget_s: float = 10.0) -> tuple[int, list[str]]:
    """Minimal typed repair from candidate c to medoid m (after align + gran bridge)."""
    ac = align(c, m)[0]
    gb = gran_bridge(ac, m)
    base, tgt = gb if gb else (ac, m)
    ops, _ = search(base, tgt, budget_s=budget_s)
    return (len(ops), list(ops)) if ops else (3, ["COMPOUND"])


def alignable_frac(cand, ref) -> float | None:
    """Fraction of candidate predicates identical to, or align()-mapped onto, a reference predicate."""
    if cand is None or ref is None:
        return None
    from repair_census import symbols
    pc, _ = symbols(cand)
    pr, _ = symbols(ref)
    if not pc:
        return 1.0
    _, pmap, _ = align(cand, ref)
    ok = sum(1 for p in pc if p in pr or p in pmap)
    return ok / len(pc)
