"""PART 3 (M4): peer-count scaling AUROC(k), fixed 3-family pools (in-sample + cross-fitted on exp 6 folds_E),
leave-one-family-out, and $ / CPU-seconds per sentence at each k."""
from __future__ import annotations

import hashlib
import json
import random
from collections import defaultdict
from itertools import combinations

import numpy as np
import pandas as pd
from loguru import logger

from consensus_mx import c_from_fams
from stats import SentBoot, WAuc, WStratAuc, auc, ci, strat_auc

N_DRAWS = 50


def _draw(row_key: str, k: int, j: int, fams: list[str]) -> list[str]:
    seed = int(hashlib.sha1(f"M4|{row_key}|{k}|{j}".encode()).hexdigest(), 16)
    return random.Random(seed).sample(sorted(fams), k)


def auroc_k(P: pd.DataFrame, boot: SentBoot, fam_col: str, all_fams: list[str], k_max: int, primary: bool = True,
            b_ci: int = 2000) -> dict:
    """AUROC(k) over 50 reproducible random k-subsets of each candidate's available other families.
    primary=True: constant population = rows with all k_max other families available; else rows with >=2 available and
    k capped at the available count (share capped reported)."""
    avail = P[fam_col].apply(lambda fs: sorted(fs.keys()))
    n_av = avail.apply(len).values
    mask = (n_av == k_max) if primary else (n_av >= 2)
    d = P[mask]
    av = avail[mask].values
    fs = d[fam_col].values
    y = d.y_AB.values.astype(int)
    strata = d.stratum.values
    W = boot.W(np.asarray(mask))[:b_ci]
    terc = d.words_t.values
    res = {"population": "all K_max families available" if primary else ">=2 families available (k capped)",
           "n": int(len(d)), "n_err": int(y.sum()), "n_cor": int((1 - y).sum()), "n_sent": int(d.sentence_id.nunique()), "k": {}}
    full_c = None
    for k in range(1, k_max + 1):
        draws_pooled, draws_strat, draws_maj, draws_terc = [], [], [], defaultdict(list)
        wb_sum = np.zeros(W.shape[0])
        capped = np.array([len(a) < k for a in av])
        for j in range(N_DRAWS):
            c = np.empty(len(d))
            for i in range(len(d)):
                kk = min(k, len(av[i]))
                sel = _draw(d.row_key.values[i], kk, j, av[i])
                c[i] = c_from_fams(fs[i], sel)
            draws_pooled.append(auc(y, c))
            draws_strat.append(strat_auc(y, c, strata))
            draws_maj.append(auc(y, (c >= 0.5).astype(float)))  # END_MAJ-at-k: endorsed iff eq_frac > 1/2 (c < 0.5)
            for t in ("T1", "T2", "T3"):
                m = terc == t
                draws_terc[t].append(auc(y[m], c[m]))
            wa = WAuc(y, c)
            wb_sum += np.array([wa(W[b]) for b in range(W.shape[0])])
            if k == k_max and j == 0:
                full_c = c.copy()
        wb_mean = wb_sum / N_DRAWS
        res["k"][k] = {"auroc_mean": float(np.mean(draws_pooled)), "draw_band": [float(np.percentile(draws_pooled, 2.5)),
                                                                                   float(np.percentile(draws_pooled, 97.5))],
                       "auroc_ci_of_draw_mean": ci(wb_mean), "strat_auroc_mean": float(np.mean(draws_strat)),
                       "endmaj_auroc_mean": float(np.mean(draws_maj)),
                       "tercile_auroc_mean": {t: float(np.mean(v)) for t, v in draws_terc.items()},
                       "share_capped": float(capped.mean())}
        logger.info(f"M4 {fam_col} primary={primary} k={k}: AUROC {res['k'][k]['auroc_mean']:.4f}")
    top = res["k"][k_max]["auroc_mean"]
    res["k95"] = next((k for k in range(1, k_max + 1) if res["k"][k]["auroc_mean"] >= 0.95 * top), None)
    res["k95_tercile"] = {}
    for t in ("T1", "T2", "T3"):
        tt = res["k"][k_max]["tercile_auroc_mean"][t]
        res["k95_tercile"][t] = next((k for k in range(1, k_max + 1) if res["k"][k]["tercile_auroc_mean"][t] >= 0.95 * tt), None)
    res["M4_verdict"] = "CONFIRMED" if (res["k95"] is not None and res["k95"] <= 5) else "REFUTED"
    return res


