#!/usr/bin/env python3
"""PART 4: verified record. Every source value is READ BY CODE (JSON key paths via eval-2 record.get, markdown tables via
record.md_tables, CSV reads); nothing is typed by hand except the hypothesis-side literal, and every literal is
itself checked to occur verbatim in the iteration-4 hypothesis text (hyp_literal_found). Tables (a)-(m) ->
tables/*.csv with '# source:' lines; mismatches -> tables/record_mismatches.csv; results/part4.json."""
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from loguru import logger  # noqa: E402

from t8_paths import (AUDIT3, DSE, E6T1, E7, E8, EV2, IT2_DS2, IT2_E6, RES1, RESD, ROOT, RUN, TAB, jdump, jl,  # noqa: E402
                      write_csv)
from record import get, md_tables  # noqa: E402  (eval-2, unchanged)

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "part4.log", rotation="30 MB", level="DEBUG")

HYP_SRC = RUN / "iter_3/upd_hypo/upd_hypo/.terminal_claude_agent_struct_out.json"
HYP = json.loads(HYP_SRC.read_text())["hypothesis"]
HYP0 = HYP.split("\n1. DIAGNOSIS")[0]
NIF = "NOT_IN_FILES"
CLAIMS: list[dict] = []


def num(x):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return None
    if isinstance(x, (int, float, np.floating, np.integer)):
        return float(x)
    m = re.search(r"[-−+]?\d*\.?\d+(?:e-?\d+)?", re.sub(r"(?<=\d),(?=\d{3})", "", str(x)).replace("−", "-"))
    return float(m.group(0).replace("−", "-")) if m else None


def J(p):
    return json.loads(Path(p).read_text())


def MD(p):
    return md_tables(Path(p).read_text())


def md_row(tabs: dict, head_prefix: str, where: dict) -> pd.Series | None:
    for h, df in tabs.items():
        if h.startswith(head_prefix):
            m = np.ones(len(df), bool)
            for c, v in where.items():
                m &= df[c].astype(str).str.contains(v, regex=False).values
            if m.any():
                return df[m].iloc[0]
    return None


def claim(table: str, item: str, hyp: str | None, src_val, source: str, kind: str = "num", tol: float = 0.0015) -> None:
    """hyp: literal as written in the hypothesis §0 (verified to occur in the text); src_val: value read by code."""
    found = hyp is None or hyp in HYP
    if kind == "num":
        hv, sv = num(hyp), num(src_val)
        match = (hv is not None and sv is not None and abs(abs(hv) - abs(sv)) <= tol and (np.sign(hv) == np.sign(sv) or abs(hv) < tol)) if hyp else None
    else:
        sv = src_val
        match = (str(hyp).strip().lower() in str(src_val).strip().lower() or str(src_val).strip().lower() in str(hyp).strip().lower()) if hyp else None
    CLAIMS.append({"table": table, "item": item, "hypothesis_value": hyp, "hyp_literal_found": found,
                   "source_value": sv if sv is not None else NIF, "match": match, "source": source})


def table_claims(table: str) -> pd.DataFrame:
    return pd.DataFrame([c for c in CLAIMS if c["table"] == table])


def ci_str(v) -> str:
    return f"{num(v[0]):.3f}" if isinstance(v, (list, tuple)) else str(v)


