"""PEER+TEXT: gold-free faithfulness scoring of an NL->FOL candidate from (text, fol, peer formalisations).

PEER side (text-free, name-free, graded cross-family consensus):
  parse_fol(s)                      dataset-E parser (vendor_e/fol.py) -> AST or None (coverage failure, counted).
  claim_units(ast)                  the formula as a list of independent closed claims (conjunction of units == formula).
  symbol_signature(ast)             per predicate/constant a NAME-FREE structural signature (arity, polarity profile,
                                    quantifier force / block of its argument variables, 1-WL neighbourhood hash).
  name_free_align(cand, peer, ...)  k-best predicate/constant bijections peer->candidate from signatures only (NF-pure)
                                    or signatures + text anchors (NF-anchored), verified by unit entailment.
  entails(premise, unit)            finite-model refuter (64 random interpretations, domains 1..3) then z3.
  graded_consensus(...)             support (share of candidate claims the peers entail), coverage (share of the peers'
                                    majority claims the candidate entails), g_score = 1 - F1(support, coverage),
                                    c_score_nf = 1 - share of peers z3-equivalent under the accepted mapping,
                                    unit_codes: NEG / QUANT / SWAP / ADD for unsupported claims, DROP for uncovered ones.
TEXT side (vendored unchanged from iteration-1 exp A, fol_triage.py):
  l2_bow(text, fol)                 content accounting: #unanchored predicates + share of uncarried content words.
  l3_z3(q, fol)                     role questionnaire of the TEXT (small LLM, never sees the formula) vs the formula's
                                    exact z3 role profile; sum of the 5 gated field mismatches.
FUSION:
  peer_text_score(text, fol, peers, frozen)  frozen logistic over [g_score, c_score_nf, l2_bow, l3_z3].

What PEER is blind to (stated, measured): errors every peer shares (peer-endorsed errors), meaning-level renames that
keep structure (MEANING_RENAME: a wrong predicate in the right place), and for NF-pure errors that are automorphisms of the
formula structure (e.g. ∀x(B→A) vs ∀x(A→B) with A, B structurally symmetric: the ROLE_PERMUTE probe).
What TEXT is blind to: structure the text words do not reveal (scope, binding), and anything the small LLM misreads.
"""
from __future__ import annotations

import hashlib
import itertools
import math
import os
import re
import sys
import time
from functools import lru_cache
from pathlib import Path

import numpy as np
import z3
from scipy.optimize import linear_sum_assignment

sys.setrecursionlimit(20000)
SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
os.environ.setdefault("NLTK_DATA", str(ROOT / "data" / "nltk_data"))
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
import vendor_e.fol as EFOL  # noqa: E402  (the parser that produced dataset E's UNPARSEABLE labels)

# every vendored module does `from fol import ...`: bind that name to the dataset-E parser (fixed <-> / ⊕ precedence)
sys.modules["fol"] = EFOL
for _p in (SRC / "vendor_c", SRC / "vendor_a"):
    if str(_p) not in sys.path:
        sys.path.insert(1, str(_p))

BINSYM = {"iff": "↔", "xor": "⊕", "imp": "→", "or": "∨", "and": "∧"}
BIN = ("and", "or", "imp", "iff", "xor")
UNIT_CAP = 16


# =================================================================================================== parse & print
def parse_fol(s: str | None):
    """Dataset-E parser. Returns the AST or None (unparseable = coverage failure, never silently dropped)."""
    if s is None or not str(s).strip():
        return None
    try:
        return EFOL.parse(str(s))
    except (ValueError, IndexError, RecursionError, TypeError):
        return None


def to_str(e) -> str:
    """Fully parenthesised Unicode rendering; parse_fol(to_str(e)) == e."""
    k = e[0]
    if k == "atom":
        return f"{e[1]}({', '.join(e[2])})" if e[2] else e[1]
    if k in ("all", "ex"):
        return f"{'∀' if k == 'all' else '∃'}{e[1]} ({to_str(e[2])})"
    if k == "not":
        return f"¬({to_str(e[1])})" if e[1][0] not in ("atom", "not") else f"¬{to_str(e[1])}"
    return f"({to_str(e[1])} {BINSYM[k]} {to_str(e[2])})"


def free_vars(e, bound=frozenset()) -> set:
    k = e[0]
    if k == "atom":
        return set()  # arguments not bound are constants in this grammar
    if k in ("all", "ex"):
        return free_vars(e[2], bound | {e[1]})
    if k == "not":
        return free_vars(e[1], bound)
    return free_vars(e[1], bound) | free_vars(e[2], bound)


def mentions(e, v: str) -> bool:
    k = e[0]
    if k == "atom":
        return v in e[2]
    if k in ("all", "ex"):
        return False if e[1] == v else mentions(e[2], v)
    if k == "not":
        return mentions(e[1], v)
    return mentions(e[1], v) or mentions(e[2], v)


def alpha(e, env=None, ctr=None):
    """Alpha-normalise bound variables to v0, v1, ... in order of their binders (canonical strings; unique binders)."""
    env = {} if env is None else env
    ctr = [0] if ctr is None else ctr
    k = e[0]
    if k == "atom":
        return ("atom", e[1], tuple(env.get(a, a) for a in e[2]))
    if k in ("all", "ex"):
        nv = f"v{ctr[0]}"
        ctr[0] += 1
        return (k, nv, alpha(e[2], {**env, e[1]: nv}, ctr))
    if k == "not":
        return ("not", alpha(e[1], env, ctr))
    return (k, alpha(e[1], env, ctr), alpha(e[2], env, ctr))


def canon(e) -> str:
    return to_str(alpha(e))


