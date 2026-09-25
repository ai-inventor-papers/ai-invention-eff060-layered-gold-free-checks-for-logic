#!/usr/bin/env python3
"""B3: checker gates for GG. G-A: dataset-5 gloss_gate_items via prompt gloss_gg_gateA_v1 (half A = dev, half B = confirm).
G-B: symbol pairs from PERTURB R_COMP-base items (RENAME_SYN controls -> YES; MEANING_RENAME mutants -> NO) via the GG
prompt itself (gloss_gg_v1), dev/confirm by sha1(base) parity. Usage: gg_gates.py dev | confirm [--version v1|v2]
Writes results/gg_gate_items_B.jsonl, results/gg_gates_<stage>.json."""
from __future__ import annotations

import asyncio
import hashlib
import json
import sys
from collections import Counter, defaultdict

from common import DS3, DS5, FREEZE, RES, ROOT, jdump, jl, sha1, setup_logger
from gloss_client import Client, ckey, run_calls, spent

sys.path.insert(0, str(FREEZE))
import gg  # noqa: E402
from gg_fol import parse  # noqa: E402

logger = setup_logger("gg_gates")
PRE = json.loads((ROOT / "prereg_gg.json").read_text())
MODEL = PRE["checker"]["model"]
GATE_CAP = 0.10