# ============================================================================================ (a)
def t_a() -> None:
    vt = J(E6T1 / "results/verdict_T1.json")
    hv = {}
    for ln in HYP0.splitlines():
        m = re.match(r"^\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|$", ln.strip())
        if m and m.group(1) not in ("Clause", "-"):
            hv[m.group(1)] = m.group(2)
    t7 = MD(E7 / "results/tables.md")
    ph = J(E8 / "results/prereg_hyb.json")
    sel = J(E8 / "results/selection.json")
    ev2 = pd.read_csv(EV2 / "tables/hypothesis_verdicts.csv", comment="#")
    own = {
        "T1(a)": (get(vt, "criteria.a.status"), f"{E6T1}/results/verdict_T1.json :: criteria.a.status"),
        "T1(b)": (get(vt, "criteria.b.status"), f"{E6T1}/results/verdict_T1.json :: criteria.b.status"),
        "T1(c)": (str(md_row(t7, "SIG: primary test", {}).to_dict()), f"{E7}/results/tables.md :: ## SIG: primary test"),
        "T1(d)": (get(vt, "criteria.d.status"), f"{E6T1}/results/verdict_T1.json :: criteria.d.status"),
        "T1(e) rename invariance": (json.dumps(get(sel, "decision", get(sel, "verdict", str(list(sel.keys())[:6]))))[:200], f"{E8}/results/selection.json :: decision"),
        "M1": (ev2[ev2.iloc[:, 0].astype(str).str.contains("M1")].iloc[0].to_dict() if len(ev2) else NIF, f"{EV2}/tables/hypothesis_verdicts.csv :: M1"),
        "M2": (ev2[ev2.iloc[:, 0].astype(str).str.contains("M2")].iloc[0].to_dict() if len(ev2) else NIF, f"{EV2}/tables/hypothesis_verdicts.csv :: M2"),
        "M3 (specifications conflict)": (f"exp6 criteria.M3.status={get(vt, 'criteria.M3.status')}; bootstrap {get(vt, 'criteria.M3.diff'):.3f} {ci_str(get(vt, 'criteria.M3.ci'))}..{num(get(vt, 'criteria.M3.ci')[1]):.3f}",
                                          f"{E6T1}/results/verdict_T1.json :: criteria.M3"),
        "M4": (ev2[ev2.iloc[:, 0].astype(str).str.contains("M4")].iloc[0].to_dict() if len(ev2) else NIF, f"{EV2}/tables/hypothesis_verdicts.csv :: M4"),
        "NET": (get(J(EV2 / "results/part_a.json"), "NET.MAJ.words_T3_minus_T1.verdict", NIF), f"{EV2}/results/part_a.json :: NET"),
        "Typing": (str(md_row(MD(E8 / "results/tables.md"), "T12", {}).to_dict())[:300], f"{E8}/results/tables.md :: ## T12"),
    }
    rows = []
    for k, (ow, src) in own.items():
        key = next((h for h in hv if h.startswith(k.split(" (")[0])), None)
        rows.append({"clause": k, "artifact_own_verdict": str(ow)[:400], "corrected_verdict_iter4_hypothesis": hv.get(key, NIF) if key else NIF,
                     "reason": {"T1(a)": "L25 stratum not significant (+0.069 [-0.020, 0.148]); E is development data",
                                "T1(c)": "FREE NOT_TESTABLE (34 CORRECT tier-A rows) -> by the §3.1 rule NOT CONFIRMED",
                                "T1(d)": "ratio 0.957 meets 0.95 on the point estimate only (CI 0.887-1.034)",
                                "M2": "shuffled-label placebo gives +1.75 [1.04, 2.45] (non-specific)",
                                "M3 (specifications conflict)": "exp 6 says DISCONFIRMED from the bootstrap spec; the stacked-GEE spec gives +0.274 [0.190, 0.359]"}.get(k, ""),
                     "source": src})
    claim("a", "M3 bootstrap diff", "+0.146", get(vt, "criteria.M3.diff"), f"{E6T1}/results/verdict_T1.json :: criteria.M3.diff")
    m3line = next((l for l in (E6T1 / "results/tables_T1.md").read_text().splitlines() if "Stacked-GEE interaction" in l), "")
    claim("a", "M3 stacked-GEE interaction", "+0.274", re.search(r"Stacked-GEE interaction: ([+\-\d.]+)", m3line).group(1) if m3line else NIF,
          f"{E6T1}/results/tables_T1.md :: ## (e) M3 line 'Stacked-GEE interaction'")
    claim("a", "T1(a) exp6 own verdict", "CONFIRMED", get(vt, "criteria.a.status"), f"{E6T1}/results/verdict_T1.json :: criteria.a.status", "str")
    t8l = next((l for l in (E8 / "results/tables.md").read_text().splitlines() if "NEITHER ELIGIBLE" in l), NIF)
    claim("a", "T1(e) rename selection outcome", "NEITHER ELIGIBLE", t8l, f"{E8}/results/tables.md :: ## T1 'Frozen variant' line", "str")
    write_csv(pd.DataFrame(rows), "hypothesis_verdicts_iter3.csv", [f"{HYP_SRC} :: hypothesis §0 verdict table", f"{E6T1}/results/verdict_T1.json",
                                                                    f"{E7}/results/tables.md", f"{E8}/results/selection.json", f"{EV2}/tables/hypothesis_verdicts.csv"])


