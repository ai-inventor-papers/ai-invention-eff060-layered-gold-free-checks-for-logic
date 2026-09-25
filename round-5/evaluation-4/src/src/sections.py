"""record_final.md: 17 paste-ready sections. No numeric literal appears in these templates; every
number is rendered through Ctx.v / Ctx.ci / Ctx.vc from a numbers.csv row (HTML tag <!-- n:id -->),
copied verbatim from a source table row (tag <!-- v:file -->), or sits inside a struck quote of the
original paper text (~~...~~) or inside backticks (definitions, model ids, paths)."""
from __future__ import annotations

import json
import re
from pathlib import Path

from src import checker as CK
from src import io_locators as L
from src.claims_spec import A9, CU, D4, D5, E8, EV2, EV3, PC, X10, X9
from src.ctx import Ctx, src_line, verbatim_table

RUN = L.RUN
T = f"{EV3}/tables"
OLA = f"{D5}/results/old_label_agreement.json"
REVIEW = L.REVIEW
ARTIFACT_IDS_PLAN = ["art_d0njuqy2Csj-", "art_i3cVDxBp-USk", "art_elDZY26Pu6GD", "art_U4Hsqt4Ay9Tg", "art_TaxJRnPcJMuZ",
                     "art_zcwCQgTqk6DN", "art_HepAw8c6Eu7-", "art_7GxreYjATkC5", "art_cxnoDYQNFolW", "art_YYD-HDzfQfEj",
                     "art_FWy8D4_y9GBn", "art_VIF75I5R6f0v", "art_BvAL_KZTZuw8", "art_D7k2ZWgE3nVd", "art_pAmLrGqsmFUx",
                     "art_2OmxzMInZZJY", "art_Ia_FT284H33j"]
PLACEHOLDER_ALIAS = {"art_T1_API_bar": "T1 / exp 6", "art_R_COMP": "T2 / exp 7 (R_COMP)",
                     "art_PERTURB_scoring": "exp 8", "art_evaluation_2": "eval 2"}


def s01_perturb(c: Ctx) -> str:
    c.section = "S1"
    rows = []
    for m in ("c_align", "c_nf", "c_hyb", "judge_cheap_disg", "p_peer_text", "p_text", "l3_z3", "S4_local"):
        cells = []
        for fam in ("RENAME_NONCE", "RENAME_SYN"):
            cells += [c.vc(f"pc_{m}_{fam}_fa"), c.v(f"pc_{m}_{fam}_base"), c.v(f"pc_{m}_{fam}_flip")]
        rows.append(f"| `{m}` | " + " | ".join(cells) + " |")
    note = L.csv_cell(PC, {"metric": "c_align", "family": "BASE"}, "note")[0]
    out = f"""## 1. §3.4 PERTURB sensitivity and the rename trade-off (corrected)

{c.replaces('### 3.4')}

{c.strike(r'^MEANING_RENAME is the false-alarm diagnostic', 'MEANING_RENAME replaces a predicate by one with a DIFFERENT meaning; it is an ERROR operator, not a meaning-preserving rewrite. A within-base AUROC near chance on it means the metric is BLIND to a real error class (c_nf ' + c.v('e8_cnf_mr') + '), not that it is rename-invariant', f'{T}/perturb_corrected.csv', critique='1')}

{c.strike(r'^The consensus metric is polarity-symmetric', 'deleted: per-operator consensus within-base AUROC is a base-endorsement artefact (most mutants of a flagged base sit at the maximum score), so neither an operator ranking nor a polarity-symmetry claim can be read from it', f'{T}/perturb_corrected.csv', critique='1')}

{c.strike(r'^c_align achieves within-base AUROC ≥ 0\.84 on every testable operator', 'no per-operator ranking is reported for consensus scores (artefact above); the recall at the PRIMARY threshold is flat across operators (c_align NEG ' + c.v('pc_calign_recall_NEG') + ', SWAP ' + c.v('pc_calign_recall_SWAP') + ', DROP ' + c.v('pc_calign_recall_DROP') + ', ADD ' + c.v('pc_calign_recall_ADD') + ', MEANING_RENAME ' + c.v('pc_calign_recall_MEANING_RENAME') + ')', f'{T}/perturb_corrected.csv', critique='1')}

{c.strike(r'It is polarity-symmetric \(\|DOWN − UP\| < 0\.01\)', 'deleted (same artefact)', f'{T}/perturb_corrected.csv', critique='1')}

**Corrected text.** The eval-3 note on the source table reads verbatim: "{note}"<!-- v:perturb_corrected.csv -->. MEANING_RENAME is therefore typed as an ERROR operator throughout. The name-free score `c_nf` is blind to it (within-base AUROC {c.v('e8_cnf_mr')}), which, together with the failed pre-registered selection below, is what ended the name-free line.

**Invariance on meaning-preserving renames of CORRECT E bases** (FA = share flagged; the paired base FA and the flip rate separate rename sensitivity from base over-flagging; development data):

| metric | NONCE FA [CI] | NONCE base FA | NONCE flip | SYN FA [CI] | SYN base FA | SYN flip |
|-|-|-|-|-|-|-|
{chr(10).join(rows)}

**Pre-registered rename-invariant selection FAILED** (exp 8 `selection.json`; the pre-registered selection rule uses FA only, no paired flip): HYB PERTURB RENAME_SYN / NONCE FA {c.v('e8_hyb_syn')} / {c.v('e8_hyb_nonce')}; NF-anchored {c.v('e8_nf_syn')} / {c.v('e8_nf_nonce')}; both INELIGIBLE, nothing was frozen.

**Coverage (T11).** {c.v('e8_cov_ok')} of {c.v('e8_cov_n')} PERTURB rows were scored by the consensus family; the rest are R_COMP rows without peers or rows whose peers were unavailable, counted, not dropped.

{src_line([f'{T}/perturb_corrected.csv', f'{E8}/perturb_sensitivity.csv', f'{E8}/selection.json', f'{E8}/coverage_perturb.csv'])}
"""
    return out


def s02_t2(c: Ctx) -> str:
    c.section = "S2"
    return f"""## 2. §3.3 T2 on R_COMP: NOT CONFIRMED (corrected)

{c.replaces('### 3.3')}

{c.strike(r'\*\*T2 CONFIRMED: consensus dominates on R_COMP\.\*\*', 'T2 is NOT CONFIRMED under the §3.1 rule: SIG passes (within-template ' + c.v('t2_sig') + ' vs ' + c.v('t2_judge') + '; vs the ORIGINAL judge ' + c.v('t2_vs_orig') + ') but SIG is the controlled-vocabulary regime the user excluded, and FREE was NOT_TESTABLE', f'{T}/t2_record.csv', critique='1')}

{c.strike(r'The FREE tier-A delta is \+0\.214', 'the FREE tier-A deltas in this section are VOID: those labels over-call ERROR (' + c.v('t2_free_mapped') + ' of ' + c.v('t2_free_err') + ' old ERROR rows are MAPPED by the name-free search)', OLA, critique='6')}

{c.strike(r'The frontier judge costs \$0\.00605 per call', 'unit error: per ITEM the frontier judge costs ' + c.v('rv_frontier_x') + '× the consensus score (FULL, per candidate); see the single cost table (section 13)', f'{T}/cost_units.csv', critique='11')}

**Corrected text.** On R_COMP SIG (out-of-scope controlled vocabulary; development data) `c_score_sig` reaches within-template AUROC {c.v('t2_sig')} against the disguised flash-lite judge's {c.v('t2_judge')}; against the ORIGINAL (undisguised) judge the gap is {c.v('t2_vs_orig')}. This is the regime the user excluded, so it cannot confirm the operating condition. The in-scope FREE condition was NOT_TESTABLE in iteration 3, and the iteration-3 FREE tier-A labels were later shown to over-call ERROR (UP TO {c.v('d5_707')} of old ERROR rows are MAPPED; MAPPED is an upper bound of CORRECT). Verdict: **T2 NOT CONFIRMED**; criterion (c) is pending on R_COMP FREE in iteration 5 (`confirm_verdict_rcomp.json`).

{src_line([f'{T}/t2_record.csv', OLA, f'{T}/cost_units.csv'])}
"""


