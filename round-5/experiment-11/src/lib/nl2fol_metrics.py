"""Reusable gold-free NL->FOL faithfulness metrics (E2-A, iteration 5), thin wrappers over the FROZEN code copies in
../frozen (exp-5 peer_text / pool_scoring / vendor_c eqmv) and ../freeze_copy (consensus_variants). Nothing is refit.

Every per-candidate score is oriented HIGHER = MORE LIKELY AN ERROR (unfaithful translation).
Every function states (i) what it MEASURES, (ii) what it does NOT measure, (iii) whether it needs a gold formula, (iv) cost.

Entry points
  parse_fol(fol)                                        dataset-E parser; None = unparseable (coverage failure)
  c_score_align(fol, peers, family=None)                V0, the frozen primary consensus score
  c_exact(fol, peers, family=None)                      same consensus with exact symbol names (no aligner)
  peer_text(text, fol, peers, family=None, q=None)      PT: frozen fusion of graded consensus + V0 + text-side checks
  variants_for_sentence(rows, weights=None)             V1-V5 for every output of ONE sentence (set-level)
  family_weights_from_sentences(list_of_rows_lists)     label-free family reliability weights for V2/V3/V5
  evaluate(scores, labels, strata, sentence_ids)        stratified AUROC + stratified sentence-cluster bootstrap CI

`peers` = list of (peer_fol: str, peer_family: str): formalizations of the SAME sentence produced by other systems.
With `family` given, peers of the candidate's own model family are dropped (leave-own-family-out, as frozen).
"""
from __future__ import annotations

import sys
from pathlib import Path

