"""T1 head-on API bar: reusable metric wrappers (text, fol) and the statistics core of analyse_T1.py.

ORIENTATION CONVENTION (every score returned or consumed here): higher = more likely UNFAITHFUL to the text.

Metric wrappers (async; each takes a budget.Budget so every call is cost-capped and cached in results/llm_cache.jsonl)
  judge_api(b, text, fol, model, view, rubric='A')   1 - P(faithful) from a rubric-A JSON LLM judge (T=0, max_tokens 150)
  judge_pyes(b, text, fol, model, view)              1 - P(YES) from next-token logprobs of a one-word YES/NO judge
  frontier_judge(b, text, fol, view, model=...)      judge_api with a reasoning model (effort low, max_tokens 4000)
  sc5_api(b, text, k=5)                              k T=0.7 formalisations of the sentence (dataset-E few-shot prompt)
  sc5_score(candidate, samples)                      (1 - share of samples equivalent to the candidate modulo vocabulary,
                                                      entropy of the equivalence classes of {candidate} + samples)  [z3]
  roundtrip_api(b, text, fol)                        FOL -> English (flash-lite VERBALISE) -> the text; NLI / cosine are
                                                      computed on the GPU by method.py --stage nli --which api
  view = 'orig' (the sentence and formula as given) or 'disg' (exp-D nonce disguise of content words, both sides).

Statistics core (numpy; sentence-clustered)
  auroc, tie_rate, strat_auroc, ClusterBoot, paired_boot, boot_ci, delong, matched_fa_threshold, recall_at,
  build_s4 / nested_delta / permutation_null (cross-fitted logistic stacks on folds_E), gee_slope, gee_slope_diff,
  consensus_cost_per_item, ipw_auroc, vex_subset (re-exported from src/vocab_exact.py).
"""
from __future__ import annotations

import math
from collections import defaultdict
from typing import Callable, Sequence

import numpy as np
from scipy.stats import rankdata

STRATA = ("L25", "L20", "EXC", "CTRL")


# ===================================================================================================== metric wrappers
async def judge_api(b, text: str, fol: str, model: str = "google/gemini-2.5-flash-lite", view: str = "disg",
                    rubric: str = "A", item_id: str = "") -> dict:
    """Rubric-A JSON judge. MEASURES: the model's stated probability that `fol` expresses the meaning of `text`
    (quantifiers, condition vs assertion, negation, argument order, missing/added content; renaming and logically
    equivalent rewrites allowed). RETURNS {'score': 1 - P(faithful) or None, 'type', 'fail', 'cost'}.
    `view` is only recorded: pass the disguised pair (text_d, fol_d) for view='disg'."""
    from . import judges as J
    rub = J.RUBRIC_A if rubric == "A" else J.RUBRIC_B
    o = await J.judge_json(b, component="judge_cheap", model=model, rubric=rub, text=text, fol=fol, item_id=item_id or view,
                           user_tmpl=J.USER_JSON_A)
    return {"score": None if o.get("p") is None else 1.0 - o["p"], "type": o.get("type"), "fail": o.get("fail"),
            "cost": o.get("cost"), "view": view}


async def judge_pyes(b, text: str, fol: str, model: str = "openai/gpt-4.1-nano", view: str = "disg", item_id: str = "") -> dict:
    """One-token YES/NO judge (rubric A system prompt). MEASURES: P(YES) renormalised over the YES/NO top-5 logprobs
    (verdict-token fallback gives p in {0,1}). RETURNS {'score': 1 - P(YES) or None, 'src', 'fail', 'cost'}."""
    from . import judges as J
    o = await J.judge_logprob(b, component="judge_cheap2", model=model, rubric=J.RUBRIC_A, text=text, fol=fol,
                              item_id=item_id or view)
    return {"score": None if o.get("p") is None else 1.0 - o["p"], "src": o.get("src"), "fail": o.get("fail"),
            "cost": o.get("cost"), "view": view}


async def frontier_judge(b, text: str, fol: str, view: str = "orig", model: str = "google/gemini-3.1-pro-preview",
                         max_tokens: int = 4000, item_id: str = "") -> dict:
    """Frontier reasoning judge, same rubric-A JSON prompt (reasoning effort 'low'). Same output as judge_api."""
    from . import judges as J
    o = await J.judge_json(b, component="strong", model=model, rubric=J.RUBRIC_A, text=text, fol=fol, item_id=item_id or view,
                           max_tokens=max_tokens, extra={"reasoning": {"effort": "low"}}, user_tmpl=J.USER_JSON_A)
    return {"score": None if o.get("p") is None else 1.0 - o["p"], "type": o.get("type"), "fail": o.get("fail"),
            "cost": o.get("cost"), "view": view}


