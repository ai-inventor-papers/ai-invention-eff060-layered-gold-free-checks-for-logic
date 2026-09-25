"""SHARED FROZEN SCREEN (gen_strat_1 definition): track L = Logic-LM FOLIO-dev outputs vs trusted references,
track H = curated human original gold vs corrected gold (FOLIO-validation conclusions + MALLS-test 100).

Writes data/screen_items.json (sorted by item_id), data/label_vector.sha1, data/screen_build_log.json.
Labelling runs in a spawn ProcessPool with PYTHONHASHSEED=0 (deterministic fingerprints / set orders).
"""
from __future__ import annotations

import csv
import json
import multiprocessing as mp
import os
import re
import time
from collections import Counter, defaultdict
from concurrent.futures import ProcessPoolExecutor, as_completed

from loguru import logger

from .common import DATA, SRC_DATA, SYSTEMS, item_id, jdump, norm, read_jsonl, sha1

EXC_RE = re.compile(r"\b(unless|except|excluding|other than|apart from|but not|without)\b", re.I)
Q_PREFIX = re.compile(r"^.*?is the following statement true, false, or uncertain\?\s*", re.I | re.S)


# ------------------------------------------------------------------ worker (spawned; PYTHONHASHSEED=0 inherited)
def _label_worker(args):
    key, cand, ref, do_search = args
    import sys
    sys.setrecursionlimit(10000)
    from .labeller.labeller import equivalent_modulo_vocab
    t0 = time.time()
    try:
        r = equivalent_modulo_vocab(cand, ref, do_search=do_search)
    except RecursionError:
        r = {"cls": "UNPARSEABLE", "why": "recursion"}
    except Exception as e:  # noqa: BLE001 - labeller failure is recorded, never silently dropped
        r = {"cls": "TIMEOUT_UNKNOWN", "why": f"labeller_exception:{type(e).__name__}:{str(e)[:100]}"}
    if r.get("search_wall_hit"):
        r = {**r, "cls": "TIMEOUT_UNKNOWN", "why": "search_wall_timeout"}
    r["label_secs"] = round(time.time() - t0, 2)
    return key, r


def label_many(pairs: dict, workers: int = 6, do_search: bool = True) -> dict:
    """pairs: {key: (cand, ref)} -> {key: result}. Deterministic given PYTHONHASHSEED=0."""
    os.environ["PYTHONHASHSEED"] = "0"
    out = {}
    todo = [(k, c, r, do_search) for k, (c, r) in pairs.items()]
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context("spawn")) as pool:
        futs = [pool.submit(_label_worker, a) for a in todo]
        for i, f in enumerate(as_completed(futs)):
            k, r = f.result()
            out[k] = r
            if (i + 1) % 100 == 0:
                logger.info(f"  labelled {i+1}/{len(todo)} ({time.time()-t0:.0f}s)")
    return out


# ------------------------------------------------------------------ Logic-LM programs
def parse_program(raw: str) -> dict | None:
    """Split 'Predicates:/Premises:/Conclusion:' sections; each line 'FOL ::: NL'. None if malformed."""
    if not raw or "Premises:" not in raw or "Conclusion:" not in raw:
        return None
    try:
        pre_part, rest = raw.split("Premises:", 1)
        prem_part, concl_part = rest.split("Conclusion:", 1)
    except ValueError:
        return None
    decl = []
    for ln in pre_part.replace("Predicates:", "").strip().splitlines():
        if ":::" in ln:
            f = ln.split(":::")[0].strip()
            m = re.match(r"\s*([A-Za-z_][A-Za-z0-9_]*)\s*\(([^)]*)\)", f)
            if m:
                decl.append((m.group(1), len([a for a in m.group(2).split(",") if a.strip()])))
            else:
                m2 = re.match(r"\s*([A-Za-z_][A-Za-z0-9_]*)", f)
                if m2:
                    decl.append((m2.group(1), 0))

    def lines(part):
        out, n_bad = [], 0
        for ln in part.strip().splitlines():
            if not ln.strip():
                continue
            if ":::" in ln:
                f, nl = ln.split(":::", 1)
                out.append({"fol": f.strip(), "nl": nl.strip()})
            else:
                n_bad += 1
                out.append({"fol": ln.strip(), "nl": None})
        return out, n_bad
    prem, b1 = lines(prem_part)
    concl, b2 = lines(concl_part)
    return {"decl": decl, "premises": prem, "conclusions": concl, "n_bad_lines": b1 + b2,
            "n_lines": len(prem) + len(concl)}


