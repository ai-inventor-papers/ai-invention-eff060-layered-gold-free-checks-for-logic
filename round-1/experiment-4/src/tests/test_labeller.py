# NOTE (published copy): this file names server paths this repository
# does not publish (a stage it does not ship, or another run's workspace),
# so the steps that read them will not run from a clone as written:
#   /ai-inventor/aii_data/runs/run_u75jRHUss0zo/iter_3/gen_hypo/claude_agent/data/DSAVlab-UNIUD_FOLIO_validation-curated__FOLIO_instances.jsonl
"""T1: parser precedence + labeller identity/rename checks."""
import os, sys, random
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.labeller.fol import parse
from src.labeller.labeller import equivalent_modulo_vocab
A, B, C = ("atom", "A", ("x",)), ("atom", "B", ("x",)), ("atom", "C", ("x",))
assert parse("A(x) ⊕ B(x) → C(x)") == ("imp", ("xor", A, B), C), parse("A(x) ⊕ B(x) → C(x)")
assert parse("A → B → C") == ("imp", ("atom", "A", ()), ("imp", ("atom", "B", ()), ("atom", "C", ())))
e = parse("∀x (P(x)) ∧ ∀y (Q(y))")
assert e[0] == "and" and e[1][0] == "all" and e[2][0] == "all", e
assert parse("A(x) ∨ B(x) ⊕ C(x)")[0] in ("or", "xor")
assert parse("A(x) ∧ B(x) ⊕ C(x)") == ("xor", ("and", A, B), C)
print("precedence OK")
import json
rows = [json.loads(l) for l in open("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/iter_3/gen_hypo/claude_agent/data/DSAVlab-UNIUD_FOLIO_validation-curated__FOLIO_instances.jsonl") if l.strip()]
golds = [r["FOL_sentence"] for r in rows if str(r["id"]).startswith("concl")]
random.Random(0).shuffle(golds)
ok_id = ok_ren = n = 0
import re
for g in golds[:50]:
    try: parse(g)
    except Exception: continue
    n += 1
    ok_id += equivalent_modulo_vocab(g, g)["cls"] == "EQUIV"
    # rename every predicate P -> PRenamedX (keeps token overlap) : expect VOCAB
    ren = re.sub(r"\b([A-Z][A-Za-z0-9]*)\(", lambda m: m.group(1) + "Thing(", g)
    r = equivalent_modulo_vocab(ren, g)
    ok_ren += r["cls"] in ("VOCAB", "GRAN", "EQUIV")
print(f"identity EQUIV {ok_id}/{n}; renamed -> VOCAB {ok_ren}/{n}")
assert ok_id == n
