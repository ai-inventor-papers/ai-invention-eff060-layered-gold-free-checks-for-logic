#!/usr/bin/env python3
"""STEP 5 PART B ANALYSIS: per-error-type sensitivity of EVERY available metric on the synthetic PERTURB suite.
Refuses to run unless prereg_hyb AND prereg_perturb are frozen and unmodified. PERTURB is never pooled with real-error AUROC.

Rows: 4,234 mutants (y=1) + 868 controls (y=0) + 300 unmutated bases (y=0, control type BASE); base = cluster unit.
Metrics (higher = more likely ERROR): see METRICS; thresholds = prereg_perturb PRIMARY (E R_AB CORRECT, FA 0.10, fractional
ties) + GPU thresholds by the frozen rule on nf4 EC CORRECT rows (results/thresholds_gpu.json, written here BEFORE any
PERTURB statistic) + SECONDARY FA 0.10 on PERTURB non-rename controls + BASE (in-sample).
Outputs: results/perturb_scores.jsonl, perturb_sensitivity.csv, perturb_downup.csv, perturb_basematched_auroc.csv,
         perturb_breakdowns.csv, coverage_perturb.csv, invariance_table.csv, tradeoff.csv, analysis_perturb.json
"""
from __future__ import annotations

import csv
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from loguru import logger

sys.path.insert(0, str(Path(__file__).resolve().parent))
import an_common as C  # noqa: E402
import fit_s4_perturb as S4  # noqa: E402
import stats as ST  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(C.ROOT / "logs" / "analyse_perturb.log", rotation="30 MB", level="DEBUG")

PS = C.RES / "perturb_scores"
CONS = ["c_align", "c_nf", "c_hyb", "g_align", "g_nf", "g_hyb"]
CPU = ["parse_fail", "pilot_joint_conflict", "pilot_arity_incons", "pilot_shape_incons", "pilot_dangling", "l2_bow", "l3_z3",
       "p_peer_text", "p_text", "sc5_local_eq_frac", "sc5_local_entropy"]
GPU = ["judge_local_qwen8b_disg", "judge_local_llama8b_disg", "rt_nli_min_local", "rt_nli_fwd_local", "rt_nli_bwd_local",
       "rt_nli_contra_local", "rt_nli_min_alt_local", "rt_embed_cos_local"]
API = ["judge_cheap_disg"]
REFERENCE_ONLY = {"parse_fail", "pilot_joint_conflict", "pilot_arity_incons", "pilot_shape_incons", "pilot_dangling"}
NONRENAME_CTRL = {"CONTRAPOSITIVE", "REORDER_COMMUTE", "REORDER_QUANT", "DEMORGAN", "BASE"}
OPS = ["NEG", "REV", "QUANT", "RESTR", "CONN", "MOVE", "DROP", "ADD", "SWAP", "BIND", "MEANING_RENAME", "SCOPE", "UNGLUE"]


def jl(p):
    return C.jl(p)


# =============================================================================================== assembly
def load_rows() -> list[dict]:
    R = jl(C.DATA / "perturb_rows.jsonl")
    U, seen = [], {}
    for r in R:
        is_ctrl = r["fold"] == "PERTURB_CONTROL"
        U.append({"key": "PT:" + r["item_id"], "item_id": r["item_id"], "base": r["base_item_id"], "sentence_id": r["sentence_id"],
                  "y": 0 if is_ctrl else 1, "operator": None if is_ctrl else r["operator"], "op_fine": r["op_fine"],
                  "control_type": r["control_type"] if is_ctrl else None, "polarity": r["polarity"],
                  "matched_pair_id": r["matched_pair_id"], "pair_complete": r["matched_pair_complete"], "subtype": r["subtype"],
                  "base_status": "R_COMP" if r["base_source"] == "RCOMP" else r["base_source"].replace("E_", ""),
                  "is_rcomp": r["base_source"] == "RCOMP", "strata": r["strata"], "text": r["text"], "fol": r["candidate_fol"],
                  "reference_fol": r["reference_fol"], "disguised_text": r["disguised_text"], "disguised_fol": r["disguised_fol"]})
        if r["base_item_id"] not in seen:
            seen[r["base_item_id"]] = 1
            U.append({"key": "PB:" + r["base_item_id"], "item_id": r["base_item_id"], "base": r["base_item_id"],
                      "sentence_id": r["sentence_id"], "y": 0, "operator": None, "op_fine": None, "control_type": "BASE",
                      "polarity": None, "matched_pair_id": None, "pair_complete": None, "subtype": None,
                      "base_status": "R_COMP" if r["base_source"] == "RCOMP" else r["base_source"].replace("E_", ""),
                      "is_rcomp": r["base_source"] == "RCOMP", "strata": r["strata"], "text": r["text"], "fol": r["reference_fol"],
                      "reference_fol": r["reference_fol"], "disguised_text": r["disguised_text"],
                      "disguised_fol": r["disguised_reference_fol"]})
    return U


