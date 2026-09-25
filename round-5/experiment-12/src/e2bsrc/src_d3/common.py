"""Shared paths, imports of dataset E's code, and small helpers for the R_COMP / PERTURB pipeline."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
E_DIR = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_dataset_1")
for p in (ROOT / "labeller", ROOT / "src_e", ROOT / "src"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
sys.setrecursionlimit(10000)
import nltk  # noqa: E402

nltk.data.path.insert(0, str(ROOT / "nltk_data"))

W = ROOT / "work"
RAW = ROOT / "raw"
LOGS = ROOT / "logs"
for d in (W, RAW, LOGS):
    d.mkdir(exist_ok=True)


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest()


def load_jsonl(p: Path) -> list[dict]:
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def append_jsonl(p: Path, rec: dict) -> None:
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def dump(p: Path, obj) -> None:
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=1))


def setup_logger(name: str):
    from loguru import logger
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(LOGS / f"{name}.log", rotation="30 MB", level="DEBUG")
    return logger
