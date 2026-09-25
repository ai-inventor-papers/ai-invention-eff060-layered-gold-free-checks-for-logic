"""Extracted verbatim from ../../../../../../../round-3/experiment-7/src/src/sig_prompt.py (sha256 c4ccc4d724f3358840aa8c5f34d8a827fba263c78c6d07b763220f6f2c94bf3f): reference_signature, signature_symbols."""
from __future__ import annotations
from fol import parse
from repair_census_min import atoms, bound_vars


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


def signature_symbols(sent: dict) -> tuple[dict, set]:
    """{pred_name: arity} (names unique per sentence by construction) and the constant set."""
    preds, consts, _ = reference_signature(sent)
    out = {}
    for (n, a) in preds:
        if n in out and out[n] != a:
            raise ValueError(f"arity clash for {n} in {sent['sentence_id']}")
        out[n] = a
    return out, consts