def psha(p: dict) -> str:
    return hashlib.sha256(json.dumps(p, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def atoms_in_order(e, acc=None):
    acc = [] if acc is None else acc
    if e[0] == "atom":
        acc.append(e)
    elif e[0] in ("all", "ex"):
        atoms_in_order(e[2], acc)
    elif e[0] == "not":
        atoms_in_order(e[1], acc)
    else:
        atoms_in_order(e[1], acc)
        atoms_in_order(e[2], acc)
    return acc


def gate_b_items() -> tuple[list[dict], dict]:
    """(items, counts). Only R_COMP-base PERTURB rows are read (never rcomp_free / rcomp candidates)."""
    d = json.loads((DS3 / "full_data_out.json").read_text())
    ex = [e for g in d["datasets"] if g["dataset"] == "perturb_suite" for e in g["examples"]]
    del d
    items, drop = [], Counter()
    for e in ex:
        if not str(e.get("metadata_base_source", "")).startswith("RCOMP"):
            continue
        inp = json.loads(e["input"])
        cand, ref = inp["candidate_fol"], inp["reference_fol"]
        base = e["metadata_base_item_id"]
        if e.get("metadata_subtype") == "RENAME_SYN":
            try:
                ce, re_ = parse(cand), parse(ref)
            except (ValueError, IndexError):
                drop["parse"] += 1
                continue
            for old, new in (e.get("metadata_rename_map") or {}).items():
                name, ar = old.rsplit("/", 1)
                if name.lower() == new.lower():
                    continue
                items.append({"id": e["metadata_item_id"] + "|" + old, "sid": e["metadata_sentence_id"], "base": base, "text": inp["text"],
                              "a": f"{new}/{ar}", "b": old, "a_use": gg.atom_example(ce, f"{new}/{ar}"), "b_use": gg.atom_example(re_, old),
                              "expected": "YES", "kind": "RENAME_SYN"})
        elif "MEANING_RENAME" in (e.get("metadata_error_ops") or []):
            old = e.get("metadata_edited_predicate")
            try:
                ca, ra = atoms_in_order(parse(cand)), atoms_in_order(parse(ref))
            except (ValueError, IndexError):
                drop["parse"] += 1
                continue
            if not old or len(ca) != len(ra):
                drop["alignment"] += 1
                continue
            name, ar = old.rsplit("/", 1)
            new = {x[1] for x, y in zip(ca, ra) if y[1] == name and len(y[2]) == int(ar) and x[1] != y[1]}
            if len(new) != 1:
                drop["alignment"] += 1
                continue
            nn = new.pop()
            items.append({"id": e["metadata_item_id"], "sid": e["metadata_sentence_id"], "base": base, "text": inp["text"],
                          "a": f"{nn}/{ar}", "b": old, "a_use": gg.atom_example(parse(cand), f"{nn}/{ar}"),
                          "b_use": gg.atom_example(parse(ref), old), "expected": "NO", "kind": "MEANING_RENAME"})
    for it in items:
        it["half"] = "dev" if int(sha1(it["base"]), 16) % 2 == 0 else "confirm"
    return items, {"n_items": len(items), "by_kind_half": Counter(f"{i['kind']}|{i['half']}" for i in items), "dropped": dict(drop)}


def gate_a_items() -> list[dict]:
    d = json.loads((DS5 / "full_data_out.json").read_text())
    ex = [e for g in d["datasets"] if g["dataset"] == "gloss_gate_items" for e in g["examples"]]
    out = []
    for e in ex:
        inp = json.loads(e["input"])
        out.append({"id": e["metadata_item_id"], "sid": e["metadata_sentence_id"], "text": inp["sentence"], "atom": inp["candidate_atom"],
                    "meaning": inp["proposed_meaning"], "expected": e["output"], "cls": e["metadata_class"],
                    "half": "dev" if e["metadata_half"] == "A" else "confirm"})
    return out


def calls_for(items, prompt, render, keyf):
    by = defaultdict(list)
    for it in items:
        by[it["sid"]].append(it)
    calls = []
    n = prompt["max_items_per_call"]
    for sid, its in sorted(by.items()):
        its = sorted(its, key=lambda x: sha1(x["id"]))
        for i in range(0, len(its), n):
            ch = its[i:i + n]
            lines = "\n".join(render(k + 1, it) for k, it in enumerate(ch))
            msgs = [{"role": "system", "content": prompt["system"]},
                    {"role": "user", "content": prompt["user_template"].format(sentence=ch[0]["text"], items=lines)}]
            calls.append({"sid": sid, "messages": msgs, "keys": [keyf(it) for it in ch], "items": ch})
    return calls


def score(items, verdict_of) -> dict:
    tp = sum(1 for i in items if i["expected"] == "YES" and verdict_of(i) == "YES")
    npos = sum(1 for i in items if i["expected"] == "YES")
    tn = sum(1 for i in items if i["expected"] == "NO" and verdict_of(i) != "YES")
    nneg = sum(1 for i in items if i["expected"] == "NO")
    tpr, tnr = (tp / npos if npos else None), (tn / nneg if nneg else None)
    return {"n": len(items), "n_yes": npos, "n_no": nneg, "tpr": tpr, "tnr": tnr,
            "balanced_accuracy": (tpr + tnr) / 2 if tpr is not None and tnr is not None else None,
            "n_unparseable": sum(1 for i in items if verdict_of(i) == "NO_UNPARSEABLE"),
            "n_not_run": sum(1 for i in items if str(verdict_of(i)).startswith("NOT_RUN"))}


async def run(stage: str, version: str):
    pa = PRE[f"prompt_gloss_gg_gateA_{version}"] if f"prompt_gloss_gg_gateA_{version}" in PRE else json.loads((RES / f"prompt_gateA_{version}.json").read_text())
    pg = gg.PROMPT_GG_V1 if version == "v1" else json.loads((RES / f"prompt_gg_{version}.json").read_text())
    sa, sg = psha(pa), psha(pg)
    A = [i for i in gate_a_items() if i["half"] == stage]
    Bi, bcounts = gate_b_items()
    jdump({"counts": bcounts, "items": Bi}, RES / "gg_gate_items_B.json")
    Bs = [i for i in Bi if i["half"] == stage]
    stop_at = min(2.0, spent() + GATE_CAP)
    client = Client(MODEL, f"gate_{stage}_{version}", stop_at=stop_at, logger=logger)
    ca = calls_for(A, pa, lambda n, it: pa["item_template"].format(n=n, atom=it["atom"], meaning=it["meaning"]),
                   lambda it: ["gateA", it["atom"], it["meaning"]])
    cb = calls_for(Bs, pg, lambda n, it: pg["item_template"].format(n=n, a=it["a"], b=it["b"], a_use=it["a_use"], b_use=it["b_use"]),
                   lambda it: gg.pair_key(("pred", it["a"], it["b"])))
    logger.info(f"stage {stage} {version}: G-A {len(A)} items / {len(ca)} calls; G-B {len(Bs)} items / {len(cb)} calls; spend so far ${spent():.4f}")
    va = await run_calls(client, ca, gg.parse_verdicts, sa)
    vb = await run_calls(client, cb, gg.parse_verdicts, sg)
    ra = score(A, lambda it: va.get(ckey(MODEL, sa, it["sid"], ["gateA", it["atom"], it["meaning"]])))
    per_cls = {}
    for c in sorted({i["cls"] for i in A}):
        sub = [i for i in A if i["cls"] == c]
        ok = sum(1 for i in sub if (va.get(ckey(MODEL, sa, i["sid"], ["gateA", i["atom"], i["meaning"]])) == "YES") == (i["expected"] == "YES"))
        per_cls[c] = {"n": len(sub), "expected": sub[0]["expected"], "accuracy": ok / len(sub)}
    ra["per_class"] = per_cls
    vbf = lambda it: vb.get(ckey(MODEL, sg, it["sid"], list(gg.pair_key(("pred", it["a"], it["b"])))))  # noqa: E731
    rb = score(Bs, vbf)
    rb["testable"] = rb["n_yes"] >= 30 and rb["n_no"] >= 30  # per half; the >= 60 / 60 rule is on both halves together
    rb["n_yes_both_halves"] = sum(i["expected"] == "YES" for i in Bi)
    rb["n_no_both_halves"] = sum(i["expected"] == "NO" for i in Bi)
    rb["examples_wrong"] = [{k: i[k] for k in ("a", "b", "a_use", "b_use", "expected", "text")} | {"got": vbf(i)} for i in Bs if (vbf(i) == "YES") != (i["expected"] == "YES")][:20]
    out = {"stage": stage, "version": version, "model": MODEL, "prompt_sha_gateA": sa, "prompt_sha_gg": sg, "G-A": ra, "G-B": rb,
           "G-B_counts": {k: (dict(v) if isinstance(v, Counter) else v) for k, v in bcounts.items()},
           "client": client.stats, "spend_total_after": spent()}
    out["pass_A"] = bool(ra["balanced_accuracy"] is not None and ra["balanced_accuracy"] >= 0.90)
    out["pass_B"] = bool(rb["balanced_accuracy"] is not None and rb["balanced_accuracy"] >= 0.90) if rb["n_yes_both_halves"] >= 60 and rb["n_no_both_halves"] >= 60 else "NOT_TESTABLE"
    jdump(out, RES / f"gg_gates_{stage}_{version}.json")
    logger.info(f"G-A {stage}: BA {ra['balanced_accuracy']:.3f} (tpr {ra['tpr']:.3f}, tnr {ra['tnr']:.3f}); per class "
                + json.dumps({k: round(v['accuracy'], 3) for k, v in per_cls.items()}))
    logger.info(f"G-B {stage}: BA {rb['balanced_accuracy']} (tpr {rb['tpr']}, tnr {rb['tnr']}, n {rb['n_yes']}/{rb['n_no']}); "
                f"client {client.stats}")


@logger.catch(reraise=True)
def main():
    stage = sys.argv[1] if len(sys.argv) > 1 else "dev"
    version = sys.argv[2] if len(sys.argv) > 2 else "v1"
    asyncio.run(run(stage, version))


if __name__ == "__main__":
    main()
