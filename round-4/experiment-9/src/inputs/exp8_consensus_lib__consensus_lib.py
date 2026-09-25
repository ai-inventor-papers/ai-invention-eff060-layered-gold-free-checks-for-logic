"""consensus_lib: gold-free cross-family consensus metrics for NL->FOL candidates (iteration 3, Part D).

WHAT THESE METRICS MEASURE. Agreement of a candidate formula with INDEPENDENT translations ("peers") of the SAME sentence
produced by other model families. They do NOT measure truth against a reference; a candidate that every peer also gets
wrong in the same way (a coincident error) scores as faithful. Orientation everywhere: HIGHER = MORE LIKELY ERROR.

Modes of pair agreement (candidate c, peer p):
  exact  identical predicate/constant signature (names + arities) AND z3-equivalent with no mapping (the R_COMP-SIG mode).
  align  equivalent modulo vocabulary (iteration-1 eqmv): exact, else name-similarity alignment of predicates/constants
         (CamelCase-token Jaccard >= 0.5 or trigram Dice >= 0.6) in either direction, else a merge/split granularity
         bridge; each step z3-verified. Blind spot: RENAMES to dissimilar names break it (measured: RENAME false alarms).
  nf     NF-anchored name-free alignment (exp 5): k-best (k=5) predicate/constant bijections from structural signatures
         + text anchors, accepted only within a cost window (tau = 0.5), verified by z3 unit entailment both ways.
         Blind spot: formula automorphisms (structurally symmetric predicates), guarded but not removed by tau.
  hyb    PEER_HYB: align OR nf. UNKNOWN (z3 timeout / pair cap) never counts as agreement.
Scores:
  consensus_score  c = 1 - (#peers agreeing)/(#peers used)
  graded_consensus g = 1 - F1(support, coverage) over claim units (partial agreement), + unit error codes.
Failure modes (all explicit, never silent): unparseable candidate -> score 1.0 and status 'UNPARSEABLE'; unparseable peers
are dropped and counted; fewer than 2 usable peers -> score None and status 'PEER_UNAVAILABLE'; z3 UNKNOWN pairs are
counted in n_unknown and are never agreement.
Measured behaviour (this artifact, results/): on dataset E (real outputs of 10 LLM generators, R_AB labels) stratified
AUROC c_align 0.741, c_hyb 0.738, c_nf 0.686; hyb's extra agreements over align are label-discordant 39% of the time vs
13% for align agreements (over-alignment); on PERTURB rename controls both hyb and nf exceed a 0.10 false-alarm rate at
E-derived thresholds mostly because the unmutated reference itself is rarely endorsed by peers on long sentences.
Cost: z3 ~0.1-3 s CPU per pair (30 s cap); peers cost API $ per sentence (see peer_pool dry_run estimate).
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
os.environ.setdefault("NLTK_DATA", str(ROOT / "data" / "nltk_data"))
import peer_text as PT  # noqa: E402  (installs the dataset-E parser as module 'fol')
import pairs as PR  # noqa: E402
# Eager imports: every lazily-imported heavy module is loaded HERE, never inside a SIGALRM-guarded pair call (a slow first
# import on a network filesystem interrupted by the 30 s pair cap leaves scipy half-initialised: NameError '_ndimage_api').
import scipy.ndimage  # noqa: E402,F401
import scipy.optimize  # noqa: E402,F401
import scipy.stats  # noqa: E402,F401
from common import eqmv as _eqmv_warm  # noqa: E402,F401
import repair_census as _rc_warm  # noqa: E402,F401

DEFAULT_PARAMS = {"k": 5, "tau": {"NF-anchored": 0.5, "ALIGN": None}, "timeout_ms": 2000, "pair_cap_s": 30}
MODES = ("exact", "align", "nf", "hyb")
name_free_align = PT.name_free_align  # re-export: name_free_align(cand, peer, text=None, variant='NF-pure'|'NF-anchored', k, tau)


def equivalent_modulo_vocab(fol_a: str, fol_b: str, ms: int = 3000) -> tuple[bool | None, str]:
    """Iteration-1 eqmv on two formula STRINGS. Returns (True|False|None=UNKNOWN, how in {exact, align, gran, none})."""
    from common import eqmv
    a, b = PT.parse_fol(fol_a), PT.parse_fol(fol_b)
    if a is None or b is None:
        return None, "unparseable"
    return eqmv(a, b, ms=ms)


def _exact_eq(a_s: str, b_s: str, ms: int = 2000) -> bool | None:
    from common import _eq
    from repair_census import symbols
    a, b = PT.parse_fol(a_s), PT.parse_fol(b_s)
    if symbols(a) != symbols(b):
        return False
    return _eq(a, b, ms)


def _prepare(text: str, fol: str, peers: list[str]):
    e = PT.parse_fol(fol)
    cs = PT.canon(e) if e is not None else None
    ps, n_bad = [], 0
    for p in peers:
        pe = PT.parse_fol(p)
        if pe is None:
            n_bad += 1
        else:
            ps.append(PT.canon(pe))
    return cs, ps, n_bad


def consensus_score(text: str, fol: str, peers: list[str], mode: str = "hyb", params: dict | None = None) -> dict:
    """Binary cross-family consensus of candidate `fol` for sentence `text` against peer formulas.

    Inputs: text (the sentence), fol (candidate formula string), peers (formula strings from OTHER systems/families for the
    same sentence; do not include the candidate's own family), mode in {exact, align, nf, hyb}.
    Output: {'c_score': 1 - agree/used (higher = more likely error) | 1.0 if unparseable | None if < 2 peers,
             'status', 'n_peers', 'n_peers_unparseable', 'n_agree', 'n_unknown', 'per_peer': [True/False/None], 'secs'}.
    """
    assert mode in MODES, mode
    P = {**DEFAULT_PARAMS, **(params or {})}
    t0 = time.time()
    cs, ps, n_bad = _prepare(text, fol, peers)
    base = {"n_peers": len(ps), "n_peers_unparseable": n_bad, "mode": mode}
    if cs is None:
        return {**base, "c_score": 1.0, "status": "UNPARSEABLE", "n_agree": 0, "n_unknown": 0, "per_peer": [], "secs": 0.0}
    if len(ps) < 2:
        return {**base, "c_score": None, "status": "PEER_UNAVAILABLE", "n_agree": 0, "n_unknown": 0, "per_peer": [],
                "secs": round(time.time() - t0, 3)}
    ent = PT.Entailer(P["timeout_ms"])
    verd = []
    for p in ps:
        if p == cs:
            verd.append(True)
            continue
        if mode == "exact":
            verd.append(_exact_eq(cs, p, P["timeout_ms"]))
            continue
        modes = {"align": ("EQMV",), "nf": ("NF-anchored",), "hyb": ("EQMV", "NF-anchored")}[mode]
        pv = PR.pair_verdicts(cs, p, text, ent, P, None, modes=modes)
        verd.append({"align": pv["align_eq"], "nf": pv["nf_eq"], "hyb": pv["hyb_eq"]}[mode])
    n_agree = sum(v is True for v in verd)
    return {**base, "c_score": 1 - n_agree / len(ps), "status": "OK", "n_agree": n_agree,
            "n_unknown": sum(v is None for v in verd), "per_peer": verd, "secs": round(time.time() - t0, 3)}


def graded_consensus(text: str, fol: str, peers: list[str], mode: str = "hyb", params: dict | None = None) -> dict:
    """Graded (claim-unit) consensus. g_score = 1 - F1(support, coverage): support = share of the candidate's claim units
    entailed by the (mapped) peers, coverage = share of the peers' majority units the candidate entails. unit_codes name
    unsupported/uncovered units (NEG / QUANT / SWAP / ADD / DROP). mode: align (ALIGN map), nf (NF-anchored map), hyb
    (per peer: ALIGN map if align-equivalent, else NF map if nf-equivalent, else the map with more verified unit entailments).
    Output: {'g_score' (higher = more likely error; 1.0 unparseable; None < 2 peers), 'support', 'coverage', 'c_score_nf',
             'unit_codes', 'status'}."""
    assert mode in ("align", "nf", "hyb"), mode
    P = {**DEFAULT_PARAMS, **(params or {})}
    cs, ps, n_bad = _prepare(text, fol, peers)
    if cs is None:
        return {"g_score": 1.0, "status": "UNPARSEABLE", "n_peers_unparseable": n_bad}
    if len(ps) < 2:
        return {"g_score": None, "status": "PEER_UNAVAILABLE", "n_peers": len(ps), "n_peers_unparseable": n_bad}
    ent = PT.Entailer(P["timeout_ms"])
    table = {}
    for a in sorted(set([cs] + ps)):
        for b in ps:
            if a == b:
                continue
            pv = PR.pair_verdicts(a, b, text, ent, P, None, modes=("ALIGN", "NF-anchored", "EQMV"))
            table[(a, b)] = pv["al"] if mode == "align" else pv["nf"] if mode == "nf" else PR.composite_record(pv)
    g = PT.graded_consensus(cs, ps, table, ent, return_codes=True)
    return {"g_score": g["g_score"], "support": g.get("support"), "coverage": g.get("coverage"), "c_score_nf": g.get("c_score_nf"),
            "unit_codes": [c["code"] for c in g.get("unit_codes", [])], "status": "OK", "n_peers": len(ps), "n_peers_unparseable": n_bad}


def minimal_typed_repair(fol: str, target: str, budget_s: float = 10.0) -> dict:
    """Smallest typed edit sequence (depth <= 2; NEG, REV, QUANT, RESTR, CONN, MOVE, DROP, ADD, SWAP, BIND, SCOPE, UNGLUE)
    turning `fol` into a formula z3-equivalent to `target` after vocabulary alignment (exp C repair census).
    Returns {'cls': EQUIV | VOCAB | GRAN | '<OP>[+<OP>]' | TIMEOUT_OR_COMPOUND | PARSE_FAIL, 'ops', 'secs'}. Note the ops repair
    `fol` towards `target`: an extra conjunct in `fol` is repaired by DROP."""
    import typing_perturb as TP
    TP.BUDGET_S = budget_s
    return TP.typed_repair(("-", "lib", fol, target))


# ------------------------------------------------------------------------------------------------ peer pool
PEER_SLOTS = {  # dataset E generator slots (iteration 1 generate.py), temperature 0, few-shot fewshot_v1
    "G1": ("meta-llama/llama-3.1-8b-instruct", "meta", {}),
    "G1b": ("meta-llama/llama-3.3-70b-instruct", "meta", {}),
    "G2": ("qwen/qwen3-235b-a22b-2507", "qwen", {}),
    "G3": ("mistralai/mistral-small-3.2-24b-instruct", "mistral", {}),
    "G4": ("deepseek/deepseek-v3.2", "deepseek", {"reasoning": {"enabled": False}}),
    "G5": ("google/gemma-3-27b-it", "google", {}),
    "G6": ("microsoft/phi-4", "microsoft", {}),
    "G7": ("openai/gpt-4.1-mini", "openai", {}),
    "G8": ("google/gemini-2.5-flash", "google", {"reasoning": {"max_tokens": 0}}),
    "G9": ("cohere/command-r7b-12-2024", "cohere", {}),
}
PROMPT_P = ROOT / "data" / "prompts" / "fewshot_v1.txt"


def _messages(text: str) -> list[dict]:
    pr = json.loads(PROMPT_P.read_text())
    return [{"role": "system", "content": pr["system"]}] + pr["exemplars"] + [{"role": "user", "content": f"Sentence: {text}"}]


def _extract(out: str) -> str | None:
    for line in (out or "").splitlines():
        if line.strip().startswith("FOL:"):
            return line.split("FOL:", 1)[1].strip()
    s = (out or "").strip()
    return s or None


def peer_pool(text: str, families: list[str] | None = None, k: int | None = None, dry_run: bool = True,
              client=None, price_per_token: dict | None = None, ledger: Path | None = None) -> dict:
    """Generate peer formalisations of `text` with dataset E's fewshot_v1 prompt on the E generator slots (one per family;
    `families` = slot ids, default all; k = first k slots). Calls go to OpenRouter at os.environ['OPENROUTER_BASE_URL'].
    dry_run=True: no call; returns {'estimate_usd', 'slots'}. Otherwise returns {'peers': [{'slot','family','model','fol',
    'raw','cost'}], 'cost_usd'} and appends $ per call to `ledger`. `client(model, messages, params) -> (text, cost)` can
    be injected (tests use a mock)."""
    slots = [s for s in (families or list(PEER_SLOTS)) if s in PEER_SLOTS][: k or None]
    msgs = _messages(text)
    n_in = int(sum(len(m["content"]) for m in msgs) / 3.2) + 8
    pr = price_per_token or {}
    est = sum(n_in * pr.get(PEER_SLOTS[s][0], {}).get("in", 3e-7) + 80 * pr.get(PEER_SLOTS[s][0], {}).get("out", 1.2e-6) for s in slots)
    if dry_run:
        return {"estimate_usd": est, "slots": slots, "n_prompt_tokens_est": n_in}
    client = client or _openrouter_client
    out, total = [], 0.0
    for s in slots:
        model, fam, extra = PEER_SLOTS[s]
        txt, cost = client(model, msgs, {**extra, "temperature": 0.0, "max_tokens": 600})
        total += cost or 0.0
        out.append({"slot": s, "family": fam, "model": model, "fol": _extract(txt), "raw": txt, "cost": cost})
        if ledger is not None:
            with Path(ledger).open("a") as f:
                f.write(json.dumps({"ts": time.time(), "component": "peer_pool", "model": model, "cost_usd": cost}) + "\n")
    return {"peers": out, "cost_usd": total}


def _openrouter_client(model: str, messages: list[dict], params: dict):
    import requests
    base = os.environ["OPENROUTER_BASE_URL"].rstrip("/")
    r = requests.post(base + "/chat/completions", timeout=120,
                      headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}", "User-Agent": "aii-consensus-lib/1.0"},
                      json={"model": model, "messages": messages, "usage": {"include": True}, **params})
    d = r.json()
    if "choices" not in d:
        raise RuntimeError(f"OpenRouter error: {str(d)[:200]}")
    return d["choices"][0]["message"].get("content") or "", float((d.get("usage") or {}).get("cost") or 0.0)
