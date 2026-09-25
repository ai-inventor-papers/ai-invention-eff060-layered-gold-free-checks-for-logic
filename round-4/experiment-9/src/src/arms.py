"""Deterministic, label-blind (except RENAME, which by design uses CORRECT rows) row selection and API job lists per arm.

Every arm maps row_key -> list of peer slots {model, family, key}; jobs are deduplicated by key = sha1(model | messages),
so candidates of one sentence that share a signature share their peer calls (and their cost)."""
from __future__ import annotations

import hashlib
import json
import random
from collections import defaultdict
from pathlib import Path

import csc
import rename as RN

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
STRATA = ("L25", "L20", "EXC", "CTRL")
POOL_FAMS = {m[1] for m in csc.POOL}


def h(s: str) -> str:
    return hashlib.sha1(s.encode()).hexdigest()


def jl(p: Path) -> list[dict]:
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]


def load_frame() -> list[dict]:
    return jl(DATA / "frame_blind.jsonl")


def stratified(rows: list[dict], n: int, tag: str) -> list[dict]:
    """Proportional allocation over source_stratum (largest remainder), sha1(tag|row_key) order within stratum."""
    if n >= len(rows):
        return sorted(rows, key=lambda r: h(tag + "|" + r["row_key"]))
    by = defaultdict(list)
    for r in rows:
        by[r["stratum"]].append(r)
    tot = len(rows)
    quota = {s: n * len(v) / tot for s, v in by.items()}
    alloc = {s: int(q) for s, q in quota.items()}
    rest = n - sum(alloc.values())
    for s in sorted(quota, key=lambda s: -(quota[s] - alloc[s]))[:rest]:
        alloc[s] += 1
    out = []
    for s, v in by.items():
        out += sorted(v, key=lambda r: h(tag + "|" + r["row_key"]))[: alloc[s]]
    return out


def _jobs_for(text: str, sig_items: list[str] | None, models, arm: str, fmt_only: bool = False):
    msgs = csc.build_prompt(text, sig_items, fmt_only=fmt_only)
    slots, jobs = [], []
    for model, fam, extra in models:
        k = csc.prompt_key(model, msgs)
        slots.append({"model": model, "family": fam, "key": k})
        jobs.append({"key": k, "model": model, "extra": extra, "messages": msgs, "tag": arm})
    return slots, jobs


def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if (a | b) else 1.0


