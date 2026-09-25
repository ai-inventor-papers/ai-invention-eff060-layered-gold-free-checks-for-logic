"""PART B (verified record): every number re-read from files; each CSV starts with '# source: <abs path> :: <key path>'.
A value that cannot be found in any file is written as NOT_IN_FILES (never copied from prose)."""
from __future__ import annotations

import ast
import csv
import glob
import hashlib
import io
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import pandas as pd
from loguru import logger
from sklearn.linear_model import LogisticRegression

from paths import DS2, DS3, DS_E, E5, E6, EV1, I1, REVIEW, ROOT, jl, sha256_file
from stats import SentBoot, WAuc, WStratAuc, auc, ci, strat_auc

TAB = ROOT / "tables"
NIF = "NOT_IN_FILES"


def write_csv(df: pd.DataFrame, name: str, sources: list[str]):
    with (TAB / name).open("w") as fh:
        for s in sources:
            fh.write(f"# source: {s}\n")
        df.to_csv(fh, index=False)


def get(obj, path: str, default=NIF):
    """Read a dotted key path ('a.b[0].c'). Keys may themselves contain dots, spaces or '|' ('FA0.10_fractional',
    'MDE_2.8SE'): at each dict level the LONGEST key that prefixes the remaining path is taken."""
    cur, rest = obj, path
    while rest:
        rest = rest.lstrip(".")
        m = re.match(r"\[(\d+)\]", rest)
        if m:
            if not isinstance(cur, list) or int(m.group(1)) >= len(cur):
                return default
            cur, rest = cur[int(m.group(1))], rest[m.end():]
            continue
        if not isinstance(cur, dict):
            return default
        hits = [k for k in cur if isinstance(k, str) and (rest == k or rest.startswith(k + ".") or rest.startswith(k + "["))]
        if not hits:
            return default
        k = max(hits, key=len)
        cur, rest = cur[k], rest[len(k):]
    return cur


def J(p: Path):
    return json.loads(Path(p).read_text())


# =================================================================================================== (i) exp 6
def md_tables(md: str) -> dict[str, pd.DataFrame]:
    """Every '## heading' followed by a markdown table -> DataFrame."""
    out = {}
    cur = None
    lines = md.splitlines()
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("## "):
            cur = ln[3:].strip()
        if ln.startswith("|") and i + 1 < len(lines) and re.match(r"^\|[-| :]+\|$", lines[i + 1].strip()) and cur:
            hdr = [c.strip() for c in ln.strip().strip("|").split("|")]
            rows = []
            i += 2
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            out[cur] = pd.DataFrame([r[:len(hdr)] + [""] * (len(hdr) - len(r)) for r in rows], columns=hdr)
            continue
        i += 1
    return out


def _slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "_", s.split(":")[0]).strip("_")[:50]


def exp6_tables() -> dict:
    sm = (E6 / "results" / "summary.md").read_text()
    an = J(E6 / "results" / "analysis_E.json")
    tabs = md_tables(sm)
    info = {}
    for head, df in tabs.items():
        setkey = head.split(":")[0].strip()
        chk = []
        if setkey in an.get("sets", {}) and "AUROC [95% CI]" in df.columns:
            for r in df.itertuples(index=False):
                m = r[0]
                fv = get(an, f"sets.{setkey}.metrics.{m}.auroc")
                pv = re.match(r"(-?[0-9.]+)", r[1])
                if fv == NIF or pv is None:
                    chk.append(NIF)
                else:
                    chk.append("MATCH" if abs(float(fv) - float(pv.group(1))) <= 5e-4 else f"DISCREPANT(file={fv})")
            df = df.assign(crosscheck_analysis_E_json=chk)
        name = f"exp6_{_slug(head)}.csv"
        write_csv(df, name, [f"{E6}/results/summary.md :: ## {head}",
                             f"{E6}/results/analysis_E.json :: sets.{setkey}.metrics.<metric>.auroc (cross-check column)"])
        info[name] = {"rows": len(df), "n_match": sum(c == "MATCH" for c in chk), "n_checked": len(chk)}
    # bullet sections read from analysis_E.json directly
    rows = []
    for j, v in an["contamination"].items():
        if not isinstance(v, dict) or "DiD" not in v:
            continue
        rows.append({"judge": j, "E_POOL_delta_disg": get(v, "E_POOL.delta_disg"), "GOLDSYS_delta_disg": get(v, "GOLDSYS.delta_disg"),
                     "DiD": get(v, "DiD.point"), "DiD_ci_lo": get(v, "DiD.ci[0]"), "DiD_ci_hi": get(v, "DiD.ci[1]"),
                     "MDE_2.8SE": get(v, "DiD.MDE_2.8SE"), "probe_DiD": get(v, "gold_recognition_probe.DiD.point")})
    write_csv(pd.DataFrame(rows), "exp6_contamination_DiD.csv", [f"{E6}/results/analysis_E.json :: contamination.<judge>.{{E_POOL,GOLDSYS,DiD}}"])
    rows = []
    for m, v in an["complexity_gee"].items():
        for var, d in v.items():
            if isinstance(d, dict) and "slope_per_sd" in d:
                rows.append({"metric": m, "variable": var, "slope_per_sd": d["slope_per_sd"], "se": d.get("se"), "p": d.get("p"),
                             "ci_lo": get(d, "ci[0]"), "ci_hi": get(d, "ci[1]")})
    write_csv(pd.DataFrame(rows), "exp6_complexity_gee.csv", [f"{E6}/results/analysis_E.json :: complexity_gee.<metric>.<variable>"])
    sysl = []
    for ln in sm.split("## System level")[1].splitlines():
        m = re.match(r"- (\S+): τ=(\S+) \[(\S+), (\S+)\] ; 11-family τ=(\S+) \[(\S+), (\S+)\]", ln)
        if m:
            sysl.append(dict(zip(["metric", "tau_b_13", "lo_13", "hi_13", "tau_b_11fam", "lo_11fam", "hi_11fam"], m.groups())))
    write_csv(pd.DataFrame(sysl), "exp6_system_level.csv", [f"{E6}/results/summary.md :: ## System level (Kendall τ-b, 13 system×variant rows; descriptive)"])
    fr = re.search(r"## Frame \(284 rows\)[^\n]*\n\n```\n(.*?)```", sm, re.S)
    if fr:
        fj = json.loads(fr.group(1))
        write_csv(pd.DataFrame([{"contrast": k, **{kk: (vv if not isinstance(vv, list) else json.dumps(vv)) for kk, vv in v.items()}}
                                for k, v in fj.items()]), "exp6_frame_284.csv",
                  [f"{E6}/results/summary.md :: ## Frame (284 rows): larger vs cheap judge"])
    # deviations (F-KEY etc.)
    dev = [{"id": "F-KEY", "text": get(an, "bar_note"), "source_key": "analysis_E.json :: bar_note"},
           {"id": "missing_components", "text": json.dumps(get(an, "missing_components")), "source_key": "analysis_E.json :: missing_components"},
           {"id": "api_spend_total_usd", "text": str(get(an, "api_spend_total_usd")), "source_key": "analysis_E.json :: api_spend_total_usd"}]
    rd = (E6 / "README.md").read_text()
    dep = rd.split("## Departures from the plan")[1].split("\n## ")[0] if "## Departures from the plan" in rd else ""
    for k, ln in enumerate(l for l in dep.splitlines() if l.strip().startswith(("-", "*", "1", "2", "3", "4", "5", "6", "7", "8", "9"))):
        dev.append({"id": f"README_departure_{k + 1}", "text": ln.strip()[:400], "source_key": "README.md :: ## Departures from the plan"})
    write_csv(pd.DataFrame(dev), "exp6_deviations.csv", [f"{E6}/results/analysis_E.json", f"{E6}/README.md :: ## Departures from the plan (all logged)"])
    # B2 dead end
    g = J(E6 / "results" / "b2_gate.json")
    t = J(E6 / "results" / "b2_think_diagnostic.json")
    b2 = [{"quantity": "gate balanced accuracy (track-H corrected, non-thinking reader)", "value": get(g, "primary_gate_trackH_corrected.bal_acc"),
           "target": ">= 0.85", "source": f"{E6}/results/b2_gate.json :: primary_gate_trackH_corrected.bal_acc"},
          {"quantity": "b2_score AUROC R_AB pooled", "value": get(an, "sets.R_AB|pooled.metrics.b2_score.auroc"), "target": "",
           "source": f"{E6}/results/analysis_E.json :: sets.R_AB|pooled.metrics.b2_score.auroc"},
          {"quantity": "b2_score AUROC R_AB long pool", "value": get(an, "sets.R_AB|long_L25_L20_EXC.metrics.b2_score.auroc"), "target": "",
           "source": f"{E6}/results/analysis_E.json :: sets.R_AB|long_L25_L20_EXC.metrics.b2_score.auroc"},
          {"quantity": "dropped-condition UNDETERMINED AUROC", "value": get(an, "b2.undet_share_DROP_vs_CORRECT.auroc"), "target": "",
           "source": f"{E6}/results/analysis_E.json :: b2.undet_share_DROP_vs_CORRECT.auroc"},
          {"quantity": "thinking-mode reader balanced accuracy (post hoc)", "value": get(t, "thinking_reader_on_completed_items.bal_acc"),
           "target": "post hoc; not pursued", "source": f"{E6}/results/b2_think_diagnostic.json :: thinking_reader_on_completed_items.bal_acc"},
          {"quantity": "thinking-mode reader completed items / gate items", "value": f"{get(t, 'thinking_reader_on_completed_items.n_items_ok')}/{get(t, 'gate_items')}",
           "target": "", "source": f"{E6}/results/b2_think_diagnostic.json :: thinking_reader_on_completed_items.n_items_ok, gate_items"}]
    df = pd.DataFrame(b2)
    df["status"] = "DROPPED (settled negative; not retried)"
    write_csv(df, "b2_dead_end.csv", [f"{E6}/results/b2_gate.json", f"{E6}/results/b2_think_diagnostic.json", f"{E6}/results/analysis_E.json"])
    info["b2"] = b2
    return info


