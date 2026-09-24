#!/usr/bin/env python3
"""Builds tables.md (one '# source:' line per table), method_out.json (exp_gen_sol_out; predict_* oriented higher = ERROR),
the M3 marker e2/E2A_FINAL_READY.json and results/cost_E2A.json from the result files. Numbers are copied, never retyped."""
from __future__ import annotations

import hashlib
import json
import time
from collections import Counter, defaultdict
from pathlib import Path

WS = Path(__file__).resolve().parents[1]
RES = WS / "results"
E2S = WS / "e2src"
SHOW = ["c_score_align", "p_peer_text", "S4_E2_plus_V0", "S4_E2", "c_exact", "g_align", "c_pn", "c_rw", "c_pn_rw", "c_two", "c_v5",
        "judge_cheap_disg", "judge_cheap_orig", "judge_cheap2_disg", "judge_cheap2_orig", "judge_local_qwen8b_disg",
        "judge_local_qwen8b_orig", "l2_bow", "l3_z3", "pilot_joint_conflict", "pilot_arity_incons", "pilot_shape_incons",
        "pilot_dangling", "pilot_rerun_jacc"]


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def J(name: str):
    p = RES / name
    return json.loads(p.read_text()) if p.exists() else None


def f3(x):
    return "—" if x is None else f"{x:.3f}"


def fci(c):
    return "—" if not c or c[0] is None else f"[{c[0]:.3f}, {c[1]:.3f}]"


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def cost() -> dict:
    led = jl(E2S / "cost_ledger.jsonl")
    by = defaultdict(float)
    for r in led:
        by[r["phase"]] += r["cost_usd"]
    t1 = jl(WS / "cache" / "t1_results" / "costs.jsonl")
    for r in t1:
        by["judges_" + r.get("component", "?")] += r.get("cost", r.get("cost_usd", 0)) or 0
    for r in jl(WS / "cache" / "l3_cost_ledger.jsonl"):
        by["l3_questionnaire"] += r.get("cost_usd", 0)
    sc = jl(WS / "scores_E2A.jsonl")
    n = len(sc)
    gen = sum(r["gen_cost_usd"] for r in sc)
    n_sent = len({r["sentence_id"] for r in sc})
    secs = {}
    for r in sc:
        secs[r["sentence_id"]] = r.get("secs_consensus_sentence") or 0
    cpu = sum(secs.values())
    return {"spend_by_phase_usd": {k: round(v, 5) for k, v in by.items()}, "total_usd": round(sum(by.values()), 4),
            "cap_usd": 9.5, "iter4_dataset4_spend_excluded_usd": 0.2409,
            "consensus_cost_per_candidate": {
                "FULL_usd": gen / n, "FULL_note": "the peers' generation cost: every slot's output of the sentence (10 slots) / candidates",
                "FULL_usd_per_sentence": gen / n_sent, "MARGINAL_usd": 0.0,
                "MARGINAL_cpu_seconds": cpu / n, "MARGINAL_note": "eqmv z3 + text side CPU seconds per candidate (peers already exist)"},
            "judge_cost_per_call_usd": {k: (sum(r.get("cost") or 0 for r in jl(WS / "cache" / f"{k}.jsonl")) /
                                            max(1, sum(1 for r in jl(WS / "cache" / f"{k}.jsonl") if r.get("p") is not None)))
                                        for k in ("judge_cheap", "judge_cheap2")}}