def pred_keys(e, acc=None) -> dict:
    """{(name, arity): True} in order of first occurrence."""
    acc = {} if acc is None else acc
    k = e[0]
    if k == "atom":
        acc.setdefault((e[1], len(e[2])), True)
    elif k in ("all", "ex"):
        pred_keys(e[2], acc)
    elif k == "not":
        pred_keys(e[1], acc)
    else:
        pred_keys(e[1], acc)
        pred_keys(e[2], acc)
    return acc


def constants(e, bound=frozenset(), acc=None) -> dict:
    acc = {} if acc is None else acc
    k = e[0]
    if k == "atom":
        for a in e[2]:
            if a not in bound:
                acc.setdefault(a, True)
    elif k in ("all", "ex"):
        constants(e[2], bound | {e[1]}, acc)
    elif k == "not":
        constants(e[1], bound, acc)
    else:
        constants(e[1], bound, acc)
        constants(e[2], bound, acc)
    return acc


def rename(e, pmap: dict, cmap: dict, bound=frozenset()):
    """pmap: {(name, arity): new_name}; cmap: {const: new_const}. Bound variables untouched."""
    k = e[0]
    if k == "atom":
        return ("atom", pmap.get((e[1], len(e[2])), e[1]), tuple(a if a in bound else cmap.get(a, a) for a in e[2]))
    if k in ("all", "ex"):
        return (k, e[1], rename(e[2], pmap, cmap, bound | {e[1]}))
    if k == "not":
        return ("not", rename(e[1], pmap, cmap, bound))
    return (k, rename(e[1], pmap, cmap, bound), rename(e[2], pmap, cmap, bound))


# =================================================================================================== claim units
def _conseq_pieces(c) -> list:
    """C == AND(pieces). Splits ∧, curried →, ∀ over ∧, ¬∨ (De Morgan)."""
    k = c[0]
    if k == "and":
        return _conseq_pieces(c[1]) + _conseq_pieces(c[2])
    if k == "imp":
        return [("imp", c[1], p) for p in _conseq_pieces(c[2])]
    if k == "all":
        return [("all", c[1], p) if mentions(p, c[1]) else p for p in _conseq_pieces(c[2])]
    if k == "not" and c[1][0] == "or":
        return _conseq_pieces(("not", c[1][1])) + _conseq_pieces(("not", c[1][2]))
    if k == "not" and c[1][0] == "not":
        return _conseq_pieces(c[1][1])
    return [c]


def claim_units(e, cap: int = UNIT_CAP) -> tuple[list, list, bool]:
    """-> (units, locations, truncated). The formula is logically equivalent to the conjunction of its units
    (before truncation): top-level ∧ split; ∀ distributed over ∧; for a universal rule ∀x̄(R → C1 ∧ .. ∧ Cm) one unit
    ∀x̄(R → Cj) per consequent conjunct; ¬¬, ¬(A∨B), ¬(A→B), ¬∃ normalised so that they split; ∃-claims kept whole;
    ground literals are units. Units keep the index path of their origin (for DROP/ADD location reports).
    Vacuous quantifiers are removed from units. Cap: first `cap` units in textual order (truncated=True if cut)."""
    out, locs = [], []

    def emit(prefix, x, loc):
        for v in reversed(prefix):
            if mentions(x, v):
                x = ("all", v, x)
        out.append(x)
        locs.append(loc)

    def split(x, prefix, loc):
        k = x[0]
        if k == "and":
            split(x[1], prefix, loc + (1,))
            split(x[2], prefix, loc + (2,))
            return
        if k == "all":
            split(x[2], prefix + [x[1]], loc + (2,))
            return
        if k == "not":
            y = x[1]
            if y[0] == "not":
                return split(y[1], prefix, loc + (1,))
            if y[0] == "or":
                return split(("and", ("not", y[1]), ("not", y[2])), prefix, loc)
            if y[0] == "imp":
                return split(("and", y[1], ("not", y[2])), prefix, loc)
            if y[0] == "ex":
                return split(("all", y[1], ("not", y[2])), prefix, loc)
        if k == "imp":
            ps = _conseq_pieces(x[2])
            for i, c in enumerate(ps):
                emit(prefix, ("imp", x[1], c), loc + (2, i) if len(ps) > 1 else loc)
            return
        emit(prefix, x, loc)

    split(e, [], ())
    trunc = len(out) > cap
    return out[:cap], locs[:cap], trunc


@lru_cache(maxsize=200000)
def units_of(s: str):
    """Cached claim units of a canonical formula string -> (tuple(unit canon strings), tuple(unit ASTs), truncated)."""
    e = parse_fol(s)
    us, _, tr = claim_units(e)
    us = [alpha(u) for u in us]
    return tuple(to_str(u) for u in us), tuple(us), tr


# =================================================================================================== signatures
def _occurrences(e):
    """Atom occurrences with syntactic polarity (+1 up, -1 down, 0 mixed under ↔/⊕) and argument binders."""
    occ = []

    def go(x, pol, binders, depth):
        k = x[0]
        if k == "atom":
            occ.append((x[1], len(x[2]), x[2], pol, dict(binders)))
        elif k in ("all", "ex"):
            go(x[2], pol, {**binders, x[1]: (k, depth)}, depth + 1)
        elif k == "not":
            go(x[1], -pol, binders, depth)
        elif k == "imp":
            go(x[1], -pol, binders, depth)
            go(x[2], pol, binders, depth)
        elif k in ("iff", "xor"):
            go(x[1], 0, binders, depth)
            go(x[2], 0, binders, depth)
        else:
            go(x[1], pol, binders, depth)
            go(x[2], pol, binders, depth)
    go(alpha(e), 1, {}, 0)
    return occ


def _qdepth(e) -> int:
    k = e[0]
    if k == "atom":
        return 0
    if k in ("all", "ex"):
        return 1 + _qdepth(e[2])
    if k == "not":
        return _qdepth(e[1])
    return max(_qdepth(e[1]), _qdepth(e[2]))


