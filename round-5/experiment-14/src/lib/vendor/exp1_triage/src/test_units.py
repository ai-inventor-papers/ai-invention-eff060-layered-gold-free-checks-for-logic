"""T3 (formula_role_profile) and T4 (role_accounting planted errors) unit tests."""
import sys
from fol_triage import formula_role_profile, role_accounting, fol_lint, content_accounting

def t3():
    p = formula_role_profile("∀x (Dog(x) ∧ Bark(x) → Loud(x))")
    assert p["Dog/1"]["mono"] == "DOWN" and p["Dog/1"]["role"] == "condition", p
    assert p["Bark/1"]["role"] == "condition" and p["Loud/1"]["role"] == "asserted" and p["Loud/1"]["mono"] == "UP"
    assert all(v["force"] == "all" and v["claim"] == 0 for v in p.values())
    p = formula_role_profile("∀x ∀y (Wolf(x) ∧ Bird(y) → Howl(x) ∧ Chirp(y))")
    assert p["Wolf/1"]["claim"] == p["Howl/1"]["claim"] != p["Bird/1"]["claim"] == p["Chirp/1"]["claim"], p
    p = formula_role_profile("∀x (A(x) ∧ ¬E(x) → B(x))")
    assert p["E/1"]["mono"] == "UP" and p["E/1"]["local_neg"] and p["E/1"]["pos"] == "antecedent", p
    p = formula_role_profile("Loves(john, mary)")
    assert p["Loves/2"]["force"] == "named" and p["Loves/2"]["slots"] == [("const", "john"), ("const", "mary")], p
    p = formula_role_profile("∀x ∀y (Dog(x) ∧ Cat(y) ∧ Chases(x, y) → Barks(x))")
    assert p["Chases/2"]["slots"] == [("var", "Dog"), ("var", "Cat")], p["Chases/2"]
    print("T3 pass")

T4 = [  # (text, correct fol, planted-error fol, error type)
    ("Every dog that barks is loud.", "∀x (Dog(x) ∧ Bark(x) → Loud(x))", "∀x (Dog(x) ∧ Loud(x) → Bark(x))", "RESTR"),
    ("If a student studies, then the student passes.", "∀x (Student(x) ∧ Study(x) → Pass(x))", "∀x (Student(x) ∧ Pass(x) → Study(x))", "RESTR"),
    ("All employees who travel are reimbursed.", "∀x (Employee(x) ∧ Travel(x) → Reimbursed(x))", "∀x (Employee(x) ∧ Reimbursed(x) → Travel(x))", "RESTR"),
    ("No managers work remotely.", "∀x (Manager(x) → ¬WorkRemotely(x))", "∀x (Manager(x) → WorkRemotely(x))", "NEG"),
    ("Bonnie does not perform in talent shows.", "¬Perform(bonnie, talentShow)", "Perform(bonnie, talentShow)", "NEG"),
    ("If a plant is not watered, it wilts.", "∀x (Plant(x) ∧ ¬Watered(x) → Wilt(x))", "∀x (Plant(x) ∧ Watered(x) → Wilt(x))", "NEG"),
    ("John loves Mary.", "Loves(john, mary)", "Loves(mary, john)", "SWAP"),
    ("Mary is admired by Leo.", "Admires(leo, mary)", "Admires(mary, leo)", "SWAP"),
    ("Every cat chases a mouse.", "∀x (Cat(x) → ∃y (Mouse(y) ∧ Chases(x, y)))", "∀x (Cat(x) → ∃y (Mouse(y) ∧ Chases(y, x)))", "SWAP"),
    ("Some birds cannot fly.", "∃x (Bird(x) ∧ ¬Fly(x))", "∃x (Bird(x) ∧ Fly(x))", "NEG"),
]

def t4():
    bad = 0
    for text, good, err, typ in T4:
        rg, re_ = role_accounting(text, good), role_accounting(text, err)
        ok = (not rg["flag"]) and re_["flag"]
        bad += not ok
        print(("OK  " if ok else "FAIL"), typ, text, "| correct:", rg["codes"], "| error:", re_["codes"])
    print(f"T4 {len(T4) - bad}/{len(T4)} pass")
    return bad

if __name__ == "__main__":
    t3()
    b = t4()
    print(fol_lint("∃x (Dog(x) → Bark(x))"), content_accounting("Every dog barks.", "∀x (Dog(x) → Bark(x))"))
    sys.exit(1 if b else 0)