def s03_mech(c: Ctx) -> str:
    c.section = "S3"
    hv = f"{EV2}/tables/hypothesis_verdicts.csv"
    m1 = L.csv_cell(hv, {"clause_id": "M1"}, "clause_text")[0]
    m2 = L.csv_cell(hv, {"clause_id": "M2"}, "clause_text")[0]
    m3 = L.csv_cell(hv, {"clause_id": "M3"}, "clause_text")[0]
    m4 = L.csv_cell(hv, {"clause_id": "M4"}, "clause_text")[0]
    return f"""## 3. §3.5 Mechanism verdicts under the PRE-REGISTERED definitions (corrected)

{c.replaces('### 3.5')}

{c.strike(r'\*\*M1 \(Anna Karenina\)', 'M1 was pre-registered and tested; its pre-registered text is given below with verdict INCONCLUSIVE', f'{EV2}/prereg_mech.json', whole=True, critique='1')}

{c.strike(r'^\*\*M2 \(endorsement/divergence decomposition\)', 'M2 is pre-registered as a slope claim (CONFIRMED but non-specific), not the e/d bookkeeping identity', f'{EV2}/tables/hypothesis_verdicts.csv', whole=True, critique='1')}

{c.strike(r'^\| 1 \| 0\.685 \| \$0\.000024 \|', 'the cost column was per-candidate arithmetic mislabelled as per sentence; per-sentence k-pool costs are in the table below', f'{T}/cost_units.csv', whole=True, critique='1, 11')}

{c.strike(r'^This has practical significance: a consensus metric with 3 peer families costs', 'unit error: a 3-family pool costs ' + c.v('cost_k3') + ' per SENTENCE (FULL), vs flash-lite ' + c.v('cost_flash') + ' per item-call', f'{T}/cost_units.csv', critique='11')}

**Corrected text (pre-registered definitions, eval 2 `prereg_mech.json`; development data E):**

- **M1** "{m1}"<!-- v:hypothesis_verdicts.csv -->: **{c.v('ev2_m1')}**.
- **M2** "{m2}"<!-- v:hypothesis_verdicts.csv -->: **CONFIRMED but non-specific**: the shuffled-label placebo also passes (eval-2 README), so M2 alone does not show a label-specific mechanism.
- **M3** "{m3}"<!-- v:hypothesis_verdicts.csv -->: owned by T1, where it is **INCONCLUSIVE** because its two specifications conflict (bootstrap {c.vc('t1_m3_boot')}{c.ns('t1_m3_boot')} vs stacked GEE {c.vc('t1_m3_gee')}); the local-judge version (M3-local) is secondary.
- **M4** "{m4}"<!-- v:hypothesis_verdicts.csv -->: **CONFIRMED**, k95 = {c.v('ev2_k95')} overall; by words tercile k95 = {c.v('ev2_k95_t1')} / {c.v('ev2_k95_t2')} / {c.v('ev2_k95_t3')}: long sentences need more peers.
- **NET** Δ(e+d), words T3 − T1: {c.vc('ev2_net')}: consensus DEGRADES with length, driven by d (Δd {c.v('ev2_net_dd')}, Δe {c.v('ev2_net_de')}).
- **SCATTER** SI_cor / SI_err {c.vc('ev2_scatter')}; graded − binary AUROC {c.vc('ev2_graded')}.

| k | AUROC | AUROC words T3 | $ per SENTENCE (FULL, peer generation) |
|-|-|-|-|
| 1 | {c.v('ev2_k1')} | {c.v('ev2_k1_T3')} | {c.v('cost_k1')} |
| 3 | {c.v('ev2_k3')} | {c.v('ev2_k3_T3')} | {c.v('cost_k3')} |
| 5 | {c.v('ev2_k5')} | {c.v('ev2_k5_T3')} | {c.v('cost_k5')} |
| 7 | {c.v('ev2_k7')} | {c.v('ev2_k7_T3')} | {c.v('cost_k7')} |

{src_line([f'{EV2}/results/part_a.json', f'{EV2}/tables/hypothesis_verdicts.csv', f'{EV2}/prereg_mech.json', f'{EV2}/README.md', f'{T}/cost_units.csv'])}
"""


def s04_iter12(c: Ctx) -> str:
    c.section = "S4"
    path = f"{T}/corrections_iter12.csv"
    items = [
        (r"\+0\.024 \[−0\.075, 0\.111\], not significant", "C4: under panel labels the frontier-judge advantage STRENGTHENS (see corrections_iter12.csv row C4)"),
        (r"The frontier judge \(Gemini 3\.1 Pro\) adds nothing significant over the cheap judge", "C4: the frontier advantage is n.s. only under solver labels; under panel labels it STRENGTHENS"),
        (r"reversing the non-significant iteration-1 finding", "'reversing' overstates: the iteration-1 solver-label advantage was already positive; the panel-label result STRENGTHENS it (C4)"),
        (r"588 common items", "the common-set size must be read from evaluation 1's tables (corrections_iter12.csv)"),
        (r"fitted under solver labels", "the fused score was calibrated on track H, not 'fitted under solver labels' (corrections_iter12.csv)"),
    ]
    marks = "\n\n".join("- " + c.strike(p, w, path, critique="1") for p, w in items)
    tbl = verbatim_table(path, ["id", "claim_as_reported", "corrected_value", "verified"], "corrections_iter12.csv", max_cell=260)
    return f"""## 4. Iteration-1/2 corrections applied in place

Replaces: the listed sentences in paper_draft.md §1.4, §1.5 and §2.5 (line numbers in each marker).

{marks}

The corrections table (verbatim; every row machine-verified by eval 3 against its source path):

{tbl}

{src_line([path])}
"""


def s05_ids(c: Ctx) -> tuple[str, list[dict]]:
    c.section = "S5"
    idmap = {r["placeholder"]: r["artifact_id"] for r in L._csv_rows(f"{T}/artifact_id_map.csv")}
    valid = set(v for v in idmap.values() if v) | set(ARTIFACT_IDS_PLAN)
    res = []
    for i, ln in enumerate(CK.paper_lines(), 1):
        for m in re.finditer(r"\[ARTIFACT:([^\]]+)\]", ln):
            pid = m.group(1)
            if pid in valid:
                res.append(dict(line=i, placeholder=pid, new=pid, status="VALID"))
            elif pid in PLACEHOLDER_ALIAS and idmap.get(PLACEHOLDER_ALIAS[pid]):
                res.append(dict(line=i, placeholder=pid, new=idmap[PLACEHOLDER_ALIAS[pid]], status="RESOLVED",
                                via=PLACEHOLDER_ALIAS[pid]))
            else:
                res.append(dict(line=i, placeholder=pid, new="", status="UNRESOLVED"))
    rows = "\n".join(f"| L{r['line']} | `{r['placeholder']}` | `{r['new'] or '—'}` | {r['status']} |" for r in res)
    sed = "\n".join(f"sed -i '{r['line']}s/\\[ARTIFACT:{re.escape(r['placeholder'])}\\]/[ARTIFACT:{r['new']}]/' paper_draft.md"
                    for r in res if r["status"] == "RESOLVED")
    n_res = c.add("ids_resolved", sum(r["status"] == "RESOLVED" for r in res), "0", f"{L.PAPER} :: regex \\[ARTIFACT:...\\] vs {T}/artifact_id_map.csv", "placeholders resolved")
    n_unres = c.add("ids_unresolved", sum(r["status"] == "UNRESOLVED" for r in res), "0", f"{L.PAPER} :: regex", "placeholders unresolved")
    n_all = c.add("ids_total", len(res), "0", f"{L.PAPER} :: regex", "artifact markers in paper")
    miss = sorted(set(ARTIFACT_IDS_PLAN) - {r["new"] for r in res})
    out = f"""## 5. Placeholder → real artifact IDs

Replaces: every `[ARTIFACT:...]` marker in paper_draft.md ({c.v(n_all)} markers; {c.v(n_res)} placeholders resolved from `artifact_id_map.csv`, {c.v(n_unres)} unresolved; no ID is invented).

| paper line | marker | replacement | status |
|-|-|-|-|
{rows}

Sed-ready list (run in the paper directory):

```
{sed}
```

Artifacts with NO marker in the paper (the paper step must add one where their results are cited): {', '.join(f'`{m}`' for m in miss)}. The research artifact `art_VIF75I5R6f0v` gets its own section (section 7 below).

{src_line([L.PAPER, f'{T}/artifact_id_map.csv'])}
"""
    return out, res


def s06_verdicts(c: Ctx) -> str:
    c.section = "S6"
    tbl = verbatim_table(f"{T}/hypothesis_verdicts_iter3.csv", ["clause", "corrected_verdict_iter4_hypothesis", "reason"],
                         "hypothesis_verdicts_iter3.csv", max_cell=220)
    gp = json.loads(Path(f"{X10}/csc_gate_P.json").read_text())
    gp_s = "; ".join(f"{k}: {v.get('verdict', '') if isinstance(v, dict) else v}" for k, v in gp.items() if k in ("G3_P", "G4", "MT")) or "see file"
    return f"""## 6. §3.7 Hypothesis verdicts (new section)

Insert after §3.6. Iteration-3 rows verbatim from eval 3 Part 4:

{tbl}

Iteration-4 rows (development data E / PERTURB; PROVISIONAL where stated):

| clause | verdict | source |
|-|-|-|
| CSC G1 (d ≤ `0.35` AND non-positive words slope) | FAIL: d {c.v('x9_g1_d')}, slope {c.vc('x9_g1_slope')} | `csc_gate_E.json` |
| CSC G2 (`strat AUROC(CSC) ≥ c_score_align − 0.01` on R_AB AND pooled AUROC(CSC) > c_score_align on L25) | NOT_READ ({c.v('x9_g2')}): R_AB part FAIL; L25 cell below `50/50` (Δ {c.vc('x9_g2_l25')}, not read) | `csc_gate_E.json` |
| CSC G3-E (RENAME_SYN FA gate, flip not computed) | {c.v('x9_g3')} | `csc_gate_E.json` |
| CSC G4 | null on E (sibling arm) | `csc_gate_E.json` |
| CSC G5 (FULL $/candidate ≤ `$0.002`) | PASS (PROVISIONAL): {c.v('x9_g5')} per candidate; deduped {c.v('x9_g5_dd')} | `csc_gate_E.json`, `results/analysis.json g_cost` |
| exp-10 G3-P / G4 / MT | UNTESTED (0 CSC peers generated; budget) — {gp_s}<!-- v:csc_gate_P.json --> | `csc_gate_P.json` |
| E2 confirmation cells | NOT TESTABLE ({c.v('d4_cor')} CORRECT rows) | `testability_E2.json`, `sealed/labels_E2.jsonl` |
| R_COMP FREE criterion (c) | NOT TESTABLE ({c.v('d5_cor')} CORRECT rows; gloss not run) | `testability_FREE_v2.json` |

{src_line([f'{T}/hypothesis_verdicts_iter3.csv', f'{X9}/csc_gate_E.json', f'{X10}/csc_gate_P.json', f'{D4}/testability_E2.json', f'{D5}/results/testability_FREE_v2.json'])}
"""