def pool_scores(P: pd.DataFrame, fam_col: str, pool: tuple, neutral: float) -> np.ndarray:
    """Consensus of each candidate against the rows of the fixed pool S minus its own family (None -> neutral)."""
    out = np.empty(len(P))
    for i, (fs, own) in enumerate(zip(P[fam_col].values, P.family_vendor.values)):
        v = c_from_fams(fs, [f for f in pool if f != own])
        out[i] = neutral if v is None else v
    return out


def fixed_pools(P: pd.DataFrame, fam_col: str, all_fams: list[str], neutral: float, size: int, fold: np.ndarray) -> dict:
    y = P.y_AB.values.astype(int)
    pools = list(combinations(sorted(all_fams), size))
    sc = {p: pool_scores(P, fam_col, p, neutral) for p in pools}
    tab = sorted(((p, auc(y, sc[p]), strat_auc(y, sc[p], P.stratum.values)) for p in pools), key=lambda x: -x[1])
    oof = np.empty(len(P))
    picks = []
    for f in sorted(np.unique(fold)):
        tr, te = fold != f, fold == f
        best = max(pools, key=lambda p: (auc(y[tr], sc[p][tr]), p))
        picks.append({"fold": int(f), "pool": "+".join(best), "train_auroc": auc(y[tr], sc[best][tr]),
                      "test_auroc": auc(y[te], sc[best][te])})
        oof[te] = sc[best][te]
    cnt = defaultdict(int)
    for pk in picks:
        cnt[pk["pool"]] += 1
    return {"size": size, "n_pools": len(pools),
            "table": [{"pool": "+".join(p), "auroc": a, "strat_auroc": s} for p, a, s in tab],
            "in_sample_best": {"pool": "+".join(tab[0][0]), "auroc": tab[0][1]},
            "in_sample_worst": {"pool": "+".join(tab[-1][0]), "auroc": tab[-1][1]},
            "crossfit": {"oof_auroc": auc(y, oof), "oof_strat_auroc": strat_auc(y, oof, P.stratum.values), "picks": picks,
                         "pick_counts": dict(cnt)}, "oof_scores": oof}


def lofo(P: pd.DataFrame, boot: SentBoot, fam_col: str, all_fams: list[str], neutral: float, judge_bar: float) -> dict:
    """Leave-one-family-out: remove family f from every candidate's peers (>=2 remaining rows required, else neutral)."""
    y = P.y_AB.values.astype(int)
    W = boot.W(P.in_RAB.values) if len(P) == P.in_RAB.sum() else boot.W()

    def score(excl):
        out = np.empty(len(P))
        for i, fs in enumerate(P[fam_col].values):
            keep = [f for f in fs if f != excl]
            n = sum(fs[f][0] for f in keep)
            out[i] = neutral if n < 2 else c_from_fams(fs, keep)
        return out
    full = score(None)
    wa_full = WAuc(y, full)
    res = {"full_auroc": auc(y, full), "families": {}}
    for f in sorted(all_fams):
        s = score(f)
        for nm, m in (("all_rows", np.ones(len(P), bool)), ("rows_not_from_f", P.family_vendor.values != f)):
            wa1, wa0 = WAuc(y[m], s[m]), WAuc(y[m], full[m])
            dB = [wa1(W[b][m]) - wa0(W[b][m]) for b in range(W.shape[0])]
            res["families"].setdefault(f, {})[nm] = {"n": int(m.sum()), "auroc_lofo": auc(y[m], s[m]), "auroc_full": auc(y[m], full[m]),
                                                      "delta": auc(y[m], s[m]) - auc(y[m], full[m]), "delta_ci": ci(dB)}
    ok = all(v["all_rows"]["delta_ci"][0] > -0.03 and v["all_rows"]["auroc_lofo"] > judge_bar for v in res["families"].values())
    res["rule"] = f"no single family carries the effect iff every LOFO dAUROC CI lower bound > -0.03 AND every LOFO AUROC > {judge_bar}"
    res["verdict"] = "NO_SINGLE_FAMILY_CARRIES_EFFECT" if ok else "SOME_FAMILY_MATTERS"
    res["min_delta"] = min(v["all_rows"]["delta"] for v in res["families"].values())
    res["min_delta_family"] = min(res["families"], key=lambda f: res["families"][f]["all_rows"]["delta"])
    return res


