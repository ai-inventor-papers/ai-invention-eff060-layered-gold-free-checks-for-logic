#!/usr/bin/env python3
"""STEP A1: vendor the reused code by COPYING it (whole files, or single functions extracted with `ast`) into ./vendor,
recording the sha256 of every source file and of every written vendor file in VENDOR_SHA256.json.

Firewall: nothing from consensus_lib / peer_text / consensus_rcomp / the eqmv aligner / repair_census.align /
tri / dice / toks / any name-similarity helper is copied. Only the listed functions are extracted.
"""
from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = Path(__file__).resolve().parents[4]
D3 = R / "iter_2/gen_art/gen_art_dataset_3"
E5 = R / "iter_2/gen_art/gen_art_experiment_5"
E7 = R / "iter_3/gen_art/gen_art_experiment_7"
V = ROOT / "vendor"

WHOLE = {"fol.py": D3 / "labeller/fol.py", "templates.py": D3 / "src/templates.py"}
EXTRACT = {
    "repair_census_min.py": (D3 / "labeller/repair_census.py", ["atoms", "bound_vars", "symbols", "rename"],
                             "import itertools\nfrom fol import parse, equivalent  # noqa: F401\n"),
    "perturb_min.py": (D3 / "src/perturb.py", ["name_tokens", "wn_synonyms", "meaning_rename", "first_sense_synonyms",
                                               "control_rename"],
                       "import random\nimport re\nimport hashlib\n\n\ndef sha1(s: str) -> str:\n    return hashlib.sha1(s.encode()).hexdigest()\n\n\nCONS, VOW = 'bdfgklmnprtvz', 'aeiou'\n"),
    "fol_triage_min.py": (E5 / "src/vendor_a/fol_triage.py", ["_occurrences", "formula_role_profile"],
                          "from collections import Counter, defaultdict  # noqa: F401\nfrom fol import parse, profile, prenex_blocks  # noqa: F401\n"),
    "sig_prompt_min.py": (E7 / "src/sig_prompt.py", ["reference_signature", "signature_symbols"],
                          "from fol import parse\nfrom repair_census_min import atoms, bound_vars\n"),
    "label_sig_min.py": (E7 / "src/label_sig.py", ["_to_str", "_rename", "_free_consts"], ""),
}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main() -> None:
    V.mkdir(exist_ok=True)
    rec = {"sources": {}, "vendor": {}}
    for dst, src in WHOLE.items():
        (V / dst).write_bytes(src.read_bytes())
        rec["sources"][str(src)] = sha(src)
    for dst, (src, names, header) in EXTRACT.items():
        txt = src.read_text()
        tree = ast.parse(txt)
        lines = txt.splitlines()
        parts = []
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name in names:
                parts.append("\n".join(lines[node.lineno - 1 - len(node.decorator_list):node.end_lineno]))
        missing = set(names) - {p.split("(")[0].replace("def ", "").strip() for p in parts}
        assert not missing, (dst, missing)
        body = (f'"""Extracted verbatim from {src} (sha256 {sha(src)}): {", ".join(names)}."""\n'
                "from __future__ import annotations\n" + header + "\n\n" + "\n\n\n".join(parts) + "\n")
        (V / dst).write_text(body)
        rec["sources"][str(src)] = sha(src)
    (V / "__init__.py").write_text("")
    for p in sorted(V.glob("*.py")):
        rec["vendor"][p.name] = sha(p)
    (ROOT / "VENDOR_SHA256.json").write_text(json.dumps(rec, indent=1))
    print(json.dumps(rec, indent=1))


if __name__ == "__main__":
    main()
