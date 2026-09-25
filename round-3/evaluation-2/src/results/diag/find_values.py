"""Discovery helper: print JSON key paths whose numeric value matches a target (used to pin '# source:' key paths)."""
import json, sys
def walk(o, p, out):
    if isinstance(o, dict):
        for k, v in o.items(): walk(v, f"{p}.{k}", out)
    elif isinstance(o, list):
        for i, v in enumerate(o): walk(v, f"{p}[{i}]", out)
    elif isinstance(o, (int, float)) and not isinstance(o, bool):
        out.append((p, o))
f = sys.argv[1]; targets = [float(x) for x in sys.argv[2:]]
out = []; walk(json.load(open(f)), "", out)
for t in targets:
    hits = [(p, v) for p, v in out if abs(v - t) <= 5e-4 * max(1, abs(t))]
    print(t, hits[:6])