# =================================================================================================== (ii) R_ADJ
def radj_gate() -> pd.DataFrame:
    g = J(DS2 / "gate_report.json")
    card = (DS2 / "radj_card.md").read_text()
    rows = []
    for mdl, nm in (("primary", "sonnet-5"), ("grok", "grok-4.20")):
        for half in ("gate", "dev", "all"):
            for sub in ("overall", "synthetic", "H", "H-orig", "H-corr"):
                o = get(g, f"{mdl}.{half}.{sub}", None)
                if o is None:
                    continue
                n_unf, k_unf = o.get("n_unfaithful"), o.get("k_unfaithful")
                amb = o.get("ambiguous_reading_rate", [None])[0]
                n_amb = round(amb * o["n"]) if amb is not None else None
                judged_faithful = (n_unf - k_unf - (n_amb or 0) - (o.get("parse_fail") or 0)) if (sub == "H-orig" and n_unf) else None
                rows.append({"adjudicator": nm, "half": half, "subset": sub, "n": o["n"], "balanced_accuracy": o.get("balanced_accuracy"),
                             "recall_faithful": o["recall_faithful"][0], "recall_unfaithful": o["recall_unfaithful"][0],
                             "expert_rejected_originals_judged_FAITHFUL": judged_faithful,
                             "gate_pass": g.get(f"{mdl}_gate_pass"), "robust_pass": g.get(f"{mdl}_robust_pass"),
                             "source_key": f"gate_report.json :: {mdl}.{half}.{sub}"})
    df = pd.DataFrame(rows)
    extra = [{"adjudicator": "sonnet-5 vs grok-4.20", "half": "all", "subset": "kappa (all)", "n": get(g, "kappa_sonnet_grok_all.n"),
              "balanced_accuracy": None, "recall_faithful": None, "recall_unfaithful": None,
              "kappa": get(g, "kappa_sonnet_grok_all.kappa"), "source_key": "gate_report.json :: kappa_sonnet_grok_all.kappa"}]
    m = re.search(r"- ALL: n=(\d+), flip rate ([0-9.]+) \[([0-9.]+), ([0-9.]+)\], κ\(first, retest\) = ([0-9.]+)", card)
    if m:
        extra.append({"adjudicator": "sonnet-5 test-retest", "half": "ALL", "subset": "retest", "n": int(m.group(1)), "flip_rate": float(m.group(2)),
                      "kappa": float(m.group(5)), "source_key": "radj_card.md :: ## 4. T2 — test-retest :: - ALL"})
    m = re.search(r"On real E rows \(cell D, (\d+) rows\): κ = ([0-9.]+), raw agreement ([0-9.]+)", card)
    if m:
        extra.append({"adjudicator": "sonnet-5 vs grok-4.20", "half": "cell D", "subset": "kappa on real E rows", "n": int(m.group(1)),
                      "kappa": float(m.group(2)), "raw_agreement": float(m.group(3)), "source_key": "radj_card.md :: cell D kappa line"})
    m = re.search(r"- \*\*cell D\*\*: `error\|faithful\|CORRECT` (\d+), `faithful\|error\|CORRECT` (\d+), `error\|faithful\|ERROR` (\d+)", card)
    if m:
        extra.append({"adjudicator": "cell-D cross-tab (solver|panel|UNGATED primary)", "half": "cell D", "subset": "T4",
                      "crosstab": f"error|faithful|CORRECT {m.group(1)}; faithful|error|CORRECT {m.group(2)}; error|faithful|ERROR {m.group(3)}",
                      "source_key": "radj_card.md :: ## 6. T4 :: cell D"})
    tot = sum(float(json.loads(l).get("cost_usd") or 0) for l in (DS2 / "cost_ledger.jsonl").read_text().splitlines() if l.strip())
    m = re.search(r"Total \*\*\$([0-9.]+)\*\*", card)
    extra.append({"adjudicator": "spend", "half": "all", "subset": "USD", "usd_ledger_sum": round(tot, 4),
                  "usd_card": float(m.group(1)) if m else NIF, "source_key": "cost_ledger.jsonl (sum cost_usd); radj_card.md :: Total"})
    df = pd.concat([df, pd.DataFrame(extra)], ignore_index=True)
    df["status"] = "GATE FAILED -> DROPPED" if not (g.get("primary_gate_pass") or g.get("grok_gate_pass")) else "GATE PASSED"
    write_csv(df, "radj_gate.csv", [f"{DS2}/gate_report.json", f"{DS2}/radj_card.md", f"{DS2}/cost_ledger.jsonl"])
    return df


# =================================================================================================== (iii) PT vs S4 rerun
def _f(x):
    try:
        v = float(x)
        return None if np.isnan(v) else v
    except (TypeError, ValueError):
        return None


