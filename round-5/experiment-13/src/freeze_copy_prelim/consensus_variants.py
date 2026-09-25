"""consensus_variants: label-free rescorings of cross-family solver consensus (iteration 5 FREEZE, Part A).

Pure functions, no I/O. Input = one sentence's record of eval-2's label-free pairwise matrix (pairwise_classes_E.jsonl line:
nodes with canon_fol + rows {row_key, slot, family, family_field, is_peer}, pairs [i, j, eq, kind, secs], cliques).
Orientation everywhere: HIGHER = MORE LIKELY ERROR. UNKNOWN (eq None) never counts as agreement.

Peer pool P(x) (leave-own-family-out, exp 5 convention): parseable rows with is_peer True whose vendor `family` differs from
the candidate's, excluding the candidate row itself. |P| < 2 -> score None (exp 5 imputes a neutral value downstream);
unparseable candidate (no matrix node) -> 1.0.

Variants (V0 is the frozen incumbent):
  V0 c_score_align  1 - share of P agreeing (eqmv: exact / align / gran). REPRODUCTION ONLY: E2 must score V0 with the
                    byte-identical exp-5 code, not with this function.
  c_exact           1 - share of P agreeing by pure z3 equivalence with identical symbols (aligner-free).
  V1 c_pn           plurality-normalised: 1 - min(1, share_A / max_class_share); classes = eval-2 greedy cliques
                    restricted to P's rows; share_A == 0 -> 1.0.
  V2 c_rw           reliability-weighted: 1 - sum_{p in P, A} w_f(p) / sum_{p in P} w_f(p); w_f are label-free
                    Dawid-Skene-style family weights (mean cross-family agreement rate, shrunk to the grand mean with
                    strength 20 sentences), estimated OUT OF FOLD (sentence folds) by family_weights().
  V3 c_pn_rw        V1 with w-weighted shares (candidate share and class shares).
  V4 c_two_channel  logistic(b0 + b1*c_exact + b2*c_align); coefficients were fit on E labels (cross-fitted OOF on E, then
                    refit once on all scorable E R_AB rows = the frozen coefficients); APPLICATION is gold-free.
  V5 c_v5           V3 on the cost-matched 3-pool {deepseek, microsoft, openai} minus the candidate's own family.

COST: all variants use the same peer pool as V0 (7 peer families, $0.002206 per sentence of generation, eval-2
tables/m4_auroc_k_cost.csv k=7) except V5 (3-pool, $0.000946 per sentence by the same table's per-family unit cost);
CPU = the eqmv matrix (median 0.005 s per node pair) plus microseconds of arithmetic.
"""
from __future__ import annotations

import math
from collections import defaultdict

POOL3 = ("deepseek", "microsoft", "openai")
SHRINK = 20.0


# ------------------------------------------------------------------------------------------------ index
def build_index(rec: dict) -> dict:
    """Index one pairwise_classes record. Returns {'sid', 'node_of', 'meta', 'eq', 'kind', 'clique_of'}.
    MEASURES: nothing (data structure). GOLD-FREE: yes. COST: O(#pairs)."""
    eq, kind = {}, {}
    for i, j, e, k, _s in rec["pairs"]:
        eq[(i, j)] = eq[(j, i)] = e
        kind[(i, j)] = kind[(j, i)] = k
    node_of, meta = {}, {}
    for nd in rec["nodes"]:
        for r in nd["rows"]:
            node_of[r["row_key"]] = nd["node_id"]
            meta[r["row_key"]] = r
    clique_of = {}
    for ci, cl in enumerate(rec.get("cliques") or [[nd["node_id"]] for nd in rec["nodes"]]):
        for n in cl:
            clique_of[n] = ci
    return {"sid": rec["sentence_id"], "node_of": node_of, "meta": meta, "eq": eq, "kind": kind, "clique_of": clique_of,
            "nodes": rec["nodes"]}


