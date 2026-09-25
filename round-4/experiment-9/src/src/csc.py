"""csc: Candidate-Signature Consensus (CSC) -- a gold-free error score for an NL->FOL candidate (iteration 4, T6-E).

WHAT c_csc MEASURES (precisely). Given a sentence x.text and a candidate formula x.fol, CSC asks k (=3) cheap peer LLMs
from families other than the candidate's own to translate x.text with the dataset-E few-shot prompt PLUS one block that
lists the candidate's own predicate/constant symbols (name/arity, seeded random order). It then checks, per peer, whether
the peer's formula is z3-equivalent to the candidate with symbols identified by LOWERCASED NAME AND ARITY ONLY (no
aligner, no synonym or granularity bridge).
    c_csc(x) = 1 - (share of parseable family-disjoint peers whose formula is z3-equivalent to x.fol)
It estimates how far the candidate sits from what independent models write for the same sentence in the SAME
vocabulary. Orientation: HIGHER = MORE LIKELY ERROR. It does NOT measure truth against a reference: an error that the
peers reproduce (anchoring on a listed symbol, or a bias shared by the peers) scores as faithful; a legitimate second
reading that no peer picks scores as an error.

Variants (one API call per peer gives all three):
  c_csc        exact-equivalence share (above).
  c_csc_graded 1 - F1(support, coverage) over claim units (exp 5 peer_text.graded_consensus) with the IDENTITY map
               (same vocabulary, no alignment).
  c_csc_multi  peer p endorses x if x == p.fol, OR x == p.alt_fol when that alternative reading is also produced
               (as fol or alt_fol) by at least one other peer.
Failure conventions (never silent): unparseable candidate -> score 1.0 (COVERAGE view only), status UNPARSEABLE;
unparseable peers are dropped from the denominator and counted; fewer than 2 usable peers -> 0.5 with status
csc_insufficient_peers; z3 UNKNOWN (2 s timeout) counts as NOT equivalent and is counted in n_unknown.
Cost: 3 peer calls per unique (text, signature) (~$3e-4 each on the pool below) + z3 CPU (~0.01-2 s per pair).
"""
from __future__ import annotations

import hashlib
import json
import os
import random
import re
import signal
import sys
import time
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
VENDOR = ROOT / "vendor" / "e8src"
os.environ.setdefault("NLTK_DATA", "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/"
                                   "gen_art_experiment_8/data/nltk_data")
for _p in (str(VENDOR),):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import peer_text as PT  # noqa: E402  (installs the dataset-E parser as module 'fol'; adds vendor_c / vendor_a to sys.path)
import vendor_e.fol as EFOL  # noqa: E402
import repair_census as RC  # noqa: E402  (vendor_c: symbols, fp, search)

sys.setrecursionlimit(20000)
PROMPT_PATH = ROOT / "vendor" / "data" / "prompts" / "fewshot_v1.txt"
B_SIG = ("Symbols from another translation of this sentence (name/arity, random order): {sig}. Use a listed symbol "
         "wherever its name fits what the sentence says, and keep its arity. If part of the sentence is not covered by "
         "any listed symbol, introduce a new symbol. You need not use every listed symbol. The list is not a translation: "
         "translate the sentence itself. Return JSON {{\"fol\": <formula>, \"alt_fol\": <a formula for a second "
         "legitimate reading, or null>}}.")
# FORMAT-ONLY control: the same output instruction, no symbol list (isolates the signature from the format change)
B_FMT = ("Translate the sentence itself. Return JSON {\"fol\": <formula>, \"alt_fol\": <a formula for a second "
         "legitimate reading, or null>}.")
POOL = [("deepseek/deepseek-v3.2", "deepseek", {"reasoning": {"enabled": False}}),
        ("microsoft/phi-4", "microsoft", {}),
        ("openai/gpt-4.1-mini", "openai", {}),
        ("qwen/qwen3-235b-a22b-2507", "qwen", {})]
FAMILY_RULES = [("gpt-", "openai"), ("openai/", "openai"), ("malls_gpt4", "openai"), ("llama", "meta"), ("qwen", "qwen"),
                ("mistral", "mistral"), ("deepseek", "deepseek"), ("gemma", "google"), ("gemini", "google"),
                ("phi", "microsoft"), ("command", "cohere"), ("cohere", "cohere"), ("ccg2lambda", "symbolic")]


# =================================================================================================== families / peers
def family_of(system: str) -> str:
    """Vendor family of an E system string (gpt-* -> openai, llama -> meta, gemma/gemini -> google, ...)."""
    s = system.lower()
    for key, fam in FAMILY_RULES:
        if key in s:
            return fam
    return "other:" + s


def peers_for(cand_family: str, k: int = 3) -> list[tuple[str, str, dict]]:
    """First k members of POOL whose family differs from the candidate's (family-disjoint; never the candidate's own)."""
    return [m for m in POOL if m[1] != cand_family][:k]


