#!/usr/bin/env python3
"""Runner for E2's frozen panel-side scripts with PINNED providers (M2 protocol) and the D1 shim.
Reads <WS>/e2b/drift_decision.json {"pins": {"P1": ["Provider"], ...}} (written by the marker poller or by our own
drift gate) and adds provider={order: [...], allow_fallbacks: false} to panel.MEMBERS[m]['params'] for every pinned
member, BEFORE the frozen script runs. The panel cache key (sentence|model|prompt sha|class ids) is unaffected.
Usage: pe.py <src script.py | src_e2/repair.py> [args...]"""
import json
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WS = ROOT.parent
sys.path.insert(0, str(ROOT / "src_e2"))
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "labeller"))
from compat import install  # noqa: E402

install()
import panel  # noqa: E402

dec = json.loads((WS / "e2b" / "drift_decision.json").read_text())
for m, order in (dec.get("pins") or {}).items():
    if m in panel.MEMBERS and order:
        panel.MEMBERS[m]["params"]["provider"] = {"order": list(order), "allow_fallbacks": False}
print(f"pins applied: { {m: panel.MEMBERS[m]['params'].get('provider') for m in ('P1', 'P3', 'R1')} }", flush=True)
script = sys.argv[1]
path = ROOT / script if "/" in script else ROOT / "src" / script
sys.argv = [str(path)] + sys.argv[2:]
if script.endswith("repair.py"):
    import asyncio
    import repair_refs  # noqa: E402
    cap = float(sys.argv[sys.argv.index("--cap") + 1]) if "--cap" in sys.argv else 1.0
    asyncio.run(repair_refs.main(cap=cap))
else:
    runpy.run_path(str(path), run_name="__main__")
