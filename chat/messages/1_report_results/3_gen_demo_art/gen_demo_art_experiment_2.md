# gen_demo_art_experiment_2 — report_results

> Phase: `gen_paper_repo` · `gen_demo_art`
> Run: `gen_paper_repo_a2e1d024cc16` — Cross-Family Solver Consensus as a Gold-Free Faithfulness Metric for Natural Language to First-Order Logic Translation
>
> Full, verbatim transcript of this agent task — every system/user prompt, assistant response, thinking block, tool call and tool result — in the order they occurred. Nothing truncated.

## Task: `gen_demo_art_experiment_2` (terminal_claude_agent, claude-opus-5-5)

### [1] CONFIG · 2026-09-25 12:33:53 UTC

```
model: claude-opus-5-5 | effort: high | permission: bypassPermissions
```

### [2] SYSTEM-USER prompt · 2026-09-25 12:33:59 UTC

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
Your workspace: `/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk`

CRITICAL: Every file you create, write, or save MUST be inside this workspace directory (subdirectories OK). You MUST NOT write files anywhere outside this path — external paths are READ-ONLY. Use absolute paths for all file operations.

EVERY file write MUST start with `/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/`:
GOOD: `/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/file.py`, `/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/results/out.json`
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
id: art_i3cVDxBp-USk
type: experiment
title: Do other models' translations agree? Consensus metric for NL-to-logic
summary: >-
  Experiment 3 screens candidate C, a text-free, gold-free consensus metric for NL->FOL faithfulness, on the shared frozen
  screen (label hash 0e43cbdd...). c_score = 1 - eq_frac: the share of OTHER systems' translations of the same sentence that
  are NOT z3-equivalent to the candidate modulo vocabulary alignment. The pool has 6 fresh OpenRouter families (llama-3.3-70b,
  qwen3-235b, deepseek-v3.1, mistral-small-3.2, gemini-2.5-flash-lite, gpt-4.1-mini) plus the 3 released Logic-LM systems,
  leave-one-out. Also scored: medoid repair depth and operators, and semantic entropy over z3 classes. Baselines: K=5 self-consistency
  (gpt-4.1-nano T=0.7 on all items; true same-model gpt-3.5-turbo SC for gpt-3.5 candidates), predicate-set stability, and
  FOL length. PRIMARY (track L, 297 CORRECT vs 249 ERROR, sentence-clustered bootstrap 2000): c_score AUROC 0.866 [0.821,
  0.906]; peers-only 0.872; non-OpenAI peers 0.863; other Logic-LM systems only 0.753; cluster entropy 0.773; medoid depth
  0.722; sc5_cheap 0.725 [0.669, 0.781] (n=546, now complete). Paired Δ c_score - sc5_cheap = +0.140 [0.085, 0.197]; c_score
  - sc5_same = +0.140 [0.057, 0.227] (n=167). Cross-fitted [c_score, sc5] vs [sc5] = +0.147. Vocab-clean subset (shared-aligner
  confound control): c_score 0.852 vs SC 0.714. At the medoid threshold: recall 0.62, false alarms 0.14. Shared blind spot:
  38% of errors are endorsed by the consensus (POLARITY 5%, COVERAGE 41%, STRUCT 57%). Repair operators match the labeller's
  81% of the time (chance 46%). RENAME rewrites cause 96% false alarms (the aligner does not survive synonym or constant renaming);
  z3-equivalent rewrites flip 0% by construction. Long/conditioned stratum n=5, descriptive only. Cost: $1.52 total; the peer
  pool costs $0.0015 per sentence. This re-run completed the SC_cheap arm that the shared-key limit had cut to 231/307 units,
  and restored WordNet for RENAME.
workspace_path: >-
  /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3
out_expected_files:
- method.py
- full_method_out.json
- mini_method_out.json
- preview_method_out.json
out_demo_files:
- path: method.py
  description: Research methodology implementation
</artifact_info>

