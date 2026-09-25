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


SENT = {s["sentence_id"]: s for s in json.loads((W / "sentences.json").read_text())}


def stratum_of(r, st: str) -> bool:
    s = SENT[r["metadata_sentence_id"]]
    if st == "L25_orig200":
        return s["source_stratum"] == "L25" and not s.get("topup_batch")
    if st == "L25_topup100":
        return bool(s.get("topup_batch"))
    if st == "MALLS_all":
        return s["source"].startswith("MALLS")
    return s["source_stratum"] == st


def pmaj(r):
    v = r["metadata_panel_votes"] or {}
    f = sum(x["faithful"] for x in v.values()); u = len(v) - f
    return "FAITHFUL" if f >= 2 else ("UNFAITHFUL" if u >= 2 else None)


def cohen(a, b):
    n = len(a)
    if n == 0:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return round((po - pe) / (1 - pe), 4) if pe < 1 else None


def fleiss(items):
    """items = list of [n_faithful, n_unfaithful], same number of raters per item."""
    if not items:
        return None
    k = sum(items[0]); N = len(items)
    p = [sum(it[j] for it in items) / (N * k) for j in range(2)]
    P = [(sum(x * x for x in it) - k) / (k * (k - 1)) for it in items]
    Pb, Pe = sum(P) / N, sum(x * x for x in p)
    return round((Pb - Pe) / (1 - Pe), 4) if Pe < 1 else None


