"""Absolute READ-ONLY input locations (all dependency workspaces of run_u75jRHUss0zo) and small IO helpers."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parents[6]
E5 = RUN / "iter_2/gen_art/gen_art_experiment_5"
E6 = RUN / "iter_2/gen_art/gen_art_experiment_6"
DS_E = RUN / "iter_1/gen_art/gen_art_dataset_1"
DS2 = RUN / "iter_2/gen_art/gen_art_dataset_2"
DS3 = RUN / "iter_2/gen_art/gen_art_dataset_3"
EV1 = RUN / "iter_2/gen_art/gen_art_evaluation_1"
REVIEW = RUN / "iter_2/review_report/review_report"
I1 = RUN / "round-1"
ROOT = Path(__file__).resolve().parent.parent


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()] if Path(p).exists() else []


def sha256_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()
