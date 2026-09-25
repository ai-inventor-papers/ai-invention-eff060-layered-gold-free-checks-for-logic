"""Name-free (alignment-free) labelling of free-vocabulary FOL candidates against template readings.

No name similarity is used anywhere: symbol names are only used (a) as identifiers, (b) by the B5 lexical-negation
regex, which licenses the map ``P := ¬U`` (a gloss check still has to accept it). Which candidate symbol means which
template atom is decided by EXHAUSTIVE enumeration of a declared map family under SOUND semantic prunes, followed by
z3 equivalence; the lexical plausibility of the winning map is decided separately by a gloss check (``checker``).

Map family (frozen in prereg_freelab.json):
  * A candidate predicate is a UNIT if, in every occurrence, all argument positions but one (the subject position)
    hold the same constants, and those constants occur nowhere else ("constant absorption"; unary predicates are
    trivially units). A template atom over the single variable x (U(x) or R(x, c)) is a template UNIT.
  * UNIT maps a candidate unit to exactly one template unit (plain, B1 reification and B2 de-reification are all
    this form: P(x) := R(x, c); P(x, k) := U(x); P(x, k) := R(x, c)). B5: P := ¬u (only if the name's first token is a
    negation marker). B3 merge: P := u1 ∧ u2 (u1, u2 sibling conjuncts of the reading). B4 split: two candidate units
    that only ever occur as positive sibling conjuncts both := u.
  * REL maps a genuinely relational candidate predicate (arity 2, not a unit) to a template binary predicate, either
    argument order; its non-absorbed constants map injectively to template constants or stay free (fresh).
  * Injective: each template unit / predicate is the target of at most one candidate symbol (B4 excepted).
    Structural bridge uses (B3 + B4) <= MAX_STRUCT per map; B1/B2/B5 are 1:1 unit forms and are not capped.
  * Semantically inert candidate symbols (F ≡ F[s := fresh]) are dropped (kept as fresh symbols in the image).
Sound prunes: relevance (every relevant candidate symbol must be mapped; every template unit must be covered),
polarity (z3-exact monotonicity is preserved by 1:1 generic substitutions), and a finite-model fingerprint
(128 interpretations, domain 2-3, fixed seeds; a mismatch is a certified countermodel). Maps that pass the
fingerprint go to z3 (2 s, retry 10 s).

EXACT: ERROR (no equivalent map) is exact RELATIVE TO THIS FAMILY and these caps; every equivalent map is a z3 proof.
BOUNDED: maps outside the family (extra quantified structure, ∃-for-constant, ternary relations with variables, ...)
are not searched; the search stops at MAX_MAPS maps or MAX_SECS seconds per (candidate, reading) -> CAP.
"""
from __future__ import annotations

import itertools
import re
import time
import zlib
from collections import Counter, defaultdict
from functools import lru_cache

import z3

from fol import mkpred, parse, preds, profile, to_z3, valid, U
from repair_census_min import atoms, bound_vars

MAX_MAPS = 200_000
MAX_SECS = 90.0
MAX_STRUCT = 2
N_FP = 128
Z3_MS, Z3_MS_RETRY = 2000, 10000
NEG_TOKEN = re.compile(r"^(not|non|no|un|in|im|il|ir|dis|never|lacks?|without)$", re.I)
NEG_PREFIX = re.compile(r"^(Un|Non|In|Im|Dis)[A-Z]")
FLIP = {"UP": "DOWN", "DOWN": "UP", "NONMONO": "NONMONO"}


# ------------------------------------------------------------------------------------------------ AST helpers
def to_str(e) -> str:
    k = e[0]
    if k == "atom":
        return f"{e[1]}({', '.join(e[2])})" if e[2] else e[1]
    if k in ("all", "ex"):
        return f"{'∀' if k == 'all' else '∃'}{e[1]} ({to_str(e[2])})"
    if k == "not":
        return f"¬{to_str(e[1])}"
    sym = {"and": "∧", "or": "∨", "imp": "→", "iff": "↔", "xor": "⊕"}[k]
    return f"({to_str(e[1])} {sym} {to_str(e[2])})"


def name_tokens(n: str) -> list[str]:
    return re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", n.replace("_", " "))


def negation_named(name: str) -> bool:
    """B5 licence: first CamelCase/underscore token is a negation marker, or the name starts Un/Non/In/Im/Dis+Upper."""
    t = name_tokens(name)
    return bool((t and NEG_TOKEN.match(t[0])) or NEG_PREFIX.match(name))


def free_consts(e) -> set:
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


def occurrences(e):
    """-> list of (atom, bound-set at that occurrence)."""
    out = []

    def walk(x, bv):
        if x[0] == "atom":
            out.append((x, bv))
        elif x[0] in ("all", "ex"):
            walk(x[2], bv | {x[1]})
        elif x[0] == "not":
            walk(x[1], bv)
        else:
            walk(x[1], bv); walk(x[2], bv)
    walk(e, frozenset())
    return out


