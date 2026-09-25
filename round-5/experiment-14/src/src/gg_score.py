#!/usr/bin/env python3
"""B6: GG scores + dev gates + diagnostics.
  E:        c_gg(x) = 1 - share of P(x) (V0's leave-own-family-out pool) agreeing under GG, for every row of the sentences
            searched (sentences with >= 1 Z row); brackets c_gg_allyes (every mapped pair accepted = pure name-free map)
            and c_exact (every non-identity pair rejected; matrix kind 'exact').
  PERTURB:  E-base MEANING_RENAME mutants, RENAME_SYN / RENAME_NONCE controls and BASE references vs every peer row of
            their E sentence (exp-8 pool_rule 'all'); baseline c_align from exp-8 perturb_scores.jsonl (same rows).
Gates g1 (RENAME_SYN paired flip <= 0.05 and FA <= FA(base) + 0.05), g2 (MEANING_RENAME recall >= c_align recall - 0.05),
g3 (E strat AUROC(c_gg) on Z >= V0 - 0.01). Writes results/scores_gg_E.jsonl, results/scores_gg_perturb.jsonl,
results/gg_dev.json, tables/gg_*.csv."""
from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict

import numpy as np
import pandas as pd

from common import FREEZE, MATRIX, PERTURB_SCORES, RES, ROOT, SEED, TAB, B, jdump, jl, setup_logger
from labels import T9, frame
from stats import SentBoot, WAuc, WStratAuc, auroc, boot_ci, strat_auroc

sys.path.insert(0, str(FREEZE))
import consensus_variants as CV  # noqa: E402
import gg  # noqa: E402

logger = setup_logger("gg_score")


def load_search() -> dict:
    return {r["id"]: r for r in jl(RES / "gg_search.jsonl")}


def decide(rec: dict | None, sid: str, verdicts: dict) -> tuple[bool, bool, bool, str]:
    """(agree_gg, agree_allyes, agree_identity_map, reason) for one search record."""
    if rec is None:
        return False, False, False, "no_record"
    if rec["status"] != "MAPPED":
        return False, False, False, rec["status"].split(":")[0]
    if any(not m["nonidentity"] for m in rec["maps"]):
        return True, True, True, "identity_map"
    for m in rec["maps"]:
        if all(verdicts.get(json.dumps([sid] + list(gg.pair_key(it)))) == "YES" for it in m["nonidentity"]):
            return True, True, False, "gloss_yes"
    return False, True, False, "gloss_rejected"


def accepted_index(rec: dict, sid: str, verdicts: dict) -> int:
    """Index of the first kept map whose every non-identity pair the checker accepted (the map that made GG agree)."""
    for k, m in enumerate(rec["maps"]):
        if all(verdicts.get(json.dumps([sid] + list(gg.pair_key(it)))) == "YES" for it in m["nonidentity"]):
            return k
    return 0


