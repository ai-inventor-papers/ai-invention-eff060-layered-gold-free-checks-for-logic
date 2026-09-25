#!/usr/bin/env python3
"""STEP 7b: data-quality statistics (NO metric results) -> work/label_report.json; testability declaration -> prereg_strata.json.

Also runs the disguise guard of plan 5a: on 50 sentences, the pairwise plain-z3 equivalence structure of the class
representatives must be unchanged after disguise.
"""
from __future__ import annotations

import json
import math
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "labeller"))
sys.setrecursionlimit(10000)
W = ROOT / "work"


def load_jsonl(p):
    p = Path(p)
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if p.exists() else []


def wilson(k, n, z=1.96):
    if n == 0:
        return None
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(k / n, 4), round(c - h, 4), round(c + h, 4)]


def disguise_check(n=50):
    from disguise import Disguiser
    from fol import parse, equivalent
    labs = load_jsonl(W / "labels_heldout.jsonl")[:n]
    sents = {s["sentence_id"]: s for s in json.loads((W / "sentences.json").read_text())}
    from run_label import heldout_jobs
    jobs = {j["sentence_id"]: j for j in heldout_jobs()}
    mism = pairs = unk = 0
    for lab in labs:
        sid = lab["sentence_id"]
        allf = [lab["reference"]] + [c["fol"] for c in jobs[sid]["cands"] if c["fol"]]
        d = Disguiser(sid, sents[sid]["text"], sorted(set(allf)))
        reps = [c["rep_fol"] for c in lab["classes"] if c["rep_fol"].strip()][:8]
        for i in range(len(reps)):
            for j in range(i + 1, len(reps)):
                try:
                    a, b = parse(reps[i]), parse(reps[j])
                except Exception:  # noqa: BLE001
                    continue
                r1 = equivalent(a, b, ms=1500)
                r2 = equivalent(d.ast(reps[i]), d.ast(reps[j]), ms=1500)
                pairs += 1
                if r1 is None or r2 is None:
                    unk += 1
                elif r1 != r2:
                    mism += 1
    return {"sentences": len(labs), "pairs": pairs, "mismatches": mism, "z3_unknown_pairs": unk, "passed": mism == 0}


