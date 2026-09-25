"""PEER_HYB pair engine (iteration 3, T3): pair-level ALIGN / NF-anchored / HYB verdicts and per-row consensus scores.

For every sentence task we compute, for each ordered pair (a, b) with a in {candidates} ∪ pool and b in pool, a != b:
  align_eq = vendor_c common.eqmv(parse(a), parse(b))   (EXACTLY the call exp 5 pool_scoring.score_sentence makes for
             c_score_align, symmetric, 30 s SIGALRM cap -> None)
  nf       = peer_text.pair_result(a, b, ent, text, variant='NF-anchored', k=5, tau=0.5)   (exp 5 NF-anchored)
  al       = peer_text.pair_result(a, b, ent, variant='ALIGN')                             (exp 5 graded ALIGN)
  hyb_eq   = True if align_eq is True or nf['equiv'] is True; False if both are False; else None (UNKNOWN, never agreement)
Row scores (leave-one-FAMILY-out pool P_c, as exp 5):
  c_align = 1 - #(align_eq True)/|P_c|   c_nf = graded_consensus(NF pairs)['c_score_nf']   c_hyb = 1 - #(hyb_eq True)/|P_c|
  g_align = graded_consensus(ALIGN pairs)  g_nf = graded_consensus(NF pairs)
  g_hyb   = graded_consensus over a composite pair table: ALIGN record if align_eq True, else NF record if nf_eq True,
            else whichever record has more verified (True) unit entailments fwd+bwd (ties -> ALIGN).  Pre-registered.
All scores are NA (None) when |P_c| < 2 (peer_unavailable). Unparseable candidates get coverage_status UNPARSEABLE.
Identical canonical strings are True in every mode (exp C gotcha).
"""
from __future__ import annotations

import hashlib
import json
import os
import resource
import signal
import sqlite3
import sys
import time
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
os.environ.setdefault("NLTK_DATA", str(ROOT / "data" / "nltk_data"))
import peer_text as PT  # noqa: E402

CACHE_DB = ROOT / "cache" / "pair_cache.sqlite"


class _TO(Exception):
    pass


def _alarm(signum, frame):  # noqa: ARG001
    raise _TO()


def init_worker(mem_gb: float = 3.5):
    os.environ["PYTHONHASHSEED"] = "0"
    try:
        resource.setrlimit(resource.RLIMIT_AS, (int(mem_gb * 1024 ** 3), int(mem_gb * 1024 ** 3)))
    except (ValueError, OSError):
        pass
    signal.signal(signal.SIGALRM, _alarm)


def _with_alarm(secs: int, fn, *a, **kw):
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(secs)
    try:
        return fn(*a, **kw), False
    except _TO:
        return None, True
    finally:
        signal.alarm(0)


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest()


# ------------------------------------------------------------------------------------------------ sqlite pair cache
class PairCache:
    """Pair cache keyed by (mode, sha1(a), sha1(b), sha1(text) for NF). Workers use an in-memory dict preloaded by the
    parent (`preload`) and return their new entries; ONLY the parent process writes the sqlite file (single writer: the
    workspace sits on a network filesystem where multi-process WAL is unsafe). Values are JSON pair records."""

    def __init__(self, preload: dict | None = None, enabled: bool = True):
        self.enabled = enabled
        self.mem: dict = dict(preload or {})
        self.new: dict = {}

    @staticmethod
    def key(mode: str, a: str, b: str, text: str | None) -> str:
        return f"{mode}|{sha1(a)}|{sha1(b)}|{sha1(text) if (mode == 'NF-anchored' and text) else '-'}"

    def get(self, mode, a, b, text=None):
        return self.mem.get(self.key(mode, a, b, text)) if self.enabled else None

    def put(self, mode, a, b, text, v):
        if not self.enabled:
            return
        k = self.key(mode, a, b, text)
        self.mem[k] = v
        self.new[k] = v

    def flush(self):  # kept for API symmetry; persistence is done by the parent (store_pairs / load_pairs)
        return


