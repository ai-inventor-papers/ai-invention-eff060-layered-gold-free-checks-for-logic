#!/usr/bin/env python3
"""STEP D: gloss gate. Known-answer (symbol use, meaning) items built deterministically from the R_COMP sentences and the
dataset-3 lexicon (7 classes, target 120 each, one item per class per sentence, stratified over templates), halves A/B
by sha1(sentence_id) parity. Both checkers rate half A with gloss_v1; PASS rule from the prereg.

usage: gate.py build | gate.py run [--half A|B] [--version gloss_v1]  -> results/gate_items.json, results/gate_report.json
"""
from __future__ import annotations

import argparse
import asyncio
import json
import math
import os
import random
import re
from collections import Counter, defaultdict

from common import LEXICON, NLTK_DATA, RES, SENTS, dump, setup_logger, sha1

os.environ.setdefault("NLTK_DATA", str(NLTK_DATA))
from fol import parse  # noqa: E402
from inputs import template_units  # noqa: E402
from perturb_min import first_sense_synonyms, wn_synonyms  # noqa: E402

TARGET = 120
CLASSES = ["YES_IDENT", "YES_SYN", "YES_FORM", "NO_NONCE", "NO_DONOR", "NO_ROLE", "NO_MERGE"]
SYMMETRIC = {"friend", "friends", "sibling", "siblings", "married", "neighbor", "neighbour", "related", "near", "with",
             "meet", "meets", "partner", "similar", "equal", "adjacent", "connected", "together", "and"}
CONS, VOW = "bdfgklmptvz", "aeiou"


def toks(n: str) -> list[str]:
    return re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", n.replace("_", " "))


def strip_k(name: str) -> str:
    return re.sub(r"_\d+$", "", name)


def disp(name: str, arity: int, subj: int, fills: dict) -> str:
    return f"{name}({', '.join(fills.get(j, 'x') if j != subj else 'x' for j in range(arity))})"


def nonce(rng: random.Random) -> str:
    while True:
        w = "".join(rng.choice(CONS) + rng.choice(VOW) for _ in range(2)) + rng.choice(CONS)
        w = w.capitalize()
        if not re.match(r"^(Un|Non|In|Im|Dis|No|Not)", w):
            return w


def units_of(sent: dict, lex: dict) -> list[dict]:
    us = template_units(sent, lex)
    out = []
    for uid, u in us.items():
        subj = u["args"].index("x") if "x" in u["args"] else 0
        fills = {j: a for j, a in enumerate(u["args"]) if j != subj}
        out.append({"uid": uid, **u, "subj": subj, "fills": fills})
    return out


def siblings(sent: dict) -> list[tuple[str, str]]:
    e = parse(sent["reference_fol_weak"])
    # weak reading antecedent: one flat conjunction of units
    ante = e[2][1] if e[0] == "all" and e[2][0] == "imp" else None
    if ante is None:
        return []
    acc = []

    def flat(x):
        if x[0] == "and":
            flat(x[1]); flat(x[2])
        elif x[0] == "atom":
            acc.append(f"{x[1]}({', '.join(x[2])})")
    flat(ante)
    return [(a, b) for i, a in enumerate(acc) for b in acc[i + 1:]]


