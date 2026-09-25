"""claims_ledger.csv (data role + the iteration-5 file that confirms each claim) and
reviewer_checklist.csv (critique -> action -> section anchor -> source -> CLOSED/PARTIAL)."""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from src import io_locators as L
from src.claims_spec import E6
from src.ctx import Ctx

G5 = "iter_5/gen_art/*/"
E2A, E2B, UNI, RC = "confirm_verdict_E2A.json", "confirm_verdict_E2B.json", "union_longpool.json", "confirm_verdict_rcomp.json"


def _p(c: Ctx, i: str) -> str:
    r = c._row(i)
    return r["source_value"]


def _ci(c: Ctx, i: str) -> str:
    return c._row(i).get("source_ci") or ""


def write_claims_ledger(c: Ctx, path: Path) -> list[dict]:
    n_rab = c.add("t1_n", L.json_key(E6, "a_head_on.R_AB pooled.n")[0], "0", f"{E6} :: a_head_on.R_AB pooled.n", "R_AB rows")
    n_err = c.add("t1_nerr", L.json_key(E6, "a_head_on.R_AB pooled.n_error")[0], "0", f"{E6} :: a_head_on.R_AB pooled.n_error", "R_AB ERROR")
    n_cor = c.add("t1_ncor", L.json_key(E6, "a_head_on.R_AB pooled.n_correct")[0], "0", f"{E6} :: a_head_on.R_AB pooled.n_correct", "R_AB CORRECT")
    n_sen = c.add("t1_nsent", L.json_key(E6, "a_head_on.R_AB pooled.n_sentences")[0], "0", f"{E6} :: a_head_on.R_AB pooled.n_sentences", "R_AB sentences")
    nE = f"{_p(c, n_rab)} ({_p(c, n_err)}/{_p(c, n_cor)}; {_p(c, n_sen)} sentences)"
    nP = f"{_p(c, 'x9_n')} ({_p(c, 'x9_nerr')}/{_p(c, 'x9_ncor')}; {_p(c, 'x9_nsent')} sentences)"
    R = []

    def add(cid, claim, ids, role, n, cf, field, rule):
        main = ids[0]
        R.append(dict(claim_id=cid, claim=claim, value=_p(c, main), CI=_ci(c, main), n=n, data_role=role,
                      source_path=c._row(main)["source_path"], numbers_csv_ids=";".join(ids),
                      confirming_file=cf, confirming_field=field, verdict_rule=rule))

    add("HP_a", "H-PRIMARY (a): frozen c_score_align beats the disguised flash-lite judge on the long pool (strat Δ)", ["t1_long", "t1_delta"], "DEV", nE,
        G5 + E2A, "longpool.delta_strat_flashlite_disg.ci", "CONFIRM iff E2 long-pool CI > 0 AND point > 0 vs flash-lite original and nano")
    add("HP_a_union", "H-PRIMARY (a), pooled E2 + E2-B long pool", ["t1_long"], "CONFIRM-PENDING", "pending", G5 + UNI, "union.delta_strat_flashlite_disg.ci", "union CI > 0; heterogeneity reported")
    add("HP_a_B", "H-PRIMARY (a) replication on E2-B (second L25 sample)", ["t1_l25"], "CONFIRM-PENDING", "pending", G5 + E2B, "longpool.delta_strat_flashlite_disg.ci", "same rule as E2-A")
    add("HP_b", "H-PRIMARY (b): nested [S4 + c] − S4 strat gain", ["t1_nested"], "DEV", nE, G5 + E2A, "nested.delta_strat.ci", "CI > 0 on E2")
    add("HP_c", "H-PRIMARY (c): within-template c_score_align − flash-lite on R_COMP FREE untouched (disguised AND original)", ["d5_cor"], "CONFIRM-PENDING",
        f"untouched rows {_p(c, 'd5_untouched')}; CORRECT currently {_p(c, 'd5_cor')}", G5 + RC, "criterion_c.delta_within_template.ci", "testable iff >= 50 CORRECT; CI > 0 both views")
    add("L25", "L25 stratum Δ vs flash-lite disguised (user priority)", ["t1_l25"], "DEV", nE, G5 + E2A, "L25.delta_strat_flashlite_disg", f"reported with power (MDE80 {_p(c, 'pw_mde')})")
    add("EXC", "EXC stratum Δ", ["t1_exc"], "DEV", nE, G5 + E2A, "EXC.delta_flashlite_disg", "descriptive (EXC-core supply exhausted, D3)")
    add("frontier", "frontier ratio c / frontier judge (0.95 bar)", ["t1_ratio"], "DEV", "284 (frame)", G5 + E2B, "frontier.ratio.ci", "point only unless CI lower > 0.95")
    add("frontier_cost", "frontier judge costs many times consensus per item", ["rv_frontier_x"], "DESCRIPTIVE", "cost ledgers", "none (DEV only)", "", "unit-stated")
    add("m3", "M3: consensus degrades less with length than the judge", ["t1_m3_boot", "t1_m3_gee"], "DEV", nE, "none (DEV only)", "", "INCONCLUSIVE: specifications conflict")
    add("did", "flash-lite contamination DiD", ["t1_did"], "DEV", "GOLDSYS 240 vs E", "none (DEV only)", "", "marginal")
    add("t2_sig", "SIG within-template AUROC (controlled vocabulary)", ["t2_sig", "t2_judge"], "OUT-OF-SCOPE-SIG", "2,024 rows / 221 sentences", "none (DEV only)", "", "never evidence for the operating condition")
    add("sigproxy", "SIGPROXY k=3 within-template AUROC; d cued vs uncued", ["x10_sigproxy", "x10_d_diff"], "OUT-OF-SCOPE-SIG", "2,024 rows; 74 bases", "none (DEV only)", "", "out of scope")
    add("MECH_i", "H-MECH (i): >= 50% of non-agreeing peers of CORRECT candidates are labelled ERROR", ["e3_77", "e3_61"], "DEV", "25,358 pairs (9-family)", G5 + "hmech_E2.json", "i.share_peer_error", "CONFIRMED iff >= 0.50 on E2")
    add("MECH_ii", "H-MECH (ii): SCATTER ratio SI_cor/SI_err >= 2", ["ev2_scatter"], "DEV", "141 sentences", G5 + "hmech_E2.json", "ii.scatter_ratio", "CONFIRMED iff >= 2")
    add("MECH_iii", "H-MECH (iii): NET Δ(e+d) over word terciles > 0 (degradation)", ["ev2_net"], "DEV", nE, G5 + "hmech_E2.json", "iii.net_delta.ci", "CONFIRMED iff > 0")
    add("MECH_iv", "H-MECH (iv): ALIGN lowers d and raises e (MEANING_RENAME-type e, FREE_ALIGN vs exact)", ["x9_t9b_mr_fa", "x9_t9b_mr_fx", "x9_full_d_fa", "x9_full_d_fx"], "DEV",
        "FULL 2,686 rows; 221 MR-type errors", G5 + "hmech_E2.json", "iv.align_vs_exact", "CONFIRMED iff ALIGN d lower AND e higher on MR-type and ADD/DROP")
    add("vocab_refuted", "only a small share of correct-correct disagreement is vocabulary-resolvable (vocabulary diagnosis refuted on E)", ["e3_9"], "DEV", "9-family pairs", G5 + "hmech_E2.json", "i.vocab_share", "descriptive")
    add("IMPROVE", "H-IMPROVE: the carried wrong-peer-discounting variant beats V0 on the E2 long pool", ["t1_long"], "CONFIRM-PENDING", "5 variants screened on E",
        G5 + "freeze/selection.json", "winner", "CONFIRMED iff variant − V0 strat CI > 0 on E2 long pool (improve_E2.json)")
    add("IMPROVE_E2", "H-IMPROVE on E2", ["t1_long"], "CONFIRM-PENDING", "pending", G5 + "improve_E2.json", "delta_vs_V0.ci", "CI > 0")
    add("RENAME", "H-RENAME: gloss-gated agreement passes the dev gate and has RENAME_SYN flip <= 0.05 on E2", ["x10_flip_syn"], "CONFIRM-PENDING", "PERTURB E bases",
        G5 + "freeze/gg_gate.json", "gate.pass", "CONFIRMED only if dev gate PASS AND E2 flip <= 0.05 AND AUROC >= c_score_align − 0.01 (rename_E2.json)")
    add("RENAME_E2", "H-RENAME on E2", ["x10_flip_syn"], "CONFIRM-PENDING", "pending", G5 + "rename_E2.json", "RENAME_SYN.flip", "<= 0.05")
    add("boundary", "boundary: c_align PERTURB NONCE/SYN FA with paired flips", ["e8_calign_nonce", "e8_calign_syn", "x10_flip_nonce", "x10_flip_syn"], "DEV", "E bases 110 / 88",
        "none (DEV only)", "", "reported as a measured boundary if GG fails")
    add("rename9", "9-peer c_score_align rename ΔFA under WordNet synonyms", ["x9_t15_d"], "DEV", "E SYN rows", G5 + "rename_E2.json", "c_score_align.delta_FA", "descriptive")
    add("errtype", "error typing is NEGATIVE outside a shared vocabulary (free3 on E; medoid ≈ judge)", ["x10_free3", "e8_typ_medoid", "e8_typ_judge"], "DEV", "2,688 E mutants", "none (DEV only)", "", "no new budget")
    add("oracle_typing", "gold-using oracle typing accuracy", ["x10_oracle", "e8_typ_oracle"], "GOLD-USING-ORACLE", "2,688 E mutants", "none (DEV only)", "", "not a gold-free metric")
    add("csc", "CSC strat AUROC (provisional negative)", ["x9_csc"], "DEV", nP, "none (DEV only)", "", "CLOSED; provisional, completion-selected")
    add("csc_anchor", "CSC anchoring: e rises while d falls", ["x9_e_csc", "x9_e_fx", "x9_d_csc", "x9_d_fx"], "DEV", nP, "none (DEV only)", "", "descriptive")
    add("csc_mr", "MEANING_RENAME-type Δe CSC − FREE_ALIGN", ["x9_t9_mr_d"], "DEV", f"{_p(c, 'x9_t9_mr_n')} errors", "none (DEV only)", "", "NOT_READ")
    add("free_recall", "FREE-consensus mutant recall ≈ 1 with base FA 0.71–0.99 (trivial)", ["x10_bfa_calign", "x10_bfa_fx_e", "x10_bfa_fx_r", "x10_bfa_fa_r"], "DEV", "E 198/173; R_COMP 74 bases",
        "none (DEV only)", "", "descriptive")
    add("local2", "LOCAL2 endorsement is insufficient-peer ties", ["x10_l2_tie", "x10_l2_excl_own"], "DEV", "381 mutants", "none (DEV only)", "", "descriptive")
    add("k95", "k95 = 3 overall, 5 in the long tercile", ["ev2_k95", "ev2_k95_t3"], "DEV", "2,014 rows", G5 + E2A, "k_curve.k95", "descriptive")
    add("cost_cons", "consensus FULL $ per candidate", ["cost_cons"], "DESCRIPTIVE", "T1 ledger", G5 + E2A, "cost.full_usd_per_candidate", "unit-stated")
    add("cost_k3", "3-family pool $ per sentence", ["cost_k3"], "DESCRIPTIVE", "eval-2", "none (DEV only)", "", "unit-stated")
    add("cost_flash", "flash-lite judge $ per item-call", ["cost_flash"], "DESCRIPTIVE", "T1 ledger", "none (DEV only)", "", "unit-stated")
    add("cost_csc", "CSC G5 $ per candidate", ["x9_g5", "x9_g5_dd"], "DESCRIPTIVE", "exp-9 ledger", "none (DEV only)", "", "PASS (PROVISIONAL)")
    add("cost_e2", "E2 L25 $ per sentence (projection)", ["d4_pilot_usd"], "DESCRIPTIVE", "pilot", "none (DEV only)", "", "projection")
    add("drift", "E2 panel drift stop rule", ["d4_comb", "d4_repl", "d4_flag_today", "d4_flag_E"], "DESCRIPTIVE", "22 unambiguous track-H judgements",
        G5 + "e2/E2_DRIFT_DECISION.json", "decision", "PASS/FAIL decided by E2-A")
    add("power", "E2 alone is underpowered for L25 (MDE80)", ["pw_mde", "pw_882", "pw_237"], "DESCRIPTIVE", "planned 350 L25", G5 + UNI, "mde80", "descriptive")
    add("rcomp_labels", "old iter-3 FREE labels over-call ERROR (up to)", ["d5_707", "d5_kappa"], "DESCRIPTIVE", "420 old ERROR rows", G5 + RC, "labels.final_counts", "descriptive")
    add("audit_prec", "ERROR_CERT audit precision", ["d5_prec"], "DESCRIPTIVE", "60 rows", G5 + "audit_report.json", "precision", "descriptive")
    add("calib", "post-hoc vocabulary instruments under-count (calibration error)", ["e3_calib"], "DEV", "2,010 rows", "none (DEV only)", "", "NOT VALIDATED")
    add("oracle_floor", "no-anchoring oracle d floor (3-pool; L25)", ["e3_oracle3", "e3_oracle_l25"], "GOLD-USING-ORACLE", "3-pool", "none (DEV only)", "", "oracle, uses labels")
    add("tau", "system-level τ-b: CSC vs c_score_align", ["x9_t14_csc", "x9_t14_ca"], "DEV", "13 system×variant rows", G5 + E2A, "system_level.tau_b", "descriptive")
    add("coverage", "PERTURB coverage", ["e8_cov_ok", "e8_cov_n"], "DESCRIPTIVE", "5,402 rows", G5 + E2A, "coverage", "unparseables in the denominator")
    cols = ["claim_id", "claim", "value", "CI", "n", "data_role", "source_path", "numbers_csv_ids", "confirming_file", "confirming_field", "verdict_rule"]
    with path.open("w", newline="") as f:
        f.write("# source: values from numbers.csv rows named in numbers_csv_ids; confirming_file/field = iteration-5 sibling output contract (iter_5/gen_strat/gen_strat_1); field names are PROPOSED where the contract names only the file\n")
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in R:
            w.writerow(r)
    return R