def open_db(path: Path = CACHE_DB) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(str(path), timeout=120)
    con.execute("CREATE TABLE IF NOT EXISTS pc (k TEXT PRIMARY KEY, v TEXT)")
    con.commit()
    return con


def store_pairs(con: sqlite3.Connection, new: dict):
    if new:
        con.executemany("INSERT OR REPLACE INTO pc (k, v) VALUES (?, ?)", [(k, json.dumps(v, ensure_ascii=False)) for k, v in new.items()])
        con.commit()


def load_pairs(con: sqlite3.Connection, keys: list[str]) -> dict:
    out = {}
    for i in range(0, len(keys), 500):
        chunk = keys[i:i + 500]
        q = "SELECT k, v FROM pc WHERE k IN (%s)" % ",".join("?" * len(chunk))
        for k, v in con.execute(q, chunk):
            out[k] = json.loads(v)
    return out


def preload_keys(text: str, pool_strings: list[str]) -> list[str]:
    """Cache keys of every peer-peer pair of a sentence (all modes), for reuse across scoring passes."""
    ks = []
    for a in pool_strings:
        for b in pool_strings:
            if a == b:
                continue
            ks += [PairCache.key("ALIGN", a, b, None), PairCache.key("NF-anchored", a, b, text)]
            if a < b:
                ks.append(PairCache.key("EQMV", a, b, None))
    return ks


# ------------------------------------------------------------------------------------------------ pair verdicts
def _unknown_pair(cand_s: str, peer_s: str) -> dict:
    return {"fwd": [None] * len(PT.units_of(cand_s)[0]), "bwd": [None] * len(PT.units_of(peer_s)[0]), "peer_r": peer_s,
            "peer_units_r": list(PT.units_of(peer_s)[0]), "equiv": None, "cost": None, "n_maps": 0, "rank": None,
            "timeout": True}


def _slim(r: dict) -> dict:
    return {k: r.get(k) for k in ("fwd", "bwd", "peer_r", "peer_units_r", "equiv", "cost", "n_maps", "rank", "timeout")}


def n_true(r: dict | None) -> int:
    if r is None:
        return 0
    return sum(x is True for x in r["fwd"]) + sum(x is True for x in r["bwd"])


def hyb_of(a_eq, n_eq):
    """OR with UNKNOWN: True if either True; False if both False; else None (never counts as agreement)."""
    if a_eq is True or n_eq is True:
        return True
    if a_eq is False and n_eq is False:
        return False
    return None


def pair_verdicts(cand_s: str, peer_s: str, text: str | None, ent: PT.Entailer, params: dict,
                  cache: PairCache | None = None, modes=("ALIGN", "NF-anchored", "EQMV")) -> dict:
    """Pair-level verdicts for canonical strings cand_s, peer_s (peer aligned INTO the candidate's vocabulary).
    Returns {'align_eq', 'nf_eq', 'hyb_eq', 'nf_cost', 'nf_rank', 'nf', 'al', 'secs'}."""
    cache = cache or PairCache(enabled=False)
    t0 = time.time()
    out = {}
    if cand_s == peer_s:
        ident = PT.pair_result(cand_s, peer_s, ent)
        return {"align_eq": True, "nf_eq": True, "hyb_eq": True, "nf_cost": 0.0, "nf_rank": 0, "nf": ident, "al": ident,
                "secs": 0.0}
    for mode in modes:
        if mode == "EQMV":
            a, b = (cand_s, peer_s) if cand_s < peer_s else (peer_s, cand_s)  # symmetric, exp 5 key order
            v = cache.get("EQMV", a, b)
            if v is None:
                from common import eqmv
                res, to = _with_alarm(params["pair_cap_s"], eqmv, PT.parse_fol(a), PT.parse_fol(b))
                v = {"eq": None if (to or res is None) else res[0], "how": None if (to or res is None) else res[1],
                     "timeout": bool(to)}
                cache.put("EQMV", a, b, None, v)
            out["eqmv"] = v
        else:
            v = cache.get(mode, cand_s, peer_s, text)
            if v is None:
                res, to = _with_alarm(params["pair_cap_s"], PT.pair_result, cand_s, peer_s, ent, text=text, variant=mode,
                                      k=params["k"], tau=params["tau"].get(mode))
                v = _slim(_unknown_pair(cand_s, peer_s) if (to or res is None) else res)
                cache.put(mode, cand_s, peer_s, text, v)
            out["nf" if mode == "NF-anchored" else "al"] = v
    a_eq = out.get("eqmv", {}).get("eq")
    n_eq = out.get("nf", {}).get("equiv") if "nf" in out else None
    return {"align_eq": a_eq, "nf_eq": n_eq, "hyb_eq": hyb_of(a_eq, n_eq), "nf_cost": (out.get("nf") or {}).get("cost"),
            "nf_rank": (out.get("nf") or {}).get("rank"), "nf": out.get("nf"), "al": out.get("al"),
            "secs": round(time.time() - t0, 3)}