def build(logger) -> list[dict]:
    lex = {e["lexicon_id"]: e for e in json.loads(LEXICON.read_text())["entries"]}
    sents = sorted(json.loads(SENTS.read_text()), key=lambda s: sha1(s["sentence_id"]))
    by_sort = defaultdict(list)
    su = {}
    for s in sents:
        su[s["sentence_id"]] = units_of(s, lex)
        for u in su[s["sentence_id"]]:
            by_sort[s["sort_group"]].append((s["sentence_id"], u))
    items = []
    counts = Counter()
    per_template = defaultdict(Counter)
    for s in sents:
        sid = s["sentence_id"]
        rng = random.Random(int(sha1("gate|" + sid), 16))
        us = su[sid]
        rng.shuffle(us)
        half = "A" if int(sha1(sid), 16) % 2 == 0 else "B"
        t = s["template_id"]
        uid_g = {u["uid"]: u for u in us}

        def add(cls, use, meaning, note=""):
            gold = "YES" if cls.startswith("YES") else "NO"
            # balance templates: at most ceil(TARGET/9)+2 per (class, template)
            if counts[cls] >= TARGET or per_template[cls][t] >= math.ceil(TARGET / 9) + 2:
                return False
            counts[cls] += 1
            per_template[cls][t] += 1
            items.append({"item_id": sha1(f"{cls}|{sid}|{use}|{meaning}")[:16], "class": cls, "gold": gold,
                          "sentence_id": sid, "sentence": s["text"], "template_id": t, "half": half,
                          "candidate_atom": use, "proposed_meaning": meaning, "note": note})
            return True
        # YES_IDENT
        u = us[0]
        add("YES_IDENT", disp(strip_k(u["pred"]), u["arity"], u["subj"], u["fills"]), u["gloss_pos"])
        # YES_SYN: mutual first-sense WordNet synonym of one name token
        for u in us:
            tk = toks(strip_k(u["pred"]))
            done = False
            for i, w in enumerate(tk):
                if len(w) < 4 or not w.isalpha():
                    continue
                for syn in sorted(first_sense_synonyms(w.lower())):
                    if not syn.isalpha() or len(syn) < 3 or syn == w.lower():
                        continue
                    nn = "".join(tk[:i] + [syn.capitalize()] + tk[i + 1:])
                    done = add("YES_SYN", disp(nn, u["arity"], u["subj"], u["fills"]), u["gloss_pos"], f"{w}->{syn}")
                    break
                if done:
                    break
            if done:
                break
        # YES_FORM: reify / de-reify / lexical negation / merged name (rotating by sentence hash)
        forms = []
        for u in us:
            if u["arity"] == 2 and u["fills"]:
                c = list(u["fills"].values())[0]
                forms.append(("reify", f"{strip_k(u['pred'])}{c[0].upper() + c[1:]}(x)", u["gloss_pos"]))
            tk = toks(strip_k(u["pred"]))
            if u["arity"] == 1 and len(tk) >= 2:
                rest = "".join(tk[1:])
                forms.append(("dereify", f"{tk[0]}(x, {rest[0].lower() + rest[1:]})", u["gloss_pos"]))
            if u["arity"] == 1:
                forms.append(("lexneg", f"Not{strip_k(u['pred'])}(x)", u["gloss_neg"]))
        sib = siblings(s)
        if sib:
            a, b = sib[0]
            if a in uid_g and b in uid_g and uid_g[a]["arity"] == 1 and uid_g[b]["arity"] == 1:
                forms.append(("merge", f"{strip_k(uid_g[a]['pred'])}{strip_k(uid_g[b]['pred'])}(x)",
                              uid_g[a]["gloss_pos"] + " and " + uid_g[b]["gloss_pos"]))
        if forms:
            f = forms[int(sha1("form|" + sid), 16) % len(forms)]
            add("YES_FORM", f[1], f[2], f[0])
        # NO_NONCE
        u = us[1 % len(us)]
        add("NO_NONCE", disp(nonce(rng), u["arity"], u["subj"], u["fills"]), u["gloss_pos"])
        # NO_DONOR: same-sort predicate from another sentence, no shared token / WordNet synonym
        u = us[2 % len(us)]
        tp = {w.lower() for w in toks(strip_k(u["pred"]))}
        syn = set().union(*[wn_synonyms(w) for w in tp]) if tp else set()
        pool = [x for x in by_sort[s["sort_group"]] if x[0] != sid and x[1]["arity"] == u["arity"]]
        rng.shuffle(pool)
        own = {strip_k(x["pred"]) for x in us}
        for _, d in pool:
            td = {w.lower() for w in toks(strip_k(d["pred"]))}
            if td & (tp | syn) or strip_k(d["pred"]) in own:
                continue
            add("NO_DONOR", disp(strip_k(d["pred"]), u["arity"], u["subj"], u["fills"] if u["arity"] > 1 else {}),
                u["gloss_pos"], f"donor={d['pred']}")
            break
        # NO_ROLE: swapped directional binary unit, else positive name for the negated gloss
        role_done = False
        for u in us:
            if u["arity"] == 2 and u["fills"] and not ({w.lower() for w in toks(u["pred"])} & SYMMETRIC):
                c = list(u["fills"].values())[0]
                role_done = add("NO_ROLE", f"{strip_k(u['pred'])}({c}, x)", u["gloss_pos"], "swap")
                break
        if not role_done:
            u = us[3 % len(us)]
            add("NO_ROLE", disp(strip_k(u["pred"]), u["arity"], u["subj"], u["fills"]), u["gloss_neg"], "pos_for_neg")
        # NO_MERGE: one unit's name for the conjunction of its gloss and a sibling's
        if sib:
            a, b = sib[-1]
            if a in uid_g and b in uid_g:
                ua, ub = uid_g[a], uid_g[b]
                add("NO_MERGE", disp(strip_k(ua["pred"]), ua["arity"], ua["subj"], ua["fills"]),
                    ua["gloss_pos"] + " and " + ub["gloss_pos"])
    logger.info(f"gate items: {dict(counts)}; halves {dict(Counter(i['half'] for i in items))}")
    dump(RES / "gate_items.json", items)
    return items