_WS = Path(__file__).resolve().parents[1]
for _p in (_WS / "frozen" / "exp5" / "src", _WS / "freeze_copy", _WS / "frozen" / "eval2" / "src"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import numpy as np  # noqa: E402

import peer_text as _PT  # noqa: E402  (frozen exp-5; binds the dataset-E parser)

_PRE5 = None


def _prereg5() -> dict:
    global _PRE5
    if _PRE5 is None:
        import json
        _PRE5 = json.loads((_WS / "frozen" / "exp5" / "results" / "prereg.json").read_text())
    return _PRE5


def parse_fol(fol: str | None):
    """MEASURES: whether `fol` parses under the dataset-E grammar (the parser that defines UNPARSEABLE labels).
    Returns the AST or None. GOLD: not needed. COST: microseconds."""
    return _PT.parse_fol(fol) if fol else None


def _pool(peers, family):
    return [p for p, f in peers if (family is None or f != family)]


def c_score_align(fol: str, peers: list[tuple[str, str]], family: str | None = None, min_peers: int = 2) -> float | None:
    """V0 (PRIMARY, frozen). MEASURES: 1 - (share of parseable peer formalizations of the same sentence, from model families
    other than the candidate's, that the iteration-1 eqmv procedure proves z3-equivalent to the candidate modulo a
    predicate/constant vocabulary alignment). i.e. how far the candidate sits from what independent systems write.
    DOES NOT MEASURE: agreement with a reference, or truth. An error that most peers share scores as faithful
    (peer-endorsed error); a correct but idiosyncratic reading scores as an error; a wrong predicate in the right place
    can be aligned away (MEANING_RENAME blind spot).
    Unparseable candidate -> 1.0; < `min_peers` parseable peers -> None (the caller imputes; E2 used exp-5's neutral 0.6266).
    GOLD: not needed. COST: the peers' generation (~$0.002 per sentence for 7 families) + z3 (eqmv 3 s cap per pair)."""
    from common import eqmv  # vendor_c (bound to the dataset-E parser by peer_text)
    e = parse_fol(fol)
    if e is None:
        return 1.0
    cs = _PT.canon(e)
    P = []
    for p in _pool(peers, family):
        pe = parse_fol(p)
        if pe is not None:
            P.append(_PT.canon(pe))
    if len(P) < min_peers:
        return None
    agree = 0
    for ps in P:
        if ps == cs:
            agree += 1
            continue
        a, b = (cs, ps) if cs < ps else (ps, cs)  # frozen canonical argument order
        try:
            r = eqmv(_PT.parse_fol(a), _PT.parse_fol(b))
            agree += bool(r and r[0] is True)
        except Exception:  # noqa: BLE001 - UNKNOWN counts as not equivalent
            pass
    return 1 - agree / len(P)


def c_exact(fol: str, peers: list[tuple[str, str]], family: str | None = None, min_peers: int = 2, ms: int = 2000) -> float | None:
    """MEASURES: 1 - share of family-disjoint parseable peers that z3 proves equivalent to the candidate with symbols
    identified by their EXACT names (no aligner). Stricter than V0: any vocabulary difference counts as disagreement, so it
    false-alarms on correct candidates whose wording differs from the peers'. DOES NOT MEASURE: meaning across vocabularies.
    GOLD: not needed. COST: as V0, z3 only (2 x `ms` per pair)."""
    e = parse_fol(fol)
    if e is None:
        return 1.0
    P = [parse_fol(p) for p in _pool(peers, family)]
    P = [p for p in P if p is not None]
    if len(P) < min_peers:
        return None
    n = 0
    for pe in P:
        if _PT.canon(pe) == _PT.canon(e):
            n += 1
            continue
        n += bool(_PT.z3_entails(e, pe, ms) is True and _PT.z3_entails(pe, e, ms) is True)
    return 1 - n / len(P)


def peer_text(text: str, fol: str, peers: list[tuple[str, str]], family: str | None = None, q: dict | None = None) -> dict:
    """PT (frozen exp-5 fusion). MEASURES: a fixed logistic combination (coefficients frozen on the iteration-2 screen) of
    ALIGN graded consensus g, V0, L2-bow (share of the sentence's content words the formula's symbols do not carry, plus
    unanchored predicates) and L3 (mismatches between an LLM's role questionnaire of the TEXT and the formula's z3 role
    profile; needs `q` from the exp-A questionnaire, else the neutral value is used).
    Returns {'p_error', 'c_score_align', 'g_align', 'l2_bow', 'l3_z3'}. DOES NOT MEASURE: anything the peers all get wrong
    and the text words do not reveal (scope, binding). GOLD: not needed. COST: V0's plus one small LLM call per sentence (L3)."""
    import pool_scoring as PS
    pre = _prereg5()
    P = dict(pre["scoring_params"])
    P.update(variants=["ALIGN"], k6_seeds=0, famfield=False, medoid_budget_s=0)
    rows = [{"key": "CAND", "fol": fol, "family": family or "__cand__", "family_field": family or "__cand__", "system": "cand", "is_peer": True}]
    rows += [{"key": f"P{i}", "fol": p, "family": f, "family_field": f, "system": f"peer{i}", "is_peer": True} for i, (p, f) in enumerate(peers)]
    out = {r["key"]: r for r in PS.score_sentence({"sentence_id": "lib", "text": text, "q": q, "rows": rows}, P)["rows"]}
    s = out["CAND"]
    if s.get("coverage_status") != "OK":
        return {"p_error": 1.0, "c_score_align": 1.0, "g_align": 1.0, "l2_bow": 1.0, "l3_z3": 1.0}
    neutral = pre["imputation"]["neutral"]
    feats = dict(s)
    for k in ("c_score_align", "ALIGN:g_score", "l2_bow", "l3_z3"):
        if feats.get(k) is None:
            feats[k] = neutral.get(k)
    feats["coverage_status"] = "OK"
    return {"p_error": _PT.fused_score(pre["frozen"], feats)["p_error"], "c_score_align": feats["c_score_align"],
            "g_align": feats["ALIGN:g_score"], "l2_bow": feats["l2_bow"], "l3_z3": feats["l3_z3"]}


def variants_for_sentence(rows: list[dict], weights: dict | None = None) -> dict[str, dict]:
    """SET-LEVEL (all outputs of ONE sentence). rows = [{'row_key', 'fol', 'family', 'slot'}]. Builds the eval-2 pairwise
    eqmv matrix, then returns per row_key {V0, c_exact, V1 c_pn, V2 c_rw, V3 c_pn_rw, V5 c_v5} with the frozen freeze code.
    MEASURES (V1): disagreement normalised by the size of the largest agreeing class (discounts scattered peers);
    (V2/V3/V5): the same with label-free family reliability weights (`weights` from family_weights_from_sentences; None =
    uniform). On E2 none of V1-V5 was carried by the freeze (development gain < +0.015 over V0). GOLD: not needed."""
    import consensus_variants as CV
    import pairwise
    m = pairwise.pairwise_matrix([{"row_key": r["row_key"], "fol": r["fol"], "slot": r.get("slot", r["family"]), "family": r["family"],
                                   "family_field": r["family"], "system_class": "llm"} for r in rows])
    m["sentence_id"] = "lib"
    I = CV.build_index(m)
    w = weights or {}
    out = {}
    for r in rows:
        k = r["row_key"]
        out[k] = {"V0": CV.c_score_align(I, k), "c_exact": CV.c_exact(I, k), "V1": CV.c_pn(I, k), "V2": CV.c_rw(I, k, w),
                  "V3": CV.c_pn_rw(I, k, w), "V5": CV.c_v5(I, k, w)}
    return out


def family_weights_from_sentences(sentences: list[list[dict]]) -> dict:
    """Label-free family reliability weights (mean cross-family agreement rate, shrunk to the grand mean with 20
    pseudo-sentences; freeze consensus_variants.family_weights). MEASURES how often a family's outputs agree with other
    families' - a proxy for reliability, NOT accuracy. GOLD: not needed."""
    import consensus_variants as CV
    import pairwise
    idx = []
    for i, rows in enumerate(sentences):
        m = pairwise.pairwise_matrix([{"row_key": r["row_key"], "fol": r["fol"], "slot": r.get("slot", r["family"]), "family": r["family"],
                                       "family_field": r["family"], "system_class": "llm"} for r in rows])
        m["sentence_id"] = f"s{i}"
        idx.append(CV.build_index(m))
    return CV.family_weights(idx, {f"s{i}": 0 for i in range(len(idx))}, None)


def evaluate(scores, labels, strata, sentence_ids, b: int = 2000, seed: int = 0) -> dict:
    """META-EVALUATION of any score column. labels: 1 = ERROR, 0 = CORRECT (None rows are skipped). MEASURES: the
    within-stratum pair AUROC (probability that a random ERROR scores above a random CORRECT of the same stratum) with a
    stratified sentence-cluster bootstrap 95% CI. 0.5 = does not track correctness."""
    from stats import WStratAuc, ci, strat_auc
    sys.path.insert(0, str(_WS / "analysis"))
    from analyse_E2A import strat_boot_weights
    s = np.asarray(scores, float)
    y = np.array([np.nan if v is None else float(v) for v in labels])
    st, sid = np.asarray(strata), np.asarray(sentence_ids)
    m = ~np.isnan(s) & ~np.isnan(y)
    W = strat_boot_weights(sid[m], st[m], b, seed)
    f = WStratAuc(y[m], s[m], st[m])
    return {"n": int(m.sum()), "strat_auroc": float(strat_auc(y[m], s[m], st[m])), "ci": ci([f(W[i]) for i in range(b)])}