CLAMP_DOMAINS = ((1, 64), (2, 64))


def clamp_profile(e) -> dict:
    """Rewrite-invariant SEMANTIC signature: for every predicate P, the truth rate of the formula over 128 random finite
    interpretations (domains 1 and 2) with P clamped to all-true and to all-false. Logically equivalent formulas
    (contrapositive, De Morgan, prenex, reordering) get identical profiles up to sampling of the other predicates."""
    ea = alpha(e)
    out = {}
    for key in pred_keys(ea):
        vals = []
        for val in (True, False):
            tot = n = 0
            for d, m in CLAMP_DOMAINS:
                v = _fm_eval(ea, d, m, clamp=(key[0], key[1], val))
                if v is not None:
                    tot += int(v.sum())
                    n += len(v)
            vals.append(tot / n if n else 0.5)
        out[key] = tuple(vals)
    return out


def symbol_signature(e) -> dict:
    """NAME-FREE signature of every predicate and constant of formula e.
    pred (name, arity) -> {'arity', 'pol': (up, down, mixed) shares over occurrences (syntactic polarity; ↔/⊕ operands
    are MIXED; syntactic monotonicity is sound for semantic monotonicity), 'qforce': mean over argument slots of 1 (∀) /
    0 (∃) / 0.5 (constant), 'qblock': mean binder depth / max quantifier depth, 'nbr': set of (arity, polarity, own slot,
    other slot) of atoms sharing a bound variable with it (1-WL neighbourhood)}.
    const -> {'fill': set of (arity, slot, polarity) it fills}."""
    occ = _occurrences(e)
    md = max(1, _qdepth(e))
    P, C = {}, {}
    for i, (name, ar, args, pol, b) in enumerate(occ):
        d = P.setdefault((name, ar), {"arity": ar, "pc": [0, 0, 0], "qf": [], "qb": [], "nbr": set()})
        d["pc"][0 if pol > 0 else (1 if pol < 0 else 2)] += 1
        for s, a in enumerate(args):
            if a in b:
                d["qf"].append(1.0 if b[a][0] == "all" else 0.0)
                d["qb"].append(b[a][1] / md)
            else:
                d["qf"].append(0.5)
                d["qb"].append(0.0)
                C.setdefault(a, set()).add((ar, s, pol))
        for j, (n2, ar2, args2, pol2, b2) in enumerate(occ):
            if j == i:
                continue
            for s, a in enumerate(args):
                if a in b:
                    for s2, a2 in enumerate(args2):
                        if a2 == a and b2.get(a2) == b[a]:
                            d["nbr"].add((ar2, pol2, s, s2))
    out = {}
    cp = clamp_profile(e)
    for k, d in P.items():
        n = sum(d["pc"])
        out[k] = {"arity": d["arity"], "pol": tuple(x / n for x in d["pc"]), "clamp": cp.get(k, (0.5, 0.5)),
                  "qforce": float(np.mean(d["qf"])) if d["qf"] else 0.5,
                  "qblock": float(np.mean(d["qb"])) if d["qb"] else 0.0, "nbr": frozenset(d["nbr"])}
    return {"preds": out, "consts": {c: {"fill": frozenset(v)} for c, v in C.items()}}


def _jac(a, b) -> float:
    if not a and not b:
        return 1.0
    return len(a & b) / len(a | b)


def pred_cost(a: dict, b: dict) -> float:
    """Structural cost in [0,1]; five components weighted 0.2 each, fixed a priori (not tuned): polarity profile L1/2,
    quantifier force, quantifier block, 1 - Jaccard(neighbourhood), semantic clamp profile mean |difference|."""
    l1 = sum(abs(x - y) for x, y in zip(a["pol"], b["pol"])) / 2
    cl = (abs(a["clamp"][0] - b["clamp"][0]) + abs(a["clamp"][1] - b["clamp"][1])) / 2
    return 0.2 * l1 + 0.2 * abs(a["qforce"] - b["qforce"]) + 0.2 * abs(a["qblock"] - b["qblock"]) + \
        0.2 * (1 - _jac(a["nbr"], b["nbr"])) + 0.2 * cl


# ------------------------------------------------------------------------------------------- text anchors
_TEXT_TOK = re.compile(r"[A-Za-z]+|\d+")


@lru_cache(maxsize=100000)
def _text_tokens(text: str) -> tuple:
    import content_accounting as ca  # vendor_a
    return tuple((i, w.lower()) for i, w in enumerate(_TEXT_TOK.findall(text))
                 if w.lower() not in ca.FUNC and len(w) > 1)


@lru_cache(maxsize=200000)
def text_anchor(symbol: str, text: str) -> frozenset:
    """Sentence token indices matched by the words of a predicate/constant name (exp A word_match: Porter stem or
    WordNet lemma / synonym / derivation). Used ONLY by NF-anchored."""
    import fol_triage as FT  # vendor_a
    nw = FT.name_words(symbol)
    toks = _text_tokens(text)
    return frozenset(i for i, w in toks for x in nw if FT.word_match(w, x))


def anchor_cost(a: frozenset, b: frozenset) -> float:
    if not a or not b:
        return 0.5
    return 1 - len(a & b) / len(a | b)


# =================================================================================================== alignment
BIG = 1e6
DUMMY = 0.6


def _solve(M: np.ndarray):
    r, c = linear_sum_assignment(M)
    return r, c, float(M[r, c].sum())