def agree(ix: dict, a: int, b: int) -> bool:
    """eqmv agreement of two nodes (same node = True; UNKNOWN = False)."""
    return True if a == b else ix["eq"].get((a, b)) is True


def agree_exact(ix: dict, a: int, b: int) -> bool:
    """Aligner-free agreement: same node, or eq True with kind 'exact'."""
    return True if a == b else (ix["eq"].get((a, b)) is True and ix["kind"].get((a, b)) == "exact")


def peers_lofo(ix: dict, row_key: str, families: tuple | None = None, family_key: str = "family") -> list[str]:
    """Peer rows of candidate `row_key`: is_peer, other vendor family, not itself; optionally restricted to `families`.
    MEASURES: the pool. GOLD-FREE: yes."""
    fam = ix["meta"][row_key][family_key]
    out = []
    for rk, m in ix["meta"].items():
        if not m["is_peer"] or m[family_key] == fam or rk == row_key:
            continue
        if families is not None and m[family_key] not in families:
            continue
        out.append(rk)
    return sorted(out)


# ------------------------------------------------------------------------------------------------ V0 / exact
def c_score_align(ix: dict, row_key: str, peers: list[str] | None = None, min_peers: int = 2) -> float | None:
    """V0 = 1 - share of peers eqmv-agreeing. REPRODUCTION ONLY (E2 must use exp-5 byte-identical code for V0).
    MEASURES: disagreement with other-family translations modulo vocabulary alignment. GOLD-FREE: yes."""
    if row_key not in ix["node_of"]:
        return 1.0
    P = peers_lofo(ix, row_key) if peers is None else peers
    if len(P) < min_peers:
        return None
    c = ix["node_of"][row_key]
    return 1 - sum(agree(ix, c, ix["node_of"][p]) for p in P) / len(P)


def c_exact(ix: dict, row_key: str, peers: list[str] | None = None, min_peers: int = 2) -> float | None:
    """1 - share of peers z3-equivalent with identical symbols (no aligner). GOLD-FREE: yes."""
    if row_key not in ix["node_of"]:
        return 1.0
    P = peers_lofo(ix, row_key) if peers is None else peers
    if len(P) < min_peers:
        return None
    c = ix["node_of"][row_key]
    return 1 - sum(agree_exact(ix, c, ix["node_of"][p]) for p in P) / len(P)


# ------------------------------------------------------------------------------------------------ V1 / V3 / V5
def _pn(ix: dict, row_key: str, P: list[str], w: dict | None) -> float:
    c = ix["node_of"][row_key]
    wt = (lambda rk: 1.0) if w is None else (lambda rk: float(w.get(ix["meta"][rk]["family"], 1.0)))
    tot = sum(wt(p) for p in P)
    if tot <= 0:
        return 1.0
    share_a = sum(wt(p) for p in P if agree(ix, c, ix["node_of"][p])) / tot
    if share_a == 0:
        return 1.0
    cls = defaultdict(float)
    for p in P:
        cls[ix["clique_of"][ix["node_of"][p]]] += wt(p)
    max_share = max(cls.values()) / tot
    return 1 - min(1.0, share_a / max_share)


def c_pn(ix: dict, row_key: str, peers: list[str] | None = None, min_peers: int = 2) -> float | None:
    """V1 plurality-normalised consensus: 1 - min(1, share_A / max_class_share) (share_A = 0 -> 1.0).
    MEASURES: how far the candidate's support falls short of the largest peer class (a candidate in the plurality of a
    scattered pool scores 0). GOLD-FREE: yes."""
    if row_key not in ix["node_of"]:
        return 1.0
    P = peers_lofo(ix, row_key) if peers is None else peers
    if len(P) < min_peers:
        return None
    return _pn(ix, row_key, P, None)


def c_pn_rw(ix: dict, row_key: str, weights: dict, peers: list[str] | None = None, min_peers: int = 2) -> float | None:
    """V3 = V1 with family-weighted shares. GOLD-FREE: yes (weights are label-free)."""
    if row_key not in ix["node_of"]:
        return 1.0
    P = peers_lofo(ix, row_key) if peers is None else peers
    if len(P) < min_peers:
        return None
    return _pn(ix, row_key, P, weights)


