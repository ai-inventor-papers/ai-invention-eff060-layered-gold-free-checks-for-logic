#!/usr/bin/env python3
"""Deviation D4: re-issue generator calls whose FINAL failure was a transient upstream/provider error (HTTP 429 rate
limit, 5xx, timeout, connection) - infrastructure, not model behaviour; E had none (all of E's failures were key-limit
403s, which E's own generate.py already retries). Deterministic model failures (HTTP 400/404, empty content with a
200) remain data. Runs E's frozen generate.amain with done_keys() widened accordingly; the later record wins
(E's convention for duplicate keys). Usage: gen_retry.py --sentences F [--concurrency 6] [--cap 1.3]"""
import argparse
import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import generate  # noqa: E402

TRANSIENT = ("HTTP 429", "HTTP 5", "TimeoutError", "ClientError", "ClientConnector", "ServerDisconnected", "ClientPayload")


def done_keys() -> set:
    keys = set()
    if generate.GEN.exists():
        for line in generate.GEN.read_text().splitlines():
            if line.strip():
                r = json.loads(line)
                err = r.get("api_error") or ""
                if r.get("raw_output") is not None or (r.get("final_failure") and "Key limit exceeded" not in err and not any(t in err for t in TRANSIENT)):
                    keys.add((r["sentence_id"], r["slot"], r["prompt_variant"]))
    return keys


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--slots", default="G1,G1b,G2,G3,G4,G5,G6,G7,G8,G9")
    ap.add_argument("--variants", default="fewshot_v1")
    ap.add_argument("--cap", type=float, default=1.3)
    ap.add_argument("--concurrency", type=int, default=6)
    ap.add_argument("--sentences", default="work/sentences.json")
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    generate.done_keys = done_keys
    asyncio.run(generate.amain(a))
