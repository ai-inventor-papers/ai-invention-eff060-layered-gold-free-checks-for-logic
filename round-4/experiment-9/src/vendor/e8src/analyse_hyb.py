#!/usr/bin/env python3
"""STEP 4 PART A ANALYSIS (refuses to run unless results/prereg_hyb.json is frozen and unmodified).

  A1 screen: FA-0.10 thresholds (AGREE-set track-L CORRECT, fractional ties) for c/g x {align, nf, hyb}; screen AUROCs;
     regression check c_align track-L AUROC vs exp C 0.866.
  A2 rename FA on the three pre-registered sources + the full invariance table for the consensus variants.
  A3 over-alignment: PERTURB MEANING_RENAME / SWAP and screen probes recall at the frozen screen thresholds.
  A4 SELECTION (prereg rule, verbatim) -> results/selection.json
  A5 E R_AB / R_A AUROC tables + paired stratified deltas (sentence-cluster bootstrap), coverage view, placebo.
  A6 new-agreement audit on real E pairs (label discordance), 30-pair by-hand sample.
  A7 complexity (word bins, n_conditions) for ALIGN / NF / HYB.
Outputs: results/analysis_hyb.json, results/selection.json, results/invariance_table_consensus.csv,
         results/per_item_hyb_E.jsonl, results/per_item_screen_hyb.jsonl, results/tables/hyb_*.md
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from loguru import logger

sys.path.insert(0, str(Path(__file__).resolve().parent))
import an_common as C  # noqa: E402
import stats as ST  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(C.ROOT / "logs" / "analyse_hyb.log", rotation="30 MB", level="DEBUG")

CONS = ["c_align", "c_nf", "c_hyb", "g_align", "g_nf", "g_hyb"]
VARIANT_SCORE = {"HYB": "c_hyb", "NF-anchored": "c_nf", "ALIGN": "c_align"}


def solver_label(auto):
    return {"CORRECT": "CORRECT", "EQ": "CORRECT", "VOCAB_GRAN": "CORRECT", "ERROR": "ERROR", "COMPOUND": "ERROR"}.get(auto or "")


def adj_label(v):
    if v["label_tier"] in ("A", "B") and v["final_label"] in ("CORRECT", "ERROR") and not v.get("reading_choice"):
        return v["final_label"]
    return None


def sc(r: dict | None, m: str) -> float:
    """screen/PERTURB score with exp 5's screen convention: unparseable or missing -> 1.0 (most suspicious)."""
    if r is None or r.get("coverage_status") != "OK":
        return 1.0
    v = r.get(m)
    return 1.0 if v is None else float(v)


# =============================================================================================== A1 screen
def screen_part(A: dict) -> tuple[dict, dict, dict]:
    labs = json.loads((C.DATA / "screen" / "screen_adjudicated_labels.json").read_text())
    rows = C.load_scores("screen")
    agree = []
    for iid, v in labs.items():
        if iid not in rows or v["track"] not in ("L", "H"):
            continue
        sl, al = solver_label(v["auto_label"]), adj_label(v)
        if sl is not None and al is not None and sl == al:
            agree.append((iid, al, v["track"]))
    Lcor = [i for i, l, t in agree if l == "CORRECT" and t == "L"]
    thr = {m: ST.matched_fa([sc(rows[i], m) for i in Lcor], 0.10) for m in CONS}
    tie = {m: ST.tie_share_at([sc(rows[i], m) for i in Lcor], thr[m][0]) for m in CONS}
    y = np.array([1 if l == "ERROR" else 0 for _, l, _ in agree])
    trk = np.array([t for _, _, t in agree])
    aur = {}
    for m in CONS:
        s = np.array([sc(rows[i], m) for i, _, _ in agree])
        aur[m] = {"agree_all": ST.auc_fast(y, s), "agree_trackL": ST.auc_fast(y[trk == "L"], s[trk == "L"]),
                  "agree_trackH": ST.auc_fast(y[trk == "H"], s[trk == "H"])}
    # regression (b): exp C track-L AUROC of c_score_align = 0.866 (solver labels on track L)
    trL = [(i, solver_label(v["auto_label"])) for i, v in labs.items() if v["track"] == "L" and i in rows and solver_label(v["auto_label"])]
    yl = np.array([1 if l == "ERROR" else 0 for _, l in trL])
    reg = {"trackL_solver_labels": {"n": len(trL), "auroc_c_align": ST.auc_fast(yl, [sc(rows[i], "c_align") for i, _ in trL])},
           "trackL_agree": aur["c_align"]["agree_trackL"], "expC_reference": 0.866}
    reg["reproduces_0.866_pm_0.005"] = any(abs(x - 0.866) <= 0.005 for x in (reg["trackL_solver_labels"]["auroc_c_align"], reg["trackL_agree"]))
    A["screen"] = {"agree_counts": dict(Counter((t, l) for _, l, t in agree).items().__iter__()) if False else
                   {f"{t}:{l}": n for (t, l), n in Counter((t, l) for _, l, t in agree).items()},
                   "n_trackL_correct": len(Lcor), "thresholds": {m: {"t": thr[m][0], "lambda": thr[m][1], "tie_share_at_t": tie[m],
                                                                     "degenerate": tie[m] > 0.5} for m in CONS},
                   "auroc": aur, "regression_b": reg}
    # per-item screen output
    with (C.RES / "per_item_screen_hyb.jsonl").open("w") as fh:
        for k, r in rows.items():
            fh.write(json.dumps({"key": k, "sentence_id": r["sentence_id"], "coverage_status": r.get("coverage_status"),
                                 **{m: r.get(m) for m in CONS + ["c_nf_pairs", "n_peers", "n_unknown_hyb"]},
                                 "label": (adj_label(labs[k]) if k in labs else None)}) + "\n")
    logger.info(f"screen thresholds: { {m: (round(thr[m][0], 4), round(thr[m][1], 3)) for m in CONS} }")
    return thr, rows, labs