def s07_prior(c: Ctx) -> str:
    c.section = "S7"
    pa = f"{T}/prior_art.csv"
    tbl = verbatim_table(pa, ["section", "line"], "prior_art.csv", max_cell=700)
    rr = f"{RUN}/iter_3/gen_art/gen_art_research_1"
    qfiles = [f"{rr}/notes/QUOTES.md", f"{rr}/notes/full/vossel.md"]
    found = [p for p in qfiles if Path(p).exists() and "predicate availability boosts performance by 15-20%" in Path(p).read_text(errors="replace")]
    for p in found:
        L._read_text(p)
    vflag = (f"verbatim quote verified in `{found[0]}`" if found else "PARAPHRASE, quote not verified in the research notes")
    c.add("vossel_verified", len(found), "0", " ; ".join(qfiles), "files in which the Vossel quote was found")
    return f"""## 7. Prior-art positioning [ARTIFACT:art_VIF75I5R6f0v] (new section)

Insert as §3.x. The research artifact's scoop rule, neighbour table and C1–C5 verdicts, verbatim from eval 3 `prior_art.csv` (built from `research_report.md`):

{tbl}

**Two sentences to add under the iteration-4 claims:**

- Under §4.3's shared-vocabulary result: supplying a predicate list is a documented NL→FOL lever — Vossel et al. (`arXiv:2509.22338`) report that "predicate availability boosts performance by 15-20%"<!-- v:vossel.md --> ({vflag}), and ARc (`arXiv:2511.09008`) scores translations over a fixed shared schema precisely so that k translations can be compared. What SIGPROXY adds is only a measured d reduction ({c.v('x10_d_cued')} cued vs {c.v('x10_d_uncued')} uncued on the same long templated bases, {c.vc('x10_d_diff')}) in the controlled-vocabulary regime the user excluded.
- Under §4.2's anchoring result: peers given the candidate's symbols copying its errors is the correlated-failure mode of N-version programming (Chen & Avizienis, `FTCS-8`). The new element is the per-class e measurement; its sharpest contrast, MEANING_RENAME-type, is CSC {c.v('x9_t9_MR_CSC')} vs FREE_exact {c.v('x9_t9_MR_FREE_exact')}, but against FREE_ALIGN (the aligner c_score_align uses) the difference is only {c.vc('x9_t9_mr_d')}{c.ns('x9_t9_mr_d')}, NOT_READ.

{src_line([pa, f'{rr}/research_report.md'] + found)}
"""


def s08_reasoning(c: Ctx) -> str:
    c.section = "S8"
    rv3 = f"{RUN}/iter_3/review_report/review_report/.terminal_claude_agent_struct_out.json"
    up3 = f"{RUN}/iter_3/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json"
    gs4 = f"{RUN}/iter_4/gen_strat/gen_strat_1/.terminal_claude_agent_struct_out.json"
    pr = f"{X9}/prereg_csc_E.json"
    d = json.loads(L._read_text(rv3))
    u = json.loads(L._read_text(up3))
    g = json.loads(L._read_text(gs4))["strategies"][0]
    prj = json.loads(L._read_text(pr))
    c.add("rv3_score", d["score"], "0", f"{rv3} :: score", "iter-3 review score")
    c.add("rv3_n", len(d["critiques"]), "0", f"{rv3} :: len(critiques)", "iter-3 review critiques")
    gates = "\n".join(f"  - {k}: \"{v}\"<!-- v:prereg_csc_E.json -->" for k, v in prj["gates"].items())
    plan = []
    for i, a in enumerate(g["artifact_directions"]):
        cap = re.search(r"cap \$(\d+(?:\.\d+)?)", a["approach"])
        cid = c.add(f"i4_cap_{i}", float(cap.group(1)) if cap else 0.0, "$0.0", f"{gs4} :: artifact_directions[{i}].approach regex 'cap $x'", f"iter-4 planned cap {i}")
        plan.append(f"| {a['type']} | {a['objective'][:110].replace('|', '/')}…<!-- v:gen_strat_1 --> | {c.v(cid)} |")
    return f"""## 8. §4.1 Reasoning block (new; opens §4)

{c.replaces('### 4.1')} (the reasoning block below goes before the strategy paragraph).

{c.strike(r'Pre-registered gates for CSC \(experiment 9', 'the gates are quoted verbatim from the prereg below; G2 is not a fixed-AUROC bar and G3-E is the RENAME_SYN false-alarm gate, not E2 confirmation', pr, critique='2, 8')}

**Why iteration 4 did what it did.**
1. The previous review scored the record {c.v('rv3_score')} (blocking) with {c.v('rv3_n')} critiques; eval 3 Part 4 was built to answer its record items (corrected verdicts, cost units, artifact IDs).
2. The iter-3 hypothesis update chose move **{u['move'].upper()}** with title "{u['title']}"<!-- v:iter_3/upd_hypo -->.
3. The CSC prediction: cueing peers with the candidate's own symbols should give a LOWER d without a HIGHER e; eval 3's pre-registered d_floor (instrument bracket {c.v('e3_br_lo')}–{c.v('e3_br_hi')}, no-anchoring oracle floor {c.v('e3_oracle3')}) was the yardstick; stopping rule: CSC is dropped if G1 or G2 fails.
4. The gates, verbatim from `prereg_csc_E.json`:
{gates}
5. Planned artifacts and caps (iteration-4 strategy) vs actual spend (ledgers; section 14):

| type | objective (truncated) | planned cap |
|-|-|-|
{chr(10).join(plan)}

   Actual: exp 9 {c.v('x9_spend')}, exp 10 {c.v('x10_spend')}, dataset 4 {c.v('d4_spend')}, dataset 5 {c.v('sp_d5')}, eval 3 no ledger (CPU only). The platform refused paid calls at the first HTTP 403 (section 14 gives the time and the evidenced vs unaccounted spend).

{src_line([rv3, up3, gs4, pr])}
"""


