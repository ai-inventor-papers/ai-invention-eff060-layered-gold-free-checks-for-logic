"""csc_lib: Candidate-Signature Consensus (CSC) for gold-free NL->FOL faithfulness (iteration 4, T6-P).

WHAT CSC MEASURES. Peers from k = 3 other model families translate the SAME sentence after being shown the
CANDIDATE's own symbol list (predicate and constant names with arities, shuffled deterministically). A peer agrees
when its formula is z3-equivalent to the candidate with NO aligner: symbol names are matched case-insensitively
(key = (lower(name), arity)) and nothing else. Because the peers are cued with the candidate's vocabulary, the
rename/vocabulary problem of free consensus disappears by construction: an equivalent translation in the same
vocabulary is exact-equivalent. The price is ANCHORING: a peer may copy a wrong symbol from the list (a foreign
conjunct, a wrong-meaning predicate) and thereby endorse an error. This library measures both sides.

Orientation everywhere: HIGHER score = MORE LIKELY ERROR.

  c_csc        = 1 - (#peers exact-equivalent to the candidate) / (#peers with a parseable formula).
                 z3 UNKNOWN (2 s timeout) counts as NOT equivalent and is recorded in n_unknown.
                 < 2 parseable peers -> 0.5 with status 'csc_insufficient_peers'.
                 Unparseable candidate -> 1.0 with status 'UNPARSEABLE' (coverage view; never silently dropped).
  c_csc_multi  = the same, but peer p also endorses when its SECOND reading (alt_fol) is equivalent to the candidate
                 AND another peer q != p produced that reading too (fol or alt) - a corroborated alternative reading.
  c_csc_graded = exp-5 / exp-8 peer_text.graded_consensus over claim units with the IDENTITY symbol map
                 (1 - F1(support, coverage)); unit entailment by the finite-model refuter then z3.
Blind spots (stated): errors every cued peer copies from the list (anchoring; measured on PERTURB ADD_FOREIGN /
MEANING_RENAME); errors shared by the peers independently of the cue; readings no peer produces.
Cost: k API calls per unique (sentence, signature); z3 CPU seconds per candidate (MARGINAL cost).
"""
from __future__ import annotations

import hashlib
import itertools
import json
import random
import re
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
V8 = SRC / "vendor_x8"
if str(V8) not in sys.path:
    sys.path.insert(0, str(V8))
import peer_text as PT  # noqa: E402  (installs the dataset-E parser as module 'fol'; adds vendor_c / vendor_a)
import fol as EFOL  # noqa: E402  (== vendor_e.fol, the dataset-E parser)
sys.path.insert(0, str(V8 / "vendor_c"))
import repair_census as RC  # noqa: E402  (vendor_c: atoms, symbols, fp, edits, search)

PROMPT_PATH = ROOT / "data" / "prompts" / "fewshot_v1.txt"
PEERS = [("deepseek/deepseek-v3.2", "deepseek", {"reasoning": {"enabled": False}}),
         ("microsoft/phi-4", "microsoft", {}),
         ("openai/gpt-4.1-mini", "openai", {}),
         ("qwen/qwen3-235b-a22b-2507", "qwen", {})]
PEER_MODELS = [p[0] for p in PEERS]
PEER_FAMILY = {p[0]: p[1] for p in PEERS}
PEER_EXTRA = {p[0]: p[2] for p in PEERS}
BLOCK_TEMPLATE = ("Symbols from another translation of this sentence (name/arity, random order): {items}. "
                  "Use a listed symbol wherever its name fits what the sentence says, and keep its arity. "
                  "If part of the sentence is not covered by any listed symbol, introduce a new symbol. "
                  "You need not use every listed symbol. The list is not a translation: translate the sentence "
                  "itself. Return JSON {{\"fol\": <formula>, \"alt_fol\": <a formula for a second legitimate "
                  "reading, or null>}}.")
V1B_PREFIX = "For this sentence, a symbol list IS given: "
Z3_MS = 2000


def block_template_sha256() -> str:
    return hashlib.sha256(BLOCK_TEMPLATE.encode()).hexdigest()


# ============================================================================================ parse / signature
def parse(s: str | None):
    """Dataset-E parser -> AST or None (unparseable)."""
    return PT.parse_fol(s)


def _bound(e, acc=None):
    return RC.bound_vars(e, acc)


