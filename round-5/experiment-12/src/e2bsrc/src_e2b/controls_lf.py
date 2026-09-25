#!/usr/bin/env python3
"""LABEL-FREE rename controls (added while the run budget was exhausted): E2's frozen control generator
(src_e2/controls_e2.py: dataset 3 perturb.control_rename, RENAME_SYN and forced RENAME_NONCE, z3-verified under the
inverse map) applied to a sha1('E2B_lfctrl|'+row_key) sample of N PARSEABLE E2-B candidates, regardless of their label.
A rename is meaning-preserving for ANY candidate, so the paired flip (control flagged while its parent is not) and the
score shift are label-free invariance measures; FA proper (on CORRECT parents) still needs labels.
Reads only raw/generations.jsonl + <WS>/e2b/sentences_E2B.json. -> <WS>/scores/controls_lf_E2B.jsonl"""
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WS = ROOT.parent
sys.path.insert(0, str(ROOT / "src_e2"))
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "src_d3"))
sys.path.insert(0, str(ROOT / "labeller"))
sys.setrecursionlimit(10000)
import controls_e2 as C  # noqa: E402  (E2's frozen variant(): perturb.control_rename, forced-nonce branch)
from fol import parse, equivalent  # noqa: E402
from repair_census import rename  # noqa: E402
from disguise import emit  # noqa: E402

N = int(sys.argv[1]) if len(sys.argv) > 1 else 300
sents = {s["sentence_id"]: s for s in json.loads((WS / "e2b" / "sentences_E2B.json").read_text())}
rows = [json.loads(l) for l in (WS / "scores" / "rows_E2B.jsonl").read_text().splitlines() if l.strip()]
rows = sorted([r for r in rows if r["parse_ok"]], key=lambda r: hashlib.sha1(("E2B_lfctrl|" + r["row_key"]).encode()).hexdigest())[:N]
out = []
for r in rows:
    try:
        e = parse(r["candidate_fol"])
    except Exception:  # noqa: BLE001
        continue
    for want, force in (("RENAME_SYN", False), ("RENAME_NONCE", True)):
        try:
            kind, mp, e2 = C.variant(e, r["row_key"], force)
        except Exception as ex:  # noqa: BLE001
            out.append({"parent_row_key": r["row_key"], "control_type": want, "status": f"generator_error:{str(ex)[:60]}"})
            continue
        if want == "RENAME_SYN" and kind != "RENAME_SYN":
            out.append({"parent_row_key": r["row_key"], "control_type": want, "status": "syn_unavailable"})
            continue
        inv = {(nn, p[1]): p[0] for p, nn in mp.items()}
        ok = equivalent(rename(e2, inv, {}), e) is True
        out.append({"parent_row_key": r["row_key"], "control_type": want, "status": "ok" if ok else "inverse_not_equivalent",
                    "candidate_fol": emit(e2), "rename_map": {f"{p[0]}/{p[1]}": nn for p, nn in mp.items()}})
(WS / "scores" / "controls_lf_E2B.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in out))
from collections import Counter  # noqa: E402
print(json.dumps({"parents": len(rows), "controls": len(out), "status": {f"{a}|{b}": n for (a, b), n in Counter((x["control_type"], x["status"]) for x in out).items()}}))