def conj_chains(e):
    """All maximal ∧-chains -> list of lists of direct conjuncts (subformulas)."""
    chains = []

    def flat(x, acc):
        if x[0] == "and":
            flat(x[1], acc); flat(x[2], acc)
        else:
            acc.append(x)

    def walk(x, parent_and):
        k = x[0]
        if k == "and":
            if not parent_and:
                acc = []
                flat(x, acc)
                chains.append(acc)
            walk(x[1], True); walk(x[2], True)
        elif k in ("all", "ex"):
            walk(x[2], False)
        elif k == "not":
            walk(x[1], False)
        elif k != "atom":
            walk(x[1], False); walk(x[2], False)
    walk(e, False)
    return chains


def rename_const(e, old: str, new: str, bv=frozenset()):
    k = e[0]
    if k == "atom":
        return ("atom", e[1], tuple(new if (a == old and a not in bv) else a for a in e[2]))
    if k in ("all", "ex"):
        return (k, e[1], rename_const(e[2], old, new, bv | {e[1]}))
    if k == "not":
        return ("not", rename_const(e[1], old, new, bv))
    return (k, rename_const(e[1], old, new, bv), rename_const(e[2], old, new, bv))


def z3_equiv(a, b, ms: int) -> bool | None:
    ar = {**preds(a), **preds(b)}
    P = {q: mkpred(q, m) for q, m in ar.items()}
    return valid(to_z3(a, {}, P) == to_z3(b, {}, P), ms)


def z3_equiv_retry(a, b) -> bool | None:
    r = z3_equiv(a, b, Z3_MS)
    return z3_equiv(a, b, Z3_MS_RETRY) if r is None else r


# ------------------------------------------------------------------------------------------------ finite models
DENS = (50, 75, 90, 25)


@lru_cache(maxsize=2_000_000)
def _atom_val(i: int, name: str, args: tuple) -> bool:
    return (zlib.crc32(f"{i}|{name}|{args}".encode()) % 100) < DENS[i % 4]


@lru_cache(maxsize=200_000)
def _const_val(i: int, name: str) -> int:
    return zlib.crc32(f"{i}|const|{name}".encode()) % dom_size(i)