def extract_signature_ast(e) -> list[tuple[str, int]]:
    """Symbols of a parsed formula: predicates (name, arity >= 0 for propositional atoms) and constants (name, 0);
    bound variables excluded. Sorted by (lower(name), arity, name); one entry per lowercase key (first spelling wins)."""
    P, C = RC.symbols(e)
    items = sorted(set(P) | {(c, 0) for c in C}, key=lambda t: (t[0].lower(), t[1], t[0]))
    out, seen = [], set()
    for n, a in items:
        k = (n.lower(), a)
        if k not in seen:
            seen.add(k)
            out.append((n, a))
    return out


def extract_signature(fol: str) -> list[tuple[str, int]]:
    """(name, arity) list of the formula's predicates and constants (arity 0), variables excluded; [] if unparseable."""
    e = parse(fol)
    return [] if e is None else extract_signature_ast(e)


def sig_lower(sig) -> list[tuple[str, int]]:
    return sorted({(n.lower(), a) for n, a in sig})


def sig_string(sig) -> str:
    return "|".join(f"{n}/{a}" for n, a in sig_lower(sig))


def sig_key(sig) -> str:
    return hashlib.sha1(sig_string(sig).encode()).hexdigest()[:16]


# ============================================================================================ prompt
_PROMPT_CACHE: dict = {}


def _prompt() -> dict:
    if "p" not in _PROMPT_CACHE:
        _PROMPT_CACHE["p"] = json.loads(PROMPT_PATH.read_text())
    return _PROMPT_CACHE["p"]


def symbols_block(text: str, sig, variant: str = "v1") -> str:
    """The appended CSC block; the list order is a deterministic shuffle seeded by sha1(text | canonical signature)."""
    items = [f"{n}/{a}" for n, a in sorted(sig, key=lambda t: (t[0].lower(), t[1], t[0]))]
    rng = random.Random(int(hashlib.sha1((text + "|" + sig_string(sig)).encode()).hexdigest(), 16))
    rng.shuffle(items)
    b = BLOCK_TEMPLATE.format(items=", ".join(items))
    return (V1B_PREFIX + b) if variant == "v1b" else b


def csc_prompt(text: str, signature, variant: str = "v1") -> list[dict]:
    """Messages: the byte-identical dataset-E few-shot prompt (system + 6 exemplars) + the user turn
    'Sentence: <text>' followed by a blank line and the symbols block."""
    pr = _prompt()
    user = pr["user_template"].replace("{sentence}", text) + "\n\n" + symbols_block(text, signature, variant)
    return [{"role": "system", "content": pr["system"]}] + list(pr["exemplars"]) + [{"role": "user", "content": user}]


def free_prompt(text: str) -> list[dict]:
    pr = _prompt()
    return [{"role": "system", "content": pr["system"]}] + list(pr["exemplars"]) + \
        [{"role": "user", "content": pr["user_template"].replace("{sentence}", text)}]


# ============================================================================================ peer output parsing
_FENCE = re.compile(r"```(?:json)?", re.I)


def _clean_formula(s):
    if s is None:
        return None
    if not isinstance(s, str):
        return None
    s = s.strip()
    if s.lower() in ("", "null", "none", "n/a"):
        return None
    if s.startswith("FOL:"):
        s = s[4:].strip()
    return s


def parse_peer(raw: str | None) -> dict:
    """Peer raw output -> {'fol', 'alt_fol', 'format' in {json, fol_line, bare, fail}}.
    (1) first JSON object (```json fences tolerated) with a string 'fol'; (2) a 'FOL:' line (alt = None);
    (3) the whole output if it is a single line that parses as a formula ('bare'); else fail."""
    s = (raw or "").strip()
    if not s:
        return {"fol": None, "alt_fol": None, "format": "fail"}
    t = _FENCE.sub("", s)
    dec = json.JSONDecoder()
    for m in re.finditer(r"\{", t):
        try:
            obj, _ = dec.raw_decode(t[m.start():])
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and isinstance(obj.get("fol"), str) and obj.get("fol").strip():
            return {"fol": _clean_formula(obj.get("fol")), "alt_fol": _clean_formula(obj.get("alt_fol")), "format": "json"}
    for line in s.splitlines():
        if line.strip().startswith("FOL:"):
            return {"fol": line.split("FOL:", 1)[1].strip() or None, "alt_fol": None, "format": "fol_line"}
    lines = [x for x in t.splitlines() if x.strip()]
    if len(lines) == 1 and parse(lines[0].strip()) is not None:
        return {"fol": lines[0].strip(), "alt_fol": None, "format": "bare"}
    return {"fol": None, "alt_fol": None, "format": "fail"}


