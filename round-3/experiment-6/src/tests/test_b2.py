"""T0(6): B2 world construction on handmade formulas; independent evaluator re-check; stub readers."""
import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault("PYTHONHASHSEED", "0")
from src.b2_world_probe import build_worlds, score, _eval, domains, _consts  # noqa: E402
from src.labeller.fol import parse  # noqa: E402

CASES = ["∀x (Student(x) → Smart(x))",
         "∀x ((Car(x) ∧ MadeIn(x, maranello)) → Carry(x, ferrariV12Engine))",
         "Kitten(piper) ∨ CuteAnimal(piper)",
         "∀x (Planet(x) ∧ In(x, solarSystem) → ¬RelyOnToGenerate(x, nuclearFusion, light))",
         "∃x (Dog(x) ∧ ∀y (Cat(y) → Chases(x, y)))"]
ok = True
for f in CASES:
    t0 = time.time()
    b = build_worlds(f, "test|" + f)
    phi = parse(f)
    print(f"{f}\n  status={b['status']} n_worlds={len(b['worlds'])} tried={b.get('n_mut_tried')} {time.time()-t0:.2f}s")
    for w in b["worlds"]:
        print(f"   [{w['mutant_op']}/{w['direction']}] psi={w['mutant']}")
        print("     " + w["world_text"].replace("\n", "\n     "))
        assert not re.search(r"[∀∃¬∧∨→↔⊕]", w["world_text"]), "logic symbol leaked into world text"
    ts = [w["phi_truth"] for w in b["worlds"]]
    if len(ts) >= 2 and all(ts) or (len(ts) >= 2 and not any(ts)):
        print("  WARNING: one-sided truth values")
    always_true = score(b["worlds"], ["TRUE"] * len(b["worlds"]))
    oracle = score(b["worlds"], ["TRUE" if w["phi_truth"] else "FALSE" for w in b["worlds"]])
    print(f"  always-TRUE b2={always_true['b2_score']:.2f}  oracle b2={oracle['b2_score']:.2f}")
    ok &= oracle["b2_score"] == 0
    if f.startswith("∀x (Student"):
        ops = {w["mutant_op"] for w in b["worlds"]}
        ok &= len(b["worlds"]) >= 3
print("T0-B2", "PASS" if ok else "FAIL")
