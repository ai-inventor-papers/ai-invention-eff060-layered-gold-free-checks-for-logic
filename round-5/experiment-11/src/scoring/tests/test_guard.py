# NOTE (published copy): this file names server paths this repository
# does not publish (a stage it does not ship, or another run's workspace),
# so the steps that read them will not run from a clone as written:
#   /ai-inventor/aii_data/runs/x/labels_foo.jsonl
"""Allowlist guard: refuses 12 label-like / out-of-allowlist paths, allows the 4 permitted kinds."""
import sys
from pathlib import Path
import pytest
WS = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(WS))
from scoring import guard  # noqa: E402

E2S = WS / "e2src"
REFUSE = [E2S / "sealed" / "labels_E2.jsonl", E2S / "work" / "labels_heldout.jsonl", E2S / "work" / "panel_cache.jsonl",
          E2S / "work" / "panel_heldout.jsonl", E2S / "seal.json", E2S / "full_data_out.json", E2S / "work" / "reference_overrides.json",
          E2S / "work" / "trackh_panel_rows.json", WS / "per_item_E2A.jsonl", E2S / "work" / "assembled_E2.json",
          E2S / "sealed" / "references_E2.jsonl", Path("/ai-inventor/aii_data/runs/x/labels_foo.jsonl")]
ALLOW = [WS / "e2" / "candidates_E2_nolabels.jsonl", WS / "frozen" / "exp5" / "results" / "prereg.json", WS / "cache" / "x.jsonl",
         WS / "frozen" / "t1" / "src" / "labeller" / "fol.py"]


@pytest.mark.parametrize("p", REFUSE)
def test_refuses(p):
    with pytest.raises(PermissionError):
        guard.check(p)


@pytest.mark.parametrize("p", ALLOW)
def test_allows(p):
    guard.check(p)
