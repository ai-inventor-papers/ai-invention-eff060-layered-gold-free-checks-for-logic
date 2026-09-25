"""Label-side helpers (imported ONLY by post-seal scripts): the R_AB frame, T9 error classes (exp 9 analyse.py classes(),
verbatim logic), eval-3/exp-5 op_class (vendor_c common.op_class + COARSE, verbatim)."""
from __future__ import annotations

import json

import numpy as np
import pandas as pd

from common import PER_ITEM, ROOT, RES, jl, sha256_file

COARSE = {"ADD": "COVERAGE", "DROP": "COVERAGE", "NEG": "POLARITY", "REV": "POLARITY", "QUANT": "POLARITY"}
T9 = ["ADD", "DROP", "COMPOUND", "polarity(NEG/REV/QUANT)", "structural(CONN/RESTR/BIND/MOVE/SWAP/SCOPE/UNGLUE)",
      "MEANING_RENAME-type (MEANING_RENAME op or tier-B VOCAB_GRAN)"]


def op_class(ops) -> str:
    """eval-2 vendor_exp5/vendor_c/common.py op_class (verbatim)."""
    ops = list(ops) if ops is not None and not isinstance(ops, float) else []
    if not ops:
        return "NONE"
    cs = {COARSE.get(o, "STRUCT") for o in ops}
    return cs.pop() if len(cs) == 1 else "MIXED"


def t9_classes(error_ops, auto_label) -> list[str]:
    """exp 9 src/analyse.py (e) classes(r), verbatim logic."""
    ops = set(error_ops or [])
    out = []
    if "ADD" in ops: out.append("ADD")
    if "DROP" in ops: out.append("DROP")
    if "COMPOUND" in ops: out.append("COMPOUND")
    if ops & {"NEG", "REV", "QUANT"}: out.append("polarity(NEG/REV/QUANT)")
    if ops & {"CONN", "RESTR", "BIND", "MOVE", "SWAP", "SCOPE", "UNGLUE"}: out.append("structural(CONN/RESTR/BIND/MOVE/SWAP/SCOPE/UNGLUE)")
    if "MEANING_RENAME" in ops or auto_label == "VOCAB_GRAN": out.append("MEANING_RENAME-type (MEANING_RENAME op or tier-B VOCAB_GRAN)")
    return out


def check_seal(name: str = "prereg_improve_addendum.json", key: str = "scores_sha256", path: str = "results/scores_E_variants.jsonl"):
    add = json.loads((ROOT / name).read_text())
    h = sha256_file(ROOT / path)
    assert add[key] == h, f"SEAL BROKEN: {path} {h} != {add[key]}"
    return add


def frame() -> pd.DataFrame:
    """All E rows: sealed variant scores joined with labels + frozen comparator columns (post-seal only)."""
    check_seal()
    S = pd.DataFrame(jl(RES / "scores_E_variants.jsonl"))
    keep = ["canonical_key", "in_R_AB", "pool", "parse_ok", "y_R_AB", "final_label", "auto_label", "error_ops", "label_tier",
            "judge_cheap_disg", "judge_cheap_orig", "judge_cheap2_orig", "p_peer_text", "S4_full_oof", "system", "prompt_variant"]
    L = []
    for r in jl(PER_ITEM):
        d = {k: r.get(k) for k in keep}
        d["words"] = r["strata"]["words"]
        d["n_conditions"] = r["strata"]["n_conditions"]
        L.append(d)
    df = S.merge(pd.DataFrame(L), on="canonical_key", how="left", validate="one_to_one")
    df["R_AB"] = df.in_R_AB.fillna(False).astype(bool) & (df.pool == "E_POOL") & df.parse_ok.fillna(False).astype(bool)
    df["Z"] = df.R_AB & df.in_matrix & (df.n_peers >= 2)
    df["y"] = df.y_R_AB
    df["long"] = df.stratum.isin(["L25", "L20", "EXC"])
    df["words_t"] = np.where(df.words <= 20, "T1", np.where(df.words <= 26, "T2", "T3"))
    df["t9"] = [t9_classes(o, a) if y == 1 else [] for o, a, y in zip(df.error_ops, df.auto_label, df.y)]
    df["opc"] = [op_class(o) for o in df.error_ops]
    v4p = RES / "scores_E_V4.jsonl"
    if v4p.exists():
        check_seal("prereg_improve_addendum_v4.json", "v4_sha256", "results/scores_E_V4.jsonl")
        V4 = pd.DataFrame(jl(v4p))[["row_key", "V4"]]
        df = df.merge(V4, on="row_key", how="left", validate="one_to_one")
    return df
