#!/usr/bin/env python3
"""B1: write prereg_gg.json + .sha256 before the full map search and before any gloss call. Refuses to overwrite."""
from __future__ import annotations

import hashlib
import json
import sys

from common import FREEZE, ROOT, sha256_file, utc

sys.path.insert(0, str(FREEZE))
import gg  # noqa: E402

P, S = ROOT / "prereg_gg.json", ROOT / "prereg_gg.sha256"

GATE_A_PROMPT = {
    "version": "gloss_gg_gateA_v1",
    "system": gg.PROMPT_GG_V1["system"],
    "user_template": ("Sentence: {sentence}\n\nEach numbered line shows symbol A (a logic atom used in a formalisation of the "
                      "sentence) and B (an English meaning).\n{items}\n\nFor each line answer YES if symbol A can denote exactly "
                      "meaning B (same argument roles) in this sentence, else NO. Return ONLY a JSON object mapping each line number "
                      "to \"YES\" or \"NO\", e.g. {{\"1\": \"YES\", \"2\": \"NO\"}}."),
    "item_template": "{n}. A = {atom} | B = the meaning \"{meaning}\"",
    "temperature": 0, "max_tokens": 200, "max_items_per_call": 12}


def prompt_sha(p: dict) -> str:
    return hashlib.sha256(json.dumps(p, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


PREREG = {
    "title": "PREREG_GG (iteration 5, Part B, H-RENAME): gloss-gated name-free agreement",
    "definition": ("GG agreement of formulas a, b of the same sentence: exact z3 equivalence with identical symbols, OR an "
                   "exhaustive injective arity-consistent symbol map (predicates + constants, bijection between z3-relevant symbols) "
                   "yielding z3 equivalence AND the gloss checker says YES for EVERY non-identity mapped pair of that map. "
                   "c_gg(x) = 1 - share of P(x) (same peer pool as V0) agreeing under GG."),
    "map_family": {"PRIMARY": "injective arity-consistent predicate map + injective constant map; either direction (bijection => one direction searched); NO B1-B5 bridges; argument order is never permuted",
                   "SECONDARY GG_B": "dataset-5 freelab full family (B1-B5): run only if CPU time remains",
                   "sound_prunes": "relevance (VACUOUS predicates / INERT constants dropped), equal arity multiset, equal #constants, equal (arity, polarity) multiset, 128-model fingerprint, z3 2 s",
                   "anchoring": "only when the full family exceeds the map cap: symbols whose lowercased name/arity occurs in BOTH formulas map to themselves (flag counted)",
                   "identity_pairs": "same lowercased name and same arity: no gloss needed",
                   "caps": {"max_maps_per_pair": gg.MAX_MAPS, "max_secs_per_pair": gg.MAX_SECS, "keep_equiv_maps": gg.KEEP,
                            "cap_hit": "not agreeing (counted)", "z3_unknown": "not agreeing (counted)"},
                   "agreement": "SOME kept equivalence map has ALL non-identity pairs YES"},
    "checker": {"model": "google/gemini-2.5-flash", "params": {"temperature": 0, "reasoning": {"max_tokens": 0}, "max_tokens": 200},
                "fallback_order": ["openai/gpt-4.1-mini", "mistralai/mistral-small-3.2-24b-instruct"],
                "never": ["anthropic/*", "qwen/*", "z-ai/* (Zhipu)", "moonshotai/*"],
                "family_note": "google is also the family of the flash-lite judge comparator (judge_cheap_*): stated as a limitation for any judge-vs-GG comparison",
                "batch": "<= 12 pairs per call, one sentence per call", "unparseable_answer": "NO (counted)",
                "cache_key": "checker|prompt_sha|sentence_id|kind|sorted(symbol_a, symbol_b)"},
    "prompt_gloss_gg_v1": gg.PROMPT_GG_V1, "prompt_gloss_gg_v1_sha256": prompt_sha(gg.PROMPT_GG_V1),
    "gates_checker": {
        "G-A": "dataset-5 gloss_gate_items (840; halves A/B), wrapped by prompt gloss_gg_gateA_v1 (same system text); develop on half A, confirm on half B; balanced accuracy >= 0.90 per half; per-class accuracy reported (7 classes)",
        "G-B": "symbol pairs from PERTURB R_COMP-base items only: RENAME_SYN controls (old -> new name from metadata_rename_map; expected YES) vs MEANING_RENAME mutants (metadata_edited_predicate -> the mutant's new name by positional atom alignment; expected NO); split by sha1(base) into dev/confirm halves; balanced accuracy >= 0.90 on each; need >= 60 YES and >= 60 NO pairs else NOT_TESTABLE (G-A alone)",
        "revision": "ONE prompt revision allowed after the dev halves (hashed as gloss_gg_v2 / gateA_v2), confirm halves re-run once",
        "fail": "GG status FAIL(checker): no E/PERTURB gloss sweep; CPU brackets still reported; boundary statement written"},
    "prompt_gloss_gg_gateA_v1": GATE_A_PROMPT, "prompt_gloss_gg_gateA_v1_sha256": prompt_sha(GATE_A_PROMPT),
    "dev_gates": {
        "g1": "RENAME_SYN paired flip = mean over controls of [flag(control) != flag(base)] at c > 0.5 <= 0.05 AND FA(RENAME_SYN) <= FA(base refs) + 0.05 (PERTURB E-bases)",
        "g2": "MEANING_RENAME recall at c > 0.5 >= c_align's recall (perturb_scores.jsonl, same rows) - 0.05; base FA and recall|base_endorsed printed beside",
        "g3": "E strat AUROC(c_gg) on Z >= V0 - 0.01 (paired, same rows)",
        "PASS": "g1 AND g2 AND g3 AND checker gates passed",
        "NONCE": "RENAME_NONCE FA / paired flip are an EXPECTED FAILURE for a meaning-checking GG (a nonce has no lexical meaning): reported, not gated"},
    "firewall": "GG is never evaluated on R_COMP FREE rows; no rcomp_free row is loaded (asserted in code: only perturb_scores is_rcomp False rows and dataset-3 R_COMP-base PERTURB items for gate G-B are read)",
    "budget": {"hard_cap_usd": 2.0, "reserve": 0.10, "gates_cap_usd": 0.10},
    "fallbacks": "F4 (checker blocked -> fallbacks, else brackets + UNTESTED(budget)), F5 (gate fail), F6 (CPU), F7 (spend) as in the plan",
    "search_code_sha256": sha256_file(FREEZE / "gg.py"), "fol_parser_sha256": sha256_file(FREEZE / "gg_fol.py"),
}


def main():
    if P.exists():
        raise SystemExit("prereg_gg.json exists")
    PREREG["written_utc"] = utc()
    P.write_text(json.dumps(PREREG, indent=1, ensure_ascii=False))
    S.write_text(hashlib.sha256(P.read_bytes()).hexdigest() + "  prereg_gg.json\n")
    print(S.read_text())


if __name__ == "__main__":
    main()