def name_free_align(cand, peer, text: str | None = None, variant: str = "NF-pure", k: int = 5,
                    sig_c: dict | None = None, sig_p: dict | None = None) -> list[dict]:
    """k cheapest peer->candidate symbol bijections (predicates within equal arity; constants separately; arity mismatch =
    +inf; unmatched symbols pay DUMMY=0.6 and stay fresh 'pp_' symbols). k-best by Murty's algorithm. NF-anchored adds 1.0 x anchor cost (1 - Jaccard of text anchors, 0.5 if either side is
    unanchored). Returns [{'pmap', 'cmap', 'cost'}] sorted by cost (total over symbols)."""
    sig_c = sig_c or symbol_signature(cand)
    sig_p = sig_p or symbol_signature(peer)
    Pp, Pc = list(sig_p["preds"]), list(sig_c["preds"])
    Kp, Kc = list(sig_p["consts"]), list(sig_c["consts"])
    rows = [("p", x) for x in Pp] + [("c", x) for x in Kp]
    cols = [("p", x) for x in Pc] + [("c", x) for x in Kc]
    nr, nc = len(rows), len(cols)
    n = nr + nc
    M = np.full((n, n), BIG)
    M[nr:, nc:] = 0.0
    anch = variant == "NF-anchored" and text
    for i, (si, x) in enumerate(rows):
        M[i, nc + i] = DUMMY
        for j, (sj, y) in enumerate(cols):
            if si != sj:
                continue
            if si == "p":
                if x[1] != y[1]:
                    continue
                cst = pred_cost(sig_p["preds"][x], sig_c["preds"][y])
            else:
                cst = 1 - _jac(sig_p["consts"][x]["fill"], sig_c["consts"][y]["fill"])
            if anch:  # both anchored: the text decides, structure breaks ties; else structure + 0.5 (pre-registered)
                ax_, ay_ = text_anchor(x[0] if si == "p" else x, text), text_anchor(y[0] if sj == "p" else y, text)
                cst = (anchor_cost(ax_, ay_) + 0.25 * cst) if (ax_ and ay_) else (cst + 0.5)
            M[i, j] = cst
    for j in range(nc):
        M[nr + j, j] = DUMMY

    def to_map(r, c):
        pmap, cmap = {}, {}
        for i, j in zip(r, c):
            if i >= nr:
                continue
            si, x = rows[i]
            if j < nc:
                y = cols[j][1]
                if si == "p":
                    pmap[x] = y[0]
                else:
                    cmap[x] = y
            else:
                if si == "p":
                    pmap[x] = "pp_" + x[0]
                else:
                    cmap[x] = "pp_" + x
        return pmap, cmap

    if n == 0:
        return [{"pmap": {}, "cmap": {}, "cost": 0.0}]
    return [{"pmap": pm, "cmap": cm, "cost": t} for (pm, cm), t in _murty(M, nr, k, to_map)]


def _murty(M: np.ndarray, nr: int, k: int, to_map) -> list:
    """Murty's k-best assignment, partitioning on the peer-row edges (they determine the mapping)."""
    import heapq

    def solve(forced, forbidden):
        M2 = M.copy()
        for (i, j) in forbidden:
            M2[i, j] = BIG
        for (i, j) in forced:
            keep = M2[i, j]
            M2[i, :] = BIG
            M2[:, j] = BIG
            M2[i, j] = keep
        r, c, t = _solve(M2)
        if t >= BIG / 2:
            return None
        return r, c, t
    first = solve((), ())
    if first is None:
        return []
    heap = [(first[2], 0, first, (), ())]
    ctr, out, seen = 1, [], set()
    while heap and len(out) < k:
        t, _, (r, c, _t), forced, forbidden = heapq.heappop(heap)
        mp = to_map(r, c)
        key = repr(sorted(mp[0].items()) + sorted(mp[1].items()))
        if key not in seen:
            seen.add(key)
            out.append((mp, t))
        edges = [(i, j) for i, j in zip(r, c) if i < nr and (i, j) not in forced]
        f = list(forced)
        for e in edges:
            sol = solve(tuple(f), forbidden + (e,))
            if sol is not None:
                heapq.heappush(heap, (sol[2], ctr, sol, tuple(f), forbidden + (e,)))
                ctr += 1
            f.append(e)
        if len(heap) > 50 * k:
            heap = heapq.nsmallest(10 * k, heap)
            heapq.heapify(heap)
    return out


# =================================================================================================== entailment
FM_DOMAINS = ((1, 16), (2, 24), (3, 24))          # (domain size, #random interpretations) -> 64 models
FM_P = np.array([0.15, 0.5, 0.85])


def _seed(*parts) -> int:
    return int(hashlib.sha1("|".join(map(str, parts)).encode()).hexdigest()[:12], 16)


@lru_cache(maxsize=100000)
def _table(name: str, arity: int, d: int, m: int) -> np.ndarray:
    rng = np.random.default_rng(_seed("P", name, arity, d, m))
    p = FM_P[np.arange(m) % 3].reshape((m,) + (1,) * arity)
    return rng.random((m,) + (d,) * arity) < p


@lru_cache(maxsize=100000)
def _const(name: str, d: int, m: int) -> np.ndarray:
    rng = np.random.default_rng(_seed("C", name, d, m))
    return rng.integers(0, d, size=m)


