"""Shared paths / io / logging for the E2-A label-free scoring processes. Import scoring.guard BEFORE this module."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from loguru import logger

WS = Path(__file__).resolve().parents[1]
CAND = WS / "e2" / "candidates_E2_nolabels.jsonl"
CACHE = WS / "cache"
FROZEN = WS / "frozen"
LOGS = WS / "logs"
CACHE.mkdir(exist_ok=True)
LOGS.mkdir(exist_ok=True)


def setup_log(name: str) -> None:
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(LOGS / f"{name}.log", rotation="30 MB", level="DEBUG")


def jl(p: Path) -> list[dict]:
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


def append_jsonl(p: Path, rows: list[dict]) -> None:
    with p.open("a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def candidates() -> list[dict]:
    return jl(CAND)


def by_sentence(rows: list[dict]) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for r in rows:
        out.setdefault(r["sentence_id"], []).append(r)
    return out
