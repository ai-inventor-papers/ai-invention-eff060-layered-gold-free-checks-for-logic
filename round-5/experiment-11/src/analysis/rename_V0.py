#!/usr/bin/env python3
"""V0 rename controls (post-label, $0). For every RENAME_SYN / RENAME_NONCE control of a final-CORRECT E2 row (dataset 3's
frozen perturb.control_rename; z3-equivalent to its parent under the inverse map; text unchanged), score V0 of the
control formula against the SAME family-disjoint peers as its parent (lib.nl2fol_metrics.c_score_align = the frozen eqmv
consensus). Reports: FA = share of controls flagged (V0 > 0.5), base FA = share of their parents flagged, paired flip =
share of (parent, control) pairs whose flag differs. -> results/rename_V0.json"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

WS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WS / "lib"))
import nl2fol_metrics as M  # noqa: E402


def main() -> None:
    cand = [json.loads(l) for l in (WS / "e2" / "candidates_E2_nolabels.jsonl").read_text().splitlines() if l.strip()]
    by_sid = defaultdict(list)
    for r in cand:
        by_sid[r["sentence_id"]].append(r)
    fam = {r["row_key"]: r["family"] for r in cand}
    sc = {json.loads(l)["row_key"]: json.loads(l) for l in (WS / "scores_E2A.jsonl").read_text().splitlines() if l.strip()}
    ctrl = [json.loads(l) for l in (WS / "e2src" / "controls_E2_nolabels.jsonl").read_text().splitlines() if l.strip()]
    rows = []
    for c in ctrl:
        parent = c["control_parent_row_key"]
        ctype = c["row_key"].rsplit("|", 1)[1]
        f = fam[parent]
        peers = [(p["candidate_fol"], p["family"]) for p in by_sid[c["sentence_id"]] if p["row_key"] != parent]
        v = M.c_score_align(c["candidate_fol"], peers, family=f)
        pv = sc[parent]["c_score_align"]
        rows.append({"row_key": c["row_key"], "type": ctype, "stratum": sc[parent]["stratum"], "v0_control": v, "v0_parent": pv})
    out = {"n_controls": len(rows)}
    for t in ("RENAME_SYN", "RENAME_NONCE"):
        rs = [r for r in rows if r["type"] == t and r["v0_control"] is not None and r["v0_parent"] is not None]
        if not rs:
            out[t] = {"n": 0}
            continue
        fc = np.array([r["v0_control"] > 0.5 for r in rs])
        fp = np.array([r["v0_parent"] > 0.5 for r in rs])
        out[t] = {"n": len(rs), "FA_control": float(fc.mean()), "FA_parent_base": float(fp.mean()), "paired_flip": float((fc != fp).mean()),
                  "mean_v0_shift": float(np.mean([r["v0_control"] - r["v0_parent"] for r in rs])),
                  "by_stratum": {s: {"n": int(sum(1 for r in rs if r["stratum"] == s)),
                                     "paired_flip": float(np.mean([(r["v0_control"] > 0.5) != (r["v0_parent"] > 0.5) for r in rs if r["stratum"] == s]))
                                     if any(r["stratum"] == s for r in rs) else None} for s in ("L25", "EXC", "DT")}}
    (WS / "results" / "rename_V0.json").write_text(json.dumps(out, indent=1))
    (WS / "results" / "rename_V0_rows.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
