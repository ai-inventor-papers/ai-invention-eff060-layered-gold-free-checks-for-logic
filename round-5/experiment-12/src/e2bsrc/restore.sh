#!/bin/bash
# Restores every path marked `delete` in .aii/manifest.yaml.
set -e
cd "$(dirname "$0")"
uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r pyproject.toml
.venv/bin/python -c "import nltk; [nltk.download(p, download_dir='nltk_data') for p in ('wordnet','omw-1.4')]"
.venv/bin/python - <<'PY'
from huggingface_hub import hf_hub_download as d
for f in ("dev/easy.json", "dev/medium.json", "dev/hard.json", "train/provergen-5000.json", "README.md"):
    d("opendatalab/ProverQA", f, repo_type="dataset", revision="e2561beed450272690da658d21ae667570dbbafc", local_dir="raw/hf/opendatalab__ProverQA")
for f in ("folio_v2_train.jsonl", "folio_v2_validation.jsonl"):
    d("tasksource/folio", f, repo_type="dataset", revision="295b95fb4fe9be4ff3f933b73142d142cf6b2c97", local_dir="raw/hf/tasksource__folio")
# rejected candidates, previewed during the dataset search (not used by any script)
d("tasksource/LogicNLI", "data/validation-00000-of-00001-85e933b1046e9300.parquet", repo_type="dataset", local_dir="raw/hf/tasksource__LogicNLI")
d("jhkim64/NL2FOL_sentence", "data/train-00000-of-00001.parquet", repo_type="dataset", local_dir="raw/hf/jhkim64__NL2FOL_sentence")
PY
.venv/bin/python -m pytest -q -c pytest.ini tests/test_fol.py