def pt_vs_s4() -> dict:
    """Independent re-implementation of the reviewer audit (own join, own stack, own bootstrap), plus stratified rows."""
    e6 = J(E6 / "full_method_out.json")
    six = defaultdict(list)
    for ds in e6["datasets"]:
        if ds["dataset"] == "E_heldout":
            for ex in ds["examples"]:
                six[(ex["metadata_item_id"], json.loads(ex["input"]).get("prompt_variant"))].append(ex)
    del e6
    five = defaultdict(list)
    for r in jl(E5 / "results" / "per_item_E.jsonl"):
        five[(r["item_id"], r["prompt_variant"])].append(r)
    recs = []
    for k, L in six.items():
        if len(L) != 1 or len(five.get(k, [])) != 1:
            continue
        ex, r = L[0], five[k][0]
        if not ex.get("metadata_in_R_AB") or ex["output"] not in ("ERROR", "CORRECT"):
            continue
        recs.append({"y": int(ex["output"] == "ERROR"), "sid": ex["metadata_sentence_id"], "fold": ex["metadata_fold_E"],
                     "stratum": ex["metadata_strata"]["source_stratum"], "tier": ex.get("metadata_label_tier"),
                     "pt": _f(r["p_peer_text"]), "cal": _f(r["c_score_align"]), "s4": _f(ex.get("predict_S4_local_oof_RAB")),
                     "s4nj": _f(ex.get("predict_S4_local_noLLMjudge_oof_RAB")), "jl": _f(ex.get("predict_judge_local_qwen8b_disg"))})
    n_join = len(recs)
    D = pd.DataFrame([r for r in recs if None not in (r["pt"], r["cal"], r["s4"], r["s4nj"], r["jl"])]).reset_index(drop=True)
    y = D.y.values

    def stack(cols):
        Z = D[cols].values
        oof = np.zeros(len(D))
        for f in sorted(D.fold.unique()):
            tr, te = (D.fold != f).values, (D.fold == f).values
            mu, sd = Z[tr].mean(0), Z[tr].std(0) + 1e-9
            oof[te] = LogisticRegression(C=1.0, max_iter=2000).fit((Z[tr] - mu) / sd, y[tr]).predict_proba((Z[te] - mu) / sd)[:, 1]
        return oof
    D["s4_plus_pt"] = stack(["s4", "pt"])
    D["s4_refit"] = stack(["s4"])
    rev = J(REVIEW / "audit" / "pt_vs_s4.json")
    rows = []
    boot = SentBoot(D.sid.values, b=2000, seed=0)

    def pair(a, b, mask, label, strat=False):
        m = mask
        W = boot.W(m)
        if strat:
            fa, fb = WStratAuc(y[m], D[a].values[m], D.stratum.values[m]), WStratAuc(y[m], D[b].values[m], D.stratum.values[m])
            pt_ = strat_auc(y[m], D[a].values[m], D.stratum.values[m]) - strat_auc(y[m], D[b].values[m], D.stratum.values[m])
        else:
            fa, fb = WAuc(y[m], D[a].values[m]), WAuc(y[m], D[b].values[m])
            pt_ = auc(y[m], D[a].values[m]) - auc(y[m], D[b].values[m])
        ds = [fa(W[i]) - fb(W[i]) for i in range(W.shape[0])]
        return {"subset": label, "statistic": "stratified" if strat else "pooled", "quantity": f"{a} - {b}", "n": int(m.sum()),
                "n_err": int(y[m].sum()), "n_sent": int(D.sid[m].nunique()), "delta": pt_, "ci_lo": ci(ds)[0], "ci_hi": ci(ds)[1]}
    ALL = np.ones(len(D), bool)
    LONG = D.stratum.isin(["L25", "L20", "EXC"]).values
    RA = (D.tier == "A").values & D.stratum.isin(["L20", "EXC"]).values
    revmap = {("pt", "s4"): "delta_pt_minus_s4local", ("cal", "s4"): "delta_cal_minus_s4local", ("pt", "s4nj"): "delta_pt_minus_s4_noLLMjudge",
              ("pt", "jl"): "delta_pt_minus_judge_local", ("s4_plus_pt", "s4_refit"): "nested_s4pt_minus_s4refit"}
    for (a, b), rk in revmap.items():
        for mask, lab in ((ALL, "R_AB pooled"), (LONG, "R_AB long (L25+L20+EXC)"), (RA, "R_A L20+EXC")):
            for strat in (False, True):
                r = pair(a, b, mask, lab, strat)
                if lab == "R_AB pooled" and not strat:
                    rv = rev.get(rk)
                    r["reviewer_delta"] = rv[0] if rv else NIF
                    r["reviewer_ci_lo"], r["reviewer_ci_hi"] = (rv[1][0], rv[1][1]) if rv else (NIF, NIF)
                    r["point_match_1e-4"] = bool(rv and abs(r["delta"] - rv[0]) <= 1e-4 + 5e-5)
                    r["ci_match_0.01"] = bool(rv and abs(r["ci_lo"] - rv[1][0]) <= 0.01 and abs(r["ci_hi"] - rv[1][1]) <= 0.01)
                rows.append(r)
    au = {k: auc(y, D[k].values) for k in ["pt", "cal", "s4", "s4nj", "jl", "s4_plus_pt", "s4_refit"]}
    auc_rows = [{"subset": "R_AB pooled", "statistic": "pooled", "quantity": f"AUROC {k}", "n": len(D), "delta": v,
                 "reviewer_delta": get(rev, f"auroc.{k}"), "point_match_1e-4": abs(v - get(rev, f"auroc.{k}")) <= 1e-4 + 5e-5}
                for k, v in au.items()]
    for k in ["pt", "s4", "jl", "cal"]:
        v = auc(y[LONG], D[k].values[LONG])
        auc_rows.append({"subset": "R_AB long (L25+L20+EXC)", "statistic": "pooled", "quantity": f"AUROC {k}", "n": int(LONG.sum()), "delta": v,
                         "reviewer_delta": get(rev, f"long_pool.{k}"), "point_match_1e-4": abs(v - get(rev, f"long_pool.{k}")) <= 1e-4 + 5e-5})
    for k in ["pt", "cal", "s4", "s4nj", "jl", "s4_plus_pt", "s4_refit"]:
        auc_rows.append({"subset": "R_AB pooled", "statistic": "stratified", "quantity": f"AUROC {k}", "n": len(D),
                         "delta": strat_auc(y, D[k].values, D.stratum.values)})
    out = pd.DataFrame(auc_rows + rows)
    write_csv(out, "pt_vs_s4_rerun.csv", [f"{E6}/full_method_out.json :: datasets[E_heldout].examples (metadata_in_R_AB, output, predict_S4_local_oof_RAB, predict_S4_local_noLLMjudge_oof_RAB, predict_judge_local_qwen8b_disg, metadata_fold_E)",
                                          f"{E5}/results/per_item_E.jsonl :: p_peer_text, c_score_align (raw)",
                                          f"{REVIEW}/audit/pt_vs_s4.json :: reviewer target values",
                                          "method: own join on (item_id, prompt_variant) unique rows; stack = train-fold standardise + LogisticRegression(C=1, max_iter=2000); sentence-cluster bootstrap B=2000 default_rng(0) as multiplicity weights (RNG order differs from the reviewer's)"])
    summ = {"n_joined_R_AB": n_join, "n_complete": len(D), "n_sent": int(D.sid.nunique()),
            "all_points_match": bool(out["point_match_1e-4"].dropna().astype(bool).all()),
            "all_cis_match": bool(out["ci_match_0.01"].dropna().astype(bool).all()),
            "rows": out.to_dict("records")}
    return summ