def score_E(S: dict, verdicts: dict, searched: set) -> tuple[pd.DataFrame, list]:
    out, pair_rows = [], []
    for r in jl(MATRIX):
        sid = r["sentence_id"]
        if sid not in searched:
            continue
        ix = CV.build_index(r)
        for rk in ix["node_of"]:
            P = CV.peers_lofo(ix, rk)
            if len(P) < 2:
                out.append({"row_key": rk, "c_gg": None, "c_gg_allyes": None, "gg_status": "PEER_UNAVAILABLE"})
                continue
            c = ix["node_of"][rk]
            ag = al = 0
            reasons = Counter()
            for p in P:
                pn = ix["node_of"][p]
                if pn == c or ix["kind"].get((c, pn)) == "exact" and ix["eq"].get((c, pn)) is True:
                    ag += 1
                    al += 1
                    reasons["exact"] += 1
                    continue
                i, j = min(c, pn), max(c, pn)
                rec = S.get(f"E|{sid}|{i}|{j}") or S.get(f"E|{sid}|{j}|{i}")
                a, b_, _, why = decide(rec, sid, verdicts)
                ag += a
                al += b_
                reasons[why] += 1
            out.append({"row_key": rk, "c_gg": 1 - ag / len(P), "c_gg_allyes": 1 - al / len(P), "gg_status": "OK", "n_peers_gg": len(P),
                        "reasons": dict(reasons)})
        for i, j, eq, kind, _s in r["pairs"]:
            if kind == "exact":
                continue
            rec = S.get(f"E|{sid}|{i}|{j}")
            a, b_, _, why = decide(rec, sid, verdicts)
            pair_rows.append({"sid": sid, "i": i, "j": j, "align_eq": eq is True, "kind": kind, "gg": a, "allyes": b_, "why": why,
                              "fol_i": r["nodes"][i]["canon_fol"] if r["nodes"][i]["node_id"] == i else None,
                              "fol_j": r["nodes"][j]["canon_fol"] if r["nodes"][j]["node_id"] == j else None,
                              "maps": ([rec["maps"][accepted_index(rec, sid, verdicts)]] if a and why == "gloss_yes" else rec["maps"][:1]) if rec else []})
    # unparseable rows of searched sentences -> 1.0
    return pd.DataFrame(out), pair_rows


def score_perturb(S: dict, verdicts: dict) -> pd.DataFrame:
    recs = {r["sentence_id"]: r for r in jl(MATRIX)}
    rows = []
    for r in jl(PERTURB_SCORES):
        if r["is_rcomp"]:
            continue
        kind = r["operator"] if r["operator"] else r["control_type"]
        if kind not in ("MEANING_RENAME", "RENAME_SYN", "RENAME_NONCE", "BASE"):
            continue
        m = recs[r["sentence_id"]]
        peer_rows = [(nd["node_id"], x["row_key"]) for nd in m["nodes"] for x in nd["rows"] if x["is_peer"]]
        d = {"key": r["key"], "base": r["base"], "sentence_id": r["sentence_id"], "kind": kind, "y": r["y"], "polarity": r.get("polarity"),
             "subtype": r.get("subtype"), "base_status": r.get("base_status"), "c_align": r.get("c_align"), "c_align_status": r.get("c_align__status"),
             "base_endorsed": r.get("base_endorsed"), "stratum": (r.get("strata") or {}).get("source_stratum"), "n_peer_rows": len(peer_rows)}
        if r.get("unparseable"):
            d.update(c_gg=1.0, c_gg_allyes=1.0, c_exact_pt=1.0)
        elif len(peer_rows) < 2:
            d.update(c_gg=None, c_gg_allyes=None, c_exact_pt=None)
        else:
            ag = al = ax = 0
            for n, _rk in peer_rows:
                a, b_, x, _ = decide(S.get(f"P|{r['key']}|{n}"), r["sentence_id"], verdicts)
                ag += a
                al += b_
                ax += x
            k = len(peer_rows)
            d.update(c_gg=1 - ag / k, c_gg_allyes=1 - al / k, c_exact_pt=1 - ax / k)
        rows.append(d)
    return pd.DataFrame(rows)


