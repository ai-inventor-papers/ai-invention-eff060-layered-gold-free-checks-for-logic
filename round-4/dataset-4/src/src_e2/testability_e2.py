#!/usr/bin/env python3
"""E2 STEP 9: testability_E2.json, written after labels and BEFORE any metric exists (this artifact computes none).

Rule (E's, verbatim in prereg_E2.json): a cell is TESTABLE iff it has >=50 ERROR rows AND >=50 CORRECT rows AND >=25
distinct sentences contributing ERROR rows AND >=25 contributing CORRECT rows; LLM systems only; CONTESTED and
reading_choice rows excluded.  Regimes:
  R_AB            tiers A + B                                  (primary)
  R_A             tier A only                                   (robustness)
  R_VEX           R_AB rows with vex == True                    (instrument-disjoint subset)
  R_A_UNAUDITED   tier 'A_unaudited_ref' (solver vs unaudited gold; the regime that exists when the panel cannot run)
Expected power: SE = 0.0434 * sqrt(74 / N_both) where N_both = distinct sentences with both classes in the cell
(E's L25: stratified dAUROC CI half-width 0.085 -> SE 0.0434 with 74 both-class sentences among 873 A+B rows);
MDE80 = 2.8 * SE. The Hanley-McNeil iid SE at AUROC 0.70 is reported next to it as an optimistic floor.
"""
from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W = ROOT / "work"
SE_E, NBOTH_E = 0.085 / 1.96, 74
CORE = ("unless", "except", "excluding", "other_than")
REGIMES = {
    "R_AB": lambda r: r["metadata_label_tier"] in ("A", "B"),
    "R_A": lambda r: r["metadata_label_tier"] == "A",
    "R_VEX": lambda r: r["metadata_label_tier"] in ("A", "B") and r.get("metadata_vex") is True,
    "R_A_UNAUDITED": lambda r: r["metadata_label_tier"] == "A_unaudited_ref",
}
STRATA = {
    "L25": lambda s: s["source_stratum"] == "L25",
    "L25_bin_25-29": lambda s: s["source_stratum"] == "L25" and s.get("word_bin") == "25-29",
    "L25_bin_30-34": lambda s: s["source_stratum"] == "L25" and s.get("word_bin") == "30-34",
    "EXC": lambda s: s["source_stratum"] == "EXC",
    "EXC_core_marker": lambda s: s["source_stratum"] == "EXC" and s.get("exception_type") in CORE,
    "DT": lambda s: s["source_stratum"] == "DT",
    "ALL_MALLS": lambda s: s["source_stratum"] in ("L25", "EXC"),
    "ALL": lambda s: True,
}


def hanley_mcneil(a: float, n1: int, n0: int) -> float | None:
    if n1 == 0 or n0 == 0:
        return None
    q1, q2 = a / (2 - a), 2 * a * a / (1 + a)
    return math.sqrt((a * (1 - a) + (n1 - 1) * (q1 - a * a) + (n0 - 1) * (q2 - a * a)) / (n1 * n0))


def main():
    d = json.loads((W / "assembled_E2.json").read_text())
    cands = next(g for g in d["datasets"] if g["dataset"] == "e2_candidates")["examples"]
    sents = {r["metadata_sentence_id"]: r["metadata_strata"] for r in next(g for g in d["datasets"] if g["dataset"] == "e2_sentences")["examples"]}
    n_active = {k: sum(f(s) for s in sents.values()) for k, f in STRATA.items()}
    out = {"rule": "testable iff >=50 ERROR and >=50 CORRECT rows and >=25 distinct sentences on each side; LLM rows only; CONTESTED and reading_choice excluded",
           "power_model": "SE = 0.0434*sqrt(74/N_both); MDE80 = 2.8*SE (E's L25 design effect); HM = Hanley-McNeil iid SE at AUROC 0.70",
           "written_before_any_metric": True, "cells": {}}
    for sname, sf in STRATA.items():
        rows = [r for r in cands if r["metadata_system_class"] == "llm" and sf({**r["metadata_strata"], "exception_type": r["metadata_strata"].get("exception_type")})]
        n_sent_with_rows = len({r["metadata_sentence_id"] for r in rows})
        base = {"n_active_sentences": n_active[sname], "n_sentences_with_candidates": n_sent_with_rows, "n_llm_rows": len(rows),
                "CONTESTED": sum(r["output"] == "CONTESTED" for r in rows),
                "reading_choice": sum(bool(r["metadata_reading_choice"]) for r in rows),
                "tier_C": sum(r["metadata_label_tier"] == "C" for r in rows),
                "UNRESOLVED": sum(r["output"] == "UNRESOLVED" for r in rows),
                "UNPARSEABLE": sum(r["output"] == "UNPARSEABLE" for r in rows)}
        cell = {"counts_all_regimes": base}
        for rname, rf in REGIMES.items():
            sel = [r for r in rows if r["output"] in ("CORRECT", "ERROR") and not r["metadata_reading_choice"] and rf(r)]
            side = defaultdict(set)
            for r in sel:
                side[r["output"]].add(r["metadata_sentence_id"])
            nc, ne = sum(r["output"] == "CORRECT" for r in sel), sum(r["output"] == "ERROR" for r in sel)
            both = len(side["CORRECT"] & side["ERROR"])
            se = SE_E * math.sqrt(NBOTH_E / both) if both else None
            hm = hanley_mcneil(0.70, nc, ne)
            cell[rname] = {"CORRECT_rows": nc, "ERROR_rows": ne, "CORRECT_sentences": len(side["CORRECT"]), "ERROR_sentences": len(side["ERROR"]),
                           "sentences_with_both_classes": both,
                           "testable": bool(nc >= 50 and ne >= 50 and len(side["CORRECT"]) >= 25 and len(side["ERROR"]) >= 25),
                           "SE_design_effect": round(se, 4) if se else None, "MDE80": round(2.8 * se, 3) if se else None,
                           "SE_hanley_mcneil_iid_auc0.7": round(hm, 4) if hm else None}
        out["cells"][sname] = cell
    out["expected_power_if_completed"] = {
        "note": "projection for the pre-registered design (E's L25 yield: 74 both-class sentences per 300 L25 sentences)",
        "L25_350": round(2.8 * SE_E * math.sqrt(NBOTH_E / (350 * 74 / 300)), 3),
        "L25_450": round(2.8 * SE_E * math.sqrt(NBOTH_E / (450 * 74 / 300)), 3),
        "pooled_550_at_L25_yield": round(2.8 * SE_E * math.sqrt(NBOTH_E / (550 * 74 / 300)), 3)}
    (ROOT / "testability_E2.json").write_text(json.dumps(out, indent=1))
    print(json.dumps({k: {r: (v[r]["testable"], v[r]["CORRECT_rows"], v[r]["ERROR_rows"]) for r in REGIMES} for k, v in out["cells"].items()}))
    print(out["expected_power_if_completed"])


if __name__ == "__main__":
    main()
