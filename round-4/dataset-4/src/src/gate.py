#!/usr/bin/env python3
"""STEP 4b/4c: panel calibration gate in EXACTLY the production format (disguised, batched per sentence, blind).

--synthetic: work/calibration_items.json; per sentence the variants + the reference are shown together.
    Gate per model: balanced accuracy >= 0.80 AND recall >= 0.70 on FAITHFUL AND on UNFAITHFUL.
--trackh: the curated original->corrected pairs that are NOT plain-z3-equivalent (both parseable); both formulas shown
    blind. Human verdict: corrected = faithful, original = unfaithful; ambiguity-flagged pairs reported separately.
Results: work/gate_results.json (merged per mode).
"""
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from collections import defaultdict
from pathlib import Path

from loguru import logger

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "labeller"))
sys.setrecursionlimit(10000)
from or_client import Client  # noqa: E402
from panel import Panel, MEMBERS  # noqa: E402
from disguise import Disguiser  # noqa: E402
from fol import parse, equivalent  # noqa: E402

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "gate.log", level="DEBUG")
OUT = ROOT / "work" / "gate_results.json"


def load_jsonl(p):
    return [json.loads(l) for l in open(p, encoding="utf-8") if l.strip()]


def trackh_pairs():
    census = {r["id"]: r for r in json.loads((ROOT / "labeller" / "repair_census.rows.json").read_text())}
    pairs = []
    for f, src, newk in [("DSAVlab-UNIUD_MALLS_test_subset-CURATED__MALLS_instances.jsonl", "MALLS", "FOL_sentence_new"),
                         ("DSAVlab-UNIUD_FOLIO_validation-curated__FOLIO_instances.jsonl", "FOLIO-concl", "FOL_sentence")]:
        for r in load_jsonl(ROOT / "data_local" / f):
            if str(r["id"]).startswith("story"):
                continue
            try:
                o, n = parse(r["FOL_sentence_old"]), parse(r[newk])
            except Exception:  # noqa: BLE001
                continue
            if equivalent(o, n) is True:
                continue
            c = census.get(r["id"], {})
            cls = c.get("cls", "UNKNOWN")
            cc = "VOCAB_GRAN" if cls in ("VOCAB", "GRAN") else ("COMPOUND" if cls == "COMPOUND" else
                                                               ("single-op" if c.get("depth") == 1 else ("two-op" if c.get("depth") == 2 else "UNKNOWN")))
            pairs.append({"id": str(r["id"]), "src": src, "text": r["NL_sentence"], "orig": r["FOL_sentence_old"],
                          "corr": r[newk], "ambiguous": str(r.get("ambiguity")) == "True", "census_cls": cls, "census_class": cc})
    return pairs


async def run_synthetic(members, cap):
    items = json.loads((ROOT / "work" / "calibration_items.json").read_text())
    by = defaultdict(list)
    for it in items:
        by[it["sentence_id"]].append(it)
    async with Client("gate", phase_cap=cap, concurrency=12) as client:
        panel = Panel(client)
        jobs, meta = [], []
        for sid, its in by.items():
            text = its[0]["text"]
            fs = [its[0]["reference_fol"]] + [i["variant_fol"] for i in its]
            d = Disguiser("calib|" + sid, text, fs)
            shown = [("REF", d.formula(its[0]["reference_fol"]))] + [(i["calib_id"], d.formula(i["variant_fol"])) for i in its]
            for m in members:
                jobs.append(panel.judge(m, "calib|" + sid, d.text(text), shown, tag="gate"))
                meta.append((m, sid))
        res = await asyncio.gather(*jobs, return_exceptions=True)
    out = {}
    gold = {i["calib_id"]: i for i in items}
    for m in members:
        rows = []
        ref_ok = []
        for (mm, sid), r in zip(meta, res):
            if mm != m or isinstance(r, Exception) or "verdicts" not in r:
                continue
            for cid, v in r["verdicts"].items():
                if cid == "REF":
                    ref_ok.append(v["faithful"]); continue
                g = gold[cid]
                rows.append({"cid": cid, "gold": g["gold"], "pred": "FAITHFUL" if v["faithful"] else "UNFAITHFUL",
                             "type": g["variant_type"], "pos": g["position"]})
        def rec(sel):
            sel = list(sel)
            return round(sum(r["gold"] == r["pred"] for r in sel) / len(sel), 3) if sel else None
        rf = rec(r for r in rows if r["gold"] == "FAITHFUL")
        ru = rec(r for r in rows if r["gold"] == "UNFAITHFUL")
        bal = round((rf + ru) / 2, 3) if rf is not None and ru is not None else None
        out[m] = {"model": MEMBERS[m]["model"], "n_scored": len(rows), "n_expected": len(items), "recall_faithful": rf,
                  "recall_unfaithful": ru, "balanced_accuracy": bal,
                  "recall_unfaithful_DOWN": rec(r for r in rows if r["gold"] == "UNFAITHFUL" and r["pos"] == "DOWN"),
                  "recall_unfaithful_UP": rec(r for r in rows if r["gold"] == "UNFAITHFUL" and r["pos"] == "UP"),
                  "recall_STRICT": rec(r for r in rows if r["type"].startswith("STRICT")),
                  "recall_RENAME": rec(r for r in rows if r["type"] == "RENAME_SYNONYM"),
                  "by_type": {t: rec(r for r in rows if r["type"] == t) for t in sorted({r["type"] for r in rows})},
                  "reference_accepted": round(sum(ref_ok) / len(ref_ok), 3) if ref_ok else None,
                  "passes_gate": bool(bal is not None and bal >= 0.80 and rf >= 0.70 and ru >= 0.70 and len(rows) >= 0.9 * len(items))}
        logger.info(f"GATE {m} {out[m]}")
    return out