def s09_exp9(c: Ctx) -> str:
    c.section = "S9"
    done = c.add("x9_calls_done", L.to_float(L.regex(f"{X9}/tables.md", r"after ([\d,]+) of ~([\d,]+) planned calls")[0]), "1,000", f"{X9}/tables.md :: regex 'after N of ~M planned calls' group 1", "completed peer calls")
    plan = c.add("x9_calls_plan", L.to_float(L.regex(f"{X9}/tables.md", r"after ([\d,]+) of ~([\d,]+) planned calls", 2)[0]), "1,000", f"{X9}/tables.md :: regex group 2", "planned peer calls")
    t4 = "\n".join(f"| {n} | {c.vc(i)} |" for n, i in [("c_csc", "x9_csc"), ("FREE_exact (same 3 families)", "x9_fexact"), ("FREE_ALIGN", "x9_falign"),
                                                        ("c_score_align", "x9_calign"), ("p_peer_text", "x9_ppt"), ("S4_full", "x9_s4"),
                                                        ("flash-lite disguised", "x9_flash"), ("HYB_MEAN (fails G1)", "x9_hyb")])
    t5 = "\n".join(f"| c_csc − {n} | {c.vc(i)}{c.ns(i)} |" for n, i in [("FREE_exact", "x9_d_fexact"), ("c_score_align", "x9_d_calign"),
                                                                     ("flash-lite", "x9_d_flash"), ("S4_full", "x9_d_s4"), ("p_peer_text", "x9_d_ppt")])
    cls = [("ADD", "ADD"), ("DROP", "DROP"), ("COMPOUND", "COMPOUND"), ("MEANING_RENAME-type (n = " + c.v('x9_t9_mr_n') + ")", "MR"),
           ("structural", "STRUCT"), ("polarity", "POL")]
    t9 = "\n".join(f"| {n} | {c.v(f'x9_t9_{k}_CSC')} | {c.v(f'x9_t9_{k}_FREE_exact')} | {c.v(f'x9_t9_{k}_FREE_align')} |" for n, k in cls)
    return f"""## 9. §4.2 Experiment 9, CSC on DEVELOPMENT set E: re-transcribed

{c.replaces('### 4.2')}

{c.strike(r'^### 4\.2 Experiment 9: CSC on held-out E', 'E is DEVELOPMENT data; heading becomes "§4.2 Experiment 9: CSC on development set E — provisional negative"', f'{L.RUN}/iter_4/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json', whole=True, critique='1')}

{c.strike(r'^\| \*\*CSC\*\* \| \*\*0\.614', 'every CI in the headline table was narrower than the source; the T4 table below is transcribed from analysis.json', f'{A9}', whole=True, critique='2')}

{c.strike(r'^\| COMPOUND \| 0\.643', 'COMPOUND e_CSC / e_FREE_exact are ' + c.v('x9_t9_COMPOUND_CSC') + ' / ' + c.v('x9_t9_COMPOUND_FREE_exact') + ' (T9); the struck values were a different quantity', f'{A9}', whole=True, critique='2')}

{c.strike(r'The M3-style length interaction for CSC is negative', 'M3 under both specifications: bootstrap ' + c.vc('x9_m3_boot') + ', stacked GEE ' + c.vc('x9_m3_gee'), f'{A9}', critique='2')}

{c.strike(r'^\| G2 \(strat AUROC ≥ 0\.700\)', 'G2 is NOT_READ (R_AB part FAIL; L25 below the readable cell size)', f'{X9}/csc_gate_E.json', whole=True, critique='2')}

{c.strike(r'^\| G3-E \(E2 confirmation\)', 'G3-E is the RENAME_SYN false-alarm gate: NOT_RUN', f'{X9}/prereg_csc_E.json', whole=True, critique='2')}

{c.strike(r'^CSC degrades the decision boundary relative to the FREE baseline', 'NET is the within-arm change from words T1 to T3; every arm degrades (FULL FREE_exact ' + c.v('x9_net_fx') + ', FREE_align ' + c.v('x9_net_fa') + ')', f'{A9}', critique='2')}

{c.strike(r'^CSC fails both quality gates\. It is a dead end', "'dead end' becomes 'provisional negative on a completion-selected subset; L25 and RENAME untested'", f'{X9}/csc_gate_E.json', critique='3')}

**Population and selection.** The platform refused paid calls after {c.v(done)} of ~{c.v(plan)} planned peer calls, so CSC is scored on a COMPLETION-SELECTED subset: PRIMARY = {c.v('x9_n')} R_AB rows ({c.v('x9_nerr')} ERROR / {c.v('x9_ncor')} CORRECT, {c.v('x9_nsent')} sentences). CTRL makes up {c.v('x9_ctrl_prim')} of PRIMARY CORRECT rows vs {c.v('x9_ctrl_full')} on FULL. No stratum reaches `50/50` (L25: {c.v('x9_l25_err')} / {c.v('x9_l25_cor')}), so L25 is NOT_READ. c_csc is almost binary (tie rate {c.v('x9_tie')}). The prereg calls every gate PROVISIONAL. CIs: sentence-cluster percentile bootstrap, B = 2000, seed 0, stratified by source stratum (tables.md header).

**T4. Strat AUROC on PRIMARY** (CIs verbatim):

| metric | strat AUROC [95% CI] |
|-|-|
{t4}

**T5. Paired Δ, same rows:**

| contrast | Δ [95% CI] |
|-|-|
{t5}

Nesting: [S4_full + c_csc] − S4_full {c.vc('x9_nest')}{c.ns('x9_nest')}. Phi-4 exemplar leakage (T17, POST-HOC): {c.v('x9_phi_calls')} CSC calls copied the few-shot exemplar; removing them symmetrically gives c_csc_clean {c.v('x9_clean')} and Δ vs FREE_exact_clean {c.vc('x9_clean_d')}.

**e and d.** CSC e {c.v('x9_e_csc')} vs FREE_exact {c.v('x9_e_fx')} vs FREE_ALIGN {c.v('x9_e_fa')}; d {c.v('x9_d_csc')} vs {c.v('x9_d_fx')} vs {c.v('x9_d_fa')}. FULL population ($0, T2): FREE_exact d {c.v('x9_full_d_fx')} vs ALIGN {c.v('x9_full_d_fa')} (e {c.v('x9_full_e_fx')} vs {c.v('x9_full_e_fa')}).

**T9. e by error class, PRIMARY** (FREE_exact AND FREE_ALIGN side by side):

| class | e_CSC | e_FREE_exact | e_FREE_ALIGN |
|-|-|-|-|
{t9}

MEANING_RENAME-type Δe CSC − FREE_ALIGN {c.vc('x9_t9_mr_d')}{c.ns('x9_t9_mr_d')} (NOT_READ). T9b (FULL, free peers): FREE_ALIGN e on MEANING_RENAME-type {c.v('x9_t9b_mr_fa')} vs FREE_exact {c.v('x9_t9b_mr_fx')}. Reading: every vocabulary bridge (the aligner, or peers cued with the candidate's symbols) lowers d AND raises e; the aligner that c_score_align uses already endorses meaning-rename errors almost as often as CSC.

**Gates (verbatim definitions in section 8).** G1 FAIL (d {c.v('x9_g1_d')} passes the bar but the words slope is {c.vc('x9_g1_slope')}); G2 NOT_READ (R_AB part FAIL; L25 Δ {c.vc('x9_g2_l25')}, n below the readable size); G3-E {c.v('x9_g3')}; G4 null; G5 PASS {c.v('x9_g5')} per candidate ({c.v('x9_g5_dd')} deduped). CSC_graded ({c.vc('x9_graded')}) and CSC_multi ({c.vc('x9_multi')}) and HYB_MEAN (d {c.v('x9_hyb_g1d')}, slope {c.v('x9_hyb_g1s')}) also fail G1.

**Length.** M3 (CSC − flash-lite, decision correctness vs words): bootstrap {c.vc('x9_m3_boot')}; stacked GEE {c.vc('x9_m3_gee')}. NET is within-arm length degradation: FULL FREE_exact {c.v('x9_net_fx')}, FREE_align {c.v('x9_net_fa')}. Words-tercile strat AUROC, PRIMARY: c_csc {c.v('x9_t12_csc_T1')} / {c.v('x9_t12_csc_T2')} / {c.v('x9_t12_csc_T3')}; c_score_align {c.v('x9_t12_ca_T1')} / {c.v('x9_t12_ca_T2')} / {c.v('x9_t12_ca_T3')}.

**T8 (where d comes from, FULL).** {c.v('x9_t8_struct')} of free-exact disagreements with CORRECT candidates are structural (no vocabulary map makes them equivalent); only {c.v('x9_t8_vocab')} of flagged CORRECT rows have every disagreement vocabulary-resolvable. **T10 typing:** own_majority {c.v('x9_t10_own')}, below the majority class {c.v('x9_t10_maj')}. **T14 system level:** CSC τ-b {c.v('x9_t14_csc')} (p = {c.v('x9_t14_csc_p')}) vs c_score_align {c.v('x9_t14_ca')} (p = {c.v('x9_t14_ca_p')}). **T15 rename (9-peer c_score_align, WordNet synonyms):** FA {c.v('x9_t15_base')} → {c.v('x9_t15_syn')}, ΔFA {c.vc('x9_t15_d')}. Reproduction check: eval-2 3-pool strat {c.v('x9_repro')}. Spend {c.v('x9_spend')}.

**Verdict wording.** "Provisional negative on a completion-selected subset; L25 and RENAME untested." CSC vs flash-lite and vs S4_full is n.s. on PRIMARY.

{src_line([A9, f'{X9}/tables.md', f'{X9}/csc_gate_E.json', f'{X9}/prereg_csc_E.json', f'{X9}/results/posthoc_phi_contamination.json', f'{X9}/results/repro_checks.json'])}
"""


