#!/usr/bin/env python3
"""Union with the E2-B sibling (plan STEP 5(k)). Polls <iter_5>/gen_art/*/e2b/E2B_FINAL_READY.json (token
'aii_iter5_e2b_final_v1') until the deadline, checks the token and the per-row file's sha256, then:
  * UNION long pool: R_AB rows of E2-A long pool (L25, EXC) + E2-B (L25), strata {L25_E2A, L25_E2B, EXC}; strat AUROC
    Delta(c_score_align - judge_cheap_disg) with a stratified sentence-cluster bootstrap over the sentences of both sets;
  * inverse-variance meta-analysis of the two independent Deltas (E2-A long pool, E2-B L25); heterogeneity
    Delta_E2A - Delta_E2B with a normal CI.
A sentence labelled by both artifacts counts ONCE, taking E2-B's copy (contract). -> results/union_longpool.json
Usage: python analysis/union_E2B.py --deadline-utc 2026-09-24T16:27:00Z [--once]"""
from __future__ import annotations

import argparse
import datetime as dt
import glob
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

WS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WS / "analysis"))
from analyse_E2A import B, Data, cell_eval, jl  # noqa: E402

TOKEN = "aii_iter5_e2b_final_v1"
PAT = str(WS.parent / "*" / "e2b" / "E2B_FINAL_READY.json")


def find_marker():
    for p in glob.glob(PAT):
        try:
            m = json.loads(Path(p).read_text())
        except (json.JSONDecodeError, OSError):
            continue
        if m.get("token") == TOKEN:
            return Path(p), m
    return None, None


def per_row_path(mp: Path, m: dict) -> Path:
    for k in ("per_row_file", "per_row_path", "path", "file"):
        if m.get(k):
            p = Path(m[k])
            return p if p.is_absolute() else mp.parent.parent / p
    raise KeyError("no per-row path in marker")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--deadline-utc", required=True)
    ap.add_argument("--once", action="store_true")
    a = ap.parse_args()
    deadline = dt.datetime.fromisoformat(a.deadline_utc.replace("Z", "+00:00")).timestamp()
    log = WS / "logs" / "e2b_marker_polls.jsonl"
    while True:
        mp, m = find_marker()
        with log.open("a") as f:
            f.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "found": bool(mp)}) + "\n")
        if mp or a.once or time.time() > deadline:
            break
        time.sleep(300)
    out = {"marker": str(mp) if mp else None}
    if not mp:
        out["status"] = "E2B_ABSENT at the deadline: union computed by E2-B (contract)"
        (WS / "results" / "union_longpool.json").write_text(json.dumps(out, indent=1))
        print(out["status"])
        return
    pr = per_row_path(mp, m)
    sha = hashlib.sha256(pr.read_bytes()).hexdigest()
    exp = m.get("sha256") or m.get("per_row_sha256")
    out["sha256_ok"] = (sha == exp)
    assert out["sha256_ok"], f"E2-B per-row sha mismatch {sha} vs {exp}"
    A = [r for r in jl(WS / "per_item_E2A.jsonl") if r["stratum"] in ("L25", "EXC")]
    Bv = jl(pr)
    b_sids = {r["sentence_id"] for r in Bv}
    A = [r for r in A if r["sentence_id"] not in b_sids]  # collisions: E2-B's copy wins
    rows = []
    for r in A:
        rr = dict(r)
        rr["stratum"] = "L25_E2A" if r["stratum"] == "L25" else "EXC"
        rows.append(rr)
    for r in Bv:
        if r.get("stratum", "L25") not in ("L25", "L25_E2B"):
            continue
        rows.append({"row_key": r["row_key"], "sentence_id": "B|" + r["sentence_id"], "stratum": "L25_E2B",
                     "label": r.get("label"), "label_tier": r.get("label_tier", r.get("tier")),
                     "reading_choice": bool(r.get("reading_choice")),
                     "c_score_align": r.get("c_score_align", r.get("V0")),
                     "judge_cheap_disg": r.get("judge_cheap_disg", r.get("flashlite_disg")),
                     "judge_cheap_orig": r.get("judge_cheap_orig", r.get("flashlite_orig"))})
    D = Data(rows)
    mets = {k: D.col(k) for k in ("c_score_align", "judge_cheap_disg", "judge_cheap_orig")}
    U = cell_eval(D, D.regime["R_AB"], mets, [("c_score_align", "judge_cheap_disg"), ("c_score_align", "judge_cheap_orig")])
    out["union_long_pool"] = U
    dA = json.loads((WS / "results" / "auroc_cells.json").read_text())["R_AB"]["LONG (L25+EXC)"]["deltas"].get("c_score_align - judge_cheap_disg")
    DB = Data([r for r in rows if r["stratum"] == "L25_E2B"])
    dB = cell_eval(DB, DB.regime["R_AB"], {k: DB.col(k) for k in ("c_score_align", "judge_cheap_disg")},
                   [("c_score_align", "judge_cheap_disg")])["deltas"].get("c_score_align - judge_cheap_disg")
    if dA and dB and dA.get("ci") and dB.get("ci") and None not in dA["ci"] and None not in dB["ci"]:
        seA = (dA["ci"][1] - dA["ci"][0]) / 3.919928
        seB = (dB["ci"][1] - dB["ci"][0]) / 3.919928
        w = np.array([1 / seA ** 2, 1 / seB ** 2])
        est = float((w * np.array([dA["delta"], dB["delta"]])).sum() / w.sum())
        se = float(1 / np.sqrt(w.sum()))
        het = dA["delta"] - dB["delta"]
        hse = float(np.sqrt(seA ** 2 + seB ** 2))
        out["meta_ivw"] = {"delta_E2A_long": dA["delta"], "se_E2A": seA, "delta_E2B_L25": dB["delta"], "se_E2B": seB,
                           "ivw_delta": est, "ivw_ci": [est - 1.959964 * se, est + 1.959964 * se],
                           "heterogeneity_delta_A_minus_B": het, "het_ci": [het - 1.959964 * hse, het + 1.959964 * hse]}
    out["note"] = ("The label regime (the panel) is shared by E2-A and E2-B: the union adds SAMPLING power, not label-regime "
                   "independence.")
    (WS / "results" / "union_longpool.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps({k: v for k, v in out.items() if k != "union_long_pool"}, indent=1, default=str))


if __name__ == "__main__":
    main()