async def sc5_api(b, text: str, k: int = 5, model: str = "openai/gpt-4.1-nano") -> list[str | None]:
    """k independent T=0.7 formalisations of `text` with dataset E's few-shot generation prompt (the samples a
    self-consistency metric compares the candidate against). RETURNS k extracted formulas (None = failed call)."""
    import method as M  # noqa: PLC0415 - the SC call (and its cache key) lives in the orchestrator
    from . import judges as J
    outs = [await M._sc_call(b, J, text, "api_bar", i) for i in range(k)]
    forms = [J.extract_formula(o.get("text")) if o.get("text") else None for o in outs]
    return [f[4:].strip() if f and f.upper().startswith("FOL:") else f for f in forms]


def sc5_score(candidate: str, samples: Sequence[str | None], ms: int = 2000) -> dict:
    """SC-5 modulo vocabulary. MEASURES: disagreement of the candidate with the model's own resamples of the sentence.
    sc5_eq_frac (oriented) = 1 - #samples equivalent to the candidate (z3, after predicate/constant alignment) / k;
    sc5_entropy = entropy of the equivalence classes of {candidate} + samples (unparseable samples = singletons)."""
    from .consensus_min import sc_scores_one
    from .labeller.labeller import equivalent_modulo_vocab, parse_ok
    smp = [s if (s and parse_ok(s)) else None for s in samples]
    memo: dict = {}

    def eq(a, c):
        if a == c:
            return True
        key = (a, c) if a < c else (c, a)
        if key not in memo:
            try:
                memo[key] = equivalent_modulo_vocab(a, c, ms=ms, do_search=False)["cls"] in ("EQUIV", "VOCAB", "GRAN")
            except Exception:  # noqa: BLE001 - a z3 failure counts as not equivalent
                memo[key] = False
        return memo[key]
    r = sc_scores_one(candidate, smp, eq)
    return {"sc5_eq_frac": 1.0 - r["sc5_eq_frac"], "sc5_entropy": r["sc5_entropy"]}


async def roundtrip_api(b, text: str, fol: str, model: str = "google/gemini-2.5-flash-lite", item_id: str = "") -> dict:
    """Round trip step 1: FOL -> one plain English sentence (VERBALISE prompt, T=0). The NLI/cosine comparison with
    `text` (rt_nli_min = 1 - min(P_entail(text=>v), P_entail(v=>text)); rt_embed_cos = 1 - mpnet cosine) runs on the GPU
    in method.py --stage nli. RETURNS {'verbalisation', 'leak' (logic symbols left in the output), 'fail', 'cost'}."""
    from . import judges as J
    g = await J.simple_text(b, component="roundtrip", model=model, prompt=J.VERBALISE.format(fol=fol), item_id=item_id,
                            max_tokens=120)
    v, leak = J.clean_verbalisation(g["text"]) if g.get("text") else (None, False)
    return {"verbalisation": v, "leak": leak, "fail": g.get("fail"), "cost": g.get("cost")}


# ===================================================================================================== statistics
def auroc(y, s) -> float:
    """Mann-Whitney AUROC, ties counted 1/2 (== sklearn roc_auc_score). nan if one class is empty."""
    y = np.asarray(y)
    s = np.asarray(s, float)
    n1 = int(y.sum())
    n0 = len(y) - n1
    if n1 == 0 or n0 == 0:
        return float("nan")
    r = rankdata(s)
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))


def tie_rate(y, s) -> float:
    """Share of (ERROR, CORRECT) pairs whose scores are exactly tied."""
    y = np.asarray(y)
    s = np.asarray(s, float)
    pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    vals, inv = np.unique(np.concatenate([pos, neg]), return_inverse=True)
    cp = np.bincount(inv[:len(pos)], minlength=len(vals))
    cn = np.bincount(inv[len(pos):], minlength=len(vals))
    return float((cp * cn).sum() / (len(pos) * len(neg)))


