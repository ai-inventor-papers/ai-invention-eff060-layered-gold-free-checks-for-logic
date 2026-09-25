#!/usr/bin/env python3
"""STEP 2d: ccg2lambda (kenken6696/folio_by_ccg2lambda, TRAIN split only) candidates for CTRL sentences.

NLTK event-semantics -> fol.py syntax. Deterministic surface conversion:
  _name(x) -> Name(x); exists/all -> ∃/∀; & | -> <-> - -> ∧ ∨ → ↔ ¬;
  role equalities Subj(e) = x -> Subj(e, x) (function term relationalised); x = y -> Eq(x, y).
Writes raw/ccg2lambda_candidates.jsonl (system='ccg2lambda', system_class='symbolic_eventsem').
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd
from nltk.sem import logic as L

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "labeller"))
sys.setrecursionlimit(10000)
from select_sentences import norm  # noqa: E402
from fol import parse  # noqa: E402


def pname(n: str) -> str:
    n = n.lstrip("_")
    parts = [p for p in n.replace("-", "_").split("_") if p]
    return "".join(p[:1].upper() + p[1:] for p in parts) or "P"


def term(t) -> str:
    if isinstance(t, (L.IndividualVariableExpression, L.EventVariableExpression, L.FunctionVariableExpression, L.VariableExpression)):
        return str(t.variable)
    if isinstance(t, L.ConstantExpression):
        return str(t.variable).lstrip("_").lower()
    raise ValueError(f"complex term {t}")


def emit(e) -> str:
    if isinstance(e, L.ExistsExpression):
        return f"∃{e.variable} ({emit(e.term)})"
    if isinstance(e, L.AllExpression):
        return f"∀{e.variable} ({emit(e.term)})"
    if isinstance(e, L.NegatedExpression):
        return f"¬({emit(e.term)})"
    if isinstance(e, L.AndExpression):
        return f"({emit(e.first)} ∧ {emit(e.second)})"
    if isinstance(e, L.OrExpression):
        return f"({emit(e.first)} ∨ {emit(e.second)})"
    if isinstance(e, L.ImpExpression):
        return f"({emit(e.first)} → {emit(e.second)})"
    if isinstance(e, L.IffExpression):
        return f"({emit(e.first)} ↔ {emit(e.second)})"
    if isinstance(e, L.EqualityExpression):
        a, b = e.first, e.second
        if isinstance(a, L.ApplicationExpression):
            f, args = a.uncurry()
            return f"{pname(str(f))}({', '.join([term(x) for x in args] + [term(b)])})"
        if isinstance(b, L.ApplicationExpression):
            f, args = b.uncurry()
            return f"{pname(str(f))}({', '.join([term(x) for x in args] + [term(a)])})"
        return f"Eq({term(a)}, {term(b)})"
    if isinstance(e, L.ApplicationExpression):
        f, args = e.uncurry()
        return f"{pname(str(f))}({', '.join(term(x) for x in args)})"
    if isinstance(e, (L.ConstantExpression, L.FunctionVariableExpression)):
        return pname(str(e))
    raise ValueError(f"unsupported {type(e).__name__}: {e}")


def main():
    sents = json.loads((ROOT / "work" / "sentences.json").read_text())
    ctrl = {norm(s["text"]): s for s in sents if s["source_stratum"] == "CTRL"}
    df = pd.read_parquet(ROOT / "raw/hf/kenken6696__folio_by_ccg2lambda/data/train-00000-of-00001.parquet")
    out, seen, stats = [], set(), {"train_rows": len(df), "matched": 0, "convert_fail": 0, "parse_fail": 0}
    for _, r in df.iterrows():
        n = norm(r["original"])
        if n not in ctrl or n in seen:
            continue
        seen.add(n)
        stats["matched"] += 1
        s = ctrl[n]
        raw = r["logical_form"]
        try:
            fol = emit(L.Expression.fromstring(raw))
        except Exception as ex:  # noqa: BLE001 - nltk raises LogicalExpressionException and friends
            stats["convert_fail"] += 1
            fol, err = "", f"convert: {str(ex)[:100]}"
        else:
            err = ""
        ok = False
        if fol:
            try:
                parse(fol); ok = True
            except Exception as ex:  # noqa: BLE001
                stats["parse_fail"] += 1; err = f"parse: {str(ex)[:100]}"
        out.append({"sentence_id": s["sentence_id"], "slot": "CCG", "system": "ccg2lambda", "model": "ccg2lambda",
                    "family": "symbolic", "system_class": "symbolic_eventsem", "prompt_variant": "none",
                    "prompt_sha1": None, "raw_output": raw, "candidate_fol": fol, "normalisation_applied": ["nltk_to_fol"],
                    "parse_ok": ok, "parse_error": err, "cost_usd": 0.0})
    (ROOT / "raw" / "ccg2lambda_candidates.jsonl").write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in out))
    stats["ctrl_sentences"] = len(ctrl)
    (ROOT / "work" / "ccg2lambda_stats.json").write_text(json.dumps(stats, indent=1))
    print(stats)
    for x in out[:3]:
        print(x["raw_output"], "\n  ->", x["candidate_fol"], x["parse_ok"])


if __name__ == "__main__":
    main()