# =================================================================================================== parsing / signature
def parse(s: str | None):
    return PT.parse_fol(s)


def extract_signature(fol: str | None) -> list[tuple[str, int, str]] | None:
    """Predicate symbols with arity plus constants (arity 0) of `fol`, read by the dataset-E parser.
    Returns a sorted list of (lowercased name, arity, original-casing name) -- one entry per (lowercased name, arity),
    the first original casing in sorted order kept -- or None if unparseable. Variables, connectives and quantifiers are
    excluded; an argument that is not bound by a quantifier is a constant (E-parser convention)."""
    e = parse(fol)
    if e is None:
        return None
    P, C = RC.symbols(e)
    out = {}
    for name, ar in sorted(P):
        out.setdefault((name.lower(), ar), name)
    for c in sorted(C):
        out.setdefault((c.lower(), 0), c)
    return sorted((k[0], k[1], v) for k, v in out.items())


def canonical_sig(sig: list) -> str:
    return ",".join(f"{n}/{a}" for n, a, _ in sorted(sig))


def order_symbols(text: str, sig: list) -> list[str]:
    """'Name/arity' strings in the candidate's original casing, shuffled by
    random.Random(int(sha1(text + '|' + canonical_sorted_sig), 16)) -> same (text, signature) = same prompt bytes."""
    items = [f"{orig}/{a}" for _, a, orig in sorted(sig)]
    rng = random.Random(int(hashlib.sha1((text + "|" + canonical_sig(sig)).encode()).hexdigest(), 16))
    rng.shuffle(items)
    return items


def load_prompt() -> dict:
    return json.loads(PROMPT_PATH.read_text())


def build_prompt(text: str, sig_list: list[str] | None, fmt_only: bool = False) -> list[dict]:
    """dataset-E fewshot_v1 messages byte-identical + one appended block in the final user message.
    sig_list=None and fmt_only=True -> FORMAT-ONLY control block (no symbols)."""
    pr = load_prompt()
    user = pr["user_template"].format(sentence=text)
    if fmt_only:
        user += "\n\n" + B_FMT
    else:
        user += "\n\n" + B_SIG.format(sig=", ".join(sig_list or []))
    return [{"role": "system", "content": pr["system"]}] + pr["exemplars"] + [{"role": "user", "content": user}]


def prompt_key(model: str, messages: list[dict]) -> str:
    return hashlib.sha1((model + "|" + json.dumps(messages, ensure_ascii=False, sort_keys=True)).encode()).hexdigest()


_FORMULA_CH = re.compile(r"[∀∃¬∧∨→↔⊕]|\w+\(")


def parse_response(raw: str | None) -> dict:
    """Peer JSON {fol, alt_fol} -> dict with 'route'. Routes: json | json_fenced | json_regex | fol_line | formula_line | none."""
    s = (raw or "").strip()
    if not s:
        return {"fol": None, "alt_fol": None, "route": "none"}
    cand = [("json", s)]
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", s, re.S)
    if m:
        cand.append(("json_fenced", m.group(1)))
    m = re.search(r"\{.*\}", s, re.S)
    if m:
        cand.append(("json_regex", m.group(0)))
    for route, t in cand:
        try:
            d = json.loads(t)
        except (json.JSONDecodeError, ValueError):
            continue
        if isinstance(d, dict) and "fol" in d:
            f = d.get("fol")
            a = d.get("alt_fol")
            f = f.strip() if isinstance(f, str) and f.strip() else None
            a = a.strip() if isinstance(a, str) and a.strip() and a.strip().lower() not in ("null", "none") else None
            return {"fol": f, "alt_fol": a, "route": route}
    for line in s.splitlines():  # few-shot format leakage 'FOL: ...'
        if line.strip().startswith("FOL:"):
            return {"fol": line.split("FOL:", 1)[1].strip(), "alt_fol": None, "route": "fol_line"}
    for line in s.splitlines():
        if _FORMULA_CH.search(line) and not line.strip().startswith("{"):
            return {"fol": line.strip().strip("`"), "alt_fol": None, "route": "formula_line"}
    return {"fol": None, "alt_fol": None, "route": "none"}


# =================================================================================================== same-vocabulary equivalence
def _norm(e, bound=frozenset()):
    """Case-normalise symbols: predicate names -> lowercase; constants -> 'k_' + lowercase (cannot capture a bound
    variable). Arity stays part of a predicate's identity (z3 keys 'name/arity')."""
    k = e[0]
    if k == "atom":
        return ("atom", e[1].lower(), tuple(a if a in bound else "k_" + a.lower() for a in e[2]))
    if k in ("all", "ex"):
        return (k, e[1], _norm(e[2], bound | {e[1]}))
    if k == "not":
        return ("not", _norm(e[1], bound))
    return (k, _norm(e[1], bound), _norm(e[2], bound))


