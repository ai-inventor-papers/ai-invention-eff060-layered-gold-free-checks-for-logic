"""T1 analyses (step 6): the ONLY place where the new API scores meet labels.

Guard: prereg_T1.sha256 must exist, match prereg_T1.json, and predate the first line of every results/scores/*.jsonl.
Main population: E_POOL PRIMARY under R_AB (n = 2,686; 1,822 ERROR / 864 CORRECT; 292 sentences).
Every paired delta is on the rows where BOTH metrics have a value (status ok / fallback / fail-by-design), n reported.
Outputs: results/analysis_T1.json, results/verdict_T1.json, results/tables_T1.md, results/per_item_T1.jsonl,
results/s4_full_coefs.json, figures/*.png|pdf.
"""
from __future__ import annotations

import hashlib
import json
import math
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from loguru import logger

from . import api_bar as AB
from .common import DATA, RES, ROOT, jdump, jload, read_jsonl

STRATA = ["L25", "L20", "EXC", "CTRL"]
LONG = ("L25", "L20", "EXC")
CHALLENGERS = ["c_score_align", "g_score", "nf_c_score", "p_peer_text", "p_text"]
API_BARS = ["judge_cheap_disg", "judge_cheap_orig", "judge_cheap2_disg", "judge_cheap2_orig"]
LOCAL_BAR = "L:judge_local_qwen8b_disg"
B = 2000
FIG = ROOT / "figures"
TIEBREAK_EPS = 1e-9


def _u01(k: str) -> float:
    return int(hashlib.sha1(("tiebreak|" + k).encode()).hexdigest()[:12], 16) / 16 ** 12


# ===================================================================================================== guard
def guard() -> dict:
    ps, pj = ROOT / "prereg_T1.sha256", ROOT / "prereg_T1.json"
    if not ps.exists():
        raise SystemExit("REFUSED: prereg_T1.sha256 missing")
    if ps.read_text().split()[0] != hashlib.sha256(pj.read_bytes()).hexdigest():
        raise SystemExit("REFUSED: prereg_T1.json changed after the freeze")
    t_fr = ps.stat().st_mtime
    first = {}
    for p in (RES / "scores").glob("*.jsonl"):
        l = p.open().readline()
        if l.strip():
            ts = json.loads(l).get("ts")
            first[p.name] = ts
            if ts is not None and ts < t_fr:
                raise SystemExit(f"REFUSED: {p.name} first line predates the prereg_T1 freeze")
    return {"prereg": jload(pj), "sha256": ps.read_text().split()[0], "frozen_mtime": t_fr, "score_first_ts": first}


# ===================================================================================================== table
class Table:
    """Per-row values of every metric (oriented), with the status-aware accessor .vec(metric, keys)."""

    def __init__(self, rows, api, fail_fill):
        self.rows = rows
        self.by = {x["canonical_key"]: x for x in rows}
        self.api = api
        self.fail_fill = fail_fill
        self.extra: dict[str, dict] = {}

    def value(self, m: str, k: str):
        if m in self.extra:
            return self.extra[m].get(k)
        if m in self.api:
            return self.api[m]["v"].get(k)
        x = self.by[k]
        if m.startswith("L:"):
            st = x.get(m + "__status")
            v = x.get(m)
            if st == "fail":
                return self.fail_fill.get(m[2:], 1.0) if v is None else v
            return v
        return x.get(m)

    def status(self, m: str, k: str) -> str:
        if m in self.api:
            return self.api[m]["st"].get(k, "missing")
        if m.startswith("L:"):
            return self.by[k].get(m + "__status") or "na"
        return "ok" if self.value(m, k) is not None else "missing"

    def vec(self, m: str, keys) -> np.ndarray:
        return np.array([np.nan if (v := self.value(m, k)) is None else float(v) for k in keys], float)

    def vec_tb(self, m: str, keys) -> np.ndarray:
        """vec() + a label-free, seeded tie-breaker (TIEBREAK_EPS x U[0,1) from sha1(canonical_key)) for the matched-FA
        operating points: quantised scores put >10% of CORRECT rows at the maximum, so 'flag = s > q90' never fires
        without it (randomised test; AUROCs never use it)."""
        return self.vec(m, keys) + TIEBREAK_EPS * np.array([_u01(k) for k in keys])

    def has(self, m: str) -> bool:
        return m in self.extra or m in self.api or any(self.value(m, x["canonical_key"]) is not None for x in self.rows[:500])


class Cell:
    """A labelled row set (keys, y, clusters, strata) with one bootstrap shared by every metric of the cell."""

    def __init__(self, name, keys, y, T: Table, b=B):
        self.name, self.keys, self.y = name, list(keys), np.asarray(y)
        self.cl = np.array([T.by[k]["sentence_id"] for k in self.keys])
        self.h = np.array([T.by[k]["source_stratum"] for k in self.keys])
        self.T = T
        self.b = b
        self._boots: dict = {}
        self._cache: dict = {}

    def boot(self, mask):
        key = hashlib.sha1(mask.tobytes()).hexdigest()
        if key not in self._boots:
            self._boots[key] = AB.ClusterBoot(list(self.cl[mask]), b=self.b, seed=0)
        return key, self._boots[key]

    def series(self, m, mask, stat):
        mk, cb = self.boot(mask)
        ck = (mk, m, stat)
        if ck not in self._cache:
            s = self.T.vec(m, self.keys)[mask]
            y, h = self.y[mask], self.h[mask]
            f = (lambda yy, ss, hh: AB.auroc(yy, ss)) if stat == "pooled" else AB.strat_auroc
            pt = f(y, s, h)
            bs = np.array([f(y[ix], s[ix], h[ix]) for ix in cb.idx])
            self._cache[ck] = (pt, bs)
        return self._cache[ck]

    def mask_for(self, *ms):
        mask = np.ones(len(self.keys), bool)
        for m in ms:
            mask &= ~np.isnan(self.T.vec(m, self.keys))
        return mask

    def n_info(self, mask):
        y = self.y[mask]
        return {"n": int(mask.sum()), "n_error": int(y.sum()), "n_correct": int(len(y) - y.sum()),
                "n_sentences": int(len(set(self.cl[mask])))}

    def metric(self, m, stat="pooled", mask=None):
        mask = self.mask_for(m) if mask is None else mask
        if mask.sum() < 10 or len(set(self.y[mask])) < 2:
            return {"untestable": True, **self.n_info(mask)}
        pt, bs = self.series(m, mask, stat)
        return {"auroc": pt, "ci": AB.boot_ci(bs), **self.n_info(mask)}

    def delta(self, a, c, stat="strat"):
        mask = self.mask_for(a, c)
        if mask.sum() < 10 or len(set(self.y[mask])) < 2:
            return {"untestable": True, **self.n_info(mask)}
        pa, ba = self.series(a, mask, stat)
        pc, bc = self.series(c, mask, stat)
        d = ba - bc
        d = d[~np.isnan(d)]
        out = {"a": a, "b": c, "stat": stat, "auroc_a": pa, "auroc_b": pc, "delta": pa - pc, "ci": AB.boot_ci(d),
               "p_one_sided_le0": float(np.mean(d <= 0)) if len(d) else None, "se": float(np.std(d)) if len(d) else None,
               **self.n_info(mask)}
        if stat == "pooled" and mask.sum() <= 6000:
            y = self.y[mask]
            dl = AB.delong(y, self.T.vec(a, self.keys)[mask], self.T.vec(c, self.keys)[mask])
            out["delong_z"], out["delong_p"] = dl["z"], dl["p"]
        return out


def testable(y, cl) -> bool:
    y = np.asarray(y)
    cl = np.asarray(cl)
    return int(y.sum()) >= 50 and int((y == 0).sum()) >= 50 and len(set(cl[y == 1])) >= 25 and len(set(cl[y == 0])) >= 25


