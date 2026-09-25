# gen_demo_art_experiment_5 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `gen_paper_repo_a2e1d024cc16` — Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for Natural Language to First-Order Logic Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_5` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-25 12:45:06 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-25 12:45:12 UTC

````
<conversion_philosophy>
**MINIMAL CHANGES — PRESERVE THE ORIGINAL CODE**

The goal is to make the artifact's code READABLE, UNDERSTANDABLE, and RUNNABLE in a short time
to someone reviewing the research, with the option to easily scale parameters back to original
values for a full run (which can take much longer). Think of this as annotating and reformatting,
not refactoring.

**DO:**
- Split the original script into logical notebook cells (imports, setup, processing, results)
- Add markdown cells BETWEEN code cells explaining what each section does and why
- Add inline comments where the logic is non-obvious
- Add a visualization/summary cell at the end showing key outputs
- Fix hardcoded file paths to use the GitHub data loading pattern

**DO NOT:**
- Rewrite functions or change algorithms
- Rename variables or restructure logic
- Add error handling, type hints, or "improvements" that weren't in the original
- Simplify or "clean up" the original code
- Remove any original comments or logic
- Change the computational approach

The reader should recognize the original script when looking at the notebook — it's the
same code, just split into cells with explanatory markdown between sections.
</conversion_philosophy>

<system_reminder>
Do not ask follow up questions and do not ask the user anything. Execute all steps independently.
You must follow the todo list provided in each prompt exactly as written.
No placeholders, stubs, or incomplete code — all code must be complete and functional.
</system_reminder>

<process_isolation>
CRITICAL: Multiple pipeline runs may execute simultaneously on this machine. `ps aux | grep method.py` matches ALL runs, not just yours.
- NEVER kill processes by name (`killall`, `pkill -f`, `ps aux | grep ... | xargs kill`). This kills OTHER runs' processes.
- NEVER monitor processes by name (`ps aux | grep method.py`). You will see other runs' processes and get confused.
- ALWAYS use PID-based process management:
  Run: `uv run method.py & PID=$!` or `timeout <seconds> uv run method.py & PID=$!`
  Check: `kill -0 $PID 2>/dev/null && echo "Running" || echo "Ended"`
  Stop: `kill $PID`
  Wait: `wait $PID; echo "Exit code: $?"`
  Monitor: `tail -f logs/run.log & TAIL_PID=$!` then `kill $TAIL_PID` when done
</process_isolation>

<workspace>
Your workspace: `/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/`:
GOOD: `/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/file.py`, `/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<disposable_outputs>
A SHARED CACHE ALREADY EXISTS FOR THIS RUN: `/ai-inventor/aii_data/runs/run_qck1d05BqxkX/.shared_cache`
`HF_HOME`, `HF_HUB_CACHE`, `TRANSFORMERS_CACHE`, `HF_DATASETS_CACHE`,
`TORCH_HOME`, `PIP_CACHE_DIR` and `UV_CACHE_DIR` are ALREADY set to point
there. Every step and every iteration of this run shares it, so a model or
dataset an earlier experiment downloaded is already on disk for you.

DO NOT override those variables. In particular do NOT write the common
pattern `os.environ["HF_HOME"] = <workspace>/hf_cache` — `HF_HOME` and
`TRANSFORMERS_CACHE` are read differently by `huggingface_hub` (one has
`/hub` appended, the other does not), so pointing both at one directory
stores every weight TWICE. That mistake cost one run 25 GB of identical
blobs. If you must set them, use the values above verbatim.

YOUR WORKING DIRECTORY IS A DELIVERABLE. When this module ends it must read
like a GitHub repository someone else can fork, resume and run — and the bulk
it holds must be either worth keeping or restorable. This run shares a storage
volume with the database; a run that fills it stops every other run on the box.

So before you finish, produce TWO files:

1. `.aii/manifest.yaml` — one entry per heavy path, each with EXACTLY ONE decision.
   The `.aii/` directory ALREADY EXISTS in your cwd: write the file into
   it. Do not create, replace or `touch` `.aii` itself — a plain file by
   that name makes the manifest unwritable for the rest of the module.

```yaml
entries:
  - path: results/
    keep: six GPU-hours of sweep output, not reproducible inside this run
  - path: hf_cache/
    delete: redownloadable
    source: "huggingface-cli download meta-llama/Llama-3-8B"
  - path: checkpoints/
    delete: regenerable
    source: "uv run train.py --epochs 3 --seed 0"
```

   - `keep:` takes a ONE-LINE reason. Use it for the expensive and the
     irreproducible: trained weights, long-running results, datasets you
     collected yourself.
   - `delete:` takes `redownloadable` (and a `source:` naming the repo id, URL
     or command) or `regenerable` (and a `source:` that is the command which
     rebuilds it). These are deleted AFTER the round ends, never mid-step.
   - Every path is RELATIVE TO YOUR CWD and must resolve INSIDE it. Absolute
     paths, `..`, and anything resolving outside are rejected.
   - Globs and whole directories are fine. A whole `hf_cache/` is ONE entry —
     do not list files individually.

2. `README.md` — written as if your cwd were a GitHub repository: what you
   did, the layout with a line per important file/directory, how to run it,
   and a **"Restoring removed files"** section giving the install/download
   command for EVERY `delete` entry. An `install.sh` or `restore.sh` beside it
   is welcome.

A CHECKER RUNS WHEN YOU SUBMIT. If anything heavy has no decision it fails
your submission and hands you the uncovered list, grouped by directory with
sizes, and you fix the manifest and submit again.

WHAT NEEDS NO DECISION — do not write entries for these:
- text and code files, at ANY size (source, JSON, CSV, YAML, logs, markdown);
- anything under the auto-keep floor (10 MB), whatever it holds.
Only large binaries and cache directories (`hf_cache/`, `.venv/`,
`node_modules/`, `checkpoints/`, `wandb/`, `__pycache__/`, …) need one.

NEVER mark your results, figures, papers, code, logs or anything a later step
reads as `delete`. If a later step needs it, it is a `keep`.

WHAT A `keep` BUYS YOU. Anything you do not mark `delete` stays exactly where
you wrote it, on this run's storage volume, at the path it already has — it is
not moved, renamed or copied. A later round reads it there, by that absolute
workspace path, so a checkpoint you keep is a checkpoint the next round can
load instead of retraining. It is also the ONLY copy: the publish step pushes
your cwd to GitHub but skips every file of 100 MB or
more, so trained weights and large binary artifacts never leave the volume.
Name each kept artifact in your results and your `README.md` by its path
RELATIVE to your cwd, and say it stays on the run's volume rather than in the
published repository. Never write an absolute server path into a file that is
published: a reader's machine has none of them.
</disposable_outputs>

<tool_use>
Maximize parallel tool calls. Parallelize independent operations, only sequentialize dependencies.
- Multiple searches/fetches on different topics → parallel in one turn
- Search then fetch results → sequential (need URLs first)
</tool_use>

<task>
Convert this artifact's Python script into a demo notebook with MINIMAL changes to the original code.
Split into cells, add markdown explanations between sections, add a visualization cell at the end.
Output: mini_demo_data.json + code_demo.ipynb (notebook that loads data from GitHub URL)
</task>

<artifact_info>
id: art_7GxreYjATkC5
type: experiment
title: Peer agreement vs paid AI judges on held-out logic
summary: >-
  T1 head-on test on held-out NL->FOL dataset E (8,507 real candidates, 700 sentences). The frozen peer-agreement consensus
  metric (c_score_align, exp 5) and PEER+TEXT fusion (p_peer_text) are compared with newly scored paid API comparators: gemini-2.5-flash-lite
  rubric-A JSON judge (disguised + original, every parseable row), gpt-4.1-nano P(YES) judge (both views), gemini-3.1-pro-preview
  frontier judge (original view, 284-row frame; disguised view blocked by the pre-registered shared-key reserve rule), API
  round trip (flash-lite verbaliser -> DeBERTa NLI/mpnet) and API SC-5 (nano, T=0.7, z3 modulo vocabulary); plus S4_full,
  a cross-fitted stack of all 28 baselines. Pre-registered in prereg_T1.json (sha256 c2a6cf84, frozen before any sweep score).
  Main population R_AB E_POOL PRIMARY n=2,686 (1,822 ERROR/864 CORRECT, 292 sentences); sentence-cluster bootstrap B=2000.
  RESULTS: stratified AUROC c_score_align 0.741 vs flash-lite disguised 0.642 (pooled 0.782 vs 0.696). (a) CONFIRMED: strat
  dAUROC +0.099 [0.049,0.146]; long pool +0.116 [0.070,0.163]; R_A L20+EXC +0.299; also vs best cheap judge (nano orig) +0.089
  [0.043,0.134]. (b) CONFIRMED: nested [S4_full+c]-S4_full strat +0.039 [0.021,0.057], permutation-null p95 0.009; c alone
  ~= S4_full (+0.006 [-0.031,0.042]). (d) CONFIRMED: frame ratio vs frontier 0.957 [0.887,1.034], consensus $1.2e-4 vs frontier
  $3.65e-3/item, nested frame gain +0.037 [0.008,0.066]. VEX aligner-confound control CONFIRMED: +0.306 [0.232,0.376]. M3
  (smaller length slope than the judge) DISCONFIRMED: +0.146 [-0.051,0.361]. Overall T1 (this artifact): CONFIRMED. Caveats:
  no advantage on the short FOLIO CTRL stratum (-0.069 [-0.23,0.10]) or on <12-word / <=1-condition sentences; the advantage
  concentrates in long, conditioned, exception sentences (EXC +0.197). Consensus misses aligner-masked MEANING_RENAME errors
  (recall 0.07 at FA 0.10 vs judges 0.13-0.20) and peer-endorsed errors (0.00). Flash-lite contamination DiD +0.105 [0.006,0.201]
  (MDE 0.14). Test-retest Spearman 0.975. API spend $2.395 (cap $4.60). Independent checks: tests/audit_T1.py (5 headline
  numbers match to 1e-3) and tests/audit_raw_T1.py (raw files -> identical confirmatory/long-pool delta and frame ratio; placebos
  fail as required). Files: results/analysis_T1.json, verdict_T1.json, tables_T1.md, per_item_T1.jsonl, deviations.json, api_cost_ledger.json,
  llm_cache.jsonl; figures/forest_T1, complexity_curves; full_method_out.json (predict_* oriented scores for every metric).
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
- reproducibility.md
out_demo_files:
- path: method.py
  description: Research methodology implementation
</artifact_info>

<github_repo>
Repo URL: https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-3/experiment-6/demo/mini_demo_data.json

URLs won't work yet — files pushed to GitHub AFTER notebook creation.
Use local fallback pattern so notebook works locally (now) and in Colab (after deployment).
</github_repo>

<data_file_sizes>
Data files come in three sizes:
- preview_*_out.json — READ THIS to inspect the data structure
- mini_*_out.json (~3 examples) — use for prototyping/testing
- full_*_out.json (complete) — use for the final production run. NEVER open it directly (too large to read into context). Instead, extract values programmatically with shell commands (e.g. grep) or a Python script (use aii-long-running-tasks skill for scripts).
</data_file_sizes>

<install_dependencies_pattern>
Follow the aii-colab skill exactly. It has the install cell pattern, pre-installed package list, numpy 2.0 compat shims, and all Colab-specific rules.
</install_dependencies_pattern>

<data_loading_pattern>
`mini_demo_data.json` = curated subset for the demo.
Use this pattern for Colab compatibility (GitHub URL with local fallback):
```python
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-3/experiment-6/demo/mini_demo_data.json"
import json
from pathlib import Path

def load_data():
    try:
        import urllib.request
        with urllib.request.urlopen(GITHUB_DATA_URL) as response:
            return json.loads(response.read().decode())
    except Exception: pass
    local = Path("mini_demo_data.json")
    if local.exists(): return json.loads(local.read_text())
    raise FileNotFoundError("Could not load mini_demo_data.json")
```
</data_loading_pattern>

<notebook_structure>
--- Setup ---
Cell 1 (markdown): Title, description, what this artifact does.
Cell 2 (code): Install dependencies — follow the aii-colab skill's install cell pattern exactly. Fill in all packages imported by the artifact's code.
Cell 3 (code): Imports — copy original import block as-is, plus any additional imports needed for the notebook (e.g. matplotlib for visualization).
Cell 4 (code): Data loading helper — use the <data_loading_pattern> above.
Cell 5 (code): `data = load_data()`

--- Config ---
Config cell (code): Define ALL tunable parameters (iterations, epochs, n_samples, hidden_size, etc.) as variables at the top of this cell. Start with the ABSOLUTE MINIMUM values — the smallest that produce any output at all (e.g. 1 iteration, 2 samples, smallest array size). These get gradually increased during testing — see TODOs.

--- Processing ---
Remaining cells: One code cell per logical section of the original script. Add a markdown cell BEFORE each code cell. Copy code as closely as possible, with these changes:
  1. Replace file paths to use the loaded `data` variable.
  2. Use the config variables from the config cell (NOT hardcoded values).
  3. Minimal fixes are allowed if something doesn't work in notebook context (e.g. adjusting paths, removing CLI args, fixing imports), but keep changes to the absolute minimum.

--- Results ---
Visualization cell (code): Print key results in a readable table, plot numeric data with matplotlib if appropriate.
</notebook_structure>

<priority>
WORKING > OPTIMIZED. A small-scale demo that runs correctly is the goal. Once the notebook passes with minimum config values, scale up only if time permits — do NOT spend multiple retries chasing larger parameters. If a working version exists, finish and move on.
</priority>

<max_notebook_total_runtime>600s (10 min)</max_notebook_total_runtime>

<test_environment>
To test-run the notebook in a clean environment (simulating Colab), use the disposable venv at `/tmp/aii_nb_test_envs/art_7GxreYjATkC5-321ae79c96cc`. It is on this machine's local disk, outside your workspace, which is on a slow network volume: never create a venv inside your workspace.
```bash
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_7GxreYjATkC5-321ae79c96cc
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_7GxreYjATkC5-321ae79c96cc/bin/python jupyter ipykernel
/tmp/aii_nb_test_envs/art_7GxreYjATkC5-321ae79c96cc/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
```
The timeout is set to <max_notebook_total_runtime>. The entire notebook must finish within this time.
`UV_VENV_CLEAR=1` recreates the venv empty at the start of every test, so each test starts clean. Do NOT delete it yourself: the pipeline removes it after you finish. If you run a test in the background, wait for its result before starting the next test.

What happens: the venv starts with only pip, jupyter and ipykernel. When the notebook's install cell runs, `google.colab` is NOT in sys.modules, so ALL packages get installed — non-Colab packages unconditionally, and Colab packages (numpy, pandas, etc.) at Colab's exact versions via the guard block. The result mirrors Colab's environment as closely as possible. If a cell fails, fix the notebook and re-run.
</test_environment>

FIRST, add ALL of these to your todo list using your task/todo-tracking tool:

CRITICAL: Todo content must be copied exactly as is written here, with NO CHANGES. These todos are intentionally detailed so that another LLM could read each one without any external context and understand exactly what it has to do.


<todos>
TODO 1. Read and STRICTLY follow these skills: aii-colab, aii-long-running-tasks.
TODO 2. Read demo file and relevant preview_* files (preview only). Understand script structure: imports, setup, processing, output. Identify ALL tunable parameters (iterations, epochs, n_samples, hidden_size, batch_size, etc.) — these go in the config cell.
TODO 3. Create `mini_demo_data.json`: curated subset from at most ONE dataset (no more than 100 diverse examples). CRITICAL: do NOT read/grep full output file — may crash. Use `head -c 5000` or stream first entries with Python to pick examples.
TODO 4. Create `code_demo.ipynb` via NotebookEdit following <notebook_structure>. Set ALL config parameters to ABSOLUTE MINIMUM values — the smallest that produce any output (e.g. 1 iteration, 2 samples, smallest array sizes). Test-run using <test_environment>. Fix all errors until it passes.
TODO 5. GRADUALLY SCALE (but don't overdo it): increase config params step by step (e.g. ~2x each round). After each increase: test-run, record runtime, fix errors. STOP SCALING as soon as results look meaningful — a working small-scale demo beats a failed large-scale one. If full original params fit within <max_notebook_total_runtime> (10% margin), use them. Otherwise keep whatever works and comment out the true original values. Do NOT spend more than 2-3 scaling rounds.
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-3/experiment-6/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
</todos>

---

Output the result as JSON to: `./.terminal_claude_agent_struct_out.json`

JSON Schema:
```json
{
  "$defs": {
    "DemoExpectedFiles": {
      "description": "Expected output files from code demo notebook generation.",
      "properties": {
        "notebook": {
          "default": "",
          "description": "Path to the generated demo notebook. Example: 'code_demo.ipynb'",
          "title": "Notebook",
          "type": "string"
        },
        "mini_data_file": {
          "default": "",
          "description": "Path to the mini demo data JSON (curated subset). Example: 'mini_demo_data.json'",
          "title": "Mini Data File",
          "type": "string"
        }
      },
      "title": "DemoExpectedFiles",
      "type": "object"
    }
  },
  "description": "Dataset/experiment/evaluation \u2192 Jupyter notebook demo.\n\nTitle and summary come from the parent artifact (gen_art step),\nnot from the demo agent. The agent only outputs expected files.",
  "properties": {
    "out_expected_files": {
      "$ref": "#/$defs/DemoExpectedFiles",
      "description": "All output files you created. Must include the demo notebook."
    }
  },
  "required": [],
  "title": "CodeDemo",
  "type": "object"
}
```

IMPORTANT: this task is NOT complete until `./.terminal_claude_agent_struct_out.json` exists and contains JSON matching the schema above.
````

### [3] HUMAN-USER prompt · 2026-09-25 12:45:12 UTC

```
I work on converting natural-language text into first-order logic (NL→FOL, autoformalization) with
LLM pipelines. Evaluation is the bottleneck. Correct FOL for a sentence is not unique — different
predicate names, different decompositions of the same concept, and logically equivalent rewrites can
all be correct. Gold FOL annotations are rare and expensive. The metrics in use either need a gold
formula (exact match, BLEU, prover-checked equivalence to the gold) or only check that the output
parses. In my own pilot I used cheap structural metrics: whether a set of generated formulas loads
together without conflicts, whether predicate arities stay consistent, how many predicates are used
but never defined, and how similar the predicate sets are across reruns. Those measure stability and
composability, not whether a formula says what the sentence says.

Find new metrics for NL→FOL output quality. Operating situation: you are given a natural-language
sentence (or short passage) and a candidate FOL formalization produced by any system. There is no gold
formula, no ontology or controlled vocabulary, and no domain knowledge. The metric returns a score
that predicts whether the formalization is faithful to the text, and ideally which kind of error it
contains (quantifier or scope error, dropped or added condition, negation/polarity error, swapped
arguments, conflated or wrongly split concepts). Metrics may score a single formula or a set (several
samples for one sentence, or the formalizations of all sentences in one document). They must be
task-agnostic — usable for any NL→FOL setting, not tied to a domain, dataset or pipeline — and cheap
enough to run on every output (solver calls and small models are fine; a large-LLM judge per formula
only if shown to earn its cost).

Requirements:
- Keep the target fixed: the metric must predict faithfulness to the text. Detecting synthetic
  perturbations, parse validity, or run-to-run stability are not substitutes for that target.
- Validate against ground truth, never against the metric itself. Use public datasets with gold
  sentence-level FOL (e.g. FOLIO, MALLS, or others you find) to build a meta-evaluation set: real
  candidate formalizations from several different systems, plus controlled perturbations of gold
  formulas with known error types, labelled via prover-checked equivalence to gold. Handle two known
  problems: some gold annotations are wrong, and a candidate can be correct without being equivalent
  to the gold (different vocabulary or granularity). Estimate how often each happens and how it
  biases the labels. These datasets are public, so check whether LLM-based metrics benefit from having
  seen the gold.