def s10_exp10(c: Ctx) -> str:
    c.section = "S10"
    arms = [("c_align (exp 8)", "E", "x10_bfa_calign", "x10_rec_FREE_c_align_exp8_E"), ("FREE3_exact", "E", "x10_bfa_fx_e", "x10_rec_FREE3_exact_E"),
            ("FREE3_align", "E", "x10_bfa_fa_e", "x10_rec_FREE3_align_E"), ("FREE3_exact", "R_COMP", "x10_bfa_fx_r", "x10_rec_FREE3_exact_RCOMP"),
            ("FREE3_align", "R_COMP", "x10_bfa_fa_r", "x10_rec_FREE3_align_RCOMP"), ("flash-lite judge", "E", "x10_bfa_judge_e", "x10_rec_JUDGE_flashlite_disg_exp8_E")]
    t_rec = "\n".join(f"| {a} | {s} | recall {c.v(r)} | base FA {c.v(b)} |" for a, s, b, r in arms)
    ctl_rows = []
    for var in ("FREE_c_align_exp8", "FREE3_exact", "FREE3_align", "JUDGE_flashlite_disg_exp8", "SIGPROXY_K3"):
        for src in ("E", "RCOMP"):
            k0 = f"ctl_{var}_RENAME_SYN_{src}_fa"
            if k0 not in c.r:
                continue
            cells = []
            for ctl in ("RENAME_SYN", "RENAME_NONCE", "REORDER_COMMUTE", "CONTRAPOSITIVE"):
                k = f"ctl_{var}_{ctl}_{src}"
                cells.append(f"FA {c.v(k + '_fa')} / base FA {c.v(k + '_base')} / flip {c.v(k + '_flip')}")
            ctl_rows.append(f"| `{var}` | {src} | " + " | ".join(cells) + " |")
    return f"""## 10. §4.3 Experiment 10 (CSC on PERTURB, budget-stopped): corrected

{c.replaces('### 4.3')}

{c.strike(r'^FREE consensus achieves near-perfect recall on PERTURB', 'FREE-consensus recall ≈ 1 comes with base FA on verified-CORRECT bases of ' + c.v('x10_bfa_calign') + ' / ' + c.v('x10_bfa_fx_e') + ' / ' + c.v('x10_bfa_fx_r') + ' / ' + c.v('x10_bfa_fa_r') + ' (table below): that recall is trivial', f'{X10}/d_by_length.csv', critique='4')}

{c.strike(r'LOCAL2 \(small 1\.5-2B local peers\) has substantial endorsement', 'every LOCAL2 endorsement is an insufficient-peer tie at `c = 0.5` (tie share ' + c.v('x10_l2_tie') + '); excluding ties e is ' + c.v('x10_l2_excl_own') + ' / ' + c.v('x10_l2_excl_base'), f'{X10}/anchoring.csv', critique='4')}

{c.strike(r'The flash-lite judge endorses 12\.4% of mutants, matching the iteration-3 E endorsement rate', 'the judge misses ' + c.v('x10_judge_e') + ' of PERTURB mutants; this is NOT END_MAJ e on real errors (a different quantity)', f'{X10}/anchoring.csv', critique='4')}

{c.strike(r'^\| free3 \(independent vocab\) \| ALL', 'free3 on E is ' + c.vc('x10_free3') + '; the pooled ' + c.v('x10_free3_pool') + ' includes R_COMP rows at zero', f'{X10}/typing_csc.csv', whole=True, critique='4')}

{c.strike(r'^All consensus variants flag RENAME controls at 85-100% FA', 'most rename FA is base FA: the paired flip rates are the rename effect (c_align E SYN ' + c.v('x10_flip_syn') + ', NONCE ' + c.v('x10_flip_nonce') + '); controls split by base source below', f'{X10}/controls_fa.csv', critique='4')}

{c.strike(r'^\| FREE3_exact \| 1\.000 \| 1\.000 \| 0\.986 \(R_COMP\)', 'mixed sources: FREE3_exact REORDER / CONTRA FA on E is ' + c.v('x10_reorder_e') + ' / ' + c.v('x10_contra_e') + '; on R_COMP ' + c.v('x10_contra_r'), f'{X10}/controls_fa.csv', whole=True, critique='4')}

**Status.** 0 CSC peers were generated (run budget refused the first call; spend {c.v('x10_spend')}); G3-P, G4 and MT are UNTESTED, not failed. Zero-cost arms follow (development data).

**Recall next to base FA** (`c > 0.5`; mutants vs the verified-CORRECT bases they were derived from):

| arm | bases | mutant recall | base FA |
|-|-|-|-|
{t_rec}

**d rises with length (T4, uncued, E bases, words terciles):** c_align {c.v('x10_t1')} / {c.v('x10_t2')} / {c.v('x10_t3')}; FREE3_exact {c.v('x10_FREE3_exact_d_T1')} / {c.v('x10_FREE3_exact_d_T2')} / {c.v('x10_FREE3_exact_d_T3')}.

**Controls split by base source** (FA / paired base FA / flip):

| variant | bases | RENAME_SYN | RENAME_NONCE | REORDER_COMMUTE | CONTRAPOSITIVE |
|-|-|-|-|-|-|
{chr(10).join(ctl_rows)}

The eval-3 table in section 1 gives a larger c_align NONCE flip ({c.v('pc_c_align_RENAME_NONCE_flip')}) than exp 10 ({c.v('x10_flip_nonce')}); they pair renames with different base rows (eval 3: exp-8 PERTURB scoring; exp 10: its own base join) and are reported side by side, not harmonised.

**SIGPROXY (out-of-scope controlled vocabulary; R_COMP SIG).** k = 3 within-template AUROC {c.vc('x10_sigproxy')}. On the same long templated bases, correct-base FA d is {c.v('x10_d_cued')} cued vs {c.v('x10_d_uncued')} uncued FREE3-ALIGN, paired {c.vc('x10_d_diff')} — with base FA shown, not recall alone. Prior art: see section 7 (Vossel; ARc).

**Typing (which kind of error).** free3 on E {c.vc('x10_free3')}; peer-medoid {c.v('e8_typ_medoid')} ≈ judge {c.v('e8_typ_judge')} (exp 8). `oracle` repairs against the known gold base: it is **GOLD-USING**, not a gold-free metric ({c.v('x10_oracle')} on E). SIGPROXY majority {c.vc('x10_proxy')} is within a shared vocabulary (out of scope). **Answer to the user's "which kind of error": NEGATIVE outside a shared vocabulary.**

**T8 (R_COMP FREE, label-free).** ALIGN pairwise agreement among FREE candidates {c.v('x10_t8_align')}.

{src_line([f'{X10}/tables.md', f'{X10}/anchoring.csv', f'{X10}/controls_fa.csv', f'{X10}/d_by_length.csv', f'{X10}/typing_csc.csv', f'{X10}/rcomp_sig_csc.json', f'{X10}/paired_cue_effect.csv', f'{X10}/api_cost_ledger.jsonl', f'{L.RUN}/iter_4/review_report/review_report/audit/recompute_perturb_csc.json'])}
"""


def _devs_d4() -> list[str]:
    txt = L._read_text(f"{D4}/dataset_card.md")
    return [ln.strip()[2:] for ln in txt.splitlines() if re.match(r"^- \*\*D\d\*\*", ln.strip())]


def _devs_d5() -> list[str]:
    d = json.loads(L._read_text(f"{D5}/deviations.json"))["deviations"]
    out = []
    items = d.items() if isinstance(d, dict) else [(x.get("id", "?"), x) for x in d]
    for k, v in items:
        if isinstance(v, dict):
            vid = v.get("id", k)
            txt = v.get("title") or v.get("what") or v.get("description") or v.get("summary") or json.dumps(v)[:200]
        else:
            vid, txt = k, str(v)
        out.append(f"**{vid}**: {str(txt)[:260]}")
    return out


def s11_datasets(c: Ctx) -> str:
    c.section = "S11"
    d4 = "\n".join(f"- {x}<!-- v:dataset_card.md -->" for x in _devs_d4())
    d5 = "\n".join(f"- {x}<!-- v:deviations.json -->" for x in _devs_d5())
    return f"""## 11. §4.4 / §4.5 caveats (E2 and R_COMP FREE)

{c.replaces('### 4.4')}; {c.replaces('### 4.5')}

{c.strike(r'Gate balanced accuracies \(P1 0\.861, P3 0\.875, R1 0\.837\) all pass the gate', 'the drift stop rule is UNDECIDED (passes = ' + c.v('d4_passes') + '): the replay was cut off; the combined agreement ' + c.v('d4_comb') + ' counts unreplayed items, while on the replayed items majority agreement is ' + c.v('d4_repl'), f'{D4}/panel_drift_E2.json', critique='6')}

{c.strike(r'^Of 420 old tier-A ERROR rows, 297 are MAPPED \(70\.7%\)', "'up to " + c.v('d5_707') + "' (MAPPED is an upper bound: in the executor audit only " + c.v('d5_mapped_f') + " of MAPPED rows are faithful)", OLA, critique='6')}

**E2 (dataset 4).** 550 sentences are frozen and sealed; a 30-sentence pilot gave {c.v('d4_err')} ERROR / {c.v('d4_unres')} UNRESOLVED (incl. gold-as-system) / {c.v('d4_unp')} UNPARSEABLE / {c.v('d4_cor')} CORRECT: no cell is testable. **Panel drift:** the stop rule is UNDECIDED. The replay was incomplete ({c.v('d4_trackh_repl')} of {c.v('d4_trackh_n')} track-H judgements got ≥ 2 new votes); synthetic gate items agree {c.v('d4_syn')}; on the {c.v('d4_n22')} replayed unambiguous track-H judgements today's panel flags {c.v('d4_flag_today')} of original errors vs {c.v('d4_flag_E')} in E — a drift ALARM on small n that came from the incomplete replay, whose replayed items agree {c.v('d4_repl')}. Iteration 5's E2-A decides it (`e2/E2_DRIFT_DECISION.json`). Spend {c.v('d4_spend')}; projected completion {c.v('d4_proj')}. Deviations D0–D7 (verbatim from `dataset_card.md`):

{d4}

**R_COMP FREE (dataset 5).** Search-only labels: ERROR_CERT {c.v('d5_err')}, MAPPED {c.v('d5_map')}, UNPARSEABLE {c.v('d5_unp')}, NO_OUTPUT {c.v('d5_noout')}; CORRECT {c.v('d5_cor')} (gloss not run). Search soundness: {c.v('d5_false')} false ERROR_CERT on {c.v('d5_1595')} renamed SIG-CORRECT rows; known-ERROR rescue {c.v('d5_resc_n')} (nonce) / {c.v('d5_resc_s')} (synonym), by template up to T8 {c.v('d5_t8')} and T9 {c.v('d5_t9n')}–{c.v('d5_t9s')}. Executor audit: ERROR_CERT precision {c.vc('d5_prec')}; MAPPED faithful {c.v('d5_mapped_f')}; the disagreement sample includes a MAPPED certificate that swaps `LivesIn` and `StudentInClass` (a real error passing the search; `old_label_agreement.json` sample 0). Old iter-3 labels: UP TO {c.v('d5_707')} of old ERROR rows are MAPPED; old/new kappa {c.v('d5_kappa')}. Pointer: §3.3 carries the VOID marker (section 2). Deviations D1–D9 (verbatim, incl. D6, the map-family amendment after the freeze):

{d5}

{src_line([f'{D4}/panel_drift_E2.json', f'{D4}/dataset_card.md', f'{D4}/sealed/labels_E2.jsonl', f'{D4}/pilot_projection.json', f'{D5}/results/soundness_audit.json', OLA, f'{D5}/deviations.json', f'{D5}/results/testability_FREE_v2.json'])}
"""