def attach_scores(U: list[dict]) -> dict:
    """Adds every metric column (None = not scorable) + '<m>__status' in {ok, fail(->fill), na:<reason>}."""
    cons = C.load_scores("E")
    cpu = {r["key"]: r for r in jl(PS / "cpu.jsonl")}
    jq = {r["key"].rsplit("|", 1)[0]: r for r in jl(PS / "judge_local_qwen8b_nf4.jsonl") if r["key"].endswith("|disg")}
    jll = {r["key"].rsplit("|", 1)[0]: r for r in jl(PS / "judge_local_llama8b_nf4.jsonl") if r["key"].endswith("|disg")}
    nli = {r["key"]: r for r in jl(PS / "rt_nli_local_nf4.jsonl")}
    verb = {r["key"]: r for r in jl(PS / "rt_verbal_local_nf4.jsonl")}
    jc = {r["key"]: r for r in jl(PS / "judge_cheap_disg.jsonl")}
    s4 = json.loads((C.RES / "s4_perturb_coefs.json").read_text())
    avail = {"judge_local_qwen8b_disg": len(jq) >= len(U), "judge_local_llama8b_disg": len(jll) >= len(U),
             "rt": len(nli) >= 0.95 * len(U), "judge_cheap_disg": bool(jc)}

    def put(u, m, v, st):
        u[m] = None if v is None or (isinstance(v, float) and math.isnan(v)) else float(v)
        u[m + "__status"] = st
    for u in U:
        k = u["key"]
        c = cpu.get(k, {})
        unp = bool(c.get("parse_fail", 0))
        u["unparseable"] = unp
        # consensus
        o = cons.get(k)
        for m in CONS:
            if unp:
                put(u, m, 1.0, "fail")
            elif u["is_rcomp"]:
                put(u, m, None, "na:no_peers_yet(R_COMP)")
            elif o is None or o.get(m) is None:
                put(u, m, None, "na:peer_unavailable")
            else:
                put(u, m, o[m], "ok")
        # cpu
        put(u, "parse_fail", float(unp), "ok")
        for m in ("pilot_joint_conflict", "pilot_arity_incons", "pilot_shape_incons", "pilot_dangling"):
            if unp:
                put(u, m, S4_FILL.get(m, 1.0), "fail")
            elif c.get(m) is None:
                put(u, m, S4_FILL.get(m, 1.0), "fail") if m == "pilot_joint_conflict" else put(u, m, None, "na")
            else:
                put(u, m, c[m], "ok")
        for m in ("l2_bow", "p_peer_text", "p_text"):
            put(u, m, 1.0 if unp else c.get(m), "fail" if unp else ("ok" if c.get(m) is not None else "na:error"))
        if unp:
            put(u, "l3_z3", 1.0, "fail")
        elif c.get("l3_z3") is None:
            put(u, "l3_z3", None, "na:no_cached_questionnaire(R_COMP)" if u["is_rcomp"] else f"na:{c.get('l3_status')}")
        else:
            put(u, "l3_z3", c["l3_z3"], "ok")
        for m in ("sc5_local_eq_frac", "sc5_local_entropy"):
            if unp:
                put(u, m, S4_FILL.get(m, 1.0), "fail")
            elif c.get(m) is None:
                put(u, m, None, "na:no_sc_samples(R_COMP)" if u["is_rcomp"] else "na")
            else:
                put(u, m, c[m], "ok")
        # GPU judges (1 - p), round trip (1 - entail / 1 - cos; contra as is)
        for m, src in (("judge_local_qwen8b_disg", jq), ("judge_local_llama8b_disg", jll)):
            r = src.get(k)
            if not avail[m]:
                put(u, m, None, "na:not_run")
            elif r is None:
                put(u, m, None, "na:missing")
            elif r.get("p") is None:
                put(u, m, 1.0, "fail")
            else:
                put(u, m, 1.0 - r["p"], "ok")
        r = nli.get(k)
        for m in ("rt_nli_min_local", "rt_nli_fwd_local", "rt_nli_bwd_local", "rt_nli_contra_local", "rt_nli_min_alt_local", "rt_embed_cos_local"):
            if not avail["rt"]:
                put(u, m, None, "na:not_run")
            elif r is None or r.get(m) is None:
                put(u, m, 1.0, "fail")  # no verbalisation (empty/leak) -> failure, exp 6 fail_fill
            else:
                put(u, m, r[m] if m == "rt_nli_contra_local" else 1.0 - r[m], "ok")
        r = jc.get(k)
        if r is None:
            put(u, "judge_cheap_disg", None, "na:missing")
        elif r.get("p") is None:
            put(u, "judge_cheap_disg", 1.0, "fail")
        else:
            put(u, "judge_cheap_disg", 1.0 - r["p"], "ok")
        u["judge_cheap_type"] = r.get("type") if r else None
        u["judge_local_qwen8b_type"] = (jq.get(k) or {}).get("type")
    # S4_local (needs every S4 input column present)
    n_units = len(U)
    S4_ok = (len(jq) >= n_units and len(jll) >= n_units and len(nli) >= 0.95 * n_units)
    if S4_ok:
        feats_rows = []
        for u in U:
            fr = {}
            for f in s4["features"]:
                st = u.get(f + "__status", "na")
                fr[f] = u.get(f)
                fr[f + "__status"] = "fail" if st == "fail" else ("ok" if st == "ok" else "na")
                if st.startswith("na"):
                    fr[f] = None
            feats_rows.append(fr)
        p = S4.apply(s4, feats_rows)
        for u, pp in zip(U, p):
            put(u, "S4_local", pp, "ok")
    else:
        for u in U:
            put(u, "S4_local", None, "na:inputs_not_run")
    return avail