def split_sents(t: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+(?=[A-Z])", t.strip()) if s.strip()]


# ------------------------------------------------------------------ strata
def strata(text: str, ref: str | None) -> dict:
    from .labeller.fol import parse
    from .labeller.labeller import ast_depth, n_conditions, n_quantifiers
    w = len(text.split())
    st = {"words": w, "words_bin": "<12" if w < 12 else ("12-19" if w < 20 else ">=20")}
    m = EXC_RE.search(text)
    st["exception"] = bool(m)
    st["exception_marker"] = m.group(1).lower() if m else None
    try:
        e = parse(ref)
        st.update(n_quant=n_quantifiers(e), depth=ast_depth(e), n_cond=n_conditions(e))
    except Exception:  # noqa: BLE001
        st.update(n_quant=None, depth=None, n_cond=None)
    nq, nc = st["n_quant"], st["n_cond"]
    st["n_quant_bin"] = None if nq is None else ("0-1" if nq <= 1 else ("2" if nq == 2 else ">=3"))
    st["n_cond_bin"] = None if nc is None else ("0" if nc == 0 else ("1-2" if nc <= 2 else ">=3"))
    d = st["depth"]
    st["depth_bin"] = None if d is None else ("<=3" if d <= 3 else ("4-5" if d <= 5 else ">=6"))
    return st


def census_class(eq: dict) -> str | None:
    if eq["cls"] == "ERROR":
        return "+".join(eq["ops"])
    if eq["cls"] in ("COMPOUND", "TIMEOUT_UNKNOWN"):
        return "COMPOUND"
    return None


def map_label_L(eq: dict) -> str:
    c = eq["cls"]
    if c in ("EQUIV", "VOCAB", "GRAN"):
        return "CORRECT"
    if c == "ERROR":
        return "ERROR"
    if c in ("COMPOUND", "TIMEOUT_UNKNOWN"):
        return "UNCERTAIN"
    return "UNPARSEABLE"


# ------------------------------------------------------------------ build
def build_screen(workers: int = 6) -> list[dict]:
    log = {"started": time.time()}
    folio = read_jsonl(SRC_DATA / "DSAVlab-UNIUD_FOLIO_validation-curated__FOLIO_instances.jsonl")
    malls = read_jsonl(SRC_DATA / "DSAVlab-UNIUD_MALLS_test_subset-CURATED__MALLS_instances.jsonl")
    malls_full = json.loads((SRC_DATA / "yuan-yang__MALLS-v0__MALLS-v0.1-test.json").read_text())
    refined = list(csv.DictReader(open(SRC_DATA / "folio_refined_validation.csv", encoding="utf-8")))
    concl = [r for r in folio if str(r["id"]).startswith("concl_")]
    stories = {str(r["id"]).split("_", 1)[1]: r for r in folio if str(r["id"]).startswith("story_")}
    logger.info(f"curated FOLIO: {len(concl)} conclusions, {len(stories)} stories; MALLS curated {len(malls)}; "
                f"MALLS-v0.1-test {len(malls_full)}; folio-refined rows {len(refined)}")

    # sanity: curated MALLS FOL_sentence_old == public MALLS-v0.1-test gold for the same NL
    mf = {norm(m["NL"]): m["FOL"] for m in malls_full}
    same = sum(1 for r in malls if mf.get(norm(r["NL_sentence"]), "").strip() == r["FOL_sentence_old"].strip())
    found = sum(1 for r in malls if norm(r["NL_sentence"]) in mf)
    log["malls_curated_vs_public"] = {"nl_found_in_public_test": found, "old_gold_identical_to_public": same, "n": len(malls)}
    logger.info(f"MALLS curated vs public test: NL found {found}/100, old gold identical {same}/100")

    # --- curated conclusions by norm text
    concl_by_norm = defaultdict(list)
    for r in concl:
        concl_by_norm[norm(r["NL_sentence"])].append(r)

    # --- premise pool: curated story sentence i <-> FOL_sentence_old line i (count-aligned only)
    story_mis = []
    pool = {}  # norm(sentence) -> {text, orig, story}
    for sid, r in stories.items():
        sents = split_sents(r["NL_sentence"])
        fols = [x.strip() for x in r["FOL_sentence_old"].strip().split("\n") if x.strip()]
        if len(sents) != len(fols):
            story_mis.append({"story": sid, "n_sents": len(sents), "n_fol": len(fols)})
            continue
        for s, f in zip(sents, fols):
            pool.setdefault(norm(s), {"text": s, "orig": f, "story": sid})
    log["story_count_mismatch"] = story_mis
    refined_line = {}
    for row in refined:
        nls = [x.strip() for x in row["nl premises"].strip().split("\n")]
        fls = [x.strip() for x in row["fol premises"].strip().split("\n")]
        if len(nls) == len(fls):
            for a, b in zip(nls, fls):
                if a:
                    refined_line.setdefault(norm(a), b)
    agree_pairs = {k: (v["orig"], refined_line[k]) for k, v in pool.items() if k in refined_line}
    logger.info(f"premise pool {len(pool)} sentences ({len(story_mis)} stories count-mismatched); "
                f"with folio-refined line: {len(agree_pairs)}; checking agreement (z3 modulo vocab)")
    agree = label_many(agree_pairs, workers=workers, do_search=False)
    agreed = {k: pool[k] for k, r in agree.items() if r["cls"] in ("EQUIV", "VOCAB", "GRAN")}
    log["premise_pool"] = {"n_pool": len(pool), "n_with_refined": len(agree_pairs), "n_agreed": len(agreed),
                           "agree_cls": dict(Counter(r["cls"] for r in agree.values()))}
    logger.info(f"agreed premises: {len(agreed)} / {len(agree_pairs)}  {log['premise_pool']['agree_cls']}")

    # --- Logic-LM
    raw_items = []
    sys_stats = {}
    for sysn in SYSTEMS:
        progs = json.loads((DATA / "logiclm" / f"FOLIO_dev_{sysn}.json").read_text())
        st = Counter()
        for ex in progs:
            prog = parse_program((ex.get("raw_logic_programs") or [""])[0])
            q_stmt = Q_PREFIX.sub("", ex.get("question", "")).strip()
            st["programs"] += 1
            if prog is None:
                st["malformed_programs"] += 1
                # conclusion still scoreable as UNPARSEABLE if its text matches
                cands = concl_by_norm.get(norm(q_stmt), [])
                if cands:
                    raw_items.append({"system": sysn, "story_id": ex["id"], "role": "conclusion", "cand": None,
                                      "curated": cands, "q_stmt": q_stmt, "prog": None, "ctx": ex.get("context", "")})
                continue
            st["lines"] += prog["n_lines"]
            st["bad_lines"] += prog["n_bad_lines"]
            # conclusion(s)
            for cl in prog["conclusions"][:1]:
                keys = [norm(q_stmt)] + ([norm(cl["nl"])] if cl["nl"] else [])
                cands = next((concl_by_norm[k] for k in keys if k in concl_by_norm), [])
                if cands:
                    raw_items.append({"system": sysn, "story_id": ex["id"], "role": "conclusion", "cand": cl["fol"],
                                      "curated": cands, "q_stmt": q_stmt, "prog": prog, "ctx": ex.get("context", "")})
                    st["concl_matched"] += 1
            # premises
            ctx_sents = split_sents(ex.get("context", ""))
            for i, pl in enumerate(prog["premises"]):
                k = norm(pl["nl"]) if pl["nl"] else None
                route = None
                if k and k in agreed:
                    route = "gloss"
                elif len(ctx_sents) == len(prog["premises"]) and norm(ctx_sents[i]) in agreed:
                    k, route = norm(ctx_sents[i]), "context_index"
                if route:
                    raw_items.append({"system": sysn, "story_id": ex["id"], "role": "premise", "cand": pl["fol"],
                                      "agreed_key": k, "route": route, "prog": prog, "prem_idx": i,
                                      "ctx": ex.get("context", "")})
                    st[f"prem_matched_{route}"] += 1
        sys_stats[sysn] = dict(st)
        logger.info(f"{sysn}: {dict(st)}")
    log["logiclm_parse_stats"] = sys_stats

    # --- resolve conclusion references (disambiguate duplicates by story-text overlap)
    def _overlap(a, b):
        A, B = set(norm(a).split()), set(norm(b).split())
        return len(A & B) / max(1, len(A | B))
    items, pairs = [], {}
    for it in raw_items:
        if it["role"] == "conclusion":
            cands = it["curated"]
            if len(cands) > 1 and len({c["FOL_sentence"] for c in cands}) > 1:
                sid_of = lambda c: str(c["id"]).split("_")[1]
                cands = sorted(cands, key=lambda c: -_overlap(stories.get(sid_of(c), {}).get("NL_sentence", ""), it["ctx"]))
            c = cands[0]
            text, ref, ref_type = c["NL_sentence"], c["FOL_sentence"], "corrected_conclusion"
            extra = {"curated_id": c["id"], "ambiguity": bool(c.get("ambiguity")), "folio_answer": c.get("label"),
                     "orig_gold": c.get("FOL_sentence_old")}
        else:
            p = agreed[it["agreed_key"]]
            text, ref, ref_type = p["text"], p["orig"], "agreed_premise"
            extra = {"curated_id": f"story_{p['story']}", "ambiguity": None, "folio_answer": None, "match_route": it["route"],
                     "orig_gold": p["orig"]}
        prog = it["prog"]
        if prog is not None:
            prem = [x["fol"] for j, x in enumerate(prog["premises"]) if not (it["role"] == "premise" and j == it["prem_idx"])]
            decl = prog["decl"]
        else:
            prem, decl = [], []
        rec = {"item_id": item_id(it["system"], text, it["cand"]), "track": "L", "system": it["system"],
               "story_id": it["story_id"], "role": it["role"], "text": text, "candidate_fol": it["cand"],
               "reference_fol": ref, "ref_type": ref_type, "story_premises_fol": prem, "declared_predicates": decl, **extra}
        items.append(rec)
        pairs[rec["item_id"]] = (it["cand"], ref)

    # --- track H
    for c in concl:
        sid = str(c["id"]).split("_")[1]
        st_r = stories.get(sid)
        prem = [x.strip() for x in st_r["FOL_sentence_old"].strip().split("\n") if x.strip()] if st_r else []
        rec = {"item_id": item_id("human_original", c["NL_sentence"], c["FOL_sentence_old"]), "track": "H",
               "system": "human_original", "sub_source": "FOLIO-concl", "story_id": f"story_{sid}", "role": "conclusion",
               "text": c["NL_sentence"], "candidate_fol": c["FOL_sentence_old"], "reference_fol": c["FOL_sentence"],
               "ref_type": "corrected_conclusion", "story_premises_fol": prem, "declared_predicates": [],
               "curated_id": c["id"], "ambiguity": bool(c.get("ambiguity")), "folio_answer": c.get("label"),
               "orig_gold": c["FOL_sentence_old"], "curator_corrected": c.get("corrected")}
        items.append(rec)
        pairs[rec["item_id"]] = (c["FOL_sentence_old"], c["FOL_sentence"])
    for r in malls:
        rec = {"item_id": item_id("human_original", r["NL_sentence"], r["FOL_sentence_old"]), "track": "H",
               "system": "human_original", "sub_source": "MALLS", "story_id": None, "role": "sentence",
               "text": r["NL_sentence"], "candidate_fol": r["FOL_sentence_old"], "reference_fol": r["FOL_sentence_new"],
               "ref_type": "corrected_malls", "story_premises_fol": [], "declared_predicates": [],
               "curated_id": f"malls_{r['id']}", "ambiguity": bool(r.get("ambiguity")), "folio_answer": None,
               "orig_gold": r["FOL_sentence_old"], "curator_corrected": r.get("corrected")}
        items.append(rec)
        pairs[rec["item_id"]] = (r["FOL_sentence_old"], r["FOL_sentence_new"])

    # --- dedupe by item_id (same system + text + candidate)
    seen, dedup, dups = set(), [], 0
    for rec in items:
        if rec["item_id"] in seen:
            dups += 1
            continue
        seen.add(rec["item_id"])
        dedup.append(rec)
    items = dedup
    log["duplicates_removed"] = dups
    logger.info(f"screen items before labelling: {len(items)} (dups removed {dups}); labelling with {workers} workers")

    # --- label (cache identical (cand, ref) pairs)
    uniq = {}
    for rec in items:
        uniq.setdefault(sha1(f"{rec['candidate_fol']}||{rec['reference_fol']}"), (rec["candidate_fol"], rec["reference_fol"]))
    t0 = time.time()
    res = label_many(uniq, workers=workers, do_search=True)
    log["label_seconds"] = round(time.time() - t0, 1)
    out, ref_bad = [], 0
    for rec in items:
        eq = res[sha1(f"{rec['candidate_fol']}||{rec['reference_fol']}")]
        if eq["cls"] == "REF_UNPARSEABLE":
            ref_bad += 1
            continue
        lab = map_label_L(eq)
        rec["correct_vocab"] = eq["cls"] in ("VOCAB", "GRAN")
        if rec["track"] == "H" and rec.get("ambiguity") and eq["cls"] in ("ERROR", "COMPOUND", "TIMEOUT_UNKNOWN"):
            lab = "READING_CHOICE"
        rec.update(label=lab, auto_class=eq["cls"], repair_ops=eq.get("ops"), vocab_borderline=bool(eq.get("borderline", False)),
                   census_class=census_class(eq), label_detail={k: v for k, v in eq.items() if k not in ("cls", "ops")})
        # substitution-only repair (ADD+DROP of an unaligned predicate): likely vocabulary mismatch, flagged for sensitivity
        rec["subst_only"] = bool(eq["cls"] == "ERROR" and sorted(eq["ops"]) == ["ADD", "DROP"])
        # track-H curator-certified view: COMPOUND counts as ERROR (curators corrected a non-vocab-equivalent formula)
        if rec["track"] == "H":
            rec["label_h_curator"] = ("ERROR" if lab == "UNCERTAIN" else lab)
        rec["strata"] = strata(rec["text"], rec["reference_fol"])
        out.append(rec)
    log["ref_unparseable_dropped"] = ref_bad
    out.sort(key=lambda r: r["item_id"])
    L = [r for r in out if r["track"] == "L"]
    log["n_items"] = {"L": len(L), "H": len(out) - len(L)}
    log["n_distinct_conclusions_matched"] = len({r["curated_id"] for r in L if r["role"] == "conclusion"})
    log["n_distinct_premises_matched"] = len({norm(r["text"]) for r in L if r["role"] == "premise"})
    log["conclusion_match_rate"] = round(log["n_distinct_conclusions_matched"] / len(concl), 3)
    log["premise_match_routes"] = dict(Counter(r.get("match_route") for r in L if r["role"] == "premise"))
    log["label_dist"] = {f"{t}|{s}": dict(Counter(r["label"] for r in out if r["track"] == t and r["system"] == s))
                         for t, s in sorted({(r["track"], r["system"]) for r in out})}
    log["auto_class_dist"] = {t: dict(Counter(r["auto_class"] for r in out if r["track"] == t)) for t in ("L", "H")}
    log["vocab_borderline"] = {t: sum(r["vocab_borderline"] for r in out if r["track"] == t) for t in ("L", "H")}
    log["subst_only"] = {t: sum(r["subst_only"] for r in out if r["track"] == t) for t in ("L", "H")}
    if log["n_distinct_conclusions_matched"] < 150:
        logger.warning("fewer than 150 distinct conclusions matched: agreed premises are included (they always are)")
    jdump(out, DATA / "screen_items.json")
    lv = "\n".join(f"{r['item_id']}:{r['label']}" for r in out)
    (DATA / "label_vector.sha1").write_text(sha1(lv) + "\n")
    log["label_vector_sha1"] = sha1(lv)
    jdump(log, DATA / "screen_build_log.json")
    logger.info(f"screen: {log['n_items']}  label_dist={log['label_dist']}  sha1={log['label_vector_sha1']}")
    return out