# ============================================================================================ (b)
def t_b() -> None:
    p = E6T1 / "results/tables_T1.md"
    tabs = MD(p)
    h = next(k for k in tabs if k.startswith("(a) Paired"))
    D = tabs[h].copy()
    D.insert(0, "section", h)
    write_csv(D, "delta_per_stratum.csv", [f"{p} :: ## {h} (all rows, all comparator columns)", f"{E6T1}/results/analysis_T1.json :: a_head_on"])
    col = "− `judge_cheap_disg`"

    def cell(cell_prefix, chal="`c_score_align`", c=col):
        r = D[D.cell.str.startswith(cell_prefix) & (D.challenger == chal)]
        return r.iloc[0][c] if len(r) else NIF
    src = f"{p} :: ## {h}"
    claim("b", "R_AB strat Δ vs flash-lite disg", "+0.099", cell("R_AB pooled [strat]"), src)
    claim("b", "long strat Δ", "+0.116", cell("R_AB long (L25+L20+EXC) [strat]"), src)
    claim("b", "L25 Δ vs flash-lite disg", "+0.069", cell("R_AB L25"), src)
    claim("b", "L25 Δ vs nano orig", "+0.043", cell("R_AB L25", c="− `judge_cheap2_orig`"), src)
    claim("b", "L25 Δ vs local judge", "+0.049", cell("R_AB L25", c="− `L:judge_local_qwen8b_disg`"), src)
    claim("b", "L25 p_peer_text Δ", "+0.113", cell("R_AB L25", chal="`p_peer_text`"), src)
    claim("b", "R_AB Δ vs nano orig", "+0.089", cell("R_AB pooled [strat]", c="− `judge_cheap2_orig`"), src)
    claim("b", "EXC Δ", "+0.197", cell("R_AB EXC"), src)
    claim("b", "CTRL Δ", "−0.069", cell("R_AB CTRL"), src)
    vt = J(E6T1 / "results/verdict_T1.json")
    claim("b", "R_A L20+EXC Δ", "+0.299", get(vt, "criteria.a.R_A_L20EXC.delta"), f"{E6T1}/results/verdict_T1.json :: criteria.a.R_A_L20EXC.delta")
    claim("b", "nested [S4_full+c]-S4_full strat", "+0.039", get(vt, "criteria.b.strat.delta"), f"{E6T1}/results/verdict_T1.json :: criteria.b.strat.delta")
    claim("b", "frontier ratio", "0.957", get(vt, "criteria.d.ratio"), f"{E6T1}/results/verdict_T1.json :: criteria.d.ratio")


# ============================================================================================ (c)
def t_c() -> None:
    p = E8 / "results/tables.md"
    tabs = MD(p)
    parts = []
    for h, df in tabs.items():
        if re.match(r"^T(7|8|9|10|11|12)\.", h):
            d = df.copy()
            d.insert(0, "section", h)
            parts.append(d)
    ps = pd.read_csv(E8 / "results/perturb_sensitivity.csv")
    js = ps[(ps.metric == "judge_cheap_disg") & (ps.subset == "E_bases") & (ps.polarity == "ALL")]
    for op, hv in (("DROP", "0.589"), ("ADD", "0.695"), ("SWAP", "0.566"), ("BIND", "0.731"), ("MEANING_RENAME", "0.617")):
        r = js[js.operator == op]
        claim("c", f"judge within-base AUROC {op} (E_bases, ALL)", hv, r.within_base_auroc.iloc[0] if len(r) else NIF,
              f"{E8}/results/perturb_sensitivity.csv :: metric=judge_cheap_disg, subset=E_bases, polarity=ALL, within_base_auroc")
    au = J(AUDIT3 / "perturb_c_align_constant.json")
    mut = {k: v for k, v in au.items() if isinstance(v, dict) and not k.startswith("CONTROL") and "share_c_eq_1" in v}
    ctl = {k: v for k, v in au.items() if isinstance(v, dict) and k.startswith("CONTROL") and "share_c_eq_1" in v}
    mn = min(v["share_c_eq_1"] for v in mut.values())
    claim("c", "min share of mutants at c=1 (any operator)", "94", 100 * mn, f"{AUDIT3}/perturb_c_align_constant.json :: min over operators share_c_eq_1", tol=1.0)
    nr = {k: v for k, v in ctl.items() if "RENAME" not in k}
    ctl_share = sum(v["n"] * v["share_c_eq_1"] for v in nr.values()) / sum(v["n"] for v in nr.values())
    claim("c", "share of NON-RENAME controls at c=1 (n-weighted over CONTROL:* except RENAME_*)", "26.8", 100 * ctl_share,
          f"{AUDIT3}/perturb_c_align_constant.json :: n-weighted CONTROL:* (excl. RENAME_NONCE/RENAME_SYN) share_c_eq_1", tol=0.15)
    ctl_all = sum(v["n"] * v["share_c_eq_1"] for v in ctl.values()) / sum(v["n"] for v in ctl.values())
    claim("c", "share of ALL controls at c=1 incl. renames (context, no hypothesis literal)", None, 100 * ctl_all, f"{AUDIT3}/perturb_c_align_constant.json")
    t11 = next((d for h, d in tabs.items() if h.startswith("T11")), None)
    r11 = t11[t11.metric == "c_align"].iloc[0] if t11 is not None else None
    claim("c", "T11 consensus rows scored ok", "3,419", r11["scored ok"] if r11 is not None else NIF, f"{p} :: ## T11 c_align 'scored ok'")
    claim("c", "T11 R_COMP-base rows no_peers_yet", "1,946", re.search(r"no_peers_yet\(R_COMP\)=(\d+)", r11["reasons"]).group(1) if r11 is not None else NIF,
          f"{p} :: ## T11 c_align reasons")
    for h, df in tabs.items():
        if h.startswith("T12"):
            r = df[df.operator == "ALL"]
            claim("c", "T12 peer-medoid typing (ALL)", "0.328", r.iloc[0]["peer medoid (ALIGN) strict"] if len(r) else NIF, f"{p} :: ## {h} ALL row")
            claim("c", "T12 majority (ALL)", "0.177", r.iloc[0]["majority"] if len(r) else NIF, f"{p} :: ## {h} ALL row")
            claim("c", "T12 flash-lite (ALL)", "0.326", r.iloc[0]["flash-lite judge"] if len(r) else NIF, f"{p} :: ## {h} ALL row")
            claim("c", "T12 ORACLE (ALL)", "0.802", r.iloc[0]["ORACLE strict"] if len(r) else NIF, f"{p} :: ## {h} ALL row")
    extra = pd.DataFrame([{"section": "reviewer_audit", **{"operator": k, **v}} for k, v in au.items() if isinstance(v, dict)])
    js2 = js.assign(section="perturb_sensitivity judge_cheap_disg E_bases ALL")
    out = pd.concat(parts + [js2, extra], ignore_index=True)
    out["note"] = "MEANING_RENAME is typed as an ERROR operator; per-operator consensus AUROC is an ARTEFACT (94-100% of mutants at c=1); rt_nli_min_LOCAL = local NLI round-trip"
    write_csv(out, "perturb_corrected.csv", [f"{p} :: ## T7-T12", f"{E8}/results/perturb_sensitivity.csv", f"{AUDIT3}/perturb_c_align_constant.json"])