def _fm_eval(e, d: int, m: int, clamp: tuple | None = None) -> np.ndarray | None:
    """Truth value of closed formula e in m random interpretations over a domain of size d -> bool array (m,).
    Variables are array axes; quantifiers reduce over their axis. None if too many variables for this domain."""
    ea = alpha(e)
    nv = sum(1 for _ in _binders(ea))
    if d ** nv * m > 2_000_000:
        return None
    nd = 1 + nv
    ax = {}

    def shape_at(i):
        s = [1] * nd
        s[i] = -1
        return s
    mid = np.arange(m).reshape(shape_at(0))

    def ev(x):
        k = x[0]
        if k == "atom":
            if clamp is not None and clamp[0] == x[1] and clamp[1] == len(x[2]):
                return np.full((m,) + (1,) * nv, clamp[2])
            T = _table(x[1], len(x[2]), d, m)
            if not x[2]:
                return T.reshape(shape_at(0))
            idx = [mid]
            for a in x[2]:
                if a in ax:
                    idx.append(np.arange(d).reshape(shape_at(ax[a])))
                else:
                    idx.append(_const(a, d, m).reshape(shape_at(0)))
            return T[tuple(idx)]
        if k in ("all", "ex"):
            ax[x[1]] = 1 + int(x[1][1:])
            b = ev(x[2])
            if b.ndim < nd:
                b = b.reshape(b.shape + (1,) * (nd - b.ndim))
            return b.all(axis=ax[x[1]], keepdims=True) if k == "all" else b.any(axis=ax[x[1]], keepdims=True)
        if k == "not":
            return ~ev(x[1])
        a, b = ev(x[1]), ev(x[2])
        if k == "and":
            return a & b
        if k == "or":
            return a | b
        if k == "imp":
            return ~a | b
        if k == "iff":
            return a == b
        return a ^ b
    r = ev(ea)
    return np.broadcast_to(r, (m,) + (1,) * (r.ndim - 1)).reshape(m)


def _binders(e):
    k = e[0]
    if k in ("all", "ex"):
        yield e[1]
        yield from _binders(e[2])
    elif k == "not":
        yield from _binders(e[1])
    elif k != "atom":
        yield from _binders(e[1])
        yield from _binders(e[2])


_FM_CACHE: dict = {}


def fm_vector(s: str, e=None) -> list:
    """Cached truth vectors of formula string s over the fixed random interpretations (one array per domain)."""
    r = _FM_CACHE.get(s)
    if r is None:
        e = e if e is not None else parse_fol(s)
        r = [_fm_eval(e, d, m) for d, m in FM_DOMAINS]
        if len(_FM_CACHE) > 300000:
            _FM_CACHE.clear()
        _FM_CACHE[s] = r
    return r


def fm_refutes(prem_s: str, unit_s: str, prem=None, unit=None) -> bool:
    """True iff some random finite interpretation makes the premise true and the unit false (a genuine countermodel,
    so prem ⊭ unit). Sound: never True when prem ⊨ unit."""
    vp, vu = fm_vector(prem_s, prem), fm_vector(unit_s, unit)
    for a, b in zip(vp, vu):
        if a is not None and b is not None and bool(np.any(a & ~b)):
            return True
    return False


def z3_entails(prem, unit, ms: int = 2000):
    """z3: prem ∧ ¬unit unsat -> True; sat -> False; unknown/timeout -> None."""
    P = {}
    for key in list(pred_keys(prem)) + list(pred_keys(unit)):
        q = f"{key[0]}/{key[1]}"
        if q not in P:
            P[q] = EFOL.mkpred(q, key[1])
    s = z3.Solver()
    s.set("timeout", ms)
    s.add(EFOL.to_z3(prem, {}, P))
    s.add(z3.Not(EFOL.to_z3(unit, {}, P)))
    r = s.check()
    return True if r == z3.unsat else (False if r == z3.sat else None)


class Entailer:
    """entails(premise, unit) with a per-process cache keyed by canonical strings.
    Order: identical -> True; unit is literally one of the premise's claim units -> True; finite-model countermodel ->
    False; z3 (timeout_ms) -> True / False / None (UNKNOWN, never counted as False)."""

    def __init__(self, timeout_ms: int = 2000, use_fm: bool = True):
        self.ms = timeout_ms
        self.use_fm = use_fm
        self.cache: dict = {}
        self.stats = {"identical": 0, "unit": 0, "fm": 0, "z3_true": 0, "z3_false": 0, "z3_unknown": 0, "cached": 0}

    def __call__(self, prem_s: str, unit_s: str, prem=None, unit=None):
        key = (prem_s, unit_s)
        if key in self.cache:
            self.stats["cached"] += 1
            return self.cache[key]
        if prem_s == unit_s:
            r = True
            self.stats["identical"] += 1
        elif unit_s in units_of(prem_s)[0]:
            r = True
            self.stats["unit"] += 1
        elif self.use_fm and fm_refutes(prem_s, unit_s, prem, unit):
            r = False
            self.stats["fm"] += 1
        else:
            prem = prem if prem is not None else parse_fol(prem_s)
            unit = unit if unit is not None else parse_fol(unit_s)
            try:
                r = z3_entails(prem, unit, self.ms)
            except (z3.Z3Exception, RecursionError, KeyError) as ex:  # noqa: F841
                r = None
            self.stats["z3_true" if r is True else ("z3_false" if r is False else "z3_unknown")] += 1
        if len(self.cache) > 500000:
            self.cache.clear()
        self.cache[key] = r
        return r


