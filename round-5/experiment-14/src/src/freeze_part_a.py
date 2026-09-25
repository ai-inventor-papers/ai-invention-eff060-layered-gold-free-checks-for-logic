#!/usr/bin/env python3
"""A7: write freeze/selection.json (immutable) and marker M1 freeze/CONSENSUS_FREEZE_READY.json (atomic). Refuses to
overwrite an existing selection.json."""
from __future__ import annotations

import json
import time

from common import FREEZE, RES, ROOT, atomic_write, jdump, sha256_file, utc

VARIANTS = ["V1", "V2", "V3", "V4", "V5"]


def main():
    sel_p = FREEZE / "selection.json"
    if sel_p.exists():
        raise SystemExit("freeze/selection.json exists: immutable after M1")
    A = json.loads((RES / "screen_E.json").read_text())
    S = json.loads((RES / "selection_E.json").read_text())
    W = json.loads((RES / "family_weights.json").read_text())
    C4 = json.loads((RES / "v4_coefs.json").read_text())
    per = {}
    for v in ["V0_frozen", "c_exact"] + VARIANTS:
        per[v] = {"auroc": {c: {k: A["auroc"][c][v][k] for k in ("auroc", "ci", "n")} for c in A["auroc"]},
                  "delta_vs_V0": {c: A["delta_vs_V0"][c].get(v) for c in A["delta_vs_V0"]} if v != "V0_frozen" else None,
                  "ed": {c: {k: A["ed"][c][v][k] for k in ("e", "d", "e_ci", "d_ci", "n_err", "n_cor")} for c in ("ALL", "LONG", "L25", "CTRL", "words_T3")}}
    sel = {
        "winner": S["winner"], "rule_text": S["rule_text"], "n_screened": S["n_screened"], "margin": S["margin"],
        "population": A["population"]["Z"], "cells": list(A["auroc"]), "E_status": "DEVELOPMENT numbers (E); E2 confirms",
        "qualification": S["qualification"], "E_numbers": per,
        "V4_coefficients_frozen": C4["frozen_coefficients_full_Z"], "V4_features": C4["features"],
        "V4_threshold_note": "V4 outputs a probability; e/d at the threshold matching V0's flag rate on Z "
                             f"({A['binary']['V0_flag_rate']:.4f}; V4 thr {A['binary']['V4_threshold_flag_rate_matched']:.4f})",
        "V2_recipe": "w_f = (n_f a_f + 20 abar)/(n_f + 20) from label-free cross-family agreement; E2 re-estimates with folds "
                     "int(sha1('E2_folds_v1|'+sentence_id),16)%5 (out of fold)",
        "V2_full_E_weights_reference": W["full_E"],
        "V5_families": ["deepseek", "microsoft", "openai"], "V5_note": "'openai' includes the frontier slot F; empty pool -> neutral 0.6266",
        "stability": S["stability"], "permutation_null": S["permutation_null"],
        "sha256": {"prereg_improve.json": sha256_file(ROOT / "prereg_improve.json"),
                   "results/scores_E_variants.jsonl": sha256_file(RES / "scores_E_variants.jsonl"),
                   "results/scores_E_V4.jsonl": sha256_file(RES / "scores_E_V4.jsonl"),
                   "freeze/consensus_variants.py": sha256_file(FREEZE / "consensus_variants.py")},
        "E2_instructions": "Score V0 with exp-5 byte-identical code (not consensus_variants.c_score_align). Winner NONE: V0 stands; "
                           "V1-V5 may be reported on E2 as development-only SECONDARY rows with consensus_variants.py unchanged.",
        "written_utc": utc()}
    jdump(sel, sel_p)
    m1 = {"token": "aii_iter5_consensus_freeze_v1", "written_utc": utc(),
          "V": {"status": "FROZEN", "selection_sha256": sha256_file(sel_p), "consensus_variants_sha256": sha256_file(FREEZE / "consensus_variants.py"),
                "winner": sel["winner"]},
          "GG": {"status": "PENDING", "expected_by_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() + 4 * 3600))},
          "files": {"selection": "freeze/selection.json", "consensus_variants": "freeze/consensus_variants.py",
                    "prereg": "prereg_improve.json", "scores": "results/scores_E_variants.jsonl", "tests": "tests/test_variants.py"},
          "workspace": str(ROOT)}
    atomic_write(FREEZE / "CONSENSUS_FREEZE_READY.json", json.dumps(m1, indent=1))
    print(json.dumps(m1, indent=1))


if __name__ == "__main__":
    main()
