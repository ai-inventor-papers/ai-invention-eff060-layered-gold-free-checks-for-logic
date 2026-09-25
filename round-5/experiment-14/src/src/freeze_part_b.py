#!/usr/bin/env python3
"""B7: freeze/gg_gate.json + atomic M1 update (GG part only; V fields untouched)."""
from __future__ import annotations

import hashlib
import json

from common import FREEZE, RES, ROOT, atomic_write, jdump, sha256_file, utc

BOUNDARY = ("rename non-invariance of consensus is a measured boundary: c_align PERTURB NONCE/SYN FA 0.765/0.565, paired flips "
            "0.327/0.182; 9-peer ΔFA +0.273")


def main():
    D = json.loads((RES / "gg_dev.json").read_text())
    pre = json.loads((ROOT / "prereg_gg.json").read_text())
    g2 = json.loads((RES / "prompt_gg_v2.json").read_text())
    psha = hashlib.sha256(json.dumps(g2, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    st = D["gates"]["GG_status"]
    failed = [k for k in ("g1", "g2", "g3", "checker") if not D["gates"][k]["pass"]]
    gate = {"status": st if st == "PASS" else f"FAIL({','.join(failed)})", "gates": D["gates"],
            "checker_model": pre["checker"]["model"], "checker_provider": "Google (OpenRouter; reasoning max_tokens 0, 0 reasoning tokens)",
            "prompt": g2["version"], "prompt_sha256": psha, "prompt_revision": json.loads((ROOT / "prompt_revision_v2.json").read_text()),
            "caps": pre["map_family"]["caps"], "map_family": pre["map_family"]["PRIMARY"],
            "E_headline": {k: D["auroc"][k] for k in ("ALL-strat", "LONG-strat", "L25")},
            "why_it_fails": ("GG lowers e in every T9 class (MEANING_RENAME-type 0.502 -> 0.224; ALL 0.140 -> 0.081) but raises d "
                             "(ALL 0.490 -> 0.629; L25 0.811 -> 0.960): bijective symbol maps cannot bridge granularity/decomposition "
                             "differences that eqmv accepts: of the 946 eqmv-accepted node pairs that GG does not accept, all 678 kind=gran pairs "
                             "fail the arity-multiset prefilter and 268 kind=align pairs are gloss-rejected, so correct candidates lose support. g1/g2 pass only trivially: base FA is "
                             "0.83 (c > 0.5), so recall ~1 and flips are bounded by the already-flagged bases."),
            "written_utc": utc()}
    if st != "PASS":
        gate["boundary"] = BOUNDARY
    jdump(gate, FREEZE / "gg_gate.json")
    m1p = FREEZE / "CONSENSUS_FREEZE_READY.json"
    m1 = json.loads(m1p.read_text())
    m1["GG"] = {"status": gate["status"], "gg_sha256": sha256_file(FREEZE / "gg.py"), "gg_gate_sha256": sha256_file(FREEZE / "gg_gate.json"),
                "checker_model": gate["checker_model"], "prompt_sha": psha, "updated_utc": utc()}
    m1["files"]["gg"] = "freeze/gg.py"
    m1["files"]["gg_gate"] = "freeze/gg_gate.json"
    m1["files"]["gg_dev"] = "results/gg_dev.json"
    atomic_write(m1p, json.dumps(m1, indent=1))
    print(json.dumps(m1["GG"], indent=1))


if __name__ == "__main__":
    main()