# =================================================================================================== pair results
def pair_result(cand_s: str, peer_s: str, ent: Entailer, text: str | None = None, variant: str = "NF-pure",
                k: int = 5, tau: float | None = None, select_by: str = "fm") -> dict:
    """Align peer into the candidate's vocabulary and verify unit entailments in both directions.
    cand_s/peer_s are canonical strings. Mapping acceptance: among the k-best mappings with cost <= min_cost + tau
    (tau = inf for NF-pure), take the one with the most unit entailments not refuted by the finite-model refuter
    (select_by='fm', a sound upper bound on the z3-verified count; 'z3' uses full entailment), ties -> lower cost.
    Returns {'fwd': [peer ⊨ cand-unit], 'bwd': [cand ⊨ peer-unit], 'peer_r': renamed peer string,
             'peer_units_r': renamed peer unit strings, 'equiv', 'cost', 'n_maps', 'rank'}."""
    cu_s, cu, ctr = units_of(cand_s)
    pu_s, pu, ptr = units_of(peer_s)
    if cand_s == peer_s:
        return {"fwd": [True] * len(cu_s), "bwd": [True] * len(pu_s), "peer_r": cand_s, "peer_units_r": list(pu_s),
                "equiv": True, "cost": 0.0, "n_maps": 0, "rank": 0}
    ce, pe = parse_fol(cand_s), parse_fol(peer_s)
    if variant == "ALIGN":  # iteration-1 aligner (name similarity, repair_census.align): one mapping peer -> candidate
        from repair_census import align as _rc_align
        _, pmap, cmap = _rc_align(pe, ce)
        maps = [{"pmap": dict(pmap), "cmap": dict(cmap), "cost": 0.0}]
    else:
        maps = name_free_align(ce, pe, text=text, variant=variant, k=k)
    tau = math.inf if tau is None else tau
    lo = maps[0]["cost"]
    window = [m for m in maps if m["cost"] <= lo + tau + 1e-9]
    best, best_key, best_rank = None, None, 0
    for rank, m in enumerate(window):
        pr = rename(pe, m["pmap"], m["cmap"])
        pr_s = canon(pr)
        pur = [canon(rename(u, m["pmap"], m["cmap"])) for u in pu]
        if select_by == "fm":
            n_ok = sum(not fm_refutes(pr_s, u) for u in cu_s) + sum(not fm_refutes(cand_s, v) for v in pur)
        else:
            n_ok = sum(ent(pr_s, u) is True for u in cu_s) + sum(ent(cand_s, v) is True for v in pur)
        key = (n_ok, -m["cost"])
        if best_key is None or key > best_key:
            best, best_key, best_rank = (m, pr_s, pur), key, rank
    m, pr_s, pur = best
    fwd = [ent(pr_s, u) for u in cu_s]
    bwd = [ent(cand_s, v) for v in pur]
    if not ctr and not ptr:
        equiv = True if (all(x is True for x in fwd) and all(x is True for x in bwd)) else \
            (None if any(x is None for x in fwd + bwd) and not any(x is False for x in fwd + bwd) else False)
    else:
        a, b = ent(pr_s, cand_s), ent(cand_s, pr_s)
        equiv = True if (a is True and b is True) else (False if (a is False or b is False) else None)
    return {"fwd": fwd, "bwd": bwd, "peer_r": pr_s, "peer_units_r": pur, "equiv": equiv, "cost": m["cost"],
            "n_maps": len(maps), "rank": best_rank}


# =================================================================================================== graded consensus
def _variants_quant(u):
    """one ∀<->∃ flip of u (each quantifier node, max 4)."""
    out = []

    def go(x, path):
        k = x[0]
        if k in ("all", "ex"):
            out.append(path)
            go(x[2], path + (2,))
        elif k == "not":
            go(x[1], path + (1,))
        elif k != "atom":
            go(x[1], path + (1,))
            go(x[2], path + (2,))
    go(u, ())
    res = []
    for p in out[:4]:
        res.append(_replace(u, p, lambda n: ("ex" if n[0] == "all" else "all", n[1], n[2])))
    return res


def _variants_swap(u):
    out = []

    def go(x, path):
        k = x[0]
        if k == "atom":
            if len(x[2]) == 2 and x[2][0] != x[2][1]:
                out.append(path)
        elif k in ("all", "ex"):
            go(x[2], path + (2,))
        elif k == "not":
            go(x[1], path + (1,))
        else:
            go(x[1], path + (1,))
            go(x[2], path + (2,))
    go(u, ())
    return [_replace(u, p, lambda n: ("atom", n[1], (n[2][1], n[2][0]))) for p in out[:4]]


def _variants_neg(u):
    """one literal polarity toggle of u (¬ added to / removed from one atom occurrence, max 6)."""
    out = []

    def go(x, path):
        k = x[0]
        if k == "atom":
            out.append((path, "add"))
        elif k == "not" and x[1][0] == "atom":
            out.append((path, "del"))
        elif k in ("all", "ex"):
            go(x[2], path + (2,))
        elif k == "not":
            go(x[1], path + (1,))
        else:
            go(x[1], path + (1,))
            go(x[2], path + (2,))
    go(u, ())
    return [_replace(u, p, (lambda n: ("not", n)) if how == "add" else (lambda n: n[1])) for p, how in out[:6]]


def _replace(e, path, fn):
    if not path:
        return fn(e)
    lst = list(e)
    lst[path[0]] = _replace(e[path[0]], path[1:], fn)
    return tuple(lst)


CODE_PRIORITY = ["NEG", "QUANT", "SWAP", "DROP", "ADD"]


def _majority_support(ent: Entailer, peers_r: list[str], u_s: str) -> bool:
    """True iff >= 50% of the (renamed) peers entail u (UNKNOWN pairs excluded); early exit."""
    yes = no = 0
    n = len(peers_r)
    for i, p in enumerate(peers_r):
        r = ent(p, u_s)
        if r is True:
            yes += 1
        elif r is False:
            no += 1
        if no > n / 2:
            return False
        if yes >= n / 2 and yes > 0:
            return True
    tot = yes + no
    return tot > 0 and yes / tot >= 0.5


