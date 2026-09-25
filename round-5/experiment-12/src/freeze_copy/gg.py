"""gg: gloss-gated name-free agreement (GG) between two FOL formalisations of the SAME sentence (iteration 5, Part B).

DEFINITION (prereg_gg.json, PRIMARY). Formulas a and b AGREE under GG iff
  (1) they are z3-equivalent with identical symbols (exact), OR
  (2) some map in the PRIMARY family -- an injective, arity-consistent predicate map plus an injective constant map
      between the z3-RELEVANT symbols of a and b -- makes a z3-equivalent to b, AND the gloss checker says YES for EVERY
      non-identity mapped pair (identity = same lowercased name and same arity) of that map.
No name similarity, no aligner and no peer cueing are used to decide equivalence: names are identifiers for the search;
their meaning is judged only by the gloss checker, which sees the sentence and two symbol uses (never a whole formula,
never a label).

SEARCH (sound prunes only; family = bijections between relevant symbols, B1-B5 bridges are NOT in the primary family):
  * relevance: a predicate is dropped if its semantic monotonicity profile is VACUOUS (z3); a constant is dropped if
    renaming it leaves the formula equivalent (z3). Irrelevant symbols cannot matter for equivalence.
  * prefilter: equal multisets of relevant predicate arities and equal numbers of relevant constants, and equal
    multisets of (arity, polarity) where polarity in {UP, DOWN, NONMONO} (monotonicity is invariant under equivalence
    and renaming); else NOT agreeing without search.
  * enumeration: DFS over bijections within (arity, polarity) classes, identity-name targets first; each full map's
    image is checked against b's 128-interpretation fingerprint (dataset-5 freelab, a mismatch is a certified
    countermodel), then by z3 (2 s; UNKNOWN = not agreeing, counted). Up to KEEP equivalence maps are kept.
  * caps: MAX_MAPS maps or MAX_SECS seconds per pair; a cap hit = not agreeing (counted). If the full family exceeds
    MAX_MAPS, symbols whose (lowercased name, arity) occurs in BOTH formulas are anchored to themselves ('anchored'
    flag; a non-identity image of a shared name would need two distinct symbols of the same formula to mean the same).
MEASURES: whether two translations say the same thing up to a renaming whose every renamed symbol is a plausible
synonym in this sentence. GOLD-FREE: yes. COST: CPU (median ~0.1 s per surviving pair) + one small LLM call per <= 12
symbol pairs (google/gemini-2.5-flash, non-thinking), cached per (sentence, symbol pair).
"""
from __future__ import annotations

import itertools
import json
import re
import sys
import time
import zlib
from functools import lru_cache
from pathlib import Path

import z3

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gg_fol import mkpred, parse, preds, profile, to_z3, valid  # noqa: E402  (dataset-5 vendor/fol.py, verbatim copy)

MAX_MAPS = 20_000
MAX_SECS = 10.0
KEEP = 5
Z3_MS = 2000
N_FP = 128

# ------------------------------------------------------------------------------------------------ finite models
# (verbatim from dataset-5 src/freelab.py: DENS, _atom_val, _const_val, dom_size, ev, fingerprint, first_mismatch)
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
    for i, v in enumerate(ref_fp):
        if ev(e, i, {}) != v:
            return i
    return None


# ------------------------------------------------------------------------------------------------ AST helpers
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
            walk(x[1], bv)
            walk(x[2], bv)
    walk(e, frozenset())
    return out


def rename(e, pmap: dict, cmap: dict, bv=frozenset()):
    """Substitute predicate keys 'Name/n' -> new name and free constants -> new constant."""
    k = e[0]
    if k == "atom":
        key = f"{e[1]}/{len(e[2])}"
        return ("atom", pmap.get(key, e[1]), tuple(cmap.get(a, a) if a not in bv else a for a in e[2]))
    if k in ("all", "ex"):
        return (k, e[1], rename(e[2], pmap, cmap, bv | {e[1]}))
    if k == "not":
        return ("not", rename(e[1], pmap, cmap, bv))
    return (k, rename(e[1], pmap, cmap, bv), rename(e[2], pmap, cmap, bv))


def z3_equiv(a, b, ms: int = Z3_MS) -> bool | None:
    ar = {**preds(a), **preds(b)}
    P = {q: mkpred(q, m) for q, m in ar.items()}
    return valid(to_z3(a, {}, P) == to_z3(b, {}, P), ms)


def atom_example(e, key: str) -> str:
    """First occurrence of predicate key in e, printed with its argument terms (variables as bound in the formula)."""
    found = []

    def walk(x):
        if found:
            return
        if x[0] == "atom":
            if f"{x[1]}/{len(x[2])}" == key:
                found.append(f"{x[1]}({', '.join(x[2])})" if x[2] else x[1])
        elif x[0] in ("all", "ex"):
            walk(x[2])
        elif x[0] == "not":
            walk(x[1])
        else:
            walk(x[1])
            walk(x[2])
    walk(e)
    return found[0] if found else key