def c_v5(ix: dict, row_key: str, weights: dict, families: tuple = POOL3) -> float | None:
    """V5 = V3 on the cost-matched 3-pool {deepseek, microsoft, openai} minus own family; >= 1 pool row required
    (eval-2 c_k3 convention: empty pool -> None, imputed neutral downstream). GOLD-FREE: yes."""
    if row_key not in ix["node_of"]:
        return 1.0
    P = peers_lofo(ix, row_key, families=families)
    if len(P) < 1:
        return None
    return _pn(ix, row_key, P, weights)


# ------------------------------------------------------------------------------------------------ V2
def family_weights(indexes: list[dict], fold_of: dict, holdout_fold: int | None, shrink: float = SHRINK) -> dict:
    """Label-free family reliability weights from the pairwise matrix of every sentence NOT in `holdout_fold`
    (holdout_fold None = all sentences). For family f and sentence s (>= 1 peer row of f and >= 1 peer row of another
    family): agr_f(s) = mean over (r in f, q not in f) of A(r, q). a_f = mean_s agr_f(s), n_f = #such sentences,
    abar = mean over all (f, s) of agr_f(s); w_f = (n_f * a_f + shrink * abar) / (n_f + shrink).
    MEASURES: how often a family's translations agree with other families' (a proxy for its reliability, Dawid-Skene
    style, no labels). GOLD-FREE: yes."""
    per = defaultdict(list)
    allv = []
    for ix in indexes:
        if holdout_fold is not None and fold_of[ix["sid"]] == holdout_fold:
            continue
        peers = [rk for rk, m in ix["meta"].items() if m["is_peer"]]
        fams = defaultdict(list)
        for rk in peers:
            fams[ix["meta"][rk]["family"]].append(rk)
        for f, rs in fams.items():
            qs = [q for q in peers if ix["meta"][q]["family"] != f]
            if not rs or not qs:
                continue
            v = sum(agree(ix, ix["node_of"][r], ix["node_of"][q]) for r in rs for q in qs) / (len(rs) * len(qs))
            per[f].append(v)
            allv.append(v)
    abar = sum(allv) / len(allv) if allv else 0.0
    return {f: (len(v) * (sum(v) / len(v)) + shrink * abar) / (len(v) + shrink) for f, v in sorted(per.items())}


def c_rw(ix: dict, row_key: str, weights: dict, peers: list[str] | None = None, min_peers: int = 2) -> float | None:
    """V2 = 1 - sum_{p in P agreeing} w_f(p) / sum_{p in P} w_f(p); families missing from `weights` get weight 1.0
    (never happens on E). GOLD-FREE: yes."""
    if row_key not in ix["node_of"]:
        return 1.0
    P = peers_lofo(ix, row_key) if peers is None else peers
    if len(P) < min_peers:
        return None
    c = ix["node_of"][row_key]
    wt = {p: float(weights.get(ix["meta"][p]["family"], 1.0)) for p in P}
    tot = sum(wt.values())
    if tot <= 0:
        return 1.0
    return 1 - sum(wt[p] for p in P if agree(ix, c, ix["node_of"][p])) / tot


# ------------------------------------------------------------------------------------------------ V4
def c_two_channel(c_exact_v: float | None, c_align_v: float | None, coefs: dict) -> float | None:
    """V4 = sigmoid(b0 + b_exact * c_exact + b_align * c_align). coefs = {'intercept', 'c_exact', 'c_align'}.
    MEASURES: a label-fitted blend of aligner-free and aligned disagreement. GOLD-FREE application (coefficients were fit
    on E labels, OOF in development)."""
    if c_exact_v is None or c_align_v is None:
        return None
    z = coefs["intercept"] + coefs["c_exact"] * c_exact_v + coefs["c_align"] * c_align_v
    return 1 / (1 + math.exp(-z))
