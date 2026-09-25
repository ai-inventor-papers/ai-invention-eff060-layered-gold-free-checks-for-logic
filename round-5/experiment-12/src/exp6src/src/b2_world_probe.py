"""B2 world_probe: does the SENTENCE agree with the candidate formula on small concrete worlds that separate the formula
from its own typed single-edit mutants?

world_probe(text, fol, item_key, reader) -> {b2_score, b2_mismatch_det, b2_undet_share, n_worlds, worlds, status}

Construction (all label-free and gold-free):
 (i)   parse phi with labeller/fol.py (repair_census tuple AST);
 (ii)  mutants psi = repair_census.edits(phi, phi) restricted to NEG/REV/QUANT/RESTR/CONN/DROP/SWAP/SCOPE (ADD is empty for
       target=phi, BIND explodes), dropping psi with fp(psi)==fp(phi); ordered by sha1(item_key|op|repr(psi)), taken
       round-robin over op types until 6 are z3-verified NON-equivalent to phi (2 s timeout, <= 20 tried);
 (iii) for mutant i, a finite world where phi and psi DISAGREE: i even -> phi TRUE & psi FALSE, i odd -> phi FALSE & psi
       TRUE (fallback: the other direction). Domain = constants + k fresh individuals (k=1..3, |D|<=4; constants+1 if
       >3 constants; cap 6). Quantifiers are expanded over D, ground atoms are z3 Bools, z3 Optimize minimises the number
       of true atoms, smallest satisfiable domain first;
 (iv)  the world is verbalised by a fixed template (no LLM, no logic symbols): individuals, one line per TRUE ground atom
       of phi's predicates, and a closed-world closing line;
 (v)   a text-only reader (never sees a formula) answers TRUE / FALSE / UNDETERMINED for the SENTENCE in each world;
 (vi)  b2_score = (#determined verdicts != phi-truth + 0.5 * #UNDETERMINED) / n_worlds  (higher = more likely unfaithful).
A faithful formula has the sentence's truth conditions, so the reader's verdicts should match phi's truth value in every
world; a formula with a quantifier/negation/direction/dropped-condition error is TRUE (or FALSE) in a world where the
sentence is not.
"""
from __future__ import annotations

import itertools
import json
import re
import time

from .common import sha1

