#!/bin/bash
# NOTE (published copy): this file names server paths this repository
# does not publish (a stage it does not ship, or another run's workspace),
# so the steps that read them will not run from a clone as written:
#   /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4
# Restores every path marked `delete` in .aii/manifest.yaml (run from this directory).
set -e
cd "$(dirname "$0")"
D4=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_4/gen_art/gen_art_dataset_4
[ -d e2bsrc/data_local ] || cp -r $D4/data_local e2bsrc/
(cd e2bsrc && uv venv .venv --python=3.12 && uv pip install --python=.venv/bin/python -r pyproject.toml scikit-learn)
(cd exp5src && uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml)
e2bsrc/.venv/bin/python -c "import nltk; [nltk.download(p, download_dir='e2bsrc/nltk_data') for p in ('wordnet','omw-1.4')]"
mkdir -p exp5src/data/nltk_data/corpora
for p in wordnet omw-1.4 words; do
  curl -sL -o exp5src/data/nltk_data/corpora/$p.zip https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/$p.zip
  (cd exp5src/data/nltk_data/corpora && unzip -q -o $p.zip)
done
(cd e2bsrc && .venv/bin/python - <<'PY'
from huggingface_hub import hf_hub_download as d
for f in ("dev/easy.json", "dev/medium.json", "dev/hard.json"):
    d("opendatalab/ProverQA", f, repo_type="dataset", revision="e2561beed450272690da658d21ae667570dbbafc", local_dir="raw/hf/opendatalab__ProverQA")
for f in ("folio_v2_train.jsonl", "folio_v2_validation.jsonl"):
    d("tasksource/folio", f, repo_type="dataset", revision="295b95fb4fe9be4ff3f933b73142d142cf6b2c97", local_dir="raw/hf/tasksource__folio")
PY
)
e2bsrc/.venv/bin/python -m pytest -q -c e2bsrc/pytest.ini e2bsrc/tests/test_fol.py
