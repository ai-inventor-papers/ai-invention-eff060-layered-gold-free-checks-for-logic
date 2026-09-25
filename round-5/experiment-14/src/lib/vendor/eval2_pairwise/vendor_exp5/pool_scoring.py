"""Per-sentence scoring worker shared by screen_fit.py (screen) and score_E.py (held-out E).

score_sentence(sent, params) takes ONE sentence with its candidate rows and pool rows (label-free) and returns one
result dict per candidate row: PEER scores for the requested variants (g_score, support, coverage, c_score_nf, unit
codes, n_unknown, n_peers_used, g_score_k6, g_score_famfield, nf_eq_medoid), c_score_align (iteration-1 aligner eqmv,
reference column), eqmv medoid + medoid_ops (exp C typed repair, second readout), TEXT columns (l2_bow, l3_z3, l1, l2_role)
and timing. Each pair has a hard SIGALRM cap (pair -> UNKNOWN); the worker process has an RLIMIT_AS cap.
"""
from __future__ import annotations

import random
import resource
import signal
import sys
import time
from pathlib import Path

SRC = Path(__file__).resolve().parent
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
import peer_text as PT  # noqa: E402


class _TO(Exception):
    pass


def _alarm(signum, frame):  # noqa: ARG001
    raise _TO()


def init_worker(mem_gb: float = 3.5):
    import os
    os.environ["PYTHONHASHSEED"] = "0"
    try:
        resource.setrlimit(resource.RLIMIT_AS, (int(mem_gb * 1024 ** 3), int(mem_gb * 1024 ** 3)))
    except (ValueError, OSError):
        pass
    signal.signal(signal.SIGALRM, _alarm)


def _unknown_pair(cand_s: str, peer_s: str) -> dict:
    return {"fwd": [None] * len(PT.units_of(cand_s)[0]), "bwd": [None] * len(PT.units_of(peer_s)[0]), "peer_r": peer_s,
            "peer_units_r": list(PT.units_of(peer_s)[0]), "equiv": None, "cost": None, "n_maps": 0, "rank": None,
            "timeout": True}


def _with_alarm(secs: int, fn, *a, **kw):
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(secs)
    try:
        return fn(*a, **kw), False
    except _TO:
        return None, True
    finally:
        signal.alarm(0)