# ===================================================================================================== descriptive per metric
def describe(cell: Cell, m: str, thr: dict, cost_item: dict) -> dict:
    mask = cell.mask_for(m)
    y = cell.y[mask]
    s = cell.T.vec(m, cell.keys)[mask]
    from sklearn.metrics import average_precision_score
    out = cell.metric(m, "pooled", mask)
    if out.get("untestable"):
        return out
    out["strat"] = cell.metric(m, "strat", mask)
    out["auprc"] = float(average_precision_score(y, s))
    out["prevalence"] = float(y.mean())
    out["tie_rate"] = AB.tie_rate(y, s)
    if m in thr and thr[m] is not None:
        out["at_frozen_threshold"] = AB.recall_at(y, s, thr[m])
    stb = cell.T.vec_tb(m, cell.keys)[mask]
    out["at_FA0.10_E"] = AB.recall_at(y, stb, AB.matched_fa_threshold(stb[y == 0], 0.10))
    out["at_FA0.10_E"]["share_correct_at_max"] = float(np.mean(s[y == 0] == np.max(s)))
    out["usd_per_item"] = cost_item.get(m)
    st = Counter(cell.T.status(m, k) for k in cell.keys)
    out["status_counts"] = dict(st)
    return out


# ===================================================================================================== main
def run(max_perm: int = 100, gee_B: int = 1000, t_budget_gee_s: float = 2400.0) -> dict:
    from .e_pool import load_E, regime_labels
    from .join_T1 import api_columns, base_rows
    G = guard()
    pre = G["prereg"]
    t0 = time.time()
    full = load_E(blind=False)
    rows, info = base_rows(full)
    by6 = {x["exp6_row_key"]: x for x in rows}
    regimes = {}
    for r in ("R_AB", "R_A", "COVERAGE", "CONTESTED_AS_CORRECT", "CONTESTED_AS_ERROR", "ALL_TIERS", "R_AB_L25_NO_TOPUP"):
        regimes[r] = {by6[k]["canonical_key"]: v for k, v in regime_labels(full, r).items()}
    api = api_columns(rows)
    api.update(vfb_columns(rows, api))
    fm = jload(DATA / "exp6_results" / "feature_meta.json")
    fail_fill = dict(fm["fail_fill"])
    for c in api:
        fail_fill[c] = math.log(6) if c.endswith("entropy") else 1.0
    T = Table(rows, api, fail_fill)
    A: dict = {"prereg_T1_sha256": G["sha256"], "guard": {k: v for k, v in G.items() if k != "prereg"}, "key_map": info,
               "api_columns": sorted(api)}
    # ---------------------------------------------------------------- populations
    def keys_for(regime, pool="E_POOL", primary=True, strata=None, extra=None):
        lab = regimes[regime]
        ks = [x["canonical_key"] for x in rows if x["canonical_key"] in lab and x["pool"] == pool
              and (x["parse_ok"] or not primary) and (strata is None or x["source_stratum"] in strata)
              and (extra is None or extra(x))]
        return ks, np.array([lab[k] for k in ks])
    P, yP = keys_for("R_AB")
    A["population"] = {"n": len(P), "n_error": int(yP.sum()), "n_correct": int(len(yP) - yP.sum()),
                       "n_sentences": len({T.by[k]["sentence_id"] for k in P})}
    logger.info(f"population {A['population']}")
    # ---------------------------------------------------------------- API coverage + status
    cov = {}
    for c in api:
        st = Counter(api[c]["st"].get(k, "missing") for k in P)
        cov[c] = {"status_RAB_primary": dict(st), "coverage_RAB": (st["ok"] + st["fallback"]) / max(1, len(P)),
                  "status_all_rows": dict(Counter(api[c]["st"].values()))}
    A["api_coverage"] = cov
    # ---------------------------------------------------------------- cost per item
    costs = read_jsonl(RES / "costs.jsonl") if (RES / "costs.jsonl").exists() else []
    comp_cost = defaultdict(list)
    for c in costs:
        comp_cost[c["component"]].append(c["cost"])
    cost_item = {}
    for m, comp in (("judge_cheap_disg", "judge_cheap"), ("judge_cheap_orig", "judge_cheap"), ("judge_cheap2_disg", "judge_cheap2"),
                    ("judge_cheap2_orig", "judge_cheap2"), ("judge_strong_orig", "strong"), ("judge_strong_disg", "strong"),
                    ("rt_nli_min", "roundtrip")):
        cc = comp_cost.get(comp, [])
        cost_item[m] = float(np.mean(cc)) if cc else None
    cc = comp_cost.get("sc5", [])
    if cc:
        n_cand_per_sent = np.mean(list(Counter(x["sentence_id"] for x in rows if x["pool"] == "E_POOL").values()))
        cost_item["sc5_eq_frac"] = float(np.mean(cc)) * 5 / n_cand_per_sent  # 5 samples per sentence, shared by its candidates
    cons_cost = consensus_costs(rows, P)
    cost_item["c_score_align"] = cons_cost["full_mean_usd_per_item"]
    cost_item["p_peer_text"] = cons_cost["full_mean_usd_per_item"]
    A["cost"] = {"per_item_usd": cost_item, "consensus": cons_cost}
    # ---------------------------------------------------------------- bars
    bars = [b for b in API_BARS if b in api]
    api_bar_ok = "judge_cheap_disg" in api and cov["judge_cheap_disg"]["coverage_RAB"] >= 0.95
    A["bar"] = {"primary": "judge_cheap_disg", "available": api_bar_ok, "api_bars_present": bars,
                "coverage": {b: cov[b]["coverage_RAB"] for b in bars}}
    cellP = Cell("R_AB pooled", P, yP, T)
    pooled_bar = {b: cellP.metric(b, "pooled")["auroc"] for b in bars if not cellP.metric(b, "pooled").get("untestable")}
    best = max(pooled_bar, key=pooled_bar.get) if pooled_bar else None
    A["bar"]["BEST_API_CHEAP"] = best
    A["bar"]["pooled_auroc"] = pooled_bar
    bar_list = bars + [LOCAL_BAR]
    # ---------------------------------------------------------------- (a) head-on bar
    cells = {}
    cells["R_AB pooled"] = cellP
    k, y = keys_for("R_AB", strata=LONG)
    cells["R_AB long (L25+L20+EXC)"] = Cell("R_AB long", k, y, T)
    for h in STRATA:
        k, y = keys_for("R_AB", strata=(h,))
        cells[f"R_AB {h}"] = Cell(f"R_AB {h}", k, y, T)
    k, y = keys_for("R_A", strata=("L20", "EXC"))
    cells["R_A L20+EXC"] = Cell("R_A L20+EXC", k, y, T)
    k, y = keys_for("R_A", strata=("L20", "EXC", "CTRL"))
    cells["R_A L20+EXC+CTRL"] = Cell("R_A L20+EXC+CTRL", k, y, T)
    k, y = keys_for("COVERAGE", primary=False)
    cells["COVERAGE (unparseable = ERROR)"] = Cell("COVERAGE", k, y, T)
    for r in ("CONTESTED_AS_CORRECT", "CONTESTED_AS_ERROR", "ALL_TIERS", "R_AB_L25_NO_TOPUP"):
        k, y = keys_for(r)
        cells[r] = Cell(r, k, y, T, b=1000)
    A["a_head_on"] = {}
    for cname, cell in cells.items():
        out = {"n": len(cell.keys), "n_error": int(cell.y.sum()), "n_correct": int(len(cell.y) - cell.y.sum()),
               "n_sentences": len(set(cell.cl)), "testable": testable(cell.y, cell.cl), "deltas": {}, "metrics": {}}
        stats = ["strat", "pooled"] if cname not in [f"R_AB {h}" for h in STRATA] else ["pooled"]
        for m in CHALLENGERS + bar_list + ["peer_only"]:
            out["metrics"][m] = {st: cell.metric(m, st) for st in stats}
        for a in CHALLENGERS:
            for bb in bar_list:
                for st in stats:
                    out["deltas"][f"{a} - {bb} [{st}]"] = cell.delta(a, bb, st)
        A["a_head_on"][cname] = out
        logger.info(f"(a) {cname}: n={out['n']} " + ", ".join(
            f"{a}-cheap_disg[{stats[0]}]={out['deltas'].get(f'{a} - judge_cheap_disg [{stats[0]}]', {}).get('delta', float('nan')):.3f}"
            for a in ("c_score_align", "p_peer_text")))
    # per-metric description on the main population
    thr = {"judge_cheap_disg": 0.5, "judge_cheap_orig": 0.5, "judge_cheap2_disg": 0.5, "judge_cheap2_orig": 0.5,
           "judge_strong_orig": 0.5, "judge_strong_disg": 0.5, "p_peer_text": pre["thresholds"]["consensus_PT"]["fused"],
           "p_text": pre["thresholds"]["consensus_PT"]["text"], LOCAL_BAR: 0.5}
    # ---------------------------------------------------------------- criterion (a)
    def crit_a(bar):
        c1 = A["a_head_on"]["R_AB pooled"]["deltas"].get(f"c_score_align - {bar} [strat]", {})
        c2 = A["a_head_on"]["R_AB long (L25+L20+EXC)"]["deltas"].get(f"c_score_align - {bar} [strat]", {})
        c3 = A["a_head_on"]["R_A L20+EXC"]["deltas"].get(f"c_score_align - {bar} [strat]", {})
        ok1 = bool(c1.get("ci") and c1["ci"][0] is not None and c1["ci"][0] > 0)
        ok2 = bool(c2.get("ci") and c2["ci"][0] is not None and c2["ci"][0] > 0)
        ok3 = bool(c3.get("delta") is not None and c3["delta"] > 0)
        return {"bar": bar, "R_AB_strat": {k_: c1.get(k_) for k_ in ("delta", "ci", "n", "p_one_sided_le0")}, "R_AB_strat_CI_gt0": ok1,
                "long_strat": {k_: c2.get(k_) for k_ in ("delta", "ci", "n")}, "long_strat_CI_gt0": ok2,
                "R_A_L20EXC": {k_: c3.get(k_) for k_ in ("delta", "ci", "n")}, "R_A_sign_gt0": ok3, "holds": ok1 and ok2 and ok3}
    A["criterion_a"] = {b: crit_a(b) for b in bar_list}
    # sensitivity: JSON-failure verdict fallback (prereg_T1.judge_json_failure_sensitivity)
    for vb in ("judge_cheap_disg_vfb", "judge_cheap_orig_vfb"):
        if vb in api:
            for cname in ("R_AB pooled", "R_AB long (L25+L20+EXC)", "R_A L20+EXC"):
                for a in ("c_score_align", "p_peer_text"):
                    A["a_head_on"][cname]["deltas"][f"{a} - {vb} [strat]"] = cells[cname].delta(a, vb, "strat")
            A["criterion_a"][vb] = crit_a(vb)
            A["a_head_on"]["R_AB pooled"]["metrics"][vb] = {"strat": cellP.metric(vb, "strat"), "pooled": cellP.metric(vb, "pooled")}
    # ---------------------------------------------------------------- (b) S4 nesting
    t1 = time.time()
    A["b_s4"], s4cols = s4_nesting(T, rows, regimes, P, yP, pre, api, cov, max_perm=max_perm)
    for c, v in s4cols.items():
        T.extra[c] = v
    logger.info(f"(b) S4 nesting done in {time.time()-t1:.0f}s")
    # describe metrics
    desc_metrics = CHALLENGERS + ["peer_only", "l2_bow", "l3_z3"] + bar_list + [m for m in ("rt_nli_min", "rt_nli_fwd", "rt_nli_bwd", "rt_nli_contra", "rt_nli_min_alt", "rt_embed_cos", "sc5_eq_frac", "sc5_entropy") if m in api] + \
        ["L:rt_nli_min_local", "L:sc5_local_eq_frac", "L:judge_local_qwen8b_orig", "L:judge_local_llama8b_disg", "L:parse_fail",
         "L:pilot_rerun_jacc"] + [c for c in s4cols if c.endswith("_oof")]
    A["metrics_R_AB"] = {m: describe(cellP, m, thr, cost_item) for m in desc_metrics}
    # S4 vs bar deltas on the main cells
    for cname in ("R_AB pooled", "R_AB long (L25+L20+EXC)", "R_A L20+EXC"):
        cell = cells[cname]
        for a in ("S4_full_oof", "S4_local_oof", "S4_full_plus_c_score_align_oof", "PT_refit_oof"):
            if a in T.extra:
                for bb in ("judge_cheap_disg", "c_score_align", "p_peer_text"):
                    if bb in api or bb in CHALLENGERS:
                        for st in ("strat", "pooled"):
                            A["a_head_on"][cname]["deltas"][f"{a} - {bb} [{st}]"] = cell.delta(a, bb, st)
    # ---------------------------------------------------------------- (c) VEX
    A["c_vex"] = vex_analysis(T, P, yP, api)
    # ---------------------------------------------------------------- (d) frontier
    A["d_frontier"] = frontier(T, regimes, api, cost_item, cons_cost)
    # ---------------------------------------------------------------- (e) M3
    t1 = time.time()
    A["e_M3"] = m3(T, P, yP, api, gee_B=gee_B, t_budget_s=t_budget_gee_s)
    logger.info(f"(e) M3 done in {time.time()-t1:.0f}s")
    # ---------------------------------------------------------------- (f) complexity
    A["f_complexity"] = complexity(T, P, yP, api)
    # ---------------------------------------------------------------- (g) contamination + retest
    A["g_contamination"] = contamination(T, regimes, api)
    # ---------------------------------------------------------------- (h) matched-FA recall per error group
    A["h_recall_by_group"] = recall_groups(T, P, yP, api)
    # ---------------------------------------------------------------- (i) system level
    A["i_system"] = system_level(T, P, yP, api)
    # ---------------------------------------------------------------- placebos
    rng = np.random.default_rng(0)
    ca = T.vec("c_score_align", P)
    jd = T.vec("judge_cheap_disg", P) if "judge_cheap_disg" in api else None
    sh = [AB.auroc(rng.permutation(yP), ca) for _ in range(200)]
    A["placebo"] = {"shuffled_label_auroc_c_score_align": float(np.mean(sh))}
    if jd is not None:
        m_ = ~np.isnan(jd)
        shd = []
        for _ in range(200):
            yy = rng.permutation(yP)
            shd.append(AB.strat_auroc(yy[m_], ca[m_], cellP.h[m_]) - AB.strat_auroc(yy[m_], jd[m_], cellP.h[m_]))
        A["placebo"]["shuffled_label_strat_delta_c_minus_cheapdisg"] = {"mean": float(np.mean(shd)), "p2.5": float(np.percentile(shd, 2.5)),
                                                                        "p97.5": float(np.percentile(shd, 97.5))}
    # ---------------------------------------------------------------- verdict
    A["verdict"] = verdict(A)
    A["runtime_s"] = time.time() - t0
    return A, T, rows, regimes