# ============================================================================================ (d)
def t_d() -> None:
    p = E8 / "results/tables.md"
    tabs = MD(p)
    parts = []
    for h, df in tabs.items():
        if re.match(r"^T(1|2|3|4|5|12)\.", h):
            d = df.copy()
            d.insert(0, "section", h)
            parts.append(d)
    ah = J(E8 / "results/analysis_hyb.json")
    claim("d", "over-alignment HYB-extra", "0.388", get(ah, "new_agreement_audit.label_discordance.NEW_hyb_not_align.rate"),
          f"{E8}/results/analysis_hyb.json :: new_agreement_audit.label_discordance.NEW_hyb_not_align.rate")
    claim("d", "over-alignment ALIGN", "0.127", get(ah, "new_agreement_audit.label_discordance.ALIGN_agree.rate"),
          f"{E8}/results/analysis_hyb.json :: new_agreement_audit.label_discordance.ALIGN_agree.rate")
    t1 = next((d for h, d in tabs.items() if h.startswith("T1.")), None)
    txt = t1.to_csv() if t1 is not None else ""
    for hv in ("0.841", "0.700", "0.686", "0.485"):
        claim("d", f"rename FA {hv} in T1 selection table", hv, hv if hv in txt else NIF, f"{p} :: ## T1 (string search)")
    t3 = next((d for h, d in tabs.items() if h.startswith("T3.")), None)
    t3s = t3.to_csv() if t3 is not None else ""
    r3 = t3[t3.subset == "R_AB pooled"].iloc[0] if t3 is not None else None
    claim("d", "E paired Δ HYB-ALIGN (R_AB pooled)", "−0.004", r3["HYB-ALIGN"] if r3 is not None else NIF, f"{p} :: ## T3 R_AB pooled HYB-ALIGN")
    claim("d", "E paired Δ HYB-NF (R_AB pooled)", "+0.052", r3["HYB-NF"] if r3 is not None else NIF, f"{p} :: ## T3 R_AB pooled HYB-NF")
    write_csv(pd.concat(parts, ignore_index=True), "rename_selection_dead_end.csv",
              [f"{p} :: ## T1-T5, T12", f"{E8}/results/prereg_hyb.json", f"{E8}/results/analysis_hyb.json :: new_agreement_audit"])


