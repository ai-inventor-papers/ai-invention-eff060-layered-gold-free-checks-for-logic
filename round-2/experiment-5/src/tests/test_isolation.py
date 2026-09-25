"""Isolation tests: the blind view has no label field, score_E.py never touches labels, analyse_E refuses without a valid,
older prereg. Run: .venv/bin/python -m pytest -c pytest.ini tests/test_isolation.py"""
import json
import os
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
FORBIDDEN = ["output", "reference_fol", "auto_label", "equiv_status", "repair_ops", "repair_status", "convention_flags",
             "panel_votes", "final_label", "error_ops", "label_tier", "label_source", "addrop_only_suspect",
             "solver_lenient_label", "correct_not_equivalent", "reading_choice", "gold_audit_flag", "reference_status",
             "class_id", "class_size"]


def test_blind_view_has_no_label_keys():
    for line in (ROOT / "data" / "E_blind.jsonl").read_text().splitlines()[:9000]:
        r = json.loads(line)
        keys = set(r) | set(r["strata"])
        assert not keys & set(FORBIDDEN), keys & set(FORBIDDEN)


@pytest.mark.parametrize("script", ["score_E.py", "run_api_E.py", "local_judge_E.py", "pool_scoring.py", "peer_text.py"])
def test_scorers_never_read_labels(script):
    src = (ROOT / "src" / script).read_text()
    for bad in ["E_labels", "final_label", "label_tier", "error_ops", "auto_label", "gold_audit_flag"]:
        assert bad not in src, f"{script} references {bad}"


def test_analyse_guard(tmp_path, monkeypatch):
    import analyse_E as AE
    monkeypatch.setattr(AE, "RES", tmp_path)
    with pytest.raises(SystemExit):
        AE.guard()  # prereg.sha256 missing
    (tmp_path / "prereg.json").write_text("{}")
    (tmp_path / "prereg.sha256").write_text("deadbeef  prereg.json\n")
    (tmp_path / "per_item_E.jsonl").write_text("")
    with pytest.raises(SystemExit):
        AE.guard()  # mismatched hash
    (tmp_path / "prereg.sha256").write_text(AE.sha256_file(tmp_path / "prereg.json") + "  prereg.json\n")
    t = time.time()
    os.utime(tmp_path / "per_item_E.jsonl", (t - 100, t - 100))
    os.utime(tmp_path / "prereg.sha256", (t, t))
    with pytest.raises(SystemExit):
        AE.guard()  # prereg newer than the score file
    os.utime(tmp_path / "per_item_E.jsonl", (t + 100, t + 100))
    assert AE.guard() == {}
