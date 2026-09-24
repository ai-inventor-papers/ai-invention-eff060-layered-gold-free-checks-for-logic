#!/usr/bin/env python3
"""Final checks (testing plan item 14 + 5):
- the prereg's git commit time precedes the first gloss-call ledger entry;
- results/cost_ledger.jsonl = labeller ledger + the probe ledger; its total is <= $4 and equals the sum of per-call usd;
- every tables.md table has a '# source:' line;
- the deviation ids D10..D24 are present.
Writes results/final_checks.json."""
from __future__ import annotations

import json
import subprocess
from collections import defaultdict

from cc import LAB, LOGS, RES, WS, dump, jl


def main() -> None:
    out = {}
    log = subprocess.run(["git", "log", "--format=%cI %s", "--reverse"], cwd=WS, capture_output=True, text=True).stdout.splitlines()
    pre = next((l.split()[0] for l in log if "Prereg + score seal" in l), None)
    led = jl(LAB / "cost_ledger.jsonl")
    gloss_calls = [r["utc"] for r in led if r.get("phase", "").startswith(("gloss_pilot", "gate_gloss", "free_gloss")) and r.get("usd", 0) > 0]
    first = min(gloss_calls) if gloss_calls else None
    out["prereg_commit_utc"] = pre
    out["first_gloss_call_utc"] = first
    out["prereg_before_first_gloss_call"] = bool(pre and first and pre.replace("+00:00", "Z") < first)
    probe = jl(LOGS / "probe_ledger.jsonl")
    allrows = led + probe
    with (RES / "cost_ledger.jsonl").open("w") as fh:
        for r in allrows:
            fh.write(json.dumps(r) + "\n")
    tot = sum(float(r.get("usd", 0.0)) for r in allrows)
    by = defaultdict(float)
    for r in allrows:
        by[r.get("phase", "?")] += float(r.get("usd", 0.0))
    last_cum = max((r.get("cum_usd", 0.0) for r in led), default=0.0)
    out["ledger_total_usd"] = round(tot, 6)
    out["ledger_by_phase_usd"] = {k: round(v, 6) for k, v in by.items()}
    out["ledger_last_cum_usd"] = last_cum
    out["ledger_total_le_4"] = tot <= 4.0
    out["ledger_all_per_call_usd_nonneg"] = all(float(r.get("usd", 0.0)) >= 0 for r in allrows)
    out["ledger_cum_note"] = ("cum_usd is a per-process running total (the audit and frontier processes ran concurrently), so the "
                              "authoritative total is the sum of per-call usd above")
    tm = (RES / "tables.md").read_text().split("\n## ")[1:]
    out["tables_n"] = len(tm)
    out["tables_all_have_source"] = all("# source:" in t.split("\n")[1] for t in tm)
    dv = {d["id"] for d in json.loads((RES / "deviations.json").read_text())["deviations"]}
    out["deviations_present"] = all(f"D{i}" in dv for i in range(10, 27))
    out["ALL_PASS"] = all(v for k, v in out.items() if isinstance(v, bool))
    dump(RES / "final_checks.json", out)
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