def s12_eval3(c: Ctx) -> str:
    c.section = "S12"
    return f"""## 12. §4.6 Evaluation 3 rewritten (wrong peers, not words)

{c.replaces('### 4.6')}

{c.strike(r'^The predicted d_floor \(0\.402\) closely matches the observed END_MAJ d', 'the reverse: the post-hoc instruments predict almost no fix (bracket ' + c.v('e3_br_lo') + '–' + c.v('e3_br_hi') + '); the pre-registered gap_closed rule is ill-conditioned (denominator ' + c.v('e3_denom') + ')', f'{EV3}/README.md', critique='5')}

{c.strike(r'The R_exact AUROC \(0\.683\) is the theoretical performance', 'the struck number is d under the exact rule on E\'s 3-pool (' + c.v('e3_683') + '); it is a divergence rate on E, not a ranking statistic and not R_COMP', f'{T}/p1_rule_cuts.csv', critique='5')}

{c.strike(r'^\| R_exact AUROC \| 0\.683 \|', 'row relabelled "d under R_exact (E 3-pool)"', f'{T}/p1_rule_cuts.csv', whole=True, critique='5')}

{c.strike(r'because it does not account for vocabulary-driven non-transitivity', 'the method UNDER-COUNTS vocabulary effects (predicted endorsement ' + c.v('e3_pred_rate') + ' vs actual SIG ' + c.v('e3_sig_rate') + '); non-transitivity (' + c.v('e3_nontrans') + ') is a separate diagnostic', f'{EV3}/results/part2.json', critique='5')}

{c.strike(r'The Part-1 d_floor model closely matches observed d', 'the instruments are shown to under-count vocabulary effects (calibration error ' + c.vc('e3_calib') + ')', f'{EV3}/results/part2.json', critique='5')}

**Main finding (label-based; no instrument needed).** Among pairs of a CORRECT candidate and a non-agreeing peer, {c.v('e3_77')} (9 families) / {c.v('e3_61')} (3-pool) of those peers are labelled ERROR, so d on E is mostly peer error, not vocabulary. Among CORRECT–CORRECT disagreements only {c.v('e3_9')} are vocabulary-resolvable. Pair classes (9 families): IRREDUCIBLE {c.v('e3_irr')}, EXACT {c.v('e3_exact')}, ALIGN_ONLY {c.v('e3_align')}, VOCAB {c.v('e3_vocab')}, NAME_ONLY {c.v('e3_name')}.

**The instruments.** On the 3-pool, END_MAJ d is {c.v('e3_endmaj3')}; the instrument bracket is {c.v('e3_br_lo')}–{c.v('e3_br_hi')} with prediction {c.v('e3_pred')}, so the pre-registered gap_closed denominator is {c.v('e3_denom')} (ill-conditioned). Where the true effect of a shared vocabulary is known (R_COMP SIG vs FREE), the method predicts endorsement {c.v('e3_pred_rate')} against an actual {c.v('e3_sig_rate')}: calibration error {c.vc('e3_calib')}, NOT VALIDATED. The post-hoc instruments predict almost no fix and are shown to under-count vocabulary effects. SIG also changes granularity (D7), so the SIG − FREE exact-agreement drop {c.vc('e3_drop')} (pairwise exact agreement SIG {c.v('e3_sigx')} vs FREE {c.v('e3_freex')}) is an upper bound; row endorsement SIG {c.v('e3_sigrow')} vs FREE {c.v('e3_freerow')}.

**Oracle floors (no anchoring).** 3-pool {c.v('e3_oracle3')} (labelled denominator {c.v('e3_labdenom')}); L25 {c.v('e3_oracle_l25')} vs END_MAJ {c.v('e3_endmaj_l25')}; 9 families {c.v('e3_oracle9')} > END_MAJ {c.v('e3_endmaj9')}, because most peers are wrong. e ceiling {c.v('e3_ecap')}.

**Other diagnostics.** Specificity placebo (VOCAB vs random IRREDUCIBLE pairs): ratio {c.vc('e3_placebo3')} (3-pool), {c.vc('e3_placebo9')} (9 families): VOCAB agreements are not label-specific. Label-free counterfactual c_vres − c_score_align on L25: {c.vc('e3_vres')} (9 families), {c.vc('e3_vres3')}{c.ns('e3_vres3')} (3-pool). NET Δ(e+d) words T3 − T1 degrades under every rule: {c.v('e3_net_lo')} (9-family R_align), {c.v('e3_net9_pl')} (9-family R_point_label), {c.v('e3_net3_pl')} (3-pool R_point_label), {c.v('e3_net_hi')} (3-pool R_align).

**Power (iteration 5).** L25 yield {c.v('pw_yield')}. MDE80 vs flash-lite disguised at 250 / 300 / 350 / 400 planned L25: {c.v('pw_mde_250')} / {c.v('pw_mde_300')} / {c.v('pw_mde_350')} / {c.v('pw_mde_400')}; power at the observed L25 Δ ({c.v('t1_l25')}): {c.v('pw_pow_250')} / {c.v('pw_pow_300')} / {c.v('pw_pow_350')} / {c.v('pw_pow_400')} (all MARGINAL). Detecting the observed L25 effect needs ~{c.v('pw_882')} planned L25 sentences; the long pool needs ~{c.v('pw_237')} usable sentences. R_COMP FREE needs ≥ {c.v('e3_200')} CORRECT rows. Eval-3 deviations D1–D10 are in its README; its reusable functions are in `function_inventory.csv` (section 16).

{src_line([f'{EV3}/README.md', f'{EV3}/results/part1.json', f'{EV3}/results/part1_net.json', f'{EV3}/results/part2.json', f'{T}/p1_rule_cuts.csv', f'{T}/p1_class_shares.csv', f'{EV3}/power_E2.json', f'{T}/p3_planned_E2.csv'])}
"""


def s13_cost(c: Ctx) -> str:
    c.section = "S13"
    from src.transcribe import COST_ITEMS
    flash = c.raw("cost_flash")
    rows = []
    for item, unit in COST_ITEMS:
        key = "cu_" + "".join(ch if ch.isalnum() else "_" for ch in f"{item}_{unit}")[:60]
        basis = L.csv_cell(CU, {"item": item, "unit": unit}, "cost_basis")[0]
        u = unit.replace("USD ", "")
        ratio = ""
        if "candidate" in unit or "item" in unit:
            rid = c.add(key + "_ratio", c.raw(key) / flash, "0.00", f"{CU} :: {item} / judge_cheap", f"{item} ÷ flash-lite per item-call")
            ratio = c.v(rid) + "×"
        rows.append(f"| `{item}` | {u} | {basis.replace('|', '/')} | ${c.v(key)} | {ratio} | `cost_units.csv` |")
    rows.append(f"| CSC (exp 9, G5) | per candidate | FULL (undeduped) | {c.v('x9_g5')} | {c.v(c.add('g5_ratio', L.to_float(c.raw('x9_g5')) / flash, '0.00', A9, 'G5/flash'))}× | `csc_gate_E.json` |")
    rows.append(f"| CSC (exp 9, G5) | per candidate | FULL (dedup-apportioned) | {c.v('x9_g5_dd')} | {c.v(c.add('g5dd_ratio', L.to_float(c.raw('x9_g5_dd')) / flash, '0.00', A9, 'G5dd/flash'))}× | `results/analysis.json g_cost` |")
    rows.append(f"| E2 pilot, L25 (generation + panel + repair) | per sentence | FULL (projection) | {c.v('d4_pilot_usd')} | — | `pilot_projection.json` |")
    return f"""## 13. ONE cost table (units explicit)

Replaces: every cost statement in §3.3, §3.5, §3.6 and §4.6 (markers in sections 2 and 3). FULL = all API spend to produce the score; MARGINAL = only the extra work given peers already exist. Ratio = cost ÷ the flash-lite judge per item-call ({c.v('cost_flash')} per item-call); ratios are given only where the unit is per item/candidate.

| item | unit | FULL / MARGINAL | $ | ratio vs flash-lite | source |
|-|-|-|-|-|-|
{chr(10).join(rows)}

The frontier judge costs {c.v('rv_frontier_x')}× the consensus score per ITEM (FULL); the ratio struck in section 2 mixed a per-call judge price with a per-candidate generation price.

{src_line([CU, f'{X9}/csc_gate_E.json', f'{D4}/pilot_projection.json'])}
"""


