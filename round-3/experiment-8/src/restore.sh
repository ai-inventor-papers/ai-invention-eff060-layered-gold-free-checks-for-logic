#!/bin/bash
# Restore everything the .aii/manifest.yaml marks `delete` (venv, pair cache, NLTK data, model weights).
set -e
cd "$(dirname "$0")"
# 1. Python environment (uv only). torch: default PyPI wheel (CUDA 13 build) worked with driver 580 / CUDA 13.0.
uv venv .venv --python=3.12
uv pip install --python .venv/bin/python -r requirements.txt
# 1b. transformers import-time rglob is extremely slow on network filesystems: cache its file list (optional speed patch)
T=.venv/lib/python3.12/site-packages/transformers
find $T/models -name "image_processing_*.py" | sed "s|^$T/||" | sort > $T/_aii_image_processing_files.txt
.venv/bin/python - <<'PY'
from pathlib import Path
p = Path(".venv/lib/python3.12/site-packages/transformers/__init__.py"); s = p.read_text()
old = '    for _proc_file in sorted((Path(__file__).parent / "models").rglob("image_processing_*.py")):'
new = ('    _aii_list = Path(__file__).parent / "_aii_image_processing_files.txt"  # AII PATCH\n'
       '    _aii_files = ([Path(__file__).parent / l for l in _aii_list.read_text().split()] if _aii_list.exists()\n'
       '                  else sorted((Path(__file__).parent / "models").rglob("image_processing_*.py")))\n'
       '    for _proc_file in _aii_files:')
if old in s:
    p.write_text(s.replace(old, new))
PY
# 2. NLTK data (WordNet, OMW, words) used by L2-bow / ALIGN token matching
.venv/bin/python -c "import nltk; [nltk.download(x, download_dir='data/nltk_data') for x in ('wordnet', 'omw-1.4', 'words')]"
# 3. Local model weights (into the platform HF cache)
scripts/download_models.sh
# 4. Pair cache (optional; speeds up re-scoring): rebuilt by the pair engine
# .venv/bin/python src/run_scoring.py E --stage all && .venv/bin/python src/run_scoring.py screen --stage all