CRIT_ACTIONS = {
    1: ("Apply eval-3 Part 4 in place (§3.3–§3.6, IDs, verdicts, prior art, coverage, iter-1/2 items, held-out E)", "sections 1–7, 16, 17"),
    2: ("Re-transcribe §4.2 with verbatim CIs, T9/T9b, prereg gate text, M3 both specs, NET within-arm, n.s. marks", "section 9 (+ gates in 6, 8)"),
    3: ("Population/selection paragraph, FREE_exact + FREE_ALIGN columns, T8/T10/T14/T15/T17 + HYB_MEAN, 'provisional negative'", "section 9"),
    4: ("Base FA next to every recall, paired flips, LOCAL2 ties, judge 12.4% ≠ END_MAJ e, free3 on E, oracle gold-using, controls by source, T4/T8", "section 10"),
    5: ("Rewrite §4.6 from eval 3: wrong-peer decomposition, instruments under-count, 0.683 is d, oracle floors, c_vres, placebo, NET, power", "sections 12, 17"),
    6: ("E2 drift UNDECIDED + 0.12 vs 0.84 on n = 22, D0–D7; 'up to 70.7%', kappa, rescue by template, D1–D9; §3.3 VOID marker", "sections 2, 11"),
    7: ("Coverage-against-request table with one-line answers; rank R_COMP FREE gloss and E2 completion first", "section 16 (+ skeleton)"),
    8: ("§4.1 reasoning block and iteration-4 spend table", "sections 8, 14"),
    9: ("Prior-art section with scoop rule and C1–C5; Vossel/ARc and Chen & Avizienis sentences", "section 7"),
    10: ("Extend dead-ends table; correct the c_nf reason", "section 15"),
    11: ("One cost table with units; correct §3.5/§3.6 in place; tercile k95 in the summary", "sections 3, 13, 17"),
}