def graded_consensus(cand_s: str, pool: list[str], pairs: dict, ent: Entailer, return_codes: bool = True,
                     unit_locs: bool = True) -> dict:
    """Graded, name-free consensus of candidate formula cand_s (canonical string) against its peer pool.

    pool   : canonical strings of the peers (already leave-one-family-out filtered; duplicates allowed = one vote each).
    pairs  : {(a, b): pair_result(a, b)} for a in {cand} ∪ pool, b in pool, a != b (b aligned INTO a's vocabulary).
    support  = mean over candidate units u (units UNKNOWN for all peers excluded) of the share of peers p with σ_p(p) ⊨ u.
    coverage = mean over peers p of the share of p's MAJORITY units (entailed by >= 50% of the other pool peers) that
               the candidate entails (σ_p applied). A peer without majority units is skipped; no majority units at all
               -> coverage = 1 (nothing agreed to cover).
    g_score  = 1 - 2·support·coverage / (support + coverage)  (1 if both 0); higher = more likely an error.
    c_score_nf = 1 - share of peers z3-equivalent to the candidate under the accepted mapping.
    unit_codes: unsupported unit (support < 0.5) -> NEG if one literal-polarity toggle of u has majority support, else QUANT if one ∀/∃ flip of u
                has it, else SWAP if one binary-argument swap of u has it, else ADD; an uncovered majority unit -> DROP.
    Blind to: errors shared by the majority of peers; meaning renames with unchanged structure."""
    cu_s, cu, ctr = units_of(cand_s)
    n_peers = len(pool)
    out = {"n_units": len(cu_s), "units_truncated": ctr, "n_peers_used": n_peers}
    if n_peers < 2:
        out.update(g_score=None, support=None, coverage=None, c_score_nf=None, peer_unavailable=True, unit_codes=[],
                   n_unknown=0)
        return out
    res = [pairs[(cand_s, p)] if p != cand_s else None for p in pool]

    def fwd_of(i, r):
        return True if r is None else r["fwd"][i]
    fracs, n_unknown, unit_support = [], 0, []
    for i in range(len(cu_s)):
        vals = [fwd_of(i, r) for r in res]
        n_unknown += sum(v is None for v in vals)
        vv = [v for v in vals if v is not None]
        if vv:
            f = sum(vv) / len(vv)
            fracs.append(f)
            unit_support.append(f)
        else:
            unit_support.append(None)
    support = float(np.mean(fracs)) if fracs else None
    covs, drops = [], []
    for pi, p in enumerate(pool):
        pu_s = units_of(p)[0]
        others = [q for qi, q in enumerate(pool) if qi != pi]
        maj = []
        for j in range(len(pu_s)):
            vals = []
            for q in others:
                if q == p:
                    vals.append(True)
                else:
                    r = pairs.get((p, q))
                    if r is not None:
                        vals.append(r["fwd"][j])
            vv = [v for v in vals if v is not None]
            if vv and sum(vv) / len(vv) >= 0.5:
                maj.append(j)
        if not maj:
            continue
        r = res[pi]
        cov_j = [(True if r is None else r["bwd"][j]) for j in maj]
        known = [v for v in cov_j if v is not None]
        n_unknown += len(cov_j) - len(known)
        if known:
            covs.append(sum(known) / len(known))
        for j, v in zip(maj, cov_j):
            if v is False:
                drops.append((pi, j, r["peer_units_r"][j]))
    coverage = float(np.mean(covs)) if covs else 1.0
    if support is None:
        g = None
    else:
        g = 1.0 if (support + coverage) == 0 else 1 - 2 * support * coverage / (support + coverage)
    eqs = [True if r is None else r["equiv"] for r in res]
    known_eq = [e for e in eqs if e is not None]
    c_nf = 1 - (sum(e is True for e in eqs) / n_peers)
    out.update(g_score=g, support=support, coverage=coverage, c_score_nf=c_nf, peer_unavailable=False,
               n_unknown=n_unknown, n_equiv_known=len(known_eq), unit_support=unit_support)
    codes = []
    if return_codes:
        peers_r = [cand_s if r is None else r["peer_r"] for r in res]
        for i, f in enumerate(unit_support):
            if f is None or f >= 0.5:
                continue
            u = cu[i]
            code = "ADD"
            if any(_majority_support(ent, peers_r, canon(v)) for v in _variants_neg(u)):
                code = "NEG"
            elif any(_majority_support(ent, peers_r, canon(v)) for v in _variants_quant(u)):
                code = "QUANT"
            elif any(_majority_support(ent, peers_r, canon(v)) for v in _variants_swap(u)):
                code = "SWAP"
            codes.append({"code": code, "unit": cu_s[i], "unit_index": i, "support": round(f, 3)})
        seen = set()
        for pi, j, us in drops:
            if us in seen:
                continue
            seen.add(us)
            codes.append({"code": "DROP", "unit": us, "peer_index": pi})
    out["unit_codes"] = codes
    out["top_code"] = next((c for c in CODE_PRIORITY if any(x["code"] == c for x in codes)), "NONE")
    return out


def g_from_subset(cand_s: str, pool: list[str], pairs: dict, ent: Entailer) -> float | None:
    """g_score with a restricted pool (used for the k=6 subsample check); no unit codes."""
    return graded_consensus(cand_s, pool, pairs, ent, return_codes=False)["g_score"]


def nf_medoid(pool: list[str], pairs: dict) -> int | None:
    """Index of the pool member NF-equivalent to the most other pool members (ties -> first)."""
    if not pool:
        return None
    best, bi = -1, None
    for i, a in enumerate(pool):
        n = sum(1 for j, b in enumerate(pool) if j != i and (a == b or (pairs.get((a, b)) or {}).get("equiv") is True))
        if n > best:
            best, bi = n, i
    return bi


# =================================================================================================== text side
L3_GATED = ["mm_role", "mm_claims", "mm_order", "missing_frac", "extra_frac"]  # exp A prereg L3_gated_fields


def l2_bow(text: str, fol_ast) -> dict:
    """L2-bow (exp A, unchanged): n_unanchored predicates + share of uncarried content words; continuous score = sum."""
    import fol_triage as FT
    r = FT.content_accounting(text, fol_ast)
    return {"l2_bow": r["n_unanchored"] + r["uncarried_frac"], "bow_n_unanch": r["n_unanchored"],
            "bow_uncarried": r["uncarried_frac"], "bow_flag": int(r["flag"]), "bow_unanchored": r["unanchored_preds"]}