# =============================================================================================== A2/A3 rewrites + probes
def perturb_rows() -> list[dict]:
    return C.jl(C.DATA / "perturb_rows.jsonl")


def invariance(A: dict, thr: dict, srows: dict, labs: dict, erows: dict) -> list[dict]:
    inv = json.loads((C.DATA / "invariance_items.json").read_text())
    table = []

    def add(metric, family, source, pairs, clusters, base_endorsed=None):
        """pairs: [(rw_score, base_score)] of CORRECT bases."""
        if not pairs:
            table.append({"metric": metric, "family": family, "source": source, "n_rewrites": 0})
            return
        f_rw = ST.flag_vec([p[0] for p in pairs], *thr[metric])
        f_b = ST.flag_vec([p[1] for p in pairs], *thr[metric])
        flip = np.abs(f_rw - f_b)  # coupled tie draw: identical scores never flip
        fa, fci = ST.cluster_boot_mean(f_rw, clusters)
        fl, flci = ST.cluster_boot_mean(flip, clusters)
        table.append({"metric": metric, "family": family, "source": source, "n_rewrites": len(pairs),
                      "n_bases": len(set(clusters)), "FA_on_correct_bases": fa, "FA_ci_lo": fci[0], "FA_ci_hi": fci[1],
                      "base_FA": float(f_b.mean()), "flip_rate": fl, "flip_ci_lo": flci[0], "flip_ci_hi": flci[1],
                      "n_flipped_expected": float(flip.sum()), "subset": base_endorsed or "all"})
    # (i) exp D rewrites of screen CORRECT bases (exp 5 rule: adjudicated final_label CORRECT)
    fams = sorted({x["family"] for x in inv})
    for m in CONS:
        for fam in fams:
            pr, cl = [], []
            for x in inv:
                if x["family"] != fam:
                    continue
                k = "RW:" + x["rw_id"]
                b = x["base_item_id"]
                if k not in srows or labs.get(b, {}).get("final_label") != "CORRECT":
                    continue
                pr.append((sc(srows[k], m), sc(srows.get(b), m)))
                cl.append(b)
            add(m, fam, "expD_screen", pr, cl)
    # (ii)/(iii) + other PERTURB controls on E-base pools (CORRECT by construction); base row = PB:<base>
    P = [r for r in perturb_rows() if r["fold"] == "PERTURB_CONTROL" and not r["base_source"].startswith("R_COMP")]
    ctypes = sorted({r["control_type"] for r in P})
    na = Counter()
    for m in CONS:
        for ct in ctypes:
            for sub in ("all", "endorsed"):
                pr, cl = [], []
                for r in P:
                    if r["control_type"] != ct:
                        continue
                    k, bk = "PT:" + r["item_id"], "PB:" + r["base_item_id"]
                    rw, bs = erows.get(k), erows.get(bk)
                    if rw is None or bs is None or rw.get("c_hyb") is None or bs.get("c_hyb") is None:
                        na[(ct, "no_peers_or_missing")] += (m == CONS[0] and sub == "all")
                        continue
                    if sub == "endorsed" and not (bs["c_hyb"] < 1.0):
                        continue
                    pr.append((sc(rw, m), sc(bs, m)))
                    cl.append(r["base_item_id"])
                add(m, ct, "PERTURB_E_bases", pr, cl, sub)
    A["invariance_na"] = {f"{k[0]}|{k[1]}": v for k, v in na.items()}
    with (C.RES / "invariance_table_consensus.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["metric", "family", "source", "subset", "n_rewrites", "n_bases", "FA_on_correct_bases",
                                           "FA_ci_lo", "FA_ci_hi", "base_FA", "flip_rate", "flip_ci_lo", "flip_ci_hi", "n_flipped_expected"])
        w.writeheader()
        for t in table:
            w.writerow({k: t.get(k) for k in w.fieldnames})
    return table


