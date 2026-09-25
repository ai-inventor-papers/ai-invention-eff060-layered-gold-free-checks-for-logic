#!/usr/bin/env python3
"""STEP 2: atom lexicon = (predicate atom <-> English 3sg verb phrase) pairs.

  extract  2a  claude-haiku-4.5, 5 source rules per call, temperature 0  -> raw/lexicon_extract.jsonl
  check    2b  deterministic checks (stems ⊆ source stems ∪ WordNet synonyms; spaCy VBZ/MD first token;
               negation marker; constant in phrase)                       -> work/lexicon_checked.json
  audit    2c  ADJUDICATOR model (Sonnet), 20 entries per call            -> raw/lexicon_audit.jsonl
  build    2d-2f keep OK entries, lexicon_id = sha1(atom|vp)[:10], resolve name collisions, sort groups
                                                                           -> lexicon.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
from collections import Counter, defaultdict

from common import ROOT, RAW, W, dump, sha1, setup_logger
from llm import ANTHROPIC_NO_THINK, run_jobs

logger = setup_logger("lexicon")
HAIKU = "anthropic/claude-haiku-4.5"
MAX_RULES = int(os.environ.get("LEX_MAX_RULES", "320"))

EXTRACT_SYS = """You map logic atoms to plain English verb phrases.
You get numbered source items. Each has an English sentence, its first-order logic formula, and a list of atoms over the variable x (x is the individual the sentence talks about; lowercase arguments are constants).
For EVERY listed atom return one object:
- "vp_sg_pos": a third-person-singular verb phrase that completes "the person ___" (or "the thing ___"), saying exactly what the atom says as it is used in the sentence. Reuse the sentence's own words. Examples: "is a student", "lives in Paris", "can make cookies", "has a pet", "is bad at chess". A binary atom's phrase must mention its constant.
- "vp_sg_neg": the negated phrase ("is not a student", "does not live in Paris", "cannot make cookies").
- "noun": only if the atom is a type/category predicate that names what x is (e.g. Student(x) -> "student", Dog(x) -> "dog"): the singular noun; otherwise null.
- "subject_sort": the kind of individual x is in this sentence: one of person, animal, object, place, organisation, event, other.
- "skip": true if no faithful phrase exists (the atom is a fragment, its meaning is unclear, or it cannot be stated about x alone), else false.
Return ONLY compact single-line JSON (no indentation, no code fence): {"atoms": [{"item": <number>, "atom": "<atom exactly as given>", "vp_sg_pos": ..., "vp_sg_neg": ..., "noun": ..., "subject_sort": ..., "skip": ...}, ...]}"""

AUDIT_SYS = """You audit a lexicon that maps logic atoms to English verb phrases. For each numbered entry you see the source sentence, its formula, one atom over the variable x, a positive phrase and a negative phrase (each completes "the person/thing ___").
An entry is OK only if (1) the positive phrase states exactly what the atom means in that sentence (not narrower, not broader, no added or dropped condition), (2) the negative phrase is its plain negation, and (3) both are grammatical.
Otherwise it is WRONG, with one reason code: MEANING (different meaning), SCOPE (too broad or too narrow), NEG (negative phrase wrong), GRAMMAR, CONST (constant missing or wrong), OTHER.
Return ONLY compact single-line JSON (no indentation, no code fence): {"verdicts": [{"entry": <number>, "verdict": "OK"|"WRONG", "reason": null|"<code>"}, ...]}"""


def select_rules(rules: list[dict]) -> list[dict]:
    """Greedy novelty in priority order: take a rule only if it adds an atom key not seen yet."""
    seen, out = set(), []
    for r in rules:
        keys = {(a["pred"], a["const"]) for a in r["atoms"]}
        if keys - seen:
            out.append(r); seen |= keys
        if len(out) >= MAX_RULES:
            break
    return out


def extract(src_file: str, cap: float):
    rules = select_rules(json.loads((W / src_file).read_text()))
    logger.info(f"selected {len(rules)} source rules")
    jobs = []
    for i in range(0, len(rules), 5):
        chunk = rules[i:i + 5]
        body = []
        for k, r in enumerate(chunk, 1):
            body.append(f"Item {k}\nSentence: {r['text']}\nFormula: {r['fol']}\nAtoms: " + "; ".join(a["atom"] for a in r["atoms"]))
        key = sha1("|".join(r["rule_id"] for r in chunk))[:16]
        jobs.append({"key": key, "rules": [r["rule_id"] for r in chunk],
                     "messages": [{"role": "system", "content": EXTRACT_SYS}, {"role": "user", "content": "\n\n".join(body)}]})
    dump(W / ("lexicon_extract_jobs_malls.json" if "malls" in src_file else "lexicon_extract_jobs.json"),
         [{"key": j["key"], "rules": j["rules"]} for j in jobs])
    return run_jobs("lexicon_extraction", cap, HAIKU, jobs, RAW / "lexicon_extract.jsonl", logger, concurrency=8,
             params={"temperature": 0.0, "max_tokens": 3000}, salvage_key="atoms",
             validate=lambda j, p: isinstance(p, dict) and isinstance(p.get("atoms"), list))


# ---------------------------------------------------------------- 2b deterministic checks
FUNC = set("""a an the is are was were be been being am do does did has have had having can could may might must shall
should will would not n't no never of in on at to for from by with as into onto about over under between among through
during before after above below up down out off than that which who whom whose what when where while it its they them their
he him his she her also very more most less least many much few some any all every each other such so there this these
those only just own one ones someone something anyone anything""".split())


def _stem(w):
    from nltk.stem import PorterStemmer
    global _PS
    try:
        _PS
    except NameError:
        _PS = PorterStemmer()
    return _PS.stem(w.lower())


def _syn_stems(word: str) -> set:
    from nltk.corpus import wordnet as wn
    out = set()
    for syn in wn.synsets(word)[:8]:
        for lem in syn.lemma_names():
            for p in lem.split("_"):
                out.add(_stem(p))
        for rel in syn.derivationally_related_forms() if hasattr(syn, "derivationally_related_forms") else []:
            pass
    for lem in wn.lemmas(word):
        for d in lem.derivationally_related_forms():
            out.add(_stem(d.name()))
    return out


def camel_words(c: str) -> list[str]:
    return [w.lower() for w in re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", c.replace("_", " "))]


def check(nlp, entry: dict, rule: dict) -> list[str]:
    fails = []
    pos, neg = (entry.get("vp_sg_pos") or "").strip(), (entry.get("vp_sg_neg") or "").strip()
    if not pos or not neg:
        return ["EMPTY"]
    sent_words = re.findall(r"[A-Za-z]+", rule["text"])
    sent_stems = {_stem(w) for w in sent_words}
    for w in re.findall(r"[A-Za-z]+", pos):
        lw = w.lower()
        if lw in FUNC:
            continue
        st = _stem(lw)
        if st in sent_stems:
            continue
        if _syn_stems(lw) & sent_stems:
            continue
        fails.append(f"STEM:{lw}")
    doc = nlp("The person " + pos + ".")
    first = doc[2] if len(doc) > 2 else None
    if first is None or not (first.tag_ in ("VBZ", "MD") or first.text.lower() in ("is", "has", "does")):
        fails.append(f"NOT_VBZ:{first.text if first is not None else ''}/{first.tag_ if first is not None else ''}")
    if not re.search(r"\b(not|no|never|cannot)\b|n't", neg.lower()):
        fails.append("NO_NEG")
    if entry.get("const"):
        cw = camel_words(entry["const"])
        if not all(re.search(r"\b" + re.escape(w), pos.lower()) for w in cw):
            fails.append("CONST_MISSING")
    return fails


def check_all():
    import spacy
    nlp = spacy.load("en_core_web_sm")
    rules = {r["rule_id"]: r for r in json.loads((W / "source_rules.json").read_text())}
    if (W / "source_rules_malls.json").exists():
        rules.update({r["rule_id"]: r for r in json.loads((W / "source_rules_malls.json").read_text())})
    jobs = {j["key"]: j for j in json.loads((W / "lexicon_extract_jobs.json").read_text())}
    if (W / "lexicon_extract_jobs_malls.json").exists():
        jobs.update({j["key"]: j for j in json.loads((W / "lexicon_extract_jobs_malls.json").read_text())})
    from llm import cached
    res = cached(RAW / "lexicon_extract.jsonl")
    out, log = [], Counter()
    for key, j in jobs.items():
        if key not in res:
            log["job_missing"] += 1; continue
        chunk = [rules[r] for r in j["rules"]]
        for a in res[key]["parsed"]["atoms"]:
            try:
                r = chunk[int(a.get("item")) - 1]
            except (TypeError, ValueError, IndexError):
                log["bad_item"] += 1; continue
            src_atom = next((x for x in r["atoms"] if x["atom"].replace(" ", "") == str(a.get("atom", "")).replace(" ", "")), None)
            if src_atom is None:
                log["atom_not_in_rule"] += 1; continue
            if a.get("skip"):
                log["skip"] += 1; continue
            e = {**src_atom, "rule_id": r["rule_id"], "source": r["source"], "source_text": r["text"],
                 "source_fol": r["fol"], "vp_sg_pos": (a.get("vp_sg_pos") or "").strip().rstrip("."),
                 "vp_sg_neg": (a.get("vp_sg_neg") or "").strip().rstrip("."), "noun": a.get("noun"),
                 "subject_sort": (a.get("subject_sort") or "other").lower(), "extract_key": key}
            # sortal = a type noun ("is a/an N"); adjectives the extractor tagged with a noun stay non-sortal
            e["sortal"] = bool(e["noun"]) and e["arity"] == 1 and re.match(r"^is an? ", e["vp_sg_pos"]) is not None
            e["check_fails"] = check(nlp, e, r)
            if e["sortal"]:
                # the noun keeps the phrase's own casing ("is a PRC national" -> "PRC national")
                e["noun"] = re.sub(r"^is an? ", "", e["vp_sg_pos"]).strip()
                if not re.fullmatch(r"[A-Za-z][A-Za-z \-]*", e["noun"]):
                    e["check_fails"].append("BAD_NOUN")
            if re.search(r"\b(them|it|this|these|those|he|she|him|her)\b", e["vp_sg_pos"], re.I):
                e["check_fails"].append("DANGLING_PRONOUN")  # antecedent-less pronoun: not composable
            log["checked"] += 1
            log["pass" if not e["check_fails"] else "fail"] += 1
            for f in e["check_fails"]:
                log["fail_" + f.split(":")[0]] += 1
            out.append(e)
    dump(W / "lexicon_checked.json", out)
    dump(W / "lexicon_check_log.json", dict(log))
    logger.info(dict(log))


def audit_model() -> str:
    p = W / "adjudicator_model.json"
    return json.loads(p.read_text())["model"]


def audit(cap: float):
    ents = [e for e in json.loads((W / "lexicon_checked.json").read_text()) if not e["check_fails"]]
    ents.sort(key=lambda e: sha1(e["rule_id"] + e["atom"]))
    model = audit_model()
    jobs = []
    for i in range(0, len(ents), 20):
        chunk = ents[i:i + 20]
        body = []
        for k, e in enumerate(chunk, 1):
            body.append(f"Entry {k}\nSentence: {e['source_text']}\nFormula: {e['source_fol']}\nAtom: {e['atom']}\n"
                        f"Positive: the person/thing {e['vp_sg_pos']}\nNegative: the person/thing {e['vp_sg_neg']}")
        key = sha1("|".join(e["rule_id"] + e["atom"] for e in chunk))[:16]
        jobs.append({"key": key, "ents": [e["rule_id"] + "|" + e["atom"] for e in chunk],
                     "messages": [{"role": "system", "content": AUDIT_SYS}, {"role": "user", "content": "\n\n".join(body)}]})
    dump(W / "lexicon_audit_jobs.json", [{"key": j["key"], "ents": j["ents"]} for j in jobs])
    return run_jobs("lexicon_audit", cap, model, jobs, RAW / "lexicon_audit.jsonl", logger, concurrency=8,
             params={"temperature": 0.0, "max_tokens": 1200, **ANTHROPIC_NO_THINK},
             validate=lambda j, p: isinstance(p, dict) and isinstance(p.get("verdicts"), list))


def build():
    from llm import cached
    ents = {e["rule_id"] + "|" + e["atom"]: e for e in json.loads((W / "lexicon_checked.json").read_text())}
    res = cached(RAW / "lexicon_audit.jsonl")
    log = Counter()
    jobs_p = W / "lexicon_audit_jobs.json"
    for e in ents.values():
        if not e["check_fails"]:
            e["audit"] = "PENDING"  # overwritten below when the Sonnet audit ran
    for j in (json.loads(jobs_p.read_text()) if jobs_p.exists() else []):
        if j["key"] not in res:
            log["audit_job_missing"] += 1; continue
        vs = {int(v.get("entry", 0)): v for v in res[j["key"]]["parsed"]["verdicts"] if str(v.get("entry", "")).isdigit()}
        for k, eid in enumerate(j["ents"], 1):
            v = vs.get(k)
            ents[eid]["audit"] = (v or {}).get("verdict", "MISSING")
            ents[eid]["audit_reason"] = (v or {}).get("reason")
            log["audit_" + ents[eid]["audit"]] += 1
            if v and v.get("verdict") == "WRONG":
                log["wrong_" + str(v.get("reason"))] += 1
    # Every check-passed entry stays in lexicon.json with its audit status (OK / WRONG / PENDING / MISSING) so that the
    # sha1-seeded composition is stable across the audit: compose.py REJECTS any sentence drawing a WRONG entry
    # (MISSING = the audit call returned no verdict for it; treated like PENDING = not yet audited).
    ok = [e for e in ents.values() if e.get("audit") in ("OK", "PENDING", "WRONG", "MISSING")]
    log["audit_pending"] = sum(e.get("audit") == "PENDING" for e in ok)
    ok.sort(key=lambda e: (e["source"].startswith("MALLS"), sha1(e["rule_id"] + e["atom"])))
    # 2e name collisions: same predicate name, different arity or different phrase meaning -> rename later one
    by_name, lex, seen_vp = defaultdict(list), [], set()
    for e in ok:
        vpn = re.sub(r"\s+", " ", e["vp_sg_pos"].lower())
        if (e["atom"], vpn) in seen_vp:
            log["dup_atom_vp"] += 1; continue
        seen_vp.add((e["atom"], vpn))
        same = by_name[e["pred"]]
        name = e["pred"]
        if any(x["arity"] != e["arity"] or (x["const"] == e["const"] and x["vp_norm"] != vpn) for x in same):
            name = f"{e['pred']}_{len(same) + 1}"
            log["renamed"] += 1
        e2 = {**e, "pred_final": name, "vp_norm": vpn}
        if e["arity"] == 1:
            e2["atom_final"] = f"{name}(x)"
        elif e["const_pos"] == 1:
            e2["atom_final"] = f"{name}(x, {e['const']})"
        else:
            e2["atom_final"] = f"{name}({e['const']}, x)"
        e2["lexicon_id"] = sha1(e2["atom_final"] + "|" + e["vp_sg_pos"])[:10]
        same.append(e2)
        lex.append(e2)
    groups = defaultdict(lambda: {"sortal": [], "nonsortal": []})
    for e in lex:
        if e.get("audit") == "WRONG":
            continue
        groups[e["subject_sort"]]["sortal" if e["sortal"] else "nonsortal"].append(e["lexicon_id"])
    usable = {}
    byid = {e["lexicon_id"]: e for e in lex}
    for s, g in groups.items():
        rules_ns = {byid[i]["rule_id"] for i in g["nonsortal"]}
        usable[s] = {"n_sortal": len(g["sortal"]), "n_nonsortal": len(g["nonsortal"]), "n_rules_nonsortal": len(rules_ns),
                     "usable": len(g["nonsortal"]) >= 12 and len(rules_ns) >= 4 and len(g["sortal"]) >= 1}
    keep = ["lexicon_id", "atom_final", "pred_final", "pred", "arity", "const", "const_pos", "vp_sg_pos", "vp_sg_neg",
            "noun", "sortal", "subject_sort", "role", "rule_id", "source", "source_text", "source_fol", "atom", "audit",
            "audit_reason"]
    out = {"n_entries": len(lex), "n_usable_not_wrong": sum(e.get("audit") != "WRONG" for e in lex),
           "audit_counts": dict(Counter(e.get("audit") for e in lex)), "groups": usable, "log": dict(log),
           "entries": [{k: e.get(k) for k in keep} for e in lex]}
    dump(ROOT / "lexicon.json", out)
    logger.info(f"lexicon {len(lex)} entries; groups {usable}; log {dict(log)}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["extract", "extract_malls", "check", "audit", "build"])
    ap.add_argument("--cap", type=float, default=0.4)
    a = ap.parse_args()
    stop = None
    if a.cmd == "extract":
        stop = extract("source_rules.json", a.cap)[1]
    elif a.cmd == "extract_malls":
        stop = extract("source_rules_malls.json", a.cap)[1]
    elif a.cmd == "check":
        check_all()
    elif a.cmd == "audit":
        stop = audit(a.cap)[1]
    else:
        build()
    raise SystemExit(3 if stop == "KEYLIMIT" else 0)  # a phase-cap stop is a planned truncation
