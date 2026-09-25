#!/usr/bin/env python3
"""Testing plan 9 (code test on SYNTHETIC rows, never a result): union.py's duplicate rule (a sentence present in both
samples counts once, E2-B's copy kept, kappa reported) and the fixed-sequence bookkeeping run end to end.
Run: exp5src/.venv/bin/python tests/test_union_synthetic.py"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

WS = Path(__file__).resolve().parents[1]
TMP = WS / "tests" / "tmp"
TMP.mkdir(parents=True, exist_ok=True)
rng = np.random.default_rng(0)


def rows(sample, sids, stratum):
    out = []
    for sid in sids:
        for slot in ("G1", "G2", "G3", "G4", "G5", "G6"):
            y = int(rng.random() < 0.6)
            out.append({"row_key": f"{sid}|{slot}", "sentence_id": sid, "stratum": stratum, "label": "ERROR" if y else "CORRECT", "tier": "A",
                        "reading_choice": False, "V0": float(np.clip(0.5 * y + rng.normal(0.3, 0.25), 0, 1)),
                        "flashlite_disg": float(np.clip(0.3 * y + rng.normal(0.3, 0.3), 0, 1)), "flashlite_orig": float(rng.random()),
                        "nano_orig": float(rng.random()), "words": 27, "word_bin": "25-29", "in_R_AB": True, "label_regime": "PASS"})
    return out


a = rows("E2A", [f"a{i}" for i in range(40)] + ["dup1"], "L25") + rows("E2A", [f"e{i}" for i in range(20)], "EXC")
b = rows("E2B", [f"b{i}" for i in range(40)] + ["dup1"], "L25_E2B")
(TMP / "a.jsonl").write_text("".join(json.dumps(r) + "\n" for r in a))
(TMP / "b.jsonl").write_text("".join(json.dumps(r) + "\n" for r in b))
r = subprocess.run([sys.executable, str(WS / "src" / "union.py"), "--e2a", str(TMP / "a.jsonl"), "--e2b", str(TMP / "b.jsonl"), "--B", "50",
                    "--out", str(TMP / "union_test.json")], capture_output=True, text=True)
assert r.returncode == 0, r.stderr[-2000:]
u = json.loads((TMP / "union_test.json").read_text())
assert u["duplicates"]["n_sentences"] == 1 and u["duplicates"]["n_rows_matched"] == 6, u["duplicates"]
n_long = u["fixed_sequence"]["results"]["U1_long_pool_V0_minus_flashlite_disg"]["n"]
assert n_long == (40 + 20) * 6 + 41 * 6, n_long  # E2-A's dup1 rows dropped, E2-B's kept
assert "L25_all_bins" in u["heterogeneity"] and "long_pool" in u["meta_analysis_fixed_effect"]
print("union synthetic test PASSED", u["duplicates"], u["fixed_sequence"]["verdicts"])
