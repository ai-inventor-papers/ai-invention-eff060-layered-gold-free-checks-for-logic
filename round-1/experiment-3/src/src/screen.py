#!/usr/bin/env python3
"""STEP 1: build the SHARED SCREEN (track L = released Logic-LM outputs vs trusted references;
track H = original human gold vs corrected gold), label every item with the shared labeller, write
results/screen_items.json + results/screen_label_hash.txt, plus results/units.json (the translation units
that peers and self-consistency samples are generated for).
"""
from __future__ import annotations

import hashlib
import json
import multiprocessing as mp
import random
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import pandas as pd
import requests
from loguru import logger

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
from common import LLM_SYSTEMS, eqmv, item_id, label, norm, safe_parse, strata  # noqa: E402

D = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/iter_3/gen_hypo/claude_agent/data")
LL = ROOT / "data" / "logiclm"
RES = ROOT / "results"
PFX = "Based on the above information, is the following statement true, false, or uncertain?"
URL = "https://raw.githubusercontent.com/teacherpeterpan/Logic-LLM/main/outputs/logic_programs/FOLIO_dev_{}.json"

logger.remove()
logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss}|{level:<7}|{message}")
logger.add(ROOT / "logs" / "screen.log", rotation="30 MB", level="DEBUG")


def fetch_logiclm() -> dict[str, list]:
    out = {}
    for s in LLM_SYSTEMS:
        p = LL / f"FOLIO_dev_{s}.json"
        if not p.exists():
            for attempt in range(3):
                try:
                    r = requests.get(URL.format(s), timeout=60)
                    r.raise_for_status()
                    p.write_bytes(r.content)
                    break
                except requests.RequestException:
                    logger.exception(f"download {s} attempt {attempt}")
                    time.sleep(2 ** attempt)
        out[s] = json.loads(p.read_text())
        logger.info(f"T1 Logic-LM {s}: {len(out[s])} entries")
        assert len(out[s]) >= 200, f"{s} has only {len(out[s])} entries (truncated download?)"
    return out


def parse_program(raw: str) -> dict:
    sec, out = None, {"premises": [], "conclusion": []}
    for line in raw.split("\n"):
        t = line.strip()
        if t.startswith("Predicates:"):
            sec = "pred"; continue
        if t.startswith("Premises:"):
            sec = "premises"; continue
        if t.startswith("Conclusion:"):
            sec = "conclusion"; continue
        if ":::" in t and sec in ("premises", "conclusion"):
            f, n = t.split(":::", 1)
            out[sec].append((f.strip(), n.strip()))
    return out


def split_sents(ctx: str) -> list[str]:
    return [x for x in re.split(r"(?<=[.!?])\s+", ctx.strip()) if x.strip()]


def load_curated():
    rows = [json.loads(l) for l in open(D / "DSAVlab-UNIUD_FOLIO_validation-curated__FOLIO_instances.jsonl") if l.strip()]
    stories, concl, cur = {}, [], None
    for r in rows:
        if str(r["id"]).startswith("story"):
            cur = r["id"]
            stories[cur] = r
        else:
            assert cur is not None, f"conclusion {r['id']} has no preceding story row"
            concl.append({**r, "story_id": cur})
    malls = [json.loads(l) for l in open(D / "DSAVlab-UNIUD_MALLS_test_subset-CURATED__MALLS_instances.jsonl") if l.strip()]
    return stories, concl, malls


def agreed_premises(stories: dict, concl: list) -> tuple[dict, dict]:
    """norm(premise NL) -> original premise FOL, only where original ≡mv folio-refined premise FOL."""
    csv = pd.read_csv(D / "folio_refined_validation.csv")
    by_concl = defaultdict(list)
    for _, r in csv.iterrows():
        by_concl[norm(str(r["nl conclusion"]))].append(r)
    stats = Counter()
    agreed, info = {}, {}
    story_first_concl = {}
    for c in concl:
        story_first_concl.setdefault(c["story_id"], c)
    for sid, st in stories.items():
        c = story_first_concl.get(sid)
        cands = by_concl.get(norm(c["NL_sentence"])) if c else None
        if not cands:
            stats["story_no_refined_row"] += 1
            continue
        r = cands[0]
        nls = [x for x in str(r["nl premises"]).split("\n") if x.strip()]
        refs = [x for x in str(r["fol premises"]).split("\n") if x.strip()]
        olds = [x for x in str(st.get("FOL_sentence_old") or "").split("\n") if x.strip()]
        if not (len(nls) == len(refs) == len(olds)):
            stats["story_premise_misaligned"] += 1
            logger.warning(f"{sid}: premise count mismatch nl={len(nls)} refined={len(refs)} orig={len(olds)}")
            continue
        for nl, rf, od in zip(nls, refs, olds):
            stats["premises"] += 1
            eo, er = safe_parse(od), safe_parse(rf)
            if eo is None or er is None:
                stats["premise_unparseable"] += 1
                continue
            ok, route = eqmv(eo, er)
            if ok is True:
                k = norm(nl)
                if k in agreed and agreed[k] != od.strip():
                    stats["premise_conflict"] += 1
                    continue
                agreed[k] = od.strip()
                info[k] = {"nl": nl.strip(), "story_id": sid, "route": route}
                stats["agreed"] += 1
            else:
                stats["disagreed" if ok is False else "timeout"] += 1
    logger.info(f"agreed premises: {dict(stats)}")
    return agreed, {"stats": dict(stats), "info": info}


