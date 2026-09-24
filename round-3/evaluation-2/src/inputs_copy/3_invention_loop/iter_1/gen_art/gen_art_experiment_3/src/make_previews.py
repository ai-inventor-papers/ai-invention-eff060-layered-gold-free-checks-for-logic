#!/usr/bin/env python3
"""Mini (3 examples per dataset) and preview (mini + strings truncated to 200 chars) variants of method_out.json."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def trunc(x):
    if isinstance(x, str):
        return x[:200]
    if isinstance(x, list):
        return [trunc(v) for v in x]
    if isinstance(x, dict):
        return {k: trunc(v) for k, v in x.items()}
    return x


if __name__ == "__main__":
    d = json.loads((ROOT / "method_out.json").read_text())
    mini = {"metadata": d["metadata"], "datasets": [{"dataset": s["dataset"], "examples": s["examples"][:3]} for s in d["datasets"]]}
    (ROOT / "mini_method_out.json").write_text(json.dumps(mini, ensure_ascii=False, indent=1))
    (ROOT / "preview_method_out.json").write_text(json.dumps(trunc(mini), ensure_ascii=False, indent=1))
    print("wrote mini_method_out.json, preview_method_out.json")
