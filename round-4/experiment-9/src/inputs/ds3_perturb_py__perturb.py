#!/usr/bin/env python3
"""STEP 9: typed-perturbation suite (PERTURB) + meaning-preserving controls (PERTURB_CONTROL). $0, z3 only.

Bases (sha1 order): E heldout GOLD_PANEL_OK + TRUSTED_AGREED (131), then PANEL_REPAIRED up to 200
(base_trust=panel_repaired), then the first 100 R_COMP main sentences (weak reading as base; accepted readings weak +
strong; mutants must also be non-equivalent to the stored only-if converse).
Mutants: repair_census.edits(base, donor) used FORWARD (donor = a sha1-chosen base of a different source with no
shared predicate: supplies ADD_FOREIGN atoms and BIND constants) via edits_tracked(), a path-tracking mirror of
edits() (tests/test_perturb.py asserts identical output), plus two own operators:
  ADD_INTERNAL   conjoin an existing atom of the base at a new restrictor / consequent position
  MEANING_RENAME replace ALL occurrences of one predicate by a same-arity donor predicate whose name tokens are
                 not WordNet synonyms of the original's tokens.
position_polarity: atom-level edits (SWAP, BIND, MEANING_RENAME) -> fol.profile(base)[pred] (semantic_profile);
structural edits -> syntactic polarity of the edited node path (flipped by ¬ and implication antecedents; ↔/⊕ give
NONMONO) (syntactic_path). For each (base, op[/ADD subtype], polarity in {DOWN, UP}) the first VALID mutant in
sha1(string) order is kept: emit->parse round-trips; z3 non-equivalent (3 s) to the base and every accepted reading
(UNKNOWN discarded); non-trivial if the base is; not a duplicate. matched_pair_id links DOWN and UP of base x op.
Controls (z3-verified EQUIVALENT): RENAME (RENAME_SYN / RENAME_NONCE, equivalent under the known inverse map),
REORDER (commute an ∧/∨ pair or swap same-type adjacent quantifiers), CONTRAPOSITIVE (DEMORGAN without implication).
"""
from __future__ import annotations

import itertools
import json
import multiprocessing as mp
import random
import re
from collections import Counter
from concurrent.futures import ProcessPoolExecutor

from common import E_DIR, W, dump, sha1, setup_logger

CAP_ROWS = 6000
BIN = ("and", "or", "imp", "iff", "xor")