B2_OPS = ["NEG", "REV", "QUANT", "RESTR", "CONN", "DROP", "SWAP", "SCOPE"]
N_MUT, MAX_TRIED, Z3_MS = 6, 20, 2000
MAX_GROUND_ATOMS = 400
CAMEL = re.compile(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+")

READER_V1 = ("Sentence: {text}\n\nBelow are {n} separate situations. For each, answer whether the sentence is TRUE, FALSE, "
             "or UNDETERMINED in that situation (UNDETERMINED only if the situation does not contain enough information). "
             "Treat each situation as the whole world.\n\n{worlds}\n\nReturn JSON {{\"answers\": [..]}} with exactly {n} "
             "answers, in order, each one of \"TRUE\", \"FALSE\", \"UNDETERMINED\".")
READER_V2 = ("Sentence: {text}\n\nBelow are {n} separate situations. For each, answer whether the sentence is TRUE, FALSE, "
             "or UNDETERMINED in that situation (UNDETERMINED only if the situation does not contain enough information). "
             "Treat each situation as the whole world: the listed individuals are the only things that exist, and a property "
             "or relation that is not listed does not hold. Property and relation names are paraphrases of words in the "
             "sentence; read them in the sentence's sense.\n\n{worlds}\n\nReturn JSON {{\"answers\": [..]}} with exactly {n} "
             "answers, in order, each one of \"TRUE\", \"FALSE\", \"UNDETERMINED\".")
READERS = {"v1": READER_V1, "v2": READER_V2}


# ------------------------------------------------------------------ AST helpers
def _consts(e) -> list[str]:
    from .labeller.repair_census import symbols
    _, C = symbols(e)
    return sorted(C)


def _preds(e, acc=None) -> dict:
    acc = {} if acc is None else acc
    k = e[0]
    if k == "atom":
        acc[(e[1], len(e[2]))] = True
    elif k in ("all", "ex"):
        _preds(e[2], acc)
    elif k == "not":
        _preds(e[1], acc)
    else:
        _preds(e[1], acc)
        _preds(e[2], acc)
    return acc


def _free_vars(e, bound=frozenset(), consts=frozenset()) -> set:
    k = e[0]
    if k == "atom":
        return set()
    if k in ("all", "ex"):
        return _free_vars(e[2], bound | {e[1]}, consts)
    if k == "not":
        return _free_vars(e[1], bound, consts)
    return _free_vars(e[1], bound, consts) | _free_vars(e[2], bound, consts)


def mutants(phi, item_key: str) -> list[tuple[str, object]]:
    """Candidate mutants (op, psi), deduplicated, fingerprint-distinct from phi, in round-robin sha1 order."""
    from .labeller.repair_census import edits, fp
    f0 = fp(phi)
    by_op: dict[str, dict[str, object]] = {}
    for op, psi in edits(phi, phi):
        if op not in B2_OPS:
            continue
        s = repr(psi)
        if s in by_op.get(op, {}):
            continue
        try:
            if fp(psi) == f0:
                continue
        except (KeyError, RecursionError):
            continue
        by_op.setdefault(op, {})[s] = psi
    queues = {op: sorted(d.items(), key=lambda kv: sha1(f"{item_key}|{op}|{kv[0]}")) for op, d in by_op.items()}
    op_order = sorted(queues, key=lambda op: sha1(f"{item_key}|{op}"))
    out = []
    while any(queues.values()):
        for op in op_order:
            if queues[op]:
                out.append((op, queues[op].pop(0)[1]))
    return out


# ------------------------------------------------------------------ grounding
def _ground(e, D, env, atoms):
    import z3
    k = e[0]
    if k == "atom":
        args = tuple(env.get(a, a) for a in e[2])
        key = (e[1], args)
        if key not in atoms:
            atoms[key] = z3.Bool(f"{e[1]}|{','.join(args)}")
        return atoms[key]
    if k == "all":
        return z3.And(*[_ground(e[2], D, {**env, e[1]: d}, atoms) for d in D]) if D else z3.BoolVal(True)
    if k == "ex":
        return z3.Or(*[_ground(e[2], D, {**env, e[1]: d}, atoms) for d in D]) if D else z3.BoolVal(False)
    if k == "not":
        return z3.Not(_ground(e[1], D, env, atoms))
    a, b = _ground(e[1], D, env, atoms), _ground(e[2], D, env, atoms)
    return {"and": lambda: z3.And(a, b), "or": lambda: z3.Or(a, b), "imp": lambda: z3.Implies(a, b),
            "iff": lambda: a == b, "xor": lambda: z3.Xor(a, b)}[k]()


def _eval(e, D, env, world: set) -> bool:
    """Independent Python evaluator (used by the unit tests and as a re-check of every z3 world)."""
    k = e[0]
    if k == "atom":
        return (e[1], tuple(env.get(a, a) for a in e[2])) in world
    if k == "all":
        return all(_eval(e[2], D, {**env, e[1]: d}, world) for d in D)
    if k == "ex":
        return any(_eval(e[2], D, {**env, e[1]: d}, world) for d in D)
    if k == "not":
        return not _eval(e[1], D, env, world)
    a, b = _eval(e[1], D, env, world), _eval(e[2], D, env, world)
    return {"and": a and b, "or": a or b, "imp": (not a) or b, "iff": a == b, "xor": a != b}[k]


def domains(consts: list[str]) -> list[list[str]]:
    n = len(consts)
    if n > 5:
        return []
    if n > 3:
        return [consts + ["thing1"]]
    return [consts + [f"thing{i}" for i in range(1, k + 1)] for k in range(1, 4) if n + k <= 4]


def _n_ground_atoms(preds: dict, D) -> int:
    return sum(len(D) ** a for (_, a) in preds)


def find_world(phi, psi, want_phi: bool, D: list[str]):
    """World over D with phi == want_phi and psi == (not want_phi), minimal #true atoms. -> (set(true atoms)) | None | 'timeout'."""
    import z3
    atoms: dict = {}
    gp = _ground(phi, D, {}, atoms)
    gq = _ground(psi, D, {}, atoms)
    # every ground atom of phi's predicates over D exists as a variable (so 'not listed' = false is well-defined)
    for (name, ar) in _preds(phi):
        for args in itertools.product(D, repeat=ar):
            if (name, args) not in atoms:
                atoms[(name, args)] = z3.Bool(f"{name}|{','.join(args)}")
    opt = z3.Optimize()
    opt.set("timeout", Z3_MS)
    opt.add(gp if want_phi else z3.Not(gp))
    opt.add(z3.Not(gq) if want_phi else gq)
    for v in atoms.values():
        opt.add_soft(z3.Not(v))
    r = opt.check()
    if r == z3.unsat:
        return None
    if r != z3.sat:
        return "timeout"
    m = opt.model()
    world = {key for key, v in atoms.items() if z3.is_true(m.eval(v, model_completion=True))}
    return world


# ------------------------------------------------------------------ template verbaliser
def words(name: str) -> str:
    parts = [p for p in re.split(r"[_\-']+", name) if p]
    toks = []
    for p in parts:
        toks += CAMEL.findall(p) or [p]
    return " ".join(t.lower() for t in toks) or name.lower()


def ind_name(x: str) -> str:
    m = re.fullmatch(r"thing(\d+)", x)
    return f"thing {m.group(1)}" if m else words(x)


def verbalise_world(D: list[str], world: set, phi_preds: dict) -> str:
    names = [ind_name(x) for x in D]
    head = f"There are exactly {len(D)} individual{'s' if len(D) != 1 else ''}: " + ", ".join(names) + "."
    lines = [head]
    keep = sorted((a for a in world if (a[0], len(a[1])) in phi_preds), key=lambda a: (a[0], a[1]))
    for name, args in keep:
        if len(args) == 0:
            lines.append(f"{words(name)}: true")
        elif len(args) == 1:
            lines.append(f"{ind_name(args[0])} — {words(name)}: yes")
        else:
            lines.append(f"{words(name)}: holds for ({', '.join(ind_name(a) for a in args)}) in that order")
    if not keep:
        lines.append("(no property or relation holds for anyone)")
    lines.append("Every property or relation not listed as holding is false for these individuals.")
    return "\n".join(lines)


# ------------------------------------------------------------------ world construction (CPU, deterministic)
def build_worlds(fol: str, item_key: str) -> dict:
    """-> {status, worlds:[{mutant_op, direction, phi_truth, world_text, domain_size}], n_mut_tried, n_mutants_nonequiv}."""
    import sys
    sys.setrecursionlimit(10000)
    from .labeller.fol import equivalent, parse
    t0 = time.time()
    try:
        phi = parse(fol)
    except Exception as e:  # noqa: BLE001 - unparseable candidate
        return {"status": "parse_fail", "worlds": [], "why": str(e)[:80]}
    if _free_vars(phi):
        return {"status": "parse_fail", "worlds": [], "why": "free variables"}
    try:
        cands = mutants(phi, item_key)
    except (RecursionError, KeyError, ValueError) as e:
        return {"status": "z3_fail", "worlds": [], "why": f"mutants:{str(e)[:60]}"}
    if not cands:
        return {"status": "no_mutant", "worlds": [], "n_mut_tried": 0}
    consts = _consts(phi)
    doms = domains(consts)
    if not doms:
        return {"status": "z3_fail", "worlds": [], "why": f"{len(consts)} constants > 5"}
    phi_preds = _preds(phi)
    worlds, tried, n_noneq, n_nodir, n_dup = [], 0, 0, 0, 0
    seen_worlds = set()
    for op, psi in cands:
        if len(worlds) >= N_MUT or tried >= MAX_TRIED:
            break
        tried += 1
        try:
            eq = equivalent(phi, psi, Z3_MS)
        except Exception:  # noqa: BLE001
            continue
        if eq is not False:  # equivalent or unknown -> not a usable mutant
            continue
        n_noneq += 1
        i = len(worlds)  # direction alternates over the worlds actually kept -> balanced phi-TRUE / phi-FALSE mix
        pref = [True, False] if i % 2 == 0 else [False, True]
        got, dup = None, False
        for want in pref:
            for D in doms:
                if _n_ground_atoms({**phi_preds, **_preds(psi)}, D) > MAX_GROUND_ATOMS:
                    continue
                w = find_world(phi, psi, want, D)
                if w is None or w == "timeout":
                    continue
                # independent re-check with the Python evaluator
                if _eval(phi, D, {}, w) != want or _eval(psi, D, {}, w) != (not want):
                    continue
                text = verbalise_world(D, w, phi_preds)
                if text in seen_worlds:  # identical situation already asked: try the other direction / next mutant
                    dup = True
                    break
                got = (want, D, w, text)
                break
            if got:
                break
        if not got:
            n_dup += dup
            n_nodir += not dup
            continue
        want, D, w, text = got
        seen_worlds.add(text)
        worlds.append({"mutant_op": op, "direction": "phi_TRUE" if want else "phi_FALSE", "phi_truth": bool(want),
                       "world_text": text, "domain_size": len(D), "mutant": _show(psi)})
    status = "ok" if worlds else ("no_mutant" if n_noneq == 0 else "z3_fail")
    return {"status": status, "worlds": worlds, "n_mut_tried": tried, "n_mutants_nonequiv": n_noneq, "n_no_world": n_nodir, "n_dup_world": n_dup,
            "seconds": round(time.time() - t0, 3)}


SYM = {'and': '∧', 'or': '∨', 'imp': '→', 'iff': '↔', 'xor': '⊕'}


def _show(e) -> str:
    k = e[0]
    if k == "atom":
        return f"{e[1]}({', '.join(e[2])})" if e[2] else e[1]
    if k in ("all", "ex"):
        return f"{'∀' if k == 'all' else '∃'}{e[1]} ({_show(e[2])})"
    if k == "not":
        return f"¬{_show(e[1])}"
    return f"({_show(e[1])} {SYM[k]} {_show(e[2])})"


# ------------------------------------------------------------------ reader prompt + scoring
def reader_prompt(text: str, worlds: list[dict], variant: str = "v1") -> str:
    block = "\n\n".join(f"Situation {i + 1}:\n{w['world_text']}" for i, w in enumerate(worlds))
    return READERS[variant].format(text=text, n=len(worlds), worlds=block)


def parse_answers(raw: str | None, n: int) -> list[str] | None:
    if not raw:
        return None
    t = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip())
    ans = None
    m = re.search(r"\{.*\}", t, re.S)
    if m:
        try:
            obj = json.loads(m.group(0))
            ans = obj.get("answers")
        except (json.JSONDecodeError, AttributeError):
            ans = None
    if ans is None:
        ans = re.findall(r"\b(TRUE|FALSE|UNDETERMINED)\b", t.upper())
    out = []
    for a in ans:
        s = str(a).strip().upper()
        if s.startswith("TRUE"):
            out.append("TRUE")
        elif s.startswith("FALSE"):
            out.append("FALSE")
        elif s.startswith("UNDET"):
            out.append("UNDETERMINED")
        else:
            out.append("UNDETERMINED")
    return out if len(out) == n else None


