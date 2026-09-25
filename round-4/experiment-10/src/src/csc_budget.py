"""Append-only API cost ledger with a HARD STOP.

Every OpenRouter call made by this artifact is recorded in `results/api_cost_ledger.jsonl`
(ts, stage, model, key_hash, prompt_tokens, completion_tokens, cost_usd = usage.cost, latency_s, cache_hit).
`check(reserve)` is called BEFORE every call: it raises BudgetExceeded when cumulative + reserve would pass HARD_CAP.
SOFT_CAP marks the point where the pre-declared shrink order (README / prereg) is applied by the caller.
The key itself is never written: only sha256(key)[:10] is stored so different keys can be told apart.
"""
from __future__ import annotations

import hashlib
import json
import os
import threading
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "results" / "api_cost_ledger.jsonl"
HARD_CAP = 9.5
SOFT_CAP = 8.5


class BudgetExceeded(RuntimeError):
    pass


_lock = threading.Lock()
_total: float | None = None


def key_hash() -> str:
    return hashlib.sha256(os.environ.get("OPENROUTER_API_KEY", "").encode()).hexdigest()[:10]


def cumulative() -> float:
    """Total $ spent so far (read once from disk, then tracked in memory)."""
    global _total
    with _lock:
        if _total is None:
            t = 0.0
            if LEDGER.exists():
                for line in LEDGER.read_text().splitlines():
                    if line.strip():
                        try:
                            t += float(json.loads(line).get("cost_usd") or 0.0)
                        except (json.JSONDecodeError, ValueError):
                            continue
            _total = t
        return _total


def check(reserve: float = 0.002) -> None:
    """Raise BudgetExceeded if spending `reserve` more would pass the hard cap."""
    if cumulative() + reserve > HARD_CAP:
        raise BudgetExceeded(f"cumulative ${cumulative():.4f} + reserve ${reserve:.4f} > hard cap ${HARD_CAP}")


def soft_exceeded() -> bool:
    return cumulative() > SOFT_CAP


def record(*, stage: str, model: str, prompt_tokens: int | None, completion_tokens: int | None, cost_usd: float,
           latency_s: float, status: str = "ok") -> None:
    global _total
    cumulative()
    rec = {"ts": round(time.time(), 3), "stage": stage, "model": model, "key_hash": key_hash(),
           "prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens, "cost_usd": float(cost_usd or 0.0),
           "latency_s": round(latency_s, 3), "status": status}
    with _lock:
        LEDGER.parent.mkdir(parents=True, exist_ok=True)
        with LEDGER.open("a") as f:
            f.write(json.dumps(rec) + "\n")
        _total = (_total or 0.0) + float(cost_usd or 0.0)