def over_alignment(A: dict, thr: dict, srows: dict, erows: dict) -> dict:
    out = {}
    probes = json.loads((C.DATA / "exp5" / "screen_probes.json").read_text())
    for m in CONS:
        o = {}
        for pname in ("MEANING_RENAME", "ROLE_PERMUTE", "SWAP"):
            ks = [f"PR:{p['probe']}:{p['base_item_id']}" for p in probes if p["probe"] == pname]
            ks = [k for k in ks if k in srows]
            v = [sc(srows[k], m) for k in ks]
            rec, ci = ST.cluster_boot_mean(ST.flag_vec(v, *thr[m]), [k.split(":")[-1] for k in ks]) if v else (None, [None, None])
            o[f"screen_probe_{pname}"] = {"n": len(v), "recall": rec, "ci": ci}
        P = [r for r in perturb_rows() if r["fold"] == "PERTURB" and not r["base_source"].startswith("R_COMP")]
        for op, pol in (("MEANING_RENAME", "DOWN"), ("MEANING_RENAME", "UP"), ("SWAP", "DOWN"), ("SWAP", "UP"),
                        ("MEANING_RENAME", None), ("SWAP", None)):
            rs = [r for r in P if r["operator"] == op and (pol is None or r["polarity"] == pol)
                  and erows.get("PT:" + r["item_id"], {}).get("c_hyb") is not None]
            v = [sc(erows["PT:" + r["item_id"]], m) for r in rs]
            rec, ci = ST.cluster_boot_mean(ST.flag_vec(v, *thr[m]), [r["base_item_id"] for r in rs]) if v else (None, [None, None])
            # endorsed-base restriction (consensus can only detect mutants of endorsed bases)
            rs2 = [r for r in rs if erows.get("PB:" + r["base_item_id"], {}).get("c_hyb", 1.0) < 1.0]
            v2 = [sc(erows["PT:" + r["item_id"]], m) for r in rs2]
            rec2, ci2 = ST.cluster_boot_mean(ST.flag_vec(v2, *thr[m]), [r["base_item_id"] for r in rs2]) if v2 else (None, [None, None])
            o[f"perturb_{op}_{pol or 'ALL'}"] = {"n": len(v), "recall": rec, "ci": ci, "n_endorsed": len(v2),
                                                 "recall_endorsed": rec2, "ci_endorsed": ci2}
        out[m] = o
    A["over_alignment"] = out
    return out


# =============================================================================================== A4 selection
def select(A: dict, table: list[dict]) -> dict:
    def fa(metric, family, source, subset="all"):
        for t in table:
            if t["metric"] == metric and t["family"] == family and t["source"] == source and t.get("subset", "all") == subset:
                return t.get("FA_on_correct_bases")
        return None
    ev = {}
    for v in ("HYB", "NF-anchored"):
        m = VARIANT_SCORE[v]
        f = {"i_expD_RENAME": fa(m, "RENAME", "expD_screen"), "ii_PERTURB_RENAME_SYN": fa(m, "RENAME_SYN", "PERTURB_E_bases"),
             "iii_PERTURB_RENAME_NONCE": fa(m, "RENAME_NONCE", "PERTURB_E_bases")}
        f_end = {"ii_endorsed": fa(m, "RENAME_SYN", "PERTURB_E_bases", "endorsed"),
                 "iii_endorsed": fa(m, "RENAME_NONCE", "PERTURB_E_bases", "endorsed")}
        elig = all(x is not None and x <= 0.10 for x in f.values())
        ev[v] = {"score": m, "rename_FA": f, "rename_FA_endorsed_bases_secondary": f_end, "eligible": elig,
                 "failing_sources": [k for k, x in f.items() if x is None or x > 0.10]}
    return ev


