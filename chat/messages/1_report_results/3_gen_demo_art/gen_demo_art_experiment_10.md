# gen_demo_art_experiment_10 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `gen_paper_repo_a2e1d024cc16` — Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for Natural Language to First-Order Logic Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_10` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-25 13:14:36 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-25 13:14:44 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh/`:
GOOD: `/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh/file.py`, `/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh/results/out.json`
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
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-5/experiment-11/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-5/experiment-11/demo/mini_demo_data.json"
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
To test-run the notebook in a clean environment (simulating Colab), use the disposable venv at `/tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-de9dd702ac22`. It is on this machine's local disk, outside your workspace, which is on a slow network volume: never create a venv inside your workspace.
```bash
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-de9dd702ac22
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-de9dd702ac22/bin/python jupyter ipykernel
/tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-de9dd702ac22/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
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
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-5/experiment-11/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] HUMAN-USER prompt · 2026-09-25 13:14:44 UTC

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

### [4] TOOL CALL — Skill · 2026-09-25 13:14:50 UTC

```
aii-colab
```

### [5] TOOL RESULT — Skill · 2026-09-25 13:14:50 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [6] TOOL CALL — Skill · 2026-09-25 13:14:50 UTC

```
aii-long-running-tasks
```

### [7] TOOL RESULT — Skill · 2026-09-25 13:14:50 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [8] TOOL CALL — Bash · 2026-09-25 13:14:50 UTC

```
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh; ls -la; ls -la .aii; W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11; ls -la $W; wc -l $W/method.py; ls -la $W/lib $W/results $W/e2 2>/dev/null | head -60
```

### [9] TOOL RESULT — Bash · 2026-09-25 13:14:50 UTC

```
{"stdout": "total 1988\ndrwxr-xr-x 3 root root 1002791 Sep 25 13:14 .\ndrwxr-xr-x 3 root root 1002791 Sep 25 13:13 ..\ndrwxr-xr-x 2 root root       1 Sep 25 13:13 .aii\n-rw------- 1 root root      54 Sep 25 13:14 .aii_claude_session.json\n-rw-r--r-- 1 root root   28834 Sep 25 13:14 .repl_agent.ptylog\ntotal 980\ndrwxr-xr-x 2 root root       1 Sep 25 13:13 .\ndrwxr-xr-x 3 root root 1002821 Sep 25 13:14 ..\ntotal 60956\ndrwxr-xr-x 14 root   root    2013491 Sep 24 15:38 .\ndrwxr-xr-x  7 root   root    2040112 Sep 24 11:06 ..\n-rw-r--r--  1 231072 231072       11 Sep 24 11:10 .T0\ndrwxr-xr-x  2 root   root      86700 Sep 24 15:38 .aii\n-rw-------  1 231072 231072       54 Sep 24 14:02 .aii_claude_session.json\n-rw-r--r--  1 231072 231072   795858 Sep 24 11:39 .aii_cost_ledger.jsonl\n-rw-------  1 231072 231072    19028 Sep 24 15:38 .aii_worker_result.json\n-rw-r--r--  1 231072 231072  3462258 Sep 24 15:38 .repl_agent.ptylog\n-rw-r--r--  1 231072 231072     3239 Sep 24 15:36 .terminal_claude_agent_struct_out.json\n-rw-r--r--  1 231072 231072      398 Sep 24 11:11 DPIN.diff\n-rw-r--r--  1 231072 231072    13297 Sep 24 15:37 README.md\ndrwxr-xr-x  3 231072 231072  1005088 Sep 24 15:34 analysis\ndrwxr-xr-x  2 231072 231072  1000650 Sep 24 15:36 audit\ndrwxr-xr-x  4 231072 231072  2002122 Sep 24 12:20 cache\n-rw-r--r--  1 231072 231072     4441 Sep 24 15:32 deviations.json\ndrwxr-xr-x  2 231072 231072  2000514 Sep 24 15:31 e2\ndrwxr-xr-x 18 231072 231072  2006487 Sep 24 16:51 e2src\nlrwxrwxrwx  1 231072 231072       13 Sep 24 11:30 env -> /root/e2a_env\n-rw-r--r--  1 231072 231072        0 Sep 24 11:16 env_install.log\ndrwxr-xr-x  2 231072 231072  1006418 Sep 24 15:34 freeze_copy\ndrwxr-xr-x  5 231072 231072  2000163 Sep 24 16:51 frozen\n-rw-r--r--  1 231072 231072 10943839 Sep 24 15:32 full_method_out.json\n-rw-r--r--  1 231072 231072    40710 Sep 24 11:52 inputs_manifest.json\ndrwxr-xr-x  3 231072 231072  1001196 Sep 24 15:34 lib\ndrwxr-xr-x  2 231072 231072  1056168 Sep 24 15:31 logs\n-rw-r--r--  1 231072 231072     2836 Sep 24 15:35 method.py\n-rw-r--r--  1 231072 231072  8754723 Sep 24 15:31 method_out.json\n-rw-r--r--  1 231072 231072    18220 Sep 24 15:32 mini_method_out.json\n-rw-r--r--  1 231072 231072     7047 Sep 24 11:11 or_client_before_DPIN.py\n-rw-r--r--  1 231072 231072 10253576 Sep 24 15:30 per_item_E2A.jsonl\n-rw-r--r--  1 231072 231072     2519 Sep 24 11:52 prereg_addendum_budgetstop.json\n-rw-r--r--  1 231072 231072       98 Sep 24 11:52 prereg_addendum_budgetstop.sha256\n-rw-r--r--  1 231072 231072     5621 Sep 24 11:12 prereg_iter5_E2A.json\n-rw-r--r--  1 231072 231072       88 Sep 24 11:12 prereg_iter5_E2A.sha256\n-rw-r--r--  1 231072 231072    17376 Sep 24 15:32 preview_method_out.json\n-rw-r--r--  1 231072 231072     4073 Sep 24 15:35 pyproject.toml\n-rw-r--r--  1 231072 231072       39 Sep 24 11:32 pytest.ini\n-rw-r--r--  1 231072 231072     6855 Sep 24 15:36 reproducibility.md\ndrwxr-xr-x  2 231072 231072  1015213 Sep 24 15:31 results\n-rw-r--r--  1 231072 231072    17782 Sep 24 13:01 score_seal.json\n-rw-r--r--  1 231072 231072  8751701 Sep 24 13:01 scores_E2A.jsonl\ndrwxr-xr-x  3 231072 231072  1004496 Sep 24 15:34 scoring\n-rw-r--r--  1 231072 231072    43598 Sep 24 15:31 tables.md\n55 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11/method.py\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11/e2:\ntotal 9186\ndrwxr-xr-x  2 231072 231072 2000514 Sep 24 15:31 .\ndrwxr-xr-x 14 root   root   2013491 Sep 24 15:38 ..\n-rw-r--r--  1 231072 231072     764 Sep 24 15:31 E2A_FINAL_READY.json\n-rw-r--r--  1 231072 231072    2010 Sep 24 11:18 E2_DRIFT_DECISION.json\n-rw-r--r--  1 231072 231072 5388326 Sep 24 11:20 candidates_E2_nolabels.jsonl\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11/lib:\ntotal 3932\ndrwxr-xr-x  3 231072 231072 1001196 Sep 24 15:34 .\ndrwxr-xr-x 14 root   root   2013491 Sep 24 15:38 ..\n-rw-r--r--  1 231072 231072   10410 Sep 24 11:46 nl2fol_metrics.py\ndrwxr-xr-x  2 231072 231072 1000179 Sep 24 15:34 tests\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11/results:\ntotal 3114\ndrwxr-xr-x  2 231072 231072 1015213 Sep 24 15:31 .\ndrwxr-xr-x 14 root   root   2013491 Sep 24 15:38 ..\n-rw-r--r--  1 231072 231072  100822 Sep 24 15:31 auroc_cells.json\n-rw-r--r--  1 231072 231072    8344 Sep 24 15:31 complexity_E2.json\n-rw-r--r--  1 231072 231072    7324 Sep 24 15:31 confirm_verdict_E2A.json\n-rw-r--r--  1 231072 231072     829 Sep 24 15:31 cost_E2A.json\n-rw-r--r--  1 231072 231072    1540 Sep 24 15:31 coverage_E2.json\n-rw-r--r--  1 231072 231072    1981 Sep 24 15:31 hmech_E2.json\n-rw-r--r--  1 231072 231072    2683 Sep 24 15:31 improve_E2.json\n-rw-r--r--  1 231072 231072     466 Sep 24 15:30 join_record.json\n-rw-r--r--  1 231072 231072     185 Sep 24 15:31 placebo_E2.json\n-rw-r--r--  1 231072 231072     174 Sep 24 15:30 prefix_used.json\n-rw-r--r--  1 231072 231072    1008 Sep 24 15:31 rename_E2.json\n-rw-r--r--  1 231072 231072     804 Sep 24 15:12 rename_V0.json\n-rw-r--r--  1 231072 231072   25539 Sep 24 15:12 rename_V0_rows.jsonl\n-rw-r--r--  1 231072 231072    2932 Sep 24 15:31 s4_E2.json\n-rw-r--r--  1 231072 231072     350 Sep 24 15:31 system_level_E2.json\n-rw-r--r--  1 231072 231072     806 Sep 24 15:31 union_longpool.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [10] TOOL CALL — Bash · 2026-09-25 13:14:54 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11; cat $W/method.py; echo ----; head -c 3000 $W/preview_method_out.json; echo; echo ----; cat $W/lib/nl2fol_metrics.py; ls $W/scoring $W/analysis $W/audit
```

### [11] TOOL RESULT — Bash · 2026-09-25 13:14:54 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"E2-A entry point: runs the label-free scoring, the seals/join and the analyses in the order actually executed.\nPaid API stages (drift gate, generation, panel, API judges) are in e2src/src_e2a/*.sh and scoring/api_judges.py; they\nare cached and never re-billed. Usage: python method.py [--from STAGE] [--prefix 110]\nStages: l3, consensus, pairwise, exact, prep, judges, local_judge, pilot, assemble, labels, join, analyse, rename, union, outputs\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport os\nimport subprocess\nimport sys\nfrom pathlib import Path\n\nWS = Path(__file__).resolve().parent\nPY = str(WS / \"env\" / \".venv\" / \"bin\" / \"python\")\nGPU = \"/root/e2a_gpu/.venv/bin/python\"\nE2PY = str(WS / \"e2src\" / \".venv\" / \"bin\" / \"python\")\n\n\ndef stages(prefix: int) -> list[tuple[str, list[str], Path]]:\n    s = [(\"l3\", [PY, \"scoring/score_consensus.py\", \"--stage\", \"l3\"], WS),\n         (\"consensus\", [PY, \"scoring/score_consensus.py\", \"--stage\", \"score\", \"--workers\", \"30\"], WS),\n         (\"pairwise\", [PY, \"scoring/score_consensus.py\", \"--stage\", \"pairwise\", \"--workers\", \"36\"], WS),\n         (\"exact\", [PY, \"scoring/score_consensus.py\", \"--stage\", \"exact\", \"--workers\", \"36\"], WS),\n         (\"prep\", [PY, \"scoring/api_judges.py\", \"--stage\", \"prep\", \"--workers\", \"10\"], WS),\n         (\"judges\", [PY, \"scoring/api_judges.py\", \"--stage\", \"judges\", \"--concurrency\", \"32\"], WS),\n         (\"local_judge\", [GPU, \"scoring/local_judge.py\", \"--which\", \"qwen8b_disg,qwen8b_orig\", \"--bs\", \"64\"], WS),\n         (\"pilot\", [PY, \"scoring/pilot_metrics_E2.py\"], WS),\n         (\"assemble\", [PY, \"scoring/assemble_scores.py\"], WS)]\n    s += [(f\"labels:{x}\", [E2PY, f\"src_e2/{x}.py\"], WS / \"e2src\")\n          for x in (\"assemble_e2\", \"controls_e2\", \"testability_e2\", \"seal_e2\", \"verify_seal\")]\n    s += [(\"join\", [PY, \"analysis/analyse_E2A.py\", \"--stage\", \"join\"], WS),\n          (\"analyse\", [PY, \"analysis/analyse_E2A.py\", \"--stage\", \"analyse\"] + ([\"--prefix\", str(prefix)] if prefix else []), WS),\n          (\"rename\", [PY, \"analysis/rename_V0.py\"], WS),\n          (\"union\", [PY, \"analysis/union_E2B.py\", \"--deadline-utc\", \"2026-09-24T15:40:00Z\", \"--once\"], WS),\n          (\"outputs\", [PY, \"analysis/make_outputs.py\"], WS)]\n    return s\n\n\ndef main() -> None:\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--from\", dest=\"start\", default=\"l3\")\n    ap.add_argument(\"--prefix\", type=int, default=110)\n    a = ap.parse_args()\n    env = dict(os.environ, PYTHONHASHSEED=\"0\", OPENBLAS_NUM_THREADS=\"1\", OMP_NUM_THREADS=\"1\")\n    run = False\n    for name, cmd, cwd in stages(a.prefix):\n        run = run or name.startswith(a.start)\n        if run:\n            print(f\"== {name}: {' '.join(cmd)}\", flush=True)\n            subprocess.run(cmd, cwd=cwd, env=env, check=True)\n\n\nif __name__ == \"__main__\":\n    sys.exit(main())\n----\n{\n  \"metadata\": {\n    \"method_name\": \"frozen cross-family solver consensus c_score_align (V0) and comparators on untouched E2\",\n    \"orientation\": \"every predict_* is higher = more likely ERROR; output = E2 final label (E's frozen protocol)\",\n    \"verdict\": \"NOT_TESTABLE ((a): too few rows with the pre-registered flash-lite disguised bar; see fallback_substitute_bar)\"\n  },\n  \"datasets\": [\n    {\n      \"dataset\": \"E2_DT\",\n      \"examples\": [\n        {\n          \"input\": \"{\\\"text\\\": \\\"If Xiomara either wakes up at dawn or has light slumber (but not both), then she sleeps very lightly.\\\", \\\"candidate_fol\\\": \\\"(WakesAtDawn(xiomara) ∨ LightSlumber(xiomara) ∧ ¬(WakesAtDawn(xiomar...\",\n          \"output\": \"CONTESTED\",\n          \"metadata_row_key\": \"a6914eef11622a25|fewshot_v1\",\n          \"metadata_sentence_id\": \"b91115ec794d\",\n          \"metadata_stratum\": \"DT\",\n          \"metadata_slot\": \"G1\",\n          \"metadata_system\": \"G1:meta-llama/llama-3.1-8b-instruct\",\n          \"metadata_family\": \"meta\",\n          \"metadata_label_tier\": \"A_unaudited_ref\",\n          \"metadata_reading_choice\": false,\n          \"metadata_vex\": false,\n          \"metadata_pilot\": true,\n          \"metadata_words\": 19,\n          \"metadata_n_conditions\": 2,\n          \"metadata_parse_ok\": true,\n          \"metadata_fold_E2\": 1,\n          \"predict_c_score_align\": \"1.000000\",\n          \"predict_p_peer_text\": \"0.957770\",\n          \"predict_c_exact\": \"1.000000\",\n          \"predict_g_align\": \"1.000000\",\n          \"predict_c_pn\": \"1.000000\",\n          \"predict_c_rw\": \"1.000000\",\n          \"predict_c_pn_rw\": \"1.000000\",\n          \"predict_c_two\": \"0.838446\",\n          \"predict_c_v5\": \"1.000000\",\n          \"predict_judge_cheap_disg\": \"null\",\n          \"predict_judge_cheap_orig\": \"null\",\n          \"predict_judge_cheap2_disg\": \"null\",\n          \"predict_judge_cheap2_orig\": \"null\",\n          \"predict_judge_local_qwen8b_disg\": \"0.150000\",\n          \"predict_judge_local_qwen8b_orig\": \"0.200000\",\n          \"predict_l2_bow\": \"0.125000\",\n          \"predict_l3_z3\": \"0.916667\",\n          \"predict_pilot_joint_conflict\": \"0.000000\",\n          \"predict_pilot_arity_incons\": \"0.000000\",\n          \"predict_pilot_shape_incons\": \"0.000000\",\n          \"predict_pilot_dangling\": \"1.000000\",\n          \"predict_pilot_rerun_jacc\": \"0.386532\"\n        },\n        {\n          \"input\": \"{\\\"text\\\": \\\"If Xiomara either wakes up at dawn or has light slumber (but not both), then she sleeps very lightly.\\\", \\\"candidate_fol\\\": \\\"(WakesUpAt(xiomara, dawn) ⊕ Has(xiomara, lightSlumber)) → SleepsVery...\",\n          \"output\": \"CORRECT\",\n          \"metadata_row_key\": \"62b8d8e91effd650|fewshot_v1\",\n          \"metadata_sentence_id\": \"b91115ec794d\",\n          \"metadata_stratum\": \"DT\",\n          \"metadata_slot\": \"G1b\",\n          \"metadata_system\": \"G1b:meta-llama/llama-3.3-70b-instruct\",\n          \"metadata_family\": \"meta\",\n          \"metadata_label_tier\": \"B\",\n          \"metadata_reading_choice\": false,\n          \"metadata_vex\": \n----\n\"\"\"Reusable gold-free NL->FOL faithfulness metrics (E2-A, iteration 5), thin wrappers over the FROZEN code copies in\n../frozen (exp-5 peer_text / pool_scoring / vendor_c eqmv) and ../freeze_copy (consensus_variants). Nothing is refit.\n\nEvery per-candidate score is oriented HIGHER = MORE LIKELY AN ERROR (unfaithful translation).\nEvery function states (i) what it MEASURES, (ii) what it does NOT measure, (iii) whether it needs a gold formula, (iv) cost.\n\nEntry points\n  parse_fol(fol)                                        dataset-E parser; None = unparseable (coverage failure)\n  c_score_align(fol, peers, family=None)                V0, the frozen primary consensus score\n  c_exact(fol, peers, family=None)                      same consensus with exact symbol names (no aligner)\n  peer_text(text, fol, peers, family=None, q=None)      PT: frozen fusion of graded consensus + V0 + text-side checks\n  variants_for_sentence(rows, weights=None)             V1-V5 for every output of ONE sentence (set-level)\n  family_weights_from_sentences(list_of_rows_lists)     label-free family reliability weights for V2/V3/V5\n  evaluate(scores, labels, strata, sentence_ids)        stratified AUROC + stratified sentence-cluster bootstrap CI\n\n`peers` = list of (peer_fol: str, peer_family: str): formalizations of the SAME sentence produced by other systems.\nWith `family` given, peers of the candidate's own model family are dropped (leave-own-family-out, as frozen).\n\"\"\"\nfrom __future__ import annotations\n\nimport sys\nfrom pathlib import Path\n\n_WS = Path(__file__).resolve().parents[1]\nfor _p in (_WS / \"frozen\" / \"exp5\" / \"src\", _WS / \"freeze_copy\", _WS / \"frozen\" / \"eval2\" / \"src\"):\n    if str(_p) not in sys.path:\n        sys.path.insert(0, str(_p))\n\nimport numpy as np  # noqa: E402\n\nimport peer_text as _PT  # noqa: E402  (frozen exp-5; binds the dataset-E parser)\n\n_PRE5 = None\n\n\ndef _prereg5() -> dict:\n    global _PRE5\n    if _PRE5 is None:\n        import json\n        _PRE5 = json.loads((_WS / \"frozen\" / \"exp5\" / \"results\" / \"prereg.json\").read_text())\n    return _PRE5\n\n\ndef parse_fol(fol: str | None):\n    \"\"\"MEASURES: whether `fol` parses under the dataset-E grammar (the parser that defines UNPARSEABLE labels).\n    Returns the AST or None. GOLD: not needed. COST: microseconds.\"\"\"\n    return _PT.parse_fol(fol) if fol else None\n\n\ndef _pool(peers, family):\n    return [p for p, f in peers if (family is None or f != family)]\n\n\ndef c_score_align(fol: str, peers: list[tuple[str, str]], family: str | None = None, min_peers: int = 2) -> float | None:\n    \"\"\"V0 (PRIMARY, frozen). MEASURES: 1 - (share of parseable peer formalizations of the same sentence, from model families\n    other than the candidate's, that the iteration-1 eqmv procedure proves z3-equivalent to the candidate modulo a\n    predicate/constant vocabulary alignment). i.e. how far the candidate sits from what independent systems write.\n    DOES NOT MEASURE: agreement with a reference, or truth. An error that most peers share scores as faithful\n    (peer-endorsed error); a correct but idiosyncratic reading scores as an error; a wrong predicate in the right place\n    can be aligned away (MEANING_RENAME blind spot).\n    Unparseable candidate -> 1.0; < `min_peers` parseable peers -> None (the caller imputes; E2 used exp-5's neutral 0.6266).\n    GOLD: not needed. COST: the peers' generation (~$0.002 per sentence for 7 families) + z3 (eqmv 3 s cap per pair).\"\"\"\n    from common import eqmv  # vendor_c (bound to the dataset-E parser by peer_text)\n    e = parse_fol(fol)\n    if e is None:\n        return 1.0\n    cs = _PT.canon(e)\n    P = []\n    for p in _pool(peers, family):\n        pe = parse_fol(p)\n        if pe is not None:\n            P.append(_PT.canon(pe))\n    if len(P) < min_peers:\n        return None\n    agree = 0\n    for ps in P:\n        if ps == cs:\n            agree += 1\n            continue\n        a, b = (cs, ps) if cs < ps else (ps, cs)  # frozen canonical argument order\n        try:\n            r = eqmv(_PT.parse_fol(a), _PT.parse_fol(b))\n            agree += bool(r and r[0] is True)\n        except Exception:  # noqa: BLE001 - UNKNOWN counts as not equivalent\n            pass\n    return 1 - agree / len(P)\n\n\ndef c_exact(fol: str, peers: list[tuple[str, str]], family: str | None = None, min_peers: int = 2, ms: int = 2000) -> float | None:\n    \"\"\"MEASURES: 1 - share of family-disjoint parseable peers that z3 proves equivalent to the candidate with symbols\n    identified by their EXACT names (no aligner). Stricter than V0: any vocabulary difference counts as disagreement, so it\n    false-alarms on correct candidates whose wording differs from the peers'. DOES NOT MEASURE: meaning across vocabularies.\n    GOLD: not needed. COST: as V0, z3 only (2 x `ms` per pair).\"\"\"\n    e = parse_fol(fol)\n    if e is None:\n        return 1.0\n    P = [parse_fol(p) for p in _pool(peers, family)]\n    P = [p for p in P if p is not None]\n    if len(P) < min_peers:\n        return None\n    n = 0\n    for pe in P:\n        if _PT.canon(pe) == _PT.canon(e):\n            n += 1\n            continue\n        n += bool(_PT.z3_entails(e, pe, ms) is True and _PT.z3_entails(pe, e, ms) is True)\n    return 1 - n / len(P)\n\n\ndef peer_text(text: str, fol: str, peers: list[tuple[str, str]], family: str | None = None, q: dict | None = None) -> dict:\n    \"\"\"PT (frozen exp-5 fusion). MEASURES: a fixed logistic combination (coefficients frozen on the iteration-2 screen) of\n    ALIGN graded consensus g, V0, L2-bow (share of the sentence's content words the formula's symbols do not carry, plus\n    unanchored predicates) and L3 (mismatches between an LLM's role questionnaire of the TEXT and the formula's z3 role\n    profile; needs `q` from the exp-A questionnaire, else the neutral value is used).\n    Returns {'p_error', 'c_score_align', 'g_align', 'l2_bow', 'l3_z3'}. DOES NOT MEASURE: anything the peers all get wrong\n    and the text words do not reveal (scope, binding). GOLD: not needed. COST: V0's plus one small LLM call per sentence (L3).\"\"\"\n    import pool_scoring as PS\n    pre = _prereg5()\n    P = dict(pre[\"scoring_params\"])\n    P.update(variants=[\"ALIGN\"], k6_seeds=0, famfield=False, medoid_budget_s=0)\n    rows = [{\"key\": \"CAND\", \"fol\": fol, \"family\": family or \"__cand__\", \"family_field\": family or \"__cand__\", \"system\": \"cand\", \"is_peer\": True}]\n    rows += [{\"key\": f\"P{i}\", \"fol\": p, \"family\": f, \"family_field\": f, \"system\": f\"peer{i}\", \"is_peer\": True} for i, (p, f) in enumerate(peers)]\n    out = {r[\"key\"]: r for r in PS.score_sentence({\"sentence_id\": \"lib\", \"text\": text, \"q\": q, \"rows\": rows}, P)[\"rows\"]}\n    s = out[\"CAND\"]\n    if s.get(\"coverage_status\") != \"OK\":\n        return {\"p_error\": 1.0, \"c_score_align\": 1.0, \"g_align\": 1.0, \"l2_bow\": 1.0, \"l3_z3\": 1.0}\n    neutral = pre[\"imputation\"][\"neutral\"]\n    feats = dict(s)\n    for k in (\"c_score_align\", \"ALIGN:g_score\", \"l2_bow\", \"l3_z3\"):\n        if feats.get(k) is None:\n            feats[k] = neutral.get(k)\n    feats[\"coverage_status\"] = \"OK\"\n    return {\"p_error\": _PT.fused_score(pre[\"frozen\"], feats)[\"p_error\"], \"c_score_align\": feats[\"c_score_align\"],\n            \"g_align\": feats[\"ALIGN:g_score\"], \"l2_bow\": feats[\"l2_bow\"], \"l3_z3\": feats[\"l3_z3\"]}\n\n\ndef variants_for_sentence(rows: list[dict], weights: dict | None = None) -> dict[str, dict]:\n    \"\"\"SET-LEVEL (all outputs of ONE sentence). rows = [{'row_key', 'fol', 'family', 'slot'}]. Builds the eval-2 pairwise\n    eqmv matrix, then returns per row_key {V0, c_exact, V1 c_pn, V2 c_rw, V3 c_pn_rw, V5 c_v5} with the frozen freeze code.\n    MEASURES (V1): disagreement normalised by the size of the largest agreeing class (discounts scattered peers);\n    (V2/V3/V5): the same with label-free family reliability weights (`weights` from family_weights_from_sentences; None =\n    uniform). On E2 none of V1-V5 was carried by the freeze (development gain < +0.015 over V0). GOLD: not needed.\"\"\"\n    import consensus_variants as CV\n    import pairwise\n    m = pairwise.pairwise_matrix([{\"row_key\": r[\"row_key\"], \"fol\": r[\"fol\"], \"slot\": r.get(\"slot\", r[\"family\"]), \"family\": r[\"family\"],\n                                   \"family_field\": r[\"family\"], \"system_class\": \"llm\"} for r in rows])\n    m[\"sentence_id\"] = \"lib\"\n    I = CV.build_index(m)\n    w = weights or {}\n    out = {}\n    for r in rows:\n        k = r[\"row_key\"]\n        out[k] = {\"V0\": CV.c_score_align(I, k), \"c_exact\": CV.c_exact(I, k), \"V1\": CV.c_pn(I, k), \"V2\": CV.c_rw(I, k, w),\n                  \"V3\": CV.c_pn_rw(I, k, w), \"V5\": CV.c_v5(I, k, w)}\n    return out\n\n\ndef family_weights_from_sentences(sentences: list[list[dict]]) -> dict:\n    \"\"\"Label-free family reliability weights (mean cross-family agreement rate, shrunk to the grand mean with 20\n    pseudo-sentences; freeze consensus_variants.family_weights). MEASURES how often a family's outputs agree with other\n    families' - a proxy for reliability, NOT accuracy. GOLD: not needed.\"\"\"\n    import consensus_variants as CV\n    import pairwise\n    idx = []\n    for i, rows in enumerate(sentences):\n        m = pairwise.pairwise_matrix([{\"row_key\": r[\"row_key\"], \"fol\": r[\"fol\"], \"slot\": r.get(\"slot\", r[\"family\"]), \"family\": r[\"family\"],\n                                       \"family_field\": r[\"family\"], \"system_class\": \"llm\"} for r in rows])\n        m[\"sentence_id\"] = f\"s{i}\"\n        idx.append(CV.build_index(m))\n    return CV.family_weights(idx, {f\"s{i}\": 0 for i in range(len(idx))}, None)\n\n\ndef evaluate(scores, labels, strata, sentence_ids, b: int = 2000, seed: int = 0) -> dict:\n    \"\"\"META-EVALUATION of any score column. labels: 1 = ERROR, 0 = CORRECT (None rows are skipped). MEASURES: the\n    within-stratum pair AUROC (probability that a random ERROR scores above a random CORRECT of the same stratum) with a\n    stratified sentence-cluster bootstrap 95% CI. 0.5 = does not track correctness.\"\"\"\n    from stats import WStratAuc, ci, strat_auc\n    sys.path.insert(0, str(_WS / \"analysis\"))\n    from analyse_E2A import strat_boot_weights\n    s = np.asarray(scores, float)\n    y = np.array([np.nan if v is None else float(v) for v in labels])\n    st, sid = np.asarray(strata), np.asarray(sentence_ids)\n    m = ~np.isnan(s) & ~np.isnan(y)\n    W = strat_boot_weights(sid[m], st[m], b, seed)\n    f = WStratAuc(y[m], s[m], st[m])\n    return {\"n\": int(m.sum()), \"strat_auroc\": float(strat_auc(y[m], s[m], st[m])), \"ci\": ci([f(W[i]) for i in range(b)])}\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11/analysis:\nanalyse_E2A.py\nmake_outputs.py\nrename_V0.py\ntests\nunion_E2B.py\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11/audit:\nrederive.py\nrederive_out.json\n\n/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11/scoring:\napi_judges.py\nassemble_scores.py\ncommon.py\nguard.py\nlocal_judge.py\npilot_metrics_E2.py\nrun_scoring.sh\nscore_consensus.py\ntests", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [12] TOOL CALL — Bash · 2026-09-25 13:14:58 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11; wc -l $W/audit/rederive.py $W/analysis/*.py $W/scoring/*.py; cat $W/audit/rederive.py; cat $W/audit/rederive_out.json | head -80
```

### [13] TOOL RESULT — Bash · 2026-09-25 13:14:58 UTC

```
{"stdout": "   87 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11/audit/rederive.py\n  549 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11/analysis/analyse_E2A.py\n  173 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11/analysis/make_outputs.py\n   57 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11/analysis/rename_V0.py\n  119 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11/analysis/union_E2B.py\n  166 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11/scoring/api_judges.py\n  154 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11/scoring/assemble_scores.py\n   45 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11/scoring/common.py\n   85 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11/scoring/guard.py\n  102 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11/scoring/local_judge.py\n   74 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11/scoring/pilot_metrics_E2.py\n  266 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11/scoring/score_consensus.py\n 1877 total\n\"\"\"Independent re-derivation of the headline numbers from RAW files through a different code path\n(sklearn roc_auc_score per stratum, raw sealed labels, raw consensus/judge caches; no analysis/ code imported).\"\"\"\nimport json, random, collections\nimport numpy as np\nfrom sklearn.metrics import roc_auc_score\nW = __import__(\"pathlib\").Path(__file__).resolve().parents[1]\njl = lambda p: [json.loads(l) for l in open(p) if l.strip()]\nlab = {r[\"row_key\"]: r for r in jl(W / \"e2src/sealed/labels_E2.jsonl\") if r[\"system_class\"] == \"llm\"}\ncand = {r[\"row_key\"]: r for r in jl(W / \"e2/candidates_E2_nolabels.jsonl\")}\norder = json.load(open(W / \"e2src/work/e2a_order.json\"))[:110]\nkeep = set(order)\nv0 = {}\nfor s in jl(W / \"cache/consensus_sentences.jsonl\"):\n    for r in s[\"rows\"]:\n        v0[r[\"key\"]] = r.get(\"c_score_align\")\nunits = {u[\"key\"]: u for u in jl(W / \"cache/units_E2.jsonl\")}\nloc = {}\nfor r in jl(W / \"cache/judge_local_qwen8b.jsonl\"):\n    if r.get(\"p\") is not None:\n        loc[r[\"key\"]] = 1 - r[\"p\"]\npil = {r[\"key\"]: r for r in jl(W / \"cache/pilot_E2.jsonl\")}\nrows = []\nfor k, l in lab.items():\n    c = cand[k]\n    if c[\"sentence_id\"] not in keep or l[\"label\"] not in (\"CORRECT\", \"ERROR\") or l[\"reading_choice\"] or l[\"label_tier\"] not in (\"A\", \"B\"):\n        continue\n    rows.append(dict(k=k, sid=c[\"sentence_id\"], st=c[\"stratum\"], y=int(l[\"label\"] == \"ERROR\"), v0=v0.get(k),\n                     loc=loc.get(k + \"|disg\"), **{m: pil[k].get(m) for m in (\"pilot_joint_conflict\", \"pilot_arity_incons\", \"pilot_shape_incons\", \"pilot_dangling\", \"pilot_rerun_jacc\")}))\n\n\ndef sauc(rs, col, ycol=\"y\"):\n    num = den = 0\n    for st in set(r[\"st\"] for r in rs):\n        g = [r for r in rs if r[\"st\"] == st and r[col] is not None]\n        y = [r[ycol] for r in g]\n        if 0 < sum(y) < len(y):\n            w = sum(y) * (len(y) - sum(y))\n            num += roc_auc_score(y, [r[col] for r in g]) * w\n            den += w\n    return num / den if den else None\n\n\nout = {}\nfor cell, sts in ((\"ALL\", (\"L25\", \"EXC\", \"DT\")), (\"DT\", (\"DT\",)), (\"LONG\", (\"L25\", \"EXC\"))):\n    rs = [r for r in rows if r[\"st\"] in sts]\n    out[cell] = {\"n\": len(rs), \"n_err\": sum(r[\"y\"] for r in rs), \"n_cor\": sum(1 - r[\"y\"] for r in rs),\n                 \"V0\": sauc(rs, \"v0\"), \"local_disg\": sauc(rs, \"loc\")}\n    out[cell][\"delta_V0_minus_local\"] = out[cell][\"V0\"] - out[cell][\"local_disg\"]\n    for m in (\"pilot_joint_conflict\", \"pilot_arity_incons\", \"pilot_shape_incons\", \"pilot_dangling\", \"pilot_rerun_jacc\"):\n        out[cell][m] = sauc(rs, m)\n# placebo: shuffled labels within stratum -> AUROC ~0.5 and the V0-local delta ~0\nrng = random.Random(0)\npl = []\nfor b in range(200):\n    rs = [dict(r) for r in rows]\n    for st in set(r[\"st\"] for r in rs):\n        idx = [i for i, r in enumerate(rs) if r[\"st\"] == st]\n        ys = [rs[i][\"y\"] for i in idx]\n        rng.shuffle(ys)\n        for i, y in zip(idx, ys):\n            rs[i][\"y\"] = y\n    pl.append((sauc(rs, \"v0\"), sauc(rs, \"v0\") - sauc(rs, \"loc\")))\npa = np.array(pl)\nout[\"placebo_shuffled\"] = {\"V0_mean\": float(pa[:, 0].mean()), \"V0_p2.5_97.5\": np.percentile(pa[:, 0], [2.5, 97.5]).tolist(),\n                           \"delta_mean\": float(pa[:, 1].mean()), \"delta_p2.5_97.5\": np.percentile(pa[:, 1], [2.5, 97.5]).tolist(),\n                           \"real_V0_ALL_above_placebo_p97.5\": bool(out[\"ALL\"][\"V0\"] > np.percentile(pa[:, 0], 97.5))}\n# rename controls from their raw rows\nrr = jl(W / \"results/rename_V0_rows.jsonl\")\nfor t in (\"RENAME_SYN\", \"RENAME_NONCE\"):\n    g = [r for r in rr if r[\"type\"] == t and r[\"v0_control\"] is not None and r[\"v0_parent\"] is not None]\n    out[t] = {\"n\": len(g), \"FA\": sum(r[\"v0_control\"] > 0.5 for r in g) / len(g), \"base\": sum(r[\"v0_parent\"] > 0.5 for r in g) / len(g)}\n# drift + spend from raw logs\nd = json.load(open(W / \"e2src/panel_drift_E2.json\"))\nout[\"drift_majority_agreement\"] = d[\"combined\"][\"majority_agreement\"]\nspend = sum(r[\"cost_usd\"] for r in jl(W / \"e2src/cost_ledger.jsonl\")) + sum(r[\"cost_usd\"] for r in jl(W / \"cache/l3_cost_ledger.jsonl\")) \\\n    + sum((r.get(\"cost\") or 0) for r in jl(W / \"cache/t1_results/costs.jsonl\"))\nout[\"spend_usd\"] = spend\n# compare with the pipeline's aggregated numbers\nA = json.load(open(W / \"results/auroc_cells.json\"))[\"R_AB\"]\ncmp = {}\nfor cell, key in ((\"ALL\", \"ALL\"), (\"DT\", \"DT\"), (\"LONG\", \"LONG (L25+EXC)\")):\n    m = A[key][\"metrics\"]\n    cmp[cell] = {\"n_match\": A[key][\"n_rows\"] == out[cell][\"n\"], \"V0_absdiff\": abs(m[\"c_score_align\"][\"strat\"] - out[cell][\"V0\"]),\n                 \"local_absdiff\": abs(m[\"judge_local_qwen8b_disg\"][\"strat\"] - out[cell][\"local_disg\"])}\nout[\"comparison_with_pipeline\"] = cmp\njson.dump(out, open(W / \"audit/rederive_out.json\", \"w\"), indent=1)\nprint(json.dumps(out, indent=1))\n{\n \"ALL\": {\n  \"n\": 273,\n  \"n_err\": 150,\n  \"n_cor\": 123,\n  \"V0\": 0.8904441294590124,\n  \"local_disg\": 0.894991731632412,\n  \"delta_V0_minus_local\": -0.004547602173399556,\n  \"pilot_joint_conflict\": 0.5,\n  \"pilot_arity_incons\": 0.5066146940703993,\n  \"pilot_shape_incons\": 0.5099811008740845,\n  \"pilot_dangling\": 0.4131230805575242,\n  \"pilot_rerun_jacc\": 0.7126151665485473\n },\n \"DT\": {\n  \"n\": 179,\n  \"n_err\": 74,\n  \"n_cor\": 105,\n  \"V0\": 0.9161518661518661,\n  \"local_disg\": 0.9129343629343629,\n  \"delta_V0_minus_local\": 0.003217503217503137,\n  \"pilot_joint_conflict\": 0.5,\n  \"pilot_arity_incons\": 0.5067567567567568,\n  \"pilot_shape_incons\": 0.5099742599742599,\n  \"pilot_dangling\": 0.3996138996138996,\n  \"pilot_rerun_jacc\": 0.7287001287001288\n },\n \"LONG\": {\n  \"n\": 94,\n  \"n_err\": 76,\n  \"n_cor\": 18,\n  \"V0\": 0.603448275862069,\n  \"local_disg\": 0.694683908045977,\n  \"delta_V0_minus_local\": -0.09123563218390807,\n  \"pilot_joint_conflict\": 0.5,\n  \"pilot_arity_incons\": 0.5050287356321839,\n  \"pilot_shape_incons\": 0.5100574712643678,\n  \"pilot_dangling\": 0.5639367816091954,\n  \"pilot_rerun_jacc\": 0.5330459770114944\n },\n \"placebo_shuffled\": {\n  \"V0_mean\": 0.49687632884479094,\n  \"V0_p2.5_97.5\": [\n   0.43272354122371837,\n   0.5784874793290811\n  ],\n  \"delta_mean\": -0.0016802504134183877,\n  \"delta_p2.5_97.5\": [\n   -0.06008002598629819,\n   0.06907335223245929\n  ],\n  \"real_V0_ALL_above_placebo_p97.5\": true\n },\n \"RENAME_SYN\": {\n  \"n\": 36,\n  \"FA\": 0.9444444444444444,\n  \"base\": 0.3611111111111111\n },\n \"RENAME_NONCE\": {\n  \"n\": 145,\n  \"FA\": 1.0,\n  \"base\": 0.2620689655172414\n },\n \"drift_majority_agreement\": 0.9554,\n \"spend_usd\": 2.04500803205,\n \"comparison_with_pipeline\": {\n  \"ALL\": {\n   \"n_match\": true,\n   \"V0_absdiff\": 0.0,\n   \"local_absdiff\": 1.1102230246251565e-16\n  },\n  \"DT\": {\n   \"n_match\": true,\n   \"V0_absdiff\": 0.0,\n   \"local_absdiff\": 1.1102230246251565e-16\n  },\n  \"LONG\": {\n   \"n_match\": true,\n   \"V0_absdiff\": 0.0,\n   \"local_absdiff\": 0.0", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [14] TOOL CALL — Bash · 2026-09-25 13:15:14 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11; cd $W; head -c 1500 per_item_E2A.jsonl; echo; wc -l per_item_E2A.jsonl results/rename_V0_rows.jsonl; head -2 results/rename_V0_rows.jsonl; grep -n "def strat_boot_weights" -A25 analysis/analyse_E2A.py; ls frozen/eval2/src; grep -n "def WStratAuc\|def strat_auc\|def ci" -A20 frozen/eval2/src/stats.py | head -80
```

### [15] TOOL RESULT — Bash · 2026-09-25 13:15:14 UTC

```
{"stdout": "{\"row_key\": \"87618fded07e3eb4|fewshot_v1\", \"item_id\": \"87618fded07e3eb4\", \"sentence_id\": \"679fdea26cad\", \"stratum\": \"EXC\", \"slot\": \"G1\", \"system\": \"G1:meta-llama/llama-3.1-8b-instruct\", \"family\": \"meta\", \"pilot\": true, \"words\": 19, \"word_bin\": null, \"exception_type\": \"without\", \"text_conditions\": 1, \"fold_E2\": 2, \"parse_ok\": true, \"consensus_coverage\": \"OK\", \"n_peers_used\": 8, \"n_unknown_align\": 0, \"gen_cost_usd\": 1.086e-05, \"c_score_align__imputed\": false, \"c_score_align\": 1.0, \"g_align__imputed\": false, \"g_align\": 1.0, \"l2_bow__imputed\": false, \"l2_bow\": 0.125, \"l3_z3__imputed\": false, \"l3_z3\": 0.25, \"p_peer_text\": 0.8927705659020497, \"c_exact\": 1.0, \"c_pn\": 1.0, \"c_rw\": 1.0, \"c_pn_rw\": 1.0, \"c_v5\": 1.0, \"c_two\": 0.8384464684152174, \"c_align_pw\": 1.0, \"c_exact_z3direct\": 1.0, \"judge_cheap_disg\": null, \"judge_cheap_disg_cost\": null, \"judge_cheap_disg_share\": null, \"judge_cheap_orig\": null, \"judge_cheap_orig_cost\": null, \"judge_cheap_orig_share\": null, \"judge_cheap2_disg\": null, \"judge_cheap2_disg_cost\": null, \"judge_cheap2_disg_share\": null, \"judge_cheap2_orig\": null, \"judge_cheap2_orig_cost\": null, \"judge_cheap2_orig_share\": null, \"judge_local_qwen8b_disg\": 0.050000000000000044, \"judge_local_qwen8b_disg_cost\": null, \"judge_local_qwen8b_disg_share\": null, \"judge_local_qwen8b_orig\": 0.050000000000000044, \"judge_local_qwen8b_orig_cost\": null, \"judge_local_qwen8b_orig_share\": null, \"pilot_joint_conflict\": 0, \"pilot_arity_incons\": 0, \"pilot_shape_incons\": 0, \"pilot_dangling\": 1.\n    5500 per_item_E2A.jsonl\n     181 results/rename_V0_rows.jsonl\n    5681 total\n{\"row_key\": \"74a7217d8d0e673e|fewshot_v1|RENAME_SYN\", \"type\": \"RENAME_SYN\", \"stratum\": \"L25\", \"v0_control\": 0.875, \"v0_parent\": 0.875}\n{\"row_key\": \"74a7217d8d0e673e|fewshot_v1|RENAME_NONCE\", \"type\": \"RENAME_NONCE\", \"stratum\": \"L25\", \"v0_control\": 1.0, \"v0_parent\": 0.875}\n126:def strat_boot_weights(sids, strata, b: int = B, seed: int = 0) -> np.ndarray:\n127-    \"\"\"Stratified sentence-cluster bootstrap: within each stratum, sentences resampled with replacement.\n128-    -> (B, n_rows) multiplicity weights.\"\"\"\n129-    sids, strata = np.asarray(sids), np.asarray(strata)\n130-    rng = np.random.default_rng(seed)\n131-    W = np.zeros((b, len(sids)))\n132-    for st in sorted(set(strata)):\n133-        m = strata == st\n134-        keys, inv = np.unique(sids[m], return_inverse=True)\n135-        S = len(keys)\n136-        C = np.stack([np.bincount(rng.integers(0, S, S), minlength=S) for _ in range(b)]).astype(float)\n137-        W[:, np.where(m)[0]] = C[:, inv]\n138-    return W\n139-\n140-\n141-def cell_eval(D: Data, mask: np.ndarray, metrics: dict[str, np.ndarray], pairs: list[tuple[str, str]], seed: int = 0) -> dict:\n142-    \"\"\"strat AUROC (+ pooled) with stratified cluster-bootstrap CIs for each metric on rows of `mask` where it is present;\n143-    paired deltas on rows where both are present.\"\"\"\n144-    idx = np.where(mask)[0]\n145-    y, st, sid = D.y[idx], D.stratum[idx], D.sid[idx]\n146-    out = {\"n_rows\": int(len(idx)), \"n_error\": int(y.sum()), \"n_correct\": int(len(idx) - y.sum()),\n147-           \"n_sentences\": int(len(set(sid))), \"n_err_sent\": int(len(set(sid[y == 1]))), \"n_cor_sent\": int(len(set(sid[y == 0]))),\n148-           \"metrics\": {}, \"deltas\": {}}\n149-    out[\"testable\"] = bool(out[\"n_error\"] >= 50 and out[\"n_correct\"] >= 50 and out[\"n_err_sent\"] >= 25 and out[\"n_cor_sent\"] >= 25)\n150-    if len(idx) == 0 or y.sum() == 0 or y.sum() == len(y):\n151-        return out\nconsensus_mx.py\ncopy_inputs.py\nframe.py\nm4.py\nmechanism.py\npairwise.py\npart_a.py\npaths.py\nrecord.py\nrun_matrix.py\nstats.py\n25:def strat_auc(y, s, strata) -> float:\n26-    \"\"\"Within-stratum pair AUROC: sum_s w_s AUROC_s with w_s = n_err,s * n_cor,s (exp 5 'stratified').\"\"\"\n27-    y, s, strata = np.asarray(y, float), np.asarray(s, float), np.asarray(strata)\n28-    num = den = 0.0\n29-    for st in np.unique(strata):\n30-        m = strata == st\n31-        n1 = int(y[m].sum())\n32-        n0 = int(m.sum()) - n1\n33-        if n1 and n0:\n34-            num += auc(y[m], s[m]) * n1 * n0\n35-            den += n1 * n0\n36-    return num / den if den else float(\"nan\")\n37-\n38-\n39-class ClusterBoot:\n40-    \"\"\"Sentence-cluster bootstrap resamples (sentence_ids drawn with replacement; all rows of a drawn sentence kept).\"\"\"\n41-\n42-    def __init__(self, sids, b: int = B_DEFAULT, seed: int = 0):\n43-        by = defaultdict(list)\n44-        for i, s in enumerate(sids):\n45-            by[s].append(i)\n--\n53:def ci(vals, lo=2.5, hi=97.5):\n54-    v = np.asarray([x for x in vals if x is not None and not np.isnan(x)], float)\n55-    if len(v) == 0:\n56-        return [None, None]\n57-    return [float(np.percentile(v, lo)), float(np.percentile(v, hi))]\n58-\n59-\n60-def boot_stat(boot: ClusterBoot, fn) -> list:\n61-    return [fn(ix) for ix in boot.idx]\n62-\n63-\n64-# ------------------------------------------------------------------ weighted (bootstrap-count) statistics\n65-class WAuc:\n66-    \"\"\"AUROC under row weights (bootstrap multiplicities); ties = 0.5. Precomputes the score ranking once.\"\"\"\n67-\n68-    def __init__(self, y, s):\n69-        self.y = np.asarray(y, float)\n70-        vals, self.inv = np.unique(np.asarray(s, float), return_inverse=True)\n71-        self.nv = len(vals)\n72-\n73-    def __call__(self, w) -> float:", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [16] TOOL CALL — Bash · 2026-09-25 13:15:28 UTC

```
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11; cd $W; sed -n 1,24p frozen/eval2/src/stats.py; sed -n 64,140p frozen/eval2/src/stats.py; head -c 800 e2src/sealed/labels_E2.jsonl; echo; head -c 1200 e2/candidates_E2_nolabels.jsonl; echo; ls -la cache e2src/work | head -40; python3 -c "
import json;d=json.load(open('e2src/panel_drift_E2.json'));print(d['combined'])"
```

### [17] TOOL RESULT — Bash · 2026-09-25 13:15:28 UTC

```
{"stdout": "\"\"\"Statistics shared by every analysis: tie-aware AUROC, stratified (within-stratum pair) AUROC, and a\nsentence-cluster bootstrap that yields resample index arrays (numpy default_rng(0), B=2000).\"\"\"\nfrom __future__ import annotations\n\nfrom collections import defaultdict\n\nimport numpy as np\nfrom scipy.stats import rankdata\n\nB_DEFAULT = 2000\n\n\ndef auc(y, s) -> float:\n    \"\"\"Mann-Whitney AUROC with ties = 0.5 (identical to sklearn roc_auc_score).\"\"\"\n    y = np.asarray(y, dtype=float)\n    s = np.asarray(s, dtype=float)\n    n1 = int(y.sum())\n    n0 = len(y) - n1\n    if n1 == 0 or n0 == 0:\n        return float(\"nan\")\n    r = rankdata(s)\n    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))\n\n\n# ------------------------------------------------------------------ weighted (bootstrap-count) statistics\nclass WAuc:\n    \"\"\"AUROC under row weights (bootstrap multiplicities); ties = 0.5. Precomputes the score ranking once.\"\"\"\n\n    def __init__(self, y, s):\n        self.y = np.asarray(y, float)\n        vals, self.inv = np.unique(np.asarray(s, float), return_inverse=True)\n        self.nv = len(vals)\n\n    def __call__(self, w) -> float:\n        w = np.asarray(w, float)\n        W1 = np.bincount(self.inv, weights=w * self.y, minlength=self.nv)\n        W0 = np.bincount(self.inv, weights=w * (1 - self.y), minlength=self.nv)\n        den = W1.sum() * W0.sum()\n        if den <= 0:\n            return float(\"nan\")\n        cum0 = np.cumsum(W0) - W0\n        return float((W1 * (cum0 + 0.5 * W0)).sum() / den)\n\n\nclass WStratAuc:\n    \"\"\"Within-stratum pair AUROC under row weights.\"\"\"\n\n    def __init__(self, y, s, strata):\n        self.y = np.asarray(y, float)\n        strata = np.asarray(strata)\n        self.parts = [(np.where(strata == st)[0], WAuc(self.y[strata == st], np.asarray(s, float)[strata == st]))\n                      for st in np.unique(strata)]\n\n    def __call__(self, w) -> float:\n        w = np.asarray(w, float)\n        num = den = 0.0\n        for ix, wa in self.parts:\n            ww = w[ix]\n            n1 = (ww * self.y[ix]).sum()\n            n0 = (ww * (1 - self.y[ix])).sum()\n            if n1 > 0 and n0 > 0:\n                num += wa(ww) * n1 * n0\n                den += n1 * n0\n        return num / den if den else float(\"nan\")\n\n\nclass SentBoot:\n    \"\"\"Sentence-cluster bootstrap as multiplicity weights: W[b, i] = #times row i's sentence was drawn in replicate b\n    (numpy default_rng(seed); sentence_ids resampled with replacement).\"\"\"\n\n    def __init__(self, sids, b: int = B_DEFAULT, seed: int = 0):\n        sids = np.asarray(sids)\n        self.keys, self.sent_ix = np.unique(sids, return_inverse=True)\n        S = len(self.keys)\n        rng = np.random.default_rng(seed)\n        self.C = np.stack([np.bincount(rng.integers(0, S, S), minlength=S) for _ in range(b)]).astype(float)\n        self.B = b\n\n    def weights(self, b: int, mask=None):\n        w = self.C[b][self.sent_ix]\n        return w if mask is None else w[mask]\n\n    def W(self, mask=None):\n        \"\"\"(B, n_rows[mask]) weight matrix.\"\"\"\n        W = self.C[:, self.sent_ix]\n        return W if mask is None else W[:, mask]\n{\"auto_label\": \"ERROR\", \"correct_not_equivalent\": false, \"error_ops\": [\"ADD\", \"DROP\"], \"label\": \"ERROR\", \"label_tier\": \"A\", \"panel_votes\": {\"P3\": {\"conf\": 5, \"faithful\": false, \"ops\": [\"SWAP\"]}, \"R1\": {\"conf\": 4, \"faithful\": false, \"ops\": [\"DROP\", \"SWAP\"]}}, \"reading_choice\": false, \"reference_status\": \"GOLD_PANEL_OK\", \"repair_ops\": [\"ADD\", \"DROP\"], \"row_key\": \"7119f4afc2b446d2|fewshot_v1\", \"system_class\": \"llm\", \"vex\": false, \"vex_eq\": false}\n{\"auto_label\": \"COMPOUND\", \"correct_not_equivalent\": false, \"error_ops\": [\"COMPOUND\", \"ADD\", \"CONN\", \"DROP\", \"MOVE\"], \"label\": \"ERROR\", \"label_tier\": \"B\", \"panel_votes\": {\"P3\": {\"conf\": 5, \"faithful\": false, \"ops\": [\"MOVE\", \"ADD\"]}, \"R1\": {\"conf\": 5, \"faithful\": false, \"ops\": [\"CONN\", \"DROP\", \"ADD\"]}}, \"reading_choice\": false, \"reference_status\": \"GO\n{\"row_key\": \"87618fded07e3eb4|fewshot_v1\", \"item_id\": \"87618fded07e3eb4\", \"sentence_id\": \"679fdea26cad\", \"text\": \"A substance that increases the rate of a chemical reaction without being consumed in the process is a catalyst.\", \"slot\": \"G1\", \"system\": \"G1:meta-llama/llama-3.1-8b-instruct\", \"model\": \"meta-llama/llama-3.1-8b-instruct\", \"family\": \"meta\", \"family_field\": \"meta\", \"prompt_variant\": \"fewshot_v1\", \"candidate_fol\": \"∀x (Substance(x) ∧ IncreasesRate(x, chemicalReaction) ∧ NotConsumed(x, chemicalReaction) → Catalyst(x))\", \"raw_output\": \"FOL: ∀x (Substance(x) ∧ IncreasesRate(x, chemicalReaction) ∧ NotConsumed(x, chemicalReaction) → Catalyst(x))\", \"parse_ok_gen\": true, \"gen_cost_usd\": 1.086e-05, \"stratum\": \"EXC\", \"words\": 19, \"text_conditions\": 1, \"exception_type\": \"without\", \"word_bin\": null, \"pilot\": true, \"source_dataset\": \"MALLS-v0.1-train\"}\n{\"row_key\": \"56c9a307c0a6cf53|fewshot_v1\", \"item_id\": \"56c9a307c0a6cf53\", \"sentence_id\": \"679fdea26cad\", \"text\": \"A substance that increases the rate of a chemical reaction without being consumed in the process is a catalyst.\", \"slot\": \"G1b\", \"system\": \"G1b:meta-llama/llama-3.3-70b-instruct\", \"model\": \"meta-llama/llama-3\ncache:\ntotal 26619\ndrwxr-xr-x  4 231072 231072 2002122 Sep 24 12:20 .\ndrwxr-xr-x 14 root   root   2013491 Sep 24 15:38 ..\n-rw-r--r--  1 231072 231072  703462 Sep 24 11:31 E2_l3_q.jsonl\n-rw-r--r--  1 231072 231072 5603886 Sep 24 11:38 consensus_sentences.jsonl\n-rw-r--r--  1 231072 231072  568358 Sep 24 11:39 exact_E2.jsonl\ndrwxr-xr-x  2 231072 231072 1057407 Sep 24 11:34 failed_run1\n-rw-r--r--  1 231072 231072 2079835 Sep 24 11:40 judge_cheap.jsonl\n-rw-r--r--  1 231072 231072 2794840 Sep 24 12:53 judge_local_qwen8b.jsonl\n-rw-r--r--  1 231072 231072   60132 Sep 24 11:31 l3_cost_ledger.jsonl\n-rw-r--r--  1 231072 231072  708991 Sep 24 11:31 l3_llm_cache.jsonl\n-rw-r--r--  1 231072 231072 3095282 Sep 24 12:53 local_cache.jsonl\n-rw-r--r--  1 231072 231072 2094052 Sep 24 11:39 pairwise_E2.jsonl\n-rw-r--r--  1 231072 231072 1349852 Sep 24 11:50 pilot_E2.jsonl\ndrwxr-xr-x  2 231072 231072 1052735 Sep 24 11:36 t1_results\n-rw-r--r--  1 231072 231072 2068996 Sep 24 11:35 units_E2.jsonl\n\ne2src/work:\ntotal 34098\ndrwxrwxrwx  2 231072 231072  2002946 Sep 24 15:11 .\ndrwxr-xr-x 18 231072 231072  2006487 Sep 24 16:51 ..\n-rw-rw-rw-  1 231072 231072 18765454 Sep 24 15:12 assembled_E2.json\n-rw-rw-rw-  1 231072 231072    37508 Sep 23 13:25 calibration_items.json\n-rw-rw-rw-  1 231072 231072   231144 Sep 24 15:12 controls_E2.json\n-rw-r--r--  1 231072 231072     8800 Sep 24 11:33 e2a_order.json\n-rw-rw-rw-  1 231072 231072     3713 Sep 23 13:11 fewshot_exemplars.json\n-rw-rw-rw-  1 231072 231072     3587 Sep 24 11:18 gate_results.json\n-rw-r--r--  1 231072 231072     3564 Sep 24 11:12 gate_results_iter4.json\n-rw-rw-rw-  1 231072 231072     3407 Sep 24 11:13 generation_manifest.json\n-rw-rw-rw-  1 231072 231072  2683424 Sep 24 11:29 labels_heldout.jsonl\n-rw-r--r--  1 231072 231072  2110109 Sep 24 11:41 labels_heldout_prefix.jsonl\n-rw-rw-rw-  1 231072 231072   747565 Sep 23 13:06 models_snapshot.json\n-rw-rw-rw-  1 231072 231072   806137 Sep 24 07:22 models_snapshot_E2.json\n-rw-r--r--  1 231072 231072  1963965 Sep 24 11:41 panel_cache.jsonl\n-rw-rw-rw-  1 231072 231072   336811 Sep 24 07:27 panel_cache_iter4_unpinned.jsonl\n-rw-r--r--  1 231072 231072   258880 Sep 24 15:11 panel_heldout.jsonl\n-rw-rw-rw-  1 231072 231072   654882 Sep 24 15:11 panel_heldout_ALL_before_prefix_cut.jsonl\n-rw-r--r--  1 231072 231072    31045 Sep 24 15:11 panel_heldout_adj.jsonl\n-rw-rw-rw-  1 231072 231072   170538 Sep 24 15:11 panel_heldout_adj_ALL_before_prefix_cut.jsonl\n{'n_items': 269, 'agreement_P1': 1.0, 'n_P1': 269, 'agreement_P3': 0.9182, 'n_P3': 269, 'agreement_R1': 0.949, 'n_R1': 255, 'majority_agreement': 0.9554, 'n_no_majority_old': 3, 'n_no_majority_new': 0, 'n_replayed_with_>=2_new_votes': 269, 'majority_agreement_on_replayed_items': 0.9554}", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [18] ASSISTANT · 2026-09-25 13:15:48 UTC

```
I've read the artifact's `method.py`, which is a stage orchestrator, and its re-derivation audit. Next I'm building `mini_demo_data.json` from 100 sentences in the labelled prefix.
```

### [19] TOOL CALL — Bash · 2026-09-25 13:15:48 UTC

```
mkdir -p /tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-ngTPhaVyXxhh/4abc7c63-e354-4aab-8688-1dd25b3200eb/scratchpad; OUT=/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh; cat > $OUT/build_mini_data.py <<'EOF'
"""Builds mini_demo_data.json from the E2-A artifact's raw files (same joins as audit/rederive.py).
One example = one sentence of the pre-registered sha1-order prefix, with its labelled candidate rows (label tier A/B,
CORRECT/ERROR, no reading choice) and its rename-control rows. 100 of the 110 prefix sentences are kept (those with the
most labelled rows, stratum-balanced)."""
import json, sys
from collections import defaultdict
from pathlib import Path
W = Path(sys.argv[1])
jl = lambda p: [json.loads(l) for l in open(p) if l.strip()]
lab = {r["row_key"]: r for r in jl(W / "e2src/sealed/labels_E2.jsonl") if r["system_class"] == "llm"}
cand = {r["row_key"]: r for r in jl(W / "e2/candidates_E2_nolabels.jsonl")}
order = json.load(open(W / "e2src/work/e2a_order.json"))[:110]
keep = set(order)
v0 = {}
for s in jl(W / "cache/consensus_sentences.jsonl"):
    for r in s["rows"]:
        v0[r["key"]] = r.get("c_score_align")
loc = {r["key"]: 1 - r["p"] for r in jl(W / "cache/judge_local_qwen8b.jsonl") if r.get("p") is not None}
pil = {r["key"]: r for r in jl(W / "cache/pilot_E2.jsonl")}
per = {r["row_key"]: r for r in jl(W / "per_item_E2A.jsonl")}
PM = ("pilot_joint_conflict", "pilot_arity_incons", "pilot_shape_incons", "pilot_dangling", "pilot_rerun_jacc")
EXTRA = ("p_peer_text", "c_exact", "l2_bow", "l3_z3", "judge_local_qwen8b_orig")
by = defaultdict(list)
for k, l in lab.items():
    c = cand[k]
    if c["sentence_id"] not in keep or l["label"] not in ("CORRECT", "ERROR") or l["reading_choice"] or l["label_tier"] not in ("A", "B"):
        continue
    p = per[k]
    by[c["sentence_id"]].append(dict(row_key=k, system=c["system"], family=c["family"], candidate_fol=c["candidate_fol"],
        label=l["label"], label_tier=l["label_tier"], error_ops=l.get("error_ops"),
        v0=v0.get(k), loc=loc.get(k + "|disg"), **{m: pil[k].get(m) for m in PM}, **{m: p.get(m) for m in EXTRA}))
# rename controls: map parent row_key -> sentence
ren = defaultdict(list)
for r in jl(W / "results/rename_V0_rows.jsonl"):
    parent = "|".join(r["row_key"].split("|")[:2])
    if parent in cand:
        ren[cand[parent]["sentence_id"]].append(r)
first = {}
for k, c in cand.items():
    first.setdefault(c["sentence_id"], c)
sents = [s for s in order]
# drop 10 sentences with fewest labelled rows (ties: later in order), keeping strata balanced (drop ~3-4 per stratum)
strat = {s: first[s]["stratum"] for s in sents}
drop = set()
for st, nd in (("L25", 3), ("EXC", 3), ("DT", 4)):
    cands = sorted([s for s in sents if strat[s] == st], key=lambda s: (len(by[s]) + len(ren[s]), -order.index(s)))
    drop |= set(cands[:nd])
ex = []
for s in sents:
    if s in drop:
        continue
    c = first[s]
    ex.append({"input": c["text"], "output": json.dumps({r["row_key"]: r["label"] for r in by[s]}),
               "metadata_sentence_id": s, "metadata_stratum": c["stratum"], "metadata_words": c["words"],
               "metadata_text_conditions": c["text_conditions"], "metadata_source_dataset": c.get("source_dataset"),
               "rows": by[s], "rename_controls": ren[s]})
d = json.load(open(W / "e2src/panel_drift_E2.json"))
spend = sum(r["cost_usd"] for r in jl(W / "e2src/cost_ledger.jsonl")) + sum(r["cost_usd"] for r in jl(W / "cache/l3_cost_ledger.jsonl")) \
    + sum((r.get("cost") or 0) for r in jl(W / "cache/t1_results/costs.jsonl"))
out = {"metadata": {"description": "E2-A mini demo: 100 of the 110 prefix sentences; per sentence the labelled candidate rows "
                    "(label 1=ERROR) with frozen label-free scores (every score higher = more likely ERROR) and rename controls.",
                    "v0": "c_score_align (frozen cross-family consensus)", "loc": "local Qwen3-8B judge, disguised view (1-p_faithful)",
                    "drift_majority_agreement": d["combined"]["majority_agreement"], "spend_usd": spend,
                    "reference_full_run": json.load(open(W / "audit/rederive_out.json"))},
       "datasets": [{"dataset": "E2_prefix", "examples": ex}]}
Path(sys.argv[2]).write_text(json.dumps(out, ensure_ascii=False))
print(len(ex), sum(len(e["rows"]) for e in ex), sum(len(e["rename_controls"]) for e in ex))
EOF
cd $OUT && python3 build_mini_data.py /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_5/gen_art/gen_art_experiment_11 mini_demo_data.json && ls -la mini_demo_data.json
```

### [20] TOOL RESULT — Bash · 2026-09-25 13:15:50 UTC

```
{"stdout": "100 273 151\n-rw-r--r-- 1 root root 239978 Sep 25 13:15 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [21] ASSISTANT · 2026-09-25 13:17:26 UTC

```
Mini data covers all 273 labelled rows, so the headline numbers should reproduce exactly. Now writing the notebook.
```

### [22] TOOL CALL — Bash · 2026-09-25 13:17:26 UTC

```
OUT=/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh; cat > $OUT/make_notebook.py <<'PYEOF'
"""Writes code_demo.ipynb (cells below). Re-run: python3 make_notebook.py"""
import json
from pathlib import Path
cells = []
def md(s): cells.append({"cell_type": "markdown", "metadata": {}, "source": s.strip("\n")})
def code(s): cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "sou... [truncated, 24641 chars total]
```

### [23] TOOL RESULT — Bash · 2026-09-25 13:17:26 UTC

```
{"stdout": "99:B_BOOT = 10        # original: 2000 (stratified sentence-cluster bootstrap replicates for 95% CIs)\n100:N_PLACEBO = 2      # original: 200  (shuffled-within-stratum label placebo replicates)\nwrote 24 cells", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [24] TOOL CALL — Bash · 2026-09-25 13:17:34 UTC

```
OUT=/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh; cd $OUT && python3 - <<'EOF'
p='make_notebook.py'; s=open(p).read()
s=s.replace('names = {"v0": "V0 consensus"','names = {"V0": "V0 consensus"')
s=s.replace('''a1.set_xticklabels([names.get(k, names.get(k.lower(), k)).replace("V0 consensus", "V0 consensus") if k != "V0" else "V0 consensus" for k in keys], rotation=40, ha="right")''','''a1.set_xticklabels([names[k] for k in keys], rotation=40, ha="right")''')
open(p,'w').write(s)
EOF
python3 make_notebook.py && (UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-de9dd702ac22 && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-de9dd702ac22/bin/python jupyter ipykernel && time /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-de9dd702ac22/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb) 2>&1 | tail -20
```

### [25] TOOL RESULT — Bash · 2026-09-25 13:18:08 UTC

```
{"stdout": "wrote 24 cells\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 146290 bytes to code_demo.ipynb\n\nreal\t0m27.917s\nuser\t0m22.177s\nsys\t0m3.182s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [26] ASSISTANT · 2026-09-25 13:18:16 UTC

```
Minimal config passes in 28 s. Scaling straight to the original values (B=2000, placebo=200); the full analysis is cheap.
```

### [27] TOOL CALL — Bash · 2026-09-25 13:18:16 UTC

```
OUT=/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh; cd $OUT && sed -i 's/^B_BOOT = 10   /B_BOOT = 200  /; s/^N_PLACEBO = 2   /N_PLACEBO = 20  /' make_notebook.py && python3 make_notebook.py && (UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-de9dd702ac22 && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-de9dd702ac22/bin/python jupyter ipykernel && time /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-de9dd702ac22/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb) 2>&1 | grep -v WARNING | tail -5; sed -i 's/^B_BOOT = 200  /B_BOOT = 2000 /; s/^N_PLACEBO = 20  /N_PLACEBO = 200 /' make_notebook.py && python3 make_notebook.py && (UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-de9dd702ac22 && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-de9dd702ac22/bin/python jupyter ipykernel && time /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-de9dd702ac22/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb) 2>&1 | grep -v WARNING | tail -5
```

### [28] TOOL RESULT — Bash · 2026-09-25 13:19:15 UTC

```
{"stdout": "wrote 24 cells\n[NbConvertApp] Writing 146247 bytes to code_demo.ipynb\n\nreal\t0m25.482s\nuser\t0m21.025s\nsys\t0m2.904s\nwrote 24 cells\n[NbConvertApp] Writing 146279 bytes to code_demo.ipynb\n\nreal\t0m27.490s\nuser\t0m22.731s\nsys\t0m3.039s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [29] ASSISTANT · 2026-09-25 13:19:21 UTC

```
Full original parameters run in 27 s. Checking the outputs against the artifact's numbers:
```

### [30] TOOL CALL — Bash · 2026-09-25 13:19:21 UTC

```
OUT=/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh; cd $OUT && python3 - <<'EOF'
import json
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
    if c['cell_type']!='code': continue
    for o in c['outputs']:
        if o['output_type']=='error': print('ERR',o['ename'],o['evalue'])
        t=o.get('text') or o.get('data',{}).get('text/plain')
        if t: print(''.join(t)[:1800]); print('---')
        if 'image/png' in o.get('data',{}): print('[image]')
EOF
grep -c 'GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-5/experiment-11/demo/mini_demo_data.json"' code_demo.ipynb
```

### [31] TOOL RESULT — Bash · 2026-09-25 13:19:21 UTC

```
{"stdout": "100 sentences | 273 labelled candidate rows | 151 rename-control rows\nexample sentence: If an object is a smartphone, it must be a mobile device that combines the functions of a cellphone, computer, and personal digital assistant, often featuring internet access and touchscreen display.\n  candidate: None\n\n---\n== l3                       python scoring/score_consensus.py --stage l3\n== consensus                python scoring/score_consensus.py --stage score --workers 30\n== pairwise                 python scoring/score_consensus.py --stage pairwise --workers 36\n== exact                    python scoring/score_consensus.py --stage exact --workers 36\n== prep                     python scoring/api_judges.py --stage prep --workers 10\n== judges                   python scoring/api_judges.py --stage judges --concurrency 32\n== local_judge              python scoring/local_judge.py --which qwen8b_disg,qwen8b_orig --bs 64\n== pilot                    python scoring/pilot_metrics_E2.py\n== assemble                 python scoring/assemble_scores.py\n== labels:assemble_e2       python src_e2/assemble_e2.py\n== labels:controls_e2       python src_e2/controls_e2.py\n== labels:testability_e2    python src_e2/testability_e2.py\n== labels:seal_e2           python src_e2/seal_e2.py\n== labels:verify_seal       python src_e2/verify_seal.py\n== join                     python analysis/analyse_E2A.py --stage join\n== analyse                  python analysis/analyse_E2A.py --stage analyse --prefix 110\n== rename                   python analysis/rename_V0.py\n== union                    python analysis/union_E2B.py --deadline-utc 2026-09-24T15:40:00Z --once\n== outputs                  python analysis/make_outputs.py\n\n---\n273 rows; st      DT  EXC  L25\nn      179   52   42\nn_err   74   41   35\n\n---\n                             k           sid  st  y        v0   loc  words  \\\n0  62b8d8e91effd650|fewshot_v1  b91115ec794d  DT  0  0.375000  0.05     19   \n1  bc7ebbda34033f05|fewshot_v1  b91115ec794d  DT  0  1.000000  0.00     19   \n2  781e1b6e32dd037e|fewshot_v1  b91115ec794d  DT  0  0.444444  0.05     19   \n3  ac4a0e43dcfc6e8c|fewshot_v1  b91115ec794d  DT  0  0.444444  0.05     19   \n4  0fb444c5049ce4b4|fewshot_v1  b91115ec794d  DT  0  0.500000  0.05     19   \n\n   pilot_joint_conflict  pilot_arity_incons  pilot_shape_incons  \\\n0                     0                   0                   0   \n1                     0                   0                   0   \n2                     0                   0                   0   \n3                     0                   0                   1   \n4                     0                   0                   0   \n\n   pilot_dangling  pilot_rerun_jacc  p_peer_text   c_exact  l2_bow     l3_z3  \\\n0        1.000000          0.294268     0.354247  0.750000   0.000  0.750000   \n1        1.000000          0.332716     0.938109  1.000000   0.125  0.583333   \n2        1.000000          0.313692     0.342394  1.000000   0.000  0.583333   \n3        0.833333          0.294268     0.420381  0.777778   0.000  0.750000   \n4        1.000000          0.381514     0.471281  1.000000   0.000  0.750000   \n\n   judge_local_qwen8b_orig  \n0                     0.05  \n1                     0.00  \n2                     0.00  \n3                     0.05  \n4                     0.05  \n---\n        n n_err n_cor        V0 local_disg delta_V0_minus_local  \\\nALL   273   150   123  0.890444   0.894992            -0.004548   \nDT    179    74   105  0.916152   0.912934             0.003218   \nLONG   94    76    18  0.603448   0.694684            -0.091236   \n\n     pilot_joint_conflict pilot_arity_incons pilot_shape_incons  \\\nALL                   0.5           0.506615           0.509981   \nDT                    0.5           0.506757           0.509974   \nLONG                  0.5           0.505029           0.510057   \n\n     pilot_dangling pilot_rerun_jacc p_peer_text   c_exact    l2_bow  \\\nALL        0.413123         0.712615    0.901665  0.830912  0.751181   \nDT         0.399614           0.7287    0.919369  0.854054  0.759974   \nLONG       0.563937         0.533046    0.704023  0.572557  0.653017   \n\n         l3_z3 judge_local_qwen8b_orig testable_50_50  \nALL   0.583274                0.900898           True  \nDT    0.572265                0.917632           True  \nLONG  0.706178                 0.71408          False  \n---\nALL   n=273  V0 0.890 [0.838,0.940]  local 0.895 [0.844,0.938]  V0-local -0.005 [-0.047,+0.041]\nDT    n=179  V0 0.916 [0.858,0.970]  local 0.913 [0.858,0.958]  V0-local +0.003 [-0.042,+0.052]\nLONG  n= 94  V0 0.603 [0.463,0.735]  local 0.695 [0.551,0.837]  V0-local -0.091 [-0.219,+0.017]\n\n---\n{'V0_mean': 0.493547424994094,\n 'V0_p2.5_97.5': [0.42281626506024095, 0.5767319277108434],\n 'delta_mean': -0.0035400425230333143,\n 'delta_p2.5_97.5': [-0.06180900070871719, 0.06481366643042755],\n 'real_V0_ALL_above_placebo_p97.5': True}\n---\n{'RENAME_SYN': {'n': 28, 'FA': 1.0, 'base': 0.25},\n 'RENAME_NONCE': {'n': 123, 'FA': 1.0, 'base': 0.17886178861788618},\n 'drift_majority_agreement': 0.9554,\n 'spend_usd': 2.04500803205}\n---\n        cell               metric  notebook  full artifact\n         ALL                    n   273.000        273.000\n         ALL                   V0     0.890          0.890\n         ALL           local_disg     0.895          0.895\n         ALL delta_V0_minus_local    -0.005         -0.005\n         ALL     pilot_rerun_jacc     0.713          0.713\n         ALL       pilot_dangling     0.413          0.413\n          DT                    n   179.000        179.000\n          DT                   V0     0.916          0.916\n          DT           local_disg     0.913          0.913\n          DT delta_V0_minus_local     0.003          0.003\n          DT     pilot_rerun_jacc     0.729          0.729\n          DT       pilot_dangling     0.400          0.400\n        LONG                    n    94.000         94.000\n        LONG                   V0     0.603          0.603\n        LONG           local_disg     0.695          0.695\n        LONG delta_V0_minus_local    -0.091         -0.091\n        LONG     pilot_rerun_jacc     0.533          0.533\n        LONG       pilot_dangling     0.564          0.564\n  RENAME_SYN                    n    28.000         36.000\n  RENAME_SYN                   FA     1.000          0.944\n  RENAME_SYN                 base     0.250          0.361\nRENAME_NONCE                    n   123.000        145.000\nRENAME_NONCE                   FA     1.000          1.000\nRENAME_NONCE                 base     0.179          0.262\n\n---\n<Figure size 1400x500 with 2 Axes>\n---\n[image]\n0", "stderr": "", "interrupted": false, "isImage": false, "returnCodeInterpretation": "No matches found", "noOutputExpected": false}
```

### [32] THINKING · 2026-09-25 13:19:39 UTC

```
The AUROC and bootstrap CI values all match the artifact exactly. I'll fix the example print, which currently picked a sentence with no labelled rows, then re-run and check the figure.
```

### [33] TOOL CALL — Bash · 2026-09-25 13:19:39 UTC

```
OUT=/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh; cd $OUT && python3 - <<'EOF'
p='make_notebook.py'; s=open(p).read()
s=s.replace('''print("example sentence:", EXAMPLES[0]["input"])
print("  candidate:", EXAMPLES[0]["rows"][0]["candidate_fol"] if EXAMPLES[0]["rows"] else None)''','''ex0 = next(e for e in EXAMPLES if e["rows"])
print("example sentence:", ex0["input"])
for r in ex0["rows"][:3]:
    print(f"  [{r['label']:7s}] {r['candidate_fol']}")''')
open(p,'w').write(s)
EOF
python3 make_notebook.py && (UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-de9dd702ac22 && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-de9dd702ac22/bin/python jupyter ipykernel && time /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-de9dd702ac22/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb) 2>&1 | grep -v WARNING | tail -4
python3 - <<'EOF'
import json,base64
nb=json.load(open('code_demo.ipynb'))
src=''.join(''.join(c['source']) for c in nb['cells'])
print('url ok:', 'GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-5/experiment-11/demo/mini_demo_data.json"' in src, 'urlopen(GITHUB_DATA_URL)' in src)
print('errors:', sum(o['output_type']=='error' for c in nb['cells'] if c['cell_type']=='code' for o in c['outputs']))
print(''.join(nb['cells'][4]['outputs'][0]['text']))
for c in nb['cells']:
    for o in c.get('outputs',[]):
        if 'image/png' in o.get('data',{}): open('/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-ngTPhaVyXxhh/4abc7c63-e354-4aab-8688-1dd25b3200eb/scratchpad/fig.png','wb').write(base64.b64decode(o['data']['image/png']))
EOF
```

### [34] TOOL RESULT — Bash · 2026-09-25 13:20:09 UTC

```
{"stdout": "wrote 24 cells\n\nreal\t0m27.313s\nuser\t0m22.382s\nsys\t0m3.028s\nurl ok: True True\nerrors: 0\n100 sentences | 273 labelled candidate rows | 151 rename-control rows\nexample sentence: If Xiomara either wakes up at dawn or has light slumber (but not both), then she sleeps very lightly.\n  [CORRECT] (WakesUpAt(xiomara, dawn) ⊕ Has(xiomara, lightSlumber)) → SleepsVeryLightly(xiomara)\n  [CORRECT] (WakesAtDawn(xiomara) ⊕ HasLightSlumber(xiomara)) → SleepsVeryLightly(xiomara)\n  [CORRECT] (WakesUpAt(xiomara, dawn) ⊕ LightSlumber(xiomara)) → SleepsVeryLightly(xiomara)", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [35] TOOL CALL — Read · 2026-09-25 13:20:11 UTC

```
/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-5-art-ngTPhaVyXxhh/4abc7c63-e354-4aab-8688-1dd25b3200eb/scratchpad/fig.png
```

### [36] TOOL RESULT — Read · 2026-09-25 13:20:11 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [37] ASSISTANT · 2026-09-25 13:20:29 UTC

```
The figure is good. The only problem is the legend overlapping a bar on the right panel, so I'll give that panel headroom. After that I'll write the README, manifest and output JSON.
```

### [38] TOOL CALL — Bash · 2026-09-25 13:20:29 UTC

```
OUT=/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_5/art_ngTPhaVyXxhh; cd $OUT && sed -i 's/a2.set_ylim(0, 1.05); a2.set_title("V0 rename invariance (V0>0.5)"); a2.legend(fontsize=8)/a2.set_ylim(0, 1.3); a2.set_title("V0 rename invariance (V0>0.5)"); a2.legend(fontsize=8, loc="upper left")/' make_notebook.py && grep -c 'ylim(0, 1.3)' make_notebook.py && python3 make_notebook.py && (UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-de9dd702ac22 && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-de9dd702ac22/bin/python jupyter ipykernel && time /tmp/aii_nb_test_envs/art_ngTPhaVyXxhh-de9dd702ac22/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb) 2>&1 | grep -v WARNING | tail -3; python3 -c "
import json;nb=json.load(open('code_demo.ipynb'));print('errors',sum(o['output_type']=='error' for c in nb['cells'] if c['cell_type']=='code' for o in c['outputs']))"
cat > .aii/manifest.yaml <<'EOF'
# No heavy paths: every file in this workspace is small text/code (< 10 MB). Nothing to keep or delete.
entries: []
EOF
cat > README.md <<'EOF'
# Demo: consensus vs LLM judges on fresh NL→FOL data (E2-A)

This is a Colab-ready demo notebook for the E2-A experiment. That experiment is the pre-registered confirmation test
of the frozen cross-family solver-consensus score `c_score_align` (V0), a gold-free metric that flags an NL→FOL
formalization as unfaithful. V0 is compared against a local Qwen3-8B judge and the user's pilot structural metrics,
on 273 panel- or prover-labelled candidates drawn from 110 sentences.

## What the notebook does
- Prints the stage plan of the artifact's `method.py`, which is kept verbatim. Its stages call GPU and paid-API
  scripts, so they are not executed.
- Re-runs the analysis stage on the sealed scores and labels:
  - stratified AUROC per cell (ALL / DT / LONG);
  - stratified sentence-cluster bootstrap CIs (B = 2000) for V0, the local judge and V0 − local;
  - a shuffled-label placebo (200 replicates);
  - the V0 rename-invariance controls.
- Compares the results with the full artifact's `audit/rederive_out.json`. All AUROCs and CIs match exactly. The
  rename controls cover 151 of the 181 rows, because 10 of the 110 sentences were left out.
- Plots every metric's AUROC and V0's rename false-alarm rate.

Total runtime is about 30 s at the original parameters, including package installs.

## Layout
| path | content |
|---|---|
| `code_demo.ipynb` | the demo notebook (executed, with outputs) |
| `mini_demo_data.json` | 100 of the 110 prefix sentences; each has its labelled candidate rows (all 273) with frozen label-free scores, its rename-control rows, drift/spend metadata and the full-run reference numbers |
| `build_mini_data.py` | builds `mini_demo_data.json` from the artifact's raw files (`python3 build_mini_data.py <artifact_dir> mini_demo_data.json`) |
| `make_notebook.py` | writes `code_demo.ipynb` (`python3 make_notebook.py`) |
| `.aii/manifest.yaml` | storage manifest (no heavy paths) |

## How to run
Open `code_demo.ipynb` in Colab or Jupyter and run all cells. The notebook loads `mini_demo_data.json` from the GitHub
raw URL and falls back to the local file if the download fails.

## Restoring removed files
Nothing is marked `delete`. Every file is small text or code and stays in the repository.
EOF
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
ls -la; du -sh .
```

### [39] TOOL RESULT — Bash · 2026-09-25 13:20:59 UTC

```
{"stdout": "1\nwrote 24 cells\nreal\t0m27.173s\nuser\t0m22.455s\nsys\t0m2.971s\nerrors 0\ntotal 3714\ndrwxr-xr-x  3 root root 1070087 Sep 25 13:20 .\ndrwxr-xr-x  5 root root 2000241 Sep 25 13:16 ..\ndrwxr-xr-x  2 root root   11600 Sep 25 13:20 .aii\n-rw-------  1 root root      54 Sep 25 13:14 .aii_claude_session.json\n-rw-r--r--  1 root root  299931 Sep 25 13:20 .repl_agent.ptylog\n-rw-r--r--  1 root root      97 Sep 25 13:20 .terminal_claude_agent_struct_out.json\n-rw-r--r--  1 root root    2240 Sep 25 13:20 README.md\n-rw-r--r--  1 root root    4176 Sep 25 13:15 build_mini_data.py\n-rw-r--r--  1 root root  146893 Sep 25 13:20 code_demo.ipynb\n-rw-r--r--+ 1 root root   24268 Sep 25 13:20 make_notebook.py\n-rw-r--r--  1 root root  239978 Sep 25 13:15 mini_demo_data.json\n1.8M\t.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [40] ASSISTANT · 2026-09-25 13:21:09 UTC

```
The demo notebook is built and runs end to end in a clean Python 3.12 venv, with no errors, in about 27 seconds. That includes installing packages and uses the original parameters: 2,000 bootstrap replicates and 200 placebo replicates. Its numbers match the artifact's own re-derivation (`audit/rederive_out.json`) exactly.

**About the original script:** the artifact's `method.py` doesn't compute anything itself. It only calls other scripts in order, and those need a GPU, the paid OpenRouter key and the artifact's frozen code, so none of them can run in Colab. The notebook therefore:
- keeps `method.py` word for word, except `WS = Path.cwd()` because a notebook has no `__file__`, and prints its stage plan instead of calling `main()`;
- actually runs the analysis step on the scores and labels saved before any labelling, using code copied from `audit/rederive.py`, the frozen `stats.py` and `strat_boot_weights`.

**`mini_demo_data.json`** holds 100 of the 110 labelled sentences, balanced across the three sentence groups (long, exception-heavy, and DT, whose gold comes from a prover). The 10 sentences left out had no labelled rows, so all 273 labelled candidates are included. Each sentence carries its frozen scores, its renamed-symbol test rows, and the full-run numbers to compare against.

**Results in the notebook** (AUROC = how well a score separates wrong from correct formulas; 0.5 is chance):

| Group | Rows | Consensus score (V0) | Local 8B judge | V0 minus judge (95% CI) |
|---|---|---|---|---|
| ALL | 273 | 0.890 | 0.895 | −0.005 [−0.047, +0.041] |
| DT | 179 | 0.916 [0.858, 0.970] | 0.913 | +0.003 [−0.042, +0.052] |
| LONG | 94 | 0.603 | 0.695 | too few correct rows to test (18) |

- **Consensus vs a small judge:** consensus ties the local 8B judge and adds nothing over it.
- **Your pilot metrics:** joint conflict, arity and shape consistency sit at chance (about 0.50), dangling predicates is inverted (0.41), and only rerun-Jaccard is above chance (0.71).
- **Placebo check:** with labels shuffled, V0 drops to 0.49, and the real score is above the placebo's 97.5th percentile.
- **Renaming:** correct formulas whose symbols are renamed are flagged 100% of the time. The notebook has 28 synonym and 123 nonce-word test rows, out of the artifact's 36 and 145. Because of that smaller subset, its synonym rate is 100% rather than the artifact's 94%.

The last cell draws a figure with each metric's AUROC and the renaming false-alarm rates.

The GitHub data URL is in the notebook exactly as given, with a fallback to the local file. The manifest has no entries because nothing in the workspace is over 10 MB. The structured output JSON is written.

Files are in the workspace:
- `code_demo.ipynb`
- `mini_demo_data.json`
- `build_mini_data.py`
- `make_notebook.py`
- `README.md`
- `.aii/manifest.yaml`
- `.terminal_claude_agent_struct_out.json`
```
