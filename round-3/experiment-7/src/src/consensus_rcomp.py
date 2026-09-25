"""Reusable cross-family consensus functions for NL->FOL candidates (no gold formula, no LLM).

consensus_exact(fol, peers)  - the SIG-exact variant used as the primary metric on R_COMP-SIG.
consensus_scores(text, fol, peers) - the three exp-5 variants (ALIGN eqmv, NF-anchored, and their union HYB) with the
                               frozen exp-5 parameters, for the realistic case where peers choose their own vocabulary.

WHAT consensus_exact MEASURES. Given a candidate formula and the translations of the SAME sentence produced by OTHER
model families (family-disjoint peers), it returns the share of peers that are NOT logically equivalent to the candidate
under IDENTICAL predicate/constant names (z3, both directions of entailment, per-pair timeout). 0 = every peer agrees,
1 = no peer agrees. Higher = more likely unfaithful. It is valid ONLY when all translations share one signature (e.g. the
predicate list was given in the prompt, as in R_COMP-SIG): renaming a predicate makes a correct formula disagree with
everyone, so it is a labelling-regime metric, not a deployable one (its rename false-alarm rate is ~1 by design).
A peer that fails to parse or times out counts as not agreeing (conservative; the number of unknown pairs is returned).
"""
from __future__ import annotations

import signal
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for _p in (ROOT / "rcomp" / "labeller", ROOT / "src" / "vendor_x5", ROOT / "src"):
    if str(_p) not in sys.path:
        sys.path.append(str(_p))


class _Timeout(Exception):
    pass


def _alarm(signum, frame):  # noqa: ARG001
    raise _Timeout()


def _equiv(a, b, ms: int, cap_s: int):
    from fol import equivalent
    old = signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(cap_s)
    try:
        return equivalent(a, b, ms)
    except _Timeout:
        return None
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)


def consensus_exact(fol: str, peers: list[str], ms: int = 5000, pair_cap_s: int = 30, return_details: bool = False):
    """Share of family-disjoint peers NOT z3-equivalent to `fol` under identical vocabulary (see module docstring).

    fol   : candidate formula (dataset-E FOL syntax: ∀ ∃ ¬ ∧ ∨ → ↔, Pred(x, const)).
    peers : translations of the same sentence by OTHER model families (the caller enforces family-disjointness).
    Returns a float in [0, 1] (None if the candidate is unparseable or fewer than 2 peers), or a dict with details.
    """
    from fol import parse
    try:
        c = parse(fol)
    except Exception:  # noqa: BLE001 - the parser raises assorted errors on junk
        return {"score": None, "reason": "unparseable"} if return_details else None
    if len(peers) < 2:
        return {"score": None, "reason": "fewer than 2 peers"} if return_details else None
    eqs = []
    for p in peers:
        try:
            pe = parse(p)
        except Exception:  # noqa: BLE001
            eqs.append(False)
            continue
        eqs.append(True if str(pe) == str(c) else _equiv(c, pe, ms, pair_cap_s))
    score = 1 - sum(e is True for e in eqs) / len(eqs)
    if return_details:
        return {"score": score, "n_peers": len(eqs), "n_equal": sum(e is True for e in eqs), "n_unknown": sum(e is None for e in eqs)}
    return score


def consensus_scores(text: str, fol: str, peers: list[str]) -> dict:
    """Frozen exp-5 consensus variants for a candidate against family-disjoint peers with FREE vocabularies.

    c_score_align : 1 - share of peers equal to the candidate after the iteration-1 eqmv vocabulary aligner (+ z3)
    c_score_nf    : NF-anchored name-free consensus (exp-5 k=5, tau=0.5)
    c_score_hyb   : 1 - share of peers where ALIGN OR NF-anchored verifies equality (<= min of the two)
    g_align/g_nf  : graded unit-level consensus 1 - F1(support, coverage) (higher = more likely error)
    """
    import json
    import pool_scoring as PS
    pre = json.loads((ROOT / "src" / "vendor_x5" / "prereg_exp5.json").read_text())
    P = dict(pre["scoring_params"])
    P.update({"do_text": False, "k6_seeds": 0, "medoid_budget_s": 0, "famfield": False, "allpool": False, "codes": False, "hyb": True})
    rows = [{"key": "cand", "fol": fol, "family": "__cand__", "family_field": "__cand__", "system": "cand", "is_peer": False}]
    rows += [{"key": f"peer{i}", "fol": p, "family": f"__peer{i}__", "family_field": f"__peer{i}__", "system": f"peer{i}", "is_peer": True}
             for i, p in enumerate(peers)]
    out = PS.score_sentence({"sentence_id": "api", "text": text, "q": None, "rows": rows}, P)
    o = next(r for r in out["rows"] if r["key"] == "cand")
    return {"c_score_align": o.get("c_score_align"), "c_score_nf": o.get("NF-anchored:c_score_nf"), "c_score_hyb": o.get("c_score_hyb"),
            "g_align": o.get("ALIGN:g_score"), "g_nf": o.get("NF-anchored:g_score")}
