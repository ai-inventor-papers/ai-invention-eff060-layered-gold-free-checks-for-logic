"""Label-free pairwise equivalence-modulo-vocabulary (eqmv) matrix among ALL parseable outputs of one sentence.

pairwise_matrix(rows) is the reusable function (iteration 4 applies it unchanged to R_COMP):
  rows = [{'row_key', 'fol', 'slot', 'family' (vendor family), 'family_field', 'system_class'}] of ONE sentence.
  -> {'nodes': [{node_id, canon_fol, rows: [{row_key, slot, family, family_field, system_class, is_peer}]}],
      'pairs': [[i, j, equiv(True/False/None), reason, secs]], 'unparseable': [row_key...]}

It calls EXACTLY the iteration-1 eqmv (vendored exp 5 vendor_c/common.py, DEFAULT ms=3000) on the canonical strings
parsed by the dataset-E parser (peer_text.parse_fol + canon), with the canonical argument order (min, max) the frozen
eq() cache used and a hard SIGALRM pair cap of 30 s (-> UNKNOWN = None). GOLD / CCG rows are nodes but never peers.
"""
from __future__ import annotations

import hashlib
import os
import resource
import signal
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VEND = ROOT / "vendor_exp5"
for p in (VEND, VEND / "vendor_c"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

PAIR_CAP_S = 30
EQMV_MS = 3000


class _TO(Exception):
    pass


def _alarm(signum, frame):  # noqa: ARG001
    raise _TO()


def init_worker(mem_gb: float = 3.5) -> None:
    """Same worker limits as exp 5's pool_scoring.init_worker (RLIMIT_AS 3.5 GB, SIGALRM handler)."""
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


def pairwise_matrix(rows: list[dict], eqmv_ms: int = EQMV_MS, pair_cap_s: int = PAIR_CAP_S) -> dict:
    """Full node x node eqmv matrix for one sentence (see module docstring)."""
    import peer_text as PT  # binds `fol` to the dataset-E parser before vendor_c is imported
    from common import eqmv

    nodes: dict[str, dict] = {}
    unparseable = []
    for r in rows:
        e = PT.parse_fol(r["fol"])
        if e is None:
            unparseable.append(r["row_key"])
            continue
        cs = PT.canon(e)
        nd = nodes.setdefault(cs, {"canon_fol": cs, "rows": []})
        nd["rows"].append({"row_key": r["row_key"], "slot": r["slot"], "family": r["family"],
                           "family_field": r.get("family_field"), "system_class": r["system_class"],
                           "is_peer": r["system_class"] == "llm"})
    keys = sorted(nodes)
    out_nodes = [dict(node_id=i, **nodes[k]) for i, k in enumerate(keys)]
    pairs = []
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            a, b = keys[i], keys[j]  # keys sorted -> (a, b) == (min, max), the frozen cache order
            t0 = time.time()
            res, to = _with_alarm(pair_cap_s, eqmv, PT.parse_fol(a), PT.parse_fol(b), eqmv_ms)
            secs = round(time.time() - t0, 4)
            if to or res is None:
                pairs.append([i, j, None, "pair_cap_timeout", secs])
            else:
                pairs.append([i, j, res[0], res[1], secs])
    return {"nodes": out_nodes, "pairs": pairs, "unparseable": unparseable}


def work(task: dict) -> dict:
    """Worker entry: one sentence task -> matrix record (label-free)."""
    t0 = time.time()
    m = pairwise_matrix(task["rows"])
    m.update({"sentence_id": task["sentence_id"], "source_stratum": task["source_stratum"], "words": task["words"],
              "n_conditions": task["n_conditions"], "secs_total": round(time.time() - t0, 3), "eqmv_ms": EQMV_MS,
              "pair_cap_s": PAIR_CAP_S})
    return m


def code_sha() -> str:
    h = hashlib.sha256()
    for p in (Path(__file__), VEND / "vendor_c" / "common.py", VEND / "vendor_c" / "repair_census.py",
              VEND / "peer_text.py", VEND / "vendor_e" / "fol.py"):
        h.update(p.read_bytes())
    return h.hexdigest()[:16]
