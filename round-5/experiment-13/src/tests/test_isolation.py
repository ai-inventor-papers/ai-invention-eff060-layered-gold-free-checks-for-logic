"""Firewall: the labeller (labeller/src, labeller/vendor) never imports confirm/ and never names a score file; the score
whitelist loader drops every label key."""
import re
import sys
from pathlib import Path

WS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(WS / "confirm"))


def test_labeller_does_not_touch_confirm_or_scores():
    bad = []
    for d in ("src", "vendor"):
        for p in (WS / "labeller" / d).rglob("*.py"):
            t = p.read_text()
            for pat in (r"\bconfirm\b", r"scores_rcomp", r"judge_orig_iter5", r"score_seal", r"judge_frontier"):
                if re.search(pat, t):
                    bad.append((p.name, pat))
    assert not bad, bad


def test_whitelist_loader_drops_labels():
    from cc import LABEL_KEYS, load_scores
    rows = load_scores("FREE")
    assert len(rows) == 2652
    assert not any(set(r) & LABEL_KEYS for r in rows)