def label_job(it: dict) -> dict:
    t0 = time.time()
    lab = label(it["candidate_fol"], it["reference_fol"], ambiguous=it["ambiguous"], track=it["track"])
    it = dict(it)
    it.update(lab)
    it["label_seconds"] = round(time.time() - t0, 2)
    return it


@logger.catch(reraise=True)
def main():
    RES.mkdir(exist_ok=True)
    ll = fetch_logiclm()
    stories, concl, malls = load_curated()
    logger.info(f"curated: {len(stories)} stories, {len(concl)} conclusions, {len(malls)} MALLS")
    agreed, ainfo = agreed_premises(stories, concl)
    cmap = defaultdict(list)
    for c in concl:
        cmap[norm(c["NL_sentence"])].append(c)

    items, units = [], []
    # ---------------------------------------------------------------- track L
    entry_match = {}  # Logic-LM entry id -> curated conclusion (matched through any system)
    progs = {s: {e["id"]: parse_program(e["raw_logic_programs"][0] if e.get("raw_logic_programs") else "") for e in ll[s]} for s in LLM_SYSTEMS}
    ctx = {e["id"]: e for e in ll["gpt-4"]}
    for s in LLM_SYSTEMS:
        for e in ll[s]:
            ctx.setdefault(e["id"], e)
    match_mode = Counter()
    for eid, e in ctx.items():
        q = e["question"].strip()
        qn = q[len(PFX):].strip() if q.startswith(PFX) else q
        hit = cmap.get(norm(qn))
        mode = "question"
        if not hit:
            for s in LLM_SYSTEMS:
                cl = progs[s].get(eid, {}).get("conclusion") or []
                if cl and cmap.get(norm(cl[0][1])):
                    hit, mode = cmap[norm(cl[0][1])], "nl_copy"
                    break
        if hit:
            if len(hit) > 1:
                logger.warning(f"{eid}: {len(hit)} curated conclusions share the text; using the first")
            entry_match[eid] = hit[0]
            match_mode[mode] += 1
    matched_concl = {c["id"] for c in entry_match.values()}
    match_rate = len(matched_concl) / len(concl)
    fallback = len(matched_concl) < 150
    logger.info(f"T1 conclusion match: {len(matched_concl)}/{len(concl)} = {match_rate:.3f} modes={dict(match_mode)}; "
                f"MATCH-RATE FALLBACK {'FIRED (agreed premises of matched stories extend track L; included by default)' if fallback else 'not fired'}")

    prem_slots = {}  # eid -> {system: [(nl_line, key, fol)]}
    prem_mode = Counter()
    for eid, e in ctx.items():
        sents = split_sents(e["context"])
        prem_slots[eid] = {}
        for s in LLM_SYSTEMS:
            pr = progs[s].get(eid, {"premises": [], "conclusion": []})
            slots = []
            for i, (f, n) in enumerate(pr["premises"]):
                key = norm(n)
                if key not in agreed and len(pr["premises"]) == len(sents) and norm(sents[i]) in agreed:
                    key = norm(sents[i])
                    prem_mode["context_position"] += 1
                elif key in agreed:
                    prem_mode["nl_copy"] += 1
                slots.append((n, key, f))
            prem_slots[eid][s] = slots

    seen = set()
    first_story_entry = {}  # premise key -> first Logic-LM entry id (entry order) containing it
    for eid in ctx:
        for s in LLM_SYSTEMS:
            for n, key, f in prem_slots[eid][s]:
                if key in agreed:
                    first_story_entry.setdefault(key, eid)
    for s in LLM_SYSTEMS:
        for e in ll[s]:
            eid = e["id"]
            c = entry_match.get(eid)
            pr = progs[s].get(eid, {"premises": [], "conclusion": []})
            if c is not None:
                cl = pr["conclusion"]
                fol = cl[0][0] if cl else ""
                text = c["NL_sentence"]
                iid = item_id(s, text, fol)
                if iid not in seen:
                    seen.add(iid)
                    items.append({"item_id": iid, "track": "L", "kind": "conclusion", "system": s, "text": text,
                                  "candidate_fol": fol, "reference_fol": c["FOL_sentence"], "ambiguous": False,
                                  "curator_ambiguous": str(c.get("ambiguity")) == "True",
                                  "story_id": c["story_id"], "source": f"logiclm:{eid}", "concl_id": c["id"],
                                  "logiclm_entry": eid, "missing_conclusion_line": not cl})
            for n, key, f in prem_slots[eid][s]:
                if key not in agreed:
                    continue
                text = ainfo["info"][key]["nl"]
                iid = item_id(s, text, f)
                if iid in seen:
                    continue
                seen.add(iid)
                items.append({"item_id": iid, "track": "L", "kind": "premise", "system": s, "text": text,
                              "candidate_fol": f, "reference_fol": agreed[key], "ambiguous": False,
                              "story_id": ainfo["info"][key]["story_id"], "source": f"logiclm:{eid}",
                              "logiclm_entry": eid, "first_entry_for_sentence": first_story_entry[key] == eid})
    logger.info(f"premise mapping modes: {dict(prem_mode)}")
    # ---------------------------------------------------------------- track H
    for c in concl:
        text = c["NL_sentence"]
        items.append({"item_id": item_id("human_original", text, c["FOL_sentence_old"] or ""), "track": "H",
                      "kind": "conclusion", "system": "human_original", "text": text,
                      "candidate_fol": c["FOL_sentence_old"] or "", "reference_fol": c["FOL_sentence"],
                      "ambiguous": str(c.get("ambiguity")) == "True", "story_id": c["story_id"],
                      "source": "FOLIO-val-curated", "concl_id": c["id"]})
    for m in malls:
        text = m["NL_sentence"]
        items.append({"item_id": item_id("human_original", text, m["FOL_sentence_old"] or ""), "track": "H",
                      "kind": "malls", "system": "human_original", "text": text,
                      "candidate_fol": m["FOL_sentence_old"] or "", "reference_fol": m["FOL_sentence_new"],
                      "ambiguous": str(m.get("ambiguity")) == "True", "story_id": None,
                      "source": "MALLS-test-curated", "malls_id": m["id"]})
    assert all(it["reference_fol"] for it in items if it["track"] == "L"), "track-L item without reference"
    for it in items:
        it["sentence_key"] = norm(it["text"])
        it["strata"] = strata(it["text"], it["reference_fol"])

    # ---------------------------------------------------------------- units (translation prompts for peers/SC)
    story_nl = {sid: st["NL_sentence"] for sid, st in stories.items()}
    concl_entry = {}
    for eid, c in entry_match.items():
        concl_entry.setdefault(c["id"], eid)
    for c in concl:
        eid = concl_entry.get(c["id"])
        if eid:
            problem, question = ctx[eid]["context"], ctx[eid]["question"]
            slots = {s: [(n, k) for n, k, _ in prem_slots[eid][s]] for s in LLM_SYSTEMS}
            sents = split_sents(ctx[eid]["context"])
        else:
            problem, question = story_nl[c["story_id"]], f"{PFX} {c['NL_sentence']}"
            slots, sents = {}, split_sents(story_nl[c["story_id"]])
        units.append({"unit_id": f"F:{c['id']}", "type": "U_F", "concl_id": c["id"], "story_id": c["story_id"],
                      "logiclm_entry": eid, "problem": problem, "question": question,
                      "conclusion_key": norm(c["NL_sentence"]), "premise_slots": slots,
                      "context_sents": [(x, norm(x)) for x in sents]})
    for m in malls:
        units.append({"unit_id": f"M:{m['id']}", "type": "U_M", "malls_id": m["id"], "sentence": m["NL_sentence"],
                      "conclusion_key": norm(m["NL_sentence"])})
    # premise sentence -> unit that supplies its peer / SC translations (first unit, curated jsonl order)
    prem_unit = {}
    for u in units:
        if u["type"] != "U_F" or not u["logiclm_entry"]:
            continue
        keys = {k for sl in u["premise_slots"].values() for _, k in sl} | {k for _, k in u["context_sents"]}
        for k in keys:
            if k in agreed:
                prem_unit.setdefault(k, u["unit_id"])
    # premise sentences that occur only in Logic-LM entries whose conclusion is unmatched: add premise-only units
    # (U_P, same Logic-LM prompt; their conclusion translation is ignored), first entry in entry order
    needed = {it["sentence_key"] for it in items if it["kind"] == "premise"} - set(prem_unit)
    for eid, e in ctx.items():
        keys = {k for s in LLM_SYSTEMS for _, k, _ in prem_slots[eid][s]} | {norm(x) for x in split_sents(e["context"])}
        if not (keys & needed):
            continue
        uid = f"P:{eid}"
        units.append({"unit_id": uid, "type": "U_P", "concl_id": None, "story_id": None, "logiclm_entry": eid,
                      "problem": e["context"], "question": e["question"], "conclusion_key": None,
                      "premise_slots": {s: [(n, k) for n, k, _ in prem_slots[eid][s]] for s in LLM_SYSTEMS},
                      "context_sents": [(x, norm(x)) for x in split_sents(e["context"])]})
        for k in keys & needed:
            prem_unit[k] = uid
        needed -= keys
    n_no_unit = sum(1 for it in items if it["kind"] == "premise" and it["sentence_key"] not in prem_unit)
    logger.info(f"premise sentences with a source unit: {len(prem_unit)}; track-L premise items without unit: {n_no_unit}")

    # ---------------------------------------------------------------- labelling
    t0 = time.time()
    with mp.get_context("spawn").Pool(4) as pool:
        labelled = pool.map(label_job, items, chunksize=1)
    logger.info(f"labelled {len(labelled)} items in {time.time() - t0:.0f}s")
    assert all(not (x["label"] == "ERROR" and x.get("underlying_label")) for x in labelled)
    labelled.sort(key=lambda x: (x["track"], x["item_id"]))
    lines = sorted(f"{x['item_id']}\t{x['label']}" for x in labelled)
    h = hashlib.sha256("\n".join(lines).encode()).hexdigest()
    (RES / "screen_items.json").write_text(json.dumps(labelled, ensure_ascii=False, indent=1))
    (RES / "screen_label_hash.txt").write_text(h + "\n")
    (RES / "units.json").write_text(json.dumps({"units": units, "premise_unit": prem_unit}, ensure_ascii=False, indent=1))

    # ---------------------------------------------------------------- T1 report
    cnt = Counter((x["track"], x["system"], x["label"]) for x in labelled)
    vs = Counter((x["track"], x["system"], x["auto_class"], x.get("vocab_strict")) for x in labelled if x["label"] == "CORRECT")
    rnd = random.Random(0)
    L = [x for x in labelled if x["track"] == "L"]
    samples = []
    for x in rnd.sample(L, min(10, len(L))):
        eid = x["logiclm_entry"]
        pr = progs[x["system"]][eid]
        cand_nl = [n for f, n in pr["premises"] + pr["conclusion"] if f == x["candidate_fol"]]
        samples.append({"logiclm_nl": cand_nl[0] if cand_nl else None, "curated_nl": x["text"]})
    report = {"logiclm_entries": {s: len(ll[s]) for s in LLM_SYSTEMS},
              "curated": {"stories": len(stories), "conclusions": len(concl), "malls": len(malls)},
              "conclusion_match": {"matched": len(matched_concl), "of": len(concl), "rate": match_rate,
                                   "modes": dict(match_mode), "fallback_fired": fallback},
              "agreed_premises": ainfo["stats"], "premise_mapping_modes": dict(prem_mode),
              "n_items": len(labelled), "label_hash": h,
              "counts": {"|".join(k): v for k, v in sorted(cnt.items())},
              "correct_vocab_strict_split": {"|".join(map(str, k)): v for k, v in sorted(vs.items(), key=str)},
              "matched_pairs_sample": samples,
              "n_track_L_by_kind": dict(Counter(x["kind"] for x in L)),
              "label_seconds_total": round(sum(x["label_seconds"] for x in labelled), 1)}
    (RES / "screen_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1))
    for k, v in sorted(cnt.items()):
        logger.info(f"T1 {k}: {v}")
    logger.info(f"label hash {h}")


if __name__ == "__main__":
    main()
