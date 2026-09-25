#!/usr/bin/env python3
"""C1: copy the reusable code of earlier artifacts into lib/vendor/<name>/ (python files + small prompt data only; never
__pycache__), write lib/PROVENANCE.json (source path, sha256 source, sha256 copy, identical flag)."""
from __future__ import annotations

import shutil
from pathlib import Path

from common import DS5, E1, E5, E8, EV2, ROOT, jdump, sha256_file, utc

LIB = ROOT / "lib" / "vendor"
SPEC = {
    "exp8_consensus": (E8, ["src/*.py", "src/vendor_a/*.py", "src/vendor_c/*.py", "src/vendor_d/*.py", "src/vendor_d/labeller/*.py",
                            "src/vendor_e/*.py", "data/prompts/*"]),
    "eval2_pairwise": (EV2, ["src/pairwise.py", "src/mechanism.py", "src/consensus_mx.py", "src/stats.py", "src/paths.py",
                             "vendor_exp5/*.py", "vendor_exp5/vendor_a/*.py", "vendor_exp5/vendor_c/*.py", "vendor_exp5/vendor_d/*.py",
                             "vendor_exp5/vendor_d/labeller/*.py", "vendor_exp5/vendor_e/*.py"]),
    "exp5_peer_text": (E5, ["src/*.py", "src/vendor_a/*.py", "src/vendor_c/*.py", "src/vendor_d/*.py", "src/vendor_d/labeller/*.py",
                            "src/vendor_e/*.py"]),
    "dataset5_freelab": (DS5, ["src/freelab.py", "src/common.py", "src/gloss.py", "vendor/*.py", "prompts/*"]),
    "exp1_triage": (E1, ["src/*.py"]),
}


def main():
    prov = {"written_utc": utc(), "files": []}
    for name, (src_root, globs) in SPEC.items():
        for g in globs:
            for p in sorted(src_root.glob(g)):
                if not p.is_file() or "__pycache__" in p.parts:
                    continue
                rel = p.relative_to(src_root)
                dst = LIB / name / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(p, dst)
                h_src, h_dst = sha256_file(p), sha256_file(dst)
                prov["files"].append({"vendor": name, "source": str(p), "copy": str(dst.relative_to(ROOT)), "sha256": h_src,
                                      "identical": h_src == h_dst, "bytes": p.stat().st_size})
    jdump(prov, ROOT / "lib" / "PROVENANCE.json")
    print(len(prov["files"]), "files;", all(f["identical"] for f in prov["files"]))


if __name__ == "__main__":
    main()