def vfb_columns(rows, api) -> dict:
    """Sensitivity copy of judge_cheap_{disg,orig}: rows whose JSON lacked faithful_prob (after the retry) but carried a
    verdict get the median P(faithful) of the ok rows with the same verdict (label-free); other fallbacks stay 0.5."""
    import re
    from .join_T1 import SCORES, _last_by_key
    J = _last_by_key(SCORES / "judge_cheap.jsonl")
    out = {}
    for cond in ("disg", "orig"):
        c = f"judge_cheap_{cond}"
        if c not in api:
            continue
        by_v = defaultdict(list)
        for k, r in J.items():
            if k.endswith("|" + cond) and r.get("p") is not None and r.get("verdict"):
                by_v[str(r["verdict"]).upper()].append(float(r["p"]))
        med = {v: float(np.median(ps)) for v, ps in by_v.items() if ps}
        vals, st, n_changed = dict(api[c]["v"]), dict(api[c]["st"]), 0
        for x in rows:
            k = x["canonical_key"]
            if st.get(k) != "fallback":
                continue
            r = J.get(f"{x['item_id']}|{cond}") or {}
            m = re.search(r'"verdict"\s*:\s*"(FAITHFUL|UNFAITHFUL)"', str(r.get("raw") or ""))
            if m and m.group(1) in med:
                vals[k] = 1.0 - med[m.group(1)]
                n_changed += 1
        out[c + "_vfb"] = {"v": vals, "st": st, "n_changed": n_changed, "verdict_medians": med}
    return out


