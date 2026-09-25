#!/usr/bin/env python3
"""Marker poller (shared cross-artifact contract). Every 5 min until 16:38 UTC it globs for
  M1 .../iter_5/gen_art/*/freeze/CONSENSUS_FREEZE_READY.json   token aii_iter5_consensus_freeze_v1
  M2 .../iter_5/gen_art/*/e2/E2_DRIFT_DECISION.json            token aii_iter5_e2_drift_v1
  M3 .../iter_5/gen_art/*/e2/E2A_FINAL_READY.json              token aii_iter5_e2a_final_v1
logs every attempt to logs/marker_polls.jsonl, and on a valid marker:
  M1 -> copies the frozen files it lists into freeze_copy/ after verifying their sha256 (never imports across paths);
  M2 -> writes e2b/drift_decision.json {source: M2, decision, pins, marker copy};
  M3 -> writes e2b/m3_pointer.json (marker copy + path + sha check).
At the M2 deadline (12:38 UTC) with no decision it runs our own drift gate (src/own_drift_gate.py, deviation D-E2B-drift).
Paths found by glob are read-only; nothing is written outside this workspace."""
from __future__ import annotations

import glob
import hashlib
import json
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

WS = Path(__file__).resolve().parents[1]
BASE = str(Path(__file__).resolve().parents[4] / "round-5")
LOG = WS / "logs" / "marker_polls.jsonl"
M2_DEADLINE = "12:38"
END = "16:38"


def now() -> str:
    return datetime.now(timezone.utc).strftime("%H:%M")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def log(rec: dict) -> None:
    rec["ts_utc"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with LOG.open("a") as f:
        f.write(json.dumps(rec) + "\n")


def find(pattern: str, token: str):
    for p in sorted(glob.glob(f"{BASE}/{pattern}")):
        if str(WS) in p:
            continue
        try:
            d = json.loads(Path(p).read_text())
        except (json.JSONDecodeError, OSError) as e:
            log({"marker": pattern, "path": p, "status": f"unreadable {e}"})
            continue
        if json.dumps(d).find(token) >= 0:
            return Path(p), d
        log({"marker": pattern, "path": p, "status": "token mismatch"})
    return None, None


def _walk_shas(d, acc):
    if isinstance(d, dict):
        for k, v in d.items():
            if isinstance(v, str) and len(v) == 64 and all(c in "0123456789abcdef" for c in v):
                acc[k] = v
            _walk_shas(v, acc)
    elif isinstance(d, list):
        for v in d:
            _walk_shas(v, acc)
    return acc


def handle_m1(p: Path, d: dict) -> dict:
    fz = p.parent
    dst = WS / "freeze_copy"
    dst.mkdir(exist_ok=True)
    shas = _walk_shas(d, {})
    out = {"marker_path": str(p), "marker_sha256": sha(p), "files": {}}
    for f in sorted(fz.iterdir()):
        if f.is_file():
            h = sha(f)
            listed = [k for k, v in shas.items() if v == h]
            shutil.copy2(f, dst / f.name)
            out["files"][f.name] = {"sha256": h, "matches_marker_key": listed, "copied": True}
    (dst / "CONSENSUS_FREEZE_READY.copy.json").write_text(json.dumps(d, indent=1))
    (WS / "e2b" / "m1_copy_record.json").write_text(json.dumps(out, indent=1))
    return out


MODEL2MEMBER = {"anthropic/claude-haiku-4.5": "P1", "z-ai/glm-4.6": "P3", "moonshotai/kimi-k2-0905": "R1"}


def pins_from(d: dict) -> dict:
    """-> {member: [provider order]}; marker keys may be member ids or model ids (E2-A uses model ids)."""
    raw = _pins_raw(d)
    return {MODEL2MEMBER.get(k, k): v for k, v in raw.items()}


def _pins_raw(d: dict) -> dict:
    for k in ("pins", "pinned_providers", "pinned_provider", "providers", "provider_pins"):
        v = d.get(k)
        if isinstance(v, dict) and v:
            out = {}
            for m, x in v.items():
                if isinstance(x, str):
                    out[m] = [x]
                elif isinstance(x, list):
                    out[m] = [str(y) for y in x]
                elif isinstance(x, dict):
                    o = x.get("order") or x.get("provider") or x.get("providers")
                    out[m] = [o] if isinstance(o, str) else list(o or [])
            return out
    return {}


def main() -> None:
    got = {"M1": False, "M1_gg_final": False, "M2": False, "M3": False}
    own_gate_started = False
    while True:
        t = now()
        m1p, m1 = find("*/freeze/CONSENSUS_FREEZE_READY.json", "aii_iter5_consensus_freeze_v1")
        m2p, m2 = find("*/e2/E2_DRIFT_DECISION.json", "aii_iter5_e2_drift_v1")
        m3p, m3 = find("*/e2/E2A_FINAL_READY.json", "aii_iter5_e2a_final_v1")
        log({"attempt": t, "M1": str(m1p) if m1p else None, "M2": str(m2p) if m2p else None, "M3": str(m3p) if m3p else None})
        if m1p:
            gg = json.dumps(m1).upper()
            gg_final = ("PASS" in gg or "FAIL" in gg) and "PENDING" not in json.dumps(m1.get("GG", m1.get("gg", ""))).upper()
            if not got["M1"] or (gg_final and not got["M1_gg_final"]) or sha(m1p) != got.get("M1_sha"):
                rec = handle_m1(m1p, m1)
                got["M1"], got["M1_sha"], got["M1_gg_final"] = True, sha(m1p), gg_final
                log({"M1_copied": rec})
        if m2p and not got["M2"]:
            dec = {"source": "M2", "marker_path": str(m2p), "marker_sha256": sha(m2p), "marker": m2,
                   "decision": m2.get("decision") or m2.get("status") or ("PASS" if m2.get("passes") else "FAIL"),
                   "pins": pins_from(m2), "read_at_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
            dd = WS / "e2b" / "drift_decision.json"
            if dd.exists():  # our own gate already decided: record E2-A's decision alongside (the union uses E2-A's)
                (WS / "e2b" / "drift_decision_M2_late.json").write_text(json.dumps(dec, indent=1))
            else:
                dd.write_text(json.dumps(dec, indent=1))
            got["M2"] = True
            log({"M2_used": dec["decision"], "pins": dec["pins"]})
        if m3p and not got["M3"]:
            (WS / "e2b" / "m3_pointer.json").write_text(json.dumps({"marker_path": str(m3p), "marker_sha256": sha(m3p), "marker": m3}, indent=1))
            got["M3"] = True
            log({"M3_found": str(m3p)})
        if not got["M2"] and not own_gate_started and t >= M2_DEADLINE and not (WS / "e2b" / "drift_decision.json").exists():
            own_gate_started = True
            log({"own_drift_gate": "starting (M2 absent at deadline)"})
            subprocess.Popen([sys.executable, str(WS / "src" / "own_drift_gate.py")], stdout=open(WS / "logs" / "own_drift_gate.log", "a"),
                             stderr=subprocess.STDOUT, cwd=str(WS))
        if t >= END or (got["M3"] and got["M1_gg_final"] and (got["M2"] or own_gate_started) and t >= "15:10"):
            log({"poller": "exit"})
            break
        time.sleep(300)


if __name__ == "__main__":
    main()