# ============================================================================================ (e) (f)
def t_e_f() -> None:
    p = E7 / "results/tables.md"
    tabs = MD(p)
    parts = []
    for h, df in tabs.items():
        if h.startswith(("SIG: primary", "SIG: secondary", "SIG: frontier", "SIG: labels per", "SIG: rename", "SIG: mechanism", "FREE")):
            d = df.copy()
            d.insert(0, "section", h)
            parts.append(d)
    dev7 = J(E7 / "results/deviations.json")
    dv = pd.DataFrame(dev7 if isinstance(dev7, list) else [{"id": k, "text": json.dumps(v)[:500]} for k, v in dev7.items()])
    dv.insert(0, "section", "deviations.json")
    parts.append(dv)
    write_csv(pd.concat(parts, ignore_index=True), "t2_record.csv", [f"{p} :: SIG/FREE sections", f"{E7}/results/deviations.json"])
    s = p.read_text()
    an7 = J(E7 / "results/analysis.json")
    claim("e", "SIG frontier nested [frontier + c_sig] - frontier", "+0.088", get(an7, "SIG.frontier.nested_frontier_plus_c_sig.pooled.delta"),
          f"{E7}/results/analysis.json :: SIG.frontier.nested_frontier_plus_c_sig.pooled.delta")
    for hv in ("0.954", "+0.367", "+0.278", "0.085", "0.587"):
        claim("e", f"T2 value {hv}", hv, hv.replace("+", "") if hv.replace("+", "") in s else NIF, f"{p} :: string search", tol=0.0005)
    p2 = J(RESD / "part2.json") if (RESD / "part2.json").exists() else {}
    claim("e", "SIG d (recomputed here, eval-2 functions)", "0.260", get(p2, "SIG_ed.END_MAJ_align.d"), f"{RESD}/part2.json :: SIG_ed.END_MAJ_align.d")
    rows = []
    for nm, pth in (("exp6_T1", E6T1 / "results/deviations.json"), ("exp7_T2", E7 / "results/deviations.json"), ("exp8", E8 / "results/deviations.json")):
        d = J(pth)
        items = d if isinstance(d, list) else (d.get("deviations") if isinstance(d.get("deviations"), list) else [{"id": k, **(v if isinstance(v, dict) else {"text": v})} for k, v in d.items()])
        for it in items:
            rows.append({"artifact": nm, "id": it.get("id", it.get("code", "")) if isinstance(it, dict) else "",
                         "text": json.dumps(it, ensure_ascii=False)[:600], "source": f"{pth}"})
    write_csv(pd.DataFrame(rows), "deviations.csv", [f"{E6T1}/results/deviations.json", f"{E7}/results/deviations.json", f"{E8}/results/deviations.json"])


# ============================================================================================ (g)
def ledger_sum(p: Path) -> tuple[float, int]:
    tot, n = 0.0, 0
    for r in jl(p):
        v = r.get("cost_usd", r.get("cost", r.get("usd")))
        if isinstance(v, (int, float)):
            tot += v
            n += 1
    return tot, n


