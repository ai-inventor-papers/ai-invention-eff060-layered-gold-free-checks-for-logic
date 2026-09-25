#!/usr/bin/env python3
"""Write work/sentences.json = the first N active sentences in the frozen sha1 order sha1('E2_v1|'+sentence_id),
strata interleaved (L25 -> EXC -> DT round robin). N=0 -> all. Used to run the panel in completed prefixes."""
import hashlib, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
W = ROOT / "work"
act = json.loads((W / "sentences_E2_active.json").read_text())
key = lambda s: hashlib.sha1(("E2_v1|" + s["sentence_id"]).encode()).hexdigest()
by = {st: sorted([s for s in act if s["source_stratum"] == st], key=key) for st in ("L25", "EXC", "DT")}
order = []
i = 0
while any(by.values()):
    for st in ("L25", "EXC", "DT"):
        if by[st]:
            order.append(by[st].pop(0))
n = int(sys.argv[1]) if len(sys.argv) > 1 else 0
sel = order[:n] if n else order
(W / "sentences.json").write_text(json.dumps(sel, ensure_ascii=False, indent=1))
(W / "e2a_order.json").write_text(json.dumps([s["sentence_id"] for s in order]))
print(f"sentences.json <- {len(sel)} of {len(order)}")