def build_arms(frame: list[dict], labels: dict | None = None, sizes: dict | None = None) -> dict:
    """-> {'arms': {arm: {row_key: {...slots, meta}}}, 'jobs': {arm: [job]}, 'selection': {...}}.
    labels (row_key -> y) is used ONLY by RENAME (CORRECT rows)."""
    S = {"OWN": None, "K4": 600, "OTHER": 900, "FMT": 900, "PLACEBO": 100, "RENAME": 400, **(sizes or {})}
    arms, jobs, sel = defaultdict(dict), defaultdict(list), {}
    own_rows = frame if S["OWN"] is None else stratified(frame, S["OWN"], "OWN")
    sig_of = {r["row_key"]: csc.extract_signature(r["candidate_fol"]) for r in frame}
    # ARM1 CSC-OWN (k = 3)
    for r in own_rows:
        sig = sig_of[r["row_key"]]
        items = csc.order_symbols(r["text"], sig)
        slots, jb = _jobs_for(r["text"], items, csc.peers_for(r["family"], 3), "OWN")
        arms["OWN"][r["row_key"]] = {"slots": slots, "sig": csc.canonical_sig(sig), "sig_items": items}
        jobs["OWN"] += jb
    # ARM4 k = 4 for candidates from families outside the pool
    k4 = stratified([r for r in frame if r["family"] not in POOL_FAMS], S["K4"], "K4")
    for r in k4:
        sig = sig_of[r["row_key"]]
        items = csc.order_symbols(r["text"], sig)
        slots, jb = _jobs_for(r["text"], items, csc.peers_for(r["family"], 4), "K4")
        arms["K4"][r["row_key"]] = {"slots": slots, "sig": csc.canonical_sig(sig)}
        jobs["K4"] += jb
    # ARM3 OTHER-SIG (sham vocabulary: the most dissimilar other parseable candidate of the same sentence)
    cands = json.loads((DATA / "sentence_cands.json").read_text())
    other_rows = stratified(frame, S["OTHER"], "OTHER")
    n_nodonor = 0
    for r in other_rows:
        own = {(n, a) for n, a, _ in sig_of[r["row_key"]]}
        best = None
        for c in cands.get(r["sentence_id"], []):
            if c["row_key"] == r["row_key"]:
                continue
            s2 = csc.extract_signature(c["fol"])
            if s2 is None:
                continue
            j = jaccard(own, {(n, a) for n, a, _ in s2})
            if j >= 1.0:
                continue
            key = (j, h(c["row_key"]))
            if best is None or key < best[0]:
                best = (key, c, s2)
        if best is None:
            n_nodonor += 1
            continue
        items = csc.order_symbols(r["text"], best[2])
        slots, jb = _jobs_for(r["text"], items, csc.peers_for(r["family"], 3), "OTHER")
        arms["OTHER"][r["row_key"]] = {"slots": slots, "donor_row_key": best[1]["row_key"], "donor_fol": best[1]["fol"],
                                       "donor_jaccard": best[0][0], "sig": csc.canonical_sig(best[2])}
        jobs["OTHER"] += jb
    sel["OTHER_no_donor"] = n_nodonor
    # ARM7 FORMAT-ONLY (no symbol list, same JSON/alt_fol output instruction; rows: S['FMT'] stratified, default all)
    for r in stratified(frame, S["FMT"], "FMT"):
        slots, jb = _jobs_for(r["text"], None, csc.peers_for(r["family"], 3), "FMT", fmt_only=True)
        arms["FMT"][r["row_key"]] = {"slots": slots}
        jobs["FMT"] += jb
    # PLACEBO: the signature of a random OTHER sentence (seeded)
    sents = sorted({r["sentence_id"] for r in frame})
    first_row = {}
    for r in sorted(frame, key=lambda r: h("PLACEBO_DONOR|" + r["row_key"])):
        first_row.setdefault(r["sentence_id"], r)
    for r in stratified(frame, S["PLACEBO"], "PLACEBO"):
        rng = random.Random(int(h("PLACEBO|" + r["row_key"]), 16))
        sid = r["sentence_id"]
        while sid == r["sentence_id"]:
            sid = rng.choice(sents)
        d = first_row[sid]
        sig = sig_of[d["row_key"]]
        items = csc.order_symbols(r["text"], sig)
        slots, jb = _jobs_for(r["text"], items, csc.peers_for(r["family"], 3), "PLACEBO")
        arms["PLACEBO"][r["row_key"]] = {"slots": slots, "donor_row_key": d["row_key"], "sig": csc.canonical_sig(sig)}
        jobs["PLACEBO"] += jb
    # ARM6 RENAME on R_AB CORRECT rows (SYN = WordNet synonym rename of one predicate; NONCE = E disguise map on the formula)
    if labels is not None:
        cor = [r for r in frame if labels.get(r["row_key"]) == 0]
        rrows = stratified(cor, S["RENAME"], "RENAME")
        n_syn = n_non = 0
        for r in rrows:
            syn = RN.rename_syn(r["candidate_fol"], r["row_key"])
            if syn is not None:
                s2 = csc.extract_signature(syn["fol"])
                items = csc.order_symbols(r["text"], s2)
                slots, jb = _jobs_for(r["text"], items, csc.peers_for(r["family"], 3), "RENAME_SYN")
                arms["RENAME_SYN"][r["row_key"]] = {"slots": slots, "cand_fol": syn["fol"], "map": syn["map"],
                                                    "sig": csc.canonical_sig(s2)}
                jobs["RENAME_SYN"] += jb
                n_syn += 1
            dfol = r.get("disguised_fol")
            s3 = csc.extract_signature(dfol) if dfol else None
            if s3 is not None:
                items = csc.order_symbols(r["text"], s3)
                slots, jb = _jobs_for(r["text"], items, csc.peers_for(r["family"], 3), "RENAME_NONCE")
                arms["RENAME_NONCE"][r["row_key"]] = {"slots": slots, "cand_fol": dfol, "sig": csc.canonical_sig(s3)}
                jobs["RENAME_NONCE"] += jb
                n_non += 1
        sel["RENAME"] = {"n_rows": len(rrows), "n_syn": n_syn, "n_nonce": n_non, "rows": [r["row_key"] for r in rrows]}
    uniq = {a: len({j["key"] for j in js}) for a, js in jobs.items()}
    sel["n_rows"] = {a: len(v) for a, v in arms.items()}
    sel["n_jobs"] = {a: len(js) for a, js in jobs.items()}
    sel["n_unique_keys"] = uniq
    return {"arms": {a: dict(v) for a, v in arms.items()}, "jobs": {a: v for a, v in jobs.items()}, "selection": sel}


def dedupe(jobs: list[dict]) -> list[dict]:
    seen, out = set(), []
    for j in jobs:
        if j["key"] not in seen:
            seen.add(j["key"])
            out.append(j)
    return out
