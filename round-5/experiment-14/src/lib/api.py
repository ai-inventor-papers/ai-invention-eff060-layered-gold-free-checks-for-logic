"""lib/api.py: one entry point for every reusable NL->FOL faithfulness function of run_u75jRHUss0zo (iterations 1-5).

Every function takes (text, fol) or a set of them. Each docstring states: MEASURES (what the number means),
GOLD-FREE / GOLD-USING, and COST. Orientation of every score: HIGHER = MORE LIKELY ERROR.

The code is VENDORED byte-identically under lib/vendor/<artifact>/ (lib/PROVENANCE.json: source path + sha256) plus the
iteration-5 frozen modules in freeze/ (consensus_variants.py, gg.py). Several vendored trees define modules with the same
name (common, fol, stats, ...); _Vendor swaps each tree's modules in and out of sys.modules so they never collide.

Functions
  consensus_score(text, fol, peers, mode, families, weights, checker)   modes: align | exact | nf | hyb | pn | rw | gg
  consensus_variants_from_rows(rows, row_key, weights)                   V0/c_exact/V1/V2/V3/V5 exactly as frozen (E rows)
  graded_consensus(text, fol, peers, mode)
  pairwise_matrix(rows) / ed_decomposition(y, endorsed)
  peer_text_score(text, fol, peers)                                      exp-5 frozen PEER+TEXT fusion
  equivalent_modulo_vocab(a, b) / equivalent_modulo_vocab_exhaustive(a, b)
  minimal_typed_repair(fol, target)                                      GOLD-USING
  exhaustive_map_label(candidate, readings, ...) / gloss_decision(...)   GOLD-USING labelling tools
  fol_lint(fol) / content_accounting(text, fol) / role_accounting(text, fol)   exp-1 FOL-Triage layers
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

LIB = Path(__file__).resolve().parent
ROOT = LIB.parent
VEND = LIB / "vendor"
FREEZE = ROOT / "freeze"
E5_PREREG = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5/results/prereg.json")
E8_NLTK = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_8/data/nltk_data")
if str(FREEZE) not in sys.path:
    sys.path.insert(0, str(FREEZE))
if E8_NLTK.exists():
    os.environ.setdefault("NLTK_DATA", str(E8_NLTK))


class _Vendor:
    """Context manager: put one vendored tree first on sys.path and install ONLY its modules in sys.modules."""

    def __init__(self, name: str, subpaths: list[str]):
        self.root = VEND / name
        self.paths = [str(self.root / s) for s in subpaths]
        self.mods: dict = {}

    def _owned(self, m, root: Path) -> bool:
        f = getattr(m, "__file__", None) or ""
        return f.startswith(str(root))

    def __enter__(self):
        self._saved = list(sys.path)
        sys.path[:0] = self.paths
        names = {q.stem for sp in self.paths for q in Path(sp).glob("*.py")} | {q.name for sp in self.paths for q in Path(sp).iterdir() if q.is_dir()}
        self._stash = {k: sys.modules.pop(k) for k, m in list(sys.modules.items())
                       if not self._owned(m, self.root) and (self._owned(m, VEND) or k.split(".")[0] in names)}
        sys.modules.update(self.mods)
        return self

    def __exit__(self, *exc):
        for k, m in list(sys.modules.items()):
            if self._owned(m, self.root):
                self.mods[k] = sys.modules.pop(k)
        sys.modules.update(self._stash)
        sys.path[:] = self._saved
        return False


E8 = _Vendor("exp8_consensus", ["src", "src/vendor_c", "src/vendor_a"])
EV2 = _Vendor("eval2_pairwise", ["src", "vendor_exp5", "vendor_exp5/vendor_c"])
E5 = _Vendor("exp5_peer_text", ["src", "src/vendor_c"])
DS5 = _Vendor("dataset5_freelab", ["src", "vendor"])
E1 = _Vendor("exp1_triage", ["src"])


# ------------------------------------------------------------------------------------------------ consensus
def consensus_score(text: str, fol: str, peers: list[str], mode: str = "align", families: list[str] | None = None,
                    weights: dict | None = None, checker=None) -> dict:
    """Cross-family consensus of candidate `fol` against peer formalisations of the same sentence (peers = other
    families' outputs; exclude the candidate's own family). Returns a dict with 'c_score' (1 - agreement share).
    MEASURES: disagreement with independent translations; a coincident error shared by the peers scores as faithful.
    GOLD-FREE: yes (all modes). COST: peers ~ $0.0003 per peer per sentence of generation; z3 ~0.01-3 s per pair.
    modes:
      align  eqmv (exact, name-similarity alignment, granularity bridge; exp 8 consensus_lib) = V0 recipe.
      exact  identical symbols + z3 equivalence (aligner-free).
      nf     NF-anchored name-free alignment (exp 5); hyb = align OR nf.
      pn     V1 plurality-normalised (freeze/consensus_variants.c_pn) on the eqmv matrix of {candidate} + peers.
      rw     V2 reliability-weighted: needs `families` (one per peer) and `weights` (family -> w; default full-E weights
             from freeze/selection.json).
      gg     gloss-gated name-free agreement (freeze/gg.py); `checker(sentence, items) -> {pair_key: YES|NO}`; without a
             checker the search-only brackets c_gg_allyes / c_exact are returned and c_gg is None when a gloss is needed.
    Note for pn / rw: the frozen E scores computed classes over ALL rows of the sentence; use
    consensus_variants_from_rows() to reproduce them exactly."""
    if mode in ("align", "exact", "nf", "hyb"):
        with E8:
            import consensus_lib as CL
            return CL.consensus_score(text, fol, peers, mode=mode)
    if mode in ("pn", "rw"):
        rows = [{"row_key": "cand", "fol": fol, "slot": "CAND", "family": "__candidate__", "family_field": "__candidate__", "system_class": "llm"}]
        fams = families or [f"peer{i}" for i in range(len(peers))]
        rows += [{"row_key": f"p{i}", "fol": p, "slot": fams[i], "family": fams[i], "family_field": fams[i], "system_class": "llm"}
                 for i, p in enumerate(peers)]
        if mode == "rw" and weights is None:
            import json
            weights = json.loads((FREEZE / "selection.json").read_text())["V2_full_E_weights_reference"]
        out = consensus_variants_from_rows(rows, "cand", weights=weights or {})
        return {"c_score": out["V1"] if mode == "pn" else out["V2"], **out}
    if mode == "gg":
        import gg
        r = gg.consensus_score_gg(text, fol, peers, checker=checker)
        return {"c_score": r["c_gg"], **r}
    raise ValueError(mode)


def consensus_variants_from_rows(rows: list[dict], row_key: str, weights: dict | None = None) -> dict:
    """V0_rep, c_exact, V1 (pn), V2 (rw), V3 (pn_rw), V5 (3-pool) for one row of a sentence, from the eqmv matrix of ALL
    rows of that sentence (eval-2 pairwise_matrix + greedy cliques, then freeze/consensus_variants).
    rows: [{'row_key', 'fol', 'slot', 'family' (vendor family), 'family_field', 'system_class' ('llm' rows are peers)}].
    GOLD-FREE: yes. COST: one eqmv matrix per sentence (median 0.005 s per node pair)."""
    import consensus_variants as CV
    rec = pairwise_matrix(rows)
    with EV2:
        import consensus_mx as MX
        sm = MX.SentenceMatrix({"sentence_id": "api", **rec})
        rec["cliques"] = sm.cliques()
    rec["sentence_id"] = "api"
    ix = CV.build_index(rec)
    w = weights or {}
    out = {"V0_rep": CV.c_score_align(ix, row_key), "c_exact": CV.c_exact(ix, row_key), "V1": CV.c_pn(ix, row_key),
           "V2": CV.c_rw(ix, row_key, w), "V3": CV.c_pn_rw(ix, row_key, w), "V5": CV.c_v5(ix, row_key, w),
           "n_peers": len(CV.peers_lofo(ix, row_key)) if row_key in ix["node_of"] else 0}
    return out


def graded_consensus(text: str, fol: str, peers: list[str], mode: str = "hyb") -> dict:
    """Claim-unit consensus g = 1 - F1(support, coverage) with unit error codes (NEG/QUANT/SWAP/ADD/DROP) (exp 8).
    MEASURES: partial agreement with the peers, per claim unit. GOLD-FREE: yes. COST: z3 per (unit, peer)."""
    with E8:
        import consensus_lib as CL
        return CL.graded_consensus(text, fol, peers, mode=mode)


def pairwise_matrix(rows: list[dict]) -> dict:
    """Label-free eqmv matrix among all parseable outputs of ONE sentence (eval 2; 3000 ms, 30 s pair cap).
    MEASURES: which outputs are equivalent modulo vocabulary. GOLD-FREE: yes. COST: O(n^2) eqmv calls."""
    with EV2:
        import pairwise as PW
        return PW.pairwise_matrix(rows)


def ed_decomposition(y, endorsed) -> dict:
    """AUROC_b = 1 - (e + d)/2 bookkeeping identity (eval 2). e = P(endorsed | ERROR), d = P(not endorsed | CORRECT).
    GOLD-USING (needs labels): an evaluation tool, not a metric."""
    with EV2:
        import mechanism as MC
        return MC.ed_decomposition(y, endorsed)


def peer_text_score(text: str, fol: str, peers: list[str], q: dict | None = None) -> dict:
    """exp 5 frozen PEER+TEXT fusion (graded name-free consensus + text accounting), with exp-5's frozen model
    (results/prereg.json 'frozen', read-only on this volume). q = cached L3 questionnaire (None -> L3 imputed z=0).
    GOLD-FREE: yes. COST: z3 per (unit, peer) + (for l3_z3) one small-LLM questionnaire per sentence."""
    import json
    frozen = json.loads(E5_PREREG.read_text())["frozen"]
    with E5:
        import peer_text as PT
        return PT.peer_text_score(text, fol, peers, frozen, q=q)


def equivalent_modulo_vocab(fol_a: str, fol_b: str, ms: int = 3000):
    """Iteration-1 eqmv on two formula strings -> (True|False|None, how in {exact, align, gran, none}). GOLD-FREE when
    used between two candidates; GOLD-USING when b is a reference. COST: ~0.01-3 s."""
    with E8:
        import consensus_lib as CL
        return CL.equivalent_modulo_vocab(fol_a, fol_b, ms=ms)


def equivalent_modulo_vocab_exhaustive(fol_a: str, fol_b: str, max_maps: int = 200_000, max_secs: float = 90.0):
    """dataset-5 freelab: symmetric, name-free exhaustive map search (units, B1-B5 bridges, relations, constants) ->
    (True|False|None, map, n_maps). Equivalence up to renaming, NOT meaning: pair it with a gloss check. GOLD-FREE."""
    with DS5:
        import freelab as FL
        return FL.equivalent_modulo_vocab_exhaustive(fol_a, fol_b, max_maps=max_maps, max_secs=max_secs)


def minimal_typed_repair(fol: str, target: str, budget_s: float = 10.0) -> dict:
    """Smallest typed edit sequence (NEG, REV, QUANT, RESTR, CONN, MOVE, DROP, ADD, SWAP, BIND, SCOPE, UNGLUE; depth <= 2)
    turning fol into a formula equivalent to target (exp 8). GOLD-USING (target = a reference). COST: up to budget_s."""
    with E8:
        import consensus_lib as CL
        return CL.minimal_typed_repair(fol, target, budget_s=budget_s)


def exhaustive_map_label(candidate_fol: str, readings: dict, glosses: dict | None = None, checker=None) -> dict:
    """dataset-5 name-free label of a candidate against accepted template readings. GOLD-USING (readings)."""
    with DS5:
        import freelab as FL
        return FL.exhaustive_map_label(candidate_fol, readings, glosses=glosses, checker=checker)


def gloss_decision(maps: list[dict], pairs_union: list, verdict: dict):
    """dataset-5 gloss rule for exhaustive_map_label maps. GOLD-USING labelling tool."""
    with DS5:
        import freelab as FL
        return FL.gloss_decision(maps, pairs_union, verdict)


def fol_lint(fol: str) -> dict:
    """exp-1 FOL-Triage L1: text-free formula smells (EX_IMP, ALL_AND, IFF_RESTR, GLUE, FREE, VACUOUS, TRIVIAL, ARITY,
    DANGLING). GOLD-FREE. COST: a few z3 calls."""
    with E1:
        import fol_triage as FT
        return FT.fol_lint(fol)


def content_accounting(text: str, fol: str) -> dict:
    """exp-1 FOL-Triage L2-bow: unanchored predicates (ADD) and uncarried content words (DROP). GOLD-FREE. COST: CPU."""
    with E1:
        import fol_triage as FT
        return FT.content_accounting(text, fol)


def role_accounting(text: str, fol: str) -> dict:
    """exp-1 FOL-Triage L2-role: spaCy dependency roles of text words vs the exact z3 monotonicity of the aligned
    predicates (condition->DOWN, asserted->UP, ...). Needs spaCy + en_core_web_sm. GOLD-FREE. COST: CPU.
    (The fused L1->L2->L3 cascade with p_error lives in exp-1 src/pipeline.py, vendored alongside.)"""
    with E1:
        import fol_triage as FT
        return FT.role_accounting(text, fol)