# ============================================================================================ exact equivalence
def lower_ast(e, bv=frozenset()):
    """Lower-case every predicate and constant name (bound variables untouched)."""
    k = e[0]
    if k == "atom":
        return ("atom", e[1].lower(), tuple(x if x in bv else x.lower() for x in e[2]))
    if k in ("all", "ex"):
        return (k, e[1], lower_ast(e[2], bv | {e[1]}))
    if k == "not":
        return ("not", lower_ast(e[1], bv))
    return (k, lower_ast(e[1], bv), lower_ast(e[2], bv))


def prep(s: str | None):
    """Parse + lowercase -> (ast, canonical string, fingerprint) or None."""
    e = parse(s)
    if e is None:
        return None
    el = lower_ast(e)
    try:
        f = RC.fp(el)
    except RecursionError:
        f = None
    return el, PT.canon(el), f


def eq_prepped(a, b, ms: int = Z3_MS):
    """a, b from prep(). True / False / None (UNKNOWN). Canonical-string identity -> True; different random-model
    fingerprints -> False (sound: they differ on a finite model); else z3 with `ms` timeout."""
    if a is None or b is None:
        return None
    if a[1] == b[1]:
        return True
    if a[2] is not None and b[2] is not None and a[2] != b[2]:
        return False
    try:
        return EFOL.equivalent(a[0], b[0], ms=ms)
    except (Exception,):  # noqa: BLE001 - z3 exceptions / recursion on huge formulas -> UNKNOWN (counted)
        return None


def eq_exact(fa: str, fb: str, ms: int = Z3_MS):
    """Exact (no aligner) case-insensitive z3 equivalence of two formula strings: True / False / None (UNKNOWN or
    unparseable)."""
    return eq_prepped(prep(fa), prep(fb), ms)


# ============================================================================================ scores
def consensus_score(text: str, fol: str, peers: list[dict | str], mode: str = "csc", ms: int = Z3_MS,
                    _prepped: dict | None = None) -> dict:
    """Binary CSC. peers: formula strings or dicts with 'fol'. Returns {'c', 'per_peer', 'n_used', 'n_unknown',
    'n_unparseable_peers', 'status'} with c = 1 - agree/used (higher = more likely error)."""
    assert mode == "csc", mode
    pp = _prepped if _prepped is not None else {}
    cand = pp.get(fol) if fol in pp else prep(fol)
    fols = [p.get("fol") if isinstance(p, dict) else p for p in peers]
    usable = []
    n_bad = 0
    for f in fols:
        x = pp.get(f) if f in pp else prep(f)
        if x is None:
            n_bad += 1
        else:
            usable.append(x)
    if cand is None:
        return {"c": 1.0, "per_peer": [], "n_used": len(usable), "n_unknown": 0, "n_unparseable_peers": n_bad,
                "status": "UNPARSEABLE"}
    if len(usable) < 2:
        return {"c": 0.5, "per_peer": [], "n_used": len(usable), "n_unknown": 0, "n_unparseable_peers": n_bad,
                "status": "csc_insufficient_peers"}
    verd = [eq_prepped(cand, x, ms) for x in usable]
    n_true = sum(v is True for v in verd)
    return {"c": 1 - n_true / len(usable), "per_peer": verd, "n_used": len(usable),
            "n_unknown": sum(v is None for v in verd), "n_unparseable_peers": n_bad, "status": "OK"}


