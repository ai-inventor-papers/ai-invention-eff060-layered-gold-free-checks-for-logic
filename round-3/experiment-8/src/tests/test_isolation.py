"""Label isolation: label-free scoring scripts never reference label keys; analyses refuse without a valid frozen prereg."""
import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LABEL_FREE = ["src/run_scoring.py", "src/tasks.py", "src/pairs.py", "src/perturb_cpu.py", "src/perturb_gpu.py",
              "src/run_api_perturb.py"]  # freeze_prereg_hyb.py only NAMES label fields in the rule text
BAD = re.compile(r"final_label|label_tier|E_labels|\[\"label\"\]|'label'|screen_adjudicated_labels")


def test_scoring_scripts_never_read_labels():
    for f in LABEL_FREE:
        # lines that ASSERT the absence of label keys (the blind-view guard) are allowed
        txt = "\n".join(l for l in (ROOT / f).read_text().splitlines() if "not in r" not in l and "label key" not in l
                        and '"output", "final_label"' not in l)
        assert not BAD.search(txt), f"{f} references a label key: {BAD.search(txt).group(0)}"


def test_preregs_intact_and_before_analyses():
    for name in ("prereg_hyb", "prereg_perturb"):
        p = ROOT / "results" / f"{name}.json"
        want = (ROOT / "results" / f"{name}.sha256").read_text().split()[0]
        assert hashlib.sha256(p.read_bytes()).hexdigest() == want
    import json
    t_hyb = json.loads((ROOT / "results/prereg_hyb.json").read_text())["timestamp_utc"]
    t_pb = json.loads((ROOT / "results/prereg_perturb.json").read_text())["timestamp_utc"]
    assert t_hyb < t_pb
    assert json.loads((ROOT / "results/prereg_hyb.json").read_text())["labels_joined_before_freeze"] is False


def test_analysis_refuses_without_prereg(tmp_path):
    code = ("import sys; sys.path.insert(0, 'src'); import an_common as C; C.RES = __import__('pathlib').Path(r'%s'); C.guard()" % tmp_path)
    r = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True)
    assert r.returncode != 0 and "refusing" in (r.stdout + r.stderr)
