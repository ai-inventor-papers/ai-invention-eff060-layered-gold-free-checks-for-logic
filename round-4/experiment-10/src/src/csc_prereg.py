"""STAGE 4: freeze results/prereg_csc_P.json (+ .sha256) BEFORE any score is joined to operator or labels.

Never overwrites an existing freeze. The analysis script verifies the sha256 at start and aborts on mismatch.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
sys.path.insert(0, str(SRC))
import csc_lib as L  # noqa: E402

RES = ROOT / "results"
P = RES / "prereg_csc_P.json"
H = RES / "prereg_csc_P.sha256"


def freeze() -> str:
    if P.exists() and H.exists():
        return H.read_text().split()[0]
    pilot = json.loads((RES / "pilot_projection.json").read_text()) if (RES / "pilot_projection.json").exists() else None
    pre = {
        "id": "prereg_csc_P", "created_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "csc_definition": {
            "prompt_file": "data/prompts/fewshot_v1.txt",
            "prompt_sha256": hashlib.sha256(L.PROMPT_PATH.read_bytes()).hexdigest(),
            "block_template": L.BLOCK_TEMPLATE, "block_template_sha256": L.block_template_sha256(),
            "variant": "v1 (pilot could not run: API budget exhausted; v1b rule never triggered)",
            "shuffle_rule": "random.Random(int(sha1(text + '|' + '|'.join(sorted lower(name)/arity)), 16)).shuffle",
            "peer_pool_P": L.PEER_MODELS, "families": [L.PEER_FAMILY[m] for m in L.PEER_MODELS],
            "K3_rule": "first 3 of P with family != candidate family", "K4_rule": "all of P iff candidate family not in P",
            "equivalence": "exact z3 equivalence after lower-casing predicate/constant names, NO aligner; fp fingerprint "
                           "prefilter (sound); z3 timeout 2000 ms; UNKNOWN = not equivalent and counted",
            "parse_rule": "first JSON object with string 'fol' -> 'FOL:' line -> bare single parseable line -> fail",
            "insufficient_peers": "< 2 parseable peers -> c = 0.5, status csc_insufficient_peers",
            "unparseable_candidate": "c = 1 in the COVERAGE view",
            "multi": "peer endorses via alt_fol only if another peer produced that reading (fol or alt)",
            "graded": "peer_text.graded_consensus with identity pair records (pairs.py record format)"},
        "thresholds": {"primary_flag": "c > 0.5 on K3 (at most 1 of 3 peers agree)", "secondary": ["c == 1", "c > 0"],
                       "multi": "same thresholds"},
        "operator_groups": {"ANCHOR_RISK": ["ADD_FOREIGN", "ADD_INTERNAL", "MEANING_RENAME"],
                            "FREE_TO_EXPOSE": ["DROP", "SWAP"],
                            "SIG_PRESERVING": ["NEG", "REV", "QUANT", "RESTR", "CONN", "MOVE", "SWAP", "BIND"],
                            "CONTROLS": ["REORDER_COMMUTE", "REORDER_QUANT", "CONTRAPOSITIVE", "DEMORGAN", "RENAME_SYN",
                                         "RENAME_NONCE"]},
        "gates": {
            "G3_P": "RENAME_SYN FA <= paired base FA + 0.05 (point estimate, pooled E+R_COMP bases with SYN controls; "
                    "E-only and R_COMP-only rows reported)",
            "G4": "CSC e on ADD (both subtypes), DROP, MEANING_RENAME <= free-peer e + 0.05; free e = exp-8 c_align <= 0.5 "
                  "on the same E-base rows; R_COMP comparator = FREE3 exact/ALIGN where available else NA",
            "MT": "strict typing accuracy >= 0.55 on E-base mutants (CSC K3 peer-majority target)",
            "G5": "FULL peer cost per candidate <= $0.002"},
        "typing_rule": {"search": "same-vocab (lower-cased) BFS depth <= 2 over repair_census.edits + SUBST + ADD_ANY "
                                  "(ADD_ANY also conjoins negated target literals); fp prefilter + z3; 6 s per pair; "
                                  "VOCAB_GAP shortcut: |symmetric difference of symbol sets| > 4 -> no depth-2 repair "
                                  "exists (each edit changes <= 2 symbols), recorded without search",
                        "map": {"DROP": "ADD", "ADD": "DROP", "ADD_ANY": "DROP", "SUBST": "MEANING_RENAME",
                                "others": "identity"},
                        "strict": "depth-1 repair whose mapped op == true operator (ADD subtypes collapse to ADD)",
                        "lenient": "true op among the mapped ops", "no_majority": "wrong in strict; coverage reported"},
        "analysis_list": ["anchoring.csv (per op x polarity x base_source x variant: n, e, recall@c>0.5, recall@c==1, "
                          "share c==1, recall | base endorsed True/False)", "controls_fa.csv (FA, paired base FA, flip)",
                          "typing_csc.csv + confusion", "rcomp_sig_csc.json (within-template AUROC, e/d)",
                          "rcomp_free_labelfree.json", "cost_table.csv", "csc_gate_P.json", "d on bases by length"],
        "bootstrap": {"B": 2000, "seed": 0, "cluster_perturb": "base_item_id",
                      "sig": "template-stratified sentence clusters (exp 7 auc_tools)"},
        "cost_estimate": pilot,
        "data_role": "all inputs are DEVELOPMENT; the FREE cache is confirmation material and is never scored against labels",
        # ------------------------------------------------------------------ deviation, frozen before any join
        "deviation_D_BUDGET": {
            "what": "Before the pilot, every OpenRouter call returned HTTP 403 aii_run_budget_exhausted (the run-wide "
                    "'Test idea' phase budget of $7.00 was spent by other artifacts: $7.03 at 07:26 UTC; the proxy says it "
                    "does not reset while the run goes on). ':free' models were also exhausted (429 "
                    "free-models-per-day-high-balance, 1000/day, reset ~16.7 h later). This artifact spent $0.0000088 "
                    "(one 1-token probe). Hence NO CSC peer (mutant-signature, base-signature or FREE) could be generated.",
            "fallback_per_plan": "all CPU work runs; no local model substitutes for the CSC peers (plan fallback). "
                                 "Gates G3-P, G4 and MT(E) are declared UNTESTED, not passed or failed.",
            "zero_cost_arms_added": {
                "FREE3": "matched-resource UNCUED baseline: dataset-E G4/G6/G7 few-shot outputs (E bases) and exp-7 FREE "
                         "G4/G6/G7 (R_COMP bases) scored with consensus_lib exact and align (as pre-planned).",
                "SIGPROXY": "signature-CUED peers that already exist at $0: exp-7 SIG-condition outputs of the SAME four "
                            "families (G4 deepseek, G6 phi-4, G7 gpt-4.1-mini, G2 qwen) for the 77 R_COMP bases that "
                            "overlap exp 7. Their cue is the BASE/template signature in a CLOSED, glossed block ('Use only "
                            "these predicates and constants'), not the candidate's own open list. On signature-preserving "
                            "rows (base signature == candidate signature) this equals base-signature CSC up to the prompt "
                            "wording; on new-signature rows it is the 'base-signature peers' term of Delta-anchor only. "
                            "Same K3/K4 rule, same exact-equivalence, same thresholds.",
                "SIGPROXY_on_SIG": "exp-7 SIG rows scored with K3/K4 subsets of the same four families (vs the 9-peer "
                                   "c_score_sig): a k=3 family-matched ablation of signature-cued consensus, labelled.",
                "ORACLE_samevocab": "same-code typing ceiling against the true reference on all mutants."},
            "never": "no gate verdict is inferred from a proxy arm; proxy rows are labelled 'SIGPROXY' in every table"},
    }
    txt = json.dumps(pre, indent=1, ensure_ascii=False)
    P.write_text(txt)
    h = hashlib.sha256(txt.encode()).hexdigest()
    H.write_text(f"{h}  prereg_csc_P.json\n")
    return h


def verify() -> str:
    h = hashlib.sha256(P.read_bytes()).hexdigest()
    exp = H.read_text().split()[0]
    if h != exp:
        raise SystemExit(f"prereg hash mismatch: {h} != {exp}")
    return h


if __name__ == "__main__":
    print(freeze())