def csc_multi_score(text: str, fol: str, peer_records: list[dict], ms: int = Z3_MS) -> dict:
    """Multi-reading CSC. Peer p endorses iff eq(cand, p.fol) OR (p.alt parseable AND eq(cand, p.alt) AND some other
    peer q != p has eq(p.alt, q.fol) or eq(p.alt, q.alt)). Denominator = peers with a parseable fol."""
    cand = prep(fol)
    P = []
    for r in peer_records:
        f = prep(r.get("fol"))
        if f is None:
            continue
        P.append((f, prep(r.get("alt_fol")) if r.get("alt_fol") else None))
    if cand is None:
        return {"c": 1.0, "status": "UNPARSEABLE", "n_used": len(P), "n_alt_endorse": 0}
    if len(P) < 2:
        return {"c": 0.5, "status": "csc_insufficient_peers", "n_used": len(P), "n_alt_endorse": 0}
    endorse, n_alt = 0, 0
    for i, (f, alt) in enumerate(P):
        if eq_prepped(cand, f, ms) is True:
            endorse += 1
            continue
        if alt is not None and eq_prepped(cand, alt, ms) is True:
            ok = False
            for j, (g, galt) in enumerate(P):
                if j == i:
                    continue
                if eq_prepped(alt, g, ms) is True or (galt is not None and eq_prepped(alt, galt, ms) is True):
                    ok = True
                    break
            if ok:
                endorse += 1
                n_alt += 1
    return {"c": 1 - endorse / len(P), "status": "OK", "n_used": len(P), "n_alt_endorse": n_alt}


def _identity_pair(a_s: str, b_s: str, ent, eqv) -> dict:
    """pairs.py-format record with the IDENTITY map: fwd = [b ⊨ unit of a], bwd = [a ⊨ unit of b]."""
    au = PT.units_of(a_s)[0]
    bu = PT.units_of(b_s)[0]
    if a_s == b_s:
        return {"fwd": [True] * len(au), "bwd": [True] * len(bu), "peer_r": b_s, "peer_units_r": list(bu),
                "equiv": True, "cost": 0.0, "n_maps": 0, "rank": 0}
    return {"fwd": [ent(b_s, u) for u in au], "bwd": [ent(a_s, v) for v in bu], "peer_r": b_s,
            "peer_units_r": list(bu), "equiv": eqv, "cost": 0.0, "n_maps": 1, "rank": 0}


_ENT = {}


def _entailer(ms: int = Z3_MS):
    if ms not in _ENT:
        _ENT[ms] = PT.Entailer(ms)
    return _ENT[ms]


def graded_consensus(text: str, fol: str, peers: list[dict | str], mode: str = "csc", ms: int = Z3_MS) -> dict:
    """Graded CSC: exp-8 peer_text.graded_consensus with the identity symbol map on lower-cased canonical formulas.
    g = 1 - F1(support, coverage) (higher = more likely error); support = share of candidate claim units entailed by
    the peers; coverage = share of the peers' majority units the candidate entails."""
    assert mode == "csc", mode
    cand = prep(fol)
    fols = [p.get("fol") if isinstance(p, dict) else p for p in peers]
    ps = [x for x in (prep(f) for f in fols) if x is not None]
    if cand is None:
        return {"g": 1.0, "status": "UNPARSEABLE"}
    if len(ps) < 2:
        return {"g": 0.5, "status": "csc_insufficient_peers"}
    ent = _entailer(ms)
    cs = cand[1]
    pool = [p[1] for p in ps]
    by = {cs: cand}
    for p in ps:
        by[p[1]] = p
    table = {}
    for a in sorted(set([cs] + pool)):
        for b in pool:
            if a == b or (a, b) in table:
                continue
            table[(a, b)] = _identity_pair(a, b, ent, eq_prepped(by[a], by[b], ms))
    try:
        g = PT.graded_consensus(cs, pool, table, ent, return_codes=True)
    except (RecursionError, KeyError, ValueError) as ex:
        return {"g": None, "status": f"GRADED_FAIL:{type(ex).__name__}"}
    return {"g": g["g_score"], "support": g.get("support"), "coverage": g.get("coverage"),
            "unit_codes": [c["code"] for c in g.get("unit_codes", [])], "status": "OK"}