def perturb_gates(T: pd.DataFrame) -> dict:
    base = T[T.kind == "BASE"].set_index("base")
    out = {}
    for col in ("c_gg", "c_gg_allyes", "c_exact_pt", "c_align"):
        f = lambda v: (np.asarray(v, float) > 0.5)  # noqa: E731
        rec = {"FA_base_all": float(f(base[col].dropna()).mean())}
        for ct in ("RENAME_SYN", "RENAME_NONCE"):
            c = T[(T.kind == ct) & T[col].notna()].copy()
            c = c[c.base.isin(base.index) & base.loc[c.base.values, col].notna().values]
            fc = f(c[col].values)
            fb = f(base.loc[c.base.values, col].values)
            rec[ct] = {"n": int(len(c)), "FA": float(fc.mean()), "FA_paired_bases": float(fb.mean()), "paired_flip": float((fc != fb).mean()),
                       "by_base_status": {bs: {"n": int((c.base_status == bs).sum()), "FA": float(fc[c.base_status.values == bs].mean()),
                                               "FA_base": float(fb[c.base_status.values == bs].mean()),
                                               "flip": float((fc != fb)[c.base_status.values == bs].mean())}
                                          for bs in sorted(c.base_status.dropna().unique())}}
        mr = T[(T.kind == "MEANING_RENAME") & T[col].notna() & T.c_align.notna()]
        fm = f(mr[col].values)
        rec["MEANING_RENAME"] = {"n": int(len(mr)), "recall": float(fm.mean()),
                                 "recall_given_base_endorsed": float(fm[mr.base_endorsed.fillna(False).astype(bool).values].mean()) if mr.base_endorsed.fillna(False).any() else None,
                                 "n_base_endorsed": int(mr.base_endorsed.fillna(False).astype(bool).sum()),
                                 "by_polarity": {p: float(fm[mr.polarity.values == p].mean()) for p in sorted(mr.polarity.dropna().unique())}}
        out[col] = rec
    return out