def const_example(e, c: str) -> str:
    found = []

    def walk(x, bv):
        if found:
            return
        if x[0] == "atom":
            if c in x[2] and c not in bv:
                found.append(f"{x[1]}({', '.join(x[2])})")
        elif x[0] in ("all", "ex"):
            walk(x[2], bv | {x[1]})
        elif x[0] == "not":
            walk(x[1], bv)
        else:
            walk(x[1], bv)
            walk(x[2], bv)
    walk(e, frozenset())
    return found[0] if found else c


# ------------------------------------------------------------------------------------------------ analysed formula
class Formula:
    """Parsed formula + relevance/polarity of its symbols + fingerprint (cache per string with analyse())."""

    def __init__(self, fol: str):
        self.fol = fol
        self.e = parse(fol)
        self.ar = preds(self.e)
        self.prof = profile(self.e, ms=3000)
        self.consts = sorted(free_consts(self.e))
        self.const_rel = {}
        for c in self.consts:
            r = z3_equiv(self.e, rename(self.e, {}, {c: c + "__alt"}), 3000)
            self.const_rel[c] = "INERT" if r is True else ("RELEVANT" if r is False else "UNKNOWN")
        self.rel_preds = sorted(k for k in self.ar if self.prof.get(k) != "VACUOUS")
        self.rel_consts = [c for c in self.consts if self.const_rel[c] != "INERT"]
        self.fp = fingerprint(self.e)

    def pclass(self, k: str) -> tuple:
        p = self.prof.get(k)
        return (self.ar[k], p if p in ("UP", "DOWN", "NONMONO") else "ANY")


_CACHE: dict = {}


def analyse(fol: str) -> Formula:
    if fol not in _CACHE:
        _CACHE[fol] = Formula(fol)
    return _CACHE[fol]


def _lname(k: str) -> str:
    return k.rsplit("/", 1)[0].lower() + "/" + k.rsplit("/", 1)[1]


def _compatible(pa: tuple, pb: tuple) -> bool:
    return pa[0] == pb[0] and (pa[1] == pb[1] or "ANY" in (pa[1], pb[1]))


def prefilter(A: Formula, Bf: Formula) -> str | None:
    """None if the pair may be map-equivalent; else the (sound) reason it cannot."""
    if sorted(A.ar[k] for k in A.rel_preds) != sorted(Bf.ar[k] for k in Bf.rel_preds):
        return "arity_multiset"
    if len(A.rel_consts) != len(Bf.rel_consts):
        return "n_constants"
    ca = sorted(A.pclass(k) for k in A.rel_preds if A.pclass(k)[1] != "ANY")
    cb = sorted(Bf.pclass(k) for k in Bf.rel_preds if Bf.pclass(k)[1] != "ANY")
    if not any(A.pclass(k)[1] == "ANY" for k in A.rel_preds) and not any(Bf.pclass(k)[1] == "ANY" for k in Bf.rel_preds) and ca != cb:
        return "polarity_multiset"
    return None


def _options(A: Formula, Bf: Formula, anchored: bool) -> tuple[list, list]:
    shared_p = {_lname(k) for k in A.rel_preds} & {_lname(k) for k in Bf.rel_preds}
    by_l = {_lname(k): k for k in Bf.rel_preds}
    popts = []
    for k in A.rel_preds:
        if anchored and _lname(k) in shared_p:
            popts.append((k, [by_l[_lname(k)]]))
            continue
        tg = [q for q in Bf.rel_preds if _compatible(A.pclass(k), Bf.pclass(q)) and not (anchored and _lname(q) in shared_p)]
        tg.sort(key=lambda q: (_lname(q) != _lname(k), q))
        popts.append((k, tg))
    shared_c = {c.lower() for c in A.rel_consts} & {c.lower() for c in Bf.rel_consts}
    cby = {c.lower(): c for c in Bf.rel_consts}
    copts = []
    for c in A.rel_consts:
        if anchored and c.lower() in shared_c:
            copts.append((c, [cby[c.lower()]]))
            continue
        tg = [d for d in Bf.rel_consts if not (anchored and d.lower() in shared_c)]
        tg.sort(key=lambda d: (d.lower() != c.lower(), d))
        copts.append((c, tg))
    popts.sort(key=lambda x: len(x[1]))
    copts.sort(key=lambda x: len(x[1]))
    return popts, copts


def _count(opts) -> float:
    n = 1.0
    for _, t in opts:
        n *= max(1, len(t))
    return n


