#!/usr/bin/env python3
"""record.md (numbers pulled from results files by code) + tables/source_hashes.csv."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pandas as pd  # noqa: E402

from t8_paths import AUDIT3, DSE, E6T1, E7, E8, EV2, RES1, RESD, ROOT, RUN, TAB, sha256_file, write_csv  # noqa: E402

INPUTS = [EV2 / "pairwise_classes_E.jsonl", EV2 / "prereg_mech.json", EV2 / "src/consensus_mx.py", EV2 / "src/mechanism.py", EV2 / "src/pairwise.py",
          EV2 / "src/stats.py", EV2 / "src/frame.py", EV2 / "src/record.py", EV2 / "vendor_exp5/vendor_c/common.py", EV2 / "vendor_exp5/peer_text.py",
          EV2 / "tables/hypothesis_verdicts.csv", EV2 / "tables/m4_auroc_k_cost.csv", EV2 / "tables/label_facts.csv", EV2 / "tables/radj_gate.csv",
          EV2 / "tables/corrections.csv", EV2 / "tables/coverage_vs_request.csv", EV2 / "results/part_a.json",
          E8 / "results/pairs_E.jsonl", E8 / "results/analysis_hyb.json", E8 / "results/tables.md", E8 / "results/perturb_sensitivity.csv",
          E8 / "results/prereg_hyb.json", E8 / "results/selection.json", E8 / "results/deviations.json", E8 / ".aii_cost_ledger.jsonl",
          E6T1 / "results/per_item_T1.jsonl", E6T1 / "results/tables_T1.md", E6T1 / "results/verdict_T1.json", E6T1 / "results/api_cost_ledger.json",
          E6T1 / "results/deviations.json", E6T1 / ".aii_cost_ledger.jsonl",
          E7 / "results/rcomp_candidates.jsonl", E7 / "results/scores_FREE.jsonl", E7 / "results/scores_SIG.jsonl", E7 / "results/tables.md",
          E7 / "results/analysis.json", E7 / "results/deviations.json", E7 / ".aii_cost_ledger.jsonl",
          DSE / "full_data_out.json", AUDIT3 / "perturb_c_align_constant.json", RES1 / "research_report.md",
          RUN / "iter_3/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json",
          RUN / "iter_2/gen_art/gen_art_experiment_5/results/per_item_E.jsonl", RUN / "iter_2/gen_art/gen_art_experiment_5/data/E_labels.jsonl"]


def main() -> None:
    rows = [{"path": str(p), "exists": p.exists(), "sha256": sha256_file(p) if p.exists() else "MISSING_INPUT"} for p in INPUTS]
    write_csv(pd.DataFrame(rows), "source_hashes.csv", ["sha256 of every input read (READ-ONLY, absolute paths)"])
    p1 = json.loads((RESD / "part1.json").read_text())
    p2 = json.loads((RESD / "part2.json").read_text())
    p4 = json.loads((RESD / "part4.json").read_text())
    pw = json.loads((ROOT / "power_E2.json").read_text())
    C = pd.read_csv(TAB / "record_claims.csv", comment="#")
    pp3, pp9 = p1["pools"]["3pool"], p1["pools"]["9fam"]
    L = []
    L.append("# Verified record (T8, iteration 4)\n")
    L.append("Every number in the tables below is read from a source file by code (`src/t8_part4.py`). Each hypothesis-side literal is also "
             "checked to occur verbatim in the iteration-4 hypothesis §0 (`hyp_literal_found`). **Where they disagree, the SOURCE value wins.** "
             "E and R_COMP are DEVELOPMENT data, so everything in Parts 1-2 is mechanism/selection evidence, not confirmation. The claims wait for E2 in iteration 5.\n")
    L.append(f"## Claim check\n\n{p4['n_claims']} claims, {p4['n_match']} match, {p4['n_mismatch']} mismatch, {p4['n_not_in_files']} NOT_IN_FILES. "
             f"{int(C.match.isna().sum())} rows are context-only, with no hypothesis literal.\n")
    L.append("| table | item | hypothesis | literal in §0 | source | match |\n|---|---|---|---|---|---|")
    for r in C.itertuples():
        sv = r.source_value if not isinstance(r.source_value, float) else f"{r.source_value:.6g}"
        L.append(f"| {r.table} | {r.item} | {r.hypothesis_value} | {r.hyp_literal_found} | {str(sv)[:70]} | {r.match} |")
    L.append("\n### Mismatches and wording corrections (source wins)\n")
    for r in C[(C.match == False) | (~C.hyp_literal_found)].itertuples():  # noqa: E712
        L.append(f"- **{r.item}**: stated `{r.hypothesis_value}` vs source `{r.source_value}` ({r.source}). The literal is in §0: {r.hyp_literal_found}.")
    L.append("- **'26.8% of controls score c = 1'** is true only for the NON-RENAME controls. Across all controls, including RENAME_NONCE (100%) and RENAME_SYN (73.9%), the share is "
             f"{float(C[C.item.str.startswith('share of ALL controls')].source_value.iloc[0]):.1f}% (audit/perturb_c_align_constant.json).")
    L.append("- **Cost units.** SIG peer generation is $0.000116 per CANDIDATE and $0.00116 per SENTENCE (10 slots). Neither equals the plan's `$0.000996 per candidate`, and that "
             "literal does not occur in the hypothesis. `tables/cost_units.csv` gives every cost with an explicit unit column. Iteration-3 spend comes from the workspace "
             "`.aii_cost_ledger.jsonl` files: T1 $2.395, T2 $1.581, exp 8 $0.352, total $4.33. `results/costs.jsonl` of exp 7 holds only the judge calls ($1.04), which is why an earlier reading could come out low.\n")
    L.append("## New numbers from this artifact (for the paper; source files named)\n")
    L.append(f"- Part 1, 3-pool (PRIMARY): END_MAJ d {pp3['d_END_MAJ_this_pool']:.3f}; predicted d_floor {pp3['d_floor_pred']:.3f} "
             f"[{pp3['d_floor_pred_ci'][0]:.3f}, {pp3['d_floor_pred_ci'][1]:.3f}]; bracket [{pp3['d_bracket'][0]:.3f}, {pp3['d_bracket'][1]:.3f}]; "
             f"R_exact {pp3['d_R_exact']:.3f}; no-anchoring oracle floor {pp3['d_R_oracle']:.3f} (labelled-denominator {pp3['d_R_oracle_labdenom']:.3f}); "
             f"e_ceiling {pp3['e_ceiling_pred']:.3f} (`results/part1.json` pools.3pool).")
    L.append(f"- Part 1, 9-family: END_MAJ d {pp9['d_END_MAJ_this_pool']:.3f}; d_floor_pred {pp9['d_floor_pred']:.3f}; bracket [{pp9['d_bracket'][0]:.3f}, {pp9['d_bracket'][1]:.3f}]; "
             f"oracle {pp9['d_R_oracle']:.3f}.")
    L.append(f"- Part 2: SIG-minus-FREE cross-family exact-agreement drop {p2['drop_pairs']['exact']['overall']['mean']:.3f} "
             f"[{p2['drop_pairs']['exact']['overall']['ci'][0]:.3f}, {p2['drop_pairs']['exact']['overall']['ci'][1]:.3f}]; "
             f"share recovered post hoc: ALIGN {p2['recovered_share']['align']['share']:.3f}, NF {p2['recovered_share']['NF']['share']:.3f}, "
             f"ALIGN or NF {p2['recovered_share']['align_or_NF']['share']:.3f}. Validation of the Part-1 method: calibration error "
             f"{p2['validation']['R_point_MC']['calib_err']['mean']:+.3f} [{p2['validation']['R_point_MC']['calib_err']['ci'][0]:.3f}, "
             f"{p2['validation']['R_point_MC']['calib_err']['ci'][1]:.3f}], so NOT validated (the pass bar was |error| <= 0.05).")
    nn = pw["n_needed"]["L25"]["flashlite_disg"]
    L.append(f"- Part 3: L25 yield {pw['yield']['L25']['yield']:.2f}. Detecting +0.069 at 80% power needs ~{nn['usable_for_mde_0.069']:.0f} usable L25 sentences, i.e. ~{nn['planned_for_mde_0.069']:.0f} planned.\n")
    L.append("## Positioning paragraph (TO-BE-CHECKED)\n")
    L.append("What CSC adds beyond ARc (fixed schema), SIG (external vocabulary) and predicate-list prompting (2509.22338): predicate availability gives +15-20% for "
             "TRANSLATION, whereas CSC uses the candidate's predicate list for VERIFICATION. "
             "ARc scores the share of k translations that entail a candidate on a FIXED schema, and SIG hands every translator an EXTERNAL signature. CSC instead re-translates "
             "with the CANDIDATE's own vocabulary, so the verifier inherits whatever the candidate chose, which is where anchoring can enter. "
             "Part 2 shows an external shared vocabulary raises cross-family exact agreement from 0.05 to 0.53. Part 1 shows that, on E, most of the "
             "disagreement behind d is with peers labelled ERROR, which no vocabulary can fix without anchoring. **TO-BE-CHECKED** against 2509.22338 and ARc 2511.09008 before it is used in the paper.\n")
    (ROOT / "record.md").write_text("\n".join(L))
    print("record.md written")


if __name__ == "__main__":
    main()