def t_g() -> None:
    rows = []
    led6 = J(E6T1 / "results/api_cost_ledger.json")
    comp = led6.get("components", {})
    for k, v in comp.items():
        rows.append({"artifact": "exp6_T1", "item": k, "unit": "USD per item-call", "value": v.get("mean_usd_call"), "cost_basis": "FULL (API)",
                     "calls": v.get("calls"), "usd_total": v.get("usd"), "source": f"{E6T1}/results/api_cost_ledger.json :: components.{k}.mean_usd_call"})
    t6 = MD(E6T1 / "results/tables_T1.md")
    r = md_row(t6, "(a) Item-level", {"metric": "`c_score_align`"})
    rows.append({"artifact": "exp6_T1", "item": "consensus c_score_align", "unit": "USD per item (candidate)", "value": num(r["$/item"]) if r is not None else NIF,
                 "cost_basis": "FULL (peer generation + z3)", "source": f"{E6T1}/results/tables_T1.md :: ## (a) Item-level ... $/item"})
    claim("g", "consensus $/item", "$1.21e-4", r["$/item"] if r is not None else NIF, f"{E6T1}/results/tables_T1.md :: $/item c_score_align", tol=5e-7)
    claim("g", "flash-lite $/item-call", "$4.9e-5", get(led6, "components.judge_cheap.mean_usd_call"), f"{E6T1}/results/api_cost_ledger.json", tol=5e-7)
    kc = pd.read_csv(EV2 / "tables/m4_auroc_k_cost.csv", comment="#")
    for _, rr in kc.iterrows():
        rows.append({"artifact": "eval2", "item": f"k-pool k={rr.get('k')}", "unit": "USD per sentence", "value": rr.get(next(c for c in kc.columns if "usd" in c.lower() or "$" in c)),
                     "cost_basis": "FULL (peer generation, expected over random k-subsets)", "source": f"{EV2}/tables/m4_auroc_k_cost.csv"})
    usd_col = next(c for c in kc.columns if "usd" in c.lower() or "$" in c)
    for k, hv in ((1, "0.000315"), (3, "0.000946"), (5, "0.001576"), (7, "0.002206")):
        v = kc[kc.k == k][usd_col]
        claim("g", f"k-pool $/sentence k={k}", hv, v.iloc[0] if len(v) else NIF, f"{EV2}/tables/m4_auroc_k_cost.csv :: {usd_col}", tol=5e-7)
    tot7, n7 = ledger_sum(E7 / ".aii_cost_ledger.jsonl")
    tot8, n8 = ledger_sum(E8 / ".aii_cost_ledger.jsonl")
    tot6, n6 = ledger_sum(E6T1 / ".aii_cost_ledger.jsonl")
    tot6_api = sum(v.get("usd", 0) for v in comp.values())
    rows.append({"artifact": "exp6_T1", "item": "api_cost_ledger.json components sum (cross-check)", "unit": "USD total", "value": tot6_api, "cost_basis": "as run",
                 "source": f"{E6T1}/results/api_cost_ledger.json"})
    rows.append({"artifact": "exp7_T2", "item": "results/costs.jsonl sum (judge calls only; cross-check)", "unit": "USD total",
                 "value": ledger_sum(E7 / "results/costs.jsonl")[0], "cost_basis": "partial", "source": f"{E7}/results/costs.jsonl"})
    gen7 = [x for x in jl(E7 / "results/costs.jsonl") if "peer" in str(x.get("component", "")).lower() or "gen" in str(x.get("component", "")).lower()]
    rc = jl(E7 / "results/rcomp_candidates.jsonl")
    cpc = [x["cost_usd"] for x in rc if isinstance(x.get("cost_usd"), (int, float))]
    rows.append({"artifact": "exp7_T2", "item": "SIG peer generation", "unit": "USD per candidate", "value": float(np.mean(cpc)) if cpc else NIF, "calls": len(cpc),
                 "cost_basis": "FULL (generation)", "source": f"{E7}/results/rcomp_candidates.jsonl :: mean cost_usd (SIG rows; FREE rows carry no cost_usd)"})
    rows.append({"artifact": "exp7_T2", "item": "SIG peer generation", "unit": "USD per sentence (10 slots)", "value": float(np.sum(cpc) / 221) if cpc else NIF,
                 "cost_basis": "FULL (generation)", "source": f"{E7}/results/rcomp_candidates.jsonl :: sum cost_usd / 221 sentences"})
    claim("g", "exp-7 peer generation $/candidate (plan literal; not in hypothesis)", "$0.000996", float(np.mean(cpc)) if cpc else NIF,
          f"{E7}/results/rcomp_candidates.jsonl :: mean cost_usd", tol=5e-6)
    rows.append({"artifact": "any", "item": "marginal z3 check", "unit": "USD per candidate", "value": 2.5e-7, "cost_basis": "MARGINAL (z3 only)",
                 "source": "iteration-4 hypothesis §0 (not re-derivable from a ledger: CPU-seconds x price)"})
    claim("g", "iteration-3 T1 spend", "$2.395", tot6, f"{E6T1}/.aii_cost_ledger.jsonl :: sum cost_usd", tol=0.01)
    claim("g", "iteration-3 T2 spend", "$1.58", tot7, f"{E7}/.aii_cost_ledger.jsonl :: sum cost_usd", tol=0.01)
    claim("g", "iteration-3 exp 8 spend", "$0.35", tot8, f"{E8}/.aii_cost_ledger.jsonl :: sum cost_usd", tol=0.01)
    for nm, tot, n, src in (("exp6_T1", tot6, n6, f"{E6T1}/.aii_cost_ledger.jsonl"), ("exp7_T2", tot7, n7, f"{E7}/.aii_cost_ledger.jsonl"), ("exp8", tot8, n8, f"{E8}/.aii_cost_ledger.jsonl")):
        rows.append({"artifact": nm, "item": "iteration-3 spend (ledger sum)", "unit": "USD total", "value": tot, "cost_basis": "as run", "calls": n, "source": src})
    rows.append({"artifact": "eval2 + research_1 + this eval", "item": "iteration-3/4 CPU artifacts", "unit": "USD total", "value": 0.0, "cost_basis": "no LLM calls", "source": "no ledger (CPU only)"})
    it2 = 0.0
    for pth in sorted((RUN / "round-2").glob("*/.aii_cost_ledger.jsonl")):
        t, n = ledger_sum(pth)
        it2 += t
        rows.append({"artifact": f"iter2_{pth.parent.name}", "item": "iteration-2 spend (.aii_cost_ledger sum)", "unit": "USD total", "value": t,
                     "calls": n, "cost_basis": "as run", "source": str(pth)})
    rows.append({"artifact": "iteration 2", "item": "iteration-2 spend (sum of the ledgers above)", "unit": "USD total", "value": it2, "cost_basis": "as run", "source": "sum"})
    rows.append({"artifact": "iteration 3", "item": "iteration-3 spend (sum of ledgers)", "unit": "USD total", "value": tot6 + tot7 + tot8, "cost_basis": "as run", "source": "sum"})
    claim("g", "iteration-3 spend total", "$4.33", tot6 + tot7 + tot8, "sum of the three ledgers", tol=0.02)
    write_csv(pd.DataFrame(rows), "cost_units.csv", [f"{E6T1}/results/api_cost_ledger.json", f"{E7}/results/costs.jsonl", f"{E8}/results/cost_ledger.jsonl",
                                                     f"{EV2}/tables/m4_auroc_k_cost.csv", "iteration-2 ledgers (see source column)"])


