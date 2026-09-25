#!/usr/bin/env python3
"""Finite-model prefilter audit (testing plan 3): 500 random (premise, unit) pairs built from screen pools (peer aligned into
the candidate's vocabulary by the iteration-1 aligner; units of the candidate and of the peer). A prefilter 'False'
(countermodel found) must NEVER coincide with z3 'True' (0 tolerance). Reports hit rate and speed-up.
Writes results/prefilter_audit.json."""
import json
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import peer_text as PT  # noqa: E402
from screen_fit import build_pools  # noqa: E402
from repair_census import align  # noqa: E402

items = json.loads((ROOT / "data" / "screen" / "screen_items.json").read_text())
pools = build_pools(items)
rng = random.Random(20260923)
keys = sorted(pools)
pairs = []
while len(pairs) < 500:
    t = pools[keys[rng.randrange(len(keys))]]["members"]
    if len(t) < 2:
        continue
    a, b = rng.sample(sorted(t), 2)
    ea, eb = PT.parse_fol(t[a]), PT.parse_fol(t[b])
    if ea is None or eb is None:
        continue
    br = align(eb, ea)[0]
    prem, prem_s = br, PT.canon(br)
    us = PT.units_of(PT.canon(ea))[0]
    pairs.append((prem_s, us[rng.randrange(len(us))]))
conf = fm_false = z3_true = unk = 0
t_fm = t_z3 = 0.0
for p, u in pairs:
    t0 = time.time(); r_fm = PT.fm_refutes(p, u); t_fm += time.time() - t0
    t0 = time.time(); r_z = PT.z3_entails(PT.parse_fol(p), PT.parse_fol(u), 2000); t_z3 += time.time() - t0
    fm_false += r_fm
    z3_true += r_z is True
    unk += r_z is None
    conf += bool(r_fm and r_z is True)
out = {"n_pairs": len(pairs), "prefilter_refuted": fm_false, "z3_true": z3_true, "z3_unknown": unk, "conflicts_fm_false_z3_true": conf,
       "prefilter_hit_rate": fm_false / len(pairs), "secs_fm_total": t_fm, "secs_z3_total": t_z3}
(ROOT / "results" / "prefilter_audit.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out))
assert conf == 0
