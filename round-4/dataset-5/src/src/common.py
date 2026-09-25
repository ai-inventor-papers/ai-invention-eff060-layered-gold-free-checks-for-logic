"""Shared paths, hashing and JSON helpers for the FREE name-free labeller (no metric, evaluator-model or aligner code here)."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for _p in (ROOT / "vendor", ROOT / "src"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))
sys.setrecursionlimit(10000)

RUN = Path(__file__).resolve().parents[4]
E7 = RUN / "iter_3/gen_art/gen_art_experiment_7"
D3 = RUN / "iter_2/gen_art/gen_art_dataset_3"
GEN_FREE = E7 / "rcomp/raw/generations.jsonl"          # FREE raw generations: no scores, no labels
SENTS = E7 / "rcomp/work/rcomp_sentences.json"
D3_FULL = D3 / "full_data_out.json"
LEXICON = D3 / "lexicon.json"
SIG_LABELS = E7 / "results/sig_labels.jsonl"            # SIG labels only (pure z3), no scores
OLD_CANDIDATES = E7 / "results/rcomp_candidates.jsonl"  # opened ONLY in STEP H (post-seal) via a whitelist loader
NLTK_DATA = E7 / "data/nltk_data"
RES = ROOT / "results"
WORK = ROOT / "work"
LOGS = ROOT / "logs"
for _d in (RES, WORK, LOGS):
    _d.mkdir(exist_ok=True)


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def norm_text(s: str) -> str:
    """Dataset E's select_sentences.norm (verbatim logic) used in the item_id recipe."""
    s = s.lower().replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def item_id(system: str, text: str, raw: str | None) -> str:
    """exp 7 / dataset 3 recipe: sha1(system | norm(text) | raw_output)[:16] (raw None -> '')."""
    return sha1(system + "|" + norm_text(text) + "|" + (raw or ""))[:16]


def load_jsonl(p: Path) -> list[dict]:
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]


def dump(p: Path, obj) -> None:
    Path(p).write_text(json.dumps(obj, indent=1, ensure_ascii=False))


def setup_logger(name: str):
    from loguru import logger
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(LOGS / f"{name}.log", rotation="30 MB", level="DEBUG")
    return logger
