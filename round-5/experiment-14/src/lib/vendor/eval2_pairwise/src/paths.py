"""Absolute READ-ONLY input locations (all dependency workspaces of run_u75jRHUss0zo) and small IO helpers."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

RUN = Path(__file__).resolve().parents[7]
E5 = RUN / "round-2/experiment-5/src"
E6 = RUN / "iter_2/gen_art/gen_art_experiment_6"
DS_E = RUN / "round-1/dataset-1/src"
DS2 = RUN / "iter_2/gen_art/gen_art_dataset_2"
DS3 = RUN / "round-2/dataset-3/src"
EV1 = RUN / "round-2/evaluation-1/src"
REVIEW = RUN / "iter_2/review_report/review_report"
I1 = RUN / "round-1"
ROOT = Path(__file__).resolve().parent.parent


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()] if Path(p).exists() else []


def sha256_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()
