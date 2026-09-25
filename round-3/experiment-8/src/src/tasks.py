"""Label-free task builders for the pair engine (screen, dataset E, PERTURB). Never reads a label key.

E rows come from exp 5's blind ALLOWLIST view (data/exp5/E_blind.jsonl, sha256 checked against exp 5's prereg).
PERTURB rows come from dataset 3's perturb_suite (data/perturb_rows.jsonl, written by prep_data.py with the output
label stripped; mutant/control TYPE is kept because it is the construction design, not a judgement).
"""
from __future__ import annotations

import hashlib
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

SRC = Path(__file__).resolve().parent
ROOT = SRC.parent
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
os.environ.setdefault("NLTK_DATA", str(ROOT / "data" / "nltk_data"))
import peer_text as PT  # noqa: E402

DATA = ROOT / "data"
EXP5 = DATA / "exp5"
STRATA = ["CTRL", "EXC", "L20", "L25"]
SCREEN_PEER_FAMILY = {"P1": "meta", "P2": "qwen", "P3": "deepseek", "P4": "mistral", "P5": "google", "P6": "openai"}
SCREEN_LLM_SYSTEMS = ["gpt-3.5-turbo", "gpt-4", "text-davinci-003"]


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest()


def sha256_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def exp5_prereg() -> dict:
    pre = json.loads((EXP5 / "prereg.json").read_text())
    assert sha256_file(EXP5 / "E_blind.jsonl") == pre["E_blind_sha256"], "E blind view differs from exp 5's frozen view"
    return pre


def E_rows() -> list[dict]:
    rows = jl(EXP5 / "E_blind.jsonl")
    for r in rows:
        for k in ("output", "final_label", "label_tier", "auto_label", "reference_fol"):
            assert k not in r, f"label key {k} in the blind view"
    return rows


def E_tasks(extra: dict | None = None) -> list[dict]:
    """One task per E sentence: every row a candidate; LLM rows are peers (leave-one-FAMILY-out, exp 5 vendor family map).
    extra: {sentence_id: [row dicts]} appended as non-peer candidates (e.g. PERTURB rows, pool_rule='all')."""
    pre = exp5_prereg()
    fam_v = pre["family_map_vendor"]
    by = defaultdict(list)
    for r in E_rows():
        by[r["sentence_id"]].append(r)
    out = []
    for sid, rs in by.items():
        trs = [{"key": r["row_key"], "fol": r["candidate_fol"], "family": fam_v[r["slot"]], "system": r["system"],
                "is_peer": r["system_class"] == "llm"} for r in rs]
        if extra is not None:
            if sid not in extra:
                continue
            trs += extra[sid]
        out.append({"sentence_id": sid, "text": rs[0]["text"], "stratum": rs[0]["strata"]["source_stratum"], "rows": trs})
    out.sort(key=lambda t: (STRATA.index(t["stratum"]), sha1(t["sentence_id"])))
    return out


# --------------------------------------------------------------------------------------------------- screen
def build_screen_pools(items: list[dict]) -> dict:
    """sentence_key -> {'text', 'members'} (exp 5 screen_fit.build_pools, verbatim logic)."""
    SD = DATA / "screen"
    uj = json.loads((SD / "units.json").read_text())
    peers = jl(SD / "peer_outputs.jsonl")
    src_unit = {}
    for it in sorted(items, key=lambda x: (x["track"] != "L", x["item_id"])):
        t = it["sentence_key"]
        if t in src_unit:
            continue
        if it["kind"] == "conclusion":
            src_unit[t] = f"F:{it['concl_id']}"
        elif it["kind"] == "premise":
            src_unit[t] = uj["premise_unit"].get(t)
        else:
            src_unit[t] = f"M:{it['malls_id']}"
    peer_by = defaultdict(dict)
    for r in peers:
        if r.get("sentence_norm") is None:
            continue
        peer_by[(r["unit_id"], r["sentence_norm"])].setdefault(r["peer"], r)
    uidx = {u["unit_id"]: u for u in uj["units"]}
    by_t = defaultdict(list)
    for it in items:
        by_t[it["sentence_key"]].append(it)
    out = {}
    for t, its in by_t.items():
        u = src_unit.get(t)
        entry = uidx[u].get("logiclm_entry") if u in uidx else None
        mem = {}
        for p in SCREEN_PEER_FAMILY:
            row = peer_by.get((u, t), {}).get(p)
            if row and row.get("fol") and PT.parse_fol(row["fol"]) is not None:
                mem[p] = row["fol"].strip()
        for s in SCREEN_LLM_SYSTEMS:
            cands = [x for x in its if x["track"] == "L" and x["system"] == s]
            if not cands:
                continue
            en = lambda x: int(x["logiclm_entry"].rsplit("_", 1)[-1]) if x.get("logiclm_entry") and x["logiclm_entry"].rsplit("_", 1)[-1].isdigit() else 10 ** 9  # noqa: E731
            cands.sort(key=lambda x: (x.get("logiclm_entry") != entry, en(x), x["item_id"]))
            f = cands[0]["candidate_fol"]
            if f and PT.parse_fol(f) is not None:
                mem["LL:" + s] = f.strip()
        out[t] = {"text": its[0]["text"], "members": mem}
    return out


