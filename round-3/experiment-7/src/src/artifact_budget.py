"""ONE artifact-wide budget for every OpenRouter call of this artifact (all vendored clients call guard() and book()).

* book(rec) appends {utc, phase, model, usd, prompt_tokens, completion_tokens, client} to <ART_ROOT>/cost_ledger.jsonl
  under an exclusive file lock (several processes may spend concurrently: SIG generation, FREE generation, judges).
* guard(phase) returns an error string (-> the calling client raises its own BudgetExceeded) when
    - the artifact total (all processes, read incrementally from the ledger) would cross ARTIFACT_CAP_USD ($9.5), or
    - the shared OpenRouter key has less than KEY_FLOOR_USD left (checked at most every KEY_CHECK_S seconds).
The key is shared by every run on the box; the floor keeps this artifact from draining it to zero.
Nothing here prints or stores the key.
"""
from __future__ import annotations

import fcntl
import json
import os
import time
from pathlib import Path

ART_ROOT = Path(os.environ.get("ART_ROOT", Path(__file__).resolve().parents[1]))
LEDGER = ART_ROOT / "cost_ledger.jsonl"
ARTIFACT_CAP_USD = float(os.environ.get("ART_CAP_USD", "9.5"))
KEY_FLOOR_USD = float(os.environ.get("ART_KEY_FLOOR_USD", "0.25"))
KEY_CHECK_S = 30.0
MARGIN_USD = 0.05  # in-flight calls (<= concurrency x a few tenths of a cent)

_state = {"offset": 0, "total": 0.0, "by_phase": {}, "key_t": 0.0, "key_rem": None}


def _refresh() -> None:
    if not LEDGER.exists():
        return
    with LEDGER.open("rb") as f:
        f.seek(_state["offset"])
        chunk = f.read()
    if not chunk:
        return
    last_nl = chunk.rfind(b"\n")
    if last_nl < 0:
        return
    for line in chunk[:last_nl].splitlines():
        if not line.strip():
            continue
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        u = float(r.get("usd") or 0.0)
        _state["total"] += u
        _state["by_phase"][r.get("phase", "?")] = _state["by_phase"].get(r.get("phase", "?"), 0.0) + u
    _state["offset"] += last_nl + 1


def total() -> float:
    _refresh()
    return _state["total"]


def by_phase() -> dict:
    _refresh()
    return dict(_state["by_phase"])


def key_remaining(force: bool = False) -> float | None:
    """limit_remaining of the shared key (None if unknown / no limit). Cached KEY_CHECK_S seconds."""
    now = time.time()
    if not force and now - _state["key_t"] < KEY_CHECK_S:
        return _state["key_rem"]
    import requests
    try:
        d = requests.get(os.environ["OPENROUTER_BASE_URL"].rstrip("/") + "/key",
                         headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"}, timeout=20).json()["data"]
        rem = d.get("limit_remaining")
        _state["key_rem"] = None if rem is None else float(rem)
    except Exception:  # noqa: BLE001 - an unknown key state must not stop the run; the artifact cap still applies
        _state["key_rem"] = None
    _state["key_t"] = now
    return _state["key_rem"]


def guard(phase: str) -> str | None:
    t = total()
    if t + MARGIN_USD >= ARTIFACT_CAP_USD:
        return f"artifact hard cap ${ARTIFACT_CAP_USD} reached (spent ${t:.4f}) [{phase}]"
    kr = key_remaining()
    if kr is not None and kr < KEY_FLOOR_USD:
        return f"shared key below floor: ${kr:.3f} < ${KEY_FLOOR_USD} [{phase}]"
    return None


def book(*, phase: str, model: str, usd: float, prompt_tokens=None, completion_tokens=None, client: str = "") -> None:
    rec = {"utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "ts": time.time(), "phase": phase, "model": model,
           "usd": float(usd or 0.0), "prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens, "client": client}
    with LEDGER.open("a", encoding="utf-8") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(json.dumps(rec) + "\n")
        f.flush()
        fcntl.flock(f, fcntl.LOCK_UN)


if __name__ == "__main__":
    import sys
    kr = key_remaining(force=True)
    print(json.dumps({"artifact_total_usd": round(total(), 4), "by_phase": {k: round(v, 4) for k, v in by_phase().items()},
                      "key_limit_remaining": kr, "cap": ARTIFACT_CAP_USD, "key_floor": KEY_FLOOR_USD}))
    sys.exit(0)
