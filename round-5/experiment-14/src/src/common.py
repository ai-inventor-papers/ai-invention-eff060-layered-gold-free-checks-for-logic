"""Paths (READ-ONLY inputs of run_u75jRHUss0zo), IO helpers and logging setup shared by every script of this artifact."""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path

RUN = Path(__file__).resolve().parents[4]
DS_E = RUN / "round-1/dataset-1/src"            # art_U4Hsqt4Ay9Tg (dataset E)
DS3 = RUN / "round-2/dataset-3/src"             # art_zcwCQgTqk6DN (PERTURB / R_COMP)
E5 = RUN / "round-2/experiment-5/src"           # frozen c_score_align code / per_item_E
E6 = RUN / "round-3/experiment-6/src"           # per_item_T1.jsonl (labels + frozen columns)
EV2 = RUN / "round-3/evaluation-2/src"          # pairwise_classes_E.jsonl
E8 = RUN / "round-3/experiment-8/src"           # perturb_scores.jsonl, pairs_E.jsonl, consensus_lib
E9 = RUN / "round-4/experiment-9/src"           # T9 classes
EV3 = RUN / "round-4/evaluation-3/src"          # R_oracle
DS5 = RUN / "round-4/dataset-5/src"             # freelab / gloss gate items
E1 = RUN / "round-1/experiment-1/src"           # fol_triage

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "results"
TAB = ROOT / "tables"
FREEZE = ROOT / "freeze"
LOGS = ROOT / "logs"
for _d in (RES, TAB, FREEZE, LOGS):
    _d.mkdir(exist_ok=True)

MATRIX = EV2 / "pairwise_classes_E.jsonl"
PER_ITEM = E6 / "results" / "per_item_T1.jsonl"
PERTURB_SCORES = E8 / "results" / "perturb_scores.jsonl"
STRATA = ("L25", "L20", "EXC", "CTRL")
LONG = ("L25", "L20", "EXC")
NEUTRAL_C = 0.6266243516243516  # exp-5 prereg imputation.neutral.c_score_align (|P| < 2 rows)
SEED = 20260924
B = 2000


def jl(p) -> list[dict]:
    p = Path(p)
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def jdump(obj, p) -> None:
    Path(p).write_text(json.dumps(obj, indent=1, ensure_ascii=False, default=_default))


def _default(o):
    import numpy as np
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return None if np.isnan(o) else float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (set, tuple)):
        return list(o)
    raise TypeError(type(o))


def sha256_file(p) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest()


def utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def setup_logger(name: str):
    from loguru import logger
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(LOGS / f"{name}.log", rotation="30 MB", level="DEBUG")
    return logger


def atomic_write(p, text: str) -> None:
    p = Path(p)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(text)
    os.replace(tmp, p)
