#!/usr/bin/env python3
"""E2 STEP 8 ($0): RENAME_SYN / RENAME_NONCE controls from dataset 3's frozen perturb.control_rename.

Base rows: up to 300 final-CORRECT LLM rows (not reading_choice), tier A first then tier B (control_base_tier), spread
over strata round-robin (L25, EXC, DT), sha1('E2_ctrl|'+row_key) order within stratum.
RENAME_SYN: control_rename as frozen (one predicate token -> mutual first-sense WordNet noun synonym); if it falls
back to NONCE the SYN variant is recorded as syn_unavailable. RENAME_NONCE: the same function with the synonym source
blanked (forces its nonce branch). Each variant is verified z3-equivalent to its parent under the inverse map; the
text is unchanged; output CORRECT. Controls sit in their own fold (E2_CONTROL) and never enter R_AB pools.
Output: work/controls_E2.json.
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src_d3"))
sys.path.insert(0, str(ROOT / "labeller"))
import perturb  # noqa: E402  (dataset 3, byte-identical)
from fol import parse, equivalent  # noqa: E402
from repair_census import rename  # noqa: E402
from disguise import emit  # noqa: E402

W = ROOT / "work"
MAX = 300


def sha(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest()


def variant(e, seed: str, force_nonce: bool):
    if force_nonce:
        real = perturb.first_sense_synonyms
        perturb.first_sense_synonyms = lambda tok: set()
        try:
            return perturb.control_rename(e, seed)
        finally:
            perturb.first_sense_synonyms = real
    return perturb.control_rename(e, seed)


def main():
    d = json.loads((W / "assembled_E2.json").read_text())
    cands = next(g for g in d["datasets"] if g["dataset"] == "e2_candidates")["examples"]
    elig = [r for r in cands if r["output"] == "CORRECT" and not r["metadata_reading_choice"] and r["metadata_label_tier"] in ("A", "A_unaudited_ref", "B")]
    tier_rank = {"A": 0, "A_unaudited_ref": 0, "B": 1}
    per = {}
    for r in elig:
        per.setdefault(r["metadata_strata"]["source_stratum"], []).append(r)
    for k in per:
        per[k].sort(key=lambda r: (tier_rank[r["metadata_label_tier"]], sha("E2_ctrl|" + r["metadata_row_key"])))
    order, i = [], 0
    strata = [s for s in ("L25", "EXC", "DT") if s in per]
    while len(order) < MAX and any(per[s] for s in strata):
        s = strata[i % len(strata)]
        if per[s]:
            order.append(per[s].pop(0))
        i += 1
    out, log = [], Counter()
    for r in order:
        inp = json.loads(r["input"])
        e = parse(inp["candidate_fol"])
        for want, force in (("RENAME_SYN", False), ("RENAME_NONCE", True)):
            kind, mp, e2 = variant(e, r["metadata_row_key"], force)
            if want == "RENAME_SYN" and kind != "RENAME_SYN":
                log["syn_unavailable"] += 1
                out.append({"control_type": "RENAME_SYN", "syn_unavailable": True, "parent": r})
                continue
            inv = {(nn, p[1]): p[0] for p, nn in mp.items()}
            back = rename(e2, inv, {})
            ok = equivalent(back, e) is True
            log[f"{want}_z3_inverse_ok={ok}"] += 1
            out.append({"control_type": want, "syn_unavailable": False, "parent": r, "fol": emit(e2),
                        "rename_map": {f"{p[0]}/{p[1]}": nn for p, nn in mp.items()}, "inverse_map_z3_equivalent": ok})
    rows = []
    for c in out:
        r = c["parent"]
        inp = json.loads(r["input"])
        if c["syn_unavailable"]:
            continue
        rows.append({"input": json.dumps({"text": inp["text"], "candidate_fol": c["fol"], "system": r["metadata_system"],
                                          "prompt_variant": r["metadata_prompt_variant"]}, ensure_ascii=False),
                     "output": "CORRECT" if c["inverse_map_z3_equivalent"] else "CONTROL_VERIFY_FAILED",
                     "metadata_fold": "E2_CONTROL", "metadata_control_type": c["control_type"],
                     "metadata_control_parent_row_key": r["metadata_row_key"], "metadata_control_base_tier": r["metadata_label_tier"],
                     "metadata_rename_map": c["rename_map"], "metadata_inverse_map_z3_equivalent": c["inverse_map_z3_equivalent"],
                     "metadata_sentence_id": r["metadata_sentence_id"], "metadata_system": r["metadata_system"],
                     "metadata_family": r["metadata_family"], "metadata_strata": r["metadata_strata"],
                     "metadata_row_key": f"{r['metadata_row_key']}|{c['control_type']}"})
    rep = {"n_eligible_final_correct": len(elig), "n_parents": len(order), "n_control_rows": len(rows),
           "parents_by_stratum": dict(Counter(r["metadata_strata"]["source_stratum"] for r in order)),
           "parents_by_tier": dict(Counter(r["metadata_label_tier"] for r in order)), "log": dict(log)}
    (W / "controls_E2.json").write_text(json.dumps({"report": rep, "rows": rows}, ensure_ascii=False, indent=1))
    print(json.dumps(rep))


if __name__ == "__main__":
    main()
