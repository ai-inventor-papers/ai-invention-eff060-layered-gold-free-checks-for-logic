"""Shared paths, the score WHITELIST loader and small helpers for the R_COMP FREE confirmation (iteration 5).

Nothing in this module reads a label file. Label files are opened only by confirm/join_and_test.py after both seals
verify. The labeller (../labeller) never imports anything from confirm/ (tests/test_firewall.py in labeller/ checks it).
"""
from __future__ import annotations

import hashlib
import json
import math
import sys
from pathlib import Path

WS = Path(__file__).resolve().parents[1]
LAB = WS / "labeller"
RES = WS / "results"
LOGS = WS / "logs"
RUN = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop")
E7 = RUN / "iter_3/gen_art/gen_art_experiment_7"
EV2 = RUN / "iter_3/gen_art/gen_art_evaluation_2"
EV3 = RUN / "iter_4/gen_art/gen_art_evaluation_3"
D5 = RUN / "iter_4/gen_art/gen_art_dataset_5"
E7_CAND = E7 / "results/rcomp_candidates.jsonl"
PAIR_MATRIX = EV3 / "results/pair_matrix_RCOMP.jsonl"
for _d in (RES, LOGS):
    _d.mkdir(exist_ok=True)

SEED = 20260924
B = 2000

# ---------------------------------------------------------------------------------------------------- whitelist
SCORE_COLS = ["c_score_align", "c_score_sig", "c_score_nf", "c_score_hyb", "g_align", "g_nf", "judge_cheap_disg",
              "judge_cheap_orig", "judge_local_disg", "judge_local_orig"]
WHITELIST = {"row_key", "item_id", "sentence_id", "condition", "template_id", "slot", "system", "family", "prompt_variant",
             "parse_ok", "coverage_status", "candidate_fol", "strata", "words", "word_tercile", "nconds_weak", "nconds_bin",
             "depth_weak", "nquant", "nested", "negated_condition", "clause_type", "cost_usd", "secs_sig", "n_peers_sig",
             "n_peers_equal_sig", "n_peers_hyb", "n_unknown_sig", *SCORE_COLS}
# every label-derived key of rcomp_candidates.jsonl; asserted absent after parsing
LABEL_KEYS = {"label", "label_source", "label_tier", "matched_reading", "repair_ops", "repair_status", "correct_not_equivalent",
              "tier_B_provisional", "panel_votes", "ref_flagged", "sig_status", "off_signature"}


def _hook(pairs):
    return {k: v for k, v in pairs if k in WHITELIST}


def load_scores(condition: str = "FREE") -> list[dict]:
    """rcomp_candidates.jsonl rows of one condition with ONLY whitelisted keys (label keys dropped at parse time)."""
    out = []
    with E7_CAND.open() as fh:
        for line in fh:
            if not line.strip():
                continue
            r = json.loads(line, object_pairs_hook=_hook)
            if r.get("condition") != condition:
                continue
            assert not (set(r) - WHITELIST), set(r) - WHITELIST
            assert not (set(r) & LABEL_KEYS)
            st = r.pop("strata", None) or {}
            for k in ("words", "word_tercile", "nconds_weak", "nconds_bin", "depth_weak", "nquant", "nested",
                      "negated_condition", "clause_type"):
                r[k] = st.get(k)
            out.append(r)
    return out


# ---------------------------------------------------------------------------------------------------- helpers
def jl(p: Path) -> list[dict]:
    p = Path(p)
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def dump(p: Path, o) -> None:
    Path(p).write_text(json.dumps(o, indent=1, ensure_ascii=False, default=_default))


def _default(x):
    if hasattr(x, "item"):
        return x.item()
    if hasattr(x, "tolist"):
        return x.tolist()
    return str(x)


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest()


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def vec_sha(pairs) -> str:
    """sha256 of the sorted (row_key, value) vector; floats rounded to 12 decimals, None kept."""
    v = sorted((k, None if x is None or (isinstance(x, float) and math.isnan(x)) else
                (round(float(x), 12) if isinstance(x, (int, float)) and not isinstance(x, bool) else x)) for k, x in pairs)
    return sha256_bytes(json.dumps(v, ensure_ascii=False).encode())


def fold_of(sid: str) -> int:
    return int(sha1("rcomp_folds_v1|" + sid), 16) % 5


def wilson(k: int, n: int, z: float = 1.96) -> list:
    if n == 0:
        return [None, None]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - h, 4), round(c + h, 4)]


def setup_logger(name: str):
    from loguru import logger
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
    logger.add(LOGS / f"{name}.log", rotation="30 MB", level="DEBUG")
    return logger
