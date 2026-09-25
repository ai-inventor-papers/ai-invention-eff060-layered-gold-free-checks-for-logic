#!/usr/bin/env python3
"""analysis/tables.md: every number is read from a result file and printed with its source (file :: key path)."""
from __future__ import annotations

import json
from pathlib import Path

WS = Path(__file__).resolve().parents[1]
AN, SC, E2B = WS / "analysis", WS / "scores", WS / "e2b"


def load(p: Path):
    try:
        return json.loads(p.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def f(x, nd=3):
    if x is None:
        return "–"
    if isinstance(x, bool):
        return str(x)
    if isinstance(x, (int,)):
        return str(x)
    if isinstance(x, float):
        return f"{x:+.{nd}f}" if abs(x) < 1 and nd == 3 and x < 0 else f"{x:.{nd}f}"
    if isinstance(x, list) and len(x) == 2:
        return f"[{f(x[0])}, {f(x[1])}]"
    return str(x)


def main():
    L = []
    A = load(AN / "analysis_E2B.json") or {}
    V = load(AN / "confirm_verdict_E2B.json") or {}
    D = load(AN / "descriptive_nolabels_E2B.json") or {}
    U = load(AN / "union_longpool.json") or {}
    C = load(E2B / "census_E2B.json") or {}
    T = load(E2B / "testability_E2B.json") or {}
    L.append("# E2-B tables (every row: value — source file :: key)\n")
    L.append("## 0. Status\n")
    bs = load(E2B / "budget_stop_batches_complete.json")
    prog = [json.loads(l) for l in (E2B / "progress.jsonl").read_text().splitlines() if l.strip()] if (E2B / "progress.jsonl").exists() else []
    L.append(f"- label regime: {A.get('label_regime')} — analysis/analysis_E2B.json :: label_regime")
    L.append(f"- completed label batches (panel end to end): {[p['batch'] for p in prog]} — e2b/progress.jsonl")
    if bs:
        L.append(f"- run-budget stop: panel records moved aside from incomplete batches {bs.get('panel_records_moved_aside_from_incomplete_batches')} — e2b/budget_stop_batches_complete.json")
    L.append(f"- label counts (all LLM rows): {A.get('label_counts')} — analysis/analysis_E2B.json :: label_counts")
    L.append(f"- tier counts: {A.get('tier_counts')} — analysis/analysis_E2B.json :: tier_counts\n")
    L.append("## 1. Sample (selection)\n")
    e = C.get("E2B", {})
    L.append("| quantity | value | source |\n|---|---|---|")
    for k in ("n", "from_E2_surplus", "continuation", "word_bin_counts", "share_25_29", "mean_words", "mean_n_conditions"):
        L.append(f"| {k} | {e.get(k)} | e2b/census_E2B.json :: E2B.{k} |")
    L.append(f"| E2 pool reproduced (sha256 98cdccff…) | {C.get('e2_reproduction', {}).get('pool_ok')} | e2b/census_E2B.json :: e2_reproduction.pool_ok |")
    L.append(f"| collisions with E / E2 (all must be 0) | {C.get('collision_checks_all_zero')} | e2b/census_E2B.json :: collision_checks_all_zero |")
    L.append(f"| supply remaining after E2-B + reserve | {C.get('supply_remaining_after_E2B_and_reserve')} | e2b/census_E2B.json |\n")
    L.append("## 2. Testability (E's rule: >=50 ERROR, >=50 CORRECT, >=25 sentences each)\n")
    L.append("| cell | regime | CORRECT | ERROR | testable | source |\n|---|---|---|---|---|---|")
    for cell, v in (T.get("cells") or {}).items():
        if not cell.startswith("L25"):
            continue
        for reg in ("R_AB", "R_A", "R_VEX", "R_A_UNAUDITED"):
            x = v.get(reg, {})
            L.append(f"| {cell} | {reg} | {x.get('CORRECT_rows')} | {x.get('ERROR_rows')} | {x.get('testable')} | e2b/testability_E2B.json :: cells.{cell}.{reg} |")
    L.append("")
    pops = ["R_AB"]
    ap = (A.get("analysis_population") or {}).get("population")
    if ap and ap != "R_AB":
        pops.append(ap)
    for popn in pops:
      cname = f"L25_E2B_{popn}"
      head = ("## 3. Confirmatory E2-B cell (L25_E2B, R_AB; strat AUROC by word bin; sentence-cluster bootstrap B=2000)\n" if popn == "R_AB" else
              f"## 3b. EXPLORATORY cell {cname} (no-panel regime: CORRECT = z3-equivalent to the UNAUDITED MALLS gold; NOT testable by E's rule; "
              "structurally favours agreement-based metrics, see the label-coupling diagnostic)\n")
      L.append(head)
      cell = (A.get("cells") or {}).get(cname, {})
      if not cell.get("metrics"):
        L.append(f"NOT TESTABLE: {cell} — analysis/analysis_E2B.json :: cells.{cname}\n")
        continue
      L.append("| metric | strat AUROC [95% CI] | pooled | AUPRC | tie rate | n (ERR/COR) | source |\n|---|---|---|---|---|---|---|")
      for m, x in cell["metrics"].items():
        if x.get("strat_auroc") is None:
          continue
        L.append(f"| {m} | {f(x['strat_auroc'])} {f(x['strat_ci'])} | {f(x['pooled_auroc'])} | {f(x['auprc'])} | {f(x['tie_rate'])} | "
                 f"{x['n']} ({x['n_error']}/{x['n_correct']}) | analysis/analysis_E2B.json :: cells.{cname}.metrics.{m} |")
      L.append("\n| delta (paired rows) | point | 95% CI | n (COR, both-class sentences) | source |\n|---|---|---|---|---|")
      for k, d in cell.get("deltas", {}).items():
        if d.get("strat_delta") is None:
          continue
        L.append(f"| {k} | {f(d['strat_delta'])} | {f(d['strat_ci'])} | {d['n']} ({d['n_correct']}, {d['sentences_with_both_classes']}) | analysis/analysis_E2B.json :: cells.{cname}.deltas.{k} |")
      cd = A.get("label_coupling_diagnostic") or {}
      if popn != "R_AB" and cd.get("V0_decoupled"):
        L.append(f"\n- label-coupling diagnostic: V0 with gold-equivalent (CORRECT-labelled) peers removed: strat AUROC {f(cd['V0_decoupled'].get('strat_auroc'))} "
                 f"{f(cd['V0_decoupled'].get('strat_ci'))} vs V0 {f(cd['V0_same_rows'].get('strat_auroc'))}; V0_decoupled − flash-lite disg "
                 f"{f(cd['V0_decoupled - flashlite_disg'].get('strat_delta'))} {f(cd['V0_decoupled - flashlite_disg'].get('strat_ci'))} — analysis/analysis_E2B.json :: label_coupling_diagnostic")
      L.append("")
    L.append("\n## 4. Verdicts\n")
    for k, v in V.items():
        L.append(f"- **{k}**: {json.dumps(v, default=str)[:600]} — analysis/confirm_verdict_E2B.json :: {k}")
    L.append("\n## 5. Frontier (B4), H-MECH, rename, cost\n")
    for k in ("frontier_B4", "H_MECH", "rename", "cost", "system_tau_b", "placebo_shuffled_peers"):
        L.append(f"- **{k}**: {json.dumps(A.get(k), default=str)[:1200]} — analysis/analysis_E2B.json :: {k}")
    L.append("\n## 6. Label-free descriptives (no faithfulness claim)\n")
    for k in ("coverage_all", "concordance_V0_vs_flashlite_disg", "system_rankings", "agreement_structure", "rename_invariance_any_label",
              "distribution_by_word_bin"):
        L.append(f"- **{k}**: {json.dumps(D.get(k), default=str)[:1500]} — analysis/descriptive_nolabels_E2B.json :: {k}")
    L.append("\n### Coverage per system\n")
    L.append("| slot | system | parse rate | V0 scorable | flash-lite disg answered | mean V0 | source |\n|---|---|---|---|---|---|---|")
    for s, x in (D.get("coverage_per_system") or {}).items():
        L.append(f"| {s} | {x['system']} | {f(x['parse_rate'])} | {f(x['V0_scorable'])} | {f(x['flashlite_disg_ok'])} | {f((x.get('V0') or {}).get('mean'))} | "
                 f"analysis/descriptive_nolabels_E2B.json :: coverage_per_system.{s} |")
    L.append("\n## 7. Union with E2-A\n")
    L.append(f"- status: {U.get('status')} — analysis/union_longpool.json :: status")
    if U.get("fixed_sequence"):
        L.append(f"- fixed sequence verdicts: {U['fixed_sequence']['verdicts']} — analysis/union_longpool.json :: fixed_sequence.verdicts")
        L.append(f"- U1 wording: {U['fixed_sequence']['U1_wording']}")
        L.append(f"- heterogeneity: {json.dumps(U.get('heterogeneity'), default=str)[:800]} — analysis/union_longpool.json :: heterogeneity")
        L.append(f"- meta-analysis: {json.dumps(U.get('meta_analysis_fixed_effect'), default=str)[:800]} — analysis/union_longpool.json :: meta_analysis_fixed_effect")
    L.append("\n## 8. Checks\n")
    for n in ("code_freeze_check_E2B.json",):
        c = load(WS / "e2bsrc" / n) or {}
        L.append(f"- code freeze: {c.get('n_checked')} files checked, {c.get('n_mismatch')} mismatches — e2bsrc/{n}")
    r = load(E2B / "exp5_repro_check.json") or {}
    L.append(f"- exp-5 copy reproduces stored E scores: c_score_align {r.get('c_score_align_exact_matches')}/{r.get('n_rows')}, "
             f"p_peer_text {r.get('p_peer_text_exact_matches')}/{r.get('n_rows')} — e2b/exp5_repro_check.json")
    t = load(E2B / "T1_repro_check.json") or {}
    L.append(f"- exp-6 statistics reproduce T1: L25 {t.get('L25', {}).get('delta')} (expected 0.06942), long {t.get('long', {}).get('delta')} — e2b/T1_repro_check.json")
    s = load(SC / "score_seal.json") or {}
    L.append(f"- score seal: {len(s.get('files', {}))} files hashed at {s.get('sealed_at_utc')}, access violations {s.get('file_access_violations')} — scores/score_seal.json")
    L.append(f"- seals verified before the join: {A.get('seals')} — analysis/analysis_E2B.json :: seals")
    (AN / "tables.md").write_text("\n".join(L) + "\n")
    print(f"tables.md: {len(L)} lines")


if __name__ == "__main__":
    main()