@logger.catch(reraise=True)
def main():
    S = load_search()
    verdicts = json.loads((RES / "gg_verdicts.json").read_text())
    df = frame()
    searched = set(df[df.Z].sentence_id)
    G, pair_rows = score_E(S, verdicts, searched)
    df = df.merge(G, on="row_key", how="left")
    df.loc[df.sentence_id.isin(searched) & ~df.in_matrix, ["c_gg", "c_gg_allyes"]] = 1.0
    with (RES / "scores_gg_E.jsonl").open("w") as fh:
        for r in df[df.sentence_id.isin(searched)][["row_key", "sentence_id", "c_gg", "c_gg_allyes", "c_exact", "V0_frozen", "gg_status", "reasons"]].to_dict("records"):
            fh.write(json.dumps({k: (None if isinstance(v, float) and np.isnan(v) else v) for k, v in r.items()}, default=str) + "\n")
    P = df[df.Z].reset_index(drop=True)
    assert P.c_gg.notna().all(), int(P.c_gg.isna().sum())
    y = P.y.values.astype(int)
    st = P.stratum.values
    boot = SentBoot(P.sentence_id.values, b=B, seed=SEED)
    Wf = boot.W()
    D = {"population_Z": {"n": len(P), "n_error": int(y.sum()), "n_correct": int((1 - y).sum())}}
    # ---- g3 + AUROC table
    cells = {"ALL-strat": (None, "strat"), "pooled": (None, "pooled"), "LONG-strat": (("L25", "L20", "EXC"), "strat"),
             "L25": (("L25",), "pooled"), "CTRL": (("CTRL",), "pooled")}
    D["auroc"] = {}
    for cn, (strata, stat) in cells.items():
        m = np.ones(len(P), bool) if strata is None else np.isin(st, strata)
        ser = {}
        for s in ("c_gg", "c_gg_allyes", "c_exact", "V0_frozen"):
            v = P[s].astype(float).values[m]
            f = WStratAuc(y[m], v, st[m]) if stat == "strat" else WAuc(y[m], v)
            pt = strat_auroc(y[m], v, st[m]) if stat == "strat" else auroc(y[m], v)
            ser[s] = (pt, np.array([f(w) for w in Wf[:, m]]))
        D["auroc"][cn] = {s: {"auroc": pt, "ci": boot_ci(bs)} for s, (pt, bs) in ser.items()}
        for s in ("c_gg", "c_gg_allyes", "c_exact"):
            D["auroc"][cn][f"{s} - V0"] = {"delta": ser[s][0] - ser["V0_frozen"][0], "ci": boot_ci(ser[s][1] - ser["V0_frozen"][1])}
    g3 = D["auroc"]["ALL-strat"]["c_gg"]["auroc"] >= D["auroc"]["ALL-strat"]["V0_frozen"]["auroc"] - 0.01
    # ---- e/d per T9 class and overall (c > 0.5)
    fl = {s: P[s].astype(float).values > 0.5 for s in ("c_gg", "c_gg_allyes", "c_exact", "V0_frozen")}
    D["ed"] = {}
    for cut, m in (("ALL", np.ones(len(P), bool)), ("LONG", P.long.values), ("L25", st == "L25"), ("words_T3", P.words_t.values == "T3")):
        D["ed"][cut] = {s: {"e": float((~fl[s][m & (y == 1)]).mean()), "d": float(fl[s][m & (y == 0)].mean()),
                            "e_ci": boot_ci((Wf[:, m & (y == 1)] @ (~fl[s][m & (y == 1)]).astype(float)) / Wf[:, m & (y == 1)].sum(1)),
                            "d_ci": boot_ci((Wf[:, m & (y == 0)] @ fl[s][m & (y == 0)].astype(float)) / Wf[:, m & (y == 0)].sum(1))} for s in fl}
    D["t9_e"] = {}
    for cl in T9:
        m = np.array([cl in x for x in P.t9])
        if m.sum():
            D["t9_e"][cl] = {"n": int(m.sum()), **{s: float((~fl[s][m]).mean()) for s in fl}}
    # ---- PERTURB gates
    T = score_perturb(S, verdicts)
    T.to_json(RES / "scores_gg_perturb.jsonl", orient="records", lines=True)
    PG = perturb_gates(T)
    D["perturb"] = PG
    syn = PG["c_gg"]["RENAME_SYN"]
    g1 = syn["paired_flip"] <= 0.05 and syn["FA"] <= syn["FA_paired_bases"] + 0.05
    g2 = PG["c_gg"]["MEANING_RENAME"]["recall"] >= PG["c_align"]["MEANING_RENAME"]["recall"] - 0.05
    gates_ck = json.loads((RES / "gg_gates_confirm_v2.json").read_text())
    ck_pass = bool(gates_ck["pass_A"]) and gates_ck["pass_B"] in (True, "NOT_TESTABLE")
    D["gates"] = {"g1": {"pass": bool(g1), "paired_flip": syn["paired_flip"], "FA_SYN": syn["FA"], "FA_paired_bases": syn["FA_paired_bases"],
                         "FA_all_bases": PG["c_gg"]["FA_base_all"], "rule": "flip <= 0.05 AND FA <= FA(base) + 0.05"},
                  "g2": {"pass": bool(g2), "recall_gg": PG["c_gg"]["MEANING_RENAME"]["recall"], "recall_c_align": PG["c_align"]["MEANING_RENAME"]["recall"],
                         "FA_base_gg": PG["c_gg"]["FA_base_all"], "FA_base_c_align": PG["c_align"]["FA_base_all"],
                         "recall_given_base_endorsed_gg": PG["c_gg"]["MEANING_RENAME"]["recall_given_base_endorsed"],
                         "recall_given_base_endorsed_c_align": PG["c_align"]["MEANING_RENAME"]["recall_given_base_endorsed"]},
                  "g3": {"pass": bool(g3), "gg": D["auroc"]["ALL-strat"]["c_gg"]["auroc"], "V0": D["auroc"]["ALL-strat"]["V0_frozen"]["auroc"],
                         "delta_ci": D["auroc"]["ALL-strat"]["c_gg - V0"]["ci"]},
                  "checker": {"pass": ck_pass, "G-A_confirm_BA": gates_ck["G-A"]["balanced_accuracy"], "G-B": gates_ck["pass_B"],
                              "G-B_confirm_BA_descriptive": gates_ck["G-B"]["balanced_accuracy"]},
                  "NONCE_expected_failure": PG["c_gg"]["RENAME_NONCE"]}
    D["gates"]["GG_status"] = "PASS" if (g1 and g2 and g3 and ck_pass) else "FAIL"
    # ---- pair-level shares + disagreement examples
    pr = pd.DataFrame(pair_rows)
    D["pairs_E"] = {"n_nonexact_pairs": int(len(pr)), "why": dict(Counter(pr.why)),
                    "share_map_found": float(pr.allyes.mean()), "share_gloss_rejected": float((pr.why == "gloss_rejected").mean()),
                    "share_capped": float((pr.why == "CAPPED").mean()),
                    "crosstab_align_vs_gg": {f"align={a},gg={g}": int(((pr.align_eq == a) & (pr.gg == g)).sum()) for a in (True, False) for g in (True, False)}}
    ex_yes = pr[(pr.gg) & (~pr.align_eq)].head(10)
    ex_no = pr[(~pr.gg) & (pr.align_eq) & (pr.why == "gloss_rejected")].head(10)
    D["examples"] = {"GG_YES_align_rejected": ex_yes[["sid", "fol_i", "fol_j", "maps"]].to_dict("records"),
                     "GG_NO_align_accepted": ex_no[["sid", "fol_i", "fol_j", "maps"]].to_dict("records")}
    # ---- cost / seconds
    run = json.loads((RES / "gg_gloss_run.json").read_text())
    sweep_usd = run["first50"]["usd"] + (run["rest"]["usd"] if isinstance(run["rest"], dict) else 0)
    secs = defaultdict(float)
    for r in S.values():
        secs[r["id"][0]] += r["secs"] or 0.0
    n_cand_E = int(df.sentence_id.isin(searched).sum())
    n_items_E = sum(1 for k in json.loads((RES / "gg_verdicts.json").read_text()))
    D["cost"] = {"gloss_sweep_usd_total_E_plus_PERTURB": sweep_usd, "n_unique_gloss_pairs": n_items_E, "usd_per_call": sweep_usd / max(1, run["n_calls"]),
                 "E_candidates_scored": n_cand_E, "E_search_cpu_s_total": secs["E"], "PERTURB_search_cpu_s_total": secs["P"],
                 "FULL_per_E_candidate": {"cpu_s": secs["E"] / n_cand_E, "usd_upper": sweep_usd / n_cand_E,
                                          "note": "usd_upper divides the whole sweep (E + PERTURB pairs) by E candidates only"},
                 "MARGINAL_per_candidate": {"cpu_s": secs["E"] / max(1, len(pr)) * float(P.n_peers.mean()),
                                            "usd": run["first50"]["usd"] / max(1, run["first50"]["calls"]) * (len(pr[pr.allyes & (pr.why != "identity_map")]) / 12) / n_cand_E,
                                            "note": "a new candidate needs ~n_peers searches and one gloss call per 12 new mapped pairs; cached pairs cost 0"},
                 "peer_generation_usd_per_sentence": 0.0022064053623312495}
    D["gloss_run"] = run
    jdump(D, RES / "gg_dev.json")
    logger.info(f"GG gates: {json.dumps({k: v.get('pass') for k, v in D['gates'].items() if isinstance(v, dict) and 'pass' in v})} -> {D['gates']['GG_status']}")
    logger.info(f"g1 {json.dumps(D['gates']['g1'])}")
    logger.info(f"g2 {json.dumps(D['gates']['g2'])}")
    logger.info(f"g3 {json.dumps(D['gates']['g3'])}")
    logger.info(f"pairs {json.dumps(D['pairs_E'])}")
    for name, rows in (("gg_t9_e", [{"class": k, **v} for k, v in D["t9_e"].items()]),
                       ("gg_ed", [{"cut": c, "score": s, **v} for c, d in D["ed"].items() for s, v in d.items()])):
        with open(TAB / f"{name}.csv", "w") as fh:
            fh.write(f"# source: results/gg_dev.json :: src/gg_score.py main() [{name}]\n")
            pd.DataFrame(rows).to_csv(fh, index=False)


if __name__ == "__main__":
    main()