async def run_trackh(members, cap):
    pairs = trackh_pairs()
    async with Client("gate_trackh", phase_cap=cap, concurrency=12) as client:
        panel = Panel(client)
        jobs, meta = [], []
        for p in pairs:
            d = Disguiser("trackH|" + p["id"], p["text"], [p["orig"], p["corr"]])
            shown = [("orig", d.formula(p["orig"])), ("corr", d.formula(p["corr"]))]
            for m in members:
                jobs.append(panel.judge(m, "trackH|" + p["id"], d.text(p["text"]), shown, tag="trackh"))
                meta.append((m, p["id"]))
        res = await asyncio.gather(*jobs, return_exceptions=True)
    per = defaultdict(dict)
    for (m, pid), r in zip(meta, res):
        if not isinstance(r, Exception) and "verdicts" in r:
            per[pid][m] = {"orig_faithful": r["verdicts"]["orig"]["faithful"], "corr_faithful": r["verdicts"]["corr"]["faithful"],
                           "orig_ops": r["verdicts"]["orig"]["ops"], "ambiguous": r["ambiguous"]}
    rows = []
    for p in pairs:
        v = per.get(p["id"], {})
        maj = {}
        for side in ("orig", "corr"):
            votes = [x[f"{side}_faithful"] for x in v.values()]
            maj[side] = (sum(votes) * 2 > len(votes)) if votes else None
        rows.append({**p, "votes": v, "majority_orig_faithful": maj["orig"], "majority_corr_faithful": maj["corr"]})
    def acc(sel, who):
        sel = [r for r in sel if (who in r["votes"]) or who == "majority"]
        n = c = 0
        for r in sel:
            if who == "majority":
                if r["majority_orig_faithful"] is None:
                    continue
                o, cf = r["majority_orig_faithful"], r["majority_corr_faithful"]
            else:
                o, cf = r["votes"][who]["orig_faithful"], r["votes"][who]["corr_faithful"]
            n += 2; c += (not o) + bool(cf)
        return {"n_judgements": n, "accuracy": round(c / n, 3) if n else None}
    unamb = [r for r in rows if not r["ambiguous"]]
    rep = {"n_pairs": len(rows), "n_unambiguous": len(unamb), "per_model": {}, "by_census_class": {}}
    for who in list(members) + ["majority"]:
        rep["per_model"][who] = {"unambiguous": acc(unamb, who), "ambiguous_READING_CHOICE": acc([r for r in rows if r["ambiguous"]], who),
                                 "orig_flagged_rate_unamb": round(sum((not r["votes"][who]["orig_faithful"]) if who != "majority" else (r["majority_orig_faithful"] is False)
                                                                      for r in unamb if who == "majority" or who in r["votes"]) / max(1, len(unamb)), 3),
                                 "corr_accepted_rate_unamb": round(sum((r["votes"][who]["corr_faithful"]) if who != "majority" else bool(r["majority_corr_faithful"])
                                                                       for r in unamb if who == "majority" or who in r["votes"]) / max(1, len(unamb)), 3)}
    for cc in sorted({r["census_class"] for r in rows}):
        rep["by_census_class"][cc] = {"n": sum(r["census_class"] == cc for r in unamb), "majority": acc([r for r in unamb if r["census_class"] == cc], "majority")}
    (ROOT / "work" / "trackh_panel_rows.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1))
    logger.info(f"TRACK-H {json.dumps(rep)}")
    return rep


@logger.catch(reraise=True)
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="synthetic")
    ap.add_argument("--members", default="P1,P2,P3,P1alt")
    ap.add_argument("--cap", type=float, default=0.3)
    a = ap.parse_args()
    members = a.members.split(",")
    prev = json.loads(OUT.read_text()) if OUT.exists() else {}
    if a.mode == "synthetic":
        r = asyncio.run(run_synthetic(members, a.cap))
        prev.setdefault("synthetic", {}).update(r)
    else:
        prev["trackh"] = asyncio.run(run_trackh(members, a.cap))
        prev["trackh"]["members"] = members
    OUT.write_text(json.dumps(prev, indent=1))


if __name__ == "__main__":
    main()