# =================================================================================================== (iv) corrections
def corrections() -> pd.DataFrame:
    a5 = J(E5 / "results" / "analysis.json")
    a6 = J(E6 / "results" / "analysis_E.json")
    sf = J(E5 / "results" / "screen_fit.json")
    x4 = J(I1 / "experiment-4/src" / "results" / "method_out.json")
    m1 = J(I1 / "experiment-1/src" / "results" / "metrics.json")
    mfa = pd.read_csv(EV1 / "tables" / "judge_matched_fa.csv", comment="#")
    fsi = pd.read_csv(EV1 / "tables" / "frontier_same_item.csv", comment="#")
    R = []

    def add(i, claim, val, path, key, ok):
        R.append({"id": i, "claim_as_reported": claim, "corrected_value": val, "source_path": str(path), "key_path": key, "verified": bool(ok)})
    v = get(a6, "contamination.judge_local_llama8b.DiD")
    add("C1a", "iteration-2 report: contamination DiD on E not reported for exp 6 (only exp 5's orig-vs-disg delta)",
        f"Llama-8B DiD {v['point']:+.3f} [{v['ci'][0]:.3f}, {v['ci'][1]:.3f}]" if v != NIF else NIF, E6 / "results/analysis_E.json",
        "contamination.judge_local_llama8b.DiD.{point,ci}", v != NIF)
    v = get(a6, "contamination.judge_local_qwen8b.DiD")
    add("C1b", "same", f"Qwen-8B DiD {v['point']:+.3f} [{v['ci'][0]:.3f}, {v['ci'][1]:.3f}] n.s., MDE {v['MDE_2.8SE']:.3f}" if v != NIF else NIF,
        E6 / "results/analysis_E.json", "contamination.judge_local_qwen8b.DiD.{point,ci,MDE_2.8SE}", v != NIF)
    v = get(a5, "i_contamination.judge_local_qwen8b.orig_minus_disg")
    add("C1c", "exp 5 contamination arm: disguise IMPROVES the Qwen judge on E (orig - disg)",
        f"{v['delta']:+.3f} [{v['ci'][0]:.3f}, {v['ci'][1]:.3f}]" if v != NIF else NIF, E5 / "results/analysis.json",
        "i_contamination.judge_local_qwen8b.orig_minus_disg", v != NIF)
    for reg in ("R_SOLVER_CONS", "R_ADJ_AB"):
        r = mfa[(mfa.regime == reg) & (mfa.judge == "judge_cheap") & (mfa.cell == "ALL") & (mfa.fa_target == 0.1)]
        ok = len(r) == 1
        add(f"C2_{reg}", "report: disguise 'forces structural reading' (disguised judge better)",
            f"ORIGINAL judge ahead at matched FA 0.10: recall orig - disg {r.diff_orig_minus_disg.iloc[0]:+.3f} [{r.ci_lo.iloc[0]:.3f}, {r.ci_hi.iloc[0]:.3f}] ({reg})" if ok else NIF,
            EV1 / "tables/judge_matched_fa.csv", f"regime={reg}, judge=judge_cheap, cell=ALL, fa_target=0.1 :: diff_orig_minus_disg", ok)
    v = get(sf, "models.fusion.oof_auroc")
    w = get(a5, "a_tables.R_AB pooled.metrics.p_peer_text.auroc")
    add("C3", "report: fusion fit on AGREE items (screen) 0.943 presented as the fused metric's quality",
        f"screen AGREE-item fusion OOF AUROC {v:.3f} shrinks to held-out E R_AB {w:.3f}" if NIF not in (v, w) else NIF,
        f"{E5}/results/screen_fit.json ; {E5}/results/analysis.json", "models.fusion.oof_auroc ; a_tables.R_AB pooled.metrics.p_peer_text.auroc",
        NIF not in (v, w))
    d = get(x4, "metadata.analysis.paired_strong_subset.L_strong_subset.judge_cheap_orig.judge_strong_orig")
    r = fsi[(fsi.regime == "R_ADJ_AB") & (fsi.strong == "judge_strong_orig") & (fsi.cheap == "judge_cheap_orig")]
    ok = d != NIF and len(r) == 1
    add("C4", "report: frontier-judge advantage weakens under panel labels",
        (f"STRENGTHENS: solver labels {d['delta_auroc']:+.3f} [{d['ci'][0]:.3f}, {d['ci'][1]:.3f}] -> panel A+B {r.delta.iloc[0]:+.3f} "
         f"{r.ci.iloc[0]} n={int(r.n.iloc[0])}") if ok else NIF,
        f"{I1}/gen_art_experiment_4/results/method_out.json ; {EV1}/tables/frontier_same_item.csv",
        "metadata.analysis.paired_strong_subset.L_strong_subset.judge_cheap_orig.judge_strong_orig ; regime=R_ADJ_AB strong=judge_strong_orig cheap=judge_cheap_orig", ok)
    g1 = get(a5, "b_P1.R_AB.FA0.10_fractional.groups.PEER_ENDORSED.recall.judge_local_qwen8b_disg")  # key contains a dot
    g2 = get(a5, "b_P1.R_AB.FA0.10_fractional.groups.PEER_ENDORSED_NF.recall.judge_local_qwen8b_disg")
    add("C5", "report: P1 group names mixed (PEER_ENDORSED vs PEER_ENDORSED_NF); judge column omitted",
        f"local judge recall at FA 0.10: PEER_ENDORSED {g1:.3f}, PEER_ENDORSED_NF {g2:.3f} (highest recall on both endorsed groups)" if NIF not in (g1, g2) else NIF,
        E5 / "results/analysis.json", "b_P1.R_AB.FA0.10_fractional.groups.{PEER_ENDORSED,PEER_ENDORSED_NF}.recall.judge_local_qwen8b_disg", NIF not in (g1, g2))
    fa5 = get(a5, "e_P4.families.RENAME.fused.FA")
    fa1 = get(m1, "invariance.RENAME.fused_flag.FA")
    fl1 = get(m1, "invariance.RENAME.fused_flag.flip_rate")
    add("C6", "report: P4 compared fused RENAME FA 0.385 with FOL-Triage '0.013'",
        f"FA vs FA: PEER+TEXT fused RENAME FA {fa5:.3f} vs FOL-Triage fused RENAME FA {fa1:.2f}; 0.013 was FOL-Triage's FLIP rate ({fl1:.4f})"
        if NIF not in (fa5, fa1, fl1) else NIF, f"{E5}/results/analysis.json ; {I1}/gen_art_experiment_1/results/metrics.json",
        "e_P4.families.RENAME.fused.FA ; invariance.RENAME.fused_flag.{FA,flip_rate}", NIF not in (fa5, fa1, fl1))
    # true iteration-2 OpenRouter spend
    parts = []
    c5 = sum(json.loads(l).get("cost", 0) or 0 for l in (E5 / "results/costs.jsonl").read_text().splitlines() if l.strip())
    l3 = 0.0
    for l in (E5 / "results/E_l3_q.jsonl").read_text().splitlines():
        if l.strip():
            d = json.loads(l)
            l3 += sum(d[k] for k in ("cost", "cost_usd") if isinstance(d.get(k), (int, float)))
            u = d.get("usage") or {}
            l3 += u.get("cost", 0) if isinstance(u, dict) and isinstance(u.get("cost"), (int, float)) else 0
    m5 = re.search(r"Total OpenRouter spend of this artifact: \*\*\$([0-9.]+)\*\*", (E5 / "README.md").read_text())
    parts.append((f"exp5 (costs.jsonl judge {c5:.4f} + E_l3_q.jsonl L3 {l3:.4f}; README states ${m5.group(1) if m5 else NIF})", c5 + l3,
                  f"{E5}/results/costs.jsonl + {E5}/results/E_l3_q.jsonl"))
    parts.append(("exp6 (analysis_E.json api_spend_total_usd)", float(get(a6, "api_spend_total_usd", 0) or 0), E6 / "results/analysis_E.json"))
    for nm, p in (("dataset2", DS2 / "cost_ledger.jsonl"), ("dataset3", DS3 / "cost_ledger.jsonl")):
        parts.append((f"{nm} (cost_ledger.jsonl sum cost_usd)", sum(float(json.loads(l).get("cost_usd") or 0) for l in p.read_text().splitlines() if l.strip()), p))
    parts.append(("evaluation1 (no LLM calls; no ledger)", 0.0, EV1))
    tot = sum(p[1] for p in parts)
    add("C7", "iteration-2 report spend statement",
        f"total ${tot:.3f} = " + " + ".join(f"{n} ${v:.3f}" for n, v, _ in parts), " ; ".join(str(p[2]) for p in parts), "sums as named", True)
    df = pd.DataFrame(R)
    write_csv(df, "corrections.csv", ["each row names its own source_path and key_path; values read programmatically by src/record.py"])
    return df