# ===================================================================================================== consensus cost
def consensus_costs(rows, P) -> dict:
    """FULL consensus $/item = (LLM-slot generation spend of the sentence's peer pool, from dataset E's per-row
    metadata_cost_usd, summed over the sentence's E_POOL rows) / (#E_POOL candidates of the sentence) + z3 CPU seconds
    (exp 5 secs_pairs, one core priced at $0.05/h). MARGINAL = z3 only. exp 5's own cost_usd_peer_text is reported too."""
    spend = defaultdict(float)
    ncand = Counter()
    for x in rows:
        if x["pool"] == "E_POOL":
            spend[x["sentence_id"]] += float(x.get("gen_cost_usd") or 0.0)
            ncand[x["sentence_id"]] += 1
    full, marg, e5 = [], [], []
    by = {x["canonical_key"]: x for x in rows}
    for k in P:
        x = by[k]
        secs = float(x.get("e5_secs_pairs") or 0.0)
        c = AB.consensus_cost_per_item(spend[x["sentence_id"]], ncand[x["sentence_id"]], secs)
        full.append(c["full"])
        marg.append(c["marginal"])
        if x.get("e5_cost_usd_peer_text") is not None:
            e5.append(float(x["e5_cost_usd_peer_text"]))
    return {"full_mean_usd_per_item": float(np.mean(full)), "marginal_mean_usd_per_item": float(np.mean(marg)),
            "exp5_cost_usd_peer_text_mean": float(np.mean(e5)) if e5 else None,
            "z3_secs_mean": float(np.mean([float(by[k].get("e5_secs_pairs") or 0) for k in P])),
            "rule": "FULL = sentence peer-pool generation spend / candidates per sentence + z3 CPU ($0.05/core-hour); MARGINAL = z3 only"}


# ===================================================================================================== (b)
def _s4_table(T: Table, rows, feats_all, strata_onehot=True):
    out = []
    for x in rows:
        if x["pool"] != "E_POOL":
            continue
        k = x["canonical_key"]
        r = {"row_key": k, "metadata_fold_E": x["fold_E"], "pool": x["pool"], "parse_ok": x["parse_ok"]}
        for f in feats_all:
            v = T.value(f, k)
            st = T.status(f, k)
            r[f] = None if v is None else float(v)
            r[f + "__status"] = "fail" if st in ("fail", "fail_verbaliser") else ("ok" if v is not None else "na")
        if strata_onehot:
            for h in STRATA[:-1]:
                r[f"strat_{h}"] = 1.0 if x["source_stratum"] == h else 0.0
                r[f"strat_{h}__status"] = "ok"
        out.append(r)
    return out


def s4_nesting(T, rows, regimes, P, yP, pre, api, cov, max_perm=100):
    from .s4 import fit_s4_oof
    s4_local = ["L:" + f for f in pre["S4_sets"]["S4_local"]]
    api_full = ["judge_cheap_disg", "judge_cheap_orig", "judge_cheap2_disg", "judge_cheap2_orig", "rt_nli_min", "rt_nli_fwd",
                "rt_nli_bwd", "rt_nli_contra", "rt_embed_cos", "sc5_eq_frac", "sc5_entropy"]
    entered, substituted = [], {}
    local_counterpart = {"rt_nli_min": "L:rt_nli_min_local", "rt_nli_fwd": "L:rt_nli_fwd_local", "rt_nli_bwd": "L:rt_nli_bwd_local",
                         "rt_nli_contra": "L:rt_nli_contra_local", "rt_embed_cos": "L:rt_embed_cos_local",
                         "sc5_eq_frac": "L:sc5_local_eq_frac", "sc5_entropy": "L:sc5_local_entropy"}
    for c in api_full:
        if c in api and cov[c]["coverage_RAB"] >= 0.95:
            entered.append(c)
        else:
            substituted[c] = {"coverage": cov.get(c, {}).get("coverage_RAB", 0.0), "local_counterpart_kept": local_counterpart.get(c)}
    S4_full = s4_local + entered
    judges_all = [f for f in S4_full if "judge" in f]
    sets = {"S4_local": s4_local, "S4_full": S4_full,
            "S4_API": ["L:parse_fail", "L:pilot_joint_conflict", "L:pilot_arity_incons", "L:pilot_shape_incons", "L:pilot_dangling",
                       "L:pilot_rerun_jacc"] + [c for c in ("rt_nli_min", "rt_nli_fwd", "rt_nli_bwd", "rt_nli_contra", "rt_embed_cos") if c in entered]
                      + ["L:rt_nli_min_local", "L:rt_embed_cos_local"] + [c for c in API_BARS if c in entered] +
                      [c for c in ("sc5_eq_frac", "sc5_entropy") if c in entered],
            "S4_full_noJudge": [f for f in S4_full if f not in judges_all],
            "S4_full_strat": S4_full + ["strat_L25", "strat_L20", "strat_EXC"],
            "S4_full_plus_c_score_align": S4_full + ["c_score_align"],
            "S4_full_plus_p_peer_text": S4_full + ["p_peer_text"],
            "S4_full_plus_nf_c_score": S4_full + ["nf_c_score"],
            "S4_full_plus_g_c": S4_full + ["g_score", "c_score_align"],
            "S4_full_strat_plus_c_score_align": S4_full + ["strat_L25", "strat_L20", "strat_EXC", "c_score_align"],
            "S4_local_plus_c_score_align": s4_local + ["c_score_align"],
            "PT_refit": ["g_score", "c_score_align", "l2_bow", "l3_z3"],
            "PT_refit_NF": ["nf_g_score", "nf_c_score", "l2_bow", "l3_z3"]}
    feats_all = sorted({f for v in sets.values() for f in v if not f.startswith("strat_")})
    tab = _s4_table(T, rows, feats_all)
    lab = {k: v for k, v in regimes["R_AB"].items() if T.by[k]["pool"] == "E_POOL"}
    folds = {r["row_key"]: r["metadata_fold_E"] for r in tab}
    out = {"entered_api_columns": entered, "substituted": substituted, "sets": sets, "fits": {}}
    cols, coefs = {}, {}
    ff = {f: T.fail_fill.get(f[2:] if f.startswith("L:") else f, 1.0) for f in feats_all}
    for nm, feats in sets.items():
        oof, info = fit_s4_oof(tab, lab, folds, feats, C=1.0, fail_fill=ff)
        cols[nm + "_oof"] = oof
        coefs[nm] = {"features_used": info["features_used"], "coefs": info["coefs"], "n_train_per_fold": info["n_train_per_fold"],
                     "fold_thresholds": info["thresholds"]}
    cellP = Cell("R_AB pooled", P, yP, T)
    for c, v in cols.items():
        T.extra[c] = v
    for nm in sets:
        c = nm + "_oof"
        out["fits"][nm] = {"pooled": cellP.metric(c, "pooled"), "strat": cellP.metric(c, "strat")}
    nested = {}
    for big, small in (("S4_full_plus_c_score_align", "S4_full"), ("S4_full_plus_p_peer_text", "S4_full"),
                       ("S4_full_plus_nf_c_score", "S4_full"), ("S4_full_plus_g_c", "S4_full"),
                       ("S4_full_strat_plus_c_score_align", "S4_full_strat"), ("S4_local_plus_c_score_align", "S4_local"),
                       ("S4_full", "S4_local")):
        nested[f"{big} - {small}"] = {st: cellP.delta(big + "_oof", small + "_oof", st) for st in ("strat", "pooled")}
    for a, bb in (("c_score_align", "S4_full_oof"), ("p_peer_text", "S4_full_oof"), ("PT_refit_oof", "S4_full_oof"),
                  ("p_peer_text", "S4_local_oof")):
        nested[f"{a} - {bb}"] = {st: cellP.delta(a, bb, st) for st in ("strat", "pooled")}
    out["nested"] = nested
    # long-pool nested
    kL = [k for k in P if T.by[k]["source_stratum"] in LONG]
    cL = Cell("long", kL, np.array([lab[k] for k in kL]), T)
    out["nested_long"] = {"S4_full_plus_c_score_align - S4_full": {st: cL.delta("S4_full_plus_c_score_align_oof", "S4_full_oof", st)
                                                                   for st in ("strat", "pooled")}}
    # permutation null (within fold x stratum; both stacks refit; delta on the permuted labels)
    t0 = time.time()
    lk = sorted(lab)
    ylk = np.array([lab[k] for k in lk])
    grp = [f"{T.by[k]['fold_E']}|{T.by[k]['source_stratum']}" for k in lk]
    Pset = set(P)
    idxP = np.array([i for i, k in enumerate(lk) if k in Pset])
    hP = np.array([T.by[lk[i]]["source_stratum"] for i in idxP])

    def fit_pair(perm):
        ob, _ = fit_s4_oof(tab, perm, folds, sets["S4_full_plus_c_score_align"], C=1.0, fail_fill=ff)
        os_, _ = fit_s4_oof(tab, perm, folds, sets["S4_full"], C=1.0, fail_fill=ff)
        return ob, os_
    rng = np.random.default_rng(0)
    cells_ = defaultdict(list)
    for i, g in enumerate(grp):
        cells_[g].append(i)
    nulls_p, nulls_s = [], []
    for rep in range(max_perm):
        yy = ylk.copy()
        for ix in cells_.values():
            ix = np.array(ix)
            yy[ix] = rng.permutation(yy[ix])
        ob, os_ = fit_pair(dict(zip(lk, yy.tolist())))
        yb = yy[idxP]
        sb = np.array([ob[lk[i]] for i in idxP])
        ss = np.array([os_[lk[i]] for i in idxP])
        nulls_p.append(AB.auroc(yb, sb) - AB.auroc(yb, ss))
        nulls_s.append(AB.strat_auroc(yb, sb, hP) - AB.strat_auroc(yb, ss, hP))
        if rep == 4:
            logger.info(f"permutation null: 5 reps in {time.time()-t0:.0f}s")
    obs_s = nested["S4_full_plus_c_score_align - S4_full"]["strat"]["delta"]
    obs_p = nested["S4_full_plus_c_score_align - S4_full"]["pooled"]["delta"]
    out["permutation_null"] = {"reps": max_perm, "strat": {"p95": float(np.percentile(nulls_s, 95)), "mean": float(np.mean(nulls_s)),
                                                          "observed": obs_s, "observed_percentile": float(np.mean(np.array(nulls_s) < obs_s))},
                               "pooled": {"p95": float(np.percentile(nulls_p, 95)), "mean": float(np.mean(nulls_p)), "observed": obs_p,
                                          "observed_percentile": float(np.mean(np.array(nulls_p) < obs_p))},
                               "seconds": time.time() - t0}
    ns = nested["S4_full_plus_c_score_align - S4_full"]["strat"]
    npd = nested["S4_full_plus_c_score_align - S4_full"]["pooled"]
    ok_s = bool(ns.get("ci") and ns["ci"][0] is not None and ns["ci"][0] > 0 and obs_s > out["permutation_null"]["strat"]["p95"])
    ok_p = bool(npd.get("ci") and npd["ci"][0] is not None and npd["ci"][0] > 0 and obs_p > out["permutation_null"]["pooled"]["p95"])
    out["criterion_b"] = {"holds": ok_s, "pooled_version_holds": ok_p, "pooled_stratified_disagree": ok_s != ok_p,
                          "strat": {k: ns.get(k) for k in ("delta", "ci", "n")}, "pooled": {k: npd.get(k) for k in ("delta", "ci", "n")},
                          "null_p95_strat": out["permutation_null"]["strat"]["p95"]}
    # standardised coefficients of S4_full per fold (+ with c_score_align)
    jdump({nm: coefs[nm] for nm in coefs}, RES / "s4_full_coefs.json")
    out["S4_full_mean_coef"] = _mean_coef(coefs["S4_full"])
    out["S4_full_plus_c_mean_coef"] = _mean_coef(coefs["S4_full_plus_c_score_align"])
    return out, cols