def score_sentence(sent: dict, params: dict) -> dict:
    """sent = {'sentence_id', 'text', 'q' (L3 questionnaire or None), 'rows': [{'key', 'fol', 'family', 'family_field',
    'is_peer', 'q_disg'?, 'fol_disg'?, 'text_disg'?}]}; params = {'variants', 'k', 'tau': {variant: tau},
    'timeout_ms', 'pair_cap_s', 'k6_seeds', 'medoid_budget_s', 'do_align', 'do_text', 'codes'}."""
    t_all = time.time()
    text = sent["text"]
    rows = sent["rows"]
    ent = PT.Entailer(params["timeout_ms"])
    parsed = {}
    for r in rows:
        e = PT.parse_fol(r["fol"])
        parsed[r["key"]] = (PT.canon(e), e) if e is not None else (None, None)
    pool = [r for r in rows if r.get("is_peer") and parsed[r["key"]][0] is not None]
    pool_strings = sorted({parsed[r["key"]][0] for r in pool})
    cand_strings = sorted({parsed[r["key"]][0] for r in rows if parsed[r["key"]][0] is not None})
    out_rows = {r["key"]: {"key": r["key"], "coverage_status": "OK" if parsed[r["key"]][0] else "UNPARSEABLE"} for r in rows}
    stats = {"n_pairs": {}, "n_pair_timeouts": {}, "secs_pairs": {}}
    pair_secs = {}
    for variant in params["variants"]:
        pairs = {}
        t0 = time.time()
        nto = 0
        for a in sorted(set(cand_strings) | set(pool_strings)):
            for b in pool_strings:
                if a == b:
                    continue
                t1 = time.time()
                res, to = _with_alarm(params["pair_cap_s"], PT.pair_result, a, b, ent, text=text, variant=variant,
                                      k=params["k"], tau=params["tau"].get(variant))
                if to or res is None:
                    res = _unknown_pair(a, b)
                    nto += 1
                pairs[(a, b)] = res
                pair_secs[(variant, a)] = pair_secs.get((variant, a), 0.0) + time.time() - t1
        stats["n_pairs"][variant] = len(pairs)
        stats["n_pair_timeouts"][variant] = nto
        stats["secs_pairs"][variant] = round(time.time() - t0, 2)
        for r in rows:
            cs = parsed[r["key"]][0]
            o = out_rows[r["key"]]
            if cs is None:
                continue
            P_c = [parsed[p["key"]][0] for p in pool if p["family"] != r["family"] and p["key"] != r["key"]]
            gc_ = PT.graded_consensus(cs, P_c, pairs, ent, return_codes=params.get("codes", True))
            pre = f"{variant}:"
            o[pre + "g_score"] = gc_["g_score"]
            o[pre + "support"] = gc_.get("support")
            o[pre + "coverage"] = gc_.get("coverage")
            o[pre + "c_score_nf"] = gc_.get("c_score_nf")
            o[pre + "n_unknown"] = gc_.get("n_unknown", 0)
            o[pre + "unit_codes"] = gc_.get("unit_codes", [])
            o[pre + "top_code"] = gc_.get("top_code", "NONE")
            o[pre + "n_units"] = gc_.get("n_units")
            o[pre + "units_truncated"] = gc_.get("units_truncated")
            o["n_peers_used"] = gc_["n_peers_used"]
            o["peer_unavailable"] = gc_["peer_unavailable"]
            # k=6 subsample (pool-size check)
            if len(P_c) > 6 and params.get("k6_seeds"):
                vals = []
                for sd in range(params["k6_seeds"]):
                    rng = random.Random(f"k6|{sent['sentence_id']}|{r['key']}|{sd}")
                    sub = rng.sample(P_c, 6)
                    v = PT.graded_consensus(cs, sub, pairs, ent, return_codes=False)["g_score"]
                    if v is not None:
                        vals.append(v)
                o[pre + "g_score_k6"] = sum(vals) / len(vals) if vals else None
            else:
                o[pre + "g_score_k6"] = gc_["g_score"]
            # sensitivity family map (row metadata family field)
            if params.get("famfield", True):
                P_f = [parsed[p["key"]][0] for p in pool if p.get("family_field", p["family"]) != r.get("family_field", r["family"])
                       and p["key"] != r["key"]]
                o[pre + "g_score_famfield"] = PT.graded_consensus(cs, P_f, pairs, ent, return_codes=False)["g_score"]
            if params.get("allpool"):  # sensitivity / exp-C-style pool: every peer except the candidate's own system
                P_a = [parsed[p["key"]][0] for p in pool if p.get("system") != r.get("system") and p["key"] != r["key"]]
                o[pre + "g_score_allpool"] = PT.graded_consensus(cs, P_a, pairs, ent, return_codes=False)["g_score"]
            mi = PT.nf_medoid(P_c, pairs)
            if mi is not None:
                ps = P_c[mi]
                o[pre + "nf_eq_medoid"] = True if ps == cs else pairs[(cs, ps)]["equiv"]
            o[pre + "secs_pairs"] = round(pair_secs.get((variant, cs), 0.0), 3)
    # ---------------- iteration-1 aligner consensus (reference column) + eqmv medoid repair
    if params.get("do_align", True):
        from common import eqmv, medoid_repair  # vendor_c (bound to the dataset-E parser via peer_text)
        eqc = {}
        t0 = time.time()

        def eq(a, b):
            if a == b:
                return True
            k = (a, b) if a < b else (b, a)
            if k not in eqc:
                res, to = _with_alarm(params["pair_cap_s"], eqmv, PT.parse_fol(k[0]), PT.parse_fol(k[1]))
                eqc[k] = None if (to or res is None) else res[0]
            return eqc[k]
        for r in rows:
            cs = parsed[r["key"]][0]
            o = out_rows[r["key"]]
            if cs is None:
                continue
            P_c = [parsed[p["key"]][0] for p in pool if p["family"] != r["family"] and p["key"] != r["key"]]
            if len(P_c) < 2:
                o["c_score_align"] = None
                continue
            eqs = [eq(cs, p) for p in P_c]
            o["c_score_align"] = 1 - sum(e is True for e in eqs) / len(P_c)
            if params.get("allpool"):
                P_a = [parsed[p["key"]][0] for p in pool if p.get("system") != r.get("system") and p["key"] != r["key"]]
                o["c_score_align_allpool"] = (1 - sum(eq(cs, p) is True for p in P_a) / len(P_a)) if len(P_a) >= 2 else None
            deg = [sum(eq(p, q) is True for j, q in enumerate(P_c) if j != i) for i, p in enumerate(P_c)]
            mi = max(range(len(P_c)), key=lambda i: (deg[i], -i))
            o["eqmv_medoid_eq"] = eqs[mi]
            if params.get("medoid_budget_s", 0) > 0:
                if eqs[mi] is True:
                    o["medoid_depth"], o["medoid_ops"] = 0, []
                else:
                    res, to = _with_alarm(int(params["medoid_budget_s"]) + 5, medoid_repair, parsed[r["key"]][1],
                                          PT.parse_fol(P_c[mi]), budget_s=params["medoid_budget_s"])
                    o["medoid_depth"], o["medoid_ops"] = (3, ["TIMEOUT"]) if (to or res is None) else res
        stats["secs_align"] = round(time.time() - t0, 2)
    # ---------------- TEXT side
    if params.get("do_text", True):
        t0 = time.time()
        tcache = {}
        for r in rows:
            cs, e = parsed[r["key"]]
            o = out_rows[r["key"]]
            if cs is None:
                continue
            ts = time.time()
            if r["fol"] not in tcache:
                res, to = _with_alarm(120, PT.text_side, text, e, sent.get("q"), None, True)
                tcache[r["fol"]] = res if res is not None else {"l2_bow": None, "l3_z3": None, "text_timeout": True}
            o.update({k: v for k, v in tcache[r["fol"]].items()})
            # disguised L3 (contamination arm): questionnaire of the disguised text vs the disguised formula
            if r.get("fol_disg") and r.get("q_disg") is not None:
                ed = PT.parse_fol(r["fol_disg"])
                if ed is not None:
                    res, to = _with_alarm(120, PT.l3_z3, r["q_disg"], ed)
                    o["l3_z3_disg"] = None if res is None else res["l3_z3"]
            o["secs_text_row"] = round(time.time() - ts, 3)
        stats["secs_text"] = round(time.time() - t0, 2)
    stats["secs_total"] = round(time.time() - t_all, 2)
    stats["ent"] = dict(ent.stats)
    return {"sentence_id": sent["sentence_id"], "rows": list(out_rows.values()), "stats": stats}
