"""Mutation test of the checker: a verifier that cannot fail proves nothing.
Inject 10 perturbed claims (last digit changed, CI bounds swapped, sign flipped) -> all must be
MISMATCH; re-check 10 untouched claims -> all must be MATCH."""
from __future__ import annotations

import copy
import json
from pathlib import Path

from src import checker as CK


def _bump_last_digit(lit: str) -> str:
    for i in range(len(lit) - 1, -1, -1):
        if lit[i].isdigit():
            d = int(lit[i])
            return lit[:i] + str((d + 3) % 10) + lit[i + 1:]
    return lit


def _flip_sign(lit: str) -> str:
    t = lit.strip()
    if t.startswith(("+",)):
        return "−" + t[1:]
    if t.startswith(("−", "-")):
        return "+" + t[1:]
    return "−" + t


def mutation_test(claims: list[dict], out: Path) -> dict:
    ids_digit = ["t1_delta", "x9_csc", "x9_e_csc", "e3_calib", "x10_sigproxy"]
    ids_swap = ["x9_d_fexact", "t1_long", "e3_drop"]
    ids_sign = ["x9_d_calign", "t1_nested"]
    by = {c["id"]: c for c in claims}
    muts = []
    for i in ids_digit:
        m = copy.deepcopy(by[i]); m["value"] = _bump_last_digit(m["value"]); m["pp"] = None
        muts.append(("last_digit", i, m))
    for i in ids_swap:
        m = copy.deepcopy(by[i]); lo, hi = CK.parse_ci(m["ci"]); m["ci"] = f"[{hi}, {lo}]"; m["pp"] = None
        muts.append(("ci_swapped", i, m))
    for i in ids_sign:
        m = copy.deepcopy(by[i]); m["value"] = _flip_sign(m["value"]); m["pp"] = None
        muts.append(("sign_flip", i, m))
    res = {"mutated": [], "untouched": []}
    for kind, i, m in muts:
        r = CK.check_claim(m)
        res["mutated"].append(dict(kind=kind, id=i, mutated_value=m["value"], mutated_ci=m.get("ci"), status=r["match_hyp_vs_file"]))
    for i in ["t1_l25", "t1_ratio", "x9_fexact", "x9_calign", "x9_t9_COMPOUND_CSC", "x10_free3", "e3_77", "d5_707", "ev2_net", "x9_m3_gee"]:
        r = CK.check_claim(by[i])
        res["untouched"].append(dict(id=i, value=by[i]["value"], status=r["match_hyp_vs_file"]))
    res["caught"] = sum(x["status"] == "MISMATCH" for x in res["mutated"])
    res["untouched_match"] = sum(x["status"] == "MATCH" for x in res["untouched"])
    res["PASS"] = res["caught"] == 10 and res["untouched_match"] == 10
    out.write_text(json.dumps(res, indent=1))
    return res