- For each metric report: correlation with correctness at item and system level; sensitivity per error
  type; invariance under meaning-preserving rewrites (variable/predicate renaming, reordering,
  equivalent restatements); coverage — unparseable outputs are counted and reported, never silently
  dropped; and cost.
- Compare against baselines: parse/compile rate, round-trip (FOL→NL→compare) similarity,
  LLM-as-judge, sampling self-consistency, and the structural consistency metrics described above. A
  new metric matters only if it adds signal those don't.
- Report how each metric's reliability changes with sentence complexity (length, number of quantifiers,
  nesting depth, number of conditions and exceptions). Long, heavily conditioned sentences matter most
  to me.
- Negative results are welcome: if a family of metrics does not track correctness, show that clearly.

Out of scope: comparing grounded vs ungrounded generation (ontology vocabulary injected into prompts),
anything that depends on a particular ontology, and building a better NL→FOL translator. The
contribution is the measurement, not the translator.

Deliverables: reusable Python functions taking (text, fol) — or a set of such pairs — each with a
precise statement of what it measures; the meta-evaluation dataset with its labels; and the results.

I appended a pilot study of this problem with some metrics I already used but haven't verified. Just for reference.
```

### [4] TOOL CALL — Skill · 2026-09-25 12:45:20 UTC

```
aii-colab
```

### [5] TOOL RESULT — Skill · 2026-09-25 12:45:20 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [6] TOOL CALL — Skill · 2026-09-25 12:45:20 UTC

```
aii-long-running-tasks
```

### [7] TOOL RESULT — Skill · 2026-09-25 12:45:20 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [8] TOOL CALL — Bash · 2026-09-25 12:45:20 UTC

```
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5; ls -la; ls -la .aii; W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6; ls -la $W; wc -l $W/method.py; ls -la $W/results $W/figures 2>/dev/null | head -50
```

### [9] TOOL RESULT — Bash · 2026-09-25 12:45:20 UTC

```
{"stdout": "total 1988\ndrwxr-xr-x 3 root root 1002768 Sep 25 12:45 .\ndrwxr-xr-x 3 root root 1002768 Sep 25 12:44 ..\ndrwxr-xr-x 2 root root       1 Sep 25 12:44 .aii\n-rw------- 1 root root      54 Sep 25 12:45 .aii_claude_session.json\n-rw-r--r-- 1 root root   28490 Sep 25 12:45 .repl_agent.ptylog\ntotal 980\ndrwxr-xr-x 2 root root       1 Sep 25 12:44 .\ndrwxr-xr-x 3 root root 1002768 Sep 25 12:45 ..\ntotal 65956\ndrwxr-xr-x 9 231072 231072  2035293 Sep 24 06:54 .\ndrwxr-xr-x 7 root   root    3000107 Sep 24 01:33 ..\ndrwxr-xr-x 2 root   root      47000 Sep 24 04:02 .aii\n-rw------- 1 165536 165536       54 Sep 24 03:19 .aii_claude_session.json\n-rw-r--r-- 1 231072 231072  4977101 Sep 24 03:31 .aii_cost_ledger.jsonl\n-rw------- 1 165536 165536    10946 Sep 24 04:02 .aii_worker_result.json\n-rw-r--r-- 1 231072 231072  1011052 Sep 24 04:02 .repl_agent.ptylog\n-rw-r--r-- 1 165536 165536     3096 Sep 24 03:58 .terminal_claude_agent_struct_out.json\n-rw-rw-rw- 1 165536 165536    14582 Sep 24 04:00 README.md\n-rwxrwxrwx 1 231072 231072     1357 Sep 24 01:36 api_chain.sh\ndrwxr-xr-x 7 231072 231072  2021521 Sep 24 01:51 data\ndrwxr-xr-x 2 165536 165536  1033052 Sep 24 03:46 figures\n-rwxrwxrwx 1 231072 231072      819 Sep 23 20:38 finalize.sh\n-rw-r--r-- 1 165536 165536 26303294 Sep 24 03:54 full_method_out.json\n-rwxrwxrwx 1 231072 231072      583 Sep 23 18:42 gpu_pipeline.sh\n-rwxrwxrwx 1 231072 231072      515 Sep 23 19:39 gpu_pipeline2.sh\n-rwxrwxrwx 1 231072 231072      409 Sep 24 01:36 key_poll.sh\ndrwxr-xr-x 2 231072 231072  2001012 Sep 24 03:57 logs\n-rw-rw-rw- 1 231072 231072   161649 Sep 24 02:00 method.py\n-rw-r--r-- 1 165536 165536 20790698 Sep 24 03:54 method_out.json\n-rw-r--r-- 1 165536 165536     9243 Sep 24 03:54 mini_method_out.json\n-rw-r--r-- 1 231072 231072    11115 Sep 24 01:54 prereg_T1.json\n-rw-r--r-- 1 231072 231072      110 Sep 24 01:54 prereg_T1.sha256\n-rw-rw-rw- 1 231072 231072     1734 Sep 23 19:35 prereg_b2.json\n-rw-rw-rw- 1 231072 231072       81 Sep 23 19:35 prereg_b2.sha256\n-rw-rw-rw- 1 231072 231072    14694 Sep 23 18:02 prereg_baselines.json\n-rw-rw-rw- 1 231072 231072       88 Sep 23 18:02 prereg_baselines.sha256\n-rw-r--r-- 1 165536 165536     9086 Sep 24 03:54 preview_method_out.json\n-rw-rw-rw- 1 231072 231072     4152 Sep 24 03:56 pyproject.toml\n-rw-r--r-- 1 165536 165536     7981 Sep 24 03:58 reproducibility.md\n-rw-rw-rw- 1 165536 165536      654 Sep 24 03:51 requirements.txt\n-rwxrwxrwx 1 231072 231072     1168 Sep 23 19:43 restore.sh\ndrwxr-xr-x 5 231072 231072  2007597 Sep 24 03:57 results\n-rw-rw-rw- 1 231072 231072      912 Sep 23 18:03 scripts_download.py\ndrwxrwxrwx 4 231072 231072  1041591 Sep 25 11:07 src\n-rwxrwxrwx 1 231072 231072     1311 Sep 24 01:54 t1_api_chain.sh\ndrwxrwxrwx 2 231072 231072  1002894 Sep 24 03:57 tests\n2701 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/method.py\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/figures:\ntotal 3329\ndrwxr-xr-x 2 165536 165536 1033052 Sep 24 03:46 .\ndrwxr-xr-x 9 231072 231072 2035293 Sep 24 06:54 ..\n-rw-r--r-- 1 165536 165536   25837 Sep 24 03:47 complexity_curves.pdf\n-rw-r--r-- 1 165536 165536  132129 Sep 24 03:47 complexity_curves.png\n-rw-r--r-- 1 165536 165536   23480 Sep 24 03:47 forest_T1.pdf\n-rw-r--r-- 1 165536 165536  157012 Sep 24 03:47 forest_T1.png\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6/results:\ntotal 67381\ndrwxr-xr-x 5 231072 231072  2007597 Sep 24 03:57 .\ndrwxr-xr-x 9 231072 231072  2035293 Sep 24 06:54 ..\n-rw-r--r-- 1 165536 165536   590258 Sep 24 03:47 analysis_T1.json\n-rw-r--r-- 1 165536 165536     2261 Sep 24 03:46 api_cost_ledger.json\n-rw-r--r-- 1 165536 165536     1309 Sep 24 03:48 audit_T1.json\n-rw-r--r-- 1 165536 165536     1472 Sep 24 03:57 audit_raw_T1.json\n-rw-r--r-- 1 231072 231072      337 Sep 24 03:46 budget_state.json\n-rw-r--r-- 1 231072 231072  7702995 Sep 24 03:31 costs.jsonl\n-rw-r--r-- 1 165536 165536     4440 Sep 24 03:58 deviations.json\n-rw-r--r-- 1 231072 231072      239 Sep 24 03:37 key_usage_log.json\n-rw-r--r-- 1 231072 231072 22130531 Sep 24 03:31 llm_cache.jsonl\n-rw-r--r-- 1 165536 165536 21937774 Sep 24 03:46 per_item_T1.jsonl\ndrwxr-xr-x 2 231072 231072  1004318 Sep 24 01:53 pilot\n-rw-r--r-- 1 231072 231072   119798 Sep 24 01:52 prices.json\n-rw-r--r-- 1 231072 231072     4333 Sep 24 01:52 repro_gates.json\n-rw-r--r-- 1 165536 165536      190 Sep 24 03:37 roundtrip_meta_api.json\n-rw-r--r-- 1 231072 231072    86177 Sep 24 03:41 s4_full_coefs.json\n-rw-r--r-- 1 165536 165536      122 Sep 24 03:32 sc5_score_meta.json\n-rw-r--r-- 1 165536 165536  9321938 Sep 24 03:32 sc_pair_cache_sc5_samples.jsonl\ndrwxr-xr-x 2 231072 231072  2001685 Sep 24 03:37 scores\ndrwxr-xr-x 2 231072 231072        1 Sep 24 01:50 tables\n-rw-r--r-- 1 165536 165536    33205 Sep 24 03:46 tables_T1.md\n-rw-r--r-- 1 165536 165536     2709 Sep 24 03:46 verdict_T1.json\n-rw-r--r-- 1 231072 231072     2794 Sep 24 01:51 vex_declaration.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [10] TOOL CALL — Bash · 2026-09-25 12:45:24 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6; cd $W; grep -n "^def \|^class \|^[A-Z_]* = \|^import\|^from\|^if __name__\|^# ===\|^@" method.py | head -300; cat preview_method_out.json | head -c 4000; echo; cat reproducibility.md | head -80
```

### [11] TOOL RESULT — Bash · 2026-09-25 12:45:24 UTC

````
{"stdout": "28:from __future__ import annotations\n30:import argparse\n31:import asyncio\n32:import hashlib\n33:import json\n34:import math\n35:import os\n36:import sys\n37:import time\n38:from collections import Counter, defaultdict\n39:from pathlib import Path\n46:from loguru import logger  # noqa: E402\n48:from src.common import DATA, LOGS, RES, ROOT, detect_cpus, jdump, jload, norm, read_jsonl, sha1, set_ram_limit  # noqa: E402\n54:NUM_CPUS = detect_cpus()\n55:WORKERS = max(1, min(12, NUM_CPUS - 2))\n58:SCORES = Path(os.environ[\"T1_SCORES_DIR\"]) if os.environ.get(\"T1_SCORES_DIR\") else RES / \"scores\"\n60:EXPD = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_4\")\n61:EXPA = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_1\")\n62:EXPC = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3\")\n63:PREREG = ROOT / \"prereg_baselines.json\"\n64:PREREG_SHA = ROOT / \"prereg_baselines.sha256\"\n65:FEWSHOT = json.loads((Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_dataset_1\")\n70:def append_jsonl(p: Path, rows: list[dict]) -> None:\n76:def load_scores(name: str) -> dict:\n86:def units() -> list[dict]:\n90:def prereg() -> dict:\n96:def require_frozen() -> dict:\n104:# =====================================================================================================================\n105:def _prep_worker(args):\n113:def strict_parse_ok(fol) -> bool:\n127:def _disg_worker(chunk):\n142:def stage_prep():\n204:# =====================================================================================================================\n205:FEATS = {\n219:STRONG = {\"model\": \"google/gemini-3.1-pro-preview\", \"extra\": {\"reasoning\": {\"effort\": \"low\"}}, \"max_tokens\": 4000}\n220:SC_MODEL = \"openai/gpt-4.1-nano\"\n224:def stage_prereg():\n332:def stage_frame():\n393:# =====================================================================================================================\n394:def _judge_units(limit, pools=(\"E_POOL\", \"GOLDSYS\", \"CCG\")):\n405:def _dedup(pairs):\n415:def stage_judges(limit=None, which=(\"cheap_disg\", \"cheap2_disg\", \"cheap_orig\", \"cheap2_orig\")):\n457:# =====================================================================================================================\n458:def _sc_messages(text):\n485:def stage_sc_gen(limit=None):\n520:# =====================================================================================================================\n521:def stage_verbalise(limit=None):\n552:# =====================================================================================================================\n553:def _strong_params() -> dict:\n565:def strong_order(which=(\"orig\", \"disg\")) -> list[tuple[str, str]]:\n588:def stage_strong(limit=None, which=(\"orig\", \"disg\")):\n638:def stage_retest(limit=None):\n675:# =====================================================================================================================\n676:def _pilot_docs(U):\n690:def stage_cpu():\n759:# =====================================================================================================================\n760:def _sc_pair_worker(chunk):\n776:def stage_sc_score(which=(\"sc5_local_samples\",)):\n781:def _sc_score(samples_name=\"sc5_samples\"):\n848:# =====================================================================================================================\n856:def _prereg_local():\n860:def _msgs_json(rub, ut, text, fol):\n865:def _local_json_judge(lm, units_, rub, ut, tag, max_new_tokens=150, bs=64):\n887:def stage_local_judges(limit=None, which=(\"qwen8b_disg\", \"qwen8b_orig\", \"llama8b_disg\", \"llama8b_orig\")):\n923:def stage_local_strong(limit=None):\n946:def stage_local_verb(limit=None):\n973:def stage_local_sc(limit=None):\n1000:# =====================================================================================================================\n1005:def b2_sets() -> dict[str, list[dict]]:\n1034:def _b2_build_worker(chunk):\n1049:def stage_b2_build():\n1084:def _b2_units(name, sets=None, limit=None):\n1094:def b2_dev_keys():\n1099:def _b2_read_local(lm, jobs, variant, max_new_tokens=160):\n1106:def stage_b2_read(limit=None, which=(\"dev\",)):\n1177:def _gate_metrics(U, outs):\n1195:# =====================================================================================================================\n1196:def stage_nli(limit=None, which=(\"local\", \"api\")):\n1242:# =====================================================================================================================\n1244:BOUNDED = 1.0\n1247:def _judge_cols(name, fname, conds=(\"orig\", \"disg\"), subset=None):\n1274:def build_columns():\n1419:def stage_s4():\n1441:# =====================================================================================================================\n1442:def stage_b2_gate_report(which=(\"b2\",)):\n1447:def _b2_gate_report(prefix=\"b2\"):\n1516:def stage_sc_invariance():\n1557:# =====================================================================================================================\n1563:SC_API = [\"sc5_eq_frac\", \"sc5_entropy\"]\n1564:SC_LOCAL = [\"sc5_local_eq_frac\", \"sc5_local_entropy\"]\n1567:def stage_analysis():\n1782:def invariance_table(thr):\n1813:def b2_report(kP, yP, types, T, thr, dropped):\n1864:# =====================================================================================================================\n1865:def write_tables(A):\n1914:def write_method_out(T, s4cols, regimes, full):\n1958:# =====================================================================================================================\n1959:def stage_t2_repro():\n1992:# =====================================================================================================================\n1993:def write_summary(A):\n2048:AE_STRATA = [\"L25\", \"L20\", \"EXC\", \"CTRL\"]\n2051:# =====================================================================================================================\n2052:def stage_b2_think(limit=None, which=(\"gate\", \"screen\")):\n2120:# =====================================================================================================================\n2121:def stage_retest_sibling():\n2153:# =====================================================================================================================\n2154:def stage_b2_read_api(limit=None, which=(\"dev\", \"gate\", \"screen\", \"rewrites\", \"Eref\", \"E\")):\n2207:# =====================================================================================================================\n2209:# =====================================================================================================================\n2215:EXPC_CONS = EXPC / \"src\" / \"consensus.py\"\n2218:def _t0_unit_tests() -> dict:\n2278:def stage_t1_prep():\n2433:def _key_status() -> dict:\n2443:def stage_t1_pilot():\n2517:def _unique_pairs(view: str) -> int:\n2524:def stage_t1_freeze():\n2655:def stage_t1_analysis(which=(\"full\",)):\n2678:def main():\n2700:if __name__ == \"__main__\":\n{\n  \"metadata\": {\n    \"method_name\": \"T1 head-on API bar on held-out dataset E\",\n    \"description\": \"Oriented scores (higher = more likely unfaithful): frozen consensus metrics (exp 5), the new API judges (flash-lite / gpt-4.1-nano, original + disguised; gemini-3.1-pro-preview on the frame), API roun...\",\n    \"prereg_T1_sha256\": \"c2a6cf845afc4286884ed702c5be34bc5b31ac06820276e1f913a0fa7432d3a5\",\n    \"verdict\": \"CONFIRMED\"\n  },\n  \"datasets\": [\n    {\n      \"dataset\": \"E_heldout_T1\",\n      \"examples\": [\n        {\n          \"input\": \"{\\\"text\\\": \\\"When something is depressing, it is sad.\\\", \\\"candidate_fol\\\": \\\"\\\", \\\"system\\\": \\\"ccg2lambda\\\", \\\"prompt_variant\\\": \\\"none\\\"}\",\n          \"output\": \"UNPARSEABLE\",\n          \"predict_c_score_align\": \"1.000000\",\n          \"predict_g_score\": \"1.000000\",\n          \"predict_nf_c_score\": \"1.000000\",\n          \"predict_nf_g_score\": \"1.000000\",\n          \"predict_p_peer_text\": \"1.000000\",\n          \"predict_p_text\": \"1.000000\",\n          \"predict_l2_bow\": \"1.000000\",\n          \"predict_l3_z3\": \"1.000000\",\n          \"predict_judge_cheap_disg\": \"1.000000\",\n          \"predict_judge_cheap_orig\": \"1.000000\",\n          \"predict_judge_cheap2_disg\": \"1.000000\",\n          \"predict_judge_cheap2_orig\": \"1.000000\",\n          \"predict_judge_strong_orig\": \"NA\",\n          \"predict_judge_strong_disg\": \"NA\",\n          \"predict_judge_cheap_disg_vfb\": \"1.000000\",\n          \"predict_rt_nli_min\": \"1.000000\",\n          \"predict_rt_nli_fwd\": \"1.000000\",\n          \"predict_rt_nli_bwd\": \"1.000000\",\n          \"predict_rt_nli_contra\": \"1.000000\",\n          \"predict_rt_nli_min_alt\": \"1.000000\",\n          \"predict_rt_embed_cos\": \"1.000000\",\n          \"predict_sc5_eq_frac\": \"1.000000\",\n          \"predict_sc5_entropy\": \"1.791759\",\n          \"predict_S4_full_oof\": \"NA\",\n          \"predict_S4_local_oof\": \"NA\",\n          \"predict_S4_full_plus_c_score_align_oof\": \"NA\",\n          \"predict_PT_refit_oof\": \"NA\",\n          \"predict_PT_refit_NF_oof\": \"NA\",\n          \"predict_local_judge_local_qwen8b_disg\": \"1.000000\",\n          \"predict_local_judge_local_qwen8b_orig\": \"1.000000\",\n          \"predict_local_judge_local_llama8b_disg\": \"1.000000\",\n          \"predict_local_rt_nli_min_local\": \"1.000000\",\n          \"predict_local_sc5_local_eq_frac\": \"1.000000\",\n          \"predict_local_parse_fail\": \"1.000000\",\n          \"predict_local_pilot_rerun_jacc\": \"1.000000\",\n          \"metadata_canonical_key\": \"31452c4db10ee367|none\",\n          \"metadata_exp6_row_key\": \"31452c4db10ee367\",\n          \"metadata_item_id\": \"31452c4db10ee367\",\n          \"metadata_sentence_id\": \"0000c2274e80\",\n          \"metadata_fold_E\": 1,\n          \"metadata_pool\": \"CCG\",\n          \"metadata_parse_ok\": false,\n          \"metadata_sysvar\": \"ccg2lambda|none\",\n          \"metadata_family\": \"symbolic\",\n          \"metadata_strata\": {\n            \"words\": 7,\n            \"n_quant\": 1,\n            \"depth\": 1,\n            \"n_conditions\": 1,\n            \"text_conditions\": 1,\n            \"exception_type\": null,\n            \"source_stratum\": \"CTRL\",\n            \"ctrl_len_bin\": \"0-11\",\n            \"l25_topup_batch\": false\n          },\n          \"metadata_label_tier\": \"-\",\n          \"metadata_in_R_AB\": false,\n          \"metadata_in_R_A\": false,\n          \"metadata_vex\": false\n        },\n        {\n          \"input\": \"{\\\"text\\\": \\\"When something is depressing, it is sad.\\\", \\\"candidate_fol\\\": \\\"∀x (Depressing(x) → Sad(x))\\\", \\\"system\\\": \\\"F:openai/gpt-5.1\\\", \\\"prompt_variant\\\": \\\"fewshot_v1\\\"}\",\n          \"output\": \"CORRECT\",\n          \"predict_c_score_align\": \"0.090909\",\n          \"predict_g_score\": \"0.047619\",\n          \"predict_nf_c_score\": \"0.090909\",\n          \"predict_nf_g_score\": \"0.047619\",\n          \"predict_p_peer_text\": \"0.090350\",\n          \"predict_p_text\": \"0.367667\",\n          \"predict_l2_bow\": \"0.000000\",\n          \"predict_l3_z3\": \"0.333333\",\n          \"predict_judge_cheap_disg\": \"0.000000\",\n          \"predict_judge_cheap_orig\": \"0.000000\",\n          \"predict_judge_cheap\n# Reproducing T1 (consensus vs paid LLM judges on held-out dataset E)\n\nThis file records what was **actually run** on 2026-09-24, from 01:35 to 03:56 UTC. That run was interrupted twice by\nplatform restarts. Every stage is cached and idempotent, so re-runs resumed where they stopped; see\n`results/deviations.json` D1 and D2.\n\n## 1. Copy the artifact\n\n```bash\ncp -r /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6 ~/t1\ncd ~/t1\n```\n\nThe workspace is self-contained. `data/` holds every frozen input, copied from earlier artifacts:\n- the label-free units `data/E_units.json`;\n- exp 5's frozen consensus scores `data/exp5/per_item_E.jsonl`;\n- exp 6's local baselines `data/exp6_*`;\n- `data/folds_E.json` and `data/frontier_frame.json`.\n\nThe labels come from dataset E. The code reads it from its original path, shown below; to use it elsewhere, copy the\nfile and edit `src/e_pool.py`'s path and the `E_FULL` constant in `tests/audit_raw_T1.py`:\n`/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_dataset_1/full_data_out.json`\n\n## 2. System, Python, environment\n\nThese are the versions actually used:\n- Ubuntu (container);\n- Python 3.12.14;\n- uv 0.6.14;\n- NVIDIA driver 580.159.04.\n\n```bash\nbash restore.sh venv    # = uv venv .venv --python=3.12 ; uv pip install -r requirements.txt ;\n                        #   uv pip install torch==2.11.0 --index-url https://download.pytorch.org/whl/cu128 --reinstall-package torch\nuv pip install --python .venv/bin/python matplotlib==3.11.2   # figures (now also listed in requirements.txt)\nbash restore.sh nltk    # WordNet / omw-1.4 / words into data/nltk_data (disguise + VEX lemmatisation)\n```\n\n`pyproject.toml` pins all 132 packages at the exact versions in `.venv` (from `uv pip freeze`, also saved as\n`logs/pip_freeze.txt`). Key versions:\n\n| package | version |\n|---|---|\n| torch | 2.11.0+cu128 |\n| numpy | 2.5.3 |\n| scikit-learn | 1.9.1 |\n| scipy | 1.18.1 |\n| statsmodels | 0.15.0 |\n| transformers | 5.17.0 |\n| sentence-transformers | 6.1.0 |\n| z3-solver | 5.1.0.0 |\n| aiohttp | 3.14.3 |\n| matplotlib | 3.11.2 |\n\nAlternatively, `uv sync` uses the pyproject, with the cu128 index already declared.\n\n## 3. Models, data and environment variables (names only)\n\n- **Environment variables:**\n  - `OPENROUTER_BASE_URL` and `OPENROUTER_API_KEY`: every LLM call goes through `src/budget.py` to that base URL.\n  - `PYTHONHASHSEED=0`.\n  - `HF_HOME` / `HF_HUB_CACHE`: the run's shared cache.\n- **Local weights**, downloaded by `scripts_download.py` into the HF cache:\n  - `MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli`\n  - `cross-encoder/nli-deberta-v3-large`\n  - `sentence-transformers/all-mpnet-base-v2`\n- **API models** (OpenRouter):\n  - `google/gemini-2.5-flash-lite`: cheap judge and verbaliser;\n  - `openai/gpt-4.1-nano`: P(YES) judge and SC-5 sampler;\n  - `google/gemini-3.1-pro-preview`: frontier judge, reasoning effort low, max_tokens 4000.\n- **Prompts** are frozen by sha1 in `prereg_T1.json`: RUBRIC_A `06686913…`, USER_JSON_A `5b3ccfb9…`, USER_YESNO\n  `b36e93cb…`, VERBALISE `584f33d0…`, SC few-shot `6c4db3c3…`.\n- **API cost cache.** `results/llm_cache.jsonl` holds every API response. With it, re-running any API stage costs\n  **$0** and returns identical scores. Without it, a fresh run costs about $2.40 (see `results/api_cost_ledger.json`);\n  temperature-0 outputs are near-deterministic, with retest exact-match 0.984.\n\n## 4. Commands, in the order actually run\n\nAll commands run from the workspace root with `export PYTHONHASHSEED=0`.", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5", "interrupted": false, "isImage": false, "noOutputExpected": false}
````

### [12] TOOL CALL — Bash · 2026-09-25 12:45:28 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6; cd $W; sed -n 1,70p method.py; sed -n 2207,2230p method.py; sed -n 2640,2701p method.py; ls src src/*; sed -n 80,200p reproducibility.md
```

### [13] TOOL RESULT — Bash · 2026-09-25 12:45:28 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"Every baseline re-run on the held-out NL->FOL set E (iteration 2, gen_art experiment 6 = plan gen_plan_experiment_2).\n\nStages (idempotent; every LLM call cached in results/llm_cache.jsonl, every score appended to results/scores/*.jsonl):\n  prep        label-blind load of E; parse check (fol.py + z3); nonce disguise (exp D disguise_item) -> data/E_units.json\n  prereg      write prereg_baselines.json (models, prompts, sha1s, feature sets, folds, thresholds, B2 spec, caps)\n  frame       draw the 300-row frontier frame (ONLY label read before scoring; disclosed) + label-vector sha1s,\n              then FREEZE prereg (sha256)\n  judges      judge_cheap (flash-lite, rubric A JSON) + judge_cheap2 (gpt-4.1-nano P(YES)), orig + disg   [--limit N]\n  sc_gen      SC-5 samples: gpt-4.1-nano, T=0.7, 5 per sentence, dataset-E few-shot prompt              [--limit N]\n  verbalise   round-trip API verbaliser (flash-lite, VERBALISE prompt)                                    [--limit N]\n  strong      judge_strong (gemini-3.1-pro-preview, effort low) orig + disg on the frontier frame         [--limit N]\n  retest      judge_cheap_disg test-retest on 200 sha1-chosen rows (cache-bypass nonce in the key only)\n  cpu         parse_fail + the user's pilot structural metrics (adapted documents)\n  sc_score    SC-5 scoring: equivalence modulo vocabulary of candidate vs samples (z3, pair cache)\n  local_judges / local_strong / local_verb / local_sc   F-KEY local path (Qwen3-8B, Llama-3.1-8B, Qwen3-14B-nf4; GPU)\n  nli         NLI (2 checkpoints, both directions) + mpnet cosine for a verbaliser (--which local|api; GPU)\n  b2_build    B2 worlds for every formula of every set (CPU, z3)\n  b2_read     B2 reader (--which dev,gate,screen,unbatched,rewrites,Eref,E; local Qwen3-8B, frozen prompt in prereg_b2.json)\n  b2_gate_report  reader gate + B2 thresholds from the screen (no E label)\n  sc_invariance   SC-5 on the shared rewrites from exp C's existing samples\n  t2_repro / retest_sibling   local-judge reproducibility vs exp D / test-retest vs the sibling experiment\n  b2_think    POST-HOC diagnostic: thinking-mode reader on the screen gate items (not pre-registered)\n  s4          feature table E_baseline_features.jsonl + folds_E.json (label-free)\n  analysis    S4 fits + all tables (src/analysis_E.py; the only place labels are joined), summary.md, method_out.json\nUsage: PYTHONHASHSEED=0 .venv/bin/python method.py --stage NAME [--limit N]\n\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport asyncio\nimport hashlib\nimport json\nimport math\nimport os\nimport sys\nimport time\nfrom collections import Counter, defaultdict\nfrom pathlib import Path\n\nos.environ.setdefault(\"PYTHONHASHSEED\", \"0\")\nos.environ.setdefault(\"NLTK_DATA\", str(Path(__file__).resolve().parent / \"data\" / \"nltk_data\"))\nos.environ.setdefault(\"TOKENIZERS_PARALLELISM\", \"false\")\nsys.setrecursionlimit(10000)\n\nfrom loguru import logger  # noqa: E402\n\nfrom src.common import DATA, LOGS, RES, ROOT, detect_cpus, jdump, jload, norm, read_jsonl, sha1, set_ram_limit  # noqa: E402\n\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\nlogger.add(str(LOGS / \"run.log\"), rotation=\"30 MB\", level=\"DEBUG\")\n\nNUM_CPUS = detect_cpus()\nWORKERS = max(1, min(12, NUM_CPUS - 2))\n# T1: label-blind pilots write to results/pilot (T1_SCORES_DIR) so that every file in results/scores post-dates the\n# prereg_T1 freeze; the LLM cache (results/llm_cache.jsonl) makes the later full sweep reuse the pilot calls for free\nSCORES = Path(os.environ[\"T1_SCORES_DIR\"]) if os.environ.get(\"T1_SCORES_DIR\") else RES / \"scores\"\nSCORES.mkdir(parents=True, exist_ok=True)\nEXPD = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_4\")\nEXPA = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_1\")\nEXPC = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3\")\nPREREG = ROOT / \"prereg_baselines.json\"\nPREREG_SHA = ROOT / \"prereg_baselines.sha256\"\nFEWSHOT = json.loads((Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_dataset_1\")\n                      / \"prompts\" / \"fewshot_v1.txt\").read_text())\n\n\n# ------------------------------------------------------------------ io helpers\ndef append_jsonl(p: Path, rows: list[dict]) -> None:\n# =====================================================================================================================\n\n# =====================================================================================================================\n# T1 (iteration 3): head-on API bar. Stages t1_prep (gates, priority, VEX), t1_pilot (label-blind), t1_freeze,\n# t1_join, t1_analysis (src/analyse_T1.py). See README.md.\nPREREG_T1 = ROOT / \"prereg_T1.json\"\nPREREG_T1_SHA = ROOT / \"prereg_T1.sha256\"\nEXP5_DIR = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_2/gen_art/gen_art_experiment_5\")\nEXPC_CONS = EXPC / \"src\" / \"consensus.py\"\n\n\ndef _t0_unit_tests() -> dict:\n    \"\"\"T0: no API, no labels.\"\"\"\n    import numpy as np\n    from sklearn.metrics import roc_auc_score\n    from src import api_bar as AB\n    from src import budget as BG\n    from src import judges as J\n    from src.vocab_exact import norm\n    out = {}\n    hits = []\n    for f in list((ROOT / \"src\").rglob(\"*.py\")) + list(ROOT.glob(\"*.sh\")):\n        if \"openrouter\" + \".ai\" in f.read_text(errors=\"ignore\"):\n            hits.append(str(f.relative_to(ROOT)))\n        \"vex\": {\"declaration_file\": \"results/vex_declaration.json\", \"declaration_sha256\": vex_sha, \"rows_sha256\": vex_rows_sha,\n                \"include_n\": vex[\"include\"][\"n\"], \"include_testable\": vex[\"include\"][\"testable\"],\n                \"strict_n\": vex[\"include_strict\"][\"n\"], \"strict_testable\": vex[\"include_strict\"][\"testable\"]},\n        \"local_fallback\": \"if an API arm is unfunded, the local exp-6 column (judge_local_qwen8b_disg etc.) is reported as a \"\n                          \"LABELLED secondary bar, never substituted silently in the verdict\",\n        \"pilot_summary\": ps,\n        \"repro_gates_sha256\": hashlib.sha256((RES / \"repro_gates.json\").read_bytes()).hexdigest(),\n    }\n    PREREG_T1.write_text(json.dumps(D, indent=1, ensure_ascii=False))\n    h = hashlib.sha256(PREREG_T1.read_bytes()).hexdigest()\n    PREREG_T1_SHA.write_text(f\"{h}  prereg_T1.json  frozen {datetime.datetime.utcnow().isoformat(timespec='seconds')}Z\\n\")\n    logger.info(f\"prereg_T1 frozen sha256 {h}; strong rule: {strong_rule}; estimates {est}\")\n\n\n\ndef stage_t1_analysis(which=(\"full\",)):\n    \"\"\"Step 5-7: join (per_item_T1.jsonl), every T1 analysis (src/analyse_T1.py), tables, verdict, figures,\n    method_out.json. --which quick = 10 permutation reps / B_gee 50 (smoke test only).\"\"\"\n    from src import analyse_T1 as AT\n    from src import report_T1 as RT\n    quick = \"quick\" in which\n    ks = _key_status()\n    jdump({\"end_of_sweeps\": ks, \"start_of_run\": jload(RES / \"pilot\" / \"key_model_check.json\")[\"key\"]}, RES / \"key_usage_log.json\")\n    A, T, rows, regimes = AT.run(max_perm=10 if quick else 100, gee_B=50 if quick else 1000)\n    A[\"cost_ledger\"] = RT.cost_ledger(A)\n    RT.per_item(T, rows, regimes, T.api)\n    n = RT.method_out(T, rows, regimes, A)\n    try:\n        A[\"figures\"] = RT.figures(A)\n    except Exception as e:  # noqa: BLE001 - figures are secondary; the failure is recorded\n        logger.error(f\"figures failed: {e}\")\n        A[\"figures\"] = {\"error\": str(e)[:300]}\n    jdump(A, RES / \"analysis_T1.json\")\n    jdump(A[\"verdict\"], RES / \"verdict_T1.json\")\n    (RES / \"tables_T1.md\").write_text(RT.tables(A))\n    logger.info(f\"T1 analysis: {A['verdict']['overall_T1_this_artifact']}; method_out rows {n}; runtime {A['runtime_s']:.0f}s\")\n\n\ndef main():\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--stage\", required=True)\n    ap.add_argument(\"--limit\", type=int, default=None)\n    ap.add_argument(\"--which\", default=None)\n    a = ap.parse_args()\n    if a.stage not in (\"local_judges\", \"local_strong\", \"local_verb\", \"local_sc\", \"nli\", \"b2_read\", \"t2_repro\", \"b2_think\"):\n        set_ram_limit(40)  # RLIMIT_AS breaks CUDA's virtual-address reservations: GPU stages rely on the VRAM guard instead\n    fn = globals().get(f\"stage_{a.stage}\")\n    if fn is None:\n        raise SystemExit(f\"unknown stage {a.stage}\")\n    t0 = time.time()\n    logger.info(f\"=== stage {a.stage} limit={a.limit} ===\")\n    kw = {}\n    if \"limit\" in fn.__code__.co_varnames[:fn.__code__.co_argcount]:\n        kw[\"limit\"] = a.limit\n    if a.which:\n        kw[\"which\"] = tuple(a.which.split(\",\"))\n    fn(**kw)\n    logger.info(f\"=== stage {a.stage} done in {time.time()-t0:.0f}s ===\")\n\n\nif __name__ == \"__main__\":\n    logger.catch(reraise=True)(main)()\nsrc/__init__.py\nsrc/analyse_T1.py\nsrc/analysis.py\nsrc/analysis_E.py\nsrc/api_bar.py\nsrc/b2_world_probe.py\nsrc/budget.py\nsrc/common.py\nsrc/consensus_min.py\nsrc/disguise.py\nsrc/e_pool.py\nsrc/exp5_analyse_E.py\nsrc/join_T1.py\nsrc/judges.py\nsrc/local_llm.py\nsrc/pilot_metrics.py\nsrc/report.py\nsrc/report_T1.py\nsrc/rewrites.py\nsrc/roundtrip.py\nsrc/s4.py\nsrc/screen.py\nsrc/vocab_exact.py\n\nsrc:\n__init__.py\n__pycache__\nanalyse_T1.py\nanalysis.py\nanalysis_E.py\napi_bar.py\nb2_world_probe.py\nbudget.py\ncommon.py\nconsensus_min.py\ndisguise.py\ne_pool.py\nexp5_analyse_E.py\njoin_T1.py\njudges.py\nlabeller\nlocal_llm.py\npilot_metrics.py\nreport.py\nreport_T1.py\nrewrites.py\nroundtrip.py\ns4.py\nscreen.py\nvocab_exact.py\n\nsrc/__pycache__:\n__init__.cpython-312.pyc\napi_bar.cpython-312.pyc\n\nsrc/labeller:\n__init__.py\nfol.py\nlabeller.py\nrepair_census.py\n\n**Hardware:**\n- setup and pilots (steps 1–3): an earlier container (GPU model not recorded in the logs; these steps are CPU/API only);\n- sweeps and analysis: NVIDIA RTX 2000 Ada (16 GB VRAM), 6 CPUs (cgroup), 251 GB RAM.\n\n**Seeds:**\n- bootstrap seed 0 (B = 2000);\n- GEE bootstrap seed 0 (B = 1000; n_conditions B = 500);\n- permutation null seed 0 (100 reps);\n- placebos seed 0.\n\n| # | command | what it does | runtime |\n|---|---|---|---|\n| 1 | `.venv/bin/python method.py --stage t1_prep` | key bijection, label-vector hashes, reproduction gates, VEX declaration → `results/repro_gates.json`, `results/vex_declaration.json` | 86 s |\n| 2 | `.venv/bin/python method.py --stage t1_pilot` | label-blind 20-row pilots → `results/pilot/` | 30 s |\n| 3 | `.venv/bin/python method.py --stage t1_freeze` | writes `prereg_T1.json` + `prereg_T1.sha256` (sha256 `c2a6cf84…`, 01:54:08Z). **Do not re-run:** the analysis refuses a changed prereg. | <1 s |\n| 4 | `bash t1_api_chain.sh` | judges `cheap_disg,cheap_orig`; judges `cheap2_disg,cheap2_orig`; `strong --which orig`; `verbalise`; `sc_gen`; `retest`; `strong --which disg` (the last is stopped by the pre-registered reserve rule) | ~10 min per cheap arm, 80 s frontier, ~9 min verbaliser, ~5 min SC-5 |\n| 5 | `method.py --stage verbalise` ; `--stage sc_gen` ; `--stage retest` | re-issue calls that failed during relay outages (cached, idempotent) | <1 min |\n| 6 | `.venv/bin/python method.py --stage nli --which api` | GPU: DeBERTa NLI in both directions (2 checkpoints) plus mpnet cosine on 6,228 (text, verbalisation) pairs | 5.4 min |\n| 7 | `.venv/bin/python method.py --stage sc_score --which sc5_samples` | CPU z3 equivalence modulo vocabulary, 25,429 pairs | 50 s |\n| 8 | `.venv/bin/python method.py --stage t1_analysis` | join, all analyses (a)–(j), verdict, tables, figures, method_out | 8.5 min |\n| 9 | `.venv/bin/python tests/audit_T1.py` | independent re-derivation from the joined per-row table | ~1 min |\n| 10 | `.venv/bin/python tests/audit_raw_T1.py` | re-derivation from RAW files (dataset E labels, exp 5 scores, raw API score files), plus placebo tests | ~1 min |\n| 11 | `aii_json_format_mini_preview.py --input method_out.json` (aii-json skill) | full / mini / preview outputs, validated as `exp_gen_sol_out` | seconds |\n\nThe figures were re-rendered after `t1_analysis`, from `results/analysis_T1.json`, via `src/report_T1.figures`, once\ntwo legend and import fixes were in (D6). No number changed.\n\n## 5. What you should get\n\nThese are the headline results (`results/verdict_T1.json`, `results/tables_T1.md`); the paper's T1 results section and\nforest figure use them. All figures are on the R_AB E_POOL PRIMARY population: n = 2,686 (1,822 ERROR / 864 CORRECT),\n292 sentences. \"Strat\" means stratified AUROC.\n\n| quantity | value |\n|---|---|\n| strat AUROC, `c_score_align` / flash-lite disguised | 0.741 / 0.642 |\n| pooled AUROC, `c_score_align` / flash-lite disguised | 0.782 / 0.696 |\n| **(a)** confirmatory strat Δ | **+0.099 [0.049, 0.146]** |\n| (a) long pool | +0.116 [0.070, 0.163] |\n| (a) R_A L20+EXC | +0.299 |\n| **(b)** nested [S4_full + c] − S4_full, strat | **+0.039 [0.021, 0.057]** (null p95 0.009) |\n| (d) frame ratio vs gemini-3.1-pro-preview | 0.957 [0.887, 1.034] |\n| (d) nested frame gain | +0.037 [0.008, 0.066] |\n| (d) cost per item, consensus / frontier | $1.2e-4 / $3.65e-3 |\n| VEX Δ | +0.306 [0.232, 0.376] |\n| M3 (words) | +0.146 [−0.051, +0.361] → **DISCONFIRMED** |\n| overall | **CONFIRMED** |\n| API spend | $2.395 |\n\nOther outputs:\n- `figures/forest_T1.png`: all cell deltas.\n- `figures/complexity_curves.png`: AUROC by length and by number of conditions.\n- `full_method_out.json`: per-row oriented scores of every metric.\n\n### Independent checks\n\n- `tests/audit_T1.py`: 5 headline numbers match to 1e-3.\n- `tests/audit_raw_T1.py`: re-derives the population, the pooled and stratified AUROCs, the confirmatory and long-pool\n  Δ, and the frame ratio exactly from the raw files. The same bootstrap test **fails**, as it should, on\n  within-stratum permuted labels (Δ +0.021 [−0.008, +0.049]) and on a random-score challenger (Δ −0.152).\n- The nested (b) gain and M3 were re-derived by `audit_T1.py` (per-row table, statsmodels refit), not from the raw\n  files. The (b) gain is additionally checked against a 100-rep label-permutation null, where it sits at percentile 1.00.", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [14] TOOL CALL — Bash · 2026-09-25 12:45:34 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6; cd $W; wc -l src/*.py tests/*.py; grep -n "^def \|^[A-Z_]* = " src/analyse_T1.py | head -80
```

### [15] TOOL RESULT — Bash · 2026-09-25 12:45:34 UTC

```
{"stdout": "     0 src/__init__.py\n  1030 src/analyse_T1.py\n   322 src/analysis.py\n   423 src/analysis_E.py\n   377 src/api_bar.py\n   363 src/b2_world_probe.py\n   186 src/budget.py\n    92 src/common.py\n    39 src/consensus_min.py\n   285 src/disguise.py\n   173 src/e_pool.py\n   882 src/exp5_analyse_E.py\n   210 src/join_T1.py\n   248 src/judges.py\n   219 src/local_llm.py\n   164 src/pilot_metrics.py\n   611 src/report.py\n   391 src/report_T1.py\n   252 src/rewrites.py\n    87 src/roundtrip.py\n   102 src/s4.py\n   359 src/screen.py\n   159 src/vocab_exact.py\n   168 tests/audit_E.py\n   143 tests/audit_T1.py\n   168 tests/audit_raw_T1.py\n    38 tests/test_b2.py\n    75 tests/test_units.py\n  7566 total\n24:STRATA = [\"L25\", \"L20\", \"EXC\", \"CTRL\"]\n25:LONG = (\"L25\", \"L20\", \"EXC\")\n26:CHALLENGERS = [\"c_score_align\", \"g_score\", \"nf_c_score\", \"p_peer_text\", \"p_text\"]\n27:API_BARS = [\"judge_cheap_disg\", \"judge_cheap_orig\", \"judge_cheap2_disg\", \"judge_cheap2_orig\"]\n28:LOCAL_BAR = \"L:judge_local_qwen8b_disg\"\n29:B = 2000\n30:FIG = ROOT / \"figures\"\n31:TIEBREAK_EPS = 1e-9\n34:def _u01(k: str) -> float:\n39:def guard() -> dict:\n168:def testable(y, cl) -> bool:\n175:def describe(cell: Cell, m: str, thr: dict, cost_item: dict) -> dict:\n199:def run(max_perm: int = 100, gee_B: int = 1000, t_budget_gee_s: float = 2400.0) -> dict:\n380:def vfb_columns(rows, api) -> dict:\n411:def consensus_costs(rows, P) -> dict:\n438:def _s4_table(T: Table, rows, feats_all, strata_onehot=True):\n458:def s4_nesting(T, rows, regimes, P, yP, pre, api, cov, max_perm=100):\n574:def _mean_coef(c):\n583:def vex_analysis(T, P, yP, api):\n635:def frontier(T, regimes, api, cost_item, cons_cost):\n706:def nested_frame(cell, ks, y, T):\n728:def m3(T, P, yP, api, gee_B=1000, t_budget_s=2400.0):\n806:BINS = {\"words\": [(0, 12, \"<12\"), (12, 20, \"12-19\"), (20, 25, \"20-24\"), (25, 35, \"25-34\"), (35, 10 ** 6, \">=35\")],\n811:def complexity(T, P, yP, api):\n844:def contamination(T, regimes, api):\n909:def err_groups(x) -> list[str]:\n933:def recall_groups(T, P, yP, api):\n963:def system_level(T, P, yP, api):\n995:def verdict(A) -> dict:", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [16] TOOL CALL — Bash · 2026-09-25 12:45:36 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6; cd $W; cat tests/audit_raw_T1.py; sed -n 1,380p src/analyse_T1.py
```

### [17] TOOL RESULT — Bash · 2026-09-25 12:45:36 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"Raw-file re-derivation of the T1 headline numbers (TODO 5), on a code path disjoint from src/ and tests/audit_T1.py.\n\nReads ONLY raw inputs, never the joined or aggregated outputs:\n- labels from dataset E itself (iter_1 full_data_out.json, heldout_candidates);\n- pool and parse_ok from data/E_units.json;\n- consensus scores from exp 5's frozen per_item_E.jsonl (exp 5 imputation value read from data/exp5/prereg.json);\n- API judge sc... [truncated, 29881 chars total]
```

### [18] ASSISTANT · 2026-09-25 12:45:46 UTC

```
Reading the artifact's analysis code (method.py dispatches to `src/analyse_T1.py` and `src/api_bar.py`) so I can pick the parts that run offline for the demo.
```

### [19] TOOL CALL — Bash · 2026-09-25 12:45:46 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6; cd $W; grep -n "^def \|^class " src/api_bar.py; python3 - <<'EOF'
import re
src=open('src/api_bar.py').read()
for name in ['auroc','strat_auroc','ClusterBoot','boot_ci','delong','tie_rate','recall_at','matched_fa_threshold']:
    m=re.search(r'^(def|class) '+name+r'\b.*?(?=^\S)', src, re.S|re.M)
    print(m.group(0) if m else 'MISSING '+name)
EOF
sed -n 1,30p src/api_bar.py
```

### [20] TOOL RESULT — Bash · 2026-09-25 12:45:46 UTC

```
{"stdout": "78:def sc5_score(candidate: str, samples: Sequence[str | None], ms: int = 2000) -> dict:\n113:def auroc(y, s) -> float:\n125:def tie_rate(y, s) -> float:\n138:def strat_auroc(y, s, stratum) -> float:\n155:class ClusterBoot:\n173:def boot_ci(vals, lo: float = 2.5, hi: float = 97.5) -> list:\n180:def paired_boot(y, a, c, cb: ClusterBoot, stat: str = \"pooled\", stratum=None) -> dict:\n202:def boot_stat(y, s, cb: ClusterBoot, stat: str = \"pooled\", stratum=None) -> dict:\n212:def delong(y, s1, s2) -> dict:\n245:def matched_fa_threshold(neg_vals, fa: float = 0.10) -> float:\n250:def recall_at(y, s, t) -> dict:\n260:def ipw_auroc(y, s, w) -> float:\n275:def build_s4(table: list[dict], labels: dict, folds: dict, feats: list[str], fail_fill: dict, C: float = 1.0):\n282:def nested_delta(y, s_big, s_small, cb: ClusterBoot, stratum=None) -> dict:\n289:def permutation_null(fit_pair: Callable[[dict], tuple[np.ndarray, np.ndarray]], keys: list[str], y: np.ndarray,\n311:def gee_slope(correct, z, stratum, groups, alt_glm: bool = True) -> dict:\n333:def _gee_fast_slope(c, z, H, g) -> float:\n341:def gee_slope_diff(correct_a, correct_b, z, stratum, groups, B: int = 1000, seed: int = 0, n_jobs: int = 7) -> dict:\n367:def consensus_cost_per_item(peer_cost_sentence: float, n_candidates_sentence: int, z3_seconds: float,\n375:def vex_subset(*a, **k):\ndef auroc(y, s) -> float:\n    \"\"\"Mann-Whitney AUROC, ties counted 1/2 (== sklearn roc_auc_score). nan if one class is empty.\"\"\"\n    y = np.asarray(y)\n    s = np.asarray(s, float)\n    n1 = int(y.sum())\n    n0 = len(y) - n1\n    if n1 == 0 or n0 == 0:\n        return float(\"nan\")\n    r = rankdata(s)\n    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))\n\n\n\ndef strat_auroc(y, s, stratum) -> float:\n    \"\"\"Within-stratum AUROC: sum_h AUC_h * P_h * N_h / sum_h P_h * N_h (only (ERROR, CORRECT) pairs from the same\n    source stratum count), identical to exp 5's strat_auc. Removes the stratum-composition part of pooled AUROC.\"\"\"\n    y = np.asarray(y)\n    s = np.asarray(s, float)\n    stratum = np.asarray(stratum)\n    num = den = 0.0\n    for h in np.unique(stratum):\n        m = stratum == h\n        n1 = int(y[m].sum())\n        n0 = int(m.sum()) - n1\n        if n1 and n0:\n            num += auroc(y[m], s[m]) * n1 * n0\n            den += n1 * n0\n    return num / den if den else float(\"nan\")\n\n\n\nclass ClusterBoot:\n    \"\"\"Sentence-clustered bootstrap index sets: resample sentence ids with replacement (fixed seed); every metric on a\n    row set uses the IDENTICAL resamples, which makes deltas paired.\"\"\"\n\n    def __init__(self, clusters: Sequence[str], b: int = 2000, seed: int = 0):\n        by = defaultdict(list)\n        for i, c in enumerate(clusters):\n            by[c].append(i)\n        keys = sorted(by)\n        arr = [np.array(by[k]) for k in keys]\n        rng = np.random.default_rng(seed)\n        self.idx = []\n        for _ in range(b):\n            pick = rng.integers(0, len(keys), len(keys))\n            self.idx.append(np.concatenate([arr[j] for j in pick]))\n        self.n_clusters = len(keys)\n\n\n\ndef boot_ci(vals, lo: float = 2.5, hi: float = 97.5) -> list:\n    v = np.asarray([x for x in vals if x is not None and not (isinstance(x, float) and math.isnan(x))], float)\n    if len(v) == 0:\n        return [None, None]\n    return [float(np.percentile(v, lo)), float(np.percentile(v, hi))]\n\n\n\ndef delong(y, s1, s2) -> dict:\n    \"\"\"DeLong paired test on pooled AUROC (secondary: ignores sentence clustering).\"\"\"\n    from scipy.stats import norm\n    y = np.asarray(y)\n    s1 = np.asarray(s1, float)\n    s2 = np.asarray(s2, float)\n    pos, neg = s1[y == 1], s1[y == 0]\n    pos2, neg2 = s2[y == 1], s2[y == 0]\n    m, n = len(pos), len(neg)\n    if m < 2 or n < 2:\n        return {\"z\": None, \"p\": None}\n\n    def comps(p, q):\n        # V10_i = mean_j [p_i > q_j] + .5[p_i == q_j]; vectorised by ranks\n        allv = np.concatenate([p, q])\n        r_all = rankdata(allv)\n        r_p = rankdata(p)\n        r_q = rankdata(q)\n        v10 = (r_all[:len(p)] - r_p) / len(q)\n        v01 = 1.0 - (r_all[len(p):] - r_q) / len(p)\n        return v10, v01\n    a10, a01 = comps(pos, neg)\n    b10, b01 = comps(pos2, neg2)\n    d = a10.mean() - b10.mean()\n    s10 = np.cov(np.vstack([a10, b10]))\n    s01 = np.cov(np.vstack([a01, b01]))\n    var = (s10[0, 0] + s10[1, 1] - 2 * s10[0, 1]) / m + (s01[0, 0] + s01[1, 1] - 2 * s01[0, 1]) / n\n    if var <= 0:\n        return {\"z\": None, \"p\": None}\n    z = d / math.sqrt(var)\n    return {\"z\": float(z), \"p\": float(2 * (1 - norm.cdf(abs(z))))}\n\n\n\ndef tie_rate(y, s) -> float:\n    \"\"\"Share of (ERROR, CORRECT) pairs whose scores are exactly tied.\"\"\"\n    y = np.asarray(y)\n    s = np.asarray(s, float)\n    pos, neg = s[y == 1], s[y == 0]\n    if len(pos) == 0 or len(neg) == 0:\n        return float(\"nan\")\n    vals, inv = np.unique(np.concatenate([pos, neg]), return_inverse=True)\n    cp = np.bincount(inv[:len(pos)], minlength=len(vals))\n    cn = np.bincount(inv[len(pos):], minlength=len(vals))\n    return float((cp * cn).sum() / (len(pos) * len(neg)))\n\n\n\ndef recall_at(y, s, t) -> dict:\n    y = np.asarray(y)\n    s = np.asarray(s, float)\n    f = s > t\n    tp = int((f & (y == 1)).sum())\n    fp = int((f & (y == 0)).sum())\n    return {\"threshold\": float(t), \"recall\": tp / max(1, int(y.sum())), \"fa\": fp / max(1, int((y == 0).sum())),\n            \"precision\": tp / max(1, tp + fp), \"n_flag\": int(f.sum())}\n\n\n\ndef matched_fa_threshold(neg_vals, fa: float = 0.10) -> float:\n    \"\"\"Threshold t = the (1-fa) quantile of the scores of CORRECT rows (flag = score > t).\"\"\"\n    return float(np.quantile(np.asarray(neg_vals, float), 1 - fa))\n\n\n\n\"\"\"T1 head-on API bar: reusable metric wrappers (text, fol) and the statistics core of analyse_T1.py.\n\nORIENTATION CONVENTION (every score returned or consumed here): higher = more likely UNFAITHFUL to the text.\n\nMetric wrappers (async; each takes a budget.Budget so every call is cost-capped and cached in results/llm_cache.jsonl)\n  judge_api(b, text, fol, model, view, rubric='A')   1 - P(faithful) from a rubric-A JSON LLM judge (T=0, max_tokens 150)\n  judge_pyes(b, text, fol, model, view)              1 - P(YES) from next-token logprobs of a one-word YES/NO judge\n  frontier_judge(b, text, fol, view, model=...)      judge_api with a reasoning model (effort low, max_tokens 4000)\n  sc5_api(b, text, k=5)                              k T=0.7 formalisations of the sentence (dataset-E few-shot prompt)\n  sc5_score(candidate, samples)                      (1 - share of samples equivalent to the candidate modulo vocabulary,\n                                                      entropy of the equivalence classes of {candidate} + samples)  [z3]\n  roundtrip_api(b, text, fol)                        FOL -> English (flash-lite VERBALISE) -> the text; NLI / cosine are\n                                                      computed on the GPU by method.py --stage nli --which api\n  view = 'orig' (the sentence and formula as given) or 'disg' (exp-D nonce disguise of content words, both sides).\n\nStatistics core (numpy; sentence-clustered)\n  auroc, tie_rate, strat_auroc, ClusterBoot, paired_boot, boot_ci, delong, matched_fa_threshold, recall_at,\n  build_s4 / nested_delta / permutation_null (cross-fitted logistic stacks on folds_E), gee_slope, gee_slope_diff,\n  consensus_cost_per_item, ipw_auroc, vex_subset (re-exported from src/vocab_exact.py).\n\"\"\"\nfrom __future__ import annotations\n\nimport math\nfrom collections import defaultdict\nfrom typing import Callable, Sequence\n\nimport numpy as np\nfrom scipy.stats import rankdata\n\nSTRATA = (\"L25\", \"L20\", \"EXC\", \"CTRL\")", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] TOOL CALL — Bash · 2026-09-25 12:45:52 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6; cd $W; sed -n 806,845p src/analyse_T1.py; python3 - <<'EOF'
import json, collections
d=json.load(open('full_method_out.json'))
print(d.keys(), d['metadata'].keys())
for ds in d['datasets']:
    ex=ds['examples']; print(ds['dataset'], len(ex))
    P=[e for e in ex if e['metadata_in_R_AB'] and e['metadata_pool']=='E_POOL' and e['metadata_parse_ok']]
    print('P',len(P), collections.Counter(e['output'] for e in P), len({e['metadata_sentence_id'] for e in P}))
    print(collections.Counter(e['metadata_strata']['source_stratum'] for e in P))
    print(collections.Counter((e['metadata_strata']['source_stratum'],e['output']) for e in P))
    na=collections.Counter(k for e in P for k,v in e.items() if k.startswith('predict_') and v=='NA'); print(na)
    print(sorted(set(k for e in ex[:3] for k in e)))
    print(len(json.dumps(P[0])))
EOF
```

### [22] TOOL RESULT — Bash · 2026-09-25 12:45:52 UTC

```
{"stdout": "BINS = {\"words\": [(0, 12, \"<12\"), (12, 20, \"12-19\"), (20, 25, \"20-24\"), (25, 35, \"25-34\"), (35, 10 ** 6, \">=35\")],\n        \"n_conditions\": [(0, 2, \"<=1\"), (2, 3, \"2\"), (3, 4, \"3\"), (4, 10 ** 6, \"4+\")],\n        \"n_quant\": [(0, 2, \"0-1\"), (2, 3, \"2\"), (3, 10 ** 6, \"3+\")]}\n\n\ndef complexity(T, P, yP, api):\n    mets = [\"c_score_align\", \"nf_c_score\", \"p_peer_text\"] + [b for b in API_BARS if b in api] + \\\n        [m for m in (\"S4_full_oof\", \"sc5_eq_frac\", \"rt_nli_min\") if m in api or m in T.extra] + [LOCAL_BAR]\n    depth = np.array([T.by[k][\"strata\"][\"depth\"] for k in P], float)\n    q = np.quantile(depth, [1 / 3, 2 / 3])\n    out = {}\n    for var, bins in list(BINS.items()) + [(\"depth\", [(-1, q[0] + 1e-9, f\"<={q[0]:g}\"), (q[0] + 1e-9, q[1] + 1e-9, f\"({q[0]:g},{q[1]:g}]\"),\n                                                     (q[1] + 1e-9, 10 ** 6, f\">{q[1]:g}\")]), (\"exception_type\", None)]:\n        res = {}\n        if bins is None:\n            vals = [str(T.by[k][\"strata\"].get(\"exception_type\")) for k in P]\n            groups = sorted(set(vals))\n            idx_of = {gname: [i for i, v in enumerate(vals) if v == gname] for gname in groups}\n        else:\n            vv = np.array([T.by[k][\"strata\"][var] for k in P], float)\n            idx_of = {lab: list(np.where((vv >= lo) & (vv < hi))[0]) for lo, hi, lab in bins}\n        for lab, ix in idx_of.items():\n            ks = [P[i] for i in ix]\n            y = yP[ix]\n            cell = Cell(f\"{var}:{lab}\", ks, y, T, b=1000)\n            r = {\"n\": len(ks), \"n_error\": int(y.sum()), \"n_correct\": int(len(y) - y.sum()), \"testable\": testable(y, cell.cl),\n                 \"metrics\": {}}\n            if len(ks) >= 10 and 0 < y.sum() < len(y):\n                for m in mets:\n                    r[\"metrics\"][m] = cell.metric(m, \"pooled\")\n                if \"judge_cheap_disg\" in api:\n                    r[\"delta_c_minus_cheapdisg\"] = cell.delta(\"c_score_align\", \"judge_cheap_disg\", \"pooled\")\n            res[lab] = r\n        out[var] = res\n    return out\n\n\n# ===================================================================================================== (g)\ndef contamination(T, regimes, api):\n    out = {}\ndict_keys(['metadata', 'datasets']) dict_keys(['method_name', 'description', 'prereg_T1_sha256', 'verdict'])\nE_heldout_T1 8507\nP 2686 Counter({'ERROR': 1822, 'CORRECT': 864}) 292\nCounter({'L25': 873, 'L20': 821, 'EXC': 606, 'CTRL': 386})\nCounter({('L25', 'ERROR'): 697, ('L20', 'ERROR'): 592, ('EXC', 'ERROR'): 384, ('CTRL', 'CORRECT'): 237, ('L20', 'CORRECT'): 229, ('EXC', 'CORRECT'): 222, ('L25', 'CORRECT'): 176, ('CTRL', 'ERROR'): 149})\nCounter({'predict_judge_strong_disg': 2686, 'predict_judge_strong_orig': 2402, 'predict_local_pilot_rerun_jacc': 3})\n['input', 'metadata_canonical_key', 'metadata_exp6_row_key', 'metadata_family', 'metadata_fold_E', 'metadata_in_R_A', 'metadata_in_R_AB', 'metadata_item_id', 'metadata_label_tier', 'metadata_parse_ok', 'metadata_pool', 'metadata_sentence_id', 'metadata_strata', 'metadata_sysvar', 'metadata_vex', 'output', 'predict_PT_refit_NF_oof', 'predict_PT_refit_oof', 'predict_S4_full_oof', 'predict_S4_full_plus_c_score_align_oof', 'predict_S4_local_oof', 'predict_c_score_align', 'predict_g_score', 'predict_judge_cheap2_disg', 'predict_judge_cheap2_orig', 'predict_judge_cheap_disg', 'predict_judge_cheap_disg_vfb', 'predict_judge_cheap_orig', 'predict_judge_strong_disg', 'predict_judge_strong_orig', 'predict_l2_bow', 'predict_l3_z3', 'predict_local_judge_local_llama8b_disg', 'predict_local_judge_local_qwen8b_disg', 'predict_local_judge_local_qwen8b_orig', 'predict_local_parse_fail', 'predict_local_pilot_rerun_jacc', 'predict_local_rt_nli_min_local', 'predict_local_sc5_local_eq_frac', 'predict_nf_c_score', 'predict_nf_g_score', 'predict_p_peer_text', 'predict_p_text', 'predict_rt_embed_cos', 'predict_rt_nli_bwd', 'predict_rt_nli_contra', 'predict_rt_nli_fwd', 'predict_rt_nli_min', 'predict_rt_nli_min_alt', 'predict_sc5_entropy', 'predict_sc5_eq_frac']\n2227", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [23] TOOL CALL — Bash · 2026-09-25 12:46:18 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6; cd $W; sed -n 635,730p src/analyse_T1.py; cat results/verdict_T1.json; python3 -c "
import json;p=json.load(open('prereg_T1.json'));print(p.keys());print(json.dumps(p.get('thresholds'))[:1000])
p=json.load(open('prereg_baselines.json'));print(json.dumps(p.get('thresholds'))[:1000])"
```

### [24] TOOL RESULT — Bash · 2026-09-25 12:46:18 UTC

```
{"stdout": "def frontier(T, regimes, api, cost_item, cons_cost):\n    fr = jload(DATA / \"frontier_frame.json\")\n    pop = fr[\"cells_population\"]\n    item_to_keys = defaultdict(list)\n    for x in T.rows:\n        if x[\"pool\"] == \"E_POOL\" and x[\"parse_ok\"]:\n            item_to_keys[x[\"item_id\"]].append(x[\"canonical_key\"])\n    lab = regimes[\"R_AB\"]\n    ks, y, w, cellname = [], [], [], []\n    for r in fr[\"rows\"]:\n        cand = [k for k in item_to_keys[r[\"item_id\"]] if k in lab]\n        if not cand:\n            continue\n        k = sorted(cand)[0]  # one row per frame item (colliding item ids carry identical inputs and scores)\n        ks.append(k)\n        y.append(lab[k])\n        w.append(1.0 / r[\"incl_prob\"])\n        cellname.append(r[\"cell\"])\n    y = np.array(y)\n    w = np.array(w)\n    out = {\"n_frame_rows\": len(ks), \"n_error\": int(y.sum()), \"n_correct\": int(len(y) - y.sum()), \"metrics\": {}}\n    cell = Cell(\"frame\", ks, y, T)\n    mets = [\"c_score_align\", \"p_peer_text\", \"nf_c_score\", \"judge_strong_orig\", \"judge_strong_disg\", \"judge_cheap_disg\",\n            \"judge_cheap_orig\", \"S4_full_oof\", \"S4_local_oof\", \"L:judge_local_qwen14b_orig\", \"L:judge_local_qwen14b_disg\", LOCAL_BAR]\n    for m in mets:\n        if not (m in api or m in T.extra or m.startswith(\"L:\") or m in CHALLENGERS):\n            continue\n        s = T.vec(m, ks)\n        mk = ~np.isnan(s)\n        if mk.sum() < 20:\n            out[\"metrics\"][m] = {\"n\": int(mk.sum()), \"untestable\": True}\n            continue\n        mt = cell.metric(m, \"pooled\", mk)\n        mt[\"auroc_ipw\"] = AB.ipw_auroc(y[mk], s[mk], w[mk])\n        cb = cell.boot(mk)[1]\n        mt[\"auroc_ipw_ci\"] = AB.boot_ci([AB.ipw_auroc(y[mk][ix], s[mk][ix], w[mk][ix]) for ix in cb.idx[:1000]])\n        mt[\"coverage_frame\"] = int(mk.sum())\n        out[\"metrics\"][m] = mt\n    views = [v for v in (\"judge_strong_orig\", \"judge_strong_disg\") if v in out[\"metrics\"] and not out[\"metrics\"][v].get(\"untestable\", False)]\n    if views:\n        best = max(views, key=lambda v: out[\"metrics\"][v][\"auroc\"])\n        mk = cell.mask_for(\"c_score_align\", best)\n        pa, ba = cell.series(\"c_score_align\", mk, \"pooled\")\n        pb, bb = cell.series(best, mk, \"pooled\")\n        ratio_b = ba / bb\n        out[\"ratio\"] = {\"best_frontier_view\": best, \"ratio\": pa / pb, \"ci\": AB.boot_ci(ratio_b), \"auroc_c\": pa, \"auroc_frontier\": pb,\n                        \"n\": int(mk.sum()), \"delta\": cell.delta(\"c_score_align\", best, \"pooled\")}\n        s_ipw_c = AB.ipw_auroc(y[mk], T.vec(\"c_score_align\", ks)[mk], w[mk])\n        s_ipw_f = AB.ipw_auroc(y[mk], T.vec(best, ks)[mk], w[mk])\n        out[\"ratio\"][\"ratio_ipw\"] = s_ipw_c / s_ipw_f\n        # nested inside the frame: 5-fold GroupKFold by sentence, logistic [strong_orig + c] vs [strong_orig]\n        if \"judge_strong_orig\" in api:\n            out[\"nested_frame\"] = nested_frame(cell, ks, y, T)\n        fcost = [cost_item.get(v) for v in views if cost_item.get(v) is not None]\n        f_item = float(sum(fcost)) if fcost else None  # orig (+ disg if both used) per item\n        out[\"cost\"] = {\"frontier_usd_per_item_views_used\": f_item, \"frontier_views\": views,\n                       \"frontier_usd_per_call\": cost_item.get(\"judge_strong_orig\"),\n                       \"consensus_full_usd_per_item\": cons_cost[\"full_mean_usd_per_item\"],\n                       \"consensus_marginal_usd_per_item\": cons_cost[\"marginal_mean_usd_per_item\"]}\n        cost_ok = f_item is not None and cons_cost[\"full_mean_usd_per_item\"] <= 0.10 * f_item\n        ratio_ok = out[\"ratio\"][\"ratio\"] >= 0.95\n        nest_ok = bool(out.get(\"nested_frame\", {}).get(\"ci\") and out[\"nested_frame\"][\"ci\"][0] is not None and out[\"nested_frame\"][\"ci\"][0] > 0)\n        out[\"criterion_d\"] = {\"ratio_ge_0.95\": ratio_ok, \"cost_le_0.10x\": cost_ok, \"nested_CI_gt0\": nest_ok,\n                              \"holds\": (ratio_ok and cost_ok) or nest_ok, \"ratio\": out[\"ratio\"][\"ratio\"], \"ratio_ci\": out[\"ratio\"][\"ci\"]}\n        if \"judge_strong_orig\" in api and \"judge_strong_disg\" in api:\n            out[\"orig_minus_disg_frontier\"] = cell.delta(\"judge_strong_orig\", \"judge_strong_disg\", \"pooled\")\n    else:\n        out[\"criterion_d\"] = {\"holds\": None, \"note\": \"no frontier scores\"}\n    return out\n\n\ndef nested_frame(cell, ks, y, T):\n    from sklearn.linear_model import LogisticRegression\n    from sklearn.model_selection import GroupKFold\n    so = T.vec(\"judge_strong_orig\", ks)\n    sc = T.vec(\"c_score_align\", ks)\n    mk = ~np.isnan(so) & ~np.isnan(sc)\n    yy, g = y[mk], cell.cl[mk]\n    X1 = so[mk][:, None]\n    X2 = np.column_stack([so[mk], sc[mk]])\n    o1, o2 = np.zeros(len(yy)), np.zeros(len(yy))\n    for tr, te in GroupKFold(n_splits=5).split(X1, yy, g):\n        for X, o in ((X1, o1), (X2, o2)):\n            mu, sd = X[tr].mean(0), X[tr].std(0)\n            sd[sd == 0] = 1\n            clf = LogisticRegression(C=1.0, max_iter=2000).fit((X[tr] - mu) / sd, yy[tr])\n            o[te] = clf.predict_proba((X[te] - mu) / sd)[:, 1]\n    cb = AB.ClusterBoot(list(g), b=B, seed=0)\n    r = AB.paired_boot(yy, o2, o1, cb, \"pooled\")\n    return {\"delta\": r[\"delta\"], \"ci\": r[\"ci\"], \"auroc_with_c\": r[\"a\"], \"auroc_strong_only\": r[\"b\"], \"n\": int(mk.sum())}\n\n\n# ===================================================================================================== (e)\ndef m3(T, P, yP, api, gee_B=1000, t_budget_s=2400.0):\n    from .api_bar import gee_slope, gee_slope_diff\n    words = np.array([T.by[k][\"strata\"][\"words\"] for k in P], float)\n{\n \"criteria\": {\n  \"a\": {\n   \"status\": \"CONFIRMED\",\n   \"bar\": \"judge_cheap_disg\",\n   \"R_AB_strat\": {\n    \"delta\": 0.09897545149036036,\n    \"ci\": [\n     0.049345245474241926,\n     0.14599146000544172\n    ],\n    \"n\": 2686,\n    \"p_one_sided_le0\": 0.0\n   },\n   \"R_AB_strat_CI_gt0\": true,\n   \"long_strat\": {\n    \"delta\": 0.11625879215576673,\n    \"ci\": [\n     0.06991415990284278,\n     0.16265250895731315\n    ],\n    \"n\": 2300\n   },\n   \"long_strat_CI_gt0\": true,\n   \"R_A_L20EXC\": {\n    \"delta\": 0.29941908034691533,\n    \"ci\": [\n     0.21218117482349824,\n     0.3897211402882066\n    ],\n    \"n\": 449\n   },\n   \"R_A_sign_gt0\": true,\n   \"holds\": true\n  },\n  \"b\": {\n   \"status\": \"CONFIRMED\",\n   \"holds\": true,\n   \"pooled_version_holds\": true,\n   \"pooled_stratified_disagree\": false,\n   \"strat\": {\n    \"delta\": 0.038774976834802466,\n    \"ci\": [\n     0.020688153046929857,\n     0.057380026063755245\n    ],\n    \"n\": 2686\n   },\n   \"pooled\": {\n    \"delta\": 0.03008052303126396,\n    \"ci\": [\n     0.014868954855340838,\n     0.04471130808071272\n    ],\n    \"n\": 2686\n   },\n   \"null_p95_strat\": 0.009063862027819385\n  },\n  \"d\": {\n   \"status\": \"CONFIRMED\",\n   \"ratio_ge_0.95\": true,\n   \"cost_le_0.10x\": true,\n   \"nested_CI_gt0\": true,\n   \"holds\": true,\n   \"ratio\": 0.9573029948134515,\n   \"ratio_ci\": [\n    0.8874732219365781,\n    1.0344404378370433\n   ]\n  },\n  \"VEX\": {\n   \"status\": \"CONFIRMED\",\n   \"testable\": true,\n   \"delta\": 0.3058391294592776,\n   \"ci\": [\n    0.23239109453303944,\n    0.37569156989574914\n   ],\n   \"sign_positive\": true,\n   \"strong_form_CI_gt0\": true,\n   \"holds\": true\n  },\n  \"M3\": {\n   \"status\": \"DISCONFIRMED\",\n   \"holds\": false,\n   \"diff\": 0.14627685998181889,\n   \"ci\": [\n    -0.05067399100847099,\n    0.3609236572521462\n   ],\n   \"ncond_diff\": 0.11562187346987633,\n   \"ncond_ci\": [\n    -0.04412439823540026,\n    0.2637934915607844\n   ]\n  },\n  \"c\": {\n   \"status\": \"OTHER ARTIFACT (R_COMP-SIG)\"\n  },\n  \"e\": {\n   \"status\": \"OTHER ARTIFACT\"\n  }\n },\n \"overall_T1_this_artifact\": \"CONFIRMED\",\n \"robustness_BEST_API_CHEAP\": {\n  \"bar\": \"judge_cheap2_orig\",\n  \"criterion_a\": \"CONFIRMED\",\n  \"R_AB_strat\": {\n   \"delta\": 0.08883292282755317,\n   \"ci\": [\n    0.043263924047980074,\n    0.13441047833661954\n   ],\n   \"n\": 2686,\n   \"p_one_sided_le0\": 0.0\n  },\n  \"R_AB_strat_CI_gt0\": true,\n  \"long_strat\": {\n   \"delta\": 0.09834695826346185,\n   \"ci\": [\n    0.051745649074517466,\n    0.14301297147118297\n   ],\n   \"n\": 2300\n  },\n  \"long_strat_CI_gt0\": true,\n  \"R_A_L20EXC\": {\n   \"delta\": 0.2859597447226313,\n   \"ci\": [\n    0.2006732880873332,\n    0.36614180380498107\n   ],\n   \"n\": 449\n  },\n  \"R_A_sign_gt0\": true,\n  \"holds\": true\n },\n \"local_bar_secondary\": {\n  \"bar\": \"L:judge_local_qwen8b_disg\",\n  \"criterion_a\": \"CONFIRMED\"\n }\n}dict_keys(['title', 'created_iso', 'hypothesis_T1', 'models', 'model_swaps', 'live_prices', 'prompt_sha1', 'params', 'strong', 'judge_json_failure_sensitivity', 'budget', 'execution_order', 'frontier_frame', 'comparators_priority', 'challengers', 'confirmatory_contrast', 'population', 'criteria', 'bootstrap', 'thresholds', 'testability', 'S4_sets', 'vex', 'local_fallback', 'pilot_summary', 'repro_gates_sha256'])\n{\"judges\": \"flag if P(faithful) < 0.5 (oriented > 0.5), screen-frozen\", \"consensus_PT\": {\"fused\": 0.6902659323258526, \"text\": 0.7809534183242605}, \"M3_operating_point\": \"FA = 0.10 on E R_AB CORRECT rows (90th percentile), same for every metric\"}\n{\"rule\": \"frozen from the SCREEN (exp D results/analysis.json); judges flag if P(faithful)<0.5\", \"values_from_expD\": {\"parse_fail\": 0.5, \"pilot_joint_conflict\": 0.5, \"pilot_arity_incons\": 0.0, \"pilot_shape_incons\": 0.0, \"pilot_dangling\": 0.5, \"pilot_undeclared\": 0.0, \"pilot_rerun_jacc\": 0.5, \"rt_nli_min\": 0.9774119272828102, \"rt_nli_fwd\": 0.33368949890136723, \"rt_nli_bwd\": 0.9551530726253987, \"rt_nli_contra\": 0.026751494035124845, \"rt_nli_min_alt\": 0.9949031063355506, \"rt_embed_cos\": 0.3201072692871094, \"rt_reformalise_eq\": 0.5, \"judge_cheap_orig\": 0.5, \"judge_cheap_disg\": 0.5, \"judge_cheap2_orig\": 0.5, \"judge_cheap2_disg\": 0.5, \"judge_strong_orig\": 0.5, \"judge_strong_disg\": 0.5, \"judge_local_qwen8b_orig\": 0.5, \"judge_local_qwen8b_disg\": 0.5, \"judge_local_llama8b_orig\": 0.5, \"judge_local_llama8b_disg\": 0.5, \"judge_local_qwen14b_orig\": 0.5, \"judge_local_qwen14b_disg\": 0.5, \"rt_nli_min_localverb\": 0.9840680196881295, \"rt_reformalise_eq_localverb\": 0.5}, \"new_columns\": {\"rt_nli_min_local\"", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [25] TOOL CALL — Bash · 2026-09-25 12:46:26 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6; cd $W; sed -n 180,212p src/api_bar.py; python3 - <<'EOF'
import json
A=json.load(open('results/analysis_T1.json'))
print(A.keys())
m=A['a_head_on']['R_AB pooled']['metrics']
for k,v in m.items(): print(k, {s:(round(x.get('auroc',float('nan')),3)) for s,x in v.items()})
print(json.dumps(A['d_frontier']['ratio'])[:600])
print(json.dumps(A['b_s4'])[:1500])
print(A['population'])
EOF
```

### [26] TOOL RESULT — Bash · 2026-09-25 12:46:26 UTC

```
{"stdout": "def paired_boot(y, a, c, cb: ClusterBoot, stat: str = \"pooled\", stratum=None) -> dict:\n    \"\"\"Paired delta stat(a) - stat(c) on identical rows; percentile CI over cluster resamples; one-sided\n    p = share of resampled deltas <= 0. stat in {'pooled', 'strat'} (strat needs `stratum`).\"\"\"\n    y = np.asarray(y)\n    a = np.asarray(a, float)\n    c = np.asarray(c, float)\n    st = None if stratum is None else np.asarray(stratum)\n    f = (lambda yy, ss, hh: auroc(yy, ss)) if stat == \"pooled\" else strat_auroc\n    pa, pc = f(y, a, st), f(y, c, st)\n    da, dc, dd = [], [], []\n    for ix in cb.idx:\n        hh = None if st is None else st[ix]\n        xa, xc = f(y[ix], a[ix], hh), f(y[ix], c[ix], hh)\n        da.append(xa)\n        dc.append(xc)\n        dd.append(xa - xc)\n    dd_ = np.array([d for d in dd if not math.isnan(d)])\n    return {\"a\": pa, \"b\": pc, \"a_ci\": boot_ci(da), \"b_ci\": boot_ci(dc), \"delta\": pa - pc, \"ci\": boot_ci(dd),\n            \"p_one_sided_le0\": float(np.mean(dd_ <= 0)) if len(dd_) else None, \"se\": float(np.std(dd_)) if len(dd_) else None,\n            \"n\": int(len(y)), \"n_error\": int(y.sum()), \"n_correct\": int(len(y) - y.sum()), \"stat\": stat}\n\n\ndef boot_stat(y, s, cb: ClusterBoot, stat: str = \"pooled\", stratum=None) -> dict:\n    y = np.asarray(y)\n    s = np.asarray(s, float)\n    st = None if stratum is None else np.asarray(stratum)\n    f = (lambda yy, ss, hh: auroc(yy, ss)) if stat == \"pooled\" else strat_auroc\n    pt = f(y, s, st)\n    bs = [f(y[ix], s[ix], None if st is None else st[ix]) for ix in cb.idx]\n    return {\"auroc\": pt, \"ci\": boot_ci(bs)}\n\n\ndef delong(y, s1, s2) -> dict:\ndict_keys(['prereg_T1_sha256', 'guard', 'key_map', 'api_columns', 'population', 'api_coverage', 'cost', 'bar', 'a_head_on', 'criterion_a', 'b_s4', 'metrics_R_AB', 'c_vex', 'd_frontier', 'e_M3', 'f_complexity', 'g_contamination', 'h_recall_by_group', 'i_system', 'placebo', 'verdict', 'runtime_s', 'cost_ledger', 'figures'])\nc_score_align {'strat': 0.741, 'pooled': 0.782}\ng_score {'strat': 0.694, 'pooled': 0.748}\nnf_c_score {'strat': 0.686, 'pooled': 0.743}\np_peer_text {'strat': 0.753, 'pooled': 0.79}\np_text {'strat': 0.67, 'pooled': 0.693}\njudge_cheap_disg {'strat': 0.642, 'pooled': 0.696}\njudge_cheap_orig {'strat': 0.623, 'pooled': 0.635}\njudge_cheap2_disg {'strat': 0.644, 'pooled': 0.681}\njudge_cheap2_orig {'strat': 0.653, 'pooled': 0.7}\nL:judge_local_qwen8b_disg {'strat': 0.674, 'pooled': 0.71}\npeer_only {'strat': 0.694, 'pooled': 0.748}\njudge_cheap_disg_vfb {'strat': 0.642, 'pooled': 0.696}\njudge_cheap_orig_vfb {'strat': 0.624, 'pooled': 0.642}\n{\"best_frontier_view\": \"judge_strong_orig\", \"ratio\": 0.9573029948134515, \"ci\": [0.8874732219365781, 1.0344404378370433], \"auroc_c\": 0.7097246340858347, \"auroc_frontier\": 0.7413793103448276, \"n\": 284, \"delta\": {\"a\": \"c_score_align\", \"b\": \"judge_strong_orig\", \"stat\": \"pooled\", \"auroc_a\": 0.7097246340858347, \"auroc_b\": 0.7413793103448276, \"delta\": -0.031654676258992875, \"ci\": [-0.08528323049763684, 0.02441253463472301], \"p_one_sided_le0\": 0.865, \"se\": 0.028392750957405802, \"n\": 284, \"n_error\": 139, \"n_correct\": 145, \"n_sentences\": 207, \"delong_z\": -1.0946500977435083, \"delong_p\": 0.27366995867617\n{\"entered_api_columns\": [\"judge_cheap_disg\", \"judge_cheap_orig\", \"judge_cheap2_disg\", \"judge_cheap2_orig\", \"rt_nli_min\", \"rt_nli_fwd\", \"rt_nli_bwd\", \"rt_nli_contra\", \"rt_embed_cos\", \"sc5_eq_frac\", \"sc5_entropy\"], \"substituted\": {}, \"sets\": {\"S4_local\": [\"L:parse_fail\", \"L:pilot_joint_conflict\", \"L:pilot_arity_incons\", \"L:pilot_shape_incons\", \"L:pilot_dangling\", \"L:pilot_rerun_jacc\", \"L:rt_nli_min_local\", \"L:rt_nli_fwd_local\", \"L:rt_nli_bwd_local\", \"L:rt_nli_contra_local\", \"L:rt_embed_cos_local\", \"L:judge_local_qwen8b_disg\", \"L:judge_local_qwen8b_orig\", \"L:judge_local_llama8b_disg\", \"L:judge_local_llama8b_orig\", \"L:sc5_local_eq_frac\", \"L:sc5_local_entropy\"], \"S4_full\": [\"L:parse_fail\", \"L:pilot_joint_conflict\", \"L:pilot_arity_incons\", \"L:pilot_shape_incons\", \"L:pilot_dangling\", \"L:pilot_rerun_jacc\", \"L:rt_nli_min_local\", \"L:rt_nli_fwd_local\", \"L:rt_nli_bwd_local\", \"L:rt_nli_contra_local\", \"L:rt_embed_cos_local\", \"L:judge_local_qwen8b_disg\", \"L:judge_local_qwen8b_orig\", \"L:judge_local_llama8b_disg\", \"L:judge_local_llama8b_orig\", \"L:sc5_local_eq_frac\", \"L:sc5_local_entropy\", \"judge_cheap_disg\", \"judge_cheap_orig\", \"judge_cheap2_disg\", \"judge_cheap2_orig\", \"rt_nli_min\", \"rt_nli_fwd\", \"rt_nli_bwd\", \"rt_nli_contra\", \"rt_embed_cos\", \"sc5_eq_frac\", \"sc5_entropy\"], \"S4_API\": [\"L:parse_fail\", \"L:pilot_joint_conflict\", \"L:pilot_arity_incons\", \"L:pilot_shape_incons\", \"L:pilot_dangling\", \"L:pilot_rerun_jacc\", \"rt_nli_min\", \"rt_nli_fwd\", \"rt_nli_bwd\", \"rt_nli_contra\", \"rt_embed_cos\", \"L:rt\n{'n': 2686, 'n_error': 1822, 'n_correct': 864, 'n_sentences': 292}", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [27] ASSISTANT · 2026-09-25 12:46:46 UTC

```
Now building the 100-row curated subset.
```

### [28] TOOL CALL — Bash · 2026-09-25 12:46:46 UTC

```
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5; mkdir -p scripts; cat > scripts/make_mini_demo_data.py <<'EOF'
#!/usr/bin/env python3
"""Build mini_demo_data.json: a sentence-clustered, stratum-balanced 100-row subset of the T1 main population
(R_AB, E_POOL, parseable) from the artifact's full_method_out.json, plus the full-population reference numbers."""
import json
import random
from collections import defaultdict
from pathlib import Path

SRC = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6")
OUT = Path(__file__).resolve().parent.parent / "mini_demo_data.json"
N_PER_STRATUM = 25
MAX_PER_SENT = 3

d = json.loads((SRC / "full_method_out.json").read_text())
ex = d["datasets"][0]["examples"]
P = [e for e in ex if e["metadata_in_R_AB"] and e["metadata_pool"] == "E_POOL" and e["metadata_parse_ok"]]
rng = random.Random(0)
by_sent = defaultdict(list)
for e in P:
    by_sent[(e["metadata_strata"]["source_stratum"], e["metadata_sentence_id"])].append(e)
picked = []
for h in ("L25", "L20", "EXC", "CTRL"):
    sents = [s for (hh, s) in by_sent if hh == h]
    rng.shuffle(sents)
    # sentences with both labels AND a frontier-frame row first, then sentences with both labels, then the rest
    def pri(s):
        rows = by_sent[(h, s)]
        both = len({r["output"] for r in rows}) == 2
        frame = any(r["predict_judge_strong_orig"] != "NA" for r in rows)
        return (not both, not frame)
    sents.sort(key=pri)
    n = 0
    for s in sents:
        rows = by_sent[(h, s)][:]
        rng.shuffle(rows)
        rows.sort(key=lambda r: r["predict_judge_strong_orig"] == "NA")  # frame rows first
        take, labs = [], set()
        for r in rows:  # label mix inside the sentence
            if r["output"] not in labs or len(labs) == 2:
                take.append(r)
                labs.add(r["output"])
            if len(take) == MAX_PER_SENT:
                break
        take = take[:N_PER_STRATUM - n]
        picked += take
        n += len(take)
        if n >= N_PER_STRATUM:
            break


def slim(e):
    out = {"input": json.loads(e["input"]), "output": e["output"]}
    for k, v in e.items():
        if k.startswith("predict_"):
            out[k] = None if v == "NA" else float(v)
        elif k.startswith("metadata_"):
            out[k] = v
    return out


A = json.loads((SRC / "results" / "analysis_T1.json").read_text())
V = json.loads((SRC / "results" / "verdict_T1.json").read_text())
m = A["a_head_on"]["R_AB pooled"]["metrics"]
ref = {"population": A["population"],
       "auroc_R_AB": {k: {s: x.get("auroc") for s, x in v.items()} for k, v in m.items()},
       "criterion_a": V["criteria"]["a"], "criterion_b": V["criteria"]["b"], "criterion_d": V["criteria"]["d"],
       "frame_ratio": {k: A["d_frontier"]["ratio"][k] for k in ("ratio", "ci", "auroc_c", "auroc_frontier", "n")},
       "overall": V["overall_T1_this_artifact"]}
pre = json.loads((SRC / "prereg_T1.json").read_text())
data = {"metadata": {**d["metadata"],
                     "subset": f"{len(picked)} rows of the R_AB E_POOL PRIMARY population (n=2,686), "
                               f"<= {MAX_PER_SENT} rows per sentence, {N_PER_STRATUM} per source stratum, seed 0",
                     "thresholds": pre["thresholds"]},
        "reference_full_population": ref,
        "examples": [slim(e) for e in picked]}
OUT.write_text(json.dumps(data, indent=1, ensure_ascii=False))
print(OUT, len(picked))
EOF
python3 scripts/make_mini_demo_data.py && python3 - <<'EOF'
import json, collections
d=json.load(open('mini_demo_data.json'))
E=d['examples']
print(collections.Counter((e['metadata_strata']['source_stratum'],e['output']) for e in E))
print('sent',len({e['metadata_sentence_id'] for e in E}),'frame',sum(e['predict_judge_strong_orig'] is not None for e in E),
 'R_A', collections.Counter((e['metadata_strata']['source_stratum'],e['output']) for e in E if e['metadata_in_R_A']))
print(json.dumps(E[0],ensure_ascii=False)[:1500])
EOF
ls -la mini_demo_data.json
```

### [29] TOOL RESULT — Bash · 2026-09-25 12:46:46 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/mini_demo_data.json 100\nCounter({('L20', 'ERROR'): 17, ('L25', 'ERROR'): 14, ('CTRL', 'CORRECT'): 14, ('EXC', 'CORRECT'): 13, ('EXC', 'ERROR'): 12, ('L25', 'CORRECT'): 11, ('CTRL', 'ERROR'): 11, ('L20', 'CORRECT'): 8})\nsent 36 frame 52 R_A Counter({('EXC', 'CORRECT'): 11, ('CTRL', 'CORRECT'): 6, ('CTRL', 'ERROR'): 5, ('EXC', 'ERROR'): 4, ('L25', 'CORRECT'): 3, ('L20', 'CORRECT'): 3, ('L20', 'ERROR'): 3, ('L25', 'ERROR'): 1})\n{\"input\": {\"text\": \"A fuel x is suitable for an engine y in a vehicle z if x meets the performance requirements of y and is compatible with the fuel system of z.\", \"candidate_fol\": \"∀x∀y∀z (Fuel(x) ∧ Engine(y) ∧ Vehicle(z) → (Suitable(x, y, z) ↔ (MeetsPerformance(x, y) ∧ CompatibleWithFuelSystem(x, z))))\", \"system\": \"G2:qwen/qwen3-235b-a22b-2507\", \"prompt_variant\": \"fewshot_v1\"}, \"output\": \"CORRECT\", \"predict_c_score_align\": 1.0, \"predict_g_score\": 1.0, \"predict_nf_c_score\": 1.0, \"predict_nf_g_score\": 1.0, \"predict_p_peer_text\": 0.82412, \"predict_p_text\": 0.350778, \"predict_l2_bow\": 0.1, \"predict_l3_z3\": 0.0, \"predict_judge_cheap_disg\": 0.05, \"predict_judge_cheap_orig\": 0.0, \"predict_judge_cheap2_disg\": 0.377539, \"predict_judge_cheap2_orig\": 0.00522, \"predict_judge_strong_orig\": 0.9, \"predict_judge_strong_disg\": null, \"predict_judge_cheap_disg_vfb\": 0.05, \"predict_rt_nli_min\": 0.359328, \"predict_rt_nli_fwd\": 0.359328, \"predict_rt_nli_bwd\": 0.006218, \"predict_rt_nli_contra\": 0.003784, \"predict_rt_nli_min_alt\": 0.022395, \"predict_rt_embed_cos\": 0.101177, \"predict_sc5_eq_frac\": 1.0, \"predict_sc5_entropy\": 1.011404, \"predict_S4_full_oof\": 0.765816, \"predict_S4_local_oof\": 0.773453, \"predict_S4_full_plus_c_score_align_oof\": 0.881544, \"predict_PT_refit_oof\": 0.886247, \"predict_PT_refit_NF_oof\": 0.860968, \"predict_local_judge_local_qwen8b_disg\": 0.1, \"predict_local_judge_local_qwen8b_orig\": 0.05, \"predict_local_judge_local_llama8b_disg\": 0.320553, \"predict_local_rt_nli_min_local\": 0\n-rw-r--r-- 1 root root 249614 Sep 25 12:46 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [30] TOOL CALL — Bash · 2026-09-25 12:47:13 UTC

```
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5; python3 -c "
import json;d=json.load(open('mini_demo_data.json'));E=d['examples']
print(len({e['metadata_canonical_key'] for e in E}), len({e['metadata_item_id'] for e in E}))
print(d['metadata']['thresholds'])"; W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6; sed -n 411,437p $W/src/analyse_T1.py; sed -n 995,1030p $W/src/analyse_T1.py
```

### [31] TOOL RESULT — Bash · 2026-09-25 12:47:13 UTC

```
{"stdout": "100 100\n{'judges': 'flag if P(faithful) < 0.5 (oriented > 0.5), screen-frozen', 'consensus_PT': {'fused': 0.6902659323258526, 'text': 0.7809534183242605}, 'M3_operating_point': 'FA = 0.10 on E R_AB CORRECT rows (90th percentile), same for every metric'}\ndef consensus_costs(rows, P) -> dict:\n    \"\"\"FULL consensus $/item = (LLM-slot generation spend of the sentence's peer pool, from dataset E's per-row\n    metadata_cost_usd, summed over the sentence's E_POOL rows) / (#E_POOL candidates of the sentence) + z3 CPU seconds\n    (exp 5 secs_pairs, one core priced at $0.05/h). MARGINAL = z3 only. exp 5's own cost_usd_peer_text is reported too.\"\"\"\n    spend = defaultdict(float)\n    ncand = Counter()\n    for x in rows:\n        if x[\"pool\"] == \"E_POOL\":\n            spend[x[\"sentence_id\"]] += float(x.get(\"gen_cost_usd\") or 0.0)\n            ncand[x[\"sentence_id\"]] += 1\n    full, marg, e5 = [], [], []\n    by = {x[\"canonical_key\"]: x for x in rows}\n    for k in P:\n        x = by[k]\n        secs = float(x.get(\"e5_secs_pairs\") or 0.0)\n        c = AB.consensus_cost_per_item(spend[x[\"sentence_id\"]], ncand[x[\"sentence_id\"]], secs)\n        full.append(c[\"full\"])\n        marg.append(c[\"marginal\"])\n        if x.get(\"e5_cost_usd_peer_text\") is not None:\n            e5.append(float(x[\"e5_cost_usd_peer_text\"]))\n    return {\"full_mean_usd_per_item\": float(np.mean(full)), \"marginal_mean_usd_per_item\": float(np.mean(marg)),\n            \"exp5_cost_usd_peer_text_mean\": float(np.mean(e5)) if e5 else None,\n            \"z3_secs_mean\": float(np.mean([float(by[k].get(\"e5_secs_pairs\") or 0) for k in P])),\n            \"rule\": \"FULL = sentence peer-pool generation spend / candidates per sentence + z3 CPU ($0.05/core-hour); MARGINAL = z3 only\"}\n\n\n# ===================================================================================================== (b)\ndef verdict(A) -> dict:\n    ca = A[\"criterion_a\"].get(\"judge_cheap_disg\", {})\n    cb = A[\"b_s4\"].get(\"criterion_b\", {})\n    cd = A[\"d_frontier\"].get(\"criterion_d\", {})\n    cv = A[\"c_vex\"].get(\"vex_rule\", {})\n    cm = A[\"e_M3\"].get(\"criterion_M3\", {})\n    a, b, d, v = ca.get(\"holds\"), cb.get(\"holds\"), cd.get(\"holds\"), cv.get(\"holds\")\n\n    def lab(x):\n        return \"CONFIRMED\" if x is True else (\"DISCONFIRMED\" if x is False else \"UNTESTABLE\")\n    if not A[\"bar\"][\"available\"]:\n        overall = \"UNTESTABLE (API bar missing)\"\n    elif a is False:\n        overall = \"DISCONFIRMED\"\n    elif a and b and d and v:\n        overall = \"CONFIRMED\"\n    elif a and not b:\n        overall = \"PARTIAL (a holds, b fails: consensus redundant with the API-judge stack)\"\n    elif a and b and not v:\n        overall = \"PARTIAL (a and b hold, VEX fails: aligner confound not excluded)\"\n    elif a and b and v and d is False:\n        overall = \"PARTIAL (a, b, VEX hold; d fails: frontier judge not matched at <=10% cost)\"\n    elif a and b and v and d is None:\n        overall = \"PARTIAL (a, b, VEX hold; d untestable: no frontier scores)\"\n    else:\n        overall = \"PARTIAL\"\n    out = {\"criteria\": {\"a\": {\"status\": lab(a), **ca}, \"b\": {\"status\": lab(b), **cb}, \"d\": {\"status\": lab(d), **cd},\n                        \"VEX\": {\"status\": lab(v), **cv}, \"M3\": {\"status\": lab(cm.get(\"holds\")), **cm},\n                        \"c\": {\"status\": \"OTHER ARTIFACT (R_COMP-SIG)\"}, \"e\": {\"status\": \"OTHER ARTIFACT\"}},\n           \"overall_T1_this_artifact\": overall}\n    best = A[\"bar\"].get(\"BEST_API_CHEAP\")\n    if best and best in A[\"criterion_a\"]:\n        cab = A[\"criterion_a\"][best]\n        out[\"robustness_BEST_API_CHEAP\"] = {\"bar\": best, \"criterion_a\": lab(cab.get(\"holds\")), **cab}\n    out[\"local_bar_secondary\"] = {\"bar\": LOCAL_BAR, \"criterion_a\": lab(A[\"criterion_a\"].get(LOCAL_BAR, {}).get(\"holds\"))}\n    return out", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [32] TOOL CALL — Bash · 2026-09-25 12:47:17 UTC

```
mkdir -p /tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/576c8881-bdc5-43aa-a926-9186f688f0d2/scratchpad; echo ok
```

### [33] TOOL RESULT — Bash · 2026-09-25 12:47:17 UTC

```
{"stdout": "ok", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [34] TOOL CALL — Write · 2026-09-25 12:49:57 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [35] TOOL RESULT — Write · 2026-09-25 12:49:57 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [36] TOOL CALL — Bash · 2026-09-25 12:50:05 UTC

```
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5; SP=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/576c8881-bdc5-43aa-a926-9186f688f0d2/scratchpad
python3 $SP/build_nb.py '{"B":10,"B_COMPLEXITY":10,"N_PLACEBO":5}' && \
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_7GxreYjATkC5-321ae79c96cc && \
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_7GxreYjATkC5-321ae79c96cc/bin/python jupyter ipykernel && \
time /tmp/aii_nb_test_envs/art_7GxreYjATkC5-321ae79c96cc/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -30
```

### [37] TOOL RESULT — Bash · 2026-09-25 12:50:33 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/code_demo.ipynb 28 cells {'B': 10, 'B_COMPLEXITY': 10, 'N_PLACEBO': 5}\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 297793 bytes to code_demo.ipynb\n\nreal\t0m22.460s\nuser\t0m17.913s\nsys\t0m2.374s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [38] TOOL CALL — Bash · 2026-09-25 12:50:35 UTC

```
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5; python3 - <<'EOF'
import json
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    if c['cell_type']!='code': continue
    for o in c['outputs']:
        if o['output_type']=='stream': print(''.join(o['text'])[:3000])
        elif o['output_type']=='error': print('ERR', o['ename'], o['evalue'])
        elif o['output_type'] in('display_data','execute_result'): print('[display]', list(o['data']))
    print('-----')
EOF
```

### [39] TOOL RESULT — Bash · 2026-09-25 12:50:37 UTC

```
{"stdout": "-----\n-----\n-----\nT1 head-on API bar on held-out dataset E | verdict of the full run: CONFIRMED\n100 rows of the R_AB E_POOL PRIMARY population (n=2,686), <= 3 rows per sentence, 25 per source stratum, seed 0\nrows: 100\n\nexample row:\n  text: A fuel x is suitable for an engine y in a vehicle z if x meets the performance requirements of y and is compatible with the fuel system of z. \n  fol : ∀x∀y∀z (Fuel(x) ∧ Engine(y) ∧ Vehicle(z) → (Suitable(x, y, z) ↔ (MeetsPerformance(x, y) ∧ CompatibleWithFuelSystem(x, z)))) \n  system: G2:qwen/qwen3-235b-a22b-2507 | label: CORRECT | c_score_align: 1.0 | judge_cheap_disg: 0.05\n\n-----\n-----\n-----\n-----\n100 rows, 15 API columns, 5 S4 stacks; R_AB labels 100, R_A labels 36\n\n-----\n12:50:28|INFO   |population {'n': 100, 'n_error': 54, 'n_correct': 46, 'n_sentences': 36}   (full run: {'n': 2686, 'n_error': 1822, 'n_correct': 864, 'n_sentences': 292})\n\n12:50:28|INFO   |(a) R_AB pooled: n=100 c_score_align-cheap_disg[strat]=0.092, p_peer_text-cheap_disg[strat]=0.015\n\n12:50:28|INFO   |(a) R_AB long (L25+L20+EXC): n=75 c_score_align-cheap_disg[strat]=0.098, p_peer_text-cheap_disg[strat]=0.039\n\n12:50:28|INFO   |(a) R_AB L25: n=25 c_score_align-cheap_disg[pooled]=0.042, p_peer_text-cheap_disg[pooled]=0.101\n\n12:50:28|INFO   |(a) R_AB L20: n=25 c_score_align-cheap_disg[pooled]=-0.015, p_peer_text-cheap_disg[pooled]=-0.004\n\n12:50:28|INFO   |(a) R_AB EXC: n=25 c_score_align-cheap_disg[pooled]=0.250, p_peer_text-cheap_disg[pooled]=0.016\n\n12:50:28|INFO   |(a) R_AB CTRL: n=25 c_score_align-cheap_disg[pooled]=0.075, p_peer_text-cheap_disg[pooled]=-0.055\n\n12:50:28|INFO   |(a) R_A L20+EXC: n=21 c_score_align-cheap_disg[strat]=0.377, p_peer_text-cheap_disg[strat]=0.038\n\n12:50:28|INFO   |(a) R_A L20+EXC+CTRL: n=32 c_score_align-cheap_disg[strat]=0.349, p_peer_text-cheap_disg[strat]=0.060\n\n12:50:28|INFO   |(a) done in 0.4s\n\n\nCriterion (a) vs judge_cheap_disg on the DEMO SUBSET\n  R_AB strat delta  +0.092  CI [-0.031  0.212]  n=100\n  long strat delta  +0.098  CI [0.055 0.22 ]  n=75\n  R_A L20+EXC delta +0.377  n=21\n  holds on subset: False\nFULL RUN (n=2686): R_AB strat +0.099 [0.049 0.146], long +0.116 [0.07  0.163], R_A L20+EXC +0.299 -> CONFIRMED\n\n-----\n  nested_strat                     delta -0.022  CI [-0.091  0.017]  (0.808 vs 0.830, n=100)\n  nested_pooled                    delta -0.029  CI [-0.071 -0.008]  (0.798 vs 0.826, n=100)\n  c_alone_minus_S4_full_strat      delta -0.064  CI [-0.149  0.042]  (0.766 vs 0.830, n=100)\nFULL RUN: nested strat +0.039 [0.021 0.057], permutation-null p95 0.009 -> CONFIRMED\n\n-----\n12:50:29|INFO   |describe done in 0.2s\n\nmetric                              pooled   strat  AUPRC  ties rec@FA.10\nc_score_align                        0.738   0.766  0.742  0.13      0.48\ng_score                              0.740   0.743  0.701  0.19      0.33\nnf_c_score                           0.737   0.746  0.724  0.16      0.31\np_peer_text                          0.687   0.689  0.735  0.00      0.41\np_text                               0.600   0.577  0.676  0.04      0.30\nl2_bow                               0.577   0.551  0.631  0.23      0.26\nl3_z3                                0.588   0.615  0.660  0.17      0.28\njudge_cheap_disg                     0.697   0.674  0.666  0.26      0.31\njudge_cheap_orig                     0.646   0.645  0.682  0.39      0.35\njudge_cheap2_disg                    0.664   0.664  0.682  0.01      0.22\njudge_cheap2_orig                    0.696   0.677  0.734  0.00      0.33\nL:judge_local_qwen8b_disg            0.716   0.713  0.739  0.15      0.44\nrt_nli_min                           0.600   0.594  0.654  0.00      0.22\nrt_nli_fwd                           0.644   0.629  0.698  0.00      0.24\nrt_nli_bwd                           0.573   0.606  0.624  0.00      0.15\nrt_nli_contra                        0.597   0.589  0.649  0.00      0.17\nrt_nli_min_alt                       0.654   0.637  0.677  0.00      0.24\nrt_embed_cos                         0.595   0.594  0.629  0.00      0.17\nsc5_eq_frac                          0.643   0.637  0.623  0.54      0.35\nsc5_entropy                          0.575   0.573  0.579  0.14      0.15\nL:rt_nli_min_local                   0.626   0.603  0.640  0.00      0.22\nL:sc5_local_eq_frac                  0.724   0.719  0.692  0.41      0.28\nL:judge_local_qwen8b_orig            0.703   0.744  0.738  0.16      0.35\nL:judge_local_llama8b_disg           0.603   0.565  0.609  0.00      0.09\nL:parse_fail                         0.500   0.500  0.540  1.00      0.15\nL:pilot_rerun_jacc                   0.757   0.752  0.754  0.01      0.41\nS4_full_oof                          0.826   0.830  0.852  0.00      0.56\nS4_local_oof                         0.812   0.820  0.838  0.00      0.44\nS4_full_plus_c_score_align_oof       0.798   0.808  0.852  0.00      0.48\nPT_refit_oof                         0.692   0.709  0.709  0.00      0.26\nPT_refit_NF_oof                      0.686   0.683  0.704  0.00      0.24\n\n-----\nframe rows in subset: 52 (25 ERROR / 27 CORRECT)\n  AUROC c_score_align 0.706 vs frontier 0.703 -> ratio 1.004 CI [0.879 1.171]\n  nested [strong+c] - [strong]: +0.006 CI [-0.021  0.042]\n  cost/item: consensus $1.2e-04 vs frontier $3.65e-03 (<=10%: True)\n  criterion (d) on subset: True\nFULL RUN (frame n=284): ratio 0.957 [0.887 1.034] (AUROC 0.710 vs 0.741) -> CONFIRMED\n\n-----\n12:50:29|INFO   |(f) complexity done in 0.2s\n\n\nwords:\n     <12 n= 24  c_score_align 0.906  judge_cheap_disg 0.711  delta +0.195\n   12-19 n= 23  c_score_align 0.671  judge_cheap_disg 0.571  delta +0.099\n   20-24 n= 28  c_score_align 0.661  judge_cheap_disg 0.733  delta -0.072\n   25-34 n= 24  c_score_align 0.654  judge_cheap_disg 0.607  delta +0.046\n    >=35 n=  1  untestable on subset\n\nn_conditions:\n     <=1 n= 32  c_score_align 0.883  judge_cheap_disg 0.742  delta +0.141\n       2 n=  6  untestable on subset\n       3 n= 18  c_score_align 0.856  judge_cheap_disg 0.625  delta +0.231\n      4+ n= 44  c_score_align 0.652  judge_cheap_disg 0.723  delta -0.072\n\n-----\n{\n \"shuffled_label_auroc_c_score_align\": 0.514573268921095,\n \"shuffled_label_strat_delta_c_minus_cheapdisg\": {\n  \"mean\": -0.015730388405984695,\n  \"p2.5\": -0.11759441560766061,\n  \"p97.5\": 0.06540663886229998\n }\n}\n\n-----\nmetric                             subset strat subset pooled FULL strat FULL pooled\nc_score_align                             0.766         0.738      0.741       0.782\ng_score                                   0.743         0.740      0.694       0.748\nnf_c_score                                0.746         0.737      0.686       0.743\np_peer_text                               0.689         0.687      0.753       0.790\np_text                                    0.577         0.600      0.670       0.693\njudge_cheap_disg                          0.674         0.697      0.642       0.696\njudge_cheap_orig                          0.645         0.646      0.623       0.635\njudge_cheap2_disg                         0.664         0.664      0.644       0.681\njudge_cheap2_orig                         0.677         0.696      0.653       0.700\nL:judge_local_qwen8b_disg                 0.713         0.716      0.674       0.710\nS4_full_oof                               0.830         0.826        -           -  \nS4_full_plus_c_score_align_oof            0.808         0.798        -           -  \nrt_nli_min                                0.594         0.600        -           -  \nsc5_eq_frac                               0.637         0.643        -           -  \n\nCriteria on the demo subset:  (a) False | (b) nested CI>0: False | (d) True\nFull run verdict: CONFIRMED | a: CONFIRMED | b: CONFIRMED | d: CONFIRMED\n\n[display] ['image/png', 'text/plain']\n-----", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [40] ASSISTANT · 2026-09-25 12:50:45 UTC

```
The notebook runs end to end in about 22 s at the minimum config. Next I'm adding the missing full-run reference AUROCs and then scaling the bootstrap toward the original values.
```

### [41] TOOL CALL — Bash · 2026-09-25 12:50:45 UTC

```
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5; python3 - <<'EOF'
p='scripts/make_mini_demo_data.py'
s=open(p).read()
s=s.replace('''       "auroc_R_AB": {k: {s: x.get("auroc") for s, x in v.items()} for k, v in m.items()},''','''       "auroc_R_AB": {**{k: {"pooled": v.get("auroc"), "strat": v.get("strat", {}).get("auroc")}
                         for k, v in A["metrics_R_AB"].items() if not v.get("untestable")},
                      **{k: {s: x.get("auroc") for s, x in v.items()} for k, v in m.items()}},''')
open(p,'w').write(s)
EOF
python3 scripts/make_mini_demo_data.py && python3 -c "
import json;d=json.load(open('mini_demo_data.json'));r=d['reference_full_population']['auroc_R_AB'];print({k:r[k] for k in ['S4_full_oof','S4_full_plus_c_score_align_oof','rt_nli_min','c_score_align']})"
```

### [42] TOOL RESULT — Bash · 2026-09-25 12:50:45 UTC

```
{"stdout": "/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/mini_demo_data.json 100\n{'S4_full_oof': {'pooled': 0.7765244491198113, 'strat': 0.7350930963751415}, 'S4_full_plus_c_score_align_oof': {'pooled': 0.8066049721510753, 'strat': 0.773868073209944}, 'rt_nli_min': {'pooled': 0.6392824201122088, 'strat': 0.605902571534922}, 'c_score_align': {'strat': 0.7414618757606236, 'pooled': 0.7823775511241208}}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [43] TOOL CALL — Edit · 2026-09-25 12:50:57 UTC

```
File: /tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/576c8881-bdc5-43aa-a926-9186f688f0d2/scratchpad/build_nb.py
OLD: The subset's CIs are wide because it has only about 36 sentence clusters. The full run's conclusions rest on 292.
""")
NEW: The subset's CIs are wide because it has only about 36 sentence clusters. The full run's conclusions rest on 292.

**Reading the subset honestly.** With 100 rows, the point estimates land near the full-run values:
- c_score_align's stratified AUROC is about 0.74–0.77 against about 0.64–0.68 for the cheap judges;
- the Δ versus judge_cheap_disg is about +0.09.

The subset's bootstrap CIs, however, can straddle 0. Its S4 stacks are the full-population out-of-fold predictions
evaluated on only 100 rows, so the nested gain of criterion (b) does not reproduce here; on the full population it is
+0.039 [0.021, 0.057]. The confirmatory verdict (CONFIRMED) comes from the full population, whose values are printed
beside each subset number.
""")
```

### [44] TOOL RESULT — Edit · 2026-09-25 12:50:57 UTC

```
{"filePath": "/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/576c8881-bdc5-43aa-a926-9186f688f0d2/scratchpad/build_nb.py", "oldString": "The subset's CIs are wide because it has only about 36 sentence clusters. The full run's conclusions rest on 292.\n\"\"\")", "newString": "The subset's CIs are wide because it has only about 36 sentence clusters. The full run's conclusions rest on 292.\n\n**Reading the subset honestly.** With 100 rows, the point estimates land near the full-run values:\n- c_score_align's stratified AUROC is about 0.74–0.77 against about 0.64–0.68 for the cheap judges;\n- the Δ versus judge_cheap_disg is about +0.09.\n\nThe subset's bootstrap CIs, however, can straddle 0. Its S4 stacks are the full-population out-of-fold predictions\nevaluated on only 100 rows, so the nested gain of criterion (b) does not reproduce here; on the full population it is\n+0.039 [0.021, 0.057]. The confirmatory verdict (CONFIRMED) comes from the full population, whose values are printed\nbeside each subset number.\n\"\"\")", "originalFile": null, "structuredPatch": [{"oldStart": 876, "oldLines": 6, "newStart": 876, "newLines": 15, "lines": [" 4. AUROC by number of conditions.", " ", " The subset's CIs are wide because it has only about 36 sentence clusters. The full run's conclusions rest on 292.", "+", "+**Reading the subset honestly.** With 100 rows, the point estimates land near the full-run values:", "+- c_score_align's stratified AUROC is about 0.74–0.77 against about 0.64–0.68 for the cheap judges;", "+- the Δ versus judge_cheap_disg is about +0.09.", "+", "+The subset's bootstrap CIs, however, can straddle 0. Its S4 stacks are the full-population out-of-fold predictions", "+evaluated on only 100 rows, so the nested gain of criterion (b) does not reproduce here; on the full population it is", "++0.039 [0.021, 0.057]. The confirmatory verdict (CONFIRMED) comes from the full population, whose values are printed", "+beside each subset number.", " \"\"\")", " ", " code(r'''"]}], "userModified": false, "replaceAll": false}
```

### [45] TOOL CALL — Bash · 2026-09-25 12:50:57 UTC

```
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5; SP=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/576c8881-bdc5-43aa-a926-9186f688f0d2/scratchpad
python3 $SP/build_nb.py '{"B":200,"B_COMPLEXITY":100,"N_PLACEBO":20}' && \
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_7GxreYjATkC5-321ae79c96cc && \
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_7GxreYjATkC5-321ae79c96cc/bin/python jupyter ipykernel && \
time /tmp/aii_nb_test_envs/art_7GxreYjATkC5-321ae79c96cc/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -3; grep -o 'done in [0-9.]*s' code_demo.ipynb
```

### [46] TOOL RESULT — Bash · 2026-09-25 12:51:25 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/code_demo.ipynb 28 cells {'B': 200, 'B_COMPLEXITY': 100, 'N_PLACEBO': 20}\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 298402 bytes to code_demo.ipynb\n\nreal\t0m26.566s\nuser\t0m22.106s\nsys\t0m2.672s\ndone in 2.8s\ndone in 1.3s\ndone in 1.0s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [47] ASSISTANT · 2026-09-25 12:51:33 UTC

```
Fast at B = 200. Moving to the full original values (B = 2000, B_COMPLEXITY = 1000, 200 placebo reps).
```

### [48] TOOL CALL — Bash · 2026-09-25 12:51:33 UTC

```
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5; SP=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/576c8881-bdc5-43aa-a926-9186f688f0d2/scratchpad
python3 $SP/build_nb.py '{"B":2000,"B_COMPLEXITY":1000,"N_PLACEBO":200}' && \
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_7GxreYjATkC5-321ae79c96cc && \
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_7GxreYjATkC5-321ae79c96cc/bin/python jupyter ipykernel && \
time /tmp/aii_nb_test_envs/art_7GxreYjATkC5-321ae79c96cc/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -3; python3 - <<'EOF'
import json
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    if c['cell_type']!='code': continue
    for o in c['outputs']:
        if o['output_type']=='stream': print(''.join(o['text'])[-1800:])
        elif o['output_type']=='error': print('ERR', o['ename'], o['evalue'])
        elif o['output_type'] in('display_data',): 
            import base64; open('/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/576c8881-bdc5-43aa-a926-9186f688f0d2/scratchpad/fig.png','wb').write(base64.b64decode(o['data']['image/png']))
EOF
```

### [49] TOOL RESULT — Bash · 2026-09-25 12:52:51 UTC

```
{"stdout": "wrote /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5/code_demo.ipynb 28 cells {'B': 2000, 'B_COMPLEXITY': 1000, 'N_PLACEBO': 200}\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 297978 bytes to code_demo.ipynb\n\nreal\t1m14.393s\nuser\t1m10.349s\nsys\t0m2.506s\nT1 head-on API bar on held-out dataset E | verdict of the full run: CONFIRMED\n100 rows of the R_AB E_POOL PRIMARY population (n=2,686), <= 3 rows per sentence, 25 per source stratum, seed 0\nrows: 100\n\nexample row:\n  text: A fuel x is suitable for an engine y in a vehicle z if x meets the performance requirements of y and is compatible with the fuel system of z. \n  fol : ∀x∀y∀z (Fuel(x) ∧ Engine(y) ∧ Vehicle(z) → (Suitable(x, y, z) ↔ (MeetsPerformance(x, y) ∧ CompatibleWithFuelSystem(x, z)))) \n  system: G2:qwen/qwen3-235b-a22b-2507 | label: CORRECT | c_score_align: 1.0 | judge_cheap_disg: 0.05\n\n100 rows, 15 API columns, 5 S4 stacks; R_AB labels 100, R_A labels 36\n\n12:51:54|INFO   |population {'n': 100, 'n_error': 54, 'n_correct': 46, 'n_sentences': 36}   (full run: {'n': 2686, 'n_error': 1822, 'n_correct': 864, 'n_sentences': 292})\n\n12:52:00|INFO   |(a) R_AB pooled: n=100 c_score_align-cheap_disg[strat]=0.092, p_peer_text-cheap_disg[strat]=0.015\n\n12:52:06|INFO   |(a) R_AB long (L25+L20+EXC): n=75 c_score_align-cheap_disg[strat]=0.098, p_peer_text-cheap_disg[strat]=0.039\n\n12:52:07|INFO   |(a) R_AB L25: n=25 c_score_align-cheap_disg[pooled]=0.042, p_peer_text-cheap_disg[pooled]=0.101\n\n12:52:08|INFO   |(a) R_AB L20: n=25 c_score_align-cheap_disg[pooled]=-0.015, p_peer_text-cheap_disg[pooled]=-0.004\n\n12:52:09|INFO   |(a) R_AB EXC: n=25 c_score_align-cheap_disg[pooled]=0.250, p_peer_text-cheap_disg[pooled]=0.016\n\n12:52:10|INFO   |(a) R_AB CTRL: n=25 c_score_align-cheap_disg[pooled]=0.075, p_peer_text-cheap_disg[pooled]=-0.055\n\n12:52:14|INFO   |(a) R_A L20+EXC: n=21 c_score_align-cheap_disg[strat]=0.377, p_peer_text-cheap_disg[strat]=0.038\n\n12:52:19|INFO   |(a) R_A L20+EXC+CTRL: n=32 c_score_align-cheap_disg[strat]=0.349, p_peer_text-cheap_disg[strat]=0.060\n\n12:52:19|INFO   |(a) done in 25.3s\n\n\nCriterion (a) vs judge_cheap_disg on the DEMO SUBSET\n  R_AB strat delta  +0.092  CI [-0.053  0.244]  n=100\n  long strat delta  +0.098  CI [-0.066  0.278]  n=75\n  R_A L20+EXC delta +0.377  n=21\n  holds on subset: False\nFULL RUN (n=2686): R_AB strat +0.099 [0.049 0.146], long +0.116 [0.07  0.163], R_A L20+EXC +0.299 -> CONFIRMED\n\n  nested_strat                     delta -0.022  CI [-0.101  0.053]  (0.808 vs 0.830, n=100)\n  nested_pooled                    delta -0.029  CI [-0.08   0.017]  (0.798 vs 0.826, n=100)\n  c_alone_minus_S4_full_strat      delta -0.064  CI [-0.188  0.03 ]  (0.766 vs 0.830, n=100)\nFULL RUN: nested strat +0.039 [0.021 0.057], permutation-null p95 0.009 -> CONFIRMED\n\n12:52:37|INFO   |describe done in 11.5s\n\n  0.660  0.17      0.28\njudge_cheap_disg                     0.697   0.674  0.666  0.26      0.31\njudge_cheap_orig                     0.646   0.645  0.682  0.39      0.35\njudge_cheap2_disg                    0.664   0.664  0.682  0.01      0.22\njudge_cheap2_orig                    0.696   0.677  0.734  0.00      0.33\nL:judge_local_qwen8b_disg            0.716   0.713  0.739  0.15      0.44\nrt_nli_min                           0.600   0.594  0.654  0.00      0.22\nrt_nli_fwd                           0.644   0.629  0.698  0.00      0.24\nrt_nli_bwd                           0.573   0.606  0.624  0.00      0.15\nrt_nli_contra                        0.597   0.589  0.649  0.00      0.17\nrt_nli_min_alt                       0.654   0.637  0.677  0.00      0.24\nrt_embed_cos                         0.595   0.594  0.629  0.00      0.17\nsc5_eq_frac                          0.643   0.637  0.623  0.54      0.35\nsc5_entropy                          0.575   0.573  0.579  0.14      0.15\nL:rt_nli_min_local                   0.626   0.603  0.640  0.00      0.22\nL:sc5_local_eq_frac                  0.724   0.719  0.692  0.41      0.28\nL:judge_local_qwen8b_orig            0.703   0.744  0.738  0.16      0.35\nL:judge_local_llama8b_disg           0.603   0.565  0.609  0.00      0.09\nL:parse_fail                         0.500   0.500  0.540  1.00      0.15\nL:pilot_rerun_jacc                   0.757   0.752  0.754  0.01      0.41\nS4_full_oof                          0.826   0.830  0.852  0.00      0.56\nS4_local_oof                         0.812   0.820  0.838  0.00      0.44\nS4_full_plus_c_score_align_oof       0.798   0.808  0.852  0.00      0.48\nPT_refit_oof                         0.692   0.709  0.709  0.00      0.26\nPT_refit_NF_oof                      0.686   0.683  0.704  0.00      0.24\n\nframe rows in subset: 52 (25 ERROR / 27 CORRECT)\n  AUROC c_score_align 0.706 vs frontier 0.703 -> ratio 1.004 CI [0.865 1.198]\n  nested [strong+c] - [strong]: +0.006 CI [-0.049  0.061]\n  cost/item: consensus $1.2e-04 vs frontier $3.65e-03 (<=10%: True)\n  criterion (d) on subset: True\nFULL RUN (frame n=284): ratio 0.957 [0.887 1.034] (AUROC 0.710 vs 0.741) -> CONFIRMED\n\n12:52:48|INFO   |(f) complexity done in 9.5s\n\n\nwords:\n     <12 n= 24  c_score_align 0.906  judge_cheap_disg 0.711  delta +0.195\n   12-19 n= 23  c_score_align 0.671  judge_cheap_disg 0.571  delta +0.099\n   20-24 n= 28  c_score_align 0.661  judge_cheap_disg 0.733  delta -0.072\n   25-34 n= 24  c_score_align 0.654  judge_cheap_disg 0.607  delta +0.046\n    >=35 n=  1  untestable on subset\n\nn_conditions:\n     <=1 n= 32  c_score_align 0.883  judge_cheap_disg 0.742  delta +0.141\n       2 n=  6  untestable on subset\n       3 n= 18  c_score_align 0.856  judge_cheap_disg 0.625  delta +0.231\n      4+ n= 44  c_score_align 0.652  judge_cheap_disg 0.723  delta -0.072\n\n{\n \"shuffled_label_auroc_c_score_align\": 0.5005766908212561,\n \"shuffled_label_strat_delta_c_minus_cheapdisg\": {\n  \"mean\": 6.173238432766182e-05,\n  \"p2.5\": -0.1755536274070756,\n  \"p97.5\": 0.17636871613485852\n }\n}\n\nmetric                             subset strat subset pooled FULL strat FULL pooled\nc_score_align                             0.766         0.738      0.741       0.782\ng_score                                   0.743         0.740      0.694       0.748\nnf_c_score                                0.746         0.737      0.686       0.743\np_peer_text                               0.689         0.687      0.753       0.790\np_text                                    0.577         0.600      0.670       0.693\njudge_cheap_disg                          0.674         0.697      0.642       0.696\njudge_cheap_orig                          0.645         0.646      0.623       0.635\njudge_cheap2_disg                         0.664         0.664      0.644       0.681\njudge_cheap2_orig                         0.677         0.696      0.653       0.700\nL:judge_local_qwen8b_disg                 0.713         0.716      0.674       0.710\nS4_full_oof                               0.830         0.826      0.735       0.777\nS4_full_plus_c_score_align_oof            0.808         0.798      0.774       0.807\nrt_nli_min                                0.594         0.600      0.606       0.639\nsc5_eq_frac                               0.637         0.643      0.598       0.656\n\nCriteria on the demo subset:  (a) False | (b) nested CI>0: False | (d) True\nFull run verdict: CONFIRMED | a: CONFIRMED | b: CONFIRMED | d: CONFIRMED", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [50] ASSISTANT · 2026-09-25 12:52:55 UTC

```
Full original parameters run in 74 s, well inside the 600 s budget. Checking the figure.
```

### [51] TOOL CALL — Read · 2026-09-25 12:52:55 UTC

```
/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/576c8881-bdc5-43aa-a926-9186f688f0d2/scratchpad/fig.png
```

### [52] TOOL RESULT — Read · 2026-09-25 12:52:55 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [53] ASSISTANT · 2026-09-25 12:53:13 UTC

```
The figure renders correctly. Next: making the helper scripts free of absolute server paths, then writing the verification, manifest, README and struct output.
```

### [54] TOOL CALL — Bash · 2026-09-25 12:53:13 UTC

```
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5; SP=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-3-art-7GxreYjATkC5/576c8881-bdc5-43aa-a926-9186f688f0d2/scratchpad
cp $SP/build_nb.py scripts/build_notebook.py
python3 - <<'EOF'
import re
p='scripts/build_notebook.py'; s=open(p).read()
s=re.sub(r'OUT = Path\(".*?"\)', 'OUT = Path(__file__).resolve().parent.parent / "code_demo.ipynb"', s)
s=s.replace('CFG = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}','# usage: python scripts/build_notebook.py \'{"B": 2000, "B_COMPLEXITY": 1000, "N_PLACEBO": 200}\'\nCFG = json.loads(sys.argv[1]) if len(sys.argv) > 1 else {}')
open(p,'w').write(s)
p='scripts/make_mini_demo_data.py'; s=open(p).read()
s=re.sub(r'SRC = Path\(".*?"\)', 'SRC = Path(sys.argv[1])  # the T1 artifact directory (holds full_method_out.json, results/, prereg_T1.json)', s)
s=s.replace('import json\nimport random','import json\nimport random\nimport sys')
s=s.replace('"""Build mini_demo_data.json','"""Usage: python scripts/make_mini_demo_data.py <T1_artifact_dir>\n\nBuild mini_demo_data.json')
open(p,'w').write(s)
EOF
grep -n "ai-inventor" scripts/*.py; md5sum mini_demo_data.json; python3 scripts/make_mini_demo_data.py /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_3/gen_art/gen_art_experiment_6 >/dev/null; md5sum mini_demo_data.json
python3 - <<'EOF'
import json
nb=json.load(open('code_demo.ipynb')); src='\n'.join(''.join(c['source']) for c in nb['cells'])
print('url exact:', 'GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-3/experiment-6/demo/mini_demo_data.json"' in src)
print('urlopen:', 'urllib.request.urlopen(GITHUB_DATA_URL)' in src, '| errors:', sum(o['output_type']=='error' for c in nb['cells'] if c['cell_type']=='code' for o in c['outputs']))
print('abs paths in nb:', 'ai-inventor/aii_data' in src)
EOF
ls -la
```

### [55] TOOL RESULT — Bash · 2026-09-25 12:53:13 UTC

```
{"stdout": "scripts/build_notebook.py:120:GITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-3/experiment-6/demo/mini_demo_data.json\"\nb15260380e572ce1ee7b9878fe014fc0  mini_demo_data.json\nb15260380e572ce1ee7b9878fe014fc0  mini_demo_data.json\nurl exact: True\nurlopen: True | errors: 0\nabs paths in nb: False\ntotal 4958\ndrwxr-xr-x 4 root root 1099755 Sep 25 12:50 .\ndrwxr-xr-x 6 root root 2000196 Sep 25 12:51 ..\ndrwxr-xr-x 2 root root       1 Sep 25 12:44 .aii\n-rw------- 1 root root      54 Sep 25 12:45 .aii_claude_session.json\n-rw-r--r-- 1 root root  419769 Sep 25 12:53 .repl_agent.ptylog\n-rw-r--r-- 1 root root  298044 Sep 25 12:52 code_demo.ipynb\n-rw-r--r-- 1 root root  252412 Sep 25 12:53 mini_demo_data.json\ndrwxr-xr-x 2 root root 1005008 Sep 25 12:53 scripts", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [56] TOOL CALL — Bash · 2026-09-25 12:53:31 UTC

````
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_3/art_7GxreYjATkC5; grep -c "ai-inventor/aii_data" mini_demo_data.json; grep -o "B = [0-9]*\|N_PLACEBO = [0-9]*\|B_COMPLEXITY = [0-9]*" code_demo.ipynb | head -3
cat > .aii/manifest.yaml <<'EOF'
# No heavy paths: every file in this workspace is a small text/code/JSON file (all well under the 10 MB floor).
# The notebook's test venv lives outside the workspace (on local /tmp) and is removed by the pipeline.
entries: []
EOF
cat > README.md <<'EOF'
# T1 demo: peer agreement vs paid AI judges on held-out NL→FOL data

This is a runnable, Colab-ready demo of the artifact **"Peer agreement vs paid AI judges on held-out logic"** (T1). The
artifact asks whether a gold-free, peer-agreement metric can score NL→FOL candidates: `c_score_align` is z3 equivalence
with other systems' formalisations of the same sentence, after predicate alignment. The comparison is against paid LLM
judges on the held-out dataset E:
- gemini-2.5-flash-lite (rubric JSON);
- gpt-4.1-nano P(YES);
- the gemini-3.1-pro-preview frontier judge.

The demo also compares against round-trip NLI, SC-5 and a stacked 28-baseline model (S4).

## What the notebook does

The artifact's `method.py` is a stage dispatcher. Its API and GPU stages need OpenRouter keys, a GPU and about $2.40,
so they are not re-run. Their per-row outputs are the frozen `predict_*` columns in `mini_demo_data.json`. The
notebook re-runs the `t1_analysis` statistics with the original code (`src/api_bar.py`, `src/analyse_T1.py`):
- stratified and pooled AUROC with a sentence-cluster bootstrap (B = 2000);
- criterion (a), head-on paired deltas against the cheap judges;
- criterion (b), the nested S4 gain, computed from the frozen out-of-fold stacks;
- criterion (d), the frontier-frame ratio and nested frame model;
- complexity curves;
- label-permutation placebos;
- a final results table and a 4-panel figure.

It runs on 100 rows, so its CIs are wide. The full-population (n = 2,686) values are printed beside each subset number.
Full run: strat Δ(c_score_align − flash-lite disguised) = +0.099 [0.049, 0.146]; verdict **CONFIRMED**. At the original
bootstrap sizes the notebook runs in about 75 s.

## Layout

| path | what it is |
|---|---|
| `code_demo.ipynb` | the demo notebook, executed, with outputs |
| `mini_demo_data.json` | 100 rows of the R_AB / E_POOL / parseable population: 25 per source stratum (L25, L20, EXC, CTRL), ≤ 3 rows per sentence, 36 sentences. Each row has the sentence, the candidate FOL, the system, the label and every oriented metric score. The file also holds the full-run reference numbers and the frozen thresholds. |
| `scripts/make_mini_demo_data.py` | rebuilds `mini_demo_data.json` from the T1 artifact directory (`full_method_out.json`, `results/analysis_T1.json`, `results/verdict_T1.json`, `prereg_T1.json`) |
| `scripts/build_notebook.py` | regenerates `code_demo.ipynb` (config passed as JSON: `B`, `B_COMPLEXITY`, `N_PLACEBO`) |
| `.aii/manifest.yaml` | disposable-output manifest (no heavy paths) |

## How to run

- **Colab:** open `code_demo.ipynb` and run all cells. The data loads from the GitHub raw URL.
- **Locally:**

```bash
uv venv --seed --python 3.12 /tmp/t1demo && uv pip install --python /tmp/t1demo/bin/python jupyter ipykernel
/tmp/t1demo/bin/jupyter nbconvert --to notebook --execute code_demo.ipynb --output code_demo.ipynb
```

The install cell pins Colab's versions of numpy, scipy, scikit-learn and matplotlib, and installs them only outside
Colab. It also installs loguru. If the GitHub URL is unreachable, the notebook falls back to the local
`mini_demo_data.json`.

To rebuild the inputs:

```bash
python scripts/make_mini_demo_data.py <path-to-T1-artifact-dir>
python scripts/build_notebook.py '{"B": 2000, "B_COMPLEXITY": 1000, "N_PLACEBO": 200}'
```

## Restoring removed files

Nothing is marked `delete` in `.aii/manifest.yaml`: the workspace holds no caches, weights or large binaries, so
nothing needs restoring.
EOF
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
cat .terminal_claude_agent_struct_out.json; du -sh .
````

### [57] TOOL RESULT — Bash · 2026-09-25 12:53:33 UTC

```
{"stdout": "0\nB = 2000\nB = 1000\nB = 2000\n{\"out_expected_files\": {\"notebook\": \"code_demo.ipynb\", \"mini_data_file\": \"mini_demo_data.json\"}}\n3.1M\t.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [58] ASSISTANT · 2026-09-25 12:53:42 UTC

```
I've built the demo notebook and its 100-row data file. The notebook runs cleanly in the fresh test environment in about 74 s (budget 600 s), using the artifact's original settings of 2,000 bootstrap draws, 1,000 for the complexity bins and 200 placebo runs.

**What the notebook re-runs.** `method.py` only dispatches stages. Its judge, round-trip and self-consistency stages call paid APIs and a GPU, so the notebook doesn't re-run them. It uses their saved per-row scores and re-runs the analysis stage with the original code copied almost unchanged: stratified and pooled AUROC, the sentence-level bootstrap, criteria (a), (b) and (d), the complexity bins and the placebos. It ends with a comparison table and a 4-panel figure. The small edits were: bootstrap sizes moved into a config cell, a small shim so the copied code runs unchanged, and building the per-row table from the loaded data instead of the original files.

**Results on the subset.** They are noisy, and the notebook says so. Point estimates are close to the full run:

| | 100-row subset | full run (2,686 rows) |
|---|---|---|
| Stratified AUROC, peer agreement (`c_score_align`) | 0.766 | 0.741 |
| Stratified AUROC, flash-lite judge, disguised view | 0.674 | 0.642 |
| Δ, peer agreement minus that judge | +0.092 | +0.099 |

On 36 sentences the confidence intervals include 0, so criteria (a) and (b) don't hold on the subset; (d) does. The notebook prints the full-run value beside every subset number, and the headline verdict (CONFIRMED) comes from the full run. Criterion (b) uses the saved stacked-model predictions, not a refit, which wouldn't mean anything on 100 rows. Two parts of the original are left out because the data they need isn't in the subset: the contested-label cells and the probability-weighted frontier AUROC.

**The data file.** It holds 100 rows, 25 from each of the four sentence groups (L25, L20, EXC, CTRL), at most 3 rows per sentence, and 52 of the rows that the frontier judge scored. It also stores the full-run headline numbers and the frozen thresholds. The notebook loads it from the exact GitHub URL, falling back to the local file.

There was no todo-list tool in this session, so I followed the six TODOs in order without one. The manifest has no entries because nothing in the workspace is large (3.1 MB in total).

Files are in the workspace:
- `code_demo.ipynb`
- `mini_demo_data.json`
- `scripts/make_mini_demo_data.py`
- `scripts/build_notebook.py`
- `README.md`
- `.aii/manifest.yaml`
- `.terminal_claude_agent_struct_out.json`
```