# ---------------------------------------------------------------- path-tracked mirror of repair_census.edits
def edits_tracked(e, target):
    """Yield (label, subtype, path, candidate) for exactly the edits repair_census.edits(e, target) yields."""
    from repair_census import atoms, symbols, subterms, replace, parent_kind, unglue
    tgt_atoms = atoms(target)
    Pe, _ = symbols(e)
    _, Ct = symbols(target)
    new_atoms = [a for a in tgt_atoms if (a[1], len(a[2])) not in Pe]
    for path, node, scope in list(subterms(e)):
        k = node[0]
        if k == "not":
            yield "NEG", "NEG_REMOVE", path, replace(e, path, node[1])
        else:
            yield "NEG", "NEG_INSERT", path, replace(e, path, ("not", node))
        if k in ("all", "ex"):
            yield "QUANT", "QUANT_FLIP", path, replace(e, path, ("ex" if k == "all" else "all", node[1], node[2]))
            vs, body = [], node
            while body[0] == k:
                vs.append(body[1]); body = body[2]
            if body[0] in ("imp", "and"):
                nb = ("and" if body[0] == "imp" else "imp", body[1], body[2])
                q = "ex" if k == "all" else "all"
                for v in reversed(vs):
                    nb = (q, v, nb)
                yield "QUANT", "QUANT_BLOCK_RESTRICTOR", path, replace(e, path, nb)
            if node[2][0] in ("all", "ex"):
                inner = node[2]
                yield "SCOPE", "SCOPE", path, replace(e, path, (inner[0], inner[1], (k, node[1], inner[2])))
            ug = unglue(node) if k == "all" else None
            if ug is not None:
                yield "UNGLUE", "UNGLUE", path, replace(e, path, ug)
        if k in ("imp", "iff") and node[1][0] == "and":
            yield "MOVE", "MOVE_OUT_LEFT", path, replace(e, path, ("imp", node[1][1], (k, node[1][2], node[2])))
            yield "MOVE", "MOVE_OUT_RIGHT", path, replace(e, path, ("imp", node[1][2], (k, node[1][1], node[2])))
        if k == "imp" and node[2][0] == "imp":
            yield "MOVE", "MOVE_EXCHANGE", path, replace(e, path, ("imp", ("and", node[1], node[2][2]), node[2][1]))
        if k in BIN:
            if k == "imp":
                yield "REV", "REV", path, replace(e, path, ("imp", node[2], node[1]))
            for op in BIN:
                if op != k:
                    lab = "RESTR" if {k, op} == {"imp", "and"} and parent_kind(e, path) in ("all", "ex") else "CONN"
                    yield lab, f"{lab}_{k}_to_{op}", path, replace(e, path, (op, node[1], node[2]))
            if k in ("and", "or"):
                yield "DROP", "DROP_RIGHT", path, replace(e, path, node[1])
                yield "DROP", "DROP_LEFT", path, replace(e, path, node[2])
        if k == "atom":
            args = node[2]
            if len(args) >= 2:
                for perm in set(itertools.permutations(args)):
                    if perm != args:
                        yield "SWAP", "SWAP", path, replace(e, path, ("atom", node[1], perm))
            pool = set(scope) | Ct
            for i, a in enumerate(args):
                for b in pool:
                    if b != a:
                        yield "BIND", ("BIND_VAR" if b in scope else "BIND_CONST"), path, \
                            replace(e, path, ("atom", node[1], args[:i] + (b,) + args[i + 1:]))
        for a in new_atoms:
            sc = list(scope)
            opts = []
            for x in a[2]:
                opts.append([x] if (x in Ct or x in sc) else (sc or [x]))
            for combo in itertools.islice(itertools.product(*opts), 6):
                yield "ADD", "ADD_FOREIGN", path, replace(e, path, ("and", node, ("atom", a[1], tuple(combo))))


SYM = {"and": "∧", "or": "∨", "imp": "→", "iff": "↔", "xor": "⊕"}
PREC = {"iff": 1, "imp": 2, "xor": 3, "or": 3, "and": 4}


def emit_min(e) -> str:
    """Unicode FOL with minimal parentheses under fol.py's grammar (↔ < → < ∨/⊕ < ∧, ∧/∨/⊕/↔ left-assoc,
    → right-assoc; a quantifier binds the next group/atom/¬/quantifier). parse(emit_min(e)) == e is checked by callers."""
    k = e[0]
    if k == "atom":
        return f"{e[1]}({', '.join(e[2])})" if e[2] else e[1]
    if k in ("all", "ex"):
        q = "∀" if k == "all" else "∃"
        b = e[2]
        inner = emit_min(b)
        return f"{q}{e[1]} {inner}" if b[0] in ("atom", "not", "all", "ex") else f"{q}{e[1]} ({inner})"
    if k == "not":
        b = e[1]
        return f"¬{emit_min(b)}" if b[0] in ("atom", "not", "all", "ex") else f"¬({emit_min(b)})"
    p = PREC[k]

    def side(c, right):
        s_ = emit_min(c)
        if c[0] in PREC:
            pc = PREC[c[0]]
            need = pc < p or (pc == p and (right if k != "imp" else not right))
            return f"({s_})" if need else s_
        if c[0] in ("all", "ex") and not right:
            return s_  # a quantifier binds only its own group
        return s_
    return f"{side(e[1], False)} {SYM[k]} {side(e[2], True)}"


def free_vars(e, bound=frozenset()) -> set:
    """Variable-looking arguments (x, y, z1 ...) not bound by an enclosing quantifier (ill-formed FOL)."""
    k = e[0]
    if k == "atom":
        return {a for a in e[2] if re.fullmatch(r"[a-z][0-9]*", a) and a not in bound}
    if k in ("all", "ex"):
        return free_vars(e[2], bound | {e[1]})
    if k == "not":
        return free_vars(e[1], bound)
    return free_vars(e[1], bound) | free_vars(e[2], bound)


