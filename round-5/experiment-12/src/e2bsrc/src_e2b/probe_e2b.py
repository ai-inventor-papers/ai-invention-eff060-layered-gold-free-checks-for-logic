#!/usr/bin/env python3
"""E2-B step 0.1 / testing plan 3: 1-token OpenRouter probe (booked in cost_ledger.jsonl, phase 'probe') and a $0
catalog check that every generator slot, panel member and judge id is still served. -> work/models_snapshot_E2B.json"""
import asyncio
import json
import os
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from or_client import Client  # noqa: E402

IDS = {"G1": "meta-llama/llama-3.1-8b-instruct", "G1b": "meta-llama/llama-3.3-70b-instruct", "G2": "qwen/qwen3-235b-a22b-2507",
       "G3": "mistralai/mistral-small-3.2-24b-instruct", "G4": "deepseek/deepseek-v3.2", "G5": "google/gemma-3-27b-it",
       "G6": "microsoft/phi-4", "G7": "openai/gpt-4.1-mini", "G8": "google/gemini-2.5-flash", "G9": "cohere/command-r7b-12-2024",
       "P1": "anthropic/claude-haiku-4.5", "P3": "z-ai/glm-4.6", "R1": "moonshotai/kimi-k2-0905",
       "J_flashlite": "google/gemini-2.5-flash-lite", "J_nano": "openai/gpt-4.1-nano", "J_costmatched": "deepseek/deepseek-v3.2",
       "J_frontier": "google/gemini-3.1-pro-preview"}


async def probe():
    async with Client("probe", phase_cap=0.01, concurrency=1) as c:
        return await c.chat("meta-llama/llama-3.1-8b-instruct", [{"role": "user", "content": "Say OK"}], tag="probe", max_tokens=1, temperature=0)


def main():
    r = asyncio.run(probe())
    base = os.environ["OPENROUTER_BASE_URL"].rstrip("/")
    cat = requests.get(base + "/models", headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"}, timeout=60).json()
    data = cat["data"] if isinstance(cat, dict) else cat
    by = {m["id"]: m for m in data}
    served = {k: {"id": v, "served": v in by, "pricing": by.get(v, {}).get("pricing")} for k, v in IDS.items()}
    (ROOT / "work" / "models_snapshot_E2B.json").write_text(json.dumps({"ts_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                                                                          "n_catalog": len(data), "ids": served}, indent=1))
    print(json.dumps({"probe_text": r["text"], "probe_error": r["error"], "probe_cost": r["cost_usd"], "provider": r["provider"],
                      "not_served": [k for k, v in served.items() if not v["served"]]}))


if __name__ == "__main__":
    main()
