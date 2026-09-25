#!/usr/bin/env python3
"""STEP 0.5: one 1-token key probe to the cheapest generator slot (G9 command-r7b) through the frozen or_client."""
import asyncio, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from or_client import Client  # noqa: E402

async def main():
    async with Client("probe", phase_cap=0.01, concurrency=1) as c:
        r = await c.chat("cohere/command-r7b-12-2024", [{"role": "user", "content": "Say OK"}], tag="probe", retries=1, max_tokens=1, temperature=0)
    print(json.dumps({k: r[k] for k in ("text", "error", "cost_usd", "model_returned")}))
asyncio.run(main())
