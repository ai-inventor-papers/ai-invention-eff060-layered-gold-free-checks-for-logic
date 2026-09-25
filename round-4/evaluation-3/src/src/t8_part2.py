#!/usr/bin/env python3
"""PART 2: R_COMP second population with eval-2's UNCHANGED matrix readouts (row_consensus, ed_decomposition,
scatter_index, net_test, gee_fit). Writes pairwise_classes_RCOMP.jsonl, results/part2.json, tables/p2_*.csv."""
from __future__ import annotations

import json
import multiprocessing as mp
import os
import sys
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor
from itertools import combinations
from pathlib import Path

os.environ["PYTHONHASHSEED"] = "0"
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from loguru import logger  # noqa: E402
from scipy.stats import spearmanr  # noqa: E402

from t8_paths import E7, RESD, ROOT, jdump, jl, write_csv  # noqa: E402
import consensus_mx as CS  # noqa: E402
import mechanism as MC  # noqa: E402
from stats import SentBoot, ci  # noqa: E402
import t8_classes as TC  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "part2.log", rotation="30 MB", level="DEBUG")
N_MC = 500


def sboot_mean(vals: np.ndarray, sids: np.ndarray, B: int = 2000) -> dict:
    """Mean of pair/row-level values with a sentence-cluster bootstrap CI (stats.SentBoot weights)."""
    m = ~np.isnan(vals)
    vals, sids = vals[m], sids[m]
    if len(vals) == 0:
        return {"mean": None, "ci": [None, None], "n": 0, "n_sent": 0}
    bt = SentBoot(sids, b=B, seed=0)
    W = bt.W()
    return {"mean": float(vals.mean()), "ci": ci((W @ vals) / W.sum(1)), "n": int(len(vals)), "n_sent": int(len(set(sids)))}


