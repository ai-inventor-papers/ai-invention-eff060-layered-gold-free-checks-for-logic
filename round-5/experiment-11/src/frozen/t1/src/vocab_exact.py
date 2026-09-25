"""VOCAB-EXACT (VEX) subset of dataset E: rows whose label needs NO alignment / renaming step.

Why: c_score_align shares the aligner (labeller/repair_census.align) with the solver labeller that produced tier-A
labels, so part of its advantage could be shared-instrument circularity. On VEX rows the candidate's symbols are a
subset of the labelling reference's symbols up to a deterministic surface normalisation, so the label is re-derivable
by plain z3 equivalence after an identity rename (no aligner, no panel for tier A).

norm(name)  lowercase, split camelCase / underscores / digits, drop a leading 'is' / 'has' / 'does' token (when more
            tokens remain), WordNet-lemmatise each token (noun, then verb), join with one space.
            'IsTallPerson' -> 'tall person'; 'has_children' -> 'child'.
sig(f)      {('P', norm(pred), arity)} U {('C', norm(const))}.
VEX row     E_POOL, PRIMARY (parseable), in R_AB, auto_label != VOCAB_GRAN, sig(cand) <= sig(ref) and norm is injective
            on both sides (no two raw symbols of one formula share a normal form).
Label re-verification  tier A: rename the candidate's symbols to the reference's raw names by norm identity; plain z3
            equivalence (5 s). EQ must hold iff final == CORRECT, otherwise the row is excluded (counted), TIMEOUT
            excluded. Tier B (COMPOUND, panel-decided, reference-free and alignment-free panel): the panel label is kept.
VEX_STRICT  same with raw-string identity of names instead of norm.
"""
from __future__ import annotations

import re
from functools import lru_cache

_LEM = None


def _lemmatizer():
    global _LEM
    if _LEM is None:
        from nltk.stem import WordNetLemmatizer
        _LEM = WordNetLemmatizer()
    return _LEM


def split_name(name: str) -> list[str]:
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", name)
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", s)
    s = re.sub(r"([A-Za-z])([0-9])", r"\1 \2", s)
    s = s.replace("_", " ").replace("-", " ").replace("'", " ")
    return [t.lower() for t in s.split() if t]


@lru_cache(maxsize=None)
def norm(name: str) -> str:
    toks = split_name(name)
    if len(toks) > 1 and toks[0] in ("is", "has", "does", "have"):
        toks = toks[1:]
    lem = _lemmatizer()
    out = []
    for t in toks:
        n = lem.lemmatize(t, "n")
        if n == t:
            n = lem.lemmatize(t, "v")
        out.append(n)
    return " ".join(out)


def raw_symbols(e):
    """-> ({(pred, arity)}, {const}) of a parsed formula."""
    from .labeller.repair_census import symbols
    P, C = symbols(e)
    return set(P), set(C)


def sig_map(e, strict: bool = False):
    """-> (signature set, {normal form: raw symbol}, injective?)."""
    P, C = raw_symbols(e)
    f = (lambda x: x) if strict else norm
    nf = {}
    ok = True
    for p, a in P:
        k = ("P", f(p), a)
        if k in nf and nf[k] != (p, a):
            ok = False
        nf[k] = (p, a)
    for c in C:
        k = ("C", f(c))
        if k in nf and nf[k] != c:
            ok = False
        nf[k] = c
    return set(nf), nf, ok


def vex_check(cand: str, ref: str, strict: bool = False, ms: int = 5000) -> dict:
    """{'vex': bool, 'why', 'eq': True/False/None (only computed when vex)} for one (candidate, labelling reference)."""
    from .labeller.fol import equivalent, parse
    from .labeller.repair_census import rename
    try:
        ec, er = parse(cand), parse(ref)
    except Exception as e:  # noqa: BLE001
        return {"vex": False, "why": f"parse:{str(e)[:60]}", "eq": None}
    sc, mc, okc = sig_map(ec, strict)
    sr, mr, okr = sig_map(er, strict)
    if not (okc and okr):
        return {"vex": False, "why": "norm_not_injective", "eq": None}
    if not sc <= sr:
        return {"vex": False, "why": "cand_symbol_not_in_ref", "eq": None, "n_extra": len(sc - sr)}
    pmap, cmap = {}, {}
    for k, raw in mc.items():
        tgt = mr[k]
        if k[0] == "P":
            pmap[raw] = tgt[0]
        else:
            cmap[raw] = tgt
    try:
        ren = rename(ec, pmap, cmap)
        eq = equivalent(ren, er, ms)
    except Exception as e:  # noqa: BLE001 - z3 conversion failure (name used as predicate and constant)
        return {"vex": True, "why": f"z3:{str(e)[:60]}", "eq": None}
    return {"vex": True, "why": "ok", "eq": eq, "n_ref_symbols_unused": len(sr - sc)}


def _worker(chunk):
    import sys
    sys.setrecursionlimit(10000)
    out = []
    for key, cand, ref in chunk:
        out.append((key, vex_check(cand, ref, False), vex_check(cand, ref, True)))
    return out


def vex_rows(rows: list[dict], n_jobs: int = 7) -> dict:
    """rows: [{'key', 'candidate_fol', 'labelling_ref', 'label_tier', 'auto_label', 'final_label'}] (R_AB E_POOL
    PRIMARY). -> {key: {'vex', 'vex_strict', 'vex_reason', 'eq', 'eq_strict', 'include', 'include_strict', 'y'}}."""
    import multiprocessing as mp
    todo = [(r["key"], r["candidate_fol"], r["labelling_ref"]) for r in rows
            if r["auto_label"] != "VOCAB_GRAN" and r.get("labelling_ref")]
    chunks = [todo[i:i + 40] for i in range(0, len(todo), 40)]
    res = {}
    with mp.get_context("spawn").Pool(n_jobs) as pool:
        for part in pool.imap_unordered(_worker, chunks):
            for key, a, b in part:
                res[key] = (a, b)
    out = {}
    for r in rows:
        k = r["key"]
        if r["auto_label"] == "VOCAB_GRAN":
            out[k] = {"vex": False, "vex_strict": False, "vex_reason": "VOCAB_GRAN", "include": False, "include_strict": False}
            continue
        if k not in res:
            out[k] = {"vex": False, "vex_strict": False, "vex_reason": "no_labelling_ref", "include": False, "include_strict": False}
            continue
        a, b = res[k]
        rec = {"vex": a["vex"], "vex_strict": b["vex"], "vex_reason": a["why"], "eq": a.get("eq"), "eq_strict": b.get("eq")}
        for nm, chk in (("include", a), ("include_strict", b)):
            if not chk["vex"]:
                rec[nm] = False
                rec[nm + "_why"] = "not_vex"
            elif r["label_tier"] == "A":
                if chk.get("eq") is None:
                    rec[nm], rec[nm + "_why"] = False, "timeout_or_z3"
                elif bool(chk["eq"]) == (r["final_label"] == "CORRECT"):
                    rec[nm], rec[nm + "_why"] = True, "tierA_reverified"
                else:
                    rec[nm], rec[nm + "_why"] = False, "tierA_label_mismatch"
            else:  # tier B COMPOUND: the panel decided without the aligner
                rec[nm], rec[nm + "_why"] = True, "tierB_panel_kept"
        out[k] = rec
    return out
