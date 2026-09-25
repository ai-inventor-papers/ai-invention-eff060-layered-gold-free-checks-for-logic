# /// script
# requires-python = ">=3.12"
# dependencies = ["loguru==0.7.3"]
# ///
"""Build full_data_out.json (exp_sel_data_out) from the three chosen datasets, one example per data row:
  rcomp_free_labels      2,652 FREE rows, name-free labels (search-only, sealed; see dataset_card.md)
  gloss_gate_items         840 known-answer (symbol use, meaning) items
  sig_soundness_replay   4,280 renamed SIG rows with known pure-z3 labels
All three are derived from this run's R_COMP artifacts by src/*.py (results/*.jsonl, work/sentences.json).
usage: uv run data.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "vendor"))

from loguru import logger  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
(ROOT / "logs").mkdir(exist_ok=True)
logger.add(ROOT / "logs" / "data.log", rotation="30 MB", level="DEBUG")

SELECTED = ["rcomp_free_labels", "gloss_gate_items", "sig_soundness_replay"]


@logger.catch(reraise=True)
def main() -> None:
    import build_output as B  # run-derived plan groups (reads results/*.jsonl, work/sentences.json)
    groups = [B.free_group(), B.gate_group(), B.sig_group()]
    for g in groups:
        assert g["examples"], g["dataset"]
        for e in g["examples"]:
            assert isinstance(e["input"], str) and isinstance(e["output"], str), g["dataset"]
            assert not ({"split", "dataset", "context"} & set(e)), g["dataset"]
    seal = json.loads((ROOT / "results" / "seal.json").read_text())["seals"][-1]
    t = json.loads((ROOT / "results" / "testability_FREE_v2.json").read_text())
    out = {"metadata": {
        "artifact": "T7b name-free labels for free-vocabulary rule translations (run_u75jRHUss0zo, iter 4, gen_art_dataset_5)",
        "workspace": str(ROOT),
        "selection": ("the three plan groups (chosen as best 3 of 6 standardised candidates; folio / malls_test / "
                      "logicnli_test were context only: no multi-system candidates, ~36-39% wrong gold, or no FOL; their "
                      "standardised record is temp/candidates_data_out.json)"),
        "label_mode": seal["mode"],
        "status_note": ("SEARCH-ONLY labels: the paid gloss step could not run (deviation D9: run OpenRouter budget "
                        "exhausted before this artifact's first call; re-probed at packaging, still HTTP 403). ERROR_CERT is "
                        "final and certificate-backed; MAPPED rows are UNRESOLVED_GLOSS_NOT_RUN until src/resume_gloss.py "
                        "runs. metadata_label_binary_search_provisional (ERROR vs MAPPED) is a provisional view with audited "
                        "contamination (results/soundness_audit.json)."),
        "seal_all_rows_sha256": seal["label_vector_sha256_all_rows"],
        "seal_untouched_sha256": seal.get("label_vector_sha256_untouched"),
        "prereg_sha256": seal["prereg_sha256"],
        "testability_all_rows": {k: t["all_rows"][k] for k in ("n_ERROR", "n_CORRECT", "TESTABLE", "label_counts")},
        "testability_untouched": {k: t["untouched_subset"][k] for k in ("n_ERROR", "n_CORRECT", "TESTABLE", "label_counts")},
        "provisional_view_testable": {k: t["search_provisional_view"][k]["TESTABLE"] for k in ("all_rows", "untouched_subset")},
    }, "datasets": [g for g in groups if g["dataset"] in SELECTED]}
    (ROOT / "full_data_out.json").write_text(json.dumps(out, ensure_ascii=False))
    logger.info(f"full_data_out.json: {[(g['dataset'], len(g['examples'])) for g in out['datasets']]}")


if __name__ == "__main__":
    main()
