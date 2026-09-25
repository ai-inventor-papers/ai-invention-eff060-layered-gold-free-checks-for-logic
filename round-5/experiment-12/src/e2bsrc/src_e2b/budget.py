#!/usr/bin/env python3
"""E2-B budget: spent() = e2bsrc/cost_ledger.jsonl (E2's frozen scripts) + exp5src/results/costs.jsonl (vendor_d judges,
frontier, cost-matched) + exp5src/cache/l3_cost_ledger.jsonl (L3 questionnaires) + scores/extra_ledger.jsonl (GG etc.). can_start(est) is True iff remaining - reserve >= est. CLI: budget.py [--estimate X] -> prints JSON."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WS = ROOT.parent
HARD_CAP, RESERVE = 9.5, 0.95
LEDGERS = [ROOT / "cost_ledger.jsonl", WS / "exp5src" / "results" / "costs.jsonl", WS / "exp5src" / "cache" / "l3_cost_ledger.jsonl",
           WS / "scores" / "extra_ledger.jsonl"]


def spent_by_file() -> dict:
    out = {}
    for p in LEDGERS:
        tot = 0.0
        if p.exists():
            for line in p.read_text().splitlines():
                if line.strip():
                    r = json.loads(line)
                    tot += float(r.get("cost_usd", r.get("cost", 0.0)) or 0.0)
        out[str(p.relative_to(WS))] = tot
    return out


def spent() -> float:
    return sum(spent_by_file().values())


def remaining() -> float:
    return HARD_CAP - spent()


def can_start(estimate: float) -> bool:
    return remaining() - RESERVE >= estimate


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--estimate", type=float, default=0.0)
    a = ap.parse_args()
    print(json.dumps({"spent": round(spent(), 5), "by_file": spent_by_file(), "remaining": round(remaining(), 5),
                      "can_start": can_start(a.estimate), "estimate": a.estimate}))