S4_FILL = {}


# =============================================================================================== thresholds
def gpu_thresholds(pp: dict) -> dict:
    """Frozen rule on the nf4 EC CORRECT rows; written BEFORE any PERTURB statistic."""
    p = C.RES / "thresholds_gpu.json"
    cal = [c for c in jl(C.DATA / "E_calib_units.jsonl")]
    calC = sorted(c["key"] for c in cal if c["label"] == "CORRECT")
    import hashlib
    assert hashlib.sha256("\n".join(calC).encode()).hexdigest() == pp["thresholds_gpu_rule"]["ec_correct_keys_sha256"]
    jq = {r["key"].rsplit("|", 1)[0]: r for r in jl(PS / "judge_local_qwen8b_nf4.jsonl") if r["key"].endswith("|disg")}
    jll = {r["key"].rsplit("|", 1)[0]: r for r in jl(PS / "judge_local_llama8b_nf4.jsonl") if r["key"].endswith("|disg")}
    nli = {r["key"]: r for r in jl(PS / "rt_nli_local_nf4.jsonl")}
    out = {}
    for m, src in (("judge_local_qwen8b_disg", jq), ("judge_local_llama8b_disg", jll)):
        if src and all(k in src for k in calC):  # only once the EC arm is complete
            v = [1.0 - src[k]["p"] if src[k].get("p") is not None else 1.0 for k in calC]
            t = ST.matched_fa(v, 0.10)
            out[m] = {"t": t[0], "lambda": t[1], "n_neg": len(v), "tie_share_at_t": ST.tie_share_at(v, t[0])}
    if nli and all(k in nli for k in calC):
        for m in ("rt_nli_min_local", "rt_nli_fwd_local", "rt_nli_bwd_local", "rt_nli_contra_local", "rt_nli_min_alt_local", "rt_embed_cos_local"):
            v = []
            for k in calC:
                r = nli.get(k)
                v.append(1.0 if r is None or r.get(m) is None else (r[m] if m == "rt_nli_contra_local" else 1.0 - r[m]))
            t = ST.matched_fa(v, 0.10)
            out[m] = {"t": t[0], "lambda": t[1], "n_neg": len(v), "tie_share_at_t": ST.tie_share_at(v, t[0])}
    # S4_local on nf4 EC rows: shift diagnostic only (primary S4 threshold stays the frozen E one)
    p.write_text(json.dumps(out, indent=1))
    return out