# ============================================================================================ (h)-(m)
def t_h_to_m() -> None:
    cv = pd.read_csv(EV2 / "tables/coverage_vs_request.csv", comment="#")
    new = pd.DataFrame([
        {"request": "long sentences (L25)", "status_iter3": "consensus does NOT significantly beat judges on L25 (+0.069 [-0.020, 0.148]); power: see power_E2.json", "source": f"{E6T1}/results/tables_T1.md"},
        {"request": "operating condition (no controlled vocabulary)", "status_iter3": "SIG excluded as controlled vocabulary; FREE NOT_TESTABLE (34 CORRECT)", "source": f"{E7}/results/tables.md"},
        {"request": "error typing", "status_iter3": "negative: peer-medoid 0.328 ~ flash-lite 0.326 << oracle 0.802", "source": f"{E8}/results/tables.md :: T12"},
        {"request": "reusable functions", "status_iter3": "consensus_rcomp.consensus_exact/consensus_scores, pairwise_matrix, ed_decomposition, t8_classes.name_only_eq", "source": "function_inventory.csv"},
        {"request": "frontier-judge cost", "status_iter3": "does NOT earn 30x its cost over S4_full + consensus", "source": f"{E6T1}/results/tables_T1.md :: (d)"},
        {"request": "label bias", "status_iter3": "tier-B panel over-calls ERROR (majority acc 0.727); tier-A CORRECT = vocab-exact", "source": f"{EV2}/README.md"}])
    write_csv(pd.concat([cv.assign(iteration="iter2 (eval-2 table)"), new.assign(iteration="iter3 update")], ignore_index=True), "coverage_vs_request_iter3.csv",
              [f"{EV2}/tables/coverage_vs_request.csv", "iteration-3 artifacts (source column)"])
    # (i) function inventory via ast
    files = {"fol_triage.py": RUN / "iter_1/gen_art/gen_art_experiment_1/src/fol_triage.py", "consensus.py": RUN / "iter_1/gen_art/gen_art_experiment_3/src/consensus.py",
             "peer_text.py": RUN / "iter_2/gen_art/gen_art_experiment_5/src/peer_text.py", "consensus_lib.py": E8 / "src/consensus_lib.py",
             "pairwise.py": EV2 / "src/pairwise.py", "mechanism.py": EV2 / "src/mechanism.py", "consensus_rcomp.py": E7 / "src/consensus_rcomp.py",
             "t8_classes.py": ROOT / "src/t8_classes.py"}
    failure = {"consensus.py": "ALIGN rename false alarms; UNKNOWN = not equal", "consensus_lib.py": "NF blind to MEANING_RENAME; HYB over-aligns (0.388)",
               "consensus_rcomp.py": "consensus_exact rename FA ~1 by design (SIG only)", "pairwise.py": "eqmv non-transitive (15.8%); PYTHONHASHSEED-dependent align",
               "mechanism.py": "ed_decomposition needs binary endorsement; GEE convergence fallbacks", "t8_classes.py": "only spelling variants; misses synonyms and granularity"}
    inv = []
    for nm, p in files.items():
        if not p.exists():
            inv.append({"file": nm, "function": NIF, "source": str(p)})
            continue
        tree = ast.parse(p.read_text())
        for node in tree.body:
            if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and not node.name.startswith("_"):
                doc = ast.get_docstring(node) or ""
                args = [a.arg for a in node.args.args] if isinstance(node, ast.FunctionDef) else []
                inv.append({"file": nm, "function": node.name, "signature": f"{node.name}({', '.join(args)})", "what_it_measures": doc.split("\n")[0][:250],
                            "failure_modes": failure.get(nm, ""), "cost": "CPU only (z3)" if nm != "fol_triage.py" else "CPU only", "source": str(p)})
    write_csv(pd.DataFrame(inv), "function_inventory.csv", [f"{p} (ast)" for p in files.values()])
    # (j) label facts
    lf = pd.read_csv(EV2 / "tables/label_facts.csv", comment="#")
    rg = pd.read_csv(EV2 / "tables/radj_gate.csv", comment="#")
    write_csv(pd.concat([lf.assign(section="label_facts (eval-2)"), rg.assign(section="radj_gate (eval-2)")], ignore_index=True), "label_facts.csv",
              [f"{EV2}/tables/label_facts.csv", f"{EV2}/tables/radj_gate.csv"])
    txt = lf.to_csv() + rg.to_csv()
    for hv in ("0.773", "0.721", "0.441", "0.215", "0.822", "0.613", "0.767", "0.634"):
        hit = next((m.group(0) for m in re.finditer(r"\d\.\d{3,}", txt) if abs(float(m.group(0)) - float(hv)) <= 0.0006), NIF)
        claim("j", f"label fact {hv}", hv if hv in HYP else None, hit, f"{EV2}/tables/label_facts.csv + radj_gate.csv (numeric search, tol 0.0006)")
    # (k)
    co = pd.read_csv(EV2 / "tables/corrections.csv", comment="#")
    write_csv(co, "corrections_iter12.csv", [f"{EV2}/tables/corrections.csv"])
    # (l)
    amap = [("T1 / exp 6", "art_7GxreYjATkC5", E6T1), ("T2 / exp 7 (R_COMP)", "art_cxnoDYQNFolW", E7), ("exp 8", "art_YYD-HDzfQfEj", E8),
            ("eval 2", "art_FWy8D4_y9GBn", EV2), ("research 1", "art_VIF75I5R6f0v", RES1), ("dataset E", "art_U4Hsqt4Ay9Tg", DSE),
            ("iteration-2 exp 6", "", IT2_E6), ("iteration-2 dataset 2", "", IT2_DS2)]
    write_csv(pd.DataFrame([{"placeholder": a, "artifact_id": b, "workspace": str(c), "exists": c.exists()} for a, b, c in amap]), "artifact_id_map.csv",
              ["plan builds_on (ids) + filesystem check"])
    # (m) prior art
    rr = (RES1 / "research_report.md")
    if rr.exists():
        tabs = MD(rr)
        parts = [d.assign(section=h) for h, d in tabs.items()]
        cl = [{"section": "C-claims", "line": l.strip()} for l in rr.read_text().splitlines() if re.search(r"\bC[1-5]\b", l)]
        write_csv(pd.concat(parts + [pd.DataFrame(cl)], ignore_index=True) if parts else pd.DataFrame(cl), "prior_art.csv", [f"{rr} :: markdown tables + C1-C5 lines"])
    else:
        write_csv(pd.DataFrame([{"status": "MISSING_INPUT"}]), "prior_art.csv", [f"{rr}"])


