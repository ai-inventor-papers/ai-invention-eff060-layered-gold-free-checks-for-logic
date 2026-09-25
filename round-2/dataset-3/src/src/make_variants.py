#!/usr/bin/env python3
"""mini_data_out.json (first 3 examples per group) and preview_data_out.json (same, strings truncated to 200 chars)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def trunc(x):
    if isinstance(x, str):
        return x[:200]
    if isinstance(x, list):
        return [trunc(v) for v in x]
    if isinstance(x, dict):
        return {k: trunc(v) for k, v in x.items()}
    return x


d = json.loads((ROOT / "full_data_out.json").read_text())
mini = {"metadata": d.get("metadata", {}), "datasets": [{"dataset": g["dataset"], "examples": g["examples"][:3]} for g in d["datasets"]]}
(ROOT / "mini_data_out.json").write_text(json.dumps(mini, ensure_ascii=False, indent=1))
(ROOT / "preview_data_out.json").write_text(json.dumps(trunc(mini), ensure_ascii=False, indent=1))
print("mini/preview written:", {g["dataset"]: len(g["examples"]) for g in mini["datasets"]})
