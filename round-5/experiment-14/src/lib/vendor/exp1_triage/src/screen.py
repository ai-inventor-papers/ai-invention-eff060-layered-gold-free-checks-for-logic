"""STAGE 2: deterministic SHARED frozen screen.

TRACK L  Logic-LM released FOLIO-dev programs (gpt-3.5-turbo, gpt-4, text-davinci-003); every (system, nl, fol) line whose
         norm(nl) equals a curated (arXiv 2606.02837, HF DSAVlab-UNIUD) FOLIO-validation conclusion (ref = corrected FOL),
         extended (distinct matched conclusions < 150) ONLY with premises of matched stories whose original FOLIO FOL and
         folio-refined FOL agree (EQUIV/VOCAB) (ref = refined FOL).
TRACK H  302 curated items (202 FOLIO conclusions + 100 MALLS-test): candidate = original gold, ref = corrected gold.
HREF     corrected gold as its own candidate (label CORRECT_REF; this experiment only, NOT in screen_items.json).
item_id = sha1(system + '|' + norm(text) + '|' + candidate_fol)[:16]; strata from the REFERENCE formula.
"""
from __future__ import annotations

import hashlib
import json
import multiprocessing as mp
import os
import re
from collections import Counter
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import pandas as pd
from loguru import logger

from fol import parse

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CACHE = ROOT / "cache"
SYSTEMS = ["gpt-3.5-turbo", "gpt-4", "text-davinci-003"]
EXC_RE = re.compile(r"\b(unless|except|excluding|but not|without|other than|provided that)\b", re.I)


def norm(t: str) -> str:
    t = t.lower().replace("’", "'").replace("‘", "'")
    t = re.sub(r"(\w)'(\w)", r"\1\2", t)  # inner apostrophes removed
    t = re.sub(r"[^\w\s]", " ", t)
    return " ".join(t.split())


