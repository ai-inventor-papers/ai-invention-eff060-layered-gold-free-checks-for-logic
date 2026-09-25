"""STAGE 7: analysis. Verifies the prereg sha256 FIRST (abort on mismatch); only then joins scores to operators/labels.

Parts (every output carries its variant label; proxy / local arms are never used for a gate verdict):
  1 anchoring.csv          per op_label x polarity x base_source x variant: n, e (+ base-clustered CI), recall at
                           c>0.5 / c==1 / c>0, recall | base endorsed; d on BASES by length; delta_anchor (LOCAL2).
  2 controls_fa.csv        per control_type x base_source x variant: FA (3 thresholds), paired base FA, FA - base FA,
                           flip rate (CIs); exp-8 reference rows cited.
  3 typing_csc.csv (+confusion, rows)   same-vocab typing accuracy per target (oracle / proxy / free3 / csc).
  4 rcomp_sig_csc.json, rcomp_free_labelfree.json
  5 cost_table.csv
  6 csc_gate_P.json, tables.md
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

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(SRC / "vendor_x7"))
import csc_prereg  # noqa: E402

DATA = ROOT / "data"
RES = ROOT / "results"
RUN = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop")
E8 = RUN / "iter_3/gen_art/gen_art_experiment_8"
E7 = RUN / "iter_3/gen_art/gen_art_experiment_7"
E9 = RUN / "iter_4/gen_art/gen_art_experiment_9"
B = 2000
SEED = 0
TYPING_MAP = {"DROP": "ADD", "ADD": "DROP", "ADD_ANY": "DROP", "SUBST": "MEANING_RENAME"}
ANCHOR_OPS = ["ADD_FOREIGN", "ADD_INTERNAL", "MEANING_RENAME", "DROP", "SWAP", "NEG", "REV", "QUANT", "RESTR", "CONN",
              "MOVE", "BIND"]
CONTROLS = ["RENAME_SYN", "RENAME_NONCE", "REORDER_COMMUTE", "REORDER_QUANT", "CONTRAPOSITIVE", "DEMORGAN"]


def jl(p: Path) -> list[dict]:
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()] if p.exists() else []


def fnum(x, d=3):
    return None if x is None or (isinstance(x, float) and math.isnan(x)) else round(float(x), d)


# ============================================================================================ bootstrap helpers
def boot_ratio(num: np.ndarray, den: np.ndarray, b: int = B, seed: int = SEED) -> tuple[float, float, float]:
    """Cluster bootstrap of sum(num)/sum(den); num/den are per-cluster sums."""
    num, den = np.asarray(num, float), np.asarray(den, float)
    if den.sum() == 0:
        return (float("nan"),) * 3
    est = num.sum() / den.sum()
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(num), size=(b, len(num)))
    nb, db = num[idx].sum(1), den[idx].sum(1)
    ok = db > 0
    bs = nb[ok] / db[ok]
    return est, float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))


def clustered(values: list[float], clusters: list) -> tuple[float, float, float]:
    """Mean of per-row values with a cluster bootstrap."""
    if not values:
        return (float("nan"),) * 3
    num, den = defaultdict(float), defaultdict(float)
    for v, c in zip(values, clusters):
        num[c] += v
        den[c] += 1
    ks = sorted(num)
    return boot_ratio(np.array([num[k] for k in ks]), np.array([den[k] for k in ks]))


# ============================================================================================ data join
def load_rows() -> tuple[list[dict], dict]:
    view = jl(DATA / "perturb_view.jsonl")
    sc = {r["key"]: r for r in jl(RES / "scores_raw.jsonl")}
    loc = {r["key"]: r for r in jl(RES / "scores_local2.jsonl")}
    e8 = {}
    for line in (E8 / "results" / "perturb_scores.jsonl").read_text().splitlines():
        x = json.loads(line)
        e8[x["key"]] = {k: x.get(k) for k in ("c_align", "c_hyb", "c_nf", "judge_cheap_disg", "base_endorsed_align")}
    rows = []
    for r in view:
        s = sc.get(r["key"], {})
        l2 = loc.get(r["key"], {})
        x = e8.get(r["key"], {})
        rows.append({**r, **{k: v for k, v in s.items() if k not in ("key", "set")},
                     **{k: v for k, v in l2.items() if k not in ("key", "set")},
                     "c_align_exp8": x.get("c_align"), "c_hyb_exp8": x.get("c_hyb"), "c_nf_exp8": x.get("c_nf"),
                     "judge_cheap_disg_exp8": x.get("judge_cheap_disg")})
    return rows, {"n_scores": len(sc), "n_local": len(loc)}


def variants(rows: list[dict]) -> dict:
    """variant -> score column; only variants with >= 1 non-null score are kept."""
    cand = {"CSC_K3": "c_csc", "CSC_K4": "c_csc_k4", "CSC_multi": "c_csc_multi", "CSC_graded": "c_csc_graded",
            "SIGPROXY_K3": "c_proxy", "SIGPROXY_K4": "c_proxy_k4", "SIGPROXY_graded": "c_proxy_graded",
            "LOCAL2_own_sig": "c_local", "LOCAL2_base_sig": "c_localbase", "LOCAL2_graded": "c_local_graded",
            "FREE_c_align_exp8": "c_align_exp8", "FREE_c_hyb_exp8": "c_hyb_exp8",
            "FREE3_exact": "c_free3_exact", "FREE3_align": "c_free3_align", "FREE3_lc": "c_free3_lc",
            "JUDGE_flashlite_disg_exp8": "judge_cheap_disg_exp8"}
    out = {}
    for v, col in cand.items():
        if any(r.get(col) is not None for r in rows):
            out[v] = col
    return out


# ============================================================================================ PART 1 anchoring
def part1(rows: list[dict], V: dict) -> list[dict]:
    base_score = {v: {r["base_item_id"]: r.get(col) for r in rows if r["fold"] == "BASE"} for v, col in V.items()}
    out = []
    muts = [r for r in rows if r["fold"] == "PERTURB"]
    for v, col in V.items():
        for op in ANCHOR_OPS + ["ALL_MUTANTS"]:
            for pol in ("ALL", "DOWN", "UP"):
                for src in ("E", "RCOMP", "ALL"):
                    sel = [r for r in muts if (op == "ALL_MUTANTS" or r["op_label"] == op)
                           and (pol == "ALL" or r["polarity"] == pol)
                           and (src == "ALL" or (r["is_rcomp"] == (src == "RCOMP")))]
                    have = [r for r in sel if r.get(col) is not None]
                    if not have:
                        continue
                    c = [float(r[col]) for r in have]
                    cl = [r["base_item_id"] for r in have]
                    endorsed = [1.0 if x <= 0.5 else 0.0 for x in c]
                    e, lo, hi = clustered(endorsed, cl)
                    stc = col.replace("c_", "") + "_status"
                    suff = [r for r in have if not str(r.get(stc, "")).startswith("csc_insuff")]
                    rec = {"variant": v, "op_label": op, "polarity": pol, "base_source": src, "n": len(have),
                           "n_na": len(sel) - len(have),
                           "n_insufficient": len(have) - len(suff),
                           "e_excl_insufficient": fnum(np.mean([float(r[col]) <= 0.5 for r in suff])) if suff else None,
                           "e": fnum(e), "e_lo": fnum(lo), "e_hi": fnum(hi), "recall_gt05": fnum(1 - e),
                           "recall_eq1": fnum(np.mean([x >= 1 - 1e-9 for x in c])),
                           "recall_gt0": fnum(np.mean([x > 1e-9 for x in c]))}
                    be = [(x, base_score[v].get(r["base_item_id"])) for x, r in zip(c, have)]
                    for tag, cond in (("base_endorsed", lambda b: b is not None and b <= 0.5),
                                      ("base_not_endorsed", lambda b: b is not None and b > 0.5)):
                        sub = [x for x, b in be if cond(b)]
                        rec[f"n_{tag}"] = len(sub)
                        rec[f"recall_given_{tag}"] = fnum(np.mean([x > 0.5 for x in sub])) if sub else None
                    out.append(rec)
    return out


def d_by_length(rows: list[dict], V: dict) -> list[dict]:
    """CSC-style FA on the unmutated BASES (label-certain CORRECT): overall, by words tercile, by n_conditions, and the
    logistic slope of flag ~ words (per 10 words) with a base bootstrap."""
    from sklearn.linear_model import LogisticRegression
    bases = [r for r in rows if r["fold"] == "BASE"]
    out = []
    for v, col in V.items():
        for src in ("E", "RCOMP"):
            bs = [r for r in bases if r["is_rcomp"] == (src == "RCOMP") and r.get(col) is not None]
            if len(bs) < 10:
                continue
            w = np.array([r["strata"]["words"] for r in bs], float)
            f = np.array([float(r[col]) > 0.5 for r in bs], float)
            t1, t2 = np.percentile(w, [100 / 3, 200 / 3])
            terc = np.where(w <= t1, "T1", np.where(w <= t2, "T2", "T3"))
            nc = np.array([min(int(r["strata"].get("n_conditions") or 0), 5) for r in bs])
            rec = {"variant": v, "base_source": src, "n_bases": len(bs), "d_all": fnum(f.mean()),
                   "tercile_cuts_words": [fnum(t1, 1), fnum(t2, 1)]}
            for t in ("T1", "T2", "T3"):
                m = terc == t
                rec[f"d_{t}"] = fnum(f[m].mean()) if m.any() else None
                rec[f"n_{t}"] = int(m.sum())
            for k in sorted(set(nc)):
                m = nc == k
                rec[f"d_ncond_{k}{'+' if k == 5 else ''}"] = fnum(f[m].mean())
            if 0 < f.sum() < len(f):
                x = (w / 10.0).reshape(-1, 1)
                slope = LogisticRegression(C=1e6, max_iter=1000).fit(x, f).coef_[0][0]
                rng = np.random.default_rng(SEED)
                sl = []
                for _ in range(500):
                    i = rng.integers(0, len(f), len(f))
                    if 0 < f[i].sum() < len(i):
                        sl.append(LogisticRegression(C=1e6, max_iter=1000).fit(x[i], f[i]).coef_[0][0])
                rec.update(logit_slope_per10words=fnum(slope), slope_lo=fnum(np.percentile(sl, 2.5)),
                           slope_hi=fnum(np.percentile(sl, 97.5)), slope_boot=len(sl))
            out.append(rec)
    return out


def paired_cue_effect(rows: list[dict], V: dict) -> list[dict]:
    """Same bases, same families: cued (SIGPROXY / LOCAL2 own-signature) vs uncued (FREE3) base FA d and mutant recall;
    paired difference with a base bootstrap. Descriptive (proxy arms never decide a gate)."""
    pairs = [("SIGPROXY_K3", "FREE3_align"), ("SIGPROXY_K3", "FREE3_exact"), ("SIGPROXY_K3", "FREE3_lc"),
             ("SIGPROXY_graded", "FREE3_align"), ("LOCAL2_own_sig", "FREE3_align"), ("LOCAL2_own_sig", "FREE_c_align_exp8")]
    out = []
    for a, b in pairs:
        if a not in V or b not in V:
            continue
        ca, cb = V[a], V[b]
        for kind, fold in (("d_bases", "BASE"), ("recall_mutants", "PERTURB"), ("FA_equiv_rewrites", "PERTURB_CONTROL")):
            sel = [r for r in rows if r["fold"] == fold and r.get(ca) is not None and r.get(cb) is not None
                   and not (fold == "PERTURB_CONTROL" and r["op_label"].startswith("RENAME"))]
            if len(sel) < 5:
                continue
            fa = [float(r[ca] > 0.5) for r in sel]
            fb = [float(r[cb] > 0.5) for r in sel]
            cl = [r["base_item_id"] for r in sel]
            d, lo, hi = clustered([x - y for x, y in zip(fa, fb)], cl)
            out.append({"a": a, "b": b, "quantity": kind, "n": len(sel), "n_bases": len(set(cl)), "a_value": fnum(np.mean(fa)),
                        "b_value": fnum(np.mean(fb)), "a_minus_b": fnum(d), "lo": fnum(lo), "hi": fnum(hi)})
    return out


def symbol_roles(rows: list[dict]) -> dict:
    """Per row: role of every listed symbol (lower-case key) relative to its base signature."""
    base_sig = {r["base_item_id"]: {(n.lower(), a) for n, a in r["signature"]} for r in rows if r["fold"] == "BASE"}
    role_new = {"RENAME_SYN": "SYNONYM", "RENAME_NONCE": "NONCE", "MEANING_RENAME": "DONOR", "ADD_FOREIGN": "FOREIGN"}
    out = {}
    for r in rows:
        bs = base_sig[r["base_item_id"]]
        out[r["key"]] = [((n, a), "GENUINE" if (n.lower(), a) in bs else role_new.get(r["op_label"], "OTHER_NEW"))
                         for n, a in r["signature"]]
    return out


def local_anchor(rows: list[dict]) -> dict:
    """LOCAL2 (secondary): symbol usage by role, P(peer eq mutant | used the foreign/donor symbol), delta_anchor per
    operator with base-clustered CIs, and the within-base label-shuffle placebo."""
    import csc_lib as L
    peers = {(u["text"], u["sig_key"]): u["peers"] for u in jl(DATA / "peers_local2.jsonl")}
    if not peers:
        return {"status": "NOT_RUN"}
    roles = symbol_roles(rows)
    use = defaultdict(list)
    use_by_model = defaultdict(list)
    cond = defaultdict(lambda: [0, 0])
    fmt = Counter()
    for r in rows:
        ps = peers.get((r["text"], r["sig_key"]))
        if ps is None:
            continue
        for p in ps:
            fmt[(p["model"], p["format"], p["parse_ok"])] += 1
        pf = [p["fol"] for p in ps if p["parse_ok"]]
        if not pf:
            continue
        sig = [tuple(x[0]) for x in roles[r["key"]]]
        U = L.symbol_usage(sig, pf)
        pm = [p["model"] for p in ps if p["parse_ok"]]
        for (s, role), used in zip(roles[r["key"]], U):
            for u, m in zip(used, pm):
                use[role].append(u)
                use_by_model[(m, role)].append(u)
        if r["op_label"] in ("ADD_FOREIGN", "MEANING_RENAME"):
            for (s, role), used in zip(roles[r["key"]], U):
                if role in ("FOREIGN", "DONOR"):
                    for u, f in zip(used, pf):
                        if u:
                            eq = L.eq_exact(r["candidate_fol"], f) is True
                            cond[r["op_label"]][0] += eq
                            cond[r["op_label"]][1] += 1
    usage = {role: {"rate": fnum(np.mean(v)), "n": len(v)} for role, v in use.items()}
    usage_m = {f"{m}|{role}": {"rate": fnum(np.mean(v)), "n": len(v)} for (m, role), v in use_by_model.items()}
    # delta anchor (new-signature mutants and controls)
    dl = []
    # both peer sets must be usable (>= 2 parseable peers): an 'insufficient' 0.5 is not an endorsement
    sel_all = [r for r in rows if r.get("c_local") is not None and r.get("c_localbase") is not None and not r["sig_shared_with_base"]]
    sel = [r for r in sel_all if r.get("local_status") == "OK" and r.get("localbase_status") == "OK"]
    n_excluded = len(sel_all) - len(sel)
    for op in sorted({r["op_label"] for r in sel}):
        s = [r for r in sel if r["op_label"] == op]
        d_row = [float(r["c_local"] <= 0.5) - float(r["c_localbase"] <= 0.5) for r in s]
        d_share = [(1 - r["c_local"]) - (1 - r["c_localbase"]) for r in s]
        est, lo, hi = clustered(d_row, [r["base_item_id"] for r in s])
        est2, lo2, hi2 = clustered(d_share, [r["base_item_id"] for r in s])
        dl.append({"op_label": op, "n": len(s), "e_own_sig": fnum(np.mean([r["c_local"] <= 0.5 for r in s])),
                   "e_base_sig": fnum(np.mean([r["c_localbase"] <= 0.5 for r in s])),
                   "delta_anchor_rowlevel": fnum(est), "lo": fnum(lo), "hi": fnum(hi),
                   "delta_anchor_peershare": fnum(est2), "lo_share": fnum(lo2), "hi_share": fnum(hi2)})
    # placebo: permute op labels within base, recompute the per-op row-level delta
    rng = np.random.default_rng(SEED)
    by_base = defaultdict(list)
    for r in sel:
        by_base[r["base_item_id"]].append(r)
    perm_lab = {}
    for b, rs in by_base.items():
        labs = [r["op_label"] for r in rs]
        rng.shuffle(labs)
        for r, lab in zip(rs, labs):
            perm_lab[r["key"]] = lab
    plc = []
    for op in sorted(set(perm_lab.values())):
        s = [r for r in sel if perm_lab[r["key"]] == op]
        plc.append({"op_label_permuted": op, "n": len(s),
                    "delta_anchor_rowlevel": fnum(np.mean([float(r["c_local"] <= 0.5) - float(r["c_localbase"] <= 0.5) for r in s]))})
    # base endorsement and sanity
    bases = [r for r in rows if r["fold"] == "BASE" and r.get("c_local") is not None]
    lstat = Counter(r.get("local_status") for r in rows if r.get("c_local") is not None)
    return {"status": "OK", "peers": ["local/qwen2.5-1.5b-instruct-q4km", "local/gemma-2-2b-it-q4km"],
            "n_rows_scored": sum(lstat.values()), "row_status_counts": dict(lstat),
            "delta_anchor_rows_used": len(sel), "delta_anchor_rows_excluded_insufficient": n_excluded,
            "n_bases": len(bases), "base_endorsement_rate": fnum(np.mean([r["c_local"] <= 0.5 for r in bases])) if bases else None,
            "base_endorsement_rate_excl_insufficient": fnum(np.mean([r["c_local"] <= 0.5 for r in bases if r.get("local_status") == "OK"]))
            if any(r.get("local_status") == "OK" for r in bases) else None,
            "n_bases_sufficient": sum(r.get("local_status") == "OK" for r in bases),
            "format_counts": {f"{m}|{f}|parse_ok={p}": n for (m, f, p), n in sorted(fmt.items())},
            "symbol_usage_by_role": usage, "symbol_usage_by_model_role": usage_m,
            "p_peer_eq_mutant_given_used_new_symbol": {k: {"rate": fnum(v[0] / v[1]) if v[1] else None, "n": v[1]} for k, v in cond.items()},
            "delta_anchor": dl, "placebo_within_base_label_shuffle": plc,
            "caveat": "secondary arm with 1.5-2B local peers; NOT the pre-registered peers; no gate verdict"}


# ============================================================================================ PART 2 controls
def part2(rows: list[dict], V: dict) -> list[dict]:
    base = {v: {r["base_item_id"]: r.get(col) for r in rows if r["fold"] == "BASE"} for v, col in V.items()}
    out = []
    ctls = [r for r in rows if r["fold"] == "PERTURB_CONTROL"]
    for v, col in V.items():
        for ct in CONTROLS + ["ALL_RENAME", "ALL_EQUIV_REWRITE"]:
            for src in ("E", "RCOMP", "ALL"):
                sel = [r for r in ctls if (r["op_label"] == ct or (ct == "ALL_RENAME" and r["op_label"].startswith("RENAME"))
                                           or (ct == "ALL_EQUIV_REWRITE" and not r["op_label"].startswith("RENAME")))
                       and (src == "ALL" or r["is_rcomp"] == (src == "RCOMP"))]
                have = [r for r in sel if r.get(col) is not None and base[v].get(r["base_item_id"]) is not None]
                if not have:
                    continue
                cl = [r["base_item_id"] for r in have]
                fc = [float(float(r[col]) > 0.5) for r in have]
                fb = [float(float(base[v][r["base_item_id"]]) > 0.5) for r in have]
                fa, fa_lo, fa_hi = clustered(fc, cl)
                bfa, _, _ = clustered(fb, cl)
                dif, d_lo, d_hi = clustered([a - b for a, b in zip(fc, fb)], cl)
                fl, fl_lo, fl_hi = clustered([abs(a - b) for a, b in zip(fc, fb)], cl)
                stc = col.replace("c_", "") + "_status"
                n_ins = sum(1 for r in have if str(r.get(stc, "")).startswith("csc_insuff"))
                out.append({"variant": v, "control_type": ct, "base_source": src, "n": len(have), "n_na": len(sel) - len(have),
                            "n_insufficient": n_ins,
                            "FA_gt05": fnum(fa), "FA_lo": fnum(fa_lo), "FA_hi": fnum(fa_hi),
                            "FA_eq1": fnum(np.mean([float(r[col]) >= 1 - 1e-9 for r in have])),
                            "FA_gt0": fnum(np.mean([float(r[col]) > 1e-9 for r in have])),
                            "paired_base_FA": fnum(bfa), "FA_minus_base": fnum(dif), "diff_lo": fnum(d_lo), "diff_hi": fnum(d_hi),
                            "flip_rate": fnum(fl), "flip_lo": fnum(fl_lo), "flip_hi": fnum(fl_hi)})
    return out


# ============================================================================================ PART 3 typing
def part3(rows: list[dict]) -> dict:
    by = {r["key"]: r for r in rows}
    srch = defaultdict(dict)
    for x in jl(RES / "typing_search_rows.jsonl"):
        srch[x["key"]][x["which"]] = x
    muts = [r for r in rows if r["fold"] == "PERTURB"]
    targets = ["oracle", "csc", "proxy", "free3"]
    per_row = []
    for r in muts:
        true = "ADD" if r["operator"] == "ADD" else r["operator"]
        rec = {"key": r["key"], "base_item_id": r["base_item_id"], "sentence_id": r["sentence_id"], "is_rcomp": r["is_rcomp"],
               "true": true, "op_label": r["op_label"], "polarity": r["polarity"]}
        maj_status = {"csc": r.get("csc_majority_status"), "proxy": r.get("proxy_majority_status"),
                      "free3": r.get("free3_majority_status"), "oracle": "TRUE_REFERENCE"}
        for t in targets:
            x = srch[r["key"]].get(t)
            if x is None:
                if t != "oracle" and maj_status[t] is None:
                    pred = None  # target not available for this row (arm not run / not applicable)
                else:
                    pred = "NO_TARGET"
                rec[f"{t}_pred"] = pred
                rec[f"{t}_cls"] = maj_status[t]
                rec[f"{t}_strict"] = False if pred == "NO_TARGET" else None
                rec[f"{t}_lenient"] = False if pred == "NO_TARGET" else None
                rec[f"{t}_found"] = False if pred == "NO_TARGET" else None
                continue
            ops = x.get("ops") or []
            mapped = [TYPING_MAP.get(o, o) for o in ops]
            if x["cls"] == "EQUIV":
                pred = "NONE(equivalent)"
            elif not mapped:
                pred = x["cls"]
            else:
                pred = mapped[0] if len(mapped) == 1 else "+".join(sorted(mapped))
            rec[f"{t}_pred"] = pred
            rec[f"{t}_cls"] = x["cls"]
            rec[f"{t}_strict"] = len(mapped) == 1 and mapped[0] == true
            rec[f"{t}_lenient"] = true in mapped
            rec[f"{t}_found"] = bool(mapped)
            rec[f"{t}_secs"] = x.get("secs")
        per_row.append(rec)
    with (RES / "typing_rows_csc.jsonl").open("w") as f:
        for x in per_row:
            f.write(json.dumps(x) + "\n")
    table, conf = [], Counter()
    for t in targets:
        for src in ("E", "RCOMP", "ALL"):
            rs = [x for x in per_row if x[f"{t}_pred"] is not None and (src == "ALL" or x["is_rcomp"] == (src == "RCOMP"))]
            if not rs:
                continue
            for op in sorted({x["true"] for x in rs}) + ["ALL", "ALL_excl_MEANING_RENAME"]:
                s = [x for x in rs if op == "ALL" or (op == "ALL_excl_MEANING_RENAME" and x["true"] != "MEANING_RENAME") or x["true"] == op]
                if not s:
                    continue
                acc, lo, hi = clustered([float(x[f"{t}_strict"]) for x in s], [x["sentence_id"] for x in s])
                table.append({"target": t, "base_source": src, "true_op": op, "n": len(s), "strict": fnum(acc), "lo": fnum(lo),
                              "hi": fnum(hi), "lenient": fnum(np.mean([x[f"{t}_lenient"] for x in s])),
                              "repair_found": fnum(np.mean([x[f"{t}_found"] for x in s])),
                              "no_target": fnum(np.mean([x[f"{t}_pred"] == "NO_TARGET" for x in s])),
                              "equiv_to_target": fnum(np.mean([x[f"{t}_pred"] == "NONE(equivalent)" for x in s])),
                              "oracle_strict_same_rows": fnum(np.mean([bool(x["oracle_strict"]) for x in s])),
                              "majority_class_acc_same_rows": fnum(max(Counter(x["true"] for x in s).values()) / len(s))})
            for x in rs:
                conf[(t, src, x["true"], x[f"{t}_pred"])] += 1
    with (RES / "typing_confusion_csc.csv").open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["target", "base_source", "true_op", "pred", "n"])
        for (t, src, a, p), n in sorted(conf.items()):
            if src != "ALL":
                w.writerow([t, src, a, p, n])
    write_csv(RES / "typing_csc.csv", table)
    e8 = json.loads((E8 / "results" / "analysis_typing.json").read_text())
    E_mut = [x for x in per_row if not x["is_rcomp"]]
    ops_true = Counter(x["true"] for x in E_mut)
    ref = {"source": str(E8 / "results" / "analysis_typing.json"), "majority_class": e8["majority_class"],
           "majority_acc_exp8": e8["majority_acc"], "marginal_chance_exp8": e8["marginal_chance"],
           "medoid_align_exp8": e8["verdict"]["medoid_align"], "judge_flashlite_exp8": e8["verdict"]["judge_cheap"],
           "judge_local_qwen8b_exp8": e8["verdict"]["judge_local"], "oracle_strict_exp8": e8["oracle_strict_acc"],
           "majority_acc_recomputed": fnum(max(ops_true.values()) / len(E_mut)),
           "chance_recomputed": fnum(sum((v / len(E_mut)) ** 2 for v in ops_true.values()))}
    return {"table": table, "reference_baselines": ref}


# ============================================================================================ PART 4 R_COMP
def part4_sig() -> dict:
    import auc_tools as AT
    sig_view = {r["row_key"]: r for r in jl(DATA / "rcomp_sig_view.jsonl")}
    sc = {r["key"][4:]: r for r in jl(RES / "scores_raw.jsonl") if r["key"].startswith("SIG:")}
    rows = []
    for x in jl(E7 / "results" / "analysis_rows_SIG.jsonl"):
        if x["label"] not in ("CORRECT", "ERROR"):
            continue
        s = sc.get(x["row_key"], {})
        v = sig_view.get(x["row_key"], {})
        rows.append({**x, "c_proxy": s.get("c_proxy"), "c_proxy_k4": s.get("c_proxy_k4"), "c_proxy_graded": s.get("c_proxy_graded"),
                     "proxy_status": s.get("proxy_status"), "matched_reading": v.get("matched_reading"), "family": v.get("family")})
    metrics = ["c_proxy", "c_proxy_k4", "c_proxy_graded", "c_score_sig", "g_align", "judge_cheap_disg", "judge_cheap_orig",
               "judge_local_disg", "judge_local_orig"]

    def auc_on(rs, m, weights=None):
        sc_ = np.array([r[m] for r in rs], float)
        y = np.array([r["label"] == "ERROR" for r in rs])
        tmpl = np.array([r["template_id"] for r in rs])
        sids = sorted({r["sentence_id"] for r in rs})
        cid = {s: i for i, s in enumerate(sids)}
        cl = np.array([cid[r["sentence_id"]] for r in rs])
        return AT.StratAUC(sc_, y, tmpl, cl), cl, sids

    out = {"pool": {"n": len(rows), "n_error": sum(r["label"] == "ERROR" for r in rows),
                    "n_sentences": len({r["sentence_id"] for r in rows})}, "auroc_within_template": {}, "paired_delta": {}}
    for m in metrics:
        rs = [r for r in rows if r.get(m) is not None]
        if len(rs) < 20:
            continue
        sa, cl, sids = auc_on(rs, m)
        tmpl_of = {}
        for r in rs:
            tmpl_of[r["sentence_id"]] = r["template_id"]
        W = AT.boot_weights(np.array([tmpl_of[s] for s in sids]), B, SEED)
        bs = np.array([sa.value(W[b]) for b in range(B)])
        out["auroc_within_template"][m] = {"n": len(rs), **AT.summarize(sa.value(), bs)}
    for a in ("c_proxy", "c_proxy_k4", "c_proxy_graded"):
        for bm in ("c_score_sig", "g_align", "judge_cheap_disg", "judge_cheap_orig", "judge_local_disg", "judge_local_orig"):
            rs = [r for r in rows if r.get(a) is not None and r.get(bm) is not None]
            if len(rs) < 20:
                continue
            sa, cl, sids = auc_on(rs, a)
            sb, _, _ = auc_on(rs, bm)
            tmpl_of = {r["sentence_id"]: r["template_id"] for r in rs}
            W = AT.boot_weights(np.array([tmpl_of[s] for s in sids]), B, SEED)
            d = np.array([sa.value(W[b]) - sb.value(W[b]) for b in range(B)])
            out["paired_delta"][f"{a}_minus_{bm}"] = {"n": len(rs), "auroc_a": fnum(sa.value()), "auroc_b": fnum(sb.value()),
                                                      **AT.summarize(sa.value() - sb.value(), d),
                                                      "p_one_sided_le0": fnum(float(np.mean(d <= 0)), 4)}
    # e / d at c > 0.5 for proxy and c_score_sig (same rows)
    ed = {}
    for m in ("c_proxy", "c_proxy_k4", "c_score_sig"):
        rs = [r for r in rows if r.get(m) is not None]
        err = [r for r in rs if r["label"] == "ERROR"]
        cor = [r for r in rs if r["label"] == "CORRECT"]
        rec = {"n": len(rs), "e_error_endorsed": fnum(np.mean([r[m] <= 0.5 for r in err])),
               "d_correct_flagged": fnum(np.mean([r[m] > 0.5 for r in cor]))}
        for mr in ("weak", "strong"):
            s = [r for r in cor if r.get("matched_reading") == mr]
            rec[f"d_{mr}"] = fnum(np.mean([r[m] > 0.5 for r in s])) if s else None
            rec[f"n_correct_{mr}"] = len(s)
        ed[m] = rec
    out["e_d_at_0.5"] = ed
    out["status_counts_proxy"] = dict(Counter(r.get("proxy_status") for r in rows))
    out["note"] = ("SIGPROXY = exp-7 SIG outputs of deepseek-v3.2 / phi-4 / gpt-4.1-mini (+qwen3-235b for K4), cued with the "
                   "closed template signature; family-disjoint K3/K4 rule; exact case-insensitive z3 equivalence. A k=3 "
                   "ablation of signature-cued consensus, NOT CSC with the candidate's own open list. Development evidence "
                   "in a controlled-vocabulary regime the user excluded; never a headline.")
    (RES / "rcomp_sig_csc.json").write_text(json.dumps(out, indent=1))
    return out


def part4_free() -> dict:
    """Label-free FREE statistics (firewalled view only). CSC FREE peers were NOT generated (D-BUDGET)."""
    import csc_lib as L
    free = jl(DATA / "rcomp_free_view.jsonl")
    by = defaultdict(list)
    for r in free:
        if r["prompt_variant"] == "fewshot_v1":
            by[r["sentence_id"]].append(r)
    res = {}
    for mode in ("free_align_class_id", "free_hyb_class_id"):
        per_t = defaultdict(lambda: [0, 0])
        for sid, rs in by.items():
            rs = [r for r in rs if r[mode] is not None]
            for i in range(len(rs)):
                for j in range(i + 1, len(rs)):
                    t = rs[i]["template_id"]
                    per_t[t][0] += rs[i][mode] == rs[j][mode]
                    per_t[t][1] += 1
        tot = [sum(v[0] for v in per_t.values()), sum(v[1] for v in per_t.values())]
        res[mode] = {"pairwise_equiv_rate": fnum(tot[0] / tot[1]), "n_pairs": tot[1],
                     "by_template": {t: fnum(v[0] / v[1]) for t, v in sorted(per_t.items())}}
    # SIGPROXY peer-peer exact agreement on SIG sentences (reference level of cued agreement)
    sig = jl(DATA / "rcomp_sig_view.jsonl")
    ps = defaultdict(dict)
    for r in sig:
        if r["slot"] in ("G4", "G6", "G7"):
            ps[r["sentence_id"]][r["slot"]] = r["candidate_fol"] if r.get("parse_ok") else None
    agree = []
    ncls = Counter()
    for sid, d in ps.items():
        f = [d.get(s) for s in ("G4", "G6", "G7")]
        pp = [L.prep(x) for x in f if x]
        pp = [x for x in pp if x is not None]
        if len(pp) < 2:
            continue
        pairs = [(i, j) for i in range(len(pp)) for j in range(i + 1, len(pp))]
        agree.append(np.mean([L.eq_prepped(pp[i], pp[j]) is True for i, j in pairs]))
        ncls[L.peer_majority([x for x in f if x]).get("n_classes")] += 1
    res["sigproxy_peer_peer_exact_agreement_on_SIG"] = {"mean": fnum(np.mean(agree)), "n_sentences": len(agree),
                                                        "n_classes_distribution": dict(ncls),
                                                        "label_free_d_proxy": fnum(1 - np.mean(agree))}
    res["csc_free_cache"] = "NOT GENERATED: OpenRouter run budget exhausted before the first peer call (D-BUDGET); the job " \
                            "manifest results/csc_job_manifest.json lists every (text, signature, model) job for iteration 5"
    res["firewall"] = "only whitelisted FREE fields were read (see results/firewall.json); no FREE label was read"
    (RES / "rcomp_free_labelfree.json").write_text(json.dumps(res, indent=1))
    return res


# ============================================================================================ PART 5 cost
def part5(rows: list[dict]) -> list[dict]:
    pil = json.loads((E9 / "results" / "pilot.json").read_text())["per_model"]
    out = []
    for m, d in pil.items():
        out.append({"item": f"per_call_mean_usd[{m}]", "value": fnum(d["usd_per_call"], 7), "unit": "USD/call",
                    "source": "sibling exp 9 pilot (identical CSC block template, same model ids), results/pilot.json"})
        out.append({"item": f"per_call_mean_secs[{m}]", "value": fnum(d["secs_per_call"], 2), "unit": "s/call", "source": "exp 9 pilot"})
    k3 = ["deepseek/deepseek-v3.2", "microsoft/phi-4", "openai/gpt-4.1-mini"]
    full_k3 = sum(pil[m]["usd_per_call"] for m in k3)
    full_k4 = full_k3 + pil["qwen/qwen3-235b-a22b-2507"]["usd_per_call"]
    out += [{"item": "CSC FULL per candidate K3 (projected)", "value": fnum(full_k3, 6), "unit": "USD/candidate",
             "source": "sum of exp-9 per-call means"},
            {"item": "CSC FULL per candidate K4 (projected)", "value": fnum(full_k4, 6), "unit": "USD/candidate", "source": "idem"},
            {"item": "CSC FULL API seconds per candidate K3, parallel calls (max)", "value": fnum(max(pil[m]["secs_per_call"] for m in k3), 2),
             "unit": "s/candidate", "source": "exp 9 pilot"},
            {"item": "CSC FULL API seconds per candidate K3, serial (sum)", "value": fnum(sum(pil[m]["secs_per_call"] for m in k3), 2),
             "unit": "s/candidate", "source": "exp 9 pilot"}]
    uniq = jl(DATA / "unique_sigs_perturb.jsonl")
    out.append({"item": "amortised per PERTURB row (projected; amortised, not deployable)",
                "value": fnum(full_k4 * len(uniq) / len(rows), 6), "unit": "USD/row",
                "source": f"{len(uniq)} unique signatures x K4 / {len(rows)} rows"})
    # SIGPROXY actual peer cost (exp-7 SIG generation cost of the G4/G6/G7 outputs of the sentence)
    cost = defaultdict(float)
    for r in jl(DATA / "rcomp_sig_view.jsonl"):
        if r["slot"] in ("G4", "G6", "G7"):
            cost[r["sentence_id"]] += float(r.get("cost_usd") or 0.0)
    v = np.array(list(cost.values()))
    out += [{"item": "SIGPROXY FULL per candidate K3 (actual exp-7 cost), median", "value": fnum(np.median(v), 6), "unit": "USD/candidate",
             "source": "exp 7 rcomp_candidates.jsonl cost_usd"},
            {"item": "SIGPROXY FULL per candidate K3 (actual), p90", "value": fnum(np.percentile(v, 90), 6), "unit": "USD/candidate",
             "source": "idem"}]
    secs = [r.get("secs_csc") for r in rows if r.get("secs_csc") is not None and r.get("c_proxy") is not None]
    secs_f3 = [r.get("secs_free3") for r in rows if r.get("secs_free3")]
    out += [{"item": "MARGINAL z3 CPU seconds per candidate (SIGPROXY K3+K4+multi+graded), median", "value": fnum(np.median(secs), 3),
             "unit": "CPU s", "source": "results/scores_raw.jsonl secs_csc"},
            {"item": "MARGINAL z3 CPU seconds per candidate, p90", "value": fnum(np.percentile(secs, 90), 3), "unit": "CPU s", "source": "idem"},
            {"item": "FREE3 exact+align+lc CPU seconds per candidate, median", "value": fnum(np.median(secs_f3), 3), "unit": "CPU s",
             "source": "results/scores_raw.jsonl secs_free3"},
            {"item": "G5 reference: FULL <= $0.002 per candidate", "value": "PASS (projected)" if full_k3 <= 0.002 else "FAIL (projected)",
             "unit": "", "source": "projection from sibling-measured prices; no CSC call ran here"},
            {"item": "API spend of THIS artifact", "value": fnum(sum(float(json.loads(x).get("cost_usd") or 0) for x in
                                                                     (RES / "api_cost_ledger.jsonl").read_text().splitlines() if x.strip()), 7),
             "unit": "USD", "source": "results/api_cost_ledger.jsonl"}]
    write_csv(RES / "cost_table.csv", out)
    return out


def write_csv(p: Path, rows: list[dict]) -> None:
    if not rows:
        p.write_text("")
        return
    keys = []
    for r in rows:
        for k in r:
            if k not in keys:
                keys.append(k)
    with p.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow({k: (json.dumps(v) if isinstance(v, (list, dict)) else v) for k, v in r.items()})


def sanity(rows: list[dict]) -> dict:
    """(i) signature-preserving mutants of a SIGPROXY-endorsed base must NOT be endorsed by the same peers (they are
    non-equivalent to the base; a peer equivalent to both would imply base == mutant); (ii) z3-equivalent controls of a
    sig-preserving type keep the base's SIGPROXY verdict; (iii) every mutant non-equivalent to its reference."""
    import csc_lib as L
    base = {r["base_item_id"]: r for r in rows if r["fold"] == "BASE"}
    viol = []
    n_chk = 0
    for r in rows:
        if r["fold"] == "PERTURB" and r["sig_shared_with_base"] and r.get("c_proxy") is not None:
            b = base[r["base_item_id"]]
            if b.get("proxy_per_peer") and r.get("proxy_per_peer"):
                for pb, pm in zip(b["proxy_per_peer"], r["proxy_per_peer"]):
                    n_chk += 1
                    if pb is True and pm is True:
                        viol.append(r["key"])
    keep = []
    for r in rows:
        if r["fold"] == "PERTURB_CONTROL" and r["sig_shared_with_base"] and r.get("proxy_per_peer") is not None:
            b = base[r["base_item_id"]]
            if b.get("proxy_per_peer"):
                keep.append(r["proxy_per_peer"] == b["proxy_per_peer"])
    mut_eq = sum(1 for r in rows if r["fold"] == "PERTURB" and L.eq_exact(r["candidate_fol"], r["reference_fol"]) is True)
    ctl_neq = sum(1 for r in rows if r["fold"] == "PERTURB_CONTROL" and not r["op_label"].startswith("RENAME")
                  and L.eq_exact(r["candidate_fol"], base[r["base_item_id"]]["candidate_fol"]) is not True)
    return {"peer_endorses_both_base_and_sigpreserving_mutant": len(viol), "n_peer_checks": n_chk, "examples": viol[:5],
            "sigpreserving_controls_keep_base_per_peer_verdicts": fnum(np.mean(keep)) if keep else None, "n_controls": len(keep),
            "mutants_equivalent_to_reference_same_vocab": mut_eq,
            "nonrename_controls_not_equivalent_to_base": ctl_neq}


