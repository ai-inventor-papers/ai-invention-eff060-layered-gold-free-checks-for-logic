# Reproducibility: Candidate C (cross-system z3 consensus for NL→FOL faithfulness)

All commands are run from this folder (the artifact folder of the cloned repository). Everything below comes from
`README.md`, `method.py`, `run_all.sh`, `pyproject.toml`, `src/`, `tests/` and `results/`.

## 1. Get the artifact
```bash
git clone <URL of the public repository>   # URL not recorded in the workspace
cd <repo>/<this artifact folder>           # the folder holding method.py, run_all.sh, pyproject.toml
```

## 2. Environment
- OS: Ubuntu (Linux 6.8). No system packages beyond `python3.12` and `uv` are recorded as needed (z3 comes from the `z3-solver` wheel).
- Python: 3.12 (`requires-python >=3.12`; README uses `uv venv --python=3.12`).
- Pinned versions are in `pyproject.toml` (`[project].dependencies`, the `uv pip freeze` of the run). Direct deps: z3-solver==5.1.0.0, numpy==2.5.3, pandas==3.0.6, scikit-learn==1.9.1, scipy==1.18.1, aiohttp==3.14.3, loguru==0.7.3, nltk==3.10.3, requests==2.34.2, tenacity==9.1.4, psutil==7.2.2, pytest==9.1.1 (transitive pins are listed in the file).
```bash
uv venv .venv --python=3.12
uv pip install --python=.venv/bin/python -r <(python3 -c "import tomllib;print('\n'.join(tomllib.load(open('pyproject.toml','rb'))['project']['dependencies']))")
.venv/bin/python -c "import nltk; nltk.download('wordnet', download_dir='data/nltk_data'); nltk.download('omw-1.4', download_dir='data/nltk_data')"
```
WordNet is required: `src/consensus.py` refuses to run without `data/nltk_data/` (needed by the RENAME rewrite). It is not stored in this folder (40 MB, redownloadable).

## 3. Data, models, keys
- Logic-LM FOLIO-dev outputs of 3 systems and the prompt `FOLIO.txt`: included in `data/logiclm/`.
- Every paid OpenRouter response is cached in `data/peer_raw/` (plus `data/peer_raw_dryrun_v0/`), so the pipeline can be re-run without new spend. Model catalogue: `data/or_models.json`.
- Peer models (6 families, T=0): llama-3.3-70b, qwen3-235b, deepseek-v3.1 (`deepseek/deepseek-chat-v3.1`), mistral-small-3.2, gemini-2.5-flash-lite, gpt-4.1-mini (exact OpenRouter ids are in `src/peers.py`). SC baselines: `openai/gpt-4.1-nano` (K=5, T=0.7) and `openai/gpt-3.5-turbo` (K=5, T=0.7, gpt-3.5 candidates only).
- Env var (name only): `OPENROUTER_API_KEY`, needed only for calls that are not cached (`src/peers.py call`). Spend caps in the code: $8 for optional arms, $9.5 overall. Run with `--skip-api` to use the cache only.
- **External upstream input, not in this folder:** `src/screen.py` and `src/repair_census.py` read the curated DSAVlab-UNIUD FOLIO/MALLS instance files and `folio_refined_validation.csv` from the constant `D` (hard-coded to the sibling run directory `iter_3/gen_hypo/claude_agent/data`), and `src/peers.py` reads `yuan-yang__MALLS-v0__MALLS-v0.1-train.json` (`MALLS_TRAIN`). These are absolute server paths and are NOT published; a reader must supply their own copies of these files and edit `D` / `MALLS_TRAIN` to point to them (the code has not been made relative). The frozen output of that step is in `results/screen_items.json`, `results/units.json` and `results/screen_label_hash.txt` (label hash `0e43cbdd…`), so the later stages (`build`, consensus, analysis) can be checked from those files. `data/repair_census.rows.json` holds the census rows.

## 4. Commands (in the order run)
Full pipeline (`run_all.sh`; equivalent to `.venv/bin/python method.py [--skip-api] [--boot 2000]`):
```bash
bash run_all.sh
```
which executes, with `PYTHONHASHSEED=0`:
1. `.venv/bin/python -m pytest -c /dev/null --rootdir . --noconftest -q tests/test_fol.py`
2. `.venv/bin/python tests/census_regression.py`
3. `.venv/bin/python src/screen.py` (shared screen, labels, hash)
4. `.venv/bin/python src/peers.py call --arm peers --dry-run`, then `call --arm peers`, `call --arm sc_cheap`, `call --arm sc_same`
5. `.venv/bin/python src/peers.py build`
6. `.venv/bin/python src/consensus.py --mini 20`, then `.venv/bin/python src/consensus.py`
7. `.venv/bin/python src/analysis.py --boot 2000` (writes `results/summary.json` and `method_out.json`)
8. `.venv/bin/python tests/audit_rederive.py` (writes `results/audit_rederive.json`)

Seeds: `PYTHONHASHSEED=0`; the bootstrap uses `np.random.default_rng(seed=0)` with 2000 sentence-clustered resamples (`--boot 2000`); placebo permutations use `random.Random(seed)`, seeds 0–19 in `src/analysis.py`, and the audit runs 200 label permutations. LLM sampling seeds are not recorded (SC samples at T=0.7 are reproduced only via the cached responses).
Hardware/runtime: no GPU. README reports z3 on 4 CPUs: 15,265 pairwise eqmv calls in 7 s, 599 medoid repairs in 45 s, 1,575 labels in 205 s (cold run). Total wall-clock and RAM were not recorded. The original run's SC_cheap arm was completed in a second pass after a key limit (see README, deviation 1).

## 5. Expected outputs and numbers
Primary contrast (track L, 297 CORRECT vs 249 ERROR, n=546, cluster bootstrap 2000), from `results/summary.json` / README:
- c_score AUROC 0.866 [0.821, 0.906]; peers-only 0.872; non-OpenAI peers 0.863; other Logic-LM only 0.753; cluster entropy 0.773; medoid depth 0.722; sc5_cheap 0.725 [0.669, 0.781].
- Δ c_score − sc5_cheap = +0.140 [0.085, 0.197]; c_score − sc5_same = +0.140 [0.057, 0.227] (n=167); cross-fitted [c_score, sc5] vs [sc5] = +0.147.
- Vocab-clean subset: c_score 0.852 vs sc5_cheap 0.714. Medoid threshold: recall 0.62, false alarms 0.14. Blind spot 38% of errors (POLARITY 5%, COVERAGE 41%, STRUCT 57%). Operator match 81% (chance 46%). RENAME rewrites: 96% false alarms.
- Cost: total $1.5194 (`logs/cost_log.jsonl`).
- `results/audit_rederive.json` independently reproduces c_score 0.8655, sc5_cheap 0.7254, Δ +0.140, vocab-clean 0.8518, recall 0.6185, false alarms 0.138.
Per-item predictions: `method_out.json` (also `full_`, `mini_`, `preview_method_out.json`). Paper table/figure mapping is not recorded in the workspace; the README headline tables are the reference. Bootstrap CIs, strata, rewrite rates and blind-spot rates are not covered by the independent audit.