# =============================================================================================== statistics helpers
def flags(rows, m, thr):
    return ST.flag_vec([r[m] for r in rows], *thr)


def auc_ties(pos, neg) -> float:
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    gt = (pos[:, None] > neg[None, :]).mean()
    eq = (pos[:, None] == neg[None, :]).mean()
    return float(gt + 0.5 * eq)


def base_matched_auroc(mut: list[dict], ctrl_by_base: dict, m: str) -> dict:
    by = defaultdict(list)
    for r in mut:
        by[r["base"]].append(r[m])
    per = {b: auc_ties(v, ctrl_by_base[b]) for b, v in by.items() if ctrl_by_base.get(b)}
    if not per:
        return {"n_bases": 0, "within_base_auroc": None, "ci": [None, None], "pooled_auroc": None}
    bases = sorted(per)
    vals = np.array([per[b] for b in bases])
    mean, ci = ST.cluster_boot_mean(vals, bases)
    pos = [x for b in bases for x in by[b]]
    neg = [x for b in bases for x in ctrl_by_base[b]]
    return {"n_bases": len(bases), "within_base_auroc": mean, "ci": ci, "pooled_auroc": auc_ties(pos, neg)}


# =============================================================================================== main
@logger.catch(reraise=True)
def main():
    C.guard("prereg_hyb")
    pp = C.guard("prereg_perturb")
    global S4_FILL
    S4_FILL = json.loads((C.RES / "s4_perturb_coefs.json").read_text())["fail_fill"]
    U = load_rows()
    avail = attach_scores(U)
    thr_gpu = gpu_thresholds(pp)
    THR = {m: (v["t"], v["lambda"]) for m, v in pp["thresholds_primary"].items()}
    THR.update({m: (v["t"], v["lambda"]) for m, v in thr_gpu.items()})
    METRICS = [m for m in CONS + CPU + GPU + API + ["S4_local"] if m in THR and any(u.get(m) is not None for u in U)]
    TIE = {m: pp["thresholds_primary"].get(m, thr_gpu.get(m, {})).get("tie_share_at_t") for m in METRICS}
    logger.info(f"metrics analysed: {METRICS}")
    A = {"prereg_perturb_sha256": C.sha256_file(C.RES / "prereg_perturb.json"), "available": avail, "metrics": METRICS,
         "thresholds_used": {m: THR[m] for m in METRICS}, "tie_share_at_t_E": TIE}
    # ---- base endorsement (consensus can only detect mutants of bases peers endorse)
    base_row = {u["base"]: u for u in U if u["control_type"] == "BASE"}
    for u in U:
        b = base_row[u["base"]]
        u["base_endorsed"] = None if b.get("c_hyb") is None else bool(b["c_hyb"] < 1.0)
        u["base_endorsed_align"] = None if b.get("c_align") is None else bool(b["c_align"] < 1.0)
    eb = [b for b in base_row.values() if not b["is_rcomp"]]
    A["base_endorsement"] = {"n_E_bases": len(eb), "share_endorsed_hyb": float(np.mean([bool(b.get("base_endorsed")) for b in eb])),
                             "share_endorsed_align": float(np.mean([bool(b.get("base_endorsed_align")) for b in eb])),
                             "by_status": {s: float(np.mean([bool(b.get("base_endorsed")) for b in eb if b["base_status"] == s]))
                                           for s in sorted({b["base_status"] for b in eb})}}
    # ---- write per-row scores
    with (C.RES / "perturb_scores.jsonl").open("w") as fh:
        for u in U:
            fh.write(json.dumps({k: v for k, v in u.items() if k not in ("text", "disguised_text", "disguised_fol")}, ensure_ascii=False) + "\n")
    # ---- coverage
    cov_rows = []
    for m in METRICS:
        st = Counter(u.get(m + "__status") for u in U)
        cov_rows.append({"metric": m, "n_rows": len(U), "n_scored_ok": st.get("ok", 0), "n_fail_filled": st.get("fail", 0),
                         "n_not_scorable": sum(v for k, v in st.items() if k and k.startswith("na")),
                         "reasons": "; ".join(f"{k}={v}" for k, v in st.items() if k and k.startswith("na")),
                         "reference_row_only": m in REFERENCE_ONLY})
    for m in set(CONS + CPU + GPU + API + ["S4_local"]) - set(METRICS):
        cov_rows.append({"metric": m, "n_rows": len(U), "n_scored_ok": 0, "n_fail_filled": 0, "n_not_scorable": len(U),
                         "reasons": "not run: " + ("GPU arm not completed" if m in GPU or m == "S4_local" else "no threshold/scores"),
                         "reference_row_only": m in REFERENCE_ONLY})
    wcsv(C.RES / "coverage_perturb.csv", cov_rows)
    # ---- secondary thresholds (in-sample, PERTURB non-rename controls + BASE)
    THR2 = {}
    for m in METRICS:
        v = [u[m] for u in U if u["y"] == 0 and u["control_type"] in NONRENAME_CTRL and u.get(m) is not None]
        THR2[m] = ST.matched_fa(v, 0.10) if v else (float("inf"), 0.0)
    A["thresholds_secondary"] = THR2
    # ---- per operator x polarity sensitivity
    mut = [u for u in U if u["y"] == 1]
    ctrl_by_base = defaultdict(lambda: defaultdict(list))
    for u in U:
        if u["y"] == 0 and u["control_type"] in NONRENAME_CTRL:
            for m in METRICS:
                if u.get(m) is not None:
                    ctrl_by_base[m][u["base"]].append(u[m])
    sens = []
    cells = [(op, pol) for op in OPS for pol in ("DOWN", "UP", "ALL")]
    cells += [("ADD[ADD_FOREIGN]", "ALL"), ("ADD[ADD_INTERNAL]", "ALL")]
    for m in METRICS:
        for op, pol in cells:
            if op.startswith("ADD["):
                sub = op[4:-1]
                rs = [u for u in mut if u["operator"] == "ADD" and u["subtype"] == sub]
            else:
                rs = [u for u in mut if u["operator"] == op and (pol == "ALL" or u["polarity"] == pol)]
            rs = [u for u in rs if u.get(m) is not None]
            for subset in ("all", "E_bases", "E_bases_endorsed"):
                rr = rs if subset == "all" else [u for u in rs if not u["is_rcomp"]]
                if subset == "E_bases_endorsed":
                    rr = [u for u in rr if u["base_endorsed"]]
                row = {"metric": m, "operator": op, "polarity": pol, "subset": subset, "n": len(rr),
                       "n_bases": len({u["base"] for u in rr})}
                if len(rr) == 0:
                    row["status"] = "absent (0 rows)"
                    sens.append(row)
                    continue
                f = flags(rr, m, THR[m])
                rec, ci = ST.cluster_boot_mean(f, [u["base"] for u in rr])
                f2 = flags(rr, m, THR2[m])
                bm = base_matched_auroc(rr, ctrl_by_base[m], m) if subset != "E_bases_endorsed" else {}
                row.update({"recall_primary": rec, "ci_lo": ci[0], "ci_hi": ci[1], "recall_secondary_insample": float(f2.mean()),
                            "within_base_auroc": bm.get("within_base_auroc"), "wb_ci_lo": (bm.get("ci") or [None])[0],
                            "wb_ci_hi": (bm.get("ci") or [None, None])[1], "pooled_auroc": bm.get("pooled_auroc"),
                            "status": "untestable (<30 rows)" if len(rr) < 30 else ("reported, not analysed" if op == "MOVE" else "ok"),
                            "threshold_degenerate": bool((TIE.get(m) or 0) > 0.5)})
                sens.append(row)
    wcsv(C.RES / "perturb_sensitivity.csv", sens)
    # ---- DOWN vs UP matched pairs
    pairs = defaultdict(dict)
    for u in mut:
        if u["matched_pair_id"] and u["pair_complete"] and u["polarity"] in ("DOWN", "UP"):
            pairs[u["matched_pair_id"]][u["polarity"]] = u
    pairs = {k: v for k, v in pairs.items() if "DOWN" in v and "UP" in v}
    A["n_complete_pairs"] = len(pairs)
    du = []
    for m in METRICS:
        for op in OPS + ["ALL"]:
            pr = [v for v in pairs.values() if (op == "ALL" or v["DOWN"]["operator"] == op)
                  and v["DOWN"].get(m) is not None and v["UP"].get(m) is not None]
            if not pr:
                continue
            fd = flags([p["DOWN"] for p in pr], m, THR[m])
            fu = flags([p["UP"] for p in pr], m, THR[m])
            d = fd - fu
            mean, ci = ST.cluster_boot_mean(d, [p["DOWN"]["base"] for p in pr])
            hd = fd >= 0.5  # hard flag = tie-aware flag rounded (score > t, or score == t with lambda >= 0.5)
            hu = fu >= 0.5
            sd = np.array([p["DOWN"][m] - p["UP"][m] for p in pr])
            du.append({"metric": m, "operator": op, "n_pairs": len(pr), "recall_DOWN": float(fd.mean()), "recall_UP": float(fu.mean()),
                       "diff_DOWN_minus_UP": mean, "ci_lo": ci[0], "ci_hi": ci[1],
                       "mcnemar_down_only": int((hd & ~hu).sum()), "mcnemar_up_only": int((~hd & hu).sum()),
                       "mcnemar_p": mcnemar(int((hd & ~hu).sum()), int((~hd & hu).sum())),
                       "mean_score_diff_DOWN_minus_UP": float(sd.mean()),
                       "polarity_symmetric_|diff|<0.05": bool(abs(mean) < 0.05),
                       "status": "untestable (<30 pairs)" if len(pr) < 30 else "ok"})
    wcsv(C.RES / "perturb_downup.csv", du)
    # ---- breakdowns by base status and base endorsement (pooled polarity)
    bd = []
    for m in METRICS:
        for op in OPS:
            rs = [u for u in mut if u["operator"] == op and u.get(m) is not None]
            if not rs:
                continue
            for dim, key in (("base_status", lambda u: u["base_status"]),
                             ("base_endorsed_hyb", lambda u: "R_COMP(no peers)" if u["is_rcomp"] else ("endorsed" if u["base_endorsed"] else "not_endorsed"))):
                g = C.group(rs, key)
                for lvl, rr in sorted(g.items()):
                    f = flags(rr, m, THR[m])
                    rec, ci = ST.cluster_boot_mean(f, [u["base"] for u in rr], b=500)
                    bd.append({"metric": m, "operator": op, "dimension": dim, "level": lvl, "n": len(rr), "recall_primary": rec,
                               "ci_lo": ci[0], "ci_hi": ci[1]})
    wcsv(C.RES / "perturb_breakdowns.csv", bd)
    # ---- invariance table (all metrics, PRIMARY thresholds) on PERTURB controls; flip vs the same base
    inv = []
    ctrl = [u for u in U if u["y"] == 0]
    for m in METRICS:
        for ct in sorted({u["control_type"] for u in ctrl}):
            for subset in ("all", "E_bases", "E_bases_endorsed"):
                rs = [u for u in ctrl if u["control_type"] == ct and u.get(m) is not None]
                if subset != "all":
                    rs = [u for u in rs if not u["is_rcomp"]]
                if subset == "E_bases_endorsed":
                    rs = [u for u in rs if u["base_endorsed"]]
                if ct != "BASE":
                    rs = [u for u in rs if base_row[u["base"]].get(m) is not None]
                if not rs:
                    continue
                f = flags(rs, m, THR[m])
                fa, ci = ST.cluster_boot_mean(f, [u["base"] for u in rs])
                row = {"metric": m, "family": ct, "source": "PERTURB_CONTROL" if ct != "BASE" else "PERTURB_BASE", "subset": subset,
                       "threshold": "primary_E", "n_rows": len(rs), "n_bases": len({u["base"] for u in rs}), "FA_on_correct": fa,
                       "FA_ci_lo": ci[0], "FA_ci_hi": ci[1]}
                if ct != "BASE":
                    fb = flags([base_row[u["base"]] for u in rs], m, THR[m])
                    flip = np.abs(f - fb)  # coupled tie draw: identical scores never flip
                    fl, flci = ST.cluster_boot_mean(flip, [u["base"] for u in rs])
                    row.update({"base_FA": float(fb.mean()), "flip_rate": fl, "flip_ci_lo": flci[0], "flip_ci_hi": flci[1],
                                "n_flipped_expected": float(flip.sum())})
                inv.append(row)
    inv += expD_rewrites(THR)
    # Part A rows (consensus, screen thresholds) appended for completeness
    for r in csv.DictReader((C.RES / "invariance_table_consensus.csv").open()):
        inv.append({"metric": r["metric"], "family": r["family"], "source": r["source"], "subset": r["subset"],
                    "threshold": "screen_prereg_hyb", "n_rows": r["n_rewrites"], "n_bases": r["n_bases"],
                    "FA_on_correct": r["FA_on_correct_bases"], "FA_ci_lo": r["FA_ci_lo"], "FA_ci_hi": r["FA_ci_hi"],
                    "base_FA": r["base_FA"], "flip_rate": r["flip_rate"], "flip_ci_lo": r["flip_ci_lo"], "flip_ci_hi": r["flip_ci_hi"],
                    "n_flipped_expected": r["n_flipped_expected"]})
    wcsv(C.RES / "invariance_table.csv", inv)
    # ---- invariance / sensitivity trade-off
    def get(rows, **kw):
        for r in rows:
            if all(r.get(k) == v for k, v in kw.items()):
                return r
        return {}
    to = []
    for m in METRICS:
        for subset in ("all", "E_bases"):
            to.append({"metric": m, "subset": subset,
                       "RENAME_SYN_FA": get(inv, metric=m, family="RENAME_SYN", subset=subset, threshold="primary_E").get("FA_on_correct"),
                       "RENAME_SYN_flip": get(inv, metric=m, family="RENAME_SYN", subset=subset, threshold="primary_E").get("flip_rate"),
                       "RENAME_NONCE_FA": get(inv, metric=m, family="RENAME_NONCE", subset=subset, threshold="primary_E").get("FA_on_correct"),
                       "RENAME_NONCE_flip": get(inv, metric=m, family="RENAME_NONCE", subset=subset, threshold="primary_E").get("flip_rate"),
                       "BASE_FA": get(inv, metric=m, family="BASE", subset=subset).get("FA_on_correct"),
                       "MEANING_RENAME_recall": get(sens, metric=m, operator="MEANING_RENAME", polarity="ALL", subset=subset).get("recall_primary"),
                       "SWAP_recall": get(sens, metric=m, operator="SWAP", polarity="ALL", subset=subset).get("recall_primary"),
                       "MEANING_RENAME_within_base_auroc": get(sens, metric=m, operator="MEANING_RENAME", polarity="ALL", subset=subset).get("within_base_auroc")})
    wcsv(C.RES / "tradeoff.csv", to)
    # ---- cross-metric comparison on the E-base subset where EVERY metric exists
    common = [u for u in U if not u["is_rcomp"] and all(u.get(m) is not None for m in METRICS)]
    cm = {"n_rows": len(common), "n_mutants": sum(u["y"] for u in common), "metrics": {}}
    ctrl_c = defaultdict(lambda: defaultdict(list))
    for u in common:
        if u["y"] == 0 and u["control_type"] in NONRENAME_CTRL:
            for m in METRICS:
                ctrl_c[m][u["base"]].append(u[m])
    for m in METRICS:
        mm = [u for u in common if u["y"] == 1]
        f = flags(mm, m, THR[m])
        cm["metrics"][m] = {"recall_all_mutants": float(f.mean()) if len(f) else None,
                            "within_base_auroc_all_mutants": base_matched_auroc(mm, ctrl_c[m], m).get("within_base_auroc"),
                            "control_FA": float(flags([u for u in common if u["y"] == 0], m, THR[m]).mean())}
    A["common_subset"] = cm
    A["n_rows"] = {"mutants": len(mut), "controls": sum(1 for u in U if u["y"] == 0 and u["control_type"] != "BASE"),
                   "bases": len(base_row)}
    (C.RES / "analysis_perturb.json").write_text(json.dumps(A, indent=1, default=str))
    logger.info(f"analysis_perturb done: {len(sens)} sensitivity rows, {len(du)} down/up rows, {len(inv)} invariance rows")


