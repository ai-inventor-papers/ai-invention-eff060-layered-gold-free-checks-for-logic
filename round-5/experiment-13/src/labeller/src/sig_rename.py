#!/usr/bin/env python3
"""Audit (i) inputs: every on-signature SIG row (pure-z3 label CORRECT / ERROR / READING_CHOICE) re-expressed with ALL
symbols consistently renamed (a) to nonce tokens, (b) to WordNet mutual first-sense synonyms of one name token where one
exists (else the name is kept; the renamed share is reported). Uses the z3-labelled canonical form (canon_fol).
-> work/sig_renamed_nonce.jsonl, work/sig_renamed_syn.jsonl"""
from __future__ import annotations

import json
import os
import random
import re

from common import NLTK_DATA, SIG_LABELS, WORK, load_jsonl, setup_logger, sha1

os.environ.setdefault("NLTK_DATA", str(NLTK_DATA))
from fol import parse  # noqa: E402
from freelab import free_consts, to_str  # noqa: E402
from perturb_min import first_sense_synonyms  # noqa: E402
from repair_census_min import atoms  # noqa: E402

logger = setup_logger("sig_rename")
CONS, VOW = "bdfgklmptvz", "aeiou"


def toks(n: str) -> list[str]:
    return re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", n.replace("_", " "))


def nonce(rng, used, upper=True):
    while True:
        w = "".join(rng.choice(CONS) + rng.choice(VOW) for _ in range(2)) + rng.choice(CONS)
        w = w.capitalize() if upper else w
        if w not in used and not re.match(r"^(Un|Non|In|Im|Dis|No|Not|un|non|in|im|dis|no|not)", w):
            used.add(w)
            return w


def syn_name(name: str, upper: bool) -> str:
    tk = toks(re.sub(r"_\d+$", "", name))
    for i, t in enumerate(tk):
        if len(t) < 4 or not t.isalpha():
            continue
        for s in sorted(first_sense_synonyms(t.lower())):
            if s.isalpha() and len(s) >= 3 and s != t.lower():
                nt = tk[:i] + [s.capitalize() if (t[0].isupper()) else s] + tk[i + 1:]
                n = "".join(nt)
                return n[0].upper() + n[1:] if upper else n[0].lower() + n[1:]
    return name


def rename(e, pmap, cmap, bv=frozenset()):
    k = e[0]
    if k == "atom":
        return ("atom", pmap.get(e[1], e[1]), tuple(a if a in bv else cmap.get(a, a) for a in e[2]))
    if k in ("all", "ex"):
        return (k, e[1], rename(e[2], pmap, cmap, bv | {e[1]}))
    if k == "not":
        return ("not", rename(e[1], pmap, cmap, bv))
    return (k, rename(e[1], pmap, cmap, bv), rename(e[2], pmap, cmap, bv))


def main() -> None:
    rows = [r for r in load_jsonl(SIG_LABELS) if r["label"] in ("CORRECT", "ERROR", "READING_CHOICE")
            and r["sig_status"] == "ON_SIGNATURE"]
    logger.info(f"SIG rows for replay: {len(rows)}")
    for mode in ("nonce", "syn"):
        out, n_ren, n_sym = [], 0, 0
        for r in rows:
            e = parse(r["canon_fol"])
            names = sorted({a[1] for a in atoms(e)})
            consts = sorted(free_consts(e))
            rng = random.Random(int(sha1(r["sentence_id"] + mode), 16))  # same sentence -> same renaming across slots
            used = set()
            if mode == "nonce":
                pmap = {n: nonce(rng, used) for n in names}
                cmap = {c: nonce(rng, used, upper=False) for c in consts}
            else:
                pmap = {n: syn_name(n, True) for n in names}
                cmap = {c: syn_name(c, False) for c in consts}
                if len(set(pmap.values())) < len(pmap) or len(set(cmap.values())) < len(cmap):
                    pmap = {n: n for n in names}  # collision guard: keep names
                    cmap = {c: c for c in consts}
            n_sym += len(pmap) + len(cmap)
            n_ren += sum(k != v for k, v in list(pmap.items()) + list(cmap.items()))
            out.append({"row_key": r["row_key"], "sentence_id": r["sentence_id"], "slot": r["slot"],
                        "template_id": r["template_id"], "sig_label": r["label"], "matched_reading": r["matched_reading"],
                        "canon_fol": r["canon_fol"], "renamed_fol": to_str(rename(e, pmap, cmap)),
                        "rename_map": {**pmap, **{f"const:{k}": v for k, v in cmap.items()}}})
        with (WORK / f"sig_renamed_{mode}.jsonl").open("w") as fh:
            for o in out:
                fh.write(json.dumps(o, ensure_ascii=False) + "\n")
        logger.info(f"{mode}: {len(out)} rows, symbols renamed {n_ren}/{n_sym} ({n_ren / max(n_sym, 1):.2%})")


if __name__ == "__main__":
    main()