def cost_table(gen_path, fam_map: dict, pair_secs: np.ndarray, rows_per_family: float, k_max: int, frontier: dict,
               pools: list[str]) -> dict:
    """$ per sentence per family (few-shot; zero-shot separately) from the dataset-E generation ledger, expected cost of a
    random k-subset, CPU-seconds from matrix pair timings."""
    cost = defaultdict(float)
    slot_cost = defaultdict(float)
    slot_sents = defaultdict(set)
    tok = defaultdict(list)
    sents = set()
    zs = defaultdict(float)
    n_calls = defaultdict(int)
    with open(gen_path) as fh:
        for line in fh:
            r = json.loads(line)
            fam = fam_map.get(r.get("slot"))
            if fam is None or "never_peer" in str(fam):
                continue
            sents.add(r["sentence_id"])
            c = r.get("cost_usd") or (r.get("usage") or {}).get("cost") or 0.0
            if r.get("prompt_variant") == "fewshot_v1":
                cost[fam] += c
                slot_cost[r["slot"]] += c
                slot_sents[r["slot"]].add(r["sentence_id"])
                n_calls[fam] += 1
                tok[fam].append((r.get("usage") or {}).get("completion_tokens") or 0)
            else:
                zs[f"{fam}|{r.get('prompt_variant')}"] += c
    S = len(sents)
    # slots cover 200-700 sentences (F: 200; G1b/G4/G5/G7/G8: 600), so each slot is costed per sentence IT covered and a
    # family's cost = sum of its few-shot slots' per-sentence costs (= cost of all its slots on one sentence)
    per_slot = {s: slot_cost[s] / len(slot_sents[s]) for s in slot_cost}
    per = defaultdict(float)
    for s, v in per_slot.items():
        per[fam_map[s]] += v
    per = dict(per)
    per_as_run = {f: cost[f] / S for f in cost}
    fams = sorted(per)
    mean_fam = float(np.mean([per[f] for f in fams]))
    mean_pair = float(np.mean(pair_secs))
    tab = []
    for k in range(1, k_max + 1):
        tab.append({"k": k, "usd_per_sentence_expected": k * mean_fam, "usd_per_sentence_cheapest_k": float(sum(sorted(per.values())[:k])),
                     "usd_per_sentence_dearest_k": float(sum(sorted(per.values())[-k:])),
                     "cpu_s_per_candidate": k * rows_per_family * mean_pair,
                     "cpu_s_intra_pool_plur": (k * rows_per_family) * (k * rows_per_family - 1) / 2 * mean_pair})
    return {"n_sentences_ledger": S, "usd_per_sentence_by_family_fewshot": per,
            "usd_per_sentence_by_slot_fewshot": per_slot, "sentences_by_slot_fewshot": {s: len(v) for s, v in slot_sents.items()},
            "usd_per_sentence_by_family_as_run_total_over_all_sentences": per_as_run, "calls_by_family_fewshot": dict(n_calls),
            "mean_completion_tokens_by_family": {f: float(np.mean(v)) for f, v in tok.items()},
            "usd_zero_shot_total_by_family_variant": dict(zs), "mean_family_usd_per_sentence": mean_fam,
            "mean_pair_cpu_s": mean_pair, "rows_per_family_per_sentence": rows_per_family, "by_k": tab,
            "fixed_pool_usd": {p: float(sum(per.get(f, 0) for f in p.split("+"))) for p in pools},
            "frontier_judge_reference": frontier}
