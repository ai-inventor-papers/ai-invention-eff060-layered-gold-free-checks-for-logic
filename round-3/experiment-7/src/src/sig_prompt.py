"""SIG condition prompt: dataset-3's frozen fewshot_v1 prompt + a fixed, alphabetically sorted signature block.

build_signature_block(sentence, lex) lists every predicate symbol (with arity) and every constant that occurs in ANY
accepted/recorded reading of the sentence (weak, strong, and the T8 converse), each with a gloss taken from the
lexicon entry whose pred_final equals the predicate (its positive verb phrase `vp_sg_pos`) and a verbatim example atom.
Lines are sorted alphabetically by predicate name (never template order), so the role of an atom (condition,
consequent, exception, proviso) is not leaked; the block contains no wording about exceptions or readings.
The few-shot system message and exemplars are byte-identical to prompts/fewshot_v1.txt; the block is appended to the
final user message only (exemplars keep their own vocabulary; disclosed).
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RC = ROOT / "rcomp"
sys.path.insert(0, str(RC / "labeller"))
sys.setrecursionlimit(10000)
from fol import parse  # noqa: E402  (dataset-3 / dataset-E parser)
from repair_census import atoms, bound_vars  # noqa: E402

HEADER = "Use only these predicates and constants (do not introduce any others):"
FORBIDDEN_WORDS = ("unless", "except", "provided", "only", "weak", "strong", "exception", "iff")


def load_prompt() -> tuple[dict, str, str]:
    txt = (RC / "prompts" / "fewshot_v1.txt").read_text()
    return json.loads(txt), hashlib.sha1(txt.encode()).hexdigest(), hashlib.sha256(txt.encode()).hexdigest()


def load_lexicon() -> dict:
    return {e["lexicon_id"]: e for e in json.loads((RC / "lexicon.json").read_text())["entries"]}


def reference_signature(sent: dict) -> tuple[dict, set, dict]:
    """-> ({(pred, arity): example_atom_string}, {constants}, {pred: first atom args}) over every stored reading."""
    preds, consts = {}, set()
    for key in ("reference_fol_weak", "reference_fol_strong", "reading_converse"):
        f = sent.get(key)
        if not f:
            continue
        e = parse(f)
        bv = bound_vars(e)
        for a in atoms(e):
            k = (a[1], len(a[2]))
            if k not in preds:
                preds[k] = a
            for x in a[2]:
                if x not in bv:
                    consts.add(x)
    return preds, consts, {}


def _example(atom, bv_letters=("x", "y", "z")) -> str:
    name, args = atom[1], atom[2]
    return f"{name}({', '.join(args)})" if args else name


def build_signature_block(sent: dict, lex: dict) -> str:
    preds, consts, _ = reference_signature(sent)
    gloss = {}
    for lid in sent["lexicon_ids"]:
        e = lex.get(lid)
        if e is not None:
            gloss[e["pred_final"]] = e["vp_sg_pos"]
    lines = []
    for (name, ar), atom in sorted(preds.items(), key=lambda kv: (kv[0][0].lower(), kv[0][0], kv[0][1])):
        g = gloss.get(name)
        if g is None:
            raise KeyError(f"no lexicon gloss for predicate {name} in sentence {sent['sentence_id']}")
        lines.append(f"{name}/{ar}: {g}  e.g. {_example(atom)}")
    block = HEADER + "\n" + "\n".join(lines)
    if consts:
        block += "\nConstants: " + ", ".join(sorted(consts, key=lambda c: (c.lower(), c)))
    return block


def sig_messages(sent: dict, prompt: dict, lex: dict) -> list[dict]:
    user = prompt["user_template"].format(sentence=sent["text"]) + "\n\n" + build_signature_block(sent, lex)
    return [{"role": "system", "content": prompt["system"]}] + prompt["exemplars"] + [{"role": "user", "content": user}]


def free_messages(sent: dict, prompt: dict) -> list[dict]:
    return ([{"role": "system", "content": prompt["system"]}] + prompt["exemplars"]
            + [{"role": "user", "content": prompt["user_template"].format(sentence=sent["text"])}])


def signature_symbols(sent: dict) -> tuple[dict, set]:
    """{pred_name: arity} (names unique per sentence by construction) and the constant set."""
    preds, consts, _ = reference_signature(sent)
    out = {}
    for (n, a) in preds:
        if n in out and out[n] != a:
            raise ValueError(f"arity clash for {n} in {sent['sentence_id']}")
        out[n] = a
    return out, consts