def main() -> None:
    A = J("auroc_cells.json")
    V = J("confirm_verdict_E2A.json")
    H = J("hmech_E2.json")
    C = cost()
    (RES / "cost_E2A.json").write_text(json.dumps(C, indent=1))
    L = []
    L.append("# E2-A tables (iteration 5, untouched E2; frozen metrics; labels joined after both seals)\n")
    L.append("## T1. Verdict of the pre-registered confirmation\n# source: results/confirm_verdict_E2A.json\n")
    a = V["a"]
    L.append(f"- OVERALL: **{V['overall']}**")
    L.append(f"- (a) R_AB long pool (L25+EXC): n = {a['n']} rows ({a['n_error']} ERROR / {a['n_correct']} CORRECT, {a['n_sentences']} sentences), testable = {a['testable']}")
    for k, nm in (("delta_vs_flashlite_disg", "V0 − flash-lite disguised (PRIMARY)"), ("delta_vs_flashlite_orig", "V0 − flash-lite original"),
                  ("delta_vs_nano_orig", "V0 − nano original"), ("delta_vs_nano_disg", "V0 − nano disguised")):
        d = a.get(k) or {}
        L.append(f"  - {nm}: Δ = {f3(d.get('delta'))} {fci(d.get('ci'))} (n = {d.get('n', '—')}; pooled-cluster CI {fci(d.get('ci_pooled_cluster_boot'))})")
    b = V["b"]["nested_S4_E2_plus_V0_minus_S4_E2"] or {}
    L.append(f"- (b) nested [S4_E2 + V0] − S4_E2: Δ = {f3(b.get('delta'))} {fci(b.get('ci'))}; S4 features used {V['b']['S4_features']}; dropped (<95% coverage) {V['b']['S4_features_dropped']}")
    fb = V.get("fallback_substitute_bar") or {}
    L.append(f"- FALLBACK (declared substitute bar, secondary): {fb.get('note', '')}")
    for k, d in fb.items():
        if isinstance(d, dict):
            L.append(f"  - {k}: Δ = {f3(d.get('delta'))} {fci(d.get('ci'))} (n = {d.get('n')}; {d.get('n_error')} ERR / {d.get('n_correct')} COR; testable {d.get('testable')})")
    L.append(f"- (c) R_COMP FREE (sibling): {json.dumps(V['c']['status'])} ({V['c'].get('source')})")
    for k, v in V["also_reported"].items():
        if isinstance(v, dict) and "delta" in v and isinstance(v["delta"], dict):
            L.append(f"- {k}: Δ = {f3(v['delta'].get('delta'))} {fci(v['delta'].get('ci'))}; testable {v.get('testable')}; MDE80 {f3(v.get('mde80'))}")
        elif isinstance(v, dict):
            L.append(f"- {k}: Δ = {f3(v.get('delta'))} {fci(v.get('ci'))} (n = {v.get('n')})")
        else:
            L.append(f"- {k}: {v}")
    L.append("")
    for rn in ("R_AB", "R_A", "R_VEX", "R_AB_nopilot"):
        for cn, cell in A[rn].items():
            L.append(f"## AUROC — regime {rn}, cell {cn}\n# source: results/auroc_cells.json :: {rn} / {cn}\n")
            L.append(f"n = {cell['n_rows']} ({cell['n_error']} ERROR / {cell['n_correct']} CORRECT; {cell['n_sentences']} sentences); testable = {cell['testable']}\n")
            if not cell["metrics"]:
                continue
            L.append("| metric | n | strat AUROC | 95% CI | pooled |\n|---|---|---|---|---|")
            for m in SHOW:
                x = cell["metrics"].get(m)
                if x and x.get("strat") is not None:
                    L.append(f"| {m} | {x['n']} | {f3(x['strat'])} | {fci(x.get('strat_ci'))} | {f3(x.get('pooled'))} |")
            L.append("\n| paired Δ (strat) | n | Δ | 95% CI | CI > 0 |\n|---|---|---|---|---|")
            for k, d in cell["deltas"].items():
                L.append(f"| {k} | {d['n']} | {f3(d['delta'])} | {fci(d['ci'])} | {d['ci_gt0']} |")
            L.append("")
    L.append("## H-MECH\n# source: results/hmech_E2.json\n")
    for k, v in H.items():
        L.append(f"- {k}: {json.dumps({kk: vv for kk, vv in v.items() if kk != 'by_class'})[:600]}")
        if "by_class" in v:
            for cl, x in v["by_class"].items():
                L.append(f"  - {cl}: {json.dumps(x)}")
    L.append("")
    for nm, fn in (("H-IMPROVE", "improve_E2.json"), ("H-RENAME", "rename_E2.json"), ("Complexity", "complexity_E2.json"),
                   ("System-level Kendall τ-b", "system_level_E2.json"), ("Coverage", "coverage_E2.json"), ("Placebos", "placebo_E2.json"),
                   ("Cost", "cost_E2A.json"), ("Union with E2-B", "union_longpool.json"), ("Prefix used", "prefix_used.json")):
        x = J(fn)
        if x is None:
            continue
        L.append(f"## {nm}\n# source: results/{fn}\n")
        if nm == "Coverage":
            x = {k: v for k, v in x.items() if k != "COVERAGE_view_long"} | {"COVERAGE_view_long_deltas": x["COVERAGE_view_long"]["deltas"],
                                                                            "COVERAGE_view_long_auroc": {k: v.get("strat") for k, v in x["COVERAGE_view_long"]["metrics"].items()}}
        L.append("```\n" + json.dumps(x, indent=1, default=str)[:6000] + "\n```\n")
    (WS / "tables.md").write_text("\n".join(L))
    # ---------------- method_out.json
    rows = jl(WS / "per_item_E2A.jsonl")
    pre = {r["row_key"]: r for r in jl(WS / "scores_E2A.jsonl")}
    groups = defaultdict(list)
    for r in rows:
        c = pre[r["row_key"]]
        ex = {"input": json.dumps({"text": None, "candidate_fol": None, "row_key": r["row_key"]}), "output": str(r.get("label"))}
        ex["metadata_row_key"] = r["row_key"]
        for k in ("sentence_id", "stratum", "slot", "system", "family", "label_tier", "reading_choice", "vex", "pilot", "words",
                  "n_conditions", "parse_ok", "fold_E2"):
            ex[f"metadata_{k}"] = r.get(k)
        for m in SHOW:
            if m in r:
                ex[f"predict_{m}"] = "null" if r.get(m) is None else f"{r[m]:.6f}"
        groups[r["stratum"]].append(ex)
    cand = {json.loads(l)["row_key"]: json.loads(l) for l in (WS / "e2" / "candidates_E2_nolabels.jsonl").read_text().splitlines()}
    for g in groups.values():
        for ex in g:
            c = cand[ex["metadata_row_key"]]
            ex["input"] = json.dumps({"text": c["text"], "candidate_fol": c["candidate_fol"]}, ensure_ascii=False)
    mo = {"metadata": {"method_name": "frozen cross-family solver consensus c_score_align (V0) and comparators on untouched E2",
                       "orientation": "every predict_* is higher = more likely ERROR; output = E2 final label (E's frozen protocol)",
                       "verdict": V["overall"]},
          "datasets": [{"dataset": f"E2_{k}", "examples": v} for k, v in sorted(groups.items())]}
    (WS / "method_out.json").write_text(json.dumps(mo, ensure_ascii=False))
    # ---------------- M3 marker
    p = WS / "per_item_E2A.jsonl"
    m3 = {"token": "aii_iter5_e2a_final_v1", "written_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
          "per_row_file": str(p), "sha256": sha(p), "n_rows": len(rows),
          "columns_note": "row_key, sentence_id, stratum, label, label_tier, reading_choice, every frozen score (higher = ERROR)",
          "overall": V["overall"], "prefix_used": J("prefix_used.json")}
    (WS / "e2" / "E2A_FINAL_READY.json").write_text(json.dumps(m3, indent=1))
    print("tables.md, method_out.json, cost_E2A.json, E2A_FINAL_READY.json written")


if __name__ == "__main__":
    main()