def sha1(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()


def item_id(system: str, text: str, fol: str) -> str:
    return sha1(system + "|" + norm(text) + "|" + fol)[:16]


def load_jsonl(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]


# ------------------------------------------------------------------ strata (reference formula)
def depth(e) -> int:
    k = e[0]
    if k == "atom":
        return 0
    if k in ("all", "ex"):
        return 1 + depth(e[2])
    if k == "not":
        return depth(e[1])
    return 1 + max(depth(e[1]), depth(e[2]))


def n_quant(e) -> int:
    k = e[0]
    if k == "atom":
        return 0
    if k in ("all", "ex"):
        return 1 + n_quant(e[2])
    if k == "not":
        return n_quant(e[1])
    return n_quant(e[1]) + n_quant(e[2])


def n_conditions(e, in_ante=False) -> int:
    """Atom occurrences lying in the left operand of some → or ↔ (antecedent / restrictor positions)."""
    k = e[0]
    if k == "atom":
        return 1 if in_ante else 0
    if k in ("all", "ex"):
        return n_conditions(e[2], in_ante)
    if k == "not":
        return n_conditions(e[1], in_ante)
    if k in ("imp", "iff"):
        return n_conditions(e[1], True) + n_conditions(e[2], in_ante)
    return n_conditions(e[1], in_ante) + n_conditions(e[2], in_ante)


def strata(text: str, ref_fol: str) -> dict:
    w = len(text.split())
    out = {"words": w, "len_bin": "<12" if w < 12 else ("12-19" if w < 20 else ">=20"),
           "exception": bool(EXC_RE.search(text))}
    try:
        e = parse(ref_fol)
        out.update(n_quant=n_quant(e), depth=depth(e), n_conditions=n_conditions(e))
    except Exception:  # noqa: BLE001
        out.update(n_quant=None, depth=None, n_conditions=None)
    return out


# ------------------------------------------------------------------ Logic-LM parsing
def parse_program(prog: str) -> list[tuple[str, str, str]]:
    """-> [(role, fol, nl)] for lines in the Premises / Conclusion sections."""
    out, sec = [], None
    for line in prog.split("\n"):
        s = line.strip()
        if s.startswith("Predicates:"):
            sec = "pred"; continue
        if s.startswith("Premises:"):
            sec = "premise"; continue
        if s.startswith("Conclusion:"):
            sec = "conclusion"; continue
        m = re.match(r"(.+?):::(.+)", s)
        if m and sec in ("premise", "conclusion"):
            out.append((sec, m.group(1).strip(), m.group(2).strip()))
    return out


def load_logiclm() -> dict:
    out = {}
    for s in SYSTEMS:
        p = DATA / "logiclm" / f"FOLIO_dev_{s}.json"
        if not p.exists():
            import requests
            url = f"https://raw.githubusercontent.com/teacherpeterpan/Logic-LLM/main/outputs/logic_programs/FOLIO_dev_{s}.json"
            r = requests.get(url, timeout=60)
            r.raise_for_status()
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(r.text)
        out[s] = json.loads(p.read_text())
        logger.info(f"Logic-LM {s}: n_records={len(out[s])}")
    return out


# ------------------------------------------------------------------ labelling (parallel, cached)
def label_many(pairs: list[tuple[str, str]], budget_s: float = 25.0, hard_s: int = 60, workers: int = 4) -> dict:
    """pairs: [(cand, ref)] -> {sha1(cand|ref|budget): label record}. Cached in cache/labels.jsonl."""
    CACHE.mkdir(exist_ok=True)
    cp = CACHE / "labels.jsonl"
    cache = {}
    if cp.exists():
        for r in load_jsonl(cp):
            cache[r["key"]] = r
    todo = {}
    for c, r in pairs:
        k = sha1(f"{c}|{r}|{budget_s}")
        if k not in cache:
            todo[k] = (k, c, r, budget_s, hard_s)
    logger.info(f"label_many: {len(pairs)} pairs, {len(todo)} uncached")
    if todo:
        os.environ["PYTHONHASHSEED"] = "0"  # repair_census fingerprint uses hash(); fix it in spawned workers
        from labeller import label_job
        with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn")) as pool, cp.open("a") as fh:
            futs = [pool.submit(label_job, a) for a in todo.values()]
            for i, f in enumerate(as_completed(futs)):
                res = f.result()
                cache[res["key"]] = res
                fh.write(json.dumps(res, ensure_ascii=False) + "\n"); fh.flush()
                if (i + 1) % 50 == 0:
                    logger.info(f"  labelled {i + 1}/{len(todo)}")
    return {sha1(f"{c}|{r}|{budget_s}"): cache[sha1(f"{c}|{r}|{budget_s}")] for c, r in pairs}


def lab_of(labels: dict, c: str, r: str, budget_s: float = 25.0) -> dict:
    return labels[sha1(f"{c}|{r}|{budget_s}")]


# ------------------------------------------------------------------ build
def build(max_items: int | None = None, systems: list[str] | None = None) -> dict:
    systems = systems or SYSTEMS
    folio = load_jsonl(DATA / "DSAVlab-UNIUD_FOLIO_validation-curated__FOLIO_instances.jsonl")
    malls = load_jsonl(DATA / "DSAVlab-UNIUD_MALLS_test_subset-CURATED__MALLS_instances.jsonl")
    conc = {}
    for r in folio:
        if str(r["id"]).startswith("story"):
            continue
        conc.setdefault(norm(r["NL_sentence"]), r)
    stories = [r for r in folio if str(r["id"]).startswith("story")]
    # --- agreed premises: curated story rows (original FOL) x folio-refined (refined FOL), by story text + line index
    fr = pd.read_csv(DATA / "folio_refined_validation.csv")
    refined = {}
    for _, r in fr.iterrows():
        nl = [x.strip() for x in str(r["nl premises"]).split("\n") if x.strip()]
        fo = [x.strip() for x in str(r["fol premises"]).split("\n") if x.strip()]
        refined[norm(" ".join(nl))] = (nl, fo)
    prem_pairs, prem_meta = [], []
    n_story_match = n_story_aligned = 0
    for r in stories:
        k = norm(r["NL_sentence"])
        old = [x.strip() for x in r["FOL_sentence_old"].split("\n") if x.strip()]
        if k not in refined:
            continue
        n_story_match += 1
        nl, fo = refined[k]
        if not (len(nl) == len(fo) == len(old)):
            continue
        n_story_aligned += 1
        for i, (t, o, f) in enumerate(zip(nl, old, fo)):
            prem_pairs.append((o, f))
            prem_meta.append({"story_id": r["id"], "idx": i, "text": t, "orig": o, "refined": f})
    logger.info(f"premise agreement: curated stories {len(stories)}, matched to folio-refined {n_story_match}, "
                f"line-aligned {n_story_aligned}, premise lines {len(prem_pairs)}")
    # --- track H + premise agreement labels
    H = []
    for r in malls:
        H.append({"src": "MALLS", "cid": f"malls_{r['id']}", "text": r["NL_sentence"], "cand": r["FOL_sentence_old"],
                  "ref": r["FOL_sentence_new"], "amb": bool(r.get("ambiguity") in (True, "True", "true"))})
    for r in folio:
        if str(r["id"]).startswith("story"):
            continue
        H.append({"src": "FOLIO-concl", "cid": r["id"], "text": r["NL_sentence"], "cand": r["FOL_sentence_old"],
                  "ref": r["FOL_sentence"], "amb": bool(r.get("ambiguity") in (True, "True", "true"))})
    # --- track L candidates
    llm = load_logiclm()
    raw_L, unmatched_conc = [], Counter()
    agreed_lookup = {}
    need = [(h["cand"], h["ref"]) for h in H] + prem_pairs
    labels = label_many(need)
    for pm, (o, f) in zip(prem_meta, prem_pairs):
        st = lab_of(labels, o, f)["status"]
        pm["agree_status"] = st
        if st in ("EQUIV", "VOCAB"):
            agreed_lookup.setdefault(norm(pm["text"]), pm)
    logger.info(f"agreed premises: {len(agreed_lookup)} distinct texts (of {len(prem_meta)} lines); "
                f"status {dict(Counter(p['agree_status'] for p in prem_meta))}")
    matched_conc = set()
    story_of_ctx = {}
    for s in systems:
        for rec in llm[s]:
            lines = parse_program(rec["raw_logic_programs"][0]) if rec.get("raw_logic_programs") else []
            ctx = norm(rec["context"])
            for role, fol, nl in lines:
                n = norm(nl)
                if role == "conclusion":
                    if n in conc:
                        matched_conc.add(n)
                        story_of_ctx.setdefault(ctx, set()).add(conc[n]["id"])
                        raw_L.append((s, rec["id"], ctx, "conclusion", fol, nl, n))
                    else:
                        unmatched_conc[nl] += 1
                else:
                    raw_L.append((s, rec["id"], ctx, "premise", fol, nl, n))
    n_conc_distinct = len(matched_conc)
    extend = n_conc_distinct < 150
    logger.info(f"track-L conclusion match: distinct {n_conc_distinct}/{len(conc)}; extension with agreed premises of "
                f"matched stories: {extend}")
    L = []
    for s, rid, ctx, role, fol, nl, n in raw_L:
        if role == "conclusion":
            r = conc[n]
            L.append({"system": s, "record": rid, "role": role, "story_id": str(r["id"]).rsplit("_", 1)[0],
                      "text": r["NL_sentence"], "cand": fol, "ref": r["FOL_sentence"],
                      "amb": bool(r.get("ambiguity") in (True, "True", "true")), "ref_source": "curated_corrected"})
        elif extend and ctx in story_of_ctx and n in agreed_lookup:
            pm = agreed_lookup[n]
            L.append({"system": s, "record": rid, "role": role, "story_id": pm["story_id"], "text": pm["text"],
                      "cand": fol, "ref": pm["refined"], "amb": False, "ref_source": "agreed_premise_refined"})
    # dedupe by item_id (same story appears in several Logic-LM records)
    seen, Ld = set(), []
    for x in L:
        iid = item_id(x["system"], x["text"], x["cand"])
        if iid in seen:
            continue
        seen.add(iid)
        x["item_id"] = iid
        Ld.append(x)
    if max_items:
        Ld = sorted(Ld, key=lambda x: x["item_id"])[:max_items]
    labels.update(label_many([(x["cand"], x["ref"]) for x in Ld]))
    href = []
    items = []
    for x in sorted(Ld, key=lambda x: x["item_id"]):
        lb = lab_of(labels, x["cand"], x["ref"])
        items.append({"item_id": x["item_id"], "track": "L", "system": x["system"], "role": x["role"],
                      "story_id": x["story_id"], "text": x["text"], "candidate_fol": x["cand"], "reference_fol": x["ref"],
                      "ref_source": x["ref_source"], "label": lb["label"], "auto_class": lb["auto_class"],
                      "repair_ops": lb.get("ops"), "ambiguous": x["amb"], "strata": strata(x["text"], x["ref"])})
    for h in H:
        lb = lab_of(labels, h["cand"], h["ref"])
        lab = lb["label"]
        if h["amb"] and lab not in ("CORRECT", "UNPARSEABLE", "REF_UNPARSEABLE"):
            lab = "READING_CHOICE"
        iid = item_id("human_original", h["text"], h["cand"])
        items.append({"item_id": iid, "track": "H", "system": "human_original", "role": h["src"],
                      "story_id": h["cid"], "text": h["text"], "candidate_fol": h["cand"], "reference_fol": h["ref"],
                      "ref_source": "curated_corrected", "label": lab, "auto_class": lb["auto_class"],
                      "repair_ops": lb.get("ops"), "ambiguous": h["amb"], "strata": strata(h["text"], h["ref"])})
        href.append({"item_id": item_id("human_corrected", h["text"], h["ref"]), "track": "HREF",
                     "system": "human_corrected", "role": h["src"], "story_id": h["cid"], "text": h["text"],
                     "candidate_fol": h["ref"], "reference_fol": h["ref"], "label": "CORRECT_REF",
                     "auto_class": "REF", "repair_ops": None, "ambiguous": h["amb"],
                     "strata": strata(h["text"], h["ref"])})
    items.sort(key=lambda x: (x["track"], x["item_id"]))
    labs = sorted((x["item_id"], x["label"]) for x in items)
    meta = {
        "n_items": len(items),
        "n_by_track_label": {t: dict(Counter(x["label"] for x in items if x["track"] == t)) for t in ("L", "H")},
        "n_by_system_label": {s: dict(Counter(x["label"] for x in items if x["system"] == s)) for s in systems},
        "n_by_role_L": dict(Counter(x["role"] for x in items if x["track"] == "L")),
        "auto_class_L": dict(Counter(x["auto_class"] for x in items if x["track"] == "L")),
        "auto_class_H": dict(Counter(x["auto_class"] for x in items if x["track"] == "H")),
        "match_rate": {"distinct_conclusions_matched": n_conc_distinct, "curated_conclusions": len(conc),
                       "rate": round(n_conc_distinct / max(1, len(conc)), 4), "extension_applied": extend,
                       "n_unmatched_conclusion_lines": sum(unmatched_conc.values())},
        "premise_agreement": {"curated_story_rows": len(stories), "matched_to_refined": n_story_match,
                              "line_aligned_stories": n_story_aligned, "premise_lines": len(prem_meta),
                              "status_counts": dict(Counter(p["agree_status"] for p in prem_meta)),
                              "agreed_distinct_texts": len(agreed_lookup)},
        "strata_note": "strata computed from the REFERENCE formula / text so they are identical across experiments",
        "labels_sha256": hashlib.sha256(json.dumps(labs).encode()).hexdigest(),
        "code_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                        for p in sorted((ROOT / "src").glob("*.py")) if p.name in
                        ("fol.py", "repair_census.py", "labeller.py", "screen.py", "rewrites.py")},
    }
    return {"items": items, "href": href, "meta": meta, "unmatched_conclusions": sorted(unmatched_conc),
            "premise_meta": prem_meta}


def build_invariance(items: list[dict], n: int = 150) -> list[dict]:
    from rewrites import rewrite_all
    corr = sorted([x for x in items if x["track"] == "L" and x["label"] == "CORRECT"], key=lambda x: x["item_id"])[:n]
    out = []
    for x in corr:
        for r in rewrite_all(x["candidate_fol"]):
            out.append({"item_id": x["item_id"], **r})
    return out