def _mean_coef(c):
    agg = defaultdict(list)
    for f in c["coefs"]:
        for k, v in f["coef"].items():
            agg[k].append(v)
    return {k: {"mean": float(np.mean(v)), "min": float(np.min(v)), "max": float(np.max(v))} for k, v in sorted(agg.items(), key=lambda kv: -abs(np.mean(kv[1])))}


# ===================================================================================================== (c)
def vex_analysis(T, P, yP, api):
    V = jload(DATA / "vex_rows.json")
    decl = jload(RES / "vex_declaration.json")
    ymap = dict(zip(P, yP.tolist()))
    out = {"declaration": {k: decl[k] for k in ("include", "include_strict") if k in decl}}
    mets = [("c_score_align", "judge_cheap_disg"), ("nf_c_score", "judge_cheap_disg"), ("p_peer_text", "judge_cheap_disg"),
            ("c_score_align", "judge_cheap_orig"), ("c_score_align", LOCAL_BAR)]
    for nm, cond in (("VEX", lambda v: v.get("include")), ("VEX_STRICT", lambda v: v.get("include_strict")),
                     ("VEX_tierA_only", lambda v: v.get("include") and v.get("include_why") == "tierA_reverified")):
        ks = [k for k in P if k in V and cond(V[k])]
        y = np.array([ymap[k] for k in ks])
        cell = Cell(nm, ks, y, T)
        tst = testable(y, cell.cl) if len(ks) else False
        per = {}
        for h in STRATA:
            m_ = cell.h == h
            per[h] = {"n_error": int(y[m_].sum()), "n_correct": int((y[m_] == 0).sum()), "testable": testable(y[m_], cell.cl[m_])}
        n_tst = sum(v["testable"] for v in per.values())
        stat = "strat" if n_tst >= 2 else "pooled"
        res = {"n": len(ks), "n_error": int(y.sum()), "n_correct": int(len(y) - y.sum()), "n_sentences": len(set(cell.cl)),
               "testable": tst, "per_stratum": per, "stat_used": stat, "deltas": {}, "metrics": {}}
        if len(ks) >= 10 and 0 < y.sum() < len(y):
            for a, bb in mets:
                if bb in api or bb == LOCAL_BAR:
                    res["deltas"][f"{a} - {bb}"] = cell.delta(a, bb, stat)
                    res["deltas"][f"{a} - {bb} [pooled]"] = cell.delta(a, bb, "pooled")
            for m in ("c_score_align", "nf_c_score", "p_peer_text", "p_text", "judge_cheap_disg", "judge_cheap_orig", LOCAL_BAR):
                if m in api or m in CHALLENGERS or m == LOCAL_BAR:
                    res["metrics"][m] = cell.metric(m, "pooled")
        out[nm] = res
    main = out["VEX"]["deltas"].get("c_score_align - judge_cheap_disg", {})
    out["vex_rule"] = {"testable": out["VEX"]["testable"], "delta": main.get("delta"), "ci": main.get("ci"),
                       "sign_positive": bool(main.get("delta") is not None and main["delta"] > 0),
                       "strong_form_CI_gt0": bool(main.get("ci") and main["ci"][0] is not None and main["ci"][0] > 0),
                       "holds": bool(out["VEX"]["testable"] and main.get("delta") is not None and main["delta"] > 0)}
    # aligner-masked errors: tier-B rows whose auto label was VOCAB_GRAN and panel verdict ERROR (E's analogue of the
    # screen's solver-CORRECT -> panel-ERROR flips); recall at FA=0.10 (thresholds from R_AB CORRECT rows)
    neg = [k for k, y in zip(P, yP) if y == 0]
    masked = [k for k, y in zip(P, yP) if y == 1 and T.by[k]["label_tier"] == "B" and T.by[k]["auto_label"] == "VOCAB_GRAN"]
    mr = {"n": len(masked), "n_with_MEANING_RENAME_op": sum("MEANING_RENAME" in (T.by[k]["error_ops"] or []) for k in masked), "recall_FA0.10": {}}
    for m in ["c_score_align", "nf_c_score", "p_text", "p_peer_text"] + [b for b in API_BARS if b in api] + [LOCAL_BAR, "S4_full_oof"]:
        sn = T.vec_tb(m, neg)
        sm = T.vec_tb(m, masked)
        sn, sm = sn[~np.isnan(sn)], sm[~np.isnan(sm)]
        if len(sn) and len(sm):
            t = AB.matched_fa_threshold(sn, 0.10)
            mr["recall_FA0.10"][m] = {"recall": float(np.mean(sm > t)), "n": int(len(sm)), "threshold": t}
    out["aligner_masked_errors"] = mr
    return out