def main() -> None:
    h = csc_prereg.verify()
    logger.info(f"prereg sha256 verified: {h}")
    rows, meta = load_rows()
    V = variants(rows)
    logger.info(f"rows {len(rows)}; variants {list(V)}; {meta}")
    a1 = part1(rows, V)
    write_csv(RES / "anchoring.csv", a1)
    dl = d_by_length(rows, V)
    write_csv(RES / "d_by_length.csv", dl)
    write_csv(RES / "paired_cue_effect.csv", paired_cue_effect(rows, V))
    loc = local_anchor(rows)
    (RES / "local2_anchoring.json").write_text(json.dumps(loc, indent=1))
    a2 = part2(rows, V)
    write_csv(RES / "controls_fa.csv", a2)
    ty = part3(rows)
    (RES / "typing_summary.json").write_text(json.dumps(ty["reference_baselines"], indent=1))
    sg = part4_sig()
    fr = part4_free()
    co = part5(rows)
    san = sanity(rows)
    (RES / "sanity_checks.json").write_text(json.dumps(san, indent=1))
    logger.info(f"sanity: {san}")
    gates(a1, a2, ty, co, loc, sg)
    logger.info("analysis done")


def pick(rows, **kw):
    for r in rows:
        if all(r.get(k) == v for k, v in kw.items()):
            return r
    return None


