"""STEP 0.4: 1-token OpenRouter probe of the GG checker with reasoning disabled; writes results/probe.json + ledger line."""
import json, os, time
from pathlib import Path
import httpx
ROOT = Path(__file__).resolve().parent.parent
out = {}
for model, extra in (("google/gemini-2.5-flash", {"reasoning": {"max_tokens": 0}}),):
    body = {"model": model, "messages": [{"role": "user", "content": "Reply with the single word OK."}], "max_tokens": 5,
            "temperature": 0, "usage": {"include": True}, **extra}
    r = httpx.post(os.environ["OPENROUTER_BASE_URL"].rstrip("/") + "/chat/completions", json=body, timeout=60,
                   headers={"Authorization": f"Bearer {os.environ['OPENROUTER_API_KEY']}"})
    d = r.json()
    u = d.get("usage") or {}
    out[model] = {"status": r.status_code, "content": ((d.get("choices") or [{}])[0].get("message") or {}).get("content"),
                  "usage": u, "provider": d.get("provider"), "extra": extra, "error": d.get("error")}
    with (ROOT / "cost_ledger.jsonl").open("a") as fh:
        fh.write(json.dumps({"ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "phase": "probe", "model": model,
                             "prompt_tok": u.get("prompt_tokens"), "completion_tok": u.get("completion_tokens"),
                             "reasoning_tok": (u.get("completion_tokens_details") or {}).get("reasoning_tokens"),
                             "usd": float(u.get("cost") or 0.0), "cumulative_usd": float(u.get("cost") or 0.0)}) + "\n")
(ROOT / "results" / "probe.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