def expD_rewrites(THR: dict) -> list[dict]:
    """exp D shared rewrites (screen pools): consensus at the PRIMARY (E) thresholds, and exp D's own flash-lite judge
    (judge_cheap_disg column, 1 - p) at the EC threshold. Bases = screen items with adjudicated final_label CORRECT."""
    labs = json.loads((C.DATA / "screen" / "screen_adjudicated_labels.json").read_text())
    srows = C.load_scores("screen")
    inv = json.loads((C.DATA / "invariance_items.json").read_text())
    jd = {r["rw_id"]: r for r in jl(C.DATA / "screen" / "expD_rewrite_scores.jsonl")}
    jb = {r["item_id"]: r for r in jl(C.DATA / "screen" / "expD_per_item_scores.jsonl")} if (C.DATA / "screen" / "expD_per_item_scores.jsonl").exists() else {}
    out = []

    def sc(r, m):
        if r is None or r.get("coverage_status") != "OK":
            return 1.0
        v = r.get(m)
        return 1.0 if v is None else float(v)

    def jv(r):
        if r is None:
            return None
        v = r.get("judge_cheap_disg")
        return None if v is None else (1.0 - float(v) if v <= 1 else None)
    for fam in sorted({x["family"] for x in inv}):
        its = [x for x in inv if x["family"] == fam and labs.get(x["base_item_id"], {}).get("final_label") == "CORRECT"]
        for m in CONS + ["judge_cheap_disg"]:
            if m not in THR:
                continue
            pr, cl = [], []
            for x in its:
                if m == "judge_cheap_disg":
                    a, b = jv(jd.get(x["rw_id"])), jv(jb.get(x["base_item_id"]))
                    if a is None or b is None:
                        continue
                else:
                    k = "RW:" + x["rw_id"]
                    if k not in srows:
                        continue
                    a, b = sc(srows[k], m), sc(srows.get(x["base_item_id"]), m)
                pr.append((a, b))
                cl.append(x["base_item_id"])
            if not pr:
                continue
            f = ST.flag_vec([p[0] for p in pr], *THR[m])
            fb = ST.flag_vec([p[1] for p in pr], *THR[m])
            flip = np.abs(f - fb)  # coupled tie draw: identical scores never flip
            fa, ci = ST.cluster_boot_mean(f, cl)
            fl, flci = ST.cluster_boot_mean(flip, cl)
            out.append({"metric": m, "family": fam, "source": "expD_screen", "subset": "all", "threshold": "primary_E",
                        "n_rows": len(pr), "n_bases": len(set(cl)), "FA_on_correct": fa, "FA_ci_lo": ci[0], "FA_ci_hi": ci[1],
                        "base_FA": float(fb.mean()), "flip_rate": fl, "flip_ci_lo": flci[0], "flip_ci_hi": flci[1],
                        "n_flipped_expected": float(flip.sum())})
    return out


def mcnemar(b: int, c: int) -> float | None:
    from scipy.stats import binomtest
    return float(binomtest(b, b + c, 0.5).pvalue) if b + c > 0 else None


def wcsv(p: Path, rows: list[dict]):
    keys = []
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with p.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow(r)


if __name__ == "__main__":
    main()