# =============================================================================================== A5 E tables
def E_part(A: dict) -> list[dict]:
    rows = C.load_E()
    # sanity: c_hyb <= min(c_align_re, c_nf_pairs) on scored rows (by construction)
    viol = [r["row_key"] for r in rows if not r["unparseable"] and not r.get("c_hyb__imputed")
            and r["c_hyb"] > min(r["c_align_re"], r["c_nf_pairs"]) + 1e-12]
    A["assert_c_hyb_le_min"] = {"violations": len(viol), "examples": viol[:5]}
    assert not viol, f"c_hyb > min(c_align, c_nf_pairs) on {len(viol)} rows"
    METRICS = ["c_hyb", "c_align", "c_nf", "g_hyb", "g_align", "g_nf", "c_align_re", "c_nf_pairs", "p_peer_text"]
    PAIRS = [("c_hyb", "c_align"), ("c_hyb", "c_nf"), ("c_hyb", "c_align_re"), ("g_hyb", "g_align"), ("g_hyb", "g_nf"),
             ("c_nf", "c_align"), ("c_hyb", "p_peer_text")]
    SUB = {"R_AB pooled": ("y_AB", None), "R_AB L25": ("y_AB", ("L25",)), "R_AB L20": ("y_AB", ("L20",)),
           "R_AB EXC": ("y_AB", ("EXC",)), "R_AB CTRL": ("y_AB", ("CTRL",)), "R_AB long (L25+L20+EXC)": ("y_AB", ("L25", "L20", "EXC")),
           "R_A pooled L20+EXC": ("y_A", ("L20", "EXC")), "R_A all strata (sign only)": ("y_A", None)}
    A["E"] = {}
    for name, (yk, st) in SUB.items():
        rs = [dict(r, y=r[yk]) for r in rows if r[yk] is not None and (st is None or r["stratum"] in st)]
        ev = C.evaluate(rs, METRICS, pairs=PAIRS)
        for j in ("judge_local_qwen8b_disg", "judge_cheap_disg"):
            rj = [r for r in rs if C.nz(r.get(j))]
            if len(rj) >= 20 and 0 < sum(r["y"] for r in rj) < len(rj):
                ev[f"vs_{j}"] = C.evaluate(rj, ["c_hyb", "c_nf", "c_align", j],
                                           pairs=[("c_hyb", j), ("c_nf", j), ("c_align", j)])
            else:
                ev[f"vs_{j}"] = {"n": len(rj), "untestable": True}
        # coverage view (unparseable rows = ERROR predictions are already 1.0) vs parseable-only view
        rp = [r for r in rs if not r["unparseable"]]
        ev["parseable_only"] = C.evaluate(rp, ["c_hyb", "c_align", "c_nf"], pairs=[("c_hyb", "c_align"), ("c_hyb", "c_nf")], b=500)
        ev["n_unparseable"] = len(rs) - len(rp)
        A["E"][name] = ev
        mm = ev.get("metrics", {})
        logger.info(f"E {name}: n={ev['n']} err={ev['n_error']} | strat AUROC hyb {C.fmt(mm.get('c_hyb', {}).get('strat_auroc'))} "
                    f"align {C.fmt(mm.get('c_align', {}).get('strat_auroc'))} nf {C.fmt(mm.get('c_nf', {}).get('strat_auroc'))}")
    # placebo: labels shuffled within stratum (seed 0)
    rs = [dict(r, y=r["y_AB"]) for r in rows if r["y_AB"] is not None]
    rng = np.random.default_rng(0)
    ys = np.array([r["y"] for r in rs])
    st = np.array([r["stratum"] for r in rs])
    for s in set(st.tolist()):
        m = st == s
        ys[m] = rng.permutation(ys[m])
    A["placebo_shuffled_within_stratum"] = {m: ST.strat_auc(ys, [r[m] for r in rs], st) for m in ("c_hyb", "c_align", "c_nf")}
    # peer / unknown diagnostics
    A["E_diag"] = {"n_rows": len(rows), "n_imputed_c_hyb": sum(bool(r.get("c_hyb__imputed")) for r in rows),
                   "n_unparseable": sum(r["unparseable"] for r in rows),
                   "rows_with_unknown_hyb_pairs": sum((r.get("n_unknown_hyb") or 0) > 0 for r in rows),
                   "mean_n_peers_llm": float(np.mean([r["n_peers"] for r in rows if r["n_peers"] is not None and r["system_class"] == "llm"]))}
    return rows