def norm_canon(fol: str | None) -> str | None:
    """Canonical (alpha-normalised, case-normalised) string of a formula, or None if unparseable."""
    e = parse(fol)
    return None if e is None else PT.canon(_norm(e))


class _TO(Exception):
    pass


def _alarm(signum, frame):  # noqa: ARG001
    raise _TO()


def exact_equiv(a: str | None, b: str | None, timeout_ms: int = 2000, cap_s: int = 20) -> bool | None:
    """z3 equivalence with symbols identified by (lowercased name, arity); union vocabulary as uninterpreted symbols.
    Unlike consensus_lib 'exact' this does NOT require identical signatures (a formula using a symbol the other lacks
    is equivalent only if that symbol is logically idle). True / False / None (UNKNOWN: z3 timeout or cap)."""
    ca, cb = norm_canon(a), norm_canon(b)
    if ca is None or cb is None:
        return None
    return _eq_canon(ca, cb, timeout_ms, cap_s)


_EQ_CACHE: dict = {}


def _eq_canon(ca: str, cb: str, timeout_ms: int = 2000, cap_s: int = 20) -> bool | None:
    if ca == cb:
        return True
    key = (ca, cb) if ca < cb else (cb, ca)
    if key in _EQ_CACHE:
        return _EQ_CACHE[key]
    ea, eb = EFOL.parse(ca), EFOL.parse(cb)
    use_alarm = hasattr(signal, "SIGALRM")
    try:
        if use_alarm:
            old = signal.signal(signal.SIGALRM, _alarm)
            signal.alarm(cap_s)
        try:
            if RC.fp(ea) != RC.fp(eb):  # sound necessary condition (random finite models)
                r = False
            else:
                r = EFOL.equivalent(ea, eb, ms=timeout_ms)
        finally:
            if use_alarm:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old)
    except (_TO, RecursionError, Exception):  # noqa: BLE001 - z3 exceptions / pathological formulas -> UNKNOWN (counted)
        r = None
    if len(_EQ_CACHE) > 200000:
        _EQ_CACHE.clear()
    _EQ_CACHE[key] = r
    return r


# =================================================================================================== consensus scores
def _identity_pair(cand_s: str, peer_s: str, ent) -> dict:
    """pair_result record for graded_consensus with the IDENTITY vocabulary map (strings already case-normalised)."""
    cu_s = PT.units_of(cand_s)[0]
    pu_s = PT.units_of(peer_s)[0]
    fwd = [ent(peer_s, u) for u in cu_s]
    bwd = [ent(cand_s, v) for v in pu_s]
    eq = _eq_canon(cand_s, peer_s)
    return {"fwd": fwd, "bwd": bwd, "peer_r": peer_s, "peer_units_r": list(pu_s), "equiv": eq, "cost": 0.0, "n_maps": 1, "rank": 0}


def consensus_score(cand_fol: str | None, peer_outs: list[dict], modes=("csc", "csc_graded", "csc_multi"),
                    timeout_ms: int = 2000, graded: bool = True) -> dict:
    """Score candidate `cand_fol` against peer outputs [{'fol': str|None, 'alt_fol': str|None, 'model': ...}, ...].

    Returns {'status', 'n_peers', 'n_usable', 'n_unparseable_peers', 'n_unknown', 'per_peer' (True/False/None),
             'c_csc', 'c_csc_graded', 'c_csc_multi', 'unit_codes', 'secs'} (all scores oriented higher = more likely error)."""
    t0 = time.time()
    cs = norm_canon(cand_fol)
    usable = []
    n_bad = 0
    for p in peer_outs:
        c = norm_canon(p.get("fol"))
        if c is None:
            n_bad += 1
            continue
        usable.append({"c": c, "alt": norm_canon(p.get("alt_fol")) if p.get("alt_fol") else None, "model": p.get("model")})
    base = {"n_peers": len(peer_outs), "n_usable": len(usable), "n_unparseable_peers": n_bad}
    if cs is None:
        return {**base, "status": "UNPARSEABLE", "c_csc": 1.0, "c_csc_graded": 1.0, "c_csc_multi": 1.0, "n_unknown": 0,
                "per_peer": [], "unit_codes": [], "secs": 0.0}
    if len(usable) < 2:
        return {**base, "status": "csc_insufficient_peers", "c_csc": 0.5, "c_csc_graded": 0.5, "c_csc_multi": 0.5,
                "n_unknown": 0, "per_peer": [], "unit_codes": [], "secs": round(time.time() - t0, 3)}
    verd = [_eq_canon(cs, u["c"], timeout_ms) for u in usable]
    n_eq = sum(v is True for v in verd)
    out = {**base, "status": "OK", "per_peer": verd, "n_unknown": sum(v is None for v in verd), "c_csc": 1 - n_eq / len(usable)}
    # multi-reading endorsement
    endorse = []
    for i, u in enumerate(usable):
        if verd[i] is True:
            endorse.append(True)
            continue
        ok = False
        if u["alt"] is not None and _eq_canon(cs, u["alt"], timeout_ms) is True:
            for j, q in enumerate(usable):
                if j == i:
                    continue
                if _eq_canon(u["alt"], q["c"], timeout_ms) is True or (q["alt"] is not None and _eq_canon(u["alt"], q["alt"], timeout_ms) is True):
                    ok = True
                    break
        endorse.append(ok)
    out["c_csc_multi"] = 1 - sum(endorse) / len(usable)
    out["per_peer_multi"] = endorse
    if graded and "csc_graded" in modes:
        try:
            ent = PT.Entailer(timeout_ms)
            pool = [u["c"] for u in usable]
            table = {}
            for a in sorted(set([cs] + pool)):
                for b in pool:
                    if a != b and (a, b) not in table:
                        table[(a, b)] = _identity_pair(a, b, ent)
            g = PT.graded_consensus(cs, pool, table, ent, return_codes=True)
            out["c_csc_graded"] = g["g_score"] if g["g_score"] is not None else out["c_csc"]
            out["graded_support"], out["graded_coverage"] = g.get("support"), g.get("coverage")
            out["unit_codes"] = [c["code"] for c in g.get("unit_codes", [])]
        except (RecursionError, KeyError, ValueError, IndexError, TypeError) as ex:
            out["c_csc_graded"] = out["c_csc"]
            out["graded_error"] = str(ex)[:120]
            out["unit_codes"] = []
    out["secs"] = round(time.time() - t0, 3)
    return out