# ===================================================================================================== (d)
def frontier(T, regimes, api, cost_item, cons_cost):
    fr = jload(DATA / "frontier_frame.json")
    pop = fr["cells_population"]
    item_to_keys = defaultdict(list)
    for x in T.rows:
        if x["pool"] == "E_POOL" and x["parse_ok"]:
            item_to_keys[x["item_id"]].append(x["canonical_key"])
    lab = regimes["R_AB"]
    ks, y, w, cellname = [], [], [], []
    for r in fr["rows"]:
        cand = [k for k in item_to_keys[r["item_id"]] if k in lab]
        if not cand:
            continue
        k = sorted(cand)[0]  # one row per frame item (colliding item ids carry identical inputs and scores)
        ks.append(k)
        y.append(lab[k])
        w.append(1.0 / r["incl_prob"])
        cellname.append(r["cell"])
    y = np.array(y)
    w = np.array(w)
    out = {"n_frame_rows": len(ks), "n_error": int(y.sum()), "n_correct": int(len(y) - y.sum()), "metrics": {}}
    cell = Cell("frame", ks, y, T)
    mets = ["c_score_align", "p_peer_text", "nf_c_score", "judge_strong_orig", "judge_strong_disg", "judge_cheap_disg",
            "judge_cheap_orig", "S4_full_oof", "S4_local_oof", "L:judge_local_qwen14b_orig", "L:judge_local_qwen14b_disg", LOCAL_BAR]
    for m in mets:
        if not (m in api or m in T.extra or m.startswith("L:") or m in CHALLENGERS):
            continue
        s = T.vec(m, ks)
        mk = ~np.isnan(s)
        if mk.sum() < 20:
            out["metrics"][m] = {"n": int(mk.sum()), "untestable": True}
            continue
        mt = cell.metric(m, "pooled", mk)
        mt["auroc_ipw"] = AB.ipw_auroc(y[mk], s[mk], w[mk])
        cb = cell.boot(mk)[1]
        mt["auroc_ipw_ci"] = AB.boot_ci([AB.ipw_auroc(y[mk][ix], s[mk][ix], w[mk][ix]) for ix in cb.idx[:1000]])
        mt["coverage_frame"] = int(mk.sum())
        out["metrics"][m] = mt
    views = [v for v in ("judge_strong_orig", "judge_strong_disg") if v in out["metrics"] and not out["metrics"][v].get("untestable", False)]
    if views:
        best = max(views, key=lambda v: out["metrics"][v]["auroc"])
        mk = cell.mask_for("c_score_align", best)
        pa, ba = cell.series("c_score_align", mk, "pooled")
        pb, bb = cell.series(best, mk, "pooled")
        ratio_b = ba / bb
        out["ratio"] = {"best_frontier_view": best, "ratio": pa / pb, "ci": AB.boot_ci(ratio_b), "auroc_c": pa, "auroc_frontier": pb,
                        "n": int(mk.sum()), "delta": cell.delta("c_score_align", best, "pooled")}
        s_ipw_c = AB.ipw_auroc(y[mk], T.vec("c_score_align", ks)[mk], w[mk])
        s_ipw_f = AB.ipw_auroc(y[mk], T.vec(best, ks)[mk], w[mk])
        out["ratio"]["ratio_ipw"] = s_ipw_c / s_ipw_f
        # nested inside the frame: 5-fold GroupKFold by sentence, logistic [strong_orig + c] vs [strong_orig]
        if "judge_strong_orig" in api:
            out["nested_frame"] = nested_frame(cell, ks, y, T)
        fcost = [cost_item.get(v) for v in views if cost_item.get(v) is not None]
        f_item = float(sum(fcost)) if fcost else None  # orig (+ disg if both used) per item
        out["cost"] = {"frontier_usd_per_item_views_used": f_item, "frontier_views": views,
                       "frontier_usd_per_call": cost_item.get("judge_strong_orig"),
                       "consensus_full_usd_per_item": cons_cost["full_mean_usd_per_item"],
                       "consensus_marginal_usd_per_item": cons_cost["marginal_mean_usd_per_item"]}
        cost_ok = f_item is not None and cons_cost["full_mean_usd_per_item"] <= 0.10 * f_item
        ratio_ok = out["ratio"]["ratio"] >= 0.95
        nest_ok = bool(out.get("nested_frame", {}).get("ci") and out["nested_frame"]["ci"][0] is not None and out["nested_frame"]["ci"][0] > 0)
        out["criterion_d"] = {"ratio_ge_0.95": ratio_ok, "cost_le_0.10x": cost_ok, "nested_CI_gt0": nest_ok,
                              "holds": (ratio_ok and cost_ok) or nest_ok, "ratio": out["ratio"]["ratio"], "ratio_ci": out["ratio"]["ci"]}
        if "judge_strong_orig" in api and "judge_strong_disg" in api:
            out["orig_minus_disg_frontier"] = cell.delta("judge_strong_orig", "judge_strong_disg", "pooled")
    else:
        out["criterion_d"] = {"holds": None, "note": "no frontier scores"}
    return out


def nested_frame(cell, ks, y, T):
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import GroupKFold
    so = T.vec("judge_strong_orig", ks)
    sc = T.vec("c_score_align", ks)
    mk = ~np.isnan(so) & ~np.isnan(sc)
    yy, g = y[mk], cell.cl[mk]
    X1 = so[mk][:, None]
    X2 = np.column_stack([so[mk], sc[mk]])
    o1, o2 = np.zeros(len(yy)), np.zeros(len(yy))
    for tr, te in GroupKFold(n_splits=5).split(X1, yy, g):
        for X, o in ((X1, o1), (X2, o2)):
            mu, sd = X[tr].mean(0), X[tr].std(0)
            sd[sd == 0] = 1
            clf = LogisticRegression(C=1.0, max_iter=2000).fit((X[tr] - mu) / sd, yy[tr])
            o[te] = clf.predict_proba((X[te] - mu) / sd)[:, 1]
    cb = AB.ClusterBoot(list(g), b=B, seed=0)
    r = AB.paired_boot(yy, o2, o1, cb, "pooled")
    return {"delta": r["delta"], "ci": r["ci"], "auroc_with_c": r["a"], "auroc_strong_only": r["b"], "n": int(mk.sum())}


