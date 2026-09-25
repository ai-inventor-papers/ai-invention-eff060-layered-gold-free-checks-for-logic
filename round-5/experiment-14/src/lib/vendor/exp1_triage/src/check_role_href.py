"""Calibration check (known negatives only): L2-role false alarms + role-token resolution on HREF (corrected gold)."""
import json, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fol_triage import role_accounting
from fol import parse
ROOT = Path(__file__).resolve().parent.parent
href = json.loads((ROOT / "href_items.json").read_text())
n = w = r = fa = 0; C = Counter(); ex = []
for h in href:
    try:
        parse(h["candidate_fol"])
    except Exception:
        continue
    ro = role_accounting(h["text"], h["candidate_fol"])
    n += 1; w += ro["n_role_words"]; r += ro["n_resolved"]; fa += ro["flag"]
    C.update(ro["codes"])
    if ro["flag"]:
        ex.append((h["text"][:120], h["candidate_fol"][:120], ro["codes"]))
out = {"n": n, "resolution_rate": r / w, "FA": fa / n, "codes": dict(C), "examples": ex[:40]}
(ROOT / "results" / "role_href_calibration.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print({k: v for k, v in out.items() if k != "examples"})
for e in ex[:25]:
    print(e)