def wilson(k: int, n: int, z: float = 1.96) -> list:
    if n == 0:
        return [None, None]
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(c - h, 3), round(c + h, 3)]


def kappa(a: list, b: list) -> float | None:
    n = len(a)
    if n == 0:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(ca) | set(cb)) / (n * n)
    return round((po - pe) / (1 - pe), 3) if pe < 1 else None


def evaluate(items: list[dict], verdicts: dict, half: str, version: str) -> dict:
    rows = [i for i in items if i["half"] == half]
    rep = {"half": half, "version": version, "n_items": len(rows), "per_class": {}, "per_checker": {}}
    views = {"haiku": lambda i: verdicts.get(("haiku", i["sentence_id"], i["candidate_atom"], i["proposed_meaning"])),
             "qwen": lambda i: verdicts.get(("qwen", i["sentence_id"], i["candidate_atom"], i["proposed_meaning"]))}
    views["both_yes"] = lambda i: ("YES" if views["haiku"](i) == "YES" and views["qwen"](i) == "YES" else "NO")
    for v, f in views.items():
        yes = [i for i in rows if i["gold"] == "YES"]
        no = [i for i in rows if i["gold"] == "NO"]
        ry = sum(f(i) == "YES" for i in yes) / max(len(yes), 1)
        rn = sum(f(i) == "NO" for i in no) / max(len(no), 1)
        rep["per_checker"][v] = {"recall_YES": round(ry, 3), "recall_NO": round(rn, 3), "balanced_accuracy": round((ry + rn) / 2, 3),
                                 "recall_YES_ci": wilson(sum(f(i) == "YES" for i in yes), len(yes)),
                                 "recall_NO_ci": wilson(sum(f(i) == "NO" for i in no), len(no)),
                                 "no_verdict": sum(f(i) not in ("YES", "NO") for i in rows)}
        for cls in CLASSES:
            cr = [i for i in rows if i["class"] == cls]
            k = sum(f(i) == cr[0]["gold"] for i in cr) if cr else 0
            rep["per_class"].setdefault(cls, {"n": len(cr)})[v] = {"recall": round(k / max(len(cr), 1), 3), "ci": wilson(k, len(cr))}
    both = [(views["haiku"](i), views["qwen"](i)) for i in rows if views["haiku"](i) in ("YES", "NO") and views["qwen"](i) in ("YES", "NO")]
    rep["cohen_kappa_haiku_qwen"] = kappa([a for a, _ in both], [b for _, b in both])
    pc = rep["per_checker"]
    rep["PASS"] = bool(pc["haiku"]["balanced_accuracy"] >= 0.90 and pc["qwen"]["balanced_accuracy"] >= 0.90
                       and pc["both_yes"]["balanced_accuracy"] >= 0.90 and pc["both_yes"]["recall_YES"] >= 0.85
                       and pc["both_yes"]["recall_NO"] >= 0.85)
    return rep


async def run(half: str, version: str, logger) -> dict:
    import gloss
    items = json.loads((RES / "gate_items.json").read_text())
    jobs = defaultdict(lambda: {"pairs": []})
    for i in items:
        if i["half"] != half:
            continue
        j = jobs[i["sentence_id"]]
        j.update(sentence_id=i["sentence_id"], sentence=i["sentence"])
        j["pairs"].append((i["candidate_atom"], i["proposed_meaning"]))
    client = gloss.Client(phase=f"gate_{version}_{half}")
    try:
        v = await gloss.rate_pairs(client, list(jobs.values()), version=version, logger=logger)
    finally:
        await client.close()
    rep = evaluate(items, v, half, version)
    rep["artifact_spend_usd"] = round(gloss.spent(), 4)
    for i in items:
        if i["half"] == half:
            i[f"haiku_{version}"] = v.get(("haiku", i["sentence_id"], i["candidate_atom"], i["proposed_meaning"]))
            i[f"qwen_{version}"] = v.get(("qwen", i["sentence_id"], i["candidate_atom"], i["proposed_meaning"]))
    dump(RES / "gate_items.json", items)
    prev = json.loads((RES / "gate_report.json").read_text()) if (RES / "gate_report.json").exists() else {}
    prev[f"{version}_{half}"] = rep
    dump(RES / "gate_report.json", prev)
    logger.info(f"gate {version} half {half}: PASS={rep['PASS']} {json.dumps(rep['per_checker'])}")
    return rep


if __name__ == "__main__":
    lg = setup_logger("gate")
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["build", "run"])
    ap.add_argument("--half", default="A")
    ap.add_argument("--version", default="gloss_v1")
    a = ap.parse_args()
    if a.cmd == "build":
        build(lg)
    else:
        asyncio.run(run(a.half, a.version, lg))