# =================================================================================================== (v) R_PANEL renames
def regimes_panel() -> pd.DataFrame:
    ren = {"R_ADJ_AB": "R_PANEL_AB", "R_ADJ_ALL": "R_PANEL_ALL", "R_ADJ_A": "R_PANEL_A", "R_ADJ_AB_CONT_C": "R_PANEL_AB_CONT_C",
           "R_ADJ_AB_CONT_E": "R_PANEL_AB_CONT_E", "H_ADJ_AB": "H_PANEL_AB"}
    rows = []
    for old, new in ren.items():
        p = EV1 / "tables" / f"available_case_{old}.csv"
        cp = EV1 / "tables" / f"common_items_{old}.csv"
        if not p.exists():
            rows.append({"old_name": old, "new_name": new, "n": NIF})
            continue
        d = pd.read_csv(p, comment="#")
        c = pd.read_csv(cp, comment="#") if cp.exists() else None
        n = int(d.n.max())
        ne = int(d.n_err.max())
        nsent = int(c.n_sent.max()) if (c is not None and "n_sent" in c.columns) else NIF
        rows.append({"old_name": old, "new_name": new, "n_max_available_case": n, "n_err": ne, "n_cor": n - ne, "n_sentences": nsent,
                     "testable_50_50": bool(ne >= 50 and n - ne >= 50), "source": f"{p} :: max(n), max(n_err)"})
    df = pd.DataFrame(rows)
    df["note"] = "these regimes are dataset E's own Haiku/GLM/Kimi screen-audit panel labels, NOT the R_ADJ adjudicator (dataset 2, DROPPED)"
    write_csv(df, "regimes_R_PANEL.csv", [f"{EV1}/tables/available_case_*.csv :: n, n_err", f"{EV1}/tables/common_items_*.csv", f"{EV1}/tables/bookkeeping.csv"])
    return df