def composite_record(pv: dict) -> dict:
    """g_score_hyb mapping rule (pre-registered): ALIGN record if align_eq True, else NF record if nf_eq True, else the
    record with more verified unit entailments (ties -> ALIGN)."""
    al, nf = pv["al"], pv["nf"]
    if pv["align_eq"] is True:
        return al
    if pv["nf_eq"] is True:
        return nf
    return al if n_true(al) >= n_true(nf) else nf


# ------------------------------------------------------------------------------------------------ per-sentence worker
def score_sentence(sent: dict, params: dict) -> dict:
    """sent = {'sentence_id', 'text', 'rows': [{'key', 'fol', 'family', 'is_peer', 'pool_rule'?}]}.
    pool_rule: 'lofo' (default: peers of a different family and not the row itself) | 'all' (every peer: PERTURB rows, whose
    base is a reference with no family). Returns {'sentence_id', 'rows': [...], 'pairs': [...], 'stats'}."""
    t_all = time.time()
    text = sent["text"]
    rows = sent["rows"]
    ent = PT.Entailer(params["timeout_ms"])
    cache = PairCache(preload=sent.get("preload"), enabled=params.get("use_cache", True))
    parsed = {}
    for r in rows:
        e = PT.parse_fol(r["fol"])
        parsed[r["key"]] = PT.canon(e) if e is not None else None
    pool = [r for r in rows if r.get("is_peer") and parsed[r["key"]] is not None]
    pool_strings = sorted({parsed[r["key"]] for r in pool})
    cand_strings = sorted({parsed[r["key"]] for r in rows if parsed[r["key"]] is not None})
    PV = {}
    n_to = {"eqmv": 0, "nf": 0, "al": 0}
    for a in sorted(set(cand_strings) | set(pool_strings)):
        for b in pool_strings:
            if a == b:
                continue
            pv = pair_verdicts(a, b, text, ent, params, cache)
            PV[(a, b)] = pv
            n_to["eqmv"] += pv["align_eq"] is None
            n_to["nf"] += bool((pv["nf"] or {}).get("timeout"))
            n_to["al"] += bool((pv["al"] or {}).get("timeout"))
        cache.flush()
    pairs_nf = {k: v["nf"] for k, v in PV.items()}
    pairs_al = {k: v["al"] for k, v in PV.items()}
    pairs_hy = {k: composite_record(v) for k, v in PV.items()}
    out_rows, out_pairs = [], []
    for r in rows:
        cs = parsed[r["key"]]
        o = {"key": r["key"], "coverage_status": "OK" if cs else "UNPARSEABLE"}
        out_rows.append(o)
        if cs is None:
            continue
        if r.get("pool_rule") == "all":
            P_rows = [p for p in pool if p["key"] != r["key"]]
        else:
            P_rows = [p for p in pool if p["family"] != r["family"] and p["key"] != r["key"]]
        P_c = [parsed[p["key"]] for p in P_rows]
        o["n_peers"] = len(P_c)
        o["peer_unavailable"] = len(P_c) < 2
        verd = []
        for p, ps in zip(P_rows, P_c):
            if ps == cs:
                v = {"align_eq": True, "nf_eq": True, "hyb_eq": True, "nf_cost": 0.0}
            else:
                pv = PV[(cs, ps)]
                v = {k: pv[k] for k in ("align_eq", "nf_eq", "hyb_eq", "nf_cost")}
            verd.append(v)
            if params.get("emit_pairs", True):
                out_pairs.append({"cand": r["key"], "peer": p["key"], **v})
        if len(P_c) < 2:
            for c in ("c_align", "c_nf", "c_hyb", "g_align", "g_nf", "g_hyb"):
                o[c] = None
            o["n_unknown_hyb"] = 0
            continue
        n = len(P_c)
        o["c_align"] = 1 - sum(v["align_eq"] is True for v in verd) / n
        o["c_hyb"] = 1 - sum(v["hyb_eq"] is True for v in verd) / n
        o["c_nf_pairs"] = 1 - sum(v["nf_eq"] is True for v in verd) / n
        o["n_agree_align"] = sum(v["align_eq"] is True for v in verd)
        o["n_agree_nf"] = sum(v["nf_eq"] is True for v in verd)
        o["n_agree_hyb"] = sum(v["hyb_eq"] is True for v in verd)
        o["n_unknown_align"] = sum(v["align_eq"] is None for v in verd)
        o["n_unknown_nf"] = sum(v["nf_eq"] is None for v in verd)
        o["n_unknown_hyb"] = sum(v["hyb_eq"] is None for v in verd)
        for tag, pr in (("nf", pairs_nf), ("align", pairs_al), ("hyb", pairs_hy)):
            try:
                gc_ = PT.graded_consensus(cs, P_c, pr, ent, return_codes=params.get("codes", False))
            except (KeyError, RecursionError) as ex:  # noqa: PERF203 - recorded, never silently dropped
                o[f"g_{tag}"] = None
                o[f"g_{tag}_err"] = str(ex)[:120]
                continue
            o[f"g_{tag}"] = gc_["g_score"]
            if tag == "nf":
                o["c_nf"] = gc_["c_score_nf"]
            if tag == "align":
                o["c_align_graded_map"] = gc_["c_score_nf"]  # exp 5 frozen 'c_score_nf' column (ALIGN-variant equivalence)
            if params.get("codes", False):
                o[f"top_code_{tag}"] = gc_.get("top_code")
                o[f"unit_codes_{tag}"] = [c["code"] for c in gc_.get("unit_codes", [])]
        # medoid under the HYB agreement (for Part C typing)
        if params.get("medoid", False):
            for md in ("hyb_eq", "nf_eq", "align_eq"):
                o["medoid_" + md.split("_")[0]] = medoid_of(P_c, PV, md)
    stats = {"n_pairs": len(PV), "timeouts": n_to, "secs_total": round(time.time() - t_all, 2), "ent": dict(ent.stats),
             "n_cache_hits_preload": len(sent.get("preload") or {}), "n_new_cache": len(cache.new)}
    return {"sentence_id": sent["sentence_id"], "rows": out_rows, "pairs": out_pairs, "stats": stats, "new_cache": cache.new}


def medoid_of(P: list[str], PV: dict, mode: str = "hyb_eq") -> str | None:
    """Pool member agreeing (under `mode`) with the most other pool members (ties -> lexicographically first string)."""
    if not P:
        return None
    best = None
    for i, a in enumerate(P):
        n = sum(1 for j, b in enumerate(P) if j != i and (a == b or (PV.get((a, b)) or {}).get(mode) is True))
        if best is None or n > best[0] or (n == best[0] and a < best[1]):
            best = (n, a)
    return best[1]