def dom_size(i: int) -> int:
    return 2 + (i // 4) % 2


def ev(e, i: int, env: dict) -> bool:
    """Exact truth value of e in finite interpretation i (domain 2 or 3; predicate tables and constants from a fixed
    crc32 hash of (i, symbol, args)); same semantics as fol.to_z3 (no unique names, non-empty domain)."""
    k = e[0]
    if k == "atom":
        args = tuple(env[a] if a in env else _const_val(i, a) for a in e[2])
        return _atom_val(i, f"{e[1]}/{len(e[2])}", args)
    if k == "all":
        return all(ev(e[2], i, {**env, e[1]: d}) for d in range(dom_size(i)))
    if k == "ex":
        return any(ev(e[2], i, {**env, e[1]: d}) for d in range(dom_size(i)))
    if k == "not":
        return not ev(e[1], i, env)
    a = ev(e[1], i, env)
    if k == "and":
        return a and ev(e[2], i, env)
    if k == "or":
        return a or ev(e[2], i, env)
    if k == "imp":
        return (not a) or ev(e[2], i, env)
    b = ev(e[2], i, env)
    return (a == b) if k == "iff" else (a != b)


def fingerprint(e, n: int = N_FP) -> tuple:
    return tuple(ev(e, i, {}) for i in range(n))


def first_mismatch(e, ref_fp: tuple) -> int | None:
    """Index of the first interpretation where e and the reference differ (a certified countermodel), else None."""
    for i, v in enumerate(ref_fp):
        if ev(e, i, {}) != v:
            return i
    return None


# ------------------------------------------------------------------------------------------------ symbol analysis
def analyse_symbols(e) -> dict:
    """Units / relations / constants of a formula. key = 'name/arity'."""
    occ = occurrences(e)
    by = defaultdict(list)
    for a, bv in occ:
        by[f"{a[1]}/{len(a[2])}"].append((a, bv))
    const_sites = defaultdict(set)  # constant -> {(key, pos)}
    for k, lst in by.items():
        for a, bv in lst:
            for j, x in enumerate(a[2]):
                if x not in bv:
                    const_sites[x].add((k, j))
    units, rels, other = {}, {}, {}
    absorbed = set()
    for k, lst in by.items():
        n = len(lst[0][0][2])
        name = lst[0][0][1]
        if n == 0:
            other[k] = {"name": name, "arity": 0}
            continue
        if n == 1:
            units[k] = {"name": name, "arity": 1, "subj": 0, "fills": {}}
            continue
        cands = []
        for s in range(n):
            fills, ok, has_var = {}, True, False
            for a, bv in lst:
                if a[2][s] in bv:
                    has_var = True
                for j, x in enumerate(a[2]):
                    if j == s:
                        continue
                    if x in bv or fills.setdefault(j, x) != x:
                        ok = False
            if ok and has_var and all(const_sites[c] == {(k, j)} for j, c in fills.items()):
                cands.append((s, fills))
        if len(cands) == 1:
            s, fills = cands[0]
            units[k] = {"name": name, "arity": n, "subj": s, "fills": fills}
            absorbed |= set(fills.values())
        elif n == 2:
            rels[k] = {"name": name, "arity": 2}
        else:
            other[k] = {"name": name, "arity": n}
    consts = sorted(c for c in const_sites if c not in absorbed)
    return {"units": units, "rels": rels, "other": other, "consts": consts, "absorbed": sorted(absorbed)}


def unit_display(u: dict, subj: str = "x") -> str:
    args = [u["fills"].get(j, subj) if j != u["subj"] else subj for j in range(u["arity"])]
    return f"{u['name']}({', '.join(args)})"


# ------------------------------------------------------------------------------------------------ template side
class Reading:
    """One template reading: its units (atoms over the single variable), polarity, siblings and fingerprint."""

    def __init__(self, fol: str, unit_glosses: dict | None = None):
        self.fol = fol
        self.e = parse(fol)
        self.fp = fingerprint(self.e)
        sy = analyse_symbols(self.e)
        self.prof = profile(self.e, ms=5000)
        self.units = {}
        inst = {}
        for a, bv in occurrences(self.e):  # template units = atom instances with exactly one variable argument
            vpos = [j for j, x in enumerate(a[2]) if x in bv]
            if len(vpos) != 1:
                continue
            s = vpos[0]
            u = {"name": a[1], "arity": len(a[2]), "subj": s, "fills": {j: x for j, x in enumerate(a[2]) if j != s}}
            inst.setdefault(unit_display(u), (f"{a[1]}/{len(a[2])}", u))
        pred_count = Counter(k for k, _ in inst.values())
        for uid, (k, u) in inst.items():
            pol = self.prof.get(k)
            self.units[uid] = {**u, "key": k, "pol": pol if pred_count[k] == 1 else None,
                               "gloss_pos": (unit_glosses or {}).get(uid, {}).get("gloss_pos") or f"x: {uid}",
                               "gloss_neg": (unit_glosses or {}).get(uid, {}).get("gloss_neg") or f"x: not {uid}"}
        sy["rels"] = {k: v for k, v in sy["rels"].items() if k not in pred_count}
        self.rel_preds = {k: v for k, v in sy["rels"].items()}
        for uid, u in self.units.items():  # a template binary unit's predicate is also a relation target
            if u["arity"] == 2:
                self.rel_preds.setdefault(u["key"], {"name": u["name"], "arity": 2})
        self.rel_pol = {k: self.prof.get(k) for k in self.rel_preds}
        self.consts = sorted({c for u in self.units.values() for c in u["fills"].values()} | set(sy["consts"]))
        self.other = sy["other"]
        self.relevant_units = [uid for uid, u in self.units.items() if self.prof.get(u["key"]) != "VACUOUS"]
        sib = set()
        for ch in conj_chains(self.e):
            pos = [unit_display_of_atom(x, self.units) for x in ch if x[0] == "atom"]
            pos = [p for p in pos if p]
            for a, b in itertools.combinations(sorted(set(pos)), 2):
                sib.add((a, b))
        self.siblings = sorted(sib)

    def unit_atom(self, uid: str, subj_term: str):
        u = self.units[uid]
        args = tuple(u["fills"].get(j, subj_term) if j != u["subj"] else subj_term for j in range(u["arity"]))
        return ("atom", u["name"], args)


def unit_display_of_atom(a, units: dict) -> str | None:
    for uid, u in units.items():
        if u["name"] == a[1] and u["arity"] == len(a[2]) and all(a[2][j] == c for j, c in u["fills"].items()):
            return uid
    return None


# ------------------------------------------------------------------------------------------------ candidate side
class Candidate:
    """Parsed candidate + relevance (z3) + polarity (z3) + units/relations/constants."""

    def __init__(self, fol: str):
        self.fol = fol
        self.e = parse(fol)
        self.sy = analyse_symbols(self.e)
        self.prof = profile(self.e, ms=3000)
        self.const_rel = {}
        for c in self.sy["consts"]:
            r = z3_equiv(self.e, rename_const(self.e, c, c + "__alt"), 3000)
            self.const_rel[c] = "INERT" if r is True else ("RELEVANT" if r is False else "UNKNOWN")
        self.inert = sorted([k for k in list(self.sy["units"]) + list(self.sy["rels"]) + list(self.sy["other"])
                             if self.prof.get(k) == "VACUOUS"] + [f"const:{c}" for c, v in self.const_rel.items() if v == "INERT"])
        self.split_pairs = self._split_pairs()

    def _split_pairs(self) -> list[tuple[str, str]]:
        """B4 licence: two unary-form units that occur ONLY as positive direct sibling conjuncts with the same
        subject term (checked syntactically on every occurrence)."""
        units = self.sy["units"]
        occ_count = Counter(f"{a[1]}/{len(a[2])}" for a, _ in occurrences(self.e))
        chains = conj_chains(self.e)
        out = []
        keys = sorted(units)
        for k1, k2 in itertools.combinations(keys, 2):
            u1, u2 = units[k1], units[k2]
            n_pair = 0
            for ch in chains:
                a1 = [x for x in ch if x[0] == "atom" and f"{x[1]}/{len(x[2])}" == k1]
                a2 = [x for x in ch if x[0] == "atom" and f"{x[1]}/{len(x[2])}" == k2]
                for x in a1:
                    if any(y[2][u2["subj"]] == x[2][u1["subj"]] for y in a2):
                        n_pair += 1
            if n_pair and n_pair == occ_count[k1] == occ_count[k2]:
                out.append((k1, k2))
        return out


# ------------------------------------------------------------------------------------------------ enumeration
def _pol_ok(p, q) -> bool:
    """Candidate polarity p vs target polarity q (None / UNKNOWN = no prune)."""
    if p in (None, "UNKNOWN") or q in (None, "UNKNOWN"):
        return True
    return p == q


def unit_options(key: str, cand: Candidate, rd: Reading) -> list[tuple]:
    p = cand.prof.get(key)
    name = cand.sy["units"][key]["name"]
    opts = []
    for uid, u in rd.units.items():
        if _pol_ok(p, u["pol"]):
            opts.append(("U", uid))
        if negation_named(name) and _pol_ok(p, FLIP.get(u["pol"], u["pol"]) if u["pol"] else None):
            opts.append(("N", uid))
    for a, b in rd.siblings:
        pa, pb = rd.units[a]["pol"], rd.units[b]["pol"]
        if p in ("UP", "DOWN"):
            if _pol_ok(p, pa) and _pol_ok(p, pb):
                opts.append(("M", a, b))
        else:
            opts.append(("M", a, b))
    if p == "UNKNOWN":
        opts.append(("F",))
    return opts


def rel_options(key: str, cand: Candidate, rd: Reading) -> list[tuple]:
    p = cand.prof.get(key)
    opts = []
    for rk, r in rd.rel_preds.items():
        if _pol_ok(p, rd.rel_pol.get(rk)):
            opts.append(("R", rk, 0))
            opts.append(("R", rk, 1))
    if p == "UNKNOWN":
        opts.append(("F",))
    return opts


def build_image(cand: Candidate, rd: Reading, assign: dict, cmap: dict):
    """Substitute the map into the candidate AST -> formula over template symbols (+ fresh symbols)."""
    units, rels = cand.sy["units"], cand.sy["rels"]

    def term(t, bv):
        if t in bv:
            return t
        if t in cmap and cmap[t] is not None:
            return cmap[t]
        return "k__" + t

    def sub(x, bv):
        k = x[0]
        if k == "atom":
            key = f"{x[1]}/{len(x[2])}"
            opt = assign.get(key)
            if opt is None or opt[0] == "F":
                return ("atom", "p__" + x[1], tuple(term(t, bv) for t in x[2]))
            if key in units:
                s = term(x[2][units[key]["subj"]], bv)
                if opt[0] in ("U", "S"):
                    return rd.unit_atom(opt[1], s)
                if opt[0] == "N":
                    return ("not", rd.unit_atom(opt[1], s))
                if opt[0] == "M":
                    return ("and", rd.unit_atom(opt[1], s), rd.unit_atom(opt[2], s))
            if key in rels and opt[0] == "R":
                a, b = (term(t, bv) for t in x[2])
                nm = rd.rel_preds[opt[1]]["name"]
                return ("atom", nm, (a, b) if opt[2] == 0 else (b, a))
            raise ValueError(f"bad option {opt} for {key}")
        if k in ("all", "ex"):
            return (k, x[1], sub(x[2], bv | {x[1]}))
        if k == "not":
            return ("not", sub(x[1], bv))
        return (k, sub(x[1], bv), sub(x[2], bv))
    return sub(cand.e, frozenset())


def map_to_json(assign: dict, cmap: dict, cand: Candidate, rd: Reading) -> dict:
    out = {}
    for key, opt in sorted(assign.items()):
        disp = unit_display(cand.sy["units"][key]) if key in cand.sy["units"] else key
        if opt[0] in ("U", "S"):
            out[disp] = opt[1] + (" [split]" if opt[0] == "S" else "")
        elif opt[0] == "N":
            out[disp] = "¬" + opt[1]
        elif opt[0] == "M":
            out[disp] = f"{opt[1]} ∧ {opt[2]}"
        elif opt[0] == "R":
            nm = rd.rel_preds[opt[1]]["name"]
            out[disp] = f"{nm}(x, y)" if opt[2] == 0 else f"{nm}(y, x)"
        else:
            out[disp] = "<fresh>"
    for c, t in sorted(cmap.items()):
        out[f"const:{c}"] = t if t is not None else "<free>"
    return out


def bridges_of(assign: dict, cand: Candidate, rd: Reading) -> list[str]:
    out = []
    for key, opt in assign.items():
        if key not in cand.sy["units"]:
            continue
        cu = cand.sy["units"][key]
        if opt[0] == "N":
            out.append("B5")
        elif opt[0] == "M":
            out.append("B3")
        elif opt[0] == "S":
            out.append("B4")
        elif opt[0] == "U":
            tu = rd.units[opt[1]]
            if cu["arity"] == 1 and tu["arity"] > 1:
                out.append("B1")
            elif cu["arity"] > 1 and tu["arity"] == 1:
                out.append("B2")
    return sorted(out)


def search(cand: Candidate, rd: Reading, max_maps: int = MAX_MAPS, max_secs: float = MAX_SECS,
           keep_equiv: int = 100_000) -> dict:
    """Exhaustive enumeration of the declared family for one (candidate, reading). Returns counts, certificates and
    every z3-equivalent map (up to keep_equiv stored)."""
    t0 = time.time()
    res = {"n_maps_enumerated": 0, "n_fp_pass": 0, "n_equiv": 0, "cert": Counter(), "equiv_maps": [],
           "z3_unknown": 0, "capped": False, "unmappable": [], "images": set()}
    units, rels = cand.sy["units"], cand.sy["rels"]
    relevant_other = [k for k in cand.sy["other"] if cand.prof.get(k) not in ("VACUOUS",)]
    if relevant_other:
        res["unmappable"] = relevant_other
        res["cert"]["unmappable_symbol"] += 1
        return _finish(res, t0)
    rel_units = [k for k in units if cand.prof.get(k) != "VACUOUS"]
    rel_rels = [k for k in rels if cand.prof.get(k) != "VACUOUS"]
    consts = [c for c in cand.sy["consts"] if cand.const_rel.get(c) != "INERT"]
    # split variants: none, or one/two disjoint licensed pairs
    pairs = [p for p in cand.split_pairs if p[0] in rel_units and p[1] in rel_units]
    split_sets = [()]
    for n in range(1, MAX_STRUCT + 1):
        for combo in itertools.combinations(pairs, n):
            flat = [k for p in combo for k in p]
            if len(flat) == len(set(flat)):
                split_sets.append(combo)
    need = set(rd.relevant_units)
    for splits in split_sets:
        # symbols to assign: each split pair is one pseudo-symbol
        split_of = {p[0]: p for p in splits}
        skip = {p[1] for p in splits}
        syms = []
        for k in rel_units:
            if k in skip:
                continue
            if k in split_of:
                p = split_of[k]
                pa, pb = cand.prof.get(p[0]), cand.prof.get(p[1])
                q = pa if pa == pb else None
                opts = [("S", uid) for uid, u in rd.units.items() if q is None or _pol_ok(q, u["pol"])]
                syms.append((("SPLIT",) + p, opts))
            else:
                syms.append((k, unit_options(k, cand, rd)))
        for k in rel_rels:
            syms.append((k, rel_options(k, cand, rd)))
        if any(not o for _, o in syms):
            res["cert"]["no_polarity_compatible_target"] += 1
            continue
        syms.sort(key=lambda s: len(s[1]))
        n_struct0 = len(splits)
        _dfs(0, syms, {}, set(), set(), n_struct0, need, consts, cand, rd, res, t0, max_maps, max_secs, keep_equiv)
        if res["capped"]:
            break
    return _finish(res, t0)


def _covers(opt) -> list[str]:
    if opt[0] in ("U", "N", "S"):
        return [opt[1]]
    if opt[0] == "M":
        return [opt[1], opt[2]]
    return []


def _dfs(i, syms, assign, used_units, used_rels, n_struct, need, consts, cand, rd, res, t0, max_maps, max_secs, keep):
    if res["capped"]:
        return
    # count prune: remaining symbols can cover at most 2 units each (merge), 1 otherwise
    remaining_need = need - used_units - {uid for uid in need if rd.units[uid]["key"] in used_rels}
    cap_left = sum(2 if any(o[0] == "M" for o in s[1]) else (1 if any(o[0] != "F" and o[0] != "R" for o in s[1]) else 0)
                   for s in syms[i:])
    rel_left = [s for s in syms[i:] if any(o[0] == "R" for o in s[1])]
    if len(remaining_need) > cap_left + 99 * len(rel_left):
        res["cert"]["count_prune_subtree"] += 1
        return
    if i == len(syms):
        if remaining_need:
            res["cert"]["coverage"] += 1
            return
        _leaf(assign, consts, cand, rd, res, t0, max_maps, max_secs, keep)
        return
    key, opts = syms[i]
    for opt in opts:
        if opt[0] in ("U", "N", "S", "M"):
            cov = _covers(opt)
            if any(u in used_units or rd.units[u]["key"] in used_rels for u in cov):
                continue
            ns = n_struct + (1 if opt[0] == "M" else 0)
            if ns > MAX_STRUCT:
                continue
            if opt[0] == "M" and any(o[0] == "S" for o in assign.values()) or (opt[0] == "S" and any(o[0] == "M" for o in assign.values())):
                continue  # prereg v1.1 (D6): a map never mixes a B3 merge with a B4 split
            if isinstance(key, tuple):  # split pseudo-symbol
                a2 = {**assign, key[1]: opt, key[2]: opt}
            else:
                a2 = {**assign, key: opt}
            _dfs(i + 1, syms, a2, used_units | set(cov), used_rels, ns, need, consts, cand, rd, res, t0, max_maps,
                 max_secs, keep)
        elif opt[0] == "R":
            if opt[1] in used_rels or any(u["key"] == opt[1] for uid, u in rd.units.items() if uid in used_units):
                continue
            _dfs(i + 1, syms, {**assign, key: opt}, used_units, used_rels | {opt[1]}, n_struct, need, consts, cand,
                 rd, res, t0, max_maps, max_secs, keep)
        else:  # F: leave an UNKNOWN-relevance symbol fresh
            _dfs(i + 1, syms, {**assign, key: opt}, used_units, used_rels, n_struct, need, consts, cand, rd, res,
                 t0, max_maps, max_secs, keep)
        if res["capped"]:
            return


def _leaf(assign, consts, cand, rd, res, t0, max_maps, max_secs, keep):
    tconsts = rd.consts
    choices = [list(tconsts) + [None] for _ in consts]
    for combo in itertools.product(*choices) if consts else [()]:
        used = [c for c in combo if c is not None]
        if len(used) != len(set(used)):
            continue
        res["n_maps_enumerated"] += 1
        if res["n_maps_enumerated"] > max_maps or (res["n_maps_enumerated"] % 64 == 0 and time.time() - t0 > max_secs):
            res["capped"] = True
            return
        cmap = dict(zip(consts, combo))
        img = build_image(cand, rd, assign, cmap)
        mm = first_mismatch(img, rd.fp)
        if mm is not None:
            res["cert"]["countermodel"] += 1
            continue
        res["n_fp_pass"] += 1
        r = z3_equiv_retry(img, rd.e)
        if r is True:
            res["n_equiv"] += 1
            if len(res["equiv_maps"]) < keep:
                res["equiv_maps"].append({"assign": dict(assign), "cmap": cmap, "image": to_str(img)})
        elif r is False:
            res["cert"]["z3_sat"] += 1
        else:
            res["z3_unknown"] += 1
        if time.time() - t0 > max_secs:
            res["capped"] = True
            return


def _finish(res, t0):
    res["secs"] = round(time.time() - t0, 3)
    res["cert"] = dict(res["cert"])
    res.pop("images", None)
    return res


# ------------------------------------------------------------------------------------------------ gloss pairs
def pair_items(m: dict, cand: Candidate, rd: Reading) -> list[tuple[str, str]]:
    """(symbol use, proposed meaning) pairs of one equivalent map. Relation maps are shown per candidate atom."""
    out = []
    assign = m["assign"]
    done = set()
    for key, opt in sorted(assign.items(), key=lambda kv: kv[0]):
        if key in done or opt[0] == "F":
            continue
        if key in cand.sy["units"]:
            use = unit_display(cand.sy["units"][key])
            if opt[0] == "S":
                other = [k for k, o in assign.items() if o == opt and k != key]
                done.update(other)
                use = " ∧ ".join([use] + [unit_display(cand.sy["units"][k]) for k in other])
                out.append((use, rd.units[opt[1]]["gloss_pos"]))
            elif opt[0] == "U":
                out.append((use, rd.units[opt[1]]["gloss_pos"]))
            elif opt[0] == "N":
                out.append((use, rd.units[opt[1]]["gloss_neg"]))
            elif opt[0] == "M":
                out.append((use, rd.units[opt[1]]["gloss_pos"] + " and " + rd.units[opt[2]]["gloss_pos"]))
        elif key in cand.sy["rels"] and opt[0] == "R":
            seen = set()
            for a, bv in occurrences(cand.e):
                if f"{a[1]}/{len(a[2])}" != key:
                    continue
                args = [x if x in bv else x for x in a[2]]
                va = [("x" if x in bv else x) for x in args]
                if len({x for x in args if x in bv}) == 2:
                    va = ["x", "y"] if args[0] != args[1] else ["x", "x"]
                disp = f"{a[1]}({', '.join(va)})"
                if disp in seen:
                    continue
                seen.add(disp)
                cm = m["cmap"]
                t = [(x if x in bv else (cm.get(x) or "k__" + x)) for x in a[2]]
                t = t if opt[2] == 0 else t[::-1]
                img = ("atom", rd.rel_preds[opt[1]]["name"], tuple(t))
                uid = None
                for cand_uid, u in rd.units.items():
                    if u["name"] == img[1] and u["arity"] == 2 and all(img[2][j] == c for j, c in u["fills"].items()):
                        uid = cand_uid
                if uid is not None:
                    # subject variable of the unit must be the variable argument
                    out.append((disp, rd.units[uid]["gloss_pos"]))
                else:
                    ex = next((u for u in rd.units.values() if u["key"] == opt[1]), None)
                    g = ex["gloss_pos"] if ex else rd.rel_preds[opt[1]]["name"]
                    order = "first argument relates to second" if opt[2] == 0 else "second argument relates to first"
                    out.append((disp, f"the relation used in '{g}' ({order}), with no fixed object"))
    return out


# ------------------------------------------------------------------------------------------------ public API
def label_candidate(candidate_fol: str, readings: dict, glosses: dict | None = None, max_maps: int = MAX_MAPS,
                    max_secs: float = MAX_SECS) -> dict:
    """Map search of one candidate against readings {'weak','strong'[, 'converse']} (search only, no gloss).

    Returns {'status': MAPPED | READING_CHOICE | ERROR_CERT | UNRESOLVED_SEARCH_CAP | UNRESOLVED_Z3_UNKNOWN |
    UNPARSEABLE, 'per_reading': {...}, 'equiv_maps': [one per distinct pair set, with pair_ids], 'pairs_union': [...], ...}."""
    t0 = time.time()
    try:
        cand = Candidate(candidate_fol)
    except (ValueError, IndexError, TypeError, KeyError, RecursionError) as ex:
        return {"status": "UNPARSEABLE", "error": str(ex)[:160]}
    rds = {k: Reading(v, glosses) for k, v in readings.items() if v}
    return label_with(cand, rds, max_maps, max_secs, t0)


def label_with(cand: Candidate, rds: dict, max_maps: int, max_secs: float, t0: float | None = None) -> dict:
    t0 = t0 or time.time()
    per = {}
    for name, rd in rds.items():
        per[name] = search(cand, rd, max_maps=max_maps, max_secs=max_secs)
    main = [k for k in ("weak", "strong") if k in per]
    eq_main = [k for k in main if per[k]["n_equiv"] > 0]
    capped = any(per[k]["capped"] for k in per)
    unknown = any(per[k]["z3_unknown"] for k in per) or any(v == "UNKNOWN" for v in cand.prof.values()) \
        or any(v == "UNKNOWN" for v in cand.const_rel.values())
    if eq_main:
        status = "MAPPED"
        matched = "both" if len(eq_main) == 2 else eq_main[0]
    elif "converse" in per and per["converse"]["n_equiv"] > 0:
        status, matched = "READING_CHOICE", "converse"
    elif capped:
        status, matched = "UNRESOLVED_SEARCH_CAP", None
    elif unknown:
        status, matched = "UNRESOLVED_Z3_UNKNOWN", None
    else:
        status, matched = "ERROR_CERT", None
    # every equivalent map -> its (symbol use, meaning) pair set; maps with identical pair sets are one gloss unit
    pairs_union, pidx, sig_seen, maps = [], {}, {}, []
    entries_union, eidx = [], {}
    n_equiv = 0
    map_readings = eq_main + (["converse"] if "converse" in per and per["converse"]["n_equiv"] > 0 else [])
    for k in map_readings:
        for m in per[k]["equiv_maps"]:
            n_equiv += 1
            ps = pair_items(m, cand, rds[k])
            ids = []
            for p in ps:
                if p not in pidx:
                    pidx[p] = len(pairs_union)
                    pairs_union.append(p)
                ids.append(pidx[p])
            sig = tuple(sorted(set(ids)))
            if sig in sig_seen:
                continue
            sig_seen[sig] = len(maps)
            ent = []
            for a, b in map_to_json(m["assign"], m["cmap"], cand, rds[k]).items():
                es = f"{a} => {b}"
                if es not in eidx:
                    eidx[es] = len(entries_union)
                    entries_union.append(es)
                ent.append(eidx[es])
            maps.append({"reading": k, "entry_ids": ent, "bridges": bridges_of(m["assign"], cand, rds[k]),
                         "pair_ids": list(sig)})
    orbit_sigs = {(m["reading"], tuple(sorted(set(m["bridges"])))) for m in maps}
    cert = Counter()
    for k in per:
        cert.update(per[k]["cert"])
    return {"status": status, "matched_reading": matched,
            "per_reading": {k: {x: v[x] for x in ("n_maps_enumerated", "n_fp_pass", "n_equiv", "cert", "z3_unknown",
                                                    "capped", "unmappable", "secs")} for k, v in per.items()},
            "n_maps_enumerated": sum(v["n_maps_enumerated"] for v in per.values()),
            "n_maps_fingerprint_pass": sum(v["n_fp_pass"] for v in per.values()),
            "n_equiv_maps": n_equiv, "n_equiv_pairsets": len(maps), "n_equiv_map_orbits": len(orbit_sigs),
            "nonequiv_certificate_type_counts": dict(cert),
            "equiv_maps": maps, "pairs_union": [list(p) for p in pairs_union], "map_entries_union": entries_union,
            "irrelevant_symbols": cand.inert, "cand_profile": cand.prof, "const_relevance": cand.const_rel,
            "search_secs": round(time.time() - t0, 3)}


def gloss_decision(maps: list[dict], pairs_union: list, verdict: dict) -> tuple[str, int | None]:
    """verdict[(use, meaning)] = (checker_a, checker_b), each 'YES' / 'NO' / None (no verdict).
    CORRECT iff some weak/strong equivalent map has ALL its pairs YES from BOTH checkers (returns the first such index);
    else READING_CHOICE iff some T8-converse map does (v1.1 amendment D8: without names the converse is a relabelling of
    the weak reading, so the reading is resolved at the gloss level); ERROR_GLOSS iff EVERY equivalent map (any reading)
    has at least one pair that is NO from BOTH checkers; else UNRESOLVED_GLOSS."""
    best, best_conv = None, None
    all_rejected = True
    for i, m in enumerate(maps):
        vs = [verdict.get(tuple(pairs_union[j]), (None, None)) for j in m["pair_ids"]]
        if all(a == "YES" and b == "YES" for a, b in vs):
            if m["reading"] == "converse":
                best_conv = i if best_conv is None else best_conv
            elif best is None:
                best = i
        if not any(a == "NO" and b == "NO" for a, b in vs):
            all_rejected = False
    if best is not None:
        return "CORRECT", best
    if best_conv is not None:
        return "READING_CHOICE", best_conv
    if maps and all_rejected:
        return "ERROR_GLOSS", None
    return "UNRESOLVED_GLOSS", None


def exhaustive_map_label(candidate_fol: str, readings: dict, atoms: dict | None = None, glosses: dict | None = None,
                         checker=None) -> dict:
    """End-to-end name-free label of one candidate.

    candidate_fol: candidate formula (FOLIO/MALLS unicode syntax). readings: {'weak': fol, 'strong': fol
    [, 'converse': fol]} accepted readings (converse = stored but NOT accepted -> READING_CHOICE). atoms: optional
    {unit_str: (arity, predicate)} for documentation only (units are derived from the readings). glosses:
    {unit_str: {'gloss_pos': 'x ...', 'gloss_neg': 'x is not ...'}}. checker: callable(list[(use, meaning)]) ->
    {pair: (verdict_a, verdict_b)}; if None, a MAPPED candidate gets label UNRESOLVED_GLOSS (search-only mode).

    Returns {'label', 'certificate', 'reason', 'search': <label_candidate output>}.
    EXACT: ERROR_CERT = no map of the declared family makes the candidate z3-equivalent to an accepted reading (every
    rejected map carries a countermodel, a z3 SAT, or a sound-prune certificate). CORRECT = a z3-verified map whose
    every (symbol use, meaning) pair both checkers accept. BOUNDED: family + caps (see module docstring); the gloss
    check is model-relative."""
    s = label_candidate(candidate_fol, readings, glosses)
    st = s["status"]
    if st != "MAPPED":
        return {"label": st, "certificate": s.get("nonequiv_certificate_type_counts"), "reason": st, "search": s}
    if checker is None:
        return {"label": "UNRESOLVED_GLOSS", "certificate": s["equiv_maps"][0], "reason": "no checker", "search": s}
    uniq = [tuple(p) for p in s["pairs_union"]]
    verdict = checker(uniq)
    lab, idx = gloss_decision(s["equiv_maps"], s["pairs_union"], verdict)
    return {"label": lab, "certificate": s["equiv_maps"][idx] if idx is not None else None, "reason": lab, "search": s}


def equivalent_modulo_vocab_exhaustive(a_fol: str, b_fol: str, max_maps: int = MAX_MAPS, max_secs: float = MAX_SECS
                                       ) -> tuple[bool | None, dict | None, int]:
    """Is there a map of the declared family (units, B1-B5, relations, constants) under which a is z3-equivalent to b,
    or b to a? Symmetric (both directions are searched) and name-free (names are identifiers only; B5 uses the
    negation regex). Returns (True, map, n_maps) if found; (False, None, n) if the family is exhausted with
    certificates; (None, None, n) if a cap was hit or z3 returned unknown.
    Note: equivalence here is 'equivalent up to a family renaming', NOT meaning-equivalence: pair it with a gloss
    check before calling two formulas meaning-equivalent."""
    n = 0
    unknown = False
    for x, y in ((a_fol, b_fol), (b_fol, a_fol)):
        cand = Candidate(x)
        rd = Reading(y)
        r = search(cand, rd, max_maps=max_maps, max_secs=max_secs)
        n += r["n_maps_enumerated"]
        if r["n_equiv"] > 0:
            m = r["equiv_maps"][0]
            return True, map_to_json(m["assign"], m["cmap"], cand, rd), n
        if r["capped"] or r["z3_unknown"] or any(v == "UNKNOWN" for v in cand.prof.values()):
            unknown = True
    return (None if unknown else False), None, n