def s14_spend(c: Ctx, sp: dict) -> str:
    c.section = "S14"
    loc = "results/spend_iter4.json"
    rows = []
    for k, v in sp["by_artifact_usd"].items():
        rid = c.add("spend_" + re.sub(r"\W", "_", k)[-40:], v, "$0.0000", f"{loc} :: by_artifact_usd.{k}", f"spend in window {k}")
        rows.append(f"| `{k}` | {c.v(rid)} | {sp['records_by_artifact'].get(k, 0)} |")
    ev = c.add("spend_evidenced", sp["evidenced_total_usd"], "$0.000", f"{loc} :: evidenced_total_usd", "evidenced total in window")
    ev4 = c.add("spend_iter4", sp["evidenced_iter4_artifacts_usd"], "$0.000", f"{loc} :: evidenced_iter4_artifacts_usd", "iter-4 artifacts")
    evo = c.add("spend_other", sp["evidenced_other_artifacts_in_window_usd"], "$0.000", f"{loc} :: evidenced_other_artifacts_in_window_usd", "other artifacts in window")
    bud = c.add("spend_budget", sp["phase_budget_usd"], "$0.00", f"{loc} :: phase_budget_usd (tables.md T0 of exp 9)", "phase budget")
    un = c.add("spend_unacc", sp["unaccounted_usd"], "$0.000", f"{loc} :: unaccounted_usd", "unaccounted")
    return f"""## 14. Iteration-4 spend table (ledgers only)

Replaces: the three different budget statements in §4.1–§4.4 (`budget event at $0.108`, `run-wide budget exhausted by earlier artifacts`, `exhausted at 07:26 UTC`).

Method: every `*ledger*.json(l)` and `budget_state.json` under the run root was read ({sp['n_ledger_files_found']} files; {sp['n_duplicate_files_by_sha256']} byte-identical copies dropped, e.g. repo clones), and records were de-duplicated across files by (second, model, cost). Window: {sp['window_utc'][0]} (earliest iteration-4 ledger record minus 6 h) to {sp['window_utc'][1]} (first HTTP 403 budget refusal, `{sp['first_403_source']}`).

| artifact (ledger dir) | $ in window | records |
|-|-|-|
{chr(10).join(rows)}

- Iteration-4 artifacts: {c.v(ev4)} (exp 9 {c.v('x9_spend')}, exp 10 {c.v('x10_spend')}, dataset 4 {c.v('d4_spend')}, dataset 5 {c.v('sp_d5')}; eval 3 has no ledger, CPU only).
- Other artifacts whose ledger records fall inside the same window: {c.v(evo)} (iteration-3 experiments). The ledgers do not record which phase budget these calls were charged to; this table does not attribute them.
- Evidenced total in the window: {c.v(ev)} vs the {c.v(bud)} 'Test idea' phase budget: **unaccounted {c.v(un)} (no ledger in the run tree records it)**.
- What the ledgers themselves say about the budget (verbatim notes): {' '.join('"' + n['note'] + '"<!-- v:' + Path(n['file']).name + ' -->' for n in sp.get('ledger_budget_notes', [])[:3]) or 'none'}
- iter_4 gen_art directories without any ledger: {', '.join('`' + Path(x).name + '`' for x in sp['iter4_gen_art_dirs_without_ledger'])}.

{src_line([loc, 'src/spend.py'])}
"""


def s15_deadends(c: Ctx) -> str:
    c.section = "S15"
    b2 = f"{RUN}/iter_3/gen_art/gen_art_evaluation_2/tables/b2_dead_end.csv"
    ra = f"{RUN}/iter_3/gen_art/gen_art_evaluation_2/tables/radj_gate.csv"
    p = f"{RUN}/iter_2/gen_art/gen_art_experiment_5/results/p_tests.json"
    pt = json.loads(L._read_text(p))
    b1 = f"{RUN}/iter_1/gen_art/gen_art_experiment_2"
    b1_empty = not any(x.name not in (".aii",) for x in Path(b1).iterdir()) if Path(b1).exists() else True
    c.add("b1_files", sum(1 for x in Path(b1).iterdir() if x.name != ".aii") if Path(b1).exists() else 0, "0", f"{b1} :: count files (excluding .aii)", "files in B1 workspace")
    return f"""## 15. Dead ends (extended, with sources)

Replaces: the "Dead ends accumulated across all iterations" table in §4.7.

{c.strike(r'^\| Name-free consensus \(c_nf\) \| 2-3 \| SWAP recall 0\.512', 'the reason is the pre-registered selection failure (PERTURB RENAME_SYN / NONCE FA, selection rule without paired flip, ' + c.v('e8_nf_syn') + ' / ' + c.v('e8_nf_nonce') + ') plus blindness to MEANING_RENAME (' + c.v('e8_cnf_mr') + ')', f'{E8}/selection.json', whole=True, critique='10')}

| dead end | iteration | reason | source |
|-|-|-|-|
| Rename-invariant selection (NF-anchored and HYB) | 3 | both INELIGIBLE (FA-only selection rule, no flip): RENAME_SYN / NONCE FA NF {c.v('e8_nf_syn')} / {c.v('e8_nf_nonce')}, HYB {c.v('e8_hyb_syn')} / {c.v('e8_hyb_nonce')}; nothing frozen | `rename_selection_dead_end.csv`, `selection.json` |
| Name-free consensus `c_nf` | 2-3 | pre-registered selection failure + MEANING_RENAME blindness ({c.v('e8_cnf_mr')}) | `selection.json`, `perturb_sensitivity.csv` |
| Candidate B1 | 1 | planned, never ran (workspace holds {c.v('b1_files')} files{' — empty' if b1_empty else ''}) | `{b1}` |
| FOL-Triage fused score | 1 | fails the rewrite-FA gate (worst-family FA {c.v('iter1_triage_fa')} vs a `0.10` bar; equals the FA on originals) | `iter_1/gen_art/gen_art_experiment_1/README.md` |
| P2 / P4 (exp 5) | 2 | P2 {pt['P2']}, P4 {pt['P4']}<!-- v:p_tests.json --> | `p_tests.json` |
| B2 decomposed z3 reader | 2 | gate failure: balanced accuracy {c.v('ev2_b2_gate')} | `b2_dead_end.csv`, eval-2 `hypothesis_verdicts.csv` |
| R_ADJ LLM adjudicator | 2 | gate failure: Sonnet-5 balanced accuracy {c.v('ev2_radj_all')} overall, {c.v('ev2_radj_h')} on expert track-H | `radj_gate.csv`, eval-2 `hypothesis_verdicts.csv` |
| CSC, CSC_graded, CSC_multi, HYB_MEAN | 4 | all fail G1 (d slopes positive); CSC provisional negative on a completion-selected subset; L25 and RENAME untested | `csc_gate_E.json` |
| E2 EXC-core stratum | 4 | core-exception supply exhausted (D3) | dataset 4 `dataset_card.md` |
| CSC arms and the panel route for R_COMP FREE | 4→5 | CLOSED by the iteration-5 hypothesis | iter_4 `upd_hypo` |
| Vocabulary-divergence diagnosis of iteration 3 | 3→4 | refuted on E by the label-based decomposition (section 12) | eval 3 `p1_class_shares.csv` |

{src_line([f'{T}/rename_selection_dead_end.csv', f'{E8}/selection.json', f'{E8}/perturb_sensitivity.csv', p, b2, ra, f'{X9}/csc_gate_E.json'])}
"""


