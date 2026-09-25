#!/usr/bin/env python3
"""Copy every small (< 12 MB) READ-ONLY input into inputs_copy/<path relative to 3_invention_loop> and write
inputs_manifest.json (source path, sha256, bytes, copied?). Large inputs are referenced by absolute path + sha256."""
from __future__ import annotations

import shutil
from pathlib import Path

from common import DS3, DS5, DS_E, E1, E5, E6, E8, E9, EV2, EV3, MATRIX, PER_ITEM, PERTURB_SCORES, ROOT, RUN, jdump, sha256_file, utc

INPUTS = [
    MATRIX, PER_ITEM, PERTURB_SCORES, E6 / "prereg_T1.json", E6 / "results" / "analysis_T1.json",
    EV2 / "prereg_mech.json", EV2 / "tables" / "m4_fixed_pools_k3.csv", EV2 / "tables" / "m4_auroc_k_cost.csv",
    EV2 / "src" / "consensus_mx.py", EV2 / "src" / "stats.py", EV2 / "src" / "pairwise.py", EV2 / "src" / "mechanism.py",
    EV2 / "vendor_exp5" / "vendor_c" / "common.py", E6 / "src" / "api_bar.py",
    E8 / "results" / "prereg_perturb.json", E8 / "results" / "pairs_E.jsonl", E8 / "src" / "consensus_lib.py",
    E9 / "src" / "analyse.py", EV3 / "src" / "t8_part1.py", EV3 / "tables" / "p1_rule_cuts.csv", EV3 / "tables" / "cost_units.csv",
    DS5 / "src" / "freelab.py", DS5 / "src" / "gloss.py", DS5 / "vendor" / "fol.py", DS5 / "prompts" / "gloss_v1.json",
    DS5 / "full_data_out.json", DS3 / "full_data_out.json", DS_E / "full_data_out.json",
    E5 / "results" / "prereg.json", E5 / "results" / "per_item_E.jsonl",
]
LIMIT = 12 * 1024 ** 2


def main():
    out = {"written_utc": utc(), "limit_bytes": LIMIT, "files": []}
    for p in INPUTS:
        p = Path(p)
        if not p.exists():
            out["files"].append({"source": str(p), "missing": True})
            continue
        rel = p.relative_to(RUN)
        size = p.stat().st_size
        rec = {"source": str(p), "sha256": sha256_file(p), "bytes": size, "copied": size < LIMIT}
        if size < LIMIT:
            dst = ROOT / "inputs_copy" / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, dst)
            rec["copy"] = str(dst.relative_to(ROOT))
        out["files"].append(rec)
    jdump(out, ROOT / "inputs_manifest.json")
    print(f"{sum(f.get('copied', False) for f in out['files'])} copied, {sum(not f.get('copied', True) for f in out['files'])} referenced, "
          f"{sum(f.get('missing', False) for f in out['files'])} missing")


if __name__ == "__main__":
    main()
