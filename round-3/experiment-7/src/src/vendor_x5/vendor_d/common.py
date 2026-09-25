# NOTE (published copy): this file names server paths this repository
# does not publish (a stage it does not ship, or another run's workspace),
# so the steps that read them will not run from a clone as written:
#   /ai-inventor/aii_data/runs/run_u75jRHUss0zo/iter_3/gen_hypo/claude_agent/data
"""Shared helpers: paths, normalisation, item ids, hardware limits, json io."""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import resource
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]  # VENDOR PATCH (iter2 exp5): workspace root; PATCH iter3 exp7: one level deeper (src/vendor_x5/vendor_d)
DATA = ROOT / "data"
RES = ROOT / "results"
TAB = RES / "tables"
LOGS = ROOT / "logs"
SRC_DATA = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/iter_3/gen_hypo/claude_agent/data")
for _d in (DATA, RES, TAB, LOGS):
    _d.mkdir(parents=True, exist_ok=True)

SYSTEMS = ["gpt-3.5-turbo", "gpt-4", "text-davinci-003"]

_QUOTES = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", "—": "-", "−": "-"})


def norm(s: str) -> str:
    s = (s or "").translate(_QUOTES).lower()
    s = re.sub(r"[^\w\s]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()


def item_id(system: str, text: str, cand_raw: str | None) -> str:
    return sha1(f"{system}|{norm(text)}|{(cand_raw or '').strip()}")[:16]


def detect_cpus() -> int:
    try:
        q = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_quota_us").read_text())
        p = int(Path("/sys/fs/cgroup/cpu/cpu.cfs_period_us").read_text())
        if q > 0:
            return math.ceil(q / p)
    except (FileNotFoundError, ValueError):
        pass
    try:
        parts = Path("/sys/fs/cgroup/cpu.max").read_text().split()
        if parts[0] != "max":
            return math.ceil(int(parts[0]) / int(parts[1]))
    except (FileNotFoundError, ValueError):
        pass
    return len(os.sched_getaffinity(0))


def set_ram_limit(gb: float) -> None:
    b = int(gb * 1024 ** 3)
    resource.setrlimit(resource.RLIMIT_AS, (b, b))


def jdump(obj, p: Path, indent: int | None = 1) -> None:
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=indent, default=_default))


def _default(o):
    import numpy as np
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return None if np.isnan(o) else float(o)
    if isinstance(o, (set, tuple)):
        return list(o)
    raise TypeError(type(o))


def jload(p: Path):
    return json.loads(Path(p).read_text())


def read_jsonl(p: Path) -> list[dict]:
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]


def disable_triton_overrides() -> None:
    """torch 2.14 routes some aten ops (e.g. bmm outer products in RoPE) to Triton kernels that need a C compiler at
    first use; this box has none, so fall back to the native ATen kernels."""
    try:
        from torch._native import registry as R
        R.deregister_op_overrides(disable_dsl_names=["triton"])
    except (ImportError, AttributeError):
        pass