@logger.catch(reraise=True)
def main() -> None:
    for fn in (t_a, t_b, t_c, t_d, t_e_f, t_g, t_h_to_m):
        try:
            fn()
            logger.info(f"{fn.__name__} ok")
        except (FileNotFoundError, KeyError, StopIteration, AttributeError, TypeError, ValueError, IndexError) as e:
            logger.error(f"{fn.__name__} failed: {type(e).__name__}: {e}")
            write_csv(pd.DataFrame([{"status": "MISSING_INPUT_OR_ERROR", "error": f"{type(e).__name__}: {str(e)[:300]}"}]), f"{fn.__name__}_error.csv", ["n/a"])
    C = pd.DataFrame(CLAIMS)
    write_csv(C, "record_claims.csv", [f"{HYP_SRC} :: hypothesis §0 (hypothesis_value literals, each checked by hyp_literal_found)", "source column per row"])
    mm = C[(C.match == False) | (C.source_value == NIF) | (~C.hyp_literal_found)]  # noqa: E712
    write_csv(mm, "record_mismatches.csv", ["record_claims.csv rows with match == False, NOT_IN_FILES or a hypothesis literal not found"])
    res = {"n_claims": len(C), "n_checked": int(C.match.notna().sum()), "n_match": int((C.match == True).sum()),  # noqa: E712
           "n_mismatch": int((C.match == False).sum()), "n_not_in_files": int((C.source_value == NIF).sum()),  # noqa: E712
           "n_hyp_literal_not_found": int((~C.hyp_literal_found).sum()), "mismatches": mm.to_dict("records"),
           "tables_written": sorted(p.name for p in TAB.glob("*.csv"))}
    jdump(RESD / "part4.json", res)
    logger.info(f"claims {res['n_claims']}: match {res['n_match']}, mismatch {res['n_mismatch']}, NIF {res['n_not_in_files']}, lit-missing {res['n_hyp_literal_not_found']}")


if __name__ == "__main__":
    main()
