"""T0: census on track-H pairs with the fixed parser vs iter-3 repair_census.rows.json. T1: L1 / L2-bow FA on corrected gold."""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fol_triage import fol_lint, content_accounting

ROOT = Path(__file__).resolve().parent.parent
items = json.loads((ROOT / "screen_items.json").read_text())
H = [x for x in items if x["track"] == "H"]
old = {(r["src"], str(r["id"])): r["cls"] for r in json.loads((ROOT / "data/iter3_repair_census.rows.json").read_text())}
out = {"T0": {}, "T1": {}}
diff = []
new_cls = Counter()
for x in H:
    src = "MALLS" if x["role"] == "MALLS" else "FOLIO-concl"
    iid = x["story_id"].replace("malls_", "") if src == "MALLS" else x["story_id"]
    o = old.get((src, iid))
    n = x["auto_class"]
    if n not in ("EQUIV", "UNPARSEABLE", "REF_UNPARSEABLE"):
        new_cls["VOCAB/GRAN" if n in ("VOCAB", "GRAN") else "COMPOUND" if n == "COMPOUND" else "repaired"] += 1
    if o is not None and o != n:
        diff.append({"id": x["story_id"], "iter3": o, "now": n, "cand": x["candidate_fol"], "ref": x["reference_fol"]})
    if o is None and n not in ("EQUIV", "UNPARSEABLE", "REF_UNPARSEABLE"):
        diff.append({"id": x["story_id"], "iter3": None, "now": n})
out["T0"] = {"iter3_counts": dict(Counter("VOCAB/GRAN" if c in ("VOCAB", "GRAN") else "COMPOUND" if c == "COMPOUND"
                                          else "repaired" for c in old.values())),
             "now_counts": dict(new_cls), "n_changed": len(diff), "changes": diff}
fa = Counter(); n = 0; bow = Counter(); items_fa = []
seen = set()
for x in H:
    ref = x["reference_fol"]
    if ref in seen:
        continue
    seen.add(ref)
    l1 = fol_lint(ref)
    if not l1["parse_ok"]:
        continue
    n += 1
    fa["ANY"] += bool(l1["codes"]); fa["z3_unknown"] += l1["z3_unknown"]
    for c in l1["codes"]:
        fa[c] += 1
    if l1["codes"]:
        items_fa.append({"text": x["text"], "fol": ref, "codes": l1["codes"]})
    b = content_accounting(x["text"], ref)
    bow["unanchored>=1"] += b["n_unanchored"] >= 1; bow["uncarried>0.34"] += b["uncarried_frac"] > 0.34; bow["flag"] += b["flag"]
out["T1"] = {"n_parseable_corrected_gold": n, "l1_fa": dict(fa), "l1_fa_rate": fa["ANY"] / n, "l1_fa_items": items_fa,
             "bow": dict(bow), "bow_rates": {k: v / n for k, v in bow.items()},
             "iter3_reference": "L1 5/294 = 1.7%; unanchored FA 5-7%"}
(ROOT / "results" / "t0_t1_checks.json").write_text(json.dumps(out, ensure_ascii=False, indent=1))
print(json.dumps({"T0": {k: v for k, v in out["T0"].items() if k != "changes"}, "T1": {k: v for k, v in out["T1"].items() if k != "l1_fa_items"}}, indent=1))
for d in diff[:40]:
    print(d["id"], d["iter3"], "->", d["now"])