def peer_majority(peers: list[dict | str], ms: int = Z3_MS) -> dict:
    """Exact-equivalence classes among parseable peers (given in P order). Majority = a class with >= 2 members;
    a 2-2 tie (k = 4) is broken by the earliest P member. Returns {'formula' (the earliest member's fol) | None,
    'status' in {MAJORITY, NO_MAJORITY, INSUFFICIENT}, 'class_sizes'}."""
    fols = [p.get("fol") if isinstance(p, dict) else p for p in peers]
    items = [(i, f, prep(f)) for i, f in enumerate(fols)]
    items = [t for t in items if t[2] is not None]
    if len(items) < 2:
        return {"formula": None, "status": "INSUFFICIENT", "class_sizes": [len(items)] if items else []}
    classes: list[list] = []
    for t in items:
        for c in classes:
            if eq_prepped(c[0][2], t[2], ms) is True:
                c.append(t)
                break
        else:
            classes.append([t])
    best = sorted(classes, key=lambda c: (-len(c), c[0][0]))[0]
    sizes = sorted((len(c) for c in classes), reverse=True)
    if len(best) >= 2:
        return {"formula": best[0][1], "status": "MAJORITY", "class_sizes": sizes, "n_classes": len(classes)}
    return {"formula": None, "status": "NO_MAJORITY", "class_sizes": sizes, "n_classes": len(classes)}


def symbol_usage(sig, peer_fols: list[str | None]) -> list[list[bool]]:
    """For each listed symbol s (in `sig` order) and each parseable peer: used = (lower(name), arity) of s occurs among
    the peer's predicates/constants. Returns [[used for peer in parseable peers] for s in sig]."""
    psyms = []
    for f in peer_fols:
        e = parse(f)
        if e is None:
            continue
        psyms.append(set(sig_lower(extract_signature_ast(e))))
    return [[(n.lower(), a) in ps for ps in psyms] for n, a in sig]


# ============================================================================================ same-vocab typed repair
def _subst(e, a: tuple, b: str):
    k = e[0]
    if k == "atom":
        return ("atom", b, e[2]) if (e[1], len(e[2])) == a else e
    if k in ("all", "ex"):
        return (k, e[1], _subst(e[2], a, b))
    if k == "not":
        return ("not", _subst(e[1], a, b))
    return (k, _subst(e[1], a, b), _subst(e[2], a, b))


def edits_ext(e, target):
    """repair_census.edits + SUBST (replace every occurrence of predicate a (absent from the target) by a target
    predicate b of the same arity (absent from e)) + ADD_ANY (conjoin ANY target atom whose predicate already occurs
    in e, or any NEGATED target literal, re-binding foreign variables to in-scope ones exactly like ADD)."""
    yield from RC.edits(e, target)
    Pe, _ = RC.symbols(e)
    Pt, Ct = RC.symbols(target)
    for a in sorted(Pe - Pt):
        for b in sorted(Pt - Pe):
            if a[1] == b[1]:
                yield "SUBST", _subst(e, a, b[0])
    # literals to add: positive target atoms whose predicate already occurs in e (new-predicate positives are ADD's),
    # plus every NEGATED target literal (extension: a dropped '¬P(x)' condition is otherwise unreachable at depth 1)
    lits, seen = [], set()
    for at in RC.atoms(target):
        if (at[1], len(at[2])) in Pe and (False, at) not in seen:
            seen.add((False, at))
            lits.append((False, at))
    for _p, nd, _s in RC.subterms(target):
        if nd[0] == "not" and nd[1][0] == "atom" and (True, nd[1]) not in seen:
            seen.add((True, nd[1]))
            lits.append((True, nd[1]))
    for path, node, scope in list(RC.subterms(e)):
        for neg, at in lits:
            sc = list(scope)
            opts = [[x] if (x in Ct or x in sc) else (sc or [x]) for x in at[2]]
            for combo in itertools.islice(itertools.product(*opts), 6):
                lit = ("atom", at[1], tuple(combo))
                yield "ADD_ANY", RC.replace(e, path, ("and", node, ("not", lit) if neg else lit))


def _search_ext(ao, target, budget_s: float, max_d2: int = 6000):
    import time
    ft = RC.fp(target)
    t0 = time.time()
    lvl1, seen = [], set()
    for lab, c in edits_ext(ao, target):
        s = str(c)
        if s in seen:
            continue
        seen.add(s)
        lvl1.append((lab, c))
        if RC.fp(c) == ft and EFOL.equivalent(c, target, ms=1500) is True:
            return [lab], time.time() - t0, False
        if time.time() - t0 > budget_s:
            return None, time.time() - t0, True
    n = 0
    for lab1, c1 in lvl1:
        for lab2, c2 in edits_ext(c1, target):
            n += 1
            if lab1 == "NEG" and lab2 == "NEG":
                continue
            if n > max_d2 * 10 or time.time() - t0 > budget_s:
                return None, time.time() - t0, True
            if RC.fp(c2) == ft and EFOL.equivalent(c2, target, ms=1500) is True:
                return sorted([lab1, lab2]), time.time() - t0, False
    return None, time.time() - t0, False


