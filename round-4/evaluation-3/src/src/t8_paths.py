"""Absolute READ-ONLY input locations for T8 and the eval-2 import shim.

Module names in this workspace are prefixed t8_ so they never shadow eval-2's own `paths`, `stats`, `frame`, ... modules,
which are imported UNCHANGED from the eval-2 workspace (sys.path) rather than copied."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

RUN = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop")
EV2 = RUN / "iter_3/gen_art/gen_art_evaluation_2"          # art_FWy8D4_y9GBn (not declared; read-only)
E6T1 = RUN / "iter_3/gen_art/gen_art_experiment_6"         # art_7GxreYjATkC5
E7 = RUN / "iter_3/gen_art/gen_art_experiment_7"           # art_cxnoDYQNFolW (R_COMP)
E8 = RUN / "iter_3/gen_art/gen_art_experiment_8"           # art_YYD-HDzfQfEj
DSE = RUN / "iter_1/gen_art/gen_art_dataset_1"             # art_U4Hsqt4Ay9Tg (dataset E)
RES1 = RUN / "iter_3/gen_art/gen_art_research_1"           # art_VIF75I5R6f0v
AUDIT3 = RUN / "iter_3/review_report/review_report/audit"
IT2_E6 = RUN / "iter_2/gen_art/gen_art_experiment_6"
IT2_DS2 = RUN / "iter_2/gen_art/gen_art_dataset_2"
HYP4 = RUN / "iter_4/gen_strat/gen_strat_1/README.md"

ROOT = Path(__file__).resolve().parent.parent
TAB = ROOT / "tables"
RESD = ROOT / "results"
FIG = ROOT / "figures"

for _p in (EV2 / "src", EV2 / "vendor_exp5", EV2 / "vendor_exp5" / "vendor_c"):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))


def jl(p: Path) -> list[dict]:
    p = Path(p)
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def sha256_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def jdump(p: Path, o) -> None:
    Path(p).write_text(json.dumps(o, indent=1, default=lambda x: x.item() if hasattr(x, "item") else str(x)))


def write_csv(df, name: str, sources: list[str]) -> Path:
    """CSV with leading '# source: <abs path> :: <key>' provenance lines (read back with comment='#')."""
    p = TAB / name
    with p.open("w") as fh:
        for s in sources:
            fh.write(f"# source: {s}\n")
        df.to_csv(fh, index=False)
    return p