def l3_z3(q: dict | None, fol_ast, prof: dict | None = None) -> dict:
    """L3 (exp A, unchanged): text questionnaire q vs the exact z3 role profile of the formula; score = sum of gated
    field mismatches. q None -> missing (caller imputes)."""
    import fol_triage as FT
    if prof is None:
        prof = FT.formula_role_profile(fol_ast)
    if q is None:
        return {"l3_z3": None, "l3_fields": None, "profile": prof}
    cmp = FT.l3_compare(q, prof)
    return {"l3_z3": FT.l3_score(cmp, L3_GATED), "l3_fields": {k: cmp.get(k) for k in FT.L3_FIELDS}, "profile": prof}


def text_side(text: str, fol_ast, q: dict | None, prof: dict | None = None, with_role: bool = True) -> dict:
    """All TEXT-side columns: l2_bow (+parts), l3_z3 (+fields), l1 lint codes, l2_role count (columns only)."""
    import fol_triage as FT
    out = {}
    t0 = time.time()
    out.update(l2_bow(text, fol_ast))
    try:
        l3 = l3_z3(q, fol_ast, prof)
        prof = l3.pop("profile")
        out.update(l3)
    except (z3.Z3Exception, RecursionError, KeyError, ValueError, TypeError) as ex:
        out.update(l3_z3=None, l3_fields=None, l3_err=str(ex)[:100])
    try:
        out["l1_codes"] = FT.fol_lint(fol_ast)["codes"]
    except (z3.Z3Exception, RecursionError, KeyError, ValueError, TypeError):
        out["l1_codes"] = None
    if with_role and prof is not None:
        try:
            ra = FT.role_accounting(text, fol_ast, prof)
            out["l2_role"] = sum(ra.get(k, 0) for k in ("cond_in_up", "assert_in_down", "pol_flip", "slot_swap", "exc_wrong"))
        except (RecursionError, KeyError, ValueError, TypeError, IndexError, AttributeError) as ex:
            out["l2_role"] = None
            out["l2_role_err"] = str(ex)[:80]
    out["secs_text"] = round(time.time() - t0, 3)
    return out


# =================================================================================================== fusion
def _z(x, mu, sd):
    return 0.0 if x is None else (x - mu) / (sd if sd > 0 else 1.0)


def apply_logistic(model: dict, feats: dict) -> float:
    """model = {'features', 'mean', 'sd', 'coef', 'intercept'}; missing feature -> z = 0."""
    s = model["intercept"]
    for f, m, sd, c in zip(model["features"], model["mean"], model["sd"], model["coef"]):
        s += c * _z(feats.get(f), m, sd)
    return 1 / (1 + math.exp(-s))


def fused_score(frozen: dict, feats: dict) -> dict:
    """Frozen PEER+TEXT fusion. Unparseable -> p_error 1.0. peer_unavailable -> frozen TEXT-only model (pre-registered).
    fired_signal = argmax standardized contribution (PEER = g/c_score_nf features, TEXT = l2_bow/l3)."""
    if feats.get("coverage_status") == "UNPARSEABLE":
        return {"p_error": 1.0, "flag": 1, "fired_signal": "UNPARSEABLE", "model_used": "none"}
    main = frozen["fusion"]
    use = main
    if feats.get("peer_unavailable") or feats.get(main["features"][0]) is None:
        use = frozen["text_only"]
    p = apply_logistic(use, feats)
    contrib = {f: c * _z(feats.get(f), m, sd) for f, m, sd, c in zip(use["features"], use["mean"], use["sd"], use["coef"])}
    top = max(contrib, key=contrib.get) if contrib else None
    sig = "PEER" if top in ("g_score", "c_score_nf", "c_score_align") else ("TEXT" if top else None)
    thr = main["threshold"] if use is main else frozen["text_only"]["threshold"]
    return {"p_error": p, "flag": int(p >= thr), "fired_signal": sig, "model_used": "fusion" if use is main else "text_only"}


def peer_text_score(text: str, fol: str, peers: list[str], frozen: dict, q: dict | None = None,
                    variant: str | None = None) -> dict:
    """One-call API: score candidate `fol` for `text` against a list of peer formalisations (other systems / families).
    q = cached L3 questionnaire of the text (None -> L3 missing, imputed z=0). Returns p_error, flag, fired_signal,
    unit_codes, g_score, c_score_nf, l2_bow, l3_z3, coverage_status."""
    variant = variant or frozen["variant"]
    tau = frozen["tau"].get(variant)
    e = parse_fol(fol)
    if e is None:
        return {"p_error": 1.0, "flag": 1, "coverage_status": "UNPARSEABLE", "fired_signal": "UNPARSEABLE"}
    cs = canon(e)
    ps = [canon(x) for x in (parse_fol(p) for p in peers) if x is not None]
    ent = Entailer(frozen["timeout_ms"])
    pairs = {}
    for a in [cs] + ps:
        for b in ps:
            if a != b and (a, b) not in pairs:
                pairs[(a, b)] = pair_result(a, b, ent, text=text, variant=variant, k=frozen["k"], tau=tau)
    gc_ = graded_consensus(cs, ps, pairs, ent)
    feats = {"g_score": gc_["g_score"], "c_score_nf": gc_["c_score_nf"], "peer_unavailable": gc_["peer_unavailable"]}
    feats.update(text_side(text, e, q, with_role=False))
    fs = fused_score(frozen, feats)
    return {**fs, "unit_codes": gc_.get("unit_codes"), "g_score": gc_["g_score"], "c_score_nf": gc_["c_score_nf"],
            "l2_bow": feats["l2_bow"], "l3_z3": feats.get("l3_z3"), "coverage_status": "OK"}
