"""The user's pilot structural metrics (dpv_pilot_study metric1/2/3/5), adapted from Prolog files to per-sentence FOL
within a story. See results/pilot_mapping.md for the original definitions and the adaptation.

  pilot_joint_conflict  metric1 (load warnings/conflicts when files are loaded together) -> z3: story S ∪ {cand} UNSAT
                        (MALLS, no story: cand alone UNSAT). Timeout 5 s -> failure (never merged with SAT/UNSAT).
  pilot_story_unsat     diagnostic: S alone UNSAT.
  pilot_arity_incons    metric2 arity part: #predicate names in cand used with an arity different from S, + clashes in cand.
  pilot_shape_incons    metric2 shape part: #predicates of cand whose argument-kind signature (var/const per slot) never
                        occurs for that predicate in S (only predicates also used in S).
  pilot_dangling        metric3: fraction of cand predicates+constants that appear nowhere else in S (NA without a story).
  pilot_undeclared      metric3 analogue for Logic-LM: cand predicates absent from the system's own 'Predicates:' list.
  pilot_rerun_jacc      metric5 inter-run Jaccard: predicate-token-set Jaccard with the other Logic-LM systems' candidates
                        for the same sentence (a cross-system PROXY for rerun stability; track L only).
"""
from __future__ import annotations

import multiprocessing as mp
import os
import re
import time
from concurrent.futures import ProcessPoolExecutor

from loguru import logger

CAMEL = re.compile(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+")


def _atoms(e, acc, bound=frozenset()):
    k = e[0]
    if k == "atom":
        acc.append((e[1], e[2], bound))
    elif k in ("all", "ex"):
        _atoms(e[2], acc, bound | {e[1]})
    elif k == "not":
        _atoms(e[1], acc, bound)
    else:
        _atoms(e[1], acc, bound); _atoms(e[2], acc, bound)
    return acc


def _sig(e):
    """{pred_name: set(arity)}, {pred_name: set(shape)}, set(constants)."""
    ar, sh, consts = {}, {}, set()
    for name, args, bound in _atoms(e, []):
        ar.setdefault(name, set()).add(len(args))
        shape = tuple("V" if a in bound else "C" for a in args)
        sh.setdefault((name, len(args)), set()).add(shape)
        consts |= {a for a in args if a not in bound}
    return ar, sh, consts


def _sat(formulas, ms=5000):
    import z3
    from .labeller.fol import mkpred, preds, to_z3
    ar = {}
    for f in formulas:
        ar.update(preds(f))
    P = {q: mkpred(q, m) for q, m in ar.items()}
    s = z3.Solver()
    s.set("timeout", ms)
    for f in formulas:
        s.add(to_z3(f, {}, P))
    r = s.check()
    return "UNSAT" if r == z3.unsat else ("SAT" if r == z3.sat else "UNKNOWN")


def pilot_one(args) -> dict:
    """args: (key, cand_str, story_fol_list, declared, has_story)."""
    key, cand, story, declared, has_story = args
    import sys
    sys.setrecursionlimit(10000)
    from .labeller.fol import parse
    t0 = time.time()
    out = {"key": key}
    try:
        c = parse(cand) if cand else None
    except Exception:  # noqa: BLE001
        c = None
    if c is None:
        out.update(parse_fail=1, fail="unparseable")
        return out
    S = []
    n_story_bad = 0
    for s in story or []:
        try:
            S.append(parse(s))
        except Exception:  # noqa: BLE001
            n_story_bad += 1
    out["n_story_parsed"], out["n_story_unparsed"] = len(S), n_story_bad
    ar_c, sh_c, cons_c = _sig(c)
    clash_in = sum(1 for v in ar_c.values() if len(v) > 1)
    ar_s, sh_s, cons_s = {}, {}, set()
    for f in S:
        a, s_, cc = _sig(f)
        for k, v in a.items():
            ar_s.setdefault(k, set()).update(v)
        for k, v in s_.items():
            sh_s.setdefault(k, set()).update(v)
        cons_s |= cc
    out["pilot_arity_incons"] = clash_in + sum(1 for n, v in ar_c.items() if n in ar_s and not (v <= ar_s[n]))
    out["pilot_shape_incons"] = sum(1 for k, v in sh_c.items() if k in sh_s and not (v & sh_s[k]))
    try:
        if has_story:
            r = _sat(S + [c])
            out["pilot_joint_conflict"] = None if r == "UNKNOWN" else int(r == "UNSAT")
            rs = _sat(S) if S else "SAT"
            out["pilot_story_unsat"] = None if rs == "UNKNOWN" else int(rs == "UNSAT")
        else:
            r = _sat([c])
            out["pilot_joint_conflict"] = None if r == "UNKNOWN" else int(r == "UNSAT")
            out["pilot_story_unsat"] = None
        if out["pilot_joint_conflict"] is None:
            out["fail_joint"] = "z3_timeout"
    except Exception as e:  # noqa: BLE001
        out["pilot_joint_conflict"] = None
        out["fail_joint"] = f"z3_error:{str(e)[:80]}"
    if has_story:
        syms = set(ar_c) | cons_c
        out["pilot_dangling"] = sum(1 for x in syms if x not in ar_s and x not in cons_s) / max(1, len(syms))
    else:
        out["pilot_dangling"] = None  # not applicable (no story)
    if declared:
        dn = {d[0] for d in declared}
        out["pilot_undeclared"] = sum(1 for n in ar_c if n not in dn) / max(1, len(ar_c))
    else:
        out["pilot_undeclared"] = None
    out["pred_tokens"] = sorted({w.lower() for n in ar_c for w in CAMEL.findall(n)})
    out["parse_fail"] = 0
    out["z3_seconds"] = round(time.time() - t0, 3)
    return out


def compute_pilot(rows: list[dict], workers: int = 6) -> dict:
    """rows: dicts with key, candidate_fol, story_premises_fol, declared_predicates, has_story."""
    os.environ["PYTHONHASHSEED"] = "0"
    args = [(r["key"], r["candidate_fol"], r.get("story_premises_fol") or [], r.get("declared_predicates") or [],
             r["has_story"]) for r in rows]
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn")) as pool:
        res = list(pool.map(pilot_one, args, chunksize=4))
    logger.info(f"pilot metrics on {len(rows)} rows in {time.time()-t0:.0f}s")
    return {r["key"]: r for r in res}


def rerun_jaccard(items: list[dict], pilot: dict) -> dict:
    """Track L: mean predicate-token Jaccard with the OTHER Logic-LM systems' candidates for the same sentence+role."""
    from .common import norm
    groups = {}
    for it in items:
        if it["track"] != "L":
            continue
        groups.setdefault((norm(it["text"]), it["role"]), []).append(it)
    out = {}
    for g in groups.values():
        for it in g:
            mine = pilot.get(it["item_id"], {}).get("pred_tokens")
            others = [pilot.get(o["item_id"], {}).get("pred_tokens") for o in g if o["system"] != it["system"]]
            others = [o for o in others if o is not None]
            if mine is None or not others:
                out[it["item_id"]] = None
                continue
            js = [len(set(mine) & set(o)) / max(1, len(set(mine) | set(o))) for o in others]
            out[it["item_id"]] = sum(js) / len(js)
    return out
