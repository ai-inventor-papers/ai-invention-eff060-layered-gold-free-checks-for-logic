#!/usr/bin/env python3
"""E2 STEP 3 report: panel drift check. Compares today's replay (work/panel_cache.jsonl + work/gate_results.json +
work/trackh_panel_rows.json, produced by E's frozen gate.py with a FRESH cache) with E's STORED votes
(E/work/panel_cache.jsonl for the 77 synthetic gate items; E/work/trackh_panel_rows.json for the 96 track-H pairs).

Stop-rule statistic (pre-registered): majority agreement with E's stored votes over all replayed judgements
(77 gate items + 2 x 96 track-H formulas), majority = >=2 of the 3 members' faithful votes (a 1-1 split with a
missing vote counts as no majority and as a disagreement).  -> panel_drift_E2.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from panel import PROMPT_SHA1  # noqa: E402

E_DIR = Path("../../../../../round-1/dataset-1/src")
MEM = ["P1", "P3", "R1"]


def calib_votes(cache_path: Path) -> dict:
    out: dict = {}
    for line in open(cache_path, encoding="utf-8"):
        r = json.loads(line)
        if r.get("parsed") and r["sentence_id"].startswith("calib|") and r["prompt_sha1"] == PROMPT_SHA1 and r["member"] in MEM:
            for cid, v in r["verdicts"].items():
                key = cid if cid != "REF" else "REF|" + r["sentence_id"]
                out.setdefault(key, {})[r["member"]] = bool(v["faithful"])
    return out


def trackh_votes(rows: list) -> dict:
    out = {}
    for r in rows:
        for m, v in r["votes"].items():
            if m in MEM:
                out.setdefault(f"H{r['id']}:orig", {})[m] = bool(v["orig_faithful"])
                out.setdefault(f"H{r['id']}:corr", {})[m] = bool(v["corr_faithful"])
    return out


def majority(v: dict):
    f = sum(v.values())
    u = len(v) - f
    return True if f >= 2 else (False if u >= 2 else None)


def kappa(a: list, b: list) -> float | None:
    n = len(a)
    if n == 0:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return round((po - pe) / (1 - pe), 4) if pe < 1 else None


def compare(old: dict, new: dict, keys: list) -> dict:
    res = {"n_items": len(keys)}
    for m in MEM:
        pairs = [(old[k][m], new[k][m]) for k in keys if m in old.get(k, {}) and m in new.get(k, {})]
        res[f"agreement_{m}"] = round(sum(x == y for x, y in pairs) / len(pairs), 4) if pairs else None
        res[f"n_{m}"] = len(pairs)
    mo = [majority(old.get(k, {})) for k in keys]
    mn = [majority(new.get(k, {})) for k in keys]
    res["majority_agreement"] = round(sum(x == y and x is not None for x, y in zip(mo, mn)) / len(keys), 4) if keys else None
    res["n_no_majority_old"] = sum(x is None for x in mo)
    res["n_no_majority_new"] = sum(x is None for x in mn)
    done = [i for i, k in enumerate(keys) if len(new.get(k, {})) >= 2]
    res["n_replayed_with_>=2_new_votes"] = len(done)
    res["majority_agreement_on_replayed_items"] = round(sum(mo[i] == mn[i] and mo[i] is not None for i in done) / len(done), 4) if done else None
    return res


def main():
    old_c = calib_votes(E_DIR / "work" / "panel_cache.jsonl")
    new_c = calib_votes(ROOT / "work" / "panel_cache.jsonl")
    items = json.loads((ROOT / "work" / "calibration_items.json").read_text())
    gate_keys = [it["calib_id"] for it in items]
    ref_keys = sorted(k for k in old_c if k.startswith("REF|"))
    old_h = trackh_votes(json.loads((E_DIR / "work" / "trackh_panel_rows.json").read_text()))
    new_rows = json.loads((ROOT / "work" / "trackh_panel_rows.json").read_text())
    new_h = trackh_votes(new_rows)
    h_keys = sorted(set(old_h) | set(new_h))
    old_all, new_all = {**old_c, **old_h}, {**new_c, **new_h}
    all_keys = gate_keys + h_keys
    comb = compare(old_all, new_all, all_keys)
    g_old = json.loads((ROOT / "E_ref" / "gate_results.json").read_text())
    g_new = json.loads((ROOT / "work" / "gate_results.json").read_text())
    # Cohen kappa P3-R1 over all replayed judgements where both voted (today and, for reference, E)
    def k_p3r1(v):
        ks = [k for k in all_keys if "P3" in v.get(k, {}) and "R1" in v.get(k, {})]
        return kappa([v[k]["P3"] for k in ks], [v[k]["R1"] for k in ks]), len(ks)
    kn, nn = k_p3r1(new_all)
    ko, no = k_p3r1(old_all)
    stat = comb["majority_agreement"]
    complete = comb["n_replayed_with_>=2_new_votes"] == len(all_keys)
    rep = {
        "status": "COMPLETE" if complete else "INCOMPLETE: the replay was cut off by the run-level OpenRouter budget stop (HTTP 403 aii_run_budget_exhausted); items without >=2 new votes are unreplayed, not disagreements",
        "stop_rule_decision": ("PASS" if stat >= 0.85 else "STOP") if complete else "UNDECIDED (replay incomplete); on the replayed items the majority agreement is " + str(comb["majority_agreement_on_replayed_items"]),
        "stop_rule": "panel NOT used for E2 if combined majority agreement with E's stored votes < 0.85 or a panel model id is no longer served",
        "combined_majority_agreement_all_items": stat,
        "combined_majority_agreement_replayed_items": comb["majority_agreement_on_replayed_items"],
        "passes": bool(complete and stat is not None and stat >= 0.85),
        "combined": comb,
        "synthetic_gate_77": compare(old_c, new_c, gate_keys),
        "synthetic_gate_reference_items": compare(old_c, new_c, ref_keys),
        "trackh_192_judgements": compare(old_h, new_h, h_keys),
        "gate_balanced_accuracy": {m: {"today": g_new["synthetic"][m]["balanced_accuracy"], "E": g_old["synthetic"][m]["balanced_accuracy"],
                                       "today_passes_gate": g_new["synthetic"][m]["passes_gate"]} for m in MEM},
        "trackh_majority_vs_experts": {"today": g_new["trackh"]["per_model"]["majority"], "E": g_old["trackh"]["per_model"]["majority"]},
        "trackh_per_member_vs_experts": {m: {"today": g_new["trackh"]["per_model"][m], "E": g_old["trackh"]["per_model"][m]} for m in MEM},
        "cohen_kappa_P3_R1": {"today": kn, "n_today": nn, "E_stored": ko, "n_E": no},
        "cache": "fresh work/panel_cache.jsonl (created empty for E2); no E reply could be served",
    }
    (ROOT / "panel_drift_E2.json").write_text(json.dumps(rep, indent=1))
    print(json.dumps({k: rep[k] for k in ("status", "stop_rule_decision", "combined_majority_agreement_replayed_items", "passes", "gate_balanced_accuracy", "trackh_majority_vs_experts", "cohen_kappa_P3_R1")}, indent=1))


if __name__ == "__main__":
    main()