def gg_map_search(fol_a: str, fol_b: str, max_maps: int = MAX_MAPS, max_secs: float = MAX_SECS, keep: int = KEEP) -> dict:
    """Exhaustive search of the PRIMARY map family for a -> b. Returns {'status': MAPPED | NO_MAP | PREFILTER:<reason> |
    CAPPED | UNPARSEABLE, 'maps': [{'pred': {a_key: b_key}, 'const': {a_c: b_c}, 'nonidentity': [...]}], 'n_maps',
    'n_fp_pass', 'n_z3_unknown', 'anchored', 'secs'}. Pairs in 'nonidentity' are (kind, a_symbol, b_symbol, a_use, b_use)."""
    t0 = time.time()
    try:
        A, Bf = analyse(fol_a), analyse(fol_b)
    except (ValueError, IndexError, TypeError, KeyError, RecursionError) as ex:
        return {"status": "UNPARSEABLE", "error": str(ex)[:120], "maps": [], "n_maps": 0, "secs": round(time.time() - t0, 3)}
    res = {"maps": [], "n_maps": 0, "n_fp_pass": 0, "n_z3_unknown": 0, "anchored": False, "capped": False}
    pf = prefilter(A, Bf)
    if pf:
        return {**res, "status": "PREFILTER:" + pf, "secs": round(time.time() - t0, 3)}
    popts, copts = _options(A, Bf, anchored=False)
    if _count(popts) * _count(copts) > max_maps:
        popts, copts = _options(A, Bf, anchored=True)
        res["anchored"] = True
    if any(not t for _, t in popts) or any(not t for _, t in copts):
        return {**res, "status": "NO_MAP", "secs": round(time.time() - t0, 3)}
    irrelevant = {k: "p__irr_" + k.split("/")[0] for k in A.ar if k not in A.rel_preds}
    irr_c = {c: "k__irr_" + c for c in A.consts if c not in A.rel_consts}

    def leaf(pm: dict, cm: dict) -> bool:
        res["n_maps"] += 1
        if res["n_maps"] > max_maps or (res["n_maps"] % 32 == 0 and time.time() - t0 > max_secs):
            res["capped"] = True
            return True
        pmap = {k: v.rsplit("/", 1)[0] for k, v in pm.items()}
        pmap.update(irrelevant)
        img = rename(A.e, pmap, {**cm, **irr_c})
        if first_mismatch(img, Bf.fp) is not None:
            return False
        res["n_fp_pass"] += 1
        r = z3_equiv(img, Bf.e)
        if r is None:
            res["n_z3_unknown"] += 1
        elif r is True:
            nonid = [("pred", k, v, atom_example(A.e, k), atom_example(Bf.e, v)) for k, v in sorted(pm.items()) if _lname(k) != _lname(v)]
            nonid += [("const", c, d, const_example(A.e, c), const_example(Bf.e, d)) for c, d in sorted(cm.items()) if c.lower() != d.lower()]
            res["maps"].append({"pred": dict(pm), "const": dict(cm), "nonidentity": nonid})
            if len(res["maps"]) >= keep:
                return True
        return time.time() - t0 > max_secs and _cap(res)

    def dfs_c(i: int, pm: dict, cm: dict, used: set) -> bool:
        if i == len(copts):
            return leaf(pm, cm)
        c, tg = copts[i]
        for d in tg:
            if d in used:
                continue
            if dfs_c(i + 1, pm, {**cm, c: d}, used | {d}):
                return True
        return False

    def dfs_p(i: int, pm: dict, used: set) -> bool:
        if i == len(popts):
            return dfs_c(0, pm, {}, set())
        k, tg = popts[i]
        for q in tg:
            if q in used:
                continue
            if dfs_p(i + 1, {**pm, k: q}, used | {q}):
                return True
        return False

    dfs_p(0, {}, set())
    status = "MAPPED" if res["maps"] else ("CAPPED" if res["capped"] else "NO_MAP")
    return {**res, "status": status, "secs": round(time.time() - t0, 3)}


def _cap(res) -> bool:
    res["capped"] = True
    return True


# ------------------------------------------------------------------------------------------------ gloss
PROMPT_GG_V1 = {
    "version": "gloss_gg_v1",
    "system": ("You judge whether two logic symbols used to formalise the SAME sentence can denote the same concept or relation "
               "with the same argument roles in that sentence. Different wording, synonyms, inflection and camelCase are fine; "
               "a broader/narrower, opposite, or different concept is NO; swapped argument roles is NO."),
    "user_template": ("Sentence: {sentence}\n\nEach numbered line shows symbol A and symbol B (name/arity, and one use of it in "
                      "its formula).\n{items}\n\nFor each line answer YES if A and B can denote the same concept or relation "
                      "(same argument roles) in this sentence, else NO. Return ONLY a JSON object mapping each line number to "
                      "\"YES\" or \"NO\", e.g. {{\"1\": \"YES\", \"2\": \"NO\"}}."),
    "item_template": "{n}. A = {a} (as used: {a_use}) | B = {b} (as used: {b_use})",
    "temperature": 0, "max_tokens": 200, "max_items_per_call": 12,
}