def syn_polarity(e, path) -> str:
    """Syntactic polarity of the node at `path`: ¬ flips, implication antecedent flips, ↔/⊕ -> NONMONO."""
    pol, x = 1, e
    for i in path:
        k = x[0]
        if k == "not":
            pol = -pol
        elif k == "imp" and i == 1:
            pol = -pol
        elif k in ("iff", "xor"):
            return "NONMONO"
        x = x[i]
    return "UP" if pol > 0 else "DOWN"


def add_internal(e):
    """Own ADD_INTERNAL: conjoin an existing atom of e (args re-bound to in-scope vars) at a restrictor / consequent
    position (a node directly under an implication side or inside a conjunction there) where it is not yet present."""
    from repair_census import atoms, subterms, replace
    base_atoms = sorted({a for a in atoms(e)}, key=str)
    for path, node, scope in list(subterms(e)):
        if not path:
            continue
        # restrictor / consequent positions: the two sides of an implication, and conjuncts on those sides
        par = e
        for i in path[:-1]:
            par = par[i]
        if par[0] not in ("imp", "and"):
            continue
        present = {str(a) for a in atoms(node)}
        for a in base_atoms:
            args = tuple(x if (x in scope or not re.fullmatch(r"[a-z][0-9]*", x)) else None for x in a[2])
            if None in args:
                continue
            na = ("atom", a[1], args)
            if str(na) in present:
                continue
            yield "ADD", "ADD_INTERNAL", path, replace(e, path, ("and", node, na))