# ===================================================================================================== (e)
def m3(T, P, yP, api, gee_B=1000, t_budget_s=2400.0):
    from .api_bar import gee_slope, gee_slope_diff
    words = np.array([T.by[k]["strata"]["words"] for k in P], float)
    ncond = np.array([T.by[k]["strata"]["n_conditions"] for k in P], float)
    H = np.array([T.by[k]["source_stratum"] for k in P])
    g = np.array([T.by[k]["sentence_id"] for k in P])
    zw = (words - words.mean()) / words.std()
    zc = (ncond - ncond.mean()) / ncond.std()
    mets = ["c_score_align", "nf_c_score", "p_peer_text", "judge_cheap_disg", "judge_cheap_orig", "judge_cheap2_disg",
            "S4_full_oof", "sc5_eq_frac", "rt_nli_min", LOCAL_BAR]
    corr = {}
    out = {"slopes_words": {}, "slopes_ncond": {}, "thresholds_FA0.10": {}}
    for m in mets:
        if not (m in api or m in T.extra or m in CHALLENGERS or m.startswith("L:")):
            continue
        s = T.vec_tb(m, P)
        mk = ~np.isnan(s)
        if mk.sum() < 0.95 * len(P):
            out["slopes_words"][m] = {"skipped": f"coverage {mk.mean():.3f}"}
            continue
        s = np.where(mk, s, np.nanmedian(s))
        thr = AB.matched_fa_threshold(s[yP == 0], 0.10)
        c = ((s > thr).astype(int) == yP).astype(float)
        corr[m] = c
        out["thresholds_FA0.10"][m] = thr
        out.setdefault("achieved_operating_point", {})[m] = {"fa": float(np.mean(s[yP == 0] > thr)),
                                                             "recall": float(np.mean(s[yP == 1] > thr)),
                                                             "accuracy": float(c.mean())}
        out["slopes_words"][m] = gee_slope(c, zw, H, g)
        out["slopes_ncond"][m] = gee_slope(c, zc, H, g)
    if "c_score_align" in corr and "judge_cheap_disg" in corr:
        # timing check -> B
        t0 = time.time()
        _ = gee_slope_diff(corr["c_score_align"], corr["judge_cheap_disg"], zw, H, g, B=20, seed=1, n_jobs=7)
        per = (time.time() - t0) / 20
        Bw = gee_B if per * gee_B <= t_budget_s else 500
        out["bootstrap_timing"] = {"secs_per_rep_20rep_probe": per, "B_used": Bw}
        out["M3_words"] = gee_slope_diff(corr["c_score_align"], corr["judge_cheap_disg"], zw, H, g, B=Bw, seed=0, n_jobs=7)
        out["M3_ncond"] = gee_slope_diff(corr["c_score_align"], corr["judge_cheap_disg"], zc, H, g, B=min(Bw, 500), seed=0, n_jobs=7)
        # stacked GEE interaction cross-check
        import pandas as pd
        import statsmodels.api as sm
        import statsmodels.formula.api as smf
        df = pd.DataFrame({"c": np.concatenate([corr["c_score_align"], corr["judge_cheap_disg"]]), "z": np.concatenate([zw, zw]),
                           "m": ["cons"] * len(P) + ["judge"] * len(P), "h": np.concatenate([H, H]), "g": np.concatenate([g, g])})
        try:
            fit = smf.gee("c ~ z * C(m, Treatment('judge')) + C(h)", groups="g", data=df, family=sm.families.Binomial(),
                          cov_struct=sm.cov_struct.Exchangeable()).fit()
            nm = [p for p in fit.params.index if p.startswith("z:")][0]
            ci_ = fit.conf_int().loc[nm].tolist()
            out["stacked_interaction"] = {"term": nm, "coef": float(fit.params[nm]), "ci": [float(ci_[0]), float(ci_[1])],
                                          "p": float(fit.pvalues[nm])}
        except Exception as e:  # noqa: BLE001
            out["stacked_interaction"] = {"error": str(e)[:200]}
        ci = out["M3_words"]["ci"]
        out["criterion_M3"] = {"holds": bool(ci[0] is not None and ci[0] > 0), "diff": out["M3_words"]["diff"], "ci": ci,
                               "ncond_diff": out["M3_ncond"]["diff"], "ncond_ci": out["M3_ncond"]["ci"]}
    else:
        out["criterion_M3"] = {"holds": None, "note": "judge_cheap_disg missing"}
    # secondary: frozen screen thresholds (judges 0.5; others FA-matched unchanged)
    sec = {}
    for m in ("judge_cheap_disg", "judge_cheap_orig"):
        if m in corr:
            s = T.vec(m, P)
            mk = ~np.isnan(s)
            s = np.where(mk, s, 0.5)
            c = ((s > 0.5).astype(int) == yP).astype(float)
            sec[m] = gee_slope(c, zw, H, g)
    if "p_peer_text" in corr:
        s = T.vec("p_peer_text", P)
        pre = jload(ROOT / "prereg_T1.json")
        c = ((s > pre["thresholds"]["consensus_PT"]["fused"]).astype(int) == yP).astype(float)
        sec["p_peer_text"] = gee_slope(c, zw, H, g)
    out["secondary_frozen_thresholds"] = sec
    return out


# ===================================================================================================== (f)
BINS = {"words": [(0, 12, "<12"), (12, 20, "12-19"), (20, 25, "20-24"), (25, 35, "25-34"), (35, 10 ** 6, ">=35")],
        "n_conditions": [(0, 2, "<=1"), (2, 3, "2"), (3, 4, "3"), (4, 10 ** 6, "4+")],
        "n_quant": [(0, 2, "0-1"), (2, 3, "2"), (3, 10 ** 6, "3+")]}


def complexity(T, P, yP, api):
    mets = ["c_score_align", "nf_c_score", "p_peer_text"] + [b for b in API_BARS if b in api] + \
        [m for m in ("S4_full_oof", "sc5_eq_frac", "rt_nli_min") if m in api or m in T.extra] + [LOCAL_BAR]
    depth = np.array([T.by[k]["strata"]["depth"] for k in P], float)
    q = np.quantile(depth, [1 / 3, 2 / 3])
    out = {}
    for var, bins in list(BINS.items()) + [("depth", [(-1, q[0] + 1e-9, f"<={q[0]:g}"), (q[0] + 1e-9, q[1] + 1e-9, f"({q[0]:g},{q[1]:g}]"),
                                                     (q[1] + 1e-9, 10 ** 6, f">{q[1]:g}")]), ("exception_type", None)]:
        res = {}
        if bins is None:
            vals = [str(T.by[k]["strata"].get("exception_type")) for k in P]
            groups = sorted(set(vals))
            idx_of = {gname: [i for i, v in enumerate(vals) if v == gname] for gname in groups}
        else:
            vv = np.array([T.by[k]["strata"][var] for k in P], float)
            idx_of = {lab: list(np.where((vv >= lo) & (vv < hi))[0]) for lo, hi, lab in bins}
        for lab, ix in idx_of.items():
            ks = [P[i] for i in ix]
            y = yP[ix]
            cell = Cell(f"{var}:{lab}", ks, y, T, b=1000)
            r = {"n": len(ks), "n_error": int(y.sum()), "n_correct": int(len(y) - y.sum()), "testable": testable(y, cell.cl),
                 "metrics": {}}
            if len(ks) >= 10 and 0 < y.sum() < len(y):
                for m in mets:
                    r["metrics"][m] = cell.metric(m, "pooled")
                if "judge_cheap_disg" in api:
                    r["delta_c_minus_cheapdisg"] = cell.delta("c_score_align", "judge_cheap_disg", "pooled")
            res[lab] = r
        out[var] = res
    return out


# ===================================================================================================== (g)
def contamination(T, regimes, api):
    out = {}
    lab = regimes["R_AB"]
    kE = [x["canonical_key"] for x in T.rows if x["pool"] == "E_POOL" and x["parse_ok"] and x["canonical_key"] in lab]
    kG = [x["canonical_key"] for x in T.rows if x["pool"] == "GOLDSYS" and x["parse_ok"] and x["canonical_key"] in lab]
    yE = np.array([lab[k] for k in kE])
    yG = np.array([lab[k] for k in kG])
    out["n"] = {"E_POOL": len(kE), "GOLDSYS": len(kG), "GOLDSYS_error": int(yG.sum()), "GOLDSYS_correct": int(len(yG) - yG.sum())}
    sidE = np.array([T.by[k]["sentence_id"] for k in kE])
    sidG = np.array([T.by[k]["sentence_id"] for k in kG])
    sents = sorted(set(sidE) | set(sidG))
    posE, posG = defaultdict(list), defaultdict(list)
    for i, s in enumerate(sidE):
        posE[s].append(i)
    for i, s in enumerate(sidG):
        posG[s].append(i)
    rng = np.random.default_rng(0)
    draws = [rng.integers(0, len(sents), len(sents)) for _ in range(B)]
    for name in ("judge_cheap", "judge_cheap2"):
        o, d = f"{name}_orig", f"{name}_disg"
        if o not in api or d not in api:
            continue
        sEo, sEd, sGo, sGd = T.vec(o, kE), T.vec(d, kE), T.vec(o, kG), T.vec(d, kG)
        mE = ~np.isnan(sEo) & ~np.isnan(sEd)
        mG = ~np.isnan(sGo) & ~np.isnan(sGd)

        def stat(iE, iG):
            iE = iE[mE[iE]]
            iG = iG[mG[iG]]
            dE = AB.auroc(yE[iE], sEo[iE]) - AB.auroc(yE[iE], sEd[iE])
            dG = AB.auroc(yG[iG], sGo[iG]) - AB.auroc(yG[iG], sGd[iG])
            return dG - dE, dG, dE
        pt = stat(np.arange(len(kE)), np.arange(len(kG)))
        bs = []
        for dr in draws:
            iE = np.array([i for j in dr for i in posE.get(sents[j], [])], int)
            iG = np.array([i for j in dr for i in posG.get(sents[j], [])], int)
            if len(iG) and len(iE):
                bs.append(stat(iE, iG))
        bs = np.array(bs)
        se = float(np.nanstd(bs[:, 0]))
        out[name] = {"DiD": pt[0], "DiD_ci": AB.boot_ci(bs[:, 0]), "delta_orig_minus_disg_GOLDSYS": pt[1],
                     "delta_orig_minus_disg_GOLDSYS_ci": AB.boot_ci(bs[:, 1]), "delta_orig_minus_disg_E": pt[2],
                     "delta_orig_minus_disg_E_ci": AB.boot_ci(bs[:, 2]), "MDE": 2.8 * se, "se": se,
                     "note": "DiD = [AUROC_orig - AUROC_disg] on public MALLS gold used as a candidate (GOLDSYS) minus the same on "
                             "E_POOL; a positive DiD is consistent with memorisation of the public gold"}
    # test-retest of flash-lite (disguised view)
    R = {}
    p = RES / "scores" / "judge_cheap_retest.jsonl"
    if p.exists():
        for r in read_jsonl(p):
            R[r["key"]] = r
        J = {}
        for r in read_jsonl(RES / "scores" / "judge_cheap.jsonl"):
            J[r["key"]] = r
        pairs = [(J[k]["p"], r["p"]) for k, r in R.items() if k in J and J[k].get("p") is not None and r.get("p") is not None]
        if pairs:
            from scipy.stats import spearmanr
            a, b = np.array(pairs).T
            out["retest"] = {"n": len(pairs), "spearman": float(spearmanr(a, b).statistic), "exact_match": float(np.mean(a == b)),
                             "mean_abs_diff": float(np.mean(np.abs(a - b))), "n_requested": len(R)}
    return out


