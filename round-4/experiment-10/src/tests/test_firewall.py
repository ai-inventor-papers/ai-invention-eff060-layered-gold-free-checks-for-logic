"""Firewall checks on WRITTEN files (plan testing item 8)."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DERIVED = {"text", "signature", "sig_key", "cand_parse_ok"}
WHITELIST = {"row_key", "item_id", "sentence_id", "template_id", "slot", "system", "family", "condition", "candidate_fol",
             "parse_ok", "prompt_variant", "free_align_class_id", "free_hyb_class_id"}


def test_free_view_has_only_whitelisted_fields():
    for line in (ROOT / "data" / "rcomp_free_view.jsonl").read_text().splitlines():
        keys = set(json.loads(line))
        assert keys <= WHITELIST | DERIVED, keys - WHITELIST - DERIVED


def test_firewall_sha_matches_disk():
    fw = json.loads((ROOT / "results" / "firewall.json").read_text())
    assert fw["firewalled_view_sha256"] == hashlib.sha256((ROOT / "data" / "rcomp_free_view.jsonl").read_bytes()).hexdigest()
    assert fw["files_never_opened"] == ["free_labels.jsonl"]


def test_no_free_rows_or_labels_in_outputs():
    free_keys = {json.loads(x)["row_key"] for x in (ROOT / "data" / "rcomp_free_view.jsonl").read_text().splitlines()}
    mo = json.loads((ROOT / "method_out.json").read_text())
    for ds in mo["datasets"]:
        for ex in ds["examples"]:
            assert ex.get("metadata_row_key") not in free_keys
    # no file this artifact wrote references the FREE label file except the documentation of the firewall itself
    allowed = {"firewall.json", "prereg_csc_P.json", "README.md", "tables.md", "deviations.json", "rcomp_free_labelfree.json"}
    for p in list((ROOT / "results").glob("*")) + list((ROOT / "data").glob("*.json*")):
        if p.is_file() and p.name not in allowed and p.stat().st_size < 50_000_000:
            assert "free_labels" not in p.read_text(errors="ignore"), p
