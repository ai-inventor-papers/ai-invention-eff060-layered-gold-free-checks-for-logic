#!/usr/bin/env python3
"""E's frozen panel_run writes a sentence record even when some of its calls failed (errors list), and then treats the
sentence as done. After every panel sweep, move records with errors to <name>_quarantine_403.jsonl so a resume re-asks
them (successful calls are served from work/panel_cache.jsonl, never re-billed). Writes <WS>/e2b/api_blocked.flag if any
error is the run-budget 403. Usage: quarantine_errors.py panel_heldout.jsonl"""
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
p = ROOT / "work" / sys.argv[1]
rs = [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []
good = [r for r in rs if not r.get("errors")]
bad = [r for r in rs if r.get("errors")]
if bad:
    with open(p.with_name(p.stem + "_quarantine_403.jsonl"), "a") as f:
        for r in bad:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    p.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in good))
blocked = any("aii_run_budget_exhausted" in json.dumps(r.get("errors")) or "HTTP 403" in json.dumps(r.get("errors")) or "HTTP 402" in json.dumps(r.get("errors")) for r in bad)
if blocked:
    (ROOT.parent / "e2b" / "api_blocked.flag").write_text(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
print(json.dumps({"file": p.name, "kept": len(good), "quarantined": len(bad), "api_blocked": blocked}))
