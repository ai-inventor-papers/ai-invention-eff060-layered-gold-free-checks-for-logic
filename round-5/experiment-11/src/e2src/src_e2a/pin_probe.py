#!/usr/bin/env python3
"""E2-A testing step 3: one small call per panel model WITH the provider pin; records served provider + model id."""
import asyncio, json, os, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.environ["AII_PROVIDER_PIN"] = (ROOT / "src_e2a" / "pin.json").read_text()
from or_client import Client  # noqa: E402

async def main():
    pin = json.loads(os.environ["AII_PROVIDER_PIN"])
    out = {}
    async with Client("pin_probe", phase_cap=0.02, concurrency=3) as c:
        rs = await asyncio.gather(*[c.chat(m, [{"role": "user", "content": "Say OK"}], tag="pin_probe", retries=2,
                                           max_tokens=5, temperature=0) for m in pin])
    for m, r in zip(pin, rs):
        out[m] = {"pinned_order": pin[m]["order"], "served_provider": r["provider"], "model_returned": r["model_returned"],
                  "error": r["error"], "ok": bool(r["provider"]) and r["provider"] in pin[m]["order"]}
    (ROOT / "src_e2a" / "pin_probe_result.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))
asyncio.run(main())