def majority_formula(peer_outs: list[dict], timeout_ms: int = 2000) -> str | None:
    """The peer formula (case-normalised canonical string) equivalent to the most other peers; requires >= 2 peers in
    its class (a strict peer majority for k = 3); None otherwise."""
    cs = [norm_canon(p.get("fol")) for p in peer_outs]
    cs = [c for c in cs if c is not None]
    best, bn = None, 0
    for i, a in enumerate(cs):
        n = 1 + sum(1 for j, b in enumerate(cs) if j != i and _eq_canon(a, b, timeout_ms) is True)
        if n > bn:
            best, bn = a, n
    return best if bn >= 2 else None


def typed_repair_same_vocab(cand_fol: str, target: str, budget_s: float = 10.0) -> dict:
    """Smallest typed edit sequence (depth <= 2; NEG, REV, QUANT, RESTR, CONN, MOVE, DROP, ADD, SWAP, BIND, SCOPE, UNGLUE)
    turning the candidate into a formula z3-equivalent to `target`, in the SAME vocabulary (identity map: case-normalised
    names; no aligner, no granularity bridge). The ops repair the candidate towards the target (an extra conjunct in the
    candidate is repaired by DROP, so the candidate's error type is the INVERSE: DROP-repair = ADD error).
    Returns {'cls': EQUIV | '<OP>[+<OP>]' | TIMEOUT_OR_COMPOUND | PARSE_FAIL | ERROR, 'ops', 'secs'}."""
    t0 = time.time()
    a = norm_canon(cand_fol)
    b = norm_canon(target)
    if a is None or b is None:
        return {"cls": "PARSE_FAIL", "ops": [], "secs": 0.0}
    try:
        if _eq_canon(a, b) is True:
            return {"cls": "EQUIV", "ops": [], "secs": round(time.time() - t0, 2)}
        ops, _ = RC.search(EFOL.parse(a), EFOL.parse(b), budget_s=budget_s)
        return {"cls": "+".join(ops) if ops else "TIMEOUT_OR_COMPOUND", "ops": ops or [], "secs": round(time.time() - t0, 2)}
    except Exception as ex:  # noqa: BLE001 - recorded, never silent
        return {"cls": "ERROR", "ops": [], "err": str(ex)[:100], "secs": round(time.time() - t0, 2)}


def csc_peers(text: str, signature: list, families: list[str] | None = None, k: int = 3, client=None) -> list[dict]:
    """Synchronous convenience wrapper: generate CSC peers for (text, signature) with the first k pool members whose
    family is not in `families` (the candidate's family). `client(model, messages, extra) -> raw text`. The experiment
    itself uses the async cached client in src/llm.py."""
    fams = set(families or [])
    models = [m for m in POOL if m[1] not in fams][:k]
    msgs = build_prompt(text, order_symbols(text, signature))
    out = []
    for model, fam, extra in models:
        raw = client(model, msgs, extra) if client else None
        out.append({"model": model, "family": fam, **parse_response(raw)})
    return out
