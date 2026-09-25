#!/bin/bash
# Restore every path .aii/manifest.yaml marks `delete` (run from the workspace root).
set -e
cd "$(dirname "$0")"
uv venv .venv --python=3.12 && uv pip install --python .venv/bin/python -r pyproject.toml
ln -sfn ../.venv rcomp/.venv
uv venv .venv_gpu --python=3.12 && uv pip install --python .venv_gpu/bin/python -r requirements_gpu.txt
mkdir -p data/nltk_data/corpora
for p in wordnet omw-1.4 words; do
  curl -sL -o data/nltk_data/corpora/$p.zip https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/corpora/$p.zip
  (cd data/nltk_data/corpora && unzip -q -o $p.zip && rm $p.zip)
done
# local judge weights live in the run's shared HF cache (HF_HOME), not in this workspace:
# .venv_gpu/bin/python -c "from huggingface_hub import snapshot_download; snapshot_download('Qwen/Qwen3-8B')"
