#!/usr/bin/env python3
"""E2 STEP 4 readout: cost projection and shrink/surplus decision (COST ONLY; no label is inspected).

Generation cost per sentence: measured on the E2 pilot (raw/generations.jsonl, pilot sentence ids).
Panel stage-1 / adjudication / reference-repair cost per sentence: measured on the E2 pilot panel when it exists
(work/panel_cache.jsonl, pilot ids); otherwise E's own measured per-sentence costs by stratum from E's panel cache
and repair log (the run-level budget stop blocked the E2 panel pilot). DT uses E's EXC costs (similar length).
Writes pilot_projection.json with the pre-registered decision (shrink order / surplus rule).
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E_DIR = Path(__file__).resolve().parents[4] / "round-1/dataset-1/src"


def jl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()] if Path(p).exists() else []


def main():
    active = json.loads((ROOT / "work" / "sentences_E2_active.json").read_text())
    pilot = {s["sentence_id"]: s["source_stratum"] for s in active if s.get("pilot")}
    gen = defaultdict(float)
    for g in jl(ROOT / "raw" / "generations.jsonl"):
        if g["sentence_id"] in pilot:
            gen[pilot[g["sentence_id"]]] += g.get("cost_usd") or 0.0
    n_p = defaultdict(int)
    for st in pilot.values():
        n_p[st] += 1
    gen_ps = {st: gen[st] / n_p[st] for st in n_p}
    # E per-sentence panel costs by stratum (stage 1 = panel_heldout P3/R1, adj = P1 on heldout, repair)
    e_st = {s["sentence_id"]: s["source_stratum"] for s in json.loads((E_DIR / "work" / "sentences.json").read_text())}
    cost = defaultdict(lambda: defaultdict(float))
    for r in jl(E_DIR / "work" / "panel_cache.jsonl"):
        st = e_st.get(r["sentence_id"])
        if st:
            cost[st]["P1" if r["member"] == "P1" else "stage1"] += r.get("cost_usd") or 0.0
    for r in jl(E_DIR / "raw" / "reference_repair.jsonl"):
        st = e_st.get(r["sentence_id"])
        if st:
            cost[st]["repair"] += r.get("cost_usd") or 0.0
    n_e = defaultdict(int)
    for st in e_st.values():
        n_e[st] += 1
    e_ps = {st: {k: v / n_e[st] for k, v in cost[st].items()} for st in cost}
    # E2 pilot panel (if it ran)
    e2p = defaultdict(lambda: defaultdict(float))
    for r in jl(ROOT / "work" / "panel_cache.jsonl"):
        if r["sentence_id"] in pilot:
            e2p[pilot[r["sentence_id"]]]["P1" if r["member"] == "P1" else "stage1"] += r.get("cost_usd") or 0.0
    panel_source = "stage 1 (P3+R1) from the E2 pilot; P1 adjudication and repair from E" if e2p else "E per-stratum measured costs (E2 panel pilot blocked by the run budget stop)"
    per_sent = {}
    for st in ("L25", "EXC", "DT"):
        est = e_ps.get(st if st != "DT" else "EXC", {})
        p1_share_pilot = 1.0  # E's pilot used 3 raters; production P1 only adjudicates: E's P1 cost already reflects that mix
        stage1 = e2p[st]["stage1"] / n_p[st] if e2p.get(st) and n_p.get(st) else est.get("stage1", 0.0)
        per_sent[st] = {"generation": round(gen_ps.get(st, 0.0), 5),
                        "panel_stage1": round(stage1, 5), "adjudication_P1": round(est.get("P1", 0.0) * p1_share_pilot, 5),
                        "reference_repair": round(est.get("repair", 0.0), 5)}
        per_sent[st]["total"] = round(sum(per_sent[st].values()), 5)
    ledger = sum(json.loads(l)["cost_usd"] for l in open(ROOT / "cost_ledger.jsonl")) if (ROOT / "cost_ledger.jsonl").exists() else 0.0
    counts = {"L25": 350, "EXC": 100, "DT": 100}
    remaining = {st: counts[st] - n_p.get(st, 0) for st in counts}
    proj = ledger + sum(per_sent[st]["total"] * remaining[st] for st in counts) + 0.6  # + drift-check remainder
    decision = "base design (350/100/100)"
    add_l25 = 0
    if proj <= 8.0:
        add_l25 = min(100, int((8.6 - proj) / per_sent["L25"]["total"])) if per_sent["L25"]["total"] > 0 else 0
        decision = f"SURPLUS: add {add_l25} L25 sentences from the pre-registered surplus order"
    elif proj > 9.5:
        decision = "SHRINK: EXC -> 75 first, then L25 toward 300"
    out = {"per_sentence_cost_usd": per_sent, "panel_cost_source": panel_source, "pilot_sentences": dict(n_p),
           "spent_so_far_usd": round(ledger, 4), "projected_total_usd": round(proj, 3), "decision": decision, "add_l25": add_l25,
           "E_per_sentence_costs_by_stratum": {k: {kk: round(vv, 5) for kk, vv in v.items()} for k, v in e_ps.items()},
           "note": "COST ONLY; no pilot label was inspected for this decision"}
    (ROOT / "pilot_projection.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
