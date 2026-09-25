#!/usr/bin/env python3
"""SANITY SIGNALS (testing plan): for every PERTURB control of an E base, the share of the base's endorsers (peers with
hyb_eq True for the unmutated base) that also agree with the control, per control type and mode. z3-equivalent controls
(CONTRAPOSITIVE, REORDER_*, DEMORGAN) must keep >= 95% (else the rewrite/parse path is broken); rename controls measure
how much each mode's agreement survives renaming. Also: UNKNOWN share of pair verdicts on PERTURB rows.
Writes results/sanity_checks.json."""
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
R = ROOT / "results"
rows = {r["item_id"]: r for r in (json.loads(l) for l in (ROOT / "data/perturb_rows.jsonl").read_text().splitlines())}
P = defaultdict(dict)
n_unk = defaultdict(lambda: [0, 0])
with (R / "pairs_E.jsonl").open() as fh:
    for l in fh:
        p = json.loads(l)
        if p["cand"].startswith(("PT:", "PB:")):
            P[p["cand"]][p["peer"]] = p
            for m in ("align_eq", "nf_eq", "hyb_eq"):
                n_unk[m][0] += p[m] is None
                n_unk[m][1] += 1
out = {"unknown_share_perturb_pairs": {m: a / b for m, (a, b) in n_unk.items()}, "controls": {}}
agg = defaultdict(lambda: defaultdict(lambda: [0, 0]))
for iid, r in rows.items():
    if r["fold"] != "PERTURB_CONTROL":
        continue
    c, b = P.get("PT:" + iid), P.get("PB:" + r["base_item_id"])
    if not c or not b:
        continue
    for m in ("align_eq", "nf_eq", "hyb_eq"):
        end = [q for q, v in b.items() if v[m] is True]
        agg[r["control_type"]][m][0] += sum(1 for q in end if c.get(q, {}).get(m) is True)
        agg[r["control_type"]][m][1] += len(end)
for ct, d in agg.items():
    out["controls"][ct] = {m: {"kept": k, "endorsers": n, "share": k / n if n else None} for m, (k, n) in d.items()}
eq_types = ("CONTRAPOSITIVE", "REORDER_COMMUTE", "REORDER_QUANT", "DEMORGAN")
k = sum(agg[t]["hyb_eq"][0] for t in eq_types if t in agg)
n = sum(agg[t]["hyb_eq"][1] for t in eq_types if t in agg)
out["equivalent_controls_hyb_kept_share"] = k / n if n else None
out["sanity_pass_>=0.95"] = bool(n and k / n >= 0.95)
(R / "sanity_checks.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