# =================================================================================================== (vi) hypothesis verdicts
def hypothesis_verdicts(A: dict, pts: dict, lab: pd.DataFrame) -> pd.DataFrame:
    a5 = J(E5 / "results" / "analysis.json")
    a6 = J(E6 / "results" / "analysis_E.json")
    g = J(DS2 / "gate_report.json")
    rev = J(REVIEW / "audit" / "pt_vs_s4.json")
    rows = []

    def chk(cid, text, claimed, fval, src, prec=3):
        if fval in (NIF, None):
            st = "NOT_IN_FILES"
        else:
            st = "VERIFIED_MATCH" if round(float(fval), prec) == round(float(claimed), prec) or abs(float(fval) - float(claimed)) <= 0.5 * 10 ** -prec + 1e-12 else "DISCREPANT"
        rows.append({"clause_id": cid, "clause_text": text[:200], "status": st, "claimed": claimed,
                     "file_value": None if fval in (NIF, None) else round(float(fval), 4), "source": src})
    T = "a_tables.R_AB pooled.metrics"
    chk("i.PT_pooled", "Frozen PEER+TEXT 0.790 pooled (R_AB)", 0.790, get(a5, f"{T}.p_peer_text.auroc"), f"{E5}/results/analysis.json :: {T}.p_peer_text.auroc")
    chk("i.c_score_align", "c_score_align 0.782", 0.782, get(a5, f"{T}.c_score_align.auroc"), f"{E5}/results/analysis.json :: {T}.c_score_align.auroc")
    chk("i.nf_c_score", "NF-anchored c_score 0.743", 0.743, get(a5, f"{T}.nf_c_score.auroc"), f"{E5}/results/analysis.json :: {T}.nf_c_score.auroc")
    chk("i.TEXT", "TEXT 0.693", 0.693, get(a5, f"{T}.p_text.auroc"), f"{E5}/results/analysis.json :: {T}.p_text.auroc")
    chk("i.judge", "local Qwen3-8B disguised judge 0.710 (exp 6)", 0.710, get(a6, "sets.R_AB|pooled.metrics.judge_local_qwen8b_disg.auroc"),
        f"{E6}/results/analysis_E.json :: sets.R_AB|pooled.metrics.judge_local_qwen8b_disg.auroc")
    S = "a_stratified.R_AB pooled.stratified_auroc"
    for k, m, v in (("PT", "p_peer_text", 0.753), ("c_score_align", "c_score_align", 0.741), ("PEER-g", "peer_only", 0.694),
                    ("TEXT", "p_text", 0.670), ("judge", "judge_local_qwen8b_disg", 0.677)):
        chk(f"i.strat_{k}", f"stratified {k} {v}", v, get(a5, f"{S}.{m}.auroc"), f"{E5}/results/analysis.json :: {S}.{m}.auroc")
    chk("i.strat_PT-judge", "PT - judge stratified +0.075 [0.036, 0.114]", 0.075, get(a5, "a_stratified.R_AB pooled.delta_fused_minus_local_judge.delta"),
        f"{E5}/results/analysis.json :: a_stratified.R_AB pooled.delta_fused_minus_local_judge.delta")
    chk("i.strat_long", "long pool +0.086", 0.086, get(a5, "a_stratified.R_AB long (L25+L20+EXC).delta_fused_minus_local_judge.delta"),
        f"{E5}/results/analysis.json :: a_stratified.R_AB long (L25+L20+EXC).delta_fused_minus_local_judge.delta")
    chk("i.strat_RA", "R_A L20+EXC +0.208", 0.208, get(a5, "a_stratified.R_A pooled L20+EXC.delta_fused_minus_local_judge.delta"),
        f"{E5}/results/analysis.json :: a_stratified.R_A pooled L20+EXC.delta_fused_minus_local_judge.delta")
    chk("i.placebo", "within-stratum placebo 0.59", 0.59, get(a5, "placebo_within_stratum.p_peer_text", None) if not isinstance(get(a5, "placebo_within_stratum.p_peer_text", None), dict)
        else get(a5, "placebo_within_stratum.p_peer_text.mean"), f"{E5}/results/analysis.json :: placebo_within_stratum.p_peer_text", prec=2)
    for cid, k, v in (("i.PT-S4", "delta_pt_minus_s4local", 0.042), ("i.cal-S4", "delta_cal_minus_s4local", 0.035),
                      ("i.PT-S4nj", "delta_pt_minus_s4_noLLMjudge", 0.087), ("i.nested", "nested_s4pt_minus_s4refit", 0.055)):
        mine = next((r["delta"] for r in pts["rows"] if r["quantity"] == {"delta_pt_minus_s4local": "pt - s4", "delta_cal_minus_s4local": "cal - s4",
                     "delta_pt_minus_s4_noLLMjudge": "pt - s4nj", "nested_s4pt_minus_s4refit": "s4_plus_pt - s4_refit"}[k]
                     and r["subset"] == "R_AB pooled" and r["statistic"] == "pooled"), None)
        chk(cid, f"{k} {v:+.3f} (reviewer audit; re-run here)", v, mine, f"{ROOT}/tables/pt_vs_s4_rerun.csv (independent re-run of {REVIEW}/audit/pt_vs_s4.json :: {k})")
    chk("i.long_PT", "On the long pool PT 0.769", 0.769, get(rev, "long_pool.pt"), f"{REVIEW}/audit/pt_vs_s4.json :: long_pool.pt")
    chk("i.long_S4", "S4_local 0.711 on long pool", 0.711, get(rev, "long_pool.s4"), f"{REVIEW}/audit/pt_vs_s4.json :: long_pool.s4")
    chk("i.PT-cal_strat", "PT - c_score_align stratified +0.011", 0.011, get(a5, "a_stratified.R_AB pooled.delta_fused_minus_c_score_align.delta"),
        f"{E5}/results/analysis.json :: a_stratified.R_AB pooled.delta_fused_minus_c_score_align.delta")
    chk("i.RA_cal", "R_A c_score_align 0.860", 0.860, get(a5, "a_tables.R_A pooled L20+EXC.metrics.c_score_align.auroc"),
        f"{E5}/results/analysis.json :: a_tables.R_A pooled L20+EXC.metrics.c_score_align.auroc")
    chk("i.RA_PT", "R_A PT 0.818", 0.818, get(a5, "a_tables.R_A pooled L20+EXC.metrics.p_peer_text.auroc"),
        f"{E5}/results/analysis.json :: a_tables.R_A pooled L20+EXC.metrics.p_peer_text.auroc")
    rows.append({"clause_id": "ii.untested_bars", "clause_text": "API flash-lite judge untestable on E (20 rows); no API SC-5 / round-trip / frontier rows on E",
                 "status": "OWNED_BY_OTHER_ARTIFACT (T1)", "claimed": None, "file_value": None, "source": "T1 experiment (iteration 3)"})
    chk("ii.frontier_solver", "frontier advantage +0.077 under solver labels", 0.077,
        get(J(I1 / "experiment-4/src/results/method_out.json"), "metadata.analysis.paired_strong_subset.L_strong_subset.judge_cheap_orig.judge_strong_orig.delta_auroc"),
        f"{I1}/gen_art_experiment_4/results/method_out.json :: metadata.analysis.paired_strong_subset.L_strong_subset.judge_cheap_orig.judge_strong_orig.delta_auroc")
    fsi = pd.read_csv(EV1 / "tables/frontier_same_item.csv", comment="#")
    r = fsi[(fsi.regime == "R_ADJ_AB") & (fsi.strong == "judge_strong_orig") & (fsi.cheap == "judge_cheap_orig")]
    chk("ii.frontier_panel", "+0.166 under panel A+B (n=90)", 0.166, r.delta.iloc[0] if len(r) else None, f"{EV1}/tables/frontier_same_item.csv :: R_ADJ_AB strong_orig vs cheap_orig delta")
    chk("ii.frontier_cost", "frontier judge $0.0029/call", 0.0029, get(J(I1 / "experiment-4/src/results/method_out.json"),
        "metadata.analysis.cost.judge_strong (API, per condition).usd_per_call"),
        f"{I1}/gen_art_experiment_4/results/method_out.json :: metadata.analysis.cost['judge_strong (API, per condition)'].usd_per_call", prec=4)
    fl = pd.read_csv(EV1 / "tables/flipped_items.csv", comment="#")
    r = fl[(fl.definition == "D_solver") & (fl.group == "CORRECT->ERROR") & (fl.metric == "c_score")]
    chk("iii.flip_catch_34pct", "c_score_align catches only 34% of solver-CORRECT->panel-ERROR flips (evaluation_1)", 0.34,
        r["share_flagged_FA0.20"].iloc[0] if len(r) else None, f"{EV1}/tables/flipped_items.csv :: definition=D_solver, group=CORRECT->ERROR, metric=c_score :: share_flagged_FA0.20", prec=2)
    chk("iii.RENAME_FA_align", "c_score_align RENAME FA 0.859", 0.859, get(a5, "e_P4.families.RENAME.c_score_align.FA"),
        f"{E5}/results/analysis.json :: e_P4.families.RENAME.c_score_align.FA")
    chk("iv.P2_spearman", "P2 REFUTED: Spearman(PEER, TEXT | error) = 0.294", 0.294, get(a5, "c_P2.spearman_peer_text_errors"),
        f"{E5}/results/analysis.json :: c_P2.spearman_peer_text_errors")
    chk("iv.P3_interaction", "P3 metric length interaction -0.023", -0.023, get(a5, "d_P3.p_peer_text.interaction"), f"{E5}/results/analysis.json :: d_P3.p_peer_text.interaction")
    chk("iv.P4_FA", "P4 REFUTED: fused RENAME FA 0.385", 0.385, get(a5, "e_P4.families.RENAME.fused.FA"), f"{E5}/results/analysis.json :: e_P4.families.RENAME.fused.FA")
    chk("iv.unit_typing", "unit-code typing 0.371 vs chance 0.382", 0.371, get(a5, "f_error_types.top_code_accuracy"), f"{E5}/results/analysis.json :: f_error_types.top_code_accuracy")
    chk("iv.judge_slope", "exp 6 GEE judge slope -0.56/SD words", -0.56, get(a6, "complexity_gee.judge_local_qwen8b_disg.words.slope_per_sd"),
        f"{E6}/results/analysis_E.json :: complexity_gee.judge_local_qwen8b_disg.words.slope_per_sd", prec=2)
    chk("v.B2_gate", "B2 gate balanced accuracy 0.476", 0.476, get(J(E6 / "results/b2_gate.json"), "primary_gate_trackH_corrected.bal_acc"),
        f"{E6}/results/b2_gate.json :: primary_gate_trackH_corrected.bal_acc")
    chk("v.B2_pooled", "B2 0.574 pooled", 0.574, get(a6, "sets.R_AB|pooled.metrics.b2_score.auroc"), f"{E6}/results/analysis_E.json :: sets.R_AB|pooled.metrics.b2_score.auroc")
    chk("v.RADJ_sonnet", "R_ADJ Sonnet-5 gate balanced accuracy 0.767", 0.767, get(g, "primary.gate.overall.balanced_accuracy"), f"{DS2}/gate_report.json :: primary.gate.overall.balanced_accuracy")
    chk("v.RADJ_sonnet_H", "0.662 on expert track-H pairs", 0.662, get(g, "primary.gate.H.balanced_accuracy"), f"{DS2}/gate_report.json :: primary.gate.H.balanced_accuracy")
    chk("v.RADJ_grok", "Grok-4.20 0.634", 0.634, get(g, "grok.gate.overall.balanced_accuracy"), f"{DS2}/gate_report.json :: grok.gate.overall.balanced_accuracy")
    chk("v.pilot_rerun", "pilot_rerun_jacc 0.660", 0.660, get(a6, "sets.R_AB|pooled.metrics.pilot_rerun_jacc.auroc"), f"{E6}/results/analysis_E.json :: sets.R_AB|pooled.metrics.pilot_rerun_jacc.auroc")
    chk("vi.llama_DiD", "Llama-8B judge DiD +0.162", 0.162, get(a6, "contamination.judge_local_llama8b.DiD.point"), f"{E6}/results/analysis_E.json :: contamination.judge_local_llama8b.DiD.point")
    chk("vi.qwen_DiD", "Qwen-8B DiD +0.036 n.s. (MDE 0.107)", 0.036, get(a6, "contamination.judge_local_qwen8b.DiD.point"), f"{E6}/results/analysis_E.json :: contamination.judge_local_qwen8b.DiD.point")
    for st, v in (("L25", 0.773), ("L20", 0.721), ("EXC", 0.441), ("CTRL", 0.215)):
        fv = lab[(lab.fact == "correct_not_equivalent_share_R_AB") & (lab.cell == st)]["value"]
        chk(f"vii.CNE_{st}", f"correct-but-not-equivalent share {st} {v}", v, fv.iloc[0] if len(fv) else None, f"{ROOT}/tables/label_facts.csv (computed from {E5}/data/E_labels.jsonl)")
    chk("vii.gold_error", "panel judges MALLS gold wrong 0.822", 0.822, get(a6, "label_quality.gold_error.MALLS_all.rate"), f"{E6}/results/analysis_E.json :: label_quality.gold_error.MALLS_all.rate")
    fv = lab[lab.fact == "panel_majority_accepts_expert_corrected"]["value"]
    chk("vii.expert_accept", "panel accepts 0.613 of expert-corrected formulas", 0.613, fv.iloc[0] if len(fv) else None, f"{DS_E}/dataset_card.md :: majority row")
    chk("vii.retest", "test-retest Spearman 0.989", 0.989, get(J(E6 / "results/retest_vs_sibling.json"), "disg.spearman"), f"{E6}/results/retest_vs_sibling.json :: disg.spearman")
    # mechanism clauses tested here
    M = A["M1_M2"]
    rows.append({"clause_id": "M1", "clause_text": "peer-endorsement rate among errors falls with n_conditions (GEE slope < 0, CI excludes 0)",
                 "status": "TESTED_HERE", "claimed": None, "file_value": M["M1"]["MAJ|primary"]["verdict"], "source": f"{ROOT}/eval_out.json :: metadata.verdicts.M1"})
    rows.append({"clause_id": "M2", "clause_text": "divergence among CORRECT rows rises with words", "status": "TESTED_HERE", "claimed": None,
                 "file_value": M["M2"]["MAJ|primary"]["verdict"], "source": f"{ROOT}/eval_out.json :: metadata.verdicts.M2"})
    rows.append({"clause_id": "M3", "clause_text": "consensus length slope less negative than the API judge's (difference CI > 0)",
                 "status": "OWNED_BY_OTHER_ARTIFACT (T1); local-judge version TESTED_HERE (secondary)", "claimed": None,
                 "file_value": json.dumps(A["M3_local"]["slope_diff_ci"]), "source": f"{ROOT}/eval_out.json :: metadata.verdicts.M3_local"})
    rows.append({"clause_id": "M3_T4", "clause_text": "distinct z3 classes among erroneous vs correct outputs per sentence",
                 "status": "TESTED_HERE", "claimed": None, "file_value": None, "source": f"{ROOT}/eval_out.json :: metadata.scatter (cpo_err, cpo_cor)"})
    rows.append({"clause_id": "M4", "clause_text": "k needed to reach 95% of the full-pool AUROC is <= 5 families", "status": "TESTED_HERE", "claimed": None,
                 "file_value": A["M4"]["random_k_primary"]["k95"], "source": f"{ROOT}/eval_out.json :: metadata.verdicts.M4"})
    for c, own in (("a", "T1"), ("b", "T1"), ("c", "T2 (vocab-exact part partly TESTED_HERE)"), ("d", "T1"), ("e", "T3")):
        rows.append({"clause_id": f"CONFIRM.{c}", "clause_text": f"success criterion ({c})", "status": f"OWNED_BY_OTHER_ARTIFACT ({own})",
                     "claimed": None, "file_value": None, "source": "hypothesis SUCCESS CRITERIA"})
    df = pd.DataFrame(rows)
    write_csv(df, "hypothesis_verdicts.csv", [f"{ROOT}/inputs_copy/hypothesis_iter2_upd.txt :: CORRECTED RECORD (i)-(vii), MECHANISM M1-M4, CONFIRM (a)-(e)",
                                              "each row's own source column"])
    return df


