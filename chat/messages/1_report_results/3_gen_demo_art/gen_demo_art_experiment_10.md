# gen_demo_art_experiment_10 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `gen_paper_repo_a2e1d024cc16` — Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for Logic Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_10` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-25 16:42:52 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-25 16:42:58 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh/`:
GOOD: `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh/file.py`, `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh/results/out.json`
BAD: `/tmp/file.py`, `~/output.json`, `./file.py`, any path outside the workspace
</workspace>
<disposable_outputs>
A SHARED CACHE ALREADY EXISTS FOR THIS RUN: `/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/.shared_cache`
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
id: art_ngTPhaVyXxhh
type: experiment
title: Consensus vs LLM judges on fresh logic data
summary: >-
  E2-A (iter 5): the pre-registered confirmation of frozen cross-family consensus c_score_align (V0) on the untouched E2 NL->FOL
  set. STATUS PARTIAL / NOT_TESTABLE: the run-level OpenRouter 'Test idea' budget ($12, shared) ran out at ~11:40 UTC after
  this artifact spent $2.05; key polled to the pre-registered 15:30 cutoff, never recovered. Done: drift gate PASS (panel
  majority agreement 0.955 on 269 items, providers pinned, M2 e2/E2_DRIFT_DECISION.json); all 5,500 candidates (550 sentences
  x 10 slots) generated; solver labels for all; panel labels only for the first sha1-order prefix of 110 sentences (37 L25/37
  EXC/36 DT; random prefix); every label-free score sealed before labels (V0, PT, c_exact, V1-V5, L2, L3, user's pilot metrics,
  local Qwen3-8B judge both views); flash-lite judge on 707 rows only; nano/round trip not run. RESULTS on the prefix (R_AB,
  strat AUROC, sentence-cluster bootstrap B=2000): long pool 94 rows (76 ERR/18 COR) -> (a) NOT_TESTABLE, (b) not testable,
  (c) NOT_TESTABLE in R_COMP sibling. DT (179 rows, prover-built gold): V0 0.916 [0.858,0.970] vs local judge 0.913, delta
  +0.003 [-0.042,+0.052]; ALL (273): V0 0.890, S4 stack 0.931, [S4+V0]-S4 -0.009 [-0.034,+0.014] -> consensus ties a local
  8B judge and adds nothing over it. User's pilot metrics do NOT track correctness: joint-conflict 0.500, arity 0.507, shape
  0.510, dangling 0.413 (inverted); only 1-rerun-Jaccard 0.713 (a lexical cross-system agreement proxy). V0 is not rename-invariant:
  nonce-renamed correct formulas flagged 100% (n=145, base 0.26), synonym 94% (n=36). H-MECH: (i) 0.909 of peers disagreeing
  with CORRECT candidates are ERROR; (iv) ALIGN lowers false alarms 0.74->0.18 but endorses more rename-type errors; (ii)
  NOT_READ; (iii) CI includes 0. H-IMPROVE: V0 stands (freeze winner NONE); H-RENAME NOT CONFIRMED (GG failed dev gate). E2-B
  union adds no R_AB rows. Headline numbers independently re-derived (audit/rederive.py, sklearn from raw files, exact match;
  shuffled-label placebo 0.497). FILES: per_item_E2A.jsonl (scores+labels; M3 marker e2/E2A_FINAL_READY.json with sha256),
  scores_E2A.jsonl + score_seal.json, e2src/sealed/labels_E2.jsonl, results/*.json, tables.md, method_out.json (exp_gen_sol_out,
  predict_* higher=ERROR), lib/nl2fol_metrics.py (reusable (text,fol,peers) metrics with 'measures / does not measure' docstrings),
  deviations.json (17), README.md. Resume scripts finish the full test if the budget is raised.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11
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
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-5/experiment-11/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-5/experiment-11/demo/mini_demo_data.json"
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
To test-run the notebook in a clean environment (simulating Colab), use the disposable venv at `/tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-a1a05088362b`. It is on this machine's local disk, outside your workspace, which is on a slow network volume: never create a venv inside your workspace.
```bash
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-a1a05088362b
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-a1a05088362b/bin/python jupyter ipykernel
/tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-a1a05088362b/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
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
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-5/experiment-11/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] HUMAN-USER prompt · 2026-09-25 16:42:58 UTC

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

### [4] ASSISTANT · 2026-09-25 16:43:06 UTC

```
I'll start by loading the required skills and looking at the artifact.
```

### [5] TOOL CALL — Skill · 2026-09-25 16:43:06 UTC

```
aii-colab
```

### [6] TOOL RESULT — Skill · 2026-09-25 16:43:06 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [7] TOOL CALL — Skill · 2026-09-25 16:43:06 UTC

```
aii-long-running-tasks
```

### [8] TOOL RESULT — Skill · 2026-09-25 16:43:06 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [9] TOOL CALL — Bash · 2026-09-25 16:43:06 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11 && ls -la && wc -l method.py && ls -la /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh/ /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh/.aii
```

### [10] TOOL RESULT — Bash · 2026-09-25 16:43:06 UTC

```
{"stdout": "total 60956\ndrwxr-xr-x 14 root   root    2013491 Sep 24 15:38 .\ndrwxr-xr-x  7 root   root    2040112 Sep 24 11:06 ..\n-rw-r--r--  1 231072 231072       11 Sep 24 11:10 .T0\ndrwxr-xr-x  2 root   root      86700 Sep 24 15:38 .aii\n-rw-------  1 231072 231072       54 Sep 24 14:02 .aii_claude_session.json\n-rw-r--r--  1 231072 231072   795858 Sep 24 11:39 .aii_cost_ledger.jsonl\n-rw-------  1 231072 231072    19028 Sep 24 15:38 .aii_worker_result.json\n-rw-r--r--  1 231072 231072  3462258 Sep 24 15:38 .repl_agent.ptylog\n-rw-r--r--  1 231072 231072     3239 Sep 24 15:36 .terminal_claude_agent_struct_out.json\n-rw-r--r--  1 231072 231072      398 Sep 24 11:11 DPIN.diff\n-rw-r--r--  1 231072 231072    13297 Sep 24 15:37 README.md\ndrwxr-xr-x  3 231072 231072  1005088 Sep 24 15:34 analysis\ndrwxr-xr-x  2 231072 231072  1000650 Sep 24 15:36 audit\ndrwxr-xr-x  4 231072 231072  2002122 Sep 24 12:20 cache\n-rw-r--r--  1 231072 231072     4441 Sep 24 15:32 deviations.json\ndrwxr-xr-x  2 231072 231072  2000514 Sep 24 15:31 e2\ndrwxr-xr-x 18 231072 231072  2006487 Sep 24 16:51 e2src\nlrwxrwxrwx  1 231072 231072       13 Sep 24 11:30 env -> /root/e2a_env\n-rw-r--r--  1 231072 231072        0 Sep 24 11:16 env_install.log\ndrwxr-xr-x  2 231072 231072  1006418 Sep 24 15:34 freeze_copy\ndrwxr-xr-x  5 231072 231072  2000163 Sep 24 16:51 frozen\n-rw-r--r--  1 231072 231072 10943839 Sep 24 15:32 full_method_out.json\n-rw-r--r--  1 231072 231072    40710 Sep 24 11:52 inputs_manifest.json\ndrwxr-xr-x  3 231072 231072  1001196 Sep 24 15:34 lib\ndrwxr-xr-x  2 231072 231072  1056168 Sep 24 15:31 logs\n-rw-r--r--  1 231072 231072     2836 Sep 24 15:35 method.py\n-rw-r--r--  1 231072 231072  8754723 Sep 24 15:31 method_out.json\n-rw-r--r--  1 231072 231072    18220 Sep 24 15:32 mini_method_out.json\n-rw-r--r--  1 231072 231072     7047 Sep 24 11:11 or_client_before_DPIN.py\n-rw-r--r--  1 231072 231072 10253576 Sep 24 15:30 per_item_E2A.jsonl\n-rw-r--r--  1 231072 231072     2519 Sep 24 11:52 prereg_addendum_budgetstop.json\n-rw-r--r--  1 231072 231072       98 Sep 24 11:52 prereg_addendum_budgetstop.sha256\n-rw-r--r--  1 231072 231072     5621 Sep 24 11:12 prereg_iter5_E2A.json\n-rw-r--r--  1 231072 231072       88 Sep 24 11:12 prereg_iter5_E2A.sha256\n-rw-r--r--  1 231072 231072    17376 Sep 24 15:32 preview_method_out.json\n-rw-r--r--  1 231072 231072     4073 Sep 24 15:35 pyproject.toml\n-rw-r--r--  1 231072 231072       39 Sep 24 11:32 pytest.ini\n-rw-r--r--  1 231072 231072     6855 Sep 24 15:36 reproducibility.md\ndrwxr-xr-x  2 231072 231072  1015213 Sep 24 15:31 results\n-rw-r--r--  1 231072 231072    17782 Sep 24 13:01 score_seal.json\n-rw-r--r--  1 231072 231072  8751701 Sep 24 13:01 scores_E2A.jsonl\ndrwxr-xr-x  3 231072 231072  1004496 Sep 24 15:34 scoring\n-rw-r--r--  1 231072 231072    43598 Sep 24 15:31 tables.md\n55 method.py\n/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh/:\ntotal 1988\ndrwxr-xr-x 3 root root 1002774 Sep 25 16:42 .\ndrwxr-xr-x 3 root root 1002774 Sep 25 16:42 ..\ndrwxr-xr-x 2 root root       1 Sep 25 16:42 .aii\n-rw------- 1 root root      54 Sep 25 16:42 .aii_claude_session.json\n-rw-r--r-- 1 root root   31937 Sep 25 16:43 .repl_agent.ptylog\n\n/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh/.aii:\ntotal 980\ndrwxr-xr-x 2 root root       1 Sep 25 16:42 .\ndrwxr-xr-x 3 root root 1002774 Sep 25 16:42 ..", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [11] TOOL CALL — Bash · 2026-09-25 16:43:08 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11 && cat method.py && echo ---- && head -c 4000 preview_method_out.json && echo && python3 -c "
import json;d=json.load(open('preview_method_out.json'));print(type(d), list(d.keys()) if isinstance(d,dict) else len(d))
" && ls lib lib/* scoring scoring/* results audit analysis e2 | head -100
```

### [12] TOOL RESULT — Bash · 2026-09-25 16:43:10 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"E2-A entry point: runs the label-free scoring, the seals/join and the analyses in the order actually executed.\nPaid API stages (drift gate, generation, panel, API judges) are in e2src/src_e2a/*.sh and scoring/api_judges.py; they\nare cached and never re-billed. Usage: python method.py [--from STAGE] [--prefix 110]\nStages: l3, consensus, pairwise, exact, prep, judges, local_judge, pilot, assemble, labels, join, analyse, rename, union, outputs\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport os\nimport subprocess\nimport sys\nfrom pathlib import Path\n\nWS = Path(__file__).resolve().parent\nPY = str(WS / \"env\" / \".venv\" / \"bin\" / \"python\")\nGPU = \"/root/e2a_gpu/.venv/bin/python\"\nE2PY = str(WS / \"e2src\" / \".venv\" / \"bin\" / \"python\")\n\n\ndef stages(prefix: int) -> list[tuple[str, list[str], Path]]:\n    s = [(\"l3\", [PY, \"scoring/score_consensus.py\", \"--stage\", \"l3\"], WS),\n         (\"consensus\", [PY, \"scoring/score_consensus.py\", \"--stage\", \"score\", \"--workers\", \"30\"], WS),\n         (\"pairwise\", [PY, \"scoring/score_consensus.py\", \"--stage\", \"pairwise\", \"--workers\", \"36\"], WS),\n         (\"exact\", [PY, \"scoring/score_consensus.py\", \"--stage\", \"exact\", \"--workers\", \"36\"], WS),\n         (\"prep\", [PY, \"scoring/api_judges.py\", \"--stage\", \"prep\", \"--workers\", \"10\"], WS),\n         (\"judges\", [PY, \"scoring/api_judges.py\", \"--stage\", \"judges\", \"--concurrency\", \"32\"], WS),\n         (\"local_judge\", [GPU, \"scoring/local_judge.py\", \"--which\", \"qwen8b_disg,qwen8b_orig\", \"--bs\", \"64\"], WS),\n         (\"pilot\", [PY, \"scoring/pilot_metrics_E2.py\"], WS),\n         (\"assemble\", [PY, \"scoring/assemble_scores.py\"], WS)]\n    s += [(f\"labels:{x}\", [E2PY, f\"src_e2/{x}.py\"], WS / \"e2src\")\n          for x in (\"assemble_e2\", \"controls_e2\", \"testability_e2\", \"seal_e2\", \"verify_seal\")]\n    s += [(\"join\", [PY, \"analysis/analyse_E2A.py\", \"--stage\", \"join\"], WS),\n          (\"analyse\", [PY, \"analysis/analyse_E2A.py\", \"--stage\", \"analyse\"] + ([\"--prefix\", str(prefix)] if prefix else []), WS),\n          (\"rename\", [PY, \"analysis/rename_V0.py\"], WS),\n          (\"union\", [PY, \"analysis/union_E2B.py\", \"--deadline-utc\", \"2026-09-24T15:40:00Z\", \"--once\"], WS),\n          (\"outputs\", [PY, \"analysis/make_outputs.py\"], WS)]\n    return s\n\n\ndef main() -> None:\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--from\", dest=\"start\", default=\"l3\")\n    ap.add_argument(\"--prefix\", type=int, default=110)\n    a = ap.parse_args()\n    env = dict(os.environ, PYTHONHASHSEED=\"0\", OPENBLAS_NUM_THREADS=\"1\", OMP_NUM_THREADS=\"1\")\n    run = False\n    for name, cmd, cwd in stages(a.prefix):\n        run = run or name.startswith(a.start)\n        if run:\n            print(f\"== {name}: {' '.join(cmd)}\", flush=True)\n            subprocess.run(cmd, cwd=cwd, env=env, check=True)\n\n\nif __name__ == \"__main__\":\n    sys.exit(main())\n----\n{\n  \"metadata\": {\n    \"method_name\": \"frozen cross-family solver consensus c_score_align (V0) and comparators on untouched E2\",\n    \"orientation\": \"every predict_* is higher = more likely ERROR; output = E2 final label (E's frozen protocol)\",\n    \"verdict\": \"NOT_TESTABLE ((a): too few rows with the pre-registered flash-lite disguised bar; see fallback_substitute_bar)\"\n  },\n  \"datasets\": [\n    {\n      \"dataset\": \"E2_DT\",\n      \"examples\": [\n        {\n          \"input\": \"{\\\"text\\\": \\\"If Xiomara either wakes up at dawn or has light slumber (but not both), then she sleeps very lightly.\\\", \\\"candidate_fol\\\": \\\"(WakesAtDawn(xiomara) ∨ LightSlumber(xiomara) ∧ ¬(WakesAtDawn(xiomar...\",\n          \"output\": \"CONTESTED\",\n          \"metadata_row_key\": \"a6914eef11622a25|fewshot_v1\",\n          \"metadata_sentence_id\": \"b91115ec794d\",\n          \"metadata_stratum\": \"DT\",\n          \"metadata_slot\": \"G1\",\n          \"metadata_system\": \"G1:meta-llama/llama-3.1-8b-instruct\",\n          \"metadata_family\": \"meta\",\n          \"metadata_label_tier\": \"A_unaudited_ref\",\n          \"metadata_reading_choice\": false,\n          \"metadata_vex\": false,\n          \"metadata_pilot\": true,\n          \"metadata_words\": 19,\n          \"metadata_n_conditions\": 2,\n          \"metadata_parse_ok\": true,\n          \"metadata_fold_E2\": 1,\n          \"predict_c_score_align\": \"1.000000\",\n          \"predict_p_peer_text\": \"0.957770\",\n          \"predict_c_exact\": \"1.000000\",\n          \"predict_g_align\": \"1.000000\",\n          \"predict_c_pn\": \"1.000000\",\n          \"predict_c_rw\": \"1.000000\",\n          \"predict_c_pn_rw\": \"1.000000\",\n          \"predict_c_two\": \"0.838446\",\n          \"predict_c_v5\": \"1.000000\",\n          \"predict_judge_cheap_disg\": \"null\",\n          \"predict_judge_cheap_orig\": \"null\",\n          \"predict_judge_cheap2_disg\": \"null\",\n          \"predict_judge_cheap2_orig\": \"null\",\n          \"predict_judge_local_qwen8b_disg\": \"0.150000\",\n          \"predict_judge_local_qwen8b_orig\": \"0.200000\",\n          \"predict_l2_bow\": \"0.125000\",\n          \"predict_l3_z3\": \"0.916667\",\n          \"predict_pilot_joint_conflict\": \"0.000000\",\n          \"predict_pilot_arity_incons\": \"0.000000\",\n          \"predict_pilot_shape_incons\": \"0.000000\",\n          \"predict_pilot_dangling\": \"1.000000\",\n          \"predict_pilot_rerun_jacc\": \"0.386532\"\n        },\n        {\n          \"input\": \"{\\\"text\\\": \\\"If Xiomara either wakes up at dawn or has light slumber (but not both), then she sleeps very lightly.\\\", \\\"candidate_fol\\\": \\\"(WakesUpAt(xiomara, dawn) ⊕ Has(xiomara, lightSlumber)) → SleepsVery...\",\n          \"output\": \"CORRECT\",\n          \"metadata_row_key\": \"62b8d8e91effd650|fewshot_v1\",\n          \"metadata_sentence_id\": \"b91115ec794d\",\n          \"metadata_stratum\": \"DT\",\n          \"metadata_slot\": \"G1b\",\n          \"metadata_system\": \"G1b:meta-llama/llama-3.3-70b-instruct\",\n          \"metadata_family\": \"meta\",\n          \"metadata_label_tier\": \"B\",\n          \"metadata_reading_choice\": false,\n          \"metadata_vex\": false,\n          \"metadata_pilot\": true,\n          \"metadata_words\": 19,\n          \"metadata_n_conditions\": 2,\n          \"metadata_parse_ok\": true,\n          \"metadata_fold_E2\": 1,\n          \"predict_c_score_align\": \"0.375000\",\n          \"predict_p_peer_text\": \"0.354247\",\n          \"predict_c_exact\": \"0.750000\",\n          \"predict_g_align\": \"0.454545\",\n          \"predict_c_pn\": \"0.000000\",\n          \"predict_c_rw\": \"0.308866\",\n          \"predict_c_pn_rw\": \"0.000000\",\n          \"predict_c_two\": \"0.444249\",\n          \"predict_c_v5\": \"0.000000\",\n          \"predict_judge_cheap_disg\": \"0.000000\",\n          \"predict_judge_cheap_orig\": \"null\",\n          \"predict_judge_cheap2_disg\": \"null\",\n          \"predict_judge_cheap2_orig\": \"null\",\n          \"predict_judge_local_qwen8b_disg\": \"0.050000\",\n          \"predict_judge_local_qwen8b_orig\": \"0.050000\",\n          \"predict_l2_bow\": \"0.000000\",\n          \"predict_l3_z3\": \"0.750000\",\n          \"predict_pilot_joint_conflict\": \"0.000000\",\n          \"pre\n<class 'dict'> ['metadata', 'datasets']\nlib/nl2fol_metrics.py\nscoring/api_judges.py\nscoring/assemble_scores.py\nscoring/common.py\nscoring/guard.py\nscoring/local_judge.py\nscoring/pilot_metrics_E2.py\nscoring/run_scoring.sh\nscoring/score_consensus.py\n\nanalysis:\nanalyse_E2A.py\nmake_outputs.py\nrename_V0.py\ntests\nunion_E2B.py\n\naudit:\nrederive.py\nrederive_out.json\n\ne2:\nE2A_FINAL_READY.json\nE2_DRIFT_DECISION.json\ncandidates_E2_nolabels.jsonl\n\nlib:\nnl2fol_metrics.py\ntests\n\nlib/tests:\ntest_lib.py\n\nresults:\nauroc_cells.json\ncomplexity_E2.json\nconfirm_verdict_E2A.json\ncost_E2A.json\ncoverage_E2.json\nhmech_E2.json\nimprove_E2.json\njoin_record.json\nplacebo_E2.json\nprefix_used.json\nrename_E2.json\nrename_V0.json\nrename_V0_rows.jsonl\ns4_E2.json\nsystem_level_E2.json\nunion_longpool.json\n\nscoring:\napi_judges.py\nassemble_scores.py\ncommon.py\nguard.py\nlocal_judge.py\npilot_metrics_E2.py\nrun_scoring.sh\nscore_consensus.py\ntests\n\nscoring/tests:\ntest_guard.py\ntest_v0_repro.py\ntest_variants.py", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [13] ASSISTANT · 2026-09-25 16:43:14 UTC

```
`method.py` is only a stage orchestrator that calls subprocesses. I'll look at the scripts it calls to find code that can run inside the notebook.
```

### [14] TOOL CALL — Bash · 2026-09-25 16:43:14 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11 && wc -l scoring/*.py analysis/*.py audit/rederive.py lib/nl2fol_metrics.py && cat audit/rederive.py && head -c 3000 audit/rederive_out.json
```

### [15] TOOL RESULT — Bash · 2026-09-25 16:43:14 UTC

```
{"stdout": "   166 scoring/api_judges.py\n   154 scoring/assemble_scores.py\n    45 scoring/common.py\n    85 scoring/guard.py\n   102 scoring/local_judge.py\n    74 scoring/pilot_metrics_E2.py\n   266 scoring/score_consensus.py\n   549 analysis/analyse_E2A.py\n   173 analysis/make_outputs.py\n    57 analysis/rename_V0.py\n   119 analysis/union_E2B.py\n    87 audit/rederive.py\n   186 lib/nl2fol_metrics.py\n  2063 total\n\"\"\"Independent re-derivation of the headline numbers from RAW files through a different code path\n(sklearn roc_auc_score per stratum, raw sealed labels, raw consensus/judge caches; no analysis/ code imported).\"\"\"\nimport json, random, collections\nimport numpy as np\nfrom sklearn.metrics import roc_auc_score\nW = __import__(\"pathlib\").Path(__file__).resolve().parents[1]\njl = lambda p: [json.loads(l) for l in open(p) if l.strip()]\nlab = {r[\"row_key\"]: r for r in jl(W / \"e2src/sealed/labels_E2.jsonl\") if r[\"system_class\"] == \"llm\"}\ncand = {r[\"row_key\"]: r for r in jl(W / \"e2/candidates_E2_nolabels.jsonl\")}\norder = json.load(open(W / \"e2src/work/e2a_order.json\"))[:110]\nkeep = set(order)\nv0 = {}\nfor s in jl(W / \"cache/consensus_sentences.jsonl\"):\n    for r in s[\"rows\"]:\n        v0[r[\"key\"]] = r.get(\"c_score_align\")\nunits = {u[\"key\"]: u for u in jl(W / \"cache/units_E2.jsonl\")}\nloc = {}\nfor r in jl(W / \"cache/judge_local_qwen8b.jsonl\"):\n    if r.get(\"p\") is not None:\n        loc[r[\"key\"]] = 1 - r[\"p\"]\npil = {r[\"key\"]: r for r in jl(W / \"cache/pilot_E2.jsonl\")}\nrows = []\nfor k, l in lab.items():\n    c = cand[k]\n    if c[\"sentence_id\"] not in keep or l[\"label\"] not in (\"CORRECT\", \"ERROR\") or l[\"reading_choice\"] or l[\"label_tier\"] not in (\"A\", \"B\"):\n        continue\n    rows.append(dict(k=k, sid=c[\"sentence_id\"], st=c[\"stratum\"], y=int(l[\"label\"] == \"ERROR\"), v0=v0.get(k),\n                     loc=loc.get(k + \"|disg\"), **{m: pil[k].get(m) for m in (\"pilot_joint_conflict\", \"pilot_arity_incons\", \"pilot_shape_incons\", \"pilot_dangling\", \"pilot_rerun_jacc\")}))\n\n\ndef sauc(rs, col, ycol=\"y\"):\n    num = den = 0\n    for st in set(r[\"st\"] for r in rs):\n        g = [r for r in rs if r[\"st\"] == st and r[col] is not None]\n        y = [r[ycol] for r in g]\n        if 0 < sum(y) < len(y):\n            w = sum(y) * (len(y) - sum(y))\n            num += roc_auc_score(y, [r[col] for r in g]) * w\n            den += w\n    return num / den if den else None\n\n\nout = {}\nfor cell, sts in ((\"ALL\", (\"L25\", \"EXC\", \"DT\")), (\"DT\", (\"DT\",)), (\"LONG\", (\"L25\", \"EXC\"))):\n    rs = [r for r in rows if r[\"st\"] in sts]\n    out[cell] = {\"n\": len(rs), \"n_err\": sum(r[\"y\"] for r in rs), \"n_cor\": sum(1 - r[\"y\"] for r in rs),\n                 \"V0\": sauc(rs, \"v0\"), \"local_disg\": sauc(rs, \"loc\")}\n    out[cell][\"delta_V0_minus_local\"] = out[cell][\"V0\"] - out[cell][\"local_disg\"]\n    for m in (\"pilot_joint_conflict\", \"pilot_arity_incons\", \"pilot_shape_incons\", \"pilot_dangling\", \"pilot_rerun_jacc\"):\n        out[cell][m] = sauc(rs, m)\n# placebo: shuffled labels within stratum -> AUROC ~0.5 and the V0-local delta ~0\nrng = random.Random(0)\npl = []\nfor b in range(200):\n    rs = [dict(r) for r in rows]\n    for st in set(r[\"st\"] for r in rs):\n        idx = [i for i, r in enumerate(rs) if r[\"st\"] == st]\n        ys = [rs[i][\"y\"] for i in idx]\n        rng.shuffle(ys)\n        for i, y in zip(idx, ys):\n            rs[i][\"y\"] = y\n    pl.append((sauc(rs, \"v0\"), sauc(rs, \"v0\") - sauc(rs, \"loc\")))\npa = np.array(pl)\nout[\"placebo_shuffled\"] = {\"V0_mean\": float(pa[:, 0].mean()), \"V0_p2.5_97.5\": np.percentile(pa[:, 0], [2.5, 97.5]).tolist(),\n                           \"delta_mean\": float(pa[:, 1].mean()), \"delta_p2.5_97.5\": np.percentile(pa[:, 1], [2.5, 97.5]).tolist(),\n                           \"real_V0_ALL_above_placebo_p97.5\": bool(out[\"ALL\"][\"V0\"] > np.percentile(pa[:, 0], 97.5))}\n# rename controls from their raw rows\nrr = jl(W / \"results/rename_V0_rows.jsonl\")\nfor t in (\"RENAME_SYN\", \"RENAME_NONCE\"):\n    g = [r for r in rr if r[\"type\"] == t and r[\"v0_control\"] is not None and r[\"v0_parent\"] is not None]\n    out[t] = {\"n\": len(g), \"FA\": sum(r[\"v0_control\"] > 0.5 for r in g) / len(g), \"base\": sum(r[\"v0_parent\"] > 0.5 for r in g) / len(g)}\n# drift + spend from raw logs\nd = json.load(open(W / \"e2src/panel_drift_E2.json\"))\nout[\"drift_majority_agreement\"] = d[\"combined\"][\"majority_agreement\"]\nspend = sum(r[\"cost_usd\"] for r in jl(W / \"e2src/cost_ledger.jsonl\")) + sum(r[\"cost_usd\"] for r in jl(W / \"cache/l3_cost_ledger.jsonl\")) \\\n    + sum((r.get(\"cost\") or 0) for r in jl(W / \"cache/t1_results/costs.jsonl\"))\nout[\"spend_usd\"] = spend\n# compare with the pipeline's aggregated numbers\nA = json.load(open(W / \"results/auroc_cells.json\"))[\"R_AB\"]\ncmp = {}\nfor cell, key in ((\"ALL\", \"ALL\"), (\"DT\", \"DT\"), (\"LONG\", \"LONG (L25+EXC)\")):\n    m = A[key][\"metrics\"]\n    cmp[cell] = {\"n_match\": A[key][\"n_rows\"] == out[cell][\"n\"], \"V0_absdiff\": abs(m[\"c_score_align\"][\"strat\"] - out[cell][\"V0\"]),\n                 \"local_absdiff\": abs(m[\"judge_local_qwen8b_disg\"][\"strat\"] - out[cell][\"local_disg\"])}\nout[\"comparison_with_pipeline\"] = cmp\njson.dump(out, open(W / \"audit/rederive_out.json\", \"w\"), indent=1)\nprint(json.dumps(out, indent=1))\n{\n \"ALL\": {\n  \"n\": 273,\n  \"n_err\": 150,\n  \"n_cor\": 123,\n  \"V0\": 0.8904441294590124,\n  \"local_disg\": 0.894991731632412,\n  \"delta_V0_minus_local\": -0.004547602173399556,\n  \"pilot_joint_conflict\": 0.5,\n  \"pilot_arity_incons\": 0.5066146940703993,\n  \"pilot_shape_incons\": 0.5099811008740845,\n  \"pilot_dangling\": 0.4131230805575242,\n  \"pilot_rerun_jacc\": 0.7126151665485473\n },\n \"DT\": {\n  \"n\": 179,\n  \"n_err\": 74,\n  \"n_cor\": 105,\n  \"V0\": 0.9161518661518661,\n  \"local_disg\": 0.9129343629343629,\n  \"delta_V0_minus_local\": 0.003217503217503137,\n  \"pilot_joint_conflict\": 0.5,\n  \"pilot_arity_incons\": 0.5067567567567568,\n  \"pilot_shape_incons\": 0.5099742599742599,\n  \"pilot_dangling\": 0.3996138996138996,\n  \"pilot_rerun_jacc\": 0.7287001287001288\n },\n \"LONG\": {\n  \"n\": 94,\n  \"n_err\": 76,\n  \"n_cor\": 18,\n  \"V0\": 0.603448275862069,\n  \"local_disg\": 0.694683908045977,\n  \"delta_V0_minus_local\": -0.09123563218390807,\n  \"pilot_joint_conflict\": 0.5,\n  \"pilot_arity_incons\": 0.5050287356321839,\n  \"pilot_shape_incons\": 0.5100574712643678,\n  \"pilot_dangling\": 0.5639367816091954,\n  \"pilot_rerun_jacc\": 0.5330459770114944\n },\n \"placebo_shuffled\": {\n  \"V0_mean\": 0.49687632884479094,\n  \"V0_p2.5_97.5\": [\n   0.43272354122371837,\n   0.5784874793290811\n  ],\n  \"delta_mean\": -0.0016802504134183877,\n  \"delta_p2.5_97.5\": [\n   -0.06008002598629819,\n   0.06907335223245929\n  ],\n  \"real_V0_ALL_above_placebo_p97.5\": true\n },\n \"RENAME_SYN\": {\n  \"n\": 36,\n  \"FA\": 0.9444444444444444,\n  \"base\": 0.3611111111111111\n },\n \"RENAME_NONCE\": {\n  \"n\": 145,\n  \"FA\": 1.0,\n  \"base\": 0.2620689655172414\n },\n \"drift_majority_agreement\": 0.9554,\n \"spend_usd\": 2.04500803205,\n \"comparison_with_pipeline\": {\n  \"ALL\": {\n   \"n_match\": true,\n   \"V0_absdiff\": 0.0,\n   \"local_absdiff\": 1.1102230246251565e-16\n  },\n  \"DT\": {\n   \"n_match\": true,\n   \"V0_absdiff\": 0.0,\n   \"local_absdiff\": 1.1102230246251565e-16\n  },\n  \"LONG\": {\n   \"n_match\": true,\n   \"V0_absdiff\": 0.0,\n   \"local_absdiff\": 0.0\n  }\n }\n}", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [16] TOOL CALL — Bash · 2026-09-25 16:43:18 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11 && cat scoring/score_consensus.py scoring/common.py
```

### [17] TOOL RESULT — Bash · 2026-09-25 16:43:18 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"E2-A label-free consensus scoring with the FROZEN iteration-2 exp-5 code (frozen/exp5/src, byte-identical copies).\n\n  l3        L3 role questionnaire (exp-A role_questionnaire, flash-lite, TEXT ONLY) for every E2 sentence -> cache/E2_l3_q.jsonl\n  score     exp-5 pool_scoring.score_sentence per sentence (peers = the other LLM slots of the same sentence, leave-own-\n            vendor-family-out, frozen family_map_vendor) -> cache/consensus_sentences.jsonl\n              c_score_align = 1 - share of family-disjoint parseable peers eqmv-equivalent to the candidate (V0, PRIMARY)\n              ALIGN:g_score (graded consensus), l2_bow, l3_z3 (TEXT side) -> p_peer_text (frozen fusion), n_peers_used\n  pairwise  eval-2 pairwise_matrix per sentence (all eqmv pairs among parseable outputs; H-MECH and variants V1-V5)\n            -> cache/pairwise_E2.jsonl\n  exact     c_exact: the same consensus with z3 equivalence on IDENTICAL symbol names (no aligner) -> cache/exact_E2.jsonl\n\nParameters: exp-5 prereg scoring_params, except variants = ['ALIGN'] (NF-anchored is a closed strand), k6_seeds = 0,\nfamfield = False, medoid_budget_s = 0. These switch off auxiliary readouts only; c_score_align, ALIGN:g_score, l2_bow and\nl3_z3 are computed by the unchanged code path (checked by scoring/tests: reproduction of E rows).\nUsage: env/.venv/bin/python scoring/score_consensus.py --stage l3|score|pairwise|exact [--workers 44]\n\"\"\"\nfrom __future__ import annotations\n\nimport sys\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).resolve().parents[1]))\nimport scoring.guard  # noqa: E402,F401\nfrom scoring.common import CACHE, FROZEN, append_jsonl, by_sentence, candidates, jl, setup_log  # noqa: E402\n\nimport argparse  # noqa: E402\nimport asyncio  # noqa: E402\nimport hashlib  # noqa: E402\nimport json  # noqa: E402\nimport multiprocessing as mp  # noqa: E402\nimport os  # noqa: E402\nimport time  # noqa: E402\nfrom concurrent.futures import ProcessPoolExecutor, as_completed  # noqa: E402\n\nfrom loguru import logger  # noqa: E402\n\nEXP5 = FROZEN / \"exp5\" / \"src\"\nos.environ.setdefault(\"NLTK_DATA\", str(FROZEN / \"nltk_data\"))\nPRE5 = json.loads((FROZEN / \"exp5\" / \"results\" / \"prereg.json\").read_text())\nFAM = PRE5[\"family_map_vendor\"]\nL3P = CACHE / \"E2_l3_q.jsonl\"\nJUDGE_MODEL = \"google/gemini-2.5-flash-lite\"\n\n\ndef params() -> dict:\n    P = dict(PRE5[\"scoring_params\"])\n    P.update(variants=[\"ALIGN\"], k6_seeds=0, famfield=False, medoid_budget_s=0)\n    return P\n\n\ndef sentence_tasks() -> list[dict]:\n    q = {r[\"text\"]: r[\"q\"] for r in jl(L3P) if r.get(\"coverage_status\") == \"OK\"}\n    out = []\n    for sid, rs in by_sentence(candidates()).items():\n        text = rs[0][\"text\"]\n        out.append({\"sentence_id\": sid, \"text\": text, \"q\": q.get(text), \"stratum\": rs[0][\"stratum\"],\n                    \"rows\": [{\"key\": r[\"row_key\"], \"fol\": r[\"candidate_fol\"], \"family\": FAM[r[\"slot\"]],\n                              \"family_field\": r.get(\"family_field\") or FAM[r[\"slot\"]], \"system\": r[\"system\"], \"is_peer\": True}\n                             for r in rs]})\n    out.sort(key=lambda t: hashlib.sha1((\"E2_v1|\" + t[\"sentence_id\"]).encode()).hexdigest())\n    return out\n\n\n# ------------------------------------------------------------------------------------------------------------ L3\nasync def _l3(texts: list[str]) -> None:\n    sys.path.insert(0, str(EXP5))\n    sys.path.insert(0, str(EXP5 / \"vendor_a\"))\n    import peer_text  # noqa: F401  (binds the dataset-E parser as `fol` for the vendored modules)\n    import llm as LA\n    import fol_triage as FT\n    LA.URL = os.environ[\"OPENROUTER_BASE_URL\"].rstrip(\"/\") + \"/chat/completions\"  # transport-only (as dataset-4 D0)\n    LA.CACHE_P = CACHE / \"l3_llm_cache.jsonl\"\n    LA.LEDGER_P = CACHE / \"l3_cost_ledger.jsonl\"\n    LA.HARD_STOP_USD = 0.5\n    have = {r[\"text\"] for r in jl(L3P) if r.get(\"coverage_status\") == \"OK\"}\n    todo = [t for t in dict.fromkeys(texts) if t not in have]\n    logger.info(f\"L3: {len(todo)} texts to answer\")\n    async with LA.LLM(concurrency=24) as llm:\n        async def one(t):\n            try:\n                r = await FT.role_questionnaire(t, llm, JUDGE_MODEL, tag=\"L3\")\n            except LA.StopBudget as ex:\n                r = {\"q\": None, \"coverage_status\": \"BUDGET_STOP\", \"cost_usd\": 0.0, \"secs\": 0.0, \"err\": str(ex)}\n            except RuntimeError as ex:\n                r = {\"q\": None, \"coverage_status\": \"L3_FAIL\", \"cost_usd\": 0.0, \"secs\": 0.0, \"err\": str(ex)[:200]}\n            return {\"text\": t, \"cond\": \"orig\", **r}\n        res = await asyncio.gather(*[one(t) for t in todo])\n    append_jsonl(L3P, res)\n    logger.info(f\"L3: ok {sum(r['coverage_status'] == 'OK' for r in res)}/{len(res)}; spent ${llm.spent:.4f}\")\n\n\n# --------------------------------------------------------------------------------------------------------- score\ndef _init(mem_gb: float = 4.0):\n    sys.path.insert(0, str(EXP5))\n    import scoring.guard  # noqa: F401\n    import pool_scoring as PS\n    PS.init_worker(mem_gb)\n\n\ndef _score_one(t: dict, P: dict) -> dict:\n    import pool_scoring as PS\n    return PS.score_sentence(t, P)\n\n\ndef stage_score(workers: int) -> None:\n    outp = CACHE / \"consensus_sentences.jsonl\"\n    done = {r[\"sentence_id\"] for r in jl(outp)}\n    T = [t for t in sentence_tasks() if t[\"sentence_id\"] not in done]\n    P = params()\n    logger.info(f\"score: {len(T)} sentences; params {P}; q present {sum(t['q'] is not None for t in T)}\")\n    t0 = time.time()\n    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context(\"spawn\"), initializer=_init) as ex, \\\n            outp.open(\"a\") as fh:\n        futs = {ex.submit(_score_one, t, P): t for t in T}\n        for i, fu in enumerate(as_completed(futs)):\n            t = futs[fu]\n            try:\n                res = fu.result()\n            except Exception as e:  # noqa: BLE001 - counted as coverage failure of every row of the sentence\n                logger.error(f\"sentence {t['sentence_id']} failed: {e}\")\n                res = {\"sentence_id\": t[\"sentence_id\"], \"rows\": [{\"key\": r[\"key\"], \"coverage_status\": \"WORKER_FAIL\"} for r in t[\"rows\"]],\n                       \"stats\": {\"error\": str(e)[:300]}}\n            res[\"stratum\"] = t[\"stratum\"]\n            fh.write(json.dumps(res, ensure_ascii=False) + \"\\n\")\n            fh.flush()\n            if (i + 1) % 25 == 0:\n                logger.info(f\"score {i + 1}/{len(T)} {time.time() - t0:.0f}s\")\n    logger.info(f\"score done in {time.time() - t0:.0f}s\")\n\n\n# ------------------------------------------------------------------------------------------------------ pairwise\ndef _init_pw():\n    sys.path.insert(0, str(FROZEN / \"eval2\" / \"src\"))\n    import scoring.guard  # noqa: F401\n    import pairwise\n    pairwise.init_worker(4.0)\n\n\ndef _pw_one(t: dict) -> dict:\n    import pairwise\n    t0 = time.time()\n    rows = [{\"row_key\": r[\"key\"], \"fol\": r[\"fol\"], \"slot\": r[\"slot\"], \"family\": r[\"family\"], \"family_field\": r[\"family_field\"],\n             \"system_class\": \"llm\"} for r in t[\"rows\"]]\n    m = pairwise.pairwise_matrix(rows)\n    m[\"sentence_id\"] = t[\"sentence_id\"]\n    m[\"secs\"] = round(time.time() - t0, 2)\n    return m\n\n\ndef stage_pairwise(workers: int) -> None:\n    outp = CACHE / \"pairwise_E2.jsonl\"\n    done = {r[\"sentence_id\"] for r in jl(outp)}\n    cand = by_sentence(candidates())\n    T = []\n    for t in sentence_tasks():\n        if t[\"sentence_id\"] in done:\n            continue\n        slot_of = {r[\"row_key\"]: r[\"slot\"] for r in cand[t[\"sentence_id\"]]}\n        for r in t[\"rows\"]:\n            r[\"slot\"] = slot_of[r[\"key\"]]\n        T.append(t)\n    logger.info(f\"pairwise: {len(T)} sentences\")\n    t0 = time.time()\n    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context(\"spawn\"), initializer=_init_pw) as ex, \\\n            outp.open(\"a\") as fh:\n        futs = {ex.submit(_pw_one, t): t for t in T}\n        for i, fu in enumerate(as_completed(futs)):\n            try:\n                res = fu.result()\n            except Exception as e:  # noqa: BLE001\n                res = {\"sentence_id\": futs[fu][\"sentence_id\"], \"error\": str(e)[:300]}\n            fh.write(json.dumps(res, ensure_ascii=False) + \"\\n\")\n            fh.flush()\n            if (i + 1) % 50 == 0:\n                logger.info(f\"pairwise {i + 1}/{len(T)} {time.time() - t0:.0f}s\")\n\n\n# --------------------------------------------------------------------------------------------------------- exact\ndef _init_ex():\n    sys.path.insert(0, str(EXP5))\n    import scoring.guard  # noqa: F401\n    import pool_scoring as PS\n    PS.init_worker(4.0)\n\n\ndef _exact_one(t: dict) -> dict:\n    \"\"\"c_exact: z3 equivalence (both entailment directions, 2 s each, frozen PT.z3_entails) with symbols identified by\n    their exact name; UNKNOWN = not equivalent (counted).\"\"\"\n    import peer_text as PT\n    import pool_scoring as PS\n    parsed = {}\n    for r in t[\"rows\"]:\n        e = PT.parse_fol(r[\"fol\"])\n        parsed[r[\"key\"]] = (PT.canon(e), e) if e is not None else (None, None)\n    cache: dict = {}\n    n_unknown = 0\n\n    def eq(a: str, b: str):\n        nonlocal n_unknown\n        if a == b:\n            return True\n        k = (a, b) if a < b else (b, a)\n        if k not in cache:\n            ea, eb = PT.parse_fol(k[0]), PT.parse_fol(k[1])\n            r1, to1 = PS._with_alarm(10, PT.z3_entails, ea, eb, 2000)\n            r2, to2 = (None, True) if (to1 or r1 is not True) else PS._with_alarm(10, PT.z3_entails, eb, ea, 2000)\n            if r1 is False or r2 is False:\n                cache[k] = False\n            elif r1 is True and r2 is True:\n                cache[k] = True\n            else:\n                cache[k] = None\n                n_unknown += 1\n        return cache[k]\n    out = []\n    for r in t[\"rows\"]:\n        cs = parsed[r[\"key\"]][0]\n        if cs is None:\n            out.append({\"key\": r[\"key\"], \"c_exact\": None, \"n_peers_exact\": 0})\n            continue\n        P_c = [parsed[p[\"key\"]][0] for p in t[\"rows\"] if p[\"family\"] != r[\"family\"] and parsed[p[\"key\"]][0] is not None]\n        if len(P_c) < 2:\n            out.append({\"key\": r[\"key\"], \"c_exact\": None, \"n_peers_exact\": len(P_c)})\n            continue\n        eqs = [eq(cs, p) for p in P_c]\n        out.append({\"key\": r[\"key\"], \"c_exact\": 1 - sum(e is True for e in eqs) / len(P_c), \"n_peers_exact\": len(P_c),\n                    \"n_unknown_exact\": sum(e is None for e in eqs)})\n    return {\"sentence_id\": t[\"sentence_id\"], \"rows\": out, \"n_unknown_pairs\": n_unknown}\n\n\ndef stage_exact(workers: int) -> None:\n    outp = CACHE / \"exact_E2.jsonl\"\n    done = {r[\"sentence_id\"] for r in jl(outp)}\n    T = [t for t in sentence_tasks() if t[\"sentence_id\"] not in done]\n    logger.info(f\"exact: {len(T)} sentences\")\n    with ProcessPoolExecutor(max_workers=workers, mp_context=mp.get_context(\"spawn\"), initializer=_init_ex) as ex, \\\n            outp.open(\"a\") as fh:\n        futs = {ex.submit(_exact_one, t): t for t in T}\n        for fu in as_completed(futs):\n            try:\n                res = fu.result()\n            except Exception as e:  # noqa: BLE001\n                res = {\"sentence_id\": futs[fu][\"sentence_id\"], \"rows\": [], \"error\": str(e)[:300]}\n            fh.write(json.dumps(res, ensure_ascii=False) + \"\\n\")\n            fh.flush()\n\n\ndef main() -> None:\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--stage\", required=True)\n    ap.add_argument(\"--workers\", type=int, default=44)\n    a = ap.parse_args()\n    setup_log(f\"consensus_{a.stage}\")\n    if a.stage == \"l3\":\n        asyncio.run(_l3([t[\"text\"] for t in sentence_tasks()]))\n    elif a.stage == \"score\":\n        stage_score(a.workers)\n    elif a.stage == \"pairwise\":\n        stage_pairwise(a.workers)\n    elif a.stage == \"exact\":\n        stage_exact(a.workers)\n\n\nif __name__ == \"__main__\":\n    main()\n\"\"\"Shared paths / io / logging for the E2-A label-free scoring processes. Import scoring.guard BEFORE this module.\"\"\"\nfrom __future__ import annotations\n\nimport json\nimport sys\nfrom pathlib import Path\n\nfrom loguru import logger\n\nWS = Path(__file__).resolve().parents[1]\nCAND = WS / \"e2\" / \"candidates_E2_nolabels.jsonl\"\nCACHE = WS / \"cache\"\nFROZEN = WS / \"frozen\"\nLOGS = WS / \"logs\"\nCACHE.mkdir(exist_ok=True)\nLOGS.mkdir(exist_ok=True)\n\n\ndef setup_log(name: str) -> None:\n    logger.remove()\n    logger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\n    logger.add(LOGS / f\"{name}.log\", rotation=\"30 MB\", level=\"DEBUG\")\n\n\ndef jl(p: Path) -> list[dict]:\n    if not p.exists():\n        return []\n    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()]\n\n\ndef append_jsonl(p: Path, rows: list[dict]) -> None:\n    with p.open(\"a\", encoding=\"utf-8\") as f:\n        for r in rows:\n            f.write(json.dumps(r, ensure_ascii=False) + \"\\n\")\n\n\ndef candidates() -> list[dict]:\n    return jl(CAND)\n\n\ndef by_sentence(rows: list[dict]) -> dict[str, list[dict]]:\n    out: dict[str, list[dict]] = {}\n    for r in rows:\n        out.setdefault(r[\"sentence_id\"], []).append(r)\n    return out", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [18] TOOL CALL — Bash · 2026-09-25 16:43:18 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11 && cat lib/nl2fol_metrics.py; sed -n 1,140p analysis/analyse_E2A.py
```

### [19] TOOL RESULT — Bash · 2026-09-25 16:43:18 UTC

```
{"stdout": "\"\"\"Reusable gold-free NL->FOL faithfulness metrics (E2-A, iteration 5), thin wrappers over the FROZEN code copies in\n../frozen (exp-5 peer_text / pool_scoring / vendor_c eqmv) and ../freeze_copy (consensus_variants). Nothing is refit.\n\nEvery per-candidate score is oriented HIGHER = MORE LIKELY AN ERROR (unfaithful translation).\nEvery function states (i) what it MEASURES, (ii) what it does NOT measure, (iii) whether it needs a gold formula, (iv) cost.\n\nEntry points\n  parse_fol(fol)                                        dataset-E parser; None = unparseable (coverage failure)\n  c_score_align(fol, peers, family=None)                V0, the frozen primary consensus score\n  c_exact(fol, peers, family=None)                      same consensus with exact symbol names (no aligner)\n  peer_text(text, fol, peers, family=None, q=None)      PT: frozen fusion of graded consensus + V0 + text-side checks\n  variants_for_sentence(rows, weights=None)             V1-V5 for every output of ONE sentence (set-level)\n  family_weights_from_sentences(list_of_rows_lists)     label-free family reliability weights for V2/V3/V5\n  evaluate(scores, labels, strata, sentence_ids)        stratified AUROC + stratified sentence-cluster bootstrap CI\n\n`peers` = list of (peer_fol: str, peer_family: str): formalizations of the SAME sentence produced by other systems.\nWith `family` given, peers of the candidate's own model family are dropped (leave-own-family-out, as frozen).\n\"\"\"\nfrom __future__ import annotations\n\nimport sys\nfrom pathlib import Path\n\n_WS = Path(__file__).resolve().parents[1]\nfor _p in (_WS / \"frozen\" / \"exp5\" / \"src\", _WS / \"freeze_copy\", _WS / \"frozen\" / \"eval2\" / \"src\"):\n    if str(_p) not in sys.path:\n        sys.path.insert(0, str(_p))\n\nimport numpy as np  # noqa: E402\n\nimport peer_text as _PT  # noqa: E402  (frozen exp-5; binds the dataset-E parser)\n\n_PRE5 = None\n\n\ndef _prereg5() -> dict:\n    global _PRE5\n    if _PRE5 is None:\n        import json\n        _PRE5 = json.loads((_WS / \"frozen\" / \"exp5\" / \"results\" / \"prereg.json\").read_text())\n    return _PRE5\n\n\ndef parse_fol(fol: str | None):\n    \"\"\"MEASURES: whether `fol` parses under the dataset-E grammar (the parser that defines UNPARSEABLE labels).\n    Returns the AST or None. GOLD: not needed. COST: microseconds.\"\"\"\n    return _PT.parse_fol(fol) if fol else None\n\n\ndef _pool(peers, family):\n    return [p for p, f in peers if (family is None or f != family)]\n\n\ndef c_score_align(fol: str, peers: list[tuple[str, str]], family: str | None = None, min_peers: int = 2) -> float | None:\n    \"\"\"V0 (PRIMARY, frozen). MEASURES: 1 - (share of parseable peer formalizations of the same sentence, from model families\n    other than the candidate's, that the iteration-1 eqmv procedure proves z3-equivalent to the candidate modulo a\n    predicate/constant vocabulary alignment). i.e. how far the candidate sits from what independent systems write.\n    DOES NOT MEASURE: agreement with a reference, or truth. An error that most peers share scores as faithful\n    (peer-endorsed error); a correct but idiosyncratic reading scores as an error; a wrong predicate in the right place\n    can be aligned away (MEANING_RENAME blind spot).\n    Unparseable candidate -> 1.0; < `min_peers` parseable peers -> None (the caller imputes; E2 used exp-5's neutral 0.6266).\n    GOLD: not needed. COST: the peers' generation (~$0.002 per sentence for 7 families) + z3 (eqmv 3 s cap per pair).\"\"\"\n    from common import eqmv  # vendor_c (bound to the dataset-E parser by peer_text)\n    e = parse_fol(fol)\n    if e is None:\n        return 1.0\n    cs = _PT.canon(e)\n    P = []\n    for p in _pool(peers, family):\n        pe = parse_fol(p)\n        if pe is not None:\n            P.append(_PT.canon(pe))\n    if len(P) < min_peers:\n        return None\n    agree = 0\n    for ps in P:\n        if ps == cs:\n            agree += 1\n            continue\n        a, b = (cs, ps) if cs < ps else (ps, cs)  # frozen canonical argument order\n        try:\n            r = eqmv(_PT.parse_fol(a), _PT.parse_fol(b))\n            agree += bool(r and r[0] is True)\n        except Exception:  # noqa: BLE001 - UNKNOWN counts as not equivalent\n            pass\n    return 1 - agree / len(P)\n\n\ndef c_exact(fol: str, peers: list[tuple[str, str]], family: str | None = None, min_peers: int = 2, ms: int = 2000) -> float | None:\n    \"\"\"MEASURES: 1 - share of family-disjoint parseable peers that z3 proves equivalent to the candidate with symbols\n    identified by their EXACT names (no aligner). Stricter than V0: any vocabulary difference counts as disagreement, so it\n    false-alarms on correct candidates whose wording differs from the peers'. DOES NOT MEASURE: meaning across vocabularies.\n    GOLD: not needed. COST: as V0, z3 only (2 x `ms` per pair).\"\"\"\n    e = parse_fol(fol)\n    if e is None:\n        return 1.0\n    P = [parse_fol(p) for p in _pool(peers, family)]\n    P = [p for p in P if p is not None]\n    if len(P) < min_peers:\n        return None\n    n = 0\n    for pe in P:\n        if _PT.canon(pe) == _PT.canon(e):\n            n += 1\n            continue\n        n += bool(_PT.z3_entails(e, pe, ms) is True and _PT.z3_entails(pe, e, ms) is True)\n    return 1 - n / len(P)\n\n\ndef peer_text(text: str, fol: str, peers: list[tuple[str, str]], family: str | None = None, q: dict | None = None) -> dict:\n    \"\"\"PT (frozen exp-5 fusion). MEASURES: a fixed logistic combination (coefficients frozen on the iteration-2 screen) of\n    ALIGN graded consensus g, V0, L2-bow (share of the sentence's content words the formula's symbols do not carry, plus\n    unanchored predicates) and L3 (mismatches between an LLM's role questionnaire of the TEXT and the formula's z3 role\n    profile; needs `q` from the exp-A questionnaire, else the neutral value is used).\n    Returns {'p_error', 'c_score_align', 'g_align', 'l2_bow', 'l3_z3'}. DOES NOT MEASURE: anything the peers all get wrong\n    and the text words do not reveal (scope, binding). GOLD: not needed. COST: V0's plus one small LLM call per sentence (L3).\"\"\"\n    import pool_scoring as PS\n    pre = _prereg5()\n    P = dict(pre[\"scoring_params\"])\n    P.update(variants=[\"ALIGN\"], k6_seeds=0, famfield=False, medoid_budget_s=0)\n    rows = [{\"key\": \"CAND\", \"fol\": fol, \"family\": family or \"__cand__\", \"family_field\": family or \"__cand__\", \"system\": \"cand\", \"is_peer\": True}]\n    rows += [{\"key\": f\"P{i}\", \"fol\": p, \"family\": f, \"family_field\": f, \"system\": f\"peer{i}\", \"is_peer\": True} for i, (p, f) in enumerate(peers)]\n    out = {r[\"key\"]: r for r in PS.score_sentence({\"sentence_id\": \"lib\", \"text\": text, \"q\": q, \"rows\": rows}, P)[\"rows\"]}\n    s = out[\"CAND\"]\n    if s.get(\"coverage_status\") != \"OK\":\n        return {\"p_error\": 1.0, \"c_score_align\": 1.0, \"g_align\": 1.0, \"l2_bow\": 1.0, \"l3_z3\": 1.0}\n    neutral = pre[\"imputation\"][\"neutral\"]\n    feats = dict(s)\n    for k in (\"c_score_align\", \"ALIGN:g_score\", \"l2_bow\", \"l3_z3\"):\n        if feats.get(k) is None:\n            feats[k] = neutral.get(k)\n    feats[\"coverage_status\"] = \"OK\"\n    return {\"p_error\": _PT.fused_score(pre[\"frozen\"], feats)[\"p_error\"], \"c_score_align\": feats[\"c_score_align\"],\n            \"g_align\": feats[\"ALIGN:g_score\"], \"l2_bow\": feats[\"l2_bow\"], \"l3_z3\": feats[\"l3_z3\"]}\n\n\ndef variants_for_sentence(rows: list[dict], weights: dict | None = None) -> dict[str, dict]:\n    \"\"\"SET-LEVEL (all outputs of ONE sentence). rows = [{'row_key', 'fol', 'family', 'slot'}]. Builds the eval-2 pairwise\n    eqmv matrix, then returns per row_key {V0, c_exact, V1 c_pn, V2 c_rw, V3 c_pn_rw, V5 c_v5} with the frozen freeze code.\n    MEASURES (V1): disagreement normalised by the size of the largest agreeing class (discounts scattered peers);\n    (V2/V3/V5): the same with label-free family reliability weights (`weights` from family_weights_from_sentences; None =\n    uniform). On E2 none of V1-V5 was carried by the freeze (development gain < +0.015 over V0). GOLD: not needed.\"\"\"\n    import consensus_variants as CV\n    import pairwise\n    m = pairwise.pairwise_matrix([{\"row_key\": r[\"row_key\"], \"fol\": r[\"fol\"], \"slot\": r.get(\"slot\", r[\"family\"]), \"family\": r[\"family\"],\n                                   \"family_field\": r[\"family\"], \"system_class\": \"llm\"} for r in rows])\n    m[\"sentence_id\"] = \"lib\"\n    I = CV.build_index(m)\n    w = weights or {}\n    out = {}\n    for r in rows:\n        k = r[\"row_key\"]\n        out[k] = {\"V0\": CV.c_score_align(I, k), \"c_exact\": CV.c_exact(I, k), \"V1\": CV.c_pn(I, k), \"V2\": CV.c_rw(I, k, w),\n                  \"V3\": CV.c_pn_rw(I, k, w), \"V5\": CV.c_v5(I, k, w)}\n    return out\n\n\ndef family_weights_from_sentences(sentences: list[list[dict]]) -> dict:\n    \"\"\"Label-free family reliability weights (mean cross-family agreement rate, shrunk to the grand mean with 20\n    pseudo-sentences; freeze consensus_variants.family_weights). MEASURES how often a family's outputs agree with other\n    families' - a proxy for reliability, NOT accuracy. GOLD: not needed.\"\"\"\n    import consensus_variants as CV\n    import pairwise\n    idx = []\n    for i, rows in enumerate(sentences):\n        m = pairwise.pairwise_matrix([{\"row_key\": r[\"row_key\"], \"fol\": r[\"fol\"], \"slot\": r.get(\"slot\", r[\"family\"]), \"family\": r[\"family\"],\n                                       \"family_field\": r[\"family\"], \"system_class\": \"llm\"} for r in rows])\n        m[\"sentence_id\"] = f\"s{i}\"\n        idx.append(CV.build_index(m))\n    return CV.family_weights(idx, {f\"s{i}\": 0 for i in range(len(idx))}, None)\n\n\ndef evaluate(scores, labels, strata, sentence_ids, b: int = 2000, seed: int = 0) -> dict:\n    \"\"\"META-EVALUATION of any score column. labels: 1 = ERROR, 0 = CORRECT (None rows are skipped). MEASURES: the\n    within-stratum pair AUROC (probability that a random ERROR scores above a random CORRECT of the same stratum) with a\n    stratified sentence-cluster bootstrap 95% CI. 0.5 = does not track correctness.\"\"\"\n    from stats import WStratAuc, ci, strat_auc\n    sys.path.insert(0, str(_WS / \"analysis\"))\n    from analyse_E2A import strat_boot_weights\n    s = np.asarray(scores, float)\n    y = np.array([np.nan if v is None else float(v) for v in labels])\n    st, sid = np.asarray(strata), np.asarray(sentence_ids)\n    m = ~np.isnan(s) & ~np.isnan(y)\n    W = strat_boot_weights(sid[m], st[m], b, seed)\n    f = WStratAuc(y[m], s[m], st[m])\n    return {\"n\": int(m.sum()), \"strat_auroc\": float(strat_auc(y[m], s[m], st[m])), \"ci\": ci([f(W[i]) for i in range(b)])}\n#!/usr/bin/env python3\n\"\"\"E2-A analyses (plan STEP 4-5). Runs ONLY after both seals verify; joins sealed labels to sealed scores by row_key.\n\n  join       verify score_seal.json (recompute every hash) + e2src verify_seal.py, assert score seal time < join time,\n             write per_item_E2A.jsonl (scores + labels + complexity)\n  analyse    (a) primary confirmation, (b) S4_E2 nesting, H-MECH (i)-(iv), H-IMPROVE, H-RENAME, complexity, system tau-b,\n             coverage, cost, placebos -> results/*.json, tables.md\nStatistics: frozen eval-2 stats (auc, strat_auc, WStratAuc); stratified sentence-cluster bootstrap (sentences resampled\nWITHIN stratum, B = 2000, seed 0; the prereg'd scheme) with the frozen pooled SentBoot as a sensitivity; S4 via the frozen\nT1 s4.fit_s4_oof (C = 1.0, 5 E2 folds).\n\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport glob\nimport hashlib\nimport json\nimport math\nimport subprocess\nimport sys\nimport time\nfrom collections import Counter, defaultdict\nfrom pathlib import Path\n\nimport numpy as np\n\nWS = Path(__file__).resolve().parents[1]\nsys.path.insert(0, str(WS / \"frozen\" / \"eval2\" / \"src\"))\nsys.path.insert(0, str(WS / \"frozen\" / \"t1\"))\nfrom stats import SentBoot, WStratAuc, auc, ci, strat_auc  # noqa: E402  (frozen eval-2)\n\nRES = WS / \"results\"\nRES.mkdir(exist_ok=True)\nE2S = WS / \"e2src\"\nB = 2000\nLONG = (\"L25\", \"EXC\")\nPRIMARY = \"c_score_align\"\nBAR = \"judge_cheap_disg\"\nMETRICS = [\"c_score_align\", \"p_peer_text\", \"c_exact\", \"g_align\", \"l2_bow\", \"l3_z3\", \"c_pn\", \"c_rw\", \"c_pn_rw\", \"c_two\", \"c_v5\",\n           \"judge_cheap_disg\", \"judge_cheap_orig\", \"judge_cheap2_disg\", \"judge_cheap2_orig\", \"judge_local_qwen8b_disg\",\n           \"judge_local_qwen8b_orig\", \"pilot_joint_conflict\", \"pilot_arity_incons\", \"pilot_shape_incons\", \"pilot_dangling\",\n           \"pilot_rerun_jacc\"]\nLABEL_OF = {\"c_score_align\": \"V0 c_score_align (frozen consensus)\", \"p_peer_text\": \"PT p_peer_text (frozen fusion)\",\n            \"c_exact\": \"c_exact (no aligner)\", \"g_align\": \"ALIGN graded g\", \"l2_bow\": \"L2-bow (text side)\", \"l3_z3\": \"L3 (text side)\",\n            \"c_pn\": \"V1 plurality-normalised\", \"c_rw\": \"V2 reliability-weighted\", \"c_pn_rw\": \"V3 = V1+V2\", \"c_two\": \"V4 two-channel\",\n            \"c_v5\": \"V5 3-pool\", \"judge_cheap_disg\": \"flash-lite rubric A, disguised (PRIMARY BAR)\",\n            \"judge_cheap_orig\": \"flash-lite rubric A, original\", \"judge_cheap2_disg\": \"gpt-4.1-nano P(YES), disguised\",\n            \"judge_cheap2_orig\": \"gpt-4.1-nano P(YES), original\", \"judge_local_qwen8b_disg\": \"local Qwen3-8B, disguised\",\n            \"judge_local_qwen8b_orig\": \"local Qwen3-8B, original\", \"pilot_joint_conflict\": \"pilot m1 joint-load conflict (adapted)\",\n            \"pilot_arity_incons\": \"pilot m2 arity inconsistency\", \"pilot_shape_incons\": \"pilot m2 shape inconsistency\",\n            \"pilot_dangling\": \"pilot m3 dangling symbols\", \"pilot_rerun_jacc\": \"pilot m5 1 - rerun Jaccard (cross-system proxy)\", \"S4_E2\": \"S4_E2 stack (OOF)\", \"S4_E2_plus_V0\": \"S4_E2 + V0 (OOF)\"}\nS4_FEATS = [\"judge_cheap_disg\", \"judge_cheap_orig\", \"judge_cheap2_disg\", \"judge_cheap2_orig\", \"judge_local_qwen8b_disg\",\n            \"judge_local_qwen8b_orig\", \"l2_bow\", \"l3_z3\"]\n\n\ndef jl(p: Path) -> list[dict]:\n    return [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []\n\n\ndef sha256(p: Path) -> str:\n    return hashlib.sha256(p.read_bytes()).hexdigest()\n\n\ndef dump(name: str, obj) -> None:\n    (RES / name).write_text(json.dumps(obj, indent=1, default=lambda o: None if isinstance(o, float) and math.isnan(o) else str(o)))\n\n\n# ================================================================================================================ join\ndef stage_join() -> None:\n    seal = json.loads((WS / \"score_seal.json\").read_text())\n    bad = [k for k, h in seal[\"sha256\"].items() if not (WS / k).exists() or sha256(WS / k) != h]\n    assert not bad, f\"score seal broken: {bad[:5]}\"\n    vs = subprocess.run([str(E2S / \".venv\" / \"bin\" / \"python\"), str(E2S / \"src_e2\" / \"verify_seal.py\")], capture_output=True,\n                        text=True, cwd=str(E2S))\n    assert vs.returncode == 0 and \"seal_intact\" in (vs.stdout + vs.stderr), f\"label seal verify failed: {vs.stdout[-500:]} {vs.stderr[-500:]}\"\n    lseal = json.loads((E2S / \"seal.json\").read_text())\n    t_join = time.time()\n    assert seal[\"written_ts\"] < t_join, \"score seal must predate the join\"\n    labels = {r[\"row_key\"]: r for r in jl(E2S / \"sealed\" / \"labels_E2.jsonl\") if r.get(\"system_class\") == \"llm\"}\n    sents = {s[\"sentence_id\"]: s for s in json.loads((E2S / \"work\" / \"sentences_E2_active.json\").read_text())}\n    scores = jl(WS / \"scores_E2A.jsonl\")\n    out, miss = [], 0\n    for r in scores:\n        lab = labels.get(r[\"row_key\"])\n        if lab is None:\n            miss += 1\n        s = sents[r[\"sentence_id\"]]\n        r = dict(r)\n        r.update({\"label\": (lab or {}).get(\"label\"), \"label_tier\": (lab or {}).get(\"label_tier\"),\n                  \"reading_choice\": bool((lab or {}).get(\"reading_choice\")), \"vex\": (lab or {}).get(\"vex\"),\n                  \"vex_eq\": (lab or {}).get(\"vex_eq\"), \"auto_label\": (lab or {}).get(\"auto_label\"),\n                  \"error_ops\": (lab or {}).get(\"error_ops\"), \"reference_status\": (lab or {}).get(\"reference_status\"),\n                  \"correct_not_equivalent\": (lab or {}).get(\"correct_not_equivalent\"),\n                  \"n_conditions\": s.get(\"n_conditions\"), \"n_quant\": s.get(\"n_quant\"), \"depth\": s.get(\"depth\")})\n        out.append(r)\n    p = WS / \"per_item_E2A.jsonl\"\n    p.write_text(\"\".join(json.dumps(r, ensure_ascii=False) + \"\\n\" for r in out))\n    rec = {\"score_seal_utc\": seal[\"written_utc\"], \"score_seal_ts\": seal[\"written_ts\"], \"label_seal_utc\": lseal.get(\"sealed_at_utc\"),\n           \"label_seal_verify_stdout_tail\": vs.stdout[-400:], \"join_utc\": time.strftime(\"%Y-%m-%dT%H:%M:%SZ\", time.gmtime(t_join)),\n           \"join_ts\": t_join, \"n_rows\": len(out), \"rows_without_label\": miss, \"per_item_sha256\": sha256(p),\n           \"score_seal_files_verified\": len(seal[\"sha256\"])}\n    dump(\"join_record.json\", rec)\n    print(json.dumps(rec, indent=1))\n\n\n# ============================================================================================================ helpers\nclass Data:\n    def __init__(self, rows: list[dict]):\n        self.rows = rows\n        self.n = len(rows)\n        self.col = lambda c: np.array([np.nan if r.get(c) is None else float(r[c]) for r in rows], float)\n        self.sid = np.array([r[\"sentence_id\"] for r in rows])\n        self.stratum = np.array([r[\"stratum\"] for r in rows])\n        lab = np.array([r.get(\"label\") for r in rows])\n        tier = np.array([r.get(\"label_tier\") for r in rows])\n        rc = np.array([bool(r.get(\"reading_choice\")) for r in rows])\n        cls = np.isin(lab, [\"CORRECT\", \"ERROR\"]) & ~rc\n        self.y = (lab == \"ERROR\").astype(float)\n        self.regime = {\"R_AB\": cls & np.isin(tier, [\"A\", \"B\"]), \"R_A\": cls & (tier == \"A\"),\n                       \"R_VEX\": cls & np.isin(tier, [\"A\", \"B\"]) & np.array([r.get(\"vex\") is True for r in rows]),\n                       \"R_AB_nopilot\": cls & np.isin(tier, [\"A\", \"B\"]) & ~np.array([bool(r.get(\"pilot\")) for r in rows])}\n        self.cells = {\"LONG (L25+EXC)\": np.isin(self.stratum, LONG), \"L25\": self.stratum == \"L25\", \"EXC\": self.stratum == \"EXC\",\n                      \"DT\": self.stratum == \"DT\", \"ALL\": np.ones(self.n, bool)}\n\n\ndef strat_boot_weights(sids, strata, b: int = B, seed: int = 0) -> np.ndarray:\n    \"\"\"Stratified sentence-cluster bootstrap: within each stratum, sentences resampled with replacement.\n    -> (B, n_rows) multiplicity weights.\"\"\"\n    sids, strata = np.asarray(sids), np.asarray(strata)\n    rng = np.random.default_rng(seed)\n    W = np.zeros((b, len(sids)))\n    for st in sorted(set(strata)):\n        m = strata == st\n        keys, inv = np.unique(sids[m], return_inverse=True)\n        S = len(keys)\n        C = np.stack([np.bincount(rng.integers(0, S, S), minlength=S) for _ in range(b)]).astype(float)\n        W[:, np.where(m)[0]] = C[:, inv]\n    return W", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [20] TOOL CALL — Bash · 2026-09-25 16:43:28 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11 && find frozen freeze_copy -name "*.py" | xargs wc -l | sort -n | tail -40; cat frozen/eval2/src/stats.py | head -120
```

### [21] TOOL RESULT — Bash · 2026-09-25 16:43:30 UTC

```
{"stdout": "    285 frozen/eval2/vendor_exp5/vendor_d/disguise.py\n    285 frozen/exp5/src/vendor_d/disguise.py\n    285 frozen/t1/src/disguise.py\n    322 frozen/t1/src/analysis.py\n    359 frozen/t1/src/screen.py\n    363 frozen/t1/src/b2_world_probe.py\n    377 frozen/t1/src/api_bar.py\n    379 frozen/eval2/src/part_a.py\n    391 frozen/t1/src/report_T1.py\n    423 frozen/t1/src/analysis_E.py\n    440 freeze_copy/gg.py\n    441 frozen/eval2/src/mechanism.py\n    457 frozen/eval2/vendor_exp5/vendor_c/peers.py\n    457 frozen/exp5/src/vendor_c/peers.py\n    458 frozen/eval2/vendor_exp5/vendor_a/repair_census.py\n    458 frozen/eval2/vendor_exp5/vendor_c/repair_census.py\n    458 frozen/eval2/vendor_exp5/vendor_d/labeller/repair_census.py\n    458 frozen/eval2/vendor_exp5/vendor_e/repair_census.py\n    458 frozen/exp5/src/vendor_a/repair_census.py\n    458 frozen/exp5/src/vendor_c/repair_census.py\n    458 frozen/exp5/src/vendor_d/labeller/repair_census.py\n    458 frozen/exp5/src/vendor_e/repair_census.py\n    458 frozen/t1/src/labeller/repair_census.py\n    470 frozen/eval2/vendor_exp5/vendor_c/consensus.py\n    470 frozen/exp5/src/vendor_c/consensus.py\n    611 frozen/t1/src/report.py\n    613 frozen/eval2/vendor_exp5/vendor_c/analysis.py\n    613 frozen/exp5/src/vendor_c/analysis.py\n    629 frozen/eval2/vendor_exp5/screen_fit.py\n    629 frozen/exp5/src/screen_fit.py\n    654 frozen/eval2/src/record.py\n    852 frozen/eval2/vendor_exp5/vendor_a/fol_triage.py\n    852 frozen/exp5/src/vendor_a/fol_triage.py\n    882 frozen/eval2/vendor_exp5/analyse_E.py\n    882 frozen/exp5/src/analyse_E.py\n    882 frozen/t1/src/exp5_analyse_E.py\n   1025 frozen/eval2/vendor_exp5/peer_text.py\n   1025 frozen/exp5/src/peer_text.py\n   1030 frozen/t1/src/analyse_T1.py\n  35526 total\n\"\"\"Statistics shared by every analysis: tie-aware AUROC, stratified (within-stratum pair) AUROC, and a\nsentence-cluster bootstrap that yields resample index arrays (numpy default_rng(0), B=2000).\"\"\"\nfrom __future__ import annotations\n\nfrom collections import defaultdict\n\nimport numpy as np\nfrom scipy.stats import rankdata\n\nB_DEFAULT = 2000\n\n\ndef auc(y, s) -> float:\n    \"\"\"Mann-Whitney AUROC with ties = 0.5 (identical to sklearn roc_auc_score).\"\"\"\n    y = np.asarray(y, dtype=float)\n    s = np.asarray(s, dtype=float)\n    n1 = int(y.sum())\n    n0 = len(y) - n1\n    if n1 == 0 or n0 == 0:\n        return float(\"nan\")\n    r = rankdata(s)\n    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))\n\n\ndef strat_auc(y, s, strata) -> float:\n    \"\"\"Within-stratum pair AUROC: sum_s w_s AUROC_s with w_s = n_err,s * n_cor,s (exp 5 'stratified').\"\"\"\n    y, s, strata = np.asarray(y, float), np.asarray(s, float), np.asarray(strata)\n    num = den = 0.0\n    for st in np.unique(strata):\n        m = strata == st\n        n1 = int(y[m].sum())\n        n0 = int(m.sum()) - n1\n        if n1 and n0:\n            num += auc(y[m], s[m]) * n1 * n0\n            den += n1 * n0\n    return num / den if den else float(\"nan\")\n\n\nclass ClusterBoot:\n    \"\"\"Sentence-cluster bootstrap resamples (sentence_ids drawn with replacement; all rows of a drawn sentence kept).\"\"\"\n\n    def __init__(self, sids, b: int = B_DEFAULT, seed: int = 0):\n        by = defaultdict(list)\n        for i, s in enumerate(sids):\n            by[s].append(i)\n        keys = sorted(by)\n        arr = [np.array(by[k]) for k in keys]\n        rng = np.random.default_rng(seed)\n        self.idx = [np.concatenate([arr[j] for j in rng.integers(0, len(keys), len(keys))]) for _ in range(b)]\n        self.n_clusters = len(keys)\n\n\ndef ci(vals, lo=2.5, hi=97.5):\n    v = np.asarray([x for x in vals if x is not None and not np.isnan(x)], float)\n    if len(v) == 0:\n        return [None, None]\n    return [float(np.percentile(v, lo)), float(np.percentile(v, hi))]\n\n\ndef boot_stat(boot: ClusterBoot, fn) -> list:\n    return [fn(ix) for ix in boot.idx]\n\n\n# ------------------------------------------------------------------ weighted (bootstrap-count) statistics\nclass WAuc:\n    \"\"\"AUROC under row weights (bootstrap multiplicities); ties = 0.5. Precomputes the score ranking once.\"\"\"\n\n    def __init__(self, y, s):\n        self.y = np.asarray(y, float)\n        vals, self.inv = np.unique(np.asarray(s, float), return_inverse=True)\n        self.nv = len(vals)\n\n    def __call__(self, w) -> float:\n        w = np.asarray(w, float)\n        W1 = np.bincount(self.inv, weights=w * self.y, minlength=self.nv)\n        W0 = np.bincount(self.inv, weights=w * (1 - self.y), minlength=self.nv)\n        den = W1.sum() * W0.sum()\n        if den <= 0:\n            return float(\"nan\")\n        cum0 = np.cumsum(W0) - W0\n        return float((W1 * (cum0 + 0.5 * W0)).sum() / den)\n\n\nclass WStratAuc:\n    \"\"\"Within-stratum pair AUROC under row weights.\"\"\"\n\n    def __init__(self, y, s, strata):\n        self.y = np.asarray(y, float)\n        strata = np.asarray(strata)\n        self.parts = [(np.where(strata == st)[0], WAuc(self.y[strata == st], np.asarray(s, float)[strata == st]))\n                      for st in np.unique(strata)]\n\n    def __call__(self, w) -> float:\n        w = np.asarray(w, float)\n        num = den = 0.0\n        for ix, wa in self.parts:\n            ww = w[ix]\n            n1 = (ww * self.y[ix]).sum()\n            n0 = (ww * (1 - self.y[ix])).sum()\n            if n1 > 0 and n0 > 0:\n                num += wa(ww) * n1 * n0\n                den += n1 * n0\n        return num / den if den else float(\"nan\")\n\n\nclass SentBoot:\n    \"\"\"Sentence-cluster bootstrap as multiplicity weights: W[b, i] = #times row i's sentence was drawn in replicate b\n    (numpy default_rng(seed); sentence_ids resampled with replacement).\"\"\"\n\n    def __init__(self, sids, b: int = B_DEFAULT, seed: int = 0):\n        sids = np.asarray(sids)\n        self.keys, self.sent_ix = np.unique(sids, return_inverse=True)\n        S = len(self.keys)\n        rng = np.random.default_rng(seed)\n        self.C = np.stack([np.bincount(rng.integers(0, S, S), minlength=S) for _ in range(b)]).astype(float)\n        self.B = b\n\n    def weights(self, b: int, mask=None):\n        w = self.C[b][self.sent_ix]\n        return w if mask is None else w[mask]", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [22] THINKING · 2026-09-25 16:43:40 UTC

```
`method.py` only orchestrates subprocess stages that need a private venv, GPU judge, and paid APIs, so it can't run in Colab—only the meta-evaluation of sealed scores against sealed labels (via `audit/rederive.py` and frozen `stats.py`) can execute there, so I'll show the stage list as a dry run and actually run that analysis. Next I'll inspect the per-item rows.
```

### [23] TOOL CALL — Bash · 2026-09-25 16:43:40 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11 && python3 - <<'EOF'
import json, collections
rows=[json.loads(l) for l in open('per_item_E2A.jsonl')]
print(len(rows)); r=rows[0]; print(json.dumps({k:(str(v)[:80]) for k,v in r.items()},indent=0))
order=json.load(open('e2src/work/e2a_order.json'))[:110]; keep=set(order)
rab=[r for r in rows if r['sentence_id'] in keep and r.get('label') in ('CORRECT','ERROR') and not r.get('reading_choice') and r.get('label_tier') in ('A','B') and r.get('system_class','llm')=='llm']
print(len(rab), collections.Counter((r['stratum'],r['label']) for r in rab))
print(collections.Counter(r.get('system_class') for r in rows))
EOF
head -c 600 results/rename_V0_rows.jsonl
```

### [24] TOOL RESULT — Bash · 2026-09-25 16:43:40 UTC

```
{"stdout": "5500\n{\n\"row_key\": \"87618fded07e3eb4|fewshot_v1\",\n\"item_id\": \"87618fded07e3eb4\",\n\"sentence_id\": \"679fdea26cad\",\n\"stratum\": \"EXC\",\n\"slot\": \"G1\",\n\"system\": \"G1:meta-llama/llama-3.1-8b-instruct\",\n\"family\": \"meta\",\n\"pilot\": \"True\",\n\"words\": \"19\",\n\"word_bin\": \"None\",\n\"exception_type\": \"without\",\n\"text_conditions\": \"1\",\n\"fold_E2\": \"2\",\n\"parse_ok\": \"True\",\n\"consensus_coverage\": \"OK\",\n\"n_peers_used\": \"8\",\n\"n_unknown_align\": \"0\",\n\"gen_cost_usd\": \"1.086e-05\",\n\"c_score_align__imputed\": \"False\",\n\"c_score_align\": \"1.0\",\n\"g_align__imputed\": \"False\",\n\"g_align\": \"1.0\",\n\"l2_bow__imputed\": \"False\",\n\"l2_bow\": \"0.125\",\n\"l3_z3__imputed\": \"False\",\n\"l3_z3\": \"0.25\",\n\"p_peer_text\": \"0.8927705659020497\",\n\"c_exact\": \"1.0\",\n\"c_pn\": \"1.0\",\n\"c_rw\": \"1.0\",\n\"c_pn_rw\": \"1.0\",\n\"c_v5\": \"1.0\",\n\"c_two\": \"0.8384464684152174\",\n\"c_align_pw\": \"1.0\",\n\"c_exact_z3direct\": \"1.0\",\n\"judge_cheap_disg\": \"None\",\n\"judge_cheap_disg_cost\": \"None\",\n\"judge_cheap_disg_share\": \"None\",\n\"judge_cheap_orig\": \"None\",\n\"judge_cheap_orig_cost\": \"None\",\n\"judge_cheap_orig_share\": \"None\",\n\"judge_cheap2_disg\": \"None\",\n\"judge_cheap2_disg_cost\": \"None\",\n\"judge_cheap2_disg_share\": \"None\",\n\"judge_cheap2_orig\": \"None\",\n\"judge_cheap2_orig_cost\": \"None\",\n\"judge_cheap2_orig_share\": \"None\",\n\"judge_local_qwen8b_disg\": \"0.050000000000000044\",\n\"judge_local_qwen8b_disg_cost\": \"None\",\n\"judge_local_qwen8b_disg_share\": \"None\",\n\"judge_local_qwen8b_orig\": \"0.050000000000000044\",\n\"judge_local_qwen8b_orig_cost\": \"None\",\n\"judge_local_qwen8b_orig_share\": \"None\",\n\"pilot_joint_conflict\": \"0\",\n\"pilot_arity_incons\": \"0\",\n\"pilot_shape_incons\": \"0\",\n\"pilot_dangling\": \"1.0\",\n\"pilot_rerun_jacc\": \"0.43553791887125226\",\n\"secs_consensus_sentence\": \"56.76\",\n\"label\": \"ERROR\",\n\"label_tier\": \"C\",\n\"reading_choice\": \"False\",\n\"vex\": \"False\",\n\"vex_eq\": \"False\",\n\"auto_label\": \"NO_REF\",\n\"error_ops\": \"['BIND']\",\n\"reference_status\": \"NO_TRUSTED_REFERENCE\",\n\"correct_not_equivalent\": \"False\",\n\"n_conditions\": \"3\",\n\"n_quant\": \"1\",\n\"depth\": \"3\"\n}\n273 Counter({('DT', 'CORRECT'): 105, ('DT', 'ERROR'): 74, ('EXC', 'ERROR'): 41, ('L25', 'ERROR'): 35, ('EXC', 'CORRECT'): 11, ('L25', 'CORRECT'): 7})\nCounter({None: 5500})\n{\"row_key\": \"74a7217d8d0e673e|fewshot_v1|RENAME_SYN\", \"type\": \"RENAME_SYN\", \"stratum\": \"L25\", \"v0_control\": 0.875, \"v0_parent\": 0.875}\n{\"row_key\": \"74a7217d8d0e673e|fewshot_v1|RENAME_NONCE\", \"type\": \"RENAME_NONCE\", \"stratum\": \"L25\", \"v0_control\": 1.0, \"v0_parent\": 0.875}\n{\"row_key\": \"c119d57cfe461a1a|fewshot_v1|RENAME_NONCE\", \"type\": \"RENAME_NONCE\", \"stratum\": \"EXC\", \"v0_control\": 1.0, \"v0_parent\": 0.5555555555555556}\n{\"row_key\": \"e3feb7957ea26502|fewshot_v1|RENAME_NONCE\", \"type\": \"RENAME_NONCE\", \"stratum\": \"DT\", \"v0_control\": 1.0, \"v0_parent\": 0.25}\n{\"row_key\": \"1226bd1421470e29|fewshot_v1|RE", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [25] ASSISTANT · 2026-09-25 16:44:04 UTC

```
The per-item rows don't contain the sentence text or the FOL, so I'll join them from `e2/candidates_E2_nolabels.jsonl` and build the mini data from whole sentences, balanced across strata.
```

### [26] TOOL CALL — Bash · 2026-09-25 16:44:04 UTC

```
mkdir -p /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh/scripts && cat > /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh/scripts/build_mini_demo_data.py <<'EOF'
"""Build mini_demo_data.json: <=100 labelled candidate rows (R_AB regime, 110-sentence prefix) of the E2-A artifact,
whole sentences only, balanced over the L25 / EXC / DT strata. Usage: python scripts/build_mini_demo_data.py <artifact_dir>"""
import hashlib, json, sys
from collections import Counter, defaultdict
from pathlib import Path

A = Path(sys.argv[1])
OUT = Path(__file__).resolve().parents[1] / "mini_demo_data.json"
jl = lambda p: [json.loads(l) for l in open(p) if l.strip()]
MAX_ROWS = 100
SCORES = ["c_score_align", "p_peer_text", "c_exact", "g_align", "l2_bow", "l3_z3", "c_pn", "c_rw", "c_pn_rw", "c_two", "c_v5",
          "judge_local_qwen8b_disg", "judge_local_qwen8b_orig", "pilot_joint_conflict", "pilot_arity_incons",
          "pilot_shape_incons", "pilot_dangling", "pilot_rerun_jacc"]
META = ["row_key", "sentence_id", "stratum", "slot", "system", "family", "words", "n_conditions", "n_quant", "depth",
        "parse_ok", "label", "label_tier", "error_ops", "reference_status", "correct_not_equivalent", "c_score_align__imputed"]

per = jl(A / "per_item_E2A.jsonl")
cand = {r["row_key"]: r for r in jl(A / "e2" / "candidates_E2_nolabels.jsonl")}
keep = set(json.load(open(A / "e2src" / "work" / "e2a_order.json"))[:110])
rab = [r for r in per if r["sentence_id"] in keep and r.get("label") in ("CORRECT", "ERROR") and not r.get("reading_choice")
       and r.get("label_tier") in ("A", "B")]
assert len(rab) == 273, len(rab)
by = defaultdict(list)
for r in rab:
    by[r["sentence_id"]].append(r)
h = lambda s: hashlib.sha1(("demo|" + s).encode()).hexdigest()
# sentences with both classes first (they carry within-stratum AUROC signal), then the rest; round-robin over strata
buckets = defaultdict(list)
for sid, rs in by.items():
    mixed = len({r["label"] for r in rs}) == 2
    buckets[rs[0]["stratum"]].append((not mixed, h(sid), sid))
for st in buckets:
    buckets[st].sort()
chosen, n = [], 0
quota = {"DT": 50, "L25": 25, "EXC": 25}
used = Counter()
progress = True
while progress:
    progress = False
    for st in ("DT", "EXC", "L25"):
        if not buckets[st]:
            continue
        sid = buckets[st][0][2]
        k = len(by[sid])
        if used[st] + k > quota[st] or n + k > MAX_ROWS:
            buckets[st].pop(0)
            progress = True
            continue
        buckets[st].pop(0)
        chosen.append(sid)
        used[st] += k
        n += k
        progress = True
rows = []
for sid in chosen:
    for r in sorted(by[sid], key=lambda r: r["slot"]):
        c = cand[r["row_key"]]
        rows.append({"text": c["text"], "candidate_fol": c["candidate_fol"], **{k: r.get(k) for k in META},
                     "scores": {k: r.get(k) for k in SCORES}})
ref = json.load(open(A / "audit" / "rederive_out.json"))
rename = jl(A / "results" / "rename_V0_rows.jsonl")
data = {
    "description": "E2-A NL->FOL meta-evaluation subset: labelled LLM candidate formalizations (R_AB regime: tier A/B "
                   "prover-built or audited labels, no reading-choice rows) from the 110-sentence random prefix. "
                   "Every score is label-free, sealed BEFORE labels, and oriented higher = more likely ERROR.",
    "source_files": ["per_item_E2A.jsonl", "e2/candidates_E2_nolabels.jsonl", "results/rename_V0_rows.jsonl", "audit/rederive_out.json"],
    "n_rows": len(rows), "n_sentences": len(chosen),
    "rows": rows,
    "rename_controls": [{k: r[k] for k in ("type", "stratum", "v0_control", "v0_parent")} for r in rename],
    "full_run_reference": {k: ref[k] for k in ("ALL", "DT", "LONG", "placebo_shuffled", "RENAME_SYN", "RENAME_NONCE",
                                               "drift_majority_agreement", "spend_usd")},
}
OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1))
print(len(rows), len(chosen), Counter((r["stratum"], r["label"]) for r in rows), OUT.stat().st_size)
print(Counter(r["c_score_align__imputed"] for r in rows), Counter(r["scores"]["c_score_align"] is None for r in rows))
EOF
cd /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh && python3 scripts/build_mini_demo_data.py /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11
```

### [27] TOOL RESULT — Bash · 2026-09-25 16:44:04 UTC

```
{"stdout": "93 11 Counter({('DT', 'CORRECT'): 35, ('L25', 'ERROR'): 17, ('DT', 'ERROR'): 15, ('EXC', 'ERROR'): 12, ('EXC', 'CORRECT'): 7, ('L25', 'CORRECT'): 7}) 143195\nCounter({False: 93}) Counter({False: 93})", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [28] ASSISTANT · 2026-09-25 16:44:20 UTC

```
The mini data has 93 rows from 11 whole sentences and no imputed V0 values. Next I'll check how `analyse_E2A.py` computes the delta CI so the notebook uses the same method.
```

### [29] TOOL CALL — Bash · 2026-09-25 16:44:20 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11 && grep -n "def \|delta\|WStratAuc(" analysis/analyse_E2A.py | head -60
```

### [30] TOOL RESULT — Bash · 2026-09-25 16:44:20 UTC

```
{"stdout": "56:def jl(p: Path) -> list[dict]:\n60:def sha256(p: Path) -> str:\n64:def dump(name: str, obj) -> None:\n69:def stage_join() -> None:\n108:    def __init__(self, rows: list[dict]):\n126:def strat_boot_weights(sids, strata, b: int = B, seed: int = 0) -> np.ndarray:\n141:def cell_eval(D: Data, mask: np.ndarray, metrics: dict[str, np.ndarray], pairs: list[tuple[str, str]], seed: int = 0) -> dict:\n143:    paired deltas on rows where both are present.\"\"\"\n148:           \"metrics\": {}, \"deltas\": {}}\n159:        f = WStratAuc(y[m], s[m], st[m])\n170:        fa, fc = WStratAuc(y[m], sa[m], st[m]), WStratAuc(y[m], sc[m], st[m])\n176:        out[\"deltas\"][f\"{a} - {c}\"] = {\"n\": int(m.sum()), \"n_error\": ne, \"n_correct\": nc,\n178:                                       \"delta\": float(pt), \"ci\": c95, \"p_le0\": float(np.mean(d <= 0)),\n180:                                       \"pooled_delta\": float(auc(y[m], sa[m]) - auc(y[m], sc[m]))}\n185:        out[\"deltas\"][f\"{a} - {c}\"][\"ci_pooled_cluster_boot\"] = ci(dp)\n189:def mde80(se: float) -> float:\n194:def s4(D: Data, reg: np.ndarray) -> dict:\n216:def load_pairwise() -> dict:\n222:def hmech(D: Data, reg: np.ndarray) -> dict:\n298:    def ed(w, sel):\n307:    delta = (e3 + d3) - (e1 + d1)\n309:    out[\"iii_net\"] = {\"delta_e_plus_d_T3_minus_T1\": float(delta), \"ci\": c95, \"e_T1\": float(e1), \"d_T1\": float(d1), \"e_T3\": float(e3),\n311:                      \"verdict\": \"CONFIRMED\" if delta > 0 else \"REFUTED\"}\n316:    def cls_of(r):\n354:def stage_analyse(prefix: int = 0) -> None:\n391:    dA = L[\"deltas\"].get(f\"{PRIMARY} - {BAR}\", {})\n392:    dO = L[\"deltas\"].get(f\"{PRIMARY} - judge_cheap_orig\", {})\n393:    dN = L[\"deltas\"].get(f\"{PRIMARY} - judge_cheap2_orig\", {})\n394:    dNd = L[\"deltas\"].get(f\"{PRIMARY} - judge_cheap2_disg\", {})\n395:    dB = L[\"deltas\"].get(\"S4_E2_plus_V0 - S4_E2\", {})\n396:    a_ok = bool(dA.get(\"ci_gt0\")) and (dO.get(\"delta\", -1) > 0) and (dN.get(\"delta\", -1) > 0)\n411:    pt = dA.get(\"delta\")\n425:    dL = L25[\"deltas\"].get(f\"{PRIMARY} - {BAR}\", {})\n429:        \"a\": {\"cell\": \"R_AB LONG (L25+EXC)\", \"delta_vs_flashlite_disg\": dA, \"delta_vs_flashlite_orig\": dO,\n430:              \"delta_vs_nano_orig\": dN, \"delta_vs_nano_disg\": dNd, \"holds\": a_ok, \"n\": L[\"n_rows\"], \"n_error\": L[\"n_error\"],\n436:                                    \"V0_minus_local_disg\": L[\"deltas\"].get(f\"{PRIMARY} - judge_local_qwen8b_disg\"),\n437:                                    \"V0_minus_local_orig\": L[\"deltas\"].get(f\"{PRIMARY} - judge_local_qwen8b_orig\"),\n438:                                    \"PT_minus_local_disg\": L[\"deltas\"].get(\"p_peer_text - judge_local_qwen8b_disg\"),\n439:                                    \"L25_V0_minus_local_disg\": L25[\"deltas\"].get(f\"{PRIMARY} - judge_local_qwen8b_disg\"),\n440:                                    \"EXC_V0_minus_local_disg\": A[\"R_AB\"][\"EXC\"][\"deltas\"].get(f\"{PRIMARY} - judge_local_qwen8b_disg\"),\n441:                                    \"DT_V0_minus_local_disg\": A[\"R_AB\"][\"DT\"][\"deltas\"].get(f\"{PRIMARY} - judge_local_qwen8b_disg\")},\n444:            \"L25_alone\": {\"delta\": dL, \"testable\": L25[\"testable\"], \"se_from_ci\": se_L, \"mde80\": mde80(se_L) if se_L else None},\n445:            \"EXC\": A[\"R_AB\"][\"EXC\"][\"deltas\"].get(f\"{PRIMARY} - {BAR}\"),\n446:            \"DT_sign\": A[\"R_AB\"][\"DT\"][\"deltas\"].get(f\"{PRIMARY} - {BAR}\"),\n447:            \"long_without_pilot\": A[\"R_AB_nopilot\"][\"LONG (L25+EXC)\"][\"deltas\"].get(f\"{PRIMARY} - {BAR}\"),\n448:            \"R_A_long\": A[\"R_A\"][\"LONG (L25+EXC)\"][\"deltas\"].get(f\"{PRIMARY} - {BAR}\"),\n449:            \"R_VEX_long\": A[\"R_VEX\"][\"LONG (L25+EXC)\"][\"deltas\"].get(f\"{PRIMARY} - {BAR}\")}}\n456:           \"exploratory_long_pool_deltas_vs_V0\": {v: L[\"deltas\"].get(f\"{v} - {PRIMARY}\") for v in (\"c_pn\", \"c_rw\", \"c_pn_rw\", \"c_two\", \"c_v5\", \"c_exact\")}}\n457:    ps = sorted([(k, v[\"p_le0\"]) for k, v in imp[\"exploratory_long_pool_deltas_vs_V0\"].items() if v], key=lambda t: t[1])\n485:                                            \"delta_V0_minus_bar\": ce[\"deltas\"].get(f\"{PRIMARY} - {BAR}\"), \"binary_e_d_thr0.5\": ed_}\n491:        comp[\"exception_type\"][et] = {\"n\": ce[\"n_rows\"], \"delta\": ce[\"deltas\"].get(f\"{PRIMARY} - {BAR}\")}\n534:    print(json.dumps({\"overall\": overall, \"a\": {k: dA.get(k) for k in (\"delta\", \"ci\", \"n\")}, \"b\": {k: dB.get(k) for k in (\"delta\", \"ci\")}}, indent=1))\n537:def main() -> None:", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [31] TOOL CALL — Bash · 2026-09-25 16:44:22 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11 && sed -n 141,188p analysis/analyse_E2A.py
```

### [32] TOOL RESULT — Bash · 2026-09-25 16:44:22 UTC

```
{"stdout": "def cell_eval(D: Data, mask: np.ndarray, metrics: dict[str, np.ndarray], pairs: list[tuple[str, str]], seed: int = 0) -> dict:\n    \"\"\"strat AUROC (+ pooled) with stratified cluster-bootstrap CIs for each metric on rows of `mask` where it is present;\n    paired deltas on rows where both are present.\"\"\"\n    idx = np.where(mask)[0]\n    y, st, sid = D.y[idx], D.stratum[idx], D.sid[idx]\n    out = {\"n_rows\": int(len(idx)), \"n_error\": int(y.sum()), \"n_correct\": int(len(idx) - y.sum()),\n           \"n_sentences\": int(len(set(sid))), \"n_err_sent\": int(len(set(sid[y == 1]))), \"n_cor_sent\": int(len(set(sid[y == 0]))),\n           \"metrics\": {}, \"deltas\": {}}\n    out[\"testable\"] = bool(out[\"n_error\"] >= 50 and out[\"n_correct\"] >= 50 and out[\"n_err_sent\"] >= 25 and out[\"n_cor_sent\"] >= 25)\n    if len(idx) == 0 or y.sum() == 0 or y.sum() == len(y):\n        return out\n    W = strat_boot_weights(sid, st, B, seed)\n    for name, v in metrics.items():\n        s = v[idx]\n        m = ~np.isnan(s)\n        if m.sum() < 10 or len(set(y[m])) < 2:\n            out[\"metrics\"][name] = {\"n\": int(m.sum()), \"strat\": None}\n            continue\n        f = WStratAuc(y[m], s[m], st[m])\n        vals = np.array([f(W[b][m]) for b in range(B)])\n        out[\"metrics\"][name] = {\"n\": int(m.sum()), \"strat\": float(strat_auc(y[m], s[m], st[m])), \"strat_ci\": ci(vals),\n                                \"pooled\": float(auc(y[m], s[m])), \"coverage\": float(m.mean())}\n    for a, c in pairs:\n        if a not in metrics or c not in metrics:\n            continue\n        sa, sc = metrics[a][idx], metrics[c][idx]\n        m = ~np.isnan(sa) & ~np.isnan(sc)\n        if m.sum() < 10 or len(set(y[m])) < 2:\n            continue\n        fa, fc = WStratAuc(y[m], sa[m], st[m]), WStratAuc(y[m], sc[m], st[m])\n        d = np.array([fa(W[b][m]) - fc(W[b][m]) for b in range(B)])\n        pt = strat_auc(y[m], sa[m], st[m]) - strat_auc(y[m], sc[m], st[m])\n        c95 = ci(d)\n        ym, sm_ = y[m], sid[m]\n        ne, nc = int(ym.sum()), int(len(ym) - ym.sum())\n        out[\"deltas\"][f\"{a} - {c}\"] = {\"n\": int(m.sum()), \"n_error\": ne, \"n_correct\": nc,\n                                       \"testable\": bool(ne >= 50 and nc >= 50 and len(set(sm_[ym == 1])) >= 25 and len(set(sm_[ym == 0])) >= 25),\n                                       \"delta\": float(pt), \"ci\": c95, \"p_le0\": float(np.mean(d <= 0)),\n                                       \"ci_gt0\": bool(c95[0] is not None and c95[0] > 0),\n                                       \"pooled_delta\": float(auc(y[m], sa[m]) - auc(y[m], sc[m]))}\n        # sensitivity: frozen pooled sentence-cluster bootstrap (eval-2 SentBoot)\n        sb = SentBoot(sid[m], B, 0)\n        Wp = sb.W()\n        dp = np.array([fa(Wp[b]) - fc(Wp[b]) for b in range(B)])\n        out[\"deltas\"][f\"{a} - {c}\"][\"ci_pooled_cluster_boot\"] = ci(dp)\n    return out", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [33] TOOL CALL — Bash · 2026-09-25 16:44:26 UTC

```
cd /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11 && sed -n 120,200p frozen/eval2/src/stats.py
```

### [34] TOOL RESULT — Bash · 2026-09-25 16:44:26 UTC

```
{"stdout": "        return w if mask is None else w[mask]\n\n    def W(self, mask=None):\n        \"\"\"(B, n_rows[mask]) weight matrix.\"\"\"\n        W = self.C[:, self.sent_ix]\n        return W if mask is None else W[:, mask]", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [35] THINKING · 2026-09-25 16:46:28 UTC

```
I'll now write a builder script to generate the notebook, incorporating the verbatim `method.py` stage table, frozen `stats.py` functions from eval-2, key components from `analyse_E2A.py`, and `audit/rederive.py`, all run against the loaded data.
```

### [36] TOOL CALL — Write · 2026-09-25 16:46:28 UTC

```
File: /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh/scripts/build_notebook.py

"""Generate code_demo.ipynb from the cell list below (markdown / code). Usage: python scripts/build_notebook.py"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parents[1] / "code_demo.ipynb"
cells = []
md = lambda s: cells.append(("markdown", s.strip("\n")))
code = lambda s: cells.append(("code", s.strip("\n"... [truncated, 32883 chars total]
```

### [37] TOOL RESULT — Write · 2026-09-25 16:46:28 UTC

```
{"type": "create", "filePath": "/ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh/scripts/build_notebook.py", "content": "\"\"\"Generate code_demo.ipynb from the cell list below (markdown / code). Usage: python scripts/build_notebook.py\"\"\"\nimport json\nfrom pathlib import Path\n\nOUT = Path(__file__).resolve().parents[1] / \"code_demo.ipynb\"\ncells = []\nmd = lambda s: cells.append((\"markdown\", s.st... [truncated, 34811 chars total]
```

### [38] ASSISTANT · 2026-09-25 16:46:38 UTC

```
The builder is written. Following TODO 4, I'll first test at the absolute minimum config (B=10, N_PLACEBO=5) in the clean test venv.
```

### [39] TOOL CALL — Bash · 2026-09-25 16:46:38 UTC

```
sed -i 's/^B = 200 /B = 10  /; s/^N_PLACEBO = 50 /N_PLACEBO = 5  /' scripts/build_notebook.py && grep -n "^B = \|^N_PLACEBO" scripts/build_notebook.py && python3 scripts/build_notebook.py && \
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-a1a05088362b && \
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-a1a05088362b/bin/python jupyter ipykernel && \
start=$(date +%s); /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-a1a05088362b/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -20; echo "runtime $(( $(date +%s)-start ))s"
```

### [40] TOOL RESULT — Bash · 2026-09-25 16:47:10 UTC

```
{"stdout": "112:B = 10             # stratified sentence-cluster bootstrap replicates   (original: B = 2000)\n113:N_PLACEBO = 5      # shuffled-label placebo replicates                   (original: 200)\nwrote /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh/code_demo.ipynb (27 cells)\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 219795 bytes to code_demo.ipynb\nruntime 27s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [41] ASSISTANT · 2026-09-25 16:47:14 UTC

```
The minimum-config run passes in 27s. Next I'll check the text outputs for sanity.
```

### [42] TOOL CALL — Bash · 2026-09-25 16:47:14 UTC

```
python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    if c['cell_type']!='code': continue
    for o in c['outputs']:
        if o.get('output_type')=='stream': print(''.join(o['text'])[:3500]); print('-----')
        elif o.get('output_type')=='error': print('ERR', o['ename'], o['evalue'])
        else: print('[', o.get('output_type'), list(o.get('data',{}).keys()), ']')
"
```

### [43] TOOL RESULT — Bash · 2026-09-25 16:47:14 UTC

```
{"stdout": "E2-A NL->FOL meta-evaluation subset: labelled LLM candidate formalizations (R_AB regime: tier A/B prover-built or audited labels, no reading-choice rows) from the 110-sentence random prefix. Every score is label-free, sealed BEFORE labels, and oriented higher = more likely ERROR.\n93 labelled candidate rows from 11 sentences; 181 rename-control rows\n\n-----\n== l3                     scoring/score_consensus.py --stage l3\n== consensus              scoring/score_consensus.py --stage score --workers 30\n== pairwise               scoring/score_consensus.py --stage pairwise --workers 36\n== exact                  scoring/score_consensus.py --stage exact --workers 36\n== prep                   scoring/api_judges.py --stage prep --workers 10\n== judges                 scoring/api_judges.py --stage judges --concurrency 32\n== local_judge            scoring/local_judge.py --which qwen8b_disg,qwen8b_orig --bs 64\n== pilot                  scoring/pilot_metrics_E2.py\n== assemble               scoring/assemble_scores.py\n== labels:assemble_e2     src_e2/assemble_e2.py\n== labels:controls_e2     src_e2/controls_e2.py\n== labels:testability_e2  src_e2/testability_e2.py\n== labels:seal_e2         src_e2/seal_e2.py\n== labels:verify_seal     src_e2/verify_seal.py\n== join                   analysis/analyse_E2A.py --stage join\n== analyse                analysis/analyse_E2A.py --stage analyse --prefix 110\n== rename                 analysis/rename_V0.py\n== union                  analysis/union_E2B.py --deadline-utc 2026-09-24T15:40:00Z --once\n== outputs                analysis/make_outputs.py\n\n-----\nlabel    CORRECT  ERROR\nstratum                \nDT            35     15\nEXC            7     12\nL25            7     17\n\nOne sentence per row:\nstratum  words  n_conditions                                                                                                                                                                          text\n     DT     19             2                                                          If Heaven either builds a strong community or fosters local economies (but not both), then she drives social change.\n    EXC     15             3                                                                                  A smartphone is considered waterproof if it can be submerged in water without being damaged.\n    L25     28             5                                A musical instrument that has strings, is played with a bow, and can be held between the chin and shoulder is a violin if it has four strings.\n     DT     15             2                                                                                   If Cruz either follows traditions or obeys authority (but not both), then he respects laws.\n    EXC     19             3                                                        A natural resource that is replenished over time and can be used repeatedly without depletion is a renewable resource.\n    L25     26             4              A person is considered a baker if they prepare and produce baked goods, often in a bakery or other commercial setting, using various ingredients and techniques.\n     DT     17             2                                                                If Callahan either experiences fatigue or requires medication (but not both), then he has a chronic condition.\n    L25     30             5 An electronic device that captures and stores images, typically using a lens and a sensor, and can be used for photography or videography is a digital camera or a camcorder.\n     DT     19             2                                                                         If Xiomara either wakes up at dawn or has light slumber (but not both), then she sleeps very lightly.\n     DT     17             2                                                                                   If Mary either reads novels or listens to music (but not both), then she enjoys alone time.\n     DT     18             2                                                             If Uriah is either environmentally negligent or cares about wildlife (but not both), then he makes green choices.\n\nAll candidates of the first sentence (V0 = c_score_align):\n                                     system   label  c_score_align  judge_local_qwen8b_disg                                                                                        candidate_fol\n      G1b:meta-llama/llama-3.3-70b-instruct CORRECT       0.375000                     0.05   (Builds(heaven, strongCommunity) ⊕ Fosters(heaven, localEconomies)) → Drives(heaven, socialChange)\n               G2:qwen/qwen3-235b-a22b-2507 CORRECT       0.250000                     0.00       ((BuildsStrongCommunity(heaven) ⊕ FostersLocalEconomies(heaven)) → DrivesSocialChange(heaven))\nG3:mistralai/mistral-small-3.2-24b-instruct CORRECT       0.625000                     0.00   (HeavenBuildsStrongCommunity(heaven) ⊕ FostersLocalEconomies(heaven)) → DrivesSocialChange(heaven)\n                  G4:deepseek/deepseek-v3.2 CORRECT       0.375000                     0.\n-----\nanalyse: 0.1s with B=10\nLONG (L25+EXC)   n= 43 (ERR 29 / COR 14; 5 sentences)  testable=False\nL25              n= 24 (ERR 17 / COR  7; 3 sentences)  testable=False\nEXC              n= 19 (ERR 12 / COR  7; 2 sentences)  testable=False\nDT               n= 50 (ERR 15 / COR 35; 6 sentences)  testable=False\nALL              n= 93 (ERR 44 / COR 49; 11 sentences)  testable=False\n\n-----\nWithin-stratum AUROC (higher = better at ranking ERROR above CORRECT; 0.5 = no signal) with 95% stratified cluster-bootstrap CI\n                                         metric               ALL                DT    LONG (L25+EXC)\n            V0 c_score_align (frozen consensus) 0.786 [0.67,0.89] 0.855 [0.71,1.00] 0.606 [0.53,0.66]\n                 PT p_peer_text (frozen fusion) 0.798 [0.69,0.94] 0.846 [0.71,1.00] 0.675 [0.65,0.87]\n                           c_exact (no aligner) 0.777 [0.74,0.84] 0.838 [0.78,0.90] 0.618 [0.50,0.76]\n                                 ALIGN graded g 0.851 [0.79,0.89] 0.932 [0.91,0.98] 0.640 [0.51,0.78]\n                             L2-bow (text side) 0.701 [0.67,0.76] 0.722 [0.70,0.76] 0.648 [0.62,0.82]\n                                 L3 (text side) 0.495 [0.45,0.54] 0.447 [0.39,0.53] 0.618 [0.53,0.69]\n                        V1 plurality-normalised 0.834 [0.77,0.90] 0.916 [0.84,1.00] 0.623 [0.57,0.70]\n                        V2 reliability-weighted 0.792 [0.68,0.89] 0.863 [0.73,1.00] 0.608 [0.53,0.66]\n                                     V3 = V1+V2 0.832 [0.77,0.90] 0.914 [0.84,1.00] 0.618 [0.57,0.70]\n                                 V4 two-channel 0.852 [0.83,0.91] 0.939 [0.91,1.00] 0.626 [0.60,0.75]\n                                      V5 3-pool 0.829 [0.74,0.91] 0.903 [0.80,1.00] 0.633 [0.57,0.70]\n                      local Qwen3-8B, disguised 0.783 [0.68,0.88] 0.840 [0.71,0.93] 0.635 [0.61,0.82]\n                       local Qwen3-8B, original 0.845 [0.77,0.95] 0.905 [0.82,0.98] 0.690 [0.67,0.99]\n         pilot m1 joint-load conflict (adapted) 0.500 [0.50,0.50] 0.500 [0.50,0.50] 0.500 [0.50,0.50]\n                   pilot m2 arity inconsistency 0.500 [0.50,0.50] 0.500 [0.50,0.50] 0.500 [0.50,0.50]\n                   pilot m2 shape inconsistency 0.469 [0.45,0.49] 0.457 [0.43,0.49] 0.500 [0.50,0.50]\n                      pilot m3 dangling symbols 0.478 [0.42,0.53] 0.396 [0.30,0.46] 0.690 [0.55,0.72]\npilot m5 1 - rerun Jaccard (cross-system proxy) 0.585 [0.52,0.68] 0.589 [0.52,0.72] 0.576 [0.50,0.82]\n\nPaired deltas (strat AUROC of A minus B), stratified-bootstrap CI and pooled-bootstrap CI:\n  ALL             c_score_align - judge_local_qwen8b_disg       +0.003  CI [-0.023,+0.051]  pooled-CI [-0.055,+0.048]  testable=False\n  ALL             c_score_align - judge_local_qwen8b_orig       -0.059  CI [-0.107,-0.008]  pooled-CI [-0.137,+0.002]  testable=False\n  ALL             p_peer_text - judge_local_qwen8b_disg         +0.015  CI [+0.005,+0.081]  pooled-CI [-0.041,+0.056]  testable=False\n  ALL             c_exact - c_score_align                       -0.009  CI [-0.113,+0.094]  pooled-CI [-0.079,+0.085]  testable=False\n  ALL             c_pn - c_score_align                          +0.049  CI [+0.001,+0.096]  pooled-CI [+0.004,+0.093]  testable=False\n  ALL             c_v5 - c_score_align                          +0.041  CI [-0.007,+0.064]  pooled-CI [+0.018,+0.075]  testable=False\n  DT              c_score_align - judge_local_qwen8b_disg       +0.015  CI [-0.016,+0.090]  pooled-CI [-0.016,+0.090]  testable=False\n  DT              c_score_align - judge_local_qwen8b_orig       -0.050  CI [-0.109,+0.034]  pooled-CI [-0.109,+0.034]  testable=False\n  DT              p_peer_text - judge_local_qwen8b_disg         +0.006  CI [-0.024,+0.089]  pooled-CI [-0.024,+0.089]  testable=False\n  DT              c_exact - c_score_align                       -0.017  CI [-0.140,+0.153]  pooled-CI [-0.140,+0.153]  testable=False\n  \n-----\nALL   n= 93  V0 0.7857 (|diff| vs cell_eval 1.1e-16)  local 0.7830  delta +0.0027\nDT    n= 50  V0 0.8552 (|diff| vs cell_eval 1.1e-16)  local 0.8400  delta +0.0152\nLONG  n= 43  V0 0.6059 (|diff| vs cell_eval 1.1e-16)  local 0.6355  delta -0.0296\n\n-----\n{\n \"V0_mean\": 0.48365384615384616,\n \"V0_p2.5_97.5\": [\n  0.39539835164835163,\n  0.5466346153846153\n ],\n \"delta_mean\": 0.007967032967032972,\n \"delta_p2.5_97.5\": [\n  -0.06943681318681315,\n  0.09711538461538459\n ],\n \"real_V0_ALL_above_placebo_p97.5\": true\n}\n\n-----\nRENAME_SYN {'n': 36, 'FA': 0.9444444444444444, 'base': 0.3611111111111111}\nRENAME_NONCE {'n': 145, 'FA': 1.0, 'base': 0.2620689655172414}\n\n-----\nDEMO SUBSET (93 rows, 11 sentences):\n                    quantity   ALL    DT   LONG\n              V0 strat AUROC 0.786 0.855  0.606\nlocal Qwen3-8B judge (disg.) 0.783 0.840  0.635\n            delta V0 - judge 0.003 0.015 -0.030\n      pilot m5 rerun-Jaccard 0.585 0.589  0.576\n           pilot m3 dangling 0.478 0.396  0.690\n\nFULL RUN (audit/rederive_out.json; ALL n=273, DT n=179, LONG n=94):\n                    quantity    ALL    DT   LONG\n              V0 strat AUROC  0.890 0.916  0.603\nlocal Qwen3-8B judge (disg.)  0.895 0.913  0.695\n            delta V0 - judge -0.005 0.003 -0.091\n      pilot m5 rerun-Jaccard  0.713 0.729  0.533\n           pilot m3 dangling  0.413 0.400  0.564\n\nRename FA: demo SYN 0.94 / NONCE 1.00   full SYN 0.94 / NONCE 1.00\nFull-run placebo V0 mean 0.497; drift-gate panel agreement 0.9554; API spend $2.05\n\n-----\n[ display_data ['image/png', 'text/plain'] ]", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [44] THINKING · 2026-09-25 16:47:24 UTC

```
All cells run cleanly and the audit path matches `cell_eval` exactly, with "dangling" hitting 0.69 on the LONG subset (noisy, 5 sentences) and V1/V4 outperforming V0. Next I'll check the figure and revise the concluding markdown to avoid overclaiming.
```

### [45] TOOL CALL — Bash · 2026-09-25 16:47:24 UTC

```
mkdir -p /tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-ngTPhaVyXxhh/65df35fc-9bf6-4746-8bcc-acfc19dbbf7c/scratchpad && python3 -c "
import json,base64
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    for o in c.get('outputs',[]):
        if 'image/png' in o.get('data',{}): open('/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-ngTPhaVyXxhh/65df35fc-9bf6-4746-8bcc-acfc19dbbf7c/scratchpad/fig.png','wb').write(base64.b64decode(o['data']['image/png']))
"
```

### [46] TOOL RESULT — Bash · 2026-09-25 16:47:24 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [47] TOOL CALL — Read · 2026-09-25 16:47:26 UTC

```
/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-ngTPhaVyXxhh/65df35fc-9bf6-4746-8bcc-acfc19dbbf7c/scratchpad/fig.png
```

### [48] TOOL RESULT — Read · 2026-09-25 16:47:26 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [49] ASSISTANT · 2026-09-25 16:47:44 UTC

```
The figure renders. The middle panel's tick labels overlap, so I'll fix those and rewrite the conclusion to match the subset's numbers. Then I'll scale to B=200 / N_PLACEBO=50.
```

### [50] TOOL CALL — Bash · 2026-09-25 16:47:44 UTC

```
python3 - <<'EOF'
from pathlib import Path
p = Path("scripts/build_notebook.py"); s = p.read_text()
s = s.replace('labs.append(f"{st}\\n{lab[:3]} (n={len(v)})")', 'labs.append(f"{st}\\n{lab[:3]}\\nn={len(v)}")')
s = s.replace('"width_ratios": [2.2, 1.3, 1]', '"width_ratios": [2.2, 1.5, 1]')
s = s.replace('^B = 10 ', '')
old_start = s.index('**Reading the results.**')
old_end = s.index('""")', old_start)
s = s[:old_start] + '''**Reading the results.** The demo subset reproduces the full run's qualitative picture:

* **Consensus works on short sentences, much less on long ones.** V0 and its variants rank ERROR above CORRECT well on `DT`
  (≈0.84–0.94) but drop to ≈0.6 on the long `L25`/`EXC` pool. There, correct but idiosyncratic long formalizations disagree
  with their peers and get flagged (see the `L25 COR` box at V0 = 1.0).
* **Consensus ties a cheap judge.** V0 − local Qwen3-8B (disguised) is ≈0 and its CI includes 0 — same as the full run
  (DT +0.003, ALL −0.005).
* **The user's pilot structural metrics do not track correctness.** Joint-load conflict and arity/shape inconsistency sit at
  ≈0.5 in every cell. Dangling symbols is ≤0.5 on DT/ALL (inverted); its 0.69 on the long cell here rests on 5 sentences, and the
  full run gives 0.56. Rerun-Jaccard carries some signal only because it is itself a lexical cross-system agreement proxy.
* **V0 is not rename-invariant:** renaming the predicates of a correct formula gets it flagged 94% (synonym) / 100% (nonce) of
  the time. These are the full 181 controls, so the numbers equal the full run.
* The subset has only 11 sentences, so CIs are wide and point estimates differ from the full run (◆ / second table: 273 rows,
  110 sentences). For example, V1/V4 edge above V0 here, while in the full run no variant cleared the freeze gate. No cell passes
  the pre-registered testability bar, and the long cell stays **not testable** in the full run too.
''' + s[old_end:]
p.write_text(s)
EOF
sed -i 's/^B = 10  /B = 200 /; s/^N_PLACEBO = 5  /N_PLACEBO = 50 /' scripts/build_notebook.py && grep -n "^B = \|^N_PLACEBO\|nn={len" scripts/build_notebook.py && python3 scripts/build_notebook.py && \
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-a1a05088362b && \
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-a1a05088362b/bin/python jupyter ipykernel && \
start=$(date +%s); /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-a1a05088362b/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | grep -v WARNING | tail -5; echo "runtime $(( $(date +%s)-start ))s"; python3 -c "
import json
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    for o in c.get('outputs',[]):
        t=''.join(o.get('text',''))
        if o.get('output_type')=='error': print('ERR',o['ename'],o['evalue'])
        if 'analyse:' in t or 'V0_mean' in t: print(t[:600])
"
```

### [51] TOOL RESULT — Bash · 2026-09-25 16:48:12 UTC

```
{"stdout": "112:B = 200            # stratified sentence-cluster bootstrap replicates   (original: B = 2000)\n113:N_PLACEBO = 50     # shuffled-label placebo replicates                   (original: 200)\n585:        data_b.append(v); pos.append(j * 3 + k); labs.append(f\"{st}\\n{lab[:3]}\\nn={len(v)}\")\nwrote /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh/code_demo.ipynb (27 cells)\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[NbConvertApp] Writing 219397 bytes to code_demo.ipynb\nruntime 27s\nanalyse: 1.2s with B=200\nLONG (L25+EXC)   n= 43 (ERR 29 / COR 14; 5 sentences)  testable=False\nL25              n= 24 (ERR 17 / COR  7; 3 sentences)  testable=False\nEXC              n= 19 (ERR 12 / COR  7; 2 sentences)  testable=False\nDT               n= 50 (ERR 15 / COR 35; 6 sentences)  testable=False\nALL              n= 93 (ERR 44 / COR 49; 11 sentences)  testable=False\n\n{\n \"V0_mean\": 0.5015521978021978,\n \"V0_p2.5_97.5\": [\n  0.3910370879120879,\n  0.6140625000000001\n ],\n \"delta_mean\": 0.005178571428571421,\n \"delta_p2.5_97.5\": [\n  -0.09500343406593408,\n  0.1401614010989011\n ],\n \"real_V0_ALL_above_placebo_p97.5\": true\n}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [52] ASSISTANT · 2026-09-25 16:48:24 UTC

```
At B=200 the analysis takes 1.2s, so the original values (B=2000, 200 placebos) fit easily. Final scaling round:
```

### [53] TOOL CALL — Bash · 2026-09-25 16:48:24 UTC

```
python3 - <<'EOF'
from pathlib import Path
p = Path("scripts/build_notebook.py"); s = p.read_text()
s = s.replace('B = 200            # stratified sentence-cluster bootstrap replicates   (original: B = 2000)',
              'B = 2000           # stratified sentence-cluster bootstrap replicates   (original value; demo tested 10 -> 200 -> 2000)')
s = s.replace('N_PLACEBO = 50     # shuffled-label placebo replicates                   (original: 200)',
              'N_PLACEBO = 200    # shuffled-label placebo replicates                   (original value; demo tested 5 -> 50 -> 200)')
s = s.replace('''All tunable parameters. The original run used `B = 2000` bootstrap replicates (analysis) and `200` shuffled-label placebo
replicates (audit). The demo values below are reduced so the whole notebook finishes in well under a minute; set them back to
the originals for the full-precision run (the analysis is cheap — a few minutes at original values on the full data).''',
'''All tunable parameters. The analysis stage is cheap, so the notebook runs at the **original** values: `B = 2000` bootstrap
replicates (analysis) and `200` shuffled-label placebo replicates (audit), about 15 s in total. Lower them (e.g. `B = 10`,
`N_PLACEBO = 5`) for a quick smoke test.''')
p.write_text(s)
EOF
grep -n "^B = \|^N_PLACEBO" scripts/build_notebook.py && python3 scripts/build_notebook.py && \
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-a1a05088362b && \
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-a1a05088362b/bin/python jupyter ipykernel && \
start=$(date +%s); /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-a1a05088362b/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | grep -v WARNING | tail -5; echo "runtime $(( $(date +%s)-start ))s"; python3 -c "
import json,base64
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    for o in c.get('outputs',[]):
        t=''.join(o.get('text',''))
        if o.get('output_type')=='error': print('ERR',o['ename'],o['evalue'])
        if 'analyse:' in t or 'V0_mean' in t or 'Paired' in t: print(t[:4000])
        if 'image/png' in o.get('data',{}): open('/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-ngTPhaVyXxhh/65df35fc-9bf6-4746-8bcc-acfc19dbbf7c/scratchpad/fig.png','wb').write(base64.b64decode(o['data']['image/png']))
"
```

### [54] TOOL RESULT — Bash · 2026-09-25 16:49:04 UTC

```
{"stdout": "112:B = 2000           # stratified sentence-cluster bootstrap replicates   (original value; demo tested 10 -> 200 -> 2000)\n113:N_PLACEBO = 200    # shuffled-label placebo replicates                   (original value; demo tested 5 -> 50 -> 200)\nwrote /ai-inventor/aii_data/runs/run_An1uy2kF2SjZ/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh/code_demo.ipynb (27 cells)\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[NbConvertApp] Writing 219426 bytes to code_demo.ipynb\nruntime 37s\nanalyse: 11.8s with B=2000\nLONG (L25+EXC)   n= 43 (ERR 29 / COR 14; 5 sentences)  testable=False\nL25              n= 24 (ERR 17 / COR  7; 3 sentences)  testable=False\nEXC              n= 19 (ERR 12 / COR  7; 2 sentences)  testable=False\nDT               n= 50 (ERR 15 / COR 35; 6 sentences)  testable=False\nALL              n= 93 (ERR 44 / COR 49; 11 sentences)  testable=False\n\nWithin-stratum AUROC (higher = better at ranking ERROR above CORRECT; 0.5 = no signal) with 95% stratified cluster-bootstrap CI\n                                         metric               ALL                DT    LONG (L25+EXC)\n            V0 c_score_align (frozen consensus) 0.786 [0.66,0.90] 0.855 [0.68,1.00] 0.606 [0.54,0.66]\n                 PT p_peer_text (frozen fusion) 0.798 [0.69,0.94] 0.846 [0.68,1.00] 0.675 [0.57,0.87]\n                           c_exact (no aligner) 0.777 [0.71,0.84] 0.838 [0.76,0.91] 0.618 [0.50,0.73]\n                                 ALIGN graded g 0.851 [0.78,0.90] 0.932 [0.89,0.97] 0.640 [0.46,0.75]\n                             L2-bow (text side) 0.701 [0.63,0.77] 0.722 [0.63,0.79] 0.648 [0.54,0.80]\n                                 L3 (text side) 0.495 [0.42,0.55] 0.447 [0.36,0.52] 0.618 [0.52,0.70]\n                        V1 plurality-normalised 0.834 [0.77,0.91] 0.916 [0.82,1.00] 0.623 [0.56,0.69]\n                        V2 reliability-weighted 0.792 [0.67,0.90] 0.863 [0.70,1.00] 0.608 [0.54,0.67]\n                                     V3 = V1+V2 0.832 [0.76,0.91] 0.914 [0.82,1.00] 0.618 [0.56,0.69]\n                                 V4 two-channel 0.852 [0.79,0.92] 0.939 [0.86,1.00] 0.626 [0.56,0.73]\n                                      V5 3-pool 0.829 [0.74,0.91] 0.903 [0.77,1.00] 0.633 [0.56,0.70]\n                      local Qwen3-8B, disguised 0.783 [0.69,0.89] 0.840 [0.70,0.95] 0.635 [0.56,0.80]\n                       local Qwen3-8B, original 0.845 [0.76,0.95] 0.905 [0.78,0.99] 0.690 [0.55,0.95]\n         pilot m1 joint-load conflict (adapted) 0.500 [0.50,0.50] 0.500 [0.50,0.50] 0.500 [0.50,0.50]\n                   pilot m2 arity inconsistency 0.500 [0.50,0.50] 0.500 [0.50,0.50] 0.500 [0.50,0.50]\n                   pilot m2 shape inconsistency 0.469 [0.45,0.49] 0.457 [0.43,0.49] 0.500 [0.50,0.50]\n                      pilot m3 dangling symbols 0.478 [0.39,0.54] 0.396 [0.29,0.48] 0.690 [0.53,0.81]\npilot m5 1 - rerun Jaccard (cross-system proxy) 0.585 [0.48,0.70] 0.589 [0.45,0.71] 0.576 [0.48,0.83]\n\nPaired deltas (strat AUROC of A minus B), stratified-bootstrap CI and pooled-bootstrap CI:\n  ALL             c_score_align - judge_local_qwen8b_disg       +0.003  CI [-0.062,+0.060]  pooled-CI [-0.100,+0.075]  testable=False\n  ALL             c_score_align - judge_local_qwen8b_orig       -0.059  CI [-0.150,+0.030]  pooled-CI [-0.198,+0.032]  testable=False\n  ALL             p_peer_text - judge_local_qwen8b_disg         +0.015  CI [-0.047,+0.094]  pooled-CI [-0.057,+0.100]  testable=False\n  ALL             c_exact - c_score_align                       -0.009  CI [-0.136,+0.121]  pooled-CI [-0.144,+0.121]  testable=False\n  ALL             c_pn - c_score_align                          +0.049  CI [+0.000,+0.109]  pooled-CI [+0.000,+0.109]  testable=False\n  ALL             c_v5 - c_score_align                          +0.041  CI [-0.013,+0.079]  pooled-CI [-0.032,+0.084]  testable=False\n  DT              c_score_align - judge_local_qwen8b_disg       +0.015  CI [-0.042,+0.094]  pooled-CI [-0.042,+0.094]  testable=False\n  DT              c_score_align - judge_local_qwen8b_orig       -0.050  CI [-0.119,+0.061]  pooled-CI [-0.119,+0.061]  testable=False\n  DT              p_peer_text - judge_local_qwen8b_disg         +0.006  CI [-0.060,+0.094]  pooled-CI [-0.060,+0.094]  testable=False\n  DT              c_exact - c_score_align                       -0.017  CI [-0.167,+0.147]  pooled-CI [-0.167,+0.147]  testable=False\n  DT              c_pn - c_score_align                          +0.061  CI [+0.000,+0.138]  pooled-CI [+0.000,+0.138]  testable=False\n  DT              c_v5 - c_score_align                          +0.048  CI [+0.000,+0.089]  pooled-CI [+0.000,+0.089]  testable=False\n  LONG (L25+EXC)  c_score_align - judge_local_qwen8b_disg       -0.030  CI [-0.220,+0.027]  pooled-CI [-0.271,+0.098]  testable=False\n  LONG (L25+EXC)  c_score_align - judge_local_qwen8b_orig       -0.084  CI [-0.350,+0.053]  pooled-C\n{\n \"V0_mean\": 0.49916895604395606,\n \"V0_p2.5_97.5\": [\n  0.38033997252747254,\n  0.6073660714285716\n ],\n \"delta_mean\": 0.0022733516483516487,\n \"delta_p2.5_97.5\": [\n  -0.1277815934065934,\n  0.1354223901098902\n ],\n \"real_V0_ALL_above_placebo_p97.5\": true\n}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [55] TOOL CALL — Read · 2026-09-25 16:49:06 UTC

```
/tmp/claude-0/-ai-inventor-aii-data-runs-run-An1uy2kF2SjZ-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-ngTPhaVyXxhh/65df35fc-9bf6-4746-8bcc-acfc19dbbf7c/scratchpad/fig.png
```

### [56] TOOL RESULT — Read · 2026-09-25 16:49:06 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [57] THINKING · 2026-09-25 16:49:12 UTC

```
The notebook runs cleanly in 37s at the original settings (B=2000, 200 placebos) with a clean figure. Next I'll run the TODO 6 checks, then write the README, manifest, and structured output.
```

### [58] TOOL CALL — Bash · 2026-09-25 16:49:12 UTC

```
grep -c 'GITHUB_DATA_URL = \\"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_An1uy2kF2SjZ/round-5/experiment-11/demo/mini_demo_data.json\\"' code_demo.ipynb; grep -c "urllib.request.urlopen(GITHUB_DATA_URL)" code_demo.ipynb; ls -la; du -sh .; find . -size +10M
```

### [59] TOOL RESULT — Bash · 2026-09-25 16:49:12 UTC

```
{"stdout": "1\n1\ntotal 4692\ndrwxr-xr-x 4 root root 1074339 Sep 25 16:46 .\ndrwxr-xr-x 7 root root 2000333 Sep 25 16:46 ..\ndrwxr-xr-x 2 root root       1 Sep 25 16:42 .aii\n-rw------- 1 root root      54 Sep 25 16:42 .aii_claude_session.json\n-rw-r--r-- 1 root root  364390 Sep 25 16:49 .repl_agent.ptylog\n-rw-r--r-- 1 root root  219531 Sep 25 16:49 code_demo.ipynb\n-rw-r--r-- 1 root root  143195 Sep 25 16:44 mini_demo_data.json\ndrwxr-xr-x 2 root root 1003648 Sep 25 16:47 scripts\n2.8M\t.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [60] ASSISTANT · 2026-09-25 16:49:26 UTC

```
All three checks pass, and nothing in the workspace is over 10 MB. Next I'll write the manifest, README and structured output.
```

### [61] TOOL CALL — Bash · 2026-09-25 16:49:26 UTC

````
cat > .aii/manifest.yaml <<'EOF'
# No heavy paths: every file in this workspace is small text/code (< 1 MB). No venv, cache or checkpoint lives here
# (the notebook test venv is on local disk outside the workspace and is removed by the pipeline).
entries: []
EOF
cat > README.md <<'EOF'
# Consensus vs LLM judges on fresh logic data (E2-A) — demo notebook

A runnable, annotated demo of the E2-A experiment. That experiment is the pre-registered confirmation test of the frozen
cross-family solver-consensus score **V0 = `c_score_align`** as a gold-free predictor of whether an NL→FOL formalization is
faithful to its sentence. It compares V0 against a local Qwen3-8B LLM judge, text-side checks, consensus variants V1–V5 and
the user's pilot structural metrics.

The original `method.py` is a stage orchestrator. Its stages need paid API calls, a GPU judge and private virtualenvs, so the
notebook lists them as a dry run and loads their **sealed outputs** (label-free scores + prover-built labels). It then re-runs
the meta-evaluation code itself on a curated subset:
- `analysis/analyse_E2A.py`: `Data`, `strat_boot_weights`, `cell_eval`;
- the frozen eval-2 `stats.py`: within-stratum AUROC and bootstrap classes;
- `audit/rederive.py`: the independent sklearn re-derivation, the shuffled-label placebo and the rename-invariance controls.

The subset is 93 labelled candidates from 11 whole sentences, balanced over the DT / L25 / EXC strata. The full-run reference
numbers (273 rows, 110 sentences) are shipped alongside for comparison.

## Layout
| path | what |
|---|---|
| `code_demo.ipynb` | the demo notebook (loads data from GitHub, falls back to the local file); ~40 s end to end at the original B = 2000 |
| `mini_demo_data.json` | 93 candidate rows (text, candidate FOL, label, all sealed scores), 181 rename-control rows, full-run reference numbers |
| `scripts/build_mini_demo_data.py` | builds `mini_demo_data.json` from the artifact's `per_item_E2A.jsonl`, `e2/candidates_E2_nolabels.jsonl`, `results/rename_V0_rows.jsonl`, `audit/rederive_out.json` |
| `scripts/build_notebook.py` | generates `code_demo.ipynb` (cell sources) |

## Run
```bash
pip install jupyter
jupyter nbconvert --to notebook --execute code_demo.ipynb --output code_demo.ipynb   # or open it in Colab / Jupyter
```
The first code cell installs numpy / pandas / scikit-learn / scipy / matplotlib at Colab's versions when not on Colab.
To rebuild the data or notebook: `python scripts/build_mini_demo_data.py <path-to-E2-A-artifact>` and
`python scripts/build_notebook.py`.

## Restoring removed files
Nothing is marked for deletion (`.aii/manifest.yaml` has no entries); every file here is small text and is kept.
EOF
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
python3 -c "import json,yaml;json.load(open('.terminal_claude_agent_struct_out.json'));print(yaml.safe_load(open('.aii/manifest.yaml')))"
````

### [62] TOOL RESULT — Bash · 2026-09-25 16:49:26 UTC

```
{"stdout": "{'entries': []}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [63] ASSISTANT · 2026-09-25 16:49:36 UTC

```
I built `code_demo.ipynb` and `mini_demo_data.json`. The notebook runs cleanly in the Colab-like test venv in about 37 seconds (the limit is 600) with the original settings: 2,000 bootstrap replicates and 200 placebo shuffles.

**What the notebook can and can't run.** The artifact's `method.py` only starts other scripts one after another. Those scripts need paid API calls, a GPU judge, private virtualenvs and about 35k lines of frozen solver code, so they can't run in Colab. The notebook therefore:
- **Lists `method.py`'s stages** without running them.
- **Loads the saved outputs**: the precomputed scores and correctness labels.
- **Runs the evaluation code, copied unchanged**: the AUROC and bootstrap functions from the frozen `stats.py`, the analysis helpers from `analysis/analyse_E2A.py`, and the independent re-check from `audit/rederive.py` (placebo and rename tests included).

The only edits are to file paths, and I dropped two extra label subsets that need flags the demo data doesn't carry.

**The demo data.** 93 labelled candidate formulas from 11 whole sentences, balanced across the short (DT) and long (L25/EXC) sentence groups. It also includes all 181 renaming checks and the full run's reference numbers.

**Results on the subset.** Same overall picture as the full run, but less precise with only 11 sentences:

| | Subset (93 rows) | Full run (273 rows) |
|---|---|---|
| V0, all sentences | 0.786 | 0.890 |
| V0, short sentences (DT) | 0.855 | 0.916 |
| V0, long sentences | 0.606 | 0.603 |
| V0 minus local Qwen3-8B judge, all | +0.003 | −0.005 |
| Share of renamed correct formulas flagged (synonym / nonce) | 94% / 100% | 94% / 100% |

- **Two code paths agree:** the notebook's rerun of the independent check matches the analysis code to within 1e-16.
- **Pilot metrics:** your structural metrics stay at about 0.5 AUROC, meaning no signal.
- **Where the subset differs:** two consensus variants (V1, V4) score slightly above V0 here, while none beat it in the full run. The notebook's closing notes call this out so the subset isn't read as the headline result.

**Before relying on the notebook:**
- **GitHub link not live yet.** The data URL is in the notebook exactly as specified, but it only works once the files are pushed. Until then the notebook falls back to the local `mini_demo_data.json`, which is how it ran here.
- **No todo list.** No todo-tracking tool was available in this session, so I didn't create one, but I did all six steps.

`.aii/manifest.yaml` has no entries because nothing in the workspace is large. The README gives the layout, how to run it, and a "Restoring removed files" section that says nothing needs restoring.

Files are in the workspace:
- `code_demo.ipynb`
- `mini_demo_data.json`
- `README.md`
- `.aii/manifest.yaml`
- `.terminal_claude_agent_struct_out.json`
- `scripts/build_mini_demo_data.py`
- `scripts/build_notebook.py`
```