def gates(a1, a2, ty, co, loc, sg) -> None:
    csc_ran = any(r["variant"].startswith("CSC_") for r in a1)
    g = {"prereg": "results/prereg_csc_P.json", "csc_peers_generated": csc_ran}
    if not csc_ran:
        why = "UNTESTED: no CSC peer could be generated (OpenRouter run budget exhausted before the first call; D-BUDGET)"
        g["G3_P"] = {"verdict": why}
        g["G4"] = {"verdict": why, "free_peer_comparator_e_exp8_c_align_E": {
            op: pick(a1, variant="FREE_c_align_exp8", op_label=op, polarity="ALL", base_source="E") for op in
            ("ADD_FOREIGN", "ADD_INTERNAL", "DROP", "MEANING_RENAME")}}
        g["MT"] = {"verdict": why, "oracle_samevocab_E_ALL": pick(ty["table"], target="oracle", base_source="E", true_op="ALL")}
    g["G5"] = {"verdict": pick(co, item="G5 reference: FULL <= $0.002 per candidate")["value"],
               "full_k3_usd": pick(co, item="CSC FULL per candidate K3 (projected)")["value"], "source": "results/cost_table.csv"}
    g["descriptive_not_gates"] = {
        "SIGPROXY_rcomp_recall_sigpreserving_mutants": [r for r in a1 if r["variant"] == "SIGPROXY_K3" and r["polarity"] == "ALL"
                                                          and r["base_source"] == "RCOMP"],
        "SIGPROXY_rcomp_base_FA": [r for r in a2 if r["variant"] == "SIGPROXY_K3" and r["base_source"] == "RCOMP"],
        "SIGPROXY_typing_rcomp": [r for r in ty["table"] if r["target"] == "proxy" and r["base_source"] == "RCOMP" and r["true_op"] in ("ALL", "ALL_excl_MEANING_RENAME")],
        "SIG_k3_ablation_auroc": sg["auroc_within_template"],
        "LOCAL2": {k: loc.get(k) for k in ("status", "symbol_usage_by_role", "delta_anchor")}}
    (RES / "csc_gate_P.json").write_text(json.dumps(g, indent=1))


if __name__ == "__main__":
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(ROOT / "logs" / "csc_analysis.log", rotation="30 MB", level="DEBUG")
    main()
