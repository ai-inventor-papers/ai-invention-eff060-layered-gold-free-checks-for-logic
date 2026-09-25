#!/usr/bin/env python3
"""Copy every small (<10 MB) input this artifact reads into ./inputs_copy/ (self-contained record) and write
tables/source_hashes.csv: sha256 of each vendored exp-5 file and of every input (large inputs are referenced by absolute
path, not copied)."""
from __future__ import annotations

import glob
import shutil
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from paths import DS2, DS3, DS_E, E5, E6, EV1, I1, REVIEW, ROOT, sha256_file  # noqa: E402

LIMIT = 10 * 1024 * 1024
INPUTS = [E5 / "results/per_item_E.jsonl", E5 / "data/E_labels.jsonl", E5 / "data/E_blind.jsonl", E5 / "results/prereg.json",
          E5 / "results/tables.md", E5 / "results/analysis.json", E5 / "results/p_tests.json", E5 / "results/deviations.json",
          E5 / "results/screen_fit.json", E5 / "results/posthoc_nf_fusion.json", E5 / "results/budget_state.json",
          E5 / "results/costs.jsonl", E5 / "results/E_l3_q.jsonl", E5 / "README.md",
          E6 / "full_method_out.json", E6 / "folds_E.json", E6 / "results/summary.md", E6 / "results/analysis_E.json",
          E6 / "results/b2_gate.json", E6 / "results/b2_think_diagnostic.json", E6 / "results/s4_coefs.json",
          E6 / "results/budget_state.json", E6 / "results/retest_vs_sibling.json", E6 / "README.md",
          DS2 / "gate_report.json", DS2 / "radj_card.md", DS2 / "prereg_radj.json", DS2 / "cost_ledger.jsonl",
          DS3 / "full_data_out.json", DS3 / "dataset_card.md", DS3 / "prereg_rcomp.json", DS3 / "TODO.md", DS3 / "cost_ledger.jsonl",
          DS_E / "full_data_out.json", DS_E / "raw/generations.jsonl", DS_E / "dataset_card.md",
          REVIEW / "audit/pt_vs_s4.py", REVIEW / "audit/pt_vs_s4.json",
          I1 / "experiment-4/src/results/method_out.json", I1 / "experiment-1/src/results/metrics.json",
          I1 / "experiment-1/src/src/fol_triage.py"]
INPUTS += [Path(p) for p in sorted(glob.glob(str(EV1 / "tables/*.csv")))]
INPUTS += [Path(p) for p in sorted(glob.glob(str(I1 / "experiment-3/src/src/*.py")))]


def main():
    out = ROOT / "inputs_copy"
    out.mkdir(exist_ok=True)
    rows = []
    for p in INPUTS:
        if not p.exists():
            rows.append({"kind": "input", "path": str(p), "sha256": "MISSING", "bytes": 0, "copied_to": ""})
            continue
        rel = p.relative_to(ROOT.parents[3])  # relative to 3_invention_loop
        dst = ""
        if p.stat().st_size < LIMIT:
            d = out / rel
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, d)
            dst = str(d.relative_to(ROOT))
        rows.append({"kind": "input", "path": str(p), "sha256": sha256_file(p), "bytes": p.stat().st_size, "copied_to": dst})
    for p in sorted((ROOT / "vendor_exp5").rglob("*.py")):
        src = E5 / "src" / p.relative_to(ROOT / "vendor_exp5")
        rows.append({"kind": "vendored_exp5_src", "path": str(p.relative_to(ROOT)), "sha256": sha256_file(p), "bytes": p.stat().st_size,
                     "copied_to": f"identical_to_source={src.exists() and sha256_file(src) == sha256_file(p)}"})
    pd.DataFrame(rows).to_csv(ROOT / "tables" / "source_hashes.csv", index=False)
    print(f"{sum(r['kind'] == 'input' for r in rows)} inputs, {sum(bool(r['copied_to']) and r['kind'] == 'input' for r in rows)} copied")


if __name__ == "__main__":
    main()
