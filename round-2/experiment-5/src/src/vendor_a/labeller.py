"""Shared-screen labeller: identical logic to iter-3 probes/repair_census.work(), with the fixed fol.py parser.

equivalent_modulo_vocab(cand, ref) -> status in EQUIV | VOCAB | GRAN | NONEQ | UNPARSEABLE | TIMEOUT
minimal_typed_repair(cand, ref)    -> smallest typed-edit sequence (depth <= 2, z3-verified) or None
label(cand, ref)                   -> (label, auto_class, ops)
    EQUIV / VOCAB            -> CORRECT     (auto_class EQUIV / VOCAB)
    GRAN                     -> UNCERTAIN   (auto_class GRAN, vocab-borderline)
    NONEQ + repair depth 1-2 -> ERROR       (auto_class = '+'.join(sorted ops))
    NONEQ + no repair        -> UNCERTAIN   (auto_class COMPOUND)
    TIMEOUT                  -> UNCERTAIN   (auto_class TIMEOUT_UNKNOWN)
    candidate unparseable    -> UNPARSEABLE (kept in every denominator)
    reference unparseable    -> REF_UNPARSEABLE (item cannot be labelled; counted, excluded from analyses)
Labels are never read by scoring code; only analysis.py joins them.
"""
from __future__ import annotations

import signal
import sys
import time

sys.setrecursionlimit(10000)

from fol import parse, equivalent  # noqa: E402
from repair_census import align, gran_bridge, search  # noqa: E402


class _ItemTimeout(Exception):
    pass


def _alarm(signum, frame):  # noqa: ARG001
    raise _ItemTimeout()


def equivalent_modulo_vocab(cand_str: str, ref_str: str) -> dict:
    """Is the candidate equivalent to the reference, possibly after a vocabulary (rename) or granularity (merge/split,
    arity-reification) bridge?  Mirrors repair_census.work() stages 0-1."""
    try:
        r = parse(ref_str)
    except Exception as ex:  # noqa: BLE001
        return {"status": "REF_UNPARSEABLE", "err": str(ex)[:120]}
    try:
        c = parse(cand_str)
    except Exception as ex:  # noqa: BLE001
        return {"status": "UNPARSEABLE", "err": str(ex)[:120]}
    eq = equivalent(c, r)
    if eq is True:
        return {"status": "EQUIV", "pmap": {}, "cmap": {}}
    if eq is None:
        return {"status": "TIMEOUT", "pmap": {}, "cmap": {}}
    ac, pmap, cmap = align(c, r)
    pm = {f"{k[0]}/{k[1]}": v for k, v in pmap.items()}
    if equivalent(ac, r) is True:
        return {"status": "VOCAB", "pmap": pm, "cmap": cmap}
    gb = gran_bridge(ac, r)
    if gb and equivalent(gb[0], gb[1]) is True:
        return {"status": "GRAN", "pmap": pm, "cmap": cmap}
    return {"status": "NONEQ", "pmap": pm, "cmap": cmap, "_base": gb if gb else (ac, r)}


def minimal_typed_repair(cand_str: str, ref_str: str, budget_s: float = 25.0) -> dict:
    """Breadth-first typed-edit repair (NEG REV QUANT RESTR CONN MOVE DROP ADD SWAP BIND SCOPE UNGLUE), depth <= 2, on the
    vocabulary-aligned (and granularity-bridged, when a bridge exists) candidate; accepted when z3 proves equivalence."""
    st = equivalent_modulo_vocab(cand_str, ref_str)
    if st["status"] != "NONEQ":
        return {"ops": None, "depth": None, "secs": 0.0, "status": st["status"]}
    base, tgt = st["_base"]
    ops, dt = search(base, tgt, budget_s=budget_s)
    return {"ops": ops, "depth": len(ops) if ops else None, "secs": round(dt, 2), "status": "NONEQ"}


def label(cand_str: str, ref_str: str, budget_s: float = 25.0) -> dict:
    t0 = time.time()
    st = equivalent_modulo_vocab(cand_str, ref_str)
    s = st["status"]
    out = {"status": s, "pmap": st.get("pmap", {}), "cmap": st.get("cmap", {}), "ops": None, "depth": None}
    if s in ("EQUIV", "VOCAB"):
        out.update(label="CORRECT", auto_class=s)
    elif s == "GRAN":
        out.update(label="UNCERTAIN", auto_class="GRAN")
    elif s == "UNPARSEABLE":
        out.update(label="UNPARSEABLE", auto_class="UNPARSEABLE")
    elif s == "REF_UNPARSEABLE":
        out.update(label="REF_UNPARSEABLE", auto_class="REF_UNPARSEABLE")
    elif s == "TIMEOUT":
        out.update(label="UNCERTAIN", auto_class="TIMEOUT_UNKNOWN")
    else:
        base, tgt = st["_base"]
        ops, dt = search(base, tgt, budget_s=budget_s)
        if ops:
            out.update(label="ERROR", auto_class="+".join(sorted(ops)), ops=sorted(ops), depth=len(ops))
        else:
            out.update(label="UNCERTAIN", auto_class="COMPOUND")
    out["secs"] = round(time.time() - t0, 2)
    return out


def label_job(args: tuple) -> dict:
    """Worker entry: (key, cand, ref, budget_s, hard_s). Hard per-item cap via SIGALRM -> UNCERTAIN(TIMEOUT_UNKNOWN)."""
    key, cand, ref, budget_s, hard_s = args
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(int(hard_s))
    try:
        res = label(cand, ref, budget_s)
    except _ItemTimeout:
        res = {"status": "TIMEOUT", "label": "UNCERTAIN", "auto_class": "TIMEOUT_UNKNOWN", "ops": None, "depth": None,
               "pmap": {}, "cmap": {}, "secs": float(hard_s), "hard_timeout": True}
    except RecursionError:
        res = {"status": "TIMEOUT", "label": "UNCERTAIN", "auto_class": "TIMEOUT_UNKNOWN", "ops": None, "depth": None,
               "pmap": {}, "cmap": {}, "secs": 0.0, "error": "RecursionError"}
    finally:
        signal.alarm(0)
    res["key"] = key
    return res
