#!/usr/bin/env python3
"""F1: poll the shared OpenRouter key (limit_remaining only; the key is never printed) every 10 min for up to 60 min.
Writes logs/key_poll.jsonl; exits early and writes logs/key_poll_ok.flag if limit_remaining >= the threshold."""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import artifact_budget as ART  # noqa: E402

THRESH = float(sys.argv[1]) if len(sys.argv) > 1 else 2.0
for i in range(7):
    kr = ART.key_remaining(force=True)
    rec = {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "limit_remaining": kr, "threshold": THRESH}
    with (ROOT / "logs" / "key_poll.jsonl").open("a") as fh:
        fh.write(json.dumps(rec) + "\n")
    if kr is not None and kr >= THRESH:
        (ROOT / "logs" / "key_poll_ok.flag").write_text(json.dumps(rec))
        break
    if i < 6:
        time.sleep(600)