# =============================================================================================== A6 new-agreement audit
def audit(A: dict, rows: list[dict]):
    lab = {r["row_key"]: r for r in rows}
    fols = {r["row_key"]: r["candidate_fol"] for r in C.jl(C.DATA / "exp5" / "E_blind.jsonl")}
    texts = {r["row_key"]: r["text"] for r in C.jl(C.DATA / "exp5" / "E_blind.jsonl")}
    cnt = Counter()
    disc = defaultdict(lambda: [0, 0])  # group -> [discordant, both-labelled]
    cand_err = defaultdict(lambda: [0, 0])
    new_pairs = []
    seen = set()
    with (C.RES / "pairs_E.jsonl").open() as fh:
        for l in fh:
            p = json.loads(l)
            a, b = p["cand"], p["peer"]
            if a not in lab or b not in lab:
                continue
            key = tuple(sorted((a, b)))
            if key in seen:  # count each unordered pair once per ordered direction class -> keep ordered? use unordered
                continue
            seen.add(key)
            g = ("NEW_hyb_not_align" if (p["hyb_eq"] is True and p["align_eq"] is not True) else
                 "ALIGN_agree" if p["align_eq"] is True else
                 "NF_only_agree" if p["nf_eq"] is True else "DISAGREE_hyb_false" if p["hyb_eq"] is False else "UNKNOWN")
            cnt[g] += 1
            ya, yb = lab[a]["y_AB"], lab[b]["y_AB"]
            if ya is not None and yb is not None:
                disc[g][1] += 1
                disc[g][0] += int(ya != yb)
            if ya is not None:
                cand_err[g][1] += 1
                cand_err[g][0] += int(ya == 1)
            if g == "NEW_hyb_not_align":
                new_pairs.append((hashlib.sha1(f"{a}|{b}".encode()).hexdigest(), a, b, p.get("nf_cost")))
    res = {"n_unordered_pairs": dict(cnt),
           "label_discordance": {g: {"discordant": d, "both_labelled": n, "rate": d / n if n else None} for g, (d, n) in disc.items()},
           "candidate_error_share": {g: {"error": d, "labelled": n, "rate": d / n if n else None} for g, (d, n) in cand_err.items()}}
    # bootstrap CI (clustered by sentence) of discordance difference NEW - ALIGN
    new_pairs.sort()
    sample = []
    for h, a, b, cost in new_pairs[:30]:
        sample.append({"sentence_text": texts.get(a), "cand_row": a, "cand_fol": fols.get(a), "cand_label": lab[a]["final_label"],
                       "peer_row": b, "peer_fol": fols.get(b), "peer_label": lab[b]["final_label"], "nf_cost": cost})
    res["sample_30_sha1_ordered"] = sample
    A["new_agreement_audit"] = res
    logger.info(f"audit: {json.dumps({k: v for k, v in res.items() if k != 'sample_30_sha1_ordered'})[:600]}")