def name_tokens(n):
    return [t.lower() for t in re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", n.replace("_", " "))]


def wn_synonyms(tok: str) -> set:
    from nltk.corpus import wordnet as wn
    out = set()
    for s in wn.synsets(tok)[:8]:
        out |= {l.lower() for l in s.lemma_names()}
    return out


def meaning_rename(e, donor):
    """Own MEANING_RENAME: all occurrences of one base predicate -> a same-arity donor predicate whose name tokens are
    not WordNet synonyms of the original's tokens (and not already in the base)."""
    from repair_census import symbols, rename
    Pe, _ = symbols(e)
    Pd, _ = symbols(donor)
    names_e = {p[0] for p in Pe}
    for p in sorted(Pe):
        tp = set(name_tokens(p[0]))
        syn = set().union(*[wn_synonyms(t) for t in tp]) if tp else set()
        for q in sorted(Pd):
            if q[1] != p[1] or q[0] in names_e:
                continue
            tq = set(name_tokens(q[0]))
            if tq & (tp | syn):
                continue
            yield "MEANING_RENAME", "MEANING_RENAME", p, rename(e, {p: q[0]}, {})


# ---------------------------------------------------------------- controls
def first_sense_synonyms(tok: str) -> set:
    """Mutual first-sense WordNet synonyms: s is in tok's first synset AND tok is in s's first synset
    (guards against wrong-sense swaps such as steal -> bargain)."""
    from nltk.corpus import wordnet as wn
    ss_ = wn.synsets(tok)
    if not ss_ or ss_[0].pos() != "n" or wn.synsets(tok, pos="v") or wn.synsets(tok, pos="a"):
        return set()  # nouns only: verb/adjective senses make wrong-sense swaps likely
    out = set()
    for lem in ss_[0].lemma_names():
        l = lem.lower()
        if l == tok:
            continue
        s2 = wn.synsets(l)
        if s2 and tok in {x.lower() for x in s2[0].lemma_names()}:
            out.add(l)
    return out


CONS, VOW = "bdfgklmnprtvz", "aeiou"


def control_rename(e, seed: str):
    """RENAME_SYN: one predicate token -> a WordNet synonym (single word, not already a token); else RENAME_NONCE."""
    from repair_census import symbols, rename
    Pe, _ = symbols(e)
    names = {p[0] for p in Pe}
    for p in sorted(Pe, key=lambda p: sha1(seed + p[0])):
        toks = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", p[0])
        for i, t in enumerate(toks):
            if len(t) < 4 or not t.isalpha():
                continue
            for s in sorted(first_sense_synonyms(t.lower())):
                if "_" in s or "-" in s or s == t.lower() or not s.isalpha() or len(s) < 3:
                    continue
                nt = toks[:i] + [s.capitalize() if t[0].isupper() else s] + toks[i + 1:]
                nn = "".join(nt)
                if nn not in names and nn != p[0]:
                    return "RENAME_SYN", {p: nn}, rename(e, {p: nn}, {})
    rng = random.Random(int(sha1(seed), 16))
    p = sorted(Pe, key=lambda p: sha1(seed + p[0]))[0]
    while True:
        w = "".join(rng.choice(CONS) + rng.choice(VOW) for _ in range(2)) + rng.choice(CONS)
        nn = w.capitalize()
        if nn not in names:
            break
    return "RENAME_NONCE", {p: nn}, rename(e, {p: nn}, {})


def control_reorder(e):
    from repair_census import subterms, replace
    for path, node, _ in subterms(e):
        if node[0] in ("and", "or") and node[1] != node[2]:
            return "REORDER_COMMUTE", replace(e, path, (node[0], node[2], node[1]))
        if node[0] in ("all", "ex") and node[2][0] == node[0] and node[1] != node[2][1]:
            inner = node[2]
            return "REORDER_QUANT", replace(e, path, (node[0], inner[1], (node[0], node[1], inner[2])))
    return None, None


def neg(x):
    return x[1] if x[0] == "not" else ("not", x)


def control_contra(e):
    from repair_census import subterms, replace
    for path, node, _ in subterms(e):
        if node[0] == "imp":
            return "CONTRAPOSITIVE", replace(e, path, ("imp", neg(node[2]), neg(node[1])))
    for path, node, _ in subterms(e):
        if node[0] in ("and", "or"):
            dual = "or" if node[0] == "and" else "and"
            return "DEMORGAN", replace(e, path, ("not", (dual, neg(node[1]), neg(node[2]))))
    return None, None


# ---------------------------------------------------------------- per-base worker
def work(job: dict) -> dict:
    import common  # noqa: F401 - sys.path in spawned worker
    import z3
    from fol import parse, profile, equivalent, preds, mkpred, to_z3, valid
    from repair_census import rename
    emit = emit_min
    base = parse(job["base_fol"])
    base_free = free_vars(base)
    donor = parse(job["donor_fol"])
    readings = [parse(f) for f in job["accepted_readings"]] + [parse(f) for f in job.get("also_nonequiv", [])]
    prof = profile(base)

    def trivial(x):
        P = {q: mkpred(q, m) for q, m in preds(x).items()}
        z = to_z3(x, {}, P)
        return valid(z) is True or valid(z3.Not(z)) is True
    base_trivial = trivial(base)
    log = Counter()
    groups = {}
    gen = itertools.chain(edits_tracked(base, donor), add_internal(base), meaning_rename(base, donor))
    for lab, sub, loc, cand in gen:
        if lab == "MEANING_RENAME":
            pol, meth, pred = prof.get(f"{loc[0]}/{loc[1]}", "UNKNOWN"), "semantic_profile", f"{loc[0]}/{loc[1]}"
        elif lab in ("SWAP", "BIND"):
            x = base
            for i in loc:
                x = x[i]
            pred = f"{x[1]}/{len(x[2])}"
            pol, meth = prof.get(pred, "UNKNOWN"), "semantic_profile"
        else:
            pol, meth, pred = syn_polarity(base, loc), "syntactic_path", None
        if pol not in ("UP", "DOWN"):
            log[f"skip_polarity_{pol}"] += 1
            continue
        key = ("ADD_INTERNAL" if sub == "ADD_INTERNAL" else lab, pol)
        try:
            s = emit(cand)
        except (IndexError, TypeError):
            continue
        groups.setdefault(key, {})[s] = (lab, sub, loc, cand, meth, pred)
    rows = []
    seen = {emit(base)}
    for (opkey, pol), cands in sorted(groups.items()):
        found = None
        for s in sorted(cands, key=sha1):
            lab, sub, loc, cand, meth, pred = cands[s]
            log["tested"] += 1
            if s in seen:
                log["dup"] += 1; continue
            try:
                rt = parse(s)
            except Exception:  # noqa: BLE001 - emit/parse round trip guard
                log["roundtrip_fail"] += 1; continue
            if rt != cand:
                log["roundtrip_mismatch"] += 1; continue
            if free_vars(cand) - base_free:
                log["free_variable"] += 1; continue
            eqs = [equivalent(cand, r, ms=3000) for r in [base] + readings]
            if any(q is None for q in eqs):
                log["unknown"] += 1; continue
            if any(q is True for q in eqs):
                log["equivalent"] += 1; continue
            if not base_trivial and trivial(cand):
                log["trivial"] += 1; continue
            found = (s, lab, sub, loc, meth, pred)
            break
        if found:
            s, lab, sub, loc, meth, pred = found
            seen.add(s)
            rows.append({"candidate_fol": s, "operator": lab, "subtype": sub, "position_polarity": pol,
                         "polarity_method": meth, "edited_path": list(loc) if isinstance(loc, tuple) and all(isinstance(i, int) for i in loc) else None,
                         "edited_predicate": pred, "select_key": opkey})
    # controls
    ctrl = []
    kind, mp_, c = control_rename(base, job["base_item_id"])
    inv = {(v, k[1]): k[0] for k, v in mp_.items()}
    back = rename(c, inv, {})
    if equivalent(back, base, ms=3000) is True and emit(c) != emit(base):
        ctrl.append({"candidate_fol": emit(c), "control_type": "RENAME", "subtype": kind,
                     "rename_map": {f"{k[0]}/{k[1]}": v for k, v in mp_.items()}, "verified": "EQ_UNDER_INVERSE_MAP"})
    else:
        log["control_rename_fail"] += 1
    for fn, typ in ((control_reorder, "REORDER"), (control_contra, "CONTRAPOSITIVE")):
        kind, c = fn(base)
        if c is None:
            log[f"control_{typ}_na"] += 1; continue
        s = emit(c)
        if s != emit(base) and parse(s) == c and equivalent(c, base, ms=3000) is True:
            ctrl.append({"candidate_fol": s, "control_type": typ, "subtype": kind, "verified": "Z3_EQ"})
        else:
            log[f"control_{typ}_fail"] += 1
    return {"base_item_id": job["base_item_id"], "rows": rows, "controls": ctrl, "log": dict(log),
            "profile": prof, "base_trivial": base_trivial}


def load_bases():
    import select_sentences as ss
    d = json.loads((E_DIR / "full_data_out.json").read_text())
    hs = [g for g in d["datasets"] if g["dataset"] == "heldout_sentences"][0]["examples"]
    tr = sorted([x for x in hs if x["output"] in ("GOLD_PANEL_OK", "TRUSTED_AGREED")], key=lambda x: x["metadata_sentence_id"])
    pr = sorted([x for x in hs if x["output"] == "PANEL_REPAIRED"], key=lambda x: x["metadata_sentence_id"])
    bases = []
    for x in tr + pr[: max(0, 200 - len(tr))]:
        inp = json.loads(x["input"])
        bases.append({"sentence_id": x["metadata_sentence_id"], "text": inp["text"], "base_fol": inp["reference_fol"],
                      "accepted_readings": [], "base_source": "E_" + x["output"], "source_group": x["metadata_source"],
                      "base_trust": "panel_repaired" if x["output"] == "PANEL_REPAIRED" else "trusted",
                      "strata": x["metadata_strata"]})
    rc = json.loads((W / "rcomp_sentences.json").read_text())
    rc = sorted([r for r in rc if r["batch"] == "main"], key=lambda r: r["sentence_id"])[:100]
    for r in rc:
        bases.append({"sentence_id": r["sentence_id"], "text": r["text"], "base_fol": r["reference_fol_weak"],
                      "accepted_readings": [r["reference_fol_strong"]],
                      "also_nonequiv": [r["reading_converse"]] if r.get("reading_converse") else [],
                      "base_source": "RCOMP", "source_group": "RCOMP", "base_trust": "rcomp_by_construction",
                      "template_id": r["template_id"], "lexicon_ids": r["lexicon_ids"],
                      "strata": {"words": r["words"], "n_quant": r["nquant"], "depth": r["depth_weak"],
                                 "n_conditions": r["nconds_weak"], "exception_type": r["exception_type"],
                                 "template_id": r["template_id"], "word_bin": r["word_bin"]}})
    from fol import parse
    from repair_census import symbols
    for b in bases:
        b["base_item_id"] = sha1("PERTURB_BASE|" + ss.norm(b["text"]) + "|" + b["base_fol"])[:16]
        b["_preds"] = {p[0] for p in symbols(parse(b["base_fol"]))[0]}
    for b in bases:  # donor: sha1-first base of a different source group with no shared predicate name
        cands = [o for o in bases if o["source_group"] != b["source_group"] and not (o["_preds"] & b["_preds"])]
        if not cands:
            cands = [o for o in bases if o["sentence_id"] != b["sentence_id"] and not (o["_preds"] & b["_preds"])]
        dn = min(cands, key=lambda o: sha1(b["base_item_id"] + "|" + o["base_item_id"]))
        b["donor_fol"], b["donor_item_id"] = dn["base_fol"], dn["base_item_id"]
    for b in bases:
        b.pop("_preds")
    return bases


def main():
    logger = setup_logger("perturb")
    bases = load_bases()
    logger.info(f"bases {len(bases)} {dict(Counter(b['base_source'] for b in bases))}")
    res = {}
    with ProcessPoolExecutor(max_workers=4, mp_context=mp.get_context("spawn")) as pool:
        futs = {pool.submit(work, b): b["base_item_id"] for b in bases}
        from concurrent.futures import as_completed
        for n, f in enumerate(as_completed(futs), 1):
            bid = futs[f]
            try:
                res[bid] = f.result(timeout=900)
            except Exception as ex:  # noqa: BLE001 - one bad base must not kill the suite
                logger.error(f"base {bid} failed: {type(ex).__name__}: {ex}")
            if n % 25 == 0:
                logger.info(f"{n}/{len(bases)} bases done")
    import select_sentences as ss
    rows, ctrls, log = [], [], Counter()
    for b in bases:
        r = res.get(b["base_item_id"])
        if r is None:
            log["base_failed"] += 1; continue
        for k, v in r["log"].items():
            log[k] += v
        meta = {k: b[k] for k in ("base_item_id", "sentence_id", "text", "base_fol", "accepted_readings", "base_source",
                                  "base_trust", "strata", "donor_item_id")}
        meta["template_id"] = b.get("template_id")
        meta["reading_converse"] = (b.get("also_nonequiv") or [None])[0]
        for m in r["rows"]:
            system = f"PERTURB:{m['operator']}:{m['position_polarity']}"
            if m["subtype"] == "ADD_INTERNAL":
                system = f"PERTURB:ADD_INTERNAL:{m['position_polarity']}"
            m.update(meta)
            m["system"] = system
            m["item_id"] = sha1(system + "|" + ss.norm(b["text"]) + "|" + m["candidate_fol"])[:16]
            m["matched_pair_id"] = sha1(b["base_item_id"] + "|" + m["select_key"])[:12]
            rows.append(m)
        for c in r["controls"]:
            system = f"CONTROL:{c['control_type']}"
            c.update(meta)
            c["system"] = system
            c["item_id"] = sha1(system + "|" + ss.norm(b["text"]) + "|" + c["candidate_fol"])[:16]
            ctrls.append(c)
    pair_n = Counter(m["matched_pair_id"] for m in rows)
    for m in rows:
        m["matched_pair_complete"] = pair_n[m["matched_pair_id"]] == 2
    if len(rows) > CAP_ROWS:  # cap: keep complete pairs first, then sha1 order
        rows.sort(key=lambda m: (not m["matched_pair_complete"], m["item_id"]))
        rows = rows[:CAP_ROWS]
        log["capped"] = 1
    log = dict(log)
    log.update({"bases": len(bases), "mutants": len(rows), "controls": len(ctrls),
                "per_op_pol": {f"{k[0]}:{k[1]}": v for k, v in sorted(Counter((m["select_key"], m["position_polarity"]) for m in rows).items())},
                "complete_pairs": sum(1 for v in pair_n.values() if v == 2),
                "per_control": dict(Counter(c["subtype"] for c in ctrls))})
    dump(W / "perturb_suite.json", rows)
    dump(W / "perturb_controls.json", ctrls)
    dump(W / "perturb_bases.json", bases)
    dump(W / "perturb_log.json", dict(log))
    logger.info(json.dumps(dict(log))[:3000])


if __name__ == "__main__":
    main()
