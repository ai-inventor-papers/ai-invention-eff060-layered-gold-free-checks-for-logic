"""Paths (READ-ONLY inputs of run_u75jRHUss0zo), IO helpers and logging setup shared by every script of this artifact."""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from pathlib import Path

RUN = Path(__file__).resolve().parents[4]
DS_E = RUN / "iter_1/gen_art/gen_art_dataset_1"            # art_U4Hsqt4Ay9Tg (dataset E)
DS3 = RUN / "iter_2/gen_art/gen_art_dataset_3"             # art_zcwCQgTqk6DN (PERTURB / R_COMP)
E5 = RUN / "iter_2/gen_art/gen_art_experiment_5"           # frozen c_score_align code / per_item_E
E6 = RUN / "iter_3/gen_art/gen_art_experiment_6"           # per_item_T1.jsonl (labels + frozen columns)
EV2 = RUN / "iter_3/gen_art/gen_art_evaluation_2"          # pairwise_classes_E.jsonl
E8 = RUN / "iter_3/gen_art/gen_art_experiment_8"           # perturb_scores.jsonl, pairs_E.jsonl, consensus_lib
E9 = RUN / "iter_4/gen_art/gen_art_experiment_9"           # T9 classes
EV3 = RUN / "iter_4/gen_art/gen_art_evaluation_3"          # R_oracle
DS5 = RUN / "iter_4/gen_art/gen_art_dataset_5"             # freelab / gloss gate items
E1 = RUN / "iter_1/gen_art/gen_art_experiment_1"           # fol_triage

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