# =============================================================================================== A7 complexity
def complexity(A: dict, rows: list[dict]):
    rs = [dict(r, y=r["y_AB"]) for r in rows if r["y_AB"] is not None]

    def wbin(r):
        w = r["strata"].get("words") or 0
        return "<12" if w < 12 else "12-19" if w < 20 else "20-24" if w < 25 else "25-29" if w < 30 else "30+"

    def cbin(r):
        c = r["strata"].get("n_conditions") or 0
        return "0-1" if c <= 1 else "2" if c == 2 else "3" if c == 3 else "4+"

    def qbin(r):
        q = r["strata"].get("n_quant") or 0
        return "0-1" if q <= 1 else "2" if q == 2 else "3+"

    def dbin(r):
        d = r["strata"].get("depth") or 0
        return "<=2" if d <= 2 else "3" if d == 3 else "4+"

    out = {}
    for name, fn in (("words", wbin), ("n_conditions", cbin), ("n_quant", qbin), ("depth", dbin),
                     ("exception", lambda r: "exception" if r["strata"].get("exception_type") else "none")):
        g = C.group(rs, fn)
        out[name] = {}
        for k in sorted(g):
            ev = C.evaluate(g[k], ["c_hyb", "c_align", "c_nf"], pairs=[("c_hyb", "c_align"), ("c_hyb", "c_nf")], b=500)
            out[name][k] = {"n": ev["n"], "n_error": ev["n_error"], "testable": ev.get("testable", False),
                            **{m: ev["metrics"].get(m, {}).get("auroc") for m in ("c_hyb", "c_align", "c_nf")},
                            "hyb_minus_align": ev["paired"].get("c_hyb - c_align", {}).get("delta_auroc"),
                            "hyb_minus_align_ci": ev["paired"].get("c_hyb - c_align", {}).get("ci")}
    A["complexity"] = out


# =============================================================================================== main
@logger.catch(reraise=True)
def main():
    pre = C.guard()
    A = {"prereg_sha256": C.sha256_file(C.RES / "prereg_hyb.json"), "prereg_timestamp": pre["timestamp_utc"]}
    thr, srows, labs = screen_part(A)
    erows = C.load_scores("E")
    table = invariance(A, thr, srows, labs, erows)
    over_alignment(A, thr, srows, erows)
    ev = select(A, table)
    rows = E_part(A)
    # selection rule (verbatim prereg)
    elig = [v for v in ("HYB", "NF-anchored") if ev[v]["eligible"]]
    sauc = {v: A["E"]["R_AB pooled"]["metrics"][VARIANT_SCORE[v]]["strat_auroc"] for v in ("HYB", "NF-anchored", "ALIGN")}
    if not elig:
        chosen, note = None, "NEITHER ELIGIBLE: no rename-invariant consensus exists here; both reported as failed; the R_COMP read uses ALIGN."
    elif len(elig) == 2 and abs(sauc["HYB"] - sauc["NF-anchored"]) < 0.005:
        chosen, note = "NF-anchored", "both eligible, tie (|diff| < 0.005) -> NF-anchored"
    else:
        chosen = max(elig, key=lambda v: sauc[v])
        note = f"eligible {elig}; higher E stratified AUROC (R_AB) -> {chosen}"
    sel = {"prereg_sha256": A["prereg_sha256"], "rule": pre["selection_rule_verbatim"], "evidence": ev,
           "E_strat_auroc_R_AB": sauc, "frozen_variant": chosen, "frozen_score": VARIANT_SCORE.get(chosen) if chosen else None,
           "note": note, "screen_thresholds": A["screen"]["thresholds"],
           "R_COMP_read_uses": chosen if chosen else "ALIGN (c_align)",
           "caveat": "E is DEVELOPMENT data for this choice (2 candidates): the E AUROC of the frozen variant is optimistically selected; the held-out read is the sibling's R_COMP run."}
    (C.RES / "selection.json").write_text(json.dumps(sel, indent=1))
    A["selection"] = sel
    logger.info(f"SELECTION: {note}; evidence {json.dumps(ev)}")
    audit(A, rows)
    complexity(A, rows)
    # per-item E output
    with (C.RES / "per_item_hyb_E.jsonl").open("w") as fh:
        for r in rows:
            fh.write(json.dumps({k: r.get(k) for k in ("row_key", "sentence_id", "stratum", "system", "system_class", "fold_E",
                                                       "coverage_status", "n_peers", "n_unknown_hyb", "c_hyb", "g_hyb", "c_align",
                                                       "c_nf", "g_align", "g_nf", "c_align_re", "c_nf_re", "c_nf_pairs",
                                                       "final_label", "label_tier", "y_AB", "y_A")}) + "\n")
    (C.RES / "analysis_hyb.json").write_text(json.dumps(A, indent=1, default=str))
    logger.info("analysis_hyb done")


if __name__ == "__main__":
    main()
