#!/usr/bin/env python3
"""After the run-budget stop: every 15 min until 15:38 UTC (T+4:30, the pre-registered last paid call), make a 1-token
probe through the base URL (cheapest slot, G9). Every attempt is logged to logs/budget_polls.jsonl. When a probe succeeds,
remove e2b/api_blocked.flag and launch (once) the label resume driver and the judge resume chain, then keep monitoring."""
import json
import os
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

WS = Path(__file__).resolve().parents[1]
LOG = WS / "logs" / "budget_polls.jsonl"
END = "15:38"


def probe() -> tuple[bool, str]:
    try:
        r = requests.post(os.environ["OPENROUTER_BASE_URL"].rstrip("/") + "/chat/completions",
                          headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"},
                          json={"model": "cohere/command-r7b-12-2024", "messages": [{"role": "user", "content": "Say OK"}], "max_tokens": 1,
                                "temperature": 0, "usage": {"include": True}}, timeout=60)
        cost = ((r.json() or {}).get("usage") or {}).get("cost") if r.status_code == 200 else None
        if cost:
            with open(WS / "scores" / "extra_ledger.jsonl", "a") as f:
                f.write(json.dumps({"ts": time.time(), "phase": "budget_probe", "cost_usd": float(cost)}) + "\n")
        return r.status_code == 200, f"HTTP {r.status_code}: {r.text[:160]}"
    except requests.RequestException as e:
        return False, f"exc {e}"


def main():
    launched = False
    while True:
        t = datetime.now(timezone.utc).strftime("%H:%M")
        ok, msg = probe()
        with LOG.open("a") as f:
            f.write(json.dumps({"ts_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "ok": ok, "msg": msg}) + "\n")
        if ok and not launched:
            (WS / "e2b" / "api_blocked.flag").unlink(missing_ok=True)
            subprocess.Popen(["bash", str(WS / "e2bsrc/src_e2b/run_batches_resume.sh")], stdout=open(WS / "logs/run_batches_resume.log", "a"),
                             stderr=subprocess.STDOUT)
            subprocess.Popen(["bash", str(WS / "src/judge_resume.sh")], stdout=open(WS / "logs/judge_resume.log", "a"), stderr=subprocess.STDOUT)
            launched = True
        if t >= END or launched:
            break
        time.sleep(900)


if __name__ == "__main__":
    main()
