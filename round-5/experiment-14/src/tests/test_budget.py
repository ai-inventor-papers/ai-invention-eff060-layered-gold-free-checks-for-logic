"""Budget guard: a client whose stop is at or below the current spend refuses to call (dry run, no network), and the
ledger's cumulative_usd equals the running sum of per-call usd."""
import asyncio
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
import gloss_client as GC  # noqa: E402


def test_stop_triggers_without_calling(monkeypatch):
    monkeypatch.setenv("OPENROUTER_BASE_URL", "http://127.0.0.1:9")
    monkeypatch.setenv("OPENROUTER_API_KEY", "dry-run")
    c = GC.Client("google/gemini-2.5-flash", "test", stop_at=min(0.01, GC.spent()))
    with pytest.raises(GC.BudgetStop):
        asyncio.run(c.chat(None, [{"role": "user", "content": "x"}], 1))


def test_ledger_cumulative_matches_sum():
    lines = [json.loads(l) for l in (ROOT / "cost_ledger.jsonl").read_text().splitlines() if l.strip()]
    tot = sum(float(x.get("usd") or 0) for x in lines)
    assert abs(tot - GC.spent()) < 1e-12
    assert abs(lines[-1]["cumulative_usd"] - tot) < 1e-5
    assert tot < 2.0