def symbol_label(kind: str, sym: str) -> str:
    return sym if kind == "pred" else f"{sym} (constant)"


def build_messages(prompt: dict, sentence: str, items: list[tuple]) -> list[dict]:
    """items: [(kind, a_sym, b_sym, a_use, b_use)] (<= max_items_per_call)."""
    lines = "\n".join(prompt["item_template"].format(n=i + 1, a=symbol_label(k, a), b=symbol_label(k, b), a_use=au, b_use=bu)
                      for i, (k, a, b, au, bu) in enumerate(items))
    return [{"role": "system", "content": prompt["system"]},
            {"role": "user", "content": prompt["user_template"].format(sentence=sentence, items=lines)}]


def parse_verdicts(txt: str | None, n: int) -> dict | None:
    """Strict: a JSON object with keys 1..n, each YES/NO; else None (the caller counts it as NO)."""
    if not txt:
        return None
    m = re.search(r"\{.*\}", txt, re.S)
    if not m:
        return None
    try:
        d = json.loads(m.group(0))
    except json.JSONDecodeError:
        return None
    out = {}
    for i in range(1, n + 1):
        v = str(d.get(str(i), "")).strip().upper()
        if v not in ("YES", "NO"):
            return None
        out[i] = v
    return out


def pair_key(item: tuple) -> tuple:
    """Symmetric cache key of one symbol pair (kind, {a, b} with arity)."""
    k, a, b = item[0], item[1], item[2]
    return (k,) + tuple(sorted((a, b)))


def gg_decision(search: dict, verdict: dict) -> tuple[bool, int | None]:
    """verdict[pair_key] = 'YES' / 'NO'. Agree iff some kept map has every non-identity pair YES (identity-only map ->
    agree). Returns (agree, index of the accepting map)."""
    for i, m in enumerate(search.get("maps", [])):
        if all(verdict.get(pair_key(it)) == "YES" for it in m["nonidentity"]):
            return True, i
    return False, None


def gg_agree(text: str, fol_a: str, fol_b: str, checker=None) -> dict:
    """Pairwise GG agreement. checker(sentence, items) -> {pair_key: 'YES'|'NO'}; None -> search-only brackets.
    Returns {'agree' (None if checker None and a non-identity map is needed), 'agree_allyes', 'agree_exact', 'search'}."""
    s = gg_map_search(fol_a, fol_b)
    exact = any(not m["nonidentity"] for m in s.get("maps", []))
    allyes = bool(s.get("maps"))
    if exact or not allyes:
        return {"agree": exact, "agree_allyes": allyes, "agree_exact": exact, "search": s}
    if checker is None:
        return {"agree": None, "agree_allyes": allyes, "agree_exact": exact, "search": s}
    items = sorted({pair_key(it): it for m in s["maps"] for it in m["nonidentity"]}.values())
    verdict = checker(text, items)
    ok, _ = gg_decision(s, verdict)
    return {"agree": ok, "agree_allyes": allyes, "agree_exact": exact, "search": s, "verdict": verdict}


def consensus_score_gg(text: str, fol: str, peers: list[str], checker=None, min_peers: int = 2) -> dict:
    """c_gg = 1 - share of peers agreeing under GG (higher = more likely error). peers = formulas of OTHER families for
    the same sentence. Unparseable candidate -> 1.0; < min_peers parseable peers -> None. Also returns the brackets
    c_gg_allyes (every mapped pair accepted) and c_exact (every non-identity pair rejected)."""
    try:
        analyse(fol)
    except (ValueError, IndexError, TypeError, KeyError, RecursionError):
        return {"c_gg": 1.0, "c_gg_allyes": 1.0, "c_exact": 1.0, "status": "UNPARSEABLE"}
    res = []
    for p in peers:
        try:
            analyse(p)
        except (ValueError, IndexError, TypeError, KeyError, RecursionError):
            continue
        res.append(gg_agree(text, fol, p, checker))
    if len(res) < min_peers:
        return {"c_gg": None, "c_gg_allyes": None, "c_exact": None, "status": "PEER_UNAVAILABLE", "n_peers": len(res)}
    n = len(res)
    return {"c_gg": (1 - sum(bool(r["agree"]) for r in res) / n) if all(r["agree"] is not None for r in res) else None,
            "c_gg_allyes": 1 - sum(r["agree_allyes"] for r in res) / n, "c_exact": 1 - sum(r["agree_exact"] for r in res) / n,
            "status": "OK", "n_peers": n}