def strat_auroc(y, s, stratum) -> float:
    """Within-stratum AUROC: sum_h AUC_h * P_h * N_h / sum_h P_h * N_h (only (ERROR, CORRECT) pairs from the same
    source stratum count), identical to exp 5's strat_auc. Removes the stratum-composition part of pooled AUROC."""
    y = np.asarray(y)
    s = np.asarray(s, float)
    stratum = np.asarray(stratum)
    num = den = 0.0
    for h in np.unique(stratum):
        m = stratum == h
        n1 = int(y[m].sum())
        n0 = int(m.sum()) - n1
        if n1 and n0:
            num += auroc(y[m], s[m]) * n1 * n0
            den += n1 * n0
    return num / den if den else float("nan")


class ClusterBoot:
    """Sentence-clustered bootstrap index sets: resample sentence ids with replacement (fixed seed); every metric on a
    row set uses the IDENTICAL resamples, which makes deltas paired."""

    def __init__(self, clusters: Sequence[str], b: int = 2000, seed: int = 0):
        by = defaultdict(list)
        for i, c in enumerate(clusters):
            by[c].append(i)
        keys = sorted(by)
        arr = [np.array(by[k]) for k in keys]
        rng = np.random.default_rng(seed)
        self.idx = []
        for _ in range(b):
            pick = rng.integers(0, len(keys), len(keys))
            self.idx.append(np.concatenate([arr[j] for j in pick]))
        self.n_clusters = len(keys)


def boot_ci(vals, lo: float = 2.5, hi: float = 97.5) -> list:
    v = np.asarray([x for x in vals if x is not None and not (isinstance(x, float) and math.isnan(x))], float)
    if len(v) == 0:
        return [None, None]
    return [float(np.percentile(v, lo)), float(np.percentile(v, hi))]


def paired_boot(y, a, c, cb: ClusterBoot, stat: str = "pooled", stratum=None) -> dict:
    """Paired delta stat(a) - stat(c) on identical rows; percentile CI over cluster resamples; one-sided
    p = share of resampled deltas <= 0. stat in {'pooled', 'strat'} (strat needs `stratum`)."""
    y = np.asarray(y)
    a = np.asarray(a, float)
    c = np.asarray(c, float)
    st = None if stratum is None else np.asarray(stratum)
    f = (lambda yy, ss, hh: auroc(yy, ss)) if stat == "pooled" else strat_auroc
    pa, pc = f(y, a, st), f(y, c, st)
    da, dc, dd = [], [], []
    for ix in cb.idx:
        hh = None if st is None else st[ix]
        xa, xc = f(y[ix], a[ix], hh), f(y[ix], c[ix], hh)
        da.append(xa)
        dc.append(xc)
        dd.append(xa - xc)
    dd_ = np.array([d for d in dd if not math.isnan(d)])
    return {"a": pa, "b": pc, "a_ci": boot_ci(da), "b_ci": boot_ci(dc), "delta": pa - pc, "ci": boot_ci(dd),
            "p_one_sided_le0": float(np.mean(dd_ <= 0)) if len(dd_) else None, "se": float(np.std(dd_)) if len(dd_) else None,
            "n": int(len(y)), "n_error": int(y.sum()), "n_correct": int(len(y) - y.sum()), "stat": stat}


def boot_stat(y, s, cb: ClusterBoot, stat: str = "pooled", stratum=None) -> dict:
    y = np.asarray(y)
    s = np.asarray(s, float)
    st = None if stratum is None else np.asarray(stratum)
    f = (lambda yy, ss, hh: auroc(yy, ss)) if stat == "pooled" else strat_auroc
    pt = f(y, s, st)
    bs = [f(y[ix], s[ix], None if st is None else st[ix]) for ix in cb.idx]
    return {"auroc": pt, "ci": boot_ci(bs)}