# =================================================================================================== (vii) coverage / (viii) inventory
def coverage_vs_request() -> pd.DataFrame:
    old = pd.read_csv(EV1 / "tables" / "coverage_vs_request.csv", comment="#")
    old["iteration"] = "1 (evaluation_1 view)"
    new = [
        ("item-level correlation with correctness", "iter2 exp5 results/tables.md; iter2 exp6 summary.md; this artifact tables/ed_decomposition_cuts.csv", "answered", "held-out E; local judge bar only (API bar = T1)"),
        ("system-level correlation", "iter2 exp6 tables/exp6_system_level.csv (13 rows, 11 families)", "partial", "descriptive; wide CIs"),
        ("per-error-type sensitivity", "iter2 exp5 p_tests (P1); PERTURB suite counts tables/perturb_counts.csv", "partial", "real-error cells thin; PERTURB scoring owned by T5"),
        ("invariance under meaning-preserving rewrites", "iter2 exp5 analysis e_P4 (fused RENAME FA 0.385; c_score_align 0.859)", "answered", "fails for aligner consensus; NF variant passes"),
        ("coverage (unparseable counted)", "iter2 exp5 coverage_status (1,086 UNPARSEABLE of 8,507); this artifact population exclusions", "answered", ""),
        ("cost", "this artifact tables/m4_auroc_k_cost.csv ($ and CPU-s per sentence at each k)", "answered", "generation cost of the peer pool from the dataset-E ledger"),
        ("complexity (length, quantifiers, depth, conditions, exceptions)", "this artifact e/d by words tercile, n_conditions bin, exception type; exp6 complexity_gee", "answered", "E only"),
        ("contamination", "tables/exp6_contamination_DiD.csv; corrections C1", "answered", "MDE 0.107-0.139"),
        ("gold-error rate", "tables/label_facts.csv (gold_error)", "answered", ""),
        ("correct-but-not-equivalent rate", "tables/label_facts.csv (CNE per stratum)", "answered", ""),
        ("baseline: parse/compile rate", "exp6 parse_fail AUROC 0.500", "answered", ""),
        ("baseline: round-trip", "exp6 rt_nli_* local (0.62-0.63)", "partial", "API round-trip = T1"),
        ("baseline: LLM-as-judge", "exp6 local judges; API judges", "partial", "API judge on E = T1"),
        ("baseline: sampling self-consistency", "exp6 sc5_local (0.664)", "partial", "API SC-5 = T1"),
        ("baseline: structural pilot metrics", "exp6 pilot_* (0.50-0.54; rerun_jacc 0.660)", "answered", "null"),
        ("adds signal beyond baselines", "tables/pt_vs_s4_rerun.csv (vs local S4 stack, pooled + stratified)", "partial", "API stack = T1"),
        ("reusable functions", "tables/function_inventory.csv (+ pairwise_matrix, ed_decomposition)", "answered", ""),
        ("dataset with labels", "dataset E (iter1 gen_art_dataset_1) + pairwise_classes_E.jsonl (label-free matrix)", "answered", ""),
        ("mechanism: why consensus works (errors scatter)", "this artifact: M1, M2, NET, SCATTER, M4", "answered", "E only; R_COMP rerun in iteration 4"),
        ("label bias estimate (adjudicator ceiling)", "tables/radj_gate.csv (Sonnet-5 0.662 on expert pairs)", "answered", "R_ADJ DROPPED")]
    df = pd.concat([old, pd.DataFrame([{"requirement": a, "where_answered": b, "status": c, "gap": d, "iteration": "2-3 (this artifact)"}
                                       for a, b, c, d in new])], ignore_index=True)
    write_csv(df, "coverage_vs_request.csv", [f"{EV1}/tables/coverage_vs_request.csv (iteration-1 rows, unchanged)", "iteration 2-3 rows: this artifact"])
    return df