def main():
    A = json.loads((W / "assembled.json").read_text())
    g = {d["dataset"]: d["examples"] for d in A["datasets"]}
    H, S, C, SC = g["heldout_candidates"], g["heldout_sentences"], g["panel_calibration"], g["screen_audit"]
    rep = {"generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    rep["counts"] = {k: len(v) for k, v in g.items()}
    rep["heldout_final_label"] = dict(Counter(r["output"] for r in H))
    rep["heldout_tier"] = dict(Counter(r["metadata_label_tier"] for r in H))
    rep["heldout_auto_label"] = dict(Counter(r["metadata_auto_label"] for r in H))
    rep["heldout_repair_status"] = dict(Counter(str(r["metadata_repair_status"]) for r in H))
    rep["heldout_equiv_status"] = dict(Counter(str(r["metadata_equiv_status"]) for r in H))
    ops = Counter(o for r in H if r["output"] == "ERROR" for o in (r["metadata_error_ops"] or []))
    rep["heldout_error_ops_mass"] = dict(ops.most_common())
    rep["heldout_error_depth"] = dict(Counter(len(r["metadata_error_ops"] or []) for r in H if r["output"] == "ERROR"))
    El = [r for r in H if r["output"] == "ERROR" and r["metadata_system_class"] == "llm"]
    rep["addrop"] = {"n_error_llm": len(El), "n_addrop_only": sum(r["metadata_addrop_only_suspect"] for r in El),
                     "n_add_plus_drop": sum((r["metadata_error_ops"] or []) == ["ADD", "DROP"] for r in El),
                     "signatures": dict(Counter("+".join(r["metadata_error_ops"] or []) for r in El).most_common(25))}
    rep["convention_flags"] = dict(Counter(f for r in H for f in (r["metadata_convention_flags"] or [])))
    rep["reference_status"] = dict(Counter(r["output"] for r in S))
    # per system x variant
    per = defaultdict(Counter)
    for r in H:
        key = f"{r['metadata_system']}|{r['metadata_prompt_variant']}"
        per[key]["n"] += 1
        per[key][r["metadata_auto_label"]] += 1
    rep["per_system"] = {k: {**dict(v), "parse_rate": round(1 - v["UNPARSEABLE"] / v["n"], 4)} for k, v in sorted(per.items())}
    # per stratum x tier, rows and distinct sentences
    strat = {}
    for st in ("L25", "L20", "EXC", "CTRL"):
        rows = [r for r in H if r["metadata_strata"]["source_stratum"] == st and r["metadata_system_class"] == "llm"]
        d = {"rows": len(rows), "sentences": len({r["metadata_sentence_id"] for r in rows})}
        for tier in ("A", "A_unaudited_ref", "B", "C"):
            for lab in ("CORRECT", "ERROR", "CONTESTED"):
                sel = [r for r in rows if r["metadata_label_tier"] == tier and r["output"] == lab]
                if sel:
                    d[f"{tier}:{lab}"] = {"rows": len(sel), "sentences": len({r["metadata_sentence_id"] for r in sel})}
        d["UNRESOLVED"] = sum(r["output"] == "UNRESOLVED" for r in rows)
        d["UNPARSEABLE"] = sum(r["output"] == "UNPARSEABLE" for r in rows)
        if st == "EXC":
            d["by_exception_type"] = {t: dict(Counter(r["output"] for r in rows if r["metadata_strata"]["exception_type"] == t))
                                      for t in sorted({str(r["metadata_strata"]["exception_type"]) for r in rows})}
        if st == "CTRL":
            d["by_len_bin"] = {b: dict(Counter(r["output"] for r in rows if r["metadata_strata"]["ctrl_len_bin"] == b))
                               for b in sorted({str(r["metadata_strata"]["ctrl_len_bin"]) for r in rows})}
        strat[st] = d
    rep["strata"] = strat
    # testability: official rule uses tiers A+B with an audited reference; provisional uses A_unaudited_ref
    decl = {}
    for st, d in strat.items():
        def side(lab, tiers):
            rows = [r for r in H if r["metadata_strata"]["source_stratum"] == st and r["metadata_system_class"] == "llm"
                    and r["metadata_label_tier"] in tiers and r["output"] == lab]
            return len(rows), len({r["metadata_sentence_id"] for r in rows})
        e_o, es_o = side("ERROR", ("A", "B")); c_o, cs_o = side("CORRECT", ("A", "B"))
        e_p, es_p = side("ERROR", ("A", "B", "A_unaudited_ref")); c_p, cs_p = side("CORRECT", ("A", "B", "A_unaudited_ref"))
        rows_s = [r for r in H if r["metadata_strata"]["source_stratum"] == st and r["metadata_system_class"] == "llm"
                  and r["metadata_label_tier"] in ("A", "B", "A_unaudited_ref") and r["output"] == "ERROR" and not r["metadata_addrop_only_suspect"]]
        e_s, es_s = len(rows_s), len({r["metadata_sentence_id"] for r in rows_s})
        decl_strict = {"ERROR_rows": e_s, "ERROR_sents": es_s, "CORRECT_rows": c_p, "CORRECT_sents": cs_p,
                       "testable": e_s >= 50 and c_p >= 50 and es_s >= 25 and cs_p >= 25}
        decl[st] = {"provisional_strict_excl_addrop": decl_strict, "official_tierAB": {"ERROR_rows": e_o, "ERROR_sents": es_o, "CORRECT_rows": c_o, "CORRECT_sents": cs_o,
                                        "testable": e_o >= 50 and c_o >= 50 and es_o >= 25 and cs_o >= 25},
                    "provisional_incl_unaudited_ref": {"ERROR_rows": e_p, "ERROR_sents": es_p, "CORRECT_rows": c_p, "CORRECT_sents": cs_p,
                                                       "testable": e_p >= 50 and c_p >= 50 and es_p >= 25 and cs_p >= 25}}
    rep["testability"] = decl
    # sensitivity only: solver-lenient label (VOCAB_GRAN counted CORRECT) — NOT a testability basis
    len_ = {}
    for st in ("L25", "L20", "EXC", "CTRL"):
        rows = [r for r in H if r["metadata_strata"]["source_stratum"] == st and r["metadata_system_class"] == "llm"]
        c = Counter(r["metadata_solver_lenient_label"] for r in rows)
        len_[st] = {**dict(c), "CORRECT_sents": len({r["metadata_sentence_id"] for r in rows if r["metadata_solver_lenient_label"] == "CORRECT"}),
                    "ERROR_sents": len({r["metadata_sentence_id"] for r in rows if r["metadata_solver_lenient_label"] == "ERROR"})}
    rep["solver_lenient_by_stratum"] = len_
    # auto-label distribution per stratum (all LLM rows)
    rep["auto_by_stratum"] = {st: dict(Counter(r["metadata_auto_label"] for r in H if r["metadata_strata"]["source_stratum"] == st
                                               and r["metadata_system_class"] == "llm")) for st in ("L25", "L20", "EXC", "CTRL")}
    # L25 top-up rule check (rule frozen before labels were seen)
    l25 = decl["L25"]["provisional_incl_unaudited_ref"]
    rep["l25_topup_rule"] = {"tierA_projected_ERROR": l25["ERROR_rows"], "tierA_projected_CORRECT": l25["CORRECT_rows"],
                             "triggered": l25["ERROR_rows"] < 60 or l25["CORRECT_rows"] < 60,
                             "executed": False, "reason_not_executed": "OpenRouter key daily limit exhausted (limit_remaining=0) — no generation possible"}
    # ccg2lambda + gold rows
    rep["ccg2lambda"] = json.loads((W / "ccg2lambda_stats.json").read_text())
    rep["ccg2lambda_auto"] = dict(Counter(r["metadata_auto_label"] for r in H if r["metadata_system"] == "ccg2lambda"))
    rep["exclusion_log"] = json.loads((W / "exclusion_log.json").read_text())
    rep["screen_meta"] = json.loads((W / "screen_meta.json").read_text()) if (W / "screen_meta.json").exists() else None
    rep["screen_final_label"] = {t: dict(Counter(r["output"] for r in SC if r["metadata_track"] == t)) for t in ("L", "H")}
    rep["screen_auto_label"] = {t: dict(Counter(r["metadata_auto_label"] for r in SC if r["metadata_track"] == t)) for t in ("L", "H")}
    rep["screen_auto_by_system"] = {s: dict(Counter(r["metadata_auto_label"] for r in SC if r["metadata_system"] == s))
                                    for s in sorted({r["metadata_system"] for r in SC})}
    # gate
    rep["gate_prompt_v2"] = json.loads((W / "gate_results.json").read_text()).get("synthetic") if (W / "gate_results.json").exists() else None
    rep["gate_prompt_v1"] = json.loads((W / "gate_results_v1_prompt_v1.json").read_text()).get("synthetic") if (W / "gate_results_v1_prompt_v1.json").exists() else None
    th = [r for r in C if r["metadata_subset"] == "trackH_real_error_pairs"]
    cov = Counter(len(r["metadata_panel_votes"] or {}) for r in th)
    rep["trackH_panel_coverage"] = {"pairs": len(th), "votes_per_pair": dict(cov),
                                    "note": "4c was cut off by the key's daily limit after a few calls; accuracy is NOT reported (too few judgements)"}
    # costs
    led = load_jsonl(ROOT / "cost_ledger.jsonl")
    ph = defaultdict(lambda: [0, 0.0])
    for r in led:
        ph[r["phase"]][0] += 1; ph[r["phase"]][1] += r["cost_usd"]
    rep["cost_by_phase"] = {k: {"calls": v[0], "usd": round(v[1], 4)} for k, v in ph.items()}
    rep["cost_total_usd"] = round(sum(r["cost_usd"] for r in led), 4)
    rep["disguise_check"] = disguise_check(50)
    (W / "label_report.json").write_text(json.dumps(rep, indent=1))
    pr = json.loads((ROOT / "prereg_strata.json").read_text())
    pr["testability_declaration"] = {"declared_at_utc": rep["generated_at_utc"], "declared_before_any_metric_run": True,
                                     "per_stratum": decl,
                                     "status": "OFFICIAL tier A+B testability = FALSE for every stratum because the panel (gold audit + tier-B "
                                               "adjudication) was blocked by the shared OpenRouter key's daily limit. PROVISIONAL counts use "
                                               "solver-only tier A against UNAUDITED references (MALLS GPT-4 gold / agreed FOLIO refs). If the "
                                               "panel is later run (src/resume_panel.sh), re-run stats.py and this declaration is superseded."}
    (ROOT / "prereg_strata.json").write_text(json.dumps(pr, indent=1))
    print(json.dumps({k: rep[k] for k in ("counts", "heldout_final_label", "heldout_tier", "testability", "disguise_check", "cost_total_usd")}, indent=1))


if __name__ == "__main__":
    main()