def score(worlds: list[dict], verdicts: list[str] | None) -> dict:
    """Oriented B2 scores from per-world reader verdicts."""
    n = len(worlds)
    if not n or verdicts is None or len(verdicts) != n:
        return {"b2_score": None, "b2_mismatch_det": None, "b2_undet_share": None}
    det = [(w, v) for w, v in zip(worlds, verdicts) if v != "UNDETERMINED"]
    mism = sum(1 for w, v in det if (v == "TRUE") != w["phi_truth"])
    und = n - len(det)
    per_op = {}
    for w, v in zip(worlds, verdicts):
        o = per_op.setdefault(w["mutant_op"], [0, 0])
        o[1] += 1
        o[0] += (v == "UNDETERMINED") * 0.5 + (v != "UNDETERMINED" and (v == "TRUE") != w["phi_truth"])
    return {"b2_score": (mism + 0.5 * und) / n, "b2_mismatch_det": (mism / len(det)) if det else None,
            "b2_undet_share": und / n, "per_op": {k: v[0] / v[1] for k, v in per_op.items()}}


def world_probe(text: str, fol: str, item_key: str, reader) -> dict:
    """Synchronous convenience API: reader(prompt:str) -> raw JSON text. Used by the reusable deliverable."""
    b = build_worlds(fol, item_key)
    if b["status"] != "ok":
        return {"b2_score": None, "b2_mismatch_det": None, "b2_undet_share": None, "n_worlds": 0, "worlds": [], "status": b["status"]}
    raw = reader(reader_prompt(text, b["worlds"]))
    v = parse_answers(raw, len(b["worlds"]))
    s = score(b["worlds"], v)
    ws = [{**w, "verdict": (v[i] if v else None)} for i, w in enumerate(b["worlds"])]
    return {**s, "n_worlds": len(ws), "worlds": ws, "status": "ok" if v else "reader_fail"}