def write_checklist(c: Ctx, path: Path, lint_fails: list) -> list[dict]:
    rv = json.loads(L._read_text(L.REVIEW))
    by_crit: dict[int, list] = {}
    for m in c.markers:
        for k in str(m.get("critique", "")).replace(" ", "").split(","):
            if k.isdigit():
                by_crit.setdefault(int(k), []).append(m)
    rows = []
    for k, cr in enumerate(rv["critiques"], 1):
        action, anchor = CRIT_ACTIONS[k]
        ms = by_crit.get(k, [])
        nf = [m for m in ms if m["status"] != "OK"]
        status, note = "CLOSED", ""
        if k == 7:
            status, note = "PARTIAL", "the text is written; the substantive gap (no testable long-sentence / free-vocabulary result) is closed only by the iteration-5 siblings"
        elif k == 8:
            status, note = "PARTIAL", "reasoning block and spend table written; part of the $7 phase budget stays unaccounted because no ledger in the run tree records it"
        elif nf:
            status, note = "CLOSED", f"{len(nf)} targeted original sentence(s) not present in paper_draft.md (nothing to strike): " + "; ".join(m['what'][:60] for m in nf)
        if lint_fails:
            status, note = "PARTIAL", note + f" lint failures {len(lint_fails)}"
        srcs = sorted({m["source"] for m in ms})
        rows.append(dict(critique=k, category=cr["category"], severity=cr["severity"], summary=cr["description"][:160].replace("\n", " "),
                         action=action, section_anchor=f"record_final.md {anchor}", n_markers=len(ms),
                         sources="; ".join(srcs)[:900], status=status, note=note))
    cols = list(rows[0].keys())
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return rows
