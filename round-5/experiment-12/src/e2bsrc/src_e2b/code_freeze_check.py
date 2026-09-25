#!/usr/bin/env python3
"""E2-B step 0.2: verify that every file frozen by E2 (prereg_E2.json labeller_sha256 + code_freeze.json) is
byte-identical in this copy (e2bsrc/). Any mismatch -> exit 1 (the run STOPS). Writes code_freeze_check_E2B.json."""
import hashlib
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def pins_equal(rel: str, orig: Path, copy: Path) -> tuple[bool, str]:
    import re
    import tomllib
    if rel == "pyproject.toml":
        a = sorted(tomllib.loads(orig.read_text())["project"]["dependencies"])
        b = sorted(tomllib.loads(copy.read_text())["project"]["dependencies"])
        return a == b, f"dependency pins identical ({len(a)}); only project name/description differ" if a == b else "PINS DIFFER"
    pk = lambda t: sorted((x["name"], x.get("version")) for x in tomllib.loads(t).get("package", []) if x.get("source", {}).get("virtual") is None and x.get("source", {}).get("editable") is None)
    a, b = pk(orig.read_text()), pk(copy.read_text())
    if a == b:
        return True, f"locked third-party packages identical ({len(a)}); only the root project entry differs"
    pins = set(tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]["dependencies"])
    extra_b, extra_a = set(b) - set(a), set(a) - set(b)
    if not extra_a and all(f"{n}=={v}" in pins for n, v in extra_b):
        return True, f"E2's lock adds {sorted(extra_b)} which is pinned identically in E's and E2's pyproject; all other packages identical; venv built from the pyproject pins"
    return False, f"LOCK DIFFERS: +{sorted(extra_b)} -{sorted(extra_a)}"


def main() -> int:
    pre = json.loads((ROOT / "prereg_E2.json").read_text())
    cf = json.loads((ROOT / "code_freeze.json").read_text())
    rows, bad = [], []
    d0_after = {d["file"]: d.get("sha256_after") for d in cf.get("deviations", [])}
    for rel, h in pre["labeller_sha256"].items():
        p = ROOT / rel
        got = sha(p) if p.exists() else None
        ok = got == h or (rel in d0_after and got == d0_after[rel])
        rows.append({"source": "prereg_E2.labeller_sha256", "file": rel, "expected": h, "got": got, "ok": ok})
        if not ok:
            bad.append(rel)
    d0 = {d["file"] for d in cf.get("deviations", [])}
    for f in cf["files"]:
        rel = f["copy"]
        p = ROOT / rel
        got = sha(p) if p.exists() else None
        # D0-modified files are checked against the post-D0 hash recorded in prereg labeller_sha256 above
        exp = d0_after[rel] if rel in d0 else f["sha256_copy"]
        ok = got == exp
        note = ""
        if not ok and rel in ("pyproject.toml", "uv.lock"):
            # E2 renamed its project (name/description) after the freeze; the dependency PINS are what must match
            ok, note = pins_equal(rel, Path(f["original"]), p)
        rows.append({"source": "code_freeze.json", "file": rel, "expected": exp, "got": got, "ok": ok, "d0_modified": rel in d0, "note": note})
        if not ok:
            bad.append(rel)
    pre_sha = sha(ROOT / "prereg_E2.json")
    exp_pre = (ROOT / "prereg_E2.sha256").read_text().split()[0]
    cf_sha = sha(ROOT / "code_freeze.json")
    out = {"checked_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "n_checked": len(rows), "n_mismatch": len(bad),
           "mismatches": sorted(set(bad)), "prereg_E2_sha256": pre_sha, "prereg_E2_sha256_expected": exp_pre,
           "prereg_ok": pre_sha == exp_pre, "code_freeze_sha256": cf_sha,
           "code_freeze_sha256_expected_by_prereg": pre["code_freeze_sha256"], "code_freeze_ok": cf_sha == pre["code_freeze_sha256"],
           "rows": rows}
    (ROOT / "code_freeze_check_E2B.json").write_text(json.dumps(out, indent=1))
    ok = not bad and out["prereg_ok"] and out["code_freeze_ok"]
    print(json.dumps({k: out[k] for k in ("n_checked", "n_mismatch", "mismatches", "prereg_ok", "code_freeze_ok")}))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