@logger.catch(reraise=True)
def main() -> None:
    A = {}
    pre = json.loads((ROOT / "prereg_d_split.json").read_text())
    p_acc = float(pre["vocab_discount"]["accept_prob"])
    mats = jl(RESD / "pair_matrix_RCOMP.jsonl")
    sms = {(r["sentence_id"], r["condition"]): CS.SentenceMatrix(r) for r in mats}
    zver, csha = mats[0]["z3_version"], mats[0]["code_sha"]
    # ---------------- pairwise_classes_RCOMP.jsonl + non-transitivity
    nt = {"SIG": [0, 0], "FREE": [0, 0]}
    with (ROOT / "pairwise_classes_RCOMP.jsonl").open("w") as fh:
        for k in sorted(sms):
            line = CS.pairwise_class_line(sms[k], zver, csha)
            line["condition"] = k[1]
            fh.write(json.dumps(line, ensure_ascii=False) + "\n")
            nt[k[1]][0] += line["n_nontransitive_triples"]
            nt[k[1]][1] += line["n_wedges"]
    A["nontransitivity"] = {c: {"open": v[0], "wedges": v[1], "rate": v[0] / max(v[1], 1)} for c, v in nt.items()}
    A["matrix"] = {"n_tasks": len(mats), "n_pairs": int(sum(len(r["pairs"]) for r in mats)),
                   "reason_counts": {c: dict(pd.Series([p[3] for r in mats if r["condition"] == c for p in r["pairs"]]).value_counts()) for c in ("SIG", "FREE")},
                   "n_unknown": int(sum(p[2] is None for r in mats for p in r["pairs"])), "z3": zver, "code_sha": csha}
    # ---------------- per-row readouts
    C = pd.DataFrame(jl(E7 / "results" / "rcomp_candidates.jsonl"))
    C["word_tercile"] = C.strata.apply(lambda s: s["word_tercile"])
    C["nconds_bin"] = C.strata.apply(lambda s: s["nconds_bin"])
    C["words"] = C.strata.apply(lambda s: s["words"])
    C["n_conditions"] = C.strata.apply(lambda s: s["nconds_weak"])
    rc = []
    for r in C.itertuples():
        sm_ = sms.get((r.sentence_id, r.condition))
        x = CS.row_consensus(sm_, r.row_key) if sm_ is not None else None
        d = {"row_key": r.row_key, "in_matrix": x is not None}
        if x:
            d.update(npc=x["npc"], n_eq=x["n_eq"], n_eq_exact=x["n_eq_exact"], c_re=x["c_re"], c_exact=x["c_exact"],
                     end_maj=x["end_maj"], is_peer=sm_.row_meta[r.row_key]["is_peer"])
            d["end_maj_exact"] = (x["n_eq_exact"] > x["npc"] / 2) if x["npc"] >= 2 else None
        rc.append(d)
    C = C.merge(pd.DataFrame(rc), on="row_key", how="left")
    # ---------------- G3
    g3 = {}
    for cond, col_mx, col_7 in (("SIG", "c_exact", "c_score_sig"), ("SIG", "c_re", "c_score_align"), ("FREE", "c_re", "c_score_align")):
        s = C[(C.condition == cond) & C.parse_ok]
        both = s[s[col_mx].notna() & s[col_7].notna()]
        mis = both[(both[col_mx] - both[col_7]).abs() > 1e-6]
        none_mis = s[s[col_mx].isna() != s[col_7].isna()]
        g3[f"{cond}|{col_7}"] = {"n_compared": len(both), "n_mismatch": len(mis), "match_rate": 1 - len(mis) / max(len(both), 1),
                                 "n_none_disagree": len(none_mis), "pass": (1 - len(mis) / max(len(both), 1)) >= 0.99,
                                 "mismatch_examples": mis[["row_key", col_mx, col_7, "npc", "n_peers_sig" if cond == "SIG" else "n_peers_hyb"]].head(8).to_dict("records")}
        mis.assign(gate=f"{cond}|{col_7}")[["gate", "row_key", "sentence_id", col_mx, col_7, "npc"]].to_csv(
            ROOT / "tables" / f"p2_g3_mismatch_{cond}_{col_7}.csv", index=False)
    A["G3"] = g3
    logger.info(f"G3 {({k: (v['match_rate'], v['n_compared']) for k, v in g3.items()})}")
    # ---------------- SIG labelled
    sig = C[C.condition == "SIG"].copy()
    A["SIG_label_counts"] = {k: int(v) for k, v in sig.label.value_counts().items()}
    S = sig[sig.label.isin(["CORRECT", "ERROR"]) & sig.c_re.notna()].copy().reset_index(drop=True)
    S["y_AB"] = (S.label == "ERROR").astype(int)
    S["end_MAJ"] = S.end_maj.astype(int)
    S["end_MAJ_EXACT"] = S.end_maj_exact.astype(int)
    S["end_SIG7"] = (S.c_score_sig < 0.5).astype(int)
    A["SIG_excluded"] = {"not_labelled_CORRECT_ERROR": int((~sig.label.isin(["CORRECT", "ERROR"])).sum()),
                         "labelled_but_npc_lt2_or_unparseable": int((sig.label.isin(["CORRECT", "ERROR"]) & sig.c_re.isna()).sum())}
    A["SIG_ed"] = {r: MC.ed_decomposition(S.y_AB, S[c]) for r, c in (("END_MAJ_align", "end_MAJ"), ("MAJ_EXACT", "end_MAJ_EXACT"),
                                                                    ("exp7_c_score_sig_lt_0.5", "end_SIG7"))}
    A["SIG_ed_gate"] = {"exp7_e": 0.0, "exp7_d": 0.2596}
    bt = SentBoot(S.sentence_id.values, b=2000, seed=0)
    W = bt.W()
    y = S.y_AB.values
    rows = []
    for dim, lab in (("ALL", np.array(["ALL"] * len(S))), ("word_tercile", S.word_tercile.values), ("nconds_bin", S.nconds_bin.values),
                     ("template_id", S.template_id.values), ("matched_reading", S.matched_reading.fillna("none").values)):
        for val in sorted(set(lab)):
            m = lab == val
            for rule, col in (("END_MAJ_align", "end_MAJ"), ("MAJ_EXACT", "end_MAJ_EXACT")):
                en = S[col].values.astype(float)
                yy, ee, Wm = y[m], en[m], W[:, m]
                with np.errstate(invalid="ignore", divide="ignore"):
                    eb = (Wm @ (ee * yy)) / (Wm @ yy)
                    db = (Wm @ ((1 - ee) * (1 - yy))) / (Wm @ (1 - yy))
                ns = len(set(S.sentence_id.values[m]))
                rows.append({"dim": dim, "cell": val, "rule": rule, "n_err": int(yy.sum()), "n_cor": int((1 - yy).sum()), "n_sent": ns,
                             "e": float(ee[yy == 1].mean()) if yy.sum() else None, "d": float(1 - ee[yy == 0].mean()) if (1 - yy).sum() else None,
                             "e_ci": ci(eb) if yy.sum() >= 30 else [None, None], "d_ci": ci(db) if (1 - yy).sum() >= 30 else [None, None],
                             "testable": bool(min(yy.sum(), (1 - yy).sum()) >= 30 and ns >= 10)})
    T = pd.DataFrame(rows)
    write_csv(T, "p2_sig_ed_cuts.csv", [f"{ROOT}/pairwise_classes_RCOMP.jsonl :: SIG matrix", f"{E7}/results/rcomp_candidates.jsonl :: label, strata, matched_reading"])
    A["SIG_d_by_reading"] = T[(T.dim == "matched_reading")].to_dict("records")
    # scatter_index (unchanged): P_lab needs family_vendor, y_AB, words, n_conditions, stratum
    sent_words = S.drop_duplicates("sentence_id").words.values
    cut = {"words_tercile_cuts": [float(q) for q in np.quantile(sent_words, [1 / 3, 2 / 3])]}
    Plab = S.assign(family_vendor=S.family, stratum=S.template_id)
    sms_sig = {k[0]: v for k, v in sms.items() if k[1] == "SIG"}
    try:
        sc = MC.scatter_index(Plab, sms_sig, cut)
        A["SIG_scatter"] = {"overall": sc["summary"]["overall"], "by_words_tercile": sc["summary"]["by_words_tercile"],
                            "pair_gee": sc["summary"]["pair_gee"], "n_pairs": sc["summary"]["n_pairs"], "prediction": sc["summary"]["prediction"]}
    except (ValueError, KeyError, ZeroDivisionError) as e:
        logger.error(f"scatter_index failed: {e}")
        A["SIG_scatter"] = {"error": str(e)[:300]}
    # net_test (unchanged): R_COMP words tercile W1/W3 -> T1/T3; nconds 4 (bottom) -> '0-1', 5 (top) -> '4+'
    Pn = S.assign(in_RAB=True, long=True, words_t=S.word_tercile.map({"W1": "T1", "W2": "T2", "W3": "T3"}),
                  ncond_bin=S.nconds_bin.map({"4": "0-1", "5": "4+"}), stratum=S.template_id)
    A["SIG_net"] = {}
    for rule, col in (("END_MAJ_align", "end_MAJ"), ("MAJ_EXACT", "end_MAJ_EXACT")):
        try:
            A["SIG_net"][rule] = MC.net_test(Pn, SentBoot(Pn.sentence_id.values, b=200, seed=0), col)
        except (ValueError, np.linalg.LinAlgError) as e:
            A["SIG_net"][rule] = {"error": str(e)[:200]}
    A["SIG_net_note"] = "net_test unchanged; B = 200 (AME refits); 'ncond_4p_minus_01' here = nconds 5 minus nconds 4 (R_COMP has only 4/5)"
    # GEE slopes of d
    cor = MC.zcols(S[S.y_AB == 0].assign(not_endorsed=lambda d: 1 - d.end_MAJ))
    A["SIG_gee_d"] = {"words": MC.gee_fit(cor, "not_endorsed ~ zw"), "nconds": MC.gee_fit(cor, "not_endorsed ~ zn")}
    logger.info(f"SIG e/d {A['SIG_ed']}")
    # ---------------- FREE vs SIG, peer (few-shot) rows paired by (sentence, slot)
    nf_of = {}
    for cond in ("SIG", "FREE"):
        for rec in jl(E7 / "results" / f"scores_{cond}.jsonl"):
            for rk, o in rec["rows"].items():
                for pk, v in (o.get("peer_equal_nf") or {}).items():
                    nf_of[(rk, pk)] = v
    peers = C[C.is_peer.fillna(False).astype(bool)].copy()
    slot_row = {(r.sentence_id, r.condition, r.slot): r for r in peers.itertuples()}
    pair_rows = []
    name_need = set()
    for (sid, cond), sm_ in sms.items():
        if cond != "FREE":
            continue
        slots = sorted({k[2] for k in slot_row if k[0] == sid and k[1] == "FREE"})
        for s, t in combinations(slots, 2):
            a, b = slot_row[(sid, "FREE", s)], slot_row[(sid, "FREE", t)]
            if a.family == b.family:
                continue
            a2, b2 = slot_row.get((sid, "SIG", s)), slot_row.get((sid, "SIG", t))
            sm_s = sms.get((sid, "SIG"))
            na, nb = sm_.row_node[a.row_key], sm_.row_node[b.row_key]
            rec = {"sentence_id": sid, "template_id": a.template_id, "word_tercile": a.word_tercile, "s": s, "t": t,
                   "free_exact": int(sm_.is_exact(na, nb)), "free_align": int(sm_.is_eq(na, nb)),
                   "free_nf": int(bool(nf_of.get((a.row_key, b.row_key)) or nf_of.get((b.row_key, a.row_key)))),
                   "free_nf_known": (a.row_key, b.row_key) in nf_of or (b.row_key, a.row_key) in nf_of,
                   "fa": sm_.nodes[na]["canon_fol"], "fb": sm_.nodes[nb]["canon_fol"]}
            if a2 is not None and b2 is not None and sm_s is not None:
                ma, mb = sm_s.row_node[a2.row_key], sm_s.row_node[b2.row_key]
                rec.update(sig_exact=int(sm_s.is_exact(ma, mb)), sig_align=int(sm_s.is_eq(ma, mb)),
                           sig_nf=int(bool(nf_of.get((a2.row_key, b2.row_key)) or nf_of.get((b2.row_key, a2.row_key)))))
            if not rec["free_exact"]:
                name_need.add((min(rec["fa"], rec["fb"]), max(rec["fa"], rec["fb"])))
            pair_rows.append(rec)
    PR = pd.DataFrame(pair_rows)
    # NAME_ONLY on FREE pairs (z3 on normalised vocabularies)
    import pairwise as PW
    pre_f = {u: TC.name_only_prefilter(*u) for u in name_need}
    todo = [u for u, v in pre_f.items() if v == "z3"]
    res = {u: (False, v) for u, v in pre_f.items() if v != "z3"}
    with ProcessPoolExecutor(max_workers=4, mp_context=mp.get_context("spawn"), initializer=PW.init_worker, initargs=(3.5,)) as ex:
        for a_, b_, r_, why in ex.map(TC.work_name_only, todo, chunksize=4):
            res[(a_, b_)] = (r_, why)
    PR["free_name"] = [int((not fe) and res.get((min(a_, b_), max(a_, b_)), (False,))[0] is True)
                       for a_, b_, fe in zip(PR.fa, PR.fb, PR.free_exact)]
    A["FREE_name_only"] = {"n_unique_pairs": len(name_need), "n_z3": len(todo), "n_true": int(sum(v[0] is True for v in res.values())),
                           "prefilter": dict(pd.Series(list(pre_f.values())).value_counts())}
    PR["free_align_or_nf"] = ((PR.free_align + PR.free_nf) > 0).astype(int)
    both = PR[PR.sig_exact.notna()].copy()
    sids = both.sentence_id.values
    drops = {}
    for rule, col in (("exact", "free_exact"), ("align", "free_align"), ("NF", "free_nf"), ("align_or_NF", "free_align_or_nf")):
        v = (both.sig_exact - both[col]).values.astype(float)
        drops[rule] = {"overall": sboot_mean(v, sids), "by_template": {}, "by_word_tercile": {}}
        for tpl, g in both.groupby("template_id"):
            drops[rule]["by_template"][tpl] = sboot_mean((g.sig_exact - g[col]).values.astype(float), g.sentence_id.values)
        for wt, g in both.groupby("word_tercile"):
            drops[rule]["by_word_tercile"][wt] = sboot_mean((g.sig_exact - g[col]).values.astype(float), g.sentence_id.values)
    A["drop_pairs"] = drops
    ag = {k: sboot_mean(both[k].values.astype(float), sids) for k in ("sig_exact", "sig_align", "sig_nf", "free_exact", "free_align", "free_nf", "free_align_or_nf", "free_name")}
    A["agreement_rates_pairs"] = ag
    bt2 = SentBoot(sids, b=2000, seed=0)
    W2 = bt2.W()
    rec_share = {}
    for rule, col in (("align", "free_align"), ("NF", "free_nf"), ("align_or_NF", "free_align_or_nf")):
        num = both[col].values - both.free_exact.values
        den = both.sig_exact.values - both.free_exact.values
        rec_share[rule] = {"share": float(num.mean() / den.mean()), "ci": ci((W2 @ num) / (W2 @ den))}
    A["recovered_share"] = rec_share
    logger.info(f"agreement SIG exact {ag['sig_exact']['mean']:.3f} FREE exact {ag['free_exact']['mean']:.3f} align {ag['free_align']['mean']:.3f} "
                f"NF {ag['free_nf']['mean']:.3f}; recovered {rec_share}")
    PR.drop(columns=["fa", "fb"]).to_csv(ROOT / "tables" / "p2_slot_pairs.csv", index=False)
    # ---------------- row-level endorsement: SIG vs FREE same (sentence, slot), peer rows
    pe = peers[peers.npc >= 2]
    sigr = pe[pe.condition == "SIG"].set_index(["sentence_id", "slot"])
    frer = pe[pe.condition == "FREE"].set_index(["sentence_id", "slot"])
    J = sigr[["end_maj", "end_maj_exact", "template_id", "word_tercile", "row_key"]].join(
        frer[["end_maj", "end_maj_exact", "row_key"]], lsuffix="_sig", rsuffix="_free", how="inner").reset_index()
    for a_, b_ in (("end_maj_exact_sig", "end_maj_free"), ("end_maj_sig", "end_maj_free"), ("end_maj_exact_sig", "end_maj_exact_free")):
        v = (J[a_].astype(float) - J[b_].astype(float)).values
        A.setdefault("row_endorsement_drop", {})[f"{a_} - {b_}"] = sboot_mean(v, J.sentence_id.values)
    A["row_endorsement_rates"] = {c: float(J[c].astype(float).mean()) for c in ("end_maj_sig", "end_maj_exact_sig", "end_maj_free", "end_maj_exact_free")}
    A["row_endorsement_n"] = {"n_rows": len(J), "n_sent": int(J.sentence_id.nunique())}
    # ---------------- FREE classes per sentence and plurality share (peer rows)
    cls = []
    for (sid, cond), sm_ in sms.items():
        pn = sorted({sm_.row_node[rk] for rk, m in sm_.row_meta.items() if m["is_peer"]})
        nrows = sum(1 for m in sm_.row_meta.values() if m["is_peer"])
        if not pn:
            continue

        def comps(edge):
            par = {i: i for i in pn}

            def f(i):
                while par[i] != i:
                    par[i] = par[par[i]]
                    i = par[i]
                return i
            for i, j in combinations(pn, 2):
                if edge(i, j):
                    par[f(i)] = f(j)
            return par, f
        out_c = {}
        for nm, edge in (("exact", sm_.is_exact), ("eqmv", sm_.is_eq)):
            par, f = comps(edge)
            size = defaultdict(int)
            for rk, m in sm_.row_meta.items():
                if m["is_peer"]:
                    size[f(sm_.row_node[rk])] += 1
            out_c[f"n_classes_{nm}"] = len(size)
            out_c[f"plurality_share_{nm}"] = max(size.values()) / nrows
        cl = sm_.cliques()
        out_c["n_cliques_eqmv_all_nodes"] = len(cl)
        cls.append({"sentence_id": sid, "condition": cond, "n_peer_rows": nrows, "n_peer_nodes": len(pn), **out_c})
    CL = pd.DataFrame(cls)
    write_csv(CL, "p2_classes_per_sentence.csv", [f"{ROOT}/pairwise_classes_RCOMP.jsonl :: peer rows"])
    A["classes_per_sentence"] = CL.groupby("condition")[[c for c in CL.columns if c.startswith(("n_", "plurality"))]].mean().to_dict("index")
    A["endorsement_rate_all_rows"] = {c: float(C[(C.condition == c) & C.end_maj.notna()].end_maj.astype(float).mean()) for c in ("SIG", "FREE")}
    # ---------------- OUT-OF-SAMPLE VALIDATION: Part-1 method on FREE predicts SIG endorsement
    fr = peers[(peers.condition == "FREE") & (peers.npc >= 2)]
    val = []
    for r in fr.itertuples():
        sm_ = sms[(r.sentence_id, "FREE")]
        ci_ = sm_.row_node[r.row_key]
        fam = r.family
        base = vocab = n = 0
        for rk, m in sm_.row_meta.items():
            if not m["is_peer"] or m["family"] == fam or rk == r.row_key:
                continue
            n += 1
            pj = sm_.row_node[rk]
            al = sm_.is_eq(ci_, pj)
            fa_, fb_ = sm_.nodes[ci_]["canon_fol"], sm_.nodes[pj]["canon_fol"]
            nm = (not sm_.is_exact(ci_, pj)) and res.get((min(fa_, fb_), max(fa_, fb_)), (False,))[0] is True
            if al or nm:
                base += 1
            elif nf_of.get((r.row_key, rk)) is True:
                vocab += 1
        val.append({"sentence_id": r.sentence_id, "slot": r.slot, "template_id": r.template_id, "npc": n, "base": base, "vocab": vocab,
                    "R_align": int(r.end_maj), "R_name": int(base > n / 2), "R_liberal": int(base + vocab > n / 2)})
    V = pd.DataFrame(val)
    rng = np.random.default_rng(0)
    draws = np.array([(V.base.values + rng.binomial(V.vocab.values, p_acc)) > V.npc.values / 2 for _ in range(N_MC)]).astype(float)
    V["R_point_MC"] = draws.mean(0)
    sg = sig[(sig.is_peer.fillna(False).astype(bool)) & (sig.npc >= 2)][["sentence_id", "slot", "end_maj_exact", "end_maj"]]
    V = V.merge(sg, on=["sentence_id", "slot"], how="inner")
    V["actual_SIG_exact"] = V.end_maj_exact.astype(float)
    V["actual_SIG_align"] = V.end_maj.astype(float)
    vr = {"n_rows": len(V), "n_sent": int(V.sentence_id.nunique()), "actual_SIG_exact_rate": float(V.actual_SIG_exact.mean())}
    per_tpl = []
    for rule in ("R_align", "R_name", "R_liberal", "R_point_MC"):
        v = (V[rule] - V.actual_SIG_exact).values.astype(float)
        vr[rule] = {"pred_rate": float(V[rule].mean()), "calib_err": sboot_mean(v, V.sentence_id.values)}
        vr[rule]["validated_abs_err_le_0.05"] = bool(abs(vr[rule]["calib_err"]["mean"]) <= 0.05)
        pt = V.groupby("template_id").agg(pred=(rule, "mean"), actual=("actual_SIG_exact", "mean"), n=("slot", "size"))
        vr[rule]["spearman_templates"] = float(spearmanr(pt.pred, pt.actual).correlation) if pt.pred.nunique() > 1 else None
        for tpl, g in V.groupby("template_id"):
            ce = sboot_mean((g[rule] - g.actual_SIG_exact).values.astype(float), g.sentence_id.values, B=1000)
            per_tpl.append({"rule": rule, "template_id": tpl, "n": len(g), "pred": float(g[rule].mean()), "actual": float(g.actual_SIG_exact.mean()),
                            "calib_err": ce["mean"], "ci_lo": ce["ci"][0], "ci_hi": ce["ci"][1]})
    A["validation"] = vr
    write_csv(pd.DataFrame(per_tpl), "p2_validation_by_template.csv", [f"{ROOT}/pairwise_classes_RCOMP.jsonl", f"{E7}/results/scores_FREE.jsonl :: peer_equal_nf"])
    V.to_csv(ROOT / "tables" / "p2_validation_rows.csv", index=False)
    logger.info(f"validation {({k: (v['pred_rate'], v['calib_err']['mean']) for k, v in vr.items() if isinstance(v, dict)})} actual {vr['actual_SIG_exact_rate']:.3f}")
    # ---------------- FREE tier-A labelled subset (descriptive)
    F = C[(C.condition == "FREE") & C.label.isin(["CORRECT", "ERROR"]) & C.c_re.notna()]
    yF = (F.label == "ERROR").astype(int).values
    A["FREE_tierA"] = {"END_MAJ_align": MC.ed_decomposition(yF, F.end_maj.astype(int).values),
                       "MAJ_EXACT": MC.ed_decomposition(yF, F.end_maj_exact.astype(int).values),
                       "caveat": "34 CORRECT rows only: descriptive, no test"}
    keep = ["row_key", "sentence_id", "condition", "template_id", "slot", "family", "label", "parse_ok", "is_peer", "npc", "n_eq", "n_eq_exact",
            "c_re", "c_exact", "end_maj", "end_maj_exact", "c_score_sig", "c_score_align", "word_tercile", "nconds_bin"]
    C[keep].to_pickle(RESD / "part2_rows.pkl")
    PR.drop(columns=["fa", "fb"]).to_pickle(RESD / "part2_pairs.pkl")
    jdump(RESD / "part2.json", A)
    logger.info("PART 2 done")


if __name__ == "__main__":
    main()
