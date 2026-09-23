#!/usr/bin/env python3
"""STEP 5e: reference repair for GOLD_WRONG MALLS sentences (NOT YET EXECUTED: blocked by the key's daily limit).

Each panel model writes its own FOL for the ORIGINAL (undisguised) sentence with the frozen few-shot prompt
(prompts/fewshot_v1.txt). If >=2 of the 3 are mutually equivalent_modulo_vocab (EQ/VOCAB/GRAN), the new reference is
the agreeing formula with the smallest symbol count -> work/reference_overrides.json (PANEL_REPAIRED); otherwise the
sentence goes to work/no_trusted_reference.json. Then: run_label.py --refs work/reference_overrides.json
--out labels_heldout_repaired.jsonl, and assemble.py.
"""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "labeller"))
sys.setrecursionlimit(10000)
from or_client import BudgetExceeded, Client  # noqa: E402
from panel import MEMBERS  # noqa: E402
from normalise import normalise  # noqa: E402
from fol import parse  # noqa: E402
from label_lib import equivalent_modulo_vocab  # noqa: E402
from repair_census import atoms  # noqa: E402

PANEL = ["P1", "P3", "R1"]
OUT = ROOT / "raw" / "reference_repair.jsonl"


def gold_wrong_ids() -> list[str]:
    ids = []
    adj = {}
    p = ROOT / "work" / "panel_heldout_adj.jsonl"
    if p.exists():  # third member's votes on the two raters' disagreements
        for line in open(p):
            a = json.loads(line)
            for cid, v in a["votes"].items():
                adj.setdefault(cid, {})[a["member"]] = v
    for line in open(ROOT / "work" / "panel_heldout.jsonl"):
        r = json.loads(line)
        sid = r["sentence_id"]
        v = {m: x for m, x in {**r["votes"].get(f"{sid}:c0", {}), **adj.get(f"{sid}:c0", {})}.items() if m in PANEL}
        if len(v) >= 2 and sum(not x["faithful"] for x in v.values()) >= 2:
            ids.append(sid)
    sents = {s["sentence_id"]: s for s in json.loads((ROOT / "work" / "sentences.json").read_text())}
    return [i for i in ids if sents[i]["source"].startswith("MALLS")]


async def main(cap: float = 0.6):
    sents = {s["sentence_id"]: s for s in json.loads((ROOT / "work" / "sentences.json").read_text())}
    prompt = json.loads((ROOT / "prompts" / "fewshot_v1.txt").read_text())
    ids = gold_wrong_ids()
    done = {(json.loads(l)["sentence_id"], json.loads(l)["member"]) for l in open(OUT)} if OUT.exists() else set()
    async with Client("reference_repair", phase_cap=cap, concurrency=12) as client:
        async def one(sid, m):
            msgs = [{"role": "system", "content": prompt["system"]}] + prompt["exemplars"] + \
                   [{"role": "user", "content": prompt["user_template"].format(sentence=sents[sid]["text"])}]
            cfg = MEMBERS[m]
            try:
                r = await client.chat(cfg["model"], msgs, tag=f"repair:{m}:{sid}", retries=2, **{**cfg["params"], "max_tokens": 600})
            except BudgetExceeded as e:
                print(f"budget: {e}")
                return
            with open(OUT, "a", encoding="utf-8") as f:
                f.write(json.dumps({"sentence_id": sid, "member": m, "raw": r["text"], "error": r["error"], "cost_usd": r["cost_usd"]}, ensure_ascii=False) + "\n")
        # sequential agreement (budget): the two cheaper members first; P1 only where they are not mutually equivalent
        await asyncio.gather(*[one(s, m) for s in ids for m in ("P3", "R1") if (s, m) not in done])
        first = {}
        for line in (open(OUT) if OUT.exists() else []):
            r = json.loads(line)
            if r["raw"]:
                first.setdefault(r["sentence_id"], {})[r["member"]] = normalise(r["raw"])[0]
        need = []
        for sid in ids:
            f = first.get(sid, {})
            ok = False
            if "P3" in f and "R1" in f:
                try:
                    ok = equivalent_modulo_vocab(parse(f["P3"]), parse(f["R1"])) in ("EQ", "VOCAB", "GRAN")
                except Exception:  # noqa: BLE001
                    ok = False
            if not ok and (sid, "P1") not in done:
                need.append(sid)
        print(f"P3/R1 agree on {len(ids) - len(need)} of {len(ids)}; P1 called for {len(need)}")
        await asyncio.gather(*[one(s, "P1") for s in need])
    by = {}
    for line in (open(OUT) if OUT.exists() else []):
        r = json.loads(line)
        if r["raw"]:
            by.setdefault(r["sentence_id"], {})[r["member"]] = normalise(r["raw"])[0]
    overrides, noref = {}, []
    for sid in ids:
        fs = []
        for m, f in by.get(sid, {}).items():
            try:
                fs.append((f, parse(f)))
            except Exception:  # noqa: BLE001
                pass
        best = None
        for i in range(len(fs)):
            agree = [fs[i]] + [fs[j] for j in range(len(fs)) if j != i and equivalent_modulo_vocab(fs[j][1], fs[i][1]) in ("EQ", "VOCAB", "GRAN")]
            if len(agree) >= 2:
                cand = min(agree, key=lambda t: len(atoms(t[1])))
                if best is None or len(atoms(cand[1])) < len(atoms(best[1])):
                    best = cand
        if best:
            overrides[sid] = best[0]
        else:
            noref.append(sid)
    (ROOT / "work" / "reference_overrides.json").write_text(json.dumps(overrides, ensure_ascii=False, indent=1))
    (ROOT / "work" / "no_trusted_reference.json").write_text(json.dumps(noref, indent=1))
    print(f"GOLD_WRONG {len(ids)}: PANEL_REPAIRED {len(overrides)}, NO_TRUSTED_REFERENCE {len(noref)}")


if __name__ == "__main__":
    asyncio.run(main())