# ===================================================================================================== (h)
def err_groups(x) -> list[str]:
    ops = x.get("error_ops") or x.get("repair_ops") or []
    g = []
    if ops and set(ops) <= {"ADD", "DROP"}:
        g.append("COVERAGE (ADD/DROP only)")
    if x.get("e5_eqmv_medoid_eq") is True:
        g.append("PEER_ENDORSED")
    if x.get("e5_nf_eq_medoid_nf") is True:
        g.append("PEER_ENDORSED_NF")
    if x["label_tier"] == "B" and x["auto_label"] == "COMPOUND":
        g.append("COMPOUND (tier B)")
    if "MEANING_RENAME" in ops:
        g.append("MEANING_RENAME")
    if set(ops) & {"NEG", "REV", "QUANT"}:
        g.append("polarity (NEG/REV/QUANT)")
    if set(ops) & {"RESTR", "CONN", "BIND", "SWAP", "MOVE", "SCOPE"}:
        g.append("structural (RESTR/CONN/BIND/SWAP/MOVE/SCOPE)")
    if x["label_tier"] == "A" and len(ops) == 2:
        g.append("two-op (tier A)")
    if x["label_tier"] == "A" and len(ops) == 1:
        g.append("single-op (tier A)")
    return g


def recall_groups(T, P, yP, api):
    mets = ["c_score_align", "nf_c_score", "p_peer_text", "p_text"] + [b for b in API_BARS if b in api] + \
        [m for m in ("judge_strong_orig", "S4_full_oof", "sc5_eq_frac", "rt_nli_min") if m in api or m in T.extra] + [LOCAL_BAR]
    neg = [k for k, y in zip(P, yP) if y == 0]
    groups = defaultdict(list)
    for k, y in zip(P, yP):
        if y == 1:
            for gname in err_groups(T.by[k]):
                groups[gname].append(k)
    out = {"note": "tier-A repair ops point candidate -> reference (repair ADD = the candidate is missing content); descriptive"}
    for fa in (0.10, 0.20):
        res = {}
        th = {}
        for m in mets:
            sn = T.vec_tb(m, neg)
            sn = sn[~np.isnan(sn)]
            if len(sn) >= 50:
                th[m] = AB.matched_fa_threshold(sn, fa)
        for gname, ks in sorted(groups.items()):
            r = {"n": len(ks), "n_sentences": len({T.by[k]["sentence_id"] for k in ks}), "recall": {}}
            for m, t in th.items():
                s = T.vec_tb(m, ks)
                s = s[~np.isnan(s)]
                r["recall"][m] = float(np.mean(s > t)) if len(s) else None
            res[gname] = r
        out[f"FA{fa:.2f}"] = {"thresholds": th, "groups": res}
    return out


# ===================================================================================================== (i)
def system_level(T, P, yP, api):
    from scipy.stats import kendalltau
    mets = ["c_score_align", "nf_c_score", "p_peer_text", "p_text"] + [b for b in API_BARS if b in api] + \
        [m for m in ("S4_full_oof", "S4_local_oof", "sc5_eq_frac", "rt_nli_min") if m in api or m in T.extra] + [LOCAL_BAR]
    out = {}
    for unit in ("sysvar", "family"):
        units_ = np.array([T.by[k][unit] for k in P])
        sid = np.array([T.by[k]["sentence_id"] for k in P])
        U_ = sorted(set(units_))
        S = {m: T.vec(m, P) for m in mets}

        def taus(ix):
            er = np.array([yP[ix][units_[ix] == u].mean() if (units_[ix] == u).any() else np.nan for u in U_])
            res = {}
            for m in mets:
                sm = np.array([np.nanmean(S[m][ix][units_[ix] == u]) if (units_[ix] == u).any() else np.nan for u in U_])
                ok = ~np.isnan(er) & ~np.isnan(sm)
                res[m] = kendalltau(er[ok], sm[ok]).statistic if ok.sum() >= 3 else np.nan
            return res
        pt = taus(np.arange(len(P)))
        cb = AB.ClusterBoot(list(sid), b=1000, seed=0)
        bs = defaultdict(list)
        for ix in cb.idx:
            for m, v in taus(ix).items():
                bs[m].append(v)
        out[unit] = {"n_units": len(U_), "units": U_, "error_rate": {u: float(yP[units_ == u].mean()) for u in U_},
                     "tau_b": {m: {"tau": float(pt[m]), "ci": AB.boot_ci(bs[m])} for m in mets}}
    out["note"] = "descriptive (13 system x variant rows / 11 families); Kendall tau-b of mean oriented score vs R_AB error rate"
    return out


# ===================================================================================================== verdict
def verdict(A) -> dict:
    ca = A["criterion_a"].get("judge_cheap_disg", {})
    cb = A["b_s4"].get("criterion_b", {})
    cd = A["d_frontier"].get("criterion_d", {})
    cv = A["c_vex"].get("vex_rule", {})
    cm = A["e_M3"].get("criterion_M3", {})
    a, b, d, v = ca.get("holds"), cb.get("holds"), cd.get("holds"), cv.get("holds")

    def lab(x):
        return "CONFIRMED" if x is True else ("DISCONFIRMED" if x is False else "UNTESTABLE")
    if not A["bar"]["available"]:
        overall = "UNTESTABLE (API bar missing)"
    elif a is False:
        overall = "DISCONFIRMED"
    elif a and b and d and v:
        overall = "CONFIRMED"
    elif a and not b:
        overall = "PARTIAL (a holds, b fails: consensus redundant with the API-judge stack)"
    elif a and b and not v:
        overall = "PARTIAL (a and b hold, VEX fails: aligner confound not excluded)"
    elif a and b and v and d is False:
        overall = "PARTIAL (a, b, VEX hold; d fails: frontier judge not matched at <=10% cost)"
    elif a and b and v and d is None:
        overall = "PARTIAL (a, b, VEX hold; d untestable: no frontier scores)"
    else:
        overall = "PARTIAL"
    out = {"criteria": {"a": {"status": lab(a), **ca}, "b": {"status": lab(b), **cb}, "d": {"status": lab(d), **cd},
                        "VEX": {"status": lab(v), **cv}, "M3": {"status": lab(cm.get("holds")), **cm},
                        "c": {"status": "OTHER ARTIFACT (R_COMP-SIG)"}, "e": {"status": "OTHER ARTIFACT"}},
           "overall_T1_this_artifact": overall}
    best = A["bar"].get("BEST_API_CHEAP")
    if best and best in A["criterion_a"]:
        cab = A["criterion_a"][best]
        out["robustness_BEST_API_CHEAP"] = {"bar": best, "criterion_a": lab(cab.get("holds")), **cab}
    out["local_bar_secondary"] = {"bar": LOCAL_BAR, "criterion_a": lab(A["criterion_a"].get(LOCAL_BAR, {}).get("holds"))}
    return out
