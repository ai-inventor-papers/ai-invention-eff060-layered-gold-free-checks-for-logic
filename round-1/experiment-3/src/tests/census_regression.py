"""T0 census regression: re-run repair_census.work() under the fixed ⊕ precedence on 20 curated rows (sorted by
(src, id)) plus every row whose formulas contain ⊕, and compare with the recorded iter-3 class.
Only ⊕ rows may change (F7: stop if more than 3 non-⊕ rows change)."""
import json
import multiprocessing as mp
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.setrecursionlimit(10000)


def run(r):
    from repair_census import work
    rec = work((r["src"], r["id"], r["nl"], r["old"], r["new"], "True" if r["ambiguous"] else "False"))
    return r["id"], r["src"], r["cls"], (rec or {}).get("cls", "EQUIV"), ("⊕" in r["old"] or "⊕" in r["new"])


if __name__ == "__main__":
    rows = json.loads((ROOT / "data" / "repair_census.rows.json").read_text())
    rows.sort(key=lambda r: (r["src"], str(r["id"])))
    xor = [r for r in rows if "⊕" in r["old"] or "⊕" in r["new"]]
    plain = [r for r in rows if r not in xor][:20]
    with mp.get_context("spawn").Pool(4) as pool:
        res = pool.map(run, plain + xor, chunksize=1)
    out = [{"id": i, "src": s, "old_cls": a, "new_cls": b, "has_xor": x, "changed": a != b} for i, s, a, b, x in res]
    n_plain_changed = sum(o["changed"] and not o["has_xor"] for o in out)
    n_xor_changed = sum(o["changed"] and o["has_xor"] for o in out)
    summary = {"n_plain": len(plain), "n_xor": len(xor), "plain_changed": n_plain_changed, "xor_changed": n_xor_changed,
               "F7_stop": n_plain_changed > 3, "rows": out}
    (ROOT / "results" / "census_regression.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print(json.dumps({k: v for k, v in summary.items() if k != "rows"}))
    for o in out:
        if o["changed"]:
            print(o)
