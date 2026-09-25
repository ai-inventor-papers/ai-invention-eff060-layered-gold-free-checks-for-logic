#!/usr/bin/env python3
"""The user's pilot structural metrics on E2 (label-free, $0), with the FROZEN T1 adaptation (frozen/t1/src/pilot_metrics.py
compute_pilot; T1 method.py stage_cpu document rule): artificial 'documents' = (system, stratum, sha1(sentence_id) % B)
with B = round(#sentences in stratum / 20); story = the other parseable formulas of the document.
Columns (all oriented higher = more suspicious): pilot_joint_conflict (story + cand UNSAT), pilot_arity_incons,
pilot_shape_incons, pilot_dangling, pilot_rerun_jacc (1 - mean predicate-token Jaccard with the other slots on the same
sentence: a cross-system proxy; E2 has one prompt variant). -> cache/pilot_E2.jsonl"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import scoring.guard  # noqa: E402,F401
from scoring.common import CACHE, FROZEN, candidates, jl, setup_log  # noqa: E402

import hashlib  # noqa: E402
import json  # noqa: E402
from collections import defaultdict  # noqa: E402

from loguru import logger  # noqa: E402

sys.path.insert(0, str(FROZEN / "t1"))


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest()


def main() -> None:
    setup_log("pilot_metrics_E2")
    from src.pilot_metrics import compute_pilot
    units = {u["key"]: u for u in jl(CACHE / "units_E2.jsonl")}
    U = [dict(c, parse_ok=units[c["row_key"]]["parse_ok"]) for c in candidates()]
    n_sent = defaultdict(set)
    for u in U:
        n_sent[u["stratum"]].add(u["sentence_id"])
    Bk = {s: max(1, round(len(v) / 20)) for s, v in n_sent.items()}
    docs = defaultdict(list)
    for u in U:
        docs[(u["system"], u["stratum"], int(sha1(u["sentence_id"]), 16) % Bk[u["stratum"]])].append(u)
    rows = []
    for us in docs.values():
        for u in us:
            story = [v["candidate_fol"] for v in us if v["row_key"] != u["row_key"] and v["parse_ok"]]
            rows.append({"key": u["row_key"], "candidate_fol": u["candidate_fol"] if u["parse_ok"] else None,
                         "story_premises_fol": story, "declared_predicates": None, "has_story": True})
    res = compute_pilot(rows, workers=36)
    by_sent = defaultdict(list)
    for u in U:
        by_sent[u["sentence_id"]].append(u)

    def jac(a, b):
        return len(set(a) & set(b)) / max(1, len(set(a) | set(b)))
    out = []
    for u in U:
        p = dict(res.get(u["row_key"], {}))
        mine = p.get("pred_tokens")
        rj = None
        if mine is not None:
            others = [res.get(v["row_key"], {}).get("pred_tokens") for v in by_sent[u["sentence_id"]] if v["slot"] != u["slot"]]
            others = [t for t in others if t is not None]
            if others:
                rj = 1 - sum(jac(mine, t) for t in others) / len(others)
        out.append({"key": u["row_key"], "pilot_joint_conflict": p.get("pilot_joint_conflict"),
                    "pilot_arity_incons": p.get("pilot_arity_incons"), "pilot_shape_incons": p.get("pilot_shape_incons"),
                    "pilot_dangling": p.get("pilot_dangling"), "pilot_rerun_jacc": rj, "pilot_story_unsat": p.get("pilot_story_unsat"),
                    "z3_seconds": p.get("z3_seconds"), "fail_joint": p.get("fail_joint")})
    (CACHE / "pilot_E2.jsonl").write_text("".join(json.dumps(r) + "\n" for r in out))
    logger.info(f"pilot E2: {len(out)} rows; docs {len(docs)} B {Bk}; joint_conflict=1 {sum(1 for r in out if r['pilot_joint_conflict'] == 1)}")


if __name__ == "__main__":
    main()