def s16_coverage(c: Ctx) -> str:
    c.section = "S16"
    cov = verbatim_table(f"{T}/coverage_vs_request_iter3.csv", ["requirement", "status", "gap", "iteration"], "coverage_vs_request_iter3.csv", max_cell=160)
    fi = verbatim_table(f"{T}/function_inventory.csv", ["file", "function", "what_it_measures"], "function_inventory.csv", max_cell=160)
    return f"""## 16. Coverage against the request (iteration 4 update + iteration-5 pending cells)

Insert as a table in §4.7 (and the final summary).

**One-line answers (iteration 4):**

| requirement | answer after iteration 4 | pending in iteration 5 |
|-|-|-|
| Long, heavily conditioned sentences | UNTESTED in iteration 4 (CSC L25 NOT_READ; E2 {c.v('d4_cor')} CORRECT rows); on development E, L25 Δ {c.vc('t1_l25')}{c.ns('t1_l25')} | `confirm_verdict_E2A.json`, `confirm_verdict_E2B.json`, `union_longpool.json` |
| No ontology / controlled vocabulary | consensus UNVALIDATED (R_COMP FREE CORRECT class empty); the only positive iteration-4 numbers (SIGPROXY {c.v('x10_sigproxy')}; d {c.v('x10_d_cued')}) are in the excluded SIG regime | `confirm_verdict_rcomp.json` |
| Which kind of error | NEGATIVE outside a shared vocabulary: free3 {c.v('x10_free3')} on E; medoid {c.v('e8_typ_medoid')} ≈ judge {c.v('e8_typ_judge')} | none (no new budget) |
| Invariance | rename non-invariance measured: c_align NONCE / SYN FA {c.v('e8_calign_nonce')} / {c.v('e8_calign_syn')} with flips {c.v('x10_flip_nonce')} / {c.v('x10_flip_syn')}; 9-peer ΔFA {c.v('x9_t15_d')} | `freeze/gg_gate.json`, `rename_E2.json` |
| Per-type sensitivity | per-operator consensus AUROC is an artefact; per-class e on real errors (section 9) | `hmech_E2.json` |
| Coverage | counted: PERTURB {c.v('e8_cov_ok')} / {c.v('e8_cov_n')} scored | E2 coverage with unparseables in the denominator |
| Cost | one table with units (section 13) | $ and seconds per candidate on E2 |
| Baselines | flash-lite (both views), nano, S4 stacks, frontier ratio {c.v('t1_ratio')} (point only) | `judges_costmatched`, `judge_frontier` (E2-B) |
| Complexity | d rises with length in every arm (sections 3, 9, 10) | `hmech_E2.json` (NET) |
| Contamination | flash-lite DiD {c.vc('t1_did')} (marginal) | — |
| Deliverable functions | inventory below (each marked gold-free / gold-using in its row) | `freeze/` library |

Iteration-3 coverage table (verbatim):

{cov}

Function inventory (verbatim; `oracle`, `exhaustive_map_label`, `gloss_decision` and anything reading a reference are GOLD-USING labelling tools, all others gold-free):

{fi}

{src_line([f'{T}/coverage_vs_request_iter3.csv', f'{T}/function_inventory.csv'])}
"""


def s17_learned(c: Ctx) -> str:
    c.section = "S17"
    return f"""## 17. "What we have learned" (draft replacement)

{c.replaces('## What we have learned')}

{c.strike(r'It achieves stratified AUROC 0\.741 on held-out E', 'E is DEVELOPMENT data (it was used to choose the method); nothing on E is confirmation', f'{L.RUN}/iter_4/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json', critique='1')}

{c.strike(r'On long composed sentences with trusted references \(R_COMP\), it reaches 0\.954', 'out-of-scope SIG (controlled vocabulary) result; not evidence for the user\'s operating condition', f'{T}/t2_record.csv', critique='1')}

{c.strike(r"It achieves 96% of the frontier judge's discriminative power", "point estimate only: ratio " + c.vc('rv_frontier_ratio') + '; and three families suffice overall but the long tercile needs k95 = ' + c.v('ev2_k95_t3'), f'{L.I3}/gen_art_experiment_6/results/analysis_T1.json', critique='1, 11')}

{c.strike(r'degrades when translators choose vocabulary independently \(R_COMP FREE d_floor 0\.402, theoretical AUROC 0\.683\)', 'both numbers are E quantities and neither is an AUROC; the vocabulary-divergence diagnosis is refuted on E (section 12)', f'{T}/p1_rule_cuts.csv', critique='5')}

**Draft.** On DEVELOPMENT data E, frozen cross-family solver consensus (`c_score_align`) beats the disguised cheap API judge: strat Δ {c.vc('t1_delta')}, long pool {c.vc('t1_long')}, and it adds signal over a 28-feature stack only when nested ({c.vc('t1_nested')}). On L25, the user's priority stratum, it is n.s. ({c.vc('t1_l25')}). The frontier ratio {c.vc('t1_ratio')} meets the 95% bar on the point estimate only. k95 = {c.v('ev2_k95')} peer families overall, but the long-sentence tercile needs {c.v('ev2_k95_t3')}. Consensus degrades with length (NET {c.vc('ev2_net')}).

The iteration-3 explanation — correct translations disagree about WORDS — is refuted on E: {c.v('e3_77')} / {c.v('e3_61')} of the peers that disagree with a correct candidate are themselves labelled ERROR, and only {c.v('e3_9')} of correct–correct disagreement is vocabulary-resolvable. Every vocabulary bridge trades d for e: the aligner lowers FULL d from {c.v('x9_full_d_fx')} to {c.v('x9_full_d_fa')} but raises meaning-rename e from {c.v('x9_t9b_mr_fx')} to {c.v('x9_t9b_mr_fa')}; cueing peers with the candidate's symbols (CSC) lowers d to {c.v('x9_d_csc')} but raises e to {c.v('x9_e_csc')}. CSC is a **provisional negative on a completion-selected subset; L25 and RENAME untested**. Error typing is negative outside a shared vocabulary (free3 {c.v('x10_free3')}). The SIG results ({c.v('t2_sig')}; SIGPROXY {c.v('x10_sigproxy')}) are out of scope. Nothing here is confirmed; the confirmation verdict (CONFIRM / PARTIAL / DISCONFIRM) comes from E2, E2-B and R_COMP FREE in iteration 5 (skeleton_iter5.md).

{src_line([f'{L.I3}/gen_art_experiment_6/results/analysis_T1.json', f'{EV2}/results/part_a.json', f'{T}/p1_class_shares.csv', A9, f'{X10}/typing_csc.csv'])}
"""


def s00_summary(c: Ctx) -> str:
    c.section = "S0"
    claims = [r for r in c.rows if r.get("value")]
    hm = [r for r in claims if r["match_hyp_vs_file"] != "MATCH"]
    pm = [r for r in claims if r["match_paper_vs_file"] == "MISMATCH"]
    n_cl = c.add("s0_nclaims", len(claims), "0", "numbers.csv :: rows with a claim literal", "claims checked")
    n_hm = c.add("s0_nhm", len(hm), "0", "numbers.csv :: match_hyp_vs_file != MATCH", "hypothesis mismatches")
    n_pm = c.add("s0_npm", len(pm), "0", "numbers.csv :: match_paper_vs_file == MISMATCH", "paper mismatches")
    hyp_txt = ("none: every hypothesis §0.2–§0.3 and review literal matches its file at the literal's precision" if not hm else
               "; ".join(f"`{r['id']}` claimed `{r['value']}` vs file {c.v(r['id'])}" for r in hm))
    rows = "\n".join(f"| `{r['id']}` | `{r['text'][:80]}` | `{r['paper_value']}` (L{r['paper_line']}) | "
                      + (c.vc(r['id']) if r.get('source_ci') else c.v(r['id'])) + " |" for r in pm)
    return f"""## 0. What this record verified

{c.v(n_cl)} claims checked; hypothesis text mismatching its source: {c.v(n_hm)}. **Hypothesis text corrected by this artifact:** {hyp_txt}.

**Paper-vs-file mismatches ({c.v(n_pm)})** — the values the iteration-4 paper prints differ from the source file (each is struck in the sections below):

| claim | quantity | paper prints | file value |
|-|-|-|-|
{rows}

{src_line(['numbers.csv', 'mismatches.csv'])}
"""


def build(c: Ctx, spend: dict) -> tuple[str, list[dict]]:
    parts = [f"""# Corrected record and paper-ready fixes (iteration 5, eval 4)

Every number below is read by code from the file named in `numbers.csv` (row id in the HTML comment after it). Struck text (`~~…~~`) is quoted verbatim from `{L.PAPER}` with its line number; the marker gives the change and the source path. All E, R_COMP SIG and PERTURB numbers are DEVELOPMENT data.
"""]
    parts.append(s00_summary(c))
    parts.append(s01_perturb(c))
    parts.append(s02_t2(c))
    parts.append(s03_mech(c))
    parts.append(s04_iter12(c))
    s5, ids = s05_ids(c)
    parts.append(s5)
    parts += [s06_verdicts(c), s07_prior(c), s08_reasoning(c), s09_exp9(c), s10_exp10(c), s11_datasets(c), s12_eval3(c),
              s13_cost(c), s14_spend(c, spend), s15_deadends(c), s16_coverage(c), s17_learned(c)]
    return "\n\n".join(parts), ids