def delong(y, s1, s2) -> dict:
    """DeLong paired test on pooled AUROC (secondary: ignores sentence clustering)."""
    from scipy.stats import norm
    y = np.asarray(y)
    s1 = np.asarray(s1, float)
    s2 = np.asarray(s2, float)
    pos, neg = s1[y == 1], s1[y == 0]
    pos2, neg2 = s2[y == 1], s2[y == 0]
    m, n = len(pos), len(neg)
    if m < 2 or n < 2:
        return {"z": None, "p": None}

    def comps(p, q):
        # V10_i = mean_j [p_i > q_j] + .5[p_i == q_j]; vectorised by ranks
        allv = np.concatenate([p, q])
        r_all = rankdata(allv)
        r_p = rankdata(p)
        r_q = rankdata(q)
        v10 = (r_all[:len(p)] - r_p) / len(q)
        v01 = 1.0 - (r_all[len(p):] - r_q) / len(p)
        return v10, v01
    a10, a01 = comps(pos, neg)
    b10, b01 = comps(pos2, neg2)
    d = a10.mean() - b10.mean()
    s10 = np.cov(np.vstack([a10, b10]))
    s01 = np.cov(np.vstack([a01, b01]))
    var = (s10[0, 0] + s10[1, 1] - 2 * s10[0, 1]) / m + (s01[0, 0] + s01[1, 1] - 2 * s01[0, 1]) / n
    if var <= 0:
        return {"z": None, "p": None}
    z = d / math.sqrt(var)
    return {"z": float(z), "p": float(2 * (1 - norm.cdf(abs(z))))}


def matched_fa_threshold(neg_vals, fa: float = 0.10) -> float:
    """Threshold t = the (1-fa) quantile of the scores of CORRECT rows (flag = score > t)."""
    return float(np.quantile(np.asarray(neg_vals, float), 1 - fa))


def recall_at(y, s, t) -> dict:
    y = np.asarray(y)
    s = np.asarray(s, float)
    f = s > t
    tp = int((f & (y == 1)).sum())
    fp = int((f & (y == 0)).sum())
    return {"threshold": float(t), "recall": tp / max(1, int(y.sum())), "fa": fp / max(1, int((y == 0).sum())),
            "precision": tp / max(1, tp + fp), "n_flag": int(f.sum())}


def ipw_auroc(y, s, w) -> float:
    """Weighted Mann-Whitney AUROC: each (ERROR i, CORRECT j) pair weighted w_i * w_j (w = 1 / inclusion prob)."""
    y = np.asarray(y)
    s = np.asarray(s, float)
    w = np.asarray(w, float)
    p, n = s[y == 1], s[y == 0]
    wp, wn = w[y == 1], w[y == 0]
    if len(p) == 0 or len(n) == 0:
        return float("nan")
    gt = (p[:, None] > n[None, :]) + 0.5 * (p[:, None] == n[None, :])
    ww = wp[:, None] * wn[None, :]
    return float((gt * ww).sum() / ww.sum())


# ===================================================================================================== stacks
def build_s4(table: list[dict], labels: dict, folds: dict, feats: list[str], fail_fill: dict, C: float = 1.0):
    """Cross-fitted L2 logistic stack (exp 6 src/s4.fit_s4_oof: standardisation on training folds, missing-indicator
    columns, FAIL -> worst value). RETURNS (oof {row_key: p}, info)."""
    from .s4 import fit_s4_oof
    return fit_s4_oof(table, labels, folds, feats, C=C, fail_fill=fail_fill)


def nested_delta(y, s_big, s_small, cb: ClusterBoot, stratum=None) -> dict:
    """OOF(S+X) - OOF(S) on identical rows; pooled and stratified, paired cluster bootstrap over OOF predictions
    (no refit inside the bootstrap: exp D / exp 6 convention; slightly understates variance)."""
    return {"pooled": paired_boot(y, s_big, s_small, cb, "pooled"),
            "strat": paired_boot(y, s_big, s_small, cb, "strat", stratum) if stratum is not None else None}


def permutation_null(fit_pair: Callable[[dict], tuple[np.ndarray, np.ndarray]], keys: list[str], y: np.ndarray,
                     groups: list[str], stratum, n_rep: int = 100, seed: int = 0) -> dict:
    """Empirical null of a nested gain: permute labels WITHIN fold x stratum, refit both stacks (fit_pair(perm_labels)
    -> (oof_big, oof_small) aligned with keys) and record the delta against the permuted labels."""
    rng = np.random.default_rng(seed)
    cells = defaultdict(list)
    for i, g in enumerate(groups):
        cells[g].append(i)
    out_p, out_s = [], []
    st = np.asarray(stratum)
    for _ in range(n_rep):
        yy = y.copy()
        for ix in cells.values():
            ix = np.array(ix)
            yy[ix] = rng.permutation(yy[ix])
        big, small = fit_pair(dict(zip(keys, yy.tolist())))
        out_p.append(auroc(yy, big) - auroc(yy, small))
        out_s.append(strat_auroc(yy, big, st) - strat_auroc(yy, small, st))
    return {"pooled": out_p, "strat": out_s}