def screen_tasks() -> list[dict]:
    """exp 5 screen tasks: track L/H candidates + exp C peers (P1-P6 + Logic-LM) + exp D rewrites (RW:) + probes (PR:)."""
    SD = DATA / "screen"
    items = json.loads((SD / "screen_items.json").read_text())
    pools = build_screen_pools(items)
    inv = json.loads((DATA / "invariance_items.json").read_text())
    probes = json.loads((EXP5 / "screen_probes.json").read_text())
    by_id = {x["item_id"]: x for x in items}
    fam = lambda x: "openai" if x["track"] == "L" else "human"  # noqa: E731
    extra = defaultdict(list)
    for r in inv:
        if r["base_item_id"] in by_id:
            b = by_id[r["base_item_id"]]
            extra[b["sentence_key"]].append({"key": "RW:" + r["rw_id"], "fol": r["candidate_fol"], "family": fam(b),
                                             "system": b["system"]})
    for pr in probes:
        b = by_id[pr["base_item_id"]]
        extra[b["sentence_key"]].append({"key": f"PR:{pr['probe']}:{pr['base_item_id']}", "fol": pr["fol"], "family": fam(b),
                                         "system": b["system"]})
    by_t = defaultdict(list)
    for x in items:
        by_t[x["sentence_key"]].append(x)
    tasks = []
    for t in sorted(pools):
        rows = [{"key": x["item_id"], "fol": x["candidate_fol"], "family": fam(x), "system": x["system"], "is_peer": False}
                for x in by_t[t] if x["track"] in ("L", "H")]
        rows += [{"key": "M:" + m, "fol": f, "family": SCREEN_PEER_FAMILY.get(m, "openai"), "system": m.replace("LL:", ""),
                  "is_peer": True} for m, f in pools[t]["members"].items()]
        rows += [dict(r, is_peer=False) for r in extra.get(t, [])]
        tasks.append({"sentence_id": sha1(t)[:12], "sentence_key": t, "text": pools[t]["text"], "stratum": "SCREEN",
                      "rows": rows})
    return tasks


# --------------------------------------------------------------------------------------------------- PERTURB
def perturb_rows() -> list[dict]:
    return jl(DATA / "perturb_rows.jsonl")


def perturb_extra(include_base: bool = True) -> dict:
    """{E sentence_id: [PERTURB candidate rows]} for bases whose sentence is an E sentence (R_COMP bases have no peers).
    Each mutant/control is a non-peer candidate scored against ALL peers (pool_rule='all'). The unmutated base
    (reference formula) is added once per base as control type BASE."""
    extra = defaultdict(list)
    seen_base = set()
    for r in perturb_rows():
        if r["base_source"].startswith("R_COMP"):
            continue
        extra[r["sentence_id"]].append({"key": "PT:" + r["item_id"], "fol": r["candidate_fol"], "family": "PERTURB_REF",
                                        "is_peer": False, "pool_rule": "all"})
        if include_base and r["base_item_id"] not in seen_base:
            seen_base.add(r["base_item_id"])
            extra[r["sentence_id"]].append({"key": "PB:" + r["base_item_id"], "fol": r["reference_fol"],
                                            "family": "PERTURB_REF", "is_peer": False, "pool_rule": "all"})
    return extra