def typed_repair_same_vocab(fol: str, target: str, budget_s: float = 6.0) -> dict:
    """Smallest typed edit sequence (depth <= 2) turning `fol` into a formula exact-equivalent (lower-cased, same
    vocabulary, NO align/gran bridge) to `target`. Operators: NEG REV QUANT RESTR CONN MOVE DROP ADD SWAP BIND SCOPE
    UNGLUE (repair_census) + SUBST + ADD_ANY. The ops repair `fol` TOWARDS `target` (an extra conjunct in `fol` is
    repaired by DROP). Returns {'cls': EQUIV | '<OP>[+<OP>]' | NO_REPAIR | TIMEOUT | PARSE_FAIL | ERROR, 'ops', 'secs'}."""
    import time
    t0 = time.time()
    a, b = prep(fol), prep(target)
    if a is None or b is None:
        return {"cls": "PARSE_FAIL", "ops": [], "secs": 0.0}
    try:
        if eq_prepped(a, b) is True:
            return {"cls": "EQUIV", "ops": [], "secs": round(time.time() - t0, 3)}
        ops, dt, timed_out = _search_ext(a[0], b[0], budget_s)
        if ops:
            return {"cls": "+".join(ops), "ops": ops, "secs": round(time.time() - t0, 3)}
        return {"cls": "TIMEOUT" if timed_out else "NO_REPAIR", "ops": [], "secs": round(time.time() - t0, 3)}
    except (RecursionError, ValueError, KeyError, IndexError, TypeError) as ex:
        return {"cls": "ERROR", "ops": [], "err": f"{type(ex).__name__}: {str(ex)[:80]}", "secs": round(time.time() - t0, 3)}


# ============================================================================================ peers (API)
def peer_assignment(candidate_family: str | None) -> dict:
    """K3 = the first 3 members of P whose family != candidate_family; K4 = all of P only if candidate_family is not
    a P family (else None). PERTURB rows (no generator family) -> K3 = deepseek, microsoft, openai; K4 adds qwen."""
    k3 = [m for m in PEER_MODELS if PEER_FAMILY[m] != candidate_family][:3]
    k4 = list(PEER_MODELS) if candidate_family not in set(PEER_FAMILY.values()) else None
    return {"k3": k3, "k4": k4}


def csc_peers(text: str, signature, families: list[str] | None = None, k: int = 3, candidate_family: str | None = None,
              client=None, dry_run: bool = True, variant: str = "v1") -> dict:
    """Generate CSC peers for (text, signature). dry_run=True -> {'models', 'estimate_usd', 'messages'} (no call).
    Otherwise runs the async OpenRouter client (src/llm.py; cached, budget-checked) and returns
    {'peers': [{model, family, raw, fol, alt_fol, format, parse_ok, cost}], 'cost_usd'}."""
    asg = peer_assignment(candidate_family)
    models = families or (asg["k3"] if k == 3 else (asg["k4"] or asg["k3"]))
    msgs = csc_prompt(text, signature, variant)
    est = {"deepseek/deepseek-v3.2": 3.2e-4, "microsoft/phi-4": 1.1e-4, "openai/gpt-4.1-mini": 5.6e-4,
           "qwen/qwen3-235b-a22b-2507": 1.6e-4}
    if dry_run:
        return {"models": models, "estimate_usd": sum(est.get(m, 5e-4) for m in models), "messages": msgs}
    import asyncio
    import aiohttp
    import or_client as llm

    async def run():
        cl = client or llm.Client(stage="csc_peers_lib")
        async with aiohttp.ClientSession() as s:
            return await asyncio.gather(*[cl.chat(s, m, msgs, PEER_EXTRA[m]) for m in models])
    recs = asyncio.run(run())
    out, tot = [], 0.0
    for m, r in zip(models, recs):
        pr = parse_peer(r.get("content"))
        out.append({"model": m, "family": PEER_FAMILY[m], "raw": r.get("content"), **pr,
                    "parse_ok": prep(pr["fol"]) is not None, "cost": 0.0 if r.get("cache_hit") else r.get("cost_usd", 0.0)})
        tot += out[-1]["cost"] or 0.0
    return {"peers": out, "cost_usd": tot}