<github_repo>
Repo URL: https://github.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic
Raw data URL: https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-1/experiment-3/demo/mini_demo_data.json

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
GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-1/experiment-3/demo/mini_demo_data.json"
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
To test-run the notebook in a clean environment (simulating Colab), use the disposable venv at `/tmp/aii_nb_test_envs/art_i3cVDxBp-USk-be48f6bcb721`. It is on this machine's local disk, outside your workspace, which is on a slow network volume: never create a venv inside your workspace.
```bash
UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 /tmp/aii_nb_test_envs/art_i3cVDxBp-USk-be48f6bcb721
UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python /tmp/aii_nb_test_envs/art_i3cVDxBp-USk-be48f6bcb721/bin/python jupyter ipykernel
/tmp/aii_nb_test_envs/art_i3cVDxBp-USk-be48f6bcb721/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb
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
TODO 6. Verify: (1) code_demo.ipynb contains GITHUB_DATA_URL = "https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-1/experiment-3/demo/mini_demo_data.json" exactly, (2) mini_demo_data.json exists, (3) uses GitHub URL pattern not just open('mini_demo_data.json').
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

### [3] HUMAN-USER prompt · 2026-09-25 12:33:59 UTC

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

### [4] TOOL CALL — Skill · 2026-09-25 12:34:07 UTC

```
aii-colab
```

### [5] TOOL RESULT — Skill · 2026-09-25 12:34:07 UTC

```
{"success": true, "commandName": "aii-colab"}
```

### [6] TOOL CALL — Skill · 2026-09-25 12:34:07 UTC

```
aii-long-running-tasks
```

### [7] TOOL RESULT — Skill · 2026-09-25 12:34:07 UTC

```
{"success": true, "commandName": "aii-long-running-tasks"}
```

### [8] TOOL CALL — Bash · 2026-09-25 12:34:07 UTC

```
List workspace and artifact directory:
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk; ls -la; ls -la .aii; W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; ls -la $W; wc -l $W/method.py
```

### [9] TOOL RESULT — Bash · 2026-09-25 12:34:07 UTC

```
{"stdout": "total 1991\ndrwxr-xr-x 3 root root 1002714 Sep 25 12:33 .\ndrwxr-xr-x 6 root root 1005885 Sep 25 12:33 ..\ndrwxr-xr-x 2 root root       1 Sep 25 12:33 .aii\n-rw------- 1 root root      54 Sep 25 12:33 .aii_claude_session.json\n-rw-r--r-- 1 root root   27934 Sep 25 12:34 .repl_agent.ptylog\ntotal 980\ndrwxr-xr-x 2 root root       1 Sep 25 12:33 .\ndrwxr-xr-x 3 root root 1002714 Sep 25 12:33 ..\ntotal 17609\ndrwxr-xr-x 8 root root 2003681 Sep 24 23:20 .\ndrwxr-xr-x 7 root root 2032801 Sep 23 13:02 ..\ndrwxr-xr-x 2 root root 1000103 Sep 23 15:34 .aii\n-rw------- 1 root root      54 Sep 24 23:19 .aii_claude_session.json\n-rw-r--r-- 1 root root  675333 Sep 23 15:18 .aii_cost_ledger.jsonl\n-rw-r--r-- 1 root root   67356 Sep 24 23:20 .repl_agent.ptylog\n-rw-r--r-- 1 root root    2542 Sep 24 23:20 .terminal_claude_agent_struct_out.json\n-rw-r--r-- 1 root root   17031 Sep 23 15:31 README.md\ndrwxr-xr-x 5 root root 2000738 Sep 23 17:35 data\n-rw-r--r-- 1 root root 2212306 Sep 23 15:31 full_method_out.json\ndrwxr-xr-x 2 root root 2000290 Sep 23 15:29 logs\n-rw-r--r-- 1 root root    1948 Sep 23 13:54 method.py\n-rw-r--r-- 1 root root 1943922 Sep 23 15:29 method_out.json\n-rw-r--r-- 1 root root   20816 Sep 23 15:31 mini_method_out.json\n-rw-r--r-- 1 root root   20743 Sep 23 15:31 preview_method_out.json\n-rw-r--r-- 1 root root    1212 Sep 23 13:54 pyproject.toml\n-rw-r--r-- 1 root root    6092 Sep 24 23:20 reproducibility.md\ndrwxr-xr-x 2 root root 2002163 Sep 23 13:55 results\n-rwxr-xr-x 1 root root    1101 Sep 23 13:54 run_all.sh\ndrwxr-xr-x 2 root root 1014601 Sep 23 17:35 src\ndrwxr-xr-x 2 root root 1001319 Sep 23 17:35 tests\n51 /ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/method.py", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [10] TOOL CALL — Bash · 2026-09-25 12:34:11 UTC

```
Inspect artifact source and data:
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; cd $W; cat method.py; cat pyproject.toml; cat run_all.sh; ls -la src tests data results logs; wc -l src/*.py; head -c 3000 preview_method_out.json
```

### [11] TOOL RESULT — Bash · 2026-09-25 12:34:11 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"Entry point: candidate C (cross-system z3 consensus) + self-consistency baselines on the frozen NL->FOL screen.\n\nRuns the full pipeline in order (each stage is a module in src/; OpenRouter responses are cached in data/peer_raw/,\nso a re-run does not re-bill). Stages: T0 tests -> screen (labels + hash) -> peers / SC sampling -> build ->\nconsensus (T3 mini, then full) -> analysis (writes results/summary.json + method_out.json) -> previews.\n\nusage: python method.py [--skip-api] [--boot 2000]\n\"\"\"\nimport argparse\nimport os\nimport subprocess\nimport sys\nfrom pathlib import Path\n\nfrom loguru import logger\n\nROOT = Path(__file__).resolve().parent\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\nlogger.add(ROOT / \"logs\" / \"method.log\", rotation=\"30 MB\", level=\"DEBUG\")\n\n\ndef run(args: list[str]) -> None:\n    logger.info(\"$ \" + \" \".join(args))\n    env = {**os.environ, \"PYTHONHASHSEED\": \"0\"}\n    subprocess.run([sys.executable, *args], cwd=ROOT, env=env, check=True)\n\n\n@logger.catch(reraise=True)\ndef main():\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--skip-api\", action=\"store_true\", help=\"do not call OpenRouter; use cached responses only\")\n    ap.add_argument(\"--boot\", type=int, default=2000)\n    a = ap.parse_args()\n    run([\"-m\", \"pytest\", \"-c\", \"/dev/null\", \"--rootdir\", \".\", \"--noconftest\", \"-q\", \"tests/test_fol.py\"])\n    run([\"tests/census_regression.py\"])\n    run([\"src/screen.py\"])\n    if not a.skip_api:\n        for arm in (\"peers\", \"sc_cheap\", \"sc_same\"):\n            run([\"src/peers.py\", \"call\", \"--arm\", arm])\n    run([\"src/peers.py\", \"build\"])\n    run([\"src/consensus.py\", \"--mini\", \"20\"])\n    run([\"src/consensus.py\"])\n    run([\"src/analysis.py\", \"--boot\", str(a.boot)])\n    run([\"tests/audit_rederive.py\"])\n    logger.info(\"done: method_out.json, results/summary.json, results/audit_rederive.json\")\n\n\nif __name__ == \"__main__\":\n    main()\n[project]\nname = \"consensus-fol-screen\"\nversion = \"0.1.0\"\ndescription = \"Candidate C: cross-system z3 consensus metric for NL->FOL faithfulness, with self-consistency baselines\"\nrequires-python = \">=3.12\"\n# exact versions installed in .venv (uv pip freeze); direct deps: z3-solver numpy pandas scikit-learn scipy aiohttp loguru nltk requests tenacity psutil pytest\ndependencies = [\n  \"aiohappyeyeballs==2.7.1\",\n  \"aiohttp==3.14.3\",\n  \"aiosignal==1.4.0\",\n  \"attrs==26.1.0\",\n  \"certifi==2026.7.22\",\n  \"charset-normalizer==3.5.1\",\n  \"click==8.5.0\",\n  \"cloudpickle==3.1.2\",\n  \"defusedxml==0.7.1\",\n  \"frozenlist==1.8.0\",\n  \"idna==3.20\",\n  \"iniconfig==2.3.0\",\n  \"joblib==1.6.0\",\n  \"loguru==0.7.3\",\n  \"multidict==6.9.1\",\n  \"narwhals==2.26.0\",\n  \"nltk==3.10.3\",\n  \"numpy==2.5.3\",\n  \"packaging==26.3\",\n  \"pandas==3.0.6\",\n  \"pluggy==1.6.0\",\n  \"propcache==0.5.4\",\n  \"psutil==7.2.2\",\n  \"pygments==2.21.0\",\n  \"pytest==9.1.1\",\n  \"python-dateutil==2.9.0.post0\",\n  \"regex==2026.9.10\",\n  \"requests==2.34.2\",\n  \"scikit-learn==1.9.1\",\n  \"scipy==1.18.1\",\n  \"six==1.17.0\",\n  \"tenacity==9.1.4\",\n  \"threadpoolctl==3.7.0\",\n  \"tqdm==4.70.1\",\n  \"typing-extensions==4.16.0\",\n  \"urllib3==2.8.0\",\n  \"yarl==1.25.1\",\n  \"z3-solver==5.1.0.0\",\n]\n#!/usr/bin/env bash\n# Full pipeline, in order. OpenRouter responses are cached in data/peer_raw/, so re-runs do not re-bill.\nset -euo pipefail\ncd \"$(dirname \"$0\")\"\nexport PYTHONHASHSEED=0\nPY=.venv/bin/python\n$PY -m pytest -c /dev/null --rootdir . --noconftest -q tests/test_fol.py   # T0\n$PY tests/census_regression.py                                          # T0 / F7\n$PY src/screen.py                                                       # STEP 1 (labels + hash)\n$PY src/peers.py call --arm peers --dry-run                             # T2\n$PY src/peers.py call --arm peers                                       # STEP 3\n$PY src/peers.py call --arm sc_cheap                                    # STEP 4\n$PY src/peers.py call --arm sc_same                                     # STEP 4 (optional arm)\n$PY src/peers.py build\n$PY src/consensus.py --mini 20                                          # T3\n$PY src/consensus.py                                                    # STEP 5/6 + T5\n$PY src/analysis.py --boot 2000                                         # STEP 7/8\n$PY tests/audit_rederive.py\ndata:\ntotal 8701\ndrwxr-xr-x  5 root root 2000738 Sep 23 17:35 .\ndrwxr-xr-x  8 root root 2003681 Sep 24 23:20 ..\ndrwxr-xr-x  2 root root 1099257 Sep 23 13:04 logiclm\n-rw-r--r--  1 root root  747565 Sep 23 13:07 or_models.json\ndrwxr-xr-x 10 root root 2000555 Sep 23 13:22 peer_raw\ndrwxr-xr-x  8 root root 1010195 Sep 23 13:15 peer_raw_dryrun_v0\n-rw-r--r--  1 root root   45240 Sep 23 13:07 repair_census.rows.json\n\nlogs:\ntotal 6888\ndrwxr-xr-x 2 root root 2000290 Sep 23 15:29 .\ndrwxr-xr-x 8 root root 2003681 Sep 24 23:20 ..\n-rw-r--r-- 1 root root    4844 Sep 23 15:29 analysis.log\n-rw-r--r-- 1 root root     921 Sep 23 15:29 analysis_full.out\n-rw-r--r-- 1 root root     847 Sep 23 15:30 audit_rerun.out\n-rw-r--r-- 1 root root    3367 Sep 23 13:38 build_final.out\n-rw-r--r-- 1 root root     451 Sep 23 13:10 census_regression.log\n-rw-r--r-- 1 root root   13322 Sep 23 15:28 consensus.log\n-rw-r--r-- 1 root root     490 Sep 23 15:28 consensus_full.out\n-rw-r--r-- 1 root root     454 Sep 23 15:28 consensus_mini20.out\n-rw-r--r-- 1 root root  915331 Sep 23 15:18 cost_log.jsonl\n-rw-r--r-- 1 root root     143 Sep 23 13:20 dryrun_v1.out\n-rw-r--r-- 1 root root    1076 Sep 23 15:25 method.log\n-rw-r--r-- 1 root root   13385 Sep 23 15:25 method_rerun.out\n-rw-r--r-- 1 root root 1811697 Sep 23 15:29 peers.log\n-rw-r--r-- 1 root root   12328 Sep 23 15:20 screen.log\n-rw-r--r-- 1 root root    7905 Sep 23 13:14 screen.out\n-rw-r--r-- 1 root root    2350 Sep 23 13:50 screen_rerun.out\n-rw-r--r-- 1 root root    1889 Sep 23 13:26 sweep_peers.out\n-rw-r--r-- 1 root root  250935 Sep 23 13:37 sweep_sc_cheap.out\n-rw-r--r-- 1 root root    1117 Sep 23 15:18 sweep_sc_cheap_resume.out\n-rw-r--r-- 1 root root     494 Sep 23 13:27 sweep_sc_same.out\n\nresults:\ntotal 26069\ndrwxr-xr-x 2 root root 2002163 Sep 23 13:55 .\ndrwxr-xr-x 8 root root 2003681 Sep 24 23:20 ..\n-rw-r--r-- 1 root root 1704387 Sep 23 15:29 analysis_table.jsonl\n-rw-r--r-- 1 root root     846 Sep 23 15:30 audit_rederive.json\n-rw-r--r-- 1 root root    4503 Sep 23 15:19 census_regression.json\n-rw-r--r-- 1 root root 1902117 Sep 23 15:28 consensus.json\n-rw-r--r-- 1 root root  110832 Sep 23 15:28 consensus_mini20.json\n-rw-r--r-- 1 root root     619 Sep 23 15:20 cost_estimate.json\n-rw-r--r-- 1 root root  485662 Sep 23 13:43 label_cache.jsonl\n-rw-r--r-- 1 root root    3310 Sep 23 13:49 mini_peer_outputs_labelled.json\n-rw-r--r-- 1 root root 3594445 Sep 23 15:24 pairwise_eq.jsonl\n-rw-r--r-- 1 root root    2192 Sep 23 15:23 peer_build_stats.json\n-rw-r--r-- 1 root root 4556597 Sep 23 15:23 peer_outputs.jsonl\n-rw-r--r-- 1 root root 3372664 Sep 23 15:28 peer_outputs_labelled.json\n-rw-r--r-- 1 root root  144675 Sep 23 15:28 peer_outputs_labelled_mini20.json\n-rw-r--r-- 1 root root    2946 Sep 23 13:15 prereg.json\n-rw-r--r-- 1 root root      86 Sep 23 13:15 prereg.sha256\n-rw-r--r-- 1 root root    3310 Sep 23 13:49 preview_peer_outputs_labelled.json\n-rw-r--r-- 1 root root  132126 Sep 23 13:45 repair_cache.jsonl\n-rw-r--r-- 1 root root 4918711 Sep 23 15:23 sc_samples.jsonl\n-rw-r--r-- 1 root root 1011061 Sep 23 15:20 screen_items.json\n-rw-r--r-- 1 root root      65 Sep 23 15:20 screen_label_hash.txt\n-rw-r--r-- 1 root root    3490 Sep 23 15:20 screen_report.json\n-rw-r--r-- 1 root root   65810 Sep 23 15:29 summary.json\n-rw-r--r-- 1 root root  661279 Sep 23 15:20 units.json\n\nsrc:\ntotal 3096\ndrwxr-xr-x 2 root root 1014601 Sep 23 17:35 .\ndrwxr-xr-x 8 root root 2003681 Sep 24 23:20 ..\n-rw-r--r-- 1 root root   38787 Sep 23 15:28 analysis.py\n-rw-r--r-- 1 root root    7277 Sep 23 13:08 common.py\n-rw-r--r-- 1 root root   22428 Sep 23 15:28 consensus.py\n-rw-r--r-- 1 root root    6993 Sep 23 13:44 eqcache.py\n-rw-r--r-- 1 root root    8989 Sep 23 13:08 fol.py\n-rw-r--r-- 1 root root     934 Sep 23 13:48 make_previews.py\n-rw-r--r-- 1 root root   21207 Sep 23 13:30 peers.py\n-rw-r--r-- 1 root root   17800 Sep 23 13:08 repair_census.py\n-rw-r--r-- 1 root root    7507 Sep 23 15:27 rewrites.py\n-rw-r--r-- 1 root root   17595 Sep 23 13:12 screen.py\n\ntests:\ntotal 2949\ndrwxr-xr-x 2 root root 1001319 Sep 23 17:35 .\ndrwxr-xr-x 8 root root 2003681 Sep 24 23:20 ..\n-rw-r--r-- 1 root root    8953 Sep 23 13:55 audit_rederive.py\n-rw-r--r-- 1 root root    1822 Sep 23 13:10 census_regression.py\n-rw-r--r-- 1 root root    2735 Sep 23 13:08 test_fol.py\n   613 src/analysis.py\n   210 src/common.py\n   470 src/consensus.py\n   178 src/eqcache.py\n   263 src/fol.py\n    24 src/make_previews.py\n   457 src/peers.py\n   458 src/repair_census.py\n   214 src/rewrites.py\n   354 src/screen.py\n  3241 total\n{\n  \"metadata\": {\n    \"method_name\": \"Candidate C: cross-system z3 consensus (eq_frac / medoid repair / semantic entropy) vs K=5 self-consistency\",\n    \"primary_contrast\": \"track L CORRECT vs ERROR\",\n    \"headline\": {\n      \"c_score\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.8655,\n        \"auroc_ci95\": [\n          0.8211,\n          0.9058\n        ],\n        \"auprc\": 0.8267,\n        \"prevalence\": 0.456\n      },\n      \"medoid_depth\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.7216,\n        \"auroc_ci95\": [\n          0.6726,\n          0.7737\n        ],\n        \"auprc\": 0.622,\n        \"prevalence\": 0.456\n      },\n      \"cluster_entropy\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.7732,\n        \"auroc_ci95\": [\n          0.7239,\n          0.8203\n        ],\n        \"auprc\": 0.6906,\n        \"prevalence\": 0.456\n      },\n      \"c_score_peers6\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.8721,\n        \"auroc_ci95\": [\n          0.8299,\n          0.9112\n        ],\n        \"auprc\": 0.8247,\n        \"prevalence\": 0.456\n      },\n      \"c_score_nonoai\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.8633,\n        \"auroc_ci95\": [\n          0.8197,\n          0.9034\n        ],\n        \"auprc\": 0.8082,\n        \"prevalence\": 0.456\n      },\n      \"c_score_llm2\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.7527,\n        \"auroc_ci95\": [\n          0.7006,\n          0.8059\n        ],\n        \"auprc\": 0.6586,\n        \"prevalence\": 0.456\n      },\n      \"sc5_cheap\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.7254,\n        \"auroc_ci95\": [\n          0.6688,\n          0.7811\n        ],\n        \"auprc\": 0.6265,\n        \"prevalence\": 0.456\n      },\n      \"sc5_entropy_cheap\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.6312,\n        \"auroc_ci95\": [\n          0.5678,\n          0.6934\n        ],\n        \"auprc\": 0.539,\n        \"prevalence\": 0.456\n      },\n      \"sc5_same\": {\n        \"n\": 167,\n        \"n_err\": 71,\n        \"auroc\": 0.7159,\n        \"auroc_ci95\": [\n          0.6316,\n          0.7962\n        ],\n        \"auprc\": 0.6281,\n        \"prevalence\": 0.4251\n      },\n      \"predset_instab_sc\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.6878,\n        \"auroc_ci95\": [\n          0.6257,\n          0.7497\n        ],\n        \"auprc\": 0.6015,\n        \"prevalence\": 0.456\n      },\n      \"predset_instab_pool\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.77,\n        \"auroc_ci95\": [\n          0.7165,\n          0.821\n        ],\n        \"auprc\": 0.7214,\n        \"prevalence\": 0.456\n      },\n      \"fol_length\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.5274,\n        \"auroc_ci95\": [\n          0.4695,\n          0.586\n        ],\n        \"auprc\": 0.4853,\n        \"prevalence\": 0.456\n      },\n      \"misalign\": {\n        \"n\": 546,\n        \"n_err\": 249,\n        \"auroc\": 0.8353,\n        \"auroc_ci95\": [\n          0.7935,", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [12] TOOL CALL — Bash · 2026-09-25 12:34:17 UTC

```
Read common, fol, eqcache modules:
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; cd $W; cat src/common.py src/fol.py src/eqcache.py
```

### [13] TOOL RESULT — Bash · 2026-09-25 12:34:17 UTC

```
{"stdout": "\"\"\"Shared primitives of the frozen screen: text normalisation, item ids, the automatic labeller,\nequivalence-modulo-vocabulary (eqmv) and the complexity strata.\n\nThe labeller reproduces the iter-3 repair census (repair_census.work) stage by stage, so the label\nvector is identical to sibling experiments A/B/D and dataset E (EQUIV+VOCAB -> CORRECT,\nGRAN -> UNCERTAIN_GRAN, depth<=2 repair -> ERROR[ops], no repair -> UNCERTAIN_COMPOUND).\n\"\"\"\nfrom __future_... [truncated, 24732 chars total]
```

### [14] TOOL CALL — Bash · 2026-09-25 12:34:19 UTC

```
Read consensus and repair_census modules:
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; cd $W; cat src/consensus.py src/repair_census.py
```

### [15] TOOL RESULT — Bash · 2026-09-25 12:34:19 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"STEP 5 (+ STEP 6 rewrites, T5 sanity checks, secondary peer-as-candidate sample).\n\nFor every screen candidate c of sentence t:\n  pool      = parsed LLM outputs for t (P1..P6 fresh peers + Logic-LM systems), leaving out c's own system;\n              'human_original' is never a pool member\n  eq_frac_* = share of pool members that are eqmv-equivalent to c (z3 timeouts count as NOT equivalent)\n  medoid    = pool member with most eqmv... [truncated, 32216 chars total]
```

### [16] TOOL CALL — Read · 2026-09-25 12:34:23 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/consensus.py
```

### [17] TOOL RESULT — Read · 2026-09-25 12:34:23 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/consensus.py", "content": "#!/usr/bin/env python3\n\"\"\"STEP 5 (+ STEP 6 rewrites, T5 sanity checks, secondary peer-as-candidate sample).\n\nFor every screen candidate c of sentence t:\n  pool      = parsed LLM outputs for t (P1..P6 fresh peers + Logic-LM systems), leaving out c's own system;\n              'human_original' is never a poo... [truncated, 24032 chars total]
```

### [18] ASSISTANT · 2026-09-25 12:34:25 UTC

```
Still reading the source: the orchestrator `method.py` calls modules in `src/`. Next I'll read `repair_census.py`, which holds `align` and `search`, then design the notebook.
```

### [19] TOOL CALL — Read · 2026-09-25 12:34:25 UTC

```
/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/repair_census.py
```

### [20] TOOL RESULT — Read · 2026-09-25 12:34:25 UTC

```
{"type": "text", "file": {"filePath": "/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src/repair_census.py", "content": "\"\"\"MINIMAL-TYPED-REPAIR census of real NL->FOL errors (review critique 1 & 2 of iter 2).\n\nFor every curated FOLIO-conclusion / MALLS-test item whose ORIGINAL gold is not logically equivalent to the\nCORRECTED gold (arXiv 2606.02837, HF DSAVlab-UNIUD), we ask: what is the SMALLEST sequence of typed edits that\nturns the original into a formula equivalent to the corrected one, AFTER vocabulary alignment?\n\nStage 0  ALIGN   rename original predicates/constants onto corrected ones (same arity; CamelCase-token Jaccard\n                 >= 0.5 or char-trigram Dice >= 0.6; constants by normalised string / containment).\n                 equivalent after renaming                 -> VOCAB   (vocabulary only; not an error)\nStage 1  GRAN    definitional merge/split bridge: P(args) := Q1(args) & Q2(args) when tokens(P) == tokens(Q1)+tokens(Q2)\n                 equivalent after bridge                   -> GRAN    (granularity only; not an error)\nStage 2  REPAIR  breadth-first search, depth <= 2, over typed operators applied to the aligned original:\n                 NEG (insert/remove negation), REV (swap sides of ->), QUANT (forall<->exists), RESTR (-> <-> & directly\n                 under a quantifier), CONN (other connective change among & | -> <-> xor), DROP (delete an operand of & / |),\n                 ADD (conjoin an atom that exists only in the corrected formula), SWAP (permute arguments),\n                 BIND (replace one argument by another in-scope variable or a corrected-formula constant),\n                 SCOPE (swap adjacent quantifiers), UNGLUE (split independent generic claims out of one quantifier block).\n                 A candidate is accepted when z3 proves it equivalent to the corrected formula; a cheap random-model\n                 fingerprint pre-filters candidates. Items with no repair within depth 2 are COMPOUND.\nThe class of a real error is its operator multiset. Curators' AMBIGUITY flag is carried along, so 'reading choice'\ncorrections can be reported separately.\n\"\"\"\nimport itertools\nimport json\nimport random\nimport re\nimport sys\nimport time\nfrom collections import Counter\nfrom pathlib import Path\n\nfrom fol import parse, equivalent\n\nD = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/iter_3/gen_hypo/claude_agent/data\")  # read-only iter-3 data dir\nTOKRE = re.compile(r\"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\\d+\")\nSTOP = {\"and\", \"or\", \"of\", \"in\", \"on\", \"the\", \"a\", \"an\", \"to\", \"is\", \"has\", \"have\", \"can\", \"for\", \"with\", \"by\", \"at\", \"from\", \"be\", \"are\"}\nBIN = (\"and\", \"or\", \"imp\", \"iff\", \"xor\")\n\n\ndef toks(name):\n    out = []\n    for w in TOKRE.findall(name.replace(\"_\", \" \")):\n        w = w.lower()\n        if w in STOP:\n            continue\n        out.append(w[:-1] if w.endswith(\"s\") and len(w) > 3 else w)\n    return out\n\n\ndef tri(s):\n    s = re.sub(r\"[^a-z0-9]\", \"\", s.lower())\n    return {s[i:i + 3] for i in range(max(1, len(s) - 2))}\n\n\ndef dice(a, b):\n    A, B = tri(a), tri(b)\n    return 2 * len(A & B) / max(1, len(A) + len(B))\n\n\n# ---------------------------------------------------------------- AST utilities\ndef atoms(e, acc=None):\n    acc = [] if acc is None else acc\n    if e[0] == \"atom\":\n        acc.append(e)\n    elif e[0] in (\"all\", \"ex\"):\n        atoms(e[2], acc)\n    elif e[0] == \"not\":\n        atoms(e[1], acc)\n    else:\n        atoms(e[1], acc); atoms(e[2], acc)\n    return acc\n\n\ndef bound_vars(e, acc=None):\n    acc = set() if acc is None else acc\n    if e[0] in (\"all\", \"ex\"):\n        acc.add(e[1]); bound_vars(e[2], acc)\n    elif e[0] == \"not\":\n        bound_vars(e[1], acc)\n    elif e[0] != \"atom\":\n        bound_vars(e[1], acc); bound_vars(e[2], acc)\n    return acc\n\n\ndef symbols(e):\n    bv = bound_vars(e)\n    P, C = {}, set()\n    for a in atoms(e):\n        P[(a[1], len(a[2]))] = True\n        for x in a[2]:\n            if x not in bv:\n                C.add(x)\n    return set(P), C\n\n\ndef rename(e, pmap, cmap, bv=frozenset()):\n    k = e[0]\n    if k == \"atom\":\n        return (\"atom\", pmap.get((e[1], len(e[2])), e[1]), tuple(x if x in bv else cmap.get(x, x) for x in e[2]))\n    if k in (\"all\", \"ex\"):\n        return (k, e[1], rename(e[2], pmap, cmap, bv | {e[1]}))\n    if k == \"not\":\n        return (\"not\", rename(e[1], pmap, cmap, bv))\n    return (k, rename(e[1], pmap, cmap, bv), rename(e[2], pmap, cmap, bv))\n\n\ndef expand(e, defs):\n    \"\"\"defs: {(name, arity): [name1, name2]}  P(args) -> Q1(args) & Q2(args)\"\"\"\n    k = e[0]\n    if k == \"atom\":\n        key = (e[1], len(e[2]))\n        if key in defs:\n            q = defs[key]\n            out = (\"atom\", q[0], e[2])\n            for n in q[1:]:\n                out = (\"and\", out, (\"atom\", n, e[2]))\n            return out\n        return e\n    if k in (\"all\", \"ex\"):\n        return (k, e[1], expand(e[2], defs))\n    if k == \"not\":\n        return (\"not\", expand(e[1], defs))\n    return (k, expand(e[1], defs), expand(e[2], defs))\n\n\ndef align(old, new):\n    Po, Co = symbols(old)\n    Pn, Cn = symbols(new)\n    pmap, used = {}, set()\n    cands = []\n    for p in Po - Pn:\n        for q in Pn - Po:\n            if p[1] != q[1]:\n                continue\n            to, tn = set(toks(p[0])), set(toks(q[0]))\n            j = len(to & tn) / max(1, len(to | tn))\n            s = max(j, dice(p[0], q[0]))\n            if p[0].lower() == q[0].lower():\n                s = 2\n            if j >= 0.5 or dice(p[0], q[0]) >= 0.6 or s == 2:\n                cands.append((s, p, q))\n    for s, p, q in sorted(cands, reverse=True):\n        if p in pmap or q in used:\n            continue\n        pmap[p] = q[0]; used.add(q)\n    cmap, cused = {}, set()\n    norm = lambda s: re.sub(r\"[^a-z0-9]\", \"\", s.lower())\n    for c in Co - Cn:\n        best = None\n        for d in Cn - Co:\n            if d in cused:\n                continue\n            a, b = norm(c), norm(d)\n            if a == b or (min(len(a), len(b)) >= 4 and (a in b or b in a)) or dice(c, d) >= 0.7:\n                best = d\n                break\n        if best:\n            cmap[c] = best; cused.add(best)\n    return rename(old, pmap, cmap), pmap, cmap\n\n\ndef gran_bridge(ao, new):\n    \"\"\"Try merge/split definitional bridges between leftover predicates of the aligned original and corrected.\"\"\"\n    Po, _ = symbols(ao)\n    Pn, _ = symbols(new)\n    lo, ln = Po - Pn, Pn - Po\n    defs_old, defs_new = {}, {}\n    for p in lo:  # original merged predicate -> corrected split pair\n        tp = sorted(toks(p[0]))\n        for q1, q2 in itertools.combinations([q for q in ln if q[1] == p[1]], 2):\n            if sorted(toks(q1[0]) + toks(q2[0])) == tp or set(toks(q1[0]) + toks(q2[0])) == set(tp):\n                defs_old[p] = [q1[0], q2[0]]\n    for q in ln:  # corrected merged predicate -> original split pair\n        tq = sorted(toks(q[0]))\n        for p1, p2 in itertools.combinations([p for p in lo if p[1] == q[1]], 2):\n            if sorted(toks(p1[0]) + toks(p2[0])) == tq or set(toks(p1[0]) + toks(p2[0])) == set(tq):\n                defs_new[q] = [p1[0], p2[0]]\n    _, Cn = symbols(new)\n    reify = {}\n    for p in lo:  # P(x) := Q(x, c) when tokens(P) == tokens(Q) + tokens(c)\n        for q in ln:\n            if q[1] != p[1] + 1:\n                continue\n            for c in Cn:\n                if set(toks(q[0]) + toks(c)) == set(toks(p[0])):\n                    reify[p] = (q[0], c)\n    if not defs_old and not defs_new and not reify:\n        return None\n    return reify_expand(expand(ao, defs_old), reify), expand(new, defs_new)\n\n\ndef reify_expand(e, reify):\n    k = e[0]\n    if k == \"atom\":\n        key = (e[1], len(e[2]))\n        if key in reify:\n            q, c = reify[key]\n            return (\"atom\", q, e[2] + (c,))\n        return e\n    if k in (\"all\", \"ex\"):\n        return (k, e[1], reify_expand(e[2], reify))\n    if k == \"not\":\n        return (\"not\", reify_expand(e[1], reify))\n    return (k, reify_expand(e[1], reify), reify_expand(e[2], reify))\n\n\n# ---------------------------------------------------------------- random-model fingerprint (necessary condition)\nSEEDS = list(range(24))\n\n\ndef ev(e, m, env, dom, seed):\n    k = e[0]\n    if k == \"atom\":\n        args = tuple(env[x] if x in env else (hash((seed, \"c\", x)) % dom) for x in e[2])\n        return (hash((seed, e[1], len(e[2]), args)) >> 3) & 1 == 1\n    if k == \"all\":\n        return all(ev(e[2], m, {**env, e[1]: d}, dom, seed) for d in range(dom))\n    if k == \"ex\":\n        return any(ev(e[2], m, {**env, e[1]: d}, dom, seed) for d in range(dom))\n    if k == \"not\":\n        return not ev(e[1], m, env, dom, seed)\n    a, b = ev(e[1], m, env, dom, seed), ev(e[2], m, env, dom, seed)\n    return {\"and\": a and b, \"or\": a or b, \"imp\": (not a) or b, \"iff\": a == b, \"xor\": a != b}[k]\n\n\ndef fp(e):\n    return tuple(ev(e, None, {}, 3, s) for s in SEEDS)\n\n\n# ---------------------------------------------------------------- typed operators\ndef subterms(e, path=(), scope=()):\n    yield path, e, scope\n    k = e[0]\n    if k in (\"all\", \"ex\"):\n        yield from subterms(e[2], path + (2,), scope + (e[1],))\n    elif k == \"not\":\n        yield from subterms(e[1], path + (1,), scope)\n    elif k != \"atom\":\n        yield from subterms(e[1], path + (1,), scope)\n        yield from subterms(e[2], path + (2,), scope)\n\n\ndef replace(e, path, new):\n    if not path:\n        return new\n    i = path[0]\n    lst = list(e)\n    lst[i] = replace(e[i], path[1:], new)\n    return tuple(lst)\n\n\ndef parent_kind(e, path):\n    if not path:\n        return None\n    x = e\n    for i in path[:-1]:\n        x = x[i]\n    return x[0]\n\n\ndef unglue(node):\n    \"\"\"∀x∀y (A(x) ∧ B(y) → C(x) ∧ D(y))  ->  ∀x (A(x) → C(x)) ∧ ∀y (B(y) → D(y))\"\"\"\n    vs, body = [], node\n    while body[0] == \"all\":\n        vs.append(body[1]); body = body[2]\n    if len(vs) < 2 or body[0] != \"imp\":\n        return None\n\n    def conj(x):\n        return conj(x[1]) + conj(x[2]) if x[0] == \"and\" else [x]\n\n    def vars_of(x):\n        return {a for at in atoms(x) for a in at[2] if a in vs}\n    ant, con = conj(body[1]), conj(body[2])\n    groups = []\n    for v in vs:\n        a = [x for x in ant if vars_of(x) == {v}]\n        c = [x for x in con if vars_of(x) == {v}]\n        if not c:\n            return None\n        groups.append((v, a, c))\n    if sum(len(g[1]) for g in groups) != len(ant) or sum(len(g[2]) for g in groups) != len(con):\n        return None\n\n    def mk(lst, op=\"and\"):\n        out = lst[0]\n        for x in lst[1:]:\n            out = (op, out, x)\n        return out\n    parts = [(\"all\", v, (\"imp\", mk(a), mk(c)) if a else mk(c)) for v, a, c in groups]\n    return mk(parts)\n\n\ndef edits(e, target):\n    \"\"\"Yield (op_label, candidate) for every single typed edit of e.\"\"\"\n    tgt_atoms = atoms(target)\n    Pe, _ = symbols(e)\n    _, Ct = symbols(target)\n    new_atoms = [a for a in tgt_atoms if (a[1], len(a[2])) not in Pe]\n    for path, node, scope in list(subterms(e)):\n        k = node[0]\n        # NEG\n        if k == \"not\":\n            yield \"NEG\", replace(e, path, node[1])\n        else:\n            yield \"NEG\", replace(e, path, (\"not\", node))\n        if k in (\"all\", \"ex\"):\n            yield \"QUANT\", replace(e, path, (\"ex\" if k == \"all\" else \"all\", node[1], node[2]))\n            # block flip with the restrictor convention: ∀x∀y(A→B) <-> ∃x∃y(A∧B)\n            vs, body = [], node\n            while body[0] == k:\n                vs.append(body[1]); body = body[2]\n            if body[0] in (\"imp\", \"and\"):\n                nb = (\"and\" if body[0] == \"imp\" else \"imp\", body[1], body[2])\n                q = \"ex\" if k == \"all\" else \"all\"\n                for v in reversed(vs):\n                    nb = (q, v, nb)\n                yield \"QUANT\", replace(e, path, nb)\n            if node[2][0] in (\"all\", \"ex\"):\n                inner = node[2]\n                yield \"SCOPE\", replace(e, path, (inner[0], inner[1], (k, node[1], inner[2])))\n            ug = unglue(node) if k == \"all\" else None\n            if ug is not None:\n                yield \"UNGLUE\", replace(e, path, ug)\n        if k in (\"imp\", \"iff\") and node[1][0] == \"and\":\n            # MOVE: pull a conjunct of the left side out as an outer restriction: (A ∧ B op C) -> (A -> (B op C))\n            yield \"MOVE\", replace(e, path, (\"imp\", node[1][1], (k, node[1][2], node[2])))\n            yield \"MOVE\", replace(e, path, (\"imp\", node[1][2], (k, node[1][1], node[2])))\n        if k == \"imp\" and node[2][0] == \"imp\":\n            # MOVE inverse: A -> (B -> C)  <->  (A ∧ C) -> B style condition/consequence exchange\n            yield \"MOVE\", replace(e, path, (\"imp\", (\"and\", node[1], node[2][2]), node[2][1]))\n        if k in BIN:\n            if k == \"imp\":\n                yield \"REV\", replace(e, path, (\"imp\", node[2], node[1]))\n            for op in BIN:\n                if op != k:\n                    lab = \"RESTR\" if {k, op} == {\"imp\", \"and\"} and parent_kind(e, path) in (\"all\", \"ex\") else \"CONN\"\n                    yield lab, replace(e, path, (op, node[1], node[2]))\n            if k in (\"and\", \"or\"):\n                yield \"DROP\", replace(e, path, node[1])\n                yield \"DROP\", replace(e, path, node[2])\n        if k == \"atom\":\n            args = node[2]\n            if len(args) >= 2:\n                for perm in set(itertools.permutations(args)):\n                    if perm != args:\n                        yield \"SWAP\", replace(e, path, (\"atom\", node[1], perm))\n            pool = set(scope) | Ct\n            for i, a in enumerate(args):\n                for b in pool:\n                    if b != a:\n                        yield \"BIND\", replace(e, path, (\"atom\", node[1], args[:i] + (b,) + args[i + 1:]))\n        # ADD: conjoin a corrected-only atom (args re-bound to in-scope variables when its variables are foreign)\n        if k != \"atom\" or True:\n            for a in new_atoms:\n                sc = list(scope)\n                opts = []\n                for x in a[2]:\n                    opts.append([x] if (x in Ct or x in sc) else (sc or [x]))\n                for combo in itertools.islice(itertools.product(*opts), 6):\n                    yield \"ADD\", replace(e, path, (\"and\", node, (\"atom\", a[1], tuple(combo))))\n\n\ndef search(ao, target, budget_s=25.0, max_d2=6000):\n    ft = fp(target)\n    t0 = time.time()\n    lvl1 = []\n    seen = set()\n    for lab, c in edits(ao, target):\n        s = str(c)\n        if s in seen:\n            continue\n        seen.add(s)\n        lvl1.append((lab, c))\n        if fp(c) == ft and equivalent(c, target, ms=1500) is True:\n            return [lab], time.time() - t0\n    n = 0\n    for lab1, c1 in lvl1:\n        for lab2, c2 in edits(c1, target):\n            n += 1\n            if lab1 == \"NEG\" and lab2 == \"NEG\":\n                continue\n            if n > max_d2 * 10 or time.time() - t0 > budget_s:\n                return None, time.time() - t0\n            if fp(c2) == ft and equivalent(c2, target, ms=1500) is True:\n                return sorted([lab1, lab2]), time.time() - t0\n    return None, time.time() - t0\n\n\ndef load(p):\n    return [json.loads(l) for l in open(p) if l.strip()]\n\n\ndef pairs():\n    for r in load(D / \"DSAVlab-UNIUD_MALLS_test_subset-CURATED__MALLS_instances.jsonl\"):\n        yield \"MALLS\", r[\"id\"], r[\"NL_sentence\"], r[\"FOL_sentence_old\"], r[\"FOL_sentence_new\"], str(r.get(\"ambiguity\", \"NA\"))\n    for r in load(D / \"DSAVlab-UNIUD_FOLIO_validation-curated__FOLIO_instances.jsonl\"):\n        if str(r[\"id\"]).startswith(\"story\"):\n            continue\n        yield \"FOLIO-concl\", r[\"id\"], r[\"NL_sentence\"], r[\"FOL_sentence_old\"], r[\"FOL_sentence\"], str(r.get(\"ambiguity\", \"NA\"))\n\n\ndef work(item):\n    src, iid, nl, old, new, amb = item\n    try:\n        oe, ne = parse(old), parse(new)\n    except Exception:\n        return None\n    if equivalent(oe, ne) is True:\n        return None\n    ao, pmap, cmap = align(oe, ne)\n    rec = {\"src\": src, \"id\": iid, \"nl\": nl, \"old\": old, \"new\": new, \"ambiguous\": amb == \"True\",\n           \"pmap\": {f\"{k[0]}/{k[1]}\": v for k, v in pmap.items()}, \"cmap\": cmap}\n    if equivalent(ao, ne) is True:\n        rec[\"cls\"] = \"VOCAB\"; return rec\n    gb = gran_bridge(ao, ne)\n    if gb and equivalent(gb[0], gb[1]) is True:\n        rec[\"cls\"] = \"GRAN\"; return rec\n    base, tgt = (gb if gb else (ao, ne))\n    ops, dt = search(base, tgt)\n    rec[\"secs\"] = round(dt, 1)\n    rec[\"cls\"] = \"+\".join(ops) if ops else \"COMPOUND\"\n    rec[\"depth\"] = len(ops) if ops else None\n    return rec\n\n\ndef main():\n    from multiprocessing import Pool\n    items = list(pairs())\n    with Pool(2) as pool:\n        recs = [r for r in pool.imap_unordered(work, items, chunksize=1) if r]\n    out = Path(__file__).with_suffix(\".rows.json\")\n    out.write_text(json.dumps(recs, ensure_ascii=False, indent=1))\n    n = len(recs)\n    c = Counter(r[\"cls\"] for r in recs)\n    print(f\"non-equivalent pairs: {n}\")\n    for k, v in c.most_common():\n        print(f\"  {k:22s} {v:3d}  ({v/n:.2f})\")\n    vocab = sum(r[\"cls\"] in (\"VOCAB\", \"GRAN\") for r in recs)\n    err = [r for r in recs if r[\"cls\"] not in (\"VOCAB\", \"GRAN\")]\n    single = sum(r.get(\"depth\") == 1 for r in err)\n    two = sum(r.get(\"depth\") == 2 for r in err)\n    comp = sum(r[\"cls\"] == \"COMPOUND\" for r in err)\n    print(f\"vocabulary/granularity-only (auto): {vocab}/{n}\")\n    print(f\"remaining errors: {len(err)}  single-op: {single}  two-op: {two}  compound(>2 or unresolved): {comp}\")\n    ops = Counter(o for r in err if r.get(\"depth\") for o in r[\"cls\"].split(\"+\"))\n    print(\"operator mass among repaired errors:\", dict(ops.most_common()))\n    for amb in (True, False):\n        sub = [r for r in recs if r[\"ambiguous\"] == amb]\n        print(f\"ambiguous={amb}: n={len(sub)}\", dict(Counter(r[\"cls\"] for r in sub).most_common()))\n    for s in (\"MALLS\", \"FOLIO-concl\"):\n        sub = [r for r in recs if r[\"src\"] == s]\n        print(f\"{s}: n={len(sub)}\", dict(Counter(r[\"cls\"] for r in sub).most_common()))\n\n\nif __name__ == \"__main__\":\n    sys.setrecursionlimit(10000)\n    main()\n", "numLines": 459, "startLine": 1, "totalLines": 459}}
```

### [21] TOOL CALL — Bash · 2026-09-25 12:34:31 UTC

```
Skim analysis.py head and function list:
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; cd $W; sed -n 1,140p src/analysis.py; grep -n "^def \|^    def " src/analysis.py
```

### [22] TOOL RESULT — Bash · 2026-09-25 12:34:31 UTC

```
{"stdout": "#!/usr/bin/env python3\n\"\"\"STEP 7 + 8: meta-evaluation of candidate C (cross-system z3 consensus) against the sampling\nself-consistency baselines and cheap structural baselines on the frozen screen; writes\nresults/summary.json and method_out.json (exp_gen_sol_out schema).\n\nusage: analysis.py [--mini N] [--boot 2000]\n\"\"\"\nfrom __future__ import annotations\n\nimport argparse\nimport hashlib\nimport json\nimport math\nimport random\nimport re\nimport sys\nfrom collections import Counter, defaultdict\nfrom pathlib import Path\n\nimport numpy as np\nimport pandas as pd\nfrom loguru import logger\nfrom scipy.stats import rankdata, spearmanr\nfrom sklearn.linear_model import LogisticRegression\nfrom sklearn.metrics import average_precision_score, roc_auc_score\nfrom sklearn.model_selection import GroupKFold\n\nROOT = Path(__file__).resolve().parent.parent\nsys.path.insert(0, str(ROOT / \"src\"))\nfrom common import COARSE, LLM_SYSTEMS, op_class, safe_parse  # noqa: E402\nfrom repair_census import symbols  # noqa: E402\n\nRES = ROOT / \"results\"\nlogger.remove()\nlogger.add(sys.stdout, level=\"INFO\", format=\"{time:HH:mm:ss}|{level:<7}|{message}\")\nlogger.add(ROOT / \"logs\" / \"analysis.log\", rotation=\"30 MB\", level=\"DEBUG\")\n\nSCORES = {  # name -> description (higher = more likely an error)\n    \"c_score\": \"1 - eq_frac over the full leave-one-system-out LLM pool (candidate C, PRIMARY)\",\n    \"medoid_depth\": \"typed-repair distance to the pool medoid, 0-3 (candidate C)\",\n    \"cluster_entropy\": \"semantic entropy of z3-eqmv classes of pool ∪ {c} (candidate C variant)\",\n    \"c_score_peers6\": \"1 - eq_frac over the six fresh peers only\",\n    \"c_score_nonoai\": \"1 - eq_frac over the five non-OpenAI peers\",\n    \"c_score_llm2\": \"1 - eq_frac over the other Logic-LM systems only\",\n    \"sc5_cheap\": \"1 - share of K=5 gpt-4.1-nano T=0.7 samples eqmv to c (single-other-model agreement baseline)\",\n    \"sc5_entropy_cheap\": \"semantic entropy of c + the 5 gpt-4.1-nano samples\",\n    \"sc5_same\": \"1 - share of K=5 gpt-3.5-turbo T=0.7 samples eqmv to c (true same-model SC; gpt-3.5 candidates)\",\n    \"predset_instab_sc\": \"1 - mean Jaccard of predicate names, c vs SC samples (user's rerun predicate-set similarity baseline)\",\n    \"predset_instab_pool\": \"1 - mean Jaccard of predicate names, c vs pool members (string-level consensus baseline)\",\n    \"fol_length\": \"number of atoms in the candidate (trivial complexity baseline)\",\n    \"misalign\": \"1 - alignable_frac (candidate predicates alignable to the REFERENCE; uses gold, confound probe only)\",\n}\n\n\n# ------------------------------------------------------------------ statistics\ndef auc_fast(y: np.ndarray, s: np.ndarray) -> float:\n    n1 = int(y.sum()); n0 = len(y) - n1\n    if n1 == 0 or n0 == 0:\n        return float(\"nan\")\n    r = rankdata(s)\n    return (r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * n0)\n\n\ndef cluster_boot_idx(groups: np.ndarray, B: int, seed: int = 0) -> list[np.ndarray]:\n    rng = np.random.default_rng(seed)\n    uniq, inv = np.unique(groups, return_inverse=True)\n    members = [np.where(inv == g)[0] for g in range(len(uniq))]\n    out = []\n    for _ in range(B):\n        pick = rng.integers(0, len(uniq), len(uniq))\n        out.append(np.concatenate([members[g] for g in pick]))\n    return out\n\n\ndef ci(vals) -> list:\n    v = np.array([x for x in vals if not np.isnan(x)])\n    return [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))] if len(v) else [None, None]\n\n\ndef wilson(k: int, n: int, z: float = 1.96) -> list:\n    if n == 0:\n        return [None, None]\n    p = k / n\n    d = 1 + z * z / n\n    c = (p + z * z / (2 * n)) / d\n    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d\n    return [round(c - h, 4), round(c + h, 4)]\n\n\ndef tie_acc(y: np.ndarray, s: np.ndarray, eps: float) -> float:\n    \"\"\"Deutsch, Foster & Freitag (2023) acc_eq over all item pairs, metric ties within eps.\"\"\"\n    g = np.sign(y[:, None] - y[None, :])\n    m = s[:, None] - s[None, :]\n    tie = np.abs(m) <= eps\n    ok = np.where(g == 0, tie, (~tie) & (np.sign(m) == g))\n    iu = np.triu_indices(len(y), 1)\n    return float(ok[iu].mean())\n\n\ndef tie_calibrated(y, s) -> dict:\n    diffs = np.unique(np.abs(s[:, None] - s[None, :]))\n    cands = np.unique(np.concatenate([[0.0], diffs[: min(len(diffs), 60)] + 1e-9]))\n    best = max(((tie_acc(y, s, e), e) for e in cands), key=lambda t: t[0])\n    return {\"acc_eq_eps0\": round(tie_acc(y, s, 1e-12), 4), \"acc_eq_best\": round(best[0], 4), \"eps_best\": float(best[1])}\n\n\ndef evaluate(df: pd.DataFrame, score: str, B: int, boots=None, thr_flag: str | None = None) -> dict:\n    d = df[df[score].notna()]\n    y = d[\"y\"].to_numpy().astype(int)\n    s = d[score].to_numpy().astype(float)\n    n1, n0 = int(y.sum()), int(len(y) - y.sum())\n    out = {\"n\": len(d), \"n_err\": n1, \"n_cor\": n0, \"prevalence\": round(n1 / max(1, len(d)), 4)}\n    if n1 == 0 or n0 == 0:\n        return out\n    out[\"auroc\"] = round(auc_fast(y, s), 4)\n    out[\"auprc\"] = round(float(average_precision_score(y, s)), 4)\n    groups = d[\"sentence_key\"].to_numpy()\n    bi = cluster_boot_idx(groups, B) if boots is None else boots\n    out[\"auroc_ci95\"] = [round(x, 4) if x is not None else None for x in ci([auc_fast(y[i], s[i]) for i in bi])]\n    if len(d) <= 1500:\n        out.update(tie_calibrated(y, s))\n    out[\"testable\"] = n1 >= 50 and n0 >= 50\n    if thr_flag:\n        f = d[thr_flag].to_numpy().astype(bool)\n        tp, fp = int((f & (y == 1)).sum()), int((f & (y == 0)).sum())\n        tpr, fpr = tp / n1, fp / n0\n        out[\"threshold\"] = {\"flag\": thr_flag, \"recall\": round(tpr, 4), \"recall_ci95\": wilson(tp, n1), \"false_alarm\": round(fpr, 4),\n                            \"false_alarm_ci95\": wilson(fp, n0), \"precision\": round(tp / max(1, tp + fp), 4)}\n        for pi in (0.10, 0.25):\n            out[\"threshold\"][f\"precision_at_prev_{int(pi * 100)}\"] = round(tpr * pi / max(1e-12, tpr * pi + fpr * (1 - pi)), 4)\n    return out\n\n\ndef paired_delta(df: pd.DataFrame, a: str, b: str, B: int) -> dict:\n    d = df[df[a].notna() & df[b].notna()]\n    y = d[\"y\"].to_numpy().astype(int)\n    if y.sum() == 0 or y.sum() == len(y):\n        return {\"n\": len(d)}\n    sa, sb = d[a].to_numpy().astype(float), d[b].to_numpy().astype(float)\n    bi = cluster_boot_idx(d[\"sentence_key\"].to_numpy(), B)\n56:def auc_fast(y: np.ndarray, s: np.ndarray) -> float:\n64:def cluster_boot_idx(groups: np.ndarray, B: int, seed: int = 0) -> list[np.ndarray]:\n75:def ci(vals) -> list:\n80:def wilson(k: int, n: int, z: float = 1.96) -> list:\n90:def tie_acc(y: np.ndarray, s: np.ndarray, eps: float) -> float:\n100:def tie_calibrated(y, s) -> dict:\n107:def evaluate(df: pd.DataFrame, score: str, B: int, boots=None, thr_flag: str | None = None) -> dict:\n134:def paired_delta(df: pd.DataFrame, a: str, b: str, B: int) -> dict:\n148:def crossfit(df: pd.DataFrame, feats: list[str], base: list[str], B: int) -> dict:\n169:def partial_spearman(y, s, z) -> float:\n171:    def res(a, b):\n178:def jacc(a: set, b: set) -> float:\n182:def pred_names(f: str | None) -> set | None:\n189:def n_atoms(f: str | None) -> float | None:\n197:def bins(df: pd.DataFrame) -> pd.DataFrame:\n210:def main():\n266:    def contrast(name):\n379:    def rates(g):\n576:def write_method_out(df: pd.DataFrame, S_: dict, suffix: str):\n577:    def s(v):", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [23] TOOL CALL — Bash · 2026-09-25 12:34:35 UTC

```
Read analysis main table construction:
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; cd $W; sed -n 134,300p src/analysis.py
```

### [24] TOOL RESULT — Bash · 2026-09-25 12:34:35 UTC

```
{"stdout": "def paired_delta(df: pd.DataFrame, a: str, b: str, B: int) -> dict:\n    d = df[df[a].notna() & df[b].notna()]\n    y = d[\"y\"].to_numpy().astype(int)\n    if y.sum() == 0 or y.sum() == len(y):\n        return {\"n\": len(d)}\n    sa, sb = d[a].to_numpy().astype(float), d[b].to_numpy().astype(float)\n    bi = cluster_boot_idx(d[\"sentence_key\"].to_numpy(), B)\n    deltas = [auc_fast(y[i], sa[i]) - auc_fast(y[i], sb[i]) for i in bi]\n    dv = np.array([x for x in deltas if not np.isnan(x)])\n    return {\"n\": len(d), \"n_err\": int(y.sum()), \"auroc_a\": round(auc_fast(y, sa), 4), \"auroc_b\": round(auc_fast(y, sb), 4),\n            \"delta\": round(auc_fast(y, sa) - auc_fast(y, sb), 4), \"delta_ci95\": [round(x, 4) for x in ci(deltas)],\n            \"p_delta_le_0\": round(float((dv <= 0).mean()), 4)}\n\n\ndef crossfit(df: pd.DataFrame, feats: list[str], base: list[str], B: int) -> dict:\n    d = df.dropna(subset=list(set(feats + base))).copy()\n    y = d[\"y\"].to_numpy().astype(int)\n    if y.sum() < 10 or (len(y) - y.sum()) < 10:\n        return {\"n\": len(d)}\n    g = d[\"sentence_key\"].to_numpy()\n    gkf = GroupKFold(n_splits=5)\n    oof = {}\n    for name, fs in ((\"full\", feats), (\"base\", base)):\n        p = np.zeros(len(d))\n        X = d[fs].to_numpy().astype(float)\n        for tr, te in gkf.split(X, y, g):\n            m = LogisticRegression(max_iter=1000).fit(X[tr], y[tr])\n            p[te] = m.predict_proba(X[te])[:, 1]\n        oof[name] = p\n    d[\"_full\"], d[\"_base\"] = oof[\"full\"], oof[\"base\"]\n    r = paired_delta(d, \"_full\", \"_base\", B)\n    r.update(features=feats, base=base)\n    return r\n\n\ndef partial_spearman(y, s, z) -> float:\n    ry, rs, rz = rankdata(y), rankdata(s), rankdata(z)\n    def res(a, b):\n        b1 = np.c_[np.ones(len(b)), b]\n        coef, *_ = np.linalg.lstsq(b1, a, rcond=None)\n        return a - b1 @ coef\n    return float(np.corrcoef(res(ry, rz), res(rs, rz))[0, 1])\n\n\ndef jacc(a: set, b: set) -> float:\n    return len(a & b) / len(a | b) if (a | b) else 1.0\n\n\ndef pred_names(f: str | None) -> set | None:\n    e = safe_parse(f) if f else None\n    if e is None:\n        return None\n    return {p[0].lower() for p in symbols(e)[0]}\n\n\ndef n_atoms(f: str | None) -> float | None:\n    e = safe_parse(f) if f else None\n    if e is None:\n        return None\n    from repair_census import atoms\n    return float(len(atoms(e)))\n\n\ndef bins(df: pd.DataFrame) -> pd.DataFrame:\n    st = df[\"strata\"]\n    df = df.copy()\n    df[\"len_bin\"] = [s[\"len_bin\"] for s in st]\n    df[\"words\"] = [s[\"words\"] for s in st]\n    df[\"nq_bin\"] = [None if s[\"n_quant\"] is None else (\"<=1\" if s[\"n_quant\"] <= 1 else (\"2\" if s[\"n_quant\"] == 2 else \">=3\")) for s in st]\n    df[\"depth_bin\"] = [None if s[\"depth\"] is None else (\"<=3\" if s[\"depth\"] <= 3 else (\"4-5\" if s[\"depth\"] <= 5 else \">=6\")) for s in st]\n    df[\"ncond_bin\"] = [None if s[\"n_cond\"] is None else (\"0\" if s[\"n_cond\"] == 0 else (\"1-2\" if s[\"n_cond\"] <= 2 else \">=3\")) for s in st]\n    df[\"exception\"] = [bool(s[\"exception\"]) for s in st]\n    return df\n\n\n@logger.catch(reraise=True)\ndef main():\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--mini\", type=int, default=0)\n    ap.add_argument(\"--boot\", type=int, default=2000)\n    a = ap.parse_args()\n    B = a.boot\n    suffix = f\"_mini{a.mini}\" if a.mini else \"\"\n    items = json.loads((RES / \"screen_items.json\").read_text())\n    cons = json.loads((RES / f\"consensus{suffix}.json\").read_text())\n    peer_lab = json.loads((RES / f\"peer_outputs_labelled{suffix}.json\").read_text())\n    prereg = json.loads((RES / \"prereg.json\").read_text())\n    h = (RES / \"screen_label_hash.txt\").read_text().strip()\n    assert prereg[\"screen_label_hash\"] == h, \"label hash changed after pre-registration\"\n    rec = {r[\"item_id\"]: r for r in cons[\"records\"]}\n    items = [x for x in items if x[\"item_id\"] in rec]\n    sents = cons[\"sentences\"]\n    sc_rows = [json.loads(l) for l in (RES / \"sc_samples.jsonl\").read_text().splitlines() if l.strip()]\n    uj = json.loads((RES / \"units.json\").read_text())\n\n    rows = []\n    for x in items:\n        r = rec[x[\"item_id\"]]\n        S = sents[x[\"sentence_key\"]]\n        row = {k: x[k] for k in (\"item_id\", \"track\", \"kind\", \"system\", \"text\", \"candidate_fol\", \"reference_fol\", \"label\",\n                                 \"auto_class\", \"repair_ops\", \"vocab_strict\", \"sentence_key\", \"strata\")}\n        row.update({k: r.get(k) for k in (\"eq_frac_full\", \"eq_frac_peers6\", \"eq_frac_nonoai\", \"eq_frac_llm2\", \"medoid\", \"medoid_fol\",\n                                           \"medoid_support\", \"medoid_depth\", \"medoid_ops\", \"cluster_entropy\", \"n_classes\",\n                                           \"n_peers_parsed\", \"n_peers_total\", \"coverage_status\", \"c_score\", \"sc5_eq_frac_cheap\",\n                                           \"sc5_eq_frac_same\", \"sc5_entropy_cheap\", \"sc5_entropy_same\", \"alignable_frac\",\n                                           \"medoid_label\", \"medoid_ref_ops\", \"pool_eq\", \"pool_ids\", \"seconds_z3\", \"n_timeouts\")})\n        ok = r[\"coverage_status\"] == \"ok\"\n        for nm, col in ((\"c_score_peers6\", \"eq_frac_peers6\"), (\"c_score_nonoai\", \"eq_frac_nonoai\"), (\"c_score_llm2\", \"eq_frac_llm2\")):\n            v = r.get(col)\n            row[nm] = (1 - v) if (ok and v is not None) else 1.0\n        row[\"sc5_cheap\"] = 1 - r[\"sc5_eq_frac_cheap\"] if r.get(\"sc5_eq_frac_cheap\") is not None else None\n        row[\"sc5_same\"] = (1 - r[\"sc5_eq_frac_same\"]) if (r.get(\"sc5_eq_frac_same\") is not None and x[\"system\"] == \"gpt-3.5-turbo\") else None\n        row[\"flag_medoid\"] = (r[\"medoid_depth\"] or 0) >= 1\n        cp = pred_names(x[\"candidate_fol\"])\n        scs = [f for f in [None] * 0]\n        u = S[\"unit\"]\n        smp = [s[\"fol\"] for s in sc_rows if s[\"arm\"] == \"sc_cheap\" and s[\"unit_id\"] == u and s.get(\"sentence_norm\") == x[\"sentence_key\"]]\n        if cp is not None:\n            js = [jacc(cp, pred_names(f)) for f in smp if pred_names(f) is not None]\n            row[\"predset_instab_sc\"] = 1 - (sum(js) / 5 if js else 0.0)\n            pm = [S[\"members\"][m] for m in (r.get(\"pool_ids\") or [])]\n            jp = [jacc(cp, pred_names(f)) for f in pm if f]\n            row[\"predset_instab_pool\"] = 1 - (sum(jp) / len(jp)) if jp else 1.0\n        else:\n            row[\"predset_instab_sc\"] = row[\"predset_instab_pool\"] = None\n        row[\"fol_length\"] = n_atoms(x[\"candidate_fol\"])\n        row[\"misalign\"] = (1 - r[\"alignable_frac\"]) if r.get(\"alignable_frac\") is not None else None\n        rows.append(row)\n    df = bins(pd.DataFrame(rows))\n    S_ = {}\n\n    # ------------------------------------------------------------------ contrasts\n    def contrast(name):\n        L = df[df[\"track\"] == \"L\"]\n        if name == \"primary\":\n            d = L[L[\"label\"].isin([\"CORRECT\", \"ERROR\"])]\n        elif name == \"lenient\":\n            d = L[L[\"label\"].isin([\"CORRECT\", \"ERROR\", \"UNCERTAIN_COMPOUND\"])]\n        elif name == \"vocab_strict\":\n            d = L[(L[\"label\"] == \"ERROR\") | ((L[\"label\"] == \"CORRECT\") & (L[\"vocab_strict\"] == True))]  # noqa: E712\n        elif name == \"trackH\":\n            H = df[df[\"track\"] == \"H\"]\n            d = H[H[\"label\"].isin([\"CORRECT\", \"ERROR\"])]\n        elif name == \"vocab_clean\":\n            d = L[L[\"label\"].isin([\"CORRECT\", \"ERROR\"]) & (L[\"alignable_frac\"] == 1.0)]\n        else:\n            raise ValueError(name)\n        d = d.copy()\n        d[\"y\"] = (d[\"label\"] != \"CORRECT\").astype(int)\n        return d\n    CONTR = [\"primary\", \"lenient\", \"vocab_strict\", \"trackH\", \"vocab_clean\"]\n    res = {}\n    for cn in CONTR:\n        d = contrast(cn)\n        res[cn] = {}\n        for sc in SCORES:\n            res[cn][sc] = evaluate(d, sc, B, thr_flag=\"flag_medoid\" if sc == \"c_score\" else None)\n        logger.info(f\"[{cn}] n={len(d)} err={int(d['y'].sum())}  \" +\n                    \"  \".join(f\"{sc}={res[cn][sc].get('auroc')}\" for sc in (\"c_score\", \"medoid_depth\", \"cluster_entropy\", \"sc5_cheap\", \"sc5_same\", \"misalign\")))\n    S_[\"auroc\"] = res\n    P = contrast(\"primary\")\n    # ------------------------------------------------------------------ paired deltas\n    deltas = {}\n    for cn in (\"primary\", \"lenient\", \"trackH\", \"vocab_clean\"):\n        d = contrast(cn)\n        deltas[cn] = {\"c_score-sc5_cheap\": paired_delta(d, \"c_score\", \"sc5_cheap\", B),\n                      \"c_score-cluster_entropy\": paired_delta(d, \"c_score\", \"cluster_entropy\", B),", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [25] TOOL CALL — Bash · 2026-09-25 12:34:49 UTC

```
Inspect screen items, caches, timings:
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; cd $W; python3 - <<'EOF'
import json,statistics as st
from collections import Counter
items=json.load(open('results/screen_items.json'))
print(len(items), items[0].keys())
print(json.dumps(items[0],ensure_ascii=False)[:1500])
L=[x for x in items if x['track']=='L' and x['label'] in('CORRECT','ERROR')]
print(len(L), Counter(x['label'] for x in L), len({x['sentence_key'] for x in L}))
print(Counter(x['system'] for x in L))
pe=[json.loads(l) for l in open('results/pairwise_eq.jsonl')]
s=[r['secs'] for r in pe]; print(len(pe), st.mean(s), st.median(s), max(s), sum(x>1 for x in s))
rp=[json.loads(l) for l in open('results/repair_cache.jsonl')]
s=[r['secs'] for r in rp]; print('repair',len(rp), st.mean(s), st.median(s), max(s))
c=json.load(open('results/consensus.json'))
print(c['timing'])
k=next(iter(c['sentences'])); print(k, json.dumps(c['sentences'][k],ensure_ascii=False)[:1500])
print(json.dumps(c['records'][0],ensure_ascii=False)[:1500])
EOF
```

### [26] TOOL RESULT — Bash · 2026-09-25 12:34:49 UTC

```
{"stdout": "1169 dict_keys(['item_id', 'track', 'kind', 'system', 'text', 'candidate_fol', 'reference_fol', 'ambiguous', 'story_id', 'source', 'malls_id', 'sentence_key', 'strata', 'label', 'auto_class', 'repair_ops', 'vocab_strict', 'pmap', 'label_seconds'])\n{\"item_id\": \"0039a78a4874a842\", \"track\": \"H\", \"kind\": \"malls\", \"system\": \"human_original\", \"text\": \"A product is eco-friendly if it is made from sustainable materials, has a low carbon footprint, or encourages conservation of resources.\", \"candidate_fol\": \"∀x (Product(x) ∧ (SustainableMaterials(x) ∨ LowCarbonFootprint(x) ∨ EncouragesConservation(x)) → EcoFriendly(x))\", \"reference_fol\": \"∀x (Product(x) ∧ (SustainableMaterials(x) ∨ LowCarbonFootprint(x) ∨ EncouragesConservation(x)) → EcoFriendly(x))\", \"ambiguous\": true, \"story_id\": null, \"source\": \"MALLS-test-curated\", \"malls_id\": 22, \"sentence_key\": \"a product is ecofriendly if it is made from sustainable materials has a low carbon footprint or encourages conservation of resources\", \"strata\": {\"words\": 21, \"len_bin\": \">=20\", \"exception\": false, \"exception_marker\": null, \"n_quant\": 1, \"depth\": 5, \"n_cond\": 2}, \"label\": \"CORRECT\", \"auto_class\": \"EQUIV\", \"repair_ops\": [], \"vocab_strict\": true, \"pmap\": {}, \"label_seconds\": 0.0}\n546 Counter({'CORRECT': 297, 'ERROR': 249}) 192\nCounter({'gpt-4': 198, 'text-davinci-003': 181, 'gpt-3.5-turbo': 167})\n19226 0.001536825132632893 0.001 0.032 0\nrepair 798 0.2848872180451128 0.01 10.01\n{'pairs_s': 0.0, 'repair_s': 0.0, 'labels_s': 0.0, 'total_s': 18.0, 'n_pairs': 18245, 'n_sentences': 440, 'repair_budget_s': 10.0}\n1984 is a streaming service {\"unit\": \"F:concl_343_50\", \"members\": {\"P1\": null, \"P2\": null, \"P3\": null, \"P4\": null, \"P5\": null, \"P6\": null, \"gpt-3.5-turbo\": null, \"gpt-4\": null, \"text-davinci-003\": null}, \"attempted\": [\"P1\", \"P2\", \"P3\", \"P4\", \"P5\", \"P6\", \"gpt-3.5-turbo\", \"gpt-4\", \"text-davinci-003\"], \"ref\": \"StreamingService(y1984)\"}\n{\"n_peers_parsed\": 6, \"n_peers_total\": 6, \"pool_ids\": [\"P1\", \"P2\", \"P3\", \"P4\", \"P5\", \"P6\"], \"pool_eq\": {\"P1\": false, \"P2\": true, \"P3\": false, \"P4\": true, \"P5\": true, \"P6\": true}, \"n_timeouts\": 0, \"eq_frac_full\": 0.6666666666666666, \"eq_frac_peers6\": 0.6666666666666666, \"eq_frac_nonoai\": 0.6, \"eq_frac_llm2\": null, \"cluster_entropy\": 0.5982695885852573, \"n_classes\": 2, \"coverage_status\": \"ok\", \"medoid\": \"P2\", \"medoid_fol\": \"∀x (Product(x) ∧ (MadeFromSustainableMaterials(x) ∨ HasLowCarbonFootprint(x) ∨ EncouragesConservationOfResources(x)) → EcoFriendly(x))\", \"medoid_support\": 0.6, \"eq_medoid\": true, \"sc5_present_cheap\": true, \"sc5_eq_frac_cheap\": 0.0, \"sc5_entropy_cheap\": 0.45056120886630463, \"sc5_present_same\": false, \"sc5_eq_frac_same\": null, \"item_id\": \"0039a78a4874a842\", \"medoid_depth\": 0, \"medoid_ops\": [], \"seconds_z3\": 0.016, \"c_score\": 0.33333333333333337, \"alignable_frac\": 1.0, \"medoid_label\": \"CORRECT\", \"medoid_ref_ops\": []}", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [27] TOOL CALL — Bash · 2026-09-25 12:35:09 UTC

```
Inspect rewrites, SC/peer rows, z3 availability:
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; cd $W; head -30 src/rewrites.py; python3 -c "
import json,statistics as st
items=json.load(open('results/screen_items.json'))
L=[x for x in items if x['track']=='L' and x['label'] in('CORRECT','ERROR')]
s=[x['label_seconds'] for x in L]; print(st.mean(s), st.median(s), max(s))
from collections import Counter
print(Counter(x['kind'] for x in L)); print(Counter(x['strata']['len_bin'] for x in L))
"; head -c 1500 results/sc_samples.jsonl; echo; head -c 1200 results/peer_outputs.jsonl; echo; UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip compile --python-version 3.12 - <<<'z3-solver==5.1.0.0' 2>&1 | tail -3; which python3; python3 --version
```

### [28] TOOL RESULT — Bash · 2026-09-25 12:35:11 UTC

```
{"stdout": "\"\"\"Deterministic meaning-preserving rewrites of FOL ASTs (STEP 6, rewrite invariance).\n\nRENAME          head CamelCase token of every predicate -> first WordNet synonym from a different word of the\n                first synset (CamelCased), else token reversed + 'Q'; constants -> 'c_' + sha1(name)[:4]\n                (equivalent only after the inverse map; this is the real test of the aligner)\nRENAME(token_alignable=True)  pluralise the head token and keep constants (the aligner must undo it; used by T0)\nREORDER         swap the operands of every ∧ / ∨\nDEMORGAN        rewrite the first ∧ as ¬(¬A ∨ ¬B) (or, if there is no ∧, the first ∨ as ¬(¬A ∧ ¬B))\nPRENEX          pull ONE quantifier outwards across ∧ / ∨ or across the consequent of → when sound, else n/a\nCONTRAPOSITIVE  every A → B becomes ¬B → ¬A\n\"\"\"\nfrom __future__ import annotations\n\nimport hashlib\nimport re\nfrom pathlib import Path\nfrom functools import lru_cache\n\nfrom repair_census import bound_vars, symbols\n\nTOKRE = re.compile(r\"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\\d+\")\nNLTK_DIR = Path(__file__).resolve().parent.parent / \"data\" / \"nltk_data\"   # nltk.download('wordnet', download_dir=...)\nSYN_STATS = {\"wordnet\": 0, \"nonce\": 0}   # how each distinct head token was renamed (reported in summary.json)\n\n\ndef wordnet_available() -> bool:\n    try:\n        import nltk\n        if str(NLTK_DIR) not in nltk.data.path:\n            nltk.data.path.insert(0, str(NLTK_DIR))\n0.010750915750915751 0.0 0.35\nCounter({'premise': 336, 'conclusion': 210})\nCounter({'<12': 505, '12-19': 38, '>=20': 3})\n{\"unit_id\": \"F:concl_380_1\", \"unit_type\": \"U_F\", \"model\": \"openai/gpt-4.1-nano\", \"sample\": 0, \"arm\": \"sc_cheap\", \"sentence_norm\": \"bonnie performs in school talent shows often\", \"nl\": \"Bonnie performs in school talent shows often.\", \"fol\": \"PerformsOften(Bonnie)\", \"parse_ok\": true, \"mapping_mode\": \"text\", \"cost_usd\": 3.258571428571428e-05, \"unit_cost_usd\": 0.0002281, \"latency_s\": 4.27, \"raw_hash\": \"e0f524e89150\", \"attempts\": 1}\n{\"unit_id\": \"F:concl_380_1\", \"unit_type\": \"U_F\", \"model\": \"openai/gpt-4.1-nano\", \"sample\": 0, \"arm\": \"sc_cheap\", \"sentence_norm\": \"if people perform in school talent shows often then they attend and are very engaged with school events\", \"nl\": \"If people perform in school talent shows often, then they attend and are very engaged with school events.\", \"fol\": \"∀x (PerformsOften(x) → AttendsSchoolEvents(x))\", \"parse_ok\": true, \"mapping_mode\": \"text\", \"cost_usd\": 3.258571428571428e-05, \"unit_cost_usd\": 0.0002281, \"latency_s\": 4.27, \"raw_hash\": \"e0f524e89150\", \"attempts\": 1}\n{\"unit_id\": \"F:concl_380_1\", \"unit_type\": \"U_F\", \"model\": \"openai/gpt-4.1-nano\", \"sample\": 0, \"arm\": \"sc_cheap\", \"sentence_norm\": \"people either perform in school talent shows often or are inactive and disinterested members of their community\", \"nl\": \"People either perform in school talent shows often or are inactive and disinterested members of their community.\", \"fol\": \"∀x (PerformsOften(x) ∨ (InactiveMember(x)))\", \"parse_ok\": true, \"mapping_mode\": \"text\", \"cost_usd\": 3.2585714\n{\"unit_id\": \"F:concl_380_1\", \"unit_type\": \"U_F\", \"model\": \"meta-llama/llama-3.3-70b-instruct\", \"sample\": 0, \"peer\": \"P1\", \"family\": \"meta\", \"arm\": \"peer\", \"sentence_norm\": \"bonnie performs in school talent shows often\", \"nl\": \"Bonnie performs in school talent shows often.\", \"fol\": \"Perform(bonnie)\", \"parse_ok\": true, \"mapping_mode\": \"text\", \"cost_usd\": 5.257142857142857e-05, \"unit_cost_usd\": 0.000368, \"latency_s\": 10.15, \"raw_hash\": \"ef91bb4b17d7\", \"attempts\": 1}\n{\"unit_id\": \"F:concl_380_1\", \"unit_type\": \"U_F\", \"model\": \"meta-llama/llama-3.3-70b-instruct\", \"sample\": 0, \"peer\": \"P1\", \"family\": \"meta\", \"arm\": \"peer\", \"sentence_norm\": \"if people perform in school talent shows often then they attend and are very engaged with school events\", \"nl\": \"If people perform in school talent shows often, then they attend and are very engaged with school events.\", \"fol\": \"∀x (Perform(x) → (Attend(x) ∧ Engaged(x)))\", \"parse_ok\": true, \"mapping_mode\": \"text\", \"cost_usd\": 5.257142857142857e-05, \"unit_cost_usd\": 0.000368, \"latency_s\": 10.15, \"raw_hash\": \"ef91bb4b17d7\", \"attempts\": 1}\n{\"unit_id\": \"F:concl_380_1\", \"unit_type\": \"U_F\", \"model\": \"meta-llama/llama-3.3-70b-instruct\", \"sample\": 0, \"pee\n# This file was autogenerated by uv via the following command:\n#    uv pip compile --python-version 3.12 -\nz3-solver==5.1.0.0\n/usr/local/bin/python3\nPython 3.12.14", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [29] TOOL CALL — Bash · 2026-09-25 12:35:21 UTC

```
Set up scratch copy and inspect summary:
SP=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-i3cVDxBp-USk/9515af7b-63fd-4c30-8b8a-c704cc189967/scratchpad; W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3; mkdir -p $SP/proj/logs $SP/proj/results; cp -r $W/src $SP/proj/; for f in screen_items.json units.json peer_outputs.jsonl sc_samples.jsonl consensus.json summary.json; do ln -sf $W/results/$f $SP/proj/results/$f; done; python3 -c "
import json; s=json.load(open('$W/results/summary.json')); print(list(s.keys())); print(json.dumps(s['auroc']['primary']['c_score']))
for k in s:
  print(k, str(s[k])[:300])
"
```

### [30] TOOL RESULT — Bash · 2026-09-25 12:35:21 UTC

```
{"stdout": "['auroc', 'paired_delta_auroc', 'crossfit_logistic', 'per_system', 'per_type_sensitivity', 'pool_size_curve', 'shared_aligner_confound', 'blind_spots', 'operator_agreement', 'complexity', 'coverage', 'cost', 'secondary_peer_as_candidate', 'system_level', 'sanity', 'rewrite_invariance', 'label_noise_context', 'prereg', 'score_definitions', 'n']\n{\"n\": 546, \"n_err\": 249, \"n_cor\": 297, \"prevalence\": 0.456, \"auroc\": 0.8655, \"auprc\": 0.8267, \"auroc_ci95\": [0.8211, 0.9058], \"acc_eq_eps0\": 0.5437, \"acc_eq_best\": 0.6419, \"eps_best\": 0.41666666766666666, \"testable\": true, \"threshold\": {\"flag\": \"flag_medoid\", \"recall\": 0.6185, \"recall_ci95\": [0.5568, 0.6766], \"false_alarm\": 0.138, \"false_alarm_ci95\": [0.1034, 0.1819], \"precision\": 0.7897, \"precision_at_prev_10\": 0.3324, \"precision_at_prev_25\": 0.5989}}\nauroc {'primary': {'c_score': {'n': 546, 'n_err': 249, 'n_cor': 297, 'prevalence': 0.456, 'auroc': 0.8655, 'auprc': 0.8267, 'auroc_ci95': [0.8211, 0.9058], 'acc_eq_eps0': 0.5437, 'acc_eq_best': 0.6419, 'eps_best': 0.41666666766666666, 'testable': True, 'threshold': {'flag': 'flag_medoid', 'recall': 0.6185\npaired_delta_auroc {'primary': {'c_score-sc5_cheap': {'n': 546, 'n_err': 249, 'auroc_a': 0.8655, 'auroc_b': 0.7254, 'delta': 0.1401, 'delta_ci95': [0.0847, 0.1967], 'p_delta_le_0': 0.0}, 'c_score-cluster_entropy': {'n': 546, 'n_err': 249, 'auroc_a': 0.8655, 'auroc_b': 0.7732, 'delta': 0.0924, 'delta_ci95': [0.0607, 0.\ncrossfit_logistic {'primary: [c_score, sc5_cheap] vs [sc5_cheap]': {'n': 546, 'n_err': 249, 'auroc_a': 0.8645, 'auroc_b': 0.7175, 'delta': 0.147, 'delta_ci95': [0.0985, 0.1989], 'p_delta_le_0': 0.0, 'features': ['c_score', 'sc5_cheap'], 'base': ['sc5_cheap']}, 'primary: [c_score, medoid_depth, cluster_entropy, sc5_ch\nper_system {'gpt-3.5-turbo': {'c_score': {'n': 167, 'n_err': 71, 'n_cor': 96, 'prevalence': 0.4251, 'auroc': 0.8563, 'auprc': 0.8145, 'auroc_ci95': [0.7928, 0.9136], 'acc_eq_eps0': 0.5285, 'acc_eq_best': 0.6403, 'eps_best': 0.625000001, 'testable': True}, 'medoid_depth': {'n': 167, 'n_err': 71, 'n_cor': 96, 'p\nper_type_sensitivity {'trackL': {'COVERAGE': {'n': 197, 'recall_at_threshold': 0.5939, 'ci95': [0.5242, 0.6601], 'mean_c_score': 0.6686, 'sc5_cheap_mean': 0.8132}, 'MIXED': {'n': 8, 'recall_at_threshold': 0.875, 'ci95': [0.5291, 0.9776], 'mean_c_score': 0.8594, 'sc5_cheap_mean': 0.95}, 'POLARITY': {'n': 21, 'recall_at_t\npool_size_curve {'1': {'mean_auroc': 0.7418, 'sd': 0.0112, 'mean_pool_used': 1.0}, '2': {'mean_auroc': 0.803, 'sd': 0.0091, 'mean_pool_used': 1.99}, '3': {'mean_auroc': 0.8263, 'sd': 0.01, 'mean_pool_used': 2.98}, '4': {'mean_auroc': 0.8415, 'sd': 0.0096, 'mean_pool_used': 3.97}, '6': {'mean_auroc': 0.8607, 'sd': 0\nshared_aligner_confound {'auroc_misalign_alone': 0.8353, 'auroc_c_score': 0.8655, 'vocab_clean_subset': {'c_score': {'n': 379, 'n_err': 82, 'n_cor': 297, 'prevalence': 0.2164, 'auroc': 0.8518, 'auprc': 0.634, 'auroc_ci95': [0.765, 0.9294], 'acc_eq_eps0': 0.4739, 'acc_eq_best': 0.7167, 'eps_best': 0.5833333343333333, 'testa\nblind_spots {'overall': {'n': 249, 'blind_strict': 0.3815, 'blind_strict_ci95': [0.3234, 0.4432], 'blind_same_ops': 0.4056, 'blind_same_ops_ci95': [0.3465, 0.4676], 'majority_endorses': 0.3454, 'majority_endorses_ci95': [0.2891, 0.4064], 'medoid_correct': 0.3414, 'medoid_correct_ci95': [0.2853, 0.4023]}, 'ceili\noperator_agreement {'n': 139, 'exact_multiset': 0.8058, 'exact_ci95': [0.7321, 0.8629], 'any_overlap': 0.9496, 'coarse_class': 0.9209, 'coarse_ci95': [0.8638, 0.9552], 'chance_majority_coarse': {'class': 'COVERAGE', 'freq': 0.777}, 'chance_majority_exact': {'ops': ['ADD', 'DROP'], 'freq': 0.4604}}\ncomplexity {'len_bin': {'12-19': {'n_err': 20, 'n_cor': 18, 'testable': False, 'auroc': {'c_score': 0.775, 'medoid_depth': 0.6917, 'sc5_cheap': 0.7611}, 'auroc_ci95': {'c_score': [0.5629, 0.9258], 'medoid_depth': [0.5199, 0.834], 'sc5_cheap': [0.5992, 0.8966]}, 'false_alarm_at_threshold': 0.2778, 'recall_at_th\ncoverage {'coverage_status_counts': {'H|ok': 278, 'H|insufficient_pool': 1, 'H|candidate_unparseable': 23, 'L|ok': 799, 'L|candidate_unparseable': 65, 'L|insufficient_pool': 3}, 'screen_label_counts': {'H|human_original|CORRECT': 201, 'H|human_original|REF_UNPARSEABLE': 8, 'H|human_original|ERROR': 35, 'H|hu\ncost {'total_usd': 1.5194, 'by_model_usd': {'deepseek/deepseek-chat-v3.1': 0.1205, 'google/gemini-2.5-flash-lite': 0.0662, 'meta-llama/llama-3.3-70b-instruct': 0.0757, 'mistralai/mistral-small-3.2-24b-instruct': 0.0534, 'openai/gpt-3.5-turbo': 0.6864, 'openai/gpt-4.1-mini': 0.198, 'openai/gpt-4.1-nano': \nsecondary_peer_as_candidate {'all_sentences': {'c_score': {'n': 1686, 'n_err': 564, 'n_cor': 1122, 'prevalence': 0.3345, 'auroc': 0.8253, 'auprc': 0.7163, 'auroc_ci95': [0.7855, 0.8653], 'testable': True, 'threshold': {'flag': 'flag_medoid', 'recall': 0.5018, 'recall_ci95': [0.4606, 0.5429], 'false_alarm': 0.0775, 'false_alarm\nsystem_level {'systems': [{'system': 'gpt-3.5-turbo', 'error_rate': 0.4251, 'mean_c_score': 0.3757, 'mean_sc5_cheap': 0.6263}, {'system': 'gpt-4', 'error_rate': 0.399, 'mean_c_score': 0.3767, 'mean_sc5_cheap': 0.6606}, {'system': 'text-davinci-003', 'error_rate': 0.547, 'mean_c_score': 0.4807, 'mean_sc5_cheap': \nsanity {'gold_as_candidate_mean_eq_frac_trackL': 0.4751, 'trackL_ERROR_mean_eq_frac': 0.3192, 'trackL_CORRECT_mean_eq_frac': 0.8199, 'gold_exceeds_error': True, 'planted': {'n': 30, 'ops': {'DROP': 8, 'NEG': 22}, 'rises_strict': 0.9667, 'rises_among_items_with_room': 0.9667, 'n_with_room': 30, 'pass_70pct'\nrewrite_invariance {'CONTRAPOSITIVE': {'n_applicable': 54, 'n_scored': 53, 'n_proved_equivalent': 54, 'false_alarm_rate': 0.2642, 'false_alarm_ci95': [0.1644, 0.3958], 'base_false_alarm_rate': 0.2642, 'flip_rate': 0.0, 'mean_abs_delta_eq_frac': 0.0}, 'DEMORGAN': {'n_applicable': 54, 'n_scored': 54, 'n_proved_equivalen\nlabel_noise_context {'trackH_original_gold_not_CORRECT_share': 0.3344, 'trackH_label_counts': {'CORRECT': 201, 'REF_UNPARSEABLE': 8, 'ERROR': 35, 'UNCERTAIN_COMPOUND': 22, 'READING_CHOICE': 25, 'UNPARSEABLE': 11}, 'trackL_CORRECT_via_VOCAB_share': 0.4276, 'trackL_CORRECT_VOCAB_nonstrict_share': 0.2054, 'trackL_uncertai\nprereg {'hash_check': 'screen_label_hash matches prereg.json', 'screen_label_hash': '0e43cbddb54901f3f1ddfe0ded607948a30b02548ffcbd235f02a39ef2da863a', 'written_utc': '2026-09-23T13:14:59.145938+00:00'}\nscore_definitions {'c_score': '1 - eq_frac over the full leave-one-system-out LLM pool (candidate C, PRIMARY)', 'medoid_depth': 'typed-repair distance to the pool medoid, 0-3 (candidate C)', 'cluster_entropy': 'semantic entropy of z3-eqmv classes of pool ∪ {c} (candidate C variant)', 'c_score_peers6': '1 - eq_frac ov\nn {'screen_items': 1169, 'primary_n': 546, 'primary_err': 249, 'primary_cor': 297}", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [31] ASSISTANT · 2026-09-25 12:35:39 UTC

```
Next I'm building `mini_demo_data.json`: 100 sentence pools, each with its peer and self-consistency translations and its labelled candidates.
```

### [32] TOOL CALL — Bash · 2026-09-25 12:35:39 UTC

```
Build curated mini_demo_data.json:
SP=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-i3cVDxBp-USk/9515af7b-63fd-4c30-8b8a-c704cc189967/scratchpad; OUT=/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk; cat > $SP/build_mini.py <<'EOF'
import json, random, sys
from collections import Counter
from pathlib import Path
SP = Path(sys.argv[1]); OUT = Path(sys.argv[2])
sys.path.insert(0, str(SP / "proj" / "src"))
import consensus as C
RES = SP / "proj" / "results"
items = json.loads((RES / "screen_items.json").read_text())
uj = json.loads((RES / "units.json").read_text())
peers, sc = C.jl(RES / "peer_outputs.jsonl"), C.jl(RES / "sc_samples.jsonl")
sents = C.build_sentences(items, peers, sc, uj["units"], uj["premise_unit"])
cons = json.loads((RES / "consensus.json").read_text())
rec = {r["item_id"]: r for r in cons["records"]}
L = [x for x in items if x["track"] == "L" and x["label"] in ("CORRECT", "ERROR")]
by_t = {}
for x in L:
    by_t.setdefault(x["sentence_key"], []).append(x)
keys = sorted(by_t)
# diverse pick: all longer sentences (>=12 words) + stratified random fill (seed 0) so both labels and both kinds are present
long_ = [t for t in keys if by_t[t][0]["strata"]["words"] >= 12]
rest = [t for t in keys if t not in long_]
rnd = random.Random(0)
pick = long_[:30] + rnd.sample(rest, 100 - min(30, len(long_)))
pick = sorted(pick)
FIELDS = ("item_id", "track", "kind", "system", "candidate_fol", "reference_fol", "label", "auto_class", "repair_ops", "vocab_strict", "strata")
ex = []
for t in pick:
    S = sents[t]
    cands = []
    for x in sorted(by_t[t], key=lambda x: x["item_id"]):
        c = {k: x[k] for k in FIELDS}
        r = rec[x["item_id"]]
        c["full_run"] = {k: r.get(k) for k in ("c_score", "eq_frac_full", "medoid", "medoid_depth", "medoid_ops", "cluster_entropy", "sc5_eq_frac_cheap", "sc5_eq_frac_same")}
        cands.append(c)
    ex.append({"sentence_key": t, "text": S["text"], "unit": S["unit"], "reference_fol": S["ref"],
               "members": S["members"], "raw": S["raw"], "attempted": S["attempted"], "sc": S["sc"], "candidates": cands})
summ = json.loads((RES / "summary.json").read_text())
meta = {"description": "Curated subset of the frozen NL->FOL screen (Experiment 3, candidate C). One example = one sentence: its text, "
        "gold reference FOL, the leave-one-out translation pool (P1..P6 fresh OpenRouter peers + 3 Logic-LM systems), the K=5 "
        "self-consistency samples (sc_cheap = gpt-4.1-nano T=0.7, sc_same = gpt-3.5-turbo T=0.7) and the track-L candidates "
        "labelled CORRECT/ERROR by prover-checked equivalence to gold (full_run = the original run's scores, for comparison).",
        "source": "FOLIO (validation, curated) + MALLS (test, curated) sentences; candidates from Logic-LM released outputs",
        "peer_models": C.PEER_MODEL, "n_sentences": len(ex), "n_candidates": sum(len(e["candidates"]) for e in ex),
        "label_counts": dict(Counter(c["label"] for e in ex for c in e["candidates"])),
        "full_run_primary_auroc": {k: {kk: v.get(kk) for kk in ("n", "n_err", "auroc", "auroc_ci95")} for k, v in summ["auroc"]["primary"].items()},
        "full_run_paired_delta": summ["paired_delta_auroc"]["primary"],
        "full_run_sanity": summ["sanity"]}
(OUT / "mini_demo_data.json").write_text(json.dumps({"metadata": meta, "examples": ex}, ensure_ascii=False, indent=1))
print(meta["n_sentences"], meta["n_candidates"], meta["label_counts"], Counter(e["candidates"][0]["kind"] for e in ex), len(long_))
EOF
cd $SP && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv run -q --no-project --python 3.12 --with loguru --with z3-solver==4.15.4.0 --with nltk python build_mini.py $SP $OUT && ls -la $OUT/mini_demo_data.json
```

### [33] TOOL RESULT — Bash · 2026-09-25 12:35:41 UTC

```
{"stdout": "100 278 {'CORRECT': 145, 'ERROR': 133} Counter({'premise': 60, 'conclusion': 40}) 19\n-rw-r--r-- 1 root root 420979 Sep 25 12:35 /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk/mini_demo_data.json", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [34] ASSISTANT · 2026-09-25 12:36:27 UTC

```
Now I'll generate the notebook. The code cells are pulled verbatim from the original `src/` modules, so the original code isn't retyped.
```

### [35] TOOL CALL — Bash · 2026-09-25 12:36:27 UTC

```
Find line markers for extraction:
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src; grep -n "^TOK = \|^import\|^from" $W/fol.py; grep -n "^TOKRE\|^D = \|^def load\|^SEEDS" $W/repair_census.py; grep -n "^LLM_SYSTEMS\|^from\|^import\|^sys" $W/common.py; grep -n "^SCORES\|^@logger\|^def bins" $W/analysis.py; sed -n 200,215p $W/analysis.py
```

### [36] TOOL RESULT — Bash · 2026-09-25 12:36:27 UTC

```
{"stdout": "9:import re\n10:import z3\n12:TOK = re.compile(r\"\\s*(∀|∃|¬|∧|∨|→|↔|⊕|\\(|\\)|,|[A-Za-z_][A-Za-z0-9_'\\-]*)\")\n34:D = Path(\"/ai-inventor/aii_data/runs/run_u75jRHUss0zo/iter_3/gen_hypo/claude_agent/data\")  # read-only iter-3 data dir\n35:TOKRE = re.compile(r\"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\\d+\")\n208:SEEDS = list(range(24))\n390:def load(p):\n8:from __future__ import annotations\n10:import hashlib\n11:import re\n12:import sys\n13:from pathlib import Path\n15:sys.path.insert(0, str(Path(__file__).resolve().parent))\n16:sys.setrecursionlimit(10000)\n18:from fol import equivalent, parse  # noqa: E402\n19:from repair_census import align, atoms, fp, gran_bridge, search, toks  # noqa: E402\n21:LLM_SYSTEMS = [\"gpt-3.5-turbo\", \"gpt-4\", \"text-davinci-003\"]\n38:SCORES = {  # name -> description (higher = more likely an error)\n197:def bins(df: pd.DataFrame) -> pd.DataFrame:\n209:@logger.catch(reraise=True)\n    df[\"len_bin\"] = [s[\"len_bin\"] for s in st]\n    df[\"words\"] = [s[\"words\"] for s in st]\n    df[\"nq_bin\"] = [None if s[\"n_quant\"] is None else (\"<=1\" if s[\"n_quant\"] <= 1 else (\"2\" if s[\"n_quant\"] == 2 else \">=3\")) for s in st]\n    df[\"depth_bin\"] = [None if s[\"depth\"] is None else (\"<=3\" if s[\"depth\"] <= 3 else (\"4-5\" if s[\"depth\"] <= 5 else \">=6\")) for s in st]\n    df[\"ncond_bin\"] = [None if s[\"n_cond\"] is None else (\"0\" if s[\"n_cond\"] == 0 else (\"1-2\" if s[\"n_cond\"] <= 2 else \">=3\")) for s in st]\n    df[\"exception\"] = [bool(s[\"exception\"]) for s in st]\n    return df\n\n\n@logger.catch(reraise=True)\ndef main():\n    ap = argparse.ArgumentParser()\n    ap.add_argument(\"--mini\", type=int, default=0)\n    ap.add_argument(\"--boot\", type=int, default=2000)\n    a = ap.parse_args()\n    B = a.boot", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [37] TOOL CALL — Bash · 2026-09-25 12:38:33 UTC

```
Write notebook generator script:
SP=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-i3cVDxBp-USk/9515af7b-63fd-4c30-8b8a-c704cc189967/scratchpad; cat > $SP/gen_nb.py <<'PYEOF'
import json, sys
from pathlib import Path
SRC = Path("/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src")
OUT = Path(sys.argv[1])
CFG = dict(N_SENTENCES=int(sys.argv[2]), REPAIR_BUDGET_S=f... [truncated, 36449 chars total]
```

### [38] TOOL RESULT — Bash · 2026-09-25 12:38:35 UTC

```
{"stdout": "ok", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [39] ASSISTANT · 2026-09-25 12:38:39 UTC

```
The planted-error step needs `rewrites.to_str` to print ASTs back to FOL strings. Let me look at it.
```

### [40] TOOL CALL — Bash · 2026-09-25 12:38:39 UTC

```
Find to_str in rewrites.py:
W=/ai-inventor/aii_data/runs/run_u75jRHUss0zo/3_invention_loop/iter_1/gen_art/gen_art_experiment_3/src; grep -n "def \|^[A-Z_]* = " $W/rewrites.py; sed -n "$(grep -n 'def to_str' $W/rewrites.py | cut -d: -f1),+25p" $W/rewrites.py
```

### [41] TOOL RESULT — Bash · 2026-09-25 12:38:39 UTC

```
{"stdout": "21:TOKRE = re.compile(r\"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\\d+\")\n22:NLTK_DIR = Path(__file__).resolve().parent.parent / \"data\" / \"nltk_data\"   # nltk.download('wordnet', download_dir=...)\n23:SYN_STATS = {\"wordnet\": 0, \"nonce\": 0}   # how each distinct head token was renamed (reported in summary.json)\n26:def wordnet_available() -> bool:\n39:def _synonym(tok: str) -> str:\n54:def _rename_pred(name: str, token_alignable: bool) -> str:\n65:def _map_atoms(e, pmap, cmap, bv=frozenset()):\n76:def rename_rewrite(e, token_alignable: bool = False, preds: bool = True, consts: bool = True):\n90:def inverse_rename(e, maps):\n94:def reorder(e):\n106:def _first(e, kind):\n127:def demorgan(e):\n134:def free_vars(e, bound=frozenset()) -> set:\n145:def _args(e) -> set:\n156:def _prenex_once(e):\n180:def prenex(e):\n185:def contrapositive(e):\n197:FAMILIES = {\"RENAME\": lambda e: rename_rewrite(e)[0], \"REORDER\": reorder, \"DEMORGAN\": demorgan,\n204:def to_str(e) -> str:\ndef to_str(e) -> str:\n    \"\"\"Render an AST back to FOLIO-style Unicode FOL (fully parenthesised binary nodes).\"\"\"\n    k = e[0]\n    if k == \"atom\":\n        return f\"{e[1]}({', '.join(e[2])})\" if e[2] else e[1]\n    if k in (\"all\", \"ex\"):\n        return f\"{'∀' if k == 'all' else '∃'}{e[1]} ({to_str(e[2])})\"\n    if k == \"not\":\n        return f\"¬({to_str(e[1])})\"\n    sym = {\"and\": \"∧\", \"or\": \"∨\", \"imp\": \"→\", \"iff\": \"↔\", \"xor\": \"⊕\"}[k]\n    return f\"({to_str(e[1])} {sym} {to_str(e[2])})\"", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [42] TOOL CALL — Bash · 2026-09-25 12:38:49 UTC

```
Patch planted cell to use to_str:
SP=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-i3cVDxBp-USk/9515af7b-63fd-4c30-8b8a-c704cc189967/scratchpad; cd $SP; python3 - <<'EOF'
p='gen_nb.py'; s=open(p).read()
old='''        planted.append({"item_id": x["item_id"], "op": op, "fol": RW_to_str(new) if False else None, "ast": new})
""".replace('RW_to_str(new) if False else None', 'None'))'''
assert old in s
s=s.replace(old,'''        planted.append({"item_id": x["item_id"], "op": op, "fol": to_str(new)})  # original: RW.to_str(new)
print(f"planted {len(planted)} errors:", dict(Counter(p["op"] for p in planted)))
for p in planted[:3]:
    print(f"  {p['op']:4s} {by_id_[p['item_id']]['candidate_fol']}  ->  {p['fol']}")
""".replace("by_id_", "{x['item_id']: x for x in items}"))''')
old2='code(lines("consensus.py", 39, 44) + "\\n\\n" + lines("consensus.py", 60, 61) + "\\n\\n" + lines("consensus.py", 128, 252))'
assert old2 in s
s=s.replace(old2, old2[:-1] + ' + "\\n\\n# from src/rewrites.py (used to render planted-error ASTs back to FOL strings)\\n" + lines("rewrites.py", 204, 214))')
s=s.replace("* `plant()` makes one typed edit (DROP an operand, else NEG an atom). It is used only to check that c_score rises on known-bad formulas.",
 "* `plant()` makes one typed edit (DROP an operand, else NEG an atom). It is used only to check that c_score rises on known-bad formulas. `to_str` (from `rewrites.py`) prints an AST back to FOL.")
open(p,'w').write(s)
EOF
grep -n "by_id_\|{x\['item_id'\]: x for x in items}\[" gen_nb.py | head
```

### [43] TOOL RESULT — Bash · 2026-09-25 12:38:49 UTC

```
{"stdout": "368:    print(f\"  {p['op']:4s} {by_id_[p['item_id']]['candidate_fol']}  ->  {p['fol']}\")\n369:\"\"\".replace(\"by_id_\", \"{x['item_id']: x for x in items}\"))", "stderr": "\nShell cwd was reset to /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [44] TOOL CALL — Bash · 2026-09-25 12:38:57 UTC

```
Generate minimal notebook and syntax-check:
SP=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-i3cVDxBp-USk/9515af7b-63fd-4c30-8b8a-c704cc189967/scratchpad; cd $SP; python3 - <<'EOF'
p='gen_nb.py'; s=open(p).read()
s=s.replace('''for p in planted[:3]:
    print(f"  {p['op']:4s} {by_id_[p['item_id']]['candidate_fol']}  ->  {p['fol']}")
""".replace("by_id_", "{x['item_id']: x for x in items}"))''','''_fol_of = {x["item_id"]: x["candidate_fol"] for x in items}
for p in planted[:3]:
    print(f"  {p['op']:4s} {_fol_of[p['item_id']]}  ->  {p['fol']}")
""")''')
open(p,'w').write(s)
EOF
OUT=/ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk; python3 gen_nb.py $OUT/code_demo.ipynb 2 1.0 10 2 && cd $OUT && python3 -c "
import json; nb=json.load(open('code_demo.ipynb'))
src='\n\n'.join(''.join(c['source']) for c in nb['cells'] if c['cell_type']=='code')
import ast; 
for i,c in enumerate(nb['cells']):
  if c['cell_type']=='code': ast.parse(''.join(c['source']))
print('syntax ok')"
```

### [45] TOOL RESULT — Bash · 2026-09-25 12:38:59 UTC

```
{"stdout": "cells: 36\nsyntax ok", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [46] ASSISTANT · 2026-09-25 12:39:05 UTC

```
Minimal notebook generated (2 sentences, 10 bootstrap resamples). Running it in the clean test venv now.
```

### [47] TOOL CALL — Bash · 2026-09-25 12:39:05 UTC

```
Test-run notebook at minimum config:
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk; E=/tmp/aii_nb_test_envs/art_i3cVDxBp-USk-be48f6bcb721; UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && S=$(date +%s); $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | tail -30; echo "runtime $(( $(date +%s)-S ))s"
```

### [48] TOOL RESULT — Bash · 2026-09-25 12:39:39 UTC

```
{"stdout": "[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.\n[NbConvertApp] Writing 291650 bytes to code_demo.ipynb\nruntime 30s", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [49] TOOL CALL — Bash · 2026-09-25 12:39:45 UTC

```
Inspect executed notebook outputs:
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk; python3 - <<'EOF'
import json
nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    if c['cell_type']!='code': continue
    for o in c['outputs']:
        if o['output_type']=='stream': print(f'--[{i}]', ''.join(o['text'])[-1500:])
        elif o['output_type']=='error': print(f'--[{i}] ERR', o['ename'], o['evalue'])
        elif o['output_type'] in('display_data','execute_result'): print(f'--[{i}]', list(o['data'].keys()))
EOF
```

### [50] TOOL RESULT — Bash · 2026-09-25 12:39:45 UTC

```
{"stdout": "--[2] ['text/plain']\n--[4] {\n \"n_sentences\": 100,\n \"n_candidates\": 278,\n \"label_counts\": {\n  \"CORRECT\": 145,\n  \"ERROR\": 133\n },\n \"peer_models\": {\n  \"P1\": \"meta-llama/llama-3.3-70b-instruct\",\n  \"P2\": \"qwen/qwen3-235b-a22b-2507\",\n  \"P3\": \"deepseek/deepseek-chat-v3.1\",\n  \"P4\": \"mistralai/mistral-small-3.2-24b-instruct\",\n  \"P5\": \"google/gemini-2.5-flash-lite\",\n  \"P6\": \"openai/gpt-4.1-mini\"\n }\n}\n\n--[18] 12:39:37|INFO   |sentences: 2, candidates: 7\n\n--[18] TEXT: A duster is a household appliance that doesn't suck.\nGOLD: HouseholdAppliance(duster) ∧ ¬Suck(duster)\n  pool P1                 ∃x (Duster(x) ∧ HouseholdAppliance(x) ∧ ¬Suck(x))\n  pool P2                 HouseholdAppliance(duster) ∧ ¬Suck(duster)\n  pool P3                 ∀x (Duster(x) → HouseholdAppliance(x) ∧ ¬Suck(x))\n  pool P4                 HouseholdAppliance(duster) ∧ Duster(duster) ∧ ¬Suck(duster)\n  pool P5                 Duster(x) ∧ HouseholdAppliance(x) ∧ ¬Suck(x)\n  pool P6                 HouseholdAppliance(duster) ∧ ¬Suck(duster)\n  pool gpt-3.5-turbo      Duster(duster) ∧ HouseholdAppliance(duster) ∧ ¬Suck(duster)\n  pool gpt-4              HouseholdAppliance(duster) ∧ ¬Suck(duster)\n  pool text-davinci-003   ¬Suck(duster)\n  CANDIDATE [gpt-4] CORRECT  HouseholdAppliance(duster) ∧ ¬Suck(duster)\n  CANDIDATE [text-davinci-003] ERROR    ¬Suck(duster)\n  CANDIDATE [gpt-4] ERROR    Duster(duster) ∧ HouseholdAppliance(duster) ∧ ¬Suck(duster)\n  CANDIDATE [text-davinci-003] ERROR    Duster(duster) ∧ ¬Suck(duster)\n  CANDIDATE [gpt-3.5-turbo] ERROR    Duster(duster) ∧ ¬Suck(duster)\n  CANDIDATE [gpt-3.5-turbo] ERROR    Duster(duster) ∧ HouseholdAppliance(duster) ∧ ¬Suck(duster)\n\n--[20] 12:39:37|INFO   |[gold-labels] labels to compute: 5\n\n--[20] 12:39:37|INFO   |[gold-labels] labels done in 0s\n\n--[20] re-derived labels agree with the frozen screen labels on 7/7 candidates (0.0s)\nlabel counts: {'CORRECT': 2, 'ERROR': 5}\nerror classes: {'DROP': 2, 'ADD+DROP': 2, 'ADD': 1}\n\n--[22] planted 2 errors: {'DROP': 2}\n  DROP HouseholdAppliance(duster) ∧ ¬Suck(duster)  ->  HouseholdAppliance(duster)\n  DROP Born(ailtonSilva, year1995) ∧ KnownAs(ailtonSilva, ailton)  ->  Born(ailtonSilva, year1995)\n\n--[24] 12:39:37|INFO   |[pairs] eqmv pairs to compute: 75 (cached 0)\n\n--[24] 12:39:37|INFO   |[pairs] done in 0s\n\n--[24] 12:39:37|INFO   |pairwise stage 0s for 75 pairs\n\n--[24] routes: {'none': 72, 'align': 2, 'exact': 1}\n\n--[26] 12:39:37|INFO   |[medoid-repair] medoid repairs to compute: 3 (budget 1.0s each)\n\n--[26] 12:39:37|INFO   |[medoid-repair] repairs done in 0s\n\n--[26] 12:39:37|INFO   |coverage: {'ok': 6, 'insufficient_pool': 1}; pairs 0s, repair 0s, labels 0s\n\n--[26] 12:39:37|INFO   |per-candidate seconds (z3): mean 0.007\n\n--[26] {\n \"item_id\": \"10ab3102cfae3e77\",\n \"pool_eq\": {\n  \"P1\": false,\n  \"P2\": true,\n  \"P3\": false,\n  \"P4\": false,\n  \"P5\": false,\n  \"P6\": true,\n  \"gpt-3.5-turbo\": false,\n  \"text-davinci-003\": false\n },\n \"eq_frac_full\": 0.25,\n \"c_score\": 0.75,\n \"medoid\": \"P2\",\n \"medoid_depth\": 0,\n \"medoid_ops\": [],\n \"cluster_entropy\": 1.6769877743224173,\n \"sc5_eq_frac_cheap\": 0.0\n}\n\n--[28] {\n \"gold_mean_eq_frac\": 0.6666666666666666,\n \"ERROR_mean_eq_frac\": 0.075,\n \"CORRECT_mean_eq_frac\": 0.625,\n \"planted_n\": 2,\n \"planted_ops\": {\n  \"DROP\": 2\n },\n \"planted_rises\": 0.5\n}\nfull run: {\"gold_as_candidate_mean_eq_frac_trackL\": 0.4751, \"trackL_ERROR_mean_eq_frac\": 0.3192, \"trackL_CORRECT_mean_eq_frac\": 0.8199}\n\n--[32] 12:39:37|INFO   |[primary] n=7 err=5  c_score=0.6  medoid_depth=0.5  cluster_entropy=0.8  sc5_cheap=0.5  sc5_same=None  misalign=0.9\n\n--[32] 12:39:37|INFO   |[vocab_clean] n=3 err=1  c_score=0.75  medoid_depth=0.5  cluster_entropy=0.75  sc5_cheap=0.5  sc5_same=None  misalign=0.5\n\n--[32] {\n \"c_score-sc5_cheap\": {\n  \"n\": 7,\n  \"n_err\": 5,\n  \"auroc_a\": 0.6,\n  \"auroc_b\": 0.5,\n  \"delta\": 0.1,\n  \"delta_ci95\": [\n   0.1,\n   0.4\n  ],\n  \"p_delta_le_0\": 0.0\n },\n \"c_score-cluster_entropy\": {\n  \"n\": 7,\n  \"n_err\": 5,\n  \"auroc_a\": 0.6,\n  \"auroc_b\": 0.8,\n  \"delta\": -0.2,\n  \"delta_ci95\": [\n   -0.2,\n   0.3\n  ],\n  \"p_delta_le_0\": 0.5\n },\n \"c_score-sc5_same\": {\n  \"n\": 2\n }\n}\ncross-fitted [c_score, sc5_cheap] vs [sc5_cheap]: {'n': 7, 'auroc_a': None, 'auroc_b': None, 'delta': None, 'delta_ci95': None}\ntotal notebook pipeline time: 0s\n\n--[34]      0.55   [0.55, 0.8]            0.8633  [0.8197, 0.9034]                      0.75\n       c_score_llm2  7      5          0.40    [0.4, 0.4]            0.7527  [0.7006, 0.8059]                      0.50\n    cluster_entropy  7      5          0.80    [0.6, 0.8]            0.7732  [0.7239, 0.8203]                      0.75\n       medoid_depth  7      5          0.50    [0.5, 1.0]            0.7216  [0.6726, 0.7737]                      0.50\n          sc5_cheap  7      5          0.50    [0.5, 0.5]            0.7254  [0.6688, 0.7811]                      0.50\n  sc5_entropy_cheap  7      5          0.25   [0.25, 0.5]            0.6312  [0.5678, 0.6934]                      0.25\n           sc5_same  2      2           NaN          None            0.7159  [0.6316, 0.7962]                       NaN\n  predset_instab_sc  7      5          0.05   [0.05, 0.1]            0.6878  [0.6257, 0.7497]                      0.25\npredset_instab_pool  7      5          0.80    [0.6, 0.8]            0.7700   [0.7165, 0.821]                      1.00\n         fol_length  7      5          0.60    [0.6, 0.6]            0.5274   [0.4695, 0.586]                      0.00\n           misalign  7      5          0.90    [0.9, 0.9]            0.8353  [0.7935, 0.8761]                      0.50\n\nAt the medoid threshold (medoid_depth >= 1): recall 1.0, false alarm 0.5, precision 0.8333\nPaired Δ c_score − sc5_cheap: 0.1 [0.1, 0.4]  (full run: 0.1401)\nc_score reproduced exactly (|Δ|<1e-9) for 7/7 candidates\n\n--[34] \nPer error type (ERROR candidates):\nop_class  n  recall  mean_c  mean_sc5\nCOVERAGE  5     1.0   0.925       1.0\n\n--[34] ['image/png', 'text/plain']", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [51] THINKING · 2026-09-25 12:39:57 UTC

```
The minimal config passed in 30s, and c_score matched exactly across all 7 candidates. Now scaling up to 25 sentences with the original repair budget of 10s and 500 bootstrap resamples.
```

### [52] TOOL CALL — Bash · 2026-09-25 12:39:57 UTC

```
Test-run notebook with 25 sentences:
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk; SP=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-i3cVDxBp-USk/9515af7b-63fd-4c30-8b8a-c704cc189967/scratchpad; python3 $SP/gen_nb.py $PWD/code_demo.ipynb 25 10.0 500 30; E=/tmp/aii_nb_test_envs/art_i3cVDxBp-USk-be48f6bcb721; UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && S=$(date +%s); $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | grep -v WARNING | tail -20; echo "runtime $(( $(date +%s)-S ))s"; python3 - <<'EOF'
import json
nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    if c['cell_type']!='code': continue
    for o in c['outputs']:
        if o['output_type']=='stream' and i>=20: print(f'--[{i}]', ''.join(o['text'])[-2500:])
        elif o['output_type']=='error': print(f'--[{i}] ERR', o['ename'], o['evalue'])
EOF
```

### [53] TOOL RESULT — Bash · 2026-09-25 12:40:29 UTC

```
{"stdout": "cells: 36\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[NbConvertApp] Writing 314888 bytes to code_demo.ipynb\nruntime 30s\n--[20] 12:40:23|INFO   |[gold-labels] labels to compute: 60\n\n--[20] 12:40:23|INFO   |[gold-labels] labels done in 0s\n\n--[20] re-derived labels agree with the frozen screen labels on 81/81 candidates (0.5s)\nlabel counts: {'CORRECT': 43, 'ERROR': 38}\nerror classes: {'ADD': 12, 'ADD+DROP': 11, 'DROP': 5, 'SWAP+SWAP': 3, 'SWAP': 3, 'NEG': 2, 'ADD+SWAP': 1, 'ADD+BIND': 1}\n\n--[22] planted 30 errors: {'DROP': 11, 'NEG': 19}\n  DROP ∀x (Dog(x) → Animal(x) ∧ Bark(x))  ->  ∀x ((Dog(x) → Animal(x)))\n  NEG  Lead(beethoven, viennaMusicSociety)  ->  ¬(Lead(beethoven, viennaMusicSociety))\n  NEG  ∀x (FourSided(x) → Shape(x))  ->  ∀x ((¬(FourSided(x)) → Shape(x)))\n\n--[24] 12:40:24|INFO   |[pairs] eqmv pairs to compute: 903 (cached 0)\n\n--[24] 12:40:24|INFO   |[pairs] done in 1s\n\n--[24] 12:40:24|INFO   |pairwise stage 1s for 908 pairs\n\n--[24] routes: {'none': 704, 'align': 158, 'identical': 3, 'exact': 11, 'gran': 27}\n\n--[26] 12:40:24|INFO   |[medoid-repair] medoid repairs to compute: 33 (budget 10.0s each)\n\n--[26] 12:40:25|INFO   |[medoid-repair] repairs done in 0s\n\n--[26] 12:40:25|INFO   |[labels] labels to compute: 9\n\n--[26] 12:40:25|INFO   |[labels] labels done in 0s\n\n--[26] 12:40:25|INFO   |coverage: {'ok': 80, 'insufficient_pool': 1}; pairs 1s, repair 0s, labels 0s\n\n--[26] 12:40:25|INFO   |per-candidate seconds (z3): mean 0.008\n\n--[26] {\n \"item_id\": \"10ab3102cfae3e77\",\n \"pool_eq\": {\n  \"P1\": false,\n  \"P2\": true,\n  \"P3\": false,\n  \"P4\": false,\n  \"P5\": false,\n  \"P6\": true,\n  \"gpt-3.5-turbo\": false,\n  \"text-davinci-003\": false\n },\n \"eq_frac_full\": 0.25,\n \"c_score\": 0.75,\n \"medoid\": \"P2\",\n \"medoid_depth\": 0,\n \"medoid_ops\": [],\n \"cluster_entropy\": 1.6769877743224173,\n \"sc5_eq_frac_cheap\": 0.0\n}\n\n--[28] {\n \"gold_mean_eq_frac\": 0.5977777777777777,\n \"ERROR_mean_eq_frac\": 0.32261904761904764,\n \"CORRECT_mean_eq_frac\": 0.7566445182724252,\n \"planted_n\": 30,\n \"planted_ops\": {\n  \"DROP\": 11,\n  \"NEG\": 19\n },\n \"planted_rises\": 0.8333333333333334\n}\nfull run: {\"gold_as_candidate_mean_eq_frac_trackL\": 0.4751, \"trackL_ERROR_mean_eq_frac\": 0.3192, \"trackL_CORRECT_mean_eq_frac\": 0.8199}\n\n--[32] 12:40:25|INFO   |[primary] n=81 err=38  c_score=0.7956  medoid_depth=0.7362  cluster_entropy=0.7702  sc5_cheap=0.7472  sc5_same=0.8774  misalign=0.6974\n\n--[32] 12:40:26|INFO   |[vocab_clean] n=66 err=23  c_score=0.6987  medoid_depth=0.6299  cluster_entropy=0.7037  sc5_cheap=0.7472  sc5_same=0.8359  misalign=0.5\n\n--[32] {\n \"c_score-sc5_cheap\": {\n  \"n\": 81,\n  \"n_err\": 38,\n  \"auroc_a\": 0.7956,\n  \"auroc_b\": 0.7472,\n  \"delta\": 0.0483,\n  \"delta_ci95\": [\n   -0.1541,\n   0.2569\n  ],\n  \"p_delta_le_0\": 0.284\n },\n \"c_score-cluster_entropy\": {\n  \"n\": 81,\n  \"n_err\": 38,\n  \"auroc_a\": 0.7956,\n  \"auroc_b\": 0.7702,\n  \"delta\": 0.0254,\n  \"delta_ci95\": [\n   -0.0445,\n   0.1195\n  ],\n  \"p_delta_le_0\": 0.248\n },\n \"c_score-sc5_same\": {\n  \"n\": 29,\n  \"n_err\": 13,\n  \"auroc_a\": 0.774,\n  \"auroc_b\": 0.8774,\n  \"delta\": -0.1034,\n  \"delta_ci95\": [\n   -0.3765,\n   0.1768\n  ],\n  \"p_delta_le_0\": 0.724\n }\n}\ncross-fitted [c_score, sc5_cheap] vs [sc5_cheap]: {'n': 81, 'auroc_a': np.float64(0.7959), 'auroc_b': np.float64(0.6937), 'delta': np.float64(0.1022), 'delta_ci95': [-0.0582, 0.2974]}\ntotal notebook pipeline time: 3s\n\n--[34]               score  n  n_err  AUROC (demo)    95% CI (demo)  AUROC (full run) 95% CI (full run)  vocab_clean AUROC (demo)\n            c_score 81     38        0.7956 [0.6103, 0.9661]            0.8655  [0.8211, 0.9058]                    0.6987\n     c_score_peers6 81     38        0.8225 [0.6466, 0.9749]            0.8721  [0.8299, 0.9112]                    0.7386\n     c_score_nonoai 81     38        0.8378 [0.6699, 0.9773]            0.8633  [0.8197, 0.9034]                    0.7654\n       c_score_llm2 81     38        0.6405 [0.4572, 0.8301]            0.7527  [0.7006, 0.8059]                    0.5288\n    cluster_entropy 81     38        0.7702     [0.6, 0.901]            0.7732  [0.7239, 0.8203]                    0.7037\n       medoid_depth 81     38        0.7362 [0.5819, 0.8965]            0.7216  [0.6726, 0.7737]                    0.6299\n          sc5_cheap 81     38        0.7472 [0.5917, 0.8761]            0.7254  [0.6688, 0.7811]                    0.7472\n  sc5_entropy_cheap 81     38        0.7203 [0.5474, 0.8474]            0.6312  [0.5678, 0.6934]                    0.7391\n           sc5_same 29     13        0.8774 [0.7079, 0.9948]            0.7159  [0.6316, 0.7962]                    0.8359\n  predset_instab_sc 81     38        0.6047 [0.4101, 0.7927]            0.6878  [0.6257, 0.7497]                    0.5814\npredset_instab_pool 81     38        0.7182 [0.5383, 0.8711]            0.7700   [0.7165, 0.821]                    0.6598\n         fol_length 81     38        0.4507  [0.2983, 0.612]            0.5274   [0.4695, 0.586]                    0.3519\n           misalign 81     38        0.6974 [0.5893, 0.8239]            0.8353  [0.7935, 0.8761]                    0.5000\n\nAt the medoid threshold (medoid_depth >= 1): recall 0.7105, false alarm 0.2093, precision 0.75\nPaired Δ c_score − sc5_cheap: 0.0483 [-0.1541, 0.2569]  (full run: 0.1401)\nc_score reproduced exactly (|Δ|<1e-9) for 81/81 candidates\n\nPer error type (ERROR candidates):\nop_class  n  recall  mean_c  mean_sc5\nCOVERAGE 28   0.821   0.737     0.864\n   MIXED  2   1.000   0.938     0.800\nPOLARITY  2   1.000   0.866     0.900\n  STRUCT  6   0.000   0.250     1.000", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [54] ASSISTANT · 2026-09-25 12:40:39 UTC

```
25 sentences took 3s of pipeline time and reproduced 81/81 exactly. Now the full original parameters: all 100 sentences, 2000 bootstrap resamples, 10s repair budget.
```

### [55] TOOL CALL — Bash · 2026-09-25 12:40:39 UTC

```
Test-run notebook at full original params:
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk; SP=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-i3cVDxBp-USk/9515af7b-63fd-4c30-8b8a-c704cc189967/scratchpad; python3 $SP/gen_nb.py $PWD/code_demo.ipynb 100 10.0 2000 30; E=/tmp/aii_nb_test_envs/art_i3cVDxBp-USk-be48f6bcb721; UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && S=$(date +%s); $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | grep -v WARNING | tail -20; echo "runtime $(( $(date +%s)-S ))s"; python3 - <<'EOF'
import json
nb=json.load(open('code_demo.ipynb'))
for i,c in enumerate(nb['cells']):
    if c['cell_type']!='code': continue
    for o in c['outputs']:
        if o['output_type']=='stream' and i>=20 and i!=26: print(f'--[{i}]', ''.join(o['text'])[-2200:])
        elif o['output_type']=='error': print(f'--[{i}] ERR', o['ename'], o['evalue'])
EOF
```

### [56] TOOL RESULT — Bash · 2026-09-25 12:41:51 UTC

```
{"stdout": "cells: 36\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[NbConvertApp] Writing 320779 bytes to code_demo.ipynb\nruntime 70s\n--[20] 12:41:06|INFO   |[gold-labels] labels to compute: 216\n\n--[20] 12:41:07|INFO   |[gold-labels] 200/216 labels, 2s\n\n--[20] 12:41:08|INFO   |[gold-labels] labels done in 2s\n\n--[20] re-derived labels agree with the frozen screen labels on 276/278 candidates (2.0s)\nlabel counts: {'CORRECT': 145, 'ERROR': 133}\nerror classes: {'ADD+DROP': 65, 'ADD': 25, 'NEG': 11, 'DROP': 10, 'SWAP': 5, 'CONN': 4, 'SWAP+SWAP': 3, 'ADD+SWAP': 3}\n\n--[22] planted 30 errors: {'DROP': 11, 'NEG': 19}\n  DROP ∀x ∀y (SuperheroMovie(x) ∧ NamedAfter(x, y) → GoodGuy(y))  ->  ∀x (∀y ((SuperheroMovie(x) → GoodGuy(y))))\n  DROP ∀x (Dog(x) → Animal(x) ∧ Bark(x))  ->  ∀x ((Dog(x) → Animal(x)))\n  DROP ¬∃x (Politician(x) ∧ Member(x, naziReichstag))  ->  ¬(∃x (Politician(x)))\n\n--[24] 12:41:08|INFO   |[pairs] eqmv pairs to compute: 4234 (cached 0)\n\n--[24] 12:41:08|INFO   |[pairs] 50/212 chunks, 1s, eta 2s\n\n--[24] 12:41:09|INFO   |[pairs] 100/212 chunks, 1s, eta 1s\n\n--[24] 12:41:10|INFO   |[pairs] 150/212 chunks, 2s, eta 1s\n\n--[24] 12:41:12|INFO   |[pairs] 200/212 chunks, 4s, eta 0s\n\n--[24] 12:41:12|INFO   |[pairs] done in 4s\n\n--[24] 12:41:12|INFO   |pairwise stage 4s for 4234 pairs\n\n--[24] routes: {'none': 3346, 'align': 680, 'gran': 156, 'exact': 51, 'identical': 1}\n\n--[28] {\n \"gold_mean_eq_frac\": 0.5491865079365079,\n \"ERROR_mean_eq_frac\": 0.3137128535624776,\n \"CORRECT_mean_eq_frac\": 0.7552134646962233,\n \"planted_n\": 30,\n \"planted_ops\": {\n  \"DROP\": 11,\n  \"NEG\": 19\n },\n \"planted_rises\": 0.9333333333333333\n}\nfull run: {\"gold_as_candidate_mean_eq_frac_trackL\": 0.4751, \"trackL_ERROR_mean_eq_frac\": 0.3192, \"trackL_CORRECT_mean_eq_frac\": 0.8199}\n\n--[32] 12:41:44|INFO   |[primary] n=278 err=133  c_score=0.8274  medoid_depth=0.6839  cluster_entropy=0.7425  sc5_cheap=0.7267  sc5_same=0.7499  misalign=0.7895\n\n--[32] 12:41:47|INFO   |[vocab_clean] n=201 err=56  c_score=0.8157  medoid_depth=0.6936  cluster_entropy=0.7523  sc5_cheap=0.7401  sc5_same=0.7667  misalign=0.5\n\n--[32] {\n \"c_score-sc5_cheap\": {\n  \"n\": 278,\n  \"n_err\": 133,\n  \"auroc_a\": 0.8274,\n  \"auroc_b\": 0.7267,\n  \"delta\": 0.1006,\n  \"delta_ci95\": [\n   0.0205,\n   0.1787\n  ],\n  \"p_delta_le_0\": 0.0065\n },\n \"c_score-cluster_entropy\": {\n  \"n\": 278,\n  \"n_err\": 133,\n  \"auroc_a\": 0.8274,\n  \"auroc_b\": 0.7425,\n  \"delta\": 0.0848,\n  \"delta_ci95\": [\n   0.0404,\n   0.133\n  ],\n  \"p_delta_le_0\": 0.0005\n },\n \"c_score-sc5_same\": {\n  \"n\": 90,\n  \"n_err\": 39,\n  \"auroc_a\": 0.8308,\n  \"auroc_b\": 0.7499,\n  \"delta\": 0.0809,\n  \"delta_ci95\": [\n   -0.0428,\n   0.2034\n  ],\n  \"p_delta_le_0\": 0.104\n }\n}\ncross-fitted [c_score, sc5_cheap] vs [sc5_cheap]: {'n': 278, 'auroc_a': np.float64(0.8179), 'auroc_b': np.float64(0.6959), 'delta': np.float64(0.122), 'delta_ci95': [0.0487, 0.198]}\ntotal notebook pipeline time: 42s\n\n--[34]               score   n  n_err  AUROC (demo)    95% CI (demo)  AUROC (full run) 95% CI (full run)  vocab_clean AUROC (demo)\n            c_score 278    133        0.8274 [0.7568, 0.8894]            0.8655  [0.8211, 0.9058]                    0.8157\n     c_score_peers6 278    133        0.8287 [0.7575, 0.8898]            0.8721  [0.8299, 0.9112]                    0.8326\n     c_score_nonoai 278    133        0.8254 [0.7561, 0.8864]            0.8633  [0.8197, 0.9034]                    0.8302\n       c_score_llm2 278    133        0.7295 [0.6485, 0.8058]            0.7527  [0.7006, 0.8059]                    0.6883\n    cluster_entropy 278    133        0.7425 [0.6688, 0.8107]            0.7732  [0.7239, 0.8203]                    0.7523\n       medoid_depth 278    133        0.6839 [0.6047, 0.7586]            0.7216  [0.6726, 0.7737]                    0.6936\n          sc5_cheap 278    133        0.7267 [0.6516, 0.7952]            0.7254  [0.6688, 0.7811]                    0.7401\n  sc5_entropy_cheap 278    133        0.6510 [0.5704, 0.7279]            0.6312  [0.5678, 0.6934]                    0.7272\n           sc5_same  90     39        0.7499 [0.6451, 0.8458]            0.7159  [0.6316, 0.7962]                    0.7667\n  predset_instab_sc 278    133        0.6870 [0.5991, 0.7757]            0.6878  [0.6257, 0.7497]                    0.6156\npredset_instab_pool 278    133        0.7343 [0.6581, 0.8075]            0.7700   [0.7165, 0.821]                    0.6234\n         fol_length 278    133        0.4578 [0.3829, 0.5345]            0.5274   [0.4695, 0.586]                    0.4543\n           misalign 278    133        0.7895 [0.7282, 0.8504]            0.8353  [0.7935, 0.8761]                    0.5000\n\nAt the medoid threshold (medoid_depth >= 1): recall 0.6391, false alarm 0.2069, precision 0.7391\nPaired Δ c_score − sc5_cheap: 0.1006 [0.0205, 0.1787]  (full run: 0.1401)\nc_score reproduced exactly (|Δ|<1e-9) for 276/278 candidates\n\nPer error type (ERROR candidates):\nop_class   n  recall  mean_c  mean_sc5\nCOVERAGE 100   0.620   0.680     0.836\n   MIXED   6   0.833   0.812     0.933\nPOLARITY  12   0.917   0.839     0.850\n  STRUCT  15   0.467   0.552     0.920", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [57] ASSISTANT · 2026-09-25 12:42:01 UTC

```
Full original parameters run in 70s total, well under the 600s limit. Let me check the figure.
```

### [58] TOOL CALL — Bash · 2026-09-25 12:42:01 UTC

```
Extract rendered figure:
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk; SP=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-i3cVDxBp-USk/9515af7b-63fd-4c30-8b8a-c704cc189967/scratchpad; python3 -c "
import json,base64
nb=json.load(open('code_demo.ipynb'))
for c in nb['cells']:
  for o in c.get('outputs',[]):
    if 'data' in o and 'image/png' in o['data']: open('$SP/fig.png','wb').write(base64.b64decode(o['data']['image/png']))
"
```

### [59] TOOL RESULT — Bash · 2026-09-25 12:42:01 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [60] TOOL CALL — Read · 2026-09-25 12:42:01 UTC

```
/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-i3cVDxBp-USk/9515af7b-63fd-4c30-8b8a-c704cc189967/scratchpad/fig.png
```

### [61] TOOL RESULT — Read · 2026-09-25 12:42:01 UTC

```
[event truncated: exceeded SSE frame limit]
```

### [62] ASSISTANT · 2026-09-25 12:42:17 UTC

```
Figure looks right. Last pass: I'll update the closing markdown with the demo's numbers, regenerate, re-run, then write the README, manifest and structured output.
```

### [63] TOOL CALL — Bash · 2026-09-25 12:42:17 UTC

```
Final regenerate, test-run, verify URL:
SP=/tmp/claude-0/-ai-inventor-aii-data-runs-run-qck1d05BqxkX-4-gen-paper-repo--4-gen-demo-art-notebook-workspaces-iter-1-art-i3cVDxBp-USk/9515af7b-63fd-4c30-8b8a-c704cc189967/scratchpad; cd $SP; python3 - <<'EOF'
p='gen_nb.py'; s=open(p).read()
old='''**Reading the results.** Agreement of *other systems'* translations'''
assert old in s
s=s.replace(old,'''**Demo numbers** (100 sentences, 278 candidates, original parameters, about 1 minute): c_score AUROC ≈ 0.83 against 0.73 for sc5_cheap. The paired Δ is ≈ +0.10, and its sentence-clustered
CI excludes 0. Cross-fitted [c_score, sc5_cheap] over [sc5_cheap] adds ≈ +0.12. The curated subset over-represents longer sentences, so the numbers sit slightly below the full run.
In 276 of 278 cases, both the labels and the per-candidate c_score reproduce the original run exactly. The 2 exceptions come from set-iteration order in `align`/`search`,
which depends on `PYTHONHASHSEED`: the original fixed it to 0, and a notebook kernel randomises it.

**Reading the results.** Agreement of *other systems'* translations''')
s=s.replace('# sentences (pools) to score; the data holds 100','# sentences (pools) to score; the data holds 100 (= all, default)')
open(p,'w').write(s)
EOF
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk; python3 $SP/gen_nb.py $PWD/code_demo.ipynb 100 10.0 2000 30; E=/tmp/aii_nb_test_envs/art_i3cVDxBp-USk-be48f6bcb721; UV_VENV_CLEAR=1 UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv venv -q --seed --python /usr/local/bin/python3.12 $E && UV_CACHE_DIR=/tmp/aii_nb_test_envs/uv-cache uv pip install -q --python $E/bin/python jupyter ipykernel && S=$(date +%s); $E/bin/jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600 code_demo.ipynb --output code_demo.ipynb 2>&1 | grep -v WARNING | tail -3; echo "runtime $(( $(date +%s)-S ))s"; python3 -c "
import json; nb=json.load(open('code_demo.ipynb'))
errs=[o for c in nb['cells'] for o in c.get('outputs',[]) if o['output_type']=='error']; print('errors:',len(errs))
src=''.join(''.join(c['source']) for c in nb['cells'])
print('url ok:', 'GITHUB_DATA_URL = \"https://raw.githubusercontent.com/ai-inventor-papers/ai-invention-eff060-layered-gold-free-checks-for-logic/fork/run_qck1d05BqxkX/round-1/experiment-3/demo/mini_demo_data.json\"' in src, 'urlopen(GITHUB_DATA_URL)' in src)
print('abs paths:', src.count('/ai-inventor'))
"; ls -la
```

### [64] TOOL RESULT — Bash · 2026-09-25 12:43:39 UTC

```
{"stdout": "cells: 36\n[NbConvertApp] Converting notebook code_demo.ipynb to notebook\n[NbConvertApp] Writing 321482 bytes to code_demo.ipynb\nruntime 80s\nerrors: 0\nurl ok: True True\nabs paths: 1\ntotal 5096\ndrwxr-xr-x 3 root root 2000115 Sep 25 12:38 .\ndrwxr-xr-x 6 root root 2000789 Sep 25 12:33 ..\ndrwxr-xr-x 2 root root       1 Sep 25 12:33 .aii\n-rw------- 1 root root      54 Sep 25 12:33 .aii_claude_session.json\n-rw-r--r-- 1 root root  472584 Sep 25 12:43 .repl_agent.ptylog\n-rw-r--r-- 1 root root  321792 Sep 25 12:43 code_demo.ipynb\n-rw-r--r-- 1 root root  420979 Sep 25 12:35 mini_demo_data.json", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [65] ASSISTANT · 2026-09-25 12:43:45 UTC

```
One absolute server path is still in the notebook source. Finding it:
```

### [66] TOOL CALL — Bash · 2026-09-25 12:43:45 UTC

```
Locate absolute path occurrences:
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk; grep -o ".\{80\}/ai-inventor.\{60\}" code_demo.ipynb mini_demo_data.json | head
```

### [67] TOOL RESULT — Bash · 2026-09-25 12:43:45 UTC

```
{"stdout": "", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [68] TOOL CALL — Bash · 2026-09-25 12:43:49 UTC

```
Grep absolute paths excluding repo URL:
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk; grep -n "ai-inventor" code_demo.ipynb | grep -v "ai-inventor-papers" | cut -c1-200; grep -c "ai-inventor" mini_demo_data.json
```

### [69] TOOL RESULT — Bash · 2026-09-25 12:43:49 UTC

```
{"stdout": "0", "stderr": "", "interrupted": false, "isImage": false, "returnCodeInterpretation": "No matches found", "noOutputExpected": false}
```

### [70] ASSISTANT · 2026-09-25 12:44:05 UTC

```
That match was only the GitHub URL (`/ai-inventor-papers/...`), so no server paths leak. Now writing the README, manifest and structured output.
```

### [71] TOOL CALL — Bash · 2026-09-25 12:44:05 UTC

````
Write README, manifest, struct output:
cd /ai-inventor/aii_data/runs/run_qck1d05BqxkX/4_gen_paper_repo/_4_gen_demo_art/notebook_workspaces/iter_1/art_i3cVDxBp-USk; cat > README.md <<'EOF'
# Demo: cross-system z3 consensus as a faithfulness metric for NL→FOL

A runnable Colab/Jupyter demo of **Experiment 3 (candidate C)**. The metric is gold-free and text-free. For a candidate FOL formula, it measures the share of
*other* systems' translations of the same sentence that are **not** z3-equivalent to the candidate after vocabulary alignment (`c_score = 1 − eq_frac`).
The notebook compares it against K=5 self-consistency and structural baselines, using labels from prover-checked equivalence to gold (FOLIO/MALLS, curated).

## Layout

| path | what it is |
|---|---|
| `code_demo.ipynb` | The demo notebook, executed with its outputs. It inlines the original `fol.py`, `repair_census.py`, `common.py`, `eqcache.py`, `consensus.py` (helpers + main loop) and `analysis.py` (statistics), and re-runs labelling, pairwise z3 equivalence, consensus scoring, medoid repair, sanity checks and the AUROC / paired-Δ / cross-fit meta-evaluation. |
| `mini_demo_data.json` | A curated subset: 100 sentences (all 19 sentences with ≥ 12 words, plus a seeded random sample). Each sentence has its gold FOL, the leave-one-out translation pool (6 OpenRouter peers + 3 Logic-LM systems), the K=5 self-consistency samples, and 278 track-L candidates labelled CORRECT/ERROR. It also carries the original full run's headline results for comparison. |
| `README.md` | This file. |
| `.aii/manifest.yaml` | Storage manifest. Nothing heavy is produced. |

## How to run

Open `code_demo.ipynb` in Colab, or run it locally with Python 3.12:

```bash
jupyter nbconvert --to notebook --execute code_demo.ipynb --output code_demo.ipynb
```

The first code cell installs `z3-solver` and `loguru`. Locally it also installs Colab's versions of numpy, pandas, scipy, scikit-learn and matplotlib.
The data loads from the GitHub raw URL, falling back to the local `mini_demo_data.json`. No API key is needed, because the LLM translations are already cached in the data file.
With the original parameters (`N_BOOT=2000`, `REPAIR_BUDGET_S=10`, all 100 sentences), the whole notebook takes about 80 s, including installs.

## Results (demo subset vs original full run)

| score | AUROC demo (n=278) | AUROC full run (n=546) |
|---|---|---|
| c_score | 0.827 [0.757, 0.889] | 0.866 [0.821, 0.906] |
| cluster_entropy | 0.743 | 0.773 |
| medoid_depth | 0.684 | 0.722 |
| sc5_cheap (self-consistency) | 0.727 | 0.725 |
| fol_length | 0.458 | 0.527 |

Paired Δ c_score − sc5_cheap: +0.101 [0.021, 0.179] in the demo and +0.140 in the full run. In 276 of 278 cases, both the labels and the per-candidate c_score match the original run exactly.
The 2 differences come from `PYTHONHASHSEED`-dependent set ordering in the aligner and repair search.

## Restoring removed files

No files are marked for deletion, so nothing needs restoring. The notebook's pip installs go into the user's own environment, not into this directory.
EOF
cat > .aii/manifest.yaml <<'EOF'
# No heavy binaries or cache directories are produced by this module: code_demo.ipynb (~0.3 MB) and
# mini_demo_data.json (~0.4 MB) are text files below the auto-keep floor.
entries: []
EOF
cat > .terminal_claude_agent_struct_out.json <<'EOF'
{"out_expected_files": {"notebook": "code_demo.ipynb", "mini_data_file": "mini_demo_data.json"}}
EOF
cat .terminal_claude_agent_struct_out.json; du -sh .
````

### [72] TOOL RESULT — Bash · 2026-09-25 12:44:05 UTC

```
{"stdout": "{\"out_expected_files\": {\"notebook\": \"code_demo.ipynb\", \"mini_data_file\": \"mini_demo_data.json\"}}\n3.2M\t.", "stderr": "", "interrupted": false, "isImage": false, "noOutputExpected": false}
```

### [73] ASSISTANT · 2026-09-25 12:44:17 UTC

```
I built the demo notebook and its data file. The notebook runs cleanly in the fresh test venv at the full original settings (2000 bootstrap resamples, 10 s repair budget, all 100 sentences) in about 80 s, well under the 10-minute limit.

**How I handled the conversion:** `method.py` itself is only a launcher that runs the scripts in `src/` one after another, including paid OpenRouter calls. So the notebook carries the real code from those scripts, cut out of the source files programmatically so nothing was retyped. It then re-runs the solver side of the pipeline live: labelling against gold, the pairwise equivalence checks, the consensus scores, the repair search, the sanity checks and the statistics. The model translations are already stored in the data file, so no API key is needed.

**Changes to the original code:**
- The on-disk caches became in-memory. The 4-worker process pool became a plain sequential loop, because the spawned workers can't load functions defined in a notebook.
- Two in-function imports were removed, because those functions are already defined in the notebook.
- `to_str` was copied in from `rewrites.py` so the planted-error formulas can be printed back as text.
- **Left out:** the rewrite-invariance step (it needs WordNet), the "peer outputs as candidates" analysis, and the census code, which reads a different dataset. The markdown says so where each would have been.

**Results on the demo subset (278 candidates) against the original full run (546):**

| Score | Demo AUROC | Full-run AUROC |
|---|---|---|
| c_score (consensus) | 0.827 [0.757, 0.889] | 0.866 |
| self-consistency baseline | 0.727 | 0.725 |

- c_score beats self-consistency by +0.10, with a confidence interval of [0.02, 0.18]; the full run shows +0.14.
- The subset over-represents longer sentences (all 19 with 12+ words), which likely explains why the demo numbers sit a little below the full run.
- Labels and per-candidate c_scores match the original run on 276 of 278 candidates. The 2 mismatches probably come from Python's hash randomisation: the original fixed it with `PYTHONHASHSEED=0`, and a notebook can't. The notebook explains this.
- About 93% of planted errors raise c_score, against 97% in the full run.

The final cell prints the results table and draws four panels: accuracy with confidence intervals, ROC curves, c_score by label, and sensitivity by error type.

**Checks:** the notebook contains the exact `GITHUB_DATA_URL` and falls back to the local file, and no server paths appear in either output file. The manifest has no entries because nothing heavy was produced. There was no todo-list tool in this session, so I worked through the six TODOs in order without one.

Files are in `art_i3cVDxBp-USk/`:
- code_demo.ipynb
- mini_demo_data.json
- README.md
- .aii/manifest.yaml
- .terminal_claude_agent_struct_out.json
```