def panel_reliability():
    recs = {r["sentence_id"]: r for r in load_jsonl(W / "panel_heldout.jsonl")}
    adj = load_jsonl(W / "panel_heldout_adj.jsonl")
    out = {"design": "P3 (GLM-4.6) and R1 (Kimi-K2-0905) judge every shown item; P1 (Haiku-4.5) judges only the items where "
                     "they disagree or a vote is missing (label-preserving: the 2-of-3 majority equals the full 3-vote majority). "
                     "The first 30 sentences (sha1 order) were judged by all three (pilot) and give the 3-rater Fleiss kappa."}
    per_st = {}
    for st in ("L25", "L20", "EXC", "CTRL", "ALL"):
        a, b = [], []
        for sid, r in recs.items():
            if st != "ALL" and SENT[sid]["source_stratum"] != st:
                continue
            for cid, v in r["votes"].items():
                if "P3" in v and "R1" in v:
                    a.append(int(v["P3"]["faithful"])); b.append(int(v["R1"]["faithful"]))
        per_st[st] = {"items": len(a), "agreement": round(sum(x == y for x, y in zip(a, b)) / len(a), 4) if a else None,
                      "cohen_kappa_P3_R1": cohen(a, b), "faithful_rate_P3": round(sum(a) / len(a), 4) if a else None,
                      "faithful_rate_R1": round(sum(b) / len(b), 4) if b else None}
    out["pairwise_P3_R1_by_stratum"] = per_st
    pilot = [r for r in recs.values() if "P1" in r.get("members", [])]
    items, pairs = [], {("P1", "P3"): ([], []), ("P1", "R1"): ([], []), ("P3", "R1"): ([], [])}
    for r in pilot:
        for cid, v in r["votes"].items():
            if all(m in v for m in ("P1", "P3", "R1")):
                f = sum(v[m]["faithful"] for m in ("P1", "P3", "R1")); items.append([f, 3 - f])
                for (x, y), (la, lb) in pairs.items():
                    la.append(int(v[x]["faithful"])); lb.append(int(v[y]["faithful"]))
    out["pilot_3rater"] = {"sentences": len(pilot), "items": len(items), "fleiss_kappa": fleiss(items),
                           "unanimous_share": round(sum(max(i) == 3 for i in items) / len(items), 4) if items else None,
                           "cohen": {f"{x}-{y}": cohen(la, lb) for (x, y), (la, lb) in pairs.items()}}
    n_items = sum(len(r["items"]) for r in adj)
    agree = Counter()
    for r in adj:
        v0 = recs.get(r["sentence_id"], {}).get("votes", {})
        for cid, v in r["votes"].items():
            o = v0.get(cid, {})
            for m in ("P3", "R1"):
                if m in o:
                    agree[f"P1_agrees_{m}"] += int(o[m]["faithful"] == v["faithful"]); agree[f"n_{m}"] += 1
    stage1_items = sum(len(r["shown"]) for r in recs.values() if "P1" not in r.get("members", []))
    out["adjudication"] = {"sentences": len(adj), "items_sent_to_P1": n_items, "stage1_items": stage1_items,
                           "share_items_adjudicated": round(n_items / max(1, stage1_items), 4),
                           "P1_agreement_counts": dict(agree), "failed_calls": sum(bool(r["errors"]) for r in adj)}
    out["sentences_with_errors_stage1"] = sum(bool(r.get("errors")) for r in recs.values())
    return out


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
    # ---- primary-pool testability (tiers A+B, CONTESTED and reading_choice excluded) + tier-A-only, L25 incl./excl. top-up
    def pool_counts(sel_rows):
        out = {}
        for lab in ("CORRECT", "ERROR"):
            rr = [r for r in sel_rows if r["output"] == lab]
            out[lab] = {"rows": len(rr), "sents": len({r["metadata_sentence_id"] for r in rr})}
        out["testable"] = all(out[l]["rows"] >= 50 and out[l]["sents"] >= 25 for l in ("CORRECT", "ERROR"))
        return out
    prim = {}
    for st in ("L25", "L25_orig200", "L25_topup100", "L20", "EXC", "CTRL"):
        base = [r for r in H if r["metadata_system_class"] == "llm" and stratum_of(r, st)]
        prim[st] = {"tierAB_primary": pool_counts([r for r in base if r["metadata_label_tier"] in ("A", "B") and not r["metadata_reading_choice"]]),
                    "tierAB_incl_reading_choice": pool_counts([r for r in base if r["metadata_label_tier"] in ("A", "B")]),
                    "tierA_only": pool_counts([r for r in base if r["metadata_label_tier"] == "A" and not r["metadata_reading_choice"]]),
                    "CONTESTED_rows": sum(r["output"] == "CONTESTED" for r in base),
                    "UNRESOLVED_rows": sum(r["output"] == "UNRESOLVED" for r in base),
                    "tierC_rows": sum(r["metadata_label_tier"] == "C" for r in base),
                    "reading_choice_rows": sum(bool(r["metadata_reading_choice"]) for r in base),
                    "rows": len(base), "sentences": len({r["metadata_sentence_id"] for r in base})}
    rep["testability_primary"] = prim
    # ---- gold audit (5d) per stratum, Wilson 95% CI; reference status
    ga = {}
    for st in ("L25", "L25_orig200", "L25_topup100", "L20", "EXC", "CTRL", "MALLS_all"):
        ss = [r for r in S if stratum_of(r, st)]
        aud = [r for r in ss if r["metadata_gold_audit_flag"] in ("FAITHFUL", "UNFAITHFUL")]
        wrong = sum(r["metadata_gold_audit_flag"] == "UNFAITHFUL" for r in aud)
        ga[st] = {"sentences": len(ss), "audited": len(aud), "judged_wrong": wrong, "gold_error_rate_wilson95": wilson(wrong, len(aud)),
                  "reference_status": dict(Counter(r["output"] for r in ss)),
                  "reading_choice_sentences": sum(bool(r["metadata_reading_choice"]) for r in ss)}
    rep["gold_audit"] = ga
    # ---- correct-but-not-equivalent rate
    def cne(rows):
        dec = [r for r in rows if r["metadata_label_tier"] in ("A", "B") and r["output"] in ("CORRECT", "ERROR") and r["metadata_auto_label"] != "CORRECT"]
        k = sum(r["output"] == "CORRECT" for r in dec)
        cor = [r for r in rows if r["metadata_label_tier"] in ("A", "B") and r["output"] == "CORRECT"]
        return {"non_EQ_decided_rows": len(dec), "final_CORRECT_among_non_EQ": wilson(k, len(dec)),
                "share_of_final_CORRECT_that_is_not_EQ": wilson(sum(r["metadata_correct_not_equivalent"] for r in cor), len(cor))}
    L = [r for r in H if r["metadata_system_class"] == "llm"]
    rep["correct_not_equivalent"] = {"by_stratum": {st: cne([r for r in L if stratum_of(r, st)]) for st in ("L25", "L20", "EXC", "CTRL")},
                                     "by_system": {s_: cne([r for r in L if f"{r['metadata_system']}|{r['metadata_prompt_variant']}" == s_])
                                                   for s_ in sorted({f"{r['metadata_system']}|{r['metadata_prompt_variant']}" for r in L})},
                                     "all_llm": cne(L)}
    # ---- automatic labeller vs panel majority (rows whose reference was audited FAITHFUL or repaired)
    cm = defaultdict(Counter)
    for r in L:
        if r["metadata_auto_label"] in ("UNPARSEABLE", "NO_REF") or r["metadata_reference_status"] not in ("GOLD_PANEL_OK", "TRUSTED_AGREED", "PANEL_REPAIRED"):
            continue
        cm[r["metadata_auto_label"]][pmaj(r) or "no_majority_or_not_covered"] += 1
    rep["labeller_vs_panel_confusion"] = {k: dict(v) for k, v in cm.items()}
    tp = sum(cm[a]["UNFAITHFUL"] for a in ("ERROR", "COMPOUND", "TIMEOUT_UNKNOWN"))
    fp = sum(cm[a]["FAITHFUL"] for a in ("ERROR", "COMPOUND", "TIMEOUT_UNKNOWN"))
    fn = sum(cm[a]["UNFAITHFUL"] for a in ("CORRECT", "VOCAB_GRAN"))
    tn = sum(cm[a]["FAITHFUL"] for a in ("CORRECT", "VOCAB_GRAN"))
    tp2, fp2 = cm["ERROR"]["UNFAITHFUL"], cm["ERROR"]["FAITHFUL"]
    rep["labeller_vs_panel_binary"] = {
        "definition": "auto-positive(error) = ERROR/COMPOUND/TIMEOUT_UNKNOWN, auto-negative = CORRECT/VOCAB_GRAN; panel truth = strict 2-of-3 majority; "
                      "LLM rows whose reference was audited FAITHFUL or repaired; rows without a panel majority excluded",
        "error_precision": wilson(tp, tp + fp), "error_recall": wilson(tp, tp + fn),
        "faithful_precision": wilson(tn, tn + fn), "faithful_recall": wilson(tn, tn + fp),
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "ERROR_only_precision": wilson(tp2, tp2 + fp2)}
    rep["panel_reliability"] = panel_reliability()
    rep["contested_rate"] = {st: wilson(sum(r["output"] == "CONTESTED" for r in L if stratum_of(r, st)),
                                        sum(r["output"] in ("CORRECT", "ERROR", "CONTESTED") for r in L if stratum_of(r, st)))
                             for st in ("L25", "L20", "EXC", "CTRL")}
    rep["ctrl_agreement_type"] = dict(Counter(r["metadata_agreement_type"] for r in S if r["metadata_strata"]["source_stratum"] == "CTRL"))
    rep["panel_scope"] = dict(Counter(r.get("metadata_panel_scope") for r in H))
    rep["error_ops_tierB_panel"] = dict(Counter(o for r in H if r["output"] == "ERROR" and r["metadata_label_tier"] == "B" for o in (r["metadata_error_ops"] or [])).most_common())
    rep["final_by_system_class"] = {c: dict(Counter(r["output"] for r in H if r["metadata_system_class"] == c)) for c in sorted({r["metadata_system_class"] for r in H})}
    rep["unresolved_reasons"] = dict(Counter(f"{r['metadata_auto_label']}|{r['metadata_reference_status']}" for r in H if r["output"] == "UNRESOLVED"))
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
    rep["l25_topup_rule"] = {"trigger_value_after_step3": "tier-A CORRECT = 9 (< 60)", "triggered": True, "executed": True,
                             "execution": json.loads((ROOT / "prereg_strata.json").read_text()).get("top_up_execution")}
    # ccg2lambda + gold rows
    rep["ccg2lambda"] = json.loads((W / "ccg2lambda_stats.json").read_text())
    rep["ccg2lambda_auto"] = dict(Counter(r["metadata_auto_label"] for r in H if r["metadata_system"] == "ccg2lambda"))
    rep["exclusion_log"] = json.loads((W / "exclusion_log.json").read_text())
    rep["screen_meta"] = json.loads((W / "screen_meta.json").read_text()) if (W / "screen_meta.json").exists() else None
    rep["screen_final_label"] = {t: dict(Counter(r["output"] for r in SC if r["metadata_track"] == t)) for t in ("L", "H")}
    rep["screen_auto_label"] = {t: dict(Counter(r["metadata_auto_label"] for r in SC if r["metadata_track"] == t)) for t in ("L", "H")}
    rep["screen_auto_by_system"] = {s: dict(Counter(r["metadata_auto_label"] for r in SC if r["metadata_system"] == s))
                                    for s in sorted({r["metadata_system"] for r in SC})}
    rep["screen_panel"] = {"rows_with_votes": sum(bool(r["metadata_panel_votes"]) for r in SC),
                           "tier_by_track": {t: dict(Counter(r["metadata_label_tier"] for r in SC if r["metadata_track"] == t)) for t in ("L", "H")},
                           "trackL_auto_vs_panel_majority": {a: dict(Counter(pmaj(r) or "none" for r in SC if r["metadata_track"] == "L" and r["metadata_auto_label"] == a and r["metadata_panel_votes"]))
                                                             for a in sorted({r["metadata_auto_label"] for r in SC if r["metadata_track"] == "L"})}}
    # gate
    rep["gate_prompt_v2"] = json.loads((W / "gate_results.json").read_text()).get("synthetic") if (W / "gate_results.json").exists() else None
    rep["gate_prompt_v1"] = json.loads((W / "gate_results_v1_prompt_v1.json").read_text()).get("synthetic") if (W / "gate_results_v1_prompt_v1.json").exists() else None
    th = [r for r in C if r["metadata_subset"] == "trackH_real_error_pairs"]
    rep["trackH_panel_coverage"] = {"pairs": len(th), "votes_per_pair": dict(Counter(len(r["metadata_panel_votes"] or {}) for r in th))}
    rep["trackH_real_error_accuracy"] = json.loads((W / "gate_results.json").read_text()).get("trackh")
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
                                     "primary_pool": prim,
                                     "status": "OFFICIAL = primary_pool[stratum].tierAB_primary.testable (tiers A+B, CONTESTED and reading_choice rows "
                                               "excluded, LLM systems only). Declared after labelling, before any metric run. per_stratum.* are the "
                                               "pre-panel provisional views, kept for traceability."}
    (ROOT / "prereg_strata.json").write_text(json.dumps(pr, indent=1))
    print(json.dumps({k: rep[k] for k in ("counts", "heldout_final_label", "heldout_tier", "testability_primary", "gold_audit", "labeller_vs_panel_binary", "disguise_check", "cost_total_usd")}, indent=1))


if __name__ == "__main__":
    main()