def function_inventory() -> pd.DataFrame:
    files = [I1 / "experiment-1/src/src/fol_triage.py"] + sorted(Path(p) for p in glob.glob(str(I1 / "experiment-3/src/src/*.py")))
    files += [E5 / "src/vendor_c/consensus.py", E5 / "src/peer_text.py"]
    files += sorted(Path(p) for p in glob.glob(str(E6 / "src/*b2*.py")) + glob.glob(str(E6 / "src/*world*.py")))
    files += [ROOT / "src/pairwise.py", ROOT / "src/mechanism.py"]
    rows = []
    for f in dict.fromkeys(files):
        if not f.exists():
            continue
        src = f.read_text()
        sha = hashlib.sha256(src.encode()).hexdigest()
        tree = ast.parse(src)
        dead = "b2" in f.name or "world" in f.name
        for n in tree.body:
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and not n.name.startswith("_"):
                args = [a.arg for a in n.args.args]
                doc = ast.get_docstring(n) or ""
                if f.parent == ROOT / "src" and n.name not in ("pairwise_matrix", "ed_decomposition"):
                    continue
                rows.append({"file": str(f), "sha256": sha, "function": n.name, "signature": f"{n.name}({', '.join(args)})",
                             "has_docstring": bool(doc), "docstring_first_line": doc.strip().splitlines()[0][:160] if doc else "",
                             "input_contract_text_fol": bool({"text", "fol"} <= set(args)) or bool(set(args) & {"fol", "cand", "cand_s"}),
                             "status": "dead-end (B2 DROPPED)" if dead else ("NEW (this artifact)" if f.parent == ROOT / "src" else "live")})
    df = pd.DataFrame(rows)
    write_csv(df, "function_inventory.csv", ["ast parse (no import) of each listed file; sha256 of file bytes", f"{EV1}/tables/function_inventory.csv (iteration-1 starting point)"])
    return df


# =================================================================================================== (ix) PERTURB counts
def perturb_counts() -> dict:
    d = J(DS3 / "full_data_out.json")
    ps = [g for g in d["datasets"] if g["dataset"] == "perturb_suite"][0]["examples"]
    del d
    mut = [e for e in ps if e.get("metadata_operator") and e["output"] == "ERROR"]
    ctl = [e for e in ps if e not in mut]
    c1 = Counter((e["metadata_operator"], e.get("metadata_position_polarity")) for e in mut)
    rows = [{"kind": "mutant", "operator": o, "polarity": p, "n": n} for (o, p), n in sorted(c1.items(), key=lambda x: (x[0][0], str(x[0][1])))]
    c2 = Counter((e.get("metadata_operator") or json.loads(e["input"]).get("system", "")).split(":")[1] if ":" in json.loads(e["input"]).get("system", "") else e.get("metadata_operator") for e in ctl)
    rows += [{"kind": "control", "operator": o, "polarity": "", "n": n} for o, n in sorted(c2.items(), key=lambda x: str(x[0]))]
    pairs = {e["metadata_matched_pair_id"] for e in ps if e.get("metadata_matched_pair_complete") and e.get("metadata_matched_pair_id")}
    card = (DS3 / "dataset_card.md").read_text()
    tot = {"mutants": len(mut), "controls": len(ctl), "complete_matched_pairs": len(pairs)}
    exp = {"mutants": 4234, "controls": 868, "complete_matched_pairs": 1354}
    tot["reproduces_card"] = {k: tot[k] == v for k, v in exp.items()}
    tot["card_mentions"] = {k: str(v) in card or f"{v:,}" in card for k, v in exp.items()}
    rows.append({"kind": "TOTAL", "operator": "mutants", "polarity": "", "n": len(mut)})
    rows.append({"kind": "TOTAL", "operator": "controls", "polarity": "", "n": len(ctl)})
    rows.append({"kind": "TOTAL", "operator": "complete_matched_pairs", "polarity": "", "n": len(pairs)})
    df = pd.DataFrame(rows)
    df["caveat"] = "synthetic; never pooled with real-error AUROC; QUANT/REV/RESTR UP-only; SCOPE/UNGLUE 0 rows"
    write_csv(df, "perturb_counts.csv", [f"{DS3}/full_data_out.json :: datasets[perturb_suite].examples (metadata_operator, metadata_position_polarity, metadata_matched_pair_id/complete)",
                                         f"{DS3}/dataset_card.md :: totals 4,234 / 868 / 1,354"])
    return tot


# =================================================================================================== (x) label facts
def label_facts(df_frame: pd.DataFrame, radj: pd.DataFrame) -> pd.DataFrame:
    a6 = J(E6 / "results" / "analysis_E.json")
    rows = []
    ab = df_frame[df_frame.y_AB.notna()]
    for st in ("L25", "L20", "EXC", "CTRL"):
        c = ab[(ab.stratum == st) & (ab.y_AB == 0)]
        v = float(c.correct_not_equivalent.mean())
        x = get(a6, f"label_quality.correct_not_equivalent.{st}.share_correct_not_eq")
        rows.append({"fact": "correct_not_equivalent_share_R_AB", "cell": st, "value": round(v, 4), "n": len(c), "crosscheck_exp6": x,
                     "match": x != NIF and abs(v - x) < 5e-4, "source": f"{E5}/data/E_labels.jsonl :: correct_not_equivalent among R_AB CORRECT rows"})
    ge = get(a6, "label_quality.gold_error")
    for k, v in ge.items():
        rows.append({"fact": "gold_error_rate_panel_judges_MALLS_gold_wrong", "cell": k, "value": v["rate"], "n": v["audited"],
                     "source": f"{E6}/results/analysis_E.json :: label_quality.gold_error.{k}.rate"})
    card = (DS_E / "dataset_card.md").read_text()
    m = re.search(r"\| majority \| (\d+) \| ([0-9.]+) \| ([0-9.]+) \| ([0-9.]+) \| ([0-9.]+) \|", card)
    if m:
        rows.append({"fact": "panel_majority_accuracy_real_errors", "cell": "track H unambiguous", "value": float(m.group(2)), "n": int(m.group(1)),
                     "source": f"{DS_E}/dataset_card.md :: Real-error accuracy table, majority row"})
        rows.append({"fact": "panel_majority_accepts_expert_corrected", "cell": "track H unambiguous", "value": float(m.group(4)), "n": int(m.group(1)),
                     "source": f"{DS_E}/dataset_card.md :: Real-error accuracy table, majority row (corrected accepted)"})
    d = J(DS_E / "full_data_out.json")
    hs = [g for g in d["datasets"] if g["dataset"] == "heldout_sentences"][0]["examples"]
    del d
    for k, n in Counter(e["output"] for e in hs).most_common():
        rows.append({"fact": "reference_status_count", "cell": k, "value": n, "n": len(hs), "source": f"{DS_E}/full_data_out.json :: datasets[heldout_sentences].examples[].output"})
    rt = J(E6 / "results" / "retest_vs_sibling.json")
    rows.append({"fact": "local_judge_test_retest_spearman", "cell": "disg", "value": get(rt, "disg.spearman"), "n": None,
                 "source": f"{E6}/results/retest_vs_sibling.json :: disg.spearman"})
    s = radj[(radj.adjudicator == "sonnet-5") & (radj.half == "gate") & (radj.subset == "H")]
    rows.append({"fact": "adjudicator_vs_expert_ceiling", "cell": "Sonnet-5 gate track-H balanced accuracy",
                 "value": float(s.balanced_accuracy.iloc[0]) if len(s) else NIF, "n": int(s.n.iloc[0]) if len(s) else None,
                 "source": f"{DS2}/gate_report.json :: primary.gate.H.balanced_accuracy"})
    df = pd.DataFrame(rows)
    write_csv(df, "label_facts.csv", ["each row's own source column"])
    return df
