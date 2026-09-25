"""Firewall: no aligner / consensus / judge / name-similarity code in ./src or ./vendor, and no reader of scored files
before STEP H (only src/post_seal_join.py may name rcomp_candidates.jsonl, and only through its whitelist loader)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BANNED = [r"equivalent_modulo_vocab\(", r"c_score", r"judge", r"difflib"]
SCORED = [r"scores_FREE", r"judge_FREE", r"free_labels\.jsonl"]


def _files():
    return [p for d in ("src", "vendor") for p in (ROOT / d).rglob("*.py")]


def test_no_banned_tokens():
    bad = []
    for p in _files():
        txt = p.read_text()
        for pat in BANNED:
            if re.search(pat, txt):
                bad.append((p.name, pat))
    assert not bad, bad


def test_scored_files_not_read():
    bad = []
    for p in _files():
        txt = p.read_text()
        for pat in SCORED:
            if re.search(pat, txt):
                bad.append((p.name, pat))
        if "rcomp_candidates" in txt and p.name not in ("post_seal_join.py", "common.py"):
            bad.append((p.name, "rcomp_candidates"))
    assert not bad, bad