# ===================================================================================================== GEE
def gee_slope(correct, z, stratum, groups, alt_glm: bool = True) -> dict:
    """GEE Binomial(logit), exchangeable, clustered by sentence: correct ~ z + C(stratum). Returns slope of z."""
    import pandas as pd
    import statsmodels.api as sm
    import statsmodels.formula.api as smf
    df = pd.DataFrame({"c": np.asarray(correct, float), "z": np.asarray(z, float), "h": np.asarray(stratum), "g": np.asarray(groups)})
    try:
        m = smf.gee("c ~ z + C(h)", groups="g", data=df, family=sm.families.Binomial(),
                    cov_struct=sm.cov_struct.Exchangeable()).fit()
        ci_ = m.conf_int().loc["z"].tolist()
        return {"slope": float(m.params["z"]), "ci_model": [float(ci_[0]), float(ci_[1])], "p": float(m.pvalues["z"]),
                "fit": "GEE_exchangeable"}
    except Exception as e:  # noqa: BLE001 - non-convergence -> cluster-robust GLM (pre-declared fallback)
        if not alt_glm:
            raise
        m = smf.glm("c ~ z + C(h)", data=df, family=sm.families.Binomial()).fit(cov_type="cluster",
                                                                               cov_kwds={"groups": pd.factorize(df["g"])[0]})
        ci_ = m.conf_int().loc["z"].tolist()
        return {"slope": float(m.params["z"]), "ci_model": [float(ci_[0]), float(ci_[1])], "p": float(m.pvalues["z"]),
                "fit": f"GLM_cluster_fallback ({str(e)[:60]})"}


def _gee_fast_slope(c, z, H, g) -> float:
    """Slope from a GEE fit (used inside the bootstrap)."""
    try:
        return gee_slope(c, z, H, g)["slope"]
    except Exception:  # noqa: BLE001
        return float("nan")


def gee_slope_diff(correct_a, correct_b, z, stratum, groups, B: int = 1000, seed: int = 0, n_jobs: int = 7) -> dict:
    """M3 statistic: slope_a - slope_b (log-odds of a correct flag per SD of z), cluster bootstrap over sentences
    (resampled sentences get fresh cluster ids so duplicates are separate clusters)."""
    from joblib import Parallel, delayed
    ca, cb_, z, H, g = (np.asarray(x) for x in (correct_a, correct_b, z, stratum, groups))
    sa, sb = gee_slope(ca, z, H, g), gee_slope(cb_, z, H, g)
    # fresh cluster ids per draw: the position of the cluster in the draw
    by = defaultdict(list)
    for i, s in enumerate(g):
        by[s].append(i)
    keys = sorted(by)
    arr = [np.array(by[k]) for k in keys]
    rng = np.random.default_rng(seed)
    draws = [rng.integers(0, len(keys), len(keys)) for _ in range(B)]

    def rep(pick):
        ix = np.concatenate([arr[j] for j in pick])
        gid = np.concatenate([np.full(len(arr[j]), n) for n, j in enumerate(pick)])
        return (_gee_fast_slope(ca[ix], z[ix], H[ix], gid), _gee_fast_slope(cb_[ix], z[ix], H[ix], gid))
    res = Parallel(n_jobs=n_jobs)(delayed(rep)(p) for p in draws)
    d = [x - y for x, y in res if not (math.isnan(x) or math.isnan(y))]
    return {"slope_a": sa, "slope_b": sb, "diff": sa["slope"] - sb["slope"], "ci": boot_ci(d), "B_ok": len(d), "B": B,
            "slope_a_ci_boot": boot_ci([x for x, _ in res]), "slope_b_ci_boot": boot_ci([y for _, y in res])}


# ===================================================================================================== cost
def consensus_cost_per_item(peer_cost_sentence: float, n_candidates_sentence: int, z3_seconds: float,
                            cpu_usd_per_hour: float = 0.05) -> dict:
    """Consensus $/item. FULL = the sentence's peer-pool generation spend / candidates of the sentence + z3 CPU time
    priced at cpu_usd_per_hour (one core); MARGINAL = z3 CPU only (peer outputs already exist)."""
    cpu = z3_seconds / 3600.0 * cpu_usd_per_hour
    return {"full": peer_cost_sentence / max(1, n_candidates_sentence) + cpu, "marginal": cpu}


def vex_subset(*a, **k):
    from .vocab_exact import vex_rows
    return vex_rows(*a, **k)
