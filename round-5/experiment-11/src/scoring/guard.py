"""Label-blind file-access allowlist for every scoring/ process (E2-A, iteration 5).

Imported FIRST by every scoring script. It wraps builtins.open, io.open, os.open and pathlib.Path.open / read_text /
read_bytes. A path is refused (PermissionError) when
  * it matches a label-like pattern (label | labels_ | panel_ | seal | full_data_out | reference_overrides | trackh), or
  * it is a WORKSPACE data file outside the allowed roots {e2/candidates_E2_nolabels.jsonl, frozen/, freeze_copy/,
    cache/, scoring/, env/ (python packages), logs/}.
Library files outside /ai-inventor (site-packages, model weights, /proc, /tmp, the HF cache) are allowed, because they
cannot hold E2 labels; the label-like pattern check applies to every path under /ai-inventor (all run data).
"""
from __future__ import annotations

import builtins
import io
import os
import pathlib
import re

WS = pathlib.Path(__file__).resolve().parents[1]
DENY = re.compile(r"(label|labels_|panel_|seal|full_data_out|reference_overrides|trackh)", re.I)
ALLOW_FILES = {WS / "e2" / "candidates_E2_nolabels.jsonl", WS / "prereg_iter5_E2A.json", WS / "scores_E2A.jsonl",
               WS / "score_seal.json"}  # the two label-free OUTPUT files of the scoring stage
ALLOW_DIRS = [WS / d for d in ("frozen", "freeze_copy", "cache", "scoring", "env", "logs")]
# frozen/ holds copied CODE; its sub-paths may contain the word 'labeller' (a code package, not labels)
CODE_OK = re.compile(r"/frozen/.*\.py$|/labeller/?$")


def check(path) -> None:
    try:
        p = pathlib.Path(os.fspath(path)).resolve()
    except TypeError:  # file descriptors
        return
    s = str(p)
    if s.startswith(str(WS) + os.sep + "env" + os.sep):  # installed python packages of the scoring env
        return
    if p in ALLOW_FILES:  # the label-free candidate file (its name contains 'nolabels')
        return
    if s.startswith("/ai-inventor") and DENY.search(s) and not CODE_OK.search(s):
        raise PermissionError(f"scoring guard: label-like path refused: {s}")
    if s.startswith(str(WS) + os.sep) or s == str(WS):
        if p in ALLOW_FILES or any(s == str(d) or s.startswith(str(d) + os.sep) for d in ALLOW_DIRS):
            return
        raise PermissionError(f"scoring guard: workspace path outside the allowlist: {s}")


_open, _io_open, _os_open = builtins.open, io.open, os.open
_p_open, _p_rt, _p_rb = pathlib.Path.open, pathlib.Path.read_text, pathlib.Path.read_bytes


def _g_open(file, *a, **k):
    if not isinstance(file, int):
        check(file)
    return _open(file, *a, **k)


def _g_os_open(path, *a, **k):
    check(path)
    return _os_open(path, *a, **k)


def _g_p_open(self, *a, **k):
    check(self)
    return _p_open(self, *a, **k)


def _g_p_rt(self, *a, **k):
    check(self)
    return _p_rt(self, *a, **k)


def _g_p_rb(self, *a, **k):
    check(self)
    return _p_rb(self, *a, **k)


def install() -> None:
    builtins.open = _g_open
    io.open = _g_open
    os.open = _g_os_open
    pathlib.Path.open = _g_p_open
    pathlib.Path.read_text = _g_p_rt
    pathlib.Path.read_bytes = _g_p_rb


install()
